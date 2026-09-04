# 📊 Architecture Document 11: Public Health Analytics & Epidemiological Intelligence Specification
## Namma Clinic Digital Health & Operations Platform
### Greater Bengaluru Authority (GBA) / BBMP Health Department
**Standard:** Real-Time CDC / ClickHouse Columnar / Star Schema / Apache Superset | **Status:** APPROVED BASELINE | **Code:** `ARCH-ANL-11`

---

## 01. Document Overview & Analytical Philosophy
This document specifies the municipal public health analytics, change data capture (CDC) pipelines, columnar storage schemas, epidemiological surveillance engines, and business intelligence architectures for the Namma Clinic Digital Health & Operations Platform. Serving 183 primary clinics across Greater Bengaluru Authority (GBA), the platform transitions municipal healthcare governance from retrospective monthly paperwork into near-real-time epidemiological situational awareness.

### 01.1 Core Analytics Invariants & Design Principles
1. **Zero-Impact on Operational OLTP:** Analytical aggregations and heavy dashboard queries are completely decoupled from production PostgreSQL databases using streaming Change Data Capture (CDC) into an isolated ClickHouse columnar cluster.
2. **Sub-Second Municipal Query Latency:** Analytical queries spanning millions of clinical encounters across 183 clinics must execute in < 1,000ms via ClickHouse vector-oriented columnar execution.
3. **Differential Privacy & k-Anonymity (k >= 5):** Public dashboards enforce k-anonymity; any demographic or disease query returning fewer than 5 citizens in a municipal ward is automatically suppressed or blurred.
4. **Spatial-Temporal Epidemiological Granularity:** All clinical encounters, fever syndromes, and diagnostic lab confirmations are indexed by BBMP Zone, Ward (1-225), and UTC timestamp, enabling micro-cluster outbreak detection.
5. **Continuous Syndromic Fever Anomaly Detection:** Real-time Poisson and CUSUM statistical anomaly detectors monitor daily footfall to alert municipal epidemiologists to emergent dengue, chikungunya, or cholera clusters.
6. **Standardized Public Health Indicators:** Metrics conform strictly to National Health Mission (NHM), WHO Primary Healthcare Guidelines, and Karnataka State HMIS definitions.

## 02. End-to-End Real-Time CDC Architecture (Debezium + Kafka + ClickHouse)
Data streaming architecture pipeline offloading operational events into analytical storage:
```
 +-------------------+     WAL Streaming     +--------------------+     Avro Events     +---------------------+
 | Central PostgreSQL| -------------------> |  Debezium Engine   | -------------------> | Apache Kafka Topics |
 | (Port 5432)       |  Logical Decoding    |  (Kafka Connect)   |   Snappy Compressed  | (24 Partitions)     |
 +-------------------+                      +--------------------+                      +---------------------+
                                                                                                   |
                                                                                            Micro-batch Poll
                                                                                           (Every 2,000ms)
                                                                                                   v
 +-------------------+     Visual Queries   +--------------------+     Vectorized SQL   +---------------------+
 |  Apache Superset  | <------------------- |  ClickHouse OLAP   | <------------------- | Kafka Connect Sink  |
 |  (Municipal BI)   |   Sub-second Render  |  (ReplacingMerge)  |   Block Ingestion    | (ClickHouse Driver) |
 +-------------------+                      +--------------------+                      +---------------------+
```

## 03. Canonical Star Schema: 12 Analytical Fact Tables
Exhaustive ClickHouse DDL table definitions, Kafka ingestion topics, materialized views, and sorting indices for 12 fact tables:

### 03.01 Fact Table Specification: `fact_consultations`
- **Table Identifier:** `analytics.fact_consultations`
- **Business Grain:** Individual clinical outpatient consultation episodes.
- **ClickHouse Storage Engine:** `ReplacingMergeTree(version)`
- **Partitioning Key:** `toYYYYMM(event_date)`
- **CDC Kafka Ingestion Topic:** `cdc.namma.consultations`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.fact_consultations (
    encounter_id UUID,
    clinic_id LowCardinality(String),
    zone_id LowCardinality(String),
    ward_number UInt16,
    doctor_id UUID,
    patient_id UUID,
    patient_age UInt8,
    patient_gender LowCardinality(String),
    primary_icd10 LowCardinality(String),
    primary_snomed UInt64,
    consultation_duration_seconds UInt16,
    systolic_bp UInt16,
    diastolic_bp UInt16,
    mews_score UInt8,
    prescribed_drugs_count UInt8,
    antibiotic_prescribed UInt8,
    lab_investigations_count UInt8,
    referred_secondary UInt8,
    event_timestamp DateTime64(3, 'UTC'),
    event_date Date DEFAULT toDate(event_timestamp),
    version UInt64
) ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_date)
ORDER BY (zone_id, ward_number, clinic_id, event_date, encounter_id);
```

#### Kafka Connect Avro Schema Contract:
```json
{
  "type": "record",
  "name": "fact_consultationsEvent",
  "namespace": "in.gov.bbmp.namma.analytics",
  "fields": [
    { "name": "eventId", "type": "string", "logicalType": "uuid" },
    { "name": "clinicId", "type": "string" },
    { "name": "zoneId", "type": "string" },
    { "name": "eventTimestamp", "type": "long", "logicalType": "timestamp-millis" },
    { "name": "payload", "type": "string" },
    { "name": "version", "type": "long" }
  ]
}
```

#### Materialized View Aggregation Definition:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_hourly_fact_consultations (
    clinic_id LowCardinality(String),
    event_hour DateTime,
    total_records UInt32
) ENGINE = SummingMergeTree()
ORDER BY (clinic_id, event_hour) AS
SELECT
    clinic_id,
    toStartOfHour(event_timestamp) AS event_hour,
    count() AS total_records
FROM analytics.fact_consultations
GROUP BY clinic_id, event_hour;
```

#### Indexing & Vectorized Query Optimization:
1. Primary key sorting enables skip-index scans on zone, ward, and clinic prefixes.
2. LowCardinality dictionary encoding reduces string storage footprints by up to 85%.
3. Native integer timestamps allow sub-second SIMD vectorized aggregations.
4. Table data retention: Hot tier on NVMe SSD for 180 days; cold archival to S3-compatible object store after 2 years.

---

### 03.02 Fact Table Specification: `fact_dispensations`
- **Table Identifier:** `analytics.fact_dispensations`
- **Business Grain:** Line-item drug dispensations from clinic pharmacies.
- **ClickHouse Storage Engine:** `ReplacingMergeTree(version)`
- **Partitioning Key:** `toYYYYMM(event_date)`
- **CDC Kafka Ingestion Topic:** `cdc.namma.dispensations`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.fact_dispensations (
    dispensation_id UUID,
    clinic_id LowCardinality(String),
    zone_id LowCardinality(String),
    ward_number UInt16,
    pharmacist_id UUID,
    patient_id UUID,
    drug_id LowCardinality(String),
    batch_number String,
    expiry_date Date,
    quantity_dispensed UInt16,
    unit_cost_paise UInt32,
    total_cost_paise UInt32,
    is_fefo_compliant UInt8,
    barcode_scanned UInt8,
    event_timestamp DateTime64(3, 'UTC'),
    event_date Date DEFAULT toDate(event_timestamp),
    version UInt64
) ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_date)
ORDER BY (zone_id, clinic_id, drug_id, event_date, dispensation_id);
```

#### Kafka Connect Avro Schema Contract:
```json
{
  "type": "record",
  "name": "fact_dispensationsEvent",
  "namespace": "in.gov.bbmp.namma.analytics",
  "fields": [
    { "name": "eventId", "type": "string", "logicalType": "uuid" },
    { "name": "clinicId", "type": "string" },
    { "name": "zoneId", "type": "string" },
    { "name": "eventTimestamp", "type": "long", "logicalType": "timestamp-millis" },
    { "name": "payload", "type": "string" },
    { "name": "version", "type": "long" }
  ]
}
```

#### Materialized View Aggregation Definition:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_hourly_fact_dispensations (
    clinic_id LowCardinality(String),
    event_hour DateTime,
    total_records UInt32
) ENGINE = SummingMergeTree()
ORDER BY (clinic_id, event_hour) AS
SELECT
    clinic_id,
    toStartOfHour(event_timestamp) AS event_hour,
    count() AS total_records
FROM analytics.fact_dispensations
GROUP BY clinic_id, event_hour;
```

#### Indexing & Vectorized Query Optimization:
1. Primary key sorting enables skip-index scans on zone, ward, and clinic prefixes.
2. LowCardinality dictionary encoding reduces string storage footprints by up to 85%.
3. Native integer timestamps allow sub-second SIMD vectorized aggregations.
4. Table data retention: Hot tier on NVMe SSD for 180 days; cold archival to S3-compatible object store after 2 years.

---

### 03.03 Fact Table Specification: `fact_lab_investigations`
- **Table Identifier:** `analytics.fact_lab_investigations`
- **Business Grain:** Diagnostic point-of-care lab test results (58 panels).
- **ClickHouse Storage Engine:** `ReplacingMergeTree(version)`
- **Partitioning Key:** `toYYYYMM(event_date)`
- **CDC Kafka Ingestion Topic:** `cdc.namma.lab_investigations`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.fact_lab_investigations (
    order_id UUID,
    clinic_id LowCardinality(String),
    zone_id LowCardinality(String),
    ward_number UInt16,
    technician_id UUID,
    patient_id UUID,
    test_code LowCardinality(String),
    loinc_code LowCardinality(String),
    result_numeric Float32,
    result_text LowCardinality(String),
    is_abnormal UInt8,
    is_panic_value UInt8,
    turnaround_time_seconds UInt16,
    event_timestamp DateTime64(3, 'UTC'),
    event_date Date DEFAULT toDate(event_timestamp),
    version UInt64
) ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_date)
ORDER BY (zone_id, clinic_id, test_code, is_panic_value, event_date, order_id);
```

#### Kafka Connect Avro Schema Contract:
```json
{
  "type": "record",
  "name": "fact_lab_investigationsEvent",
  "namespace": "in.gov.bbmp.namma.analytics",
  "fields": [
    { "name": "eventId", "type": "string", "logicalType": "uuid" },
    { "name": "clinicId", "type": "string" },
    { "name": "zoneId", "type": "string" },
    { "name": "eventTimestamp", "type": "long", "logicalType": "timestamp-millis" },
    { "name": "payload", "type": "string" },
    { "name": "version", "type": "long" }
  ]
}
```

#### Materialized View Aggregation Definition:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_hourly_fact_lab_investigations (
    clinic_id LowCardinality(String),
    event_hour DateTime,
    total_records UInt32
) ENGINE = SummingMergeTree()
ORDER BY (clinic_id, event_hour) AS
SELECT
    clinic_id,
    toStartOfHour(event_timestamp) AS event_hour,
    count() AS total_records
FROM analytics.fact_lab_investigations
GROUP BY clinic_id, event_hour;
```

