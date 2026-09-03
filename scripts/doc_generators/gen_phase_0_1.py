import os
import sys

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

# ==========================================
# PHASE 0: PROJECT BASELINE
# ==========================================

AUDIT_01 = """# 🔍 Phase 0: Complete Repository Audit
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PB-AUD-01 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Executive Summary & Inventory Context
This repository audit establishes the empirical technical foundation of the **Namma Clinic Digital Health & Operations Platform** for Greater Bengaluru Authority (GBA) / Bruhat Bengaluru Mahanagara Palike (BBMP) Health Department. The repository currently serves as the initial architectural discovery and project proposal repository.

```
+-------------------------------------------------------------------------+
|                      REPOSITORY AUDIT SUMMARY MATRIX                     |
+------------------------------------+------------------------------------+
| Repository URI                     | https://github.com/saimaa0910/mvp  |
| Active Workspace Directory         | d:\\clone\\mvp                       |
| Current Working Branch             | planning/master-project-plan       |
| Initial Commit SHA                 | c7927d46bdfa6504c0c3a950dfc1aff8f  |
| Authoritative Proposal PDF         | K_Mati_Namma_Clinic_Proposal.pdf   |
| Pre-existing Discovery Files       | 20 Markdown/YAML Documents         |
| Pre-existing Implementation Code   | 0 Lines (Clean Greenfield State)   |
| Production Application Ready       | NO (Planning Baseline Mandatory)   |
+------------------------------------+------------------------------------+
```

---

### 2. Comprehensive File System & Artifact Inventory

| Category | File Path | Size (Bytes) | Nature / Role in Baseline |
| :--- | :--- | :--- | :--- |
| **Root Proposal** | `K_Mati_Namma_Clinic_Detailed_Project_Proposal.pdf` | 516,624 | Authoritative commercial & operational proposal submitted to GBA / BBMP. |
| **Root Metadata** | `README.md` | 21 | Initial 3-line stub repository description. |
| **Phase 0 Discovery**| `docs/phase-0/01_stakeholder_field_research_report.md` | 17,382 | Field observations across 12 high-volume BBMP primary clinics. |
| **Phase 0 Discovery**| `docs/phase-0/02_workflow_mapping.md` | 25,823 | Baseline workflow maps: Registration, Doctor, Pharmacy, Lab. |
| **Phase 0 Discovery**| `docs/phase-0/03_technical_discovery_report.md` | 17,736 | Connectivity, hardware, printer, and power audits in pilot clinics. |
| **Phase 0 Discovery**| `docs/phase-0/04_detailed_project_report_DPR.md` | 29,169 | Detailed Project Report specifying pilot milestones, budget, scope. |
| **Phase 0 Discovery**| `docs/phase-0/05_executive_pitch_deck.md` | 6,504 | Presentation outline for GBA / BBMP Special Commissioner. |
| **Phase 0 Discovery**| `docs/phase-0/06_pilot_term_sheet.md` | 7,145 | Commercial term sheet for 20-clinic pilot deployment. |
| **Phase 0 Discovery**| `docs/phase-0/07_data_privacy_governance.md` | 10,453 | Preliminary DPDP Act 2023 compliance framework. |
| **Phase 0 Discovery**| `docs/phase-0/08_cover_letter.md` | 3,831 | Formal submission letter to Government of Karnataka. |
| **Technical Docs** | `docs/cross-cutting/technical-docs/01_system_architecture_document.md` | 10,791 | Preliminary C4 architectural blueprint (TD-ARC-01). |
| **Technical Docs** | `docs/cross-cutting/technical-docs/02_openapi_specification.yaml` | 18,878 | Initial 15 REST endpoint definitions (TD-API-02). |
| **Technical Docs** | `docs/cross-cutting/technical-docs/03_database_schema_and_migrations.md` | 14,406 | Initial 15 PostgreSQL 16 DDL tables (TD-DB-03). |
| **Technical Docs** | `docs/cross-cutting/technical-docs/04_operations_and_incident_runbook.md` | 6,567 | Operations, DR, and incident playbooks (TD-OPS-04). |
| **Technical Docs** | `docs/cross-cutting/technical-docs/05_developer_onboarding_guide.md` | 6,126 | Engineering environment setup guide (TD-DEV-05). |
| **Technical Docs** | `docs/cross-cutting/technical-docs/06_analytics_codebook_and_metrics.md` | 6,670 | Public health and clinic operational KPI definitions (TD-ANL-06). |
| **Project Mgmt** | `docs/cross-cutting/project-management/01_core_team_charter.md` | 12,106 | Core team RACI and governance charter (PM-GOV-01). |
| **Project Mgmt** | `docs/cross-cutting/project-management/02_sprint_cadence_and_ceremonies.md` | 7,027 | Scrum ceremonies and fortnightly review framework (PM-AG-02). |
| **Project Mgmt** | `docs/cross-cutting/project-management/03_fortnightly_governance_report_template.md` | 6,386 | Reporting template for BBMP steering committee (PM-REP-03). |
| **Project Mgmt** | `docs/cross-cutting/project-management/04_project_risk_register.md` | 6,277 | Risk register with impact and mitigation strategies (PM-RSK-04). |
| **Project Mgmt** | `docs/cross-cutting/project-management/05_change_management_framework_and_log.md` | 6,526 | Scope control and change approval procedures (PM-CHG-05). |
| **Data Governance** | `docs/cross-cutting/data-governance/01_government_data_ownership_clause.md` | 6,703 | Sovereign data ownership and IP protection clause (DG-OWN-01). |
| **Data Governance** | `docs/cross-cutting/data-governance/02_master_data_dictionary.md` | 9,920 | Foundational data dictionary across 12 domains (DG-DIC-02). |
| **Data Governance** | `docs/cross-cutting/data-governance/03_open_api_data_portability_spec.md` | 5,717 | NDHM / ABDM open export standard specification (DG-EXP-03). |
| **Data Governance** | `docs/cross-cutting/data-governance/04_data_access_audit_logging_spec.md` | 5,692 | Immutable audit log architecture (DG-AUD-04). |
| **Data Governance** | `docs/cross-cutting/data-governance/05_annual_data_governance_review_charter.md` | 5,806 | Annual third-party compliance review charter (DG-REV-05). |
| **User Manuals** | `docs/cross-cutting/user-manuals/01_bilingual_user_manual_kannada_english.md` | 11,210 | Frontline clinic user guide in English & Kannada (UM-BIL-01). |

---

### 3. Empirical Findings & Baseline Registers

#### AUD-FIND-001: Absence of Execution Backlog & Engineering Traceability
- **Category:** Project Management & Agile Architecture
- **Current State:** High-level milestones and sprints outlined in PM-AG-02, but zero granular task or micro-task definitions exist.
- **Target State:** Complete backlog hierarchy (EPIC -> FEAT -> US -> TASK -> MT) with 100% forward and backward traceability.
- **Gap:** 100% missing engineering task breakdowns, story point estimation models, and acceptance test criteria.
- **Impact:** Critical. Engineering teams cannot commence sprints without clear, unambiguous user stories and tasks.
- **Priority:** CRITICAL (P0)
- **Recommendation:** Construct Phase 16 Backlog Master (`docs/16-backlog/`) with 23 Epics, 75 Features, 150 User Stories, and 300 Tasks.
- **Dependency:** Requirements Baseline (Phase 2), Workflow Mapping (Phase 3).
- **Risk:** Uncontrolled scope creep and sprint failure without explicit Definition of Ready (DoR).
- **Decision Required:** Formalize 2-week sprint cadence with 18 sprints across 8 releases.
- **Evidence/Source:** `docs/cross-cutting/project-management/02_sprint_cadence_and_ceremonies.md` line 24.

#### AUD-FIND-002: Relational Data Model Coverage Gap
- **Category:** Database Architecture
- **Current State:** 15 relational tables defined in `03_database_schema_and_migrations.md`.
- **Target State:** Comprehensive enterprise health schema comprising 37 transactional tables + 7 Analytical Fact tables + 8 Dimensional tables.
- **Gap:** Missing core entities: corporations, zones, wards, staff, permissions, user_roles, diagnoses master, lab_tests master, patient_consents, triage_records, visit_diagnoses, medicine_batches, inventory_transactions, suppliers, indents, citizen_feedback, grievances.
- **Impact:** High. Clinical, inventory, and governance workflows cannot persist state without complete entity modeling.
- **Priority:** CRITICAL (P0)
- **Recommendation:** Build complete Phase 7 Data Model (`docs/07-database/`) with 18 design artifacts, column dictionaries, and star schema.
- **Dependency:** Clinical Workflows (Phase 3), ABDM FHIR Standards (Phase 15).
- **Risk:** Schema refactoring churn during implementation if entity relationships are incomplete.
- **Decision Required:** Adopt PostgreSQL 16 with UUIDv7 primary keys, JSONB for dynamic clinical observations, and partitioning for audit logs.
- **Evidence/Source:** `docs/cross-cutting/technical-docs/03_database_schema_and_migrations.md` lines 32-350.

#### AUD-FIND-003: API Contract Scope Discrepancy
- **Category:** API Architecture
- **Current State:** 15 REST endpoints defined in `02_openapi_specification.yaml`.
- **Target State:** 22 API domain specifications covering over 65 discrete endpoints with strict idempotency, rate limiting, and RBAC annotations.
- **Gap:** Missing endpoints for triage records, indents, suppliers, citizen feedback, grievances, batch sync, audit search, and fine-grained permissions.
- **Impact:** High. Frontline UI components and offline sync engines cannot synchronize data without defined REST interfaces.
- **Priority:** CRITICAL (P0)
- **Recommendation:** Establish Phase 8 API Plan (`docs/08-api/`) covering all 22 domains with request/response schemas, error envelopes, and audit triggers.
- **Dependency:** Database Entity Modeling (Phase 7), Security RBAC (Phase 10).
- **Risk:** Contract divergence between frontend engineers and backend API teams.
- **Decision Required:** Standardize on RESTful OpenAPI 3.1 with standardized envelope `{"success": bool, "data": {}, "error": {}, "meta": {}}`.
- **Evidence/Source:** `docs/cross-cutting/technical-docs/02_openapi_specification.yaml`.

#### AUD-FIND-004: Lack of Automated Quality & Validation Framework
- **Category:** Quality Engineering & CI/CD
- **Current State:** Zero test files (`test/`, `spec/`), zero GitHub Actions workflows (`.github/workflows/`), zero issue templates.
- **Target State:** Multi-tier testing strategy (Unit, Integration, E2E, Performance, Security), Automated Planning Validator script, and GitHub governance templates.
- **Gap:** 100% missing testing infrastructure and CI/CD pipeline definitions.
- **Impact:** High. Inability to enforce quality gates or track planning consistency automatically.
- **Priority:** HIGH (P1)
- **Recommendation:** Author Phase 11 QA Strategy (`docs/11-qa/`), Phase 12 DevOps Plan (`docs/12-devops/`), and `scripts/validate_planning.py`.
- **Dependency:** Backlog Traceability (Phase 21).
- **Risk:** Regressions and untracked defects during multi-clinic rollout.
- **Decision Required:** Enforce Gate 1 through Gate 12 before permitting any implementation code.
- **Evidence/Source:** Root directory inspection (`ls -la`).
"""

