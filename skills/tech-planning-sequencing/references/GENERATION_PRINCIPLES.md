## Code & Product Generation Principles

When generating code, plans, architecture, or any final product output, strictly follow these principles in priority order:

1. **KISS** (Keep It Simple, Stupid)  
   - Always choose the simplest solution that works correctly.  
   - Avoid unnecessary abstractions, layers, or features.  
   - Favor readable, straightforward code over cleverness.

2. **DRY** (Don't Repeat Yourself)  
   - Eliminate duplication: extract shared logic into functions, components, hooks, utilities, etc.  
   - Reuse existing patterns, libraries, and conventions instead of reinventing.

3. **Convention over Configuration**  
   - Use strong, sensible defaults and conventions so the generated product "just works" with minimal setup.  
   - Assume standard naming (e.g., PascalCase components, kebab-case files), folder structures (e.g., src/components, src/pages), and framework idioms.  
   - Only add explicit configuration when the user explicitly deviates from conventions (e.g., custom table name, non-standard routing).  
   - Goal: Beginners/leigos get a working product immediately; no boilerplate decisions needed.

4. **Progressive Disclosure** (applied to the generated product)  
   - Make the end-user experience simple by default:  
     - Show only essential features/UI/options initially.  
     - Hide advanced settings, power-user tools, or customization behind toggles, "Show more", modals, or config files.  
   - Provide overrides for advanced users:  
     - Expose flags, env vars, config objects, or extension points only when requested or clearly needed.  
   - In UI/apps: Start with basic views → reveal complexity progressively (e.g., basic form → advanced validation/rules on expand).

5. **Polymorphism when technologies allow**  
   - Use interfaces, abstract classes, traits, or duck typing for extensibility (e.g., strategy pattern for behaviors, dependency injection for services).  
   - Apply only when it adds real value (e.g., pluggable auth providers, multiple renderers) — never over-engineer.  
   - Prefer in typed languages (TS, Python with protocols/ABCs); keep simple in scripts/prototypes.

When in doubt: Default to the simplest, most conventional path. Only add complexity/configuration if the user explicitly asks for it or the context demands it (YAGNI).