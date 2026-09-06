# 🔌 API Specification: Referral Management & Secondary Hospital Bridge API Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-13 | **Status:** Authoritative Baseline | **Date:** September 2026
> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Standard Framework:** RFC 7231 (HTTP/1.1), JSON:API v1.1, DPDP Act 2023, ABDM Interoperability Standards
> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.

---

## 1. Executive Summary & Domain Scope

The **Referral Management & Secondary Hospital Bridge API Specification** defines the authoritative, implementation-ready contracts for the `Referral` subsystem across all 183 Namma Clinic primary healthcare centers in Greater Bengaluru. This domain operates under the supervisory jurisdiction of `ROLE-002 (Referring Medical Officer)` and fulfills the core mission: **Facilitate outward patient transfers to BBMP General Hospitals and government medical colleges, dispatch 108 Arogya Kavacha ambulances, and ingest counter-referral discharge notes.**

All 19 endpoints specified in this document adhere strictly to uniform JSON:API response envelopes, time-ordered UUIDv7 identifiers, ISO-8601 UTC timestamps, optimistic concurrency control via ETags, and automated audit logging.

## 2. Operational Architecture & Relational Mapping

The following table maps the domain's operational context to architectural containers, components, database tables, and default role entitlements:

| Dimension | Specification Detail |
| :--- | :--- |
| **Functional Domain** | `Referral` (Code: `REF`) |
| **Authoritative Endpoints** | 19 Active Endpoints (`API-REF-001` to `API-REF-019`) |
| **Primary Architecture Container** | `ARCH-CONT-011` |
| **Assigned Component** | `ARCH-COMP-031` |
| **Primary Database Tables** | `referrals, referral_counter_notes` |
| **Lead Role Entitlement** | `ROLE-002 (Referring Medical Officer)` |
| **Default Rate Limiting** | `60 req/min per User` |
| **Offline Edge Support** | `Edge Local Queue with Delta Sync` |

## 3. Domain Operational State Machine

The operational state transitions governing entities within this domain are modeled below:

```mermaid
stateDiagram-v2
    [*] --> ReferralInitiated: Doctor Identifies Need for Higher Care
    ReferralInitiated --> DossierCompiled: Auto-Assemble Vitals, Notes, Diagnoses
    DossierCompiled --> AmbulanceRequested: 108 Emergency Ambulance Dispatched
    DossierCompiled --> RoutineTransfer: Patient Directed to Outpatient Specialty
    AmbulanceRequested --> PatientEnRoute: Telemetry Bridge Active
    PatientEnRoute --> TertiaryAdmitted: Receiving Hospital Acknowledges
    TertiaryAdmitted --> CounterNoteReceived: Discharge Summary Ingested
    CounterNoteReceived --> Closed: Continuity of Care Complete
    Closed --> [*]
```

## 4. End-to-End Operational Data Flow

The sequence diagram below illustrates the end-to-end operational flow between frontline clinic staff, edge workstations, the central API gateway, and backing data stores:

```mermaid
sequenceDiagram
    autonumber
    participant Doc as Clinic Doctor
    participant UI as Clinic EMR
    participant API as Referral Service
    participant EMS as 108 Ambulance Dispatch Gateway
    participant Hospital as BBMP General Hospital
    Doc->>UI: Initiate Emergency Referral (Acute Coronary Syndrome)
    UI->>API: POST /api/v1/referrals
    API->>EMS: Transmit 108 Dispatch Request with GPS Location
    API->>Hospital: Pre-Alert Emergency Department with Patient EMR Dossier
    EMS-->>API: Ambulance Dispatched (ETA: 8 mins)
    API-->>UI: HTTP 201 Created (Referral Dispatched)
```

## 5. Domain Endpoint Inventory Catalog

Complete inventory of all 19 endpoints defined for the `Referral` domain:

| Endpoint ID | Method | URI Route Path | Functional Title | Role Context | Idempotency Standard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API-REF-001** | `POST` | `/api/v1/referrals` | Create New Hospital Referral Record | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-REF-002** | `GET` | `/api/v1/referrals/{referralId}` | Retrieve Hospital Referral Details by ID | `ROLE-002` | Read-Only Idempotent |
| **API-REF-003** | `GET` | `/api/v1/referrals` | List and Filter Hospital Referral Records | `ROLE-002` | Read-Only Idempotent |
| **API-REF-004** | `PUT` | `/api/v1/referrals/{referralId}` | Update Full Hospital Referral Specification | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-REF-005** | `PATCH` | `/api/v1/referrals/{referralId}/status` | Update Hospital Referral Operational State | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-REF-006** | `GET` | `/api/v1/referrals/{referralId}/search` | Search Hospital Referral Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-REF-007** | `GET` | `/api/v1/referrals/history` | History Hospital Referral Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-REF-008** | `GET` | `/api/v1/referrals/{referralId}/audit` | Audit Hospital Referral Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-REF-009** | `POST` | `/api/v1/referrals/cancel` | Cancel Hospital Referral Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-REF-010** | `POST` | `/api/v1/referrals/verify` | Verify Hospital Referral Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-REF-011** | `GET` | `/api/v1/referrals/export` | Export Hospital Referral Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-REF-012** | `GET` | `/api/v1/referrals/{referralId}/metrics` | Metrics Hospital Referral Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-REF-013** | `POST` | `/api/v1/referrals/reconcile` | Reconcile Hospital Referral Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-REF-014** | `POST` | `/api/v1/referrals/batch` | Batch Hospital Referral Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-REF-015** | `GET` | `/api/v1/referrals/sync` | Sync Hospital Referral Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-REF-016** | `GET` | `/api/v1/referrals/{referralId}/alerts` | Alerts Hospital Referral Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-REF-017** | `POST` | `/api/v1/referrals/escalate` | Escalate Hospital Referral Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-REF-018** | `POST` | `/api/v1/referrals/approve` | Approve Hospital Referral Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-REF-019** | `POST` | `/api/v1/referrals/reversal` | Reversal Hospital Referral Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |

## 6. Comprehensive Endpoint Technical Specifications

Exhaustive technical contracts for all 19 endpoints in the `Referral` domain:

### 6.1 `API-REF-001`: Create New Hospital Referral Record

- **API Identifier:** `API-REF-001`
- **HTTP Route:** `POST /api/v1/referrals`
- **Functional Purpose:** Authoritative specification for create new hospital referral record within Referral operations.
- **Product Capability:** `CAPABILITY-016` | **Feature Code:** `FEATURE-016`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:post`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-016, SRS-NFR-036` | **Workflow:** `WF-021`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-016`
- **Planned Verification Test Case:** `PLANNED-TEST-API-195`
- **Dependency DAG Edge:** `API-DEP-016`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals:
    post:
      summary: "Create New Hospital Referral Record"
      tags:
        - "Referral"
      operationId: "post_api_v1_referrals"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals" \
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
  "operation": "Create New Hospital Referral Record",
  "domain": "Referral",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-REF-001"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-001",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-001.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-016` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-195` under simulated offline network conditions.

### 6.2 `API-REF-002`: Retrieve Hospital Referral Details by ID

- **API Identifier:** `API-REF-002`
- **HTTP Route:** `GET /api/v1/referrals/{referralId}`
- **Functional Purpose:** Authoritative specification for retrieve hospital referral details by id within Referral operations.
- **Product Capability:** `CAPABILITY-017` | **Feature Code:** `FEATURE-017`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:get`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-017, SRS-NFR-037` | **Workflow:** `WF-022`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-017`
- **Planned Verification Test Case:** `PLANNED-TEST-API-196`
- **Dependency DAG Edge:** `API-DEP-017`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/{referralId}:
    get:
      summary: "Retrieve Hospital Referral Details by ID"
      tags:
        - "Referral"
      operationId: "get_api_v1_referrals_referralId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/{referralId}" \
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
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-002",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-002.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-017` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-196` under simulated offline network conditions.

### 6.3 `API-REF-003`: List and Filter Hospital Referral Records

