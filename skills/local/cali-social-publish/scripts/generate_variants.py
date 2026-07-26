"""
Reads a source (direct text, local .md file, or URL), expands it into
original post(s) for X and/or LinkedIn, and generates N variations with
different angles.

Uses the Anthropic API directly (doesn't depend on a chat session -- this
way it also works in unattended auto/cron mode).

Usage:
  python generate_variants.py --source text --input "loose idea" \
    --platform both --n-variants 3 --mode review

  python generate_variants.py --source file --input ./notes.md \
    --platform x --n-variants 3 --mode review

  python generate_variants.py --source url --input https://example.com/article \
    --platform linkedin --n-variants 3 --mode auto

Requires ANTHROPIC_API_KEY in the environment.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
import yaml

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
OUT_DIR = Path("data")

PLATFORM_RULES = {
    "x": (
        "X/Twitter format: max 280 characters per post (or a short thread "
        "of 2-4 numbered posts if the content needs more room). "
        "Direct, no fluff, line breaks are fine for rhythm."
    ),
    "linkedin": (
        "LinkedIn format: 3-6 short paragraphs, with a strong hook in the "
        "first line (it appears alone before 'see more'), frequent line "
        "breaks, no more than 2-3 hashtags at the end."
    ),
}


def load_config():
    cfg_path = Path("config.yaml")
    if not cfg_path.exists():
        return {"tone": "direct, no marketing jargon, real experience"}
    return yaml.safe_load(cfg_path.read_text())


def get_source_material(source_type, source_input):
    if source_type == "text":
        return source_input
    if source_type == "file":
        path = Path(source_input)
        if not path.exists():
            raise SystemExit(f"File not found: {path}")
        return path.read_text()
    if source_type == "url":
        resp = requests.get(source_input, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        # simple extraction -- for cleaner content, swap for trafilatura/readability
        return resp.text[:8000]
    raise SystemExit(f"Invalid --source: {source_type}")


def build_prompt(material, source_type, platforms, n_variants, tone):
    copyright_note = (
        "The reference below is ONLY for inspiration -- never copy phrases "
        "or excerpts from it verbatim. Rewrite the core idea entirely in "
        "your own words.\n\n"
        if source_type == "url"
        else ""
    )
    platform_block = "\n".join(
        f"- {p.upper()}: {PLATFORM_RULES[p]}" for p in platforms
    )
    return f"""You're helping expand a reference into original social media
posts, in this tone: {tone}.

{copyright_note}Reference:
---
{material}
---

Generate {n_variants} DISTINCT variations (different angles, not paraphrases
of each other) for each of these platforms:
{platform_block}

Mark exactly ONE variation per platform as "recommended": true -- the one
you think is strongest (most real experience, least generic).

Respond ONLY with valid JSON, in this format, no markdown, no text before or after:
{{
  "x": [
    {{"text": "...", "recommended": false}},
    {{"text": "...", "recommended": true}}
  ],
  "linkedin": [
    {{"text": "...", "recommended": true}}
  ]
}}

Only include the requested platforms: {", ".join(platforms)}.
"""


def call_claude(prompt):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("ANTHROPIC_API_KEY is not set in the environment.")
    resp = requests.post(
        ANTHROPIC_API_URL,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    text_blocks = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
    raw_text = "\n".join(text_blocks).strip()
    raw_text = raw_text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw_text)


def main(args):
    cfg = load_config()
    tone = cfg.get("tone", "direct, no marketing jargon")
    platforms = ["x", "linkedin"] if args.platform == "both" else [args.platform]

    material = get_source_material(args.source, args.input)
    prompt = build_prompt(material, args.source, platforms, args.n_variants, tone)
    variants = call_claude(prompt)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    out_path = OUT_DIR / f"variants_{ts}.json"
    out_path.write_text(json.dumps(variants, ensure_ascii=False, indent=2))
    print(f"Variations saved to {out_path}\n")

    for platform, opts in variants.items():
        print(f"=== {platform.upper()} ===")
        for i, opt in enumerate(opts):
            tag = " [RECOMMENDED]" if opt.get("recommended") else ""
            print(f"[{i}]{tag} {opt['text']}\n")

    if args.mode == "auto":
        print("Auto mode: publishing the recommended variation for each platform...")
        for platform, opts in variants.items():
            chosen = next((o for o in opts if o.get("recommended")), opts[0])
            script = "x_post.py" if platform == "x" else "linkedin_post.py"
            print(f"-> {platform}: calling scripts/{script} (implement the actual "
                  f"call via subprocess or a direct import of the post() function)")
            # Example of direct integration, avoiding subprocess:
            # from x_post import post_tweet
            # post_tweet(chosen["text"])
    else:
        print("Review mode: nothing was published. Pick a variation and run "
              "x_post.py / linkedin_post.py manually with the final text, "
              "or ask Claude to do it in the conversation.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["text", "file", "url"], required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--platform", choices=["x", "linkedin", "both"], default="both")
    parser.add_argument("--n-variants", type=int, default=3)
    parser.add_argument("--mode", choices=["auto", "review"], default="review")
    main(parser.parse_args())
