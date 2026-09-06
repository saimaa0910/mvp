# 🔌 API Specification: Citizen Data Portability & DPDP Act Rights API Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-18 | **Status:** Authoritative Baseline | **Date:** September 2026
> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Standard Framework:** RFC 7231 (HTTP/1.1), JSON:API v1.1, DPDP Act 2023, ABDM Interoperability Standards
> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.

---

## 1. Executive Summary & Domain Scope

The **Citizen Data Portability & DPDP Act Rights API Specification** defines the authoritative, implementation-ready contracts for the `Portability` subsystem across all 183 Namma Clinic primary healthcare centers in Greater Bengaluru. This domain operates under the supervisory jurisdiction of `ROLE-011 (Data Protection Officer) / Citizen Self-Service` and fulfills the core mission: **Implement Section 12 of the Digital Personal Data Protection (DPDP) Act 2023, enabling citizens to request complete digital archives of their health records in FHIR, CSV, or password-encrypted PDF formats.**

All 17 endpoints specified in this document adhere strictly to uniform JSON:API response envelopes, time-ordered UUIDv7 identifiers, ISO-8601 UTC timestamps, optimistic concurrency control via ETags, and automated audit logging.

## 2. Operational Architecture & Relational Mapping

The following table maps the domain's operational context to architectural containers, components, database tables, and default role entitlements:

| Dimension | Specification Detail |
| :--- | :--- |
| **Functional Domain** | `Portability` (Code: `PORT`) |
| **Authoritative Endpoints** | 17 Active Endpoints (`API-PORT-001` to `API-PORT-017`) |
| **Primary Architecture Container** | `ARCH-CONT-005` |
| **Assigned Component** | `ARCH-COMP-013` |
| **Primary Database Tables** | `patients, consent_records, clinical_encounters` |
| **Lead Role Entitlement** | `ROLE-011 (Data Protection Officer) / Citizen Self-Service` |
| **Default Rate Limiting** | `60 req/min per User` |
| **Offline Edge Support** | `Cloud Only` |

## 3. Domain Operational State Machine

The operational state transitions governing entities within this domain are modeled below:

```mermaid
stateDiagram-v2
    [*] --> RequestSubmitted: Citizen Requests Full Data Export
    RequestSubmitted --> IdentityVerified: Citizen Authenticated via Mobile OTP
    IdentityVerified --> JobQueued: Asynchronous Export Worker Enqueued
    JobQueued --> CompilingData: Extracting Encounters, Vitals, Drugs, Labs
    CompilingData --> GeneratingArchive: Packaging Password-Encrypted ZIP / PDF
    GeneratingArchive --> S3Staged: Uploaded to Ephemeral Pre-Signed S3 Bucket
    S3Staged --> LinkDelivered: SMS with Temporary Download Link Sent
    LinkDelivered --> Downloaded: Citizen Downloads Archive
    S3Staged --> Expired: 30-Minute Validity Window Elapses (File Purged)
    Downloaded --> Expired
    Expired --> [*]
```

## 4. End-to-End Operational Data Flow

The sequence diagram below illustrates the end-to-end operational flow between frontline clinic staff, edge workstations, the central API gateway, and backing data stores:

```mermaid
sequenceDiagram
    autonumber
    participant Citizen as Citizen Patient
    participant Portal as Citizen Health Portal
    participant API as Portability API
    participant Worker as BullMQ Export Worker
    participant S3 as Secure Ephemeral S3 Storage
    Citizen->>Portal: Request Health Data Export (DPDP Section 12)
    Portal->>API: POST /api/v1/portability/jobs
    API->>Worker: Enqueue Export Task (Job ID: 018e3a20-...)
    API-->>Portal: HTTP 202 Accepted (Job Queued)
    Worker->>Worker: Assemble FHIR Records & Encrypt Archive
    Worker->>S3: Upload Archive (30-Minute Auto-Purge Policy)
    Worker-->>Citizen: Send SMS with Pre-Signed Download Link
```

## 5. Domain Endpoint Inventory Catalog

Complete inventory of all 17 endpoints defined for the `Portability` domain:

| Endpoint ID | Method | URI Route Path | Functional Title | Role Context | Idempotency Standard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API-PORT-001** | `POST` | `/api/v1/portability` | Create New Data Portability Record | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-PORT-002** | `GET` | `/api/v1/portability/{portabilityId}` | Retrieve Data Portability Details by ID | `ROLE-011` | Read-Only Idempotent |
| **API-PORT-003** | `GET` | `/api/v1/portability` | List and Filter Data Portability Records | `ROLE-011` | Read-Only Idempotent |
| **API-PORT-004** | `PUT` | `/api/v1/portability/{portabilityId}` | Update Full Data Portability Specification | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-PORT-005** | `PATCH` | `/api/v1/portability/{portabilityId}/status` | Update Data Portability Operational State | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-PORT-006** | `GET` | `/api/v1/portability/{portabilityId}/search` | Search Data Portability Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-PORT-007** | `GET` | `/api/v1/portability/history` | History Data Portability Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-PORT-008** | `GET` | `/api/v1/portability/{portabilityId}/audit` | Audit Data Portability Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-PORT-009** | `POST` | `/api/v1/portability/cancel` | Cancel Data Portability Workflow Operation | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-PORT-010** | `POST` | `/api/v1/portability/verify` | Verify Data Portability Workflow Operation | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-PORT-011** | `GET` | `/api/v1/portability/export` | Export Data Portability Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-PORT-012** | `GET` | `/api/v1/portability/{portabilityId}/metrics` | Metrics Data Portability Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-PORT-013** | `POST` | `/api/v1/portability/reconcile` | Reconcile Data Portability Workflow Operation | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-PORT-014** | `POST` | `/api/v1/portability/batch` | Batch Data Portability Workflow Operation | `ROLE-011` | Supported via X-Idempotency-Key |
| **API-PORT-015** | `GET` | `/api/v1/portability/sync` | Sync Data Portability Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-PORT-016** | `GET` | `/api/v1/portability/{portabilityId}/alerts` | Alerts Data Portability Workflow Operation | `ROLE-011` | Read-Only Idempotent |
| **API-PORT-017** | `POST` | `/api/v1/portability/escalate` | Escalate Data Portability Workflow Operation | `ROLE-011` | Supported via X-Idempotency-Key |

## 6. Comprehensive Endpoint Technical Specifications

Exhaustive technical contracts for all 17 endpoints in the `Portability` domain:

### 6.1 `API-PORT-001`: Create New Data Portability Record

- **API Identifier:** `API-PORT-001`
- **HTTP Route:** `POST /api/v1/portability`
- **Functional Purpose:** Authoritative specification for create new data portability record within Portability operations.
- **Product Capability:** `CAPABILITY-125` | **Feature Code:** `FEATURE-125`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:post`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-005, SRS-NFR-025` | **Workflow:** `WF-005`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-005`
- **Planned Verification Test Case:** `PLANNED-TEST-API-304`
- **Dependency DAG Edge:** `API-DEP-005`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability:
    post:
      summary: "Create New Data Portability Record"
      tags:
        - "Portability"
      operationId: "post_api_v1_portability"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability" \
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
  "operation": "Create New Data Portability Record",
  "domain": "Portability",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PORT-001"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-001",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-001.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-005` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-304` under simulated offline network conditions.

### 6.2 `API-PORT-002`: Retrieve Data Portability Details by ID

- **API Identifier:** `API-PORT-002`
- **HTTP Route:** `GET /api/v1/portability/{portabilityId}`
- **Functional Purpose:** Authoritative specification for retrieve data portability details by id within Portability operations.
- **Product Capability:** `CAPABILITY-126` | **Feature Code:** `FEATURE-126`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:get`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-006, SRS-NFR-026` | **Workflow:** `WF-006`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-006`
- **Planned Verification Test Case:** `PLANNED-TEST-API-305`
- **Dependency DAG Edge:** `API-DEP-006`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/{portabilityId}:
    get:
      summary: "Retrieve Data Portability Details by ID"
      tags:
        - "Portability"
      operationId: "get_api_v1_portability_portabilityId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/{portabilityId}" \
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
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-002",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-002.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-006` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-305` under simulated offline network conditions.

### 6.3 `API-PORT-003`: List and Filter Data Portability Records