#### Indexing & Vectorized Query Optimization:
1. Primary key sorting enables skip-index scans on zone, ward, and clinic prefixes.
2. LowCardinality dictionary encoding reduces string storage footprints by up to 85%.
3. Native integer timestamps allow sub-second SIMD vectorized aggregations.
4. Table data retention: Hot tier on NVMe SSD for 180 days; cold archival to S3-compatible object store after 2 years.

---

### 03.04 Fact Table Specification: `fact_queue_waits`
- **Table Identifier:** `analytics.fact_queue_waits`
- **Business Grain:** Patient waiting durations across clinic journey stations.
- **ClickHouse Storage Engine:** `ReplacingMergeTree(version)`
- **Partitioning Key:** `toYYYYMM(event_date)`
- **CDC Kafka Ingestion Topic:** `cdc.namma.queue_waits`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.fact_queue_waits (
    token_id UUID,
    clinic_id LowCardinality(String),
    zone_id LowCardinality(String),
    ward_number UInt16,
    registration_wait_seconds UInt16,
    triage_wait_seconds UInt16,
    doctor_wait_seconds UInt16,
    pharmacy_wait_seconds UInt16,
    lab_wait_seconds UInt16,
    total_clinic_duration_seconds UInt16,
    priority_category LowCardinality(String),
    event_timestamp DateTime64(3, 'UTC'),
    event_date Date DEFAULT toDate(event_timestamp),
    version UInt64
) ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_date)
ORDER BY (zone_id, clinic_id, priority_category, event_date, token_id);
```

#### Kafka Connect Avro Schema Contract:
```json
{
  "type": "record",
  "name": "fact_queue_waitsEvent",
  "namespace": "in.gov.bbmp.namma.analytics",
  "fields": [
    { "name": "eventId", "type": "string", "logicalType": "uuid" },
    { "name": "clinicId", "type": "string" },
    { "name": "zoneId", "type": "string" },
    { "name": "eventTimestamp", "type": "long", "logicalType": "timestamp-millis" },
    { "name": "payload", "type": "string" },
    { "name": "version", "type": "long" }
  ]
}
```

#### Materialized View Aggregation Definition:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_hourly_fact_queue_waits (
    clinic_id LowCardinality(String),
    event_hour DateTime,
    total_records UInt32
) ENGINE = SummingMergeTree()
ORDER BY (clinic_id, event_hour) AS
SELECT
    clinic_id,
    toStartOfHour(event_timestamp) AS event_hour,
    count() AS total_records
FROM analytics.fact_queue_waits
GROUP BY clinic_id, event_hour;
```

#### Indexing & Vectorized Query Optimization:
1. Primary key sorting enables skip-index scans on zone, ward, and clinic prefixes.
2. LowCardinality dictionary encoding reduces string storage footprints by up to 85%.
3. Native integer timestamps allow sub-second SIMD vectorized aggregations.
4. Table data retention: Hot tier on NVMe SSD for 180 days; cold archival to S3-compatible object store after 2 years.

---

### 03.05 Fact Table Specification: `fact_stock_movements`
- **Table Identifier:** `analytics.fact_stock_movements`
- **Business Grain:** Pharmacy inventory receipts, adjustments, and burn rates.
- **ClickHouse Storage Engine:** `ReplacingMergeTree(version)`
- **Partitioning Key:** `toYYYYMM(event_date)`
- **CDC Kafka Ingestion Topic:** `cdc.namma.stock_movements`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.fact_stock_movements (
    movement_id UUID,
    clinic_id LowCardinality(String),
    zone_id LowCardinality(String),
    drug_id LowCardinality(String),
    batch_number String,
    movement_type LowCardinality(String),
    quantity Int32,
    balance_after UInt32,
    days_to_expiry Int16,
    event_timestamp DateTime64(3, 'UTC'),
    event_date Date DEFAULT toDate(event_timestamp),
    version UInt64
) ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_date)
ORDER BY (zone_id, clinic_id, drug_id, event_date, movement_id);
```

#### Kafka Connect Avro Schema Contract:
```json
{
  "type": "record",
  "name": "fact_stock_movementsEvent",
  "namespace": "in.gov.bbmp.namma.analytics",
  "fields": [
    { "name": "eventId", "type": "string", "logicalType": "uuid" },
    { "name": "clinicId", "type": "string" },
    { "name": "zoneId", "type": "string" },
    { "name": "eventTimestamp", "type": "long", "logicalType": "timestamp-millis" },
    { "name": "payload", "type": "string" },
    { "name": "version", "type": "long" }
  ]
}
```

#### Materialized View Aggregation Definition:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_hourly_fact_stock_movements (
    clinic_id LowCardinality(String),
    event_hour DateTime,
    total_records UInt32
) ENGINE = SummingMergeTree()
ORDER BY (clinic_id, event_hour) AS
SELECT
    clinic_id,
    toStartOfHour(event_timestamp) AS event_hour,
    count() AS total_records
FROM analytics.fact_stock_movements
GROUP BY clinic_id, event_hour;
```

#### Indexing & Vectorized Query Optimization:
1. Primary key sorting enables skip-index scans on zone, ward, and clinic prefixes.
2. LowCardinality dictionary encoding reduces string storage footprints by up to 85%.
3. Native integer timestamps allow sub-second SIMD vectorized aggregations.
4. Table data retention: Hot tier on NVMe SSD for 180 days; cold archival to S3-compatible object store after 2 years.

---

### 03.06 Fact Table Specification: `fact_citizen_feedback`
- **Table Identifier:** `analytics.fact_citizen_feedback`
- **Business Grain:** Citizen ratings and grievance filings across kiosk tablets.
- **ClickHouse Storage Engine:** `ReplacingMergeTree(version)`
- **Partitioning Key:** `toYYYYMM(event_date)`
- **CDC Kafka Ingestion Topic:** `cdc.namma.citizen_feedback`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.fact_citizen_feedback (
    feedback_id UUID,
    clinic_id LowCardinality(String),
    zone_id LowCardinality(String),
    ward_number UInt16,
    star_rating UInt8,
    cleanliness_score UInt8,
    staff_behavior_score UInt8,
    medicine_availability_score UInt8,
    grievance_filed UInt8,
    grievance_category LowCardinality(String),
    event_timestamp DateTime64(3, 'UTC'),
    event_date Date DEFAULT toDate(event_timestamp),
    version UInt64
) ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_date)
ORDER BY (zone_id, clinic_id, star_rating, event_date, feedback_id);
```

#### Kafka Connect Avro Schema Contract:
```json
{
  "type": "record",
  "name": "fact_citizen_feedbackEvent",
  "namespace": "in.gov.bbmp.namma.analytics",
  "fields": [
    { "name": "eventId", "type": "string", "logicalType": "uuid" },
    { "name": "clinicId", "type": "string" },
    { "name": "zoneId", "type": "string" },
    { "name": "eventTimestamp", "type": "long", "logicalType": "timestamp-millis" },
    { "name": "payload", "type": "string" },
    { "name": "version", "type": "long" }
  ]
}
```

#### Materialized View Aggregation Definition:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_hourly_fact_citizen_feedback (
    clinic_id LowCardinality(String),
    event_hour DateTime,
    total_records UInt32
) ENGINE = SummingMergeTree()
ORDER BY (clinic_id, event_hour) AS
SELECT
    clinic_id,
    toStartOfHour(event_timestamp) AS event_hour,
    count() AS total_records
FROM analytics.fact_citizen_feedback
GROUP BY clinic_id, event_hour;
```

#### Indexing & Vectorized Query Optimization:
1. Primary key sorting enables skip-index scans on zone, ward, and clinic prefixes.
2. LowCardinality dictionary encoding reduces string storage footprints by up to 85%.
3. Native integer timestamps allow sub-second SIMD vectorized aggregations.
4. Table data retention: Hot tier on NVMe SSD for 180 days; cold archival to S3-compatible object store after 2 years.

---

