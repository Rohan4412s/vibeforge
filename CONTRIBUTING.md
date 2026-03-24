# Contributing to VibeForge ⚡

Thanks for wanting to contribute! Here's how to get started.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/Rohan4412s/vibeforge.git
cd vibeforge

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install in dev mode
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v
```

## What to Contribute

### 🟢 Easy (Great First Issues)
- Add a new template in `vibe/templates.py`
- Improve an existing prompt in `vibe/prompts.py`
- Fix typos or improve documentation

### 🟡 Medium
- Add support for a new LLM provider
- Improve the file parser in `vibe/parser.py`
- Add more auto-polish features

### 🔴 Advanced
- Build a web UI
- Add a VS Code extension
- Implement conversation mode (iterative vibe coding)

## Pull Request Process

1. Fork the repo and create your branch from `main`
2. Make your changes
3. Run the tests: `python -m pytest tests/ -v`
4. Submit a PR with a clear description of what you changed and why

## Code Style

- Use Python 3.10+ features
- Follow PEP 8
- Add type hints where possible
- Write docstrings for public functions

## Community

- Be respectful and inclusive
- Help newcomers
- Have fun vibing 🎶
