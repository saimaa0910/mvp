"""
generate_all_timeplan_docs.py
Master generator for Phase 20: Master Timeplan Baseline.
Executes generators for all 8 timeplan documents and the completeness audit artifact.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.timeplan.gen_timeplan_01 import generate_timeplan_01
from scripts.timeplan.gen_timeplan_02 import generate_timeplan_02
from scripts.timeplan.gen_timeplan_03 import generate_timeplan_03
from scripts.timeplan.gen_timeplan_04 import generate_timeplan_04
from scripts.timeplan.gen_timeplan_05 import generate_timeplan_05
from scripts.timeplan.gen_timeplan_06 import generate_timeplan_06
from scripts.timeplan.gen_timeplan_07 import generate_timeplan_07
from scripts.timeplan.gen_timeplan_08 import generate_timeplan_08
from scripts.timeplan.gen_timeplan_audit import generate_timeplan_audit_doc

def generate_all_timeplans():
    print("=" * 75)
    print("STARTING PHASE 20 MASTER TIMEPLAN DOCUMENTATION GENERATION")
    print("=" * 75)

    results = {}
    print("\n--- Generating 01-master-timeplan.md ---")
    results["01-master-timeplan.md"] = generate_timeplan_01()

    print("\n--- Generating 02-team-capacity.md ---")
    results["02-team-capacity.md"] = generate_timeplan_02()

    print("\n--- Generating 03-resource-plan.md ---")
    results["03-resource-plan.md"] = generate_timeplan_03()

    print("\n--- Generating 04-estimation-model.md ---")
    results["04-estimation-model.md"] = generate_timeplan_04()

    print("\n--- Generating 05-workstream-timeline.md ---")
    results["05-workstream-timeline.md"] = generate_timeplan_05()

    print("\n--- Generating 06-milestone-plan.md ---")
    results["06-milestone-plan.md"] = generate_timeplan_06()

    print("\n--- Generating 07-pilot-plan.md ---")
    results["07-pilot-plan.md"] = generate_timeplan_07()

    print("\n--- Generating 08-rollout-plan.md ---")
    results["08-rollout-plan.md"] = generate_timeplan_08()

    print("\n--- Generating TIMEPLAN_COMPLETENESS_AUDIT.md ---")
    results["TIMEPLAN_COMPLETENESS_AUDIT.md"] = generate_timeplan_audit_doc()

    print("=" * 75)
    print("COMPLETED PHASE 20 GENERATION: All 9 documents generated.")
    for name, stat in results.items():
        print(f"- {name}: Total Lines: {stat['total']}, Substantive: {stat['substantive']}")
    print("=" * 75)
    return results

if __name__ == "__main__":
    generate_all_timeplans()
