# 🔌 API Specification: Electronic Prescription & Formulary Governance API Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-09 | **Status:** Authoritative Baseline | **Date:** September 2026
> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Standard Framework:** RFC 7231 (HTTP/1.1), JSON:API v1.1, DPDP Act 2023, ABDM Interoperability Standards
> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.

---

## 1. Executive Summary & Domain Scope

The **Electronic Prescription & Formulary Governance API Specification** defines the authoritative, implementation-ready contracts for the `Prescription` subsystem across all 183 Namma Clinic primary healthcare centers in Greater Bengaluru. This domain operates under the supervisory jurisdiction of `ROLE-002 (Prescribing Medical Officer)` and fulfills the core mission: **Manage digital prescription authoring, BBMP essential drugs formulary validation, drug-drug and drug-allergy interaction checking, pediatric dosage safety, and bilingual slip generation.**

All 19 endpoints specified in this document adhere strictly to uniform JSON:API response envelopes, time-ordered UUIDv7 identifiers, ISO-8601 UTC timestamps, optimistic concurrency control via ETags, and automated audit logging.

## 2. Operational Architecture & Relational Mapping

The following table maps the domain's operational context to architectural containers, components, database tables, and default role entitlements:

| Dimension | Specification Detail |
| :--- | :--- |
| **Functional Domain** | `Prescription` (Code: `RX`) |
| **Authoritative Endpoints** | 19 Active Endpoints (`API-RX-001` to `API-RX-019`) |
| **Primary Architecture Container** | `ARCH-CONT-008` |
| **Assigned Component** | `ARCH-COMP-022` |
| **Primary Database Tables** | `prescriptions, prescription_items, formulary_drugs` |
| **Lead Role Entitlement** | `ROLE-002 (Prescribing Medical Officer)` |
| **Default Rate Limiting** | `60 req/min per User` |
| **Offline Edge Support** | `Edge Local Queue with Delta Sync` |

## 3. Domain Operational State Machine

The operational state transitions governing entities within this domain are modeled below:

```mermaid
stateDiagram-v2
    [*] --> DraftRegimen: Doctor Adds Formulary Medicines
    DraftRegimen --> InteractionCheck: CDSS Evaluates Contraindications
    InteractionCheck --> WarningFlagged: Drug Interaction Detected
    WarningFlagged --> OverrideJustified: Clinician Records Justification
    WarningFlagged --> DrugReplaced: Clinician Selects Alternate Drug
    InteractionCheck --> Validated: No Interactions Found
    Validated --> Signed: Digital Cryptographic Signature Applied
    Signed --> Transmitted: Sent to Clinic Dispensary Queue
    Transmitted --> Dispensed: Pharmacist Issues Medication
    Signed --> Cancelled: Cancelled prior to Dispensing
    Dispensed --> [*]
```

## 4. End-to-End Operational Data Flow

The sequence diagram below illustrates the end-to-end operational flow between frontline clinic staff, edge workstations, the central API gateway, and backing data stores:

```mermaid
sequenceDiagram
    autonumber
    participant Doc as Treating Physician
    participant UI as Prescription PWA
    participant API as Prescription API
    participant CDSS as CDSS Interaction Engine
    participant DB as Pharmacy DB
    Doc->>UI: Prescribe Paracetamol 500mg TDS x 5 days
    UI->>API: POST /api/v1/prescriptions
    API->>CDSS: Check Active Patient Regimens
    CDSS-->>API: Zero Adverse Interactions
    API->>DB: Insert Prescription & Items with HMAC Signature
    API-->>UI: HTTP 201 Created (Prescription Signed)
    UI-->>Doc: Display Printable Slip (Kannada + English)
```

## 5. Domain Endpoint Inventory Catalog

Complete inventory of all 19 endpoints defined for the `Prescription` domain:

| Endpoint ID | Method | URI Route Path | Functional Title | Role Context | Idempotency Standard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API-RX-001** | `POST` | `/api/v1/prescriptions` | Create New Electronic Prescription Record | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-RX-002** | `GET` | `/api/v1/prescriptions/{prescriptionId}` | Retrieve Electronic Prescription Details by ID | `ROLE-002` | Read-Only Idempotent |
| **API-RX-003** | `GET` | `/api/v1/prescriptions` | List and Filter Electronic Prescription Records | `ROLE-002` | Read-Only Idempotent |
| **API-RX-004** | `PUT` | `/api/v1/prescriptions/{prescriptionId}` | Update Full Electronic Prescription Specification | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-RX-005** | `PATCH` | `/api/v1/prescriptions/{prescriptionId}/status` | Update Electronic Prescription Operational State | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-RX-006** | `GET` | `/api/v1/prescriptions/{prescriptionId}/search` | Search Electronic Prescription Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-RX-007** | `GET` | `/api/v1/prescriptions/history` | History Electronic Prescription Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-RX-008** | `GET` | `/api/v1/prescriptions/{prescriptionId}/audit` | Audit Electronic Prescription Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-RX-009** | `POST` | `/api/v1/prescriptions/cancel` | Cancel Electronic Prescription Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-RX-010** | `POST` | `/api/v1/prescriptions/verify` | Verify Electronic Prescription Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-RX-011** | `GET` | `/api/v1/prescriptions/export` | Export Electronic Prescription Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-RX-012** | `GET` | `/api/v1/prescriptions/{prescriptionId}/metrics` | Metrics Electronic Prescription Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-RX-013** | `POST` | `/api/v1/prescriptions/reconcile` | Reconcile Electronic Prescription Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-RX-014** | `POST` | `/api/v1/prescriptions/batch` | Batch Electronic Prescription Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-RX-015** | `GET` | `/api/v1/prescriptions/sync` | Sync Electronic Prescription Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-RX-016** | `GET` | `/api/v1/prescriptions/{prescriptionId}/alerts` | Alerts Electronic Prescription Workflow Operation | `ROLE-002` | Read-Only Idempotent |
| **API-RX-017** | `POST` | `/api/v1/prescriptions/escalate` | Escalate Electronic Prescription Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-RX-018** | `POST` | `/api/v1/prescriptions/approve` | Approve Electronic Prescription Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-RX-019** | `POST` | `/api/v1/prescriptions/reversal` | Reversal Electronic Prescription Workflow Operation | `ROLE-002` | Supported via X-Idempotency-Key |

## 6. Comprehensive Endpoint Technical Specifications

Exhaustive technical contracts for all 19 endpoints in the `Prescription` domain:

### 6.1 `API-RX-001`: Create New Electronic Prescription Record

- **API Identifier:** `API-RX-001`
- **HTTP Route:** `POST /api/v1/prescriptions`
- **Functional Purpose:** Authoritative specification for create new electronic prescription record within Prescription operations.
- **Product Capability:** `CAPABILITY-107` | **Feature Code:** `FEATURE-107`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:post`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-047, SRS-NFR-027` | **Workflow:** `WF-007`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-017`
- **Planned Verification Test Case:** `PLANNED-TEST-API-106`
- **Dependency DAG Edge:** `API-DEP-047`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions:
    post:
      summary: "Create New Electronic Prescription Record"
      tags:
        - "Prescription"
      operationId: "post_api_v1_prescriptions"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions" \
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
  "operation": "Create New Electronic Prescription Record",
  "domain": "Prescription",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-RX-001"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-001",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-001.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-017` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-106` under simulated offline network conditions.

### 6.2 `API-RX-002`: Retrieve Electronic Prescription Details by ID

- **API Identifier:** `API-RX-002`
- **HTTP Route:** `GET /api/v1/prescriptions/{prescriptionId}`
- **Functional Purpose:** Authoritative specification for retrieve electronic prescription details by id within Prescription operations.
- **Product Capability:** `CAPABILITY-108` | **Feature Code:** `FEATURE-108`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:get`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-048, SRS-NFR-028` | **Workflow:** `WF-008`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-018`
- **Planned Verification Test Case:** `PLANNED-TEST-API-107`
- **Dependency DAG Edge:** `API-DEP-048`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/{prescriptionId}:
    get:
      summary: "Retrieve Electronic Prescription Details by ID"
      tags:
        - "Prescription"
      operationId: "get_api_v1_prescriptions_prescriptionId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/{prescriptionId}" \
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
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-002",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-002.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-018` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-107` under simulated offline network conditions.

### 6.3 `API-RX-003`: List and Filter Electronic Prescription Records

