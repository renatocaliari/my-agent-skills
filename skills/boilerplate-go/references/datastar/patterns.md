# Datastar Patterns

Advanced Datastar v1.0.0 patterns for reactive hypermedia.

> ⚠️ **IMPORTANT:** Use Datastar v1.0.0 from CDN or the included file.

## Signals

Signals are reactive state in the frontend. Define on the parent element:

```html
<div
    id="my-component"
    data-signals={ templ.JSONString(MySignals{Value: "initial"}) }
>
    <!-- Children inherit signals -->
</div>
```

### Go -> Frontend (struct)

```go
type MySignals struct {
    Count    int      `json:"count"`
    Name     string   `json:"name"`
    IsActive bool     `json:"isActive"`
    Items    []string `json:"items"`
}

templ MyComponent() {
    <div
        data-signals={ templ.JSONString(MySignals{
            Count: 0,
            Name:  "Hello",
        }) }
    >
        <span data-text="$count"></span>
    </div>
}
```

### Backend -> Frontend (patch)

```go
sse := datastar.NewSSE(w, r)

// Patch specific element
sse.PatchElementTempl(MyComponent(), datastar.WithModeAppend(), datastar.WithSelector("#target"))

// Update signals directly
store := gabs.New()
store.Set(42, "count")
store.Set("updated", "name")
sse.MarshalAndPatchSignals(store)
```

## Event Handlers

### Click

```html
<button
    data-on:click={ datastar.GetSSE("/api/data") }
>
    Fetch
</button>

<!-- With parameters -->
<button
    data-on:click={ datastar.PostSSE("/api/item/%d/toggle", itemID) }
>
    Toggle
</button>
```

### Keydown

```html
<input
    class="input"
    data-bind:inputValue
    data-on:keydown={`
        if (evt.key !== 'Enter' || !$inputValue.trim().length) return;
        ${datastar.PutSSE("/api/search")}
        $inputValue = '';
    `}
/>
```

### Click Outside

```html
<!-- Close dropdown when clicking outside -->
<div
    id="dropdown"
    data-on:click__outside={ datastar.PutSSE("/ui/dropdown/close") }
>
    <button class="btn">Open</button>
</div>
```

## Loading Indicators (data-indicator)

Shows loading state while request is pending.

### Button with indicator

```html
<button
    class="btn btn-primary"
    data-on:click={ datastar.PostSSE("/api/action") }
    data-indicator="myIndicator"
>
    Submit
</button>

<!-- Visual indicator (spinner) -->
@common.SseIndicator("myIndicator")
```

### Input disabled during loading

```html
<input
    class="input"
    data-bind:inputValue
    data-attr-disabled="$isLoading"
    data-indicator="searchIndicator"
/>

<span data-text="$isLoading ? 'Searching...' : 'Ready'"></span>
```

### Indicator CSS

```css
[data-indicator] {
    position: relative;
}

[data-indicator-fetching] {
    opacity: 0.6;
    pointer-events: none;
}

[data-indicator-fetching]::after {
    content: '';
    position: absolute;
    /* spinner styles */
}
```

### Manual boolean signals (alternative)

Many projects use manual boolean signals instead of `data-indicator`:

```html
<button data-show="!$isSaving" data-on:click="$isSaving = true; @post('/api/action')">
  Save
</button>
<button data-show="$isSaving" disabled>
  <span class="loading loading-spinner"></span> Saving...
</button>
```

```go
// Backend: reset after operation
sse.MarshalAndPatchSignals(map[string]interface{}{"isSaving": false})
```

Both approaches work. Manual signals give more explicit control; `data-indicator` is more concise.

## Reactive Attributes (data-attr-*)

### Dynamic disabled

```html
<button
    class="btn"
    data-on:click={ datastar.PostSSE("/api/submit") }
    data-indicator="submitting"
    data-attr-disabled="$isSubmitting"
>
    Submit
</button>
```

### Dynamic class

```html
<div
    class={ "p-4", templ.KV("bg-primary", isActive) }
    data-on:click={ datastar.PutSSE("/api/toggle") }
>
    Click
</div>
```

### Dynamic style

```html
<div
    data-style:width={ fmt.Sprintf("%dpx", width) }
    data-style:background-color={ color }
>
    Content
</div>
```

## SSE (Server-Sent Events)

### Backend Go

```go
sse := datastar.NewSSE(w, r)

// PATCH - update HTML fragment
sse.PatchElementTempl(Component(), datastar.WithModeAppend(), datastar.WithSelector("#target"))

// SIGNALS - update JS state
update := gabs.New()
update.Set(42, "count")
sse.MarshalAndPatchSignals(update)

// EXECUTE - execute JS script
sse.ExecuteScript("alert('Done!')")
```

### Patching with Raw HTML Strings

