# agent-sync-public

Public, credential-free skills installable via [npx skills](https://github.com/vercel-labs/agent-skills):

```bash
npx skills add calionauta/agent-sync-public -s "substack-publish writing-style" -g --yes
```

## Layout & authoritative sources

All skills live under `skills/local/<name>/` — the path published by the
`agent-sync` CLI for skills sourced from the local hub (`source_id: local`).

| Family | Authoritative source | Update channel |
|---|---|---|
| `substack-publish`, `writing-style`, `publishing-skill` | this repo (hand-curated) | direct commits |
| `cali-*` (coding/ops/social/questions/skill-validator) | this repo ↔ Mac hub via agent-sync backup | weekly `npx skills update -g` |
| `stelow-*`, `stelow-entry`, `stelow-router` | **not here** — [`calionauta/stelow`](https://github.com/calionauta/stelow) | `npx skills update -g` |
| `cali-degustia-*` | **not here** — [`calionauta/degustia`](https://github.com/calionauta/degustia) (private) | `npx skills update -g` |
| `last30days`, `pocketbase`, `landing-page-evaluator` | upstream third-party repos | `npx skills update -g` |

**No credentials ever.** Skills that need runtime values read them from
`~/.secrets/<tool>.env` on each host and print a guided setup when missing
(see `skills/local/substack-publish/SKILL.md` → "Configuration guard").

## Re-publishing (keep this repo in sync with the Mac hub)

Published copies can go stale vs the authoritative hub. After editing any
skill locally:

```bash
agent-sync share run        # re-publish selected skills → skills/local/
git -C . pull --rebase && git push   # if publishing from another clone
```

Planned: weekly automated `share run` alongside the Sunday
`npx skills update -g` cycle.
