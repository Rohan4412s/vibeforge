"""
VibeForge Templates — Built-in template hints for popular tech stacks.

These get injected into the planner prompt to guide the AI toward
best practices for each specific stack.
"""

TEMPLATES = {
    "nextjs": {
        "name": "Next.js 15",
        "description": (
            "Modern Next.js 15 app with App Router, TypeScript, and Tailwind CSS. "
            "Use the /app directory structure with layout.tsx, page.tsx, and loading.tsx. "
            "Include proper metadata exports for SEO. Use Server Components by default, "
            "mark client components with 'use client'. Use Geist font from next/font."
        ),
    },
    "react": {
        "name": "React + Vite",
        "description": (
            "React app scaffolded with Vite and TypeScript. "
            "Use functional components with hooks. Include react-router-dom for routing. "
            "Use CSS Modules or styled-components for styling. "
            "Include a proper vite.config.ts."
        ),
    },
    "flask": {
        "name": "Flask",
        "description": (
            "Python Flask web application with Jinja2 templates. "
            "Use blueprints for route organization. Include Flask-SQLAlchemy for database, "
            "Flask-Migrate for migrations. Use a proper app factory pattern (create_app). "
            "Include requirements.txt and a config.py."
        ),
    },
    "fastapi": {
        "name": "FastAPI",
        "description": (
            "Python FastAPI backend with automatic OpenAPI docs. "
            "Use Pydantic models for request/response validation. "
            "Include SQLModel or SQLAlchemy for database. "
            "Use dependency injection. Include proper requirements.txt, "
            "Dockerfile, and uvicorn config."
        ),
    },
    "python-cli": {
        "name": "Python CLI",
        "description": (
            "Python CLI application using Typer for commands and Rich for terminal output. "
            "Use pyproject.toml with hatchling build system. "
            "Include proper entry points in [project.scripts]. "
            "Add --help descriptions for all commands and options."
        ),
    },
    "express": {
        "name": "Express.js",
        "description": (
            "Node.js Express backend with TypeScript. "
            "Use proper middleware pattern, error handling, and route organization. "
            "Include dotenv for environment variables. "
            "Add a proper tsconfig.json and package.json with scripts."
        ),
    },
    "svelte": {
        "name": "SvelteKit",
        "description": (
            "SvelteKit application with TypeScript. "
            "Use the +page.svelte file-based routing convention. "
            "Include proper +layout.svelte, +error.svelte, and +server.ts files. "
            "Use Tailwind CSS for styling."
        ),
    },
    "vue": {
        "name": "Vue 3 + Vite",
        "description": (
            "Vue 3 application with Vite, TypeScript, and Composition API. "
            "Use script setup syntax. Include Vue Router and Pinia for state management. "
            "Use CSS scoped styles or Tailwind CSS."
        ),
    },
}


def get_template(name: str) -> dict | None:
    """Get a template by name."""
    return TEMPLATES.get(name.lower())


def list_templates() -> list[dict]:
    """List all available templates."""
    return [
        {"key": key, "name": t["name"], "description": t["description"][:80] + "..."}
        for key, t in TEMPLATES.items()
    ]