For projects not using Templ, use `PatchElements` with raw HTML strings:

```go
sse := datastar.NewSSE(w, r)

// Patch raw HTML to element
sse.PatchElements(htmlString,
    datastar.WithSelectorID("chat-container"),
    datastar.WithModeAppend())

// Patch signals from map
sse.MarshalAndPatchSignals(map[string]interface{}{
    "contextBlocks": settings.ContextBlocks,
})
```

>`PatchElementTempl` uses Templ components; `PatchElements` uses raw HTML strings.

### Patch Modes

| Mode | Description |
|------|-------------|
| `Append` | Adds after element |
| `Prepend` | Adds before element |
| `Outer` | Replaces element |
| `Inner` | Replaces inner content |
| `Delete` | Removes element |
| `Morph` | Idiomorph (merge DOM) |

### Frontend: listening to SSE events

```javascript
// Connect to SSE endpoint
const sse = new EventSource('/api/stream');

sse.addEventListener('datastar', (event) => {
    const data = JSON.parse(event.data);
    // process patches, signals, etc
});

// Specific patches
sse.addEventListener('datastar-patch', (event) => {
    const patch = JSON.parse(event.data);
    applyPatch(patch);
});
```

## Forms with Datastar

### Input binding

```html
<form
    data-signals={ templ.JSONString(FormSignals{Email: ""}) }
    data-on:submit={ datastar.PostSSE("/api/register") }
>
    <input
        type="email"
        class="input input-bordered"
        placeholder="email@example.com"
        data-bind:email
    />
    <button type="submit" class="btn btn-primary">
        Register
    </button>
</form>
```

### Client-side validation

```go
type FormSignals struct {
    Email    string `json:"email"`
    Error    string `json:"error"`
    IsValid  bool   `json:"isValid"`
}

templ Form() {
    <form
        data-signals={ templ.JSONString(FormSignals{}) }
        data-on:submit={`
            if (!/$email/.test($email)) {
                $error = 'Invalid email';
                return;
            }
            ${datastar.PostSSE("/api/register")}
        `}
    >
        <input
            class="input input-bordered"
            class={ templ.KV("input-error", error !== "") }
            data-bind:email
            data-on:input={`$error = ''`}
        />
        if error != "" {
            <span class="text-error text-sm">{ error }</span>
        }
    </form>
}
```

## Best Practices

### Request cancellation for pages

```html
<div
    data-init={ datastar.GetSSE("/api/list", {requestCancellation: 'disabled'}) }
>
    <!-- does not cancel when navigating to another page -->
</div>
```

### try/catch on media operations

```javascript
async function enableMic() {
    try {
        await room.localParticipant.setMicrophoneEnabled(true);
    } catch (e) {
        console.warn('Mic access denied:', e);
    }
}
```

### View Transitions for smooth navigation

```css
@view-transition {
    navigation: auto;
}
```

---

## Complete Form Patterns (v1.0.0 Verified)

### Full Form with Validation and Loading State

```go
// Go handler
type SettingsSignals struct {
    Model         string `json:"model"`
    RefinePrompt  string `json:"refinePrompt"`
    CurrentTab    string `json:"currentTab"`
    IsSaving      bool   `json:"isSaving"`
    ShowSaveToast bool   `json:"showSaveToast"`
}

func (ns *NarrativeService) saveSettings(sse *datastar.ServerSentEventGenerator, signals map[string]interface{}) {
    // ... save to database ...

    // IMPORTANT: Reset loading signal!
    sse.MarshalAndPatchSignals(map[string]interface{}{
        "isSaving":      false,
        "showSaveToast": true,
    })
}
```

```html
<!-- HTML Template -->
<div data-signals={ templ.JSONString(SettingsSignals{
    Model:        "gpt-4",
    CurrentTab:   "refine",
    IsSaving:     false,
}) }>

    <!-- Tabs -->
    <div class="tabs">
        <button data-on:click="$currentTab = 'refine'">Refinar</button>
        <button data-on:click="$currentTab = 'generate'">Gerar</button>
    </div>

    <!-- Tab Content -->
    <div data-show="$currentTab === 'refine'">
        <input type="text" name="model" data-bind="model">
        <textarea name="refinePrompt" data-bind="refinePrompt"></textarea>
    </div>

    <div data-show="$currentTab === 'generate'">
        <!-- generate content -->
    </div>

    <!-- Save Button with Loading State -->
    <button
        data-show="!$isSaving"
        data-on:click="$isSaving = true; @post('/api/ui/action?action=save_settings')"
    >
        Salvar
    </button>

    <button data-show="$isSaving" disabled>
        <span class="loading loading-spinner"></span>
        Salvando...
    </button>
</div>
```

