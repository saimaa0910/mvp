"""
github_gen_common.py
Shared formatting and line counting utilities for Phase 22: GitHub Governance.
Enforces strict substantive line counting, documentation-only annotations, and Markdown formatting.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

GITHUB_DOCS_DIR = PROJECT_ROOT / "docs" / "22-github"

def count_substantive_strict(content: str) -> int:
    """
    Counts substantive lines strictly excluding:
    - Blank lines
    - Markdown headings (starting with '#')
    - Horizontal rules ('---', '***', '___')
    """
    sub = 0
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped in ["---", "***", "___"]:
            continue
        sub += 1
    return sub

def write_github_doc(filename: str, content: str, min_substantive: int = 2000) -> Dict[str, Any]:
    """
    Writes a generated Markdown document into docs/22-github/, enforcing substantive line count
    and stripping trailing whitespace.
    """
    GITHUB_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_path = GITHUB_DOCS_DIR / filename

    cleaned_lines = [line.rstrip() for line in content.strip().splitlines()]
    final_content = "\n".join(cleaned_lines) + "\n"

    total = len(cleaned_lines)
    sub = count_substantive_strict(final_content)

    print(f"[docs/22-github/{filename}] Total lines: {total}, Substantive (excl. headings): {sub}")
    if sub < min_substantive:
        raise ValueError(
            f"CRITICAL ERROR: {filename} has only {sub} substantive lines (excl. headings)! "
            f"Minimum required is {min_substantive}."
        )

    target_path.write_text(final_content, encoding="utf-8")
    return {"total": total, "substantive": sub}

def format_mermaid_diagram(title: str, mermaid_code: str) -> List[str]:
    """Formats a Mermaid diagram block with proper title."""
    return [
        f"### Architecture Diagram: {title}",
        "```mermaid",
        mermaid_code.strip(),
        "```",
        ""
    ]

def format_documentation_example(title: str, lang: str, code_content: str) -> List[str]:
    """Formats a configuration specification example with mandatory DOCUMENTATION-ONLY annotations."""
    return [
        f"#### Specification Example: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        f"```{lang}",
        f"# DOCUMENTATION-ONLY CONFIGURATION: {title}",
        code_content.strip(),
        "```",
        ""
    ]

def format_metadata_block(
    doc_id: str,
    title: str,
    version: str,
    classification: str,
    status: str,
    domain: str,
    target_audience: str
) -> List[str]:
    """Formats an enterprise document control metadata block."""
    return [
        "| Governance Attribute | Specification Value |",
        "| :--- | :--- |",
        f"| **Document Identifier** | `{doc_id}` |",
        f"| **Document Title** | {title} |",
        f"| **Document Version** | `{version}` |",
        f"| **Security Classification** | `{classification}` |",
        f"| **Ratification Status** | `{status}` |",
        f"| **Program Domain** | {domain} |",
        f"| **Target Audience** | {target_audience} |",
        ""
    ]

def format_callout(alert_type: str, title: str, body: str) -> List[str]:
    """Formats a GitHub Flavored Markdown alert blockquote."""
    alert_type_clean = alert_type.upper()
    return [
        f"> [!{alert_type_clean}]",
        f"> **{title}**",
        f"> {body}",
        ""
    ]

def format_table(headers: List[str], rows: List[List[str]]) -> List[str]:
    """Formats a GitHub Flavored Markdown table."""
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join([":---"] * len(headers)) + " |"
    table_lines = [header_line, sep_line]
    for row in rows:
        table_lines.append("| " + " | ".join(row) + " |")
    table_lines.append("")
    return table_lines

