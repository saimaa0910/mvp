# 🔌 API Specification: Triage Assessment, Vitals Acquisition & Early Warning API Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-07 | **Status:** Authoritative Baseline | **Date:** September 2026
> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Standard Framework:** RFC 7231 (HTTP/1.1), JSON:API v1.1, DPDP Act 2023, ABDM Interoperability Standards
> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.

---

## 1. Executive Summary & Domain Scope

The **Triage Assessment, Vitals Acquisition & Early Warning API Specification** defines the authoritative, implementation-ready contracts for the `Triage` subsystem across all 183 Namma Clinic primary healthcare centers in Greater Bengaluru. This domain operates under the supervisory jurisdiction of `ROLE-016 (Registered Staff Nurse)` and fulfills the core mission: **Capture physiologic vital signs, evaluate South African Triage Scale (SATS) color acuity tiers, calculate Modified Early Warning Scores (MEWS), and trigger immediate doctor escalation for critical patients.**

All 19 endpoints specified in this document adhere strictly to uniform JSON:API response envelopes, time-ordered UUIDv7 identifiers, ISO-8601 UTC timestamps, optimistic concurrency control via ETags, and automated audit logging.

## 2. Operational Architecture & Relational Mapping

The following table maps the domain's operational context to architectural containers, components, database tables, and default role entitlements:

| Dimension | Specification Detail |
| :--- | :--- |
| **Functional Domain** | `Triage` (Code: `TRIAGE`) |
| **Authoritative Endpoints** | 19 Active Endpoints (`API-TRIAGE-001` to `API-TRIAGE-019`) |
| **Primary Architecture Container** | `ARCH-CONT-006` |
| **Assigned Component** | `ARCH-COMP-017` |
| **Primary Database Tables** | `triage_assessments, patient_vitals, danger_alerts` |
| **Lead Role Entitlement** | `ROLE-016 (Registered Staff Nurse)` |
| **Default Rate Limiting** | `60 req/min per User` |
| **Offline Edge Support** | `Edge Local Queue with Delta Sync` |

## 3. Domain Operational State Machine

The operational state transitions governing entities within this domain are modeled below:

```mermaid
stateDiagram-v2
    [*] --> PendingAssessment: Patient Arrives at Triage Station
    PendingAssessment --> VitalsCaptured: Nurse Records BP, Pulse, SpO2, Temp
    VitalsCaptured --> ScoringEngine: Automated SATS / MEWS Calculation
    ScoringEngine --> GreenRoutine: MEWS 0-1 (Routine Outpatient)
    ScoringEngine --> YellowModerate: MEWS 2-3 (Moderate Priority)
    ScoringEngine --> OrangeUrgent: MEWS 4-5 (Urgent Medical Review)
    ScoringEngine --> RedEmergency: MEWS >= 6 or Danger Sign (Immediate Resuscitation)
    RedEmergency --> PagerTriggered: Automated Doctor Alert Broadcast
    GreenRoutine --> Finalized: Triage Completed
    Finalized --> [*]
```

## 4. End-to-End Operational Data Flow

The sequence diagram below illustrates the end-to-end operational flow between frontline clinic staff, edge workstations, the central API gateway, and backing data stores:

```mermaid
sequenceDiagram
    autonumber
    participant Nurse as Triage Staff Nurse
    participant Tab as Triage Tablet UI
    participant API as Triage Service
    participant Engine as Clinical Scoring Engine
    participant AlertSvc as Emergency Alert Dispatcher
    Nurse->>Tab: Input BP: 80/50, Pulse: 130, SpO2: 89%
    Tab->>API: POST /api/v1/triage
    API->>Engine: Evaluate Vitals Matrix
    Engine-->>API: MEWS Score: 7 (RED Acuity Emergency)
    API->>AlertSvc: Trigger Emergency Room Pager
    AlertSvc-->>Nurse: Display Immediate Red Banner
    API-->>Tab: HTTP 201 Created (Acuity: RED, Alert: Triggered)
```

## 5. Domain Endpoint Inventory Catalog

