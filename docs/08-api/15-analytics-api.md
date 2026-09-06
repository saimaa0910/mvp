# 🔌 API Specification: Epidemic Surveillance, KPI Aggregation & Executive Analytics API Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-15 | **Status:** Authoritative Baseline | **Date:** September 2026
> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Standard Framework:** RFC 7231 (HTTP/1.1), JSON:API v1.1, DPDP Act 2023, ABDM Interoperability Standards
> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.

---

## 1. Executive Summary & Domain Scope

The **Epidemic Surveillance, KPI Aggregation & Executive Analytics API Specification** defines the authoritative, implementation-ready contracts for the `Analytics` subsystem across all 183 Namma Clinic primary healthcare centers in Greater Bengaluru. This domain operates under the supervisory jurisdiction of `ROLE-013 (Epidemiologist / BBMP Health Officer)` and fulfills the core mission: **Provide aggregated real-time epidemiological surveillance (syndromic dengue/fever tracking), clinic footfall metrics, doctor workloads, formulary stockout alerts, and municipal health KPIs.**

All 26 endpoints specified in this document adhere strictly to uniform JSON:API response envelopes, time-ordered UUIDv7 identifiers, ISO-8601 UTC timestamps, optimistic concurrency control via ETags, and automated audit logging.

## 2. Operational Architecture & Relational Mapping

The following table maps the domain's operational context to architectural containers, components, database tables, and default role entitlements:

| Dimension | Specification Detail |
| :--- | :--- |
| **Functional Domain** | `Analytics` (Code: `ANALYTICS`) |
| **Authoritative Endpoints** | 26 Active Endpoints (`API-ANALYTICS-001` to `API-ANALYTICS-026`) |
| **Primary Architecture Container** | `ARCH-CONT-015` |
| **Assigned Component** | `ARCH-COMP-043` |
| **Primary Database Tables** | `clinical_encounters, dispensations, clinic_stock` |
| **Lead Role Entitlement** | `ROLE-013 (Epidemiologist / BBMP Health Officer)` |
| **Default Rate Limiting** | `60 req/min per User` |
| **Offline Edge Support** | `Edge Local Queue with Delta Sync` |

## 3. Domain Operational State Machine

The operational state transitions governing entities within this domain are modeled below:

```mermaid
stateDiagram-v2
    [*] --> RawEventIngested: OPD Encounter Logged in Operational DB
    RawEventIngested --> KafkaPipeline: Streamed to Analytical Bus
    KafkaPipeline --> ClickHouseLoaded: Ingested into Columnar Star Schema
    ClickHouseLoaded --> MaterializedViews: Aggregated by Ward, Zone, Date
    MaterializedViews --> AnomalyDetected: Outbreak Spike > 3 Sigma
    AnomalyDetected --> AlertBroadcast: Disease Surveillance Alert Dispatched
    MaterializedViews --> DashboardQuery: Executive KPI Query Executed
    DashboardQuery --> [*]
```

## 4. End-to-End Operational Data Flow

The sequence diagram below illustrates the end-to-end operational flow between frontline clinic staff, edge workstations, the central API gateway, and backing data stores:

```mermaid
sequenceDiagram
    autonumber
    participant Officer as Chief Health Officer
    participant Dash as Municipal Analytics Dashboard
    participant API as Analytics Service
    participant CH as ClickHouse Columnar Cluster
    Officer->>Dash: Open Greater Bengaluru Fever Heatmap
    Dash->>API: GET /api/v1/analytics/surveillance/fever-clusters
    API->>CH: Query Materialized Aggregates by Ward & Date
    CH-->>API: Return Syndromic Case Counts & Baseline Variances
    API-->>Dash: HTTP 200 OK (Geospatial JSON GeoJSON)
    Dash-->>Officer: Render Live Outbreak Heatmap
```

## 5. Domain Endpoint Inventory Catalog

Complete inventory of all 26 endpoints defined for the `Analytics` domain:

| Endpoint ID | Method | URI Route Path | Functional Title | Role Context | Idempotency Standard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API-ANALYTICS-001** | `POST` | `/api/v1/analytics` | Create New Municipal Analytics Record | `ROLE-013` | Supported via X-Idempotency-Key |
| **API-ANALYTICS-002** | `GET` | `/api/v1/analytics/{analyticId}` | Retrieve Municipal Analytics Details by ID | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-003** | `GET` | `/api/v1/analytics` | List and Filter Municipal Analytics Records | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-004** | `PUT` | `/api/v1/analytics/{analyticId}` | Update Full Municipal Analytics Specification | `ROLE-013` | Supported via X-Idempotency-Key |
| **API-ANALYTICS-005** | `PATCH` | `/api/v1/analytics/{analyticId}/status` | Update Municipal Analytics Operational State | `ROLE-013` | Supported via X-Idempotency-Key |
| **API-ANALYTICS-006** | `GET` | `/api/v1/analytics/{analyticId}/search` | Search Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-007** | `GET` | `/api/v1/analytics/history` | History Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-008** | `GET` | `/api/v1/analytics/{analyticId}/audit` | Audit Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-009** | `POST` | `/api/v1/analytics/cancel` | Cancel Municipal Analytics Workflow Operation | `ROLE-013` | Supported via X-Idempotency-Key |
| **API-ANALYTICS-010** | `POST` | `/api/v1/analytics/verify` | Verify Municipal Analytics Workflow Operation | `ROLE-013` | Supported via X-Idempotency-Key |
| **API-ANALYTICS-011** | `GET` | `/api/v1/analytics/export` | Export Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-012** | `GET` | `/api/v1/analytics/{analyticId}/metrics` | Metrics Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-013** | `POST` | `/api/v1/analytics/reconcile` | Reconcile Municipal Analytics Workflow Operation | `ROLE-013` | Supported via X-Idempotency-Key |
| **API-ANALYTICS-014** | `POST` | `/api/v1/analytics/batch` | Batch Municipal Analytics Workflow Operation | `ROLE-013` | Supported via X-Idempotency-Key |
| **API-ANALYTICS-015** | `GET` | `/api/v1/analytics/sync` | Sync Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-016** | `GET` | `/api/v1/analytics/{analyticId}/alerts` | Alerts Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-017** | `POST` | `/api/v1/analytics/escalate` | Escalate Municipal Analytics Workflow Operation | `ROLE-013` | Supported via X-Idempotency-Key |
| **API-ANALYTICS-018** | `POST` | `/api/v1/analytics/approve` | Approve Municipal Analytics Workflow Operation | `ROLE-013` | Supported via X-Idempotency-Key |
| **API-ANALYTICS-019** | `POST` | `/api/v1/analytics/reversal` | Reversal Municipal Analytics Workflow Operation | `ROLE-013` | Supported via X-Idempotency-Key |
| **API-ANALYTICS-020** | `GET` | `/api/v1/analytics/{analyticId}/items` | Items Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-021** | `GET` | `/api/v1/analytics/documents` | Documents Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-022** | `GET` | `/api/v1/analytics/{analyticId}/timeline` | Timeline Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-023** | `GET` | `/api/v1/analytics/stats` | Stats Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-024** | `GET` | `/api/v1/analytics/{analyticId}/search` | Search Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-025** | `GET` | `/api/v1/analytics/history` | History Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |
| **API-ANALYTICS-026** | `GET` | `/api/v1/analytics/{analyticId}/audit` | Audit Municipal Analytics Workflow Operation | `ROLE-013` | Read-Only Idempotent |

## 6. Comprehensive Endpoint Technical Specifications

Exhaustive technical contracts for all 26 endpoints in the `Analytics` domain:

### 6.1 `API-ANALYTICS-001`: Create New Municipal Analytics Record

