---
name: interface-brainstorming
description: >
  Generate multiple strategically distinct UI/UX interface proposals for a conceptual solution.
  Activate automatically when:
  - the task involves UI, UX, interaction flows, layouts, screens, wireframes, or frontend decisions
  - visual or interaction trade-offs are ambiguous
  - brainstorming transitions into interface definition
  - the user requests interface alternatives, UX exploration, or design directions
---

# Interface Brainstorming

A skill for generating strategically distinct interface proposals for conceptual product solutions.

The goal is not merely to vary aesthetics, but to explore fundamentally different interaction models, mental models, densities, workflows, and user philosophies.

This skill should help:
- expand solution space
- reveal hidden assumptions
- expose trade-offs
- compare interaction philosophies
- converge toward a strategically coherent direction

---

# When to Use

Use this skill when:
- designing new products or features
- evaluating competing UI approaches
- interface decisions are ambiguous
- exploring user flows or interaction models
- translating product concepts into concrete interfaces
- frontend structure meaningfully affects product strategy

---

# Context Reconstruction

Before generating proposals:

1. Infer as much context as possible from:
   - the current request
   - session history
   - previous brainstorming
   - referenced plans/specifications
   - implied workflows and constraints

2. Reconstruct internally:
   - problem statement
   - user goals
   - likely workflows
   - platform assumptions
   - interaction constraints
   - success criteria

3. Extract the likely underlying job-to-be-done instead of relying only on the explicitly requested interface structure.

Do not blindly preserve:
- existing UI metaphors
- requested layouts
- assumed workflows

Challenge assumptions when useful.

---

# Progressive Clarification Principle

Prefer proceeding with explicit assumptions instead of blocking for additional information.

Only ask follow-up questions when missing information would materially change:
- interaction architecture
- platform strategy
- density strategy
- primary workflows
- accessibility constraints
- technical feasibility

If assumptions are made:
- state them explicitly
- continue with the exploration

Avoid asking for:
- restating already available context
- full specifications
- exhaustive requirements
- formal solution documents

---

# Hidden Job Extraction

Do not accept the requested interface structure at face value.

Infer:
- the underlying job-to-be-done
- latent user motivations
- operational tensions
- likely misuse/friction points
- whether the requested UI metaphor is actually necessary

The proposals should respond to the underlying need, not only the explicitly requested structure.

---

# Design Archetypes

| Proposal | Philosophy | Core Goal |
|---|---|---|
| **A** | Conventional Standard | Maximize familiarity and reduce learning curve |
| **B** | Interaction Paradigm Shift | Reframe the mental model of the interaction itself |
| **C** | Technological Vanguard | Use advanced technology to create a magical experience |
| **D** | Radical Simplicity | Remove everything except the essential interaction |
| **E** | Expert / Command-First | Optimize for speed, fluency, and expert throughput |

---

# Archetype Details

## Proposal A — Conventional Standard

Use the safest and most established UX patterns for the problem space.

Optimize for:
- predictability
- familiarity
- onboarding ease
- low usability risk
- consistency with existing SaaS/mobile conventions

The interface should feel immediately understandable.

---

## Proposal B — Interaction Paradigm Shift

Completely rethink how the user conceptualizes the task.

Possible transformations:
- active → passive
- search → discovery
- form → conversation
- dashboard → journey
- command → context
- state → progression

Guiding question:

> "If we had never seen this category before, how else could this interaction be conceived?"

The goal is conceptual reframing, not cosmetic novelty.

---

## Proposal C — Technological Vanguard

Use advanced technologies to radically simplify or elevate the experience.

Potential technologies:
- AI copilots
- natural language interaction
- predictive systems
- ambient computing
- automation
- computer vision
- semantic search
- adaptive interfaces

Focus on:
- experiential innovation
- leverage through intelligence
- reducing user effort via technology

Implementation complexity is acceptable if the user experience meaningfully improves.

---

## Proposal D — Radical Simplicity

Innovation through subtraction and focus.

Process:
1. Identify the true job-to-be-done
2. Remove non-essential interactions
3. Collapse flows aggressively
4. Replace complex metaphors with simpler ones

Optimize for:
- clarity
- calmness
- low cognitive load
- immediacy
- essentialism