Complete inventory of all 19 endpoints defined for the `Triage` domain:

| Endpoint ID | Method | URI Route Path | Functional Title | Role Context | Idempotency Standard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API-TRIAGE-001** | `POST` | `/api/v1/triage` | Create New Triage Assessment Record | `ROLE-016` | Supported via X-Idempotency-Key |
| **API-TRIAGE-002** | `GET` | `/api/v1/triage/{triageId}` | Retrieve Triage Assessment Details by ID | `ROLE-016` | Read-Only Idempotent |
| **API-TRIAGE-003** | `GET` | `/api/v1/triage` | List and Filter Triage Assessment Records | `ROLE-016` | Read-Only Idempotent |
| **API-TRIAGE-004** | `PUT` | `/api/v1/triage/{triageId}` | Update Full Triage Assessment Specification | `ROLE-016` | Supported via X-Idempotency-Key |
| **API-TRIAGE-005** | `PATCH` | `/api/v1/triage/{triageId}/status` | Update Triage Assessment Operational State | `ROLE-016` | Supported via X-Idempotency-Key |
| **API-TRIAGE-006** | `GET` | `/api/v1/triage/{triageId}/search` | Search Triage Assessment Workflow Operation | `ROLE-016` | Read-Only Idempotent |
| **API-TRIAGE-007** | `GET` | `/api/v1/triage/history` | History Triage Assessment Workflow Operation | `ROLE-016` | Read-Only Idempotent |
| **API-TRIAGE-008** | `GET` | `/api/v1/triage/{triageId}/audit` | Audit Triage Assessment Workflow Operation | `ROLE-016` | Read-Only Idempotent |
| **API-TRIAGE-009** | `POST` | `/api/v1/triage/cancel` | Cancel Triage Assessment Workflow Operation | `ROLE-016` | Supported via X-Idempotency-Key |
| **API-TRIAGE-010** | `POST` | `/api/v1/triage/verify` | Verify Triage Assessment Workflow Operation | `ROLE-016` | Supported via X-Idempotency-Key |
| **API-TRIAGE-011** | `GET` | `/api/v1/triage/export` | Export Triage Assessment Workflow Operation | `ROLE-016` | Read-Only Idempotent |
| **API-TRIAGE-012** | `GET` | `/api/v1/triage/{triageId}/metrics` | Metrics Triage Assessment Workflow Operation | `ROLE-016` | Read-Only Idempotent |
| **API-TRIAGE-013** | `POST` | `/api/v1/triage/reconcile` | Reconcile Triage Assessment Workflow Operation | `ROLE-016` | Supported via X-Idempotency-Key |
| **API-TRIAGE-014** | `POST` | `/api/v1/triage/batch` | Batch Triage Assessment Workflow Operation | `ROLE-016` | Supported via X-Idempotency-Key |
| **API-TRIAGE-015** | `GET` | `/api/v1/triage/sync` | Sync Triage Assessment Workflow Operation | `ROLE-016` | Read-Only Idempotent |
| **API-TRIAGE-016** | `GET` | `/api/v1/triage/{triageId}/alerts` | Alerts Triage Assessment Workflow Operation | `ROLE-016` | Read-Only Idempotent |
| **API-TRIAGE-017** | `POST` | `/api/v1/triage/escalate` | Escalate Triage Assessment Workflow Operation | `ROLE-016` | Supported via X-Idempotency-Key |
| **API-TRIAGE-018** | `POST` | `/api/v1/triage/approve` | Approve Triage Assessment Workflow Operation | `ROLE-016` | Supported via X-Idempotency-Key |
| **API-TRIAGE-019** | `POST` | `/api/v1/triage/reversal` | Reversal Triage Assessment Workflow Operation | `ROLE-016` | Supported via X-Idempotency-Key |

## 6. Comprehensive Endpoint Technical Specifications

Exhaustive technical contracts for all 19 endpoints in the `Triage` domain:

### 6.1 `API-TRIAGE-001`: Create New Triage Assessment Record

