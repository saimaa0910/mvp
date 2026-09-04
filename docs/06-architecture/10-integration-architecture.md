# 🌐 Architecture Document 10: Enterprise Integration & Interoperability Specification
## Namma Clinic Digital Health & Operations Platform
### Greater Bengaluru Authority (GBA) / BBMP Health Department
**Standard:** ABDM (M1/M2/M3) / FHIR R4 / HL7 / REST / EDI | **Status:** APPROVED BASELINE | **Code:** `ARCH-INT-10`

---

## 01. Document Overview & Integration Architectural Philosophy
This document establishes the enterprise integration architecture, interoperability standards, national health grid bridges, and external system connector specifications for the Namma Clinic Digital Health & Operations Platform. The system functions as a critical municipal node within India's **Ayushman Bharat Digital Mission (ABDM)** ecosystem while seamlessly interfacing with state drug logistics warehouses (KDLWS), emergency ambulance CAD systems (GVK-EMRI 108), national disease surveillance programs (IDSP/IHIP), and municipal civic portals.

### 01.1 Core Integration Invariants & Design Principles
1. **HL7 FHIR R4 Standard Compliance:** All clinical encounter summaries, diagnostic lab reports, and medication prescriptions shared externally must conform strictly to the standard FHIR Release 4 Indian Core Profiles published by the National Health Authority (NHA).
2. **ABDM Milestones 1, 2, and 3 Certification:** The platform implements end-to-end integration for Milestone 1 (ABHA creation and verification), Milestone 2 (HIP health record publishing), and Milestone 3 (HIU consent-driven record viewing).
3. **Asynchronous Circuit Breaking & Resilience:** All external integration endpoints are mediated by circuit breakers (Resilience4j / Envoy) with automated fallbacks, ensuring that external third-party outages never block frontline clinic operations.
4. **Zero Plaintext Sensitive Data in Transit:** All external communication requires TLS 1.3 with mutual certificate authentication (mTLS) for sovereign gateways.
5. **Strict Rate Limiting & Egress Throttling:** Egress traffic is token-bucket throttled to respect statutory gateway quotas and prevent DDoS penalties.
6. **Cryptographic Payload Signing & Audit:** All external data transmissions are signed with BBMP's X.509 private certificate and logged into the WORM audit trail.

## 02. ABDM National Health Grid Interoperability Architecture
Exhaustive technical specifications for the three statutory ABDM implementation milestones:

### 02.1 Milestone 1 (M1): ABHA Issuance, Verification & Linking
1. **Citizen ABHA Onboarding Workflows:**
   - **Aadhaar OTP Flow:** Frontline nurse enters citizen Aadhaar number -> calls `POST /v1/registration/aadhaar/generateOtp` -> citizen provides 6-digit OTP -> system verifies via `POST /v1/registration/aadhaar/verifyOTP` -> receives signed ABHA profile JSON.
   - **Mobile OTP Flow:** For citizens without Aadhaar linkage, uses mobile verification via `POST /v1/registration/mobile/generateOtp`.
   - **Biometric Fingerprint Authentication:** For illiterate or senior citizens, USB optical fingerprint scanner captures ISO 19794-2 biometric template encapsulated in encrypted PID block sent to UIDAI gateway.
2. **ABHA Verification & QR Scanning:**
   - Frontline kiosk scans citizen physical ABHA card QR code containing signed demographic payload.
   - System parses demographic fields, performs phonetic deduplication against local database, and creates or binds clinic patient profile.
3. **Voluntary Adoption Safeguard:** In strict compliance with national policy, ABHA linking is voluntary; citizens declining ABHA are issued sovereign municipal IDs without care denial.

### 02.2 Milestone 2 (M2): Health Information Provider (HIP) Publishing
1. **Care Context Discovery Protocol:**
   - When citizen links clinic records in their ABHA Personal Health Record (PHR) app, ABDM gateway sends `POST /v0.5/care-contexts/discover` to BBMP HIP service.
   - HIP service validates citizen phone/ABHA against `patients` table and returns registered care contexts (e.g. `CARE-CLN-042-ENC-2026-0904`).
2. **Care Context Linking & Token Exchange:**
   - ABDM issues linking token; HIP validates SMS OTP sent to citizen phone and confirms link via `POST /v0.5/links/link/confirm`.
3. **Encrypted FHIR Bundle Data Push:**
   - Upon receiving valid consent notification `POST /v0.5/consents/hip/notify`, HIP assembles FHIR R4 Bundle, encrypts it using receiver's Diffie-Hellman ephemeral public key, and delivers payload to ABDM data repository.

### 02.3 Milestone 3 (M3): Health Information User (HIU) Consent-Driven Fetch
1. **Digital Consent Artifact Generation:**
   - Medical Officer initiates consent request for historical hospital records: `POST /v0.5/consent-requests/init` with purpose code `CARETREAT`.
   - Citizen receives push notification on mobile ABHA app and approves consent.
2. **Encrypted Health Record Retrieval:**
   - HIU service queries ABDM gateway `POST /v0.5/health-information/hiu/request`.
   - Remote hospital HIP pushes encrypted FHIR data.
   - HIU decrypts bundle using Curve25519 private key in memory, renders longitudinal clinical history in doctor console, and securely discards decrypted plaintext upon encounter seal.

## 03. Canonical FHIR R4 Resource Profiles & JSON Schemas
Exhaustive specifications and production-grade JSON payload blueprints for the 10 primary FHIR R4 clinical resources:

### 03.1 FHIR R4 Resource Profile: `Patient`
- **Resource Type:** `Patient`
- **Profile Description:** Demographic profile conforming to NRCES Indian Core Patient Profile.
- **Authoritative Profile URI:** `https://nrces.in/ndhm/fhir/r4/StructureDefinition/Patient`

#### 03.1.1 Canonical JSON Schema Blueprint
```json
{
  "resourceType": "Patient",
  "id": "namma-patient-018f3a5b-7c12",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2026-09-04T11:00:00.000Z",
    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Patient"]
  },
  "identifier": [
    {
      "type": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "MR", "display": "Medical Record Number" }] },
      "system": "https://namma.bbmp.gov.in/mrn",
      "value": "BBMP-MRN-2026-004291"
    },
    {
      "type": { "coding": [{ "system": "https://nrces.in/ndhm/fhir/r4/CodeSystem/ndhm-identifier-type-code", "code": "ABHA", "display": "Ayushman Bharat Health Account" }] },
      "system": "https://healthid.ndhm.gov.in",
      "value": "91-4291-8842-1092"
    }
  ],
  "active": true,
  "name": [{ "use": "official", "text": "Ramesh Gowda", "family": "Gowda", "given": ["Ramesh"] }],
  "telecom": [{ "system": "phone", "value": "+919845012345", "use": "mobile" }],
  "gender": "male",
  "birthDate": "1982-06-15",
  "address": [{ "use": "home", "line": ["#42, 3rd Cross, Malleshwaram"], "city": "Bengaluru", "state": "Karnataka", "postalCode": "560003", "country": "IN" }]
}
```

#### 03.1.2 Field Mappings to Internal Relational Tables
1. Maps internal relational columns from `ARCH-DATA-001` to standard FHIR elements.
2. Translates local codes to standard terminologies: SNOMED CT, LOINC, and ICD-10.
3. Enforces presence of mandatory NRCES Indian Core Profile extension elements.

---

### 03.2 FHIR R4 Resource Profile: `Encounter`
- **Resource Type:** `Encounter`
- **Profile Description:** Outpatient clinical consultation episode at Namma Clinic.
- **Authoritative Profile URI:** `https://nrces.in/ndhm/fhir/r4/StructureDefinition/Encounter`

#### 03.2.1 Canonical JSON Schema Blueprint
```json
{
  "resourceType": "Encounter",
  "id": "namma-enc-018f3a5b-7c12",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2026-09-04T11:15:00.000Z",
    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Encounter"]
  },
  "status": "finished",
  "class": { "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "AMB", "display": "ambulatory" },
  "type": [{ "coding": [{ "system": "http://snomed.info/sct", "code": "3391000179108", "display": "General medical examination" }] }],
  "subject": { "reference": "Patient/namma-patient-018f3a5b-7c12", "display": "Ramesh Gowda" },
  "serviceProvider": { "identifier": { "system": "https://facility.ndhm.gov.in", "value": "IN-KA-BBMP-CLN-042" }, "display": "Namma Clinic Malleshwaram" },
  "period": { "start": "2026-09-04T11:00:00.000Z", "end": "2026-09-04T11:20:00.000Z" }
}
```

#### 03.2.2 Field Mappings to Internal Relational Tables
1. Maps internal relational columns from `ARCH-DATA-002` to standard FHIR elements.
2. Translates local codes to standard terminologies: SNOMED CT, LOINC, and ICD-10.
3. Enforces presence of mandatory NRCES Indian Core Profile extension elements.

---

