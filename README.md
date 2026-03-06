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

### interface-exploration

**Interface & Interaction Exploration**

A skill for generating 4 distinct, creative interface proposals for any conceptual solution. Each proposal represents a different design philosophy, with detailed trade-off analysis, interaction breadboarding, ASCII wireframes, and ASCII flow diagrams.

---

**Required Inputs**

Ask the user to provide:

1. **Conceptual Solution Proposal (required)**: The output from a solution-generation prompt, specifically the sections covering: problem, solution (with...

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

**When to Use Each Variant**

- **General Deep Analysis**: For broad, timeless strategic studies of a topic, market, or industry over time horizons (past → present → future 5 years).
- **Weekly Intelligence Canvas**: For fast-moving, 7-day competitive intelligence reports. Works best with rea...

---

### opportunity-mapping

**Opportunity Mapping**

A skill for generating structured strategic analyses that surface opportunities and ranked solutions from any business, product, or organizational input. Output is formatted in Confluence Wiki Markup for use in Confluence, Notion, or similar tools.

---

**Required Input**

Ask the user to provide:

1. **`<INPUT DO USUÁRIO>` (required)**: The core problem, idea, pain point, or strategic question.
2. **`<PRODUTOS ATUAIS PARA CLIENTES EXTERNOS>` (optional)**: Current exter...

---

### shape-up-planning

**Shape Up Planning Skill**

You will act as a strategic product and design partner, combining the skills of a senior product strategist (Shape Up expert) and an experienced chief of design. Your goal is to transform a raw idea into a complete, clear, scoped work specification ready for development, acting as a collaborator who enriches and structures original ideas.

**Overall Objective**

The process has two phases:

1. **Strategy Phase (Shape Up):** Analyze the initial proposal, question to g...

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
**After generating any component, run: `python starhtml_check.py <file>`**

> **Sub-references** (load when needed, same directory as this file):
> `./reference/icons.md` · `./reference/js.md` · `./reference/handlers.md` · `./reference/slots.md` · `./reference/demos.md`
>
> **Official demos** (canonical runnable examples, always from official framework repo):
> `https://raw.githubusercontent.com/banditbu...

---

### tech-planning-sequencing

**When to use this skill**

Use this skill when you need to:
- Plan the implementation sequence for a new feature or PRD
- Decompose tasks into a risk-aware development order
- Identify critical spikes before implementation
- Structure work into scopes with clear Definition of Done

**When NOT to use this skill**

- For simple, well-understood tasks that don't need sequencing
- When the user asks for code implementation directly (switch to Code mode)
- For architectural decisions without task br...

---

