# 🔌 API Specification: Dispensary Operations, FEFO Allocation & Dispensing API Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-10 | **Status:** Authoritative Baseline | **Date:** September 2026
> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Standard Framework:** RFC 7231 (HTTP/1.1), JSON:API v1.1, DPDP Act 2023, ABDM Interoperability Standards
> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.

---

## 1. Executive Summary & Domain Scope

The **Dispensary Operations, FEFO Allocation & Dispensing API Specification** defines the authoritative, implementation-ready contracts for the `Pharmacy` subsystem across all 183 Namma Clinic primary healthcare centers in Greater Bengaluru. This domain operates under the supervisory jurisdiction of `ROLE-017 (Registered Pharmacist)` and fulfills the core mission: **Execute prescription fulfillment, FEFO batch allocation, barcode verification, patient counseling recording, partial fills, and automated inventory deduction in clinic dispensary.**

All 21 endpoints specified in this document adhere strictly to uniform JSON:API response envelopes, time-ordered UUIDv7 identifiers, ISO-8601 UTC timestamps, optimistic concurrency control via ETags, and automated audit logging.

## 2. Operational Architecture & Relational Mapping

The following table maps the domain's operational context to architectural containers, components, database tables, and default role entitlements:

| Dimension | Specification Detail |
| :--- | :--- |
| **Functional Domain** | `Pharmacy` (Code: `PHARM`) |
| **Authoritative Endpoints** | 21 Active Endpoints (`API-PHARM-001` to `API-PHARM-021`) |
| **Primary Architecture Container** | `ARCH-CONT-009` |
| **Assigned Component** | `ARCH-COMP-025` |
| **Primary Database Tables** | `dispensations, dispensation_items, pharmacy_batches` |
| **Lead Role Entitlement** | `ROLE-017 (Registered Pharmacist)` |
| **Default Rate Limiting** | `60 req/min per User` |
| **Offline Edge Support** | `Edge Local Queue with Delta Sync` |

## 3. Domain Operational State Machine

The operational state transitions governing entities within this domain are modeled below:

```mermaid
stateDiagram-v2
    [*] --> InPharmacyQueue: Prescription Received from Doctor
    InPharmacyQueue --> BatchAllocated: Automated FEFO Batch Allocation
    BatchAllocated --> BarcodeScanned: Pharmacist Scans Medicine Box
    BarcodeScanned --> CounselingRecorded: Verbal Dosage Guidance Given
    CounselingRecorded --> Dispensed: Stock Deducted from Pharmacy Batch
    BatchAllocated --> PartialDispense: Out of Stock (Partial Fill)
    Dispensed --> Reversed: Reversal within 24h Window
    Dispensed --> [*]
    Reversed --> [*]
```

## 4. End-to-End Operational Data Flow

The sequence diagram below illustrates the end-to-end operational flow between frontline clinic staff, edge workstations, the central API gateway, and backing data stores:

```mermaid
sequenceDiagram
    autonumber
    participant Pharm as Clinic Pharmacist
    participant Barcode as 2D Barcode Scanner
    participant UI as Dispensary Workstation
    participant API as Pharmacy Service
    participant DB as Stock Ledger DB
    Pharm->>UI: Select Prescription Token A-042
    Pharm->>Barcode: Scan Paracetamol Batch Box
    Barcode->>UI: Transmit Barcode Data
    UI->>API: POST /api/v1/pharmacy/dispense
    API->>DB: Verify Expiry & Deduct 15 Units via FEFO
    API-->>UI: HTTP 200 OK (Dispensation Logged)
    UI-->>Pharm: Print Citizen Drug Label
```

## 5. Domain Endpoint Inventory Catalog

Complete inventory of all 21 endpoints defined for the `Pharmacy` domain:

| Endpoint ID | Method | URI Route Path | Functional Title | Role Context | Idempotency Standard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API-PHARM-001** | `POST` | `/api/v1/pharmacy` | Create New Pharmacy Dispensation Record | `ROLE-017` | Supported via X-Idempotency-Key |
| **API-PHARM-002** | `GET` | `/api/v1/pharmacy/{pharmacyId}` | Retrieve Pharmacy Dispensation Details by ID | `ROLE-017` | Read-Only Idempotent |
| **API-PHARM-003** | `GET` | `/api/v1/pharmacy` | List and Filter Pharmacy Dispensation Records | `ROLE-017` | Read-Only Idempotent |
| **API-PHARM-004** | `PUT` | `/api/v1/pharmacy/{pharmacyId}` | Update Full Pharmacy Dispensation Specification | `ROLE-017` | Supported via X-Idempotency-Key |
| **API-PHARM-005** | `PATCH` | `/api/v1/pharmacy/{pharmacyId}/status` | Update Pharmacy Dispensation Operational State | `ROLE-017` | Supported via X-Idempotency-Key |
| **API-PHARM-006** | `GET` | `/api/v1/pharmacy/{pharmacyId}/search` | Search Pharmacy Dispensation Workflow Operation | `ROLE-017` | Read-Only Idempotent |
| **API-PHARM-007** | `GET` | `/api/v1/pharmacy/history` | History Pharmacy Dispensation Workflow Operation | `ROLE-017` | Read-Only Idempotent |
| **API-PHARM-008** | `GET` | `/api/v1/pharmacy/{pharmacyId}/audit` | Audit Pharmacy Dispensation Workflow Operation | `ROLE-017` | Read-Only Idempotent |
| **API-PHARM-009** | `POST` | `/api/v1/pharmacy/cancel` | Cancel Pharmacy Dispensation Workflow Operation | `ROLE-017` | Supported via X-Idempotency-Key |
| **API-PHARM-010** | `POST` | `/api/v1/pharmacy/verify` | Verify Pharmacy Dispensation Workflow Operation | `ROLE-017` | Supported via X-Idempotency-Key |
| **API-PHARM-011** | `GET` | `/api/v1/pharmacy/export` | Export Pharmacy Dispensation Workflow Operation | `ROLE-017` | Read-Only Idempotent |
| **API-PHARM-012** | `GET` | `/api/v1/pharmacy/{pharmacyId}/metrics` | Metrics Pharmacy Dispensation Workflow Operation | `ROLE-017` | Read-Only Idempotent |
| **API-PHARM-013** | `POST` | `/api/v1/pharmacy/reconcile` | Reconcile Pharmacy Dispensation Workflow Operation | `ROLE-017` | Supported via X-Idempotency-Key |
| **API-PHARM-014** | `POST` | `/api/v1/pharmacy/batch` | Batch Pharmacy Dispensation Workflow Operation | `ROLE-017` | Supported via X-Idempotency-Key |
| **API-PHARM-015** | `GET` | `/api/v1/pharmacy/sync` | Sync Pharmacy Dispensation Workflow Operation | `ROLE-017` | Read-Only Idempotent |
| **API-PHARM-016** | `GET` | `/api/v1/pharmacy/{pharmacyId}/alerts` | Alerts Pharmacy Dispensation Workflow Operation | `ROLE-017` | Read-Only Idempotent |
| **API-PHARM-017** | `POST` | `/api/v1/pharmacy/escalate` | Escalate Pharmacy Dispensation Workflow Operation | `ROLE-017` | Supported via X-Idempotency-Key |
| **API-PHARM-018** | `POST` | `/api/v1/pharmacy/approve` | Approve Pharmacy Dispensation Workflow Operation | `ROLE-017` | Supported via X-Idempotency-Key |
| **API-PHARM-019** | `POST` | `/api/v1/pharmacy/reversal` | Reversal Pharmacy Dispensation Workflow Operation | `ROLE-017` | Supported via X-Idempotency-Key |
| **API-PHARM-020** | `GET` | `/api/v1/pharmacy/{pharmacyId}/items` | Items Pharmacy Dispensation Workflow Operation | `ROLE-017` | Read-Only Idempotent |
| **API-PHARM-021** | `GET` | `/api/v1/pharmacy/documents` | Documents Pharmacy Dispensation Workflow Operation | `ROLE-017` | Read-Only Idempotent |

## 6. Comprehensive Endpoint Technical Specifications

Exhaustive technical contracts for all 21 endpoints in the `Pharmacy` domain:

### 6.1 `API-PHARM-001`: Create New Pharmacy Dispensation Record