- **API Identifier:** `API-RX-003`
- **HTTP Route:** `GET /api/v1/prescriptions`
- **Functional Purpose:** Authoritative specification for list and filter electronic prescription records within Prescription operations.
- **Product Capability:** `CAPABILITY-109` | **Feature Code:** `FEATURE-109`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:get`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-049, SRS-NFR-029` | **Workflow:** `WF-009`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-019`
- **Planned Verification Test Case:** `PLANNED-TEST-API-108`
- **Dependency DAG Edge:** `API-DEP-049`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions:
    get:
      summary: "List and Filter Electronic Prescription Records"
      tags:
        - "Prescription"
      operationId: "get_api_v1_prescriptions"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions" \
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
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-003",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-003.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-019` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-108` under simulated offline network conditions.

### 6.4 `API-RX-004`: Update Full Electronic Prescription Specification

- **API Identifier:** `API-RX-004`
- **HTTP Route:** `PUT /api/v1/prescriptions/{prescriptionId}`
- **Functional Purpose:** Authoritative specification for update full electronic prescription specification within Prescription operations.
- **Product Capability:** `CAPABILITY-110` | **Feature Code:** `FEATURE-110`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:put`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-050, SRS-NFR-030` | **Workflow:** `WF-010`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-020`
- **Planned Verification Test Case:** `PLANNED-TEST-API-109`
- **Dependency DAG Edge:** `API-DEP-050`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/{prescriptionId}:
    put:
      summary: "Update Full Electronic Prescription Specification"
      tags:
        - "Prescription"
      operationId: "put_api_v1_prescriptions_prescriptionId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/{prescriptionId}" \
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
  "operation": "Update Full Electronic Prescription Specification",
  "domain": "Prescription",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-RX-004"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-004",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-004.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-020` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-109` under simulated offline network conditions.

### 6.5 `API-RX-005`: Update Electronic Prescription Operational State

- **API Identifier:** `API-RX-005`
- **HTTP Route:** `PATCH /api/v1/prescriptions/{prescriptionId}/status`
- **Functional Purpose:** Authoritative specification for update electronic prescription operational state within Prescription operations.
- **Product Capability:** `CAPABILITY-111` | **Feature Code:** `FEATURE-111`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:patch`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-051, SRS-NFR-031` | **Workflow:** `WF-011`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-021`
- **Planned Verification Test Case:** `PLANNED-TEST-API-110`
- **Dependency DAG Edge:** `API-DEP-051`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/{prescriptionId}/status:
    patch:
      summary: "Update Electronic Prescription Operational State"
      tags:
        - "Prescription"
      operationId: "patch_api_v1_prescriptions_prescriptionId_status"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/{prescriptionId}/status" \
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
  "operation": "Update Electronic Prescription Operational State",
  "domain": "Prescription",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-RX-005"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-005",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-005.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-021` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-110` under simulated offline network conditions.

### 6.6 `API-RX-006`: Search Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-006`
- **HTTP Route:** `GET /api/v1/prescriptions/{prescriptionId}/search`
- **Functional Purpose:** Authoritative specification for search electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-112` | **Feature Code:** `FEATURE-112`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:get`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-052, SRS-NFR-032` | **Workflow:** `WF-012`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-022`
- **Planned Verification Test Case:** `PLANNED-TEST-API-111`
- **Dependency DAG Edge:** `API-DEP-052`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/{prescriptionId}/search:
    get:
      summary: "Search Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "get_api_v1_prescriptions_prescriptionId_search"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/{prescriptionId}/search" \
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
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-006",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-006.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-022` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-111` under simulated offline network conditions.

### 6.7 `API-RX-007`: History Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-007`
- **HTTP Route:** `GET /api/v1/prescriptions/history`
- **Functional Purpose:** Authoritative specification for history electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-113` | **Feature Code:** `FEATURE-113`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:get`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-053, SRS-NFR-033` | **Workflow:** `WF-013`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-023`
- **Planned Verification Test Case:** `PLANNED-TEST-API-112`
- **Dependency DAG Edge:** `API-DEP-053`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/history:
    get:
      summary: "History Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "get_api_v1_prescriptions_history"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/history" \
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
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-007",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-007.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-023` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-112` under simulated offline network conditions.

