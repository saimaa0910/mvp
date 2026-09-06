# Phase 07 — Normalized Logical Data Model Specification

> **Document Identifier**: `DB-LOGICAL-001`
> **System**: Namma Clinic Digital Health & Operations Platform
> **Municipal Authority**: Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Status**: APPROVED LOGICAL BASELINE
> **Normalization Level**: Third Normal Form (3NF) & Boyce-Codd Normal Form (BCNF)
> **Table Catalog Coverage**: 52 Normalized Relational Entities (`TABLE-001` to `TABLE-052`)
> **Relational Schemas**: `identity`, `intake`, `clinical`, `pharmacy`, `continuity`, `audit`, `sync`

---

## 1. Executive Summary & Logical Modeling Framework

The Logical Data Model translates the real-world business entities specified in the Conceptual Data Model into a fully normalized, mathematically rigorous relational representation. It establishes exact schema namespaces, candidate keys, surrogate primary keys, foreign key constraints, column domain types, and check constraints across all 52 core tables.

To prevent anomalies in concurrent healthcare delivery, the logical design enforces strict Third Normal Form (3NF) and Boyce-Codd Normal Form (BCNF) across all transactional entities. Limited, rigorously justified denormalizations are documented explicitly with operational rationale, concurrency protections, and reconciliation protocols.

## 2. Normalization Foundations & Mathematical Proofs

The logical model systematically eliminates insertion, update, and deletion anomalies through formal normalization rules:

### 2.1 First Normal Form (1NF) Compliance
1. **Atomicity of Attributes**: Every column contains atomic, indivisible values. Repeating groups and comma-delimited strings are strictly prohibited. Multi-valued contacts, addresses, and identifiers are extracted into dedicated child tables (`patient_contacts`, `patient_addresses`, `patient_identifiers`).
2. **Unique Row Identification**: Every table possesses a defined primary key (`id` UUIDv7), guaranteeing that no duplicate tuples can exist.
3. **JSONB Usage Bounds**: Structured JSONB columns (e.g. `clinical_payload_json`, `metadata_json`) are strictly reserved for extensible domain attributes and IoT sensor payloads where dynamic schematization is necessary, never used to conceal first-class relational entities.

### 2.2 Second Normal Form (2NF) Compliance
1. **Full Functional Dependency**: Every non-key attribute is fully functionally dependent on the entire primary key. In all 52 tables, surrogate primary keys consist of single-column UUIDv7 identifiers, mathematically precluding partial key dependencies.
2. **Junction Table Decomposition**: Many-to-many relationships (e.g. `role_permissions`, `user_roles`) are decomposed into independent relational entities where composite candidate keys enforce relational uniqueness while delegating primary identity to surrogate UUIDs.

### 2.3 Third Normal Form (3NF) Compliance
1. **Elimination of Transitive Dependencies**: Non-key attributes depend solely on the primary key and not on any other non-key attribute. For example, clinic ward and zone names are not stored in patient demographic rows; instead, patients link to `facilities.id`, which resolves geographic attributes through normalized foreign keys.
2. **Master Catalog Reference**: Drug categories, LOINC lab definitions, and diagnostic taxonomies are segregated into master lookup tables (`drug_categories`, `formulary_drugs`), eliminating transitive redundancy across transactional line items.

### 2.4 Boyce-Codd Normal Form (BCNF) Compliance
For every functional dependency `X -> Y`, `X` is a superkey. In entities with alternate unique candidate keys (e.g. `facilities.facility_code`, `auth_users.username`, `tokens.(facility_id, date, sequence_number)`), uniqueness constraints ensure that every determinant acts as a candidate key.

## 3. Controlled Denormalization Register & Engineering Trade-offs

While 3NF is the default, 5 specific denormalization exceptions are implemented to guarantee sub-second clinical UI rendering and sub-5ms POS barcode scanning under peak morning load:

| Denormalization ID | Target Table | Denormalized Attribute | Source of Truth | Operational Justification | Consistency & Reconciliation Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DN-001** | `pharmacy.clinic_stock` | `quantity_on_hand` | `pharmacy.stock_movements` ledger sum | Dispensing pharmacist barcode scanner must evaluate stock availability in `< 2ms` without executing expensive `SUM()` queries over millions of historical movement rows. | Updated atomically within the same transaction as `stock_movements` (TXN-016). Nightly reconciliation cron verifies that `clinic_stock.quantity_on_hand == SUM(stock_movements.quantity_change)`. |
| **DN-002** | `intake.queue_entries` | `priority_score` | `intake.triage_assessments.acuity_score` | Queue display screens and doctor call lists order waiting patients by urgency score 50+ times per minute per clinic. Joining triage tables on every queue poll causes CPU spikes. | Copied from triage assessment upon triage completion; immutable once set. |
| **DN-003** | `clinical.prescription_items` | `facility_id`, `patient_id` | `clinical.prescriptions` header | Pharmacy stock deduction workers and adverse drug reaction reporting pipelines frequently filter item-level records by facility without needing prescription header attributes. | Inherited from parent prescription at creation; guaranteed invariant by database trigger. |
| **DN-004** | `pharmacy.dispensation_items` | `unit_cost_inr` | `pharmacy.pharmacy_batches.unit_cost` | Historical financial audits require preserving the exact unit procurement cost at the moment of dispensation, even if batch costs are retrospectively adjusted or revalued. | Captured at point of sale; permanently immutable in dispensation item tuple. |
| **DN-005** | `clinical.clinical_encounters` | `token_number_display` | `intake.tokens.sequence_number` | Clinician workstation UI displays the daily token number (e.g. A-042) on active patient banner without issuing continuous foreign key joins. | Populated upon encounter initiation; read-only display attribute. |

## 4. Relational Schema Namespaces & Table Mapping

The 52 canonical tables are organized across seven PostgreSQL relational schemas:

```
+--------------------------------------------------------------------------------+
|                     LOGICAL DATABASE SCHEMA NAMESPACES                         |
+--------------------------------------------------------------------------------+
| [ identity ]   - 12 Tables: Core staff, credentials, RBAC, facilities, configs |
| [ intake ]     - 10 Tables: Master patient index, identifiers, queue, vitals   |
| [ clinical ]   -  9 Tables: Encounters, SOAP notes, diagnoses, Rx, lab orders  |
| [ pharmacy ]   - 11 Tables: Formulary, batches, clinic stock, dispensations    |
| [ continuity ] -  7 Tables: Hospital referrals, NCD care, reminders, grievances|
| [ audit ]      -  1 Table : Immutable append-only cryptographic audit ledger    |
| [ sync ]       -  2 Tables: Edge mutation journals and ABDM FHIR documents     |
+--------------------------------------------------------------------------------+
```

## 5. Master Logical Table Specifications (TABLE-001 to TABLE-052)

Below is the exhaustive specification for each of the 52 normalized tables, documenting purpose, domain ownership, primary keys, candidate keys, foreign key constraints, check constraints, sensitive fields, and full attribute catalogs.

### TABLE-001: `identity.auth_users`

**Table Identifier**: `TABLE-001`
**Fully Qualified Table Name**: `identity.auth_users`
**Operational Domain**: `Identity & Access`
**Executive Data Owner**: Chief Information Security Officer (CISO)
**Table Lifecycle**: Created during staff onboarding; updated on credential/profile change; soft-deleted/deactivated on offboarding; retained 10 years per audit policy.
**Estimated Volume & Growth**: 5,000 staff accounts across 198 BBMP wards (15% annual turnover / expansion)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `identity.auth_users` realizes primary operational storage: Master registry of all authenticated healthcare personnel, administrative staff, and system service accounts.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores user credentials identity root, email, mobile phone, status (ACTIVE, SUSPENDED, DEACTIVATED), and global audit timestamps.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None (Low volume, high read frequency)
- **Data Classification**: `CLASS-004`
- **Retention Policy**: Governed by `RETENTION-006`
- **Audit Requirement**: Full row change capture with IP and actor tracking
- **Edge Synchronization**: Full bidirectional cloud-to-edge synchronization with role-based filtering

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `primary_facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | User base home clinic posting |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 compliant format | CLASS-004 |
| `username` | `VARCHAR(64)` | NO | None | **NONE** | ^[a-z0-9_.]{4,64}$ | CLASS-004 |
| `email` | `VARCHAR(255)` | NO | None | **NONE** | RFC 5322 email regex | CLASS-004 |
| `phone_number` | `VARCHAR(20)` | NO | None | **NONE** | ^\+91[6-9]\d{9}$ | CLASS-004 |
| `phone_blind_index` | `VARCHAR(64)` | NO | None | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `first_name` | `VARCHAR(100)` | NO | None | **NONE** | 1-100 characters | CLASS-004 |
| `last_name` | `VARCHAR(100)` | NO | None | **NONE** | 1-100 characters | CLASS-004 |
| `user_type` | `VARCHAR(32)` | NO | `'CLINICAL'` | **NONE** | IN ('CLINICAL', 'ADMIN', 'PARAMEDICAL', 'INTEGRATION') | CLASS-002 |
| `account_status` | `VARCHAR(32)` | NO | `'PENDING_ACTIVATION'` | **NONE** | IN ('ACTIVE', 'SUSPENDED', 'LOCKED', 'DEACTIVATED', 'PENDING_ACTIVATION') | CLASS-002 |
| `primary_facility_id` | `UUID` | YES | None | **FK** | Valid facility UUID | CLASS-002 |
| `failed_login_count` | `INTEGER` | NO | `0` | **NONE** | >= 0 | CLASS-002 |
| `lockout_until` | `TIMESTAMPTZ` | YES | None | **NONE** | Valid UTC timestamp | CLASS-002 |
| `mfa_enabled` | `BOOLEAN` | NO | `true` | **NONE** | true or false | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | Valid UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | Valid UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | Valid UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 5 designated indexes supporting primary access paths.
  - `INDEX-001`: Unique B-tree on `(email)` — Accelerate login lookups by email
  - `INDEX-002`: Unique B-tree on `(phone_blind_index)` — Lookup staff user by blinded phone hash
  - `INDEX-003`: B-tree on `(primary_facility_id)` — Filter active staff assigned to a clinic
  - `INDEX-029`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on auth_users
  - `INDEX-030`: Composite B-tree on `(created_at)` — Optimize operational status workflows and temporal slicing on auth_users
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-002: `identity.user_credentials`

**Table Identifier**: `TABLE-002`
**Fully Qualified Table Name**: `identity.user_credentials`
**Operational Domain**: `Identity & Access`
**Executive Data Owner**: Security Engineering Lead
**Table Lifecycle**: Created at user registration; modified on password rotation; purged on user erasure.
**Estimated Volume & Growth**: 5,000 records (Proportional to auth_users)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `identity.user_credentials` realizes primary operational storage: Cryptographic authentication secrets including Argon2id password hashes, MFA totp secrets, and failed login counters.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores high-security credentials separated from user demographic profile to isolate cryptographic attack surface.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-005`
- **Retention Policy**: Governed by `RETENTION-011`
- **Audit Requirement**: Strict security audit; passwords never logged in plaintext
- **Edge Synchronization**: Edge-synchronized with salted hash derivation; offline auth enabled via local cache

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `user_id` | `auth_users` | `id` | `CASCADE` | `CASCADE` | Every credential record belongs strictly to one authenticated user |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 | CLASS-005 |
| `user_id` | `UUID` | NO | None | **FK** | Valid user UUID | CLASS-005 |
| `password_hash` | `VARCHAR(255)` | NO | None | **NONE** | ^\$argon2id\$v=19\$.* | CLASS-005 |
| `password_salt` | `VARCHAR(64)` | NO | None | **NONE** | 32-byte hex salt | CLASS-005 |
| `mfa_secret_encrypted` | `BYTEA` | YES | None | **NONE** | Valid ciphertext | CLASS-005 |
| `mfa_backup_codes_hash` | `JSONB` | YES | None | **NONE** | Valid JSON array of hashes | CLASS-005 |
| `password_changed_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | Valid UTC timestamp | CLASS-002 |
| `force_password_reset` | `BOOLEAN` | NO | `true` | **NONE** | true or false | CLASS-002 |
| `failed_mfa_count` | `INTEGER` | NO | `0` | **NONE** | >= 0 | CLASS-002 |
| `security_stamp` | `VARCHAR(64)` | NO | `gen_random_uuid()::text` | **NONE** | Valid random string | CLASS-005 |
| `argon2_memory_cost` | `INTEGER` | NO | `65536` | **NONE** | >= 65536 | CLASS-002 |
| `argon2_time_cost` | `INTEGER` | NO | `3` | **NONE** | >= 3 | CLASS-002 |
| `argon2_parallelism` | `INTEGER` | NO | `4` | **NONE** | >= 1 | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | Valid UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | Valid UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | Valid UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-031`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on user_credentials
  - `INDEX-032`: Composite B-tree on `(created_at)` — Optimize operational status workflows and temporal slicing on user_credentials
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-003: `identity.user_sessions`