- **API Identifier:** `API-PHARM-001`
- **HTTP Route:** `POST /api/v1/pharmacy`
- **Functional Purpose:** Authoritative specification for create new pharmacy dispensation record within Pharmacy operations.
- **Product Capability:** `CAPABILITY-126` | **Feature Code:** `FEATURE-126`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:post`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-006, SRS-NFR-006` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-006`
- **Planned Verification Test Case:** `PLANNED-TEST-API-125`
- **Dependency DAG Edge:** `API-DEP-006`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy:
    post:
      summary: "Create New Pharmacy Dispensation Record"
      tags:
        - "Pharmacy"
      operationId: "post_api_v1_pharmacy"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy" \
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
  "operation": "Create New Pharmacy Dispensation Record",
  "domain": "Pharmacy",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PHARM-001"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-001",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-001.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-006` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-125` under simulated offline network conditions.

### 6.2 `API-PHARM-002`: Retrieve Pharmacy Dispensation Details by ID

- **API Identifier:** `API-PHARM-002`
- **HTTP Route:** `GET /api/v1/pharmacy/{pharmacyId}`
- **Functional Purpose:** Authoritative specification for retrieve pharmacy dispensation details by id within Pharmacy operations.
- **Product Capability:** `CAPABILITY-127` | **Feature Code:** `FEATURE-127`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:get`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-007, SRS-NFR-007` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-007`
- **Planned Verification Test Case:** `PLANNED-TEST-API-126`
- **Dependency DAG Edge:** `API-DEP-007`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/{pharmacyId}:
    get:
      summary: "Retrieve Pharmacy Dispensation Details by ID"
      tags:
        - "Pharmacy"
      operationId: "get_api_v1_pharmacy_pharmacyId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/{pharmacyId}" \
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
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-002",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-002.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-007` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-126` under simulated offline network conditions.

### 6.3 `API-PHARM-003`: List and Filter Pharmacy Dispensation Records

- **API Identifier:** `API-PHARM-003`
- **HTTP Route:** `GET /api/v1/pharmacy`
- **Functional Purpose:** Authoritative specification for list and filter pharmacy dispensation records within Pharmacy operations.
- **Product Capability:** `CAPABILITY-128` | **Feature Code:** `FEATURE-128`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:get`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-008, SRS-NFR-008` | **Workflow:** `WF-003`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-008`
- **Planned Verification Test Case:** `PLANNED-TEST-API-127`
- **Dependency DAG Edge:** `API-DEP-008`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy:
    get:
      summary: "List and Filter Pharmacy Dispensation Records"
      tags:
        - "Pharmacy"
      operationId: "get_api_v1_pharmacy"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy" \
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
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-003",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-003.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-008` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-127` under simulated offline network conditions.

### 6.4 `API-PHARM-004`: Update Full Pharmacy Dispensation Specification

- **API Identifier:** `API-PHARM-004`
- **HTTP Route:** `PUT /api/v1/pharmacy/{pharmacyId}`
- **Functional Purpose:** Authoritative specification for update full pharmacy dispensation specification within Pharmacy operations.
- **Product Capability:** `CAPABILITY-129` | **Feature Code:** `FEATURE-129`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:put`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-009, SRS-NFR-009` | **Workflow:** `WF-004`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-009`
- **Planned Verification Test Case:** `PLANNED-TEST-API-128`
- **Dependency DAG Edge:** `API-DEP-009`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/{pharmacyId}:
    put:
      summary: "Update Full Pharmacy Dispensation Specification"
      tags:
        - "Pharmacy"
      operationId: "put_api_v1_pharmacy_pharmacyId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/{pharmacyId}" \
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
  "operation": "Update Full Pharmacy Dispensation Specification",
  "domain": "Pharmacy",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PHARM-004"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-004",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-004.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-009` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-128` under simulated offline network conditions.

### 6.5 `API-PHARM-005`: Update Pharmacy Dispensation Operational State

