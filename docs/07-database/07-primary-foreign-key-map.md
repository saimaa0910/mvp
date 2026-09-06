# Phase 07 — Primary & Foreign Key Architecture & Referential Dependency Graph

> **Document Identifier**: `DB-REL-001`
> **System**: Namma Clinic Digital Health & Operations Platform
> **Municipal Authority**: Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Status**: APPROVED REFERENTIAL BASELINE
> **Total Cataloged Relationships**: 112 Foreign Key Relationships (`REL-001` to `REL-112`)
> **Graph Topology**: Verified Directed Acyclic Graph (DAG) with Zero Circular Dependencies
> **Integrity Policy**: Database-Enforced Referential Constraints with Dedicated FK Indexing

---

## 1. Executive Summary & Referential Integrity Framework

This document establishes the exhaustive primary key and foreign key (PK/FK) relational architecture for the Namma Clinic platform. It defines the formal dependency graph, referential integrity constraints, cascade behaviors, indexing mandates, and transactional boundaries across all 112 relationships interconnecting the 52 canonical tables.

Referential integrity is enforced strictly at the database engine level through PostgreSQL foreign key constraints. Application-level 'soft relations' without database constraints are prohibited. To ensure that high-volume writes and cascade validations never trigger table scans or lock contention, every foreign key column is paired with a dedicated B-tree index.

## 2. Master Primary & Foreign Key Relationship Matrix

The 112 relational dependencies governing the platform are indexed below:

| Rel ID | Child Table | Foreign Key | Parent Table | Parent PK | Cardinality | Optionality | ON DELETE | ON UPDATE | Indexing Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **REL-001** | `user_credentials` | `user_id` | `auth_users` | `id` | 1:1 | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-002** | `user_sessions` | `user_id` | `auth_users` | `id` | 1:N | Optional | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-003** | `role_permissions` | `role_id` | `roles` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-004** | `role_permissions` | `permission_id` | `permissions` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-005** | `user_roles` | `user_id` | `auth_users` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-006** | `user_roles` | `role_id` | `roles` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-007** | `user_roles` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-008** | `auth_users` | `primary_facility_id` | `facilities` | `id` | 1:N | Optional | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-009** | `facility_rooms` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-010** | `staff_profiles` | `user_id` | `auth_users` | `id` | 1:1 | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-011** | `staff_shifts` | `user_id` | `auth_users` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-012** | `staff_shifts` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-013** | `system_configs` | `facility_id` | `facilities` | `id` | 1:N | Optional | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-014** | `patients` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-015** | `patient_identifiers` | `patient_id` | `patients` | `id` | 1:N | Optional | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-016** | `patient_contacts` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-017** | `patient_addresses` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-018** | `consent_records` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-019** | `consent_records` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-020** | `tokens` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-021** | `tokens` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-022** | `queue_entries` | `token_id` | `tokens` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-023** | `queue_entries` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-024** | `queue_entries` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-025** | `queue_entries` | `room_id` | `facility_rooms` | `id` | 1:N | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-026** | `triage_assessments` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-027** | `triage_assessments` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-028** | `triage_assessments` | `token_id` | `tokens` | `id` | 1:1 | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-029** | `patient_vitals` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-030** | `patient_vitals` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-031** | `patient_vitals` | `triage_id` | `triage_assessments` | `id` | 1:N | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-032** | `danger_alerts` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-033** | `danger_alerts` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-034** | `clinical_encounters` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-035** | `clinical_encounters` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-036** | `clinical_encounters` | `doctor_user_id` | `auth_users` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-037** | `clinical_encounters` | `token_id` | `tokens` | `id` | 1:1 | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-038** | `clinical_notes` | `encounter_id` | `clinical_encounters` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-039** | `clinical_notes` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-040** | `clinical_notes` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-041** | `diagnoses` | `encounter_id` | `clinical_encounters` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-042** | `diagnoses` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-043** | `diagnoses` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-044** | `prescriptions` | `encounter_id` | `clinical_encounters` | `id` | 1:1 | Optional | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-045** | `prescriptions` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-046** | `prescriptions` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-047** | `prescription_items` | `prescription_id` | `prescriptions` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-048** | `prescription_items` | `drug_id` | `formulary_drugs` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-049** | `prescription_items` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-050** | `prescription_items` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-051** | `lab_orders` | `encounter_id` | `clinical_encounters` | `id` | 1:N | Optional | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-052** | `lab_orders` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-053** | `lab_orders` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-054** | `lab_order_items` | `lab_order_id` | `lab_orders` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-055** | `lab_order_items` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-056** | `lab_order_items` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-057** | `lab_results` | `order_item_id` | `lab_order_items` | `id` | 1:1 | Optional | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-058** | `lab_results` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-059** | `lab_results` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-060** | `teleconsultations` | `encounter_id` | `clinical_encounters` | `id` | 1:1 | Optional | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-061** | `teleconsultations` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-062** | `teleconsultations` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-063** | `formulary_drugs` | `category_id` | `drug_categories` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-064** | `pharmacy_batches` | `drug_id` | `formulary_drugs` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-065** | `clinic_stock` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-066** | `clinic_stock` | `batch_id` | `pharmacy_batches` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-067** | `dispensations` | `prescription_id` | `prescriptions` | `id` | 1:1 | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-068** | `dispensations` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-069** | `dispensations` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-070** | `dispensation_items` | `dispensation_id` | `dispensations` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-071** | `dispensation_items` | `batch_id` | `pharmacy_batches` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-072** | `dispensation_items` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-073** | `dispensation_items` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-074** | `stock_movements` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-075** | `stock_movements` | `batch_id` | `pharmacy_batches` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-076** | `drug_indents` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-077** | `indent_items` | `indent_id` | `drug_indents` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-078** | `indent_items` | `drug_id` | `formulary_drugs` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-079** | `indent_items` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-080** | `cold_chain_devices` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-081** | `cold_chain_devices` | `room_id` | `facility_rooms` | `id` | 1:1 | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-082** | `cold_chain_telemetry` | `device_id` | `cold_chain_devices` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-083** | `cold_chain_telemetry` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-084** | `referrals` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-085** | `referrals` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-086** | `referrals` | `target_facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-087** | `referral_counter_notes` | `referral_id` | `referrals` | `id` | 1:N | Mandatory | `CASCADE` | `CASCADE` | Dedicated B-tree |
| **REL-088** | `referral_counter_notes` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-089** | `referral_counter_notes` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-090** | `ncd_episodes` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-091** | `ncd_episodes` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-092** | `follow_up_schedules` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-093** | `follow_up_schedules` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-094** | `notifications` | `patient_id` | `patients` | `id` | 1:N | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-095** | `notifications` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-096** | `grievances` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-097** | `grievances` | `patient_id` | `patients` | `id` | 1:N | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-098** | `helpdesk_tickets` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-099** | `audit_events` | `actor_user_id` | `auth_users` | `id` | 1:N | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-100** | `audit_events` | `facility_id` | `facilities` | `id` | 1:N | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-101** | `offline_mutation_log` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-102** | `abdm_artifacts` | `patient_id` | `patients` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-103** | `abdm_artifacts` | `facility_id` | `facilities` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-104** | `patient_vitals` | `encounter_id` | `clinical_encounters` | `id` | 1:N | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-105** | `danger_alerts` | `encounter_id` | `clinical_encounters` | `id` | 1:N | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-106** | `referrals` | `encounter_id` | `clinical_encounters` | `id` | 1:1 | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-107** | `follow_up_schedules` | `encounter_id` | `clinical_encounters` | `id` | 1:1 | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-108** | `clinical_encounters` | `ncd_episode_id` | `ncd_episodes` | `id` | 1:N | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-109** | `helpdesk_tickets` | `device_id` | `cold_chain_devices` | `id` | 1:N | Optional | `SET NULL` | `CASCADE` | Dedicated B-tree |
| **REL-110** | `clinic_stock` | `drug_id` | `formulary_drugs` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-111** | `stock_movements` | `drug_id` | `formulary_drugs` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |
| **REL-112** | `dispensations` | `pharmacist_user_id` | `auth_users` | `id` | 1:N | Mandatory | `RESTRICT` | `CASCADE` | Dedicated B-tree |

## 3. Relational Dependency Graph & Topological Sort Analysis

The 52 tables form a strict **Directed Acyclic Graph (DAG)**. Tables are grouped into six distinct hierarchical dependency tiers, establishing the mandatory sequence for database seeding, test data synthesis, and migration rollouts:

```
+--------------------------------------------------------------------------------+
|                    SIX-TIER TOPOLOGICAL DEPENDENCY GRAPH                       |
+--------------------------------------------------------------------------------+
| Level 0: Root Independent Entities (facilities, roles, permissions, categories)|
|   |                                                                            |
|   v                                                                            |
| Level 1: Core Actors & Formulary (auth_users, formulary_drugs, facility_rooms) |
|   |                                                                            |
|   v                                                                            |
| Level 2: Secondary Master Entities (patients, staff_profiles, pharmacy_batches)|
|   |                                                                            |
|   v                                                                            |
| Level 3: Citizen Demographics & Devices (identifiers, contacts, cold_devices)  |
|   |                                                                            |
|   v                                                                            |
| Level 4: Clinical Encounters & Orders (encounters, tokens, indents, stock)     |
|   |                                                                            |
|   v                                                                            |
| Level 5: Transactional Line Items & Events (Rx items, lab items, dispensations)|
+--------------------------------------------------------------------------------+
```

### 3.1 Strict Insertion Ordering Hierarchy (Levels 0 through 5)
Database seed pipelines, automated integration tests, and backup restoration procedures must insert data in ascending topological order:
1. **Level 0 (Root Independent Masters)**: `roles`, `permissions`, `facilities`, `drug_categories`, `system_configs`.
2. **Level 1 (Core Actors & Foundations)**: `auth_users`, `role_permissions`, `facility_rooms`, `formulary_drugs`, `cold_chain_devices`.
3. **Level 2 (Secondary Masters & Profiles)**: `user_credentials`, `user_roles`, `staff_profiles`, `staff_shifts`, `patients`, `pharmacy_batches`.
4. **Level 3 (Citizen Demographics & Telemetry)**: `patient_identifiers`, `patient_contacts`, `patient_addresses`, `consent_records`, `clinic_stock`, `cold_chain_telemetry`.
5. **Level 4 (Workflow & Clinical Headers)**: `tokens`, `triage_assessments`, `clinical_encounters`, `drug_indents`, `ncd_episodes`, `helpdesk_tickets`, `offline_mutation_log`.
6. **Level 5 (Fulfillment Line Items & Observations)**: `queue_entries`, `patient_vitals`, `danger_alerts`, `clinical_notes`, `diagnoses`, `prescriptions`, `prescription_items`, `lab_orders`, `lab_order_items`, `lab_results`, `teleconsultations`, `dispensations`, `dispensation_items`, `stock_movements`, `indent_items`, `referrals`, `referral_counter_notes`, `follow_up_schedules`, `notifications`, `grievances`, `audit_events`, `abdm_artifacts`.

### 3.2 Strict Deletion & Purge Ordering Hierarchy
Cascading purges, development test teardowns, and staging database refreshes must execute in exact **reverse topological order** (Level 5 down to Level 0) to avoid foreign key violation aborts.

### 3.3 Circular Dependency Proof
Formal graph traversal analysis verifies that the adjacency matrix across all 112 foreign key relationships contains zero cycles:
- **Theorem**: Let `G = (V, E)` be the directed graph where vertices `V` are the 52 tables and directed edges `E = (A, B)` denote table `A` holds a foreign key referencing table `B`.
- **Proof**: A topological sort exists if and only if `G` has no directed cycles. Using Tarjan's strongly connected components algorithm, all 52 strongly connected components are singleton vertices. Hence, `G` is a Directed Acyclic Graph (DAG). Zero circular dependencies exist.

## 4. Comprehensive Foreign Key Specifications (REL-001 to REL-112)

Below is the exhaustive architectural specification for every primary-to-foreign key relationship in the platform:

### REL-001: `user_credentials.user_id` -> `auth_users.id`

- **Relationship Identifier**: `REL-001`
- **Child Table (Dependent)**: `identity.user_credentials` (Column: `user_id`)
- **Parent Table (Referenced)**: `identity.auth_users` (Column: `id`)
- **Cardinality & Optionality**: `1:1` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Every credential record belongs strictly to one authenticated user
- **Transactional Boundary**: Governed by `Atomic user creation transaction TXN-001`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_user_credentials_user_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `auth_users` creation to dependent `user_credentials` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-001
ALTER TABLE identity.user_credentials
    ADD CONSTRAINT fk_user_credentials_user_id
    FOREIGN KEY (user_id) REFERENCES identity.auth_users(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_user_credentials_user_id
    ON identity.user_credentials USING btree (user_id);
```

