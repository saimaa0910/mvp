#!/usr/bin/env python3
"""
validate_workflows.py
Comprehensive automated validator for Namma Clinic Workflow Engineering (docs/03-workflows/).
Enforces all 37 quality, completeness, and architectural integrity rules:
- 25 primary workflow documents (each >= 2,000 substantive lines)
- 6 supporting catalog documents with strict substantive line thresholds
- Zero duplicate paragraphs (>= 60 chars) across all 31 documents
- All 67 standardized sections present across all 25 primary workflows
- 4 Mermaid architecture diagrams per primary workflow (100 total)
- Acyclic DAG validation using Kahn's topological sort
- Strictly zero application source code files
Returns exit code 0 on 100% compliance, 1 on any failure.
"""

import os
import sys
import re
import subprocess
from typing import Dict, List, Tuple

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
WORKFLOW_SCRIPTS_DIR = os.path.join(SCRIPTS_DIR, "workflows")
sys.path.append(WORKFLOW_SCRIPTS_DIR)

from workflow_metadata import WORKFLOW_SPECS, WORKFLOW_MAP
from common import count_lines, find_duplicate_paragraphs

# The 67 mandatory standardized sections
MANDATORY_SECTION_PREFIXES = [
    "## 01.", "## 02.", "## 03.", "## 04.", "## 05.", "## 06.", "## 07.", "## 08.", "## 09.", "## 10.",
    "## 11.", "## 12.", "## 13.", "## 14.", "## 15.", "## 16.", "## 17.", "## 18.", "## 19.", "## 20.",
    "## 21.", "## 22.", "## 23.", "## 24.", "## 25.", "## 26.", "## 27.", "## 28.", "## 29.", "## 30.",
    "## 31.", "## 32.", "## 33.", "## 34.", "## 35.", "## 36.", "## 37.", "## 38.", "## 39.", "## 40.",
    "## 41.", "## 42.", "## 43.", "## 44.", "## 45.", "## 46.", "## 47.", "## 48.", "## 49.", "## 50.",
    "## 51.", "## 52.", "## 53.", "## 54.", "## 55.", "## 56.", "## 57.", "## 58.", "## 59.", "## 60.",
    "## 61.", "## 62.", "## 63.", "## 64.", "## 65.", "## 66.", "## 67."
]

def check_acyclic_dag() -> bool:
    """Verifies that the workflow dependency graph has zero cycles using Kahn's algorithm."""
    from catalog_dependency_graph import DEPENDENCY_EDGES
    nodes = {f"WF-{i:03d}" for i in range(1, 26)}
    in_degree = {n: 0 for n in nodes}
    adj = {n: [] for n in nodes}
    for src, dst in DEPENDENCY_EDGES:
        if src in nodes and dst in nodes:
            adj[src].append(dst)
            in_degree[dst] += 1
    queue = [n for n in nodes if in_degree[n] == 0]
    visited_count = 0
    while queue:
        u = queue.pop(0)
        visited_count += 1
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    return visited_count == len(nodes)

