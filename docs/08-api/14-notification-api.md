# 🔌 API Specification: Citizen Communications, SMS & WhatsApp Alerts API Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-14 | **Status:** Authoritative Baseline | **Date:** September 2026
> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Standard Framework:** RFC 7231 (HTTP/1.1), JSON:API v1.1, DPDP Act 2023, ABDM Interoperability Standards
> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.

---

## 1. Executive Summary & Domain Scope

The **Citizen Communications, SMS & WhatsApp Alerts API Specification** defines the authoritative, implementation-ready contracts for the `Notification` subsystem across all 183 Namma Clinic primary healthcare centers in Greater Bengaluru. This domain operates under the supervisory jurisdiction of `ROLE-014 (Community Coordinator / Automated Worker)` and fulfills the core mission: **Dispatch automated bilingual (Kannada and English) citizen notifications, appointment reminders, chronic disease NCD follow-up alerts, and epidemic advisories via DLT-approved telecom gateways.**

All 19 endpoints specified in this document adhere strictly to uniform JSON:API response envelopes, time-ordered UUIDv7 identifiers, ISO-8601 UTC timestamps, optimistic concurrency control via ETags, and automated audit logging.

## 2. Operational Architecture & Relational Mapping

The following table maps the domain's operational context to architectural containers, components, database tables, and default role entitlements:

| Dimension | Specification Detail |
| :--- | :--- |
| **Functional Domain** | `Notification` (Code: `NOTIF`) |
| **Authoritative Endpoints** | 19 Active Endpoints (`API-NOTIF-001` to `API-NOTIF-019`) |
| **Primary Architecture Container** | `ARCH-CONT-012` |
| **Assigned Component** | `ARCH-COMP-034` |
| **Primary Database Tables** | `notifications` |
| **Lead Role Entitlement** | `ROLE-014 (Community Coordinator / Automated Worker)` |
| **Default Rate Limiting** | `60 req/min per User` |
| **Offline Edge Support** | `Edge Local Queue with Delta Sync` |

## 3. Domain Operational State Machine

The operational state transitions governing entities within this domain are modeled below:

```mermaid
stateDiagram-v2
    [*] --> MessageEnqueued: Event Triggered (Encounter, Prescription)
    MessageEnqueued --> ConsentChecked: Verify Citizen Consent Preferences
    ConsentChecked --> DroppedConsentOptOut: Citizen Opted Out
    ConsentChecked --> TemplateRendered: Dynamic Variables Injected (Kannada)
    TemplateRendered --> DispatchedToCarrier: Sent via Telecom SMS Gateway
    DispatchedToCarrier --> Delivered: Carrier Delivery Receipt Confirmed
    DispatchedToCarrier --> RetryScheduled: Temporary Carrier Failure (Max 3)
    RetryScheduled --> DispatchedToCarrier: Backoff Delay Elapsed
    RetryScheduled --> Undelivered: Maximum Retries Exceeded
    Delivered --> [*]
    Undelivered --> [*]
```

## 4. End-to-End Operational Data Flow

The sequence diagram below illustrates the end-to-end operational flow between frontline clinic staff, edge workstations, the central API gateway, and backing data stores:

```mermaid
sequenceDiagram
    autonumber
    participant Worker as BullMQ Notification Worker
    participant API as Notification Service
    participant DLT as C-DAC / Telecom Gateway
    participant Citizen as Citizen Mobile Phone
    Worker->>API: POST /api/v1/notifications/send
    API->>API: Render DLT Template in Kannada
    API->>DLT: POST /sms/v1/transmit (HTTPS mTLS)
    DLT-->>Citizen: Deliver SMS Message
    DLT-->>API: Webhook Delivery Receipt (HTTP 200)
```

## 5. Domain Endpoint Inventory Catalog

Complete inventory of all 19 endpoints defined for the `Notification` domain:

| Endpoint ID | Method | URI Route Path | Functional Title | Role Context | Idempotency Standard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API-NOTIF-001** | `POST` | `/api/v1/notifications` | Create New Citizen Notification Record | `ROLE-014` | Supported via X-Idempotency-Key |
| **API-NOTIF-002** | `GET` | `/api/v1/notifications/{notificationId}` | Retrieve Citizen Notification Details by ID | `ROLE-014` | Read-Only Idempotent |
| **API-NOTIF-003** | `GET` | `/api/v1/notifications` | List and Filter Citizen Notification Records | `ROLE-014` | Read-Only Idempotent |
| **API-NOTIF-004** | `PUT` | `/api/v1/notifications/{notificationId}` | Update Full Citizen Notification Specification | `ROLE-014` | Supported via X-Idempotency-Key |
| **API-NOTIF-005** | `PATCH` | `/api/v1/notifications/{notificationId}/status` | Update Citizen Notification Operational State | `ROLE-014` | Supported via X-Idempotency-Key |
| **API-NOTIF-006** | `GET` | `/api/v1/notifications/{notificationId}/search` | Search Citizen Notification Workflow Operation | `ROLE-014` | Read-Only Idempotent |
| **API-NOTIF-007** | `GET` | `/api/v1/notifications/history` | History Citizen Notification Workflow Operation | `ROLE-014` | Read-Only Idempotent |
| **API-NOTIF-008** | `GET` | `/api/v1/notifications/{notificationId}/audit` | Audit Citizen Notification Workflow Operation | `ROLE-014` | Read-Only Idempotent |
| **API-NOTIF-009** | `POST` | `/api/v1/notifications/cancel` | Cancel Citizen Notification Workflow Operation | `ROLE-014` | Supported via X-Idempotency-Key |
| **API-NOTIF-010** | `POST` | `/api/v1/notifications/verify` | Verify Citizen Notification Workflow Operation | `ROLE-014` | Supported via X-Idempotency-Key |
| **API-NOTIF-011** | `GET` | `/api/v1/notifications/export` | Export Citizen Notification Workflow Operation | `ROLE-014` | Read-Only Idempotent |
| **API-NOTIF-012** | `GET` | `/api/v1/notifications/{notificationId}/metrics` | Metrics Citizen Notification Workflow Operation | `ROLE-014` | Read-Only Idempotent |
| **API-NOTIF-013** | `POST` | `/api/v1/notifications/reconcile` | Reconcile Citizen Notification Workflow Operation | `ROLE-014` | Supported via X-Idempotency-Key |
| **API-NOTIF-014** | `POST` | `/api/v1/notifications/batch` | Batch Citizen Notification Workflow Operation | `ROLE-014` | Supported via X-Idempotency-Key |
| **API-NOTIF-015** | `GET` | `/api/v1/notifications/sync` | Sync Citizen Notification Workflow Operation | `ROLE-014` | Read-Only Idempotent |
| **API-NOTIF-016** | `GET` | `/api/v1/notifications/{notificationId}/alerts` | Alerts Citizen Notification Workflow Operation | `ROLE-014` | Read-Only Idempotent |
| **API-NOTIF-017** | `POST` | `/api/v1/notifications/escalate` | Escalate Citizen Notification Workflow Operation | `ROLE-014` | Supported via X-Idempotency-Key |
| **API-NOTIF-018** | `POST` | `/api/v1/notifications/approve` | Approve Citizen Notification Workflow Operation | `ROLE-014` | Supported via X-Idempotency-Key |
| **API-NOTIF-019** | `POST` | `/api/v1/notifications/reversal` | Reversal Citizen Notification Workflow Operation | `ROLE-014` | Supported via X-Idempotency-Key |

## 6. Comprehensive Endpoint Technical Specifications

Exhaustive technical contracts for all 19 endpoints in the `Notification` domain:

### 6.1 `API-NOTIF-001`: Create New Citizen Notification Record

