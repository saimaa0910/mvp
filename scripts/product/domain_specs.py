#!/usr/bin/env python3
"""
domain_specs.py
Authoritative definitions for the 6 Product Domains and 30 Core Product Modules
for the Namma Clinic Digital Health & Operations Platform (docs/04-product/).
Aggregates domain specifications across D1 through D6 modules.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from domain_specs_d1 import D1_MODULES
from domain_specs_d2 import D2_MODULES
from domain_specs_d3 import D3_MODULES
from domain_specs_d4 import D4_MODULES
from domain_specs_d5 import D5_MODULES
from domain_specs_d6 import D6_MODULES

DOMAINS = [
    {
        "id": "DOMAIN-001",
        "name": "Core Foundation & Platform Administration",
        "description": "Enterprise multi-tenant substrate providing identity, cryptographic role-based access control, facility organizational hierarchy, staff credentials, and centralized system administration.",
        "objectives": ["OBJECTIVE-001", "OBJECTIVE-003", "OBJECTIVE-009", "OBJECTIVE-014"],
        "scopes": ["SCOPE-001", "SCOPE-002", "INSCOPE-001", "INSCOPE-003", "INSCOPE-015"],
        "modules": ["MODULE-001", "MODULE-002", "MODULE-003", "MODULE-004", "MODULE-026"]
    },
    {
        "id": "DOMAIN-002",
        "name": "Frontline Intake & Citizen Operations",
        "description": "Public-facing citizen touchpoints including bilingual registration, national ABHA ID generation, informed digital consent, biometric deduplication, priority token minting, waiting hall display orchestration, and citizen grievance redressal.",
        "objectives": ["OBJECTIVE-001", "OBJECTIVE-004", "OBJECTIVE-005", "OBJECTIVE-011"],
        "scopes": ["SCOPE-001", "SCOPE-003", "INSCOPE-002", "INSCOPE-006", "INSCOPE-007"],
        "modules": ["MODULE-005", "MODULE-006", "MODULE-007", "MODULE-008", "MODULE-020"]
    },
    {
        "id": "DOMAIN-003",
        "name": "Clinical Care & Diagnostic Orders",
        "description": "Doctor and nurse clinical care delivery systems, electronic health records (EMR), structured SOAP documentation, standard diagnostic coding (ICD-10/SNOMED CT), electronic prescribing with drug safety validation, point-of-care laboratory orders, and telemedicine tele-consultation.",
        "objectives": ["OBJECTIVE-002", "OBJECTIVE-005", "OBJECTIVE-006", "OBJECTIVE-010"],
        "scopes": ["SCOPE-001", "SCOPE-004", "INSCOPE-008", "INSCOPE-009", "INSCOPE-010"],
        "modules": ["MODULE-009", "MODULE-010", "MODULE-011", "MODULE-012", "MODULE-029"]
    },
    {
        "id": "DOMAIN-004",
        "name": "Pharmacy, Dispensing & Inventory Supply Chain",
        "description": "End-to-end pharmaceutical supply chain, point-of-care dispensing with 2D barcode verification, real-time batch and expiry tracking, First-Expiry First-Out (FEFO) stock control, automated indent replenishment, and Essential Medicine List (EML) formulary management.",
        "objectives": ["OBJECTIVE-002", "OBJECTIVE-007", "OBJECTIVE-013"],
        "scopes": ["SCOPE-001", "SCOPE-005", "INSCOPE-011", "INSCOPE-012", "INSCOPE-013"],
        "modules": ["MODULE-013", "MODULE-014", "MODULE-015", "MODULE-016"]
    },
    {
        "id": "DOMAIN-005",
        "name": "Care Continuity, Referrals & Community Outreach",
        "description": "Longitudinal care management connecting primary health clinics to secondary referral hospitals, emergency 108 ambulance transit, chronic Non-Communicable Disease (NCD) follow-up, multichannel citizen reminders (SMS/WhatsApp), and facility operations helpdesk support.",
        "objectives": ["OBJECTIVE-001", "OBJECTIVE-008", "OBJECTIVE-012"],
        "scopes": ["SCOPE-001", "SCOPE-006", "INSCOPE-014", "INSCOPE-016", "INSCOPE-017"],
        "modules": ["MODULE-017", "MODULE-018", "MODULE-019", "MODULE-028"]
    },
    {
        "id": "DOMAIN-006",
        "name": "Intelligence, Governance, Offline & Interoperability",
        "description": "Platform infrastructure, tamper-evident cryptographic WORM audit ledger, municipal epidemiological analytics, clinical decision support AI safeguards, ABDM national health gateway integration, autonomous offline edge mesh, statutory state HMIS reporting, and disaster command center.",
        "objectives": ["OBJECTIVE-003", "OBJECTIVE-009", "OBJECTIVE-010", "OBJECTIVE-015"],
        "scopes": ["SCOPE-002", "SCOPE-007", "INSCOPE-018", "INSCOPE-019", "INSCOPE-020"],
        "modules": ["MODULE-021", "MODULE-022", "MODULE-023", "MODULE-024", "MODULE-025", "MODULE-027", "MODULE-030"]
    }
]

# Assemble all 30 modules
MODULE_SPECS = []
MODULE_SPECS.extend(D1_MODULES)
MODULE_SPECS.extend(D2_MODULES)
MODULE_SPECS.extend(D3_MODULES)
MODULE_SPECS.extend(D4_MODULES)
MODULE_SPECS.extend(D5_MODULES)
MODULE_SPECS.extend(D6_MODULES)

# Mapping dictionaries
DOMAIN_MAP = {d["id"]: d for d in DOMAINS}
MODULE_MAP = {m["id"]: m for m in MODULE_SPECS}

# Submodules and Capabilities flat registries
ALL_SUBMODULES = []
ALL_CAPABILITIES = []

for m in MODULE_SPECS:
    for s in m["submodules"]:
        s_copy = dict(s)
        s_copy["module_id"] = m["id"]
        s_copy["domain_id"] = m["domain_id"]
        ALL_SUBMODULES.append(s_copy)
    for c in m["capabilities"]:
        c_copy = dict(c)
        c_copy["module_id"] = m["id"]
        c_copy["domain_id"] = m["domain_id"]
        ALL_CAPABILITIES.append(c_copy)

SUBMODULE_MAP = {s["id"]: s for s in ALL_SUBMODULES}
CAPABILITY_MAP = {c["id"]: c for c in ALL_CAPABILITIES}

if __name__ == "__main__":
    print(f"Total Domains: {len(DOMAINS)}")
    print(f"Total Modules: {len(MODULE_SPECS)}")
    print(f"Total Submodules: {len(ALL_SUBMODULES)}")
    print(f"Total Capabilities: {len(ALL_CAPABILITIES)}")
    assert len(DOMAINS) == 6, "Expected 6 domains"
    assert len(MODULE_SPECS) == 30, "Expected 30 modules"
    assert len(ALL_SUBMODULES) == 90, "Expected 90 submodules (3 per module)"
    assert len(ALL_CAPABILITIES) == 180, "Expected 180 capabilities (6 per module)"
    print("domain_specs self-check: PASS!")
