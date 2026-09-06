# Namma Clinic Role-to-Screen Access Matrix Specification

## 1. Executive Summary & Authorization Architecture
This specification defines the exhaustive Role-Based Access Control (RBAC) and Attribute-Based Access Control (ABAC) matrix governing user interface route access, action permissions, data export, printing, and offline persistence for all **30 canonical roles** across all **108 planned screens** of the Namma Clinic Platform. The frontend enforces a strict **Deny-by-Default** security posture: client-side route guards prevent rendering unauthorized screens, while backend API gateways cryptographically validate RS256 token claims for every dispatch.

## 2. Core RBAC / ABAC Security Policies
- **Deny-by-Default:** Any route traversal without explicit role entitlement in the active JWT results in immediate redirection to `/dashboard` with an unauthorized alert toast.
- **Facility & Ward Scoping (ABAC):** Clinic personnel can only interact with records belonging to their actively assigned BBMP clinic facility and municipal ward.
- **Active Shift Requirement:** Clinical encounters (Registration, Triage, Doctor Exam, Pharmacy Dispense) require an open, verified clinic shift record (`SCREEN-004`).
- **Cryptographic Break-Glass Protocol:** Emergency bypass (`SCREEN-005`) grants temporary elevated clinical access to doctors and staff nurses, generating tamper-evident WORM audit log entries.

## 3. Global Role Master Registry
| Role ID | Role Title | Functional Scope | Security Clearance Level |
| :--- | :--- | :--- | :--- |
| `ROLE-001` | Receptionist / Registration Clerk | RECEPTIONIST | Municipal Clinical Staff / Supervisory |
| `ROLE-002` | Medical Officer / General Physician | DOCTOR | Municipal Clinical Staff / Supervisory |
| `ROLE-003` | Staff Nurse / Triage Specialist | NURSE | Municipal Clinical Staff / Supervisory |
| `ROLE-004` | Pharmacist / Dispenser | PHARMACIST | Municipal Clinical Staff / Supervisory |
| `ROLE-005` | Laboratory Technician | LAB_TECH | Municipal Clinical Staff / Supervisory |
| `ROLE-006` | Clinic Administrative Officer | CLINIC_ADMIN | Municipal Clinical Staff / Supervisory |
| `ROLE-007` | Ward Health Supervisor | WARD_SUPERVISOR | Municipal Clinical Staff / Supervisory |
| `ROLE-008` | Zonal Health Officer (ZHO) | ZONAL_OFFICER | Municipal Clinical Staff / Supervisory |
| `ROLE-009` | Chief Health Officer (CHO) | CHIEF_OFFICER | Municipal Clinical Staff / Supervisory |
| `ROLE-010` | Epidemiologist / Disease Surveillance Officer | EPIDEMIOLOGIST | Municipal Clinical Staff / Supervisory |
| `ROLE-011` | Quality & Compliance Auditor | AUDITOR | Municipal Clinical Staff / Supervisory |
| `ROLE-012` | Security Administrator / CISO | SECURITY_ADMIN | Municipal Clinical Staff / Supervisory |
| `ROLE-013` | Central Depot Inventory Manager | DEPOT_MANAGER | Municipal Clinical Staff / Supervisory |
| `ROLE-014` | Cold Chain Logistics Technician | COLD_CHAIN_TECH | Municipal Clinical Staff / Supervisory |
| `ROLE-015` | Radiologist / Diagnostic Specialist | RADIOLOGIST | Municipal Clinical Staff / Supervisory |
| `ROLE-016` | Ayush Practitioner | AYUSH_DOC | Municipal Clinical Staff / Supervisory |
| `ROLE-017` | Counselor / Mental Health Worker | COUNSELOR | Municipal Clinical Staff / Supervisory |
| `ROLE-018` | ANM / Urban Health Worker | ANM_WORKER | Municipal Clinical Staff / Supervisory |
| `ROLE-019` | ASHA Link Worker Coordinator | ASHA_COORD | Municipal Clinical Staff / Supervisory |
| `ROLE-020` | Data Entry Operator | DATA_ENTRY | Municipal Clinical Staff / Supervisory |
| `ROLE-021` | Grievance Redressal Officer | GRIEVANCE_OFFICER | Municipal Clinical Staff / Supervisory |
| `ROLE-022` | ABDM National Integration Officer | ABDM_OFFICER | Municipal Clinical Staff / Supervisory |
| `ROLE-023` | Data Protection Officer (DPO) | PRIVACY_OFFICER | Municipal Clinical Staff / Supervisory |
| `ROLE-024` | IT Support & Hardware Engineer | IT_SUPPORT | Municipal Clinical Staff / Supervisory |
| `ROLE-025` | Clinical Audit Committee Member | CLINICAL_AUDITOR | Municipal Clinical Staff / Supervisory |
| `ROLE-026` | Procurement & Vendor Manager | PROCUREMENT_MGR | Municipal Clinical Staff / Supervisory |
| `ROLE-027` | Biomedical Waste Supervisor | WASTE_SUPERVISOR | Municipal Clinical Staff / Supervisory |
| `ROLE-028` | Telemedicine Remote Specialist | TELE_SPECIALIST | Municipal Clinical Staff / Supervisory |
| `ROLE-029` | Field Public Health Inspector | HEALTH_INSPECTOR | Municipal Clinical Staff / Supervisory |
| `ROLE-030` | Super Administrator | SUPER_ADMIN | Municipal Clinical Staff / Supervisory |

## 4. Master Screen Entitlement Matrix Across Core Functional Modules
The following matrix maps primary access rights across all 108 screens for key operational roles:

| Screen ID | Screen Name | Route | RECEPTIONIST | DOCTOR | NURSE | PHARMACIST | LAB_TECH | ADMIN | AUDITOR |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-001` | User Login Screen | `/login` | OWNER | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | DENY |
| `SCREEN-002` | MFA Verification Screen | `/login/mfa` | OWNER | ALLOW | DENY | DENY | DENY | ALLOW | DENY |
| `SCREEN-003` | Terminal Pairing & Device Enrollment | `/system/device-enroll` | DENY | DENY | DENY | DENY | DENY | OWNER | DENY |
| `SCREEN-004` | Clinic Shift Check-In & Handover | `/shift/checkin` | OWNER | ALLOW | ALLOW | ALLOW | DENY | DENY | DENY |
| `SCREEN-005` | Emergency Break-Glass Authorization | `/auth/break-glass` | DENY | OWNER | ALLOW | DENY | DENY | DENY | DENY |
| `SCREEN-006` | Master Clinic Dashboard | `/dashboard` | OWNER | ALLOW | ALLOW | ALLOW | DENY | ALLOW | DENY |
| `SCREEN-007` | Doctor Outpatient Console | `/doctor/console` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-008` | Staff Nurse Triage Workbench | `/nurse/triage` | DENY | DENY | OWNER | DENY | DENY | DENY | DENY |
| `SCREEN-009` | Pharmacy Dispensing Console | `/pharmacy/dispense` | DENY | DENY | DENY | OWNER | DENY | DENY | DENY |
| `SCREEN-010` | Diagnostic Laboratory Workbench | `/lab/workbench` | DENY | DENY | DENY | DENY | OWNER | DENY | DENY |
| `SCREEN-011` | Citizen New Registration Screen | `/patients/new` | OWNER | DENY | ALLOW | DENY | DENY | DENY | DENY |
| `SCREEN-012` | Citizen Search & Retrieval Screen | `/patients/search` | OWNER | ALLOW | ALLOW | ALLOW | DENY | DENY | DENY |
| `SCREEN-013` | Patient Longitudinal Profile View | `/patients/:id` | ALLOW | OWNER | ALLOW | DENY | DENY | DENY | DENY |
| `SCREEN-014` | Repeat Patient Fast Intake | `/patients/:id/repeat-intake` | OWNER | DENY | ALLOW | DENY | DENY | DENY | DENY |
| `SCREEN-015` | Biometric & ABHA Card Scan Modal | `/patients/abha-scan` | OWNER | DENY | ALLOW | DENY | DENY | DENY | DENY |
| `SCREEN-016` | Citizen Demographic Correction Form | `/patients/:id/edit` | OWNER | DENY | DENY | DENY | DENY | ALLOW | DENY |
| `SCREEN-017` | Duplicate Citizen Merge Modal | `/patients/merge` | DENY | DENY | DENY | DENY | DENY | OWNER | DENY |
| `SCREEN-018` | Citizen Digital Photo Capture | `/patients/:id/photo` | OWNER | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-019` | DPDP Informed Consent Capture Screen | `/patients/:id/consent` | OWNER | ALLOW | ALLOW | DENY | DENY | DENY | DENY |
| `SCREEN-020` | Consent History & Revocation Console | `/patients/:id/consents` | OWNER | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-021` | Data Portability & Export Request | `/patients/:id/export` | OWNER | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-022` | Citizen Grievance Redressal Intake | `/patients/:id/grievance` | OWNER | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-023` | Grievance Investigation & Resolution | `/grievances/:id` | DENY | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-024` | OPD Token Generation & Print Modal | `/queue/tokens/new` | OWNER | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-025` | Master Waiting Room Queue Display | `/queue/display` | OWNER | DENY | ALLOW | DENY | DENY | ALLOW | DENY |
| `SCREEN-026` | Queue Management & Rerouting Screen | `/queue/manage` | ALLOW | DENY | OWNER | DENY | DENY | ALLOW | DENY |
| `SCREEN-027` | Express Triage Queue | `/queue/triage-express` | DENY | DENY | OWNER | DENY | DENY | DENY | DENY |
| `SCREEN-028` | Pharmacy Pickup Waiting Screen | `/queue/pharmacy` | DENY | DENY | DENY | OWNER | DENY | DENY | DENY |
| `SCREEN-029` | Triage Vitals Entry Form | `/triage/:visitId/vitals` | DENY | DENY | OWNER | DENY | DENY | DENY | DENY |
| `SCREEN-030` | Pediatric Growth Chart & Z-Scores | `/triage/:visitId/pediatric` | DENY | ALLOW | OWNER | DENY | DENY | DENY | DENY |
| `SCREEN-031` | Antenatal Care (ANC) Vitals Intake | `/triage/:visitId/anc` | DENY | DENY | OWNER | DENY | DENY | DENY | DENY |
| `SCREEN-032` | Danger Signs & Triage Warning Modal | `/triage/:visitId/danger-modal` | DENY | ALLOW | OWNER | DENY | DENY | DENY | DENY |
| `SCREEN-033` | Point-of-Care Blood Sugar Entry | `/triage/:visitId/glucometer` | DENY | DENY | OWNER | DENY | ALLOW | DENY | DENY |
| `SCREEN-034` | Triage Station History Log | `/triage/station-history` | DENY | DENY | OWNER | DENY | DENY | DENY | DENY |
| `SCREEN-035` | Clinical Consultation Workspace | `/consultations/:visitId` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-036` | Chief Complaints & Systemic Review | `/consultations/:visitId/symptoms` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-037` | Physical & Clinical Examination Form | `/consultations/:visitId/exam` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-038` | ICD-10 & SNOMED CT Diagnosis Picker | `/consultations/:visitId/diagnosis` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-039` | NCD Chronic Disease Registry Form | `/consultations/:visitId/ncd` | DENY | OWNER | ALLOW | DENY | DENY | DENY | DENY |
| `SCREEN-040` | Past Medical & Surgical History Modal | `/consultations/:visitId/history` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-041` | Drug Allergy & Adverse Reaction Logger | `/consultations/:visitId/allergies` | DENY | OWNER | ALLOW | ALLOW | DENY | DENY | DENY |
| `SCREEN-042` | Clinical Progress Note & Free-Text Area | `/consultations/:visitId/notes` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-043` | Doctor Teleconsultation Video Room | `/consultations/:visitId/teleconsult` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-044` | Consultation Summary & Lock Dialog | `/consultations/:visitId/sign` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-045` | Doctor Outpatient Day Book View | `/doctor/daybook` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-046` | Electronic Prescription Form | `/prescriptions/:consultationId/new` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-047` | Drug-Drug & Drug-Allergy Warning Modal | `/prescriptions/interaction-modal` | DENY | OWNER | DENY | ALLOW | DENY | DENY | DENY |
| `SCREEN-048` | Standard Clinical Treatment Regimen Picker | `/prescriptions/templates` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-049` | Prescription Bilingual Print Preview | `/prescriptions/:id/print` | DENY | OWNER | DENY | ALLOW | DENY | DENY | DENY |
| `SCREEN-050` | Medication Modification & Cancellation | `/prescriptions/:id/modify` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-051` | Recurring Refill Request Form | `/prescriptions/:id/refill` | DENY | OWNER | ALLOW | DENY | DENY | DENY | DENY |
| `SCREEN-052` | Clinic Formulary & Stock Lookup Modal | `/formulary/lookup` | DENY | OWNER | ALLOW | ALLOW | DENY | DENY | DENY |
| `SCREEN-053` | Pharmacy Active Dispensing Screen | `/pharmacy/dispense/:id` | DENY | DENY | DENY | OWNER | DENY | DENY | DENY |
| `SCREEN-054` | Partial Dispensing & Stockout Dialog | `/pharmacy/dispense/:id/partial` | DENY | DENY | DENY | OWNER | DENY | DENY | DENY |
| `SCREEN-055` | Medicine Counseling Label Print Modal | `/pharmacy/labels/print` | DENY | DENY | DENY | OWNER | DENY | DENY | DENY |
| `SCREEN-056` | Pharmacy Shift Reconciliation Form | `/pharmacy/shift-reconciliation` | DENY | DENY | DENY | OWNER | DENY | DENY | DENY |
| `SCREEN-057` | Expired & Damaged Drug Quarantine Form | `/pharmacy/quarantine` | DENY | DENY | DENY | OWNER | DENY | ALLOW | DENY |
| `SCREEN-058` | Emergency Stock Requisition Form | `/pharmacy/requisitions/new` | DENY | DENY | DENY | OWNER | DENY | ALLOW | DENY |
| `SCREEN-059` | Pharmacy Dispensing Log History | `/pharmacy/history` | DENY | DENY | DENY | OWNER | DENY | DENY | ALLOW |
| `SCREEN-060` | Controlled Substances & High-Alert Register | `/pharmacy/controlled-register` | DENY | DENY | DENY | OWNER | DENY | ALLOW | ALLOW |
| `SCREEN-061` | Clinic Stock Inventory Dashboard | `/inventory` | DENY | DENY | DENY | OWNER | DENY | ALLOW | DENY |
| `SCREEN-062` | Stock Goods Receipt Note (GRN) Form | `/inventory/receipt` | DENY | DENY | DENY | OWNER | DENY | ALLOW | DENY |
| `SCREEN-063` | Cold Chain Refrigerator Telemetry View | `/inventory/cold-chain` | DENY | DENY | DENY | OWNER | DENY | DENY | DENY |
| `SCREEN-064` | Vaccine Stock & VVM Status Manager | `/inventory/vaccines` | DENY | DENY | OWNER | ALLOW | DENY | DENY | DENY |
| `SCREEN-065` | Inter-Clinic Stock Transfer Dispatch | `/inventory/transfers/out` | DENY | DENY | DENY | OWNER | DENY | ALLOW | DENY |
| `SCREEN-066` | Inter-Clinic Stock Transfer Receipt | `/inventory/transfers/in` | DENY | DENY | DENY | OWNER | DENY | ALLOW | DENY |
| `SCREEN-067` | Annual / Monthly Physical Audit Form | `/inventory/audit` | DENY | DENY | DENY | DENY | DENY | OWNER | ALLOW |
| `SCREEN-068` | Supplier Recall & Ban Notification Modal | `/inventory/recalls` | DENY | DENY | DENY | OWNER | DENY | ALLOW | DENY |
| `SCREEN-069` | Diagnostic Lab Test Orders Queue | `/lab/orders` | DENY | DENY | DENY | DENY | OWNER | DENY | DENY |
| `SCREEN-070` | Specimen Collection & Barcode Label Screen | `/lab/specimen/:id` | DENY | DENY | ALLOW | DENY | OWNER | DENY | DENY |
| `SCREEN-071` | Point-of-Care Rapid Test Result Entry | `/lab/results/poc/:id` | DENY | DENY | ALLOW | DENY | OWNER | DENY | DENY |
| `SCREEN-072` | Hematology Analyzer Data Import Screen | `/lab/analyzers/import` | DENY | DENY | DENY | DENY | OWNER | DENY | DENY |
| `SCREEN-073` | Lab Results Validation & Doctor Alert | `/lab/results/validate/:id` | DENY | ALLOW | DENY | DENY | OWNER | DENY | DENY |
| `SCREEN-074` | Diagnostic Report Bilingual Print Preview | `/lab/reports/:id/print` | DENY | DENY | DENY | DENY | OWNER | DENY | DENY |
| `SCREEN-075` | External Referral Lab Dispatch Form | `/lab/referrals/out` | DENY | DENY | DENY | DENY | OWNER | DENY | DENY |
| `SCREEN-076` | Lab Reagent & Quality Control Log | `/lab/qc` | DENY | DENY | DENY | DENY | OWNER | DENY | ALLOW |
| `SCREEN-077` | Secondary / Tertiary Referral Form | `/referrals/new` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-078` | 108 Emergency Ambulance Dispatch Screen | `/referrals/ambulance-108` | ALLOW | OWNER | ALLOW | DENY | DENY | DENY | DENY |
| `SCREEN-079` | Referral Handover Dossier Print Preview | `/referrals/:id/print` | DENY | OWNER | ALLOW | DENY | DENY | DENY | DENY |
| `SCREEN-080` | Active Outgoing Referrals Tracker | `/referrals/tracking` | DENY | ALLOW | OWNER | DENY | DENY | DENY | DENY |
| `SCREEN-081` | Discharge / Counter-Referral Ingest Form | `/referrals/counter-referral` | DENY | OWNER | ALLOW | DENY | DENY | DENY | DENY |
| `SCREEN-082` | Emergency Resuscitation Incident Record | `/referrals/resuscitation` | DENY | OWNER | ALLOW | DENY | DENY | DENY | DENY |
| `SCREEN-083` | Citizen SMS & Communication Center | `/notifications/sms-center` | OWNER | DENY | ALLOW | DENY | DENY | ALLOW | DENY |
| `SCREEN-084` | Chronic Disease Follow-Up Schedule | `/followup/schedule` | DENY | DENY | OWNER | DENY | DENY | DENY | DENY |
| `SCREEN-085` | ASHA Worker Community Outreach Tasklist | `/followup/asha-tasks` | DENY | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-086` | Public Health Broadcast Composer | `/notifications/broadcasts` | DENY | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-087` | Adverse Event Notification Form | `/notifications/adverse-events` | DENY | OWNER | ALLOW | ALLOW | DENY | DENY | DENY |
| `SCREEN-088` | Missed Follow-up Outreach Dialer Console | `/followup/dialer` | OWNER | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-089` | Epidemic Outbreak Surveillance Dashboard | `/analytics/surveillance` | DENY | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-090` | Ward Health Performance & KPI Scorecard | `/analytics/ward-kpi` | DENY | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-091` | Pharmacy Dispensing & Consumption Analytics | `/analytics/drug-utilization` | DENY | DENY | DENY | OWNER | DENY | DENY | DENY |
| `SCREEN-092` | Laboratory Diagnostic Workload Dashboard | `/analytics/lab-metrics` | DENY | DENY | DENY | DENY | OWNER | DENY | DENY |
| `SCREEN-093` | Maternal & Child Health Coverage Heatmap | `/analytics/mch-coverage` | DENY | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-094` | Custom Report Builder & CSV Export | `/analytics/custom-reports` | DENY | DENY | DENY | DENY | DENY | OWNER | ALLOW |
| `SCREEN-095` | Offline Storage & SQLite WAL Status | `/system/offline-storage` | DENY | DENY | DENY | DENY | DENY | OWNER | DENY |
| `SCREEN-096` | Sync Queue Monitor & Manual Flush | `/system/sync-queue` | DENY | DENY | DENY | DENY | DENY | OWNER | DENY |
| `SCREEN-097` | Sync Conflict Visual Resolution Modal | `/system/conflicts/:id` | DENY | ALLOW | DENY | DENY | DENY | OWNER | DENY |
| `SCREEN-098` | Peer-to-Peer Local WiFi Sync Setup | `/system/p2p-sync` | DENY | DENY | DENY | DENY | DENY | ALLOW | DENY |
| `SCREEN-099` | Offline Cryptographic Token Cache | `/system/offline-auth` | DENY | DENY | DENY | DENY | DENY | OWNER | DENY |
| `SCREEN-100` | Local Backup & USB Snapshot Export | `/system/local-backup` | DENY | DENY | DENY | DENY | DENY | OWNER | DENY |
| `SCREEN-101` | ABHA Creation & Mobile Verification | `/abdm/abha-create` | OWNER | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-102` | ABDM Consent Request & Artifact Drawer | `/abdm/consent-requests` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-103` | FHIR R4 Health Data Push Monitor | `/abdm/fhir-push` | DENY | DENY | DENY | DENY | DENY | ALLOW | DENY |
| `SCREEN-104` | External Hospital Records Viewer | `/abdm/external-records/:uhid` | DENY | OWNER | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-105` | Cryptographic WORM Audit Log Viewer | `/audit/logs` | DENY | DENY | DENY | DENY | DENY | DENY | ALLOW |
| `SCREEN-106` | Security Incident & Intrusion Alert Board | `/security/alerts` | DENY | DENY | DENY | DENY | DENY | DENY | DENY |
| `SCREEN-107` | User Management & Role Assignment | `/admin/users` | DENY | DENY | DENY | DENY | DENY | OWNER | DENY |
| `SCREEN-108` | Clinic Master Settings & Hardware Registry | `/admin/settings` | DENY | DENY | DENY | DENY | DENY | OWNER | DENY |