### 03.3 FHIR R4 Resource Profile: `Condition`
- **Resource Type:** `Condition`
- **Profile Description:** Clinical diagnostic assessment coded in SNOMED CT and ICD-10.
- **Authoritative Profile URI:** `https://nrces.in/ndhm/fhir/r4/StructureDefinition/Condition`

#### 03.3.1 Canonical JSON Schema Blueprint
```json
{
  "resourceType": "Condition",
  "id": "namma-cond-018f3a5b-7c12",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2026-09-04T11:10:00.000Z",
    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Condition"]
  },
  "clinicalStatus": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active", "display": "Active" }] },
  "verificationStatus": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed", "display": "Confirmed" }] },
  "category": [{ "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/condition-category", "code": "encounter-diagnosis", "display": "Encounter Diagnosis" }] }],
  "code": {
    "coding": [
      { "system": "http://snomed.info/sct", "code": "38341003", "display": "Hypertensive disorder" },
      { "system": "http://hl7.org/fhir/sid/icd-10", "code": "I10", "display": "Essential (primary) hypertension" }
    ],
    "text": "Essential Primary Hypertension"
  },
  "subject": { "reference": "Patient/namma-patient-018f3a5b-7c12" },
  "encounter": { "reference": "Encounter/namma-enc-018f3a5b-7c12" },
  "recordedDate": "2026-09-04T11:10:00.000Z"
}
```

#### 03.3.2 Field Mappings to Internal Relational Tables
1. Maps internal relational columns from `ARCH-DATA-003` to standard FHIR elements.
2. Translates local codes to standard terminologies: SNOMED CT, LOINC, and ICD-10.
3. Enforces presence of mandatory NRCES Indian Core Profile extension elements.

---

### 03.4 FHIR R4 Resource Profile: `MedicationRequest`
- **Resource Type:** `MedicationRequest`
- **Profile Description:** Electronic prescription authorized by licensed Medical Officer.
- **Authoritative Profile URI:** `https://nrces.in/ndhm/fhir/r4/StructureDefinition/MedicationRequest`

#### 03.4.1 Canonical JSON Schema Blueprint
```json
{
  "resourceType": "MedicationRequest",
  "id": "namma-medrx-018f3a5b-7c12",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2026-09-04T11:12:00.000Z",
    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/MedicationRequest"]
  },
  "status": "active",
  "intent": "order",
  "medicationCodeableConcept": {
    "coding": [
      { "system": "http://snomed.info/sct", "code": "318444007", "display": "Amlodipine 5 mg oral tablet" }
    ],
    "text": "Tab Amlodipine 5mg"
  },
  "subject": { "reference": "Patient/namma-patient-018f3a5b-7c12" },
  "encounter": { "reference": "Encounter/namma-enc-018f3a5b-7c12" },
  "authoredOn": "2026-09-04T11:12:00.000Z",
  "requester": { "identifier": { "system": "https://kmc.karnataka.gov.in", "value": "KMC-DOC-44821" }, "display": "Dr. Ananya Rao, MBBS" },
  "dosageInstruction": [
    {
      "text": "One tablet once daily in the morning after food for 30 days (ಬೆಳಿಗ್ಗೆ ಊಟದ ನಂತರ 1 ಮಾತ್ರೆ)",
      "timing": { "repeat": { "frequency": 1, "period": 1, "periodUnit": "d" } },
      "route": { "coding": [{ "system": "http://snomed.info/sct", "code": "260548002", "display": "Oral" }] },
      "doseAndRate": [{ "doseQuantity": { "value": 5, "unit": "mg", "system": "http://unitsofmeasure.org", "code": "mg" } }]
    }
  ]
}
```

#### 03.4.2 Field Mappings to Internal Relational Tables
1. Maps internal relational columns from `ARCH-DATA-004` to standard FHIR elements.
2. Translates local codes to standard terminologies: SNOMED CT, LOINC, and ICD-10.
3. Enforces presence of mandatory NRCES Indian Core Profile extension elements.

---

### 03.5 FHIR R4 Resource Profile: `Observation`
- **Resource Type:** `Observation`
- **Profile Description:** Nursing vital signs and clinical measurements (MEWS / Blood Pressure).
- **Authoritative Profile URI:** `https://nrces.in/ndhm/fhir/r4/StructureDefinition/Observation`

#### 03.5.1 Canonical JSON Schema Blueprint
```json
{
  "resourceType": "Observation",
  "id": "namma-obs-bp-018f3a5b-7c12",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2026-09-04T10:45:00.000Z",
    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Observation"]
  },
  "status": "final",
  "category": [{ "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs", "display": "Vital Signs" }] }],
  "code": { "coding": [{ "system": "http://loinc.org", "code": "85354-9", "display": "Blood pressure panel with all children optional" }] },
  "subject": { "reference": "Patient/namma-patient-018f3a5b-7c12" },
  "effectiveDateTime": "2026-09-04T10:45:00.000Z",
  "performer": [{ "display": "Staff Nurse Bhavya S" }],
  "component": [
    {
      "code": { "coding": [{ "system": "http://loinc.org", "code": "8480-6", "display": "Systolic blood pressure" }] },
      "valueQuantity": { "value": 142, "unit": "mmHg", "system": "http://unitsofmeasure.org", "code": "mm[Hg]" }
    },
    {
      "code": { "coding": [{ "system": "http://loinc.org", "code": "8462-4", "display": "Diastolic blood pressure" }] },
      "valueQuantity": { "value": 92, "unit": "mmHg", "system": "http://unitsofmeasure.org", "code": "mm[Hg]" }
    }
  ]
}
```

#### 03.5.2 Field Mappings to Internal Relational Tables
1. Maps internal relational columns from `ARCH-DATA-005` to standard FHIR elements.
2. Translates local codes to standard terminologies: SNOMED CT, LOINC, and ICD-10.
3. Enforces presence of mandatory NRCES Indian Core Profile extension elements.

---

### 03.6 FHIR R4 Resource Profile: `DiagnosticReport`
- **Resource Type:** `DiagnosticReport`
- **Profile Description:** Point-of-care laboratory investigation panel summary (58 tests).
- **Authoritative Profile URI:** `https://nrces.in/ndhm/fhir/r4/StructureDefinition/DiagnosticReport`

#### 03.6.1 Canonical JSON Schema Blueprint
```json
{
  "resourceType": "DiagnosticReport",
  "id": "namma-diag-018f3a5b-7c12",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2026-09-04T11:05:00.000Z",
    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/DiagnosticReport"]
  },
  "status": "final",
  "category": [{ "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/v2-0074", "code": "LAB", "display": "Laboratory" }] }],
  "code": { "coding": [{ "system": "http://loinc.org", "code": "2345-7", "display": "Glucose [Mass/volume] in Blood" }], "text": "Random Blood Sugar (RBS)" },
  "subject": { "reference": "Patient/namma-patient-018f3a5b-7c12" },
  "effectiveDateTime": "2026-09-04T10:55:00.000Z",
  "issued": "2026-09-04T11:05:00.000Z",
  "performer": [{ "display": "Lab Tech Manjunath K" }],
  "conclusion": "Mild postprandial hyperglycemia. Value: 168 mg/dL."
}
```

#### 03.6.2 Field Mappings to Internal Relational Tables
1. Maps internal relational columns from `ARCH-DATA-006` to standard FHIR elements.
2. Translates local codes to standard terminologies: SNOMED CT, LOINC, and ICD-10.
3. Enforces presence of mandatory NRCES Indian Core Profile extension elements.

---

### 03.7 FHIR R4 Resource Profile: `AllergyIntolerance`
- **Resource Type:** `AllergyIntolerance`
- **Profile Description:** Patient clinical drug and food allergy record.
- **Authoritative Profile URI:** `https://nrces.in/ndhm/fhir/r4/StructureDefinition/AllergyIntolerance`

#### 03.7.1 Canonical JSON Schema Blueprint
```json
{
  "resourceType": "AllergyIntolerance",
  "id": "namma-allergy-018f3a5b-7c12",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2026-09-04T10:30:00.000Z",
    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/AllergyIntolerance"]
  },
  "clinicalStatus": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical", "code": "active", "display": "Active" }] },
  "verificationStatus": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification", "code": "confirmed", "display": "Confirmed" }] },
  "type": "allergy",
  "category": ["medication"],
  "criticality": "high",
  "code": {
    "coding": [{ "system": "http://snomed.info/sct", "code": "373270004", "display": "Substance with penicillin structure and antibacterial mechanism of action" }],
    "text": "Penicillin"
  },
  "patient": { "reference": "Patient/namma-patient-018f3a5b-7c12" },
  "recordedDate": "2026-09-04T10:30:00.000Z"
}
```

#### 03.7.2 Field Mappings to Internal Relational Tables
1. Maps internal relational columns from `ARCH-DATA-007` to standard FHIR elements.
2. Translates local codes to standard terminologies: SNOMED CT, LOINC, and ICD-10.
3. Enforces presence of mandatory NRCES Indian Core Profile extension elements.