- **API Identifier:** `API-REF-003`
- **HTTP Route:** `GET /api/v1/referrals`
- **Functional Purpose:** Authoritative specification for list and filter hospital referral records within Referral operations.
- **Product Capability:** `CAPABILITY-018` | **Feature Code:** `FEATURE-018`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:get`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-018, SRS-NFR-038` | **Workflow:** `WF-023`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-018`
- **Planned Verification Test Case:** `PLANNED-TEST-API-197`
- **Dependency DAG Edge:** `API-DEP-018`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals:
    get:
      summary: "List and Filter Hospital Referral Records"
      tags:
        - "Referral"
      operationId: "get_api_v1_referrals"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals" \
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
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-003",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-003.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-018` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-197` under simulated offline network conditions.

### 6.4 `API-REF-004`: Update Full Hospital Referral Specification

- **API Identifier:** `API-REF-004`
- **HTTP Route:** `PUT /api/v1/referrals/{referralId}`
- **Functional Purpose:** Authoritative specification for update full hospital referral specification within Referral operations.
- **Product Capability:** `CAPABILITY-019` | **Feature Code:** `FEATURE-019`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:put`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-019, SRS-NFR-039` | **Workflow:** `WF-024`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-019`
- **Planned Verification Test Case:** `PLANNED-TEST-API-198`
- **Dependency DAG Edge:** `API-DEP-019`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/{referralId}:
    put:
      summary: "Update Full Hospital Referral Specification"
      tags:
        - "Referral"
      operationId: "put_api_v1_referrals_referralId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/{referralId}" \
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
  "operation": "Update Full Hospital Referral Specification",
  "domain": "Referral",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-REF-004"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-004",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-004.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-019` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-198` under simulated offline network conditions.

### 6.5 `API-REF-005`: Update Hospital Referral Operational State

- **API Identifier:** `API-REF-005`
- **HTTP Route:** `PATCH /api/v1/referrals/{referralId}/status`
- **Functional Purpose:** Authoritative specification for update hospital referral operational state within Referral operations.
- **Product Capability:** `CAPABILITY-020` | **Feature Code:** `FEATURE-020`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:patch`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-020, SRS-NFR-040` | **Workflow:** `WF-025`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-020`
- **Planned Verification Test Case:** `PLANNED-TEST-API-199`
- **Dependency DAG Edge:** `API-DEP-020`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/{referralId}/status:
    patch:
      summary: "Update Hospital Referral Operational State"
      tags:
        - "Referral"
      operationId: "patch_api_v1_referrals_referralId_status"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/{referralId}/status" \
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
  "operation": "Update Hospital Referral Operational State",
  "domain": "Referral",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-REF-005"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-005",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-005.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-020` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-199` under simulated offline network conditions.

### 6.6 `API-REF-006`: Search Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-006`
- **HTTP Route:** `GET /api/v1/referrals/{referralId}/search`
- **Functional Purpose:** Authoritative specification for search hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-021` | **Feature Code:** `FEATURE-021`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:get`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-021, SRS-NFR-001` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-021`
- **Planned Verification Test Case:** `PLANNED-TEST-API-200`
- **Dependency DAG Edge:** `API-DEP-021`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/{referralId}/search:
    get:
      summary: "Search Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "get_api_v1_referrals_referralId_search"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/{referralId}/search" \
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
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-006",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-006.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-021` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-200` under simulated offline network conditions.

### 6.7 `API-REF-007`: History Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-007`
- **HTTP Route:** `GET /api/v1/referrals/history`
- **Functional Purpose:** Authoritative specification for history hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-022` | **Feature Code:** `FEATURE-022`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:get`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-022, SRS-NFR-002` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-022`
- **Planned Verification Test Case:** `PLANNED-TEST-API-201`
- **Dependency DAG Edge:** `API-DEP-022`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/history:
    get:
      summary: "History Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "get_api_v1_referrals_history"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/history" \
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
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-007",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-007.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-022` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-201` under simulated offline network conditions.

### 6.8 `API-REF-008`: Audit Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-008`
- **HTTP Route:** `GET /api/v1/referrals/{referralId}/audit`
- **Functional Purpose:** Authoritative specification for audit hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-023` | **Feature Code:** `FEATURE-023`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:get`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-023, SRS-NFR-003` | **Workflow:** `WF-003`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-023`
- **Planned Verification Test Case:** `PLANNED-TEST-API-202`
- **Dependency DAG Edge:** `API-DEP-023`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/{referralId}/audit:
    get:
      summary: "Audit Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "get_api_v1_referrals_referralId_audit"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/{referralId}/audit" \
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
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-008",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-008.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-023` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-202` under simulated offline network conditions.

