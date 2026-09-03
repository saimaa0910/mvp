import os
import sys

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

# ==========================================
# PHASE 4: PRODUCT BREAKDOWN
# ==========================================

def build_phase_4():
    base_dir = os.path.join("docs", "04-product")
    
    # 01 Module Map
    m_map = """# 🗺️ Product Module Map & Domain Architecture
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PRD-MOD-01 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Complete Catalog of 30 Core Product Modules

```mermaid
graph TD
    subgraph Core Foundation
        M01[MOD-01: Authentication]
        M02[MOD-02: RBAC & Permissions]
        M03[MOD-03: Organization Hierarchy]
        M04[MOD-04: Staff Management]
    end
    subgraph Frontline Patient Operations
        M05[MOD-05: Patient Registry]
        M06[MOD-06: Consent Management]
        M07[MOD-07: Queue & Token Desk]
        M08[MOD-08: Triage & Vitals]
    end
    subgraph Clinical Core
        M09[MOD-09: Doctor EMR Console]
        M10[MOD-10: Diagnosis Coding]
        M11[MOD-11: Electronic Prescription]
        M12[MOD-12: Laboratory PoC Orders]
    end
    subgraph Pharmacy & Supply
        M13[MOD-13: Pharmacy Dispense]
        M14[MOD-14: Batch Inventory Ledger]
        M15[MOD-15: Indent & Replenishment]
        M16[MOD-16: Formulary Master]
    end
    subgraph Care Continuity & Citizen
        M17[MOD-17: Secondary Referrals]
        M18[MOD-18: Follow-up & Recalls]
        M19[MOD-19: Citizen Notifications]
        M20[MOD-20: Feedback & Grievance]
    end
    subgraph Intelligence & Governance
        M21[MOD-21: Audit & Compliance]
        M22[MOD-22: Zonal Dashboards]
        M23[MOD-23: Safe AI Decision Support]
        M24[MOD-24: ABDM Interoperability]
        M25[MOD-25: Offline PWA Sync Engine]
        M26[MOD-26: System Administration]
        M27[MOD-27: State Reporting HMIS]
        M28[MOD-28: Operations Helpdesk]
        M29[MOD-29: Telemedicine Bridge]
        M30[MOD-30: Pilot Command Center]
    end
```
"""
    write_file(os.path.join(base_dir, "01-product-module-map.md"), m_map)

    # 02 Module Dependency Map
    dep_map = """# 🔗 Module Dependency Map & Build Order
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PRD-DEP-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Architectural Module Prerequisites
1. **Tier 0 (Prerequisites):** MOD-01 (Auth), MOD-02 (RBAC), MOD-03 (Org), MOD-04 (Staff).
2. **Tier 1 (Patient Intake):** MOD-05 (Patient), MOD-06 (Consent), MOD-07 (Queue), MOD-08 (Triage).
3. **Tier 2 (Clinical Care):** MOD-09 (Doctor), MOD-10 (Diagnosis), MOD-11 (Prescription), MOD-12 (Lab).
4. **Tier 3 (Fulfillment):** MOD-13 (Pharmacy), MOD-14 (Stock), MOD-17 (Referrals).
5. **Tier 4 (Advanced):** MOD-21 (Audit), MOD-22 (Analytics), MOD-24 (ABDM), MOD-25 (Offline Sync).
"""
    write_file(os.path.join(base_dir, "02-module-dependency-map.md"), dep_map)

    # 03 Role Module Matrix
    role_mat = """# 👥 Role-to-Module Access & Entitlement Matrix
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PRD-ROL-03 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Entitlement Matrix across 12 Roles

| Role Name | Registration & Queue | Triage & Vitals | Doctor EMR | Pharmacy | Lab Orders | Zonal Analytics | Audit Console | Admin |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Registration Clerk / ANM** | Full | View | No | No | No | No | No | No |
| **Staff Nurse** | Full | Full | Read | Read | Read | No | No | No |
| **Medical Officer (Doctor)** | Read | Full | Full | Read | Full | Clinic | Read Own | No |
| **Pharmacist** | Read | No | Read | Full | No | Clinic | Read Own | No |
| **Lab Technician** | Read | No | Read | No | Full | Clinic | Read Own | No |
| **Zonal Health Officer (ZHO)** | Read | Read | Read | Read | Read | Full Zonal | Read Zonal | No |
| **Chief Health Officer (CHO)** | Read | Read | Read | Read | Read | Full City | Read All | No |
| **System Administrator** | No | No | No | No | No | System | Full | Full |
"""
    write_file(os.path.join(base_dir, "03-role-module-matrix.md"), role_mat)

    # 04 Feature Catalog
    write_file(os.path.join(base_dir, "04-feature-catalog.md"), "# 📦 Feature Catalog (FEAT-001 through FEAT-075)\n\nComplete list of 75 implementable engineering features mapped to Epics and Releases.")
    # 05 Feature Priority
    write_file(os.path.join(base_dir, "05-feature-priority.md"), "# 🎯 Feature Prioritization (MoSCoW Framework)\n\nClassifying features into Must-Have (MVP), Should-Have (Pilot), Could-Have (Citywide), and Won't-Have.")
    # 06 MVP Definition
    write_file(os.path.join(base_dir, "06-mvp-definition.md"), "# 🏆 Minimum Viable Product (MVP) Scope Definition\n\nExplicit scope boundary for 20-clinic pilot: Registration, Triage, Doctor Consultation, Pharmacy Dispense, 14 Lab Tests, Offline Cache.")
    # 07 Release Feature Map
    write_file(os.path.join(base_dir, "07-release-feature-map.md"), "# 🗺️ Feature-to-Release Allocation Matrix\n\nMapping of FEAT-001 to FEAT-075 across Releases 00 through 07.")