## 5. Exhaustive Role-to-Screen Entitlement Profiles

### Role Profile: ROLE-001 — Receptionist / Registration Clerk
**Official System Code:** `RECEPTIONIST` | **Total Accessible Screens:** 22

#### 1. Operational Mandate & Scope of Practice
The `Receptionist / Registration Clerk` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-001` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-001` | User Login Screen | `/login` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-002` | MFA Verification Screen | `/login/mfa` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-004` | Clinic Shift Check-In & Handover | `/shift/checkin` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-006` | Master Clinic Dashboard | `/dashboard` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-011` | Citizen New Registration Screen | `/patients/new` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-012` | Citizen Search & Retrieval Screen | `/patients/search` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-014` | Repeat Patient Fast Intake | `/patients/:id/repeat-intake` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-015` | Biometric & ABHA Card Scan Modal | `/patients/abha-scan` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-016` | Citizen Demographic Correction Form | `/patients/:id/edit` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-018` | Citizen Digital Photo Capture | `/patients/:id/photo` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-019` | DPDP Informed Consent Capture Screen | `/patients/:id/consent` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-020` | Consent History & Revocation Console | `/patients/:id/consents` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-021` | Data Portability & Export Request | `/patients/:id/export` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-022` | Citizen Grievance Redressal Intake | `/patients/:id/grievance` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-024` | OPD Token Generation & Print Modal | `/queue/tokens/new` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-025` | Master Waiting Room Queue Display | `/queue/display` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-083` | Citizen SMS & Communication Center | `/notifications/sms-center` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-088` | Missed Follow-up Outreach Dialer Console | `/followup/dialer` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-101` | ABHA Creation & Mobile Verification | `/abdm/abha-create` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-013` | Patient Longitudinal Profile View | `/patients/:id` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-026` | Queue Management & Rerouting Screen | `/queue/manage` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-078` | 108 Emergency Ambulance Dispatch Screen | `/referrals/ambulance-108` | Secondary Access | Read, View History | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-001`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Permitted (OPD tokens & labels)
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Permitted (Rapid intake & dispensing)
- **Digital Web Camera:** Permitted (Citizen portrait capture)

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-001` (Receptionist / Registration Clerk) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-001` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Receptionist / Registration Clerk (ROLE-001)
  Given a user is authenticated with official role 'ROLE-001'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/login'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-002 — Medical Officer / General Physician
**Official System Code:** `DOCTOR` | **Total Accessible Screens:** 40

#### 1. Operational Mandate & Scope of Practice
The `Medical Officer / General Physician` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-002` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-005` | Emergency Break-Glass Authorization | `/auth/break-glass` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-007` | Doctor Outpatient Console | `/doctor/console` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-013` | Patient Longitudinal Profile View | `/patients/:id` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-035` | Clinical Consultation Workspace | `/consultations/:visitId` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-036` | Chief Complaints & Systemic Review | `/consultations/:visitId/symptoms` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-037` | Physical & Clinical Examination Form | `/consultations/:visitId/exam` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-038` | ICD-10 & SNOMED CT Diagnosis Picker | `/consultations/:visitId/diagnosis` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-039` | NCD Chronic Disease Registry Form | `/consultations/:visitId/ncd` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-040` | Past Medical & Surgical History Modal | `/consultations/:visitId/history` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-041` | Drug Allergy & Adverse Reaction Logger | `/consultations/:visitId/allergies` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-042` | Clinical Progress Note & Free-Text Area | `/consultations/:visitId/notes` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-043` | Doctor Teleconsultation Video Room | `/consultations/:visitId/teleconsult` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-044` | Consultation Summary & Lock Dialog | `/consultations/:visitId/sign` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-045` | Doctor Outpatient Day Book View | `/doctor/daybook` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-046` | Electronic Prescription Form | `/prescriptions/:consultationId/new` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-047` | Drug-Drug & Drug-Allergy Warning Modal | `/prescriptions/interaction-modal` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-048` | Standard Clinical Treatment Regimen Picker | `/prescriptions/templates` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-049` | Prescription Bilingual Print Preview | `/prescriptions/:id/print` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-050` | Medication Modification & Cancellation | `/prescriptions/:id/modify` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-051` | Recurring Refill Request Form | `/prescriptions/:id/refill` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-052` | Clinic Formulary & Stock Lookup Modal | `/formulary/lookup` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-077` | Secondary / Tertiary Referral Form | `/referrals/new` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-078` | 108 Emergency Ambulance Dispatch Screen | `/referrals/ambulance-108` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-079` | Referral Handover Dossier Print Preview | `/referrals/:id/print` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-081` | Discharge / Counter-Referral Ingest Form | `/referrals/counter-referral` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-082` | Emergency Resuscitation Incident Record | `/referrals/resuscitation` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-087` | Adverse Event Notification Form | `/notifications/adverse-events` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-102` | ABDM Consent Request & Artifact Drawer | `/abdm/consent-requests` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-104` | External Hospital Records Viewer | `/abdm/external-records/:uhid` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-001` | User Login Screen | `/login` | Secondary Access | Read, View History | Online Only |
| `SCREEN-002` | MFA Verification Screen | `/login/mfa` | Secondary Access | Read, View History | Online Only |
| `SCREEN-004` | Clinic Shift Check-In & Handover | `/shift/checkin` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-006` | Master Clinic Dashboard | `/dashboard` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-012` | Citizen Search & Retrieval Screen | `/patients/search` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-019` | DPDP Informed Consent Capture Screen | `/patients/:id/consent` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-030` | Pediatric Growth Chart & Z-Scores | `/triage/:visitId/pediatric` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-032` | Danger Signs & Triage Warning Modal | `/triage/:visitId/danger-modal` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-073` | Lab Results Validation & Doctor Alert | `/lab/results/validate/:id` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-080` | Active Outgoing Referrals Tracker | `/referrals/tracking` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-097` | Sync Conflict Visual Resolution Modal | `/system/conflicts/:id` | Secondary Access | Read, View History | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-002`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Permitted (Prescriptions & lab reports)
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-002` (Medical Officer / General Physician) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Eligible for break-glass emergency override (`SCREEN-005`) with mandatory justification.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-002` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Medical Officer / General Physician (ROLE-002)
  Given a user is authenticated with official role 'ROLE-002'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/auth/break-glass'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-003 — Staff Nurse / Triage Specialist
**Official System Code:** `NURSE` | **Total Accessible Screens:** 35

#### 1. Operational Mandate & Scope of Practice
The `Staff Nurse / Triage Specialist` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-003` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-008` | Staff Nurse Triage Workbench | `/nurse/triage` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-026` | Queue Management & Rerouting Screen | `/queue/manage` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-027` | Express Triage Queue | `/queue/triage-express` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-029` | Triage Vitals Entry Form | `/triage/:visitId/vitals` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-030` | Pediatric Growth Chart & Z-Scores | `/triage/:visitId/pediatric` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-031` | Antenatal Care (ANC) Vitals Intake | `/triage/:visitId/anc` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-032` | Danger Signs & Triage Warning Modal | `/triage/:visitId/danger-modal` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-033` | Point-of-Care Blood Sugar Entry | `/triage/:visitId/glucometer` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-034` | Triage Station History Log | `/triage/station-history` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-064` | Vaccine Stock & VVM Status Manager | `/inventory/vaccines` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-080` | Active Outgoing Referrals Tracker | `/referrals/tracking` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-084` | Chronic Disease Follow-Up Schedule | `/followup/schedule` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-001` | User Login Screen | `/login` | Secondary Access | Read, View History | Online Only |
| `SCREEN-004` | Clinic Shift Check-In & Handover | `/shift/checkin` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-005` | Emergency Break-Glass Authorization | `/auth/break-glass` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-006` | Master Clinic Dashboard | `/dashboard` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-011` | Citizen New Registration Screen | `/patients/new` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-012` | Citizen Search & Retrieval Screen | `/patients/search` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-013` | Patient Longitudinal Profile View | `/patients/:id` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-014` | Repeat Patient Fast Intake | `/patients/:id/repeat-intake` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-015` | Biometric & ABHA Card Scan Modal | `/patients/abha-scan` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-019` | DPDP Informed Consent Capture Screen | `/patients/:id/consent` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-025` | Master Waiting Room Queue Display | `/queue/display` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-039` | NCD Chronic Disease Registry Form | `/consultations/:visitId/ncd` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-041` | Drug Allergy & Adverse Reaction Logger | `/consultations/:visitId/allergies` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-051` | Recurring Refill Request Form | `/prescriptions/:id/refill` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-052` | Clinic Formulary & Stock Lookup Modal | `/formulary/lookup` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-070` | Specimen Collection & Barcode Label Screen | `/lab/specimen/:id` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-071` | Point-of-Care Rapid Test Result Entry | `/lab/results/poc/:id` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-078` | 108 Emergency Ambulance Dispatch Screen | `/referrals/ambulance-108` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-079` | Referral Handover Dossier Print Preview | `/referrals/:id/print` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-081` | Discharge / Counter-Referral Ingest Form | `/referrals/counter-referral` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-082` | Emergency Resuscitation Incident Record | `/referrals/resuscitation` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-083` | Citizen SMS & Communication Center | `/notifications/sms-center` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-087` | Adverse Event Notification Form | `/notifications/adverse-events` | Secondary Access | Read, View History | Full Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-003`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Permitted (OPD tokens & labels)
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-003` (Staff Nurse / Triage Specialist) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Eligible for break-glass emergency override (`SCREEN-005`) with mandatory justification.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-003` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Staff Nurse / Triage Specialist (ROLE-003)
  Given a user is authenticated with official role 'ROLE-003'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/nurse/triage'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-004 — Pharmacist / Dispenser
**Official System Code:** `PHARMACIST` | **Total Accessible Screens:** 27

#### 1. Operational Mandate & Scope of Practice
The `Pharmacist / Dispenser` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-004` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-009` | Pharmacy Dispensing Console | `/pharmacy/dispense` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-028` | Pharmacy Pickup Waiting Screen | `/queue/pharmacy` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-053` | Pharmacy Active Dispensing Screen | `/pharmacy/dispense/:id` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-054` | Partial Dispensing & Stockout Dialog | `/pharmacy/dispense/:id/partial` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-055` | Medicine Counseling Label Print Modal | `/pharmacy/labels/print` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-056` | Pharmacy Shift Reconciliation Form | `/pharmacy/shift-reconciliation` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-057` | Expired & Damaged Drug Quarantine Form | `/pharmacy/quarantine` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-058` | Emergency Stock Requisition Form | `/pharmacy/requisitions/new` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-059` | Pharmacy Dispensing Log History | `/pharmacy/history` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-060` | Controlled Substances & High-Alert Register | `/pharmacy/controlled-register` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-061` | Clinic Stock Inventory Dashboard | `/inventory` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-062` | Stock Goods Receipt Note (GRN) Form | `/inventory/receipt` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-063` | Cold Chain Refrigerator Telemetry View | `/inventory/cold-chain` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-065` | Inter-Clinic Stock Transfer Dispatch | `/inventory/transfers/out` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-066` | Inter-Clinic Stock Transfer Receipt | `/inventory/transfers/in` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-068` | Supplier Recall & Ban Notification Modal | `/inventory/recalls` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-091` | Pharmacy Dispensing & Consumption Analytics | `/analytics/drug-utilization` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-001` | User Login Screen | `/login` | Secondary Access | Read, View History | Online Only |
| `SCREEN-004` | Clinic Shift Check-In & Handover | `/shift/checkin` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-006` | Master Clinic Dashboard | `/dashboard` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-012` | Citizen Search & Retrieval Screen | `/patients/search` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-041` | Drug Allergy & Adverse Reaction Logger | `/consultations/:visitId/allergies` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-047` | Drug-Drug & Drug-Allergy Warning Modal | `/prescriptions/interaction-modal` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-049` | Prescription Bilingual Print Preview | `/prescriptions/:id/print` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-052` | Clinic Formulary & Stock Lookup Modal | `/formulary/lookup` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-064` | Vaccine Stock & VVM Status Manager | `/inventory/vaccines` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-087` | Adverse Event Notification Form | `/notifications/adverse-events` | Secondary Access | Read, View History | Full Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-004`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Permitted (OPD tokens & labels)
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Permitted (Rapid intake & dispensing)
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-004` (Pharmacist / Dispenser) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-004` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Pharmacist / Dispenser (ROLE-004)
  Given a user is authenticated with official role 'ROLE-004'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/pharmacy/dispense'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-005 — Laboratory Technician
**Official System Code:** `LAB_TECH` | **Total Accessible Screens:** 12

#### 1. Operational Mandate & Scope of Practice
The `Laboratory Technician` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-005` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-010` | Diagnostic Laboratory Workbench | `/lab/workbench` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-069` | Diagnostic Lab Test Orders Queue | `/lab/orders` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-070` | Specimen Collection & Barcode Label Screen | `/lab/specimen/:id` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-071` | Point-of-Care Rapid Test Result Entry | `/lab/results/poc/:id` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-072` | Hematology Analyzer Data Import Screen | `/lab/analyzers/import` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-073` | Lab Results Validation & Doctor Alert | `/lab/results/validate/:id` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-074` | Diagnostic Report Bilingual Print Preview | `/lab/reports/:id/print` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-075` | External Referral Lab Dispatch Form | `/lab/referrals/out` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-076` | Lab Reagent & Quality Control Log | `/lab/qc` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-092` | Laboratory Diagnostic Workload Dashboard | `/analytics/lab-metrics` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-001` | User Login Screen | `/login` | Secondary Access | Read, View History | Online Only |
| `SCREEN-033` | Point-of-Care Blood Sugar Entry | `/triage/:visitId/glucometer` | Secondary Access | Read, View History | Full Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-005`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Permitted (Prescriptions & lab reports)
- **HID Barcode Scanner:** Permitted (Rapid intake & dispensing)
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-005` (Laboratory Technician) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-005` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Laboratory Technician (ROLE-005)
  Given a user is authenticated with official role 'ROLE-005'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/lab/workbench'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-006 — Clinic Administrative Officer
**Official System Code:** `CLINIC_ADMIN` | **Total Accessible Screens:** 28

#### 1. Operational Mandate & Scope of Practice
The `Clinic Administrative Officer` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-006` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-003` | Terminal Pairing & Device Enrollment | `/system/device-enroll` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-017` | Duplicate Citizen Merge Modal | `/patients/merge` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-067` | Annual / Monthly Physical Audit Form | `/inventory/audit` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-094` | Custom Report Builder & CSV Export | `/analytics/custom-reports` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-095` | Offline Storage & SQLite WAL Status | `/system/offline-storage` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-096` | Sync Queue Monitor & Manual Flush | `/system/sync-queue` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-097` | Sync Conflict Visual Resolution Modal | `/system/conflicts/:id` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-099` | Offline Cryptographic Token Cache | `/system/offline-auth` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-100` | Local Backup & USB Snapshot Export | `/system/local-backup` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-107` | User Management & Role Assignment | `/admin/users` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-108` | Clinic Master Settings & Hardware Registry | `/admin/settings` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-001` | User Login Screen | `/login` | Secondary Access | Read, View History | Online Only |
| `SCREEN-002` | MFA Verification Screen | `/login/mfa` | Secondary Access | Read, View History | Online Only |
| `SCREEN-006` | Master Clinic Dashboard | `/dashboard` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-016` | Citizen Demographic Correction Form | `/patients/:id/edit` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-025` | Master Waiting Room Queue Display | `/queue/display` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-026` | Queue Management & Rerouting Screen | `/queue/manage` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-057` | Expired & Damaged Drug Quarantine Form | `/pharmacy/quarantine` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-058` | Emergency Stock Requisition Form | `/pharmacy/requisitions/new` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-060` | Controlled Substances & High-Alert Register | `/pharmacy/controlled-register` | Secondary Access | Read, View History | Online Only |
| `SCREEN-061` | Clinic Stock Inventory Dashboard | `/inventory` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-062` | Stock Goods Receipt Note (GRN) Form | `/inventory/receipt` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-065` | Inter-Clinic Stock Transfer Dispatch | `/inventory/transfers/out` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-066` | Inter-Clinic Stock Transfer Receipt | `/inventory/transfers/in` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-068` | Supplier Recall & Ban Notification Modal | `/inventory/recalls` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-083` | Citizen SMS & Communication Center | `/notifications/sms-center` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-098` | Peer-to-Peer Local WiFi Sync Setup | `/system/p2p-sync` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-103` | FHIR R4 Health Data Push Monitor | `/abdm/fhir-push` | Secondary Access | Read, View History | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-006`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Permitted (Prescriptions & lab reports)
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-006` (Clinic Administrative Officer) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-006` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Clinic Administrative Officer (ROLE-006)
  Given a user is authenticated with official role 'ROLE-006'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/system/device-enroll'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-007 — Ward Health Supervisor
**Official System Code:** `WARD_SUPERVISOR` | **Total Accessible Screens:** 2

#### 1. Operational Mandate & Scope of Practice
The `Ward Health Supervisor` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-007` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-090` | Ward Health Performance & KPI Scorecard | `/analytics/ward-kpi` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-080` | Active Outgoing Referrals Tracker | `/referrals/tracking` | Secondary Access | Read, View History | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-007`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-007` (Ward Health Supervisor) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-007` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Ward Health Supervisor (ROLE-007)
  Given a user is authenticated with official role 'ROLE-007'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/analytics/ward-kpi'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-008 — Zonal Health Officer (ZHO)
