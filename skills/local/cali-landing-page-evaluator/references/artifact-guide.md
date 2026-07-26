# Three-tab HTML artifact guide

The deliverable for this skill is always a single self-contained HTML file
with **three tabs**: Questions, Evaluation, Wireframe. This file is
regenerated (overwritten) every time the user answers open questions or
provides new context, so it always reflects the current state of the
conversation.

## Why three tabs, not three files
Keeping all three views in one file makes the state easy to re-share and
re-open after every iteration, and makes the relationship between an open
question and the part of the wireframe it blocks visually obvious (a
question and the placeholder it unblocks share an id/reference).

## Technical rules
- Single HTML file, CSS and JS embedded, no external dependencies, no CSS
  framework.
- Plain tab UI: three buttons/tabs at the top ("Questions", "Evaluation",
  "Wireframe"), one visible panel at a time, vanilla JS `onclick` toggling
  `display`/a `.active` class. No routing, no build step.
- Mobile-first: central container `max-width` around 720-900px, readable
  base font size (16-18px), line-height 1.5-1.6, system font stack
  (`system-ui, -apple-system, sans-serif`).
- Badge/counter on the "Questions" tab button showing how many open
  questions remain (e.g. "Questions (3)"), so the state is visible without
  clicking in.

## Tab 1 — Questions
- One list, ordered with structure-changing questions first (the ones that
  would change the category or the whole framework) and cosmetic/detail
  questions last.
- Each question shows: the question itself, phrased so the user can answer
  it directly in the chat reply, and a one-line note on *why* it matters
  (what gap or contradiction triggered it).
- Once a question is answered in conversation, remove it from this tab in
  the next regeneration (don't just cross it out — the tab should always
  reflect only what's still open).

## Tab 2 — Evaluation
- Assessment of everything submitted so far: framework fit (does the
  structure match the category's base framework), the anti-AI-tone
  checklist results, and category-specific pitfalls (see frameworks.md).
- If evaluating existing copy: strengths first (quoted briefly), then the
  3-5 highest-impact issues, each with the original snippet, why it's an
  issue (tied to a named principle), and a suggested rewrite.
- If building from a brief/description rather than existing copy: state
  clearly what's solid (confirmed by the user) vs. what's still an
  assumption pending an answer in the Questions tab.
- Never silently resolve a gap here — if something is unconfirmed, say so
  explicitly rather than treating an assumption as a fact.

## Tab 3 — Wireframe
- Reflects **only** what has been confirmed or explicitly provided by the
  user. This is a hard rule: no invented copy, no invented proof, no
  invented sections to "fill out" the funnel.
- Each section of the chosen framework (see frameworks.md) that has enough
  confirmed content renders as a normal wireframe block: `<section>` with
  an HTML comment naming the section and its role in the framework (e.g.
  `<!-- Problem — PAS: Problem -->`), containing the real copy.
- Each section that depends on an unanswered question renders as a
  visibly different placeholder block (dashed border, muted background,
  a label like "⏳ Pending — needs an answer to Q2") instead of invented
  content. Never fabricate a testimonial, statistic, or client name to
  fill a gap — mark it pending instead.
- Buttons/CTAs use the real decided copy, not "CTA button here." No real
  `<form>` submit; `<button>` or `<a href="#">` with no action is fine.
- Neutral gray placeholders for images (`background: #e5e5e5`, centered
  text like "[image: product screenshot]") — never generate fake images.

## File location
Save to `/mnt/user-data/outputs/<slug>-landing-page.html` and present via
`present_files`. Overwrite the same file on each iteration rather than
creating a new versioned file, unless the user asks to keep a history.

## Optional final markdown handoff
Once the Questions tab is empty (or the user says the open questions no
longer matter) and the Wireframe tab is essentially complete, offer — don't
force — to also produce a clean markdown copy document with the same final
content, for handoff to design/dev. Only produce it on request.
