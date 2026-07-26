"""
Captures tweets from the timeline or a search on X, intercepting GraphQL
responses instead of parsing HTML. Reuses the session saved by
x_login_once.py -- never asks for login again.

Usage:
  python x_capture.py --source home --rounds 10
  python x_capture.py --source search --query "agentic coding" --rounds 10
"""
import argparse
import asyncio
import json
import random
import time
from pathlib import Path
from playwright.async_api import async_playwright

STATE_PATH = Path.home() / ".social-listening" / "x-state.json"
OUT_DIR = Path("data/raw")

GRAPHQL_MARKERS = [
    "HomeTimeline",
    "HomeLatestTimeline",
    "SearchTimeline",
    "UserTweets",
    "TweetDetail",
]


async def capture(source: str, query: str | None, rounds: int):
    if not STATE_PATH.exists():
        raise SystemExit(
            f"Session not found at {STATE_PATH}. Run x_login_once.py first."
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    captured = []

    async def on_response(response):
        if any(marker in response.url for marker in GRAPHQL_MARKERS):
            try:
                data = await response.json()
                captured.append({"url": response.url, "data": data})
            except Exception:
                pass  # empty or non-JSON response, ignore

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=str(STATE_PATH))
        page = await context.new_page()
        page.on("response", on_response)

        if source == "home":
            await page.goto("https://x.com/home")
        elif source == "search":
            if not query:
                raise SystemExit("--query is required with --source search")
            await page.goto(
                f"https://x.com/search?q={query.replace(' ', '%20')}&f=live"
            )
        else:
            raise SystemExit("--source must be 'home' or 'search'")

        await page.wait_for_timeout(3000)  # let the first batch load

        for i in range(rounds):
            await page.mouse.wheel(0, random.randint(1200, 2200))
            # randomized delay -- regular cadence is the most obvious bot signal
            await page.wait_for_timeout(random.randint(1500, 4000))
            print(f"round {i + 1}/{rounds} — {len(captured)} responses captured so far")

        await browser.close()

    ts = int(time.time())
    out_path = OUT_DIR / f"x_{source}_{ts}.json"
    out_path.write_text(json.dumps(captured, ensure_ascii=False, indent=2))
    print(f"Saved: {out_path} ({len(captured)} responses)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["home", "search"], default="home")
    parser.add_argument("--query", default=None)
    parser.add_argument("--rounds", type=int, default=10)
    args = parser.parse_args()
    asyncio.run(capture(args.source, args.query, args.rounds))