### 6.8 `API-RX-008`: Audit Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-008`
- **HTTP Route:** `GET /api/v1/prescriptions/{prescriptionId}/audit`
- **Functional Purpose:** Authoritative specification for audit electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-114` | **Feature Code:** `FEATURE-114`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:get`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-054, SRS-NFR-034` | **Workflow:** `WF-014`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-024`
- **Planned Verification Test Case:** `PLANNED-TEST-API-113`
- **Dependency DAG Edge:** `API-DEP-054`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/{prescriptionId}/audit:
    get:
      summary: "Audit Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "get_api_v1_prescriptions_prescriptionId_audit"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/{prescriptionId}/audit" \
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
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-008",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-008.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-024` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-113` under simulated offline network conditions.

### 6.9 `API-RX-009`: Cancel Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-009`
- **HTTP Route:** `POST /api/v1/prescriptions/cancel`
- **Functional Purpose:** Authoritative specification for cancel electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-115` | **Feature Code:** `FEATURE-115`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:post`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-055, SRS-NFR-035` | **Workflow:** `WF-015`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-025`
- **Planned Verification Test Case:** `PLANNED-TEST-API-114`
- **Dependency DAG Edge:** `API-DEP-055`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/cancel:
    post:
      summary: "Cancel Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "post_api_v1_prescriptions_cancel"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/cancel" \
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
  "operation": "Cancel Electronic Prescription Workflow Operation",
  "domain": "Prescription",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-RX-009"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-009",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-009.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-025` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-114` under simulated offline network conditions.

### 6.10 `API-RX-010`: Verify Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-010`
- **HTTP Route:** `POST /api/v1/prescriptions/verify`
- **Functional Purpose:** Authoritative specification for verify electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-116` | **Feature Code:** `FEATURE-116`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:post`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-056, SRS-NFR-036` | **Workflow:** `WF-016`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-026`
- **Planned Verification Test Case:** `PLANNED-TEST-API-115`
- **Dependency DAG Edge:** `API-DEP-056`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/verify:
    post:
      summary: "Verify Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "post_api_v1_prescriptions_verify"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/verify" \
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
  "operation": "Verify Electronic Prescription Workflow Operation",
  "domain": "Prescription",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-RX-010"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-010",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-010.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-026` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-115` under simulated offline network conditions.

### 6.11 `API-RX-011`: Export Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-011`
- **HTTP Route:** `GET /api/v1/prescriptions/export`
- **Functional Purpose:** Authoritative specification for export electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-117` | **Feature Code:** `FEATURE-117`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:get`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-057, SRS-NFR-037` | **Workflow:** `WF-017`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-027`
- **Planned Verification Test Case:** `PLANNED-TEST-API-116`
- **Dependency DAG Edge:** `API-DEP-057`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/export:
    get:
      summary: "Export Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "get_api_v1_prescriptions_export"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/export" \
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
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-011",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-011.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-027` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-116` under simulated offline network conditions.

### 6.12 `API-RX-012`: Metrics Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-012`
- **HTTP Route:** `GET /api/v1/prescriptions/{prescriptionId}/metrics`
- **Functional Purpose:** Authoritative specification for metrics electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-118` | **Feature Code:** `FEATURE-118`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:get`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-058, SRS-NFR-038` | **Workflow:** `WF-018`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-028`
- **Planned Verification Test Case:** `PLANNED-TEST-API-117`
- **Dependency DAG Edge:** `API-DEP-058`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/{prescriptionId}/metrics:
    get:
      summary: "Metrics Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "get_api_v1_prescriptions_prescriptionId_metrics"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/{prescriptionId}/metrics" \
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
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-012",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-012.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-028` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-117` under simulated offline network conditions.

### 6.13 `API-RX-013`: Reconcile Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-013`
- **HTTP Route:** `POST /api/v1/prescriptions/reconcile`
- **Functional Purpose:** Authoritative specification for reconcile electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-119` | **Feature Code:** `FEATURE-119`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:post`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-059, SRS-NFR-039` | **Workflow:** `WF-019`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-029`
- **Planned Verification Test Case:** `PLANNED-TEST-API-118`
- **Dependency DAG Edge:** `API-DEP-059`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/reconcile:
    post:
      summary: "Reconcile Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "post_api_v1_prescriptions_reconcile"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/reconcile" \
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
  "operation": "Reconcile Electronic Prescription Workflow Operation",
  "domain": "Prescription",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-RX-013"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-013",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-013.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-029` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-118` under simulated offline network conditions.