- **API Identifier:** `API-NOTIF-001`
- **HTTP Route:** `POST /api/v1/notifications`
- **Functional Purpose:** Authoritative specification for create new citizen notification record within Notification operations.
- **Product Capability:** `CAPABILITY-035` | **Feature Code:** `FEATURE-035`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:post`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-035, SRS-NFR-015` | **Workflow:** `WF-015`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-005`
- **Planned Verification Test Case:** `PLANNED-TEST-API-214`
- **Dependency DAG Edge:** `API-DEP-035`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications:
    post:
      summary: "Create New Citizen Notification Record"
      tags:
        - "Notification"
      operationId: "post_api_v1_notifications"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications" \
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
  "operation": "Create New Citizen Notification Record",
  "domain": "Notification",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-NOTIF-001"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-001",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-001.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-005` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-214` under simulated offline network conditions.

### 6.2 `API-NOTIF-002`: Retrieve Citizen Notification Details by ID

- **API Identifier:** `API-NOTIF-002`
- **HTTP Route:** `GET /api/v1/notifications/{notificationId}`
- **Functional Purpose:** Authoritative specification for retrieve citizen notification details by id within Notification operations.
- **Product Capability:** `CAPABILITY-036` | **Feature Code:** `FEATURE-036`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:get`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-036, SRS-NFR-016` | **Workflow:** `WF-016`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-006`
- **Planned Verification Test Case:** `PLANNED-TEST-API-215`
- **Dependency DAG Edge:** `API-DEP-036`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/{notificationId}:
    get:
      summary: "Retrieve Citizen Notification Details by ID"
      tags:
        - "Notification"
      operationId: "get_api_v1_notifications_notificationId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/{notificationId}" \
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
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-002",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-002.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-006` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-215` under simulated offline network conditions.

### 6.3 `API-NOTIF-003`: List and Filter Citizen Notification Records

- **API Identifier:** `API-NOTIF-003`
- **HTTP Route:** `GET /api/v1/notifications`
- **Functional Purpose:** Authoritative specification for list and filter citizen notification records within Notification operations.
- **Product Capability:** `CAPABILITY-037` | **Feature Code:** `FEATURE-037`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:get`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-037, SRS-NFR-017` | **Workflow:** `WF-017`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-007`
- **Planned Verification Test Case:** `PLANNED-TEST-API-216`
- **Dependency DAG Edge:** `API-DEP-037`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications:
    get:
      summary: "List and Filter Citizen Notification Records"
      tags:
        - "Notification"
      operationId: "get_api_v1_notifications"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications" \
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
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-003",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-003.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-007` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-216` under simulated offline network conditions.

### 6.4 `API-NOTIF-004`: Update Full Citizen Notification Specification

- **API Identifier:** `API-NOTIF-004`
- **HTTP Route:** `PUT /api/v1/notifications/{notificationId}`
- **Functional Purpose:** Authoritative specification for update full citizen notification specification within Notification operations.
- **Product Capability:** `CAPABILITY-038` | **Feature Code:** `FEATURE-038`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:put`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-038, SRS-NFR-018` | **Workflow:** `WF-018`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-008`
- **Planned Verification Test Case:** `PLANNED-TEST-API-217`
- **Dependency DAG Edge:** `API-DEP-038`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/{notificationId}:
    put:
      summary: "Update Full Citizen Notification Specification"
      tags:
        - "Notification"
      operationId: "put_api_v1_notifications_notificationId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/{notificationId}" \
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
  "operation": "Update Full Citizen Notification Specification",
  "domain": "Notification",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-NOTIF-004"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-004",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-004.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-008` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-217` under simulated offline network conditions.

### 6.5 `API-NOTIF-005`: Update Citizen Notification Operational State

