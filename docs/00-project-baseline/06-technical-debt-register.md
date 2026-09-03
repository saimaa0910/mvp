# 💳 Technical Debt Register & Pre-Implementation Risk Log
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
