# NATS Workflow Patterns (Durable Execution Without Engine)

NATS JetStream solves delay, retry, rate limit, concurrency, and queues **without an external engine**. Use these patterns directly when you don't need a full DAG engine.

---

## Delay / Retry (NakWithDelay)

Native NATS. No extra library.

```go
// Handler: retry with backoff
func handler(msg jetstream.Msg) {
    err := process(msg.Data())
    if err != nil {
        msg.NakWithDelay(5 * time.Second)
        return
    }
    msg.Ack()
}
```

Consumer-level backoff (server manages timers):

```go
cons, _ := js.OrderedConsumer(ctx, "TASKS", jetstream.MaxDeliver(5),
    jetstream.Backoff([]time.Duration{
        time.Second, 5 * time.Second, 15 * time.Second, time.Minute,
    }),
)
```

---

## Rate Limit (MaxAckPending + Handler-side)

NATS native:

```go
cons, _ := js.OrderedConsumer(ctx, "TASKS",
    jetstream.MaxAckPending(50),
    jetstream.MaxDeliver(3),
    jetstream.Backoff([]time.Duration{time.Second, 5 * time.Second}),
)
```

Handler-side with `uber-go/ratelimit` (4.7k stars, maintained by Uber):

```go
import "go.uber.org/ratelimit"

var rl = ratelimit.New(100) // 100 req/s

func handler(msg jetstream.Msg) {
    rl.Take()
    // process
    msg.Ack()
}
```

---

## Keyed Rate Limit (NATS KV Token Bucket)

Self-contained implementation (~50 lines) using NATS KV with CAS. Pattern from DagnATS `engine/ratelimit.go`:

```go
type TokenBucket struct {
    Tokens     int   `json:"tokens"`
    LastRefill int64 `json:"last_refill_ns"`
    Limit      int   `json:"limit"`
    PeriodNs   int64 `json:"period_ns"`
}

func (rl *RateLimiter) Allow(ctx context.Context, key string, limit int, period time.Duration, units int) (bool, error) {
    // CAS loop: load bucket → refill → consume → save
    // kv.Get, json.Unmarshal, kv.Update with revision
}
```

Usage:

```go
allowed, _ := limiter.Allow(ctx, "user:"+userID, 10, time.Minute, 1)
if !allowed { http.Error(w, "rate limit", 429); return }
```

---

## Concurrency (Max Runs Per Workflow)

KV bucket with atomic counter:

```go
func acquireRunSlot(ctx context.Context, kv jetstream.KeyValue, wfID string, max int) (bool, error) {
    for attempt := 0; attempt < 10; attempt++ {
        entry, err := kv.Get(ctx, "concurrency:"+wfID)
        if errors.Is(err, jetstream.ErrKeyNotFound) {
            _, err = kv.Create(ctx, "concurrency:"+wfID, []byte("1"))
            return err == nil, nil
        }
        count, _ := strconv.Atoi(string(entry.Value()))
        if count >= max { return false, nil }
        _, err = kv.Update(ctx, "concurrency:"+wfID, []byte(strconv.Itoa(count+1)), entry.Revision())
        if err == nil { return true, nil }
    }
    return false, errors.New("CAS exhausted")
}

func releaseRunSlot(ctx context.Context, kv jetstream.KeyValue, wfID string) {
    // decrement via CAS
}
```

---

## Cron / Scheduling (gocron/v2)

`gocron/v2` (5k+ stars, actively maintained) for embedded single-instance cron:

```go
import "github.com/go-co-op/gocron/v2"

s, _ := gocron.NewScheduler()
_, _ = s.NewJob(
    gocron.CronJob("0 9 * * MON", false),
    gocron.NewTask(func() {
        nc.Publish("reports.weekly", nil)
    }),
)
s.Start()

// Worker subscribes to the same subject
nc.Subscribe("reports.weekly", func(msg *nats.Msg) {
    generateReport()
})
```