- **API Identifier:** `API-NOTIF-005`
- **HTTP Route:** `PATCH /api/v1/notifications/{notificationId}/status`
- **Functional Purpose:** Authoritative specification for update citizen notification operational state within Notification operations.
- **Product Capability:** `CAPABILITY-039` | **Feature Code:** `FEATURE-039`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:patch`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-039, SRS-NFR-019` | **Workflow:** `WF-019`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-009`
- **Planned Verification Test Case:** `PLANNED-TEST-API-218`
- **Dependency DAG Edge:** `API-DEP-039`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/{notificationId}/status:
    patch:
      summary: "Update Citizen Notification Operational State"
      tags:
        - "Notification"
      operationId: "patch_api_v1_notifications_notificationId_status"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/{notificationId}/status" \
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
  "operation": "Update Citizen Notification Operational State",
  "domain": "Notification",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-NOTIF-005"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-005",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-005.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-009` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-218` under simulated offline network conditions.

### 6.6 `API-NOTIF-006`: Search Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-006`
- **HTTP Route:** `GET /api/v1/notifications/{notificationId}/search`
- **Functional Purpose:** Authoritative specification for search citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-040` | **Feature Code:** `FEATURE-040`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:get`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-040, SRS-NFR-020` | **Workflow:** `WF-020`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-010`
- **Planned Verification Test Case:** `PLANNED-TEST-API-219`
- **Dependency DAG Edge:** `API-DEP-040`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/{notificationId}/search:
    get:
      summary: "Search Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "get_api_v1_notifications_notificationId_search"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/{notificationId}/search" \
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
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-006",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-006.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-010` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-219` under simulated offline network conditions.

### 6.7 `API-NOTIF-007`: History Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-007`
- **HTTP Route:** `GET /api/v1/notifications/history`
- **Functional Purpose:** Authoritative specification for history citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-041` | **Feature Code:** `FEATURE-041`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:get`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-041, SRS-NFR-021` | **Workflow:** `WF-021`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-011`
- **Planned Verification Test Case:** `PLANNED-TEST-API-220`
- **Dependency DAG Edge:** `API-DEP-041`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/history:
    get:
      summary: "History Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "get_api_v1_notifications_history"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/history" \
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
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-007",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-007.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-011` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-220` under simulated offline network conditions.

### 6.8 `API-NOTIF-008`: Audit Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-008`
- **HTTP Route:** `GET /api/v1/notifications/{notificationId}/audit`
- **Functional Purpose:** Authoritative specification for audit citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-042` | **Feature Code:** `FEATURE-042`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:get`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-042, SRS-NFR-022` | **Workflow:** `WF-022`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-012`
- **Planned Verification Test Case:** `PLANNED-TEST-API-221`
- **Dependency DAG Edge:** `API-DEP-042`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/{notificationId}/audit:
    get:
      summary: "Audit Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "get_api_v1_notifications_notificationId_audit"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/{notificationId}/audit" \
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
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-008",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-008.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-012` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-221` under simulated offline network conditions.

### 6.9 `API-NOTIF-009`: Cancel Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-009`
- **HTTP Route:** `POST /api/v1/notifications/cancel`
- **Functional Purpose:** Authoritative specification for cancel citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-043` | **Feature Code:** `FEATURE-043`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:post`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-043, SRS-NFR-023` | **Workflow:** `WF-023`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-013`
- **Planned Verification Test Case:** `PLANNED-TEST-API-222`
- **Dependency DAG Edge:** `API-DEP-043`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/cancel:
    post:
      summary: "Cancel Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "post_api_v1_notifications_cancel"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/cancel" \
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
  "operation": "Cancel Citizen Notification Workflow Operation",
  "domain": "Notification",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-NOTIF-009"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-009",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-009.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-013` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-222` under simulated offline network conditions.

### 6.10 `API-NOTIF-010`: Verify Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-010`
- **HTTP Route:** `POST /api/v1/notifications/verify`
- **Functional Purpose:** Authoritative specification for verify citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-044` | **Feature Code:** `FEATURE-044`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:post`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-044, SRS-NFR-024` | **Workflow:** `WF-024`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-014`
- **Planned Verification Test Case:** `PLANNED-TEST-API-223`
- **Dependency DAG Edge:** `API-DEP-044`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/verify:
    post:
      summary: "Verify Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "post_api_v1_notifications_verify"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/verify" \
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
  "operation": "Verify Citizen Notification Workflow Operation",
  "domain": "Notification",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-NOTIF-010"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-010",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-010.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-014` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-223` under simulated offline network conditions.

