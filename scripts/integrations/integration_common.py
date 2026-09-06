"""
integration_common.py
Shared utilities for Phase 15 Enterprise Integration Engineering documentation.
Enforces documentation-only code labeling, Markdown formatting, and line-count mandates.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines

INT_DOCS_DIR = PROJECT_ROOT / "docs" / "15-integrations"

def write_int_doc(filename: str, content: str, min_substantive: int = 2000) -> Dict[str, Any]:
    """
    Writes a generated Markdown document into docs/15-integrations/, enforcing substantive line count
    and stripping trailing whitespace.
    """
    INT_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_path = INT_DOCS_DIR / filename

    cleaned_lines = [line.rstrip() for line in content.strip().splitlines()]
    final_content = "\n".join(cleaned_lines) + "\n"
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
    """Formats an integration client Python example with required documentation annotations."""
    return [
        f"### Integration Specification Example: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```python",
        "# DOCUMENTATION-ONLY PYTHON",
        py_content.strip(),
        "```",
        "",
    ]

def format_json_example(title: str, json_content: str) -> List[str]:
    """Formats an integration payload JSON example with required documentation annotations."""
    return [
        f"### Interface Payload Example: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```json",
        "// DOCUMENTATION-ONLY JSON",
        json_content.strip(),
        "```",
        "",
    ]

def format_yaml_example(title: str, yaml_content: str) -> List[str]:
    """Formats an integration configuration YAML example with required documentation annotations."""
    return [
        f"### Configuration Specification Example: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```yaml",
        "# DOCUMENTATION-ONLY CONFIGURATION",
        yaml_content.strip(),
        "```",
        "",
    ]

def format_openapi_example(title: str, openapi_content: str) -> List[str]:
    """Formats an OpenAPI contract example with required documentation annotations."""
    return [
        f"### OpenAPI Interface Contract: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```yaml",
        "# DOCUMENTATION-ONLY OPENAPI",
        openapi_content.strip(),
        "```",
        "",
    ]
