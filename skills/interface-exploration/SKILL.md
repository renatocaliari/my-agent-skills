---
name: interface-exploration
description: Generate 4 distinct UI/UX interface proposals for any conceptual product solution, each based on a different design philosophy — from conventional patterns to radical simplicity and technological vanguard. Use this skill whenever the user wants to explore interface alternatives, design proposals, UI options, or interaction patterns for a feature or product. Also trigger when the user provides a solution concept and asks "how could this look", "what are some UI options", "design alternatives", or wants to compare design approaches — even if they don't explicitly say "interface exploration".
---

# Interface & Interaction Exploration

A skill for generating 4 distinct, creative interface proposals for any conceptual solution. Each proposal represents a different design philosophy, with detailed trade-off analysis, interaction breadboarding, ASCII wireframes, and ASCII flow diagrams.

---

## Required Inputs

Ask the user to provide:

1. **Conceptual Solution Proposal (required)**: The output from a solution-generation prompt, specifically the sections covering: problem, solution (with features and breadboarding), and out-of-scope items.
2. **Current Product Documentation (optional)**: Links to design systems, screenshots, or existing UI patterns to ensure consistency.

---

## The 4 Design Philosophies

Each proposal must be based on one of these distinct philosophies:

| Proposal | Philosophy | Core Goal |
|----------|-----------|-----------|
| **A** | Conventional Standard | Zero learning curve; use the safest, most established UI patterns |
| **B** | Interaction Paradigm Shift | Inverte o modelo mental da interação - sistema propõe ao invés de usuário buscar, ou muda metáfora central (ex: lista→timeline, busca→descoberta) |
| **C** | Technological Vanguard | Use cutting-edge tech (AI, NLP, computer vision) for a "magical" experience |
| **D** | Radical Simplicity | Aggressive subtraction — find the minimum viable interaction |

### Proposal D — Radical Simplicity: Step-by-Step

This is the most nuanced proposal. Follow these steps:

1. **Deconstruct the request**: Don't accept the solution as given. What is the true "job to be done" behind the initial request?
2. **Practice aggressive subtraction**: What is the "1-week version" of this problem? Start with Proposal A and remove features, buttons, and information until only the essential core remains.
3. **Create a new visual metaphor**: Does the solution need to be a "table" or a "form"? Or can it be something drastically simpler?

> **Inspiration — The Dot Grid Calendar (Basecamp)**: Customers asked for a "calendar" (complex). Investigation revealed the real job was just "quickly see if a week is full or empty to plan ahead." They subtracted everything (event names, times, colors) and created a new metaphor: a simple grid where days with work get a dot. Seek similarly ingenious solutions.

---

## Prompt Template

Use this prompt, replacing the placeholder sections with user input:

```
Act as a senior product designer, expert in interaction design, information architecture, and multiple design philosophies — from conventional to radical. Your superpower is translating a conceptual solution into multiple concrete interface proposals and, crucially, analyzing the strategic trade-offs of each.

Your task is to analyze the provided solution proposal and generate **4 distinct and creative interface proposals** to implement it. Each proposal must represent a different design philosophy and be accompanied by a clear analysis of its pros and cons.

<conceptual solution proposal>
[insert the output from the solution generation prompt here — especially the 'problem', 'solution' (with features and breadboarding), and 'out of scope' sections]
</conceptual solution proposal>

<current product documentation (optional)>
[insert any link to a design system, screenshots of the current product, or description of existing UI patterns to ensure consistency, if needed]
</current product documentation>

### Main Task

Based on the materials provided, generate 4 interface proposals. To ensure they are truly distinct, base each on one of the following philosophies:

* **Proposal A — Conventional Standard:** Use the safest, most established UI/UX patterns for the problem. Goal: zero learning curve and maximum familiarity for the user.
* **Proposal B — Interaction Paradigm Shift:** Inverte completamente o modelo mental da interação. Não modifique apenas controles - mude como o usuário CONCEITUALIZA a tarefa. Baseie-se em 1-2 destes princípios:
  - **Inversão ativo/passivo:** Ao invés do usuário buscar/executar, o sistema antecipa/sugere/propõe
  - **Troca de metáfora central:** Lista→Timeline, Formulário→Conversa, Busca→Descoberta, Painel→Jornada
  - **Contexto sobre comando:** Interface que responde a contexto (tempo, local, histórico) ao invés de comandos explícitos
  - **União sobre separação:** Combinar visualização+edição, navegação+ação, configuração+uso em um único modo
  - **Progressão sobre estado:** Pensar em fluxos e evolução ao invés de estados e telas estáticas
  - **Pergunta norteadora:** "Se desconhecêssemos como isso é feito hoje, qual seria uma forma totalmente diferente de conceber essa interação?"
* **Proposal C — Technological Vanguard (Simplicity via Technology):** Imagine you have access to cutting-edge technologies (AI, natural language, computer vision, etc.). How would you use this technology to create a radically simpler or "magical" experience for the user, even if implementation is complex? Focus on experience innovation.
* **Proposal D — Radical Simplicity (Focus and Subtraction):** Innovation here comes not from technology, but from deeper understanding of the problem. Follow these steps:
    1. **Deconstruct the request:** Don't accept the solution as given. What is the true "job to be done" behind the initial request?
    2. **Practice aggressive subtraction:** What is the "1-week version" of this problem? Start with Proposal A and remove features, buttons, and information until only the essential core remains that still solves the main problem.
    3. **Create a new visual metaphor:** Does the solution need to be a "table" or a "form"? Or can it be something drastically simpler?

For each of the 4 proposals, strictly follow the 5-point output structure below.

---

### Response Format

---
### 🎨 Proposal A: Conventional Standard

**1. Philosophy and Design Guidelines:**
* [Describe in 1-2 sentences the philosophy of this proposal. E.g., "This approach uses a table layout with top filters, a universally recognized pattern..."]

**2. Breadboarding and Interaction Guidelines:**
* **Interface Elements (Ingredients):**
    * ↳ [Component 1, e.g., habit card]
    * ↳ [Component 2, e.g., weekly tracker container with checkboxes]
    * ↳ [Component 3, e.g., 'save' button]
* **Main Interaction Flow:** [Describe the user micro-flow. E.g., "User views list of cards, clicks a checkbox to mark the day, system auto-saves."]
* **Feedback and States:** [Describe visual states. E.g., "On save, checkbox fills and a success toast appears. For a panel with no habits, an empty-state message is shown with a call-to-action."]
* **Information Density and Copy:** [Define how "full" the interface should be and the tone of voice. E.g., "Medium density, with direct and informative text."]

**3. Main Interface Sketch (ASCII Art):**
* [Draw ASCII art representing the layout and components described above]

**4. Interaction Flow (ASCII Art):**
* [Create an ASCII art flowchart/flow diagram detailing the micro-flow specific to this proposal]

**5. ⚖️ Trade-off Analysis:**
* **Pros:** [E.g., low usability risk, fast development with standard components]
* **Cons:** [E.g., may not be most efficient for advanced users, little differentiation]
* **Development Effort:** [E.g., Low — uses existing components and patterns]
* **Main Risk:** [E.g., Risk of appearing generic and failing to engage users]

---
... (Follow the same 5-point structure for proposals B, C, and D)

```

---

## Output Structure Summary

For each of the 4 proposals, generate:

1. **Philosophy and Design Guidelines** — 1–2 sentence design rationale
2. **Breadboarding and Interaction Guidelines** — ingredients, interaction flow, feedback/states, information density
3. **ASCII Wireframe** — visual sketch of the main interface
4. **ASCII Flow Diagram** — interaction diagram using ASCII art
5. **Trade-off Analysis** — pros, cons, development effort, main risk

---

## Tips for Strong Outputs

- **Proposal A** should feel immediately familiar — think standard SaaS patterns.
- **Proposal B** should feel like a paradigm shift — the same problem solved through a completely different mental model (ex: instead of searching, the system anticipates; instead of forms, a conversation).
- **Proposal C** should feel like the future — leverage AI, voice, real-time, or ambient interaction.
- **Proposal D** should make the user say "why didn't we think of that?" — inspired by the Basecamp dot grid story.
- ASCII art doesn't need to be pretty, just clear enough to communicate layout and hierarchy.
- ASCII flow diagrams should cover the critical user path, not every edge case.