- **API Identifier:** `API-PHARM-005`
- **HTTP Route:** `PATCH /api/v1/pharmacy/{pharmacyId}/status`
- **Functional Purpose:** Authoritative specification for update pharmacy dispensation operational state within Pharmacy operations.
- **Product Capability:** `CAPABILITY-130` | **Feature Code:** `FEATURE-130`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:patch`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-010, SRS-NFR-010` | **Workflow:** `WF-005`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-010`
- **Planned Verification Test Case:** `PLANNED-TEST-API-129`
- **Dependency DAG Edge:** `API-DEP-010`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/{pharmacyId}/status:
    patch:
      summary: "Update Pharmacy Dispensation Operational State"
      tags:
        - "Pharmacy"
      operationId: "patch_api_v1_pharmacy_pharmacyId_status"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/{pharmacyId}/status" \
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
  "operation": "Update Pharmacy Dispensation Operational State",
  "domain": "Pharmacy",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PHARM-005"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-005",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-005.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-010` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-129` under simulated offline network conditions.

### 6.6 `API-PHARM-006`: Search Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-006`
- **HTTP Route:** `GET /api/v1/pharmacy/{pharmacyId}/search`
- **Functional Purpose:** Authoritative specification for search pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-131` | **Feature Code:** `FEATURE-131`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:get`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-011, SRS-NFR-011` | **Workflow:** `WF-006`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-011`
- **Planned Verification Test Case:** `PLANNED-TEST-API-130`
- **Dependency DAG Edge:** `API-DEP-011`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/{pharmacyId}/search:
    get:
      summary: "Search Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "get_api_v1_pharmacy_pharmacyId_search"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/{pharmacyId}/search" \
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
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-006",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-006.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-011` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-130` under simulated offline network conditions.

### 6.7 `API-PHARM-007`: History Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-007`
- **HTTP Route:** `GET /api/v1/pharmacy/history`
- **Functional Purpose:** Authoritative specification for history pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-132` | **Feature Code:** `FEATURE-132`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:get`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-012, SRS-NFR-012` | **Workflow:** `WF-007`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-012`
- **Planned Verification Test Case:** `PLANNED-TEST-API-131`
- **Dependency DAG Edge:** `API-DEP-012`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/history:
    get:
      summary: "History Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "get_api_v1_pharmacy_history"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/history" \
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
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-007",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-007.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-012` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-131` under simulated offline network conditions.

### 6.8 `API-PHARM-008`: Audit Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-008`
- **HTTP Route:** `GET /api/v1/pharmacy/{pharmacyId}/audit`
- **Functional Purpose:** Authoritative specification for audit pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-133` | **Feature Code:** `FEATURE-133`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:get`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-013, SRS-NFR-013` | **Workflow:** `WF-008`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-013`
- **Planned Verification Test Case:** `PLANNED-TEST-API-132`
- **Dependency DAG Edge:** `API-DEP-013`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/{pharmacyId}/audit:
    get:
      summary: "Audit Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "get_api_v1_pharmacy_pharmacyId_audit"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/{pharmacyId}/audit" \
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
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-008",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-008.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-013` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-132` under simulated offline network conditions.

### 6.9 `API-PHARM-009`: Cancel Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-009`
- **HTTP Route:** `POST /api/v1/pharmacy/cancel`
- **Functional Purpose:** Authoritative specification for cancel pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-134` | **Feature Code:** `FEATURE-134`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:post`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-014, SRS-NFR-014` | **Workflow:** `WF-009`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-014`
- **Planned Verification Test Case:** `PLANNED-TEST-API-133`
- **Dependency DAG Edge:** `API-DEP-014`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/cancel:
    post:
      summary: "Cancel Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "post_api_v1_pharmacy_cancel"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/cancel" \
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
  "operation": "Cancel Pharmacy Dispensation Workflow Operation",
  "domain": "Pharmacy",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PHARM-009"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-009",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-009.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-014` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-133` under simulated offline network conditions.

### 6.10 `API-PHARM-010`: Verify Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-010`
- **HTTP Route:** `POST /api/v1/pharmacy/verify`
- **Functional Purpose:** Authoritative specification for verify pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-135` | **Feature Code:** `FEATURE-135`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:post`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-015, SRS-NFR-015` | **Workflow:** `WF-010`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-015`
- **Planned Verification Test Case:** `PLANNED-TEST-API-134`
- **Dependency DAG Edge:** `API-DEP-015`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/verify:
    post:
      summary: "Verify Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "post_api_v1_pharmacy_verify"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/verify" \
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
  "operation": "Verify Pharmacy Dispensation Workflow Operation",
  "domain": "Pharmacy",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PHARM-010"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-010",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-010.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-015` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-134` under simulated offline network conditions.

### 6.11 `API-PHARM-011`: Export Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-011`
- **HTTP Route:** `GET /api/v1/pharmacy/export`
- **Functional Purpose:** Authoritative specification for export pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-136` | **Feature Code:** `FEATURE-136`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:get`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-016, SRS-NFR-016` | **Workflow:** `WF-011`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-016`
- **Planned Verification Test Case:** `PLANNED-TEST-API-135`
- **Dependency DAG Edge:** `API-DEP-016`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/export:
    get:
      summary: "Export Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "get_api_v1_pharmacy_export"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/export" \
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
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-011",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-011.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-016` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-135` under simulated offline network conditions.

