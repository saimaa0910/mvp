"""
generate_all_ai_docs.py
Master orchestrator to generate all 14 Phase 14 AI/ML Engineering & Decision Support documents.
Enforces >= 2,000 substantive lines on every generated document.
"""

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines

from scripts.ai import (
    gen_ai_01_strategy,
    gen_ai_02_governance,
    gen_ai_03_use_cases,
    gen_ai_04_stock_forecasting,
    gen_ai_05_fever_anomaly,
    gen_ai_06_ncd_recall,
    gen_ai_07_feature_engineering,
    gen_ai_08_data_requirements,
    gen_ai_09_model_evaluation,
    gen_ai_10_model_monitoring,
    gen_ai_11_human_approval,
    gen_ai_12_safety,
    gen_ai_13_versioning,
    gen_ai_audit,
)

GENERATORS = [
    ("01-ai-strategy.md", gen_ai_01_strategy.generate_doc),
    ("02-ai-governance.md", gen_ai_02_governance.generate_doc),
    ("03-ai-use-cases.md", gen_ai_03_use_cases.generate_doc),
    ("04-stock-forecasting.md", gen_ai_04_stock_forecasting.generate_doc),
    ("05-fever-anomaly-detection.md", gen_ai_05_fever_anomaly.generate_doc),
    ("06-ncd-recall-prioritization.md", gen_ai_06_ncd_recall.generate_doc),
    ("07-feature-engineering.md", gen_ai_07_feature_engineering.generate_doc),
    ("08-model-data-requirements.md", gen_ai_08_data_requirements.generate_doc),
    ("09-model-evaluation.md", gen_ai_09_model_evaluation.generate_doc),
    ("10-model-monitoring.md", gen_ai_10_model_monitoring.generate_doc),
    ("11-human-approval.md", gen_ai_11_human_approval.generate_doc),
    ("12-ai-safety.md", gen_ai_12_safety.generate_doc),
    ("13-model-versioning.md", gen_ai_13_versioning.generate_doc),
    ("AI_COMPLETENESS_AUDIT.md", gen_ai_audit.generate_doc),
]

def main():
    print("=" * 70)
    print("PHASE 14 — AI/ML ENGINEERING & DECISION SUPPORT: MASTER GENERATOR")
    print("Generating all 14 documents under docs/14-ai/")
    print("=" * 70)

    start_time = time.time()
    results = []
    total_substantive = 0
    total_raw = 0

    for idx, (doc_name, gen_func) in enumerate(GENERATORS, 1):
        t0 = time.time()
        print(f"[{idx:02d}/{len(GENERATORS):02d}] Generating {doc_name}...", end=" ", flush=True)
        res = gen_func()
        elapsed = time.time() - t0

        sub = res["substantive"]
        tot = res["total"]

        total_substantive += sub
        total_raw += tot
        results.append((doc_name, sub, tot, elapsed))
        print(f"DONE ({sub:,} substantive / {tot:,} total lines in {elapsed:.2f}s)")

    duration = time.time() - start_time
    print("=" * 70)
    print(f"SUMMARY: 14 documents generated in {duration:.2f}s")
    print(f"Total Substantive Lines: {total_substantive:,}")
    print(f"Total Raw Lines:         {total_raw:,}")
    print("=" * 70)

    failed = [r for r in results if r[1] < 2000]
    if failed:
        print(f"ERROR: {len(failed)} documents failed the 2,000 substantive line threshold!")
        for doc_name, sub, tot, _ in failed:
            print(f"  - {doc_name}: {sub} substantive lines")
        sys.exit(1)

    print("ALL 14 DOCUMENTS EXCEED 2,000 SUBSTANTIVE LINES! PASS!")

if __name__ == "__main__":
    main()
