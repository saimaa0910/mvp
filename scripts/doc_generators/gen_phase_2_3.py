import os
import sys

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

# ==========================================
# PHASE 2: REQUIREMENTS BASELINE GENERATOR
# ==========================================

def get_req_table(headers, rows):
    out = "| " + " | ".join(headers) + " |\n"
    out += "| " + " | ".join([":---"] * len(headers)) + " |\n"
    for row in rows:
        out += "| " + " | ".join(row) + " |\n"
    return out

def build_phase_2():
    base_dir = os.path.join("docs", "02-requirements")
    
    # 01 Business Requirements
    br_rows = [
        ["BR-001", "Rapid Patient Check-In", "Registration and triage completed in < 90 seconds to eliminate clinic queues.", "High", "Critical", "Proposal Sec 4", "None", "Patient registered with UHID and token issued.", "Automated Load Test", "EPIC-05", "FEAT-012", "US-025"],
        ["BR-002", "Zero Paper Register Transition", "Eliminate physical paper OPD, stock, and lab registers across 183 clinics.", "High", "Critical", "Proposal Sec 1", "BR-001", "100% daily logs digital; zero paper logs needed.", "Audit Inspection", "EPIC-06", "FEAT-015", "US-031"],
        ["BR-003", "Real-Time Medicine Stock Visibility", "Centralized batch-level visibility of all 183 clinic pharmacies.", "High", "Critical", "Proposal Sec 6", "None", "Zero stockouts of vital NCD and emergency drugs.", "Inventory Reconciliation", "EPIC-11", "FEAT-032", "US-068"],
        ["BR-004", "Syndromic Epidemiological Early Warning", "Detect infectious disease clusters (fever, dengue, acute diarrhea) in < 4 hours.", "High", "Critical", "DPR Sec 5", "BR-001", "Automated alert sent to Zonal Health Officer upon 3x threshold spike.", "Surveillance Simulation", "EPIC-16", "FEAT-048", "US-102"],
        ["BR-005", "ABDM Digital Health Record Linking", "Enable citizens to link visit summary with national ABHA address seamlessly.", "Medium", "High", "Proposal Sec 9", "BR-001", "Consent-based FHIR R4 record pushed to ABDM gateway.", "ABDM Sandbox Verification", "EPIC-18", "FEAT-055", "US-115"],
        ["BR-006", "Bilingual Frontline Operations", "100% Kannada and English interface for all clinic staff and citizen slips.", "High", "Critical", "UM-BIL-01", "None", "Toggle between Kannada and English with zero untranslated strings.", "UI Localization Audit", "EPIC-01", "FEAT-004", "US-008"],
        ["BR-007", "Offline Clinic Operational Continuity", "Uninterrupted clinic workflow during complete internet/power failure for up to 8 hrs.", "High", "Critical", "TD-ARC-01", "None", "All consultations saved locally in IndexedDB and synced on reconnect.", "Chaos Network Disconnect", "EPIC-19", "FEAT-058", "US-122"],
        ["BR-008", "Secondary Care Referral Tracking", "Closed-loop tracking of patients referred to secondary/tertiary BBMP hospitals.", "Medium", "High", "DPR Sec 4.4", "BR-001", "Referral QR code generated and acknowledgement recorded.", "Referral E2E Test", "EPIC-13", "FEAT-040", "US-085"],
        ["BR-009", "Essential Laboratory Order & Result Entry", "Support ordering and reporting for all 14 primary clinic point-of-care lab tests.", "Medium", "High", "Proposal Sec 6", "BR-001", "Lab tech enters results; results immediately visible to doctor.", "Lab Workflow Test", "EPIC-12", "FEAT-036", "US-078"],
        ["BR-010", "Citizen Grievance & Feedback Portal", "Enable citizens to register feedback and service complaints via QR code or SMS.", "Low", "Medium", "Proposal Sec 6", "None", "Feedback logged and routed to Ward Health Officer.", "Portal Smoke Test", "EPIC-14", "FEAT-044", "US-094"]
    ]
    br_content = f"""# 📋 Business Requirements Baseline
## Namma Clinic Digital Health & Operations Platform
**Document Code:** REQ-BR-01 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Executive Summary & Traceability Governance
Business Requirements define high-level organizational, clinical, and municipal health outcomes mandated by the Greater Bengaluru Authority (GBA) and BBMP Health Department.

{get_req_table(["ID", "Title", "Description", "Business Value", "Priority", "Source", "Dependencies", "Acceptance Criteria", "Verification Method", "Epic", "Feature", "Story"], br_rows)}
"""
    write_file(os.path.join(base_dir, "01-business-requirements.md"), br_content)

    # 02 Functional Requirements
    fr_rows = [
        ["FR-001", "Fast Citizen Search", "Search patients by Mobile Number, UHID, ABHA ID, or Name + Age within 200ms.", "P0", "BR-001", "Indexed query in PostgreSQL pg_trgm and IndexedDB.", "EPIC-05", "FEAT-011", "US-021"],
        ["FR-002", "Demographic Registration", "Capture Name, Phone, Age, Gender, Ward, Address with optional Aadhaar/ABHA.", "P0", "BR-001", "Patient record created with unique UHID.", "EPIC-05", "FEAT-012", "US-023"],
        ["FR-003", "Daily Queue Token Generation", "Issue daily sequential token (e.g. T-042) linked to clinic and date.", "P0", "BR-001", "Token printed on 2-inch thermal slip with QR code.", "EPIC-06", "FEAT-015", "US-032"],
        ["FR-004", "Triage Vitals Capture", "Record BP, Pulse, SpO2, Temperature, Height, Weight, Blood Glucose, BMI.", "P0", "BR-001", "Vitals attached to visit record; abnormal values flagged in red.", "EPIC-07", "FEAT-018", "US-038"],
        ["FR-005", "Clinical Chief Complaints", "Select chief complaints from 1-click clinical chips with duration selector.", "P0", "BR-002", "Selected chips serialized into encounter JSONB.", "EPIC-08", "FEAT-021", "US-045"],
        ["FR-006", "Provisional Diagnosis Coding", "Search and select ICD-10 / SNOMED CT diagnoses with free-text note override.", "P0", "BR-002", "Diagnosis saved with certainty (Provisional / Confirmed).", "EPIC-08", "FEAT-022", "US-047"],
        ["FR-007", "Electronic Prescription Generation", "Prescribe formulary drugs with dosage, frequency, duration, and food timing.", "P0", "BR-002", "Validated prescription sent to pharmacy queue immediately.", "EPIC-09", "FEAT-025", "US-052"],
        ["FR-008", "Pharmacy Dispense Confirmation", "Pharmacist verifies batch number, expiry date, and marks items as dispensed.", "P0", "BR-003", "Inventory ledger deducted; bilingual prescription slip printed.", "EPIC-10", "FEAT-028", "US-061"],
        ["FR-009", "Stock Ledger Deduction", "Automatic real-time deduction of medicine batch quantity upon dispense.", "P0", "BR-003", "Stock ledger updated within atomic ACID transaction.", "EPIC-11", "FEAT-031", "US-066"],
        ["FR-010", "Point-of-Care Lab Orders", "Doctor orders from 14 essential tests (RBS, Malaria, Dengue NS1, Urine, etc.).", "P1", "BR-009", "Lab order visible in lab queue with pending status.", "EPIC-12", "FEAT-035", "US-075"],
        ["FR-011", "Secondary Care Referral", "Generate outbound referral letter with clinical summary and destination hospital.", "P1", "BR-008", "Referral QR generated and status set to 'Referred'.", "EPIC-13", "FEAT-039", "US-083"],
        ["FR-012", "Offline Session Sync", "Queue local transactions and sync sequentially to server upon network reconnect.", "P0", "BR-007", "Zero data loss; conflict-free deterministic merge.", "EPIC-19", "FEAT-059", "US-125"]
    ]
    fr_content = f"""# ⚙️ Functional Requirements Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** REQ-FR-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Functional Scope & Verification Matrix

{get_req_table(["ID", "Title", "Description", "Priority", "Source Req", "Acceptance Criteria", "Epic", "Feature", "Story"], fr_rows)}
"""
    write_file(os.path.join(base_dir, "02-functional-requirements.md"), fr_content)

    # 03 Non-Functional Requirements
    nfr_rows = [
        ["NFR-001", "Sub-Second Latency", "API p95 latency < 300ms under standard clinic concurrency (50 requests/sec).", "Critical", "Load Testing with k6", "TD-ARC-01"],
        ["NFR-002", "High Availability", "99.9% uptime during operational clinic hours (08:00 to 20:00 IST Monday-Saturday).", "Critical", "Synthetic Uptime Monitors", "TD-OPS-04"],
        ["NFR-003", "Offline Resilience", "Complete offline operation capability for 8+ hours with zero browser crash.", "Critical", "Chaos Browser Disconnect", "TD-ARC-01"],
        ["NFR-004", "Data Integrity", "Zero data loss (RPO = 0) during network partition or abrupt client shutdown.", "Critical", "Transactional Flush Test", "TD-DB-03"],
        ["NFR-005", "Concurrent Clinic Scale", "Support 183 concurrent clinics with peak 500 active staff sessions without degradation.", "High", "Distributed Stress Test", "DPR Sec 6"],
        ["NFR-006", "Low Bandwidth Optimization", "Initial app load < 2MB; subsequent REST payload size < 15KB compressed.", "High", "Bundle Analyzer & Chrome DevTools", "TD-ARC-01"],
        ["NFR-007", "Accessibility (WCAG)", "Comply with WCAG 2.1 Level AA for all doctor, nurse, and citizen interfaces.", "Medium", "Axe Accessibility Scanner", "UM-BIL-01"],
        ["NFR-008", "Disaster Recovery (RTO)", "Recovery Time Objective < 60 minutes in the event of primary AZ cloud failure.", "High", "Multi-AZ RDS Failover Drill", "TD-OPS-04"]
    ]
    nfr_content = f"""# ⚡ Non-Functional Requirements Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** REQ-NFR-03 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. System Quality Attributes & SLA Thresholds

{get_req_table(["ID", "Title", "Specification & Threshold", "Priority", "Verification Method", "Source"], nfr_rows)}
"""
    write_file(os.path.join(base_dir, "03-non-functional-requirements.md"), nfr_content)

    # 04 Business Rules
    brules = [
        ["BRULE-001", "Free Healthcare Policy", "All consultations, medicines, and laboratory investigations are 100% free; zero financial collection is permitted."],
        ["BRULE-002", "Single Active Visit Rule", "A patient can possess at most one active (in-progress) visit per clinic per calendar day."],
        ["BRULE-003", "First-Expiry-First-Out (FEFO)", "Pharmacy dispensing algorithms must mandate dispensing the medicine batch with the nearest expiry date."],
        ["BRULE-004", "Controlled Drug Restriction", "Schedule H/H1 antibiotics and sedative drugs can only be dispensed against a verified doctor prescription."],
        ["BRULE-005", "Prescription Validity Window", "A routine outpatient prescription remains valid for dispensing for exactly 72 hours from consultation time."]
    ]
    write_file(os.path.join(base_dir, "04-business-rules.md"), f"# 📜 Business Rules\n\n{get_req_table(['ID', 'Rule Name', 'Enforcement Logic'], brules)}")

    # 05 Clinical Rules
    crules = [
        ["CRULE-001", "Hypertension Red Flag Alert", "Systolic BP >= 160 mmHg or Diastolic BP >= 100 mmHg must trigger immediate visual triage alert."],
        ["CRULE-002", "Pediatric Fever Danger Sign", "Temperature >= 102°F in infants under 12 months mandates immediate priority doctor queue jump."],
        ["CRULE-003", "Hypoglycemia Emergency Protocol", "Random Blood Glucose < 70 mg/dL mandates immediate clinical stabilization prompt."],
        ["CRULE-004", "Pregnancy Drug Safety Filter", "Category X or contraindicated drugs must be strictly blocked if pregnancy indicator is active."],
        ["CRULE-005", "Mandatory TB Screening Trigger", "Cough lasting > 2 weeks automatically triggers Sputum AFB / NAAT screening prompt."]
    ]
    write_file(os.path.join(base_dir, "05-clinical-rules.md"), f"# 🩺 Clinical Rules & Patient Safety Guardrails\n\n{get_req_table(['ID', 'Clinical Rule Name', 'Safety Condition & Action'], crules)}")

    # 06 Operational Rules
    orules = [
        ["ORULE-001", "Clinic Operating Hours", "Standard operational hours are 08:00 to 20:00 IST Monday through Saturday."],
        ["ORULE-002", "Daily Closing Physical Stock Count", "Pharmacist must record physical count of top 20 essential drugs before clinic day closure."],
        ["ORULE-003", "Emergency Walk-In Token Override", "Severe trauma or acute respiratory distress cases can be assigned Token E-1 to bypass queue."],
        ["ORULE-004", "Offline Queue Sync Frequency", "Offline client must attempt background synchronization every 30 seconds when network is detected."],
        ["ORULE-005", "Staff Session Inactivity Timeout", "Clinic terminal sessions must auto-lock after 15 minutes of user inactivity."]
    ]
    write_file(os.path.join(base_dir, "06-operational-rules.md"), f"# 🏢 Operational & Frontline Rules\n\n{get_req_table(['ID', 'Operational Rule', 'Operational Guideline'], orules)}")

    # 07-17 Other Requirements
    write_file(os.path.join(base_dir, "07-security-requirements.md"), "# 🔒 Security Requirements (SEC-001 to SEC-025)\n\nCovering RBAC, TLS 1.3, AES-256-GCM, Bcrypt password hashing, and token invalidation.")
    write_file(os.path.join(base_dir, "08-privacy-requirements.md"), "# 🛡️ Privacy & DPDP Compliance Requirements (PRIV-001 to PRIV-020)\n\nCovering citizen consent lifecycle, right to erasure, data minimization, and audit trails.")
    write_file(os.path.join(base_dir, "09-performance-requirements.md"), "# ⏱️ Performance Requirements (PERF-001 to PERF-015)\n\nTargeting <300ms p95 response time, sub-second search, and efficient client bundle sizes.")
    write_file(os.path.join(base_dir, "10-availability-requirements.md"), "# 📈 Availability & Resilience Requirements (AVAIL-001 to AVAIL-015)\n\nTargeting 99.9% uptime, multi-AZ failover, and automatic database health checks.")
    write_file(os.path.join(base_dir, "11-localization-requirements.md"), "# 🌐 Localization Requirements (LOC-001 to LOC-015)\n\nEnforcing complete bilingual English and Kannada (`kn_IN`) string catalogs.")
    write_file(os.path.join(base_dir, "12-accessibility-requirements.md"), "# ♿ Accessibility Requirements (ACC-001 to ACC-015)\n\nEnforcing WCAG 2.1 Level AA color contrast, keyboard navigation, and screen-reader tags.")
    write_file(os.path.join(base_dir, "13-offline-requirements.md"), "# 📴 Offline Operation Requirements (OFF-001 to OFF-020)\n\nSpecifying IndexedDB storage limits, background sync queues, and conflict resolution.")
    write_file(os.path.join(base_dir, "14-reporting-requirements.md"), "# 📊 Reporting Requirements (REP-001 to REP-020)\n\nCovering daily OPD registers, monthly stock consumption, and disease prevalence reports.")
    write_file(os.path.join(base_dir, "15-analytics-requirements.md"), "# 📈 Analytics Requirements (ANL-001 to ANL-020)\n\nCovering Star Schema data marts, syndromic anomaly alerts, and executive KPIs.")
    write_file(os.path.join(base_dir, "16-ai-requirements.md"), "# 🤖 AI Decision Support Requirements (AI-001 to AI-015)\n\nCovering non-autonomous stockout forecasts, fever anomaly detection, and human sign-off.")
    write_file(os.path.join(base_dir, "17-integration-requirements.md"), "# 🔌 External Integration Requirements (INT-001 to INT-020)\n\nCovering ABDM ABHA creation, FHIR R4 bundles, eHospital referral bridge, and SMS gateway.")

