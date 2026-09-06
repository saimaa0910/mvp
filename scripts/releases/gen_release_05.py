"""
gen_release_05.py
Generator for RELEASE-05: Pilot Deployment & Clinical Hardening Release.
Outputs to docs/19-releases/release-05-pilot.md
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.releases.release_builder import generate_release_doc_by_idx

def generate_release_05():
    return generate_release_doc_by_idx(5)

if __name__ == "__main__":
    res = generate_release_05()
    print(f"RELEASE-05 generated: {res}")