### 03.07 Fact Table Specification: `fact_ncd_episodes`
- **Table Identifier:** `analytics.fact_ncd_episodes`
- **Business Grain:** Longitudinal chronic care management for hypertension and diabetes.
- **ClickHouse Storage Engine:** `ReplacingMergeTree(version)`
- **Partitioning Key:** `toYYYYMM(event_date)`
- **CDC Kafka Ingestion Topic:** `cdc.namma.ncd_episodes`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.fact_ncd_episodes (
    episode_id UUID,
    clinic_id LowCardinality(String),
    zone_id LowCardinality(String),
    ward_number UInt16,
    patient_id UUID,
    condition_code LowCardinality(String), -- HYPERTENSION, DIABETES, DUAL
    is_controlled UInt8,
    latest_systolic_bp UInt16,
    latest_diastolic_bp UInt16,
    latest_rbs Float32,
    days_since_last_visit UInt16,
    is_defaulter UInt8,
    outreach_contacted UInt8,
    event_timestamp DateTime64(3, 'UTC'),
    event_date Date DEFAULT toDate(event_timestamp),
    version UInt64
) ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_date)
ORDER BY (zone_id, ward_number, condition_code, is_defaulter, event_date, episode_id);
```

#### Kafka Connect Avro Schema Contract:
```json
{
  "type": "record",
  "name": "fact_ncd_episodesEvent",
  "namespace": "in.gov.bbmp.namma.analytics",
  "fields": [
    { "name": "eventId", "type": "string", "logicalType": "uuid" },
    { "name": "clinicId", "type": "string" },
    { "name": "zoneId", "type": "string" },
    { "name": "eventTimestamp", "type": "long", "logicalType": "timestamp-millis" },
    { "name": "payload", "type": "string" },
    { "name": "version", "type": "long" }
  ]
}
```

#### Materialized View Aggregation Definition:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_hourly_fact_ncd_episodes (
    clinic_id LowCardinality(String),
    event_hour DateTime,
    total_records UInt32
) ENGINE = SummingMergeTree()
ORDER BY (clinic_id, event_hour) AS
SELECT
    clinic_id,
    toStartOfHour(event_timestamp) AS event_hour,
    count() AS total_records
FROM analytics.fact_ncd_episodes
GROUP BY clinic_id, event_hour;
```

#### Indexing & Vectorized Query Optimization:
1. Primary key sorting enables skip-index scans on zone, ward, and clinic prefixes.
2. LowCardinality dictionary encoding reduces string storage footprints by up to 85%.
3. Native integer timestamps allow sub-second SIMD vectorized aggregations.
4. Table data retention: Hot tier on NVMe SSD for 180 days; cold archival to S3-compatible object store after 2 years.

---

### 03.08 Fact Table Specification: `fact_maternal_antenatal`
- **Table Identifier:** `analytics.fact_maternal_antenatal`
- **Business Grain:** Maternal and child health antenatal checkup tracking.
- **ClickHouse Storage Engine:** `ReplacingMergeTree(version)`
- **Partitioning Key:** `toYYYYMM(event_date)`
- **CDC Kafka Ingestion Topic:** `cdc.namma.maternal_antenatal`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.fact_maternal_antenatal (
    anc_id UUID,
    clinic_id LowCardinality(String),
    zone_id LowCardinality(String),
    ward_number UInt16,
    mother_patient_id UUID,
    trimester UInt8,
    anc_visit_number UInt8,
    gestational_age_weeks UInt8,
    hemoglobin_level Float32,
    is_high_risk_pregnancy UInt8,
    tt_vaccine_given UInt8,
    ifa_tablets_dispensed UInt16,
    event_timestamp DateTime64(3, 'UTC'),
    event_date Date DEFAULT toDate(event_timestamp),
    version UInt64
) ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_date)
ORDER BY (zone_id, ward_number, is_high_risk_pregnancy, event_date, anc_id);
```

#### Kafka Connect Avro Schema Contract:
```json
{
  "type": "record",
  "name": "fact_maternal_antenatalEvent",
  "namespace": "in.gov.bbmp.namma.analytics",
  "fields": [
    { "name": "eventId", "type": "string", "logicalType": "uuid" },
    { "name": "clinicId", "type": "string" },
    { "name": "zoneId", "type": "string" },
    { "name": "eventTimestamp", "type": "long", "logicalType": "timestamp-millis" },
    { "name": "payload", "type": "string" },
    { "name": "version", "type": "long" }
  ]
}
```

#### Materialized View Aggregation Definition:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_hourly_fact_maternal_antenatal (
    clinic_id LowCardinality(String),
    event_hour DateTime,
    total_records UInt32
) ENGINE = SummingMergeTree()
ORDER BY (clinic_id, event_hour) AS
SELECT
    clinic_id,
    toStartOfHour(event_timestamp) AS event_hour,
    count() AS total_records
FROM analytics.fact_maternal_antenatal
GROUP BY clinic_id, event_hour;
```

#### Indexing & Vectorized Query Optimization:
1. Primary key sorting enables skip-index scans on zone, ward, and clinic prefixes.
2. LowCardinality dictionary encoding reduces string storage footprints by up to 85%.
3. Native integer timestamps allow sub-second SIMD vectorized aggregations.
4. Table data retention: Hot tier on NVMe SSD for 180 days; cold archival to S3-compatible object store after 2 years.

---

### 03.09 Fact Table Specification: `fact_child_immunizations`
- **Table Identifier:** `analytics.fact_child_immunizations`
- **Business Grain:** Pediatric vaccination administration cohort data.
- **ClickHouse Storage Engine:** `ReplacingMergeTree(version)`
- **Partitioning Key:** `toYYYYMM(event_date)`
- **CDC Kafka Ingestion Topic:** `cdc.namma.child_immunizations`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.fact_child_immunizations (
    immunization_id UUID,
    clinic_id LowCardinality(String),
    zone_id LowCardinality(String),
    ward_number UInt16,
    child_patient_id UUID,
    child_age_months UInt8,
    vaccine_code LowCardinality(String),
    dose_number UInt8,
    is_on_time UInt8,
    batch_number String,
    event_timestamp DateTime64(3, 'UTC'),
    event_date Date DEFAULT toDate(event_timestamp),
    version UInt64
) ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_date)
ORDER BY (zone_id, ward_number, vaccine_code, event_date, immunization_id);
```

#### Kafka Connect Avro Schema Contract:
```json
{
  "type": "record",
  "name": "fact_child_immunizationsEvent",
  "namespace": "in.gov.bbmp.namma.analytics",
  "fields": [
    { "name": "eventId", "type": "string", "logicalType": "uuid" },
    { "name": "clinicId", "type": "string" },
    { "name": "zoneId", "type": "string" },
    { "name": "eventTimestamp", "type": "long", "logicalType": "timestamp-millis" },
    { "name": "payload", "type": "string" },
    { "name": "version", "type": "long" }
  ]
}
```

#### Materialized View Aggregation Definition:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_hourly_fact_child_immunizations (
    clinic_id LowCardinality(String),
    event_hour DateTime,
    total_records UInt32
) ENGINE = SummingMergeTree()
ORDER BY (clinic_id, event_hour) AS
SELECT
    clinic_id,
    toStartOfHour(event_timestamp) AS event_hour,
    count() AS total_records
FROM analytics.fact_child_immunizations
GROUP BY clinic_id, event_hour;
```

#### Indexing & Vectorized Query Optimization:
1. Primary key sorting enables skip-index scans on zone, ward, and clinic prefixes.
2. LowCardinality dictionary encoding reduces string storage footprints by up to 85%.
3. Native integer timestamps allow sub-second SIMD vectorized aggregations.
4. Table data retention: Hot tier on NVMe SSD for 180 days; cold archival to S3-compatible object store after 2 years.

---

### 03.10 Fact Table Specification: `fact_emergency_referrals`
- **Table Identifier:** `analytics.fact_emergency_referrals`
- **Business Grain:** Emergency secondary referrals and 108 ambulance transits.
- **ClickHouse Storage Engine:** `ReplacingMergeTree(version)`
- **Partitioning Key:** `toYYYYMM(event_date)`
- **CDC Kafka Ingestion Topic:** `cdc.namma.emergency_referrals`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.fact_emergency_referrals (
    referral_id UUID,
    clinic_id LowCardinality(String),
    zone_id LowCardinality(String),
    destination_hospital_name LowCardinality(String),
    triage_priority LowCardinality(String), -- RED, YELLOW, GREEN
    primary_condition LowCardinality(String),
    cad_108_dispatched UInt8,
    ambulance_transit_duration_seconds UInt16,
    counter_referral_received UInt8,
    event_timestamp DateTime64(3, 'UTC'),
    event_date Date DEFAULT toDate(event_timestamp),
    version UInt64
) ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_date)
ORDER BY (zone_id, clinic_id, triage_priority, event_date, referral_id);
```

#### Kafka Connect Avro Schema Contract:
```json
{
  "type": "record",
  "name": "fact_emergency_referralsEvent",
  "namespace": "in.gov.bbmp.namma.analytics",
  "fields": [
    { "name": "eventId", "type": "string", "logicalType": "uuid" },
    { "name": "clinicId", "type": "string" },
    { "name": "zoneId", "type": "string" },
    { "name": "eventTimestamp", "type": "long", "logicalType": "timestamp-millis" },
    { "name": "payload", "type": "string" },
    { "name": "version", "type": "long" }
  ]
}
```

#### Materialized View Aggregation Definition:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_hourly_fact_emergency_referrals (
    clinic_id LowCardinality(String),
    event_hour DateTime,
    total_records UInt32
) ENGINE = SummingMergeTree()
ORDER BY (clinic_id, event_hour) AS
SELECT
    clinic_id,
    toStartOfHour(event_timestamp) AS event_hour,
    count() AS total_records
FROM analytics.fact_emergency_referrals
GROUP BY clinic_id, event_hour;
```

#### Indexing & Vectorized Query Optimization:
1. Primary key sorting enables skip-index scans on zone, ward, and clinic prefixes.
2. LowCardinality dictionary encoding reduces string storage footprints by up to 85%.
3. Native integer timestamps allow sub-second SIMD vectorized aggregations.
4. Table data retention: Hot tier on NVMe SSD for 180 days; cold archival to S3-compatible object store after 2 years.

---

