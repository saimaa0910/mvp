"""
gen_release_04.py
Generator for RELEASE-04: Analytics, Reporting & Offline Sync Release.
Outputs to docs/19-releases/release-04-analytics-offline.md
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.releases.release_builder import generate_release_doc_by_idx

def generate_release_04():
    return generate_release_doc_by_idx(4)

if __name__ == "__main__":
    res = generate_release_04()
    print(f"RELEASE-04 generated: {res}")