### 6.12 `API-PHARM-012`: Metrics Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-012`
- **HTTP Route:** `GET /api/v1/pharmacy/{pharmacyId}/metrics`
- **Functional Purpose:** Authoritative specification for metrics pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-137` | **Feature Code:** `FEATURE-137`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:get`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-017, SRS-NFR-017` | **Workflow:** `WF-012`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-017`
- **Planned Verification Test Case:** `PLANNED-TEST-API-136`
- **Dependency DAG Edge:** `API-DEP-017`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/{pharmacyId}/metrics:
    get:
      summary: "Metrics Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "get_api_v1_pharmacy_pharmacyId_metrics"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/{pharmacyId}/metrics" \
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
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-012",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-012.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-017` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-136` under simulated offline network conditions.

### 6.13 `API-PHARM-013`: Reconcile Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-013`
- **HTTP Route:** `POST /api/v1/pharmacy/reconcile`
- **Functional Purpose:** Authoritative specification for reconcile pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-138` | **Feature Code:** `FEATURE-138`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:post`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-018, SRS-NFR-018` | **Workflow:** `WF-013`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-018`
- **Planned Verification Test Case:** `PLANNED-TEST-API-137`
- **Dependency DAG Edge:** `API-DEP-018`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/reconcile:
    post:
      summary: "Reconcile Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "post_api_v1_pharmacy_reconcile"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/reconcile" \
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
  "operation": "Reconcile Pharmacy Dispensation Workflow Operation",
  "domain": "Pharmacy",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PHARM-013"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-013",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-013.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-018` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-137` under simulated offline network conditions.

### 6.14 `API-PHARM-014`: Batch Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-014`
- **HTTP Route:** `POST /api/v1/pharmacy/batch`
- **Functional Purpose:** Authoritative specification for batch pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-139` | **Feature Code:** `FEATURE-139`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:post`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-019, SRS-NFR-019` | **Workflow:** `WF-014`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-019`
- **Planned Verification Test Case:** `PLANNED-TEST-API-138`
- **Dependency DAG Edge:** `API-DEP-019`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/batch:
    post:
      summary: "Batch Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "post_api_v1_pharmacy_batch"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/batch" \
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
  "operation": "Batch Pharmacy Dispensation Workflow Operation",
  "domain": "Pharmacy",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PHARM-014"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-014",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-014.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-019` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-138` under simulated offline network conditions.

### 6.15 `API-PHARM-015`: Sync Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-015`
- **HTTP Route:** `GET /api/v1/pharmacy/sync`
- **Functional Purpose:** Authoritative specification for sync pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-140` | **Feature Code:** `FEATURE-140`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:get`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-020, SRS-NFR-020` | **Workflow:** `WF-015`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-020`
- **Planned Verification Test Case:** `PLANNED-TEST-API-139`
- **Dependency DAG Edge:** `API-DEP-020`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/sync:
    get:
      summary: "Sync Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "get_api_v1_pharmacy_sync"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/sync" \
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
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-015",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-015.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-020` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-139` under simulated offline network conditions.

### 6.16 `API-PHARM-016`: Alerts Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-016`
- **HTTP Route:** `GET /api/v1/pharmacy/{pharmacyId}/alerts`
- **Functional Purpose:** Authoritative specification for alerts pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-141` | **Feature Code:** `FEATURE-141`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:get`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-021, SRS-NFR-021` | **Workflow:** `WF-016`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-021`
- **Planned Verification Test Case:** `PLANNED-TEST-API-140`
- **Dependency DAG Edge:** `API-DEP-021`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/{pharmacyId}/alerts:
    get:
      summary: "Alerts Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "get_api_v1_pharmacy_pharmacyId_alerts"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/{pharmacyId}/alerts" \
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
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-016",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-016.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-021` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-140` under simulated offline network conditions.