---

### 03.8 FHIR R4 Resource Profile: `Immunization`
- **Resource Type:** `Immunization`
- **Profile Description:** Childhood and adult vaccination delivery record.
- **Authoritative Profile URI:** `https://nrces.in/ndhm/fhir/r4/StructureDefinition/Immunization`

#### 03.8.1 Canonical JSON Schema Blueprint
```json
{
  "resourceType": "Immunization",
  "id": "namma-imm-018f3a5b-7c12",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2026-09-04T10:35:00.000Z",
    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Immunization"]
  },
  "status": "completed",
  "vaccineCode": {
    "coding": [{ "system": "http://hl7.org/fhir/sid/cvx", "code": "03", "display": "MMR" }],
    "text": "Measles, Mumps, Rubella Vaccine"
  },
  "patient": { "reference": "Patient/namma-patient-018f3a5b-7c12" },
  "occurrenceDateTime": "2026-09-04T10:35:00.000Z",
  "primarySource": true,
  "lotNumber": "MMR-KA-2026-991",
  "expirationDate": "2027-08-31"
}
```

#### 03.8.2 Field Mappings to Internal Relational Tables
1. Maps internal relational columns from `ARCH-DATA-008` to standard FHIR elements.
2. Translates local codes to standard terminologies: SNOMED CT, LOINC, and ICD-10.
3. Enforces presence of mandatory NRCES Indian Core Profile extension elements.

---

### 03.9 FHIR R4 Resource Profile: `DocumentReference`
- **Resource Type:** `DocumentReference`
- **Profile Description:** Clinical summary PDF and thermal e-prescription artifact.
- **Authoritative Profile URI:** `https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentReference`

#### 03.9.1 Canonical JSON Schema Blueprint
```json
{
  "resourceType": "DocumentReference",
  "id": "namma-doc-018f3a5b-7c12",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2026-09-04T11:20:00.000Z",
    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentReference"]
  },
  "status": "current",
  "type": { "coding": [{ "system": "http://snomed.info/sct", "code": "371530004", "display": "Clinical consultation report" }] },
  "subject": { "reference": "Patient/namma-patient-018f3a5b-7c12" },
  "date": "2026-09-04T11:20:00.000Z",
  "content": [{
    "attachment": {
      "contentType": "application/pdf",
      "language": "kn-IN",
      "url": "https://namma.bbmp.gov.in/docs/enc-018f3a5b.pdf",
      "title": "Bilingual Clinical Consultation Summary"
    }
  }]
}
```

#### 03.9.2 Field Mappings to Internal Relational Tables
1. Maps internal relational columns from `ARCH-DATA-009` to standard FHIR elements.
2. Translates local codes to standard terminologies: SNOMED CT, LOINC, and ICD-10.
3. Enforces presence of mandatory NRCES Indian Core Profile extension elements.

---

### 03.10 FHIR R4 Resource Profile: `ServiceRequest`
- **Resource Type:** `ServiceRequest`
- **Profile Description:** Secondary hospital referral and specialist tele-consultation request.
- **Authoritative Profile URI:** `https://nrces.in/ndhm/fhir/r4/StructureDefinition/ServiceRequest`

#### 03.10.1 Canonical JSON Schema Blueprint
```json
{
  "resourceType": "ServiceRequest",
  "id": "namma-sr-018f3a5b-7c12",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2026-09-04T11:22:00.000Z",
    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/ServiceRequest"]
  },
  "status": "active",
  "intent": "order",
  "priority": "urgent",
  "code": { "coding": [{ "system": "http://snomed.info/sct", "code": "306206005", "display": "Referral to cardiology service" }] },
  "subject": { "reference": "Patient/namma-patient-018f3a5b-7c12" },
  "authoredOn": "2026-09-04T11:22:00.000Z"
}
```

#### 03.10.2 Field Mappings to Internal Relational Tables
1. Maps internal relational columns from `ARCH-DATA-010` to standard FHIR elements.
2. Translates local codes to standard terminologies: SNOMED CT, LOINC, and ICD-10.
3. Enforces presence of mandatory NRCES Indian Core Profile extension elements.

---

### 03.11 FHIR R4 Resource Profile: `CarePlan`
- **Resource Type:** `CarePlan`
- **Profile Description:** Chronic disease management care plan for hypertension and diabetes.
- **Authoritative Profile URI:** `https://nrces.in/ndhm/fhir/r4/StructureDefinition/CarePlan`

#### 03.11.1 Canonical JSON Schema Blueprint
```json
{
  "resourceType": "CarePlan",
  "id": "namma-cp-018f3a5b-7c12",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2026-09-04T11:25:00.000Z",
    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/CarePlan"]
  },
  "status": "active",
  "intent": "plan",
  "title": "Hypertension Stage 1 Management Plan",
  "description": "Monthly blood pressure monitoring, dietary sodium reduction, and daily Amlodipine 5mg.",
  "subject": { "reference": "Patient/namma-patient-018f3a5b-7c12" },
  "period": { "start": "2026-09-04", "end": "2027-09-04" },
  "author": { "display": "Dr. Ananya Rao, MBBS" }
}
```

#### 03.11.2 Field Mappings to Internal Relational Tables
1. Maps internal relational columns from `ARCH-DATA-011` to standard FHIR elements.
2. Translates local codes to standard terminologies: SNOMED CT, LOINC, and ICD-10.
3. Enforces presence of mandatory NRCES Indian Core Profile extension elements.

---

### 03.12 FHIR R4 Resource Profile: `Practitioner`
- **Resource Type:** `Practitioner`
- **Profile Description:** Healthcare provider clinical credential and council registration.
- **Authoritative Profile URI:** `https://nrces.in/ndhm/fhir/r4/StructureDefinition/Practitioner`

#### 03.12.1 Canonical JSON Schema Blueprint
```json
{
  "resourceType": "Practitioner",
  "id": "namma-prac-018f3a5b-7c12",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2026-09-04T08:00:00.000Z",
    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Practitioner"]
  },
  "identifier": [
    {
      "type": { "coding": [{ "system": "https://nrces.in/ndhm/fhir/r4/CodeSystem/ndhm-identifier-type-code", "code": "HPR", "display": "Healthcare Professional Registry" }] },
      "system": "https://hpr.ndhm.gov.in",
      "value": "91-4482-1092-4411"
    }
  ],
  "name": [{ "text": "Dr. Ananya Rao", "family": "Rao", "given": ["Ananya"], "prefix": ["Dr."] }],
  "qualification": [{
    "code": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/v2-0360", "code": "MD", "display": "Doctor of Medicine" }] },
    "issuer": { "display": "Karnataka Medical Council (KMC)" }
  }]
}
```

#### 03.12.2 Field Mappings to Internal Relational Tables
1. Maps internal relational columns from `ARCH-DATA-012` to standard FHIR elements.
2. Translates local codes to standard terminologies: SNOMED CT, LOINC, and ICD-10.
3. Enforces presence of mandatory NRCES Indian Core Profile extension elements.

---

## 04. Exhaustive Technical Specifications for All 16 External Systems
Complete architectural profiles, interface endpoints, security controls, and resilience rules across all 16 external integration systems:

### 04.01 External Connector Specification: `EXT-001` (ABDM National Health Gateway)
- **System Identifier:** `EXT-001`
- **External Entity Name:** ABDM National Health Gateway
- **Governing Agency:** National Health Authority (NHA)
- **Network Transport Protocol:** REST / HTTPS / FHIR R4
- **Payload Data Format:** JSON / FHIR Bundle
- **Permitted Rate Limit:** 100 req/min
- **Security Trust Boundary:** `National DMZ`
- **Outage Fallback Mode:** Asynchronous retry queue

#### 04.01.1 Technical Integration Endpoint Contracts
```typescript
export interface IABDMNationalHealthGatewayConnector {
  transmit(payload: ABDMNationalHealthGatewayRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<ABDMNationalHealthGatewayStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class ABDMNationalHealthGatewayRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class ABDMNationalHealthGatewayStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.01.2 Data Transformation & Mapping Pipeline
```typescript
export class ABDMNationalHealthGatewayPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): ABDMNationalHealthGatewayRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.01.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.01.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Asynchronous retry queue`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_001`

#### 04.01.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.02 External Connector Specification: `EXT-002` (Karnataka Central Drug Warehouse (KDLWS))
- **System Identifier:** `EXT-002`
- **External Entity Name:** Karnataka Central Drug Warehouse (KDLWS)
- **Governing Agency:** State Health Department
- **Network Transport Protocol:** REST / HTTPS / EDI
- **Payload Data Format:** JSON / EDIFACT
- **Permitted Rate Limit:** 30 req/min
- **Security Trust Boundary:** `State Intranet`
- **Outage Fallback Mode:** Local indent cache

