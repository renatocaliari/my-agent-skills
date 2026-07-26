---
name: cali-social-publish
description: Creates and publishes NEW, original posts to your own X and/or LinkedIn feed, from direct text, a local .md file, or a reference URL. Expands the source into full post(s), generates variations/alternatives, and publishes by reusing an already-logged-in browser session (free) or via official API (configurable per platform). Supports automatic mode (publishes without human choice) and review mode (shows alternatives and waits for confirmation). Use when the user asks to "create a post about X", "turn this article/markdown into a post", "publish to my feed", or "post something based on [reference]". Do NOT use this to reply/comment on other people's posts — that's the `social-engage` skill. Do NOT use this to read/analyze timelines — that's `social-listening`.
---

# Social Publish

Creates original posts for your own feed from a reference (text, local
`.md` file, or URL) and publishes by reusing the browser session already
logged in by `social-listening` (free, no extra setup) or via the official
API (configurable per platform, see below). This is why the risk profile is
completely different from `social-engage`: posting your own content, at low
frequency, is not the same pattern as mass engagement on other people's
posts.

## Official API vs. reused browser -- the two options

There are two ways to actually publish, configurable per platform in
`config.yaml` (`posting_method`):

**`browser`** (suggested default) — reuses the SAME persistent session that
`social-listening` already uses (`~/.social-listening/x-state.json` on X,
CDP on your real Chrome on LinkedIn). Free, zero extra setup beyond the
login you already did once. On X, it actually publishes. On LinkedIn, it
**fills the post box and stops** — the final click on "Post" is yours, on
purpose (see why below).

**`api`** — uses each platform's official API (X: pay-per-use, ~$0.015 per
post; LinkedIn: `w_member_social`, free but with app/OAuth setup). Zero
detection ambiguity, but more configuration friction.

### Why the `browser` mode doesn't auto-publish on LinkedIn

LinkedIn's detection is about whether the **session** looks automated
end-to-end — browser fingerprinting, click/scroll biometrics, request
velocity (see `social-listening/references/linkedin-safety-limits.md`).
This doesn't distinguish "posting" from "commenting": what matters is
whether the entire session, from login to the final action, looks bot-like.
Leaving the final publish click manual breaks that end-to-end pattern even
while reusing the session to fill in the text -- and it still saves you the
tedious part (retyping everything).

If you want fully hands-off publishing on LinkedIn, switch
`posting_method.linkedin` to `api` — that's the official, sanctioned route,
without this caveat.

On X the risk is much lower (own content, low frequency, not mass
engagement), so there the `browser` mode actually publishes.

## Setup (once)

- **`browser` method** (default): no extra setup if you've already run
  `social-listening/scripts/x_login_once.py` and already have Chrome open
  with `--remote-debugging-port=9222` logged into LinkedIn. Reuses all of that.
- **`api` method** (optional, per platform):
  - **X**: create an app at developer.x.com, generate API key/secret +
    access token/secret (user context). Save as environment variables:
    `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET`.
    See `references/x-api-setup.md`.
  - **LinkedIn**: run `scripts/linkedin_oauth_setup.py` once — it opens the
    OAuth flow in the browser, saves the access token (valid 60 days) and
    the refresh token (valid 365 days) to
    `~/.social-publish/linkedin-token.json`. See `references/linkedin-api-setup.md`.
- Copy `config.example.yaml` to `config.yaml` and adjust `tone`,
  `posting_method` per platform, and the default mode (`auto` or `review`).

## Flow

```bash
# from direct text
python scripts/generate_variants.py --source text \
  --input "loose idea about what I learned today with X" \
  --platform both --n-variants 3 --mode review

# from a local markdown file
python scripts/generate_variants.py --source file \
  --input ./notes/pi-stack-learnings.md \
  --platform x --n-variants 3 --mode review

# from a reference URL (becomes inspiration, never copied verbatim)
python scripts/generate_variants.py --source url \
  --input https://example.com/article --platform linkedin \
  --n-variants 3 --mode auto
```

The script generates the variations and saves them to
`data/variants_<timestamp>.json`. After choosing (or automatically, in
`auto` mode), the final text goes to the post script matching the
configured `posting_method`:

| Platform | `browser`                  | `api`               |
|---|---|---|
| X        | `scripts/x_post_browser.py` (actually posts) | `scripts/x_post.py` |
| LinkedIn | `scripts/linkedin_post_browser.py` (fills in, you click post) | `scripts/linkedin_post.py` |

### `review` mode (default)

The script stops after generating the variations and shows them. You pick
which to publish (or ask for a tweak), and only then is the matching post
script called with the final text. **Nothing is published without this
explicit confirmation** (and on LinkedIn/browser, the final click stays
manual even after that).

### `auto` mode

`generate_variants.py` itself picks the best variation (the one the
generation pass marked `"recommended": true`) and calls the matching post
script right away, without waiting for text confirmation. Use this only for
flows you already trust — e.g. a daily cron publishing from notes you've
already reviewed before they became `.md` files. On LinkedIn/browser, even
in `auto` mode, the final publish click stays yours -- "auto" here means
"no choosing between variations", not "no human involvement whatsoever".

## About the source being a URL

When the source is a URL, it's treated as **reference/inspiration**, never
as text to reproduce. Generation should paraphrase the core idea in its own
words -- never paste excerpts from the original article into the post. This
matters both for copyright and because a post that's just a paraphrase of
another article lacks the real voice/experience that makes it worth posting.

## Reference files

- `references/x-api-setup.md` — how to create the X app and generate credentials
- `references/linkedin-api-setup.md` — how to create the LinkedIn app and run OAuth
