# AGENTS.md

## Universal Instructions

**⚡ Session Tree & Fork Awareness:** Pi stores sessions as trees. Use `/tree` to navigate branches, `/fork` to create new sessions, `/clone` to duplicate. These are interactive TUI commands — you cannot execute them yourself. For CLI branching: `pi --fork <session-file>`.

---

## Cymbal

Prefer cymbal over Read/Grep/Glob/Bash for code navigation (symbol search, refs, impact, trace, etc.). `pi-cymbal` provides native `cymbal_*` tools and auto-runs the session `remind` + pre-tool `nudge` — no manual invocation needed. Falls back to fff tools (fffind/ffgrep) for pure file or content search only — never raw `find`/`grep` from system.

See **`cali-code-navigation`** skill for full workflow.

## Code Navigation

Tool priority rules, Cymbal workflow, batch guidance for token efficiency, semantic diff commands — see **`cali-code-navigation`** skill.

> **Prefer `sem diff` over `git diff`** for entity-level change detection (functions, types, methods). `git diff` shows raw lines; `sem diff` shows meaningful symbols. If `sem` is unavailable, fall back to `git diff` — never block on its absence.

> **Active loading:** `cali-code-navigation` is referenced here but NOT auto-loaded. Load it explicitly when navigating code: use the `skill` tool with `name: cali-code-navigation`.

### Cymbal Commands Quick Reference

| Goal | Command |
|------|---------|
| Adaptive exploration | `cymbal investigate <symbol>` |
| Find symbol | `cymbal search <name>` |
| Read source | `cymbal show <symbol>` |
| File outline | `cymbal outline <file>` |
| References | `cymbal refs <symbol>` |
| Upstream impact | `cymbal impact <symbol>` |
| Downstream trace | `cymbal trace <symbol>` |
| Implementations | `cymbal impls <iface>` |
| Diff-to-impact | `cymbal changed` (unstaged) / `--staged` |
| Repo map | `cymbal structure` |
| Import fan-in | `cymbal importers <pkg>` |
| Graph topology (add `--graph` to trace/impact/impls/importers) |

---

## ast-grep (Structural Code Search)

`ast-grep` (`sg`) is a structural (AST-based) search/lint/rewrite tool, provided by the `joelhooks/pi-ast-grep` extension (bundles `sg`; also on Homebrew). **Different modality from fff and cymbal:**

| Tool | Layer | Answers |
|------|-------|---------|
| `fff` (pi-fff) | **Lexical** | "Where does this **text** appear?" — fuzzy file find, SIMD grep, frecency |
| `ast-grep` | **Structural** | "Where does this **code pattern** appear?" — AST pattern match, language-aware |
| `cymbal` | **Graph/Semantic** | "Who calls this **symbol**?" — references, impact, call graph |

**No overlap or conflict.** Use priority:
1. **Text/filename** → `fffind` / `ffgrep` (fff)
2. **Code shape/pattern** → `ast-grep` (structural)
3. **Symbol refs/impact** → `cymbal` (graph)

### When to use ast-grep

Use **ast-grep over fff/grep** when you need structural awareness:
- "Find all unchecked `err` returns" → `sg -p 'f(), err := $F()'` (finds ignored errors WITHOUT `_ =`)
- "Find all `context.Background()` in HTTP handlers" → `sg -p 'context.Background()'`
- "Find all `sync.Mutex` copies" → `sg -p 'func $F($$$) { $$$ }'` + filter types
- Pattern rewrite: `sg -p '$A && $A()' -r '$A?.()'` (replace with optional chaining)

Use **fff/grep over ast-grep** when:
- You need a filename or path
- The pattern is trivial text (a string literal, a config key)
- You need frecency ranking (most-accessed files first)

### Basic usage

```bash
ast-grep -p 'fmt.Sprintf("$MSG", $ARGS)'   # structural search
ast-grep -p 'func $NAME($$$) error'          # find all error-returning funcs
ast-grep -l go -p 'defer $FILE.Close()'      # find all deferred Close() calls
ast-grep --stdin                              # batch queries via stdin
```

### Refactoring (rewrite with AST safety)

Use `-r` (rewrite) for cross-file refactoring. Prefer over grep+sed — ast-grep
preserves AST structure and never matches inside strings, comments, or tokens
that happen to look like code:

```bash
# Add ctx param to all error-returning funcs that lack it
ast-grep -p 'func ($R *$T) $F($$$) error' \
  -r 'func ($R *$T) $F(ctx context.Context, $$$) error' \
  --rewrite

# Rename method across all files
ast-grep -p 'func ($R *$T) oldName($$$) $RES' \
  -r 'func ($R *$T) newName($$$) $RES' \
  --rewrite

# Replace pattern structurally (not textually)
ast-grep -p '$A && $A()' -r '$A?.()' --rewrite
```

