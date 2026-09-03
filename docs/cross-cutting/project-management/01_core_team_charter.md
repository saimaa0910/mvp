# 👥 Project Management: Core Team Charter & RACI Matrix
## Namma Clinic Digital Health & Operations Platform
### K Mati (Kushagramati Analytics Pvt Ltd) & GBA / BBMP Health Department
### Document Code: PM-CH-01 | Version: 1.0 | Date: September 2026

---

## 1. Executive Summary

This Core Team Charter formalizes the cross-functional leadership team responsible for delivering the Namma Clinic Digital Health & Operations Platform across all execution phases (Discovery, Prototyping, Pilot in 20 clinics, Hardening, and Citywide Scale across 183+ clinics). It defines key roles, qualifications, responsibilities, decision authorities, and a comprehensive RACI matrix covering technical, clinical, operational, and administrative workstreams.

---

## 2. Core Leadership Team Profiles

### 2.1 Project Director
* **Name / Title:** Project Director (GovTech & Public Health Engagements)
* **Allocation:** 100% Full-Time Equivalent (FTE)
* **Qualifications & Experience:** 15+ years in large-scale government program management, smart governance, health informatics implementations, and institutional liaison with municipal bodies in Karnataka.
* **Core Responsibilities:**
  1. Overall program ownership, milestone governance, contract delivery, and budget control.
  2. Direct liaison with the Special Commissioner, Additional Director (Health), Chief Health Officer, and Zonal Medical Officers.
  3. Escalation management, steering committee representation, and inter-departmental conflict resolution.
  4. Vendor and consortium management, hardware dispatch oversight, and quality audits.
* **Key Decision Authority:** Approval of milestone deliverables, project budget drawdowns, contractual modifications, and high-level stakeholder communications.

### 2.2 Clinical Advisor (Doctor with Primary Care Experience)
* **Name / Title:** Lead Clinical Advisor & Primary Care Specialist (MBBS, MD Community Medicine / Public Health)
* **Allocation:** 60% FTE (3 dedicated days/week + on-call during clinic pilot hours)
* **Qualifications & Experience:** 12+ years in clinical practice, former consultant with Urban Primary Health Centres (UPHCs) in Bengaluru, deep familiarity with National Health Mission (NHM) guidelines, National Vector Borne Disease Control Programme (NVBDCP), and NP-NCD protocols.
* **Core Responsibilities:**
  1. Clinical validation of EMR-lite templates, triage scoring logic, and emergency danger flags.
  2. Standardization of primary care drug formulary and dosage guidelines aligned with Karnataka State Drug Logistics Society (KSDLPS).
  3. Definition of referral pathways, specialist routing protocols, and diagnostic normal ranges.
  4. Clinical training curriculum design and peer-to-peer training sessions for Medical Officers.
  5. Review of adverse events, diagnostic discrepancy logs, and patient safety safeguards.
* **Key Decision Authority:** Clinical workflow sign-off, medical terminology mapping, triage threshold validations, and medical escalation policies.

### 2.3 Solution Architect
* **Name / Title:** Principal Healthcare Solutions Architect
* **Allocation:** 100% FTE
* **Qualifications & Experience:** 14+ years in distributed microservices architectures, cloud platforms (AWS / NIC Cloud / MeghRaj), Ayushman Bharat Digital Mission (ABDM) sandbox certifications (M1, M2, M3), FHIR R4, and HL7 messaging standards.
* **Core Responsibilities:**
  1. Technical blueprint design, service boundaries, API Gateway routing, and database topologies.
  2. ABDM architecture design (ABHA creation, verification, Health Information Provider [HIP], Health Information User [HIU], and Consent Management).
  3. Offline caching and transactional sync strategy (IndexedDB + Service Worker + Conflict Resolution).
  4. Infrastructure sizing, auto-scaling, cloud hosting, and continuous deployment (CI/CD) pipelines.
  5. Technical lead for third-party integrations (eHospital, state reporting engines, SMS/WhatsApp gateways).
* **Key Decision Authority:** Technology stack selection, schema design approval, API contract approval, and infrastructure security sign-off.

