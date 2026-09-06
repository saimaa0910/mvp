"""
generate_all_planning_docs.py
Master orchestrator executing all Phase 17 (Master Planning) and Phase 18 (18-Sprint Execution) generators.
"""

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.planning.gen_planning_01_dependency_map import generate_doc as gen_p01
from scripts.planning.gen_planning_02_critical_path import generate_doc as gen_p02
from scripts.planning.gen_planning_03_dependency_register import generate_doc as gen_p03
from scripts.planning.gen_planning_04_blockers import generate_doc as gen_p04
from scripts.planning.gen_planning_05_risk_adjusted import generate_doc as gen_p05
from scripts.planning.gen_planning_06_capacity import generate_doc as gen_p06
from scripts.planning.gen_planning_07_velocity import generate_doc as gen_p07
from scripts.planning.gen_planning_08_estimation import generate_doc as gen_p08
from scripts.planning.gen_planning_09_workstreams import generate_doc as gen_p09
from scripts.planning.gen_planning_audit import generate_doc as gen_p_audit
from scripts.planning.gen_sprints import generate_all_sprints
from scripts.planning.gen_sprint_audit import generate_doc as gen_s_audit

def main():
    print("=" * 80)
    print("EXECUTING ALL PHASE 17 & PHASE 18 PLANNING & SPRINT GENERATORS")
    print("=" * 80)
    start_time = time.time()

    total_substantive = 0
    total_raw = 0

    planning_gens = [
        ("docs/17-planning/01-master-dependency-map.md", gen_p01),
        ("docs/17-planning/02-critical-path.md", gen_p02),
        ("docs/17-planning/03-dependency-register.md", gen_p03),
        ("docs/17-planning/04-blocker-register.md", gen_p04),
        ("docs/17-planning/05-risk-adjusted-plan.md", gen_p05),
        ("docs/17-planning/06-resource-capacity.md", gen_p06),
        ("docs/17-planning/07-velocity-model.md", gen_p07),
        ("docs/17-planning/08-estimation-model.md", gen_p08),
        ("docs/17-planning/09-workstream-plan.md", gen_p09),
        ("docs/17-planning/PLANNING_COMPLETENESS_AUDIT.md", gen_p_audit),
    ]

    print("\n--- Generating Phase 17 Master Planning Documents (10 Documents) ---")
    for name, gen_fn in planning_gens:
        t0 = time.time()
        stats = gen_fn()
        elapsed = time.time() - t0
        sub = stats["substantive"]
        tot = stats["total"]
        total_substantive += sub
        total_raw += tot
        print(f" -> {name:<50} Total: {tot:>5} | Sub: {sub:>5} ({elapsed:.2f}s)")

    print("\n--- Generating Phase 18 Sprint Execution Documents (18 Sprints + Audit) ---")
    t0 = time.time()
    generate_all_sprints()
    elapsed_sprints = time.time() - t0
    print(f" -> Generated 18 Sprint Execution Documents ({elapsed_sprints:.2f}s)")

    t0 = time.time()
    audit_stats = gen_s_audit()
    elapsed_audit = time.time() - t0
    sub = audit_stats["substantive"]
    tot = audit_stats["total"]
    total_substantive += sub
    total_raw += tot
    print(f" -> docs/18-sprints/SPRINT_EXECUTION_COMPLETENESS_AUDIT.md Total: {tot:>5} | Sub: {sub:>5} ({elapsed_audit:.2f}s)")

    # Compute full stats from disk
    from scripts.srs.common import count_lines
    p17_dir = PROJECT_ROOT / "docs" / "17-planning"
    p18_dir = PROJECT_ROOT / "docs" / "18-sprints"

    p17_sub = sum(count_lines(f.read_text(encoding="utf-8"))["substantive"] for f in p17_dir.glob("*.md"))
    p17_tot = sum(count_lines(f.read_text(encoding="utf-8"))["total"] for f in p17_dir.glob("*.md"))
    p18_sub = sum(count_lines(f.read_text(encoding="utf-8"))["substantive"] for f in p18_dir.glob("*.md"))
    p18_tot = sum(count_lines(f.read_text(encoding="utf-8"))["total"] for f in p18_dir.glob("*.md"))

    duration = time.time() - start_time
    print("=" * 80)
    print(f"MASTER PLANNING & SPRINT GENERATION COMPLETE ({duration:.2f}s)")
    print(f"Phase 17 Documents: {len(list(p17_dir.glob('*.md')))} | Total Lines: {p17_tot:,} | Substantive: {p17_sub:,}")
    print(f"Phase 18 Documents: {len(list(p18_dir.glob('*.md')))} | Total Lines: {p18_tot:,} | Substantive: {p18_sub:,}")
    print(f"Grand Total:        {len(list(p17_dir.glob('*.md'))) + len(list(p18_dir.glob('*.md')))} Documents | Total: {p17_tot + p18_tot:,} | Substantive: {p17_sub + p18_sub:,}")
    print("=" * 80)

if __name__ == "__main__":
    main()
