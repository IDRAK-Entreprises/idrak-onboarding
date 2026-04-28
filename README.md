# IDRAK Onboarding

Starter project for new applicants — FastAPI backend + Vue / Next.js frontend, fully containerised with VS Code Dev Containers.

---

## Prerequisites

| Tool | Platform |
|---|---|
| [OrbStack](https://orbstack.dev) | macOS (recommended) |
| [Docker Desktop](https://www.docker.com/products/docker-desktop) | macOS or Windows |

> Install **one** of the above, then install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension in VS Code.

---

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/IDRAK-Entreprises/idrak-onboarding.git
cd idrak-onboarding

# 2. Open in VS Code, then reopen in container
code .
# → VS Code will prompt: "Reopen in Container" — click it
```

Once inside the container:

```bash
# Backend (FastAPI) — from /workspace/backend
uvicorn main:app --reload --port 8000

# Frontend (Vue / Next.js) — from /workspace/frontend
npm run dev
```

Ports `8000` and `3000` are forwarded automatically.

---

## Project Structure

```
.
├── .devcontainer/      # Dev Container config
├── backend/            # FastAPI app
└── frontend/           # Vue / Next.js app
```
