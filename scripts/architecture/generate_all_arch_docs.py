"""
generate_all_arch_docs.py
Master Orchestration Script for Phase 06 Architecture Documentation Generation:
Executes all 19 architecture generators, verifies substantive line counts >= 2,000,
and checks cross-document paragraph duplication.
"""

import sys
import importlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines, find_duplicate_paragraphs

DOCS_DIR = PROJECT_ROOT / "docs" / "06-architecture"

ARCH_DOCS = [
    ("01-solution-architecture.md", "scripts.architecture.gen_arch_01"),
    ("02-system-context.md", "scripts.architecture.gen_arch_02"),
    ("03-container-architecture.md", "scripts.architecture.gen_arch_03"),
    ("04-component-architecture.md", "scripts.architecture.gen_arch_04"),
    ("05-frontend-architecture.md", "scripts.architecture.gen_arch_05"),
    ("06-backend-architecture.md", "scripts.architecture.gen_arch_06"),
    ("07-data-architecture.md", "scripts.architecture.gen_arch_07"),
    ("08-security-architecture.md", "scripts.architecture.gen_arch_08"),
    ("09-offline-architecture.md", "scripts.architecture.gen_arch_09"),
    ("10-integration-architecture.md", "scripts.architecture.gen_arch_10"),
    ("11-analytics-architecture.md", "scripts.architecture.gen_arch_11"),
    ("12-ai-architecture.md", "scripts.architecture.gen_arch_12"),
    ("13-observability-architecture.md", "scripts.architecture.gen_arch_13"),
    ("14-disaster-recovery.md", "scripts.architecture.gen_arch_14"),
    ("15-scalability.md", "scripts.architecture.gen_arch_15"),
    ("16-deployment-architecture.md", "scripts.architecture.gen_arch_16"),
    ("17-environment-strategy.md", "scripts.architecture.gen_arch_17"),
    ("18-architecture-decisions.md", "scripts.architecture.gen_arch_18"),
    ("ARCHITECTURE_TRACEABILITY_MATRIX.md", "scripts.architecture.gen_arch_traceability"),
]

def main():
    print("=" * 90)
    print("NAMMA CLINIC DIGITAL HEALTH PLATFORM - PHASE 06 ARCHITECTURE MASTER GENERATOR")
    print("=" * 90)
    print(f"Target Output Directory: {DOCS_DIR}\n")

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    file_contents = {}

    for doc_name, module_name in ARCH_DOCS:
        print(f"--> Generating {doc_name} via {module_name} ...")
        mod = importlib.import_module(module_name)
        out_path, total_lines, substantive_lines = mod.generate_document()
        with open(out_path, "r", encoding="utf-8") as f:
            content = f.read()
        file_contents[doc_name] = content
        metrics = count_lines(content)
        passed = metrics["substantive"] >= 2000
        results.append({
            "name": doc_name,
            "path": out_path,
            "total": metrics["total"],
            "substantive": metrics["substantive"],
            "blank": metrics["blank"],
            "heading": metrics["heading"],
            "separator": metrics["separator"],
            "passed": passed
        })

    # Summary Table
    print("\n" + "=" * 90)
    print("PHASE 06 ARCHITECTURE DOCUMENTATION METRICS SUMMARY")
    print("=" * 90)
    header = f"{'Document Name':<38} | {'Total':>7} | {'Substantive':>11} | {'Min Req':>8} | {'Status':>8}"
    print(header)
    print("-" * 90)

    all_passed = True
    total_total = 0
    total_substantive = 0

    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        if not r["passed"]:
            all_passed = False
        total_total += r["total"]
        total_substantive += r["substantive"]
        print(f"{r['name']:<38} | {r['total']:>7} | {r['substantive']:>11} | {2000:>8} | {status:>8}")

    print("-" * 90)
    print(f"{'TOTALS (19 ARCHITECTURE DOCUMENTS)':<38} | {total_total:>7} | {total_substantive:>11} | {'-':>8} | {'PASS' if all_passed else 'FAIL':>8}")
    print("=" * 90)

    # Cross-document duplicate analysis
    print("\nCalculating cross-document paragraph duplication (>= 60 chars)...")
    duplicates = find_duplicate_paragraphs(file_contents, min_len=60)
    print(f"Cross-Document Duplicate Paragraphs Found: {len(duplicates)}")
    if duplicates:
        for doc1, doc2, snip in duplicates[:5]:
            print(f"  - Between '{doc1}' and '{doc2}': {snip}")

    if all_passed:
        print("\n[SUCCESS] All 19 Phase 06 Architecture documents meet the >= 2,000 substantive line requirement!")
        return 0
    else:
        print("\n[FAILURE] One or more architecture documents failed the substantive line threshold!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
