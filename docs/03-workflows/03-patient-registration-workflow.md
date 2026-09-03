# 🔄 Workflow: New Patient Registration & Demographics Capture
## Namma Clinic Digital Health & Operations Platform
**Document Code:** WF-03 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Workflow Overview & Architecture
This document defines the end-to-end operational, technical, and data flow for **New Patient Registration & Demographics Capture**.

### 2. Operational Specification
- **Primary Actors:** Frontline Clinic Staff (Nurse, Doctor, Pharmacist, Lab Tech, Patient)
- **Trigger:** Event initiation in clinic environment
- **Preconditions:** Active clinic session and verified user permissions
- **Security & RBAC:** Role-checked at API gateway and client UI state
- **Offline Resilience:** Local transaction persistence with deterministic sync queue
- **Audit Logging:** Emits structured immutable audit record upon state transition

### 3. Workflow Diagram & Sequence
```mermaid
flowchart TD
    A[Citizen Arrives] --> B{Existing Patient?}
    B -- Yes --> C[Search via Mobile / UHID]
    B -- No --> D[Enter Name, Phone, Age, Gender, Ward]
    D --> E{Link ABHA?}
    E -- Yes --> F[Aadhaar OTP / Scan ABHA QR]
    E -- No --> G[Generate Internal UHID]
    F --> G
    G --> H[Issue Daily Queue Token]
    H --> I[Proceed to Triage Desk]
```

### 4. Database & API Touchpoints
- **APIs Involved:** Dedicated REST endpoints with idempotency keys
- **Database Entities:** ACID transaction boundaries across core relational tables
- **Audit Events:** `AUDIT_EVENT_CREATED` recorded in `access_audit_logs`
