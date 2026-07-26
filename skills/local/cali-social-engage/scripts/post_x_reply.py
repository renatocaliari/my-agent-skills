"""
Posts a reply on X reusing the persistent session saved by x_login_once.py
(social-listening skill).

Only call this after explicit confirmation from the user IN THIS
CONVERSATION, regardless of the auto_post_x config value. There's no
LinkedIn equivalent on purpose -- see SKILL.md.

Usage:
  python post_x_reply.py --post-id <id> --text "your reply here"

Safety note: even with a visible browser and a manual confirmation step,
this script deliberately does NOT click the final "Reply" button -- that
stays with the human, always.
"""
import argparse
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

STATE_PATH = Path.home() / ".social-listening" / "x-state.json"


async def post_reply(post_id: str, text: str):
    if not STATE_PATH.exists():
        raise SystemExit(
            f"Session not found at {STATE_PATH}. "
            "Run social-listening/scripts/x_login_once.py first."
        )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # visible on purpose
        context = await browser.new_context(storage_state=str(STATE_PATH))
        page = await context.new_page()
        await page.goto(f"https://x.com/i/status/{post_id}")
        await page.wait_for_timeout(2000)

        reply_box = page.get_by_test_id("tweetTextarea_0")
        await reply_box.click()
        await reply_box.fill(text)

        print(
            "Draft filled in the X window. Review it and click 'Reply' "
            "manually to confirm -- this script does not click the final button."
        )
        input("Press Enter here after posting (or closing without posting) to finish...")

        await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--post-id", required=True)
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    asyncio.run(post_reply(args.post_id, args.text))
