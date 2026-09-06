# 🔌 API Specification: Authentication, Identity & Access Management (IAM) API Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-04 | **Status:** Authoritative Baseline | **Date:** September 2026
> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Standard Framework:** RFC 7231 (HTTP/1.1), JSON:API v1.1, DPDP Act 2023, ABDM Interoperability Standards
> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.

---

## 1. Executive Summary & Domain Scope

The **Authentication, Identity & Access Management (IAM) API Specification** defines the authoritative, implementation-ready contracts for the `Auth` subsystem across all 183 Namma Clinic primary healthcare centers in Greater Bengaluru. This domain operates under the supervisory jurisdiction of `ROLE-015 (Medical Superintendent / IT Admin)` and fulfills the core mission: **Govern staff authentication via Argon2id, device fingerprint registration, RS256 JWT issuance, session lifecycle management, and emergency clinical break-glass protocols across all municipal clinic facilities.**

All 16 endpoints specified in this document adhere strictly to uniform JSON:API response envelopes, time-ordered UUIDv7 identifiers, ISO-8601 UTC timestamps, optimistic concurrency control via ETags, and automated audit logging.

## 2. Operational Architecture & Relational Mapping

The following table maps the domain's operational context to architectural containers, components, database tables, and default role entitlements:

| Dimension | Specification Detail |
| :--- | :--- |
| **Functional Domain** | `Auth` (Code: `AUTH`) |
| **Authoritative Endpoints** | 16 Active Endpoints (`API-AUTH-001` to `API-AUTH-016`) |
| **Primary Architecture Container** | `ARCH-CONT-004` |
| **Assigned Component** | `ARCH-COMP-010` |
| **Primary Database Tables** | `auth_users, user_credentials, user_sessions` |
| **Lead Role Entitlement** | `ROLE-015 (Medical Superintendent / IT Admin)` |
| **Default Rate Limiting** | `10 req/min per IP (Burst 15)` |
| **Offline Edge Support** | `Edge Local Mirror Cached` |

## 3. Domain Operational State Machine

The operational state transitions governing entities within this domain are modeled below:

```mermaid
stateDiagram-v2
    [*] --> Anonymous: Client Disconnected
    Anonymous --> Authenticating: Submit Staff Credentials + Device Fingerprint
    Authenticating --> ActiveSession: Credentials Valid (Argon2id Match)
    Authenticating --> AccountLocked: 5 Failed Attempts (30m Cooldown)
    ActiveSession --> ActiveSession: Token Rotation via /refresh
    ActiveSession --> BreakGlassActive: Emergency Clinical Bypass Invoked
    BreakGlassActive --> ActiveSession: Emergency Consultation Closed
    ActiveSession --> Revoked: Session Terminated / Logout
    Revoked --> [*]
```

## 4. End-to-End Operational Data Flow

The sequence diagram below illustrates the end-to-end operational flow between frontline clinic staff, edge workstations, the central API gateway, and backing data stores:

```mermaid
sequenceDiagram
    autonumber
    participant Staff as Clinic Clinician / Nurse
    participant UI as Workstation Tablet
    participant GW as API Gateway
    participant Auth as IAM Microservice
    participant Redis as Session Redis Cache
    participant DB as Auth PostgreSQL DB
    Staff->>UI: Enter Municipal ID & Password
    UI->>GW: POST /api/v1/auth/login
    GW->>Auth: Validate Credentials & Hardware Fingerprint
    Auth->>DB: Query Staff Profile & Password Hash
    Auth->>Auth: Verify Argon2id Hash
    Auth->>Redis: Store Session ID & Refresh Token
    Auth-->>GW: Return Access Token + Refresh Token
    GW-->>UI: HTTP 200 OK (JWT)
    UI-->>Staff: Display Clinic Dashboard
```

## 5. Domain Endpoint Inventory Catalog

Complete inventory of all 16 endpoints defined for the `Auth` domain:

| Endpoint ID | Method | URI Route Path | Functional Title | Role Context | Idempotency Standard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API-AUTH-001** | `POST` | `/api/v1/auth/login` | Staff Credential Login & Session Issuance | `ROLE-015` | Supported via X-Idempotency-Key |
| **API-AUTH-002** | `POST` | `/api/v1/auth/refresh` | Token Rotation & Refresh Exchange | `ROLE-015` | Strict Single-Use Rotation |
| **API-AUTH-003** | `POST` | `/api/v1/auth/logout` | Session Termination & Token Revocation | `ROLE-015` | Idempotent Termination |
| **API-AUTH-004** | `GET` | `/api/v1/auth/me` | Current Staff Profile & Entitlements Lookup | `ROLE-015` | Read-Only Idempotent |
| **API-AUTH-005** | `POST` | `/api/v1/auth/password/change` | Self-Service Staff Password Update | `ROLE-015` | Not Required (Sequential) |
| **API-AUTH-006** | `GET` | `/api/v1/auth/.well-known/jwks.json` | JSON Web Key Set (JWKS) Public Verification Keys | `ROLE-006` | Read-Only Idempotent |
| **API-AUTH-007** | `POST` | `/api/v1/auth/mfa/verify` | Multi-Factor Authentication (TOTP) Verification | `ROLE-002` | Single-Use Code Verification |
| **API-AUTH-008** | `POST` | `/api/v1/auth/break-glass` | Clinical Break-Glass Emergency Access Activation | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-AUTH-009** | `POST` | `/api/v1/auth/devices/register` | Clinic Tablet Hardware Device Registration | `ROLE-024` | Supported via X-Idempotency-Key |
| **API-AUTH-010** | `GET` | `/api/v1/auth/devices` | Facility Registered Workstations List | `ROLE-024` | Read-Only Idempotent |
| **API-AUTH-011** | `DELETE` | `/api/v1/auth/devices/{deviceId}` | De-register & Revoke Workstation Trust | `ROLE-011` | Idempotent Deletion |
| **API-AUTH-012** | `GET` | `/api/v1/auth/roles` | Master RBAC Roles Catalog Listing | `ROLE-001` | Read-Only Idempotent |
| **API-AUTH-013** | `POST` | `/api/v1/auth/users/{userId}/roles` | Assign Roles and Facility Scope to Staff | `ROLE-015` | Supported via X-Idempotency-Key |
| **API-AUTH-014** | `GET` | `/api/v1/auth/sessions` | Active Staff Sessions Listing | `ROLE-011` | Read-Only Idempotent |
| **API-AUTH-015** | `DELETE` | `/api/v1/auth/sessions/{sessionId}` | Force Invalidate Specific Session | `ROLE-011` | Idempotent Deletion |
| **API-AUTH-016** | `POST` | `/api/v1/auth/shifts/clock-in` | Staff Duty Shift Clock-In | `ROLE-016` | Supported via X-Idempotency-Key |

