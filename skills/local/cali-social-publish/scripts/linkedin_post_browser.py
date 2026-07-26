"""
Fills in the new post box on LinkedIn by reusing the CDP session from your
real Chrome (same pattern as social-listening's linkedin_capture.py).

Does NOT click "Post" -- that's left to you, on purpose. LinkedIn's
detection is about the session looking automated end-to-end; leaving the
final click human breaks that pattern even while reusing the session to
fill in the text.

Before running:
  google-chrome --remote-debugging-port=9222
  (logged into LinkedIn normally)

Usage:
  python linkedin_post_browser.py --text "your post here"
"""
import argparse
import asyncio
import random
from playwright.async_api import async_playwright


async def prefill(text: str):
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
        await page.goto("https://www.linkedin.com/feed/")
        await page.wait_for_timeout(random.randint(2000, 3500))

        start_post_button = page.get_by_role("button", name="Start a post")
        await start_post_button.click()
        await page.wait_for_timeout(random.randint(1000, 1800))

        editor = page.locator(".ql-editor").first
        await editor.click()
        for chunk in [text[i:i + 10] for i in range(0, len(text), 10)]:
            await editor.type(chunk, delay=random.randint(20, 60))
            await page.wait_for_timeout(random.randint(40, 150))

        print(
            "Post box filled in on LinkedIn. Review it and click 'Post' "
            "manually -- this script does not publish on its own."
        )
        # don't close the browser -- it's the user's real Chrome, and the
        # post stays open waiting for the manual click


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    asyncio.run(prefill(args.text))
