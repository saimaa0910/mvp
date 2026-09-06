# Phase 07 — Enterprise Table Catalog & Master Entity Registry

> **Document Identifier**: `DB-CATALOG-001`
> **System**: Namma Clinic Digital Health & Operations Platform
> **Municipal Authority**: Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Status**: APPROVED ENTERPRISE CATALOG
> **Catalog Coverage**: 52 Master Relational Tables (`TABLE-001` to `TABLE-052`)
> **Relational Schemas**: `identity`, `intake`, `clinical`, `pharmacy`, `continuity`, `audit`, `sync`
> **Classification Framework**: 5-Tier Data Classification Standard (`CLASS-001` to `CLASS-005`)

---

## 1. Executive Summary & Catalog Scope

This document establishes the master enterprise table catalog for the Namma Clinic platform. It serves as the single authoritative encyclopedia detailing the operational purpose, data ownership, schema boundary, lifecycle states, growth projections, data classifications, foreign key dependencies, indexing models, data quality rules, and end-to-end lineage for all 52 relational tables.

Every table profile is engineered to provide complete operational, architectural, and regulatory clarity to database administrators, backend service developers, data protection officers, and clinical governance auditors. Superficial descriptions are prohibited; each entry provides comprehensive specifications covering both operational steady-state behavior and emergency disaster recovery parameters.

## 2. Master Table Inventory Summary Matrix

The 52 tables are categorized across 6 major functional healthcare domains:

| Table ID | Table Name | Schema | Operational Domain | Primary Key | Partition Strategy | Classification | Retention Policy | Estimated Annual Volume |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TABLE-001** | `auth_users` | `identity` | Identity & Access | `id` | None (Low volume, high read frequency) | `CLASS-004` | `RETENTION-006` | 5,000 staff accounts across 198 BBMP wards |
| **TABLE-002** | `user_credentials` | `identity` | Identity & Access | `id` | None | `CLASS-005` | `RETENTION-011` | 5,000 records |
| **TABLE-003** | `user_sessions` | `identity` | Identity & Access | `id` | Range partitioned by created_at (Monthly) | `CLASS-003` | `RETENTION-011` | 500,000 annual sessions |
| **TABLE-004** | `roles` | `identity` | Role-Based Access Control | `id` | None | `CLASS-002` | `RETENTION-006` | 30 canonical roles |
| **TABLE-005** | `permissions` | `identity` | Role-Based Access Control | `id` | None | `CLASS-002` | `RETENTION-006` | 180 distinct permissions |
| **TABLE-006** | `role_permissions` | `identity` | Role-Based Access Control | `id` | None | `CLASS-002` | `RETENTION-006` | 900 mapping records |
| **TABLE-007** | `user_roles` | `identity` | Role-Based Access Control | `id` | None | `CLASS-002` | `RETENTION-006` | 8,000 assignments |
| **TABLE-008** | `facilities` | `identity` | Facility Operations | `id` | None | `CLASS-001` | `RETENTION-006` | 450 facilities across Greater Bengaluru |
| **TABLE-009** | `facility_rooms` | `identity` | Facility Operations | `id` | None | `CLASS-002` | `RETENTION-019` | 3,000 rooms/stations across clinics |
| **TABLE-010** | `staff_profiles` | `identity` | Human Resources | `id` | None | `CLASS-004` | `RETENTION-006` | 6,000 staff profiles |
| **TABLE-011** | `staff_shifts` | `identity` | Human Resources | `id` | Range partitioned by shift_date (Quarterly) | `CLASS-002` | `RETENTION-002` | 1,200,000 shift records over 3 years |
| **TABLE-012** | `system_configs` | `identity` | System Configuration | `id` | None | `CLASS-002` | `RETENTION-006` | 1,500 configuration parameters |
| **TABLE-013** | `patients` | `intake` | Citizen Demographics | `id` | Hash partitioned by id (16 partitions) | `CLASS-004` | `RETENTION-001` | 3,500,000 citizens registered across BBMP jurisdiction |
| **TABLE-014** | `patient_identifiers` | `intake` | Citizen Demographics | `id` | Hash partitioned by patient_id (16 partitions) | `CLASS-004` | `RETENTION-005` | 5,000,000 identifier records |
| **TABLE-015** | `patient_contacts` | `intake` | Citizen Demographics | `id` | Hash partitioned by patient_id (16 partitions) | `CLASS-004` | `RETENTION-001` | 4,200,000 records |
| **TABLE-016** | `patient_addresses` | `intake` | Citizen Demographics | `id` | Hash partitioned by patient_id (16 partitions) | `CLASS-004` | `RETENTION-001` | 3,800,000 records |
| **TABLE-017** | `consent_records` | `intake` | Consent Management | `id` | Range partitioned by granted_at (Semi-annual) | `CLASS-004` | `RETENTION-005` | 6,000,000 consent artifacts |
| **TABLE-018** | `tokens` | `intake` | Queue Management | `id` | Range partitioned by issued_at (Monthly) | `CLASS-002` | `RETENTION-007` | 15,000,000 tokens annually across 450 facilities |
| **TABLE-019** | `queue_entries` | `intake` | Queue Management | `id` | Range partitioned by created_at (Monthly) | `CLASS-002` | `RETENTION-007` | 45,000,000 queue transitions annually |
| **TABLE-020** | `triage_assessments` | `intake` | Clinical Triage | `id` | Range partitioned by assessed_at (Quarterly) | `CLASS-003` | `RETENTION-001` | 10,000,000 records |
| **TABLE-021** | `patient_vitals` | `intake` | Clinical Triage | `id` | Range partitioned by recorded_at (Quarterly) | `CLASS-003` | `RETENTION-001` | 25,000,000 vitals snapshots |
| **TABLE-022** | `danger_alerts` | `intake` | Clinical Safety | `id` | Range partitioned by triggered_at (Quarterly) | `CLASS-003` | `RETENTION-001` | 1,500,000 alerts |
| **TABLE-023** | `clinical_encounters` | `clinical` | Clinical Consultation | `id` | Range partitioned by encounter_date (Monthly) | `CLASS-003` | `RETENTION-001` | 12,000,000 consultations |
| **TABLE-024** | `clinical_notes` | `clinical` | Clinical Consultation | `id` | Range partitioned by created_at (Monthly) | `CLASS-005` | `RETENTION-001` | 12,000,000 records |
| **TABLE-025** | `diagnoses` | `clinical` | Clinical Consultation | `id` | Range partitioned by created_at (Quarterly) | `CLASS-003` | `RETENTION-001` | 18,000,000 diagnosis entries |
| **TABLE-026** | `prescriptions` | `clinical` | Pharmacy & Prescribing | `id` | Range partitioned by prescribed_at (Monthly) | `CLASS-003` | `RETENTION-003` | 11,000,000 prescriptions |
| **TABLE-027** | `prescription_items` | `clinical` | Pharmacy & Prescribing | `id` | Range partitioned by created_at (Monthly) | `CLASS-003` | `RETENTION-003` | 35,000,000 line items |
| **TABLE-028** | `lab_orders` | `clinical` | Diagnostic Services | `id` | Range partitioned by ordered_at (Quarterly) | `CLASS-003` | `RETENTION-004` | 4,500,000 lab orders |
| **TABLE-029** | `lab_order_items` | `clinical` | Diagnostic Services | `id` | Range partitioned by created_at (Quarterly) | `CLASS-003` | `RETENTION-004` | 12,000,000 items |
| **TABLE-030** | `lab_results` | `clinical` | Diagnostic Services | `id` | Range partitioned by verified_at (Quarterly) | `CLASS-003` | `RETENTION-004` | 25,000,000 test observations |
| **TABLE-031** | `teleconsultations` | `clinical` | Telemedicine | `id` | Range partitioned by session_start (Semi-annual) | `CLASS-003` | `RETENTION-016` | 350,000 teleconsultations |
| **TABLE-032** | `formulary_drugs` | `pharmacy` | Pharmaceutical Master | `id` | None | `CLASS-001` | `RETENTION-009` | 1,200 approved drug formulations |
| **TABLE-033** | `drug_categories` | `pharmacy` | Pharmaceutical Master | `id` | None | `CLASS-001` | `RETENTION-009` | 150 categories |
| **TABLE-034** | `pharmacy_batches` | `pharmacy` | Inventory & Traceability | `id` | None | `CLASS-002` | `RETENTION-009` | 45,000 active and historical batches |
| **TABLE-035** | `clinic_stock` | `pharmacy` | Inventory & Traceability | `id` | None | `CLASS-002` | `RETENTION-009` | 250,000 stock balance records across 450 facilities |
| **TABLE-036** | `dispensations` | `pharmacy` | Pharmacy Operations | `id` | Range partitioned by dispensed_at (Monthly) | `CLASS-003` | `RETENTION-003` | 11,000,000 dispensations |
| **TABLE-037** | `dispensation_items` | `pharmacy` | Pharmacy Operations | `id` | Range partitioned by created_at (Monthly) | `CLASS-003` | `RETENTION-003` | 33,000,000 items |
| **TABLE-038** | `stock_movements` | `pharmacy` | Inventory & Traceability | `id` | Range partitioned by movement_timestamp (Quarterly) | `CLASS-002` | `RETENTION-009` | 40,000,000 movement records |
| **TABLE-039** | `drug_indents` | `pharmacy` | Supply Chain & Procurement | `id` | None | `CLASS-002` | `RETENTION-009` | 120,000 indents |
| **TABLE-040** | `indent_items` | `pharmacy` | Supply Chain & Procurement | `id` | None | `CLASS-002` | `RETENTION-009` | 1,500,000 indent items |
| **TABLE-041** | `cold_chain_devices` | `pharmacy` | Cold Chain & IoT | `id` | None | `CLASS-002` | `RETENTION-008` | 1,800 devices across clinics and storage points |
| **TABLE-042** | `cold_chain_telemetry` | `pharmacy` | Cold Chain & IoT | `id` | Range partitioned by recorded_at (Monthly) | `CLASS-002` | `RETENTION-008` | 250,000,000 sensor observations annually |
| **TABLE-043** | `referrals` | `continuity` | Continuity of Care | `id` | Range partitioned by referred_at (Quarterly) | `CLASS-003` | `RETENTION-010` | 1,200,000 referrals |
| **TABLE-044** | `referral_counter_notes` | `continuity` | Continuity of Care | `id` | Range partitioned by created_at (Quarterly) | `CLASS-003` | `RETENTION-010` | 800,000 feedback notes |
| **TABLE-045** | `ncd_episodes` | `continuity` | Chronic Disease Management | `id` | None | `CLASS-003` | `RETENTION-013` | 1,500,000 registered NCD patients |
| **TABLE-046** | `follow_up_schedules` | `continuity` | Continuity of Care | `id` | Range partitioned by scheduled_date (Monthly) | `CLASS-003` | `RETENTION-001` | 18,000,000 schedules |
| **TABLE-047** | `notifications` | `continuity` | Citizen Engagement | `id` | Range partitioned by created_at (Monthly) | `CLASS-003` | `RETENTION-015` | 40,000,000 notifications annually |
| **TABLE-048** | `grievances` | `continuity` | Citizen Grievance & Feedback | `id` | Range partitioned by filed_at (Semi-annual) | `CLASS-002` | `RETENTION-014` | 250,000 grievances |
| **TABLE-049** | `helpdesk_tickets` | `continuity` | IT & Infrastructure Support | `id` | None | `CLASS-002` | `RETENTION-019` | 150,000 tickets |
| **TABLE-050** | `audit_events` | `audit` | Compliance & Security | `id` | Range partitioned by event_timestamp (Monthly) | `CLASS-004` | `RETENTION-006` | 500,000,000 audit events |
| **TABLE-051** | `offline_mutation_log` | `sync` | Edge Offline Synchronization | `id` | Range partitioned by created_at (Monthly) | `CLASS-003` | `RETENTION-012` | 15,000,000 offline mutations |
| **TABLE-052** | `abdm_artifacts` | `sync` | National Interoperability | `id` | Range partitioned by created_at (Quarterly) | `CLASS-003` | `RETENTION-005` | 12,000,000 FHIR bundles |

## 3. Comprehensive Table Catalog (TABLE-001 to TABLE-052)

### TABLE-001: `identity.auth_users`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-001`
- **Fully Qualified Name**: `identity.auth_users`
- **Functional Domain**: `Identity & Access`
- **Executive Data Owner**: Chief Information Security Officer (CISO)
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-004` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-006`
- **Audit Requirements**: Full row change capture with IP and actor tracking

#### 2. Business Purpose & Scope Description
**Operational Role**: Master registry of all authenticated healthcare personnel, administrative staff, and system service accounts.

Stores user credentials identity root, email, mobile phone, status (ACTIVE, SUSPENDED, DEACTIVATED), and global audit timestamps.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created during staff onboarding; updated on credential/profile change; soft-deleted/deactivated on offboarding; retained 10 years per audit policy.
- **Estimated Storage Footprint**: Baseline capacity: `5,000 staff accounts across 198 BBMP wards`; Expected growth rate: `15% annual turnover / expansion`.
- **Partitioning Architecture**: `None (Low volume, high read frequency)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `primary_facility_id` | `facilities` | `id` | `RESTRICT` | User base home clinic posting |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `user_credentials` | `user_id` | `1:1` | Every credential record belongs strictly to one authenticated user |
| `user_sessions` | `user_id` | `1:N` | A user can have multiple concurrent active sessions across mobile and desktop |
| `user_roles` | `user_id` | `1:N` | Staff members are assigned roles |
| `staff_profiles` | `user_id` | `1:1` | Clinical staff profile links to authentication user |
| `staff_shifts` | `user_id` | `1:N` | Duty rosters track shifts per staff member |
| `clinical_encounters` | `doctor_user_id` | `1:N` | Treating licensed physician |
| `audit_events` | `actor_user_id` | `1:N` | User performing audited system mutation |
| `dispensations` | `pharmacist_user_id` | `1:N` | Licensed pharmacist dispensing medications |

#### 5. Indexing Architecture & Query Acceleration
The table features 5 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-001` | Unique B-tree | `(email)` | Very High | `SELECT * FROM auth_users WHERE email = $1` |
| `INDEX-002` | Unique B-tree | `(phone_blind_index)` | Very High | `SELECT * FROM auth_users WHERE phone_blind_index = $1` |
| `INDEX-003` | B-tree | `(primary_facility_id)` | High | `SELECT * FROM auth_users WHERE primary_facility_id = $1` |
| `INDEX-029` | B-tree | `(facility_id)` | High | `SELECT * FROM auth_users WHERE facility_id = $1` |
| `INDEX-030` | Composite B-tree | `(created_at)` | High | `SELECT * FROM auth_users WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-001, FR-002, SECR-001, SECR-004`
- **Upstream Workflows**: `WF-001, WF-002`
- **REST / GraphQL APIs**: `Auth Service, Staff Management API, Admin Console`
- **Reporting Dashboards**: `Staff Activity Dashboard, Security Audit Log`
- **Analytical Warehousing**: `Clinician Utilization Model`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Full bidirectional cloud-to-edge synchronization with role-based filtering`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL (RPO <= 5m, RTO <= 15m)`
- **Recovery Priority**: `Tier 1 (Core Identity)`
- **Migration Sensitivity**: `HIGH (Foreign key root for all operational tables)`
- **Governing Data Quality Rules**: `DQ-001, DQ-002`
- **Data Lineage Traceability**: `LINEAGE-001`

