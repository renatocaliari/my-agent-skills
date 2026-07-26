# Queue & Workflow Engine Details

Full reference for the tools listed in the decision tree (see SKILL.md).

---

## goqite — simple background queue

- **When:** Single-process, no NATS, no DAG, just enqueue + handler
- **How:** SQLite-backed SQS-like queue. `queue.New(db)`, `jobs.Enqueue(ctx, payload)`
- **Benchmark:** ~18.5k msg/s single-writer, 528★, actively maintained
- **Trade-off:** Not a durable workflow engine — no step replay, no DAG
- **Reference:** `references/queue/goqite-patterns.md` (ctx rules, SSE Hub race)
- **GitHub:** https://github.com/maragudk/goqite

---

## turbine — durable workflow, single-process, PocketBase-native

- **When:** Durable multi-step workflow, single process, embeds in PocketBase's own SQLite
- **Key feature:** `WithName()` decouples the persisted step name from the Go function name. If LLM renames the Go function, the persisted step name stays → replay still finds the correct handler. **Safe against agent rewriting functions.**
- **Step replay:** Environment saves completed step outputs individually. On crash/resume, only incomplete steps re-execute. Completed steps restore from DB — no re-run.
- **Trade-off:** Single-writer SQLite — does not scale to multiple workers/machines. No NATS integration.
- **GitHub:** https://github.com/YakirOren/turbine

---

## ebind — NATS-native task queue + DAG, same binary

- **When:** Multi-worker, NATS already in stack, need typed function-first API
- **API:** `Register(reg, MyFunc)`, `Enqueue(c, MyFunc, args...)`, `Await[T](ctx, fut)` — compile-time function reference, not string dispatch
- **DAG:** `dag.Step("a", Fn).Ref()` → `dag.Step("b", Fn2, a.Ref())`, with `RefOrDefault` for optional steps
- **HA:** `embed.StartCluster()` spawns 3-node JetStream cluster in-process
- **Trade-off:** No native cron/webhook triggers, no ops console. Function name inferred from Go reflection (no `WithName()` documented — LLM renaming risk is medium).
- **GitHub:** https://github.com/F1bonacc1/ebind

---

## dagnats — NATS-native DAG engine with console/triggers

- **When:** Multi-worker, need cron/webhook triggers + ops console, accept sidecar
- **Workflow definition:** JSON primary format (+ Go builder for tests/in-process use)
- **Native triggers:** Cron, webhook, NATS subject, HTTP request/response
- **Console:** Built-in Datastar web UI at `http://127.0.0.1:8080/console/`
- **Extra step types:** Agent loops, sub-workflows, sleep, wait-for-event, approval gates, map (fan-out), planner (LLM generates steps at runtime)
- **Trade-off:** Experimental (2★, single author), sidecar (second process), large surface (83k LOC non-test), capability grants and agent runtimes may be incomplete
- **GitHub:** https://github.com/danmestas/dagnats

---

## go-workflows — full Temporal-like engine

- **When:** Need signals, child workflows, durable timers, diagnostics UI, determinism analyzer. Accept bringing an extra database.
- **Key features:**
  - **Event-sourced replay** — history stored in SQLite/PG/MySQL/Redis
  - **Sub-workflows** — `workflow.CreateSubWorkflowInstance`
  - **Signals** — `workflow.SignalWorkflow` + `workflow.NewSignalChannel`
  - **Timers** — `workflow.ScheduleTimer`
  - **Cancel** — `c.CancelWorkflowInstance` + context cancel
  - **ContinueAsNew** — restart with fresh history to control history size
  - **Tester** — `tester.NewWorkflowTester` with mocked activities (advance mock clock). Catches non-determinism early.
  - **Diagnostics UI** — `diag.NewServeMux(b)` for history inspection
  - **OpenTelemetry** — tracer provider passthrough
  - **Determinism analyzer** — golangci-lint linter catches `time.Now()`, `rand`, `map range` inside workflow code