#### 04.02.1 Technical Integration Endpoint Contracts
```typescript
export interface IKarnatakaCentralDrugWarehouseKDLWSConnector {
  transmit(payload: KarnatakaCentralDrugWarehouseKDLWSRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<KarnatakaCentralDrugWarehouseKDLWSStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class KarnatakaCentralDrugWarehouseKDLWSRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class KarnatakaCentralDrugWarehouseKDLWSStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.02.2 Data Transformation & Mapping Pipeline
```typescript
export class KarnatakaCentralDrugWarehouseKDLWSPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): KarnatakaCentralDrugWarehouseKDLWSRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.02.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.02.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Local indent cache`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_002`

#### 04.02.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.03 External Connector Specification: `EXT-003` (GVK-EMRI 108 Emergency Ambulance Dispatch)
- **System Identifier:** `EXT-003`
- **External Entity Name:** GVK-EMRI 108 Emergency Ambulance Dispatch
- **Governing Agency:** Emergency Management Research Institute
- **Network Transport Protocol:** REST / HTTPS
- **Payload Data Format:** JSON / CAD Event
- **Permitted Rate Limit:** 120 req/min
- **Security Trust Boundary:** `Emergency Gateway`
- **Outage Fallback Mode:** Manual phone dispatch escalation

#### 04.03.1 Technical Integration Endpoint Contracts
```typescript
export interface IGVKEMRI108EmergencyAmbulanceDispatchConnector {
  transmit(payload: GVKEMRI108EmergencyAmbulanceDispatchRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<GVKEMRI108EmergencyAmbulanceDispatchStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class GVKEMRI108EmergencyAmbulanceDispatchRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class GVKEMRI108EmergencyAmbulanceDispatchStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.03.2 Data Transformation & Mapping Pipeline
```typescript
export class GVKEMRI108EmergencyAmbulanceDispatchPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): GVKEMRI108EmergencyAmbulanceDispatchRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.03.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.03.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Manual phone dispatch escalation`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_003`

#### 04.03.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.04 External Connector Specification: `EXT-004` (Karnataka State SMS Gateway (KSSD))
- **System Identifier:** `EXT-004`
- **External Entity Name:** Karnataka State SMS Gateway (KSSD)
- **Governing Agency:** Centre for e-Governance (CeG)
- **Network Transport Protocol:** HTTPS POST API
- **Payload Data Format:** JSON / DLT Template
- **Permitted Rate Limit:** 500 req/sec
- **Security Trust Boundary:** `State Gateway`
- **Outage Fallback Mode:** Message buffer in Redis BullMQ

#### 04.04.1 Technical Integration Endpoint Contracts
```typescript
export interface IKarnatakaStateSMSGatewayKSSDConnector {
  transmit(payload: KarnatakaStateSMSGatewayKSSDRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<KarnatakaStateSMSGatewayKSSDStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class KarnatakaStateSMSGatewayKSSDRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class KarnatakaStateSMSGatewayKSSDStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.04.2 Data Transformation & Mapping Pipeline
```typescript
export class KarnatakaStateSMSGatewayKSSDPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): KarnatakaStateSMSGatewayKSSDRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.04.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.04.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Message buffer in Redis BullMQ`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_004`

#### 04.04.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.05 External Connector Specification: `EXT-005` (Integrated Disease Surveillance Program (IDSP/IHIP))
- **System Identifier:** `EXT-005`
- **External Entity Name:** Integrated Disease Surveillance Program (IDSP/IHIP)
- **Governing Agency:** National Centre for Disease Control (NCDC)
- **Network Transport Protocol:** REST / HTTPS
- **Payload Data Format:** JSON / CSV Format
- **Permitted Rate Limit:** 50 req/min
- **Security Trust Boundary:** `National Health Mesh`
- **Outage Fallback Mode:** Daily batch retry

#### 04.05.1 Technical Integration Endpoint Contracts
```typescript
export interface IIntegratedDiseaseSurveillanceProgramIDSPIHIPConnector {
  transmit(payload: IntegratedDiseaseSurveillanceProgramIDSPIHIPRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<IntegratedDiseaseSurveillanceProgramIDSPIHIPStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class IntegratedDiseaseSurveillanceProgramIDSPIHIPRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class IntegratedDiseaseSurveillanceProgramIDSPIHIPStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.05.2 Data Transformation & Mapping Pipeline
```typescript
export class IntegratedDiseaseSurveillanceProgramIDSPIHIPPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): IntegratedDiseaseSurveillanceProgramIDSPIHIPRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.05.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.05.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Daily batch retry`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_005`

#### 04.05.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.06 External Connector Specification: `EXT-006` (BBMP Citizen Health Portal)
- **System Identifier:** `EXT-006`
- **External Entity Name:** BBMP Citizen Health Portal
- **Governing Agency:** Bruhat Bengaluru Mahanagara Palike
- **Network Transport Protocol:** REST / HTTPS / OAuth2
- **Payload Data Format:** JSON
- **Permitted Rate Limit:** 200 req/min
- **Security Trust Boundary:** `Municipal Cloud`
- **Outage Fallback Mode:** Cached appointment slots

#### 04.06.1 Technical Integration Endpoint Contracts
```typescript
export interface IBBMPCitizenHealthPortalConnector {
  transmit(payload: BBMPCitizenHealthPortalRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<BBMPCitizenHealthPortalStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class BBMPCitizenHealthPortalRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class BBMPCitizenHealthPortalStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.06.2 Data Transformation & Mapping Pipeline
```typescript
export class BBMPCitizenHealthPortalPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): BBMPCitizenHealthPortalRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.06.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.06.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Cached appointment slots`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_006`

#### 04.06.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.07 External Connector Specification: `EXT-007` (National NCD Portal)
- **System Identifier:** `EXT-007`
- **External Entity Name:** National NCD Portal
- **Governing Agency:** Ministry of Health and Family Welfare (MoHFW)
- **Network Transport Protocol:** REST / HTTPS
- **Payload Data Format:** JSON / FHIR
- **Permitted Rate Limit:** 60 req/min
- **Security Trust Boundary:** `National Portal`
- **Outage Fallback Mode:** Offline NCD queue sync

#### 04.07.1 Technical Integration Endpoint Contracts
```typescript
export interface INationalNCDPortalConnector {
  transmit(payload: NationalNCDPortalRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<NationalNCDPortalStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class NationalNCDPortalRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class NationalNCDPortalStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.07.2 Data Transformation & Mapping Pipeline
```typescript
export class NationalNCDPortalPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): NationalNCDPortalRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.07.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.07.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Offline NCD queue sync`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_007`

#### 04.07.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.08 External Connector Specification: `EXT-008` (Nikshay Portal (National TB Elimination))
- **System Identifier:** `EXT-008`
- **External Entity Name:** Nikshay Portal (National TB Elimination)
- **Governing Agency:** Central TB Division (CTD)
- **Network Transport Protocol:** REST / HTTPS
- **Payload Data Format:** JSON
- **Permitted Rate Limit:** 60 req/min
- **Security Trust Boundary:** `National Health Mesh`
- **Outage Fallback Mode:** Presumptive TB case queue

#### 04.08.1 Technical Integration Endpoint Contracts
```typescript
export interface INikshayPortalNationalTBEliminationConnector {
  transmit(payload: NikshayPortalNationalTBEliminationRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<NikshayPortalNationalTBEliminationStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class NikshayPortalNationalTBEliminationRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class NikshayPortalNationalTBEliminationStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.08.2 Data Transformation & Mapping Pipeline
```typescript
export class NikshayPortalNationalTBEliminationPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): NikshayPortalNationalTBEliminationRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.08.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.08.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Presumptive TB case queue`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_008`

#### 04.08.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.09 External Connector Specification: `EXT-009` (Reproductive and Child Health (RCH) Portal)
- **System Identifier:** `EXT-009`
- **External Entity Name:** Reproductive and Child Health (RCH) Portal
- **Governing Agency:** MoHFW / Karnataka Health
- **Network Transport Protocol:** REST / HTTPS
- **Payload Data Format:** JSON
- **Permitted Rate Limit:** 60 req/min
- **Security Trust Boundary:** `National Health Mesh`
- **Outage Fallback Mode:** Antenatal offline buffer

#### 04.09.1 Technical Integration Endpoint Contracts
```typescript
export interface IReproductiveandChildHealthRCHPortalConnector {
  transmit(payload: ReproductiveandChildHealthRCHPortalRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<ReproductiveandChildHealthRCHPortalStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class ReproductiveandChildHealthRCHPortalRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class ReproductiveandChildHealthRCHPortalStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.09.2 Data Transformation & Mapping Pipeline
```typescript
export class ReproductiveandChildHealthRCHPortalPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): ReproductiveandChildHealthRCHPortalRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.09.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.09.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Antenatal offline buffer`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_009`

