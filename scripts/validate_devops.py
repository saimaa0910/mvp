#!/usr/bin/env python3
"""
validate_devops.py
Top-level quality gate validator for Namma Clinic Phase 12: DevOps Engineering Planning & Design.
Invokes scripts/devops/validate_devops_docs.py and returns appropriate exit code.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.devops.validate_devops_docs import main

if __name__ == "__main__":
    sys.exit(main())
