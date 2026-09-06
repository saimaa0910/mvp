# 🔌 API Specification: Clinical Consultation, EMR & Diagnostic Coding API Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-08 | **Status:** Authoritative Baseline | **Date:** September 2026
> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Standard Framework:** RFC 7231 (HTTP/1.1), JSON:API v1.1, DPDP Act 2023, ABDM Interoperability Standards
> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.

---

## 1. Executive Summary & Domain Scope

The **Clinical Consultation, EMR & Diagnostic Coding API Specification** defines the authoritative, implementation-ready contracts for the `Consultation` subsystem across all 183 Namma Clinic primary healthcare centers in Greater Bengaluru. This domain operates under the supervisory jurisdiction of `ROLE-002 (Medical Officer / Clinician)` and fulfills the core mission: **Provide outpatient SOAP clinical progress notes, chief complaint recording, WHO ICD-10 diagnostic coding, Clinical Decision Support System (CDSS) advisories, and encounter closure.**

All 23 endpoints specified in this document adhere strictly to uniform JSON:API response envelopes, time-ordered UUIDv7 identifiers, ISO-8601 UTC timestamps, optimistic concurrency control via ETags, and automated audit logging.

## 2. Operational Architecture & Relational Mapping

The following table maps the domain's operational context to architectural containers, components, database tables, and default role entitlements:

| Dimension | Specification Detail |
| :--- | :--- |
| **Functional Domain** | `Consultation` (Code: `CONSULT`) |
| **Authoritative Endpoints** | 23 Active Endpoints (`API-CONSULT-001` to `API-CONSULT-023`) |
| **Primary Architecture Container** | `ARCH-CONT-007` |
| **Assigned Component** | `ARCH-COMP-019` |
| **Primary Database Tables** | `clinical_encounters, clinical_notes, diagnoses` |
| **Lead Role Entitlement** | `ROLE-002 (Medical Officer / Clinician)` |
| **Default Rate Limiting** | `60 req/min per User` |
| **Offline Edge Support** | `Edge Local Queue with Delta Sync` |

## 3. Domain Operational State Machine

The operational state transitions governing entities within this domain are modeled below:

```mermaid
stateDiagram-v2
    [*] --> EncounterOpened: Doctor Calls Patient into Room
    EncounterOpened --> HistoryIntake: Review Chief Complaints & Past Visits
    HistoryIntake --> PhysicalExam: Record Systemic Clinical Findings
    PhysicalExam --> DiagnosticCoding: Select ICD-10 & SNOMED CT Codes
    DiagnosticCoding --> CdssAdvisory: Evaluate Clinical Guidelines
    CdssAdvisory --> CarePlanDefined: Prescriptions & Lab Tests Linked
    CarePlanDefined --> Finalized: Doctor Signs Encounter
    Finalized --> AddendumAppended: Formal Clinician Addendum
    Finalized --> [*]
```

## 4. End-to-End Operational Data Flow

The sequence diagram below illustrates the end-to-end operational flow between frontline clinic staff, edge workstations, the central API gateway, and backing data stores:

```mermaid
sequenceDiagram
    autonumber
    participant Doctor as Medical Officer
    participant UI as Doctor Consultation Station
    participant API as Consultation Service
    participant CDSS as Decision Support Microservice
    participant DB as EMR PostgreSQL Database
    Doctor->>UI: Enter Chief Complaints (Fever x 3 days)
    Doctor->>UI: Select ICD-10 Diagnosis (A90 Dengue Fever)
    UI->>API: POST /api/v1/consultations
    API->>CDSS: Check Syndromic Fever Cluster Guidelines
    CDSS-->>API: Suggest Rapid Dengue NS1 Antigen Test
    API->>DB: Persist Encounter, Notes, Diagnoses
    API-->>UI: HTTP 201 Created (Encounter Finalized)
```

## 5. Domain Endpoint Inventory Catalog

Complete inventory of all 23 endpoints defined for the `Consultation` domain:

