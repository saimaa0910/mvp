# Namma Clinic Planned Screen Catalog Specification

## 1. Executive Summary & Screen Registry Scope
This document establishes the canonical, implementation-ready catalog of all **108 planned frontend screens** (`SCREEN-001` through `SCREEN-108`) for the Namma Clinic Digital Health & Operations Platform. Each specification details the operational purpose, visual layout primitives, entry and exit conditions, upstream API contracts, offline behaviors, WCAG 2.1 AA accessibility bindings, and automated acceptance criteria.

## 2. Global Screen Master Registry Table
| Screen ID | Screen Name | Module | Primary Route | Primary Role | Offline Capability | Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-001` | User Login Screen | `MODULE-001` | `/login` | Receptionist / Registration Clerk | Online Only | `PLANNED-TEST-FE-001` |
| `SCREEN-002` | MFA Verification Screen | `MODULE-001` | `/login/mfa` | Receptionist / Registration Clerk | Online Only | `PLANNED-TEST-FE-002` |
| `SCREEN-003` | Terminal Pairing & Device Enrollment | `MODULE-001` | `/system/device-enroll` | Clinic Administrative Officer | Online Only | `PLANNED-TEST-FE-003` |
| `SCREEN-004` | Clinic Shift Check-In & Handover | `MODULE-001` | `/shift/checkin` | Receptionist / Registration Clerk | Degraded Offline | `PLANNED-TEST-FE-004` |
| `SCREEN-005` | Emergency Break-Glass Authorization | `MODULE-001` | `/auth/break-glass` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-005` |
| `SCREEN-006` | Master Clinic Dashboard | `MODULE-002` | `/dashboard` | Receptionist / Registration Clerk | Degraded Offline | `PLANNED-TEST-FE-006` |
| `SCREEN-007` | Doctor Outpatient Console | `MODULE-002` | `/doctor/console` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-007` |
| `SCREEN-008` | Staff Nurse Triage Workbench | `MODULE-002` | `/nurse/triage` | Staff Nurse / Triage Specialist | Full Offline | `PLANNED-TEST-FE-008` |
| `SCREEN-009` | Pharmacy Dispensing Console | `MODULE-002` | `/pharmacy/dispense` | Pharmacist / Dispenser | Full Offline | `PLANNED-TEST-FE-009` |
| `SCREEN-010` | Diagnostic Laboratory Workbench | `MODULE-002` | `/lab/workbench` | Laboratory Technician | Full Offline | `PLANNED-TEST-FE-010` |
| `SCREEN-011` | Citizen New Registration Screen | `MODULE-003` | `/patients/new` | Receptionist / Registration Clerk | Full Offline | `PLANNED-TEST-FE-011` |
| `SCREEN-012` | Citizen Search & Retrieval Screen | `MODULE-003` | `/patients/search` | Receptionist / Registration Clerk | Full Offline | `PLANNED-TEST-FE-012` |
| `SCREEN-013` | Patient Longitudinal Profile View | `MODULE-003` | `/patients/:id` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-013` |
| `SCREEN-014` | Repeat Patient Fast Intake | `MODULE-003` | `/patients/:id/repeat-intake` | Receptionist / Registration Clerk | Full Offline | `PLANNED-TEST-FE-014` |
| `SCREEN-015` | Biometric & ABHA Card Scan Modal | `MODULE-003` | `/patients/abha-scan` | Receptionist / Registration Clerk | Degraded Offline | `PLANNED-TEST-FE-015` |
| `SCREEN-016` | Citizen Demographic Correction Form | `MODULE-003` | `/patients/:id/edit` | Receptionist / Registration Clerk | Degraded Offline | `PLANNED-TEST-FE-016` |
| `SCREEN-017` | Duplicate Citizen Merge Modal | `MODULE-003` | `/patients/merge` | Clinic Administrative Officer | Online Only | `PLANNED-TEST-FE-017` |
| `SCREEN-018` | Citizen Digital Photo Capture | `MODULE-003` | `/patients/:id/photo` | Receptionist / Registration Clerk | Full Offline | `PLANNED-TEST-FE-018` |
| `SCREEN-019` | DPDP Informed Consent Capture Screen | `MODULE-004` | `/patients/:id/consent` | Receptionist / Registration Clerk | Full Offline | `PLANNED-TEST-FE-019` |
| `SCREEN-020` | Consent History & Revocation Console | `MODULE-004` | `/patients/:id/consents` | Receptionist / Registration Clerk | Full Offline | `PLANNED-TEST-FE-020` |
| `SCREEN-021` | Data Portability & Export Request | `MODULE-004` | `/patients/:id/export` | Receptionist / Registration Clerk | Degraded Offline | `PLANNED-TEST-FE-021` |
| `SCREEN-022` | Citizen Grievance Redressal Intake | `MODULE-004` | `/patients/:id/grievance` | Receptionist / Registration Clerk | Full Offline | `PLANNED-TEST-FE-022` |
| `SCREEN-023` | Grievance Investigation & Resolution | `MODULE-004` | `/grievances/:id` | Grievance Redressal Officer | Online Only | `PLANNED-TEST-FE-023` |
| `SCREEN-024` | OPD Token Generation & Print Modal | `MODULE-005` | `/queue/tokens/new` | Receptionist / Registration Clerk | Full Offline | `PLANNED-TEST-FE-024` |
| `SCREEN-025` | Master Waiting Room Queue Display | `MODULE-005` | `/queue/display` | Receptionist / Registration Clerk | Full Offline | `PLANNED-TEST-FE-025` |
| `SCREEN-026` | Queue Management & Rerouting Screen | `MODULE-005` | `/queue/manage` | Staff Nurse / Triage Specialist | Full Offline | `PLANNED-TEST-FE-026` |
| `SCREEN-027` | Express Triage Queue | `MODULE-005` | `/queue/triage-express` | Staff Nurse / Triage Specialist | Full Offline | `PLANNED-TEST-FE-027` |
| `SCREEN-028` | Pharmacy Pickup Waiting Screen | `MODULE-005` | `/queue/pharmacy` | Pharmacist / Dispenser | Full Offline | `PLANNED-TEST-FE-028` |
| `SCREEN-029` | Triage Vitals Entry Form | `MODULE-006` | `/triage/:visitId/vitals` | Staff Nurse / Triage Specialist | Full Offline | `PLANNED-TEST-FE-029` |
| `SCREEN-030` | Pediatric Growth Chart & Z-Scores | `MODULE-006` | `/triage/:visitId/pediatric` | Staff Nurse / Triage Specialist | Full Offline | `PLANNED-TEST-FE-030` |
| `SCREEN-031` | Antenatal Care (ANC) Vitals Intake | `MODULE-006` | `/triage/:visitId/anc` | Staff Nurse / Triage Specialist | Full Offline | `PLANNED-TEST-FE-031` |
| `SCREEN-032` | Danger Signs & Triage Warning Modal | `MODULE-006` | `/triage/:visitId/danger-modal` | Staff Nurse / Triage Specialist | Full Offline | `PLANNED-TEST-FE-032` |
| `SCREEN-033` | Point-of-Care Blood Sugar Entry | `MODULE-006` | `/triage/:visitId/glucometer` | Staff Nurse / Triage Specialist | Full Offline | `PLANNED-TEST-FE-033` |
| `SCREEN-034` | Triage Station History Log | `MODULE-006` | `/triage/station-history` | Staff Nurse / Triage Specialist | Full Offline | `PLANNED-TEST-FE-034` |
| `SCREEN-035` | Clinical Consultation Workspace | `MODULE-007` | `/consultations/:visitId` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-035` |
| `SCREEN-036` | Chief Complaints & Systemic Review | `MODULE-007` | `/consultations/:visitId/symptoms` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-036` |
| `SCREEN-037` | Physical & Clinical Examination Form | `MODULE-007` | `/consultations/:visitId/exam` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-037` |
| `SCREEN-038` | ICD-10 & SNOMED CT Diagnosis Picker | `MODULE-007` | `/consultations/:visitId/diagnosis` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-038` |
| `SCREEN-039` | NCD Chronic Disease Registry Form | `MODULE-007` | `/consultations/:visitId/ncd` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-039` |
| `SCREEN-040` | Past Medical & Surgical History Modal | `MODULE-007` | `/consultations/:visitId/history` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-040` |
| `SCREEN-041` | Drug Allergy & Adverse Reaction Logger | `MODULE-007` | `/consultations/:visitId/allergies` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-041` |
| `SCREEN-042` | Clinical Progress Note & Free-Text Area | `MODULE-007` | `/consultations/:visitId/notes` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-042` |
| `SCREEN-043` | Doctor Teleconsultation Video Room | `MODULE-007` | `/consultations/:visitId/teleconsult` | Medical Officer / General Physician | Online Only | `PLANNED-TEST-FE-043` |
| `SCREEN-044` | Consultation Summary & Lock Dialog | `MODULE-007` | `/consultations/:visitId/sign` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-044` |
| `SCREEN-045` | Doctor Outpatient Day Book View | `MODULE-007` | `/doctor/daybook` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-045` |
| `SCREEN-046` | Electronic Prescription Form | `MODULE-008` | `/prescriptions/:consultationId/new` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-046` |
| `SCREEN-047` | Drug-Drug & Drug-Allergy Warning Modal | `MODULE-008` | `/prescriptions/interaction-modal` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-047` |
| `SCREEN-048` | Standard Clinical Treatment Regimen Picker | `MODULE-008` | `/prescriptions/templates` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-048` |
| `SCREEN-049` | Prescription Bilingual Print Preview | `MODULE-008` | `/prescriptions/:id/print` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-049` |
| `SCREEN-050` | Medication Modification & Cancellation | `MODULE-008` | `/prescriptions/:id/modify` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-050` |
| `SCREEN-051` | Recurring Refill Request Form | `MODULE-008` | `/prescriptions/:id/refill` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-051` |
| `SCREEN-052` | Clinic Formulary & Stock Lookup Modal | `MODULE-008` | `/formulary/lookup` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-052` |
| `SCREEN-053` | Pharmacy Active Dispensing Screen | `MODULE-009` | `/pharmacy/dispense/:id` | Pharmacist / Dispenser | Full Offline | `PLANNED-TEST-FE-053` |
| `SCREEN-054` | Partial Dispensing & Stockout Dialog | `MODULE-009` | `/pharmacy/dispense/:id/partial` | Pharmacist / Dispenser | Full Offline | `PLANNED-TEST-FE-054` |
| `SCREEN-055` | Medicine Counseling Label Print Modal | `MODULE-009` | `/pharmacy/labels/print` | Pharmacist / Dispenser | Full Offline | `PLANNED-TEST-FE-055` |
| `SCREEN-056` | Pharmacy Shift Reconciliation Form | `MODULE-009` | `/pharmacy/shift-reconciliation` | Pharmacist / Dispenser | Full Offline | `PLANNED-TEST-FE-056` |
| `SCREEN-057` | Expired & Damaged Drug Quarantine Form | `MODULE-009` | `/pharmacy/quarantine` | Pharmacist / Dispenser | Full Offline | `PLANNED-TEST-FE-057` |
| `SCREEN-058` | Emergency Stock Requisition Form | `MODULE-009` | `/pharmacy/requisitions/new` | Pharmacist / Dispenser | Degraded Offline | `PLANNED-TEST-FE-058` |
| `SCREEN-059` | Pharmacy Dispensing Log History | `MODULE-009` | `/pharmacy/history` | Pharmacist / Dispenser | Full Offline | `PLANNED-TEST-FE-059` |
| `SCREEN-060` | Controlled Substances & High-Alert Register | `MODULE-009` | `/pharmacy/controlled-register` | Pharmacist / Dispenser | Online Only | `PLANNED-TEST-FE-060` |
| `SCREEN-061` | Clinic Stock Inventory Dashboard | `MODULE-010` | `/inventory` | Pharmacist / Dispenser | Full Offline | `PLANNED-TEST-FE-061` |
| `SCREEN-062` | Stock Goods Receipt Note (GRN) Form | `MODULE-010` | `/inventory/receipt` | Pharmacist / Dispenser | Full Offline | `PLANNED-TEST-FE-062` |
| `SCREEN-063` | Cold Chain Refrigerator Telemetry View | `MODULE-010` | `/inventory/cold-chain` | Pharmacist / Dispenser | Full Offline | `PLANNED-TEST-FE-063` |
| `SCREEN-064` | Vaccine Stock & VVM Status Manager | `MODULE-010` | `/inventory/vaccines` | Staff Nurse / Triage Specialist | Full Offline | `PLANNED-TEST-FE-064` |
| `SCREEN-065` | Inter-Clinic Stock Transfer Dispatch | `MODULE-010` | `/inventory/transfers/out` | Pharmacist / Dispenser | Degraded Offline | `PLANNED-TEST-FE-065` |
| `SCREEN-066` | Inter-Clinic Stock Transfer Receipt | `MODULE-010` | `/inventory/transfers/in` | Pharmacist / Dispenser | Degraded Offline | `PLANNED-TEST-FE-066` |
| `SCREEN-067` | Annual / Monthly Physical Audit Form | `MODULE-010` | `/inventory/audit` | Clinic Administrative Officer | Online Only | `PLANNED-TEST-FE-067` |
| `SCREEN-068` | Supplier Recall & Ban Notification Modal | `MODULE-010` | `/inventory/recalls` | Pharmacist / Dispenser | Full Offline | `PLANNED-TEST-FE-068` |
| `SCREEN-069` | Diagnostic Lab Test Orders Queue | `MODULE-011` | `/lab/orders` | Laboratory Technician | Full Offline | `PLANNED-TEST-FE-069` |
| `SCREEN-070` | Specimen Collection & Barcode Label Screen | `MODULE-011` | `/lab/specimen/:id` | Laboratory Technician | Full Offline | `PLANNED-TEST-FE-070` |
| `SCREEN-071` | Point-of-Care Rapid Test Result Entry | `MODULE-011` | `/lab/results/poc/:id` | Laboratory Technician | Full Offline | `PLANNED-TEST-FE-071` |
| `SCREEN-072` | Hematology Analyzer Data Import Screen | `MODULE-011` | `/lab/analyzers/import` | Laboratory Technician | Full Offline | `PLANNED-TEST-FE-072` |
| `SCREEN-073` | Lab Results Validation & Doctor Alert | `MODULE-011` | `/lab/results/validate/:id` | Laboratory Technician | Full Offline | `PLANNED-TEST-FE-073` |
| `SCREEN-074` | Diagnostic Report Bilingual Print Preview | `MODULE-011` | `/lab/reports/:id/print` | Laboratory Technician | Full Offline | `PLANNED-TEST-FE-074` |
| `SCREEN-075` | External Referral Lab Dispatch Form | `MODULE-011` | `/lab/referrals/out` | Laboratory Technician | Degraded Offline | `PLANNED-TEST-FE-075` |
| `SCREEN-076` | Lab Reagent & Quality Control Log | `MODULE-011` | `/lab/qc` | Laboratory Technician | Full Offline | `PLANNED-TEST-FE-076` |
| `SCREEN-077` | Secondary / Tertiary Referral Form | `MODULE-012` | `/referrals/new` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-077` |
| `SCREEN-078` | 108 Emergency Ambulance Dispatch Screen | `MODULE-012` | `/referrals/ambulance-108` | Medical Officer / General Physician | Degraded Offline | `PLANNED-TEST-FE-078` |
| `SCREEN-079` | Referral Handover Dossier Print Preview | `MODULE-012` | `/referrals/:id/print` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-079` |
| `SCREEN-080` | Active Outgoing Referrals Tracker | `MODULE-012` | `/referrals/tracking` | Staff Nurse / Triage Specialist | Degraded Offline | `PLANNED-TEST-FE-080` |
| `SCREEN-081` | Discharge / Counter-Referral Ingest Form | `MODULE-012` | `/referrals/counter-referral` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-081` |
| `SCREEN-082` | Emergency Resuscitation Incident Record | `MODULE-012` | `/referrals/resuscitation` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-082` |
| `SCREEN-083` | Citizen SMS & Communication Center | `MODULE-013` | `/notifications/sms-center` | Receptionist / Registration Clerk | Degraded Offline | `PLANNED-TEST-FE-083` |
| `SCREEN-084` | Chronic Disease Follow-Up Schedule | `MODULE-013` | `/followup/schedule` | Staff Nurse / Triage Specialist | Full Offline | `PLANNED-TEST-FE-084` |
| `SCREEN-085` | ASHA Worker Community Outreach Tasklist | `MODULE-013` | `/followup/asha-tasks` | ASHA Link Worker Coordinator | Full Offline | `PLANNED-TEST-FE-085` |
| `SCREEN-086` | Public Health Broadcast Composer | `MODULE-013` | `/notifications/broadcasts` | Zonal Health Officer (ZHO) | Online Only | `PLANNED-TEST-FE-086` |
| `SCREEN-087` | Adverse Event Notification Form | `MODULE-013` | `/notifications/adverse-events` | Medical Officer / General Physician | Full Offline | `PLANNED-TEST-FE-087` |
| `SCREEN-088` | Missed Follow-up Outreach Dialer Console | `MODULE-013` | `/followup/dialer` | Receptionist / Registration Clerk | Online Only | `PLANNED-TEST-FE-088` |
| `SCREEN-089` | Epidemic Outbreak Surveillance Dashboard | `MODULE-014` | `/analytics/surveillance` | Epidemiologist / Disease Surveillance Officer | Degraded Offline | `PLANNED-TEST-FE-089` |
| `SCREEN-090` | Ward Health Performance & KPI Scorecard | `MODULE-014` | `/analytics/ward-kpi` | Ward Health Supervisor | Degraded Offline | `PLANNED-TEST-FE-090` |
| `SCREEN-091` | Pharmacy Dispensing & Consumption Analytics | `MODULE-014` | `/analytics/drug-utilization` | Pharmacist / Dispenser | Degraded Offline | `PLANNED-TEST-FE-091` |
| `SCREEN-092` | Laboratory Diagnostic Workload Dashboard | `MODULE-014` | `/analytics/lab-metrics` | Laboratory Technician | Degraded Offline | `PLANNED-TEST-FE-092` |
| `SCREEN-093` | Maternal & Child Health Coverage Heatmap | `MODULE-014` | `/analytics/mch-coverage` | Zonal Health Officer (ZHO) | Degraded Offline | `PLANNED-TEST-FE-093` |
| `SCREEN-094` | Custom Report Builder & CSV Export | `MODULE-014` | `/analytics/custom-reports` | Clinic Administrative Officer | Online Only | `PLANNED-TEST-FE-094` |
| `SCREEN-095` | Offline Storage & SQLite WAL Status | `MODULE-015` | `/system/offline-storage` | Clinic Administrative Officer | Full Offline | `PLANNED-TEST-FE-095` |
| `SCREEN-096` | Sync Queue Monitor & Manual Flush | `MODULE-015` | `/system/sync-queue` | Clinic Administrative Officer | Full Offline | `PLANNED-TEST-FE-096` |
| `SCREEN-097` | Sync Conflict Visual Resolution Modal | `MODULE-015` | `/system/conflicts/:id` | Clinic Administrative Officer | Degraded Offline | `PLANNED-TEST-FE-097` |
| `SCREEN-098` | Peer-to-Peer Local WiFi Sync Setup | `MODULE-015` | `/system/p2p-sync` | IT Support & Hardware Engineer | Full Offline | `PLANNED-TEST-FE-098` |
| `SCREEN-099` | Offline Cryptographic Token Cache | `MODULE-015` | `/system/offline-auth` | Clinic Administrative Officer | Full Offline | `PLANNED-TEST-FE-099` |
| `SCREEN-100` | Local Backup & USB Snapshot Export | `MODULE-015` | `/system/local-backup` | Clinic Administrative Officer | Full Offline | `PLANNED-TEST-FE-100` |
| `SCREEN-101` | ABHA Creation & Mobile Verification | `MODULE-016` | `/abdm/abha-create` | Receptionist / Registration Clerk | Online Only | `PLANNED-TEST-FE-101` |
| `SCREEN-102` | ABDM Consent Request & Artifact Drawer | `MODULE-016` | `/abdm/consent-requests` | Medical Officer / General Physician | Online Only | `PLANNED-TEST-FE-102` |
| `SCREEN-103` | FHIR R4 Health Data Push Monitor | `MODULE-016` | `/abdm/fhir-push` | ABDM National Integration Officer | Degraded Offline | `PLANNED-TEST-FE-103` |
| `SCREEN-104` | External Hospital Records Viewer | `MODULE-016` | `/abdm/external-records/:uhid` | Medical Officer / General Physician | Online Only | `PLANNED-TEST-FE-104` |
| `SCREEN-105` | Cryptographic WORM Audit Log Viewer | `MODULE-017` | `/audit/logs` | Quality & Compliance Auditor | Full Offline | `PLANNED-TEST-FE-105` |
| `SCREEN-106` | Security Incident & Intrusion Alert Board | `MODULE-017` | `/security/alerts` | Security Administrator / CISO | Degraded Offline | `PLANNED-TEST-FE-106` |
| `SCREEN-107` | User Management & Role Assignment | `MODULE-017` | `/admin/users` | Clinic Administrative Officer | Online Only | `PLANNED-TEST-FE-107` |
| `SCREEN-108` | Clinic Master Settings & Hardware Registry | `MODULE-017` | `/admin/settings` | Clinic Administrative Officer | Full Offline | `PLANNED-TEST-FE-108` |

## 3. Exhaustive Screen Specifications

### SCREEN-001: User Login Screen
**Module:** `MODULE-001` | **Primary Route:** `/login` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `User Login Screen` screen (SCREEN-001) provides the user interface for Credential entry with Argon2id client hashing and biometric prompt. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Medical Officer / General Physician, Staff Nurse / Triage Specialist, Pharmacist / Dispenser, Laboratory Technician, Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-AUTH-001, API-AUTH-002`
- **Underlying Database Tables:** `auth_users, user_sessions`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with User Login Screen (SCREEN-001)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/login'
  When user completes operational interaction on screen 'SCREEN-001'
  Then the system persists data to 'API-AUTH-001, API-AUTH-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-001' validates state transitions and UI responsiveness