- **API Identifier:** `API-ANALYTICS-001`
- **HTTP Route:** `POST /api/v1/analytics`
- **Functional Purpose:** Authoritative specification for create new municipal analytics record within Analytics operations.
- **Product Capability:** `CAPABILITY-054` | **Feature Code:** `FEATURE-054`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:post`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-054, SRS-NFR-034` | **Workflow:** `WF-009`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-024`
- **Planned Verification Test Case:** `PLANNED-TEST-API-233`
- **Dependency DAG Edge:** `API-DEP-054`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics:
    post:
      summary: "Create New Municipal Analytics Record"
      tags:
        - "Analytics"
      operationId: "post_api_v1_analytics"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics" \
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
  "operation": "Create New Municipal Analytics Record",
  "domain": "Analytics",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-ANALYTICS-001"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-001",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-001.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-024` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-233` under simulated offline network conditions.

### 6.2 `API-ANALYTICS-002`: Retrieve Municipal Analytics Details by ID

- **API Identifier:** `API-ANALYTICS-002`
- **HTTP Route:** `GET /api/v1/analytics/{analyticId}`
- **Functional Purpose:** Authoritative specification for retrieve municipal analytics details by id within Analytics operations.
- **Product Capability:** `CAPABILITY-055` | **Feature Code:** `FEATURE-055`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-055, SRS-NFR-035` | **Workflow:** `WF-010`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-025`
- **Planned Verification Test Case:** `PLANNED-TEST-API-234`
- **Dependency DAG Edge:** `API-DEP-055`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/{analyticId}:
    get:
      summary: "Retrieve Municipal Analytics Details by ID"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_analyticId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/{analyticId}" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-002",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-002.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-025` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-234` under simulated offline network conditions.

### 6.3 `API-ANALYTICS-003`: List and Filter Municipal Analytics Records

- **API Identifier:** `API-ANALYTICS-003`
- **HTTP Route:** `GET /api/v1/analytics`
- **Functional Purpose:** Authoritative specification for list and filter municipal analytics records within Analytics operations.
- **Product Capability:** `CAPABILITY-056` | **Feature Code:** `FEATURE-056`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-056, SRS-NFR-036` | **Workflow:** `WF-011`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-026`
- **Planned Verification Test Case:** `PLANNED-TEST-API-235`
- **Dependency DAG Edge:** `API-DEP-056`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics:
    get:
      summary: "List and Filter Municipal Analytics Records"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-003",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-003.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-026` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-235` under simulated offline network conditions.

### 6.4 `API-ANALYTICS-004`: Update Full Municipal Analytics Specification

- **API Identifier:** `API-ANALYTICS-004`
- **HTTP Route:** `PUT /api/v1/analytics/{analyticId}`
- **Functional Purpose:** Authoritative specification for update full municipal analytics specification within Analytics operations.
- **Product Capability:** `CAPABILITY-057` | **Feature Code:** `FEATURE-057`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:put`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-057, SRS-NFR-037` | **Workflow:** `WF-012`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-027`
- **Planned Verification Test Case:** `PLANNED-TEST-API-236`
- **Dependency DAG Edge:** `API-DEP-057`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/{analyticId}:
    put:
      summary: "Update Full Municipal Analytics Specification"
      tags:
        - "Analytics"
      operationId: "put_api_v1_analytics_analyticId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/{analyticId}" \
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
  "operation": "Update Full Municipal Analytics Specification",
  "domain": "Analytics",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-ANALYTICS-004"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-004",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-004.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-027` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-236` under simulated offline network conditions.

### 6.5 `API-ANALYTICS-005`: Update Municipal Analytics Operational State

- **API Identifier:** `API-ANALYTICS-005`
- **HTTP Route:** `PATCH /api/v1/analytics/{analyticId}/status`
- **Functional Purpose:** Authoritative specification for update municipal analytics operational state within Analytics operations.
- **Product Capability:** `CAPABILITY-058` | **Feature Code:** `FEATURE-058`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:patch`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-058, SRS-NFR-038` | **Workflow:** `WF-013`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-028`
- **Planned Verification Test Case:** `PLANNED-TEST-API-237`
- **Dependency DAG Edge:** `API-DEP-058`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/{analyticId}/status:
    patch:
      summary: "Update Municipal Analytics Operational State"
      tags:
        - "Analytics"
      operationId: "patch_api_v1_analytics_analyticId_status"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/{analyticId}/status" \
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
  "operation": "Update Municipal Analytics Operational State",
  "domain": "Analytics",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-ANALYTICS-005"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-005",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-005.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-028` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-237` under simulated offline network conditions.

### 6.6 `API-ANALYTICS-006`: Search Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-006`
- **HTTP Route:** `GET /api/v1/analytics/{analyticId}/search`
- **Functional Purpose:** Authoritative specification for search municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-059` | **Feature Code:** `FEATURE-059`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-059, SRS-NFR-039` | **Workflow:** `WF-014`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-029`
- **Planned Verification Test Case:** `PLANNED-TEST-API-238`
- **Dependency DAG Edge:** `API-DEP-059`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/{analyticId}/search:
    get:
      summary: "Search Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_analyticId_search"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/{analyticId}/search" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-006",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-006.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-029` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-238` under simulated offline network conditions.

### 6.7 `API-ANALYTICS-007`: History Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-007`
- **HTTP Route:** `GET /api/v1/analytics/history`
- **Functional Purpose:** Authoritative specification for history municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-060` | **Feature Code:** `FEATURE-060`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-060, SRS-NFR-040` | **Workflow:** `WF-015`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-030`
- **Planned Verification Test Case:** `PLANNED-TEST-API-239`
- **Dependency DAG Edge:** `API-DEP-060`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/history:
    get:
      summary: "History Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_history"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/history" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-007",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-007.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-030` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-239` under simulated offline network conditions.

### 6.8 `API-ANALYTICS-008`: Audit Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-008`
- **HTTP Route:** `GET /api/v1/analytics/{analyticId}/audit`
- **Functional Purpose:** Authoritative specification for audit municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-061` | **Feature Code:** `FEATURE-061`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-001, SRS-NFR-001` | **Workflow:** `WF-016`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-001`
- **Planned Verification Test Case:** `PLANNED-TEST-API-240`
- **Dependency DAG Edge:** `API-DEP-001`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/{analyticId}/audit:
    get:
      summary: "Audit Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_analyticId_audit"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/{analyticId}/audit" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-008",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-008.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-001` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-240` under simulated offline network conditions.

### 6.9 `API-ANALYTICS-009`: Cancel Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-009`
- **HTTP Route:** `POST /api/v1/analytics/cancel`
- **Functional Purpose:** Authoritative specification for cancel municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-062` | **Feature Code:** `FEATURE-062`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:post`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-002, SRS-NFR-002` | **Workflow:** `WF-017`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-002`
- **Planned Verification Test Case:** `PLANNED-TEST-API-241`
- **Dependency DAG Edge:** `API-DEP-002`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/cancel:
    post:
      summary: "Cancel Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "post_api_v1_analytics_cancel"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/cancel" \
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
  "operation": "Cancel Municipal Analytics Workflow Operation",
  "domain": "Analytics",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-ANALYTICS-009"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-009",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-009.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-002` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-241` under simulated offline network conditions.

