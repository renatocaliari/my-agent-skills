---
name: shape-up-planning
description: >
  Strategic product shaping using Shape Up principles.
  Activate automatically when:
  - discussing vague product ideas, MVPs, or feature proposals
  - scope, risks, or boundaries are unclear
  - transforming brainstorming into structured product direction
  - planning initiatives before implementation sequencing
  - evaluating trade-offs, assumptions, or delivery shape
---

# Shape Up Planning

A strategic shaping skill inspired by Shape Up methodology.

This skill transforms raw ideas into:
- scoped proposals
- strategic framing
- risk maps
- implementation boundaries
- sequencing foundations

The goal is NOT detailed specification writing.

The goal is:
- shaping
- framing
- reducing ambiguity
- exposing trade-offs
- identifying risks early
- defining meaningful scope boundaries

This skill acts as:
- product strategist
- systems thinker
- scope designer
- delivery-oriented planning partner

---

# When to Use

Use this skill when:
- product direction is ambiguous
- a feature idea feels too broad
- scope boundaries are unclear
- risks are poorly understood
- brainstorming must become actionable
- teams need a strategically coherent proposal before implementation
- product and workflow assumptions need clarification

---

# Context Reconstruction

Before asking questions:

1. Infer as much context as possible from:
   - current request
   - session history
   - brainstorming artifacts
   - referenced plans/specs
   - implied workflows
   - business constraints
   - technical hints

2. Reconstruct internally:
   - probable goals
   - stakeholders
   - operational tensions
   - workflows
   - implementation pressures
   - implicit assumptions

3. Infer the likely job-to-be-done behind the proposal.

Avoid asking users to restate information already present in context.

---

# Progressive Clarification Principle

Prefer:
- explicit assumptions
- provisional shaping
- iterative refinement

over blocking for complete information.

Only ask follow-up questions when missing information would materially affect:
- scope definition
- platform strategy
- business viability
- implementation feasibility
- operational constraints
- delivery sequencing

If assumptions are made:
- state them explicitly
- continue shaping

---

# Clarification and Gap Resolution

Before generating the final shaped proposal or invoking `plannotator`:

1. Identify:
   - unresolved ambiguities
   - missing constraints
   - unclear ownership
   - platform uncertainties
   - workflow gaps
   - business rule holes

2. Decide whether clarification is necessary.

Clarification should happen BEFORE:
- final proposal consolidation
- sequencing
- `plannotator` invocation

Use the `question` tool whenever available.

If unavailable:
- ask directly in chat.

Avoid excessive questioning.

Only ask questions that materially improve shaping quality.

---

# Recommendation-Aware Questions

Whenever using the `question` tool for strategic decisions:

Include:
- explicit options
- one AI-recommended option

The recommendation should:
- reflect the current context
- explain the reasoning briefly
- remain overridable by the user

Example:
- A — broader MVP
- B — narrow workflow-first scope
- R — recommended: narrow workflow-first scope to reduce integration risk

If the `question` tool is unavailable:
- present the same options in chat.

---

# Core Principles

All proposals should prioritize:

- KISS
- DRY
- convention over configuration
- progressive disclosure
- asymmetric risk reduction
- delivery realism
- focused scope
- sustainable complexity

Avoid:
- speculative over-engineering
- premature extensibility
- “platform thinking” too early
- vague MVPs
- feature soup

---

# Strategic Alternatives Rule

Generate strategic alternatives when useful.

Focus on:
- workflow strategy
- operational model
- ownership boundaries
- automation level
- rollout strategy
- integration strategy
- scope shape
- user responsibility model

Do NOT generate detailed UI/UX alternatives here.

If meaningful interaction or workflow complexity exists:
- recommend invoking the `interface-brainstorming` skill
- use it as the dedicated interface exploration phase
- integrate the selected direction back into the final proposal

---

# Interface Exploration Escalation

When meaningful UX or workflow complexity exists:

1. Evaluate whether invoking the `interface-brainstorming` skill would materially improve:
   - interaction clarity
   - scope definition
   - workflow strategy
   - UX risk reduction

2. Present a recommendation to the user.

Use the `question` tool when available.

Example options:
- "Yes — explore interface directions"
- "No — continue shaping only"
- "R — recommended: explore interface directions before final sequencing"

If the user approves (or selects the recommendation):
- invoke the `interface-brainstorming` skill
- integrate the selected/recommended direction back into the shaped proposal

---

# Origin Legend

Classify output origins using:

- `📥 from user/context:` extracted or adapted from user-provided information
- `✨ proposed by ai:` inference, refinement, recommendation, or gap-filling

Apply labels at the most logical granularity:
- section
- paragraph
- bullet group

---

# Main Shaping Responsibilities

The skill should:

1. Clarify the problem
2. Reveal hidden assumptions
3. Expose risks and tensions
4. Define scope boundaries
5. Identify linchpins
6. Shape a coherent solution direction
7. Prevent uncontrolled scope growth
8. Prepare the proposal for downstream UX and implementation planning

---

# Required Output Structure

## 1. 🤔 unanswered questions and unexplored issues

