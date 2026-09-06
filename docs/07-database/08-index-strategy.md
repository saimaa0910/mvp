# Phase 07 — Complete Indexing Strategy & Performance Acceleration Blueprint

> **Document Identifier**: `DB-INDEX-001`
> **System**: Namma Clinic Digital Health & Operations Platform
> **Municipal Authority**: Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Status**: APPROVED INDEXING BASELINE
> **Total Cataloged Indexes**: 132 Database Indexes (`INDEX-001` to `INDEX-132`)
> **Supported Index Engines**: B-tree, GIN, BRIN, Composite, Partial, and Expression Indexes
> **Operational Rule**: Zero Table Locking — All Production Indexes Built Using `CONCURRENTLY`

---

## 1. Executive Summary & Indexing Strategy Objectives

This document establishes the comprehensive database indexing strategy for the Namma Clinic platform on PostgreSQL 16. It details the technical rationale, query patterns, selectivity profiles, write amplification trade-offs, and monitoring runbooks across all 132 designated indexes supporting the 52 canonical tables.

The indexing architecture is engineered to guarantee sub-5 millisecond response times for primary clinical workflows (patient search, doctor call queue, barcode drug dispensing) while strictly controlling write amplification on high-throughput ingestion tables (IoT temperature telemetry, queue state transitions, WORM audit logs).

## 2. PostgreSQL Index Type Taxonomy & Use Cases

The platform utilizes five specialized index engines tailored to specific data access patterns:

| Index Engine | Storage & Access Mechanics | Primary Use Case in Namma Clinic | Write & Maintenance Cost |
| :--- | :--- | :--- | :--- |
| **B-Tree (Standard)** | Balanced search tree with O(log N) lookup, range scanning, and sort ordering. | Primary keys, foreign keys, unique natural handles (email, phone blind index). | Low to Medium; optimal for high-cardinality keys. |
| **Composite B-Tree** | Multi-column B-tree indexed in strict left-to-right prefix order. | Multi-predicate filters (e.g. `facility_id` + `status` + `priority_score`). | Medium; order of columns determines index reusability. |
| **Partial B-Tree** | B-tree index restricted to a subset of rows via a `WHERE` predicate filter. | Filtering active records (`WHERE deleted_at IS NULL`) or pending items. | Very Low; index size is tiny compared to full table. |
| **BRIN (Block Range)** | Block Range Index storing minimum and maximum values per 128 disk pages. | High-volume append-only time-series (`cold_chain_telemetry`, `audit_events`). | Extremely Low (< 1% of table size); minimal write cost. |
| **GIN (Generalized Inverted)**| Inverted index mapping terms and paths to tuple IDs. | Extensible JSONB searching on `clinical_payload_json` and metadata. | High write cost; optimized for rich clinical document queries. |

## 3. Database Indexing Anti-Patterns & Prevention Guardrails

To prevent operational degradation under heavy municipal loads, five critical indexing anti-patterns are strictly prohibited across all schemas:

| Anti-Pattern ID | Anti-Pattern Name | Description & Mechanism of Failure | Architectural Prevention Invariant |
| :--- | :--- | :--- | :--- |
| **AP-IDX-001** | Redundant Prefix Indexing | Creating a standalone index on column `A` when a composite index already exists on `(A, B)`. | PostgreSQL can utilize `(A, B)` for queries on `A` alone. Standalone index on `A` is redundant and wastes write I/O. |
| **AP-IDX-002** | Low-Selectivity Boolean Indexing | Building a full B-tree index on low-cardinality columns (e.g. `is_active BOOLEAN`). | Query planner ignores index and performs sequential scan if a value matches > 15% of table rows. Use partial index instead. |
| **AP-IDX-003** | Unindexed Foreign Keys | Omitting a dedicated B-tree index on a child table foreign key column. | When parent row is updated or deleted, PostgreSQL acquires a share-row lock and scans the entire child table, causing deadlocks. |
| **AP-IDX-004** | Over-Indexing on High-Ingest Tables | Creating 5+ B-tree indexes on append-heavy tables (`telemetry`, `mutations`). | Every insert must update all B-tree indexes, causing severe write amplification and disk I/O bottlenecks. |
| **AP-IDX-005** | Unused Index Accumulation | Retaining indexes that are never selected by the PostgreSQL query planner. | Wastes RAM buffer pool memory and slows table vacuuming. Monitored via `pg_stat_user_indexes`. |

## 4. Master Index Inventory (INDEX-001 to INDEX-132)

The 132 database indexes deployed across the platform are cataloged below:

| Index ID | Table Name | Columns | Index Engine | Uniqueness | Partial Predicate | Purpose & Query Pattern |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **INDEX-001** | `auth_users` | `(email)` | Unique B-tree | UNIQUE | `deleted_at IS NULL` | Accelerate login lookups by email |
| **INDEX-002** | `auth_users` | `(phone_blind_index)` | Unique B-tree | UNIQUE | `deleted_at IS NULL` | Lookup staff user by blinded phone hash |
| **INDEX-003** | `auth_users` | `(primary_facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Filter active staff assigned to a clinic |
| **INDEX-004** | `patients` | `(id)` | Unique B-tree | UNIQUE | None (Full) | Primary key index on UUIDv7 |
| **INDEX-005** | `patients` | `(facility_id, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Filter clinic registered patients sorted by intake date |
| **INDEX-006** | `patient_identifiers` | `(patient_id)` | B-tree | NON-UNIQUE | None (Full) | Foreign key lookup for patient identifiers |
| **INDEX-007** | `patient_identifiers` | `(reference_code)` | B-tree | NON-UNIQUE | None (Full) | Fast ABHA / external identifier lookup |
| **INDEX-008** | `tokens` | `(facility_id, status)` | Composite B-tree | NON-UNIQUE | None (Full) | Filter active daily tokens for clinic display queue |
| **INDEX-009** | `tokens` | `(patient_id)` | B-tree | NON-UNIQUE | None (Full) | Find daily token issued to specific patient |
| **INDEX-010** | `queue_entries` | `(facility_id, status, priority_score)` | Composite B-tree | NON-UNIQUE | None (Full) | Ordered queue retrieval for doctor and triage stations |
| **INDEX-011** | `queue_entries` | `(clinical_payload_json)` | GIN | NON-UNIQUE | None (Full) | JSONB search for queue tags and clinical flags |
| **INDEX-012** | `clinical_encounters` | `(patient_id, created_at)` | Composite B-tree | NON-UNIQUE | None (Full) | Fetch chronological consultation history for patient |
| **INDEX-013** | `clinical_encounters` | `(facility_id, created_at)` | BRIN | NON-UNIQUE | None (Full) | Block Range Index for multi-year encounter reporting |
| **INDEX-014** | `prescriptions` | `(patient_id, status)` | Composite B-tree | NON-UNIQUE | None (Full) | Fetch unfulfilled prescriptions for pharmacy dispensing |
| **INDEX-015** | `clinic_stock` | `(facility_id, batch_id)` | Unique B-tree | UNIQUE | None (Full) | Ensure single stock record per batch per clinic |
| **INDEX-016** | `cold_chain_telemetry` | `(facility_id, created_at)` | BRIN | NON-UNIQUE | None (Full) | Ultra-compact index for high-frequency IoT temperature readings |
| **INDEX-017** | `audit_events` | `(created_at)` | BRIN | NON-UNIQUE | None (Full) | Time-ordered append-only WORM audit query acceleration |
| **INDEX-018** | `facilities` | `(facility_code)` | Unique B-tree | UNIQUE | `deleted_at IS NULL` | Natural key lookup for facility onboarding and sync |
| **INDEX-019** | `facilities` | `(zone_name, ward_number)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Administrative hierarchical drilldown for municipal reports |
| **INDEX-020** | `facility_rooms` | `(facility_id, status)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Active consultation room lookup for queue routing |
| **INDEX-021** | `staff_profiles` | `(user_id)` | Unique B-tree | UNIQUE | `deleted_at IS NULL` | 1:1 link between auth user and medical credential profile |
| **INDEX-022** | `staff_shifts` | `(facility_id, status, created_at)` | Composite B-tree | NON-UNIQUE | None (Full) | Duty roster attendance lookup per clinic shift |
| **INDEX-023** | `system_configs` | `(facility_id, category_type)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Hierarchical config parameter lookup |
| **INDEX-024** | `patient_contacts` | `(patient_id, status)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Active contact information retrieval for patient |
| **INDEX-025** | `patient_addresses` | `(patient_id, status)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Current residential address lookup for citizen |
| **INDEX-026** | `consent_records` | `(patient_id, status)` | Composite B-tree | NON-UNIQUE | None (Full) | Active DPDP consent check before clinical record access |
| **INDEX-027** | `triage_assessments` | `(patient_id, created_at)` | Composite B-tree | NON-UNIQUE | None (Full) | Longitudinal triage history query for patient |
| **INDEX-028** | `danger_alerts` | `(facility_id, status)` | Composite B-tree | NON-UNIQUE | None (Full) | Real-time clinic dashboard danger alerts filter |
| **INDEX-029** | `auth_users` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on auth_users |
| **INDEX-030** | `auth_users` | `(created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on auth_users |
| **INDEX-031** | `user_credentials` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on user_credentials |
| **INDEX-032** | `user_credentials` | `(created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on user_credentials |
| **INDEX-033** | `user_sessions` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on user_sessions |
| **INDEX-034** | `user_sessions` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on user_sessions |
| **INDEX-035** | `roles` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on roles |
| **INDEX-036** | `roles` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on roles |
| **INDEX-037** | `permissions` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on permissions |
| **INDEX-038** | `permissions` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on permissions |
| **INDEX-039** | `role_permissions` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on role_permissions |
| **INDEX-040** | `role_permissions` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on role_permissions |
| **INDEX-041** | `user_roles` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on user_roles |
| **INDEX-042** | `user_roles` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on user_roles |
| **INDEX-043** | `facilities` | `(ward_number)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on facilities |
| **INDEX-044** | `facilities` | `(created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on facilities |
| **INDEX-045** | `facility_rooms` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on facility_rooms |
| **INDEX-046** | `facility_rooms` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on facility_rooms |
| **INDEX-047** | `staff_profiles` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on staff_profiles |
| **INDEX-048** | `staff_profiles` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on staff_profiles |
| **INDEX-049** | `staff_shifts` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on staff_shifts |
| **INDEX-050** | `staff_shifts` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on staff_shifts |
| **INDEX-051** | `system_configs` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on system_configs |
| **INDEX-052** | `system_configs` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on system_configs |
| **INDEX-053** | `patients` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on patients |
| **INDEX-054** | `patients` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on patients |
| **INDEX-055** | `patient_identifiers` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on patient_identifiers |
| **INDEX-056** | `patient_identifiers` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on patient_identifiers |
| **INDEX-057** | `patient_contacts` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on patient_contacts |
| **INDEX-058** | `patient_contacts` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on patient_contacts |
| **INDEX-059** | `patient_addresses` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on patient_addresses |
| **INDEX-060** | `patient_addresses` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on patient_addresses |
| **INDEX-061** | `consent_records` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on consent_records |
| **INDEX-062** | `consent_records` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on consent_records |
| **INDEX-063** | `tokens` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on tokens |
| **INDEX-064** | `tokens` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on tokens |
| **INDEX-065** | `queue_entries` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on queue_entries |
| **INDEX-066** | `queue_entries` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on queue_entries |
| **INDEX-067** | `triage_assessments` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on triage_assessments |
| **INDEX-068** | `triage_assessments` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on triage_assessments |
| **INDEX-069** | `patient_vitals` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on patient_vitals |
| **INDEX-070** | `patient_vitals` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on patient_vitals |
| **INDEX-071** | `danger_alerts` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on danger_alerts |
| **INDEX-072** | `danger_alerts` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on danger_alerts |
| **INDEX-073** | `clinical_encounters` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on clinical_encounters |
| **INDEX-074** | `clinical_encounters` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on clinical_encounters |
| **INDEX-075** | `clinical_notes` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on clinical_notes |
| **INDEX-076** | `clinical_notes` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on clinical_notes |
| **INDEX-077** | `diagnoses` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on diagnoses |
| **INDEX-078** | `diagnoses` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on diagnoses |
| **INDEX-079** | `prescriptions` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on prescriptions |
| **INDEX-080** | `prescriptions` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on prescriptions |
| **INDEX-081** | `prescription_items` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on prescription_items |
| **INDEX-082** | `prescription_items` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on prescription_items |
| **INDEX-083** | `lab_orders` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on lab_orders |
| **INDEX-084** | `lab_orders` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on lab_orders |
| **INDEX-085** | `lab_order_items` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on lab_order_items |
| **INDEX-086** | `lab_order_items` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on lab_order_items |
| **INDEX-087** | `lab_results` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on lab_results |
| **INDEX-088** | `lab_results` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on lab_results |
| **INDEX-089** | `teleconsultations` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on teleconsultations |
| **INDEX-090** | `teleconsultations` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on teleconsultations |
| **INDEX-091** | `formulary_drugs` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on formulary_drugs |
| **INDEX-092** | `formulary_drugs` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on formulary_drugs |
| **INDEX-093** | `drug_categories` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on drug_categories |
| **INDEX-094** | `drug_categories` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on drug_categories |
| **INDEX-095** | `pharmacy_batches` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on pharmacy_batches |
| **INDEX-096** | `pharmacy_batches` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on pharmacy_batches |
| **INDEX-097** | `clinic_stock` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on clinic_stock |
| **INDEX-098** | `clinic_stock` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on clinic_stock |
| **INDEX-099** | `dispensations` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on dispensations |
| **INDEX-100** | `dispensations` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on dispensations |
| **INDEX-101** | `dispensation_items` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on dispensation_items |
| **INDEX-102** | `dispensation_items` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on dispensation_items |
| **INDEX-103** | `stock_movements` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on stock_movements |
| **INDEX-104** | `stock_movements` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on stock_movements |
| **INDEX-105** | `drug_indents` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on drug_indents |
| **INDEX-106** | `drug_indents` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on drug_indents |
| **INDEX-107** | `indent_items` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on indent_items |
| **INDEX-108** | `indent_items` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on indent_items |
| **INDEX-109** | `cold_chain_devices` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on cold_chain_devices |
| **INDEX-110** | `cold_chain_devices` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on cold_chain_devices |
| **INDEX-111** | `cold_chain_telemetry` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on cold_chain_telemetry |
| **INDEX-112** | `cold_chain_telemetry` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on cold_chain_telemetry |
| **INDEX-113** | `referrals` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on referrals |
| **INDEX-114** | `referrals` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on referrals |
| **INDEX-115** | `referral_counter_notes` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on referral_counter_notes |
| **INDEX-116** | `referral_counter_notes` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on referral_counter_notes |
| **INDEX-117** | `ncd_episodes` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on ncd_episodes |
| **INDEX-118** | `ncd_episodes` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on ncd_episodes |
| **INDEX-119** | `follow_up_schedules` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on follow_up_schedules |
| **INDEX-120** | `follow_up_schedules` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on follow_up_schedules |
| **INDEX-121** | `notifications` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on notifications |
| **INDEX-122** | `notifications` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on notifications |
| **INDEX-123** | `grievances` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on grievances |
| **INDEX-124** | `grievances` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on grievances |
| **INDEX-125** | `helpdesk_tickets` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on helpdesk_tickets |
| **INDEX-126** | `helpdesk_tickets` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on helpdesk_tickets |
| **INDEX-127** | `audit_events` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on audit_events |
| **INDEX-128** | `audit_events` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on audit_events |
| **INDEX-129** | `offline_mutation_log` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on offline_mutation_log |
| **INDEX-130** | `offline_mutation_log` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on offline_mutation_log |
| **INDEX-131** | `abdm_artifacts` | `(facility_id)` | B-tree | NON-UNIQUE | `deleted_at IS NULL` | Accelerate clinic facility filtering on abdm_artifacts |
| **INDEX-132** | `abdm_artifacts` | `(status, created_at)` | Composite B-tree | NON-UNIQUE | `deleted_at IS NULL` | Optimize operational status workflows and temporal slicing on abdm_artifacts |

## 5. Detailed Index Specifications (INDEX-001 to INDEX-132)

Below is the exhaustive technical specification for every index in the platform, documenting columns, selectivity, query patterns, concurrency considerations, and removal criteria:

### INDEX-001: `idx_auth_users_index_001` on `identity.auth_users`

- **Index Identifier**: `INDEX-001`
- **Target Table**: `identity.auth_users`
- **Indexed Columns / Expression**: `(email)`
- **Engine Type**: `Unique B-tree` (Unique)
- **Technical Purpose**: Accelerate login lookups by email
- **Target Query Pattern**: `SELECT * FROM auth_users WHERE email = $1`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `Unique`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `lower(email)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-001
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS idx_auth_users_index_001
    ON identity.auth_users USING unique (email)
    WHERE deleted_at IS NULL;
```

### INDEX-002: `idx_auth_users_index_002` on `identity.auth_users`

- **Index Identifier**: `INDEX-002`
- **Target Table**: `identity.auth_users`
- **Indexed Columns / Expression**: `(phone_blind_index)`
- **Engine Type**: `Unique B-tree` (Unique)
- **Technical Purpose**: Lookup staff user by blinded phone hash
- **Target Query Pattern**: `SELECT * FROM auth_users WHERE phone_blind_index = $1`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `Unique`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-002
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS idx_auth_users_index_002
    ON identity.auth_users USING unique (phone_blind_index)
    WHERE deleted_at IS NULL;
```

### INDEX-003: `idx_auth_users_index_003` on `identity.auth_users`

- **Index Identifier**: `INDEX-003`
- **Target Table**: `identity.auth_users`
- **Indexed Columns / Expression**: `(primary_facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Filter active staff assigned to a clinic
- **Target Query Pattern**: `SELECT * FROM auth_users WHERE primary_facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-003
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_auth_users_index_003
    ON identity.auth_users USING b-tree (primary_facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-004: `idx_patients_index_004` on `intake.patients`

- **Index Identifier**: `INDEX-004`
- **Target Table**: `intake.patients`
- **Indexed Columns / Expression**: `(id)`
- **Engine Type**: `Unique B-tree` (Unique)
- **Technical Purpose**: Primary key index on UUIDv7
- **Target Query Pattern**: `SELECT * FROM patients WHERE id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `Unique`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Medium`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-004
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS idx_patients_index_004
    ON intake.patients USING unique (id);
```

### INDEX-005: `idx_patients_index_005` on `intake.patients`

- **Index Identifier**: `INDEX-005`
- **Target Table**: `intake.patients`
- **Indexed Columns / Expression**: `(facility_id, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Filter clinic registered patients sorted by intake date
- **Target Query Pattern**: `SELECT * FROM patients WHERE facility_id = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-005
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patients_index_005
    ON intake.patients USING composite (facility_id, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-006: `idx_patient_identifiers_index_006` on `intake.patient_identifiers`

- **Index Identifier**: `INDEX-006`
- **Target Table**: `intake.patient_identifiers`
- **Indexed Columns / Expression**: `(patient_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Foreign key lookup for patient identifiers
- **Target Query Pattern**: `SELECT * FROM patient_identifiers WHERE patient_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `High`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-006
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patient_identifiers_index_006
    ON intake.patient_identifiers USING b-tree (patient_id);
```

### INDEX-007: `idx_patient_identifiers_index_007` on `intake.patient_identifiers`

- **Index Identifier**: `INDEX-007`
- **Target Table**: `intake.patient_identifiers`
- **Indexed Columns / Expression**: `(reference_code)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Fast ABHA / external identifier lookup
- **Target Query Pattern**: `SELECT patient_id FROM patient_identifiers WHERE reference_code = $1`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `High`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-007
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patient_identifiers_index_007
    ON intake.patient_identifiers USING b-tree (reference_code);
```

### INDEX-008: `idx_tokens_index_008` on `intake.tokens`

- **Index Identifier**: `INDEX-008`
- **Target Table**: `intake.tokens`
- **Indexed Columns / Expression**: `(facility_id, status)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Filter active daily tokens for clinic display queue
- **Target Query Pattern**: `SELECT * FROM tokens WHERE facility_id = $1 AND status = 'ACTIVE'`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-008
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tokens_index_008
    ON intake.tokens USING composite (facility_id, status);
```

### INDEX-009: `idx_tokens_index_009` on `intake.tokens`

- **Index Identifier**: `INDEX-009`
- **Target Table**: `intake.tokens`
- **Indexed Columns / Expression**: `(patient_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Find daily token issued to specific patient
- **Target Query Pattern**: `SELECT * FROM tokens WHERE patient_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `High`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-009
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tokens_index_009
    ON intake.tokens USING b-tree (patient_id);
```

### INDEX-010: `idx_queue_entries_index_010` on `intake.queue_entries`

- **Index Identifier**: `INDEX-010`
- **Target Table**: `intake.queue_entries`
- **Indexed Columns / Expression**: `(facility_id, status, priority_score)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Ordered queue retrieval for doctor and triage stations
- **Target Query Pattern**: `SELECT * FROM queue_entries WHERE facility_id = $1 AND status = 'WAITING' ORDER BY priority_score DESC, created_at ASC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-010
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_queue_entries_index_010
    ON intake.queue_entries USING composite (facility_id, status, priority_score);
```

### INDEX-011: `idx_queue_entries_index_011` on `intake.queue_entries`

- **Index Identifier**: `INDEX-011`
- **Target Table**: `intake.queue_entries`
- **Indexed Columns / Expression**: `(clinical_payload_json)`
- **Engine Type**: `GIN` (Non-Unique)
- **Technical Purpose**: JSONB search for queue tags and clinical flags
- **Target Query Pattern**: `SELECT * FROM queue_entries WHERE clinical_payload_json @> '{"fast_track": true}'`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `High`; Storage Footprint `Medium`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-011
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_queue_entries_index_011
    ON intake.queue_entries USING gin (clinical_payload_json);
```

### INDEX-012: `idx_clinical_encounters_index_012` on `clinical.clinical_encounters`

- **Index Identifier**: `INDEX-012`
- **Target Table**: `clinical.clinical_encounters`
- **Indexed Columns / Expression**: `(patient_id, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Fetch chronological consultation history for patient
- **Target Query Pattern**: `SELECT * FROM clinical_encounters WHERE patient_id = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-012
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_clinical_encounters_index_012
    ON clinical.clinical_encounters USING composite (patient_id, created_at);
```

### INDEX-013: `idx_clinical_encounters_index_013` on `clinical.clinical_encounters`

- **Index Identifier**: `INDEX-013`
- **Target Table**: `clinical.clinical_encounters`
- **Indexed Columns / Expression**: `(facility_id, created_at)`
- **Engine Type**: `BRIN` (Non-Unique)
- **Technical Purpose**: Block Range Index for multi-year encounter reporting
- **Target Query Pattern**: `SELECT count(*) FROM clinical_encounters WHERE facility_id = $1 AND created_at BETWEEN $2 AND $3`
- **Expected Selectivity & Cardinality**: Selectivity `Medium`; Cardinality `Very High`
- **Resource Impact**: Write Cost `Very Low`; Storage Footprint `Very Low`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-013
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_clinical_encounters_index_013
    ON clinical.clinical_encounters USING brin (facility_id, created_at);
```

### INDEX-014: `idx_prescriptions_index_014` on `clinical.prescriptions`

- **Index Identifier**: `INDEX-014`
- **Target Table**: `clinical.prescriptions`
- **Indexed Columns / Expression**: `(patient_id, status)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Fetch unfulfilled prescriptions for pharmacy dispensing
- **Target Query Pattern**: `SELECT * FROM prescriptions WHERE patient_id = $1 AND status = 'PENDING'`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Low`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-014
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_prescriptions_index_014
    ON clinical.prescriptions USING composite (patient_id, status);
```

### INDEX-015: `idx_clinic_stock_index_015` on `pharmacy.clinic_stock`

- **Index Identifier**: `INDEX-015`
- **Target Table**: `pharmacy.clinic_stock`
- **Indexed Columns / Expression**: `(facility_id, batch_id)`
- **Engine Type**: `Unique B-tree` (Unique)
- **Technical Purpose**: Ensure single stock record per batch per clinic
- **Target Query Pattern**: `SELECT quantity_on_hand FROM clinic_stock WHERE facility_id = $1 AND batch_id = $2`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `Unique`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-015
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS idx_clinic_stock_index_015
    ON pharmacy.clinic_stock USING unique (facility_id, batch_id);
```

### INDEX-016: `idx_cold_chain_telemetry_index_016` on `pharmacy.cold_chain_telemetry`

- **Index Identifier**: `INDEX-016`
- **Target Table**: `pharmacy.cold_chain_telemetry`
- **Indexed Columns / Expression**: `(facility_id, created_at)`
- **Engine Type**: `BRIN` (Non-Unique)
- **Technical Purpose**: Ultra-compact index for high-frequency IoT temperature readings
- **Target Query Pattern**: `SELECT avg(temperature) FROM cold_chain_telemetry WHERE facility_id = $1 AND created_at >= now() - interval '24h'`
- **Expected Selectivity & Cardinality**: Selectivity `Medium`; Cardinality `Very High`
- **Resource Impact**: Write Cost `Very Low`; Storage Footprint `Very Low`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-016
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_cold_chain_telemetry_index_016
    ON pharmacy.cold_chain_telemetry USING brin (facility_id, created_at);
```

### INDEX-017: `idx_audit_events_index_017` on `audit.audit_events`

- **Index Identifier**: `INDEX-017`
- **Target Table**: `audit.audit_events`
- **Indexed Columns / Expression**: `(created_at)`
- **Engine Type**: `BRIN` (Non-Unique)
- **Technical Purpose**: Time-ordered append-only WORM audit query acceleration
- **Target Query Pattern**: `SELECT * FROM audit_events WHERE created_at BETWEEN $1 AND $2`
- **Expected Selectivity & Cardinality**: Selectivity `Medium`; Cardinality `Very High`
- **Resource Impact**: Write Cost `Very Low`; Storage Footprint `Very Low`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-017
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_audit_events_index_017
    ON audit.audit_events USING brin (created_at);
```

### INDEX-018: `idx_facilities_index_018` on `identity.facilities`

- **Index Identifier**: `INDEX-018`
- **Target Table**: `identity.facilities`
- **Indexed Columns / Expression**: `(facility_code)`
- **Engine Type**: `Unique B-tree` (Unique)
- **Technical Purpose**: Natural key lookup for facility onboarding and sync
- **Target Query Pattern**: `SELECT id FROM facilities WHERE facility_code = $1`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `Unique`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-018
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS idx_facilities_index_018
    ON identity.facilities USING unique (facility_code)
    WHERE deleted_at IS NULL;
```

### INDEX-019: `idx_facilities_index_019` on `identity.facilities`

- **Index Identifier**: `INDEX-019`
- **Target Table**: `identity.facilities`
- **Indexed Columns / Expression**: `(zone_name, ward_number)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Administrative hierarchical drilldown for municipal reports
- **Target Query Pattern**: `SELECT * FROM facilities WHERE zone_name = $1 AND ward_number = $2`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-019
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_facilities_index_019
    ON identity.facilities USING composite (zone_name, ward_number)
    WHERE deleted_at IS NULL;
```

### INDEX-020: `idx_facility_rooms_index_020` on `identity.facility_rooms`

- **Index Identifier**: `INDEX-020`
- **Target Table**: `identity.facility_rooms`
- **Indexed Columns / Expression**: `(facility_id, status)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Active consultation room lookup for queue routing
- **Target Query Pattern**: `SELECT * FROM facility_rooms WHERE facility_id = $1 AND status = 'ACTIVE'`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Low`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-020
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_facility_rooms_index_020
    ON identity.facility_rooms USING composite (facility_id, status)
    WHERE deleted_at IS NULL;
```

### INDEX-021: `idx_staff_profiles_index_021` on `identity.staff_profiles`

- **Index Identifier**: `INDEX-021`
- **Target Table**: `identity.staff_profiles`
- **Indexed Columns / Expression**: `(user_id)`
- **Engine Type**: `Unique B-tree` (Unique)
- **Technical Purpose**: 1:1 link between auth user and medical credential profile
- **Target Query Pattern**: `SELECT * FROM staff_profiles WHERE user_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `Unique`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-021
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS idx_staff_profiles_index_021
    ON identity.staff_profiles USING unique (user_id)
    WHERE deleted_at IS NULL;
```

### INDEX-022: `idx_staff_shifts_index_022` on `identity.staff_shifts`

- **Index Identifier**: `INDEX-022`
- **Target Table**: `identity.staff_shifts`
- **Indexed Columns / Expression**: `(facility_id, status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Duty roster attendance lookup per clinic shift
- **Target Query Pattern**: `SELECT * FROM staff_shifts WHERE facility_id = $1 AND status = 'ACTIVE'`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-022
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_staff_shifts_index_022
    ON identity.staff_shifts USING composite (facility_id, status, created_at);
```

### INDEX-023: `idx_system_configs_index_023` on `identity.system_configs`

- **Index Identifier**: `INDEX-023`
- **Target Table**: `identity.system_configs`
- **Indexed Columns / Expression**: `(facility_id, category_type)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Hierarchical config parameter lookup
- **Target Query Pattern**: `SELECT * FROM system_configs WHERE facility_id = $1 AND category_type = $2`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `High`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-023
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_system_configs_index_023
    ON identity.system_configs USING composite (facility_id, category_type)
    WHERE deleted_at IS NULL;
```

### INDEX-024: `idx_patient_contacts_index_024` on `intake.patient_contacts`

- **Index Identifier**: `INDEX-024`
- **Target Table**: `intake.patient_contacts`
- **Indexed Columns / Expression**: `(patient_id, status)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Active contact information retrieval for patient
- **Target Query Pattern**: `SELECT * FROM patient_contacts WHERE patient_id = $1 AND status = 'PRIMARY'`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `High`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-024
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patient_contacts_index_024
    ON intake.patient_contacts USING composite (patient_id, status)
    WHERE deleted_at IS NULL;
```

### INDEX-025: `idx_patient_addresses_index_025` on `intake.patient_addresses`

- **Index Identifier**: `INDEX-025`
- **Target Table**: `intake.patient_addresses`
- **Indexed Columns / Expression**: `(patient_id, status)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Current residential address lookup for citizen
- **Target Query Pattern**: `SELECT * FROM patient_addresses WHERE patient_id = $1 AND status = 'CURRENT'`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `High`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-025
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patient_addresses_index_025
    ON intake.patient_addresses USING composite (patient_id, status)
    WHERE deleted_at IS NULL;
```

### INDEX-026: `idx_consent_records_index_026` on `intake.consent_records`

- **Index Identifier**: `INDEX-026`
- **Target Table**: `intake.consent_records`
- **Indexed Columns / Expression**: `(patient_id, status)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Active DPDP consent check before clinical record access
- **Target Query Pattern**: `SELECT * FROM consent_records WHERE patient_id = $1 AND status = 'GRANTED'`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-026
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_consent_records_index_026
    ON intake.consent_records USING composite (patient_id, status);
```

### INDEX-027: `idx_triage_assessments_index_027` on `intake.triage_assessments`

- **Index Identifier**: `INDEX-027`
- **Target Table**: `intake.triage_assessments`
- **Indexed Columns / Expression**: `(patient_id, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Longitudinal triage history query for patient
- **Target Query Pattern**: `SELECT * FROM triage_assessments WHERE patient_id = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-027
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_triage_assessments_index_027
    ON intake.triage_assessments USING composite (patient_id, created_at);
```

### INDEX-028: `idx_danger_alerts_index_028` on `intake.danger_alerts`

- **Index Identifier**: `INDEX-028`
- **Target Table**: `intake.danger_alerts`
- **Indexed Columns / Expression**: `(facility_id, status)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Real-time clinic dashboard danger alerts filter
- **Target Query Pattern**: `SELECT * FROM danger_alerts WHERE facility_id = $1 AND status = 'ACTIVE'`
- **Expected Selectivity & Cardinality**: Selectivity `Very High`; Cardinality `Low`
- **Resource Impact**: Write Cost `High`; Storage Footprint `Low`
- **Partial Predicate**: `None (Indexes All Tuples)`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Dropped if write overhead > 15% and scan count < 100 per week

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-028
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_danger_alerts_index_028
    ON intake.danger_alerts USING composite (facility_id, status);
```

### INDEX-029: `idx_auth_users_index_029` on `identity.auth_users`

- **Index Identifier**: `INDEX-029`
- **Target Table**: `identity.auth_users`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on auth_users
- **Target Query Pattern**: `SELECT * FROM auth_users WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-029
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_auth_users_index_029
    ON identity.auth_users USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-030: `idx_auth_users_index_030` on `identity.auth_users`

- **Index Identifier**: `INDEX-030`
- **Target Table**: `identity.auth_users`
- **Indexed Columns / Expression**: `(created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on auth_users
- **Target Query Pattern**: `SELECT * FROM auth_users WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-030
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_auth_users_index_030
    ON identity.auth_users USING composite (created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-031: `idx_user_credentials_index_031` on `identity.user_credentials`

- **Index Identifier**: `INDEX-031`
- **Target Table**: `identity.user_credentials`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on user_credentials
- **Target Query Pattern**: `SELECT * FROM user_credentials WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-031
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_credentials_index_031
    ON identity.user_credentials USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-032: `idx_user_credentials_index_032` on `identity.user_credentials`

- **Index Identifier**: `INDEX-032`
- **Target Table**: `identity.user_credentials`
- **Indexed Columns / Expression**: `(created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on user_credentials
- **Target Query Pattern**: `SELECT * FROM user_credentials WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-032
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_credentials_index_032
    ON identity.user_credentials USING composite (created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-033: `idx_user_sessions_index_033` on `identity.user_sessions`

- **Index Identifier**: `INDEX-033`
- **Target Table**: `identity.user_sessions`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on user_sessions
- **Target Query Pattern**: `SELECT * FROM user_sessions WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-033
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_sessions_index_033
    ON identity.user_sessions USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-034: `idx_user_sessions_index_034` on `identity.user_sessions`

- **Index Identifier**: `INDEX-034`
- **Target Table**: `identity.user_sessions`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on user_sessions
- **Target Query Pattern**: `SELECT * FROM user_sessions WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-034
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_sessions_index_034
    ON identity.user_sessions USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-035: `idx_roles_index_035` on `identity.roles`

- **Index Identifier**: `INDEX-035`
- **Target Table**: `identity.roles`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on roles
- **Target Query Pattern**: `SELECT * FROM roles WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-035
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_roles_index_035
    ON identity.roles USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-036: `idx_roles_index_036` on `identity.roles`

- **Index Identifier**: `INDEX-036`
- **Target Table**: `identity.roles`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on roles
- **Target Query Pattern**: `SELECT * FROM roles WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-036
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_roles_index_036
    ON identity.roles USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-037: `idx_permissions_index_037` on `identity.permissions`

- **Index Identifier**: `INDEX-037`
- **Target Table**: `identity.permissions`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on permissions
- **Target Query Pattern**: `SELECT * FROM permissions WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-037
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_permissions_index_037
    ON identity.permissions USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-038: `idx_permissions_index_038` on `identity.permissions`

- **Index Identifier**: `INDEX-038`
- **Target Table**: `identity.permissions`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on permissions
- **Target Query Pattern**: `SELECT * FROM permissions WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-038
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_permissions_index_038
    ON identity.permissions USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-039: `idx_role_permissions_index_039` on `identity.role_permissions`

- **Index Identifier**: `INDEX-039`
- **Target Table**: `identity.role_permissions`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on role_permissions
- **Target Query Pattern**: `SELECT * FROM role_permissions WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-039
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_role_permissions_index_039
    ON identity.role_permissions USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-040: `idx_role_permissions_index_040` on `identity.role_permissions`

- **Index Identifier**: `INDEX-040`
- **Target Table**: `identity.role_permissions`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on role_permissions
- **Target Query Pattern**: `SELECT * FROM role_permissions WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-040
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_role_permissions_index_040
    ON identity.role_permissions USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-041: `idx_user_roles_index_041` on `identity.user_roles`

- **Index Identifier**: `INDEX-041`
- **Target Table**: `identity.user_roles`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on user_roles
- **Target Query Pattern**: `SELECT * FROM user_roles WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-041
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_roles_index_041
    ON identity.user_roles USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-042: `idx_user_roles_index_042` on `identity.user_roles`

- **Index Identifier**: `INDEX-042`
- **Target Table**: `identity.user_roles`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on user_roles
- **Target Query Pattern**: `SELECT * FROM user_roles WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-042
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_roles_index_042
    ON identity.user_roles USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-043: `idx_facilities_index_043` on `identity.facilities`

- **Index Identifier**: `INDEX-043`
- **Target Table**: `identity.facilities`
- **Indexed Columns / Expression**: `(ward_number)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on facilities
- **Target Query Pattern**: `SELECT * FROM facilities WHERE ward_number = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-043
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_facilities_index_043
    ON identity.facilities USING b-tree (ward_number)
    WHERE deleted_at IS NULL;
```

### INDEX-044: `idx_facilities_index_044` on `identity.facilities`

- **Index Identifier**: `INDEX-044`
- **Target Table**: `identity.facilities`
- **Indexed Columns / Expression**: `(created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on facilities
- **Target Query Pattern**: `SELECT * FROM facilities WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-044
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_facilities_index_044
    ON identity.facilities USING composite (created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-045: `idx_facility_rooms_index_045` on `identity.facility_rooms`

- **Index Identifier**: `INDEX-045`
- **Target Table**: `identity.facility_rooms`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on facility_rooms
- **Target Query Pattern**: `SELECT * FROM facility_rooms WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-045
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_facility_rooms_index_045
    ON identity.facility_rooms USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-046: `idx_facility_rooms_index_046` on `identity.facility_rooms`

- **Index Identifier**: `INDEX-046`
- **Target Table**: `identity.facility_rooms`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on facility_rooms
- **Target Query Pattern**: `SELECT * FROM facility_rooms WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-046
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_facility_rooms_index_046
    ON identity.facility_rooms USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-047: `idx_staff_profiles_index_047` on `identity.staff_profiles`

- **Index Identifier**: `INDEX-047`
- **Target Table**: `identity.staff_profiles`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on staff_profiles
- **Target Query Pattern**: `SELECT * FROM staff_profiles WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-047
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_staff_profiles_index_047
    ON identity.staff_profiles USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-048: `idx_staff_profiles_index_048` on `identity.staff_profiles`

- **Index Identifier**: `INDEX-048`
- **Target Table**: `identity.staff_profiles`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on staff_profiles
- **Target Query Pattern**: `SELECT * FROM staff_profiles WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-048
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_staff_profiles_index_048
    ON identity.staff_profiles USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-049: `idx_staff_shifts_index_049` on `identity.staff_shifts`

- **Index Identifier**: `INDEX-049`
- **Target Table**: `identity.staff_shifts`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on staff_shifts
- **Target Query Pattern**: `SELECT * FROM staff_shifts WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-049
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_staff_shifts_index_049
    ON identity.staff_shifts USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-050: `idx_staff_shifts_index_050` on `identity.staff_shifts`

- **Index Identifier**: `INDEX-050`
- **Target Table**: `identity.staff_shifts`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on staff_shifts
- **Target Query Pattern**: `SELECT * FROM staff_shifts WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-050
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_staff_shifts_index_050
    ON identity.staff_shifts USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-051: `idx_system_configs_index_051` on `identity.system_configs`

- **Index Identifier**: `INDEX-051`
- **Target Table**: `identity.system_configs`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on system_configs
- **Target Query Pattern**: `SELECT * FROM system_configs WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-051
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_system_configs_index_051
    ON identity.system_configs USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-052: `idx_system_configs_index_052` on `identity.system_configs`

- **Index Identifier**: `INDEX-052`
- **Target Table**: `identity.system_configs`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on system_configs
- **Target Query Pattern**: `SELECT * FROM system_configs WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-052
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_system_configs_index_052
    ON identity.system_configs USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-053: `idx_patients_index_053` on `intake.patients`

- **Index Identifier**: `INDEX-053`
- **Target Table**: `intake.patients`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on patients
- **Target Query Pattern**: `SELECT * FROM patients WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-053
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patients_index_053
    ON intake.patients USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-054: `idx_patients_index_054` on `intake.patients`

- **Index Identifier**: `INDEX-054`
- **Target Table**: `intake.patients`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on patients
- **Target Query Pattern**: `SELECT * FROM patients WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-054
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patients_index_054
    ON intake.patients USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-055: `idx_patient_identifiers_index_055` on `intake.patient_identifiers`

- **Index Identifier**: `INDEX-055`
- **Target Table**: `intake.patient_identifiers`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on patient_identifiers
- **Target Query Pattern**: `SELECT * FROM patient_identifiers WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-055
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patient_identifiers_index_055
    ON intake.patient_identifiers USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-056: `idx_patient_identifiers_index_056` on `intake.patient_identifiers`

- **Index Identifier**: `INDEX-056`
- **Target Table**: `intake.patient_identifiers`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on patient_identifiers
- **Target Query Pattern**: `SELECT * FROM patient_identifiers WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-056
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patient_identifiers_index_056
    ON intake.patient_identifiers USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-057: `idx_patient_contacts_index_057` on `intake.patient_contacts`

- **Index Identifier**: `INDEX-057`
- **Target Table**: `intake.patient_contacts`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on patient_contacts
- **Target Query Pattern**: `SELECT * FROM patient_contacts WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-057
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patient_contacts_index_057
    ON intake.patient_contacts USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-058: `idx_patient_contacts_index_058` on `intake.patient_contacts`

- **Index Identifier**: `INDEX-058`
- **Target Table**: `intake.patient_contacts`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on patient_contacts
- **Target Query Pattern**: `SELECT * FROM patient_contacts WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-058
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patient_contacts_index_058
    ON intake.patient_contacts USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-059: `idx_patient_addresses_index_059` on `intake.patient_addresses`

- **Index Identifier**: `INDEX-059`
- **Target Table**: `intake.patient_addresses`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on patient_addresses
- **Target Query Pattern**: `SELECT * FROM patient_addresses WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-059
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patient_addresses_index_059
    ON intake.patient_addresses USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-060: `idx_patient_addresses_index_060` on `intake.patient_addresses`

- **Index Identifier**: `INDEX-060`
- **Target Table**: `intake.patient_addresses`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on patient_addresses
- **Target Query Pattern**: `SELECT * FROM patient_addresses WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-060
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patient_addresses_index_060
    ON intake.patient_addresses USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-061: `idx_consent_records_index_061` on `intake.consent_records`

- **Index Identifier**: `INDEX-061`
- **Target Table**: `intake.consent_records`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on consent_records
- **Target Query Pattern**: `SELECT * FROM consent_records WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-061
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_consent_records_index_061
    ON intake.consent_records USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-062: `idx_consent_records_index_062` on `intake.consent_records`

- **Index Identifier**: `INDEX-062`
- **Target Table**: `intake.consent_records`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on consent_records
- **Target Query Pattern**: `SELECT * FROM consent_records WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-062
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_consent_records_index_062
    ON intake.consent_records USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-063: `idx_tokens_index_063` on `intake.tokens`

- **Index Identifier**: `INDEX-063`
- **Target Table**: `intake.tokens`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on tokens
- **Target Query Pattern**: `SELECT * FROM tokens WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-063
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tokens_index_063
    ON intake.tokens USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-064: `idx_tokens_index_064` on `intake.tokens`

- **Index Identifier**: `INDEX-064`
- **Target Table**: `intake.tokens`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on tokens
- **Target Query Pattern**: `SELECT * FROM tokens WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-064
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tokens_index_064
    ON intake.tokens USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-065: `idx_queue_entries_index_065` on `intake.queue_entries`

- **Index Identifier**: `INDEX-065`
- **Target Table**: `intake.queue_entries`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on queue_entries
- **Target Query Pattern**: `SELECT * FROM queue_entries WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-065
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_queue_entries_index_065
    ON intake.queue_entries USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-066: `idx_queue_entries_index_066` on `intake.queue_entries`

- **Index Identifier**: `INDEX-066`
- **Target Table**: `intake.queue_entries`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on queue_entries
- **Target Query Pattern**: `SELECT * FROM queue_entries WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-066
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_queue_entries_index_066
    ON intake.queue_entries USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-067: `idx_triage_assessments_index_067` on `intake.triage_assessments`

- **Index Identifier**: `INDEX-067`
- **Target Table**: `intake.triage_assessments`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on triage_assessments
- **Target Query Pattern**: `SELECT * FROM triage_assessments WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-067
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_triage_assessments_index_067
    ON intake.triage_assessments USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-068: `idx_triage_assessments_index_068` on `intake.triage_assessments`

- **Index Identifier**: `INDEX-068`
- **Target Table**: `intake.triage_assessments`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on triage_assessments
- **Target Query Pattern**: `SELECT * FROM triage_assessments WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-068
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_triage_assessments_index_068
    ON intake.triage_assessments USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-069: `idx_patient_vitals_index_069` on `intake.patient_vitals`

- **Index Identifier**: `INDEX-069`
- **Target Table**: `intake.patient_vitals`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on patient_vitals
- **Target Query Pattern**: `SELECT * FROM patient_vitals WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-069
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patient_vitals_index_069
    ON intake.patient_vitals USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-070: `idx_patient_vitals_index_070` on `intake.patient_vitals`

- **Index Identifier**: `INDEX-070`
- **Target Table**: `intake.patient_vitals`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on patient_vitals
- **Target Query Pattern**: `SELECT * FROM patient_vitals WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-070
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_patient_vitals_index_070
    ON intake.patient_vitals USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-071: `idx_danger_alerts_index_071` on `intake.danger_alerts`

- **Index Identifier**: `INDEX-071`
- **Target Table**: `intake.danger_alerts`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on danger_alerts
- **Target Query Pattern**: `SELECT * FROM danger_alerts WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-071
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_danger_alerts_index_071
    ON intake.danger_alerts USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-072: `idx_danger_alerts_index_072` on `intake.danger_alerts`

- **Index Identifier**: `INDEX-072`
- **Target Table**: `intake.danger_alerts`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on danger_alerts
- **Target Query Pattern**: `SELECT * FROM danger_alerts WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-072
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_danger_alerts_index_072
    ON intake.danger_alerts USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-073: `idx_clinical_encounters_index_073` on `clinical.clinical_encounters`

- **Index Identifier**: `INDEX-073`
- **Target Table**: `clinical.clinical_encounters`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on clinical_encounters
- **Target Query Pattern**: `SELECT * FROM clinical_encounters WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-073
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_clinical_encounters_index_073
    ON clinical.clinical_encounters USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-074: `idx_clinical_encounters_index_074` on `clinical.clinical_encounters`

- **Index Identifier**: `INDEX-074`
- **Target Table**: `clinical.clinical_encounters`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on clinical_encounters
- **Target Query Pattern**: `SELECT * FROM clinical_encounters WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-074
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_clinical_encounters_index_074
    ON clinical.clinical_encounters USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-075: `idx_clinical_notes_index_075` on `clinical.clinical_notes`

- **Index Identifier**: `INDEX-075`
- **Target Table**: `clinical.clinical_notes`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on clinical_notes
- **Target Query Pattern**: `SELECT * FROM clinical_notes WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-075
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_clinical_notes_index_075
    ON clinical.clinical_notes USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-076: `idx_clinical_notes_index_076` on `clinical.clinical_notes`

- **Index Identifier**: `INDEX-076`
- **Target Table**: `clinical.clinical_notes`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on clinical_notes
- **Target Query Pattern**: `SELECT * FROM clinical_notes WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-076
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_clinical_notes_index_076
    ON clinical.clinical_notes USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-077: `idx_diagnoses_index_077` on `clinical.diagnoses`

- **Index Identifier**: `INDEX-077`
- **Target Table**: `clinical.diagnoses`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on diagnoses
- **Target Query Pattern**: `SELECT * FROM diagnoses WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-077
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_diagnoses_index_077
    ON clinical.diagnoses USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-078: `idx_diagnoses_index_078` on `clinical.diagnoses`

- **Index Identifier**: `INDEX-078`
- **Target Table**: `clinical.diagnoses`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on diagnoses
- **Target Query Pattern**: `SELECT * FROM diagnoses WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-078
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_diagnoses_index_078
    ON clinical.diagnoses USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-079: `idx_prescriptions_index_079` on `clinical.prescriptions`

- **Index Identifier**: `INDEX-079`
- **Target Table**: `clinical.prescriptions`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on prescriptions
- **Target Query Pattern**: `SELECT * FROM prescriptions WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-079
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_prescriptions_index_079
    ON clinical.prescriptions USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-080: `idx_prescriptions_index_080` on `clinical.prescriptions`

- **Index Identifier**: `INDEX-080`
- **Target Table**: `clinical.prescriptions`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on prescriptions
- **Target Query Pattern**: `SELECT * FROM prescriptions WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-080
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_prescriptions_index_080
    ON clinical.prescriptions USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-081: `idx_prescription_items_index_081` on `clinical.prescription_items`

- **Index Identifier**: `INDEX-081`
- **Target Table**: `clinical.prescription_items`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on prescription_items
- **Target Query Pattern**: `SELECT * FROM prescription_items WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-081
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_prescription_items_index_081
    ON clinical.prescription_items USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-082: `idx_prescription_items_index_082` on `clinical.prescription_items`

- **Index Identifier**: `INDEX-082`
- **Target Table**: `clinical.prescription_items`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on prescription_items
- **Target Query Pattern**: `SELECT * FROM prescription_items WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-082
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_prescription_items_index_082
    ON clinical.prescription_items USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-083: `idx_lab_orders_index_083` on `clinical.lab_orders`

- **Index Identifier**: `INDEX-083`
- **Target Table**: `clinical.lab_orders`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on lab_orders
- **Target Query Pattern**: `SELECT * FROM lab_orders WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-083
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_lab_orders_index_083
    ON clinical.lab_orders USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-084: `idx_lab_orders_index_084` on `clinical.lab_orders`

- **Index Identifier**: `INDEX-084`
- **Target Table**: `clinical.lab_orders`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on lab_orders
- **Target Query Pattern**: `SELECT * FROM lab_orders WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-084
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_lab_orders_index_084
    ON clinical.lab_orders USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-085: `idx_lab_order_items_index_085` on `clinical.lab_order_items`

- **Index Identifier**: `INDEX-085`
- **Target Table**: `clinical.lab_order_items`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on lab_order_items
- **Target Query Pattern**: `SELECT * FROM lab_order_items WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-085
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_lab_order_items_index_085
    ON clinical.lab_order_items USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-086: `idx_lab_order_items_index_086` on `clinical.lab_order_items`

- **Index Identifier**: `INDEX-086`
- **Target Table**: `clinical.lab_order_items`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on lab_order_items
- **Target Query Pattern**: `SELECT * FROM lab_order_items WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-086
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_lab_order_items_index_086
    ON clinical.lab_order_items USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-087: `idx_lab_results_index_087` on `clinical.lab_results`

- **Index Identifier**: `INDEX-087`
- **Target Table**: `clinical.lab_results`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on lab_results
- **Target Query Pattern**: `SELECT * FROM lab_results WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-087
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_lab_results_index_087
    ON clinical.lab_results USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-088: `idx_lab_results_index_088` on `clinical.lab_results`

- **Index Identifier**: `INDEX-088`
- **Target Table**: `clinical.lab_results`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on lab_results
- **Target Query Pattern**: `SELECT * FROM lab_results WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-088
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_lab_results_index_088
    ON clinical.lab_results USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-089: `idx_teleconsultations_index_089` on `clinical.teleconsultations`

- **Index Identifier**: `INDEX-089`
- **Target Table**: `clinical.teleconsultations`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on teleconsultations
- **Target Query Pattern**: `SELECT * FROM teleconsultations WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-089
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_teleconsultations_index_089
    ON clinical.teleconsultations USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-090: `idx_teleconsultations_index_090` on `clinical.teleconsultations`

- **Index Identifier**: `INDEX-090`
- **Target Table**: `clinical.teleconsultations`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on teleconsultations
- **Target Query Pattern**: `SELECT * FROM teleconsultations WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-090
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_teleconsultations_index_090
    ON clinical.teleconsultations USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-091: `idx_formulary_drugs_index_091` on `pharmacy.formulary_drugs`

- **Index Identifier**: `INDEX-091`
- **Target Table**: `pharmacy.formulary_drugs`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on formulary_drugs
- **Target Query Pattern**: `SELECT * FROM formulary_drugs WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-091
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_formulary_drugs_index_091
    ON pharmacy.formulary_drugs USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-092: `idx_formulary_drugs_index_092` on `pharmacy.formulary_drugs`

- **Index Identifier**: `INDEX-092`
- **Target Table**: `pharmacy.formulary_drugs`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on formulary_drugs
- **Target Query Pattern**: `SELECT * FROM formulary_drugs WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-092
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_formulary_drugs_index_092
    ON pharmacy.formulary_drugs USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-093: `idx_drug_categories_index_093` on `pharmacy.drug_categories`

- **Index Identifier**: `INDEX-093`
- **Target Table**: `pharmacy.drug_categories`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on drug_categories
- **Target Query Pattern**: `SELECT * FROM drug_categories WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-093
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_drug_categories_index_093
    ON pharmacy.drug_categories USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-094: `idx_drug_categories_index_094` on `pharmacy.drug_categories`

- **Index Identifier**: `INDEX-094`
- **Target Table**: `pharmacy.drug_categories`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on drug_categories
- **Target Query Pattern**: `SELECT * FROM drug_categories WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-094
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_drug_categories_index_094
    ON pharmacy.drug_categories USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-095: `idx_pharmacy_batches_index_095` on `pharmacy.pharmacy_batches`

- **Index Identifier**: `INDEX-095`
- **Target Table**: `pharmacy.pharmacy_batches`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on pharmacy_batches
- **Target Query Pattern**: `SELECT * FROM pharmacy_batches WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-095
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_pharmacy_batches_index_095
    ON pharmacy.pharmacy_batches USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-096: `idx_pharmacy_batches_index_096` on `pharmacy.pharmacy_batches`

- **Index Identifier**: `INDEX-096`
- **Target Table**: `pharmacy.pharmacy_batches`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on pharmacy_batches
- **Target Query Pattern**: `SELECT * FROM pharmacy_batches WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-096
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_pharmacy_batches_index_096
    ON pharmacy.pharmacy_batches USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-097: `idx_clinic_stock_index_097` on `pharmacy.clinic_stock`

- **Index Identifier**: `INDEX-097`
- **Target Table**: `pharmacy.clinic_stock`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on clinic_stock
- **Target Query Pattern**: `SELECT * FROM clinic_stock WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-097
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_clinic_stock_index_097
    ON pharmacy.clinic_stock USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-098: `idx_clinic_stock_index_098` on `pharmacy.clinic_stock`

- **Index Identifier**: `INDEX-098`
- **Target Table**: `pharmacy.clinic_stock`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on clinic_stock
- **Target Query Pattern**: `SELECT * FROM clinic_stock WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-098
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_clinic_stock_index_098
    ON pharmacy.clinic_stock USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-099: `idx_dispensations_index_099` on `pharmacy.dispensations`

- **Index Identifier**: `INDEX-099`
- **Target Table**: `pharmacy.dispensations`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on dispensations
- **Target Query Pattern**: `SELECT * FROM dispensations WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-099
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_dispensations_index_099
    ON pharmacy.dispensations USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-100: `idx_dispensations_index_100` on `pharmacy.dispensations`

- **Index Identifier**: `INDEX-100`
- **Target Table**: `pharmacy.dispensations`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on dispensations
- **Target Query Pattern**: `SELECT * FROM dispensations WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-100
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_dispensations_index_100
    ON pharmacy.dispensations USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-101: `idx_dispensation_items_index_101` on `pharmacy.dispensation_items`

- **Index Identifier**: `INDEX-101`
- **Target Table**: `pharmacy.dispensation_items`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on dispensation_items
- **Target Query Pattern**: `SELECT * FROM dispensation_items WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-101
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_dispensation_items_index_101
    ON pharmacy.dispensation_items USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-102: `idx_dispensation_items_index_102` on `pharmacy.dispensation_items`

- **Index Identifier**: `INDEX-102`
- **Target Table**: `pharmacy.dispensation_items`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on dispensation_items
- **Target Query Pattern**: `SELECT * FROM dispensation_items WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-102
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_dispensation_items_index_102
    ON pharmacy.dispensation_items USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-103: `idx_stock_movements_index_103` on `pharmacy.stock_movements`

- **Index Identifier**: `INDEX-103`
- **Target Table**: `pharmacy.stock_movements`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on stock_movements
- **Target Query Pattern**: `SELECT * FROM stock_movements WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-103
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_stock_movements_index_103
    ON pharmacy.stock_movements USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-104: `idx_stock_movements_index_104` on `pharmacy.stock_movements`

- **Index Identifier**: `INDEX-104`
- **Target Table**: `pharmacy.stock_movements`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on stock_movements
- **Target Query Pattern**: `SELECT * FROM stock_movements WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-104
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_stock_movements_index_104
    ON pharmacy.stock_movements USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-105: `idx_drug_indents_index_105` on `pharmacy.drug_indents`

- **Index Identifier**: `INDEX-105`
- **Target Table**: `pharmacy.drug_indents`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on drug_indents
- **Target Query Pattern**: `SELECT * FROM drug_indents WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-105
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_drug_indents_index_105
    ON pharmacy.drug_indents USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-106: `idx_drug_indents_index_106` on `pharmacy.drug_indents`

- **Index Identifier**: `INDEX-106`
- **Target Table**: `pharmacy.drug_indents`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on drug_indents
- **Target Query Pattern**: `SELECT * FROM drug_indents WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-106
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_drug_indents_index_106
    ON pharmacy.drug_indents USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-107: `idx_indent_items_index_107` on `pharmacy.indent_items`

- **Index Identifier**: `INDEX-107`
- **Target Table**: `pharmacy.indent_items`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on indent_items
- **Target Query Pattern**: `SELECT * FROM indent_items WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-107
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_indent_items_index_107
    ON pharmacy.indent_items USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-108: `idx_indent_items_index_108` on `pharmacy.indent_items`

- **Index Identifier**: `INDEX-108`
- **Target Table**: `pharmacy.indent_items`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on indent_items
- **Target Query Pattern**: `SELECT * FROM indent_items WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-108
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_indent_items_index_108
    ON pharmacy.indent_items USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-109: `idx_cold_chain_devices_index_109` on `pharmacy.cold_chain_devices`

- **Index Identifier**: `INDEX-109`
- **Target Table**: `pharmacy.cold_chain_devices`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on cold_chain_devices
- **Target Query Pattern**: `SELECT * FROM cold_chain_devices WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-109
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_cold_chain_devices_index_109
    ON pharmacy.cold_chain_devices USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-110: `idx_cold_chain_devices_index_110` on `pharmacy.cold_chain_devices`

- **Index Identifier**: `INDEX-110`
- **Target Table**: `pharmacy.cold_chain_devices`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on cold_chain_devices
- **Target Query Pattern**: `SELECT * FROM cold_chain_devices WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-110
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_cold_chain_devices_index_110
    ON pharmacy.cold_chain_devices USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-111: `idx_cold_chain_telemetry_index_111` on `pharmacy.cold_chain_telemetry`

- **Index Identifier**: `INDEX-111`
- **Target Table**: `pharmacy.cold_chain_telemetry`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on cold_chain_telemetry
- **Target Query Pattern**: `SELECT * FROM cold_chain_telemetry WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-111
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_cold_chain_telemetry_index_111
    ON pharmacy.cold_chain_telemetry USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-112: `idx_cold_chain_telemetry_index_112` on `pharmacy.cold_chain_telemetry`

- **Index Identifier**: `INDEX-112`
- **Target Table**: `pharmacy.cold_chain_telemetry`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on cold_chain_telemetry
- **Target Query Pattern**: `SELECT * FROM cold_chain_telemetry WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-112
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_cold_chain_telemetry_index_112
    ON pharmacy.cold_chain_telemetry USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-113: `idx_referrals_index_113` on `continuity.referrals`

- **Index Identifier**: `INDEX-113`
- **Target Table**: `continuity.referrals`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on referrals
- **Target Query Pattern**: `SELECT * FROM referrals WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-113
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_referrals_index_113
    ON continuity.referrals USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-114: `idx_referrals_index_114` on `continuity.referrals`

- **Index Identifier**: `INDEX-114`
- **Target Table**: `continuity.referrals`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on referrals
- **Target Query Pattern**: `SELECT * FROM referrals WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-114
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_referrals_index_114
    ON continuity.referrals USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-115: `idx_referral_counter_notes_index_115` on `continuity.referral_counter_notes`

- **Index Identifier**: `INDEX-115`
- **Target Table**: `continuity.referral_counter_notes`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on referral_counter_notes
- **Target Query Pattern**: `SELECT * FROM referral_counter_notes WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-115
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_referral_counter_notes_index_115
    ON continuity.referral_counter_notes USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-116: `idx_referral_counter_notes_index_116` on `continuity.referral_counter_notes`

- **Index Identifier**: `INDEX-116`
- **Target Table**: `continuity.referral_counter_notes`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on referral_counter_notes
- **Target Query Pattern**: `SELECT * FROM referral_counter_notes WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-116
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_referral_counter_notes_index_116
    ON continuity.referral_counter_notes USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-117: `idx_ncd_episodes_index_117` on `continuity.ncd_episodes`

- **Index Identifier**: `INDEX-117`
- **Target Table**: `continuity.ncd_episodes`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on ncd_episodes
- **Target Query Pattern**: `SELECT * FROM ncd_episodes WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-117
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_ncd_episodes_index_117
    ON continuity.ncd_episodes USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-118: `idx_ncd_episodes_index_118` on `continuity.ncd_episodes`

- **Index Identifier**: `INDEX-118`
- **Target Table**: `continuity.ncd_episodes`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on ncd_episodes
- **Target Query Pattern**: `SELECT * FROM ncd_episodes WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-118
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_ncd_episodes_index_118
    ON continuity.ncd_episodes USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-119: `idx_follow_up_schedules_index_119` on `continuity.follow_up_schedules`

- **Index Identifier**: `INDEX-119`
- **Target Table**: `continuity.follow_up_schedules`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on follow_up_schedules
- **Target Query Pattern**: `SELECT * FROM follow_up_schedules WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-119
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_follow_up_schedules_index_119
    ON continuity.follow_up_schedules USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-120: `idx_follow_up_schedules_index_120` on `continuity.follow_up_schedules`

- **Index Identifier**: `INDEX-120`
- **Target Table**: `continuity.follow_up_schedules`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on follow_up_schedules
- **Target Query Pattern**: `SELECT * FROM follow_up_schedules WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-120
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_follow_up_schedules_index_120
    ON continuity.follow_up_schedules USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-121: `idx_notifications_index_121` on `continuity.notifications`

- **Index Identifier**: `INDEX-121`
- **Target Table**: `continuity.notifications`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on notifications
- **Target Query Pattern**: `SELECT * FROM notifications WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-121
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_notifications_index_121
    ON continuity.notifications USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-122: `idx_notifications_index_122` on `continuity.notifications`

- **Index Identifier**: `INDEX-122`
- **Target Table**: `continuity.notifications`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on notifications
- **Target Query Pattern**: `SELECT * FROM notifications WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-122
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_notifications_index_122
    ON continuity.notifications USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-123: `idx_grievances_index_123` on `continuity.grievances`

- **Index Identifier**: `INDEX-123`
- **Target Table**: `continuity.grievances`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on grievances
- **Target Query Pattern**: `SELECT * FROM grievances WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-123
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_grievances_index_123
    ON continuity.grievances USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-124: `idx_grievances_index_124` on `continuity.grievances`

- **Index Identifier**: `INDEX-124`
- **Target Table**: `continuity.grievances`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on grievances
- **Target Query Pattern**: `SELECT * FROM grievances WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-124
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_grievances_index_124
    ON continuity.grievances USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-125: `idx_helpdesk_tickets_index_125` on `continuity.helpdesk_tickets`

- **Index Identifier**: `INDEX-125`
- **Target Table**: `continuity.helpdesk_tickets`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on helpdesk_tickets
- **Target Query Pattern**: `SELECT * FROM helpdesk_tickets WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-125
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_helpdesk_tickets_index_125
    ON continuity.helpdesk_tickets USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-126: `idx_helpdesk_tickets_index_126` on `continuity.helpdesk_tickets`

- **Index Identifier**: `INDEX-126`
- **Target Table**: `continuity.helpdesk_tickets`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on helpdesk_tickets
- **Target Query Pattern**: `SELECT * FROM helpdesk_tickets WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-126
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_helpdesk_tickets_index_126
    ON continuity.helpdesk_tickets USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-127: `idx_audit_events_index_127` on `audit.audit_events`

- **Index Identifier**: `INDEX-127`
- **Target Table**: `audit.audit_events`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on audit_events
- **Target Query Pattern**: `SELECT * FROM audit_events WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-127
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_audit_events_index_127
    ON audit.audit_events USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-128: `idx_audit_events_index_128` on `audit.audit_events`

- **Index Identifier**: `INDEX-128`
- **Target Table**: `audit.audit_events`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on audit_events
- **Target Query Pattern**: `SELECT * FROM audit_events WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-128
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_audit_events_index_128
    ON audit.audit_events USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-129: `idx_offline_mutation_log_index_129` on `sync.offline_mutation_log`

- **Index Identifier**: `INDEX-129`
- **Target Table**: `sync.offline_mutation_log`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on offline_mutation_log
- **Target Query Pattern**: `SELECT * FROM offline_mutation_log WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-129
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_offline_mutation_log_index_129
    ON sync.offline_mutation_log USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-130: `idx_offline_mutation_log_index_130` on `sync.offline_mutation_log`

- **Index Identifier**: `INDEX-130`
- **Target Table**: `sync.offline_mutation_log`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on offline_mutation_log
- **Target Query Pattern**: `SELECT * FROM offline_mutation_log WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-130
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_offline_mutation_log_index_130
    ON sync.offline_mutation_log USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

### INDEX-131: `idx_abdm_artifacts_index_131` on `sync.abdm_artifacts`

- **Index Identifier**: `INDEX-131`
- **Target Table**: `sync.abdm_artifacts`
- **Indexed Columns / Expression**: `(facility_id)`
- **Engine Type**: `B-tree` (Non-Unique)
- **Technical Purpose**: Accelerate clinic facility filtering on abdm_artifacts
- **Target Query Pattern**: `SELECT * FROM abdm_artifacts WHERE facility_id = $1`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `Moderate`
- **Resource Impact**: Write Cost `Low`; Storage Footprint `Low`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created in background
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Mandatory FK index - retained permanently

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-131
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_abdm_artifacts_index_131
    ON sync.abdm_artifacts USING b-tree (facility_id)
    WHERE deleted_at IS NULL;
```

### INDEX-132: `idx_abdm_artifacts_index_132` on `sync.abdm_artifacts`

- **Index Identifier**: `INDEX-132`
- **Target Table**: `sync.abdm_artifacts`
- **Indexed Columns / Expression**: `(status, created_at)`
- **Engine Type**: `Composite B-tree` (Non-Unique)
- **Technical Purpose**: Optimize operational status workflows and temporal slicing on abdm_artifacts
- **Target Query Pattern**: `SELECT * FROM abdm_artifacts WHERE status = $1 ORDER BY created_at DESC`
- **Expected Selectivity & Cardinality**: Selectivity `High`; Cardinality `High`
- **Resource Impact**: Write Cost `Medium`; Storage Footprint `Medium`
- **Partial Predicate**: `deleted_at IS NULL`
- **Functional Expression**: `None (Direct Column Values)`
- **Covering Columns (INCLUDE)**: `None`
- **Concurrency & Rollout**: CONCURRENTLY created
- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`
- **Decommissioning Criteria**: Evaluated quarterly based on scan metrics

```sql
-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for INDEX-132
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_abdm_artifacts_index_132
    ON sync.abdm_artifacts USING composite (status, created_at)
    WHERE deleted_at IS NULL;
```

## 6. Operational Reindexing & Bloat Remediation Runbook

Over time, continuous updates on high-frequency tables cause B-tree index bloat. The following operational runbook governs maintenance without table locks:

### 6.1 Index Bloat Detection Query
```sql
-- DOCUMENTATION-ONLY SQL: Index Bloat Detection Query
SELECT
    schemaname,
    relname AS table_name,
    indexrelname AS index_name,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC LIMIT 20;
```

### 6.2 Zero-Downtime Reindexing Runbook
To compact bloated B-tree indexes without acquiring exclusive table locks:
1. **Execute Concurrent Reindex**: `REINDEX INDEX CONCURRENTLY <index_name>;`
2. **Monitor Reindex Progress**: Query `pg_stat_progress_create_index` to observe processing phases.
3. **Handle Interrupted Builds**: If a reindex is cancelled, drop the temporary invalid index: `DROP INDEX CONCURRENTLY <index_name>_ccnew;`

## 7. Conclusion & Index Verification Baseline

The 132 database indexes cataloged in this specification provide complete, high-selectivity query acceleration for the Namma Clinic platform. Every index has been assigned an explicit engine type, selectivity profile, and zero-downtime concurrent rollout plan.