### 6.14 `API-RX-014`: Batch Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-014`
- **HTTP Route:** `POST /api/v1/prescriptions/batch`
- **Functional Purpose:** Authoritative specification for batch electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-120` | **Feature Code:** `FEATURE-120`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:post`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-060, SRS-NFR-040` | **Workflow:** `WF-020`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-030`
- **Planned Verification Test Case:** `PLANNED-TEST-API-119`
- **Dependency DAG Edge:** `API-DEP-060`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/batch:
    post:
      summary: "Batch Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "post_api_v1_prescriptions_batch"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/batch" \
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
  "operation": "Batch Electronic Prescription Workflow Operation",
  "domain": "Prescription",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-RX-014"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-014",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-014.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-030` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-119` under simulated offline network conditions.

### 6.15 `API-RX-015`: Sync Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-015`
- **HTTP Route:** `GET /api/v1/prescriptions/sync`
- **Functional Purpose:** Authoritative specification for sync electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-121` | **Feature Code:** `FEATURE-121`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:get`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-001, SRS-NFR-001` | **Workflow:** `WF-021`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-001`
- **Planned Verification Test Case:** `PLANNED-TEST-API-120`
- **Dependency DAG Edge:** `API-DEP-001`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/sync:
    get:
      summary: "Sync Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "get_api_v1_prescriptions_sync"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/sync" \
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
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-015",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-015.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-001` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-120` under simulated offline network conditions.

### 6.16 `API-RX-016`: Alerts Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-016`
- **HTTP Route:** `GET /api/v1/prescriptions/{prescriptionId}/alerts`
- **Functional Purpose:** Authoritative specification for alerts electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-122` | **Feature Code:** `FEATURE-122`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:get`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-002, SRS-NFR-002` | **Workflow:** `WF-022`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-002`
- **Planned Verification Test Case:** `PLANNED-TEST-API-121`
- **Dependency DAG Edge:** `API-DEP-002`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/{prescriptionId}/alerts:
    get:
      summary: "Alerts Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "get_api_v1_prescriptions_prescriptionId_alerts"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/{prescriptionId}/alerts" \
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
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-016",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-016.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-002` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-121` under simulated offline network conditions.

### 6.17 `API-RX-017`: Escalate Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-017`
- **HTTP Route:** `POST /api/v1/prescriptions/escalate`
- **Functional Purpose:** Authoritative specification for escalate electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-123` | **Feature Code:** `FEATURE-123`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:post`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-003, SRS-NFR-003` | **Workflow:** `WF-023`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-003`
- **Planned Verification Test Case:** `PLANNED-TEST-API-122`
- **Dependency DAG Edge:** `API-DEP-003`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/escalate:
    post:
      summary: "Escalate Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "post_api_v1_prescriptions_escalate"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/escalate" \
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
  "operation": "Escalate Electronic Prescription Workflow Operation",
  "domain": "Prescription",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-RX-017"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-017",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-017.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-003` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-122` under simulated offline network conditions.

### 6.18 `API-RX-018`: Approve Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-018`
- **HTTP Route:** `POST /api/v1/prescriptions/approve`
- **Functional Purpose:** Authoritative specification for approve electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-124` | **Feature Code:** `FEATURE-124`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:post`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-004, SRS-NFR-004` | **Workflow:** `WF-024`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-004`
- **Planned Verification Test Case:** `PLANNED-TEST-API-123`
- **Dependency DAG Edge:** `API-DEP-004`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/approve:
    post:
      summary: "Approve Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "post_api_v1_prescriptions_approve"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/approve" \
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
  "operation": "Approve Electronic Prescription Workflow Operation",
  "domain": "Prescription",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-RX-018"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-018",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-018.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-004` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-123` under simulated offline network conditions.

### 6.19 `API-RX-019`: Reversal Electronic Prescription Workflow Operation

