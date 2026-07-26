# LinkedIn API — setup for posting to your own profile

## Steps

1. Go to developer.linkedin.com and create an app.
2. Registration requires linking the app to a **company page** -- even if
   you're only going to post to your personal profile. If you don't have
   one, create a placeholder page just to satisfy the registration
   requirement.
3. Verify the app (LinkedIn's own security step).
4. Under "Products", add:
   - **Sign In with LinkedIn using OpenID Connect** (auth flow)
   - **Share on LinkedIn** (this unlocks the `w_member_social` scope)
5. Note down the app's **Client ID** and **Client Secret**.
6. Run `scripts/linkedin_oauth_setup.py` once -- it opens the browser for
   the 3-legged OAuth flow, you authorize, and the script saves the access
   token and refresh token locally.

## Tokens

- Access token expires in **60 days**.
- Refresh token lasts **365 days** -- the post script uses it to
  automatically renew the access token when needed, so you won't be asked
  to log in again until a year has passed.
- Rate limit: around 100 calls/day per member -- not a real limit for
  normal posting frequency.

## What NOT to do

Don't request the `w_organization_social` scope (posting to a company
page) unless you need it -- that falls under the Marketing Developer
Platform, which requires partner review (weeks). For posting to your
personal profile, stick to `w_member_social`, which is self-serve and
immediate.