- **API Identifier:** `API-PORT-003`
- **HTTP Route:** `GET /api/v1/portability`
- **Functional Purpose:** Authoritative specification for list and filter data portability records within Portability operations.
- **Product Capability:** `CAPABILITY-127` | **Feature Code:** `FEATURE-127`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:get`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-007, SRS-NFR-027` | **Workflow:** `WF-007`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-007`
- **Planned Verification Test Case:** `PLANNED-TEST-API-306`
- **Dependency DAG Edge:** `API-DEP-007`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability:
    get:
      summary: "List and Filter Data Portability Records"
      tags:
        - "Portability"
      operationId: "get_api_v1_portability"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability" \
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
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-003",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-003.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-007` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-306` under simulated offline network conditions.

### 6.4 `API-PORT-004`: Update Full Data Portability Specification

- **API Identifier:** `API-PORT-004`
- **HTTP Route:** `PUT /api/v1/portability/{portabilityId}`
- **Functional Purpose:** Authoritative specification for update full data portability specification within Portability operations.
- **Product Capability:** `CAPABILITY-128` | **Feature Code:** `FEATURE-128`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:put`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-008, SRS-NFR-028` | **Workflow:** `WF-008`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-008`
- **Planned Verification Test Case:** `PLANNED-TEST-API-307`
- **Dependency DAG Edge:** `API-DEP-008`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/{portabilityId}:
    put:
      summary: "Update Full Data Portability Specification"
      tags:
        - "Portability"
      operationId: "put_api_v1_portability_portabilityId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/{portabilityId}" \
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
  "operation": "Update Full Data Portability Specification",
  "domain": "Portability",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PORT-004"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-004",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-004.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-008` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-307` under simulated offline network conditions.

### 6.5 `API-PORT-005`: Update Data Portability Operational State

- **API Identifier:** `API-PORT-005`
- **HTTP Route:** `PATCH /api/v1/portability/{portabilityId}/status`
- **Functional Purpose:** Authoritative specification for update data portability operational state within Portability operations.
- **Product Capability:** `CAPABILITY-129` | **Feature Code:** `FEATURE-129`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:patch`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-009, SRS-NFR-029` | **Workflow:** `WF-009`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-009`
- **Planned Verification Test Case:** `PLANNED-TEST-API-308`
- **Dependency DAG Edge:** `API-DEP-009`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/{portabilityId}/status:
    patch:
      summary: "Update Data Portability Operational State"
      tags:
        - "Portability"
      operationId: "patch_api_v1_portability_portabilityId_status"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/{portabilityId}/status" \
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
  "operation": "Update Data Portability Operational State",
  "domain": "Portability",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PORT-005"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-005",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-005.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-009` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-308` under simulated offline network conditions.

### 6.6 `API-PORT-006`: Search Data Portability Workflow Operation

- **API Identifier:** `API-PORT-006`
- **HTTP Route:** `GET /api/v1/portability/{portabilityId}/search`
- **Functional Purpose:** Authoritative specification for search data portability workflow operation within Portability operations.
- **Product Capability:** `CAPABILITY-130` | **Feature Code:** `FEATURE-130`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:get`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-010, SRS-NFR-030` | **Workflow:** `WF-010`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-010`
- **Planned Verification Test Case:** `PLANNED-TEST-API-309`
- **Dependency DAG Edge:** `API-DEP-010`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/{portabilityId}/search:
    get:
      summary: "Search Data Portability Workflow Operation"
      tags:
        - "Portability"
      operationId: "get_api_v1_portability_portabilityId_search"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/{portabilityId}/search" \
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
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-006",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-006.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-010` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-309` under simulated offline network conditions.

### 6.7 `API-PORT-007`: History Data Portability Workflow Operation