VS_TARGET_02 = """# ⚖️ Existing vs Target State Architectural Analysis
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PB-GAP-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Comparative Architecture Matrix

| Architectural Dimension | Existing Baseline State | Target Production Architecture | Gap Analysis & Remediation |
| :--- | :--- | :--- | :--- |
| **System Scale & Scope** | Informal pilot proposal for 20 clinics | 183+ Namma Clinics across 8 BBMP/GBA zones; ~4.7M annual visits | Scale multiplier of 9.15x. Requires multi-tier caching, read-replicas, and horizontal scaling. |
| **Application Layer** | Unimplemented conceptual Node/React architecture | Modular Monolith (TypeScript / Next.js / Node 20 LTS) with clean hexagonal domain isolation | Need strict package boundaries, domain interfaces, and DTO validation layers before implementation. |
| **Database Entities** | 15 tables in single schema | 37 Transactional Tables + 7 Star Schema Fact Tables + 8 Dimensions | 30 additional tables required across geographic master, inventory ledger, indents, and grievances. |
| **API Endpoints** | 15 basic REST routes in OpenAPI YAML | 65+ REST endpoints across 22 operational domains | Missing endpoints for indents, batch stock tracking, emergency exceptions, and audit streaming. |
| **Offline Operations** | High-level Service Worker / IndexedDB concept | Production Offline-First Sync Engine with CRDT conflict resolution, offline PIN, and tamper-evident local storage | Full offline state machine, local schema migrations, and sync queue retry architecture required. |
| **Security & RBAC** | Basic JWT and 6 conceptual roles | Fine-grained RBAC with 12 roles, 48 permissions, WebAuthn MFA, and DPDP Act 2023 compliance | Formal permission catalog, session invalidation, and data pseudonymization pipelines required. |
| **Analytics & OLAP** | 6 KPI queries defined in markdown | Star Schema DW with daily Debezium CDC / ELT pipelines, 25 KPI definitions, and zonal dashboards | Dedicated analytical read-store, dimensional modeling, and refresh pipelines required. |
| **AI / Decision Support** | Brief mention of predictive analytics | 3 Decision-Support Models (Stockout, Fever Anomaly, NCD Recall) with strict human-in-the-loop guardrails | Zero autonomous diagnosis policy, explicit physician override logging, and drift monitoring. |
| **Interoperability** | Basic ABHA verification endpoint | Full ABDM M1 (ABHA creation), M2 (HIP), M3 (HIU) with FHIR R4 bundles and eHospital referral bridge | Complete FHIR resource mapping, consent manager webhooks, and retry queues required. |
| **DevOps & Environments**| Conceptual AWS deployment plan | 6-Tier Environment Strategy (Local, Dev, Test, Staging, Pilot, Prod) with Terraform IaC and GitHub Actions CI/CD | Full pipeline definitions, secrets management (HashiCorp Vault/AWS KMS), and DR runbooks required. |

---

### 2. Domain-by-Domain Delta Evaluation

```mermaid
graph TD
    subgraph Current Baseline
        A1[15 DB Tables]
        A2[15 API Routes]
        A3[Unstructured Backlog]
        A4[Zero CI/CD Automation]
    end
    subgraph Target Enterprise Baseline
        B1[37 Transactional Tables + 15 DW Tables]
        B2[65+ Documented API Contracts]
        B3[Backlog: 23 Epics / 75 Feats / 150 Stories / 300 Tasks]
        B4[18 Sprints / 8 Releases / Automated Validator]
    end
    A1 -->|Phase 7 Modeling| B1
    A2 -->|Phase 8 OpenAPI Contracts| B2
    A3 -->|Phase 16 Decomposition| B3
    A4 -->|Phase 12 DevOps & Phase 27 Script| B4
```
"""

