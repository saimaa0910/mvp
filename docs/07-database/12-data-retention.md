# Phase 07 — Data Retention, Archival & Cryptographic Lifecycle Policy

> **Document Identifier**: `DB-RET-001`
> **System**: Namma Clinic Digital Health & Operations Platform
> **Municipal Authority**: Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Status**: APPROVED STATUTORY RETENTION BASELINE
> **Cataloged Retention Policies**: 20 Comprehensive Rules (`RETENTION-001` to `RETENTION-020`)
> **Statutory Governance**: DPDP Act 2023, NMC Guidelines, Drugs and Cosmetics Act 1940, KTPP Act 1999, IT Act 2000
> **Notice**: All SQL blocks contained herein are strictly **DOCUMENTATION-ONLY SQL**. Zero runtime code or migrations are executed during this phase.

---

## 1. Executive Summary & Statutory Governance Framework

In a municipal primary healthcare network processing millions of citizen consultations annually, data retention is governed by a delicate balance between legal imperatives: preserving longitudinal medical histories for patient safety, satisfying medical malpractice limitation periods, complying with public procurement and financial audit rules, and strictly enforcing the data minimization mandates of the **Digital Personal Data Protection (DPDP) Act 2023**.

Data retained beyond statutory necessity exposes the municipal authority to severe regulatory penalties, data breach liability, and soaring cloud infrastructure costs. Conversely, premature data destruction violates National Medical Commission (NMC) regulations, invalidates legal defense in civil medical negligence suits, and corrupts public health epidemiological surveillance.

This document establishes the authoritative Data Retention, Archival, and Disposal Architecture for the Namma Clinic Digital Health Platform. It defines 20 discrete statutory retention rules (`RETENTION-001` to `RETENTION-020`) governing all 52 relational database tables, spanning multi-tier storage progressions, automated partition archiving, immutable WORM object locking, legal hold freezing protocols, and cryptographic shredding algorithms.

### 1.1 DPDP Act 2023 Statutory Compliance Matrix

The Digital Personal Data Protection Act 2023 imposes stringent statutory obligations on Data Fiduciaries (BBMP Health Department). The database retention architecture directly addresses each operational mandate:

| DPDP Section | Statutory Mandate | Architectural Implementation in Namma Clinic Database | Non-Compliance Risk |
| :--- | :--- | :--- | :--- |
| **Section 6 (1)** | Purpose-limited consent | Consent artifacts (`RETENTION-005`) retained alongside patient records; expired consents automatically disable data processing pathways. | Fine up to ₹50 Crores |
| **Section 8 (7)** | Mandatory erasure upon purpose completion | Automated partition lifecycle daemons purge operational data once statutory clinical horizons elapse. | Fine up to ₹250 Crores |
| **Section 8 (8)** | Reasonable security safeguards | Envelope encryption with per-patient DEKs; cold archives stored in WORM-locked AWS S3 Glacier. | Fine up to ₹250 Crores |
| **Section 12 (3)** | Citizen Right to Erasure | Automated crypto-shredding runbooks purge encryption keys, rendering historical records permanently unreadable. | Regulatory inquiry & fine |
| **Section 13** | Grievance redressal tracking | Citizen grievance tickets (`RETENTION-014`) retained for 5 years with immutable audit logs of resolution. | Administrative reprimand |

## 2. Multi-Tier Storage Progression Architecture

To achieve sub-second clinical query latency while optimizing petabyte-scale long-term retention economics, data moves through four distinct lifecycle tiers:

```mermaid
graph LR
    A[Tier 1: Hot OLTP<br/>PostgreSQL NVMe SSD<br/>0 to 12 Months] -->|Automated Detach & Parquet Export| B[Tier 2: Warm Analytical<br/>S3 Standard-IA / ClickHouse<br/>1 to 3 Years]
    B -->|Lifecycle Transition Rule| C[Tier 3: Cold WORM Archive<br/>AWS S3 Glacier Object Lock<br/>3 to 21 Years]
    C -->|Retention Expiry / Key Destruction| D[Tier 4: Cryptographic Shredding<br/>Vault KMS Key Purge & Tombstone]
```

### 2.1 Tier Definitions and Technical Specifications

| Tier Name | Storage Media & Substrate | Target Latency | Storage Cost Relative | Encryption Paradigm | Typical Resident Data |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Hot OLTP** | AWS EBS io2 / gp3 NVMe SSD attached to PostgreSQL 16 | p95 < 15 ms | 1.0x (Baseline) | Transparent Data Encryption (TDE) + AES-256 Column Enclave | Active consultations, current-day queue tokens, active pharmacy inventory balances. |
| **Tier 2: Warm Analytical** | Columnar Parquet on S3 Standard-Infrequent Access / ClickHouse | p95 < 2.5 sec | 0.20x (-80%) | SSE-KMS with Customer Managed Keys (CMK) | 1-3 year old patient encounters, historical lab trends, monthly HMIS indicator rollups. |
| **Tier 3: Cold WORM Archive** | AWS S3 Glacier Flexible Archive with Object Lock Compliance Mode | 3 to 5 hours | 0.03x (-97%) | FIPS 140-2 Level 3 Root KMS Key + SHA-256 Hash Tree | 3-21 year statutory archives, legal defense records, immutable audit logs. |
| **Tier 4: Disposal / Shredding** | Cryptographic key destruction in Vault KMS / Table Tombstone | Zero (Destroyed) | 0.00x | Key Destruction (Ciphertext Irrecoverable) | Expired temporary tokens, superseded consent artifacts, pruned edge journals. |

## 3. Master Relational Table Retention Horizons (All 52 Tables)

Every relational table across all schemas is mapped to its governing retention policy, partition key, hot tier lifespan, and archival target:

| Table ID | Schema & Table Name | Governing Policy | Hot Storage (PostgreSQL) | Cold Storage (Glacier) | Final Disposal Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TABLE-001` | `identity.auth_users` | **RETENTION-011** | 12 Months | 1 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-002` | `identity.user_credentials` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-003` | `identity.user_sessions` | **RETENTION-011** | 12 Months | 1 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-004` | `identity.roles` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-005` | `identity.permissions` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-006` | `identity.role_permissions` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-007` | `identity.user_roles` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-008` | `identity.facilities` | **RETENTION-019** | 12 Months | 3 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-009` | `identity.facility_rooms` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-010` | `identity.staff_profiles` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-011` | `identity.staff_shifts` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-012` | `identity.system_configs` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-013` | `intake.patients` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-014` | `intake.patient_identifiers` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-015` | `intake.patient_contacts` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-016` | `intake.patient_addresses` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-017` | `intake.consent_records` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-018` | `intake.tokens` | **RETENTION-007** | 12 Months | 3 Months WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-019` | `intake.queue_entries` | **RETENTION-007** | 12 Months | 3 Months WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-020` | `intake.triage_assessments` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-021` | `intake.patient_vitals` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-022` | `intake.danger_alerts` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-023` | `clinical.clinical_encounters` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-024` | `clinical.clinical_notes` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-025` | `clinical.diagnoses` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-026` | `clinical.prescriptions` | **RETENTION-003** | 12 Months | 5 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-027` | `clinical.prescription_items` | **RETENTION-003** | 12 Months | 5 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-028` | `clinical.lab_orders` | **RETENTION-004** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-029` | `clinical.lab_order_items` | **RETENTION-004** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-030` | `clinical.lab_results` | **RETENTION-004** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-031` | `clinical.teleconsultations` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-032` | `pharmacy.formulary_drugs` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-033` | `pharmacy.drug_categories` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-034` | `pharmacy.pharmacy_batches` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-035` | `pharmacy.clinic_stock` | **RETENTION-009** | 12 Months | 8 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-036` | `pharmacy.dispensations` | **RETENTION-003** | 12 Months | 5 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-037` | `pharmacy.dispensation_items` | **RETENTION-003** | 12 Months | 5 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-038` | `pharmacy.stock_movements` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-039` | `pharmacy.drug_indents` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-040` | `pharmacy.indent_items` | **RETENTION-009** | 12 Months | 8 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-041` | `pharmacy.cold_chain_devices` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-042` | `pharmacy.cold_chain_telemetry` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-043` | `continuity.referrals` | **RETENTION-010** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-044` | `continuity.referral_counter_notes` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-045` | `continuity.ncd_episodes` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-046` | `continuity.follow_up_schedules` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-047` | `continuity.notifications` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-048` | `continuity.grievances` | **RETENTION-014** | 12 Months | 5 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-049` | `continuity.helpdesk_tickets` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-050` | `audit.audit_events` | **RETENTION-006** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-051` | `sync.offline_mutation_log` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |
| `TABLE-052` | `sync.abdm_artifacts` | **RETENTION-001** | 12 Months | 10 Years WORM | Cryptographic Shredding / Vault KMS |

## 4. Master Retention Policy Registry (RETENTION-001 to RETENTION-020)

The 20 statutory retention policies are cataloged below with statutory durations, regulatory legal bases, and primary storage tiers:

| Policy ID | Policy Name | Statutory Horizon | Min Days | Legal & Regulatory Basis | Primary Lifecycle Progression |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RETENTION-001** | Adult Outpatient Clinical Records | `10 Years` | 3650d | National Medical Commission (NMC) Guidelines | Active online 3 years |
| **RETENTION-002** | Pediatric Clinical Records | `21 Years` | 7670d | Indian Limitation Act 1963 | Retained until child reaches age of majority (18 years) plus 3 years limitation period. |
| **RETENTION-003** | Electronic Prescriptions & Dispensation Logs | `5 Years` | 1825d | Pharmacy Practice Regulations | Stored in PostgreSQL online database 2 years |
| **RETENTION-004** | Diagnostic Laboratory Results & Panic Logs | `10 Years` | 3650d | Clinical Establishments (Registration and Regulation) Act | Retained online for longitudinal trend analysis across repeat patient visits. |
| **RETENTION-005** | Citizen Consent Artifacts & Revocations | `7 Years` | 2555d | Digital Personal Data Protection (DPDP) Act 2023 Section 6 | Retained for duration of consent plus 7 years post-revocation for evidentiary audit. |
| **RETENTION-006** | Immutable Cryptographic WORM Audit Trails | `10 Years` | 3650d | Information Technology Act 2000 Section 7A | Never deleted |
| **RETENTION-007** | Daily Queue Tokens & Waiting Hall State | `3 Months` | 90d | BBMP Health Operations SLA Standard | Retained in operational database 90 days |
| **RETENTION-008** | Cold-Chain IoT Sensor Temperature Telemetry | `3 Years` | 1095d | Universal Immunization Programme (UIP) Cold Chain Guidelines | Raw 60-second readings stored in ClickHouse 180 days |
| **RETENTION-009** | Pharmacy Stock Movements & Indent Receipts | `8 Years` | 2920d | Karnataka Transparency in Public Procurements (KTPP) Act | Complete double-entry inventory ledger retained for statutory financial and CAG audits. |
| **RETENTION-010** | Secondary Hospital Referral Dossiers | `10 Years` | 3650d | ABDM Continuity of Care | Retained in clinical continuity registry |
| **RETENTION-011** | Staff Authentication Sessions & Access Tokens | `1 Years` | 365d | CERT-In Cyber Security Directions 2022 | Active sessions expired after 15m idle |
| **RETENTION-012** | Edge Offline Mutation Journal Logs | `6 Months` | 180d | Platform Offline Architecture Standard ARCH-OFF-09 | Retained on edge appliance 30 days post successful cloud reconciliation |
| **RETENTION-013** | Non-Communicable Disease (NCD) Registries | `15 Years` | 5475d | National Programme for Prevention | Longitudinal hypertension and diabetes care plans retained for lifetime of patient management. |
| **RETENTION-014** | Citizen Grievances & Resolution Records | `5 Years` | 1825d | Karnataka Sakala Services Act 2011 | Full grievance lifecycle, ombudsman notes, and resolution actions retained 5 years. |
| **RETENTION-015** | Outbound Citizen SMS & WhatsApp Notifications | `1 Years` | 365d | TRAI Telecom Commercial Communications Regulations | Dispatched message metadata, delivery receipts, and carrier reference IDs retained 12 months. |
| **RETENTION-016** | Teleconsultation Session Metadata & Joint Notes | `10 Years` | 3650d | Telemedicine Practice Guidelines (Board of Governors in supersession of MCI) | Doctor-to-specialist teleconsultation logs, duration, and clinical decisions retained 10 years. |
| **RETENTION-017** | Database Backup Snapshots (WAL & Full) | `7 Years` | 2555d | Disaster Recovery Framework ARCH-DR-14 | Continuous WAL 35 days |
| **RETENTION-018** | Clinical AI Advisory Prediction Records | `5 Years` | 1825d | AI Governance Framework ARCH-AI-12 | AI inference inputs, confidence scores, and physician accept/override actions kept 5 years. |
| **RETENTION-019** | Facility Hardware Fault & Maintenance Logs | `3 Years` | 1095d | BBMP Health Infrastructure Asset Management Policy | Equipment breakdown tickets, peripheral replacements, and SLA penalties kept 3 years. |
| **RETENTION-020** | Statutory HMIS Monthly Health Indicator Reports | `10 Years` | 3650d | Integrated Disease Surveillance Programme (IDSP) | Monthly ward-level public health disease surveillance returns retained 10 years. |

## 5. Comprehensive Statutory Retention Specifications (RETENTION-001 to RETENTION-020)

The following subsections provide detailed engineering specifications for each retention rule, including governing legal citations, affected relational entities, multi-tier migration schedules, automated SQL purge scripts, legal hold procedures, recovery defrost runbooks, and cryptographic disposal standards:

### RETENTION-001: Adult Outpatient Clinical Records

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-001`
- **Statutory Retention Horizon**: `10 Years (3650 Days)`
- **Governing Legal Authority**: National Medical Commission (NMC) Guidelines & BBMP Healthcare Bylaws
- **Operational Policy Summary**: Active online 3 years; archived to compressed WORM S3 cold storage 7 years; permanent hash ledger.
- **Governed Relational Entities**: `encounters`, `consultation_notes`, `vital_signs`, `clinical_diagnoses`, `triage_assessments`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 3650)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 3650)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-001
-- Policy Target: Adult Outpatient Clinical Records
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-001' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.encounters
    DETACH PARTITION clinical.encounters_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.encounters_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-001/encounters_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-001', 'encounters', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-001/encounters_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.encounters_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-001/encounters_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-001",
    "target_table": "encounters",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-001/encounters_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-002: Pediatric Clinical Records

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-002`
- **Statutory Retention Horizon**: `21 Years (7670 Days)`
- **Governing Legal Authority**: Indian Limitation Act 1963 & Protection of Children Health Guidelines
- **Operational Policy Summary**: Retained until child reaches age of majority (18 years) plus 3 years limitation period.
- **Governed Relational Entities**: `immunizations`, `pediatric_growth_logs`, `encounters`, `patients`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 7670)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 7670)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-002
-- Policy Target: Pediatric Clinical Records
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-002' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.immunizations
    DETACH PARTITION clinical.immunizations_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.immunizations_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-002/immunizations_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-002', 'immunizations', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-002/immunizations_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.immunizations_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-002/immunizations_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-002",
    "target_table": "immunizations",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-002/immunizations_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-003: Electronic Prescriptions & Dispensation Logs

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-003`
- **Statutory Retention Horizon**: `5 Years (1825 Days)`
- **Governing Legal Authority**: Pharmacy Practice Regulations & Drugs and Cosmetics Act 1940
- **Operational Policy Summary**: Stored in PostgreSQL online database 2 years; moved to columnar compressed archive 3 years.
- **Governed Relational Entities**: `prescriptions`, `prescription_items`, `dispensations`, `dispensation_items`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 1825)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 1825)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-003
-- Policy Target: Electronic Prescriptions & Dispensation Logs
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-003' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.prescriptions
    DETACH PARTITION clinical.prescriptions_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.prescriptions_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-003/prescriptions_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-003', 'prescriptions', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-003/prescriptions_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.prescriptions_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-003/prescriptions_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-003",
    "target_table": "prescriptions",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-003/prescriptions_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-004: Diagnostic Laboratory Results & Panic Logs

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-004`
- **Statutory Retention Horizon**: `10 Years (3650 Days)`
- **Governing Legal Authority**: Clinical Establishments (Registration and Regulation) Act
- **Operational Policy Summary**: Retained online for longitudinal trend analysis across repeat patient visits.
- **Governed Relational Entities**: `lab_orders`, `lab_order_items`, `lab_results`, `lab_specimens`, `panic_alerts`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 3650)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 3650)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-004
-- Policy Target: Diagnostic Laboratory Results & Panic Logs
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-004' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.lab_orders
    DETACH PARTITION clinical.lab_orders_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.lab_orders_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-004/lab_orders_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-004', 'lab_orders', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-004/lab_orders_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.lab_orders_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-004/lab_orders_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-004",
    "target_table": "lab_orders",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-004/lab_orders_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-005: Citizen Consent Artifacts & Revocations

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-005`
- **Statutory Retention Horizon**: `7 Years (2555 Days)`
- **Governing Legal Authority**: Digital Personal Data Protection (DPDP) Act 2023 Section 6
- **Operational Policy Summary**: Retained for duration of consent plus 7 years post-revocation for evidentiary audit.
- **Governed Relational Entities**: `consents`, `consent_revocations`, `consent_audit`, `dpdp_requests`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 2555)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 2555)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-005
-- Policy Target: Citizen Consent Artifacts & Revocations
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-005' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.consents
    DETACH PARTITION clinical.consents_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.consents_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-005/consents_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-005', 'consents', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-005/consents_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.consents_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-005/consents_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-005",
    "target_table": "consents",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-005/consents_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-006: Immutable Cryptographic WORM Audit Trails

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-006`
- **Statutory Retention Horizon**: `10 Years (3650 Days)`
- **Governing Legal Authority**: Information Technology Act 2000 Section 7A & DPDP Act Section 8
- **Operational Policy Summary**: Never deleted; append-only SHA-256 HMAC hash chained log; archived to Glacier Object Lock.
- **Governed Relational Entities**: `audit_events`, `audit_hashes`, `system_access_logs`, `data_access_logs`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 3650)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 3650)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-006
-- Policy Target: Immutable Cryptographic WORM Audit Trails
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-006' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.audit_events
    DETACH PARTITION clinical.audit_events_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.audit_events_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-006/audit_events_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-006', 'audit_events', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-006/audit_events_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.audit_events_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-006/audit_events_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-006",
    "target_table": "audit_events",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-006/audit_events_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-007: Daily Queue Tokens & Waiting Hall State

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-007`
- **Statutory Retention Horizon**: `3 Months (90 Days)`
- **Governing Legal Authority**: BBMP Health Operations SLA Standard
- **Operational Policy Summary**: Retained in operational database 90 days; aggregated into daily KPI metrics; purged quarterly.
- **Governed Relational Entities**: `tokens`, `queue_entries`, `appointments`, `waiting_hall_metrics`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 90)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 90)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-007
-- Policy Target: Daily Queue Tokens & Waiting Hall State
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-007' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.tokens
    DETACH PARTITION clinical.tokens_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.tokens_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-007/tokens_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-007', 'tokens', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-007/tokens_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.tokens_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-007/tokens_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-007",
    "target_table": "tokens",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-007/tokens_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-008: Cold-Chain IoT Sensor Temperature Telemetry

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-008`
- **Statutory Retention Horizon**: `3 Years (1095 Days)`
- **Governing Legal Authority**: Universal Immunization Programme (UIP) Cold Chain Guidelines
- **Operational Policy Summary**: Raw 60-second readings stored in ClickHouse 180 days; aggregated hourly averages kept 3 years.
- **Governed Relational Entities**: `iot_device_telemetry`, `cold_chain_alerts`, `sensor_readings`, `gateway_health`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 1095)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 1095)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-008
-- Policy Target: Cold-Chain IoT Sensor Temperature Telemetry
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-008' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.iot_device_telemetry
    DETACH PARTITION clinical.iot_device_telemetry_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.iot_device_telemetry_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-008/iot_device_telemetry_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-008', 'iot_device_telemetry', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-008/iot_device_telemetry_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.iot_device_telemetry_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-008/iot_device_telemetry_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-008",
    "target_table": "iot_device_telemetry",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-008/iot_device_telemetry_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-009: Pharmacy Stock Movements & Indent Receipts

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-009`
- **Statutory Retention Horizon**: `8 Years (2920 Days)`
- **Governing Legal Authority**: Karnataka Transparency in Public Procurements (KTPP) Act & CAG Audit Rules
- **Operational Policy Summary**: Complete double-entry inventory ledger retained for statutory financial and CAG audits.
- **Governed Relational Entities**: `clinic_stock`, `stock_transactions`, `indent_requests`, `indent_items`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 2920)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 2920)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-009
-- Policy Target: Pharmacy Stock Movements & Indent Receipts
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-009' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.clinic_stock
    DETACH PARTITION clinical.clinic_stock_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.clinic_stock_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-009/clinic_stock_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-009', 'clinic_stock', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-009/clinic_stock_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.clinic_stock_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-009/clinic_stock_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-009",
    "target_table": "clinic_stock",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-009/clinic_stock_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-010: Secondary Hospital Referral Dossiers

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-010`
- **Statutory Retention Horizon**: `10 Years (3650 Days)`
- **Governing Legal Authority**: ABDM Continuity of Care & Emergency Medical Referral Policy
- **Operational Policy Summary**: Retained in clinical continuity registry; linked to patient longitudinal health record.
- **Governed Relational Entities**: `referrals`, `referral_updates`, `referral_notes`, `emergency_transfers`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 3650)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 3650)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-010
-- Policy Target: Secondary Hospital Referral Dossiers
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-010' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.referrals
    DETACH PARTITION clinical.referrals_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.referrals_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-010/referrals_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-010', 'referrals', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-010/referrals_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.referrals_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-010/referrals_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-010",
    "target_table": "referrals",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-010/referrals_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-011: Staff Authentication Sessions & Access Tokens

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-011`
- **Statutory Retention Horizon**: `1 Years (365 Days)`
- **Governing Legal Authority**: CERT-In Cyber Security Directions 2022
- **Operational Policy Summary**: Active sessions expired after 15m idle; token revocation history retained 1 year for forensics.
- **Governed Relational Entities**: `user_sessions`, `auth_users`, `auth_roles`, `refresh_tokens`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 365)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 365)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-011
-- Policy Target: Staff Authentication Sessions & Access Tokens
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-011' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.user_sessions
    DETACH PARTITION clinical.user_sessions_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.user_sessions_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-011/user_sessions_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-011', 'user_sessions', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-011/user_sessions_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.user_sessions_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-011/user_sessions_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-011",
    "target_table": "user_sessions",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-011/user_sessions_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-012: Edge Offline Mutation Journal Logs

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-012`
- **Statutory Retention Horizon**: `6 Months (180 Days)`
- **Governing Legal Authority**: Platform Offline Architecture Standard ARCH-OFF-09
- **Operational Policy Summary**: Retained on edge appliance 30 days post successful cloud reconciliation; pruned automatically.
- **Governed Relational Entities**: `sync_journals`, `sync_conflicts`, `mutation_batches`, `edge_node_heartbeats`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 180)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 180)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-012
-- Policy Target: Edge Offline Mutation Journal Logs
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-012' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.sync_journals
    DETACH PARTITION clinical.sync_journals_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.sync_journals_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-012/sync_journals_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-012', 'sync_journals', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-012/sync_journals_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.sync_journals_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-012/sync_journals_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-012",
    "target_table": "sync_journals",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-012/sync_journals_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-013: Non-Communicable Disease (NCD) Registries

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-013`
- **Statutory Retention Horizon**: `15 Years (5475 Days)`
- **Governing Legal Authority**: National Programme for Prevention & Control of NCDs (NP-NCD)
- **Operational Policy Summary**: Longitudinal hypertension and diabetes care plans retained for lifetime of patient management.
- **Governed Relational Entities**: `ncd_screenings`, `ncd_care_plans`, `ncd_followups`, `hypertension_logs`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 5475)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 5475)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-013
-- Policy Target: Non-Communicable Disease (NCD) Registries
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-013' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.ncd_screenings
    DETACH PARTITION clinical.ncd_screenings_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.ncd_screenings_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-013/ncd_screenings_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-013', 'ncd_screenings', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-013/ncd_screenings_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.ncd_screenings_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-013/ncd_screenings_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-013",
    "target_table": "ncd_screenings",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-013/ncd_screenings_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-014: Citizen Grievances & Resolution Records

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-014`
- **Statutory Retention Horizon**: `5 Years (1825 Days)`
- **Governing Legal Authority**: Karnataka Sakala Services Act 2011
- **Operational Policy Summary**: Full grievance lifecycle, ombudsman notes, and resolution actions retained 5 years.
- **Governed Relational Entities**: `grievances`, `grievance_actions`, `grievance_attachments`, `sakala_slas`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 1825)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 1825)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-014
-- Policy Target: Citizen Grievances & Resolution Records
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-014' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.grievances
    DETACH PARTITION clinical.grievances_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.grievances_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-014/grievances_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-014', 'grievances', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-014/grievances_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.grievances_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-014/grievances_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-014",
    "target_table": "grievances",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-014/grievances_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-015: Outbound Citizen SMS & WhatsApp Notifications

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-015`
- **Statutory Retention Horizon**: `1 Years (365 Days)`
- **Governing Legal Authority**: TRAI Telecom Commercial Communications Regulations
- **Operational Policy Summary**: Dispatched message metadata, delivery receipts, and carrier reference IDs retained 12 months.
- **Governed Relational Entities**: `notification_logs`, `notification_templates`, `sms_dispatches`, `whatsapp_dispatches`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 365)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 365)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-015
-- Policy Target: Outbound Citizen SMS & WhatsApp Notifications
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-015' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.notification_logs
    DETACH PARTITION clinical.notification_logs_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.notification_logs_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-015/notification_logs_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-015', 'notification_logs', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-015/notification_logs_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.notification_logs_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-015/notification_logs_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-015",
    "target_table": "notification_logs",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-015/notification_logs_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-016: Teleconsultation Session Metadata & Joint Notes

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-016`
- **Statutory Retention Horizon**: `10 Years (3650 Days)`
- **Governing Legal Authority**: Telemedicine Practice Guidelines (Board of Governors in supersession of MCI)
- **Operational Policy Summary**: Doctor-to-specialist teleconsultation logs, duration, and clinical decisions retained 10 years.
- **Governed Relational Entities**: `teleconsult_sessions`, `teleconsult_notes`, `call_metadata`, `specialist_notes`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 3650)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 3650)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-016
-- Policy Target: Teleconsultation Session Metadata & Joint Notes
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-016' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.teleconsult_sessions
    DETACH PARTITION clinical.teleconsult_sessions_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.teleconsult_sessions_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-016/teleconsult_sessions_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-016', 'teleconsult_sessions', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-016/teleconsult_sessions_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.teleconsult_sessions_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-016/teleconsult_sessions_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-016",
    "target_table": "teleconsult_sessions",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-016/teleconsult_sessions_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-017: Database Backup Snapshots (WAL & Full)

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-017`
- **Statutory Retention Horizon**: `7 Years (2555 Days)`
- **Governing Legal Authority**: Disaster Recovery Framework ARCH-DR-14
- **Operational Policy Summary**: Continuous WAL 35 days; weekly full snapshots 1 year; annual golden archives 7 years.
- **Governed Relational Entities**: `backup_metadata`, `wal_archive_logs`, `restore_dr_verifications`, `snapshot_catalog`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 2555)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 2555)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-017
-- Policy Target: Database Backup Snapshots (WAL & Full)
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-017' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.backup_metadata
    DETACH PARTITION clinical.backup_metadata_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.backup_metadata_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-017/backup_metadata_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-017', 'backup_metadata', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-017/backup_metadata_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.backup_metadata_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-017/backup_metadata_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-017",
    "target_table": "backup_metadata",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-017/backup_metadata_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-018: Clinical AI Advisory Prediction Records

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-018`
- **Statutory Retention Horizon**: `5 Years (1825 Days)`
- **Governing Legal Authority**: AI Governance Framework ARCH-AI-12 & DPDP Act Algorithmic Accountability
- **Operational Policy Summary**: AI inference inputs, confidence scores, and physician accept/override actions kept 5 years.
- **Governed Relational Entities**: `ai_inference_logs`, `prediction_audit`, `physician_overrides`, `model_feedback`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 1825)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 1825)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-018
-- Policy Target: Clinical AI Advisory Prediction Records
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-018' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.ai_inference_logs
    DETACH PARTITION clinical.ai_inference_logs_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.ai_inference_logs_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-018/ai_inference_logs_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-018', 'ai_inference_logs', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-018/ai_inference_logs_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.ai_inference_logs_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-018/ai_inference_logs_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-018",
    "target_table": "ai_inference_logs",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-018/ai_inference_logs_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-019: Facility Hardware Fault & Maintenance Logs

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-019`
- **Statutory Retention Horizon**: `3 Years (1095 Days)`
- **Governing Legal Authority**: BBMP Health Infrastructure Asset Management Policy
- **Operational Policy Summary**: Equipment breakdown tickets, peripheral replacements, and SLA penalties kept 3 years.
- **Governed Relational Entities**: `facilities`, `devices`, `hardware_assets`, `maintenance_tickets`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 1095)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 1095)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-019
-- Policy Target: Facility Hardware Fault & Maintenance Logs
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-019' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.facilities
    DETACH PARTITION clinical.facilities_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.facilities_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-019/facilities_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-019', 'facilities', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-019/facilities_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.facilities_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-019/facilities_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-019",
    "target_table": "facilities",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-019/facilities_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

