"""
VibeForge CLI — Beautiful terminal interface for vibe coding.

Commands:
    vibeforge new "prompt"     — Generate a full app from a prompt
    vibeforge config set KEY VALUE — Set a config value
    vibeforge config show      — Show current config
    vibeforge templates        — List built-in templates
"""

import sys
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from typing import Optional

from . import __version__
from .config import load_config, set_value, get_api_key, get_model
from .agents import VibePipeline
from .scaffold import write_project, detect_project_type, get_next_steps, print_file_tree
from .polisher import auto_polish
from .parser import count_files
from .templates import get_template, list_templates, TEMPLATES

app = typer.Typer(
    name="vibeforge",
    help="⚡ Vibe code full apps in one prompt. Local-first. Powered by any LLM.",
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="rich",
)
config_app = typer.Typer(help="⚙️  Manage VibeForge configuration.", no_args_is_help=True)
app.add_typer(config_app, name="config")

console = Console()

BANNER = """
[bold cyan]
 ╦  ╦┬┌┐ ┌─┐╔═╗┌─┐┬─┐┌─┐┌─┐
 ╚╗╔╝│├┴┐├┤ ╠╣ │ │├┬┘│ ┬├┤ 
  ╚╝ ┴└─┘└─┘╚  └─┘┴└─└─┘└─┘
[/bold cyan]
[dim]Vibe code full apps. No BS. Local or API. Zero to shipped in minutes.[/dim]
"""


def show_banner():
    """Display the VibeForge banner."""
    console.print(BANNER)
    console.print(f"  [dim]v{__version__} • github.com/Rohan4412s/vibeforge[/dim]\n")


