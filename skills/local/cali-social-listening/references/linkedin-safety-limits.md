# LinkedIn — why the mode here differs from X

## What changed in 2026

LinkedIn's session-fingerprinting system (Q1 2026 update) now flags bot
patterns within ~48h of use (it used to take weeks). A first violation now
usually results in direct suspension instead of a warning. Sessions
recreated on every request, perfectly regular cadence, and navigation
limited to search/feed pages (no message timeline, no organic dwell time)
are the strongest detection signals.

## That's why LinkedIn capture here is:

1. **Manual, never scheduled.** Only run it when you decide to, not on a cron.
2. **Via CDP on your real Chrome**, not a separate Playwright profile —
   reuses cookies, fingerprint, and browsing history you already have:
   ```bash
   # open Chrome with remote debugging on, logged in normally
   google-chrome --remote-debugging-port=9222
   ```
   The script connects to that port via `browser_type.connect_over_cdp(...)`
   instead of opening a fresh browser.
3. **Few scroll rounds** (3–5, never 10+) with longer delays than on X
   (3–6s, with variation).
4. **At most once a day.** If you need more data, it's better to wait until
   the next day than to increase volume within the same session.
5. **No automated posting/liking** — that's even more sensitive than
   reading and is deliberately out of scope for the `social-engage` skill
   on LinkedIn (see that SKILL.md).

## If you ever need higher volume

At that point it stops being "reading your own feed with automation help"
and becomes real scraping — the safer route for the account is a managed
service that absorbs the detection surface (e.g. offerings that run an
authenticated session with residential IP and their own rate limiting), not
DIY. But for the use case here — summarizing your own feed and finding
patterns — the manual mode above is enough and keeps risk low.
