# 🧠 Deep Research From Scratch — Setup Guide

This project is an **Autonomous Learning Agent** built with [LangGraph](https://github.com/langchain-ai/langgraph) and Google Gemini. It implements a full multi-agent research pipeline using the Feynman pedagogy and checkpoint verification, structured across 6 progressive Jupyter notebooks.

---

## 📋 Project Structure

```
Infosys_springboard_Project/
├── src/
│   └── deep_research_from_scratch/   # Core agent source modules
│       ├── research_agent.py
│       ├── research_agent_scope.py
│       ├── research_agent_mcp.py
│       ├── multi_agent_supervisor.py
│       ├── research_agent_full.py
│       ├── learning_agent.py
│       └── deep_research_agent.py
├── notebooks/                        # 6 step-by-step tutorial notebooks
│   ├── 1_scoping.ipynb
│   ├── 2_research_agent.ipynb
│   ├── 3_research_agent_mcp.ipynb
│   ├── 4_research_supervisor.ipynb
│   ├── 5_full_agent.ipynb
│   └── 6_checkpoint_agent.ipynb
├── .env.example                      # Template for environment variables
├── pyproject.toml                    # Project dependencies
├── langgraph.json                    # LangGraph graph registry
├── Dockerfile                        # Docker image definition
└── docker-compose.yml                # Docker Compose config
```

---

## 🔑 Prerequisites

Before you begin, get the following API keys:

| Service | Purpose | Get it at |
|---|---|---|
| **Google Gemini API Key** | Primary AI model | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| **Tavily API Key** | Web search for research agents | [tavily.com](https://tavily.com) |
| **LangSmith API Key** *(optional)* | Tracing and evaluation | [smith.langchain.com](https://smith.langchain.com) |

---

## ⚙️ Environment Setup

1. **Copy the example env file:**

   ```powershell
   copy .env.example .env
   ```

2. **Edit `.env`** and fill in your real API keys:

   ```env
   # Required — Google Gemini (primary model)
   GOOGLE_API_KEY=your_google_api_key_here

   # Required — Tavily (web search for research agents)
   TAVILY_API_KEY=your_tavily_api_key_here

   # Optional — LangSmith tracing
   LANGSMITH_API_KEY=your_langsmith_api_key_here
   LANGSMITH_TRACING=true
   LANGSMITH_PROJECT=deep_research_from_scratch
   ```

> ⚠️ **Never** commit your `.env` file. It is already listed in `.gitignore`.

---

## 🐳 Option 1: Docker (Recommended)

This is the simplest way — Docker bundles Python 3.11, Node.js, and `uv` for you.

### Prerequisites
- [Docker Desktop](https://docs.docker.com/get-docker/) installed and running

### Steps

```powershell
# 1. Build the Docker image (first time only)
docker-compose build

# 2. Start the container in the background
docker-compose up -d

# 3. View logs to confirm it started successfully
docker-compose logs -f
```

### Access the Services

| Service | URL |
|---|---|
| **LangGraph Studio** | https://smith.langchain.com/studio/?baseUrl=http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs |
| **API Root** | http://localhost:8000 |

### Useful Docker Commands

```powershell
# Stop the container
docker-compose down

# Rebuild from scratch (after code changes)
docker-compose down && docker-compose build --no-cache && docker-compose up -d

# Stop and remove all data volumes
docker-compose down -v
```

---

## 💻 Option 2: Local Installation (Windows)

Use this path if you prefer to run the project directly on your machine.

### Step 1 — Install Python 3.11+

Download from [python.org](https://www.python.org/downloads/) and verify:

```powershell
python --version   # Should show 3.11.x or higher
```

> ⚠️ During installation, check **"Add Python to PATH"**.

### Step 2 — Install `uv` (Package Manager)

`uv` is a fast Python package manager used by this project instead of pip.

```powershell
# Install uv using pip
pip install uv

# Verify
uv --version
```

### Step 3 — Install Node.js (for MCP notebooks)

Download from [nodejs.org](https://nodejs.org/en/download) (LTS version). Verify:

```powershell
node --version
npx --version
```

### Step 4 — Install Project Dependencies

```powershell
# This creates a virtual environment and installs all packages from pyproject.toml
uv sync
```

### Step 5 — Activate the Virtual Environment

```powershell
.venv\Scripts\activate
```

Your prompt should change to show `(.venv)`.

### Step 6 — Run the LangGraph Server

```powershell
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking
```

Then open LangGraph Studio at:
```
https://smith.langchain.com/studio/?baseUrl=http://localhost:8000
```

### Step 7 — Or Run Jupyter Notebooks

```powershell
# Run notebooks using uv (no need to activate the venv separately)
uv run jupyter notebook
```

This opens a browser window where you can open notebooks from the `notebooks/` folder.

---

## 📓 Notebook Learning Path

Run the notebooks in order for the best learning experience:

| # | Notebook | What You Learn |
|---|---|---|
| 1 | `1_scoping.ipynb` | User clarification, brief generation, structured output |
| 2 | `2_research_agent.ipynb` | ReAct agent loop, Tavily search, tool integration |
| 3 | `3_research_agent_mcp.ipynb` | Model Context Protocol (MCP), async tool execution |
| 4 | `4_research_supervisor.ipynb` | Multi-agent coordination, parallel research |
| 5 | `5_full_agent.ipynb` | End-to-end: Scope → Research → Write pipeline |
| 6 | `6_checkpoint_agent.ipynb` | Checkpoint verification, Feynman pedagogy |

---

## 🧩 LangGraph Graphs

The following graphs are registered in `langgraph.json` and available via the LangGraph Studio UI:

| Graph Name | Description |
|---|---|
| `scope_research` | Scoping and clarification agent |
| `research_agent` | Basic research agent with tools |
| `research_agent_mcp` | Research agent using MCP servers |
| `research_agent_supervisor` | Multi-agent supervisor orchestrator |
| `research_agent_full` | Full three-phase pipeline |
| `learning_agent` | Feynman-based learning agent |
| `deep_researcher` | Full deep research agent |

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| `RESOURCE_EXHAUSTED` from Gemini API | You've hit the free-tier quota. Wait or upgrade to a paid plan. Generate a new key at [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| `API key expired` | Generate a fresh key and update `.env` |
| `uv: command not found` | Run `pip install uv` and ensure your PATH is set |
| Port 8000 already in use | Stop other services, or change the port in `docker-compose.yml` |
| `ModuleNotFoundError` in notebooks | Make sure you ran `uv sync` and selected the `.venv` kernel in Jupyter |
| Docker not starting | Make sure Docker Desktop is running before running `docker-compose` commands |

---

## 📦 Key Dependencies

| Package | Purpose |
|---|---|
| `langgraph` | Graph-based agent orchestration |
| `langchain` + `langchain-google-genai` | LLM integration (Gemini) |
| `langchain-tavily` | Web search tool |
| `langchain-mcp-adapters` | MCP server integration |
| `langchain-groq` | Groq LLM support |
| `pydantic` | Structured data validation |
| `jupyter` + `ipykernel` | Interactive notebooks |
| `rich` | Beautiful terminal output |