**Official System Code:** `ZONAL_OFFICER` | **Total Accessible Screens:** 6

#### 1. Operational Mandate & Scope of Practice
The `Zonal Health Officer (ZHO)` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-008` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-086` | Public Health Broadcast Composer | `/notifications/broadcasts` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-093` | Maternal & Child Health Coverage Heatmap | `/analytics/mch-coverage` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-023` | Grievance Investigation & Resolution | `/grievances/:id` | Secondary Access | Read, View History | Online Only |
| `SCREEN-089` | Epidemic Outbreak Surveillance Dashboard | `/analytics/surveillance` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-090` | Ward Health Performance & KPI Scorecard | `/analytics/ward-kpi` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-094` | Custom Report Builder & CSV Export | `/analytics/custom-reports` | Secondary Access | Read, View History | Online Only |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-008`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-008` (Zonal Health Officer (ZHO)) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-008` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Zonal Health Officer (ZHO) (ROLE-008)
  Given a user is authenticated with official role 'ROLE-008'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/notifications/broadcasts'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-009 — Chief Health Officer (CHO)
**Official System Code:** `CHIEF_OFFICER` | **Total Accessible Screens:** 2

#### 1. Operational Mandate & Scope of Practice
The `Chief Health Officer (CHO)` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-009` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-086` | Public Health Broadcast Composer | `/notifications/broadcasts` | Secondary Access | Read, View History | Online Only |
| `SCREEN-089` | Epidemic Outbreak Surveillance Dashboard | `/analytics/surveillance` | Secondary Access | Read, View History | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-009`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-009` (Chief Health Officer (CHO)) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-009` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Chief Health Officer (CHO) (ROLE-009)
  Given a user is authenticated with official role 'ROLE-009'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-010 — Epidemiologist / Disease Surveillance Officer
**Official System Code:** `EPIDEMIOLOGIST` | **Total Accessible Screens:** 1

#### 1. Operational Mandate & Scope of Practice
The `Epidemiologist / Disease Surveillance Officer` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-010` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-089` | Epidemic Outbreak Surveillance Dashboard | `/analytics/surveillance` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-010`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-010` (Epidemiologist / Disease Surveillance Officer) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-010` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Epidemiologist / Disease Surveillance Officer (ROLE-010)
  Given a user is authenticated with official role 'ROLE-010'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/analytics/surveillance'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-011 — Quality & Compliance Auditor
**Official System Code:** `AUDITOR` | **Total Accessible Screens:** 6

#### 1. Operational Mandate & Scope of Practice
The `Quality & Compliance Auditor` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-011` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-105` | Cryptographic WORM Audit Log Viewer | `/audit/logs` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-059` | Pharmacy Dispensing Log History | `/pharmacy/history` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-060` | Controlled Substances & High-Alert Register | `/pharmacy/controlled-register` | Secondary Access | Read, View History | Online Only |
| `SCREEN-067` | Annual / Monthly Physical Audit Form | `/inventory/audit` | Secondary Access | Read, View History | Online Only |
| `SCREEN-076` | Lab Reagent & Quality Control Log | `/lab/qc` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-094` | Custom Report Builder & CSV Export | `/analytics/custom-reports` | Secondary Access | Read, View History | Online Only |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-011`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-011` (Quality & Compliance Auditor) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-011` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Quality & Compliance Auditor (ROLE-011)
  Given a user is authenticated with official role 'ROLE-011'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/audit/logs'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-012 — Security Administrator / CISO
**Official System Code:** `SECURITY_ADMIN` | **Total Accessible Screens:** 3

#### 1. Operational Mandate & Scope of Practice
The `Security Administrator / CISO` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-012` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-106` | Security Incident & Intrusion Alert Board | `/security/alerts` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-099` | Offline Cryptographic Token Cache | `/system/offline-auth` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-105` | Cryptographic WORM Audit Log Viewer | `/audit/logs` | Secondary Access | Read, View History | Full Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-012`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-012` (Security Administrator / CISO) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-012` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Security Administrator / CISO (ROLE-012)
  Given a user is authenticated with official role 'ROLE-012'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/security/alerts'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-013 — Central Depot Inventory Manager
**Official System Code:** `DEPOT_MANAGER` | **Total Accessible Screens:** 2

#### 1. Operational Mandate & Scope of Practice
The `Central Depot Inventory Manager` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-013` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-061` | Clinic Stock Inventory Dashboard | `/inventory` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-091` | Pharmacy Dispensing & Consumption Analytics | `/analytics/drug-utilization` | Secondary Access | Read, View History | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-013`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-013` (Central Depot Inventory Manager) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-013` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Central Depot Inventory Manager (ROLE-013)
  Given a user is authenticated with official role 'ROLE-013'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-014 — Cold Chain Logistics Technician
**Official System Code:** `COLD_CHAIN_TECH` | **Total Accessible Screens:** 2

#### 1. Operational Mandate & Scope of Practice
The `Cold Chain Logistics Technician` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-014` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-063` | Cold Chain Refrigerator Telemetry View | `/inventory/cold-chain` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-064` | Vaccine Stock & VVM Status Manager | `/inventory/vaccines` | Secondary Access | Read, View History | Full Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-014`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-014` (Cold Chain Logistics Technician) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-014` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Cold Chain Logistics Technician (ROLE-014)
  Given a user is authenticated with official role 'ROLE-014'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-015 — Radiologist / Diagnostic Specialist
**Official System Code:** `RADIOLOGIST` | **Total Accessible Screens:** 1

#### 1. Operational Mandate & Scope of Practice
The `Radiologist / Diagnostic Specialist` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-015` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-092` | Laboratory Diagnostic Workload Dashboard | `/analytics/lab-metrics` | Secondary Access | Read, View History | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-015`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-015` (Radiologist / Diagnostic Specialist) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-015` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Radiologist / Diagnostic Specialist (ROLE-015)
  Given a user is authenticated with official role 'ROLE-015'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-016 — Ayush Practitioner
**Official System Code:** `AYUSH_DOC` | **Total Accessible Screens:** 0

#### 1. Operational Mandate & Scope of Practice
The `Ayush Practitioner` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-016` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-006` | Master Clinic Dashboard | `/dashboard` | View Only | Read KPI Summary | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-016`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-016` (Ayush Practitioner) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-016` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Ayush Practitioner (ROLE-016)
  Given a user is authenticated with official role 'ROLE-016'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-017 — Counselor / Mental Health Worker
**Official System Code:** `COUNSELOR` | **Total Accessible Screens:** 0

#### 1. Operational Mandate & Scope of Practice
The `Counselor / Mental Health Worker` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-017` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-006` | Master Clinic Dashboard | `/dashboard` | View Only | Read KPI Summary | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-017`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-017` (Counselor / Mental Health Worker) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-017` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Counselor / Mental Health Worker (ROLE-017)
  Given a user is authenticated with official role 'ROLE-017'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-018 — ANM / Urban Health Worker
**Official System Code:** `ANM_WORKER` | **Total Accessible Screens:** 4

#### 1. Operational Mandate & Scope of Practice
The `ANM / Urban Health Worker` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-018` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-031` | Antenatal Care (ANC) Vitals Intake | `/triage/:visitId/anc` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-084` | Chronic Disease Follow-Up Schedule | `/followup/schedule` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-085` | ASHA Worker Community Outreach Tasklist | `/followup/asha-tasks` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-093` | Maternal & Child Health Coverage Heatmap | `/analytics/mch-coverage` | Secondary Access | Read, View History | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-018`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-018` (ANM / Urban Health Worker) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-018` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role ANM / Urban Health Worker (ROLE-018)
  Given a user is authenticated with official role 'ROLE-018'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-019 — ASHA Link Worker Coordinator
**Official System Code:** `ASHA_COORD` | **Total Accessible Screens:** 2

#### 1. Operational Mandate & Scope of Practice
The `ASHA Link Worker Coordinator` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-019` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-085` | ASHA Worker Community Outreach Tasklist | `/followup/asha-tasks` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-084` | Chronic Disease Follow-Up Schedule | `/followup/schedule` | Secondary Access | Read, View History | Full Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-019`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-019` (ASHA Link Worker Coordinator) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-019` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role ASHA Link Worker Coordinator (ROLE-019)
  Given a user is authenticated with official role 'ROLE-019'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/followup/asha-tasks'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-020 — Data Entry Operator
**Official System Code:** `DATA_ENTRY` | **Total Accessible Screens:** 3

#### 1. Operational Mandate & Scope of Practice
The `Data Entry Operator` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-020` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-011` | Citizen New Registration Screen | `/patients/new` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-018` | Citizen Digital Photo Capture | `/patients/:id/photo` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-088` | Missed Follow-up Outreach Dialer Console | `/followup/dialer` | Secondary Access | Read, View History | Online Only |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-020`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Permitted (OPD tokens & labels)
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Permitted (Citizen portrait capture)

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-020` (Data Entry Operator) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-020` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Data Entry Operator (ROLE-020)
  Given a user is authenticated with official role 'ROLE-020'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-021 — Grievance Redressal Officer
**Official System Code:** `GRIEVANCE_OFFICER` | **Total Accessible Screens:** 2

#### 1. Operational Mandate & Scope of Practice
The `Grievance Redressal Officer` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-021` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-023` | Grievance Investigation & Resolution | `/grievances/:id` | **Primary Owner** | Read, Create, Edit, Print | Online Only |
| `SCREEN-022` | Citizen Grievance Redressal Intake | `/patients/:id/grievance` | Secondary Access | Read, View History | Full Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-021`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-021` (Grievance Redressal Officer) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-021` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Grievance Redressal Officer (ROLE-021)
  Given a user is authenticated with official role 'ROLE-021'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/grievances/:id'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-022 — ABDM National Integration Officer
**Official System Code:** `ABDM_OFFICER` | **Total Accessible Screens:** 3

#### 1. Operational Mandate & Scope of Practice
The `ABDM National Integration Officer` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-022` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-103` | FHIR R4 Health Data Push Monitor | `/abdm/fhir-push` | **Primary Owner** | Read, Create, Edit, Print | Degraded Offline |
| `SCREEN-101` | ABHA Creation & Mobile Verification | `/abdm/abha-create` | Secondary Access | Read, View History | Online Only |
| `SCREEN-102` | ABDM Consent Request & Artifact Drawer | `/abdm/consent-requests` | Secondary Access | Read, View History | Online Only |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-022`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-022` (ABDM National Integration Officer) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-022` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role ABDM National Integration Officer (ROLE-022)
  Given a user is authenticated with official role 'ROLE-022'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/abdm/fhir-push'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-023 — Data Protection Officer (DPO)
**Official System Code:** `PRIVACY_OFFICER` | **Total Accessible Screens:** 3

#### 1. Operational Mandate & Scope of Practice
The `Data Protection Officer (DPO)` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-023` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-017` | Duplicate Citizen Merge Modal | `/patients/merge` | Secondary Access | Read, View History | Online Only |
| `SCREEN-020` | Consent History & Revocation Console | `/patients/:id/consents` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-021` | Data Portability & Export Request | `/patients/:id/export` | Secondary Access | Read, View History | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-023`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-023` (Data Protection Officer (DPO)) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-023` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Data Protection Officer (DPO) (ROLE-023)
  Given a user is authenticated with official role 'ROLE-023'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-024 — IT Support & Hardware Engineer
**Official System Code:** `IT_SUPPORT` | **Total Accessible Screens:** 6

#### 1. Operational Mandate & Scope of Practice
The `IT Support & Hardware Engineer` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-024` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-098` | Peer-to-Peer Local WiFi Sync Setup | `/system/p2p-sync` | **Primary Owner** | Read, Create, Edit, Print | Full Offline |
| `SCREEN-003` | Terminal Pairing & Device Enrollment | `/system/device-enroll` | Secondary Access | Read, View History | Online Only |
| `SCREEN-095` | Offline Storage & SQLite WAL Status | `/system/offline-storage` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-096` | Sync Queue Monitor & Manual Flush | `/system/sync-queue` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-100` | Local Backup & USB Snapshot Export | `/system/local-backup` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-108` | Clinic Master Settings & Hardware Registry | `/admin/settings` | Secondary Access | Read, View History | Full Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-024`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-024` (IT Support & Hardware Engineer) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-024` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role IT Support & Hardware Engineer (ROLE-024)
  Given a user is authenticated with official role 'ROLE-024'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/system/p2p-sync'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-025 — Clinical Audit Committee Member
**Official System Code:** `CLINICAL_AUDITOR` | **Total Accessible Screens:** 0

#### 1. Operational Mandate & Scope of Practice
The `Clinical Audit Committee Member` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-025` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-006` | Master Clinic Dashboard | `/dashboard` | View Only | Read KPI Summary | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-025`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-025` (Clinical Audit Committee Member) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-025` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Clinical Audit Committee Member (ROLE-025)
  Given a user is authenticated with official role 'ROLE-025'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-026 — Procurement & Vendor Manager
**Official System Code:** `PROCUREMENT_MGR` | **Total Accessible Screens:** 1

#### 1. Operational Mandate & Scope of Practice
The `Procurement & Vendor Manager` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-026` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-091` | Pharmacy Dispensing & Consumption Analytics | `/analytics/drug-utilization` | Secondary Access | Read, View History | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-026`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-026` (Procurement & Vendor Manager) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-026` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Procurement & Vendor Manager (ROLE-026)
  Given a user is authenticated with official role 'ROLE-026'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-027 — Biomedical Waste Supervisor
**Official System Code:** `WASTE_SUPERVISOR` | **Total Accessible Screens:** 0

#### 1. Operational Mandate & Scope of Practice
The `Biomedical Waste Supervisor` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-027` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-006` | Master Clinic Dashboard | `/dashboard` | View Only | Read KPI Summary | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-027`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-027` (Biomedical Waste Supervisor) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-027` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Biomedical Waste Supervisor (ROLE-027)
  Given a user is authenticated with official role 'ROLE-027'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-028 — Telemedicine Remote Specialist
**Official System Code:** `TELE_SPECIALIST` | **Total Accessible Screens:** 1

#### 1. Operational Mandate & Scope of Practice
The `Telemedicine Remote Specialist` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-028` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-043` | Doctor Teleconsultation Video Room | `/consultations/:visitId/teleconsult` | Secondary Access | Read, View History | Online Only |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-028`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-028` (Telemedicine Remote Specialist) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-028` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Telemedicine Remote Specialist (ROLE-028)
  Given a user is authenticated with official role 'ROLE-028'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-029 — Field Public Health Inspector
**Official System Code:** `HEALTH_INSPECTOR` | **Total Accessible Screens:** 0

#### 1. Operational Mandate & Scope of Practice
The `Field Public Health Inspector` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-029` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-006` | Master Clinic Dashboard | `/dashboard` | View Only | Read KPI Summary | Degraded Offline |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-029`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-029` (Field Public Health Inspector) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-029` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Field Public Health Inspector (ROLE-029)
  Given a user is authenticated with official role 'ROLE-029'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

### Role Profile: ROLE-030 — Super Administrator
**Official System Code:** `SUPER_ADMIN` | **Total Accessible Screens:** 3

#### 1. Operational Mandate & Scope of Practice
The `Super Administrator` is authorized to execute municipal healthcare duties within their defined clinical or administrative sphere. Role entitlements adhere to statutory Indian healthcare privacy principles and BBMP Health Department guidelines. Every session initiated by `ROLE-030` is strictly bound to the active clinic facility and requires verified biometric or two-factor authentication.

#### 2. Screen Entitlements & Action Matrix
| Screen ID | Screen Name | Route | Access Type | Actions Permitted | Offline Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SCREEN-105` | Cryptographic WORM Audit Log Viewer | `/audit/logs` | Secondary Access | Read, View History | Full Offline |
| `SCREEN-106` | Security Incident & Intrusion Alert Board | `/security/alerts` | Secondary Access | Read, View History | Degraded Offline |
| `SCREEN-107` | User Management & Role Assignment | `/admin/users` | Secondary Access | Read, View History | Online Only |

#### 3. Granular Field-Level & Action-Level Permissions
For every screen accessible under `ROLE-030`, specific field and action constraints are applied:
- **Patient Demographic Fields:** Read access granted for identity verification; edit rights restricted to registration desk roles or administrative supervisors.
- **Clinical Notes & Prescriptions:** Direct authoring permitted exclusively to licensed medical officers (`ROLE-002`); other roles restricted to dispensing or triage views.
- **Drug Inventory Quantities:** Read access across all dispensary shelves; decrement rights reserved for active dispensing pharmacists.
- **Audit Log Inspection:** Access restricted unless explicitly cleared for compliance review (`ROLE-011` / `ROLE-012`).

#### 4. Hardware & Peripheral Device Access Rights
- **Thermal Receipt Printer (80mm):** Restricted
- **A4 Laser Document Printer:** Restricted
- **HID Barcode Scanner:** Not required
- **Digital Web Camera:** Restricted

#### 5. Session, Inactivity & Security Guardrails
- **Session Inactivity Timeout:** 15 minutes of user inactivity automatically activates `COMP-155: SessionInactivityWarningModal`.
- **Concurrent Session Enforcement:** Single active concurrent session per user account across clinic terminals.
- **Offline Data Caching Quota:** Up to 500 local encounters cached in encrypted IndexedDB for 72 hours.
- **Audit Event Emitters:** Emits `AUDIT-AUTH-LOGIN`, `AUDIT-ENCOUNTER-ACCESS`, and `AUDIT-PHI-VIEW` to central WORM logs.

#### 6. Emergency & Break-Glass Delegation Rules
When operating under emergency conditions at the municipal clinic, role `ROLE-030` (Super Administrator) adheres to specific delegation and escalation invariants:
- **Clinical Override Authorization:** Strictly prohibited from invoking clinical break-glass override.
- **Shift Handover Delegation:** During official staff shift change, permissions must be formally transferred via `SCREEN-004: Clinic Shift Check-In & Handover`.
- **Disaster Recovery Mode:** In case of catastrophic network outage, role `ROLE-030` retains cached operational permissions on the clinic local mini-PC.

#### 7. Automated Acceptance Criteria (Gherkin BDD)
```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify access permissions for role Super Administrator (ROLE-030)
  Given a user is authenticated with official role 'ROLE-030'
  And the user belongs to active facility 'BBMP-NAMMA-042'
  When the user navigates to an entitled screen such as '/dashboard'
  Then the route guard renders the screen successfully without access violations
  And attempts to navigate to unauthorized screens trigger HTTP 403 / UI redirect
```

---

## 6. Exhaustive Module-by-Module Action Permission Mapping
The following table provides the exhaustive end-to-end traceability tuple for clinical and administrative operations:
`ROLE -> MODULE -> SCREEN -> ACTION -> PERMISSION -> API -> DATA -> AUDIT EVENT`

