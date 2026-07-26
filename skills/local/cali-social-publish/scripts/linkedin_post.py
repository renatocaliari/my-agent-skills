"""
Publishes a post on LinkedIn via the official API (POST /rest/posts), using
the token saved by linkedin_oauth_setup.py. Renews itself with the refresh
token if the access token has expired.

Usage:
  python linkedin_post.py --text "your post here"
"""
import argparse
import json
import os
import time
from pathlib import Path

import requests

TOKEN_PATH = Path.home() / ".social-publish" / "linkedin-token.json"
API_VERSION = "202506"  # update to the current month in YYYYMM format


def load_token():
    if not TOKEN_PATH.exists():
        raise SystemExit("Token not found. Run linkedin_oauth_setup.py first.")
    return json.loads(TOKEN_PATH.read_text())


def refresh_token(token_data):
    client_id = os.environ.get("LINKEDIN_CLIENT_ID")
    client_secret = os.environ.get("LINKEDIN_CLIENT_SECRET")
    resp = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "refresh_token",
            "refresh_token": token_data["refresh_token"],
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    resp.raise_for_status()
    new_token = resp.json()
    new_token["obtained_at"] = time.time()
    TOKEN_PATH.write_text(json.dumps(new_token, indent=2))
    return new_token


def get_valid_token():
    token_data = load_token()
    obtained_at = token_data.get("obtained_at", 0)
    expires_in = token_data.get("expires_in", 0)
    if time.time() > obtained_at + expires_in - 300:  # 5 min margin
        token_data = refresh_token(token_data)
    return token_data["access_token"]


def get_member_urn(access_token):
    resp = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    resp.raise_for_status()
    return f"urn:li:person:{resp.json()['sub']}"


def post_text(text: str):
    access_token = get_valid_token()
    author_urn = get_member_urn(access_token)

    resp = requests.post(
        "https://api.linkedin.com/rest/posts",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "LinkedIn-Version": API_VERSION,
            "X-Restli-Protocol-Version": "2.0.0",
        },
        json={
            "author": author_urn,
            "commentary": text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        },
    )
    if resp.status_code != 201:
        raise RuntimeError(f"Failed to post ({resp.status_code}): {resp.text}")
    post_id = resp.headers.get("x-restli-id", "")
    print(f"Posted on LinkedIn: {post_id}")
    return post_id


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    post_text(args.text)
