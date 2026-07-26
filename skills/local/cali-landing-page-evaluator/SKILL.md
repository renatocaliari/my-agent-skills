---
name: landing-page-evaluator
description: "Evaluates existing landing page copy (or a description/brief of a landing page not yet written) and/or generates a new landing page structure with full copy, based on copywriting frameworks mapped to 5 product/service/brand categories, with a focus on human tone and anti-marketing-bullshit writing (avoiding generic-AI clichés like 'elevate', 'unlock', 'seamless', 'journey', empty promises). Use this skill whenever the user mentions a landing page, sales page, opt-in page, conversion copy, or a product/service page structure, or asks to review, critique, improve, or create copy for a page meant to convert — even if they don't use the words 'landing page' explicitly (e.g. 'my course page', 'my SaaS homepage copy', 'copy to attract mentorship clients')."
---

# Landing Page Evaluator & Builder

This skill runs a single unified workflow, whether the user is evaluating
existing copy or building one from scratch: gather whatever context exists,
actively surface gaps and contradictions instead of silently filling them,
and produce a three-part deliverable — **Questions**, **Evaluation**,
**Wireframe** — as one interactive HTML artifact. As the user answers
questions in follow-up turns, regenerate the same artifact with updated
state.

Always read `references/frameworks.md` (the 5 categories) and
`references/anti-ai-tone.md` (the cross-cutting checklist) before
evaluating or generating any copy — they are the basis for judgment in this
skill, not optional background material. Read `references/artifact-guide.md`
before building the HTML deliverable.

## The 5 categories (summary — full detail in references/frameworks.md)

1. **SaaS / technical tool** — Honest PAS + FAB. Rational decision.
2. **High-involvement relational service** (coaching, consulting, mentorship) — StoryBrand + BAB. Client is the hero, you're the guide.
3. **Therapeutic practice / personal care / vulnerable audience** — clarity + safety, not aggressive persuasion.
4. **Physical product / experience / e-commerce / lifestyle** — Sensory AIDA.
5. **Open-source project / developer tool** — Problem → Approach → Evidence → How to try it. No hype.

---

## Core principle: surface gaps and contradictions, never silently resolve them

This is the most important behavior in this skill. Understanding context
well enough to notice what's missing or inconsistent matters more than
producing a fast, polished-looking result. A confident-sounding landing
page built on invented assumptions is worse than a shorter one with the
gaps clearly marked.

**Gaps** — information needed to write a specific section that hasn't been
provided, for example:
- No stated audience, or audience described too broadly to write to
- No clear desired action / final CTA
- No tone-of-voice reference (existing site, prior writing, voice sample)
- No real proof (testimonial, number, case) when the category's framework
  calls for proof
- Category is genuinely ambiguous between two of the 5 (e.g. a technical
  product that's sometimes sold to developers, sometimes to enterprise
  buyers — those are different categories with different frameworks)
- Language of the final page is unclear or plausibly different from the
  language of the conversation

**Contradictions** — signals that conflict with each other, for example:
- Audience described as vulnerable/overwhelmed but the user is asking for
  urgency-heavy, high-pressure copy
- Product described as a peer-to-peer developer tool but the brief asks
  for heavy sales rhetoric and lead-capture CTAs
- Existing copy claims something ("used by thousands of teams") that
  contradicts other context the user gave (e.g. "this just launched last
  week")
- Tone samples provided don't match the tone the user says they want

**Rule:** if something is a gap or contradiction that would change a
section's content or the overall structure, it becomes a question in the
Questions tab — do not guess and move on. The only exception is a genuinely
trivial stylistic choice where any reasonable default works and doesn't
change structure or meaning (e.g. minor phrasing); in that case, make the
call and state the assumption in the Evaluation tab instead of blocking on
it.

**Language of the page:** default inference is the language the user is
writing the conversation in. Treat this as a question needing confirmation
only if it's ambiguous or contradicted by context (e.g. the brief mentions
an international audience while the user writes in Portuguese). Otherwise,
state the assumed language as a normal assumption in the Evaluation tab and
don't hold up the whole page over it.

---

## Workflow

### Step 1 — Intake
Take whatever the user provides: pasted/uploaded existing copy, or a
description/brief of an offer that doesn't exist as copy yet. Both are
valid starting points for the same workflow.

### Step 2 — Analyze
- Identify the most likely category (or a hybrid of two, if genuinely
  mixed — e.g. a project that's both a technical SaaS product and an
  open-source developer tool depending on audience) and note the
  reasoning.
- Run the anti-AI-tone checklist and the category's framework-fit check
  against whatever exists (existing copy, or the brief as given).
- Actively look for gaps and contradictions per the section above — this
  is not a passive step; assume there are gaps unless the brief is
  unusually complete, and check for them deliberately category by
  category (audience, goal/CTA, tone reference, proof, category fit,
  language).

### Step 3 — Produce the three-part artifact
Always produce all three parts together, even when one is minimal:
- **Questions** — every gap and contradiction found, phrased as a direct
  question the user can answer in their next chat message, ordered with
  structure-changing questions (e.g. category ambiguity) first.
- **Evaluation** — assessment of everything submitted so far: strengths,
  the highest-impact issues (existing copy) or what's solid vs. assumed
  (new brief), scored against frameworks.md and anti-ai-tone.md. State
  assumptions explicitly rather than presenting them as settled.
- **Wireframe** — reflects *only* confirmed/provided content. Sections
  with enough real information render with full real copy. Sections that
  depend on an open question render as a clearly marked pending block
  instead of invented content (see artifact-guide.md for the exact
  rule). Never invent testimonials, numbers, or client names to fill a
  gap — always mark it pending instead.

Build this as a single three-tab HTML file per `references/artifact-guide.md`,
save to `/mnt/user-data/outputs/<slug>-landing-page.html`, and present it
via `present_files`.

### Step 4 — Iteration loop
When the user answers one or more open questions in a later message:
- Update the category/language inference if the answer changes it.
- Re-run the Step 2 analysis with the new information.
- Regenerate the same three-tab file (overwrite it), moving resolved
  points out of Questions and into Evaluation/Wireframe, and expanding
  wireframe sections that are now unblocked.
- Re-present the file. Don't re-ask questions that were already answered.

### Optional final step — markdown handoff
Once the Questions tab is empty (or the user explicitly says the
remaining open questions don't matter to them) and the Wireframe tab is
essentially complete, offer to produce a clean markdown copy document with
the final content, for handoff to design/dev. Only produce this on
request — it's not part of the default deliverable.

### Rule on invented proof
This skill never invents numbers, testimonials, client names, or
statistics. When a framework calls for proof and none was provided, that
is always a gap — it goes in the Questions tab and shows as pending in the
Wireframe tab, never as fabricated content presented as real.
