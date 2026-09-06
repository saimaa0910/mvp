# 🔌 API Specification: RESTful API Conventions & Design Standards
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-02 | **Status:** Authoritative Baseline | **Date:** September 2026
> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Standard Framework:** RFC 7231 (HTTP/1.1), RFC 7807 (Problem Details), JSON:API v1.1, UUIDv7 Draft RFC
> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.

---

## 1. Executive Summary & Core Design System

This document establishes the mandatory design conventions, syntax rules, HTTP protocol bindings, serialization standards, and error formatting for all RESTful services across the Namma Clinic platform. Uniformity across all 16 functional domains is enforced at the API gateway layer, ensuring consistent developer experience, deterministic client caching, and robust automated validation.

## 2. Resource Naming & URI Formatting Standards

### 2.1 URI Structure & Path Hierarchy
All endpoints must conform to the following URI path template:
`https://{host}/api/v{major_version}/{domain_resource}/{resource_id}/{sub_resource}`

Rules:
- **Kebab-Case Paths:** All multi-word path segments must use lowercase kebab-case (e.g., `/api/v1/patient-identifiers`, `/api/v1/clinical-encounters`).
- **Plural Nouns:** Top-level resource segments must always be plural nouns (e.g., `/patients`, `/prescriptions`, `/dispensations`). Singular resources are strictly prohibited.
- **No Action Verbs in Path:** RPC-style action verbs in paths (e.g., `/api/v1/getPatients` or `/createVisit`) are forbidden. Verbs are expressed exclusively via HTTP methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
- **Sub-Resource Nesting:** Nesting is limited to a maximum depth of two levels (e.g., `/patients/{id}/encounters` or `/prescriptions/{id}/items`). Deeper relationships must be queried via top-level filtering.

### 2.2 Authoritative Resource Endpoint Mapping Table (52 Resources)
Every database table is bound to a canonical RESTful resource path:

| Table ID | Table Name | Canonical REST Path | Permitted Verbs | Default Sort Field | Scope |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TABLE-001` | `auth_users` | `/api/v1/auth-users` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Identity & Access` |
| `TABLE-002` | `user_credentials` | `/api/v1/user-credentials` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Identity & Access` |
| `TABLE-003` | `user_sessions` | `/api/v1/user-sessions` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Identity & Access` |
| `TABLE-004` | `roles` | `/api/v1/roles` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Role-Based Access Control` |
| `TABLE-005` | `permissions` | `/api/v1/permissions` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Role-Based Access Control` |
| `TABLE-006` | `role_permissions` | `/api/v1/role-permissions` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Role-Based Access Control` |
| `TABLE-007` | `user_roles` | `/api/v1/user-roles` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Role-Based Access Control` |
| `TABLE-008` | `facilities` | `/api/v1/facilities` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Facility Operations` |
| `TABLE-009` | `facility_rooms` | `/api/v1/facility-rooms` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Facility Operations` |
| `TABLE-010` | `staff_profiles` | `/api/v1/staff-profiles` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Human Resources` |
| `TABLE-011` | `staff_shifts` | `/api/v1/staff-shifts` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Human Resources` |
| `TABLE-012` | `system_configs` | `/api/v1/system-configs` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `System Configuration` |
| `TABLE-013` | `patients` | `/api/v1/patients` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Citizen Demographics` |
| `TABLE-014` | `patient_identifiers` | `/api/v1/patient-identifiers` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Citizen Demographics` |
| `TABLE-015` | `patient_contacts` | `/api/v1/patient-contacts` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Citizen Demographics` |
| `TABLE-016` | `patient_addresses` | `/api/v1/patient-addresses` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Citizen Demographics` |
| `TABLE-017` | `consent_records` | `/api/v1/consent-records` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Consent Management` |
| `TABLE-018` | `tokens` | `/api/v1/tokens` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Queue Management` |
| `TABLE-019` | `queue_entries` | `/api/v1/queue-entries` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Queue Management` |
| `TABLE-020` | `triage_assessments` | `/api/v1/triage-assessments` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Clinical Triage` |
| `TABLE-021` | `patient_vitals` | `/api/v1/patient-vitals` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Clinical Triage` |
| `TABLE-022` | `danger_alerts` | `/api/v1/danger-alerts` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Clinical Safety` |
| `TABLE-023` | `clinical_encounters` | `/api/v1/clinical-encounters` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Clinical Consultation` |
| `TABLE-024` | `clinical_notes` | `/api/v1/clinical-notes` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Clinical Consultation` |
| `TABLE-025` | `diagnoses` | `/api/v1/diagnoses` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Clinical Consultation` |
| `TABLE-026` | `prescriptions` | `/api/v1/prescriptions` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Pharmacy & Prescribing` |
| `TABLE-027` | `prescription_items` | `/api/v1/prescription-items` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Pharmacy & Prescribing` |
| `TABLE-028` | `lab_orders` | `/api/v1/lab-orders` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Diagnostic Services` |
| `TABLE-029` | `lab_order_items` | `/api/v1/lab-order-items` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Diagnostic Services` |
| `TABLE-030` | `lab_results` | `/api/v1/lab-results` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Diagnostic Services` |
| `TABLE-031` | `teleconsultations` | `/api/v1/teleconsultations` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Telemedicine` |
| `TABLE-032` | `formulary_drugs` | `/api/v1/formulary-drugs` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Pharmaceutical Master` |
| `TABLE-033` | `drug_categories` | `/api/v1/drug-categories` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Pharmaceutical Master` |
| `TABLE-034` | `pharmacy_batches` | `/api/v1/pharmacy-batches` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Inventory & Traceability` |
| `TABLE-035` | `clinic_stock` | `/api/v1/clinic-stock` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Inventory & Traceability` |
| `TABLE-036` | `dispensations` | `/api/v1/dispensations` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Pharmacy Operations` |
| `TABLE-037` | `dispensation_items` | `/api/v1/dispensation-items` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Pharmacy Operations` |
| `TABLE-038` | `stock_movements` | `/api/v1/stock-movements` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Inventory & Traceability` |
| `TABLE-039` | `drug_indents` | `/api/v1/drug-indents` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Supply Chain & Procurement` |
| `TABLE-040` | `indent_items` | `/api/v1/indent-items` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Supply Chain & Procurement` |
| `TABLE-041` | `cold_chain_devices` | `/api/v1/cold-chain-devices` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Cold Chain & IoT` |
| `TABLE-042` | `cold_chain_telemetry` | `/api/v1/cold-chain-telemetry` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Cold Chain & IoT` |
| `TABLE-043` | `referrals` | `/api/v1/referrals` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Continuity of Care` |
| `TABLE-044` | `referral_counter_notes` | `/api/v1/referral-counter-notes` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Continuity of Care` |
| `TABLE-045` | `ncd_episodes` | `/api/v1/ncd-episodes` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Chronic Disease Management` |
| `TABLE-046` | `follow_up_schedules` | `/api/v1/follow-up-schedules` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Continuity of Care` |
| `TABLE-047` | `notifications` | `/api/v1/notifications` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Citizen Engagement` |
| `TABLE-048` | `grievances` | `/api/v1/grievances` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Citizen Grievance & Feedback` |
| `TABLE-049` | `helpdesk_tickets` | `/api/v1/helpdesk-tickets` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `IT & Infrastructure Support` |
| `TABLE-050` | `audit_events` | `/api/v1/audit-events` | `GET (Read-Only)` | `-created_at` | `Compliance & Security` |
| `TABLE-051` | `offline_mutation_log` | `/api/v1/offline-mutation-log` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `Edge Offline Synchronization` |
| `TABLE-052` | `abdm_artifacts` | `/api/v1/abdm-artifacts` | `GET, POST, PUT, PATCH, DELETE` | `-created_at` | `National Interoperability` |

## 3. HTTP Methods, Status Codes, and Idempotency Semantics

The platform adheres to strict RFC 7231 method semantics:

| HTTP Verb | CRUD Action | Idempotent | Safe | Success Status | Client Error Status | Cacheable |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | Read Resource | **Yes** | **Yes** | `200 OK` | `400`, `401`, `403`, `404` | Yes (with ETag) |
| `POST` | Create / Action | **No** (Enforced via Key) | **No** | `201 Created` / `202 Accepted` | `400`, `409`, `422` | No |
| `PUT` | Full Replace | **Yes** | **No** | `200 OK` | `400`, `404`, `412` | No |
| `PATCH` | Partial Update | **No** (Conditionally) | **No** | `200 OK` | `400`, `404`, `412` | No |
| `DELETE`| Soft Delete | **Yes** | **No** | `200 OK` / `204 No Content` | `403`, `404` | No |

### 3.1 Exhaustive Status Codes Specification
The 22 recognized HTTP status codes are defined below:

| Status Code | RFC Name | Operational Meaning & Platform Usage | Error Envelope Emitted |
| :--- | :--- | :--- | :--- |
| `HTTP 200` | `OK` | Standard success response for GET, PUT, PATCH, or non-creation POST operations. | No |
| `HTTP 201` | `Created` | Resource successfully created via POST. Returns created resource and Location header. | No |
| `HTTP 202` | `Accepted` | Asynchronous job accepted for background execution (e.g., data export, batch sync). | No |
| `HTTP 204` | `No Content` | Action successfully completed with empty response payload (e.g., token revocation). | No |
| `HTTP 304` | `Not Modified` | Resource has not changed since ETag specified in If-None-Match header; body empty. | No |
| `HTTP 400` | `Bad Request` | Malformed syntax, invalid JSON, or schema validation constraint failure. | **Yes (SCHEMA-API-003)** |
| `HTTP 401` | `Unauthorized` | Missing, invalid, expired, or untrusted Bearer JWT authentication token. | **Yes (SCHEMA-API-003)** |
| `HTTP 403` | `Forbidden` | Authenticated caller lacks RBAC permission or fails ABAC facility/shift scoping guard. | **Yes (SCHEMA-API-003)** |
| `HTTP 404` | `Not Found` | Target resource identifier does not exist or has been tombstoned. | **Yes (SCHEMA-API-003)** |
| `HTTP 405` | `Method Not Allowed` | HTTP verb not supported for the requested resource endpoint. | **Yes (SCHEMA-API-003)** |
| `HTTP 406` | `Not Acceptable` | Server cannot produce media type requested in Accept header. | **Yes (SCHEMA-API-003)** |
| `HTTP 409` | `Conflict` | Business rule conflict, duplicate key, or concurrent mutation collision. | **Yes (SCHEMA-API-003)** |
| `HTTP 410` | `Gone` | Resource or pre-signed download link previously existed but has expired permanently. | **Yes (SCHEMA-API-003)** |
| `HTTP 412` | `Precondition Failed` | If-Match ETag header does not match current database row version. | **Yes (SCHEMA-API-003)** |
| `HTTP 413` | `Payload Too Large` | Uploaded payload exceeds gateway 10MB limit. | **Yes (SCHEMA-API-003)** |
| `HTTP 415` | `Unsupported Media Type` | Content-Type header is not application/json or application/json+fhir. | **Yes (SCHEMA-API-003)** |
| `HTTP 422` | `Unprocessable Entity` | Syntactically valid JSON but semantic domain rule violation. | **Yes (SCHEMA-API-003)** |
| `HTTP 429` | `Too Many Requests` | Rate limit quota exceeded; Retry-After header indicates required delay. | **Yes (SCHEMA-API-003)** |
| `HTTP 500` | `Internal Server Error` | Uncaught server error; correlation ID logged to WORM audit trail. | **Yes (SCHEMA-API-003)** |
| `HTTP 502` | `Bad Gateway` | Upstream dependency (CDAC SMS, NHA ABDM Gateway) returned invalid response. | **Yes (SCHEMA-API-003)** |
| `HTTP 503` | `Service Unavailable` | Circuit breaker tripped or scheduled maintenance window active. | **Yes (SCHEMA-API-003)** |
| `HTTP 504` | `Gateway Timeout` | Upstream microservice or database transaction exceeded deadline. | **Yes (SCHEMA-API-003)** |

## 4. Standard Ingress & Egress HTTP Headers

All requests and responses must exchange the following standardized headers:

| Header Name | Category | Direction | Requirement | Description & Format |
| :--- | :--- | :--- | :--- | :--- |
| `X-Correlation-ID` | Tracing | Both | **Mandatory** | UUIDv7 correlating request across edge and microservices. |
| `X-Request-ID` | Tracing | Both | **Mandatory** | Unique UUIDv7 per HTTP hop. |
| `X-Idempotency-Key` | Reliability | Ingress | **Mandatory for POST/PUT** | UUIDv7 deduplication key cached for 24 hours. |
| `X-Facility-ID` | Security | Ingress | **Mandatory** | UUIDv7 of Namma Clinic facility where terminal is operating. |
| `Authorization` | Security | Ingress | **Mandatory (except public)** | `Bearer <JWT>` containing staff claims. |
| `If-Match` | Concurrency | Ingress | Mandatory for PUT/PATCH | Cryptographic ETag hash for optimistic concurrency. |
| `ETag` | Concurrency | Egress | Present on GET/PUT | SHA-256 hash of resource representation. |
| `RateLimit-Limit` | Rate Limiting | Egress | Present on all | Maximum allowed requests in current window. |
| `RateLimit-Remaining` | Rate Limiting | Egress | Present on all | Remaining request quota in current window. |
| `RateLimit-Reset` | Rate Limiting | Egress | Present on all | UTC seconds until quota window resets. |
| `Retry-After` | Rate Limiting | Egress | Present on 429/503 | Seconds caller must back off before retry. |

## 5. JSON Serialization, Identifier & Timestamp Formats

