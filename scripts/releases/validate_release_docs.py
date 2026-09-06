"""
validate_release_docs.py
Rigorous validation suite for Phase 19: Release Management documentation.
Enforces:
1. Existence of all 9 release documents.
2. Minimum 2,000 substantive lines per document.
3. Zero forbidden placeholder tokens (TODO, TBD, FIXME, etc.).
4. Presence of all 54 mandated sections in each release document.
5. Cross-document duplicate paragraph ratio < 2.0%.
6. Documentation-only safety tag on configuration snippets.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.releases.release_core_data import RELEASES_LIST, SECTION_NAMES_54

DOCS_DIR = PROJECT_ROOT / "docs" / "19-releases"

EXPECTED_FILES = [
    "release-00-foundation.md",
    "release-01-core-patient.md",
    "release-02-clinical.md",
    "release-03-pharmacy-lab-referral.md",
    "release-04-analytics-offline.md",
    "release-05-pilot.md",
    "release-06-production-scale.md",
    "release-07-ai-abdm.md",
    "RELEASE_COMPLETENESS_AUDIT.md"
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

def validate_54_sections(filepath: Path) -> List[str]:
    errors = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    for s_idx, s_name in enumerate(SECTION_NAMES_54, 1):
        expected_header = f"## {s_idx}. {s_name}"
        if expected_header not in content:
            errors.append(f"Missing mandated section in {filepath.name}: '{expected_header}'")
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

def run_release_validation() -> bool:
    print("=" * 75)
    print("PHASE 19: RELEASE MANAGEMENT DOCUMENTATION VALIDATOR")
    print("=" * 75)

    all_errors: List[str] = []

    # 1. Check directory existence
    if not DOCS_DIR.exists():
        print(f"FAIL: Directory does not exist: {DOCS_DIR}")
        return False

    # 2. Check expected files existence
    existing_fps: List[Path] = []
    for fname in EXPECTED_FILES:
        fp = DOCS_DIR / fname
        if not fp.exists():
            all_errors.append(f"Missing expected release document: {fname}")
        else:
            existing_fps.append(fp)

    if all_errors:
        for err in all_errors:
            print(f"ERROR: {err}")
        return False

    # 3. Check substantive line count & placeholders
    print(f"\n[1/4] Validating Line Counts and Placeholder Tokens across {len(existing_fps)} documents:")
    for fp in existing_fps:
        total, substantive = count_substantive_lines(fp)
        status_str = "PASS" if substantive >= 2000 else "FAIL"
        print(f"  - {fp.name:<38} | Total: {total:>5} | Substantive: {substantive:>5} | [{status_str}]")
        if substantive < 2000:
            all_errors.append(f"{fp.name} has only {substantive} substantive lines (minimum 2,000 required)")

        placeholder_errs = validate_placeholders(fp)
        if placeholder_errs:
            all_errors.extend(placeholder_errs)

    # 4. Check 54 mandated sections in release documents (release-00 to release-07)
    print("\n[2/4] Validating 54 Mandated Sections in Release Documents:")
    release_docs = [fp for fp in existing_fps if fp.name.startswith("release-")]
    for fp in release_docs:
        sec_errs = validate_54_sections(fp)
        if sec_errs:
            all_errors.extend(sec_errs)
            print(f"  - {fp.name:<38} | FAIL: {len(sec_errs)} missing sections")
        else:
            print(f"  - {fp.name:<38} | PASS: All 54 sections present")

    # 5. Check duplicate paragraph ratio across all release documents
    print("\n[3/4] Validating Cross-Document Paragraph Duplication:")
    dup_ratio, dup_errs = validate_duplicate_paragraphs(existing_fps)
    print(f"  - Duplicate paragraph ratio: {dup_ratio:.2f}% (Threshold: < 2.00%)")
    if dup_errs:
        all_errors.extend(dup_errs)

    # 6. Check documentation-only safety annotations on configuration snippets
    print("\n[4/4] Validating Documentation Safety Invariants:")
    for fp in existing_fps:
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
            if "openapi:" in content and "DOCUMENTATION-ONLY" not in content:
                all_errors.append(f"{fp.name} contains OpenAPI block without DOCUMENTATION-ONLY tag")

    print("\n" + "=" * 75)
    if all_errors:
        print(f"VALIDATION FAILED with {len(all_errors)} errors:")
        for err in all_errors:
            print(f"  - {err}")
        print("=" * 75)
        return False
    else:
        print("VALIDATION SUCCESS: All Phase 19 Release Documents pass 100% of quality gates!")
        print("=" * 75)
        return True

if __name__ == "__main__":
    success = run_release_validation()
    sys.exit(0 if success else 1)
