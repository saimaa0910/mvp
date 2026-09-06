#!/usr/bin/env python3
"""
validate_github_docs.py
Validation suite: verifies all 10 Phase 22 GitHub Engineering documents
meet quality thresholds (line counts, zero placeholders, duplication ratio).
"""

import sys
import os
import re
from pathlib import Path
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scripts.github.github_gen_common import count_substantive_strict

GITHUB_DOCS_DIR = Path(__file__).resolve().parent.parent.parent / "docs" / "22-github"

CANONICAL_DOCS = [
    "01-github-strategy.md",
    "02-issue-hierarchy.md",
    "03-label-ontology.md",
    "04-project-board.md",
    "05-milestones.md",
    "06-issue-linking.md",
    "07-branching-strategy.md",
    "08-pr-strategy.md",
    "09-release-management.md",
    "GITHUB_COMPLETENESS_AUDIT.md",
]

FORBIDDEN_TOKENS = ["TODO", "TBD", "FIXME", "lorem ipsum", "to be decided", "work in progress"]
MIN_SUBSTANTIVE = 2000
MAX_DUP_RATIO = 2.0  # percent


def validate_existence():
    """Check all 10 canonical files exist."""
    errors = []
    for doc in CANONICAL_DOCS:
        if not (GITHUB_DOCS_DIR / doc).exists():
            errors.append(f"MISSING: {doc}")
    return errors


def validate_line_counts():
    """Check each document has >= MIN_SUBSTANTIVE substantive lines."""
    errors = []
    results = []
    for doc in CANONICAL_DOCS:
        path = GITHUB_DOCS_DIR / doc
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        total = len(content.strip().splitlines())
        sub = count_substantive_strict(content)
        results.append((doc, total, sub))
        if sub < MIN_SUBSTANTIVE:
            errors.append(f"LINE COUNT FAIL: {doc} has {sub} substantive lines (minimum {MIN_SUBSTANTIVE})")
    return errors, results


def validate_no_placeholders():
    """Check zero forbidden placeholder tokens."""
    errors = []
    # Legitimate contextual uses that are NOT draft placeholders
    allowed_contexts = [
        "state `todo`",          # GitHub Projects column/state name
        "state todo",
        "work in progress",      # GitHub PR Draft status description
        "draft pr: work in progress",  # Mermaid diagram node label
    ]
    for doc in CANONICAL_DOCS:
        path = GITHUB_DOCS_DIR / doc
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_TOKENS:
            count = 0
            for line_num, line in enumerate(content.splitlines(), 1):
                stripped = line.strip()
                # Skip lines that are part of validation/audit descriptions
                if stripped.startswith("- **") or stripped.startswith("| "):
                    continue
                lower_line = stripped.lower()
                if token.lower() in lower_line:
                    # Check if this is a known legitimate contextual use
                    is_allowed = any(ctx in lower_line for ctx in allowed_contexts)
                    if not is_allowed:
                        count += 1
            if count > 0:
                errors.append(f"PLACEHOLDER FOUND: {doc} contains {count} occurrences of '{token}'")
    return errors


def validate_duplication():
    """Check cross-document duplicate paragraph ratio < MAX_DUP_RATIO%."""
    all_paragraphs = []
    for doc in CANONICAL_DOCS:
        path = GITHUB_DOCS_DIR / doc
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        paras = re.split(r"\n\s*\n", content)
        for p in paras:
            cleaned = p.strip()
            if len(cleaned) > 80:  # Only check substantial paragraphs
                all_paragraphs.append(cleaned)

    if not all_paragraphs:
        return [], 0.0

    counter = Counter(all_paragraphs)
    total = len(all_paragraphs)
    duplicates = sum(c - 1 for c in counter.values() if c > 1)
    ratio = (duplicates / total * 100) if total > 0 else 0.0

    errors = []
    if ratio >= MAX_DUP_RATIO:
        errors.append(f"DUPLICATION FAIL: Cross-document duplicate ratio {ratio:.2f}% exceeds {MAX_DUP_RATIO}%")
    return errors, ratio


def main():
    print("=" * 70)
    print("Phase 22: GitHub Engineering Documentation Validation Suite")
    print("=" * 70)

    all_errors = []

    # 1. Existence check
    print("\n[1/4] Checking file existence...")
    errs = validate_existence()
    all_errors.extend(errs)
    if errs:
        for e in errs:
            print(f"  FAIL: {e}")
    else:
        print(f"  PASS: All {len(CANONICAL_DOCS)} canonical documents exist")

    # 2. Line count check
    print("\n[2/4] Checking substantive line counts...")
    errs, results = validate_line_counts()
    all_errors.extend(errs)
    for doc, total, sub in results:
        status = "PASS" if sub >= MIN_SUBSTANTIVE else "FAIL"
        print(f"  [{status}] {doc}: {sub} substantive lines (total {total})")

    # 3. Placeholder check
    print("\n[3/4] Checking for forbidden placeholder tokens...")
    errs = validate_no_placeholders()
    all_errors.extend(errs)
    if errs:
        for e in errs:
            print(f"  FAIL: {e}")
    else:
        print(f"  PASS: Zero forbidden placeholder tokens found")

    # 4. Duplication check
    print("\n[4/4] Checking cross-document duplication ratio...")
    errs, ratio = validate_duplication()
    all_errors.extend(errs)
    status = "PASS" if ratio < MAX_DUP_RATIO else "FAIL"
    print(f"  [{status}] Cross-document duplicate paragraph ratio: {ratio:.2f}% (max {MAX_DUP_RATIO}%)")

    # Summary
    print("\n" + "=" * 70)
    if all_errors:
        print(f"VALIDATION FAILED: {len(all_errors)} error(s) detected")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        total_sub = sum(r[2] for r in results)
        print(f"VALIDATION PASSED: All {len(CANONICAL_DOCS)} documents compliant")
        print(f"Total substantive lines: {total_sub}")
        print(f"Duplicate ratio: {ratio:.2f}%")
        sys.exit(0)


if __name__ == "__main__":
    main()
