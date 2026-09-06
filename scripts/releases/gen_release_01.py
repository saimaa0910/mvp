"""
gen_release_01.py
Generator for RELEASE-01: Core Patient Master & Registration Release.
Outputs to docs/19-releases/release-01-core-patient.md
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.releases.release_builder import generate_release_doc_by_idx

def generate_release_01():
    return generate_release_doc_by_idx(1)

if __name__ == "__main__":
    res = generate_release_01()
    print(f"RELEASE-01 generated: {res}")