TECH_STACK_03 = """# 💻 Technology Stack Inventory & Engineering Standards
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PB-STK-03 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Technology Standards & Architectural Selection

| Layer | Selected Technology | Version | Rationale & Enterprise Standards |
| :--- | :--- | :--- | :--- |
| **Runtime & Language** | Node.js / TypeScript | Node 20.x LTS / TS 5.4+ | Enterprise type safety, high concurrency I/O, shared domain types between client and server. |
| **Backend Framework** | Express.js / Fastify | Fastify 4.x / Express 4.19+ | Low-latency HTTP routing, schema-based JSON serialization, robust plugin architecture. |
| **Frontend Framework** | React / Next.js | React 18.3+ / Next.js 14 LTS | Server-side rendering for executive dashboards, PWA capabilities, optimized bundle chunking. |
| **UI Styling & Tokens** | Tailwind CSS / Vanilla CSS | Tailwind 3.4+ / CSS Modules | Design token consistency, zero runtime CSS overhead, accessible contrast ratios. |
| **Primary Database** | PostgreSQL | PostgreSQL 16.3 (RDS Multi-AZ) | ACID compliance, JSONB document querying, temporal table support, native trigram indexing (`pg_trgm`). |
| **Caching & Queue** | Redis | Redis 7.2 (ElastiCache) | Distributed session storage, token queue state, API rate limiting, and pub/sub for clinic notifications. |
| **Offline Storage** | IndexedDB via Dexie.js | Dexie 4.x | Robust browser-level transactional storage, compound indexing, observable queries for offline sync. |
| **Data Validation** | Zod | Zod 3.23+ | Runtime schema validation, automatic TypeScript inference, single source of truth for DTOs. |
| **ORM / Query Builder** | Prisma / Kysely | Prisma 5.x / Kysely 0.27+ | Type-safe database queries, automated migration management, zero raw-SQL injection risks. |
| **Testing Suite** | Vitest / Playwright / k6 | Vitest 1.6+, Playwright 1.44+, k6 v0.51 | Blazing fast unit tests, cross-browser frontline E2E testing, high-concurrency clinic load simulation. |
| **Containerization** | Docker / Docker Compose | Docker Engine 26+, Compose v2 | Reproducible multi-tier local development, immutable production container images. |
| **IaC & Cloud** | Terraform | Terraform 1.8+ | Declarative cloud infrastructure provisioning across AWS India-South (Mumbai) or Karnataka SDC. |
| **Observability** | Prometheus / Grafana / Loki | OpenTelemetry, Grafana 10+ | Structured JSON logging, RED metrics (Rate, Errors, Duration), clinic connectivity telemetry. |

---

### 2. Engineering Invariants & Constraints
1. **Zero Raw SQL in Application Code:** All database access must pass through repository abstractions using validated ORM/query builders.
2. **Strict Schema Validation:** Every incoming API request body, query parameter, and route parameter must be validated against a Zod schema before hitting business logic.
3. **Immutable Audit Trails:** Audit log records (`access_audit_logs`) must be append-only with cryptographic hashing to prevent tampering.
4. **Bilingual Frontline UI:** Every user-facing UI component must support English and Kannada (`kn_IN`) with zero hardcoded UI strings.
"""

DOC_INVENTORY_04 = """# 📚 Existing Documentation Inventory & Gap Catalog
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PB-DOC-04 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Catalog of Pre-Existing Documents

| Document Name | Location | Primary Author | Purpose & Content | Status in Master Baseline |
| :--- | :--- | :--- | :--- | :--- |
| `01_stakeholder_field_research_report.md` | `docs/phase-0/` | Field Research Team | Observational data on patient wait times, doctor consultation times (avg 4.2 mins), and pharmacy queues. | Incorporated into Phase 2 & 3. |
| `02_workflow_mapping.md` | `docs/phase-0/` | Business Analyst | High-level swimlane diagrams for patient check-in, triage, doctor examination, and drug dispensing. | Expanded into 25 workflows in Phase 3. |
| `03_technical_discovery_report.md` | `docs/phase-0/` | Systems Architect | Hardware audit of 20 pilot clinics: broadband speeds (1-10 Mbps), power cuts (2-4 hrs/day), tablet specs. | Governs Phase 6 & 10 offline designs. |
| `04_detailed_project_report_DPR.md` | `docs/phase-0/` | Program Manager | Comprehensive DPR including budget estimates, staffing allocations, and phase rollout schedules. | Aligned with Phase 1 & 24 timeplans. |
| `01_system_architecture_document.md` | `docs/cross-cutting/technical-docs/` | Solutions Architect | C4 System Context and preliminary component models. | Expanded into 18 architecture docs in Phase 6. |
| `02_openapi_specification.yaml` | `docs/cross-cutting/technical-docs/` | Backend Lead | Initial 15 REST endpoints. | Superseded by 22 API domain plans in Phase 8. |
| `03_database_schema_and_migrations.md` | `docs/cross-cutting/technical-docs/` | Data Architect | Initial 15 DDL tables. | Expanded to 37 core tables + DW schema in Phase 7. |
| `01_core_team_charter.md` | `docs/cross-cutting/project-management/` | PMO | Core team roles, RACI matrix, escalation path. | Reconciled into Phase 1 PM baseline. |
| `01_government_data_ownership_clause.md` | `docs/cross-cutting/data-governance/` | Legal Counsel | Sovereign data ownership agreement ensuring GBA retains 100% data rights. | Enforced in Phase 1 & Phase 10 security. |

---

### 2. Documentation Coverage Gaps Identified
- **GAP-DOC-01:** No formal IEEE 830 / ISO/IEC/IEEE 29148 System Requirements Specification (SRS).
- **GAP-DOC-02:** No granular User Stories with BDD Given/When/Then acceptance criteria.
- **GAP-DOC-03:** No day-level sprint execution plans or Definition of Ready (DoR).
- **GAP-DOC-04:** No comprehensive database column dictionary or primary/foreign key dependency maps.
- **GAP-DOC-05:** No formal Threat Model (STRIDE) or DPDP Act 2023 consent lifecycle specification.
"""

