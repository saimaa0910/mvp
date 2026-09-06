"""
devops_core_data.py
Master registry aggregator for Phase 12 DevOps Engineering Planning & Design Baseline.
Imports and validates all 20 canonical DevOps registries (1,166 unique items).
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.devops.devops_data_part1 import (
    ENV_TIERS, CLOUD_RESOURCES, IAC_MODULES, CI_PIPELINES, CD_PIPELINES
)
from scripts.devops.devops_data_part2 import (
    DOCKER_IMAGES, GIT_POLICIES, PR_GATES, BRANCHING_RULES, SECRETS_MANAGEMENT
)
from scripts.devops.devops_data_part3 import (
    MONITORING_METRICS, LOGGING_STANDARDS, ALERTING_RULES, BACKUP_POLICIES, DISASTER_RECOVERY
)
from scripts.devops.devops_data_part4 import (
    ROLLBACK_STRATEGIES, RELEASE_MANAGEMENT, PRR_CHECKLIST, RUNBOOKS, DEVOPS_GATES
)

ALL_DEVOPS_REGISTRIES = {
    "ENV_TIERS": ENV_TIERS,
    "CLOUD_RESOURCES": CLOUD_RESOURCES,
    "IAC_MODULES": IAC_MODULES,
    "CI_PIPELINES": CI_PIPELINES,
    "CD_PIPELINES": CD_PIPELINES,
    "DOCKER_IMAGES": DOCKER_IMAGES,
    "GIT_POLICIES": GIT_POLICIES,
    "PR_GATES": PR_GATES,
    "BRANCHING_RULES": BRANCHING_RULES,
    "SECRETS_MANAGEMENT": SECRETS_MANAGEMENT,
    "MONITORING_METRICS": MONITORING_METRICS,
    "LOGGING_STANDARDS": LOGGING_STANDARDS,
    "ALERTING_RULES": ALERTING_RULES,
    "BACKUP_POLICIES": BACKUP_POLICIES,
    "DISASTER_RECOVERY": DISASTER_RECOVERY,
    "ROLLBACK_STRATEGIES": ROLLBACK_STRATEGIES,
    "RELEASE_MANAGEMENT": RELEASE_MANAGEMENT,
    "PRR_CHECKLIST": PRR_CHECKLIST,
    "RUNBOOKS": RUNBOOKS,
    "DEVOPS_GATES": DEVOPS_GATES,
}

def validate_registries():
    """Sanity checks: asserts no empty registries and no duplicate entity IDs."""
    total = 0
    all_ids = set()
    for reg_name, items in ALL_DEVOPS_REGISTRIES.items():
        if not items:
            raise ValueError(f"Registry {reg_name} is empty!")
        for item in items:
            iid = item.get("id")
            if not iid:
                raise ValueError(f"Item missing ID in {reg_name}: {item}")
            if iid in all_ids:
                raise ValueError(f"Duplicate ID found across DevOps registries: {iid}")
            all_ids.add(iid)
        total += len(items)
    print(f"[OK] Verified 20 canonical DevOps registries: {total:,} unique entities.")
    return total

if __name__ == "__main__":
    validate_registries()