### 6.9 `API-REF-009`: Cancel Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-009`
- **HTTP Route:** `POST /api/v1/referrals/cancel`
- **Functional Purpose:** Authoritative specification for cancel hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-024` | **Feature Code:** `FEATURE-024`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:post`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-024, SRS-NFR-004` | **Workflow:** `WF-004`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-024`
- **Planned Verification Test Case:** `PLANNED-TEST-API-203`
- **Dependency DAG Edge:** `API-DEP-024`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/cancel:
    post:
      summary: "Cancel Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "post_api_v1_referrals_cancel"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/cancel" \
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
  "operation": "Cancel Hospital Referral Workflow Operation",
  "domain": "Referral",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-REF-009"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-009",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-009.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-024` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-203` under simulated offline network conditions.

### 6.10 `API-REF-010`: Verify Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-010`
- **HTTP Route:** `POST /api/v1/referrals/verify`
- **Functional Purpose:** Authoritative specification for verify hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-025` | **Feature Code:** `FEATURE-025`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:post`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-025, SRS-NFR-005` | **Workflow:** `WF-005`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-025`
- **Planned Verification Test Case:** `PLANNED-TEST-API-204`
- **Dependency DAG Edge:** `API-DEP-025`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/verify:
    post:
      summary: "Verify Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "post_api_v1_referrals_verify"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/verify" \
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
  "operation": "Verify Hospital Referral Workflow Operation",
  "domain": "Referral",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-REF-010"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-010",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-010.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-025` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-204` under simulated offline network conditions.

### 6.11 `API-REF-011`: Export Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-011`
- **HTTP Route:** `GET /api/v1/referrals/export`
- **Functional Purpose:** Authoritative specification for export hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-026` | **Feature Code:** `FEATURE-026`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:get`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-026, SRS-NFR-006` | **Workflow:** `WF-006`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-026`
- **Planned Verification Test Case:** `PLANNED-TEST-API-205`
- **Dependency DAG Edge:** `API-DEP-026`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/export:
    get:
      summary: "Export Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "get_api_v1_referrals_export"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/export" \
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
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-011",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-011.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-026` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-205` under simulated offline network conditions.

### 6.12 `API-REF-012`: Metrics Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-012`
- **HTTP Route:** `GET /api/v1/referrals/{referralId}/metrics`
- **Functional Purpose:** Authoritative specification for metrics hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-027` | **Feature Code:** `FEATURE-027`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:get`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-027, SRS-NFR-007` | **Workflow:** `WF-007`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-027`
- **Planned Verification Test Case:** `PLANNED-TEST-API-206`
- **Dependency DAG Edge:** `API-DEP-027`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/{referralId}/metrics:
    get:
      summary: "Metrics Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "get_api_v1_referrals_referralId_metrics"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/{referralId}/metrics" \
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
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-012",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-012.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-027` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-206` under simulated offline network conditions.

### 6.13 `API-REF-013`: Reconcile Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-013`
- **HTTP Route:** `POST /api/v1/referrals/reconcile`
- **Functional Purpose:** Authoritative specification for reconcile hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-028` | **Feature Code:** `FEATURE-028`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:post`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-028, SRS-NFR-008` | **Workflow:** `WF-008`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-028`
- **Planned Verification Test Case:** `PLANNED-TEST-API-207`
- **Dependency DAG Edge:** `API-DEP-028`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/reconcile:
    post:
      summary: "Reconcile Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "post_api_v1_referrals_reconcile"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/reconcile" \
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
  "operation": "Reconcile Hospital Referral Workflow Operation",
  "domain": "Referral",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-REF-013"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-013",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-013.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-028` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-207` under simulated offline network conditions.