- **API Identifier:** `API-TRIAGE-001`
- **HTTP Route:** `POST /api/v1/triage`
- **Functional Purpose:** Authoritative specification for create new triage assessment record within Triage operations.
- **Product Capability:** `CAPABILITY-065` | **Feature Code:** `FEATURE-065`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:post`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-005, SRS-NFR-025` | **Workflow:** `WF-015`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-005`
- **Planned Verification Test Case:** `PLANNED-TEST-API-064`
- **Dependency DAG Edge:** `API-DEP-005`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage:
    post:
      summary: "Create New Triage Assessment Record"
      tags:
        - "Triage"
      operationId: "post_api_v1_triage"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage" \
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
  "operation": "Create New Triage Assessment Record",
  "domain": "Triage",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-TRIAGE-001"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-001",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-001.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-005` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-064` under simulated offline network conditions.

### 6.2 `API-TRIAGE-002`: Retrieve Triage Assessment Details by ID

- **API Identifier:** `API-TRIAGE-002`
- **HTTP Route:** `GET /api/v1/triage/{triageId}`
- **Functional Purpose:** Authoritative specification for retrieve triage assessment details by id within Triage operations.
- **Product Capability:** `CAPABILITY-066` | **Feature Code:** `FEATURE-066`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:get`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-006, SRS-NFR-026` | **Workflow:** `WF-016`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-006`
- **Planned Verification Test Case:** `PLANNED-TEST-API-065`
- **Dependency DAG Edge:** `API-DEP-006`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/{triageId}:
    get:
      summary: "Retrieve Triage Assessment Details by ID"
      tags:
        - "Triage"
      operationId: "get_api_v1_triage_triageId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/{triageId}" \
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
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-002",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-002.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-006` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-065` under simulated offline network conditions.

### 6.3 `API-TRIAGE-003`: List and Filter Triage Assessment Records

- **API Identifier:** `API-TRIAGE-003`
- **HTTP Route:** `GET /api/v1/triage`
- **Functional Purpose:** Authoritative specification for list and filter triage assessment records within Triage operations.
- **Product Capability:** `CAPABILITY-067` | **Feature Code:** `FEATURE-067`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:get`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-007, SRS-NFR-027` | **Workflow:** `WF-017`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-007`
- **Planned Verification Test Case:** `PLANNED-TEST-API-066`
- **Dependency DAG Edge:** `API-DEP-007`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage:
    get:
      summary: "List and Filter Triage Assessment Records"
      tags:
        - "Triage"
      operationId: "get_api_v1_triage"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage" \
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
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-003",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-003.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-007` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-066` under simulated offline network conditions.

### 6.4 `API-TRIAGE-004`: Update Full Triage Assessment Specification

- **API Identifier:** `API-TRIAGE-004`
- **HTTP Route:** `PUT /api/v1/triage/{triageId}`
- **Functional Purpose:** Authoritative specification for update full triage assessment specification within Triage operations.
- **Product Capability:** `CAPABILITY-068` | **Feature Code:** `FEATURE-068`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:put`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-008, SRS-NFR-028` | **Workflow:** `WF-018`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-008`
- **Planned Verification Test Case:** `PLANNED-TEST-API-067`
- **Dependency DAG Edge:** `API-DEP-008`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/{triageId}:
    put:
      summary: "Update Full Triage Assessment Specification"
      tags:
        - "Triage"
      operationId: "put_api_v1_triage_triageId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/{triageId}" \
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
  "operation": "Update Full Triage Assessment Specification",
  "domain": "Triage",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-TRIAGE-004"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-004",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-004.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-008` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-067` under simulated offline network conditions.

### 6.5 `API-TRIAGE-005`: Update Triage Assessment Operational State