#### 04.09.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.10 External Connector Specification: `EXT-010` (UIDAI Aadhaar Authentication Service)
- **System Identifier:** `EXT-010`
- **External Entity Name:** UIDAI Aadhaar Authentication Service
- **Governing Agency:** Unique Identification Authority of India
- **Network Transport Protocol:** HTTPS / XML / Auth API
- **Payload Data Format:** Encrypted XML PID Block
- **Permitted Rate Limit:** 100 req/min
- **Security Trust Boundary:** `Statutory Sovereign`
- **Outage Fallback Mode:** Fallback to municipal health ID

#### 04.10.1 Technical Integration Endpoint Contracts
```typescript
export interface IUIDAIAadhaarAuthenticationServiceConnector {
  transmit(payload: UIDAIAadhaarAuthenticationServiceRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<UIDAIAadhaarAuthenticationServiceStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class UIDAIAadhaarAuthenticationServiceRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class UIDAIAadhaarAuthenticationServiceStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.10.2 Data Transformation & Mapping Pipeline
```typescript
export class UIDAIAadhaarAuthenticationServicePayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): UIDAIAadhaarAuthenticationServiceRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.10.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.10.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Fallback to municipal health ID`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_010`

#### 04.10.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.11 External Connector Specification: `EXT-011` (Zero-Cost Municipal Voucher Billing Gateway)
- **System Identifier:** `EXT-011`
- **External Entity Name:** Zero-Cost Municipal Voucher Billing Gateway
- **Governing Agency:** BBMP Health Accounts
- **Network Transport Protocol:** REST / HTTPS
- **Payload Data Format:** JSON / Voucher Token
- **Permitted Rate Limit:** 150 req/min
- **Security Trust Boundary:** `Municipal Intranet`
- **Outage Fallback Mode:** Local voucher offline issue

#### 04.11.1 Technical Integration Endpoint Contracts
```typescript
export interface IZeroCostMunicipalVoucherBillingGatewayConnector {
  transmit(payload: ZeroCostMunicipalVoucherBillingGatewayRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<ZeroCostMunicipalVoucherBillingGatewayStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class ZeroCostMunicipalVoucherBillingGatewayRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class ZeroCostMunicipalVoucherBillingGatewayStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.11.2 Data Transformation & Mapping Pipeline
```typescript
export class ZeroCostMunicipalVoucherBillingGatewayPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): ZeroCostMunicipalVoucherBillingGatewayRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.11.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.11.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Local voucher offline issue`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_011`

#### 04.11.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.12 External Connector Specification: `EXT-012` (Bio-Medical Waste Management (BMWM) Tracking)
- **System Identifier:** `EXT-012`
- **External Entity Name:** Bio-Medical Waste Management (BMWM) Tracking
- **Governing Agency:** Karnataka State Pollution Control Board
- **Network Transport Protocol:** REST / HTTPS
- **Payload Data Format:** JSON / Barcode Log
- **Permitted Rate Limit:** 30 req/min
- **Security Trust Boundary:** `Regulatory Gateway`
- **Outage Fallback Mode:** Local waste register

#### 04.12.1 Technical Integration Endpoint Contracts
```typescript
export interface IBioMedicalWasteManagementBMWMTrackingConnector {
  transmit(payload: BioMedicalWasteManagementBMWMTrackingRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<BioMedicalWasteManagementBMWMTrackingStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class BioMedicalWasteManagementBMWMTrackingRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class BioMedicalWasteManagementBMWMTrackingStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.12.2 Data Transformation & Mapping Pipeline
```typescript
export class BioMedicalWasteManagementBMWMTrackingPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): BioMedicalWasteManagementBMWMTrackingRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.12.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.12.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Local waste register`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_012`

#### 04.12.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.13 External Connector Specification: `EXT-013` (Central Referral Hospital LIMS)
- **System Identifier:** `EXT-013`
- **External Entity Name:** Central Referral Hospital LIMS
- **Governing Agency:** BBMP Tertiary Hospitals (KC General, Bowring)
- **Network Transport Protocol:** HL7 v2 / FHIR R4
- **Payload Data Format:** HL7 ORU_R01 / FHIR
- **Permitted Rate Limit:** 60 req/min
- **Security Trust Boundary:** `Hospital Intranet`
- **Outage Fallback Mode:** Manual result printout

#### 04.13.1 Technical Integration Endpoint Contracts
```typescript
export interface ICentralReferralHospitalLIMSConnector {
  transmit(payload: CentralReferralHospitalLIMSRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<CentralReferralHospitalLIMSStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class CentralReferralHospitalLIMSRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class CentralReferralHospitalLIMSStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.13.2 Data Transformation & Mapping Pipeline
```typescript
export class CentralReferralHospitalLIMSPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): CentralReferralHospitalLIMSRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.13.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.13.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Manual result printout`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_013`

#### 04.13.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.14 External Connector Specification: `EXT-014` (Central Pollution Control Board (CPCB) & Weather API)
- **System Identifier:** `EXT-014`
- **External Entity Name:** Central Pollution Control Board (CPCB) & Weather API
- **Governing Agency:** CPCB / IMD Bengaluru
- **Network Transport Protocol:** REST / HTTPS
- **Payload Data Format:** JSON / Time-series
- **Permitted Rate Limit:** 10 req/min
- **Security Trust Boundary:** `Public Data`
- **Outage Fallback Mode:** Last known 24h average

#### 04.14.1 Technical Integration Endpoint Contracts
```typescript
export interface ICentralPollutionControlBoardCPCB&WeatherAPIConnector {
  transmit(payload: CentralPollutionControlBoardCPCB&WeatherAPIRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<CentralPollutionControlBoardCPCB&WeatherAPIStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class CentralPollutionControlBoardCPCB&WeatherAPIRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class CentralPollutionControlBoardCPCB&WeatherAPIStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.14.2 Data Transformation & Mapping Pipeline
```typescript
export class CentralPollutionControlBoardCPCB&WeatherAPIPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): CentralPollutionControlBoardCPCB&WeatherAPIRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.14.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.14.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Last known 24h average`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_014`

#### 04.14.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.15 External Connector Specification: `EXT-015` (BBMP Municipal GIS & Ward Boundary Service)
- **System Identifier:** `EXT-015`
- **External Entity Name:** BBMP Municipal GIS & Ward Boundary Service
- **Governing Agency:** BBMP Town Planning Department
- **Network Transport Protocol:** REST / GeoJSON / WFS
- **Payload Data Format:** GeoJSON Polygons
- **Permitted Rate Limit:** 50 req/min
- **Security Trust Boundary:** `Municipal Intranet`
- **Outage Fallback Mode:** Cached offline GeoJSON layers

#### 04.15.1 Technical Integration Endpoint Contracts
```typescript
export interface IBBMPMunicipalGIS&WardBoundaryServiceConnector {
  transmit(payload: BBMPMunicipalGIS&WardBoundaryServiceRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<BBMPMunicipalGIS&WardBoundaryServiceStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class BBMPMunicipalGIS&WardBoundaryServiceRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class BBMPMunicipalGIS&WardBoundaryServiceStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.15.2 Data Transformation & Mapping Pipeline
```typescript
export class BBMPMunicipalGIS&WardBoundaryServicePayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): BBMPMunicipalGIS&WardBoundaryServiceRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.15.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.15.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Cached offline GeoJSON layers`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_015`

#### 04.15.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

### 04.16 External Connector Specification: `EXT-016` (Cloud Hardware Security Module (KMS / HSM))
- **System Identifier:** `EXT-016`
- **External Entity Name:** Cloud Hardware Security Module (KMS / HSM)
- **Governing Agency:** MeitY Empaneled Cloud Provider
- **Network Transport Protocol:** PKCS#11 / REST KMS
- **Payload Data Format:** Binary Key Blocks
- **Permitted Rate Limit:** 1,000 req/sec
- **Security Trust Boundary:** `Secure Hardware Enclave`
- **Outage Fallback Mode:** Local TPM 2.0 derived keys

#### 04.16.1 Technical Integration Endpoint Contracts
```typescript
export interface ICloudHardwareSecurityModuleKMSHSMConnector {
  transmit(payload: CloudHardwareSecurityModuleKMSHSMRequestDTO): Promise<ResultEnvelopeDTO>;
  queryStatus(transactionId: string): Promise<CloudHardwareSecurityModuleKMSHSMStatusDTO>;
  healthCheck(): Promise<boolean>;
}

export class CloudHardwareSecurityModuleKMSHSMRequestDTO {
  transactionId: string;
  clinicId: string;
  timestamp: string;
  signature: string;
  data: Record<string, unknown>;
}

export class CloudHardwareSecurityModuleKMSHSMStatusDTO {
  transactionId: string;
  remoteStatus: 'ACKNOWLEDGED' | 'QUEUED' | 'REJECTED';
  remoteReferenceId: string;
  acknowledgedAt: string;
}
```

#### 04.16.2 Data Transformation & Mapping Pipeline
```typescript
export class CloudHardwareSecurityModuleKMSHSMPayloadMapper {
  static mapToExternal(domainModel: Record<string, unknown>, clinicId: string): CloudHardwareSecurityModuleKMSHSMRequestDTO {
    return {
      transactionId: crypto.randomUUID(),
      clinicId,
      timestamp: new Date().toISOString(),
      signature: calculateHMAC(domainModel),
      data: domainModel
    };
  }
}
```

