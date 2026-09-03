# 🔌 API Specification: Standardized Error Codes & Fault Envelopes
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-19 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Domain Specification & Technical Scope
HTTP 400, 401, 403, 404, 409, 422, 500 error mapping with localized user messages.

### 2. Standard Endpoint Specifications
- **Authentication:** Mandatory Bearer JWT or Secure HttpOnly Cookie
- **Idempotency:** Enforced via `X-Idempotency-Key` header for mutation endpoints
- **RBAC Guard:** Checked against permission catalog prior to handler execution
- **Audit Hook:** Automatic asynchronous emission to `access_audit_logs`
- **Offline Behavior:** Queued locally in IndexedDB when offline; played back via sync engine
