# 🔌 API Specification: Point-of-Care Laboratory & Rapid Diagnostic API Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-12 | **Status:** Authoritative Baseline | **Date:** September 2026
> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Standard Framework:** RFC 7231 (HTTP/1.1), JSON:API v1.1, DPDP Act 2023, ABDM Interoperability Standards
> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.

---

## 1. Executive Summary & Domain Scope

The **Point-of-Care Laboratory & Rapid Diagnostic API Specification** defines the authoritative, implementation-ready contracts for the `Lab` subsystem across all 183 Namma Clinic primary healthcare centers in Greater Bengaluru. This domain operates under the supervisory jurisdiction of `ROLE-018 (Laboratory Technician)` and fulfills the core mission: **Govern point-of-care rapid test requisitions (dengue, malaria, glucose, hemoglobin, urine routine), specimen accessioning, barcode tracking, Panic value alerts, and doctor notification.**

All 23 endpoints specified in this document adhere strictly to uniform JSON:API response envelopes, time-ordered UUIDv7 identifiers, ISO-8601 UTC timestamps, optimistic concurrency control via ETags, and automated audit logging.

## 2. Operational Architecture & Relational Mapping

The following table maps the domain's operational context to architectural containers, components, database tables, and default role entitlements:

| Dimension | Specification Detail |
| :--- | :--- |
| **Functional Domain** | `Lab` (Code: `LAB`) |
| **Authoritative Endpoints** | 23 Active Endpoints (`API-LAB-001` to `API-LAB-023`) |
| **Primary Architecture Container** | `ARCH-CONT-010` |
| **Assigned Component** | `ARCH-COMP-028` |
| **Primary Database Tables** | `lab_orders, lab_order_items, lab_results` |
| **Lead Role Entitlement** | `ROLE-018 (Laboratory Technician)` |
| **Default Rate Limiting** | `60 req/min per User` |
| **Offline Edge Support** | `Edge Local Queue with Delta Sync` |

## 3. Domain Operational State Machine

The operational state transitions governing entities within this domain are modeled below:

```mermaid
stateDiagram-v2
    [*] --> OrderPlaced: Doctor Orders Diagnostic Investigation
    OrderPlaced --> SpecimenCollected: Phlebotomy Sample Collected & Barcoded
    SpecimenCollected --> SampleRejected: Hemolysis / Clotted (Recollect)
    SpecimenCollected --> Analyzing: Rapid POC Analyzer Running
    Analyzing --> ResultEntered: Technician Inputs Quantitative Result
    ResultEntered --> NormalReport: Within Reference Range
    ResultEntered --> PanicAlertTriggered: Exceeds Critical Biological Limit
    PanicAlertTriggered --> DoctorNotified: Direct Pager / Alert Sent
    NormalReport --> Finalized: Report Signed & Linked to EMR
    Finalized --> [*]
```

## 4. End-to-End Operational Data Flow

The sequence diagram below illustrates the end-to-end operational flow between frontline clinic staff, edge workstations, the central API gateway, and backing data stores:

```mermaid
sequenceDiagram
    autonumber
    participant Tech as Lab Technician
    participant UI as Lab Tablet
    participant API as Lab Service
    participant Alert as Panic Alert Engine
    participant Doc as Attending Clinician
    Tech->>UI: Enter RBS: 450 mg/dL (Severe Hyperglycemia)
    UI->>API: POST /api/v1/lab/results
    API->>Alert: Evaluate Panic Value Threshold (>400 mg/dL)
    Alert-->>Doc: Immediate Audio/Visual Alert on Screen
    API-->>UI: HTTP 200 OK (Result Stored & Panic Flagged)
```

## 5. Domain Endpoint Inventory Catalog

Complete inventory of all 23 endpoints defined for the `Lab` domain:

| Endpoint ID | Method | URI Route Path | Functional Title | Role Context | Idempotency Standard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API-LAB-001** | `POST` | `/api/v1/lab` | Create New Laboratory Investigation Record | `ROLE-018` | Supported via X-Idempotency-Key |
| **API-LAB-002** | `GET` | `/api/v1/lab/{labId}` | Retrieve Laboratory Investigation Details by ID | `ROLE-018` | Read-Only Idempotent |
| **API-LAB-003** | `GET` | `/api/v1/lab` | List and Filter Laboratory Investigation Records | `ROLE-018` | Read-Only Idempotent |
| **API-LAB-004** | `PUT` | `/api/v1/lab/{labId}` | Update Full Laboratory Investigation Specification | `ROLE-018` | Supported via X-Idempotency-Key |
| **API-LAB-005** | `PATCH` | `/api/v1/lab/{labId}/status` | Update Laboratory Investigation Operational State | `ROLE-018` | Supported via X-Idempotency-Key |
| **API-LAB-006** | `GET` | `/api/v1/lab/{labId}/search` | Search Laboratory Investigation Workflow Operation | `ROLE-018` | Read-Only Idempotent |
| **API-LAB-007** | `GET` | `/api/v1/lab/history` | History Laboratory Investigation Workflow Operation | `ROLE-018` | Read-Only Idempotent |
| **API-LAB-008** | `GET` | `/api/v1/lab/{labId}/audit` | Audit Laboratory Investigation Workflow Operation | `ROLE-018` | Read-Only Idempotent |
| **API-LAB-009** | `POST` | `/api/v1/lab/cancel` | Cancel Laboratory Investigation Workflow Operation | `ROLE-018` | Supported via X-Idempotency-Key |
| **API-LAB-010** | `POST` | `/api/v1/lab/verify` | Verify Laboratory Investigation Workflow Operation | `ROLE-018` | Supported via X-Idempotency-Key |
| **API-LAB-011** | `GET` | `/api/v1/lab/export` | Export Laboratory Investigation Workflow Operation | `ROLE-018` | Read-Only Idempotent |
| **API-LAB-012** | `GET` | `/api/v1/lab/{labId}/metrics` | Metrics Laboratory Investigation Workflow Operation | `ROLE-018` | Read-Only Idempotent |
| **API-LAB-013** | `POST` | `/api/v1/lab/reconcile` | Reconcile Laboratory Investigation Workflow Operation | `ROLE-018` | Supported via X-Idempotency-Key |
| **API-LAB-014** | `POST` | `/api/v1/lab/batch` | Batch Laboratory Investigation Workflow Operation | `ROLE-018` | Supported via X-Idempotency-Key |
| **API-LAB-015** | `GET` | `/api/v1/lab/sync` | Sync Laboratory Investigation Workflow Operation | `ROLE-018` | Read-Only Idempotent |
| **API-LAB-016** | `GET` | `/api/v1/lab/{labId}/alerts` | Alerts Laboratory Investigation Workflow Operation | `ROLE-018` | Read-Only Idempotent |
| **API-LAB-017** | `POST` | `/api/v1/lab/escalate` | Escalate Laboratory Investigation Workflow Operation | `ROLE-018` | Supported via X-Idempotency-Key |
| **API-LAB-018** | `POST` | `/api/v1/lab/approve` | Approve Laboratory Investigation Workflow Operation | `ROLE-018` | Supported via X-Idempotency-Key |
| **API-LAB-019** | `POST` | `/api/v1/lab/reversal` | Reversal Laboratory Investigation Workflow Operation | `ROLE-018` | Supported via X-Idempotency-Key |
| **API-LAB-020** | `GET` | `/api/v1/lab/{labId}/items` | Items Laboratory Investigation Workflow Operation | `ROLE-018` | Read-Only Idempotent |
| **API-LAB-021** | `GET` | `/api/v1/lab/documents` | Documents Laboratory Investigation Workflow Operation | `ROLE-018` | Read-Only Idempotent |
| **API-LAB-022** | `GET` | `/api/v1/lab/{labId}/timeline` | Timeline Laboratory Investigation Workflow Operation | `ROLE-018` | Read-Only Idempotent |
| **API-LAB-023** | `GET` | `/api/v1/lab/stats` | Stats Laboratory Investigation Workflow Operation | `ROLE-018` | Read-Only Idempotent |

## 6. Comprehensive Endpoint Technical Specifications

Exhaustive technical contracts for all 23 endpoints in the `Lab` domain:

### 6.1 `API-LAB-001`: Create New Laboratory Investigation Record

- **API Identifier:** `API-LAB-001`
- **HTTP Route:** `POST /api/v1/lab`
- **Functional Purpose:** Authoritative specification for create new laboratory investigation record within Lab operations.
- **Product Capability:** `CAPABILITY-173` | **Feature Code:** `FEATURE-173`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:post`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-053, SRS-NFR-013` | **Workflow:** `WF-023`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-023`
- **Planned Verification Test Case:** `PLANNED-TEST-API-172`
- **Dependency DAG Edge:** `API-DEP-053`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab:
    post:
      summary: "Create New Laboratory Investigation Record"
      tags:
        - "Lab"
      operationId: "post_api_v1_lab"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/StandardApiResponseEnvelope"
      responses:
        '201':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '409':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X POST \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "X-Idempotency-Key: 018e3a20-9000-7000-8000-000000000001" \
  -H "Content-Type: application/json" \
  -d '{"sampleAttribute": "value"}'
```

#### Request Body Wire Representation
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "facilityId": "018e3a20-0008-7000-8000-000000000001",
  "operation": "Create New Laboratory Investigation Record",
  "domain": "Lab",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-LAB-001"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-001",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-001.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-023` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-172` under simulated offline network conditions.

### 6.2 `API-LAB-002`: Retrieve Laboratory Investigation Details by ID

