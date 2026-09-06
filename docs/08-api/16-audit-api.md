# 🔌 API Specification: Immutable WORM Audit Ledger & Tamper-Detection API Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-16 | **Status:** Authoritative Baseline | **Date:** September 2026
> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Standard Framework:** RFC 7231 (HTTP/1.1), JSON:API v1.1, DPDP Act 2023, ABDM Interoperability Standards
> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.

---

## 1. Executive Summary & Domain Scope

The **Immutable WORM Audit Ledger & Tamper-Detection API Specification** defines the authoritative, implementation-ready contracts for the `Audit` subsystem across all 183 Namma Clinic primary healthcare centers in Greater Bengaluru. This domain operates under the supervisory jurisdiction of `ROLE-011 (Chief Data Privacy Officer / Legal Auditor)` and fulfills the core mission: **Provide cryptographic proof of non-repudiation, tamper detection, WORM log querying, and break-glass access auditing in compliance with DPDP Act 2023 and DISHA statutory regulations.**

All 19 endpoints specified in this document adhere strictly to uniform JSON:API response envelopes, time-ordered UUIDv7 identifiers, ISO-8601 UTC timestamps, optimistic concurrency control via ETags, and automated audit logging.

## 2. Operational Architecture & Relational Mapping

The following table maps the domain's operational context to architectural containers, components, database tables, and default role entitlements:

| Dimension | Specification Detail |
| :--- | :--- |
| **Functional Domain** | `Audit` (Code: `AUDIT`) |
| **Authoritative Endpoints** | 19 Active Endpoints (`API-AUDIT-001` to `API-AUDIT-019`) |
| **Primary Architecture Container** | `ARCH-CONT-017` |
| **Assigned Component** | `ARCH-COMP-049` |
| **Primary Database Tables** | `audit_events` |
| **Lead Role Entitlement** | `ROLE-011 (Chief Data Privacy Officer / Legal Auditor)` |
| **Default Rate Limiting** | `60 req/min per User` |
| **Offline Edge Support** | `Edge Local Queue with Delta Sync` |

## 3. Domain Operational State Machine

The operational state transitions governing entities within this domain are modeled below:

```mermaid
stateDiagram-v2
    [*] --> EventCaptured: User Executes Clinical Action or View
    EventCaptured --> PayloadHashed: Compute SHA-256 Hash of Event Data
    PayloadHashed --> ChainLinked: Link to Previous Block Hash (HMAC SHA-256)
    ChainLinked --> ImmutableAppended: Append to audit_events WORM Table
    ImmutableAppended --> VerificationRequested: Auditor Runs Integrity Scan
    VerificationRequested --> ChainIntact: All Sequential Hashes Validate
    VerificationRequested --> TamperAlert: Cryptographic Mismatch Detected
    TamperAlert --> SecurityIncident: Automated Security Incident Triggered
    ChainIntact --> ReportGenerated: Audit Certificate Exported
    ReportGenerated --> [*]
```

## 4. End-to-End Operational Data Flow

The sequence diagram below illustrates the end-to-end operational flow between frontline clinic staff, edge workstations, the central API gateway, and backing data stores:

```mermaid
sequenceDiagram
    autonumber
    participant Auditor as Data Privacy Officer
    participant UI as Compliance Audit Portal
    participant API as Audit Service
    participant WORM as Cryptographic Audit Ledger
    Auditor->>UI: Request Cryptographic Hash Verification (Ward 142)
    UI->>API: POST /api/v1/audit/verify-chain
    API->>WORM: Sequentially Verify 50,000 Hash Blocks
    WORM-->>API: Zero Tampering Detected (Hash Chain 100% Valid)
    API-->>UI: HTTP 200 OK (Verification Status: VALID)
    UI-->>Auditor: Display Signed Compliance Certificate
```

## 5. Domain Endpoint Inventory Catalog

Complete inventory of all 19 endpoints defined for the `Audit` domain:

| Endpoint ID | Method | URI Route Path | Functional Title | Role Context | Idempotency Standard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API-AUDIT-001** | `POST` | `/api/v1/audit` | Create New WORM Audit Ledger Record | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-AUDIT-002** | `GET` | `/api/v1/audit/{auditId}` | Retrieve WORM Audit Ledger Details by ID | `ROLE-011` | Read-Only Idempotent |
| **API-AUDIT-003** | `GET` | `/api/v1/audit` | List and Filter WORM Audit Ledger Records | `ROLE-011` | Read-Only Idempotent |
| **API-AUDIT-004** | `PUT` | `/api/v1/audit/{auditId}` | Update Full WORM Audit Ledger Specification | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-AUDIT-005** | `PATCH` | `/api/v1/audit/{auditId}/status` | Update WORM Audit Ledger Operational State | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-AUDIT-006** | `GET` | `/api/v1/audit/{auditId}/search` | Search WORM Audit Ledger Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-AUDIT-007** | `GET` | `/api/v1/audit/history` | History WORM Audit Ledger Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-AUDIT-008** | `GET` | `/api/v1/audit/{auditId}/audit` | Audit WORM Audit Ledger Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-AUDIT-009** | `POST` | `/api/v1/audit/cancel` | Cancel WORM Audit Ledger Workflow Operation | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-AUDIT-010** | `POST` | `/api/v1/audit/verify` | Verify WORM Audit Ledger Workflow Operation | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-AUDIT-011** | `GET` | `/api/v1/audit/export` | Export WORM Audit Ledger Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-AUDIT-012** | `GET` | `/api/v1/audit/{auditId}/metrics` | Metrics WORM Audit Ledger Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-AUDIT-013** | `POST` | `/api/v1/audit/reconcile` | Reconcile WORM Audit Ledger Workflow Operation | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-AUDIT-014** | `POST` | `/api/v1/audit/batch` | Batch WORM Audit Ledger Workflow Operation | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-AUDIT-015** | `GET` | `/api/v1/audit/sync` | Sync WORM Audit Ledger Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-AUDIT-016** | `GET` | `/api/v1/audit/{auditId}/alerts` | Alerts WORM Audit Ledger Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-AUDIT-017** | `POST` | `/api/v1/audit/escalate` | Escalate WORM Audit Ledger Workflow Operation | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-AUDIT-018** | `POST` | `/api/v1/audit/approve` | Approve WORM Audit Ledger Workflow Operation | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-AUDIT-019** | `POST` | `/api/v1/audit/reversal` | Reversal WORM Audit Ledger Workflow Operation | `ROLE-011` | Supported via X-Idempotency-Key |

## 6. Comprehensive Endpoint Technical Specifications

Exhaustive technical contracts for all 19 endpoints in the `Audit` domain:

### 6.1 `API-AUDIT-001`: Create New WORM Audit Ledger Record

- **API Identifier:** `API-AUDIT-001`
- **HTTP Route:** `POST /api/v1/audit`
- **Functional Purpose:** Authoritative specification for create new worm audit ledger record within Audit operations.
- **Product Capability:** `CAPABILITY-080` | **Feature Code:** `FEATURE-080`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:post`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-020, SRS-NFR-020` | **Workflow:** `WF-010`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-020`
- **Planned Verification Test Case:** `PLANNED-TEST-API-259`
- **Dependency DAG Edge:** `API-DEP-020`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit:
    post:
      summary: "Create New WORM Audit Ledger Record"
      tags:
        - "Audit"
      operationId: "post_api_v1_audit"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit" \
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
  "operation": "Create New WORM Audit Ledger Record",
  "domain": "Audit",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUDIT-001"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-001",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-001.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-020` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-259` under simulated offline network conditions.

### 6.2 `API-AUDIT-002`: Retrieve WORM Audit Ledger Details by ID

- **API Identifier:** `API-AUDIT-002`
- **HTTP Route:** `GET /api/v1/audit/{auditId}`
- **Functional Purpose:** Authoritative specification for retrieve worm audit ledger details by id within Audit operations.
- **Product Capability:** `CAPABILITY-081` | **Feature Code:** `FEATURE-081`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:get`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-021, SRS-NFR-021` | **Workflow:** `WF-011`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-021`
- **Planned Verification Test Case:** `PLANNED-TEST-API-260`
- **Dependency DAG Edge:** `API-DEP-021`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/{auditId}:
    get:
      summary: "Retrieve WORM Audit Ledger Details by ID"
      tags:
        - "Audit"
      operationId: "get_api_v1_audit_auditId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/{auditId}" \
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
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-002",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-002.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-021` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-260` under simulated offline network conditions.

### 6.3 `API-AUDIT-003`: List and Filter WORM Audit Ledger Records