### 6.10 `API-ANALYTICS-010`: Verify Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-010`
- **HTTP Route:** `POST /api/v1/analytics/verify`
- **Functional Purpose:** Authoritative specification for verify municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-063` | **Feature Code:** `FEATURE-063`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:post`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-003, SRS-NFR-003` | **Workflow:** `WF-018`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-003`
- **Planned Verification Test Case:** `PLANNED-TEST-API-242`
- **Dependency DAG Edge:** `API-DEP-003`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/verify:
    post:
      summary: "Verify Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "post_api_v1_analytics_verify"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/verify" \
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
  "operation": "Verify Municipal Analytics Workflow Operation",
  "domain": "Analytics",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-ANALYTICS-010"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-010",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-010.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-003` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-242` under simulated offline network conditions.

### 6.11 `API-ANALYTICS-011`: Export Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-011`
- **HTTP Route:** `GET /api/v1/analytics/export`
- **Functional Purpose:** Authoritative specification for export municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-064` | **Feature Code:** `FEATURE-064`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-004, SRS-NFR-004` | **Workflow:** `WF-019`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-004`
- **Planned Verification Test Case:** `PLANNED-TEST-API-243`
- **Dependency DAG Edge:** `API-DEP-004`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/export:
    get:
      summary: "Export Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_export"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/export" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-011",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-011.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-004` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-243` under simulated offline network conditions.

### 6.12 `API-ANALYTICS-012`: Metrics Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-012`
- **HTTP Route:** `GET /api/v1/analytics/{analyticId}/metrics`
- **Functional Purpose:** Authoritative specification for metrics municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-065` | **Feature Code:** `FEATURE-065`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-005, SRS-NFR-005` | **Workflow:** `WF-020`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-005`
- **Planned Verification Test Case:** `PLANNED-TEST-API-244`
- **Dependency DAG Edge:** `API-DEP-005`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/{analyticId}/metrics:
    get:
      summary: "Metrics Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_analyticId_metrics"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/{analyticId}/metrics" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-012",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-012.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-005` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-244` under simulated offline network conditions.

### 6.13 `API-ANALYTICS-013`: Reconcile Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-013`
- **HTTP Route:** `POST /api/v1/analytics/reconcile`
- **Functional Purpose:** Authoritative specification for reconcile municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-066` | **Feature Code:** `FEATURE-066`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:post`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-006, SRS-NFR-006` | **Workflow:** `WF-021`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-006`
- **Planned Verification Test Case:** `PLANNED-TEST-API-245`
- **Dependency DAG Edge:** `API-DEP-006`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/reconcile:
    post:
      summary: "Reconcile Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "post_api_v1_analytics_reconcile"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/reconcile" \
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
  "operation": "Reconcile Municipal Analytics Workflow Operation",
  "domain": "Analytics",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-ANALYTICS-013"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-013",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-013.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-006` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-245` under simulated offline network conditions.