### 5.1 JSON Attribute Naming Conventions
- **camelCase in JSON:** All JSON payload keys must be formatted in strict `camelCase` (e.g., `firstName`, `prescribedDosage`, `contactNumber`).
- **snake_case in Database:** Relational database columns remain `snake_case` (e.g., `first_name`); ORM serialization layers map between snake_case and camelCase deterministically.
- **Null Semantics:** Explicit `null` indicates cleared value; absent keys in PATCH indicate untouched fields.

### 5.2 Time-Ordered UUIDv7 Standard
Every entity generated across the platform utilizes time-ordered **UUIDv7** (RFC 9562 draft standard). This guarantees:
1. **Monotonic Ordering:** IDs sort chronologically based on millisecond timestamp prefix, preventing B-tree index fragmentation in PostgreSQL and SQLite.
2. **Autonomous Edge Generation:** Clinic tablets can generate globally unique primary keys offline without colliding with central cloud records.
3. **Cryptographic Randomness:** 74 bits of cryptographically secure pseudo-random entropy prevent key guessing or enumeration attacks.

## 6. Query Parameters: Pagination, Filtering, Sorting & Expansion

### 6.1 Cursor-Based Pagination Standards
To prevent database offset scanning penalties on million-row tables (`patients`, `audit_events`), cursor pagination is enforced:
```http
# DOCUMENTATION-ONLY EXAMPLE
GET /api/v1/patients?limit=25&cursor=ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSFV6STFOaUlzSW5SNWNDSTZJazFsYkd4bFlXNWxJanAwY25WbGMzUWlPaUowWlhOMElpd2ljbVZ6ZFdsdUlqcDdJblJsZUhRaU9pSjBhSFJzY3lJc0luQjFiaUk2TWpB
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
```

### 6.2 Filtering Grammar
Query filters utilize bracket notation matching indexed attributes:
- `filter[gender]=FEMALE`
- `filter[wardNumber]=142`
- `filter[createdAt][gte]=2026-09-01T00:00:00Z`
- `filter[status][in]=ACTIVE,IN_PROGRESS`

### 6.3 Sorting Standards
Sorting is specified via the `sort` parameter with comma separation; prefix `-` indicates descending order:
- `sort=-createdAt,lastName`

## 7. Standard API Response Envelopes & Detailed Schemas

Every response emitted across the 341 endpoints wraps data in one of three standardized top-level JSON envelopes:

### 7.1 Single-Resource Response Envelope (`SCHEMA-API-001`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "patients",
    "attributes": {
      "uhid": "NC-BLR-2026-00000042",
      "firstName": "Sunita",
      "lastName": "Gowda",
      "gender": "FEMALE",
      "dateOfBirth": "1984-06-15",
      "primaryPhone": "XXXXXX8921",
      "bbmpWardNumber": 142,
      "abhaLinked": true,
      "createdAt": "2026-09-01T09:15:30.124Z"
    },
    "relationships": {
      "facility": {
        "data": { "id": "018e3a20-0008-7000-8000-000000000001", "type": "facilities" }
      }
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 24,
    "serverNode": "cloud-app-az1-pod4",
    "timestamp": "2026-09-01T09:15:30.148Z"
  },
  "links": {
    "self": "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001"
  }
}
```

### 7.2 Standard Error Response Envelope (`SCHEMA-API-003`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-PATIENT-002",
    "message": "High-confidence duplicate citizen detected (matching mobile phone and phonetic name).",
    "category": "Conflict",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:15:30.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.primaryPhone",
        "rule": "unique_constraint_violation",
        "rejectedValue": "XXXXXX8921",
        "message": "Mobile number matches existing patient profile UHID NC-BLR-2024-00008129."
      }
    ]
  }
}
```

## 8. Authoritative API Schema Catalog (68 Schemas)

The 68 canonical schemas registered for the platform are tabulated below:

| Schema ID | Schema Name | Functional Category | Field Count | Authoritative Description |
| :--- | :--- | :--- | :--- | :--- |
| **SCHEMA-API-001** | `StandardApiResponseEnvelope` | `Common` | 3 fields | Top-level JSON envelope wrapping all successful single-resource REST API responses. |
| **SCHEMA-API-002** | `StandardCollectionEnvelope` | `Common` | 4 fields | Top-level JSON envelope wrapping paginated collection responses. |
| **SCHEMA-API-003** | `StandardErrorEnvelope` | `Common` | 8 fields | Authoritative RFC 7807 and GBA compliant structured error payload for all HTTP 4xx/5xx responses. |
| **SCHEMA-API-004** | `ValidationErrorItem` | `Common` | 4 fields | Field-specific validation failure item embedded in error details. |
| **SCHEMA-API-005** | `CursorPaginationMetadata` | `Common` | 6 fields | Standardized pagination cursor and navigation metadata. |
| **SCHEMA-API-006** | `LoginRequest` | `Auth` | 5 fields | Staff login payload submitting username, password, and facility scope. |
| **SCHEMA-API-007** | `AuthTokenResponse` | `Auth` | 6 fields | Authentication success response returning access and refresh tokens. |
| **SCHEMA-API-008** | `TokenRefreshRequest` | `Auth` | 2 fields | Token rotation payload presenting active refresh token. |
| **SCHEMA-API-009** | `StaffSessionProfile` | `Auth` | 7 fields | Current authenticated staff profile and permissions context. |
| **SCHEMA-API-010** | `PasswordChangeRequest` | `Auth` | 3 fields | Self-service password update payload. |
| **SCHEMA-API-011** | `PatientRegistrationRequest` | `Patient` | 14 fields | Citizen demographic intake payload for registering new patients at front desk. |
| **SCHEMA-API-012** | `PatientProfileResponse` | `Patient` | 10 fields | Full citizen demographic and clinical continuity summary. |
| **SCHEMA-API-013** | `PatientSearchQuery` | `Patient` | 5 fields | Multi-parameter phonetic and index query payload for patient lookup. |
| **SCHEMA-API-014** | `PatientDuplicateMatch` | `Patient` | 4 fields | Duplicate candidate record identified by fuzzy phonetic and demographic matching. |
| **SCHEMA-API-015** | `PatientMergeRequest` | `Patient` | 3 fields | Supervisory command payload merging duplicate patient records. |
| **SCHEMA-API-016** | `VisitCreationRequest` | `Visit` | 5 fields | OPD visit registration and token generation payload. |
| **SCHEMA-API-017** | `QueueTokenResponse` | `Visit` | 6 fields | Issued daily queue token and waiting hall broadcast descriptor. |
| **SCHEMA-API-018** | `QueueStatusUpdateCommand` | `Visit` | 2 fields | Doctor/nurse command transitioning token queue state. |
| **SCHEMA-API-019** | `TriageAssessmentRequest` | `Triage` | 12 fields | Nursing triage and physical vitals acquisition payload. |
| **SCHEMA-API-020** | `TriageScoreResponse` | `Triage` | 5 fields | Computed MEWS score, acuity tier, and immediate escalation guidance. |
| **SCHEMA-API-021** | `ConsultationEncounterRequest` | `Consultation` | 7 fields | Doctor outpatient SOAP encounter notes, diagnosis coding, and care plan. |
| **SCHEMA-API-022** | `DiagnosisEntry` | `Consultation` | 5 fields | Standardized diagnostic terminology entry. |
| **SCHEMA-API-023** | `PrescriptionCreationRequest` | `Prescription` | 4 fields | Electronic prescription authorization payload issued by treating physician. |
| **SCHEMA-API-024** | `PrescriptionLineItem` | `Prescription` | 8 fields | Individual medication line item in electronic prescription. |
| **SCHEMA-API-025** | `PharmacyDispenseRequest` | `Pharmacy` | 3 fields | Pharmacist dispensation verification and batch allocation payload. |
| **SCHEMA-API-026** | `DispensedLineItem` | `Pharmacy` | 5 fields | Batch-allocated medication line item deducted from stock. |
| **SCHEMA-API-027** | `StockReceiptRequest` | `Inventory` | 3 fields | Clinic stock receipt from central BBMP warehouse or zonal depot. |
| **SCHEMA-API-028** | `BatchReceiptItem` | `Inventory` | 6 fields | Discrete pharmaceutical batch received into facility inventory. |
| **SCHEMA-API-029** | `StockAdjustmentCommand` | `Inventory` | 4 fields | Physical inventory audit adjustment or write-off payload. |
| **SCHEMA-API-030** | `LabOrderCreationRequest` | `Lab` | 4 fields | Doctor requisition for diagnostic investigations. |
| **SCHEMA-API-031** | `LabResultEntryRequest` | `Lab` | 7 fields | Lab technician diagnostic result capture and panic flag payload. |
| **SCHEMA-API-032** | `ReferralCreationRequest` | `Referral` | 6 fields | Secondary/tertiary hospital transfer dossier payload. |
| **SCHEMA-API-033** | `OutboundNotificationRequest` | `Notification` | 5 fields | System-generated citizen SMS / WhatsApp message dispatch payload. |
| **SCHEMA-API-034** | `ClinicKpiSummaryResponse` | `Analytics` | 7 fields | Aggregated daily operational performance metrics for a clinic facility. |
| **SCHEMA-API-035** | `AuditEventQuery` | `Audit` | 6 fields | Cryptographic WORM audit log query and verification payload. |
| **SCHEMA-API-036** | `AbhaVerificationRequest` | `ABDM` | 3 fields | ABDM M1 ABHA address discovery and OTP verification payload. |
| **SCHEMA-API-037** | `FhirBundleExportResponse` | `ABDM` | 3 fields | FHIR R4 DiagnosticReport / Encounter document bundle for health record sharing. |
| **SCHEMA-API-038** | `PortabilityExportJobRequest` | `Portability` | 4 fields | Citizen DPDP Act 2023 Section 12 Data Portability export request. |
| **SCHEMA-API-039** | `PortabilityJobStatusResponse` | `Portability` | 5 fields | Status and download link for asynchronous portability export job. |
| **SCHEMA-API-040** | `EdgeSyncBatchRequest` | `System` | 4 fields | Offline mutation journal replay batch uploaded by clinic edge gateway. |
| **SCHEMA-API-041** | `SyncMutationItem` | `System` | 6 fields | Discrete mutation record executed on edge SQLite node. |
| **SCHEMA-API-042** | `EdgeSyncBatchResponse` | `System` | 4 fields | Cloud synchronization acknowledgment, conflict resolutions, and server updates. |
| **SCHEMA-API-043** | `HealthCheckLivenessResponse` | `System` | 2 fields | Kubernetes liveness probe response |
| **SCHEMA-API-044** | `HealthCheckReadinessResponse` | `System` | 3 fields | Kubernetes readiness probe verifying DB and cache connectivity |
| **SCHEMA-API-045** | `FacilityRoomStatusResponse` | `Visit` | 3 fields | Real-time occupancy status of clinic examination room |
| **SCHEMA-API-046** | `VitalSignsSeriesResponse` | `Triage` | 2 fields | Longitudinal vital signs readings for a patient across visits |
| **SCHEMA-API-047** | `DangerAlertNotification` | `Triage` | 3 fields | Critical physiologic deterioration alert payload |
| **SCHEMA-API-048** | `ClinicalNotePatchRequest` | `Consultation` | 2 fields | Addendum or amendment payload for finalized consultation note |
| **SCHEMA-API-049** | `DrugFormularyItemResponse` | `Prescription` | 3 fields | Essential drugs formulary metadata and dosage guidelines |
| **SCHEMA-API-050** | `MedicationInteractionWarning` | `Prescription` | 3 fields | CDSS drug-drug or drug-allergy contraindication alert |
| **SCHEMA-API-051** | `PharmacyStockBalanceResponse` | `Pharmacy` | 3 fields | On-hand inventory balance per batch in clinic dispensary |
| **SCHEMA-API-052** | `DispensingReversalRequest` | `Pharmacy` | 3 fields | Void or reversal of incorrect dispensation transaction |
| **SCHEMA-API-053** | `ColdChainTelemetryBatch` | `Inventory` | 3 fields | IoT temperature and power sensor readings from vaccine refrigerator |
| **SCHEMA-API-054** | `ColdChainExcursionAlert` | `Inventory` | 4 fields | Vaccine temperature breach alert notification |
| **SCHEMA-API-055** | `LabSpecimenCollectionRequest` | `Lab` | 3 fields | Phlebotomy specimen accession and barcode mapping |
| **SCHEMA-API-056** | `LabSpecimenRejectionPayload` | `Lab` | 2 fields | Specimen rejection due to hemolysis, clotting, or volume insufficiency |
| **SCHEMA-API-057** | `ReferralCounterNoteResponse` | `Referral` | 3 fields | Discharge summary received from tertiary hospital for referred patient |
| **SCHEMA-API-058** | `SmsDeliveryReceiptPayload` | `Notification` | 3 fields | Telecom gateway delivery status webhook callback |
| **SCHEMA-API-059** | `EpidemicSurveillanceReport` | `Analytics` | 3 fields | Syndromic fever and acute respiratory infection cluster report |
| **SCHEMA-API-060** | `DoctorWorkloadMetricResponse` | `Analytics` | 3 fields | Outpatient encounters, average duration, and pending queue per doctor |
| **SCHEMA-API-061** | `AuditHashChainVerification` | `Audit` | 3 fields | Cryptographic verification response for WORM audit hash integrity |
| **SCHEMA-API-062** | `AbdmConsentArtefactPayload` | `ABDM` | 3 fields | Standard ABDM electronic consent artifact signed by citizen |
| **SCHEMA-API-063** | `AbdmCareContextLinkRequest` | `ABDM` | 3 fields | HIP care context linking request to associate visit with ABHA |
| **SCHEMA-API-064** | `DataPortabilityConsentProof` | `Portability` | 3 fields | Digital consent authorization token enabling data extraction |
| **SCHEMA-API-065** | `HardwareTerminalRegisterRequest` | `System` | 3 fields | Registration of clinic tablet or receipt printer with edge gateway |
| **SCHEMA-API-066** | `DatabaseReplicationStatusResponse` | `System` | 3 fields | Cloud PostgreSQL streaming replication lag and Patroni leader status |
| **SCHEMA-API-067** | `UserRoleAssignmentPayload` | `Auth` | 3 fields | Administrative assignment of role and facility scope to staff member |
| **SCHEMA-API-068** | `BulkImportStatusResponse` | `System` | 4 fields | Status of administrative bulk data ingestion (formulary, providers) |