### 2.4 Data Lead / Analytics Engineer
* **Name / Title:** Lead Health Data Engineer & Epidemiological Analytics Specialist
* **Allocation:** 100% FTE
* **Qualifications & Experience:** 10+ years in health data warehousing, geospatial information systems (GIS), predictive modeling, ETL pipelines, and public health dashboard design for urban surveillance.
* **Core Responsibilities:**
  1. Analytical data model design (fact/dimension stars, aggregate tables, CDC data pipelines).
  2. Development of multi-tier dashboards (Clinic Real-Time, Zonal Health Officer, Special Commissioner Command).
  3. Algorithmic development of epidemiological early-warning indicators (fever clusters, dengue spike heuristics, seasonal anomalies).
  4. Pharmacy inventory forecasting models (stock-out predictive alerts at 7-day and 14-day horizons).
  5. Non-Communicable Disease (NCD) cohort tracking and patient recall automation logic.
* **Key Decision Authority:** Data pipeline architecture, KPI metric definitions, anomaly detection thresholds, and analytics dashboard layout approvals.

### 2.5 Field Implementation Lead
* **Name / Title:** Field Operations & Change Management Lead
* **Allocation:** 100% FTE (Stationed in Bengaluru for on-site clinic operations)
* **Qualifications & Experience:** 9+ years managing grassroots field deployments, clinic hardware rollouts, frontline health worker enablement (ASHAs, ANMs, Staff Nurses), and bilingual helpdesk operations in Karnataka.
* **Core Responsibilities:**
  1. Physical clinic readiness audits, hardware deployment (desktops, tablets, thermal printers, UPS, 4G routers).
  2. In-person field training sessions in Kannada and English across all 20 pilot clinics and subsequent wave clinics.
  3. On-site "hypercare" deployment for the first 5 days of each clinic go-live.
  4. Daily management of Tier-1 and Tier-2 bilingual helpdesk ticketing and issue escalation.
  5. Change management, digital adoption champions identification, and user feedback synthesis.
* **Key Decision Authority:** Clinic site readiness sign-off, hardware dispatch schedules, field training completion sign-offs, and on-site support resource allocation.

---

## 3. Extended Team Roles

| Role | Headcount | Reporting To | Core Focus |
| :--- | :--- | :--- | :--- |
| **Frontend Engineers (React/Next.js/PWA)** | 3 | Solution Architect | Clinic UI/UX, responsive tablet views, offline caching, Kannada typography. |
| **Backend Engineers (Node.js/PostgreSQL)** | 3 | Solution Architect | RESTful APIs, auth/RBAC, FHIR mapping, transactional data layers. |
| **DevOps & Cloud Security Engineer** | 1 | Solution Architect | VPC/networking, TLS/KMS configuration, CI/CD, backup automation, CERT-In compliance. |
| **QA & VAPT Security Specialist** | 2 | Solution Architect | Automated regression testing, load testing, pre-VAPT hardening, security remediations. |
| **Clinical Field Trainers (Bilingual)** | 4 | Field Implementation Lead | On-site hands-on training for Doctors, Nurses, Pharmacists, and Receptionists in Kannada. |
| **Bilingual Helpdesk Support Agents** | 2 | Field Implementation Lead | Clinic-hour live phone & WhatsApp support, ticket triage, and issue resolution tracking. |

---

## 4. Comprehensive RACI Matrix

**RACI Definitions:**
* **R - Responsible:** The role that performs the activity to achieve the deliverable.
* **A - Accountable:** The sole role with ultimate veto and sign-off authority. Only one 'A' per activity.
* **C - Consulted:** Key experts providing input, review, and feedback (two-way communication).
* **I - Informed:** Stakeholders kept updated on progress, outputs, or delays (one-way communication).

### Key Role Codes:
* **PD:** Project Director (K Mati)
* **CA:** Clinical Advisor (K Mati)
* **SA:** Solution Architect (K Mati)
* **DL:** Data Lead / Analytics Engineer (K Mati)
* **FL:** Field Implementation Lead (K Mati)
* **SC:** Special Commissioner (GBA / BBMP Health)
* **ZMO:** Zonal Medical Officers (BBMP)
* **MO:** Clinic Medical Officers (Frontline Doctors)

