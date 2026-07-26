"""
Captures feed posts from LinkedIn by connecting via CDP to YOUR real
Chrome (already logged in normally), instead of opening a separate
automated browser. See references/linkedin-safety-limits.md for why.

Before running:
  google-chrome --remote-debugging-port=9222
  (log into LinkedIn manually in that window, as you always do)

Usage (run at most 1x/day, few rounds):
  python linkedin_capture.py --rounds 4
"""
import argparse
import asyncio
import json
import random
import time
from pathlib import Path
from playwright.async_api import async_playwright

OUT_DIR = Path("data/raw")
VOYAGER_MARKER = "voyager/api"  # LinkedIn's internal API


async def capture(rounds: int):
    if rounds > 6:
        raise SystemExit(
            "More than 6 rounds on LinkedIn increases the risk of an account "
            "flag. Run it again tomorrow instead of increasing volume now."
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    captured = []

    async def on_response(response):
        if VOYAGER_MARKER in response.url and "feed" in response.url:
            try:
                data = await response.json()
                captured.append({"url": response.url, "data": data})
            except Exception:
                pass

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            raise SystemExit(
                "Could not connect to Chrome. Open it with "
                "'google-chrome --remote-debugging-port=9222' and log into LinkedIn first.\n"
                f"Original error: {e}"
            )

        context = browser.contexts[0]
        page = await context.new_page()
        page.on("response", on_response)

        await page.goto("https://www.linkedin.com/feed/")
        await page.wait_for_timeout(4000)

        for i in range(rounds):
            await page.mouse.wheel(0, random.randint(800, 1400))
            # longer delays than X -- LinkedIn detects cadence faster
            await page.wait_for_timeout(random.randint(3000, 6000))
            print(f"round {i + 1}/{rounds} — {len(captured)} responses captured so far")

        await page.close()
        # don't close the browser -- it's the user's real Chrome

    ts = int(time.time())
    out_path = OUT_DIR / f"linkedin_feed_{ts}.json"
    out_path.write_text(json.dumps(captured, ensure_ascii=False, indent=2))
    print(f"Saved: {out_path} ({len(captured)} responses)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=4)
    args = parser.parse_args()
    asyncio.run(capture(args.rounds))