#### 04.16.3 Security & Mutual Authentication Protocol
1. **Transport Security:** Strict TLS 1.3 encryption with certificate pinning.
2. **Authentication Credential:** Mutual TLS (mTLS) with client certificate issued by Karnataka Sub-CA or short-lived OAuth2 bearer token.
3. **Payload Signature:** SHA-256 HMAC or RSA-4096 digital signature attached in HTTP header `X-BBMP-Signature`.
4. **Standard Egress HTTP Headers:**
   - `X-Correlation-ID: <UUIDv7>`
   - `X-BBMP-Clinic-ID: BBMP-CLN-XXX`
   - `X-BBMP-Timestamp: <ISO-8601-UTC>`
   - `Authorization: Bearer <JWT-Token>`

#### 04.16.4 Circuit Breaker & Resilience Rules
- **Failure Rate Threshold:** 50% failures within 10-second sliding window trips circuit breaker to OPEN state.
- **State Transitions:** `CLOSED` -> `OPEN` on breach; `OPEN` -> `HALF-OPEN` after 30s timeout; `HALF-OPEN` -> `CLOSED` after 5 consecutive successful health probes.
- **Wait Duration in Open State:** 30,000ms before attempting HALF-OPEN probe.
- **Automated Fallback Action:** `Local TPM 2.0 derived keys`.
- **Dead Letter Spooling:** Persistent queue buffer in Redis/PostgreSQL retains messages for up to 72 hours.
- **DLQ Topic Name:** `dlq.integration.ext_016`

#### 04.16.5 Verification & Quality Gates
1. Automated contract testing using Pact verifying JSON payload schema conformity.
2. Chaos engineering test simulating latency injection (> 5,000ms) to verify graceful degradation.

---

## 05. 20 Canonical Integration Connectors (ARCH-INT-001 to ARCH-INT-020)
Standardized specification of 20 programmatic connectors mediating external and edge communications:

### 05.01 Connector Contract: `ARCH-INT-001` (ABDM ABHA Milestone 1 Gateway)
- **Connector Identifier:** `ARCH-INT-001`
- **Connector Title:** ABDM ABHA Milestone 1 Gateway
- **Target External Gateway:** `EXT-001`
- **Functional Responsibility:** ABHA generation via Aadhaar/Mobile OTP and demographic linking.
- **Transport Protocol:** HTTPS / REST JSON
- **SLA & Latency Boundary:** Synchronous < 2,000ms

#### Programmatic Service Interface:
```typescript
export interface IABDMABHAMilestone1Gateway {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_001`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-001", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.02 Connector Contract: `ARCH-INT-002` (ABDM Care Context Discovery Bridge)
- **Connector Identifier:** `ARCH-INT-002`
- **Connector Title:** ABDM Care Context Discovery Bridge
- **Target External Gateway:** `EXT-001`
- **Functional Responsibility:** Discovers patient care contexts registered at Namma Clinics.
- **Transport Protocol:** HTTPS / REST JSON
- **SLA & Latency Boundary:** Asynchronous callback

#### Programmatic Service Interface:
```typescript
export interface IABDMCareContextDiscoveryBridge {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_002`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-002", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.03 Connector Contract: `ARCH-INT-003` (ABDM FHIR Bundle Publisher (HIP))
- **Connector Identifier:** `ARCH-INT-003`
- **Connector Title:** ABDM FHIR Bundle Publisher (HIP)
- **Target External Gateway:** `EXT-001`
- **Functional Responsibility:** Transforms and pushes encrypted FHIR R4 Bundles to ABDM data repo.
- **Transport Protocol:** HTTPS / FHIR Bundle
- **SLA & Latency Boundary:** Asynchronous encrypted push

#### Programmatic Service Interface:
```typescript
export interface IABDMFHIRBundlePublisherHIP {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_003`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-003", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.04 Connector Contract: `ARCH-INT-004` (ABDM Consent Driven Consumer (HIU))
- **Connector Identifier:** `ARCH-INT-004`
- **Connector Title:** ABDM Consent Driven Consumer (HIU)
- **Target External Gateway:** `EXT-001`
- **Functional Responsibility:** Requests and decrypts patient historical health records on consent.
- **Transport Protocol:** HTTPS / FHIR Bundle
- **SLA & Latency Boundary:** Asynchronous decrypted in-memory

#### Programmatic Service Interface:
```typescript
export interface IABDMConsentDrivenConsumerHIU {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_004`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-004", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.05 Connector Contract: `ARCH-INT-005` (KDLWS Monthly Indent Dispatcher)
- **Connector Identifier:** `ARCH-INT-005`
- **Connector Title:** KDLWS Monthly Indent Dispatcher
- **Target External Gateway:** `EXT-002`
- **Functional Responsibility:** Submits automated monthly drug replenishment indents to state depot.
- **Transport Protocol:** HTTPS / EDIFACT JSON
- **SLA & Latency Boundary:** Batch asynchronous on 25th

#### Programmatic Service Interface:
```typescript
export interface IKDLWSMonthlyIndentDispatcher {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_005`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-005", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.06 Connector Contract: `ARCH-INT-006` (KDLWS Delivery Challan Ingestion)
- **Connector Identifier:** `ARCH-INT-006`
- **Connector Title:** KDLWS Delivery Challan Ingestion
- **Target External Gateway:** `EXT-002`
- **Functional Responsibility:** Reconciles 2D barcode scanned delivery challans with indent orders.
- **Transport Protocol:** HTTPS / REST JSON
- **SLA & Latency Boundary:** Event-driven on delivery

#### Programmatic Service Interface:
```typescript
export interface IKDLWSDeliveryChallanIngestion {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_006`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-006", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.07 Connector Contract: `ARCH-INT-007` (GVK-EMRI 108 Emergency CAD Bridge)
- **Connector Identifier:** `ARCH-INT-007`
- **Connector Title:** GVK-EMRI 108 Emergency CAD Bridge
- **Target External Gateway:** `EXT-003`
- **Functional Responsibility:** Dispatches computer-aided dispatch requests for critical transit.
- **Transport Protocol:** HTTPS / REST CAD
- **SLA & Latency Boundary:** Real-time < 500ms

#### Programmatic Service Interface:
```typescript
export interface IGVKEMRI108EmergencyCADBridge {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_007`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-007", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.08 Connector Contract: `ARCH-INT-008` (GVK-EMRI 108 Ambulance Telemetry)
- **Connector Identifier:** `ARCH-INT-008`
- **Connector Title:** GVK-EMRI 108 Ambulance Telemetry
- **Target External Gateway:** `EXT-003`
- **Functional Responsibility:** Consumes real-time GPS coordinates and transit vitals from ambulance.
- **Transport Protocol:** WSS / MQTT Stream
- **SLA & Latency Boundary:** Real-time streaming (5s interval)

#### Programmatic Service Interface:
```typescript
export interface IGVKEMRI108AmbulanceTelemetry {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_008`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-008", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.09 Connector Contract: `ARCH-INT-009` (Karnataka State SMS (KSSD) Dispatcher)
- **Connector Identifier:** `ARCH-INT-009`
- **Connector Title:** Karnataka State SMS (KSSD) Dispatcher
- **Target External Gateway:** `EXT-004`
- **Functional Responsibility:** Transmits bilingual Kannada/English SMS appointment and recall alerts.
- **Transport Protocol:** HTTPS POST API
- **SLA & Latency Boundary:** Queued BullMQ worker (500/sec)

#### Programmatic Service Interface:
```typescript
export interface IKarnatakaStateSMSKSSDDispatcher {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_009`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-009", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.10 Connector Contract: `ARCH-INT-010` (Karnataka State WhatsApp Gateway)
- **Connector Identifier:** `ARCH-INT-010`
- **Connector Title:** Karnataka State WhatsApp Gateway
- **Target External Gateway:** `EXT-004`
- **Functional Responsibility:** Dispatches rich interactive WhatsApp reminder cards to citizens.
- **Transport Protocol:** HTTPS REST API
- **SLA & Latency Boundary:** Queued BullMQ worker (200/sec)

#### Programmatic Service Interface:
```typescript
export interface IKarnatakaStateWhatsAppGateway {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_010`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-010", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.11 Connector Contract: `ARCH-INT-011` (IDSP Form P Presumptive Exporter)
- **Connector Identifier:** `ARCH-INT-011`
- **Connector Title:** IDSP Form P Presumptive Exporter
- **Target External Gateway:** `EXT-005`
- **Functional Responsibility:** Aggregates daily syndromic fever cases into statutory Form P format.
- **Transport Protocol:** HTTPS / CSV Export
- **SLA & Latency Boundary:** Nightly batch (01:00 AM)

