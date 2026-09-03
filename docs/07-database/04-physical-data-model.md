# 🗄️ Physical Data Model & Complete Relational ERD
## Namma Clinic Digital Health & Operations Platform
**Document Code:** DB-PHY-04 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Entity-Relationship Diagram (Transactional Core)

```mermaid
erDiagram
    corporations ||--o{ zones : contains
    zones ||--o{ wards : contains
    wards ||--o{ clinics : hosts
    clinics ||--o{ staff : employs
    users ||--o{ user_roles : assigned
    roles ||--o{ user_roles : defines
    roles ||--o{ role_permissions : grants
    permissions ||--o{ role_permissions : specifies

    patients ||--o{ patient_consents : grants
    patients ||--o{ visits : attends
    clinics ||--o{ visits : hosts
    visits ||--o{ vitals : records
    visits ||--o{ triage_records : triaged
    visits ||--o{ clinical_encounters : documents
    clinical_encounters ||--o{ visit_diagnoses : diagnosed
    diagnoses ||--o{ visit_diagnoses : referenced

    clinical_encounters ||--o{ prescriptions : prescribed
    prescriptions ||--o{ prescription_items : contains
    medicines_master ||--o{ prescription_items : specifies
    medicines_master ||--o{ medicine_batches : batches
    clinics ||--o{ pharmacy_stock_ledger : holds
    medicine_batches ||--o{ pharmacy_stock_ledger : tracks
    prescriptions ||--o{ medicine_issues : dispenses
    medicine_issues ||--o{ medicine_issue_items : items

    clinical_encounters ||--o{ lab_orders : orders
    lab_tests ||--o{ lab_order_items : tests
    lab_orders ||--o{ lab_order_items : contains

    clinical_encounters ||--o{ referrals : refers
    external_facilities ||--o{ referrals : receives
    patients ||--o{ follow_ups : scheduled
    users ||--o{ access_audit_logs : logs
```
