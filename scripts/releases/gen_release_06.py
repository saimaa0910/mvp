"""
gen_release_06.py
Generator for RELEASE-06: Production Scale & Multi-Zone Rollout Release.
Outputs to docs/19-releases/release-06-production-scale.md
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.releases.release_builder import generate_release_doc_by_idx

def generate_release_06():
    return generate_release_doc_by_idx(6)

if __name__ == "__main__":
    res = generate_release_06()
    print(f"RELEASE-06 generated: {res}")
