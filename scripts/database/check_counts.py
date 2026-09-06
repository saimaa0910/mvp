import sys
from pathlib import Path

# Add root to sys.path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from scripts.srs.common import count_lines

docs_dir = ROOT / "docs" / "07-database"
files = sorted(docs_dir.glob("*.md"))
print(f"Checking {len(files)} files in {docs_dir}:")
for p in files:
    content = p.read_text(encoding="utf-8")
    stats = count_lines(content)
    status = "PASS" if stats["substantive"] >= 2000 else "FAIL (<2000)"
    print(f"  {p.name:<35}: {stats['substantive']:>5} substantive lines (total {stats['total']:>5}) [{status}]")