```

---

### SCREEN-002: MFA Verification Screen
**Module:** `MODULE-001` | **Primary Route:** `/login/mfa` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `MFA Verification Screen` screen (SCREEN-002) provides the user interface for Time-based OTP or WebAuthn hardware security key verification. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Medical Officer / General Physician, Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-AUTH-002`
- **Underlying Database Tables:** `user_sessions`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with MFA Verification Screen (SCREEN-002)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/login/mfa'
  When user completes operational interaction on screen 'SCREEN-002'
  Then the system persists data to 'API-AUTH-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-002' validates state transitions and UI responsiveness
```

---

### SCREEN-003: Terminal Pairing & Device Enrollment
**Module:** `MODULE-001` | **Primary Route:** `/system/device-enroll` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `Terminal Pairing & Device Enrollment` screen (SCREEN-003) provides the user interface for Hardware fingerprint registration and mTLS cert binding. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-006` (Clinic Administrative Officer)
- **Secondary / Supervisory Roles:** IT Support & Hardware Engineer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-SYS-001`
- **Underlying Database Tables:** `hardware_terminals`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Terminal Pairing & Device Enrollment (SCREEN-003)
  Given user is authenticated with role 'ROLE-006'
  And the active terminal is assigned to route '/system/device-enroll'
  When user completes operational interaction on screen 'SCREEN-003'
  Then the system persists data to 'API-SYS-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-003' validates state transitions and UI responsiveness
```

---

### SCREEN-004: Clinic Shift Check-In & Handover
**Module:** `MODULE-001` | **Primary Route:** `/shift/checkin` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Clinic Shift Check-In & Handover` screen (SCREEN-004) provides the user interface for Active roster confirmation, station assignment, and cash float check. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Medical Officer / General Physician, Staff Nurse / Triage Specialist, Pharmacist / Dispenser
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-AUTH-005`
- **Underlying Database Tables:** `clinic_shifts`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Clinic Shift Check-In & Handover (SCREEN-004)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/shift/checkin'
  When user completes operational interaction on screen 'SCREEN-004'
  Then the system persists data to 'API-AUTH-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-004' validates state transitions and UI responsiveness
```

---

### SCREEN-005: Emergency Break-Glass Authorization
**Module:** `MODULE-001` | **Primary Route:** `/auth/break-glass` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Emergency Break-Glass Authorization` screen (SCREEN-005) provides the user interface for High-priority override with statutory justification and WORM audit logging. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-AUTH-004`
- **Underlying Database Tables:** `audit_events, consultations`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Emergency Break-Glass Authorization (SCREEN-005)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/auth/break-glass'
  When user completes operational interaction on screen 'SCREEN-005'
  Then the system persists data to 'API-AUTH-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-005' validates state transitions and UI responsiveness
```

---

