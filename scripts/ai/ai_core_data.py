"""
ai_core_data.py
Master registry aggregator for Phase 14 AI/ML Engineering & Decision Support.
Imports and validates all 11 canonical AI registries (865 unique items).
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.ai.ai_data_part1 import (
    AI_USE_CASES, MODELS, MODEL_VERSIONS, AI_DATASETS
)
from scripts.ai.ai_data_part2 import (
    FEATURES_ML, EVALUATION_METRICS
)
from scripts.ai.ai_data_part3 import (
    AI_RISKS, AI_CONTROLS
)
from scripts.ai.ai_data_part4 import (
    MONITORING_RULES, HUMAN_APPROVALS, AI_LINEAGE
)

ALL_AI_REGISTRIES = {
    "AI_USE_CASES": AI_USE_CASES,
    "MODELS": MODELS,
    "MODEL_VERSIONS": MODEL_VERSIONS,
    "AI_DATASETS": AI_DATASETS,
    "FEATURES_ML": FEATURES_ML,
    "EVALUATION_METRICS": EVALUATION_METRICS,
    "AI_RISKS": AI_RISKS,
    "AI_CONTROLS": AI_CONTROLS,
    "MONITORING_RULES": MONITORING_RULES,
    "HUMAN_APPROVALS": HUMAN_APPROVALS,
    "AI_LINEAGE": AI_LINEAGE,
}

def validate_registries():
    """Sanity checks: asserts no empty registries and no duplicate entity IDs."""
    total = 0
    all_ids = set()
    for reg_name, items in ALL_AI_REGISTRIES.items():
        if not items:
            raise ValueError(f"Registry {reg_name} is empty!")
        for item in items:
            iid = item.get("id")
            if not iid:
                raise ValueError(f"Item missing ID in {reg_name}: {item}")
            if iid in all_ids:
                raise ValueError(f"Duplicate entity ID detected: {iid} in {reg_name}")
            all_ids.add(iid)
            total += 1
    print(f"AI Registry Validation PASSED: {len(ALL_AI_REGISTRIES)} registries, {total} unique items.")
    return total

if __name__ == "__main__":
    validate_registries()
