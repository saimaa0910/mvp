"""
generate_all_srs_docs.py
Master Orchestration Script for Phase 05 SRS Documentation Generation:
  docs/05-srs/01-srs-master.md
  docs/05-srs/SRS_COMPLETENESS_AUDIT.md
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines, find_duplicate_paragraphs
from scripts.srs.generate_01_srs_master import generate_srs_master
from scripts.srs.generate_srs_completeness_audit import generate_srs_audit

DOCS_DIR = PROJECT_ROOT / "docs" / "05-srs"

def main():
    print("=" * 80)
    print("NAMMA CLINIC DIGITAL HEALTH PLATFORM - PHASE 05 SRS GENERATOR")
    print("=" * 80)
    print(f"Target Output Directory: {DOCS_DIR}\n")

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    generators = [
        ("01-srs-master.md", generate_srs_master),
        ("SRS_COMPLETENESS_AUDIT.md", generate_srs_audit),
    ]

    results = []
    file_contents = {}

    for doc_name, gen_func in generators:
        print(f"--> Generating {doc_name} ...")
        out_path, total_lines, substantive_lines = gen_func()
        with open(out_path, "r", encoding="utf-8") as f:
            content = f.read()
        file_contents[doc_name] = content
        metrics = count_lines(content)
        results.append({
            "name": doc_name,
            "path": out_path,
            "total": metrics["total"],
            "substantive": metrics["substantive"],
            "blank": metrics["blank"],
            "heading": metrics["heading"],
            "separator": metrics["separator"],
            "passed": metrics["substantive"] >= 2000
        })

    # Summary Table
    print("\n" + "=" * 80)
    print("SRS DOCUMENTATION METRICS SUMMARY")
    print("=" * 80)
    header = f"{'Document Name':<34} | {'Total':>7} | {'Substantive':>11} | {'Min Req':>8} | {'Status':>8}"
    print(header)
    print("-" * 80)

    all_passed = True
    total_total = 0
    total_substantive = 0

    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        if not r["passed"]:
            all_passed = False
        total_total += r["total"]
        total_substantive += r["substantive"]
        print(f"{r['name']:<34} | {r['total']:>7} | {r['substantive']:>11} | {2000:>8} | {status:>8}")

    print("-" * 80)
    print(f"{'TOTALS':<34} | {total_total:>7} | {total_substantive:>11} | {'-':>8} | {'PASS' if all_passed else 'FAIL':>8}")
    print("=" * 80)

    # Cross-document duplicate analysis
    print("\nCalculating cross-document paragraph duplication...")
    duplicates = find_duplicate_paragraphs(file_contents, min_len=60)
    print(f"Cross-Document Duplicate Paragraphs Found (>=60 chars): {len(duplicates)}")
    if duplicates:
        for doc1, doc2, snip in duplicates[:5]:
            print(f"  - Between '{doc1}' and '{doc2}': {snip}")

    if len(duplicates) == 0 and all_passed:
        print("\n[SUCCESS] All SRS documents meet line-count and unique-content requirements (0 duplicates)!")
        return 0
    elif len(duplicates) < 10 and all_passed:
        print(f"\n[SUCCESS] All SRS documents meet line-count requirements with negligible duplication ({len(duplicates)} items).")
        return 0
    else:
        print("\n[FAILURE] One or more validation criteria failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
