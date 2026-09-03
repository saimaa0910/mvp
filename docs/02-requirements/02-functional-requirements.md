# ⚙️ Functional Requirements Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** REQ-FR-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Functional Scope & Verification Matrix

| ID | Title | Description | Priority | Source Req | Acceptance Criteria | Epic | Feature | Story |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| FR-001 | Fast Citizen Search | Search patients by Mobile Number, UHID, ABHA ID, or Name + Age within 200ms. | P0 | BR-001 | Indexed query in PostgreSQL pg_trgm and IndexedDB. | EPIC-05 | FEAT-011 | US-021 |
| FR-002 | Demographic Registration | Capture Name, Phone, Age, Gender, Ward, Address with optional Aadhaar/ABHA. | P0 | BR-001 | Patient record created with unique UHID. | EPIC-05 | FEAT-012 | US-023 |
| FR-003 | Daily Queue Token Generation | Issue daily sequential token (e.g. T-042) linked to clinic and date. | P0 | BR-001 | Token printed on 2-inch thermal slip with QR code. | EPIC-06 | FEAT-015 | US-032 |
| FR-004 | Triage Vitals Capture | Record BP, Pulse, SpO2, Temperature, Height, Weight, Blood Glucose, BMI. | P0 | BR-001 | Vitals attached to visit record; abnormal values flagged in red. | EPIC-07 | FEAT-018 | US-038 |
| FR-005 | Clinical Chief Complaints | Select chief complaints from 1-click clinical chips with duration selector. | P0 | BR-002 | Selected chips serialized into encounter JSONB. | EPIC-08 | FEAT-021 | US-045 |
| FR-006 | Provisional Diagnosis Coding | Search and select ICD-10 / SNOMED CT diagnoses with free-text note override. | P0 | BR-002 | Diagnosis saved with certainty (Provisional / Confirmed). | EPIC-08 | FEAT-022 | US-047 |
| FR-007 | Electronic Prescription Generation | Prescribe formulary drugs with dosage, frequency, duration, and food timing. | P0 | BR-002 | Validated prescription sent to pharmacy queue immediately. | EPIC-09 | FEAT-025 | US-052 |
| FR-008 | Pharmacy Dispense Confirmation | Pharmacist verifies batch number, expiry date, and marks items as dispensed. | P0 | BR-003 | Inventory ledger deducted; bilingual prescription slip printed. | EPIC-10 | FEAT-028 | US-061 |
| FR-009 | Stock Ledger Deduction | Automatic real-time deduction of medicine batch quantity upon dispense. | P0 | BR-003 | Stock ledger updated within atomic ACID transaction. | EPIC-11 | FEAT-031 | US-066 |
| FR-010 | Point-of-Care Lab Orders | Doctor orders from 14 essential tests (RBS, Malaria, Dengue NS1, Urine, etc.). | P1 | BR-009 | Lab order visible in lab queue with pending status. | EPIC-12 | FEAT-035 | US-075 |
| FR-011 | Secondary Care Referral | Generate outbound referral letter with clinical summary and destination hospital. | P1 | BR-008 | Referral QR generated and status set to 'Referred'. | EPIC-13 | FEAT-039 | US-083 |
| FR-012 | Offline Session Sync | Queue local transactions and sync sequentially to server upon network reconnect. | P0 | BR-007 | Zero data loss; conflict-free deterministic merge. | EPIC-19 | FEAT-059 | US-125 |
