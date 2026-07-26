"""
LinkedIn's 3-legged OAuth flow, run once, to generate an access token +
refresh token with the w_member_social scope. After this, linkedin_post.py
renews it on its own using the refresh token (valid for 365 days).

Requires LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET in the environment
(see references/linkedin-api-setup.md).

Usage:
  python linkedin_oauth_setup.py
  (opens the browser, authorize, paste the returned code when prompted)
"""
import json
import os
import urllib.parse
from pathlib import Path

import requests

TOKEN_DIR = Path.home() / ".social-publish"
TOKEN_PATH = TOKEN_DIR / "linkedin-token.json"
REDIRECT_URI = "http://localhost:8765/callback"  # register this exact value in the LinkedIn app
SCOPES = "openid profile w_member_social"


def main():
    client_id = os.environ.get("LINKEDIN_CLIENT_ID")
    client_secret = os.environ.get("LINKEDIN_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise SystemExit("Set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET in the environment.")

    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization?"
        + urllib.parse.urlencode({
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPES,
        })
    )
    print("Open this link, authorize, and paste the 'code' from the redirect URL here:")
    print(auth_url)
    code = input("code=").strip()

    resp = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": client_id,
            "client_secret": client_secret,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    resp.raise_for_status()
    token_data = resp.json()

    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(json.dumps(token_data, indent=2))
    print(f"Tokens saved to {TOKEN_PATH}")


if __name__ == "__main__":
    main()
