---
name: cali-social-listening
description: Reads and analyzes X/Twitter and LinkedIn timelines to summarize information, detect conversation patterns, and rank posts worth engaging with. Use whenever the user asks to "read the feed", "see what people are saying about X", "summarize recent tweets/posts", "find patterns", or "where could I comment" on X or LinkedIn — even if they don't use the word "scraping" or "skill". This skill is READ-ONLY: it never posts, comments, or likes anything. For interacting/replying, use the separate `social-engage` skill.
---

# Social Listening

Read-only pipeline to capture, summarize, and rank posts from X and LinkedIn.
**Never posts anything.** Interaction is a separate, opt-in skill
(`social-engage`) — never trigger its actions from here without the user
explicitly asking.

## Why X and LinkedIn use different strategies

The two sites have very different bot-detection profiles in 2026:

- **X**: GraphQL response interception is resilient and the anti-bot system
  is tolerable for moderate automated scrolling.
- **LinkedIn**: a session-fingerprinting update (Q1 2026) flags automation
  patterns within ~48h, with direct suspension instead of a warning.
  High-volume automated scrolling is a real account risk. That's why
  LinkedIn here runs in manual/light mode, reusing the user's real browser
  session.

Never apply the X capture script to LinkedIn or vice versa.

## Setup (once)

1. `pip install playwright langdetect --break-system-packages && playwright install chromium`
2. Run `scripts/x_login_once.py` to open a visible Chromium window, log
   into X manually, and save the session to `~/.social-listening/x-state.json`.
   After that, it never asks for login again.
3. There's no separate session setup for LinkedIn — the script connects to
   the user's real Chrome via CDP (see `references/linkedin-safety-limits.md`).
4. Edit `config.yaml` (copy from `config.example.yaml`) with: handles/topics
   that matter, languages (`pt-BR`, `en`), scroll rounds, output directory.

## Flow

1. **Capture** — `scripts/x_capture.py` (X) and/or `scripts/linkedin_capture.py`
   (LinkedIn) → raw JSON dumps in `data/raw/`.
2. **Rank** — `scripts/score_rank.py` filters by language, computes
   engagement velocity, reply competition, and topic relevance →
   `data/ranked.json`.
3. **Patterns + final rerank (you do this, not a script)** — read
   `data/ranked.json` (top ~30) and:
   - Group by recurring theme/tone (what people are talking about, how
     they're talking about it).
   - For each post in the top 30, honestly assess: "do I actually have real
     experience to contribute here, or does this just match keywords?"
     Cut the ones that are only keyword coincidence without a genuine angle.
   - Produce a short digest: 3-5 observed patterns + a final list of posts
     with a suggested angle for contributing (not the reply text itself —
     that's `social-engage`).

## Capture commands

```bash
# X — 10 scroll rounds (default), home timeline + search by config terms
python scripts/x_capture.py --source home --rounds 10
python scripts/x_capture.py --source search --query "agentic coding" --rounds 10

# LinkedIn — manual, light, at most 1x/day, 3-5 rounds
python scripts/linkedin_capture.py --rounds 4

# Rank what was captured
python scripts/score_rank.py --input data/raw/ --output data/ranked.json \
  --languages pt,en
```

## Scoring (what `score_rank.py` computes)

- **Engagement velocity**: `(likes + reposts + replies) / minutes_since_post`
- **Reply competition**: inverse of reply count — fewer existing replies =
  more room/visibility for a new comment
- **Topic relevance**: keyword/topic match against `config.yaml`
  (swap for embeddings later if you want something more precise)

The final score is a weighted combination configurable in `config.yaml`
(`weights: {velocity: 0.4, reply_gap: 0.3, relevance: 0.3}`).

## Reference files

- `references/x-graphql-endpoints.md` — which endpoints to intercept and why
- `references/linkedin-safety-limits.md` — safe limits and why the mode differs