### 6.11 `API-NOTIF-011`: Export Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-011`
- **HTTP Route:** `GET /api/v1/notifications/export`
- **Functional Purpose:** Authoritative specification for export citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-045` | **Feature Code:** `FEATURE-045`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:get`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-045, SRS-NFR-025` | **Workflow:** `WF-025`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-015`
- **Planned Verification Test Case:** `PLANNED-TEST-API-224`
- **Dependency DAG Edge:** `API-DEP-045`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/export:
    get:
      summary: "Export Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "get_api_v1_notifications_export"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/export" \
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
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-011",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-011.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-015` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-224` under simulated offline network conditions.

### 6.12 `API-NOTIF-012`: Metrics Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-012`
- **HTTP Route:** `GET /api/v1/notifications/{notificationId}/metrics`
- **Functional Purpose:** Authoritative specification for metrics citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-046` | **Feature Code:** `FEATURE-046`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:get`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-046, SRS-NFR-026` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-016`
- **Planned Verification Test Case:** `PLANNED-TEST-API-225`
- **Dependency DAG Edge:** `API-DEP-046`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/{notificationId}/metrics:
    get:
      summary: "Metrics Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "get_api_v1_notifications_notificationId_metrics"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/{notificationId}/metrics" \
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
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-012",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-012.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-016` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-225` under simulated offline network conditions.

### 6.13 `API-NOTIF-013`: Reconcile Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-013`
- **HTTP Route:** `POST /api/v1/notifications/reconcile`
- **Functional Purpose:** Authoritative specification for reconcile citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-047` | **Feature Code:** `FEATURE-047`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:post`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-047, SRS-NFR-027` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-017`
- **Planned Verification Test Case:** `PLANNED-TEST-API-226`
- **Dependency DAG Edge:** `API-DEP-047`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/reconcile:
    post:
      summary: "Reconcile Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "post_api_v1_notifications_reconcile"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/reconcile" \
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
  "operation": "Reconcile Citizen Notification Workflow Operation",
  "domain": "Notification",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-NOTIF-013"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-013",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-013.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-017` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-226` under simulated offline network conditions.

### 6.14 `API-NOTIF-014`: Batch Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-014`
- **HTTP Route:** `POST /api/v1/notifications/batch`
- **Functional Purpose:** Authoritative specification for batch citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-048` | **Feature Code:** `FEATURE-048`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:post`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-048, SRS-NFR-028` | **Workflow:** `WF-003`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-018`
- **Planned Verification Test Case:** `PLANNED-TEST-API-227`
- **Dependency DAG Edge:** `API-DEP-048`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/batch:
    post:
      summary: "Batch Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "post_api_v1_notifications_batch"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/batch" \
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
  "operation": "Batch Citizen Notification Workflow Operation",
  "domain": "Notification",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-NOTIF-014"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-014",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-014.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-018` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-227` under simulated offline network conditions.

### 6.15 `API-NOTIF-015`: Sync Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-015`
- **HTTP Route:** `GET /api/v1/notifications/sync`
- **Functional Purpose:** Authoritative specification for sync citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-049` | **Feature Code:** `FEATURE-049`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:get`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-049, SRS-NFR-029` | **Workflow:** `WF-004`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-019`
- **Planned Verification Test Case:** `PLANNED-TEST-API-228`
- **Dependency DAG Edge:** `API-DEP-049`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/sync:
    get:
      summary: "Sync Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "get_api_v1_notifications_sync"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/sync" \
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
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-015",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-015.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-019` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-228` under simulated offline network conditions.