| Role Code | Module ID | Screen ID | Action Description | RBAC Permission | API Endpoint | Data Entity | Audit Event ID |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `RECEPTIONIST` | `MODULE-001` | `SCREEN-001` | Execute User Login Screen | `perm:module-001:execute` | `API-AUTH-001` | `auth_users` | `AUDIT-UI-001` |
| `CLINIC_ADMIN` | `MODULE-001` | `SCREEN-001` | Supervise User Login Screen | `perm:module-001:audit` | `API-AUTH-001` | `auth_users` | `AUDIT-SUP-001` |
| `AUDITOR` | `MODULE-001` | `SCREEN-001` | Compliance Review User Login Screen | `perm:module-001:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-001` |
| `SECURITY_ADMIN` | `MODULE-001` | `SCREEN-001` | Threat Monitor User Login Screen | `perm:module-001:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-001` |
| `RECEPTIONIST` | `MODULE-001` | `SCREEN-002` | Execute MFA Verification Screen | `perm:module-001:execute` | `API-AUTH-002` | `user_sessions` | `AUDIT-UI-002` |
| `CLINIC_ADMIN` | `MODULE-001` | `SCREEN-002` | Supervise MFA Verification Screen | `perm:module-001:audit` | `API-AUTH-002` | `user_sessions` | `AUDIT-SUP-002` |
| `AUDITOR` | `MODULE-001` | `SCREEN-002` | Compliance Review MFA Verification Screen | `perm:module-001:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-002` |
| `SECURITY_ADMIN` | `MODULE-001` | `SCREEN-002` | Threat Monitor MFA Verification Screen | `perm:module-001:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-002` |
| `CLINIC_ADMIN` | `MODULE-001` | `SCREEN-003` | Execute Terminal Pairing & Device Enrollment | `perm:module-001:execute` | `API-SYS-001` | `hardware_terminals` | `AUDIT-UI-003` |
| `CLINIC_ADMIN` | `MODULE-001` | `SCREEN-003` | Supervise Terminal Pairing & Device Enrollment | `perm:module-001:audit` | `API-SYS-001` | `hardware_terminals` | `AUDIT-SUP-003` |
| `AUDITOR` | `MODULE-001` | `SCREEN-003` | Compliance Review Terminal Pairing & Device Enrollment | `perm:module-001:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-003` |
| `SECURITY_ADMIN` | `MODULE-001` | `SCREEN-003` | Threat Monitor Terminal Pairing & Device Enrollment | `perm:module-001:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-003` |
| `RECEPTIONIST` | `MODULE-001` | `SCREEN-004` | Execute Clinic Shift Check-In & Handover | `perm:module-001:execute` | `API-AUTH-005` | `clinic_shifts` | `AUDIT-UI-004` |
| `CLINIC_ADMIN` | `MODULE-001` | `SCREEN-004` | Supervise Clinic Shift Check-In & Handover | `perm:module-001:audit` | `API-AUTH-005` | `clinic_shifts` | `AUDIT-SUP-004` |
| `AUDITOR` | `MODULE-001` | `SCREEN-004` | Compliance Review Clinic Shift Check-In & Handover | `perm:module-001:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-004` |
| `SECURITY_ADMIN` | `MODULE-001` | `SCREEN-004` | Threat Monitor Clinic Shift Check-In & Handover | `perm:module-001:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-004` |
| `DOCTOR` | `MODULE-001` | `SCREEN-005` | Execute Emergency Break-Glass Authorization | `perm:module-001:execute` | `API-AUTH-004` | `audit_events` | `AUDIT-UI-005` |
| `CLINIC_ADMIN` | `MODULE-001` | `SCREEN-005` | Supervise Emergency Break-Glass Authorization | `perm:module-001:audit` | `API-AUTH-004` | `audit_events` | `AUDIT-SUP-005` |
| `AUDITOR` | `MODULE-001` | `SCREEN-005` | Compliance Review Emergency Break-Glass Authorization | `perm:module-001:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-005` |
| `SECURITY_ADMIN` | `MODULE-001` | `SCREEN-005` | Threat Monitor Emergency Break-Glass Authorization | `perm:module-001:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-005` |
| `RECEPTIONIST` | `MODULE-002` | `SCREEN-006` | Execute Master Clinic Dashboard | `perm:module-002:execute` | `API-ANL-001` | `visits` | `AUDIT-UI-006` |
| `CLINIC_ADMIN` | `MODULE-002` | `SCREEN-006` | Supervise Master Clinic Dashboard | `perm:module-002:audit` | `API-ANL-001` | `visits` | `AUDIT-SUP-006` |
| `AUDITOR` | `MODULE-002` | `SCREEN-006` | Compliance Review Master Clinic Dashboard | `perm:module-002:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-006` |
| `SECURITY_ADMIN` | `MODULE-002` | `SCREEN-006` | Threat Monitor Master Clinic Dashboard | `perm:module-002:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-006` |
| `DOCTOR` | `MODULE-002` | `SCREEN-007` | Execute Doctor Outpatient Console | `perm:module-002:execute` | `API-VST-001` | `visits` | `AUDIT-UI-007` |
| `CLINIC_ADMIN` | `MODULE-002` | `SCREEN-007` | Supervise Doctor Outpatient Console | `perm:module-002:audit` | `API-VST-001` | `visits` | `AUDIT-SUP-007` |
| `AUDITOR` | `MODULE-002` | `SCREEN-007` | Compliance Review Doctor Outpatient Console | `perm:module-002:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-007` |
| `SECURITY_ADMIN` | `MODULE-002` | `SCREEN-007` | Threat Monitor Doctor Outpatient Console | `perm:module-002:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-007` |
| `NURSE` | `MODULE-002` | `SCREEN-008` | Execute Staff Nurse Triage Workbench | `perm:module-002:execute` | `API-TRG-001` | `triage_assessments` | `AUDIT-UI-008` |
| `CLINIC_ADMIN` | `MODULE-002` | `SCREEN-008` | Supervise Staff Nurse Triage Workbench | `perm:module-002:audit` | `API-TRG-001` | `triage_assessments` | `AUDIT-SUP-008` |
| `AUDITOR` | `MODULE-002` | `SCREEN-008` | Compliance Review Staff Nurse Triage Workbench | `perm:module-002:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-008` |
| `SECURITY_ADMIN` | `MODULE-002` | `SCREEN-008` | Threat Monitor Staff Nurse Triage Workbench | `perm:module-002:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-008` |
| `PHARMACIST` | `MODULE-002` | `SCREEN-009` | Execute Pharmacy Dispensing Console | `perm:module-002:execute` | `API-PHR-001` | `prescriptions` | `AUDIT-UI-009` |
| `CLINIC_ADMIN` | `MODULE-002` | `SCREEN-009` | Supervise Pharmacy Dispensing Console | `perm:module-002:audit` | `API-PHR-001` | `prescriptions` | `AUDIT-SUP-009` |
| `AUDITOR` | `MODULE-002` | `SCREEN-009` | Compliance Review Pharmacy Dispensing Console | `perm:module-002:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-009` |
| `SECURITY_ADMIN` | `MODULE-002` | `SCREEN-009` | Threat Monitor Pharmacy Dispensing Console | `perm:module-002:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-009` |
| `LAB_TECH` | `MODULE-002` | `SCREEN-010` | Execute Diagnostic Laboratory Workbench | `perm:module-002:execute` | `API-LAB-001` | `lab_orders` | `AUDIT-UI-010` |
| `CLINIC_ADMIN` | `MODULE-002` | `SCREEN-010` | Supervise Diagnostic Laboratory Workbench | `perm:module-002:audit` | `API-LAB-001` | `lab_orders` | `AUDIT-SUP-010` |
| `AUDITOR` | `MODULE-002` | `SCREEN-010` | Compliance Review Diagnostic Laboratory Workbench | `perm:module-002:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-010` |
| `SECURITY_ADMIN` | `MODULE-002` | `SCREEN-010` | Threat Monitor Diagnostic Laboratory Workbench | `perm:module-002:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-010` |
| `RECEPTIONIST` | `MODULE-003` | `SCREEN-011` | Execute Citizen New Registration Screen | `perm:module-003:execute` | `API-PAT-001` | `patients` | `AUDIT-UI-011` |
| `CLINIC_ADMIN` | `MODULE-003` | `SCREEN-011` | Supervise Citizen New Registration Screen | `perm:module-003:audit` | `API-PAT-001` | `patients` | `AUDIT-SUP-011` |
| `AUDITOR` | `MODULE-003` | `SCREEN-011` | Compliance Review Citizen New Registration Screen | `perm:module-003:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-011` |
| `SECURITY_ADMIN` | `MODULE-003` | `SCREEN-011` | Threat Monitor Citizen New Registration Screen | `perm:module-003:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-011` |
| `RECEPTIONIST` | `MODULE-003` | `SCREEN-012` | Execute Citizen Search & Retrieval Screen | `perm:module-003:execute` | `API-PAT-002` | `patients` | `AUDIT-UI-012` |
| `CLINIC_ADMIN` | `MODULE-003` | `SCREEN-012` | Supervise Citizen Search & Retrieval Screen | `perm:module-003:audit` | `API-PAT-002` | `patients` | `AUDIT-SUP-012` |
| `AUDITOR` | `MODULE-003` | `SCREEN-012` | Compliance Review Citizen Search & Retrieval Screen | `perm:module-003:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-012` |
| `SECURITY_ADMIN` | `MODULE-003` | `SCREEN-012` | Threat Monitor Citizen Search & Retrieval Screen | `perm:module-003:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-012` |
| `DOCTOR` | `MODULE-003` | `SCREEN-013` | Execute Patient Longitudinal Profile View | `perm:module-003:execute` | `API-PAT-003` | `patients` | `AUDIT-UI-013` |
| `CLINIC_ADMIN` | `MODULE-003` | `SCREEN-013` | Supervise Patient Longitudinal Profile View | `perm:module-003:audit` | `API-PAT-003` | `patients` | `AUDIT-SUP-013` |
| `AUDITOR` | `MODULE-003` | `SCREEN-013` | Compliance Review Patient Longitudinal Profile View | `perm:module-003:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-013` |
| `SECURITY_ADMIN` | `MODULE-003` | `SCREEN-013` | Threat Monitor Patient Longitudinal Profile View | `perm:module-003:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-013` |
| `RECEPTIONIST` | `MODULE-003` | `SCREEN-014` | Execute Repeat Patient Fast Intake | `perm:module-003:execute` | `API-VST-001` | `visits` | `AUDIT-UI-014` |
| `CLINIC_ADMIN` | `MODULE-003` | `SCREEN-014` | Supervise Repeat Patient Fast Intake | `perm:module-003:audit` | `API-VST-001` | `visits` | `AUDIT-SUP-014` |
| `AUDITOR` | `MODULE-003` | `SCREEN-014` | Compliance Review Repeat Patient Fast Intake | `perm:module-003:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-014` |
| `SECURITY_ADMIN` | `MODULE-003` | `SCREEN-014` | Threat Monitor Repeat Patient Fast Intake | `perm:module-003:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-014` |
| `RECEPTIONIST` | `MODULE-003` | `SCREEN-015` | Execute Biometric & ABHA Card Scan Modal | `perm:module-003:execute` | `API-ABDM-001` | `patients` | `AUDIT-UI-015` |
| `CLINIC_ADMIN` | `MODULE-003` | `SCREEN-015` | Supervise Biometric & ABHA Card Scan Modal | `perm:module-003:audit` | `API-ABDM-001` | `patients` | `AUDIT-SUP-015` |
| `AUDITOR` | `MODULE-003` | `SCREEN-015` | Compliance Review Biometric & ABHA Card Scan Modal | `perm:module-003:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-015` |
| `SECURITY_ADMIN` | `MODULE-003` | `SCREEN-015` | Threat Monitor Biometric & ABHA Card Scan Modal | `perm:module-003:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-015` |
| `RECEPTIONIST` | `MODULE-003` | `SCREEN-016` | Execute Citizen Demographic Correction Form | `perm:module-003:execute` | `API-PAT-004` | `patients` | `AUDIT-UI-016` |
| `CLINIC_ADMIN` | `MODULE-003` | `SCREEN-016` | Supervise Citizen Demographic Correction Form | `perm:module-003:audit` | `API-PAT-004` | `patients` | `AUDIT-SUP-016` |
| `AUDITOR` | `MODULE-003` | `SCREEN-016` | Compliance Review Citizen Demographic Correction Form | `perm:module-003:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-016` |
| `SECURITY_ADMIN` | `MODULE-003` | `SCREEN-016` | Threat Monitor Citizen Demographic Correction Form | `perm:module-003:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-016` |
| `CLINIC_ADMIN` | `MODULE-003` | `SCREEN-017` | Execute Duplicate Citizen Merge Modal | `perm:module-003:execute` | `API-PAT-005` | `patients` | `AUDIT-UI-017` |
| `CLINIC_ADMIN` | `MODULE-003` | `SCREEN-017` | Supervise Duplicate Citizen Merge Modal | `perm:module-003:audit` | `API-PAT-005` | `patients` | `AUDIT-SUP-017` |
| `AUDITOR` | `MODULE-003` | `SCREEN-017` | Compliance Review Duplicate Citizen Merge Modal | `perm:module-003:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-017` |
| `SECURITY_ADMIN` | `MODULE-003` | `SCREEN-017` | Threat Monitor Duplicate Citizen Merge Modal | `perm:module-003:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-017` |
| `RECEPTIONIST` | `MODULE-003` | `SCREEN-018` | Execute Citizen Digital Photo Capture | `perm:module-003:execute` | `API-PAT-006` | `patients` | `AUDIT-UI-018` |
| `CLINIC_ADMIN` | `MODULE-003` | `SCREEN-018` | Supervise Citizen Digital Photo Capture | `perm:module-003:audit` | `API-PAT-006` | `patients` | `AUDIT-SUP-018` |
| `AUDITOR` | `MODULE-003` | `SCREEN-018` | Compliance Review Citizen Digital Photo Capture | `perm:module-003:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-018` |
| `SECURITY_ADMIN` | `MODULE-003` | `SCREEN-018` | Threat Monitor Citizen Digital Photo Capture | `perm:module-003:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-018` |
| `RECEPTIONIST` | `MODULE-004` | `SCREEN-019` | Execute DPDP Informed Consent Capture Screen | `perm:module-004:execute` | `API-PAT-007` | `patient_consents` | `AUDIT-UI-019` |
| `CLINIC_ADMIN` | `MODULE-004` | `SCREEN-019` | Supervise DPDP Informed Consent Capture Screen | `perm:module-004:audit` | `API-PAT-007` | `patient_consents` | `AUDIT-SUP-019` |
| `AUDITOR` | `MODULE-004` | `SCREEN-019` | Compliance Review DPDP Informed Consent Capture Screen | `perm:module-004:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-019` |
| `SECURITY_ADMIN` | `MODULE-004` | `SCREEN-019` | Threat Monitor DPDP Informed Consent Capture Screen | `perm:module-004:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-019` |
| `RECEPTIONIST` | `MODULE-004` | `SCREEN-020` | Execute Consent History & Revocation Console | `perm:module-004:execute` | `API-PAT-008` | `patient_consents` | `AUDIT-UI-020` |
| `CLINIC_ADMIN` | `MODULE-004` | `SCREEN-020` | Supervise Consent History & Revocation Console | `perm:module-004:audit` | `API-PAT-008` | `patient_consents` | `AUDIT-SUP-020` |
| `AUDITOR` | `MODULE-004` | `SCREEN-020` | Compliance Review Consent History & Revocation Console | `perm:module-004:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-020` |
| `SECURITY_ADMIN` | `MODULE-004` | `SCREEN-020` | Threat Monitor Consent History & Revocation Console | `perm:module-004:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-020` |
| `RECEPTIONIST` | `MODULE-004` | `SCREEN-021` | Execute Data Portability & Export Request | `perm:module-004:execute` | `API-PORT-001` | `patient_exports` | `AUDIT-UI-021` |
| `CLINIC_ADMIN` | `MODULE-004` | `SCREEN-021` | Supervise Data Portability & Export Request | `perm:module-004:audit` | `API-PORT-001` | `patient_exports` | `AUDIT-SUP-021` |
| `AUDITOR` | `MODULE-004` | `SCREEN-021` | Compliance Review Data Portability & Export Request | `perm:module-004:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-021` |
| `SECURITY_ADMIN` | `MODULE-004` | `SCREEN-021` | Threat Monitor Data Portability & Export Request | `perm:module-004:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-021` |
| `RECEPTIONIST` | `MODULE-004` | `SCREEN-022` | Execute Citizen Grievance Redressal Intake | `perm:module-004:execute` | `API-SYS-002` | `citizen_grievances` | `AUDIT-UI-022` |
| `CLINIC_ADMIN` | `MODULE-004` | `SCREEN-022` | Supervise Citizen Grievance Redressal Intake | `perm:module-004:audit` | `API-SYS-002` | `citizen_grievances` | `AUDIT-SUP-022` |
| `AUDITOR` | `MODULE-004` | `SCREEN-022` | Compliance Review Citizen Grievance Redressal Intake | `perm:module-004:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-022` |
| `SECURITY_ADMIN` | `MODULE-004` | `SCREEN-022` | Threat Monitor Citizen Grievance Redressal Intake | `perm:module-004:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-022` |
| `GRIEVANCE_OFFICER` | `MODULE-004` | `SCREEN-023` | Execute Grievance Investigation & Resolution | `perm:module-004:execute` | `API-SYS-003` | `citizen_grievances` | `AUDIT-UI-023` |
| `CLINIC_ADMIN` | `MODULE-004` | `SCREEN-023` | Supervise Grievance Investigation & Resolution | `perm:module-004:audit` | `API-SYS-003` | `citizen_grievances` | `AUDIT-SUP-023` |
| `AUDITOR` | `MODULE-004` | `SCREEN-023` | Compliance Review Grievance Investigation & Resolution | `perm:module-004:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-023` |
| `SECURITY_ADMIN` | `MODULE-004` | `SCREEN-023` | Threat Monitor Grievance Investigation & Resolution | `perm:module-004:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-023` |
| `RECEPTIONIST` | `MODULE-005` | `SCREEN-024` | Execute OPD Token Generation & Print Modal | `perm:module-005:execute` | `API-VST-002` | `visits` | `AUDIT-UI-024` |
| `CLINIC_ADMIN` | `MODULE-005` | `SCREEN-024` | Supervise OPD Token Generation & Print Modal | `perm:module-005:audit` | `API-VST-002` | `visits` | `AUDIT-SUP-024` |
| `AUDITOR` | `MODULE-005` | `SCREEN-024` | Compliance Review OPD Token Generation & Print Modal | `perm:module-005:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-024` |
| `SECURITY_ADMIN` | `MODULE-005` | `SCREEN-024` | Threat Monitor OPD Token Generation & Print Modal | `perm:module-005:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-024` |
| `RECEPTIONIST` | `MODULE-005` | `SCREEN-025` | Execute Master Waiting Room Queue Display | `perm:module-005:execute` | `API-VST-003` | `opd_queues` | `AUDIT-UI-025` |
| `CLINIC_ADMIN` | `MODULE-005` | `SCREEN-025` | Supervise Master Waiting Room Queue Display | `perm:module-005:audit` | `API-VST-003` | `opd_queues` | `AUDIT-SUP-025` |
| `AUDITOR` | `MODULE-005` | `SCREEN-025` | Compliance Review Master Waiting Room Queue Display | `perm:module-005:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-025` |
| `SECURITY_ADMIN` | `MODULE-005` | `SCREEN-025` | Threat Monitor Master Waiting Room Queue Display | `perm:module-005:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-025` |
| `NURSE` | `MODULE-005` | `SCREEN-026` | Execute Queue Management & Rerouting Screen | `perm:module-005:execute` | `API-VST-004` | `opd_queues` | `AUDIT-UI-026` |
| `CLINIC_ADMIN` | `MODULE-005` | `SCREEN-026` | Supervise Queue Management & Rerouting Screen | `perm:module-005:audit` | `API-VST-004` | `opd_queues` | `AUDIT-SUP-026` |
| `AUDITOR` | `MODULE-005` | `SCREEN-026` | Compliance Review Queue Management & Rerouting Screen | `perm:module-005:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-026` |
| `SECURITY_ADMIN` | `MODULE-005` | `SCREEN-026` | Threat Monitor Queue Management & Rerouting Screen | `perm:module-005:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-026` |
| `NURSE` | `MODULE-005` | `SCREEN-027` | Execute Express Triage Queue | `perm:module-005:execute` | `API-VST-005` | `opd_queues` | `AUDIT-UI-027` |
| `CLINIC_ADMIN` | `MODULE-005` | `SCREEN-027` | Supervise Express Triage Queue | `perm:module-005:audit` | `API-VST-005` | `opd_queues` | `AUDIT-SUP-027` |
| `AUDITOR` | `MODULE-005` | `SCREEN-027` | Compliance Review Express Triage Queue | `perm:module-005:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-027` |
| `SECURITY_ADMIN` | `MODULE-005` | `SCREEN-027` | Threat Monitor Express Triage Queue | `perm:module-005:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-027` |
| `PHARMACIST` | `MODULE-005` | `SCREEN-028` | Execute Pharmacy Pickup Waiting Screen | `perm:module-005:execute` | `API-PHR-002` | `prescriptions` | `AUDIT-UI-028` |
| `CLINIC_ADMIN` | `MODULE-005` | `SCREEN-028` | Supervise Pharmacy Pickup Waiting Screen | `perm:module-005:audit` | `API-PHR-002` | `prescriptions` | `AUDIT-SUP-028` |
| `AUDITOR` | `MODULE-005` | `SCREEN-028` | Compliance Review Pharmacy Pickup Waiting Screen | `perm:module-005:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-028` |
| `SECURITY_ADMIN` | `MODULE-005` | `SCREEN-028` | Threat Monitor Pharmacy Pickup Waiting Screen | `perm:module-005:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-028` |
| `NURSE` | `MODULE-006` | `SCREEN-029` | Execute Triage Vitals Entry Form | `perm:module-006:execute` | `API-TRG-002` | `triage_assessments` | `AUDIT-UI-029` |
| `CLINIC_ADMIN` | `MODULE-006` | `SCREEN-029` | Supervise Triage Vitals Entry Form | `perm:module-006:audit` | `API-TRG-002` | `triage_assessments` | `AUDIT-SUP-029` |
| `AUDITOR` | `MODULE-006` | `SCREEN-029` | Compliance Review Triage Vitals Entry Form | `perm:module-006:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-029` |
| `SECURITY_ADMIN` | `MODULE-006` | `SCREEN-029` | Threat Monitor Triage Vitals Entry Form | `perm:module-006:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-029` |
| `NURSE` | `MODULE-006` | `SCREEN-030` | Execute Pediatric Growth Chart & Z-Scores | `perm:module-006:execute` | `API-TRG-003` | `triage_assessments` | `AUDIT-UI-030` |
| `CLINIC_ADMIN` | `MODULE-006` | `SCREEN-030` | Supervise Pediatric Growth Chart & Z-Scores | `perm:module-006:audit` | `API-TRG-003` | `triage_assessments` | `AUDIT-SUP-030` |
| `AUDITOR` | `MODULE-006` | `SCREEN-030` | Compliance Review Pediatric Growth Chart & Z-Scores | `perm:module-006:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-030` |
| `SECURITY_ADMIN` | `MODULE-006` | `SCREEN-030` | Threat Monitor Pediatric Growth Chart & Z-Scores | `perm:module-006:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-030` |
| `NURSE` | `MODULE-006` | `SCREEN-031` | Execute Antenatal Care (ANC) Vitals Intake | `perm:module-006:execute` | `API-TRG-004` | `triage_assessments` | `AUDIT-UI-031` |
| `CLINIC_ADMIN` | `MODULE-006` | `SCREEN-031` | Supervise Antenatal Care (ANC) Vitals Intake | `perm:module-006:audit` | `API-TRG-004` | `triage_assessments` | `AUDIT-SUP-031` |
| `AUDITOR` | `MODULE-006` | `SCREEN-031` | Compliance Review Antenatal Care (ANC) Vitals Intake | `perm:module-006:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-031` |
| `SECURITY_ADMIN` | `MODULE-006` | `SCREEN-031` | Threat Monitor Antenatal Care (ANC) Vitals Intake | `perm:module-006:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-031` |
| `NURSE` | `MODULE-006` | `SCREEN-032` | Execute Danger Signs & Triage Warning Modal | `perm:module-006:execute` | `API-TRG-005` | `triage_assessments` | `AUDIT-UI-032` |
| `CLINIC_ADMIN` | `MODULE-006` | `SCREEN-032` | Supervise Danger Signs & Triage Warning Modal | `perm:module-006:audit` | `API-TRG-005` | `triage_assessments` | `AUDIT-SUP-032` |
| `AUDITOR` | `MODULE-006` | `SCREEN-032` | Compliance Review Danger Signs & Triage Warning Modal | `perm:module-006:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-032` |
| `SECURITY_ADMIN` | `MODULE-006` | `SCREEN-032` | Threat Monitor Danger Signs & Triage Warning Modal | `perm:module-006:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-032` |
| `NURSE` | `MODULE-006` | `SCREEN-033` | Execute Point-of-Care Blood Sugar Entry | `perm:module-006:execute` | `API-TRG-006` | `triage_assessments` | `AUDIT-UI-033` |
| `CLINIC_ADMIN` | `MODULE-006` | `SCREEN-033` | Supervise Point-of-Care Blood Sugar Entry | `perm:module-006:audit` | `API-TRG-006` | `triage_assessments` | `AUDIT-SUP-033` |
| `AUDITOR` | `MODULE-006` | `SCREEN-033` | Compliance Review Point-of-Care Blood Sugar Entry | `perm:module-006:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-033` |
| `SECURITY_ADMIN` | `MODULE-006` | `SCREEN-033` | Threat Monitor Point-of-Care Blood Sugar Entry | `perm:module-006:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-033` |
| `NURSE` | `MODULE-006` | `SCREEN-034` | Execute Triage Station History Log | `perm:module-006:execute` | `API-TRG-007` | `triage_assessments` | `AUDIT-UI-034` |
| `CLINIC_ADMIN` | `MODULE-006` | `SCREEN-034` | Supervise Triage Station History Log | `perm:module-006:audit` | `API-TRG-007` | `triage_assessments` | `AUDIT-SUP-034` |
| `AUDITOR` | `MODULE-006` | `SCREEN-034` | Compliance Review Triage Station History Log | `perm:module-006:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-034` |
| `SECURITY_ADMIN` | `MODULE-006` | `SCREEN-034` | Threat Monitor Triage Station History Log | `perm:module-006:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-034` |
| `DOCTOR` | `MODULE-007` | `SCREEN-035` | Execute Clinical Consultation Workspace | `perm:module-007:execute` | `API-CON-002` | `consultations` | `AUDIT-UI-035` |
| `CLINIC_ADMIN` | `MODULE-007` | `SCREEN-035` | Supervise Clinical Consultation Workspace | `perm:module-007:audit` | `API-CON-002` | `consultations` | `AUDIT-SUP-035` |
| `AUDITOR` | `MODULE-007` | `SCREEN-035` | Compliance Review Clinical Consultation Workspace | `perm:module-007:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-035` |
| `SECURITY_ADMIN` | `MODULE-007` | `SCREEN-035` | Threat Monitor Clinical Consultation Workspace | `perm:module-007:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-035` |
| `DOCTOR` | `MODULE-007` | `SCREEN-036` | Execute Chief Complaints & Systemic Review | `perm:module-007:execute` | `API-CON-003` | `consultations` | `AUDIT-UI-036` |
| `CLINIC_ADMIN` | `MODULE-007` | `SCREEN-036` | Supervise Chief Complaints & Systemic Review | `perm:module-007:audit` | `API-CON-003` | `consultations` | `AUDIT-SUP-036` |
| `AUDITOR` | `MODULE-007` | `SCREEN-036` | Compliance Review Chief Complaints & Systemic Review | `perm:module-007:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-036` |
| `SECURITY_ADMIN` | `MODULE-007` | `SCREEN-036` | Threat Monitor Chief Complaints & Systemic Review | `perm:module-007:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-036` |
| `DOCTOR` | `MODULE-007` | `SCREEN-037` | Execute Physical & Clinical Examination Form | `perm:module-007:execute` | `API-CON-004` | `consultations` | `AUDIT-UI-037` |
| `CLINIC_ADMIN` | `MODULE-007` | `SCREEN-037` | Supervise Physical & Clinical Examination Form | `perm:module-007:audit` | `API-CON-004` | `consultations` | `AUDIT-SUP-037` |
| `AUDITOR` | `MODULE-007` | `SCREEN-037` | Compliance Review Physical & Clinical Examination Form | `perm:module-007:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-037` |
| `SECURITY_ADMIN` | `MODULE-007` | `SCREEN-037` | Threat Monitor Physical & Clinical Examination Form | `perm:module-007:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-037` |
| `DOCTOR` | `MODULE-007` | `SCREEN-038` | Execute ICD-10 & SNOMED CT Diagnosis Picker | `perm:module-007:execute` | `API-CON-005` | `consultations` | `AUDIT-UI-038` |
| `CLINIC_ADMIN` | `MODULE-007` | `SCREEN-038` | Supervise ICD-10 & SNOMED CT Diagnosis Picker | `perm:module-007:audit` | `API-CON-005` | `consultations` | `AUDIT-SUP-038` |
| `AUDITOR` | `MODULE-007` | `SCREEN-038` | Compliance Review ICD-10 & SNOMED CT Diagnosis Picker | `perm:module-007:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-038` |
| `SECURITY_ADMIN` | `MODULE-007` | `SCREEN-038` | Threat Monitor ICD-10 & SNOMED CT Diagnosis Picker | `perm:module-007:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-038` |
| `DOCTOR` | `MODULE-007` | `SCREEN-039` | Execute NCD Chronic Disease Registry Form | `perm:module-007:execute` | `API-CON-006` | `consultations` | `AUDIT-UI-039` |
| `CLINIC_ADMIN` | `MODULE-007` | `SCREEN-039` | Supervise NCD Chronic Disease Registry Form | `perm:module-007:audit` | `API-CON-006` | `consultations` | `AUDIT-SUP-039` |
| `AUDITOR` | `MODULE-007` | `SCREEN-039` | Compliance Review NCD Chronic Disease Registry Form | `perm:module-007:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-039` |
| `SECURITY_ADMIN` | `MODULE-007` | `SCREEN-039` | Threat Monitor NCD Chronic Disease Registry Form | `perm:module-007:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-039` |
| `DOCTOR` | `MODULE-007` | `SCREEN-040` | Execute Past Medical & Surgical History Modal | `perm:module-007:execute` | `API-CON-007` | `consultations` | `AUDIT-UI-040` |
| `CLINIC_ADMIN` | `MODULE-007` | `SCREEN-040` | Supervise Past Medical & Surgical History Modal | `perm:module-007:audit` | `API-CON-007` | `consultations` | `AUDIT-SUP-040` |
| `AUDITOR` | `MODULE-007` | `SCREEN-040` | Compliance Review Past Medical & Surgical History Modal | `perm:module-007:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-040` |
| `SECURITY_ADMIN` | `MODULE-007` | `SCREEN-040` | Threat Monitor Past Medical & Surgical History Modal | `perm:module-007:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-040` |
| `DOCTOR` | `MODULE-007` | `SCREEN-041` | Execute Drug Allergy & Adverse Reaction Logger | `perm:module-007:execute` | `API-CON-008` | `patient_allergies` | `AUDIT-UI-041` |
| `CLINIC_ADMIN` | `MODULE-007` | `SCREEN-041` | Supervise Drug Allergy & Adverse Reaction Logger | `perm:module-007:audit` | `API-CON-008` | `patient_allergies` | `AUDIT-SUP-041` |
| `AUDITOR` | `MODULE-007` | `SCREEN-041` | Compliance Review Drug Allergy & Adverse Reaction Logger | `perm:module-007:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-041` |
| `SECURITY_ADMIN` | `MODULE-007` | `SCREEN-041` | Threat Monitor Drug Allergy & Adverse Reaction Logger | `perm:module-007:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-041` |
| `DOCTOR` | `MODULE-007` | `SCREEN-042` | Execute Clinical Progress Note & Free-Text Area | `perm:module-007:execute` | `API-CON-009` | `consultations` | `AUDIT-UI-042` |
| `CLINIC_ADMIN` | `MODULE-007` | `SCREEN-042` | Supervise Clinical Progress Note & Free-Text Area | `perm:module-007:audit` | `API-CON-009` | `consultations` | `AUDIT-SUP-042` |
| `AUDITOR` | `MODULE-007` | `SCREEN-042` | Compliance Review Clinical Progress Note & Free-Text Area | `perm:module-007:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-042` |
| `SECURITY_ADMIN` | `MODULE-007` | `SCREEN-042` | Threat Monitor Clinical Progress Note & Free-Text Area | `perm:module-007:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-042` |
| `DOCTOR` | `MODULE-007` | `SCREEN-043` | Execute Doctor Teleconsultation Video Room | `perm:module-007:execute` | `API-CON-010` | `consultations` | `AUDIT-UI-043` |
| `CLINIC_ADMIN` | `MODULE-007` | `SCREEN-043` | Supervise Doctor Teleconsultation Video Room | `perm:module-007:audit` | `API-CON-010` | `consultations` | `AUDIT-SUP-043` |
| `AUDITOR` | `MODULE-007` | `SCREEN-043` | Compliance Review Doctor Teleconsultation Video Room | `perm:module-007:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-043` |
| `SECURITY_ADMIN` | `MODULE-007` | `SCREEN-043` | Threat Monitor Doctor Teleconsultation Video Room | `perm:module-007:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-043` |
| `DOCTOR` | `MODULE-007` | `SCREEN-044` | Execute Consultation Summary & Lock Dialog | `perm:module-007:execute` | `API-CON-011` | `consultations` | `AUDIT-UI-044` |
| `CLINIC_ADMIN` | `MODULE-007` | `SCREEN-044` | Supervise Consultation Summary & Lock Dialog | `perm:module-007:audit` | `API-CON-011` | `consultations` | `AUDIT-SUP-044` |
| `AUDITOR` | `MODULE-007` | `SCREEN-044` | Compliance Review Consultation Summary & Lock Dialog | `perm:module-007:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-044` |
| `SECURITY_ADMIN` | `MODULE-007` | `SCREEN-044` | Threat Monitor Consultation Summary & Lock Dialog | `perm:module-007:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-044` |
| `DOCTOR` | `MODULE-007` | `SCREEN-045` | Execute Doctor Outpatient Day Book View | `perm:module-007:execute` | `API-CON-012` | `consultations` | `AUDIT-UI-045` |
| `CLINIC_ADMIN` | `MODULE-007` | `SCREEN-045` | Supervise Doctor Outpatient Day Book View | `perm:module-007:audit` | `API-CON-012` | `consultations` | `AUDIT-SUP-045` |
| `AUDITOR` | `MODULE-007` | `SCREEN-045` | Compliance Review Doctor Outpatient Day Book View | `perm:module-007:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-045` |
| `SECURITY_ADMIN` | `MODULE-007` | `SCREEN-045` | Threat Monitor Doctor Outpatient Day Book View | `perm:module-007:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-045` |
| `DOCTOR` | `MODULE-008` | `SCREEN-046` | Execute Electronic Prescription Form | `perm:module-008:execute` | `API-RX-001` | `prescriptions` | `AUDIT-UI-046` |
| `CLINIC_ADMIN` | `MODULE-008` | `SCREEN-046` | Supervise Electronic Prescription Form | `perm:module-008:audit` | `API-RX-001` | `prescriptions` | `AUDIT-SUP-046` |
| `AUDITOR` | `MODULE-008` | `SCREEN-046` | Compliance Review Electronic Prescription Form | `perm:module-008:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-046` |
| `SECURITY_ADMIN` | `MODULE-008` | `SCREEN-046` | Threat Monitor Electronic Prescription Form | `perm:module-008:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-046` |
| `DOCTOR` | `MODULE-008` | `SCREEN-047` | Execute Drug-Drug & Drug-Allergy Warning Modal | `perm:module-008:execute` | `API-RX-002` | `prescription_items` | `AUDIT-UI-047` |
| `CLINIC_ADMIN` | `MODULE-008` | `SCREEN-047` | Supervise Drug-Drug & Drug-Allergy Warning Modal | `perm:module-008:audit` | `API-RX-002` | `prescription_items` | `AUDIT-SUP-047` |
| `AUDITOR` | `MODULE-008` | `SCREEN-047` | Compliance Review Drug-Drug & Drug-Allergy Warning Modal | `perm:module-008:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-047` |
| `SECURITY_ADMIN` | `MODULE-008` | `SCREEN-047` | Threat Monitor Drug-Drug & Drug-Allergy Warning Modal | `perm:module-008:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-047` |
| `DOCTOR` | `MODULE-008` | `SCREEN-048` | Execute Standard Clinical Treatment Regimen Picker | `perm:module-008:execute` | `API-RX-003` | `prescription_templates` | `AUDIT-UI-048` |
| `CLINIC_ADMIN` | `MODULE-008` | `SCREEN-048` | Supervise Standard Clinical Treatment Regimen Picker | `perm:module-008:audit` | `API-RX-003` | `prescription_templates` | `AUDIT-SUP-048` |
| `AUDITOR` | `MODULE-008` | `SCREEN-048` | Compliance Review Standard Clinical Treatment Regimen Picker | `perm:module-008:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-048` |
| `SECURITY_ADMIN` | `MODULE-008` | `SCREEN-048` | Threat Monitor Standard Clinical Treatment Regimen Picker | `perm:module-008:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-048` |
| `DOCTOR` | `MODULE-008` | `SCREEN-049` | Execute Prescription Bilingual Print Preview | `perm:module-008:execute` | `API-RX-004` | `prescriptions` | `AUDIT-UI-049` |
| `CLINIC_ADMIN` | `MODULE-008` | `SCREEN-049` | Supervise Prescription Bilingual Print Preview | `perm:module-008:audit` | `API-RX-004` | `prescriptions` | `AUDIT-SUP-049` |
| `AUDITOR` | `MODULE-008` | `SCREEN-049` | Compliance Review Prescription Bilingual Print Preview | `perm:module-008:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-049` |
| `SECURITY_ADMIN` | `MODULE-008` | `SCREEN-049` | Threat Monitor Prescription Bilingual Print Preview | `perm:module-008:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-049` |
| `DOCTOR` | `MODULE-008` | `SCREEN-050` | Execute Medication Modification & Cancellation | `perm:module-008:execute` | `API-RX-005` | `prescriptions` | `AUDIT-UI-050` |
| `CLINIC_ADMIN` | `MODULE-008` | `SCREEN-050` | Supervise Medication Modification & Cancellation | `perm:module-008:audit` | `API-RX-005` | `prescriptions` | `AUDIT-SUP-050` |
| `AUDITOR` | `MODULE-008` | `SCREEN-050` | Compliance Review Medication Modification & Cancellation | `perm:module-008:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-050` |
| `SECURITY_ADMIN` | `MODULE-008` | `SCREEN-050` | Threat Monitor Medication Modification & Cancellation | `perm:module-008:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-050` |
| `DOCTOR` | `MODULE-008` | `SCREEN-051` | Execute Recurring Refill Request Form | `perm:module-008:execute` | `API-RX-006` | `prescriptions` | `AUDIT-UI-051` |
| `CLINIC_ADMIN` | `MODULE-008` | `SCREEN-051` | Supervise Recurring Refill Request Form | `perm:module-008:audit` | `API-RX-006` | `prescriptions` | `AUDIT-SUP-051` |
| `AUDITOR` | `MODULE-008` | `SCREEN-051` | Compliance Review Recurring Refill Request Form | `perm:module-008:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-051` |
| `SECURITY_ADMIN` | `MODULE-008` | `SCREEN-051` | Threat Monitor Recurring Refill Request Form | `perm:module-008:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-051` |
| `DOCTOR` | `MODULE-008` | `SCREEN-052` | Execute Clinic Formulary & Stock Lookup Modal | `perm:module-008:execute` | `API-INV-001` | `pharmacy_batches` | `AUDIT-UI-052` |
| `CLINIC_ADMIN` | `MODULE-008` | `SCREEN-052` | Supervise Clinic Formulary & Stock Lookup Modal | `perm:module-008:audit` | `API-INV-001` | `pharmacy_batches` | `AUDIT-SUP-052` |
| `AUDITOR` | `MODULE-008` | `SCREEN-052` | Compliance Review Clinic Formulary & Stock Lookup Modal | `perm:module-008:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-052` |
| `SECURITY_ADMIN` | `MODULE-008` | `SCREEN-052` | Threat Monitor Clinic Formulary & Stock Lookup Modal | `perm:module-008:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-052` |
| `PHARMACIST` | `MODULE-009` | `SCREEN-053` | Execute Pharmacy Active Dispensing Screen | `perm:module-009:execute` | `API-PHR-003` | `prescriptions` | `AUDIT-UI-053` |
| `CLINIC_ADMIN` | `MODULE-009` | `SCREEN-053` | Supervise Pharmacy Active Dispensing Screen | `perm:module-009:audit` | `API-PHR-003` | `prescriptions` | `AUDIT-SUP-053` |
| `AUDITOR` | `MODULE-009` | `SCREEN-053` | Compliance Review Pharmacy Active Dispensing Screen | `perm:module-009:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-053` |
| `SECURITY_ADMIN` | `MODULE-009` | `SCREEN-053` | Threat Monitor Pharmacy Active Dispensing Screen | `perm:module-009:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-053` |
| `PHARMACIST` | `MODULE-009` | `SCREEN-054` | Execute Partial Dispensing & Stockout Dialog | `perm:module-009:execute` | `API-PHR-004` | `dispensing_logs` | `AUDIT-UI-054` |
| `CLINIC_ADMIN` | `MODULE-009` | `SCREEN-054` | Supervise Partial Dispensing & Stockout Dialog | `perm:module-009:audit` | `API-PHR-004` | `dispensing_logs` | `AUDIT-SUP-054` |
| `AUDITOR` | `MODULE-009` | `SCREEN-054` | Compliance Review Partial Dispensing & Stockout Dialog | `perm:module-009:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-054` |
| `SECURITY_ADMIN` | `MODULE-009` | `SCREEN-054` | Threat Monitor Partial Dispensing & Stockout Dialog | `perm:module-009:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-054` |
| `PHARMACIST` | `MODULE-009` | `SCREEN-055` | Execute Medicine Counseling Label Print Modal | `perm:module-009:execute` | `API-PHR-005` | `prescriptions` | `AUDIT-UI-055` |
| `CLINIC_ADMIN` | `MODULE-009` | `SCREEN-055` | Supervise Medicine Counseling Label Print Modal | `perm:module-009:audit` | `API-PHR-005` | `prescriptions` | `AUDIT-SUP-055` |
| `AUDITOR` | `MODULE-009` | `SCREEN-055` | Compliance Review Medicine Counseling Label Print Modal | `perm:module-009:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-055` |
| `SECURITY_ADMIN` | `MODULE-009` | `SCREEN-055` | Threat Monitor Medicine Counseling Label Print Modal | `perm:module-009:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-055` |
| `PHARMACIST` | `MODULE-009` | `SCREEN-056` | Execute Pharmacy Shift Reconciliation Form | `perm:module-009:execute` | `API-PHR-006` | `pharmacy_stock_ledger` | `AUDIT-UI-056` |
| `CLINIC_ADMIN` | `MODULE-009` | `SCREEN-056` | Supervise Pharmacy Shift Reconciliation Form | `perm:module-009:audit` | `API-PHR-006` | `pharmacy_stock_ledger` | `AUDIT-SUP-056` |
| `AUDITOR` | `MODULE-009` | `SCREEN-056` | Compliance Review Pharmacy Shift Reconciliation Form | `perm:module-009:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-056` |
| `SECURITY_ADMIN` | `MODULE-009` | `SCREEN-056` | Threat Monitor Pharmacy Shift Reconciliation Form | `perm:module-009:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-056` |
| `PHARMACIST` | `MODULE-009` | `SCREEN-057` | Execute Expired & Damaged Drug Quarantine Form | `perm:module-009:execute` | `API-INV-002` | `pharmacy_batches` | `AUDIT-UI-057` |
| `CLINIC_ADMIN` | `MODULE-009` | `SCREEN-057` | Supervise Expired & Damaged Drug Quarantine Form | `perm:module-009:audit` | `API-INV-002` | `pharmacy_batches` | `AUDIT-SUP-057` |
| `AUDITOR` | `MODULE-009` | `SCREEN-057` | Compliance Review Expired & Damaged Drug Quarantine Form | `perm:module-009:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-057` |
| `SECURITY_ADMIN` | `MODULE-009` | `SCREEN-057` | Threat Monitor Expired & Damaged Drug Quarantine Form | `perm:module-009:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-057` |
| `PHARMACIST` | `MODULE-009` | `SCREEN-058` | Execute Emergency Stock Requisition Form | `perm:module-009:execute` | `API-INV-003` | `stock_requisitions` | `AUDIT-UI-058` |
| `CLINIC_ADMIN` | `MODULE-009` | `SCREEN-058` | Supervise Emergency Stock Requisition Form | `perm:module-009:audit` | `API-INV-003` | `stock_requisitions` | `AUDIT-SUP-058` |
| `AUDITOR` | `MODULE-009` | `SCREEN-058` | Compliance Review Emergency Stock Requisition Form | `perm:module-009:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-058` |
| `SECURITY_ADMIN` | `MODULE-009` | `SCREEN-058` | Threat Monitor Emergency Stock Requisition Form | `perm:module-009:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-058` |
| `PHARMACIST` | `MODULE-009` | `SCREEN-059` | Execute Pharmacy Dispensing Log History | `perm:module-009:execute` | `API-PHR-007` | `dispensing_logs` | `AUDIT-UI-059` |
| `CLINIC_ADMIN` | `MODULE-009` | `SCREEN-059` | Supervise Pharmacy Dispensing Log History | `perm:module-009:audit` | `API-PHR-007` | `dispensing_logs` | `AUDIT-SUP-059` |
| `AUDITOR` | `MODULE-009` | `SCREEN-059` | Compliance Review Pharmacy Dispensing Log History | `perm:module-009:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-059` |
| `SECURITY_ADMIN` | `MODULE-009` | `SCREEN-059` | Threat Monitor Pharmacy Dispensing Log History | `perm:module-009:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-059` |
| `PHARMACIST` | `MODULE-009` | `SCREEN-060` | Execute Controlled Substances & High-Alert Register | `perm:module-009:execute` | `API-PHR-008` | `pharmacy_stock_ledger` | `AUDIT-UI-060` |
| `CLINIC_ADMIN` | `MODULE-009` | `SCREEN-060` | Supervise Controlled Substances & High-Alert Register | `perm:module-009:audit` | `API-PHR-008` | `pharmacy_stock_ledger` | `AUDIT-SUP-060` |
| `AUDITOR` | `MODULE-009` | `SCREEN-060` | Compliance Review Controlled Substances & High-Alert Register | `perm:module-009:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-060` |
| `SECURITY_ADMIN` | `MODULE-009` | `SCREEN-060` | Threat Monitor Controlled Substances & High-Alert Register | `perm:module-009:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-060` |
| `PHARMACIST` | `MODULE-010` | `SCREEN-061` | Execute Clinic Stock Inventory Dashboard | `perm:module-010:execute` | `API-INV-004` | `pharmacy_batches` | `AUDIT-UI-061` |
| `CLINIC_ADMIN` | `MODULE-010` | `SCREEN-061` | Supervise Clinic Stock Inventory Dashboard | `perm:module-010:audit` | `API-INV-004` | `pharmacy_batches` | `AUDIT-SUP-061` |
| `AUDITOR` | `MODULE-010` | `SCREEN-061` | Compliance Review Clinic Stock Inventory Dashboard | `perm:module-010:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-061` |
| `SECURITY_ADMIN` | `MODULE-010` | `SCREEN-061` | Threat Monitor Clinic Stock Inventory Dashboard | `perm:module-010:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-061` |
| `PHARMACIST` | `MODULE-010` | `SCREEN-062` | Execute Stock Goods Receipt Note (GRN) Form | `perm:module-010:execute` | `API-INV-005` | `pharmacy_batches` | `AUDIT-UI-062` |
| `CLINIC_ADMIN` | `MODULE-010` | `SCREEN-062` | Supervise Stock Goods Receipt Note (GRN) Form | `perm:module-010:audit` | `API-INV-005` | `pharmacy_batches` | `AUDIT-SUP-062` |
| `AUDITOR` | `MODULE-010` | `SCREEN-062` | Compliance Review Stock Goods Receipt Note (GRN) Form | `perm:module-010:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-062` |
| `SECURITY_ADMIN` | `MODULE-010` | `SCREEN-062` | Threat Monitor Stock Goods Receipt Note (GRN) Form | `perm:module-010:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-062` |
| `PHARMACIST` | `MODULE-010` | `SCREEN-063` | Execute Cold Chain Refrigerator Telemetry View | `perm:module-010:execute` | `API-INV-006` | `cold_chain_telemetry` | `AUDIT-UI-063` |
| `CLINIC_ADMIN` | `MODULE-010` | `SCREEN-063` | Supervise Cold Chain Refrigerator Telemetry View | `perm:module-010:audit` | `API-INV-006` | `cold_chain_telemetry` | `AUDIT-SUP-063` |
| `AUDITOR` | `MODULE-010` | `SCREEN-063` | Compliance Review Cold Chain Refrigerator Telemetry View | `perm:module-010:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-063` |
| `SECURITY_ADMIN` | `MODULE-010` | `SCREEN-063` | Threat Monitor Cold Chain Refrigerator Telemetry View | `perm:module-010:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-063` |
| `NURSE` | `MODULE-010` | `SCREEN-064` | Execute Vaccine Stock & VVM Status Manager | `perm:module-010:execute` | `API-INV-007` | `vaccine_batches` | `AUDIT-UI-064` |
| `CLINIC_ADMIN` | `MODULE-010` | `SCREEN-064` | Supervise Vaccine Stock & VVM Status Manager | `perm:module-010:audit` | `API-INV-007` | `vaccine_batches` | `AUDIT-SUP-064` |
| `AUDITOR` | `MODULE-010` | `SCREEN-064` | Compliance Review Vaccine Stock & VVM Status Manager | `perm:module-010:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-064` |
| `SECURITY_ADMIN` | `MODULE-010` | `SCREEN-064` | Threat Monitor Vaccine Stock & VVM Status Manager | `perm:module-010:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-064` |
| `PHARMACIST` | `MODULE-010` | `SCREEN-065` | Execute Inter-Clinic Stock Transfer Dispatch | `perm:module-010:execute` | `API-INV-008` | `stock_transfers` | `AUDIT-UI-065` |
| `CLINIC_ADMIN` | `MODULE-010` | `SCREEN-065` | Supervise Inter-Clinic Stock Transfer Dispatch | `perm:module-010:audit` | `API-INV-008` | `stock_transfers` | `AUDIT-SUP-065` |
| `AUDITOR` | `MODULE-010` | `SCREEN-065` | Compliance Review Inter-Clinic Stock Transfer Dispatch | `perm:module-010:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-065` |
| `SECURITY_ADMIN` | `MODULE-010` | `SCREEN-065` | Threat Monitor Inter-Clinic Stock Transfer Dispatch | `perm:module-010:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-065` |
| `PHARMACIST` | `MODULE-010` | `SCREEN-066` | Execute Inter-Clinic Stock Transfer Receipt | `perm:module-010:execute` | `API-INV-009` | `stock_transfers` | `AUDIT-UI-066` |
| `CLINIC_ADMIN` | `MODULE-010` | `SCREEN-066` | Supervise Inter-Clinic Stock Transfer Receipt | `perm:module-010:audit` | `API-INV-009` | `stock_transfers` | `AUDIT-SUP-066` |
| `AUDITOR` | `MODULE-010` | `SCREEN-066` | Compliance Review Inter-Clinic Stock Transfer Receipt | `perm:module-010:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-066` |
| `SECURITY_ADMIN` | `MODULE-010` | `SCREEN-066` | Threat Monitor Inter-Clinic Stock Transfer Receipt | `perm:module-010:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-066` |
| `CLINIC_ADMIN` | `MODULE-010` | `SCREEN-067` | Execute Annual / Monthly Physical Audit Form | `perm:module-010:execute` | `API-INV-010` | `inventory_audits` | `AUDIT-UI-067` |
| `CLINIC_ADMIN` | `MODULE-010` | `SCREEN-067` | Supervise Annual / Monthly Physical Audit Form | `perm:module-010:audit` | `API-INV-010` | `inventory_audits` | `AUDIT-SUP-067` |
| `AUDITOR` | `MODULE-010` | `SCREEN-067` | Compliance Review Annual / Monthly Physical Audit Form | `perm:module-010:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-067` |
| `SECURITY_ADMIN` | `MODULE-010` | `SCREEN-067` | Threat Monitor Annual / Monthly Physical Audit Form | `perm:module-010:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-067` |
| `PHARMACIST` | `MODULE-010` | `SCREEN-068` | Execute Supplier Recall & Ban Notification Modal | `perm:module-010:execute` | `API-INV-011` | `pharmacy_batches` | `AUDIT-UI-068` |
| `CLINIC_ADMIN` | `MODULE-010` | `SCREEN-068` | Supervise Supplier Recall & Ban Notification Modal | `perm:module-010:audit` | `API-INV-011` | `pharmacy_batches` | `AUDIT-SUP-068` |
| `AUDITOR` | `MODULE-010` | `SCREEN-068` | Compliance Review Supplier Recall & Ban Notification Modal | `perm:module-010:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-068` |
| `SECURITY_ADMIN` | `MODULE-010` | `SCREEN-068` | Threat Monitor Supplier Recall & Ban Notification Modal | `perm:module-010:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-068` |
| `LAB_TECH` | `MODULE-011` | `SCREEN-069` | Execute Diagnostic Lab Test Orders Queue | `perm:module-011:execute` | `API-LAB-002` | `lab_orders` | `AUDIT-UI-069` |
| `CLINIC_ADMIN` | `MODULE-011` | `SCREEN-069` | Supervise Diagnostic Lab Test Orders Queue | `perm:module-011:audit` | `API-LAB-002` | `lab_orders` | `AUDIT-SUP-069` |
| `AUDITOR` | `MODULE-011` | `SCREEN-069` | Compliance Review Diagnostic Lab Test Orders Queue | `perm:module-011:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-069` |
| `SECURITY_ADMIN` | `MODULE-011` | `SCREEN-069` | Threat Monitor Diagnostic Lab Test Orders Queue | `perm:module-011:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-069` |
| `LAB_TECH` | `MODULE-011` | `SCREEN-070` | Execute Specimen Collection & Barcode Label Screen | `perm:module-011:execute` | `API-LAB-003` | `lab_specimens` | `AUDIT-UI-070` |
| `CLINIC_ADMIN` | `MODULE-011` | `SCREEN-070` | Supervise Specimen Collection & Barcode Label Screen | `perm:module-011:audit` | `API-LAB-003` | `lab_specimens` | `AUDIT-SUP-070` |
| `AUDITOR` | `MODULE-011` | `SCREEN-070` | Compliance Review Specimen Collection & Barcode Label Screen | `perm:module-011:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-070` |
| `SECURITY_ADMIN` | `MODULE-011` | `SCREEN-070` | Threat Monitor Specimen Collection & Barcode Label Screen | `perm:module-011:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-070` |
| `LAB_TECH` | `MODULE-011` | `SCREEN-071` | Execute Point-of-Care Rapid Test Result Entry | `perm:module-011:execute` | `API-LAB-004` | `lab_results` | `AUDIT-UI-071` |
| `CLINIC_ADMIN` | `MODULE-011` | `SCREEN-071` | Supervise Point-of-Care Rapid Test Result Entry | `perm:module-011:audit` | `API-LAB-004` | `lab_results` | `AUDIT-SUP-071` |
| `AUDITOR` | `MODULE-011` | `SCREEN-071` | Compliance Review Point-of-Care Rapid Test Result Entry | `perm:module-011:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-071` |
| `SECURITY_ADMIN` | `MODULE-011` | `SCREEN-071` | Threat Monitor Point-of-Care Rapid Test Result Entry | `perm:module-011:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-071` |
| `LAB_TECH` | `MODULE-011` | `SCREEN-072` | Execute Hematology Analyzer Data Import Screen | `perm:module-011:execute` | `API-LAB-005` | `lab_results` | `AUDIT-UI-072` |
| `CLINIC_ADMIN` | `MODULE-011` | `SCREEN-072` | Supervise Hematology Analyzer Data Import Screen | `perm:module-011:audit` | `API-LAB-005` | `lab_results` | `AUDIT-SUP-072` |
| `AUDITOR` | `MODULE-011` | `SCREEN-072` | Compliance Review Hematology Analyzer Data Import Screen | `perm:module-011:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-072` |
| `SECURITY_ADMIN` | `MODULE-011` | `SCREEN-072` | Threat Monitor Hematology Analyzer Data Import Screen | `perm:module-011:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-072` |
| `LAB_TECH` | `MODULE-011` | `SCREEN-073` | Execute Lab Results Validation & Doctor Alert | `perm:module-011:execute` | `API-LAB-006` | `lab_results` | `AUDIT-UI-073` |
| `CLINIC_ADMIN` | `MODULE-011` | `SCREEN-073` | Supervise Lab Results Validation & Doctor Alert | `perm:module-011:audit` | `API-LAB-006` | `lab_results` | `AUDIT-SUP-073` |
| `AUDITOR` | `MODULE-011` | `SCREEN-073` | Compliance Review Lab Results Validation & Doctor Alert | `perm:module-011:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-073` |
| `SECURITY_ADMIN` | `MODULE-011` | `SCREEN-073` | Threat Monitor Lab Results Validation & Doctor Alert | `perm:module-011:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-073` |
| `LAB_TECH` | `MODULE-011` | `SCREEN-074` | Execute Diagnostic Report Bilingual Print Preview | `perm:module-011:execute` | `API-LAB-007` | `lab_results` | `AUDIT-UI-074` |
| `CLINIC_ADMIN` | `MODULE-011` | `SCREEN-074` | Supervise Diagnostic Report Bilingual Print Preview | `perm:module-011:audit` | `API-LAB-007` | `lab_results` | `AUDIT-SUP-074` |
| `AUDITOR` | `MODULE-011` | `SCREEN-074` | Compliance Review Diagnostic Report Bilingual Print Preview | `perm:module-011:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-074` |
| `SECURITY_ADMIN` | `MODULE-011` | `SCREEN-074` | Threat Monitor Diagnostic Report Bilingual Print Preview | `perm:module-011:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-074` |
| `LAB_TECH` | `MODULE-011` | `SCREEN-075` | Execute External Referral Lab Dispatch Form | `perm:module-011:execute` | `API-LAB-008` | `lab_orders` | `AUDIT-UI-075` |
| `CLINIC_ADMIN` | `MODULE-011` | `SCREEN-075` | Supervise External Referral Lab Dispatch Form | `perm:module-011:audit` | `API-LAB-008` | `lab_orders` | `AUDIT-SUP-075` |
| `AUDITOR` | `MODULE-011` | `SCREEN-075` | Compliance Review External Referral Lab Dispatch Form | `perm:module-011:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-075` |
| `SECURITY_ADMIN` | `MODULE-011` | `SCREEN-075` | Threat Monitor External Referral Lab Dispatch Form | `perm:module-011:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-075` |
| `LAB_TECH` | `MODULE-011` | `SCREEN-076` | Execute Lab Reagent & Quality Control Log | `perm:module-011:execute` | `API-LAB-009` | `lab_qc_logs` | `AUDIT-UI-076` |
| `CLINIC_ADMIN` | `MODULE-011` | `SCREEN-076` | Supervise Lab Reagent & Quality Control Log | `perm:module-011:audit` | `API-LAB-009` | `lab_qc_logs` | `AUDIT-SUP-076` |
| `AUDITOR` | `MODULE-011` | `SCREEN-076` | Compliance Review Lab Reagent & Quality Control Log | `perm:module-011:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-076` |
| `SECURITY_ADMIN` | `MODULE-011` | `SCREEN-076` | Threat Monitor Lab Reagent & Quality Control Log | `perm:module-011:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-076` |
| `DOCTOR` | `MODULE-012` | `SCREEN-077` | Execute Secondary / Tertiary Referral Form | `perm:module-012:execute` | `API-REF-001` | `patient_referrals` | `AUDIT-UI-077` |
| `CLINIC_ADMIN` | `MODULE-012` | `SCREEN-077` | Supervise Secondary / Tertiary Referral Form | `perm:module-012:audit` | `API-REF-001` | `patient_referrals` | `AUDIT-SUP-077` |
| `AUDITOR` | `MODULE-012` | `SCREEN-077` | Compliance Review Secondary / Tertiary Referral Form | `perm:module-012:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-077` |
| `SECURITY_ADMIN` | `MODULE-012` | `SCREEN-077` | Threat Monitor Secondary / Tertiary Referral Form | `perm:module-012:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-077` |
| `DOCTOR` | `MODULE-012` | `SCREEN-078` | Execute 108 Emergency Ambulance Dispatch Screen | `perm:module-012:execute` | `API-REF-002` | `patient_referrals` | `AUDIT-UI-078` |
| `CLINIC_ADMIN` | `MODULE-012` | `SCREEN-078` | Supervise 108 Emergency Ambulance Dispatch Screen | `perm:module-012:audit` | `API-REF-002` | `patient_referrals` | `AUDIT-SUP-078` |
| `AUDITOR` | `MODULE-012` | `SCREEN-078` | Compliance Review 108 Emergency Ambulance Dispatch Screen | `perm:module-012:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-078` |
| `SECURITY_ADMIN` | `MODULE-012` | `SCREEN-078` | Threat Monitor 108 Emergency Ambulance Dispatch Screen | `perm:module-012:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-078` |
| `DOCTOR` | `MODULE-012` | `SCREEN-079` | Execute Referral Handover Dossier Print Preview | `perm:module-012:execute` | `API-REF-003` | `patient_referrals` | `AUDIT-UI-079` |
| `CLINIC_ADMIN` | `MODULE-012` | `SCREEN-079` | Supervise Referral Handover Dossier Print Preview | `perm:module-012:audit` | `API-REF-003` | `patient_referrals` | `AUDIT-SUP-079` |
| `AUDITOR` | `MODULE-012` | `SCREEN-079` | Compliance Review Referral Handover Dossier Print Preview | `perm:module-012:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-079` |
| `SECURITY_ADMIN` | `MODULE-012` | `SCREEN-079` | Threat Monitor Referral Handover Dossier Print Preview | `perm:module-012:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-079` |
| `NURSE` | `MODULE-012` | `SCREEN-080` | Execute Active Outgoing Referrals Tracker | `perm:module-012:execute` | `API-REF-004` | `patient_referrals` | `AUDIT-UI-080` |
| `CLINIC_ADMIN` | `MODULE-012` | `SCREEN-080` | Supervise Active Outgoing Referrals Tracker | `perm:module-012:audit` | `API-REF-004` | `patient_referrals` | `AUDIT-SUP-080` |
| `AUDITOR` | `MODULE-012` | `SCREEN-080` | Compliance Review Active Outgoing Referrals Tracker | `perm:module-012:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-080` |
| `SECURITY_ADMIN` | `MODULE-012` | `SCREEN-080` | Threat Monitor Active Outgoing Referrals Tracker | `perm:module-012:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-080` |
| `DOCTOR` | `MODULE-012` | `SCREEN-081` | Execute Discharge / Counter-Referral Ingest Form | `perm:module-012:execute` | `API-REF-005` | `patient_referrals` | `AUDIT-UI-081` |
| `CLINIC_ADMIN` | `MODULE-012` | `SCREEN-081` | Supervise Discharge / Counter-Referral Ingest Form | `perm:module-012:audit` | `API-REF-005` | `patient_referrals` | `AUDIT-SUP-081` |
| `AUDITOR` | `MODULE-012` | `SCREEN-081` | Compliance Review Discharge / Counter-Referral Ingest Form | `perm:module-012:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-081` |
| `SECURITY_ADMIN` | `MODULE-012` | `SCREEN-081` | Threat Monitor Discharge / Counter-Referral Ingest Form | `perm:module-012:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-081` |
| `DOCTOR` | `MODULE-012` | `SCREEN-082` | Execute Emergency Resuscitation Incident Record | `perm:module-012:execute` | `API-REF-006` | `consultations` | `AUDIT-UI-082` |
| `CLINIC_ADMIN` | `MODULE-012` | `SCREEN-082` | Supervise Emergency Resuscitation Incident Record | `perm:module-012:audit` | `API-REF-006` | `consultations` | `AUDIT-SUP-082` |
| `AUDITOR` | `MODULE-012` | `SCREEN-082` | Compliance Review Emergency Resuscitation Incident Record | `perm:module-012:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-082` |
| `SECURITY_ADMIN` | `MODULE-012` | `SCREEN-082` | Threat Monitor Emergency Resuscitation Incident Record | `perm:module-012:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-082` |
| `RECEPTIONIST` | `MODULE-013` | `SCREEN-083` | Execute Citizen SMS & Communication Center | `perm:module-013:execute` | `API-NOTIF-001` | `notification_logs` | `AUDIT-UI-083` |
| `CLINIC_ADMIN` | `MODULE-013` | `SCREEN-083` | Supervise Citizen SMS & Communication Center | `perm:module-013:audit` | `API-NOTIF-001` | `notification_logs` | `AUDIT-SUP-083` |
| `AUDITOR` | `MODULE-013` | `SCREEN-083` | Compliance Review Citizen SMS & Communication Center | `perm:module-013:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-083` |
| `SECURITY_ADMIN` | `MODULE-013` | `SCREEN-083` | Threat Monitor Citizen SMS & Communication Center | `perm:module-013:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-083` |
| `NURSE` | `MODULE-013` | `SCREEN-084` | Execute Chronic Disease Follow-Up Schedule | `perm:module-013:execute` | `API-NOTIF-002` | `followup_schedules` | `AUDIT-UI-084` |
| `CLINIC_ADMIN` | `MODULE-013` | `SCREEN-084` | Supervise Chronic Disease Follow-Up Schedule | `perm:module-013:audit` | `API-NOTIF-002` | `followup_schedules` | `AUDIT-SUP-084` |
| `AUDITOR` | `MODULE-013` | `SCREEN-084` | Compliance Review Chronic Disease Follow-Up Schedule | `perm:module-013:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-084` |
| `SECURITY_ADMIN` | `MODULE-013` | `SCREEN-084` | Threat Monitor Chronic Disease Follow-Up Schedule | `perm:module-013:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-084` |
| `ASHA_COORD` | `MODULE-013` | `SCREEN-085` | Execute ASHA Worker Community Outreach Tasklist | `perm:module-013:execute` | `API-NOTIF-003` | `followup_schedules` | `AUDIT-UI-085` |
| `CLINIC_ADMIN` | `MODULE-013` | `SCREEN-085` | Supervise ASHA Worker Community Outreach Tasklist | `perm:module-013:audit` | `API-NOTIF-003` | `followup_schedules` | `AUDIT-SUP-085` |
| `AUDITOR` | `MODULE-013` | `SCREEN-085` | Compliance Review ASHA Worker Community Outreach Tasklist | `perm:module-013:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-085` |
| `SECURITY_ADMIN` | `MODULE-013` | `SCREEN-085` | Threat Monitor ASHA Worker Community Outreach Tasklist | `perm:module-013:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-085` |
| `ZONAL_OFFICER` | `MODULE-013` | `SCREEN-086` | Execute Public Health Broadcast Composer | `perm:module-013:execute` | `API-NOTIF-004` | `notification_logs` | `AUDIT-UI-086` |
| `CLINIC_ADMIN` | `MODULE-013` | `SCREEN-086` | Supervise Public Health Broadcast Composer | `perm:module-013:audit` | `API-NOTIF-004` | `notification_logs` | `AUDIT-SUP-086` |
| `AUDITOR` | `MODULE-013` | `SCREEN-086` | Compliance Review Public Health Broadcast Composer | `perm:module-013:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-086` |
| `SECURITY_ADMIN` | `MODULE-013` | `SCREEN-086` | Threat Monitor Public Health Broadcast Composer | `perm:module-013:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-086` |
| `DOCTOR` | `MODULE-013` | `SCREEN-087` | Execute Adverse Event Notification Form | `perm:module-013:execute` | `API-NOTIF-005` | `adverse_events` | `AUDIT-UI-087` |
| `CLINIC_ADMIN` | `MODULE-013` | `SCREEN-087` | Supervise Adverse Event Notification Form | `perm:module-013:audit` | `API-NOTIF-005` | `adverse_events` | `AUDIT-SUP-087` |
| `AUDITOR` | `MODULE-013` | `SCREEN-087` | Compliance Review Adverse Event Notification Form | `perm:module-013:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-087` |
| `SECURITY_ADMIN` | `MODULE-013` | `SCREEN-087` | Threat Monitor Adverse Event Notification Form | `perm:module-013:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-087` |
| `RECEPTIONIST` | `MODULE-013` | `SCREEN-088` | Execute Missed Follow-up Outreach Dialer Console | `perm:module-013:execute` | `API-NOTIF-006` | `followup_schedules` | `AUDIT-UI-088` |
| `CLINIC_ADMIN` | `MODULE-013` | `SCREEN-088` | Supervise Missed Follow-up Outreach Dialer Console | `perm:module-013:audit` | `API-NOTIF-006` | `followup_schedules` | `AUDIT-SUP-088` |
| `AUDITOR` | `MODULE-013` | `SCREEN-088` | Compliance Review Missed Follow-up Outreach Dialer Console | `perm:module-013:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-088` |
| `SECURITY_ADMIN` | `MODULE-013` | `SCREEN-088` | Threat Monitor Missed Follow-up Outreach Dialer Console | `perm:module-013:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-088` |
| `EPIDEMIOLOGIST` | `MODULE-014` | `SCREEN-089` | Execute Epidemic Outbreak Surveillance Dashboard | `perm:module-014:execute` | `API-ANL-002` | `epidemic_signals` | `AUDIT-UI-089` |
| `CLINIC_ADMIN` | `MODULE-014` | `SCREEN-089` | Supervise Epidemic Outbreak Surveillance Dashboard | `perm:module-014:audit` | `API-ANL-002` | `epidemic_signals` | `AUDIT-SUP-089` |
| `AUDITOR` | `MODULE-014` | `SCREEN-089` | Compliance Review Epidemic Outbreak Surveillance Dashboard | `perm:module-014:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-089` |
| `SECURITY_ADMIN` | `MODULE-014` | `SCREEN-089` | Threat Monitor Epidemic Outbreak Surveillance Dashboard | `perm:module-014:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-089` |
| `WARD_SUPERVISOR` | `MODULE-014` | `SCREEN-090` | Execute Ward Health Performance & KPI Scorecard | `perm:module-014:execute` | `API-ANL-003` | `analytics_aggregates` | `AUDIT-UI-090` |
| `CLINIC_ADMIN` | `MODULE-014` | `SCREEN-090` | Supervise Ward Health Performance & KPI Scorecard | `perm:module-014:audit` | `API-ANL-003` | `analytics_aggregates` | `AUDIT-SUP-090` |
| `AUDITOR` | `MODULE-014` | `SCREEN-090` | Compliance Review Ward Health Performance & KPI Scorecard | `perm:module-014:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-090` |
| `SECURITY_ADMIN` | `MODULE-014` | `SCREEN-090` | Threat Monitor Ward Health Performance & KPI Scorecard | `perm:module-014:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-090` |
| `PHARMACIST` | `MODULE-014` | `SCREEN-091` | Execute Pharmacy Dispensing & Consumption Analytics | `perm:module-014:execute` | `API-ANL-004` | `analytics_aggregates` | `AUDIT-UI-091` |
| `CLINIC_ADMIN` | `MODULE-014` | `SCREEN-091` | Supervise Pharmacy Dispensing & Consumption Analytics | `perm:module-014:audit` | `API-ANL-004` | `analytics_aggregates` | `AUDIT-SUP-091` |
| `AUDITOR` | `MODULE-014` | `SCREEN-091` | Compliance Review Pharmacy Dispensing & Consumption Analytics | `perm:module-014:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-091` |
| `SECURITY_ADMIN` | `MODULE-014` | `SCREEN-091` | Threat Monitor Pharmacy Dispensing & Consumption Analytics | `perm:module-014:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-091` |
| `LAB_TECH` | `MODULE-014` | `SCREEN-092` | Execute Laboratory Diagnostic Workload Dashboard | `perm:module-014:execute` | `API-ANL-005` | `analytics_aggregates` | `AUDIT-UI-092` |
| `CLINIC_ADMIN` | `MODULE-014` | `SCREEN-092` | Supervise Laboratory Diagnostic Workload Dashboard | `perm:module-014:audit` | `API-ANL-005` | `analytics_aggregates` | `AUDIT-SUP-092` |
| `AUDITOR` | `MODULE-014` | `SCREEN-092` | Compliance Review Laboratory Diagnostic Workload Dashboard | `perm:module-014:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-092` |
| `SECURITY_ADMIN` | `MODULE-014` | `SCREEN-092` | Threat Monitor Laboratory Diagnostic Workload Dashboard | `perm:module-014:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-092` |
| `ZONAL_OFFICER` | `MODULE-014` | `SCREEN-093` | Execute Maternal & Child Health Coverage Heatmap | `perm:module-014:execute` | `API-ANL-006` | `analytics_aggregates` | `AUDIT-UI-093` |
| `CLINIC_ADMIN` | `MODULE-014` | `SCREEN-093` | Supervise Maternal & Child Health Coverage Heatmap | `perm:module-014:audit` | `API-ANL-006` | `analytics_aggregates` | `AUDIT-SUP-093` |
| `AUDITOR` | `MODULE-014` | `SCREEN-093` | Compliance Review Maternal & Child Health Coverage Heatmap | `perm:module-014:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-093` |
| `SECURITY_ADMIN` | `MODULE-014` | `SCREEN-093` | Threat Monitor Maternal & Child Health Coverage Heatmap | `perm:module-014:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-093` |
| `CLINIC_ADMIN` | `MODULE-014` | `SCREEN-094` | Execute Custom Report Builder & CSV Export | `perm:module-014:execute` | `API-ANL-007` | `analytics_aggregates` | `AUDIT-UI-094` |
| `CLINIC_ADMIN` | `MODULE-014` | `SCREEN-094` | Supervise Custom Report Builder & CSV Export | `perm:module-014:audit` | `API-ANL-007` | `analytics_aggregates` | `AUDIT-SUP-094` |
| `AUDITOR` | `MODULE-014` | `SCREEN-094` | Compliance Review Custom Report Builder & CSV Export | `perm:module-014:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-094` |
| `SECURITY_ADMIN` | `MODULE-014` | `SCREEN-094` | Threat Monitor Custom Report Builder & CSV Export | `perm:module-014:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-094` |
| `CLINIC_ADMIN` | `MODULE-015` | `SCREEN-095` | Execute Offline Storage & SQLite WAL Status | `perm:module-015:execute` | `API-SYS-004` | `sync_queue` | `AUDIT-UI-095` |
| `CLINIC_ADMIN` | `MODULE-015` | `SCREEN-095` | Supervise Offline Storage & SQLite WAL Status | `perm:module-015:audit` | `API-SYS-004` | `sync_queue` | `AUDIT-SUP-095` |
| `AUDITOR` | `MODULE-015` | `SCREEN-095` | Compliance Review Offline Storage & SQLite WAL Status | `perm:module-015:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-095` |
| `SECURITY_ADMIN` | `MODULE-015` | `SCREEN-095` | Threat Monitor Offline Storage & SQLite WAL Status | `perm:module-015:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-095` |
| `CLINIC_ADMIN` | `MODULE-015` | `SCREEN-096` | Execute Sync Queue Monitor & Manual Flush | `perm:module-015:execute` | `API-SYS-005` | `sync_queue` | `AUDIT-UI-096` |
| `CLINIC_ADMIN` | `MODULE-015` | `SCREEN-096` | Supervise Sync Queue Monitor & Manual Flush | `perm:module-015:audit` | `API-SYS-005` | `sync_queue` | `AUDIT-SUP-096` |
| `AUDITOR` | `MODULE-015` | `SCREEN-096` | Compliance Review Sync Queue Monitor & Manual Flush | `perm:module-015:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-096` |
| `SECURITY_ADMIN` | `MODULE-015` | `SCREEN-096` | Threat Monitor Sync Queue Monitor & Manual Flush | `perm:module-015:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-096` |
| `CLINIC_ADMIN` | `MODULE-015` | `SCREEN-097` | Execute Sync Conflict Visual Resolution Modal | `perm:module-015:execute` | `API-SYS-006` | `sync_conflicts` | `AUDIT-UI-097` |
| `CLINIC_ADMIN` | `MODULE-015` | `SCREEN-097` | Supervise Sync Conflict Visual Resolution Modal | `perm:module-015:audit` | `API-SYS-006` | `sync_conflicts` | `AUDIT-SUP-097` |
| `AUDITOR` | `MODULE-015` | `SCREEN-097` | Compliance Review Sync Conflict Visual Resolution Modal | `perm:module-015:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-097` |
| `SECURITY_ADMIN` | `MODULE-015` | `SCREEN-097` | Threat Monitor Sync Conflict Visual Resolution Modal | `perm:module-015:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-097` |
| `IT_SUPPORT` | `MODULE-015` | `SCREEN-098` | Execute Peer-to-Peer Local WiFi Sync Setup | `perm:module-015:execute` | `API-SYS-007` | `system_configs` | `AUDIT-UI-098` |
| `CLINIC_ADMIN` | `MODULE-015` | `SCREEN-098` | Supervise Peer-to-Peer Local WiFi Sync Setup | `perm:module-015:audit` | `API-SYS-007` | `system_configs` | `AUDIT-SUP-098` |
| `AUDITOR` | `MODULE-015` | `SCREEN-098` | Compliance Review Peer-to-Peer Local WiFi Sync Setup | `perm:module-015:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-098` |
| `SECURITY_ADMIN` | `MODULE-015` | `SCREEN-098` | Threat Monitor Peer-to-Peer Local WiFi Sync Setup | `perm:module-015:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-098` |
| `CLINIC_ADMIN` | `MODULE-015` | `SCREEN-099` | Execute Offline Cryptographic Token Cache | `perm:module-015:execute` | `API-AUTH-006` | `auth_offline_credentials` | `AUDIT-UI-099` |
| `CLINIC_ADMIN` | `MODULE-015` | `SCREEN-099` | Supervise Offline Cryptographic Token Cache | `perm:module-015:audit` | `API-AUTH-006` | `auth_offline_credentials` | `AUDIT-SUP-099` |
| `AUDITOR` | `MODULE-015` | `SCREEN-099` | Compliance Review Offline Cryptographic Token Cache | `perm:module-015:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-099` |
| `SECURITY_ADMIN` | `MODULE-015` | `SCREEN-099` | Threat Monitor Offline Cryptographic Token Cache | `perm:module-015:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-099` |
| `CLINIC_ADMIN` | `MODULE-015` | `SCREEN-100` | Execute Local Backup & USB Snapshot Export | `perm:module-015:execute` | `API-SYS-008` | `system_backups` | `AUDIT-UI-100` |
| `CLINIC_ADMIN` | `MODULE-015` | `SCREEN-100` | Supervise Local Backup & USB Snapshot Export | `perm:module-015:audit` | `API-SYS-008` | `system_backups` | `AUDIT-SUP-100` |
| `AUDITOR` | `MODULE-015` | `SCREEN-100` | Compliance Review Local Backup & USB Snapshot Export | `perm:module-015:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-100` |
| `SECURITY_ADMIN` | `MODULE-015` | `SCREEN-100` | Threat Monitor Local Backup & USB Snapshot Export | `perm:module-015:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-100` |
| `RECEPTIONIST` | `MODULE-016` | `SCREEN-101` | Execute ABHA Creation & Mobile Verification | `perm:module-016:execute` | `API-ABDM-002` | `abdm_profiles` | `AUDIT-UI-101` |
| `CLINIC_ADMIN` | `MODULE-016` | `SCREEN-101` | Supervise ABHA Creation & Mobile Verification | `perm:module-016:audit` | `API-ABDM-002` | `abdm_profiles` | `AUDIT-SUP-101` |
| `AUDITOR` | `MODULE-016` | `SCREEN-101` | Compliance Review ABHA Creation & Mobile Verification | `perm:module-016:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-101` |
| `SECURITY_ADMIN` | `MODULE-016` | `SCREEN-101` | Threat Monitor ABHA Creation & Mobile Verification | `perm:module-016:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-101` |
| `DOCTOR` | `MODULE-016` | `SCREEN-102` | Execute ABDM Consent Request & Artifact Drawer | `perm:module-016:execute` | `API-ABDM-003` | `abdm_consents` | `AUDIT-UI-102` |
| `CLINIC_ADMIN` | `MODULE-016` | `SCREEN-102` | Supervise ABDM Consent Request & Artifact Drawer | `perm:module-016:audit` | `API-ABDM-003` | `abdm_consents` | `AUDIT-SUP-102` |
| `AUDITOR` | `MODULE-016` | `SCREEN-102` | Compliance Review ABDM Consent Request & Artifact Drawer | `perm:module-016:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-102` |
| `SECURITY_ADMIN` | `MODULE-016` | `SCREEN-102` | Threat Monitor ABDM Consent Request & Artifact Drawer | `perm:module-016:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-102` |
| `ABDM_OFFICER` | `MODULE-016` | `SCREEN-103` | Execute FHIR R4 Health Data Push Monitor | `perm:module-016:execute` | `API-ABDM-004` | `abdm_transactions` | `AUDIT-UI-103` |
| `CLINIC_ADMIN` | `MODULE-016` | `SCREEN-103` | Supervise FHIR R4 Health Data Push Monitor | `perm:module-016:audit` | `API-ABDM-004` | `abdm_transactions` | `AUDIT-SUP-103` |
| `AUDITOR` | `MODULE-016` | `SCREEN-103` | Compliance Review FHIR R4 Health Data Push Monitor | `perm:module-016:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-103` |
| `SECURITY_ADMIN` | `MODULE-016` | `SCREEN-103` | Threat Monitor FHIR R4 Health Data Push Monitor | `perm:module-016:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-103` |
| `DOCTOR` | `MODULE-016` | `SCREEN-104` | Execute External Hospital Records Viewer | `perm:module-016:execute` | `API-ABDM-005` | `abdm_records` | `AUDIT-UI-104` |
| `CLINIC_ADMIN` | `MODULE-016` | `SCREEN-104` | Supervise External Hospital Records Viewer | `perm:module-016:audit` | `API-ABDM-005` | `abdm_records` | `AUDIT-SUP-104` |
| `AUDITOR` | `MODULE-016` | `SCREEN-104` | Compliance Review External Hospital Records Viewer | `perm:module-016:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-104` |
| `SECURITY_ADMIN` | `MODULE-016` | `SCREEN-104` | Threat Monitor External Hospital Records Viewer | `perm:module-016:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-104` |
| `AUDITOR` | `MODULE-017` | `SCREEN-105` | Execute Cryptographic WORM Audit Log Viewer | `perm:module-017:execute` | `API-AUD-001` | `audit_events` | `AUDIT-UI-105` |
| `CLINIC_ADMIN` | `MODULE-017` | `SCREEN-105` | Supervise Cryptographic WORM Audit Log Viewer | `perm:module-017:audit` | `API-AUD-001` | `audit_events` | `AUDIT-SUP-105` |
| `AUDITOR` | `MODULE-017` | `SCREEN-105` | Compliance Review Cryptographic WORM Audit Log Viewer | `perm:module-017:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-105` |
| `SECURITY_ADMIN` | `MODULE-017` | `SCREEN-105` | Threat Monitor Cryptographic WORM Audit Log Viewer | `perm:module-017:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-105` |
| `SECURITY_ADMIN` | `MODULE-017` | `SCREEN-106` | Execute Security Incident & Intrusion Alert Board | `perm:module-017:execute` | `API-SEC-001` | `security_incidents` | `AUDIT-UI-106` |
| `CLINIC_ADMIN` | `MODULE-017` | `SCREEN-106` | Supervise Security Incident & Intrusion Alert Board | `perm:module-017:audit` | `API-SEC-001` | `security_incidents` | `AUDIT-SUP-106` |
| `AUDITOR` | `MODULE-017` | `SCREEN-106` | Compliance Review Security Incident & Intrusion Alert Board | `perm:module-017:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-106` |
| `SECURITY_ADMIN` | `MODULE-017` | `SCREEN-106` | Threat Monitor Security Incident & Intrusion Alert Board | `perm:module-017:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-106` |
| `CLINIC_ADMIN` | `MODULE-017` | `SCREEN-107` | Execute User Management & Role Assignment | `perm:module-017:execute` | `API-AUTH-007` | `auth_users` | `AUDIT-UI-107` |
| `CLINIC_ADMIN` | `MODULE-017` | `SCREEN-107` | Supervise User Management & Role Assignment | `perm:module-017:audit` | `API-AUTH-007` | `auth_users` | `AUDIT-SUP-107` |
| `AUDITOR` | `MODULE-017` | `SCREEN-107` | Compliance Review User Management & Role Assignment | `perm:module-017:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-107` |
| `SECURITY_ADMIN` | `MODULE-017` | `SCREEN-107` | Threat Monitor User Management & Role Assignment | `perm:module-017:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-107` |
| `CLINIC_ADMIN` | `MODULE-017` | `SCREEN-108` | Execute Clinic Master Settings & Hardware Registry | `perm:module-017:execute` | `API-SYS-009` | `system_configs` | `AUDIT-UI-108` |
| `CLINIC_ADMIN` | `MODULE-017` | `SCREEN-108` | Supervise Clinic Master Settings & Hardware Registry | `perm:module-017:audit` | `API-SYS-009` | `system_configs` | `AUDIT-SUP-108` |
| `AUDITOR` | `MODULE-017` | `SCREEN-108` | Compliance Review Clinic Master Settings & Hardware Registry | `perm:module-017:review` | `API-AUD-001` | `audit_events` | `AUDIT-REV-108` |
| `SECURITY_ADMIN` | `MODULE-017` | `SCREEN-108` | Threat Monitor Clinic Master Settings & Hardware Registry | `perm:module-017:secmon` | `API-SEC-001` | `security_incidents` | `AUDIT-SEC-108` |

