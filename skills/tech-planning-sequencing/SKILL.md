---
name: tech-planning-sequencing
description: >
  Generate structured development plans with risk-based or UI-first sequencing. Analyzes
  tasks, identifies critical spikes, and produces detailed implementation sequences with
  DoD and acceptance criteria. Activate when:
  - Explicitly called by the `shape-up-planning` skill after a proposal is shaped
  - Keywords / intents: "sequence tasks", "prioritize", "riskiest first", "dependencies",
    "group scopes", "technical planning", "plan spikes", "order implementation"
  - Workflow stage: after high-level brainstorming/pitch, during or before detailed task
    breakdown, when dependencies or risk order are unclear
---

# Tech Planning & Sequencing Skill

You will act as a senior technical lead producing a structured, risk-aware implementation
plan. Your goal is to decompose a feature or plan into sequenced scopes with clear
Definition of Done and acceptance criteria — and, when relevant, ground the plan in a
real understanding of the existing codebase.

## When to use this skill

- Plan the implementation sequence for a new feature or plan
- Decompose tasks into a risk-aware development order
- Identify critical spikes before implementation
- Structure work into scopes with clear Definition of Done

## When NOT to use this skill

- Simple, well-understood tasks that don't need sequencing
- User asks for code implementation directly → switch to Code mode
- Architectural decisions without task breakdowns → use Architect mode directly

---
## Non-technical adaptation note

This skill's sequencing principles (risk order, dependencies, spikes) apply equally to
non-technical projects: business process rollouts, marketing campaigns, events. Adapt by:
- Replacing "tech risk" with "executional risk" or "process risk"
- Treating spikes as "research tasks" or "validation tasks"
- Keeping the scope + DoD + acceptance criteria structure intact

---

## Interaction Tool Guidelines

**IMPORTANT**: When the user needs to choose between predefined options, ALWAYS use the
`question` tool (if available) with enumerated format:
- Options with short `label` and `description`
- Examples: strategy selection (risky/ui-first), mode (strict/suggestive), approval, etc.

When `question` tool is not available, use enumerated text in chat (A/B/C/D or 1/2/3).

---

## Output Guidelines

- Default mode: riskiest-first (identify & front-load spikes)
- Alternative modes: UI-first, suggestive (infer from context)
- Group into scopes with explicit DoD and acceptance criteria per scope
- Use tags: [SCOPE-1] [DOD] [RISK-ORDER] [SPIKES] [SEQUENCE]
- After output, use `question` tool to ask for approval (Approve / Refine / Execute)
- Fallback (no question tool): "Approve sequence? (respond: approve, refine, or execute)"

---

## Inputs

1. **sequencing_strategy** (optional): `riskiest-first` (default) or `ui-first`
   - `riskiest-first`: Prioritize high-risk tasks and spikes early
   - `ui-first`: Prioritize UI/UX deliverables to get early feedback

2. **analysis_mode** (optional): `suggestive` (default) or `strict`
   - `suggestive`: Identify and suggest risks, spikes, and enablers not explicitly marked
   - `strict`: Only work with explicitly marked risks and tasks

3. **tasks** (required): plan, solution proposal, or task list
   - May include markers: `nice-to-have` or `risky`
   - Format: bullet list or structured document

---

## Workflow

### Step 0 — Codebase awareness check ⚠️

Before sequencing, assess whether the existing codebase is understood well enough to
evaluate technical impact. Do this in order:

1. **Check memory and recent context:** Look for any stored summaries, prior exploration
   results, or git history references that describe the current architecture, key modules,
   or past changes related to the feature area.

2. **If codebase knowledge is absent or stale**, ask the user using the `question` tool
   (or via chat if unavailable):

   > "To plan accurate scopes and risks, it helps to understand where this feature will
   > touch the existing codebase. Do you want me to explore it now?"

   Options:
   - "Yes — explore the codebase and map impact areas"
   - "No — proceed with what we have"
   - "Recommend based on complexity"

3. **If user confirms exploration:** launch a subagent instructed to:
   - Scan the relevant modules, services, APIs, and data models likely touched by the
     feature
   - Identify existing patterns, coupling points, and potential conflict zones
   - Return a structured impact summary (touched files, data flows, risk areas)

   Feed the subagent's findings into Steps 1–6 below and into the CTO risk analysis
   (see Step 1b).

4. **If user declines:** proceed from Step 1 using only available context, and note any
   assumptions made due to limited codebase visibility.

---

### Step 1 — Read and analyze the task list

- Identify any markers (`nice-to-have`, `risky`)
- Understand domain and context

#### Step 1b — Deep technical risk analysis (conditional)

If codebase exploration was performed in Step 0, or if the user requests a detailed
technical assessment, load and apply
**[references/CTO_RISK_ANALYSIS.md](references/CTO_RISK_ANALYSIS.md)**.

This produces two outputs:
- **Part 1** — `⚠️ dangers and uncertainties` block ready to paste into the proposal
- **Part 2** — Full technical analysis for the engineering team (impact on data, APIs,
  codebase complexity, NFRs, trade-offs)

The findings from Part 2 directly inform the spike identification and scope sequencing
in Steps 2–5 below.

---

### Step 2 — Identify critical spikes

- Look for tasks marked as `risky`
- If `analysis_mode = suggestive`, identify additional fundamental uncertainties
- Define an "initial critical spikes scope" if applicable

### Step 3 — Define main functional scopes

- Identify and name the main functional scopes
- First scope must be "domain core functionality"
- Group related tasks logically

### Step 4 — Sequence scopes at high level

- Apply `sequencing_strategy` to order scopes
- Justify the sequence based on the chosen strategy

### Step 5 — Detail task sequence per scope

- Use principles 0–6 (see [references/SEQUENCE_PRINCIPLES.md](references/SEQUENCE_PRINCIPLES.md))
- For each task: name, objective, components, justification, acceptance criteria
- Mark suggested items with `💡 [suggestion]` when `analysis_mode = suggestive`

### Step 6 — Output in specified format

Follow the complete template in [references/OUTPUT_FORMAT.md](references/OUTPUT_FORMAT.md).

### Step 7 — Create trackable todos (if `todowrite` is available)

Check if `todowrite` is available. If yes, create trackable tasks from the scopes and
sequence generated. If not, skip and use textual output only.

### Step 8 — Confirm next step

After output, use the `question` tool to confirm next steps:

Options:
- "Create todos and execute with subagents" — for independent parallel tasks
- "Display sequence only" — no task creation
- "Execute sequentially" — no subagents
- "Recommend based on context" — let the AI decide

Fallback (no question tool): "Next step? (respond: create tasks, display, execute, or
recommend)"

---

# References

- **[references/PRINCIPLES.md](references/PRINCIPLES.md)** - The 6 sequencing principles for task ordering
- **[references/OUTPUT_FORMAT.md](references/OUTPUT_FORMAT.md)** - Complete output template with all sections
- **[references/RISK_ANALYSIS_FRAMEWORK.md](references/RISK_ANALYSIS_FRAMEWORK.md)** - CTO-level technical risk analysis framework (loaded conditionally in Step 1b)
