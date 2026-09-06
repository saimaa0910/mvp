"""
generate_all_integration_docs.py
Master orchestrator executing all Phase 15 Integration Engineering document generators.
"""

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.integrations.gen_int_01_architecture import generate_doc as gen_01
from scripts.integrations.gen_int_02_abha import generate_doc as gen_02
from scripts.integrations.gen_int_03_fhir import generate_doc as gen_03
from scripts.integrations.gen_int_04_ehospital import generate_doc as gen_04
from scripts.integrations.gen_int_05_sms import generate_doc as gen_05
from scripts.integrations.gen_int_06_state_reporting import generate_doc as gen_06
from scripts.integrations.gen_int_07_file_export import generate_doc as gen_07
from scripts.integrations.gen_int_08_security import generate_doc as gen_08
from scripts.integrations.gen_int_09_error_handling import generate_doc as gen_09
from scripts.integrations.gen_int_10_monitoring import generate_doc as gen_10
from scripts.integrations.gen_int_11_environment import generate_doc as gen_11
from scripts.integrations.gen_int_audit import generate_doc as gen_audit

GENERATORS = [
    ("01-integration-architecture.md", gen_01),
    ("02-abha-abdm.md", gen_02),
    ("03-fhir.md", gen_03),
    ("04-eHospital.md", gen_04),
    ("05-sms.md", gen_05),
    ("06-state-reporting.md", gen_06),
    ("07-file-export.md", gen_07),
    ("08-integration-security.md", gen_08),
    ("09-integration-error-handling.md", gen_09),
    ("10-integration-monitoring.md", gen_10),
    ("11-sandbox-vs-production.md", gen_11),
    ("INTEGRATION_COMPLETENESS_AUDIT.md", gen_audit),
]

def main():
    print("=" * 70)
    print("EXECUTING ALL PHASE 15 INTEGRATION ENGINEERING GENERATORS")
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
    print(f"PHASE 15 GENERATION COMPLETE ({duration:.2f}s)")
    print(f"Total Documents:   {len(GENERATORS)}")
    print(f"Total Raw Lines:   {total_raw:,}")
    print(f"Total Substantive: {total_substantive:,}")
    print("=" * 70)

if __name__ == "__main__":
    main()