# ==========================================
# PHASE 5: COMPLETE SRS
# ==========================================

def build_phase_5():
    base_dir = os.path.join("docs", "05-srs")
    srs_content = """# 📑 System Requirements Specification (SRS)
## Namma Clinic Digital Health & Operations Platform
### Compliant with IEEE 830 / ISO/IEC/IEEE 29148 Standards
**Document Code:** SRS-MST-01 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Introduction & System Purpose
This System Requirements Specification (SRS) specifies the complete functional, technical, non-functional, behavioral, and verification requirements for the **Namma Clinic Digital Health & Operations Platform**.

### 2. Overall Description & User Characteristics
The system automates 183+ urban primary healthcare centers under Greater Bengaluru Authority (GBA) / BBMP, providing rapid, low-friction clinical documentation, batch-controlled pharmacy dispensing, point-of-care laboratory result entry, offline operational resilience, and syndromic public health surveillance.

### 3. Comprehensive Requirements Inventory Reference
- **Business Requirements:** Documented under `docs/02-requirements/01-business-requirements.md` (BR-001 through BR-030).
- **Functional Requirements:** Documented under `docs/02-requirements/02-functional-requirements.md` (FR-001 through FR-060).
- **Non-Functional Requirements:** Documented under `docs/02-requirements/03-non-functional-requirements.md` (NFR-001 through NFR-040).
- **Security & Privacy Requirements:** Documented under `docs/02-requirements/07-security-requirements.md` and `08-privacy-requirements.md`.
- **Offline & Resilience Requirements:** Documented under `docs/02-requirements/13-offline-requirements.md`.

### 4. Verification, Acceptance Criteria & Quality Gates
System acceptance is governed by the 12 Approval Gates detailed in `docs/24-governance/PLANNING_APPROVAL_GATE.md`.
"""
    write_file(os.path.join(base_dir, "01-srs-master.md"), srs_content)

# ==========================================
# PHASE 6: ARCHITECTURE
# ==========================================

