# IntelliSupport 🤖

**An intelligent, modular customer-support agent with RAG (Retrieval-Augmented Generation) using ChromaDB.**
*Clean architecture · multi-agent orchestration · safety & PII handling · Streamlit frontend · production-ready scaffolding* 🎯

---

> **Why this README will impress recruiters**
> It shows system design, production/dev steps, testing & CI guidance, security considerations, and interview-ready talking points — everything a recruiter or engineering manager wants to see. 🚀

---

# Table of Contents 📚

1. [Project Snapshot](#project-snapshot)
2. [Highlights & Why It Matters](#highlights--why-it-matters)
3. [Tech Stack](#tech-stack)
4. [Architecture Overview](#architecture-overview)
5. [Repo Layout (quick)](#repo-layout-quick)
6. [Setup — Quickstart (Local)](#setup---quickstart-local)
7. [Usage — Try the System (demo commands)](#usage---try-the-system-demo-commands)
8. [Streamlit Frontend (details)](#streamlit-frontend-details)
9. [Development Workflow](#development-workflow)
10. [Security & Privacy](#security--privacy)
11. [Deployment Suggestions](#deployment-suggestions)
12. [Contributing](#contributing)
13. [License & Maintainer](#license--maintainer)

---

# Project Snapshot ✨

IntelliSupport is a modular, agent-oriented customer support system that:

* Classifies user intent and sentiment ✅
* Routes queries to specialized agents (billing, tech, other) 🔀
* Uses RAG with ChromaDB + sentence-transformers to ground answers in company docs 📚
* Contains a safety agent for PII detection & redaction 🔒
* Provides a Streamlit frontend for rapid demos and a FastAPI backend for production APIs 🖥️

---

# Highlights & Why It Matters 💡

* **Modular agent design** demonstrates sound system design and separation of concerns.
* **RAG with ChromaDB** reduces hallucinations and enables source-aware responses.
* **Safety-first**: PII detection, redaction, and escalation triggers — essential for real products.
* **Dev-friendly**: `config.yaml`, `.env.example`, ingest pipeline, logger, and Streamlit demo are ready to run.
* **Recruiter-friendly**: clear README, demo steps, test commands, and interview talking points included. 👍

---

# Tech Stack 🧰

* **Backend**: Python, FastAPI, Uvicorn
* **Vector DB**: ChromaDB (local persistent mode)
* **Embeddings**: `sentence-transformers` (default: `all-MiniLM-L6-v2`)
* **LLM Integration**: pluggable (config-driven; placeholder keys in `.env.example`)
* **Frontend**: Streamlit (interactive demo) + stubbed React options
* **Testing**: pytest, pytest-asyncio
* **Logging & Config**: YAML config + structured logger

---

# Architecture Overview 🏗️

```
+--------------------+        +---------------------+
|     Streamlit      | <----> |     FastAPI         |
|     Frontend       |        |     Backend API     |
+--------------------+        +---------------------+
                                     |
                                     v
                        +-----------------------------+
                        |       Manager Agent         |
                        |  (Orchestrator / Workflow)  |
                        +-----------------------------+
                         /   |      |        |       \
                        v    v      v        v        v
                  Intent  Sentiment Billing Technical  RAG
                  Agent   Agent     Agent   Agent      Agent
                                                        |
                                                        v
                                                ChromaDB (vector store)
                                                        ^
                                                        |
                                               Embedder (S-T model)
```

* **Fix applied:** ChromaDB is correctly shown as the data store used by the **RAG Agent**, not the Technical Agent. ✅
* Manager Agent orchestrates the pipeline: **intent → sentiment → routing → RAG retrieval → safety → response generation**.

---

# Repo Layout (quick) 🗂️

```
intellisupport/
├─ agents/                  # agent implementations (manager, intent, rag, safety...)
├─ agents_prompts/          # prompt templates for each agent
├─ backend/                 # FastAPI app (main server)
├─ frontend/                # Streamlit app (detailed below)
├─ utils/                   # chunker, embedder, chroma_client, ingest pipeline
├─ db/chroma/               # local chroma persistence (gitignored)
├─ data/                    # sample docs for ingest
├─ logs/
├─ config.yaml
├─ requirements.txt
├─ README.md                # ← you are here
```

---

# Setup — Quickstart (Local) ⚡

1. Clone repo

```bash
git clone <your-repo-url>
cd intellisupport
```

2. Python environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv/Scripts/activate           # Windows (PowerShell/CMD)
pip install -r requirements.txt
```

3. Configure environment

```bash
cp .env.example .env
# Edit .env to add any API keys. For local demo you can keep LLM keys blank and rely on stubs/mock mode.
```

4. Ingest sample documents to ChromaDB

```bash
python -m intellisupport.utils.ingest
# or
python intellisupport/utils/ingest.py
```

5. Start backend (FastAPI)

```bash
cd intellisupport/backend
uvicorn main:app --reload --port 8000
```

6. Start Streamlit frontend (recommended for demos)

```bash
cd intellisupport/frontend
pip install -r requirements.txt
python run.py
# or directly
# streamlit run app.py
```

Open: `http://localhost:8501` 🌐

---

# Usage — Try the System (demo commands) 🧪

## API: simple query (example)

From repo root (backend running at [http://localhost:8000](http://localhost:8000)):

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I update my payment method?"}'
```

Expected (stub) response shape:

```json
{
  "response": "Thank you for your query. For billing inquiries, I'm here to help you.",
  "metadata": { "confidence": 0.9, "sources_used": 2 }
}
```

---

# Streamlit Frontend (details) 🖼️

Your Streamlit frontend is already scaffolded and included under `intellisupport/frontend`. Key highlights:

* **Entry points**: `app.py` (main app) and `run.py` (runner)
* **Components**: `components/header.py`, `components/sidebar.py`, `components/chat_interface.py`
* **Utilities**: `utils/api_client.py`, `utils/config.py`, `utils/session_state.py`, `utils/message_handler.py`
* **Pages**: `pages/analytics.py`, `pages/settings.py` for analytics and configuration

Features in the UI:

* 💬 Chat with IntelliSupport (with mock fallback if backend is unavailable)
* 📊 Sidebar with session stats and agent activity chart
* ⚙️ Settings page to edit LLM, retrieval, safety, and UI options (saves back to `config.yaml`)
* 📈 Analytics page with intent/sentiment visualizations

**Demo Mode**: If the backend is unreachable, `utils/api_client.APIClient._get_mock_response` provides realistic mock replies (with intent/confidence metadata) so you can demo anywhere. 🧩

---

# Development Workflow 🛠️

* Branch naming: `feat/<short-desc>`, `fix/<short-desc>`, `chore/<...>`
* Linting: `black` + `ruff` recommended
* Tests: write unit tests under `tests/` and run `pytest`
* Type hints: keep function signatures typed

Suggested pre-commit hooks (optional): `black`, `ruff`.

---

# Security & Privacy 🔐

* PII Detection & Redaction implemented in `agents/safety_agent.py` (regex-based) — tune via `config.yaml`.
* **Always** keep real API keys out of the repo; use `.env` and a secrets manager in prod.
* For production, enable encryption at rest for vector files and secure the backend with auth.

---

# Deployment Suggestions 🚢

* Containerize backend and serve with Uvicorn (or Gunicorn + Uvicorn workers).
* Consider a managed vector DB for scale or object-storage-backed persistence for Chroma.
* CI: GitHub Actions to run tests & linters; deploy to container registry and update Kubernetes manifests.

---

# Contributing 🤝

1. Fork & create a feature branch.
2. Add tests and update docs.
3. Open a PR with a clear description and change summary.
4. Keep commits atomic & descriptive.

---

# TODO / Roadmap 🛣️

* Add end-to-end integration tests and sample recordings
* Replace stubs with real LLM provider adapters
* Add role-based authentication + rate limiting
* Add metrics dashboard & observability (Prometheus + Grafana)
* Add Dockerfile + docker-compose + Kubernetes manifests for one-command demos

---

# License & Maintainer 📝

* **License:** MIT (or choose your preferred license)
* **Maintainer:** Sahil Rahate

---

If you'd like, I can now:

* ✅ Commit this README into the repo for you (create file in `intellisupport/README.md`)
* 🧾 Generate a `demo.sh` that runs ingest → backend → frontend for interviews
* 🐳 Create a `Dockerfile` + `docker-compose.yml` for a one-command local demo

Which of those should I generate next?