# ==========================================
# PHASE 3: WORKFLOWS GENERATOR
# ==========================================

def build_phase_3():
    base_dir = os.path.join("docs", "03-workflows")
    
    workflows = [
        ("01-master-clinic-workflow.md", "Master Clinic Day Operational Workflow", """```mermaid
sequenceDiagram
    autonumber
    actor P as Patient
    actor N as Staff Nurse
    actor D as Doctor
    actor PH as Pharmacist
    actor L as Lab Tech
    P->>N: 1. Arrives at Clinic Desk
    N->>N: 2. Search / Register Patient & Issue Token
    N->>N: 3. Record Vitals & Triage Priority
    N->>D: 4. Patient Enters Doctor Room
    D->>D: 5. Examination, Diagnosis & e-Prescription
    alt Lab Required
        D->>L: 6a. Order Point-of-Care Lab Test
        L->>D: 6b. Collect Sample & Enter Result
    end
    D->>PH: 7. e-Prescription Sent to Pharmacy
    PH->>P: 8. Dispense Medicines (FEFO) & Explain Dosage
    P->>P: 9. Patient Departs Clinic
```"""),
        ("02-login-authentication-workflow.md", "Staff Authentication & Role-Based Session Workflow", """```mermaid
sequenceDiagram
    autonumber
    actor S as Clinic Staff
    participant UI as Frontend PWA
    participant API as Auth Service
    participant DB as Users Table
    S->>UI: Enter Username / Staff ID & Password
    UI->>API: POST /api/v1/auth/login
    API->>DB: Verify bcrypt hash & active status
    DB-->>API: User & Role Permissions
    API-->>UI: JWT Access Token + Refresh Token (HttpOnly)
    UI-->>S: Role-Specific Dashboard Loaded
```"""),
        ("03-patient-registration-workflow.md", "New Patient Registration & Demographics Capture", """```mermaid
flowchart TD
    A[Citizen Arrives] --> B{Existing Patient?}
    B -- Yes --> C[Search via Mobile / UHID]
    B -- No --> D[Enter Name, Phone, Age, Gender, Ward]
    D --> E{Link ABHA?}
    E -- Yes --> F[Aadhaar OTP / Scan ABHA QR]
    E -- No --> G[Generate Internal UHID]
    F --> G
    G --> H[Issue Daily Queue Token]
    H --> I[Proceed to Triage Desk]
```"""),
        ("04-patient-search-workflow.md", "Rapid Patient Search & Identity Verification", "Search patient by Phone, UHID, ABHA ID with fast trigram matching."),
        ("05-repeat-patient-workflow.md", "Repeat Patient Encounter & Visit Linking", "Link previous clinical history, past prescriptions, and chronic NCD records."),
        ("06-consent-workflow.md", "Citizen Consent & Privacy Acknowledgement", "Capture DPDP Act compliant explicit consent for health data recording and ABDM sharing."),
        ("07-token-generation-workflow.md", "Daily Token Generation & Slip Printing", "Generate sequential daily token, print 2-inch thermal slip with QR code."),
        ("08-queue-workflow.md", "Dynamic Queue Management & Doctor Room Routing", "Maintain real-time queue states (Waiting, In-Consultation, Lab-Pending, Completed)."),
        ("09-triage-workflow.md", "Vitals Capture & Clinical Triage Prioritization", "Record BP, Pulse, SpO2, Temp, Glucose; flag abnormal vitals for urgent queue escalation."),
        ("10-danger-alert-workflow.md", "Clinical Danger Alert & Emergency Escalation", "Immediate audio-visual alert for hypertensive crisis, severe respiratory distress, or shock."),
        ("11-doctor-consultation-workflow.md", "Doctor Clinical Examination & EMR Documentation", "Review vitals, select chief complaints, enter clinical findings and provisional diagnosis."),
        ("12-prescription-workflow.md", "Electronic Prescription & Formulary Verification", "Select medicines, dosage, food instructions, check drug allergies and stock availability."),
        ("13-pharmacy-dispensing-workflow.md", "Pharmacy Dispensing & Batch Verification", "Verify prescription, select batch via FEFO, confirm dispensed quantity, print bilingual slip."),
        ("14-stock-replenishment-workflow.md", "Stock Indent, Receipt & Batch Inventory Management", "Create monthly clinic indent, record stock delivery from zonal warehouse, log batch expiry."),
        ("15-laboratory-workflow.md", "Point-of-Care Lab Test Ordering & Result Entry", "Order 14 essential tests, log sample collection, enter numeric/qualitative result."),
        ("16-referral-workflow.md", "Secondary Care Referral & Clinical Summary Generation", "Generate outbound referral letter with QR code for BBMP General Hospital or Medical College."),
        ("17-follow-up-workflow.md", "NCD Patient Recall & Follow-Up Scheduling", "Schedule 30-day follow-up for hypertensive and diabetic patients; trigger SMS reminders."),
        ("18-notification-workflow.md", "Automated Citizen Notification & Telephony Alerts", "Send visit summary, drug dosage instructions, and follow-up reminders via SMS."),
        ("19-grievance-workflow.md", "Citizen Grievance Submission & Resolution Tracking", "Capture citizen feedback on wait times, medicine availability, and staff behavior."),
        ("20-audit-workflow.md", "Data Access Auditing & Forensic Log Review", "Log every access to patient demographic and clinical records in immutable audit table."),
        ("21-analytics-workflow.md", "Public Health Data Extraction & Zonal Dashboard Refresh", "Daily ELT aggregation of clinic encounters into Star Schema for epidemiological tracking."),
        ("22-offline-workflow.md", "Offline Clinic Operation & Transactional Queuing", "Operate PWA seamlessly without internet; queue all mutations in local IndexedDB."),
        ("23-sync-conflict-workflow.md", "Sync Conflict Resolution & Exception Handling", "Deterministic merge of offline transactions upon reconnect; flag clinical discrepancies."),
        ("24-ABDM-workflow.md", "Ayushman Bharat Digital Mission (ABHA) Interoperability", "Verify ABHA, create FHIR R4 Care Context, and link health records to national ABDM network."),
        ("25-emergency-exception-workflow.md", "Emergency Walk-In & Trauma Exception Protocol", "Emergency bypass workflow allowing immediate doctor consultation without prior registration.")
    ]

    for filename, title, diagram_or_desc in workflows:
        content = f"""# 🔄 Workflow: {title}
## Namma Clinic Digital Health & Operations Platform
**Document Code:** WF-{filename[:2]} | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Workflow Overview & Architecture
This document defines the end-to-end operational, technical, and data flow for **{title}**.

### 2. Operational Specification
- **Primary Actors:** Frontline Clinic Staff (Nurse, Doctor, Pharmacist, Lab Tech, Patient)
- **Trigger:** Event initiation in clinic environment
- **Preconditions:** Active clinic session and verified user permissions
- **Security & RBAC:** Role-checked at API gateway and client UI state
- **Offline Resilience:** Local transaction persistence with deterministic sync queue
- **Audit Logging:** Emits structured immutable audit record upon state transition

### 3. Workflow Diagram & Sequence
{diagram_or_desc}

### 4. Database & API Touchpoints
- **APIs Involved:** Dedicated REST endpoints with idempotency keys
- **Database Entities:** ACID transaction boundaries across core relational tables
- **Audit Events:** `AUDIT_EVENT_CREATED` recorded in `access_audit_logs`
"""
        write_file(os.path.join(base_dir, filename), content)

def main():
    build_phase_2()
    build_phase_3()

if __name__ == "__main__":
    main()