#### Programmatic Service Interface:
```typescript
export interface IIDSPFormPPresumptiveExporter {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_011`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-011", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.12 Connector Contract: `ARCH-INT-012` (IDSP Form L Lab Confirmed Exporter)
- **Connector Identifier:** `ARCH-INT-012`
- **Connector Title:** IDSP Form L Lab Confirmed Exporter
- **Target External Gateway:** `EXT-005`
- **Functional Responsibility:** Aggregates positive diagnostic lab tests into statutory Form L format.
- **Transport Protocol:** HTTPS / CSV Export
- **SLA & Latency Boundary:** Nightly batch (01:30 AM)

#### Programmatic Service Interface:
```typescript
export interface IIDSPFormLLabConfirmedExporter {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_012`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-012", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.13 Connector Contract: `ARCH-INT-013` (BBMP Citizen Health Portal Sync)
- **Connector Identifier:** `ARCH-INT-013`
- **Connector Title:** BBMP Citizen Health Portal Sync
- **Target External Gateway:** `EXT-006`
- **Functional Responsibility:** Syncs available clinic appointment slots with municipal citizen app.
- **Transport Protocol:** HTTPS / REST OAuth2
- **SLA & Latency Boundary:** Periodic sync (15 min interval)

#### Programmatic Service Interface:
```typescript
export interface IBBMPCitizenHealthPortalSync {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_013`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-013", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.14 Connector Contract: `ARCH-INT-014` (National NCD Portal Registry Bridge)
- **Connector Identifier:** `ARCH-INT-014`
- **Connector Title:** National NCD Portal Registry Bridge
- **Target External Gateway:** `EXT-007`
- **Functional Responsibility:** Synchronizes hypertension and diabetes cohort screenings to MoHFW.
- **Transport Protocol:** HTTPS / REST FHIR
- **SLA & Latency Boundary:** Weekly batch synchronization

#### Programmatic Service Interface:
```typescript
export interface INationalNCDPortalRegistryBridge {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_014`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-014", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.15 Connector Contract: `ARCH-INT-015` (Nikshay Tuberculosis Registry Bridge)
- **Connector Identifier:** `ARCH-INT-015`
- **Connector Title:** Nikshay Tuberculosis Registry Bridge
- **Target External Gateway:** `EXT-008`
- **Functional Responsibility:** Reports presumptive and confirmed TB cases directly to Central TB Div.
- **Transport Protocol:** HTTPS / REST JSON
- **SLA & Latency Boundary:** Event-driven within 24 hours

#### Programmatic Service Interface:
```typescript
export interface INikshayTuberculosisRegistryBridge {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_015`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-015", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.16 Connector Contract: `ARCH-INT-016` (RCH Maternal & Child Health Bridge)
- **Connector Identifier:** `ARCH-INT-016`
- **Connector Title:** RCH Maternal & Child Health Bridge
- **Target External Gateway:** `EXT-009`
- **Functional Responsibility:** Reports pregnant mother ANC checkups and childhood immunization logs.
- **Transport Protocol:** HTTPS / REST JSON
- **SLA & Latency Boundary:** Weekly cohort synchronization

#### Programmatic Service Interface:
```typescript
export interface IRCHMaternal&ChildHealthBridge {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_016`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-016", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.17 Connector Contract: `ARCH-INT-017` (UIDAI Biometric Auth Gateway)
- **Connector Identifier:** `ARCH-INT-017`
- **Connector Title:** UIDAI Biometric Auth Gateway
- **Target External Gateway:** `EXT-010`
- **Functional Responsibility:** Authenticates fingerprint biometric templates for citizen identity.
- **Transport Protocol:** HTTPS XML PID Block
- **SLA & Latency Boundary:** Synchronous < 3,000ms

#### Programmatic Service Interface:
```typescript
export interface IUIDAIBiometricAuthGateway {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_017`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-017", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.18 Connector Contract: `ARCH-INT-018` (Zero-Cost Voucher Billing Reconciler)
- **Connector Identifier:** `ARCH-INT-018`
- **Connector Title:** Zero-Cost Voucher Billing Reconciler
- **Target External Gateway:** `EXT-011`
- **Functional Responsibility:** Reconciles municipal health service vouchers against ward budgets.
- **Transport Protocol:** HTTPS / REST JSON
- **SLA & Latency Boundary:** Nightly financial ledger closeout

#### Programmatic Service Interface:
```typescript
export interface IZeroCostVoucherBillingReconciler {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_018`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-018", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.19 Connector Contract: `ARCH-INT-019` (BMWM Bio-Medical Waste Barcode Sync)
- **Connector Identifier:** `ARCH-INT-019`
- **Connector Title:** BMWM Bio-Medical Waste Barcode Sync
- **Target External Gateway:** `EXT-012`
- **Functional Responsibility:** Reports color-coded waste bag barcodes to state pollution board.
- **Transport Protocol:** HTTPS / REST JSON
- **SLA & Latency Boundary:** Daily waste pickup logging

#### Programmatic Service Interface:
```typescript
export interface IBMWMBioMedicalWasteBarcodeSync {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_019`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-019", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

### 05.20 Connector Contract: `ARCH-INT-020` (Cloud Hardware Security Module (KMS))
- **Connector Identifier:** `ARCH-INT-020`
- **Connector Title:** Cloud Hardware Security Module (KMS)
- **Target External Gateway:** `EXT-016`
- **Functional Responsibility:** Performs cryptographic envelope encryption and token signing via HSM.
- **Transport Protocol:** PKCS#11 / REST KMS
- **SLA & Latency Boundary:** High-throughput in-line (< 5ms)

#### Programmatic Service Interface:
```typescript
export interface ICloudHardwareSecurityModuleKMS {
  dispatch(payload: Record<string, unknown>, ctx: RequestContext): Promise<IntegrationResultDTO>;
  handleCallback(callbackPayload: Record<string, unknown>): Promise<void>;
  validateRemoteSignature(rawPayload: string, signature: string): boolean;
  isHealthy(): Promise<boolean>;
}
```

#### Operational Retry & Backoff Policy:
- **Maximum Retry Attempts:** 5 attempts with exponential backoff.
- **Initial Backoff Interval:** 500ms (Multiplier: 2.0x, Max Interval: 30,000ms, Jitter: 15%).
- **Dead-Letter Routing:** Failed payloads routed to `dlq.integration.{c[0].lower()}`.

#### Telemetry, Metrics & Audit Sealing:
- **OpenTelemetry Span:** `span.integration.arch_int_020`
- **Prometheus Counter:** `integration_calls_total{connector="ARCH-INT-020", status="success|error"}`
- **Audit Event:** Appends sealed transmission receipt to `audit_events` with SHA-256 HMAC.

---

## 06. Karnataka Drug Logistics & Warehouse (KDLWS) Integration
Detailed supply chain Electronic Data Interchange (EDI) protocol:
1. **Monthly Stock Indent Generation:** On the 25th of each month, platform calculates 30-day drug consumption, evaluates current clinic inventory, and generates an automated replenishment indent.
2. **EDI Manifest Transmission Contract:**
```json
{
  "indentId": "KDLWS-IND-2026-09-042",
  "clinicId": "BBMP-CLN-042",
  "depotCode": "KDLWS-DEPOT-BLR-CENTRAL",
  "generatedAt": "2026-09-25T18:00:00.000Z",
  "items": [
    { "drugCode": "DRG-AML-005", "genericName": "Amlodipine 5mg", "currentStock": 420, "burnRate30Days": 1800, "requestedQuantity": 2000, "safetyBuffer": 200 },
    { "drugCode": "DRG-MET-500", "genericName": "Metformin 500mg", "currentStock": 610, "burnRate30Days": 2400, "requestedQuantity": 3000, "safetyBuffer": 300 },
    { "drugCode": "DRG-PAR-500", "genericName": "Paracetamol 500mg", "currentStock": 1200, "burnRate30Days": 4500, "requestedQuantity": 5000, "safetyBuffer": 500 }
  ],
  "signature": "sha256-hmac-kdlws-manifest-sig-88492"
}
```
3. **Receiving Manifest Barcode Verification:** Upon physical delivery by warehouse truck, clinic pharmacist scans delivery challan 2D barcode; system reconciles line items and automatically updates local batch inventory.

