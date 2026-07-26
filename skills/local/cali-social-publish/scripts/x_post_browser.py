"""
Posts on X by reusing the SAME persistent session from social-listening
(~/.social-listening/x-state.json) -- no paid API, no setup beyond the
login you already did once.

Risk: low. Posts own content, low frequency (normal usage), not mass
engagement. Still technically automation -- avoid running it at high
frequency or with a perfectly regular cadence.

Usage:
  python x_post_browser.py --text "your post here"
"""
import argparse
import asyncio
import random
from pathlib import Path
from playwright.async_api import async_playwright

STATE_PATH = Path.home() / ".social-listening" / "x-state.json"


async def post(text: str):
    if not STATE_PATH.exists():
        raise SystemExit(
            f"Session not found at {STATE_PATH}. "
            "Run social-listening/scripts/x_login_once.py first."
        )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=str(STATE_PATH))
        page = await context.new_page()
        await page.goto("https://x.com/compose/post")
        await page.wait_for_timeout(random.randint(1500, 2500))

        box = page.get_by_test_id("tweetTextarea_0")
        await box.click()
        # type in chunks with delay -- human typing cadence,
        # don't paste the whole text at once
        for chunk in [text[i:i + 8] for i in range(0, len(text), 8)]:
            await box.type(chunk, delay=random.randint(20, 60))
            await page.wait_for_timeout(random.randint(30, 120))

        await page.wait_for_timeout(random.randint(800, 1500))
        post_button = page.get_by_test_id("tweetButton")
        await post_button.click()
        await page.wait_for_timeout(2000)

        print("Post published on X.")
        await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    asyncio.run(post(args.text))