- **API Identifier:** `API-AUDIT-003`
- **HTTP Route:** `GET /api/v1/audit`
- **Functional Purpose:** Authoritative specification for list and filter worm audit ledger records within Audit operations.
- **Product Capability:** `CAPABILITY-082` | **Feature Code:** `FEATURE-082`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:get`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-022, SRS-NFR-022` | **Workflow:** `WF-012`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-022`
- **Planned Verification Test Case:** `PLANNED-TEST-API-261`
- **Dependency DAG Edge:** `API-DEP-022`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit:
    get:
      summary: "List and Filter WORM Audit Ledger Records"
      tags:
        - "Audit"
      operationId: "get_api_v1_audit"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit" \
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
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-003",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-003.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-022` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-261` under simulated offline network conditions.

### 6.4 `API-AUDIT-004`: Update Full WORM Audit Ledger Specification

- **API Identifier:** `API-AUDIT-004`
- **HTTP Route:** `PUT /api/v1/audit/{auditId}`
- **Functional Purpose:** Authoritative specification for update full worm audit ledger specification within Audit operations.
- **Product Capability:** `CAPABILITY-083` | **Feature Code:** `FEATURE-083`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:put`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-023, SRS-NFR-023` | **Workflow:** `WF-013`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-023`
- **Planned Verification Test Case:** `PLANNED-TEST-API-262`
- **Dependency DAG Edge:** `API-DEP-023`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/{auditId}:
    put:
      summary: "Update Full WORM Audit Ledger Specification"
      tags:
        - "Audit"
      operationId: "put_api_v1_audit_auditId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/{auditId}" \
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
  "operation": "Update Full WORM Audit Ledger Specification",
  "domain": "Audit",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUDIT-004"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-004",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-004.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-023` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-262` under simulated offline network conditions.

### 6.5 `API-AUDIT-005`: Update WORM Audit Ledger Operational State

- **API Identifier:** `API-AUDIT-005`
- **HTTP Route:** `PATCH /api/v1/audit/{auditId}/status`
- **Functional Purpose:** Authoritative specification for update worm audit ledger operational state within Audit operations.
- **Product Capability:** `CAPABILITY-084` | **Feature Code:** `FEATURE-084`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:patch`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-024, SRS-NFR-024` | **Workflow:** `WF-014`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-024`
- **Planned Verification Test Case:** `PLANNED-TEST-API-263`
- **Dependency DAG Edge:** `API-DEP-024`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/{auditId}/status:
    patch:
      summary: "Update WORM Audit Ledger Operational State"
      tags:
        - "Audit"
      operationId: "patch_api_v1_audit_auditId_status"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/{auditId}/status" \
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
  "operation": "Update WORM Audit Ledger Operational State",
  "domain": "Audit",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUDIT-005"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-005",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-005.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-024` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-263` under simulated offline network conditions.

### 6.6 `API-AUDIT-006`: Search WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-006`
- **HTTP Route:** `GET /api/v1/audit/{auditId}/search`
- **Functional Purpose:** Authoritative specification for search worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-085` | **Feature Code:** `FEATURE-085`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:get`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-025, SRS-NFR-025` | **Workflow:** `WF-015`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-025`
- **Planned Verification Test Case:** `PLANNED-TEST-API-264`
- **Dependency DAG Edge:** `API-DEP-025`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/{auditId}/search:
    get:
      summary: "Search WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "get_api_v1_audit_auditId_search"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/{auditId}/search" \
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
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-006",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-006.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-025` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-264` under simulated offline network conditions.

### 6.7 `API-AUDIT-007`: History WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-007`
- **HTTP Route:** `GET /api/v1/audit/history`
- **Functional Purpose:** Authoritative specification for history worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-086` | **Feature Code:** `FEATURE-086`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:get`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-026, SRS-NFR-026` | **Workflow:** `WF-016`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-026`
- **Planned Verification Test Case:** `PLANNED-TEST-API-265`
- **Dependency DAG Edge:** `API-DEP-026`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/history:
    get:
      summary: "History WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "get_api_v1_audit_history"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/history" \
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
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-007",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-007.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-026` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-265` under simulated offline network conditions.