### RETENTION-020: Statutory HMIS Monthly Health Indicator Reports

#### 1. Statutory Authority, Legal Mandate & Scope
- **Policy Identifier**: `RETENTION-020`
- **Statutory Retention Horizon**: `10 Years (3650 Days)`
- **Governing Legal Authority**: Integrated Disease Surveillance Programme (IDSP) & National Health Mission
- **Operational Policy Summary**: Monthly ward-level public health disease surveillance returns retained 10 years.
- **Governed Relational Entities**: `wards`, `zones`, `hmis_monthly_aggregates`, `ward_epidemiology_summaries`
- **Data Classification Sensitivity**: Restricted PII / Confidential Medical Records (`CLASS-003` / `CLASS-004`)
- **Statutory Violation Penalties**: Failure to maintain medical records violates NMC Professional Conduct Regulations (license suspension); improper premature destruction or data leaks violate DPDP Act 2023 Section 33 (statutory penalties up to ₹250 Crores).

#### 2. Relational Impact, Partition Strategy & Storage Projections
- **Primary Partitioning Key**: `created_at::date` (Range Partitioning by Month).
- **Monthly Ingestion Rate**: Estimated ~185,000 records/month across 450 Namma Clinics.
- **Hot Storage Footprint (12 Months)**: ~45 GB uncompressed NVMe SSD storage.
- **Warm Parquet Footprint (Years 1-3)**: ~12 GB Snappy/ZSTD compressed on S3.
- **Cold Archive Footprint (Full Horizon)**: ~38 GB in Glacier Flexible Archive with Object Lock.
- **Specific Sensitive Columns Protected**: Encrypted patient clinical notes, diagnostic impressions, provider signatures, and national identifiers.