### 6.14 `API-REF-014`: Batch Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-014`
- **HTTP Route:** `POST /api/v1/referrals/batch`
- **Functional Purpose:** Authoritative specification for batch hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-029` | **Feature Code:** `FEATURE-029`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:post`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-029, SRS-NFR-009` | **Workflow:** `WF-009`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-029`
- **Planned Verification Test Case:** `PLANNED-TEST-API-208`
- **Dependency DAG Edge:** `API-DEP-029`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/batch:
    post:
      summary: "Batch Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "post_api_v1_referrals_batch"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/batch" \
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
  "operation": "Batch Hospital Referral Workflow Operation",
  "domain": "Referral",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-REF-014"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-014",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-014.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-029` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-208` under simulated offline network conditions.

### 6.15 `API-REF-015`: Sync Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-015`
- **HTTP Route:** `GET /api/v1/referrals/sync`
- **Functional Purpose:** Authoritative specification for sync hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-030` | **Feature Code:** `FEATURE-030`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:get`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-030, SRS-NFR-010` | **Workflow:** `WF-010`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-030`
- **Planned Verification Test Case:** `PLANNED-TEST-API-209`
- **Dependency DAG Edge:** `API-DEP-030`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/sync:
    get:
      summary: "Sync Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "get_api_v1_referrals_sync"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/sync" \
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
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-015",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-015.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-030` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-209` under simulated offline network conditions.

### 6.16 `API-REF-016`: Alerts Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-016`
- **HTTP Route:** `GET /api/v1/referrals/{referralId}/alerts`
- **Functional Purpose:** Authoritative specification for alerts hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-031` | **Feature Code:** `FEATURE-031`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:get`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-031, SRS-NFR-011` | **Workflow:** `WF-011`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-001`
- **Planned Verification Test Case:** `PLANNED-TEST-API-210`
- **Dependency DAG Edge:** `API-DEP-031`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/{referralId}/alerts:
    get:
      summary: "Alerts Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "get_api_v1_referrals_referralId_alerts"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/{referralId}/alerts" \
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
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-016",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-016.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-001` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-210` under simulated offline network conditions.

### 6.17 `API-REF-017`: Escalate Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-017`
- **HTTP Route:** `POST /api/v1/referrals/escalate`
- **Functional Purpose:** Authoritative specification for escalate hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-032` | **Feature Code:** `FEATURE-032`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:post`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-032, SRS-NFR-012` | **Workflow:** `WF-012`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-002`
- **Planned Verification Test Case:** `PLANNED-TEST-API-211`
- **Dependency DAG Edge:** `API-DEP-032`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/escalate:
    post:
      summary: "Escalate Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "post_api_v1_referrals_escalate"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/escalate" \
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
  "operation": "Escalate Hospital Referral Workflow Operation",
  "domain": "Referral",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-REF-017"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-017",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-017.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-002` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-211` under simulated offline network conditions.

### 6.18 `API-REF-018`: Approve Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-018`
- **HTTP Route:** `POST /api/v1/referrals/approve`
- **Functional Purpose:** Authoritative specification for approve hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-033` | **Feature Code:** `FEATURE-033`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:post`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-033, SRS-NFR-013` | **Workflow:** `WF-013`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-003`
- **Planned Verification Test Case:** `PLANNED-TEST-API-212`
- **Dependency DAG Edge:** `API-DEP-033`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/approve:
    post:
      summary: "Approve Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "post_api_v1_referrals_approve"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/approve" \
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
  "operation": "Approve Hospital Referral Workflow Operation",
  "domain": "Referral",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-REF-018"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-018",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-018.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-003` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-212` under simulated offline network conditions.

### 6.19 `API-REF-019`: Reversal Hospital Referral Workflow Operation

