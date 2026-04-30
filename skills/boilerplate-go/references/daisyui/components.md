# DaisyUI Components

Ready-to-copy DaisyUI components. All use Tailwind + DaisyUI classes.

## Buttons

```html
<!-- Primary button -->
<button class="btn btn-primary">Primary</button>

<!-- Button with icon -->
<button class="btn btn-secondary">
  <iconify-icon icon="material-symbols:add"></iconify-icon>
  Add
</button>

<!-- Loading button -->
<button class="btn btn-primary" disabled>
  <span class="loading loading-spinner"></span>
  Loading
</button>

<!-- Button group (join) -->
<div class="join">
  <button class="btn join-item">1</button>
  <button class="btn join-item btn-active">2</button>
  <button class="btn join-item">3</button>
</div>
```

## Inputs

```html
<!-- Basic input -->
<input type="text" class="input input-bordered" placeholder="Type here..."/>

<!-- Input with floating label (daisyui 5) -->
<div class="form-control">
  <label class="label">
    <span class="label-text">Email</span>
  </label>
  <input type="email" class="input input-bordered" placeholder="email@example.com"/>
</div>

<!-- Textarea -->
<textarea class="textarea textarea-bordered" placeholder="Description..."></textarea>

<!-- Select -->
<select class="select select-bordered">
  <option disabled selected>Select...</option>
  <option>Option 1</option>
  <option>Option 2</option>
</select>

<!-- Checkbox -->
<label class="cursor-pointer label">
  <input type="checkbox" class="checkbox checkbox-primary"/>
  <span class="label-text">Remember me</span>
</label>

<!-- Radio -->
<div class="form-control">
  <label class="cursor-pointer label">
    <input type="radio" name="opt" class="radio radio-secondary"/>
    <span class="label-text">Option A</span>
  </label>
  <label class="cursor-pointer label">
    <input type="radio" name="opt" class="radio radio-secondary"/>
    <span class="label-text">Option B</span>
  </label>
</div>
```

## Cards

```html
<div class="card card-compact bg-base-100 shadow-xl">
  <figure>
    <img src="/img.jpg" alt="Image"/>
  </figure>
  <div class="card-body">
    <h2 class="card-title">Card Title</h2>
    <p>Content description.</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Action</button>
    </div>
  </div>
</div>

<!-- Simple card (stats) -->
<div class="stats shadow">
  <div class="stat">
    <div class="stat-title">Total</div>
    <div class="stat-value text-primary">$50K</div>
    <div class="stat-desc">↗︎ 12% more than last month</div>
  </div>
</div>
```

## Alerts

```html
<div class="alert alert-info">
  <iconify-icon icon="material-symbols:info"></iconify-icon>
  <span>Informative message</span>
</div>

<div class="alert alert-success">
  <iconify-icon icon="material-symbols:check-circle"></iconify-icon>
  <span>Operation completed successfully!</span>
</div>

<div class="alert alert-warning">
  <iconify-icon icon="material-symbols:warning"></iconify-icon>
  <span>Warning: check the data</span>
</div>

<div class="alert alert-error">
  <iconify-icon icon="material-symbols:error"></iconify-icon>
  <span>Something went wrong!</span>
</div>
```

## Badges

```html
<span class="badge badge-primary">Primary</span>
<span class="badge badge-secondary">Secondary</span>
<span class="badge badge-outline badge-accent">Outline</span>

<!-- Badge as indicator -->
<div class="badge badge-lg badge-error gap-2">
  <span class="loading loading-spinner loading-xs"></span>
  Processing...
</div>
```

## Tooltips

```html
<!-- Simple tooltip -->
<div class="tooltip" data-tip="Tooltip text">
  <button class="btn">Hover me</button>
</div>

<!-- Tooltip in different positions -->
<div class="tooltip tooltip-top" data-tip="Top">
  <button class="btn">Top</button>
</div>
<div class="tooltip tooltip-bottom" data-tip="Bottom">
  <button class="btn">Bottom</button>
</div>
```

## Modal

```html
<!-- Open modal -->
<button class="btn" onclick="modal_id.showModal()">Open</button>

<!-- Dialog (modal) -->
<dialog id="modal_id" class="modal">
  <div class="modal-box">
    <h3 class="font-bold text-lg">Title</h3>
    <p class="py-4">Modal content</p>
    <div class="modal-action">
      <form method="dialog">
        <button class="btn">Close</button>
      </form>
    </div>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
```

### Modal with Datastar

> ⚠️ **Do NOT use `data-show`** on `<dialog>` elements — it only toggles `display: none`, which doesn't work with DaisyUI modals. DaisyUI requires the `modal-open` CSS class.

**✅ CORRECT: Use `data-class` with `modal-open`**
```html
<dialog class="modal" data-class="{'modal-open': $showDialog}">
  <div class="modal-box">
    <h3 class="font-bold text-lg">Title</h3>
    <div class="modal-action">
      <button data-on:click="$showDialog = false">Close</button>
    </div>
  </div>
</dialog>

<button class="btn btn-primary" data-on:click="$showDialog = true">Open Modal</button>
```

**❌ WRONG: `data-show` on dialog**
```html
<dialog class="modal" data-show="$showDialog">
  <!-- Modal won't display properly -->
</dialog>
```

## Table

```html
<div class="overflow-x-auto">
  <table class="table">
    <thead>
      <tr>
        <th></th>
        <th>Name</th>
        <th>Job</th>
        <th>Favorite Color</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th>1</th>
        <td>Cy Ganderton</td>
        <td>Quality Control Specialist</td>
        <td>Blue</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- Zebra table -->
<table class="table table-zebra">
```

## Navbar

```html
<div class="navbar bg-base-100 shadow-sm">
  <div class="flex-1">
    <a class="btn btn-ghost text-xl">daisyUI</a>
  </div>
  <div class="flex-none">
    <button class="btn btn-square btn-ghost">
      <iconify-icon icon="material-symbols:search"></iconify-icon>
    </button>
  </div>
</div>
```

## Themes

The project uses DaisyUI themes configured in `styles.css`:

```css
@plugin "daisyui" {
  themes: cupcake --default, dark --prefersdark;
}
```

To use a specific theme:
```html
<div data-theme="dark">
  <!-- Content with dark theme -->
</div>
```

To switch themes dynamically with Datastar:
```html
<select class="select" data-theme="light">
  <option value="light">Light</option>
  <option value="dark">Dark</option>
  <option value="cupcake">Cupcake</option>
</select>
```