| Endpoint ID | Method | URI Route Path | Functional Title | Role Context | Idempotency Standard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API-CONSULT-001** | `POST` | `/api/v1/consultations` | Create New Clinical Consultation Record | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-CONSULT-002** | `GET` | `/api/v1/consultations/{consultationId}` | Retrieve Clinical Consultation Details by ID | `ROLE-002` | Read-Only Idempotent |
| **API-CONSULT-003** | `GET` | `/api/v1/consultations` | List and Filter Clinical Consultation Records | `ROLE-002` | Read-Only Idempotent |
| **API-CONSULT-004** | `PUT` | `/api/v1/consultations/{consultationId}` | Update Full Clinical Consultation Specification | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-CONSULT-005** | `PATCH` | `/api/v1/consultations/{consultationId}/status` | Update Clinical Consultation Operational State | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-CONSULT-006** | `GET` | `/api/v1/consultations/{consultationId}/search` | Search Clinical Consultation Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-CONSULT-007** | `GET` | `/api/v1/consultations/history` | History Clinical Consultation Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-CONSULT-008** | `GET` | `/api/v1/consultations/{consultationId}/audit` | Audit Clinical Consultation Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-CONSULT-009** | `POST` | `/api/v1/consultations/cancel` | Cancel Clinical Consultation Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-CONSULT-010** | `POST` | `/api/v1/consultations/verify` | Verify Clinical Consultation Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-CONSULT-011** | `GET` | `/api/v1/consultations/export` | Export Clinical Consultation Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-CONSULT-012** | `GET` | `/api/v1/consultations/{consultationId}/metrics` | Metrics Clinical Consultation Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-CONSULT-013** | `POST` | `/api/v1/consultations/reconcile` | Reconcile Clinical Consultation Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-CONSULT-014** | `POST` | `/api/v1/consultations/batch` | Batch Clinical Consultation Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-CONSULT-015** | `GET` | `/api/v1/consultations/sync` | Sync Clinical Consultation Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-CONSULT-016** | `GET` | `/api/v1/consultations/{consultationId}/alerts` | Alerts Clinical Consultation Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-CONSULT-017** | `POST` | `/api/v1/consultations/escalate` | Escalate Clinical Consultation Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-CONSULT-018** | `POST` | `/api/v1/consultations/approve` | Approve Clinical Consultation Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-CONSULT-019** | `POST` | `/api/v1/consultations/reversal` | Reversal Clinical Consultation Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-CONSULT-020** | `GET` | `/api/v1/consultations/{consultationId}/items` | Items Clinical Consultation Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-CONSULT-021** | `GET` | `/api/v1/consultations/documents` | Documents Clinical Consultation Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-CONSULT-022** | `GET` | `/api/v1/consultations/{consultationId}/timeline` | Timeline Clinical Consultation Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-CONSULT-023** | `GET` | `/api/v1/consultations/stats` | Stats Clinical Consultation Workflow Operation | `ROLE-002` | Read-Only Idempotent |

## 6. Comprehensive Endpoint Technical Specifications

Exhaustive technical contracts for all 23 endpoints in the `Consultation` domain:

### 6.1 `API-CONSULT-001`: Create New Clinical Consultation Record

- **API Identifier:** `API-CONSULT-001`
- **HTTP Route:** `POST /api/v1/consultations`
- **Functional Purpose:** Authoritative specification for create new clinical consultation record within Consultation operations.
- **Product Capability:** `CAPABILITY-084` | **Feature Code:** `FEATURE-084`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:post`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-024, SRS-NFR-004` | **Workflow:** `WF-009`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-024`
- **Planned Verification Test Case:** `PLANNED-TEST-API-083`
- **Dependency DAG Edge:** `API-DEP-024`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations:
    post:
      summary: "Create New Clinical Consultation Record"
      tags:
        - "Consultation"
      operationId: "post_api_v1_consultations"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations" \
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
  "operation": "Create New Clinical Consultation Record",
  "domain": "Consultation",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-CONSULT-001"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-001",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-001.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-024` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-083` under simulated offline network conditions.

### 6.2 `API-CONSULT-002`: Retrieve Clinical Consultation Details by ID

- **API Identifier:** `API-CONSULT-002`
- **HTTP Route:** `GET /api/v1/consultations/{consultationId}`
- **Functional Purpose:** Authoritative specification for retrieve clinical consultation details by id within Consultation operations.
- **Product Capability:** `CAPABILITY-085` | **Feature Code:** `FEATURE-085`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:get`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-025, SRS-NFR-005` | **Workflow:** `WF-010`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-025`
- **Planned Verification Test Case:** `PLANNED-TEST-API-084`
- **Dependency DAG Edge:** `API-DEP-025`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/{consultationId}:
    get:
      summary: "Retrieve Clinical Consultation Details by ID"
      tags:
        - "Consultation"
      operationId: "get_api_v1_consultations_consultationId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/{consultationId}" \
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
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-002",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-002.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-025` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-084` under simulated offline network conditions.