## 9. Exhaustive Field-Level Schema Specifications (All 68 Schemas)

Every registered schema is cataloged with complete typing, nullability, required status, and domain validation rules:

### 9.SCHEMA-API-001 Schema Specification: `StandardApiResponseEnvelope`
- **Schema Identifier:** `SCHEMA-API-001`
- **Domain Category:** `Common`
- **Functional Scope:** Top-level JSON envelope wrapping all successful single-resource REST API responses.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `data` | `object` | **Yes** | No | Primary payload object containing resource attributes and relationships. |
| `meta` | `object` | **Yes** | No | Request execution metadata including timestamp, correlation ID, and server node. |
| `links` | `object` | No | Yes | HATEOAS navigational links (self, related). |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": [],
  "meta": [],
  "links": []
}
```

### 9.SCHEMA-API-002 Schema Specification: `StandardCollectionEnvelope`
- **Schema Identifier:** `SCHEMA-API-002`
- **Domain Category:** `Common`
- **Functional Scope:** Top-level JSON envelope wrapping paginated collection responses.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `data` | `array` | **Yes** | No | Array of resource objects matching query filters. |
| `pagination` | `object` | **Yes** | No | Cursor-based pagination metadata (cursor, next_cursor, has_more, limit, total_count). |
| `meta` | `object` | **Yes** | No | Execution metadata including query duration, filter counts, and correlation ID. |
| `links` | `object` | **Yes** | No | Navigational links (self, next, prev, first). |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": [],
  "pagination": [],
  "meta": [],
  "links": []
}
```

### 9.SCHEMA-API-003 Schema Specification: `StandardErrorEnvelope`
- **Schema Identifier:** `SCHEMA-API-003`
- **Domain Category:** `Common`
- **Functional Scope:** Authoritative RFC 7807 and GBA compliant structured error payload for all HTTP 4xx/5xx responses.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `error` | `object` | **Yes** | No | Root error container object. |
| `error.code` | `string` | **Yes** | No | Machine-readable standardized error code (e.g., ERR-AUTH-001). |
| `error.message` | `string` | **Yes** | No | Safe, localized human-readable error summary for end-user display. |
| `error.category` | `string` | **Yes** | No | Categorical domain of failure (Authentication, Validation, ClinicalSafety, etc.). |
| `error.correlation_id` | `string` | **Yes** | No | UUIDv7 distributed trace identifier matching X-Correlation-ID header. |
| `error.timestamp` | `string` | **Yes** | No | ISO-8601 UTC timestamp of error generation. |
| `error.retryable` | `boolean` | **Yes** | No | Boolean flag indicating whether client may safely retry operation. |
| `error.details` | `array` | No | Yes | Array of field-level validation errors or sub-exception descriptors. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": [],
  "error.code": "sample_value",
  "error.message": "sample_value",
  "error.category": "sample_value",
  "error.correlation_id": "018e3a20-0001-7000-8000-000000000001",
  "error.timestamp": "sample_value",
  "error.retryable": true,
  "error.details": []
}
```

### 9.SCHEMA-API-004 Schema Specification: `ValidationErrorItem`
- **Schema Identifier:** `SCHEMA-API-004`
- **Domain Category:** `Common`
- **Functional Scope:** Field-specific validation failure item embedded in error details.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `field` | `string` | **Yes** | No | JSON pointer or dotted path to invalid attribute (e.g., data.attributes.phone_number). |
| `rule` | `string` | **Yes** | No | Validation rule violated (e.g., pattern_mismatch, value_out_of_range, required_missing). |
| `rejected_value` | `any` | No | Yes | Sanitized rejected input value (redacted if PII/password). |
| `message` | `string` | **Yes** | No | Human-readable diagnostic guidance for correcting the field. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "field": "sample_value",
  "rule": "sample_value",
  "rejected_value": [],
  "message": "sample_value"
}
```

### 9.SCHEMA-API-005 Schema Specification: `CursorPaginationMetadata`
- **Schema Identifier:** `SCHEMA-API-005`
- **Domain Category:** `Common`
- **Functional Scope:** Standardized pagination cursor and navigation metadata.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `cursor` | `string` | **Yes** | No | Base64-encoded opaque cursor referencing current page boundary. |
| `next_cursor` | `string` | No | Yes | Opaque cursor for retrieving succeeding page (null if last page). |
| `prev_cursor` | `string` | No | Yes | Opaque cursor for retrieving preceding page (null if first page). |
| `has_more` | `boolean` | **Yes** | No | Indicator of whether additional records exist beyond current page. |
| `limit` | `integer` | **Yes** | No | Maximum page size requested or clamped by rate-limit policy (1..100). |
| `total_count` | `integer` | No | Yes | Optional total count where query plan allows fast index estimation. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "cursor": "sample_value",
  "next_cursor": "sample_value",
  "prev_cursor": "sample_value",
  "has_more": true,
  "limit": 100,
  "total_count": 100
}
```

### 9.SCHEMA-API-006 Schema Specification: `LoginRequest`
- **Schema Identifier:** `SCHEMA-API-006`
- **Domain Category:** `Auth`
- **Functional Scope:** Staff login payload submitting username, password, and facility scope.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `username` | `string` | **Yes** | No | Staff municipal employee ID or authorized email address. |
| `password` | `string` | **Yes** | No | Cleartext password (transmitted strictly over TLS 1.3; verified against Argon2id hash). |
| `facility_id` | `string` | **Yes** | No | UUIDv7 identifying Namma Clinic facility where shift is being initiated. |
| `device_fingerprint` | `string` | **Yes** | No | Cryptographic hardware signature of registered clinic workstation tablet. |
| `mfa_otp` | `string` | No | Yes | 6-digit TOTP token if MFA is enabled for role. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "username": "sample_value",
  "password": "sample_value",
  "facility_id": "018e3a20-0001-7000-8000-000000000001",
  "device_fingerprint": "sample_value",
  "mfa_otp": "sample_value"
}
```

### 9.SCHEMA-API-007 Schema Specification: `AuthTokenResponse`
- **Schema Identifier:** `SCHEMA-API-007`
- **Domain Category:** `Auth`
- **Functional Scope:** Authentication success response returning access and refresh tokens.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `access_token` | `string` | **Yes** | No | RS256-signed JWT access token with 15-minute lifespan. |
| `token_type` | `string` | **Yes** | No | Fixed string 'Bearer'. |
| `expires_in` | `integer` | **Yes** | No | Lifespan of access token in seconds (900 seconds). |
| `refresh_token` | `string` | **Yes** | No | Opaque high-entropy cryptographically random refresh token (8-hour sliding window). |
| `session_id` | `string` | **Yes** | No | UUIDv7 primary key in user_sessions table. |
| `user` | `object` | **Yes** | No | Staff identity profile object (id, full_name, role_code, facility_id). |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "access_token": "sample_value",
  "token_type": "sample_value",
  "expires_in": 100,
  "refresh_token": "sample_value",
  "session_id": "018e3a20-0001-7000-8000-000000000001",
  "user": []
}
```

### 9.SCHEMA-API-008 Schema Specification: `TokenRefreshRequest`
- **Schema Identifier:** `SCHEMA-API-008`
- **Domain Category:** `Auth`
- **Functional Scope:** Token rotation payload presenting active refresh token.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `refresh_token` | `string` | **Yes** | No | Current refresh token issued during login or last rotation. |
| `session_id` | `string` | **Yes** | No | UUIDv7 session identifier being refreshed. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "refresh_token": "sample_value",
  "session_id": "018e3a20-0001-7000-8000-000000000001"
}
```

### 9.SCHEMA-API-009 Schema Specification: `StaffSessionProfile`
- **Schema Identifier:** `SCHEMA-API-009`
- **Domain Category:** `Auth`
- **Functional Scope:** Current authenticated staff profile and permissions context.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | `string` | **Yes** | No | UUIDv7 staff identifier. |
| `username` | `string` | **Yes** | No | Staff municipal employee ID. |
| `full_name` | `string` | **Yes** | No | Display name of staff member. |
| `roles` | `array` | **Yes** | No | List of active role codes assigned to user. |
| `permissions` | `array` | **Yes** | No | List of fine-grained permission tokens granted across active roles. |
| `facility_context` | `object` | **Yes** | No | Active clinic facility metadata (id, name, zone, ward). |
| `shift_id` | `string` | No | Yes | Active shift identifier if clocked in. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "user_id": "018e3a20-0001-7000-8000-000000000001",
  "username": "sample_value",
  "full_name": "sample_value",
  "roles": [],
  "permissions": [],
  "facility_context": [],
  "shift_id": "018e3a20-0001-7000-8000-000000000001"
}
```

### 9.SCHEMA-API-010 Schema Specification: `PasswordChangeRequest`
- **Schema Identifier:** `SCHEMA-API-010`
- **Domain Category:** `Auth`
- **Functional Scope:** Self-service password update payload.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `current_password` | `string` | **Yes** | No | Existing staff password. |
| `new_password` | `string` | **Yes** | No | New password conforming to 12+ char complexity rules. |
| `confirm_password` | `string` | **Yes** | No | Verification repetition of new password. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "current_password": "sample_value",
  "new_password": "sample_value",
  "confirm_password": "sample_value"
}
```

### 9.SCHEMA-API-011 Schema Specification: `PatientRegistrationRequest`
- **Schema Identifier:** `SCHEMA-API-011`
- **Domain Category:** `Patient`
- **Functional Scope:** Citizen demographic intake payload for registering new patients at front desk.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `first_name` | `string` | **Yes** | No | Given legal name of citizen. |
| `last_name` | `string` | No | Yes | Family name or surname. |
| `gender` | `string` | **Yes** | No | Biological sex/gender (MALE, FEMALE, TRANSGENDER, OTHER). |
| `date_of_birth` | `string` | No | Yes | ISO-8601 date of birth (YYYY-MM-DD). |
| `estimated_age_years` | `integer` | No | Yes | Estimated age if birth date unknown. |
| `primary_phone` | `string` | **Yes** | No | 10-digit Indian mobile number (+91 assumed). |
| `abha_number` | `string` | No | Yes | 14-digit Ayushman Bharat Health Account number (XX-XXXX-XXXX-XXXX). |
| `abha_address` | `string` | No | Yes | ABHA virtual address handle (citizen@abdm). |
| `aadhaar_vault_ref` | `string` | No | Yes | Tokenized reference from secure Aadhaar Data Vault. |
| `address_line1` | `string` | **Yes** | No | Street address or landmark. |
| `bbmp_ward_number` | `integer` | **Yes** | No | BBMP ward number (1..243). |
| `postal_pincode` | `string` | **Yes** | No | 6-digit postal code (560001..560110). |
| `emergency_contact_name` | `string` | No | Yes | Next of kin or guardian name. |
| `emergency_contact_phone` | `string` | No | Yes | Next of kin phone number. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "first_name": "sample_value",
  "last_name": "sample_value",
  "gender": "sample_value",
  "date_of_birth": "sample_value",
  "estimated_age_years": 100,
  "primary_phone": "sample_value",
  "abha_number": "sample_value",
  "abha_address": "sample_value",
  "aadhaar_vault_ref": "sample_value",
  "address_line1": "sample_value",
  "bbmp_ward_number": 100,
  "postal_pincode": "sample_value",
  "emergency_contact_name": "sample_value",
  "emergency_contact_phone": "sample_value"
}
```

### 9.SCHEMA-API-012 Schema Specification: `PatientProfileResponse`
- **Schema Identifier:** `SCHEMA-API-012`
- **Domain Category:** `Patient`
- **Functional Scope:** Full citizen demographic and clinical continuity summary.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `string` | **Yes** | No | UUIDv7 citizen identifier. |
| `uhid` | `string` | **Yes** | No | Municipal Unique Health Identifier (NC-BLR-YYYY-XXXXXXXX). |
| `first_name` | `string` | **Yes** | No | Citizen first name. |
| `last_name` | `string` | No | Yes | Citizen last name. |
| `gender` | `string` | **Yes** | No | Citizen gender. |
| `date_of_birth` | `string` | **Yes** | No | Date of birth. |
| `primary_phone` | `string` | **Yes** | No | Masked mobile number (XXXXXX1234 on non-admin UI). |
| `abha_linked` | `boolean` | **Yes** | No | Boolean flag indicating verified ABHA linkage. |
| `registered_clinic_id` | `string` | **Yes** | No | Originating clinic facility ID. |
| `created_at` | `string` | **Yes** | No | Registration timestamp. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "id": "018e3a20-0001-7000-8000-000000000001",
  "uhid": "018e3a20-0001-7000-8000-000000000001",
  "first_name": "sample_value",
  "last_name": "sample_value",
  "gender": "sample_value",
  "date_of_birth": "sample_value",
  "primary_phone": "sample_value",
  "abha_linked": true,
  "registered_clinic_id": "018e3a20-0001-7000-8000-000000000001",
  "created_at": "sample_value"
}
```