- **API Identifier:** `API-PORT-007`
- **HTTP Route:** `GET /api/v1/portability/history`
- **Functional Purpose:** Authoritative specification for history data portability workflow operation within Portability operations.
- **Product Capability:** `CAPABILITY-131` | **Feature Code:** `FEATURE-131`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:get`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-011, SRS-NFR-031` | **Workflow:** `WF-011`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-011`
- **Planned Verification Test Case:** `PLANNED-TEST-API-310`
- **Dependency DAG Edge:** `API-DEP-011`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/history:
    get:
      summary: "History Data Portability Workflow Operation"
      tags:
        - "Portability"
      operationId: "get_api_v1_portability_history"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/history" \
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
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-007",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-007.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-011` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-310` under simulated offline network conditions.

### 6.8 `API-PORT-008`: Audit Data Portability Workflow Operation

- **API Identifier:** `API-PORT-008`
- **HTTP Route:** `GET /api/v1/portability/{portabilityId}/audit`
- **Functional Purpose:** Authoritative specification for audit data portability workflow operation within Portability operations.
- **Product Capability:** `CAPABILITY-132` | **Feature Code:** `FEATURE-132`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:get`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-012, SRS-NFR-032` | **Workflow:** `WF-012`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-012`
- **Planned Verification Test Case:** `PLANNED-TEST-API-311`
- **Dependency DAG Edge:** `API-DEP-012`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/{portabilityId}/audit:
    get:
      summary: "Audit Data Portability Workflow Operation"
      tags:
        - "Portability"
      operationId: "get_api_v1_portability_portabilityId_audit"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/{portabilityId}/audit" \
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
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-008",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-008.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-012` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-311` under simulated offline network conditions.

### 6.9 `API-PORT-009`: Cancel Data Portability Workflow Operation

- **API Identifier:** `API-PORT-009`
- **HTTP Route:** `POST /api/v1/portability/cancel`
- **Functional Purpose:** Authoritative specification for cancel data portability workflow operation within Portability operations.
- **Product Capability:** `CAPABILITY-133` | **Feature Code:** `FEATURE-133`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:post`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-013, SRS-NFR-033` | **Workflow:** `WF-013`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-013`
- **Planned Verification Test Case:** `PLANNED-TEST-API-312`
- **Dependency DAG Edge:** `API-DEP-013`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/cancel:
    post:
      summary: "Cancel Data Portability Workflow Operation"
      tags:
        - "Portability"
      operationId: "post_api_v1_portability_cancel"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/cancel" \
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
  "operation": "Cancel Data Portability Workflow Operation",
  "domain": "Portability",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PORT-009"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-009",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-009.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-013` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-312` under simulated offline network conditions.

### 6.10 `API-PORT-010`: Verify Data Portability Workflow Operation

- **API Identifier:** `API-PORT-010`
- **HTTP Route:** `POST /api/v1/portability/verify`
- **Functional Purpose:** Authoritative specification for verify data portability workflow operation within Portability operations.
- **Product Capability:** `CAPABILITY-134` | **Feature Code:** `FEATURE-134`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:post`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-014, SRS-NFR-034` | **Workflow:** `WF-014`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-014`
- **Planned Verification Test Case:** `PLANNED-TEST-API-313`
- **Dependency DAG Edge:** `API-DEP-014`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/verify:
    post:
      summary: "Verify Data Portability Workflow Operation"
      tags:
        - "Portability"
      operationId: "post_api_v1_portability_verify"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/verify" \
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
  "operation": "Verify Data Portability Workflow Operation",
  "domain": "Portability",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PORT-010"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-010",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-010.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-014` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-313` under simulated offline network conditions.

### 6.11 `API-PORT-011`: Export Data Portability Workflow Operation

- **API Identifier:** `API-PORT-011`
- **HTTP Route:** `GET /api/v1/portability/export`
- **Functional Purpose:** Authoritative specification for export data portability workflow operation within Portability operations.
- **Product Capability:** `CAPABILITY-135` | **Feature Code:** `FEATURE-135`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:get`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-015, SRS-NFR-035` | **Workflow:** `WF-015`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-015`
- **Planned Verification Test Case:** `PLANNED-TEST-API-314`
- **Dependency DAG Edge:** `API-DEP-015`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/export:
    get:
      summary: "Export Data Portability Workflow Operation"
      tags:
        - "Portability"
      operationId: "get_api_v1_portability_export"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/export" \
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
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-011",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-011.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-015` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-314` under simulated offline network conditions.

### 6.12 `API-PORT-012`: Metrics Data Portability Workflow Operation

- **API Identifier:** `API-PORT-012`
- **HTTP Route:** `GET /api/v1/portability/{portabilityId}/metrics`
- **Functional Purpose:** Authoritative specification for metrics data portability workflow operation within Portability operations.
- **Product Capability:** `CAPABILITY-136` | **Feature Code:** `FEATURE-136`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:get`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-016, SRS-NFR-036` | **Workflow:** `WF-016`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-016`
- **Planned Verification Test Case:** `PLANNED-TEST-API-315`
- **Dependency DAG Edge:** `API-DEP-016`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/{portabilityId}/metrics:
    get:
      summary: "Metrics Data Portability Workflow Operation"
      tags:
        - "Portability"
      operationId: "get_api_v1_portability_portabilityId_metrics"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/{portabilityId}/metrics" \
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
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-012",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-012.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-016` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-315` under simulated offline network conditions.