### SCREEN-006: Master Clinic Dashboard
**Module:** `MODULE-002` | **Primary Route:** `/dashboard` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Master Clinic Dashboard` screen (SCREEN-006) provides the user interface for Live OPD operational metrics, triage queue health, and stock alerts. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Medical Officer / General Physician, Staff Nurse / Triage Specialist, Pharmacist / Dispenser, Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-ANL-001`
- **Underlying Database Tables:** `visits, triage_assessments, pharmacy_batches`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Master Clinic Dashboard (SCREEN-006)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/dashboard'
  When user completes operational interaction on screen 'SCREEN-006'
  Then the system persists data to 'API-ANL-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-006' validates state transitions and UI responsiveness
```

---

### SCREEN-007: Doctor Outpatient Console
**Module:** `MODULE-002` | **Primary Route:** `/doctor/console` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Doctor Outpatient Console` screen (SCREEN-007) provides the user interface for Active patient waiting list, vitals preview, and consultation launcher. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-VST-001, API-CON-001`
- **Underlying Database Tables:** `visits, consultations`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Doctor Outpatient Console (SCREEN-007)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/doctor/console'
  When user completes operational interaction on screen 'SCREEN-007'
  Then the system persists data to 'API-VST-001, API-CON-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-007' validates state transitions and UI responsiveness
```

---

### SCREEN-008: Staff Nurse Triage Workbench
**Module:** `MODULE-002` | **Primary Route:** `/nurse/triage` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Staff Nurse Triage Workbench` screen (SCREEN-008) provides the user interface for Rapid intake vitals grid, early warning score calculator, and queue routing. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-003` (Staff Nurse / Triage Specialist)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-TRG-001`
- **Underlying Database Tables:** `triage_assessments`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Staff Nurse Triage Workbench (SCREEN-008)
  Given user is authenticated with role 'ROLE-003'
  And the active terminal is assigned to route '/nurse/triage'
  When user completes operational interaction on screen 'SCREEN-008'
  Then the system persists data to 'API-TRG-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-008' validates state transitions and UI responsiveness
```

---

### SCREEN-009: Pharmacy Dispensing Console
**Module:** `MODULE-002` | **Primary Route:** `/pharmacy/dispense` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Pharmacy Dispensing Console` screen (SCREEN-009) provides the user interface for Prescription verification, barcode scanning, and FEFO stock deduction. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PHR-001`
- **Underlying Database Tables:** `prescriptions, pharmacy_batches`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Pharmacy Dispensing Console (SCREEN-009)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/pharmacy/dispense'
  When user completes operational interaction on screen 'SCREEN-009'
  Then the system persists data to 'API-PHR-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-009' validates state transitions and UI responsiveness
```

---

### SCREEN-010: Diagnostic Laboratory Workbench
**Module:** `MODULE-002` | **Primary Route:** `/lab/workbench` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Diagnostic Laboratory Workbench` screen (SCREEN-010) provides the user interface for Specimen collection, rapid test kit entry, and result authorization. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-005` (Laboratory Technician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-LAB-001`
- **Underlying Database Tables:** `lab_orders, lab_results`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Diagnostic Laboratory Workbench (SCREEN-010)
  Given user is authenticated with role 'ROLE-005'
  And the active terminal is assigned to route '/lab/workbench'
  When user completes operational interaction on screen 'SCREEN-010'
  Then the system persists data to 'API-LAB-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-010' validates state transitions and UI responsiveness
```

---

### SCREEN-011: Citizen New Registration Screen
**Module:** `MODULE-003` | **Primary Route:** `/patients/new` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Citizen New Registration Screen` screen (SCREEN-011) provides the user interface for Demographic entry, mobile OTP verification, and photo capture. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist, Data Entry Operator
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PAT-001`
- **Underlying Database Tables:** `patients`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Citizen New Registration Screen (SCREEN-011)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/patients/new'
  When user completes operational interaction on screen 'SCREEN-011'
  Then the system persists data to 'API-PAT-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-011' validates state transitions and UI responsiveness
```

---

### SCREEN-012: Citizen Search & Retrieval Screen
**Module:** `MODULE-003` | **Primary Route:** `/patients/search` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Citizen Search & Retrieval Screen` screen (SCREEN-012) provides the user interface for Phonetic Kannada/English search by UHID, phone number, or name. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Medical Officer / General Physician, Staff Nurse / Triage Specialist, Pharmacist / Dispenser
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PAT-002`
- **Underlying Database Tables:** `patients`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Citizen Search & Retrieval Screen (SCREEN-012)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/patients/search'
  When user completes operational interaction on screen 'SCREEN-012'
  Then the system persists data to 'API-PAT-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-012' validates state transitions and UI responsiveness
```

---

### SCREEN-013: Patient Longitudinal Profile View
**Module:** `MODULE-003` | **Primary Route:** `/patients/:id` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Patient Longitudinal Profile View` screen (SCREEN-013) provides the user interface for Unified timeline of past visits, vitals trends, allergies, and diagnoses. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Receptionist / Registration Clerk, Staff Nurse / Triage Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PAT-003`
- **Underlying Database Tables:** `patients, visits, consultations`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Patient Longitudinal Profile View (SCREEN-013)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/patients/:id'
  When user completes operational interaction on screen 'SCREEN-013'
  Then the system persists data to 'API-PAT-003' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-013' validates state transitions and UI responsiveness
```

---

### SCREEN-014: Repeat Patient Fast Intake
**Module:** `MODULE-003` | **Primary Route:** `/patients/:id/repeat-intake` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Repeat Patient Fast Intake` screen (SCREEN-014) provides the user interface for Quick verification of active profile and instant token dispatch. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-VST-001`
- **Underlying Database Tables:** `visits`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Repeat Patient Fast Intake (SCREEN-014)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/patients/:id/repeat-intake'
  When user completes operational interaction on screen 'SCREEN-014'
  Then the system persists data to 'API-VST-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-014' validates state transitions and UI responsiveness
```

---

### SCREEN-015: Biometric & ABHA Card Scan Modal
**Module:** `MODULE-003` | **Primary Route:** `/patients/abha-scan` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Biometric & ABHA Card Scan Modal` screen (SCREEN-015) provides the user interface for ABHA QR code scanning and national grid profile pre-population. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-ABDM-001`
- **Underlying Database Tables:** `patients, abdm_profiles`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Biometric & ABHA Card Scan Modal (SCREEN-015)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/patients/abha-scan'
  When user completes operational interaction on screen 'SCREEN-015'
  Then the system persists data to 'API-ABDM-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-015' validates state transitions and UI responsiveness
```

---

### SCREEN-016: Citizen Demographic Correction Form
**Module:** `MODULE-003` | **Primary Route:** `/patients/:id/edit` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Citizen Demographic Correction Form` screen (SCREEN-016) provides the user interface for Formal profile modification with reason logging and audit trail. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PAT-004`
- **Underlying Database Tables:** `patients, audit_events`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Citizen Demographic Correction Form (SCREEN-016)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/patients/:id/edit'
  When user completes operational interaction on screen 'SCREEN-016'
  Then the system persists data to 'API-PAT-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-016' validates state transitions and UI responsiveness
```

---

### SCREEN-017: Duplicate Citizen Merge Modal
**Module:** `MODULE-003` | **Primary Route:** `/patients/merge` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `Duplicate Citizen Merge Modal` screen (SCREEN-017) provides the user interface for Side-by-side comparison and deduplication with record re-linking. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-006` (Clinic Administrative Officer)
- **Secondary / Supervisory Roles:** Data Protection Officer (DPO)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PAT-005`
- **Underlying Database Tables:** `patients, audit_events`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Duplicate Citizen Merge Modal (SCREEN-017)
  Given user is authenticated with role 'ROLE-006'
  And the active terminal is assigned to route '/patients/merge'
  When user completes operational interaction on screen 'SCREEN-017'
  Then the system persists data to 'API-PAT-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-017' validates state transitions and UI responsiveness
```

---

### SCREEN-018: Citizen Digital Photo Capture
**Module:** `MODULE-003` | **Primary Route:** `/patients/:id/photo` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Citizen Digital Photo Capture` screen (SCREEN-018) provides the user interface for Webcam capture with client-side cropping and privacy masking. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Data Entry Operator
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PAT-006`
- **Underlying Database Tables:** `patients`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Citizen Digital Photo Capture (SCREEN-018)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/patients/:id/photo'
  When user completes operational interaction on screen 'SCREEN-018'
  Then the system persists data to 'API-PAT-006' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-018' validates state transitions and UI responsiveness
```

---

### SCREEN-019: DPDP Informed Consent Capture Screen
**Module:** `MODULE-004` | **Primary Route:** `/patients/:id/consent` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `DPDP Informed Consent Capture Screen` screen (SCREEN-019) provides the user interface for Bilingual purpose selection, digital signature, and guardian declaration. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Medical Officer / General Physician, Staff Nurse / Triage Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PAT-007`
- **Underlying Database Tables:** `patient_consents`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with DPDP Informed Consent Capture Screen (SCREEN-019)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/patients/:id/consent'
  When user completes operational interaction on screen 'SCREEN-019'
  Then the system persists data to 'API-PAT-007' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-019' validates state transitions and UI responsiveness
```

---

### SCREEN-020: Consent History & Revocation Console
**Module:** `MODULE-004` | **Primary Route:** `/patients/:id/consents` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Consent History & Revocation Console` screen (SCREEN-020) provides the user interface for Active consent directives list with instant purpose revocation toggle. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Data Protection Officer (DPO)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PAT-008`
- **Underlying Database Tables:** `patient_consents`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Consent History & Revocation Console (SCREEN-020)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/patients/:id/consents'
  When user completes operational interaction on screen 'SCREEN-020'
  Then the system persists data to 'API-PAT-008' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-020' validates state transitions and UI responsiveness
```

---

### SCREEN-021: Data Portability & Export Request
**Module:** `MODULE-004` | **Primary Route:** `/patients/:id/export` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Data Portability & Export Request` screen (SCREEN-021) provides the user interface for Citizen right to portability: JSON/FHIR/PDF export generation. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Data Protection Officer (DPO)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PORT-001`
- **Underlying Database Tables:** `patient_exports`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Data Portability & Export Request (SCREEN-021)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/patients/:id/export'
  When user completes operational interaction on screen 'SCREEN-021'
  Then the system persists data to 'API-PORT-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-021' validates state transitions and UI responsiveness
```

---

### SCREEN-022: Citizen Grievance Redressal Intake
**Module:** `MODULE-004` | **Primary Route:** `/patients/:id/grievance` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Citizen Grievance Redressal Intake` screen (SCREEN-022) provides the user interface for Formal grievance filing regarding privacy, wait times, or care quality. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Grievance Redressal Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-SYS-002`
- **Underlying Database Tables:** `citizen_grievances`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Citizen Grievance Redressal Intake (SCREEN-022)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/patients/:id/grievance'
  When user completes operational interaction on screen 'SCREEN-022'
  Then the system persists data to 'API-SYS-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-022' validates state transitions and UI responsiveness
```

---

### SCREEN-023: Grievance Investigation & Resolution
**Module:** `MODULE-004` | **Primary Route:** `/grievances/:id` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `Grievance Investigation & Resolution` screen (SCREEN-023) provides the user interface for Investigative review, clinical supervisor remarks, and formal closure. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-021` (Grievance Redressal Officer)
- **Secondary / Supervisory Roles:** Zonal Health Officer (ZHO)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-SYS-003`
- **Underlying Database Tables:** `citizen_grievances`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Grievance Investigation & Resolution (SCREEN-023)
  Given user is authenticated with role 'ROLE-021'
  And the active terminal is assigned to route '/grievances/:id'
  When user completes operational interaction on screen 'SCREEN-023'
  Then the system persists data to 'API-SYS-003' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-023' validates state transitions and UI responsiveness
```

---

### SCREEN-024: OPD Token Generation & Print Modal
**Module:** `MODULE-005` | **Primary Route:** `/queue/tokens/new` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `OPD Token Generation & Print Modal` screen (SCREEN-024) provides the user interface for Department selection, priority tag allocation, and thermal 80mm ticket print. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-VST-002`
- **Underlying Database Tables:** `visits, opd_queues`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with OPD Token Generation & Print Modal (SCREEN-024)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/queue/tokens/new'
  When user completes operational interaction on screen 'SCREEN-024'
  Then the system persists data to 'API-VST-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-024' validates state transitions and UI responsiveness
```

---

### SCREEN-025: Master Waiting Room Queue Display
**Module:** `MODULE-005` | **Primary Route:** `/queue/display` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Master Waiting Room Queue Display` screen (SCREEN-025) provides the user interface for High-contrast public display screen with Kannada audio voice announcements. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist, Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-VST-003`
- **Underlying Database Tables:** `opd_queues`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Master Waiting Room Queue Display (SCREEN-025)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/queue/display'
  When user completes operational interaction on screen 'SCREEN-025'
  Then the system persists data to 'API-VST-003' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-025' validates state transitions and UI responsiveness
```

