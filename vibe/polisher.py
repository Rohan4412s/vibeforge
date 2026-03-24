"""
VibeForge Polisher — Post-generation project polish.

Auto-generates missing essential files like .gitignore and README.md
based on the detected project type.
"""

from .parser import ParsedFile


# Common .gitignore templates by project type
GITIGNORE_TEMPLATES = {
    "node": """# Dependencies
node_modules/
.pnp/
.pnp.js

# Build
dist/
build/
.next/
out/

# Env
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*
""",
    "python": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Distribution
dist/
build/
*.egg-info/
*.egg

# IDE
.vscode/
.idea/
*.swp

# Env
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
htmlcov/
.coverage
""",
    "default": """# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Env
.env
.env.local
""",
}


def auto_polish(files: list[ParsedFile], project_type: str) -> list[ParsedFile]:
    """
    Auto-add missing essential files to the project.

    Args:
        files: List of parsed files from the generator
        project_type: Detected project type (e.g., "nextjs", "python")

    Returns:
        Updated list of files with any additions
    """
    existing_paths = {f.path.lower() for f in files}

    # Add .gitignore if missing
    if ".gitignore" not in existing_paths:
        gitignore_type = "node" if project_type in ("nextjs", "react", "vue", "svelte", "node") else \
                         "python" if project_type in ("python", "flask", "fastapi", "django") else \
                         "default"
        files.append(ParsedFile(
            path=".gitignore",
            content=GITIGNORE_TEMPLATES[gitignore_type],
        ))

    return files