### 6.13 `API-PORT-013`: Reconcile Data Portability Workflow Operation

- **API Identifier:** `API-PORT-013`
- **HTTP Route:** `POST /api/v1/portability/reconcile`
- **Functional Purpose:** Authoritative specification for reconcile data portability workflow operation within Portability operations.
- **Product Capability:** `CAPABILITY-137` | **Feature Code:** `FEATURE-137`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:post`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-017, SRS-NFR-037` | **Workflow:** `WF-017`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-017`
- **Planned Verification Test Case:** `PLANNED-TEST-API-316`
- **Dependency DAG Edge:** `API-DEP-017`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/reconcile:
    post:
      summary: "Reconcile Data Portability Workflow Operation"
      tags:
        - "Portability"
      operationId: "post_api_v1_portability_reconcile"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/reconcile" \
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
  "operation": "Reconcile Data Portability Workflow Operation",
  "domain": "Portability",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PORT-013"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-013",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-013.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-017` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-316` under simulated offline network conditions.

### 6.14 `API-PORT-014`: Batch Data Portability Workflow Operation

- **API Identifier:** `API-PORT-014`
- **HTTP Route:** `POST /api/v1/portability/batch`
- **Functional Purpose:** Authoritative specification for batch data portability workflow operation within Portability operations.
- **Product Capability:** `CAPABILITY-138` | **Feature Code:** `FEATURE-138`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:post`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-018, SRS-NFR-038` | **Workflow:** `WF-018`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-018`
- **Planned Verification Test Case:** `PLANNED-TEST-API-317`
- **Dependency DAG Edge:** `API-DEP-018`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/batch:
    post:
      summary: "Batch Data Portability Workflow Operation"
      tags:
        - "Portability"
      operationId: "post_api_v1_portability_batch"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/batch" \
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
  "operation": "Batch Data Portability Workflow Operation",
  "domain": "Portability",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PORT-014"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-014",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-014.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-018` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-317` under simulated offline network conditions.

### 6.15 `API-PORT-015`: Sync Data Portability Workflow Operation

- **API Identifier:** `API-PORT-015`
- **HTTP Route:** `GET /api/v1/portability/sync`
- **Functional Purpose:** Authoritative specification for sync data portability workflow operation within Portability operations.
- **Product Capability:** `CAPABILITY-139` | **Feature Code:** `FEATURE-139`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:get`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-019, SRS-NFR-039` | **Workflow:** `WF-019`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-019`
- **Planned Verification Test Case:** `PLANNED-TEST-API-318`
- **Dependency DAG Edge:** `API-DEP-019`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/sync:
    get:
      summary: "Sync Data Portability Workflow Operation"
      tags:
        - "Portability"
      operationId: "get_api_v1_portability_sync"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/sync" \
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
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-015",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-015.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-019` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-318` under simulated offline network conditions.

### 6.16 `API-PORT-016`: Alerts Data Portability Workflow Operation

- **API Identifier:** `API-PORT-016`
- **HTTP Route:** `GET /api/v1/portability/{portabilityId}/alerts`
- **Functional Purpose:** Authoritative specification for alerts data portability workflow operation within Portability operations.
- **Product Capability:** `CAPABILITY-140` | **Feature Code:** `FEATURE-140`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:get`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-020, SRS-NFR-040` | **Workflow:** `WF-020`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-020`
- **Planned Verification Test Case:** `PLANNED-TEST-API-319`
- **Dependency DAG Edge:** `API-DEP-020`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/{portabilityId}/alerts:
    get:
      summary: "Alerts Data Portability Workflow Operation"
      tags:
        - "Portability"
      operationId: "get_api_v1_portability_portabilityId_alerts"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/{portabilityId}/alerts" \
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
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-016",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-016.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-020` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-319` under simulated offline network conditions.