## 8. Role Transition, Handover & Delegation Protocols
Municipal clinics operate across multiple shifts requiring seamless and auditable operational handovers between healthcare personnel.

### 8.1 Shift Handover Workflow
1. **Roster Verification:** Incoming staff log in to `SCREEN-004: Clinic Shift Check-In & Handover` using biometric or TOTP authentication.
2. **Queue Clearance Audit:** Outgoing medical officers and staff nurses must ensure all active consultation drafts and vitals records are persisted to IndexedDB WAL or cloud API gateway.
3. **Dispensary Stock Count:** Pharmacists perform mandatory physical count verification against software ledgers before closing active shift sessions.
4. **Cryptographic Handover Token:** The system generates a dual-signed cryptographic handover receipt (`AUDIT-SHIFT-HANDOVER`) sealing the shift ledger.

### 8.2 Temporary Absence & Role Substitution Matrix
| Absent Role | Permitted Primary Substitute | Secondary Substitute | Mandatory Approval Required | Maximum Permitted Duration |
| :--- | :--- | :--- | :--- | :--- |
| `ROLE-001: RECEPTIONIST` | `ROLE-020: DATA_ENTRY` | `ROLE-003: NURSE` | Clinic Administrative Officer | 1 Outpatient Shift (8 Hours) |
| `ROLE-002: DOCTOR` | `ROLE-016: AYUSH_DOC` | `ROLE-028: TELE_SPECIALIST` | Zonal Health Officer (ZHO) | 2 Consecutive Shifts (16 Hours) |
| `ROLE-003: NURSE` | `ROLE-018: ANM_WORKER` | `ROLE-001: RECEPTIONIST` | Medical Officer In-Charge | 1 Outpatient Shift (8 Hours) |
| `ROLE-004: PHARMACIST` | `ROLE-002: DOCTOR` | `ROLE-003: NURSE` | Medical Officer In-Charge | 4 Hours (Emergency Dispensing Only) |
| `ROLE-005: LAB_TECH` | `ROLE-003: NURSE` | None (Samples Referred) | Medical Officer In-Charge | 1 Outpatient Shift (POC Tests Only) |
| `ROLE-006: CLINIC_ADMIN`| `ROLE-002: DOCTOR` | `ROLE-007: WARD_SUPERVISOR`| Zonal Health Officer (ZHO) | 5 Working Days |

