"""
qa_core_data.py
Master QA Canonical Registry for Namma Clinic Phase 11.
Aggregates and validates all QA entities across parts 1 through 4.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.qa.qa_data_part1 import (
    TEST_STRATEGIES, TEST_LEVELS, DEFECT_REGISTRY,
    QUALITY_GATES, ENVIRONMENT_CONFIGS, REGRESSION_SUITES
)
from scripts.qa.qa_data_part2 import TEST_CASES_PART2
from scripts.qa.qa_data_part3 import TEST_CASES_PART3
from scripts.qa.qa_data_part4 import (
    TEST_SCENARIOS, TEST_DATASETS, PERFORMANCE_TESTS,
    SECURITY_TESTS_QA, OFFLINE_TESTS, ACCESSIBILITY_TESTS,
    LOCALIZATION_TESTS, API_TESTS, DATABASE_TESTS,
    UI_TESTS, INTEGRATION_TESTS, UAT_TESTS, PILOT_TESTS
)

# Combine test cases into master catalog (1,050 detailed test cases)
TEST_CASES = TEST_CASES_PART2 + TEST_CASES_PART3

# Lookup dictionaries for O(1) referential integrity
TEST_CASE_MAP = {tc["id"]: tc for tc in TEST_CASES}
TEST_STRATEGY_MAP = {s["id"]: s for s in TEST_STRATEGIES}
TEST_LEVEL_MAP = {l["id"]: l for l in TEST_LEVELS}
QUALITY_GATE_MAP = {g["id"]: g for g in QUALITY_GATES}
SCENARIO_MAP = {sc["id"]: sc for sc in TEST_SCENARIOS}
DATASET_MAP = {ds["id"]: ds for ds in TEST_DATASETS}
DEFECT_MAP = {d["id"]: d for d in DEFECT_REGISTRY}

def verify_qa_registries():
    """Validates that all QA IDs are globally unique with zero duplicates."""
    all_ids = []
    registries = [
        ("TEST_STRATEGIES", TEST_STRATEGIES),
        ("TEST_LEVELS", TEST_LEVELS),
        ("DEFECT_REGISTRY", DEFECT_REGISTRY),
        ("QUALITY_GATES", QUALITY_GATES),
        ("ENVIRONMENT_CONFIGS", ENVIRONMENT_CONFIGS),
        ("REGRESSION_SUITES", REGRESSION_SUITES),
        ("TEST_CASES", TEST_CASES),
        ("TEST_SCENARIOS", TEST_SCENARIOS),
        ("TEST_DATASETS", TEST_DATASETS),
        ("PERFORMANCE_TESTS", PERFORMANCE_TESTS),
        ("SECURITY_TESTS_QA", SECURITY_TESTS_QA),
        ("OFFLINE_TESTS", OFFLINE_TESTS),
        ("ACCESSIBILITY_TESTS", ACCESSIBILITY_TESTS),
        ("LOCALIZATION_TESTS", LOCALIZATION_TESTS),
        ("API_TESTS", API_TESTS),
        ("DATABASE_TESTS", DATABASE_TESTS),
        ("UI_TESTS", UI_TESTS),
        ("INTEGRATION_TESTS", INTEGRATION_TESTS),
        ("UAT_TESTS", UAT_TESTS),
        ("PILOT_TESTS", PILOT_TESTS),
    ]

    total_count = 0
    for name, reg in registries:
        ids = [item["id"] for item in reg]
        if len(ids) != len(set(ids)):
            raise ValueError(f"CRITICAL: Duplicate IDs detected inside registry {name}!")
        all_ids.extend(ids)
        total_count += len(ids)

    if len(all_ids) != len(set(all_ids)):
        from collections import Counter
        dups = [item for item, count in Counter(all_ids).items() if count > 1]
        raise ValueError(f"CRITICAL: Cross-registry duplicate IDs detected: {dups}")

    print(f"[PASS] All {len(registries)} QA registries verified clean: {total_count:,} unique records.")
    return total_count

if __name__ == "__main__":
    verify_qa_registries()
