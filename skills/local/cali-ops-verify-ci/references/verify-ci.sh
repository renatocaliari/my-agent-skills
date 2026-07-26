#!/usr/bin/env bash
# verify-ci.sh — deterministic CI + live-deploy verifier.
# Uses gh's embedded --jq (gojq); only `gh` + `curl` required (no jq binary).
# Emits a single JSON line; exits 0 (verified) / 1 (needs attention).
#
# Usage: verify-ci.sh <repo-slug> [live-url] [expect-file]
#   repo-slug   : "gogogo" (-> calionauta/gogogo) or "owner/repo"
#   live-url    : optional URL to byte-diff / HTTP-check
#   expect-file : optional local file whose content should match live-url
# Env: VERIFY_CI_MAX_WAIT (sec, default 120), VERIFY_CI_POLL (sec, default 15)

set -o pipefail

REPO_IN="${1:-}"
LIVE_URL="${2:-}"
EXPECT_FILE="${3:-}"
MAX_WAIT="${VERIFY_CI_MAX_WAIT:-120}"
POLL="${VERIFY_CI_POLL:-15}"

if [ -z "$REPO_IN" ]; then
  echo '{"error":"usage: verify-ci.sh <repo-slug> [live-url] [expect-file]"}' >&2
  exit 2
fi

case "$REPO_IN" in
  */*) REPO="$REPO_IN" ;;
  *)   REPO="calionauta/$REPO_IN" ;;
esac

if ! command -v gh >/dev/null 2>&1; then echo '{"error":"gh CLI not found"}'; exit 1; fi
if ! command -v curl >/dev/null 2>&1; then echo '{"error":"curl not found"}'; exit 1; fi

notes=""
add_note() { if [ -z "$notes" ]; then notes="$1"; else notes="$notes"$'\n'"$1"; fi; }
json_escape() { printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'; }

pending="false"
deploy_live="null"
url=""

# 1) latest run on default branch (single call; gh embedded --jq, no jq binary)
IFS=$'\t' read -r run_id status conclusion url < <(gh run list --repo "$REPO" --limit 1 \
  --json databaseId,status,conclusion,url \
  --jq '.[0] | "\(.databaseId)\t\(.status)\t\(.conclusion // "")\t\(.url // "")"' 2>/dev/null)

if [ -z "$run_id" ] && [ -z "$status" ]; then
  printf '{"repo":"%s","run_id":null,"ci_status":"unknown","conclusion":null,"pending":false,"deploy_live":null,"url":"","notes":["no workflow runs found"]}\n' "$REPO"
  exit 1
fi

# 2) bounded wait if still running (never indefinite)
elapsed=0
timed_out="false"
while [ "$status" = "in_progress" ] || [ "$status" = "queued" ] || [ "$status" = "requested" ]; do
  if [ "$elapsed" -ge "$MAX_WAIT" ]; then
    timed_out="true"
    add_note "run $run_id still $status after ${MAX_WAIT}s; not waiting further"
    break
  fi
  sleep "$POLL"
  elapsed=$((elapsed + POLL))
  status="$(gh run list --repo "$REPO" --limit 1 --json status --jq '.[0].status // "unknown"' 2>/dev/null)"
done
pending="$timed_out"

# refresh final status + conclusion after any wait
IFS=$'\t' read -r status conclusion < <(gh run list --repo "$REPO" --limit 1 \
  --json status,conclusion \
  --jq '.[0] | "\(.status)\t\(.conclusion // "")"' 2>/dev/null)

ci_status="$status"
[ -n "$conclusion" ] && ci_status="$conclusion"

# 3) optional live deploy byte-diff / HTTP check
if [ -n "$LIVE_URL" ]; then
  if [ -n "$EXPECT_FILE" ] && [ -r "$EXPECT_FILE" ]; then
    live="$(curl -fsSL --max-time 20 "$LIVE_URL" 2>/dev/null)" || live=""
    if [ -z "$live" ]; then
      deploy_live="false"; add_note "live URL unreachable: $LIVE_URL"
    elif diff <(printf '%s\n' "$live") "$EXPECT_FILE" >/dev/null 2>&1; then
      deploy_live="true"
    else
      deploy_live="false"; add_note "live content differs from $EXPECT_FILE"
    fi
  else
    code="$(curl -fsS -o /dev/null -w '%{http_code}' --max-time 20 "$LIVE_URL" 2>/dev/null || echo 000)"
    if [ "$code" = "200" ]; then deploy_live="true"; else deploy_live="false"; add_note "live URL HTTP $code"; fi
  fi
fi

# 4) emit JSON (manual build; no jq binary)
conclusion_out="null"; [ -n "$conclusion" ] && conclusion_out="\"$conclusion\""
run_id_out="null";     [ -n "$run_id" ] && run_id_out="$run_id"
url_out="$(json_escape "$url")"
notes_json="["
first=1
while IFS= read -r line; do
  [ -z "$line" ] && continue
  [ $first -eq 1 ] && first=0 || notes_json="$notes_json,"
  notes_json="$notes_json\"$(json_escape "$line")\""
done <<< "$notes"
notes_json="$notes_json]"

printf '{"repo":"%s","run_id":%s,"ci_status":"%s","conclusion":%s,"pending":%s,"deploy_live":%s,"url":"%s","notes":%s}\n' \
  "$REPO" "$run_id_out" "$ci_status" "$conclusion_out" "$pending" "$deploy_live" "$url_out" "$notes_json"

# 5) exit semantics
case "$ci_status" in
  success) exit 0 ;;
  *) exit 1 ;;
esac