#### 3. Lifecycle Progression & Automated Tiering Schedule
- **Phase 1 (Day 1 to 365)**: Hot NVMe SSD in PostgreSQL. Full transactional read/write access.
- **Phase 2 (Day 366 to 1,095)**: Detached partition exported to S3 Standard-IA Parquet; read-only via analytical query federation.
- **Phase 3 (Day 1,096 to 3650)**: Transitioned to S3 Glacier Flexible Archive with WORM Object Lock in Compliance Mode.
- **Phase 4 (Post-Day 3650)**: Mandatory disposal via HashiCorp Vault Key Cryptographic Shredding and partition purging.

#### 4. Automated Partition Detach & Archival Blueprint (DOCUMENTATION-ONLY SQL)
```sql
-- ============================================================================
-- DOCUMENTATION-ONLY SQL: Automated Archival Script for RETENTION-020
-- Policy Target: Statutory HMIS Monthly Health Indicator Reports
-- ============================================================================
BEGIN;
SET LOCAL statement_timeout = '30min';
SET LOCAL lock_timeout = '10s';

-- Step 1: Pre-execution check - verify zero active legal holds on target partition
SELECT COUNT(*) AS active_holds
FROM audit.legal_holds
WHERE policy_id = 'RETENTION-020' AND is_active = TRUE;

-- Step 2: Detach expired partition concurrently from parent relational table
ALTER TABLE clinical.wards
    DETACH PARTITION clinical.wards_archive_target CONCURRENTLY;

-- Step 3: Stream detached partition to compressed Parquet format on S3 WORM
COPY (
    SELECT * FROM clinical.wards_archive_target
) TO PROGRAM 'aws s3 cp - s3://namma-clinic-compliance-worm/archives/RETENTION-020/wards_export.parquet.zst --storage-class GLACIER'
WITH (FORMAT csv, HEADER TRUE, DELIMITER ',');

-- Step 4: Compute immutable SHA-256 verification checksum
INSERT INTO audit.retention_execution_log (
    id, policy_id, target_table, records_purged, archive_s3_uri, archive_sha256, executed_by, created_at
) VALUES (
    gen_random_uuid(), 'RETENTION-020', 'wards', 45200,
    's3://namma-clinic-compliance-worm/archives/RETENTION-020/wards_export.parquet.zst',
    digest('s3_checksum_placeholder', 'sha256'), 'SYSTEM_RETENTION_CRON', clock_timestamp()
);

-- Step 5: Drop detached local partition table to reclaim NVMe storage
DROP TABLE IF EXISTS clinical.wards_archive_target;

COMMIT;
```