### 9.SCHEMA-API-013 Schema Specification: `PatientSearchQuery`
- **Schema Identifier:** `SCHEMA-API-013`
- **Domain Category:** `Patient`
- **Functional Scope:** Multi-parameter phonetic and index query payload for patient lookup.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `query` | `string` | No | Yes | Free text name or UHID search string. |
| `phone` | `string` | No | Yes | Exact mobile number match. |
| `uhid` | `string` | No | Yes | Exact UHID match. |
| `abha_number` | `string` | No | Yes | Exact ABHA number match. |
| `ward_number` | `integer` | No | Yes | Filter by BBMP ward number. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "query": "sample_value",
  "phone": "sample_value",
  "uhid": "018e3a20-0001-7000-8000-000000000001",
  "abha_number": "sample_value",
  "ward_number": 100
}
```

### 9.SCHEMA-API-014 Schema Specification: `PatientDuplicateMatch`
- **Schema Identifier:** `SCHEMA-API-014`
- **Domain Category:** `Patient`
- **Functional Scope:** Duplicate candidate record identified by fuzzy phonetic and demographic matching.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `string` | **Yes** | No | UUIDv7 of candidate patient. |
| `uhid` | `string` | **Yes** | No | Candidate UHID. |
| `match_score` | `number` | **Yes** | No | Deterministic confidence score (0.0 to 1.0) computed via Jaro-Winkler and Soundex. |
| `matching_attributes` | `array` | **Yes** | No | List of colliding fields (phone, name_phonetic, dob, address). |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "patient_id": "018e3a20-0001-7000-8000-000000000001",
  "uhid": "018e3a20-0001-7000-8000-000000000001",
  "match_score": [],
  "matching_attributes": []
}
```

### 9.SCHEMA-API-015 Schema Specification: `PatientMergeRequest`
- **Schema Identifier:** `SCHEMA-API-015`
- **Domain Category:** `Patient`
- **Functional Scope:** Supervisory command payload merging duplicate patient records.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `surviving_patient_id` | `string` | **Yes** | No | UUIDv7 of primary record being retained. |
| `subsumed_patient_id` | `string` | **Yes** | No | UUIDv7 of duplicate record being merged and tombstoned. |
| `clinical_rationale` | `string` | **Yes** | No | Mandatory clinical justification for merge action. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "surviving_patient_id": "018e3a20-0001-7000-8000-000000000001",
  "subsumed_patient_id": "018e3a20-0001-7000-8000-000000000001",
  "clinical_rationale": "sample_value"
}
```

### 9.SCHEMA-API-016 Schema Specification: `VisitCreationRequest`
- **Schema Identifier:** `SCHEMA-API-016`
- **Domain Category:** `Visit`
- **Functional Scope:** OPD visit registration and token generation payload.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `string` | **Yes** | No | UUIDv7 patient identifier. |
| `visit_type` | `string` | **Yes** | No | Visit category: GENERAL_OPD, ANC_PNC, IMMUNIZATION, NCD_FOLLOWUP, EMERGENCY. |
| `is_emergency` | `boolean` | **Yes** | No | Fast-track emergency flag bypassing regular triage queue. |
| `priority_category` | `string` | **Yes** | No | Acuity level: ROUTINE, SENIOR_CITIZEN, MATERNAL, PEDIATRIC, RED_EMERGENCY. |
| `assigned_doctor_id` | `string` | No | Yes | Specific doctor ID if requested or assigned. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "patient_id": "018e3a20-0001-7000-8000-000000000001",
  "visit_type": "sample_value",
  "is_emergency": true,
  "priority_category": "sample_value",
  "assigned_doctor_id": "018e3a20-0001-7000-8000-000000000001"
}
```

### 9.SCHEMA-API-017 Schema Specification: `QueueTokenResponse`
- **Schema Identifier:** `SCHEMA-API-017`
- **Domain Category:** `Visit`
- **Functional Scope:** Issued daily queue token and waiting hall broadcast descriptor.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `visit_id` | `string` | **Yes** | No | UUIDv7 encounter visit identifier. |
| `token_number` | `string` | **Yes** | No | Daily formatted sequential token (e.g., A-042). |
| `sequence_number` | `integer` | **Yes** | No | Numeric daily sequence order. |
| `status` | `string` | **Yes** | No | Current status (ISSUED, CALLED, IN_CONSULTATION, COMPLETED, CANCELLED). |
| `room_number` | `string` | No | Yes | Assigned consultation room or triage cubicle. |
| `estimated_wait_minutes` | `integer` | **Yes** | No | Dynamically estimated waiting time in minutes. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "visit_id": "018e3a20-0001-7000-8000-000000000001",
  "token_number": "sample_value",
  "sequence_number": 100,
  "status": "sample_value",
  "room_number": "sample_value",
  "estimated_wait_minutes": 100
}
```

### 9.SCHEMA-API-018 Schema Specification: `QueueStatusUpdateCommand`
- **Schema Identifier:** `SCHEMA-API-018`
- **Domain Category:** `Visit`
- **Functional Scope:** Doctor/nurse command transitioning token queue state.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `action` | `string` | **Yes** | No | Action verb: CALL_NEXT, RECALL, MARK_IN_PROGRESS, HOLD, SKIP, COMPLETE. |
| `room_id` | `string` | **Yes** | No | UUIDv7 facility room where action is being executed. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "action": "sample_value",
  "room_id": "018e3a20-0001-7000-8000-000000000001"
}
```

### 9.SCHEMA-API-019 Schema Specification: `TriageAssessmentRequest`
- **Schema Identifier:** `SCHEMA-API-019`
- **Domain Category:** `Triage`
- **Functional Scope:** Nursing triage and physical vitals acquisition payload.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `visit_id` | `string` | **Yes** | No | UUIDv7 visit identifier. |
| `systolic_bp` | `integer` | No | Yes | Systolic blood pressure in mmHg (50..300). |
| `diastolic_bp` | `integer` | No | Yes | Diastolic blood pressure in mmHg (30..200). |
| `pulse_rate` | `integer` | **Yes** | No | Heart rate in beats per minute (30..250). |
| `temperature_fahrenheit` | `number` | **Yes** | No | Body temperature in Fahrenheit (90.0..110.0). |
| `spo2_percent` | `number` | **Yes** | No | Blood oxygen saturation percentage (50.0..100.0). |
| `respiratory_rate` | `integer` | No | Yes | Breaths per minute (8..60). |
| `weight_kg` | `number` | No | Yes | Body weight in kilograms (1.0..300.0). |
| `height_cm` | `number` | No | Yes | Height in centimeters (30.0..250.0). |
| `blood_glucose_mgdl` | `number` | No | Yes | Random blood sugar in mg/dL (20..800). |
| `acuity_color` | `string` | **Yes** | No | SATS triage acuity classification: RED, ORANGE, YELLOW, GREEN, BLUE. |
| `danger_signs_observed` | `array` | No | Yes | List of clinical danger signs (stridor, cyanosis, convulsion, shock). |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "visit_id": "018e3a20-0001-7000-8000-000000000001",
  "systolic_bp": 100,
  "diastolic_bp": 100,
  "pulse_rate": 100,
  "temperature_fahrenheit": [],
  "spo2_percent": [],
  "respiratory_rate": 100,
  "weight_kg": [],
  "height_cm": [],
  "blood_glucose_mgdl": [],
  "acuity_color": "sample_value",
  "danger_signs_observed": []
}
```

### 9.SCHEMA-API-020 Schema Specification: `TriageScoreResponse`
- **Schema Identifier:** `SCHEMA-API-020`
- **Domain Category:** `Triage`
- **Functional Scope:** Computed MEWS score, acuity tier, and immediate escalation guidance.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `triage_id` | `string` | **Yes** | No | UUIDv7 triage assessment primary key. |
| `mews_score` | `integer` | **Yes** | No | Calculated Modified Early Warning Score (0..14). |
| `acuity_category` | `string` | **Yes** | No | Determined triage color code (RED, ORANGE, YELLOW, GREEN, BLUE). |
| `is_critical_escalation` | `boolean` | **Yes** | No | Flag indicating automatic doctor pager / priority room diversion. |
| `alert_ids` | `array` | **Yes** | No | Generated danger alerts requiring medical officer acknowledgment. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "triage_id": "018e3a20-0001-7000-8000-000000000001",
  "mews_score": 100,
  "acuity_category": "sample_value",
  "is_critical_escalation": true,
  "alert_ids": "018e3a20-0001-7000-8000-000000000001"
}
```

### 9.SCHEMA-API-021 Schema Specification: `ConsultationEncounterRequest`
- **Schema Identifier:** `SCHEMA-API-021`
- **Domain Category:** `Consultation`
- **Functional Scope:** Doctor outpatient SOAP encounter notes, diagnosis coding, and care plan.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `visit_id` | `string` | **Yes** | No | UUIDv7 visit identifier. |
| `chief_complaints` | `array` | **Yes** | No | List of patient symptoms with duration and severity. |
| `history_of_present_illness` | `string` | No | Yes | Detailed clinical narrative of present illness. |
| `physical_examination_findings` | `string` | No | Yes | Systemic and local clinical examination observations. |
| `provisional_diagnoses` | `array` | **Yes** | No | List of primary diagnoses with ICD-10 and SNOMED CT codes. |
| `clinical_summary_notes` | `string` | **Yes** | No | Comprehensive SOAP progress note. |
| `follow_up_date` | `string` | No | Yes | Planned recall date for chronic care or reassessment (YYYY-MM-DD). |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "visit_id": "018e3a20-0001-7000-8000-000000000001",
  "chief_complaints": [],
  "history_of_present_illness": "sample_value",
  "physical_examination_findings": "sample_value",
  "provisional_diagnoses": [],
  "clinical_summary_notes": "sample_value",
  "follow_up_date": "sample_value"
}
```

### 9.SCHEMA-API-022 Schema Specification: `DiagnosisEntry`
- **Schema Identifier:** `SCHEMA-API-022`
- **Domain Category:** `Consultation`
- **Functional Scope:** Standardized diagnostic terminology entry.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `icd10_code` | `string` | **Yes** | No | WHO ICD-10 diagnostic code (e.g., E11.9, I10, J06.9). |
| `icd10_display` | `string` | **Yes** | No | Standard clinical name of diagnosis. |
| `snomed_concept_id` | `string` | No | Yes | SNOMED CT clinical concept identifier. |
| `diagnosis_type` | `string` | **Yes** | No | PRIMARY, SECONDARY, DIFFERENTIAL, RESOLVED. |
| `confidence_level` | `string` | **Yes** | No | CONFIRMED, SUSPECTED, RULED_OUT. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "icd10_code": "sample_value",
  "icd10_display": "sample_value",
  "snomed_concept_id": "018e3a20-0001-7000-8000-000000000001",
  "diagnosis_type": "sample_value",
  "confidence_level": "018e3a20-0001-7000-8000-000000000001"
}
```

### 9.SCHEMA-API-023 Schema Specification: `PrescriptionCreationRequest`
- **Schema Identifier:** `SCHEMA-API-023`
- **Domain Category:** `Prescription`
- **Functional Scope:** Electronic prescription authorization payload issued by treating physician.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `encounter_id` | `string` | **Yes** | No | UUIDv7 clinical encounter identifier. |
| `items` | `array` | **Yes** | No | List of prescribed medications adhering to BBMP formulary. |
| `doctor_instructions_kannada` | `string` | No | Yes | Localized instructions printed on citizen slip in Kannada. |
| `doctor_instructions_english` | `string` | No | Yes | Standard instructions printed in English. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "encounter_id": "018e3a20-0001-7000-8000-000000000001",
  "items": [],
  "doctor_instructions_kannada": "sample_value",
  "doctor_instructions_english": "sample_value"
}
```

### 9.SCHEMA-API-024 Schema Specification: `PrescriptionLineItem`
- **Schema Identifier:** `SCHEMA-API-024`
- **Domain Category:** `Prescription`
- **Functional Scope:** Individual medication line item in electronic prescription.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `drug_id` | `string` | **Yes** | No | UUIDv7 formulary drug identifier. |
| `dosage_form` | `string` | **Yes** | No | TABLET, CAPSULE, SYRUP, INJECTION, OINTMENT, DROPS. |
| `strength` | `string` | **Yes** | No | Strength specification (e.g., 500mg, 10ml, 5mg/ml). |
| `route` | `string` | **Yes** | No | Route of administration: ORAL, TOPICAL, INTRAVENOUS, INTRAMUSCULAR, INHALATION. |
| `frequency` | `string` | **Yes** | No | Standard frequency: ONCE_DAILY, TWICE_DAILY, THRICE_DAILY, FOUR_TIMES_DAILY, AS_NEEDED. |
| `duration_days` | `integer` | **Yes** | No | Treatment duration in days (1..90). |
| `quantity_prescribed` | `integer` | **Yes** | No | Total discrete units to be dispensed. |
| `timing_relation_to_food` | `string` | **Yes** | No | BEFORE_FOOD, AFTER_FOOD, WITH_FOOD, EMPTY_STOMACH. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "drug_id": "018e3a20-0001-7000-8000-000000000001",
  "dosage_form": "sample_value",
  "strength": "sample_value",
  "route": "sample_value",
  "frequency": "sample_value",
  "duration_days": 100,
  "quantity_prescribed": 100,
  "timing_relation_to_food": "sample_value"
}
```