Generate:
- unresolved tensions
- hidden assumptions
- missing business rules
- stakeholder questions
- operational ambiguities
- validation unknowns

Questions should materially improve shaping quality.

Avoid trivial clarification requests.

---

## 2. 🧭 strategic shaping alternatives

Generate strategic alternatives focused on:
- product shape
- operational approach
- workflow ownership
- rollout philosophy
- integration strategy
- automation boundaries
- system responsibility

Each alternative should:
- optimize different trade-offs
- intentionally sacrifice something
- expose strategic implications

Do NOT produce detailed interface concepts here.

If interface complexity becomes central:
- recommend invoking the `interface-brainstorming` skill

---

## 3. 📝 structured shape up proposal

---

### 🎯 problem

Describe:
- who is affected
- where the problem appears
- operational/business impact
- why current approaches fail

Do NOT include solutions here.

---

### 💡 solution

Describe:
- core approach
- linchpin concepts
- essential workflows
- critical system behaviors
- key constraints
- main operational rules

Focus on conceptual clarity.

Avoid:
- low-level implementation detail
- visual/UI specifics
- excessive edge-case enumeration

Use structure:

#### [feature or capability name]

- what it is
- why it exists
- critical behavior
- important constraints
- operational implications

---

### ⚠️ dangers and uncertainties

Critically analyze:

#### 1. assumptions and gaps

Identify:
- implicit assumptions
- undefined rules
- missing workflows
- empty/error states
- business logic ambiguities
- operational dependencies

---

#### 2. systemic touch analysis

Analyze:
- integrations
- APIs
- data dependencies
- permissions
- architectural pressure
- operational coupling
- migration complexity

---

#### 3. investigation questions

Transform risks into concrete questions for:
- product
- design
- engineering
- stakeholders

---

#### 4. actionable risk map

Separate into:

##### product/business risks

Include:
- missing rules
- value proposition risks
- operational inconsistencies
- adoption assumptions

---

##### UX/workflow risks

Include:
- flow ambiguity
- cognitive overload risks
- discoverability concerns
- workflow fragmentation
- interaction complexity

Do not deeply solve interface design here.

Escalate major interaction exploration to:
`interface-brainstorming` skill

---

##### technical risks

Include:
- architecture pressure
- performance concerns
- scalability uncertainty
- data consistency risks
- operational complexity

---

### 🚫 out of scope

Explicitly define:
- excluded features
- deferred integrations
- future concerns
- intentionally unsupported workflows
- avoided complexity

Out-of-scope should protect focus.

---

# Interface Exploration Integration

If the proposal contains meaningful:
- UX complexity
- workflow ambiguity
- interaction design tension
- multi-step flows
- density trade-offs
- expert vs beginner tensions

recommend invoking:
`interface-brainstorming` skill

The interface exploration phase may redefine:
- scope
- implementation complexity
- risks
- sequencing
- out-of-scope boundaries
- workflow assumptions

After interface exploration:

1. Evaluate the selected/recommended direction
2. Reconcile findings back into the shaped proposal
3. Update:
   - risks
   - scope
   - constraints
   - sequencing assumptions
   - implementation expectations

The final proposal should reflect the selected interaction direction.

---

# Todo Tracking Behavior

If `todowrite` is available:
- always use it for actionable tracking items
- organize todos by:
  - shaping
  - risks
  - UX decisions
  - sequencing
  - technical investigation

If unavailable:
- provide structured textual todos in chat.

---

# Tracking and Sequencing

After shaping and interface reconciliation:

## Step 1 — tracking todos

Create structured tracking items covering:
- shaping decisions
- open risks
- UX decisions
- sequencing blockers
- investigation tasks

---

## Step 2 — sequencing integration

If the `tech-planning-sequencing` skill is available:

Offer:
- milestone mapping
- dependency sequencing
- vertical slicing
- implementation ordering
- risk-first sequencing

Use the `question` tool when available.

Example options:
- "Yes — generate implementation sequencing"
- "No — stop at shaping"
- "R — recommended: sequence implementation due to identified technical dependencies"

Only sequence AFTER:
- shaping convergence
- interface direction convergence

---

## Step 3 — final proposal consolidation

The final proposal should integrate:
- shaped strategy
- selected interface direction
- updated risks
- scope boundaries
- sequencing assumptions

The final artifact should feel:
- coherent
- opinionated
- scoped
- implementation-aware

---

# Cross-Domain Adaptability

This skill can be adapted beyond digital product planning.

The same shaping principles apply to:
- operational workflows
- service design
- internal processes
- organizational systems
- AI agent behaviors
- education/training flows
- physical experiences

Adapt by treating:
- "features" as capabilities or interventions
- "users" as participants, operators, or stakeholders
- "interfaces" as interaction surfaces, touchpoints, or workflows

---

# Output Expectations

Strong outputs:
- reduce ambiguity
- expose hidden tensions
- narrow scope intelligently
- reveal strategic trade-offs
- create implementation clarity
- integrate UX implications into shaping

Weak outputs:
- generic feature lists
- fake MVPs
- vague risks
- UI-first thinking too early
- pretending uncertainty does not exist
- broad unbounded scope
- “future-proof platform” thinking