## 6. Comprehensive Endpoint Technical Specifications

Exhaustive technical contracts for all 16 endpoints in the `Auth` domain:

### 6.1 `API-AUTH-001`: Staff Credential Login & Session Issuance

- **API Identifier:** `API-AUTH-001`
- **HTTP Route:** `POST /api/v1/auth/login`
- **Functional Purpose:** Authenticate clinic staff credentials via Argon2id, enforce device trust, issue RS256 JWT access token and refresh token.
- **Product Capability:** `CAPABILITY-001` | **Feature Code:** `FEATURE-001`
- **Primary Actor:** Clinic Staff | **User Persona:** All Personas
- **Required RBAC Role:** `ROLE-015`
- **Authentication Requirement:** `Anonymous / Public Ingress`
- **RBAC Permission Tokens:** `auth:session:create`
- **ABAC Scoping Rule:** Validates registered clinic device fingerprint and facility roster schedule.
- **Upstream Traceability:** `SRS-FR-001, SRS-NFR-008, BR-001` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `auth_users, user_credentials, user_sessions`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `10 req/min per IP (Burst 15)`
- **Offline Edge Resilience:** Edge Local Mirror Cached
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-001`
- **Planned Verification Test Case:** `PLANNED-TEST-API-001`
- **Dependency DAG Edge:** `API-DEP-001`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/login:
    post:
      summary: "Staff Credential Login & Session Issuance"
      tags:
        - "Auth"
      operationId: "post_api_v1_auth_login"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/LoginRequest"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AuthTokenResponse"
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
        '403':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '429':
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/login" \
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
  "operation": "Staff Credential Login & Session Issuance",
  "domain": "Auth",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUTH-001"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-001",
      "domain": "Auth",
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
    "code": "ERR-AUTH-001",
    "message": "Domain constraint validation failed during execution of API-AUTH-001.",
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
- **Relational Database Mutation:** Modifies tables `auth_users, user_credentials, user_sessions` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-001` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-001` under simulated offline network conditions.

### 6.2 `API-AUTH-002`: Token Rotation & Refresh Exchange

- **API Identifier:** `API-AUTH-002`
- **HTTP Route:** `POST /api/v1/auth/refresh`
- **Functional Purpose:** Exchange valid refresh token for renewed 15-minute JWT access token with single-use token rotation.
- **Product Capability:** `CAPABILITY-001` | **Feature Code:** `FEATURE-001`
- **Primary Actor:** Authenticated Client | **User Persona:** All Personas
- **Required RBAC Role:** `ROLE-015`
- **Authentication Requirement:** `Refresh Token Header`
- **RBAC Permission Tokens:** `auth:token:refresh`
- **ABAC Scoping Rule:** Requires active non-revoked session ID in Redis cache and database.
- **Upstream Traceability:** `SRS-FR-001, SRS-NFR-008` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `user_sessions`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Strict Single-Use Rotation
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `30 req/min per Session`
- **Offline Edge Resilience:** Edge Local Gateway Proxy
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-002`
- **Planned Verification Test Case:** `PLANNED-TEST-API-002`
- **Dependency DAG Edge:** `API-DEP-002`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/refresh:
    post:
      summary: "Token Rotation & Refresh Exchange"
      tags:
        - "Auth"
      operationId: "post_api_v1_auth_refresh"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/TokenRefreshRequest"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AuthTokenResponse"
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
curl -X POST \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/refresh" \
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
  "operation": "Token Rotation & Refresh Exchange",
  "domain": "Auth",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUTH-002"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-002",
      "domain": "Auth",
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
    "code": "ERR-AUTH-002",
    "message": "Domain constraint validation failed during execution of API-AUTH-002.",
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
- **Relational Database Mutation:** Modifies tables `user_sessions` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-002` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-002` under simulated offline network conditions.

### 6.3 `API-AUTH-003`: Session Termination & Token Revocation

