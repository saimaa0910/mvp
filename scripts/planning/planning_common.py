"""
planning_common.py
Shared utilities for Phase 17 Master Planning and Phase 18 Sprint Execution documentation.
Enforces documentation-only annotations, Markdown formatting, and line-count mandates.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines

PLANNING_DOCS_DIR = PROJECT_ROOT / "docs" / "17-planning"
SPRINTS_DOCS_DIR = PROJECT_ROOT / "docs" / "18-sprints"

def write_planning_doc(filename: str, content: str, min_substantive: int = 2000) -> Dict[str, Any]:
    """
    Writes a generated Markdown document into docs/17-planning/, enforcing substantive line count
    and stripping trailing whitespace.
    """
    PLANNING_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_path = PLANNING_DOCS_DIR / filename

    cleaned_lines = [line.rstrip() for line in content.strip().splitlines()]
    final_content = "\n".join(cleaned_lines) + "\n"
    stats = count_lines(final_content)
    sub = stats["substantive"]
    tot = stats["total"]

    print(f"[docs/17-planning/{filename}] Total lines: {tot}, Substantive: {sub}")
    if sub < min_substantive:
        raise ValueError(
            f"CRITICAL ERROR: {filename} has only {sub} substantive lines! "
            f"Minimum required is {min_substantive}."
        )

    target_path.write_text(final_content, encoding="utf-8")
    return stats

def write_sprint_doc(filename: str, content: str, min_substantive: int = 2000) -> Dict[str, Any]:
    """
    Writes a generated Markdown document into docs/18-sprints/, enforcing substantive line count
    and stripping trailing whitespace.
    """
    SPRINTS_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_path = SPRINTS_DOCS_DIR / filename

    cleaned_lines = [line.rstrip() for line in content.strip().splitlines()]
    final_content = "\n".join(cleaned_lines) + "\n"
    stats = count_lines(final_content)
    sub = stats["substantive"]
    tot = stats["total"]

    print(f"[docs/18-sprints/{filename}] Total lines: {tot}, Substantive: {sub}")
    if sub < min_substantive:
        raise ValueError(
            f"CRITICAL ERROR: {filename} has only {sub} substantive lines! "
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

def format_python_example(title: str, py_content: str) -> List[str]:
    """Formats a python example with required documentation annotations."""
    return [
        f"### Implementation Script Example: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```python",
        "# DOCUMENTATION-ONLY PYTHON",
        py_content.strip(),
        "```",
        "",
    ]
