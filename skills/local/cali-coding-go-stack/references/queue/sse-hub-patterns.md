# SSE Hub — Live streaming from goqite workers to HTTP handlers

The SSE Hub bridges background workers (goqite goroutines) to live HTTP SSE
connections. Workers push events to the hub; HTTP handlers consume them and
patch the DOM via Datastar.

## Architecture

```
goqite worker (goroutine)
  │ chunk/complete/error events
  ▼
SSE Hub (in-memory PubSub per sessionID)
  │ replay buffer (capped at 500 events)
  ▼
HTTP handler goroutine (polling ch channel)
  │ Datastar SSE patch
  ▼
Browser (Datastar reactive DOM)
```

## Core API

```go
// Get the process-global hub (singleton)
hub := jobs.GetSSEHub()

// Handler: register BEFORE enqueueing
id, ch := hub.Register(sessionID)
defer hub.Unregister(sessionID, id)

// Worker: push events
hub.Send(sessionID, SSEEvent{Type: "chunk", TargetID: "#bubble-123", Content: "hello"})
hub.Send(sessionID, SSEEvent{Type: "complete", FullResponse: "...", ...})
hub.Send(sessionID, SSEEvent{Type: "error", ErrMsg: "..."})
```

## Canonical Consumer Loop

```go
handlerID, ch := hub.Register(sessionID)
defer hub.Unregister(sessionID, handlerID)

for {
    select {
    case evt := <-ch:
        switch evt.Type {
        case "chunk":
            patchDOM(evt.TargetID, evt.Content)
        case "complete":
            handleComplete(evt.FullResponse)
            return
        case "error":
            handleError(evt.ErrMsg)
            return
        case "retry-status":
            showRetryIndicator(evt.Attempt, evt.MaxTries)
        }
    case <-ctx.Done():
        return // timeout or shutdown
    }
}
```

## Race Condition: Register After Enqueue

```go
// ❌ WRONG — worker may send events before handler is listening
jobs.Enqueue(ctx, payload)
handlerID, ch := hub.Register(sessionID) // too late — events dropped

// ✅ CORRECT — register first, enqueue after
handlerID, ch := hub.Register(sessionID)
defer hub.Unregister(sessionID, handlerID)
jobs.Enqueue(ctx, payload) // worker will find subscriber already registered
```

## Replay Buffer (page refresh resilience)

The SSE Hub keeps a capped replay buffer per session (500 events). When a
handler disconnects (page refresh) and re-registers, buffered events are
replayed into the new channel. This prevents lost events between disconnect
and re-register.

```go
// Send always appends to the replay buffer:
func (h *SSEHub) Send(sessionID string, evt SSEEvent) {
    // ... push to live channels ...
    // Append to replay buffer (capped at 500)
    replay := h.replays[sessionID]
    replay = append(replay, evt)
    if len(replay) > replayBufferSize {
        replay = replay[len(replay)-replayBufferSize:]
    }
    h.replays[sessionID] = replay
}
```

**Clear replay on new job enqueue** to prevent stale events from a previous
workflow run being replayed:

```go
hub.ClearSessionReplay(sessionID)
```

## Backpressure (channel full)

Each subscriber channel has capacity 512. If the consumer is slow (e.g.
browser throttles SSE, handler busy), `Send` drains oldest events to half
capacity and retries:

```go
// Simplified from ssehub.go:
for _, ch := range h.subs[sessionID] {
    select {
    case ch <- evt:
    default:
        // Channel full: drain oldest half, then retry
        for len(ch) > channelCapacity/2 {
            <-ch
        }
        select {
        case ch <- evt:
        default:
            // Still full — drop event entirely
        }
    }
}
```

## Design Considerations

| Property | Value |
|----------|-------|
| Channel capacity | 512 events per subscriber |
| Replay buffer | 500 events per session (capped, FIFO drop) |
| Send blocking | Never (non-blocking, drops if full) |
| Subscriber isolation | One channel per (sessionID, handlerID) |
| Cleanup | `Unregister` closes channel. Remaining events garbage-collected. |
| Global state | Yes — process-level singleton. OK for single-binary apps. |
| Multi-process | Not supported. For multi-instance, use NATS PubSub or Redis. |

## Reference Implementation

See `features/narrative-therapy/jobs/ssehub.go` in
`treinador-praticas-narrativas-go-new` for the canonical implementation.