For distributed leader-election cron, build a schedule loop with NATS `NakWithDelay`: publish next fire time as NakWithDelay, on redelivery check if still leader, fire and re-schedule.

> **Note:** `trader7/nats-cron` was evaluated but abandoned (no commits since Aug 2025, 0 stars). Not recommended.

---

## Approval Gate (NATS KV Signal + Timeout)

No external library needed. ~30 lines, zero deps:

```go
// Worker pauses step
stepStatus := "pending_approval"
kv.Put(ctx, "approval:"+stepID, []byte(stepStatus))

// Watcher goroutine with timeout
watcher, _ := kv.Watch("approval:" + stepID)
select {
case entry := <-watcher.Updates():
    if string(entry.Value()) == "approved" {
        // continue workflow
    }
case <-time.After(24 * time.Hour):
    // timeout — cancel or retry
}

// Operator approves via API endpoint
func handleApprove(w http.ResponseWriter, r *http.Request) {
    kv.Put(ctx, "approval:"+stepID, []byte("approved"))
}
```

> **Note:** `lawale/quorum` was evaluated but it is a standalone HTTP server with Postgres/SQL Server (not a library). It adds a second process + DB. For single-binary, NATS KV signal is simpler and zero-dependency.

---

## Sub-Workflow (deepnoodle-ai/workflow)

Lightweight DAG workflow library with child workflows, checkpointing, branching, signal/sleep/pause (40 stars, 7 forks, Apache 2.0):

```go
import "github.com/deepnoodle-ai/workflow"

wf, _ := workflow.New(workflow.Options{
    Name: "parent",
    Steps: []*workflow.Step{
        {Name: "child", Activity: "my_child_wf", Next: []*workflow.Edge{{Step: "done"}}},
        {Name: "done", Activity: "print", Parameters: map[string]any{"message": "ok"}},
    },
})
exec, _ := workflow.NewExecution(wf, reg)
runner := workflow.NewRunner()
result, _ := runner.Run(ctx, exec)
```

---

## State Machine (looplab/fsm + NATS KV)

`looplab/fsm` (3.4k stars, 12 years mature) + NATS KV for persistence:

```go
import "github.com/looplab/fsm"

type OrderFSM struct {
    fsm *fsm.FSM
    kv  jetstream.KeyValue
}

func NewOrderFSM(initial string, kv jetstream.KeyValue) *OrderFSM {
    o := &OrderFSM{kv: kv}
    o.fsm = fsm.NewFSM(initial, fsm.Events{
        {Name: "pay", Src: []string{"pending"}, Dst: "paid"},
        {Name: "ship", Src: []string{"paid"}, Dst: "shipped"},
    }, fsm.Callbacks{
        "after_pay": func(e *fsm.Event) {
            o.kv.Put(context.Background(), "fsm:order:123", []byte(o.fsm.Current()))
        },
    })
    return o
}
```

---

## Datastar SSE Integration

No engine has native Datastar integration (DagnATS only in its own console). Bridge via NATS publish → Datastar SSE handler:

```go
func handleWorkflowEvent(nc *nats.Conn, sse *datastar.ServerSentEventGenerator) {
    nc.Subscribe("workflow.events.>", func(msg *nats.Msg) {
        sse.PatchElements(string(msg.Data))
    })
}
```

---

## Summary: When to Use Each Pattern

| Pattern | Library | When |
|---------|---------|------|
| Delay/retry | NATS `NakWithDelay` | Any handler |
| Rate limit (local) | `uber-go/ratelimit` | In-memory, single instance |
| Rate limit (keyed) | NATS KV token bucket | Distributed, multi-instance |
| Concurrency runs | NATS KV CAS | Limit workflow parallelism |
| Cron | `gocron/v2` or NATS NakWithDelay loop | Recurring scheduling |
| Approval gate | NATS KV signal + timeout (~30 lines) | Human-in-the-loop |
| Sub-workflow | `deepnoodle-ai/workflow` | Light DAG with child workflows |
| FSM | `looplab/fsm` + NATS KV | Simple state machine |