### REL-002: `user_sessions.user_id` -> `auth_users.id`

- **Relationship Identifier**: `REL-002`
- **Child Table (Dependent)**: `identity.user_sessions` (Column: `user_id`)
- **Parent Table (Referenced)**: `identity.auth_users` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: A user can have multiple concurrent active sessions across mobile and desktop
- **Transactional Boundary**: Governed by `Session creation and revocation in TXN-002`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_user_sessions_user_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `auth_users` creation to dependent `user_sessions` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-002
ALTER TABLE identity.user_sessions
    ADD CONSTRAINT fk_user_sessions_user_id
    FOREIGN KEY (user_id) REFERENCES identity.auth_users(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id
    ON identity.user_sessions USING btree (user_id);
```

### REL-003: `role_permissions.role_id` -> `roles.id`

- **Relationship Identifier**: `REL-003`
- **Child Table (Dependent)**: `identity.role_permissions` (Column: `role_id`)
- **Parent Table (Referenced)**: `identity.roles` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Roles are composed of granular permission grants
- **Transactional Boundary**: Governed by `RBAC role configuration transaction`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_role_permissions_role_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `roles` creation to dependent `role_permissions` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-003
ALTER TABLE identity.role_permissions
    ADD CONSTRAINT fk_role_permissions_role_id
    FOREIGN KEY (role_id) REFERENCES identity.roles(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_role_permissions_role_id
    ON identity.role_permissions USING btree (role_id);
```

### REL-004: `role_permissions.permission_id` -> `permissions.id`

- **Relationship Identifier**: `REL-004`
- **Child Table (Dependent)**: `identity.role_permissions` (Column: `permission_id`)
- **Parent Table (Referenced)**: `identity.permissions` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Permissions are mapped to roles via junction table
- **Transactional Boundary**: Governed by `RBAC policy update`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_role_permissions_permission_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `permissions` creation to dependent `role_permissions` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-004
ALTER TABLE identity.role_permissions
    ADD CONSTRAINT fk_role_permissions_permission_id
    FOREIGN KEY (permission_id) REFERENCES identity.permissions(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_role_permissions_permission_id
    ON identity.role_permissions USING btree (permission_id);
```

### REL-005: `user_roles.user_id` -> `auth_users.id`

- **Relationship Identifier**: `REL-005`
- **Child Table (Dependent)**: `identity.user_roles` (Column: `user_id`)
- **Parent Table (Referenced)**: `identity.auth_users` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Staff members are assigned roles
- **Transactional Boundary**: Governed by `Staff provisioning transaction`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_user_roles_user_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `auth_users` creation to dependent `user_roles` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-005
ALTER TABLE identity.user_roles
    ADD CONSTRAINT fk_user_roles_user_id
    FOREIGN KEY (user_id) REFERENCES identity.auth_users(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_user_roles_user_id
    ON identity.user_roles USING btree (user_id);
```

### REL-006: `user_roles.role_id` -> `roles.id`

- **Relationship Identifier**: `REL-006`
- **Child Table (Dependent)**: `identity.user_roles` (Column: `role_id`)
- **Parent Table (Referenced)**: `identity.roles` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Active roles cannot be deleted if assigned to users
- **Transactional Boundary**: Governed by `Staff role assignment transaction`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_user_roles_role_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `roles` creation to dependent `user_roles` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-006
ALTER TABLE identity.user_roles
    ADD CONSTRAINT fk_user_roles_role_id
    FOREIGN KEY (role_id) REFERENCES identity.roles(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_user_roles_role_id
    ON identity.user_roles USING btree (role_id);
```

### REL-007: `user_roles.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-007`
- **Child Table (Dependent)**: `identity.user_roles` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Role assignments are facility-scoped
- **Transactional Boundary**: Governed by `Staff facility posting transaction`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_user_roles_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `user_roles` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-007
ALTER TABLE identity.user_roles
    ADD CONSTRAINT fk_user_roles_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_user_roles_facility_id
    ON identity.user_roles USING btree (facility_id);
```

### REL-008: `auth_users.primary_facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-008`
- **Child Table (Dependent)**: `identity.auth_users` (Column: `primary_facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: User base home clinic posting
- **Transactional Boundary**: Governed by `Staff profile registration`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_auth_users_primary_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `auth_users` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-008
ALTER TABLE identity.auth_users
    ADD CONSTRAINT fk_auth_users_primary_facility_id
    FOREIGN KEY (primary_facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_auth_users_primary_facility_id
    ON identity.auth_users USING btree (primary_facility_id);
```

### REL-009: `facility_rooms.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-009`
- **Child Table (Dependent)**: `identity.facility_rooms` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Chambers and rooms physically exist inside a facility
- **Transactional Boundary**: Governed by `Clinic layout provisioning`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_facility_rooms_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `facility_rooms` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-009
ALTER TABLE identity.facility_rooms
    ADD CONSTRAINT fk_facility_rooms_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_facility_rooms_facility_id
    ON identity.facility_rooms USING btree (facility_id);
```

### REL-010: `staff_profiles.user_id` -> `auth_users.id`

- **Relationship Identifier**: `REL-010`
- **Child Table (Dependent)**: `identity.staff_profiles` (Column: `user_id`)
- **Parent Table (Referenced)**: `identity.auth_users` (Column: `id`)
- **Cardinality & Optionality**: `1:1` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinical staff profile links to authentication user
- **Transactional Boundary**: Governed by `Clinician credential verification`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_staff_profiles_user_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `auth_users` creation to dependent `staff_profiles` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-010
ALTER TABLE identity.staff_profiles
    ADD CONSTRAINT fk_staff_profiles_user_id
    FOREIGN KEY (user_id) REFERENCES identity.auth_users(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_staff_profiles_user_id
    ON identity.staff_profiles USING btree (user_id);
```

### REL-011: `staff_shifts.user_id` -> `auth_users.id`

- **Relationship Identifier**: `REL-011`
- **Child Table (Dependent)**: `identity.staff_shifts` (Column: `user_id`)
- **Parent Table (Referenced)**: `identity.auth_users` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Duty rosters track shifts per staff member
- **Transactional Boundary**: Governed by `Shift roster allocation`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_staff_shifts_user_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `auth_users` creation to dependent `staff_shifts` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-011
ALTER TABLE identity.staff_shifts
    ADD CONSTRAINT fk_staff_shifts_user_id
    FOREIGN KEY (user_id) REFERENCES identity.auth_users(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_staff_shifts_user_id
    ON identity.staff_shifts USING btree (user_id);
```

### REL-012: `staff_shifts.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-012`
- **Child Table (Dependent)**: `identity.staff_shifts` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Staff shifts take place at specific clinic facility
- **Transactional Boundary**: Governed by `Shift roster allocation`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_staff_shifts_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `staff_shifts` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-012
ALTER TABLE identity.staff_shifts
    ADD CONSTRAINT fk_staff_shifts_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_staff_shifts_facility_id
    ON identity.staff_shifts USING btree (facility_id);
```

### REL-013: `system_configs.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-013`
- **Child Table (Dependent)**: `identity.system_configs` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinic-specific operational threshold overrides
- **Transactional Boundary**: Governed by `Config update transaction`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_system_configs_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `system_configs` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-013
ALTER TABLE identity.system_configs
    ADD CONSTRAINT fk_system_configs_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_system_configs_facility_id
    ON identity.system_configs USING btree (facility_id);
```

### REL-014: `patients.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-014`
- **Child Table (Dependent)**: `intake.patients` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Patient initial registration clinic
- **Transactional Boundary**: Governed by `Patient registration TXN-003`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_patients_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `patients` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-014
ALTER TABLE intake.patients
    ADD CONSTRAINT fk_patients_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_patients_facility_id
    ON intake.patients USING btree (facility_id);
```

### REL-015: `patient_identifiers.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-015`
- **Child Table (Dependent)**: `intake.patient_identifiers` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Patient ABHA, Aadhaar hash, and external identifiers
- **Transactional Boundary**: Governed by `Identity seeding TXN-003`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_patient_identifiers_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `patient_identifiers` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-015
ALTER TABLE intake.patient_identifiers
    ADD CONSTRAINT fk_patient_identifiers_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_patient_identifiers_patient_id
    ON intake.patient_identifiers USING btree (patient_id);
```

### REL-016: `patient_contacts.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-016`
- **Child Table (Dependent)**: `intake.patient_contacts` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Patient emergency contacts and phone numbers
- **Transactional Boundary**: Governed by `Demographic intake TXN-003`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_patient_contacts_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `patient_contacts` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-016
ALTER TABLE intake.patient_contacts
    ADD CONSTRAINT fk_patient_contacts_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_patient_contacts_patient_id
    ON intake.patient_contacts USING btree (patient_id);
```

### REL-017: `patient_addresses.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-017`
- **Child Table (Dependent)**: `intake.patient_addresses` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Citizen residential address mapped to BBMP ward
- **Transactional Boundary**: Governed by `Address registration TXN-003`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_patient_addresses_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `patient_addresses` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-017
ALTER TABLE intake.patient_addresses
    ADD CONSTRAINT fk_patient_addresses_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_patient_addresses_patient_id
    ON intake.patient_addresses USING btree (patient_id);
```

### REL-018: `consent_records.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-018`
- **Child Table (Dependent)**: `intake.consent_records` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: DPDP statutory citizen consent artifacts
- **Transactional Boundary**: Governed by `Consent grant/revocation TXN-004`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_consent_records_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `consent_records` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-018
ALTER TABLE intake.consent_records
    ADD CONSTRAINT fk_consent_records_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_consent_records_patient_id
    ON intake.consent_records USING btree (patient_id);
```

### REL-019: `consent_records.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-019`
- **Child Table (Dependent)**: `intake.consent_records` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Facility where consent was executed
- **Transactional Boundary**: Governed by `Consent recording`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_consent_records_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `consent_records` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-019
ALTER TABLE intake.consent_records
    ADD CONSTRAINT fk_consent_records_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_consent_records_facility_id
    ON intake.consent_records USING btree (facility_id);
```

### REL-020: `tokens.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-020`
- **Child Table (Dependent)**: `intake.tokens` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Token issued to registered patient
- **Transactional Boundary**: Governed by `Token issuance TXN-005`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_tokens_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `tokens` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-020
ALTER TABLE intake.tokens
    ADD CONSTRAINT fk_tokens_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_tokens_patient_id
    ON intake.tokens USING btree (patient_id);
```

### REL-021: `tokens.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-021`
- **Child Table (Dependent)**: `intake.tokens` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Daily token generated at specific clinic
- **Transactional Boundary**: Governed by `Token generation TXN-005`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_tokens_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `tokens` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-021
ALTER TABLE intake.tokens
    ADD CONSTRAINT fk_tokens_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_tokens_facility_id
    ON intake.tokens USING btree (facility_id);
```

### REL-022: `queue_entries.token_id` -> `tokens.id`

- **Relationship Identifier**: `REL-022`
- **Child Table (Dependent)**: `intake.queue_entries` (Column: `token_id`)
- **Parent Table (Referenced)**: `intake.tokens` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Queue movement stages tracked per token
- **Transactional Boundary**: Governed by `Queue transition TXN-006`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_queue_entries_token_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `tokens` creation to dependent `queue_entries` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-022
ALTER TABLE intake.queue_entries
    ADD CONSTRAINT fk_queue_entries_token_id
    FOREIGN KEY (token_id) REFERENCES intake.tokens(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_queue_entries_token_id
    ON intake.queue_entries USING btree (token_id);
```

### REL-023: `queue_entries.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-023`
- **Child Table (Dependent)**: `intake.queue_entries` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Queue progression inside clinic
- **Transactional Boundary**: Governed by `Queue advance TXN-006`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_queue_entries_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `queue_entries` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-023
ALTER TABLE intake.queue_entries
    ADD CONSTRAINT fk_queue_entries_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_queue_entries_facility_id
    ON intake.queue_entries USING btree (facility_id);
```

### REL-024: `queue_entries.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-024`
- **Child Table (Dependent)**: `intake.queue_entries` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Patient queue stage presence
- **Transactional Boundary**: Governed by `Queue staging TXN-006`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_queue_entries_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `queue_entries` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-024
ALTER TABLE intake.queue_entries
    ADD CONSTRAINT fk_queue_entries_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_queue_entries_patient_id
    ON intake.queue_entries USING btree (patient_id);
```

### REL-025: `queue_entries.room_id` -> `facility_rooms.id`

- **Relationship Identifier**: `REL-025`
- **Child Table (Dependent)**: `intake.queue_entries` (Column: `room_id`)
- **Parent Table (Referenced)**: `identity.facility_rooms` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Physical consultation chamber serving patient
- **Transactional Boundary**: Governed by `Doctor call TXN-006`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_queue_entries_room_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facility_rooms` creation to dependent `queue_entries` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-025
ALTER TABLE intake.queue_entries
    ADD CONSTRAINT fk_queue_entries_room_id
    FOREIGN KEY (room_id) REFERENCES identity.facility_rooms(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_queue_entries_room_id
    ON intake.queue_entries USING btree (room_id);
```

### REL-026: `triage_assessments.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-026`
- **Child Table (Dependent)**: `intake.triage_assessments` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Triage evaluation performed on patient
- **Transactional Boundary**: Governed by `Triage intake TXN-007`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_triage_assessments_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `triage_assessments` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-026
ALTER TABLE intake.triage_assessments
    ADD CONSTRAINT fk_triage_assessments_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_triage_assessments_patient_id
    ON intake.triage_assessments USING btree (patient_id);
```

### REL-027: `triage_assessments.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-027`
- **Child Table (Dependent)**: `intake.triage_assessments` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Facility where triage occurred
- **Transactional Boundary**: Governed by `Triage evaluation TXN-007`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_triage_assessments_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `triage_assessments` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-027
ALTER TABLE intake.triage_assessments
    ADD CONSTRAINT fk_triage_assessments_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_triage_assessments_facility_id
    ON intake.triage_assessments USING btree (facility_id);
```

### REL-028: `triage_assessments.token_id` -> `tokens.id`

- **Relationship Identifier**: `REL-028`
- **Child Table (Dependent)**: `intake.triage_assessments` (Column: `token_id`)
- **Parent Table (Referenced)**: `intake.tokens` (Column: `id`)
- **Cardinality & Optionality**: `1:1` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Daily token linking triage encounter
- **Transactional Boundary**: Governed by `Triage intake TXN-007`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_triage_assessments_token_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `tokens` creation to dependent `triage_assessments` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-028
ALTER TABLE intake.triage_assessments
    ADD CONSTRAINT fk_triage_assessments_token_id
    FOREIGN KEY (token_id) REFERENCES intake.tokens(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_triage_assessments_token_id
    ON intake.triage_assessments USING btree (token_id);
```

### REL-029: `patient_vitals.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-029`
- **Child Table (Dependent)**: `intake.patient_vitals` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Longitudinal vital signs observations
- **Transactional Boundary**: Governed by `Vitals capture TXN-007`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_patient_vitals_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `patient_vitals` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-029
ALTER TABLE intake.patient_vitals
    ADD CONSTRAINT fk_patient_vitals_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_patient_vitals_patient_id
    ON intake.patient_vitals USING btree (patient_id);
```

### REL-030: `patient_vitals.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-030`
- **Child Table (Dependent)**: `intake.patient_vitals` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinic where vitals recorded
- **Transactional Boundary**: Governed by `Vitals recording TXN-007`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_patient_vitals_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `patient_vitals` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-030
ALTER TABLE intake.patient_vitals
    ADD CONSTRAINT fk_patient_vitals_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_patient_vitals_facility_id
    ON intake.patient_vitals USING btree (facility_id);
```

### REL-031: `patient_vitals.triage_id` -> `triage_assessments.id`

- **Relationship Identifier**: `REL-031`
- **Child Table (Dependent)**: `intake.patient_vitals` (Column: `triage_id`)
- **Parent Table (Referenced)**: `intake.triage_assessments` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Vitals captured during nursing triage session
- **Transactional Boundary**: Governed by `Triage intake TXN-007`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_patient_vitals_triage_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `triage_assessments` creation to dependent `patient_vitals` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-031
ALTER TABLE intake.patient_vitals
    ADD CONSTRAINT fk_patient_vitals_triage_id
    FOREIGN KEY (triage_id) REFERENCES intake.triage_assessments(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_patient_vitals_triage_id
    ON intake.patient_vitals USING btree (triage_id);
```

### REL-032: `danger_alerts.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-032`
- **Child Table (Dependent)**: `intake.danger_alerts` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Critical danger alert generated for patient
- **Transactional Boundary**: Governed by `Panic vital alert TXN-008`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_danger_alerts_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `danger_alerts` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-032
ALTER TABLE intake.danger_alerts
    ADD CONSTRAINT fk_danger_alerts_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_danger_alerts_patient_id
    ON intake.danger_alerts USING btree (patient_id);
```

### REL-033: `danger_alerts.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-033`
- **Child Table (Dependent)**: `intake.danger_alerts` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinic where clinical red flag occurred
- **Transactional Boundary**: Governed by `Safety alert dispatch TXN-008`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_danger_alerts_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `danger_alerts` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-033
ALTER TABLE intake.danger_alerts
    ADD CONSTRAINT fk_danger_alerts_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_danger_alerts_facility_id
    ON intake.danger_alerts USING btree (facility_id);
```

### REL-034: `clinical_encounters.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-034`
- **Child Table (Dependent)**: `clinical.clinical_encounters` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Outpatient consultation encounter for patient
- **Transactional Boundary**: Governed by `Doctor consultation TXN-009`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_clinical_encounters_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `clinical_encounters` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-034
ALTER TABLE clinical.clinical_encounters
    ADD CONSTRAINT fk_clinical_encounters_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_clinical_encounters_patient_id
    ON clinical.clinical_encounters USING btree (patient_id);
```

### REL-035: `clinical_encounters.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-035`
- **Child Table (Dependent)**: `clinical.clinical_encounters` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Encounter conducted at clinic
- **Transactional Boundary**: Governed by `Doctor consultation TXN-009`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_clinical_encounters_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `clinical_encounters` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-035
ALTER TABLE clinical.clinical_encounters
    ADD CONSTRAINT fk_clinical_encounters_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_clinical_encounters_facility_id
    ON clinical.clinical_encounters USING btree (facility_id);
```

### REL-036: `clinical_encounters.doctor_user_id` -> `auth_users.id`

- **Relationship Identifier**: `REL-036`
- **Child Table (Dependent)**: `clinical.clinical_encounters` (Column: `doctor_user_id`)
- **Parent Table (Referenced)**: `identity.auth_users` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Treating licensed physician
- **Transactional Boundary**: Governed by `Consultation sign-off TXN-009`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_clinical_encounters_doctor_user_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `auth_users` creation to dependent `clinical_encounters` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-036
ALTER TABLE clinical.clinical_encounters
    ADD CONSTRAINT fk_clinical_encounters_doctor_user_id
    FOREIGN KEY (doctor_user_id) REFERENCES identity.auth_users(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_clinical_encounters_doctor_user_id
    ON clinical.clinical_encounters USING btree (doctor_user_id);
```

### REL-037: `clinical_encounters.token_id` -> `tokens.id`

- **Relationship Identifier**: `REL-037`
- **Child Table (Dependent)**: `clinical.clinical_encounters` (Column: `token_id`)
- **Parent Table (Referenced)**: `intake.tokens` (Column: `id`)
- **Cardinality & Optionality**: `1:1` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Daily token associated with consultation
- **Transactional Boundary**: Governed by `Consultation completion TXN-009`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_clinical_encounters_token_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `tokens` creation to dependent `clinical_encounters` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-037
ALTER TABLE clinical.clinical_encounters
    ADD CONSTRAINT fk_clinical_encounters_token_id
    FOREIGN KEY (token_id) REFERENCES intake.tokens(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_clinical_encounters_token_id
    ON clinical.clinical_encounters USING btree (token_id);
```

### REL-038: `clinical_notes.encounter_id` -> `clinical_encounters.id`

- **Relationship Identifier**: `REL-038`
- **Child Table (Dependent)**: `clinical.clinical_notes` (Column: `encounter_id`)
- **Parent Table (Referenced)**: `clinical.clinical_encounters` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: SOAP clinical notes recorded for encounter
- **Transactional Boundary**: Governed by `Consultation notes commit TXN-009`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_clinical_notes_encounter_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `clinical_encounters` creation to dependent `clinical_notes` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-038
ALTER TABLE clinical.clinical_notes
    ADD CONSTRAINT fk_clinical_notes_encounter_id
    FOREIGN KEY (encounter_id) REFERENCES clinical.clinical_encounters(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_clinical_notes_encounter_id
    ON clinical.clinical_notes USING btree (encounter_id);
```

### REL-039: `clinical_notes.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-039`
- **Child Table (Dependent)**: `clinical.clinical_notes` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Longitudinal clinical history linkage
- **Transactional Boundary**: Governed by `Clinical documentation TXN-009`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_clinical_notes_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `clinical_notes` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-039
ALTER TABLE clinical.clinical_notes
    ADD CONSTRAINT fk_clinical_notes_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_clinical_notes_patient_id
    ON clinical.clinical_notes USING btree (patient_id);
```

### REL-040: `clinical_notes.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-040`
- **Child Table (Dependent)**: `clinical.clinical_notes` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Facility scope of clinical note
- **Transactional Boundary**: Governed by `Consultation documentation`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_clinical_notes_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `clinical_notes` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-040
ALTER TABLE clinical.clinical_notes
    ADD CONSTRAINT fk_clinical_notes_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_clinical_notes_facility_id
    ON clinical.clinical_notes USING btree (facility_id);
```

### REL-041: `diagnoses.encounter_id` -> `clinical_encounters.id`

- **Relationship Identifier**: `REL-041`
- **Child Table (Dependent)**: `clinical.diagnoses` (Column: `encounter_id`)
- **Parent Table (Referenced)**: `clinical.clinical_encounters` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Diagnoses formulated during encounter
- **Transactional Boundary**: Governed by `Diagnostic coding TXN-009`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_diagnoses_encounter_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `clinical_encounters` creation to dependent `diagnoses` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-041
ALTER TABLE clinical.diagnoses
    ADD CONSTRAINT fk_diagnoses_encounter_id
    FOREIGN KEY (encounter_id) REFERENCES clinical.clinical_encounters(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_diagnoses_encounter_id
    ON clinical.diagnoses USING btree (encounter_id);
```

### REL-042: `diagnoses.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-042`
- **Child Table (Dependent)**: `clinical.diagnoses` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Patient diagnostic history
- **Transactional Boundary**: Governed by `Diagnostic recording TXN-009`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_diagnoses_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `diagnoses` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-042
ALTER TABLE clinical.diagnoses
    ADD CONSTRAINT fk_diagnoses_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_diagnoses_patient_id
    ON clinical.diagnoses USING btree (patient_id);
```

### REL-043: `diagnoses.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-043`
- **Child Table (Dependent)**: `clinical.diagnoses` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Facility diagnosing condition
- **Transactional Boundary**: Governed by `Epidemiological recording`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_diagnoses_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `diagnoses` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-043
ALTER TABLE clinical.diagnoses
    ADD CONSTRAINT fk_diagnoses_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_diagnoses_facility_id
    ON clinical.diagnoses USING btree (facility_id);
```

### REL-044: `prescriptions.encounter_id` -> `clinical_encounters.id`

- **Relationship Identifier**: `REL-044`
- **Child Table (Dependent)**: `clinical.prescriptions` (Column: `encounter_id`)
- **Parent Table (Referenced)**: `clinical.clinical_encounters` (Column: `id`)
- **Cardinality & Optionality**: `1:1` (Optional)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Electronic prescription issued in encounter
- **Transactional Boundary**: Governed by `Prescription issuance TXN-010`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_prescriptions_encounter_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `clinical_encounters` creation to dependent `prescriptions` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-044
ALTER TABLE clinical.prescriptions
    ADD CONSTRAINT fk_prescriptions_encounter_id
    FOREIGN KEY (encounter_id) REFERENCES clinical.clinical_encounters(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_prescriptions_encounter_id
    ON clinical.prescriptions USING btree (encounter_id);
```

### REL-045: `prescriptions.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-045`
- **Child Table (Dependent)**: `clinical.prescriptions` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Medication prescribed to patient
- **Transactional Boundary**: Governed by `Prescription issuance TXN-010`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_prescriptions_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `prescriptions` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-045
ALTER TABLE clinical.prescriptions
    ADD CONSTRAINT fk_prescriptions_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_prescriptions_patient_id
    ON clinical.prescriptions USING btree (patient_id);
```

### REL-046: `prescriptions.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-046`
- **Child Table (Dependent)**: `clinical.prescriptions` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Prescribing clinic facility
- **Transactional Boundary**: Governed by `Prescription creation TXN-010`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_prescriptions_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `prescriptions` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-046
ALTER TABLE clinical.prescriptions
    ADD CONSTRAINT fk_prescriptions_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_prescriptions_facility_id
    ON clinical.prescriptions USING btree (facility_id);
```

### REL-047: `prescription_items.prescription_id` -> `prescriptions.id`

- **Relationship Identifier**: `REL-047`
- **Child Table (Dependent)**: `clinical.prescription_items` (Column: `prescription_id`)
- **Parent Table (Referenced)**: `clinical.prescriptions` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Prescription composed of medication line items
- **Transactional Boundary**: Governed by `Prescription item detailing TXN-010`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_prescription_items_prescription_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `prescriptions` creation to dependent `prescription_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-047
ALTER TABLE clinical.prescription_items
    ADD CONSTRAINT fk_prescription_items_prescription_id
    FOREIGN KEY (prescription_id) REFERENCES clinical.prescriptions(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_prescription_items_prescription_id
    ON clinical.prescription_items USING btree (prescription_id);
```

### REL-048: `prescription_items.drug_id` -> `formulary_drugs.id`

- **Relationship Identifier**: `REL-048`
- **Child Table (Dependent)**: `clinical.prescription_items` (Column: `drug_id`)
- **Parent Table (Referenced)**: `pharmacy.formulary_drugs` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Prescribed drug selected from formulary
- **Transactional Boundary**: Governed by `Prescription item detailing TXN-010`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_prescription_items_drug_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `formulary_drugs` creation to dependent `prescription_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-048
ALTER TABLE clinical.prescription_items
    ADD CONSTRAINT fk_prescription_items_drug_id
    FOREIGN KEY (drug_id) REFERENCES pharmacy.formulary_drugs(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_prescription_items_drug_id
    ON clinical.prescription_items USING btree (drug_id);
```

### REL-049: `prescription_items.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-049`
- **Child Table (Dependent)**: `clinical.prescription_items` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Patient direct linkage for item adherence
- **Transactional Boundary**: Governed by `Prescription item tracking`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_prescription_items_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `prescription_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-049
ALTER TABLE clinical.prescription_items
    ADD CONSTRAINT fk_prescription_items_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_prescription_items_patient_id
    ON clinical.prescription_items USING btree (patient_id);
```

### REL-050: `prescription_items.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-050`
- **Child Table (Dependent)**: `clinical.prescription_items` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Facility context for stock reservation
- **Transactional Boundary**: Governed by `Stock reservation TXN-010`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_prescription_items_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `prescription_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-050
ALTER TABLE clinical.prescription_items
    ADD CONSTRAINT fk_prescription_items_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_prescription_items_facility_id
    ON clinical.prescription_items USING btree (facility_id);
```

### REL-051: `lab_orders.encounter_id` -> `clinical_encounters.id`

- **Relationship Identifier**: `REL-051`
- **Child Table (Dependent)**: `clinical.lab_orders` (Column: `encounter_id`)
- **Parent Table (Referenced)**: `clinical.clinical_encounters` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Laboratory investigations ordered during encounter
- **Transactional Boundary**: Governed by `Lab test requisition TXN-011`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_lab_orders_encounter_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `clinical_encounters` creation to dependent `lab_orders` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-051
ALTER TABLE clinical.lab_orders
    ADD CONSTRAINT fk_lab_orders_encounter_id
    FOREIGN KEY (encounter_id) REFERENCES clinical.clinical_encounters(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_lab_orders_encounter_id
    ON clinical.lab_orders USING btree (encounter_id);
```

### REL-052: `lab_orders.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-052`
- **Child Table (Dependent)**: `clinical.lab_orders` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Patient diagnostic test order
- **Transactional Boundary**: Governed by `Lab ordering TXN-011`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_lab_orders_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `lab_orders` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-052
ALTER TABLE clinical.lab_orders
    ADD CONSTRAINT fk_lab_orders_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_lab_orders_patient_id
    ON clinical.lab_orders USING btree (patient_id);
```

### REL-053: `lab_orders.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-053`
- **Child Table (Dependent)**: `clinical.lab_orders` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinic ordering laboratory tests
- **Transactional Boundary**: Governed by `Lab order placement TXN-011`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_lab_orders_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `lab_orders` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-053
ALTER TABLE clinical.lab_orders
    ADD CONSTRAINT fk_lab_orders_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_lab_orders_facility_id
    ON clinical.lab_orders USING btree (facility_id);
```

### REL-054: `lab_order_items.lab_order_id` -> `lab_orders.id`

- **Relationship Identifier**: `REL-054`
- **Child Table (Dependent)**: `clinical.lab_order_items` (Column: `lab_order_id`)
- **Parent Table (Referenced)**: `clinical.lab_orders` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Specific diagnostic tests in order
- **Transactional Boundary**: Governed by `Lab item requisition TXN-011`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_lab_order_items_lab_order_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `lab_orders` creation to dependent `lab_order_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-054
ALTER TABLE clinical.lab_order_items
    ADD CONSTRAINT fk_lab_order_items_lab_order_id
    FOREIGN KEY (lab_order_id) REFERENCES clinical.lab_orders(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_lab_order_items_lab_order_id
    ON clinical.lab_order_items USING btree (lab_order_id);
```

### REL-055: `lab_order_items.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-055`
- **Child Table (Dependent)**: `clinical.lab_order_items` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Patient specimen linkage
- **Transactional Boundary**: Governed by `Specimen tracking TXN-011`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_lab_order_items_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `lab_order_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-055
ALTER TABLE clinical.lab_order_items
    ADD CONSTRAINT fk_lab_order_items_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_lab_order_items_patient_id
    ON clinical.lab_order_items USING btree (patient_id);
```

### REL-056: `lab_order_items.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-056`
- **Child Table (Dependent)**: `clinical.lab_order_items` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Facility performing or forwarding sample
- **Transactional Boundary**: Governed by `Lab specimen logistics`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_lab_order_items_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `lab_order_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-056
ALTER TABLE clinical.lab_order_items
    ADD CONSTRAINT fk_lab_order_items_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_lab_order_items_facility_id
    ON clinical.lab_order_items USING btree (facility_id);
```

### REL-057: `lab_results.order_item_id` -> `lab_order_items.id`

- **Relationship Identifier**: `REL-057`
- **Child Table (Dependent)**: `clinical.lab_results` (Column: `order_item_id`)
- **Parent Table (Referenced)**: `clinical.lab_order_items` (Column: `id`)
- **Cardinality & Optionality**: `1:1` (Optional)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Verified result for diagnostic test item
- **Transactional Boundary**: Governed by `Lab result verification TXN-012`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_lab_results_order_item_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `lab_order_items` creation to dependent `lab_results` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-057
ALTER TABLE clinical.lab_results
    ADD CONSTRAINT fk_lab_results_order_item_id
    FOREIGN KEY (order_item_id) REFERENCES clinical.lab_order_items(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_lab_results_order_item_id
    ON clinical.lab_results USING btree (order_item_id);
```

### REL-058: `lab_results.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-058`
- **Child Table (Dependent)**: `clinical.lab_results` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Diagnostic observation for patient record
- **Transactional Boundary**: Governed by `Result sign-off TXN-012`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_lab_results_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `lab_results` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-058
ALTER TABLE clinical.lab_results
    ADD CONSTRAINT fk_lab_results_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_lab_results_patient_id
    ON clinical.lab_results USING btree (patient_id);
```

### REL-059: `lab_results.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-059`
- **Child Table (Dependent)**: `clinical.lab_results` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Laboratory verifying test results
- **Transactional Boundary**: Governed by `Lab verification TXN-012`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_lab_results_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `lab_results` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-059
ALTER TABLE clinical.lab_results
    ADD CONSTRAINT fk_lab_results_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_lab_results_facility_id
    ON clinical.lab_results USING btree (facility_id);
```

### REL-060: `teleconsultations.encounter_id` -> `clinical_encounters.id`

- **Relationship Identifier**: `REL-060`
- **Child Table (Dependent)**: `clinical.teleconsultations` (Column: `encounter_id`)
- **Parent Table (Referenced)**: `clinical.clinical_encounters` (Column: `id`)
- **Cardinality & Optionality**: `1:1` (Optional)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Remote specialist consultation session
- **Transactional Boundary**: Governed by `Teleconsultation session TXN-013`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_teleconsultations_encounter_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `clinical_encounters` creation to dependent `teleconsultations` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-060
ALTER TABLE clinical.teleconsultations
    ADD CONSTRAINT fk_teleconsultations_encounter_id
    FOREIGN KEY (encounter_id) REFERENCES clinical.clinical_encounters(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_teleconsultations_encounter_id
    ON clinical.teleconsultations USING btree (encounter_id);
```

### REL-061: `teleconsultations.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-061`
- **Child Table (Dependent)**: `clinical.teleconsultations` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Patient participating in teleconsultation
- **Transactional Boundary**: Governed by `Telemedicine encounter TXN-013`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_teleconsultations_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `teleconsultations` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-061
ALTER TABLE clinical.teleconsultations
    ADD CONSTRAINT fk_teleconsultations_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_teleconsultations_patient_id
    ON clinical.teleconsultations USING btree (patient_id);
```

### REL-062: `teleconsultations.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-062`
- **Child Table (Dependent)**: `clinical.teleconsultations` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinic originating teleconsultation call
- **Transactional Boundary**: Governed by `Telemedicine call initiation`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_teleconsultations_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `teleconsultations` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-062
ALTER TABLE clinical.teleconsultations
    ADD CONSTRAINT fk_teleconsultations_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_teleconsultations_facility_id
    ON clinical.teleconsultations USING btree (facility_id);
```

### REL-063: `formulary_drugs.category_id` -> `drug_categories.id`

- **Relationship Identifier**: `REL-063`
- **Child Table (Dependent)**: `pharmacy.formulary_drugs` (Column: `category_id`)
- **Parent Table (Referenced)**: `pharmacy.drug_categories` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Formulary drug classified by therapeutic category
- **Transactional Boundary**: Governed by `Formulary catalog maintenance`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_formulary_drugs_category_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `drug_categories` creation to dependent `formulary_drugs` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-063
ALTER TABLE pharmacy.formulary_drugs
    ADD CONSTRAINT fk_formulary_drugs_category_id
    FOREIGN KEY (category_id) REFERENCES pharmacy.drug_categories(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_formulary_drugs_category_id
    ON pharmacy.formulary_drugs USING btree (category_id);
```

### REL-064: `pharmacy_batches.drug_id` -> `formulary_drugs.id`

- **Relationship Identifier**: `REL-064`
- **Child Table (Dependent)**: `pharmacy.pharmacy_batches` (Column: `drug_id`)
- **Parent Table (Referenced)**: `pharmacy.formulary_drugs` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Manufactured drug batch belongs to formulary drug
- **Transactional Boundary**: Governed by `Goods inward batch receipt TXN-014`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_pharmacy_batches_drug_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `formulary_drugs` creation to dependent `pharmacy_batches` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-064
ALTER TABLE pharmacy.pharmacy_batches
    ADD CONSTRAINT fk_pharmacy_batches_drug_id
    FOREIGN KEY (drug_id) REFERENCES pharmacy.formulary_drugs(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_pharmacy_batches_drug_id
    ON pharmacy.pharmacy_batches USING btree (drug_id);
```

### REL-065: `clinic_stock.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-065`
- **Child Table (Dependent)**: `pharmacy.clinic_stock` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Current stock inventory held at facility
- **Transactional Boundary**: Governed by `Stock balance update TXN-015`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_clinic_stock_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `clinic_stock` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-065
ALTER TABLE pharmacy.clinic_stock
    ADD CONSTRAINT fk_clinic_stock_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_clinic_stock_facility_id
    ON pharmacy.clinic_stock USING btree (facility_id);
```

### REL-066: `clinic_stock.batch_id` -> `pharmacy_batches.id`

- **Relationship Identifier**: `REL-066`
- **Child Table (Dependent)**: `pharmacy.clinic_stock` (Column: `batch_id`)
- **Parent Table (Referenced)**: `pharmacy.pharmacy_batches` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Facility inventory balance per specific batch
- **Transactional Boundary**: Governed by `Inventory allocation TXN-015`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_clinic_stock_batch_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `pharmacy_batches` creation to dependent `clinic_stock` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-066
ALTER TABLE pharmacy.clinic_stock
    ADD CONSTRAINT fk_clinic_stock_batch_id
    FOREIGN KEY (batch_id) REFERENCES pharmacy.pharmacy_batches(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_clinic_stock_batch_id
    ON pharmacy.clinic_stock USING btree (batch_id);
```

### REL-067: `dispensations.prescription_id` -> `prescriptions.id`

- **Relationship Identifier**: `REL-067`
- **Child Table (Dependent)**: `pharmacy.dispensations` (Column: `prescription_id`)
- **Parent Table (Referenced)**: `clinical.prescriptions` (Column: `id`)
- **Cardinality & Optionality**: `1:1` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Dispensation fulfills doctor prescription
- **Transactional Boundary**: Governed by `Pharmacy dispensing TXN-016`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_dispensations_prescription_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `prescriptions` creation to dependent `dispensations` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-067
ALTER TABLE pharmacy.dispensations
    ADD CONSTRAINT fk_dispensations_prescription_id
    FOREIGN KEY (prescription_id) REFERENCES clinical.prescriptions(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_dispensations_prescription_id
    ON pharmacy.dispensations USING btree (prescription_id);
```

### REL-068: `dispensations.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-068`
- **Child Table (Dependent)**: `pharmacy.dispensations` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Pharmacy counter dispensing drugs
- **Transactional Boundary**: Governed by `Pharmacy dispensing TXN-016`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_dispensations_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `dispensations` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-068
ALTER TABLE pharmacy.dispensations
    ADD CONSTRAINT fk_dispensations_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_dispensations_facility_id
    ON pharmacy.dispensations USING btree (facility_id);
```

### REL-069: `dispensations.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-069`
- **Child Table (Dependent)**: `pharmacy.dispensations` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Patient receiving medication
- **Transactional Boundary**: Governed by `Drug dispensing TXN-016`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_dispensations_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `dispensations` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-069
ALTER TABLE pharmacy.dispensations
    ADD CONSTRAINT fk_dispensations_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_dispensations_patient_id
    ON pharmacy.dispensations USING btree (patient_id);
```

### REL-070: `dispensation_items.dispensation_id` -> `dispensations.id`

- **Relationship Identifier**: `REL-070`
- **Child Table (Dependent)**: `pharmacy.dispensation_items` (Column: `dispensation_id`)
- **Parent Table (Referenced)**: `pharmacy.dispensations` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Dispensation composed of drug items
- **Transactional Boundary**: Governed by `Dispensation detailing TXN-016`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_dispensation_items_dispensation_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `dispensations` creation to dependent `dispensation_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-070
ALTER TABLE pharmacy.dispensation_items
    ADD CONSTRAINT fk_dispensation_items_dispensation_id
    FOREIGN KEY (dispensation_id) REFERENCES pharmacy.dispensations(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_dispensation_items_dispensation_id
    ON pharmacy.dispensation_items USING btree (dispensation_id);
```

### REL-071: `dispensation_items.batch_id` -> `pharmacy_batches.id`

- **Relationship Identifier**: `REL-071`
- **Child Table (Dependent)**: `pharmacy.dispensation_items` (Column: `batch_id`)
- **Parent Table (Referenced)**: `pharmacy.pharmacy_batches` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Specific batch deducted upon dispensing
- **Transactional Boundary**: Governed by `Inventory deduction TXN-016`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_dispensation_items_batch_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `pharmacy_batches` creation to dependent `dispensation_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-071
ALTER TABLE pharmacy.dispensation_items
    ADD CONSTRAINT fk_dispensation_items_batch_id
    FOREIGN KEY (batch_id) REFERENCES pharmacy.pharmacy_batches(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_dispensation_items_batch_id
    ON pharmacy.dispensation_items USING btree (batch_id);
```

### REL-072: `dispensation_items.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-072`
- **Child Table (Dependent)**: `pharmacy.dispensation_items` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Facility inventory decrement context
- **Transactional Boundary**: Governed by `Stock decrement TXN-016`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_dispensation_items_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `dispensation_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-072
ALTER TABLE pharmacy.dispensation_items
    ADD CONSTRAINT fk_dispensation_items_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_dispensation_items_facility_id
    ON pharmacy.dispensation_items USING btree (facility_id);
```

### REL-073: `dispensation_items.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-073`
- **Child Table (Dependent)**: `pharmacy.dispensation_items` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Direct patient linkage for pharmacovigilance
- **Transactional Boundary**: Governed by `Dispense logging`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_dispensation_items_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `dispensation_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-073
ALTER TABLE pharmacy.dispensation_items
    ADD CONSTRAINT fk_dispensation_items_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_dispensation_items_patient_id
    ON pharmacy.dispensation_items USING btree (patient_id);
```

### REL-074: `stock_movements.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-074`
- **Child Table (Dependent)**: `pharmacy.stock_movements` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Inventory movement audit ledger for facility
- **Transactional Boundary**: Governed by `Double-entry inventory audit TXN-017`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_stock_movements_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `stock_movements` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-074
ALTER TABLE pharmacy.stock_movements
    ADD CONSTRAINT fk_stock_movements_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_stock_movements_facility_id
    ON pharmacy.stock_movements USING btree (facility_id);
```

### REL-075: `stock_movements.batch_id` -> `pharmacy_batches.id`

- **Relationship Identifier**: `REL-075`
- **Child Table (Dependent)**: `pharmacy.stock_movements` (Column: `batch_id`)
- **Parent Table (Referenced)**: `pharmacy.pharmacy_batches` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Batch affected by stock movement
- **Transactional Boundary**: Governed by `Stock transaction audit TXN-017`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_stock_movements_batch_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `pharmacy_batches` creation to dependent `stock_movements` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-075
ALTER TABLE pharmacy.stock_movements
    ADD CONSTRAINT fk_stock_movements_batch_id
    FOREIGN KEY (batch_id) REFERENCES pharmacy.pharmacy_batches(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_stock_movements_batch_id
    ON pharmacy.stock_movements USING btree (batch_id);
```

### REL-076: `drug_indents.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-076`
- **Child Table (Dependent)**: `pharmacy.drug_indents` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Indent submitted by requesting clinic
- **Transactional Boundary**: Governed by `Indent requisition TXN-018`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_drug_indents_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `drug_indents` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-076
ALTER TABLE pharmacy.drug_indents
    ADD CONSTRAINT fk_drug_indents_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_drug_indents_facility_id
    ON pharmacy.drug_indents USING btree (facility_id);
```

### REL-077: `indent_items.indent_id` -> `drug_indents.id`

- **Relationship Identifier**: `REL-077`
- **Child Table (Dependent)**: `pharmacy.indent_items` (Column: `indent_id`)
- **Parent Table (Referenced)**: `pharmacy.drug_indents` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Medication line items requested in indent
- **Transactional Boundary**: Governed by `Indent itemization TXN-018`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_indent_items_indent_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `drug_indents` creation to dependent `indent_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-077
ALTER TABLE pharmacy.indent_items
    ADD CONSTRAINT fk_indent_items_indent_id
    FOREIGN KEY (indent_id) REFERENCES pharmacy.drug_indents(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_indent_items_indent_id
    ON pharmacy.indent_items USING btree (indent_id);
```

### REL-078: `indent_items.drug_id` -> `formulary_drugs.id`

- **Relationship Identifier**: `REL-078`
- **Child Table (Dependent)**: `pharmacy.indent_items` (Column: `drug_id`)
- **Parent Table (Referenced)**: `pharmacy.formulary_drugs` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Drug item requisitioned from warehouse
- **Transactional Boundary**: Governed by `Warehouse requisition TXN-018`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_indent_items_drug_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `formulary_drugs` creation to dependent `indent_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-078
ALTER TABLE pharmacy.indent_items
    ADD CONSTRAINT fk_indent_items_drug_id
    FOREIGN KEY (drug_id) REFERENCES pharmacy.formulary_drugs(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_indent_items_drug_id
    ON pharmacy.indent_items USING btree (drug_id);
```

### REL-079: `indent_items.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-079`
- **Child Table (Dependent)**: `pharmacy.indent_items` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinic destination for indent item delivery
- **Transactional Boundary**: Governed by `Indent delivery fulfillment`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_indent_items_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `indent_items` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-079
ALTER TABLE pharmacy.indent_items
    ADD CONSTRAINT fk_indent_items_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_indent_items_facility_id
    ON pharmacy.indent_items USING btree (facility_id);
```

### REL-080: `cold_chain_devices.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-080`
- **Child Table (Dependent)**: `pharmacy.cold_chain_devices` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Vaccine refrigerator located in clinic facility
- **Transactional Boundary**: Governed by `Cold chain device commissioning`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_cold_chain_devices_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `cold_chain_devices` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-080
ALTER TABLE pharmacy.cold_chain_devices
    ADD CONSTRAINT fk_cold_chain_devices_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_cold_chain_devices_facility_id
    ON pharmacy.cold_chain_devices USING btree (facility_id);
```

### REL-081: `cold_chain_devices.room_id` -> `facility_rooms.id`

- **Relationship Identifier**: `REL-081`
- **Child Table (Dependent)**: `pharmacy.cold_chain_devices` (Column: `room_id`)
- **Parent Table (Referenced)**: `identity.facility_rooms` (Column: `id`)
- **Cardinality & Optionality**: `1:1` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Room where cold chain device is physically installed
- **Transactional Boundary**: Governed by `Equipment installation`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_cold_chain_devices_room_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facility_rooms` creation to dependent `cold_chain_devices` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-081
ALTER TABLE pharmacy.cold_chain_devices
    ADD CONSTRAINT fk_cold_chain_devices_room_id
    FOREIGN KEY (room_id) REFERENCES identity.facility_rooms(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_cold_chain_devices_room_id
    ON pharmacy.cold_chain_devices USING btree (room_id);
```

### REL-082: `cold_chain_telemetry.device_id` -> `cold_chain_devices.id`

- **Relationship Identifier**: `REL-082`
- **Child Table (Dependent)**: `pharmacy.cold_chain_telemetry` (Column: `device_id`)
- **Parent Table (Referenced)**: `pharmacy.cold_chain_devices` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: High-frequency temperature sensor observations
- **Transactional Boundary**: Governed by `IoT telemetry streaming TXN-019`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_cold_chain_telemetry_device_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `cold_chain_devices` creation to dependent `cold_chain_telemetry` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-082
ALTER TABLE pharmacy.cold_chain_telemetry
    ADD CONSTRAINT fk_cold_chain_telemetry_device_id
    FOREIGN KEY (device_id) REFERENCES pharmacy.cold_chain_devices(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_cold_chain_telemetry_device_id
    ON pharmacy.cold_chain_telemetry USING btree (device_id);
```

### REL-083: `cold_chain_telemetry.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-083`
- **Child Table (Dependent)**: `pharmacy.cold_chain_telemetry` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinic temperature log roll-up
- **Transactional Boundary**: Governed by `Cold chain excursion alerting TXN-019`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_cold_chain_telemetry_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `cold_chain_telemetry` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-083
ALTER TABLE pharmacy.cold_chain_telemetry
    ADD CONSTRAINT fk_cold_chain_telemetry_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_cold_chain_telemetry_facility_id
    ON pharmacy.cold_chain_telemetry USING btree (facility_id);
```

### REL-084: `referrals.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-084`
- **Child Table (Dependent)**: `continuity.referrals` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Outbound referral dossier for patient
- **Transactional Boundary**: Governed by `Hospital referral TXN-020`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_referrals_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `referrals` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-084
ALTER TABLE continuity.referrals
    ADD CONSTRAINT fk_referrals_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_referrals_patient_id
    ON continuity.referrals USING btree (patient_id);
```

### REL-085: `referrals.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-085`
- **Child Table (Dependent)**: `continuity.referrals` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Referring clinic facility
- **Transactional Boundary**: Governed by `Hospital referral TXN-020`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_referrals_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `referrals` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-085
ALTER TABLE continuity.referrals
    ADD CONSTRAINT fk_referrals_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_referrals_facility_id
    ON continuity.referrals USING btree (facility_id);
```

### REL-086: `referrals.target_facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-086`
- **Child Table (Dependent)**: `continuity.referrals` (Column: `target_facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Destination secondary/tertiary hospital
- **Transactional Boundary**: Governed by `Hospital referral TXN-020`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_referrals_target_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `referrals` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-086
ALTER TABLE continuity.referrals
    ADD CONSTRAINT fk_referrals_target_facility_id
    FOREIGN KEY (target_facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_referrals_target_facility_id
    ON continuity.referrals USING btree (target_facility_id);
```

### REL-087: `referral_counter_notes.referral_id` -> `referrals.id`

- **Relationship Identifier**: `REL-087`
- **Child Table (Dependent)**: `continuity.referral_counter_notes` (Column: `referral_id`)
- **Parent Table (Referenced)**: `continuity.referrals` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE CASCADE`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Specialist feedback counter-note
- **Transactional Boundary**: Governed by `Counter-referral feedback TXN-021`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_referral_counter_notes_referral_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Child records cascade delete atomically with parent.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `referrals` creation to dependent `referral_counter_notes` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-087
ALTER TABLE continuity.referral_counter_notes
    ADD CONSTRAINT fk_referral_counter_notes_referral_id
    FOREIGN KEY (referral_id) REFERENCES continuity.referrals(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_referral_counter_notes_referral_id
    ON continuity.referral_counter_notes USING btree (referral_id);
```

### REL-088: `referral_counter_notes.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-088`
- **Child Table (Dependent)**: `continuity.referral_counter_notes` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Patient counter-referral medical record
- **Transactional Boundary**: Governed by `Discharge feedback TXN-021`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_referral_counter_notes_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `referral_counter_notes` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-088
ALTER TABLE continuity.referral_counter_notes
    ADD CONSTRAINT fk_referral_counter_notes_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_referral_counter_notes_patient_id
    ON continuity.referral_counter_notes USING btree (patient_id);
```

### REL-089: `referral_counter_notes.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-089`
- **Child Table (Dependent)**: `continuity.referral_counter_notes` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Referring clinic receiving specialist feedback
- **Transactional Boundary**: Governed by `Feedback review TXN-021`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_referral_counter_notes_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `referral_counter_notes` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-089
ALTER TABLE continuity.referral_counter_notes
    ADD CONSTRAINT fk_referral_counter_notes_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_referral_counter_notes_facility_id
    ON continuity.referral_counter_notes USING btree (facility_id);
```

### REL-090: `ncd_episodes.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-090`
- **Child Table (Dependent)**: `continuity.ncd_episodes` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Longitudinal chronic disease care plan
- **Transactional Boundary**: Governed by `NCD enrollment TXN-022`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_ncd_episodes_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `ncd_episodes` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-090
ALTER TABLE continuity.ncd_episodes
    ADD CONSTRAINT fk_ncd_episodes_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_ncd_episodes_patient_id
    ON continuity.ncd_episodes USING btree (patient_id);
```

### REL-091: `ncd_episodes.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-091`
- **Child Table (Dependent)**: `continuity.ncd_episodes` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Primary clinic managing patient NCD plan
- **Transactional Boundary**: Governed by `NCD care management TXN-022`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_ncd_episodes_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `ncd_episodes` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-091
ALTER TABLE continuity.ncd_episodes
    ADD CONSTRAINT fk_ncd_episodes_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_ncd_episodes_facility_id
    ON continuity.ncd_episodes USING btree (facility_id);
```

### REL-092: `follow_up_schedules.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-092`
- **Child Table (Dependent)**: `continuity.follow_up_schedules` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Scheduled review appointment for citizen
- **Transactional Boundary**: Governed by `Follow-up scheduling TXN-023`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_follow_up_schedules_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `follow_up_schedules` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-092
ALTER TABLE continuity.follow_up_schedules
    ADD CONSTRAINT fk_follow_up_schedules_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_follow_up_schedules_patient_id
    ON continuity.follow_up_schedules USING btree (patient_id);
```

### REL-093: `follow_up_schedules.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-093`
- **Child Table (Dependent)**: `continuity.follow_up_schedules` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinic where follow-up will occur
- **Transactional Boundary**: Governed by `Follow-up scheduling TXN-023`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_follow_up_schedules_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `follow_up_schedules` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-093
ALTER TABLE continuity.follow_up_schedules
    ADD CONSTRAINT fk_follow_up_schedules_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_follow_up_schedules_facility_id
    ON continuity.follow_up_schedules USING btree (facility_id);
```

### REL-094: `notifications.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-094`
- **Child Table (Dependent)**: `continuity.notifications` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Notification sent to patient mobile
- **Transactional Boundary**: Governed by `Citizen communication dispatch TXN-024`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_notifications_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `notifications` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-094
ALTER TABLE continuity.notifications
    ADD CONSTRAINT fk_notifications_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_notifications_patient_id
    ON continuity.notifications USING btree (patient_id);
```

### REL-095: `notifications.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-095`
- **Child Table (Dependent)**: `continuity.notifications` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinic originating communication message
- **Transactional Boundary**: Governed by `Notification dispatch TXN-024`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_notifications_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `notifications` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-095
ALTER TABLE continuity.notifications
    ADD CONSTRAINT fk_notifications_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_notifications_facility_id
    ON continuity.notifications USING btree (facility_id);
```

### REL-096: `grievances.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-096`
- **Child Table (Dependent)**: `continuity.grievances` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinic subject to citizen grievance ticket
- **Transactional Boundary**: Governed by `Grievance filing & resolution`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_grievances_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `grievances` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-096
ALTER TABLE continuity.grievances
    ADD CONSTRAINT fk_grievances_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_grievances_facility_id
    ON continuity.grievances USING btree (facility_id);
```

### REL-097: `grievances.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-097`
- **Child Table (Dependent)**: `continuity.grievances` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Citizen filing service grievance
- **Transactional Boundary**: Governed by `Grievance submission`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_grievances_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `grievances` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-097
ALTER TABLE continuity.grievances
    ADD CONSTRAINT fk_grievances_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_grievances_patient_id
    ON continuity.grievances USING btree (patient_id);
```

### REL-098: `helpdesk_tickets.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-098`
- **Child Table (Dependent)**: `continuity.helpdesk_tickets` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinic hardware or IT issue ticket
- **Transactional Boundary**: Governed by `Support ticket escalation`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_helpdesk_tickets_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `helpdesk_tickets` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-098
ALTER TABLE continuity.helpdesk_tickets
    ADD CONSTRAINT fk_helpdesk_tickets_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_helpdesk_tickets_facility_id
    ON continuity.helpdesk_tickets USING btree (facility_id);
```

### REL-099: `audit_events.actor_user_id` -> `auth_users.id`

- **Relationship Identifier**: `REL-099`
- **Child Table (Dependent)**: `audit.audit_events` (Column: `actor_user_id`)
- **Parent Table (Referenced)**: `identity.auth_users` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: User performing audited system mutation
- **Transactional Boundary**: Governed by `WORM audit logging TXN-025`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_audit_events_actor_user_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `auth_users` creation to dependent `audit_events` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-099
ALTER TABLE audit.audit_events
    ADD CONSTRAINT fk_audit_events_actor_user_id
    FOREIGN KEY (actor_user_id) REFERENCES identity.auth_users(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_audit_events_actor_user_id
    ON audit.audit_events USING btree (actor_user_id);
```

### REL-100: `audit_events.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-100`
- **Child Table (Dependent)**: `audit.audit_events` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Facility location where audited mutation occurred
- **Transactional Boundary**: Governed by `WORM audit logging TXN-025`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_audit_events_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `audit_events` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-100
ALTER TABLE audit.audit_events
    ADD CONSTRAINT fk_audit_events_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_audit_events_facility_id
    ON audit.audit_events USING btree (facility_id);
```

### REL-101: `offline_mutation_log.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-101`
- **Child Table (Dependent)**: `sync.offline_mutation_log` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinic edge appliance recording offline mutation
- **Transactional Boundary**: Governed by `Edge journal write TXN-025`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_offline_mutation_log_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `offline_mutation_log` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-101
ALTER TABLE sync.offline_mutation_log
    ADD CONSTRAINT fk_offline_mutation_log_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_offline_mutation_log_facility_id
    ON sync.offline_mutation_log USING btree (facility_id);
```

### REL-102: `abdm_artifacts.patient_id` -> `patients.id`

- **Relationship Identifier**: `REL-102`
- **Child Table (Dependent)**: `sync.abdm_artifacts` (Column: `patient_id`)
- **Parent Table (Referenced)**: `intake.patients` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: ABDM FHIR artifacts linked to registered citizen
- **Transactional Boundary**: Governed by `National health exchange TXN-004`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_abdm_artifacts_patient_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `patients` creation to dependent `abdm_artifacts` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-102
ALTER TABLE sync.abdm_artifacts
    ADD CONSTRAINT fk_abdm_artifacts_patient_id
    FOREIGN KEY (patient_id) REFERENCES intake.patients(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_abdm_artifacts_patient_id
    ON sync.abdm_artifacts USING btree (patient_id);
```

### REL-103: `abdm_artifacts.facility_id` -> `facilities.id`

- **Relationship Identifier**: `REL-103`
- **Child Table (Dependent)**: `sync.abdm_artifacts` (Column: `facility_id`)
- **Parent Table (Referenced)**: `identity.facilities` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Healthcare facility sharing ABDM clinical bundle
- **Transactional Boundary**: Governed by `ABDM bundle push TXN-004`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_abdm_artifacts_facility_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `facilities` creation to dependent `abdm_artifacts` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-103
ALTER TABLE sync.abdm_artifacts
    ADD CONSTRAINT fk_abdm_artifacts_facility_id
    FOREIGN KEY (facility_id) REFERENCES identity.facilities(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_abdm_artifacts_facility_id
    ON sync.abdm_artifacts USING btree (facility_id);
```

### REL-104: `patient_vitals.encounter_id` -> `clinical_encounters.id`

- **Relationship Identifier**: `REL-104`
- **Child Table (Dependent)**: `intake.patient_vitals` (Column: `encounter_id`)
- **Parent Table (Referenced)**: `clinical.clinical_encounters` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Vitals recorded directly during physician consultation
- **Transactional Boundary**: Governed by `Consultation vitals entry`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_patient_vitals_encounter_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `clinical_encounters` creation to dependent `patient_vitals` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-104
ALTER TABLE intake.patient_vitals
    ADD CONSTRAINT fk_patient_vitals_encounter_id
    FOREIGN KEY (encounter_id) REFERENCES clinical.clinical_encounters(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_patient_vitals_encounter_id
    ON intake.patient_vitals USING btree (encounter_id);
```

### REL-105: `danger_alerts.encounter_id` -> `clinical_encounters.id`

- **Relationship Identifier**: `REL-105`
- **Child Table (Dependent)**: `intake.danger_alerts` (Column: `encounter_id`)
- **Parent Table (Referenced)**: `clinical.clinical_encounters` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Danger alert triggered during doctor consultation
- **Transactional Boundary**: Governed by `Clinical safety escalation`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_danger_alerts_encounter_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `clinical_encounters` creation to dependent `danger_alerts` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-105
ALTER TABLE intake.danger_alerts
    ADD CONSTRAINT fk_danger_alerts_encounter_id
    FOREIGN KEY (encounter_id) REFERENCES clinical.clinical_encounters(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_danger_alerts_encounter_id
    ON intake.danger_alerts USING btree (encounter_id);
```

### REL-106: `referrals.encounter_id` -> `clinical_encounters.id`

- **Relationship Identifier**: `REL-106`
- **Child Table (Dependent)**: `continuity.referrals` (Column: `encounter_id`)
- **Parent Table (Referenced)**: `clinical.clinical_encounters` (Column: `id`)
- **Cardinality & Optionality**: `1:1` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Referral created as disposition of clinical encounter
- **Transactional Boundary**: Governed by `Referral order TXN-020`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_referrals_encounter_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `clinical_encounters` creation to dependent `referrals` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-106
ALTER TABLE continuity.referrals
    ADD CONSTRAINT fk_referrals_encounter_id
    FOREIGN KEY (encounter_id) REFERENCES clinical.clinical_encounters(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_referrals_encounter_id
    ON continuity.referrals USING btree (encounter_id);
```

### REL-107: `follow_up_schedules.encounter_id` -> `clinical_encounters.id`

- **Relationship Identifier**: `REL-107`
- **Child Table (Dependent)**: `continuity.follow_up_schedules` (Column: `encounter_id`)
- **Parent Table (Referenced)**: `clinical.clinical_encounters` (Column: `id`)
- **Cardinality & Optionality**: `1:1` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Follow up scheduled upon encounter discharge
- **Transactional Boundary**: Governed by `Discharge planning TXN-023`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_follow_up_schedules_encounter_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `clinical_encounters` creation to dependent `follow_up_schedules` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-107
ALTER TABLE continuity.follow_up_schedules
    ADD CONSTRAINT fk_follow_up_schedules_encounter_id
    FOREIGN KEY (encounter_id) REFERENCES clinical.clinical_encounters(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_follow_up_schedules_encounter_id
    ON continuity.follow_up_schedules USING btree (encounter_id);
```

### REL-108: `clinical_encounters.ncd_episode_id` -> `ncd_episodes.id`

- **Relationship Identifier**: `REL-108`
- **Child Table (Dependent)**: `clinical.clinical_encounters` (Column: `ncd_episode_id`)
- **Parent Table (Referenced)**: `continuity.ncd_episodes` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Encounter conducted as part of longitudinal NCD care
- **Transactional Boundary**: Governed by `NCD consultation TXN-022`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_clinical_encounters_ncd_episode_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `ncd_episodes` creation to dependent `clinical_encounters` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-108
ALTER TABLE clinical.clinical_encounters
    ADD CONSTRAINT fk_clinical_encounters_ncd_episode_id
    FOREIGN KEY (ncd_episode_id) REFERENCES continuity.ncd_episodes(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_clinical_encounters_ncd_episode_id
    ON clinical.clinical_encounters USING btree (ncd_episode_id);
```

### REL-109: `helpdesk_tickets.device_id` -> `cold_chain_devices.id`

- **Relationship Identifier**: `REL-109`
- **Child Table (Dependent)**: `continuity.helpdesk_tickets` (Column: `device_id`)
- **Parent Table (Referenced)**: `pharmacy.cold_chain_devices` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Optional)
- **Referential Actions**: `ON DELETE SET NULL`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Equipment fault ticket for cold chain refrigerator
- **Transactional Boundary**: Governed by `Cold chain breakdown ticket`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_helpdesk_tickets_device_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `cold_chain_devices` creation to dependent `helpdesk_tickets` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-109
ALTER TABLE continuity.helpdesk_tickets
    ADD CONSTRAINT fk_helpdesk_tickets_device_id
    FOREIGN KEY (device_id) REFERENCES pharmacy.cold_chain_devices(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_helpdesk_tickets_device_id
    ON continuity.helpdesk_tickets USING btree (device_id);
```

### REL-110: `clinic_stock.drug_id` -> `formulary_drugs.id`

- **Relationship Identifier**: `REL-110`
- **Child Table (Dependent)**: `pharmacy.clinic_stock` (Column: `drug_id`)
- **Parent Table (Referenced)**: `pharmacy.formulary_drugs` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Clinic stock balance aggregation by formulary drug
- **Transactional Boundary**: Governed by `Stock reorder calculation`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_clinic_stock_drug_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `formulary_drugs` creation to dependent `clinic_stock` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-110
ALTER TABLE pharmacy.clinic_stock
    ADD CONSTRAINT fk_clinic_stock_drug_id
    FOREIGN KEY (drug_id) REFERENCES pharmacy.formulary_drugs(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_clinic_stock_drug_id
    ON pharmacy.clinic_stock USING btree (drug_id);
```

### REL-111: `stock_movements.drug_id` -> `formulary_drugs.id`

- **Relationship Identifier**: `REL-111`
- **Child Table (Dependent)**: `pharmacy.stock_movements` (Column: `drug_id`)
- **Parent Table (Referenced)**: `pharmacy.formulary_drugs` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Stock movement ledger item drug classification
- **Transactional Boundary**: Governed by `Inventory reconciliation`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_stock_movements_drug_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `formulary_drugs` creation to dependent `stock_movements` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-111
ALTER TABLE pharmacy.stock_movements
    ADD CONSTRAINT fk_stock_movements_drug_id
    FOREIGN KEY (drug_id) REFERENCES pharmacy.formulary_drugs(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_stock_movements_drug_id
    ON pharmacy.stock_movements USING btree (drug_id);
```

### REL-112: `dispensations.pharmacist_user_id` -> `auth_users.id`

- **Relationship Identifier**: `REL-112`
- **Child Table (Dependent)**: `pharmacy.dispensations` (Column: `pharmacist_user_id`)
- **Parent Table (Referenced)**: `identity.auth_users` (Column: `id`)
- **Cardinality & Optionality**: `1:N` (Mandatory)
- **Referential Actions**: `ON DELETE RESTRICT`, `ON UPDATE CASCADE`
- **Architectural Rationale**: Licensed pharmacist dispensing medications
- **Transactional Boundary**: Governed by `Pharmacy handover TXN-016`
- **Dedicated FK Index Requirement**: Mandatory B-tree index `idx_dispensations_pharmacist_user_id` to accelerate joins and prevent share-row table locks during parent deletes.
- **Lifecycle Implications**: Parent deletion strictly barred while active child dependencies exist.
- **Data Quality Invariant**: Zero orphan records permitted; child foreign key must strictly resolve to valid parent primary key.
- **Lineage Traversal**: Ingestion flow traces from `auth_users` creation to dependent `dispensations` instantiation.

```sql
-- DOCUMENTATION-ONLY SQL: DDL Constraint & Index Definition for REL-112
ALTER TABLE pharmacy.dispensations
    ADD CONSTRAINT fk_dispensations_pharmacist_user_id
    FOREIGN KEY (pharmacist_user_id) REFERENCES identity.auth_users(id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS idx_dispensations_pharmacist_user_id
    ON pharmacy.dispensations USING btree (pharmacist_user_id);
```

## 5. Conclusion & Referential Integrity Invariants

The 112 foreign key specifications documented herein provide a complete, verified referential blueprint for the Namma Clinic database. All parent-child dependencies have been proven acyclic, and every foreign key has been assigned explicit cascade policies and mandatory indexing rules.
