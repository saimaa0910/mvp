"""
api_gen_common.py
Shared utilities for API documentation generation, formatting, and quality enforcement.
Phase 08: API Engineering Planning & Design Baseline.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines, find_duplicate_paragraphs

DOCS_DIR = PROJECT_ROOT / "docs" / "08-api"

def write_api_doc(filename: str, content: str) -> Dict[str, int]:
    """
    Writes an API documentation file under docs/08-api/
    Verifies that substantive lines >= 2,000.
    Strips all trailing whitespace to guarantee git diff --check cleanliness.
    """
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_path = DOCS_DIR / filename
    
    # Strip trailing whitespace on every line
    clean_lines = [line.rstrip() for line in content.splitlines()]
    clean_content = "\n".join(clean_lines) + "\n"
    
    stats = count_lines(clean_content)
    substantive = stats["substantive"]
    total = stats["total"]
    
    print(f"[{filename}] Total lines: {total}, Substantive: {substantive}")
    if substantive < 2000:
        raise ValueError(
            f"CRITICAL ERROR: {filename} has only {substantive} substantive lines! "
            f"Minimum required is 2,000."
        )
        
    with open(target_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(clean_content)
        
    return stats

def make_openapi_snippet(method: str, path: str, summary: str, tags: List[str], 
                         req_schema: str = None, resp_schema: str = None, 
                         status_codes: List[int] = None) -> List[str]:
    """Generates an OpenAPI 3.1 snippet with mandatory DOCUMENTATION-ONLY label."""
    if status_codes is None:
        status_codes = [200, 400, 401, 403, 404, 500]
    
    lines = [
        "```yaml",
        "# DOCUMENTATION-ONLY OPENAPI",
        f"openapi: 3.1.0",
        f"paths:",
        f"  {path}:",
        f"    {method.lower()}:",
        f"      summary: \"{summary}\"",
        f"      tags:",
    ]
    for tag in tags:
        lines.append(f"        - \"{tag}\"")
    lines.append(f"      operationId: \"{method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '').strip('_')}\"")
    
    if req_schema and method.upper() in ["POST", "PUT", "PATCH"]:
        lines.extend([
            f"      requestBody:",
            f"        required: true",
            f"        content:",
            f"          application/json:",
            f"            schema:",
            f"              $ref: \"#/components/schemas/{req_schema}\"",
        ])
        
    lines.append(f"      responses:")
    for code in status_codes:
        desc = "Successful operation" if code < 300 else "Client or server error"
        lines.append(f"        '{code}':")
        lines.append(f"          description: \"{desc}\"")
        lines.append(f"          content:")
        lines.append(f"            application/json:")
        lines.append(f"              schema:")
        if code < 300 and resp_schema:
            lines.append(f"                $ref: \"#/components/schemas/{resp_schema}\"")
        else:
            lines.append(f"                $ref: \"#/components/schemas/StandardErrorEnvelope\"")
    lines.append("```")
    return lines

def make_bdd_scenario(scenario_title: str, given_clauses: List[str], 
                      when_clause: str, then_clauses: List[str]) -> List[str]:
    """Generates a formatted BDD Acceptance Criteria block."""
    lines = [
        "```gherkin",
        "# DOCUMENTATION-ONLY EXAMPLE",
        f"Scenario: {scenario_title}",
    ]
    if given_clauses:
        lines.append(f"  Given {given_clauses[0]}")
        for g in given_clauses[1:]:
            lines.append(f"  And {g}")
    lines.append(f"  When {when_clause}")
    if then_clauses:
        lines.append(f"  Then {then_clauses[0]}")
        for t in then_clauses[1:]:
            lines.append(f"  And {t}")
    lines.append("```")
    return lines
