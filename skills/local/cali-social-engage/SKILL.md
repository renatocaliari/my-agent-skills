---
name: cali-social-engage
description: Creates draft replies/comments for X or LinkedIn posts identified by the social-listening skill, and optionally publishes on X (never automatically on LinkedIn). Use ONLY when the user explicitly asks to "reply", "comment", "draft a reply", or "post" something — never trigger this automatically after running social-listening without the user asking.
---

# Social Engage

Separate, opt-in skill for interaction. By default it only **drafts** —
actual publishing requires explicit confirmation every time, and on
LinkedIn it doesn't even offer automated publishing (see below).

This is intentional: reading/analysis (`social-listening`) and action
(`social-engage`) are two skills with different purposes, so running one
never triggers the other without the user deciding.

## Configuration

`config.yaml` (same file as social-listening, `engage` section):

```yaml
engage:
  auto_post_x: false   # safe default. Only true if the user explicitly asks
  tone: "direct, no marketing jargon, shares real experience"
```

The `auto_post_x` flag for automated posting exists, but **the default is
false and should stay false unless the user asks to change it**. Even with
`true`, always confirm the final text with the user before publishing in
that specific session -- the flag turns on the capability, it doesn't
replace per-post confirmation.

## Flow — X

1. The user points to a post from `data/ranked.json` (or pastes a link).
2. Draft the reply with `scripts/draft_reply.py` or directly — short, in
   the configured tone, citing real experience from the user when it makes
   sense (never invent experience they don't have).
3. Show the draft and ask if it's okay to post.
4. Only call `scripts/post_x_reply.py` after explicit confirmation in this
   conversation — regardless of the `auto_post_x` value.

## Flow — LinkedIn

**No automated publishing here, full stop.** The account risk on LinkedIn
(see `social-listening/references/linkedin-safety-limits.md`) isn't worth
it for a low-frequency action like commenting. The flow is:

1. Draft the comment text (same process as X).
2. Open the post link for the user.
3. They paste it manually. Slower, but keeps the account safe.

## Commands

```bash
python scripts/draft_reply.py --post-id <id> --ranked data/ranked.json
python scripts/post_x_reply.py --post-id <id> --text "..."   # only after confirmation
```
