---
name: cali-coding-go-stack
description: >
  [Cali] Go web stack: Datastar, Templ, DaisyUI, NATS, PocketBase/SQLite,
  GoAI LLM, Zenflow agents. Scaffold, real-time, hypermedia, auth, DB,
  embeddings, voice AI, AI agents, durable workflows, queues. Queues use
  NATS JetStream or goqite. Workflows use go-workflows, turbine, ebind,
  dagnats, or Hatchet per decision tree below.
---

### Datastar Go SDK v2 Watch

Monitor: Issue #8 (GET/POST SSE action options) and PR #18 (PatchElement* refactor) pending. Alert user if merged. Today: v1.2.2 stable.

# Go Stack Web Application

Go boilerplate inspired by [Northstar](https://github.com/delaneyj/toolbelt).

### Engineering Standards

Stack patterns only. Concurrency/linting/security in `cali-coding-go-standards`.
- Local dev (Air, `.air.toml`, Makefile) also defined in `cali-coding-go-standards`.

> ⚠️ **PocketBase hook wiring pitfall**: `app.OnServe().BindFunc(...)` from inside another `OnServe` handler is a SILENT no-op. PocketBase's `Hook.Trigger` snapshots handlers before running them — nested BindFuncs never fire. Always register routes DIRECTLY on `se.Router` inside the existing top-level hook, or as a top-level `app.OnServe().BindFunc` registered before `pb.Start()`. Symptom: route returns 303 to /login indefinitely even though `curl` shows the bind ran.

> ⚠️ **`http.ServeMux` Go 1.22+ subtree matching**: registering `GET /` for an index handler matches every `GET /<anything-not-explicit>` until you add a more specific pattern. Order of registration doesn't matter (specificity wins).
> ⚠️ **Datastar v1.0.2 Required** — uses Datastar v1.0.2 (not RC.8).
- **[Datastar](https://data-star.dev)** — Reactive hypermedia via SSE
- **[Templ](https://templ.guide)** — Go components → HTML
- **[DaisyUI + TailwindCSS](https://daisyui.com)** — UI components
- **[NATS](https://nats.io)** — Real-time messaging (JetStream for persistence)
- **[PocketBase](https://pocketbase.io)** — Database, auth, REST API, realtime, file storage (default)
  - **[sqlc](https://github.com/sqlc-dev/sqlc)** — Typed Go from SQL (escape hatch when PB too narrow)
  - **SQLite driver**: `ncruces/go-sqlite3` (pure Go, wasm2go, no CGO). Recommended over modernc for extension support (FTS5, spellfix1, unicode).
  - **Extensions**: ext/unicode (unaccent, pt_BR collation), ext/fts5, ext/spellfix1. ⚠️ ext/vec1 NOT supported.
- **[Fabric.js](http://fabricjs.com)** — Collaborative whiteboard (optional)
- **[LiveKit + Gemini](https://livekit.io)** — Voice AI (optional)
- **[GoAI](https://github.com/zendev-sh/goai)** — LLM SDK (tools, structured output, streaming, MCP) (optional)
- **[Zenflow](https://github.com/zendev-sh/zenflow)** — Declarative multi-agent harness, YAML workflows, LLM coordinator (optional)

### Queue / Workflow Toolbox

| Tool | When | Key trait |
|------|------|-----------|
| **[goqite ★](https://github.com/maragudk/goqite)** | **Default task queue** — fire-and-forget, streaming (LLM SSE), short-lived jobs | SQLite queue, low-level control (Receive/Extend/Delete), permits streaming via SSE Hub |
| **[turbine ★](https://github.com/YakirOren/turbine)** | **Default workflow engine** — durable multi-step, resume after crash, embeds in PocketBase SQLite | Step replay safe against LLM rewrites, `WithName()` decoupling |
| **[ebind](https://github.com/F1bonacc1/ebind)** v0.4 | Multi-worker, NATS-native task queue + DAG, same binary | Function-first (`Register`, `Await[T]`), requires NATS |
| **[dagnats](https://github.com/danmestas/dagnats)** (experimental) | Multi-worker NATS-native DAG engine, needs console/triggers | JSON workflows, cron/webhook triggers, UI, sidecar |
| **[go-workflows](https://github.com/cschleiden/go-workflows)** v1.4.2 | Full Temporal-like engine, needs signals/child-wf/tester | Mature (500★, 4.5y), SQLite/PG/Redis backend, diagnostics UI |
| **[Hatchet](https://github.com/hatchet-dev/hatchet)** | Multi-service, Postgres dashboard, advanced monitoring | External service, Postgres, DAG visualizer |
| **[Rivet](https://github.com/rivet-dev/rivet)** | Self-hosted Durable Execution platform, Temporal-compatible | External infra (Docker/Postgres), browser IDE |

(★) = recommended default for new blueprints. See [Canonical Pattern](#canonical-pattern) below.

---

## Canonical Pattern

```
┌──────────────────────┬─────────────────────┬──────────────────────────┐
│ Layer                │ Solves              │ Example                  │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Task queue (goqite)  │ Fire-and-forget,    │ LLM call w/ SSE,         │
│                      │ streaming,          │ send email, resize image │
│                      │ short-lived jobs    │                          │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Workflow engine      │ Multi-step durable  │ 5-step onboarding w/     │
│ (turbine)            │ w/ resume after     │ human approval, report   │
│                      │ crash               │ pipeline, multi-system   │
│                      │                     │ integration              │
└──────────────────────┴─────────────────────┴──────────────────────────┘

```
PocketBase app layout:
```
workflow engine (turbine, inside PocketBase)
  └── pt_* tables in same PB DB
       └── Onboarding multi-step (signup → email → config)
       └── Report generation pipeline (fetch → process → deliver)
       └── External webhook integration w/ durable retry

task queue (goqite + SSE Hub, queue.db separate from PB)
  └── LLM calls w/ streaming → Datastar (simulate, supervision, tips)
  └── Short-lived background jobs
```

**Why it's expected:** River (PG job queue) + Temporal coexist in production.
SimpleQ (SQLite queue) + Temporal coexist. Temporal docs: "use Activity Task
Queues for lightweight dispatch, Workflow Task Queues for orchestration."

**Caveats:**
1. **DB isolation** — turbine uses `app.DB()` (PB). goqite uses `queue.db`
   separate. Good: PB write lock doesn't affect streaming.
2. **Complexity** — turbine adds 10+ `pt_*` tables to PB DB. Only worth it
   when you truly need durable replay.
3. **Atomicity** — turbine gives transactional atomicity (same DB as PB
   data). goqite doesn't need it (fire-and-forget).
4. **No LLM streaming in turbine** — steps block. Streaming stays in goqite.

## When to Use

| Intent | Prompt |
|--------|--------|
| Go web from scratch | "create a new go web app" |
| New feature | "create a feature" |
| Real-time/SSE | "add real-time updates" |
| Hypermedia | "Datastar style app" |
| Voice AI | "add voice assistant" |
| LLM integration | "add LLM calls" |
| Multi-agent | "coordinate agents in Go" |
| Durable workflow | "add workflows to my Go app" |
| Background queue | "add a queue to my app" |
| Database | "add persistence" |
| Whiteboard | "add collaborative whiteboard" |

## 🚨 templ for ALL HTML

Read: [references/templ/rules.md](./references/templ/rules.md)
No HTML in Go source. EVER.

---

## Queue / Workflow Decision Tree

This tree covers the full stack context: PocketBase + Datastar + NATS.

```
┌─ Step 1 ─────────────────────────────────────────────────────────────┐
│  Just enqueue & run background jobs (single step, no resume after    │
│  crash, no DAG)?                                                     │
│  YES → goqite (default, simple SQLite queue, ~18.5k msg/s)          │
│         See references/queue/goqite-patterns.md                      │
│         *alt: ebind/dagnats if multi-worker NATS needed*            │
└──────────────────────────────────────────────────────────────────────┘
                                │ NO
                                ▼
┌─ Step 2 ─────────────────────────────────────────────────────────────┐
│  Need durable workflow (multi-step, resume after crash), single       │
│  process / few processes on same host, no external broker?            │
│  YES → turbine (default)                                              │
│         Embeds in PocketBase SQLite, `WithName()` decouples step name │
│         from Go function → safe against LLM rewriting handlers.       │
│         Step replay only re-executes incomplete steps.                │
│         *alt: go-workflows if need signals/child-wf/tester*          │
│         *alt: Hatchet/Rivet if external service OK*                   │
└──────────────────────────────────────────────────────────────────────┘
                                │ NO
                                ▼
┌─ Step 3 ─────────────────────────────────────────────────────────────┐
│  Multiple workers/processes/machines competing on same queue,         │
│  or need distributed async events (beyond PocketBase scope)?          │
│  YES → ebind OR dagnats (both NATS JetStream-native)                 │
│         JetStream handles ack/nak/redelivery/distribution natively.   │
│         SQLite is single-writer — doesn't scale here.                 │
└──────────────────────────────────────────────────────────────────────┘
                                │ NO → you likely already have an answer
                                ▼
┌─ Step 4 ─────────────────────────────────────────────────────────────┐
│  Between ebind and dagnats — what matters more?                      │
│                                                                       │
│  lightweight lib embedded in your binary?  → ebind                   │
│  platform with triggers/console/UI?        → dagnats (experimental)   │
│                                                                       │
│  See comparison table below.                                          │
└──────────────────────────────────────────────────────────────────────┘

┌─ Step 5 ─────────────────────────────────────────────────────────────┐
│  Need mature deterministic workflow primitives (signals, child        │
│  workflows, durable timers, diagnostics UI, determinism analyzer)     │
│  AND accept bringing an extra database (SQLite/PG/MySQL/Redis)        │
│  even though you already have NATS?                                   │
│  YES → go-workflows                                                    │
│         Most mature of the five (500★, 4.5y, Temporal-inspired).     │
│         No `GetVersion()` — requires manual discipline when LLM       │
│         rewrites workflow functions. Only worth it if you really      │
│         need those rich primitives.                                   │
└──────────────────────────────────────────────────────────────────────┘
```



## Quick Start

### Examples

**1. Scaffold** — answer decision tree above, follow generated structure.
**2. Add features** — GoAI for LLM, Zenflow for agents, choose queue/workflow from decision tree.
**3. Sample** — see each tool's README for runnable examples.

### Checklist

```markdown
- [ ] UI: DaisyUI (default)
- [ ] Real-time: NATS Core / JetStream / None
- [ ] Database: SQLite / PocketBase / None
- [ ] Hybrid search: Bleve / None
- [ ] Voice AI: LiveKit+Gemini / None
- [ ] AI/Agent: GoAI / GoAI+Zenflow / None
- [ ] Queue: NATS JetStream / goqite / None
- [ ] Durable workflow: turbine / ebind / dagnats / go-workflows / Hatchet / None
- [ ] Whiteboard: Fabric.js / None
- [ ] Secrets: age+~/.secrets/ / env vars / none
- [ ] Module: `github.com/user/project`
- [ ] Deploy: your-server.com / other / none
```

---

## Detailed Decisions

### UI: DaisyUI (default)

Ready-made Tailwind components. Zero JS for basic UI.

### Real-time: NATS Core vs JetStream

| Need | Solution |
|------|----------|
| Broadcast (1→N) | NATS Core |
| History | JetStream |
| Work queues | JetStream Consumer |
| Key-Value | JetStream KV |
| Low latency | NATS Core |

### Database: SQLite vs PocketBase

```
Simple, embedded → SQLite (ncruces)
Multi-instance, auth, REST → PocketBase
```

Embeddings, FTS5, Bleve — see `references/database/` and `references/embeddings/`.

### Queue / Workflow Engine Details

See `references/queue/workflow-decision.md` for full details on each tool:
- goqite, turbine, ebind, dagnats, go-workflows, Hatchet
- ebind vs dagnats comparison table
- LLM + versioning safety rules
- Code samples

### goqite-specific references

See `references/queue/goqite-patterns.md` for:
- SSE Hub streaming pattern
- `retry-go` integration (or custom retry with SSE feedback)

---

### LLM + Workflows: Versioning Safety

See `references/queue/workflow-decision.md` (section "LLM + Workflows: Versioning Safety") for full rules.

**TL;DR:** Use `WithName()` (turbine) or explicit versioning (`MyWorkflowV2`). Keep activities stable. Test with mocks. Avoid non-determinism inside workflow code.

---

### Secrets: age + ~/.secrets/

**3-layer model:** env vars (runtime) → `~/.secrets/<project>.env.age` (rest, age-encrypted) → provider dashboard (source of truth).

| Scenario | Approach |
|----------|----------|
| Single server, 1-2 devs, <20 secrets | `~/.secrets/` + age encryption (this stack) |
| Secrets in git CI | SOPS + age |
| Multi-team, audit | Doppler / Vault |

**Setup:** `age` CLI → `bin/init-secrets` → decrypts via `AGE_SECRET_KEY` env var or `~/.secrets/key.txt`. See `references/secrets/age-patterns.md`.

**Go integration:** `internal/secrets` package, called by `config.Load()` before `os.Getenv`. Silent skip if `~/.secrets/` missing.

For full server-side audit hardening (UFW, SSH, Docker, Tailscale), see sibling skill `cali-ops-server-security`.

---

### Datastar Patterns

> ⚠️ See `references/datastar/patterns.md` for complete patterns.

| Attribute | Example | Purpose |
|-----------|---------|---------|
| `data-on:click` | `data-on:click="@post('/api/action')"` | Click handler |
| `data-signals` | ``data-signals={`{"count":0}`}`` 🔴 JSON only | Reactive state |
| `data-bind` | `data-bind="model"` | Two-way binding |
| `data-text` | `data-text="$count"` | Text content |
| `data-class` | `data-class="{'text-primary': $active}"` | Conditional classes |
| `data-show` | `data-show="$visible"` | Conditional visibility |

Key rules: Backend source of truth. Forms need `name` + `{contentType: 'form'}`.

---

## References

| Reference | What it contains |
|-----------|-----------------|
| `references/templ/rules.md` | Zero-tolerance templ rules, CI |
| `references/datastar/patterns.md` | Signals, SSE, events, indicators |
| `references/datastar/pitfalls.md` | Known Datastar pitfalls |
| `references/datastar/toast.md` | Backend-driven toasts |
| `references/datastar/versus_javascript.md` | JS vs Datastar decision matrix |
| `references/daisyui/datastar-integration.md` | DaisyUI + Datastar rules |
| `references/nats/when-to-use-jetstream.md` | NATS Core vs JetStream |
| `references/voice-ai/when-to-use.md` | LiveKit + Gemini setup |
| `references/whiteboard/fabric_patterns.md` | Fabric.js sync |
| `references/pii-masking/cloakpipe.md` | PII masking for LLM |
| `references/context-management/strategy.md` | Context window strategy |
| `references/embeddings/README.md` | ONNX, SBD, embeddings |
| `references/queue/goqite-patterns.md` | goqite ctx rules, SSE Hub, retry with SSE feedback, canonical layer diagram |
| `references/queue/nats-workflow-patterns.md` | NATS delay/retry/rate-limit/concurrency patterns |
| `references/queue/workflow-decision.md` | Full details: goqite, turbine, ebind, dagnats, go-workflows, Hatchet, Rivet + ebind vs dagnats table + LLM versioning safety |
| `references/database/` | SQLite vs PB decision, CRUD |
| `references/examples/` | UI pattern examples |
| `references/datastar/` | Datastar patterns, pitfalls, DaisyUI integration |
| `bin/datastar-lint` (cali-go-stack) | Wrapper that installs + runs `github.com/calionauta/datastar-lint` |
| `references/ci/docker-cache.md` | Fast Docker builds |
| `references/deploy.md` | CI/CD, Docker, versioning |
| `references/llm-streaming.md` | LLM + SSE streaming (Datastar throttling, visible/hidden mode) |
| `references/troubleshooting.md` | Error diagnostics |
| `references/queue/sse-hub-patterns.md` | SSE Hub usage with goqite workers: register-before-enqueue, replay buffer, backpressure |
| `references/secrets/age-patterns.md` | age + ~/.secrets/ setup, troubleshooting |

---

## Datastar Lint (datastar-lint)

Validate Datastar `data-*` attributes against the spec. **Use the public binary — do NOT vendor a local copy.**

- Repo: `github.com/calionauta/datastar-lint` (language-agnostic: html, htm, templ)
- Install: `go install github.com/calionauta/datastar-lint@latest`
- Run (after `templ generate`): `datastar-lint -r ./features/`
- Flags: `-r` recursive, `-e "html,htm,templ"` extensions, `-s` strict (Pro attrs error)
- Exit `0` clean, `1` issues.

The `cali-go-stack` project wires this via `bin/datastar-lint` (pre-commit + `make datastar-lint`); the pi pre-commit hook installs and runs it automatically. Do not reintroduce a skill-local `references/datastar-lint/main.go`.

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| data-signals JSON escaping | Use `json.Marshal` |
| Form data not sending | Add `name` to inputs |
| Textareas not syncing | Use `data-bind` |
| Tabs not working | Use `data-show` only |
| Loading state stuck | `MarshalAndPatchSignals` |
| go-workflows non-determinism | Use `workflow.SideEffect`, `workflow.Select` |
| Activity retries not idempotent | Wrap with `workflow.NewPermanentError` |
| LLM renamed handler, replay broken | Use `WithName()` (turbine) or rename function explicitly |
| NATS + go-workflows stack confusion | go-workflows uses its own DB, not NATS. NATS is separate for messaging. |

---

## Best Practices

1. **Self-contained features** — each in own directory
2. **KISS (SSE)** — prefer SSE over WebSockets for one-way updates
3. **Indicators** — always show loading states
4. **DRY SSE** — extract `renderAndPatch` helper
5. **LoC** — prefer Datastar signals over JS DOM manipulation
6. **No HTML in Go** — use Templ components
7. **Idempotent activities** — always, retry is automatic
8. **Workflow determinism** — no `rand`, `time.Now`, `map range`
9. **Decouple step names from Go function names** — especially when LLM generates workflows

---

## Testing Protocol

After any browser-facing change:
1. Load `agent-browser` skill — navigate, verify no JS errors
2. Load `dogfood` skill — systematic edge case exploration

---

## Test Cases

### Should activate
- "Create a new Go web app with Datastar and Templ"
- "Add real-time updates to my Go project using SSE"
- "Add LLM calls with GoAI and multi-agent workflows with Zenflow"
- "Add a background queue with goqite"
- "Add a durable workflow with turbine/ebind/dagnats/go-workflows"
- "Set up a Hatchet workflow for job execution"
- "Add voice AI with LiveKit to my Go app"
- "Create a new feature module"
- "Migrate existing project to Datastar"
- "Set up Postgres with sqlc and golang-migrate"

### Should NOT activate
- "Write a Go CLI tool" (use `cali-coding-go-standards`)
- "Review my Go code for bugs" (use `cali-coding-go-standards`)
- "Debug a goroutine leak" (use `cali-coding-go-standards`)
- "Set up golangci-lint" (use `cali-coding-go-standards`)