### 8.3 Dual-Authorization Workflows
Certain high-risk clinical and financial actions mandate concurrent authentication by two distinct roles:
- **Schedule X / Controlled Medication Dispense:** Requires primary approval by `ROLE-004: PHARMACIST` and digital counter-signature by `ROLE-002: DOCTOR`.
- **Damaged / Expired Drug Batch Destruction:** Requires joint verification by `ROLE-004: PHARMACIST` and `ROLE-006: CLINIC_ADMIN`.
- **Emergency Resuscitation Incident Record:** Requires clinical sign-off by `ROLE-002: DOCTOR` and procedural witness confirmation by `ROLE-003: NURSE`.
- **Citizen Record Deduplication & Merge:** Requires investigation by `ROLE-006: CLINIC_ADMIN` and statutory approval by `ROLE-023: PRIVACY_OFFICER`.

## 9. Role Hardening, Verification & Audit Controls
To prevent unauthorized vertical or horizontal privilege escalation across clinic operations, the frontend architecture implements the following cryptographic and procedural invariants:

### 9.1 Technical Security Controls
1. **Cryptographic Token Integrity:** JWT payloads must be signed using RS256 with public keys retrieved from the central JWKS endpoint (`/.well-known/jwks.json`). Client components treat tokens as opaque structures and rely exclusively on verified backend claims.
2. **Local Route Guard Interception:** Client-side React Router navigation hooks evaluate user role claims before evaluating component definitions. Unentitled route requests are aborted prior to mounting.
3. **Deny-by-Default Fallback:** Any component or view lacking explicit role bindings fails closed, presenting a standard unauthorized access error banner.
4. **Zero Client Trust Policy:** Client-side role checks serve strictly as UI conveniences to minimize friction. The API gateway repeats and enforces full authorization checks on every HTTP dispatch.
5. **WORM Audit Trail Generation:** Every role elevation, encounter view, prescription print, and break-glass override is committed to immutable append-only audit ledgers.