- **API Identifier:** `API-AUTH-003`
- **HTTP Route:** `POST /api/v1/auth/logout`
- **Functional Purpose:** Terminate active session, revoke refresh token, and publish token revocation notice to Redis cluster.
- **Product Capability:** `CAPABILITY-001` | **Feature Code:** `FEATURE-001`
- **Primary Actor:** Authenticated Staff | **User Persona:** All Personas
- **Required RBAC Role:** `ROLE-015`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `auth:session:terminate`
- **ABAC Scoping Rule:** User may only terminate their own active session unless admin role.
- **Upstream Traceability:** `SRS-FR-001, SECR-002` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `user_sessions`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Idempotent Termination
- **Execution Timeout:** `1000ms`
- **Rate Limiting Policy:** `20 req/min per User`
- **Offline Edge Resilience:** Immediate Local Invalidation
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-003`
- **Planned Verification Test Case:** `PLANNED-TEST-API-003`
- **Dependency DAG Edge:** `API-DEP-003`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/logout:
    post:
      summary: "Session Termination & Token Revocation"
      tags:
        - "Auth"
      operationId: "post_api_v1_auth_logout"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/logout" \
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
  "operation": "Session Termination & Token Revocation",
  "domain": "Auth",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUTH-003"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-003",
      "domain": "Auth",
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
    "code": "ERR-AUTH-003",
    "message": "Domain constraint validation failed during execution of API-AUTH-003.",
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
- **Relational Database Mutation:** Modifies tables `user_sessions` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-003` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-003` under simulated offline network conditions.

### 6.4 `API-AUTH-004`: Current Staff Profile & Entitlements Lookup

- **API Identifier:** `API-AUTH-004`
- **HTTP Route:** `GET /api/v1/auth/me`
- **Functional Purpose:** Retrieve current authenticated staff profile, assigned roles, permissions matrix, and clinic facility scope.
- **Product Capability:** `CAPABILITY-001` | **Feature Code:** `FEATURE-002`
- **Primary Actor:** Authenticated Staff | **User Persona:** All Personas
- **Required RBAC Role:** `ROLE-015`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `auth:profile:read`
- **ABAC Scoping Rule:** Returns user context strictly scoped to active facility and shift.
- **Upstream Traceability:** `SRS-FR-001, SRS-FR-005` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `auth_users, roles, permissions, facilities`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Cached in Edge IndexedDB
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-004`
- **Planned Verification Test Case:** `PLANNED-TEST-API-004`
- **Dependency DAG Edge:** `API-DEP-004`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/me:
    get:
      summary: "Current Staff Profile & Entitlements Lookup"
      tags:
        - "Auth"
      operationId: "get_api_v1_auth_me"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StaffSessionProfile"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/me" \
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
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-004",
      "domain": "Auth",
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
    "code": "ERR-AUTH-003",
    "message": "Domain constraint validation failed during execution of API-AUTH-004.",
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
- **Relational Database Mutation:** Modifies tables `auth_users, roles, permissions, facilities` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-004` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-004` under simulated offline network conditions.

### 6.5 `API-AUTH-005`: Self-Service Staff Password Update