GAP_ANALYSIS_05 = """# 🧩 Comprehensive Codebase & Architecture Gap Analysis
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PB-GAP-05 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Gap Analysis Matrix Across Architectural Dimensions

| Dimension | Target Standard | Current Baseline | Gap Description | Severity | Remediation Plan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Requirements** | Unique, stable IDs (BR, FR, NFR, SEC, OFF) with forward traceability | Text descriptions in DPR without unique IDs | Impossible to verify 100% requirement coverage in tests. | CRITICAL | Generate 17 requirement documents in `docs/02-requirements/`. |
| **Workflows** | 25 End-to-End Clinical & Governance Workflows with Mermaid sequence diagrams | 4 high-level workflows in markdown | Missing emergency exceptions, sync conflicts, grievances, indents, and opening/closing flows. | HIGH | Author 25 detailed workflow specs in `docs/03-workflows/`. |
| **Product Hierarchy** | Domain -> Module -> Feature -> Story -> Task -> Micro-task | Unlinked feature lists in proposal | Engineering teams cannot estimate or implement predictably. | CRITICAL | Construct product hierarchy in `docs/04-product/` & `docs/16-backlog/`. |
| **Data Architecture** | 37 Transactional tables, Star Schema, Column Dictionary, Partitioning | 15 tables with partial index definitions | Missing multi-tier clinic hierarchy, indents, suppliers, and DW fact tables. | CRITICAL | Build complete Phase 7 Data Model in `docs/07-database/`. |
| **API Surface** | 22 API domains, REST contracts, error envelopes, rate limits | 15 basic routes in single YAML | No contracts for queue, indents, referrals, ABDM FHIR bundles. | CRITICAL | Design 22 API domain documents in `docs/08-api/`. |
| **Frontend UI/UX** | 21 Screen specifications, Design Tokens, Bilingual strings, Offline states | High-level screen mentions in user manual | Frontline clinical UI layout, validation, and error states undefined. | HIGH | Author 16 frontend plan documents in `docs/09-frontend/`. |
| **Security & Privacy** | STRIDE threat model, DPDP consent lifecycle, AES-256 encryption, RBAC matrix | High-level data privacy annexure | No formal threat-to-control matrix or key management policy. | CRITICAL | Author 20 security specifications in `docs/10-security/`. |
| **QA & Verification** | Multi-tier test strategy, Playwright E2E patient journeys, Quality gates | Zero test specifications | Inability to run regression or validate offline sync robustness. | HIGH | Author 19 QA strategy documents in `docs/11-qa/`. |
| **DevOps & CI/CD** | 6-Tier Environment Plan, Docker multi-stage builds, IaC, Automated PR checks | Generic AWS deployment text | No deployment automation, rollback strategies, or backup automation. | HIGH | Author 19 DevOps documents in `docs/12-devops/`. |
| **Sprints & Cadence** | 18 Sprints (2-week cadence) mapped to 8 Releases with Day-level tasks | Generic 4-phase rollout schedule | No sprint goals, story point allocations, or exit criteria. | CRITICAL | Build 18 sprint documents in `docs/18-sprints/`. |
"""

TECH_DEBT_06 = """# 💳 Technical Debt Register & Pre-Implementation Risk Log
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PB-DEB-06 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Pre-Implementation Technical Debt Register

| Debt ID | Category | Title & Description | Potential Impact | Remediation Milestone | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TD-001** | Database | Hardcoded Enums in Schema vs Master Tables | Potential downtime when adding new lab tests, drug forms, or clinic specialties. | Sprint 01 (Foundation) | High |
| **TD-002** | Architecture | Monolithic Single-File OpenAPI Specification | Concurrent merge conflicts and unwieldy maintenance in Git. | Sprint 01 (Foundation) | Medium |
| **TD-003** | Offline Sync | Naive Last-Write-Wins (LWW) Conflict Resolution | Risk of overwriting doctor prescription if nurse updates vitals simultaneously. | Sprint 07 (Offline Engine) | Critical |
| **TD-004** | Security | Token-Only In-Memory Authentication | Session hijacking vulnerability on shared clinic terminal desktops. | Sprint 02 (Auth & RBAC) | Critical |
| **TD-005** | Performance | Unindexed JSONB Queries in Clinical Encounters | Query degradation when search volume exceeds 1,000,000 encounters. | Sprint 04 (EMR Core) | High |
| **TD-006** | Localization | String Hardcoding in Frontend UI Drafts | Significant refactoring required if Kannada translations are not externalized from Day 1. | Sprint 03 (Design System) | High |
| **TD-007** | Integration | Mock ABDM Endpoints without Webhook Handlers | Inability to process asynchronous ABHA consent approvals from citizen apps. | Sprint 15 (ABDM M1-M3) | Medium |
| **TD-008** | Data Quality | Lack of Input Sanitization for Vital Signs | Erroneous data entry (e.g., Blood Pressure entered as 1200/80) corrupting analytics. | Sprint 03 (Triage Core) | High |
"""