---

### SCREEN-026: Queue Management & Rerouting Screen
**Module:** `MODULE-005` | **Primary Route:** `/queue/manage` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Queue Management & Rerouting Screen` screen (SCREEN-026) provides the user interface for Queue re-ordering, doctor cabin reassignment, and no-show handling. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-003` (Staff Nurse / Triage Specialist)
- **Secondary / Supervisory Roles:** Receptionist / Registration Clerk, Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-VST-004`
- **Underlying Database Tables:** `opd_queues`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Queue Management & Rerouting Screen (SCREEN-026)
  Given user is authenticated with role 'ROLE-003'
  And the active terminal is assigned to route '/queue/manage'
  When user completes operational interaction on screen 'SCREEN-026'
  Then the system persists data to 'API-VST-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-026' validates state transitions and UI responsiveness
```

---

### SCREEN-027: Express Triage Queue
**Module:** `MODULE-005` | **Primary Route:** `/queue/triage-express` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Express Triage Queue` screen (SCREEN-027) provides the user interface for Filtered intake queue for infants, antenatal mothers, and senior citizens. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-003` (Staff Nurse / Triage Specialist)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-VST-005`
- **Underlying Database Tables:** `opd_queues`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Express Triage Queue (SCREEN-027)
  Given user is authenticated with role 'ROLE-003'
  And the active terminal is assigned to route '/queue/triage-express'
  When user completes operational interaction on screen 'SCREEN-027'
  Then the system persists data to 'API-VST-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-027' validates state transitions and UI responsiveness
```

---

### SCREEN-028: Pharmacy Pickup Waiting Screen
**Module:** `MODULE-005` | **Primary Route:** `/queue/pharmacy` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Pharmacy Pickup Waiting Screen` screen (SCREEN-028) provides the user interface for Live medication assembly queue and citizen token callout. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PHR-002`
- **Underlying Database Tables:** `prescriptions`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Pharmacy Pickup Waiting Screen (SCREEN-028)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/queue/pharmacy'
  When user completes operational interaction on screen 'SCREEN-028'
  Then the system persists data to 'API-PHR-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-028' validates state transitions and UI responsiveness
```

---

### SCREEN-029: Triage Vitals Entry Form
**Module:** `MODULE-006` | **Primary Route:** `/triage/:visitId/vitals` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Triage Vitals Entry Form` screen (SCREEN-029) provides the user interface for BP, Pulse, SpO2, Temperature, Blood Glucose, Height, and Weight capture. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-003` (Staff Nurse / Triage Specialist)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-TRG-002`
- **Underlying Database Tables:** `triage_assessments`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Triage Vitals Entry Form (SCREEN-029)
  Given user is authenticated with role 'ROLE-003'
  And the active terminal is assigned to route '/triage/:visitId/vitals'
  When user completes operational interaction on screen 'SCREEN-029'
  Then the system persists data to 'API-TRG-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-029' validates state transitions and UI responsiveness
```

---

### SCREEN-030: Pediatric Growth Chart & Z-Scores
**Module:** `MODULE-006` | **Primary Route:** `/triage/:visitId/pediatric` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Pediatric Growth Chart & Z-Scores` screen (SCREEN-030) provides the user interface for WHO growth chart plot, percentile calculation, and malnutrition alert. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-003` (Staff Nurse / Triage Specialist)
- **Secondary / Supervisory Roles:** Medical Officer / General Physician
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-TRG-003`
- **Underlying Database Tables:** `triage_assessments`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Pediatric Growth Chart & Z-Scores (SCREEN-030)
  Given user is authenticated with role 'ROLE-003'
  And the active terminal is assigned to route '/triage/:visitId/pediatric'
  When user completes operational interaction on screen 'SCREEN-030'
  Then the system persists data to 'API-TRG-003' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-030' validates state transitions and UI responsiveness
```

---

### SCREEN-031: Antenatal Care (ANC) Vitals Intake
**Module:** `MODULE-006` | **Primary Route:** `/triage/:visitId/anc` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Antenatal Care (ANC) Vitals Intake` screen (SCREEN-031) provides the user interface for Gestational age, fundal height, fetal heart sound, and proteinuria check. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-003` (Staff Nurse / Triage Specialist)
- **Secondary / Supervisory Roles:** ANM / Urban Health Worker
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-TRG-004`
- **Underlying Database Tables:** `triage_assessments`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Antenatal Care (ANC) Vitals Intake (SCREEN-031)
  Given user is authenticated with role 'ROLE-003'
  And the active terminal is assigned to route '/triage/:visitId/anc'
  When user completes operational interaction on screen 'SCREEN-031'
  Then the system persists data to 'API-TRG-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-031' validates state transitions and UI responsiveness
```

---

### SCREEN-032: Danger Signs & Triage Warning Modal
**Module:** `MODULE-006` | **Primary Route:** `/triage/:visitId/danger-modal` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Danger Signs & Triage Warning Modal` screen (SCREEN-032) provides the user interface for Red alert trigger for hypertensive crisis, severe hypoxia, or sepsis. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-003` (Staff Nurse / Triage Specialist)
- **Secondary / Supervisory Roles:** Medical Officer / General Physician
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-TRG-005`
- **Underlying Database Tables:** `triage_assessments, critical_alerts`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Danger Signs & Triage Warning Modal (SCREEN-032)
  Given user is authenticated with role 'ROLE-003'
  And the active terminal is assigned to route '/triage/:visitId/danger-modal'
  When user completes operational interaction on screen 'SCREEN-032'
  Then the system persists data to 'API-TRG-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-032' validates state transitions and UI responsiveness
```

---

### SCREEN-033: Point-of-Care Blood Sugar Entry
**Module:** `MODULE-006` | **Primary Route:** `/triage/:visitId/glucometer` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Point-of-Care Blood Sugar Entry` screen (SCREEN-033) provides the user interface for Fasting, random, or post-prandial blood glucose rapid record. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-003` (Staff Nurse / Triage Specialist)
- **Secondary / Supervisory Roles:** Laboratory Technician
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-TRG-006`
- **Underlying Database Tables:** `triage_assessments`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Point-of-Care Blood Sugar Entry (SCREEN-033)
  Given user is authenticated with role 'ROLE-003'
  And the active terminal is assigned to route '/triage/:visitId/glucometer'
  When user completes operational interaction on screen 'SCREEN-033'
  Then the system persists data to 'API-TRG-006' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-033' validates state transitions and UI responsiveness
```

---

### SCREEN-034: Triage Station History Log
**Module:** `MODULE-006` | **Primary Route:** `/triage/station-history` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Triage Station History Log` screen (SCREEN-034) provides the user interface for Completed triage encounters for the active shift with edit locks. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-003` (Staff Nurse / Triage Specialist)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-TRG-007`
- **Underlying Database Tables:** `triage_assessments`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Triage Station History Log (SCREEN-034)
  Given user is authenticated with role 'ROLE-003'
  And the active terminal is assigned to route '/triage/station-history'
  When user completes operational interaction on screen 'SCREEN-034'
  Then the system persists data to 'API-TRG-007' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-034' validates state transitions and UI responsiveness
```

---

### SCREEN-035: Clinical Consultation Workspace
**Module:** `MODULE-007` | **Primary Route:** `/consultations/:visitId` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Clinical Consultation Workspace` screen (SCREEN-035) provides the user interface for Unified doctor consultation layout: notes, vitals, diagnosis, and prescription. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-CON-002`
- **Underlying Database Tables:** `consultations`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Clinical Consultation Workspace (SCREEN-035)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/consultations/:visitId'
  When user completes operational interaction on screen 'SCREEN-035'
  Then the system persists data to 'API-CON-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-035' validates state transitions and UI responsiveness
```

---

### SCREEN-036: Chief Complaints & Systemic Review
**Module:** `MODULE-007` | **Primary Route:** `/consultations/:visitId/symptoms` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Chief Complaints & Systemic Review` screen (SCREEN-036) provides the user interface for Structured symptoms selector with duration, severity, and Kannada translation. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-CON-003`
- **Underlying Database Tables:** `consultations`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Chief Complaints & Systemic Review (SCREEN-036)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/consultations/:visitId/symptoms'
  When user completes operational interaction on screen 'SCREEN-036'
  Then the system persists data to 'API-CON-003' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-036' validates state transitions and UI responsiveness
```

---

### SCREEN-037: Physical & Clinical Examination Form
**Module:** `MODULE-007` | **Primary Route:** `/consultations/:visitId/exam` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Physical & Clinical Examination Form` screen (SCREEN-037) provides the user interface for General appearance, respiratory, cardiovascular, and abdominal examination. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-CON-004`
- **Underlying Database Tables:** `consultations`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Physical & Clinical Examination Form (SCREEN-037)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/consultations/:visitId/exam'
  When user completes operational interaction on screen 'SCREEN-037'
  Then the system persists data to 'API-CON-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-037' validates state transitions and UI responsiveness
```

---

### SCREEN-038: ICD-10 & SNOMED CT Diagnosis Picker
**Module:** `MODULE-007` | **Primary Route:** `/consultations/:visitId/diagnosis` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `ICD-10 & SNOMED CT Diagnosis Picker` screen (SCREEN-038) provides the user interface for Smart predictive search for primary, secondary, and provisional diagnoses. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-CON-005`
- **Underlying Database Tables:** `consultations`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with ICD-10 & SNOMED CT Diagnosis Picker (SCREEN-038)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/consultations/:visitId/diagnosis'
  When user completes operational interaction on screen 'SCREEN-038'
  Then the system persists data to 'API-CON-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-038' validates state transitions and UI responsiveness
```

---

### SCREEN-039: NCD Chronic Disease Registry Form
**Module:** `MODULE-007` | **Primary Route:** `/consultations/:visitId/ncd` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `NCD Chronic Disease Registry Form` screen (SCREEN-039) provides the user interface for Hypertension, diabetes, COPD, and stroke longitudinal tracking dossier. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-CON-006`
- **Underlying Database Tables:** `consultations, ncd_enrollments`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with NCD Chronic Disease Registry Form (SCREEN-039)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/consultations/:visitId/ncd'
  When user completes operational interaction on screen 'SCREEN-039'
  Then the system persists data to 'API-CON-006' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-039' validates state transitions and UI responsiveness
```

---

### SCREEN-040: Past Medical & Surgical History Modal
**Module:** `MODULE-007` | **Primary Route:** `/consultations/:visitId/history` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Past Medical & Surgical History Modal` screen (SCREEN-040) provides the user interface for Prior hospitalizations, chronic illnesses, and surgical procedures record. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-CON-007`
- **Underlying Database Tables:** `consultations`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Past Medical & Surgical History Modal (SCREEN-040)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/consultations/:visitId/history'
  When user completes operational interaction on screen 'SCREEN-040'
  Then the system persists data to 'API-CON-007' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-040' validates state transitions and UI responsiveness
```

---

### SCREEN-041: Drug Allergy & Adverse Reaction Logger
**Module:** `MODULE-007` | **Primary Route:** `/consultations/:visitId/allergies` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Drug Allergy & Adverse Reaction Logger` screen (SCREEN-041) provides the user interface for Severe penicillin, sulfa, and NSAID allergy register with persistent alert badges. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist, Pharmacist / Dispenser
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-CON-008`
- **Underlying Database Tables:** `patient_allergies`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Drug Allergy & Adverse Reaction Logger (SCREEN-041)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/consultations/:visitId/allergies'
  When user completes operational interaction on screen 'SCREEN-041'
  Then the system persists data to 'API-CON-008' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-041' validates state transitions and UI responsiveness
```

---

### SCREEN-042: Clinical Progress Note & Free-Text Area
**Module:** `MODULE-007` | **Primary Route:** `/consultations/:visitId/notes` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Clinical Progress Note & Free-Text Area` screen (SCREEN-042) provides the user interface for Structured SOAP format note editor with speech-to-text integration. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-CON-009`
- **Underlying Database Tables:** `consultations`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Clinical Progress Note & Free-Text Area (SCREEN-042)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/consultations/:visitId/notes'
  When user completes operational interaction on screen 'SCREEN-042'
  Then the system persists data to 'API-CON-009' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-042' validates state transitions and UI responsiveness
```

---

### SCREEN-043: Doctor Teleconsultation Video Room
**Module:** `MODULE-007` | **Primary Route:** `/consultations/:visitId/teleconsult` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `Doctor Teleconsultation Video Room` screen (SCREEN-043) provides the user interface for WebRTC encrypted video room connecting specialist hospital doctor. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Telemedicine Remote Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-CON-010`
- **Underlying Database Tables:** `consultations`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Doctor Teleconsultation Video Room (SCREEN-043)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/consultations/:visitId/teleconsult'
  When user completes operational interaction on screen 'SCREEN-043'
  Then the system persists data to 'API-CON-010' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-043' validates state transitions and UI responsiveness