### 6.8 `API-AUDIT-008`: Audit WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-008`
- **HTTP Route:** `GET /api/v1/audit/{auditId}/audit`
- **Functional Purpose:** Authoritative specification for audit worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-087` | **Feature Code:** `FEATURE-087`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:get`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-027, SRS-NFR-027` | **Workflow:** `WF-017`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-027`
- **Planned Verification Test Case:** `PLANNED-TEST-API-266`
- **Dependency DAG Edge:** `API-DEP-027`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/{auditId}/audit:
    get:
      summary: "Audit WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "get_api_v1_audit_auditId_audit"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/{auditId}/audit" \
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
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-008",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-008.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-027` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-266` under simulated offline network conditions.

### 6.9 `API-AUDIT-009`: Cancel WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-009`
- **HTTP Route:** `POST /api/v1/audit/cancel`
- **Functional Purpose:** Authoritative specification for cancel worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-088` | **Feature Code:** `FEATURE-088`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:post`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-028, SRS-NFR-028` | **Workflow:** `WF-018`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-028`
- **Planned Verification Test Case:** `PLANNED-TEST-API-267`
- **Dependency DAG Edge:** `API-DEP-028`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/cancel:
    post:
      summary: "Cancel WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "post_api_v1_audit_cancel"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/cancel" \
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
  "operation": "Cancel WORM Audit Ledger Workflow Operation",
  "domain": "Audit",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUDIT-009"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-009",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-009.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-028` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-267` under simulated offline network conditions.

### 6.10 `API-AUDIT-010`: Verify WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-010`
- **HTTP Route:** `POST /api/v1/audit/verify`
- **Functional Purpose:** Authoritative specification for verify worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-089` | **Feature Code:** `FEATURE-089`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:post`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-029, SRS-NFR-029` | **Workflow:** `WF-019`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-029`
- **Planned Verification Test Case:** `PLANNED-TEST-API-268`
- **Dependency DAG Edge:** `API-DEP-029`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/verify:
    post:
      summary: "Verify WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "post_api_v1_audit_verify"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/verify" \
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
  "operation": "Verify WORM Audit Ledger Workflow Operation",
  "domain": "Audit",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUDIT-010"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-010",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-010.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-029` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-268` under simulated offline network conditions.

### 6.11 `API-AUDIT-011`: Export WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-011`
- **HTTP Route:** `GET /api/v1/audit/export`
- **Functional Purpose:** Authoritative specification for export worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-090` | **Feature Code:** `FEATURE-090`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:get`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-030, SRS-NFR-030` | **Workflow:** `WF-020`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-030`
- **Planned Verification Test Case:** `PLANNED-TEST-API-269`
- **Dependency DAG Edge:** `API-DEP-030`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/export:
    get:
      summary: "Export WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "get_api_v1_audit_export"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/export" \
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
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-011",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-011.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-030` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-269` under simulated offline network conditions.

### 6.12 `API-AUDIT-012`: Metrics WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-012`
- **HTTP Route:** `GET /api/v1/audit/{auditId}/metrics`
- **Functional Purpose:** Authoritative specification for metrics worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-091` | **Feature Code:** `FEATURE-091`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:get`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-031, SRS-NFR-031` | **Workflow:** `WF-021`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-001`
- **Planned Verification Test Case:** `PLANNED-TEST-API-270`
- **Dependency DAG Edge:** `API-DEP-031`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/{auditId}/metrics:
    get:
      summary: "Metrics WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "get_api_v1_audit_auditId_metrics"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/{auditId}/metrics" \
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
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-012",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-012.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-001` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-270` under simulated offline network conditions.

### 6.13 `API-AUDIT-013`: Reconcile WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-013`
- **HTTP Route:** `POST /api/v1/audit/reconcile`
- **Functional Purpose:** Authoritative specification for reconcile worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-092` | **Feature Code:** `FEATURE-092`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:post`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-032, SRS-NFR-032` | **Workflow:** `WF-022`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-002`
- **Planned Verification Test Case:** `PLANNED-TEST-API-271`
- **Dependency DAG Edge:** `API-DEP-032`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/reconcile:
    post:
      summary: "Reconcile WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "post_api_v1_audit_reconcile"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/reconcile" \
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
  "operation": "Reconcile WORM Audit Ledger Workflow Operation",
  "domain": "Audit",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUDIT-013"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-013",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-013.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-002` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-271` under simulated offline network conditions.

