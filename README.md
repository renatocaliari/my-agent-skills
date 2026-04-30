# Agent Skills

A collection of custom skills for AI agents.

## Installation

Install these skills with:

```bash
npx skills add renatocaliari/my-agent-skills
```

## About

This repository contains skills published using [agent-sync](https://github.com/renatocaliari/agent-sync).

## Skills

### boilerplate-go

**Go Web Application Boilerplate (v1.0.0 Ready)**

Go boilerplate inspired by [Northstar](https://github.com/delaneyj/toolbelt), featuring:

> ⚠️ **Datastar v1.0.0 Required** - This boilerplate uses Datastar v1.0.0 (not RC.8). See [Installation](#datastar-v100-installation) below.
- **[Datastar](https://data-star.dev)** - Reactive hypermedia via SSE
- **[Templ](https://templ.guide)** - Go components that generate HTML
- **[DaisyUI + TailwindCSS](https://daisyui.com)** - UI components and styling...

---

### codebase-spec

**Codebase → Product Spec**

You are a senior product analyst reverse-engineering a product from its source code.
Your job: produce a **living product specification** that is completely tech-stack-agnostic —
so thorough that another team could rebuild the product in any language or framework.

---

**Phase 0 — Intake**

Accept codebase via any of:
- **Uploaded files / zip** → extract and explore with bash tools
- **Pasted code snippets** → treat each as a module
- **Filesystem path** → `find` + ...

---

### evolutionary-principles

**Evolutionary Product Thinking**

A strategic thinking skill inspired by:
- evolutionary systems
- novelty search
- stepping-stones theory
- adaptive systems
- product ecosystems
- connection mapping
- exaptation
- emergent innovation

This skill helps teams:
- avoid premature convergence
- identify promising stepping-stones
- evaluate evolutionary potential
- explore non-obvious product directions
- prioritize enabling capabilities
- think beyond rigid roadmap logic
- cultivate adaptability an...

---

### interface-brainstorming

**Interface Brainstorming**

A skill for generating strategically distinct interface proposals for conceptual product solutions.

The goal is not merely to vary aesthetics, but to explore fundamentally different interaction models, mental models, densities, workflows, and user philosophies.

This skill should help:
- expand solution space
- reveal hidden assumptions
- expose trade-offs
- compare interaction philosophies
- converge toward a strategically coherent direction

---

**When to Use**

...

---

### jtbd-skill

**Jobs To Be Done — Complete Skill**

This skill contains **10 specialized prompts** for conducting comprehensive Jobs To Be Done analyses.
Each prompt corresponds to a specific step or dimension of the JTBD methodology.

---

**Prompt Map — When to Use Each**

| # | Prompt | When to use |
|---|--------|-------------|
| 1 | **Contextual Segmentation** | Create market segments based on situational factors (not demographics) |
| 2 | **Thinking Styles (Indi Young)** | Identify significantly differe...

---

### multi-method-market-analysis

**Multi-Method Market Analysis**

A skill for producing rigorous, structured market analysis using multiple complementary methodologies. Two prompt variants are available depending on the user's goal.

---

**Interaction Tool Guidelines**

**IMPORTANT**: When the user needs to choose between predefined options, ALWAYS use the `question` tool (if available) with enumerated format:
- Options with short `label` and `description`
- Examples: variant selection (General Deep/Weekly Intelligence), topi...

---

### opportunity-mapping

**Opportunity Mapping**

A skill for generating structured strategic analyses that surface opportunities and ranked solutions from any business, product, or organizational input. Output is formatted in Confluence Wiki Markup for use in Confluence, Notion, or similar tools.

---

**Interaction Tool Guidelines**

**IMPORTANT**: When the user needs to choose between predefined options, ALWAYS use the `question` tool (if available) with enumerated format:
- Options with short `label` and `descriptio...

---

### questions-quality

**Narrative Capture — Avaliação e Melhoria de Perguntas**

Skill para avaliar se perguntas (e a **sequência** entre elas) em entrevistas, formulários e roteiros terapêuticos seguem os princípios de captação de narrativas e extração de significado. 

A skill atua em duas dimensões:
1. **Qualidade Individual:** A pergunta em si evita vieses, abstrações e defesas?
2. **Qualidade do Sequenciamento:** A ordem das perguntas respeita o funcionamento da memória humana?

---

**🚨 ALERTA DE AMBIGUIDADE — ...

---

### shape-up-planning

**Shape Up Planning**

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
- deli...

---

### short-cycle-product

**Product with Short Learning Cycles**

This guide is a method to replace speculation with evidence, step by step.
**Core principle**: experiment before building. Reduce uncertainty with small, fast, and cheap experiments.

> "Life is too short to build something that nobody wants." — Ash Maurya

**Method Structure**

The process has **8 stages** (not necessarily linear):
1. Find and understand the audience
2. Define the market
3. Define and prioritize solutions
4. Develop and evaluate the offer...

---

### starhtml

**StarHTML — Core Skill**

StarHTML = Python objects that compile to reactive Datastar HTML.

**After generating any component, validate with:** `starhtml-check <file.py>`

> If `starhtml-check` is not installed:
> ```bash
> curl -L https://raw.githubusercontent.com/renatocaliari/starhtml-skill/main/starhtml_check.py \
>   -o /usr/local/bin/starhtml-check && chmod +x /usr/local/bin/starhtml-check
> ```

> **UI Components:** For production-ready UI, use **[StarUI](https://ui.starhtml.com/)** — sh...

---

### tech-planning-sequencing

**Tech Planning & Sequencing Skill**

You will act as a senior technical lead producing a structured, risk-aware implementation
plan. Your goal is to decompose a feature or plan into sequenced scopes with clear
Definition of Done and acceptance criteria — and, when relevant, ground the plan in a
real understanding of the existing codebase.

**When to use this skill**

- Plan the implementation sequence for a new feature or plan
- Decompose tasks into a risk-aware development order
- Identify cri...

---