```

---

### SCREEN-044: Consultation Summary & Lock Dialog
**Module:** `MODULE-007` | **Primary Route:** `/consultations/:visitId/sign` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Consultation Summary & Lock Dialog` screen (SCREEN-044) provides the user interface for Final review, digital sign-off, and cryptographic sealing of clinical encounter. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-CON-011`
- **Underlying Database Tables:** `consultations, audit_events`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Consultation Summary & Lock Dialog (SCREEN-044)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/consultations/:visitId/sign'
  When user completes operational interaction on screen 'SCREEN-044'
  Then the system persists data to 'API-CON-011' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-044' validates state transitions and UI responsiveness
```

---

### SCREEN-045: Doctor Outpatient Day Book View
**Module:** `MODULE-007` | **Primary Route:** `/doctor/daybook` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Doctor Outpatient Day Book View` screen (SCREEN-045) provides the user interface for Consolidated list of all encounters treated during the shift. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-CON-012`
- **Underlying Database Tables:** `consultations`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Doctor Outpatient Day Book View (SCREEN-045)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/doctor/daybook'
  When user completes operational interaction on screen 'SCREEN-045'
  Then the system persists data to 'API-CON-012' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-045' validates state transitions and UI responsiveness
```

---

### SCREEN-046: Electronic Prescription Form
**Module:** `MODULE-008` | **Primary Route:** `/prescriptions/:consultationId/new` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Electronic Prescription Form` screen (SCREEN-046) provides the user interface for Formulary-filtered drug search, dosage, route, duration, and food timing. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-RX-001`
- **Underlying Database Tables:** `prescriptions, prescription_items`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Electronic Prescription Form (SCREEN-046)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/prescriptions/:consultationId/new'
  When user completes operational interaction on screen 'SCREEN-046'
  Then the system persists data to 'API-RX-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-046' validates state transitions and UI responsiveness
```

---

### SCREEN-047: Drug-Drug & Drug-Allergy Warning Modal
**Module:** `MODULE-008` | **Primary Route:** `/prescriptions/interaction-modal` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Drug-Drug & Drug-Allergy Warning Modal` screen (SCREEN-047) provides the user interface for Real-time clinical safety warning with override justification prompt. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Pharmacist / Dispenser
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-RX-002`
- **Underlying Database Tables:** `prescription_items`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Drug-Drug & Drug-Allergy Warning Modal (SCREEN-047)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/prescriptions/interaction-modal'
  When user completes operational interaction on screen 'SCREEN-047'
  Then the system persists data to 'API-RX-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-047' validates state transitions and UI responsiveness
```

---

### SCREEN-048: Standard Clinical Treatment Regimen Picker
**Module:** `MODULE-008` | **Primary Route:** `/prescriptions/templates` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Standard Clinical Treatment Regimen Picker` screen (SCREEN-048) provides the user interface for Pre-approved clinical templates (URTI, Hypertension Stage 1, Type 2 DM). Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-RX-003`
- **Underlying Database Tables:** `prescription_templates`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Standard Clinical Treatment Regimen Picker (SCREEN-048)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/prescriptions/templates'
  When user completes operational interaction on screen 'SCREEN-048'
  Then the system persists data to 'API-RX-003' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-048' validates state transitions and UI responsiveness
```

---

### SCREEN-049: Prescription Bilingual Print Preview
**Module:** `MODULE-008` | **Primary Route:** `/prescriptions/:id/print` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Prescription Bilingual Print Preview` screen (SCREEN-049) provides the user interface for A4 or A5 printable prescription formatted in Kannada and English with QR code. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Pharmacist / Dispenser
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-RX-004`
- **Underlying Database Tables:** `prescriptions`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Prescription Bilingual Print Preview (SCREEN-049)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/prescriptions/:id/print'
  When user completes operational interaction on screen 'SCREEN-049'
  Then the system persists data to 'API-RX-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-049' validates state transitions and UI responsiveness
```

---

### SCREEN-050: Medication Modification & Cancellation
**Module:** `MODULE-008` | **Primary Route:** `/prescriptions/:id/modify` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Medication Modification & Cancellation` screen (SCREEN-050) provides the user interface for Canceling or substituting un-dispensed prescription items with reason. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-RX-005`
- **Underlying Database Tables:** `prescriptions, prescription_items`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Medication Modification & Cancellation (SCREEN-050)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/prescriptions/:id/modify'
  When user completes operational interaction on screen 'SCREEN-050'
  Then the system persists data to 'API-RX-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-050' validates state transitions and UI responsiveness
```

---

### SCREEN-051: Recurring Refill Request Form
**Module:** `MODULE-008` | **Primary Route:** `/prescriptions/:id/refill` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Recurring Refill Request Form` screen (SCREEN-051) provides the user interface for Chronic medication 30-day refill request for stable NCD citizens. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-RX-006`
- **Underlying Database Tables:** `prescriptions`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Recurring Refill Request Form (SCREEN-051)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/prescriptions/:id/refill'
  When user completes operational interaction on screen 'SCREEN-051'
  Then the system persists data to 'API-RX-006' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-051' validates state transitions and UI responsiveness
```

---

### SCREEN-052: Clinic Formulary & Stock Lookup Modal
**Module:** `MODULE-008` | **Primary Route:** `/formulary/lookup` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Clinic Formulary & Stock Lookup Modal` screen (SCREEN-052) provides the user interface for Real-time verification of in-stock medications at the clinic dispensary. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist, Pharmacist / Dispenser
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-INV-001`
- **Underlying Database Tables:** `pharmacy_batches`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Clinic Formulary & Stock Lookup Modal (SCREEN-052)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/formulary/lookup'
  When user completes operational interaction on screen 'SCREEN-052'
  Then the system persists data to 'API-INV-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-052' validates state transitions and UI responsiveness
```

---

### SCREEN-053: Pharmacy Active Dispensing Screen
**Module:** `MODULE-009` | **Primary Route:** `/pharmacy/dispense/:id` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Pharmacy Active Dispensing Screen` screen (SCREEN-053) provides the user interface for Barcode scanning of medicine strips, batch matching, and counseling checklist. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PHR-003`
- **Underlying Database Tables:** `prescriptions, dispensing_logs`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Pharmacy Active Dispensing Screen (SCREEN-053)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/pharmacy/dispense/:id'
  When user completes operational interaction on screen 'SCREEN-053'
  Then the system persists data to 'API-PHR-003' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-053' validates state transitions and UI responsiveness
```

---

### SCREEN-054: Partial Dispensing & Stockout Dialog
**Module:** `MODULE-009` | **Primary Route:** `/pharmacy/dispense/:id/partial` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Partial Dispensing & Stockout Dialog` screen (SCREEN-054) provides the user interface for Recording partial quantity dispensed with citizen referral to depot. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PHR-004`
- **Underlying Database Tables:** `dispensing_logs`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Partial Dispensing & Stockout Dialog (SCREEN-054)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/pharmacy/dispense/:id/partial'
  When user completes operational interaction on screen 'SCREEN-054'
  Then the system persists data to 'API-PHR-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-054' validates state transitions and UI responsiveness
```

---

### SCREEN-055: Medicine Counseling Label Print Modal
**Module:** `MODULE-009` | **Primary Route:** `/pharmacy/labels/print` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Medicine Counseling Label Print Modal` screen (SCREEN-055) provides the user interface for Adhesive label generation in Kannada for pill bottles and envelopes. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PHR-005`
- **Underlying Database Tables:** `prescriptions`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Medicine Counseling Label Print Modal (SCREEN-055)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/pharmacy/labels/print'
  When user completes operational interaction on screen 'SCREEN-055'
  Then the system persists data to 'API-PHR-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-055' validates state transitions and UI responsiveness
```

---

### SCREEN-056: Pharmacy Shift Reconciliation Form
**Module:** `MODULE-009` | **Primary Route:** `/pharmacy/shift-reconciliation` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Pharmacy Shift Reconciliation Form` screen (SCREEN-056) provides the user interface for Physical count verification against software balance at close of shift. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PHR-006`
- **Underlying Database Tables:** `pharmacy_stock_ledger`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Pharmacy Shift Reconciliation Form (SCREEN-056)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/pharmacy/shift-reconciliation'
  When user completes operational interaction on screen 'SCREEN-056'
  Then the system persists data to 'API-PHR-006' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-056' validates state transitions and UI responsiveness
```

---

### SCREEN-057: Expired & Damaged Drug Quarantine Form
**Module:** `MODULE-009` | **Primary Route:** `/pharmacy/quarantine` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Expired & Damaged Drug Quarantine Form` screen (SCREEN-057) provides the user interface for Isolating expired batches with destruction request and supervisor sign-off. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-INV-002`
- **Underlying Database Tables:** `pharmacy_batches`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Expired & Damaged Drug Quarantine Form (SCREEN-057)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/pharmacy/quarantine'
  When user completes operational interaction on screen 'SCREEN-057'
  Then the system persists data to 'API-INV-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-057' validates state transitions and UI responsiveness
```

---

### SCREEN-058: Emergency Stock Requisition Form
**Module:** `MODULE-009` | **Primary Route:** `/pharmacy/requisitions/new` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Emergency Stock Requisition Form` screen (SCREEN-058) provides the user interface for Urgent stock indent to Zonal Warehouse for depleted essential drugs. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-INV-003`
- **Underlying Database Tables:** `stock_requisitions`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Emergency Stock Requisition Form (SCREEN-058)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/pharmacy/requisitions/new'
  When user completes operational interaction on screen 'SCREEN-058'
  Then the system persists data to 'API-INV-003' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-058' validates state transitions and UI responsiveness
```

---

### SCREEN-059: Pharmacy Dispensing Log History
**Module:** `MODULE-009` | **Primary Route:** `/pharmacy/history` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Pharmacy Dispensing Log History` screen (SCREEN-059) provides the user interface for Audit trail of all dispensed medications sorted by token and timestamp. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** Quality & Compliance Auditor
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PHR-007`
- **Underlying Database Tables:** `dispensing_logs`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Pharmacy Dispensing Log History (SCREEN-059)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/pharmacy/history'
  When user completes operational interaction on screen 'SCREEN-059'
  Then the system persists data to 'API-PHR-007' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-059' validates state transitions and UI responsiveness
```

---

### SCREEN-060: Controlled Substances & High-Alert Register
**Module:** `MODULE-009` | **Primary Route:** `/pharmacy/controlled-register` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `Controlled Substances & High-Alert Register` screen (SCREEN-060) provides the user interface for Dual-signature ledger for sedative, opioid, and emergency injectable vials. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** Clinic Administrative Officer, Quality & Compliance Auditor
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-PHR-008`
- **Underlying Database Tables:** `pharmacy_stock_ledger`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Controlled Substances & High-Alert Register (SCREEN-060)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/pharmacy/controlled-register'
  When user completes operational interaction on screen 'SCREEN-060'
  Then the system persists data to 'API-PHR-008' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-060' validates state transitions and UI responsiveness
```

---

### SCREEN-061: Clinic Stock Inventory Dashboard
**Module:** `MODULE-010` | **Primary Route:** `/inventory` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Clinic Stock Inventory Dashboard` screen (SCREEN-061) provides the user interface for Overview of all 52 essential medicines, current quantities, and days-of-stock. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** Clinic Administrative Officer, Central Depot Inventory Manager
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-INV-004`
- **Underlying Database Tables:** `pharmacy_batches`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Clinic Stock Inventory Dashboard (SCREEN-061)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/inventory'
  When user completes operational interaction on screen 'SCREEN-061'
  Then the system persists data to 'API-INV-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-061' validates state transitions and UI responsiveness
```

---

### SCREEN-062: Stock Goods Receipt Note (GRN) Form
**Module:** `MODULE-010` | **Primary Route:** `/inventory/receipt` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Stock Goods Receipt Note (GRN) Form` screen (SCREEN-062) provides the user interface for Receiving shipments from BBMP Central Depot with batch, expiry, and pack verification. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-INV-005`
- **Underlying Database Tables:** `pharmacy_batches, stock_grn`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Stock Goods Receipt Note (GRN) Form (SCREEN-062)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/inventory/receipt'
  When user completes operational interaction on screen 'SCREEN-062'
  Then the system persists data to 'API-INV-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-062' validates state transitions and UI responsiveness
