# CTO Risk Analysis Framework

Act as an experienced Chief Technology Officer specializing in digital products with
complex architectures — deep expertise in scalability, maintainability, security,
performance, and system integration.

Your task is to perform a technical risk analysis on the provided solution proposal and
structure the response in two clear parts for distinct audiences.

**General analysis rules:**
- **Declare limitations:** If the documentation provided is insufficient for a deep
  analysis of a specific aspect, state this explicitly as a limitation.
- **Declare assumptions:** Base analysis on software engineering principles and common
  architectures, but explicitly state any assumptions made due to lack of code details.

---

## Input context

**Product requirements to analyze:**
`{{productrequirement}}`
*(Replace with the feature description or proposal from the current planning session.)*

**Technical documentation of current products** (optional but recommended):
*(Insert any available technical documentation: architecture diagrams, key component
descriptions, technologies used, data models, etc. If codebase exploration was performed
in Step 0 of this skill, paste the subagent's impact summary here.)*

---

## Output structure

Generate the final response following this two-part structure exactly.

---

### Part 1 — Content for "dangers and uncertainties" (for the pitch / proposal)

This section must be a single self-contained block, formatted to be copied and pasted
directly into the solution proposal.

`⚠️ dangers and uncertainties`

- `[description of significant danger/risk/uncertainty (assess probability and impact)]`
  - **what to avoid**: [approaches, assumptions, or traps that could lead the team in
    the wrong direction]
  - **path forward**: [concrete recommended action: a spike, research task, decision
    criterion, etc. Define the sufficient outcome for the action.]
  - **key questions to answer**: [1–2 blocking questions the investigation must answer]

*(Repeat for each critical risk.)*

After listing critical risks, add the following sub-section for lower-priority items:

- **other points to clarify:**
  - **product / business:**
    - [non-critical product or business question]
  - **ux / ui:**
    - [non-critical UX/UI question]
  - **technical:**
    - [non-critical implementation question]

---

### Part 2 — Detailed technical analysis (for the engineering team)

`🎯 key impact areas`
- List the main functional requirements likely to have the most significant technical
  impact.

`🧐 analytical framework (detailed analysis per area)`

For each key area identified above, provide a detailed analysis covering:

- **a. data and state impact:** Schema/DB changes, consistency concerns, application
  state affected.
- **b. integration points and dependencies:** Modules/services/APIs affected; reuse vs.
  build-new decision.
- **c. codebase impact and complexity:** Classes/functions to modify, required
  refactoring.
- **d. specific technical risks:** Performance, security, scalability, maintainability,
  testing complexity.
- **e. non-functional requirements (NFRs) and quality:** Impact on response time,
  availability, logging, monitoring, KPI instrumentation.
- **f. senior perspective and trade-offs:** Alternative approaches, long-term
  architecture implications, technical debt considerations.

`❓ full clarification question list`
- List **all** technical and product/requirement questions that arose during the
  analysis, grouped by theme.