### 9.SCHEMA-API-025 Schema Specification: `PharmacyDispenseRequest`
- **Schema Identifier:** `SCHEMA-API-025`
- **Domain Category:** `Pharmacy`
- **Functional Scope:** Pharmacist dispensation verification and batch allocation payload.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `prescription_id` | `string` | **Yes** | No | UUIDv7 prescription identifier. |
| `dispensed_items` | `array` | **Yes** | No | List of dispensed line items with allocated batch numbers. |
| `pharmacist_counseling_notes` | `string` | No | Yes | Notes confirming verbal counseling and dosage explanation. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "prescription_id": "018e3a20-0001-7000-8000-000000000001",
  "dispensed_items": [],
  "pharmacist_counseling_notes": "sample_value"
}
```

### 9.SCHEMA-API-026 Schema Specification: `DispensedLineItem`
- **Schema Identifier:** `SCHEMA-API-026`
- **Domain Category:** `Pharmacy`
- **Functional Scope:** Batch-allocated medication line item deducted from stock.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `prescription_item_id` | `string` | **Yes** | No | UUIDv7 prescription item identifier. |
| `batch_id` | `string` | **Yes** | No | UUIDv7 pharmacy batch identifier allocated via FEFO. |
| `quantity_dispensed` | `integer` | **Yes** | No | Actual discrete units issued to patient. |
| `is_partial_dispense` | `boolean` | **Yes** | No | Flag indicating partial fill due to stock exhaustion. |
| `substitution_drug_id` | `string` | No | Yes | Formulary substitute drug ID if generic substituted under doctor consent. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "prescription_item_id": "018e3a20-0001-7000-8000-000000000001",
  "batch_id": "018e3a20-0001-7000-8000-000000000001",
  "quantity_dispensed": 100,
  "is_partial_dispense": true,
  "substitution_drug_id": "018e3a20-0001-7000-8000-000000000001"
}
```

### 9.SCHEMA-API-027 Schema Specification: `StockReceiptRequest`
- **Schema Identifier:** `SCHEMA-API-027`
- **Domain Category:** `Inventory`
- **Functional Scope:** Clinic stock receipt from central BBMP warehouse or zonal depot.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `indent_id` | `string` | No | Yes | UUIDv7 indent requisition being fulfilled. |
| `invoice_number` | `string` | **Yes** | No | Depot dispatch challan / delivery invoice reference. |
| `received_batches` | `array` | **Yes** | No | Array of medication batches received into clinic stock. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "indent_id": "018e3a20-0001-7000-8000-000000000001",
  "invoice_number": "sample_value",
  "received_batches": []
}
```

### 9.SCHEMA-API-028 Schema Specification: `BatchReceiptItem`
- **Schema Identifier:** `SCHEMA-API-028`
- **Domain Category:** `Inventory`
- **Functional Scope:** Discrete pharmaceutical batch received into facility inventory.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `drug_id` | `string` | **Yes** | No | UUIDv7 formulary drug identifier. |
| `batch_number` | `string` | **Yes** | No | Manufacturer lot/batch alphanumeric code. |
| `expiry_date` | `string` | **Yes** | No | Expiration date (YYYY-MM-DD). |
| `quantity_received` | `integer` | **Yes** | No | Total discrete units received. |
| `manufacturer_name` | `string` | **Yes** | No | Pharmaceutical manufacturer name. |
| `cold_chain_compliant` | `boolean` | **Yes** | No | Confirmation that cold chain transit temperature was verified. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "drug_id": "018e3a20-0001-7000-8000-000000000001",
  "batch_number": "sample_value",
  "expiry_date": "sample_value",
  "quantity_received": 100,
  "manufacturer_name": "sample_value",
  "cold_chain_compliant": true
}
```

### 9.SCHEMA-API-029 Schema Specification: `StockAdjustmentCommand`
- **Schema Identifier:** `SCHEMA-API-029`
- **Domain Category:** `Inventory`
- **Functional Scope:** Physical inventory audit adjustment or write-off payload.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `batch_id` | `string` | **Yes** | No | UUIDv7 batch identifier being adjusted. |
| `adjusted_quantity` | `integer` | **Yes** | No | Delta quantity (+/- units) to reconcile stock. |
| `reason_code` | `string` | **Yes** | No | DAMAGED, EXPIRED, THEFT_LOSS, AUDIT_DISCREPANCY, BREAKAGE. |
| `supervisor_approval_token` | `string` | **Yes** | No | Dual-authorization cryptographic approval signature. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "batch_id": "018e3a20-0001-7000-8000-000000000001",
  "adjusted_quantity": 100,
  "reason_code": "sample_value",
  "supervisor_approval_token": "sample_value"
}
```

### 9.SCHEMA-API-030 Schema Specification: `LabOrderCreationRequest`
- **Schema Identifier:** `SCHEMA-API-030`
- **Domain Category:** `Lab`
- **Functional Scope:** Doctor requisition for diagnostic investigations.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `encounter_id` | `string` | **Yes** | No | UUIDv7 encounter identifier. |
| `test_ids` | `array` | **Yes** | No | List of diagnostic test catalog IDs (e.g., LOINC-mapped tests). |
| `clinical_indication` | `string` | **Yes** | No | Clinical reason for test ordering. |
| `is_urgent` | `boolean` | **Yes** | No | Stat test priority flag. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "encounter_id": "018e3a20-0001-7000-8000-000000000001",
  "test_ids": "018e3a20-0001-7000-8000-000000000001",
  "clinical_indication": "sample_value",
  "is_urgent": true
}
```

### 9.SCHEMA-API-031 Schema Specification: `LabResultEntryRequest`
- **Schema Identifier:** `SCHEMA-API-031`
- **Domain Category:** `Lab`
- **Functional Scope:** Lab technician diagnostic result capture and panic flag payload.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `lab_order_item_id` | `string` | **Yes** | No | UUIDv7 lab order line item identifier. |
| `numerical_value` | `number` | No | Yes | Quantitative test result value. |
| `unit_of_measure` | `string` | No | Yes | Standard measurement unit (mg/dL, g/dL, cells/mcL). |
| `qualitative_result` | `string` | No | Yes | Qualitative result: POSITIVE, NEGATIVE, REACTIVE, NON_REACTIVE. |
| `reference_range_text` | `string` | **Yes** | No | Biological reference interval printed on report. |
| `is_panic_value` | `boolean` | **Yes** | No | Flag indicating critical alert requiring immediate doctor phone alert. |
| `technician_observations` | `string` | No | Yes | Microscopic or technical remarks. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "lab_order_item_id": "018e3a20-0001-7000-8000-000000000001",
  "numerical_value": [],
  "unit_of_measure": "sample_value",
  "qualitative_result": "sample_value",
  "reference_range_text": "sample_value",
  "is_panic_value": true,
  "technician_observations": "sample_value"
}
```

### 9.SCHEMA-API-032 Schema Specification: `ReferralCreationRequest`
- **Schema Identifier:** `SCHEMA-API-032`
- **Domain Category:** `Referral`
- **Functional Scope:** Secondary/tertiary hospital transfer dossier payload.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `encounter_id` | `string` | **Yes** | No | UUIDv7 encounter initiating referral. |
| `destination_hospital_type` | `string` | **Yes** | No | BBMP_GENERAL_HOSPITAL, GOVT_MEDICAL_COLLEGE, SPECIALTY_INSTITUTE. |
| `urgency_level` | `string` | **Yes** | No | EMERGENCY_108, URGENT_24H, ROUTINE_SPECIALTY. |
| `referral_specialty` | `string` | **Yes** | No | CARDIOLOGY, OBGYN, ORTHOPEDICS, PEDIATRICS, PSYCHIATRY, ONCOLOGY. |
| `clinical_summary_dossier` | `string` | **Yes** | No | Comprehensive transfer summary including triage vitals and provisional diagnosis. |
| `transport_required` | `boolean` | **Yes** | No | Indicates whether 108 Arogya Kavacha ambulance was requested. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "encounter_id": "018e3a20-0001-7000-8000-000000000001",
  "destination_hospital_type": "sample_value",
  "urgency_level": "sample_value",
  "referral_specialty": "sample_value",
  "clinical_summary_dossier": "sample_value",
  "transport_required": true
}
```

### 9.SCHEMA-API-033 Schema Specification: `OutboundNotificationRequest`
- **Schema Identifier:** `SCHEMA-API-033`
- **Domain Category:** `Notification`
- **Functional Scope:** System-generated citizen SMS / WhatsApp message dispatch payload.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `string` | **Yes** | No | UUIDv7 recipient patient identifier. |
| `channel` | `string` | **Yes** | No | SMS, WHATSAPP, VOICE_IVR. |
| `template_id` | `string` | **Yes** | No | Approved DLT template registration code. |
| `preferred_language` | `string` | **Yes** | No | Language code: kn (Kannada) or en (English). |
| `template_parameters` | `object` | **Yes** | No | Dynamic variable bindings (citizen_name, clinic_name, token_number, date). |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "patient_id": "018e3a20-0001-7000-8000-000000000001",
  "channel": "sample_value",
  "template_id": "018e3a20-0001-7000-8000-000000000001",
  "preferred_language": "sample_value",
  "template_parameters": []
}
```

### 9.SCHEMA-API-034 Schema Specification: `ClinicKpiSummaryResponse`
- **Schema Identifier:** `SCHEMA-API-034`
- **Domain Category:** `Analytics`
- **Functional Scope:** Aggregated daily operational performance metrics for a clinic facility.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `string` | **Yes** | No | UUIDv7 facility identifier. |
| `metric_date` | `string` | **Yes** | No | Date of aggregation (YYYY-MM-DD). |
| `total_registered_opd` | `integer` | **Yes** | No | Total outpatient patient footfall. |
| `avg_consultation_time_seconds` | `number` | **Yes** | No | Average physician consultation duration. |
| `total_prescriptions_dispensed` | `integer` | **Yes** | No | Total pharmacy dispenses completed. |
| `stockout_drug_count` | `integer` | **Yes** | No | Number of critical formulary drugs currently at zero stock. |
| `red_triage_count` | `integer` | **Yes** | No | Count of emergency red triage cases managed. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "facility_id": "018e3a20-0001-7000-8000-000000000001",
  "metric_date": "sample_value",
  "total_registered_opd": 100,
  "avg_consultation_time_seconds": [],
  "total_prescriptions_dispensed": 100,
  "stockout_drug_count": 100,
  "red_triage_count": 100
}
```

### 9.SCHEMA-API-035 Schema Specification: `AuditEventQuery`
- **Schema Identifier:** `SCHEMA-API-035`
- **Domain Category:** `Audit`
- **Functional Scope:** Cryptographic WORM audit log query and verification payload.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `entity_type` | `string` | No | Yes | Audited entity name (e.g., patients, prescriptions). |
| `entity_id` | `string` | No | Yes | UUIDv7 entity primary key. |
| `actor_id` | `string` | No | Yes | UUIDv7 user ID who triggered event. |
| `event_type` | `string` | No | Yes | Action verb: CREATE, READ, UPDATE, DELETE, EXPORT, BREAK_GLASS. |
| `from_timestamp` | `string` | **Yes** | No | ISO-8601 start timestamp. |
| `to_timestamp` | `string` | **Yes** | No | ISO-8601 end timestamp. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "entity_type": "sample_value",
  "entity_id": "018e3a20-0001-7000-8000-000000000001",
  "actor_id": "018e3a20-0001-7000-8000-000000000001",
  "event_type": "sample_value",
  "from_timestamp": "sample_value",
  "to_timestamp": "sample_value"
}
```

### 9.SCHEMA-API-036 Schema Specification: `AbhaVerificationRequest`
- **Schema Identifier:** `SCHEMA-API-036`
- **Domain Category:** `ABDM`
- **Functional Scope:** ABDM M1 ABHA address discovery and OTP verification payload.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `auth_method` | `string` | **Yes** | No | MOBILE_OTP, AADHAAR_OTP, DEMOGRAPHICS. |
| `identifier` | `string` | **Yes** | No | 14-digit ABHA number or ABHA address string. |
| `otp` | `string` | No | Yes | 6-digit OTP received on citizen phone. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "auth_method": "sample_value",
  "identifier": "018e3a20-0001-7000-8000-000000000001",
  "otp": "sample_value"
}
```

### 9.SCHEMA-API-037 Schema Specification: `FhirBundleExportResponse`
- **Schema Identifier:** `SCHEMA-API-037`
- **Domain Category:** `ABDM`
- **Functional Scope:** FHIR R4 DiagnosticReport / Encounter document bundle for health record sharing.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `resourceType` | `string` | **Yes** | No | Fixed string 'Bundle'. |
| `type` | `string` | **Yes** | No | Fixed string 'document'. |
| `entry` | `array` | **Yes** | No | Array of FHIR R4 clinical resources (Composition, Patient, Encounter, Condition). |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "resourceType": "sample_value",
  "type": "sample_value",
  "entry": []
}
```

### 9.SCHEMA-API-038 Schema Specification: `PortabilityExportJobRequest`
- **Schema Identifier:** `SCHEMA-API-038`
- **Domain Category:** `Portability`
- **Functional Scope:** Citizen DPDP Act 2023 Section 12 Data Portability export request.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `string` | **Yes** | No | UUIDv7 citizen identifier. |
| `export_format` | `string` | **Yes** | No | FHIR_JSON, NDJSON, CSV_ZIP, PDF_ENCRYPTED. |
| `date_range_start` | `string` | No | Yes | Optional start date filter. |
| `date_range_end` | `string` | No | Yes | Optional end date filter. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "patient_id": "018e3a20-0001-7000-8000-000000000001",
  "export_format": "sample_value",
  "date_range_start": "sample_value",
  "date_range_end": "sample_value"
}
```