**Prevent FOUC (Flash of Unstyled Content):** For elements that start hidden, add `style="display: none"` as initial state:
```html
<div data-show="$currentTab === 'details'" style="display: none">
  <!-- Content hidden until Datastar initializes -->
</div>
```
This prevents FOUC by hiding the element before Datastar processes the DOM.

### Centralized Action Dispatch

A common pattern routes all UI actions through a single endpoint with a query parameter:

```html
<button data-on:click="@post('/api/ui/action?action=save_settings')">Save</button>
<button data-on:click="@post('/api/ui/action?action=delete_item&id=' + $itemId)">Delete</button>
```

```go
func handler(w http.ResponseWriter, r *http.Request) {
    sse := datastar.NewSSE(w, r)
    body, _ := io.ReadAll(r.Body)
    signals := map[string]interface{}{}
    json.Unmarshal(body, &signals)

    switch r.URL.Query().Get("action") {
    case "save_settings":
        // ...
    case "delete_item":
        // ...
    }
}
```

### Form Submit with Loading Signal

Set a loading signal before the `@post()` call — the JS executes left-to-right, so `$isSaving` is set before the fetch starts:

```html
<form data-on:submit="$isSaving = true; @post('/api/ui/action?action=send_message')">
  <button type="submit" data-show="!$isSaving">Send</button>
  <button type="submit" data-show="$isSaving" disabled>
    <span class="loading loading-spinner"></span> Sending...
  </button>
</form>
```

```go
// Backend: reset after completion
sse.MarshalAndPatchSignals(map[string]interface{}{"isSaving": false})
```

### JSON Escape Helper (REQUIRED for complex content)

```go
import "encoding/json"

// For content with newlines, quotes, special characters:
func escapeForJS(s string) string {
    b, _ := json.Marshal(s)
    return string(b)
}

// Usage in template:
// <div data-signals={ escapeForJS(complexContent) }>
```

**Never use strings.ReplaceAll for JSON escaping** - it breaks with nested quotes and special characters.

> **⚠️ Exception: Single-quoted HTML attributes.** When `data-signals` uses single-quoted JSON (`data-signals='{"key": %s}'`), single quotes inside values break the attribute boundary. In this case, replace `'` with `&#39;`:
> ```go
> func escJSON(b []byte) []byte {
>     s := string(b)
>     s = strings.ReplaceAll(s, "'", "&#39;")
>     return []byte(s)
> }
> ```
> This is the **only** safe use of `strings.ReplaceAll` for JSON escaping.

### Two-Way Data Binding

```html
<!-- Input binding - always include name attribute! -->
<input
    type="text"
    name="username"
    data-bind="username"
    class="input input-bordered"
/>

<!-- Textarea binding -->
<textarea
    name="content"
    data-bind="content"
    class="textarea textarea-bordered"
></textarea>
```

**Critical:** The `name` attribute is required for POST data to be sent correctly.

### Form Submission with contentType: 'form'

**Frontend - Use `{contentType: 'form'}` to send form-encoded data (NOT signals):**

```html
<form data-on:submit={`@post('/api/action', {contentType: 'form'})`}>
    <input name="username" data-bind="username">
    <input name="email" type="email" data-bind="email">
    <textarea name="message"></textarea>
    <button type="submit">Send</button>
</form>
```

**Backend - Parse form data:**
```go
func handleFormSubmit(sse *datastar.ServerSentEventGenerator, w http.ResponseWriter, r *http.Request) {
    // IMPORTANT: ParseForm() is required when using contentType: 'form'
    if err := r.ParseForm(); err != nil {
        sse.MarshalAndPatchSignals(map[string]interface{}{
            "error": "Failed to parse form",
        })
        return
    }

    username := r.FormValue("username")
    email := r.FormValue("email")
    message := r.FormValue("message")

    // Process...

    sse.MarshalAndPatchSignals(map[string]interface{}{
        "isSaving": false,
        "success":  true,
    })
}
```

**Key Points:**
- `{contentType: 'form'}` sends `application/x-www-form-urlencoded` (NOT JSON signals)
- `r.ParseForm()` must be called to read form values
- Use `r.FormValue("fieldname")` to get values
- **Large text content works naturally (no escaping issues!)**

### When to Use `{contentType: 'form'}` vs Signals

| Use Case | Recommended Approach | Reason |
|----------|---------------------|--------|
| Small forms (login, search) | JSON signals | Simple, reactive |
| **Large text (prompts, descriptions)** | **`{contentType: 'form'}`** | **Avoids JSON escaping issues** |
| File uploads | `{contentType: 'form'}` | Multipart encoding |
| Complex nested objects | JSON signals | Structured data |

**Rule of thumb:** If your text content has newlines, quotes, or special characters → use `{contentType: 'form'}`.

### Form Button Placement (CRITICAL)

When using `{contentType: 'form'}`, button placement and types are crucial:

**✓ CORRECT: Submit button inside form**
```html
<form data-on:submit="@post('/api/save', {contentType: 'form'})">
    <textarea name="content"></textarea>
    <button type="submit">Save</button>
</form>
```

**✓ CORRECT: Other buttons with `type="button"`**
Use `type="button"` for buttons inside the form that should NOT submit:
```html
<form data-on:submit="@post('/api/save', {contentType: 'form'})">
    <textarea name="content"></textarea>
    <button type="button" data-on:click="@post('/api/other')">
        Other Action
    </button>
    <button type="submit">Save</button>
</form>
```

**✗ WRONG: Submit button outside form**
```html
<form data-on:submit="@post('/api/save', {contentType: 'form'})">
    <textarea name="content"></textarea>
</form>
<button data-on:click="@post('/api/save', {contentType: 'form'})">
    Save  <!-- ERROR: FetchFormNotFound -->
</button>
```

**Common Error:** `FetchFormNotFound` occurs when:
- The button using `{contentType: 'form'}` is not inside a `<form>` element
- The button is inside the form but lacks `type="submit"`

**Solution:** Always place submit buttons INSIDE the form with `type="submit"` and use `data-on:submit` on the form element.

---

## Anti-Patterns to Avoid

### ❌ DON'T: Use Signals for Large Text Content

**Problem:** Using signals to store and update large text content (like prompts, descriptions, or multi-line text) causes issues:
- Complex escaping required for newlines, quotes, and special characters
- JavaScript parser errors with unescaped content
- Fragile code that breaks with edge cases

**Wrong approach (AVOID):**
```html
<!-- DON'T DO THIS - Sets large text via signal in data-on:click -->
<button data-on:click="$prompt = 'Very long text with \n newlines and \"quotes\"...'">
    Restore Default
</button>
<textarea data-bind="prompt"></textarea>
```

### ✅ DO: Use PatchElements for Large Text

**Solution:** Use `PatchElements` via SSE to update the textarea directly, then sync the signal.

**Right approach (RECOMMENDED):**

```html
<!-- Button triggers SSE request -->
<button data-on:click="@post('/api/ui/action?action=restore_prompt&type=refine')">
    Restore Default
</button>
<textarea id="refinePrompt" name="refinePrompt" data-bind="refinePrompt"></textarea>
```

```go
// Backend handler
func (ns *NarrativeService) restoreDefaultPrompt(sse *datastar.ServerSentEventGenerator, promptType string) {
    defaultPrompt := db.DefaultPrompts.RefineDescription
    
    // 1. Patch the textarea directly via SSE (no escaping needed!)
    textareaHTML := fmt.Sprintf(`<textarea id="refinePrompt" name="refinePrompt" data-bind="refinePrompt">%s</textarea>`, 
        defaultPrompt)
    sse.PatchElements(textareaHTML, datastar.WithSelectorID("refinePrompt"), datastar.WithModeOuter())
    
    // 2. Also update the signal so form submission works correctly
    sse.MarshalAndPatchSignals(map[string]string{
        "refinePrompt": defaultPrompt,
    })
}
```

**Benefits:**
- ✅ No complex escaping required
- ✅ Newlines and special characters work naturally
- ✅ More robust and maintainable
- ✅ Follows Datastar's hypermedia principles

**Rule of thumb:**
- Use **signals** for: small state values (booleans, IDs, counters, short strings)
- Use **PatchElements** for: large text content, HTML fragments, complex data

**Signal Philosophy:**
> ⚠️ **Overusing signals typically indicates trying to manage state on the frontend.**

Datastar works best when:
- Backend is the **source of truth**
- Signals are **ephemeral** (short-lived, user interaction focused)
- State is **fetched when needed**, not pre-loaded

Don't:
- Pre-load entire objects into signals
- Use signals as a client-side database
- Store fetched data in signals for later use

---

## Backend Patterns

### Go SSE Handler Template

```go
func handleAction(w http.ResponseWriter, r *http.Request) {
    sse := datastar.NewSSE(w, r)

    // Parse form if needed
    if err := r.ParseForm(); err != nil {
        sse.MarshalAndPatchSignals(map[string]interface{}{
            "error": "Failed to parse form",
        })
        return
    }

    model := r.FormValue("model")
    prompt := r.FormValue("refinePrompt")

    // Process...

    // IMPORTANT: Always reset loading states
    sse.MarshalAndPatchSignals(map[string]interface{}{
        "isSaving": false,
        "success":  true,
    })
}
```

### Store vs PatchSignals

```go
// For simple signal updates, use Map:
sse.MarshalAndPatchSignals(map[string]bool{"isSaving": false})

// For nested data, use store:
// store := gabs.New()
// store.Set(true, "user", "isActive")
// sse.MarshalAndPatchSignals(store)
```
