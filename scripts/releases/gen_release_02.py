"""
gen_release_02.py
Generator for RELEASE-02: Clinical OPD Consultation & Triage Release.
Outputs to docs/19-releases/release-02-clinical.md
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.releases.release_builder import generate_release_doc_by_idx

def generate_release_02():
    return generate_release_doc_by_idx(2)

if __name__ == "__main__":
    res = generate_release_02()
    print(f"RELEASE-02 generated: {res}")
