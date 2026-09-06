"""
gen_db_15_seeds.py
Generates docs/07-database/15-seed-data-strategy.md
Target: 2,500 - 3,500 substantive lines.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from scripts.database.db_core_data import (
    SEEDS, SEED_MAP, TABLES, TABLE_NAME_MAP
)
from scripts.database.db_gen_common import write_db_doc

def generate_doc_15():
    lines = []

    lines.append("# Phase 07 — Master Database Seed Data Strategy & Reference Catalogs")
    lines.append("")
    lines.append("> **Document Identifier**: `DB-SEED-001`  ")
    lines.append("> **System**: Namma Clinic Digital Health & Operations Platform  ")
    lines.append("> **Municipal Authority**: Greater Bengaluru Authority (GBA) / BBMP Health Department  ")
    lines.append("> **Status**: APPROVED SEED DATA BASELINE  ")
    lines.append(f"> **Cataloged Seed Datasets**: {len(SEEDS)} Master Datasets (`SEED-001` to `SEED-{len(SEEDS):03d}`)  ")
    lines.append("> **Operational Standard**: 100% Idempotent Upserts, Environment-Segregated, Zero Real PII  ")
    lines.append("> **Notice**: All SQL blocks contained herein are strictly **DOCUMENTATION-ONLY SQL**. Zero runtime code or migrations are executed during this phase.  ")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 1. Executive Summary & Seed Engineering Framework
    lines.append("## 1. Executive Summary & Seed Engineering Framework")
    lines.append("")
    lines.append("In an enterprise municipal healthcare platform, database seeding is a mission-critical discipline. Seed data encompasses all static, reference, and operational baseline records necessary for the platform to bootstrap from an empty schema into a fully operational state capable of servicing 450 Namma Clinics across Bengaluru.")
    lines.append("")
    lines.append("Seed data serves three distinct architectural tiers:")
    lines.append("1. **Core System Metadata**: Fundamental relational lookup tables, RBAC roles, security permissions, and lifecycle state machines required by microservices for authentication and transaction routing.")
    lines.append("2. **Clinical & Municipal Reference Standards**: Curated healthcare vocabularies (ICD-10 diagnosis codes, WHO Essential Medicines List, LOINC lab test panels) and Bengaluru municipal geography (8 administrative zones, 243 municipal wards, and clinic facility registries).")
    lines.append("3. **Non-Production Synthetic Testing Cohorts**: Statistically representative, synthetic patient demographics, clinical encounters, and pharmacy inventories used strictly in development, staging, load testing, and training environments.")
    lines.append("")
    lines.append("This document establishes the master seed data engineering standard. It specifies 15 canonical seed datasets (`SEED-001` to `SEED-015`), defining explicit idempotency keys (`ON CONFLICT DO UPDATE`), synthetic generation rules, environment isolation boundaries, and automated rollback protocols.")
    lines.append("")

    # 2. Seed Engineering Invariants
    lines.append("## 2. Seed Engineering Invariants & Quality Standards")
    lines.append("")
    lines.append("All seed scripts developed for the Namma Clinic Platform must satisfy four non-negotiable architectural invariants:")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph TD")
    lines.append("    A[Invariant 1: Idempotency<br/>ON CONFLICT DO UPDATE / NOTHING] --> B[Invariant 2: Environment Isolation<br/>Production Safe vs Synthetic Staging Only]")
    lines.append("    B --> C[Invariant 3: Zero Real PII<br/>100% Synthetic Citizen Demographics]")
    lines.append("    C --> D[Invariant 4: Deterministic Ordering<br/>Strict DAG Execution Sequence]")
    lines.append("```")
    lines.append("")
    lines.append("### 2.1 The Four Invariants")
    lines.append("1. **100% Idempotency**: Every seed statement must be safe to execute multiple times against the same database without creating duplicate rows, corrupting foreign keys, or causing unique constraint errors. Every `INSERT` statement must declare an explicit `ON CONFLICT (unique_key)` clause.")
    lines.append("2. **Strict Environment Segregation**: Datasets are classified as either `PRODUCTION_SAFE` (reference data, system roles, geography) or `STAGING_DEV_ONLY` (synthetic test patients, mock encounters). Production deployment pipelines automatically exclude all non-production seed files.")
    lines.append("3. **Zero Real PII Mandate**: In compliance with the DPDP Act 2023, synthetic test datasets must never contain real citizen data. All patient names, phone numbers, and addresses must be deterministically synthesized using approved mocking rules.")
    lines.append("4. **Deterministic Execution Sequence**: Seeds must be applied in strict topological order based on foreign key hierarchies (e.g. Roles -> Permissions -> Users -> Facilities -> Clinical Master -> Clinical Data).")
    lines.append("")

    # 3. Topological Execution DAG
    lines.append("## 3. Master Topological Execution DAG (Stages 1 to 7)")
    lines.append("")
    lines.append("Seed datasets must execute in strict topological dependency order to avoid foreign key violation errors (`SQLSTATE 23503`):")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph TD")
    lines.append("    S1[Stage 1: System Roles & Permissions<br/>SEED-001, SEED-002, SEED-003] --> S2[Stage 2: Municipal Geography & Clinics<br/>SEED-004, SEED-005]")
    lines.append("    S2 --> S3[Stage 3: Clinical Terminology & Formularies<br/>SEED-006, SEED-007, SEED-008]")
    lines.append("    S3 --> S4[Stage 4: Triage & Diagnostic Standards<br/>SEED-009, SEED-010]")
    lines.append("    S4 --> S5[Stage 5: Notification & Grievance Templates<br/>SEED-011, SEED-012]")
    lines.append("    S5 --> S6[Stage 6: Cold-Chain & Device Profiles<br/>SEED-013, SEED-014]")
    lines.append("    S6 --> S7[Stage 7: Synthetic Cohort Staging Only<br/>SEED-015]")
    lines.append("```")
    lines.append("")

    # 4. Master Relational Table Seed Allocation Matrix (All 52 Tables)
    lines.append("## 4. Master Relational Table Seed Allocation Matrix (All 52 Tables)")
    lines.append("")
    lines.append("The matrix below specifies the initial seeding status for all 52 relational tables:")
    lines.append("")
    lines.append("| Table ID | Schema & Table Name | Production Seed Strategy | Staging/Dev Seed Strategy | Initial Prod Row Count | Seeding Invariant |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for t in TABLES:
        tname = t["name"]
        tschema = t["schema"]
        tid = t["id"]
        if tname in ["roles", "auth_roles"]:
            prod_s = "SEED-001 (Immutable Standard Roles)"
            stag_s = "SEED-001 + Dev Test Roles"
            rows = "30"
        elif tname in ["permissions", "auth_permissions"]:
            prod_s = "SEED-002 (System Permissions Matrix)"
            stag_s = "SEED-002 (Identical)"
            rows = "180"
        elif tname in ["facilities", "zones", "wards"]:
            prod_s = "SEED-004 (BBMP Delimited Wards & Facilities)"
            stag_s = "SEED-004 (Identical)"
            rows = "450"
        elif tname in ["drug_master"]:
            prod_s = "SEED-006 (Karnataka Essential Drugs List)"
            stag_s = "SEED-006 (Identical)"
            rows = "350"
        elif tname in ["patients", "encounters", "prescriptions"]:
            prod_s = "Zero Seed (Transactionally Generated)"
            stag_s = "SEED-015 (Synthetic Cohort: 10,000 records)"
            rows = "0"
        else:
            prod_s = "Reference Lookup / Empty Genesis"
            stag_s = "Synthetic Demonstration Fixtures"
            rows = "0-50"
        lines.append(f"| `{tid}` | `{tschema}.{tname}` | {prod_s} | {stag_s} | `{rows}` | Deterministic Upsert |")
    lines.append("")

    # 5. Master Seed Registry Table
    lines.append("## 5. Master Seed Datasets Registry (SEED-001 to SEED-015)")
    lines.append("")
    lines.append("The 15 canonical seed datasets are cataloged below:")
    lines.append("")
    lines.append("| Seed ID | Dataset Name | Functional Category | Target Table | Target Environment | Planned Record Count | PII Presence | Execution Order |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for s in SEEDS:
        lines.append(f"| **{s['id']}** | {s['name']} | `{s['category']}` | `{s['target_table']}` | `{s['environment']}` | {s['record_count']:,} rows | `{s['pii_presence']}` | Stage {s['execution_order']} |")
    lines.append("")

    # 6. Comprehensive Seed Dataset Specifications
    lines.append("## 6. Comprehensive Seed Dataset Specifications (SEED-001 to SEED-015)")
    lines.append("")
    lines.append("The following subsections provide the complete architectural specification for each seed dataset, complete with concrete documentation-only SQL blueprints, synthetic algorithms, validation queries, and rollback runbooks:")
    lines.append("")

    # Custom SQL seed scripts for all 15 datasets
    dataset_sql_blueprints = {
        "SEED-001": [
            "INSERT INTO identity.roles (id, code, name, description, is_system_standard, created_at) VALUES",
            "    ('018e3a20-0001-7000-8000-000000000001', 'CHIEF_MEDICAL_OFFICER', 'Chief Medical Officer', 'Zonal clinical oversight and statutory health policy enforcement', true, clock_timestamp()),",
            "    ('018e3a20-0002-7000-8000-000000000002', 'CLINICAL_DOCTOR', 'Medical Officer / Doctor', 'Primary outpatient clinician conducting doctor consultations', true, clock_timestamp()),",
            "    ('018e3a20-0003-7000-8000-000000000003', 'STAFF_NURSE', 'Staff Nurse', 'Vitals intake, primary triage, and outpatient nursing care', true, clock_timestamp()),",
            "    ('018e3a20-0004-7000-8000-000000000004', 'PHARMACIST', 'Clinic Pharmacist', 'Medication dispensation, batch tracking, and stock management', true, clock_timestamp()),",
            "    ('018e3a20-0005-7000-8000-000000000005', 'LAB_TECHNICIAN', 'Laboratory Technician', 'Diagnostic specimen collection, sample processing, and lab test entry', true, clock_timestamp()),",
            "    ('018e3a20-0006-7000-8000-000000000006', 'REGISTRATION_CLERK', 'Intake Registration Clerk', 'Patient demographic capture, ABHA linking, and queue token issuance', true, clock_timestamp()),",
            "    ('018e3a20-0007-7000-8000-000000000007', 'ASHA_WORKER', 'Accredited Social Health Activist', 'Community health outreach, NCD screening, and maternal tracking', true, clock_timestamp()),",
            "    ('018e3a20-0008-7000-8000-000000000008', 'ZONAL_EPIDEMIOLOGIST', 'Zonal Epidemiologist', 'Municipal disease surveillance, outbreak detection, and HMIS reporting', true, clock_timestamp()),",
            "    ('018e3a20-0009-7000-8000-000000000009', 'INVENTORY_MANAGER', 'Zonal Warehouse Stock Manager', 'Bulk pharmaceutical indent approval and inter-clinic stock balancing', true, clock_timestamp()),",
            "    ('018e3a20-0010-7000-8000-000000000010', 'SYSTEM_ADMINISTRATOR', 'Platform Security Administrator', 'Cryptographic key rotation, staff onboarding, and WORM audit inspection', true, clock_timestamp()),",
            "    ('018e3a20-0011-7000-8000-000000000011', 'PHYSIOTHERAPIST', 'Clinic Physiotherapist', 'Rehabilitation and chronic pain management consultations', true, clock_timestamp()),",
            "    ('018e3a20-0012-7000-8000-000000000012', 'CLINICAL_PSYCHOLOGIST', 'Counselor / Psychologist', 'Mental health screening and counseling sessions', true, clock_timestamp()),",
            "    ('018e3a20-0013-7000-8000-000000000013', 'DENTAL_OFFICER', 'Dental Health Officer', 'Oral hygiene screening and preventive dentistry', true, clock_timestamp()),",
            "    ('018e3a20-0014-7000-8000-000000000014', 'NUTRITIONIST', 'Clinical Nutritionist', 'Dietary counseling for diabetic and hypertensive patients', true, clock_timestamp()),",
            "    ('018e3a20-0015-7000-8000-000000000015', 'QUALITY_AUDITOR', 'Healthcare Quality Inspector', 'NABH accreditation compliance and clinical audit review', true, clock_timestamp())",
            "ON CONFLICT (code) DO UPDATE SET",
            "    name = EXCLUDED.name,",
            "    description = EXCLUDED.description,",
            "    updated_at = clock_timestamp();"
        ],
        "SEED-002": [
            "INSERT INTO identity.permissions (id, code, module, description, is_core, created_at) VALUES",
            "    ('018e3a21-0001-7000-8000-000000000001', 'PATIENT_CREATE', 'INTAKE', 'Register new citizen outpatient profile', true, clock_timestamp()),",
            "    ('018e3a21-0002-7000-8000-000000000002', 'PATIENT_READ', 'INTAKE', 'View de-identified citizen demographic summary', true, clock_timestamp()),",
            "    ('018e3a21-0003-7000-8000-000000000003', 'TOKEN_GENERATE', 'INTAKE', 'Generate daily outpatient queue token sequence', true, clock_timestamp()),",
            "    ('018e3a21-0004-7000-8000-000000000004', 'TRIAGE_ASSESS', 'CLINICAL', 'Record vital signs and ESI triage priority', true, clock_timestamp()),",
            "    ('018e3a21-0005-7000-8000-000000000005', 'CONSULTATION_WRITE', 'CLINICAL', 'Record physician clinical notes and differential diagnoses', true, clock_timestamp()),",
            "    ('018e3a21-0006-7000-8000-000000000006', 'PRESCRIPTION_CREATE', 'CLINICAL', 'Create digital electronic prescription items', true, clock_timestamp()),",
            "    ('018e3a21-0007-7000-8000-000000000007', 'PRESCRIPTION_DISPENSE', 'PHARMACY', 'Dispense prescription medications and record batch deduction', true, clock_timestamp()),",
            "    ('018e3a21-0008-7000-8000-000000000008', 'STOCK_ADJUST', 'PHARMACY', 'Perform clinic inventory stock adjustment and physical count reconciliation', true, clock_timestamp()),",
            "    ('018e3a21-0009-7000-8000-000000000009', 'LAB_ORDER_CREATE', 'LAB', 'Request clinical laboratory diagnostic tests', true, clock_timestamp()),",
            "    ('018e3a21-0010-7000-8000-000000000010', 'LAB_RESULT_VERIFY', 'LAB', 'Approve and sign off on diagnostic test findings', true, clock_timestamp()),",
            "    ('018e3a21-0011-7000-8000-000000000011', 'TELECONSULT_INITIATE', 'TELEHEALTH', 'Initiate doctor-to-specialist teleconsultation session', true, clock_timestamp()),",
            "    ('018e3a21-0012-7000-8000-000000000012', 'REFERRAL_CREATE', 'CONTINUITY', 'Issue tertiary hospital referral dossier', true, clock_timestamp()),",
            "    ('018e3a21-0013-7000-8000-000000000013', 'VITAL_SIGNS_CAPTURE', 'CLINICAL', 'Record physiological vitals and panic threshold checks', true, clock_timestamp()),",
            "    ('018e3a21-0014-7000-8000-000000000014', 'IMMUNIZATION_RECORD', 'CLINICAL', 'Administer and log national immunization program vaccines', true, clock_timestamp()),",
            "    ('018e3a21-0015-7000-8000-000000000015', 'NCD_SCREENING_WRITE', 'CLINICAL', 'Log CBAC non-communicable disease community screenings', true, clock_timestamp()),",
            "    ('018e3a21-0016-7000-8000-000000000016', 'AUDIT_LOG_INSPECT', 'AUDIT', 'Read and verify cryptographic hash chains in audit ledger', true, clock_timestamp()),",
            "    ('018e3a21-0017-7000-8000-000000000017', 'IOT_TELEMETRY_INGEST', 'TELEMETRY', 'Ingest cold chain refrigerator temperature readings', true, clock_timestamp())",
            "ON CONFLICT (code) DO UPDATE SET",
            "    description = EXCLUDED.description,",
            "    updated_at = clock_timestamp();"
        ],

        "SEED-003": [
            "INSERT INTO identity.role_permissions (role_id, permission_id, created_at) VALUES",
            "    ('018e3a20-0002-7000-8000-000000000002', '018e3a21-0001-7000-8000-000000000001', clock_timestamp()),",
            "    ('018e3a20-0002-7000-8000-000000000002', '018e3a21-0002-7000-8000-000000000002', clock_timestamp()),",
            "    ('018e3a20-0002-7000-8000-000000000002', '018e3a21-0005-7000-8000-000000000005', clock_timestamp()),",
            "    ('018e3a20-0002-7000-8000-000000000002', '018e3a21-0006-7000-8000-000000000006', clock_timestamp()),",
            "    ('018e3a20-0002-7000-8000-000000000002', '018e3a21-0009-7000-8000-000000000009', clock_timestamp()),",
            "    ('018e3a20-0003-7000-8000-000000000003', '018e3a21-0004-7000-8000-000000000004', clock_timestamp()),",
            "    ('018e3a20-0004-7000-8000-000000000004', '018e3a21-0007-7000-8000-000000000007', clock_timestamp()),",
            "    ('018e3a20-0004-7000-8000-000000000004', '018e3a21-0008-7000-8000-000000000008', clock_timestamp()),",
            "    ('018e3a20-0005-7000-8000-000000000005', '018e3a21-0010-7000-8000-000000000010', clock_timestamp()),",
            "    ('018e3a20-0006-7000-8000-000000000006', '018e3a21-0001-7000-8000-000000000001', clock_timestamp()),",
            "    ('018e3a20-0006-7000-8000-000000000006', '018e3a21-0003-7000-8000-000000000003', clock_timestamp())",
            "ON CONFLICT (role_id, permission_id) DO NOTHING;"
        ],
        "SEED-004": [
            "INSERT INTO identity.facilities (id, facility_code, facility_name, facility_type, zone, ward_number, is_active, created_at) VALUES",
            "    ('018e3a22-0001-7000-8000-000000000001', 'WARD-BBMP-065', 'Malleshwaram Ward 65', 'MUNICIPAL_WARD', 'WEST', 65, true, clock_timestamp()),",
            "    ('018e3a22-0002-7000-8000-000000000002', 'WARD-BBMP-098', 'Rajajinagar Ward 98', 'MUNICIPAL_WARD', 'WEST', 98, true, clock_timestamp()),",
            "    ('018e3a22-0003-7000-8000-000000000003', 'WARD-BBMP-112', 'Indiranagar Ward 112', 'MUNICIPAL_WARD', 'EAST', 112, true, clock_timestamp()),",
            "    ('018e3a22-0004-7000-8000-000000000004', 'WARD-BBMP-153', 'Jayanagar Ward 153', 'MUNICIPAL_WARD', 'SOUTH', 153, true, clock_timestamp()),",
            "    ('018e3a22-0005-7000-8000-000000000005', 'WARD-BBMP-004', 'Yelahanka Satellite Town Ward 4', 'MUNICIPAL_WARD', 'YELAHANKA', 4, true, clock_timestamp()),",
            "    ('018e3a22-0006-7000-8000-000000000006', 'WARD-BBMP-085', 'Hoodi Ward 85', 'MUNICIPAL_WARD', 'MAHADEVAPURA', 85, true, clock_timestamp()),",
            "    ('018e3a22-0007-7000-8000-000000000007', 'WARD-BBMP-174', 'HSR Layout Ward 174', 'MUNICIPAL_WARD', 'BOMMANAHALLI', 174, true, clock_timestamp()),",
            "    ('018e3a22-0008-7000-8000-000000000008', 'WARD-BBMP-039', 'Peenya Industrial Area Ward 39', 'MUNICIPAL_WARD', 'DASARAHALLI', 39, true, clock_timestamp()),",
            "    ('018e3a22-0009-7000-8000-000000000009', 'WARD-BBMP-160', 'Kengeri Ward 160', 'MUNICIPAL_WARD', 'RR_NAGAR', 160, true, clock_timestamp()),",
            "    ('018e3a22-0010-7000-8000-000000000010', 'WARD-BBMP-091', 'Shivajinagar Ward 91', 'MUNICIPAL_WARD', 'EAST', 91, true, clock_timestamp())",
            "ON CONFLICT (facility_code) DO UPDATE SET",
            "    facility_name = EXCLUDED.facility_name,",
            "    is_active = EXCLUDED.is_active,",
            "    updated_at = clock_timestamp();"
        ],
        "SEED-005": [
            "INSERT INTO identity.facilities (id, facility_code, facility_name, facility_type, zone, ward_number, is_active, created_at) VALUES",
            "    ('018e3a22-0101-7000-8000-000000000001', 'NC-BBMP-001', 'Namma Clinic Malleshwaram 7th Cross', 'NAMMA_CLINIC', 'WEST', 65, true, clock_timestamp()),",
            "    ('018e3a22-0102-7000-8000-000000000002', 'NC-BBMP-002', 'Namma Clinic Rajajinagar 3rd Block', 'NAMMA_CLINIC', 'WEST', 98, true, clock_timestamp()),",
            "    ('018e3a22-0103-7000-8000-000000000003', 'NC-BBMP-003', 'Namma Clinic Indiranagar Binnamangala', 'NAMMA_CLINIC', 'EAST', 112, true, clock_timestamp()),",
            "    ('018e3a22-0104-7000-8000-000000000004', 'NC-BBMP-004', 'Namma Clinic Jayanagar 4th T Block', 'NAMMA_CLINIC', 'SOUTH', 153, true, clock_timestamp()),",
            "    ('018e3a22-0105-7000-8000-000000000005', 'NC-BBMP-005', 'Namma Clinic Yelahanka New Town', 'NAMMA_CLINIC', 'YELAHANKA', 4, true, clock_timestamp()),",
            "    ('018e3a22-0106-7000-8000-000000000006', 'NC-BBMP-006', 'Namma Clinic Mahadevapura Hoodi Main', 'NAMMA_CLINIC', 'MAHADEVAPURA', 85, true, clock_timestamp()),",
            "    ('018e3a22-0107-7000-8000-000000000007', 'NC-BBMP-007', 'Namma Clinic Bommanahalli HSR Sector 2', 'NAMMA_CLINIC', 'BOMMANAHALLI', 174, true, clock_timestamp()),",
            "    ('018e3a22-0108-7000-8000-000000000008', 'NC-BBMP-008', 'Namma Clinic Dasarahalli Chokkasandra', 'NAMMA_CLINIC', 'DASARAHALLI', 39, true, clock_timestamp()),",
            "    ('018e3a22-0109-7000-8000-000000000009', 'NC-BBMP-009', 'Namma Clinic RR Nagar Kengeri Satellite', 'NAMMA_CLINIC', 'RR_NAGAR', 160, true, clock_timestamp()),",
            "    ('018e3a22-0110-7000-8000-000000000010', 'NC-BBMP-010', 'Namma Clinic Shivajinagar Russell Market', 'NAMMA_CLINIC', 'EAST', 91, true, clock_timestamp())",
            "ON CONFLICT (facility_code) DO UPDATE SET",
            "    facility_name = EXCLUDED.facility_name,",
            "    is_active = EXCLUDED.is_active,",
            "    updated_at = clock_timestamp();"
        ],
        "SEED-006": [
            "INSERT INTO pharmacy.drug_master (id, drug_code, generic_name, dosage_form, strength, is_essential_formulary, created_at) VALUES",
            "    ('018e3a23-0001-7000-8000-000000000001', 'MED-PARA-500', 'Paracetamol IP', 'TABLET', '500 mg', true, clock_timestamp()),",
            "    ('018e3a23-0002-7000-8000-000000000002', 'MED-AMOX-500', 'Amoxicillin IP', 'CAPSULE', '500 mg', true, clock_timestamp()),",
            "    ('018e3a23-0003-7000-8000-000000000003', 'MED-METF-500', 'Metformin Hydrochloride IP', 'TABLET', '500 mg', true, clock_timestamp()),",
            "    ('018e3a23-0004-7000-8000-000000000004', 'MED-AMLO-5', 'Amlodipine Besylate IP', 'TABLET', '5 mg', true, clock_timestamp()),",
            "    ('018e3a23-0005-7000-8000-000000000005', 'MED-ORS-21G', 'Oral Rehydration Salts IP', 'POWDER', '21.8 g sachet', true, clock_timestamp()),",
            "    ('018e3a23-0006-7000-8000-000000000006', 'MED-ALB-400', 'Albendazole IP', 'CHEWABLE_TABLET', '400 mg', true, clock_timestamp()),",
            "    ('018e3a23-0007-7000-8000-000000000007', 'MED-CETR-10', 'Cetirizine Hydrochloride IP', 'TABLET', '10 mg', true, clock_timestamp()),",
            "    ('018e3a23-0008-7000-8000-000000000008', 'MED-OMEP-20', 'Omeprazole IP', 'CAPSULE', '20 mg', true, clock_timestamp()),",
            "    ('018e3a23-0009-7000-8000-000000000009', 'MED-AZITH-500', 'Azithromycin IP', 'TABLET', '500 mg', true, clock_timestamp()),",
            "    ('018e3a23-0010-7000-8000-000000000010', 'MED-ATRV-10', 'Atorvastatin IP', 'TABLET', '10 mg', true, clock_timestamp()),",
            "    ('018e3a23-0011-7000-8000-000000000011', 'MED-IBUP-400', 'Ibuprofen IP', 'TABLET', '400 mg', true, clock_timestamp()),",
            "    ('018e3a23-0012-7000-8000-000000000012', 'MED-SALB-INHAL', 'Salbutamol Inhaler IP', 'INHALER', '100 mcg/dose', true, clock_timestamp())",
            "ON CONFLICT (drug_code) DO UPDATE SET",
            "    generic_name = EXCLUDED.generic_name,",
            "    strength = EXCLUDED.strength,",
            "    updated_at = clock_timestamp();"
        ],
        "SEED-007": [
            "INSERT INTO clinical.lab_test_master (id, test_code, test_name, sample_type, loinc_code, normal_range_min, normal_range_max, unit_of_measure, created_at) VALUES",
            "    ('018e3a24-0001-7000-8000-000000000001', 'LAB-CBC-HB', 'Hemoglobin', 'EDTA_WHOLE_BLOOD', '718-7', 12.0, 17.5, 'g/dL', clock_timestamp()),",
            "    ('018e3a24-0002-7000-8000-000000000002', 'LAB-GLUC-RBS', 'Random Blood Sugar', 'FLUORIDE_PLASMA', '2339-0', 70.0, 140.0, 'mg/dL', clock_timestamp()),",
            "    ('018e3a24-0003-7000-8000-000000000003', 'LAB-GLUC-FBS', 'Fasting Blood Sugar', 'FLUORIDE_PLASMA', '1558-6', 70.0, 100.0, 'mg/dL', clock_timestamp()),",
            "    ('018e3a24-0004-7000-8000-000000000004', 'LAB-HBA1C', 'Glycated Hemoglobin (HbA1c)', 'EDTA_WHOLE_BLOOD', '4548-4', 4.0, 5.6, '%', clock_timestamp()),",
            "    ('018e3a24-0005-7000-8000-000000000005', 'LAB-LIPID-CHOL', 'Serum Total Cholesterol', 'SERUM', '2093-3', 100.0, 200.0, 'mg/dL', clock_timestamp()),",
            "    ('018e3a24-0006-7000-8000-000000000006', 'LAB-RFT-CREAT', 'Serum Creatinine', 'SERUM', '2160-0', 0.6, 1.2, 'mg/dL', clock_timestamp()),",
            "    ('018e3a24-0007-7000-8000-000000000007', 'LAB-LFT-SGPT', 'Alanine Aminotransferase (SGPT)', 'SERUM', '1742-6', 7.0, 56.0, 'U/L', clock_timestamp()),",
            "    ('018e3a24-0008-7000-8000-000000000008', 'LAB-URINE-PROT', 'Urine Protein Dipstick', 'MIDSTREAM_URINE', '2888-6', 0.0, 0.0, 'mg/dL', clock_timestamp()),",
            "    ('018e3a24-0009-7000-8000-000000000009', 'LAB-DENGUE-NS1', 'Dengue NS1 Antigen Rapid', 'SERUM', '51655-9', 0.0, 0.0, 'QUALITATIVE', clock_timestamp()),",
            "    ('018e3a24-0010-7000-8000-000000000010', 'LAB-MALARIA-RDT', 'Malaria Rapid Diagnostic Test', 'WHOLE_BLOOD', '51436-4', 0.0, 0.0, 'QUALITATIVE', clock_timestamp())",
            "ON CONFLICT (test_code) DO UPDATE SET",
            "    test_name = EXCLUDED.test_name,",
            "    loinc_code = EXCLUDED.loinc_code,",
            "    updated_at = clock_timestamp();"
        ],
        "SEED-008": [
            "INSERT INTO clinical.icd10_diagnosis_master (id, icd10_code, diagnosis_title, chapter_name, is_chronic_ncd, created_at) VALUES",
            "    ('018e3a25-0001-7000-8000-000000000001', 'I10', 'Essential (primary) hypertension', 'Diseases of the circulatory system', true, clock_timestamp()),",
            "    ('018e3a25-0002-7000-8000-000000000002', 'E11.9', 'Type 2 diabetes mellitus without complications', 'Endocrine, nutritional and metabolic diseases', true, clock_timestamp()),",
            "    ('018e3a25-0003-7000-8000-000000000003', 'J06.9', 'Acute upper respiratory infection, unspecified', 'Diseases of the respiratory system', false, clock_timestamp()),",
            "    ('018e3a25-0004-7000-8000-000000000004', 'A09', 'Infectious gastroenteritis and colitis, unspecified', 'Certain infectious and parasitic diseases', false, clock_timestamp()),",
            "    ('018e3a25-0005-7000-8000-000000000005', 'A90', 'Dengue fever [classical dengue]', 'Certain infectious and parasitic diseases', false, clock_timestamp()),",
            "    ('018e3a25-0006-7000-8000-000000000006', 'J45.9', 'Asthma, unspecified', 'Diseases of the respiratory system', true, clock_timestamp()),",
            "    ('018e3a25-0007-7000-8000-000000000007', 'D50.9', 'Iron deficiency anemia, unspecified', 'Diseases of the blood and blood-forming organs', true, clock_timestamp()),",
            "    ('018e3a25-0008-7000-8000-000000000008', 'B86', 'Scabies', 'Certain infectious and parasitic diseases', false, clock_timestamp()),",
            "    ('018e3a25-0009-7000-8000-000000000009', 'K21.9', 'Gastro-esophageal reflux disease without esophagitis', 'Diseases of the digestive system', false, clock_timestamp()),",
            "    ('018e3a25-0010-7000-8000-000000000010', 'M54.5', 'Low back pain', 'Diseases of the musculoskeletal system', false, clock_timestamp())",
            "ON CONFLICT (icd10_code) DO UPDATE SET",
            "    diagnosis_title = EXCLUDED.diagnosis_title,",
            "    is_chronic_ncd = EXCLUDED.is_chronic_ncd,",
            "    updated_at = clock_timestamp();"
        ],
        "SEED-009": [
            "INSERT INTO clinical.vital_types (id, vital_code, vital_name, unit, min_normal, max_normal, panic_low, panic_high, created_at) VALUES",
            "    ('018e3a26-0001-7000-8000-000000000001', 'SYS_BP', 'Systolic Blood Pressure', 'mmHg', 90, 139, 70, 180, clock_timestamp()),",
            "    ('018e3a26-0002-7000-8000-000000000002', 'DIA_BP', 'Diastolic Blood Pressure', 'mmHg', 60, 89, 40, 120, clock_timestamp()),",
            "    ('018e3a26-0003-7000-8000-000000000003', 'HEART_RATE', 'Pulse / Heart Rate', 'bpm', 60, 100, 45, 140, clock_timestamp()),",
            "    ('018e3a26-0004-7000-8000-000000000004', 'SPO2', 'Oxygen Saturation', '%', 95, 100, 88, 100, clock_timestamp()),",
            "    ('018e3a26-0005-7000-8000-000000000005', 'RESP_RATE', 'Respiratory Rate', 'breaths/min', 12, 20, 8, 30, clock_timestamp()),",
            "    ('018e3a26-0006-7000-8000-000000000006', 'TEMP_C', 'Body Temperature', 'deg C', 36.1, 37.2, 35.0, 39.5, clock_timestamp()),",
            "    ('018e3a26-0007-7000-8000-000000000007', 'WEIGHT_KG', 'Body Weight', 'kg', 10, 150, 2, 250, clock_timestamp()),",
            "    ('018e3a26-0008-7000-8000-000000000008', 'HEIGHT_CM', 'Body Height', 'cm', 50, 210, 30, 230, clock_timestamp()),",
            "    ('018e3a26-0009-7000-8000-000000000009', 'RBS', 'Random Blood Sugar', 'mg/dL', 70, 140, 50, 350, clock_timestamp()),",
            "    ('018e3a26-0010-7000-8000-000000000010', 'BMI', 'Body Mass Index', 'kg/m^2', 18.5, 24.9, 14.0, 40.0, clock_timestamp())",
            "ON CONFLICT (vital_code) DO UPDATE SET",
            "    vital_name = EXCLUDED.vital_name,",
            "    unit = EXCLUDED.unit,",
            "    updated_at = clock_timestamp();"
        ],
        "SEED-010": [
            "INSERT INTO clinical.triage_severities (id, level_code, level_name, priority_rank, target_response_mins, color_hex, created_at) VALUES",
            "    ('018e3a27-0001-7000-8000-000000000001', 'ESI_1', 'Resuscitation / Immediate', 1, 0, '#FF0000', clock_timestamp()),",
            "    ('018e3a27-0002-7000-8000-000000000002', 'ESI_2', 'Emergent / Very Urgent', 2, 10, '#FF6600', clock_timestamp()),",
            "    ('018e3a27-0003-7000-8000-000000000003', 'ESI_3', 'Urgent / Priority Outpatient', 3, 30, '#FFCC00', clock_timestamp()),",
            "    ('018e3a27-0004-7000-8000-000000000004', 'ESI_4', 'Standard Outpatient Care', 4, 60, '#009933', clock_timestamp()),",
            "    ('018e3a27-0005-7000-8000-000000000005', 'ESI_5', 'Non-Urgent Routine Followup', 5, 120, '#0066CC', clock_timestamp())",
            "ON CONFLICT (level_code) DO UPDATE SET",
            "    level_name = EXCLUDED.level_name,",
            "    target_response_mins = EXCLUDED.target_response_mins,",
            "    updated_at = clock_timestamp();"
        ],
        "SEED-011": [
            "INSERT INTO continuity.notification_templates (id, template_code, channel, language, message_body, is_active, created_at) VALUES",
            "    ('018e3a28-0001-7000-8000-000000000001', 'SMS_TOKEN_CALLED_KN', 'SMS', 'KN', 'ನಮ್ಮ ಕ್ಲಿನಿಕ್: ಟೋಕನ್ #{{token_number}} ನಿಮ್ಮ ಸರದಿ ಬಂದಿದೆ. ದಯವಿಟ್ಟು ಕೊಠಡಿ {{room_number}} ಗೆ ಪ್ರವೇಶಿಸಿ.', true, clock_timestamp()),",
            "    ('018e3a28-0002-7000-8000-000000000002', 'SMS_TOKEN_CALLED_EN', 'SMS', 'EN', 'Namma Clinic: Token #{{token_number}} your turn has arrived. Please proceed to Consultation Room {{room_number}}.', true, clock_timestamp()),",
            "    ('018e3a28-0003-7000-8000-000000000003', 'SMS_PRESCRIPTION_READY_KN', 'SMS', 'KN', 'ನಮ್ಮ ಕ್ಲಿನಿಕ್: ನಿಮ್ಮ ಔಷಧಗಳು ವಿತರಣೆಗೆ ಸಿದ್ಧವಾಗಿವೆ. ಫಾರ್ಮಸಿ ಕೌಂಟರ್ ಗೆ ಭೇಟಿ ನೀಡಿ.', true, clock_timestamp()),",
            "    ('018e3a28-0004-7000-8000-000000000004', 'SMS_PRESCRIPTION_READY_EN', 'SMS', 'EN', 'Namma Clinic: Your prescribed medications are ready for pickup at the Pharmacy Counter.', true, clock_timestamp()),",
            "    ('018e3a28-0005-7000-8000-000000000005', 'WA_LAB_RESULTS_READY_EN', 'WHATSAPP', 'EN', 'Namma Clinic: Diagnostic test results for Order #{{order_number}} are verified. View on ABHA app.', true, clock_timestamp()),",
            "    ('018e3a28-0006-7000-8000-000000000006', 'WA_IMMUNIZATION_DUE_KN', 'WHATSAPP', 'KN', 'ನಮ್ಮ ಕ್ಲಿನಿಕ್: ಮಗುವಿನ ಲಸಿಕೆ ಬಾಕಿ ಇದೆ. ಹತ್ತಿರದ ನಮ್ಮ ಕ್ಲಿನಿಕ್ ಗೆ ಭೇಟಿ ನೀಡಿ.', true, clock_timestamp())",
            "ON CONFLICT (template_code) DO UPDATE SET",
            "    message_body = EXCLUDED.message_body,",
            "    is_active = EXCLUDED.is_active,",
            "    updated_at = clock_timestamp();"
        ],
        "SEED-012": [
            "INSERT INTO continuity.grievance_categories (id, category_code, category_title, statutory_sla_days, escalation_tier, created_at) VALUES",
            "    ('018e3a29-0001-7000-8000-000000000001', 'GRV-DOC-ABS', 'Doctor Unavailability during Clinic Hours', 3, 'ZONAL_CHIEF_OFFICER', clock_timestamp()),",
            "    ('018e3a29-0002-7000-8000-000000000002', 'GRV-DRUG-OOS', 'Essential Medicine Out of Stock', 2, 'INVENTORY_MANAGER', clock_timestamp()),",
            "    ('018e3a29-0003-7000-8000-000000000003', 'GRV-LAB-DELAY', 'Laboratory Diagnostic Result Delay (>24h)', 2, 'LAB_SUPERVISOR', clock_timestamp()),",
            "    ('018e3a29-0004-7000-8000-000000000004', 'GRV-STAFF-COND', 'Unprofessional Staff Demeanor / Misconduct', 7, 'BBMP_ADMIN_OFFICER', clock_timestamp()),",
            "    ('018e3a29-0005-7000-8000-000000000005', 'GRV-FAC-CLEAN', 'Facility Cleanliness & Sanitation Issue', 1, 'SANITATION_SUPERVISOR', clock_timestamp())",
            "ON CONFLICT (category_code) DO UPDATE SET",
            "    category_title = EXCLUDED.category_title,",
            "    statutory_sla_days = EXCLUDED.statutory_sla_days,",
            "    updated_at = clock_timestamp();"
        ],
        "SEED-013": [
            "INSERT INTO telemetry.device_types (id, model_code, device_category, min_safe_temp, max_safe_temp, polling_interval_secs, created_at) VALUES",
            "    ('018e3a30-0001-7000-8000-000000000001', 'ILR-VESTF-VLS024', 'VACCINE_REFRIGERATOR', 2.0, 8.0, 60, clock_timestamp()),",
            "    ('018e3a30-0002-7000-8000-000000000002', 'ILR-GODREJ-GVR50', 'VACCINE_REFRIGERATOR', 2.0, 8.0, 60, clock_timestamp()),",
            "    ('018e3a30-0003-7000-8000-000000000003', 'DF-BOMANN-DF100', 'DEEP_FREEZER_ICEPACKS', -25.0, -15.0, 120, clock_timestamp()),",
            "    ('018e3a30-0004-7000-8000-000000000004', 'IOT-BLUETOOTH-TAG', 'PORTABLE_VACCINE_CARRIER', 2.0, 8.0, 30, clock_timestamp())",
            "ON CONFLICT (model_code) DO UPDATE SET",
            "    min_safe_temp = EXCLUDED.min_safe_temp,",
            "    max_safe_temp = EXCLUDED.max_safe_temp,",
            "    updated_at = clock_timestamp();"
        ],
        "SEED-014": [
            "INSERT INTO clinical.dosage_schedules (id, schedule_code, schedule_name, frequency_per_day, interval_hours, administration_route, created_at) VALUES",
            "    ('018e3a31-0001-7000-8000-000000000001', 'OD_MORNING', 'Once Daily (Morning after food)', 1, 24, 'ORAL', clock_timestamp()),",
            "    ('018e3a31-0002-7000-8000-000000000002', 'OD_NIGHT', 'Once Daily (Night before sleep)', 1, 24, 'ORAL', clock_timestamp()),",
            "    ('018e3a31-0003-7000-8000-000000000003', 'BD', 'Twice Daily (Morning & Night)', 2, 12, 'ORAL', clock_timestamp()),",
            "    ('018e3a31-0004-7000-8000-000000000004', 'TID', 'Three Times Daily (8-hour intervals)', 3, 8, 'ORAL', clock_timestamp()),",
            "    ('018e3a31-0005-7000-8000-000000000005', 'QID', 'Four Times Daily (6-hour intervals)', 4, 6, 'ORAL', clock_timestamp()),",
            "    ('018e3a31-0006-7000-8000-000000000006', 'SOS_PRN', 'As Needed for Symptoms (SOS / PRN)', 0, 0, 'ORAL', clock_timestamp()),",
            "    ('018e3a31-0007-7000-8000-000000000007', 'STAT', 'Immediately (Single Dose)', 1, 0, 'INTRAMUSCULAR', clock_timestamp())",
            "ON CONFLICT (schedule_code) DO UPDATE SET",
            "    schedule_name = EXCLUDED.schedule_name,",
            "    frequency_per_day = EXCLUDED.frequency_per_day,",
            "    updated_at = clock_timestamp();"
        ],
        "SEED-015": [
            "INSERT INTO intake.patients (id, abha_id, full_name, gender, date_of_birth, phone_number, registration_facility_id, is_synthetic_test_data, created_at) VALUES",
            "    ('018e3a32-0001-7000-8000-000000000001', '91-0000-1111-2222', 'Ramesh Rao', 'MALE', '1975-04-12', '+91-90000-00001', '018e3a22-0101-7000-8000-000000000001', true, clock_timestamp()),",
            "    ('018e3a32-0002-7000-8000-000000000002', '91-0000-3333-4444', 'Sunita Gowda', 'FEMALE', '1982-08-25', '+91-90000-00002', '018e3a22-0101-7000-8000-000000000001', true, clock_timestamp()),",
            "    ('018e3a32-0003-7000-8000-000000000003', '91-0000-5555-6666', 'Anand Kumar', 'MALE', '1990-11-03', '+91-90000-00003', '018e3a22-0102-7000-8000-000000000002', true, clock_timestamp()),",
            "    ('018e3a32-0004-7000-8000-000000000004', '91-0000-7777-8888', 'Lakshmi Narayana', 'FEMALE', '1968-01-19', '+91-90000-00004', '018e3a22-0103-7000-8000-000000000003', true, clock_timestamp()),",
            "    ('018e3a32-0005-7000-8000-000000000005', '91-0000-9999-0000', 'Mohammed Imran', 'MALE', '1995-06-30', '+91-90000-00005', '018e3a22-0104-7000-8000-000000000004', true, clock_timestamp())",
            "ON CONFLICT (abha_id) DO UPDATE SET",
            "    full_name = EXCLUDED.full_name,",
            "    phone_number = EXCLUDED.phone_number,",
            "    updated_at = clock_timestamp();"
        ]
    }

    for s in SEEDS:
        sid = s["id"]
        sname = s["name"]
        cat = s["category"]
        tbl = s["target_table"]
        env = s["environment"]
        count = s["record_count"]
        auth = s["source_authority"]
        ver = s["versioning"]
        idemp = s["idempotency"]
        order = s["execution_order"]
        pii = s["pii_presence"]
        rb = s["rollback_procedure"]

        lines.append(f"### {sid}: {sname}")
        lines.append("")
        
        # 1. Dataset Profile
        lines.append(f"#### 1. Dataset Profile, Operational Context & Governance")
        lines.append(f"- **Seed Identifier**: `{sid}`")
        lines.append(f"- **Functional Classification**: `{cat}`")
        lines.append(f"- **Target Relational Table**: `{tbl}`")
        lines.append(f"- **Deployment Environment**: `{env}`")
        lines.append(f"- **Baseline Record Count**: {count:,} records")
        lines.append(f"- **Authoritative Source**: {auth}")
        lines.append(f"- **Dataset Version**: `{ver}`")
        lines.append(f"- **PII Status**: `{pii}` (Strictly zero sensitive data)")
        lines.append(f"- **Execution Topological Sequence**: Stage {order} in global initialization pipeline")
        lines.append(f"- **Cache Invalidation Requirement**: Updates trigger immediate Redis key eviction on `cache:{tbl}:*` with TTL refresh.")
        lines.append("")

        # 2. Idempotency Strategy
        lines.append(f"#### 2. Idempotency Mechanism & Conflict Resolution")
        lines.append(f"- **Conflict Key**: Unique business key on `{tbl}` (e.g. `code`, `facility_code`, `drug_code`).")
        lines.append(f"- **Upsert Strategy**: {idemp}")
        lines.append(f"- **State Machine Transition**: Existing records are updated with latest official terminology descriptions while preserving historical internal surrogate UUIDs.")
        lines.append(f"- **Concurrent Lock Footprint**: Acquires row-level locks on touched rows only; sub-second transaction duration eliminates blocker hazards.")
        lines.append("")

        # 3. Concrete SQL Seed Blueprint
        lines.append(f"#### 3. Concrete SQL Seed Blueprint (DOCUMENTATION-ONLY SQL)")
        lines.append("```sql")
        lines.append(f"-- ============================================================================")
        lines.append(f"-- DOCUMENTATION-ONLY SQL: Seed Script for {sid}")
        lines.append(f"-- Dataset: {sname} ({env})")
        lines.append(f"-- ============================================================================")
        lines.append("BEGIN;")
        lines.append("SET LOCAL lock_timeout = '5s';")
        lines.append("SET LOCAL statement_timeout = '60s';")
        lines.append("")

        # Get custom DML
        custom_sql = dataset_sql_blueprints.get(sid, [
            f"INSERT INTO clinical.{tbl} (id, code, display_name, category, is_active, created_at) VALUES",
            "    (gen_random_uuid(), 'REF-001', 'Standard Entry 1', 'STANDARD', true, clock_timestamp()),",
            "    (gen_random_uuid(), 'REF-002', 'Standard Entry 2', 'STANDARD', true, clock_timestamp())",
            "ON CONFLICT (code) DO UPDATE SET display_name = EXCLUDED.display_name, updated_at = clock_timestamp();"
        ])
        for sql_line in custom_sql:
            lines.append(sql_line)

        lines.append("COMMIT;")
        lines.append("```")
        lines.append("")

        # 4. Synthetic Generation Rules
        lines.append(f"#### 4. Synthetic Generation Algorithm & Invariants (Zero PII)")
        lines.append(f"- **Generation Tooling**: Python `faker` library with localized Indian provider (`en_IN`).")
        lines.append(f"- **Demographic Name Synthesis**: Randomly selected from top 5,000 Kannada, Telugu, and Hindi municipal electoral surnames.")
        lines.append(f"- **Telephone Number Obfuscation**: Uses reserved non-allocable range `+91 90000 00001` through `+91 90000 99999`.")
        lines.append(f"- **ABHA Identification Mocking**: Formatted as `91-XXXX-XXXX-YYYY` where all digits are synthetically derived.")
        lines.append(f"- **Reference Python Code Generator Blueprint**:")
        lines.append("  ```python")
        lines.append("  from faker import Faker")
        lines.append("  fake = Faker('en_IN')")
        lines.append("  def generate_synthetic_record():")
        lines.append("      return {")
        lines.append(f"          'table': '{tbl}',")
        lines.append("          'synthetic_phone': f'+91-90000-{fake.random_number(digits=5, fix_len=True)}',")
        lines.append("          'synthetic_abha': f'91-{fake.random_number(digits=4)}-{fake.random_number(digits=4)}-{fake.random_number(digits=4)}',")
        lines.append("          'is_mock': True")
        lines.append("      }")
        lines.append("  ```")
        lines.append("")

        # 5. Edge Offline Sync & Local Cache Profile
        lines.append(f"#### 5. Edge Offline Seed Synchronization & Local SQLite Cache Profile")
        lines.append(f"- **Edge Distribution Channel**: Peripheral clinic micro-servers download `{sid}` via HTTPS during nocturnal sync windows.")
        lines.append(f"- **Local SQLite Table**: Synced to local embedded SQLite table `local_{tbl}` with SHA-256 manifest integrity verification.")
        lines.append(f"- **Offline Availability SLA**: Front-desk and consultation workstations query local SQLite cache with < 1ms latency even during total WAN disruption.")
        lines.append(f"- **Incremental Diff Protocol**: Edge sync daemon compares local version `{ver}` against central hash; downloads delta payload only.")
        lines.append("")

        # 6. Data Quality Invariants & Anomaly Prevention
        lines.append(f"#### 6. Data Quality Invariants & Anomaly Prevention")
        lines.append(f"- **Nullability Invariant**: Key identity attributes must be non-null across all rows.")
        lines.append(f"- **Format Validation Invariant**: Regex validation on codes (`^[A-Z0-9_-]{{3,32}}$`).")
        lines.append(f"- **Audit Trailing**: Insertion and modification timestamps managed via UTC `clock_timestamp()`.")
        lines.append(f"- **Foreign Key Integrity**: All referenced foreign keys verified prior to batch commit.")
        lines.append("")

        # 7. Rollback Procedure & Automated Verification Probe
        lines.append(f"#### 7. Rollback Procedure & Automated Verification Probe")
        lines.append(f"- **Compensating Rollback Script**: `{rb}`")
        lines.append(f"- **Automated Verification Assertion Probe Script**:")

        lines.append("  ```sql")
        lines.append("  -- DOCUMENTATION-ONLY SQL")
        lines.append(f"  -- Step 1: Verify minimum expected record count for {sid}")
        lines.append(f"  SELECT COUNT(*) AS actual_count,")
        lines.append(f"         CASE WHEN COUNT(*) >= 5 THEN 'PASS' ELSE 'FAIL_UNDERCOUNT' END AS test_status")
        lines.append(f"  FROM identity.{tbl} WHERE is_active = true;")
        lines.append("")
        lines.append(f"  -- Step 2: Verify zero duplicate natural business keys")
        lines.append(f"  SELECT code, COUNT(*)")
        lines.append(f"  FROM identity.{tbl}")
        lines.append(f"  GROUP BY code")
        lines.append(f"  HAVING COUNT(*) > 1;")
        lines.append("")
        lines.append(f"  -- Step 3: Verify zero orphaned records without valid audit timestamps")
        lines.append(f"  SELECT COUNT(*) AS invalid_audit_timestamps")
        lines.append(f"  FROM identity.{tbl}")
        lines.append(f"  WHERE created_at IS NULL OR updated_at IS NULL;")
        lines.append("  ```")
        lines.append("")

        # 8. Local Edge SQLite Cache Schema & Read-Only Trigger
        lines.append(f"#### 8. Local Edge SQLite Cache Schema & Read-Only Trigger")
        lines.append("```sql")
        lines.append(f"-- DOCUMENTATION-ONLY SQL: Local SQLite DDL for Edge Clinic Node")
        lines.append(f"CREATE TABLE IF NOT EXISTS local_{tbl} (")
        lines.append("    id TEXT PRIMARY KEY,")
        lines.append("    code TEXT NOT NULL UNIQUE,")
        lines.append("    name TEXT NOT NULL,")
        lines.append("    is_active INTEGER NOT NULL DEFAULT 1,")
        lines.append("    synced_at TEXT NOT NULL")
        lines.append(");")
        lines.append(f"CREATE TRIGGER IF NOT EXISTS trg_prevent_edge_write_{tbl}")
        lines.append(f"BEFORE INSERT OR UPDATE OR DELETE ON local_{tbl}")
        lines.append("BEGIN")
        lines.append("    SELECT RAISE(ABORT, 'MUTATION_PROHIBITED: Edge nodes cannot mutate central seed catalog');")
        lines.append("END;")
        lines.append("```")
        lines.append("")

        # 9. Cross-Schema Dependency & Cascading Constraints
        lines.append(f"#### 9. Cross-Schema Dependency & Cascading Constraints")
        lines.append(f"- **Upstream Prerequisite Table**: Stage {order-1 if order > 1 else 'None (Root Genesis)'}.")
        lines.append(f"- **Downstream Dependent Relations**: Relational tables requiring `{tbl}` for transactional foreign keys.")
        lines.append(f"- **Referential Integrity Enforcement**: `ON DELETE RESTRICT` guarantees that active seed items cannot be removed while referenced by clinical encounters or prescriptions.")
        # 10. Disaster Recovery Rehydration SLA & RTO Target
        lines.append(f"#### 10. Disaster Recovery Rehydration SLA & Operational RTO Target")
        lines.append(f"- **Recovery Time Objective (RTO)**: Sub-5 minute full restoration from cold Git repository.")
        lines.append(f"- **Recovery Point Objective (RPO)**: Zero data loss (RPO = 0); catalog state is 100% deterministic and version-controlled.")
        lines.append(f"- **Automated Integrity Assertion**: Deployment health checks block API gateway routing until seed row count for `{tbl}` reaches `{count}` records.")
        lines.append(f"- **Corrupted Data Eviction Runbook**: In case of partial or corrupted seed execution, run `TRUNCATE identity.{tbl} CASCADE;` followed by immediate idempotent replay from golden dump artifact.")
        lines.append("")

    # 7. CI/CD Integration & Environment Bootstrapping
    lines.append("## 7. CI/CD Database Seeding Pipeline & Automated Bootstrapping")

    lines.append("")
    lines.append("Seeding execution is integrated into GitHub Actions CI/CD workflows and Kubernetes initialization containers (`initContainers`):")
    lines.append("1. **Production Pipeline Guard**: The deployment runner evaluates `DATABASE_ENVIRONMENT`. If set to `PRODUCTION`, all scripts matching `*staging*` or `*synthetic*` are hard-blocked by pre-commit hooks.")
    lines.append("2. **Idempotent Re-execution**: During rolling updates, new pods execute `seed:run`. Since all statements implement `ON CONFLICT DO UPDATE`, running against an active production database incurs zero lock contention and zero duplicate mutations.")
    lines.append("3. **Checksum Verification**: Each seed file's SHA-256 hash is recorded in `core.seed_execution_history`. Unmodified files are bypassed automatically to minimize deployment time.")
    lines.append("")

    # 8. Cache Synchronization Architecture
    lines.append("## 8. Cache Synchronization & Redis Pub/Sub Eviction Architecture")
    lines.append("")
    lines.append("Reference datasets seeded into PostgreSQL are cached in Redis clusters to support sub-millisecond lookups during peak clinic intake:")
    lines.append("1. **Cache Structure**: Reference items are cached under key prefixes `ref:{table_name}:{code}` with a default TTL of 24 hours.")
    lines.append("2. **Automated Eviction on Upsert**: Upon executing any seed update, PostgreSQL triggers emit a `NOTIFY reference_data_updated, '{\"table\": \"...\"}'` event.")
    lines.append("3. **Subscriber Daemon**: Application API gateways listening on the channel immediately invalidate in-memory LRU caches and issue Redis `DEL` commands for modified records.")
    lines.append("")

    # 9. Non-Production Hydration Architecture
    lines.append("## 9. Non-Production Test Environment Hydration Architecture")
    lines.append("")
    lines.append("To enable realistic end-to-end integration testing, staging and load-testing clusters are populated with synthetic cohorts via `SEED-015`:")
    lines.append("1. **Scale Parameters**: 100,000 synthetic patients, 250,000 encounters, and 500,000 lab results distributed across 450 simulated Namma Clinics.")
    lines.append("2. **Epidemiological Realism**: Disease distributions mimic Karnataka state public health surveys: 28% adult hypertension prevalence, 18% Type-2 diabetes, 12% pediatric respiratory infections.")
    lines.append("3. **Zero Contamination Boundary**: Synthetic cohorts carry a deterministic boolean flag `is_synthetic_test_data = TRUE` and are physically partitioned into staging database clusters.")
    lines.append("")

    # 10. Seed Versioning & Release Governance
    lines.append("## 10. Seed Catalog Versioning & Release Governance")
    lines.append("")
    lines.append("Reference catalogs evolve over time (e.g. addition of new formulary drugs by the Department of Health or new ward delimitation). To maintain deterministic auditability across versions:")
    lines.append("1. **Semantic Versioning**: All seed catalogs adhere to SemVer (`vYYYY.MM.PATCH`). Major revisions coincide with official municipal gazette notifications.")
    lines.append("2. **Execution Tracking Schema**:")
    lines.append("   ```sql")
    lines.append("   -- DOCUMENTATION-ONLY SQL: Seed Execution Audit Ledger")
    lines.append("   CREATE TABLE IF NOT EXISTS core.seed_execution_history (")
    lines.append("       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),")
    lines.append("       seed_id VARCHAR(32) NOT NULL,")
    lines.append("       dataset_version VARCHAR(32) NOT NULL,")
    lines.append("       records_inserted INT NOT NULL,")
    lines.append("       records_updated INT NOT NULL,")
    lines.append("       checksum_sha256 VARCHAR(64) NOT NULL,")
    lines.append("       executed_by VARCHAR(64) NOT NULL,")
    lines.append("       executed_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()")
    lines.append("   );")
    lines.append("   ```")
    lines.append("3. **Immutable Golden Snapshot**: Golden seed SQL scripts are archived in Git LFS under `database/seeds/golden/` with signed cryptographic commits.")
    lines.append("")

    # 11. RACI Governance Matrix for Reference Data Management
    lines.append("## 11. RACI Governance Matrix for Reference Data Management")
    lines.append("")
    lines.append("Institutional oversight governing reference data catalog curation is structured as follows:")
    lines.append("")
    lines.append("| Operational Responsibility | Chief Medical Officer (BBMP) | Lead Clinical Pharmacist | Lead Database Architect | Site Reliability Lead | Fullstack Dev Lead |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    lines.append("| **Essential Formulary Modification** | Accountable | Responsible | Consulted | Informed | Informed |")
    lines.append("| **ICD-10 Terminology Updates** | Responsible | Consulted | Accountable | Informed | Informed |")
    lines.append("| **BBMP Facility & Ward Delimitation** | Accountable | Informed | Responsible | Informed | Informed |")
    lines.append("| **Synthetic Staging Cohort Refresh** | Informed | Informed | Consulted | Responsible | Responsible |")
    lines.append("| **Production Seeding Execution** | Informed | Informed | Accountable | Responsible | Informed |")
    lines.append("")

    # 12. Complete Python Synthetic Cohort Generation Engine
    lines.append("## 12. Synthetic Cohort Generation Engine Architecture (`SyntheticCohortEngine`)")
    lines.append("")
    lines.append("The platform utilizes an automated Python generator based on `faker` and `numpy` to generate realistic synthetic cohorts:")
    lines.append("")
    lines.append("```python")
    lines.append("# Synthetic Cohort Generator Engine for Namma Clinic Platform")
    lines.append("import random")
    lines.append("from faker import Faker")
    lines.append("import uuid")
    lines.append("from datetime import date, timedelta")
    lines.append("")
    lines.append("class SyntheticCohortEngine:")
    lines.append("    def __init__(self, random_seed: int = 42):")
    lines.append("        self.fake = Faker('en_IN')")
    lines.append("        Faker.seed(random_seed)")
    lines.append("        random.seed(random_seed)")
    lines.append("")
    lines.append("    def generate_patient(self, facility_id: str) -> dict:")
    lines.append("        age = int(random.gauss(38, 16))")
    lines.append("        age = max(1, min(95, age))")
    lines.append("        dob = date.today() - timedelta(days=age * 365.25)")
    lines.append("        gender = random.choice(['MALE', 'FEMALE', 'OTHER'])")
    lines.append("        first_name = self.fake.first_name_male() if gender == 'MALE' else self.fake.first_name_female()")
    lines.append("        last_name = self.fake.last_name()")
    lines.append("        return {")
    lines.append("            'id': str(uuid.uuid4()),")
    lines.append("            'abha_id': f'91-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',")
    lines.append("            'full_name': f'{first_name} {last_name}',")
    lines.append("            'gender': gender,")
    lines.append("            'date_of_birth': dob.isoformat(),")
    lines.append("            'phone_number': f'+91-90000-{random.randint(10000, 99999)}',")
    lines.append("            'registration_facility_id': facility_id,")
    lines.append("            'is_synthetic_test_data': True")
    lines.append("        }")
    lines.append("")
    lines.append("    def generate_encounter(self, patient: dict) -> dict:")
    lines.append("        return {")
    lines.append("            'id': str(uuid.uuid4()),")
    lines.append("            'patient_id': patient['id'],")
    lines.append("            'facility_id': patient['registration_facility_id'],")
    lines.append("            'encounter_type': 'OUTPATIENT_CONSULTATION',")
    lines.append("            'systolic_bp': int(random.gauss(124, 14)),")
    lines.append("            'diastolic_bp': int(random.gauss(80, 10)),")
    lines.append("            'heart_rate': int(random.gauss(76, 8)),")
    lines.append("            'blood_sugar_rbs': int(random.gauss(118, 35)),")
    lines.append("            'primary_icd10': random.choice(['I10', 'E11.9', 'J06.9', 'A09', 'A90'])")
    lines.append("        }")
    lines.append("```")
    lines.append("")

    # 13. Packaging & Distribution Pipeline
    lines.append("## 13. PostgreSQL pg_dump Packaging & Distribution Pipeline")
    lines.append("")
    lines.append("Reference datasets are packaged into reproducible binary dumps distributed via S3 CDN:")
    lines.append("1. **Export Command**:")
    lines.append("   ```bash")
    lines.append("   pg_dump -h db.internal -U postgres -d namma_clinic \\")
    lines.append("       --table='identity.roles' --table='identity.permissions' \\")
    lines.append("       --table='identity.facilities' --table='pharmacy.drug_master' \\")
    lines.append("       --data-only --format=custom --file=reference_seeds_v2024.1.dump")
    lines.append("   ```")
    lines.append("2. **Cryptographic Signing**:")
    lines.append("   ```bash")
    lines.append("   gpg --armor --detach-sign reference_seeds_v2024.1.dump")
    lines.append("   ```")
    lines.append("3. **Deployment Verification**:")
    lines.append("   ```bash")
    lines.append("   gpg --verify reference_seeds_v2024.1.dump.asc reference_seeds_v2024.1.dump")
    lines.append("   pg_restore --clean --if-exists -d namma_clinic reference_seeds_v2024.1.dump")
    lines.append("   ```")
    lines.append("")

    # 14. Reference Data Drift Detection
    lines.append("## 14. Reference Data Drift Detection & Continuous Integrity Scanner")
    lines.append("")
    lines.append("A nightly daemon inspects all 15 reference seed tables, comparing active database rows against golden seed manifests:")
    lines.append("1. **Hash Tree Comparison**: Computes SHA-256 over concatenated primary and business keys.")
    lines.append("2. **Drift Alerting**: If an unauthorized manual mutation occurs in production reference tables, an immediate alert is dispatched to the Lead Database Architect.")
    lines.append("3. **Automated Reconciliation**: The daemon issues an automated Git pull request proposing synchronization if official gazette updates are detected.")
    lines.append("")

    # 15. Emergency Hot-Fix Procedure
    lines.append("## 15. Emergency Out-of-Band Reference Hot-Fix Procedure")
    lines.append("")
    lines.append("If a critical reference error is identified in production (e.g. incorrect panic threshold or mislabeled drug strength):")
    lines.append("1. **Hot-Fix PR**: An expedited hot-fix branch modifies the canonical seed dataset in `scripts/database/db_migrations_seeds.py`.")
    lines.append("2. **Targeted Upsert Execution**: The hot-fix runner executes the single affected seed script using `ON CONFLICT DO UPDATE`.")
    lines.append("```sql")
    lines.append("-- DOCUMENTATION-ONLY SQL: Emergency Reference Hot-Fix Blueprint")
    lines.append("BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;")
    lines.append("SET LOCAL lock_timeout = '3s';")
    lines.append("UPDATE pharmacy.drug_master")
    lines.append("SET strength = '500 mg', updated_at = clock_timestamp()")
    lines.append("WHERE drug_code = 'MED-PARA-500';")
    lines.append("INSERT INTO core.seed_execution_history (seed_id, dataset_version, records_inserted, records_updated, checksum_sha256, executed_by)")
    lines.append("VALUES ('SEED-006', 'v2024.1.1-HOTFIX', 0, 1, digest('hotfix_content', 'sha256'), 'EMERGENCY_CISO_RELEASE');")
    lines.append("NOTIFY reference_data_updated, '{\"table\": \"drug_master\", \"code\": \"MED-PARA-500\"}';")
    lines.append("COMMIT;")
    lines.append("```")
    lines.append("")

    # 16. Seed Data Architectural Review Board & Quality Gates
    lines.append("## 16. Architectural Review Board (ARB) Seed Quality Gates")
    lines.append("")
    lines.append("Every modification to canonical seed datasets must pass four formal quality gates prior to production deployment:")
    lines.append("1. **Gate 1: Idempotency Automated Test**: The seed script is executed twice in succession against an empty shadow database; the second run must report 0 rows inserted and 0 errors.")
    lines.append("2. **Gate 2: Foreign Key Tree Validation**: All foreign keys referenced in seed datasets are verified against existing primary keys in parent tables.")
    lines.append("3. **Gate 3: PII Scanner Static Analysis**: An automated regex scanner inspects all string literals in seed files for real Indian telephone numbers, PAN cards, or Aadhaar sequences.")
    lines.append("4. **Gate 4: Clinical Advisory Sign-Off**: Formularies, ICD-10 sets, and lab test panic ranges require formal digital cryptographic sign-off from the BBMP Chief Medical Officer.")
    lines.append("")

    # 17. Automated Seed Integrity Health Check Endpoint
    lines.append("## 17. Automated Seed Integrity Health Check Endpoint")
    lines.append("")
    lines.append("To support Kubernetes liveness and readiness probes, API gateways expose an automated seed verification endpoint (`/api/v1/health/seeds`):")
    lines.append("")
    lines.append("```sql")
    lines.append("-- DOCUMENTATION-ONLY SQL: Master Seed Health Probe Query")
    lines.append("SELECT")
    lines.append("    (SELECT COUNT(*) FROM identity.roles WHERE is_system_standard = true) >= 10 AS roles_ok,")
    lines.append("    (SELECT COUNT(*) FROM identity.permissions WHERE is_core = true) >= 12 AS permissions_ok,")
    lines.append("    (SELECT COUNT(*) FROM identity.facilities WHERE is_active = true) >= 10 AS facilities_ok,")
    lines.append("    (SELECT COUNT(*) FROM pharmacy.drug_master WHERE is_essential_formulary = true) >= 12 AS drugs_ok,")
    lines.append("    (SELECT COUNT(*) FROM clinical.lab_test_master) >= 10 AS lab_tests_ok,")
    lines.append("    (SELECT COUNT(*) FROM clinical.icd10_diagnosis_master) >= 10 AS icd10_ok,")
    lines.append("    (SELECT COUNT(*) FROM clinical.vital_types) >= 10 AS vitals_ok,")
    lines.append("    (SELECT COUNT(*) FROM clinical.triage_severities) >= 5 AS triage_ok;")
    lines.append("```")
    lines.append("")

    # 18. Continuous Performance & Vacuum Implications
    lines.append("## 18. Continuous Performance & Maintenance Implications")
    lines.append("")
    lines.append("Because seed scripts utilize `ON CONFLICT DO UPDATE`, executing repeated deployments touches existing row versions, producing dead tuples in high-frequency reference tables:")
    lines.append("1. **Post-Seeding Maintenance Hook**: After large-scale seed executions or formulary catalog upgrades, the deployment orchestrator issues `VACUUM ANALYZE` on affected reference tables.")
    lines.append("2. **Index Bloat Prevention**: B-Tree indexes on reference tables have `fillfactor = 90` to accommodate minor updates without page splits.")
    lines.append("3. **Cache Warming Routine**: Upon successful seed verification, an asynchronous worker pre-warms the top 100 most frequently prescribed medications and ICD-10 diagnosis codes into local memory.")
    lines.append("")

    # 19. Seed Data Troubleshooting Runbook & Triage Matrix
    lines.append("## 19. Seed Data Troubleshooting Runbook & Triage Matrix")
    lines.append("")
    lines.append("When database seeding encounters execution errors during CI/CD or production bootstrap, engineers follow the triage matrix below:")
    lines.append("")
    lines.append("| Error Code | Error Description | Root Cause Hypothesis | Immediate Remediation Runbook | Prevention Invariant |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    lines.append("| `SQLSTATE 23505` | Unique Violation | Missing `ON CONFLICT` clause on unique key | Inspect seed SQL; ensure all `INSERT` statements declare explicit `ON CONFLICT (key) DO UPDATE` | Gate 1 Idempotency Check |")
    lines.append("| `SQLSTATE 23503` | Foreign Key Violation | Out-of-order execution in seed DAG | Verify prerequisite seed stage completed (e.g. `SEED-001` before `SEED-003`); check parent table rows | Gate 2 Dependency Tree Check |")
    lines.append("| `SQLSTATE 23502` | Not-Null Violation | Seed record omitted mandatory column | Cross-reference table schema in `06-column-data-dictionary.md`; supply valid default or canonical value | Schema linting prior to seed build |")
    lines.append("| `SQLSTATE 23514` | Check Violation | Value falls outside domain constraints | Validate check constraints (e.g. dose > 0, age >= 0, status in allowed set); adjust seed payload | Domain validation pre-check |")
    lines.append("| `SQLSTATE 22001` | String Right Truncation | Value length exceeds VARCHAR column limit | Adjust column width in prerequisite migration or truncate seed description string | Static schema linting |")
    lines.append("| `SQLSTATE 22007` | Invalid Datetime Format | ISO-8601 formatting deviation in timestamp | Use standard UTC formatting `YYYY-MM-DDTHH:MI:SS.MSZ` or `TIMESTAMPTZ` literal | Formatter validator in CI |")
    lines.append("| `SQLSTATE 22023` | Invalid Parameter Value | Malformed JSONB payload in config seeds | Validate JSON payload using `jq` or Python `json.loads()` before committing seed script | JSON linting step in build |")
    lines.append("| `SQLSTATE 42P01` | Undefined Table | Target table not yet created | Ensure all schema migrations (`MIG-001` to `MIG-030`) have executed successfully prior to seeding | Migration prerequisite check |")
    lines.append("| `SQLSTATE 40P01` | Deadlock Detected | Concurrent seed scripts writing to same tables | Enforce strictly sequential DAG execution for seed packages; never run seed scripts in parallel | Orchestrator concurrency locks |")
    lines.append("| `SQLSTATE 55P03` | Lock Timeout Exceeded | Concurrent transaction holding table lock | Increase session `lock_timeout` to '15s' or terminate blocking lock holder using `pg_terminate_backend()` | Execute during quiet window |")
    lines.append("| `SQLSTATE 57014` | Query Canceled | Seed script exceeded statement timeout | Temporarily raise `statement_timeout` for large seed batches (e.g. SNOMED/ICD-10) or chunk into smaller batches | Batch size limits (<= 500 rows) |")
    lines.append("| `SQLSTATE 28000` | Invalid Authorization | Deployment role lacks write privileges | Verify deployment role is granted `db_ddl_admin` and `db_dml_writer` memberships on target schemas | RBAC permission verification |")
    lines.append("| `SQLSTATE 25P02` | Current Transaction Aborted | Commands ignored until end of transaction block | Inspect initial error earlier in log stream; wrap discrete seed entities in distinct sub-transactions or SAVEPOINTs | Sub-transaction isolation |")
    lines.append("| `SQLSTATE 42703` | Undefined Column | Migration mismatch between model and seed payload | Verify migration schema matches seed insert column list exactly; synchronize git branch | Schema-to-seed CI drift test |")
    lines.append("")
    lines.append("If a seed script fails midway through execution, the transaction rolls back cleanly via PostgreSQL atomicity (`BEGIN ... COMMIT`). The engineer must rectify the underlying schema or data defect before re-triggering the pipeline. In staging environments, engineers execute `scripts/database/validate_seed_integrity.py` to assert zero orphaned foreign key references after seed remediation.")
    lines.append("")

    # 20. Disaster Recovery & Seed Reconstruction Procedures
    lines.append("## 20. Disaster Recovery & Cold-Start Seed Reconstruction")
    lines.append("")
    lines.append("In the event of a catastrophic disaster recovery scenario where a brand-new PostgreSQL cluster is provisioned from cold storage or bare-metal infrastructure:")
    lines.append("1. **Schema Initialization Step**: Run master migration sequence (`MIG-001` through `MIG-030`) to establish all 52 tables, constraints, indexes, and partition parent tables.")
    lines.append("2. **Core Reference Seeding**: Execute Stage 1 and Stage 2 seed packages (`SEED-001` through `SEED-007`) in strict order. These establish system tenants, facilities, administrative roles, clinical test catalogs, and national drug formularies.")
    lines.append("3. **Operational Configuration Seeding**: Execute Stage 3 seed packages (`SEED-008` through `SEED-015`) to establish SLA rule engines, triage guidelines, audit event categories, and notification delivery templates.")
    lines.append("4. **Deterministic Checksum Verification**: Execute cryptographic SHA-256 verification queries across all reference tables. The calculated table hash must match the approved baseline in git release tags:")
    lines.append("")
    lines.append("```sql")
    lines.append("-- DOCUMENTATION-ONLY SQL: Seed Deterministic Checksum Verification")
    lines.append("SELECT")
    lines.append("    'identity.roles' AS table_name,")
    lines.append("    MD5(STRING_AGG(role_code || ':' || role_name, ',' ORDER BY role_code)) AS table_fingerprint")
    lines.append("FROM identity.roles")
    lines.append("UNION ALL")
    lines.append("SELECT")
    lines.append("    'pharmacy.drug_master',")
    lines.append("    MD5(STRING_AGG(drug_code || ':' || generic_name, ',' ORDER BY drug_code))")
    lines.append("FROM pharmacy.drug_master")
    lines.append("UNION ALL")
    lines.append("SELECT")
    lines.append("    'clinical.lab_test_master',")
    lines.append("    MD5(STRING_AGG(test_code || ':' || test_name, ',' ORDER BY test_code))")
    lines.append("FROM clinical.lab_test_master;")
    lines.append("```")
    lines.append("")
    lines.append("5. **Production Readiness Sign-Off**: Once all checksums match canonical release manifests, the cluster health probe `/api/v1/health/seeds` reports HTTP `200 OK`, allowing ingress traffic to resume.")
    lines.append("6. **Cross-Tenant Consistency Assertion**: An automated SQL assertion confirms that default tenant configurations match across all 8 BBMP administrative zones.")
    lines.append("7. **Audit Event Verification**: The cold-start procedure writes a structured audit log entry to `audit.security_events` recording the timestamp, operator identity, and git commit SHA.")
    lines.append("8. **Formulary Active Status Check**: Verifies that exactly 100% of the Essential Drugs List (EDL) items are marked with `is_active = true` and valid dispensing units.")
    lines.append("9. **Lab Range Boundary Test**: Executes range validation on all lab test panic thresholds to ensure critical low values are strictly less than critical high values.")
    lines.append("10. **RBAC Closure Verification**: Validates that every permission assigned in `identity.role_permissions` maps to a registered permission in `identity.permissions`.")
    lines.append("")

    # 21. Master Seed Dataset Governance & Verification Register
    lines.append("## 21. Master Seed Dataset Governance & Verification Register")
    lines.append("")
    lines.append("The table below details the formal governance attributes, target schemas, and verification criteria for all 15 canonical seed datasets:")
    lines.append("")
    lines.append("| Seed ID | Dataset Name | Target Schema & Table | Target Rows | Execution Stage | Environment Scope | Governance Owner | Automated Test Suite Reference |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for s in SEEDS:
        table_name = s.get("target_table", "system_config")
        order = s.get("execution_order", 1)
        env = s.get("environment", "PRODUCTION_SAFE")
        rows = s.get("record_count", 10)
        lines.append(f"| `{s['id']}` | {s['name']} | `{table_name}` | {rows} | `STAGE_{order}` | `{env}` | Chief Data Architect / Lead DBA | `test_seed_{s['id'].lower().replace('-', '_')}_idempotency()` |")
    lines.append("")
    lines.append("Every pull request modifying any seed dataset must include corresponding updates to this register, unit test coverage, and ARB sign-off.")
    lines.append("")

    # 22. Seed Data Baseline & Quality Sign-Off
    lines.append("## 22. Seed Data Baseline & Quality Sign-Off")
    lines.append("")
    lines.append(f"This master specification approves all {len(SEEDS)} canonical seed datasets (`SEED-001` through `SEED-{len(SEEDS):03d}`). With 100% idempotent SQL blueprints, strict environment segregation, zero real PII invariants, automated verification probes, comprehensive synthetic generation engines, and disaster recovery checksum verification, the Namma Clinic Platform establishes a predictable, reproducible, and compliant reference data foundation.")
    lines.append("")

    content = "\n".join(lines)
    return write_db_doc("15-seed-data-strategy.md", content)

if __name__ == "__main__":
    generate_doc_15()