### 6.17 `API-PORT-017`: Escalate Data Portability Workflow Operation

- **API Identifier:** `API-PORT-017`
- **HTTP Route:** `POST /api/v1/portability/escalate`
- **Functional Purpose:** Authoritative specification for escalate data portability workflow operation within Portability operations.
- **Product Capability:** `CAPABILITY-141` | **Feature Code:** `FEATURE-141`
- **Primary Actor:** Authorized Portability Operator | **User Persona:** Portability Care Team Persona
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `portability:post`
- **ABAC Scoping Rule:** Restricted to authorized Portability personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-021, SRS-NFR-001` | **Workflow:** `WF-021`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, consent_records, clinical_encounters`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-021`
- **Planned Verification Test Case:** `PLANNED-TEST-API-320`
- **Dependency DAG Edge:** `API-DEP-021`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/portability/escalate:
    post:
      summary: "Escalate Data Portability Workflow Operation"
      tags:
        - "Portability"
      operationId: "post_api_v1_portability_escalate"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/portability/escalate" \
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
  "operation": "Escalate Data Portability Workflow Operation",
  "domain": "Portability",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PORT-017"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "portability",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PORT-017",
      "domain": "Portability",
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
    "code": "ERR-PORT-001",
    "message": "Domain constraint validation failed during execution of API-PORT-017.",
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
- **Relational Database Mutation:** Modifies tables `patients, consent_records, clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-021` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-320` under simulated offline network conditions.

## 7. Domain-Specific Error Code Catalog & Troubleshooting Runbooks

The following standardized error codes are specifically emitted by `Portability` services:

| Error Code ID | HTTP Status | Machine Code | Message Summary | Retryable | Resolution Runbook |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-PORT-001** | `HTTP 404` | `PORT_JOB_NOT_FOUND` | Data portability export task identifier does not exist. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PORT-001. |
| **ERR-PORT-002** | `HTTP 409` | `PORT_JOB_IN_PROGRESS` | A data export job is already running for this citizen. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PORT-002. |
| **ERR-PORT-003** | `HTTP 410` | `PORT_DOWNLOAD_LINK_EXPIRED` | Pre-signed download link has expired (30-minute validity window elapsed). | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PORT-003. |
| **ERR-PORT-004** | `HTTP 403` | `PORT_UNAUTHORIZED_CLAIMANT` | Export download permitted only by verified citizen or legal guardian. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PORT-004. |
| **ERR-PORT-005** | `HTTP 500` | `PORT_ARCHIVE_GENERATION_FAILED` | Background job failed to package encrypted export archive. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-PORT-005. |
| **ERR-PORT-006** | `HTTP 400` | `PORT_INVALID_EXPORT_FORMAT` | Requested export format must be FHIR_JSON, NDJSON, CSV_ZIP, or PDF_ENCRYPTED. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PORT-006. |

## 8. Offline Edge Operation & Synchronization Mechanics

When WAN connectivity to the central cloud is disrupted, `Portability` operations transition to autonomous edge mode:
1. **Local SQLite WAL Database:** Transactions are committed locally to `/data/namma_clinic_edge.db` on the clinic's Intel N100 mini-server.
2. **Offline Mutation Journal:** Every INSERT, UPDATE, and SOFT_DELETE appends a record to the `offline_mutation_log` table with a local vector clock.
3. **Conflict Resolution Policy:** Upon WAN restoration, the edge sync agent uploads buffered mutations in batches of 100 to `/api/v1/system/sync/batch`. Conflicts are resolved deterministically using Last-Write-Wins (LWW) with microsecond Lamport timestamps, except for clinical records where doctor entries take precedence over clerical updates.
4. **Storage Quotas:** Up to 72 hours of offline operations (approximately 15,000 mutations) can be buffered without storage degradation.

## 9. Security, Data Protection & DPDP Act Compliance

Data protection invariants for `Portability` operations:

| Data Element | Classification | Encryption Standard | Masking Rule | DPDP Act Section | Retention Schedule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Core Entity Record | `INTERNAL` | AES-256-GCM Column Level | Masked on non-admin UI | Section 8 (Data Security) | 10 Years (Medical Records) |
| Transaction Mutation | INTERNAL | TLS 1.3 in Transit | Zero PII in Gateway Logs | Section 6 (Consent Notice) | 10 Years (Audit Ledger) |
| WORM Audit Log | HIGHLY-RESTRICTED | HMAC SHA-256 Chained | Full Hash Ledger | Section 12 (Citizen Rights) | Permanent (Statutory Archive) |

