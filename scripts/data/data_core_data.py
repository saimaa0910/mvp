"""
data_core_data.py
Master registry aggregator for Phase 13 Data Engineering & Analytics.
Imports and validates all 14 canonical Data registries (1,015 unique items).
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.data.data_data_part1 import (
    DATA_DOMAINS, DATASETS, FACTS, DIMENSIONS, MEASURES
)
from scripts.data.data_data_part2 import (
    KPIS, DQ_RULES, LINEAGE_PATHS
)
from scripts.data.data_data_part3 import (
    ETL_PIPELINES, CDC_STREAMS, DASHBOARDS
)
from scripts.data.data_data_part4 import (
    DATA_PRODUCTS, DATA_OWNERS, GOVERNANCE_CONTROLS, DATA_CONTRACTS
)

ALL_DATA_REGISTRIES = {
    "DATA_DOMAINS": DATA_DOMAINS,
    "DATASETS": DATASETS,
    "FACTS": FACTS,
    "DIMENSIONS": DIMENSIONS,
    "MEASURES": MEASURES,
    "KPIS": KPIS,
    "DQ_RULES": DQ_RULES,
    "LINEAGE_PATHS": LINEAGE_PATHS,
    "ETL_PIPELINES": ETL_PIPELINES,
    "CDC_STREAMS": CDC_STREAMS,
    "DASHBOARDS": DASHBOARDS,
    "DATA_PRODUCTS": DATA_PRODUCTS,
    "DATA_OWNERS": DATA_OWNERS,
    "GOVERNANCE_CONTROLS": GOVERNANCE_CONTROLS,
    "DATA_CONTRACTS": DATA_CONTRACTS,
}

def validate_registries():
    """Sanity checks: asserts no empty registries and no duplicate entity IDs."""
    total = 0
    all_ids = set()
    for reg_name, items in ALL_DATA_REGISTRIES.items():
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
    print(f"Data Registry Validation PASSED: {len(ALL_DATA_REGISTRIES)} registries, {total} unique items.")
    return total

if __name__ == "__main__":
    validate_registries()
