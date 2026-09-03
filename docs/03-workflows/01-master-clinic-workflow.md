# 🔄 Workflow: Master Clinic Day Operational Workflow
## Namma Clinic Digital Health & Operations Platform
**Document Code:** WF-01 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Workflow Overview & Architecture
This document defines the end-to-end operational, technical, and data flow for **Master Clinic Day Operational Workflow**.

### 2. Operational Specification
- **Primary Actors:** Frontline Clinic Staff (Nurse, Doctor, Pharmacist, Lab Tech, Patient)
- **Trigger:** Event initiation in clinic environment
- **Preconditions:** Active clinic session and verified user permissions
- **Security & RBAC:** Role-checked at API gateway and client UI state
- **Offline Resilience:** Local transaction persistence with deterministic sync queue
- **Audit Logging:** Emits structured immutable audit record upon state transition

### 3. Workflow Diagram & Sequence
```mermaid
sequenceDiagram
    autonumber
    actor P as Patient
    actor N as Staff Nurse
    actor D as Doctor
    actor PH as Pharmacist
    actor L as Lab Tech
    P->>N: 1. Arrives at Clinic Desk
    N->>N: 2. Search / Register Patient & Issue Token
    N->>N: 3. Record Vitals & Triage Priority
    N->>D: 4. Patient Enters Doctor Room
    D->>D: 5. Examination, Diagnosis & e-Prescription
    alt Lab Required
        D->>L: 6a. Order Point-of-Care Lab Test
        L->>D: 6b. Collect Sample & Enter Result
    end
    D->>PH: 7. e-Prescription Sent to Pharmacy
    PH->>P: 8. Dispense Medicines (FEFO) & Explain Dosage
    P->>P: 9. Patient Departs Clinic
```

### 4. Database & API Touchpoints
- **APIs Involved:** Dedicated REST endpoints with idempotency keys
- **Database Entities:** ACID transaction boundaries across core relational tables
- **Audit Events:** `AUDIT_EVENT_CREATED` recorded in `access_audit_logs`
