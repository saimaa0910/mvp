"""
validate_ai.py
Root entrypoint for Phase 14 AI/ML Engineering validation.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.ai.validate_ai_docs import validate_all

if __name__ == "__main__":
    if not validate_all():
        sys.exit(1)