### 03.11 Fact Table Specification: `fact_telemedicine_sessions`
- **Table Identifier:** `analytics.fact_telemedicine_sessions`
- **Business Grain:** Specialist tele-consultation video encounter sessions.
- **ClickHouse Storage Engine:** `ReplacingMergeTree(version)`
- **Partitioning Key:** `toYYYYMM(event_date)`
- **CDC Kafka Ingestion Topic:** `cdc.namma.telemedicine_sessions`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.fact_telemedicine_sessions (
    session_id UUID,
    clinic_id LowCardinality(String),
    specialist_hospital_id LowCardinality(String),
    specialty_domain LowCardinality(String),
    call_duration_seconds UInt16,
    connection_quality_score UInt8,
    management_plan_modified UInt8,
    event_timestamp DateTime64(3, 'UTC'),
    event_date Date DEFAULT toDate(event_timestamp),
    version UInt64
) ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_date)
ORDER BY (specialty_domain, clinic_id, event_date, session_id);
```

#### Kafka Connect Avro Schema Contract:
```json
{
  "type": "record",
  "name": "fact_telemedicine_sessionsEvent",
  "namespace": "in.gov.bbmp.namma.analytics",
  "fields": [
    { "name": "eventId", "type": "string", "logicalType": "uuid" },
    { "name": "clinicId", "type": "string" },
    { "name": "zoneId", "type": "string" },
    { "name": "eventTimestamp", "type": "long", "logicalType": "timestamp-millis" },
    { "name": "payload", "type": "string" },
    { "name": "version", "type": "long" }
  ]
}
```

#### Materialized View Aggregation Definition:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_hourly_fact_telemedicine_sessions (
    clinic_id LowCardinality(String),
    event_hour DateTime,
    total_records UInt32
) ENGINE = SummingMergeTree()
ORDER BY (clinic_id, event_hour) AS
SELECT
    clinic_id,
    toStartOfHour(event_timestamp) AS event_hour,
    count() AS total_records
FROM analytics.fact_telemedicine_sessions
GROUP BY clinic_id, event_hour;
```

#### Indexing & Vectorized Query Optimization:
1. Primary key sorting enables skip-index scans on zone, ward, and clinic prefixes.
2. LowCardinality dictionary encoding reduces string storage footprints by up to 85%.
3. Native integer timestamps allow sub-second SIMD vectorized aggregations.
4. Table data retention: Hot tier on NVMe SSD for 180 days; cold archival to S3-compatible object store after 2 years.

---

### 03.12 Fact Table Specification: `fact_biomedical_waste`
- **Table Identifier:** `analytics.fact_biomedical_waste`
- **Business Grain:** Daily facility bio-medical waste segregation and disposal logs.
- **ClickHouse Storage Engine:** `ReplacingMergeTree(version)`
- **Partitioning Key:** `toYYYYMM(event_date)`
- **CDC Kafka Ingestion Topic:** `cdc.namma.biomedical_waste`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.fact_biomedical_waste (
    log_id UUID,
    clinic_id LowCardinality(String),
    zone_id LowCardinality(String),
    yellow_bag_kg Float32, -- Anatomical & soiled
    red_bag_kg Float32,    -- Contaminated plastics
    white_box_kg Float32,  -- Sharps
    blue_cardboard_kg Float32, -- Glassware
    is_manifest_signed UInt8,
    collector_vehicle_id String,
    event_timestamp DateTime64(3, 'UTC'),
    event_date Date DEFAULT toDate(event_timestamp),
    version UInt64
) ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_date)
ORDER BY (zone_id, clinic_id, event_date, log_id);
```

#### Kafka Connect Avro Schema Contract:
```json
{
  "type": "record",
  "name": "fact_biomedical_wasteEvent",
  "namespace": "in.gov.bbmp.namma.analytics",
  "fields": [
    { "name": "eventId", "type": "string", "logicalType": "uuid" },
    { "name": "clinicId", "type": "string" },
    { "name": "zoneId", "type": "string" },
    { "name": "eventTimestamp", "type": "long", "logicalType": "timestamp-millis" },
    { "name": "payload", "type": "string" },
    { "name": "version", "type": "long" }
  ]
}
```

#### Materialized View Aggregation Definition:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_hourly_fact_biomedical_waste (
    clinic_id LowCardinality(String),
    event_hour DateTime,
    total_records UInt32
) ENGINE = SummingMergeTree()
ORDER BY (clinic_id, event_hour) AS
SELECT
    clinic_id,
    toStartOfHour(event_timestamp) AS event_hour,
    count() AS total_records
FROM analytics.fact_biomedical_waste
GROUP BY clinic_id, event_hour;
```

#### Indexing & Vectorized Query Optimization:
1. Primary key sorting enables skip-index scans on zone, ward, and clinic prefixes.
2. LowCardinality dictionary encoding reduces string storage footprints by up to 85%.
3. Native integer timestamps allow sub-second SIMD vectorized aggregations.
4. Table data retention: Hot tier on NVMe SSD for 180 days; cold archival to S3-compatible object store after 2 years.

---

## 04. Canonical Star Schema: 8 Analytical Dimension Tables
ClickHouse dimension schemas providing contextual slicing and hierarchical aggregation:

### 04.1 Dimension Table Specification: `dim_clinics`
- **Dimension Identifier:** `analytics.dim_clinics`
- **Scope & Purpose:** Namma Clinic facilities, geographical coordinates, zone, ward, and operational tier.
- **Storage Engine:** `ReplacingMergeTree(version)`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.dim_clinics (
    clinic_id String,
    clinic_name String,
    zone_id LowCardinality(String),
    zone_name LowCardinality(String),
    ward_number UInt16,
    ward_name String,
    latitude Float64,
    longitude Float64,
    pin_code UInt32,
    operational_status LowCardinality(String),
    commissioned_date Date,
    version UInt64
) ENGINE = ReplacingMergeTree(version)
ORDER BY (zone_id, ward_number, clinic_id);
```

#### SCD Type 2 Historical Synchronization Strategy:
```sql
-- Incremental merge query for dim_clinics
INSERT INTO analytics.dim_clinics
SELECT
    *,
    toUInt64(toUnixTimestamp64Milli(now64())) AS version
FROM staging.stg_dim_clinics
WHERE updated_at > (SELECT max(version) FROM analytics.{d[0]});
```

#### Governance, Indexing & Data Refresh Cadence:
1. Seed fixtures loaded during clinic commissioning; delta updates synced every 15 minutes.
2. LowCardinality dictionary compaction executed nightly via `OPTIMIZE TABLE analytics.dim_clinics FINAL;`.
3. Referential integrity validated in CI via cross-table consistency checks.

#### Canonical Analytical Slice Query Blueprint:
```sql
-- Slicing fact records by dim_clinics
SELECT
    d.*,
    count() AS total_activity_records,
    uniqExact(c.patient_id) AS distinct_patients_reached
FROM analytics.fact_consultations c
JOIN analytics.dim_clinics d ON c.zone_id = d.zone_id
WHERE c.event_date >= today() - 30
GROUP BY ALL
ORDER BY total_activity_records DESC
LIMIT 50;
```

---

### 04.2 Dimension Table Specification: `dim_drugs`
- **Dimension Identifier:** `analytics.dim_drugs`
- **Scope & Purpose:** Essential medicines formulary catalog, therapeutic categories, and dosage forms.
- **Storage Engine:** `ReplacingMergeTree(version)`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.dim_drugs (
    drug_id String,
    generic_name String,
    brand_aliases Array(String),
    therapeutic_category LowCardinality(String),
    who_aware_class LowCardinality(String), -- ACCESS, WATCH, RESERVE
    dosage_form LowCardinality(String),
    strength String,
    unit_price_paise UInt32,
    is_essential UInt8,
    version UInt64
) ENGINE = ReplacingMergeTree(version)
ORDER BY (who_aware_class, therapeutic_category, drug_id);
```

#### SCD Type 2 Historical Synchronization Strategy:
```sql
-- Incremental merge query for dim_drugs
INSERT INTO analytics.dim_drugs
SELECT
    *,
    toUInt64(toUnixTimestamp64Milli(now64())) AS version
FROM staging.stg_dim_drugs
WHERE updated_at > (SELECT max(version) FROM analytics.{d[0]});
```

#### Governance, Indexing & Data Refresh Cadence:
1. Seed fixtures loaded during clinic commissioning; delta updates synced every 15 minutes.
2. LowCardinality dictionary compaction executed nightly via `OPTIMIZE TABLE analytics.dim_drugs FINAL;`.
3. Referential integrity validated in CI via cross-table consistency checks.

#### Canonical Analytical Slice Query Blueprint:
```sql
-- Slicing fact records by dim_drugs
SELECT
    d.*,
    count() AS total_activity_records,
    uniqExact(c.patient_id) AS distinct_patients_reached
FROM analytics.fact_consultations c
JOIN analytics.dim_drugs d ON c.zone_id = d.zone_id
WHERE c.event_date >= today() - 30
GROUP BY ALL
ORDER BY total_activity_records DESC
LIMIT 50;
```

---

### 04.3 Dimension Table Specification: `dim_diagnoses`
- **Dimension Identifier:** `analytics.dim_diagnoses`
- **Scope & Purpose:** Dual-coded clinical diagnoses hierarchy mapping SNOMED CT to ICD-10.
- **Storage Engine:** `ReplacingMergeTree(version)`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.dim_diagnoses (
    snomed_concept_id UInt64,
    icd10_code LowCardinality(String),
    diagnosis_name String,
    syndrome_category LowCardinality(String), -- FEVER, RESPIRATORY, DIARRHEA, NCD, MCH
    is_notifiable_disease UInt8,
    version UInt64
) ENGINE = ReplacingMergeTree(version)
ORDER BY (syndrome_category, icd10_code, snomed_concept_id);
```

#### SCD Type 2 Historical Synchronization Strategy:
```sql
-- Incremental merge query for dim_diagnoses
INSERT INTO analytics.dim_diagnoses
SELECT
    *,
    toUInt64(toUnixTimestamp64Milli(now64())) AS version
FROM staging.stg_dim_diagnoses
WHERE updated_at > (SELECT max(version) FROM analytics.{d[0]});
```

#### Governance, Indexing & Data Refresh Cadence:
1. Seed fixtures loaded during clinic commissioning; delta updates synced every 15 minutes.
2. LowCardinality dictionary compaction executed nightly via `OPTIMIZE TABLE analytics.dim_diagnoses FINAL;`.
3. Referential integrity validated in CI via cross-table consistency checks.

#### Canonical Analytical Slice Query Blueprint:
```sql
-- Slicing fact records by dim_diagnoses
SELECT
    d.*,
    count() AS total_activity_records,
    uniqExact(c.patient_id) AS distinct_patients_reached