### 6.17 `API-PHARM-017`: Escalate Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-017`
- **HTTP Route:** `POST /api/v1/pharmacy/escalate`
- **Functional Purpose:** Authoritative specification for escalate pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-142` | **Feature Code:** `FEATURE-142`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:post`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-022, SRS-NFR-022` | **Workflow:** `WF-017`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-022`
- **Planned Verification Test Case:** `PLANNED-TEST-API-141`
- **Dependency DAG Edge:** `API-DEP-022`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/escalate:
    post:
      summary: "Escalate Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "post_api_v1_pharmacy_escalate"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/escalate" \
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
  "operation": "Escalate Pharmacy Dispensation Workflow Operation",
  "domain": "Pharmacy",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PHARM-017"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-017",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-017.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-022` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-141` under simulated offline network conditions.

### 6.18 `API-PHARM-018`: Approve Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-018`
- **HTTP Route:** `POST /api/v1/pharmacy/approve`
- **Functional Purpose:** Authoritative specification for approve pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-143` | **Feature Code:** `FEATURE-143`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:post`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-023, SRS-NFR-023` | **Workflow:** `WF-018`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-023`
- **Planned Verification Test Case:** `PLANNED-TEST-API-142`
- **Dependency DAG Edge:** `API-DEP-023`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/approve:
    post:
      summary: "Approve Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "post_api_v1_pharmacy_approve"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/approve" \
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
  "operation": "Approve Pharmacy Dispensation Workflow Operation",
  "domain": "Pharmacy",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PHARM-018"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-018",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-018.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-023` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-142` under simulated offline network conditions.

### 6.19 `API-PHARM-019`: Reversal Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-019`
- **HTTP Route:** `POST /api/v1/pharmacy/reversal`
- **Functional Purpose:** Authoritative specification for reversal pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-144` | **Feature Code:** `FEATURE-144`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:post`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-024, SRS-NFR-024` | **Workflow:** `WF-019`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-024`
- **Planned Verification Test Case:** `PLANNED-TEST-API-143`
- **Dependency DAG Edge:** `API-DEP-024`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/reversal:
    post:
      summary: "Reversal Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "post_api_v1_pharmacy_reversal"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/reversal" \
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
  "operation": "Reversal Pharmacy Dispensation Workflow Operation",
  "domain": "Pharmacy",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PHARM-019"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-019",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-019.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-024` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-143` under simulated offline network conditions.

### 6.20 `API-PHARM-020`: Items Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-020`
- **HTTP Route:** `GET /api/v1/pharmacy/{pharmacyId}/items`
- **Functional Purpose:** Authoritative specification for items pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-145` | **Feature Code:** `FEATURE-145`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:get`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-025, SRS-NFR-025` | **Workflow:** `WF-020`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-025`
- **Planned Verification Test Case:** `PLANNED-TEST-API-144`
- **Dependency DAG Edge:** `API-DEP-025`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/{pharmacyId}/items:
    get:
      summary: "Items Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "get_api_v1_pharmacy_pharmacyId_items"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/{pharmacyId}/items" \
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
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-020",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-020.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-025` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-144` under simulated offline network conditions.

### 6.21 `API-PHARM-021`: Documents Pharmacy Dispensation Workflow Operation

- **API Identifier:** `API-PHARM-021`
- **HTTP Route:** `GET /api/v1/pharmacy/documents`
- **Functional Purpose:** Authoritative specification for documents pharmacy dispensation workflow operation within Pharmacy operations.
- **Product Capability:** `CAPABILITY-146` | **Feature Code:** `FEATURE-146`
- **Primary Actor:** Authorized Pharmacy Operator | **User Persona:** Pharmacy Care Team Persona
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `pharmacy:get`
- **ABAC Scoping Rule:** Restricted to authorized Pharmacy personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-026, SRS-NFR-026` | **Workflow:** `WF-021`
- **Container / Component:** `ARCH-CONT-009` / `ARCH-COMP-025`
- **Target Relational Tables:** `dispensations, dispensation_items, pharmacy_batches`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-026`
- **Planned Verification Test Case:** `PLANNED-TEST-API-145`
- **Dependency DAG Edge:** `API-DEP-026`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/pharmacy/documents:
    get:
      summary: "Documents Pharmacy Dispensation Workflow Operation"
      tags:
        - "Pharmacy"
      operationId: "get_api_v1_pharmacy_documents"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/pharmacy/documents" \
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
    "type": "pharmacy",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PHARM-021",
      "domain": "Pharmacy",
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
    "code": "ERR-PHARM-001",
    "message": "Domain constraint validation failed during execution of API-PHARM-021.",
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
- **Relational Database Mutation:** Modifies tables `dispensations, dispensation_items, pharmacy_batches` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-026` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-145` under simulated offline network conditions.