Guiding question:

> "What is the smallest possible interaction that still solves the core problem?"

---

## Proposal E — Expert / Command-First

Design for users who already understand the domain.

Prioritize:
- keyboard-first interaction
- dense information layouts
- command palettes
- batch actions
- low interaction latency
- minimal visual chrome
- progressive acceleration
- high information throughput

Assume:
- users prefer speed over guidance
- users value control over discoverability
- onboarding is secondary

Guiding question:

> "If the user already knew exactly what to do, what could we remove?"

References:
- Linear
- Raycast
- Superhuman
- Vim
- Figma command palette

---

# Difference Between D and E

Proposal D removes complexity to make the experience universally understandable.

Proposal E removes guidance, onboarding, and explanatory structure to maximize speed for experienced users.

D optimizes for clarity.

E optimizes for fluency.

They are not interchangeable.

---

# Proposal Separation Rule

Each proposal must differ in at least TWO of the following:

- interaction model
- navigation structure
- information architecture
- primary metaphor
- user agency model
- density strategy
- feedback model
- temporal flow
- command structure

Do not generate proposals that differ only visually or cosmetically.

---

# Forced Trade-Off Rule

Each proposal must intentionally sacrifice something to optimize another dimension.

Examples:
- simplicity over flexibility
- automation over control
- speed over discoverability
- familiarity over differentiation
- density over approachability

Avoid “best of all worlds” proposals.

---

# Evaluation Criteria

Each proposal should strongly optimize for a different dimension:

| Proposal | Optimization |
|---|---|
| A | Familiarity |
| B | Conceptual reframing |
| C | Experiential leverage through technology |
| D | Essentialism and reduction |
| E | Expert speed and fluency |

---

# Hybrid Recommendation Phase

After generating all proposals:

1. Evaluate the strengths and weaknesses of each proposal in context
2. Identify compatible patterns that can be combined coherently
3. Recommend:
   - one primary direction
   - optional secondary traits borrowed from others
4. Explicitly explain:
   - what should NOT be combined
   - which trade-offs are intentionally preserved

The hybrid recommendation must remain coherent.

Avoid:
- feature soup
- contradictory interaction models
- “best of all worlds” synthesis

The recommendation should feel strategically opinionated.

---

# Required Output Structure

For EACH proposal (A–E), generate:

## 1. Philosophy and Design Guidelines

Explain:
- design philosophy
- interaction philosophy
- intended user feeling
- strategic rationale

---

## 2. Breadboarding and Interaction Guidelines

Include:
- interface ingredients/components
- primary interaction loop
- navigation model
- states and feedback
- information density
- copy/tone guidance

---

## 3. Main Interface Sketch (ASCII)

Provide a simple ASCII wireframe.

The goal is clarity, not visual perfection.

---

## 4. Interaction Flow (ASCII)

Provide an ASCII flow diagram covering:
- primary user flow
- key transitions
- important system responses

---

## 5. Trade-Off Analysis

Include:
- pros
- cons
- development effort
- usability risk
- scalability implications
- maintainability considerations

---

# Recommendation Output

After Proposal E, generate:

## 🧭 Recommended Direction

Include:
- primary proposal foundation
- elements borrowed from other proposals
- why the combination fits the context
- what trade-offs are intentionally accepted
- what should explicitly NOT be combined
- suggested implementation sequencing (optional)

The recommendation should be decisive and strategically coherent.

---

# Selection Step

After presenting all proposals and the recommendation:

Use the `question` tool when available.

Provide:
- short label
- one-line description

Options:
- A — Conventional
- B — Paradigm Shift
- C — Vanguard
- D — Radical Simplicity
- E — Expert / Command-First
- H — Recommended Hybrid

Fallback:

"Select A, B, C, D, E, or H."

---

# Output Quality Expectations

Strong outputs:
- reveal hidden assumptions
- explore genuinely different interaction models
- expose meaningful trade-offs
- create productive strategic tension
- help convergence, not only divergence

Weak outputs:
- differ only cosmetically
- merely add/remove AI
- preserve identical architecture across proposals
- avoid difficult trade-offs
- collapse into generic SaaS dashboards

The proposals should feel meaningfully different in philosophy, interaction model, and strategic intent.
