"""
Run once to log into X manually and save the storageState.
After this, x_capture.py reuses the session without asking for login again.

Usage: python x_login_once.py
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

STATE_DIR = Path.home() / ".social-listening"
STATE_PATH = STATE_DIR / "x-state.json"


async def main():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://x.com/login")
        print("Log in manually in the window that opened.")
        print("Once your timeline has loaded, come back here and press Enter.")
        input()
        await context.storage_state(path=str(STATE_PATH))
        print(f"Session saved to {STATE_PATH}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
