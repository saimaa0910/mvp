#!/usr/bin/env python3
"""
req_core_data.py
Canonical structured dataset and centralized registry for all 810 requirements
governing the Namma Clinic Digital Health & Operations Platform.

Aggregates 17 requirement domain modules:
  01. BR-001  to BR-050   (50 Business Requirements)
  02. FR-001  to FR-080   (80 Functional Requirements)
  03. NFR-001 to NFR-050  (50 Non-Functional Requirements)
  04. BRULE-001 to BRULE-050 (50 Business Rules)
  05. CR-001  to CR-050   (50 Clinical Rules)
  06. OR-001  to OR-050   (50 Operational Rules)
  07. SECR-001 to SECR-050 (50 Security Requirements)
  08. PRIV-001 to PRIV-050 (50 Privacy Requirements)
  09. PERF-001 to PERF-040 (40 Performance Requirements)
  10. AVAIL-001 to AVAIL-040 (40 Availability Requirements)
  11. LOC-001 to LOC-040  (40 Localization Requirements)
  12. A11Y-001 to A11Y-040 (40 Accessibility Requirements)
  13. OFF-001 to OFF-050  (50 Offline Requirements)
  14. REP-001 to REP-050  (50 Reporting Requirements)
  15. ANL-001 to ANL-040  (40 Analytics Requirements)
  16. AIR-001 to AIR-040  (40 AI Decision-Support Requirements)
  17. INT-001 to INT-050  (50 Integration Requirements)
Total: 810 globally unique, implementation-ready requirements.
"""

import os
import sys

# Ensure local imports resolve
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_br import BR_REQUIREMENTS
from data_fr import FR_REQUIREMENTS
from data_nfr import NFR_REQUIREMENTS
from data_brule import BRULE_RULES
from data_cr import CR_RULES
from data_or import OR_RULES
from data_secr import SECR_REQUIREMENTS
from data_priv import PRIV_REQUIREMENTS
from data_perf import PERF_REQUIREMENTS
from data_avail import AVAIL_REQUIREMENTS
from data_loc import LOC_REQUIREMENTS
from data_a11y import A11Y_REQUIREMENTS
from data_off import OFF_REQUIREMENTS
from data_rep import REP_REQUIREMENTS
from data_anl import ANL_REQUIREMENTS
from data_air import AIR_REQUIREMENTS
from data_int import INT_REQUIREMENTS

# Canonical list of all 810 requirements
ALL_REQUIREMENTS = [
    *BR_REQUIREMENTS,
    *FR_REQUIREMENTS,
    *NFR_REQUIREMENTS,
    *BRULE_RULES,
    *CR_RULES,
    *OR_RULES,
    *SECR_REQUIREMENTS,
    *PRIV_REQUIREMENTS,
    *PERF_REQUIREMENTS,
    *AVAIL_REQUIREMENTS,
    *LOC_REQUIREMENTS,
    *A11Y_REQUIREMENTS,
    *OFF_REQUIREMENTS,
    *REP_REQUIREMENTS,
    *ANL_REQUIREMENTS,
    *AIR_REQUIREMENTS,
    *INT_REQUIREMENTS,
]

# Fast lookup dictionaries
REQUIREMENTS_BY_ID = {r["id"]: r for r in ALL_REQUIREMENTS}

REQUIREMENTS_BY_PREFIX = {
    "BR": BR_REQUIREMENTS,
    "FR": FR_REQUIREMENTS,
    "NFR": NFR_REQUIREMENTS,
    "BRULE": BRULE_RULES,
    "CR": CR_RULES,
    "OR": OR_RULES,
    "SECR": SECR_REQUIREMENTS,
    "PRIV": PRIV_REQUIREMENTS,
    "PERF": PERF_REQUIREMENTS,
    "AVAIL": AVAIL_REQUIREMENTS,
    "LOC": LOC_REQUIREMENTS,
    "A11Y": A11Y_REQUIREMENTS,
    "OFF": OFF_REQUIREMENTS,
    "REP": REP_REQUIREMENTS,
    "ANL": ANL_REQUIREMENTS,
    "AIR": AIR_REQUIREMENTS,
    "INT": INT_REQUIREMENTS,
}

EXPECTED_COUNTS = {
    "BR": 50,
    "FR": 80,
    "NFR": 50,
    "BRULE": 50,
    "CR": 50,
    "OR": 50,
    "SECR": 50,
    "PRIV": 50,
    "PERF": 40,
    "AVAIL": 40,
    "LOC": 40,
    "A11Y": 40,
    "OFF": 50,
    "REP": 50,
    "ANL": 40,
    "AIR": 40,
    "INT": 50,
}

def get_requirement(req_id: str):
    """Retrieve requirement by ID or None if not found."""
    return REQUIREMENTS_BY_ID.get(req_id)

def get_total_count() -> int:
    """Return total number of requirements loaded."""
    return len(ALL_REQUIREMENTS)

def get_counts_by_prefix() -> dict:
    """Return count of requirements per prefix."""
    return {pfx: len(items) for pfx, items in REQUIREMENTS_BY_PREFIX.items()}

def get_all_ids() -> list:
    """Return sorted list of all requirement IDs."""
    return sorted(REQUIREMENTS_BY_ID.keys())

def get_dependencies_graph() -> dict:
    """Build directed graph of requirement dependencies: req_id -> [dep_ids]."""
    graph = {}
    for r in ALL_REQUIREMENTS:
        req_id = r["id"]
        deps = r.get("dependencies", [])
        if isinstance(deps, str):
            deps = [d.strip() for d in deps.split(",") if d.strip()]
        graph[req_id] = deps
    return graph

if __name__ == "__main__":
    print(f"Loaded {len(ALL_REQUIREMENTS)} total requirements into canonical registry.")
    counts = get_counts_by_prefix()
    for pfx, c in counts.items():
        exp = EXPECTED_COUNTS.get(pfx, 0)
        status = "OK" if c == exp else f"MISMATCH (expected {exp})"
        print(f"  {pfx:6}: {c:3} requirements [{status}]")
