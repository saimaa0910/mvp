# 🔌 API Specification: Patient Registration, Demographics & Identity API Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** API-DOC-05 | **Status:** Authoritative Baseline | **Date:** September 2026
> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department
> **Standard Framework:** RFC 7231 (HTTP/1.1), JSON:API v1.1, DPDP Act 2023, ABDM Interoperability Standards
> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.

---

## 1. Executive Summary & Domain Scope

The **Patient Registration, Demographics & Identity API Specification** defines the authoritative, implementation-ready contracts for the `Patient` subsystem across all 183 Namma Clinic primary healthcare centers in Greater Bengaluru. This domain operates under the supervisory jurisdiction of `ROLE-019 (Front Desk Registration Operator)` and fulfills the core mission: **Manage citizen demographic intake, municipal UHID generation, Master Patient Index fuzzy deduplication, ABHA linkage, and longitudinal patient clinical history across 183 clinics.**

All 26 endpoints specified in this document adhere strictly to uniform JSON:API response envelopes, time-ordered UUIDv7 identifiers, ISO-8601 UTC timestamps, optimistic concurrency control via ETags, and automated audit logging.

## 2. Operational Architecture & Relational Mapping

The following table maps the domain's operational context to architectural containers, components, database tables, and default role entitlements:

| Dimension | Specification Detail |
| :--- | :--- |
| **Functional Domain** | `Patient` (Code: `PATIENT`) |
| **Authoritative Endpoints** | 26 Active Endpoints (`API-PATIENT-001` to `API-PATIENT-026`) |
| **Primary Architecture Container** | `ARCH-CONT-005` |
| **Assigned Component** | `ARCH-COMP-013` |
| **Primary Database Tables** | `patients, patient_identifiers, patient_contacts, patient_addresses` |
| **Lead Role Entitlement** | `ROLE-019 (Front Desk Registration Operator)` |
| **Default Rate Limiting** | `60 req/min per Facility` |
| **Offline Edge Support** | `Edge Autonomous Registration with Offline UUIDv7` |

## 3. Domain Operational State Machine

The operational state transitions governing entities within this domain are modeled below:

```mermaid
stateDiagram-v2
    [*] --> IntakeDraft: Citizen Arrives at Front Desk
    IntakeDraft --> DeduplicationCheck: Phonetic & Phone Search
    DeduplicationCheck --> Registered: No Duplicate Found (Assign UHID)
    DeduplicationCheck --> MergeCandidate: Duplicate Score > 0.85
    MergeCandidate --> SubsumedTombstone: Supervisory Merge Executed
    Registered --> AbhaLinked: ABHA OTP Verified
    Registered --> Deceased: Municipal Mortality Recorded
    Registered --> Merged: Merged into Surviving Record
    Deceased --> [*]
    Merged --> [*]
```

## 4. End-to-End Operational Data Flow

The sequence diagram below illustrates the end-to-end operational flow between frontline clinic staff, edge workstations, the central API gateway, and backing data stores:

```mermaid
sequenceDiagram
    autonumber
    participant Citizen as Citizen Patient
    participant Clerk as Registration Clerk
    participant UI as Front Desk Kiosk
    participant API as Patient Service
    participant MPI as Master Patient Index
    participant DB as PostgreSQL Database
    Citizen->>Clerk: Provide Name, Phone, Age, Ward
    Clerk->>UI: Enter Demographics
    UI->>API: POST /api/v1/patients/duplicates/check
    API->>MPI: Execute Phonetic & Exact Phone Match
    MPI-->>API: Zero Collisions Detected
    UI->>API: POST /api/v1/patients (Register)
    API->>DB: Insert Patient, Identifiers, Contacts
    API-->>UI: HTTP 201 Created (UHID: NC-BLR-2026-XXXX)
    UI-->>Clerk: Print Registration Slip
```

## 5. Domain Endpoint Inventory Catalog

Complete inventory of all 26 endpoints defined for the `Patient` domain:

| Endpoint ID | Method | URI Route Path | Functional Title | Role Context | Idempotency Standard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API-PATIENT-001** | `POST` | `/api/v1/patients` | Register New Citizen Patient Profile | `ROLE-019` | Supported via X-Idempotency-Key |
| **API-PATIENT-002** | `GET` | `/api/v1/patients/{patientId}` | Retrieve Citizen Demographic & Clinical Summary | `ROLE-016` | Read-Only Idempotent |
| **API-PATIENT-003** | `GET` | `/api/v1/patients` | Search Patients via UHID, Phone, or Phonetic Query | `ROLE-019` | Read-Only Idempotent |
| **API-PATIENT-004** | `PUT` | `/api/v1/patients/{patientId}` | Update Patient Demographic & Contact Details | `ROLE-019` | Optimistic Concurrency ETag |
| **API-PATIENT-005** | `POST` | `/api/v1/patients/duplicates/check` | Check Duplicate Citizen Candidate Matches | `ROLE-019` | Read-Only Idempotent |
| **API-PATIENT-006** | `POST` | `/api/v1/patients/merge` | Merge Subsumed Patient into Primary Profile | `ROLE-015` | Supported via X-Idempotency-Key |
| **API-PATIENT-007** | `POST` | `/api/v1/patients/{patientId}/abha/link` | Link Verified ABHA ID to Patient UHID | `ROLE-019` | Supported via X-Idempotency-Key |
| **API-PATIENT-008** | `DELETE` | `/api/v1/patients/{patientId}/abha/unlink` | Unlink ABHA Identity from Citizen UHID | `ROLE-019` | Idempotent Unlinking |
| **API-PATIENT-009** | `GET` | `/api/v1/patients/{patientId}/history` | Longitudinal Encounter & Clinical History | `ROLE-002` | Read-Only Idempotent |
| **API-PATIENT-010** | `GET` | `/api/v1/patients/{patientId}/consents` | Citizen Consent Artifacts & Preferences | `ROLE-011` | Read-Only Idempotent |
| **API-PATIENT-011** | `POST` | `/api/v1/patients/{patientId}/consents` | Record Citizen Consent Directive | `ROLE-019` | Supported via X-Idempotency-Key |
| **API-PATIENT-012** | `DELETE` | `/api/v1/patients/{patientId}/consents/{consentId}` | Revoke Citizen Consent Directive | `ROLE-019` | Idempotent Revocation |
| **API-PATIENT-013** | `GET` | `/api/v1/patients/{patientId}/audit` | Citizen Record Access Audit Trail | `ROLE-011` | Read-Only Idempotent |
| **API-PATIENT-014** | `POST` | `/api/v1/patients/{patientId}/ncd-enroll` | Enroll Patient in NCD Chronic Care Registry | `ROLE-002` | Supported via X-Idempotency-Key |
| **API-PATIENT-015** | `GET` | `/api/v1/patients/{patientId}/ncd-status` | Retrieve NCD Chronic Episode Status | `ROLE-016` | Read-Only Idempotent |
| **API-PATIENT-016** | `POST` | `/api/v1/patients/{patientId}/emergency-contacts` | Add Emergency Contact / Guardian | `ROLE-019` | Supported via X-Idempotency-Key |
| **API-PATIENT-017** | `GET` | `/api/v1/patients/{patientId}/identifiers` | List All Registered Patient Identifiers | `ROLE-019` | Read-Only Idempotent |
| **API-PATIENT-018** | `POST` | `/api/v1/patients/{patientId}/identifiers` | Bind Supplemental Identifier to Citizen Profile | `ROLE-019` | Supported via X-Idempotency-Key |
| **API-PATIENT-019** | `DELETE` | `/api/v1/patients/{patientId}/identifiers/{identifierId}` | Remove Erroneous Supplemental Identifier | `ROLE-015` | Idempotent Deletion |
| **API-PATIENT-020** | `POST` | `/api/v1/patients/{patientId}/flag-deceased` | Mark Patient Record Deceased | `ROLE-015` | Supported via X-Idempotency-Key |
| **API-PATIENT-021** | `GET` | `/api/v1/patients/{patientId}/encounters` | List Patient Past Encounters | `ROLE-002` | Read-Only Idempotent |
| **API-PATIENT-022** | `GET` | `/api/v1/patients/{patientId}/prescriptions` | List Patient Historical Prescriptions | `ROLE-017` | Read-Only Idempotent |
| **API-PATIENT-023** | `GET` | `/api/v1/patients/{patientId}/lab-reports` | List Patient Historical Diagnostic Lab Results | `ROLE-018` | Read-Only Idempotent |
| **API-PATIENT-024** | `POST` | `/api/v1/patients/{patientId}/photo` | Upload Citizen Web-Cam Identification Photo | `ROLE-019` | Supported via X-Idempotency-Key |
| **API-PATIENT-025** | `GET` | `/api/v1/patients/{patientId}/photo` | Fetch Citizen Verification Photo | `ROLE-016` | Read-Only Idempotent |
| **API-PATIENT-026** | `POST` | `/api/v1/patients/batch-lookup` | Batch Patient UHID Verification | `ROLE-014` | Read-Only Idempotent |

