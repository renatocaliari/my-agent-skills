# Testing Strategies for Single-Binary Go + PocketBase/SQLite

## Context

This reference targets small, solo-developed Go projects with these characteristics:

- **Single Go binary** that ships an HTTP server (Datastar, Chi, Gin, etc.)
- **PocketBase or SQLite** as the embedded database (via `pocketbase/pocketbase` or `ncruces/go-sqlite3`)
- **One or two external API integrations** (LLM providers, email, etc.)
- **No docker, no CI, no test staging** — `go test ./...` runs locally

If your project has 50+ engineers, a dedicated QA team, or a multi-service architecture, this playbook is too simple. Use [kagent-dev/mockllm](https://github.com/kagent-dev/mockllm), [VCR.py](https://vcrpy.readthedocs.io/), or [Reel](https://github.com/tathagat22/reel) instead.

## The Default Hybrid Strategy

Three layers, in order of effort vs. value:

### 1. Pure function tests (highest leverage)

Cover every serialiser, formatter, and data-model helper as a direct unit test. No setup, no fixtures, no DB.

```go
func TestSupervisionJSON_IndicatorSafe(t *testing.T) {
    cases := []struct{ name, in, want string }{
        {"green", "green", "green"},
        {"empty falls back to unavailable", "", "unavailable"},
    }
    for _, tt := range cases {
        t.Run(tt.name, func(t *testing.T) {
            sj := supervisionJSON{Indicator: tt.in}
            if got := sj.IndicatorSafe(); got != tt.want {
                t.Errorf("got %q, want %q", got, tt.want)
            }
        })
    }
}
```

When a helper stops being pure (e.g. it calls `ns.getSupervisionCriteria()`), extract the parameters it reads from external state and pass them in.

### 2. Function-field injection for LLM calls

For each external call (LLM, email, etc.), add an optional function field to the service struct. Production leaves it nil; tests inject a stub. The pattern is five lines:

```go
type NarrativeService struct {
    // ... existing fields ...
    superviseFn func(ctx context.Context, settings *db.UserSettings, promptID string, prompt string, tools []goai.Tool, onRawResponse ...func(string)) (*supervisionJSON, error)
}

func (ns *NarrativeService) superviseViaNS(ctx context.Context, settings *db.UserSettings, promptID string, prompt string, tools []goai.Tool, onRawResponse ...func(string)) (*supervisionJSON, error) {
    if ns.superviseFn != nil {
        return ns.superviseFn(ctx, settings, promptID, prompt, tools, onRawResponse...)
    }
    return superviseLLM(ctx, settings, promptID, prompt, tools, onRawResponse...)
}
```

Replace all internal callers (`superviseLLM(...)` → `ns.superviseViaNS(...)`). One call site per LLM, one field, one wrapper.

**Test:**

```go
ns.superviseFn = func(ctx context.Context, settings *db.UserSettings, promptID string, prompt string, tools []goai.Tool, onRawResponse ...func(string)) (*supervisionJSON, error) {
    return &supervisionJSON{Indicator: "green", Alignment: "ok"}, nil
}
ns.sendSupervisionMessage(sse, sessionID, "msg")
// assert message was saved with indicator=green
```

**Why not interface extraction?** Interfaces at every LLM call site mean the production code and test code both pay the indirection cost. Function fields keep the production path zero-overhead.

**Why not VCR-style recording?** For one binary with one LLM provider, recording and replaying fixtures costs more developer time to maintain than the 0¢ saved per test run.

**When to use a real HTTP fake server (`httptest.NewServer`):** Only when testing the LLM *client/transport layer itself* — i.e. the package that wraps GoAI/OpenAI and is responsible for wire format, `Authorization` headers, SSE streaming shape, and `context.Context` deadline propagation. In that narrow case, a local `httptest.Server` speaking the `/v1/chat/completions` slice is the right tool: it exercises the real HTTP path with zero tokens and no egress. Reference implementation: `internal/llm/fakeserver` (gogogo-template). For every *consumer* of the LLM (features, services), use function-field injection — do NOT spin up `httptest` in those tests.

### 3. In-memory database for integration tests

For a PocketBase + SQLite stack, spin up a temp-dir PB instance per test:

```go
func testPocketBase(t *testing.T) func() {
    t.Helper()
    tmpDir, err := os.MkdirTemp("", "pb-test-*")
    if err != nil { t.Fatalf("MkdirTemp: %v", err) }

    app, err := db.InitPocketBase(tmpDir, "0", true)
    if err != nil { os.RemoveAll(tmpDir); t.Fatalf("InitPocketBase: %v", err) }
    if err := app.Bootstrap(); err != nil { t.Fatalf("Bootstrap: %v", err) }
    if err := db.EnsureCollections(app); err != nil { t.Fatalf("EnsureCollections: %v", err) }
    if err := db.SeedUsers(app); err != nil { t.Logf("SeedUsers: %v", err) }
    if err := db.SeedTemplates(app); err != nil { t.Logf("SeedTemplates: %v", err) }

    prevApp := db.PocketBaseApp
    db.PocketBaseApp = app
    return func() {
        db.PocketBaseApp = prevApp
        os.RemoveAll(tmpDir)
    }
}
```

Two things matter:

1. **`db.PocketBaseApp = app`** — your service probably reads a global; assign it.
2. **The cleanup func** — restore the previous app + remove the temp dir. Run via `defer cleanup()`.

For SSE handlers, mock the writer:

```go
import "net/http/httptest"
import datastar "github.com/starfederation/datastar-go/datastar"

rec := httptest.NewRecorder()
req := httptest.NewRequest("POST", "/api/ui/action?action=foo", nil)
sse := datastar.NewSSE(rec, req)
ns.sendSupervisionMessage(sse, sessionID, "msg")
```

If your service uses `jobs.Enqueue` (a goqite-based worker queue), also init the queue with a temp dir:

```go
func testJobsQueue(t *testing.T) func() {
    t.Helper()
    tmpDir, err := os.MkdirTemp("", "jobs-test-*")
    if err != nil { t.Fatalf("MkdirTemp: %v", err) }
    if err := jobs.Init(jobs.Config{DBPath: filepath.Join(tmpDir, "queue.db")}); err != nil {
        os.RemoveAll(tmpDir); t.Fatalf("jobs.Init: %v", err)
    }
    return func() { jobs.Q = nil; os.RemoveAll(tmpDir) }
}
```

**Caution:** if the queue's worker auto-starts, you'll deadlock waiting for events. The fix: stub the worker function too, or `t.Skip` with a comment explaining the limitation.

## When to Stop Adding Tests

Stop when you've covered:

1. All pure helpers (most of the codebase in 80% of cases).
2. One happy-path integration test per user-facing flow (chat message → saved, retry → updated, fork → new session created).
3. One error-recovery test per LLM call (transient failure → retry, permanent failure → toast).

Anything beyond that is diminishing returns. Specifically:

- Don't add unit tests for every prompt template — the data is in DB, tested by integration.
- Don't add tests for HTML rendering — Templ templates are visual; verify by smoke test.
- Don't add tests for utility libraries (`embed`, `time.Now`, `json.Marshal`) — they have their own tests.

## Anti-Patterns

| Anti-pattern | Why it hurts | Use instead |
|--------------|-------------|-------------|
| Mock the entire `pocketbase.PocketBase` struct | Tight coupling, breaks on PB version bumps | Temp-dir PB + Bootstrap |
| Interface-extract every repo before any test exists | Premature abstraction, hard to refactor later | Function fields for LLM, real DB for repos |
| HTTP test server (`httptest.NewServer`) for LLM stubs in **feature/business-logic tests** | Unnecessary network stack, slow, couples the test to transport details the logic under test shouldn't care about | Function fields for business logic |
| HTTP test server (`httptest.NewServer`) for the **LLM client/transport layer itself** (wire format, auth, SSE, timeouts) | — (this is the correct tool; see `internal/llm/fakeserver` pattern) | Use it when testing the client package, not its consumers |
| `t.Skip` instead of fixing the test | Hides the test coverage gap | Fix it or use a smaller scope |
| Test-only methods on service structs (`*ForTesting`) | Pollutes the API | Function fields, set in test setup |

## When to Upgrade to a Heavier Solution

Consider a mock LLM server ([kagent-dev/mockllm](https://github.com/kagent-dev/mockllm)) or fixture-based recording ([Reel](https://github.com/tathagat22/reel)) when:

- You have **more than 5 LLM call sites** and find yourself adding function fields to multiple structs.
- You're **hitting rate limits or costs** in CI even with function injection.
- You want **non-deterministic test runs** to surface real provider behavior changes.

For a typical solo project, you'll never hit that point. Keep the function field pattern until the day you do.

## Skeleton

```go
// test_helpers_test.go
package handlers

import (
    "net/http/httptest"
    "os"
    "testing"

    "github.com/renatocaliari/treinador-praticas-narrativas/db"
    datastar "github.com/starfederation/datastar-go/datastar"
)

func testPocketBase(t *testing.T) func() {
    t.Helper()
    tmpDir, err := os.MkdirTemp("", "pb-test-*")
    if err != nil { t.Fatalf("MkdirTemp: %v", err) }

    app, err := db.InitPocketBase(tmpDir, "0", true)
    if err != nil { os.RemoveAll(tmpDir); t.Fatalf("InitPocketBase: %v", err) }
    if err := app.Bootstrap(); err != nil { t.Fatalf("Bootstrap: %v", err) }
    if err := db.EnsureCollections(app); err != nil { t.Fatalf("EnsureCollections: %v", err) }
    if err := db.SeedUsers(app); err != nil { t.Logf("SeedUsers: %v", err) }

    prev := db.PocketBaseApp
    db.PocketBaseApp = app
    return func() {
        db.PocketBaseApp = prev
        os.RemoveAll(tmpDir)
    }
}

func testSSE() (*datastar.ServerSentEventGenerator, func() string) {
    rec := httptest.NewRecorder()
    req := httptest.NewRequest("POST", "/api/ui/action", nil)
    sse := datastar.NewSSE(rec, req)
    readFn := func() string {
        rec.Result().Body.Close()
        return rec.Body.String()
    }
    return sse, readFn
}
```

## Sources

Patterns synthesised from:

- [kagent-dev/mockllm](https://github.com/kagent-dev/mockllm) — full HTTP mock server pattern
- [VCR.py](https://vcrpy.readthedocs.io/) — fixture capture/replay
- [Reel](https://github.com/tathagat22/reel) — proxy-mode VCR for LLM
- [goai test patterns in OpenAI-Go](https://github.com/openai/openai-go) — function field injection
- Red Hat OpenShift AI integration testing ([developers.redhat.com](https://developers.redhat.com/articles/2026/05/27/how-we-built-integration-testing-fast-moving-ai-backend))
- The LLM Local Development Loop ([tianpan.co](https://tianpan.co/blog/2026-04-18-llm-local-dev-loop))

The default strategy above picks the lowest-effort approach from each.