ASSUMPTIONS_07 = """# 📌 Assumptions, Constraints & Environmental Realities
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PB-CON-07 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Environmental & Operational Realities (From Field Discovery)
- **Power Continuity:** Primary health clinics experience 1 to 4 hours of unannounced power outages weekly; desktop PCs lack centralized generator backup; local UPS lasts max 20 minutes.
- **Network Bandwidth:** Clinics operate on mixed broadband / 4G dongles; average uplink speed fluctuates between 512 Kbps and 4 Mbps, with periodic total disconnection lasting up to 6 hours.
- **Hardware Profile:** Clinics are equipped with 1 desktop PC (Doctor room) and 1 Android 11/12 tablet (Registration/Triage desk). A 2-inch thermal receipt printer is shared via USB/Bluetooth.
- **User Digital Literacy:** Staff nurses and pharmacists possess moderate smartphone literacy but limited enterprise software experience. Data entry must require minimal typing (< 4 clicks per routine action).

---

### 2. Legal, Governance & Policy Constraints
- **DPDP Act 2023:** All citizen health data represents Sensitive Personal Data (SPD); explicit, revocable consent is mandatory; sovereign data localization in India is legally required.
- **Government IP Ownership:** Greater Bengaluru Authority / BBMP retains 100% intellectual property rights to data, schema designs, and operational configurations.
- **Zero Autonomous Clinical AI:** Under Karnataka medical council ethics guidelines, AI may only provide non-binding clinical decision support; human physician sign-off is non-negotiable.
"""

# ==========================================
# PHASE 1: PROJECT MANAGEMENT BASELINE
# ==========================================

CHARTER_01 = """# 📜 Project Charter: Namma Clinic Digital Health Platform
## Greater Bengaluru Authority / BBMP Health Department
**Document Code:** PM-CHA-01 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Project Purpose & Executive Mandate
The Namma Clinic Digital Health & Operations Platform is commissioned by the **Greater Bengaluru Authority (GBA) / BBMP Health Administration** to modernize primary healthcare delivery across Bengaluru's urban clinics. The platform replaces paper-based outpatient registers, manual stock counting, and fragmented reporting with an integrated, offline-first digital operational system.

```mermaid
graph LR
    A[Citizen / Patient] --> B(Namma Clinic Frontline)
    B --> C{Digital Platform}
    C --> D[Doctor EMR-Lite]
    C --> E[Pharmacy & Stock]
    C --> F[Lab & Diagnostics]
    C --> G[Zonal Surveillance]
    G --> H[GBA Executive Command]
```

### 2. Strategic Objectives & Success Targets
1. **Reduce Patient Check-In Time:** Decrease registration and triage wait times from ~15 minutes to under 90 seconds.
2. **Zero Paper Registers:** Transition 100% of daily outpatient, drug dispensing, and laboratory logs to digital records.
3. **Real-Time Medicine Inventory:** Achieve 100% batch-level stock visibility across all 183 clinics to prevent stockouts of vital NCD and antibiotic medications.
4. **Epidemiological Early Warning:** Provide real-time syndromic surveillance (fever spikes, gastroenteritis clusters) at the ward and zonal levels within 4 hours of clinical recording.
5. **ABDM Compliance:** Full readiness for Ayushman Bharat Digital Mission (ABHA creation, linked health records, FHIR R4 interoperability).

### 3. Project Authority & Key Sponsors
- **Executive Sponsor:** Special Commissioner (Health), Greater Bengaluru Authority / BBMP.
- **Clinical Director:** Chief Health Officer (CHO), Public Health Administration, Bengaluru.
- **Lead Delivery Partner:** Kushagramati Analytics Pvt Ltd (K Mati) Consortium.
"""

VISION_02 = """# 🎯 Project Vision, Mission & Strategic Outcomes
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-VIS-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Vision Statement
To establish Namma Clinics as the national gold standard for urban primary healthcare by empowering frontline clinicians with an intuitive, resilient, offline-first digital platform that delivers dignified, rapid care to citizens and actionable epidemiological intelligence to public health administrators.

### 2. The Five Guiding Architectural Principles

```
+-------------------------------------------------------------------------+
|                  FIVE GUIDING ARCHITECTURAL PRINCIPLES                  |
+-------------------+-----------------------------------------------------+
| 1. CLINIC-FIRST   | Minimal typing burden (<4 clicks for routine cases);|
|                   | page transitions under 300 ms; ergonomic UI.        |
+-------------------+-----------------------------------------------------+
| 2. CITIZEN-FIRST  | Dignified service; bilingual slips; privacy rights; |
|                   | minimal wait times; voluntary ABHA integration.     |
+-------------------+-----------------------------------------------------+
| 3. OFFLINE-FIRST  | Uninterrupted clinic operations during total power/ |
|                   | broadband drops; automatic deterministic sync.      |
+-------------------+-----------------------------------------------------+
| 4. SOVEREIGN DATA | 100% GBA ownership; zero vendor lock-in; open data  |
|                   | portability; DPDP Act 2023 compliance.             |
+-------------------+-----------------------------------------------------+
| 5. SAFE AI        | Strict decision support only; zero autonomous diag- |
|                   | nosis; full physician override auditability.        |
+-------------------+-----------------------------------------------------+
```
"""

SCOPE_03 = """# 🌐 Project Scope Management & Boundary Definition
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-SCP-03 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Scope Baseline Overview
The project encompasses the end-to-end planning, architectural design, engineering, validation, pilot deployment (20 clinics), and citywide rollout (183+ clinics) of the Namma Clinic Digital Health Platform.

```mermaid
graph TD
    subgraph IN SCOPE
        A[Urban Primary Clinics 183+]
        B[Outpatient Consultation]
        C[Pharmacy Dispensing & Batch Stock]
        D[Primary Lab Tests 14 Essential]
        E[Secondary Referral Tracking]
        F[Zonal Epidemiological Surveillance]
    end
    subgraph OUT OF SCOPE
        G[Inpatient / ICU Management]
        H[Tertiary Surgical Operations]
        I[Autonomous Diagnostic AI]
        J[Commercial Billing / Cash Collection]
    end
```
"""

IN_SCOPE_04 = """# ✅ Explicit In-Scope Functional & Technical Capabilities
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-INC-04 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. In-Scope Functional Modules
1. **Patient Registration & Queue Management:** Fast search, ABHA verification, token issuance, prioritized triage.
2. **Clinical Encounter & EMR-Lite:** Chief complaints, structured vitals, provisional diagnosis (ICD-10 / SNOMED CT), prescription writing.
3. **Pharmacy & Stock Ledger:** FIFO dispensing, batch number & expiry tracking, low-stock alerts, monthly indent generation.
4. **Laboratory Operations:** Order entry, sample collection logging, result entry for 14 essential primary diagnostic tests.
5. **Referral Gateway:** Outbound referrals to BBMP General Hospitals / Medical Colleges with structured clinical summaries.
6. **Public Health Analytics:** Ward/Zone/City dashboards tracking footfall, top morbidity patterns, NCD prevalence, and medicine consumption.
7. **Offline PWA Architecture:** Full local caching of active clinic sessions with background sync upon reconnection.
"""

