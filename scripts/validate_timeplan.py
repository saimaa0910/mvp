"""
validate_timeplan.py
Root validation entrypoint for Phase 20: Master Timeplan documentation baseline.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.timeplan.validate_timeplan_docs import run_timeplan_validation

if __name__ == "__main__":
    success = run_timeplan_validation()
    sys.exit(0 if success else 1)
