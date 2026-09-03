# 🌐 Open APIs for Data Portability & Interoperability Specification
## Namma Clinic Digital Health & Operations Platform
### Anti-Vendor Lock-In Architecture & Bulk Export Protocol (FHIR R4 & NDJSON)
### Document Code: DG-PRT-03 | Version: 1.0 | Date: September 2026

---

## 1. Statutory Mandate & Purpose

In compliance with **Clause 1.5 of the Sovereign Data Ownership Covenant** and the **National Digital Health Blueprint (NDHB)**, the Namma Clinic Platform guarantees **100% data portability**. The Greater Bengaluru Authority (GBA) / BBMP retains the perpetual right to programmatically or manually extract the entirety of municipal healthcare datasets in open, standard, non-proprietary formats without reliance on any proprietary decoding software.

This specification details:
1. **Asynchronous Bulk Data Export APIs** (aligned with the HL7 FHIR Bulk Data Access IG).
2. **Tabular Data Interchange Endpoints** (JSON / NDJSON / CSV streaming).
3. **Cryptographic verification, data packaging, and schema migration packs**.

---

## 2. Asynchronous Bulk Export Protocol Architecture

Exporting multi-gigabyte health datasets across 183+ clinics requires an asynchronous, non-blocking polling mechanism to avoid degrading frontline clinical transaction throughput:

```
[BBMP Authorized Admin / State Health Portal]
                   │
                   ▼  (1) POST /api/v1/export/bulk-request (Bearer JWT + mTLS)
       [API Gateway (Rate Limited)]
                   │
                   ▼  (2) 202 Accepted + Content-Location: /api/v1/export/jobs/{jobId}
         [Job Worker Pool]
                   │
                   ▼  (3) Asynchronous Extract, Transform & Gzip packaging
         [S3 Secure Staging Bucket] (KMS Encrypted)
                   │
                   ▼  (4) GET /api/v1/export/jobs/{jobId} -> 200 OK + Signed Download URLs
[Download Stream (NDJSON / FHIR R4 Bundles)]
```

---

## 3. Core Export API Endpoints

### 3.1 Initiate Asynchronous Bulk Export
* **Endpoint:** `POST /api/v1/portability/export`
* **Security:** `Authorization: Bearer <ADMIN_SERVICE_TOKEN>`, `X-BBMP-Authorization-Cert: <SHA256_CERT>`
* **Request Payload (JSON):**
```json
{
  "exportScope": "ALL_CLINICS",
  "zoneFilter": ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"],
  "dateRange": {
    "startDate": "2026-01-01T00:00:00Z",
    "endDate": "2026-09-01T23:59:59Z"
  },
  "resourceTypes": [
    "Patient",
    "Encounter",
    "Observation",
    "MedicationRequest",
    "MedicationDispense",
    "ServiceRequest",
    "StockLedger"
  ],
  "outputFormat": "application/fhir+ndjson",
  "compression": "gzip"
}
```
* **Response:** `HTTP 202 Accepted`
  * Header: `Content-Location: https://api.nammaclinic.bbmp.gov.in/api/v1/portability/jobs/job_99812_exp`
  * Header: `Retry-After: 120`

### 3.2 Poll Job Status & Retrieve Manifest
* **Endpoint:** `GET /api/v1/portability/jobs/{jobId}`
* **Response (When In Progress):** `HTTP 202 Accepted` (Includes `X-Progress: 64% completed`).
* **Response (When Completed):** `HTTP 200 OK`
```json
{
  "transactionTime": "2026-09-02T18:00:00Z",
  "requestUrl": "/api/v1/portability/export",
  "requiresAccessToken": true,
  "output": [
    {
      "type": "Patient",
      "url": "https://storage.nammaclinic.bbmp.gov.in/exports/job_99812/Patient.ndjson.gz",
      "count": 412500,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "type": "Encounter",
      "url": "https://storage.nammaclinic.bbmp.gov.in/exports/job_99812/Encounter.ndjson.gz",
      "count": 589000,
      "sha256": "f8a7c21245e..."
    },
    {
      "type": "Observation",
      "url": "https://storage.nammaclinic.bbmp.gov.in/exports/job_99812/Observation.ndjson.gz",
      "count": 1420000,
      "sha256": "a7b8c9d0e1..."
    }
  ],
  "error": []
}
```

---

## 4. Single-Patient Portability (Citizen Right to Port)

Under the DPDP Act 2023, citizens may demand an immediate export of their complete health record:
* **Endpoint:** `GET /api/v1/portability/patients/{patientId}/bundle`
* **Response:** Complete standalone **FHIR R4 Document Bundle** (JSON format) containing all historical encounters, vitals, prescriptions, and lab investigations:

```json
{
  "resourceType": "Bundle",
  "id": "bundle-nc-2026-001",
  "type": "document",
  "timestamp": "2026-09-02T18:30:00Z",
  "entry": [
    {
      "fullUrl": "urn:uuid:p1",
      "resource": {
        "resourceType": "Patient",
        "id": "p1",
        "identifier": [
          {"system": "https://healthid.abdm.gov.in", "value": "12-3456-7890-0001"},
          {"system": "https://nammaclinic.bbmp.gov.in/patient-id", "value": "NC-2026-001"}
        ],
        "name": [{"text": "Ramesh Kumar"}],
        "gender": "male",
        "birthDate": "1974-05-12"
      }
    },
    {
      "fullUrl": "urn:uuid:obs1",
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {"coding": [{"system": "http://loinc.org", "code": "8480-6", "display": "Systolic blood pressure"}]},
        "valueQuantity": {"value": 158, "unit": "mmHg", "system": "http://unitsofmeasure.org"}
      }
    }
  ]
}
```

---

## 5. Direct Database SQL Dump Extract Protocol

In addition to RESTful APIs, the hosting platform provides an automated weekly logical SQL dump:
1. **Tooling:** Native `pg_dump` utility with zero lock contention (`--no-owner --no-privileges -Fc`).
2. **Delivery Mechanism:** Direct delivery to BBMP's designated S3/KSDC cold-storage bucket encrypted using BBMP's GPG public key.
3. **Verification:** Automatic monthly test restore executed on an isolated sandbox VM to verify schema validity and data restoration integrity.