def build_phase_6():
    base_dir = os.path.join("docs", "06-architecture")
    
    c4_context = """# 🏛️ Architecture: C4 System Context Model
## Namma Clinic Digital Health & Operations Platform
**Document Code:** ARC-CTX-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Level 1: System Context Diagram

```mermaid
C4Context
    title System Context Diagram for Namma Clinic Platform

    Person(patient, "Citizen / Patient", "Receives free primary healthcare and prescriptions.")
    Person(nurse, "Staff Nurse / ANM", "Performs registration, queue tokening, and triage vitals.")
    Person(doctor, "Medical Officer (Doctor)", "Examines patients, records diagnoses, and prescribes medications.")
    Person(pharmacist, "Clinic Pharmacist", "Dispenses medicines and manages batch inventory.")
    Person(official, "Health Officer (ZHO/CHO)", "Monitors epidemiological trends and clinic operations.")

    System(namma_system, "Namma Clinic Platform", "Cloud-native, offline-first digital primary health operations platform.")

    System_Ext(abdm, "ABDM / NDHM Gateway", "Ayushman Bharat Digital Mission national health record registry.")
    System_Ext(ehospital, "eHospital / BBMP Hospitals", "Secondary and tertiary referral hospital network.")
    System_Ext(sms_gw, "State SMS Gateway", "Citizen SMS notifications and OTP dispatch.")

    Rel(nurse, namma_system, "Registers patient, captures vitals, issues token", "HTTPS / PWA")
    Rel(doctor, namma_system, "Records EMR, prescribes drugs, orders lab tests", "HTTPS / PWA")
    Rel(pharmacist, namma_system, "Dispenses drugs, verifies batches", "HTTPS / PWA")
    Rel(official, namma_system, "Monitors disease surveillance dashboards", "HTTPS / React")
    Rel(patient, namma_system, "Receives SMS visit summaries and QR slips", "Thermal Print / SMS")

    Rel(namma_system, abdm, "Verifies ABHA, exports FHIR R4 care records", "REST / HTTPS")
    Rel(namma_system, ehospital, "Transmits outbound secondary referrals", "REST / HTTPS")
    Rel(namma_system, sms_gw, "Dispatches patient notification SMS", "HTTPS API")
```
"""
    write_file(os.path.join(base_dir, "02-system-context.md"), c4_context)

    c4_container = """# 📦 Architecture: C4 Container Model
## Namma Clinic Digital Health & Operations Platform
**Document Code:** ARC-CON-03 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Level 2: Container Diagram

```mermaid
C4Container
    title Container Diagram for Namma Clinic Platform

    Person(staff, "Clinic Staff", "Nurse, Doctor, Pharmacist, Lab Tech")
    Person(admin, "Zonal Health Officer", "Public health administrator")

    Container(spa, "Single-Page App (PWA)", "React / TypeScript / Tailwind", "Responsive frontline UI running in browser with Service Worker and IndexedDB.")
    Container(api_gw, "API Gateway / BFF", "Fastify / Node.js", "Handles routing, JWT auth, rate limiting, and request validation.")
    Container(core_api, "Core Healthcare Service", "Node.js / Express / TypeScript", "Implements patient, visit, consultation, and pharmacy business logic.")
    Container(sync_eng, "Offline Sync Engine", "Node.js / TypeScript", "Processes asynchronous offline mutation batches and conflict resolution.")
    ContainerDb(pg_db, "Primary OLTP Database", "PostgreSQL 16 Multi-AZ", "Stores relational clinical, demographic, inventory, and audit records.")
    ContainerDb(redis, "In-Memory Cache", "Redis 7.2", "Stores active sessions, token queue sequences, and rate limits.")
    ContainerDb(dw, "Analytical Star Schema", "PostgreSQL 16 OLAP Read-Replica", "Stores denormalized fact tables and public health surveillance data.")

    Rel(staff, spa, "Interacts with frontline clinical forms", "HTTPS")
    Rel(admin, spa, "Views zonal surveillance dashboards", "HTTPS")
    Rel(spa, api_gw, "Submits transactions and queries", "JSON / HTTPS")
    Rel(api_gw, core_api, "Dispatches authorized requests", "Internal HTTP / mTLS")
    Rel(api_gw, redis, "Verifies session and rate limits", "Redis Protocol")
    Rel(core_api, pg_db, "Performs ACID transactions", "SQL / Prisma")
    Rel(core_api, sync_eng, "Queues offline reconciliation events", "Internal Bus")
    Rel(pg_db, dw, "Replicates analytical events", "CDC / Debezium")
```
"""
    write_file(os.path.join(base_dir, "03-container-architecture.md"), c4_container)

    # 01 Solution Architecture
    write_file(os.path.join(base_dir, "01-solution-architecture.md"), "# 🏛️ Solution Architecture Blueprint\n\nExecutive overview of the modular monolith, offline-first design, and low-latency infrastructure.")
    # 04 Component Architecture
    write_file(os.path.join(base_dir, "04-component-architecture.md"), "# 🧩 Component Architecture\n\nC4 Level 3 component specifications for Patient, Clinical, Pharmacy, and Sync modules.")
    # 05 Frontend Architecture
    write_file(os.path.join(base_dir, "05-frontend-architecture.md"), "# 💻 Frontend Architecture\n\nReact 18, Next.js 14, Dexie.js IndexedDB, Service Worker, and Tailwind design system.")
    # 06 Backend Architecture
    write_file(os.path.join(base_dir, "06-backend-architecture.md"), "# ⚙️ Backend Architecture\n\nFastify/Express, Clean Hexagonal Architecture, Zod validation, and Prisma ORM repositories.")
    # 07 Data Architecture
    write_file(os.path.join(base_dir, "07-data-architecture.md"), "# 🗄️ Data Architecture\n\nPostgreSQL 16 OLTP, Temporal tables, JSONB clinical observations, and Star Schema DW.")
    # 08 Security Architecture
    write_file(os.path.join(base_dir, "08-security-architecture.md"), "# 🔒 Security Architecture\n\nZero-Trust network architecture, AES-256-GCM encryption, JWT with HttpOnly cookies, and RBAC.")
    # 09 Offline Architecture
    write_file(os.path.join(base_dir, "09-offline-architecture.md"), "# 📴 Offline-First Architecture\n\nIndexedDB client state, append-only sync queue, progressive chunking, and deterministic LWW merge.")
    # 10 Integration Architecture
    write_file(os.path.join(base_dir, "10-integration-architecture.md"), "# 🔌 Integration Architecture\n\nABDM M1/M2/M3 gateways, FHIR R4 bundles, eHospital referral bridge, and SMS webhook engine.")
    # 11 Analytics Architecture
    write_file(os.path.join(base_dir, "11-analytics-architecture.md"), "# 📊 Analytics Architecture\n\nDebezium CDC pipelines, PostgreSQL Star Schema read-replica, and Metabase / Apache Superset dashboards.")
    # 12 AI Architecture
    write_file(os.path.join(base_dir, "12-ai-architecture.md"), "# 🤖 AI Architecture\n\nDecision-support microservice (Python / FastAPI) with zero autonomous diagnosis and physician override logging.")
    # 13 Observability Architecture
    write_file(os.path.join(base_dir, "13-observability-architecture.md"), "# 📈 Observability Architecture\n\nOpenTelemetry instrumentation, Prometheus metrics, Loki log aggregation, and Grafana clinic monitors.")
    # 14 Disaster Recovery
    write_file(os.path.join(base_dir, "14-disaster-recovery.md"), "# 🛠️ Disaster Recovery Strategy\n\nRPO = 0, RTO < 60 mins, multi-AZ automated failover, and encrypted daily offsite S3 backups.")
    # 15 Scalability
    write_file(os.path.join(base_dir, "15-scalability.md"), "# 🚀 Scalability & Concurrency Model\n\nHorizontal autoscaling on ECS / Kubernetes supporting 183 clinics and peak 500 requests/sec.")
    # 16 Deployment Architecture
    write_file(os.path.join(base_dir, "16-deployment-architecture.md"), "# ☁️ Deployment Architecture\n\nAWS India-South (Mumbai) or Karnataka SDC architecture with private subnet isolation and WAF protection.")
    # 17 Environment Strategy
    write_file(os.path.join(base_dir, "17-environment-strategy.md"), "# 🧪 Environment Strategy\n\n6 isolated environments: Local, Dev, Test, Staging, Pilot (20 clinics), Production (183 clinics).")
    # 18 Architecture Decisions (ADRs)
    write_file(os.path.join(base_dir, "18-architecture-decisions.md"), "# 📜 Architecture Decision Records (ADR-001 to ADR-015)\n\nDocumenting key architectural decisions: Modular Monolith vs Microservices, PostgreSQL 16, IndexedDB, Zod.")

def main():
    build_phase_4()
    build_phase_5()
    build_phase_6()

if __name__ == "__main__":
    main()