FROM analytics.fact_consultations c
JOIN analytics.dim_diagnoses d ON c.zone_id = d.zone_id
WHERE c.event_date >= today() - 30
GROUP BY ALL
ORDER BY total_activity_records DESC
LIMIT 50;
```

---

### 04.4 Dimension Table Specification: `dim_staff`
- **Dimension Identifier:** `analytics.dim_staff`
- **Scope & Purpose:** Clinical and administrative personnel directory and qualifications.
- **Storage Engine:** `ReplacingMergeTree(version)`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.dim_staff (
    staff_id UUID,
    staff_role LowCardinality(String),
    qualification LowCardinality(String),
    primary_clinic_id LowCardinality(String),
    is_active UInt8,
    version UInt64
) ENGINE = ReplacingMergeTree(version)
ORDER BY (staff_role, primary_clinic_id, staff_id);
```

#### SCD Type 2 Historical Synchronization Strategy:
```sql
-- Incremental merge query for dim_staff
INSERT INTO analytics.dim_staff
SELECT
    *,
    toUInt64(toUnixTimestamp64Milli(now64())) AS version
FROM staging.stg_dim_staff
WHERE updated_at > (SELECT max(version) FROM analytics.{d[0]});
```

#### Governance, Indexing & Data Refresh Cadence:
1. Seed fixtures loaded during clinic commissioning; delta updates synced every 15 minutes.
2. LowCardinality dictionary compaction executed nightly via `OPTIMIZE TABLE analytics.dim_staff FINAL;`.
3. Referential integrity validated in CI via cross-table consistency checks.

#### Canonical Analytical Slice Query Blueprint:
```sql
-- Slicing fact records by dim_staff
SELECT
    d.*,
    count() AS total_activity_records,
    uniqExact(c.patient_id) AS distinct_patients_reached
FROM analytics.fact_consultations c
JOIN analytics.dim_staff d ON c.zone_id = d.zone_id
WHERE c.event_date >= today() - 30
GROUP BY ALL
ORDER BY total_activity_records DESC
LIMIT 50;
```

---

### 04.5 Dimension Table Specification: `dim_wards`
- **Dimension Identifier:** `analytics.dim_wards`
- **Scope & Purpose:** Municipal BBMP ward geographical boundaries and population demographics.
- **Storage Engine:** `ReplacingMergeTree(version)`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.dim_wards (
    ward_number UInt16,
    ward_name String,
    zone_id LowCardinality(String),
    population_census_2021 UInt32,
    vulnerable_slum_population UInt32,
    area_sq_km Float32,
    version UInt64
) ENGINE = ReplacingMergeTree(version)
ORDER BY (zone_id, ward_number);
```

#### SCD Type 2 Historical Synchronization Strategy:
```sql
-- Incremental merge query for dim_wards
INSERT INTO analytics.dim_wards
SELECT
    *,
    toUInt64(toUnixTimestamp64Milli(now64())) AS version
FROM staging.stg_dim_wards
WHERE updated_at > (SELECT max(version) FROM analytics.{d[0]});
```

#### Governance, Indexing & Data Refresh Cadence:
1. Seed fixtures loaded during clinic commissioning; delta updates synced every 15 minutes.
2. LowCardinality dictionary compaction executed nightly via `OPTIMIZE TABLE analytics.dim_wards FINAL;`.
3. Referential integrity validated in CI via cross-table consistency checks.

#### Canonical Analytical Slice Query Blueprint:
```sql
-- Slicing fact records by dim_wards
SELECT
    d.*,
    count() AS total_activity_records,
    uniqExact(c.patient_id) AS distinct_patients_reached
FROM analytics.fact_consultations c
JOIN analytics.dim_wards d ON c.zone_id = d.zone_id
WHERE c.event_date >= today() - 30
GROUP BY ALL
ORDER BY total_activity_records DESC
LIMIT 50;
```

---

### 04.6 Dimension Table Specification: `dim_zones`
- **Dimension Identifier:** `analytics.dim_zones`
- **Scope & Purpose:** The 8 administrative zones of Greater Bengaluru Authority.
- **Storage Engine:** `ReplacingMergeTree(version)`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.dim_zones (
    zone_id String,
    zone_name String,
    zonal_cmo_name String,
    total_clinics UInt16,
    total_wards UInt16,
    version UInt64
) ENGINE = ReplacingMergeTree(version)
ORDER BY (zone_id);
```

#### SCD Type 2 Historical Synchronization Strategy:
```sql
-- Incremental merge query for dim_zones
INSERT INTO analytics.dim_zones
SELECT
    *,
    toUInt64(toUnixTimestamp64Milli(now64())) AS version
FROM staging.stg_dim_zones
WHERE updated_at > (SELECT max(version) FROM analytics.{d[0]});
```

#### Governance, Indexing & Data Refresh Cadence:
1. Seed fixtures loaded during clinic commissioning; delta updates synced every 15 minutes.
2. LowCardinality dictionary compaction executed nightly via `OPTIMIZE TABLE analytics.dim_zones FINAL;`.
3. Referential integrity validated in CI via cross-table consistency checks.

#### Canonical Analytical Slice Query Blueprint:
```sql
-- Slicing fact records by dim_zones
SELECT
    d.*,
    count() AS total_activity_records,
    uniqExact(c.patient_id) AS distinct_patients_reached
FROM analytics.fact_consultations c
JOIN analytics.dim_zones d ON c.zone_id = d.zone_id
WHERE c.event_date >= today() - 30
GROUP BY ALL
ORDER BY total_activity_records DESC
LIMIT 50;
```

---

### 04.7 Dimension Table Specification: `dim_lab_tests`
- **Dimension Identifier:** `analytics.dim_lab_tests`
- **Scope & Purpose:** Mandated 58 rapid point-of-care laboratory diagnostic tests.
- **Storage Engine:** `ReplacingMergeTree(version)`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.dim_lab_tests (
    test_code String,
    loinc_code LowCardinality(String),
    test_name String,
    specimen_type LowCardinality(String),
    normal_range_min Float32,
    normal_range_max Float32,
    panic_threshold_low Float32,
    panic_threshold_high Float32,
    unit String,
    version UInt64
) ENGINE = ReplacingMergeTree(version)
ORDER BY (test_code);
```

#### SCD Type 2 Historical Synchronization Strategy:
```sql
-- Incremental merge query for dim_lab_tests
INSERT INTO analytics.dim_lab_tests
SELECT
    *,
    toUInt64(toUnixTimestamp64Milli(now64())) AS version
FROM staging.stg_dim_lab_tests
WHERE updated_at > (SELECT max(version) FROM analytics.{d[0]});
```

#### Governance, Indexing & Data Refresh Cadence:
1. Seed fixtures loaded during clinic commissioning; delta updates synced every 15 minutes.
2. LowCardinality dictionary compaction executed nightly via `OPTIMIZE TABLE analytics.dim_lab_tests FINAL;`.
3. Referential integrity validated in CI via cross-table consistency checks.

#### Canonical Analytical Slice Query Blueprint:
```sql
-- Slicing fact records by dim_lab_tests
SELECT
    d.*,
    count() AS total_activity_records,
    uniqExact(c.patient_id) AS distinct_patients_reached
FROM analytics.fact_consultations c
JOIN analytics.dim_lab_tests d ON c.zone_id = d.zone_id
WHERE c.event_date >= today() - 30
GROUP BY ALL
ORDER BY total_activity_records DESC
LIMIT 50;
```

---

### 04.8 Dimension Table Specification: `dim_calendar`
- **Dimension Identifier:** `analytics.dim_calendar`
- **Scope & Purpose:** Calendar time dimension supporting municipal fiscal and epidemiological weeks.
- **Storage Engine:** `ReplacingMergeTree(version)`

#### Canonical ClickHouse DDL Definition:
```sql
CREATE TABLE analytics.dim_calendar (
    calendar_date Date,
    year UInt16,
    quarter UInt8,
    month UInt8,
    month_name LowCardinality(String),
    week_of_year UInt8,
    day_of_month UInt8,
    day_of_week UInt8,
    day_name LowCardinality(String),
    is_weekend UInt8,
    is_municipal_holiday UInt8,
    epi_week_string String
) ENGINE = MergeTree()
ORDER BY (calendar_date);
```

#### SCD Type 2 Historical Synchronization Strategy:
```sql
-- Incremental merge query for dim_calendar
INSERT INTO analytics.dim_calendar
SELECT
    *,
    toUInt64(toUnixTimestamp64Milli(now64())) AS version
FROM staging.stg_dim_calendar
WHERE updated_at > (SELECT max(version) FROM analytics.{d[0]});
```

#### Governance, Indexing & Data Refresh Cadence:
1. Seed fixtures loaded during clinic commissioning; delta updates synced every 15 minutes.
2. LowCardinality dictionary compaction executed nightly via `OPTIMIZE TABLE analytics.dim_calendar FINAL;`.
3. Referential integrity validated in CI via cross-table consistency checks.

#### Canonical Analytical Slice Query Blueprint:
```sql
-- Slicing fact records by dim_calendar
SELECT
    d.*,
    count() AS total_activity_records,
    uniqExact(c.patient_id) AS distinct_patients_reached