- **API Identifier:** `API-TRIAGE-005`
- **HTTP Route:** `PATCH /api/v1/triage/{triageId}/status`
- **Functional Purpose:** Authoritative specification for update triage assessment operational state within Triage operations.
- **Product Capability:** `CAPABILITY-069` | **Feature Code:** `FEATURE-069`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:patch`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-009, SRS-NFR-029` | **Workflow:** `WF-019`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-009`
- **Planned Verification Test Case:** `PLANNED-TEST-API-068`
- **Dependency DAG Edge:** `API-DEP-009`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/{triageId}/status:
    patch:
      summary: "Update Triage Assessment Operational State"
      tags:
        - "Triage"
      operationId: "patch_api_v1_triage_triageId_status"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/{triageId}/status" \
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
  "operation": "Update Triage Assessment Operational State",
  "domain": "Triage",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-TRIAGE-005"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-005",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-005.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-009` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-068` under simulated offline network conditions.

### 6.6 `API-TRIAGE-006`: Search Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-006`
- **HTTP Route:** `GET /api/v1/triage/{triageId}/search`
- **Functional Purpose:** Authoritative specification for search triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-070` | **Feature Code:** `FEATURE-070`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:get`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-010, SRS-NFR-030` | **Workflow:** `WF-020`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-010`
- **Planned Verification Test Case:** `PLANNED-TEST-API-069`
- **Dependency DAG Edge:** `API-DEP-010`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/{triageId}/search:
    get:
      summary: "Search Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "get_api_v1_triage_triageId_search"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/{triageId}/search" \
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
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-006",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-006.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-010` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-069` under simulated offline network conditions.

### 6.7 `API-TRIAGE-007`: History Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-007`
- **HTTP Route:** `GET /api/v1/triage/history`
- **Functional Purpose:** Authoritative specification for history triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-071` | **Feature Code:** `FEATURE-071`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:get`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-011, SRS-NFR-031` | **Workflow:** `WF-021`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-011`
- **Planned Verification Test Case:** `PLANNED-TEST-API-070`
- **Dependency DAG Edge:** `API-DEP-011`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/history:
    get:
      summary: "History Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "get_api_v1_triage_history"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/history" \
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
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-007",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-007.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-011` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-070` under simulated offline network conditions.

### 6.8 `API-TRIAGE-008`: Audit Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-008`
- **HTTP Route:** `GET /api/v1/triage/{triageId}/audit`
- **Functional Purpose:** Authoritative specification for audit triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-072` | **Feature Code:** `FEATURE-072`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:get`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-012, SRS-NFR-032` | **Workflow:** `WF-022`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-012`
- **Planned Verification Test Case:** `PLANNED-TEST-API-071`
- **Dependency DAG Edge:** `API-DEP-012`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/{triageId}/audit:
    get:
      summary: "Audit Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "get_api_v1_triage_triageId_audit"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/{triageId}/audit" \
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
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-008",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-008.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-012` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-071` under simulated offline network conditions.

### 6.9 `API-TRIAGE-009`: Cancel Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-009`
- **HTTP Route:** `POST /api/v1/triage/cancel`
- **Functional Purpose:** Authoritative specification for cancel triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-073` | **Feature Code:** `FEATURE-073`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:post`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-013, SRS-NFR-033` | **Workflow:** `WF-023`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-013`
- **Planned Verification Test Case:** `PLANNED-TEST-API-072`
- **Dependency DAG Edge:** `API-DEP-013`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/cancel:
    post:
      summary: "Cancel Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "post_api_v1_triage_cancel"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/cancel" \
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
  "operation": "Cancel Triage Assessment Workflow Operation",
  "domain": "Triage",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-TRIAGE-009"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-009",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-009.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-013` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-072` under simulated offline network conditions.

### 6.10 `API-TRIAGE-010`: Verify Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-010`
- **HTTP Route:** `POST /api/v1/triage/verify`
- **Functional Purpose:** Authoritative specification for verify triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-074` | **Feature Code:** `FEATURE-074`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:post`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-014, SRS-NFR-034` | **Workflow:** `WF-024`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-014`
- **Planned Verification Test Case:** `PLANNED-TEST-API-073`
- **Dependency DAG Edge:** `API-DEP-014`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/verify:
    post:
      summary: "Verify Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "post_api_v1_triage_verify"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/verify" \
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
  "operation": "Verify Triage Assessment Workflow Operation",
  "domain": "Triage",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-TRIAGE-010"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-010",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-010.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-014` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-073` under simulated offline network conditions.

