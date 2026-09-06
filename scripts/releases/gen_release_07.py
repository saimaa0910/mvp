"""
gen_release_07.py
Generator for RELEASE-07: AI-Assisted Clinical Support & Advanced ABDM Release.
Outputs to docs/19-releases/release-07-ai-abdm.md
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.releases.release_builder import generate_release_doc_by_idx

def generate_release_07():
    return generate_release_doc_by_idx(7)

if __name__ == "__main__":
    res = generate_release_07()
    print(f"RELEASE-07 generated: {res}")
