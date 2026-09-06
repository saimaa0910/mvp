"""
gen_api_02_conventions.py
Generator for docs/08-api/02-api-conventions.md
Produces >= 2,200 substantive lines defining authoritative REST conventions, HTTP headers,
JSON envelopes, UUIDv7 standards, pagination, filtering, ETags, and concrete examples.
"""

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.api.api_gen_common import write_api_doc, make_openapi_snippet, make_bdd_scenario
from scripts.api.api_core_data import API_SCHEMAS, API_ERROR_CODES, API_ENDPOINTS
from scripts.database.db_tables_entities import TABLES

def generate_doc():
    lines = []
    lines.append("# 🔌 API Specification: RESTful API Conventions & Design Standards")
    lines.append("## Namma Clinic Digital Health & Operations Platform")
    lines.append("**Document Code:** API-DOC-02 | **Status:** Authoritative Baseline | **Date:** September 2026")
    lines.append("> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department")
    lines.append("> **Standard Framework:** RFC 7231 (HTTP/1.1), RFC 7807 (Problem Details), JSON:API v1.1, UUIDv7 Draft RFC")
    lines.append("> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 1. Executive Summary & Design System
    lines.append("## 1. Executive Summary & Core Design System")
    lines.append("")
    lines.append("This document establishes the mandatory design conventions, syntax rules, HTTP protocol bindings, serialization standards, and error formatting for all RESTful services across the Namma Clinic platform. Uniformity across all 16 functional domains is enforced at the API gateway layer, ensuring consistent developer experience, deterministic client caching, and robust automated validation.")
    lines.append("")

    # 2. URI & Resource Naming Conventions
    lines.append("## 2. Resource Naming & URI Formatting Standards")
    lines.append("")
    lines.append("### 2.1 URI Structure & Path Hierarchy")
    lines.append("All endpoints must conform to the following URI path template:")
    lines.append("`https://{host}/api/v{major_version}/{domain_resource}/{resource_id}/{sub_resource}`")
    lines.append("")
    lines.append("Rules:")
    lines.append("- **Kebab-Case Paths:** All multi-word path segments must use lowercase kebab-case (e.g., `/api/v1/patient-identifiers`, `/api/v1/clinical-encounters`).")
    lines.append("- **Plural Nouns:** Top-level resource segments must always be plural nouns (e.g., `/patients`, `/prescriptions`, `/dispensations`). Singular resources are strictly prohibited.")
    lines.append("- **No Action Verbs in Path:** RPC-style action verbs in paths (e.g., `/api/v1/getPatients` or `/createVisit`) are forbidden. Verbs are expressed exclusively via HTTP methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).")
    lines.append("- **Sub-Resource Nesting:** Nesting is limited to a maximum depth of two levels (e.g., `/patients/{id}/encounters` or `/prescriptions/{id}/items`). Deeper relationships must be queried via top-level filtering.")
    lines.append("")

    # Full table of resource names for all 52 tables
    lines.append("### 2.2 Authoritative Resource Endpoint Mapping Table (52 Resources)")
    lines.append("Every database table is bound to a canonical RESTful resource path:")
    lines.append("")
    lines.append("| Table ID | Table Name | Canonical REST Path | Permitted Verbs | Default Sort Field | Scope |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for t in TABLES:
        slug = t["name"].replace("_", "-")
        verbs = "GET, POST, PUT, PATCH, DELETE" if not t["name"].startswith("audit_") else "GET (Read-Only)"
        sort_f = "-created_at"
        lines.append(f"| `{t['id']}` | `{t['name']}` | `/api/v1/{slug}` | `{verbs}` | `{sort_f}` | `{t['domain']}` |")
    lines.append("")

    # 3. HTTP Methods & Status Codes
    lines.append("## 3. HTTP Methods, Status Codes, and Idempotency Semantics")
    lines.append("")
    lines.append("The platform adheres to strict RFC 7231 method semantics:")
    lines.append("")
    lines.append("| HTTP Verb | CRUD Action | Idempotent | Safe | Success Status | Client Error Status | Cacheable |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    lines.append("| `GET` | Read Resource | **Yes** | **Yes** | `200 OK` | `400`, `401`, `403`, `404` | Yes (with ETag) |")
    lines.append("| `POST` | Create / Action | **No** (Enforced via Key) | **No** | `201 Created` / `202 Accepted` | `400`, `409`, `422` | No |")
    lines.append("| `PUT` | Full Replace | **Yes** | **No** | `200 OK` | `400`, `404`, `412` | No |")
    lines.append("| `PATCH` | Partial Update | **No** (Conditionally) | **No** | `200 OK` | `400`, `404`, `412` | No |")
    lines.append("| `DELETE`| Soft Delete | **Yes** | **No** | `200 OK` / `204 No Content` | `403`, `404` | No |")
    lines.append("")

    # Detailed status codes catalog
    status_codes_catalog = [
        (200, "OK", "Standard success response for GET, PUT, PATCH, or non-creation POST operations."),
        (201, "Created", "Resource successfully created via POST. Returns created resource and Location header."),
        (202, "Accepted", "Asynchronous job accepted for background execution (e.g., data export, batch sync)."),
        (204, "No Content", "Action successfully completed with empty response payload (e.g., token revocation)."),
        (304, "Not Modified", "Resource has not changed since ETag specified in If-None-Match header; body empty."),
        (400, "Bad Request", "Malformed syntax, invalid JSON, or schema validation constraint failure."),
        (401, "Unauthorized", "Missing, invalid, expired, or untrusted Bearer JWT authentication token."),
        (403, "Forbidden", "Authenticated caller lacks RBAC permission or fails ABAC facility/shift scoping guard."),
        (404, "Not Found", "Target resource identifier does not exist or has been tombstoned."),
        (405, "Method Not Allowed", "HTTP verb not supported for the requested resource endpoint."),
        (406, "Not Acceptable", "Server cannot produce media type requested in Accept header."),
        (409, "Conflict", "Business rule conflict, duplicate key, or concurrent mutation collision."),
        (410, "Gone", "Resource or pre-signed download link previously existed but has expired permanently."),
        (412, "Precondition Failed", "If-Match ETag header does not match current database row version."),
        (413, "Payload Too Large", "Uploaded payload exceeds gateway 10MB limit."),
        (415, "Unsupported Media Type", "Content-Type header is not application/json or application/json+fhir."),
        (422, "Unprocessable Entity", "Syntactically valid JSON but semantic domain rule violation."),
        (429, "Too Many Requests", "Rate limit quota exceeded; Retry-After header indicates required delay."),
        (500, "Internal Server Error", "Uncaught server error; correlation ID logged to WORM audit trail."),
        (502, "Bad Gateway", "Upstream dependency (CDAC SMS, NHA ABDM Gateway) returned invalid response."),
        (503, "Service Unavailable", "Circuit breaker tripped or scheduled maintenance window active."),
        (504, "Gateway Timeout", "Upstream microservice or database transaction exceeded deadline.")
    ]

    lines.append("### 3.1 Exhaustive Status Codes Specification")
    lines.append("The 22 recognized HTTP status codes are defined below:")
    lines.append("")
    lines.append("| Status Code | RFC Name | Operational Meaning & Platform Usage | Error Envelope Emitted |")
    lines.append("| :--- | :--- | :--- | :--- |")
    for code, name, desc in status_codes_catalog:
        err_env = "No" if code < 400 else "**Yes (SCHEMA-API-003)**"
        lines.append(f"| `HTTP {code}` | `{name}` | {desc} | {err_env} |")
    lines.append("")

    # 4. Standard HTTP Headers
    lines.append("## 4. Standard Ingress & Egress HTTP Headers")
    lines.append("")
    lines.append("All requests and responses must exchange the following standardized headers:")
    lines.append("")
    lines.append("| Header Name | Category | Direction | Requirement | Description & Format |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    lines.append("| `X-Correlation-ID` | Tracing | Both | **Mandatory** | UUIDv7 correlating request across edge and microservices. |")
    lines.append("| `X-Request-ID` | Tracing | Both | **Mandatory** | Unique UUIDv7 per HTTP hop. |")
    lines.append("| `X-Idempotency-Key` | Reliability | Ingress | **Mandatory for POST/PUT** | UUIDv7 deduplication key cached for 24 hours. |")
    lines.append("| `X-Facility-ID` | Security | Ingress | **Mandatory** | UUIDv7 of Namma Clinic facility where terminal is operating. |")
    lines.append("| `Authorization` | Security | Ingress | **Mandatory (except public)** | `Bearer <JWT>` containing staff claims. |")
    lines.append("| `If-Match` | Concurrency | Ingress | Mandatory for PUT/PATCH | Cryptographic ETag hash for optimistic concurrency. |")
    lines.append("| `ETag` | Concurrency | Egress | Present on GET/PUT | SHA-256 hash of resource representation. |")
    lines.append("| `RateLimit-Limit` | Rate Limiting | Egress | Present on all | Maximum allowed requests in current window. |")
    lines.append("| `RateLimit-Remaining` | Rate Limiting | Egress | Present on all | Remaining request quota in current window. |")
    lines.append("| `RateLimit-Reset` | Rate Limiting | Egress | Present on all | UTC seconds until quota window resets. |")
    lines.append("| `Retry-After` | Rate Limiting | Egress | Present on 429/503 | Seconds caller must back off before retry. |")
    lines.append("")

    # 5. Serialization, Timestamps & UUIDv7
    lines.append("## 5. JSON Serialization, Identifier & Timestamp Formats")
    lines.append("")
    lines.append("### 5.1 JSON Attribute Naming Conventions")
    lines.append("- **camelCase in JSON:** All JSON payload keys must be formatted in strict `camelCase` (e.g., `firstName`, `prescribedDosage`, `contactNumber`).")
    lines.append("- **snake_case in Database:** Relational database columns remain `snake_case` (e.g., `first_name`); ORM serialization layers map between snake_case and camelCase deterministically.")
    lines.append("- **Null Semantics:** Explicit `null` indicates cleared value; absent keys in PATCH indicate untouched fields.")
    lines.append("")
    lines.append("### 5.2 Time-Ordered UUIDv7 Standard")
    lines.append("Every entity generated across the platform utilizes time-ordered **UUIDv7** (RFC 9562 draft standard). This guarantees:")
    lines.append("1. **Monotonic Ordering:** IDs sort chronologically based on millisecond timestamp prefix, preventing B-tree index fragmentation in PostgreSQL and SQLite.")
    lines.append("2. **Autonomous Edge Generation:** Clinic tablets can generate globally unique primary keys offline without colliding with central cloud records.")
    lines.append("3. **Cryptographic Randomness:** 74 bits of cryptographically secure pseudo-random entropy prevent key guessing or enumeration attacks.")
    lines.append("")

    # 6. Pagination, Filtering, Sorting & Expansion
    lines.append("## 6. Query Parameters: Pagination, Filtering, Sorting & Expansion")
    lines.append("")
    lines.append("### 6.1 Cursor-Based Pagination Standards")
    lines.append("To prevent database offset scanning penalties on million-row tables (`patients`, `audit_events`), cursor pagination is enforced:")
    lines.append("```http")
    lines.append("# DOCUMENTATION-ONLY EXAMPLE")
    lines.append("GET /api/v1/patients?limit=25&cursor=ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSFV6STFOaUlzSW5SNWNDSTZJazFsYkd4bFlXNWxJanAwY25WbGMzUWlPaUowWlhOMElpd2ljbVZ6ZFdsdUlqcDdJblJsZUhRaU9pSjBhSFJzY3lJc0luQjFiaUk2TWpB")
    lines.append("Host: api.nammaclinic.bbmp.gov.in")
    lines.append("Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...")
    lines.append("X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001")
    lines.append("```")
    lines.append("")
    lines.append("### 6.2 Filtering Grammar")
    lines.append("Query filters utilize bracket notation matching indexed attributes:")
    lines.append("- `filter[gender]=FEMALE`")
    lines.append("- `filter[wardNumber]=142`")
    lines.append("- `filter[createdAt][gte]=2026-09-01T00:00:00Z`")
    lines.append("- `filter[status][in]=ACTIVE,IN_PROGRESS`")
    lines.append("")
    lines.append("### 6.3 Sorting Standards")
    lines.append("Sorting is specified via the `sort` parameter with comma separation; prefix `-` indicates descending order:")
    lines.append("- `sort=-createdAt,lastName`")
    lines.append("")

    # 7. Standard Envelopes & Concrete Examples
    lines.append("## 7. Standard API Response Envelopes & Detailed Schemas")
    lines.append("")
    lines.append("Every response emitted across the 341 endpoints wraps data in one of three standardized top-level JSON envelopes:")
    lines.append("")
    lines.append("### 7.1 Single-Resource Response Envelope (`SCHEMA-API-001`)")
    lines.append("```json")
    lines.append("// DOCUMENTATION-ONLY EXAMPLE")
    lines.append("{")
    lines.append("  \"data\": {")
    lines.append("    \"id\": \"018e3a20-0001-7000-8000-000000000001\",")
    lines.append("    \"type\": \"patients\",")
    lines.append("    \"attributes\": {")
    lines.append("      \"uhid\": \"NC-BLR-2026-00000042\",")
    lines.append("      \"firstName\": \"Sunita\",")
    lines.append("      \"lastName\": \"Gowda\",")
    lines.append("      \"gender\": \"FEMALE\",")
    lines.append("      \"dateOfBirth\": \"1984-06-15\",")
    lines.append("      \"primaryPhone\": \"XXXXXX8921\",")
    lines.append("      \"bbmpWardNumber\": 142,")
    lines.append("      \"abhaLinked\": true,")
    lines.append("      \"createdAt\": \"2026-09-01T09:15:30.124Z\"")
    lines.append("    },")
    lines.append("    \"relationships\": {")
    lines.append("      \"facility\": {")
    lines.append("        \"data\": { \"id\": \"018e3a20-0008-7000-8000-000000000001\", \"type\": \"facilities\" }")
    lines.append("      }")
    lines.append("    }")
    lines.append("  },")
    lines.append("  \"meta\": {")
    lines.append("    \"correlationId\": \"018e3a20-8000-7000-8000-000000000001\",")
    lines.append("    \"executionDurationMs\": 24,")
    lines.append("    \"serverNode\": \"cloud-app-az1-pod4\",")
    lines.append("    \"timestamp\": \"2026-09-01T09:15:30.148Z\"")
    lines.append("  },")
    lines.append("  \"links\": {")
    lines.append("    \"self\": \"https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001\"")
    lines.append("  }")
    lines.append("}")
    lines.append("```")
    lines.append("")

    lines.append("### 7.2 Standard Error Response Envelope (`SCHEMA-API-003`)")
    lines.append("```json")
    lines.append("// DOCUMENTATION-ONLY EXAMPLE")
    lines.append("{")
    lines.append("  \"error\": {")
    lines.append("    \"code\": \"ERR-PATIENT-002\",")
    lines.append("    \"message\": \"High-confidence duplicate citizen detected (matching mobile phone and phonetic name).\",")
    lines.append("    \"category\": \"Conflict\",")
    lines.append("    \"correlationId\": \"018e3a20-8000-7000-8000-000000000001\",")
    lines.append("    \"timestamp\": \"2026-09-01T09:15:30.150Z\",")
    lines.append("    \"retryable\": false,")
    lines.append("    \"details\": [")
    lines.append("      {")
    lines.append("        \"field\": \"data.attributes.primaryPhone\",")
    lines.append("        \"rule\": \"unique_constraint_violation\",")
    lines.append("        \"rejectedValue\": \"XXXXXX8921\",")
    lines.append("        \"message\": \"Mobile number matches existing patient profile UHID NC-BLR-2024-00008129.\"")
    lines.append("      }")
    lines.append("    ]")
    lines.append("  }")
    lines.append("}")
    lines.append("```")
    lines.append("")

    # 8. Complete Schema Catalog Matrix
    lines.append("## 8. Authoritative API Schema Catalog (68 Schemas)")
    lines.append("")
    lines.append("The 68 canonical schemas registered for the platform are tabulated below:")
    lines.append("")
    lines.append("| Schema ID | Schema Name | Functional Category | Field Count | Authoritative Description |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    for s in API_SCHEMAS:
        lines.append(f"| **{s['id']}** | `{s['name']}` | `{s['category']}` | {len(s['fields'])} fields | {s['description']} |")
    lines.append("")

    # 9. Exhaustive Schema Deep-Dives for ALL 68 Schemas
    lines.append("## 9. Exhaustive Field-Level Schema Specifications (All 68 Schemas)")
    lines.append("")
    lines.append("Every registered schema is cataloged with complete typing, nullability, required status, and domain validation rules:")
    lines.append("")
    for s in API_SCHEMAS:
        lines.append(f"### 9.{s['id']} Schema Specification: `{s['name']}`")
        lines.append(f"- **Schema Identifier:** `{s['id']}`")
        lines.append(f"- **Domain Category:** `{s['category']}`")
        lines.append(f"- **Functional Scope:** {s['description']}")
        lines.append("")
        lines.append("| Field Name | Data Type | Required | Nullable | Field Description & Validation Constraints |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for f in s["fields"]:
            req_str = "**Yes**" if f["required"] else "No"
            null_str = "Yes" if f["nullable"] else "No"
            lines.append(f"| `{f['name']}` | `{f['type']}` | {req_str} | {null_str} | {f['description']} |")
        lines.append("")
        lines.append("#### Example JSON Payload")
        lines.append("```json")
        lines.append("// DOCUMENTATION-ONLY EXAMPLE")
        lines.append("{")
        for j, f in enumerate(s["fields"]):
            val = "\"018e3a20-0001-7000-8000-000000000001\"" if "id" in f["name"].lower() else ("\"sample_value\"" if f["type"] == "string" else ("100" if f["type"] == "integer" else ("true" if f["type"] == "boolean" else "[]")))
            comma = "," if j < len(s["fields"]) - 1 else ""
            lines.append(f"  \"{f['name']}\": {val}{comma}")
        lines.append("}")
        lines.append("```")
        lines.append("")

    # 10. Concrete HTTP Request/Response Exchange Examples for Every Domain
    lines.append("## 10. Concrete HTTP Request and Response Wire Examples")
    lines.append("")
    lines.append("The following subsections provide concrete HTTP wire-level exchanges for major functional domains:")
    lines.append("")
    domains_sample = [
        ("Auth", "POST /api/v1/auth/login", "Staff Login", "{\"username\": \"DOC-1024\", \"password\": \"Secret@2026\", \"facilityId\": \"018e3a20-0008-7000-8000-000000000001\", \"deviceFingerprint\": \"tab-blr-042\"}", "{\"accessToken\": \"eyJhbGciOiJSUzI1Ni...\", \"tokenType\": \"Bearer\", \"expiresIn\": 900}"),
        ("Patient", "POST /api/v1/patients", "Patient Registration", "{\"firstName\": \"Sunita\", \"primaryPhone\": \"9876543210\", \"gender\": \"FEMALE\", \"bbmpWardNumber\": 142}", "{\"id\": \"018e3a20-0001-7000-8000-000000000001\", \"uhid\": \"NC-BLR-2026-00000042\"}"),
        ("Visit", "POST /api/v1/visits", "Queue Token Creation", "{\"patientId\": \"018e3a20-0001-7000-8000-000000000001\", \"visitType\": \"GENERAL_OPD\", \"priorityCategory\": \"ROUTINE\"}", "{\"visitId\": \"018e3a20-0018-7000-8000-000000000001\", \"tokenNumber\": \"A-042\", \"sequenceNumber\": 42}"),
        ("Triage", "POST /api/v1/triage", "Record Vitals", "{\"visitId\": \"018e3a20-0018-7000-8000-000000000001\", \"systolicBp\": 120, \"diastolicBp\": 80, \"pulseRate\": 72, \"temperatureFahrenheit\": 98.4, \"spo2Percent\": 99.0, \"acuityColor\": \"GREEN\"}", "{\"triageId\": \"018e3a20-0020-7000-8000-000000000001\", \"mewsScore\": 0, \"acuityCategory\": \"GREEN\"}"),
        ("Consultation", "POST /api/v1/consultations", "Finalize Notes", "{\"visitId\": \"018e3a20-0018-7000-8000-000000000001\", \"chiefComplaints\": [{\"symptom\": \"Fever\", \"durationDays\": 3}], \"provisionalDiagnoses\": [{\"icd10Code\": \"A90\", \"icd10Display\": \"Dengue fever\"}]}", "{\"encounterId\": \"018e3a20-0023-7000-8000-000000000001\", \"status\": \"FINALIZED\"}"),
        ("Prescription", "POST /api/v1/prescriptions", "Issue E-Prescription", "{\"encounterId\": \"018e3a20-0023-7000-8000-000000000001\", \"items\": [{\"drugId\": \"018e3a20-0032-7000-8000-000000000001\", \"dosageForm\": \"TABLET\", \"strength\": \"500mg\", \"frequency\": \"THRICE_DAILY\", \"durationDays\": 5, \"quantityPrescribed\": 15}]}", "{\"prescriptionId\": \"018e3a20-0026-7000-8000-000000000001\", \"status\": \"SIGNED\"}"),
        ("Pharmacy", "POST /api/v1/pharmacy/dispense", "Dispense Medicines", "{\"prescriptionId\": \"018e3a20-0026-7000-8000-000000000001\", \"dispensedItems\": [{\"batchId\": \"018e3a20-0034-7000-8000-000000000001\", \"quantityDispensed\": 15}]}", "{\"dispensationId\": \"018e3a20-0036-7000-8000-000000000001\", \"status\": \"COMPLETED\"}"),
        ("Inventory", "POST /api/v1/inventory/receipts", "Receive Stock", "{\"invoiceNumber\": \"DEPOT-INV-891\", \"receivedBatches\": [{\"drugId\": \"018e3a20-0032-7000-8000-000000000001\", \"batchNumber\": \"PCM-26-A\", \"expiryDate\": \"2028-12-31\", \"quantityReceived\": 1000}]}", "{\"receiptId\": \"018e3a20-0038-7000-8000-000000000001\", \"status\": \"POSTED\"}"),
        ("Lab", "POST /api/v1/lab/orders", "Order Diagnostic Test", "{\"encounterId\": \"018e3a20-0023-7000-8000-000000000001\", \"testIds\": [\"LOINC-4544-3\"], \"clinicalIndication\": \"Suspected dengue fever\", \"isUrgent\": true}", "{\"orderId\": \"018e3a20-0028-7000-8000-000000000001\", \"status\": \"PENDING_COLLECTION\"}"),
        ("Referral", "POST /api/v1/referrals", "Refer Patient", "{\"encounterId\": \"018e3a20-0023-7000-8000-000000000001\", \"destinationHospitalType\": \"BBMP_GENERAL_HOSPITAL\", \"urgencyLevel\": \"EMERGENCY_108\", \"referralSpecialty\": \"CARDIOLOGY\"}", "{\"referralId\": \"018e3a20-0043-7000-8000-000000000001\", \"status\": \"DISPATCHED\"}"),
        ("Notification", "POST /api/v1/notifications/send", "Send SMS Reminder", "{\"patientId\": \"018e3a20-0001-7000-8000-000000000001\", \"channel\": \"SMS\", \"templateId\": \"DLT-KN-APPT-01\", \"preferredLanguage\": \"kn\"}", "{\"messageId\": \"018e3a20-0047-7000-8000-000000000001\", \"status\": \"QUEUED\"}"),
        ("Analytics", "GET /api/v1/analytics/kpi/daily", "Fetch Daily Clinic KPIs", "", "{\"facilityId\": \"018e3a20-0008-7000-8000-000000000001\", \"totalRegisteredOpd\": 148, \"avgConsultationTimeSeconds\": 380, \"redTriageCount\": 2}"),
        ("Audit", "GET /api/v1/audit/events", "Query WORM Audit Log", "", "{\"verifiedBlockCount\": 45000, \"tamperDetected\": false}"),
        ("ABDM", "POST /api/v1/abdm/abha/verify-otp", "Verify ABHA OTP", "{\"identifier\": \"14-1234-5678-9012\", \"otp\": \"123456\"}", "{\"abhaNumber\": \"14-1234-5678-9012\", \"verificationStatus\": \"VERIFIED\"}"),
        ("Portability", "POST /api/v1/portability/jobs", "Request FHIR Export", "{\"patientId\": \"018e3a20-0001-7000-8000-000000000001\", \"exportFormat\": \"FHIR_JSON\"}", "{\"jobId\": \"018e3a20-0052-7000-8000-000000000001\", \"status\": \"PROCESSING\"}"),
        ("System", "POST /api/v1/system/sync/batch", "Replay Edge Mutation Log", "{\"facilityId\": \"018e3a20-0008-7000-8000-000000000001\", \"mutations\": []}", "{\"reconciledMutations\": 18, \"conflictCount\": 0}")
    ]

    for dname, route, title, req_b, resp_b in domains_sample:
        lines.append(f"### 10.{dname} Domain Wire Example: {title} (`{route}`)")
        lines.append("```http")
        lines.append("# DOCUMENTATION-ONLY EXAMPLE")
        lines.append(f"{route} HTTP/1.1")
        lines.append("Host: api.nammaclinic.bbmp.gov.in")
        lines.append("Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...")
        lines.append("X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001")
        lines.append("X-Facility-ID: 018e3a20-0008-7000-8000-000000000001")
        lines.append("Content-Type: application/json")
        lines.append("")
        if req_b:
            lines.append(req_b)
            lines.append("")
        lines.append("HTTP/1.1 200 OK")
        lines.append("Content-Type: application/json")
        lines.append("X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001")
        lines.append(f"ETag: W/\"sha256-{dname.lower()}-hash\"")
        lines.append("")
        lines.append(resp_b)
        lines.append("```")
        lines.append("")

    # 11. Field-Level Validation Regular Expressions Catalog
    lines.append("## 11. Authoritative Validation Regular Expressions & Masking Catalog")
    lines.append("")
    lines.append("All ingress request attributes enforce strict client- and gateway-level regular expression validation:")
    lines.append("")
    validation_regexes = [
        ("Mobile Phone Number", "primaryPhone", r"^[6-9]\d{9}$", "10-digit Indian national mobile number starting with 6, 7, 8, or 9", "XXXXXX8921"),
        ("Municipal UHID", "uhid", r"^NC-BLR-\d{4}-\d{8}$", "Namma Clinic Unique Health Identifier format NC-BLR-YYYY-XXXXXXXX", "NC-BLR-2026-00000042"),
        ("ABHA Number", "abhaNumber", r"^\d{2}-\d{4}-\d{4}-\d{4}$", "14-digit national Ayushman Bharat Health Account number", "14-1234-5678-9012"),
        ("ABHA Address", "abhaAddress", r"^[a-zA-Z0-9._]{4,32}@[a-zA-Z0-9]{3,16}$", "ABHA PHR virtual address handle (citizen@abdm)", "sunita.gowda@abdm"),
        ("Postal PIN Code", "postalPincode", r"^560\d{3}$", "Bengaluru postal delivery zone pincode (560001 to 560110)", "560042"),
        ("UUIDv7 Identifier", "id, correlationId", r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", "RFC 9562 draft time-ordered 128-bit UUIDv7 format", "018e3a20-0001-7000-8000-000000000001"),
        ("WHO ICD-10 Code", "icd10Code", r"^[A-Z]\d{2}(\.\d{1,2})?$", "World Health Organization International Classification of Diseases 10th Revision", "E11.9"),
        ("LOINC Code", "loincCode", r"^\d{3,5}-\d$", "Logical Observation Identifiers Names and Codes laboratory test identifier", "4544-3"),
        ("Password Complexity", "password", r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,64}$", "12-64 chars with lowercase, uppercase, number, and special symbol", "Redacted"),
        ("Date Format (ISO)", "dateOfBirth, followUpDate", r"^\d{4}-\d{2}-\d{2}$", "ISO-8601 calendar date YYYY-MM-DD", "1984-06-15"),
        ("Timestamp (ISO UTC)", "createdAt, timestamp", r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$", "ISO-8601 UTC timestamp with optional millisecond precision", "2026-09-01T09:15:30.124Z")
    ]
    lines.append("| Identifier / Attribute | JSON Field Path | Regex Pattern | Format Description | Masked Display Example |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    for name, fpath, pat, fdesc, mask_ex in validation_regexes:
        lines.append(f"| **{name}** | `{fpath}` | `{pat}` | {fdesc} | `{mask_ex}` |")
    lines.append("")

    # 12. Query Operators Reference Table
    lines.append("## 12. Filtering & Comparison Operators Reference")
    lines.append("")
    lines.append("The API gateway supports 14 standard query filter operators:")
    lines.append("")
    operators_list = [
        ("eq", "filter[status][eq]=ACTIVE", "Equal to comparison", "SELECT * FROM t WHERE status = 'ACTIVE'"),
        ("ne", "filter[status][ne]=CANCELLED", "Not equal to comparison", "SELECT * FROM t WHERE status != 'CANCELLED'"),
        ("gt", "filter[age][gt]=60", "Greater than strictly", "SELECT * FROM t WHERE age > 60"),
        ("gte", "filter[createdAt][gte]=2026-09-01T00:00:00Z", "Greater than or equal to", "SELECT * FROM t WHERE created_at >= '2026-09-01 00:00:00'"),
        ("lt", "filter[stockQuantity][lt]=10", "Less than strictly (low stock warning)", "SELECT * FROM t WHERE stock_quantity < 10"),
        ("lte", "filter[temperature][lte]=98.6", "Less than or equal to", "SELECT * FROM t WHERE temperature <= 98.6"),
        ("in", "filter[priorityCategory][in]=ROUTINE,MATERNAL", "In discrete set of values", "SELECT * FROM t WHERE priority_category IN ('ROUTINE', 'MATERNAL')"),
        ("nin", "filter[status][nin]=CLOSED,VOID", "Not in discrete set of values", "SELECT * FROM t WHERE status NOT IN ('CLOSED', 'VOID')"),
        ("like", "filter[firstName][like]=Sunit%", "Prefix string search", "SELECT * FROM t WHERE first_name LIKE 'Sunit%'"),
        ("ilike", "filter[lastName][ilike]=%gowda%", "Case-insensitive substring search", "SELECT * FROM t WHERE last_name ILIKE '%gowda%'"),
        ("is_null", "filter[closedAt][is_null]=true", "Checks for SQL NULL value", "SELECT * FROM t WHERE closed_at IS NULL"),
        ("not_null", "filter[abhaNumber][not_null]=true", "Checks for populated non-NULL value", "SELECT * FROM t WHERE abha_number IS NOT NULL"),
        ("between", "filter[createdAt][between]=2026-09-01,2026-09-07", "Closed range inclusion", "SELECT * FROM t WHERE created_at BETWEEN '2026-09-01' AND '2026-09-07'"),
        ("contains", "filter[tags][contains]=NCD_HYPERTENSION", "JSONB array element containment", "SELECT * FROM t WHERE tags @> '[\"NCD_HYPERTENSION\"]'")
    ]
    lines.append("| Operator | Query Parameter Syntax | Semantic Meaning | Relational SQL Translation |")
    lines.append("| :--- | :--- | :--- | :--- |")
    for op, syn, sem, sql in operators_list:
        lines.append(f"| `{op}` | `{syn}` | {sem} | `{sql}` |")
    lines.append("")

    # 13. Idempotency State Machine
    lines.append("## 13. Idempotency Key Processing Lifecycle & State Machine")
    lines.append("")
    lines.append("To prevent duplicate patient registrations or double-dispensing during network hiccups, `X-Idempotency-Key` headers are processed via Redis distributed locks:")
    lines.append("")
    lines.append("```mermaid")
    lines.append("stateDiagram-v2")
    lines.append("    [*] --> CheckRedis: Ingress POST with X-Idempotency-Key")
    lines.append("    CheckRedis --> KeyNotFound: Key not in Redis")
    lines.append("    CheckRedis --> KeyProcessing: Key state = IN_PROGRESS")
    lines.append("    CheckRedis --> KeyCompleted: Key state = COMPLETED")
    lines.append("    KeyNotFound --> AcquireLock: SETNX key IN_PROGRESS (TTL 60s)")
    lines.append("    AcquireLock --> ExecuteHandler: Execute Transactional Handler")
    lines.append("    ExecuteHandler --> SaveResponse: Store Response Body & Status (TTL 86400s)")
    lines.append("    SaveResponse --> DeliverClient: Deliver Fresh Response to Client")
    lines.append("    KeyProcessing --> Return409: Return HTTP 409 Conflict (ERR-SYS-004)")
    lines.append("    KeyCompleted --> VerifyChecksum: Compare Request Body Hash")
    lines.append("    VerifyChecksum --> ReplayResponse: Hash Matches: Replay Cached Response")
    lines.append("    VerifyChecksum --> MismatchError: Hash Differs: Return HTTP 409 Payload Mismatch")
    lines.append("    DeliverClient --> [*]")
    lines.append("    Return409 --> [*]")
    lines.append("    ReplayResponse --> [*]")
    lines.append("    MismatchError --> [*]")
    lines.append("```")
    lines.append("")

    # 14. Relationship Expansion Matrix
    lines.append("## 14. Relationship Expansion & Sub-Resource Embedding Matrix")
    lines.append("")
    lines.append("To minimize HTTP round-trips from frontline tablet clients, the API gateway supports compound document expansion via the `expand` parameter (maximum 2 levels deep):")
    lines.append("")
    expansion_matrix = [
        ("patients", "contacts,addresses,identifiers", "Encounter registration desk fetches full contact & national IDs in single query"),
        ("patients", "encounters,consents", "Clinical consultation view expands active encounter history and valid consent directives"),
        ("visits", "patient,triage,room", "Queue orchestration displays patient name, MEWS acuity color, and doctor room assignment"),
        ("clinical_encounters", "notes,diagnoses,vitals", "SOAP progress note review renders clinician notes, ICD-10 codes, and triage readings"),
        ("prescriptions", "items,doctor,facility", "Pharmacy dispensing screen expands prescribed drug line items and authorizing doctor signature"),
        ("dispensations", "items.batch,prescription", "Stock audit inspects dispensed items with allocated batch numbers and parent prescription"),
        ("lab_orders", "items.results,encounter", "Diagnostic lab review displays test orders, specimen barcodes, and recorded results"),
        ("referrals", "encounter.diagnoses,counter_notes", "Secondary hospital intake expands referral reason, primary diagnosis, and return notes"),
        ("clinic_stock", "batch,drug", "Pharmacy inventory dashboard displays on-hand balance, batch expiry date, and formulary name"),
        ("drug_indents", "items.drug,approver", "Central warehouse fulfillment view expands requested medicines and medical superintendent approval"),
        ("cold_chain_devices", "telemetry,facility", "IoT vaccine cold-chain dashboard displays device model, clinic ward, and recent temperature log"),
        ("ncd_episodes", "patient,schedules", "Chronic disease tracking dashboard expands patient profile and upcoming follow-up appointments")
    ]
    lines.append("| Primary Resource | Supported Expansion Path (`expand=...`) | Clinical / Operational Use Case |")
    lines.append("| :--- | :--- | :--- |")
    for res, exp, ucase in expansion_matrix:
        lines.append(f"| `{res}` | `{exp}` | {ucase} |")
    lines.append("")

    # 15. Standard HTTP Egress Caching & Compression Standards
    lines.append("## 15. HTTP Caching, Compression & Gateway Negotiation Standards")
    lines.append("")
    lines.append("The platform enforces deterministic caching headers based on data classification and mutability:")
    lines.append("")
    caching_policies = [
        ("PUBLIC Reference Data (Formulary, Wards)", "Cache-Control: public, max-age=86400, stale-while-revalidate=3600", "ETag + Brotli/Gzip", "CDN & Browser Cache (24 hours)"),
        ("CONFIDENTIAL Clinical Records (Encounters, Vitals)", "Cache-Control: private, no-cache, no-store, must-revalidate", "ETag (Conditional 304 Only)", "Zero Local Shared Cache; In-Memory Only"),
        ("RESTRICTED PII / Identifiers (Patients, Demographics)", "Cache-Control: private, no-store, max-age=0, s-maxage=0", "None (Direct SSL)", "Encrypted Workstation Session Memory Only"),
        ("HIGHLY-RESTRICTED Audit & Security Secrets", "Cache-Control: no-store, no-cache, private", "None", "Strictly Ephemeral (Zero Cache)"),
        ("System Configuration & Feature Flags", "Cache-Control: public, max-age=300, stale-if-error=86400", "ETag + Gzip", "Edge Gateway Cache (5 minutes)")
    ]
    lines.append("| Data Classification Tier | Mandatory Cache-Control Header | Compression & ETag Policy | Storage Scope |")
    lines.append("| :--- | :--- | :--- | :--- |")
    for tier, cc, comp, stor in caching_policies:
        lines.append(f"| **{tier}** | `{cc}` | `{comp}` | {stor} |")
    lines.append("")

    # 16. BDD Conventions Acceptance Criteria
    lines.append("## 16. API Conventions Acceptance Criteria (BDD)")
    lines.append("")
    bdd_conv1 = make_bdd_scenario(
        "Enforce Standard Error Envelope on Validation Failure",
        ["an authenticated registration user", "transmitting a patient creation request missing mandatory first_name"],
        "the client submits the payload to /api/v1/patients",
        ["the API gateway rejects the request with HTTP 400 Bad Request", "returns the standard error envelope matching SCHEMA-API-003", "contains error code 'ERR-SYS-001' or 'ERR-PATIENT-011'", "details array points to field 'data.attributes.firstName'", "correlation ID matches the X-Correlation-ID response header"]
    )
    lines.extend(bdd_conv1)
    lines.append("")

    bdd_conv2 = make_bdd_scenario(
        "Cursor Pagination Traversal and Limit Enforcement",
        ["an authenticated clinical staff member", "querying /api/v1/patients with limit=25"],
        "the client requests the first page of patients",
        ["the API returns HTTP 200 OK with exactly 25 patient items", "the pagination metadata includes an opaque next_cursor string", "has_more is true if additional records exist", "requesting with the next_cursor returns the next deterministic partition of records"]
    )
    lines.extend(bdd_conv2)
    lines.append("")

    bdd_conv3 = make_bdd_scenario(
        "Optimistic Concurrency Control via If-Match ETag Header",
        ["an authenticated clinician with stale patient data ETag W/\"old-hash\"", "another clinician has concurrently updated the patient address"],
        "the clinician submits a PUT /api/v1/patients/{id} with If-Match: W/\"old-hash\"",
        ["the database detects an ETag revision mismatch", "the API gateway rejects the mutation with HTTP 412 Precondition Failed", "returns error code 'ERR-SYS-005'", "the client workstation prompts the clinician to reload the latest changes"]
    )
    lines.extend(bdd_conv3)
    lines.append("")

    bdd_conv4 = make_bdd_scenario(
        "Idempotent Replay of Mutation Request with Identical Key",
        ["a client workstation that experienced a network timeout during POST /api/v1/prescriptions", "the server successfully processed the original prescription with X-Idempotency-Key '018e3a20-0026-7000-8000-000000000001'"],
        "the client resubmits the identical prescription payload with the same idempotency key",
        ["the API gateway detects the completed transaction key in Redis cache", "verifies that the request payload SHA-256 hash matches the original request", "replays the cached HTTP 201 Created response without re-executing database inserts", "includes the header 'X-Cache-Lookup: IDEMPOTENT-HIT'"]
    )
    lines.extend(bdd_conv4)
    lines.append("")

    content = "\n".join(lines)
    return write_api_doc("02-api-conventions.md", content)

if __name__ == "__main__":
    stats = generate_doc()
    print("Done 02-api-conventions.md:", stats)
