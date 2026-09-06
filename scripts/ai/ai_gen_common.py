"""
ai_gen_common.py
Shared utilities for generating Phase 14 AI/ML Engineering & Decision Support documentation.
Ensures documentation-only code labeling, Markdown formatting, and line-count mandates.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines

AI_DOCS_DIR = PROJECT_ROOT / "docs" / "14-ai"

def write_ai_doc(filename: str, content: str, min_substantive: int = 2000) -> Dict[str, Any]:
    """
    Writes a generated Markdown document into docs/14-ai/, enforcing substantive line count.
    """
    AI_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_path = AI_DOCS_DIR / filename

    final_content = content.strip() + "\n"
    stats = count_lines(final_content)
    sub = stats["substantive"]
    tot = stats["total"]

    print(f"[{filename}] Total lines: {tot}, Substantive: {sub}")
    if sub < min_substantive:
        raise ValueError(
            f"CRITICAL ERROR: {filename} has only {sub} substantive lines! "
            f"Minimum required is {min_substantive}."
        )

    target_path.write_text(final_content, encoding="utf-8")
    return stats

def format_python_example(title: str, py_content: str) -> List[str]:
    """Formats an ML pipeline / inference Python example with required documentation annotations."""
    return [
        f"### Model Specification Example: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```python",
        "# DOCUMENTATION-ONLY PYTHON",
        py_content.strip(),
        "```",
        "",
    ]

def format_formula_example(title: str, formula_content: str) -> List[str]:
    """Formats a mathematical formula or objective function with required documentation annotations."""
    return [
        f"### Mathematical Formulation: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```latex",
        formula_content.strip(),
        "```",
        "",
    ]

def format_yaml_example(title: str, yaml_content: str) -> List[str]:
    """Formats an ML serving / training configuration with required documentation annotations."""
    return [
        f"### Model Serving Configuration: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```yaml",
        "# DOCUMENTATION-ONLY CONFIGURATION",
        yaml_content.strip(),
        "```",
        "",
    ]

def format_json_example(title: str, json_content: str) -> List[str]:
    """Formats a model card / inference payload schema with required documentation annotations."""
    return [
        f"### Model Metadata Card: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```json",
        json_content.strip(),
        "```",
        "",
    ]
