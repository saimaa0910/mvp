"""
generate_all_db_docs.py
Master orchestrator script to execute all 19 database engineering document generators.
"""

import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "srs"))

from common import count_lines
from db_gen_common import DOCS_DIR

GENERATORS = [
    ("01-data-architecture.md", "gen_db_01_arch", "generate_doc_01"),
    ("02-conceptual-data-model.md", "gen_db_02_conceptual", "generate_doc_02"),
    ("03-logical-data-model.md", "gen_db_03_logical", "generate_doc_03"),
    ("04-physical-data-model.md", "gen_db_04_physical", "generate_doc_04"),
    ("05-table-catalog.md", "gen_db_05_catalog", "generate_doc_05"),
    ("06-column-data-dictionary.md", "gen_db_06_columns", "generate_doc_06"),
    ("07-primary-foreign-key-map.md", "gen_db_07_pk_fk", "generate_doc_07"),
    ("08-index-strategy.md", "gen_db_08_indexes", "generate_doc_08"),
    ("09-partitioning-strategy.md", "gen_db_09_partitions", "generate_doc_09"),
    ("10-audit-data-model.md", "gen_db_10_audit", "generate_doc_10"),
    ("11-transaction-model.md", "gen_db_11_transactions", "generate_doc_11"),
    ("12-data-retention.md", "gen_db_12_retention", "generate_doc_12"),
    ("13-data-classification.md", "gen_db_13_classification", "generate_doc_13"),
    ("14-migration-strategy.md", "gen_db_14_migrations", "generate_doc_14"),
    ("15-seed-data-strategy.md", "gen_db_15_seeds", "generate_doc_15"),
    ("16-olap-star-schema.md", "gen_db_16_olap", "generate_doc_16"),
    ("17-data-quality-rules.md", "gen_db_17_dq", "generate_doc_17"),
    ("18-data-lineage.md", "gen_db_18_lineage", "generate_doc_18"),
    ("DATABASE_COMPLETENESS_AUDIT.md", "gen_db_audit", "generate_doc_audit")
]

def run_all_generators():
    print("=" * 80)
    print("NAMMA CLINIC DATABASE DOCUMENTATION MASTER ORCHESTRATOR")
    print("=" * 80)
    start_total = time.time()
    
    success_count = 0
    total_substantive = 0
    total_lines = 0

    for idx, (doc_name, mod_name, func_name) in enumerate(GENERATORS, start=1):
        t0 = time.time()
        print(f"[{idx:02d}/{len(GENERATORS):02d}] Executing {mod_name}.{func_name}()...", end=" ", flush=True)
        try:
            mod = __import__(mod_name)
            func = getattr(mod, func_name)
            func()
            elapsed = time.time() - t0
            
            # Verify file
            fpath = DOCS_DIR / doc_name
            content = fpath.read_text(encoding="utf-8")
            counts = count_lines(content)
            sub = counts["substantive"]
            raw = counts["total"]
            total_substantive += sub
            total_lines += raw
            
            if sub >= 2000:
                status = "PASS"
                success_count += 1
            else:
                status = f"FAIL ({sub} < 2000)"
            print(f"[{status}] in {elapsed:.2f}s -> {sub:,} substantive lines (total {raw:,})")
        except Exception as e:
            print(f"[ERROR] {e}")

    total_time = time.time() - start_total
    print("=" * 80)
    print(f"GENERATION COMPLETE: {success_count}/{len(GENERATORS)} documents passed >= 2,000 substantive lines.")
    print(f"Total substantive lines: {total_substantive:,} | Total lines: {total_lines:,} | Time: {total_time:.2f}s")
    print("=" * 80)

    if success_count == len(GENERATORS):
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(run_all_generators())