@app.command()
def new(
    prompt: str = typer.Argument(..., help="Describe the app you want to build"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="LLM model to use (e.g., groq/llama-3.3-70b-versatile)"),
    template: Optional[str] = typer.Option(None, "--template", "-t", help="Use a built-in template (e.g., nextjs, flask)"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory name"),
    no_polish: bool = typer.Option(False, "--no-polish", help="Skip the AI polishing step"),
    no_git: bool = typer.Option(False, "--no-git", help="Don't initialize a git repo"),
):
    """⚡ Vibe code a full app from one prompt."""
    show_banner()

    # Validate API key
    api_key = get_api_key()
    resolved_model = model or get_model()

    is_local = "ollama" in resolved_model.lower()

    if not api_key and not is_local:
        console.print(Panel(
            "[bold red]No API key found![/bold red]\n\n"
            "Set one with:\n"
            "  [cyan]vibeforge config set api_key YOUR_KEY[/cyan]\n\n"
            "Or set an environment variable:\n"
            "  [cyan]export VIBEFORGE_API_KEY=your_key[/cyan]\n\n"
            "Supported providers: Groq (free), OpenAI, Anthropic, Google Gemini\n"
            "For local models, use: [cyan]--model ollama/llama3.2[/cyan]",
            title="⚠️ Setup Required",
            border_style="red",
        ))
        raise typer.Exit(1)

    # Show what we're doing
    console.print(Panel(
        f"[bold white]{prompt}[/bold white]",
        title="🎯 Your Vibe",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print(f"  [dim]Model:[/dim] [cyan]{resolved_model}[/cyan]")
    if template:
        tmpl = get_template(template)
        if tmpl:
            console.print(f"  [dim]Template:[/dim] [cyan]{tmpl['name']}[/cyan]")
        else:
            console.print(f"  [yellow]⚠️ Unknown template '{template}', ignoring[/yellow]")
            template = None

    # Get template hint
    template_hint = ""
    if template:
        tmpl = get_template(template)
        if tmpl:
            template_hint = tmpl["description"]

    # Run the pipeline
    try:
        pipeline = VibePipeline(model=resolved_model)
        files, plan = pipeline.run(
            prompt=prompt,
            template_hint=template_hint,
            skip_polish=no_polish,
        )
    except Exception as e:
        console.print(f"\n[bold red]❌ Error calling LLM:[/bold red] {e}")
        console.print("[dim]Check your API key, model name, and internet connection.[/dim]")
        raise typer.Exit(1)

    if not files:
        console.print("\n[bold red]❌ No files were generated. Try again with a different prompt or model.[/bold red]")
        raise typer.Exit(1)

    # Auto-polish (add missing .gitignore, etc.)
    project_type = detect_project_type(files)
    files = auto_polish(files, project_type)

    # Determine output directory
    if output:
        project_name = output
    else:
        # Generate a clean project name from prompt
        project_name = prompt.lower()
        # Remove common words and special chars
        for char in "\"',.!?:;()[]{}":
            project_name = project_name.replace(char, "")
        project_name = "-".join(project_name.split()[:4])
        if not project_name:
            project_name = "vibeforge-project"

    # Write to disk
    project_path = write_project(
        project_dir=project_name,
        files=files,
        auto_git=not no_git,
    )

    # Show results
    console.print()
    console.print(Panel(
        f"[bold green]Project created successfully![/bold green]",
        title="🎉 Vibes Delivered",
        border_style="green",
    ))

    # File tree
    console.print()
    print_file_tree(files, project_name)

    # Stats
    counts = count_files(files)
    stats = " • ".join([f"{ext}: {count}" for ext, count in sorted(counts.items())])
    console.print(f"\n  [dim]{len(files)} files • {stats}[/dim]")
    console.print(f"  [dim]Type: {project_type}[/dim]")

    # Next steps
    next_steps = get_next_steps(project_type)
    console.print()
    steps_table = Table(
        show_header=False,
        box=box.SIMPLE,
        padding=(0, 2),
    )
    steps_table.add_column("Step", style="cyan")
    steps_table.add_column("Command", style="bold white")

    steps_table.add_row("1.", f"cd {project_name}")
    for i, step in enumerate(next_steps, start=2):
        steps_table.add_row(f"{i}.", step)

    console.print(Panel(steps_table, title="🚀 Next Steps", border_style="cyan"))
    console.print()
    console.print("[dim]Built with vibes by VibeForge ⚡ — Star us: github.com/Rohan4412s/vibeforge[/dim]")
    console.print()


@config_app.command("set")
def config_set(
    key: str = typer.Argument(..., help="Config key (e.g., model, api_key, temperature)"),
    value: str = typer.Argument(..., help="Config value"),
):
    """Set a configuration value."""
    set_value(key, value)
    console.print(f"[green]✅ Set [bold]{key}[/bold] = [bold]{value}[/bold][/green]")


@config_app.command("show")
def config_show():
    """Show current configuration."""
    show_banner()
    config = load_config()

    table = Table(
        title="⚙️  VibeForge Config",
        box=box.ROUNDED,
        show_lines=True,
    )
    table.add_column("Key", style="cyan", width=15)
    table.add_column("Value", style="white")

    for key, value in config.items():
        display_value = str(value)
        if key == "api_key" and value:
            display_value = value[:8] + "..." + value[-4:] if len(str(value)) > 12 else "***"
        elif value is None:
            display_value = "[dim]not set[/dim]"
        table.add_row(key, display_value)

    console.print(table)
    console.print()
    console.print("[dim]Set values with: vibeforge config set KEY VALUE[/dim]")


@app.command("templates")
def show_templates():
    """📋 List available built-in templates."""
    show_banner()

    table = Table(
        title="📋 Built-in Templates",
        box=box.ROUNDED,
        show_lines=True,
    )
    table.add_column("Key", style="cyan bold", width=12)
    table.add_column("Stack", style="white", width=15)
    table.add_column("Description", style="dim")

    for tmpl in list_templates():
        table.add_row(tmpl["key"], tmpl["name"], tmpl["description"])

    console.print(table)
    console.print()
    console.print("[dim]Use with: vibeforge new \"your idea\" --template nextjs[/dim]")


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Show version"),
):
    """⚡ VibeForge — Vibe code full apps in one prompt."""
    if version:
        console.print(f"vibeforge v{__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
