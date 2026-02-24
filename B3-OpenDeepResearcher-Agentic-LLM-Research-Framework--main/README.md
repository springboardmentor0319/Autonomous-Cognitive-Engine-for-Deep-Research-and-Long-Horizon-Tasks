# B3 OpenDeepResearcher : End‑to‑End Agentic Research Framework

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange)
![Docker](https://img.shields.io/badge/Container-Docker-blue)
![License](https://img.shields.io/badge/License-MIT-green)

**Deep Research From Scratch** is a robust, LangGraph-based autonomous research assistant. It orchestrates multiple AI agents to perform deep research by clarifying user intent, browsing the web (or local files via MCP), coordinating parallel sub-researchers, and compiling comprehensive final reports.

Unlike black-box tools, this project exposes the entire logic flow—from the "thinking" process to the final report generation—making it an ideal framework for building and understanding agentic systems.

---

## 📖 Table of Contents

- [Features](#-features)
- [Quick Setup](#-quick-setup)
- [Docker Setup](#-docker-setup)
- [Architecture & Workflow](#-architecture--workflow)
- [Module Walkthrough](#-module-walkthrough)
- [The Thinking Tool](#-the-thinking-tool)
- [Notebooks & Learning Path](#-notebooks--learning-path)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

- **Structured Scoping:** Clarifies ambiguities with the user before starting, ensuring the agent understands the task via Pydantic schema validation.
- **"Thinking" Mechanism:** A dedicated tool allows agents to pause, plan, and reflect, reducing hallucinations and "search thrash."
- **Hybrid Research:** Supports both live web search (Tavily) and local file system analysis (via Model Context Protocol).
- **Multi-Agent Orchestration:** A supervisor agent manages multiple sub-agents to research topics in parallel.
- **LangGraph Integration:** Fully inspectable state machines with graph visualization support.

---

## 🚀 Quick Setup

Follow these steps to get the researcher running with the default configuration.

1. Clone the repository:
   ```bash
   git clone https://github.com/amalsalilan/B3-OpenDeepResearcher-Agentic-LLM-Research-Framework-.git
   ```
2. Change into the project directory:
   ```bash
   cd B3-OpenDeepResearcher-Agentic-LLM-Research-Framework
   ```
3. Install Python dependencies with `uv` (installation guide: https://docs.astral.sh/uv/getting-started/installation/):
   ```bash
   uv sync
   ```
4. Copy the environment variable template (WSL command shown):
   ```bash
   cp .env.example .env
   ```
5. Open `.env` and fill in the required credentials:
   - `TAVILY_API_KEY`
   - `GOOGLE_API_KEY` (Gemini)
   - `LANGSMITH_API_KEY`
6. Start the LangGraph development server:
   ```bash
   uv run langgraph dev --allow-blocking
   ```

## 🐳 Docker Setup (Simple)

1. Install Docker Desktop: https://docs.docker.com/desktop/install/
2. Copy the sample env file:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your API keys.
4. Create the persistent checkpoint volume (one-time):
   ```bash
   docker volume create langgraph-checkpoints
   ```
   - This must exist before `docker compose up` because the compose file declares an external volume.
   - Verify it exists: `docker volume ls | grep langgraph-checkpoints`
   - Inspect (optional): `docker volume inspect langgraph-checkpoints`
   - If you ever need to recreate it: stop containers, then `docker volume rm langgraph-checkpoints` and run the create command again.
5. Build and start the containers:
   ```bash
   docker compose up --build
   ```
6. Wait for the logs to settle, then open:
   - Backend API docs: `http://127.0.0.1:2024`
   - Agent Chat UI: `http://127.0.0.1:3001`
7. Launch LangGraph Studio at `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`.
8. When you are done, stop everything with:
   ```bash
   docker compose down
   ```
## 🧠 Architecture & Workflow

The project exposes five runnable graphs to LangGraph Studio. The recommended demo path is:
`scope_research` → `research_agent` → `research_agent_supervisor` → `research_agent_full`.

### End‑to‑End Flow

1. **Scoping:** Clarify the request and generate a precise research brief.
2. **Research:** Run researcher(s) to gather, reflect, and compress findings.
3. **Supervision:** Coordinate parallel researchers on sub‑topics and aggregate their results.
4. **Report:** Produce a comprehensive final report from the brief and notes.

### Data Flow

The project relies on typed state objects passed between LangGraph nodes:

* **`AgentState`**: Carries conversation `messages`, the `research_brief`, supervisor routing logic, and the `final_report`.
* **`ResearcherState`**: Tracks `researcher_messages`, `compressed_research`, and `raw_notes` produced by a single researcher loop.
* **`SupervisorState`**: Tracks supervisor planning, the overall `research_brief`, and collected `notes`.

## 📦 Module Walkthrough

### 1. Scoping and Brief Generation
* **Module:** `src/deep_research_from_scratch/research_agent_scope.py`
* **Function:** Uses a structured output schema to decide if a clarifying question is needed. If the request is clear, it generates a detailed `research_brief` to contextually seed the supervisor.

### 2. Single Research Agent (Web Search)
* **Module:** `src/deep_research_from_scratch/research_agent.py`
* **Tools:** `tavily_search` and `think_tool`
* **Logic:**
    * **LLM Call:** Decides to search or answer.
    * **Tool Execution:** Executes search or thinking.
    * **Compression:** Once the loop halts, `compress_research` aggregates findings into a citation-ready block, explicitly filtering out internal reflections.

### 3. Research Agent (Local Files via MCP)
* **Module:** `src/deep_research_from_scratch/research_agent_mcp.py`
* **Purpose:** Enables deep research over local documents (repos, notes, datasets) using the Model Context Protocol (MCP) filesystem server.
* **Features:** Handles Windows/WSL path conversion and lazy client discovery.

### 4. Multi‑Agent Supervisor
* **Module:** `src/deep_research_from_scratch/multi_agent_supervisor.py`
* **Function:** The project manager. It takes the brief, plans (often via `think_tool`), and spawns multiple researchers in parallel (`ConductResearch`). It aggregates sub-agent results and decides when to finish.

### 5. Full Orchestration
* **Module:** `src/deep_research_from_scratch/research_agent_full.py`
* **Flow:** `clarify_with_user` → `write_research_brief` → `supervisor_subgraph` → `final_report_generation`.
* **Result:** Builds a writer prompt from the brief + aggregated notes and invokes a high‑context writer model to generate the final output.

## 📓 Notebooks & Learning Path

These notebooks explain how each component is built. See `notebooks/README.md` for kernel usage.

| Notebook | Graph Mapping | Description |
| :--- | :--- | :--- |
| `1_scoping.ipynb` | `scope_research` | Scoping and brief generation. |
| `2_research_agent.ipynb` | `research_agent` | Single researcher with web search & reflection. |
| `3_research_agent_mcp.ipynb` | `research_agent_mcp` | Research over local files via MCP. |
| `4_research_supervisor.ipynb` | `research_agent_supervisor` | Supervisor coordinating multiple researchers. |
| `5_full_agent.ipynb` | `research_agent_full` | End‑to‑end integration. |

## 🔧 Troubleshooting

* **API Keys:** Ensure `TAVILY_API_KEY` and an LLM provider key (e.g., `GOOGLE_API_KEY`) are set in `.env`.
* **LangGraph Studio:** Select the desired graph from the dropdown (see `langgraph.json` for names).
* **WSL and MCP:** Ensure Windows Node.js is available in WSL for MCP; the code converts WSL paths and launches `npx` appropriately.
* **Jupyter:** Always select the `.venv` kernel when running notebooks.