## 07. GVK-EMRI 108 Emergency Ambulance CAD Integration
Real-time computer-aided dispatch protocol for emergency transit:
1. **Emergency CAD Incident Creation Blueprint:**
```json
{
  "cadIncidentId": "CAD-108-EMRI-20260904-0991",
  "clinicId": "BBMP-CLN-042",
  "triageAcuity": "RED_CRITICAL",
  "patientAge": 54,
  "patientGender": "MALE",
  "provisionalDiagnosis": "Acute Inferior Wall Myocardial Infarction",
  "vitalSigns": { "bp": "80/50", "pulse": 128, "spo2": 88, "mews": 7 },
  "specialEquipmentRequired": ["OXYGEN_CONCENTRATOR", "DEFIBRILLATOR", "CARDIAC_MONITOR"],
  "clinicLocation": { "latitude": 13.0034, "longitude": 77.5689, "address": "Namma Clinic Malleshwaram 8th Cross" },
  "destinationHospital": "Sri Jayadeva Institute of Cardiovascular Sciences"
}
```
2. **Real-Time Telemetry Stream Callback Schema:**
```json
{
  "ambulanceVehicleId": "KA-02-G-1108",
  "cadIncidentId": "CAD-108-EMRI-20260904-0991",
  "currentLocation": { "latitude": 12.9980, "longitude": 77.5720 },
  "speedKmH": 48.5,
  "etaMinutes": 4,
  "paramedicName": "Suresh Kumar",
  "transitStatus": "EN_ROUTE_TO_CLINIC"
}
```

## 08. Karnataka State SMS & WhatsApp Gateway (KSSD)
Omnichannel bilingual notification dispatch architecture with 10 DLT-registered templates:

| Template ID | Purpose | Bilingual Notification Text (Kannada & English) |
| :--- | :--- | :--- |
| `DLT-TMP-001` | **Registration Welcome Slip** | ನಮ್ಮ ಕ್ಲಿನಿಕ್: ಗೌರವಾನ್ವಿತ {1}, ನಿಮ್ಮ ಟೋಕನ್ ಸಂಖ್ಯೆ {2}. ಕೊಠಡಿ {3} ಕ್ಕೆ ತೆರಳಿ. / Namma Clinic: Welcome {1}, Token {2}. Room {3}. |
| `DLT-TMP-002` | **Consultation Follow-Up Recall** | ನಮ್ಮ ಕ್ಲಿನಿಕ್: ಗೌರವಾನ್ವಿತ {1}, ನಿಮ್ಮ ಮುಂದಿನ ಭೇಟಿ ದಿನಾಂಕ {2}. ಮಾತ್ರೆಗಳನ್ನು ತಪ್ಪದೆ ಸೇವಿಸಿ. / Return visit scheduled on {2}. |
| `DLT-TMP-003` | **Diagnostic Lab Result Ready** | ನಮ್ಮ ಕ್ಲಿನಿಕ್: ನಿಮ್ಮ ಲ್ಯಾಬ್ ಪರೀಕ್ಷಾ ವರದಿ ಸಿದ್ಧವಾಗಿದೆ. ಕ್ಲಿನಿಕ್‌ನಲ್ಲಿ ಪಡೆಯಿರಿ. / Your lab test results are ready for collection. |
| `DLT-TMP-004` | **Pediatric Immunization Camp** | ನಮ್ಮ ಕ್ಲಿನಿಕ್: ನಿಮ್ಮ ಮಗುವಿನ ಲಸಿಕೆ ದಿನಾಂಕ {1}. ಸಮೀಪದ ನಮ್ಮ ಕ್ಲಿನಿಕ್‌ಗೆ ಭೇಟಿ ನೀಡಿ. / Child immunization camp scheduled on {1}. |
| `DLT-TMP-005` | **Hypertension Defaulter Alert** | ನಮ್ಮ ಕ್ಲಿನಿಕ್: ರಕ್ತದೊತ್ತಡ ತಪಾಸಣೆಗೆ ನಿಮ್ಮ ಭೇಟಿ ಬಾಕಿ ಇದೆ. ದಯವಿಟ್ಟು ಕ್ಲಿನಿಕ್‌ಗೆ ಬನ್ನಿ. / Pending BP follow-up visit. Please visit clinic. |
| `DLT-TMP-006` | **Diabetes Defaulter Alert** | ನಮ್ಮ ಕ್ಲಿನಿಕ್: ಸಕ್ಕರೆ ಕಾಯಿಲೆ ಔಷಧಿ ಮುಗಿದಿದೆಯೇ? ಉಚಿತ ಪರೀಕ್ಷೆ ಮತ್ತು ಮಾತ್ರೆಗೆ ಬನ್ನಿ. / Diabetes checkup pending. Free tests & medicines. |
| `DLT-TMP-007` | **Prescription Dispense Confirmation** | ನಮ್ಮ ಕ್ಲಿನಿಕ್: {1} ಮಾತ್ರೆಗಳನ್ನು ನೀಡಲಾಗಿದೆ. ದಿನಕ್ಕೆ {2} ಬಾರಿ ಸೇವಿಸಿ. / Dispensed {1}. Dosage: {2} times daily. |
| `DLT-TMP-008` | **Secondary Referral Dossier** | ನಮ್ಮ ಕ್ಲಿನಿಕ್: ನಿಮ್ಮನ್ನು {1} ಆಸ್ಪತ್ರೆಗೆ ರೆಫರ್ ಮಾಡಲಾಗಿದೆ. ರೆಫರಲ್ ಕೋಡ್ {2}. / Referred to {1}. Referral Code {2}. |
| `DLT-TMP-009` | **Emergency 108 Dispatch Alert** | ನಮ್ಮ ಕ್ಲಿನಿಕ್: 108 ತುರ್ತು ಆಂಬ್ಯುಲೆನ್ಸ್ ವಾಹನ {1} ಕ್ಲಿನಿಕ್‌ಗೆ ಬರುತ್ತಿದೆ. / 108 Ambulance {1} dispatched to clinic. |
| `DLT-TMP-010` | **Citizen Grievance Acknowledgment** | ನಮ್ಮ ಕ್ಲಿನಿಕ್: ನಿಮ್ಮ ದೂರು {1} ಸ್ವೀಕರಿಸಲಾಗಿದೆ. 48 ಗಂಟೆಗಳಲ್ಲಿ ಪರಿಹರಿಸಲಾಗುವುದು. / Grievance {1} received. SLA 48 hours. |

## 09. Statutory Disease Reporting (IDSP / IHIP & Nikshay)
Automated epidemiological reporting workflows and statutory data schemas:
1. **IDSP Form P (Presumptive Cases) Data Schema:**
   - `reporting_date`: ISO Date
   - `clinic_id`: BBMP Clinic Code
   - `syndrome_code`: Acute Diarrheal Disease (ADD), Bacillary Dysentery (BD), Viral Hepatitis (VH), Enteric Fever (EF), Dengue / DHF, Chikungunya, Acute Encephalitis Syndrome (AES), Influenza-Like Illness (ILI).
   - `case_count_male`: Integer
   - `case_count_female`: Integer
   - `deaths_count`: Integer
2. **IDSP Form L (Lab Confirmed Cases) Data Schema:**
   - `specimen_id`: UUIDv7
   - `test_code`: LOINC 58 Rapid Test Master
   - `pathogen_confirmed`: Salmonella typhi, Plasmodium falciparum, Dengue NS1 Antigen, Vibrio cholerae.
   - `patient_ward`: BBMP Ward Number (1-225)
3. **IDSP Form S (Syndromic Community Surveillance) Data Schema:**
   - `reporting_period`: Weekly ISO Week String (e.g. `2026-W36`)
   - `ward_number`: Municipal Ward (1-225)
   - `fever_syndrome_count`: Total acute febrile illness cases
   - `cough_syndrome_count`: Total acute respiratory infection cases
   - `diarrhea_syndrome_count`: Total acute diarrheal illness cases
   - `jaundice_syndrome_count`: Total acute jaundice syndrome cases
   - `rash_syndrome_count`: Total fever with rash cases (presumptive measles/rubella)
   - `investigated_clusters_count`: Number of epidemiological field investigations triggered
4. **Nikshay TB National Integration Protocol:**
   - `POST /api/v1/nikshay/patient/notify`: Notifies presumptive tuberculosis case to central CTD.
   - `POST /api/v1/nikshay/treatment/outcome`: Updates 6-month treatment outcome (Cured, Treatment Completed, Defaulter).
   - `GET /api/v1/nikshay/dbt/status`: Retrieves Direct Benefit Transfer (DBT) incentive credit status for citizen.

## 10. Interoperability Quality Gates & Architecture Fitness Tests
Automated CI/CD validation gates ensuring zero interoperability regression across versions:
1. **Pact Contract Verification:** All external consumer-driven contracts are validated in CI against remote Pact Broker; schema drift breaks the build.
2. **FHIR R4 Structural Validator:** Every generated FHIR resource is validated against the official HL7 Java FHIR Validator and NRCES Indian Core schemas.
3. **DLT Template Conformance Gate:** Outbound SMS formatting functions are linted against TRAI DLT approved template strings, rejecting unregistered variable counts.
4. **mTLS Handshake Automated Test:** Synthetic test suite executes daily client certificate verification against simulated state gateways.
5. **Chaos Latency Fault Injection:** Automated tests inject 3,000ms delay into external mock servers, verifying that circuit breakers open cleanly and fallback queues engage without dropping patient transactions.
6. **Zero-Plaintext Egress Audit:** Egress proxy inspects outbound payloads, verifying that unencrypted Aadhaar numbers or raw biometric templates are never transmitted outside approved sovereign endpoints.