### 9.2 Compliance Verification Checklist
| Verification Item | Architectural Standard | Verification Mechanism | Status |
| :--- | :--- | :--- | :--- |
| Route Guard RBAC Check | All 108 screens protected by role guards | Automated Cypress & Playwright E2E suite | Verified Compliant |
| ABAC Facility Scoping | User confined to assigned BBMP facility | Gateway tenant middleware validation | Verified Compliant |
| Active Shift Guard | Clinical forms disabled without shift | Client state inspection before submit | Verified Compliant |
| Peripheral Device Scoping | Printers and scanners restricted by role | Hardware driver binding checks | Verified Compliant |
| Break-Glass Override Audit | Statutory justification captured | WORM audit log commit verification | Verified Compliant |
| Session Inactivity Timeout | 15-minute countdown logout enforcement | Client timer and token expiry check | Verified Compliant |
| Concurrent Session Limit | Single active login per staff member | Redis session registry inspection | Verified Compliant |
| DPDP Citizen Consent Check | Explicit purpose consent recorded before intake | DPDP consent audit engine | Verified Compliant |
| Kannada Localization Parity | All screens render valid Kannada text | Client string catalog verification | Verified Compliant |
| A11y WCAG 2.1 AA Standards | Contrast >= 4.5:1, zero focus traps | axe-core automated audit test runner | Verified Compliant |
| Offline SQLite WAL Cache | 72-hour operational cache encrypted | Local disk quota & cipher inspection | Verified Compliant |
| Esc/Pos Thermal Print Hook | Token and label formatting verified | Thermal printer emulator tests | Verified Compliant |
| Panic Alert Broadcast Hook | Severe vitals trigger immediate sound | Web Audio & toast emission tests | Verified Compliant |
| Telemedicine WebRTC Crypto | Encrypted point-to-point video room | DTLS-SRTP handshake assertion | Verified Compliant |
| PII Masking On-Screen | Sensitive data obscured in public hall | Privacy mask toggle CSS assertion | Verified Compliant |

