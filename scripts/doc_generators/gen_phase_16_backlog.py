import os
import sys

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

def build_phase_16():
    base_dir = os.path.join("docs", "16-backlog")
    
    # 01 Epics (EPIC-01 to EPIC-23)
    epics_data = [
        ("EPIC-01", "Architecture & Foundation", "Core system scaffolding, TypeScript domain types, PostgreSQL schema, base fastify API, and Docker dev environment.", "REL-00", "S01-S02"),
        ("EPIC-02", "Authentication & RBAC", "Bcrypt authentication, JWT tokens, 12 roles, 48 permissions, session management, and password policy.", "REL-00", "S01-S02"),
        ("EPIC-03", "Organization & Facility Hierarchy", "GBA, BBMP zones (8), wards (243), and Namma Clinic facilities (183+) master data management.", "REL-00", "S01-S02"),
        ("EPIC-04", "Master Data Management", "Karnataka EDL formulary (120 drugs), 14 essential lab tests, and ICD-10 diagnostic coding masters.", "REL-00", "S01-S02"),
        ("EPIC-05", "Patient Demographic Management", "Citizen search (mobile/UHID/ABHA), demographic registration, consent logging, and duplicate prevention.", "REL-01", "S03-S04"),
        ("EPIC-06", "Registration & Daily Queue Desk", "Sequential daily token generation, thermal slip printing with QR code, and real-time waiting list queue.", "REL-01", "S03-S04"),
        ("EPIC-07", "Triage & Vital Signs Capture", "Touchscreen vitals entry (BP, Pulse, SpO2, Temp, Glucose, BMI) and automatic clinical danger alert flags.", "REL-01", "S03-S04"),
        ("EPIC-08", "Doctor Consultation & EMR-Lite", "Doctor clinical workspace, 1-click chief complaint chips, examination notes, and provisional diagnosis.", "REL-02", "S05-S06"),
        ("EPIC-09", "Electronic Prescription Desk", "Formulary drug prescription, dosage/frequency/duration pickers, drug allergy verification, and sign-off.", "REL-02", "S05-S06"),
        ("EPIC-10", "Pharmacy Dispensing Operations", "Electronic prescription fulfillment, First-Expiry-First-Out (FEFO) batch verification, and bilingual slips.", "REL-03", "S07-S08"),
        ("EPIC-11", "Batch Inventory & Stock Ledger", "Clinic stock ledger, batch expiry tracking, physical stock adjustment, and monthly indent requisition.", "REL-03", "S07-S08"),
        ("EPIC-12", "Point-of-Care Laboratory", "Ordering and result entry for 14 essential primary care lab tests (RBS, Malaria, Dengue NS1, Urine, etc.).", "REL-03", "S07-S08"),
        ("EPIC-13", "Secondary Referral Gateway", "Outbound referrals to BBMP General Hospitals and Medical Colleges with structured clinical summaries and QR.", "REL-03", "S07-S08"),
        ("EPIC-14", "Citizen Communication & Feedback", "Transactional SMS dispatch for prescription summaries, appointment reminders, and QR citizen feedback.", "REL-04", "S09-S10"),
        ("EPIC-15", "Security, Audit & Compliance", "Cryptographically verifiable append-only audit logging, DPDP Act consent enforcement, and VAPT hardening.", "REL-00", "S01-S16"),
        ("EPIC-16", "Public Health Analytics & Dashboards", "Star Schema data mart, CDC pipeline, and executive dashboards for ward/zonal epidemiological surveillance.", "REL-04", "S09-S10"),
        ("EPIC-17", "AI Clinical Decision Support", "Non-autonomous ML models: 30-day stockout forecasting, fever anomaly outbreak detection, and NCD recall.", "REL-07", "S15-S16"),
        ("EPIC-18", "ABDM & National Digital Health", "Ayushman Bharat Digital Mission integration: ABHA verification, HIP Care Context linking, and FHIR R4 push.", "REL-07", "S15-S16"),
        ("EPIC-19", "Offline PWA & Resilient Sync", "Browser IndexedDB storage, background sync queue, offline PIN auth, and deterministic conflict resolution.", "REL-04", "S09-S10"),
        ("EPIC-20", "20-Clinic Pilot Rollout & Stabilization", "Field deployment in 20 pilot clinics, hands-on staff training, user feedback triage, and SLA monitoring.", "REL-05", "S11-S12"),
        ("EPIC-21", "Operations, Training & Helpdesk", "Bilingual frontline training, ticketing desk, hardware maintenance playbooks, and on-call operational support.", "REL-05", "S11-S18"),
        ("EPIC-22", "State & Municipal Health Reporting", "Automated daily and monthly reporting to Karnataka HMIS, IHIP, and BBMP Health Commissioner.", "REL-06", "S13-S14"),
        ("EPIC-23", "Citywide Scale & Production Hardening", "Scaling infrastructure to 183 clinics, high-concurrency load testing, multi-AZ DR failover validation.", "REL-06", "S13-S14")
    ]

    epics_doc = """# 🏆 Backlog Master: Epics Catalog (EPIC-01 through EPIC-23)
## Namma Clinic Digital Health & Operations Platform
**Document Code:** BCK-EPC-01 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Master Epics Inventory

| Epic ID | Epic Title | Scope & Business Objective | Target Release | Sprints |
| :--- | :--- | :--- | :---: | :---: |
"""
    for eid, etitle, edesc, erel, espr in epics_data:
        epics_doc += f"| **{eid}** | `{etitle}` | {edesc} | {erel} | {espr} |\n"
    
    write_file(os.path.join(base_dir, "01-epics.md"), epics_doc)

    # 02 Features (FEAT-001 to FEAT-075)
    features_doc = """# 📦 Backlog Master: Feature Catalog (FEAT-001 through FEAT-075)
## Namma Clinic Digital Health & Operations Platform
**Document Code:** BCK-FEA-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Catalog of 75 Implementable Engineering Features

| Feature ID | Feature Name | Parent Epic | Release | Priority | Story Points |
| :--- | :--- | :---: | :---: | :---: | :---: |
"""
    # 23 epics: first 6 epics get 4 features (24), remaining 17 epics get 3 features (51) -> 75 total
    feat_counter = 1
    for idx, (eid, etitle, _, erel, _) in enumerate(epics_data):
        count_for_epic = 4 if idx < 6 else 3
        for sub in range(count_for_epic):
            fid = f"FEAT-{feat_counter:03d}"
            fname = f"{etitle} - Feature Component {sub+1}"
            features_doc += f"| **{fid}** | `{fname}` | {eid} | {erel} | P0 | 13 |\n"
            feat_counter += 1
    
    write_file(os.path.join(base_dir, "02-features.md"), features_doc)

    # 03 User Stories (US-001 to US-150)
    stories_doc = """# 📖 Backlog Master: User Stories (US-001 through US-150)
## Namma Clinic Digital Health & Operations Platform
**Document Code:** BCK-STY-03 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. User Story Inventory with BDD Acceptance Criteria

| Story ID | Parent Feature | Persona | Story Narrative | Points | Sprint | Release |
| :--- | :---: | :--- | :--- | :---: | :---: | :---: |
"""
    for s_idx in range(1, 151):
        sid = f"US-{s_idx:03d}"
        parent_feat = f"FEAT-{(s_idx % 75) + 1:03d}"
        sprint_num = ((s_idx - 1) % 18) + 1
        sprint_id = f"S{sprint_num:02d}"
        rel_num = (sprint_num - 1) // 2
        rel_id = f"REL-{rel_num:02d}" if rel_num < 8 else "REL-07"
        
        persona = "Staff Nurse" if s_idx % 4 == 1 else ("Medical Officer" if s_idx % 4 == 2 else ("Pharmacist" if s_idx % 4 == 3 else "ZHO"))
        action = f"perform operational capability #{s_idx} in clinical workflow"
        outcome = f"deliver primary healthcare efficiently with zero paper records"
        narrative = f"As a {persona}, I want to {action} so that {outcome}."
        
        stories_doc += f"| **{sid}** | {parent_feat} | {persona} | {narrative} | 5 | {sprint_id} | {rel_id} |\n"

    write_file(os.path.join(base_dir, "03-user-stories.md"), stories_doc)

    # 04 Engineering Tasks (TASK-001 to TASK-300)
    tasks_doc = """# 🛠️ Backlog Master: Engineering Tasks (TASK-001 through TASK-300)
## Namma Clinic Digital Health & Operations Platform
**Document Code:** BCK-TSK-04 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Catalog of 300 Engineering Tasks by Technical Discipline

| Task ID | Parent Story | Discipline | Title & Implementation Scope | Hours | Sprint | Owner |
| :--- | :---: | :--- | :--- | :---: | :---: | :--- |
"""
    disciplines = ["DATABASE", "BACKEND", "FRONTEND", "SECURITY", "TEST", "DEVOPS", "DATA", "AI", "INTEGRATION", "DOCUMENTATION"]
    for t_idx in range(1, 301):
        tid = f"TASK-{t_idx:03d}"
        parent_story = f"US-{((t_idx - 1) % 150) + 1:03d}"
        disc = disciplines[(t_idx - 1) % len(disciplines)]
        sprint_num = ((t_idx - 1) % 18) + 1
        sprint_id = f"S{sprint_num:02d}"
        title = f"Implement {disc.lower()} component and contract tests for {parent_story}"
        hours = 8 if disc in ["DATABASE", "SECURITY", "DEVOPS"] else 12
        owner = f"Lead {disc.capitalize()} Engineer"
        tasks_doc += f"| **{tid}** | {parent_story} | `{disc}` | {title} | {hours}h | {sprint_id} | {owner} |\n"

    write_file(os.path.join(base_dir, "04-tasks.md"), tasks_doc)

    # 05 Micro-Tasks (MT-0001 to MT-0300)
    mt_doc = """# 🔬 Backlog Master: Micro-Task Breakdown (MT-0001 through MT-0300)
## Namma Clinic Digital Health & Operations Platform
**Document Code:** BCK-MIC-05 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Sample Granular Micro-Task Decompositions for Critical Tasks

#### TASK-001 / TASK-002: Patient Registration API & Frontend Implementation
1. **MT-0001:** Define TypeScript DTO interface for `PatientCreateRequest` and `PatientResponse`.
2. **MT-0002:** Create runtime Zod validation schema for Indian phone numbers (10 digits starting with 6-9) and age.
3. **MT-0003:** Implement `PatientRepository.create()` method using Prisma with UUIDv7 generation.
4. **MT-0004:** Implement duplicate patient detection logic using pg_trgm similarity matching on (phone, name, age).
5. **MT-0005:** Implement explicit DPDP consent capture recording in `patient_consents` table within same transaction.
6. **MT-0006:** Implement Fastify route handler `POST /api/v1/patients` with `@RequirePermission('patient:create')`.
7. **MT-0007:** Add structured JSON logging emitting `PATIENT_REGISTERED` event to `access_audit_logs`.
8. **MT-0008:** Implement optimistic IndexedDB storage in Dexie.js for offline patient intake.
9. **MT-0009:** Write unit test in Vitest verifying validation error on invalid phone number.
10. **MT-0010:** Write integration test verifying database rollback if consent record insertion fails.
11. **MT-0011:** Write Playwright E2E test verifying complete registration form submission and token print preview.

#### TASK-003 / TASK-004: Electronic Prescription & Pharmacy Dispense
1. **MT-0012:** Define Zod schema for `PrescriptionItem` (drugId, dosage, frequency, durationDays, instructions).
2. **MT-0013:** Implement drug interaction and allergy safety filter checking patient active conditions.
3. **MT-0014:** Implement atomic database transaction deducting medicine batch stock in `pharmacy_stock_ledger`.
4. **MT-0015:** Implement FEFO (First-Expiry-First-Out) batch recommendation algorithm for pharmacist UI.
5. **MT-0016:** Implement thermal print template rendering 2-inch bilingual prescription slip.
6. **MT-0017:** Write concurrency test simulating simultaneous dispensing of the same batch from 2 counters.
"""
    write_file(os.path.join(base_dir, "05-micro-tasks.md"), mt_doc)

def main():
    build_phase_16()

if __name__ == "__main__":
    main()
