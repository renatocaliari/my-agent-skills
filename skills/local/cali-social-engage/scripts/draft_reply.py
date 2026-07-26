"""
Generates a reply draft for a specific post from data/ranked.json.
Does NOT post anything -- only prints the draft for human review.

Usage:
  python draft_reply.py --post-id <id> --ranked data/ranked.json
"""
import argparse
import json
from pathlib import Path


def find_post(ranked_path, post_id):
    posts = json.loads(Path(ranked_path).read_text())
    for p in posts:
        if str(p.get("id")) == str(post_id):
            return p
    return None


def main(post_id, ranked_path):
    post = find_post(ranked_path, post_id)
    if not post:
        raise SystemExit(f"Post {post_id} not found in {ranked_path}")

    print("--- Original post ---")
    print(post["text"])
    print(f"\nplatform: {post['platform']} | url: {post.get('url')}")
    print("\n--- Draft ---")
    print(
        "[Write the reply here manually, or ask Claude to draft it based on "
        "the tone configured in config.yaml -- this script only fetches the "
        "post; text generation happens in conversation, not from a fixed template.]"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--post-id", required=True)
    parser.add_argument("--ranked", default="data/ranked.json")
    args = parser.parse_args()
    main(args.post_id, args.ranked)
