# Agent-First Development with VS Code and GitHub Copilot

This repository contains practice projects and notes based on the **VS Code Learn: Agent-First Development** series. This document serves as a comprehensive guide to the concepts, workflows, and tools required to transition from basic AI code completion to fully agentic software development.

---

## 1. The Core Formula for Agent Success

Success with AI agents is not magic; it is a result of five distinct components working in harmony:

- **The Harness:** This is the environment (VS Code + GitHub Copilot Chat) that provides the "wiring." It allows the AI model to communicate with your file system, terminal, and external tools.
- **The Model:** The reasoning engine (e.g., Claude 3.5 Sonnet, GPT-4o). Different models offer various "Thinking Effort" levels (Low, Medium, High) to balance response speed with architectural depth.
- **Context:** The specific information provided to the model. This includes open files, directory structures, and project-specific instructions provided via the `#` symbol or the context picker.
- **Tools:** Capabilities enabled for the agent, such as `terminal` (running commands), `file-edit` (writing code), and `web-search`. Agents use these to perform actions rather than just generating text.
- **Prompts:** The intent and instructions you provide. High-quality prompts are detailed enough to define the goal but flexible enough to let the agent determine the best implementation.

## 2. Session Management & Control

Managing how an agent interacts with your codebase is critical for maintaining safety and quality.

- **Approval Levels:**
  - **Default Approvals:** The agent asks for permission before running terminal commands or significant tool calls.
  - **Bypass Approvals:** Tools are auto-approved, but the agent will stop if it needs clarification from the user.
  - **Autopilot:** The agent is fully autonomous, making its own decisions to complete the task until it reaches the goal.
- **Context Window & Tokens:** Every model has a memory limit measured in tokens. The "Context Window" view in VS Code helps monitor how much memory is consumed by system instructions, tool definitions, and user history.
- **Compact Conversation:** A feature that summarizes long chat histories into essential implementation details, freeing up space in the context window for more complex tasks.

## 3. Steering and Refining Work

Agents are collaborative; you can steer them in real-time as they work.

- **Steering:** Instead of waiting for a task to finish, you can provide a "Steer" message to yield the current action and redirect the agent's logic (e.g., "Actually, use a dark theme instead").
- **Editing Prompts:** Editing a previous message allows you to correct the initial instruction. This triggers a "Restore Checkpoint," undoing the agent's work back to that point so it can restart with the correct information.
- **Forking Sessions:** If you want to explore an alternative architecture (e.g., "What if this CLI was a Fast API?"), you can fork the current session to a new tab. This preserves your original work while allowing for safe experimentation.
- **Checkpoints:** Automated "Save States" created by VS Code. You can restore your codebase to a specific checkpoint if an agent's changes go in an undesired direction.

## 4. Operational Modes & Environments

Agents can run in different "modes" and on different "compute" platforms.

- **Interaction Modes:**
  - **Ask Mode:** Best for general Q&A and explaining existing code without making changes.
  - **Plan Mode:** The agent acts as an architect, discussing the strategy and breakdown of a task before writing any code.
  - **Agent Mode:** The implementation phase where the agent actively uses tools to edit files and run commands.
- **Execution Environments:**
  - **Local:** The agent runs on your machine using your local resources.
  - **Cloud (GitHub Platform):** The agent runs on GitHub’s infrastructure. This is ideal for asynchronous work; you can start a task in the cloud and move to another local task while it finishes.
  - **Copilot CLI:** A terminal-based agent experience for developers who prefer staying in the command line.

## 5. Debugging and Diagnostics

When an agent fails or behaves unexpectedly, VS Code provides deep transparency tools.

- **Agent Debug Logs:** A chronological log of every "thought," tool call, and internal hook triggered during a session. It helps identify exactly where a skill or instruction failed to load.
- **Agent Flowchart:** A visual representation of the agent's decision-making process, showing the sequence of tool calls and model responses.
- **Chat Debug View:** Provides the raw data (JSON) sent to the LLM. This is used to inspect the exact system prompts, user memory preferences, and token usage for every turn.
- **Troubleshoot Command:** Using `/troubleshoot` allows you to ask the agent about its own internal state, such as where it is loading custom skills from.

---

## 6. Practical Workflow: URL Shortener Example

The culmination of these concepts is seen in the "Plan-to-Implementation" workflow:

1.  **Define Intent:** Start in **Plan Mode** to outline a URL Shortener using specific technologies (e.g., Python 3.14, SQLite, UV).
2.  **Clarify:** Have a back-and-forth conversation to define features like Base62 encoding and UI preferences.
3.  **Implement:** Switch to **Autopilot** to let the agent initialize the project, create the database schema, write the FastAPI backend, and design a dark-themed CSS frontend.
4.  **Verify:** The agent runs its own tests in the terminal to ensure the URL routing and redirection work correctly.

---

### References

- [Introduction to Agent-First Development](https://www.youtube.com/watch?v=uu4sf8z9n8c)
- [Your First Agent Session in Action](https://www.youtube.com/watch?v=WcN74XvZGes)
- [Reviewing and Controlling Agent Changes](https://www.youtube.com/watch?v=oFSJs6RnFt4)
- [Agent Sessions and Environments](https://www.youtube.com/watch?v=0CsKOO7d35I)
- [Agent Debug Logs and Chat Debug View](https://www.youtube.com/watch?v=aW2jlbbUREc)
- [Demo: Build Your First App with Agent Mode](https://www.youtube.com/watch?v=hmfldW7dmgw)
  readme.md
  Displaying readme.md.