- **API Identifier:** `API-REF-019`
- **HTTP Route:** `POST /api/v1/referrals/reversal`
- **Functional Purpose:** Authoritative specification for reversal hospital referral workflow operation within Referral operations.
- **Product Capability:** `CAPABILITY-034` | **Feature Code:** `FEATURE-034`
- **Primary Actor:** Authorized Referral Operator | **User Persona:** Referral Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `referrals:post`
- **ABAC Scoping Rule:** Restricted to authorized Referral personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-034, SRS-NFR-014` | **Workflow:** `WF-014`
- **Container / Component:** `ARCH-CONT-011` / `ARCH-COMP-031`
- **Target Relational Tables:** `referrals, referral_counter_notes`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-004`
- **Planned Verification Test Case:** `PLANNED-TEST-API-213`
- **Dependency DAG Edge:** `API-DEP-034`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/referrals/reversal:
    post:
      summary: "Reversal Hospital Referral Workflow Operation"
      tags:
        - "Referral"
      operationId: "post_api_v1_referrals_reversal"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/referrals/reversal" \
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
  "operation": "Reversal Hospital Referral Workflow Operation",
  "domain": "Referral",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-REF-019"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "referral",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-REF-019",
      "domain": "Referral",
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
    "code": "ERR-REF-001",
    "message": "Domain constraint validation failed during execution of API-REF-019.",
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
- **Relational Database Mutation:** Modifies tables `referrals, referral_counter_notes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-004` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-213` under simulated offline network conditions.

## 7. Domain-Specific Error Code Catalog & Troubleshooting Runbooks

The following standardized error codes are specifically emitted by `Referral` services:

| Error Code ID | HTTP Status | Machine Code | Message Summary | Retryable | Resolution Runbook |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-REF-001** | `HTTP 404` | `REF_NOT_FOUND` | Hospital referral dossier does not exist. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-REF-001. |
| **ERR-REF-002** | `HTTP 400` | `REF_DESTINATION_HOSPITAL_INVALID` | Destination facility must be an accredited secondary or tertiary hospital. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-REF-002. |
| **ERR-REF-003** | `HTTP 409` | `REF_ALREADY_ACCEPTED` | Referral has already been accepted by receiving secondary hospital. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-REF-003. |
| **ERR-REF-004** | `HTTP 400` | `REF_EMERGENCY_AMBULANCE_REQUIRED` | Emergency referrals require 108 ambulance dispatch confirmation or override reason. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-REF-004. |
| **ERR-REF-005** | `HTTP 403` | `REF_DOCTOR_AUTHORIZATION_REQUIRED` | Only attending medical officers may initiate outward hospital referrals. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-REF-005. |
| **ERR-REF-006** | `HTTP 500` | `REF_EMS_BRIDGE_UNAVAILABLE` | State 108 ambulance dispatch telemetry API gateway unreachable. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-REF-006. |

## 8. Offline Edge Operation & Synchronization Mechanics

When WAN connectivity to the central cloud is disrupted, `Referral` operations transition to autonomous edge mode:
1. **Local SQLite WAL Database:** Transactions are committed locally to `/data/namma_clinic_edge.db` on the clinic's Intel N100 mini-server.
2. **Offline Mutation Journal:** Every INSERT, UPDATE, and SOFT_DELETE appends a record to the `offline_mutation_log` table with a local vector clock.
3. **Conflict Resolution Policy:** Upon WAN restoration, the edge sync agent uploads buffered mutations in batches of 100 to `/api/v1/system/sync/batch`. Conflicts are resolved deterministically using Last-Write-Wins (LWW) with microsecond Lamport timestamps, except for clinical records where doctor entries take precedence over clerical updates.
4. **Storage Quotas:** Up to 72 hours of offline operations (approximately 15,000 mutations) can be buffered without storage degradation.

## 9. Security, Data Protection & DPDP Act Compliance

Data protection invariants for `Referral` operations:

| Data Element | Classification | Encryption Standard | Masking Rule | DPDP Act Section | Retention Schedule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Core Entity Record | `INTERNAL` | AES-256-GCM Column Level | Masked on non-admin UI | Section 8 (Data Security) | 10 Years (Medical Records) |
| Transaction Mutation | INTERNAL | TLS 1.3 in Transit | Zero PII in Gateway Logs | Section 6 (Consent Notice) | 10 Years (Audit Ledger) |
| WORM Audit Log | HIGHLY-RESTRICTED | HMAC SHA-256 Chained | Full Hash Ledger | Section 12 (Citizen Rights) | Permanent (Statutory Archive) |

## 10. Domain Quality Acceptance Criteria (BDD)

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify Successful Execution of Create New Hospital Referral Record
  Given an authenticated staff member with role 'ROLE-002'
  And an active clinical shift rostered in clinic facility '018e3a20-0008-7000-8000-000000000001'
  When the client sends a valid request to /api/v1/referrals
  Then the server processes the request within 1500ms
  And returns HTTP 201
  And the response conforms to envelope schema 'StandardApiResponseEnvelope'
  And an immutable audit log is appended to 'AUDIT-EVENT-016'
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Reject Unauthorized Call to Create New Hospital Referral Record
  Given a caller presenting an invalid or expired Bearer token
  And requesting protected resource access
  When the caller transmits a request to /api/v1/referrals
  Then the API gateway intercepts the request
  And returns HTTP 401 Unauthorized
  And returns error code 'ERR-AUTH-002' or 'ERR-AUTH-003'
  And rejects access before invoking backend services
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Execute Create New Hospital Referral Record in Autonomous Edge Mode
  Given the clinic workstation has lost WAN connectivity to cloud
  And the local edge mini-server is operational with local SQLite database
  When the staff member executes Create New Hospital Referral Record
  Then the edge API gateway accepts the request locally
  And returns HTTP 201 within 250ms
  And appends the mutation to the local offline sync journal
  And synchronizes to cloud automatically upon network restoration
```