### 6.3 `API-CONSULT-003`: List and Filter Clinical Consultation Records

- **API Identifier:** `API-CONSULT-003`
- **HTTP Route:** `GET /api/v1/consultations`
- **Functional Purpose:** Authoritative specification for list and filter clinical consultation records within Consultation operations.
- **Product Capability:** `CAPABILITY-086` | **Feature Code:** `FEATURE-086`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:get`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-026, SRS-NFR-006` | **Workflow:** `WF-011`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-026`
- **Planned Verification Test Case:** `PLANNED-TEST-API-085`
- **Dependency DAG Edge:** `API-DEP-026`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations:
    get:
      summary: "List and Filter Clinical Consultation Records"
      tags:
        - "Consultation"
      operationId: "get_api_v1_consultations"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations" \
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
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-003",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-003.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-026` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-085` under simulated offline network conditions.

### 6.4 `API-CONSULT-004`: Update Full Clinical Consultation Specification

- **API Identifier:** `API-CONSULT-004`
- **HTTP Route:** `PUT /api/v1/consultations/{consultationId}`
- **Functional Purpose:** Authoritative specification for update full clinical consultation specification within Consultation operations.
- **Product Capability:** `CAPABILITY-087` | **Feature Code:** `FEATURE-087`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:put`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-027, SRS-NFR-007` | **Workflow:** `WF-012`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-027`
- **Planned Verification Test Case:** `PLANNED-TEST-API-086`
- **Dependency DAG Edge:** `API-DEP-027`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/{consultationId}:
    put:
      summary: "Update Full Clinical Consultation Specification"
      tags:
        - "Consultation"
      operationId: "put_api_v1_consultations_consultationId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/{consultationId}" \
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
  "operation": "Update Full Clinical Consultation Specification",
  "domain": "Consultation",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-CONSULT-004"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-004",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-004.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-027` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-086` under simulated offline network conditions.

### 6.5 `API-CONSULT-005`: Update Clinical Consultation Operational State

- **API Identifier:** `API-CONSULT-005`
- **HTTP Route:** `PATCH /api/v1/consultations/{consultationId}/status`
- **Functional Purpose:** Authoritative specification for update clinical consultation operational state within Consultation operations.
- **Product Capability:** `CAPABILITY-088` | **Feature Code:** `FEATURE-088`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:patch`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-028, SRS-NFR-008` | **Workflow:** `WF-013`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-028`
- **Planned Verification Test Case:** `PLANNED-TEST-API-087`
- **Dependency DAG Edge:** `API-DEP-028`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/{consultationId}/status:
    patch:
      summary: "Update Clinical Consultation Operational State"
      tags:
        - "Consultation"
      operationId: "patch_api_v1_consultations_consultationId_status"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/{consultationId}/status" \
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
  "operation": "Update Clinical Consultation Operational State",
  "domain": "Consultation",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-CONSULT-005"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-005",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-005.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-028` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-087` under simulated offline network conditions.

### 6.6 `API-CONSULT-006`: Search Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-006`
- **HTTP Route:** `GET /api/v1/consultations/{consultationId}/search`
- **Functional Purpose:** Authoritative specification for search clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-089` | **Feature Code:** `FEATURE-089`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:get`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-029, SRS-NFR-009` | **Workflow:** `WF-014`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-029`
- **Planned Verification Test Case:** `PLANNED-TEST-API-088`
- **Dependency DAG Edge:** `API-DEP-029`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/{consultationId}/search:
    get:
      summary: "Search Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "get_api_v1_consultations_consultationId_search"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/{consultationId}/search" \
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
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-006",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-006.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-029` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-088` under simulated offline network conditions.

### 6.7 `API-CONSULT-007`: History Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-007`
- **HTTP Route:** `GET /api/v1/consultations/history`
- **Functional Purpose:** Authoritative specification for history clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-090` | **Feature Code:** `FEATURE-090`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:get`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-030, SRS-NFR-010` | **Workflow:** `WF-015`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-030`
- **Planned Verification Test Case:** `PLANNED-TEST-API-089`
- **Dependency DAG Edge:** `API-DEP-030`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/history:
    get:
      summary: "History Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "get_api_v1_consultations_history"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/history" \
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
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-007",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-007.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-030` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-089` under simulated offline network conditions.