### 6.14 `API-ANALYTICS-014`: Batch Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-014`
- **HTTP Route:** `POST /api/v1/analytics/batch`
- **Functional Purpose:** Authoritative specification for batch municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-067` | **Feature Code:** `FEATURE-067`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:post`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-007, SRS-NFR-007` | **Workflow:** `WF-022`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-007`
- **Planned Verification Test Case:** `PLANNED-TEST-API-246`
- **Dependency DAG Edge:** `API-DEP-007`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/batch:
    post:
      summary: "Batch Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "post_api_v1_analytics_batch"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/batch" \
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
  "operation": "Batch Municipal Analytics Workflow Operation",
  "domain": "Analytics",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-ANALYTICS-014"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-014",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-014.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-007` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-246` under simulated offline network conditions.

### 6.15 `API-ANALYTICS-015`: Sync Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-015`
- **HTTP Route:** `GET /api/v1/analytics/sync`
- **Functional Purpose:** Authoritative specification for sync municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-068` | **Feature Code:** `FEATURE-068`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-008, SRS-NFR-008` | **Workflow:** `WF-023`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-008`
- **Planned Verification Test Case:** `PLANNED-TEST-API-247`
- **Dependency DAG Edge:** `API-DEP-008`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/sync:
    get:
      summary: "Sync Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_sync"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/sync" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-015",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-015.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-008` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-247` under simulated offline network conditions.

### 6.16 `API-ANALYTICS-016`: Alerts Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-016`
- **HTTP Route:** `GET /api/v1/analytics/{analyticId}/alerts`
- **Functional Purpose:** Authoritative specification for alerts municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-069` | **Feature Code:** `FEATURE-069`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-009, SRS-NFR-009` | **Workflow:** `WF-024`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-009`
- **Planned Verification Test Case:** `PLANNED-TEST-API-248`
- **Dependency DAG Edge:** `API-DEP-009`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/{analyticId}/alerts:
    get:
      summary: "Alerts Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_analyticId_alerts"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/{analyticId}/alerts" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-016",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-016.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-009` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-248` under simulated offline network conditions.

### 6.17 `API-ANALYTICS-017`: Escalate Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-017`
- **HTTP Route:** `POST /api/v1/analytics/escalate`
- **Functional Purpose:** Authoritative specification for escalate municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-070` | **Feature Code:** `FEATURE-070`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:post`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-010, SRS-NFR-010` | **Workflow:** `WF-025`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-010`
- **Planned Verification Test Case:** `PLANNED-TEST-API-249`
- **Dependency DAG Edge:** `API-DEP-010`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/escalate:
    post:
      summary: "Escalate Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "post_api_v1_analytics_escalate"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/escalate" \
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
  "operation": "Escalate Municipal Analytics Workflow Operation",
  "domain": "Analytics",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-ANALYTICS-017"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-017",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-017.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-010` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-249` under simulated offline network conditions.

### 6.18 `API-ANALYTICS-018`: Approve Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-018`
- **HTTP Route:** `POST /api/v1/analytics/approve`
- **Functional Purpose:** Authoritative specification for approve municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-071` | **Feature Code:** `FEATURE-071`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:post`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-011, SRS-NFR-011` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-011`
- **Planned Verification Test Case:** `PLANNED-TEST-API-250`
- **Dependency DAG Edge:** `API-DEP-011`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/approve:
    post:
      summary: "Approve Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "post_api_v1_analytics_approve"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/approve" \
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
  "operation": "Approve Municipal Analytics Workflow Operation",
  "domain": "Analytics",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-ANALYTICS-018"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-018",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-018.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-011` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-250` under simulated offline network conditions.

### 6.19 `API-ANALYTICS-019`: Reversal Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-019`
- **HTTP Route:** `POST /api/v1/analytics/reversal`
- **Functional Purpose:** Authoritative specification for reversal municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-072` | **Feature Code:** `FEATURE-072`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:post`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-012, SRS-NFR-012` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-012`
- **Planned Verification Test Case:** `PLANNED-TEST-API-251`
- **Dependency DAG Edge:** `API-DEP-012`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/reversal:
    post:
      summary: "Reversal Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "post_api_v1_analytics_reversal"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/reversal" \
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
  "operation": "Reversal Municipal Analytics Workflow Operation",
  "domain": "Analytics",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-ANALYTICS-019"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-019",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-019.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-012` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-251` under simulated offline network conditions.

