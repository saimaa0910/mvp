# 🗄️ Database Relational Schema DDL & Migration Architecture
## Namma Clinic Digital Health & Operations Platform
### Target Engine: PostgreSQL 16 (RDS Multi-AZ / Self-Hosted)
### Document Code: TD-DB-03 | Version: 1.0 | Date: September 2026

---

## 1. Architectural Guidelines & Extensions

The database schema is engineered for high-concurrency transactional health workloads with automated temporal auditing and analytical partitioning.

```sql
-- Required PostgreSQL 16 Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";    -- Trigram search for fast patient matching
CREATE EXTENSION IF NOT EXISTS "btree_gist";  -- Temporal & exclusion constraints
```

---

## 2. Complete Relational DDL (Data Definition Language)

```sql
-- ====================================================================
-- 1. CLINICS & FACILITIES MASTER
-- ====================================================================
CREATE TABLE clinics (
    clinic_id           VARCHAR(20) PRIMARY KEY, -- e.g., 'NC-W-001'
    clinic_name         VARCHAR(150) NOT NULL,
    clinic_name_kn      VARCHAR(150),
    bbmp_zone           VARCHAR(30) NOT NULL CHECK (bbmp_zone IN ('NORTH', 'SOUTH', 'EAST', 'WEST', 'CENTRAL')),
    bbmp_ward_no        SMALLINT NOT NULL CHECK (bbmp_ward_no BETWEEN 1 AND 243),
    physical_address    TEXT NOT NULL,
    pincode             VARCHAR(6) NOT NULL CHECK (pincode ~ '^\d{6}$'),
    latitude            NUMERIC(9,6),
    longitude           NUMERIC(9,6),
    is_operational      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_clinics_zone ON clinics (bbmp_zone, bbmp_ward_no);

-- ====================================================================
-- 2. USERS & ACCESS CONTROL (RBAC)
-- ====================================================================
CREATE TABLE users (
    user_id             VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    username            VARCHAR(50) UNIQUE NOT NULL,
    password_hash       VARCHAR(255) NOT NULL,
    full_name           VARCHAR(100) NOT NULL,
    role                VARCHAR(25) NOT NULL CHECK (role IN (
                            'RECEPTIONIST', 'NURSE', 'DOCTOR', 'PHARMACIST', 
                            'LAB_TECH', 'CLINIC_ADMIN', 'ZONAL_MO', 'COMMISSIONER'
                        )),
    clinic_id           VARCHAR(20) REFERENCES clinics(clinic_id) ON DELETE RESTRICT,
    mobile_phone        VARCHAR(10) NOT NULL CHECK (mobile_phone ~ '^[6-9]\d{9}$'),
    email               VARCHAR(100),
    mfa_secret          VARCHAR(64),
    mfa_enabled         BOOLEAN NOT NULL DEFAULT FALSE,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    last_login_at       TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_clinic ON users (clinic_id, role);

-- ====================================================================
-- 3. PATIENTS (MASTER DEMOGRAPHIC INDEX)
-- ====================================================================
CREATE TABLE patients (
    patient_id          VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    clinic_reg_no       VARCHAR(25) UNIQUE NOT NULL, -- e.g., 'NC-2026-000142'
    abha_id             VARCHAR(17) UNIQUE,          -- e.g., '12-3456-7890-0001'
    abha_address        VARCHAR(100) UNIQUE,
    full_name           VARCHAR(150) NOT NULL,
    name_kannada        VARCHAR(150),
    date_of_birth       DATE,
    age_years           SMALLINT NOT NULL CHECK (age_years BETWEEN 0 AND 125),
    gender              VARCHAR(10) NOT NULL CHECK (gender IN ('MALE', 'FEMALE', 'OTHER')),
    mobile_phone        VARCHAR(10) NOT NULL CHECK (mobile_phone ~ '^[6-9]\d{9}$'),
    residential_address TEXT,
    bbmp_ward_no        SMALLINT CHECK (bbmp_ward_no BETWEEN 1 AND 243),
    bbmp_zone           VARCHAR(30) CHECK (bbmp_zone IN ('NORTH', 'SOUTH', 'EAST', 'WEST', 'CENTRAL')),
    blood_group         VARCHAR(5) CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    known_conditions    JSONB DEFAULT '[]'::jsonb,  -- Array of strings e.g. ["Hypertension", "Diabetes"]
    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patients_mobile ON patients (mobile_phone);
CREATE INDEX idx_patients_name_trgm ON patients USING gin (full_name gin_trgm_ops);
CREATE INDEX idx_patients_abha ON patients (abha_id) WHERE abha_id IS NOT NULL;

-- ====================================================================
-- 4. VISITS & QUEUE SESSIONS
-- ====================================================================
CREATE TABLE visits (
    visit_id            VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    patient_id          VARCHAR(36) NOT NULL REFERENCES patients(patient_id) ON DELETE RESTRICT,
    clinic_id           VARCHAR(20) NOT NULL REFERENCES clinics(clinic_id) ON DELETE RESTRICT,
    token_number        VARCHAR(10) NOT NULL, -- e.g., 'A001'
    service_category    VARCHAR(30) NOT NULL CHECK (service_category IN (
                            'GENERAL_OPD', 'FEVER', 'NCD_SCREENING', 'MCH', 'IMMUNIZATION'
                        )),
    queue_status        VARCHAR(20) NOT NULL CHECK (queue_status IN (
                            'WAITING', 'TRIAGE', 'WITH_DOCTOR', 'PHARMACY', 'LAB', 'DONE', 'LAMA'
                        )),
    danger_flag         BOOLEAN NOT NULL DEFAULT FALSE,
    attending_doctor_id VARCHAR(36) REFERENCES users(user_id) ON DELETE SET NULL,
    visit_date          DATE NOT NULL DEFAULT CURRENT_DATE,
    check_in_time       TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    discharge_time      TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_visits_clinic_date ON visits (clinic_id, visit_date, queue_status);
CREATE INDEX idx_visits_patient ON visits (patient_id, visit_date DESC);

-- ====================================================================
-- 5. VITALS & NURSING TRIAGE
-- ====================================================================
CREATE TABLE vitals (
    vitals_id           VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    visit_id            VARCHAR(36) UNIQUE NOT NULL REFERENCES visits(visit_id) ON DELETE CASCADE,
    bp_systolic         SMALLINT CHECK (bp_systolic BETWEEN 40 AND 300),
    bp_diastolic        SMALLINT CHECK (bp_diastolic BETWEEN 30 AND 200),
    pulse_rate          SMALLINT CHECK (pulse_rate BETWEEN 30 AND 250),
    body_temperature    NUMERIC(4,1) CHECK (body_temperature BETWEEN 30.0 AND 45.0),
    oxygen_saturation   SMALLINT CHECK (oxygen_saturation BETWEEN 40 AND 100),
    random_blood_sugar  SMALLINT CHECK (random_blood_sugar BETWEEN 10 AND 700),
    body_weight         NUMERIC(5,2) CHECK (body_weight BETWEEN 0.5 AND 300.0),
    body_height         NUMERIC(5,1) CHECK (body_height BETWEEN 20.0 AND 250.0),
    calculated_bmi      NUMERIC(4,1),
    chief_complaints    JSONB NOT NULL DEFAULT '[]'::jsonb,
    additional_notes    TEXT,
    recorded_by_user_id VARCHAR(36) REFERENCES users(user_id),
    recorded_at         TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ====================================================================
-- 6. CLINICAL NOTES & DOCTOR ENCOUNTER
-- ====================================================================
CREATE TABLE clinical_encounters (
    encounter_id        VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    visit_id            VARCHAR(36) UNIQUE NOT NULL REFERENCES visits(visit_id) ON DELETE CASCADE,
    doctor_id           VARCHAR(36) NOT NULL REFERENCES users(user_id),
    clinical_notes      TEXT,
    provisional_diag    TEXT NOT NULL,
    icd10_code          VARCHAR(10),
    template_applied    VARCHAR(50),
    follow_up_date      DATE,
    completed_at        TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ====================================================================
-- 7. MEDICINE MASTER & PHARMACY STOCK
-- ====================================================================
CREATE TABLE medicines_master (
    medicine_code       VARCHAR(50) PRIMARY KEY,
    generic_name        VARCHAR(150) NOT NULL,
    dosage_form         VARCHAR(30) NOT NULL CHECK (dosage_form IN ('TABLET', 'CAPSULE', 'SYRUP', 'INJECTION', 'INHALER', 'OINTMENT', 'SACHET')),
    strength            VARCHAR(50) NOT NULL,
    unit_of_measure     VARCHAR(20) NOT NULL, -- e.g., 'Tablets', 'Bottles'
    category            VARCHAR(50) NOT NULL,
    is_essential        BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE pharmacy_stock_ledger (
    stock_id            VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    clinic_id           VARCHAR(20) NOT NULL REFERENCES clinics(clinic_id) ON DELETE RESTRICT,
    medicine_code       VARCHAR(50) NOT NULL REFERENCES medicines_master(medicine_code),
    batch_number        VARCHAR(30) NOT NULL,
    current_stock       INTEGER NOT NULL CHECK (current_stock >= 0),
    min_threshold       INTEGER NOT NULL CHECK (min_threshold > 0),
    expiry_date         DATE NOT NULL,
    last_updated        TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_clinic_medicine_batch UNIQUE (clinic_id, medicine_code, batch_number)
);

CREATE INDEX idx_stock_clinic_status ON pharmacy_stock_ledger (clinic_id, current_stock, min_threshold);

-- ====================================================================
-- 8. PRESCRIPTIONS & DISPENSING
-- ====================================================================
CREATE TABLE prescriptions (
    prescription_id     VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    visit_id            VARCHAR(36) NOT NULL REFERENCES visits(visit_id) ON DELETE CASCADE,
    prescribed_by       VARCHAR(36) NOT NULL REFERENCES users(user_id),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE prescription_items (
    item_id             VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    prescription_id     VARCHAR(36) NOT NULL REFERENCES prescriptions(prescription_id) ON DELETE CASCADE,
    medicine_name       VARCHAR(150) NOT NULL,
    dosage              VARCHAR(50) NOT NULL,
    frequency           VARCHAR(30) NOT NULL,
    duration_days       SMALLINT NOT NULL CHECK (duration_days BETWEEN 1 AND 180),
    instructions_en     VARCHAR(150) NOT NULL,
    instructions_kn     VARCHAR(150),
    is_dispensed        BOOLEAN NOT NULL DEFAULT FALSE,
    dispensed_at        TIMESTAMPTZ,
    dispensed_by        VARCHAR(36) REFERENCES users(user_id),
    batch_issued        VARCHAR(30)
);

-- ====================================================================
-- 9. LAB ORDERS & RESULTS
-- ====================================================================
CREATE TABLE lab_orders (
    order_id            VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    visit_id            VARCHAR(36) NOT NULL REFERENCES visits(visit_id) ON DELETE CASCADE,
    test_name           VARCHAR(100) NOT NULL,
    status              VARCHAR(25) NOT NULL CHECK (status IN ('ORDERED', 'SAMPLE_COLLECTED', 'PROCESSING', 'RESULT_READY')) DEFAULT 'ORDERED',
    result_value        TEXT,
    interpretation      VARCHAR(20) CHECK (interpretation IN ('NORMAL', 'ABNORMAL_HIGH', 'ABNORMAL_LOW', 'POSITIVE', 'NEGATIVE')),
    verified_by_user_id VARCHAR(36) REFERENCES users(user_id),
    ordered_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at        TIMESTAMPTZ
);

-- ====================================================================
-- 10. REFERRALS
-- ====================================================================
CREATE TABLE referrals (
    referral_id         VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    visit_id            VARCHAR(36) NOT NULL REFERENCES visits(visit_id) ON DELETE CASCADE,
    patient_id          VARCHAR(36) NOT NULL REFERENCES patients(patient_id) ON DELETE RESTRICT,
    destination_facility VARCHAR(150) NOT NULL,
    clinical_reason     TEXT NOT NULL,
    urgency             VARCHAR(15) NOT NULL CHECK (urgency IN ('ROUTINE', 'PRIORITY', 'EMERGENCY')),
    status              VARCHAR(20) NOT NULL CHECK (status IN ('OPEN', 'ACKNOWLEDGED', 'CLOSED', 'EXPIRED')) DEFAULT 'OPEN',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at           TIMESTAMPTZ
);

-- ====================================================================
-- 11. ACCESS AUDIT LOGS (PARTITIONED BY MONTH FOR HIGH PERFORMANCE)
-- ====================================================================
CREATE TABLE access_audit_logs (
    audit_event_id      VARCHAR(36) DEFAULT uuid_generate_v4()::text,
    timestamp_utc       TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id             VARCHAR(36) NOT NULL,
    user_role           VARCHAR(25) NOT NULL,
    clinic_id           VARCHAR(20),
    patient_id          VARCHAR(36),
    action_category     VARCHAR(30) NOT NULL,
    resource_type       VARCHAR(30) NOT NULL,
    resource_id         VARCHAR(36),
    client_ip           VARCHAR(45) NOT NULL,
    prev_record_hash    VARCHAR(64) NOT NULL,
    current_hash        VARCHAR(64) NOT NULL,
    PRIMARY KEY (audit_event_id, timestamp_utc)
) PARTITION BY RANGE (timestamp_utc);

-- Partition for 2026
CREATE TABLE audit_logs_2026_q3 PARTITION OF access_audit_logs
    FOR VALUES FROM ('2026-07-01 00:00:00+00') TO ('2026-10-01 00:00:00+00');
CREATE TABLE audit_logs_2026_q4 PARTITION OF access_audit_logs
    FOR VALUES FROM ('2026-10-01 00:00:00+00') TO ('2027-01-01 00:00:00+00');
```

---

## 3. Database Migration Strategy

1. **Tooling:** Managed with **Prisma / Flyway / node-pg-migrate** executing forward SQL migrations (`V1__baseline.sql`, `V2__seed_masters.sql`).
2. **Zero-Downtime Releases:** Column additions are always nullable or accompanied by safe default values. Column renames or drops follow a multi-step deprecation cycle across two consecutive sprints.
3. **Automated Testing:** CI/CD pipeline spins up a transient PostgreSQL container on every Pull Request, runs all migrations from scratch, verifies foreign key constraints, and seeds synthetic mock patients.