- **API Identifier:** `API-LAB-002`
- **HTTP Route:** `GET /api/v1/lab/{labId}`
- **Functional Purpose:** Authoritative specification for retrieve laboratory investigation details by id within Lab operations.
- **Product Capability:** `CAPABILITY-174` | **Feature Code:** `FEATURE-174`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:get`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-054, SRS-NFR-014` | **Workflow:** `WF-024`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-024`
- **Planned Verification Test Case:** `PLANNED-TEST-API-173`
- **Dependency DAG Edge:** `API-DEP-054`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/{labId}:
    get:
      summary: "Retrieve Laboratory Investigation Details by ID"
      tags:
        - "Lab"
      operationId: "get_api_v1_lab_labId"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X GET \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/{labId}" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "Accept: application/json"
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-002",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-002.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-024` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-173` under simulated offline network conditions.

### 6.3 `API-LAB-003`: List and Filter Laboratory Investigation Records

- **API Identifier:** `API-LAB-003`
- **HTTP Route:** `GET /api/v1/lab`
- **Functional Purpose:** Authoritative specification for list and filter laboratory investigation records within Lab operations.
- **Product Capability:** `CAPABILITY-175` | **Feature Code:** `FEATURE-175`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:get`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-055, SRS-NFR-015` | **Workflow:** `WF-025`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-025`
- **Planned Verification Test Case:** `PLANNED-TEST-API-174`
- **Dependency DAG Edge:** `API-DEP-055`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab:
    get:
      summary: "List and Filter Laboratory Investigation Records"
      tags:
        - "Lab"
      operationId: "get_api_v1_lab"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardCollectionEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X GET \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "Accept: application/json"
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-003",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-003.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-025` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-174` under simulated offline network conditions.

### 6.4 `API-LAB-004`: Update Full Laboratory Investigation Specification

- **API Identifier:** `API-LAB-004`
- **HTTP Route:** `PUT /api/v1/lab/{labId}`
- **Functional Purpose:** Authoritative specification for update full laboratory investigation specification within Lab operations.
- **Product Capability:** `CAPABILITY-176` | **Feature Code:** `FEATURE-176`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:put`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-056, SRS-NFR-016` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-026`
- **Planned Verification Test Case:** `PLANNED-TEST-API-175`
- **Dependency DAG Edge:** `API-DEP-056`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/{labId}:
    put:
      summary: "Update Full Laboratory Investigation Specification"
      tags:
        - "Lab"
      operationId: "put_api_v1_lab_labId"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/StandardApiResponseEnvelope"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '412':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X PUT \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/{labId}" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "X-Idempotency-Key: 018e3a20-9000-7000-8000-000000000001" \
  -H "Content-Type: application/json" \
  -d '{"sampleAttribute": "value"}'
```

#### Request Body Wire Representation
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "facilityId": "018e3a20-0008-7000-8000-000000000001",
  "operation": "Update Full Laboratory Investigation Specification",
  "domain": "Lab",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-LAB-004"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-004",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-004.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-026` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-175` under simulated offline network conditions.

### 6.5 `API-LAB-005`: Update Laboratory Investigation Operational State

- **API Identifier:** `API-LAB-005`
- **HTTP Route:** `PATCH /api/v1/lab/{labId}/status`
- **Functional Purpose:** Authoritative specification for update laboratory investigation operational state within Lab operations.
- **Product Capability:** `CAPABILITY-177` | **Feature Code:** `FEATURE-177`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:patch`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-057, SRS-NFR-017` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-027`
- **Planned Verification Test Case:** `PLANNED-TEST-API-176`
- **Dependency DAG Edge:** `API-DEP-057`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/{labId}/status:
    patch:
      summary: "Update Laboratory Investigation Operational State"
      tags:
        - "Lab"
      operationId: "patch_api_v1_lab_labId_status"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/StandardApiResponseEnvelope"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X PATCH \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/{labId}/status" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "X-Idempotency-Key: 018e3a20-9000-7000-8000-000000000001" \
  -H "Content-Type: application/json" \
  -d '{"sampleAttribute": "value"}'
```

#### Request Body Wire Representation
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "facilityId": "018e3a20-0008-7000-8000-000000000001",
  "operation": "Update Laboratory Investigation Operational State",
  "domain": "Lab",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-LAB-005"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-005",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-005.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-027` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-176` under simulated offline network conditions.

### 6.6 `API-LAB-006`: Search Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-006`
- **HTTP Route:** `GET /api/v1/lab/{labId}/search`
- **Functional Purpose:** Authoritative specification for search laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-178` | **Feature Code:** `FEATURE-178`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:get`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-058, SRS-NFR-018` | **Workflow:** `WF-003`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-028`
- **Planned Verification Test Case:** `PLANNED-TEST-API-177`
- **Dependency DAG Edge:** `API-DEP-058`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/{labId}/search:
    get:
      summary: "Search Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "get_api_v1_lab_labId_search"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardCollectionEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X GET \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/{labId}/search" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "Accept: application/json"
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-006",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-006.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-028` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-177` under simulated offline network conditions.