**Regra:** refatoração cross-file que mexe em assinatura/estrutura → ast-grep.
Alteração localizada (1-2 arquivos, corpo de função) → edit/write normal.

### Linting with ast-grep

`ast-grep` can also run rule files (`sg scan`) for project-specific lint rules.
Not a replacement for `golangci-lint` — use for custom structural rules the Go
type system cannot express. See `ast-grep new` for scaffolding.

---

---

## Browser Automation (e2e, text-only LLM)

Use installed `pi-playwright-extension` (`browser_*` tools, **headless**). For e2e / visual tests with an LLM that **cannot read images**.

| Step | Tool | Why |
|------|------|-----|
| Navigate | `browser_navigate` | headless by default |
| Inspect / assert | `browser_snapshot` | **ARIA snapshot + refs + visible text = your "visual" signal** (LLM-readable) |
| Act | `browser_type` / `browser_click` / `browser_press_key` | use returned refs |
| Wait | `browser_wait_for` | stable refs invalidate on page change |
| Verify | `browser_evaluate` (JSON/text), `browser_console`, `browser_network` | all text-readable |

**LLM cannot read images:** do NOT rely on `browser_screenshot` / `browser_video_*` / `browser_run_summary` for assertions — they emit PNG/MP4 the LLM can't parse. Screenshots only as optional **human-facing** artifacts (save the file; never ask the LLM to read it).

The ARIA snapshot is the assertion surface: it carries text, roles, and stable refs — more reliable than pixels even for vision-capable models. Headless default → CI-friendly, no display. Token-light vs chrome-dev-tools (compact ARIA vs full AX tree).

## Skills Reference

| When | Skill |
|------|-------|
| Code navigation (cymbal), file search (fff), structural search (ast-grep), entity diff (sem) | `cali-code-navigation` |
| Cross-cutting debug (framework JS API, binary freshness) | `cali-cross-cutting-debug` |
| New Feature or Product | `/skill:stelow-product-orchestrator` |
| Coding standards (universal: KISS, DRY, LoB, SoC, Fail Fast, YAGNI) | `/skill:cali-product-coding-standards` |
| Go standards (idiomatic Go, concurrency, linting) | `/skill:cali-coding-go-standards` |
| Go stack (Datastar, Templ, NATS, Air) | `/skill:cali-coding-go-stack` |
| Package audit (socket.dev, Trivy, OSV-Scanner, dotenvx) | `/skill:cali-ops-package-audit` |
| Releases | `/skill:cali-ops-github-releases` |
| Testing execution (unit → subagent → UI → browser) | `/skill:cali-product-testing-execution` |
| Deploy | `/skill:cali-ops-deploy-github-tailscale` |
| Security | `/skill:cali-ops-server-security` |
| AGENTS.md create/update/validate | `/skill:cali-agents-md-generator` |
| AGENTS.md validate | `/skill:cali-agents-md-validator` |
| Post-execution critique | `/skill:cali-product-execution-critique` |
| Parallel work | `/skill:pi-subagents` |

### Skill Prefix Convention
- `cali-coding-*` — práticas/padrões de escrita de código (standards, go-stack, starhtml)
- `cali-code-*` — ferramentas de análise de código existente (navigation)
- `cali-cross-cutting-*` — regras transversais (debug)
- `stelow-*` — skills de planejamento de produto (fonte: `stelow-product-orchestrator`)
- `cali-ops-*` — operações (deploy, security, package-audit)

### Project-Level AGENTS.md

Every project **must** have a lean `AGENTS.md` (20-30 lines max, no placeholders). See `cali-agents-md-generator` for create/update/validate workflow, pre-commit hook setup, and CI guard.

Update AGENTS.md when:
- Entry point / cmd moved (e.g. `cmd/web/` → `cmd/server/`)
- New top-level package or `features/` module added/removed/renamed
- Build/test/lint command changed
- Framework swap (e.g. Templ → html/template, Datastar → HTMX, NATS → in-process)
- Database / schema migration system changed
- New convention enforced (e.g. `errors.New` → `fmt.Errorf`)

**Human must approve all AGENTS.md changes** — never auto-update.

Cosmetic changes (CSS, copy, refactors inside functions, dependency bumps, test cases) do NOT require an update.

---

## Conventions

### Language
All code, URLs, routes, handler IDs: **English**. Exception: user-facing UI text, LLM prompts, database content.

### File Naming
All project files: `lowercase-kebab-case`.