FROM analytics.fact_consultations c
JOIN analytics.dim_calendar d ON c.zone_id = d.zone_id
WHERE c.event_date >= today() - 30
GROUP BY ALL
ORDER BY total_activity_records DESC
LIMIT 50;
```

---

## 05. 15 Canonical Public Health Indicators (ARCH-ANL-001 to ARCH-ANL-015)
Standardized specification of the 15 municipal public health key performance indicators:

### 05.01 Indicator Specification: `ARCH-ANL-001` (Daily Outpatient Clinic Footfall)
- **Indicator Identifier:** `ARCH-ANL-001`
- **Indicator Name:** Daily Outpatient Clinic Footfall
- **Healthcare Domain:** Operations
- **Target Benchmark:** >= 80 patients/day per clinic
- **Critical Alert Threshold:** < 40 patients/day (Under-utilization)
- **Reporting Cadence & Granularity:** Clinic / Daily
- **Visual Dashboard Component:** Line Chart & Daily Gauge

#### Mathematical Formulation:
$$\text{Daily Footfall} = \sum_{i=1}^{N} \mathbb{I}(\text{encounter}_i \in \text{clinic}_c, \text{date}_d)$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    event_date,
    clinic_id,
    count() AS total_footfall,
    countIf(patient_gender = 'female') AS female_patients,
    countIf(patient_gender = 'male') AS male_patients,
    countIf(patient_age < 12) AS pediatric_patients,
    countIf(patient_age >= 60) AS senior_patients
FROM analytics.fact_consultations
WHERE event_date = :target_date
GROUP BY event_date, clinic_id;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `< 40 patients/day (Under-utilization)` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_001 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.02 Indicator Specification: `ARCH-ANL-002` (Average Consultation Duration)
- **Indicator Identifier:** `ARCH-ANL-002`
- **Indicator Name:** Average Consultation Duration
- **Healthcare Domain:** Clinical Quality
- **Target Benchmark:** 8.0 - 15.0 minutes
- **Critical Alert Threshold:** < 4.0 minutes (Rushed care) or > 25.0 minutes (Bottleneck)
- **Reporting Cadence & Granularity:** Doctor / Weekly
- **Visual Dashboard Component:** Boxplot & Distribution Histogram

#### Mathematical Formulation:
$$\text{Avg Duration} = \frac{1}{N} \sum_{i=1}^N \text{duration}_i$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    event_date,
    doctor_id,
    avg(consultation_duration_seconds) / 60.0 AS avg_duration_minutes,
    median(consultation_duration_seconds) / 60.0 AS median_duration_minutes,
    quantile(0.90)(consultation_duration_seconds) / 60.0 AS p90_duration_minutes
FROM analytics.fact_consultations
WHERE event_date = :target_date
GROUP BY event_date, doctor_id;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `< 4.0 minutes (Rushed care) or > 25.0 minutes (Bottleneck)` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_002 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.03 Indicator Specification: `ARCH-ANL-003` (Antibiotic AWaRe Compliance Ratio)
- **Indicator Identifier:** `ARCH-ANL-003`
- **Indicator Name:** Antibiotic AWaRe Compliance Ratio
- **Healthcare Domain:** Infectious Disease
- **Target Benchmark:** >= 60.0% Access class antibiotics (WHO Target)
- **Critical Alert Threshold:** < 50.0% Access class (Overuse of Watch antibiotics)
- **Reporting Cadence & Granularity:** Zone / Monthly
- **Visual Dashboard Component:** Stacked Bar Chart (Access vs Watch vs Reserve)

#### Mathematical Formulation:
$$\text{AWaRe Compliance} = \frac{\sum \text{Dispensations}_{\text{Access}}}{\sum \text{Dispensations}_{\text{Total Antibiotics}}} \times 100$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    toStartOfMonth(d.event_date) AS reporting_month,
    d.zone_id,
    (countIf(g.who_aware_class = 'ACCESS') / count()) * 100.0 AS access_ratio_percent,
    (countIf(g.who_aware_class = 'WATCH') / count()) * 100.0 AS watch_ratio_percent,
    (countIf(g.who_aware_class = 'RESERVE') / count()) * 100.0 AS reserve_ratio_percent
FROM analytics.fact_dispensations d
JOIN analytics.dim_drugs g ON d.drug_id = g.drug_id
WHERE g.therapeutic_category = 'ANTIBIOTIC'
GROUP BY reporting_month, d.zone_id;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `< 50.0% Access class (Overuse of Watch antibiotics)` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_003 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.04 Indicator Specification: `ARCH-ANL-004` (Essential Drug Stockout Rate)
- **Indicator Identifier:** `ARCH-ANL-004`
- **Indicator Name:** Essential Drug Stockout Rate
- **Healthcare Domain:** Supply Chain
- **Target Benchmark:** < 2.0% stockout rate across 300 EML drugs
- **Critical Alert Threshold:** > 5.0% stockout rate (Critical supply breach)
- **Reporting Cadence & Granularity:** Clinic / Daily
- **Visual Dashboard Component:** Heatmap & Red Alert Counter

#### Mathematical Formulation:
$$\text{Stockout Rate} = \frac{\sum \mathbb{I}(\text{Stock}_{\text{drug}} = 0)}{N_{\text{Essential Formulary}}} \times 100$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    event_date,
    clinic_id,
    (countIf(balance_after = 0) / count(DISTINCT drug_id)) * 100.0 AS stockout_rate_percent
FROM analytics.fact_stock_movements
WHERE event_date = :target_date
GROUP BY event_date, clinic_id;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `> 5.0% stockout rate (Critical supply breach)` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_004 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.05 Indicator Specification: `ARCH-ANL-005` (Hypertension Control Rate)
- **Indicator Identifier:** `ARCH-ANL-005`
- **Indicator Name:** Hypertension Control Rate
- **Healthcare Domain:** NCD Chronic Care
- **Target Benchmark:** >= 70.0% hypertensive patients controlled
- **Critical Alert Threshold:** < 50.0% controlled blood pressure
- **Reporting Cadence & Granularity:** Ward / Monthly
- **Visual Dashboard Component:** Trend Line & Ward Chloropleth Map

#### Mathematical Formulation:
$$\text{BP Control Rate} = \frac{\sum \mathbb{I}(\text{SBP} < 140 \land \text{DBP} < 90)}{N_{\text{Hypertension Patients}}} \times 100$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    toStartOfMonth(event_date) AS reporting_month,
    ward_number,
    (countIf(systolic_bp < 140 AND diastolic_bp < 90) / count()) * 100.0 AS bp_controlled_percent
FROM analytics.fact_consultations
WHERE primary_icd10 = 'I10'
GROUP BY reporting_month, ward_number;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `< 50.0% controlled blood pressure` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_005 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.06 Indicator Specification: `ARCH-ANL-006` (Diabetes Glycemic Control Compliance)
- **Indicator Identifier:** `ARCH-ANL-006`
- **Indicator Name:** Diabetes Glycemic Control Compliance
- **Healthcare Domain:** NCD Chronic Care
- **Target Benchmark:** >= 65.0% postprandial blood sugar < 180 mg/dL
- **Critical Alert Threshold:** < 45.0% glycemic compliance
- **Reporting Cadence & Granularity:** Ward / Monthly
- **Visual Dashboard Component:** Trend Line & Cohort Breakdown

#### Mathematical Formulation:
$$\text{Glycemic Compliance} = \frac{\sum \mathbb{I}(\text{RBS} < 180)}{N_{\text{Diabetic Tests}}} \times 100$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    toStartOfMonth(event_date) AS reporting_month,
    ward_number,
    (countIf(result_numeric < 180.0) / count()) * 100.0 AS rbs_controlled_percent
FROM analytics.fact_lab_investigations
WHERE test_code = 'LAB-RBS'
GROUP BY reporting_month, ward_number;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `< 45.0% glycemic compliance` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_006 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.07 Indicator Specification: `ARCH-ANL-007` (Presumptive TB Sputum Referral Rate)
- **Indicator Identifier:** `ARCH-ANL-007`
- **Indicator Name:** Presumptive TB Sputum Referral Rate
- **Healthcare Domain:** Infectious Disease
- **Target Benchmark:** >= 80.0% cough > 2 weeks referred for sputum
- **Critical Alert Threshold:** < 60.0% sputum referral compliance
- **Reporting Cadence & Granularity:** Clinic / Monthly
- **Visual Dashboard Component:** Bar Chart & Nikshay Integration Metric

#### Mathematical Formulation:
$$\text{TB Sputum Referral Rate} = \frac{\sum \text{Sputum Orders}}{\sum \text{Cough } > 2 \text{ Weeks}} \times 100$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    toStartOfMonth(c.event_date) AS reporting_month,
    c.clinic_id,
    (countIf(l.test_code = 'LAB-TB-SPUTUM') / countIf(c.primary_icd10 IN ('A15', 'R05'))) * 100.0 AS sputum_referral_percent
FROM analytics.fact_consultations c
LEFT JOIN analytics.fact_lab_investigations l ON c.encounter_id = l.order_id
GROUP BY reporting_month, c.clinic_id;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `< 60.0% sputum referral compliance` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_007 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.08 Indicator Specification: `ARCH-ANL-008` (Maternal Antenatal Care 4+ Compliance)
- **Indicator Identifier:** `ARCH-ANL-008`
- **Indicator Name:** Maternal Antenatal Care 4+ Compliance
- **Healthcare Domain:** MCH Health
- **Target Benchmark:** >= 85.0% pregnant mothers receiving 4+ ANC visits
- **Critical Alert Threshold:** < 70.0% ANC coverage
- **Reporting Cadence & Granularity:** Ward / Monthly
- **Visual Dashboard Component:** Cohort Funnel & Ward Bar Chart

#### Mathematical Formulation:
$$\text{ANC 4+ Coverage} = \frac{\sum \text{Mothers with } \ge 4 \text{ Visits}}{N_{\text{Registered Cohort}}} \times 100$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    toStartOfMonth(event_date) AS reporting_month,
    ward_number,
    (countIf(anc_visit_number >= 4) / count(DISTINCT mother_patient_id)) * 100.0 AS anc4_compliance_percent
FROM analytics.fact_maternal_antenatal
GROUP BY reporting_month, ward_number;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `< 70.0% ANC coverage` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_008 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.09 Indicator Specification: `ARCH-ANL-009` (Full Childhood Immunization Coverage)
- **Indicator Identifier:** `ARCH-ANL-009`
- **Indicator Name:** Full Childhood Immunization Coverage
- **Healthcare Domain:** Pediatrics
- **Target Benchmark:** >= 95.0% infant vaccination completion at 1 year
- **Critical Alert Threshold:** < 85.0% vaccination coverage
- **Reporting Cadence & Granularity:** Ward / Quarterly
- **Visual Dashboard Component:** Chloropleth Map & ASHA Task List

#### Mathematical Formulation:
$$\text{Full Immunization Rate} = \frac{\sum \text{Fully Immunized Infants}}{N_{\text{Infant Cohort}}} \times 100$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    toStartOfMonth(event_date) AS reporting_month,
    ward_number,
    (countIf(child_age_months <= 12 AND is_on_time = 1) / count(DISTINCT child_patient_id)) * 100.0 AS full_immunization_percent
FROM analytics.fact_child_immunizations
GROUP BY reporting_month, ward_number;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `< 85.0% vaccination coverage` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_009 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.10 Indicator Specification: `ARCH-ANL-010` (MEWS Critical Triage Rate)
- **Indicator Identifier:** `ARCH-ANL-010`
- **Indicator Name:** MEWS Critical Triage Rate
- **Healthcare Domain:** Emergency Triage
- **Target Benchmark:** 1.0% - 3.0% of total outpatient footfall
- **Critical Alert Threshold:** > 5.0% (Mass deterioration / epidemic)
- **Reporting Cadence & Granularity:** Clinic / Real-Time
- **Visual Dashboard Component:** Real-Time Flashing Dial & Audio Alarm

#### Mathematical Formulation:
$$\text{Critical Triage Ratio} = \frac{\sum \mathbb{I}(\text{MEWS} \ge 5)}{N_{\text{Consultations}}} \times 100$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    event_date,
    clinic_id,
    (countIf(mews_score >= 5) / count()) * 100.0 AS critical_mews_percent
FROM analytics.fact_consultations
WHERE event_date = :target_date
GROUP BY event_date, clinic_id;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `> 5.0% (Mass deterioration / epidemic)` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_010 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.11 Indicator Specification: `ARCH-ANL-011` (Panic Laboratory Result Escalation Rate)
- **Indicator Identifier:** `ARCH-ANL-011`
- **Indicator Name:** Panic Laboratory Result Escalation Rate
- **Healthcare Domain:** Diagnostics
- **Target Benchmark:** 100% panic values escalated within 5 minutes
- **Critical Alert Threshold:** < 95.0% prompt escalation
- **Reporting Cadence & Granularity:** Clinic / Weekly
- **Visual Dashboard Component:** SLA Adherence Gauge & Audit Log

#### Mathematical Formulation:
$$\text{Panic Escalation Rate} = \frac{\sum \mathbb{I}(\text{Panic} \land \text{Time} < 300s)}{N_{\text{Panic Values}}} \times 100$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    toStartOfWeek(event_date) AS reporting_week,
    clinic_id,
    (countIf(is_panic_value = 1 AND turnaround_time_seconds < 300) / countIf(is_panic_value = 1)) * 100.0 AS panic_escalation_percent
FROM analytics.fact_lab_investigations
GROUP BY reporting_week, clinic_id;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `< 95.0% prompt escalation` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_011 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.12 Indicator Specification: `ARCH-ANL-012` (Citizen Satisfaction Score (CSAT))
- **Indicator Identifier:** `ARCH-ANL-012`
- **Indicator Name:** Citizen Satisfaction Score (CSAT)
- **Healthcare Domain:** Citizen Experience
- **Target Benchmark:** >= 85.0% positive satisfaction rating
- **Critical Alert Threshold:** < 70.0% satisfaction
- **Reporting Cadence & Granularity:** Clinic / Weekly
- **Visual Dashboard Component:** Star Distribution & Trend Line

#### Mathematical Formulation:
$$\text{CSAT} = \frac{1}{5N} \sum_{i=1}^N \text{Stars}_i \times 100$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    toStartOfWeek(event_date) AS reporting_week,
    clinic_id,
    (avg(star_rating) / 5.0) * 100.0 AS csat_percent,
    count() AS total_ratings
FROM analytics.fact_citizen_feedback
GROUP BY reporting_week, clinic_id;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `< 70.0% satisfaction` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_012 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.13 Indicator Specification: `ARCH-ANL-013` (Total Clinic Waiting Duration (Front-to-Exit))
- **Indicator Identifier:** `ARCH-ANL-013`
- **Indicator Name:** Total Clinic Waiting Duration (Front-to-Exit)
- **Healthcare Domain:** Operations
- **Target Benchmark:** < 45.0 minutes total visit duration
- **Critical Alert Threshold:** > 75.0 minutes total duration (Severe delay)
- **Reporting Cadence & Granularity:** Clinic / Hourly
- **Visual Dashboard Component:** Hourly Step Chart & Journey Breakdown

#### Mathematical Formulation:
$$\text{Total Duration} = \frac{1}{N} \sum_{i=1}^N \text{Duration}_{\text{Exit}} - \text{Time}_{\text{Entry}}$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    event_date,
    clinic_id,
    avg(total_clinic_duration_seconds) / 60.0 AS avg_total_minutes,
    median(total_clinic_duration_seconds) / 60.0 AS median_total_minutes,
    quantile(0.95)(total_clinic_duration_seconds) / 60.0 AS p95_total_minutes
FROM analytics.fact_queue_waits
WHERE event_date = :target_date
GROUP BY event_date, clinic_id;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `> 75.0 minutes total duration (Severe delay)` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_013 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.14 Indicator Specification: `ARCH-ANL-014` (Pharmacy Dispensation Waiting Time)
- **Indicator Identifier:** `ARCH-ANL-014`
- **Indicator Name:** Pharmacy Dispensation Waiting Time
- **Healthcare Domain:** Operations
- **Target Benchmark:** < 10.0 minutes waiting at pharmacy counter
- **Critical Alert Threshold:** > 20.0 minutes waiting at dispensary
- **Reporting Cadence & Granularity:** Clinic / Daily
- **Visual Dashboard Component:** Queue Velocity Gauge

#### Mathematical Formulation:
$$\text{Pharmacy Wait} = \frac{1}{N} \sum_{i=1}^N \text{Wait}_{\text{Pharmacy}}$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    event_date,
    clinic_id,
    avg(pharmacy_wait_seconds) / 60.0 AS avg_pharmacy_wait_minutes
FROM analytics.fact_queue_waits
WHERE event_date = :target_date
GROUP BY event_date, clinic_id;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `> 20.0 minutes waiting at dispensary` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_014 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

### 05.15 Indicator Specification: `ARCH-ANL-015` (Bio-Medical Waste Daily Segregation Index)
- **Indicator Identifier:** `ARCH-ANL-015`
- **Indicator Name:** Bio-Medical Waste Daily Segregation Index
- **Healthcare Domain:** Facility Governance
- **Target Benchmark:** 100.0% statutory BMWM compliance
- **Critical Alert Threshold:** < 95.0% waste compliance
- **Reporting Cadence & Granularity:** Clinic / Monthly
- **Visual Dashboard Component:** Compliance Checklist & Audit Radar Chart

#### Mathematical Formulation:
$$\text{BMWM Index} = \frac{\sum \text{Compliant Disposal Days}}{N_{\text{Operating Days}}} \times 100$$

#### Authoritative Analytical SQL Calculation:
```sql
SELECT
    toStartOfMonth(event_date) AS reporting_month,
    clinic_id,
    (countIf(is_manifest_signed = 1 AND yellow_bag_kg > 0 AND red_bag_kg > 0) / count()) * 100.0 AS bmwm_compliance_percent