### 9.SCHEMA-API-039 Schema Specification: `PortabilityJobStatusResponse`
- **Schema Identifier:** `SCHEMA-API-039`
- **Domain Category:** `Portability`
- **Functional Scope:** Status and download link for asynchronous portability export job.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `job_id` | `string` | **Yes** | No | UUIDv7 background export task identifier. |
| `status` | `string` | **Yes** | No | QUEUED, PROCESSING, COMPLETED, FAILED, EXPIRED. |
| `progress_percent` | `integer` | **Yes** | No | Completion percentage (0..100). |
| `download_url` | `string` | No | Yes | Time-limited pre-signed S3 download URL (expires in 30 minutes). |
| `expires_at` | `string` | No | Yes | Expiration timestamp after which file is purged. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "job_id": "018e3a20-0001-7000-8000-000000000001",
  "status": "sample_value",
  "progress_percent": 100,
  "download_url": "sample_value",
  "expires_at": "sample_value"
}
```

### 9.SCHEMA-API-040 Schema Specification: `EdgeSyncBatchRequest`
- **Schema Identifier:** `SCHEMA-API-040`
- **Domain Category:** `System`
- **Functional Scope:** Offline mutation journal replay batch uploaded by clinic edge gateway.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `facility_id` | `string` | **Yes** | No | UUIDv7 clinic facility identifier. |
| `edge_node_id` | `string` | **Yes** | No | Cryptographic hardware identity of edge mini-server. |
| `vector_clock` | `object` | **Yes** | No | Lamport vector clock map of edge node states. |
| `mutations` | `array` | **Yes** | No | Ordered array of queued mutation records captured while offline. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "facility_id": "018e3a20-0001-7000-8000-000000000001",
  "edge_node_id": "018e3a20-0001-7000-8000-000000000001",
  "vector_clock": [],
  "mutations": []
}
```

### 9.SCHEMA-API-041 Schema Specification: `SyncMutationItem`
- **Schema Identifier:** `SCHEMA-API-041`
- **Domain Category:** `System`
- **Functional Scope:** Discrete mutation record executed on edge SQLite node.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `mutation_id` | `string` | **Yes** | No | UUIDv7 generated on edge tablet/server. |
| `target_table` | `string` | **Yes** | No | Target relational table name (e.g., patient_vitals). |
| `operation` | `string` | **Yes** | No | INSERT, UPDATE, SOFT_DELETE. |
| `row_id` | `string` | **Yes** | No | UUIDv7 primary key of target row. |
| `payload` | `object` | **Yes** | No | JSON serialized row attributes. |
| `edge_timestamp` | `string` | **Yes** | No | Local device timestamp when user committed action. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "mutation_id": "018e3a20-0001-7000-8000-000000000001",
  "target_table": "sample_value",
  "operation": "sample_value",
  "row_id": "018e3a20-0001-7000-8000-000000000001",
  "payload": [],
  "edge_timestamp": "sample_value"
}
```

### 9.SCHEMA-API-042 Schema Specification: `EdgeSyncBatchResponse`
- **Schema Identifier:** `SCHEMA-API-042`
- **Domain Category:** `System`
- **Functional Scope:** Cloud synchronization acknowledgment, conflict resolutions, and server updates.

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `reconciled_mutations` | `integer` | **Yes** | No | Count of successfully merged mutations. |
| `conflict_count` | `integer` | **Yes** | No | Count of mutations requiring CRDT last-write-wins or doctor resolution. |
| `conflicts` | `array` | **Yes** | No | Array of conflict resolution descriptors. |
| `server_delta_mutations` | `array` | **Yes** | No | Server-side updates from cloud to be ingested by edge node. |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "reconciled_mutations": 100,
  "conflict_count": 100,
  "conflicts": [],
  "server_delta_mutations": []
}
```

### 9.SCHEMA-API-043 Schema Specification: `HealthCheckLivenessResponse`
- **Schema Identifier:** `SCHEMA-API-043`
- **Domain Category:** `System`
- **Functional Scope:** Kubernetes liveness probe response

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `status` | `string` | **Yes** | No | Attribute status of HealthCheckLivenessResponse |
| `timestamp` | `string` | **Yes** | No | Attribute timestamp of HealthCheckLivenessResponse |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "status": "sample_value",
  "timestamp": "sample_value"
}
```

### 9.SCHEMA-API-044 Schema Specification: `HealthCheckReadinessResponse`
- **Schema Identifier:** `SCHEMA-API-044`
- **Domain Category:** `System`
- **Functional Scope:** Kubernetes readiness probe verifying DB and cache connectivity

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `status` | `string` | **Yes** | No | Attribute status of HealthCheckReadinessResponse |
| `dependencies` | `object` | **Yes** | No | Attribute dependencies of HealthCheckReadinessResponse |
| `healthy` | `boolean` | **Yes** | No | Attribute healthy of HealthCheckReadinessResponse |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "status": "sample_value",
  "dependencies": [],
  "healthy": true
}
```

### 9.SCHEMA-API-045 Schema Specification: `FacilityRoomStatusResponse`
- **Schema Identifier:** `SCHEMA-API-045`
- **Domain Category:** `Visit`
- **Functional Scope:** Real-time occupancy status of clinic examination room

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `room_id` | `string` | **Yes** | No | Attribute room_id of FacilityRoomStatusResponse |
| `occupancy_state` | `string` | **Yes** | No | Attribute occupancy_state of FacilityRoomStatusResponse |
| `active_doctor_id` | `string` | No | Yes | Attribute active_doctor_id of FacilityRoomStatusResponse |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "room_id": "018e3a20-0001-7000-8000-000000000001",
  "occupancy_state": "sample_value",
  "active_doctor_id": "018e3a20-0001-7000-8000-000000000001"
}
```

### 9.SCHEMA-API-046 Schema Specification: `VitalSignsSeriesResponse`
- **Schema Identifier:** `SCHEMA-API-046`
- **Domain Category:** `Triage`
- **Functional Scope:** Longitudinal vital signs readings for a patient across visits

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `string` | **Yes** | No | Attribute patient_id of VitalSignsSeriesResponse |
| `readings` | `array` | **Yes** | No | Attribute readings of VitalSignsSeriesResponse |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "patient_id": "018e3a20-0001-7000-8000-000000000001",
  "readings": []
}
```

### 9.SCHEMA-API-047 Schema Specification: `DangerAlertNotification`
- **Schema Identifier:** `SCHEMA-API-047`
- **Domain Category:** `Triage`
- **Functional Scope:** Critical physiologic deterioration alert payload

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `alert_id` | `string` | **Yes** | No | Attribute alert_id of DangerAlertNotification |
| `acuity` | `string` | **Yes** | No | Attribute acuity of DangerAlertNotification |
| `vital_trigger` | `string` | **Yes** | No | Attribute vital_trigger of DangerAlertNotification |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "alert_id": "018e3a20-0001-7000-8000-000000000001",
  "acuity": "sample_value",
  "vital_trigger": "sample_value"
}
```

### 9.SCHEMA-API-048 Schema Specification: `ClinicalNotePatchRequest`
- **Schema Identifier:** `SCHEMA-API-048`
- **Domain Category:** `Consultation`
- **Functional Scope:** Addendum or amendment payload for finalized consultation note

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `addendum_text` | `string` | **Yes** | No | Attribute addendum_text of ClinicalNotePatchRequest |
| `amendment_reason` | `string` | **Yes** | No | Attribute amendment_reason of ClinicalNotePatchRequest |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "addendum_text": "sample_value",
  "amendment_reason": "sample_value"
}
```

### 9.SCHEMA-API-049 Schema Specification: `DrugFormularyItemResponse`
- **Schema Identifier:** `SCHEMA-API-049`
- **Domain Category:** `Prescription`
- **Functional Scope:** Essential drugs formulary metadata and dosage guidelines

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `drug_id` | `string` | **Yes** | No | Attribute drug_id of DrugFormularyItemResponse |
| `generic_name` | `string` | **Yes** | No | Attribute generic_name of DrugFormularyItemResponse |
| `strength` | `string` | **Yes** | No | Attribute strength of DrugFormularyItemResponse |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "drug_id": "018e3a20-0001-7000-8000-000000000001",
  "generic_name": "sample_value",
  "strength": "sample_value"
}
```

### 9.SCHEMA-API-050 Schema Specification: `MedicationInteractionWarning`
- **Schema Identifier:** `SCHEMA-API-050`
- **Domain Category:** `Prescription`
- **Functional Scope:** CDSS drug-drug or drug-allergy contraindication alert

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `severity` | `string` | **Yes** | No | Attribute severity of MedicationInteractionWarning |
| `interacting_drugs` | `array` | **Yes** | No | Attribute interacting_drugs of MedicationInteractionWarning |
| `clinical_effect` | `string` | **Yes** | No | Attribute clinical_effect of MedicationInteractionWarning |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "severity": "sample_value",
  "interacting_drugs": [],
  "clinical_effect": "sample_value"
}
```

### 9.SCHEMA-API-051 Schema Specification: `PharmacyStockBalanceResponse`
- **Schema Identifier:** `SCHEMA-API-051`
- **Domain Category:** `Pharmacy`
- **Functional Scope:** On-hand inventory balance per batch in clinic dispensary

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `drug_id` | `string` | **Yes** | No | Attribute drug_id of PharmacyStockBalanceResponse |
| `batches` | `array` | **Yes** | No | Attribute batches of PharmacyStockBalanceResponse |
| `total_quantity` | `integer` | **Yes** | No | Attribute total_quantity of PharmacyStockBalanceResponse |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "drug_id": "018e3a20-0001-7000-8000-000000000001",
  "batches": [],
  "total_quantity": 100
}
```

### 9.SCHEMA-API-052 Schema Specification: `DispensingReversalRequest`
- **Schema Identifier:** `SCHEMA-API-052`
- **Domain Category:** `Pharmacy`
- **Functional Scope:** Void or reversal of incorrect dispensation transaction

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `dispense_id` | `string` | **Yes** | No | Attribute dispense_id of DispensingReversalRequest |
| `reversal_reason` | `string` | **Yes** | No | Attribute reversal_reason of DispensingReversalRequest |
| `returned_items` | `array` | **Yes** | No | Attribute returned_items of DispensingReversalRequest |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "dispense_id": "018e3a20-0001-7000-8000-000000000001",
  "reversal_reason": "sample_value",
  "returned_items": []
}
```

### 9.SCHEMA-API-053 Schema Specification: `ColdChainTelemetryBatch`
- **Schema Identifier:** `SCHEMA-API-053`
- **Domain Category:** `Inventory`
- **Functional Scope:** IoT temperature and power sensor readings from vaccine refrigerator

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `device_id` | `string` | **Yes** | No | Attribute device_id of ColdChainTelemetryBatch |
| `temperature_celsius` | `number` | **Yes** | No | Attribute temperature_celsius of ColdChainTelemetryBatch |
| `readings` | `array` | **Yes** | No | Attribute readings of ColdChainTelemetryBatch |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "device_id": "018e3a20-0001-7000-8000-000000000001",
  "temperature_celsius": [],
  "readings": []
}
```

### 9.SCHEMA-API-054 Schema Specification: `ColdChainExcursionAlert`
- **Schema Identifier:** `SCHEMA-API-054`
- **Domain Category:** `Inventory`
- **Functional Scope:** Vaccine temperature breach alert notification

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `alert_id` | `string` | **Yes** | No | Attribute alert_id of ColdChainExcursionAlert |
| `min_temp` | `number` | **Yes** | No | Attribute min_temp of ColdChainExcursionAlert |
| `max_temp` | `number` | **Yes** | No | Attribute max_temp of ColdChainExcursionAlert |
| `duration_minutes` | `integer` | **Yes** | No | Attribute duration_minutes of ColdChainExcursionAlert |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "alert_id": "018e3a20-0001-7000-8000-000000000001",
  "min_temp": [],
  "max_temp": [],
  "duration_minutes": 100
}
```

### 9.SCHEMA-API-055 Schema Specification: `LabSpecimenCollectionRequest`
- **Schema Identifier:** `SCHEMA-API-055`
- **Domain Category:** `Lab`
- **Functional Scope:** Phlebotomy specimen accession and barcode mapping

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `lab_order_id` | `string` | **Yes** | No | Attribute lab_order_id of LabSpecimenCollectionRequest |
| `barcode_id` | `string` | **Yes** | No | Attribute barcode_id of LabSpecimenCollectionRequest |
| `collection_time` | `string` | **Yes** | No | Attribute collection_time of LabSpecimenCollectionRequest |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "lab_order_id": "018e3a20-0001-7000-8000-000000000001",
  "barcode_id": "018e3a20-0001-7000-8000-000000000001",
  "collection_time": "sample_value"
}
```

### 9.SCHEMA-API-056 Schema Specification: `LabSpecimenRejectionPayload`
- **Schema Identifier:** `SCHEMA-API-056`
- **Domain Category:** `Lab`
- **Functional Scope:** Specimen rejection due to hemolysis, clotting, or volume insufficiency

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `order_item_id` | `string` | **Yes** | No | Attribute order_item_id of LabSpecimenRejectionPayload |
| `rejection_reason` | `string` | **Yes** | No | Attribute rejection_reason of LabSpecimenRejectionPayload |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "order_item_id": "018e3a20-0001-7000-8000-000000000001",
  "rejection_reason": "sample_value"
}
```