- **API Identifier:** `API-AUTH-005`
- **HTTP Route:** `POST /api/v1/auth/password/change`
- **Functional Purpose:** Update staff password, verifying existing credentials and validating against 12+ character complexity rules.
- **Product Capability:** `CAPABILITY-002` | **Feature Code:** `FEATURE-002`
- **Primary Actor:** Authenticated Staff | **User Persona:** All Personas
- **Required RBAC Role:** `ROLE-015`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `auth:password:update`
- **ABAC Scoping Rule:** Requires current password verification; updates Argon2id salt and hash.
- **Upstream Traceability:** `SECR-001, SRS-NFR-008` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `user_credentials, user_sessions`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Not Required (Sequential)
- **Execution Timeout:** `2000ms`
- **Rate Limiting Policy:** `5 req/hour per User`
- **Offline Edge Resilience:** Prohibited Offline
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-005`
- **Planned Verification Test Case:** `PLANNED-TEST-API-005`
- **Dependency DAG Edge:** `API-DEP-005`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/password/change:
    post:
      summary: "Self-Service Staff Password Update"
      tags:
        - "Auth"
      operationId: "post_api_v1_auth_password_change"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PasswordChangeRequest"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/password/change" \
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
  "operation": "Self-Service Staff Password Update",
  "domain": "Auth",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUTH-005"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-005",
      "domain": "Auth",
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
    "code": "ERR-AUTH-001",
    "message": "Domain constraint validation failed during execution of API-AUTH-005.",
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
- **Relational Database Mutation:** Modifies tables `user_credentials, user_sessions` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-005` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-005` under simulated offline network conditions.

### 6.6 `API-AUTH-006`: JSON Web Key Set (JWKS) Public Verification Keys

- **API Identifier:** `API-AUTH-006`
- **HTTP Route:** `GET /api/v1/auth/.well-known/jwks.json`
- **Functional Purpose:** Expose public RSA verification keys for distributed JWT signature verification across edge gateways and microservices.
- **Product Capability:** `CAPABILITY-001` | **Feature Code:** `FEATURE-001`
- **Primary Actor:** Microservice / Edge Node | **User Persona:** System
- **Required RBAC Role:** `ROLE-006`
- **Authentication Requirement:** `Anonymous / Public Ingress`
- **RBAC Permission Tokens:** `Public / Anonymous`
- **ABAC Scoping Rule:** Public read with 24-hour Cache-Control header.
- **Upstream Traceability:** `SECR-003, ARCH-CONT-004` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `system_configs`
- **Data Security Tier:** `PUBLIC`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `200ms`
- **Rate Limiting Policy:** `1000 req/min (CDN Cached)`
- **Offline Edge Resilience:** Locally Cached Public Keys
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-006`
- **Planned Verification Test Case:** `PLANNED-TEST-API-006`
- **Dependency DAG Edge:** `API-DEP-006`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/.well-known/jwks.json:
    get:
      summary: "JSON Web Key Set (JWKS) Public Verification Keys"
      tags:
        - "Auth"
      operationId: "get_api_v1_auth_.well-known_jwks.json"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/.well-known/jwks.json" \
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
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-006",
      "domain": "Auth",
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
    "code": "ERR-SYS-007",
    "message": "Domain constraint validation failed during execution of API-AUTH-006.",
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
- **Relational Database Mutation:** Modifies tables `system_configs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-006` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-006` under simulated offline network conditions.

### 6.7 `API-AUTH-007`: Multi-Factor Authentication (TOTP) Verification

- **API Identifier:** `API-AUTH-007`
- **HTTP Route:** `POST /api/v1/auth/mfa/verify`
- **Functional Purpose:** Verify 6-digit TOTP code during privileged login or step-up authentication.
- **Product Capability:** `CAPABILITY-001` | **Feature Code:** `FEATURE-001`
- **Primary Actor:** Privileged Staff | **User Persona:** Admin / Clinical Lead
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Interim Pre-Auth Token`
- **RBAC Permission Tokens:** `auth:mfa:verify`
- **ABAC Scoping Rule:** TOTP token must match within +/- 1 time step window (30s drift).
- **Upstream Traceability:** `SECR-002, SRS-FR-001` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `user_credentials, user_sessions`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Single-Use Code Verification
- **Execution Timeout:** `1000ms`
- **Rate Limiting Policy:** `5 req/min per Session`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-007`
- **Planned Verification Test Case:** `PLANNED-TEST-API-007`
- **Dependency DAG Edge:** `API-DEP-007`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/mfa/verify:
    post:
      summary: "Multi-Factor Authentication (TOTP) Verification"
      tags:
        - "Auth"
      operationId: "post_api_v1_auth_mfa_verify"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/LoginRequest"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AuthTokenResponse"
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
curl -X POST \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/mfa/verify" \
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
  "operation": "Multi-Factor Authentication (TOTP) Verification",
  "domain": "Auth",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUTH-007"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-007",
      "domain": "Auth",
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
    "code": "ERR-AUTH-009",
    "message": "Domain constraint validation failed during execution of API-AUTH-007.",
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
- **Relational Database Mutation:** Modifies tables `user_credentials, user_sessions` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-007` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-007` under simulated offline network conditions.

### 6.8 `API-AUTH-008`: Clinical Break-Glass Emergency Access Activation

- **API Identifier:** `API-AUTH-008`
- **HTTP Route:** `POST /api/v1/auth/break-glass`
- **Functional Purpose:** Activate audited break-glass emergency bypass to access restricted patient records during life-threatening encounters.
- **Product Capability:** `CAPABILITY-003` | **Feature Code:** `FEATURE-003`
- **Primary Actor:** Medical Officer | **User Persona:** Clinic Doctor
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `clinical:break_glass:invoke`
- **ABAC Scoping Rule:** Mandates treating doctor identity, patient UHID, and emergency clinical justification.
- **Upstream Traceability:** `SECR-004, PRIV-002, WF-025` | **Workflow:** `WF-025`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `user_sessions, audit_events, danger_alerts`
- **Data Security Tier:** `HIGHLY-RESTRICTED`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `3 req/hour per Doctor`
- **Offline Edge Resilience:** Edge Local WORM Logged
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-008`
- **Planned Verification Test Case:** `PLANNED-TEST-API-008`
- **Dependency DAG Edge:** `API-DEP-008`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/break-glass:
    post:
      summary: "Clinical Break-Glass Emergency Access Activation"
      tags:
        - "Auth"
      operationId: "post_api_v1_auth_break-glass"
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
                $ref: "#/components/schemas/AuthTokenResponse"
        '400':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '403':
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/break-glass" \
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
  "operation": "Clinical Break-Glass Emergency Access Activation",
  "domain": "Auth",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUTH-008"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-008",
      "domain": "Auth",
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
    "code": "ERR-AUTH-011",
    "message": "Domain constraint validation failed during execution of API-AUTH-008.",
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
- **Relational Database Mutation:** Modifies tables `user_sessions, audit_events, danger_alerts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-008` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-008` under simulated offline network conditions.

### 6.9 `API-AUTH-009`: Clinic Tablet Hardware Device Registration

- **API Identifier:** `API-AUTH-009`
- **HTTP Route:** `POST /api/v1/auth/devices/register`
- **Functional Purpose:** Register clinic workstation tablet hardware fingerprint and issue mTLS client certificate.
- **Product Capability:** `CAPABILITY-004` | **Feature Code:** `FEATURE-004`
- **Primary Actor:** Facility IT Admin | **User Persona:** Facility Administrator
- **Required RBAC Role:** `ROLE-024`
- **Authentication Requirement:** `Bearer JWT (Admin)`
- **RBAC Permission Tokens:** `system:device:register`
- **ABAC Scoping Rule:** Target facility ID must match admin jurisdiction; MAC address validated.
- **Upstream Traceability:** `SECR-005, ARCH-CONT-002` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `facilities, system_configs`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `2500ms`
- **Rate Limiting Policy:** `10 req/day per Facility`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-009`
- **Planned Verification Test Case:** `PLANNED-TEST-API-009`
- **Dependency DAG Edge:** `API-DEP-009`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/devices/register:
    post:
      summary: "Clinic Tablet Hardware Device Registration"
      tags:
        - "Auth"
      operationId: "post_api_v1_auth_devices_register"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/HardwareTerminalRegisterRequest"
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
        '403':
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/devices/register" \
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
  "operation": "Clinic Tablet Hardware Device Registration",
  "domain": "Auth",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUTH-009"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-009",
      "domain": "Auth",
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
    "code": "ERR-AUTH-010",
    "message": "Domain constraint validation failed during execution of API-AUTH-009.",
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
- **Relational Database Mutation:** Modifies tables `facilities, system_configs` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-009` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-009` under simulated offline network conditions.

