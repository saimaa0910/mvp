# 🗺️ Product Module Map & Domain Architecture
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
