# goqite — Specific Patterns

[goqite](https://github.com/maragudk/goqite) is the lightweight persistent queue used for background jobs in this stack. This reference covers ONLY rules not already in other skills (lint rules in `cali-coding-go-standards/gorules.go`, SSE/Datastar patterns in `references/datastar/*`).

## Canonical Layer Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     PocketBase App                          │
│  ┌─────────────────────┐  ┌──────────────────────────────┐  │
│  │ turbine (wf engine) │  │ goqite + SSE Hub (task q)   │  │
│  │ pt_* tables in PB   │  │ queue.db separate            │  │
│  │ Onboarding,         │  │ LLM simulate/supervision     │  │
│  │ pipeline, webhook   │  │ streaming → Datastar         │  │
│  └─────────────────────┘  └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Rule #1: `ctx context.Context` is never `nil`

goqite forwards `ctx` to `database/sql.DB.BeginTx` via `internal/sql.InTx`. That helper dereferences `ctx` internally. Passing `nil` panics at runtime:

```
runtime error: invalid memory address or nil pointer dereference
  maragu.dev/goqite/internal/sql.InTx
  maragu.dev/goqite.(*Queue).SendAndGetID
  maragu.dev/goqite/jobs.Create
  ...your handler...
```

Use `context.Background()` when no cancellation is needed. Convention over configuration.

### UI symptoms when ctx=nil

1. Initial SSE patches (loading bubbles) reach the browser
2. Panic in `Enqueue` before the worker picks up the job
3. `panicRecover` middleware (PocketBase) absorbs it silently
4. UI stuck on loading; refresh shows only the previous message
5. `queue.db` stays empty — job was never enqueued
6. **server stderr contains the stack trace** — always inspect logs when a worker is "stuck"

## Rule #2: SSE Hub race

goqite runs the job in a goroutine separate from the HTTP handler. To stream results back:

```go
// Handler: Register BEFORE Enqueue
hub.Register(sessionID)
defer hub.Unregister(sessionID, handlerID)
// ... render loading bubbles ...
jobs.Enqueue(ctx, payload)  // safe to call now

// Worker (separate goroutine): Send events
hub.Send(sessionID, SSEEvent{Type: "chunk", ...})
hub.Send(sessionID, SSEEvent{Type: "complete", ...})
hub.Send(sessionID, SSEEvent{Type: "error", ...})
```

⚠️ **Race**: Calling `Register` AFTER `Enqueue` lets the worker send events before the handler is listening — events get dropped.

## Rule #3: Retry with SSE feedback

### Option A — Custom loop (preferred, max SSE control)

Use when you need to publish `retry-status` events between attempts so the UI shows "Attempt X of N" in real time:

```go
func handleLLMJob(ctx context.Context, p Payload) error {
    hub := GetSSEHub()
    const maxAttempts = 5
    var lastErr error

    for attempt := 1; attempt <= maxAttempts; attempt++ {
        if ctx.Err() != nil {
            return ctx.Err()
        }

        // SSE event: UI updates retry indicator immediately
        hub.Send(p.SessionID, SSEEvent{
            Type: "retry-status", Attempt: attempt,
            MaxTries: maxAttempts, BubbleID: p.BubbleID,
        })

        _, sErr := streamOnce(ctx, model, p, "complete")
        if sErr == nil {
            return nil
        }
        lastErr = sErr
        if attempt < maxAttempts {
            // Exponential backoff: 1s → 2s → 4s → 8s (capped)
            delay := time.Duration(1<<min(attempt-1, 3)) * time.Second
            select {
            case <-time.After(delay):
            case <-ctx.Done():
                return ctx.Err()
            }
        }
    }
    hub.Send(p.SessionID, SSEEvent{Type: "error", JobType: p.JobType, ErrMsg: lastErr.Error()})
    return fmt.Errorf("%s: %d attempts exhausted: %w", p.JobType, maxAttempts, lastErr)
}
```

**Why custom loop over retry-go:** The SSE `retry-status` event between
attempts is the critical feature. `retry-go`'s `OnRetry` callback runs
*after* a failure, which works — but the custom loop is fewer lines,
no dependency, no callback indirection, and keeps retry logic colocated
with the SSE Hub reference.

### Option B — avast/retry-go (valid when SSE feedback not needed)

```go
import "github.com/avast/retry-go/v5"

err := retry.Do(
    func() error {
        return llmCall(ctx, prompt)
    },
    retry.Attempts(5),
    retry.Delay(1*time.Second),
    retry.MaxDelay(8*time.Second),
    retry.DelayType(retry.CombinedDelay(
        retry.BackOffDelay,
        retry.RandomDelay,
    )),
    retry.Context(ctx),
    retry.OnRetry(func(n uint, err error) {
        log.Printf("retry %d: %v", n, err)
        // SSE possible here if hub accessible:
        // hub.Send(sessionID, SSEEvent{Type: "retry-status", Attempt: int(n)+1, ...})
    }),
)
```

`OnRetry` is called after each failure. If your handler has access to
`*SSEHub` (via global or context), you CAN publish SSE status. However:
- Need to capture `sessionID`/`BubbleID` in closure — must thread them
  through the retry-go options, which is awkward.
- The custom loop is cleaner when retry-status SSE is required.

**Decision:** Use custom loop (Option A) for ALL LLM workers that stream
to UI. Use retry-go (Option B) for fire-and-forget background jobs where
the caller doesn't need progress visibility.

## Rule #4: timeout management

goqite's `jobs.Runner` already extends message timeout automatically:

```go
// runner.go (goqite v0.4.0):
go func() {
    time.Sleep(r.extend - r.extend/5)  // ~4s (default 5s)
    for {
        select {
        case <-jobCtx.Done():
            return
        default:
            r.queue.Extend(jobCtx, m.ID, r.extend)  // +5s
            time.Sleep(r.extend - r.extend/5)
        }
    }
}()
```

**Default extend interval:** 5s. Each extension resets the message timeout
by 5s. Effective for LLM calls up to minutes. No manual `Extend` needed
unless your job runs longer than the runner's total timeout.

**Caveats:**
- Extend happens AFTER `r.extend - r.extend/5` (~4s) delay. If the job
takes < extend-interval, the goroutine does one sleep and exits — no
wasted cycle.
- Extend is best-effort (error is logged, not retried). If extend
fails repeatedly, the message may be re-received by another worker
(effectively: the job runs twice). Idempotent handlers are still
recommended.

## When to use which

See main SKILL.md section **Durable Execution & Workflow Engines** for full decision tree.

Quick summary:

| Situation | Choice |
|----------|---------|
| Embedded durable workflow, Temporal-like, SQLite/any backend | **go-workflows** (same binary) |
| Simple queue + SSE streaming, no DAG | **goqite** (default) |
| Multi-worker, NATS-native | **ebind / dagnats** |
| Multi-service, Postgres dashboard | **Hatchet** (external) |
| Full Temporal-like with tester, signals | **go-workflows** |
| Fire-and-forget, no persistence | plain goroutine |

## When NOT to use goqite

- **Need durable workflows, sub-workflows, signals, timers** → use turbine or go-workflows
- **Need multi-service Postgres dashboard** → use Hatchet
- **NATS-native DAG** → use dagnATS or ebind
- **Fire-and-forget trivial work** with no persistence → plain goroutine
- **Need scheduled/cron jobs** → turbine or separate cron service

## Related References

- SSE/Datastar patterns: `references/datastar/patterns.md`
- Stack decision tree: main SKILL.md (section "Durable Execution & Workflow Engines")
- NATS workflow patterns: `references/queue/nats-workflow-patterns.md`
- SSE Hub reference: `references/queue/sse-hub-patterns.md`
- goqite docs upstream: https://github.com/maragudk/goqite