```

---

### SCREEN-063: Cold Chain Refrigerator Telemetry View
**Module:** `MODULE-010` | **Primary Route:** `/inventory/cold-chain` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Cold Chain Refrigerator Telemetry View` screen (SCREEN-063) provides the user interface for Continuous temperature graph (2°C - 8°C) with real-time breach warning. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** Cold Chain Logistics Technician
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-INV-006`
- **Underlying Database Tables:** `cold_chain_telemetry`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Cold Chain Refrigerator Telemetry View (SCREEN-063)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/inventory/cold-chain'
  When user completes operational interaction on screen 'SCREEN-063'
  Then the system persists data to 'API-INV-006' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-063' validates state transitions and UI responsiveness
```

---

### SCREEN-064: Vaccine Stock & VVM Status Manager
**Module:** `MODULE-010` | **Primary Route:** `/inventory/vaccines` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Vaccine Stock & VVM Status Manager` screen (SCREEN-064) provides the user interface for Vaccine Vial Monitor stage tracking, dilution timestamps, and discard logs. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-003` (Staff Nurse / Triage Specialist)
- **Secondary / Supervisory Roles:** Pharmacist / Dispenser, Cold Chain Logistics Technician
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-INV-007`
- **Underlying Database Tables:** `vaccine_batches`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Vaccine Stock & VVM Status Manager (SCREEN-064)
  Given user is authenticated with role 'ROLE-003'
  And the active terminal is assigned to route '/inventory/vaccines'
  When user completes operational interaction on screen 'SCREEN-064'
  Then the system persists data to 'API-INV-007' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-064' validates state transitions and UI responsiveness
```

---

### SCREEN-065: Inter-Clinic Stock Transfer Dispatch
**Module:** `MODULE-010` | **Primary Route:** `/inventory/transfers/out` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Inter-Clinic Stock Transfer Dispatch` screen (SCREEN-065) provides the user interface for Transferring surplus medicines to nearby Namma Clinic facing stockout. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-INV-008`
- **Underlying Database Tables:** `stock_transfers`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Inter-Clinic Stock Transfer Dispatch (SCREEN-065)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/inventory/transfers/out'
  When user completes operational interaction on screen 'SCREEN-065'
  Then the system persists data to 'API-INV-008' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-065' validates state transitions and UI responsiveness
```

---

### SCREEN-066: Inter-Clinic Stock Transfer Receipt
**Module:** `MODULE-010` | **Primary Route:** `/inventory/transfers/in` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Inter-Clinic Stock Transfer Receipt` screen (SCREEN-066) provides the user interface for Acceptance and verification of incoming peer clinic transfer batches. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-INV-009`
- **Underlying Database Tables:** `stock_transfers`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Inter-Clinic Stock Transfer Receipt (SCREEN-066)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/inventory/transfers/in'
  When user completes operational interaction on screen 'SCREEN-066'
  Then the system persists data to 'API-INV-009' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-066' validates state transitions and UI responsiveness
```

---

### SCREEN-067: Annual / Monthly Physical Audit Form
**Module:** `MODULE-010` | **Primary Route:** `/inventory/audit` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `Annual / Monthly Physical Audit Form` screen (SCREEN-067) provides the user interface for Stock take worksheet, variance calculation, and shrinkage reporting. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-006` (Clinic Administrative Officer)
- **Secondary / Supervisory Roles:** Quality & Compliance Auditor
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-INV-010`
- **Underlying Database Tables:** `inventory_audits`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Annual / Monthly Physical Audit Form (SCREEN-067)
  Given user is authenticated with role 'ROLE-006'
  And the active terminal is assigned to route '/inventory/audit'
  When user completes operational interaction on screen 'SCREEN-067'
  Then the system persists data to 'API-INV-010' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-067' validates state transitions and UI responsiveness
```

---

### SCREEN-068: Supplier Recall & Ban Notification Modal
**Module:** `MODULE-010` | **Primary Route:** `/inventory/recalls` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Supplier Recall & Ban Notification Modal` screen (SCREEN-068) provides the user interface for Instant alert freezing recalled manufacturer batch codes across all dispensary shelves. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-INV-011`
- **Underlying Database Tables:** `pharmacy_batches`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Supplier Recall & Ban Notification Modal (SCREEN-068)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/inventory/recalls'
  When user completes operational interaction on screen 'SCREEN-068'
  Then the system persists data to 'API-INV-011' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-068' validates state transitions and UI responsiveness
```

---

