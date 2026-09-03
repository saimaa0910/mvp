# 📖 Master Health & Operational Data Dictionary
## Namma Clinic Digital Health & Operations Platform
### Standards-Aligned Enterprise Healthcare Data Dictionary
### Alignments: ABDM FHIR R4 | ICD-10 | LOINC | SNOMED CT | MoHFW EHR Standards
### Document Code: DG-DIC-02 | Version: 1.0 | Date: September 2026

---

## 1. Data Architecture Overview

This Data Dictionary defines all structural entities, attributes, data types, constraints, validation rules, and national healthcare standards alignments for the Namma Clinic Platform. All transactional persistence adheres to **PostgreSQL 16 relational semantics**, with JSONB extensions for flexible template captures and FHIR R4 interoperability envelopes.

---

## 2. Core Clinical & Operational Entities

### 2.1 Entity: `patients` (Citizen Master Demographic Profile)
* **Description:** Represents unique individual citizens registered at any Namma Clinic.
* **FHIR R4 Equivalent:** `Patient` resource.

| Field Name | Physical Type | Nullable | Primary / Foreign Key | Description & Constraints | Standards / Vocabulary Mapping |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `patient_id` | `VARCHAR(36)` | NO | PK | System UUID (v4). | `Patient.id` |
| `clinic_reg_no`| `VARCHAR(20)` | NO | Unique | Clinic-issued ID (e.g., `NC-2026-000142`). | `Patient.identifier (type=MR)` |
| `abha_id` | `VARCHAR(17)` | YES | Unique | 14-digit ABDM ABHA number (`XX-XXXX-XXXX-XXXX`). | `Patient.identifier (system=abdm)` |
| `abha_address` | `VARCHAR(100)`| YES | Unique | ABDM PHR handle (`user@abdm`). | `Patient.identifier (system=abha-address)`|
| `full_name` | `VARCHAR(150)`| NO | — | Legal full name in English. | `Patient.name.text` |
| `name_kannada` | `VARCHAR(150)`| YES | — | Full name transliterated in Kannada script. | `Patient.name.extension (kannada)` |
| `date_of_birth`| `DATE` | YES | — | ISO-8601 Date of birth (`YYYY-MM-DD`). | `Patient.birthDate` |
| `age_years` | `SMALLINT` | NO | — | Stored age if DOB unknown (0–120). | Calculated / `Patient.extension` |
| `gender` | `VARCHAR(10)` | NO | — | Enum: `'MALE'`, `'FEMALE'`, `'OTHER'`. | `Patient.gender` (AdministrativeGender) |
| `mobile_phone` | `VARCHAR(10)` | NO | Indexed | 10-digit Indian mobile number (`^[6-9]\d{9}$`). | `Patient.telecom (system=phone)` |
| `residential_addr`| `TEXT` | YES | — | Street address, landmark. | `Patient.address.line` |
| `bbmp_ward_no` | `SMALLINT` | YES | Indexed | Official BBMP Ward Number (1 to 243). | `Patient.address.extension (ward)` |
| `bbmp_zone` | `VARCHAR(30)` | NO | Indexed | Enum: `'NORTH'`, `'SOUTH'`, `'EAST'`, `'WEST'`, `'CENTRAL'`. | `Patient.address.district` |
| `blood_group` | `VARCHAR(5)` | YES | — | Enum: `'A+'`, `'A-'`, `'B+'`, `'B-'`, `'AB+'`, `'AB-'`, `'O+'`, `'O-'`. | SNOMED CT: `365636006` |
| `emergency_contact`| `VARCHAR(10)`| YES | — | Contact number of relative/guardian. | `Patient.contact.telecom` |
| `created_at` | `TIMESTAMPTZ` | NO | — | Record creation timestamp in UTC. | `Patient.meta.lastUpdated` |

---

### 2.2 Entity: `visits` (Encounter & Daily Token Session)
* **Description:** Represents a single patient visit encounter at a clinic on a given day.
* **FHIR R4 Equivalent:** `Encounter` resource.