### 6.8 `API-CONSULT-008`: Audit Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-008`
- **HTTP Route:** `GET /api/v1/consultations/{consultationId}/audit`
- **Functional Purpose:** Authoritative specification for audit clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-091` | **Feature Code:** `FEATURE-091`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:get`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-031, SRS-NFR-011` | **Workflow:** `WF-016`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-001`
- **Planned Verification Test Case:** `PLANNED-TEST-API-090`
- **Dependency DAG Edge:** `API-DEP-031`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/{consultationId}/audit:
    get:
      summary: "Audit Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "get_api_v1_consultations_consultationId_audit"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/{consultationId}/audit" \
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
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-008",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-008.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-001` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-090` under simulated offline network conditions.

### 6.9 `API-CONSULT-009`: Cancel Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-009`
- **HTTP Route:** `POST /api/v1/consultations/cancel`
- **Functional Purpose:** Authoritative specification for cancel clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-092` | **Feature Code:** `FEATURE-092`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:post`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-032, SRS-NFR-012` | **Workflow:** `WF-017`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-002`
- **Planned Verification Test Case:** `PLANNED-TEST-API-091`
- **Dependency DAG Edge:** `API-DEP-032`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/cancel:
    post:
      summary: "Cancel Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "post_api_v1_consultations_cancel"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/cancel" \
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
  "operation": "Cancel Clinical Consultation Workflow Operation",
  "domain": "Consultation",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-CONSULT-009"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-009",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-009.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-002` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-091` under simulated offline network conditions.

### 6.10 `API-CONSULT-010`: Verify Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-010`
- **HTTP Route:** `POST /api/v1/consultations/verify`
- **Functional Purpose:** Authoritative specification for verify clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-093` | **Feature Code:** `FEATURE-093`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:post`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-033, SRS-NFR-013` | **Workflow:** `WF-018`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-003`
- **Planned Verification Test Case:** `PLANNED-TEST-API-092`
- **Dependency DAG Edge:** `API-DEP-033`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/verify:
    post:
      summary: "Verify Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "post_api_v1_consultations_verify"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/verify" \
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
  "operation": "Verify Clinical Consultation Workflow Operation",
  "domain": "Consultation",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-CONSULT-010"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-010",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-010.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-003` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-092` under simulated offline network conditions.

### 6.11 `API-CONSULT-011`: Export Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-011`
- **HTTP Route:** `GET /api/v1/consultations/export`
- **Functional Purpose:** Authoritative specification for export clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-094` | **Feature Code:** `FEATURE-094`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:get`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-034, SRS-NFR-014` | **Workflow:** `WF-019`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-004`
- **Planned Verification Test Case:** `PLANNED-TEST-API-093`
- **Dependency DAG Edge:** `API-DEP-034`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/export:
    get:
      summary: "Export Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "get_api_v1_consultations_export"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/export" \
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
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-011",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-011.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-004` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-093` under simulated offline network conditions.

### 6.12 `API-CONSULT-012`: Metrics Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-012`
- **HTTP Route:** `GET /api/v1/consultations/{consultationId}/metrics`
- **Functional Purpose:** Authoritative specification for metrics clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-095` | **Feature Code:** `FEATURE-095`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:get`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-035, SRS-NFR-015` | **Workflow:** `WF-020`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-005`
- **Planned Verification Test Case:** `PLANNED-TEST-API-094`
- **Dependency DAG Edge:** `API-DEP-035`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/{consultationId}/metrics:
    get:
      summary: "Metrics Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "get_api_v1_consultations_consultationId_metrics"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/{consultationId}/metrics" \
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
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-012",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-012.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-005` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-094` under simulated offline network conditions.