OUT_OF_SCOPE_05 = """# ❌ Out-of-Scope Capabilities & System Boundaries
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-OUT-05 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Explicitly Excluded Features
1. **Inpatient Department (IPD) & Bed Management:** Namma Clinics are strictly outpatient primary facilities.
2. **Billing, Payments & Fee Collection:** All clinical consultations, tests, and medicines are 100% free under GBA / BBMP policy.
3. **Autonomous AI Prescriptions:** AI will never generate final prescriptions or diagnoses without explicit doctor review.
4. **Complex Tertiary Imaging (PACS):** No MRI, CT, or complex radiology PACS archiving.
5. **Payroll & HR Financial Management:** Staff salary processing remains in existing BBMP HRMS systems.
"""

STAKEHOLDERS_06 = """# 👥 Stakeholder Register & Engagement Strategy
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-STK-06 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Key Stakeholders

| Stakeholder Name / Title | Organization | Role in Project | Engagement Level | Key Concerns |
| :--- | :--- | :--- | :--- | :--- |
| **Special Commissioner (Health)** | GBA / BBMP | Executive Sponsor | Fortnightly Review | Project timeline, budget adherence, public visibility. |
| **Chief Health Officer (CHO)** | BBMP Health | Clinical Authority | Weekly Steering | Clinical safety, formulary compliance, doctor adoption. |
| **Zonal Health Officers (ZHOs)** | 8 BBMP Zones | Operational Leads | Bi-weekly Sync | Zonal coverage, clinic staffing, stock availability. |
| **Medical Officers (Doctors)** | Namma Clinics | Primary End Users | Daily Frontline | Typing burden, consultation speed, software stability. |
| **Staff Nurses / ANMs** | Namma Clinics | Frontline Operators | Daily Frontline | Registration speed, token flow, Kannada UI clarity. |
| **Pharmacists** | Namma Clinics | Stock Managers | Daily Frontline | Batch inventory accuracy, expiry tracking, physical counts. |
| **Citizens of Bengaluru** | Public | Beneficiaries | Ongoing Feedback | Dignified service, minimal wait, free medicines. |
"""

PERSONAS_07 = """# 👤 User Personas & Clinical Archetypes
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-PER-07 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Primary Clinical Personas

#### Persona 1: Sister Shobha (Staff Nurse / Registration Desk)
- **Age:** 34 | **Facility:** Namma Clinic Ward 150 (Bellandur) | **Language:** Kannada (Primary), English (Functional)
- **Key Tasks:** Patient registration, vitals recording (BP, Pulse, SpO2, Blood Glucose), token generation.
- **Pain Points:** Crowded waiting area in mornings; erratic internet; difficulty typing complex medical words in English.
- **Platform Need:** 3-step Kannada touchscreen workflow; offline tablet capability; fast thermal token print.

#### Persona 2: Dr. Ramesh Kumar (Medical Officer)
- **Age:** 42 | **Facility:** Namma Clinic Ward 112 (Domlur) | **Experience:** 14 years urban clinical practice
- **Key Tasks:** Patient examination, diagnosis, electronic prescription, lab test ordering, referral decisions.
- **Pain Points:** High patient load (80-100 patients/day); cannot spend more than 2 minutes typing per consultation.
- **Platform Need:** 1-click clinical chief complaint chips; favorite prescription bundles; quick historical visit view.

#### Persona 3: Sri Anand (Clinic Pharmacist)
- **Age:** 28 | **Facility:** Namma Clinic Ward 75 | **Key Tasks:** Drug dispensing, batch verification, physical inventory.
- **Pain Points:** Discrepancies between physical stock and register; near-expiry medicine waste; manual indent writing.
- **Platform Need:** Barcode/quick-search dispensing; automated FEFO (First Expiry, First Out) prompts; 1-click monthly indent.
"""

RACI_08 = """# 📊 Project RACI Matrix & Authority Delegation
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-RAC-08 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Enterprise RACI Matrix across 18 Delivery Functions

*R = Responsible, A = Accountable, C = Consulted, I = Informed*

| Functional Area | Executive Sponsor (GBA) | Program Manager (K Mati) | Solution Architect | Lead DB / Backend | Frontend Lead | Clinical Advisor | Security Lead | QA Lead | DevOps Lead |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Project Charter & Scope** | **A** | **R** | C | I | I | C | I | I | I |
| **Requirements Baseline** | I | **A** | C | C | C | **R** | C | C | I |
| **Architecture Blueprint** | I | A | **R** | C | C | C | C | I | C |
| **Data Model & Schema** | I | A | C | **R** | I | C | C | I | I |
| **API Contract Design** | I | A | C | **R** | C | I | C | C | I |
| **Frontend UI/UX Design** | I | A | I | I | **R** | C | I | C | I |
| **Security & DPDP Compliance**| C | A | C | C | C | I | **R** | C | C |
| **QA Test Automation** | I | A | I | C | C | I | C | **R** | C |
| **CI/CD & Cloud IaC** | I | A | C | I | I | I | C | C | **R** |
| **Sprint Execution** | I | **A** | C | **R** | **R** | C | C | **R** | **R** |
| **Pilot Rollout (20 Clinics)** | C | **A** | C | C | C | **R** | C | C | C |
| **Citywide Deployment** | **A** | **R** | C | C | C | C | C | C | C |
"""

GOVERNANCE_09 = """# 🏛️ Project Governance Model & Steering Structure
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-GOV-09 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Three-Tier Governance Framework

```mermaid
graph TD
    subgraph Tier 1: Executive Steering Committee
        A[GBA Special Commissioner / BBMP CHO]
        A --> B[Fortnightly Executive Review]
    end
    subgraph Tier 2: Operational Program Management
        C[K Mati Program Manager & Zonal Health Officers]
        C --> D[Weekly Progress & Blocker Sync]
    end
    subgraph Tier 3: Technical & Clinical Working Group
        E[Solution Architect, Clinical Lead, Tech Leads]
        E --> F[Daily Standups & Mid-Sprint Demos]
    end
```

### 2. Decision Thresholds & Escalation Path
- **Level 1 (Operational / Technical):** Resolved within 24 hours by Lead Architect and Program Manager.
- **Level 2 (Clinical / Workflow Scope):** Resolved within 48 hours by BBMP Clinical Advisory Committee.
- **Level 3 (Contractual / Budget / Strategic):** Escalated to GBA Special Commissioner for formal resolution.
"""

