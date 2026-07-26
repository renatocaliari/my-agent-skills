---
name: cali-ops-verify-ci
description: "Deterministically verify a GitHub repo's CI status and (optionally) live deployment without blocking the agent. Triggers when: an agent needs to confirm CI is green after a push/merge/release, a multica Autopilot schedules a periodic CI/deploy check, or an aborted/idle-watchdog run needs post-verification. Covers: bounded gh run polling (never indefinite wait), JSON status output, and optional byte-diff of a live URL against a repo reference file. Use instead of blocking on `gh run watch`."

metadata:
  frequency: daily
  category: infra
  context-cost: low
---

# Verify CI

Deterministic CI + live-deploy checker. Runs fast (<2 min), never blocks
indefinitely, and returns structured JSON so an agent can decide what to do
without waiting synchronously.

## When to use

- After a push/merge/release and you need to confirm CI is green.
- As the engine behind a multica Autopilot (schedule or GitHub webhook) that
  periodically checks repos.
- After an aborted/idle-watchdog run, to verify what actually shipped.
- **Never** block on `gh run watch` — call this script and act on its JSON.

## Procedure

Run the bundled script:

```bash
bash ~/.agents/skills/cali-ops-verify-ci/references/verify-ci.sh <repo-slug> [live-url] [expect-file]
```

Arguments:
- `repo-slug`   — bare name resolves to `calionauta/<slug>` (e.g. `calionauta/gogogo-fullstack-template`); or pass `owner/repo`.
- `live-url`    — optional URL to byte-diff / HTTP-check.
- `expect-file` — optional local file whose content should match `live-url`.

Output (single JSON line):

```json
{
  "repo": "calionauta/gogogo",
  "run_id": 12345,
  "ci_status": "success",
  "conclusion": "success",
  "pending": false,
  "deploy_live": true,
  "url": "https://github.com/.../actions/runs/12345",
  "notes": []
}
```

Exit code: `0` = verified OK (`ci_status: success`); `1` = needs attention
(failure / still in_progress after cap / unknown / live mismatch).

### Env overrides
- `VERIFY_CI_MAX_WAIT` (default `120`) — seconds to wait for an in-progress run.
- `VERIFY_CI_POLL` (default `15`) — poll interval seconds.

## Autopilot / scheduler usage (multica)

A multica Autopilot (schedule `*/15 * * * *`, mode `run_only`) can prompt an
agent:

> Use the `cali-ops-verify-ci` skill to check recent pushes across
> `calionauta/gogogo` and `calionauta/multica`. If `ci_status` is not
> `success` or `deploy_live` is false, post a comment on the relevant issue
> and attempt a minimal fix or escalation.

The agent calls the script (deterministic) and only interprets the JSON —
keeping the check itself token-free and stall-proof.

## Pitfalls

- Script needs `gh` authed + `curl` only (uses gh's embedded `--jq` / gojq; **no standalone `jq` binary required** — verified absent on the deploy server).
- Do NOT replace this with a raw `gh run watch` loop — that is what got an
  agent idle-killed before (indefinite wait → 30m idle watchdog).
- Byte-diff compares exact content; if the live page is templated/dynamic,
  prefer the HTTP-200 check (omit `expect-file`).
- `repo-slug` without `/` defaults to `calionauta/*` — pass `owner/repo`
  for other orgs.

## Verification

```bash
# green CI only
bash ~/.agents/skills/cali-ops-verify-ci/references/verify-ci.sh calionauta/gogogo-fullstack-template
# with live deploy check
bash ~/.agents/skills/cali-ops-verify-ci/references/verify-ci.sh calionauta/gogogo-fullstack-template https://gogogo.calionauta.com/ index.html
echo $?   # 0 = ok, 1 = attention
```