## 6. Comprehensive Endpoint Technical Specifications

Exhaustive technical contracts for all 26 endpoints in the `Patient` domain:

### 6.1 `API-PATIENT-001`: Register New Citizen Patient Profile

- **API Identifier:** `API-PATIENT-001`
- **HTTP Route:** `POST /api/v1/patients`
- **Functional Purpose:** Perform demographic intake, assign municipal UHID, bind ABHA reference, and register new patient record.
- **Product Capability:** `CAPABILITY-010` | **Feature Code:** `FEATURE-010`
- **Primary Actor:** Registration Clerk | **User Persona:** Front Desk Operator
- **Required RBAC Role:** `ROLE-019`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:profile:create`
- **ABAC Scoping Rule:** Clinic front desk clerk or nurse in active facility context.
- **Upstream Traceability:** `SRS-FR-007, SRS-FR-008, BR-002, PRIV-001` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, patient_identifiers, patient_contacts, patient_addresses`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `60 req/min per Facility`
- **Offline Edge Resilience:** Edge Autonomous Registration with Offline UUIDv7
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-017`
- **Planned Verification Test Case:** `PLANNED-TEST-API-017`
- **Dependency DAG Edge:** `API-DEP-017`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients:
    post:
      summary: "Register New Citizen Patient Profile"
      tags:
        - "Patient"
      operationId: "post_api_v1_patients"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PatientRegistrationRequest"
      responses:
        '201':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/PatientProfileResponse"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients" \
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
  "operation": "Register New Citizen Patient Profile",
  "domain": "Patient",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PATIENT-001"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-001",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-002",
    "message": "Domain constraint validation failed during execution of API-PATIENT-001.",
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
- **Relational Database Mutation:** Modifies tables `patients, patient_identifiers, patient_contacts, patient_addresses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-017` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-017` under simulated offline network conditions.

### 6.2 `API-PATIENT-002`: Retrieve Citizen Demographic & Clinical Summary

- **API Identifier:** `API-PATIENT-002`
- **HTTP Route:** `GET /api/v1/patients/{patientId}`
- **Functional Purpose:** Retrieve citizen profile, contact details, ABHA linkage status, and chronic disease registry markers.
- **Product Capability:** `CAPABILITY-010` | **Feature Code:** `FEATURE-010`
- **Primary Actor:** Clinical & Admin Staff | **User Persona:** Clinician / Nurse / Clerk
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:profile:read`
- **ABAC Scoping Rule:** Masks phone number and Aadhaar reference unless authorized clinician.
- **Upstream Traceability:** `SRS-FR-007, PRIV-001` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, patient_identifiers, patient_contacts`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `600ms`
- **Rate Limiting Policy:** `120 req/min per User`
- **Offline Edge Resilience:** Edge SQLite Local Cache
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-018`
- **Planned Verification Test Case:** `PLANNED-TEST-API-018`
- **Dependency DAG Edge:** `API-DEP-018`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}:
    get:
      summary: "Retrieve Citizen Demographic & Clinical Summary"
      tags:
        - "Patient"
      operationId: "get_api_v1_patients_patientId"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/PatientProfileResponse"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-002",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-002.",
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
- **Relational Database Mutation:** Modifies tables `patients, patient_identifiers, patient_contacts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-018` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-018` under simulated offline network conditions.

### 6.3 `API-PATIENT-003`: Search Patients via UHID, Phone, or Phonetic Query

- **API Identifier:** `API-PATIENT-003`
- **HTTP Route:** `GET /api/v1/patients`
- **Functional Purpose:** Search citizen directory using phone number, exact UHID, ABHA number, or phonetic fuzzy name search.
- **Product Capability:** `CAPABILITY-011` | **Feature Code:** `FEATURE-011`
- **Primary Actor:** Frontline Staff | **User Persona:** Front Desk Operator
- **Required RBAC Role:** `ROLE-019`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:search:execute`
- **ABAC Scoping Rule:** Search results capped at 50 records; rate limited to prevent scraping.
- **Upstream Traceability:** `SRS-FR-008, SRS-NFR-002` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, patient_identifiers, patient_contacts`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `1000ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Full-Text SQLite Match
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-019`
- **Planned Verification Test Case:** `PLANNED-TEST-API-019`
- **Dependency DAG Edge:** `API-DEP-019`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients:
    get:
      summary: "Search Patients via UHID, Phone, or Phonetic Query"
      tags:
        - "Patient"
      operationId: "get_api_v1_patients"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-003",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-012",
    "message": "Domain constraint validation failed during execution of API-PATIENT-003.",
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
- **Relational Database Mutation:** Modifies tables `patients, patient_identifiers, patient_contacts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-019` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-019` under simulated offline network conditions.

### 6.4 `API-PATIENT-004`: Update Patient Demographic & Contact Details

- **API Identifier:** `API-PATIENT-004`
- **HTTP Route:** `PUT /api/v1/patients/{patientId}`
- **Functional Purpose:** Modify address, phone number, emergency contact, or demographic metadata with optimistic concurrency check.
- **Product Capability:** `CAPABILITY-010` | **Feature Code:** `FEATURE-010`
- **Primary Actor:** Registration Clerk | **User Persona:** Front Desk Operator
- **Required RBAC Role:** `ROLE-019`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:profile:update`
- **ABAC Scoping Rule:** Requires If-Match ETag header matching current version.
- **Upstream Traceability:** `SRS-FR-007` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, patient_contacts, patient_addresses`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Optimistic Concurrency ETag
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `30 req/min per User`
- **Offline Edge Resilience:** Edge Local Mutation Replay
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-020`
- **Planned Verification Test Case:** `PLANNED-TEST-API-020`
- **Dependency DAG Edge:** `API-DEP-020`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}:
    put:
      summary: "Update Patient Demographic & Contact Details"
      tags:
        - "Patient"
      operationId: "put_api_v1_patients_patientId"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PatientRegistrationRequest"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/PatientProfileResponse"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001" \
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
  "operation": "Update Patient Demographic & Contact Details",
  "domain": "Patient",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PATIENT-004"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-004",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-004.",
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
- **Relational Database Mutation:** Modifies tables `patients, patient_contacts, patient_addresses` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-020` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-020` under simulated offline network conditions.