### 6.14 `API-AUDIT-014`: Batch WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-014`
- **HTTP Route:** `POST /api/v1/audit/batch`
- **Functional Purpose:** Authoritative specification for batch worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-093` | **Feature Code:** `FEATURE-093`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:post`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-033, SRS-NFR-033` | **Workflow:** `WF-023`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-003`
- **Planned Verification Test Case:** `PLANNED-TEST-API-272`
- **Dependency DAG Edge:** `API-DEP-033`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/batch:
    post:
      summary: "Batch WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "post_api_v1_audit_batch"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/batch" \
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
  "operation": "Batch WORM Audit Ledger Workflow Operation",
  "domain": "Audit",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUDIT-014"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-014",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-014.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-003` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-272` under simulated offline network conditions.

### 6.15 `API-AUDIT-015`: Sync WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-015`
- **HTTP Route:** `GET /api/v1/audit/sync`
- **Functional Purpose:** Authoritative specification for sync worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-094` | **Feature Code:** `FEATURE-094`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:get`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-034, SRS-NFR-034` | **Workflow:** `WF-024`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-004`
- **Planned Verification Test Case:** `PLANNED-TEST-API-273`
- **Dependency DAG Edge:** `API-DEP-034`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/sync:
    get:
      summary: "Sync WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "get_api_v1_audit_sync"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/sync" \
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
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-015",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-015.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-004` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-273` under simulated offline network conditions.

### 6.16 `API-AUDIT-016`: Alerts WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-016`
- **HTTP Route:** `GET /api/v1/audit/{auditId}/alerts`
- **Functional Purpose:** Authoritative specification for alerts worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-095` | **Feature Code:** `FEATURE-095`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:get`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-035, SRS-NFR-035` | **Workflow:** `WF-025`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-005`
- **Planned Verification Test Case:** `PLANNED-TEST-API-274`
- **Dependency DAG Edge:** `API-DEP-035`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/{auditId}/alerts:
    get:
      summary: "Alerts WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "get_api_v1_audit_auditId_alerts"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/{auditId}/alerts" \
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
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-016",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-016.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-005` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-274` under simulated offline network conditions.

### 6.17 `API-AUDIT-017`: Escalate WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-017`
- **HTTP Route:** `POST /api/v1/audit/escalate`
- **Functional Purpose:** Authoritative specification for escalate worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-096` | **Feature Code:** `FEATURE-096`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:post`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-036, SRS-NFR-036` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-006`
- **Planned Verification Test Case:** `PLANNED-TEST-API-275`
- **Dependency DAG Edge:** `API-DEP-036`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/escalate:
    post:
      summary: "Escalate WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "post_api_v1_audit_escalate"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/escalate" \
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
  "operation": "Escalate WORM Audit Ledger Workflow Operation",
  "domain": "Audit",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUDIT-017"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-017",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-017.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-006` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-275` under simulated offline network conditions.

### 6.18 `API-AUDIT-018`: Approve WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-018`
- **HTTP Route:** `POST /api/v1/audit/approve`
- **Functional Purpose:** Authoritative specification for approve worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-097` | **Feature Code:** `FEATURE-097`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:post`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-037, SRS-NFR-037` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-007`
- **Planned Verification Test Case:** `PLANNED-TEST-API-276`
- **Dependency DAG Edge:** `API-DEP-037`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/approve:
    post:
      summary: "Approve WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "post_api_v1_audit_approve"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/approve" \
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
  "operation": "Approve WORM Audit Ledger Workflow Operation",
  "domain": "Audit",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUDIT-018"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-018",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-018.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-007` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-276` under simulated offline network conditions.

### 6.19 `API-AUDIT-019`: Reversal WORM Audit Ledger Workflow Operation

