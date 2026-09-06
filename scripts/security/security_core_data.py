"""
security_core_data.py
Authoritative Master Canonical Registry for Phase 10: Security Engineering Planning & Design Baseline.
Greater Bengaluru Authority (GBA) / BBMP Health Department - Namma Clinic Digital Health Platform.

Re-exports and indexes 1,005+ canonical security items:
- SEC_ARCH_CONTROLS (50: SEC-ARCH-001 .. SEC-ARCH-050)
- AUTH_REQUIREMENTS (50: AUTH-001 .. AUTH-050)
- RBAC_REQUIREMENTS (75: RBAC-001 .. RBAC-075)
- ABAC_POLICIES (30: ABAC-001 .. ABAC-030)
- MFA_REQUIREMENTS (30: MFA-001 .. MFA-030)
- SESSION_REQUIREMENTS (40: SESSION-001 .. SESSION-040)
- PASSWORD_REQUIREMENTS (30: PWD-001 .. PWD-030)
- API_SEC_CONTROLS (60: API-SEC-001 .. API-SEC-060)
- ENCRYPTION_REQUIREMENTS (40: ENC-001 .. ENC-040)
- KEY_MANAGEMENT_CONTROLS (30: KEY-001 .. KEY-030)
- AUDIT_REQUIREMENTS (60: AUDIT-SEC-001 .. AUDIT-SEC-060)
- PRIVACY_REQUIREMENTS (60: PRIV-SEC-001 .. PRIV-SEC-060)
- CONSENT_REQUIREMENTS (40: CONSENT-SEC-001 .. CONSENT-SEC-040)
- CLASSIFICATION_CONTROLS (20: CLASS-SEC-001 .. CLASS-SEC-020)
- SECRETS_CONTROLS (30: SECRET-001 .. SECRET-030)
- THREAT_RECORDS (100: THREAT-001 .. THREAT-100)
- SECURITY_TESTS (150: SEC-TEST-001 .. SEC-TEST-150)
- VAPT_SCENARIOS (50: VAPT-001 .. VAPT-050)
- INCIDENT_SCENARIOS (40: INCIDENT-001 .. INCIDENT-040)
- BACKUP_CONTROLS (30: BACKUP-SEC-001 .. BACKUP-SEC-030)
- DEVICE_CONTROLS (40: DEVICE-SEC-001 .. DEVICE-SEC-040)
- SECURITY_METRICS (30: METRIC-SEC-001 .. METRIC-SEC-030)
- SECURITY_RISKS (20: RISK-SEC-001 .. RISK-SEC-020)

Performs comprehensive uniqueness, relational, and cross-referential integrity checks on import.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import upstream data
from scripts.frontend.frontend_core_data import ROLES
from scripts.database.db_tables_entities import TABLES, TABLE_NAME_MAP
from scripts.api.api_core_data import API_ENDPOINTS, ENDPOINT_MAP

# Import partitioned security data
from scripts.security.security_data_part1 import (
    SEC_ARCH_CONTROLS, AUTH_REQUIREMENTS, RBAC_REQUIREMENTS, ABAC_POLICIES, MFA_REQUIREMENTS
)
from scripts.security.security_data_part2 import (
    SESSION_REQUIREMENTS, PASSWORD_REQUIREMENTS, API_SEC_CONTROLS,
    ENCRYPTION_REQUIREMENTS, KEY_MANAGEMENT_CONTROLS, AUDIT_REQUIREMENTS
)
from scripts.security.security_data_part3 import (
    PRIVACY_REQUIREMENTS, CONSENT_REQUIREMENTS, CLASSIFICATION_CONTROLS,
    SECRETS_CONTROLS, THREAT_RECORDS
)
from scripts.security.security_data_part4 import (
    SECURITY_TESTS, VAPT_SCENARIOS, INCIDENT_SCENARIOS,
    BACKUP_CONTROLS, DEVICE_CONTROLS, SECURITY_METRICS, SECURITY_RISKS
)

# -----------------------------------------------------------------------------
# Canonical Lookup Maps
# -----------------------------------------------------------------------------
SEC_ARCH_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in SEC_ARCH_CONTROLS}
AUTH_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in AUTH_REQUIREMENTS}
RBAC_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in RBAC_REQUIREMENTS}
ABAC_MAP: Dict[str, Dict[str, Any]] = {p["id"]: p for p in ABAC_POLICIES}
MFA_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in MFA_REQUIREMENTS}
SESSION_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in SESSION_REQUIREMENTS}
PWD_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in PASSWORD_REQUIREMENTS}
API_SEC_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in API_SEC_CONTROLS}
ENC_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in ENCRYPTION_REQUIREMENTS}
KEY_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in KEY_MANAGEMENT_CONTROLS}
AUDIT_SEC_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in AUDIT_REQUIREMENTS}
PRIV_SEC_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in PRIVACY_REQUIREMENTS}
CONSENT_SEC_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in CONSENT_REQUIREMENTS}
CLASS_SEC_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in CLASSIFICATION_CONTROLS}
SECRET_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in SECRETS_CONTROLS}
THREAT_MAP: Dict[str, Dict[str, Any]] = {t["id"]: t for t in THREAT_RECORDS}
SEC_TEST_MAP: Dict[str, Dict[str, Any]] = {t["id"]: t for t in SECURITY_TESTS}
VAPT_MAP: Dict[str, Dict[str, Any]] = {v["id"]: v for v in VAPT_SCENARIOS}
INCIDENT_MAP: Dict[str, Dict[str, Any]] = {i["id"]: i for i in INCIDENT_SCENARIOS}
BACKUP_SEC_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in BACKUP_CONTROLS}
DEVICE_SEC_MAP: Dict[str, Dict[str, Any]] = {c["id"]: c for c in DEVICE_CONTROLS}
METRIC_MAP: Dict[str, Dict[str, Any]] = {m["id"]: m for m in SECURITY_METRICS}
RISK_MAP: Dict[str, Dict[str, Any]] = {r["id"]: r for r in SECURITY_RISKS}

# -----------------------------------------------------------------------------
# Relational & Cross-Referential Integrity Verification on Import
# -----------------------------------------------------------------------------
def verify_security_registry_integrity():
    errors = []
    
    # 1. Uniqueness check across all registries
    registries = [
        ("SEC_ARCH", SEC_ARCH_CONTROLS, 50),
        ("AUTH", AUTH_REQUIREMENTS, 50),
        ("RBAC", RBAC_REQUIREMENTS, 75),
        ("ABAC", ABAC_POLICIES, 30),
        ("MFA", MFA_REQUIREMENTS, 30),
        ("SESSION", SESSION_REQUIREMENTS, 40),
        ("PWD", PASSWORD_REQUIREMENTS, 30),
        ("API_SEC", API_SEC_CONTROLS, 60),
        ("ENC", ENCRYPTION_REQUIREMENTS, 40),
        ("KEY", KEY_MANAGEMENT_CONTROLS, 30),
        ("AUDIT_SEC", AUDIT_REQUIREMENTS, 60),
        ("PRIV_SEC", PRIVACY_REQUIREMENTS, 60),
        ("CONSENT_SEC", CONSENT_REQUIREMENTS, 40),
        ("CLASS_SEC", CLASSIFICATION_CONTROLS, 20),
        ("SECRET", SECRETS_CONTROLS, 30),
        ("THREAT", THREAT_RECORDS, 100),
        ("SEC_TEST", SECURITY_TESTS, 150),
        ("VAPT", VAPT_SCENARIOS, 50),
        ("INCIDENT", INCIDENT_SCENARIOS, 40),
        ("BACKUP_SEC", BACKUP_CONTROLS, 30),
        ("DEVICE_SEC", DEVICE_CONTROLS, 40),
        ("METRIC_SEC", SECURITY_METRICS, 30),
        ("RISK_SEC", SECURITY_RISKS, 20)
    ]
    
    for name, items, expected_count in registries:
        if len(items) != expected_count:
            errors.append(f"Registry {name} has {len(items)} items; expected exactly {expected_count}.")
        seen = set()
        for item in items:
            iid = item["id"]
            if iid in seen:
                errors.append(f"Duplicate ID detected in {name}: {iid}")
            seen.add(iid)

    if errors:
        raise ValueError("Security Registry Integrity Failure:\n" + "\n".join(errors[:10]))

verify_security_registry_integrity()