### 6.10 `API-AUTH-010`: Facility Registered Workstations List

- **API Identifier:** `API-AUTH-010`
- **HTTP Route:** `GET /api/v1/auth/devices`
- **Functional Purpose:** List all registered tablets, mini-servers, and terminals associated with a clinic facility.
- **Product Capability:** `CAPABILITY-004` | **Feature Code:** `FEATURE-004`
- **Primary Actor:** Facility Admin | **User Persona:** Facility Administrator
- **Required RBAC Role:** `ROLE-024`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `system:device:read`
- **ABAC Scoping Rule:** Scoped strictly to authenticated user's clinic facility.
- **Upstream Traceability:** `SECR-005` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `facilities`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `1000ms`
- **Rate Limiting Policy:** `30 req/min per Facility`
- **Offline Edge Resilience:** Cached in Local Edge Node
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-010`
- **Planned Verification Test Case:** `PLANNED-TEST-API-010`
- **Dependency DAG Edge:** `API-DEP-010`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/devices:
    get:
      summary: "Facility Registered Workstations List"
      tags:
        - "Auth"
      operationId: "get_api_v1_auth_devices"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardCollectionEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '403':
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/devices" \
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
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-010",
      "domain": "Auth",
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
    "code": "ERR-AUTH-006",
    "message": "Domain constraint validation failed during execution of API-AUTH-010.",
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
- **Relational Database Mutation:** Modifies tables `facilities` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-010` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-010` under simulated offline network conditions.

### 6.11 `API-AUTH-011`: De-register & Revoke Workstation Trust

- **API Identifier:** `API-AUTH-011`
- **HTTP Route:** `DELETE /api/v1/auth/devices/{deviceId}`
- **Functional Purpose:** Revoke trust certificate and decommission lost, damaged, or retired clinic workstation tablet.
- **Product Capability:** `CAPABILITY-004` | **Feature Code:** `FEATURE-004`
- **Primary Actor:** Security Officer | **User Persona:** Security Administrator
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `system:device:revoke`
- **ABAC Scoping Rule:** Requires dual-authorization approval token.
- **Upstream Traceability:** `SECR-005` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `facilities, user_sessions`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Idempotent Deletion
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `10 req/hour per Admin`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-011`
- **Planned Verification Test Case:** `PLANNED-TEST-API-011`
- **Dependency DAG Edge:** `API-DEP-011`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/devices/{deviceId}:
    delete:
      summary: "De-register & Revoke Workstation Trust"
      tags:
        - "Auth"
      operationId: "delete_api_v1_auth_devices_deviceId"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '403':
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
curl -X DELETE \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/devices/{deviceId}" \
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
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-011",
      "domain": "Auth",
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
    "code": "ERR-AUTH-006",
    "message": "Domain constraint validation failed during execution of API-AUTH-011.",
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
- **Relational Database Mutation:** Modifies tables `facilities, user_sessions` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-011` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-011` under simulated offline network conditions.

### 6.12 `API-AUTH-012`: Master RBAC Roles Catalog Listing