- **Trade-offs:**
  - Requires its own database (SQLite/PG/MySQL/Redis) — separate file from PocketBase
  - **No `GetVersion()`** — manual discipline needed when LLM rewrites workflow functions (rename function for breaking changes)
  - **No NATS integration** — go-workflows persists to its own DB, not NATS. NATS can still run separately for messaging/bridge. They coexist but don't share storage.
- **Sample:**
```go
b := sqlite.NewSqliteBackend("workflows.db")
w := worker.New(b, nil)
w.RegisterWorkflow(MyWorkflow)
w.RegisterActivity(Activity1)
go w.Start(ctx)

c := client.New(b)
wf, _ := c.CreateWorkflowInstance(ctx, client.WorkflowInstanceOptions{
    InstanceID: uuid.NewString(),
}, MyWorkflow, "input")
```
```go
func MyWorkflow(ctx workflow.Context, input string) (string, error) {
    r1, _ := workflow.ExecuteActivity[int](ctx, workflow.DefaultActivityOptions, Activity1, input).Get(ctx)
    return fmt.Sprintf("result: %d", r1), nil
}
func Activity1(ctx context.Context, name string) (int, error) {
    return len(name), nil
}
```
- **GitHub:** https://github.com/cschleiden/go-workflows

---

## Hatchet — advanced external engine

- **When:** Multi-service, need Postgres dashboard, advanced monitoring, DAG visualizer
- **Architecture:** External Postgres-based engine. App connects via Go SDK.
- **Dashboard:** Built-in UI for workflows, runs, monitoring, logs
- **Local dev:** `hatchet server start` (Docker) or `--local` (embedded PG)
- **Trade-off:** External service — adds Postgres + container to your stack
- **GitHub:** https://github.com/hatchet-dev/hatchet

## Rivet — self-hosted Durable Execution platform

- **When:** Need a complete platform with Temporal-compatible SDK, serverless actors, browser-based IDE. Accept running external infra (Docker/Postgres/FoundationDB).
- **Architecture:** Rivet Engine (Go) + your backend (any language). Storage: filesystem, Postgres, or FoundationDB. Temporal SDK compatible.
- **Key features:** Browser-based IDE (`rivet debug`), hot reload, serverless actor lifecycle, envelope-based execution
- **Trade-off:** External service — requires Docker/Postgres/FoundationDB. Not embeddable. Different model from the embedded tools above.
- **GitHub:** https://github.com/rivet-dev/rivet
- **Self-hosting:** https://rivet.dev/docs/self-hosting/

---

## ebind vs dagnats — detailed comparison

| Criterion | ebind | dagnats |
|-----------|-------|---------|
| **Model** | Embedded Go library | Platform/service (`dagnats serve`) with own API |
| **Workflow definition** | Go only, typed generics (`Register`, `Enqueue`, `Await[T]`) | JSON primary (+ Go builder) |
| **Native triggers** (cron/webhook) | No | Yes |
| **Console / ops UI** | No | Yes |
| **HA without extra infra** | Yes — `embed.StartCluster` spawns 3-node JetStream in-process | Depends on external NATS (which you already have) |
| **Lock-in risk (LLM rewrites)** | Medium — dispatch by function name, inferred from Go (no `WithName` documented) | Medium/good — dispatch by task name in JSON, naturally decoupled from Go impl |
| **Operational complexity** | Low (just the lib + NATS you already run) | High (another service, control plane via nats-micro, agent runtimes, capability grants) |
| **Observed maturity** | CI + CodeQL, production concerns doc, but 0★, single author | Ambitious README (agent-created workflows, capability grants) but large surface — more risk of untested edges |
| **Choose when** | You want typed task/DAG orchestration over your existing NATS, no extra service to run | You need cron/webhook triggers + ops console, and accept running and maintaining an additional service |
