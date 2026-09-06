"""
generate_all_release_docs.py
Master generator for Phase 19: Release Management documentation baseline.
Generates all 8 release documents and the master completeness audit artifact.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.releases.release_builder import generate_release_doc_by_idx
from scripts.releases.gen_release_audit import generate_release_audit_doc

def generate_all_releases():
    print("=" * 70)
    print("STARTING PHASE 19 RELEASE DOCUMENTATION GENERATION")
    print("=" * 70)

    results = {}
    for i in range(8):
        res = generate_release_doc_by_idx(i)
        results[f"RELEASE-{i:02d}"] = res

    audit_res = generate_release_audit_doc()
    results["RELEASE_COMPLETENESS_AUDIT"] = audit_res

    print("=" * 70)
    print("COMPLETED PHASE 19 GENERATION: All 9 documents generated.")
    for name, stat in results.items():
        print(f"- {name}: Total Lines: {stat['total']}, Substantive: {stat['substantive']}")
    print("=" * 70)
    return results

if __name__ == "__main__":
    generate_all_releases()
