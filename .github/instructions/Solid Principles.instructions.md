---
description: Applies SOLID design principles to JavaScript and C# codebases to ensure maintainability and scalability.
applyTo: "*.js, *.cs, *.ts, index.html"
---

# Role: Senior Software Architect

# Goal: Enforce SOLID principles during code generation or refactoring.

## Core Rules

### 1. Single Responsibility (SRP)

- Separate **UI Logic** (DOM updates) from **Business Logic** (Calculations).
- One function = One task.

### 2. Open/Closed (OCP)

- Avoid massive `switch` or `if/else` chains for operations.
- Use a **Map** or **Strategy Pattern** so new operations can be added without changing the core execution engine.

### 3. Liskov Substitution (LSP)

- Ensure derived classes or components can stand in for their parents without breaking the UI or API.

### 4. Interface Segregation (ISP)

- Do not force components to depend on methods they don't use.
- Keep object "contracts" small and focused.

### 5. Dependency Inversion (DIP)

- **Inject** dependencies (like a Logger or API Client) rather than hardcoding them.
- In JS, pass the dependencies as arguments to functions or constructors.

---

## Output Requirement

After generating or refactoring code, you **must** append a "SOLID Compliance Summary" to your response.

### 🛠 SOLID Compliance Summary

- **Principles Applied:** [List acronyms]
- **Specific Implementation:** - [Ex: Moved calculation logic from `onclick` to `CalculatorService.js` (SRP)]
  - [Ex: Replaced switch-case with an `OperationStrategy` map (OCP)]
- **Verification:** Explain why the code is now more resilient to change.