- **API Identifier:** `API-AUTH-012`
- **HTTP Route:** `GET /api/v1/auth/roles`
- **Functional Purpose:** Retrieve authoritative list of system roles and functional capability mappings.
- **Product Capability:** `CAPABILITY-005` | **Feature Code:** `FEATURE-005`
- **Primary Actor:** Administrative Staff | **User Persona:** Facility Administrator
- **Required RBAC Role:** `ROLE-001`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `auth:roles:read`
- **ABAC Scoping Rule:** Returns active roles catalog.
- **Upstream Traceability:** `SRS-FR-005` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `roles, permissions`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Master Seed Cached
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-012`
- **Planned Verification Test Case:** `PLANNED-TEST-API-012`
- **Dependency DAG Edge:** `API-DEP-012`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/roles:
    get:
      summary: "Master RBAC Roles Catalog Listing"
      tags:
        - "Auth"
      operationId: "get_api_v1_auth_roles"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardCollectionEnvelope"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/roles" \
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
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-012",
      "domain": "Auth",
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
    "code": "ERR-AUTH-003",
    "message": "Domain constraint validation failed during execution of API-AUTH-012.",
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
- **Relational Database Mutation:** Modifies tables `roles, permissions` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-012` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-012` under simulated offline network conditions.

### 6.13 `API-AUTH-013`: Assign Roles and Facility Scope to Staff

- **API Identifier:** `API-AUTH-013`
- **HTTP Route:** `POST /api/v1/auth/users/{userId}/roles`
- **Functional Purpose:** Assign or update functional RBAC roles and clinic facility permissions for a staff member.
- **Product Capability:** `CAPABILITY-005` | **Feature Code:** `FEATURE-005`
- **Primary Actor:** Medical Superintendent | **User Persona:** Zonal Officer
- **Required RBAC Role:** `ROLE-015`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `auth:roles:assign`
- **ABAC Scoping Rule:** Target staff member must be within caller's administrative BBMP zone.
- **Upstream Traceability:** `SRS-FR-005, SECR-002` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `user_roles, staff_profiles`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `20 req/hour per Supervisor`
- **Offline Edge Resilience:** Prohibited Offline
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-013`
- **Planned Verification Test Case:** `PLANNED-TEST-API-013`
- **Dependency DAG Edge:** `API-DEP-013`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/users/{userId}/roles:
    post:
      summary: "Assign Roles and Facility Scope to Staff"
      tags:
        - "Auth"
      operationId: "post_api_v1_auth_users_userId_roles"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UserRoleAssignmentPayload"
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
        '403':
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
curl -X POST \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/users/{userId}/roles" \
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
  "operation": "Assign Roles and Facility Scope to Staff",
  "domain": "Auth",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUTH-013"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-013",
      "domain": "Auth",
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
    "code": "ERR-AUTH-006",
    "message": "Domain constraint validation failed during execution of API-AUTH-013.",
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
- **Relational Database Mutation:** Modifies tables `user_roles, staff_profiles` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-013` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-013` under simulated offline network conditions.

### 6.14 `API-AUTH-014`: Active Staff Sessions Listing

- **API Identifier:** `API-AUTH-014`
- **HTTP Route:** `GET /api/v1/auth/sessions`
- **Functional Purpose:** List active login sessions across facility devices for audit and concurrent session monitoring.
- **Product Capability:** `CAPABILITY-001` | **Feature Code:** `FEATURE-001`
- **Primary Actor:** Security Officer | **User Persona:** Security Administrator
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `auth:session:audit`
- **ABAC Scoping Rule:** Filtered by facility ID or staff user ID.
- **Upstream Traceability:** `SECR-002, SRS-NFR-008` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `user_sessions, auth_users`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `1000ms`
- **Rate Limiting Policy:** `30 req/min per Admin`
- **Offline Edge Resilience:** Edge Local Mirror
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-014`
- **Planned Verification Test Case:** `PLANNED-TEST-API-014`
- **Dependency DAG Edge:** `API-DEP-014`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/sessions:
    get:
      summary: "Active Staff Sessions Listing"
      tags:
        - "Auth"
      operationId: "get_api_v1_auth_sessions"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardCollectionEnvelope"
        '401':
          description: "Client or server error"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardErrorEnvelope"
        '403':
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/sessions" \
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
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-014",
      "domain": "Auth",
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
    "code": "ERR-AUTH-006",
    "message": "Domain constraint validation failed during execution of API-AUTH-014.",
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
- **Relational Database Mutation:** Modifies tables `user_sessions, auth_users` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-014` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-014` under simulated offline network conditions.

### 6.15 `API-AUTH-015`: Force Invalidate Specific Session

- **API Identifier:** `API-AUTH-015`
- **HTTP Route:** `DELETE /api/v1/auth/sessions/{sessionId}`
- **Functional Purpose:** Remotely terminate an active session, evicting tokens from Redis cache and database.
- **Product Capability:** `CAPABILITY-001` | **Feature Code:** `FEATURE-001`
- **Primary Actor:** Security Officer | **User Persona:** Security Administrator
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `auth:session:revoke`
- **ABAC Scoping Rule:** Immediate eviction across all distributed edge nodes.
- **Upstream Traceability:** `SECR-002` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `user_sessions`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Idempotent Deletion
- **Execution Timeout:** `1000ms`
- **Rate Limiting Policy:** `30 req/min per Admin`
- **Offline Edge Resilience:** Broadcast via Redis Pub/Sub
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-015`
- **Planned Verification Test Case:** `PLANNED-TEST-API-015`
- **Dependency DAG Edge:** `API-DEP-015`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/sessions/{sessionId}:
    delete:
      summary: "Force Invalidate Specific Session"
      tags:
        - "Auth"
      operationId: "delete_api_v1_auth_sessions_sessionId"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
        '403':
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
curl -X DELETE \
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/sessions/{sessionId}" \
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
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-015",
      "domain": "Auth",
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
    "code": "ERR-AUTH-006",
    "message": "Domain constraint validation failed during execution of API-AUTH-015.",
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
- **Relational Database Mutation:** Modifies tables `user_sessions` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-015` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-015` under simulated offline network conditions.

### 6.16 `API-AUTH-016`: Staff Duty Shift Clock-In