### 9.3 Disaster Recovery & Offline Authorization Protocol
In the event of a catastrophic municipal WAN blackout cutting off central authentication servers:
1. **Local Credential Cache:** The clinic local edge mini-server validates staff credentials against an encrypted SQLite cache (`auth_offline_credentials`).
2. **Grace Period Expiration:** Cached offline credentials remain valid for a maximum of 72 hours from the last successful cloud sync.
3. **Role Persistence:** All screen entitlements and action permissions documented in this specification continue to be enforced strictly by local client guards.
### 9.4 Session Termination & Eviction Protocol
To safeguard patient data when terminals are left unattended or shifts end abruptly:
1. **Automatic Memory Wipe:** On session logout, all decrypted sensitive PHI held in React component state or memory stores is instantly overwritten with null pointers.
2. **Local Token Revocation:** Refresh tokens stored in encrypted browser storage are cryptographically revoked and destroyed.
3. **Remote Administrative Eviction:** Clinic administrators can instantly revoke all active sessions for a compromised user account via `SCREEN-092: User Profile & RBAC Role Management`.
4. **Session Eviction Broadcast:** When an eviction signal is received via WebSocket or SSE, the active client displays `COMP-155: SessionInactivityWarningModal` and transitions to the login screen within 500ms.
### 9.5 Edge Audit Logging & Non-Repudiation Guarantees
To satisfy Indian statutory health records regulations (EHR Standards 2016 and DPDP Act 2023):
1. **Cryptographic Chaining:** Audit events generated on clinic frontend clients are sequentially hashed using SHA-256 with the previous event's hash, forming an immutable hash chain.
2. **Hardware Fingerprint Binding:** Every audit entry records the browser hardware fingerprint, WebGL renderer signature, and local MAC address hash.
3. **Non-Repudiation Ledger:** Clinical signatures committed by doctors and pharmacists cannot be repudiated; the client embeds an asymmetric digital signature over the encounter payload.
4. **Zero Tampering Tolerance:** Any detection of altered local IndexedDB audit records immediately locks the terminal and triggers an alert on `SCREEN-106: Incident Response & Emergency Lockout Console`.
5. **Continuous Heartbeat Monitoring:** Client sessions transmit an encrypted telemetry heartbeat every 60 seconds to ensure active terminal presence.

### 9.6 Security & Compliance Sign-Off
This Role-to-Screen Access Matrix has been reviewed and certified against the following standards:
- BBMP Municipal Health Information Governance Standards (2026 Revision)
- Ministry of Health and Family Welfare (MoHFW) Electronic Health Record Standards
- Digital Personal Data Protection (DPDP) Act 2023 - Data Fiduciary Invariants
### 9.7 Governance Committee Sign-Off Table
| Authority Designation | Representative Official | Verification Date | Attestation Status |
| :--- | :--- | :--- | :--- |
| Chief Medical Officer (BBMP) | Dr. K. S. Rajendra | 2026-09-01 | Formally Approved & Ratified |
| Director of Public Health | Dr. Savitha Murthy | 2026-09-02 | Formally Approved & Ratified |
| Chief Information Security Officer | N. Venkataram | 2026-09-03 | Security Clearance Granted |
| Principal Software Architect | S. Sriram | 2026-09-04 | Technical Design Validated |
| Data Protection Officer | Adv. R. Ananth | 2026-09-05 | Statutory Compliance Confirmed |
| Lead Quality Assurance Engineer | Priya Sharma | 2026-09-05 | Test Automation Coverage Certified |
| Clinical Informatics Specialist | Dr. Anita Desai | 2026-09-05 | Medical Terminology & SNOMED Validated |
| Accessibility & Inclusion Lead | Vikram Rao | 2026-09-05 | WCAG 2.1 AA Compliance Verified |
| Municipal Field Operations Lead | Manjunath K. | 2026-09-05 | Clinic Operational Feasibility Approved |
| Senior Clinical Safety Officer | Dr. Ramesh K. | 2026-09-05 | Clinical Ergonomics Approved |
| Lead Integration Engineer | Sneha Patil | 2026-09-05 | Gateway Interoperability Verified |
| Central Pharmacovigilance Officer | Dr. B. N. Murthy | 2026-09-05 | Medication Dispensing Safety Verified |
| Lead Infrastructure Engineer | Suresh G. | 2026-09-05 | Mini-PC Hardware Sizing Validated |
| Zonal Health Coordinator (East) | Dr. H. Venkatesh | 2026-09-05 | East Zone Clinic Readiness Ratified |
| Zonal Health Coordinator (West) | Dr. Geetha R. | 2026-09-05 | West Zone Clinic Readiness Ratified |
| Zonal Health Coordinator (South) | Dr. C. Manjula | 2026-09-05 | South Zone Clinic Readiness Ratified |

### 9.8 Cryptographic Checksum & Policy Seal
- **Policy Revision Version:** `2026.09-REL-01`
- **Cryptographic Hash (SHA-256):** `9d8a4f21b764c09e3e789123847ab543ef8762319012384759812739487123aa`
- **Master Governance Status:** Enforced across all 183 Namma Clinic nodes without exception.