### 6.11 `API-TRIAGE-011`: Export Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-011`
- **HTTP Route:** `GET /api/v1/triage/export`
- **Functional Purpose:** Authoritative specification for export triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-075` | **Feature Code:** `FEATURE-075`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:get`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-015, SRS-NFR-035` | **Workflow:** `WF-025`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-015`
- **Planned Verification Test Case:** `PLANNED-TEST-API-074`
- **Dependency DAG Edge:** `API-DEP-015`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/export:
    get:
      summary: "Export Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "get_api_v1_triage_export"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/export" \
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
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-011",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-011.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-015` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-074` under simulated offline network conditions.

### 6.12 `API-TRIAGE-012`: Metrics Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-012`
- **HTTP Route:** `GET /api/v1/triage/{triageId}/metrics`
- **Functional Purpose:** Authoritative specification for metrics triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-076` | **Feature Code:** `FEATURE-076`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:get`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-016, SRS-NFR-036` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-016`
- **Planned Verification Test Case:** `PLANNED-TEST-API-075`
- **Dependency DAG Edge:** `API-DEP-016`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/{triageId}/metrics:
    get:
      summary: "Metrics Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "get_api_v1_triage_triageId_metrics"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/{triageId}/metrics" \
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
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-012",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-012.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-016` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-075` under simulated offline network conditions.

### 6.13 `API-TRIAGE-013`: Reconcile Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-013`
- **HTTP Route:** `POST /api/v1/triage/reconcile`
- **Functional Purpose:** Authoritative specification for reconcile triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-077` | **Feature Code:** `FEATURE-077`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:post`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-017, SRS-NFR-037` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-017`
- **Planned Verification Test Case:** `PLANNED-TEST-API-076`
- **Dependency DAG Edge:** `API-DEP-017`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/reconcile:
    post:
      summary: "Reconcile Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "post_api_v1_triage_reconcile"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/reconcile" \
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
  "operation": "Reconcile Triage Assessment Workflow Operation",
  "domain": "Triage",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-TRIAGE-013"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-013",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-013.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-017` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-076` under simulated offline network conditions.

### 6.14 `API-TRIAGE-014`: Batch Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-014`
- **HTTP Route:** `POST /api/v1/triage/batch`
- **Functional Purpose:** Authoritative specification for batch triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-078` | **Feature Code:** `FEATURE-078`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:post`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-018, SRS-NFR-038` | **Workflow:** `WF-003`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-018`
- **Planned Verification Test Case:** `PLANNED-TEST-API-077`
- **Dependency DAG Edge:** `API-DEP-018`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/batch:
    post:
      summary: "Batch Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "post_api_v1_triage_batch"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/batch" \
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
  "operation": "Batch Triage Assessment Workflow Operation",
  "domain": "Triage",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-TRIAGE-014"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-014",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-014.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-018` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-077` under simulated offline network conditions.

### 6.15 `API-TRIAGE-015`: Sync Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-015`
- **HTTP Route:** `GET /api/v1/triage/sync`
- **Functional Purpose:** Authoritative specification for sync triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-079` | **Feature Code:** `FEATURE-079`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:get`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-019, SRS-NFR-039` | **Workflow:** `WF-004`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-019`
- **Planned Verification Test Case:** `PLANNED-TEST-API-078`
- **Dependency DAG Edge:** `API-DEP-019`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/sync:
    get:
      summary: "Sync Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "get_api_v1_triage_sync"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/sync" \
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
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-015",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-015.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-019` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-078` under simulated offline network conditions.

### 6.16 `API-TRIAGE-016`: Alerts Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-016`
- **HTTP Route:** `GET /api/v1/triage/{triageId}/alerts`
- **Functional Purpose:** Authoritative specification for alerts triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-080` | **Feature Code:** `FEATURE-080`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:get`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-020, SRS-NFR-040` | **Workflow:** `WF-005`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-020`
- **Planned Verification Test Case:** `PLANNED-TEST-API-079`
- **Dependency DAG Edge:** `API-DEP-020`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/{triageId}/alerts:
    get:
      summary: "Alerts Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "get_api_v1_triage_triageId_alerts"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/{triageId}/alerts" \
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
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-016",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-016.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-020` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-079` under simulated offline network conditions.

