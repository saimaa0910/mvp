# 🇮🇳 Ayushman Bharat Digital Mission (ABDM) Integration
## Namma Clinic Digital Health & Operations Platform
**Document Code:** INT-ABD-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. ABDM Milestone Architecture & Compliance Scope

```mermaid
graph TD
    subgraph ABDM National Health Network
        M1[Milestone 1: ABHA Creation & Verification]
        M2[Milestone 2: Health Information Provider - HIP]
        M3[Milestone 3: Health Information User - HIU]
    end
    subgraph Namma Clinic Platform
        N1[Aadhaar OTP / Demographics Verification]
        N2[FHIR R4 Bundle Generator & Care Context]
        N3[Consent Request & Health Data View]
    end
    N1 <-->|ABDM Gateway API| M1
    N2 <-->|HIP Webhook / Data Push| M2
    N3 <-->|HIU Consent Manager API| M3
```

### 2. Supported FHIR R4 Resources
- `Patient`: Demographics, UHID identifier, ABHA number.
- `Encounter`: Clinic visit metadata, attending doctor, timestamp.
- `Condition`: ICD-10 / SNOMED CT diagnostic codes.
- `MedicationRequest`: Electronic prescription details.
- `Observation`: Vital signs (BP, Pulse, Glucose) and lab results.