### Estimation Bias Correction
LLMs are trained on human data that **systematically overestimates implementation time** (Hofstadter's Law). This creates a bias toward choosing "simpler" but worse solutions to avoid perceived complexity.

**Rule:** Never let estimated implementation cost outweigh solution quality. A correct, maintainable, well-structured solution that takes longer is preferable to a quick hack. Push back against your own instinct to choose "cheap" approaches. Quality first — if a pattern is architecturally correct (SSE over polling, proper schema over flat storage, real auth over stub), implement it properly regardless of estimated effort.

### Post-Execution Verification
After ANY multi-step task: trigger **`/skill:cali-product-execution-critique`** — verifies plan compliance, edge cases, NFRs, and needed doc/test updates.

### Releases & Changelog
Tag + GitHub Release go together — never tag-only. `CHANGELOG.md` (Keep a Changelog format) is the canonical source for release notes; generate `gh release` notes FROM the changelog, not in parallel. Use [`/skill:cali-ops-github-releases`](/skill:cali-ops-github-releases) for the full workflow.

---

## Don'ts

- Never add dependencies without asking
- Never put secrets in AGENTS.md
- Never modify vendor/ without asking
- Never use Axios — use native `fetch`

---

## Secrets Management — server.calionauta.com convention

When working with the `server.calionauta.com` server (Tailscale `100.120.175.47`, user `deploy`), follow the **3-layer model** defined in skill `cali-ops-server-security`:

| Layer | Storage | Read by |
|--------|---------|---------|
| **L1 — runtime** | env vars in container | container only |
| **L2 — rest** | `~/.secrets/<service>.env` chmod 600 | owner `deploy` |
| **L3 — provider** | Cloudflare / Minimax / Telegram dashboard | rotated, IP-scoped |

### Where secrets live

- **Server side**: `/home/deploy/.secrets/` (chmod 700) containing `<service>.env` files (chmod 600).
- **Mac side**: `~/.ssh/config` has SSH alias `Host server.calionauta.com → 100.120.175.47`. Use `deploy@server.calionauta.com` (NOT `renatocaliari.com`).
- **agentmemory**: long-term facts include non-sensitive layout (paths, container names, scripts). NEVER store actual secrets.

### How to use them

For tasks on the server, use `~/bin/` scripts that already follow this convention:

- `~/bin/cloudflare-dns.sh list|add|delete|get`
- `~/bin/update-tunnel.sh [config-file]`
- `~/bin/setup-cf-token.sh` (initial setup)

Each script does `set -a; source ~/.secrets/<service>.env; set +a` then makes the API call. Don't write new scripts that hardcode tokens.

### When Claude (me) needs a token

The user pastes it **once** into `~/.secrets/<service>.env` via `setup-cf-token.sh` (token sent via stdin, not argv). The script stores it chmod 600 in `~/.secrets/`. Claude reads via scripts that `source` the file. Claude does NOT request tokens via chat or write them into scripts.

### Boundaries

- `~/.secrets/` does NOT protect against a compromised agent that already has shell access. For agent containment (network-layer policy), consider OneCLI / Vault when scope grows (3+ servers OR 50+ secrets OR compliance audit needed).
- Nango is for SaaS OAuth flows (user-as-tenant), not system-to-system agent calls.
- For git-tracked secrets, use Age + SOPS. For local at-rest, `~/.secrets/` + chmod 600 is enough (with disk encryption assumed).
- Files at `/etc/cloudflared/`, `/opt/ingress/`, `/etc/caddy/` are root-only — Claude cannot edit directly. Surface the exact edit needed for the user to apply manually.

### SSH tunnel for web UIs

For services that bind to `127.0.0.1` on the server (like Mercury web dashboard on `:6174`), use:

```
ssh -L <PORT>:127.0.0.1:<PORT> deploy@server.calionauta.com
```

Then access `http://localhost:<PORT>` from the Mac. Foreground mode matters — `network_mode: host` is required for services binding `127.0.0.1` inside Docker containers.

---

## No AI attribution in user-facing artifacts

Claude (or any AI assistant) does NOT co-author anything. The user
writes every commit, release note, pull request description, blog
post, and public message. Some projects' tools and community
conventions append `Co-Authored-By: <model> <noreply@anthropic.com>`
to commit messages and release bodies — that's an artifact of the
assistant that helped draft the content, not a real co-author.

**Rules:**

- **Never** add `Co-Authored-By: Claude ...` or any AI model trailer
  to a commit message, PR description, release notes, blog post, or
  CHANGELOG entry. Adding the trailer falsely attributes authorship to
  the model, and the model did no end-to-end work the user did not
  direct and approve.
- **Never** add an explicit "Co-Authored-By: <user>" trailer to a
  release note for the same reason — they are meta-commentary, not
  part of the artifact.
- When asked to draft commit messages, release bodies, or any other
  public text, end the file at the last meaningful sentence. Do not
  append attribution lines.
- If a tooling pipeline (e.g. `gh release create`, an editor
  plugin, a git hook) auto-appends AI attribution by default,
  disable that behavior for the project. The Project AGENTS.md should
  spell out the rule for any future session that touches the repo.

**Why this matters:** the trailer spreads AI crediting into commit
history and release pages where every reader sees it. It implies the
user shared authorship with a tool that has no standing to claim it.
For personal repos where Claude briefly helped, the trailer is
mildly absurd; for any organization where multiple contributors
share the history, it's actively misleading.