### 6.13 `API-CONSULT-013`: Reconcile Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-013`
- **HTTP Route:** `POST /api/v1/consultations/reconcile`
- **Functional Purpose:** Authoritative specification for reconcile clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-096` | **Feature Code:** `FEATURE-096`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:post`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-036, SRS-NFR-016` | **Workflow:** `WF-021`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-006`
- **Planned Verification Test Case:** `PLANNED-TEST-API-095`
- **Dependency DAG Edge:** `API-DEP-036`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/reconcile:
    post:
      summary: "Reconcile Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "post_api_v1_consultations_reconcile"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/reconcile" \
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
  "operation": "Reconcile Clinical Consultation Workflow Operation",
  "domain": "Consultation",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-CONSULT-013"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-013",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-013.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-006` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-095` under simulated offline network conditions.

### 6.14 `API-CONSULT-014`: Batch Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-014`
- **HTTP Route:** `POST /api/v1/consultations/batch`
- **Functional Purpose:** Authoritative specification for batch clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-097` | **Feature Code:** `FEATURE-097`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:post`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-037, SRS-NFR-017` | **Workflow:** `WF-022`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-007`
- **Planned Verification Test Case:** `PLANNED-TEST-API-096`
- **Dependency DAG Edge:** `API-DEP-037`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/batch:
    post:
      summary: "Batch Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "post_api_v1_consultations_batch"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/batch" \
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
  "operation": "Batch Clinical Consultation Workflow Operation",
  "domain": "Consultation",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-CONSULT-014"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-014",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-014.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-007` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-096` under simulated offline network conditions.

### 6.15 `API-CONSULT-015`: Sync Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-015`
- **HTTP Route:** `GET /api/v1/consultations/sync`
- **Functional Purpose:** Authoritative specification for sync clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-098` | **Feature Code:** `FEATURE-098`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:get`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-038, SRS-NFR-018` | **Workflow:** `WF-023`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-008`
- **Planned Verification Test Case:** `PLANNED-TEST-API-097`
- **Dependency DAG Edge:** `API-DEP-038`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/sync:
    get:
      summary: "Sync Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "get_api_v1_consultations_sync"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/sync" \
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
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-015",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-015.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-008` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-097` under simulated offline network conditions.

### 6.16 `API-CONSULT-016`: Alerts Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-016`
- **HTTP Route:** `GET /api/v1/consultations/{consultationId}/alerts`
- **Functional Purpose:** Authoritative specification for alerts clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-099` | **Feature Code:** `FEATURE-099`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:get`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-039, SRS-NFR-019` | **Workflow:** `WF-024`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-009`
- **Planned Verification Test Case:** `PLANNED-TEST-API-098`
- **Dependency DAG Edge:** `API-DEP-039`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/{consultationId}/alerts:
    get:
      summary: "Alerts Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "get_api_v1_consultations_consultationId_alerts"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/{consultationId}/alerts" \
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
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-016",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-016.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-009` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-098` under simulated offline network conditions.

### 6.17 `API-CONSULT-017`: Escalate Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-017`
- **HTTP Route:** `POST /api/v1/consultations/escalate`
- **Functional Purpose:** Authoritative specification for escalate clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-100` | **Feature Code:** `FEATURE-100`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:post`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-040, SRS-NFR-020` | **Workflow:** `WF-025`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-010`
- **Planned Verification Test Case:** `PLANNED-TEST-API-099`
- **Dependency DAG Edge:** `API-DEP-040`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/escalate:
    post:
      summary: "Escalate Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "post_api_v1_consultations_escalate"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/escalate" \
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
  "operation": "Escalate Clinical Consultation Workflow Operation",
  "domain": "Consultation",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-CONSULT-017"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-017",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-017.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-010` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-099` under simulated offline network conditions.

### 6.18 `API-CONSULT-018`: Approve Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-018`
- **HTTP Route:** `POST /api/v1/consultations/approve`
- **Functional Purpose:** Authoritative specification for approve clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-101` | **Feature Code:** `FEATURE-101`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:post`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-041, SRS-NFR-021` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-011`
- **Planned Verification Test Case:** `PLANNED-TEST-API-100`
- **Dependency DAG Edge:** `API-DEP-041`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/approve:
    post:
      summary: "Approve Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "post_api_v1_consultations_approve"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/approve" \
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
  "operation": "Approve Clinical Consultation Workflow Operation",
  "domain": "Consultation",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-CONSULT-018"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-018",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-018.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-011` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-100` under simulated offline network conditions.

