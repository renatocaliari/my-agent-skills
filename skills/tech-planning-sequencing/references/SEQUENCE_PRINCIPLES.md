# Sequencing Principles

These principles guide the ordering of tasks within each scope. Apply them in sequence when building the detailed task breakdown.

## Principle 0: External Interface Mocks

Create mocks for external interfaces first. This allows development to proceed without waiting for external dependencies.

**When to use:**
- The scope depends on third-party APIs, services, or systems
- External contracts are not yet finalized

**Examples:**
- Mock payment gateway response
- Mock external authentication provider
- Mock third-party notification service

---

## Principle 1: Internal API Mocks

Create internal API mocks to enable parallel development of UI and backend components.

**When to use:**
- Multiple teams or developers work on frontend and backend simultaneously
- API contracts are defined but implementation is not ready

**Examples:**
- Mock REST endpoints for frontend consumption
- Mock GraphQL schema
- Mock WebSocket events

---

## Principle 2: Key Enablers

Identify and implement key enablers—foundational components that unlock multiple downstream tasks.

**When to use:**
- A component is required by multiple other tasks
- The enabler has low implementation risk but high blocking potential

**Examples:**
- Authentication/authorization infrastructure
- Database schema and migrations
- State management setup
- Build/deploy pipeline configuration

---

## Principle 3: High-Risk Mitigation

Identify and address high-risk technical tasks early. Introduce `[spike]` tasks before implementation when uncertainty is fundamental.

**When to use:**
- Tasks marked as "arriscada" in the input
- `modo_analise` = `sugestivo` and you identify fundamental uncertainties
- Technical feasibility is unknown or uncertain

**Spikes:**
- Time-boxed research tasks (typically 1-3 days)
- Output: decision, prototype, or proof of concept
- May result in scope adjustment

**Examples:**
- `[spike]` Evaluate performance of candidate database for large datasets
- `[spike]` Prototype real-time sync strategy
- Implement complex algorithm with unknown performance characteristics

---

## Principle 4: Smart Unblocking for Cross-Scope Risks

Position tasks that unblock risks in subsequent scopes strategically.

**When to use:**
- A task in the current scope creates a dependency for a high-risk task in a future scope
- Early implementation reduces uncertainty across the overall plan

**Examples:**
- Implement authentication in current scope to unblock permission-heavy features in next scope
- Create data export capability early to unblock analytics scope

---

## Principle 5: Incremental Functionality

Position "nice-to-have" tasks toward the end of the sequence. Do not suggest new nice-to-have tasks.

**When to use:**
- Tasks are explicitly marked as "nice-to-have" in the input
- Core functionality is delivered first

**Note:** You only reposition existing nice-to-have markers. Never add new ones.

---

## Principle 6: Dependencies and Clear Naming

Order remaining tasks based on their dependencies. Ensure task names are clear and descriptive.

**When to use:**
- All higher-priority principles have been applied
- Remaining tasks have clear dependency relationships

**Guidelines:**
- Task names should be actionable and specific
- Use verb-noun format (e.g., "Implement user registration flow")
- Include scope context if ambiguous (e.g., "Admin panel: Add user management")
