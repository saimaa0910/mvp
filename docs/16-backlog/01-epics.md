# 🏆 Backlog Master: Epics Catalog (EPIC-01 through EPIC-23)
## Namma Clinic Digital Health & Operations Platform
**Document Code:** BCK-EPC-01 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Master Epics Inventory

| Epic ID | Epic Title | Scope & Business Objective | Target Release | Sprints |
| :--- | :--- | :--- | :---: | :---: |
| **EPIC-01** | `Architecture & Foundation` | Core system scaffolding, TypeScript domain types, PostgreSQL schema, base fastify API, and Docker dev environment. | REL-00 | S01-S02 |
| **EPIC-02** | `Authentication & RBAC` | Bcrypt authentication, JWT tokens, 12 roles, 48 permissions, session management, and password policy. | REL-00 | S01-S02 |
| **EPIC-03** | `Organization & Facility Hierarchy` | GBA, BBMP zones (8), wards (243), and Namma Clinic facilities (183+) master data management. | REL-00 | S01-S02 |
| **EPIC-04** | `Master Data Management` | Karnataka EDL formulary (120 drugs), 14 essential lab tests, and ICD-10 diagnostic coding masters. | REL-00 | S01-S02 |
| **EPIC-05** | `Patient Demographic Management` | Citizen search (mobile/UHID/ABHA), demographic registration, consent logging, and duplicate prevention. | REL-01 | S03-S04 |
| **EPIC-06** | `Registration & Daily Queue Desk` | Sequential daily token generation, thermal slip printing with QR code, and real-time waiting list queue. | REL-01 | S03-S04 |
| **EPIC-07** | `Triage & Vital Signs Capture` | Touchscreen vitals entry (BP, Pulse, SpO2, Temp, Glucose, BMI) and automatic clinical danger alert flags. | REL-01 | S03-S04 |
| **EPIC-08** | `Doctor Consultation & EMR-Lite` | Doctor clinical workspace, 1-click chief complaint chips, examination notes, and provisional diagnosis. | REL-02 | S05-S06 |
| **EPIC-09** | `Electronic Prescription Desk` | Formulary drug prescription, dosage/frequency/duration pickers, drug allergy verification, and sign-off. | REL-02 | S05-S06 |
| **EPIC-10** | `Pharmacy Dispensing Operations` | Electronic prescription fulfillment, First-Expiry-First-Out (FEFO) batch verification, and bilingual slips. | REL-03 | S07-S08 |
| **EPIC-11** | `Batch Inventory & Stock Ledger` | Clinic stock ledger, batch expiry tracking, physical stock adjustment, and monthly indent requisition. | REL-03 | S07-S08 |
| **EPIC-12** | `Point-of-Care Laboratory` | Ordering and result entry for 14 essential primary care lab tests (RBS, Malaria, Dengue NS1, Urine, etc.). | REL-03 | S07-S08 |
| **EPIC-13** | `Secondary Referral Gateway` | Outbound referrals to BBMP General Hospitals and Medical Colleges with structured clinical summaries and QR. | REL-03 | S07-S08 |
| **EPIC-14** | `Citizen Communication & Feedback` | Transactional SMS dispatch for prescription summaries, appointment reminders, and QR citizen feedback. | REL-04 | S09-S10 |
| **EPIC-15** | `Security, Audit & Compliance` | Cryptographically verifiable append-only audit logging, DPDP Act consent enforcement, and VAPT hardening. | REL-00 | S01-S16 |
| **EPIC-16** | `Public Health Analytics & Dashboards` | Star Schema data mart, CDC pipeline, and executive dashboards for ward/zonal epidemiological surveillance. | REL-04 | S09-S10 |
| **EPIC-17** | `AI Clinical Decision Support` | Non-autonomous ML models: 30-day stockout forecasting, fever anomaly outbreak detection, and NCD recall. | REL-07 | S15-S16 |
| **EPIC-18** | `ABDM & National Digital Health` | Ayushman Bharat Digital Mission integration: ABHA verification, HIP Care Context linking, and FHIR R4 push. | REL-07 | S15-S16 |
| **EPIC-19** | `Offline PWA & Resilient Sync` | Browser IndexedDB storage, background sync queue, offline PIN auth, and deterministic conflict resolution. | REL-04 | S09-S10 |
| **EPIC-20** | `20-Clinic Pilot Rollout & Stabilization` | Field deployment in 20 pilot clinics, hands-on staff training, user feedback triage, and SLA monitoring. | REL-05 | S11-S12 |
| **EPIC-21** | `Operations, Training & Helpdesk` | Bilingual frontline training, ticketing desk, hardware maintenance playbooks, and on-call operational support. | REL-05 | S11-S18 |
| **EPIC-22** | `State & Municipal Health Reporting` | Automated daily and monthly reporting to Karnataka HMIS, IHIP, and BBMP Health Commissioner. | REL-06 | S13-S14 |
| **EPIC-23** | `Citywide Scale & Production Hardening` | Scaling infrastructure to 183 clinics, high-concurrency load testing, multi-AZ DR failover validation. | REL-06 | S13-S14 |