### 6.5 `API-PATIENT-005`: Check Duplicate Citizen Candidate Matches

- **API Identifier:** `API-PATIENT-005`
- **HTTP Route:** `POST /api/v1/patients/duplicates/check`
- **Functional Purpose:** Evaluate intake demographics against Master Patient Index to detect existing registered records.
- **Product Capability:** `CAPABILITY-012` | **Feature Code:** `FEATURE-012`
- **Primary Actor:** Registration Clerk | **User Persona:** Front Desk Operator
- **Required RBAC Role:** `ROLE-019`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:dedup:check`
- **ABAC Scoping Rule:** Executes phonetic Jaro-Winkler and Soundex matching algorithm.
- **Upstream Traceability:** `SRS-FR-008, BR-002` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, patient_contacts`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `1200ms`
- **Rate Limiting Policy:** `60 req/min per Facility`
- **Offline Edge Resilience:** Edge Local Heuristic Check
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-021`
- **Planned Verification Test Case:** `PLANNED-TEST-API-021`
- **Dependency DAG Edge:** `API-DEP-021`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/duplicates/check:
    post:
      summary: "Check Duplicate Citizen Candidate Matches"
      tags:
        - "Patient"
      operationId: "post_api_v1_patients_duplicates_check"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PatientRegistrationRequest"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/duplicates/check" \
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
  "operation": "Check Duplicate Citizen Candidate Matches",
  "domain": "Patient",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PATIENT-005"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-005",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-003",
    "message": "Domain constraint validation failed during execution of API-PATIENT-005.",
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
- **Relational Database Mutation:** Modifies tables `patients, patient_contacts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-021` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-021` under simulated offline network conditions.

### 6.6 `API-PATIENT-006`: Merge Subsumed Patient into Primary Profile

- **API Identifier:** `API-PATIENT-006`
- **HTTP Route:** `POST /api/v1/patients/merge`
- **Functional Purpose:** Supervisory command consolidating duplicate records, re-pointing clinical encounters, and tombstoning subsumed record.
- **Product Capability:** `CAPABILITY-012` | **Feature Code:** `FEATURE-012`
- **Primary Actor:** Medical Superintendent | **User Persona:** Zonal Officer
- **Required RBAC Role:** `ROLE-015`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:merge:execute`
- **ABAC Scoping Rule:** Requires clinical justification note; non-reversible without supervisory DBA intervention.
- **Upstream Traceability:** `SRS-FR-008, WF-002` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, clinical_encounters, prescriptions, audit_events`
- **Data Security Tier:** `HIGHLY-RESTRICTED`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `3000ms`
- **Rate Limiting Policy:** `10 req/hour per Supervisor`
- **Offline Edge Resilience:** Prohibited Offline (Cloud Only)
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-022`
- **Planned Verification Test Case:** `PLANNED-TEST-API-022`
- **Dependency DAG Edge:** `API-DEP-022`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/merge:
    post:
      summary: "Merge Subsumed Patient into Primary Profile"
      tags:
        - "Patient"
      operationId: "post_api_v1_patients_merge"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PatientMergeRequest"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/merge" \
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
  "operation": "Merge Subsumed Patient into Primary Profile",
  "domain": "Patient",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PATIENT-006"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-006",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-006",
    "message": "Domain constraint validation failed during execution of API-PATIENT-006.",
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
- **Relational Database Mutation:** Modifies tables `patients, clinical_encounters, prescriptions, audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-022` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-022` under simulated offline network conditions.

### 6.7 `API-PATIENT-007`: Link Verified ABHA ID to Patient UHID

- **API Identifier:** `API-PATIENT-007`
- **HTTP Route:** `POST /api/v1/patients/{patientId}/abha/link`
- **Functional Purpose:** Associate verified ABHA number/address with local patient UHID following successful OTP validation.
- **Product Capability:** `CAPABILITY-013` | **Feature Code:** `FEATURE-013`
- **Primary Actor:** Registration Clerk | **User Persona:** Front Desk Operator
- **Required RBAC Role:** `ROLE-019`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:abha:link`
- **ABAC Scoping Rule:** Validates ABHA token issued by NHA ABDM gateway.
- **Upstream Traceability:** `SRS-FR-055, INT-001, WF-024` | **Workflow:** `WF-024`
- **Container / Component:** `ARCH-CONT-014` / `ARCH-COMP-040`
- **Target Relational Tables:** `patients, patient_identifiers, abdm_artifacts`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `2500ms`
- **Rate Limiting Policy:** `30 req/min per Facility`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-023`
- **Planned Verification Test Case:** `PLANNED-TEST-API-023`
- **Dependency DAG Edge:** `API-DEP-023`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/abha/link:
    post:
      summary: "Link Verified ABHA ID to Patient UHID"
      tags:
        - "Patient"
      operationId: "post_api_v1_patients_patientId_abha_link"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/AbhaVerificationRequest"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/abha/link" \
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
  "operation": "Link Verified ABHA ID to Patient UHID",
  "domain": "Patient",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PATIENT-007"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-007",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-010",
    "message": "Domain constraint validation failed during execution of API-PATIENT-007.",
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
- **Relational Database Mutation:** Modifies tables `patients, patient_identifiers, abdm_artifacts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-023` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-023` under simulated offline network conditions.

### 6.8 `API-PATIENT-008`: Unlink ABHA Identity from Citizen UHID

- **API Identifier:** `API-PATIENT-008`
- **HTTP Route:** `DELETE /api/v1/patients/{patientId}/abha/unlink`
- **Functional Purpose:** Revoke ABHA linkage upon citizen statutory request, maintaining local municipal UHID continuity.
- **Product Capability:** `CAPABILITY-013` | **Feature Code:** `FEATURE-013`
- **Primary Actor:** Registration Clerk | **User Persona:** Front Desk Operator
- **Required RBAC Role:** `ROLE-019`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:abha:unlink`
- **ABAC Scoping Rule:** Citizen consent revocation verified.
- **Upstream Traceability:** `SRS-FR-055, PRIV-001` | **Workflow:** `WF-024`
- **Container / Component:** `ARCH-CONT-014` / `ARCH-COMP-040`
- **Target Relational Tables:** `patients, patient_identifiers`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Idempotent Unlinking
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `10 req/min per Facility`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-024`
- **Planned Verification Test Case:** `PLANNED-TEST-API-024`
- **Dependency DAG Edge:** `API-DEP-024`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/abha/unlink:
    delete:
      summary: "Unlink ABHA Identity from Citizen UHID"
      tags:
        - "Patient"
      operationId: "delete_api_v1_patients_patientId_abha_unlink"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/abha/unlink" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-008",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-008.",
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
- **Relational Database Mutation:** Modifies tables `patients, patient_identifiers` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-024` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-024` under simulated offline network conditions.

### 6.9 `API-PATIENT-009`: Longitudinal Encounter & Clinical History

- **API Identifier:** `API-PATIENT-009`
- **HTTP Route:** `GET /api/v1/patients/{patientId}/history`
- **Functional Purpose:** Retrieve complete longitudinal timeline of outpatient visits, vitals, prescriptions, and lab investigations.
- **Product Capability:** `CAPABILITY-014` | **Feature Code:** `FEATURE-014`
- **Primary Actor:** Medical Officer | **User Persona:** Clinic Doctor
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:clinical_history:read`
- **ABAC Scoping Rule:** Treating clinician context required; audit event logged.
- **Upstream Traceability:** `SRS-FR-014, PRIV-001` | **Workflow:** `WF-005`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters, prescriptions, lab_orders, referrals`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `1200ms`
- **Rate Limiting Policy:** `60 req/min per Doctor`
- **Offline Edge Resilience:** Edge Local Encrypted SQLite Mirror
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-025`
- **Planned Verification Test Case:** `PLANNED-TEST-API-025`
- **Dependency DAG Edge:** `API-DEP-025`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/history:
    get:
      summary: "Longitudinal Encounter & Clinical History"
      tags:
        - "Patient"
      operationId: "get_api_v1_patients_patientId_history"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/history" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-009",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-009.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters, prescriptions, lab_orders, referrals` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-025` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-025` under simulated offline network conditions.

### 6.10 `API-PATIENT-010`: Citizen Consent Artifacts & Preferences

- **API Identifier:** `API-PATIENT-010`
- **HTTP Route:** `GET /api/v1/patients/{patientId}/consents`
- **Functional Purpose:** List active, expired, and revoked citizen consent directives governing data sharing and notifications.
- **Product Capability:** `CAPABILITY-015` | **Feature Code:** `FEATURE-015`
- **Primary Actor:** Privacy Officer / Staff | **User Persona:** Frontline Staff
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:consent:read`
- **ABAC Scoping Rule:** DPDP Act 2023 compliance verification.
- **Upstream Traceability:** `PRIV-001, RETENTION-005` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `consent_records`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `600ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Cached
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-026`
- **Planned Verification Test Case:** `PLANNED-TEST-API-026`
- **Dependency DAG Edge:** `API-DEP-026`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/consents:
    get:
      summary: "Citizen Consent Artifacts & Preferences"
      tags:
        - "Patient"
      operationId: "get_api_v1_patients_patientId_consents"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/consents" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-010",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-010.",
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
- **Relational Database Mutation:** Modifies tables `consent_records` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-026` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-026` under simulated offline network conditions.