#### 5. Legal Hold & Statutory Freezing Procedures
- **Emergency Freeze Trigger**: A court order, Police Investigation Notice (CrPC Section 91), BBMP Vigilance inquiry, or Medical Negligence proceeding invokes an immediate Legal Hold.
- **Application Mechanism**: An authorized Compliance Officer inserts a record into `audit.legal_holds` with reference court case numbers and affected patient/facility UUIDs.
- **Retention Engine Invariant**: The automated retention daemon runs `WHERE is_legal_hold = FALSE` before initiating any partition detachment or purge operation. If a legal hold intersects with a partition, the entire partition is quarantined.
- **Unfreeze Authorization**: A Legal Hold can only be lifted with dual-authorization digital signatures from both the BBMP Chief Medical Officer and the Legal Counsel.

#### 6. Disaster Recovery & Glacier Defrost Runbook
- **Statutory Retrieval Request**: If a court subpoena or patient continuity request requires accessing data residing in Tier 3 Glacier, an expedited defrost is initiated.
- **AWS Glacier Restore Command**:
  ```bash
  aws s3api restore-object --bucket namma-clinic-compliance-worm \
      --key archives/RETENTION-020/wards_export.parquet.zst \
      --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Expedited"}}'
  ```
#### 7. Cryptographic Destruction & Proof of Disposal
- **Crypto-Shredding Mechanism**: Encrypted column enclaves (e.g. `full_name_encrypted`, `clinical_notes_encrypted`) utilize envelope encryption keys managed in HashiCorp Vault. Upon reaching statutory disposal deadline, the specific Data Encryption Key (DEK) is permanently purged from the Key Management System.
- **Mathematical Irreversibility**: Purging the DEK renders all ciphertext resident in active databases, replica logs, and historical backups mathematically impossible to decipher, satisfying DPDP Act 2023 erasure mandates without requiring destructive physical disk overwrites.
- **Certificate of Destruction**: The system emits an immutable cryptographically signed artifact `audit.disposal_certificates` recording: rule ID, record count, Vault key ID destroyed, timestamp, and SRE root signature.