### 6.17 `API-TRIAGE-017`: Escalate Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-017`
- **HTTP Route:** `POST /api/v1/triage/escalate`
- **Functional Purpose:** Authoritative specification for escalate triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-081` | **Feature Code:** `FEATURE-081`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:post`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-021, SRS-NFR-001` | **Workflow:** `WF-006`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-021`
- **Planned Verification Test Case:** `PLANNED-TEST-API-080`
- **Dependency DAG Edge:** `API-DEP-021`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/escalate:
    post:
      summary: "Escalate Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "post_api_v1_triage_escalate"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/escalate" \
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
  "operation": "Escalate Triage Assessment Workflow Operation",
  "domain": "Triage",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-TRIAGE-017"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-017",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-017.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-021` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-080` under simulated offline network conditions.

### 6.18 `API-TRIAGE-018`: Approve Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-018`
- **HTTP Route:** `POST /api/v1/triage/approve`
- **Functional Purpose:** Authoritative specification for approve triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-082` | **Feature Code:** `FEATURE-082`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:post`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-022, SRS-NFR-002` | **Workflow:** `WF-007`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-022`
- **Planned Verification Test Case:** `PLANNED-TEST-API-081`
- **Dependency DAG Edge:** `API-DEP-022`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/approve:
    post:
      summary: "Approve Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "post_api_v1_triage_approve"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/approve" \
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
  "operation": "Approve Triage Assessment Workflow Operation",
  "domain": "Triage",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-TRIAGE-018"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-018",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-018.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-022` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-081` under simulated offline network conditions.

### 6.19 `API-TRIAGE-019`: Reversal Triage Assessment Workflow Operation