## 11. Requirements & Database Relational Traceability Matrix

Traceability mapping for all `Referral` endpoints:

| Endpoint ID | Upstream SRS Requirements | Workflow ID | Feature Code | Target Database Tables | Verification Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `API-REF-001` | `SRS-FR-016, SRS-NFR-036` | `WF-021` | `FEATURE-016` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-195` |
| `API-REF-002` | `SRS-FR-017, SRS-NFR-037` | `WF-022` | `FEATURE-017` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-196` |
| `API-REF-003` | `SRS-FR-018, SRS-NFR-038` | `WF-023` | `FEATURE-018` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-197` |
| `API-REF-004` | `SRS-FR-019, SRS-NFR-039` | `WF-024` | `FEATURE-019` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-198` |
| `API-REF-005` | `SRS-FR-020, SRS-NFR-040` | `WF-025` | `FEATURE-020` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-199` |
| `API-REF-006` | `SRS-FR-021, SRS-NFR-001` | `WF-001` | `FEATURE-021` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-200` |
| `API-REF-007` | `SRS-FR-022, SRS-NFR-002` | `WF-002` | `FEATURE-022` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-201` |
| `API-REF-008` | `SRS-FR-023, SRS-NFR-003` | `WF-003` | `FEATURE-023` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-202` |
| `API-REF-009` | `SRS-FR-024, SRS-NFR-004` | `WF-004` | `FEATURE-024` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-203` |
| `API-REF-010` | `SRS-FR-025, SRS-NFR-005` | `WF-005` | `FEATURE-025` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-204` |
| `API-REF-011` | `SRS-FR-026, SRS-NFR-006` | `WF-006` | `FEATURE-026` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-205` |
| `API-REF-012` | `SRS-FR-027, SRS-NFR-007` | `WF-007` | `FEATURE-027` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-206` |
| `API-REF-013` | `SRS-FR-028, SRS-NFR-008` | `WF-008` | `FEATURE-028` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-207` |
| `API-REF-014` | `SRS-FR-029, SRS-NFR-009` | `WF-009` | `FEATURE-029` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-208` |
| `API-REF-015` | `SRS-FR-030, SRS-NFR-010` | `WF-010` | `FEATURE-030` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-209` |
| `API-REF-016` | `SRS-FR-031, SRS-NFR-011` | `WF-011` | `FEATURE-031` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-210` |
| `API-REF-017` | `SRS-FR-032, SRS-NFR-012` | `WF-012` | `FEATURE-032` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-211` |
| `API-REF-018` | `SRS-FR-033, SRS-NFR-013` | `WF-013` | `FEATURE-033` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-212` |
| `API-REF-019` | `SRS-FR-034, SRS-NFR-014` | `WF-014` | `FEATURE-034` | `referrals, referral_counter_notes` | `PLANNED-TEST-API-213` |