## 10. Domain Quality Acceptance Criteria (BDD)

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify Successful Execution of Create New Data Portability Record
  Given an authenticated staff member with role 'ROLE-011'
  And an active clinical shift rostered in clinic facility '018e3a20-0008-7000-8000-000000000001'
  When the client sends a valid request to /api/v1/portability
  Then the server processes the request within 1500ms
  And returns HTTP 201
  And the response conforms to envelope schema 'StandardApiResponseEnvelope'
  And an immutable audit log is appended to 'AUDIT-EVENT-005'
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Reject Unauthorized Call to Create New Data Portability Record
  Given a caller presenting an invalid or expired Bearer token
  And requesting protected resource access
  When the caller transmits a request to /api/v1/portability
  Then the API gateway intercepts the request
  And returns HTTP 401 Unauthorized
  And returns error code 'ERR-AUTH-002' or 'ERR-AUTH-003'
  And rejects access before invoking backend services
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Execute Create New Data Portability Record in Autonomous Edge Mode
  Given the clinic workstation has lost WAN connectivity to cloud
  And the local edge mini-server is operational with local SQLite database
  When the staff member executes Create New Data Portability Record
  Then the edge API gateway accepts the request locally
  And returns HTTP 201 within 250ms
  And appends the mutation to the local offline sync journal
  And synchronizes to cloud automatically upon network restoration
```

## 11. Requirements & Database Relational Traceability Matrix

Traceability mapping for all `Portability` endpoints:

| Endpoint ID | Upstream SRS Requirements | Workflow ID | Feature Code | Target Database Tables | Verification Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `API-PORT-001` | `SRS-FR-005, SRS-NFR-025` | `WF-005` | `FEATURE-125` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-304` |
| `API-PORT-002` | `SRS-FR-006, SRS-NFR-026` | `WF-006` | `FEATURE-126` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-305` |
| `API-PORT-003` | `SRS-FR-007, SRS-NFR-027` | `WF-007` | `FEATURE-127` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-306` |
| `API-PORT-004` | `SRS-FR-008, SRS-NFR-028` | `WF-008` | `FEATURE-128` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-307` |
| `API-PORT-005` | `SRS-FR-009, SRS-NFR-029` | `WF-009` | `FEATURE-129` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-308` |
| `API-PORT-006` | `SRS-FR-010, SRS-NFR-030` | `WF-010` | `FEATURE-130` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-309` |
| `API-PORT-007` | `SRS-FR-011, SRS-NFR-031` | `WF-011` | `FEATURE-131` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-310` |
| `API-PORT-008` | `SRS-FR-012, SRS-NFR-032` | `WF-012` | `FEATURE-132` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-311` |
| `API-PORT-009` | `SRS-FR-013, SRS-NFR-033` | `WF-013` | `FEATURE-133` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-312` |
| `API-PORT-010` | `SRS-FR-014, SRS-NFR-034` | `WF-014` | `FEATURE-134` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-313` |
| `API-PORT-011` | `SRS-FR-015, SRS-NFR-035` | `WF-015` | `FEATURE-135` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-314` |
| `API-PORT-012` | `SRS-FR-016, SRS-NFR-036` | `WF-016` | `FEATURE-136` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-315` |
| `API-PORT-013` | `SRS-FR-017, SRS-NFR-037` | `WF-017` | `FEATURE-137` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-316` |
| `API-PORT-014` | `SRS-FR-018, SRS-NFR-038` | `WF-018` | `FEATURE-138` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-317` |
| `API-PORT-015` | `SRS-FR-019, SRS-NFR-039` | `WF-019` | `FEATURE-139` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-318` |
| `API-PORT-016` | `SRS-FR-020, SRS-NFR-040` | `WF-020` | `FEATURE-140` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-319` |
| `API-PORT-017` | `SRS-FR-021, SRS-NFR-001` | `WF-021` | `FEATURE-141` | `patients, consent_records, clinical_encounters` | `PLANNED-TEST-API-320` |