- **API Identifier:** `API-TRIAGE-019`
- **HTTP Route:** `POST /api/v1/triage/reversal`
- **Functional Purpose:** Authoritative specification for reversal triage assessment workflow operation within Triage operations.
- **Product Capability:** `CAPABILITY-083` | **Feature Code:** `FEATURE-083`
- **Primary Actor:** Authorized Triage Operator | **User Persona:** Triage Care Team Persona
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `triage:post`
- **ABAC Scoping Rule:** Restricted to authorized Triage personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-023, SRS-NFR-003` | **Workflow:** `WF-008`
- **Container / Component:** `ARCH-CONT-006` / `ARCH-COMP-017`
- **Target Relational Tables:** `triage_assessments, patient_vitals, danger_alerts`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-023`
- **Planned Verification Test Case:** `PLANNED-TEST-API-082`
- **Dependency DAG Edge:** `API-DEP-023`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/triage/reversal:
    post:
      summary: "Reversal Triage Assessment Workflow Operation"
      tags:
        - "Triage"
      operationId: "post_api_v1_triage_reversal"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/triage/reversal" \
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
  "operation": "Reversal Triage Assessment Workflow Operation",
  "domain": "Triage",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-TRIAGE-019"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "triage",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-TRIAGE-019",
      "domain": "Triage",
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
    "code": "ERR-TRIAGE-001",
    "message": "Domain constraint validation failed during execution of API-TRIAGE-019.",
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
- **Relational Database Mutation:** Modifies tables `triage_assessments, patient_vitals, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-023` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-082` under simulated offline network conditions.

## 7. Domain-Specific Error Code Catalog & Troubleshooting Runbooks

The following standardized error codes are specifically emitted by `Triage` services:

| Error Code ID | HTTP Status | Machine Code | Message Summary | Retryable | Resolution Runbook |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-TRIAGE-001** | `HTTP 404` | `TRIAGE_NOT_FOUND` | No triage assessment recorded for this visit. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-TRIAGE-001. |
| **ERR-TRIAGE-002** | `HTTP 400` | `TRIAGE_VITALS_OUT_OF_PHYSIOLOGIC_RANGE` | Vitals measurement is outside biological life boundaries (e.g., SpO2 > 100%). | No | Verify client request format, ensure active session, and inspect audit logs for ERR-TRIAGE-002. |
| **ERR-TRIAGE-003** | `HTTP 400` | `TRIAGE_SYSTOLIC_LESS_THAN_DIASTOLIC` | Systolic blood pressure cannot be lower than diastolic pressure. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-TRIAGE-003. |
| **ERR-TRIAGE-004** | `HTTP 409` | `TRIAGE_ALREADY_FINALIZED` | Triage assessment is already completed and cannot be overwritten. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-TRIAGE-004. |
| **ERR-TRIAGE-005** | `HTTP 400` | `TRIAGE_RED_ESCALATION_OVERRIDE_FORBIDDEN` | Cannot downgrade RED acuity triage without physician written concurrence. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-TRIAGE-005. |
| **ERR-TRIAGE-006** | `HTTP 403` | `TRIAGE_NURSE_AUTHORIZATION_REQUIRED` | Only registered staff nurses or doctors may record triage acuity. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-TRIAGE-006. |
| **ERR-TRIAGE-007** | `HTTP 400` | `TRIAGE_PULSE_MISSING` | Pulse rate is mandatory for computing MEWS acuity score. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-TRIAGE-007. |
| **ERR-TRIAGE-008** | `HTTP 400` | `TRIAGE_TEMPERATURE_EXTREME` | Temperature reading indicates severe hypothermia or hyperpyrexia. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-TRIAGE-008. |
| **ERR-TRIAGE-009** | `HTTP 500` | `TRIAGE_SCORING_ENGINE_ERROR` | Automated SATS/MEWS rule evaluation engine returned calculation error. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-TRIAGE-009. |
| **ERR-TRIAGE-010** | `HTTP 400` | `TRIAGE_VISIT_STATE_INVALID` | Cannot triage a visit that is already closed or cancelled. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-TRIAGE-010. |

## 8. Offline Edge Operation & Synchronization Mechanics

When WAN connectivity to the central cloud is disrupted, `Triage` operations transition to autonomous edge mode:
1. **Local SQLite WAL Database:** Transactions are committed locally to `/data/namma_clinic_edge.db` on the clinic's Intel N100 mini-server.
2. **Offline Mutation Journal:** Every INSERT, UPDATE, and SOFT_DELETE appends a record to the `offline_mutation_log` table with a local vector clock.
3. **Conflict Resolution Policy:** Upon WAN restoration, the edge sync agent uploads buffered mutations in batches of 100 to `/api/v1/system/sync/batch`. Conflicts are resolved deterministically using Last-Write-Wins (LWW) with microsecond Lamport timestamps, except for clinical records where doctor entries take precedence over clerical updates.
4. **Storage Quotas:** Up to 72 hours of offline operations (approximately 15,000 mutations) can be buffered without storage degradation.

## 9. Security, Data Protection & DPDP Act Compliance

Data protection invariants for `Triage` operations:

| Data Element | Classification | Encryption Standard | Masking Rule | DPDP Act Section | Retention Schedule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Core Entity Record | `CONFIDENTIAL` | AES-256-GCM Column Level | Masked on non-admin UI | Section 8 (Data Security) | 10 Years (Medical Records) |
| Transaction Mutation | INTERNAL | TLS 1.3 in Transit | Zero PII in Gateway Logs | Section 6 (Consent Notice) | 10 Years (Audit Ledger) |
| WORM Audit Log | HIGHLY-RESTRICTED | HMAC SHA-256 Chained | Full Hash Ledger | Section 12 (Citizen Rights) | Permanent (Statutory Archive) |

## 10. Domain Quality Acceptance Criteria (BDD)

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify Successful Execution of Create New Triage Assessment Record
  Given an authenticated staff member with role 'ROLE-016'
  And an active clinical shift rostered in clinic facility '018e3a20-0008-7000-8000-000000000001'
  When the client sends a valid request to /api/v1/triage
  Then the server processes the request within 1500ms
  And returns HTTP 201
  And the response conforms to envelope schema 'StandardApiResponseEnvelope'
  And an immutable audit log is appended to 'AUDIT-EVENT-005'
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Reject Unauthorized Call to Create New Triage Assessment Record
  Given a caller presenting an invalid or expired Bearer token
  And requesting protected resource access
  When the caller transmits a request to /api/v1/triage
  Then the API gateway intercepts the request
  And returns HTTP 401 Unauthorized
  And returns error code 'ERR-AUTH-002' or 'ERR-AUTH-003'
  And rejects access before invoking backend services
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Execute Create New Triage Assessment Record in Autonomous Edge Mode
  Given the clinic workstation has lost WAN connectivity to cloud
  And the local edge mini-server is operational with local SQLite database
  When the staff member executes Create New Triage Assessment Record
  Then the edge API gateway accepts the request locally
  And returns HTTP 201 within 250ms
  And appends the mutation to the local offline sync journal
  And synchronizes to cloud automatically upon network restoration
```

