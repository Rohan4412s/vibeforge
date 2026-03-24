"""
Tests for VibeForge file parser.
"""

from vibe.parser import parse_files, ParsedFile, count_files


def test_parse_xml_files():
    """Test parsing XML-tagged file blocks."""
    llm_output = '''Here is your project:

<file path="package.json">
{
  "name": "my-app",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev"
  },
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0"
  }
}
</file>

<file path="src/app/page.tsx">
export default function Home() {
  return (
    <main>
      <h1>Hello World</h1>
    </main>
  );
}
</file>

<file path="src/app/layout.tsx">
export default function RootLayout({ children }) {
  return (
    <html>
      <body>{children}</body>
    </html>
  );
}
</file>
'''
    files = parse_files(llm_output)
    assert len(files) == 3
    assert files[0].path == "package.json"
    assert '"next"' in files[0].content
    assert files[1].path == "src/app/page.tsx"
    assert "Hello World" in files[1].content
    assert files[2].path == "src/app/layout.tsx"


def test_parse_xml_single_quotes():
    """Test parsing XML with single-quoted paths."""
    llm_output = """<file path='index.html'>
<html><body>Hello</body></html>
</file>"""
    files = parse_files(llm_output)
    assert len(files) == 1
    assert files[0].path == "index.html"


def test_parse_xml_empty_output():
    """Test parsing empty output returns empty list."""
    files = parse_files("")
    assert files == []

    files = parse_files("No files here, just text.")
    assert files == []


def test_parse_markdown_fallback():
    """Test fallback markdown parsing."""
    llm_output = '''Here is your code:

```src/index.js
console.log("Hello");
```

```styles/main.css
body { margin: 0; }
```
'''
    files = parse_files(llm_output)
    assert len(files) == 2
    assert files[0].path == "src/index.js"
    assert files[1].path == "styles/main.css"


def test_count_files():
    """Test file counting by extension."""
    files = [
        ParsedFile("src/app.py", ""),
        ParsedFile("src/utils.py", ""),
        ParsedFile("package.json", ""),
        ParsedFile("index.js", ""),
        ParsedFile("README.md", ""),
    ]
    counts = count_files(files)
    assert counts[".py"] == 2
    assert counts[".json"] == 1
    assert counts[".js"] == 1
    assert counts[".md"] == 1


def test_path_normalization():
    """Test that paths are normalized."""
    llm_output = '''<file path="./src\\utils\\helper.js">
export const helper = () => {};
</file>'''
    files = parse_files(llm_output)
    assert len(files) == 1
    # Leading ./ should be removed, backslashes converted
    assert files[0].path == "src/utils/helper.js"
