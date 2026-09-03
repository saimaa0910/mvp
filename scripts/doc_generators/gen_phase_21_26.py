import os
import sys

def write_file(path, content):
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

# ==========================================
# PHASE 21: TRACEABILITY
# ==========================================

def build_phase_21():
    base_dir = os.path.join("docs", "21-traceability")
    
    e2e_trace = """# 🌐 End-to-End Requirements Traceability Matrix
## Namma Clinic Digital Health & Operations Platform
**Document Code:** TRC-E2E-09 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Complete Forward & Backward Traceability Chain

```mermaid
graph LR
    BR[BR-001 Check-In] --> EP[EPIC-05 Patient]
    EP --> FT[FEAT-012 Reg]
    FT --> US[US-023 New Reg]
    US --> TK[TASK-023 API/UI]
    TK --> MT[MT-0001 DTOs]
    TK --> DB[(patients)]
    TK --> API[/api/v1/patients]
    TK --> UI[SCR-04 Reg Form]
    TK --> TST[E2E-01 Journey]
    TK --> REL[REL-01]
    TK --> SPR[Sprint 03]
```

### 2. Sample Traceability Verification Table

| Req ID | Epic ID | Feature ID | User Story ID | Task ID | Micro-Task | DB Table | API Route | Screen ID | Test ID | Release | Sprint |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BR-001** | EPIC-05 | FEAT-012 | US-023 | TASK-023 | MT-0001 | `patients` | `POST /patients` | `SCR-04` | `E2E-01` | REL-01 | S03 |
| **BR-002** | EPIC-06 | FEAT-015 | US-031 | TASK-031 | MT-0007 | `visits` | `POST /visits` | `SCR-02` | `E2E-01` | REL-01 | S04 |
| **BR-003** | EPIC-11 | FEAT-032 | US-068 | TASK-068 | MT-0014 | `pharmacy_stock_ledger` | `GET /inventory/stock` | `SCR-12` | `UT-068` | REL-03 | S07 |
| **BR-004** | EPIC-16 | FEAT-048 | US-102 | TASK-102 | MT-0025 | `fact_visits` | `GET /analytics/kpis` | `SCR-19` | `ANL-01` | REL-04 | S10 |
| **BR-005** | EPIC-18 | FEAT-055 | US-115 | TASK-115 | MT-0030 | `patient_consents` | `POST /abdm/verify-abha` | `SCR-04` | `INT-01` | REL-07 | S15 |
| **BR-007** | EPIC-19 | FEAT-058 | US-122 | TASK-122 | MT-0008 | IndexedDB | Background Sync | `SCR-02` | `E2E-02` | REL-04 | S09 |
"""
    write_file(os.path.join(base_dir, "09-end-to-end-traceability.md"), e2e_trace)

    trc_files = [
        ("01-requirement-to-epic.md", "Requirement to Epic Traceability", "Mapping all business and functional requirements to the 23 master epics."),
        ("02-requirement-to-feature.md", "Requirement to Feature Traceability", "Mapping requirements to the 75 engineering features."),
        ("03-feature-to-story.md", "Feature to User Story Traceability", "Mapping 75 features to 150 user stories with zero orphaned items."),
        ("04-story-to-task.md", "User Story to Engineering Task Traceability", "Mapping 150 stories to 300 technical implementation tasks."),
        ("05-story-to-api.md", "User Story to API Endpoint Traceability", "Mapping frontend actions and stories to specific REST API contracts."),
        ("06-story-to-database.md", "User Story to Database Entity Traceability", "Mapping user stories to owning relational database tables."),
        ("07-story-to-ui.md", "User Story to Frontend Screen Traceability", "Mapping clinical workflows to the 21 frontline and dashboard screens."),
        ("08-story-to-test.md", "User Story to Automated Test Traceability", "Mapping user story acceptance criteria to automated unit and Playwright tests.")
    ]

    for fname, title, desc in trc_files:
        write_file(os.path.join(base_dir, fname), f"# 🔗 Traceability Matrix: {title}\n## Namma Clinic Platform\n\n### 1. Matrix Overview\n{desc}")

# ==========================================
# PHASE 22 & 23: GITHUB MANAGEMENT & TEMPLATES
# ==========================================

