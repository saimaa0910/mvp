"""
validate_releases.py
Root validation entrypoint for Phase 19: Release Management documentation baseline.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.releases.validate_release_docs import run_release_validation

if __name__ == "__main__":
    success = run_release_validation()
    sys.exit(0 if success else 1)