FROM analytics.fact_biomedical_waste
GROUP BY reporting_month, clinic_id;
```

#### Clinical Governance & Escalation Protocol:
1. **Continuous Monitoring:** Evaluated continuously on ClickHouse; breaching `< 95.0% waste compliance` dispatches high-priority alert to Zonal CMO.
2. **Intervention Action:** Directs clinic facility supervisor to initiate root-cause investigation within 24 hours.
3. **Historical Aggregation:** Aggregated into monthly municipal health quality reports and posted to public dashboard.
4. **Privacy Protection:** Data points filtered by role permissions and k-anonymity privacy constraints.

#### Materialized View Aggregation for Indicator:
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_ind_arch_anl_015 (
    event_date Date,
    zone_id LowCardinality(String),
    ward_number UInt16,
    metric_value Float32
) ENGINE = SummingMergeTree()
ORDER BY (zone_id, ward_number, event_date) AS
SELECT
    event_date,
    zone_id,
    ward_number,
    count() AS metric_value
FROM analytics.fact_consultations
GROUP BY event_date, zone_id, ward_number;
```

---

## 06. Spatial-Temporal Syndromic Surveillance Engine
Algorithmic detection of emergent infectious disease outbreaks across the 225 municipal wards:
1. **Spatial-Temporal Cluster Anomaly Detector (Poisson Regression + CUSUM):**
   - Baseline expected fever cases calculated for each ward using a rolling 21-day historical mean adjusted for seasonal rainfall.
   - Daily observed counts $Y_{w,t}$ compared against expected $\mu_{w,t}$.
   - Anomaly flag raised if cumulative sum exceeds threshold: $S_t = \max(0, S_{t-1} + Y_t - k) > h$.

