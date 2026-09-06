"""
timeplan_gen_common.py
Shared utilities for Phase 20: Master Timeplan documentation.
Enforces documentation-only annotations, Markdown formatting, and line-count mandates.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines

TIMEPLAN_DOCS_DIR = PROJECT_ROOT / "docs" / "20-timeplan"

def write_timeplan_doc(filename: str, content: str, min_substantive: int = 2000) -> Dict[str, Any]:
    """
    Writes a generated Markdown document into docs/20-timeplan/, enforcing substantive line count
    and stripping trailing whitespace.
    """
    TIMEPLAN_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_path = TIMEPLAN_DOCS_DIR / filename

    cleaned_lines = [line.rstrip() for line in content.strip().splitlines()]
    final_content = "\n".join(cleaned_lines) + "\n"
    
    total = len(cleaned_lines)
    sub = 0
    for line in cleaned_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped in ["---", "***", "___"]:
            continue
        sub += 1

    stats = {"total": total, "substantive": sub}
    print(f"[docs/20-timeplan/{filename}] Total lines: {total}, Substantive (excl. headings): {sub}")
    if sub < min_substantive:
        raise ValueError(
            f"CRITICAL ERROR: {filename} has only {sub} substantive lines (excl. headings)! "
            f"Minimum required is {min_substantive}."
        )

    target_path.write_text(final_content, encoding="utf-8")
    return stats

def format_yaml_example(title: str, yaml_content: str) -> List[str]:
    """Formats a configuration specification YAML example with required documentation annotations."""
    return [
        f"### Configuration Specification Example: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```yaml",
        "# DOCUMENTATION-ONLY CONFIGURATION",
        yaml_content.strip(),
        "```",
        "",
    ]

def format_json_example(title: str, json_content: str) -> List[str]:
    """Formats a data payload JSON example with required documentation annotations."""
    return [
        f"### Payload Specification Example: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```json",
        "// DOCUMENTATION-ONLY JSON",
        json_content.strip(),
        "```",
        "",
    ]

def format_mermaid_diagram(title: str, mermaid_content: str) -> List[str]:
    """Formats a mermaid diagram with documentation-only annotations."""
    return [
        f"### Schedule Architecture Diagram: {title}",
        "<!-- DOCUMENTATION-ONLY DIAGRAM -->",
        "```mermaid",
        mermaid_content.strip(),
        "```",
        "",
    ]
