"""
generate_all_api_docs.py
Master Orchestrator for Phase 08: API Engineering Planning & Design.
Executes all generators sequentially to produce the complete 23-document baseline in docs/08-api/.
"""

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.api import (
    gen_api_01_architecture,
    gen_api_02_conventions,
    gen_api_03_versioning,
    gen_domain_api,
    gen_api_19_errors,
    gen_api_20_security,
    gen_api_21_ratelimit,
    gen_api_22_traceability,
    gen_api_23_audit
)

def run_all():
    start_time = time.time()
    print("================================================================================")
    print("NAMMA CLINIC: PHASE 08 API ENGINEERING MASTER GENERATOR")
    print("================================================================================")

    steps = [
        ("01-api-architecture.md", gen_api_01_architecture.generate_doc),
        ("02-api-conventions.md", gen_api_02_conventions.generate_doc),
        ("03-api-versioning.md", gen_api_03_versioning.generate_doc),
    ]

    for filename, fn in steps:
        s = time.time()
        res = fn()
        dur = time.time() - s
        print(f"[{dur:.2f}s] Generated {filename}: {res['substantive']} substantive lines ({res['total']} total)")

    print("--- Generating 15 Domain API Specifications (04-auth to 18-portability) ---")
    for d in gen_domain_api.DOMAIN_CONFIGS.keys():
        s = time.time()
        res = gen_domain_api.generate_domain_doc(d)
        dur = time.time() - s
        fname = gen_domain_api.DOMAIN_CONFIGS[d]["filename"]
        print(f"[{dur:.2f}s] Generated {fname} ({d}): {res['substantive']} substantive lines ({res['total']} total)")

    post_steps = [
        ("19-error-handling.md", gen_api_19_errors.generate_doc),
        ("20-api-security.md", gen_api_20_security.generate_doc),
        ("21-api-rate-limiting.md", gen_api_21_ratelimit.generate_doc),
        ("22-api-traceability.md", gen_api_22_traceability.generate_doc),
        ("API_COMPLETENESS_AUDIT.md", gen_api_23_audit.generate_doc),
    ]

    for filename, fn in post_steps:
        s = time.time()
        res = fn()
        dur = time.time() - s
        print(f"[{dur:.2f}s] Generated {filename}: {res['substantive']} substantive lines ({res['total']} total)")

    total_dur = time.time() - start_time
    print("================================================================================")
    print(f"SUCCESS: ALL 23 API SPECIFICATIONS GENERATED IN {total_dur:.2f}s")
    print("================================================================================")

if __name__ == "__main__":
    run_all()