### 6.7 `API-LAB-007`: History Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-007`
- **HTTP Route:** `GET /api/v1/lab/history`
- **Functional Purpose:** Authoritative specification for history laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-179` | **Feature Code:** `FEATURE-179`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:get`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-059, SRS-NFR-019` | **Workflow:** `WF-004`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-029`
- **Planned Verification Test Case:** `PLANNED-TEST-API-178`
- **Dependency DAG Edge:** `API-DEP-059`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/history:
    get:
      summary: "History Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "get_api_v1_lab_history"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardCollectionEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X GET \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/history" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "Accept: application/json"
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-007",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-007.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-029` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-178` under simulated offline network conditions.

### 6.8 `API-LAB-008`: Audit Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-008`
- **HTTP Route:** `GET /api/v1/lab/{labId}/audit`
- **Functional Purpose:** Authoritative specification for audit laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-180` | **Feature Code:** `FEATURE-180`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:get`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-060, SRS-NFR-020` | **Workflow:** `WF-005`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-030`
- **Planned Verification Test Case:** `PLANNED-TEST-API-179`
- **Dependency DAG Edge:** `API-DEP-060`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/{labId}/audit:
    get:
      summary: "Audit Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "get_api_v1_lab_labId_audit"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X GET \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/{labId}/audit" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "Accept: application/json"
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-008",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-008.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-030` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-179` under simulated offline network conditions.

### 6.9 `API-LAB-009`: Cancel Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-009`
- **HTTP Route:** `POST /api/v1/lab/cancel`
- **Functional Purpose:** Authoritative specification for cancel laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-001` | **Feature Code:** `FEATURE-001`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:post`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-001, SRS-NFR-021` | **Workflow:** `WF-006`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-001`
- **Planned Verification Test Case:** `PLANNED-TEST-API-180`
- **Dependency DAG Edge:** `API-DEP-001`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/cancel:
    post:
      summary: "Cancel Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "post_api_v1_lab_cancel"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/StandardApiResponseEnvelope"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '409':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X POST \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/cancel" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "X-Idempotency-Key: 018e3a20-9000-7000-8000-000000000001" \
  -H "Content-Type: application/json" \
  -d '{"sampleAttribute": "value"}'
```

#### Request Body Wire Representation
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "facilityId": "018e3a20-0008-7000-8000-000000000001",
  "operation": "Cancel Laboratory Investigation Workflow Operation",
  "domain": "Lab",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-LAB-009"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-009",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-009.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-001` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-180` under simulated offline network conditions.

### 6.10 `API-LAB-010`: Verify Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-010`
- **HTTP Route:** `POST /api/v1/lab/verify`
- **Functional Purpose:** Authoritative specification for verify laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-002` | **Feature Code:** `FEATURE-002`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:post`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-002, SRS-NFR-022` | **Workflow:** `WF-007`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-002`
- **Planned Verification Test Case:** `PLANNED-TEST-API-181`
- **Dependency DAG Edge:** `API-DEP-002`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/verify:
    post:
      summary: "Verify Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "post_api_v1_lab_verify"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/StandardApiResponseEnvelope"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '409':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X POST \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/verify" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "X-Idempotency-Key: 018e3a20-9000-7000-8000-000000000001" \
  -H "Content-Type: application/json" \
  -d '{"sampleAttribute": "value"}'
```

#### Request Body Wire Representation
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "facilityId": "018e3a20-0008-7000-8000-000000000001",
  "operation": "Verify Laboratory Investigation Workflow Operation",
  "domain": "Lab",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-LAB-010"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-010",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-010.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-002` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-181` under simulated offline network conditions.

### 6.11 `API-LAB-011`: Export Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-011`
- **HTTP Route:** `GET /api/v1/lab/export`
- **Functional Purpose:** Authoritative specification for export laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-003` | **Feature Code:** `FEATURE-003`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:get`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-003, SRS-NFR-023` | **Workflow:** `WF-008`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-003`
- **Planned Verification Test Case:** `PLANNED-TEST-API-182`
- **Dependency DAG Edge:** `API-DEP-003`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/export:
    get:
      summary: "Export Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "get_api_v1_lab_export"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X GET \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/export" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "Accept: application/json"
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-011",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-011.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-003` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-182` under simulated offline network conditions.

### 6.12 `API-LAB-012`: Metrics Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-012`
- **HTTP Route:** `GET /api/v1/lab/{labId}/metrics`
- **Functional Purpose:** Authoritative specification for metrics laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-004` | **Feature Code:** `FEATURE-004`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:get`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-004, SRS-NFR-024` | **Workflow:** `WF-009`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-004`
- **Planned Verification Test Case:** `PLANNED-TEST-API-183`
- **Dependency DAG Edge:** `API-DEP-004`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/{labId}/metrics:
    get:
      summary: "Metrics Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "get_api_v1_lab_labId_metrics"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X GET \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/{labId}/metrics" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "Accept: application/json"
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-012",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-012.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-004` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-183` under simulated offline network conditions.

