"""
Publishes a post on X via the official API (POST /2/tweets), OAuth 1.0a
user context. No browser, no detection risk -- this is the sanctioned route.

Requires in the environment: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET
(see references/x-api-setup.md)

Usage:
  python x_post.py --text "your post here"
  python x_post.py --thread post1.txt post2.txt post3.txt   # numbered thread
"""
import argparse
import os
import sys

from requests_oauthlib import OAuth1Session

API_URL = "https://api.twitter.com/2/tweets"


def get_session():
    required = ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET"]
    missing = [v for v in required if not os.environ.get(v)]
    if missing:
        raise SystemExit(f"Missing environment variables: {', '.join(missing)}")
    return OAuth1Session(
        os.environ["X_API_KEY"],
        client_secret=os.environ["X_API_SECRET"],
        resource_owner_key=os.environ["X_ACCESS_TOKEN"],
        resource_owner_secret=os.environ["X_ACCESS_SECRET"],
    )


def post_tweet(text: str, reply_to_id: str | None = None) -> str:
    session = get_session()
    payload = {"text": text}
    if reply_to_id:
        payload["reply"] = {"in_reply_to_tweet_id": reply_to_id}
    resp = session.post(API_URL, json=payload)
    if resp.status_code != 201:
        raise RuntimeError(f"Failed to post ({resp.status_code}): {resp.text}")
    tweet_id = resp.json()["data"]["id"]
    print(f"Posted: https://x.com/i/status/{tweet_id}")
    return tweet_id


def post_thread(texts: list[str]):
    prev_id = None
    for text in texts:
        prev_id = post_tweet(text, reply_to_id=prev_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Text for a single post")
    group.add_argument("--thread", nargs="+", help=".txt files, one per thread post, in order")
    args = parser.parse_args()

    if args.text:
        post_tweet(args.text)
    else:
        texts = [open(f).read().strip() for f in args.thread]
        post_thread(texts)
