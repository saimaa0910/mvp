# 🔌 API Specification: Public Health & Zonal Analytics APIs
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-15 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Domain Specification & Technical Scope
Endpoints: GET `/analytics/dashboard/zonal`, GET `/analytics/kpis/citywide`.

### 2. Standard Endpoint Specifications
- **Authentication:** Mandatory Bearer JWT or Secure HttpOnly Cookie
- **Idempotency:** Enforced via `X-Idempotency-Key` header for mutation endpoints
- **RBAC Guard:** Checked against permission catalog prior to handler execution
- **Audit Hook:** Automatic asynchronous emission to `access_audit_logs`
- **Offline Behavior:** Queued locally in IndexedDB when offline; played back via sync engine