### 6.13 `API-LAB-013`: Reconcile Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-013`
- **HTTP Route:** `POST /api/v1/lab/reconcile`
- **Functional Purpose:** Authoritative specification for reconcile laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-005` | **Feature Code:** `FEATURE-005`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:post`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-005, SRS-NFR-025` | **Workflow:** `WF-010`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-005`
- **Planned Verification Test Case:** `PLANNED-TEST-API-184`
- **Dependency DAG Edge:** `API-DEP-005`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/reconcile:
    post:
      summary: "Reconcile Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "post_api_v1_lab_reconcile"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/StandardApiResponseEnvelope"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '409':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X POST \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/reconcile" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "X-Idempotency-Key: 018e3a20-9000-7000-8000-000000000001" \
  -H "Content-Type: application/json" \
  -d '{"sampleAttribute": "value"}'
```

#### Request Body Wire Representation
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "facilityId": "018e3a20-0008-7000-8000-000000000001",
  "operation": "Reconcile Laboratory Investigation Workflow Operation",
  "domain": "Lab",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-LAB-013"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-013",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-013.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-005` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-184` under simulated offline network conditions.

### 6.14 `API-LAB-014`: Batch Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-014`
- **HTTP Route:** `POST /api/v1/lab/batch`
- **Functional Purpose:** Authoritative specification for batch laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-006` | **Feature Code:** `FEATURE-006`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:post`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-006, SRS-NFR-026` | **Workflow:** `WF-011`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-006`
- **Planned Verification Test Case:** `PLANNED-TEST-API-185`
- **Dependency DAG Edge:** `API-DEP-006`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/batch:
    post:
      summary: "Batch Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "post_api_v1_lab_batch"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/StandardApiResponseEnvelope"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '409':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X POST \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/batch" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "X-Idempotency-Key: 018e3a20-9000-7000-8000-000000000001" \
  -H "Content-Type: application/json" \
  -d '{"sampleAttribute": "value"}'
```

#### Request Body Wire Representation
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "facilityId": "018e3a20-0008-7000-8000-000000000001",
  "operation": "Batch Laboratory Investigation Workflow Operation",
  "domain": "Lab",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-LAB-014"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-014",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-014.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-006` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-185` under simulated offline network conditions.

### 6.15 `API-LAB-015`: Sync Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-015`
- **HTTP Route:** `GET /api/v1/lab/sync`
- **Functional Purpose:** Authoritative specification for sync laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-007` | **Feature Code:** `FEATURE-007`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:get`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-007, SRS-NFR-027` | **Workflow:** `WF-012`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-007`
- **Planned Verification Test Case:** `PLANNED-TEST-API-186`
- **Dependency DAG Edge:** `API-DEP-007`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/sync:
    get:
      summary: "Sync Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "get_api_v1_lab_sync"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X GET \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/sync" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "Accept: application/json"
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-015",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-015.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-007` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-186` under simulated offline network conditions.

### 6.16 `API-LAB-016`: Alerts Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-016`
- **HTTP Route:** `GET /api/v1/lab/{labId}/alerts`
- **Functional Purpose:** Authoritative specification for alerts laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-008` | **Feature Code:** `FEATURE-008`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:get`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-008, SRS-NFR-028` | **Workflow:** `WF-013`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-008`
- **Planned Verification Test Case:** `PLANNED-TEST-API-187`
- **Dependency DAG Edge:** `API-DEP-008`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/{labId}/alerts:
    get:
      summary: "Alerts Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "get_api_v1_lab_labId_alerts"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardCollectionEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X GET \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/{labId}/alerts" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "Accept: application/json"
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-016",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-016.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-008` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-187` under simulated offline network conditions.

### 6.17 `API-LAB-017`: Escalate Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-017`
- **HTTP Route:** `POST /api/v1/lab/escalate`
- **Functional Purpose:** Authoritative specification for escalate laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-009` | **Feature Code:** `FEATURE-009`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:post`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-009, SRS-NFR-029` | **Workflow:** `WF-014`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-009`
- **Planned Verification Test Case:** `PLANNED-TEST-API-188`
- **Dependency DAG Edge:** `API-DEP-009`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/escalate:
    post:
      summary: "Escalate Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "post_api_v1_lab_escalate"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/StandardApiResponseEnvelope"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '409':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X POST \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/escalate" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "X-Idempotency-Key: 018e3a20-9000-7000-8000-000000000001" \
  -H "Content-Type: application/json" \
  -d '{"sampleAttribute": "value"}'