- **API Identifier:** `API-AUTH-016`
- **HTTP Route:** `POST /api/v1/auth/shifts/clock-in`
- **Functional Purpose:** Record staff shift commencement, room allocation, and active roster confirmation.
- **Product Capability:** `CAPABILITY-006` | **Feature Code:** `FEATURE-006`
- **Primary Actor:** Clinic Staff | **User Persona:** Frontline Health Worker
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `clinical:shift:manage`
- **ABAC Scoping Rule:** Staff member must be rostered for shift; facility matches active workstation.
- **Upstream Traceability:** `SRS-FR-005, WF-001` | **Workflow:** `WF-001`
- **Container / Component:** `ARCH-CONT-004` / `ARCH-COMP-010`
- **Target Relational Tables:** `staff_shifts, facility_rooms`
- **Data Security Tier:** `INTERNAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1200ms`
- **Rate Limiting Policy:** `5 req/day per Staff`
- **Offline Edge Resilience:** Edge Local Queue
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-016`
- **Planned Verification Test Case:** `PLANNED-TEST-API-016`
- **Dependency DAG Edge:** `API-DEP-016`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/auth/shifts/clock-in:
    post:
      summary: "Staff Duty Shift Clock-In"
      tags:
        - "Auth"
      operationId: "post_api_v1_auth_shifts_clock-in"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/auth/shifts/clock-in" \
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
  "operation": "Staff Duty Shift Clock-In",
  "domain": "Auth",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-AUTH-016"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "auth",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-AUTH-016",
      "domain": "Auth",
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
    "code": "ERR-AUTH-013",
    "message": "Domain constraint validation failed during execution of API-AUTH-016.",
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
- **Relational Database Mutation:** Modifies tables `staff_shifts, facility_rooms` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-016` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-016` under simulated offline network conditions.

## 7. Domain-Specific Error Code Catalog & Troubleshooting Runbooks

The following standardized error codes are specifically emitted by `Auth` services:

| Error Code ID | HTTP Status | Machine Code | Message Summary | Retryable | Resolution Runbook |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-AUTH-001** | `HTTP 401` | `AUTH_CREDENTIALS_INVALID` | Invalid municipal employee ID or password. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-001. |
| **ERR-AUTH-002** | `HTTP 401` | `AUTH_TOKEN_EXPIRED` | Access token has expired. Request renewal using refresh token. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-002. |
| **ERR-AUTH-003** | `HTTP 401` | `AUTH_TOKEN_INVALID` | Cryptographic signature verification failed on access token. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-003. |
| **ERR-AUTH-004** | `HTTP 401` | `AUTH_REFRESH_TOKEN_EXPIRED` | Refresh token session has expired. Full re-authentication required. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-004. |
| **ERR-AUTH-005** | `HTTP 401` | `AUTH_SESSION_REVOKED` | Session has been invalidated due to concurrent login or administrative revocation. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-005. |
| **ERR-AUTH-006** | `HTTP 403` | `AUTH_PERMISSION_DENIED` | Authenticated user lacks the required RBAC permission for this resource. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-006. |
| **ERR-AUTH-007** | `HTTP 403` | `AUTH_FACILITY_SCOPE_MISMATCH` | User is not authorized to execute operations in the requested clinic facility. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-007. |
| **ERR-AUTH-008** | `HTTP 403` | `AUTH_ACCOUNT_LOCKED` | Account temporarily locked due to excessive failed login attempts (5 strikes). | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-008. |
| **ERR-AUTH-009** | `HTTP 401` | `AUTH_MFA_REQUIRED` | Multi-factor authentication TOTP code required to complete privileged login. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-009. |
| **ERR-AUTH-010** | `HTTP 401` | `AUTH_DEVICE_UNTRUSTED` | Hardware tablet device fingerprint is not registered or certificate expired. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-010. |
| **ERR-AUTH-011** | `HTTP 403` | `AUTH_BREAK_GLASS_UNAUTHORIZED` | Break-glass privileged emergency access denied; clinical director role required. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-011. |
| **ERR-AUTH-012** | `HTTP 400` | `AUTH_PASSWORD_POLICY_VIOLATED` | Password does not meet 12+ char complexity, uppercase, symbol, or dictionary rules. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-012. |
| **ERR-AUTH-013** | `HTTP 409` | `AUTH_CONCURRENT_SHIFT_ACTIVE` | User is already logged in with an active shift at another facility. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-013. |
| **ERR-AUTH-014** | `HTTP 403` | `AUTH_IP_REPUTATION_BLOCKED` | Request originating from an unauthorized non-BBMP municipal network block. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-014. |
| **ERR-AUTH-015** | `HTTP 500` | `AUTH_KMS_SIGNING_FAILURE` | Hardware Security Module / Vault KMS failed to generate cryptographic token signature. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-AUTH-015. |

## 8. Offline Edge Operation & Synchronization Mechanics

When WAN connectivity to the central cloud is disrupted, `Auth` operations transition to autonomous edge mode:
1. **Local SQLite WAL Database:** Transactions are committed locally to `/data/namma_clinic_edge.db` on the clinic's Intel N100 mini-server.
2. **Offline Mutation Journal:** Every INSERT, UPDATE, and SOFT_DELETE appends a record to the `offline_mutation_log` table with a local vector clock.
3. **Conflict Resolution Policy:** Upon WAN restoration, the edge sync agent uploads buffered mutations in batches of 100 to `/api/v1/system/sync/batch`. Conflicts are resolved deterministically using Last-Write-Wins (LWW) with microsecond Lamport timestamps, except for clinical records where doctor entries take precedence over clerical updates.
4. **Storage Quotas:** Up to 72 hours of offline operations (approximately 15,000 mutations) can be buffered without storage degradation.

## 9. Security, Data Protection & DPDP Act Compliance

Data protection invariants for `Auth` operations:

| Data Element | Classification | Encryption Standard | Masking Rule | DPDP Act Section | Retention Schedule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Core Entity Record | `RESTRICTED` | AES-256-GCM Column Level | Masked on non-admin UI | Section 8 (Data Security) | 10 Years (Medical Records) |
| Transaction Mutation | INTERNAL | TLS 1.3 in Transit | Zero PII in Gateway Logs | Section 6 (Consent Notice) | 10 Years (Audit Ledger) |
| WORM Audit Log | HIGHLY-RESTRICTED | HMAC SHA-256 Chained | Full Hash Ledger | Section 12 (Citizen Rights) | Permanent (Statutory Archive) |

## 10. Domain Quality Acceptance Criteria (BDD)

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify Successful Execution of Staff Credential Login & Session Issuance
  Given an authenticated staff member with role 'ROLE-015'
  And an active clinical shift rostered in clinic facility '018e3a20-0008-7000-8000-000000000001'
  When the client sends a valid request to /api/v1/auth/login
  Then the server processes the request within 1500ms
  And returns HTTP 200
  And the response conforms to envelope schema 'AuthTokenResponse'
  And an immutable audit log is appended to 'AUDIT-EVENT-001'
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Reject Unauthorized Call to Staff Credential Login & Session Issuance
  Given a caller presenting an invalid or expired Bearer token
  And requesting protected resource access
  When the caller transmits a request to /api/v1/auth/login
  Then the API gateway intercepts the request
  And returns HTTP 401 Unauthorized
  And returns error code 'ERR-AUTH-002' or 'ERR-AUTH-003'
  And rejects access before invoking backend services
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Execute Staff Credential Login & Session Issuance in Autonomous Edge Mode
  Given the clinic workstation has lost WAN connectivity to cloud
  And the local edge mini-server is operational with local SQLite database
  When the staff member executes Staff Credential Login & Session Issuance
  Then the edge API gateway accepts the request locally
  And returns HTTP 200 within 250ms
  And appends the mutation to the local offline sync journal
  And synchronizes to cloud automatically upon network restoration
```

