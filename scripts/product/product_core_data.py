#!/usr/bin/env python3
"""
product_core_data.py
Authoritative, unified core product registry and data access layer
for the Namma Clinic Digital Health & Operations Platform (docs/04-product/).

This module acts as the single source of truth for all 7 product planning documents:
- 01-product-module-map.md
- 02-module-dependency-map.md
- 03-role-module-matrix.md
- 04-feature-catalog.md
- 05-feature-priority.md
- 06-mvp-definition.md
- 07-release-feature-map.md
and PRODUCT_COMPLETENESS_AUDIT.md.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import domain and module specifications
from domain_specs import (
    DOMAINS,
    MODULE_SPECS,
    DOMAIN_MAP,
    MODULE_MAP,
    ALL_SUBMODULES,
    ALL_CAPABILITIES
)

# Import feature catalogs
from features_d1 import D1_FEATURES
from features_d2 import D2_FEATURES
from features_d3 import D3_FEATURES
from features_d4 import D4_FEATURES
from features_d5 import D5_FEATURES
from features_d6 import D6_FEATURES

# Import dependencies
from dependency_data import (
    DEPENDENCIES,
    DEPENDENCY_MAP,
    check_acyclic_dependencies,
    get_topological_sort
)

# Import role entitlements and matrices
from role_entitlements_data import (
    ROLES_CATALOG,
    ROLE_MAP,
    FULL_ROLE_MODULE_MATRIX,
    SOD_CONSTRAINTS,
    PRIVILEGED_OPERATIONS,
    OFFLINE_GOVERNANCE,
    get_role_module_access
)

# Assemble all 180 features
ALL_FEATURES = []
ALL_FEATURES.extend(D1_FEATURES)
ALL_FEATURES.extend(D2_FEATURES)
ALL_FEATURES.extend(D3_FEATURES)
ALL_FEATURES.extend(D4_FEATURES)
ALL_FEATURES.extend(D5_FEATURES)
ALL_FEATURES.extend(D6_FEATURES)

# Lookup maps
SUBMODULE_MAP = {s["id"]: s for s in ALL_SUBMODULES}
CAPABILITY_MAP = {c["id"]: c for c in ALL_CAPABILITIES}
FEATURE_MAP = {f["id"]: f for f in ALL_FEATURES}

# Aliases
MODULES = MODULE_SPECS
SUBMODULES = ALL_SUBMODULES
CAPABILITIES = ALL_CAPABILITIES
FEATURES = ALL_FEATURES
ROLES = ROLES_CATALOG
ROLE_MODULE_MATRIX = FULL_ROLE_MODULE_MATRIX

# Add aliases and normalize status values to each feature for maximum compatibility
for f in ALL_FEATURES:
    raw_mvp = f.get("mvp_status", "MVP-CORE")
    if raw_mvp in ["CORE MVP", "MVP-CORE"]:
        f["mvp_status"] = "MVP-CORE"
        f["mvp_classification"] = "MVP-CORE"
    else:
        f["mvp_classification"] = raw_mvp
    f["target_release"] = f.get("release_target", "REL-01")

# Summary Metrics
TOTAL_DOMAINS = len(DOMAINS)
TOTAL_MODULES = len(MODULES)
TOTAL_SUBMODULES = len(SUBMODULES)
TOTAL_CAPABILITIES = len(CAPABILITIES)
TOTAL_FEATURES = len(FEATURES)
TOTAL_DEPENDENCIES = len(DEPENDENCIES)
TOTAL_ROLES = len(ROLES)

# Feature distributions
PRIORITY_COUNTS = {
    "P0 - Critical": sum(1 for f in FEATURES if f["priority"].startswith("P0")),
    "P1 - High": sum(1 for f in FEATURES if f["priority"].startswith("P1")),
    "P2 - Medium": sum(1 for f in FEATURES if f["priority"].startswith("P2")),
    "P3 - Low": sum(1 for f in FEATURES if f["priority"].startswith("P3"))
}

MOSCOW_COUNTS = {
    "MUST": sum(1 for f in FEATURES if f["moscow"] == "MUST"),
    "SHOULD": sum(1 for f in FEATURES if f["moscow"] == "SHOULD"),
    "COULD": sum(1 for f in FEATURES if f["moscow"] == "COULD"),
    "WON'T": sum(1 for f in FEATURES if f["moscow"] == "WON'T")
}

MVP_COUNTS = {
    "MVP-CORE": sum(1 for f in FEATURES if f["mvp_status"] == "MVP-CORE"),
    "MVP-PLUS": sum(1 for f in FEATURES if f["mvp_status"] == "MVP-PLUS"),
    "POST-MVP": sum(1 for f in FEATURES if f["mvp_status"] == "POST-MVP")
}

RELEASE_COUNTS = {}
for f in FEATURES:
    rel = f["release_target"]
    RELEASE_COUNTS[rel] = RELEASE_COUNTS.get(rel, 0) + 1

def get_features_by_module(module_id: str):
    """Returns all features belonging to a specific module."""
    return [f for f in FEATURES if f["module_id"] == module_id]

def get_features_by_capability(cap_id: str):
    """Returns all features implementing a specific capability."""
    return [f for f in FEATURES if f["capability_id"] == cap_id]

def get_features_by_mvp(mvp_type: str):
    """Returns all features matching the MVP classification."""
    return [f for f in FEATURES if f["mvp_status"] == mvp_type]

def get_features_by_release(release_id: str):
    """Returns all features targeted for a specific release."""
    return [f for f in FEATURES if f["release_target"] == release_id]

def get_module_dependencies(module_id: str, direction: str = "outgoing"):
    """Returns incoming or outgoing dependencies for a module."""
    if direction == "outgoing":
        return [d for d in DEPENDENCIES if d["source_module"] == module_id]
    elif direction == "incoming":
        return [d for d in DEPENDENCIES if d["target_module"] == module_id]
    else:
        return [d for d in DEPENDENCIES if d["source_module"] == module_id or d["target_module"] == module_id]

if __name__ == "__main__":
    print("==================================================")
    print("NAMMA CLINIC PRODUCT CORE DATA REGISTRY INITIALIZED")
    print("==================================================")
    print(f"Total Domains:       {TOTAL_DOMAINS}")
    print(f"Total Modules:       {TOTAL_MODULES}")
    print(f"Total Submodules:    {TOTAL_SUBMODULES}")
    print(f"Total Capabilities:  {TOTAL_CAPABILITIES}")
    print(f"Total Features:      {TOTAL_FEATURES}")
    print(f"Total Dependencies:  {TOTAL_DEPENDENCIES}")
    print(f"Total Roles:         {TOTAL_ROLES}")
    print("--------------------------------------------------")
    print(f"Priority Breakdown:  {PRIORITY_COUNTS}")
    print(f"MoSCoW Breakdown:    {MOSCOW_COUNTS}")
    print(f"MVP Breakdown:       {MVP_COUNTS}")
    print(f"Release Breakdown:   {sorted(RELEASE_COUNTS.items())}")
    print("--------------------------------------------------")
    is_dag, visited, total = check_acyclic_dependencies()
    print(f"Dependency Acyclicity: {'PASS (DAG)' if is_dag else 'FAIL'} ({visited}/{total} modules sorted)")
    print("==================================================")