ASSUMPTIONS_10 = """# 📋 Project Assumptions Register
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-ASM-10 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Key Project Assumptions
- **ASM-001:** GBA/BBMP will provide designated pilot clinic access and assign 1 focal point per clinic.
- **ASM-002:** Hardware procurement (tablets, desktops, printers) will be completed by BBMP prior to Sprint 11 (Pilot).
- **ASM-003:** Broadband/4G SIM data connections will be funded and maintained under BBMP operational contracts.
- **ASM-004:** Doctors and staff will be released for mandatory 4-hour hands-on training prior to clinic go-live.
"""

CONSTRAINTS_11 = """# ⛓️ Project Constraints & Boundary Conditions
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-CST-11 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Constraints Register
- **CST-001 (Time):** Pilot deployment of 20 clinics must be operational within 22 weeks of project authorization.
- **CST-002 (Language):** All patient-facing slips and frontline forms must fully support Kannada (`kn_IN`).
- **CST-003 (Security):** System must pass external CERT-In certified VAPT prior to citywide production rollout.
- **CST-004 (Infrastructure):** Application must run seamlessly on low-spec hardware (Android 11 tablet, 3GB RAM).
"""

RISKS_12 = """# 🛡️ Comprehensive Project Risk Register
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-RSK-12 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Top Project Risks & Mitigation Strategies

| Risk ID | Category | Risk Description | Probability | Impact | Score | Mitigation Strategy | Owner |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **RSK-001** | Technical | Prolonged clinic internet outage causing offline sync queue buildup. | High | High | **16** | Robust IndexedDB offline queue with progressive chunked sync and conflict resolution. | Tech Lead |
| **RSK-002** | User Adoption | Doctor resistance to typing electronic prescriptions during peak hours. | High | Critical | **20** | 1-click pre-configured medication bundles; chief complaint chips; minimal typing UX. | Clinical Lead |
| **RSK-003** | Operational | Hardware theft or physical tablet damage in clinic premises. | Med | Med | **9** | Device MDM lock; encrypted local storage; fast spare swap provisioning within 4 hours. | DevOps Lead |
| **RSK-004** | Compliance | Non-compliance with evolving DPDP Act rules regarding minor consent. | Med | High | **12** | Mandatory guardian consent workflow for patients under 18 years old. | Legal / Sec Lead |
"""

DEPENDENCIES_13 = """# 🔗 Master Project Dependency Register
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-DEP-13 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. External & Cross-Cutting Dependencies
- **DEP-001:** GBA/BBMP approval of 20 pilot clinic list (Due before Sprint 05).
- **DEP-002:** Allocation of cloud hosting tenancy in Karnataka SDC or AWS GCC (Due before Sprint 03).
- **DEP-003:** Issuance of DLT-approved SMS sender ID and WhatsApp Business API credentials (Due before Sprint 08).
- **DEP-004:** ABDM sandbox credentials and client secret provisioning by National Health Authority (Due before Sprint 14).
"""

MILESTONES_14 = """# 🚩 Project Milestones & Target Completion Schedule
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-MLS-14 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Master Milestone Schedule

```
+-------------------------------------------------------------------------+
|                       MASTER MILESTONE SCHEDULE                         |
+-----+--------------------------------------+----------+-----------------+
| ID  | Milestone Description                | Sprint   | Target Timeline |
+-----+--------------------------------------+----------+-----------------+
| M01 | Planning & Engineering Baseline Gate | Pre-S01  | Week 0 (Current)|
| M02 | Core Architecture & Foundation       | S01-S02  | Week 4          |
| M03 | Patient Registration & Triage Vitals | S03-S04  | Week 8          |
| M04 | Doctor Consultation & EMR-Lite       | S05-S06  | Week 12         |
| M05 | Pharmacy, Stock Ledger & Lab Orders  | S07-S08  | Week 16         |
| M06 | Offline PWA & Sync Engine Hardening  | S09-S10  | Week 20         |
| M07 | 20-Clinic Pilot Go-Live & Review     | S11-S12  | Week 24         |
| M08 | Zonal Dashboards & Field Hardening   | S13-S14  | Week 28         |
| M09 | ABDM M1-M3 & Safe AI Surveillance    | S15-S16  | Week 32         |
| M10 | Full 183-Clinic Citywide Rollout     | S17-S18  | Week 36         |
+-----+--------------------------------------+----------+-----------------+
```
"""

RELEASE_STRAT_15 = """# 🚀 Software Release Strategy (Releases 00 through 07)
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-REL-15 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Phased Release Architecture

| Release ID | Name / Codename | Sprints | Primary Focus & Deliverables |
| :--- | :--- | :--- | :--- |
| **REL-00** | Foundation & Core Infra | S01 - S02 | DB Schema, Base APIs, Auth/RBAC, Audit Logging, CI/CD pipelines. |
| **REL-01** | Core Patient & Queue | S03 - S04 | Patient Registration, Demographics, Token Generation, Vitals Triage. |
| **REL-02** | Clinical Encounter & EMR | S05 - S06 | Doctor Console, Diagnosis Coding, Electronic Prescription, History. |
| **REL-03** | Pharmacy, Lab & Referral| S07 - S08 | Drug Dispensing, Batch Tracking, 14 Lab Tests, Outbound Referrals. |
| **REL-04** | Analytics & Offline Core | S09 - S10 | IndexedDB Offline Cache, Background Sync, Public Health Metrics DW. |
| **REL-05** | 20-Clinic Pilot Release | S11 - S12 | Field Deployment across 20 Clinics, SLA Monitoring, User Feedback. |
| **REL-06** | Production Citywide Scale| S13 - S14 | Performance Tuning, High-Concurrency Load, Rollout to 183 Clinics. |
| **REL-07** | AI Insights & ABDM Native| S15 - S16 | Stock Forecasting, Fever Anomaly Alerts, ABHA Linking, FHIR R4. |
"""

DOR_16 = """# 🚦 Definition of Ready (DoR) for Backlog Intake
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-DOR-16 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Quality Criteria for Backlog Intake
A User Story or Engineering Task is strictly **READY** for sprint planning if and only if:
1. **Business Value & Persona Defined:** Role, user intent, and public health rationale are clearly articulated.
2. **BDD Acceptance Criteria Specified:** Given/When/Then scenarios cover primary, alternative, and error flows.
3. **Traceability Linked:** Connected to stable Requirement ID (`BR-xxx`, `FR-xxx`, `NFR-xxx`).
4. **Architectural Dependencies Resolved:** Database schema, API contracts, and UI mockups are finalized.
5. **Estimate & Story Points Assigned:** Sized by engineering team using modified Fibonacci points (1, 2, 3, 5, 8).
6. **Security & Privacy Tagged:** PII exposure risks, RBAC permissions, and audit log events explicitly stated.
"""

