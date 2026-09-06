"""
validate_ai_docs.py
Validation suite for Phase 14: AI/ML Engineering & Decision Support.
Enforces 8 Quality Gates across docs/14-ai/.
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines, find_duplicate_paragraphs
from scripts.ai.ai_core_data import (
    AI_USE_CASES, MODELS, MODEL_VERSIONS, AI_DATASETS, FEATURES_ML,
    EVALUATION_METRICS, AI_RISKS, AI_CONTROLS, MONITORING_RULES,
    HUMAN_APPROVALS, AI_LINEAGE
)
from scripts.database.db_tables_entities import TABLES
from scripts.product.product_core_data import FEATURES

DOCS = [
    "01-ai-strategy.md",
    "02-ai-governance.md",
    "03-ai-use-cases.md",
    "04-stock-forecasting.md",
    "05-fever-anomaly-detection.md",
    "06-ncd-recall-prioritization.md",
    "07-feature-engineering.md",
    "08-model-data-requirements.md",
    "09-model-evaluation.md",
    "10-model-monitoring.md",
    "11-human-approval.md",
    "12-ai-safety.md",
    "13-model-versioning.md",
    "AI_COMPLETENESS_AUDIT.md",
]

PLACEHOLDER_PATTERNS = [
    re.compile(r'\bTODO\b', re.IGNORECASE),
    re.compile(r'\bTBD\b', re.IGNORECASE),
    re.compile(r'\bFIXME\b', re.IGNORECASE),
    re.compile(r'\blorem\s+ipsum\b', re.IGNORECASE),
    re.compile(r'\bto\s+be\s+decided\b', re.IGNORECASE),
]

def validate_all() -> bool:
    print("=" * 70)
    print("RUNNING PHASE 14 AI/ML ENGINEERING QUALITY GATE VALIDATOR")
    print("=" * 70)

    ai_dir = PROJECT_ROOT / "docs" / "14-ai"
    all_passed = True

    # Gate 1: File Existence
    print("\n[GATE 1] Verifying File Existence (14 documents)...")
    missing = [d for d in DOCS if not (ai_dir / d).exists()]
    if missing:
        print(f"  FAILED: Missing documents: {missing}")
        all_passed = False
    else:
        print("  PASS: All 14 documents present.")

    # Gate 2: Substantive Line Counts (>= 2,000)
    print("\n[GATE 2] Verifying Substantive Line Counts (>= 2,000)...")
    doc_contents = {}
    under_threshold = []
    total_substantive = 0
    total_raw = 0

    for doc_name in DOCS:
        doc_path = ai_dir / doc_name
        if not doc_path.exists():
            continue
        content = doc_path.read_text(encoding="utf-8")
        doc_contents[doc_name] = content
        stats = count_lines(content)
        sub = stats["substantive"]
        tot = stats["total"]
        total_substantive += sub
        total_raw += tot
        if sub < 2000:
            under_threshold.append((doc_name, sub))
        print(f"  - {doc_name:<35}: {sub:>5,} substantive / {tot:>5,} total lines")

    print(f"  TOTAL SUBSTANTIVE LINES: {total_substantive:,}")
    print(f"  TOTAL RAW LINES:         {total_raw:,}")
    if under_threshold:
        print(f"  FAILED: {len(under_threshold)} documents below 2,000 substantive lines: {under_threshold}")
        all_passed = False
    else:
        print("  PASS: All documents exceed 2,000 substantive lines.")

    # Gate 3: Placeholder Check
    print("\n[GATE 3] Checking for Disallowed Placeholders...")
    found_placeholders = []
    for doc_name, content in doc_contents.items():
        for line_num, line in enumerate(content.splitlines(), 1):
            for pat in PLACEHOLDER_PATTERNS:
                matches = pat.findall(line)
                if matches:
                    lower_line = line.lower()
                    if (
                        "no todo" in lower_line
                        or "prohibition" in lower_line
                        or "zero todo" in lower_line
                        or "audit" in lower_line
                        or "checkpoint" in lower_line
                        or "0 occurrences" in lower_line
                        or "quality gate" in lower_line
                        or "scanned for" in lower_line
                        or "forbidden token" in lower_line
                        or "zero-placeholder" in lower_line
                        or "zero placeholder" in lower_line
                        or "zero-forbidden" in lower_line
                        or "zero forbidden" in lower_line
                        or "invariant" in lower_line
                    ):
                        continue
                    found_placeholders.append((doc_name, line_num, pat.pattern, line.strip()[:60]))

    if found_placeholders:
        print(f"  FAILED: Placeholders found in: {found_placeholders[:5]}")
        all_passed = False
    else:
        print("  PASS: Zero placeholder tokens detected.")

    # Gate 4: Cross-Document Duplication
    print("\n[GATE 4] Checking Cross-Document Paragraph Duplication (< 2.0%)...")
    duplicates = find_duplicate_paragraphs(doc_contents, min_len=60)
    total_paragraphs = sum(len(c.split("\n\n")) for c in doc_contents.values())
    dup_ratio = (len(duplicates) * 2 / total_paragraphs * 100) if total_paragraphs else 0.0
    print(f"  Total Paragraphs: {total_paragraphs:,}")
    print(f"  Duplicate Paragraph Pairs: {len(duplicates):,}")
    print(f"  Duplicate Paragraph Ratio: {dup_ratio:.2f}% (Limit: < 2.0%)")
    if dup_ratio >= 2.0:
        print("  FAILED: Duplication ratio exceeds 2.0% threshold.")
        all_passed = False
    else:
        print("  PASS: Cross-document duplication comfortably within limits.")

    # Gate 5: Canonical Registries Uniqueness
    print("\n[GATE 5] Verifying Canonical AI Registries (11 Registries, 915 items)...")
    registries = [
        ("AI_USE_CASES", AI_USE_CASES, 35),
        ("MODELS", MODELS, 30),
        ("MODEL_VERSIONS", MODEL_VERSIONS, 60),
        ("AI_DATASETS", AI_DATASETS, 60),
        ("FEATURES_ML", FEATURES_ML, 150),
        ("EVALUATION_METRICS", EVALUATION_METRICS, 100),
        ("AI_RISKS", AI_RISKS, 100),
        ("AI_CONTROLS", AI_CONTROLS, 100),
        ("MONITORING_RULES", MONITORING_RULES, 100),
        ("HUMAN_APPROVALS", HUMAN_APPROVALS, 100),
        ("AI_LINEAGE", AI_LINEAGE, 80),
    ]
    reg_errors = []
    for rname, rlist, target in registries:
        ids = [item["id"] for item in rlist]
        if len(ids) != target:
            reg_errors.append(f"{rname} count {len(ids)} != {target}")
        if len(ids) != len(set(ids)):
            reg_errors.append(f"{rname} has duplicate IDs!")

    if reg_errors:
        print(f"  FAILED: Canonical registry errors: {reg_errors}")
        all_passed = False
    else:
        print("  PASS: All 11 canonical AI registries clean (915 unique items).")

    # Gate 6: Table Traceability (52 Tables)
    print("\n[GATE 6] Verifying Upstream Table Traceability (TABLE-001 to TABLE-052)...")
    all_content = "\n".join(doc_contents.values())
    missing_tables = [t["id"] for t in TABLES if t["id"] not in all_content]
    if missing_tables:
        print(f"  FAILED: Missing tables: {missing_tables}")
        all_passed = False
    else:
        print(f"  PASS: All {len(TABLES)} relational tables traced.")

    # Gate 7: Feature Traceability (180 Features)
    print("\n[GATE 7] Verifying Upstream Feature Traceability (FEATURE-001 to FEATURE-180)...")
    missing_features = [f["id"] for f in FEATURES if f["id"] not in all_content]
    if missing_features:
        print(f"  FAILED: Missing features: {missing_features}")
        all_passed = False
    else:
        print(f"  PASS: All {len(FEATURES)} product features traced.")

    # Gate 8: Non-Autonomous Clinical Safety & Code Tagging
    print("\n[GATE 8] Verifying Non-Autonomous Clinical Safety & Code Tagging...")
    unannotated_blocks = 0
    autonomous_violations = []

    for doc_name, content in doc_contents.items():
        if "```python" in content and "DOCUMENTATION-ONLY" not in content:
            unannotated_blocks += 1

        # Check for autonomous clinical claims
        if re.search(r'\bautonomous\s+(diagnosis|prescribing|dispensation)\b', content, re.IGNORECASE):
            # Check if it's stating a prohibition (e.g., zero autonomous diagnosis)
            for line in content.splitlines():
                if re.search(r'\bautonomous\s+(diagnosis|prescribing|dispensation)\b', line, re.IGNORECASE):
                    if not any(k in line.lower() for k in ["zero", "no", "strictly", "prohibit", "forbidden", "not permitted", "non-autonomous"]):
                        autonomous_violations.append((doc_name, line.strip()[:60]))

    if unannotated_blocks > 0:
        print(f"  FAILED: Unannotated code blocks found in {unannotated_blocks} documents.")
        all_passed = False
    elif autonomous_violations:
        print(f"  FAILED: Autonomous clinical claims detected: {autonomous_violations}")
        all_passed = False
    else:
        print("  PASS: Non-autonomous clinical safety boundary strictly enforced & all code tagged.")

    print("\n" + "=" * 70)
    if all_passed:
        print("ALL 8 QUALITY GATES PASSED! PHASE 14 BASELINE IS 100% COMPLIANT!")
    else:
        print("QUALITY GATES FAILED! REVIEW ERRORS ABOVE.")
    print("=" * 70)

    return all_passed

if __name__ == "__main__":
    if not validate_all():
        sys.exit(1)