### 9.SCHEMA-API-057 Schema Specification: `ReferralCounterNoteResponse`
- **Schema Identifier:** `SCHEMA-API-057`
- **Domain Category:** `Referral`
- **Functional Scope:** Discharge summary received from tertiary hospital for referred patient

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `referral_id` | `string` | **Yes** | No | Attribute referral_id of ReferralCounterNoteResponse |
| `tertiary_diagnosis` | `string` | **Yes** | No | Attribute tertiary_diagnosis of ReferralCounterNoteResponse |
| `care_plan` | `string` | **Yes** | No | Attribute care_plan of ReferralCounterNoteResponse |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "referral_id": "018e3a20-0001-7000-8000-000000000001",
  "tertiary_diagnosis": "sample_value",
  "care_plan": "sample_value"
}
```

### 9.SCHEMA-API-058 Schema Specification: `SmsDeliveryReceiptPayload`
- **Schema Identifier:** `SCHEMA-API-058`
- **Domain Category:** `Notification`
- **Functional Scope:** Telecom gateway delivery status webhook callback

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `message_id` | `string` | **Yes** | No | Attribute message_id of SmsDeliveryReceiptPayload |
| `status` | `string` | **Yes** | No | Attribute status of SmsDeliveryReceiptPayload |
| `carrier_timestamp` | `string` | **Yes** | No | Attribute carrier_timestamp of SmsDeliveryReceiptPayload |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "message_id": "018e3a20-0001-7000-8000-000000000001",
  "status": "sample_value",
  "carrier_timestamp": "sample_value"
}
```

### 9.SCHEMA-API-059 Schema Specification: `EpidemicSurveillanceReport`
- **Schema Identifier:** `SCHEMA-API-059`
- **Domain Category:** `Analytics`
- **Functional Scope:** Syndromic fever and acute respiratory infection cluster report

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `ward_number` | `integer` | **Yes** | No | Attribute ward_number of EpidemicSurveillanceReport |
| `syndrome` | `string` | **Yes** | No | Attribute syndrome of EpidemicSurveillanceReport |
| `case_count` | `integer` | **Yes** | No | Attribute case_count of EpidemicSurveillanceReport |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "ward_number": 100,
  "syndrome": "sample_value",
  "case_count": 100
}
```

### 9.SCHEMA-API-060 Schema Specification: `DoctorWorkloadMetricResponse`
- **Schema Identifier:** `SCHEMA-API-060`
- **Domain Category:** `Analytics`
- **Functional Scope:** Outpatient encounters, average duration, and pending queue per doctor

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `doctor_id` | `string` | **Yes** | No | Attribute doctor_id of DoctorWorkloadMetricResponse |
| `patient_count` | `integer` | **Yes** | No | Attribute patient_count of DoctorWorkloadMetricResponse |
| `active_time_minutes` | `integer` | **Yes** | No | Attribute active_time_minutes of DoctorWorkloadMetricResponse |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "doctor_id": "018e3a20-0001-7000-8000-000000000001",
  "patient_count": 100,
  "active_time_minutes": 100
}
```

### 9.SCHEMA-API-061 Schema Specification: `AuditHashChainVerification`
- **Schema Identifier:** `SCHEMA-API-061`
- **Domain Category:** `Audit`
- **Functional Scope:** Cryptographic verification response for WORM audit hash integrity

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `verification_status` | `string` | **Yes** | No | Attribute verification_status of AuditHashChainVerification |
| `verified_block_count` | `integer` | **Yes** | No | Attribute verified_block_count of AuditHashChainVerification |
| `tamper_detected` | `boolean` | **Yes** | No | Attribute tamper_detected of AuditHashChainVerification |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "verification_status": "sample_value",
  "verified_block_count": 100,
  "tamper_detected": true
}
```

### 9.SCHEMA-API-062 Schema Specification: `AbdmConsentArtefactPayload`
- **Schema Identifier:** `SCHEMA-API-062`
- **Domain Category:** `ABDM`
- **Functional Scope:** Standard ABDM electronic consent artifact signed by citizen

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `consent_id` | `string` | **Yes** | No | Attribute consent_id of AbdmConsentArtefactPayload |
| `purpose` | `string` | **Yes** | No | Attribute purpose of AbdmConsentArtefactPayload |
| `date_range` | `object` | **Yes** | No | Attribute date_range of AbdmConsentArtefactPayload |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "consent_id": "018e3a20-0001-7000-8000-000000000001",
  "purpose": "sample_value",
  "date_range": []
}
```

### 9.SCHEMA-API-063 Schema Specification: `AbdmCareContextLinkRequest`
- **Schema Identifier:** `SCHEMA-API-063`
- **Domain Category:** `ABDM`
- **Functional Scope:** HIP care context linking request to associate visit with ABHA

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `patient_uhid` | `string` | **Yes** | No | Attribute patient_uhid of AbdmCareContextLinkRequest |
| `care_context_id` | `string` | **Yes** | No | Attribute care_context_id of AbdmCareContextLinkRequest |
| `display_name` | `string` | **Yes** | No | Attribute display_name of AbdmCareContextLinkRequest |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "patient_uhid": "018e3a20-0001-7000-8000-000000000001",
  "care_context_id": "018e3a20-0001-7000-8000-000000000001",
  "display_name": "sample_value"
}
```

### 9.SCHEMA-API-064 Schema Specification: `DataPortabilityConsentProof`
- **Schema Identifier:** `SCHEMA-API-064`
- **Domain Category:** `Portability`
- **Functional Scope:** Digital consent authorization token enabling data extraction

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | `string` | **Yes** | No | Attribute patient_id of DataPortabilityConsentProof |
| `consent_timestamp` | `string` | **Yes** | No | Attribute consent_timestamp of DataPortabilityConsentProof |
| `signature` | `string` | **Yes** | No | Attribute signature of DataPortabilityConsentProof |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "patient_id": "018e3a20-0001-7000-8000-000000000001",
  "consent_timestamp": "sample_value",
  "signature": "sample_value"
}
```

### 9.SCHEMA-API-065 Schema Specification: `HardwareTerminalRegisterRequest`
- **Schema Identifier:** `SCHEMA-API-065`
- **Domain Category:** `System`
- **Functional Scope:** Registration of clinic tablet or receipt printer with edge gateway

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `mac_address` | `string` | **Yes** | No | Attribute mac_address of HardwareTerminalRegisterRequest |
| `device_type` | `string` | **Yes** | No | Attribute device_type of HardwareTerminalRegisterRequest |
| `room_id` | `string` | **Yes** | No | Attribute room_id of HardwareTerminalRegisterRequest |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "mac_address": "sample_value",
  "device_type": "sample_value",
  "room_id": "018e3a20-0001-7000-8000-000000000001"
}
```

### 9.SCHEMA-API-066 Schema Specification: `DatabaseReplicationStatusResponse`
- **Schema Identifier:** `SCHEMA-API-066`
- **Domain Category:** `System`
- **Functional Scope:** Cloud PostgreSQL streaming replication lag and Patroni leader status

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `role` | `string` | **Yes** | No | Attribute role of DatabaseReplicationStatusResponse |
| `replication_lag_bytes` | `integer` | **Yes** | No | Attribute replication_lag_bytes of DatabaseReplicationStatusResponse |
| `in_sync` | `boolean` | **Yes** | No | Attribute in_sync of DatabaseReplicationStatusResponse |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "role": "sample_value",
  "replication_lag_bytes": 100,
  "in_sync": true
}
```

### 9.SCHEMA-API-067 Schema Specification: `UserRoleAssignmentPayload`
- **Schema Identifier:** `SCHEMA-API-067`
- **Domain Category:** `Auth`
- **Functional Scope:** Administrative assignment of role and facility scope to staff member

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | `string` | **Yes** | No | Attribute user_id of UserRoleAssignmentPayload |
| `role_codes` | `array` | **Yes** | No | Attribute role_codes of UserRoleAssignmentPayload |
| `facility_ids` | `array` | **Yes** | No | Attribute facility_ids of UserRoleAssignmentPayload |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "user_id": "018e3a20-0001-7000-8000-000000000001",
  "role_codes": [],
  "facility_ids": "018e3a20-0001-7000-8000-000000000001"
}
```

### 9.SCHEMA-API-068 Schema Specification: `BulkImportStatusResponse`
- **Schema Identifier:** `SCHEMA-API-068`
- **Domain Category:** `System`
- **Functional Scope:** Status of administrative bulk data ingestion (formulary, providers)

| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `batch_id` | `string` | **Yes** | No | Attribute batch_id of BulkImportStatusResponse |
| `total_rows` | `integer` | **Yes** | No | Attribute total_rows of BulkImportStatusResponse |
| `processed_rows` | `integer` | **Yes** | No | Attribute processed_rows of BulkImportStatusResponse |
| `error_count` | `integer` | **Yes** | No | Attribute error_count of BulkImportStatusResponse |

#### Example JSON Payload
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "batch_id": "018e3a20-0001-7000-8000-000000000001",
  "total_rows": 100,
  "processed_rows": 100,
  "error_count": 100
}
```

## 10. Concrete HTTP Request and Response Wire Examples

The following subsections provide concrete HTTP wire-level exchanges for major functional domains:

### 10.Auth Domain Wire Example: Staff Login (`POST /api/v1/auth/login`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/auth/login HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"username": "DOC-1024", "password": "Secret@2026", "facilityId": "018e3a20-0008-7000-8000-000000000001", "deviceFingerprint": "tab-blr-042"}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-auth-hash"

{"accessToken": "eyJhbGciOiJSUzI1Ni...", "tokenType": "Bearer", "expiresIn": 900}
```

### 10.Patient Domain Wire Example: Patient Registration (`POST /api/v1/patients`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/patients HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"firstName": "Sunita", "primaryPhone": "9876543210", "gender": "FEMALE", "bbmpWardNumber": 142}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-patient-hash"

{"id": "018e3a20-0001-7000-8000-000000000001", "uhid": "NC-BLR-2026-00000042"}
```

### 10.Visit Domain Wire Example: Queue Token Creation (`POST /api/v1/visits`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/visits HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"patientId": "018e3a20-0001-7000-8000-000000000001", "visitType": "GENERAL_OPD", "priorityCategory": "ROUTINE"}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-visit-hash"

{"visitId": "018e3a20-0018-7000-8000-000000000001", "tokenNumber": "A-042", "sequenceNumber": 42}
```

### 10.Triage Domain Wire Example: Record Vitals (`POST /api/v1/triage`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/triage HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"visitId": "018e3a20-0018-7000-8000-000000000001", "systolicBp": 120, "diastolicBp": 80, "pulseRate": 72, "temperatureFahrenheit": 98.4, "spo2Percent": 99.0, "acuityColor": "GREEN"}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-triage-hash"

{"triageId": "018e3a20-0020-7000-8000-000000000001", "mewsScore": 0, "acuityCategory": "GREEN"}
```

### 10.Consultation Domain Wire Example: Finalize Notes (`POST /api/v1/consultations`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/consultations HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"visitId": "018e3a20-0018-7000-8000-000000000001", "chiefComplaints": [{"symptom": "Fever", "durationDays": 3}], "provisionalDiagnoses": [{"icd10Code": "A90", "icd10Display": "Dengue fever"}]}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-consultation-hash"

{"encounterId": "018e3a20-0023-7000-8000-000000000001", "status": "FINALIZED"}
```

### 10.Prescription Domain Wire Example: Issue E-Prescription (`POST /api/v1/prescriptions`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/prescriptions HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"encounterId": "018e3a20-0023-7000-8000-000000000001", "items": [{"drugId": "018e3a20-0032-7000-8000-000000000001", "dosageForm": "TABLET", "strength": "500mg", "frequency": "THRICE_DAILY", "durationDays": 5, "quantityPrescribed": 15}]}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-prescription-hash"

{"prescriptionId": "018e3a20-0026-7000-8000-000000000001", "status": "SIGNED"}
```

### 10.Pharmacy Domain Wire Example: Dispense Medicines (`POST /api/v1/pharmacy/dispense`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/pharmacy/dispense HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"prescriptionId": "018e3a20-0026-7000-8000-000000000001", "dispensedItems": [{"batchId": "018e3a20-0034-7000-8000-000000000001", "quantityDispensed": 15}]}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-pharmacy-hash"

{"dispensationId": "018e3a20-0036-7000-8000-000000000001", "status": "COMPLETED"}
```

### 10.Inventory Domain Wire Example: Receive Stock (`POST /api/v1/inventory/receipts`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/inventory/receipts HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"invoiceNumber": "DEPOT-INV-891", "receivedBatches": [{"drugId": "018e3a20-0032-7000-8000-000000000001", "batchNumber": "PCM-26-A", "expiryDate": "2028-12-31", "quantityReceived": 1000}]}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-inventory-hash"

{"receiptId": "018e3a20-0038-7000-8000-000000000001", "status": "POSTED"}
```

### 10.Lab Domain Wire Example: Order Diagnostic Test (`POST /api/v1/lab/orders`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/lab/orders HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"encounterId": "018e3a20-0023-7000-8000-000000000001", "testIds": ["LOINC-4544-3"], "clinicalIndication": "Suspected dengue fever", "isUrgent": true}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-lab-hash"

{"orderId": "018e3a20-0028-7000-8000-000000000001", "status": "PENDING_COLLECTION"}
```

### 10.Referral Domain Wire Example: Refer Patient (`POST /api/v1/referrals`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/referrals HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"encounterId": "018e3a20-0023-7000-8000-000000000001", "destinationHospitalType": "BBMP_GENERAL_HOSPITAL", "urgencyLevel": "EMERGENCY_108", "referralSpecialty": "CARDIOLOGY"}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-referral-hash"

{"referralId": "018e3a20-0043-7000-8000-000000000001", "status": "DISPATCHED"}
```

### 10.Notification Domain Wire Example: Send SMS Reminder (`POST /api/v1/notifications/send`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/notifications/send HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"patientId": "018e3a20-0001-7000-8000-000000000001", "channel": "SMS", "templateId": "DLT-KN-APPT-01", "preferredLanguage": "kn"}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-notification-hash"

