"""
VibeForge Parser — Extracts individual files from LLM output.

The LLM generates code in XML format:
    <file path="src/index.js">
    console.log("Hello");
    </file>

This parser extracts those blocks into a list of (filepath, content) tuples
that can be written to disk by the scaffold module.
"""

import re
from dataclasses import dataclass


@dataclass
class ParsedFile:
    """Represents a single file extracted from LLM output."""
    path: str
    content: str


def parse_files(llm_output: str) -> list[ParsedFile]:
    """
    Parse LLM output and extract file blocks.

    Tries XML format first, falls back to markdown fenced code blocks.

    Args:
        llm_output: Raw string output from the LLM

    Returns:
        List of ParsedFile objects with path and content
    """
    files = _parse_xml_files(llm_output)
    if files:
        return files

    # Fallback: try markdown format
    files = _parse_markdown_files(llm_output)
    if files:
        return files

    return []


def _parse_xml_files(output: str) -> list[ParsedFile]:
    """
    Parse XML-tagged file blocks.

    Format:
        <file path="relative/path/to/file.ext">
        file contents
        </file>
    """
    pattern = r'<file\s+path=["\']([^"\']+)["\']\s*>(.*?)</file>'
    matches = re.findall(pattern, output, re.DOTALL)

    files = []
    for path, content in matches:
        # Clean up the content — remove leading/trailing blank lines
        content = content.strip("\n")
        # Ensure consistent line endings
        content = content.replace("\r\n", "\n")
        # Normalize the path separators
        path = path.strip().replace("\\", "/")
        # Remove leading ./ if present
        if path.startswith("./"):
            path = path[2:]

        files.append(ParsedFile(path=path, content=content))

    return files


def _parse_markdown_files(output: str) -> list[ParsedFile]:
    """
    Fallback parser for markdown fenced code blocks with filenames.

    Formats supported:
        ```filename.ext
        content
        ```

        ```language:filename.ext
        content
        ```

        **filename.ext**
        ```
        content
        ```
    """
    files = []

    # Pattern 1: ```lang:path/to/file.ext or ```path/to/file.ext
    pattern1 = r'```(?:\w+:)?([^\n`]+\.\w+)\n(.*?)```'
    matches = re.findall(pattern1, output, re.DOTALL)
    for path, content in matches:
        path = path.strip().replace("\\", "/")
        if "/" in path or "." in path:
            files.append(ParsedFile(path=path, content=content.strip("\n")))

    if files:
        return files

    # Pattern 2: **filename** followed by code block
    pattern2 = r'\*\*([^\*]+\.\w+)\*\*\s*\n```\w*\n(.*?)```'
    matches = re.findall(pattern2, output, re.DOTALL)
    for path, content in matches:
        path = path.strip().replace("\\", "/")
        files.append(ParsedFile(path=path, content=content.strip("\n")))

    return files


def count_files(files: list[ParsedFile]) -> dict:
    """
    Count files by extension for display purposes.

    Returns:
        Dict mapping extension to count, e.g. {".py": 3, ".js": 5}
    """
    counts = {}
    for f in files:
        ext = "." + f.path.rsplit(".", 1)[-1] if "." in f.path else "other"
        counts[ext] = counts.get(ext, 0) + 1
    return counts