- **API Identifier:** `API-RX-019`
- **HTTP Route:** `POST /api/v1/prescriptions/reversal`
- **Functional Purpose:** Authoritative specification for reversal electronic prescription workflow operation within Prescription operations.
- **Product Capability:** `CAPABILITY-125` | **Feature Code:** `FEATURE-125`
- **Primary Actor:** Authorized Prescription Operator | **User Persona:** Prescription Care Team Persona
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescriptions:post`
- **ABAC Scoping Rule:** Restricted to authorized Prescription personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-005, SRS-NFR-005` | **Workflow:** `WF-025`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items, formulary_drugs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-005`
- **Planned Verification Test Case:** `PLANNED-TEST-API-124`
- **Dependency DAG Edge:** `API-DEP-005`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/prescriptions/reversal:
    post:
      summary: "Reversal Electronic Prescription Workflow Operation"
      tags:
        - "Prescription"
      operationId: "post_api_v1_prescriptions_reversal"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/prescriptions/reversal" \
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
  "operation": "Reversal Electronic Prescription Workflow Operation",
  "domain": "Prescription",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-RX-019"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "prescription",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-RX-019",
      "domain": "Prescription",
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
    "code": "ERR-RX-001",
    "message": "Domain constraint validation failed during execution of API-RX-019.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items, formulary_drugs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-005` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-124` under simulated offline network conditions.

## 7. Domain-Specific Error Code Catalog & Troubleshooting Runbooks

The following standardized error codes are specifically emitted by `Prescription` services:

| Error Code ID | HTTP Status | Machine Code | Message Summary | Retryable | Resolution Runbook |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-RX-001** | `HTTP 404` | `RX_NOT_FOUND` | Electronic prescription record does not exist. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-RX-001. |
| **ERR-RX-002** | `HTTP 400` | `RX_DRUG_NOT_IN_FORMULARY` | Prescribed medicine is not approved in BBMP Namma Clinic formulary. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-RX-002. |
| **ERR-RX-003** | `HTTP 400` | `RX_DOSAGE_OUT_OF_BOUNDS` | Prescribed dosage exceeds maximum recommended pediatric/adult limits. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-RX-003. |
| **ERR-RX-004** | `HTTP 409` | `RX_CONTRAINDICATION_DETECTED` | Severe drug-drug interaction or recorded patient allergy contraindication. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-RX-004. |
| **ERR-RX-005** | `HTTP 400` | `RX_DURATION_EXCEEDS_MAX` | Prescription duration exceeds statutory 90-day municipal limit. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-RX-005. |
| **ERR-RX-006** | `HTTP 409` | `RX_ALREADY_DISPENSED` | Prescription has already been dispensed by pharmacy and cannot be altered. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-RX-006. |
| **ERR-RX-007** | `HTTP 400` | `RX_EMPTY_ITEMS` | Prescription must contain at least one valid medication line item. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-RX-007. |
| **ERR-RX-008** | `HTTP 403` | `RX_PRESCRIBER_NOT_LICENSED` | Prescribing staff lacks active medical council registration (KMC). | No | Verify client request format, ensure active session, and inspect audit logs for ERR-RX-008. |
| **ERR-RX-009** | `HTTP 400` | `RX_QUANTITY_ZERO` | Quantity prescribed must be greater than zero. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-RX-009. |
| **ERR-RX-010** | `HTTP 500` | `RX_DIGITAL_SIGNATURE_FAILED` | Failed to generate cryptographic prescription integrity signature. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-RX-010. |

## 8. Offline Edge Operation & Synchronization Mechanics

When WAN connectivity to the central cloud is disrupted, `Prescription` operations transition to autonomous edge mode:
1. **Local SQLite WAL Database:** Transactions are committed locally to `/data/namma_clinic_edge.db` on the clinic's Intel N100 mini-server.
2. **Offline Mutation Journal:** Every INSERT, UPDATE, and SOFT_DELETE appends a record to the `offline_mutation_log` table with a local vector clock.
3. **Conflict Resolution Policy:** Upon WAN restoration, the edge sync agent uploads buffered mutations in batches of 100 to `/api/v1/system/sync/batch`. Conflicts are resolved deterministically using Last-Write-Wins (LWW) with microsecond Lamport timestamps, except for clinical records where doctor entries take precedence over clerical updates.
4. **Storage Quotas:** Up to 72 hours of offline operations (approximately 15,000 mutations) can be buffered without storage degradation.

## 9. Security, Data Protection & DPDP Act Compliance

Data protection invariants for `Prescription` operations:

| Data Element | Classification | Encryption Standard | Masking Rule | DPDP Act Section | Retention Schedule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Core Entity Record | `CONFIDENTIAL` | AES-256-GCM Column Level | Masked on non-admin UI | Section 8 (Data Security) | 10 Years (Medical Records) |
| Transaction Mutation | INTERNAL | TLS 1.3 in Transit | Zero PII in Gateway Logs | Section 6 (Consent Notice) | 10 Years (Audit Ledger) |
| WORM Audit Log | HIGHLY-RESTRICTED | HMAC SHA-256 Chained | Full Hash Ledger | Section 12 (Citizen Rights) | Permanent (Statutory Archive) |

## 10. Domain Quality Acceptance Criteria (BDD)

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify Successful Execution of Create New Electronic Prescription Record
  Given an authenticated staff member with role 'ROLE-002'
  And an active clinical shift rostered in clinic facility '018e3a20-0008-7000-8000-000000000001'
  When the client sends a valid request to /api/v1/prescriptions
  Then the server processes the request within 1500ms
  And returns HTTP 201
  And the response conforms to envelope schema 'StandardApiResponseEnvelope'
  And an immutable audit log is appended to 'AUDIT-EVENT-017'
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Reject Unauthorized Call to Create New Electronic Prescription Record
  Given a caller presenting an invalid or expired Bearer token
  And requesting protected resource access
  When the caller transmits a request to /api/v1/prescriptions
  Then the API gateway intercepts the request
  And returns HTTP 401 Unauthorized
  And returns error code 'ERR-AUTH-002' or 'ERR-AUTH-003'
  And rejects access before invoking backend services
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Execute Create New Electronic Prescription Record in Autonomous Edge Mode
  Given the clinic workstation has lost WAN connectivity to cloud
  And the local edge mini-server is operational with local SQLite database
  When the staff member executes Create New Electronic Prescription Record
  Then the edge API gateway accepts the request locally
  And returns HTTP 201 within 250ms
  And appends the mutation to the local offline sync journal
  And synchronizes to cloud automatically upon network restoration
```

