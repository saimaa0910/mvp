"""
gen_release_00.py
Generator for RELEASE-00: Platform Foundation & Infrastructure Release.
Outputs to docs/19-releases/release-00-foundation.md
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.releases.release_builder import generate_release_doc_by_idx

def generate_release_00():
    return generate_release_doc_by_idx(0)

if __name__ == "__main__":
    res = generate_release_00()
    print(f"RELEASE-00 generated: {res}")