#### CUSUM Syndromic Detector Implementation Blueprint:
```python
import numpy as np

class SyndromicAnomalyDetector:
    def __init__(self, k_allowance: float = 1.5, h_threshold: float = 4.0):
        self.k = k_allowance
        self.h = h_threshold

    def evaluate_ward_series(self, counts: np.ndarray, baseline_mean: float, baseline_std: float) -> dict:
        s_pos = 0.0
        alerts = []
        for t, y in enumerate(counts):
            z = (y - baseline_mean) / max(baseline_std, 1e-4)
            s_pos = max(0.0, s_pos + z - self.k)
            if s_pos > self.h:
                alerts.append({'day_index': t, 'cusum_score': float(s_pos), 'observed_count': int(y)})
        return {'anomaly_detected': len(alerts) > 0, 'alerts': alerts}
```

2. **Micro-Cluster Heatmap Generation:**
   - GeoJSON choropleth layers colored by outbreak probability index (0.00 to 1.00).
   - Wards highlighted in RED trigger automated field inspection tasks for auxiliary nurse midwives (ANMs) and vector-borne disease control officers.

#### GeoJSON Heatmap Query Specification:
```sql
SELECT
    w.ward_number,
    w.ward_name,
    countIf(primary_icd10 IN ('A90', 'A91')) AS dengue_cases,
    countIf(primary_icd10 IN ('A09', 'A00')) AS cholera_cases,
    count() AS total_fever_cases,
    (countIf(primary_icd10 IN ('A90', 'A91')) / w.population_census_2021) * 100000.0 AS dengue_incidence_per_100k
FROM analytics.fact_consultations c
JOIN analytics.dim_wards w ON c.ward_number = w.ward_number
WHERE c.event_date >= today() - 7
GROUP BY w.ward_number, w.ward_name, w.population_census_2021
ORDER BY dengue_incidence_per_100k DESC;
```

## 07. Apache Superset Executive Dashboard Specifications
Comprehensive blueprints and JSON configuration slices for the 3 central municipal operational dashboards:

### 07.1 Zonal Chief Medical Officer Executive Cockpit
- **Target Users:** Zonal CMOs (`ROLE-012`), Municipal Health Commissioner.
- **Primary Refresh Interval:** 60 seconds (Auto-refresh enabled).
- **Slicing Filters:** Zone Selector, Ward Multi-select, Date Range (Today, WTD, MTD).

#### Dashboard Slice Configuration Blueprint:
```json
{
  "dashboard_title": "Zonal CMO Operational Cockpit",
  "slices": [
    {
      "slice_name": "Clinic Footfall Comparison",
      "viz_type": "echarts_timeseries_bar",
      "datasource": "analytics.fact_consultations",
      "metrics": ["count()"],
      "groupby": ["clinic_id"]
    },
    {
      "slice_name": "Critical MEWS Triage Alerts",
      "viz_type": "gauge_chart",
      "datasource": "analytics.fact_consultations",
      "metrics": ["countIf(mews_score >= 5)"],
      "adhoc_filters": [{"clause": "WHERE", "expressionType": "SQL", "sqlExpression": "event_date = today()"}]
    },
    {
      "slice_name": "Stockout Risk Heatmap",
      "viz_type": "heatmap",
      "datasource": "analytics.fact_stock_movements",
      "all_columns_x": "clinic_id",
      "all_columns_y": "drug_id",
      "metric": "min(balance_after)"
    }
  ]
}
```

### 07.2 Municipal Epidemiologist Surveillance Console
- **Target Users:** District Epidemiologists (`ROLE-013`), IDSP Surveillance Officers.
- **Primary Refresh Interval:** 300 seconds.
- **Slicing Filters:** Syndrome Category (Fever, Respiratory, Diarrheal), Ward Boundary (1-225).

#### Dashboard Slice Configuration Blueprint:
```json
{
  "dashboard_title": "Municipal Epidemiological Surveillance Console",
  "slices": [
    {
      "slice_name": "Ward Syndromic Chloropleth Map",
      "viz_type": "deck_geojson",
      "datasource": "analytics.dim_wards",
      "metric": "sum(fever_syndrome_count)",
      "color_scheme": "schemeOranges"
    },
    {
      "slice_name": "Antibiotic AWaRe Stewardship Ratio",
      "viz_type": "pie",
      "datasource": "analytics.fact_dispensations",
      "groupby": ["who_aware_class"],
      "metric": "count()"
    },
    {
      "slice_name": "Weekly IDSP Form P Automated Aggregation",
      "viz_type": "table",
      "datasource": "analytics.fact_consultations",
      "metrics": ["count()", "countIf(primary_icd10 = 'A09')", "countIf(primary_icd10 = 'A90')"],
      "groupby": ["ward_number", "event_date"]
    }
  ]
}
```

### 07.3 Clinic Facility Quality Auditor Cockpit
- **Target Users:** NQAS Quality Auditors (`ROLE-014`), Clinic Administrators (`ROLE-011`).
- **Primary Refresh Interval:** Daily.
- **Slicing Filters:** Clinic Facility ID, Quality Domain.

#### Dashboard Slice Configuration Blueprint:
```json
{
  "dashboard_title": "Clinic Quality & NQAS Compliance Cockpit",
  "slices": [
    {
      "slice_name": "Citizen CSAT Trend",
      "viz_type": "line",
      "datasource": "analytics.fact_citizen_feedback",
      "metric": "avg(star_rating)",
      "granularity_sqla": "event_date"
    },
    {
      "slice_name": "Patient Journey Wait Breakdown",
      "viz_type": "dist_bar",
      "datasource": "analytics.fact_queue_waits",
      "metrics": ["avg(triage_wait_seconds)", "avg(doctor_wait_seconds)", "avg(pharmacy_wait_seconds)"],
      "groupby": ["clinic_id"]
    },
    {
      "slice_name": "Bio-Medical Waste Segregation Index",
      "viz_type": "radar",
      "datasource": "analytics.fact_biomedical_waste",
      "metrics": ["sum(yellow_bag_kg)", "sum(red_bag_kg)", "sum(white_box_kg)", "sum(blue_cardboard_kg)"]
    }
  ]
}
```

## 08. Data Privacy, k-Anonymity & Differential Privacy Controls
Statutory privacy safeguards enforced on analytical queries:
1. **k-Anonymity Enforcement (k >= 5):** Aggregation queries returning groups with fewer than 5 individuals return suppressed values (`NULL` or `< 5`) preventing re-identification.
2. **Laplace Differential Privacy Noise:** Small calibrated Laplacian noise added to public footfall exports protecting individual citizen visit attendance timestamps.
3. **Role-Based Row-Level Security:** ClickHouse users authenticated via LDAP/OIDC; queries automatically inject `WHERE zone_id = :user_zone` for zonal officers.
4. **Zero-PII Storage Policy in Analytical Tier:** Patient names, Aadhaar numbers, phone numbers, and physical residential addresses are strictly barred from the ClickHouse cluster; all records are identified solely by anonymized UUIDv7 surrogates.

### 08.1 ClickHouse Distributed Cluster Topology
Production ClickHouse cluster deployment architecture ensuring high availability and linear scaling:
```xml
<clickhouse>
    <remote_servers>
        <namma_cluster>
            <shard>
                <replica>
                    <host>clickhouse-01.bbmp.internal</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>clickhouse-02.bbmp.internal</host>
                    <port>9000</port>
                </replica>
            </shard>
            <shard>
                <replica>
                    <host>clickhouse-03.bbmp.internal</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>clickhouse-04.bbmp.internal</host>
                    <port>9000</port>
                </replica>
            </shard>
        </namma_cluster>
    </remote_servers>
</clickhouse>
```

## 09. Automated Data Quality Gateways & Anomaly Verification
Automated nightly data quality monitors running against the ClickHouse star schema:
1. **Clinic Reconciliation Check:** Asserts that every active clinic has at least 1 record in `fact_consultations` per operating day; missing clinics trigger IT helpdesk alerts.
2. **Null Vitals Anomaly Detector:** Flags clinics where > 15% of consultations have missing systolic/diastolic blood pressure recordings.
3. **Negative Stock Movement Guard:** Validates that `balance_after >= 0` across all pharmacy batch rows.
4. **CDC Stream Lag Monitor:** Verifies that maximum ingestion lag between PostgreSQL WAL timestamp and ClickHouse `event_timestamp` remains < 5,000ms.
5. **Automated Partition Compaction:** Executes `OPTIMIZE TABLE ... FINAL` weekly to merge replacing trees and reclaim storage.

## 10. Analytics Architecture Fitness Tests & Operational SLOs
Service Level Objectives (SLOs) and automated CI architecture fitness tests for the analytical platform:
1. **Query Latency SLO:** 99% of Superset dashboard queries must complete in < 1,500ms; 95% complete in < 500ms.
2. **Data Freshness SLO:** Maximum end-to-end CDC pipeline lag between clinic encounter commit and ClickHouse queryability < 10.0 seconds.
3. **Availability SLO:** Analytical query interface availability >= 99.9% during municipal working hours (08:00 - 20:00 IST).
4. **Automated Fitness Test - Direct OLTP Cross-Query Prohibition:** CI linter scans all Superset slice SQL queries, failing any pull request that attempts direct connections to operational PostgreSQL.
5. **Automated Fitness Test - Partition Pruning Verification:** All queries must include `event_date` or `toYYYYMM(event_date)` filter in the WHERE clause; queries forcing full-table scans fail CI automated test suites.
6. **Storage Optimization Fitness Gate:** ClickHouse compression ratio must exceed 4.5x on uncompressed raw JSON payload sizes; monitored weekly by automated Prometheus probe.
7. **Continuous Data Drift Detection:** Automated weekly Kolmogorov-Smirnov statistical tests compare distributions of clinical vitals across clinics, detecting sensor calibration drift.
8. **Schema Evolution Compatibility Test:** Every proposed change to Kafka Avro schemas must satisfy BACKWARD_TRANSITIVE compatibility in the Schema Registry before PR merge.
9. **Query Execution Timeout Guard:** ClickHouse enforced `max_execution_time = 15` seconds preventing runaway ad-hoc queries from impacting dashboard renders.
10. **Audit Log Mirroring:** All queries executed by municipal dashboard users are mirrored to the WORM audit store for privacy compliance.