## 11. Requirements & Database Relational Traceability Matrix

Traceability mapping for all `Triage` endpoints:

| Endpoint ID | Upstream SRS Requirements | Workflow ID | Feature Code | Target Database Tables | Verification Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `API-TRIAGE-001` | `SRS-FR-005, SRS-NFR-025` | `WF-015` | `FEATURE-065` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-064` |
| `API-TRIAGE-002` | `SRS-FR-006, SRS-NFR-026` | `WF-016` | `FEATURE-066` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-065` |
| `API-TRIAGE-003` | `SRS-FR-007, SRS-NFR-027` | `WF-017` | `FEATURE-067` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-066` |
| `API-TRIAGE-004` | `SRS-FR-008, SRS-NFR-028` | `WF-018` | `FEATURE-068` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-067` |
| `API-TRIAGE-005` | `SRS-FR-009, SRS-NFR-029` | `WF-019` | `FEATURE-069` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-068` |
| `API-TRIAGE-006` | `SRS-FR-010, SRS-NFR-030` | `WF-020` | `FEATURE-070` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-069` |
| `API-TRIAGE-007` | `SRS-FR-011, SRS-NFR-031` | `WF-021` | `FEATURE-071` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-070` |
| `API-TRIAGE-008` | `SRS-FR-012, SRS-NFR-032` | `WF-022` | `FEATURE-072` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-071` |
| `API-TRIAGE-009` | `SRS-FR-013, SRS-NFR-033` | `WF-023` | `FEATURE-073` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-072` |
| `API-TRIAGE-010` | `SRS-FR-014, SRS-NFR-034` | `WF-024` | `FEATURE-074` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-073` |
| `API-TRIAGE-011` | `SRS-FR-015, SRS-NFR-035` | `WF-025` | `FEATURE-075` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-074` |
| `API-TRIAGE-012` | `SRS-FR-016, SRS-NFR-036` | `WF-001` | `FEATURE-076` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-075` |
| `API-TRIAGE-013` | `SRS-FR-017, SRS-NFR-037` | `WF-002` | `FEATURE-077` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-076` |
| `API-TRIAGE-014` | `SRS-FR-018, SRS-NFR-038` | `WF-003` | `FEATURE-078` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-077` |
| `API-TRIAGE-015` | `SRS-FR-019, SRS-NFR-039` | `WF-004` | `FEATURE-079` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-078` |
| `API-TRIAGE-016` | `SRS-FR-020, SRS-NFR-040` | `WF-005` | `FEATURE-080` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-079` |
| `API-TRIAGE-017` | `SRS-FR-021, SRS-NFR-001` | `WF-006` | `FEATURE-081` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-080` |
| `API-TRIAGE-018` | `SRS-FR-022, SRS-NFR-002` | `WF-007` | `FEATURE-082` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-081` |
| `API-TRIAGE-019` | `SRS-FR-023, SRS-NFR-003` | `WF-008` | `FEATURE-083` | `triage_assessments, patient_vitals, danger_alerts` | `PLANNED-TEST-API-082` |