### 6.20 `API-ANALYTICS-020`: Items Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-020`
- **HTTP Route:** `GET /api/v1/analytics/{analyticId}/items`
- **Functional Purpose:** Authoritative specification for items municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-073` | **Feature Code:** `FEATURE-073`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-013, SRS-NFR-013` | **Workflow:** `WF-003`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-013`
- **Planned Verification Test Case:** `PLANNED-TEST-API-252`
- **Dependency DAG Edge:** `API-DEP-013`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/{analyticId}/items:
    get:
      summary: "Items Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_analyticId_items"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/{analyticId}/items" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-020",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-020.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-013` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-252` under simulated offline network conditions.

### 6.21 `API-ANALYTICS-021`: Documents Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-021`
- **HTTP Route:** `GET /api/v1/analytics/documents`
- **Functional Purpose:** Authoritative specification for documents municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-074` | **Feature Code:** `FEATURE-074`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-014, SRS-NFR-014` | **Workflow:** `WF-004`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-014`
- **Planned Verification Test Case:** `PLANNED-TEST-API-253`
- **Dependency DAG Edge:** `API-DEP-014`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/documents:
    get:
      summary: "Documents Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_documents"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/documents" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-021",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-021.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-014` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-253` under simulated offline network conditions.

### 6.22 `API-ANALYTICS-022`: Timeline Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-022`
- **HTTP Route:** `GET /api/v1/analytics/{analyticId}/timeline`
- **Functional Purpose:** Authoritative specification for timeline municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-075` | **Feature Code:** `FEATURE-075`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-015, SRS-NFR-015` | **Workflow:** `WF-005`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-015`
- **Planned Verification Test Case:** `PLANNED-TEST-API-254`
- **Dependency DAG Edge:** `API-DEP-015`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/{analyticId}/timeline:
    get:
      summary: "Timeline Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_analyticId_timeline"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/{analyticId}/timeline" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-022",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-022.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-015` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-254` under simulated offline network conditions.

### 6.23 `API-ANALYTICS-023`: Stats Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-023`
- **HTTP Route:** `GET /api/v1/analytics/stats`
- **Functional Purpose:** Authoritative specification for stats municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-076` | **Feature Code:** `FEATURE-076`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-016, SRS-NFR-016` | **Workflow:** `WF-006`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-016`
- **Planned Verification Test Case:** `PLANNED-TEST-API-255`
- **Dependency DAG Edge:** `API-DEP-016`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/stats:
    get:
      summary: "Stats Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_stats"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/stats" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-023",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-023.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-016` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-255` under simulated offline network conditions.

### 6.24 `API-ANALYTICS-024`: Search Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-024`
- **HTTP Route:** `GET /api/v1/analytics/{analyticId}/search`
- **Functional Purpose:** Authoritative specification for search municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-077` | **Feature Code:** `FEATURE-077`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-017, SRS-NFR-017` | **Workflow:** `WF-007`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-017`
- **Planned Verification Test Case:** `PLANNED-TEST-API-256`
- **Dependency DAG Edge:** `API-DEP-017`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/{analyticId}/search:
    get:
      summary: "Search Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_analyticId_search"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/{analyticId}/search" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-024",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-024.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-017` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-256` under simulated offline network conditions.

### 6.25 `API-ANALYTICS-025`: History Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-025`
- **HTTP Route:** `GET /api/v1/analytics/history`
- **Functional Purpose:** Authoritative specification for history municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-078` | **Feature Code:** `FEATURE-078`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-018, SRS-NFR-018` | **Workflow:** `WF-008`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-018`
- **Planned Verification Test Case:** `PLANNED-TEST-API-257`
- **Dependency DAG Edge:** `API-DEP-018`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/history:
    get:
      summary: "History Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_history"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/history" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-025",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-025.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-018` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-257` under simulated offline network conditions.

### 6.26 `API-ANALYTICS-026`: Audit Municipal Analytics Workflow Operation

- **API Identifier:** `API-ANALYTICS-026`
- **HTTP Route:** `GET /api/v1/analytics/{analyticId}/audit`
- **Functional Purpose:** Authoritative specification for audit municipal analytics workflow operation within Analytics operations.
- **Product Capability:** `CAPABILITY-079` | **Feature Code:** `FEATURE-079`
- **Primary Actor:** Authorized Analytics Operator | **User Persona:** Analytics Care Team Persona
- **Required RBAC Role:** `ROLE-013`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `analytics:get`
- **ABAC Scoping Rule:** Restricted to authorized Analytics personnel in active clinic context.
- **Upstream Traceability:** `SRS-FR-019, SRS-NFR-019` | **Workflow:** `WF-009`
- **Container / Component:** `ARCH-CONT-015` / `ARCH-COMP-043`
- **Target Relational Tables:** `clinical_encounters, dispensations, clinic_stock`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue with Delta Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-019`
- **Planned Verification Test Case:** `PLANNED-TEST-API-258`
- **Dependency DAG Edge:** `API-DEP-019`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/analytics/{analyticId}/audit:
    get:
      summary: "Audit Municipal Analytics Workflow Operation"
      tags:
        - "Analytics"
      operationId: "get_api_v1_analytics_analyticId_audit"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/analytics/{analyticId}/audit" \
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
    "type": "analytics",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-ANALYTICS-026",
      "domain": "Analytics",
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
    "code": "ERR-ANALYTICS-001",
    "message": "Domain constraint validation failed during execution of API-ANALYTICS-026.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, dispensations, clinic_stock` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-019` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-258` under simulated offline network conditions.