```

#### Request Body Wire Representation
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "facilityId": "018e3a20-0008-7000-8000-000000000001",
  "operation": "Escalate Laboratory Investigation Workflow Operation",
  "domain": "Lab",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-LAB-017"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-017",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-017.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-009` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-188` under simulated offline network conditions.

### 6.18 `API-LAB-018`: Approve Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-018`
- **HTTP Route:** `POST /api/v1/lab/approve`
- **Functional Purpose:** Authoritative specification for approve laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-010` | **Feature Code:** `FEATURE-010`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:post`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-010, SRS-NFR-030` | **Workflow:** `WF-015`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-010`
- **Planned Verification Test Case:** `PLANNED-TEST-API-189`
- **Dependency DAG Edge:** `API-DEP-010`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/approve:
    post:
      summary: "Approve Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "post_api_v1_lab_approve"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/StandardApiResponseEnvelope"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '409':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X POST \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/approve" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "X-Idempotency-Key: 018e3a20-9000-7000-8000-000000000001" \
  -H "Content-Type: application/json" \
  -d '{"sampleAttribute": "value"}'
```

#### Request Body Wire Representation
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "facilityId": "018e3a20-0008-7000-8000-000000000001",
  "operation": "Approve Laboratory Investigation Workflow Operation",
  "domain": "Lab",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-LAB-018"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-018",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-018.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-010` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-189` under simulated offline network conditions.

### 6.19 `API-LAB-019`: Reversal Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-019`
- **HTTP Route:** `POST /api/v1/lab/reversal`
- **Functional Purpose:** Authoritative specification for reversal laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-011` | **Feature Code:** `FEATURE-011`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:post`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-011, SRS-NFR-031` | **Workflow:** `WF-016`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-011`
- **Planned Verification Test Case:** `PLANNED-TEST-API-190`
- **Dependency DAG Edge:** `API-DEP-011`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/reversal:
    post:
      summary: "Reversal Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "post_api_v1_lab_reversal"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/StandardApiResponseEnvelope"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '409':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X POST \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/reversal" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "X-Idempotency-Key: 018e3a20-9000-7000-8000-000000000001" \
  -H "Content-Type: application/json" \
  -d '{"sampleAttribute": "value"}'
```

#### Request Body Wire Representation
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "facilityId": "018e3a20-0008-7000-8000-000000000001",
  "operation": "Reversal Laboratory Investigation Workflow Operation",
  "domain": "Lab",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-LAB-019"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-019",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-019.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-011` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-190` under simulated offline network conditions.

### 6.20 `API-LAB-020`: Items Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-020`
- **HTTP Route:** `GET /api/v1/lab/{labId}/items`
- **Functional Purpose:** Authoritative specification for items laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-012` | **Feature Code:** `FEATURE-012`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:get`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-012, SRS-NFR-032` | **Workflow:** `WF-017`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-012`
- **Planned Verification Test Case:** `PLANNED-TEST-API-191`
- **Dependency DAG Edge:** `API-DEP-012`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/{labId}/items:
    get:
      summary: "Items Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "get_api_v1_lab_labId_items"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardCollectionEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X GET \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/{labId}/items" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "Accept: application/json"
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-020",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-020.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-012` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-191` under simulated offline network conditions.

### 6.21 `API-LAB-021`: Documents Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-021`
- **HTTP Route:** `GET /api/v1/lab/documents`
- **Functional Purpose:** Authoritative specification for documents laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-013` | **Feature Code:** `FEATURE-013`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:get`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-013, SRS-NFR-033` | **Workflow:** `WF-018`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-013`
- **Planned Verification Test Case:** `PLANNED-TEST-API-192`
- **Dependency DAG Edge:** `API-DEP-013`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/documents:
    get:
      summary: "Documents Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "get_api_v1_lab_documents"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardCollectionEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X GET \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/documents" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "Accept: application/json"
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-021",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-021.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-013` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-192` under simulated offline network conditions.

### 6.22 `API-LAB-022`: Timeline Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-022`
- **HTTP Route:** `GET /api/v1/lab/{labId}/timeline`
- **Functional Purpose:** Authoritative specification for timeline laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-014` | **Feature Code:** `FEATURE-014`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:get`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-014, SRS-NFR-034` | **Workflow:** `WF-019`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-014`
- **Planned Verification Test Case:** `PLANNED-TEST-API-193`
- **Dependency DAG Edge:** `API-DEP-014`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/{labId}/timeline:
    get:
      summary: "Timeline Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "get_api_v1_lab_labId_timeline"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X GET \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/{labId}/timeline" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "Accept: application/json"
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-022",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-022.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-014` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-193` under simulated offline network conditions.

### 6.23 `API-LAB-023`: Stats Laboratory Investigation Workflow Operation

- **API Identifier:** `API-LAB-023`
- **HTTP Route:** `GET /api/v1/lab/stats`
- **Functional Purpose:** Authoritative specification for stats laboratory investigation workflow operation within Lab operations.
- **Product Capability:** `CAPABILITY-015` | **Feature Code:** `FEATURE-015`
- **Primary Actor:** Authorized Lab Operator | **User Persona:** Lab Care Team Persona
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:get`
- **ABAC Scoping Rule:** Restricted to authorized Lab personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-015, SRS-NFR-035` | **Workflow:** `WF-020`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_order_items, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-015`
- **Planned Verification Test Case:** `PLANNED-TEST-API-194`
- **Dependency DAG Edge:** `API-DEP-015`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/lab/stats:
    get:
      summary: "Stats Laboratory Investigation Workflow Operation"
      tags:
        - "Lab"
      operationId: "get_api_v1_lab_stats"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '404':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '500':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
```

