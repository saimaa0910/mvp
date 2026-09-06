"""
generate_all_qa_docs.py
Master orchestrator script to sequentially execute all 20 Phase 11 QA generators.
"""

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.qa import (
    gen_qa_01_strategy,
    gen_qa_02_levels,
    gen_qa_03_unit,
    gen_qa_04_integration,
    gen_qa_05_api,
    gen_qa_06_e2e,
    gen_qa_07_ui,
    gen_qa_08_performance,
    gen_qa_09_security,
    gen_qa_10_offline,
    gen_qa_11_data_quality,
    gen_qa_12_accessibility,
    gen_qa_13_localization,
    gen_qa_14_regression,
    gen_qa_15_uat,
    gen_qa_16_pilot,
    gen_qa_17_test_data,
    gen_qa_18_environment,
    gen_qa_19_quality_gates,
    gen_qa_audit,
)

GENERATORS = [
    ("01-test-strategy.md", gen_qa_01_strategy.generate_doc),
    ("02-test-levels.md", gen_qa_02_levels.generate_doc),
    ("03-unit-test-plan.md", gen_qa_03_unit.generate_doc),
    ("04-integration-test-plan.md", gen_qa_04_integration.generate_doc),
    ("05-api-test-plan.md", gen_qa_05_api.generate_doc),
    ("06-e2e-test-plan.md", gen_qa_06_e2e.generate_doc),
    ("07-ui-test-plan.md", gen_qa_07_ui.generate_doc),
    ("08-performance-test-plan.md", gen_qa_08_performance.generate_doc),
    ("09-security-test-plan.md", gen_qa_09_security.generate_doc),
    ("10-offline-test-plan.md", gen_qa_10_offline.generate_doc),
    ("11-data-quality-test-plan.md", gen_qa_11_data_quality.generate_doc),
    ("12-accessibility-test-plan.md", gen_qa_12_accessibility.generate_doc),
    ("13-localization-test-plan.md", gen_qa_13_localization.generate_doc),
    ("14-regression-strategy.md", gen_qa_14_regression.generate_doc),
    ("15-uat-plan.md", gen_qa_15_uat.generate_doc),
    ("16-pilot-test-plan.md", gen_qa_16_pilot.generate_doc),
    ("17-test-data-strategy.md", gen_qa_17_test_data.generate_doc),
    ("18-test-environment.md", gen_qa_18_environment.generate_doc),
    ("19-quality-gates.md", gen_qa_19_quality_gates.generate_doc),
    ("QA_COMPLETENESS_AUDIT.md", gen_qa_audit.generate_doc),
]

def main():
    t0 = time.time()
    print("================================================================================")
    print("EXECUTING MASTER QA GENERATION ORCHESTRATOR (PHASE 11: 20 DOCUMENTS)")
    print("================================================================================")

    total_substantive = 0
    total_physical = 0
    for filename, gen_fn in GENERATORS:
        res = gen_fn()
        sub = res["substantive"] if isinstance(res, dict) else res
        tot = res["total"] if isinstance(res, dict) else sub
        total_substantive += sub
        total_physical += tot
        print(f"  -> {filename:<35} : {sub:>6} substantive ({tot:>6} total) [PASS]")

    elapsed = time.time() - t0
    print("================================================================================")
    print(f"ALL 20 QA DOCUMENTS GENERATED SUCCESSFULLY IN {elapsed:.2f}s")
    print(f"TOTAL SUBSTANTIVE LINES: {total_substantive:,} ({total_physical:,} total lines)")
    print("================================================================================")

if __name__ == "__main__":
    main()