- **API Identifier:** `API-AUDIT-019`
- **HTTP Route:** `POST /api/v1/audit/reversal`
- **Functional Purpose:** Authoritative specification for reversal worm audit ledger workflow operation within Audit operations.
- **Product Capability:** `CAPABILITY-098` | **Feature Code:** `FEATURE-098`
- **Primary Actor:** Authorized Audit Operator | **User Persona:** Audit Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `audit:post`
- **ABAC Scoping Rule:** Restricted to authorized Audit personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-038, SRS-NFR-038` | **Workflow:** `WF-003`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-008`
- **Planned Verification Test Case:** `PLANNED-TEST-API-277`
- **Dependency DAG Edge:** `API-DEP-038`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/audit/reversal:
    post:
      summary: "Reversal WORM Audit Ledger Workflow Operation"
      tags:
        - "Audit"
      operationId: "post_api_v1_audit_reversal"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/audit/reversal" \
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
  "operation": "Reversal WORM Audit Ledger Workflow Operation",
  "domain": "Audit",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUDIT-019"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "audit",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUDIT-019",
      "domain": "Audit",
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
    "code": "ERR-AUDIT-001",
    "message": "Domain constraint validation failed during execution of API-AUDIT-019.",
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
- **Relational Database Mutation:** Modifies tables `audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-008` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-277` under simulated offline network conditions.

## 7. Domain-Specific Error Code Catalog & Troubleshooting Runbooks

The following standardized error codes are specifically emitted by `Audit` services:

| Error Code ID | HTTP Status | Machine Code | Message Summary | Retryable | Resolution Runbook |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-AUDIT-001** | `HTTP 403` | `AUDIT_MUTATION_PROHIBITED` | WORM compliance violation: audit records are immutable and cannot be edited or deleted. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUDIT-001. |
| **ERR-AUDIT-002** | `HTTP 403` | `AUDIT_OFFICER_ROLE_REQUIRED` | Access to immutable audit logs requires Security & Data Privacy Officer role. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUDIT-002. |
| **ERR-AUDIT-003** | `HTTP 400` | `AUDIT_QUERY_WINDOW_EXCEEDED` | Audit log search window exceeds maximum 31-day search interval. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUDIT-003. |
| **ERR-AUDIT-004** | `HTTP 500` | `AUDIT_HASH_CHAIN_MISMATCH` | CRITICAL: Cryptographic HMAC SHA-256 ledger tamper detected on verification. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUDIT-004. |
| **ERR-AUDIT-005** | `HTTP 404` | `AUDIT_RECORD_NOT_FOUND` | Audit log entry not found. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUDIT-005. |
| **ERR-AUDIT-006** | `HTTP 500` | `AUDIT_LEDGER_WRITE_FAILED` | Failed to append record to immutable cryptographic audit log. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-AUDIT-006. |

## 8. Offline Edge Operation & Synchronization Mechanics

When WAN connectivity to the central cloud is disrupted, `Audit` operations transition to autonomous edge mode:
1. **Local SQLite WAL Database:** Transactions are committed locally to `/data/namma_clinic_edge.db` on the clinic's Intel N100 mini-server.
2. **Offline Mutation Journal:** Every INSERT, UPDATE, and SOFT_DELETE appends a record to the `offline_mutation_log` table with a local vector clock.
3. **Conflict Resolution Policy:** Upon WAN restoration, the edge sync agent uploads buffered mutations in batches of 100 to `/api/v1/system/sync/batch`. Conflicts are resolved deterministically using Last-Write-Wins (LWW) with microsecond Lamport timestamps, except for clinical records where doctor entries take precedence over clerical updates.
4. **Storage Quotas:** Up to 72 hours of offline operations (approximately 15,000 mutations) can be buffered without storage degradation.

## 9. Security, Data Protection & DPDP Act Compliance

Data protection invariants for `Audit` operations:

| Data Element | Classification | Encryption Standard | Masking Rule | DPDP Act Section | Retention Schedule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Core Entity Record | `INTERNAL` | AES-256-GCM Column Level | Masked on non-admin UI | Section 8 (Data Security) | 10 Years (Medical Records) |
| Transaction Mutation | INTERNAL | TLS 1.3 in Transit | Zero PII in Gateway Logs | Section 6 (Consent Notice) | 10 Years (Audit Ledger) |
| WORM Audit Log | HIGHLY-RESTRICTED | HMAC SHA-256 Chained | Full Hash Ledger | Section 12 (Citizen Rights) | Permanent (Statutory Archive) |

## 10. Domain Quality Acceptance Criteria (BDD)

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify Successful Execution of Create New WORM Audit Ledger Record
  Given an authenticated staff member with role 'ROLE-011'
  And an active clinical shift rostered in clinic facility '018e3a20-0008-7000-8000-000000000001'
  When the client sends a valid request to /api/v1/audit
  Then the server processes the request within 1500ms
  And returns HTTP 201
  And the response conforms to envelope schema 'StandardApiResponseEnvelope'
  And an immutable audit log is appended to 'AUDIT-EVENT-020'
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Reject Unauthorized Call to Create New WORM Audit Ledger Record
  Given a caller presenting an invalid or expired Bearer token
  And requesting protected resource access
  When the caller transmits a request to /api/v1/audit
  Then the API gateway intercepts the request
  And returns HTTP 401 Unauthorized
  And returns error code 'ERR-AUTH-002' or 'ERR-AUTH-003'
  And rejects access before invoking backend services
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Execute Create New WORM Audit Ledger Record in Autonomous Edge Mode
  Given the clinic workstation has lost WAN connectivity to cloud
  And the local edge mini-server is operational with local SQLite database
  When the staff member executes Create New WORM Audit Ledger Record
  Then the edge API gateway accepts the request locally
  And returns HTTP 201 within 250ms
  And appends the mutation to the local offline sync journal
  And synchronizes to cloud automatically upon network restoration
```