### 6.19 `API-CONSULT-019`: Reversal Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-019`
- **HTTP Route:** `POST /api/v1/consultations/reversal`
- **Functional Purpose:** Authoritative specification for reversal clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-102` | **Feature Code:** `FEATURE-102`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:post`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-042, SRS-NFR-022` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-012`
- **Planned Verification Test Case:** `PLANNED-TEST-API-101`
- **Dependency DAG Edge:** `API-DEP-042`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/reversal:
    post:
      summary: "Reversal Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "post_api_v1_consultations_reversal"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/reversal" \
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
  "operation": "Reversal Clinical Consultation Workflow Operation",
  "domain": "Consultation",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-CONSULT-019"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-019",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-019.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-012` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-101` under simulated offline network conditions.

### 6.20 `API-CONSULT-020`: Items Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-020`
- **HTTP Route:** `GET /api/v1/consultations/{consultationId}/items`
- **Functional Purpose:** Authoritative specification for items clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-103` | **Feature Code:** `FEATURE-103`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:get`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-043, SRS-NFR-023` | **Workflow:** `WF-003`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-013`
- **Planned Verification Test Case:** `PLANNED-TEST-API-102`
- **Dependency DAG Edge:** `API-DEP-043`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/{consultationId}/items:
    get:
      summary: "Items Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "get_api_v1_consultations_consultationId_items"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/{consultationId}/items" \
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
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-020",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-020.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-013` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-102` under simulated offline network conditions.

### 6.21 `API-CONSULT-021`: Documents Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-021`
- **HTTP Route:** `GET /api/v1/consultations/documents`
- **Functional Purpose:** Authoritative specification for documents clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-104` | **Feature Code:** `FEATURE-104`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:get`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-044, SRS-NFR-024` | **Workflow:** `WF-004`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-014`
- **Planned Verification Test Case:** `PLANNED-TEST-API-103`
- **Dependency DAG Edge:** `API-DEP-044`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/documents:
    get:
      summary: "Documents Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "get_api_v1_consultations_documents"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/documents" \
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
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-021",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-021.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-014` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-103` under simulated offline network conditions.

### 6.22 `API-CONSULT-022`: Timeline Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-022`
- **HTTP Route:** `GET /api/v1/consultations/{consultationId}/timeline`
- **Functional Purpose:** Authoritative specification for timeline clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-105` | **Feature Code:** `FEATURE-105`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:get`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-045, SRS-NFR-025` | **Workflow:** `WF-005`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-015`
- **Planned Verification Test Case:** `PLANNED-TEST-API-104`
- **Dependency DAG Edge:** `API-DEP-045`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/{consultationId}/timeline:
    get:
      summary: "Timeline Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "get_api_v1_consultations_consultationId_timeline"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/{consultationId}/timeline" \
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
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-022",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-022.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-015` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-104` under simulated offline network conditions.

### 6.23 `API-CONSULT-023`: Stats Clinical Consultation Workflow Operation

