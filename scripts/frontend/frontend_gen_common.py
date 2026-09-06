"""
frontend_gen_common.py
Common generation utilities and quality enforcement for Phase 09 Frontend Engineering.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines

FE_DOCS_DIR = PROJECT_ROOT / "docs" / "09-frontend"

def write_fe_doc(filename: str, content: str, min_substantive: int = 2000) -> Dict[str, int]:
    """
    Writes content to docs/09-frontend/<filename>.
    Strips trailing whitespace from every line.
    Verifies that substantive line count >= min_substantive.
    """
    FE_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_path = FE_DOCS_DIR / filename

    # Strip trailing whitespace on each line
    cleaned_lines = [line.rstrip() for line in content.splitlines()]
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

def make_ts_interface(name: str, fields: List[Dict[str, str]], description: str = "") -> List[str]:
    """Generates a documentation-only TypeScript interface definition."""
    lines = []
    lines.append("```typescript")
    lines.append("// DOCUMENTATION-ONLY TYPESCRIPT")
    if description:
        lines.append(f"/** {description} */")
    lines.append(f"export interface {name} {{")
    for f in fields:
        opt = "?" if f.get("optional", False) else ""
        comment = f" // {f['comment']}" if "comment" in f else ""
        lines.append(f"  {f['name']}{opt}: {f['type']};{comment}")
    lines.append("}")
    lines.append("```")
    return lines

def make_fe_bdd_scenario(title: str, givens: List[str], when: str, thens: List[str]) -> List[str]:
    """Generates a BDD acceptance scenario in Gherkin syntax."""
    lines = []
    lines.append(f"#### Scenario: {title}")
    lines.append("```gherkin")
    lines.append("# DOCUMENTATION-ONLY EXAMPLE")
    for i, g in enumerate(givens):
        prefix = "Given" if i == 0 else "  And"
        lines.append(f"{prefix} {g}")
    lines.append(f"When {when}")
    for i, t in enumerate(thens):
        prefix = "Then" if i == 0 else "  And"
        lines.append(f"{prefix} {t}")
    lines.append("```")
    return lines
