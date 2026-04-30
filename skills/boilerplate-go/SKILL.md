---
name: boilerplate-go
description: >
  Scaffolds Go web applications with Datastar, Templ, DaisyUI, TailwindCSS, NATS, and optional features
  (Fabric.js whiteboard, LiveKit+Gemini voice AI, PocketBase/SQLite database).
  Use when starting a new Go web project, creating real-time features, building hypermedia-driven apps,
  or scaffolding Go backend with SSE support. Triggers for "new go project", "scaffold go app",
  "go web boilerplate", "datastar go", "templ project", "go realtime app", "hypermedia go", "go sse server",
  "tailwind daisyui", "go ui components", or when user wants Go backend with reactive frontend.
  Also triggers for AI/LLM integration needs when involving voice: "voice AI", "voice bot", "livekit gemini",
  "real-time voice", "audio AI". For text-only AI use the goai skill instead.
---

# Go Web Application Boilerplate (v1.0.0 Ready)

Go boilerplate inspired by [Northstar](https://github.com/delaneyj/toolbelt), featuring:

> ⚠️ **Datastar v1.0.0 Required** - This boilerplate uses Datastar v1.0.0 (not RC.8). See [Installation](#datastar-v100-installation) below.
- **[Datastar](https://data-star.dev)** - Reactive hypermedia via SSE
- **[Templ](https://templ.guide)** - Go components that generate HTML
- **[DaisyUI + TailwindCSS](https://daisyui.com)** - UI components and styling
- **[NATS](https://nats.io)** - Real-time messaging (optional: JetStream for persistence)
- **[Fabric.js](http://fabricjs.com)** - Collaborative whiteboard (optional)
- **[LiveKit + Gemini](https://livekit.io)** - Voice AI (optional)
- **[PocketBase](https://pocketbase.io)** - Advanced database (optional)
- **[SQLite](https://sqlite.org)** - Simple database (optional)

## When to Activate This Skill

Activate this skill when the user wants:

| Intent | Example Prompt |
|--------|----------------|
| Create Go web project from scratch | "create a new go web app" |
| Add real-time/SSE | "add real-time updates to my Go app" |
| UI with ready-made components | "add a dashboard with Tailwind components" |
| Hypermedia-driven app | "build like Datastar/HTMX style app in Go" |
| Voice AI with LiveKit | "add a voice assistant to my app" |
| Collaborative whiteboard | "add a collaborative whiteboard" |
| Database | "add persistence with SQLite/PocketBase" |

---

## Quick Start

### 1. Ask the User: Which Features Are Needed?

Not every project needs everything. Use this decision tree:

```
Go Web Project
├── Need UI?
│   ├── YES → DaisyUI (always included by default)
│   └── NO → Skip to "Need data?"
│
├── Need real-time?
│   ├── Simple Pub/Sub (NATS Core) → fire-and-forget messaging
│   ├── With persistence/history (JetStream) → streams + replay
│   └── Reactive frontend only (Datastar SSE) → no NATS needed
│
├── Need database?
│   ├── Simple (1 instance, local) → SQLite
│   ├── Advanced (multi-instance, auth, REST, realtime) → PocketBase
│   └── None → in-memory data or NATS KV
│
├── Need voice AI?
│   ├── YES → LiveKit + Gemini Live API
│   └── NO → Skip
│
├── Need whiteboard?
│   ├── YES → Fabric.js
│   └── NO → Skip
```

### 2. Decision Checklist

Before starting, confirm with the user:

```markdown
## Project Configuration

- [ ] **UI**: DaisyUI + TailwindCSS (default, always recommended)
- [ ] **Real-time messaging**: NATS Core / JetStream / None
- [ ] **Database**: SQLite / PocketBase / None
- [ ] **Voice AI**: LiveKit + Gemini / None
- [ ] **Whiteboard**: Fabric.js / None
- [ ] **Module name**: `github.com/user/projectname`
```

### 3. Generated Structure

```
project/
├── cmd/web/main.go           # Entry point
├── config/
│   ├── config.go             # Configuration
│   ├── config_dev.go         # Dev config
│   └── config_prod.go        # Prod config
├── router/router.go          # Main router
├── nats/nats.go              # NATS setup
├── features/                 # Self-contained features
│   ├── common/
│   │   ├── layouts/base.templ
│   │   └── components/
│   ├── index/                # Home page
│   ├── todos/                # CRUD example (NATS KV)
│   ├── counter/              # Global vs user state
│   ├── monitor/              # System info
│   ├── sortable/             # Lit + SortableJS
│   ├── reverse/              # Streaming demo
│   ├── whiteboard/           # [OPTIONAL] Fabric.js
│   └── voice-training/       # [OPTIONAL] LiveKit + Gemini
├── web/
│   └── resources/
│       └── styles/
│           └── styles.css    # DaisyUI + Tailwind
├── go.mod
└── Taskfile.yml
```

---

## Feature Modules (Self-Contained)

Each feature in `features/<name>/` is 100% self-contained:
- Its own routes, handlers, services
- Its own static assets (via `go:embed`)
- Its own templates and components

### How to Add/Remove Features

```bash
# To add: copy the feature directory to the project
cp -r boilerplate-go/assets/scaffold/features/whiteboard myproject/features/

# To remove: delete the directory
rm -rf myproject/features/whiteboard
```

### Pattern: Embedded Assets (go:embed)

```go
// features/whiteboard/static.go
package whiteboard

import (
    "embed"
    "io/fs"
    "net/http"
)

//go:embed static/*
var staticEmbed embed.FS

func StaticFS() http.FileSystem {
    fsys, _ := fs.Sub(staticEmbed, "static")
    return http.FS(fsys)
}
```

---

## Detailed Architectural Decisions

### UI: DaisyUI (Always Recommended)

DaisyUI is ready-made TailwindCSS components. **Always recommended** for Go web projects because:
- 0 custom JavaScript for basic UI
- Consistent themes (automatic light/dark)
- Accessible components by default
- Customizable via Tailwind config

**When NOT to use DaisyUI:**
- Project needs 100% custom design (UI as differentiator)
- Team already has their own design system

### Real-time: NATS Core vs JetStream

| Need | Solution |
|------|----------|
| Simple broadcast (1→N) | NATS Core |
| Messages with history | JetStream |
| Work queues | JetStream Consumer |
| Simple Key-Value | JetStream KV |
| High performance, low latency | NATS Core |

### Database: SQLite vs PocketBase

| Criteria | SQLite | PocketBase |
|----------|--------|------------|
| Multiple instances | ❌ | ✅ |
| Built-in auth | ❌ | ✅ |
| Automatic REST API | ❌ | ✅ |
| Realtime subscriptions | ❌ | ✅ |
| Migrations | Manual | Automatic |
| Simplicity | ✅ | ✅ |
| Local data only | ✅ | ❌ |

### Voice AI: When to Activate

**Activate LiveKit + Gemini when:**
- Voice assistant/chatbot that speaks
- Real-time transcription - meetings, calls
- Visual assistants - screen sharing + voice
- Automated IVR/NPS - phone support
- Remote education - tutoring with voice

**Do NOT activate (use goai SDK instead):**
- Text/chat generation
- Embeddings
- Image analysis
- Function calling without voice

---

## Datastar v1.0.0 Patterns

> ⚠️ **CRITICAL: This boilerplate uses Datastar v1.0.0. Read this section carefully!**

### Datastar v1.0.0 Installation

#### Option 1: CDN (Recommended for quick setup)
```html
<script type="module" src="https://cdn.jsdelivr.net/gh/starfederation/[email protected]/bundles/datastar.js"></script>
```

#### Option 2: Self-hosted (Included in boilerplate)
The boilerplate includes datastar.js at `web/resources/static/datastar/datastar.js`.
```html
<script defer type="module" src="/static/datastar/datastar.js"></script>
```

#### Option 3: npm/deno/bun
```javascript
import 'https://cdn.jsdelivr.net/gh/starfederation/[email protected]/bundles/datastar.js'
```

### HTML Template Setup
Your HTML template must include the Datastar script:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <script defer type="module" src="/static/datastar/datastar.js"></script>
</head>
<body>
    { children... }
</body>
</html>
```

### Core Attributes

| Attribute | Example | Purpose |
|-----------|---------|---------|
| `data-on:click` | `data-on:click="@post('/api/action')"` | Click handler |
| `data-init` | `data-init="$count = 1"` | Optional: executes expression on element init |
| `data-signals` | `data-signals="{count: 0}"` | Reactive state |
| `data-bind` | `data-bind="model"` | Two-way binding |
| `data-text` | `data-text="$count"` | Text content |
| `data-class` | `data-class="{'text-primary': $active}"` | Conditional classes |
| `data-show` | `data-show="$visible"` | Conditional visibility |

### Signal Philosophy (IMPORTANT)

> ⚠️ **Overusing signals typically indicates trying to manage state on the frontend.**

**Favor fetching current state from the backend rather than pre-loading and assuming frontend state is current.**

**Good rule of thumb:**
- ✅ Use signals for **user interactions** (e.g., toggling element visibility, accordion state)
- ✅ Use signals for **sending new state to backend** via form bindings
- ❌ Don't use signals to **store fetched data** (fetch it when needed instead)
- ❌ Don't **pre-load entire objects** into signals and manage frontend state

**Why this matters:**
- Backend is the source of truth, not the frontend
- Signals are ephemeral - they don't persist across page loads
- Pre-loaded state can become stale when data changes elsewhere

### Form Submissions

**Standard forms (small data):**
```html
<form data-on:submit={`@post('/api/action', {contentType: 'form'})`}>
    <input name="name" data-bind="name">
    <button type="submit">Submit</button>
</form>
```

**Backend handler:**
```go
func handler(w http.ResponseWriter, r *http.Request) {
    sse := datastar.NewSSE(w, r)
    r.ParseForm() // Required for form contentType
    name := r.FormValue("name")
    // ...
}
```

> ⚠️ **Important:** Always use `{contentType: 'form'}` for form submissions to send form-encoded data, not JSON signals.

### What NOT to Use
- ❌ HTMX
- ❌ Alpine.js
- ❌ Vanilla JavaScript to replace Datastar functionality
- ❌ Other reactive frameworks

---

> ⚠️ **Read [references/datastar/patterns.md](references/datastar/patterns.md)** for complete patterns.

### Key Concepts

1. **Signals** - Reactive state in the frontend (JavaScript)
2. **SSE** - Server-Sent Events for push updates
3. **Patches** - HTML fragments updated by the server
4. **Indicators** - Visual loading states

### Example: Counter

```go
// Backend: signals and patches
type CounterSignals struct {
    Global uint32 `json:"global"`
    User   uint32 `json:"user"`
}

templ Counter(signals CounterSignals) {
    <div data-signals={ templ.JSONString(signals) }}>
        <button data-on:click={ datastar.PostSSE("/counter/increment/global") }>
            + Global
        </button>
        <span data-text="$global"></span>
    </div>
}
```

### Example: TodoMVC (NATS KV)

```go
// Backend: CRUD with NATS KV
js.Set("todos", "key", []byte(jsonData))

// Frontend: reactive signals
<div data-signals={ templ.JSONString(TodoSignals{
    Todos: []*Todo{},
    Mode:  "all",
}) }>
    <ul>
        for _, todo := range mvc.Todos {
            @TodoRow(todo)
        }
    </ul>
</div>
```

---

## References (Progressive Disclosure)

| Reference | When to Read | What It Contains |
|-----------|--------------|------------------|
| **[references/README.md](references/README.md)** | First | Index with reading path |
| **[references/datastar/patterns.md](references/datastar/patterns.md)** | When using Datastar | Signals, SSE, events, indicators |
| **[references/daisyui/components.md](references/daisyui/components.md)** | When using UI | Ready-to-copy components |
| **[references/nats/when-to-use-jetstream.md](references/nats/when-to-use-jetstream.md)** | When configuring real-time | NATS vs JetStream vs KV |
| **[references/voice-ai/when-to-use.md](references/voice-ai/when-to-use.md)** | When adding voice AI | LiveKit + Gemini |
| **[references/whiteboard/fabric_patterns.md](references/whiteboard/fabric_patterns.md)** | When using whiteboard | Fabric.js + synchronization |
| **[references/database/README.md](references/database/README.md)** | When adding DB | SQLite vs PocketBase |

---

## Working with Existing Projects

When updating an existing Go project to use Datastar v1, follow this checklist:

### Migration Checklist

1. **Datastar Script Setup**
   - Ensure datastar.js v1.0.0 is in `web/resources/static/datastar/`
   - Add to HTML: `<script defer type="module" src="/static/datastar/datastar.js"></script>`
   - `data-init` is optional (not required) - only use when you need to execute an action on page/component load

2. **Static Files Configuration**
   - Use build tags: `//go:build dev` for dev, `//go:build !dev` for prod
   - In dev: `http.FileServerFS(os.DirFS(StaticDirectoryPath))`
   - In prod: `embed.FS` + `hashfs.FileServer`
   - Test: `curl http://localhost:8080/static/datastar/datastar.js` should return 200

3. **Form Migration**
   - Add `name` attribute to all inputs/textareas
   - Add `data-bind` for two-way sync
   - Replace `data-on:input="$var = el.value"` with `data-bind="varName"`

4. **JSON Escaping**
   - Replace manual escape with `json.Marshal` approach
   - Test with special characters: newlines, quotes, unicode

5. **Visibility Patterns**
   - Replace `class="hidden"` + `data-show` with `data-show` only
   - Test tab switching

### Common Migration Issues

See [Common Pitfalls](#common-pitfalls) section below.

---

## Common Pitfalls

### 1. data-signals JSON Escaping

**❌ Don't:** Manual escaping with strings.ReplaceAll
```go
s = strings.ReplaceAll(s, "\n", "\\n")
s = strings.ReplaceAll(s, "'", "\\'")
```

**✅ Do:** Use json.Marshal
```go
func escapeForJS(s string) string {
    b, _ := json.Marshal(s)
    return string(b)
}
```

**Note:** `json.Marshal` returns the string with quotes included, so use `%s` directly in templates, not `'%s'`.

### 2. Form Data Not Sending

**❌ Don't:** Inputs without name attribute
```html
<input data-bind="model">
```

**✅ Do:** Always include name
```html
<input name="model" data-bind="model">
```

### 3. Textareas Not Syncing

**❌ Don't:** Only data-on:input
```html
<textarea data-on:input="$prompt = el.value">
```

**✅ Do:** Use data-bind
```html
<textarea name="prompt" data-bind="prompt">
```

### 4. Tabs Not Working

**❌ Don't:** Mix class="hidden" with data-show
```html
<div data-show="$tab === 'a'" class="hidden">
```

**✅ Do:** Use only data-show
```html
<div data-show="$tab === 'a'">
```

### 5. Loading State Stuck

**❌ Don't:** Forget to reset signal
```go
// Handler only saves, doesn't reset
repo.Save(data)
```

**✅ Do:** Reset signal after operation
```go
repo.Save(data)
sse.MarshalAndPatchSignals(map[string]bool{"isLoading": false})
```

---

## Troubleshooting

### "Invalid or unexpected token" in console

**Cause:** Malformed data-signals JSON
**Fix:**
1. Check json.Marshal escaping
2. View page source and validate JSON
3. Check for unescaped newlines/quotes

### "POST body empty"

**Cause:** Inputs missing name attribute
**Fix:** Add `name="fieldName"` to all form inputs

### "datastar not defined"

**Cause:** Script not loaded
**Fix:**
1. Check 404 for datastar.js
2. Verify static file serving
3. Check script path

### "Signals not updating"

**Cause:** Typically a data-bind or signal definition issue
**Fix:**
1. Ensure `data-bind` attribute is present on form elements
2. Check signal name matches between definition and usage
3. Verify server returns proper SSE response

### Handler never called

**Cause:** Wrong data-on:click syntax
**Fix:** Use `@post('/api/action')` format with quotes and leading slash

### Form data not received at backend

**Cause:** Missing `{contentType: 'form'}` in action
**Fix:** Use `@post('/api/action', {contentType: 'form'})` and call `r.ParseForm()` in handler

---

## Best Practices

1. **Self-contained features** - Each feature in its own directory
2. **Delta sync** - Send only what changed (not entire objects)
3. **KISS (SSE)** - Prefer SSE over WebSockets for one-way updates
4. **Indicators** - Always show loading states with `data-indicator`
5. **Error boundaries** - try/catch on media and storage operations
6. **View transitions** - Use `@view-transition { navigation: auto; }` for smooth navigation

---

## Inspiration

This boilerplate is inspired by [Northstar](https://github.com/delaneyj/toolbelt) by Delaney Johnson.