DOD_17 = """# 🏁 Definition of Done (DoD) for Sprint Delivery
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-DOD-17 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Quality Criteria for Sprint Completion
A User Story or Engineering Task is strictly **DONE** if and only if:
1. **Code & Contract Quality:** Code written in strict TypeScript; zero lint errors; clean architectural boundary compliance.
2. **Automated Unit & Integration Tests:** Unit test coverage >= 85%; all integration contract tests passing cleanly.
3. **E2E Validation:** Critical patient flow automated in Playwright with zero flaky test retries.
4. **Offline Resilience Validated:** Tested with simulated network disconnections and IndexedDB sync verification.
5. **Bilingual Verification:** English and Kannada UI text validated by bilingual clinical coordinator.
6. **Security & Audit Sign-Off:** All sensitive patient data access generates an immutable audit record; no plaintext PII in logs.
7. **CI/CD Quality Gate Passed:** Automated build, container security scan (Trivy), and SonarQube quality gate green.
"""

CHANGE_MGMT_18 = """# 🔄 Change Management Framework & Scope Control Log
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-CHG-18 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Change Control Process (RFC Workflow)
1. **Submission:** Change Request (CR) submitted via GitHub issue using `type:change-request` template.
2. **Impact Assessment:** Architect and PM evaluate impact on schedule, budget, clinical safety, and dependencies within 48 hours.
3. **Change Control Board (CCB) Review:** Convened weekly or ad-hoc with BBMP Clinical Representative.
4. **Approval / Rejection:** Documented in Change Log with explicit baseline revision number.
"""

COMM_PLAN_19 = """# 📢 Stakeholder Communication & Reporting Plan
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-COM-19 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Communication Cadence

| Meeting / Artifact | Frequency | Participants | Purpose |
| :--- | :--- | :--- | :--- |
| **Daily Engineering Standup** | Daily (09:30) | Engineering Leads, Scrum Master | Blocker identification, daily sprint progress. |
| **Weekly Technical Sync** | Weekly (Wed) | Solution Architect, Dev Leads, QA | Architectural alignment, API contract sign-off. |
| **Fortnightly Governance Report**| Fortnightly | Special Commissioner, CHO, PM | Progress tracking against milestones, risks, budget. |
| **Monthly Field Clinic Review** | Monthly | Zonal Health Officers, Doctors | Frontline usability feedback, training refreshers. |
"""

STATUS_MODEL_20 = """# 🚦 Project Health Status Model & KPI Indicators
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-STA-20 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Project Health Status Definitions
- 🟢 **GREEN (On Track):** Milestones within <= 3 days of plan; no blocking P0 risks; test pass rate >= 98%.
- 🟡 **AMBER (At Risk):** Milestone delay between 4-7 days; 1 or more unresolved P1 blockers; test pass rate 90-97%.
- 🔴 **RED (Critical Escalation):** Milestone delay > 7 days; any unmitigated P0 security or clinical risk; test pass rate < 90%.
"""

def main():
    base_dir = "docs"
    # Phase 0
    write_file(os.path.join(base_dir, "00-project-baseline", "01-repository-audit.md"), AUDIT_01)
    write_file(os.path.join(base_dir, "00-project-baseline", "02-existing-vs-target-state.md"), VS_TARGET_02)
    write_file(os.path.join(base_dir, "00-project-baseline", "03-technology-stack-inventory.md"), TECH_STACK_03)
    write_file(os.path.join(base_dir, "00-project-baseline", "04-existing-documentation-inventory.md"), DOC_INVENTORY_04)
    write_file(os.path.join(base_dir, "00-project-baseline", "05-codebase-gap-analysis.md"), GAP_ANALYSIS_05)
    write_file(os.path.join(base_dir, "00-project-baseline", "06-technical-debt-register.md"), TECH_DEBT_06)
    write_file(os.path.join(base_dir, "00-project-baseline", "07-assumptions-and-constraints.md"), ASSUMPTIONS_07)

    # Phase 1
    write_file(os.path.join(base_dir, "01-project-management", "01-project-charter.md"), CHARTER_01)
    write_file(os.path.join(base_dir, "01-project-management", "02-project-vision-and-objectives.md"), VISION_02)
    write_file(os.path.join(base_dir, "01-project-management", "03-project-scope.md"), SCOPE_03)
    write_file(os.path.join(base_dir, "01-project-management", "04-in-scope.md"), IN_SCOPE_04)
    write_file(os.path.join(base_dir, "01-project-management", "05-out-of-scope.md"), OUT_OF_SCOPE_05)
    write_file(os.path.join(base_dir, "01-project-management", "06-stakeholders.md"), STAKEHOLDERS_06)
    write_file(os.path.join(base_dir, "01-project-management", "07-user-personas.md"), PERSONAS_07)
    write_file(os.path.join(base_dir, "01-project-management", "08-role-and-responsibility-matrix.md"), RACI_08)
    write_file(os.path.join(base_dir, "01-project-management", "09-governance-model.md"), GOVERNANCE_09)
    write_file(os.path.join(base_dir, "01-project-management", "10-project-assumptions.md"), ASSUMPTIONS_10)
    write_file(os.path.join(base_dir, "01-project-management", "11-project-constraints.md"), CONSTRAINTS_11)
    write_file(os.path.join(base_dir, "01-project-management", "12-project-risks.md"), RISKS_12)
    write_file(os.path.join(base_dir, "01-project-management", "13-project-dependencies.md"), DEPENDENCIES_13)
    write_file(os.path.join(base_dir, "01-project-management", "14-project-milestones.md"), MILESTONES_14)
    write_file(os.path.join(base_dir, "01-project-management", "15-release-strategy.md"), RELEASE_STRAT_15)
    write_file(os.path.join(base_dir, "01-project-management", "16-definition-of-ready.md"), DOR_16)
    write_file(os.path.join(base_dir, "01-project-management", "17-definition-of-done.md"), DOD_17)
    write_file(os.path.join(base_dir, "01-project-management", "18-change-management.md"), CHANGE_MGMT_18)
    write_file(os.path.join(base_dir, "01-project-management", "19-communication-plan.md"), COMM_PLAN_19)
    write_file(os.path.join(base_dir, "01-project-management", "20-project-status-model.md"), STATUS_MODEL_20)

if __name__ == "__main__":
    main()
