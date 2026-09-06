"""
db_core_data.py
Canonical Central Data Registry for Phase 07 Database Engineering Planning & Design.
Authoritative machine-readable source of truth for:
- 52 Relational Tables (TABLE-001 to TABLE-052)
- 52 Conceptual Entities (ENTITY-001 to ENTITY-052)
- 832 Detailed Columns (COLUMN-001 to COLUMN-832)
- 112 PK/FK Relationships (REL-001 to REL-112)
- 132 Database Indexes (INDEX-001 to INDEX-132)
- 12 Partition Specifications (PART-001 to PART-012)
- 30 Audit Entities & Events (AUDIT-ENTITY-001..030, AUDIT-EVENT-001..030)
- 25 Critical Transaction Models (TXN-001 to TXN-025)
- 20 Data Retention Rules (RETENTION-001 to RETENTION-020)
- 5 Classification Tiers (CLASS-001 to CLASS-005)
- 30 Migration Blueprints (MIG-001 to MIG-030)
- 15 Seed Datasets (SEED-001 to SEED-015)
- 10 OLAP Fact Tables (FACT-001 to FACT-010)
- 12 OLAP Dimensions (DIM-001 to DIM-012)
- 50 Analytical Measures (MEASURE-001 to MEASURE-050)
- 50 Data Quality Rules (DQ-001 to DQ-050)
- 25 Data Lineage Pathways (LINEAGE-001 to LINEAGE-025)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from typing import Dict, List, Any

# -----------------------------------------------------------------------------
# 1. CLASSIFICATION TIERS (CLASS-001 to CLASS-005)
# -----------------------------------------------------------------------------
CLASSIFICATIONS = [
    {
        "id": "CLASS-001",
        "code": "PUBLIC",
        "name": "Public Data",
        "description": "Information approved for unrestricted public distribution, including clinic directory, public health advisories, standard operating hours, and published formulary lists.",
        "storage": "Standard EBS GP3 / Read-Replica Cache / CDN",
        "encryption_at_rest": "AES-256 (Standard TDE)",
        "encryption_in_transit": "TLS 1.3",
        "access_control": "Anonymous / Public Read",
        "masking": "No masking required",
        "export_policy": "Freely exportable via Open Data API",
        "retention_default": "Indefinite / Superseded on revision"
    },
    {
        "id": "CLASS-002",
        "code": "INTERNAL",
        "name": "Internal Operational Data",
        "description": "Routine municipal operational records, staff rosters, shift schedules, hardware inventory, and aggregate non-clinical operational metrics.",
        "storage": "Encrypted PostgreSQL Database Cluster",
        "encryption_at_rest": "AES-256-GCM with Vault Key Management",
        "encryption_in_transit": "TLS 1.3 with mTLS for internal microservices",
        "access_control": "Authenticated Staff / RBAC Level 1+",
        "masking": "No masking for authorized staff",
        "export_policy": "Restricted to internal reporting pipelines",
        "retention_default": "3 to 5 years based on municipal financial audit rules"
    },
    {
        "id": "CLASS-003",
        "code": "CONFIDENTIAL",
        "name": "Confidential Clinical & Administrative Data",
        "description": "De-identified patient clinical encounters, prescription histories, non-sensitive diagnostic test orders, and anonymized research extracts.",
        "storage": "Encrypted PostgreSQL Database Cluster / Read Replicas",
        "encryption_at_rest": "AES-256-GCM with Envelope Encryption",
        "encryption_in_transit": "TLS 1.3 Strict Cipher Suites",
        "access_control": "Role-Based Access Control (Clinicians, Pharmacists, Lab Techs)",
        "masking": "Partial masking (Aadhaar last 4, mobile masked) on UI",
        "export_policy": "Requires Clinical Director approval; WORM audit logged",
        "retention_default": "10 years statutory retention for outpatient records"
    },
    {
        "id": "CLASS-004",
        "code": "RESTRICTED",
        "name": "Restricted Personally Identifiable Information (PII)",
        "description": "Direct citizen demographic identifiers including full names, Aadhaar numbers, phone numbers, residential addresses, and biometric metadata.",
        "storage": "Isolated Private Database Subnet / Column-Level Cryptography",
        "encryption_at_rest": "Column-level AES-256-GCM + Blind Indexing (HMAC-SHA256)",
        "encryption_in_transit": "TLS 1.3 with Certificate Pinning",
        "access_control": "Strict Least Privilege / Registration Staff & Treating Doctor Only",
        "masking": "Strict masking on all admin & report interfaces: XXXXXXXX1234",
        "export_policy": "Prohibited from bulk export; strictly gated by DPDP Act 2023",
        "retention_default": "Duration of active care + statutory consent window"
    },
    {
        "id": "CLASS-005",
        "code": "HIGHLY-RESTRICTED",
        "name": "Highly Restricted Sensitive Personal Health Data & Secrets",
        "description": "Sensitive clinical conditions (HIV, reproductive health, psychiatric notes), master cryptographic keys, Argon2id credentials, and WORM root hashes.",
        "storage": "Air-Gapped Vault KMS / Dedicated Cryptographic Security Enclave",
        "encryption_at_rest": "Hardware Security Module (HSM) FIPS 140-2 Level 3 Root Keys",
        "encryption_in_transit": "TLS 1.3 mTLS with Zero-Trust Network Microsegmentation",
        "access_control": "Break-Glass Multi-Party Authorization / Treating Doctor Sole Grant",
        "masking": "Full cryptographic redaction unless explicit break-glass invoked",
        "export_policy": "Absolute export prohibition; legally protected statutory category",
        "retention_default": "Permanent immutable audit trail / Clinical record 10+ years"
    }
]
CLASSIFICATION_MAP = {c["id"]: c for c in CLASSIFICATIONS}
CLASS_CODE_MAP = {c["code"]: c for c in CLASSIFICATIONS}

# -----------------------------------------------------------------------------
# 2. RETENTION RULES (RETENTION-001 to RETENTION-020)
# -----------------------------------------------------------------------------
RETENTION_RULES = [
    {"id": "RETENTION-001", "name": "Adult Outpatient Clinical Records", "duration_years": 10, "min_days": 3650, "policy": "Active online 3 years; archived to compressed WORM S3 cold storage 7 years; permanent hash ledger.", "legal_basis": "National Medical Commission (NMC) Guidelines & BBMP Healthcare Bylaws"},
    {"id": "RETENTION-002", "name": "Pediatric Clinical Records", "duration_years": 21, "min_days": 7670, "policy": "Retained until child reaches age of majority (18 years) plus 3 years limitation period.", "legal_basis": "Indian Limitation Act 1963 & Protection of Children Health Guidelines"},
    {"id": "RETENTION-003", "name": "Electronic Prescriptions & Dispensation Logs", "duration_years": 5, "min_days": 1825, "policy": "Stored in PostgreSQL online database 2 years; moved to columnar compressed archive 3 years.", "legal_basis": "Pharmacy Practice Regulations & Drugs and Cosmetics Act 1940"},
    {"id": "RETENTION-004", "name": "Diagnostic Laboratory Results & Panic Logs", "duration_years": 10, "min_days": 3650, "policy": "Retained online for longitudinal trend analysis across repeat patient visits.", "legal_basis": "Clinical Establishments (Registration and Regulation) Act"},
    {"id": "RETENTION-005", "name": "Citizen Consent Artifacts & Revocations", "duration_years": 7, "min_days": 2555, "policy": "Retained for duration of consent plus 7 years post-revocation for evidentiary audit.", "legal_basis": "Digital Personal Data Protection (DPDP) Act 2023 Section 6"},
    {"id": "RETENTION-006", "name": "Immutable Cryptographic WORM Audit Trails", "duration_years": 10, "min_days": 3650, "policy": "Never deleted; append-only SHA-256 HMAC hash chained log; archived to Glacier Object Lock.", "legal_basis": "Information Technology Act 2000 Section 7A & DPDP Act Section 8"},
    {"id": "RETENTION-007", "name": "Daily Queue Tokens & Waiting Hall State", "duration_years": 0.25, "min_days": 90, "policy": "Retained in operational database 90 days; aggregated into daily KPI metrics; purged quarterly.", "legal_basis": "BBMP Health Operations SLA Standard"},
    {"id": "RETENTION-008", "name": "Cold-Chain IoT Sensor Temperature Telemetry", "duration_years": 3, "min_days": 1095, "policy": "Raw 60-second readings stored in ClickHouse 180 days; aggregated hourly averages kept 3 years.", "legal_basis": "Universal Immunization Programme (UIP) Cold Chain Guidelines"},
    {"id": "RETENTION-009", "name": "Pharmacy Stock Movements & Indent Receipts", "duration_years": 8, "min_days": 2920, "policy": "Complete double-entry inventory ledger retained for statutory financial and CAG audits.", "legal_basis": "Karnataka Transparency in Public Procurements (KTPP) Act & CAG Audit Rules"},
    {"id": "RETENTION-010", "name": "Secondary Hospital Referral Dossiers", "duration_years": 10, "min_days": 3650, "policy": "Retained in clinical continuity registry; linked to patient longitudinal health record.", "legal_basis": "ABDM Continuity of Care & Emergency Medical Referral Policy"},
    {"id": "RETENTION-011", "name": "Staff Authentication Sessions & Access Tokens", "duration_years": 1, "min_days": 365, "policy": "Active sessions expired after 15m idle; token revocation history retained 1 year for forensics.", "legal_basis": "CERT-In Cyber Security Directions 2022"},
    {"id": "RETENTION-012", "name": "Edge Offline Mutation Journal Logs", "duration_years": 0.5, "min_days": 180, "policy": "Retained on edge appliance 30 days post successful cloud reconciliation; pruned automatically.", "legal_basis": "Platform Offline Architecture Standard ARCH-OFF-09"},
    {"id": "RETENTION-013", "name": "Non-Communicable Disease (NCD) Registries", "duration_years": 15, "min_days": 5475, "policy": "Longitudinal hypertension and diabetes care plans retained for lifetime of patient management.", "legal_basis": "National Programme for Prevention & Control of NCDs (NP-NCD)"},
    {"id": "RETENTION-014", "name": "Citizen Grievances & Resolution Records", "duration_years": 5, "min_days": 1825, "policy": "Full grievance lifecycle, ombudsman notes, and resolution actions retained 5 years.", "legal_basis": "Karnataka Sakala Services Act 2011"},
    {"id": "RETENTION-015", "name": "Outbound Citizen SMS & WhatsApp Notifications", "duration_years": 1, "min_days": 365, "policy": "Dispatched message metadata, delivery receipts, and carrier reference IDs retained 12 months.", "legal_basis": "TRAI Telecom Commercial Communications Regulations"},
    {"id": "RETENTION-016", "name": "Teleconsultation Session Metadata & Joint Notes", "duration_years": 10, "min_days": 3650, "policy": "Doctor-to-specialist teleconsultation logs, duration, and clinical decisions retained 10 years.", "legal_basis": "Telemedicine Practice Guidelines (Board of Governors in supersession of MCI)"},
    {"id": "RETENTION-017", "name": "Database Backup Snapshots (WAL & Full)", "duration_years": 7, "min_days": 2555, "policy": "Continuous WAL 35 days; weekly full snapshots 1 year; annual golden archives 7 years.", "legal_basis": "Disaster Recovery Framework ARCH-DR-14"},
    {"id": "RETENTION-018", "name": "Clinical AI Advisory Prediction Records", "duration_years": 5, "min_days": 1825, "policy": "AI inference inputs, confidence scores, and physician accept/override actions kept 5 years.", "legal_basis": "AI Governance Framework ARCH-AI-12 & DPDP Act Algorithmic Accountability"},
    {"id": "RETENTION-019", "name": "Facility Hardware Fault & Maintenance Logs", "duration_years": 3, "min_days": 1095, "policy": "Equipment breakdown tickets, peripheral replacements, and SLA penalties kept 3 years.", "legal_basis": "BBMP Health Infrastructure Asset Management Policy"},
    {"id": "RETENTION-020", "name": "Statutory HMIS Monthly Health Indicator Reports", "duration_years": 10, "min_days": 3650, "policy": "Monthly ward-level public health disease surveillance returns retained 10 years.", "legal_basis": "Integrated Disease Surveillance Programme (IDSP) & National Health Mission"}
]
RETENTION_MAP = {r["id"]: r for r in RETENTION_RULES}

# -----------------------------------------------------------------------------
# 3. RE-EXPORT MODULAR REGISTRIES
# -----------------------------------------------------------------------------
from scripts.database.db_tables_entities import (
    TABLES, TABLE_MAP, TABLE_NAME_MAP,
    ENTITIES, ENTITY_MAP, ENTITY_NAME_MAP
)

from scripts.database.db_columns import (
    COLUMNS, COLUMN_MAP, TABLE_COLUMNS_MAP
)

from scripts.database.db_relations_indexes import (
    RELATIONSHIPS, RELATIONSHIP_MAP,
    INDEXES, INDEX_MAP,
    PARTITIONS, PARTITION_MAP
)

from scripts.database.db_audit_txns import (
    AUDIT_ENTITIES, AUDIT_ENTITY_MAP,
    AUDIT_EVENTS, AUDIT_EVENT_MAP,
    TRANSACTIONS, TRANSACTION_MAP
)

from scripts.database.db_migrations_seeds import (
    MIGRATIONS, MIGRATION_MAP,
    SEEDS, SEED_MAP
)

from scripts.database.db_olap_dq_lineage import (
    FACTS, FACT_MAP,
    DIMENSIONS, DIMENSION_MAP,
    MEASURES, MEASURE_MAP,
    DQ_RULES, DQ_MAP,
    LINEAGE_PATHS, LINEAGE_MAP
)

# -----------------------------------------------------------------------------
# 4. CROSS-REFERENTIAL INTEGRITY CHECKS (RUN ON IMPORT)
# -----------------------------------------------------------------------------
def verify_registry_integrity():
    errors = []
    # Check FK relationships reference valid parent and child tables
    for rel in RELATIONSHIPS:
        if rel["parent"] not in TABLE_NAME_MAP:
            errors.append(f"Relationship {rel['id']} parent table '{rel['parent']}' not found in TABLES.")
        if rel["child"] not in TABLE_NAME_MAP:
            errors.append(f"Relationship {rel['id']} child table '{rel['child']}' not found in TABLES.")

    # Check Indexes reference valid tables
    for idx in INDEXES:
        if idx["table_name"] not in TABLE_NAME_MAP:
            errors.append(f"Index {idx['id']} table '{idx['table_name']}' not found in TABLES.")

    # Check Partitions reference valid tables
    for part in PARTITIONS:
        if part["table_name"] not in TABLE_NAME_MAP:
            errors.append(f"Partition {part['id']} table '{part['table_name']}' not found in TABLES.")

    # Check Columns reference valid tables
    for col in COLUMNS:
        if col["table_name"] not in TABLE_NAME_MAP:
            errors.append(f"Column {col['id']} table '{col['table_name']}' not found in TABLES.")

    if errors:
        raise ValueError("Registry integrity verification failed:\n" + "\n".join(errors[:10]))

verify_registry_integrity()

if __name__ == "__main__":
    print("================================================================================")
    print("NAMMA CLINIC DATABASE ENGINEERING CANONICAL REGISTRY")
    print("================================================================================")
    print(f"Classifications   : {len(CLASSIFICATIONS)} tiers (CLASS-001..CLASS-{len(CLASSIFICATIONS):03d})")
    print(f"Retention Rules   : {len(RETENTION_RULES)} rules (RETENTION-001..RETENTION-{len(RETENTION_RULES):03d})")
    print(f"Tables            : {len(TABLES)} tables (TABLE-001..TABLE-{len(TABLES):03d})")
    print(f"Entities          : {len(ENTITIES)} entities (ENTITY-001..ENTITY-{len(ENTITIES):03d})")
    print(f"Columns           : {len(COLUMNS)} columns (COLUMN-001..COLUMN-{len(COLUMNS):03d})")
    print(f"Relationships     : {len(RELATIONSHIPS)} relationships (REL-001..REL-{len(RELATIONSHIPS):03d})")
    print(f"Indexes           : {len(INDEXES)} indexes (INDEX-001..INDEX-{len(INDEXES):03d})")
    print(f"Partitions        : {len(PARTITIONS)} partitions (PART-001..PART-{len(PARTITIONS):03d})")
    print(f"Audit Entities    : {len(AUDIT_ENTITIES)} audit entities (AUDIT-ENTITY-001..030)")
    print(f"Audit Events      : {len(AUDIT_EVENTS)} audit events (AUDIT-EVENT-001..030)")
    print(f"Transactions      : {len(TRANSACTIONS)} models (TXN-001..TXN-{len(TRANSACTIONS):03d})")
    print(f"Migrations        : {len(MIGRATIONS)} blueprints (MIG-001..MIG-{len(MIGRATIONS):03d})")
    print(f"Seeds             : {len(SEEDS)} datasets (SEED-001..SEED-{len(SEEDS):03d})")
    print(f"OLAP Facts        : {len(FACTS)} fact tables (FACT-001..FACT-{len(FACTS):03d})")
    print(f"OLAP Dimensions   : {len(DIMENSIONS)} dimensions (DIM-001..DIM-{len(DIMENSIONS):03d})")
    print(f"OLAP Measures     : {len(MEASURES)} measures (MEASURE-001..MEASURE-{len(MEASURES):03d})")
    print(f"Data Quality Rules: {len(DQ_RULES)} rules (DQ-001..DQ-{len(DQ_RULES):03d})")
    print(f"Lineage Pathways  : {len(LINEAGE_PATHS)} paths (LINEAGE-001..LINEAGE-{len(LINEAGE_PATHS):03d})")
    print("================================================================================")
    print("All cross-referential integrity checks passed 100%!")
