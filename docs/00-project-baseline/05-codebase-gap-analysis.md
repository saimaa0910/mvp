# 🧩 Comprehensive Codebase & Architecture Gap Analysis
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
