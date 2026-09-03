# 🧪 End-to-End (E2E) Test Plan & Patient Journey Scenarios
## Namma Clinic Digital Health & Operations Platform
**Document Code:** QA-E2E-06 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Primary Patient Journey E2E Scenarios (Playwright Automation)

#### Scenario E2E-01: Standard Outpatient Visit (Registration -> Triage -> Doctor -> Pharmacy)
- **Preconditions:** Active clinic session in Ward 150; nurse, doctor, and pharmacist logged in.
- **Step 1 (Nurse):** Register new patient (Name: Ramesh, Age: 45, Gender: Male). System issues Token `T-001`.
- **Step 2 (Nurse):** Capture vitals (BP: 130/85, Pulse: 74, Temp: 98.4°F, Glucose: 110 mg/dL). Vitals saved.
- **Step 3 (Doctor):** Doctor selects Token `T-001` from queue. Reviews vitals. Selects chief complaint 'Headache x 3 days'. Selects provisional diagnosis 'Tension Headache'. Prescribes Paracetamol 500mg (1-0-1 x 3 days). Signs prescription.
- **Step 4 (Pharmacist):** Pharmacist opens pending queue. Sees `T-001`. Scans batch `PARA-2026-08`. Confirms 6 tablets dispensed. Clicks 'Dispense'.
- **Verification:** Visit status transitions to 'Completed'; stock ledger for Paracetamol decreases by 6; patient receives SMS confirmation; audit record created.

#### Scenario E2E-02: Offline Emergency Consultation with Background Sync
- **Preconditions:** Clinic tablet loses internet connectivity (airplane mode simulated).
- **Step 1:** Nurse registers walk-in emergency trauma patient. Token `E-001` generated in local IndexedDB.
- **Step 2:** Doctor documents emergency wound dressing and tetanus toxoid administration.
- **Step 3:** Network reconnected. Background sync engine triggers.
- **Verification:** Token `E-001` and encounter data sync to server within 15 seconds; zero data loss; no duplicate IDs created.