### 6.11 `API-PATIENT-011`: Record Citizen Consent Directive

- **API Identifier:** `API-PATIENT-011`
- **HTTP Route:** `POST /api/v1/patients/{patientId}/consents`
- **Functional Purpose:** Capture signed citizen consent artifact or notice acceptance for public health reporting or teleconsultation.
- **Product Capability:** `CAPABILITY-015` | **Feature Code:** `FEATURE-015`
- **Primary Actor:** Registration Staff | **User Persona:** Front Desk Operator
- **Required RBAC Role:** `ROLE-019`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:consent:record`
- **ABAC Scoping Rule:** Must specify purpose, validity period, and authorized data scope.
- **Upstream Traceability:** `PRIV-001, DPDP-ACT-2023` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `consent_records`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1000ms`
- **Rate Limiting Policy:** `30 req/min per Facility`
- **Offline Edge Resilience:** Edge Local Capture with Cloud Sync
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-027`
- **Planned Verification Test Case:** `PLANNED-TEST-API-027`
- **Dependency DAG Edge:** `API-DEP-027`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/consents:
    post:
      summary: "Record Citizen Consent Directive"
      tags:
        - "Patient"
      operationId: "post_api_v1_patients_patientId_consents"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/DataPortabilityConsentProof"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/consents" \
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
  "operation": "Record Citizen Consent Directive",
  "domain": "Patient",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PATIENT-011"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-011",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-011.",
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
- **Relational Database Mutation:** Modifies tables `consent_records` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-027` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-027` under simulated offline network conditions.

### 6.12 `API-PATIENT-012`: Revoke Citizen Consent Directive

- **API Identifier:** `API-PATIENT-012`
- **HTTP Route:** `DELETE /api/v1/patients/{patientId}/consents/{consentId}`
- **Functional Purpose:** Revoke citizen consent, immediately halting external data dissemination and triggering audit notice.
- **Product Capability:** `CAPABILITY-015` | **Feature Code:** `FEATURE-015`
- **Primary Actor:** Citizen / Front Desk Staff | **User Persona:** Front Desk Operator
- **Required RBAC Role:** `ROLE-019`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:consent:revoke`
- **ABAC Scoping Rule:** Immediate cessation of non-essential processing.
- **Upstream Traceability:** `PRIV-001, DPDP-ACT-2023` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `consent_records`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Idempotent Revocation
- **Execution Timeout:** `1000ms`
- **Rate Limiting Policy:** `20 req/min per Facility`
- **Offline Edge Resilience:** Immediate Local Enforcement
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-028`
- **Planned Verification Test Case:** `PLANNED-TEST-API-028`
- **Dependency DAG Edge:** `API-DEP-028`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/consents/{consentId}:
    delete:
      summary: "Revoke Citizen Consent Directive"
      tags:
        - "Patient"
      operationId: "delete_api_v1_patients_patientId_consents_consentId"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/consents/{consentId}" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-012",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-012.",
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
- **Relational Database Mutation:** Modifies tables `consent_records` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-028` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-028` under simulated offline network conditions.

### 6.13 `API-PATIENT-013`: Citizen Record Access Audit Trail

- **API Identifier:** `API-PATIENT-013`
- **HTTP Route:** `GET /api/v1/patients/{patientId}/audit`
- **Functional Purpose:** Retrieve immutable log of all staff accesses, clinical views, and updates to the citizen's record.
- **Product Capability:** `CAPABILITY-016` | **Feature Code:** `FEATURE-016`
- **Primary Actor:** Privacy Officer / Legal Counsel | **User Persona:** Compliance Officer
- **Required RBAC Role:** `ROLE-011`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:audit:read`
- **ABAC Scoping Rule:** Requires authorized compliance audit justification.
- **Upstream Traceability:** `SECR-004, RETENTION-006` | **Workflow:** `WF-020`
- **Container / Component:** `ARCH-CONT-017` / `ARCH-COMP-049`
- **Target Relational Tables:** `audit_events`
- **Data Security Tier:** `HIGHLY-RESTRICTED`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `20 req/min per Auditor`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-029`
- **Planned Verification Test Case:** `PLANNED-TEST-API-029`
- **Dependency DAG Edge:** `API-DEP-029`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/audit:
    get:
      summary: "Citizen Record Access Audit Trail"
      tags:
        - "Patient"
      operationId: "get_api_v1_patients_patientId_audit"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/audit" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-013",
      "domain": "Patient",
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
    "code": "ERR-AUDIT-002",
    "message": "Domain constraint validation failed during execution of API-PATIENT-013.",
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
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-029` under simulated offline network conditions.

### 6.14 `API-PATIENT-014`: Enroll Patient in NCD Chronic Care Registry

- **API Identifier:** `API-PATIENT-014`
- **HTTP Route:** `POST /api/v1/patients/{patientId}/ncd-enroll`
- **Functional Purpose:** Enroll patient into BBMP municipal Non-Communicable Disease (hypertension, diabetes) longitudinal care protocol.
- **Product Capability:** `CAPABILITY-017` | **Feature Code:** `FEATURE-017`
- **Primary Actor:** Medical Officer / Nurse | **User Persona:** Clinic Doctor
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:ncd:enroll`
- **ABAC Scoping Rule:** Patient must have confirmed diagnosis of hypertension, diabetes, or cardiovascular risk.
- **Upstream Traceability:** `SRS-FR-025, RETENTION-013` | **Workflow:** `WF-005`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `ncd_episodes, follow_up_schedules`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `30 req/min per Clinician`
- **Offline Edge Resilience:** Edge Local Queue
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-030`
- **Planned Verification Test Case:** `PLANNED-TEST-API-030`
- **Dependency DAG Edge:** `API-DEP-030`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/ncd-enroll:
    post:
      summary: "Enroll Patient in NCD Chronic Care Registry"
      tags:
        - "Patient"
      operationId: "post_api_v1_patients_patientId_ncd-enroll"
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
        '404':
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/ncd-enroll" \
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
  "operation": "Enroll Patient in NCD Chronic Care Registry",
  "domain": "Patient",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PATIENT-014"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-014",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-014.",
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
- **Relational Database Mutation:** Modifies tables `ncd_episodes, follow_up_schedules` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-030` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-030` under simulated offline network conditions.

