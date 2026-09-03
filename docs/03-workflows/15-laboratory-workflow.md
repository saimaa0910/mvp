# 🔄 Workflow: Point-of-Care Lab Test Ordering & Result Entry
## Namma Clinic Digital Health & Operations Platform
**Document Code:** WF-15 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Workflow Overview & Architecture
This document defines the end-to-end operational, technical, and data flow for **Point-of-Care Lab Test Ordering & Result Entry**.

### 2. Operational Specification
- **Primary Actors:** Frontline Clinic Staff (Nurse, Doctor, Pharmacist, Lab Tech, Patient)
- **Trigger:** Event initiation in clinic environment
- **Preconditions:** Active clinic session and verified user permissions
- **Security & RBAC:** Role-checked at API gateway and client UI state
- **Offline Resilience:** Local transaction persistence with deterministic sync queue
- **Audit Logging:** Emits structured immutable audit record upon state transition

### 3. Workflow Diagram & Sequence
Order 14 essential tests, log sample collection, enter numeric/qualitative result.

### 4. Database & API Touchpoints
- **APIs Involved:** Dedicated REST endpoints with idempotency keys
- **Database Entities:** ACID transaction boundaries across core relational tables
- **Audit Events:** `AUDIT_EVENT_CREATED` recorded in `access_audit_logs`