## 7. Domain-Specific Error Code Catalog & Troubleshooting Runbooks

The following standardized error codes are specifically emitted by `Pharmacy` services:

| Error Code ID | HTTP Status | Machine Code | Message Summary | Retryable | Resolution Runbook |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-PHARM-001** | `HTTP 404` | `PHARM_BATCH_NOT_FOUND` | Allocated pharmaceutical batch identifier does not exist in dispensary. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PHARM-001. |
| **ERR-PHARM-002** | `HTTP 409` | `PHARM_BATCH_EXPIRED` | Selected drug batch has reached its expiration date and cannot be dispensed. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PHARM-002. |
| **ERR-PHARM-003** | `HTTP 409` | `PHARM_INSUFFICIENT_STOCK` | Requested quantity exceeds available on-hand batch balance in clinic. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PHARM-003. |
| **ERR-PHARM-004** | `HTTP 400` | `PHARM_FEFO_VIOLATION` | Earlier-expiring batch exists in dispensary; FEFO allocation enforced. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PHARM-004. |
| **ERR-PHARM-005** | `HTTP 403` | `PHARM_PHARMACIST_ROLE_REQUIRED` | Dispensation requires registered pharmacist credential and role. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PHARM-005. |
| **ERR-PHARM-006** | `HTTP 409` | `PHARM_DISPENSE_ALREADY_FINALIZED` | Prescription items have already been fully dispensed. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PHARM-006. |
| **ERR-PHARM-007** | `HTTP 400` | `PHARM_SUBSTITUTION_UNAUTHORIZED` | Therapeutic generic substitution requires prior prescriber consultation. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PHARM-007. |
| **ERR-PHARM-008** | `HTTP 400` | `PHARM_REVERSAL_EXPIRED` | Dispensation cannot be reversed after 24 hours of issue. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PHARM-008. |
| **ERR-PHARM-009** | `HTTP 409` | `PHARM_STOCK_LOCKED` | Dispensary stock currently locked for annual municipal physical inventory audit. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PHARM-009. |
| **ERR-PHARM-010** | `HTTP 500` | `PHARM_LEDGER_POST_FAILED` | Double-entry pharmacy stock movement ledger transaction failed. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-PHARM-010. |

## 8. Offline Edge Operation & Synchronization Mechanics

When WAN connectivity to the central cloud is disrupted, `Pharmacy` operations transition to autonomous edge mode:
1. **Local SQLite WAL Database:** Transactions are committed locally to `/data/namma_clinic_edge.db` on the clinic's Intel N100 mini-server.
2. **Offline Mutation Journal:** Every INSERT, UPDATE, and SOFT_DELETE appends a record to the `offline_mutation_log` table with a local vector clock.
3. **Conflict Resolution Policy:** Upon WAN restoration, the edge sync agent uploads buffered mutations in batches of 100 to `/api/v1/system/sync/batch`. Conflicts are resolved deterministically using Last-Write-Wins (LWW) with microsecond Lamport timestamps, except for clinical records where doctor entries take precedence over clerical updates.
4. **Storage Quotas:** Up to 72 hours of offline operations (approximately 15,000 mutations) can be buffered without storage degradation.

## 9. Security, Data Protection & DPDP Act Compliance

Data protection invariants for `Pharmacy` operations:

| Data Element | Classification | Encryption Standard | Masking Rule | DPDP Act Section | Retention Schedule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Core Entity Record | `INTERNAL` | AES-256-GCM Column Level | Masked on non-admin UI | Section 8 (Data Security) | 10 Years (Medical Records) |
| Transaction Mutation | INTERNAL | TLS 1.3 in Transit | Zero PII in Gateway Logs | Section 6 (Consent Notice) | 10 Years (Audit Ledger) |
| WORM Audit Log | HIGHLY-RESTRICTED | HMAC SHA-256 Chained | Full Hash Ledger | Section 12 (Citizen Rights) | Permanent (Statutory Archive) |