#### Command Line Invocation Example (curl)
```bash
# DOCUMENTATION-ONLY EXAMPLE
curl -X GET \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/lab/stats" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Correlation-ID: 018e3a20-8000-7000-8000-000000000001" \
  -H "X-Facility-ID: 018e3a20-0008-7000-8000-000000000001" \
  -H "Accept: application/json"
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "lab",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-LAB-023",
      "domain": "Lab",
      "updatedAt": "2026-09-01T09:30:00.120Z"
    }
  },
  "meta": {
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "executionDurationMs": 28,
    "serverNode": "namma-clinic-edge-gateway-01",
    "timestamp": "2026-09-01T09:30:00.148Z"
  }
}
```

#### Error Response Wire Representation (`HTTP 400 / 409`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "error": {
    "code": "ERR-LAB-001",
    "message": "Domain constraint validation failed during execution of API-LAB-023.",
    "category": "ValidationFailure",
    "correlationId": "018e3a20-8000-7000-8000-000000000001",
    "timestamp": "2026-09-01T09:30:00.150Z",
    "retryable": false,
    "details": [
      {
        "field": "data.attributes.referenceId",
        "rule": "entity_not_found",
        "message": "The specified reference entity does not exist or has been tombstoned."
      }
    ]
  }
}
```

#### Relational Database & Audit Execution Effects
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_order_items, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-015` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-194` under simulated offline network conditions.

## 7. Domain-Specific Error Code Catalog & Troubleshooting Runbooks

The following standardized error codes are specifically emitted by `Lab` services:

| Error Code ID | HTTP Status | Machine Code | Message Summary | Retryable | Resolution Runbook |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-LAB-001** | `HTTP 404` | `LAB_ORDER_NOT_FOUND` | Diagnostic laboratory test order not found. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-LAB-001. |
| **ERR-LAB-002** | `HTTP 400` | `LAB_TEST_UNAVAILABLE_AT_CLINIC` | Requested rapid test is not configured in this Namma Clinic tier. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-LAB-002. |
| **ERR-LAB-003** | `HTTP 409` | `LAB_RESULT_ALREADY_SUBMITTED` | Test result has already been recorded and validated. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-LAB-003. |
| **ERR-LAB-004** | `HTTP 400` | `LAB_SPECIMEN_REJECTED` | Specimen rejected by lab technician; recollecting sample required. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-LAB-004. |
| **ERR-LAB-005** | `HTTP 403` | `LAB_TECHNICIAN_ROLE_REQUIRED` | Result entry requires registered laboratory technician role. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-LAB-005. |
| **ERR-LAB-006** | `HTTP 400` | `LAB_VALUE_OUT_OF_RANGE` | Reported quantitative value exceeds machine calibration boundaries. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-LAB-006. |
| **ERR-LAB-007** | `HTTP 400` | `LAB_BARCODE_ALREADY_USED` | Specimen barcode identifier has already been bound to another accession. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-LAB-007. |
| **ERR-LAB-008** | `HTTP 500` | `LAB_ANALYZER_INTERFACE_DOWN` | Direct point-of-care rapid analyzer serial interface failed. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-LAB-008. |

## 8. Offline Edge Operation & Synchronization Mechanics

When WAN connectivity to the central cloud is disrupted, `Lab` operations transition to autonomous edge mode:
1. **Local SQLite WAL Database:** Transactions are committed locally to `/data/namma_clinic_edge.db` on the clinic's Intel N100 mini-server.
2. **Offline Mutation Journal:** Every INSERT, UPDATE, and SOFT_DELETE appends a record to the `offline_mutation_log` table with a local vector clock.
3. **Conflict Resolution Policy:** Upon WAN restoration, the edge sync agent uploads buffered mutations in batches of 100 to `/api/v1/system/sync/batch`. Conflicts are resolved deterministically using Last-Write-Wins (LWW) with microsecond Lamport timestamps, except for clinical records where doctor entries take precedence over clerical updates.
4. **Storage Quotas:** Up to 72 hours of offline operations (approximately 15,000 mutations) can be buffered without storage degradation.

## 9. Security, Data Protection & DPDP Act Compliance

Data protection invariants for `Lab` operations:

| Data Element | Classification | Encryption Standard | Masking Rule | DPDP Act Section | Retention Schedule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Core Entity Record | `CONFIDENTIAL` | AES-256-GCM Column Level | Masked on non-admin UI | Section 8 (Data Security) | 10 Years (Medical Records) |
| Transaction Mutation | INTERNAL | TLS 1.3 in Transit | Zero PII in Gateway Logs | Section 6 (Consent Notice) | 10 Years (Audit Ledger) |
| WORM Audit Log | HIGHLY-RESTRICTED | HMAC SHA-256 Chained | Full Hash Ledger | Section 12 (Citizen Rights) | Permanent (Statutory Archive) |

## 10. Domain Quality Acceptance Criteria (BDD)

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify Successful Execution of Create New Laboratory Investigation Record
  Given an authenticated staff member with role 'ROLE-018'
  And an active clinical shift rostered in clinic facility '018e3a20-0008-7000-8000-000000000001'
  When the client sends a valid request to /api/v1/lab
  Then the server processes the request within 1500ms
  And returns HTTP 201
  And the response conforms to envelope schema 'StandardApiResponseEnvelope'
  And an immutable audit log is appended to 'AUDIT-EVENT-023'
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Reject Unauthorized Call to Create New Laboratory Investigation Record
  Given a caller presenting an invalid or expired Bearer token
  And requesting protected resource access
  When the caller transmits a request to /api/v1/lab
  Then the API gateway intercepts the request
  And returns HTTP 401 Unauthorized
  And returns error code 'ERR-AUTH-002' or 'ERR-AUTH-003'
  And rejects access before invoking backend services
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Execute Create New Laboratory Investigation Record in Autonomous Edge Mode
  Given the clinic workstation has lost WAN connectivity to cloud
  And the local edge mini-server is operational with local SQLite database
  When the staff member executes Create New Laboratory Investigation Record
  Then the edge API gateway accepts the request locally
  And returns HTTP 201 within 250ms
  And appends the mutation to the local offline sync journal
  And synchronizes to cloud automatically upon network restoration
```

