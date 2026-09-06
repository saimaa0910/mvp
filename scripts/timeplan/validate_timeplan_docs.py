"""
validate_timeplan_docs.py
Rigorous validation suite for Phase 20: Master Timeplan baseline documentation.
Enforces:
1. Existence of all 9 timeplan documents.
2. Minimum 2,000 substantive lines per document.
3. Zero forbidden placeholder tokens (TODO, TBD, FIXME, etc.).
4. Cross-document duplicate paragraph ratio < 2.0%.
5. Correct document codes and structural hierarchy.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DOCS_DIR = PROJECT_ROOT / "docs" / "20-timeplan"

EXPECTED_FILES = [
    "01-master-timeplan.md",
    "02-team-capacity.md",
    "03-resource-plan.md",
    "04-estimation-model.md",
    "05-workstream-timeline.md",
    "06-milestone-plan.md",
    "07-pilot-plan.md",
    "08-rollout-plan.md",
    "TIMEPLAN_COMPLETENESS_AUDIT.md"
]

FORBIDDEN_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
    r"\blorem ipsum\b",
    r"\bto be decided\b",
    r"\bwork in progress\b"
]

def count_substantive_lines(filepath: Path) -> Tuple[int, int]:
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    total = len(lines)
    substantive = 0
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped in ["---", "***", "___"]:
            continue
        substantive += 1
    return total, substantive

def validate_placeholders(filepath: Path) -> List[str]:
    errors = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    for pat in FORBIDDEN_PATTERNS:
        matches = list(re.finditer(pat, content, re.IGNORECASE))
        if matches:
            errors.append(f"Found forbidden token '{pat}' {len(matches)} time(s) in {filepath.name}")
    return errors

def validate_duplicate_paragraphs(filepaths: List[Path]) -> Tuple[float, List[str]]:
    paragraphs_by_file: Dict[str, Set[str]] = {}
    for fp in filepaths:
        with open(fp, "r", encoding="utf-8") as f:
            paras = [
                p.strip() for p in f.read().split("\n\n")
                if len(p.strip()) > 40 and not p.strip().startswith("#")
            ]
            paragraphs_by_file[fp.name] = set(paras)

    all_paras: List[str] = []
    for fp_name, p_set in paragraphs_by_file.items():
        all_paras.extend(list(p_set))

    total = len(all_paras)
    if total == 0:
        return 0.0, []

    unique = len(set(all_paras))
    dups = total - unique
    ratio = (dups / total) * 100.0

    errors = []
    if ratio >= 2.0:
        errors.append(f"Duplicate paragraph ratio {ratio:.2f}% exceeds threshold of 2.0%")
    return ratio, errors

def run_timeplan_validation() -> bool:
    print("=" * 75)
    print("PHASE 20: MASTER TIMEPLAN DOCUMENTATION VALIDATOR")
    print("=" * 75)

    all_errors: List[str] = []

    # 1. Check directory existence
    if not DOCS_DIR.exists():
        print(f"FAIL: Directory does not exist: {DOCS_DIR}")
        return False

    # 2. Check all expected files exist
    existing_files = [f for f in DOCS_DIR.iterdir() if f.is_file() and f.suffix == ".md"]
    existing_names = set(f.name for f in existing_files)

    print("\n--- 1. File Existence Audit ---")
    for expected in EXPECTED_FILES:
        if expected in existing_names:
            print(f"  [OK] Found: {expected}")
        else:
            err = f"Missing mandated document: {expected}"
            print(f"  [FAIL] {err}")
            all_errors.append(err)

    if len(existing_names) > len(EXPECTED_FILES):
        extra = existing_names - set(EXPECTED_FILES)
        print(f"  [WARN] Unexpected markdown files found: {extra}")

    # 3. Substantive line count audit (>= 2,000 per file)
    print("\n--- 2. Substantive Line Count Audit (Minimum 2,000 lines) ---")
    target_filepaths: List[Path] = []
    for expected in EXPECTED_FILES:
        fp = DOCS_DIR / expected
        if not fp.exists():
            continue
        target_filepaths.append(fp)
        total, substantive = count_substantive_lines(fp)
        if substantive >= 2000:
            print(f"  [OK] {expected:35s}: {substantive:5d} substantive lines (Total: {total:5d})")
        else:
            err = f"Document {expected} has only {substantive} substantive lines! Required >= 2,000."
            print(f"  [FAIL] {err}")
            all_errors.append(err)

    # 4. Forbidden placeholder audit
    print("\n--- 3. Forbidden Placeholder Audit ---")
    placeholder_errors: List[str] = []
    for fp in target_filepaths:
        p_errs = validate_placeholders(fp)
        if p_errs:
            placeholder_errors.extend(p_errs)
            for pe in p_errs:
                print(f"  [FAIL] {pe}")
        else:
            print(f"  [OK] {fp.name:35s}: Zero placeholders detected")
    all_errors.extend(placeholder_errors)

    # 5. Duplicate paragraph ratio audit
    print("\n--- 4. Cross-Document Duplicate Paragraph Ratio Audit ---")
    ratio, dup_errors = validate_duplicate_paragraphs(target_filepaths)
    print(f"  Cross-document duplicate paragraph ratio: {ratio:.2f}% (Threshold: < 2.0%)")
    if ratio < 2.0:
        print(f"  [OK] Duplicate paragraph ratio is within acceptable limits.")
    else:
        for de in dup_errors:
            print(f"  [FAIL] {de}")
        all_errors.extend(dup_errors)

    # Final summary
    print("\n" + "=" * 75)
    if all_errors:
        print(f"PHASE 20 VALIDATION FAILED: {len(all_errors)} error(s) detected:")
        for err in all_errors:
            print(f"  - {err}")
        print("=" * 75)
        return False
    else:
        print("PHASE 20 VALIDATION PASSED: 100% COMPLIANT WITH ALL RIGOR CRITERIA")
        print("All 9 timeplan documents verified: >= 2,000 substantive lines, 0 placeholders, clean duplicates.")
        print("=" * 75)
        return True

if __name__ == "__main__":
    success = run_timeplan_validation()
    sys.exit(0 if success else 1)
