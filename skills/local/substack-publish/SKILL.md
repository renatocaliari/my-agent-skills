---
name: substack-publish
description: >
  Publish drafts and posts to the owner's Substack publication
  (${SUBSTACK_PUBLICATION_URL} — handle ${OWNER_HANDLE}, user_id ${SUBSTACK_USER_ID}).
  All operations go through the agent's MCP client as `substack-<tool>`
  (aggregated by the Bifrost /mcp gateway on the server — one endpoint, no
  CLI wrapper). The 27 substack-* tools include create_draft_post,
  update_draft, set_post_body, publish_draft, list_posts, get_draft,
  get_publication_stats, list_publication_tags, upload_image, and more.
  Only report what a tool returns; never fabricate draft ids, slugs, or
  publish results. NEVER publish without explicit user confirmation.
version: 4.0.0
category: publishing
categories:
  - publishing
  - writing
  - substack
intents:
  - criar draft no substack
  - criar rascunho no substack
  - escrever um post
  - escrever uma postagem
  - escrever texto para publicar
  - rascunho de post
  - editar post substack
  - editar draft substack
  - listar drafts substack
  - listar posts substack
  - ler draft substack
  - publicar no substack
  - substack
tags:
  - substack
  - publishing
  - draft
  - post
  - newsletter
allowed-tools:
  - exec
  - bash
---

# Substack Publish

## Configuration guard (run BEFORE any tool call)

This skill requires `~/.secrets/substack.env` on the host. Before the first
tool call of a session, verify:

```bash
test -f ~/.secrets/substack.env \
  && grep -q 'SUBSTACK_PUBLICATION_URL=' ~/.secrets/substack.env \
  && grep -q 'SUBSTACK_SESSION_TOKEN=' ~/.secrets/substack.env \
  && grep -q 'SUBSTACK_USER_ID=' ~/.secrets/substack.env && echo OK
```

**If it prints OK**, continue normally.

**If not, do NOT guess and do NOT call any tool.** Stop and walk the user
through setup, printing exactly this:

1. Create the secrets file:
   ```bash
   mkdir -p ~/.secrets && chmod 700 ~/.secrets
   cat > ~/.secrets/substack.env << 'ENV'
   SUBSTACK_PUBLICATION_URL=https://yourpub.substack.com
   SUBSTACK_SESSION_TOKEN=<paste browser session cookie>
   SUBSTACK_USER_ID=<numeric id>
   OWNER_HANDLE=@yourhandle
   ENV
   chmod 600 ~/.secrets/substack.env
   ```
2. Where each value comes from:
   - `SUBSTACK_PUBLICATION_URL` — your publication address (browser URL).
   - `SUBSTACK_SESSION_TOKEN` — logged-in browser → DevTools → Application →
     Cookies → your publication domain → session token value.
   - `SUBSTACK_USER_ID` — account settings/API, or `get_publication_stats`
     once the toolset connects.
   - `OWNER_HANDLE` — your @handle.
3. Reconnect/re-register the `substack` MCP client so it picks up the envs.
4. Verify with a harmless call (`get_publication_stats`). Only proceed when
   it returns data.

Never fabricate values to make the check pass; never echo cookie contents.

Publish drafts and posts to the owner's Substack publication via the
`substack-*` MCP tools (aggregated by Bifrost `/mcp`; no CLI wrapper).

## Publication identity

- Publication: `${SUBSTACK_PUBLICATION_URL}`
- Handle: `${OWNER_HANDLE}` · User id: `${SUBSTACK_USER_ID}`
- Tools are named `substack-<tool>` (e.g. `substack-create_draft_post`,
  `substack-update_draft`, `substack-publish_draft`). List them with
  `tools/list`; their input schemas are authoritative — do not re-describe
  them here.

## Voice & style

Draft content follows the companion **`writing-style`** skill (same repo) —
lowercase-only, staccato, no marketing. Apply it before creating/updating
the draft body unless the user explicitly overrides.

## CRITICAL: drafts go HERE, never in the vault

When the user asks to write/draft/structure a text that will be PUBLISHED,
create the draft with this skill (`create_draft_post`). Do NOT write it into
notes/raw/ — the vault is for personal notes, not publication drafts.

## Workflows

### 1. Create a draft
`substack-create_draft_post` with `title`, `subtitle` (required — may be
empty string), and `body` (plain text OR ProseMirror JSON, see "Editor
format limits" below). Returns `{draft_id, is_published}` — save and report
the `draft_id`.

### 2. Read / list
`substack-list_posts` (status drafts/published), `substack-get_draft` /
`substack-get_reader_post` to read a body. `get_draft` returns the body as
ProseMirror JSON; convert to plain text/markdown when showing the user.

### 3. Edit a draft
`substack-update_draft` (or `substack-set_post_body`) to edit an existing
draft in place. No need to create+delete anymore.

### 4. Publish
`substack-publish_draft` exists, but publishing is **irreversible** — never
call it without explicit user confirmation. If the user wants a final
human pass first, point them to the dashboard.

### 5. Promote / engage
`substack-get_publication_stats`, `substack-get_analytics`,
`substack-list_publication_tags`, `substack-add_tag_to_post`,
`substack-get_post_comments`, `substack-comment_on_post`,
`substack-restack_item`, `substack-upload_image`.

## Editor format limits (ProseMirror schema)

The Substack editor uses a fixed ProseMirror schema. Plan the format before
drafting.

- **markdown tables do not render.** Ladder: (1) Datawrapper embed (readers
  need to compare cells); (2) restructure as bullets (simple linear lists);
  (3) render to PNG + embed (last resort).
- **mermaid / live diagrams do not render.** Export PNG from mermaid.live and
  embed as image; keep the live diagram only in the vault/wiki version.
- **images** need absolute URLs (Substack fetches and re-hosts). Relative
  paths and `file://` fail.
- **works:** headings (level 1-3), paragraphs, bullet/ordered lists, links,
  bold/italic/underline/code marks, code blocks (use 2 or 4 spaces, never
  tabs), blockquotes, horizontal rules.
- Smart quotes: Substack auto-converts ASCII `"` `'` on save.

## Rules

- **Never publish without explicit user confirmation.**
- Only report what the tool returns; never fabricate draft ids, slugs, status.
- If a call fails 401/403: the Substack session token likely expired —
  re-extract it from the browser into `~/.secrets/substack.env` (server),
  then the substack MCP client needs a reconnect.
- A `create_draft_post` with an invalid ProseMirror node errors out (schema
  validation); unknown HTML is dropped silently — prefer ProseMirror JSON for
  structured content.

## Checklist before delivering a draft

- [ ] `subtitle` present (even if empty string)?
- [ ] body is plain text OR ProseMirror JSON (never raw HTML)?
- [ ] no markdown tables (or converted via the ladder)?
- [ ] no ` ```mermaid ` without PNG export?
- [ ] all image URLs absolute?
- [ ] code blocks use 2/4 spaces, no tabs?
- [ ] if 401/403: told the user about token re-extraction?
- [ ] **`publish_draft` never called without explicit user confirmation?**