## 11. Requirements & Database Relational Traceability Matrix

Traceability mapping for all `Lab` endpoints:

| Endpoint ID | Upstream SRS Requirements | Workflow ID | Feature Code | Target Database Tables | Verification Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `API-LAB-001` | `SRS-FR-053, SRS-NFR-013` | `WF-023` | `FEATURE-173` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-172` |
| `API-LAB-002` | `SRS-FR-054, SRS-NFR-014` | `WF-024` | `FEATURE-174` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-173` |
| `API-LAB-003` | `SRS-FR-055, SRS-NFR-015` | `WF-025` | `FEATURE-175` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-174` |
| `API-LAB-004` | `SRS-FR-056, SRS-NFR-016` | `WF-001` | `FEATURE-176` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-175` |
| `API-LAB-005` | `SRS-FR-057, SRS-NFR-017` | `WF-002` | `FEATURE-177` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-176` |
| `API-LAB-006` | `SRS-FR-058, SRS-NFR-018` | `WF-003` | `FEATURE-178` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-177` |
| `API-LAB-007` | `SRS-FR-059, SRS-NFR-019` | `WF-004` | `FEATURE-179` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-178` |
| `API-LAB-008` | `SRS-FR-060, SRS-NFR-020` | `WF-005` | `FEATURE-180` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-179` |
| `API-LAB-009` | `SRS-FR-001, SRS-NFR-021` | `WF-006` | `FEATURE-001` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-180` |
| `API-LAB-010` | `SRS-FR-002, SRS-NFR-022` | `WF-007` | `FEATURE-002` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-181` |
| `API-LAB-011` | `SRS-FR-003, SRS-NFR-023` | `WF-008` | `FEATURE-003` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-182` |
| `API-LAB-012` | `SRS-FR-004, SRS-NFR-024` | `WF-009` | `FEATURE-004` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-183` |
| `API-LAB-013` | `SRS-FR-005, SRS-NFR-025` | `WF-010` | `FEATURE-005` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-184` |
| `API-LAB-014` | `SRS-FR-006, SRS-NFR-026` | `WF-011` | `FEATURE-006` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-185` |
| `API-LAB-015` | `SRS-FR-007, SRS-NFR-027` | `WF-012` | `FEATURE-007` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-186` |
| `API-LAB-016` | `SRS-FR-008, SRS-NFR-028` | `WF-013` | `FEATURE-008` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-187` |
| `API-LAB-017` | `SRS-FR-009, SRS-NFR-029` | `WF-014` | `FEATURE-009` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-188` |
| `API-LAB-018` | `SRS-FR-010, SRS-NFR-030` | `WF-015` | `FEATURE-010` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-189` |
| `API-LAB-019` | `SRS-FR-011, SRS-NFR-031` | `WF-016` | `FEATURE-011` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-190` |
| `API-LAB-020` | `SRS-FR-012, SRS-NFR-032` | `WF-017` | `FEATURE-012` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-191` |
| `API-LAB-021` | `SRS-FR-013, SRS-NFR-033` | `WF-018` | `FEATURE-013` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-192` |
| `API-LAB-022` | `SRS-FR-014, SRS-NFR-034` | `WF-019` | `FEATURE-014` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-193` |
| `API-LAB-023` | `SRS-FR-015, SRS-NFR-035` | `WF-020` | `FEATURE-015` | `lab_orders, lab_order_items, lab_results` | `PLANNED-TEST-API-194` |