| Field Name | Physical Type | Nullable | Primary / Foreign Key | Description & Constraints | Standards / Vocabulary Mapping |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `visit_id` | `VARCHAR(36)` | NO | PK | Encounter UUID. | `Encounter.id` |
| `patient_id` | `VARCHAR(36)` | NO | FK (`patients`) | References registered citizen. | `Encounter.subject` |
| `clinic_id` | `VARCHAR(20)` | NO | FK (`clinics`) | Clinic facility where encounter occurred. | `Encounter.serviceProvider` |
| `token_number` | `VARCHAR(10)` | NO | Indexed | Daily sequence token (e.g., `'A001'`). | `Encounter.identifier` |
| `service_category`| `VARCHAR(30)`| NO | — | Enum: `'GENERAL_OPD'`, `'FEVER'`, `'NCD_SCREENING'`, `'MCH'`, `'IMMUNIZATION'`. | SNOMED CT: `308292007` |
| `queue_status` | `VARCHAR(20)` | NO | Indexed | Enum: `'WAITING'`, `'TRIAGE'`, `'WITH_DOCTOR'`, `'PHARMACY'`, `'LAB'`, `'DONE'`, `'LAMA'`. | `Encounter.status` |
| `danger_flag` | `BOOLEAN` | NO | Default `FALSE`| Clinical emergency alert trigger. | `Encounter.priority` |
| `attending_doctor`| `VARCHAR(36)`| YES | FK (`users`) | Medical Officer conducting consult. | `Encounter.participant.individual` |
| `visit_date` | `DATE` | NO | Indexed | Date of encounter. | `Encounter.period.start` |
| `check_in_time` | `TIMESTAMPTZ` | NO | — | Timestamp of registration/token issue. | `Encounter.period.start` |
| `discharge_time`| `TIMESTAMPTZ` | YES | — | Timestamp of final discharge/pharmacy completion.| `Encounter.period.end` |

---

### 2.3 Entity: `vitals` (Nursing Triage Parameter Store)
* **Description:** Quantitative vital signs captured during nursing triage.
* **FHIR R4 Equivalent:** `Observation` resource (Panel).

| Field Name | Physical Type | Units | Range Constraints | Clinical Alert Thresholds | Standard Mapping (LOINC) |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `bp_systolic` | `SMALLINT` | mmHg | 50 – 260 | Warning: $\ge 140$; Danger: $\ge 180$ or $<80$ | LOINC `8480-6` |
| `bp_diastolic` | `SMALLINT` | mmHg | 30 – 160 | Warning: $\ge 90$; Danger: $\ge 110$ or $<50$ | LOINC `8462-4` |
| `pulse_rate` | `SMALLINT` | bpm | 30 – 220 | Warning: $\ge 100$ or $<55$; Danger: $>140$ or $<40$ | LOINC `8867-4` |
| `body_temperature`| `NUMERIC(4,1)`| °C | 32.0 – 43.0 | Warning: $\ge 38.0$; Danger: $\ge 40.0$ or $<35.0$ | LOINC `8310-5` |
| `oxygen_saturation`| `SMALLINT` | % | 50 – 100 | Warning: $90–94\%$; Danger: $<90\%$ | LOINC `2708-6` (`SpO2`) |
| `random_blood_sugar`| `SMALLINT`| mg/dL| 20 – 600 | Warning: $\ge 140$; Danger: $>400$ or $<50$ | LOINC `2339-0` |
| `body_weight` | `NUMERIC(5,2)`| kg | 1.0 – 250.0 | — | LOINC `29463-7` |
| `body_height` | `NUMERIC(5,1)`| cm | 30.0 – 240.0 | — | LOINC `8302-2` |
| `calculated_bmi`| `NUMERIC(4,1)`| $\text{kg/m}^2$| Auto-derived | Overweight: $\ge 25.0$; Obese: $\ge 30.0$ | LOINC `39156-5` |
| `chief_complaints`| `JSONB` | Array | Quick-pick list + symptom duration. | SNOMED CT: `418799008` |

---

### 2.4 Entity: `prescriptions` & `medication_items`
* **Description:** Medical Officer orders for pharmaceutical dispensing.
* **FHIR R4 Equivalent:** `MedicationRequest` & `MedicationDispense`.