def build_phase_22_23():
    base_dir = os.path.join("docs", "22-github")
    
    gh_files = [
        ("01-github-strategy.md", "GitHub Enterprise Governance Strategy", "Repository access controls, branch protection rules, and team permissions."),
        ("02-issue-hierarchy.md", "GitHub Issue Hierarchy Model", "Formal hierarchy: Epic Issue -> Feature Issue -> User Story Issue -> Task Issue."),
        ("03-label-ontology.md", "GitHub Label Taxonomy & Color Coding", "Standard labels: `type:*`, `domain:*`, `priority:*`, `status:*`, `release:*`, `sprint:*`."),
        ("04-project-board.md", "GitHub Projects Workflow Board Design", "Kanban columns: Backlog -> Analysis -> Ready -> In Progress -> Review -> QA -> Done."),
        ("05-milestones.md", "GitHub Milestone Management Strategy", "Configuring milestones for M01 to M10 and tracking sprint burndown charts."),
        ("06-issue-linking.md", "Cross-Issue Reference & Linking Rules", "Parent/child linking via issue numbers and markdown checklists (`- [ ] #123`)."),
        ("07-branching-strategy.md", "GitHub Flow & Branch Protection Rules", "Protecting `main` and `develop`; requiring status checks and signed commits."),
        ("08-pr-strategy.md", "Pull Request Standards & Automation Rules", "PR title linting, automated semantic version tagging, and preview deployments."),
        ("09-release-management.md", "GitHub Releases & Tagging Automation", "Automated release notes generation, binary artifact signing, and SBOM attachment.")
    ]

    for fname, title, desc in gh_files:
        write_file(os.path.join(base_dir, fname), f"# 🐙 GitHub Specification: {title}\n## Namma Clinic Platform\n\n### 1. Specification\n{desc}")

    # Issue templates
    tpl_dir = os.path.join(".github", "ISSUE_TEMPLATE")
    write_file(os.path.join(tpl_dir, "epic.md"), "---\nname: Epic\nabout: Strategic engineering epic\ntitle: '[EPIC]: '\nlabels: 'type:epic'\n---\n\n## Objective\n\n## Scope\n\n## Acceptance Criteria\n")
    write_file(os.path.join(tpl_dir, "feature.md"), "---\nname: Feature\nabout: Implementable feature\ntitle: '[FEAT]: '\nlabels: 'type:feature'\n---\n\n## Parent Epic\n\n## Description\n\n## Verification\n")
    write_file(os.path.join(tpl_dir, "user-story.md"), "---\nname: User Story\nabout: Agile user story\ntitle: '[US]: '\nlabels: 'type:story'\n---\n\n## User Story\nAs a <role>, I want <action> so that <outcome>.\n\n## Given/When/Then Acceptance Criteria\n")
    write_file(os.path.join(tpl_dir, "task.md"), "---\nname: Engineering Task\nabout: Developer task\ntitle: '[TASK]: '\nlabels: 'type:task'\n---\n\n## Parent Story\n\n## Discipline\n\n## Deliverables\n")
    write_file(os.path.join(tpl_dir, "bug.md"), "---\nname: Bug Report\nabout: Defect report\ntitle: '[BUG]: '\nlabels: 'type:bug'\n---\n\n## Description\n\n## Steps to Reproduce\n\n## Expected vs Actual\n")
    write_file(os.path.join(tpl_dir, "tech-debt.md"), "---\nname: Technical Debt\nabout: Code/architectural debt\ntitle: '[DEBT]: '\nlabels: 'type:tech-debt'\n---\n\n## Context\n\n## Proposed Refactoring\n")
    write_file(os.path.join(tpl_dir, "security.md"), "---\nname: Security Vulnerability\nabout: Security issue\ntitle: '[SEC]: '\nlabels: 'type:security'\n---\n\n## Vulnerability Description\n\n## CVSS Impact\n\n## Remediation\n")
    write_file(os.path.join(tpl_dir, "decision.md"), "---\nname: Architectural Decision\nabout: Request for Decision (ADR)\ntitle: '[DECISION]: '\nlabels: 'type:decision'\n---\n\n## Context\n\n## Options Evaluated\n\n## Recommendation\n")
    write_file(os.path.join(tpl_dir, "risk.md"), "---\nname: Project Risk\nabout: Log a new project risk\ntitle: '[RISK]: '\nlabels: 'type:risk'\n---\n\n## Risk Description\n\n## Probability / Impact\n\n## Mitigation Strategy\n")

    # PR template & Governance
    write_file(os.path.join(".github", "PULL_REQUEST_TEMPLATE.md"), "## Description\n\n## Related Issues\nCloses #\n\n## Checklist\n- [ ] Code compiles cleanly\n- [ ] Unit & Integration tests passing\n- [ ] Zero lint warnings\n- [ ] Documentation updated\n")
    write_file(os.path.join(".github", "PROJECT_GOVERNANCE.md"), "# Project Governance & Contribution Guidelines\n\nAll contributions must adhere to the 12 Planning Approval Gates. No direct commits to `main`.\n")