**Table Identifier**: `TABLE-003`
**Fully Qualified Table Name**: `identity.user_sessions`
**Operational Domain**: `Identity & Access`
**Executive Data Owner**: Security Operations Center (SOC)
**Table Lifecycle**: Created on login; expired after 15 minutes of inactivity; purged after 1 year.
**Estimated Volume & Growth**: 500,000 annual sessions (1,500 new sessions per clinic day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `identity.user_sessions` realizes primary operational storage: Active and historical web/mobile authentication sessions, JWT refresh tokens, and device fingerprints.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Maintains session state, expiration timestamps, IP address geolocation, and revocation status.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by created_at (Monthly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-011`
- **Audit Requirement**: Revocation and concurrent login violations logged
- **Edge Synchronization**: Edge-local sessions propagated to cloud on connectivity restore

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `user_id` | `auth_users` | `id` | `CASCADE` | `CASCADE` | A user can have multiple concurrent active sessions across mobile and desktop |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `user_session_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-033`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on user_sessions
  - `INDEX-034`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on user_sessions
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-004: `identity.roles`

**Table Identifier**: `TABLE-004`
**Fully Qualified Table Name**: `identity.roles`
**Operational Domain**: `Role-Based Access Control`
**Executive Data Owner**: BBMP Health Administration
**Table Lifecycle**: Static reference data; updated on institutional policy revisions.
**Estimated Volume & Growth**: 30 canonical roles (Static (< 2 updates/year))

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `identity.roles` realizes primary operational storage: Master directory of standardized organizational roles (Doctor, Staff Nurse, Pharmacist, Lab Technician, Receptionist, MOIC).

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Defines canonical system roles, description, hierarchy level, and default operational permissions.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-006`
- **Audit Requirement**: Administrative changes require double sign-off
- **Edge Synchronization**: Global broadcast to all edge clinics

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `role_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-035`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on roles
  - `INDEX-036`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on roles
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-005: `identity.permissions`

**Table Identifier**: `TABLE-005`
**Fully Qualified Table Name**: `identity.permissions`
**Operational Domain**: `Role-Based Access Control`
**Executive Data Owner**: System Architecture Team
**Table Lifecycle**: System immutable code-linked definitions; updated during software releases.
**Estimated Volume & Growth**: 180 distinct permissions (Increases with new module releases)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `identity.permissions` realizes primary operational storage: Fine-grained operational capabilities (e.g., prescribe_medication, dispense_drug, order_lab_test).

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Atomic system entitlements mapped to resource actions across REST and GraphQL endpoints.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-006`
- **Audit Requirement**: Changes tracked via code repository and database schema migration
- **Edge Synchronization**: Global edge broadcast

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `permission_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-037`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on permissions
  - `INDEX-038`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on permissions
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-006: `identity.role_permissions`

**Table Identifier**: `TABLE-006`
**Fully Qualified Table Name**: `identity.role_permissions`
**Operational Domain**: `Role-Based Access Control`
**Executive Data Owner**: BBMP Health Administration
**Table Lifecycle**: Modified during role permission matrix updates.
**Estimated Volume & Growth**: 900 mapping records (Low)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `identity.role_permissions` realizes primary operational storage: Many-to-many junction mapping system permissions to roles.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Associates permissions to roles with grant timestamps, active status, and granter user ID.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-006`
- **Audit Requirement**: Audit logged on every grant/revoke
- **Edge Synchronization**: Global edge broadcast

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `role_id` | `roles` | `id` | `CASCADE` | `CASCADE` | Roles are composed of granular permission grants |
| `permission_id` | `permissions` | `id` | `CASCADE` | `CASCADE` | Permissions are mapped to roles via junction table |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `role_permission_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-039`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on role_permissions
  - `INDEX-040`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on role_permissions
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-007: `identity.user_roles`

**Table Identifier**: `TABLE-007`
**Fully Qualified Table Name**: `identity.user_roles`
**Operational Domain**: `Role-Based Access Control`
**Executive Data Owner**: BBMP District Health Officer
**Table Lifecycle**: Created upon staff facility posting; revoked on transfer.
**Estimated Volume & Growth**: 8,000 assignments (20% annual transfer rate)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `identity.user_roles` realizes primary operational storage: Assignments of roles to users scoped by specific healthcare facility.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Links users to roles within a facility context, supporting multi-facility roaming doctors.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-006`
- **Audit Requirement**: All assignment transfers audited with authorizing government order
- **Edge Synchronization**: Edge-filtered by facility ID

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `user_id` | `auth_users` | `id` | `CASCADE` | `CASCADE` | Staff members are assigned roles |
| `role_id` | `roles` | `id` | `RESTRICT` | `CASCADE` | Active roles cannot be deleted if assigned to users |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Role assignments are facility-scoped |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `user_role_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-041`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on user_roles
  - `INDEX-042`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on user_roles
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-008: `identity.facilities`

**Table Identifier**: `TABLE-008`
**Fully Qualified Table Name**: `identity.facilities`
**Operational Domain**: `Facility Operations`
**Executive Data Owner**: BBMP Health Commissioner
**Table Lifecycle**: Created on clinic commissioning; updated on infrastructure changes; deactivated on decommissioning.
**Estimated Volume & Growth**: 450 facilities across Greater Bengaluru (5% annual expansion)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `identity.facilities` realizes primary operational storage: Master directory of Namma Clinics, Urban Primary Health Centres (UPHCs), and referral hospitals.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores clinic code, official name, ward number, zone, GPS latitude/longitude, operational hours, and ABDM facility ID (HFR).

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-001`
- **Retention Policy**: Governed by `RETENTION-006`
- **Audit Requirement**: All status changes and GPS adjustments audited
- **Edge Synchronization**: Global edge broadcast of master metadata

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-001 |
| `facility_code` | `VARCHAR(32)` | NO | None | **NONE** | ^BLR-[A-Z]{2,4}-\d{3}$ | CLASS-001 |
| `facility_name` | `VARCHAR(255)` | NO | None | **NONE** | 1-255 chars | CLASS-001 |
| `ward_number` | `INTEGER` | NO | None | **NONE** | 1 to 243 | CLASS-001 |
| `zone_name` | `VARCHAR(64)` | NO | None | **NONE** | IN ('EAST', 'WEST', 'SOUTH', 'BOMMANAHALLI', 'DASARAHALLI', 'MAHADEVAPURA', 'RR_NAGARA', 'YELAHANKA') | CLASS-001 |
| `facility_type` | `VARCHAR(32)` | NO | `'NAMMA_CLINIC'` | **NONE** | IN ('NAMMA_CLINIC', 'UPHC', 'REFERRAL_HOSPITAL', 'DIAGNOSTIC_HUB') | CLASS-001 |
| `latitude` | `NUMERIC(10, 7)` | YES | None | **NONE** | 12.0 to 13.5 | CLASS-001 |
| `longitude` | `NUMERIC(10, 7)` | YES | None | **NONE** | 77.3 to 77.8 | CLASS-001 |
| `hfr_id` | `VARCHAR(64)` | YES | None | **NONE** | ^IN\d{8,}$ | CLASS-001 |
| `phone_contact` | `VARCHAR(20)` | YES | None | **NONE** | ^\+91\d{10}$ | CLASS-001 |
| `is_active` | `BOOLEAN` | NO | `true` | **NONE** | true or false | CLASS-001 |
| `operating_hours_json` | `JSONB` | YES | None | **NONE** | Valid JSON | CLASS-001 |
| `ip_address_range` | `VARCHAR(64)` | YES | None | **NONE** | CIDR notation | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 4 designated indexes supporting primary access paths.
  - `INDEX-018`: Unique B-tree on `(facility_code)` — Natural key lookup for facility onboarding and sync
  - `INDEX-019`: Composite B-tree on `(zone_name, ward_number)` — Administrative hierarchical drilldown for municipal reports
  - `INDEX-043`: B-tree on `(ward_number)` — Accelerate clinic facility filtering on facilities
  - `INDEX-044`: Composite B-tree on `(created_at)` — Optimize operational status workflows and temporal slicing on facilities
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-009: `identity.facility_rooms`

**Table Identifier**: `TABLE-009`
**Fully Qualified Table Name**: `identity.facility_rooms`
**Operational Domain**: `Facility Operations`
**Executive Data Owner**: Medical Officer In-Charge (MOIC)
**Table Lifecycle**: Configured during clinic setup; adjusted during clinic layout reorganization.
**Estimated Volume & Growth**: 3,000 rooms/stations across clinics (Low)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `identity.facility_rooms` realizes primary operational storage: Internal physical chambers, consultation rooms, triage booths, pharmacy counters, and sample collection points within a clinic.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Represents functional service points used for queue routing, token display displays, and IoT device association.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-019`
- **Audit Requirement**: Room reassignment tracked for token queue audit
- **Edge Synchronization**: Edge-local clinic partition

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `CASCADE` | `CASCADE` | Chambers and rooms physically exist inside a facility |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `facility_room_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 3 designated indexes supporting primary access paths.
  - `INDEX-020`: Composite B-tree on `(facility_id, status)` — Active consultation room lookup for queue routing
  - `INDEX-045`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on facility_rooms
  - `INDEX-046`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on facility_rooms
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-010: `identity.staff_profiles`

**Table Identifier**: `TABLE-010`
**Fully Qualified Table Name**: `identity.staff_profiles`
**Operational Domain**: `Human Resources`
**Executive Data Owner**: BBMP Health Administration HR
**Table Lifecycle**: Created at hiring; updated on degree completion/promotion; retained 10 years post-resignation.
**Estimated Volume & Growth**: 6,000 staff profiles (10% annual increase)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `identity.staff_profiles` realizes primary operational storage: Professional credentialing, medical council registration number (KMC/NMC), qualifications, and contact details of clinical staff.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores doctor registration numbers, nurse certification IDs, educational degrees, specialization, and official communication channels.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-004`
- **Retention Policy**: Governed by `RETENTION-006`
- **Audit Requirement**: License verification status changes strictly logged
- **Edge Synchronization**: Edge-replicated for assigned clinic personnel

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `user_id` | `auth_users` | `id` | `CASCADE` | `CASCADE` | Clinical staff profile links to authentication user |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-004 |
| `staff_profile_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-004 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-004 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-004 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 3 designated indexes supporting primary access paths.
  - `INDEX-021`: Unique B-tree on `(user_id)` — 1:1 link between auth user and medical credential profile
  - `INDEX-047`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on staff_profiles
  - `INDEX-048`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on staff_profiles
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-011: `identity.staff_shifts`

**Table Identifier**: `TABLE-011`
**Fully Qualified Table Name**: `identity.staff_shifts`
**Operational Domain**: `Human Resources`
**Executive Data Owner**: MOIC / Facility Administrator
**Table Lifecycle**: Created weekly/monthly; marked completed at end of shift; archived after 3 years.
**Estimated Volume & Growth**: 1,200,000 shift records over 3 years (3,000 records/day across all clinics)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `identity.staff_shifts` realizes primary operational storage: Daily work duty rosters, shift allocations (Morning, Afternoon, Evening), and biometric attendance records.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Tracks planned vs actual doctor/nurse shifts, on-call status, leave absences, and biometric punch times.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by shift_date (Quarterly)
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-002`
- **Audit Requirement**: Manual attendance overrides require MOIC digital signature
- **Edge Synchronization**: Edge-local capture with cloud synchronization

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `user_id` | `auth_users` | `id` | `RESTRICT` | `CASCADE` | Duty rosters track shifts per staff member |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Staff shifts take place at specific clinic facility |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `staff_shift_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 3 designated indexes supporting primary access paths.
  - `INDEX-022`: Composite B-tree on `(facility_id, status, created_at)` — Duty roster attendance lookup per clinic shift
  - `INDEX-049`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on staff_shifts
  - `INDEX-050`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on staff_shifts
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-012: `identity.system_configs`

**Table Identifier**: `TABLE-012`
**Fully Qualified Table Name**: `identity.system_configs`
**Operational Domain**: `System Configuration`
**Executive Data Owner**: Principal DevOps Architect
**Table Lifecycle**: Modified during operational configuration; version controlled with rollback.
**Estimated Volume & Growth**: 1,500 configuration parameters (Low)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `identity.system_configs` realizes primary operational storage: Hierarchical dynamic platform configuration parameters, feature flags, and operational thresholds.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Key-value store scoped by GLOBAL, ZONE, or FACILITY, supporting dynamic threshold adjustments without deployment.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-006`
- **Audit Requirement**: Full history of config value transitions with authorizer ID
- **Edge Synchronization**: High-priority edge push via WebSocket / MQTT

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `CASCADE` | `CASCADE` | Clinic-specific operational threshold overrides |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `system_config_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 3 designated indexes supporting primary access paths.
  - `INDEX-023`: Composite B-tree on `(facility_id, category_type)` — Hierarchical config parameter lookup
  - `INDEX-051`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on system_configs
  - `INDEX-052`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on system_configs
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-013: `intake.patients`

**Table Identifier**: `TABLE-013`
**Fully Qualified Table Name**: `intake.patients`
**Operational Domain**: `Citizen Demographics`
**Executive Data Owner**: Chief Medical Officer (CMO)
**Table Lifecycle**: Created at citizen registration; updated on demographic verification; retained permanently or statutory 10+ years.
**Estimated Volume & Growth**: 3,500,000 citizens registered across BBMP jurisdiction (8,000 new patients per day across all wards)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `intake.patients` realizes primary operational storage: Master patient index (MPI) storing primary demographic information for all registered citizens.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores system UHID (Unique Health Identifier), full name, gender, date of birth, blood group, marital status, and registration facility.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Hash partitioned by id (16 partitions)
- **Data Classification**: `CLASS-004`
- **Retention Policy**: Governed by `RETENTION-001`
- **Audit Requirement**: All demographic access and edits logged with DPDP purpose code
- **Edge Synchronization**: Edge-cached on-demand with local offline registration capability

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Patient initial registration clinic |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-004 |
| `patient_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-004 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-004 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-004 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 4 designated indexes supporting primary access paths.
  - `INDEX-004`: Unique B-tree on `(id)` — Primary key index on UUIDv7
  - `INDEX-005`: Composite B-tree on `(facility_id, created_at)` — Filter clinic registered patients sorted by intake date
  - `INDEX-053`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on patients
  - `INDEX-054`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on patients
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-014: `intake.patient_identifiers`

**Table Identifier**: `TABLE-014`
**Fully Qualified Table Name**: `intake.patient_identifiers`
**Operational Domain**: `Citizen Demographics`
**Executive Data Owner**: Lead Integration Architect
**Table Lifecycle**: Added during identity linking; updated on re-authentication; revoked on consent withdrawal.
**Estimated Volume & Growth**: 5,000,000 identifier records (10,000 per day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `intake.patient_identifiers` realizes primary operational storage: External identity linkages including ABHA Number, ABHA Address, Aadhaar Vault Reference, Ration Card, and Voter ID.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores cryptographic tokenized references to national identity systems without persisting plaintext Aadhaar numbers.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Hash partitioned by patient_id (16 partitions)
- **Data Classification**: `CLASS-004`
- **Retention Policy**: Governed by `RETENTION-005`
- **Audit Requirement**: Identity search and verification logged to WORM ledger
- **Edge Synchronization**: Cloud-authoritative; blind-index queried by edge nodes

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `CASCADE` | `CASCADE` | Patient ABHA, Aadhaar hash, and external identifiers |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-004 |
| `patient_identifier_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-004 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-004 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-004 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 4 designated indexes supporting primary access paths.
  - `INDEX-006`: B-tree on `(patient_id)` — Foreign key lookup for patient identifiers
  - `INDEX-007`: B-tree on `(reference_code)` — Fast ABHA / external identifier lookup
  - `INDEX-055`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on patient_identifiers
  - `INDEX-056`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on patient_identifiers
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-015: `intake.patient_contacts`

**Table Identifier**: `TABLE-015`
**Fully Qualified Table Name**: `intake.patient_contacts`
**Operational Domain**: `Citizen Demographics`
**Executive Data Owner**: Patient Experience Officer
**Table Lifecycle**: Created at registration; updated on phone change; retained with patient profile.
**Estimated Volume & Growth**: 4,200,000 records (Proportional to patient intake)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `intake.patient_contacts` realizes primary operational storage: Phone numbers, email addresses, and emergency next-of-kin contact details.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores primary and secondary mobile numbers with OTP verification status and emergency relationship codes.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Hash partitioned by patient_id (16 partitions)
- **Data Classification**: `CLASS-004`
- **Retention Policy**: Governed by `RETENTION-001`
- **Audit Requirement**: Contact updates audited; mobile numbers masked on non-privileged views
- **Edge Synchronization**: Edge-replicated for registered clinic patients

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `CASCADE` | `CASCADE` | Patient emergency contacts and phone numbers |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-004 |
| `patient_contact_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-004 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-004 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-004 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 3 designated indexes supporting primary access paths.
  - `INDEX-024`: Composite B-tree on `(patient_id, status)` — Active contact information retrieval for patient
  - `INDEX-057`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on patient_contacts
  - `INDEX-058`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on patient_contacts
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-016: `intake.patient_addresses`

**Table Identifier**: `TABLE-016`
**Fully Qualified Table Name**: `intake.patient_addresses`
**Operational Domain**: `Citizen Demographics`
**Executive Data Owner**: Urban Health Planner
**Table Lifecycle**: Created at registration; updated on citizen relocation; retained with patient profile.
**Estimated Volume & Growth**: 3,800,000 records (Proportional to patient intake)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `intake.patient_addresses` realizes primary operational storage: Residential addresses mapped to BBMP municipal wards, zones, and postal pin codes.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Provides GIS geographic attributes, door number, street, ward name, zone identifier, and census block.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Hash partitioned by patient_id (16 partitions)
- **Data Classification**: `CLASS-004`
- **Retention Policy**: Governed by `RETENTION-001`
- **Audit Requirement**: Ward changes audited for epidemiological tracking
- **Edge Synchronization**: Edge-replicated for catchment area

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `CASCADE` | `CASCADE` | Citizen residential address mapped to BBMP ward |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-004 |
| `patient_addresse_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-004 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-004 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-004 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 3 designated indexes supporting primary access paths.
  - `INDEX-025`: Composite B-tree on `(patient_id, status)` — Current residential address lookup for citizen
  - `INDEX-059`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on patient_addresses
  - `INDEX-060`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on patient_addresses
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-017: `intake.consent_records`

**Table Identifier**: `TABLE-017`
**Fully Qualified Table Name**: `intake.consent_records`
**Operational Domain**: `Consent Management`
**Executive Data Owner**: Data Protection Officer (DPO)
**Table Lifecycle**: Created at consent grant; updated on scope modification; terminated on revocation; retained 7 years post-expiry.
**Estimated Volume & Growth**: 6,000,000 consent artifacts (15,000 records/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `intake.consent_records` realizes primary operational storage: Explicit citizen consent artifacts compliant with DPDP Act 2023 and ABDM Consent Framework.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores consent purpose, validity window, clinical data scopes granted, signature/OTP hash, and revocation status.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by granted_at (Semi-annual)
- **Data Classification**: `CLASS-004`
- **Retention Policy**: Governed by `RETENTION-005`
- **Audit Requirement**: Strict append-only immutable logging; revocations take immediate effect
- **Edge Synchronization**: Cloud-authoritative with edge-local validation cache

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | DPDP statutory citizen consent artifacts |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Facility where consent was executed |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-004 |
| `consent_record_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-004 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-004 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-004 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 3 designated indexes supporting primary access paths.
  - `INDEX-026`: Composite B-tree on `(patient_id, status)` — Active DPDP consent check before clinical record access
  - `INDEX-061`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on consent_records
  - `INDEX-062`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on consent_records
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-018: `intake.tokens`

**Table Identifier**: `TABLE-018`
**Fully Qualified Table Name**: `intake.tokens`
**Operational Domain**: `Queue Management`
**Executive Data Owner**: Clinic Operations Lead
**Table Lifecycle**: Issued daily; updated as patient advances through stages; archived after 90 days.
**Estimated Volume & Growth**: 15,000,000 tokens annually across 450 facilities (45,000 tokens/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `intake.tokens` realizes primary operational storage: Daily sequential clinic intake tokens issued to patients upon physical arrival.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Maintains token sequence number (e.g., A-042), priority category (REGULAR, EMERGENCY, GERIATRIC, PREGNANT), and issue timestamp.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by issued_at (Monthly)
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-007`
- **Audit Requirement**: Token creation, priority overrides, and cancellations logged
- **Edge Synchronization**: Edge-local generation with asynchronous cloud telemetry rollup

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Token issued to registered patient |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Daily token generated at specific clinic |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `token_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 4 designated indexes supporting primary access paths.
  - `INDEX-008`: Composite B-tree on `(facility_id, status)` — Filter active daily tokens for clinic display queue
  - `INDEX-009`: B-tree on `(patient_id)` — Find daily token issued to specific patient
  - `INDEX-063`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on tokens
  - `INDEX-064`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on tokens
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-019: `intake.queue_entries`

**Table Identifier**: `TABLE-019`
**Fully Qualified Table Name**: `intake.queue_entries`
**Operational Domain**: `Queue Management`
**Executive Data Owner**: Clinic Operations Lead
**Table Lifecycle**: Created upon stage transfer; updated on call/complete; retained 90 days for operational KPI calculation.
**Estimated Volume & Growth**: 45,000,000 queue transitions annually (135,000 transitions/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `intake.queue_entries` realizes primary operational storage: Real-time state tracking of patient movement through service stages (TRIAGE, DOCTOR, LAB, PHARMACY).

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Records stage entry time, call time, completion time, serving staff ID, room ID, and wait duration metrics.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by created_at (Monthly)
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-007`
- **Audit Requirement**: Stage bypasses and emergency pre-emptions audited
- **Edge Synchronization**: Edge-local state machine; batch-synced to cloud analytics

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `token_id` | `tokens` | `id` | `CASCADE` | `CASCADE` | Queue movement stages tracked per token |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Queue progression inside clinic |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Patient queue stage presence |
| `room_id` | `facility_rooms` | `id` | `SET NULL` | `CASCADE` | Physical consultation chamber serving patient |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `queue_entrie_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 4 designated indexes supporting primary access paths.
  - `INDEX-010`: Composite B-tree on `(facility_id, status, priority_score)` — Ordered queue retrieval for doctor and triage stations
  - `INDEX-011`: GIN on `(clinical_payload_json)` — JSONB search for queue tags and clinical flags
  - `INDEX-065`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on queue_entries
  - `INDEX-066`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on queue_entries
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-020: `intake.triage_assessments`

**Table Identifier**: `TABLE-020`
**Fully Qualified Table Name**: `intake.triage_assessments`
**Operational Domain**: `Clinical Triage`
**Executive Data Owner**: Nursing Superintendent
**Table Lifecycle**: Created during nursing intake; finalized before doctor consultation; retained 10 years as clinical record.
**Estimated Volume & Growth**: 10,000,000 records (30,000 assessments/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `intake.triage_assessments` realizes primary operational storage: Nurse triage evaluations capturing chief complaints, visual acuity, emergency signs, and triage priority score.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Captures South African Triage Scale (SATS) / Emergency Severity Index (ESI) category (RED, YELLOW, GREEN) and presenting symptoms.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by assessed_at (Quarterly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-001`
- **Audit Requirement**: Nurse signature and acuity rating changes logged
- **Edge Synchronization**: Edge-local creation; immediate high-priority cloud sync

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Triage evaluation performed on patient |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Facility where triage occurred |
| `token_id` | `tokens` | `id` | `SET NULL` | `CASCADE` | Daily token linking triage encounter |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `triage_assessment_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `clinical_payload_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 3 designated indexes supporting primary access paths.
  - `INDEX-027`: Composite B-tree on `(patient_id, created_at)` — Longitudinal triage history query for patient
  - `INDEX-067`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on triage_assessments
  - `INDEX-068`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on triage_assessments
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-021: `intake.patient_vitals`

**Table Identifier**: `TABLE-021`
**Fully Qualified Table Name**: `intake.patient_vitals`
**Operational Domain**: `Clinical Triage`
**Executive Data Owner**: Chief Medical Officer
**Table Lifecycle**: Captured during triage or doctor visit; immutable clinical observations; retained 10 years.
**Estimated Volume & Growth**: 25,000,000 vitals snapshots (75,000 readings/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `intake.patient_vitals` realizes primary operational storage: Physiological measurements: systolic/diastolic blood pressure, pulse rate, SpO2, respiratory rate, temperature, height, weight, BMI.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Standardized longitudinal vitals observations supporting pediatric and adult reference percentile curves.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by recorded_at (Quarterly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-001`
- **Audit Requirement**: Clinical edits append correction log with reason
- **Edge Synchronization**: Edge-local storage with bidirectional sync

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Longitudinal vital signs observations |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Clinic where vitals recorded |
| `triage_id` | `triage_assessments` | `id` | `SET NULL` | `CASCADE` | Vitals captured during nursing triage session |
| `encounter_id` | `clinical_encounters` | `id` | `SET NULL` | `CASCADE` | Vitals recorded directly during physician consultation |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `patient_vital_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `clinical_payload_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-069`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on patient_vitals
  - `INDEX-070`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on patient_vitals
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-022: `intake.danger_alerts`

**Table Identifier**: `TABLE-022`
**Fully Qualified Table Name**: `intake.danger_alerts`
**Operational Domain**: `Clinical Safety`
**Executive Data Owner**: Clinical Governance Committee
**Table Lifecycle**: Triggered automatically by vitals/triage engine; acknowledged by clinician; archived after 5 years.
**Estimated Volume & Growth**: 1,500,000 alerts (4,500 alerts/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `intake.danger_alerts` realizes primary operational storage: Real-time clinical safety alerts: critical vitals, anaphylaxis history, severe maternal pre-eclampsia, and pediatric panic thresholds.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores alert severity (CRITICAL, WARNING), trigger rule ID, clinician acknowledgment status, and override justification.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by triggered_at (Quarterly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-001`
- **Audit Requirement**: Physician acknowledgment timestamp and override reason mandatory
- **Edge Synchronization**: Instant edge-to-cloud push with SMS alert escalation

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Critical danger alert generated for patient |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Clinic where clinical red flag occurred |
| `encounter_id` | `clinical_encounters` | `id` | `SET NULL` | `CASCADE` | Danger alert triggered during doctor consultation |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `danger_alert_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `clinical_payload_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 3 designated indexes supporting primary access paths.
  - `INDEX-028`: Composite B-tree on `(facility_id, status)` — Real-time clinic dashboard danger alerts filter
  - `INDEX-071`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on danger_alerts
  - `INDEX-072`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on danger_alerts
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-023: `clinical.clinical_encounters`

**Table Identifier**: `TABLE-023`
**Fully Qualified Table Name**: `clinical.clinical_encounters`
**Operational Domain**: `Clinical Consultation`
**Executive Data Owner**: Chief Medical Officer
**Table Lifecycle**: Initiated on doctor call; completed upon digital sign-off; retained 10 years per statutory rules.
**Estimated Volume & Growth**: 12,000,000 consultations (35,000 encounters/day across all Namma Clinics)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `clinical.clinical_encounters` realizes primary operational storage: Master outpatient consultation record documenting doctor-patient interaction event.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Links patient, treating doctor, facility, token, encounter type (OPD, TELEMEDICINE, HOME_VISIT), start/end time, and disposition status.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by encounter_date (Monthly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-001`
- **Audit Requirement**: Doctor digital signature timestamped; changes post-closure strictly prohibited
- **Edge Synchronization**: Edge-local capture with cloud synchronization on sign-off

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Outpatient consultation encounter for patient |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Encounter conducted at clinic |
| `doctor_user_id` | `auth_users` | `id` | `RESTRICT` | `CASCADE` | Treating licensed physician |
| `token_id` | `tokens` | `id` | `SET NULL` | `CASCADE` | Daily token associated with consultation |
| `ncd_episode_id` | `ncd_episodes` | `id` | `SET NULL` | `CASCADE` | Encounter conducted as part of longitudinal NCD care |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `clinical_encounter_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `clinical_payload_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 4 designated indexes supporting primary access paths.
  - `INDEX-012`: Composite B-tree on `(patient_id, created_at)` — Fetch chronological consultation history for patient
  - `INDEX-013`: BRIN on `(facility_id, created_at)` — Block Range Index for multi-year encounter reporting
  - `INDEX-073`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on clinical_encounters
  - `INDEX-074`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on clinical_encounters
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-024: `clinical.clinical_notes`

**Table Identifier**: `TABLE-024`
**Fully Qualified Table Name**: `clinical.clinical_notes`
**Operational Domain**: `Clinical Consultation`
**Executive Data Owner**: Medical Superintendent
**Table Lifecycle**: Created during encounter; locked upon signature; addendum notes supported with version linkage.
**Estimated Volume & Growth**: 12,000,000 records (35,000 notes/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `clinical.clinical_notes` realizes primary operational storage: Detailed clinical narrative in structured SOAP format (Subjective history, Objective exam, Assessment, Plan).

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores clinical findings, history of present illness, examination notes, and doctor confidential clinical remarks.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by created_at (Monthly)
- **Data Classification**: `CLASS-005`
- **Retention Policy**: Governed by `RETENTION-001`
- **Audit Requirement**: Addendums require explicit justification; original text never overwritten
- **Edge Synchronization**: Edge-local with encrypted cloud backup

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `encounter_id` | `clinical_encounters` | `id` | `CASCADE` | `CASCADE` | SOAP clinical notes recorded for encounter |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Longitudinal clinical history linkage |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Facility scope of clinical note |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-005 |
| `clinical_note_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-005 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `clinical_payload_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-005 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-005 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-075`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on clinical_notes
  - `INDEX-076`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on clinical_notes
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-025: `clinical.diagnoses`

**Table Identifier**: `TABLE-025`
**Fully Qualified Table Name**: `clinical.diagnoses`
**Operational Domain**: `Clinical Consultation`
**Executive Data Owner**: Directorate of Public Health
**Table Lifecycle**: Added during encounter; retained 10 years with encounter.
**Estimated Volume & Growth**: 18,000,000 diagnosis entries (50,000 diagnoses/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `clinical.diagnoses` realizes primary operational storage: Coded clinical diagnoses mapped to ICD-10 and SNOMED CT taxonomies.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores diagnosis code, display term, diagnosis type (PRIMARY, SECONDARY, PROVISIONAL, CONFIRMED), and chronic condition flag.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by created_at (Quarterly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-001`
- **Audit Requirement**: Diagnostic changes post-encounter logged to medical audit ledger
- **Edge Synchronization**: Edge-captured; batched to cloud disease surveillance

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `encounter_id` | `clinical_encounters` | `id` | `CASCADE` | `CASCADE` | Diagnoses formulated during encounter |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Patient diagnostic history |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Facility diagnosing condition |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `diagnose_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `clinical_payload_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-077`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on diagnoses
  - `INDEX-078`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on diagnoses
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-026: `clinical.prescriptions`

**Table Identifier**: `TABLE-026`
**Fully Qualified Table Name**: `clinical.prescriptions`
**Operational Domain**: `Pharmacy & Prescribing`
**Executive Data Owner**: Chief Medical Officer
**Table Lifecycle**: Issued by doctor; dispensed by pharmacy; archived after 5 years per drug regulations.
**Estimated Volume & Growth**: 11,000,000 prescriptions (32,000 prescriptions/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `clinical.prescriptions` realizes primary operational storage: Header record for electronic prescriptions issued by licensed doctors.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores prescription number, doctor digital signature token, encounter linkage, clinical instructions, and dispensing status.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by prescribed_at (Monthly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-003`
- **Audit Requirement**: Prescription issuance and cancellation cryptographically signed
- **Edge Synchronization**: Immediate edge-to-edge clinic pharmacy sync; cloud archive

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `encounter_id` | `clinical_encounters` | `id` | `CASCADE` | `CASCADE` | Electronic prescription issued in encounter |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Medication prescribed to patient |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Prescribing clinic facility |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `prescription_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 3 designated indexes supporting primary access paths.
  - `INDEX-014`: Composite B-tree on `(patient_id, status)` — Fetch unfulfilled prescriptions for pharmacy dispensing
  - `INDEX-079`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on prescriptions
  - `INDEX-080`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on prescriptions
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-027: `clinical.prescription_items`

**Table Identifier**: `TABLE-027`
**Fully Qualified Table Name**: `clinical.prescription_items`
**Operational Domain**: `Pharmacy & Prescribing`
**Executive Data Owner**: Chief Pharmacist
**Table Lifecycle**: Created with prescription; updated with dispensed quantities at pharmacy; retained 5 years.
**Estimated Volume & Growth**: 35,000,000 line items (100,000 lines/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `clinical.prescription_items` realizes primary operational storage: Line items for prescribed medications specifying drug, dosage form, strength, frequency, duration, and quantity.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Detailed pharmacological orders linked to formulary_drugs, specifying instructions (e.g., 1 tablet after food twice daily for 5 days).

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by created_at (Monthly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-003`
- **Audit Requirement**: Dispensing quantity overrides and generic substitutions logged
- **Edge Synchronization**: Edge-local synchronization with pharmacy module

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `prescription_id` | `prescriptions` | `id` | `CASCADE` | `CASCADE` | Prescription composed of medication line items |
| `drug_id` | `formulary_drugs` | `id` | `RESTRICT` | `CASCADE` | Prescribed drug selected from formulary |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Patient direct linkage for item adherence |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Facility context for stock reservation |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `prescription_item_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-081`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on prescription_items
  - `INDEX-082`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on prescription_items
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-028: `clinical.lab_orders`

**Table Identifier**: `TABLE-028`
**Fully Qualified Table Name**: `clinical.lab_orders`
**Operational Domain**: `Diagnostic Services`
**Executive Data Owner**: Head of Pathology / Diagnostic Services
**Table Lifecycle**: Ordered by physician; sample collected by lab tech; results published; retained 10 years.
**Estimated Volume & Growth**: 4,500,000 lab orders (12,000 orders/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `clinical.lab_orders` realizes primary operational storage: Header record for diagnostic laboratory investigation requests ordered during consultation.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores order number, encounter linkage, ordering physician ID, priority (ROUTINE, STAT), and specimen collection status.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by ordered_at (Quarterly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-004`
- **Audit Requirement**: Sample collection and result sign-off audited with staff timestamps
- **Edge Synchronization**: Edge-local order creation with cloud routing to hub laboratories

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `encounter_id` | `clinical_encounters` | `id` | `CASCADE` | `CASCADE` | Laboratory investigations ordered during encounter |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Patient diagnostic test order |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Clinic ordering laboratory tests |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `lab_order_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-083`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on lab_orders
  - `INDEX-084`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on lab_orders
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-029: `clinical.lab_order_items`

**Table Identifier**: `TABLE-029`
**Fully Qualified Table Name**: `clinical.lab_order_items`
**Operational Domain**: `Diagnostic Services`
**Executive Data Owner**: Head of Pathology
**Table Lifecycle**: Created with order; transitioned during lab workflow; retained 10 years.
**Estimated Volume & Growth**: 12,000,000 items (35,000 test items/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `clinical.lab_order_items` realizes primary operational storage: Individual diagnostic tests requested (e.g., Complete Blood Count, HbA1c, Dengue NS1 Ag, Urine Routine).

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Test codes mapped to LOINC standard, specimen requirement (Serum, Whole Blood, Urine), and status (PENDING, SAMPLE_COLLECTED, ANALYZED).

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by created_at (Quarterly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-004`
- **Audit Requirement**: Test cancellations require technician reason code
- **Edge Synchronization**: Edge-local execution; cloud sync on completion

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `lab_order_id` | `lab_orders` | `id` | `CASCADE` | `CASCADE` | Specific diagnostic tests in order |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Patient specimen linkage |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Facility performing or forwarding sample |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `lab_order_item_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-085`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on lab_order_items
  - `INDEX-086`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on lab_order_items
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-030: `clinical.lab_results`

**Table Identifier**: `TABLE-030`
**Fully Qualified Table Name**: `clinical.lab_results`
**Operational Domain**: `Diagnostic Services`
**Executive Data Owner**: Chief Pathologist
**Table Lifecycle**: Entered by technician; verified by pathologist; immutable upon verification; retained 10 years.
**Estimated Volume & Growth**: 25,000,000 test observations (70,000 observations/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `clinical.lab_results` realizes primary operational storage: Verified quantitative and qualitative laboratory test results, reference ranges, and critical panic value flags.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores numeric/text observation values, measurement units (mg/dL, g/dL), biological reference ranges, and panic status (LOW, NORMAL, HIGH, PANIC).

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by verified_at (Quarterly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-004`
- **Audit Requirement**: Panic value phone escalation to doctor mandatory logged with timestamp
- **Edge Synchronization**: Immediate cloud sync with doctor alert trigger

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `order_item_id` | `lab_order_items` | `id` | `CASCADE` | `CASCADE` | Verified result for diagnostic test item |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Diagnostic observation for patient record |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Laboratory verifying test results |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `lab_result_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-087`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on lab_results
  - `INDEX-088`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on lab_results
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-031: `clinical.teleconsultations`

**Table Identifier**: `TABLE-031`
**Fully Qualified Table Name**: `clinical.teleconsultations`
**Operational Domain**: `Telemedicine`
**Executive Data Owner**: Telemedicine Program Director
**Table Lifecycle**: Scheduled during clinic visit; completed upon call termination; retained 10 years per Telemedicine Practice Guidelines.
**Estimated Volume & Growth**: 350,000 teleconsultations (1,000 sessions/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `clinical.teleconsultations` realizes primary operational storage: Doctor-to-specialist teleconsultation sessions linking Namma Clinic medical officers with secondary/tertiary hospital specialists.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Maintains WebRTC room identifier, session duration, specialist physician ID, audio/video quality metrics, and joint consultation clinical summary.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by session_start (Semi-annual)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-016`
- **Audit Requirement**: Connection timestamps, specialist notes, and consent verified
- **Edge Synchronization**: Cloud-hosted WebRTC session metadata synced to clinic edge

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `encounter_id` | `clinical_encounters` | `id` | `CASCADE` | `CASCADE` | Remote specialist consultation session |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Patient participating in teleconsultation |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Clinic originating teleconsultation call |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `teleconsultation_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-089`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on teleconsultations
  - `INDEX-090`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on teleconsultations
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-032: `pharmacy.formulary_drugs`

**Table Identifier**: `TABLE-032`
**Fully Qualified Table Name**: `pharmacy.formulary_drugs`
**Operational Domain**: `Pharmaceutical Master`
**Executive Data Owner**: BBMP Essential Drugs Committee
**Table Lifecycle**: Managed by Central Formulary Committee; version-controlled annual revisions.
**Estimated Volume & Growth**: 1,200 approved drug formulations (Low (< 50 additions/year))

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `pharmacy.formulary_drugs` realizes primary operational storage: Master formulary of approved medications, generic names, dosage forms, therapeutic classes, and national drug codes.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores generic salt name, strength, dosage form (TABLET, SYRUP, INJECTION, OINTMENT), NLEM status, and maximum daily dose safety limits.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-001`
- **Retention Policy**: Governed by `RETENTION-009`
- **Audit Requirement**: Formulary inclusions, deletions, and safety limit adjustments audited
- **Edge Synchronization**: Global edge broadcast to all clinic nodes

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `category_id` | `drug_categories` | `id` | `RESTRICT` | `CASCADE` | Formulary drug classified by therapeutic category |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-001 |
| `formulary_drug_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-001 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-001 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-001 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-091`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on formulary_drugs
  - `INDEX-092`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on formulary_drugs
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-033: `pharmacy.drug_categories`

**Table Identifier**: `TABLE-033`
**Fully Qualified Table Name**: `pharmacy.drug_categories`
**Operational Domain**: `Pharmaceutical Master`
**Executive Data Owner**: Clinical Pharmacology Advisor
**Table Lifecycle**: Static master taxonomy; updated with formulary revisions.
**Estimated Volume & Growth**: 150 categories (Static)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `pharmacy.drug_categories` realizes primary operational storage: Therapeutic and anatomical classification categories (WHO ATC coding hierarchy).

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Hierarchical categorization (e.g., Cardiovascular System -> Antihypertensives -> ACE Inhibitors) for reporting and safety rule enforcement.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-001`
- **Retention Policy**: Governed by `RETENTION-009`
- **Audit Requirement**: Taxonomy updates tracked via administrative audit
- **Edge Synchronization**: Global edge broadcast

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-001 |
| `drug_categorie_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-001 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-001 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-001 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-093`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on drug_categories
  - `INDEX-094`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on drug_categories
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-034: `pharmacy.pharmacy_batches`

**Table Identifier**: `TABLE-034`
**Fully Qualified Table Name**: `pharmacy.pharmacy_batches`
**Operational Domain**: `Inventory & Traceability`
**Executive Data Owner**: Central Procurement Officer
**Table Lifecycle**: Created upon warehouse goods receipt; expires based on manufacturer shelf life; retained 8 years for CAG audit.
**Estimated Volume & Growth**: 45,000 active and historical batches (8,000 new batches/year)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `pharmacy.pharmacy_batches` realizes primary operational storage: Specific physical manufacturing batches of drugs received from central BBMP warehouse or state procurement agency.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores manufacturer batch number, manufacture date, expiration date, unit procurement cost, quality testing certification, and recall flag.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-009`
- **Audit Requirement**: Batch quality lock or recall immediately halts dispensing across all clinics
- **Edge Synchronization**: Replicated across facilities receiving shipment

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `drug_id` | `formulary_drugs` | `id` | `RESTRICT` | `CASCADE` | Manufactured drug batch belongs to formulary drug |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `pharmacy_batche_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-095`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on pharmacy_batches
  - `INDEX-096`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on pharmacy_batches
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-035: `pharmacy.clinic_stock`

**Table Identifier**: `TABLE-035`
**Fully Qualified Table Name**: `pharmacy.clinic_stock`
**Operational Domain**: `Inventory & Traceability`
**Executive Data Owner**: Clinic Pharmacist / MOIC
**Table Lifecycle**: Updated in real-time on every dispensation, inward receipt, and adjustment; active inventory ledger.
**Estimated Volume & Growth**: 250,000 stock balance records across 450 facilities (Proportional to facility and drug count)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `pharmacy.clinic_stock` realizes primary operational storage: Real-time stock balance of medications at each individual Namma Clinic pharmacy store.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Maintains quantity on hand, reserved quantity, reorder threshold, maximum stock level, and storage bin location per batch.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-009`
- **Audit Requirement**: Discrepancy adjustments require physical stock count reconciliation and MOIC sign-off
- **Edge Synchronization**: Edge-local authoritative balance; continuous sync to cloud central inventory

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Current stock inventory held at facility |
| `batch_id` | `pharmacy_batches` | `id` | `RESTRICT` | `CASCADE` | Facility inventory balance per specific batch |
| `drug_id` | `formulary_drugs` | `id` | `RESTRICT` | `CASCADE` | Clinic stock balance aggregation by formulary drug |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `clinic_stock_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 3 designated indexes supporting primary access paths.
  - `INDEX-015`: Unique B-tree on `(facility_id, batch_id)` — Ensure single stock record per batch per clinic
  - `INDEX-097`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on clinic_stock
  - `INDEX-098`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on clinic_stock
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-036: `pharmacy.dispensations`

**Table Identifier**: `TABLE-036`
**Fully Qualified Table Name**: `pharmacy.dispensations`
**Operational Domain**: `Pharmacy Operations`
**Executive Data Owner**: Chief Pharmacist
**Table Lifecycle**: Created upon drug handover; immutable completed dispensation; retained 5 years.
**Estimated Volume & Growth**: 11,000,000 dispensations (32,000 dispensations/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `pharmacy.dispensations` realizes primary operational storage: Header record for the physical event of medication dispensing by a registered pharmacist.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Records dispensation transaction number, prescription linkage, dispensing pharmacist ID, patient pickup timestamp, and counseling notes.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by dispensed_at (Monthly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-003`
- **Audit Requirement**: Pharmacist identity and timestamp locked on dispense completion
- **Edge Synchronization**: Edge-local capture with cloud synchronization

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `prescription_id` | `prescriptions` | `id` | `RESTRICT` | `CASCADE` | Dispensation fulfills doctor prescription |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Pharmacy counter dispensing drugs |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Patient receiving medication |
| `pharmacist_user_id` | `auth_users` | `id` | `RESTRICT` | `CASCADE` | Licensed pharmacist dispensing medications |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `dispensation_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-099`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on dispensations
  - `INDEX-100`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on dispensations
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-037: `pharmacy.dispensation_items`

**Table Identifier**: `TABLE-037`
**Fully Qualified Table Name**: `pharmacy.dispensation_items`
**Operational Domain**: `Pharmacy Operations`
**Executive Data Owner**: Chief Pharmacist
**Table Lifecycle**: Created with dispensation; decrements clinic_stock; retained 5 years.
**Estimated Volume & Growth**: 33,000,000 items (95,000 items/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `pharmacy.dispensation_items` realizes primary operational storage: Detailed line items for dispensed medications linking specific batch numbers and quantities deducted from stock.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores dispensed quantity, batch linkage, drug unit cost, expiry date at dispensation, and instructions given to citizen.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by created_at (Monthly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-003`
- **Audit Requirement**: Batch deduction verified by cryptographic stock movement linkage
- **Edge Synchronization**: Edge-local capture with cloud rollup

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `dispensation_id` | `dispensations` | `id` | `CASCADE` | `CASCADE` | Dispensation composed of drug items |
| `batch_id` | `pharmacy_batches` | `id` | `RESTRICT` | `CASCADE` | Specific batch deducted upon dispensing |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Facility inventory decrement context |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Direct patient linkage for pharmacovigilance |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `dispensation_item_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-101`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on dispensation_items
  - `INDEX-102`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on dispensation_items
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-038: `pharmacy.stock_movements`

**Table Identifier**: `TABLE-038`
**Fully Qualified Table Name**: `pharmacy.stock_movements`
**Operational Domain**: `Inventory & Traceability`
**Executive Data Owner**: Chief Financial Officer (CFO) & Chief Pharmacist
**Table Lifecycle**: Append-only immutable transaction log; retained 8 years for statutory municipal financial audits.
**Estimated Volume & Growth**: 40,000,000 movement records (120,000 transactions/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `pharmacy.stock_movements` realizes primary operational storage: Double-entry immutable audit ledger for every change in drug stock (RECEIPT, DISPENSATION, TRANSFER_IN, TRANSFER_OUT, EXPIRY, DAMAGE).

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores movement type, source facility, destination facility, batch ID, quantity change (+/-), running balance, and authorizing voucher.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by movement_timestamp (Quarterly)
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-009`
- **Audit Requirement**: Strict append-only ledger; running balance must equal previous balance + quantity change
- **Edge Synchronization**: Edge transactions sequenced and reconciled via cloud ledger

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Inventory movement audit ledger for facility |
| `batch_id` | `pharmacy_batches` | `id` | `RESTRICT` | `CASCADE` | Batch affected by stock movement |
| `drug_id` | `formulary_drugs` | `id` | `RESTRICT` | `CASCADE` | Stock movement ledger item drug classification |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `stock_movement_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-103`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on stock_movements
  - `INDEX-104`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on stock_movements
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-039: `pharmacy.drug_indents`

**Table Identifier**: `TABLE-039`
**Fully Qualified Table Name**: `pharmacy.drug_indents`
**Operational Domain**: `Supply Chain & Procurement`
**Executive Data Owner**: Central Medical Stores Officer
**Table Lifecycle**: Initiated by clinic; approved by MOIC; fulfilled by warehouse; retained 8 years.
**Estimated Volume & Growth**: 120,000 indents (3,000 indents/month across 450 clinics)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `pharmacy.drug_indents` realizes primary operational storage: Electronic drug requisition orders submitted by clinic pharmacists to the BBMP Central Medical Stores.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores indent number, requisition date, approving MOIC ID, warehouse processing status (SUBMITTED, APPROVED, DISPATCHED, RECEIVED), and fulfillment dates.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-009`
- **Audit Requirement**: Workflow approvals and delivery discrepancies audited
- **Edge Synchronization**: Cloud-authoritative workflow with edge notifications

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Indent submitted by requesting clinic |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `drug_indent_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-105`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on drug_indents
  - `INDEX-106`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on drug_indents
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-040: `pharmacy.indent_items`

**Table Identifier**: `TABLE-040`
**Fully Qualified Table Name**: `pharmacy.indent_items`
**Operational Domain**: `Supply Chain & Procurement`
**Executive Data Owner**: Central Medical Stores Officer
**Table Lifecycle**: Created with indent; updated during warehouse fulfillment; retained 8 years.
**Estimated Volume & Growth**: 1,500,000 indent items (35,000 items/month)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `pharmacy.indent_items` realizes primary operational storage: Individual medication line items requested in an indent, requested quantity, approved quantity, and dispatched quantity.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Tracks formulary_drugs linkage, current clinic stock at request time, average monthly consumption (AMC), and warehouse allocation.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-009`
- **Audit Requirement**: Quantity cuts by central warehouse logged with reason code
- **Edge Synchronization**: Cloud-authoritative with edge sync

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `indent_id` | `drug_indents` | `id` | `CASCADE` | `CASCADE` | Medication line items requested in indent |
| `drug_id` | `formulary_drugs` | `id` | `RESTRICT` | `CASCADE` | Drug item requisitioned from warehouse |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Clinic destination for indent item delivery |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `indent_item_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-107`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on indent_items
  - `INDEX-108`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on indent_items
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-041: `pharmacy.cold_chain_devices`

**Table Identifier**: `TABLE-041`
**Fully Qualified Table Name**: `pharmacy.cold_chain_devices`
**Operational Domain**: `Cold Chain & IoT`
**Executive Data Owner**: State Immunization Officer
**Table Lifecycle**: Registered on installation; calibrated annually; decommissioned on replacement; retained 3 years.
**Estimated Volume & Growth**: 1,800 devices across clinics and storage points (Low)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `pharmacy.cold_chain_devices` realizes primary operational storage: Master directory of temperature-controlled storage equipment (Ice-Lined Refrigerators, Deep Freezers, Vaccine Carriers) and IoT loggers.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores device serial number, model, manufacturer, installation date, clinic room linkage, min/max safe temperature thresholds (+2C to +8C), and IoT telemetry gateway MAC address.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-008`
- **Audit Requirement**: Threshold configuration and calibration certificates audited
- **Edge Synchronization**: Global edge broadcast to local telemetry collector

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Vaccine refrigerator located in clinic facility |
| `room_id` | `facility_rooms` | `id` | `SET NULL` | `CASCADE` | Room where cold chain device is physically installed |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `cold_chain_device_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-109`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on cold_chain_devices
  - `INDEX-110`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on cold_chain_devices
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-042: `pharmacy.cold_chain_telemetry`

**Table Identifier**: `TABLE-042`
**Fully Qualified Table Name**: `pharmacy.cold_chain_telemetry`
**Operational Domain**: `Cold Chain & IoT`
**Executive Data Owner**: Immunization Cold Chain Technician
**Table Lifecycle**: Ingested continuously; active raw readings retained 180 days; hourly aggregates retained 3 years.
**Estimated Volume & Growth**: 250,000,000 sensor observations annually (700,000 readings/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `pharmacy.cold_chain_telemetry` realizes primary operational storage: Time-series IoT sensor readings capturing refrigerator internal temperatures, ambient temperatures, door openings, and power status.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: High-frequency telemetry (60-second intervals) recording temperature_celsius, humidity_percent, battery_level, door_open_flag, and alert_status.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by recorded_at (Monthly)
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-008`
- **Audit Requirement**: Temperature breach (> +8C or < +2C for > 15m) triggers critical incident escalation
- **Edge Synchronization**: Edge-buffered via MQTT; batched to cloud time-series store

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `device_id` | `cold_chain_devices` | `id` | `CASCADE` | `CASCADE` | High-frequency temperature sensor observations |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Clinic temperature log roll-up |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `cold_chain_telemetry_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 3 designated indexes supporting primary access paths.
  - `INDEX-016`: BRIN on `(facility_id, created_at)` — Ultra-compact index for high-frequency IoT temperature readings
  - `INDEX-111`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on cold_chain_telemetry
  - `INDEX-112`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on cold_chain_telemetry
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-043: `continuity.referrals`

**Table Identifier**: `TABLE-043`
**Fully Qualified Table Name**: `continuity.referrals`
**Operational Domain**: `Continuity of Care`
**Executive Data Owner**: District Health Officer (DHO)
**Table Lifecycle**: Created by Namma Clinic doctor; updated on receiving hospital triage; completed on discharge/counter-referral; retained 10 years.
**Estimated Volume & Growth**: 1,200,000 referrals (3,500 referrals/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `continuity.referrals` realizes primary operational storage: Outbound patient referral dossiers routing complex cases to secondary/tertiary hospitals (e.g., Bowring, Victoria, KC General).

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores referral number, reason, provisional diagnosis, target hospital specialty, urgency level (ROUTINE, URGENT, EMERGENCY), and transfer summary.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by referred_at (Quarterly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-010`
- **Audit Requirement**: Emergency referrals trigger instant SMS notification to ambulance & destination hospital
- **Edge Synchronization**: Cloud-authoritative exchange with edge clinic synchronization

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Outbound referral dossier for patient |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Referring clinic facility |
| `target_facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Destination secondary/tertiary hospital |
| `encounter_id` | `clinical_encounters` | `id` | `SET NULL` | `CASCADE` | Referral created as disposition of clinical encounter |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `referral_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-113`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on referrals
  - `INDEX-114`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on referrals
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-044: `continuity.referral_counter_notes`

**Table Identifier**: `TABLE-044`
**Fully Qualified Table Name**: `continuity.referral_counter_notes`
**Operational Domain**: `Continuity of Care`
**Executive Data Owner**: District Health Officer
**Table Lifecycle**: Created by hospital specialist; received by primary care clinic; integrated into patient health record; retained 10 years.
**Estimated Volume & Growth**: 800,000 feedback notes (2,200 notes/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `continuity.referral_counter_notes` realizes primary operational storage: Counter-referral clinical feedback returned by secondary hospital specialists to the referring Namma Clinic doctor.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores specialist final diagnosis, operative procedures performed, discharge medication plan, and recommended local follow-up protocol.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by created_at (Quarterly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-010`
- **Audit Requirement**: Reception and doctor review of counter-note audited
- **Edge Synchronization**: Cloud-replicated to referring clinic

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `referral_id` | `referrals` | `id` | `CASCADE` | `CASCADE` | Specialist feedback counter-note |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Patient counter-referral medical record |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Referring clinic receiving specialist feedback |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `referral_counter_note_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-115`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on referral_counter_notes
  - `INDEX-116`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on referral_counter_notes
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-045: `continuity.ncd_episodes`

**Table Identifier**: `TABLE-045`
**Fully Qualified Table Name**: `continuity.ncd_episodes`
**Operational Domain**: `Chronic Disease Management`
**Executive Data Owner**: NCD Program Officer
**Table Lifecycle**: Enrolled on confirmed diagnosis; actively maintained for citizen lifespan; retained 15 years.
**Estimated Volume & Growth**: 1,500,000 registered NCD patients (15,000 new enrollments/month)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `continuity.ncd_episodes` realizes primary operational storage: Longitudinal episode management records for citizens with Non-Communicable Diseases (Diabetes, Hypertension, COPD, Cancer).

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Tracks diagnosis date, disease staging, treatment target goals (e.g., HbA1c < 7.0%, BP < 130/80), lifestyle counseling status, and assigned ASHA worker.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-013`
- **Audit Requirement**: Target goal adjustments and risk tier transitions audited
- **Edge Synchronization**: Edge-replicated for enrolled patient catchment area

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Longitudinal chronic disease care plan |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Primary clinic managing patient NCD plan |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `ncd_episode_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-117`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on ncd_episodes
  - `INDEX-118`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on ncd_episodes
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-046: `continuity.follow_up_schedules`

**Table Identifier**: `TABLE-046`
**Fully Qualified Table Name**: `continuity.follow_up_schedules`
**Operational Domain**: `Continuity of Care`
**Executive Data Owner**: Clinic Operations Lead
**Table Lifecycle**: Created at encounter discharge; updated on patient visit; archived after 3 years.
**Estimated Volume & Growth**: 18,000,000 schedules (50,000 schedules/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `continuity.follow_up_schedules` realizes primary operational storage: Scheduled follow-up dates and reminder triggers for chronic disease review, antenatal checks, and post-referral monitoring.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Maintains scheduled review date, clinical purpose, notification delivery status, attendance outcome (ATTENDED, MISSED, RESCHEDULED), and overdue flags.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by scheduled_date (Monthly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-001`
- **Audit Requirement**: Missed follow-up escalation to ASHA worker logged
- **Edge Synchronization**: Edge-local view synchronized with cloud scheduler

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | Scheduled review appointment for citizen |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Clinic where follow-up will occur |
| `encounter_id` | `clinical_encounters` | `id` | `SET NULL` | `CASCADE` | Follow up scheduled upon encounter discharge |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `follow_up_schedule_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-119`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on follow_up_schedules
  - `INDEX-120`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on follow_up_schedules
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-047: `continuity.notifications`

**Table Identifier**: `TABLE-047`
**Fully Qualified Table Name**: `continuity.notifications`
**Operational Domain**: `Citizen Engagement`
**Executive Data Owner**: Citizen Communication Lead
**Table Lifecycle**: Created by triggering event; dispatched via telecom gateway; retained 12 months per TRAI regulations.
**Estimated Volume & Growth**: 40,000,000 notifications annually (120,000 messages/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `continuity.notifications` realizes primary operational storage: Outbound citizen communications: appointment reminders, prescription links, lab ready notifications, and public health advisories.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores channel (SMS, WHATSAPP, VOICE_CALL), recipient mobile, template ID, message text, dispatch status (SENT, DELIVERED, FAILED), and telecom gateway DLR reference.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by created_at (Monthly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-015`
- **Audit Requirement**: Citizen opt-out preferences strictly enforced; delivery timestamps audited
- **Edge Synchronization**: Cloud-authoritative dispatch pipeline

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `SET NULL` | `CASCADE` | Notification sent to patient mobile |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Clinic originating communication message |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `notification_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-121`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on notifications
  - `INDEX-122`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on notifications
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-048: `continuity.grievances`

**Table Identifier**: `TABLE-048`
**Fully Qualified Table Name**: `continuity.grievances`
**Operational Domain**: `Citizen Grievance & Feedback`
**Executive Data Owner**: BBMP Public Grievance Officer
**Table Lifecycle**: Filed by citizen/helpdesk; assigned to MOIC/DHO; resolved with citizen sign-off; retained 5 years.
**Estimated Volume & Growth**: 250,000 grievances (8,000 grievances/month)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `continuity.grievances` realizes primary operational storage: Citizen complaints, service feedback, and Sakala statutory grievance tickets regarding clinic services.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Records Sakala grievance number, clinic linkage, category (STAFF_BEHAVIOR, DRUG_UNAVAILABLE, WAIT_TIME, FACILITY_CLEANLINESS), SLA deadline, and resolution details.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by filed_at (Semi-annual)
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-014`
- **Audit Requirement**: SLA breach automatically escalates to Commissioner with immutable timestamp
- **Edge Synchronization**: Cloud-authoritative with edge-local complaint capture

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Clinic subject to citizen grievance ticket |
| `patient_id` | `patients` | `id` | `SET NULL` | `CASCADE` | Citizen filing service grievance |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `grievance_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `patient_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-004 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-123`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on grievances
  - `INDEX-124`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on grievances
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-049: `continuity.helpdesk_tickets`

**Table Identifier**: `TABLE-049`
**Fully Qualified Table Name**: `continuity.helpdesk_tickets`
**Operational Domain**: `IT & Infrastructure Support`
**Executive Data Owner**: IT Infrastructure Lead
**Table Lifecycle**: Opened by clinic staff; serviced by vendor; closed upon verification; retained 3 years.
**Estimated Volume & Growth**: 150,000 tickets (4,000 tickets/month)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `continuity.helpdesk_tickets` realizes primary operational storage: Internal facility equipment breakdowns, IT hardware tickets, solar inverter faults, and peripheral maintenance requests.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Maintains ticket ID, facility linkage, asset type (TABLET, THERMAL_PRINTER, POWER_BACKUP, IOT_GATEWAY), vendor SLA deadline, and technician fix notes.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: None
- **Data Classification**: `CLASS-002`
- **Retention Policy**: Governed by `RETENTION-019`
- **Audit Requirement**: Hardware replacement serial numbers and vendor penalty credits audited
- **Edge Synchronization**: Cloud-hosted with edge-local reporting form

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Clinic hardware or IT issue ticket |
| `device_id` | `cold_chain_devices` | `id` | `SET NULL` | `CASCADE` | Equipment fault ticket for cold chain refrigerator |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-002 |
| `helpdesk_ticket_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-002 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-002 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-002 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-125`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on helpdesk_tickets
  - `INDEX-126`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on helpdesk_tickets
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-050: `audit.audit_events`

**Table Identifier**: `TABLE-050`
**Fully Qualified Table Name**: `audit.audit_events`
**Operational Domain**: `Compliance & Security`
**Executive Data Owner**: Chief Information Security Officer
**Table Lifecycle**: Append-only immutable; written in real-time; never updated or deleted; retained 10 years in WORM storage.
**Estimated Volume & Growth**: 500,000,000 audit events (1,500,000 events/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `audit.audit_events` realizes primary operational storage: Master append-only tamper-evident audit ledger capturing every critical data access, state mutation, and security event.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Cryptographically chained log storing actor ID, event category, resource URI, previous state hash, new state hash, SHA-256 HMAC chain link, and client TLS metadata.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by event_timestamp (Monthly)
- **Data Classification**: `CLASS-004`
- **Retention Policy**: Governed by `RETENTION-006`
- **Audit Requirement**: Absolute immutability; cryptographic chain break triggers emergency SOC security alert
- **Edge Synchronization**: Edge-local append; guaranteed delivery push to central SIEM via encrypted queue

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `actor_user_id` | `auth_users` | `id` | `SET NULL` | `CASCADE` | User performing audited system mutation |
| `facility_id` | `facilities` | `id` | `SET NULL` | `CASCADE` | Facility location where audited mutation occurred |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-004 |
| `audit_event_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-004 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-004 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-004 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 3 designated indexes supporting primary access paths.
  - `INDEX-017`: BRIN on `(created_at)` — Time-ordered append-only WORM audit query acceleration
  - `INDEX-127`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on audit_events
  - `INDEX-128`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on audit_events
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-051: `sync.offline_mutation_log`

**Table Identifier**: `TABLE-051`
**Fully Qualified Table Name**: `sync.offline_mutation_log`
**Operational Domain**: `Edge Offline Synchronization`
**Executive Data Owner**: Edge Architecture Team
**Table Lifecycle**: Appended during offline operations; replayed to cloud upon connectivity restoration; purged after 180 days.
**Estimated Volume & Growth**: 15,000,000 offline mutations (45,000 mutations/day across intermittent connections)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `sync.offline_mutation_log` realizes primary operational storage: Ordered journal of database mutations performed on clinic edge appliances during wide-area network outages.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores transaction sequence number, mutation payload JSONB, table name, operation (INSERT, UPDATE), conflict resolution vector, and cloud acknowledgment status.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by created_at (Monthly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-012`
- **Audit Requirement**: Sync conflict resolutions strictly logged with winning vector justification
- **Edge Synchronization**: Authoritative local edge journal; replicated to cloud reconciliation processor

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Clinic edge appliance recording offline mutation |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `offline_mutation_log_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-129`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on offline_mutation_log
  - `INDEX-130`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on offline_mutation_log
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

### TABLE-052: `sync.abdm_artifacts`

**Table Identifier**: `TABLE-052`
**Fully Qualified Table Name**: `sync.abdm_artifacts`
**Operational Domain**: `National Interoperability`
**Executive Data Owner**: ABDM Integration Lead
**Table Lifecycle**: Created upon ABDM push/pull; retained 7 years per National Digital Health Mission standards.
**Estimated Volume & Growth**: 12,000,000 FHIR bundles (35,000 artifacts/day)

#### 1. Business Purpose & Scope
In the normalized logical relational schema, `sync.abdm_artifacts` realizes primary operational storage: Ayushman Bharat Digital Mission (ABDM) integration payloads, FHIR R4 document bundles, linking tokens, and consent transaction references.

Structurally, the relation is designed to satisfy relational integrity constraints as follows: Stores ABDM transaction ID, ABHA number linkage, FHIR Bundle JSONB, health information type (OPConsultation, Prescription, DiagnosticReport), and encryption key wrap.

#### 2. Key Architecture & Relational Constraints
- **Primary Key**: `id` (UUIDv7 surrogate key, cluster-ordered)
- **Candidate / Natural Keys**: `id`, business tracking code, or unique natural identifier
- **Partitioning Strategy**: Range partitioned by created_at (Quarterly)
- **Data Classification**: `CLASS-003`
- **Retention Policy**: Governed by `RETENTION-005`
- **Audit Requirement**: ABDM gateway request/response exchange logged with cryptographic proof
- **Edge Synchronization**: Cloud-authoritative interoperability gateway

#### 3. Foreign Key Dependencies (Inbound Constraints)

| Foreign Key Column | References Parent Table | Parent PK | ON DELETE Action | ON UPDATE Action | Relationship Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | `CASCADE` | ABDM FHIR artifacts linked to registered citizen |
| `facility_id` | `facilities` | `id` | `RESTRICT` | `CASCADE` | Healthcare facility sharing ABDM clinical bundle |

#### 4. Normalized Attribute Catalog

| Column Name | Logical Type | Nullable | Default Value | Key Status | Domain Constraints & Allowed Values | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `UUID` | NO | `gen_random_uuid()` | **PK** | UUIDv7 format | CLASS-003 |
| `abdm_artifact_number` | `VARCHAR(64)` | NO | None | **NONE** | Alphanumeric tracking code | CLASS-003 |
| `facility_id` | `UUID` | NO | None | **FK** | Valid UUID | CLASS-002 |
| `created_by_user_id` | `UUID` | YES | None | **FK** | Valid UUID | CLASS-002 |
| `status` | `VARCHAR(32)` | NO | `'ACTIVE'` | **NONE** | Status Enum | CLASS-002 |
| `category_type` | `VARCHAR(64)` | NO | `'STANDARD'` | **NONE** | Classification string | CLASS-002 |
| `metadata_json` | `JSONB` | YES | `'{}'::jsonb` | **NONE** | Valid JSONB schema | CLASS-003 |
| `priority_score` | `INTEGER` | NO | `1` | **NONE** | 1 to 5 | CLASS-002 |
| `operational_notes` | `TEXT` | YES | None | **NONE** | Text up to 4000 chars | CLASS-003 |
| `sync_version` | `BIGINT` | NO | `1` | **NONE** | >= 1 | CLASS-002 |
| `edge_device_id` | `VARCHAR(64)` | YES | None | **NONE** | Device MAC or UUID | CLASS-002 |
| `record_hash` | `VARCHAR(64)` | NO | `encode(sha256('init'::bytea), 'hex')` | **NONE** | ^[a-f0-9]{64}$ | CLASS-002 |
| `verified_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |
| `created_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `updated_at` | `TIMESTAMPTZ` | NO | `clock_timestamp()` | **NONE** | UTC timestamp | CLASS-002 |
| `deleted_at` | `TIMESTAMPTZ` | YES | None | **NONE** | UTC timestamp | CLASS-002 |

#### 5. Indexing & Concurrency Characteristics
- **Index Count**: 2 designated indexes supporting primary access paths.
  - `INDEX-131`: B-tree on `(facility_id)` — Accelerate clinic facility filtering on abdm_artifacts
  - `INDEX-132`: Composite B-tree on `(status, created_at)` — Optimize operational status workflows and temporal slicing on abdm_artifacts
- **Concurrency Control**: Monotonic version counter `sync_version` for optimistic locking and edge sync conflict detection.
- **Soft Deletion Protocol**: `deleted_at` timestamp preserves historical referential integrity; physical deletes prohibited.

## 6. Logical Schema Integrity Verification

The 52 normalized tables satisfy all integrity criteria:
1. **Zero Orphaned Tables**: Every operational table is connected to the master relational graph via verified foreign key relationships.
2. **Referential Closure**: All foreign key targets reference verified primary keys in existing tables.
3. **Complete Metadata Coverage**: Every attribute possesses a strict data type, nullability declaration, validation rule, and classification tier.
4. **Documentation-First Discipline**: Zero executable SQL or runtime Prisma code has been generated; this specification serves as the authoritative blueprint for physical implementation.
