# IDRAK Onboarding

Feel free to send in your questions on our WhatsApp group. This README will explain how to set up this repo.

## Why Dev Containers

Everyone's machine is different. Different OS versions, Node versions, Python versions -- and that means code that works on one machine breaks on another. Dev Containers solve this by packaging the entire development environment into a container. When you open this repo, you're running the exact same environment as everyone else on the team. No setup friction, no "works on my machine.". This also allows us (founders) to test your code without hassle.


## Before You Start

You need two things:

**1. A container runtime**

Install one depending on your OS:

| Tool | Platform |
|---|---|
| [OrbStack](https://orbstack.dev) | macOS (recommended) |
| [Docker Desktop](https://www.docker.com/products/docker-desktop) | macOS or Windows |

**2. The Dev Containers extension for VS Code**

Install it here: [ms-vscode-remote.remote-containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)


## What to Expect

The `.devcontainer` folder in this repo is what tells VS Code to open the project inside a container instead of on your local machine.

When you open the repo in VS Code, you'll see a prompt in the bottom-right corner:

> "Reopen in Container"

Click it. VS Code will build and launch the container. This may take a few minutes the first time. Once it's done, your terminal is running inside the container with everything already installed. 


## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/IDRAK-Entreprises/idrak-onboarding.git
cd idrak-onboarding

# 2. Open in VS Code
code .

# → Click "Reopen in Container" when prompted
```

Once inside the container, you have a fresh Linux environment ready to go.



## Project Structure ( You can modify this structure )

```
.
├── .devcontainer/      # Container configuration (keep this as is, change other folders as you like)
├── backend/            # FastAPI app
└── frontend/           # Vue / Next.js app
```