### 6.15 `API-PATIENT-015`: Retrieve NCD Chronic Episode Status

- **API Identifier:** `API-PATIENT-015`
- **HTTP Route:** `GET /api/v1/patients/{patientId}/ncd-status`
- **Functional Purpose:** Query current glycemic control, blood pressure control status, and upcoming refill dates.
- **Product Capability:** `CAPABILITY-017` | **Feature Code:** `FEATURE-017`
- **Primary Actor:** Clinician / Pharmacist | **User Persona:** Care Team
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:ncd:read`
- **ABAC Scoping Rule:** Active clinic care team context.
- **Upstream Traceability:** `SRS-FR-025` | **Workflow:** `WF-005`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `ncd_episodes`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `600ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge SQLite Mirror
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-031`
- **Planned Verification Test Case:** `PLANNED-TEST-API-031`
- **Dependency DAG Edge:** `API-DEP-031`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/ncd-status:
    get:
      summary: "Retrieve NCD Chronic Episode Status"
      tags:
        - "Patient"
      operationId: "get_api_v1_patients_patientId_ncd-status"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/ncd-status" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-015",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-015.",
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
- **Relational Database Mutation:** Modifies tables `ncd_episodes` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-031` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-031` under simulated offline network conditions.

### 6.16 `API-PATIENT-016`: Add Emergency Contact / Guardian

- **API Identifier:** `API-PATIENT-016`
- **HTTP Route:** `POST /api/v1/patients/{patientId}/emergency-contacts`
- **Functional Purpose:** Register secondary next-of-kin or guardian contact numbers for minor or elderly patients.
- **Product Capability:** `CAPABILITY-010` | **Feature Code:** `FEATURE-010`
- **Primary Actor:** Registration Staff | **User Persona:** Front Desk Operator
- **Required RBAC Role:** `ROLE-019`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:profile:update`
- **ABAC Scoping Rule:** Valid 10-digit mobile number required.
- **Upstream Traceability:** `SRS-FR-007` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patient_contacts`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1000ms`
- **Rate Limiting Policy:** `30 req/min per User`
- **Offline Edge Resilience:** Edge Local Queue
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-032`
- **Planned Verification Test Case:** `PLANNED-TEST-API-032`
- **Dependency DAG Edge:** `API-DEP-032`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/emergency-contacts:
    post:
      summary: "Add Emergency Contact / Guardian"
      tags:
        - "Patient"
      operationId: "post_api_v1_patients_patientId_emergency-contacts"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PatientRegistrationRequest"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/emergency-contacts" \
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
  "operation": "Add Emergency Contact / Guardian",
  "domain": "Patient",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PATIENT-016"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-016",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-003",
    "message": "Domain constraint validation failed during execution of API-PATIENT-016.",
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
- **Relational Database Mutation:** Modifies tables `patient_contacts` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-032` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-032` under simulated offline network conditions.

### 6.17 `API-PATIENT-017`: List All Registered Patient Identifiers

- **API Identifier:** `API-PATIENT-017`
- **HTTP Route:** `GET /api/v1/patients/{patientId}/identifiers`
- **Functional Purpose:** Retrieve all bound identifiers: municipal UHID, ABHA number, ABHA address, ration card, voter ID.
- **Product Capability:** `CAPABILITY-010` | **Feature Code:** `FEATURE-010`
- **Primary Actor:** Frontline Staff | **User Persona:** Front Desk Operator
- **Required RBAC Role:** `ROLE-019`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:profile:read`
- **ABAC Scoping Rule:** Masks sensitive national ID digits on non-admin interface.
- **Upstream Traceability:** `SRS-FR-007` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patient_identifiers`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `500ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge SQLite Mirror
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-033`
- **Planned Verification Test Case:** `PLANNED-TEST-API-033`
- **Dependency DAG Edge:** `API-DEP-033`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/identifiers:
    get:
      summary: "List All Registered Patient Identifiers"
      tags:
        - "Patient"
      operationId: "get_api_v1_patients_patientId_identifiers"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/identifiers" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-017",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-017.",
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
- **Relational Database Mutation:** Modifies tables `patient_identifiers` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-033` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-033` under simulated offline network conditions.

### 6.18 `API-PATIENT-018`: Bind Supplemental Identifier to Citizen Profile

- **API Identifier:** `API-PATIENT-018`
- **HTTP Route:** `POST /api/v1/patients/{patientId}/identifiers`
- **Functional Purpose:** Add municipal welfare card, BPL ration card number, or state health scheme ID to patient profile.
- **Product Capability:** `CAPABILITY-010` | **Feature Code:** `FEATURE-010`
- **Primary Actor:** Registration Staff | **User Persona:** Front Desk Operator
- **Required RBAC Role:** `ROLE-019`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:profile:update`
- **ABAC Scoping Rule:** Validates format against identifier type schema.
- **Upstream Traceability:** `SRS-FR-007` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patient_identifiers`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1200ms`
- **Rate Limiting Policy:** `30 req/min per Facility`
- **Offline Edge Resilience:** Edge Local Queue
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-034`
- **Planned Verification Test Case:** `PLANNED-TEST-API-034`
- **Dependency DAG Edge:** `API-DEP-034`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/identifiers:
    post:
      summary: "Bind Supplemental Identifier to Citizen Profile"
      tags:
        - "Patient"
      operationId: "post_api_v1_patients_patientId_identifiers"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PatientRegistrationRequest"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/identifiers" \
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
  "operation": "Bind Supplemental Identifier to Citizen Profile",
  "domain": "Patient",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PATIENT-018"
  }
}
```

#### Successful Response Wire Representation (`HTTP 201`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-018",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-018.",
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
- **Relational Database Mutation:** Modifies tables `patient_identifiers` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-034` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-034` under simulated offline network conditions.

### 6.19 `API-PATIENT-019`: Remove Erroneous Supplemental Identifier

- **API Identifier:** `API-PATIENT-019`
- **HTTP Route:** `DELETE /api/v1/patients/{patientId}/identifiers/{identifierId}`
- **Functional Purpose:** Remove misattributed supplemental identifier; core municipal UHID cannot be deleted.
- **Product Capability:** `CAPABILITY-010` | **Feature Code:** `FEATURE-010`
- **Primary Actor:** Supervisor | **User Persona:** Superintendent
- **Required RBAC Role:** `ROLE-015`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:profile:update`
- **ABAC Scoping Rule:** Primary UHID deletion prohibited; audit justification mandatory.
- **Upstream Traceability:** `SRS-FR-007` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patient_identifiers`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Idempotent Deletion
- **Execution Timeout:** `1000ms`
- **Rate Limiting Policy:** `10 req/min per Supervisor`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-035`
- **Planned Verification Test Case:** `PLANNED-TEST-API-035`
- **Dependency DAG Edge:** `API-DEP-035`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/identifiers/{identifierId}:
    delete:
      summary: "Remove Erroneous Supplemental Identifier"
      tags:
        - "Patient"
      operationId: "delete_api_v1_patients_patientId_identifiers_identifierId"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/identifiers/{identifierId}" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-019",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-019.",
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
- **Relational Database Mutation:** Modifies tables `patient_identifiers` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-035` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-035` under simulated offline network conditions.

### 6.20 `API-PATIENT-020`: Mark Patient Record Deceased

- **API Identifier:** `API-PATIENT-020`
- **HTTP Route:** `POST /api/v1/patients/{patientId}/flag-deceased`
- **Functional Purpose:** Record formal municipal mortality event, halting outpatient reminders and locking appointment generation.
- **Product Capability:** `CAPABILITY-018` | **Feature Code:** `FEATURE-018`
- **Primary Actor:** Medical Superintendent | **User Persona:** Zonal Officer
- **Required RBAC Role:** `ROLE-015`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:status:deceased`
- **ABAC Scoping Rule:** Requires municipal death registration number or clinician confirmation.
- **Upstream Traceability:** `SRS-FR-007, RETENTION-001` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients, audit_events`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `1500ms`
- **Rate Limiting Policy:** `10 req/day per Supervisor`
- **Offline Edge Resilience:** Cloud Only
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-036`
- **Planned Verification Test Case:** `PLANNED-TEST-API-036`
- **Dependency DAG Edge:** `API-DEP-036`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/flag-deceased:
    post:
      summary: "Mark Patient Record Deceased"
      tags:
        - "Patient"
      operationId: "post_api_v1_patients_patientId_flag-deceased"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/flag-deceased" \
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
  "operation": "Mark Patient Record Deceased",
  "domain": "Patient",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PATIENT-020"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-020",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-020.",
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
- **Relational Database Mutation:** Modifies tables `patients, audit_events` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-036` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-036` under simulated offline network conditions.