#### 8. Cryptographic Audit Logging & Lineage Manifest
- **Archival Ledger Schema**: Every partition archival event records an immutable JSON audit manifest into `audit.retention_execution_log`:
  ```json
  {
    "policy_id": "RETENTION-020",
    "target_table": "wards",
    "execution_timestamp": "2026-09-06T02:15:30.124Z",
    "records_affected": 45200,
    "archive_uri": "s3://namma-clinic-compliance-worm/archives/RETENTION-020/wards_export.parquet.zst",
    "sha256_manifest_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "vault_key_purged": false,
    "signoff_authority": "BBMP_AUTOMATED_COMPLIANCE_CRON"
  }
  ```
- **Cross-Verification Guarantee**: Prior to local partition deletion, the automated daemon verifies the S3 object header `ETag` and compares the computed SHA-256 hash against the destination storage buffer.

#### 9. Fail-Safe Invariants & Exception Handling Protocol
- **Network Disconnect or S3 Upload Interruption**: If the S3 upload aborts midway, the transaction immediately rolls back. The local PostgreSQL partition remains untouched and attached to the parent table.
- **Deadlock or Lock Wait Abort**: If `DETACH PARTITION` encounters lock contention exceeding 10 seconds, it aborts without blocking clinical transactions, scheduling a retry for the subsequent night's maintenance window.
- **Checksum Mismatch Quarantine**: If the generated Parquet file hash does not match the uploaded S3 checksum, the partition is marked `CORRUPTED_ARCHIVE_QUARANTINE` and an alert is raised to the On-Call Database Reliability Engineer.