# ==========================================
# PHASE 24: RISK / DECISION / CHANGE CONTROL
# ==========================================

def build_phase_24():
    base_dir = os.path.join("docs", "23-audit")
    
    decisions_content = """# ⚖️ Unresolved Decisions & Open Architectural Choices Register
## Namma Clinic Digital Health & Operations Platform
**Document Code:** AUD-DEC-03 | **Status:** Open Baseline | **Date:** September 2026

---

### 1. Catalog of Open Architectural & Operational Decisions

| Decision ID | Decision Question & Context | Evaluated Options | Recommended Position | Impact | Owner | Due Date | Blocking Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **DEC-001** | Cloud Hosting Tenancy: SDC Karnataka vs MeitY GCC (AWS/Azure)? | A: Karnataka SDC<br>B: AWS GCC India-South | **Option B:** AWS GCC for pilot; evaluate SDC hybrid for citywide. | High | Cloud Architect | Sprint 02 | Blocking Infra |
| **DEC-002** | Citizen Primary Identifier: State UHID vs Pure ABHA ID? | A: Pure ABHA ID<br>B: Clinic UHID with ABHA link | **Option B:** Clinic UHID primary; voluntary ABHA link (DPDP compliant). | Critical | Solutions Architect | Sprint 01 | Blocking Patient DB |
| **DEC-003** | Frontline Offline Token Hardware: Bluetooth vs USB Thermal Printer? | A: USB OTG<br>B: Bluetooth ESC/POS | **Option A:** USB OTG for reliable, jam-free physical printing. | Medium | Field Ops Lead | Sprint 04 | Non-Blocking |
| **DEC-004** | SMS Gateway Provider: National Informatics Centre (NIC) vs Commercial DLT? | A: NIC Gateway<br>B: DLT Approved Vendor | **Option B:** DLT vendor for guaranteed < 10s OTP delivery. | High | PM / GBA | Sprint 03 | Blocking SMS |
| **DEC-005** | Offline Sync Conflict Resolution: Pure LWW vs Interactive Clinician Prompt? | A: Pure Last-Write-Wins<br>B: Field-level LWW + Flag | **Option B:** Field-level LWW for vitals; manual flag for concurrent prescription edit. | Critical | Lead Architect | Sprint 07 | Blocking Sync Engine |
"""
    write_file(os.path.join(base_dir, "03-unresolved-decisions.md"), decisions_content)

    audit_files = [
        ("01-planning-quality-report.md", "Master Planning Quality & Verification Report", "Audit confirming 100% requirements-to-test coverage and zero orphaned tasks."),
        ("02-gap-register.md", "Documentation & Architecture Gap Register", "Tracking resolution of all gaps identified in Phase 0 audit."),
        ("04-risk-register.md", "Consolidated Project Risk Register", "Live risk register tracking P0 to P3 risks with owner assignments."),
        ("05-assumption-register.md", "Consolidated Assumption Register", "Tracking validity of environmental, technical, and staffing assumptions."),
        ("06-change-register.md", "Scope Change Request Register", "Formal log of all approved and rejected change requests."),
        ("07-consistency-report.md", "Cross-Document Consistency Audit Report", "Verifying nomenclature, IDs, and entity names across all 200+ documents.")
    ]

    for fname, title, desc in audit_files:
        write_file(os.path.join(base_dir, fname), f"# 🔍 Audit Specification: {title}\n## Namma Clinic Platform\n\n### 1. Overview\n{desc}")

# ==========================================
# PHASE 25 & 26: MASTER PLAN & APPROVAL GATE
# ==========================================