| # | Workstream & Major Activity | PD | CA | SA | DL | FL | SC | ZMO | MO |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1.0** | **Governance & Administrative** | | | | | | | | |
| 1.1 | Project Charter, SLA & Contract Baseline | **A** | C | C | C | C | **C** | I | I |
| 1.2 | Fortnightly Governance Reporting to BBMP | **A** | C | C | C | C | **I** | I | I |
| 1.3 | Budget, Billing & Milestone Certifications | **A** | I | I | I | I | **A/C** | I | I |
| 1.4 | Scope Change Requests & Impact Analysis | **A** | C | C | C | C | **C** | I | I |
| **2.0** | **Clinical Design & Standardization** | | | | | | | | |
| 2.1 | Primary Care Condition Templates Definition | C | **A** | C | C | I | I | C | C |
| 2.2 | Vitals Triage & Danger Flag Rules Validation | I | **A** | C | C | C | I | C | C |
| 2.3 | Pharmacy Drug Formulary & Unit Standardization| I | **A** | C | C | C | I | C | C |
| 2.4 | Diagnostic Test Catalogue & Normal Ranges | I | **A** | C | C | I | I | C | C |
| 2.5 | Bilingual Prescription Format Approval | C | **A** | C | I | C | C | C | C |
| **3.0** | **Architecture, Development & Security** | | | | | | | | |
| 3.1 | System Architecture & Database Schema | I | C | **A** | C | I | I | I | I |
| 3.2 | API Contracts & OpenAPI Specification | I | C | **A** | C | I | I | I | I |
| 3.3 | Offline-Sync & Conflict Engine Design | I | I | **A** | I | C | I | I | I |
| 3.4 | ABDM Sandbox & Production API Integration | C | I | **A** | I | I | C | I | I |
| 3.5 | CERT-In VAPT Audit & Remediation Sign-Off | C | I | **A** | I | I | C | I | I |
| **4.0** | **Data Engineering & Analytics** | | | | | | | | |
| 4.1 | Analytics Warehouse Schema & ETL Pipelines | I | C | C | **A** | I | I | I | I |
| 4.2 | Real-Time Clinic & Zonal Dashboards | C | C | C | **A** | C | C | C | I |
| 4.3 | Special Commissioner Command Dashboard | C | C | C | **A** | I | **C** | I | I |
| 4.4 | AI Epidemiological Outbreak Alerts | C | C | C | **A** | I | C | C | I |
| 4.5 | Predictive Stock-out Forecasting Engine | C | C | C | **A** | C | I | C | I |
| **5.0** | **Field Implementation & Change Management** | | | | | | | | |
| 5.1 | Clinic Hardware Inspection & Connectivity Audit| I | I | C | I | **A** | I | C | C |
| 5.2 | Device Deployment, UPS & Peripherals Setup | I | I | C | I | **A** | I | I | C |
| 5.3 | In-Clinic Bilingual Staff Training Sessions | C | C | I | I | **A** | I | C | C |
| 5.4 | Clinic Pilot Go-Live (5-Day On-Site Hypercare)| C | C | C | I | **A** | I | C | C |
| 5.5 | Tier-1 / Tier-2 Helpdesk SLA Operations | C | I | C | I | **A** | I | C | C |

---

## 5. Decision-Making & Escalation Matrix

```
[Level 1: Operational Field Blockers]
(Hardware, network, local clinic logins, daily data entry sync)
       │  Escalation window: < 2 Hours
       ▼
Field Implementation Lead (FL) + Clinic Medical Officer (MO)
       │
       │ (If unresolved within 4 hours or affects clinical workflow)
       ▼
[Level 2: Clinical & Technical Architecture Blockers]
(EMR template bugs, DB sync failures, prescription printing, triage logic)
       │  Escalation window: < 6 Hours
       ▼
Solution Architect (SA) + Clinical Advisor (CA)
       │
       │ (If milestone at risk, contractual impact, or policy dispute)
       ▼
[Level 3: Executive Program Governance]
(Scope variations, zone-wide connectivity failure, procurement delays)
       │  Escalation window: < 24 Hours
       ▼
Project Director (PD, K Mati) + Special Commissioner (SC, GBA/BBMP)
```

---

## 6. Charter Sign-Off

| Entity | Designated Authority | Signature | Date |
| :--- | :--- | :--- | :--- |
| **K Mati Leadership** | Sri [Name], Managing Director | ___________________ | 02-Sep-2026 |
| **K Mati Project Team** | Project Director | ___________________ | 02-Sep-2026 |
| **GBA / BBMP Health Dept**| Sri Venkata Rao Chalapathi, IAS, Special Commissioner | ___________________ | __-___-2026 |