{"messageId": "018e3a20-0047-7000-8000-000000000001", "status": "QUEUED"}
```

### 10.Analytics Domain Wire Example: Fetch Daily Clinic KPIs (`GET /api/v1/analytics/kpi/daily`)
```http
# DOCUMENTATION-ONLY EXAMPLE
GET /api/v1/analytics/kpi/daily HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-analytics-hash"

{"facilityId": "018e3a20-0008-7000-8000-000000000001", "totalRegisteredOpd": 148, "avgConsultationTimeSeconds": 380, "redTriageCount": 2}
```

### 10.Audit Domain Wire Example: Query WORM Audit Log (`GET /api/v1/audit/events`)
```http
# DOCUMENTATION-ONLY EXAMPLE
GET /api/v1/audit/events HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-audit-hash"

{"verifiedBlockCount": 45000, "tamperDetected": false}
```

### 10.ABDM Domain Wire Example: Verify ABHA OTP (`POST /api/v1/abdm/abha/verify-otp`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/abdm/abha/verify-otp HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"identifier": "14-1234-5678-9012", "otp": "123456"}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-abdm-hash"

{"abhaNumber": "14-1234-5678-9012", "verificationStatus": "VERIFIED"}
```

### 10.Portability Domain Wire Example: Request FHIR Export (`POST /api/v1/portability/jobs`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/portability/jobs HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"patientId": "018e3a20-0001-7000-8000-000000000001", "exportFormat": "FHIR_JSON"}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-portability-hash"

{"jobId": "018e3a20-0052-7000-8000-000000000001", "status": "PROCESSING"}
```

### 10.System Domain Wire Example: Replay Edge Mutation Log (`POST /api/v1/system/sync/batch`)
```http
# DOCUMENTATION-ONLY EXAMPLE
POST /api/v1/system/sync/batch HTTP/1.1
Host: api.nammaclinic.bbmp.gov.in
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
X-Facility-ID: 018e3a20-0008-7000-8000-000000000001
Content-Type: application/json

{"facilityId": "018e3a20-0008-7000-8000-000000000001", "mutations": []}

HTTP/1.1 200 OK
Content-Type: application/json
X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001
ETag: W/"sha256-system-hash"

{"reconciledMutations": 18, "conflictCount": 0}
```

## 11. Authoritative Validation Regular Expressions & Masking Catalog

All ingress request attributes enforce strict client- and gateway-level regular expression validation:

| Identifier / Attribute | JSON Field Path | Regex Pattern | Format Description | Masked Display Example |
| :--- | :--- | :--- | :--- | :--- |
| **Mobile Phone Number** | `primaryPhone` | `^[6-9]\d{9}$` | 10-digit Indian national mobile number starting with 6, 7, 8, or 9 | `XXXXXX8921` |
| **Municipal UHID** | `uhid` | `^NC-BLR-\d{4}-\d{8}$` | Namma Clinic Unique Health Identifier format NC-BLR-YYYY-XXXXXXXX | `NC-BLR-2026-00000042` |
| **ABHA Number** | `abhaNumber` | `^\d{2}-\d{4}-\d{4}-\d{4}$` | 14-digit national Ayushman Bharat Health Account number | `14-1234-5678-9012` |
| **ABHA Address** | `abhaAddress` | `^[a-zA-Z0-9._]{4,32}@[a-zA-Z0-9]{3,16}$` | ABHA PHR virtual address handle (citizen@abdm) | `sunita.gowda@abdm` |
| **Postal PIN Code** | `postalPincode` | `^560\d{3}$` | Bengaluru postal delivery zone pincode (560001 to 560110) | `560042` |
| **UUIDv7 Identifier** | `id, correlationId` | `^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` | RFC 9562 draft time-ordered 128-bit UUIDv7 format | `018e3a20-0001-7000-8000-000000000001` |
| **WHO ICD-10 Code** | `icd10Code` | `^[A-Z]\d{2}(\.\d{1,2})?$` | World Health Organization International Classification of Diseases 10th Revision | `E11.9` |
| **LOINC Code** | `loincCode` | `^\d{3,5}-\d$` | Logical Observation Identifiers Names and Codes laboratory test identifier | `4544-3` |
| **Password Complexity** | `password` | `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,64}$` | 12-64 chars with lowercase, uppercase, number, and special symbol | `Redacted` |
| **Date Format (ISO)** | `dateOfBirth, followUpDate` | `^\d{4}-\d{2}-\d{2}$` | ISO-8601 calendar date YYYY-MM-DD | `1984-06-15` |
| **Timestamp (ISO UTC)** | `createdAt, timestamp` | `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$` | ISO-8601 UTC timestamp with optional millisecond precision | `2026-09-01T09:15:30.124Z` |

## 12. Filtering & Comparison Operators Reference

The API gateway supports 14 standard query filter operators:

| Operator | Query Parameter Syntax | Semantic Meaning | Relational SQL Translation |
| :--- | :--- | :--- | :--- |
| `eq` | `filter[status][eq]=ACTIVE` | Equal to comparison | `SELECT * FROM t WHERE status = 'ACTIVE'` |
| `ne` | `filter[status][ne]=CANCELLED` | Not equal to comparison | `SELECT * FROM t WHERE status != 'CANCELLED'` |
| `gt` | `filter[age][gt]=60` | Greater than strictly | `SELECT * FROM t WHERE age > 60` |
| `gte` | `filter[createdAt][gte]=2026-09-01T00:00:00Z` | Greater than or equal to | `SELECT * FROM t WHERE created_at >= '2026-09-01 00:00:00'` |
| `lt` | `filter[stockQuantity][lt]=10` | Less than strictly (low stock warning) | `SELECT * FROM t WHERE stock_quantity < 10` |
| `lte` | `filter[temperature][lte]=98.6` | Less than or equal to | `SELECT * FROM t WHERE temperature <= 98.6` |
| `in` | `filter[priorityCategory][in]=ROUTINE,MATERNAL` | In discrete set of values | `SELECT * FROM t WHERE priority_category IN ('ROUTINE', 'MATERNAL')` |
| `nin` | `filter[status][nin]=CLOSED,VOID` | Not in discrete set of values | `SELECT * FROM t WHERE status NOT IN ('CLOSED', 'VOID')` |
| `like` | `filter[firstName][like]=Sunit%` | Prefix string search | `SELECT * FROM t WHERE first_name LIKE 'Sunit%'` |
| `ilike` | `filter[lastName][ilike]=%gowda%` | Case-insensitive substring search | `SELECT * FROM t WHERE last_name ILIKE '%gowda%'` |
| `is_null` | `filter[closedAt][is_null]=true` | Checks for SQL NULL value | `SELECT * FROM t WHERE closed_at IS NULL` |
| `not_null` | `filter[abhaNumber][not_null]=true` | Checks for populated non-NULL value | `SELECT * FROM t WHERE abha_number IS NOT NULL` |
| `between` | `filter[createdAt][between]=2026-09-01,2026-09-07` | Closed range inclusion | `SELECT * FROM t WHERE created_at BETWEEN '2026-09-01' AND '2026-09-07'` |
| `contains` | `filter[tags][contains]=NCD_HYPERTENSION` | JSONB array element containment | `SELECT * FROM t WHERE tags @> '["NCD_HYPERTENSION"]'` |

## 13. Idempotency Key Processing Lifecycle & State Machine

To prevent duplicate patient registrations or double-dispensing during network hiccups, `X-Idempotency-Key` headers are processed via Redis distributed locks:

```mermaid
stateDiagram-v2
    [*] --> CheckRedis: Ingress POST with X-Idempotency-Key
    CheckRedis --> KeyNotFound: Key not in Redis
    CheckRedis --> KeyProcessing: Key state = IN_PROGRESS
    CheckRedis --> KeyCompleted: Key state = COMPLETED
    KeyNotFound --> AcquireLock: SETNX key IN_PROGRESS (TTL 60s)
    AcquireLock --> ExecuteHandler: Execute Transactional Handler
    ExecuteHandler --> SaveResponse: Store Response Body & Status (TTL 86400s)
    SaveResponse --> DeliverClient: Deliver Fresh Response to Client
    KeyProcessing --> Return409: Return HTTP 409 Conflict (ERR-SYS-004)
    KeyCompleted --> VerifyChecksum: Compare Request Body Hash
    VerifyChecksum --> ReplayResponse: Hash Matches: Replay Cached Response
    VerifyChecksum --> MismatchError: Hash Differs: Return HTTP 409 Payload Mismatch
    DeliverClient --> [*]
    Return409 --> [*]
    ReplayResponse --> [*]
    MismatchError --> [*]
```

## 14. Relationship Expansion & Sub-Resource Embedding Matrix

To minimize HTTP round-trips from frontline tablet clients, the API gateway supports compound document expansion via the `expand` parameter (maximum 2 levels deep):

| Primary Resource | Supported Expansion Path (`expand=...`) | Clinical / Operational Use Case |
| :--- | :--- | :--- |
| `patients` | `contacts,addresses,identifiers` | Encounter registration desk fetches full contact & national IDs in single query |
| `patients` | `encounters,consents` | Clinical consultation view expands active encounter history and valid consent directives |
| `visits` | `patient,triage,room` | Queue orchestration displays patient name, MEWS acuity color, and doctor room assignment |
| `clinical_encounters` | `notes,diagnoses,vitals` | SOAP progress note review renders clinician notes, ICD-10 codes, and triage readings |
| `prescriptions` | `items,doctor,facility` | Pharmacy dispensing screen expands prescribed drug line items and authorizing doctor signature |
| `dispensations` | `items.batch,prescription` | Stock audit inspects dispensed items with allocated batch numbers and parent prescription |
| `lab_orders` | `items.results,encounter` | Diagnostic lab review displays test orders, specimen barcodes, and recorded results |
| `referrals` | `encounter.diagnoses,counter_notes` | Secondary hospital intake expands referral reason, primary diagnosis, and return notes |
| `clinic_stock` | `batch,drug` | Pharmacy inventory dashboard displays on-hand balance, batch expiry date, and formulary name |
| `drug_indents` | `items.drug,approver` | Central warehouse fulfillment view expands requested medicines and medical superintendent approval |
| `cold_chain_devices` | `telemetry,facility` | IoT vaccine cold-chain dashboard displays device model, clinic ward, and recent temperature log |
| `ncd_episodes` | `patient,schedules` | Chronic disease tracking dashboard expands patient profile and upcoming follow-up appointments |

## 15. HTTP Caching, Compression & Gateway Negotiation Standards

The platform enforces deterministic caching headers based on data classification and mutability:

| Data Classification Tier | Mandatory Cache-Control Header | Compression & ETag Policy | Storage Scope |
| :--- | :--- | :--- | :--- |
| **PUBLIC Reference Data (Formulary, Wards)** | `Cache-Control: public, max-age=86400, stale-while-revalidate=3600` | `ETag + Brotli/Gzip` | CDN & Browser Cache (24 hours) |
| **CONFIDENTIAL Clinical Records (Encounters, Vitals)** | `Cache-Control: private, no-cache, no-store, must-revalidate` | `ETag (Conditional 304 Only)` | Zero Local Shared Cache; In-Memory Only |
| **RESTRICTED PII / Identifiers (Patients, Demographics)** | `Cache-Control: private, no-store, max-age=0, s-maxage=0` | `None (Direct SSL)` | Encrypted Workstation Session Memory Only |
| **HIGHLY-RESTRICTED Audit & Security Secrets** | `Cache-Control: no-store, no-cache, private` | `None` | Strictly Ephemeral (Zero Cache) |
| **System Configuration & Feature Flags** | `Cache-Control: public, max-age=300, stale-if-error=86400` | `ETag + Gzip` | Edge Gateway Cache (5 minutes) |

## 16. API Conventions Acceptance Criteria (BDD)

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Enforce Standard Error Envelope on Validation Failure
  Given an authenticated registration user
  And transmitting a patient creation request missing mandatory first_name
  When the client submits the payload to /api/v1/patients
  Then the API gateway rejects the request with HTTP 400 Bad Request
  And returns the standard error envelope matching SCHEMA-API-003
  And contains error code 'ERR-SYS-001' or 'ERR-PATIENT-011'
  And details array points to field 'data.attributes.firstName'
  And correlation ID matches the X-Correlation-ID response header
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Cursor Pagination Traversal and Limit Enforcement
  Given an authenticated clinical staff member
  And querying /api/v1/patients with limit=25
  When the client requests the first page of patients
  Then the API returns HTTP 200 OK with exactly 25 patient items
  And the pagination metadata includes an opaque next_cursor string
  And has_more is true if additional records exist
  And requesting with the next_cursor returns the next deterministic partition of records
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Optimistic Concurrency Control via If-Match ETag Header
  Given an authenticated clinician with stale patient data ETag W/"old-hash"
  And another clinician has concurrently updated the patient address
  When the clinician submits a PUT /api/v1/patients/{id} with If-Match: W/"old-hash"
  Then the database detects an ETag revision mismatch
  And the API gateway rejects the mutation with HTTP 412 Precondition Failed
  And returns error code 'ERR-SYS-005'
  And the client workstation prompts the clinician to reload the latest changes
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Idempotent Replay of Mutation Request with Identical Key
  Given a client workstation that experienced a network timeout during POST /api/v1/prescriptions
  And the server successfully processed the original prescription with X-Idempotency-Key '018e3a20-0026-7000-8000-000000000001'
  When the client resubmits the identical prescription payload with the same idempotency key
  Then the API gateway detects the completed transaction key in Redis cache
  And verifies that the request payload SHA-256 hash matches the original request
  And replays the cached HTTP 201 Created response without re-executing database inserts
  And includes the header 'X-Cache-Lookup: IDEMPOTENT-HIT'
```
