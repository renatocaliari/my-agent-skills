# Output Format Template

Use this exact structure when generating the sequencing plan.

---

## 1. Identified Scopes

### Critical Initial Spikes Scope (if applicable)
**Name:** `[scope name]`
**Description:** `[detailed description of critical initial spikes]`

### Main Functional Scopes
1. **`[scope name 1]`**: `[brief description]`
2. **`[scope name 2]`**: `[brief description]`
3. **`[scope name 3]`**: `[brief description]`
...

---

## 2. High-Level Sequence of Identified Scopes

1. **`[scope name]`**: `[justification for position based on sequencing strategy and principles 0–6]`
2. **`[scope name]`**: `[justification...]`
...

---

## 3. Detailed Development Sequence per Scope

### Scope: `[scope name]`

**Overall Scope Goal:** `[main objective of this scope]`

**Scope Definition of Done (DoD) – High Level:**  
`[list of completion criteria for the entire scope]`

**Detailed Task Sequence:**

#### 1. `[prefix if needed]` `💡 [suggestion]` `[task name]`
**Primary Objective / Value Delivered:** `[what this task achieves]`
**Key Components Involved:** `[list of modules, systems, or layers]`
**Sequencing Justification:** `[mandatory explanation using Principles 0–6. If influenced by a newly identified risk or suggestion, explicitly state it here.]`
**Acceptance Criteria (high-level):**  
- `[criterion 1]`  
- `[criterion 2]`  
...

#### 2. `[prefix if needed]` `💡 [suggestion]` `[task name]`
[... same format ...]

---

## 4. Final Summary – Main Functional Scope Names

- `[scope name 1]`  
- `[scope name 2]`  
- `[scope name 3]`  
...

---

## Notes on Suggestions

- When `modo_analise` = `suggestive`:  
  Mark your own contributions with `💡 [suggestion]`:  
  - Newly identified risks  
  - Recommended spikes  
  - Enabling tasks you propose  

- When `modo_analise` = `strict`:  
  Do **not** add any suggestions.  
  Work **only** with explicitly provided information.