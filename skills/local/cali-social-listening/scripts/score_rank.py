"""
Reads the raw dumps from data/raw/, extracts posts (normalized format,
independent of X or LinkedIn), filters by language, and ranks by:
  - engagement velocity (interactions / minute since publication)
  - reply competition (fewer existing replies = more room)
  - topic relevance (keyword match against config.yaml)

Usage:
  python score_rank.py --input data/raw/ --output data/ranked.json --languages pt,en
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0
except ImportError:
    detect = None

import yaml


def load_config():
    cfg_path = Path("config.yaml")
    if not cfg_path.exists():
        return {"topics": [], "weights": {"velocity": 0.4, "reply_gap": 0.3, "relevance": 0.3}}
    return yaml.safe_load(cfg_path.read_text())


def extract_posts_x(raw_entry):
    """Extracts normalized posts from an X GraphQL response.
    The exact structure varies by endpoint -- adjust the paths below
    if X changes the schema (it has before, it will again)."""
    posts = []
    data = raw_entry.get("data", {})
    # defensive navigation -- if the schema changes, this shouldn't break everything else
    instructions = (
        data.get("data", {})
        .get("home", {})
        .get("home_timeline_urt", {})
        .get("instructions", [])
    )
    for instr in instructions:
        for entry in instr.get("entries", []):
            try:
                tweet = (
                    entry["content"]["itemContent"]["tweet_results"]["result"]
                )
                legacy = tweet.get("legacy", {})
                posts.append({
                    "platform": "x",
                    "id": tweet.get("rest_id"),
                    "text": legacy.get("full_text", ""),
                    "created_at": legacy.get("created_at"),
                    "likes": legacy.get("favorite_count", 0),
                    "reposts": legacy.get("retweet_count", 0),
                    "replies": legacy.get("reply_count", 0),
                    "url": f"https://x.com/i/status/{tweet.get('rest_id')}",
                })
            except (KeyError, TypeError):
                continue
    return posts


def extract_posts_linkedin(raw_entry):
    """Extracts normalized posts from a LinkedIn voyager response.
    Schema is also unstable -- treat as best-effort."""
    posts = []
    data = raw_entry.get("data", {})
    for element in data.get("elements", []):
        try:
            commentary = element.get("commentary", {}).get("text", {}).get("text", "")
            social = element.get("socialDetail", {}).get("totalSocialActivityCounts", {})
            posts.append({
                "platform": "linkedin",
                "id": element.get("entityUrn"),
                "text": commentary,
                "created_at": None,  # LinkedIn doesn't expose an exact timestamp easily
                "likes": social.get("numLikes", 0),
                "reposts": social.get("numShares", 0),
                "replies": social.get("numComments", 0),
                "url": raw_entry.get("url"),
            })
        except (KeyError, TypeError):
            continue
    return posts


def minutes_since(created_at_str, platform):
    if not created_at_str:
        return 60  # conservative fallback if we don't know the post's age
    try:
        if platform == "x":
            dt = datetime.strptime(created_at_str, "%a %b %d %H:%M:%S %z %Y")
        else:
            return 60
        delta = datetime.now(timezone.utc) - dt
        return max(delta.total_seconds() / 60, 1)
    except Exception:
        return 60


def score_post(post, topics, weights):
    engagement = post["likes"] + post["reposts"] + post["replies"]
    age_min = minutes_since(post["created_at"], post["platform"])
    velocity = engagement / age_min

    reply_gap = 1 / (post["replies"] + 1)  # fewer replies -> higher score

    text_lower = post["text"].lower()
    relevance = sum(1 for t in topics if t.lower() in text_lower) / max(len(topics), 1)

    total = (
        weights.get("velocity", 0.4) * velocity
        + weights.get("reply_gap", 0.3) * reply_gap
        + weights.get("relevance", 0.3) * relevance
    )
    return {**post, "score": total, "velocity": velocity, "reply_gap": reply_gap, "relevance": relevance}


def main(input_dir, output_path, languages):
    cfg = load_config()
    topics = cfg.get("topics", [])
    weights = cfg.get("weights", {"velocity": 0.4, "reply_gap": 0.3, "relevance": 0.3})

    all_posts = []
    for f in Path(input_dir).glob("*.json"):
        raw = json.loads(f.read_text())
        for entry in raw:
            if "x_" in f.name or entry["url"].startswith("https://x.com") or "twitter" in entry.get("url", ""):
                all_posts.extend(extract_posts_x(entry))
            else:
                all_posts.extend(extract_posts_linkedin(entry))

    if languages and detect:
        filtered = []
        for p in all_posts:
            try:
                lang = detect(p["text"]) if p["text"] else None
            except Exception:
                lang = None
            if lang in languages or lang is None:
                filtered.append(p)
        all_posts = filtered

    scored = [score_post(p, topics, weights) for p in all_posts if p["text"]]
    scored.sort(key=lambda p: p["score"], reverse=True)

    Path(output_path).write_text(json.dumps(scored, ensure_ascii=False, indent=2))
    print(f"{len(scored)} posts ranked -> {output_path}")
    print("Top 5:")
    for p in scored[:5]:
        print(f"  [{p['platform']}] score={p['score']:.2f} — {p['text'][:80]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/raw")
    parser.add_argument("--output", default="data/ranked.json")
    parser.add_argument("--languages", default="pt,en")
    args = parser.parse_args()
    langs = [l.strip() for l in args.languages.split(",")]
    langs = ["pt-BR" if l == "pt" else l for l in langs] + (["pt"] if "pt" in langs else [])
    main(args.input, args.output, langs)
