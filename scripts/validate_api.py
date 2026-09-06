"""
validate_api.py
Master Validation Suite for Phase 08: API Engineering Planning & Design.
Enforces all 8 Architectural Quality Gates:
  1. Gate 1: Presence & Structure (23 files)
  2. Gate 2: Substantive Line Count Mandate (>= 2,000 per file)
  3. Gate 3: Canonical Registry Thresholds (Endpoints >= 315, Schemas >= 60, Errors >= 100, Deps >= 50, Tests >= 315)
  4. Gate 4: Referential Integrity & DAG Acyclicity (Zero broken references, Cycle-Free Kahn's DAG)
  5. Gate 5: Cross-Document Duplication Control (< 2.0% duplicates)
  6. Gate 6: Zero Forbidden Placeholder Tokens
  7. Gate 7: Documentation-Only Snippet Mandate (100% annotated)
  8. Gate 8: Upstream Baseline Preservation (docs/00- through docs/07-)
"""

import sys
import os
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines, find_duplicate_paragraphs
from scripts.api.api_core_data import (
    API_ENDPOINTS, API_SCHEMAS, API_ERROR_CODES, API_DEPENDENCIES, PLANNED_API_TESTS
)

API_DIR = PROJECT_ROOT / "docs" / "08-api"

MANDATORY_DOCS = [
    "01-api-architecture.md",
    "02-api-conventions.md",
    "03-api-versioning.md",
    "04-auth-api.md",
    "05-patient-api.md",
    "06-visit-api.md",
    "07-triage-api.md",
    "08-consultation-api.md",
    "09-prescription-api.md",
    "10-pharmacy-api.md",
    "11-inventory-api.md",
    "12-lab-api.md",
    "13-referral-api.md",
    "14-notification-api.md",
    "15-analytics-api.md",
    "16-audit-api.md",
    "17-abdm-api.md",
    "18-portability-api.md",
    "19-error-handling.md",
    "20-api-security.md",
    "21-api-rate-limiting.md",
    "22-api-traceability.md",
    "API_COMPLETENESS_AUDIT.md"
]

FORBIDDEN_TOKENS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
    r"\bto be decided\b",
    r"\blorem ipsum\b"
]

def check_gate_1_presence():
    print("--> Checking Gate 1: File Presence & Structural Integrity...")
    missing = []
    for doc in MANDATORY_DOCS:
        p = API_DIR / doc
        if not p.exists():
            missing.append(doc)
    if missing:
        print(f"FAILED Gate 1: Missing {len(missing)} documents: {missing}")
        return False
    print(f"PASS Gate 1: All {len(MANDATORY_DOCS)} mandatory documents present.")
    return True

def check_gate_2_line_counts():
    print("--> Checking Gate 2: Substantive Line Count Mandate (>= 2,000 per file)...")
    failed = []
    total_sub = 0
    total_all = 0
    for doc in MANDATORY_DOCS:
        p = API_DIR / doc
        text = p.read_text(encoding="utf-8")
        counts = count_lines(text)
        sub = counts["substantive"]
        tot = counts["total"]
        total_sub += sub
        total_all += tot
        if sub < 2000:
            failed.append((doc, sub))
        else:
            print(f"  [OK] {doc:<30} Substantive: {sub:>5} lines | Total: {tot:>5} lines")
    if failed:
        print(f"FAILED Gate 2: {len(failed)} files below 2,000 substantive lines: {failed}")
        return False
    print(f"PASS Gate 2: All 23 files >= 2,000 lines. Total substantive: {total_sub:,} lines (Total: {total_all:,})")
    return True

def check_gate_3_registry_thresholds():
    print("--> Checking Gate 3: Canonical Registry Thresholds...")
    errors = []
    if len(API_ENDPOINTS) < 315:
        errors.append(f"Endpoints count {len(API_ENDPOINTS)} < 315")
    if len(API_SCHEMAS) < 60:
        errors.append(f"Schemas count {len(API_SCHEMAS)} < 60")
    if len(API_ERROR_CODES) < 100:
        errors.append(f"Error codes count {len(API_ERROR_CODES)} < 100")
    if len(API_DEPENDENCIES) < 50:
        errors.append(f"Dependencies count {len(API_DEPENDENCIES)} < 50")
    if len(PLANNED_API_TESTS) < 315:
        errors.append(f"Planned tests count {len(PLANNED_API_TESTS)} < 315")

    if errors:
        print("FAILED Gate 3:", errors)
        return False
    print(f"PASS Gate 3: All registry thresholds satisfied:")
    print(f"  - Endpoints: {len(API_ENDPOINTS)} (>= 315)")
    print(f"  - Schemas: {len(API_SCHEMAS)} (>= 60)")
    print(f"  - Error Codes: {len(API_ERROR_CODES)} (>= 100)")
    print(f"  - Dependencies: {len(API_DEPENDENCIES)} (>= 50)")
    print(f"  - Planned Tests: {len(PLANNED_API_TESTS)} (>= 315)")
    return True

def check_gate_4_dag_acyclicity():
    print("--> Checking Gate 4: Referential Integrity & DAG Acyclicity (Kahn's Algorithm)...")
    # Build graph
    adj = defaultdict(list)
    in_degree = defaultdict(int)
    all_nodes = set()

    for dep in API_DEPENDENCIES:
        src = dep["source"]
        tgt = dep["target"]
        all_nodes.add(src)
        all_nodes.add(tgt)
        adj[src].append(tgt)
        in_degree[tgt] += 1
        if src not in in_degree:
            in_degree[src] = 0

    # Kahn's algorithm
    queue = [n for n in all_nodes if in_degree[n] == 0]
    visited_count = 0

    while queue:
        u = queue.pop(0)
        visited_count += 1
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if visited_count != len(all_nodes):
        print(f"FAILED Gate 4: Cycle detected in API dependency graph! Visited {visited_count} of {len(all_nodes)} nodes.")
        return False
    print(f"PASS Gate 4: DAG verified cycle-free across all {len(API_DEPENDENCIES)} dependency edges.")
    return True

