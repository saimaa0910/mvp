"""
generate_all_backlog_docs.py
Master orchestrator executing all Phase 16 Complete Delivery Backlog document generators.
"""

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.backlog.gen_backlog_01_epics import generate_doc as gen_01
from scripts.backlog.gen_backlog_02_features import generate_doc as gen_02
from scripts.backlog.gen_backlog_03_stories import generate_doc as gen_03
from scripts.backlog.gen_backlog_04_tasks import generate_doc as gen_04
from scripts.backlog.gen_backlog_05_micro_tasks import generate_doc as gen_05
from scripts.backlog.gen_backlog_audit import generate_doc as gen_audit

GENERATORS = [
    ("01-epics.md", gen_01),
    ("02-features.md", gen_02),
    ("03-user-stories.md", gen_03),
    ("04-tasks.md", gen_04),
    ("05-micro-tasks.md", gen_05),
    ("BACKLOG_COMPLETENESS_AUDIT.md", gen_audit),
]

def main():
    print("=" * 70)
    print("EXECUTING ALL PHASE 16 COMPLETE DELIVERY BACKLOG GENERATORS")
    print("=" * 70)
    start_time = time.time()

    total_substantive = 0
    total_raw = 0

    for name, gen_fn in GENERATORS:
        t0 = time.time()
        stats = gen_fn()
        elapsed = time.time() - t0
        sub = stats["substantive"]
        tot = stats["total"]
        total_substantive += sub
        total_raw += tot
        print(f" -> {name:<35} Total: {tot:>5} | Substantive: {sub:>5} ({elapsed:.2f}s)")

    duration = time.time() - start_time
    print("=" * 70)
    print(f"PHASE 16 GENERATION COMPLETE ({duration:.2f}s)")
    print(f"Total Documents:   {len(GENERATORS)}")
    print(f"Total Raw Lines:   {total_raw:,}")
    print(f"Total Substantive: {total_substantive:,}")
    print("=" * 70)

if __name__ == "__main__":
    main()
