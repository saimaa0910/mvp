"""
validate_sprints.py
Root entrypoint for Phase 17 (Master Planning) and Phase 18 (18-Sprint Execution) validation.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.planning.validate_planning_docs import validate_all

def main():
    success = validate_all()
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