## 7. Domain-Specific Error Code Catalog & Troubleshooting Runbooks

The following standardized error codes are specifically emitted by `Analytics` services:

| Error Code ID | HTTP Status | Machine Code | Message Summary | Retryable | Resolution Runbook |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-ANALYTICS-001** | `HTTP 400` | `ANL_DATE_RANGE_TOO_BROAD` | Real-time analytics query interval exceeds maximum 365-day range. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-ANALYTICS-001. |
| **ERR-ANALYTICS-002** | `HTTP 403` | `ANL_INDIVIDUAL_PII_PROHIBITED` | Analytical queries cannot return identifiable citizen health records. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-ANALYTICS-002. |
| **ERR-ANALYTICS-003** | `HTTP 400` | `ANL_INVALID_METRIC_NAME` | Requested KPI metric is not in authoritative measure catalog. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-ANALYTICS-003. |
| **ERR-ANALYTICS-004** | `HTTP 403` | `ANL_ZONE_RESTRICTION` | User is not authorized to view municipal analytics for the requested zone. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-ANALYTICS-004. |
| **ERR-ANALYTICS-005** | `HTTP 504` | `ANL_CLICKHOUSE_TIMEOUT` | Columnar analytical warehouse query execution exceeded 10-second deadline. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-ANALYTICS-005. |
| **ERR-ANALYTICS-006** | `HTTP 500` | `ANL_AGGREGATION_ENGINE_FAULT` | Materialized view refresh in analytical warehouse failed. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-ANALYTICS-006. |

## 8. Offline Edge Operation & Synchronization Mechanics

When WAN connectivity to the central cloud is disrupted, `Analytics` operations transition to autonomous edge mode:
1. **Local SQLite WAL Database:** Transactions are committed locally to `/data/namma_clinic_edge.db` on the clinic's Intel N100 mini-server.
2. **Offline Mutation Journal:** Every INSERT, UPDATE, and SOFT_DELETE appends a record to the `offline_mutation_log` table with a local vector clock.
3. **Conflict Resolution Policy:** Upon WAN restoration, the edge sync agent uploads buffered mutations in batches of 100 to `/api/v1/system/sync/batch`. Conflicts are resolved deterministically using Last-Write-Wins (LWW) with microsecond Lamport timestamps, except for clinical records where doctor entries take precedence over clerical updates.
4. **Storage Quotas:** Up to 72 hours of offline operations (approximately 15,000 mutations) can be buffered without storage degradation.

## 9. Security, Data Protection & DPDP Act Compliance

Data protection invariants for `Analytics` operations:

| Data Element | Classification | Encryption Standard | Masking Rule | DPDP Act Section | Retention Schedule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Core Entity Record | `INTERNAL` | AES-256-GCM Column Level | Masked on non-admin UI | Section 8 (Data Security) | 10 Years (Medical Records) |
| Transaction Mutation | INTERNAL | TLS 1.3 in Transit | Zero PII in Gateway Logs | Section 6 (Consent Notice) | 10 Years (Audit Ledger) |
| WORM Audit Log | HIGHLY-RESTRICTED | HMAC SHA-256 Chained | Full Hash Ledger | Section 12 (Citizen Rights) | Permanent (Statutory Archive) |

## 10. Domain Quality Acceptance Criteria (BDD)

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify Successful Execution of Create New Municipal Analytics Record
  Given an authenticated staff member with role 'ROLE-013'
  And an active clinical shift rostered in clinic facility '018e3a20-0008-7000-8000-000000000001'
  When the client sends a valid request to /api/v1/analytics
  Then the server processes the request within 1500ms
  And returns HTTP 201
  And the response conforms to envelope schema 'StandardApiResponseEnvelope'
  And an immutable audit log is appended to 'AUDIT-EVENT-024'
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Reject Unauthorized Call to Create New Municipal Analytics Record
  Given a caller presenting an invalid or expired Bearer token
  And requesting protected resource access
  When the caller transmits a request to /api/v1/analytics
  Then the API gateway intercepts the request
  And returns HTTP 401 Unauthorized
  And returns error code 'ERR-AUTH-002' or 'ERR-AUTH-003'
  And rejects access before invoking backend services
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Execute Create New Municipal Analytics Record in Autonomous Edge Mode
  Given the clinic workstation has lost WAN connectivity to cloud
  And the local edge mini-server is operational with local SQLite database
  When the staff member executes Create New Municipal Analytics Record
  Then the edge API gateway accepts the request locally
  And returns HTTP 201 within 250ms
  And appends the mutation to the local offline sync journal
  And synchronizes to cloud automatically upon network restoration