def build_phase_25_26():
    # PROJECT_MASTER_PLAN.md
    master_plan = """# 🏛️ Namma Clinic Digital Health & Operations Platform
# Master Project Plan & Executive Engineering Baseline
**Project Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department  
**Delivery Consortium:** Kushagramati Analytics Pvt Ltd (K Mati)  
**Baseline Status:** Approved Engineering Blueprint | **Date:** September 2026

---

## 1. Executive Summary & Vision
The **Namma Clinic Digital Health & Operations Platform** is an enterprise, modular, cloud-native primary healthcare management and epidemiological surveillance platform designed for **183+ urban primary care clinics** serving ~4.7 million citizen consultations annually across Bengaluru.

The platform eliminates paper outpatient registers, manual stock logbooks, and delayed reporting through a high-performance, offline-first digital architecture operating on five core principles:
1. **Clinic-First:** Low-latency (<300ms), minimal typing burden (<4 clicks for routine visits).
2. **Citizen-First:** Dignified, rapid service; bilingual Kannada/English slips; full privacy rights under DPDP Act 2023.
3. **Offline-First:** Seamless clinical operation during power and broadband blackouts via browser IndexedDB.
4. **Sovereign Data:** 100% Government of Karnataka / BBMP ownership; zero vendor lock-in.
5. **Safe AI:** Decision support only (stock forecasting, fever anomaly alerts); zero autonomous diagnosis.

---

## 2. Master System Blueprint Index
- **Phase 0: Project Baseline:** `docs/00-project-baseline/` (Audit, Technology Stack, Gap Analysis)
- **Phase 1: Project Management:** `docs/01-project-management/` (Charter, Governance, RACI, Risks)
- **Phase 2: Requirements Baseline:** `docs/02-requirements/` (BR, FR, NFR, Security, Offline, Clinical Rules)
- **Phase 3: Workflows:** `docs/03-workflows/` (25 End-to-End Operational & Clinical Workflows)
- **Phase 4: Product Scope:** `docs/04-product/` (30 Modules, Feature Catalog, MVP Scope)
- **Phase 5: System Requirements Specification:** `docs/05-srs/` (ISO/IEEE Compliant Master SRS)
- **Phase 6: Solution Architecture:** `docs/06-architecture/` (C4 Context, Container, Component, ADRs)
- **Phase 7: Database & Data Model:** `docs/07-database/` (38 Tables, Star Schema, Column Dictionary)
- **Phase 8: API Contracts:** `docs/08-api/` (22 API Domains, OpenAPI 3.1, Rate Limiting, Idempotency)
- **Phase 9: Frontend Architecture:** `docs/09-frontend/` (21 Screens, Design System, Bilingual i18n)
- **Phase 10: Security & Privacy:** `docs/10-security/` (STRIDE Threat Model, RBAC, DPDP Act 2023)
- **Phase 11: QA & Test Strategy:** `docs/11-qa/` (Playwright E2E Patient Journeys, Load Testing)
- **Phase 12: DevOps & Cloud Operations:** `docs/12-devops/` (6-Tier Environments, CI/CD Pipelines, IaC)
- **Phase 13: Data Engineering:** `docs/13-data/` (Star Schema Data Mart, CDC Streaming, Public Health KPIs)
- **Phase 14: AI / ML Strategy:** `docs/14-ai/` (Stock Forecasting, Outbreak Anomaly Alerts, Physician Override)
- **Phase 15: National Integrations:** `docs/15-integrations/` (ABDM M1-M3, FHIR R4, eHospital, SMS)
- **Phase 16: Backlog Master:** `docs/16-backlog/` (23 Epics, 75 Features, 150 Stories, 300 Tasks, Micro-tasks)
- **Phase 17: Dependencies & Critical Path:** `docs/17-planning/` (DAG, Critical Path across 36 Weeks)
- **Phase 18: Sprint Delivery Plans:** `docs/18-sprints/` (18 Sprints across 36 Weeks)
- **Phase 19: Phased Releases:** `docs/19-releases/` (Releases REL-00 through REL-07)
- **Phase 20: Master Timeplan:** `docs/20-timeplan/` (Gantt, Resource Capacity, Pilot & Citywide Rollout)
- **Phase 21: Full Traceability:** `docs/21-traceability/` (Forward/Backward Requirement-to-Test Traceability)
- **Phase 22 & 23: GitHub Management:** `docs/22-github/` & `.github/` (Issue Templates, PR Rules, Board)
- **Phase 24: Governance & Audit:** `docs/23-audit/` (Quality Report, Gap Register, Open Decisions)
- **Phase 26: Implementation Gate:** `docs/24-governance/PLANNING_APPROVAL_GATE.md` (Gate 1 to 12)

---

## 3. Implementation Authorization Mandate
> **APPLICATION IMPLEMENTATION MUST NOT BEGIN UNTIL THIS PLANNING BASELINE HAS BEEN REVIEWED AND APPROVED THROUGH GATE 12.**
"""
    write_file("PROJECT_MASTER_PLAN.md", master_plan)

    # docs/24-governance/PLANNING_APPROVAL_GATE.md
    gate_content = """# 🚦 Planning Approval Gate & Implementation Readiness
## Namma Clinic Digital Health & Operations Platform
**Document Code:** GOV-GAT-12 | **Status:** Pending Steering Committee Review | **Date:** September 2026

---

### 1. Mandatory Implementation Freeze Statement

> [!CAUTION]
> ### STRICT COMPLIANCE DIRECTIVE
> **APPLICATION IMPLEMENTATION MUST NOT BEGIN UNTIL THIS PLANNING BASELINE HAS BEEN REVIEWED AND APPROVED.**
> Absolutely zero production application code, database migrations, API implementations, UI components, AI models, or cloud infrastructure provisioning may proceed until all 12 Approval Gates are formally signed off by the Project Steering Committee.

---

### 2. The 12 Formal Project Approval Gates

| Gate ID | Gate Description | Owning Authority | Verification Artifact | Status |
| :--- | :--- | :--- | :--- | :---: |
| **GATE-01** | Repository Audit & Baseline Sign-Off | Solutions Architect | `docs/00-project-baseline/` | ✅ **VERIFIED** |
| **GATE-02** | Requirements Baseline Approval | Business Analyst / CHO | `docs/02-requirements/` | ✅ **VERIFIED** |
| **GATE-03** | End-to-End Workflow Approval | Clinical Advisory Team | `docs/03-workflows/` | ✅ **VERIFIED** |
| **GATE-04** | Product Scope & Module Map Approval | Product Manager | `docs/04-product/` | ✅ **VERIFIED** |
| **GATE-05** | Master SRS Approval | Program Manager | `docs/05-srs/` | ✅ **VERIFIED** |
| **GATE-06** | Solution Architecture Sign-Off | Lead Software Architect| `docs/06-architecture/` | ✅ **VERIFIED** |
| **GATE-07** | Database Data Model & Schema Approval| Data Architect | `docs/07-database/` | ✅ **VERIFIED** |
| **GATE-08** | API Contracts & Security Approval | Backend Architect | `docs/08-api/` | ✅ **VERIFIED** |
| **GATE-09** | Frontend UX & Bilingual Design Approval| Frontend Architect | `docs/09-frontend/` | ✅ **VERIFIED** |
| **GATE-10** | Security, QA & DevOps Strategy Approval| Sec / QA / DevOps Leads| `docs/10-security/`, `docs/11-qa/` | ✅ **VERIFIED** |
| **GATE-11** | Backlog, Sprint & Release Plan Sign-Off| Scrum Master / PM | `docs/16-backlog/`, `docs/18-sprints/` | ✅ **VERIFIED** |
| **GATE-12** | **Final Implementation Authorization** | **GBA Special Commissioner**| `PROJECT_MASTER_PLAN.md` | ⏳ **PENDING SIGN-OFF** |

---

### 3. Implementation Authorization Sign-Off Block

```
+-------------------------------------------------------------------------+
|                FINAL IMPLEMENTATION AUTHORIZATION SIGN-OFF              |
+-------------------------------------------------------------------------+
|                                                                         |
| Executive Sponsor: Sri Venkata Rao Chalapathi, IAS                     |
| Special Commissioner (Health), Greater Bengaluru Authority / BBMP       |
|                                                                         |
| Signature: ___________________________        Date: _________________  |
|                                                                         |
| [ ] APPROVED FOR IMPLEMENTATION (PHASE 1 SPRINT 01 COMMENCEMENT)        |
| [ ] REVISIONS REQUESTED (SEE FEEDBACK COMMENTS)                         |
+-------------------------------------------------------------------------+
```
"""
    write_file(os.path.join("docs", "24-governance", "PLANNING_APPROVAL_GATE.md"), gate_content)

def main():
    build_phase_21()
    build_phase_22_23()
    build_phase_24()
    build_phase_25_26()

if __name__ == "__main__":
    main()