## 11. Requirements & Database Relational Traceability Matrix

Traceability mapping for all `Audit` endpoints:

| Endpoint ID | Upstream SRS Requirements | Workflow ID | Feature Code | Target Database Tables | Verification Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `API-AUDIT-001` | `SRS-FR-020, SRS-NFR-020` | `WF-010` | `FEATURE-080` | `audit_events` | `PLANNED-TEST-API-259` |
| `API-AUDIT-002` | `SRS-FR-021, SRS-NFR-021` | `WF-011` | `FEATURE-081` | `audit_events` | `PLANNED-TEST-API-260` |
| `API-AUDIT-003` | `SRS-FR-022, SRS-NFR-022` | `WF-012` | `FEATURE-082` | `audit_events` | `PLANNED-TEST-API-261` |
| `API-AUDIT-004` | `SRS-FR-023, SRS-NFR-023` | `WF-013` | `FEATURE-083` | `audit_events` | `PLANNED-TEST-API-262` |
| `API-AUDIT-005` | `SRS-FR-024, SRS-NFR-024` | `WF-014` | `FEATURE-084` | `audit_events` | `PLANNED-TEST-API-263` |
| `API-AUDIT-006` | `SRS-FR-025, SRS-NFR-025` | `WF-015` | `FEATURE-085` | `audit_events` | `PLANNED-TEST-API-264` |
| `API-AUDIT-007` | `SRS-FR-026, SRS-NFR-026` | `WF-016` | `FEATURE-086` | `audit_events` | `PLANNED-TEST-API-265` |
| `API-AUDIT-008` | `SRS-FR-027, SRS-NFR-027` | `WF-017` | `FEATURE-087` | `audit_events` | `PLANNED-TEST-API-266` |
| `API-AUDIT-009` | `SRS-FR-028, SRS-NFR-028` | `WF-018` | `FEATURE-088` | `audit_events` | `PLANNED-TEST-API-267` |
| `API-AUDIT-010` | `SRS-FR-029, SRS-NFR-029` | `WF-019` | `FEATURE-089` | `audit_events` | `PLANNED-TEST-API-268` |
| `API-AUDIT-011` | `SRS-FR-030, SRS-NFR-030` | `WF-020` | `FEATURE-090` | `audit_events` | `PLANNED-TEST-API-269` |
| `API-AUDIT-012` | `SRS-FR-031, SRS-NFR-031` | `WF-021` | `FEATURE-091` | `audit_events` | `PLANNED-TEST-API-270` |
| `API-AUDIT-013` | `SRS-FR-032, SRS-NFR-032` | `WF-022` | `FEATURE-092` | `audit_events` | `PLANNED-TEST-API-271` |
| `API-AUDIT-014` | `SRS-FR-033, SRS-NFR-033` | `WF-023` | `FEATURE-093` | `audit_events` | `PLANNED-TEST-API-272` |
| `API-AUDIT-015` | `SRS-FR-034, SRS-NFR-034` | `WF-024` | `FEATURE-094` | `audit_events` | `PLANNED-TEST-API-273` |
| `API-AUDIT-016` | `SRS-FR-035, SRS-NFR-035` | `WF-025` | `FEATURE-095` | `audit_events` | `PLANNED-TEST-API-274` |
| `API-AUDIT-017` | `SRS-FR-036, SRS-NFR-036` | `WF-001` | `FEATURE-096` | `audit_events` | `PLANNED-TEST-API-275` |
| `API-AUDIT-018` | `SRS-FR-037, SRS-NFR-037` | `WF-002` | `FEATURE-097` | `audit_events` | `PLANNED-TEST-API-276` |
| `API-AUDIT-019` | `SRS-FR-038, SRS-NFR-038` | `WF-003` | `FEATURE-098` | `audit_events` | `PLANNED-TEST-API-277` |