### 6.16 `API-NOTIF-016`: Alerts Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-016`
- **HTTP Route:** `GET /api/v1/notifications/{notificationId}/alerts`
- **Functional Purpose:** Authoritative specification for alerts citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-050` | **Feature Code:** `FEATURE-050`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:get`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-050, SRS-NFR-030` | **Workflow:** `WF-005`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-020`
- **Planned Verification Test Case:** `PLANNED-TEST-API-229`
- **Dependency DAG Edge:** `API-DEP-050`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/{notificationId}/alerts:
    get:
      summary: "Alerts Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "get_api_v1_notifications_notificationId_alerts"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/{notificationId}/alerts" \
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
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-016",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-016.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-020` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-229` under simulated offline network conditions.

### 6.17 `API-NOTIF-017`: Escalate Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-017`
- **HTTP Route:** `POST /api/v1/notifications/escalate`
- **Functional Purpose:** Authoritative specification for escalate citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-051` | **Feature Code:** `FEATURE-051`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:post`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-051, SRS-NFR-031` | **Workflow:** `WF-006`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-021`
- **Planned Verification Test Case:** `PLANNED-TEST-API-230`
- **Dependency DAG Edge:** `API-DEP-051`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/escalate:
    post:
      summary: "Escalate Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "post_api_v1_notifications_escalate"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/escalate" \
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
  "operation": "Escalate Citizen Notification Workflow Operation",
  "domain": "Notification",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-NOTIF-017"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-017",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-017.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-021` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-230` under simulated offline network conditions.

### 6.18 `API-NOTIF-018`: Approve Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-018`
- **HTTP Route:** `POST /api/v1/notifications/approve`
- **Functional Purpose:** Authoritative specification for approve citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-052` | **Feature Code:** `FEATURE-052`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:post`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-052, SRS-NFR-032` | **Workflow:** `WF-007`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-022`
- **Planned Verification Test Case:** `PLANNED-TEST-API-231`
- **Dependency DAG Edge:** `API-DEP-052`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/approve:
    post:
      summary: "Approve Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "post_api_v1_notifications_approve"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/approve" \
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
  "operation": "Approve Citizen Notification Workflow Operation",
  "domain": "Notification",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-NOTIF-018"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-018",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-018.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-022` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-231` under simulated offline network conditions.

### 6.19 `API-NOTIF-019`: Reversal Citizen Notification Workflow Operation

- **API Identifier:** `API-NOTIF-019`
- **HTTP Route:** `POST /api/v1/notifications/reversal`
- **Functional Purpose:** Authoritative specification for reversal citizen notification workflow operation within Notification operations.
- **Product Capability:** `CAPABILITY-053` | **Feature Code:** `FEATURE-053`
- **Primary Actor:** Authorized Notification Operator | **User Persona:** Notification Care Team Persona
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `notifications:post`
- **ABAC Scoping Rule:** Restricted to authorized Notification personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-053, SRS-NFR-033` | **Workflow:** `WF-008`
- **Container / Component:** `ARCH-CONT-012` / `ARCH-COMP-034`
- **Target Relational Tables:** `notifications`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-023`
- **Planned Verification Test Case:** `PLANNED-TEST-API-232`
- **Dependency DAG Edge:** `API-DEP-053`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/notifications/reversal:
    post:
      summary: "Reversal Citizen Notification Workflow Operation"
      tags:
        - "Notification"
      operationId: "post_api_v1_notifications_reversal"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/notifications/reversal" \
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
  "operation": "Reversal Citizen Notification Workflow Operation",
  "domain": "Notification",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-NOTIF-019"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "notification",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-NOTIF-019",
      "domain": "Notification",
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
    "code": "ERR-NOTIF-001",
    "message": "Domain constraint validation failed during execution of API-NOTIF-019.",
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
- **Relational Database Mutation:** Modifies tables `notifications` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-023` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-232` under simulated offline network conditions.

## 7. Domain-Specific Error Code Catalog & Troubleshooting Runbooks

The following standardized error codes are specifically emitted by `Notification` services:

| Error Code ID | HTTP Status | Machine Code | Message Summary | Retryable | Resolution Runbook |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-NOTIF-001** | `HTTP 400` | `NOTIF_PHONE_CONSENT_OPT_OUT` | Citizen has opted out of automated promotional or advisory notifications. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-NOTIF-001. |
| **ERR-NOTIF-002** | `HTTP 404` | `NOTIF_TEMPLATE_NOT_FOUND` | DLT approved notification template ID is not configured. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-NOTIF-002. |
| **ERR-NOTIF-003** | `HTTP 429` | `NOTIF_RATE_LIMIT_EXCEEDED` | Citizen has received maximum allowable SMS alerts today (5 messages). | No | Verify client request format, ensure active session, and inspect audit logs for ERR-NOTIF-003. |
| **ERR-NOTIF-004** | `HTTP 400` | `NOTIF_TEMPLATE_PARAM_MISMATCH` | Provided template variable bindings do not match registered template spec. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-NOTIF-004. |
| **ERR-NOTIF-005** | `HTTP 502` | `NOTIF_SMS_GATEWAY_FAILURE` | State C-DAC / Telecom carrier SMS gateway returned upstream error. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-NOTIF-005. |
| **ERR-NOTIF-006** | `HTTP 504` | `NOTIF_CARRIER_TIMEOUT` | Carrier dispatch delivery confirmation timed out. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-NOTIF-006. |

## 8. Offline Edge Operation & Synchronization Mechanics

When WAN connectivity to the central cloud is disrupted, `Notification` operations transition to autonomous edge mode:
1. **Local SQLite WAL Database:** Transactions are committed locally to `/data/namma_clinic_edge.db` on the clinic's Intel N100 mini-server.
2. **Offline Mutation Journal:** Every INSERT, UPDATE, and SOFT_DELETE appends a record to the `offline_mutation_log` table with a local vector clock.
3. **Conflict Resolution Policy:** Upon WAN restoration, the edge sync agent uploads buffered mutations in batches of 100 to `/api/v1/system/sync/batch`. Conflicts are resolved deterministically using Last-Write-Wins (LWW) with microsecond Lamport timestamps, except for clinical records where doctor entries take precedence over clerical updates.
4. **Storage Quotas:** Up to 72 hours of offline operations (approximately 15,000 mutations) can be buffered without storage degradation.

## 9. Security, Data Protection & DPDP Act Compliance

Data protection invariants for `Notification` operations:

| Data Element | Classification | Encryption Standard | Masking Rule | DPDP Act Section | Retention Schedule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Core Entity Record | `INTERNAL` | AES-256-GCM Column Level | Masked on non-admin UI | Section 8 (Data Security) | 10 Years (Medical Records) |
| Transaction Mutation | INTERNAL | TLS 1.3 in Transit | Zero PII in Gateway Logs | Section 6 (Consent Notice) | 10 Years (Audit Ledger) |
| WORM Audit Log | HIGHLY-RESTRICTED | HMAC SHA-256 Chained | Full Hash Ledger | Section 12 (Citizen Rights) | Permanent (Statutory Archive) |

## 10. Domain Quality Acceptance Criteria (BDD)

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify Successful Execution of Create New Citizen Notification Record
  Given an authenticated staff member with role 'ROLE-014'
  And an active clinical shift rostered in clinic facility '018e3a20-0008-7000-8000-000000000001'
  When the client sends a valid request to /api/v1/notifications
  Then the server processes the request within 1500ms
  And returns HTTP 201
  And the response conforms to envelope schema 'StandardApiResponseEnvelope'
  And an immutable audit log is appended to 'AUDIT-EVENT-005'
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Reject Unauthorized Call to Create New Citizen Notification Record
  Given a caller presenting an invalid or expired Bearer token
  And requesting protected resource access
  When the caller transmits a request to /api/v1/notifications
  Then the API gateway intercepts the request
  And returns HTTP 401 Unauthorized
  And returns error code 'ERR-AUTH-002' or 'ERR-AUTH-003'
  And rejects access before invoking backend services
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Execute Create New Citizen Notification Record in Autonomous Edge Mode
  Given the clinic workstation has lost WAN connectivity to cloud
  And the local edge mini-server is operational with local SQLite database
  When the staff member executes Create New Citizen Notification Record
  Then the edge API gateway accepts the request locally
  And returns HTTP 201 within 250ms
  And appends the mutation to the local offline sync journal
  And synchronizes to cloud automatically upon network restoration