## 11. Requirements & Database Relational Traceability Matrix

Traceability mapping for all `Prescription` endpoints:

| Endpoint ID | Upstream SRS Requirements | Workflow ID | Feature Code | Target Database Tables | Verification Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `API-RX-001` | `SRS-FR-047, SRS-NFR-027` | `WF-007` | `FEATURE-107` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-106` |
| `API-RX-002` | `SRS-FR-048, SRS-NFR-028` | `WF-008` | `FEATURE-108` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-107` |
| `API-RX-003` | `SRS-FR-049, SRS-NFR-029` | `WF-009` | `FEATURE-109` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-108` |
| `API-RX-004` | `SRS-FR-050, SRS-NFR-030` | `WF-010` | `FEATURE-110` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-109` |
| `API-RX-005` | `SRS-FR-051, SRS-NFR-031` | `WF-011` | `FEATURE-111` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-110` |
| `API-RX-006` | `SRS-FR-052, SRS-NFR-032` | `WF-012` | `FEATURE-112` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-111` |
| `API-RX-007` | `SRS-FR-053, SRS-NFR-033` | `WF-013` | `FEATURE-113` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-112` |
| `API-RX-008` | `SRS-FR-054, SRS-NFR-034` | `WF-014` | `FEATURE-114` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-113` |
| `API-RX-009` | `SRS-FR-055, SRS-NFR-035` | `WF-015` | `FEATURE-115` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-114` |
| `API-RX-010` | `SRS-FR-056, SRS-NFR-036` | `WF-016` | `FEATURE-116` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-115` |
| `API-RX-011` | `SRS-FR-057, SRS-NFR-037` | `WF-017` | `FEATURE-117` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-116` |
| `API-RX-012` | `SRS-FR-058, SRS-NFR-038` | `WF-018` | `FEATURE-118` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-117` |
| `API-RX-013` | `SRS-FR-059, SRS-NFR-039` | `WF-019` | `FEATURE-119` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-118` |
| `API-RX-014` | `SRS-FR-060, SRS-NFR-040` | `WF-020` | `FEATURE-120` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-119` |
| `API-RX-015` | `SRS-FR-001, SRS-NFR-001` | `WF-021` | `FEATURE-121` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-120` |
| `API-RX-016` | `SRS-FR-002, SRS-NFR-002` | `WF-022` | `FEATURE-122` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-121` |
| `API-RX-017` | `SRS-FR-003, SRS-NFR-003` | `WF-023` | `FEATURE-123` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-122` |
| `API-RX-018` | `SRS-FR-004, SRS-NFR-004` | `WF-024` | `FEATURE-124` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-123` |
| `API-RX-019` | `SRS-FR-005, SRS-NFR-005` | `WF-025` | `FEATURE-125` | `prescriptions, prescription_items, formulary_drugs` | `PLANNED-TEST-API-124` |
