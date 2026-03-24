"""
VibeForge Agents — Multi-agent pipeline for vibe coding.

Pipeline:
    User Prompt → [Planner] → Plan → [Coder] → Code → [Polisher] → Polished Code
"""

from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from rich.markdown import Markdown

from .llm import call_llm, call_llm_simple
from .prompts import PLANNER_PROMPT, CODER_PROMPT, POLISHER_PROMPT, TEMPLATE_HINT
from .parser import parse_files, ParsedFile

console = Console()


class VibePipeline:
    """
    Orchestrates the multi-agent vibe coding pipeline.

    Usage:
        pipeline = VibePipeline(model="groq/llama-3.3-70b-versatile")
        files = pipeline.run("Build a Twitter clone with Next.js")
    """

    def __init__(self, model: str = None, temperature: float = 0.7):
        self.model = model
        self.temperature = temperature

    def run(
        self,
        prompt: str,
        template_hint: str = "",
        skip_polish: bool = False,
    ) -> tuple[list[ParsedFile], str]:
        """
        Run the full vibe coding pipeline.

        Args:
            prompt: User's natural language app description
            template_hint: Optional template context to inject
            skip_polish: Skip the polishing step

        Returns:
            Tuple of (list of ParsedFile, plan_text)
        """
        # Step 1: Plan
        plan = self._plan(prompt, template_hint)

        # Step 2: Code
        files = self._code(plan, prompt)

        if not files:
            console.print("[bold red]❌ Failed to parse any files from the AI output.[/bold red]")
            console.print("[dim]This can happen if the LLM didn't follow the output format. Try again or use a different model.[/dim]")
            return [], plan

        # Step 3: Polish (optional)
        if not skip_polish and len(files) > 0:
            files = self._polish(files)

        return files, plan

    def _plan(self, prompt: str, template_hint: str = "") -> str:
        """Run the planner agent."""
        console.print()
        with console.status("[bold cyan]🧠 Planning your project architecture...[/bold cyan]", spinner="dots"):
            system = PLANNER_PROMPT
            if template_hint:
                system += "\n" + TEMPLATE_HINT.format(template_description=template_hint)

            plan = call_llm(
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": f"Build this app:\n\n{prompt}"},
                ],
                model=self.model,
                temperature=self.temperature,
                max_tokens=4000,
            )

        console.print(Panel(
            Markdown(plan),
            title="[bold blue]📋 Project Plan[/bold blue]",
            border_style="blue",
            padding=(1, 2),
        ))
        return plan

    def _code(self, plan: str, original_prompt: str) -> list[ParsedFile]:
        """Run the coder agent."""
        console.print()
        with console.status("[bold green]⚡ Generating your codebase...[/bold green]", spinner="dots"):
            code_output = call_llm(
                messages=[
                    {"role": "system", "content": CODER_PROMPT},
                    {"role": "user", "content": (
                        f"Original user request: {original_prompt}\n\n"
                        f"Project plan:\n{plan}\n\n"
                        f"Now generate the COMPLETE codebase following the plan above. "
                        f"Use the <file path=\"...\">content</file> XML format for every file."
                    )},
                ],
                model=self.model,
                temperature=self.temperature,
                max_tokens=16000,
            )

        files = parse_files(code_output)
        console.print(f"[bold green]✅ Generated {len(files)} files[/bold green]")
        return files

    def _polish(self, files: list[ParsedFile]) -> list[ParsedFile]:
        """Run the polisher agent to improve code quality."""
        console.print()
        with console.status("[bold magenta]✨ Polishing your code...[/bold magenta]", spinner="dots"):
            # Build a summary of existing files for the polisher
            file_summary = ""
            for f in files:
                file_summary += f'\n<file path="{f.path}">\n{f.content}\n</file>\n'

            polish_output = call_llm(
                messages=[
                    {"role": "system", "content": POLISHER_PROMPT},
                    {"role": "user", "content": (
                        f"Here is the generated codebase. Review and improve it:\n{file_summary}"
                    )},
                ],
                model=self.model,
                temperature=0.3,  # Lower temp for more precise edits
                max_tokens=16000,
            )

        polished_files = parse_files(polish_output)

        if polished_files:
            # Merge polished files with originals (polished versions override)
            file_map = {f.path: f for f in files}
            for pf in polished_files:
                file_map[pf.path] = pf
            files = list(file_map.values())
            console.print(f"[bold magenta]✨ Polished {len(polished_files)} files[/bold magenta]")
        else:
            console.print("[dim]Polisher had no improvements — code looks good![/dim]")

        return files