- **API Identifier:** `API-CONSULT-023`
- **HTTP Route:** `GET /api/v1/consultations/stats`
- **Functional Purpose:** Authoritative specification for stats clinical consultation workflow operation within Consultation operations.
- **Product Capability:** `CAPABILITY-106` | **Feature Code:** `FEATURE-106`
- **Primary Actor:** Authorized Consultation Operator | **User Persona:** Consultation Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `consultations:get`
- **ABAC Scoping Rule:** Restricted to authorized Consultation personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-046, SRS-NFR-026` | **Workflow:** `WF-006`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, clinical_notes, diagnoses`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-016`
- **Planned Verification Test Case:** `PLANNED-TEST-API-105`
- **Dependency DAG Edge:** `API-DEP-046`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/consultations/stats:
    get:
      summary: "Stats Clinical Consultation Workflow Operation"
      tags:
        - "Consultation"
      operationId: "get_api_v1_consultations_stats"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/consultations/stats" \
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
    "type": "consultation",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-CONSULT-023",
      "domain": "Consultation",
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
    "code": "ERR-CONSULT-001",
    "message": "Domain constraint validation failed during execution of API-CONSULT-023.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, clinical_notes, diagnoses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-016` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-105` under simulated offline network conditions.

## 7. Domain-Specific Error Code Catalog & Troubleshooting Runbooks

The following standardized error codes are specifically emitted by `Consultation` services:

| Error Code ID | HTTP Status | Machine Code | Message Summary | Retryable | Resolution Runbook |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-CONSULT-001** | `HTTP 404` | `CONSULT_NOT_FOUND` | Clinical encounter progress note not found. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-CONSULT-001. |
| **ERR-CONSULT-002** | `HTTP 403` | `CONSULT_DOCTOR_PRIMACY_VIOLATION` | Only licensed medical officers may create or finalize consultation notes. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-CONSULT-002. |
| **ERR-CONSULT-003** | `HTTP 400` | `CONSULT_CHIEF_COMPLAINT_EMPTY` | At least one chief complaint symptom is mandatory. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-CONSULT-003. |
| **ERR-CONSULT-004** | `HTTP 400` | `CONSULT_DIAGNOSIS_CODE_INVALID` | Provisional diagnosis must reference a valid WHO ICD-10 code. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-CONSULT-004. |
| **ERR-CONSULT-005** | `HTTP 409` | `CONSULT_ALREADY_CLOSED` | Consultation encounter has been finalized. Modifications require formal addendum. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-CONSULT-005. |
| **ERR-CONSULT-006** | `HTTP 400` | `CONSULT_TRIAGE_PENDING` | Patient must complete nursing triage assessment prior to doctor consultation. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-CONSULT-006. |
| **ERR-CONSULT-007** | `HTTP 400` | `CONSULT_ADDENDUM_REASON_EMPTY` | Clinical reason for post-closure note addendum is mandatory. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-CONSULT-007. |
| **ERR-CONSULT-008** | `HTTP 403` | `CONSULT_ATTENDING_MISMATCH` | Only the attending clinician who opened the encounter may submit notes. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-CONSULT-008. |
| **ERR-CONSULT-009** | `HTTP 400` | `CONSULT_FOLLOWUP_DATE_PAST` | Follow-up appointment date cannot be prior to today. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-CONSULT-009. |
| **ERR-CONSULT-010** | `HTTP 500` | `CONSULT_CDSS_ADVISORY_TIMEOUT` | Clinical decision support advisory suggestion microservice timed out. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-CONSULT-010. |

## 8. Offline Edge Operation & Synchronization Mechanics

When WAN connectivity to the central cloud is disrupted, `Consultation` operations transition to autonomous edge mode:
1. **Local SQLite WAL Database:** Transactions are committed locally to `/data/namma_clinic_edge.db` on the clinic's Intel N100 mini-server.
2. **Offline Mutation Journal:** Every INSERT, UPDATE, and SOFT_DELETE appends a record to the `offline_mutation_log` table with a local vector clock.
3. **Conflict Resolution Policy:** Upon WAN restoration, the edge sync agent uploads buffered mutations in batches of 100 to `/api/v1/system/sync/batch`. Conflicts are resolved deterministically using Last-Write-Wins (LWW) with microsecond Lamport timestamps, except for clinical records where doctor entries take precedence over clerical updates.
4. **Storage Quotas:** Up to 72 hours of offline operations (approximately 15,000 mutations) can be buffered without storage degradation.

## 9. Security, Data Protection & DPDP Act Compliance

Data protection invariants for `Consultation` operations:

| Data Element | Classification | Encryption Standard | Masking Rule | DPDP Act Section | Retention Schedule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Core Entity Record | `CONFIDENTIAL` | AES-256-GCM Column Level | Masked on non-admin UI | Section 8 (Data Security) | 10 Years (Medical Records) |
| Transaction Mutation | INTERNAL | TLS 1.3 in Transit | Zero PII in Gateway Logs | Section 6 (Consent Notice) | 10 Years (Audit Ledger) |
| WORM Audit Log | HIGHLY-RESTRICTED | HMAC SHA-256 Chained | Full Hash Ledger | Section 12 (Citizen Rights) | Permanent (Statutory Archive) |

## 10. Domain Quality Acceptance Criteria (BDD)

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify Successful Execution of Create New Clinical Consultation Record
  Given an authenticated staff member with role 'ROLE-002'
  And an active clinical shift rostered in clinic facility '018e3a20-0008-7000-8000-000000000001'
  When the client sends a valid request to /api/v1/consultations
  Then the server processes the request within 1500ms
  And returns HTTP 201
  And the response conforms to envelope schema 'StandardApiResponseEnvelope'
  And an immutable audit log is appended to 'AUDIT-EVENT-024'
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Reject Unauthorized Call to Create New Clinical Consultation Record
  Given a caller presenting an invalid or expired Bearer token
  And requesting protected resource access
  When the caller transmits a request to /api/v1/consultations
  Then the API gateway intercepts the request
  And returns HTTP 401 Unauthorized
  And returns error code 'ERR-AUTH-002' or 'ERR-AUTH-003'
  And rejects access before invoking backend services
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Execute Create New Clinical Consultation Record in Autonomous Edge Mode
  Given the clinic workstation has lost WAN connectivity to cloud
  And the local edge mini-server is operational with local SQLite database
  When the staff member executes Create New Clinical Consultation Record
  Then the edge API gateway accepts the request locally
  And returns HTTP 201 within 250ms
  And appends the mutation to the local offline sync journal
  And synchronizes to cloud automatically upon network restoration
```