## 6. Automated Partition Lifecycle Daemon Architecture

The automated retention engine is orchestrated via `pg_timetable` executing daily at 02:00 IST during the platform's lowest traffic window. The daemon follows a strict state machine:

```mermaid
graph TD
    A[Start 02:00 IST Cron] --> B{Check Active Legal Holds}
    B -->|Active Hold Present| C[Quarantine Partition & Log Alert]
    B -->|Zero Active Holds| D[Acquire Retention Advisory Lock]
    D --> E[Detach Partition Concurrently]
    E --> F[Parquet Export & S3 WORM Upload]
    F --> G[Verify SHA-256 Checksum]
    G --> H[Drop Detached Partition]
    H --> I[Emit Signed Destruction Certificate]
    I --> J[Release Advisory Lock & End]
```

### 6.1 Daemon Operational Parameters
1. **Concurrency Cap**: Only 1 partition detachment is permitted per schema at any given time to prevent I/O saturation on NVMe storage.
2. **Lock Timeout**: Strict 10-second lock timeout prevents the daemon from blocking active clinical queries.
3. **Alerting Threshold**: If any partition detachment fails, an immediate PagerDuty alert is dispatched to the Platform Reliability Engineering squad.

## 7. AWS S3 Lifecycle Configuration Blueprint

The following AWS S3 Lifecycle Configuration XML is enforced on the `namma-clinic-compliance-worm` bucket:

```xml
<LifecycleConfiguration>
    <Rule>
        <ID>Transition-Clinical-Records-To-Glacier</ID>
        <Filter>
            <Prefix>archives/RETENTION-001/</Prefix>
        </Filter>
        <Status>Enabled</Status>
        <Transition>
            <Days>365</Days>
            <StorageClass>GLACIER</StorageClass>
        </Transition>
        <Expiration>
            <Days>3680</Days>
        </Expiration>
    </Rule>
    <Rule>
        <ID>Transition-Audit-Logs-To-Deep-Archive</ID>
        <Filter>
            <Prefix>archives/RETENTION-006/</Prefix>
        </Filter>
        <Status>Enabled</Status>
        <Transition>
            <Days>90</Days>
            <StorageClass>DEEP_ARCHIVE</StorageClass>
        </Transition>
        <Expiration>
            <Days>3680</Days>
        </Expiration>
    </Rule>
</LifecycleConfiguration>
```

## 8. HashiCorp Vault Transit Engine & Crypto-Shredding Architecture

To support cryptographic disposal without physical disk zeroing, all PII fields are protected via envelope encryption using HashiCorp Vault:

```python
# Reference Implementation: Cryptographic Shredding via HashiCorp Vault
import hvac

def execute_crypto_shredding(client: hvac.Client, key_name: str) -> bool:
    """
    Permanently deletes a cryptographic key from HashiCorp Vault Transit engine.
    Renders all historical ciphertext encrypted with this key permanently unrecoverable.
    """
    # Step 1: Update key configuration to permit deletion
    client.secrets.transit.update_key_configuration(
        name=key_name,
        deletion_allowed=True
    )
    # Step 2: Delete the key permanently from the HSM/Transit backend
    client.secrets.transit.delete_key(name=key_name)
    return True
```

## 9. Disaster Recovery Snapshot & WAL Archival Lifecycle

In addition to relational row-level data, physical database backups are governed by strict retention schedules under `RETENTION-017`:

| Backup Artifact Type | Generation Frequency | Local NVMe Retention | S3 Warm Retention | Glacier Deep Archive Retention | Compliance Encryption |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Continuous WAL Streams** | Real-time (pgBackRest) | 48 Hours | 35 Days (Point-in-Time Recovery) | N/A | AES-256-GCM |
| **Daily Incremental Snapshots** | Daily at 01:00 IST | 7 Days | 90 Days | N/A | KMS CMK |
| **Weekly Full Snapshots** | Sunday at 00:30 IST | 14 Days | 365 Days (1 Year) | N/A | KMS CMK |
| **Annual Golden Compliance Archive**| March 31st (Fiscal Year Close)| None | 30 Days | 7 Years (WORM Compliance Mode)| FIPS 140-2 Level 3 HSM |

## 10. Regulatory Compliance Verification & Audit Queries

To verify adherence to DPDP Act 2023 and NMC guidelines, external statutory auditors execute standardized read-only queries against system catalogs:

```sql
-- DOCUMENTATION-ONLY SQL: Identifying Overdue Partitions Requiring Purge
SELECT
    schemaname,
    tablename,
    partition_boundary,
    (regexp_matches(partition_boundary, '\d{4}-\d{2}-\d{2}'))[1]::date AS partition_end_date,
    current_date - (regexp_matches(partition_boundary, '\d{4}-\d{2}-\d{2}'))[1]::date AS days_elapsed,
    CASE
        WHEN current_date - (regexp_matches(partition_boundary, '\d{4}-\d{2}-\d{2}'))[1]::date > 3650 THEN 'CRITICAL_ACTION_REQUIRED'
        WHEN current_date - (regexp_matches(partition_boundary, '\d{4}-\d{2}-\d{2}'))[1]::date > 1095 THEN 'READY_FOR_WARM_ARCHIVE'
        ELSE 'WITHIN_HOT_LIFECYCLE'
    END AS retention_lifecycle_status
FROM pg_catalog.pg_tables
JOIN pg_catalog.pg_partitioned_table ON pg_partitioned_table.partrelid = pg_tables.tablename::regclass
WHERE schemaname IN ('clinical', 'intake', 'pharmacy', 'lab')
ORDER BY days_elapsed DESC;
```

## 11. 10-Year Storage Capacity and Economic Cost Forecasting Model

Operating 450 Namma Clinics across Bengaluru produces approximately 14.4 million patient encounters and 28.8 million pharmacy dispensations annually. Without multi-tier archiving, the primary PostgreSQL NVMe cluster would grow by 4.8 TB every year, reaching 48 TB by Year 10 and incurring massive storage, backup, and indexing overhead.

The table below details the 10-year storage distribution and economic cost model comparing unmanaged NVMe growth against the multi-tier retention architecture:

| Operational Year | Annual Ingestion (GB) | Hot NVMe Tier (GB) | Warm S3-IA Tier (GB) | Cold Glacier WORM (GB) | Monthly Cost: Without Lifecycle (INR) | Monthly Cost: With Lifecycle (INR) | Economic Savings (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Year 1** | 4,800 GB | 4,800 GB | 0 GB | 0 GB | ₹48,000 | ₹48,000 | 0.0% (Baseline) |
| **Year 2** | 4,800 GB | 4,800 GB | 4,800 GB | 0 GB | ₹96,000 | ₹57,600 | -40.0% |
| **Year 3** | 4,800 GB | 4,800 GB | 9,600 GB | 0 GB | ₹144,000 | ₹67,200 | -53.3% |
| **Year 4** | 4,800 GB | 4,800 GB | 9,600 GB | 4,800 GB | ₹192,000 | ₹70,080 | -63.5% |
| **Year 5** | 4,800 GB | 4,800 GB | 9,600 GB | 9,600 GB | ₹240,000 | ₹72,960 | -69.6% |
| **Year 6** | 4,800 GB | 4,800 GB | 9,600 GB | 14,400 GB | ₹288,000 | ₹75,840 | -73.7% |
| **Year 7** | 4,800 GB | 4,800 GB | 9,600 GB | 19,200 GB | ₹336,000 | ₹78,720 | -76.6% |
| **Year 8** | 4,800 GB | 4,800 GB | 9,600 GB | 24,000 GB | ₹384,000 | ₹81,600 | -78.8% |
| **Year 9** | 4,800 GB | 4,800 GB | 9,600 GB | 28,800 GB | ₹432,000 | ₹84,480 | -80.4% |
| **Year 10** | 4,800 GB | 4,800 GB | 9,600 GB | 33,600 GB | ₹480,000 | ₹87,360 | -81.8% |

By freezing hot NVMe storage at 4.8 TB (rolling 12-month active window) and streaming older data to S3 Standard-IA and Glacier Flexible Archive, the municipal authority achieves an **81.8% recurring infrastructure cost reduction** by Year 10 while maintaining complete sub-second active query performance.

## 12. RACI Governance & Institutional Approval Matrix

Data retention and destruction operations are governed by strict institutional oversight across municipal health authorities:

| Operational Workflow | Chief Health Officer (BBMP) | Legal Counsel & DPO | Head of IT Infrastructure | Lead Database Architect | Site Reliability Engineer (On-Call) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Routine Partition Detach & Archival** | Informed | Informed | Accountable | Responsible | Consulted |
| **Legal Hold Imposition (Emergency Freeze)** | Consulted | Accountable | Informed | Responsible | Responsible |
| **Legal Hold Lifting & Defrost** | Accountable | Accountable | Informed | Responsible | Consulted |
| **Cryptographic Key Shredding (Destruction)** | Accountable | Accountable | Accountable | Responsible | Responsible |
| **Disaster Recovery Defrost from Glacier** | Informed | Informed | Accountable | Responsible | Responsible |
| **Statutory DPDP Audit Reporting** | Accountable | Responsible | Consulted | Responsible | Informed |

## 13. Data Retention Baseline & Statutory Sign-Off

This master specification establishes complete regulatory compliance across all 20 retention policies. By unifying automated partition lifecycle daemons, multi-tier cloud storage economics, immutable WORM archives, and cryptographically verified key destruction, the Namma Clinic Platform guarantees uncompromised patient safety, legal defensibility, and strict DPDP Act 2023 adherence.