### TABLE-002: `identity.user_credentials`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-002`
- **Fully Qualified Name**: `identity.user_credentials`
- **Functional Domain**: `Identity & Access`
- **Executive Data Owner**: Security Engineering Lead
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-005` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-011`
- **Audit Requirements**: Strict security audit; passwords never logged in plaintext

#### 2. Business Purpose & Scope Description
**Operational Role**: Cryptographic authentication secrets including Argon2id password hashes, MFA totp secrets, and failed login counters.

Stores high-security credentials separated from user demographic profile to isolate cryptographic attack surface.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created at user registration; modified on password rotation; purged on user erasure.
- **Estimated Storage Footprint**: Baseline capacity: `5,000 records`; Expected growth rate: `Proportional to auth_users`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | `auth_users` | `id` | `CASCADE` | Every credential record belongs strictly to one authenticated user |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-031` | B-tree | `(facility_id)` | High | `SELECT * FROM user_credentials WHERE facility_id = $1` |
| `INDEX-032` | Composite B-tree | `(created_at)` | High | `SELECT * FROM user_credentials WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `SECR-001, SECR-002, SECR-003`
- **Upstream Workflows**: `WF-001`
- **REST / GraphQL APIs**: `Authentication Gateway`
- **Reporting Dashboards**: `None`
- **Analytical Warehousing**: `None`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Edge-synchronized with salted hash derivation; offline auth enabled via local cache`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `CRITICAL (Secrets require zero-exposure migration)`
- **Governing Data Quality Rules**: `DQ-003, DQ-004`
- **Data Lineage Traceability**: `LINEAGE-001`

### TABLE-003: `identity.user_sessions`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-003`
- **Fully Qualified Name**: `identity.user_sessions`
- **Functional Domain**: `Identity & Access`
- **Executive Data Owner**: Security Operations Center (SOC)
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-011`
- **Audit Requirements**: Revocation and concurrent login violations logged

#### 2. Business Purpose & Scope Description
**Operational Role**: Active and historical web/mobile authentication sessions, JWT refresh tokens, and device fingerprints.

Maintains session state, expiration timestamps, IP address geolocation, and revocation status.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created on login; expired after 15 minutes of inactivity; purged after 1 year.
- **Estimated Storage Footprint**: Baseline capacity: `500,000 annual sessions`; Expected growth rate: `1,500 new sessions per clinic day`.
- **Partitioning Architecture**: `Range partitioned by created_at (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | `auth_users` | `id` | `CASCADE` | A user can have multiple concurrent active sessions across mobile and desktop |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-033` | B-tree | `(facility_id)` | High | `SELECT * FROM user_sessions WHERE facility_id = $1` |
| `INDEX-034` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM user_sessions WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `SECR-004, SECR-005`
- **Upstream Workflows**: `WF-001`
- **REST / GraphQL APIs**: `Session Validation Middleware`
- **Reporting Dashboards**: `Security Compliance Monthly Report`
- **Analytical Warehousing**: `Staff Workload Heatmap`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Edge-local sessions propagated to cloud on connectivity restore`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `STANDARD (RPO <= 1h, RTO <= 4h)`
- **Recovery Priority**: `Tier 3`
- **Migration Sensitivity**: `LOW (Transient operational state)`
- **Governing Data Quality Rules**: `DQ-005`
- **Data Lineage Traceability**: `LINEAGE-002`

### TABLE-004: `identity.roles`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-004`
- **Fully Qualified Name**: `identity.roles`
- **Functional Domain**: `Role-Based Access Control`
- **Executive Data Owner**: BBMP Health Administration
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-006`
- **Audit Requirements**: Administrative changes require double sign-off

#### 2. Business Purpose & Scope Description
**Operational Role**: Master directory of standardized organizational roles (Doctor, Staff Nurse, Pharmacist, Lab Technician, Receptionist, MOIC).

Defines canonical system roles, description, hierarchy level, and default operational permissions.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Static reference data; updated on institutional policy revisions.
- **Estimated Storage Footprint**: Baseline capacity: `30 canonical roles`; Expected growth rate: `Static (< 2 updates/year)`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
*None (Top-level root table in domain hierarchy).*

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `role_permissions` | `role_id` | `1:N` | Roles are composed of granular permission grants |
| `user_roles` | `role_id` | `1:N` | Active roles cannot be deleted if assigned to users |

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-035` | B-tree | `(facility_id)` | High | `SELECT * FROM roles WHERE facility_id = $1` |
| `INDEX-036` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM roles WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-002, SECR-006`
- **Upstream Workflows**: `WF-002`
- **REST / GraphQL APIs**: `Authorization Engine, Admin Portal`
- **Reporting Dashboards**: `Role Distribution Matrix`
- **Analytical Warehousing**: `None`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Global broadcast to all edge clinics`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-006`
- **Data Lineage Traceability**: `LINEAGE-001`

### TABLE-005: `identity.permissions`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-005`
- **Fully Qualified Name**: `identity.permissions`
- **Functional Domain**: `Role-Based Access Control`
- **Executive Data Owner**: System Architecture Team
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-006`
- **Audit Requirements**: Changes tracked via code repository and database schema migration

#### 2. Business Purpose & Scope Description
**Operational Role**: Fine-grained operational capabilities (e.g., prescribe_medication, dispense_drug, order_lab_test).

Atomic system entitlements mapped to resource actions across REST and GraphQL endpoints.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: System immutable code-linked definitions; updated during software releases.
- **Estimated Storage Footprint**: Baseline capacity: `180 distinct permissions`; Expected growth rate: `Increases with new module releases`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
*None (Top-level root table in domain hierarchy).*

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `role_permissions` | `permission_id` | `1:N` | Permissions are mapped to roles via junction table |

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-037` | B-tree | `(facility_id)` | High | `SELECT * FROM permissions WHERE facility_id = $1` |
| `INDEX-038` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM permissions WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `SECR-006, SECR-007`
- **Upstream Workflows**: `WF-002`
- **REST / GraphQL APIs**: `Policy Enforcement Point (PEP)`
- **Reporting Dashboards**: `Access Control List Audit`
- **Analytical Warehousing**: `None`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Global edge broadcast`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-006`
- **Data Lineage Traceability**: `LINEAGE-001`

### TABLE-006: `identity.role_permissions`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-006`
- **Fully Qualified Name**: `identity.role_permissions`
- **Functional Domain**: `Role-Based Access Control`
- **Executive Data Owner**: BBMP Health Administration
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-006`
- **Audit Requirements**: Audit logged on every grant/revoke

#### 2. Business Purpose & Scope Description
**Operational Role**: Many-to-many junction mapping system permissions to roles.

Associates permissions to roles with grant timestamps, active status, and granter user ID.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Modified during role permission matrix updates.
- **Estimated Storage Footprint**: Baseline capacity: `900 mapping records`; Expected growth rate: `Low`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `role_id` | `roles` | `id` | `CASCADE` | Roles are composed of granular permission grants |
| `permission_id` | `permissions` | `id` | `CASCADE` | Permissions are mapped to roles via junction table |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-039` | B-tree | `(facility_id)` | High | `SELECT * FROM role_permissions WHERE facility_id = $1` |
| `INDEX-040` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM role_permissions WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-002, SECR-006`
- **Upstream Workflows**: `WF-002`
- **REST / GraphQL APIs**: `RBAC Enforcement Engine`
- **Reporting Dashboards**: `Role Entitlement Report`
- **Analytical Warehousing**: `None`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Global edge broadcast`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-006`
- **Data Lineage Traceability**: `LINEAGE-001`

### TABLE-007: `identity.user_roles`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-007`
- **Fully Qualified Name**: `identity.user_roles`
- **Functional Domain**: `Role-Based Access Control`
- **Executive Data Owner**: BBMP District Health Officer
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-006`
- **Audit Requirements**: All assignment transfers audited with authorizing government order

#### 2. Business Purpose & Scope Description
**Operational Role**: Assignments of roles to users scoped by specific healthcare facility.

Links users to roles within a facility context, supporting multi-facility roaming doctors.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created upon staff facility posting; revoked on transfer.
- **Estimated Storage Footprint**: Baseline capacity: `8,000 assignments`; Expected growth rate: `20% annual transfer rate`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | `auth_users` | `id` | `CASCADE` | Staff members are assigned roles |
| `role_id` | `roles` | `id` | `RESTRICT` | Active roles cannot be deleted if assigned to users |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Role assignments are facility-scoped |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-041` | B-tree | `(facility_id)` | High | `SELECT * FROM user_roles WHERE facility_id = $1` |
| `INDEX-042` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM user_roles WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-002, SECR-006`
- **Upstream Workflows**: `WF-002`
- **REST / GraphQL APIs**: `Authorization Service`
- **Reporting Dashboards**: `Facility Staffing Register`
- **Analytical Warehousing**: `Staff Allocation Optimization`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Edge-filtered by facility ID`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-006`
- **Data Lineage Traceability**: `LINEAGE-001`

### TABLE-008: `identity.facilities`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-008`
- **Fully Qualified Name**: `identity.facilities`
- **Functional Domain**: `Facility Operations`
- **Executive Data Owner**: BBMP Health Commissioner
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-001` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-006`
- **Audit Requirements**: All status changes and GPS adjustments audited

#### 2. Business Purpose & Scope Description
**Operational Role**: Master directory of Namma Clinics, Urban Primary Health Centres (UPHCs), and referral hospitals.

Stores clinic code, official name, ward number, zone, GPS latitude/longitude, operational hours, and ABDM facility ID (HFR).

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created on clinic commissioning; updated on infrastructure changes; deactivated on decommissioning.
- **Estimated Storage Footprint**: Baseline capacity: `450 facilities across Greater Bengaluru`; Expected growth rate: `5% annual expansion`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
*None (Top-level root table in domain hierarchy).*

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `user_roles` | `facility_id` | `1:N` | Role assignments are facility-scoped |
| `auth_users` | `primary_facility_id` | `1:N` | User base home clinic posting |
| `facility_rooms` | `facility_id` | `1:N` | Chambers and rooms physically exist inside a facility |
| `staff_shifts` | `facility_id` | `1:N` | Staff shifts take place at specific clinic facility |
| `system_configs` | `facility_id` | `1:N` | Clinic-specific operational threshold overrides |
| `patients` | `facility_id` | `1:N` | Patient initial registration clinic |
| `consent_records` | `facility_id` | `1:N` | Facility where consent was executed |
| `tokens` | `facility_id` | `1:N` | Daily token generated at specific clinic |
| `queue_entries` | `facility_id` | `1:N` | Queue progression inside clinic |
| `triage_assessments` | `facility_id` | `1:N` | Facility where triage occurred |
| `patient_vitals` | `facility_id` | `1:N` | Clinic where vitals recorded |
| `danger_alerts` | `facility_id` | `1:N` | Clinic where clinical red flag occurred |
| `clinical_encounters` | `facility_id` | `1:N` | Encounter conducted at clinic |
| `clinical_notes` | `facility_id` | `1:N` | Facility scope of clinical note |
| `diagnoses` | `facility_id` | `1:N` | Facility diagnosing condition |
| `prescriptions` | `facility_id` | `1:N` | Prescribing clinic facility |
| `prescription_items` | `facility_id` | `1:N` | Facility context for stock reservation |
| `lab_orders` | `facility_id` | `1:N` | Clinic ordering laboratory tests |
| `lab_order_items` | `facility_id` | `1:N` | Facility performing or forwarding sample |
| `lab_results` | `facility_id` | `1:N` | Laboratory verifying test results |
| `teleconsultations` | `facility_id` | `1:N` | Clinic originating teleconsultation call |
| `clinic_stock` | `facility_id` | `1:N` | Current stock inventory held at facility |
| `dispensations` | `facility_id` | `1:N` | Pharmacy counter dispensing drugs |
| `dispensation_items` | `facility_id` | `1:N` | Facility inventory decrement context |
| `stock_movements` | `facility_id` | `1:N` | Inventory movement audit ledger for facility |
| `drug_indents` | `facility_id` | `1:N` | Indent submitted by requesting clinic |
| `indent_items` | `facility_id` | `1:N` | Clinic destination for indent item delivery |
| `cold_chain_devices` | `facility_id` | `1:N` | Vaccine refrigerator located in clinic facility |
| `cold_chain_telemetry` | `facility_id` | `1:N` | Clinic temperature log roll-up |
| `referrals` | `facility_id` | `1:N` | Referring clinic facility |
| `referrals` | `target_facility_id` | `1:N` | Destination secondary/tertiary hospital |
| `referral_counter_notes` | `facility_id` | `1:N` | Referring clinic receiving specialist feedback |
| `ncd_episodes` | `facility_id` | `1:N` | Primary clinic managing patient NCD plan |
| `follow_up_schedules` | `facility_id` | `1:N` | Clinic where follow-up will occur |
| `notifications` | `facility_id` | `1:N` | Clinic originating communication message |
| `grievances` | `facility_id` | `1:N` | Clinic subject to citizen grievance ticket |
| `helpdesk_tickets` | `facility_id` | `1:N` | Clinic hardware or IT issue ticket |
| `audit_events` | `facility_id` | `1:N` | Facility location where audited mutation occurred |
| `offline_mutation_log` | `facility_id` | `1:N` | Clinic edge appliance recording offline mutation |
| `abdm_artifacts` | `facility_id` | `1:N` | Healthcare facility sharing ABDM clinical bundle |

#### 5. Indexing Architecture & Query Acceleration
The table features 4 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-018` | Unique B-tree | `(facility_code)` | Very High | `SELECT id FROM facilities WHERE facility_code = $1` |
| `INDEX-019` | Composite B-tree | `(zone_name, ward_number)` | High | `SELECT * FROM facilities WHERE zone_name = $1 AND ward_number = $2` |
| `INDEX-043` | B-tree | `(ward_number)` | High | `SELECT * FROM facilities WHERE ward_number = $1` |
| `INDEX-044` | Composite B-tree | `(created_at)` | High | `SELECT * FROM facilities WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-003, INT-001`
- **Upstream Workflows**: `WF-002`
- **REST / GraphQL APIs**: `Facility Directory API, Public Portal, Citizen Mobile App`
- **Reporting Dashboards**: `Ward-wise Clinic Coverage Map`
- **Analytical Warehousing**: `Geographic Access Inequality Model`
- **AI & Decision Support Models**: `Catchment Area Optimizer`
- **Edge Synchronization**: `Global edge broadcast of master metadata`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-007`
- **Data Lineage Traceability**: `LINEAGE-003`

### TABLE-009: `identity.facility_rooms`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-009`
- **Fully Qualified Name**: `identity.facility_rooms`
- **Functional Domain**: `Facility Operations`
- **Executive Data Owner**: Medical Officer In-Charge (MOIC)
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-019`
- **Audit Requirements**: Room reassignment tracked for token queue audit

#### 2. Business Purpose & Scope Description
**Operational Role**: Internal physical chambers, consultation rooms, triage booths, pharmacy counters, and sample collection points within a clinic.

Represents functional service points used for queue routing, token display displays, and IoT device association.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Configured during clinic setup; adjusted during clinic layout reorganization.
- **Estimated Storage Footprint**: Baseline capacity: `3,000 rooms/stations across clinics`; Expected growth rate: `Low`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `CASCADE` | Chambers and rooms physically exist inside a facility |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `queue_entries` | `room_id` | `1:N` | Physical consultation chamber serving patient |
| `cold_chain_devices` | `room_id` | `1:1` | Room where cold chain device is physically installed |

#### 5. Indexing Architecture & Query Acceleration
The table features 3 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-020` | Composite B-tree | `(facility_id, status)` | High | `SELECT * FROM facility_rooms WHERE facility_id = $1 AND status = 'ACTIVE'` |
| `INDEX-045` | B-tree | `(facility_id)` | High | `SELECT * FROM facility_rooms WHERE facility_id = $1` |
| `INDEX-046` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM facility_rooms WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-004, OR-001`
- **Upstream Workflows**: `WF-003, WF-004`
- **REST / GraphQL APIs**: `Queue Management Engine, Token Display Screen System`
- **Reporting Dashboards**: `Room Utilization Report`
- **Analytical Warehousing**: `Clinic Bottleneck Analyzer`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Edge-local clinic partition`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `MEDIUM`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-007`
- **Data Lineage Traceability**: `LINEAGE-003`

### TABLE-010: `identity.staff_profiles`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-010`
- **Fully Qualified Name**: `identity.staff_profiles`
- **Functional Domain**: `Human Resources`
- **Executive Data Owner**: BBMP Health Administration HR
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-004` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-006`
- **Audit Requirements**: License verification status changes strictly logged

#### 2. Business Purpose & Scope Description
**Operational Role**: Professional credentialing, medical council registration number (KMC/NMC), qualifications, and contact details of clinical staff.

Stores doctor registration numbers, nurse certification IDs, educational degrees, specialization, and official communication channels.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created at hiring; updated on degree completion/promotion; retained 10 years post-resignation.
- **Estimated Storage Footprint**: Baseline capacity: `6,000 staff profiles`; Expected growth rate: `10% annual increase`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | `auth_users` | `id` | `CASCADE` | Clinical staff profile links to authentication user |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 3 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-021` | Unique B-tree | `(user_id)` | Very High | `SELECT * FROM staff_profiles WHERE user_id = $1` |
| `INDEX-047` | B-tree | `(facility_id)` | High | `SELECT * FROM staff_profiles WHERE facility_id = $1` |
| `INDEX-048` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM staff_profiles WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-002, SECR-001`
- **Upstream Workflows**: `WF-002`
- **REST / GraphQL APIs**: `Doctor Prescription Header Generator, Teleconsultation Roster`
- **Reporting Dashboards**: `Clinical Credentialing Compliance Report`
- **Analytical Warehousing**: `Doctor Productivity Index`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Edge-replicated for assigned clinic personnel`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-008`
- **Data Lineage Traceability**: `LINEAGE-001`

### TABLE-011: `identity.staff_shifts`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-011`
- **Fully Qualified Name**: `identity.staff_shifts`
- **Functional Domain**: `Human Resources`
- **Executive Data Owner**: MOIC / Facility Administrator
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-002`
- **Audit Requirements**: Manual attendance overrides require MOIC digital signature

#### 2. Business Purpose & Scope Description
**Operational Role**: Daily work duty rosters, shift allocations (Morning, Afternoon, Evening), and biometric attendance records.

Tracks planned vs actual doctor/nurse shifts, on-call status, leave absences, and biometric punch times.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created weekly/monthly; marked completed at end of shift; archived after 3 years.
- **Estimated Storage Footprint**: Baseline capacity: `1,200,000 shift records over 3 years`; Expected growth rate: `3,000 records/day across all clinics`.
- **Partitioning Architecture**: `Range partitioned by shift_date (Quarterly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | `auth_users` | `id` | `RESTRICT` | Duty rosters track shifts per staff member |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Staff shifts take place at specific clinic facility |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 3 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-022` | Composite B-tree | `(facility_id, status, created_at)` | High | `SELECT * FROM staff_shifts WHERE facility_id = $1 AND status = 'ACTIVE'` |
| `INDEX-049` | B-tree | `(facility_id)` | High | `SELECT * FROM staff_shifts WHERE facility_id = $1` |
| `INDEX-050` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM staff_shifts WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `OR-002, OR-003`
- **Upstream Workflows**: `WF-002`
- **REST / GraphQL APIs**: `Duty Roster Service, Time & Attendance Sync`
- **Reporting Dashboards**: `Staff Absenteeism & Punctuality Dashboard`
- **Analytical Warehousing**: `Workforce Demand Forecast`
- **AI & Decision Support Models**: `Automated Shift Scheduler`
- **Edge Synchronization**: `Edge-local capture with cloud synchronization`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `STANDARD`
- **Recovery Priority**: `Tier 3`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-008`
- **Data Lineage Traceability**: `LINEAGE-002`

### TABLE-012: `identity.system_configs`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-012`
- **Fully Qualified Name**: `identity.system_configs`
- **Functional Domain**: `System Configuration`
- **Executive Data Owner**: Principal DevOps Architect
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-006`
- **Audit Requirements**: Full history of config value transitions with authorizer ID

#### 2. Business Purpose & Scope Description
**Operational Role**: Hierarchical dynamic platform configuration parameters, feature flags, and operational thresholds.

Key-value store scoped by GLOBAL, ZONE, or FACILITY, supporting dynamic threshold adjustments without deployment.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Modified during operational configuration; version controlled with rollback.
- **Estimated Storage Footprint**: Baseline capacity: `1,500 configuration parameters`; Expected growth rate: `Low`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `CASCADE` | Clinic-specific operational threshold overrides |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 3 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-023` | Composite B-tree | `(facility_id, category_type)` | Very High | `SELECT * FROM system_configs WHERE facility_id = $1 AND category_type = $2` |
| `INDEX-051` | B-tree | `(facility_id)` | High | `SELECT * FROM system_configs WHERE facility_id = $1` |
| `INDEX-052` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM system_configs WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `NFR-001, NFR-005`
- **Upstream Workflows**: `WF-002`
- **REST / GraphQL APIs**: `All Microservices via Configuration Bus`
- **Reporting Dashboards**: `System Audit Report`
- **Analytical Warehousing**: `None`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `High-priority edge push via WebSocket / MQTT`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-009`
- **Data Lineage Traceability**: `LINEAGE-003`

### TABLE-013: `intake.patients`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-013`
- **Fully Qualified Name**: `intake.patients`
- **Functional Domain**: `Citizen Demographics`
- **Executive Data Owner**: Chief Medical Officer (CMO)
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-004` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-001`
- **Audit Requirements**: All demographic access and edits logged with DPDP purpose code

#### 2. Business Purpose & Scope Description
**Operational Role**: Master patient index (MPI) storing primary demographic information for all registered citizens.

Stores system UHID (Unique Health Identifier), full name, gender, date of birth, blood group, marital status, and registration facility.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created at citizen registration; updated on demographic verification; retained permanently or statutory 10+ years.
- **Estimated Storage Footprint**: Baseline capacity: `3,500,000 citizens registered across BBMP jurisdiction`; Expected growth rate: `8,000 new patients per day across all wards`.
- **Partitioning Architecture**: `Hash partitioned by id (16 partitions)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Patient initial registration clinic |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `patient_identifiers` | `patient_id` | `1:N` | Patient ABHA, Aadhaar hash, and external identifiers |
| `patient_contacts` | `patient_id` | `1:N` | Patient emergency contacts and phone numbers |
| `patient_addresses` | `patient_id` | `1:N` | Citizen residential address mapped to BBMP ward |
| `consent_records` | `patient_id` | `1:N` | DPDP statutory citizen consent artifacts |
| `tokens` | `patient_id` | `1:N` | Token issued to registered patient |
| `queue_entries` | `patient_id` | `1:N` | Patient queue stage presence |
| `triage_assessments` | `patient_id` | `1:N` | Triage evaluation performed on patient |
| `patient_vitals` | `patient_id` | `1:N` | Longitudinal vital signs observations |
| `danger_alerts` | `patient_id` | `1:N` | Critical danger alert generated for patient |
| `clinical_encounters` | `patient_id` | `1:N` | Outpatient consultation encounter for patient |
| `clinical_notes` | `patient_id` | `1:N` | Longitudinal clinical history linkage |
| `diagnoses` | `patient_id` | `1:N` | Patient diagnostic history |
| `prescriptions` | `patient_id` | `1:N` | Medication prescribed to patient |
| `prescription_items` | `patient_id` | `1:N` | Patient direct linkage for item adherence |
| `lab_orders` | `patient_id` | `1:N` | Patient diagnostic test order |
| `lab_order_items` | `patient_id` | `1:N` | Patient specimen linkage |
| `lab_results` | `patient_id` | `1:N` | Diagnostic observation for patient record |
| `teleconsultations` | `patient_id` | `1:N` | Patient participating in teleconsultation |
| `dispensations` | `patient_id` | `1:N` | Patient receiving medication |
| `dispensation_items` | `patient_id` | `1:N` | Direct patient linkage for pharmacovigilance |
| `referrals` | `patient_id` | `1:N` | Outbound referral dossier for patient |
| `referral_counter_notes` | `patient_id` | `1:N` | Patient counter-referral medical record |
| `ncd_episodes` | `patient_id` | `1:N` | Longitudinal chronic disease care plan |
| `follow_up_schedules` | `patient_id` | `1:N` | Scheduled review appointment for citizen |
| `notifications` | `patient_id` | `1:N` | Notification sent to patient mobile |
| `grievances` | `patient_id` | `1:N` | Citizen filing service grievance |
| `abdm_artifacts` | `patient_id` | `1:N` | ABDM FHIR artifacts linked to registered citizen |

#### 5. Indexing Architecture & Query Acceleration
The table features 4 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-004` | Unique B-tree | `(id)` | Very High | `SELECT * FROM patients WHERE id = $1` |
| `INDEX-005` | Composite B-tree | `(facility_id, created_at)` | High | `SELECT * FROM patients WHERE facility_id = $1 ORDER BY created_at DESC` |
| `INDEX-053` | B-tree | `(facility_id)` | High | `SELECT * FROM patients WHERE facility_id = $1` |
| `INDEX-054` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM patients WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-005, FR-006, PRIV-001, PRIV-002`
- **Upstream Workflows**: `WF-003`
- **REST / GraphQL APIs**: `Registration Portal, Doctor EMR, Pharmacy Dispenser, Citizen Portal`
- **Reporting Dashboards**: `Demographic Census Dashboard, Age-Gender Pyramids`
- **Analytical Warehousing**: `Epidemiological Risk Modeling`
- **AI & Decision Support Models**: `Patient Re-identification Prevention Model`
- **Edge Synchronization**: `Edge-cached on-demand with local offline registration capability`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL (RPO <= 5m, RTO <= 15m)`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `CRITICAL`
- **Governing Data Quality Rules**: `DQ-010, DQ-011`
- **Data Lineage Traceability**: `LINEAGE-004`

### TABLE-014: `intake.patient_identifiers`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-014`
- **Fully Qualified Name**: `intake.patient_identifiers`
- **Functional Domain**: `Citizen Demographics`
- **Executive Data Owner**: Lead Integration Architect
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-004` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-005`
- **Audit Requirements**: Identity search and verification logged to WORM ledger

#### 2. Business Purpose & Scope Description
**Operational Role**: External identity linkages including ABHA Number, ABHA Address, Aadhaar Vault Reference, Ration Card, and Voter ID.

Stores cryptographic tokenized references to national identity systems without persisting plaintext Aadhaar numbers.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Added during identity linking; updated on re-authentication; revoked on consent withdrawal.
- **Estimated Storage Footprint**: Baseline capacity: `5,000,000 identifier records`; Expected growth rate: `10,000 per day`.
- **Partitioning Architecture**: `Hash partitioned by patient_id (16 partitions)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `CASCADE` | Patient ABHA, Aadhaar hash, and external identifiers |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 4 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-006` | B-tree | `(patient_id)` | Very High | `SELECT * FROM patient_identifiers WHERE patient_id = $1` |
| `INDEX-007` | B-tree | `(reference_code)` | Very High | `SELECT patient_id FROM patient_identifiers WHERE reference_code = $1` |
| `INDEX-055` | B-tree | `(facility_id)` | High | `SELECT * FROM patient_identifiers WHERE facility_id = $1` |
| `INDEX-056` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM patient_identifiers WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-007, INT-002, PRIV-003`
- **Upstream Workflows**: `WF-003`
- **REST / GraphQL APIs**: `ABDM M1/M2 Gateway, Citizen Verification Service`
- **Reporting Dashboards**: `ABHA Seeding Progress Dashboard`
- **Analytical Warehousing**: `Social Protection Benefit Cross-Match`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Cloud-authoritative; blind-index queried by edge nodes`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `CRITICAL`
- **Governing Data Quality Rules**: `DQ-012`
- **Data Lineage Traceability**: `LINEAGE-004`

### TABLE-015: `intake.patient_contacts`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-015`
- **Fully Qualified Name**: `intake.patient_contacts`
- **Functional Domain**: `Citizen Demographics`
- **Executive Data Owner**: Patient Experience Officer
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-004` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-001`
- **Audit Requirements**: Contact updates audited; mobile numbers masked on non-privileged views

#### 2. Business Purpose & Scope Description
**Operational Role**: Phone numbers, email addresses, and emergency next-of-kin contact details.

Stores primary and secondary mobile numbers with OTP verification status and emergency relationship codes.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created at registration; updated on phone change; retained with patient profile.
- **Estimated Storage Footprint**: Baseline capacity: `4,200,000 records`; Expected growth rate: `Proportional to patient intake`.
- **Partitioning Architecture**: `Hash partitioned by patient_id (16 partitions)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `CASCADE` | Patient emergency contacts and phone numbers |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 3 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-024` | Composite B-tree | `(patient_id, status)` | Very High | `SELECT * FROM patient_contacts WHERE patient_id = $1 AND status = 'PRIMARY'` |
| `INDEX-057` | B-tree | `(facility_id)` | High | `SELECT * FROM patient_contacts WHERE facility_id = $1` |
| `INDEX-058` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM patient_contacts WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-005, PRIV-001`
- **Upstream Workflows**: `WF-003`
- **REST / GraphQL APIs**: `SMS Gateway, WhatsApp Notification Dispatcher`
- **Reporting Dashboards**: `Contact Reachability Statistics`
- **Analytical Warehousing**: `Telemedicine Churn Predictor`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Edge-replicated for registered clinic patients`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-013`
- **Data Lineage Traceability**: `LINEAGE-004`

### TABLE-016: `intake.patient_addresses`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-016`
- **Fully Qualified Name**: `intake.patient_addresses`
- **Functional Domain**: `Citizen Demographics`
- **Executive Data Owner**: Urban Health Planner
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-004` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-001`
- **Audit Requirements**: Ward changes audited for epidemiological tracking

#### 2. Business Purpose & Scope Description
**Operational Role**: Residential addresses mapped to BBMP municipal wards, zones, and postal pin codes.

Provides GIS geographic attributes, door number, street, ward name, zone identifier, and census block.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created at registration; updated on citizen relocation; retained with patient profile.
- **Estimated Storage Footprint**: Baseline capacity: `3,800,000 records`; Expected growth rate: `Proportional to patient intake`.
- **Partitioning Architecture**: `Hash partitioned by patient_id (16 partitions)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `CASCADE` | Citizen residential address mapped to BBMP ward |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 3 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-025` | Composite B-tree | `(patient_id, status)` | Very High | `SELECT * FROM patient_addresses WHERE patient_id = $1 AND status = 'CURRENT'` |
| `INDEX-059` | B-tree | `(facility_id)` | High | `SELECT * FROM patient_addresses WHERE facility_id = $1` |
| `INDEX-060` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM patient_addresses WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-005, OR-004`
- **Upstream Workflows**: `WF-003`
- **REST / GraphQL APIs**: `GIS Heatmap Service, Disease Surveillance System`
- **Reporting Dashboards**: `Ward-wise Disease Outbreak Map`
- **Analytical Warehousing**: `Geographic Disease Clustering Model`
- **AI & Decision Support Models**: `Outbreak Early Warning Algorithm`
- **Edge Synchronization**: `Edge-replicated for catchment area`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-014`
- **Data Lineage Traceability**: `LINEAGE-004`

### TABLE-017: `intake.consent_records`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-017`
- **Fully Qualified Name**: `intake.consent_records`
- **Functional Domain**: `Consent Management`
- **Executive Data Owner**: Data Protection Officer (DPO)
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-004` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-005`
- **Audit Requirements**: Strict append-only immutable logging; revocations take immediate effect

#### 2. Business Purpose & Scope Description
**Operational Role**: Explicit citizen consent artifacts compliant with DPDP Act 2023 and ABDM Consent Framework.

Stores consent purpose, validity window, clinical data scopes granted, signature/OTP hash, and revocation status.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created at consent grant; updated on scope modification; terminated on revocation; retained 7 years post-expiry.
- **Estimated Storage Footprint**: Baseline capacity: `6,000,000 consent artifacts`; Expected growth rate: `15,000 records/day`.
- **Partitioning Architecture**: `Range partitioned by granted_at (Semi-annual)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | DPDP statutory citizen consent artifacts |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Facility where consent was executed |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 3 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-026` | Composite B-tree | `(patient_id, status)` | Very High | `SELECT * FROM consent_records WHERE patient_id = $1 AND status = 'GRANTED'` |
| `INDEX-061` | B-tree | `(facility_id)` | High | `SELECT * FROM consent_records WHERE facility_id = $1` |
| `INDEX-062` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM consent_records WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-008, PRIV-004, PRIV-005`
- **Upstream Workflows**: `WF-003, WF-015`
- **REST / GraphQL APIs**: `Policy Enforcement Point, ABDM Consent Manager`
- **Reporting Dashboards**: `DPO Statutory Audit Log`
- **Analytical Warehousing**: `Consent Opt-In Conversion Rate`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Cloud-authoritative with edge-local validation cache`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `CRITICAL`
- **Governing Data Quality Rules**: `DQ-015`
- **Data Lineage Traceability**: `LINEAGE-005`

### TABLE-018: `intake.tokens`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-018`
- **Fully Qualified Name**: `intake.tokens`
- **Functional Domain**: `Queue Management`
- **Executive Data Owner**: Clinic Operations Lead
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-007`
- **Audit Requirements**: Token creation, priority overrides, and cancellations logged

#### 2. Business Purpose & Scope Description
**Operational Role**: Daily sequential clinic intake tokens issued to patients upon physical arrival.

Maintains token sequence number (e.g., A-042), priority category (REGULAR, EMERGENCY, GERIATRIC, PREGNANT), and issue timestamp.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Issued daily; updated as patient advances through stages; archived after 90 days.
- **Estimated Storage Footprint**: Baseline capacity: `15,000,000 tokens annually across 450 facilities`; Expected growth rate: `45,000 tokens/day`.
- **Partitioning Architecture**: `Range partitioned by issued_at (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | Token issued to registered patient |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Daily token generated at specific clinic |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `queue_entries` | `token_id` | `1:N` | Queue movement stages tracked per token |
| `triage_assessments` | `token_id` | `1:1` | Daily token linking triage encounter |
| `clinical_encounters` | `token_id` | `1:1` | Daily token associated with consultation |

#### 5. Indexing Architecture & Query Acceleration
The table features 4 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-008` | Composite B-tree | `(facility_id, status)` | High | `SELECT * FROM tokens WHERE facility_id = $1 AND status = 'ACTIVE'` |
| `INDEX-009` | B-tree | `(patient_id)` | Very High | `SELECT * FROM tokens WHERE patient_id = $1` |
| `INDEX-063` | B-tree | `(facility_id)` | High | `SELECT * FROM tokens WHERE facility_id = $1` |
| `INDEX-064` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM tokens WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-009, OR-005`
- **Upstream Workflows**: `WF-003, WF-004`
- **REST / GraphQL APIs**: `Token Dispenser Kiosk, Reception Terminal, Display Monitors`
- **Reporting Dashboards**: `Daily Patient Footfall Analytics`
- **Analytical Warehousing**: `Peak Arrival Time Distribution`
- **AI & Decision Support Models**: `Patient Flow Simulator`
- **Edge Synchronization**: `Edge-local generation with asynchronous cloud telemetry rollup`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-016`
- **Data Lineage Traceability**: `LINEAGE-006`

### TABLE-019: `intake.queue_entries`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-019`
- **Fully Qualified Name**: `intake.queue_entries`
- **Functional Domain**: `Queue Management`
- **Executive Data Owner**: Clinic Operations Lead
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-007`
- **Audit Requirements**: Stage bypasses and emergency pre-emptions audited

#### 2. Business Purpose & Scope Description
**Operational Role**: Real-time state tracking of patient movement through service stages (TRIAGE, DOCTOR, LAB, PHARMACY).

Records stage entry time, call time, completion time, serving staff ID, room ID, and wait duration metrics.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created upon stage transfer; updated on call/complete; retained 90 days for operational KPI calculation.
- **Estimated Storage Footprint**: Baseline capacity: `45,000,000 queue transitions annually`; Expected growth rate: `135,000 transitions/day`.
- **Partitioning Architecture**: `Range partitioned by created_at (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `token_id` | `tokens` | `id` | `CASCADE` | Queue movement stages tracked per token |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Queue progression inside clinic |
| `patient_id` | `patients` | `id` | `RESTRICT` | Patient queue stage presence |
| `room_id` | `facility_rooms` | `id` | `SET NULL` | Physical consultation chamber serving patient |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 4 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-010` | Composite B-tree | `(facility_id, status, priority_score)` | High | `SELECT * FROM queue_entries WHERE facility_id = $1 AND status = 'WAITING' ORDER BY priority_score DESC, created_at ASC` |
| `INDEX-011` | GIN | `(clinical_payload_json)` | High | `SELECT * FROM queue_entries WHERE clinical_payload_json @> '{"fast_track": true}'` |
| `INDEX-065` | B-tree | `(facility_id)` | High | `SELECT * FROM queue_entries WHERE facility_id = $1` |
| `INDEX-066` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM queue_entries WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-009, FR-010, OR-006`
- **Upstream Workflows**: `WF-004`
- **REST / GraphQL APIs**: `Doctor Queue UI, Nurse Triage Station, Pharmacy Dispensing Queue`
- **Reporting Dashboards**: `Stage Bottleneck & Wait Time SLA Dashboard`
- **Analytical Warehousing**: `Service Time Efficiency Model`
- **AI & Decision Support Models**: `Dynamic Queue Balancing Recommender`
- **Edge Synchronization**: `Edge-local state machine; batch-synced to cloud analytics`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-016`
- **Data Lineage Traceability**: `LINEAGE-006`

### TABLE-020: `intake.triage_assessments`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-020`
- **Fully Qualified Name**: `intake.triage_assessments`
- **Functional Domain**: `Clinical Triage`
- **Executive Data Owner**: Nursing Superintendent
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-001`
- **Audit Requirements**: Nurse signature and acuity rating changes logged

#### 2. Business Purpose & Scope Description
**Operational Role**: Nurse triage evaluations capturing chief complaints, visual acuity, emergency signs, and triage priority score.

Captures South African Triage Scale (SATS) / Emergency Severity Index (ESI) category (RED, YELLOW, GREEN) and presenting symptoms.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created during nursing intake; finalized before doctor consultation; retained 10 years as clinical record.
- **Estimated Storage Footprint**: Baseline capacity: `10,000,000 records`; Expected growth rate: `30,000 assessments/day`.
- **Partitioning Architecture**: `Range partitioned by assessed_at (Quarterly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | Triage evaluation performed on patient |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Facility where triage occurred |
| `token_id` | `tokens` | `id` | `SET NULL` | Daily token linking triage encounter |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `patient_vitals` | `triage_id` | `1:N` | Vitals captured during nursing triage session |

#### 5. Indexing Architecture & Query Acceleration
The table features 3 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-027` | Composite B-tree | `(patient_id, created_at)` | Very High | `SELECT * FROM triage_assessments WHERE patient_id = $1 ORDER BY created_at DESC` |
| `INDEX-067` | B-tree | `(facility_id)` | High | `SELECT * FROM triage_assessments WHERE facility_id = $1` |
| `INDEX-068` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM triage_assessments WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-011, CR-001`
- **Upstream Workflows**: `WF-004`
- **REST / GraphQL APIs**: `Nurse Station Tablet, Doctor EMR Alert Banner`
- **Reporting Dashboards**: `Acuity Stratification Monthly Report`
- **Analytical Warehousing**: `Emergency Escalation Predictor`
- **AI & Decision Support Models**: `Early Deterioration Detection Model`
- **Edge Synchronization**: `Edge-local creation; immediate high-priority cloud sync`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-017`
- **Data Lineage Traceability**: `LINEAGE-007`

### TABLE-021: `intake.patient_vitals`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-021`
- **Fully Qualified Name**: `intake.patient_vitals`
- **Functional Domain**: `Clinical Triage`
- **Executive Data Owner**: Chief Medical Officer
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-001`
- **Audit Requirements**: Clinical edits append correction log with reason

#### 2. Business Purpose & Scope Description
**Operational Role**: Physiological measurements: systolic/diastolic blood pressure, pulse rate, SpO2, respiratory rate, temperature, height, weight, BMI.

Standardized longitudinal vitals observations supporting pediatric and adult reference percentile curves.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Captured during triage or doctor visit; immutable clinical observations; retained 10 years.
- **Estimated Storage Footprint**: Baseline capacity: `25,000,000 vitals snapshots`; Expected growth rate: `75,000 readings/day`.
- **Partitioning Architecture**: `Range partitioned by recorded_at (Quarterly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | Longitudinal vital signs observations |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Clinic where vitals recorded |
| `triage_id` | `triage_assessments` | `id` | `SET NULL` | Vitals captured during nursing triage session |
| `encounter_id` | `clinical_encounters` | `id` | `SET NULL` | Vitals recorded directly during physician consultation |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-069` | B-tree | `(facility_id)` | High | `SELECT * FROM patient_vitals WHERE facility_id = $1` |
| `INDEX-070` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM patient_vitals WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-011, CR-002`
- **Upstream Workflows**: `WF-004, WF-005`
- **REST / GraphQL APIs**: `Doctor Consultation EMR, NCD Surveillance Module`
- **Reporting Dashboards**: `Hypertension Screening Progress Dashboard`
- **Analytical Warehousing**: `Population Cardio-Metabolic Risk Model`
- **AI & Decision Support Models**: `Sepsis & Vital Decompensation Alert Model`
- **Edge Synchronization**: `Edge-local storage with bidirectional sync`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-018`
- **Data Lineage Traceability**: `LINEAGE-007`

### TABLE-022: `intake.danger_alerts`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-022`
- **Fully Qualified Name**: `intake.danger_alerts`
- **Functional Domain**: `Clinical Safety`
- **Executive Data Owner**: Clinical Governance Committee
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-001`
- **Audit Requirements**: Physician acknowledgment timestamp and override reason mandatory

#### 2. Business Purpose & Scope Description
**Operational Role**: Real-time clinical safety alerts: critical vitals, anaphylaxis history, severe maternal pre-eclampsia, and pediatric panic thresholds.

Stores alert severity (CRITICAL, WARNING), trigger rule ID, clinician acknowledgment status, and override justification.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Triggered automatically by vitals/triage engine; acknowledged by clinician; archived after 5 years.
- **Estimated Storage Footprint**: Baseline capacity: `1,500,000 alerts`; Expected growth rate: `4,500 alerts/day`.
- **Partitioning Architecture**: `Range partitioned by triggered_at (Quarterly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | Critical danger alert generated for patient |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Clinic where clinical red flag occurred |
| `encounter_id` | `clinical_encounters` | `id` | `SET NULL` | Danger alert triggered during doctor consultation |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 3 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-028` | Composite B-tree | `(facility_id, status)` | Very High | `SELECT * FROM danger_alerts WHERE facility_id = $1 AND status = 'ACTIVE'` |
| `INDEX-071` | B-tree | `(facility_id)` | High | `SELECT * FROM danger_alerts WHERE facility_id = $1` |
| `INDEX-072` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM danger_alerts WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-012, CR-003`
- **Upstream Workflows**: `WF-004, WF-005`
- **REST / GraphQL APIs**: `Doctor Clinical Workstation, Emergency Referral Notification`
- **Reporting Dashboards**: `Clinical Safety Incident Dashboard`
- **Analytical Warehousing**: `Panic Threshold Optimization Model`
- **AI & Decision Support Models**: `Clinical Decision Support Feedback Loop`
- **Edge Synchronization**: `Instant edge-to-cloud push with SMS alert escalation`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-019`
- **Data Lineage Traceability**: `LINEAGE-007`

### TABLE-023: `clinical.clinical_encounters`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-023`
- **Fully Qualified Name**: `clinical.clinical_encounters`
- **Functional Domain**: `Clinical Consultation`
- **Executive Data Owner**: Chief Medical Officer
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-001`
- **Audit Requirements**: Doctor digital signature timestamped; changes post-closure strictly prohibited

#### 2. Business Purpose & Scope Description
**Operational Role**: Master outpatient consultation record documenting doctor-patient interaction event.

Links patient, treating doctor, facility, token, encounter type (OPD, TELEMEDICINE, HOME_VISIT), start/end time, and disposition status.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Initiated on doctor call; completed upon digital sign-off; retained 10 years per statutory rules.
- **Estimated Storage Footprint**: Baseline capacity: `12,000,000 consultations`; Expected growth rate: `35,000 encounters/day across all Namma Clinics`.
- **Partitioning Architecture**: `Range partitioned by encounter_date (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | Outpatient consultation encounter for patient |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Encounter conducted at clinic |
| `doctor_user_id` | `auth_users` | `id` | `RESTRICT` | Treating licensed physician |
| `token_id` | `tokens` | `id` | `SET NULL` | Daily token associated with consultation |
| `ncd_episode_id` | `ncd_episodes` | `id` | `SET NULL` | Encounter conducted as part of longitudinal NCD care |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `clinical_notes` | `encounter_id` | `1:N` | SOAP clinical notes recorded for encounter |
| `diagnoses` | `encounter_id` | `1:N` | Diagnoses formulated during encounter |
| `prescriptions` | `encounter_id` | `1:1` | Electronic prescription issued in encounter |
| `lab_orders` | `encounter_id` | `1:N` | Laboratory investigations ordered during encounter |
| `teleconsultations` | `encounter_id` | `1:1` | Remote specialist consultation session |
| `patient_vitals` | `encounter_id` | `1:N` | Vitals recorded directly during physician consultation |
| `danger_alerts` | `encounter_id` | `1:N` | Danger alert triggered during doctor consultation |
| `referrals` | `encounter_id` | `1:1` | Referral created as disposition of clinical encounter |
| `follow_up_schedules` | `encounter_id` | `1:1` | Follow up scheduled upon encounter discharge |

#### 5. Indexing Architecture & Query Acceleration
The table features 4 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-012` | Composite B-tree | `(patient_id, created_at)` | Very High | `SELECT * FROM clinical_encounters WHERE patient_id = $1 ORDER BY created_at DESC` |
| `INDEX-013` | BRIN | `(facility_id, created_at)` | Medium | `SELECT count(*) FROM clinical_encounters WHERE facility_id = $1 AND created_at BETWEEN $2 AND $3` |
| `INDEX-073` | B-tree | `(facility_id)` | High | `SELECT * FROM clinical_encounters WHERE facility_id = $1` |
| `INDEX-074` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM clinical_encounters WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-013, FR-014, CR-004`
- **Upstream Workflows**: `WF-005`
- **REST / GraphQL APIs**: `Doctor Consultation EMR, FHIR Encounter Exporter, ABDM M3 Gateway`
- **Reporting Dashboards**: `Monthly OPD Workload Report, HMIS Return`
- **Analytical Warehousing**: `Doctor Workload & Consultation Duration Model`
- **AI & Decision Support Models**: `Clinical NLP Summarizer`
- **Edge Synchronization**: `Edge-local capture with cloud synchronization on sign-off`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL (RPO <= 5m, RTO <= 15m)`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `CRITICAL`
- **Governing Data Quality Rules**: `DQ-020`
- **Data Lineage Traceability**: `LINEAGE-008`

### TABLE-024: `clinical.clinical_notes`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-024`
- **Fully Qualified Name**: `clinical.clinical_notes`
- **Functional Domain**: `Clinical Consultation`
- **Executive Data Owner**: Medical Superintendent
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-005` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-001`
- **Audit Requirements**: Addendums require explicit justification; original text never overwritten

#### 2. Business Purpose & Scope Description
**Operational Role**: Detailed clinical narrative in structured SOAP format (Subjective history, Objective exam, Assessment, Plan).

Stores clinical findings, history of present illness, examination notes, and doctor confidential clinical remarks.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created during encounter; locked upon signature; addendum notes supported with version linkage.
- **Estimated Storage Footprint**: Baseline capacity: `12,000,000 records`; Expected growth rate: `35,000 notes/day`.
- **Partitioning Architecture**: `Range partitioned by created_at (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `encounter_id` | `clinical_encounters` | `id` | `CASCADE` | SOAP clinical notes recorded for encounter |
| `patient_id` | `patients` | `id` | `RESTRICT` | Longitudinal clinical history linkage |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Facility scope of clinical note |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-075` | B-tree | `(facility_id)` | High | `SELECT * FROM clinical_notes WHERE facility_id = $1` |
| `INDEX-076` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM clinical_notes WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-014, PRIV-001`
- **Upstream Workflows**: `WF-005`
- **REST / GraphQL APIs**: `Doctor Consultation Workstation, Referral Dossier Service`
- **Reporting Dashboards**: `None (Protected PHI)`
- **Analytical Warehousing**: `De-identified Symptom Frequency Index`
- **AI & Decision Support Models**: `Clinical Decision Support Symptom Classifier`
- **Edge Synchronization**: `Edge-local with encrypted cloud backup`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `CRITICAL`
- **Governing Data Quality Rules**: `DQ-021`
- **Data Lineage Traceability**: `LINEAGE-008`

### TABLE-025: `clinical.diagnoses`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-025`
- **Fully Qualified Name**: `clinical.diagnoses`
- **Functional Domain**: `Clinical Consultation`
- **Executive Data Owner**: Directorate of Public Health
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-001`
- **Audit Requirements**: Diagnostic changes post-encounter logged to medical audit ledger

#### 2. Business Purpose & Scope Description
**Operational Role**: Coded clinical diagnoses mapped to ICD-10 and SNOMED CT taxonomies.

Stores diagnosis code, display term, diagnosis type (PRIMARY, SECONDARY, PROVISIONAL, CONFIRMED), and chronic condition flag.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Added during encounter; retained 10 years with encounter.
- **Estimated Storage Footprint**: Baseline capacity: `18,000,000 diagnosis entries`; Expected growth rate: `50,000 diagnoses/day`.
- **Partitioning Architecture**: `Range partitioned by created_at (Quarterly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `encounter_id` | `clinical_encounters` | `id` | `CASCADE` | Diagnoses formulated during encounter |
| `patient_id` | `patients` | `id` | `RESTRICT` | Patient diagnostic history |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Facility diagnosing condition |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-077` | B-tree | `(facility_id)` | High | `SELECT * FROM diagnoses WHERE facility_id = $1` |
| `INDEX-078` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM diagnoses WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-015, CR-005, INT-003`
- **Upstream Workflows**: `WF-005`
- **REST / GraphQL APIs**: `Disease Surveillance System (IDSP), NCD Registry Module`
- **Reporting Dashboards**: `Communicable Disease Outbreak Report, Top-10 Morbidity Dashboard`
- **Analytical Warehousing**: `Epidemic Transmission Velocity Model`
- **AI & Decision Support Models**: `Automated ICD-10 Coding Assistant`
- **Edge Synchronization**: `Edge-captured; batched to cloud disease surveillance`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-022`
- **Data Lineage Traceability**: `LINEAGE-009`

### TABLE-026: `clinical.prescriptions`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-026`
- **Fully Qualified Name**: `clinical.prescriptions`
- **Functional Domain**: `Pharmacy & Prescribing`
- **Executive Data Owner**: Chief Medical Officer
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-003`
- **Audit Requirements**: Prescription issuance and cancellation cryptographically signed

#### 2. Business Purpose & Scope Description
**Operational Role**: Header record for electronic prescriptions issued by licensed doctors.

Stores prescription number, doctor digital signature token, encounter linkage, clinical instructions, and dispensing status.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Issued by doctor; dispensed by pharmacy; archived after 5 years per drug regulations.
- **Estimated Storage Footprint**: Baseline capacity: `11,000,000 prescriptions`; Expected growth rate: `32,000 prescriptions/day`.
- **Partitioning Architecture**: `Range partitioned by prescribed_at (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `encounter_id` | `clinical_encounters` | `id` | `CASCADE` | Electronic prescription issued in encounter |
| `patient_id` | `patients` | `id` | `RESTRICT` | Medication prescribed to patient |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Prescribing clinic facility |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `prescription_items` | `prescription_id` | `1:N` | Prescription composed of medication line items |
| `dispensations` | `prescription_id` | `1:1` | Dispensation fulfills doctor prescription |

#### 5. Indexing Architecture & Query Acceleration
The table features 3 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-014` | Composite B-tree | `(patient_id, status)` | Very High | `SELECT * FROM prescriptions WHERE patient_id = $1 AND status = 'PENDING'` |
| `INDEX-079` | B-tree | `(facility_id)` | High | `SELECT * FROM prescriptions WHERE facility_id = $1` |
| `INDEX-080` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM prescriptions WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-016, CR-006`
- **Upstream Workflows**: `WF-005, WF-006`
- **REST / GraphQL APIs**: `Pharmacy Dispensing Portal, Citizen Health Locker, SMS Prescription Link`
- **Reporting Dashboards**: `Prescribing Pattern Compliance Audit`
- **Analytical Warehousing**: `Antibiotic Stewardship Surveillance Model`
- **AI & Decision Support Models**: `Drug Interaction & Dosage Checker`
- **Edge Synchronization**: `Immediate edge-to-edge clinic pharmacy sync; cloud archive`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `CRITICAL`
- **Governing Data Quality Rules**: `DQ-023`
- **Data Lineage Traceability**: `LINEAGE-010`

### TABLE-027: `clinical.prescription_items`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-027`
- **Fully Qualified Name**: `clinical.prescription_items`
- **Functional Domain**: `Pharmacy & Prescribing`
- **Executive Data Owner**: Chief Pharmacist
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-003`
- **Audit Requirements**: Dispensing quantity overrides and generic substitutions logged

#### 2. Business Purpose & Scope Description
**Operational Role**: Line items for prescribed medications specifying drug, dosage form, strength, frequency, duration, and quantity.

Detailed pharmacological orders linked to formulary_drugs, specifying instructions (e.g., 1 tablet after food twice daily for 5 days).

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created with prescription; updated with dispensed quantities at pharmacy; retained 5 years.
- **Estimated Storage Footprint**: Baseline capacity: `35,000,000 line items`; Expected growth rate: `100,000 lines/day`.
- **Partitioning Architecture**: `Range partitioned by created_at (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `prescription_id` | `prescriptions` | `id` | `CASCADE` | Prescription composed of medication line items |
| `drug_id` | `formulary_drugs` | `id` | `RESTRICT` | Prescribed drug selected from formulary |
| `patient_id` | `patients` | `id` | `RESTRICT` | Patient direct linkage for item adherence |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Facility context for stock reservation |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-081` | B-tree | `(facility_id)` | High | `SELECT * FROM prescription_items WHERE facility_id = $1` |
| `INDEX-082` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM prescription_items WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-016, FR-017, CR-006`
- **Upstream Workflows**: `WF-005, WF-006`
- **REST / GraphQL APIs**: `Pharmacy Stock Allocation Service, Dispensing Barcode Scanner`
- **Reporting Dashboards**: `Drug Consumption Breakdown Report`
- **Analytical Warehousing**: `Formulary Demand Forecasting Model`
- **AI & Decision Support Models**: `Drug-Drug Interaction Detection Model`
- **Edge Synchronization**: `Edge-local synchronization with pharmacy module`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `CRITICAL`
- **Governing Data Quality Rules**: `DQ-023`
- **Data Lineage Traceability**: `LINEAGE-010`

### TABLE-028: `clinical.lab_orders`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-028`
- **Fully Qualified Name**: `clinical.lab_orders`
- **Functional Domain**: `Diagnostic Services`
- **Executive Data Owner**: Head of Pathology / Diagnostic Services
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-004`
- **Audit Requirements**: Sample collection and result sign-off audited with staff timestamps

#### 2. Business Purpose & Scope Description
**Operational Role**: Header record for diagnostic laboratory investigation requests ordered during consultation.

Stores order number, encounter linkage, ordering physician ID, priority (ROUTINE, STAT), and specimen collection status.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Ordered by physician; sample collected by lab tech; results published; retained 10 years.
- **Estimated Storage Footprint**: Baseline capacity: `4,500,000 lab orders`; Expected growth rate: `12,000 orders/day`.
- **Partitioning Architecture**: `Range partitioned by ordered_at (Quarterly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `encounter_id` | `clinical_encounters` | `id` | `CASCADE` | Laboratory investigations ordered during encounter |
| `patient_id` | `patients` | `id` | `RESTRICT` | Patient diagnostic test order |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Clinic ordering laboratory tests |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `lab_order_items` | `lab_order_id` | `1:N` | Specific diagnostic tests in order |

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-083` | B-tree | `(facility_id)` | High | `SELECT * FROM lab_orders WHERE facility_id = $1` |
| `INDEX-084` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM lab_orders WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-018, CR-007`
- **Upstream Workflows**: `WF-005, WF-007`
- **REST / GraphQL APIs**: `Lab Technician Workstation, Sample Collection Barcode System`
- **Reporting Dashboards**: `Lab Turnaround Time (TAT) SLA Dashboard`
- **Analytical Warehousing**: `Diagnostic Utilization Rate Model`
- **AI & Decision Support Models**: `Lab Test Ordering Appropriateness Advisor`
- **Edge Synchronization**: `Edge-local order creation with cloud routing to hub laboratories`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-024`
- **Data Lineage Traceability**: `LINEAGE-011`

### TABLE-029: `clinical.lab_order_items`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-029`
- **Fully Qualified Name**: `clinical.lab_order_items`
- **Functional Domain**: `Diagnostic Services`
- **Executive Data Owner**: Head of Pathology
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-004`
- **Audit Requirements**: Test cancellations require technician reason code

#### 2. Business Purpose & Scope Description
**Operational Role**: Individual diagnostic tests requested (e.g., Complete Blood Count, HbA1c, Dengue NS1 Ag, Urine Routine).

Test codes mapped to LOINC standard, specimen requirement (Serum, Whole Blood, Urine), and status (PENDING, SAMPLE_COLLECTED, ANALYZED).

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created with order; transitioned during lab workflow; retained 10 years.
- **Estimated Storage Footprint**: Baseline capacity: `12,000,000 items`; Expected growth rate: `35,000 test items/day`.
- **Partitioning Architecture**: `Range partitioned by created_at (Quarterly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `lab_order_id` | `lab_orders` | `id` | `CASCADE` | Specific diagnostic tests in order |
| `patient_id` | `patients` | `id` | `RESTRICT` | Patient specimen linkage |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Facility performing or forwarding sample |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `lab_results` | `order_item_id` | `1:1` | Verified result for diagnostic test item |

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-085` | B-tree | `(facility_id)` | High | `SELECT * FROM lab_order_items WHERE facility_id = $1` |
| `INDEX-086` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM lab_order_items WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-018, CR-007, INT-004`
- **Upstream Workflows**: `WF-007`
- **REST / GraphQL APIs**: `Lab Analyzer Interface (ASTM/HL7), Lab Worklist UI`
- **Reporting Dashboards**: `Test Volume & Reagent Consumption Report`
- **Analytical Warehousing**: `Diagnostic Yield & Positivity Rates`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Edge-local execution; cloud sync on completion`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-024`
- **Data Lineage Traceability**: `LINEAGE-011`

### TABLE-030: `clinical.lab_results`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-030`
- **Fully Qualified Name**: `clinical.lab_results`
- **Functional Domain**: `Diagnostic Services`
- **Executive Data Owner**: Chief Pathologist
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-004`
- **Audit Requirements**: Panic value phone escalation to doctor mandatory logged with timestamp

#### 2. Business Purpose & Scope Description
**Operational Role**: Verified quantitative and qualitative laboratory test results, reference ranges, and critical panic value flags.

Stores numeric/text observation values, measurement units (mg/dL, g/dL), biological reference ranges, and panic status (LOW, NORMAL, HIGH, PANIC).

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Entered by technician; verified by pathologist; immutable upon verification; retained 10 years.
- **Estimated Storage Footprint**: Baseline capacity: `25,000,000 test observations`; Expected growth rate: `70,000 observations/day`.
- **Partitioning Architecture**: `Range partitioned by verified_at (Quarterly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `order_item_id` | `lab_order_items` | `id` | `CASCADE` | Verified result for diagnostic test item |
| `patient_id` | `patients` | `id` | `RESTRICT` | Diagnostic observation for patient record |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Laboratory verifying test results |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-087` | B-tree | `(facility_id)` | High | `SELECT * FROM lab_results WHERE facility_id = $1` |
| `INDEX-088` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM lab_results WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-019, CR-007, CR-008`
- **Upstream Workflows**: `WF-007`
- **REST / GraphQL APIs**: `Doctor EMR Results Viewer, Citizen Health Locker, ABDM Diagnostic Report`
- **Reporting Dashboards**: `Critical Lab Values Compliance Report`
- **Analytical Warehousing**: `Ward-level Diabetes & Anemia Prevalence Trends`
- **AI & Decision Support Models**: `Automated Hematology Pattern Anomaly Detector`
- **Edge Synchronization**: `Immediate cloud sync with doctor alert trigger`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `CRITICAL`
- **Governing Data Quality Rules**: `DQ-025`
- **Data Lineage Traceability**: `LINEAGE-011`

### TABLE-031: `clinical.teleconsultations`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-031`
- **Fully Qualified Name**: `clinical.teleconsultations`
- **Functional Domain**: `Telemedicine`
- **Executive Data Owner**: Telemedicine Program Director
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-016`
- **Audit Requirements**: Connection timestamps, specialist notes, and consent verified

#### 2. Business Purpose & Scope Description
**Operational Role**: Doctor-to-specialist teleconsultation sessions linking Namma Clinic medical officers with secondary/tertiary hospital specialists.

Maintains WebRTC room identifier, session duration, specialist physician ID, audio/video quality metrics, and joint consultation clinical summary.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Scheduled during clinic visit; completed upon call termination; retained 10 years per Telemedicine Practice Guidelines.
- **Estimated Storage Footprint**: Baseline capacity: `350,000 teleconsultations`; Expected growth rate: `1,000 sessions/day`.
- **Partitioning Architecture**: `Range partitioned by session_start (Semi-annual)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `encounter_id` | `clinical_encounters` | `id` | `CASCADE` | Remote specialist consultation session |
| `patient_id` | `patients` | `id` | `RESTRICT` | Patient participating in teleconsultation |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Clinic originating teleconsultation call |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-089` | B-tree | `(facility_id)` | High | `SELECT * FROM teleconsultations WHERE facility_id = $1` |
| `INDEX-090` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM teleconsultations WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-020, CR-009`
- **Upstream Workflows**: `WF-008`
- **REST / GraphQL APIs**: `Teleconsultation Gateway, Video Signaling Server`
- **Reporting Dashboards**: `Specialist Utilization & Telemedicine Reach Dashboard`
- **Analytical Warehousing**: `Teleconsultation Resolution vs Referral Ratio`
- **AI & Decision Support Models**: `Audio Transcription & Clinical Note Draft Generator`
- **Edge Synchronization**: `Cloud-hosted WebRTC session metadata synced to clinic edge`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-026`
- **Data Lineage Traceability**: `LINEAGE-012`

### TABLE-032: `pharmacy.formulary_drugs`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-032`
- **Fully Qualified Name**: `pharmacy.formulary_drugs`
- **Functional Domain**: `Pharmaceutical Master`
- **Executive Data Owner**: BBMP Essential Drugs Committee
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-001` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-009`
- **Audit Requirements**: Formulary inclusions, deletions, and safety limit adjustments audited

#### 2. Business Purpose & Scope Description
**Operational Role**: Master formulary of approved medications, generic names, dosage forms, therapeutic classes, and national drug codes.

Stores generic salt name, strength, dosage form (TABLET, SYRUP, INJECTION, OINTMENT), NLEM status, and maximum daily dose safety limits.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Managed by Central Formulary Committee; version-controlled annual revisions.
- **Estimated Storage Footprint**: Baseline capacity: `1,200 approved drug formulations`; Expected growth rate: `Low (< 50 additions/year)`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `category_id` | `drug_categories` | `id` | `RESTRICT` | Formulary drug classified by therapeutic category |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `prescription_items` | `drug_id` | `1:N` | Prescribed drug selected from formulary |
| `pharmacy_batches` | `drug_id` | `1:N` | Manufactured drug batch belongs to formulary drug |
| `indent_items` | `drug_id` | `1:N` | Drug item requisitioned from warehouse |
| `clinic_stock` | `drug_id` | `1:N` | Clinic stock balance aggregation by formulary drug |
| `stock_movements` | `drug_id` | `1:N` | Stock movement ledger item drug classification |

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-091` | B-tree | `(facility_id)` | High | `SELECT * FROM formulary_drugs WHERE facility_id = $1` |
| `INDEX-092` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM formulary_drugs WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-021, CR-010`
- **Upstream Workflows**: `WF-005, WF-006, WF-009`
- **REST / GraphQL APIs**: `Doctor Prescription Auto-complete, Pharmacy Stock Manager`
- **Reporting Dashboards**: `Essential Drug Formulary Availability Report`
- **Analytical Warehousing**: `Drug Class Utilization Patterns`
- **AI & Decision Support Models**: `Generic Substitution Engine`
- **Edge Synchronization**: `Global edge broadcast to all clinic nodes`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-027`
- **Data Lineage Traceability**: `LINEAGE-013`

### TABLE-033: `pharmacy.drug_categories`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-033`
- **Fully Qualified Name**: `pharmacy.drug_categories`
- **Functional Domain**: `Pharmaceutical Master`
- **Executive Data Owner**: Clinical Pharmacology Advisor
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-001` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-009`
- **Audit Requirements**: Taxonomy updates tracked via administrative audit

#### 2. Business Purpose & Scope Description
**Operational Role**: Therapeutic and anatomical classification categories (WHO ATC coding hierarchy).

Hierarchical categorization (e.g., Cardiovascular System -> Antihypertensives -> ACE Inhibitors) for reporting and safety rule enforcement.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Static master taxonomy; updated with formulary revisions.
- **Estimated Storage Footprint**: Baseline capacity: `150 categories`; Expected growth rate: `Static`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
*None (Top-level root table in domain hierarchy).*

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `formulary_drugs` | `category_id` | `1:N` | Formulary drug classified by therapeutic category |

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-093` | B-tree | `(facility_id)` | High | `SELECT * FROM drug_categories WHERE facility_id = $1` |
| `INDEX-094` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM drug_categories WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-021`
- **Upstream Workflows**: `WF-005, WF-009`
- **REST / GraphQL APIs**: `Formulary Browser, Clinical Safety Engine`
- **Reporting Dashboards**: `Therapeutic Category Expenditure Report`
- **Analytical Warehousing**: `Category-level Consumption Forecasting`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Global edge broadcast`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-027`
- **Data Lineage Traceability**: `LINEAGE-013`

### TABLE-034: `pharmacy.pharmacy_batches`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-034`
- **Fully Qualified Name**: `pharmacy.pharmacy_batches`
- **Functional Domain**: `Inventory & Traceability`
- **Executive Data Owner**: Central Procurement Officer
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-009`
- **Audit Requirements**: Batch quality lock or recall immediately halts dispensing across all clinics

#### 2. Business Purpose & Scope Description
**Operational Role**: Specific physical manufacturing batches of drugs received from central BBMP warehouse or state procurement agency.

Stores manufacturer batch number, manufacture date, expiration date, unit procurement cost, quality testing certification, and recall flag.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created upon warehouse goods receipt; expires based on manufacturer shelf life; retained 8 years for CAG audit.
- **Estimated Storage Footprint**: Baseline capacity: `45,000 active and historical batches`; Expected growth rate: `8,000 new batches/year`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `drug_id` | `formulary_drugs` | `id` | `RESTRICT` | Manufactured drug batch belongs to formulary drug |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `clinic_stock` | `batch_id` | `1:N` | Facility inventory balance per specific batch |
| `dispensation_items` | `batch_id` | `1:N` | Specific batch deducted upon dispensing |
| `stock_movements` | `batch_id` | `1:N` | Batch affected by stock movement |

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-095` | B-tree | `(facility_id)` | High | `SELECT * FROM pharmacy_batches WHERE facility_id = $1` |
| `INDEX-096` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM pharmacy_batches WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-022, CR-011`
- **Upstream Workflows**: `WF-006, WF-009`
- **REST / GraphQL APIs**: `Pharmacy Dispensing UI, Warehouse Goods Inward Service`
- **Reporting Dashboards**: `Batch Expiry Aging Dashboard, Quality Recall Status`
- **Analytical Warehousing**: `Inventory Expiry Waste Prediction`
- **AI & Decision Support Models**: `Batch Near-Expiry Redistribution Optimizer`
- **Edge Synchronization**: `Replicated across facilities receiving shipment`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-028`
- **Data Lineage Traceability**: `LINEAGE-014`

### TABLE-035: `pharmacy.clinic_stock`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-035`
- **Fully Qualified Name**: `pharmacy.clinic_stock`
- **Functional Domain**: `Inventory & Traceability`
- **Executive Data Owner**: Clinic Pharmacist / MOIC
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-009`
- **Audit Requirements**: Discrepancy adjustments require physical stock count reconciliation and MOIC sign-off

#### 2. Business Purpose & Scope Description
**Operational Role**: Real-time stock balance of medications at each individual Namma Clinic pharmacy store.

Maintains quantity on hand, reserved quantity, reorder threshold, maximum stock level, and storage bin location per batch.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Updated in real-time on every dispensation, inward receipt, and adjustment; active inventory ledger.
- **Estimated Storage Footprint**: Baseline capacity: `250,000 stock balance records across 450 facilities`; Expected growth rate: `Proportional to facility and drug count`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Current stock inventory held at facility |
| `batch_id` | `pharmacy_batches` | `id` | `RESTRICT` | Facility inventory balance per specific batch |
| `drug_id` | `formulary_drugs` | `id` | `RESTRICT` | Clinic stock balance aggregation by formulary drug |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 3 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-015` | Unique B-tree | `(facility_id, batch_id)` | Very High | `SELECT quantity_on_hand FROM clinic_stock WHERE facility_id = $1 AND batch_id = $2` |
| `INDEX-097` | B-tree | `(facility_id)` | High | `SELECT * FROM clinic_stock WHERE facility_id = $1` |
| `INDEX-098` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM clinic_stock WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-022, OR-007`
- **Upstream Workflows**: `WF-006, WF-009`
- **REST / GraphQL APIs**: `Pharmacy Dispensing Point of Sale, Indent Generator`
- **Reporting Dashboards**: `Real-time Clinic Stockout Warning Dashboard`
- **Analytical Warehousing**: `Stock Depletion Velocity & Buffer Stock Model`
- **AI & Decision Support Models**: `Automated Reorder Quantity Recommender`
- **Edge Synchronization**: `Edge-local authoritative balance; continuous sync to cloud central inventory`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `CRITICAL`
- **Governing Data Quality Rules**: `DQ-029`
- **Data Lineage Traceability**: `LINEAGE-014`

### TABLE-036: `pharmacy.dispensations`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-036`
- **Fully Qualified Name**: `pharmacy.dispensations`
- **Functional Domain**: `Pharmacy Operations`
- **Executive Data Owner**: Chief Pharmacist
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-003`
- **Audit Requirements**: Pharmacist identity and timestamp locked on dispense completion

#### 2. Business Purpose & Scope Description
**Operational Role**: Header record for the physical event of medication dispensing by a registered pharmacist.

Records dispensation transaction number, prescription linkage, dispensing pharmacist ID, patient pickup timestamp, and counseling notes.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created upon drug handover; immutable completed dispensation; retained 5 years.
- **Estimated Storage Footprint**: Baseline capacity: `11,000,000 dispensations`; Expected growth rate: `32,000 dispensations/day`.
- **Partitioning Architecture**: `Range partitioned by dispensed_at (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `prescription_id` | `prescriptions` | `id` | `RESTRICT` | Dispensation fulfills doctor prescription |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Pharmacy counter dispensing drugs |
| `patient_id` | `patients` | `id` | `RESTRICT` | Patient receiving medication |
| `pharmacist_user_id` | `auth_users` | `id` | `RESTRICT` | Licensed pharmacist dispensing medications |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `dispensation_items` | `dispensation_id` | `1:N` | Dispensation composed of drug items |

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-099` | B-tree | `(facility_id)` | High | `SELECT * FROM dispensations WHERE facility_id = $1` |
| `INDEX-100` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM dispensations WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-023, CR-012`
- **Upstream Workflows**: `WF-006`
- **REST / GraphQL APIs**: `Pharmacy Dispensing Workstation, Citizen Mobile Prescription Receipt`
- **Reporting Dashboards**: `Pharmacy Daily Fulfillment SLA Report`
- **Analytical Warehousing**: `Patient Medication Adherence Estimator`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Edge-local capture with cloud synchronization`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-030`
- **Data Lineage Traceability**: `LINEAGE-015`

### TABLE-037: `pharmacy.dispensation_items`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-037`
- **Fully Qualified Name**: `pharmacy.dispensation_items`
- **Functional Domain**: `Pharmacy Operations`
- **Executive Data Owner**: Chief Pharmacist
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-003`
- **Audit Requirements**: Batch deduction verified by cryptographic stock movement linkage

#### 2. Business Purpose & Scope Description
**Operational Role**: Detailed line items for dispensed medications linking specific batch numbers and quantities deducted from stock.

Stores dispensed quantity, batch linkage, drug unit cost, expiry date at dispensation, and instructions given to citizen.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created with dispensation; decrements clinic_stock; retained 5 years.
- **Estimated Storage Footprint**: Baseline capacity: `33,000,000 items`; Expected growth rate: `95,000 items/day`.
- **Partitioning Architecture**: `Range partitioned by created_at (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `dispensation_id` | `dispensations` | `id` | `CASCADE` | Dispensation composed of drug items |
| `batch_id` | `pharmacy_batches` | `id` | `RESTRICT` | Specific batch deducted upon dispensing |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Facility inventory decrement context |
| `patient_id` | `patients` | `id` | `RESTRICT` | Direct patient linkage for pharmacovigilance |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-101` | B-tree | `(facility_id)` | High | `SELECT * FROM dispensation_items WHERE facility_id = $1` |
| `INDEX-102` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM dispensation_items WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-023, CR-012`
- **Upstream Workflows**: `WF-006`
- **REST / GraphQL APIs**: `Pharmacy Inventory Deductor, Barcode Dispense Validator`
- **Reporting Dashboards**: `Monthly Drug Consumption Returns`
- **Analytical Warehousing**: `Prescription vs Dispensation Discrepancy Rate`
- **AI & Decision Support Models**: `Dispensation Error Anomaly Detector`
- **Edge Synchronization**: `Edge-local capture with cloud rollup`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-030`
- **Data Lineage Traceability**: `LINEAGE-015`

### TABLE-038: `pharmacy.stock_movements`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-038`
- **Fully Qualified Name**: `pharmacy.stock_movements`
- **Functional Domain**: `Inventory & Traceability`
- **Executive Data Owner**: Chief Financial Officer (CFO) & Chief Pharmacist
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-009`
- **Audit Requirements**: Strict append-only ledger; running balance must equal previous balance + quantity change

#### 2. Business Purpose & Scope Description
**Operational Role**: Double-entry immutable audit ledger for every change in drug stock (RECEIPT, DISPENSATION, TRANSFER_IN, TRANSFER_OUT, EXPIRY, DAMAGE).

Stores movement type, source facility, destination facility, batch ID, quantity change (+/-), running balance, and authorizing voucher.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Append-only immutable transaction log; retained 8 years for statutory municipal financial audits.
- **Estimated Storage Footprint**: Baseline capacity: `40,000,000 movement records`; Expected growth rate: `120,000 transactions/day`.
- **Partitioning Architecture**: `Range partitioned by movement_timestamp (Quarterly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Inventory movement audit ledger for facility |
| `batch_id` | `pharmacy_batches` | `id` | `RESTRICT` | Batch affected by stock movement |
| `drug_id` | `formulary_drugs` | `id` | `RESTRICT` | Stock movement ledger item drug classification |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-103` | B-tree | `(facility_id)` | High | `SELECT * FROM stock_movements WHERE facility_id = $1` |
| `INDEX-104` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM stock_movements WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-024, OR-008`
- **Upstream Workflows**: `WF-006, WF-009`
- **REST / GraphQL APIs**: `Inventory Audit Service, Financial Reconciliation Pipeline`
- **Reporting Dashboards**: `CAG Statutory Audit Ledger, Stock Shrinkage & Loss Report`
- **Analytical Warehousing**: `Inter-Clinic Stock Transfer Optimization`
- **AI & Decision Support Models**: `Inventory Leakage & Anomaly Detection Model`
- **Edge Synchronization**: `Edge transactions sequenced and reconciled via cloud ledger`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `CRITICAL`
- **Governing Data Quality Rules**: `DQ-031`
- **Data Lineage Traceability**: `LINEAGE-015`

### TABLE-039: `pharmacy.drug_indents`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-039`
- **Fully Qualified Name**: `pharmacy.drug_indents`
- **Functional Domain**: `Supply Chain & Procurement`
- **Executive Data Owner**: Central Medical Stores Officer
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-009`
- **Audit Requirements**: Workflow approvals and delivery discrepancies audited

#### 2. Business Purpose & Scope Description
**Operational Role**: Electronic drug requisition orders submitted by clinic pharmacists to the BBMP Central Medical Stores.

Stores indent number, requisition date, approving MOIC ID, warehouse processing status (SUBMITTED, APPROVED, DISPATCHED, RECEIVED), and fulfillment dates.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Initiated by clinic; approved by MOIC; fulfilled by warehouse; retained 8 years.
- **Estimated Storage Footprint**: Baseline capacity: `120,000 indents`; Expected growth rate: `3,000 indents/month across 450 clinics`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Indent submitted by requesting clinic |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `indent_items` | `indent_id` | `1:N` | Medication line items requested in indent |

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-105` | B-tree | `(facility_id)` | High | `SELECT * FROM drug_indents WHERE facility_id = $1` |
| `INDEX-106` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM drug_indents WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-025, OR-009`
- **Upstream Workflows**: `WF-009`
- **REST / GraphQL APIs**: `Warehouse Management System (WMS), Clinic Indent Portal`
- **Reporting Dashboards**: `Indent Fulfillment Lead Time Dashboard`
- **Analytical Warehousing**: `Supply Chain Bottleneck Analysis`
- **AI & Decision Support Models**: `Central Warehouse Dispatch Route Optimizer`
- **Edge Synchronization**: `Cloud-authoritative workflow with edge notifications`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-032`
- **Data Lineage Traceability**: `LINEAGE-016`

### TABLE-040: `pharmacy.indent_items`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-040`
- **Fully Qualified Name**: `pharmacy.indent_items`
- **Functional Domain**: `Supply Chain & Procurement`
- **Executive Data Owner**: Central Medical Stores Officer
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-009`
- **Audit Requirements**: Quantity cuts by central warehouse logged with reason code

#### 2. Business Purpose & Scope Description
**Operational Role**: Individual medication line items requested in an indent, requested quantity, approved quantity, and dispatched quantity.

Tracks formulary_drugs linkage, current clinic stock at request time, average monthly consumption (AMC), and warehouse allocation.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created with indent; updated during warehouse fulfillment; retained 8 years.
- **Estimated Storage Footprint**: Baseline capacity: `1,500,000 indent items`; Expected growth rate: `35,000 items/month`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `indent_id` | `drug_indents` | `id` | `CASCADE` | Medication line items requested in indent |
| `drug_id` | `formulary_drugs` | `id` | `RESTRICT` | Drug item requisitioned from warehouse |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Clinic destination for indent item delivery |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-107` | B-tree | `(facility_id)` | High | `SELECT * FROM indent_items WHERE facility_id = $1` |
| `INDEX-108` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM indent_items WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-025, OR-009`
- **Upstream Workflows**: `WF-009`
- **REST / GraphQL APIs**: `Warehouse Picking Service, Clinic Receiving Dock`
- **Reporting Dashboards**: `Indent Fulfillment Ratio & Cut-Ratio Report`
- **Analytical Warehousing**: `Procurement Demand Aggregation Model`
- **AI & Decision Support Models**: `Automated Stock Rationing Algorithm`
- **Edge Synchronization**: `Cloud-authoritative with edge sync`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-032`
- **Data Lineage Traceability**: `LINEAGE-016`

### TABLE-041: `pharmacy.cold_chain_devices`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-041`
- **Fully Qualified Name**: `pharmacy.cold_chain_devices`
- **Functional Domain**: `Cold Chain & IoT`
- **Executive Data Owner**: State Immunization Officer
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-008`
- **Audit Requirements**: Threshold configuration and calibration certificates audited

#### 2. Business Purpose & Scope Description
**Operational Role**: Master directory of temperature-controlled storage equipment (Ice-Lined Refrigerators, Deep Freezers, Vaccine Carriers) and IoT loggers.

Stores device serial number, model, manufacturer, installation date, clinic room linkage, min/max safe temperature thresholds (+2C to +8C), and IoT telemetry gateway MAC address.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Registered on installation; calibrated annually; decommissioned on replacement; retained 3 years.
- **Estimated Storage Footprint**: Baseline capacity: `1,800 devices across clinics and storage points`; Expected growth rate: `Low`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Vaccine refrigerator located in clinic facility |
| `room_id` | `facility_rooms` | `id` | `SET NULL` | Room where cold chain device is physically installed |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `cold_chain_telemetry` | `device_id` | `1:N` | High-frequency temperature sensor observations |
| `helpdesk_tickets` | `device_id` | `1:N` | Equipment fault ticket for cold chain refrigerator |

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-109` | B-tree | `(facility_id)` | High | `SELECT * FROM cold_chain_devices WHERE facility_id = $1` |
| `INDEX-110` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM cold_chain_devices WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-026, OR-010`
- **Upstream Workflows**: `WF-010`
- **REST / GraphQL APIs**: `IoT Ingestion Gateway, Cold Chain Monitoring Dashboard`
- **Reporting Dashboards**: `UIP Vaccine Cold Chain Integrity Report`
- **Analytical Warehousing**: `Equipment Failure Prediction Model`
- **AI & Decision Support Models**: `Thermal Anomaly & Compressor Degradation Predictor`
- **Edge Synchronization**: `Global edge broadcast to local telemetry collector`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-033`
- **Data Lineage Traceability**: `LINEAGE-017`

### TABLE-042: `pharmacy.cold_chain_telemetry`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-042`
- **Fully Qualified Name**: `pharmacy.cold_chain_telemetry`
- **Functional Domain**: `Cold Chain & IoT`
- **Executive Data Owner**: Immunization Cold Chain Technician
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-008`
- **Audit Requirements**: Temperature breach (> +8C or < +2C for > 15m) triggers critical incident escalation

#### 2. Business Purpose & Scope Description
**Operational Role**: Time-series IoT sensor readings capturing refrigerator internal temperatures, ambient temperatures, door openings, and power status.

High-frequency telemetry (60-second intervals) recording temperature_celsius, humidity_percent, battery_level, door_open_flag, and alert_status.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Ingested continuously; active raw readings retained 180 days; hourly aggregates retained 3 years.
- **Estimated Storage Footprint**: Baseline capacity: `250,000,000 sensor observations annually`; Expected growth rate: `700,000 readings/day`.
- **Partitioning Architecture**: `Range partitioned by recorded_at (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `device_id` | `cold_chain_devices` | `id` | `CASCADE` | High-frequency temperature sensor observations |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Clinic temperature log roll-up |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 3 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-016` | BRIN | `(facility_id, created_at)` | Medium | `SELECT avg(temperature) FROM cold_chain_telemetry WHERE facility_id = $1 AND created_at >= now() - interval '24h'` |
| `INDEX-111` | B-tree | `(facility_id)` | High | `SELECT * FROM cold_chain_telemetry WHERE facility_id = $1` |
| `INDEX-112` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM cold_chain_telemetry WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-026, OR-010`
- **Upstream Workflows**: `WF-010`
- **REST / GraphQL APIs**: `Real-time Telemetry Stream Processor (Kafka / Flink), SMS Alert Dispatcher`
- **Reporting Dashboards**: `Hourly Cold Chain Excursion Dashboard`
- **Analytical Warehousing**: `Vaccine Thermal Exposure Risk Score`
- **AI & Decision Support Models**: `Early Power Outage & Door Left Open Predictor`
- **Edge Synchronization**: `Edge-buffered via MQTT; batched to cloud time-series store`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `STANDARD`
- **Recovery Priority**: `Tier 3`
- **Migration Sensitivity**: `LOW (High-volume time series)`
- **Governing Data Quality Rules**: `DQ-034`
- **Data Lineage Traceability**: `LINEAGE-017`

### TABLE-043: `continuity.referrals`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-043`
- **Fully Qualified Name**: `continuity.referrals`
- **Functional Domain**: `Continuity of Care`
- **Executive Data Owner**: District Health Officer (DHO)
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-010`
- **Audit Requirements**: Emergency referrals trigger instant SMS notification to ambulance & destination hospital

#### 2. Business Purpose & Scope Description
**Operational Role**: Outbound patient referral dossiers routing complex cases to secondary/tertiary hospitals (e.g., Bowring, Victoria, KC General).

Stores referral number, reason, provisional diagnosis, target hospital specialty, urgency level (ROUTINE, URGENT, EMERGENCY), and transfer summary.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created by Namma Clinic doctor; updated on receiving hospital triage; completed on discharge/counter-referral; retained 10 years.
- **Estimated Storage Footprint**: Baseline capacity: `1,200,000 referrals`; Expected growth rate: `3,500 referrals/day`.
- **Partitioning Architecture**: `Range partitioned by referred_at (Quarterly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | Outbound referral dossier for patient |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Referring clinic facility |
| `target_facility_id` | `facilities` | `id` | `RESTRICT` | Destination secondary/tertiary hospital |
| `encounter_id` | `clinical_encounters` | `id` | `SET NULL` | Referral created as disposition of clinical encounter |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `referral_counter_notes` | `referral_id` | `1:N` | Specialist feedback counter-note |

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-113` | B-tree | `(facility_id)` | High | `SELECT * FROM referrals WHERE facility_id = $1` |
| `INDEX-114` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM referrals WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-027, CR-013, INT-005`
- **Upstream Workflows**: `WF-011`
- **REST / GraphQL APIs**: `Referral Exchange Service, Secondary Hospital EMR, ABDM Health Document Bridge`
- **Reporting Dashboards**: `Referral Closure Rate & Destination Hospital Congestion Dashboard`
- **Analytical Warehousing**: `Referral Leakage & Non-Adherence Model`
- **AI & Decision Support Models**: `Specialty Recommendation Advisor`
- **Edge Synchronization**: `Cloud-authoritative exchange with edge clinic synchronization`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-035`
- **Data Lineage Traceability**: `LINEAGE-018`

### TABLE-044: `continuity.referral_counter_notes`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-044`
- **Fully Qualified Name**: `continuity.referral_counter_notes`
- **Functional Domain**: `Continuity of Care`
- **Executive Data Owner**: District Health Officer
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-010`
- **Audit Requirements**: Reception and doctor review of counter-note audited

#### 2. Business Purpose & Scope Description
**Operational Role**: Counter-referral clinical feedback returned by secondary hospital specialists to the referring Namma Clinic doctor.

Stores specialist final diagnosis, operative procedures performed, discharge medication plan, and recommended local follow-up protocol.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created by hospital specialist; received by primary care clinic; integrated into patient health record; retained 10 years.
- **Estimated Storage Footprint**: Baseline capacity: `800,000 feedback notes`; Expected growth rate: `2,200 notes/day`.
- **Partitioning Architecture**: `Range partitioned by created_at (Quarterly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `referral_id` | `referrals` | `id` | `CASCADE` | Specialist feedback counter-note |
| `patient_id` | `patients` | `id` | `RESTRICT` | Patient counter-referral medical record |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Referring clinic receiving specialist feedback |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-115` | B-tree | `(facility_id)` | High | `SELECT * FROM referral_counter_notes WHERE facility_id = $1` |
| `INDEX-116` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM referral_counter_notes WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-027, CR-013`
- **Upstream Workflows**: `WF-011`
- **REST / GraphQL APIs**: `Doctor Consultation EMR, Longitudinal Care Plan Service`
- **Reporting Dashboards**: `Two-Way Referral Loop Closure Efficiency`
- **Analytical Warehousing**: `Primary Care Diagnostic Concordance Analysis`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Cloud-replicated to referring clinic`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-035`
- **Data Lineage Traceability**: `LINEAGE-018`

### TABLE-045: `continuity.ncd_episodes`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-045`
- **Fully Qualified Name**: `continuity.ncd_episodes`
- **Functional Domain**: `Chronic Disease Management`
- **Executive Data Owner**: NCD Program Officer
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-013`
- **Audit Requirements**: Target goal adjustments and risk tier transitions audited

#### 2. Business Purpose & Scope Description
**Operational Role**: Longitudinal episode management records for citizens with Non-Communicable Diseases (Diabetes, Hypertension, COPD, Cancer).

Tracks diagnosis date, disease staging, treatment target goals (e.g., HbA1c < 7.0%, BP < 130/80), lifestyle counseling status, and assigned ASHA worker.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Enrolled on confirmed diagnosis; actively maintained for citizen lifespan; retained 15 years.
- **Estimated Storage Footprint**: Baseline capacity: `1,500,000 registered NCD patients`; Expected growth rate: `15,000 new enrollments/month`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | Longitudinal chronic disease care plan |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Primary clinic managing patient NCD plan |

**Outbound Dependencies (Child tables referencing this table):**
| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |
| :--- | :--- | :--- | :--- |
| `clinical_encounters` | `ncd_episode_id` | `1:N` | Encounter conducted as part of longitudinal NCD care |

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-117` | B-tree | `(facility_id)` | High | `SELECT * FROM ncd_episodes WHERE facility_id = $1` |
| `INDEX-118` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM ncd_episodes WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-028, CR-014`
- **Upstream Workflows**: `WF-012`
- **REST / GraphQL APIs**: `NCD Registry Portal, ASHA Mobile Tablet App, NP-NCD National Portal Sync`
- **Reporting Dashboards**: `Ward-wise Hypertension/Diabetes Control Rate Dashboard`
- **Analytical Warehousing**: `Cardiovascular 10-Year Risk Score (Framingham / WHO)`
- **AI & Decision Support Models**: `NCD Disease Complication Early Warning Model`
- **Edge Synchronization**: `Edge-replicated for enrolled patient catchment area`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-036`
- **Data Lineage Traceability**: `LINEAGE-019`

### TABLE-046: `continuity.follow_up_schedules`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-046`
- **Fully Qualified Name**: `continuity.follow_up_schedules`
- **Functional Domain**: `Continuity of Care`
- **Executive Data Owner**: Clinic Operations Lead
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-001`
- **Audit Requirements**: Missed follow-up escalation to ASHA worker logged

#### 2. Business Purpose & Scope Description
**Operational Role**: Scheduled follow-up dates and reminder triggers for chronic disease review, antenatal checks, and post-referral monitoring.

Maintains scheduled review date, clinical purpose, notification delivery status, attendance outcome (ATTENDED, MISSED, RESCHEDULED), and overdue flags.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created at encounter discharge; updated on patient visit; archived after 3 years.
- **Estimated Storage Footprint**: Baseline capacity: `18,000,000 schedules`; Expected growth rate: `50,000 schedules/day`.
- **Partitioning Architecture**: `Range partitioned by scheduled_date (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | Scheduled review appointment for citizen |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Clinic where follow-up will occur |
| `encounter_id` | `clinical_encounters` | `id` | `SET NULL` | Follow up scheduled upon encounter discharge |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-119` | B-tree | `(facility_id)` | High | `SELECT * FROM follow_up_schedules WHERE facility_id = $1` |
| `INDEX-120` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM follow_up_schedules WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-029, OR-011`
- **Upstream Workflows**: `WF-012, WF-013`
- **REST / GraphQL APIs**: `Notification Dispatcher, Clinic Daily Appointment Calendar, ASHA Line-List`
- **Reporting Dashboards**: `Patient Follow-up Adherence & Retention Dashboard`
- **Analytical Warehousing**: `Care Continuity Dropout Predictor`
- **AI & Decision Support Models**: `Predictive Appointment No-Show Model`
- **Edge Synchronization**: `Edge-local view synchronized with cloud scheduler`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-037`
- **Data Lineage Traceability**: `LINEAGE-020`

### TABLE-047: `continuity.notifications`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-047`
- **Fully Qualified Name**: `continuity.notifications`
- **Functional Domain**: `Citizen Engagement`
- **Executive Data Owner**: Citizen Communication Lead
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-015`
- **Audit Requirements**: Citizen opt-out preferences strictly enforced; delivery timestamps audited

#### 2. Business Purpose & Scope Description
**Operational Role**: Outbound citizen communications: appointment reminders, prescription links, lab ready notifications, and public health advisories.

Stores channel (SMS, WHATSAPP, VOICE_CALL), recipient mobile, template ID, message text, dispatch status (SENT, DELIVERED, FAILED), and telecom gateway DLR reference.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created by triggering event; dispatched via telecom gateway; retained 12 months per TRAI regulations.
- **Estimated Storage Footprint**: Baseline capacity: `40,000,000 notifications annually`; Expected growth rate: `120,000 messages/day`.
- **Partitioning Architecture**: `Range partitioned by created_at (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `SET NULL` | Notification sent to patient mobile |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Clinic originating communication message |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-121` | B-tree | `(facility_id)` | High | `SELECT * FROM notifications WHERE facility_id = $1` |
| `INDEX-122` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM notifications WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-030, OR-012`
- **Upstream Workflows**: `WF-013`
- **REST / GraphQL APIs**: `Telecom Aggregator Gateway (Karix / ValueFirst), Citizen App Push Service`
- **Reporting Dashboards**: `Message Delivery Rate & Telecom Cost SLA Report`
- **Analytical Warehousing**: `Communication Channel Effectiveness Model`
- **AI & Decision Support Models**: `Optimal Notification Send-Time Optimizer`
- **Edge Synchronization**: `Cloud-authoritative dispatch pipeline`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `STANDARD`
- **Recovery Priority**: `Tier 3`
- **Migration Sensitivity**: `LOW`
- **Governing Data Quality Rules**: `DQ-038`
- **Data Lineage Traceability**: `LINEAGE-021`

### TABLE-048: `continuity.grievances`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-048`
- **Fully Qualified Name**: `continuity.grievances`
- **Functional Domain**: `Citizen Grievance & Feedback`
- **Executive Data Owner**: BBMP Public Grievance Officer
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-014`
- **Audit Requirements**: SLA breach automatically escalates to Commissioner with immutable timestamp

#### 2. Business Purpose & Scope Description
**Operational Role**: Citizen complaints, service feedback, and Sakala statutory grievance tickets regarding clinic services.

Records Sakala grievance number, clinic linkage, category (STAFF_BEHAVIOR, DRUG_UNAVAILABLE, WAIT_TIME, FACILITY_CLEANLINESS), SLA deadline, and resolution details.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Filed by citizen/helpdesk; assigned to MOIC/DHO; resolved with citizen sign-off; retained 5 years.
- **Estimated Storage Footprint**: Baseline capacity: `250,000 grievances`; Expected growth rate: `8,000 grievances/month`.
- **Partitioning Architecture**: `Range partitioned by filed_at (Semi-annual)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Clinic subject to citizen grievance ticket |
| `patient_id` | `patients` | `id` | `SET NULL` | Citizen filing service grievance |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-123` | B-tree | `(facility_id)` | High | `SELECT * FROM grievances WHERE facility_id = $1` |
| `INDEX-124` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM grievances WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `FR-031, OR-013`
- **Upstream Workflows**: `WF-014`
- **REST / GraphQL APIs**: `Sakala Portal Gateway, Citizen Grievance App, DHO Review Portal`
- **Reporting Dashboards**: `Sakala SLA Compliance & Ward Grievance Heatmap`
- **Analytical Warehousing**: `Clinic Dissatisfaction Root Cause Analyzer`
- **AI & Decision Support Models**: `Automated Grievance Classification & Priority Tagger`
- **Edge Synchronization**: `Cloud-authoritative with edge-local complaint capture`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 2`
- **Migration Sensitivity**: `MEDIUM`
- **Governing Data Quality Rules**: `DQ-039`
- **Data Lineage Traceability**: `LINEAGE-022`

### TABLE-049: `continuity.helpdesk_tickets`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-049`
- **Fully Qualified Name**: `continuity.helpdesk_tickets`
- **Functional Domain**: `IT & Infrastructure Support`
- **Executive Data Owner**: IT Infrastructure Lead
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-002` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-019`
- **Audit Requirements**: Hardware replacement serial numbers and vendor penalty credits audited

#### 2. Business Purpose & Scope Description
**Operational Role**: Internal facility equipment breakdowns, IT hardware tickets, solar inverter faults, and peripheral maintenance requests.

Maintains ticket ID, facility linkage, asset type (TABLET, THERMAL_PRINTER, POWER_BACKUP, IOT_GATEWAY), vendor SLA deadline, and technician fix notes.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Opened by clinic staff; serviced by vendor; closed upon verification; retained 3 years.
- **Estimated Storage Footprint**: Baseline capacity: `150,000 tickets`; Expected growth rate: `4,000 tickets/month`.
- **Partitioning Architecture**: `None`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Clinic hardware or IT issue ticket |
| `device_id` | `cold_chain_devices` | `id` | `SET NULL` | Equipment fault ticket for cold chain refrigerator |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-125` | B-tree | `(facility_id)` | High | `SELECT * FROM helpdesk_tickets WHERE facility_id = $1` |
| `INDEX-126` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM helpdesk_tickets WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `OR-014`
- **Upstream Workflows**: `WF-014`
- **REST / GraphQL APIs**: `IT Service Management (ITSM) Portal, Field Technician Mobile App`
- **Reporting Dashboards**: `Hardware Uptime SLA & Vendor Performance Dashboard`
- **Analytical Warehousing**: `Equipment Mean Time Between Failures (MTBF)`
- **AI & Decision Support Models**: `Predictive Hardware Maintenance Model`
- **Edge Synchronization**: `Cloud-hosted with edge-local reporting form`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `STANDARD`
- **Recovery Priority**: `Tier 3`
- **Migration Sensitivity**: `LOW`
- **Governing Data Quality Rules**: `DQ-040`
- **Data Lineage Traceability**: `LINEAGE-023`

### TABLE-050: `audit.audit_events`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-050`
- **Fully Qualified Name**: `audit.audit_events`
- **Functional Domain**: `Compliance & Security`
- **Executive Data Owner**: Chief Information Security Officer
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-004` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-006`
- **Audit Requirements**: Absolute immutability; cryptographic chain break triggers emergency SOC security alert

#### 2. Business Purpose & Scope Description
**Operational Role**: Master append-only tamper-evident audit ledger capturing every critical data access, state mutation, and security event.

Cryptographically chained log storing actor ID, event category, resource URI, previous state hash, new state hash, SHA-256 HMAC chain link, and client TLS metadata.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Append-only immutable; written in real-time; never updated or deleted; retained 10 years in WORM storage.
- **Estimated Storage Footprint**: Baseline capacity: `500,000,000 audit events`; Expected growth rate: `1,500,000 events/day`.
- **Partitioning Architecture**: `Range partitioned by event_timestamp (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `actor_user_id` | `auth_users` | `id` | `SET NULL` | User performing audited system mutation |
| `facility_id` | `facilities` | `id` | `SET NULL` | Facility location where audited mutation occurred |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 3 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-017` | BRIN | `(created_at)` | Medium | `SELECT * FROM audit_events WHERE created_at BETWEEN $1 AND $2` |
| `INDEX-127` | B-tree | `(facility_id)` | High | `SELECT * FROM audit_events WHERE facility_id = $1` |
| `INDEX-128` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM audit_events WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `SECR-008, SECR-009, PRIV-006`
- **Upstream Workflows**: `WF-001 through WF-025`
- **REST / GraphQL APIs**: `Security Information and Event Management (SIEM), Forensic Query Engine`
- **Reporting Dashboards**: `Statutory DPDP & ISO 27001 Audit Compliance Ledger`
- **Analytical Warehousing**: `User Behavior Analytics (UBA) for Insider Threat Detection`
- **AI & Decision Support Models**: `Anomalous Data Access Detection Model`
- **Edge Synchronization**: `Edge-local append; guaranteed delivery push to central SIEM via encrypted queue`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL (WORM replication to S3 Object Lock)`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `CRITICAL (Zero truncation policy)`
- **Governing Data Quality Rules**: `DQ-041`
- **Data Lineage Traceability**: `LINEAGE-024`

### TABLE-051: `sync.offline_mutation_log`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-051`
- **Fully Qualified Name**: `sync.offline_mutation_log`
- **Functional Domain**: `Edge Offline Synchronization`
- **Executive Data Owner**: Edge Architecture Team
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-012`
- **Audit Requirements**: Sync conflict resolutions strictly logged with winning vector justification

#### 2. Business Purpose & Scope Description
**Operational Role**: Ordered journal of database mutations performed on clinic edge appliances during wide-area network outages.

Stores transaction sequence number, mutation payload JSONB, table name, operation (INSERT, UPDATE), conflict resolution vector, and cloud acknowledgment status.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Appended during offline operations; replayed to cloud upon connectivity restoration; purged after 180 days.
- **Estimated Storage Footprint**: Baseline capacity: `15,000,000 offline mutations`; Expected growth rate: `45,000 mutations/day across intermittent connections`.
- **Partitioning Architecture**: `Range partitioned by created_at (Monthly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Clinic edge appliance recording offline mutation |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-129` | B-tree | `(facility_id)` | High | `SELECT * FROM offline_mutation_log WHERE facility_id = $1` |
| `INDEX-130` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM offline_mutation_log WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `NFR-006, NFR-007, ARCH-OFF-01`
- **Upstream Workflows**: `WF-025`
- **REST / GraphQL APIs**: `Edge Synchronization Worker, Conflict Resolution Engine`
- **Reporting Dashboards**: `Clinic Network Connectivity & Sync Health Dashboard`
- **Analytical Warehousing**: `Edge Network Outage Duration Heatmap`
- **AI & Decision Support Models**: `None`
- **Edge Synchronization**: `Authoritative local edge journal; replicated to cloud reconciliation processor`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `HIGH`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-042`
- **Data Lineage Traceability**: `LINEAGE-025`

### TABLE-052: `sync.abdm_artifacts`

#### 1. Identification & Governance Profile

- **Table Identifier**: `TABLE-052`
- **Fully Qualified Name**: `sync.abdm_artifacts`
- **Functional Domain**: `National Interoperability`
- **Executive Data Owner**: ABDM Integration Lead
- **Primary Key Column**: `id` (PostgreSQL 128-bit `UUIDv7`)
- **Data Classification**: `CLASS-003` (Governed by DPDP Act 2023 & DISHA)
- **Statutory Retention Policy**: `RETENTION-005`
- **Audit Requirements**: ABDM gateway request/response exchange logged with cryptographic proof

#### 2. Business Purpose & Scope Description
**Operational Role**: Ayushman Bharat Digital Mission (ABDM) integration payloads, FHIR R4 document bundles, linking tokens, and consent transaction references.

Stores ABDM transaction ID, ABHA number linkage, FHIR Bundle JSONB, health information type (OPConsultation, Prescription, DiagnosticReport), and encryption key wrap.

#### 3. Operational Lifecycle & Volume Projections
- **Lifecycle Stages**: Created upon ABDM push/pull; retained 7 years per National Digital Health Mission standards.
- **Estimated Storage Footprint**: Baseline capacity: `12,000,000 FHIR bundles`; Expected growth rate: `35,000 artifacts/day`.
- **Partitioning Architecture**: `Range partitioned by created_at (Quarterly)`
- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.

#### 4. Foreign Key Relationships & Relational Dependencies

**Inbound Dependencies (Foreign Keys held by this table):**
| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `patients` | `id` | `RESTRICT` | ABDM FHIR artifacts linked to registered citizen |
| `facility_id` | `facilities` | `id` | `RESTRICT` | Healthcare facility sharing ABDM clinical bundle |

**Outbound Dependencies (Child tables referencing this table):**
*None (Leaf entity in domain dependency graph).*

#### 5. Indexing Architecture & Query Acceleration
The table features 2 dedicated indexes designed for high-selectivity retrieval:

| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |
| :--- | :--- | :--- | :--- | :--- |
| `INDEX-131` | B-tree | `(facility_id)` | High | `SELECT * FROM abdm_artifacts WHERE facility_id = $1` |
| `INDEX-132` | Composite B-tree | `(status, created_at)` | High | `SELECT * FROM abdm_artifacts WHERE status = $1 ORDER BY created_at DESC` |

#### 6. Ecosystem Consumer Systems & Data Flow
- **Upstream Requirements**: `INT-006, INT-007, FR-032`
- **Upstream Workflows**: `WF-015`
- **REST / GraphQL APIs**: `ABDM Milestone 1/2/3 Gateway, FHIR Bundle Converter`
- **Reporting Dashboards**: `National ABDM Integration Scorecard`
- **Analytical Warehousing**: `Inter-System Clinical Data Exchange Volume`
- **AI & Decision Support Models**: `FHIR Structural Validation Engine`
- **Edge Synchronization**: `Cloud-authoritative interoperability gateway`

#### 7. Reliability, Disaster Recovery & Data Quality
- **Backup Priority**: `CRITICAL`
- **Recovery Priority**: `Tier 1`
- **Migration Sensitivity**: `HIGH`
- **Governing Data Quality Rules**: `DQ-043`
- **Data Lineage Traceability**: `LINEAGE-005`

## 4. Conclusion & Cross-Catalog Verification

The 52 table profiles detailed above establish an exhaustive technical catalog. Every table is mapped to its exact schema, domain, owners, indexes, and downstream consumers without ambiguity. This catalog serves as the central operational guide for subsequent database administration and application development.