```

## 11. Requirements & Database Relational Traceability Matrix

Traceability mapping for all `Analytics` endpoints:

| Endpoint ID | Upstream SRS Requirements | Workflow ID | Feature Code | Target Database Tables | Verification Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `API-ANALYTICS-001` | `SRS-FR-054, SRS-NFR-034` | `WF-009` | `FEATURE-054` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-233` |
| `API-ANALYTICS-002` | `SRS-FR-055, SRS-NFR-035` | `WF-010` | `FEATURE-055` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-234` |
| `API-ANALYTICS-003` | `SRS-FR-056, SRS-NFR-036` | `WF-011` | `FEATURE-056` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-235` |
| `API-ANALYTICS-004` | `SRS-FR-057, SRS-NFR-037` | `WF-012` | `FEATURE-057` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-236` |
| `API-ANALYTICS-005` | `SRS-FR-058, SRS-NFR-038` | `WF-013` | `FEATURE-058` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-237` |
| `API-ANALYTICS-006` | `SRS-FR-059, SRS-NFR-039` | `WF-014` | `FEATURE-059` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-238` |
| `API-ANALYTICS-007` | `SRS-FR-060, SRS-NFR-040` | `WF-015` | `FEATURE-060` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-239` |
| `API-ANALYTICS-008` | `SRS-FR-001, SRS-NFR-001` | `WF-016` | `FEATURE-061` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-240` |
| `API-ANALYTICS-009` | `SRS-FR-002, SRS-NFR-002` | `WF-017` | `FEATURE-062` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-241` |
| `API-ANALYTICS-010` | `SRS-FR-003, SRS-NFR-003` | `WF-018` | `FEATURE-063` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-242` |
| `API-ANALYTICS-011` | `SRS-FR-004, SRS-NFR-004` | `WF-019` | `FEATURE-064` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-243` |
| `API-ANALYTICS-012` | `SRS-FR-005, SRS-NFR-005` | `WF-020` | `FEATURE-065` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-244` |
| `API-ANALYTICS-013` | `SRS-FR-006, SRS-NFR-006` | `WF-021` | `FEATURE-066` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-245` |
| `API-ANALYTICS-014` | `SRS-FR-007, SRS-NFR-007` | `WF-022` | `FEATURE-067` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-246` |
| `API-ANALYTICS-015` | `SRS-FR-008, SRS-NFR-008` | `WF-023` | `FEATURE-068` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-247` |
| `API-ANALYTICS-016` | `SRS-FR-009, SRS-NFR-009` | `WF-024` | `FEATURE-069` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-248` |
| `API-ANALYTICS-017` | `SRS-FR-010, SRS-NFR-010` | `WF-025` | `FEATURE-070` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-249` |
| `API-ANALYTICS-018` | `SRS-FR-011, SRS-NFR-011` | `WF-001` | `FEATURE-071` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-250` |
| `API-ANALYTICS-019` | `SRS-FR-012, SRS-NFR-012` | `WF-002` | `FEATURE-072` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-251` |
| `API-ANALYTICS-020` | `SRS-FR-013, SRS-NFR-013` | `WF-003` | `FEATURE-073` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-252` |
| `API-ANALYTICS-021` | `SRS-FR-014, SRS-NFR-014` | `WF-004` | `FEATURE-074` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-253` |
| `API-ANALYTICS-022` | `SRS-FR-015, SRS-NFR-015` | `WF-005` | `FEATURE-075` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-254` |
| `API-ANALYTICS-023` | `SRS-FR-016, SRS-NFR-016` | `WF-006` | `FEATURE-076` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-255` |
| `API-ANALYTICS-024` | `SRS-FR-017, SRS-NFR-017` | `WF-007` | `FEATURE-077` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-256` |
| `API-ANALYTICS-025` | `SRS-FR-018, SRS-NFR-018` | `WF-008` | `FEATURE-078` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-257` |
| `API-ANALYTICS-026` | `SRS-FR-019, SRS-NFR-019` | `WF-009` | `FEATURE-079` | `clinical_encounters, dispensations, clinic_stock` | `PLANNED-TEST-API-258` |
