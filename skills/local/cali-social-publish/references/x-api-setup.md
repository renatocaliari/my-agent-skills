# X API — setup for posting (not reading)

This is only for creating posts on your own feed. You don't need the
expensive read/search tiers -- just write access, which is cheap.

## Steps

1. Go to developer.x.com and create a project + app (the free developer
   tier works, what changes is billing per write call).
2. In the app settings, enable "OAuth 1.0a" with **Read and Write**
   permission.
3. Generate:
   - API Key + API Key Secret (for the app)
   - Access Token + Access Token Secret (for your own user account --
     "Access Token and Secret" under the Keys and Tokens tab)
4. Export as environment variables (never hardcode these in any script):
   ```bash
   export X_API_KEY="..."
   export X_API_SECRET="..."
   export X_ACCESS_TOKEN="..."
   export X_ACCESS_SECRET="..."
   ```
5. Set up pay-per-use billing in the developer portal (required even for
   low volume -- there's no longer a fully free write tier, but the cost
   per post is ~$0.015, no monthly minimum).

## Expected cost

Posting ~1x/day (30 posts/month), the cost lands around $0.45/month --
within "essentially no spend" territory.
