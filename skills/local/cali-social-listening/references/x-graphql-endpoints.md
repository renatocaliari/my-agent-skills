# X (Twitter) — GraphQL endpoints to intercept

Intercept via `page.on('response')` during navigation/scroll, filtering by
URL. Extract `await response.json()` when the content-type is JSON.

| Endpoint (URL substring)     | When it appears                    | Contains                          |
|---|---|---|
| `HomeTimeline`               | scrolling the "For You" timeline   | tweets + engagement metrics       |
| `HomeLatestTimeline`         | scrolling the "Following" timeline | same, chronological order         |
| `SearchTimeline`             | searching a term/hashtag           | tweets from search results        |
| `TweetDetail`                | opening a specific tweet           | full thread + replies             |
| `UserTweets`                 | visiting someone's profile         | that user's tweets                |

## Why intercept instead of parsing HTML

X's DOM changes frequently and is obfuscated (generated class names). The
GraphQL payload is the same structure the UI consumes, so it's more stable
across redesigns and already comes as clean JSON — no need to maintain CSS
selectors.

## Basic extraction structure

```python
async def on_response(response):
    if "HomeTimeline" in response.url or "SearchTimeline" in response.url:
        try:
            data = await response.json()
            raw_dumps.append(data)
        except Exception:
            pass  # non-JSON or empty response, ignore

page.on("response", on_response)
```

## Precautions

- Scroll with randomized delay (1.5–4s), never at a fixed interval —
  perfectly regular cadence is the most obvious automation signal.
- Always reuse the same `storageState.json` — recreating the session on
  every run is another strong bot signal.
- Don't stop at the first empty round — GraphQL sometimes takes a moment to
  fire; wait at least 2s after the scroll before the next one.