## 10. Domain Quality Acceptance Criteria (BDD)

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify Successful Execution of Create New Pharmacy Dispensation Record
  Given an authenticated staff member with role 'ROLE-017'
  And an active clinical shift rostered in clinic facility '018e3a20-0008-7000-8000-000000000001'
  When the client sends a valid request to /api/v1/pharmacy
  Then the server processes the request within 1500ms
  And returns HTTP 201
  And the response conforms to envelope schema 'StandardApiResponseEnvelope'
  And an immutable audit log is appended to 'AUDIT-EVENT-006'
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Reject Unauthorized Call to Create New Pharmacy Dispensation Record
  Given a caller presenting an invalid or expired Bearer token
  And requesting protected resource access
  When the caller transmits a request to /api/v1/pharmacy
  Then the API gateway intercepts the request
  And returns HTTP 401 Unauthorized
  And returns error code 'ERR-AUTH-002' or 'ERR-AUTH-003'
  And rejects access before invoking backend services
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Execute Create New Pharmacy Dispensation Record in Autonomous Edge Mode
  Given the clinic workstation has lost WAN connectivity to cloud
  And the local edge mini-server is operational with local SQLite database
  When the staff member executes Create New Pharmacy Dispensation Record
  Then the edge API gateway accepts the request locally
  And returns HTTP 201 within 250ms
  And appends the mutation to the local offline sync journal
  And synchronizes to cloud automatically upon network restoration
```

## 11. Requirements & Database Relational Traceability Matrix

Traceability mapping for all `Pharmacy` endpoints:

| Endpoint ID | Upstream SRS Requirements | Workflow ID | Feature Code | Target Database Tables | Verification Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `API-PHARM-001` | `SRS-FR-006, SRS-NFR-006` | `WF-001` | `FEATURE-126` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-125` |
| `API-PHARM-002` | `SRS-FR-007, SRS-NFR-007` | `WF-002` | `FEATURE-127` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-126` |
| `API-PHARM-003` | `SRS-FR-008, SRS-NFR-008` | `WF-003` | `FEATURE-128` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-127` |
| `API-PHARM-004` | `SRS-FR-009, SRS-NFR-009` | `WF-004` | `FEATURE-129` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-128` |
| `API-PHARM-005` | `SRS-FR-010, SRS-NFR-010` | `WF-005` | `FEATURE-130` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-129` |
| `API-PHARM-006` | `SRS-FR-011, SRS-NFR-011` | `WF-006` | `FEATURE-131` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-130` |
| `API-PHARM-007` | `SRS-FR-012, SRS-NFR-012` | `WF-007` | `FEATURE-132` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-131` |
| `API-PHARM-008` | `SRS-FR-013, SRS-NFR-013` | `WF-008` | `FEATURE-133` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-132` |
| `API-PHARM-009` | `SRS-FR-014, SRS-NFR-014` | `WF-009` | `FEATURE-134` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-133` |
| `API-PHARM-010` | `SRS-FR-015, SRS-NFR-015` | `WF-010` | `FEATURE-135` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-134` |
| `API-PHARM-011` | `SRS-FR-016, SRS-NFR-016` | `WF-011` | `FEATURE-136` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-135` |
| `API-PHARM-012` | `SRS-FR-017, SRS-NFR-017` | `WF-012` | `FEATURE-137` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-136` |
| `API-PHARM-013` | `SRS-FR-018, SRS-NFR-018` | `WF-013` | `FEATURE-138` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-137` |
| `API-PHARM-014` | `SRS-FR-019, SRS-NFR-019` | `WF-014` | `FEATURE-139` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-138` |
| `API-PHARM-015` | `SRS-FR-020, SRS-NFR-020` | `WF-015` | `FEATURE-140` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-139` |
| `API-PHARM-016` | `SRS-FR-021, SRS-NFR-021` | `WF-016` | `FEATURE-141` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-140` |
| `API-PHARM-017` | `SRS-FR-022, SRS-NFR-022` | `WF-017` | `FEATURE-142` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-141` |
| `API-PHARM-018` | `SRS-FR-023, SRS-NFR-023` | `WF-018` | `FEATURE-143` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-142` |
| `API-PHARM-019` | `SRS-FR-024, SRS-NFR-024` | `WF-019` | `FEATURE-144` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-143` |
| `API-PHARM-020` | `SRS-FR-025, SRS-NFR-025` | `WF-020` | `FEATURE-145` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-144` |
| `API-PHARM-021` | `SRS-FR-026, SRS-NFR-026` | `WF-021` | `FEATURE-146` | `dispensations, dispensation_items, pharmacy_batches` | `PLANNED-TEST-API-145` |
