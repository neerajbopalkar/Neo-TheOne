# 🧠 GitHub Copilot Agent Skills [Work in progress]

This folder contains custom **Agent Skills** designed to extend and refine the expertise of GitHub Copilot within this workspace.

Instead of generic suggestions, these skills provide Copilot with specific domain knowledge, architectural constraints, and "Expert Personas" to ensure high-quality code generation.

## 🎯 Current Expertise Modules

### 1. C# Architecture & Design Patterns

- **Focus:** Enforcing SOLID principles, Clean Architecture, and modern .NET 8+ syntax.
- **Logic:** Guides the agent to prefer Dependency Injection and asynchronous patterns.
- **File:** `Skills/csharp-architect.md`

### 2. JavaScript/TypeScript Best Practices

- **Focus:** Performance-optimized React patterns and Type-safety.
- **Logic:** Ensures the agent avoids `any` types and uses functional programming paradigms.
- **File:** `Skills/ts-expert.md`

### 3. Repository Context & Onboarding

- **Focus:** Teaching the agent the structure of _this_ specific "Neo-TheOne" repository.
- **Logic:** Helping the agent understand where MCP and MAF projects reside to assist with cross-project integration.

## 🛠️ How to use these Skills

These Markdown files are designed to be referenced by GitHub Copilot. You can "plug" these into your Copilot configuration to:

1.  **Standardize code reviews.**
2.  **Generate boilerplate** that aligns with specific project rules.
3.  **Provide context** for complex refactoring tasks.

---

_"I'm trying to free your mind, Neo. But I can only show you the door. You're the one that has to walk through it."_
