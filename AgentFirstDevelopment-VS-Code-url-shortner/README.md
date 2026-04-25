# 🌊 Agent-First Development & Vibe Coding

This folder documents transition into **Agent-First Development** and the emerging paradigm of **Vibe Coding**.

Inspired by the [Agent-First Dev Series](https://www.youtube.com/playlist?list=PLj6YeMhvp2S4l1_iP4-pS6p7lgyqKo-Ix), this section explores how to build complex systems by prioritizing **Intent** over **Syntax**.

---

## 🛠️ Technical Syllabus (Workflow Mastery)

Based on the official VS Code Agent-First series, I am implementing the following workflow:

### 1. Agent Sessions & Environment

- **Agent Mode:** Transitioning from chat-based snippets to full "Agent Mode" where the AI has permission to edit files and run commands.
- **Sessions:** Managing isolated agent sessions to maintain clean context windows.
- **Control:** Reviewing and controlling agent changes using the built-in diff views to ensure architectural integrity.

### 2. Debugging & Observability

- **Chat Debug View:** Using internal logs to see exactly how the agent is "thinking."
- **Agent Debug Logs:** Analyzing the step-by-step execution to troubleshoot where a "vibe" might be drifting from the intent.

### 3. Customization & Expertise (The "Construct")

- **Custom Instructions:** Setting the global "Personality" and "Rules" for the agent.
- **Agent Skills:** Providing domain-specific expertise (e.g., C# Clean Architecture) that the agent can "invoke" when needed.
- **Hooks & Prompt Files:** Moving away from repetitive prompting toward **Prompt-as-Code**, using hooks to trigger specific agent behaviors based on the file context.

---

## 🚀 The AFD Workflow Loop

1. **Initialize Session:** Start an Agent Session with a clear **Intent**.
2. **Inject Context:** Reference relevant **Skills** and **Prompt Files** to ground the agent.
3. **Vibe Code:** Allow the Agent to generate implementations while monitoring the **Chat Debug View**.
4. **Verify & Review:** Use the **Control UI** to accept/reject changes and validate against **Hooks**.

---

## 🔬 Experiments & Projects

- **Lab 01: Agent Mode App Build:** Building a full-stack module using primarily Agent Mode (Ep 6).
- **Lab 02: Custom Skill Development:** Creating `.md` based skills for specialized C#/.NET tasks.
- **Lab 03: Observability Lab:** Troubleshooting a complex logic error using the Agent Debug Logs.

---

> _"The goal isn't just to code with AI; it's to build a system where the AI understands the architecture as well as the engineer does."_
