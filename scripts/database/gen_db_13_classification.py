"""
gen_db_13_classification.py
Generates docs/07-database/13-data-classification.md
Target: 2,500 - 3,500 substantive lines.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from scripts.database.db_core_data import (
    CLASSIFICATIONS, CLASSIFICATION_MAP, CLASS_CODE_MAP,
    TABLES, TABLE_NAME_MAP, COLUMNS, TABLE_COLUMNS_MAP
)
from scripts.database.db_gen_common import write_db_doc

def generate_doc_13():
    lines = []

    lines.append("# Phase 07 — Data Classification, Column Encryption & Masking Architecture")
    lines.append("")
    lines.append("> **Document Identifier**: `DB-CLS-001`  ")
    lines.append("> **System**: Namma Clinic Digital Health & Operations Platform  ")
    lines.append("> **Municipal Authority**: Greater Bengaluru Authority (GBA) / BBMP Health Department  ")
    lines.append("> **Status**: APPROVED SECURITY & PRIVACY BASELINE  ")
    lines.append(f"> **Classification Framework**: 5 Canonical Tiers (`CLASS-001` to `CLASS-{len(CLASSIFICATIONS):03d}`)  ")
    lines.append(f"> **Governed Data Assets**: 52 Relational Tables, {len(COLUMNS)} Cataloged Columns  ")
    lines.append("> **Statutory Governance**: Digital Personal Data Protection (DPDP) Act 2023, ISO/IEC 27001:2022, CERT-In Directions 2022, DISHA Guidelines  ")
    lines.append("> **Notice**: All SQL blocks contained herein are strictly **DOCUMENTATION-ONLY SQL**. Zero runtime code or migrations are executed during this phase.  ")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 1. Executive Summary & Security Governance
    lines.append("## 1. Executive Summary & Information Security Governance")
    lines.append("")
    lines.append("The Namma Clinic Digital Health & Operations Platform operates across 450 municipal health clinics, processing sensitive citizen demographic information, diagnostic laboratory findings, and longitudinal medical consultations for millions of Bengaluru residents. In strict compliance with the **Digital Personal Data Protection (DPDP) Act 2023**, the platform implements defense-in-depth data protection at the database storage layer.")
    lines.append("")
    lines.append("Data classification constitutes the foundational discipline of information security: without granular classification of data elements, security controls cannot be applied proportionally, leading either to severe privacy breaches or paralyzing operational friction. This specification establishes the definitive data classification standard for the platform across 5 canonical security tiers (`CLASS-001` to `CLASS-005`).")
    lines.append("")
    lines.append("Every single column across all 52 relational tables ({0} total attributes) is mapped to an explicit classification tier, encryption standard, dynamic masking policy, and role-based access level. Furthermore, this document details the cryptographic engineering architecture supporting column-level envelope encryption, HMAC-SHA256 blind indexing for searchable ciphertext, dynamic data masking (DDM), and developer sanitization protocols.")
    lines.append("".format(len(COLUMNS)))

    # 2. Canonical 5-Tier Classification Taxonomy
    lines.append("## 2. Canonical 5-Tier Data Classification Taxonomy")
    lines.append("")
    lines.append("The platform organizes all stored data into five mutually exclusive classification tiers:")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph TD")
    lines.append("    A[CLASS-001: PUBLIC<br/>Unrestricted Public Data] --> B[CLASS-002: INTERNAL<br/>Routine Municipal Operations]")
    lines.append("    B --> C[CLASS-003: CONFIDENTIAL<br/>De-Identified Clinical & Orders]")
    lines.append("    C --> D[CLASS-004: RESTRICTED<br/>Personally Identifiable Info PII]")
    lines.append("    D --> E[CLASS-005: HIGHLY-RESTRICTED<br/>Sensitive Health Data & Secrets]")
    lines.append("```")
    lines.append("")
    lines.append("### 2.1 Classification Tier Profiles & Technical Controls")
    lines.append("")
    lines.append("| Tier ID | Tier Code | Formal Designation | Data Sensitivity & Impact of Breach | Encryption Standard | Dynamic Masking Rule | Export Policy |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for c in CLASSIFICATIONS:
        lines.append(f"| **{c['id']}** | `{c['code']}` | **{c['name']}** | {c['description'][:75]}... | {c['encryption_at_rest']} | {c['masking']} | {c['export_policy']} |")
    lines.append("")

    # 2.2 Comprehensive Tier Deep-Dives
    for c in CLASSIFICATIONS:
        cid = c["id"]
        code = c["code"]
        cname = c["name"]
        lines.append(f"### 2.{cid.split('-')[1]} {cid}: {cname} (`{code}`)")
        lines.append(f"- **Scope & Definition**: {c['description']}")
        lines.append(f"- **Storage Infrastructure**: {c['storage']}")
        lines.append(f"- **Encryption at Rest**: {c['encryption_at_rest']}")
        lines.append(f"- **Encryption in Transit**: {c['encryption_in_transit']}")
        lines.append(f"- **Access Control Model**: {c['access_control']}")
        lines.append(f"- **Presentation Layer Masking**: {c['masking']}")
        lines.append(f"- **Data Export Controls**: {c['export_policy']}")
        lines.append(f"- **Baseline Statutory Retention**: {c['retention_default']}")
        lines.append("")

    # 3. Column-Level Cryptographic Architecture & Searchable Encryption
    lines.append("## 3. Column-Level Cryptographic Architecture & Blind Indexing")
    lines.append("")
    lines.append("Standard transparent database encryption (TDE / EBS encryption) protects data at rest against physical disk theft. However, TDE provides zero protection against compromised database administrator credentials, SQL injection, or overprivileged application services. To neutralize these threats, the Namma Clinic platform enforces **Column-Level Envelope Encryption** combined with **HMAC Blind Indexing**.")
    lines.append("")
    lines.append("### 3.1 Column Envelope Encryption Mechanics")
    lines.append("Sensitive columns (e.g. `full_name_encrypted`, `phone_encrypted`, `clinical_notes_encrypted`) are encrypted in the application layer before reaching PostgreSQL using AES-256-GCM. The encryption key hierarchy operates as follows:")
    lines.append("1. **Master Key (KEK)**: Stored in a FIPS 140-2 Level 3 Hardware Security Module (HSM) managed by AWS KMS / HashiCorp Vault.")
    lines.append("2. **Data Encryption Key (DEK)**: Generated per tenant/facility and rotated every 90 days. Cached in-memory within secure microservice enclaves.")
    lines.append("3. **Ciphertext Envelope**: The stored column holds `base64(iv:tag:ciphertext:dek_version)`.")
    lines.append("")
    lines.append("### 3.2 Searchable Blind Indexing Architecture")
    lines.append("Because AES-256-GCM uses non-deterministic initialization vectors (IVs), encrypted columns cannot be queried directly with equality filters (`WHERE phone = ...`). Decrypting millions of rows on the server would degrade latency and expose plaintext in database memory.")
    lines.append("")
    lines.append("The platform resolves this using **HMAC-SHA256 Blind Indexing**:")
    lines.append("- For each searchable restricted attribute (such as phone number or ABHA ID), a companion column is created: `phone_blind_index` (`bytea`).")
    lines.append("- The blind index is computed as: `HMAC_SHA256(normalize(phone), secret_indexing_salt)`.")
    lines.append("- When searching for a patient, the client hashes the input phone using the blind salt and issues: `WHERE phone_blind_index = $1`.")
    lines.append("- The blind index column has a standard B-Tree index, executing searches in sub-millisecond Index Scan time while revealing zero plaintext to database eavesdroppers.")
    lines.append("")

    # 4. Dynamic Data Masking (DDM) & Row-Level Security
    lines.append("## 4. Dynamic Data Masking (DDM) & Row-Level Security Architecture")
    lines.append("")
    lines.append("Dynamic Data Masking obfuscates sensitive data in real time based on the requesting user's identity and privilege tier:")
    lines.append("")
    lines.append("```sql")
    lines.append("-- DOCUMENTATION-ONLY SQL: Dynamic Masking View for Patient Demographic Data")
    lines.append("CREATE OR REPLACE VIEW clinical.v_patients_masked AS")
    lines.append("SELECT")
    lines.append("    p.id,")
    lines.append("    p.facility_id,")
    lines.append("    -- Unrestricted for treating clinician, masked for clerical and reporting users")
    lines.append("    CASE")
    lines.append("        WHEN current_setting('request.jwt.role', true) IN ('DOCTOR', 'NURSE') THEN p.full_name")
    lines.append("        ELSE regexp_replace(p.full_name, '(?<=^.{2}).(?=.*$)', '*', 'g')")
    lines.append("    END AS full_name,")
    lines.append("    -- Mask mobile number: 9876543210 -> XXXXXX3210")
    lines.append("    CASE")
    lines.append("        WHEN current_setting('request.jwt.role', true) IN ('DOCTOR', 'REGISTRATION_CLERK') THEN p.phone_number")
    lines.append("        ELSE 'XXXXXX' || right(p.phone_number, 4)")
    lines.append("    END AS phone_number,")
    lines.append("    -- Mask Aadhaar / ABHA: 1234-5678-9012 -> XXXX-XXXX-9012")
    lines.append("    'XXXX-XXXX-' || right(p.abha_id, 4) AS abha_masked,")
    lines.append("    p.gender,")
    lines.append("    p.date_of_birth,")
    lines.append("    p.created_at")
    lines.append("FROM patients.patients p")
    lines.append("WHERE p.facility_id = current_setting('request.jwt.facility_id', true)::uuid;")
    lines.append("```")
    lines.append("")

    # 5. Master Column Data Classification Catalog (All 52 Tables, 832 Columns)
    lines.append("## 5. Master Column Classification & Security Catalog (All 52 Tables)")
    lines.append("")
    lines.append("Below is the exhaustive, column-by-column security classification catalog for all 52 relational tables and 832 attributes in the Namma Clinic Platform:")
    lines.append("")

    for tbl in TABLES:
        tname = tbl["name"]
        tschema = tbl["schema"]
        tid = tbl["id"]
        cols = TABLE_COLUMNS_MAP.get(tname, [])
        
        lines.append(f"### 5.{tid.split('-')[1]} `{tschema}.{tname}` ({tid})")
        lines.append(f"- **Schema Domain**: `{tschema}` | **Primary Business Role**: {tbl['description']}")
        lines.append(f"- **Total Cataloged Attributes**: {len(cols)} columns")
        lines.append("")
        lines.append("| Column Name | SQL Type | Classification Tier | Cryptographic Control | Presentation Masking | Authorized Roles |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        
        for c in cols:
            c_name = c["column_name"]
            c_type = c["pg_type"]
            c_cls = c["classification"]
            c_enc = c["encryption_req"]
            c_mask = c["masking_req"]
            
            # Formulate authorized role based on classification
            if c_cls in ["CLASS-001", "PUBLIC"]:
                auth_role = "Anonymous, Public, All Staff"
            elif c_cls in ["CLASS-002", "INTERNAL"]:
                auth_role = "All Authenticated Staff (RBAC 1+)"
            elif c_cls in ["CLASS-003", "CONFIDENTIAL"]:
                auth_role = "Doctor, Nurse, Pharmacist, Lab Tech"
            elif c_cls in ["CLASS-004", "RESTRICTED"]:
                auth_role = "Registration Clerk, Treating Clinician"
            else: # CLASS-005, HIGHLY-RESTRICTED
                auth_role = "Treating Doctor (Break-Glass / Dual Auth)"

            lines.append(f"| `{c_name}` | `{c_type}` | `{c_cls}` | {c_enc} | {c_mask} | {auth_role} |")
        lines.append("")

        # Detailed per-table security and masking guidance

        pii_cols = [c["column_name"] for c in cols if c["pii_status"] or c["classification"] in ["CLASS-004", "CLASS-005"]]
        phi_cols = [c["column_name"] for c in cols if c["sensitive_health_data"] or c["classification"] in ["CLASS-003", "CLASS-005"]]
        
        lines.append(f"#### Security Invariants & Cryptographic Safeguards for `{tschema}.{tname}`")
        lines.append(f"- **Governing Classification Baseline**: Highest Sensitivity Column is `{max([c['classification'] for c in cols])}`.")
        lines.append(f"- **Identified Restricted PII Columns ({len(pii_cols)})**: {', '.join([f'`{col}`' for col in pii_cols]) if pii_cols else 'None'}.")
        lines.append(f"- **Identified Sensitive Health Attributes PHI ({len(phi_cols)})**: {', '.join([f'`{col}`' for col in phi_cols]) if phi_cols else 'None'}.")
        lines.append(f"- **HashiCorp Vault Key Path**: `transit/keys/namma-clinic-{tschema}-{tname}` (AES-256-GCM Envelope Encryption).")
        lines.append(f"- **Cryptographic Re-Keying Cadence**: Scheduled DEK rotation every 90 days via Vault Transit API; automatic re-wrap of stored ciphertexts during scheduled maintenance.")
        lines.append(f"- **Principle of Least Privilege (PoLP) Grant**: Application microservice role `namma_app_svc` receives limited DML; direct access to raw unmasked views restricted to authorized API gateways.")
        lines.append(f"- **Threat Attack Vector & Residual Risk**: Evaluated against STRIDE; unauthorized enumeration mitigated via salted HMAC blind index and row-level security.")
        lines.append(f"- **Field-Level Dynamic Masking Rule**: Clerical and administrative roles querying `{tschema}.{tname}` observe deterministic redactions on sensitive attributes, while treating clinicians obtain decrypted plaintext within active encounter contexts.")
        lines.append(f"- **Statutory Retention Alignment**: Governed by `{tbl['retention']}` under municipal healthcare bylaws and DPDP statutory horizons.")
        lines.append(f"- **Row-Level Security (RLS) Policy**: `ALTER TABLE {tschema}.{tname} ENABLE ROW LEVEL SECURITY;` enforcing strict multi-tenant isolation on `facility_id`.")
        lines.append(f"- **Backup & Storage Encryption**: Stored data blocks and continuous WAL streams encrypted with AES-256-GCM before transmission.")
        lines.append(f"- **Audit Granularity Profile**: Detailed state change capture with cryptographic hash chain ledger verification in `audit.audit_events`.")
        lines.append("")


    # 6. Data Leakage Prevention (DLP) & Export Gating Rules
    lines.append("## 6. Data Leakage Prevention (DLP) & Export Gating Governance")
    lines.append("")
    lines.append("Bulk data exfiltration represents a primary vector of systemic healthcare privacy breaches. To prevent unauthorized mass exports, the platform enforces strict technical gating:")
    lines.append("1. **API Rate Limiting & Page Caps**: Clinical endpoints restrict page sizes to a maximum of 50 records per request. Bulk query pagination requires dual-token administrative authorization.")
    lines.append("2. **Export Quarantine & Watermarking**: Any authorized CSV / Excel report export containing `CLASS-003` or `CLASS-004` data automatically injects an invisible zero-width unicode cryptographic watermark embedding the requesting staff ID, timestamp, and client IP.")
    lines.append("3. **WORM Export Audit**: Every export attempt is immutably recorded into `audit.data_access_logs` with the full query SQL, result row count, and payload SHA-256 hash.")
    lines.append("")

    # 7. Developer Sanitization & Synthetic Data Generation Invariants
    lines.append("## 7. Non-Production Environment Sanitization & Synthetic Generation")
    lines.append("")
    lines.append("Under no circumstances is production data containing `CLASS-003`, `CLASS-004`, or `CLASS-005` attributes permitted to enter development, testing, staging, or CI/CD environments:")
    lines.append("1. **Absolute PII Embargo**: Live database backups are strictly prohibited from being restored into non-production VPCs.")
    lines.append("2. **Synthetic Data Synthesis**: Development and test databases are populated strictly using deterministic synthetic generators (`scripts/database/gen_db_15_seeds.py`), using fabricated Indian names, synthetic mobile numbers (`+91 90000 00001` to `90000 99999`), and mocked ABHA identifiers.")
    lines.append("3. **Cryptographic Redaction**: Where production data is extracted for machine learning model training, all PII fields undergo irreversible SHA-256 one-way salted hashing and k-anonymity verification ($k \\ge 5$).")
    lines.append("")

    # 8. Zero-Trust Network Microsegmentation & mTLS 1.3
    lines.append("## 8. Zero-Trust Database Network Microsegmentation & mTLS 1.3 Architecture")
    lines.append("")
    lines.append("All network traffic to PostgreSQL 16 is confined to isolated private VPC subnets. Direct public internet routing is architecturally prohibited:")
    lines.append("1. **Mutual TLS (mTLS 1.3) Enforcement**: All database connections require bidirectional X.509 certificate authentication issued by an internal HashiCorp Vault PKI intermediate CA.")
    lines.append("2. **PostgreSQL pg_hba.conf Security Profile**:")
    lines.append("   ```conf")
    lines.append("   # DOCUMENTATION-ONLY CONFIG: Zero-Trust Host Based Authentication")
    lines.append("   # TYPE  DATABASE        USER            ADDRESS                 METHOD")
    lines.append("   hostssl all             namma_app_svc   10.100.12.0/24          cert clientcert=verify-full")
    lines.append("   hostssl all             namma_read_rep  10.100.14.0/24          cert clientcert=verify-full")
    lines.append("   hostssl replication     replicator      10.100.10.0/24          cert clientcert=verify-full")
    lines.append("   host    all             all             all                     reject")
    lines.append("   ```")
    lines.append("3. **Cipher Suite Restrictions**: Only TLS 1.3 cipher suites `TLS_AES_256_GCM_SHA384` and `TLS_CHACHA20_POLY1305_SHA256` are permitted.")
    lines.append("")

    # 9. Threat Modeling & STRIDE Taxonomy
    lines.append("## 9. Threat Modeling & STRIDE Taxonomy for Healthcare Database Assets")
    lines.append("")
    lines.append("To ensure comprehensive defense, database engineering evaluates potential attack vectors using Microsoft STRIDE threat modeling:")
    lines.append("")
    lines.append("| STRIDE Threat Category | Potential Healthcare Attack Scenario | Implemented Database Countermeasure | Residual Risk Tier |")
    lines.append("| :--- | :--- | :--- | :--- |")
    lines.append("| **Spoofing Identity** | Malicious actor attempts rogue connection masquerading as app service | Strict mTLS with client certificate pinning and Vault short-lived credentials | Negligible |")
    lines.append("| **Tampering with Data** | Insider alters clinical consultation notes or drug inventory quantities | SHA-256 HMAC hash chaining in `audit.audit_events` and append-only ledgers | Negligible |")
    lines.append("| **Repudiation** | Doctor claims prescription or diagnosis was forged by someone else | Cryptographic digital signatures recorded with doctor registration number | Negligible |")
    lines.append("| **Information Disclosure**| Backup stolen or rogue DBA extracts raw EBS storage volumes | Column-level AES-256-GCM envelope encryption; ciphertext undecipherable without HSM | Low |")
    lines.append("| **Denial of Service** | Complex analytical queries lock transactional tables during OPD peak | Dedicated read replicas, strict 5s lock timeout, and PgBouncer connection caps | Low |")
    lines.append("| **Elevation of Privilege**| Compromised web application attempts schema modifications | PostgreSQL user `namma_app_svc` lacks DDL privileges; restricted to specific DML views | Negligible |")
    lines.append("")

    # 10. Data Subject Rights (DSR) & DPDP Citizen Request Runbooks
    lines.append("## 10. Data Subject Rights (DSR) & DPDP Citizen Request Automation Runbooks")
    lines.append("")
    lines.append("Under DPDP Act 2023 Sections 11-14, citizens possess explicit rights over their personal data. The database layer provides formal operational blueprints for each DSR workflow:")
    lines.append("1. **Right to Access Summary of Personal Data (Section 11)**: A citizen can request an export of all personal data held by BBMP clinics. A stored procedure queries all 52 tables using the patient's blinded ABHA ID, aggregating demographic, consultation, prescription, and lab records into a signed JSON/PDF health summary.")
    lines.append("2. **Right to Correction and Updating (Section 12)**: If demographic data is erroneous, an atomic mutation updates `patients.patients` and `patients.patient_contacts`, while preserving historical snapshots in audit logs for clinical malpractice defense.")
    lines.append("3. **Right to Erasure (Section 12(3))**: When a citizen exercises erasure, clinical records subject to statutory NMC 10-year retention (`RETENTION-001`) are retained in quarantine, while non-statutory commercial and communication attributes are immediately purged.")
    lines.append("4. **Right of Grievance Redressal (Section 13)**: Grievance tickets in `public.grievances` track full lifecycles with mandated 72-hour acknowledgment and 30-day resolution SLAs.")
    lines.append("")

    # 11. Regulatory Compliance Audit Queries
    lines.append("## 11. Database Security Compliance Verification Queries")
    lines.append("")
    lines.append("Security auditors execute standardized catalog validation scripts to verify that zero unencrypted PII columns exist:")
    lines.append("")
    lines.append("```sql")
    lines.append("-- DOCUMENTATION-ONLY SQL: Identifying Unencrypted PII Columns")
    lines.append("SELECT")
    lines.append("    table_schema,")
    lines.append("    table_name,")
    lines.append("    column_name,")
    lines.append("    data_type")
    lines.append("FROM information_schema.columns")
    lines.append("WHERE table_schema NOT IN ('pg_catalog', 'information_schema')")
    lines.append("  AND (")
    lines.append("      column_name ILIKE '%phone%' OR")
    lines.append("      column_name ILIKE '%aadhaar%' OR")
    lines.append("      column_name ILIKE '%email%' OR")
    lines.append("      column_name ILIKE '%name%'")
    lines.append("  )")
    lines.append("  AND column_name NOT ILIKE '%hash%'")
    lines.append("  AND column_name NOT ILIKE '%encrypted%'")
    lines.append("  AND column_name NOT ILIKE '%blind%'")
    lines.append("ORDER BY table_schema, table_name;")
    lines.append("```")
    lines.append("")

    # 12. Automated Data Discovery & Classification Scanner Pipeline
    lines.append("## 12. Automated Data Discovery & Classification Scanner Pipeline")
    lines.append("")
    lines.append("To prevent unclassified 'schema drift' where new migrations or ad-hoc columns are added without formal classification tags, an automated crawler runs weekly in CI/CD and production:")
    lines.append("1. **Regex Heuristic Engine**: Scans new attributes against patterns for phone numbers, Indian names, pin codes, email addresses, and medical ICD-10 terminology.")
    lines.append("2. **Metadata Catalog Inspection**: Verifies that every column entry in `pg_description` possesses a valid classification tag (`CLASS-001` through `CLASS-005`).")
    lines.append("3. **Automated Quarantining**: If an unclassified column is detected in production schemas, an immediate P1 alert is dispatched to the Data Protection Officer and migrations are blocked.")
    lines.append("")

    # 13. ISO 27001 Annex A Mapping Matrix
    lines.append("## 13. ISO/IEC 27001:2022 Annex A Healthcare Control Mapping")
    lines.append("")
    lines.append("The database engineering controls implemented in this specification map directly to international information security standards:")
    lines.append("")
    lines.append("| ISO 27001:2022 Control | Control Title | Specific Database Architectural Mechanism |")
    lines.append("| :--- | :--- | :--- |")
    lines.append("| **A.5.12** | Classification of Information | 5-Tier canonical taxonomy (`CLASS-001` to `CLASS-005`) enforced across 832 columns. |")
    lines.append("| **A.8.11** | Data Masking | Dynamic Data Masking (DDM) views obfuscating Aadhaar, phone, and names for clerical roles. |")
    lines.append("| **A.8.12** | Data Leakage Prevention | Export gating caps at 50 records; zero-width steganographic watermarking on CSV reports. |")
    lines.append("| **A.8.20** | Network Security | Private subnet placement; zero internet gateways; mandatory mTLS 1.3 client certificates. |")
    lines.append("| **A.8.24** | Use of Cryptography | AES-256-GCM envelope encryption via HashiCorp Vault; HMAC-SHA256 blind indexing. |")
    lines.append("")

    # 14. RACI Governance Matrix for Security & Privacy
    lines.append("## 14. RACI Governance Matrix for Healthcare Data Security")
    lines.append("")
    lines.append("Institutional responsibilities for data classification, key rotation, and privacy enforcement are formalized below:")
    lines.append("")
    lines.append("| Governance Workflow | BBMP Health Commissioner | Data Protection Officer (DPO) | Chief Information Security Officer | Lead Database Architect | Application Lead |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    lines.append("| **Classification Policy Approval** | Accountable | Responsible | Consulted | Consulted | Informed |")
    lines.append("| **New Column Classification Tagging** | Informed | Accountable | Consulted | Responsible | Responsible |")
    lines.append("| **Vault Cryptographic Key Rotation** | Informed | Informed | Accountable | Responsible | Consulted |")
    lines.append("| **DPDP Right to Erasure Execution** | Informed | Accountable | Consulted | Responsible | Informed |")
    lines.append("| **Data Leakage Forensic Investigation** | Accountable | Responsible | Responsible | Consulted | Informed |")
    lines.append("")

    # 15. Incident Response Playbook for Healthcare Data Breaches
    lines.append("## 15. Incident Response Playbook for Healthcare Data Breaches")
    lines.append("")
    lines.append("In the event of a suspected database security incident, data leakage, or unauthorized exfiltration, the platform triggers an immediate emergency response protocol:")
    lines.append("1. **Mandatory 6-Hour Statutory Disclosure**: CERT-In Directions 2022 mandate reporting cybersecurity incidents within 6 hours of discovery. The DPO dispatches an automated notification payload.")
    lines.append("2. **Automated Connection Severance**: The SRE team triggers `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = 'namma_app_svc';` and rotates mTLS certificate authority bundles in Vault.")
    lines.append("3. **Cryptographic Revocation**: If compromised DEK keys are identified, they are marked `REVOKED` in HashiCorp Vault, disabling further decryption of ciphertext envelopes.")
    lines.append("4. **Forensic Log Sealing**: Active WAL segments and `audit.data_access_logs` are duplicated to an air-gapped forensic AWS account with WORM compliance locks.")
    lines.append("")

    # 16. Cryptographic Algorithm Work Factors & Quantum Resistance Timetable
    lines.append("## 16. Cryptographic Work Factors & Quantum Resistance Timetable")
    lines.append("")
    lines.append("To protect longitudinal medical records that must remain confidential for decades, cryptographic primitives are selected in accordance with NIST SP 800-57 Part 1 Rev. 5 recommendations:")
    lines.append("")
    lines.append("| Cryptographic Primitive | Platform Usage Domain | Effective Key Strength | NIST Recommended Horizon | Post-Quantum Cryptography (PQC) Migration Path |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    lines.append("| **AES-256-GCM** | Column envelope encryption & TDE storage | 256 bits | Beyond 2035+ | Grover-resistant (128-bit quantum security); no replacement required |")
    lines.append("| **Argon2id (m=64MB, t=3, p=4)** | User credential password hashing | Memory-hard | Beyond 2035+ | Work factor parameter upgrades every 24 months |")
    lines.append("| **HMAC-SHA256 (Secret Salted)** | Searchable blind indexing & WORM log chaining | 256 bits | Beyond 2035+ | Upgrade to HMAC-SHA384 / SHA3 upon FIPS standardization |")
    lines.append("| **RSA-4096 / ECDSA P-384** | Service-to-service mTLS & JWT root signing | 140 / 192 bits | Safe until 2030 | Migration to ML-KEM (Kyber) and ML-DSA (Dilithium) scheduled 2028 |")
    lines.append("")

    # 17. Merkle Tree & Tamper-Evident Hash Chaining Procedure
    lines.append("## 17. Cryptographic Merkle Tree & Tamper-Evident Verification Blueprint")
    lines.append("")
    lines.append("Audit entries in `audit.audit_events` form an append-only cryptographic hash chain. Tampering with any row breaks the cryptographic proof:")
    lines.append("")
    lines.append("```sql")
    lines.append("-- DOCUMENTATION-ONLY SQL: Cryptographic Hash Chain Validation Function")
    lines.append("CREATE OR REPLACE FUNCTION audit.fn_verify_audit_hash_chain(p_facility_id UUID, p_date DATE)")
    lines.append("RETURNS TABLE (is_valid BOOLEAN, broken_event_id UUID, expected_hash BYTEA, actual_hash BYTEA) AS $$")
    lines.append("DECLARE")
    lines.append("    r RECORD;")
    lines.append("    v_prev_hash BYTEA := '\\x0000000000000000000000000000000000000000000000000000000000000000'::BYTEA;")
    lines.append("    v_computed_hash BYTEA;")
    lines.append("BEGIN")
    lines.append("    FOR r IN (")
    lines.append("        SELECT id, event_category, action, actor_user_id, previous_state_hash, new_state_hash, hmac_signature")
    lines.append("        FROM audit.audit_events")
    lines.append("        WHERE facility_id = p_facility_id AND created_at >= p_date AND created_at < p_date + INTERVAL '1 day'")
    lines.append("        ORDER BY created_at ASC, id ASC")
    lines.append("    ) LOOP")
    lines.append("        v_computed_hash := hmac(r.previous_state_hash || r.new_state_hash, current_setting('vault.audit_secret', true)::BYTEA, 'sha256');")
    lines.append("        IF v_computed_hash != r.hmac_signature THEN")
    lines.append("            RETURN QUERY SELECT FALSE, r.id, v_computed_hash, r.hmac_signature;")
    lines.append("            RETURN;")
    lines.append("        END IF;")
    lines.append("        v_prev_hash := r.hmac_signature;")
    lines.append("    END LOOP;")
    lines.append("    RETURN QUERY SELECT TRUE, NULL::UUID, NULL::BYTEA, NULL::BYTEA;")
    lines.append("END;")
    lines.append("$$ LANGUAGE plpgsql SECURITY DEFINER;")
    lines.append("```")
    lines.append("")

    # 18. Continuous Security Posture & CIS PostgreSQL Benchmark Compliance
    lines.append("## 18. Continuous Security Posture & CIS Benchmark Compliance")
    lines.append("")
    lines.append("The database configuration is continuously audited against the Center for Internet Security (CIS) PostgreSQL 16 Benchmark:")
    lines.append("")
    lines.append("| CIS Control ID | CIS Benchmark Recommendation | PostgreSQL 16 Architectural Parameter | Compliance State |")
    lines.append("| :--- | :--- | :--- | :--- |")
    lines.append("| **CIS 3.1.1** | Ensure standard logging is enabled | `logging_collector = on` | COMPLIANT |")
    lines.append("| **CIS 3.1.5** | Record lock waits exceeding threshold | `log_lock_waits = on` | COMPLIANT |")
    lines.append("| **CIS 3.1.14**| Record statement execution times | `log_min_duration_statement = 250ms` | COMPLIANT |")
    lines.append("| **CIS 4.3** | Enforce SSL/TLS for all client connections | `ssl = on`, `ssl_min_protocol_version = 'TLSv1.3'` | COMPLIANT |")
    lines.append("| **CIS 5.1** | Revoke default PUBLIC permissions on schemas | `REVOKE CREATE ON SCHEMA public FROM PUBLIC;` | COMPLIANT |")
    lines.append("| **CIS 6.2** | Prohibit superuser login over network | `hostssl all postgres reject` | COMPLIANT |")
    lines.append("")
    lines.append("Vulnerability remediation follows strict municipal SLA thresholds:")
    lines.append("- **Critical (CVSS 9.0 - 10.0)**: Remediated and hot-patched within **24 hours**.")
    lines.append("- **High (CVSS 7.0 - 8.9)**: Remediated within **7 calendar days**.")
    lines.append("- **Medium (CVSS 4.0 - 6.9)**: Remediated within **30 calendar days**.")
    lines.append("- **Low (CVSS 0.1 - 3.9)**: Remediated in next scheduled monthly release cycle.")
    lines.append("Automated verification of CIS benchmarks is performed using dedicated SQL audit probes:")
    lines.append("")
    lines.append("```sql")
    lines.append("-- DOCUMENTATION-ONLY SQL: CIS PostgreSQL Security Posture Verification Probe")
    lines.append("SELECT")
    lines.append("    name AS parameter_name,")
    lines.append("    setting AS current_value,")
    lines.append("    boot_val AS default_value,")
    lines.append("    context,")
    lines.append("    CASE")
    lines.append("        WHEN name = 'ssl' AND setting = 'on' THEN 'PASS'")
    lines.append("        WHEN name = 'ssl_min_protocol_version' AND setting = 'TLSv1.3' THEN 'PASS'")
    lines.append("        WHEN name = 'log_connections' AND setting = 'on' THEN 'PASS'")
    lines.append("        WHEN name = 'log_disconnections' AND setting = 'on' THEN 'PASS'")
    lines.append("        WHEN name = 'log_lock_waits' AND setting = 'on' THEN 'PASS'")
    lines.append("        WHEN name = 'password_encryption' AND setting = 'scram-sha-256' THEN 'PASS'")
    lines.append("        ELSE 'REVIEW_REQUIRED'")
    lines.append("    END AS compliance_eval")
    lines.append("FROM pg_settings")
    lines.append("WHERE name IN (")
    lines.append("    'ssl', 'ssl_min_protocol_version', 'log_connections',")
    lines.append("    'log_disconnections', 'log_lock_waits', 'password_encryption'")
    lines.append(");")
    lines.append("```")
    lines.append("")
    lines.append("### 18.1 Continuous Audit Automation Architecture")
    lines.append("The CIS security audit probe is executed continuously as part of the municipal infrastructure health check loop:")
    lines.append("1. **Automated Prometheus Exporter**: The `postgres_exporter` queries `pg_settings` every 60 seconds, exporting compliance metrics to the central Grafana dashboard.")
    lines.append("2. **Drift Detection & Remediation**: Any modification to `postgresql.conf` or `pg_hba.conf` that introduces non-compliance immediately fires a P1 alert to the Security Operations Center (SOC).")
    lines.append("3. **Quarterly Third-Party Pen Testing**: External CERT-In certified auditors validate database hardening against CIS standards every 90 days.")
    lines.append("4. **Immutable Configuration Repository**: All database configuration files are managed in Git under Infrastructure-as-Code (Terraform / Ansible) with signed Git commits.")
    lines.append("5. **Continuous File Integrity Monitoring (FIM)**: OSSEC and Falco monitor `/etc/postgresql/` and `/var/lib/postgresql/` for unauthorized file system mutations in real time.")
    lines.append("6. **Zero-Trust Network Verification**: Network ingress security group rules are validated continuously using AWS Config rules to prevent accidental exposure.")
    lines.append("")

    # 19. Conclusion & Master Baseline
    lines.append("## 19. Data Classification Baseline & Security Sign-Off")
    lines.append("")
    lines.append(f"This specification approves the comprehensive security classification and cryptographic controls across all 52 relational tables and {len(COLUMNS)} columns. With full envelope encryption, blind indexing, dynamic data masking, and strict DPDP Act 2023 compliance, the Namma Clinic Platform establishes a gold standard in municipal healthcare information security.")
    lines.append("")
    lines.append("All application engineers, database administrators, and DevOps personnel must strictly adhere to the classification invariants defined herein. Direct storage of plaintext PII or sensitive health attributes in unencrypted columns constitutes an immediate security defect subject to architectural review.")
    lines.append("")
    lines.append("Cryptographic keys, blind indexing salts, and Vault access tokens must never be hardcoded in application repositories or committed to source control. Zero-trust principles govern every connection from the edge clinics to the central database cluster.")
    lines.append("")
    content = "\n".join(lines)

    return write_db_doc("13-data-classification.md", content)

if __name__ == "__main__":
    generate_doc_13()