```

## 11. Requirements & Database Relational Traceability Matrix

Traceability mapping for all `Notification` endpoints:

| Endpoint ID | Upstream SRS Requirements | Workflow ID | Feature Code | Target Database Tables | Verification Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `API-NOTIF-001` | `SRS-FR-035, SRS-NFR-015` | `WF-015` | `FEATURE-035` | `notifications` | `PLANNED-TEST-API-214` |
| `API-NOTIF-002` | `SRS-FR-036, SRS-NFR-016` | `WF-016` | `FEATURE-036` | `notifications` | `PLANNED-TEST-API-215` |
| `API-NOTIF-003` | `SRS-FR-037, SRS-NFR-017` | `WF-017` | `FEATURE-037` | `notifications` | `PLANNED-TEST-API-216` |
| `API-NOTIF-004` | `SRS-FR-038, SRS-NFR-018` | `WF-018` | `FEATURE-038` | `notifications` | `PLANNED-TEST-API-217` |
| `API-NOTIF-005` | `SRS-FR-039, SRS-NFR-019` | `WF-019` | `FEATURE-039` | `notifications` | `PLANNED-TEST-API-218` |
| `API-NOTIF-006` | `SRS-FR-040, SRS-NFR-020` | `WF-020` | `FEATURE-040` | `notifications` | `PLANNED-TEST-API-219` |
| `API-NOTIF-007` | `SRS-FR-041, SRS-NFR-021` | `WF-021` | `FEATURE-041` | `notifications` | `PLANNED-TEST-API-220` |
| `API-NOTIF-008` | `SRS-FR-042, SRS-NFR-022` | `WF-022` | `FEATURE-042` | `notifications` | `PLANNED-TEST-API-221` |
| `API-NOTIF-009` | `SRS-FR-043, SRS-NFR-023` | `WF-023` | `FEATURE-043` | `notifications` | `PLANNED-TEST-API-222` |
| `API-NOTIF-010` | `SRS-FR-044, SRS-NFR-024` | `WF-024` | `FEATURE-044` | `notifications` | `PLANNED-TEST-API-223` |
| `API-NOTIF-011` | `SRS-FR-045, SRS-NFR-025` | `WF-025` | `FEATURE-045` | `notifications` | `PLANNED-TEST-API-224` |
| `API-NOTIF-012` | `SRS-FR-046, SRS-NFR-026` | `WF-001` | `FEATURE-046` | `notifications` | `PLANNED-TEST-API-225` |
| `API-NOTIF-013` | `SRS-FR-047, SRS-NFR-027` | `WF-002` | `FEATURE-047` | `notifications` | `PLANNED-TEST-API-226` |
| `API-NOTIF-014` | `SRS-FR-048, SRS-NFR-028` | `WF-003` | `FEATURE-048` | `notifications` | `PLANNED-TEST-API-227` |
| `API-NOTIF-015` | `SRS-FR-049, SRS-NFR-029` | `WF-004` | `FEATURE-049` | `notifications` | `PLANNED-TEST-API-228` |
| `API-NOTIF-016` | `SRS-FR-050, SRS-NFR-030` | `WF-005` | `FEATURE-050` | `notifications` | `PLANNED-TEST-API-229` |
| `API-NOTIF-017` | `SRS-FR-051, SRS-NFR-031` | `WF-006` | `FEATURE-051` | `notifications` | `PLANNED-TEST-API-230` |
| `API-NOTIF-018` | `SRS-FR-052, SRS-NFR-032` | `WF-007` | `FEATURE-052` | `notifications` | `PLANNED-TEST-API-231` |
| `API-NOTIF-019` | `SRS-FR-053, SRS-NFR-033` | `WF-008` | `FEATURE-053` | `notifications` | `PLANNED-TEST-API-232` |
