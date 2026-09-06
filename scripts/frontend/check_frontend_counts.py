"""
check_frontend_counts.py
Fast CLI inspector for Phase 09 Frontend Engineering documentation substantive line counts.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines

FE_DIR = PROJECT_ROOT / "docs" / "09-frontend"

def main():
    print(f"{'Filename':<40} | {'Total':>8} | {'Substantive':>12} | {'Status':>8}")
    print("-" * 75)

    total_all = 0
    sub_all = 0
    files = sorted(list(FE_DIR.glob("*.md")))
    for f in files:
        stats = count_lines(f.read_text(encoding="utf-8"))
        tot = stats["total"]
        sub = stats["substantive"]
        total_all += tot
        sub_all += sub
        status = "PASS" if sub >= 2000 else "FAIL"
        print(f"{f.name:<40} | {tot:>8} | {sub:>12} | {status:>8}")

    print("-" * 75)
    print(f"{'TOTAL (19 files)':<40} | {total_all:>8} | {sub_all:>12} | {'PASS' if sub_all >= 38000 else 'FAIL'}")

if __name__ == "__main__":
    main()
