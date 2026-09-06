"""
validate_backlog.py
Root entrypoint for Phase 16 Complete Delivery Backlog validation.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.backlog.validate_backlog_docs import validate_all

if __name__ == "__main__":
    if not validate_all():
        sys.exit(1)
