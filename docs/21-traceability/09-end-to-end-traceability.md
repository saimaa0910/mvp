# 🌐 End-to-End Requirements Traceability Matrix
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
