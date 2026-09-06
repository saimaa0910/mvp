"""
gen_release_03.py
Generator for RELEASE-03: Pharmacy, Diagnostics & Referral Release.
Outputs to docs/19-releases/release-03-pharmacy-lab-referral.md
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.releases.release_builder import generate_release_doc_by_idx

def generate_release_03():
    return generate_release_doc_by_idx(3)

if __name__ == "__main__":
    res = generate_release_03()
    print(f"RELEASE-03 generated: {res}")