## 11. Requirements & Database Relational Traceability Matrix

Traceability mapping for all `Auth` endpoints:

| Endpoint ID | Upstream SRS Requirements | Workflow ID | Feature Code | Target Database Tables | Verification Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `API-AUTH-001` | `SRS-FR-001, SRS-NFR-008, BR-001` | `WF-001` | `FEATURE-001` | `auth_users, user_credentials, user_sessions` | `PLANNED-TEST-API-001` |
| `API-AUTH-002` | `SRS-FR-001, SRS-NFR-008` | `WF-001` | `FEATURE-001` | `user_sessions` | `PLANNED-TEST-API-002` |
| `API-AUTH-003` | `SRS-FR-001, SECR-002` | `WF-001` | `FEATURE-001` | `user_sessions` | `PLANNED-TEST-API-003` |
| `API-AUTH-004` | `SRS-FR-001, SRS-FR-005` | `WF-001` | `FEATURE-002` | `auth_users, roles, permissions, facilities` | `PLANNED-TEST-API-004` |
| `API-AUTH-005` | `SECR-001, SRS-NFR-008` | `WF-001` | `FEATURE-002` | `user_credentials, user_sessions` | `PLANNED-TEST-API-005` |
| `API-AUTH-006` | `SECR-003, ARCH-CONT-004` | `WF-001` | `FEATURE-001` | `system_configs` | `PLANNED-TEST-API-006` |
| `API-AUTH-007` | `SECR-002, SRS-FR-001` | `WF-001` | `FEATURE-001` | `user_credentials, user_sessions` | `PLANNED-TEST-API-007` |
| `API-AUTH-008` | `SECR-004, PRIV-002, WF-025` | `WF-025` | `FEATURE-003` | `user_sessions, audit_events, danger_alerts` | `PLANNED-TEST-API-008` |
| `API-AUTH-009` | `SECR-005, ARCH-CONT-002` | `WF-001` | `FEATURE-004` | `facilities, system_configs` | `PLANNED-TEST-API-009` |
| `API-AUTH-010` | `SECR-005` | `WF-001` | `FEATURE-004` | `facilities` | `PLANNED-TEST-API-010` |
| `API-AUTH-011` | `SECR-005` | `WF-001` | `FEATURE-004` | `facilities, user_sessions` | `PLANNED-TEST-API-011` |
| `API-AUTH-012` | `SRS-FR-005` | `WF-001` | `FEATURE-005` | `roles, permissions` | `PLANNED-TEST-API-012` |
| `API-AUTH-013` | `SRS-FR-005, SECR-002` | `WF-001` | `FEATURE-005` | `user_roles, staff_profiles` | `PLANNED-TEST-API-013` |
| `API-AUTH-014` | `SECR-002, SRS-NFR-008` | `WF-001` | `FEATURE-001` | `user_sessions, auth_users` | `PLANNED-TEST-API-014` |
| `API-AUTH-015` | `SECR-002` | `WF-001` | `FEATURE-001` | `user_sessions` | `PLANNED-TEST-API-015` |
| `API-AUTH-016` | `SRS-FR-005, WF-001` | `WF-001` | `FEATURE-006` | `staff_shifts, facility_rooms` | `PLANNED-TEST-API-016` |