| Field Name | Physical Type | Nullable | Description & Constraints | Standard Mapping |
| :--- | :--- | :---: | :--- | :--- |
| `item_id` | `VARCHAR(36)` | NO (PK) | Item UUID. | `MedicationRequest.id` |
| `visit_id` | `VARCHAR(36)` | NO (FK) | Reference to parent encounter. | `MedicationRequest.encounter` |
| `medicine_name` | `VARCHAR(120)`| NO | Standard generic formulation name. | Karnataka KSDLPS Master / RxNorm |
| `dosage_form` | `VARCHAR(30)` | NO | Enum: `'TABLET'`, `'CAPSULE'`, `'SYRUP'`, `'INJECTION'`, `'INHALER'`, `'OINTMENT'`. | SNOMED CT: `736542009` |
| `strength` | `VARCHAR(30)` | NO | e.g., `'500 mg'`, `'5 mg'`, `'100 ml'`. | `Medication.ingredient.strength` |
| `frequency` | `VARCHAR(30)` | NO | Enum: `'OD'` (once daily), `'BD'` (twice), `'TDS'` (thrice), `'QID'`, `'HS'`, `'SOS'`. | SNOMED CT: `260548002` |
| `duration_days` | `SMALLINT` | NO | Duration in integer days (1 to 90). | `MedicationRequest.dispenseRequest.expectedSupplyDuration` |
| `instructions_en`| `VARCHAR(100)`| NO | e.g., `'After meals'`, `'Before meals'`, `'At bedtime'`. | `MedicationRequest.dosageInstruction.patientInstruction` |
| `instructions_kn`| `VARCHAR(100)`| NO | Kannada equivalent: e.g., `'ಊಟದ ನಂತರ'`, `'ಖಾಲಿ ಹೊಟ್ಟೆಯಲ್ಲಿ'`. | Localized Extension |
| `is_dispensed` | `BOOLEAN` | NO | Default `FALSE`; flipped by pharmacist on issue. | `MedicationDispense.status` |

---

### 2.5 Entity: `pharmacy_stock_ledger`
* **Description:** Perpetual transactional ledger tracking clinic medicine batches and quantities.

| Field Name | Physical Type | Nullable | Description & Constraints |
| :--- | :--- | :---: | :--- |
| `stock_entry_id`| `VARCHAR(36)` | NO (PK) | Ledger entry UUID. |
| `clinic_id` | `VARCHAR(20)` | NO (FK) | Clinic identifier. |
| `medicine_code`| `VARCHAR(50)` | NO | KSDLPS standard medicine code. |
| `batch_number` | `VARCHAR(30)` | NO | Manufacturer batch identification. |
| `current_stock`| `INTEGER` | NO | Real-time on-hand quantity in units (pills/bottles). $\ge 0$. |
| `min_threshold`| `INTEGER` | NO | Buffer threshold triggering automated reorder alerts. |
| `expiry_date` | `DATE` | NO | Batch expiration date. Alert generated if $\le 60$ days. |
| `last_updated` | `TIMESTAMPTZ` | NO | Automatic trigger timestamp. |

---

### 2.6 Entity: `referrals`
* **Description:** Outbound specialist or hospital referral tracks.
* **FHIR R4 Equivalent:** `ServiceRequest` resource.

| Field Name | Physical Type | Nullable | Description & Constraints | Standard Mapping |
| :--- | :--- | :---: | :--- | :--- |
| `referral_id` | `VARCHAR(36)` | NO (PK) | Referral UUID (`REF-NC-YYYY-NNNNN`). | `ServiceRequest.id` |
| `visit_id` | `VARCHAR(36)` | NO (FK) | Originating clinical visit. | `ServiceRequest.encounter` |
| `patient_id` | `VARCHAR(36)` | NO (FK) | Citizen referred. | `ServiceRequest.subject` |
| `destination_id`| `VARCHAR(50)` | NO | Target health facility (e.g., Victoria, Bowring, Vani Vilas, UPHC). | `ServiceRequest.performer` |
| `clinical_reason`| `TEXT` | NO | Doctor's referral narrative and provisional diagnosis. | `ServiceRequest.reasonCode` |
| `urgency_level` | `VARCHAR(15)` | NO | Enum: `'ROUTINE'`, `'PRIORITY'`, `'EMERGENCY'`. | `ServiceRequest.priority` |
| `referral_status`| `VARCHAR(15)`| NO | Enum: `'OPEN'`, `'ACKNOWLEDGED'`, `'CLOSED'`, `'EXPIRED'`. | `ServiceRequest.status` |
| `closure_date` | `DATE` | YES | Date when referred hospital confirmed attendance. | `ServiceRequest.occurrenceDateTime` |
