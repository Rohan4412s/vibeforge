<div align="center">

# ⚡ VibeForge

### Vibe code full apps in one terminal command.

**Local-first. No paid subscriptions. Powered by Ollama or any LLM.**

[![PyPI version](https://img.shields.io/pypi/v/vibeforge?color=blue&label=pypi)](https://pypi.org/project/vibeforge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/Rohan4412s/vibeforge?style=social)](https://github.com/Rohan4412s/vibeforge)

<br />

```bash
pip install vibeforge
vibeforge new "Twitter clone with Next.js, Tailwind, Supabase auth, real-time feed"
```

<!-- Add your demo GIF here -->
<!-- ![VibeForge Demo](examples/demo.gif) -->

*One prompt. Full project. Real files. Working code.*

</div>

---

## 🤔 What is VibeForge?

**Vibe coding** is the art of describing what you want in plain English and letting AI write all the code. No boilerplate. No copy-pasting snippets. Just vibes.

VibeForge is an **open-source CLI** that takes your idea and generates a complete, production-ready project — with proper directory structure, working code in every file, git history, and polished output.

Unlike paid tools (Cursor, Bolt.new, Lovable), VibeForge runs **locally**, supports **any LLM**, and is **100% free**.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **Multi-Agent Pipeline** | Planner → Coder → Polisher — three AI agents work in sequence |
| 📁 **Real File Output** | Generates actual files and directories, not a code dump |
| 🔌 **Any LLM** | Ollama (local/free), Groq (free tier), OpenAI, Anthropic, Gemini |
| 🎨 **Beautiful CLI** | Rich terminal UI with spinners, file trees, and color-coded output |
| 🔀 **Auto Git** | Initializes a repo with a clean initial commit |
| ✨ **Auto Polish** | Adds .gitignore, README, error handling automatically |
| 📋 **Built-in Templates** | Next.js, React, Flask, FastAPI, Vue, Svelte, Express — more coming |
| ⚡ **Zero Config** | Works out of the box — just set your API key |

## 🚀 Quick Start

### 1. Install

```bash
pip install vibeforge
```

### 2. Set your LLM (pick one)

**Free with Groq (recommended for speed):**
```bash
vibeforge config set api_key gsk_your_groq_api_key
vibeforge config set model groq/llama-3.3-70b-versatile
```

**Free with Ollama (local, private):**
```bash
# Install Ollama from ollama.ai, then:
ollama pull llama3.2
vibeforge config set model ollama/llama3.2
```

**OpenAI (GPT-5.4):**
```bash
vibeforge config set api_key sk-your_openai_key
vibeforge config set model gpt-5.4
# Also: gpt-5.4-mini, gpt-5.4-nano
```

**Anthropic (Claude 4.6):**
```bash
vibeforge config set api_key sk-ant-your_key
vibeforge config set model claude-sonnet-4-6
# Also: claude-opus-4-6-20260205
```

**Google Gemini (3.1):**
```bash
vibeforge config set api_key your_gemini_key
vibeforge config set model gemini/gemini-3.1-pro
# Also: gemini/gemini-3.1-flash-lite
```

**DeepSeek:**
```bash
vibeforge config set api_key your_deepseek_key
vibeforge config set model deepseek/deepseek-chat
```

### 3. Vibe!

```bash
vibeforge new "A beautiful landing page for a SaaS product with pricing table and testimonials"
```

## 📖 Usage

### Generate a project

```bash
# Basic usage
vibeforge new "portfolio website with dark mode and animations"

# Use a specific template
vibeforge new "todo app with authentication" --template nextjs

# Use a specific model
vibeforge new "REST API for a blog" --model gpt-5.4

# Custom output directory
vibeforge new "chat application" --output my-chat-app

# Skip the polishing step (faster)
vibeforge new "calculator app" --no-polish
```

### Configuration

```bash
# Show current config
vibeforge config show

# Set values
vibeforge config set model groq/llama-3.3-70b-versatile
vibeforge config set api_key your_api_key
vibeforge config set temperature 0.7
```

### Templates

```bash
# List available templates
vibeforge templates
```

Available templates:

| Template | Stack |
|----------|-------|
| `nextjs` | Next.js 15 + App Router + Tailwind |
| `react` | React + Vite + TypeScript |
| `flask` | Flask + SQLAlchemy + Jinja2 |
| `fastapi` | FastAPI + Pydantic + SQLModel |
| `express` | Express.js + TypeScript |
| `vue` | Vue 3 + Vite + Composition API |
| `svelte` | SvelteKit + TypeScript |
| `python-cli` | Typer + Rich CLI |

## 🏗️ How It Works

```
Your Prompt
    │
    ▼
┌─────────┐     ┌─────────┐     ┌──────────┐
│ Planner  │ ──→ │  Coder  │ ──→ │ Polisher │
│  Agent   │     │  Agent  │     │  Agent   │
└─────────┘     └─────────┘     └──────────┘
    │                │                │
    ▼                ▼                ▼
  Plan          Raw Files       Polished Files
                                     │
                                     ▼
                              ┌──────────────┐
                              │ Write to Disk │
                              │  + Git Init   │
                              └──────────────┘
```

1. **Planner** analyzes your prompt and designs the architecture, tech stack, and file structure
2. **Coder** generates complete, working code for every file
3. **Polisher** reviews the code, fixes bugs, adds error handling and best practices
4. **Scaffold** writes real files to disk, creates directories, and initializes git

## 🌟 Examples

```bash
# Full-stack web app
vibeforge new "Airbnb clone with Next.js 15, Prisma, Stripe payments, and map view"

# Backend API
vibeforge new "GraphQL API for an e-commerce store with auth, products, orders" --template fastapi

# CLI tool
vibeforge new "CLI tool that converts CSV files to JSON with filtering" --template python-cli

# Landing page
vibeforge new "Stunning dark-mode landing page for an AI startup with animations"

# Game
vibeforge new "Snake game in the browser with score tracking and sound effects"
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick ideas to contribute:**
- Add new templates (Django, Rust, Go, etc.)
- Improve prompts for better code output
- Add support for more LLM providers
- Build a web UI / VS Code extension

## 📜 License

MIT — see [LICENSE](LICENSE) for details.

## ⭐ Star History

If VibeForge helped you ship something, drop us a star! It helps others discover the project.

[![Star History Chart](https://api.star-history.com/svg?repos=Rohan4412s/vibeforge&type=Date)](https://star-history.com/#Rohan4412s/vibeforge&Date)

---

<div align="center">

**Built with vibes** ⚡

[Report Bug](https://github.com/Rohan4412s/vibeforge/issues) · [Request Feature](https://github.com/Rohan4412s/vibeforge/issues) · [Discussions](https://github.com/Rohan4412s/vibeforge/discussions)

</div>