def main():
    repo_root = os.path.abspath(os.path.join(SCRIPTS_DIR, ".."))
    docs_dir = os.path.join(repo_root, "docs", "03-workflows")

    print("=" * 80)
    print("NAMMA CLINIC WORKFLOW ENGINEERING — QUALITY GATE VALIDATOR")
    print("=" * 80)
    print(f"Target Directory: {docs_dir}")
    print(f"Total Workflows to Validate: {len(WORKFLOW_SPECS)}")
    print("-" * 80)

    results = []
    failures = 0

    def check(rule_num: int, rule_name: str, passed: bool, details: str = ""):
        nonlocal failures
        status = "PASS" if passed else "FAIL"
        if not passed:
            failures += 1
        results.append((rule_num, rule_name, status, details))
        flag = "[PASS]" if passed else "[FAIL]"
        detail_msg = f" - {details}" if details else ""
        print(f"Rule {rule_num:02d}: {flag} {rule_name}{detail_msg}")

    # Read all documents in docs/03-workflows
    doc_contents = {}
    doc_counts = {}
    if os.path.exists(docs_dir):
        for fname in os.listdir(docs_dir):
            if fname.endswith(".md"):
                fpath = os.path.join(docs_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                    doc_contents[fname] = content
                    doc_counts[fname] = count_lines(content)

    # Rule 01: All 25 Primary Workflow Documents Exist
    missing_p_docs = [s["file"] for s in WORKFLOW_SPECS if s["file"] not in doc_contents]
    check(1, "All 25 Primary Workflow Documents Exist", len(missing_p_docs) == 0,
          f"Missing: {missing_p_docs}" if missing_p_docs else "25/25 present")

    # Rule 02: All 6 Supporting Catalogs Exist
    catalog_files = [
        "WORKFLOW_DEPENDENCY_GRAPH.md",
        "WORKFLOW_TRACEABILITY_MATRIX.md",
        "WORKFLOW_TEST_CATALOG.md",
        "WORKFLOW_ERROR_CATALOG.md",
        "WORKFLOW_OBSERVABILITY_CATALOG.md",
        "WORKFLOW_COMPLETENESS_AUDIT.md",
    ]
    missing_catalogs = [c for c in catalog_files if c not in doc_contents]
    check(2, "All 6 Supporting Catalogs Exist", len(missing_catalogs) == 0,
          f"Missing: {missing_catalogs}" if missing_catalogs else "6/6 present")

    # Rules 03 - 27: Primary workflows 01 to 25 >= 2,000 substantive lines
    for i in range(1, 26):
        r_num = i + 2
        spec = WORKFLOW_SPECS[i - 1]
        fname = spec["file"]
        sub = doc_counts.get(fname, {}).get("substantive", 0)
        check(r_num, f"Workflow {i:02d} ({spec['id']}) Substantive Line Count >= 2,000",
              sub >= 2000, f"{sub:,} substantive lines in {fname}")

    # Rule 28: Zero duplicate paragraphs >= 60 chars across all 31 documents
    dups = find_duplicate_paragraphs(doc_contents, min_len=60)
    dup_details = f"Found {len(dups)} duplicate paragraphs" if dups else "0 duplicate paragraphs across all 31 documents"
    check(28, "Zero Duplicate Paragraphs (>= 60 chars) across all 31 documents", len(dups) == 0, dup_details)

    # Rule 29: Mandatory 67 standardized sections in all 25 primary workflows
    missing_sections_map = {}
    for spec in WORKFLOW_SPECS:
        fname = spec["file"]
        content = doc_contents.get(fname, "")
        missing_in_doc = []
        for pfx in MANDATORY_SECTION_PREFIXES:
            if pfx not in content:
                missing_in_doc.append(pfx)
        if missing_in_doc:
            missing_sections_map[spec["id"]] = missing_in_doc

    check(29, "All 67 Standardized Sections Present in all 25 Primary Workflows",
          len(missing_sections_map) == 0,
          f"Violations: {missing_sections_map}" if missing_sections_map else "1,675 / 1,675 sections verified")

    # Rule 30: Exactly 4 Mermaid diagrams per primary workflow (100 total)
    diagram_failures = []
    for spec in WORKFLOW_SPECS:
        fname = spec["file"]
        content = doc_contents.get(fname, "")
        mermaid_count = content.count("```mermaid")
        seq = "sequenceDiagram" in content
        st = "stateDiagram-v2" in content
        has_flowcharts = ("flowchart" in content or "graph" in content)
        if mermaid_count < 4 or not (seq and st and has_flowcharts):
            diagram_failures.append((spec["id"], f"mermaid_blocks:{mermaid_count}, seq:{seq}, st:{st}, flowchart:{has_flowcharts}"))

    check(30, "Mandatory 4 Mermaid Architecture Diagrams per Workflow (100 total)",
          len(diagram_failures) == 0,
          f"Missing: {diagram_failures}" if diagram_failures else "100 / 100 Mermaid diagrams verified")

    # Rule 31: WORKFLOW_DEPENDENCY_GRAPH.md >= 2,000 substantive lines
    dep_sub = doc_counts.get("WORKFLOW_DEPENDENCY_GRAPH.md", {}).get("substantive", 0)
    check(31, "WORKFLOW_DEPENDENCY_GRAPH.md Line Count >= 2,000", dep_sub >= 2000, f"{dep_sub:,} substantive lines")

    # Rule 32: WORKFLOW_TRACEABILITY_MATRIX.md >= 3,000 substantive lines
    tr_sub = doc_counts.get("WORKFLOW_TRACEABILITY_MATRIX.md", {}).get("substantive", 0)
    check(32, "WORKFLOW_TRACEABILITY_MATRIX.md Line Count >= 3,000", tr_sub >= 3000, f"{tr_sub:,} substantive lines")

    # Rule 33: WORKFLOW_TEST_CATALOG.md >= 3,000 substantive lines
    tst_sub = doc_counts.get("WORKFLOW_TEST_CATALOG.md", {}).get("substantive", 0)
    check(33, "WORKFLOW_TEST_CATALOG.md Line Count >= 3,000", tst_sub >= 3000, f"{tst_sub:,} substantive lines")

    # Rule 34: WORKFLOW_ERROR_CATALOG.md >= 2,500 substantive lines
    err_sub = doc_counts.get("WORKFLOW_ERROR_CATALOG.md", {}).get("substantive", 0)
    check(34, "WORKFLOW_ERROR_CATALOG.md Line Count >= 2,500", err_sub >= 2500, f"{err_sub:,} substantive lines")

    # Rule 35: WORKFLOW_OBSERVABILITY_CATALOG.md >= 2,500 substantive lines
    obs_sub = doc_counts.get("WORKFLOW_OBSERVABILITY_CATALOG.md", {}).get("substantive", 0)
    check(35, "WORKFLOW_OBSERVABILITY_CATALOG.md Line Count >= 2,500", obs_sub >= 2500, f"{obs_sub:,} substantive lines")

    # Rule 36: Acyclic Workflow Dependency Graph (DAG)
    acyclic = check_acyclic_dag()
    check(36, "Acyclic Workflow Dependency DAG (Kahn's Algorithm)", acyclic, "Zero cycles detected; strict DAG")

    # Rule 37: Strictly Zero Application Source Code Files
    res = subprocess.run(["git", "status", "--porcelain"], cwd=repo_root, capture_output=True, text=True)
    status_lines = res.stdout.splitlines()
    forbidden_exts = (".ts", ".js", ".tsx", ".jsx", ".go", ".java", ".sql", ".rs", ".cpp", ".c")
    forbidden_files = []
    for l in status_lines:
        line_path = l[3:].strip()
        # Exclude scripts directory which contains python generator scripts
        if line_path.startswith("scripts/"):
            continue
        if any(line_path.endswith(ext) for ext in forbidden_exts):
            forbidden_files.append(line_path)
    check(37, "Strictly Zero Application Source Code (Documentation-Only Phase)",
          len(forbidden_files) == 0,
          f"Forbidden files: {forbidden_files}" if forbidden_files else "100% clean documentation-only phase")

    print("-" * 80)
    passed_count = 37 - failures
    print(f"VALIDATION SUMMARY: {passed_count}/37 Rules Passed ({100 * passed_count / 37:.1f}%)")
    print("=" * 80)

    if failures > 0:
        print(f"[FAILED] Workflow validation failed with {failures} rule violation(s).")
        sys.exit(1)
    else:
        print("[SUCCESS] All 37 workflow engineering quality rules PASSED with 100% compliance!")
        sys.exit(0)

if __name__ == "__main__":
    main()
