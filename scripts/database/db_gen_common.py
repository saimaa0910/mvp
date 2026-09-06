"""
db_gen_common.py
Shared utilities for database document generation, formatting, and validation.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any

# Ensure root is in sys.path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from scripts.srs.common import count_lines

DOCS_DIR = Path(__file__).resolve().parent.parent.parent / "docs" / "07-database"

def write_db_doc(filename: str, content: str) -> Dict[str, int]:
    """
    Writes a database documentation file under docs/07-database/
    Verifies that substantive lines >= 2,000.
    """
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_path = DOCS_DIR / filename
    
    # Clean trailing whitespace on every line to satisfy git diff --check
    clean_lines = [line.rstrip() for line in content.splitlines()]
    clean_content = "\n".join(clean_lines) + "\n"
    
    stats = count_lines(clean_content)
    substantive = stats["substantive"]
    total = stats["total"]
    
    print(f"[{filename}] Total lines: {total}, Substantive: {substantive}")
    if substantive < 2000:
        raise ValueError(f"CRITICAL ERROR: {filename} has only {substantive} substantive lines! Minimum required is 2,000.")
        
    with open(target_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(clean_content)
        
    return stats