### SCREEN-069: Diagnostic Lab Test Orders Queue
**Module:** `MODULE-011` | **Primary Route:** `/lab/orders` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Diagnostic Lab Test Orders Queue` screen (SCREEN-069) provides the user interface for Incoming lab requisitions from doctor consultations awaiting specimen draw. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-005` (Laboratory Technician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-LAB-002`
- **Underlying Database Tables:** `lab_orders`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Diagnostic Lab Test Orders Queue (SCREEN-069)
  Given user is authenticated with role 'ROLE-005'
  And the active terminal is assigned to route '/lab/orders'
  When user completes operational interaction on screen 'SCREEN-069'
  Then the system persists data to 'API-LAB-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-069' validates state transitions and UI responsiveness
```

---

### SCREEN-070: Specimen Collection & Barcode Label Screen
**Module:** `MODULE-011` | **Primary Route:** `/lab/specimen/:id` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Specimen Collection & Barcode Label Screen` screen (SCREEN-070) provides the user interface for Phlebotomy collection timestamp, vial barcode generation, and specimen verification. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-005` (Laboratory Technician)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-LAB-003`
- **Underlying Database Tables:** `lab_specimens`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Specimen Collection & Barcode Label Screen (SCREEN-070)
  Given user is authenticated with role 'ROLE-005'
  And the active terminal is assigned to route '/lab/specimen/:id'
  When user completes operational interaction on screen 'SCREEN-070'
  Then the system persists data to 'API-LAB-003' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-070' validates state transitions and UI responsiveness
```

---

### SCREEN-071: Point-of-Care Rapid Test Result Entry
**Module:** `MODULE-011` | **Primary Route:** `/lab/results/poc/:id` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Point-of-Care Rapid Test Result Entry` screen (SCREEN-071) provides the user interface for Rapid Dengue, Malaria, HIV, Pregnancy, and Urine Dipstick result form. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-005` (Laboratory Technician)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-LAB-004`
- **Underlying Database Tables:** `lab_results`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Point-of-Care Rapid Test Result Entry (SCREEN-071)
  Given user is authenticated with role 'ROLE-005'
  And the active terminal is assigned to route '/lab/results/poc/:id'
  When user completes operational interaction on screen 'SCREEN-071'
  Then the system persists data to 'API-LAB-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-071' validates state transitions and UI responsiveness
```

---

### SCREEN-072: Hematology Analyzer Data Import Screen
**Module:** `MODULE-011` | **Primary Route:** `/lab/analyzers/import` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Hematology Analyzer Data Import Screen` screen (SCREEN-072) provides the user interface for Automated serial/USB parsing of CBC machine output into patient record. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-005` (Laboratory Technician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-LAB-005`
- **Underlying Database Tables:** `lab_results`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Hematology Analyzer Data Import Screen (SCREEN-072)
  Given user is authenticated with role 'ROLE-005'
  And the active terminal is assigned to route '/lab/analyzers/import'
  When user completes operational interaction on screen 'SCREEN-072'
  Then the system persists data to 'API-LAB-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-072' validates state transitions and UI responsiveness
```

---

### SCREEN-073: Lab Results Validation & Doctor Alert
**Module:** `MODULE-011` | **Primary Route:** `/lab/results/validate/:id` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Lab Results Validation & Doctor Alert` screen (SCREEN-073) provides the user interface for Panic value flag (e.g. Potassium < 2.5, Hemoglobin < 6.0) triggering doctor notification. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-005` (Laboratory Technician)
- **Secondary / Supervisory Roles:** Medical Officer / General Physician
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-LAB-006`
- **Underlying Database Tables:** `lab_results, critical_alerts`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Lab Results Validation & Doctor Alert (SCREEN-073)
  Given user is authenticated with role 'ROLE-005'
  And the active terminal is assigned to route '/lab/results/validate/:id'
  When user completes operational interaction on screen 'SCREEN-073'
  Then the system persists data to 'API-LAB-006' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-073' validates state transitions and UI responsiveness
```

---

### SCREEN-074: Diagnostic Report Bilingual Print Preview
**Module:** `MODULE-011` | **Primary Route:** `/lab/reports/:id/print` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Diagnostic Report Bilingual Print Preview` screen (SCREEN-074) provides the user interface for Standard A4 laboratory investigation report in Kannada and English. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-005` (Laboratory Technician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-LAB-007`
- **Underlying Database Tables:** `lab_results`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Diagnostic Report Bilingual Print Preview (SCREEN-074)
  Given user is authenticated with role 'ROLE-005'
  And the active terminal is assigned to route '/lab/reports/:id/print'
  When user completes operational interaction on screen 'SCREEN-074'
  Then the system persists data to 'API-LAB-007' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-074' validates state transitions and UI responsiveness
```

---

### SCREEN-075: External Referral Lab Dispatch Form
**Module:** `MODULE-011` | **Primary Route:** `/lab/referrals/out` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `External Referral Lab Dispatch Form` screen (SCREEN-075) provides the user interface for Packaging specialized samples for referral to KC General or Bowring Hospital. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-005` (Laboratory Technician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-LAB-008`
- **Underlying Database Tables:** `lab_orders`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with External Referral Lab Dispatch Form (SCREEN-075)
  Given user is authenticated with role 'ROLE-005'
  And the active terminal is assigned to route '/lab/referrals/out'
  When user completes operational interaction on screen 'SCREEN-075'
  Then the system persists data to 'API-LAB-008' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-075' validates state transitions and UI responsiveness
```

---

### SCREEN-076: Lab Reagent & Quality Control Log
**Module:** `MODULE-011` | **Primary Route:** `/lab/qc` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Lab Reagent & Quality Control Log` screen (SCREEN-076) provides the user interface for Daily calibration check and control vial lot logging before clinical testing. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-005` (Laboratory Technician)
- **Secondary / Supervisory Roles:** Quality & Compliance Auditor
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-LAB-009`
- **Underlying Database Tables:** `lab_qc_logs`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Lab Reagent & Quality Control Log (SCREEN-076)
  Given user is authenticated with role 'ROLE-005'
  And the active terminal is assigned to route '/lab/qc'
  When user completes operational interaction on screen 'SCREEN-076'
  Then the system persists data to 'API-LAB-009' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-076' validates state transitions and UI responsiveness
```

---

### SCREEN-077: Secondary / Tertiary Referral Form
**Module:** `MODULE-012` | **Primary Route:** `/referrals/new` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Secondary / Tertiary Referral Form` screen (SCREEN-077) provides the user interface for Clinical rationale, priority tier, destination hospital selection, and transport mode. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-REF-001`
- **Underlying Database Tables:** `patient_referrals`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Secondary / Tertiary Referral Form (SCREEN-077)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/referrals/new'
  When user completes operational interaction on screen 'SCREEN-077'
  Then the system persists data to 'API-REF-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-077' validates state transitions and UI responsiveness
```

---

### SCREEN-078: 108 Emergency Ambulance Dispatch Screen
**Module:** `MODULE-012` | **Primary Route:** `/referrals/ambulance-108` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `108 Emergency Ambulance Dispatch Screen` screen (SCREEN-078) provides the user interface for Urgent integration bridge calling 108 GVK-EMRI emergency ambulance with live GPS tracking. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist, Receptionist / Registration Clerk
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-REF-002`
- **Underlying Database Tables:** `patient_referrals, ambulance_dispatches`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with 108 Emergency Ambulance Dispatch Screen (SCREEN-078)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/referrals/ambulance-108'
  When user completes operational interaction on screen 'SCREEN-078'
  Then the system persists data to 'API-REF-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-078' validates state transitions and UI responsiveness
```

---

### SCREEN-079: Referral Handover Dossier Print Preview
**Module:** `MODULE-012` | **Primary Route:** `/referrals/:id/print` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Referral Handover Dossier Print Preview` screen (SCREEN-079) provides the user interface for Comprehensive A4 clinical handover slip with vitals summary, ECG, and medications given. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-REF-003`
- **Underlying Database Tables:** `patient_referrals`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Referral Handover Dossier Print Preview (SCREEN-079)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/referrals/:id/print'
  When user completes operational interaction on screen 'SCREEN-079'
  Then the system persists data to 'API-REF-003' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-079' validates state transitions and UI responsiveness
```

---

### SCREEN-080: Active Outgoing Referrals Tracker
**Module:** `MODULE-012` | **Primary Route:** `/referrals/tracking` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Active Outgoing Referrals Tracker` screen (SCREEN-080) provides the user interface for Status dashboard tracking whether referred patients arrived at tertiary hospital. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-003` (Staff Nurse / Triage Specialist)
- **Secondary / Supervisory Roles:** Medical Officer / General Physician, Ward Health Supervisor
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-REF-004`
- **Underlying Database Tables:** `patient_referrals`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Active Outgoing Referrals Tracker (SCREEN-080)
  Given user is authenticated with role 'ROLE-003'
  And the active terminal is assigned to route '/referrals/tracking'
  When user completes operational interaction on screen 'SCREEN-080'
  Then the system persists data to 'API-REF-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-080' validates state transitions and UI responsiveness
```

---

### SCREEN-081: Discharge / Counter-Referral Ingest Form
**Module:** `MODULE-012` | **Primary Route:** `/referrals/counter-referral` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Discharge / Counter-Referral Ingest Form` screen (SCREEN-081) provides the user interface for Recording return of citizen after tertiary care with continued local care plan. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-REF-005`
- **Underlying Database Tables:** `patient_referrals`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Discharge / Counter-Referral Ingest Form (SCREEN-081)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/referrals/counter-referral'
  When user completes operational interaction on screen 'SCREEN-081'
  Then the system persists data to 'API-REF-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-081' validates state transitions and UI responsiveness
```

---

### SCREEN-082: Emergency Resuscitation Incident Record
**Module:** `MODULE-012` | **Primary Route:** `/referrals/resuscitation` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Emergency Resuscitation Incident Record` screen (SCREEN-082) provides the user interface for Clinical documentation of in-clinic CPR, oxygen delivery, and emergency drugs. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-REF-006`
- **Underlying Database Tables:** `consultations, audit_events`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Emergency Resuscitation Incident Record (SCREEN-082)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/referrals/resuscitation'
  When user completes operational interaction on screen 'SCREEN-082'
  Then the system persists data to 'API-REF-006' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-082' validates state transitions and UI responsiveness
```

---

### SCREEN-083: Citizen SMS & Communication Center
**Module:** `MODULE-013` | **Primary Route:** `/notifications/sms-center` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Citizen SMS & Communication Center` screen (SCREEN-083) provides the user interface for Bilingual SMS notification history for appointment reminders and test ready alerts. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist, Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-NOTIF-001`
- **Underlying Database Tables:** `notification_logs`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Citizen SMS & Communication Center (SCREEN-083)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/notifications/sms-center'
  When user completes operational interaction on screen 'SCREEN-083'
  Then the system persists data to 'API-NOTIF-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-083' validates state transitions and UI responsiveness
```

---

### SCREEN-084: Chronic Disease Follow-Up Schedule
**Module:** `MODULE-013` | **Primary Route:** `/followup/schedule` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Chronic Disease Follow-Up Schedule` screen (SCREEN-084) provides the user interface for Monthly roster of diabetic and hypertensive citizens due for routine clinic visit. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-003` (Staff Nurse / Triage Specialist)
- **Secondary / Supervisory Roles:** ANM / Urban Health Worker, ASHA Link Worker Coordinator
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-NOTIF-002`
- **Underlying Database Tables:** `followup_schedules`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Chronic Disease Follow-Up Schedule (SCREEN-084)
  Given user is authenticated with role 'ROLE-003'
  And the active terminal is assigned to route '/followup/schedule'
  When user completes operational interaction on screen 'SCREEN-084'
  Then the system persists data to 'API-NOTIF-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-084' validates state transitions and UI responsiveness
```

---

### SCREEN-085: ASHA Worker Community Outreach Tasklist
**Module:** `MODULE-013` | **Primary Route:** `/followup/asha-tasks` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `ASHA Worker Community Outreach Tasklist` screen (SCREEN-085) provides the user interface for Home visit list for un-immunized infants and missed follow-up citizens. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-019` (ASHA Link Worker Coordinator)
- **Secondary / Supervisory Roles:** ANM / Urban Health Worker
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-NOTIF-003`
- **Underlying Database Tables:** `followup_schedules`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with ASHA Worker Community Outreach Tasklist (SCREEN-085)
  Given user is authenticated with role 'ROLE-019'
  And the active terminal is assigned to route '/followup/asha-tasks'
  When user completes operational interaction on screen 'SCREEN-085'
  Then the system persists data to 'API-NOTIF-003' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-085' validates state transitions and UI responsiveness
```

---

### SCREEN-086: Public Health Broadcast Composer
**Module:** `MODULE-013` | **Primary Route:** `/notifications/broadcasts` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `Public Health Broadcast Composer` screen (SCREEN-086) provides the user interface for Ward-level health advisory broadcast (e.g. Dengue prevention, vaccination drive). Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-008` (Zonal Health Officer (ZHO))
- **Secondary / Supervisory Roles:** Chief Health Officer (CHO)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-NOTIF-004`
- **Underlying Database Tables:** `notification_logs`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Public Health Broadcast Composer (SCREEN-086)
  Given user is authenticated with role 'ROLE-008'
  And the active terminal is assigned to route '/notifications/broadcasts'
  When user completes operational interaction on screen 'SCREEN-086'
  Then the system persists data to 'API-NOTIF-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-086' validates state transitions and UI responsiveness
```

---

### SCREEN-087: Adverse Event Notification Form
**Module:** `MODULE-013` | **Primary Route:** `/notifications/adverse-events` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Adverse Event Notification Form` screen (SCREEN-087) provides the user interface for Reporting adverse events following immunization (AEFI) or drug reaction to BBMP. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** Staff Nurse / Triage Specialist, Pharmacist / Dispenser
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-NOTIF-005`
- **Underlying Database Tables:** `adverse_events`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Adverse Event Notification Form (SCREEN-087)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/notifications/adverse-events'
  When user completes operational interaction on screen 'SCREEN-087'
  Then the system persists data to 'API-NOTIF-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-087' validates state transitions and UI responsiveness
```

---

### SCREEN-088: Missed Follow-up Outreach Dialer Console
**Module:** `MODULE-013` | **Primary Route:** `/followup/dialer` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `Missed Follow-up Outreach Dialer Console` screen (SCREEN-088) provides the user interface for Click-to-call console for calling citizens who missed critical follow-up dates. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** Data Entry Operator
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-NOTIF-006`
- **Underlying Database Tables:** `followup_schedules`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Missed Follow-up Outreach Dialer Console (SCREEN-088)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/followup/dialer'
  When user completes operational interaction on screen 'SCREEN-088'
  Then the system persists data to 'API-NOTIF-006' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-088' validates state transitions and UI responsiveness
```

---

### SCREEN-089: Epidemic Outbreak Surveillance Dashboard
**Module:** `MODULE-014` | **Primary Route:** `/analytics/surveillance` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Epidemic Outbreak Surveillance Dashboard` screen (SCREEN-089) provides the user interface for Spatiotemporal clustering of fever, diarrhea, and jaundice cases across 183 clinics. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-010` (Epidemiologist / Disease Surveillance Officer)
- **Secondary / Supervisory Roles:** Zonal Health Officer (ZHO), Chief Health Officer (CHO)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-ANL-002`
- **Underlying Database Tables:** `epidemic_signals`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Epidemic Outbreak Surveillance Dashboard (SCREEN-089)
  Given user is authenticated with role 'ROLE-010'
  And the active terminal is assigned to route '/analytics/surveillance'
  When user completes operational interaction on screen 'SCREEN-089'
  Then the system persists data to 'API-ANL-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-089' validates state transitions and UI responsiveness
```

---

### SCREEN-090: Ward Health Performance & KPI Scorecard
**Module:** `MODULE-014` | **Primary Route:** `/analytics/ward-kpi` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Ward Health Performance & KPI Scorecard` screen (SCREEN-090) provides the user interface for Outpatient throughput, average wait times, antibiotic prescription ratios. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-007` (Ward Health Supervisor)
- **Secondary / Supervisory Roles:** Zonal Health Officer (ZHO)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-ANL-003`
- **Underlying Database Tables:** `analytics_aggregates`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Ward Health Performance & KPI Scorecard (SCREEN-090)
  Given user is authenticated with role 'ROLE-007'
  And the active terminal is assigned to route '/analytics/ward-kpi'
  When user completes operational interaction on screen 'SCREEN-090'
  Then the system persists data to 'API-ANL-003' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-090' validates state transitions and UI responsiveness
```

---

### SCREEN-091: Pharmacy Dispensing & Consumption Analytics
**Module:** `MODULE-014` | **Primary Route:** `/analytics/drug-utilization` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Pharmacy Dispensing & Consumption Analytics` screen (SCREEN-091) provides the user interface for Top 20 dispensed drugs, antibiotic stewardship compliance, and stockout frequency. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-004` (Pharmacist / Dispenser)
- **Secondary / Supervisory Roles:** Central Depot Inventory Manager, Procurement & Vendor Manager
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-ANL-004`
- **Underlying Database Tables:** `analytics_aggregates`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Pharmacy Dispensing & Consumption Analytics (SCREEN-091)
  Given user is authenticated with role 'ROLE-004'
  And the active terminal is assigned to route '/analytics/drug-utilization'
  When user completes operational interaction on screen 'SCREEN-091'
  Then the system persists data to 'API-ANL-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-091' validates state transitions and UI responsiveness
```

---

### SCREEN-092: Laboratory Diagnostic Workload Dashboard
**Module:** `MODULE-014` | **Primary Route:** `/analytics/lab-metrics` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Laboratory Diagnostic Workload Dashboard` screen (SCREEN-092) provides the user interface for Daily test counts, positivity rates for endemic diseases, and turnaround time. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-005` (Laboratory Technician)
- **Secondary / Supervisory Roles:** Radiologist / Diagnostic Specialist
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-ANL-005`
- **Underlying Database Tables:** `analytics_aggregates`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Laboratory Diagnostic Workload Dashboard (SCREEN-092)
  Given user is authenticated with role 'ROLE-005'
  And the active terminal is assigned to route '/analytics/lab-metrics'
  When user completes operational interaction on screen 'SCREEN-092'
  Then the system persists data to 'API-ANL-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-092' validates state transitions and UI responsiveness
```

---

### SCREEN-093: Maternal & Child Health Coverage Heatmap
**Module:** `MODULE-014` | **Primary Route:** `/analytics/mch-coverage` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Maternal & Child Health Coverage Heatmap` screen (SCREEN-093) provides the user interface for Immunization completion percentage and ANC 4-visit coverage by municipal ward. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-008` (Zonal Health Officer (ZHO))
- **Secondary / Supervisory Roles:** ANM / Urban Health Worker
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-ANL-006`
- **Underlying Database Tables:** `analytics_aggregates`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Maternal & Child Health Coverage Heatmap (SCREEN-093)
  Given user is authenticated with role 'ROLE-008'
  And the active terminal is assigned to route '/analytics/mch-coverage'
  When user completes operational interaction on screen 'SCREEN-093'
  Then the system persists data to 'API-ANL-006' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-093' validates state transitions and UI responsiveness
```

---

### SCREEN-094: Custom Report Builder & CSV Export
**Module:** `MODULE-014` | **Primary Route:** `/analytics/custom-reports` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `Custom Report Builder & CSV Export` screen (SCREEN-094) provides the user interface for Ad-hoc query builder with anonymized data export controls. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-006` (Clinic Administrative Officer)
- **Secondary / Supervisory Roles:** Zonal Health Officer (ZHO), Quality & Compliance Auditor
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-ANL-007`
- **Underlying Database Tables:** `analytics_aggregates`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Custom Report Builder & CSV Export (SCREEN-094)
  Given user is authenticated with role 'ROLE-006'
  And the active terminal is assigned to route '/analytics/custom-reports'
  When user completes operational interaction on screen 'SCREEN-094'
  Then the system persists data to 'API-ANL-007' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-094' validates state transitions and UI responsiveness
```

---

### SCREEN-095: Offline Storage & SQLite WAL Status
**Module:** `MODULE-015` | **Primary Route:** `/system/offline-storage` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Offline Storage & SQLite WAL Status` screen (SCREEN-095) provides the user interface for Local disk capacity, Dexie / IndexedDB record count, and WAL file health. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-006` (Clinic Administrative Officer)
- **Secondary / Supervisory Roles:** IT Support & Hardware Engineer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-SYS-004`
- **Underlying Database Tables:** `sync_queue`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Offline Storage & SQLite WAL Status (SCREEN-095)
  Given user is authenticated with role 'ROLE-006'
  And the active terminal is assigned to route '/system/offline-storage'
  When user completes operational interaction on screen 'SCREEN-095'
  Then the system persists data to 'API-SYS-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-095' validates state transitions and UI responsiveness
```

---

### SCREEN-096: Sync Queue Monitor & Manual Flush
**Module:** `MODULE-015` | **Primary Route:** `/system/sync-queue` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Sync Queue Monitor & Manual Flush` screen (SCREEN-096) provides the user interface for Pending mutations queue, retry backoff counter, and immediate sync trigger. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-006` (Clinic Administrative Officer)
- **Secondary / Supervisory Roles:** IT Support & Hardware Engineer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-SYS-005`
- **Underlying Database Tables:** `sync_queue`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Sync Queue Monitor & Manual Flush (SCREEN-096)
  Given user is authenticated with role 'ROLE-006'
  And the active terminal is assigned to route '/system/sync-queue'
  When user completes operational interaction on screen 'SCREEN-096'
  Then the system persists data to 'API-SYS-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-096' validates state transitions and UI responsiveness
```

---

### SCREEN-097: Sync Conflict Visual Resolution Modal
**Module:** `MODULE-015` | **Primary Route:** `/system/conflicts/:id` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Sync Conflict Visual Resolution Modal` screen (SCREEN-097) provides the user interface for Side-by-side diff between local edge record and central cloud record with merge. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-006` (Clinic Administrative Officer)
- **Secondary / Supervisory Roles:** Medical Officer / General Physician
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-SYS-006`
- **Underlying Database Tables:** `sync_conflicts`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Sync Conflict Visual Resolution Modal (SCREEN-097)
  Given user is authenticated with role 'ROLE-006'
  And the active terminal is assigned to route '/system/conflicts/:id'
  When user completes operational interaction on screen 'SCREEN-097'
  Then the system persists data to 'API-SYS-006' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-097' validates state transitions and UI responsiveness
```

---

### SCREEN-098: Peer-to-Peer Local WiFi Sync Setup
**Module:** `MODULE-015` | **Primary Route:** `/system/p2p-sync` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Peer-to-Peer Local WiFi Sync Setup` screen (SCREEN-098) provides the user interface for Configuring mDNS local edge mini-server sync across clinic tablets during WAN outage. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-024` (IT Support & Hardware Engineer)
- **Secondary / Supervisory Roles:** Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-SYS-007`
- **Underlying Database Tables:** `system_configs`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Peer-to-Peer Local WiFi Sync Setup (SCREEN-098)
  Given user is authenticated with role 'ROLE-024'
  And the active terminal is assigned to route '/system/p2p-sync'
  When user completes operational interaction on screen 'SCREEN-098'
  Then the system persists data to 'API-SYS-007' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-098' validates state transitions and UI responsiveness
```

---

### SCREEN-099: Offline Cryptographic Token Cache
**Module:** `MODULE-015` | **Primary Route:** `/system/offline-auth` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Offline Cryptographic Token Cache` screen (SCREEN-099) provides the user interface for Encrypted local SQLite credentials cache enabling 72-hour offline clinician login. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-006` (Clinic Administrative Officer)
- **Secondary / Supervisory Roles:** Security Administrator / CISO
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-AUTH-006`
- **Underlying Database Tables:** `auth_offline_credentials`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Offline Cryptographic Token Cache (SCREEN-099)
  Given user is authenticated with role 'ROLE-006'
  And the active terminal is assigned to route '/system/offline-auth'
  When user completes operational interaction on screen 'SCREEN-099'
  Then the system persists data to 'API-AUTH-006' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-099' validates state transitions and UI responsiveness
```

---

### SCREEN-100: Local Backup & USB Snapshot Export
**Module:** `MODULE-015` | **Primary Route:** `/system/local-backup` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Local Backup & USB Snapshot Export` screen (SCREEN-100) provides the user interface for Encrypted AES-256 SQLite database dump to approved municipal USB token. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-006` (Clinic Administrative Officer)
- **Secondary / Supervisory Roles:** IT Support & Hardware Engineer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-SYS-008`
- **Underlying Database Tables:** `system_backups`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Local Backup & USB Snapshot Export (SCREEN-100)
  Given user is authenticated with role 'ROLE-006'
  And the active terminal is assigned to route '/system/local-backup'
  When user completes operational interaction on screen 'SCREEN-100'
  Then the system persists data to 'API-SYS-008' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-100' validates state transitions and UI responsiveness
```

---

### SCREEN-101: ABHA Creation & Mobile Verification
**Module:** `MODULE-016` | **Primary Route:** `/abdm/abha-create` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `ABHA Creation & Mobile Verification` screen (SCREEN-101) provides the user interface for Aadhaar OTP or mobile demographic creation of 14-digit ABHA number. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-001` (Receptionist / Registration Clerk)
- **Secondary / Supervisory Roles:** ABDM National Integration Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-ABDM-002`
- **Underlying Database Tables:** `abdm_profiles`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with ABHA Creation & Mobile Verification (SCREEN-101)
  Given user is authenticated with role 'ROLE-001'
  And the active terminal is assigned to route '/abdm/abha-create'
  When user completes operational interaction on screen 'SCREEN-101'
  Then the system persists data to 'API-ABDM-002' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-101' validates state transitions and UI responsiveness
```

---

### SCREEN-102: ABDM Consent Request & Artifact Drawer
**Module:** `MODULE-016` | **Primary Route:** `/abdm/consent-requests` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `ABDM Consent Request & Artifact Drawer` screen (SCREEN-102) provides the user interface for Reviewing citizen consent granted via Aarogya Setu / ABHA app for record fetch. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** ABDM National Integration Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-ABDM-003`
- **Underlying Database Tables:** `abdm_consents`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with ABDM Consent Request & Artifact Drawer (SCREEN-102)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/abdm/consent-requests'
  When user completes operational interaction on screen 'SCREEN-102'
  Then the system persists data to 'API-ABDM-003' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-102' validates state transitions and UI responsiveness
```

---

### SCREEN-103: FHIR R4 Health Data Push Monitor
**Module:** `MODULE-016` | **Primary Route:** `/abdm/fhir-push` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `FHIR R4 Health Data Push Monitor` screen (SCREEN-103) provides the user interface for Status of OPD bundles dispatched to national Health Information Exchange (HIE). Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-022` (ABDM National Integration Officer)
- **Secondary / Supervisory Roles:** Clinic Administrative Officer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-ABDM-004`
- **Underlying Database Tables:** `abdm_transactions`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with FHIR R4 Health Data Push Monitor (SCREEN-103)
  Given user is authenticated with role 'ROLE-022'
  And the active terminal is assigned to route '/abdm/fhir-push'
  When user completes operational interaction on screen 'SCREEN-103'
  Then the system persists data to 'API-ABDM-004' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-103' validates state transitions and UI responsiveness
```

---

### SCREEN-104: External Hospital Records Viewer
**Module:** `MODULE-016` | **Primary Route:** `/abdm/external-records/:uhid` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `External Hospital Records Viewer` screen (SCREEN-104) provides the user interface for Viewing clinical records pulled from external tertiary hospitals via ABDM gateway. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-002` (Medical Officer / General Physician)
- **Secondary / Supervisory Roles:** None (Exclusive Role)
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-ABDM-005`
- **Underlying Database Tables:** `abdm_records`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with External Hospital Records Viewer (SCREEN-104)
  Given user is authenticated with role 'ROLE-002'
  And the active terminal is assigned to route '/abdm/external-records/:uhid'
  When user completes operational interaction on screen 'SCREEN-104'
  Then the system persists data to 'API-ABDM-005' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-104' validates state transitions and UI responsiveness
```

---

### SCREEN-105: Cryptographic WORM Audit Log Viewer
**Module:** `MODULE-017` | **Primary Route:** `/audit/logs` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Cryptographic WORM Audit Log Viewer` screen (SCREEN-105) provides the user interface for Tamper-evident HMAC block viewer with filter by actor, facility, and event code. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-011` (Quality & Compliance Auditor)
- **Secondary / Supervisory Roles:** Security Administrator / CISO, Super Administrator
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-AUD-001`
- **Underlying Database Tables:** `audit_events`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Cryptographic WORM Audit Log Viewer (SCREEN-105)
  Given user is authenticated with role 'ROLE-011'
  And the active terminal is assigned to route '/audit/logs'
  When user completes operational interaction on screen 'SCREEN-105'
  Then the system persists data to 'API-AUD-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-105' validates state transitions and UI responsiveness
```

---

### SCREEN-106: Security Incident & Intrusion Alert Board
**Module:** `MODULE-017` | **Primary Route:** `/security/alerts` | **Offline Mode:** `Degraded Offline`

#### 1. Functional Purpose & Clinical Context
The `Security Incident & Intrusion Alert Board` screen (SCREEN-106) provides the user interface for Brute-force login alerts, rate limit violations, and certificate expiry warnings. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-012` (Security Administrator / CISO)
- **Secondary / Supervisory Roles:** Super Administrator
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Degraded Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-SEC-001`
- **Underlying Database Tables:** `security_incidents`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Security Incident & Intrusion Alert Board (SCREEN-106)
  Given user is authenticated with role 'ROLE-012'
  And the active terminal is assigned to route '/security/alerts'
  When user completes operational interaction on screen 'SCREEN-106'
  Then the system persists data to 'API-SEC-001' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-106' validates state transitions and UI responsiveness
```

---

### SCREEN-107: User Management & Role Assignment
**Module:** `MODULE-017` | **Primary Route:** `/admin/users` | **Offline Mode:** `Online Only`

#### 1. Functional Purpose & Clinical Context
The `User Management & Role Assignment` screen (SCREEN-107) provides the user interface for Staff onboarding, role assignment, active clinic allocation, and account deactivation. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-006` (Clinic Administrative Officer)
- **Secondary / Supervisory Roles:** Super Administrator
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Online Only`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-AUTH-007`
- **Underlying Database Tables:** `auth_users`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with User Management & Role Assignment (SCREEN-107)
  Given user is authenticated with role 'ROLE-006'
  And the active terminal is assigned to route '/admin/users'
  When user completes operational interaction on screen 'SCREEN-107'
  Then the system persists data to 'API-AUTH-007' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-107' validates state transitions and UI responsiveness
```

---

### SCREEN-108: Clinic Master Settings & Hardware Registry
**Module:** `MODULE-017` | **Primary Route:** `/admin/settings` | **Offline Mode:** `Full Offline`

#### 1. Functional Purpose & Clinical Context
The `Clinic Master Settings & Hardware Registry` screen (SCREEN-108) provides the user interface for Facility name, ward code, thermal printer IP, and barcode scanner baud rate config. Designed to optimize frontline healthcare delivery in BBMP municipal clinics, it minimizes latency and cognitive overhead while adhering to state healthcare data governance standards.

#### 2. Role Entitlements & Access Controls
- **Primary Operating Role:** `ROLE-006` (Clinic Administrative Officer)
- **Secondary / Supervisory Roles:** IT Support & Hardware Engineer
- **Deny-by-Default Policy:** Any user session lacking verified cryptographic RBAC claims for this route is redirected to `/dashboard` with an unauthorized alert toast.

#### 3. Entry & Exit Conditions
- **Entry Conditions:** Active authenticated JWT session, verified hardware terminal binding, and active clinic shift.
- **Exit Conditions:** Successful transaction persistence, cancel/discard action with dirty-form confirmation, or session expiration.

#### 4. UI Layout, Core Primitives & State Handling
- **Layout Skeleton:** Integrated inside `COMP-001: AppShell` with `COMP-002: ClinicHeader` and `COMP-004: BreadcrumbNav`.
- **Loading State:** Shimmering skeleton cards (`COMP-020`) matching form or table geometry; aria-busy='true'.
- **Empty State:** Illustrative placeholder (`COMP-019`) with descriptive Kannada and English guidance.
- **Error State:** Full-width error banner (`COMP-018`) with localized error message and retry button.
- **Offline / Sync State:** When operating under `Full Offline`, changes are buffered into Dexie IndexedDB `pending_mutations` with visual offline indicator (`COMP-136`).

#### 5. Integration Contracts & Dependencies
- **API Gateways:** `API-SYS-009`
- **Underlying Database Tables:** `system_configs, hardware_terminals`
- **Audit Event Trigger:** Encounters on this screen emit immutable audit events recorded in central WORM logs.

#### 6. Accessibility & Bilingual Localization
- **Accessibility (WCAG 2.1 AA):** Logical tab sequence, minimum 4.5:1 contrast, explicit focus rings, and screen reader announcements for all dynamic state mutations.
- **Localization:** Dynamic switching between Kannada (`kn-IN`) and English (`en-IN`) without page reload.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Successfully interact with Clinic Master Settings & Hardware Registry (SCREEN-108)
  Given user is authenticated with role 'ROLE-006'
  And the active terminal is assigned to route '/admin/settings'
  When user completes operational interaction on screen 'SCREEN-108'
  Then the system persists data to 'API-SYS-009' or queues in local IndexedDB
  And test 'PLANNED-TEST-FE-108' validates state transitions and UI responsiveness
```

---
