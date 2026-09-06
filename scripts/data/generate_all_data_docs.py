"""
generate_all_data_docs.py
Master orchestrator to generate all 16 Phase 13 Data Engineering & Analytics documents.
Enforces >= 2,000 substantive lines on every generated document.
"""

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines

from scripts.data import (
    gen_data_01_architecture,
    gen_data_02_oltp_olap,
    gen_data_03_star_schema,
    gen_data_04_etl_elt,
    gen_data_05_cdc,
    gen_data_06_quality,
    gen_data_07_lineage,
    gen_data_08_governance,
    gen_data_09_dashboard_metrics,
    gen_data_10_clinic_kpis,
    gen_data_11_zonal_kpis,
    gen_data_12_city_kpis,
    gen_data_13_public_health,
    gen_data_14_inventory,
    gen_data_15_referral,
    gen_data_audit,
)

GENERATORS = [
    ("01-data-engineering-architecture.md", gen_data_01_architecture.generate_doc),
    ("02-oltp-olap-separation.md", gen_data_02_oltp_olap.generate_doc),
    ("03-star-schema.md", gen_data_03_star_schema.generate_doc),
    ("04-etl-elt-strategy.md", gen_data_04_etl_elt.generate_doc),
    ("05-cdc-strategy.md", gen_data_05_cdc.generate_doc),
    ("06-data-quality.md", gen_data_06_quality.generate_doc),
    ("07-data-lineage.md", gen_data_07_lineage.generate_doc),
    ("08-data-governance.md", gen_data_08_governance.generate_doc),
    ("09-dashboard-metrics.md", gen_data_09_dashboard_metrics.generate_doc),
    ("10-clinic-kpis.md", gen_data_10_clinic_kpis.generate_doc),
    ("11-zonal-kpis.md", gen_data_11_zonal_kpis.generate_doc),
    ("12-city-kpis.md", gen_data_12_city_kpis.generate_doc),
    ("13-public-health-metrics.md", gen_data_13_public_health.generate_doc),
    ("14-inventory-analytics.md", gen_data_14_inventory.generate_doc),
    ("15-referral-analytics.md", gen_data_15_referral.generate_doc),
    ("DATA_COMPLETENESS_AUDIT.md", gen_data_audit.generate_doc),
]

def main():
    print("=" * 70)
    print("PHASE 13 — DATA ENGINEERING & ANALYTICS: MASTER GENERATOR")
    print("Generating all 16 documents under docs/13-data/")
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
    print(f"SUMMARY: 16 documents generated in {duration:.2f}s")
    print(f"Total Substantive Lines: {total_substantive:,}")
    print(f"Total Raw Lines:         {total_raw:,}")
    print("=" * 70)

    failed = [r for r in results if r[1] < 2000]
    if failed:
        print(f"ERROR: {len(failed)} documents failed the 2,000 substantive line threshold!")
        for doc_name, sub, tot, _ in failed:
            print(f"  - {doc_name}: {sub} substantive lines")
        sys.exit(1)

    print("ALL 16 DOCUMENTS EXCEED 2,000 SUBSTANTIVE LINES! PASS!")

if __name__ == "__main__":
    main()