## 11. Requirements & Database Relational Traceability Matrix

Traceability mapping for all `Consultation` endpoints:

| Endpoint ID | Upstream SRS Requirements | Workflow ID | Feature Code | Target Database Tables | Verification Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `API-CONSULT-001` | `SRS-FR-024, SRS-NFR-004` | `WF-009` | `FEATURE-084` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-083` |
| `API-CONSULT-002` | `SRS-FR-025, SRS-NFR-005` | `WF-010` | `FEATURE-085` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-084` |
| `API-CONSULT-003` | `SRS-FR-026, SRS-NFR-006` | `WF-011` | `FEATURE-086` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-085` |
| `API-CONSULT-004` | `SRS-FR-027, SRS-NFR-007` | `WF-012` | `FEATURE-087` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-086` |
| `API-CONSULT-005` | `SRS-FR-028, SRS-NFR-008` | `WF-013` | `FEATURE-088` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-087` |
| `API-CONSULT-006` | `SRS-FR-029, SRS-NFR-009` | `WF-014` | `FEATURE-089` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-088` |
| `API-CONSULT-007` | `SRS-FR-030, SRS-NFR-010` | `WF-015` | `FEATURE-090` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-089` |
| `API-CONSULT-008` | `SRS-FR-031, SRS-NFR-011` | `WF-016` | `FEATURE-091` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-090` |
| `API-CONSULT-009` | `SRS-FR-032, SRS-NFR-012` | `WF-017` | `FEATURE-092` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-091` |
| `API-CONSULT-010` | `SRS-FR-033, SRS-NFR-013` | `WF-018` | `FEATURE-093` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-092` |
| `API-CONSULT-011` | `SRS-FR-034, SRS-NFR-014` | `WF-019` | `FEATURE-094` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-093` |
| `API-CONSULT-012` | `SRS-FR-035, SRS-NFR-015` | `WF-020` | `FEATURE-095` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-094` |
| `API-CONSULT-013` | `SRS-FR-036, SRS-NFR-016` | `WF-021` | `FEATURE-096` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-095` |
| `API-CONSULT-014` | `SRS-FR-037, SRS-NFR-017` | `WF-022` | `FEATURE-097` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-096` |
| `API-CONSULT-015` | `SRS-FR-038, SRS-NFR-018` | `WF-023` | `FEATURE-098` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-097` |
| `API-CONSULT-016` | `SRS-FR-039, SRS-NFR-019` | `WF-024` | `FEATURE-099` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-098` |
| `API-CONSULT-017` | `SRS-FR-040, SRS-NFR-020` | `WF-025` | `FEATURE-100` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-099` |
| `API-CONSULT-018` | `SRS-FR-041, SRS-NFR-021` | `WF-001` | `FEATURE-101` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-100` |
| `API-CONSULT-019` | `SRS-FR-042, SRS-NFR-022` | `WF-002` | `FEATURE-102` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-101` |
| `API-CONSULT-020` | `SRS-FR-043, SRS-NFR-023` | `WF-003` | `FEATURE-103` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-102` |
| `API-CONSULT-021` | `SRS-FR-044, SRS-NFR-024` | `WF-004` | `FEATURE-104` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-103` |
| `API-CONSULT-022` | `SRS-FR-045, SRS-NFR-025` | `WF-005` | `FEATURE-105` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-104` |
| `API-CONSULT-023` | `SRS-FR-046, SRS-NFR-026` | `WF-006` | `FEATURE-106` | `clinical_encounters, clinical_notes, diagnoses` | `PLANNED-TEST-API-105` |