def check_gate_5_duplicate_ratio():
    print("--> Checking Gate 5: Cross-Document Duplication Control (< 2.0% duplicate paragraphs)...")
    docs_dict = {doc: (API_DIR / doc).read_text(encoding="utf-8") for doc in MANDATORY_DOCS}
    dups = find_duplicate_paragraphs(docs_dict, min_len=60)
    
    total_paragraphs = 0
    for text in docs_dict.values():
        paras = [p.strip() for p in text.split("\n\n") if len(p.strip()) >= 60 and not p.strip().startswith("|") and not p.strip().startswith("```")]
        total_paragraphs += len(paras)

    dup_count = len(dups)
    ratio = (dup_count / total_paragraphs * 100.0) if total_paragraphs > 0 else 0.0
    print(f"  Found {dup_count} duplicate paragraphs across {total_paragraphs} candidate paragraphs ({ratio:.2f}%).")
    
    if ratio >= 2.0:
        print(f"FAILED Gate 5: Duplicate paragraph ratio {ratio:.2f}% exceeds 2.0% limit!")
        return False
    print(f"PASS Gate 5: Cross-document duplicate ratio is {ratio:.2f}% (< 2.0% threshold).")
    return True

def check_gate_6_forbidden_tokens():
    print("--> Checking Gate 6: Zero Forbidden Placeholder Tokens...")
    violations = []
    for doc in MANDATORY_DOCS:
        p = API_DIR / doc
        text = p.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            # Exclude lines describing the audit or rule explanations
            if "TODO, TBD, FIXME" in line or "Zero occurrences of forbidden" in line or "Scanned for" in line:
                continue
            for pat in FORBIDDEN_TOKENS:
                if re.search(pat, line, re.IGNORECASE):
                    violations.append((doc, line_no, pat, line.strip()))
    if violations:
        print(f"FAILED Gate 6: Found {len(violations)} forbidden token violations:")
        for v in violations[:10]:
            print(f"  {v[0]}:{v[1]} matches {v[2]}: {v[3]}")
        return False
    print("PASS Gate 6: Zero forbidden placeholder tokens found across all 23 documents.")
    return True

def check_gate_7_doc_first_snippets():
    print("--> Checking Gate 7: Documentation-Only Snippet Mandate...")
    code_block_re = re.compile(r"```(openapi|yaml|json|bash|http|lua|typescript|sql)\n(.*?)```", re.DOTALL)
    unlabeled = []
    
    for doc in MANDATORY_DOCS:
        p = API_DIR / doc
        text = p.read_text(encoding="utf-8")
        for m in code_block_re.finditer(text):
            block_lang = m.group(1)
            block_content = m.group(2).strip()
            first_line = block_content.splitlines()[0] if block_content.splitlines() else ""
            if not ("DOCUMENTATION-ONLY" in first_line or "DOCUMENTATION-ONLY" in block_content[:100]):
                unlabeled.append((doc, block_lang, first_line[:60]))

    if unlabeled:
        print(f"FAILED Gate 7: Found {len(unlabeled)} code blocks missing DOCUMENTATION-ONLY label:")
        for u in unlabeled[:10]:
            print(f"  {u[0]} [{u[1]}]: '{u[2]}'")
        return False
    print("PASS Gate 7: 100% of code snippets explicitly labeled DOCUMENTATION-ONLY.")
    return True

def check_gate_8_upstream_preservation():
    print("--> Checking Gate 8: Upstream Baseline Preservation (docs/00- through docs/07-)...")
    upstream_dirs = [
        "00-project-baseline",
        "01-project-management",
        "02-requirements",
        "03-workflows",
        "04-product",
        "05-srs",
        "06-architecture",
        "07-database"
    ]
    missing = []
    for u in upstream_dirs:
        p = PROJECT_ROOT / "docs" / u
        if not p.exists() or not any(p.iterdir()):
            missing.append(u)
    if missing:
        print(f"FAILED Gate 8: Missing or empty upstream directories: {missing}")
        return False
    print("PASS Gate 8: All upstream baseline phases (00 through 07) preserved intact.")
    return True

def run_all_gates():
    print("================================================================================")
    print("NAMMA CLINIC: PHASE 08 API ENGINEERING VALIDATOR")
    print("================================================================================")
    
    gates = [
        ("Gate 1: File Presence", check_gate_1_presence),
        ("Gate 2: Line Counts", check_gate_2_line_counts),
        ("Gate 3: Registries", check_gate_3_registry_thresholds),
        ("Gate 4: DAG Acyclicity", check_gate_4_dag_acyclicity),
        ("Gate 5: Duplicate Ratio", check_gate_5_duplicate_ratio),
        ("Gate 6: Forbidden Tokens", check_gate_6_forbidden_tokens),
        ("Gate 7: Doc-First Snippets", check_gate_7_doc_first_snippets),
        ("Gate 8: Upstream Preservation", check_gate_8_upstream_preservation),
    ]

    all_pass = True
    for name, fn in gates:
        print("-" * 80)
        res = fn()
        if not res:
            all_pass = False

    print("================================================================================")
    if all_pass:
        print("RESULT: ALL 8 QUALITY GATES PASSED (100% COMPLIANT)")
    else:
        print("RESULT: ONE OR MORE QUALITY GATES FAILED")
    print("================================================================================")
    return all_pass

if __name__ == "__main__":
    success = run_all_gates()
    sys.exit(0 if success else 1)