### 6.21 `API-PATIENT-021`: List Patient Past Encounters

- **API Identifier:** `API-PATIENT-021`
- **HTTP Route:** `GET /api/v1/patients/{patientId}/encounters`
- **Functional Purpose:** Paginated retrieval of all previous clinic visits, dates, attending doctors, and primary diagnoses.
- **Product Capability:** `CAPABILITY-014` | **Feature Code:** `FEATURE-014`
- **Primary Actor:** Clinician | **User Persona:** Clinic Doctor
- **Required RBAC Role:** `ROLE-002`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:encounters:read`
- **ABAC Scoping Rule:** Filtered by date range or clinical encounter type.
- **Upstream Traceability:** `SRS-FR-014` | **Workflow:** `WF-005`
- **Container / Component:** `ARCH-CONT-007` / `ARCH-COMP-019`
- **Target Relational Tables:** `clinical_encounters`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per Doctor`
- **Offline Edge Resilience:** Edge SQLite Local Cache
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-037`
- **Planned Verification Test Case:** `PLANNED-TEST-API-037`
- **Dependency DAG Edge:** `API-DEP-037`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/encounters:
    get:
      summary: "List Patient Past Encounters"
      tags:
        - "Patient"
      operationId: "get_api_v1_patients_patientId_encounters"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/encounters" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-021",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-021.",
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
- **Relational Database Mutation:** Modifies tables `clinical_encounters` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-037` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-037` under simulated offline network conditions.

### 6.22 `API-PATIENT-022`: List Patient Historical Prescriptions

- **API Identifier:** `API-PATIENT-022`
- **HTTP Route:** `GET /api/v1/patients/{patientId}/prescriptions`
- **Functional Purpose:** Retrieve medication history, active regimens, and past dispensed drug items.
- **Product Capability:** `CAPABILITY-014` | **Feature Code:** `FEATURE-014`
- **Primary Actor:** Clinician / Pharmacist | **User Persona:** Doctor / Pharmacist
- **Required RBAC Role:** `ROLE-017`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `prescription:history:read`
- **ABAC Scoping Rule:** Scoped to active patient encounter.
- **Upstream Traceability:** `SRS-FR-017` | **Workflow:** `WF-006`
- **Container / Component:** `ARCH-CONT-008` / `ARCH-COMP-022`
- **Target Relational Tables:** `prescriptions, prescription_items`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `800ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge SQLite Local Cache
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-038`
- **Planned Verification Test Case:** `PLANNED-TEST-API-038`
- **Dependency DAG Edge:** `API-DEP-038`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/prescriptions:
    get:
      summary: "List Patient Historical Prescriptions"
      tags:
        - "Patient"
      operationId: "get_api_v1_patients_patientId_prescriptions"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/prescriptions" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-022",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-022.",
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
- **Relational Database Mutation:** Modifies tables `prescriptions, prescription_items` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-038` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-038` under simulated offline network conditions.

### 6.23 `API-PATIENT-023`: List Patient Historical Diagnostic Lab Results

- **API Identifier:** `API-PATIENT-023`
- **HTTP Route:** `GET /api/v1/patients/{patientId}/lab-reports`
- **Functional Purpose:** Retrieve longitudinal laboratory investigation history and abnormal flag trends.
- **Product Capability:** `CAPABILITY-014` | **Feature Code:** `FEATURE-014`
- **Primary Actor:** Clinician / Lab Tech | **User Persona:** Doctor / Lab Tech
- **Required RBAC Role:** `ROLE-018`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `lab:history:read`
- **ABAC Scoping Rule:** Full reports returned for verified clinicians.
- **Upstream Traceability:** `SRS-FR-021` | **Workflow:** `WF-008`
- **Container / Component:** `ARCH-CONT-010` / `ARCH-COMP-028`
- **Target Relational Tables:** `lab_orders, lab_results`
- **Data Security Tier:** `CONFIDENTIAL`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `1000ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge SQLite Local Cache
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-039`
- **Planned Verification Test Case:** `PLANNED-TEST-API-039`
- **Dependency DAG Edge:** `API-DEP-039`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/lab-reports:
    get:
      summary: "List Patient Historical Diagnostic Lab Results"
      tags:
        - "Patient"
      operationId: "get_api_v1_patients_patientId_lab-reports"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/lab-reports" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-023",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-023.",
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
- **Relational Database Mutation:** Modifies tables `lab_orders, lab_results` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-039` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-039` under simulated offline network conditions.

### 6.24 `API-PATIENT-024`: Upload Citizen Web-Cam Identification Photo

- **API Identifier:** `API-PATIENT-024`
- **HTTP Route:** `POST /api/v1/patients/{patientId}/photo`
- **Functional Purpose:** Capture optional webcam portrait of citizen for quick front-desk verification.
- **Product Capability:** `CAPABILITY-010` | **Feature Code:** `FEATURE-010`
- **Primary Actor:** Registration Clerk | **User Persona:** Front Desk Operator
- **Required RBAC Role:** `ROLE-019`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:profile:update`
- **ABAC Scoping Rule:** Image clamped to max 500KB JPEG; processed for biometric compliance.
- **Upstream Traceability:** `SRS-FR-007, PRIV-001` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Supported via X-Idempotency-Key
- **Execution Timeout:** `3000ms`
- **Rate Limiting Policy:** `30 req/min per Facility`
- **Offline Edge Resilience:** Edge Local Temporary Storage
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-040`
- **Planned Verification Test Case:** `PLANNED-TEST-API-040`
- **Dependency DAG Edge:** `API-DEP-040`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/photo:
    post:
      summary: "Upload Citizen Web-Cam Identification Photo"
      tags:
        - "Patient"
      operationId: "post_api_v1_patients_patientId_photo"
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
        '413':
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/photo" \
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
  "operation": "Upload Citizen Web-Cam Identification Photo",
  "domain": "Patient",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PATIENT-024"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-024",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-024.",
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
- **Relational Database Mutation:** Modifies tables `patients` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-040` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-040` under simulated offline network conditions.

### 6.25 `API-PATIENT-025`: Fetch Citizen Verification Photo

- **API Identifier:** `API-PATIENT-025`
- **HTTP Route:** `GET /api/v1/patients/{patientId}/photo`
- **Functional Purpose:** Retrieve encrypted citizen identification photo for workstation UI display.
- **Product Capability:** `CAPABILITY-010` | **Feature Code:** `FEATURE-010`
- **Primary Actor:** Clinic Staff | **User Persona:** Care Team
- **Required RBAC Role:** `ROLE-016`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:profile:read`
- **ABAC Scoping Rule:** Returns pre-signed URL or base64 data stream.
- **Upstream Traceability:** `SRS-FR-007` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `1000ms`
- **Rate Limiting Policy:** `60 req/min per User`
- **Offline Edge Resilience:** Edge Local Image Cache
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-041`
- **Planned Verification Test Case:** `PLANNED-TEST-API-041`
- **Dependency DAG Edge:** `API-DEP-041`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/{patientId}/photo:
    get:
      summary: "Fetch Citizen Verification Photo"
      tags:
        - "Patient"
      operationId: "get_api_v1_patients_patientId_photo"
      responses:
        '200':
          description: "Successful operation"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardApiResponseEnvelope"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/018e3a20-0001-7000-8000-000000000001/photo" \
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
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-025",
      "domain": "Patient",
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
    "code": "ERR-PATIENT-001",
    "message": "Domain constraint validation failed during execution of API-PATIENT-025.",
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
- **Relational Database Mutation:** Modifies tables `patients` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-041` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-041` under simulated offline network conditions.

### 6.26 `API-PATIENT-026`: Batch Patient UHID Verification

- **API Identifier:** `API-PATIENT-026`
- **HTTP Route:** `POST /api/v1/patients/batch-lookup`
- **Functional Purpose:** Bulk verification of UHID list for municipal immunization drives and school health screenings.
- **Product Capability:** `CAPABILITY-011` | **Feature Code:** `FEATURE-011`
- **Primary Actor:** Public Health Nurse | **User Persona:** Community Coordinator
- **Required RBAC Role:** `ROLE-014`
- **Authentication Requirement:** `Bearer JWT`
- **RBAC Permission Tokens:** `patient:batch:read`
- **ABAC Scoping Rule:** Max 100 UHIDs per batch request.
- **Upstream Traceability:** `SRS-FR-008` | **Workflow:** `WF-002`
- **Container / Component:** `ARCH-CONT-005` / `ARCH-COMP-013`
- **Target Relational Tables:** `patients`
- **Data Security Tier:** `RESTRICTED`
- **Idempotency Guarantee:** Read-Only Idempotent
- **Execution Timeout:** `2500ms`
- **Rate Limiting Policy:** `10 req/min per Nurse`
- **Offline Edge Resilience:** Edge SQLite Local Match
- **Cryptographic WORM Audit Event:** `AUDIT-EVENT-042`
- **Planned Verification Test Case:** `PLANNED-TEST-API-042`
- **Dependency DAG Edge:** `API-DEP-042`

#### Contract OpenAPI Specification
```yaml
# DOCUMENTATION-ONLY OPENAPI
openapi: 3.1.0
paths:
  /api/v1/patients/batch-lookup:
    post:
      summary: "Batch Patient UHID Verification"
      tags:
        - "Patient"
      operationId: "post_api_v1_patients_batch-lookup"
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
                $ref: "#/components/schemas/StandardCollectionEnvelope"
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
  "https://api.nammaclinic.bbmp.gov.in/api/v1/patients/batch-lookup" \
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
  "operation": "Batch Patient UHID Verification",
  "domain": "Patient",
  "timestamp": "2026-09-01T09:30:00.000Z",
  "payload": {
    "referenceId": "018e3a20-0001-7000-8000-000000000001",
    "notes": "Authoritative test payload for API-PATIENT-026"
  }
}
```

#### Successful Response Wire Representation (`HTTP 200`)
```json
// DOCUMENTATION-ONLY EXAMPLE
{
  "data": {
    "id": "018e3a20-0001-7000-8000-000000000001",
    "type": "patient",
    "attributes": {
      "status": "SUCCESS",
      "endpointId": "API-PATIENT-026",
      "domain": "Patient",
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
    "code": "ERR-SYS-006",
    "message": "Domain constraint validation failed during execution of API-PATIENT-026.",
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
- **Relational Database Mutation:** Modifies tables `patients` inside an ACID transaction.
- **WORM Audit Ledger Hook:** Emits append-only record `AUDIT-EVENT-042` linked to previous HMAC SHA-256 block hash.
- **Verification Target:** Validated via automated test case `PLANNED-TEST-API-042` under simulated offline network conditions.

## 7. Domain-Specific Error Code Catalog & Troubleshooting Runbooks

The following standardized error codes are specifically emitted by `Patient` services:

| Error Code ID | HTTP Status | Machine Code | Message Summary | Retryable | Resolution Runbook |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-PATIENT-001** | `HTTP 404` | `PATIENT_NOT_FOUND` | No active patient record matches the provided UHID or identifier. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PATIENT-001. |
| **ERR-PATIENT-002** | `HTTP 409` | `PATIENT_DUPLICATE_DETECTED` | High-confidence duplicate citizen detected (matching phone and phonetic name). | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PATIENT-002. |
| **ERR-PATIENT-003** | `HTTP 400` | `PATIENT_PHONE_INVALID` | Mobile number must be exactly 10 digits complying with Indian numbering plan. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PATIENT-003. |
| **ERR-PATIENT-004** | `HTTP 400` | `PATIENT_DOB_FUTURE` | Date of birth cannot be in the future. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PATIENT-004. |
| **ERR-PATIENT-005** | `HTTP 400` | `PATIENT_WARD_INVALID` | BBMP ward number must be between 1 and 243. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PATIENT-005. |
| **ERR-PATIENT-006** | `HTTP 409` | `PATIENT_ALREADY_MERGED` | Requested patient record has already been merged into a surviving primary profile. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PATIENT-006. |
| **ERR-PATIENT-007** | `HTTP 400` | `PATIENT_MERGE_SAME_RECORD` | Surviving and subsumed patient identifiers cannot be identical. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PATIENT-007. |
| **ERR-PATIENT-008** | `HTTP 403` | `PATIENT_PRIVACY_RESTRICTED` | Access restricted: citizen has revoked consent for general record disclosure. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PATIENT-008. |
| **ERR-PATIENT-009** | `HTTP 400` | `PATIENT_PINCODE_INVALID` | Postal pincode must be valid Bengaluru delivery code (560001..560110). | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PATIENT-009. |
| **ERR-PATIENT-010** | `HTTP 409` | `PATIENT_ABHA_ALREADY_LINKED` | Provided ABHA number is already bound to another registered citizen profile. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PATIENT-010. |
| **ERR-PATIENT-011** | `HTTP 400` | `PATIENT_NAME_MALFORMED` | First name contains illegal control characters, numbers, or exceeds 100 characters. | No | Verify client request format, ensure active session, and inspect audit logs for ERR-PATIENT-011. |
| **ERR-PATIENT-012** | `HTTP 500` | `PATIENT_MPI_SEARCH_TIMEOUT` | Master Patient Index fuzzy phonetic search cluster timed out. | **Yes** | Verify client request format, ensure active session, and inspect audit logs for ERR-PATIENT-012. |

## 8. Offline Edge Operation & Synchronization Mechanics

When WAN connectivity to the central cloud is disrupted, `Patient` operations transition to autonomous edge mode:
1. **Local SQLite WAL Database:** Transactions are committed locally to `/data/namma_clinic_edge.db` on the clinic's Intel N100 mini-server.
2. **Offline Mutation Journal:** Every INSERT, UPDATE, and SOFT_DELETE appends a record to the `offline_mutation_log` table with a local vector clock.
3. **Conflict Resolution Policy:** Upon WAN restoration, the edge sync agent uploads buffered mutations in batches of 100 to `/api/v1/system/sync/batch`. Conflicts are resolved deterministically using Last-Write-Wins (LWW) with microsecond Lamport timestamps, except for clinical records where doctor entries take precedence over clerical updates.
4. **Storage Quotas:** Up to 72 hours of offline operations (approximately 15,000 mutations) can be buffered without storage degradation.

## 9. Security, Data Protection & DPDP Act Compliance

Data protection invariants for `Patient` operations:

| Data Element | Classification | Encryption Standard | Masking Rule | DPDP Act Section | Retention Schedule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Core Entity Record | `RESTRICTED` | AES-256-GCM Column Level | Masked on non-admin UI | Section 8 (Data Security) | 10 Years (Medical Records) |
| Transaction Mutation | INTERNAL | TLS 1.3 in Transit | Zero PII in Gateway Logs | Section 6 (Consent Notice) | 10 Years (Audit Ledger) |
| WORM Audit Log | HIGHLY-RESTRICTED | HMAC SHA-256 Chained | Full Hash Ledger | Section 12 (Citizen Rights) | Permanent (Statutory Archive) |

## 10. Domain Quality Acceptance Criteria (BDD)

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Verify Successful Execution of Register New Citizen Patient Profile
  Given an authenticated staff member with role 'ROLE-019'
  And an active clinical shift rostered in clinic facility '018e3a20-0008-7000-8000-000000000001'
  When the client sends a valid request to /api/v1/patients
  Then the server processes the request within 1500ms
  And returns HTTP 201
  And the response conforms to envelope schema 'PatientProfileResponse'
  And an immutable audit log is appended to 'AUDIT-EVENT-017'
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Reject Unauthorized Call to Register New Citizen Patient Profile
  Given a caller presenting an invalid or expired Bearer token
  And requesting protected resource access
  When the caller transmits a request to /api/v1/patients
  Then the API gateway intercepts the request
  And returns HTTP 401 Unauthorized
  And returns error code 'ERR-AUTH-002' or 'ERR-AUTH-003'
  And rejects access before invoking backend services
```

```gherkin
# DOCUMENTATION-ONLY EXAMPLE
Scenario: Execute Register New Citizen Patient Profile in Autonomous Edge Mode
  Given the clinic workstation has lost WAN connectivity to cloud
  And the local edge mini-server is operational with local SQLite database
  When the staff member executes Register New Citizen Patient Profile
  Then the edge API gateway accepts the request locally
  And returns HTTP 201 within 250ms
  And appends the mutation to the local offline sync journal
  And synchronizes to cloud automatically upon network restoration
```

## 11. Requirements & Database Relational Traceability Matrix

Traceability mapping for all `Patient` endpoints:

| Endpoint ID | Upstream SRS Requirements | Workflow ID | Feature Code | Target Database Tables | Verification Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `API-PATIENT-001` | `SRS-FR-007, SRS-FR-008, BR-002, PRIV-001` | `WF-002` | `FEATURE-010` | `patients, patient_identifiers, patient_contacts, patient_addresses` | `PLANNED-TEST-API-017` |
| `API-PATIENT-002` | `SRS-FR-007, PRIV-001` | `WF-002` | `FEATURE-010` | `patients, patient_identifiers, patient_contacts` | `PLANNED-TEST-API-018` |
| `API-PATIENT-003` | `SRS-FR-008, SRS-NFR-002` | `WF-002` | `FEATURE-011` | `patients, patient_identifiers, patient_contacts` | `PLANNED-TEST-API-019` |
| `API-PATIENT-004` | `SRS-FR-007` | `WF-002` | `FEATURE-010` | `patients, patient_contacts, patient_addresses` | `PLANNED-TEST-API-020` |
| `API-PATIENT-005` | `SRS-FR-008, BR-002` | `WF-002` | `FEATURE-012` | `patients, patient_contacts` | `PLANNED-TEST-API-021` |
| `API-PATIENT-006` | `SRS-FR-008, WF-002` | `WF-002` | `FEATURE-012` | `patients, clinical_encounters, prescriptions, audit_events` | `PLANNED-TEST-API-022` |
| `API-PATIENT-007` | `SRS-FR-055, INT-001, WF-024` | `WF-024` | `FEATURE-013` | `patients, patient_identifiers, abdm_artifacts` | `PLANNED-TEST-API-023` |
| `API-PATIENT-008` | `SRS-FR-055, PRIV-001` | `WF-024` | `FEATURE-013` | `patients, patient_identifiers` | `PLANNED-TEST-API-024` |
| `API-PATIENT-009` | `SRS-FR-014, PRIV-001` | `WF-005` | `FEATURE-014` | `clinical_encounters, prescriptions, lab_orders, referrals` | `PLANNED-TEST-API-025` |
| `API-PATIENT-010` | `PRIV-001, RETENTION-005` | `WF-002` | `FEATURE-015` | `consent_records` | `PLANNED-TEST-API-026` |
| `API-PATIENT-011` | `PRIV-001, DPDP-ACT-2023` | `WF-002` | `FEATURE-015` | `consent_records` | `PLANNED-TEST-API-027` |
| `API-PATIENT-012` | `PRIV-001, DPDP-ACT-2023` | `WF-002` | `FEATURE-015` | `consent_records` | `PLANNED-TEST-API-028` |
| `API-PATIENT-013` | `SECR-004, RETENTION-006` | `WF-020` | `FEATURE-016` | `audit_events` | `PLANNED-TEST-API-029` |
| `API-PATIENT-014` | `SRS-FR-025, RETENTION-013` | `WF-005` | `FEATURE-017` | `ncd_episodes, follow_up_schedules` | `PLANNED-TEST-API-030` |
| `API-PATIENT-015` | `SRS-FR-025` | `WF-005` | `FEATURE-017` | `ncd_episodes` | `PLANNED-TEST-API-031` |
| `API-PATIENT-016` | `SRS-FR-007` | `WF-002` | `FEATURE-010` | `patient_contacts` | `PLANNED-TEST-API-032` |
| `API-PATIENT-017` | `SRS-FR-007` | `WF-002` | `FEATURE-010` | `patient_identifiers` | `PLANNED-TEST-API-033` |
| `API-PATIENT-018` | `SRS-FR-007` | `WF-002` | `FEATURE-010` | `patient_identifiers` | `PLANNED-TEST-API-034` |
| `API-PATIENT-019` | `SRS-FR-007` | `WF-002` | `FEATURE-010` | `patient_identifiers` | `PLANNED-TEST-API-035` |
| `API-PATIENT-020` | `SRS-FR-007, RETENTION-001` | `WF-002` | `FEATURE-018` | `patients, audit_events` | `PLANNED-TEST-API-036` |
| `API-PATIENT-021` | `SRS-FR-014` | `WF-005` | `FEATURE-014` | `clinical_encounters` | `PLANNED-TEST-API-037` |
| `API-PATIENT-022` | `SRS-FR-017` | `WF-006` | `FEATURE-014` | `prescriptions, prescription_items` | `PLANNED-TEST-API-038` |
| `API-PATIENT-023` | `SRS-FR-021` | `WF-008` | `FEATURE-014` | `lab_orders, lab_results` | `PLANNED-TEST-API-039` |
| `API-PATIENT-024` | `SRS-FR-007, PRIV-001` | `WF-002` | `FEATURE-010` | `patients` | `PLANNED-TEST-API-040` |
| `API-PATIENT-025` | `SRS-FR-007` | `WF-002` | `FEATURE-010` | `patients` | `PLANNED-TEST-API-041` |
| `API-PATIENT-026` | `SRS-FR-008` | `WF-002` | `FEATURE-011` | `patients` | `PLANNED-TEST-API-042` |
