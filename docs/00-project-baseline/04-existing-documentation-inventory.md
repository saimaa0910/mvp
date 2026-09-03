# 📚 Existing Documentation Inventory & Gap Catalog
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
