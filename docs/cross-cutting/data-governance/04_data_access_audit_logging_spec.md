# 🔍 Patient Data Access & Audit Logging Architecture Specification
## Namma Clinic Digital Health & Operations Platform
### Tamper-Evident Access Trails | DPDP Act 2023 | CERT-In 180-Day Mandate
### Document Code: DG-AUD-04 | Version: 1.0 | Date: September 2026

---

## 1. Compliance Mandate & Objectives

Under the **Digital Personal Data Protection Act, 2023 (DPDP Act)** and the **CERT-In Cyber Security Directions (April 2022)**, any system processing sensitive public health data must maintain an exhaustive, immutable, and tamper-evident audit record of **all interactions with citizen medical records**. 

Every event—whether a frontline nurse viewing vitals, a doctor generating a prescription, a pharmacist dispensing medication, an administrator downloading an analytical report, or an automated batch worker running an export—is permanently captured in the immutable audit log.

---

## 2. Architecture of the Tamper-Evident Audit Pipeline

```
[Clinic Frontend / API Request]
              │
              ▼
    [API Gateway / Auth Middleware] ───► Captures User Context, JWT claims, IP, Device
              │
              ▼
  [Application Service Execution]
              │
              ├──► [Database Mutation / Read]
              │
              └──► [Async Audit Event Publisher] (Redis Streams / Kafka Topic)
                             │
                             ▼
                    [Audit Worker Engine]
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
[PostgreSQL `access_audit_logs`]     [WORM S3 Bucket (Glacier Vault)]
(Cryptographically Hash-Chained)      (Signed JSON Archive, 180+ Days)
```

---

## 3. Data Schema: `access_audit_logs`

| Column Name | SQL Type | Nullable | Description |
| :--- | :--- | :---: | :--- |
| `audit_event_id` | `VARCHAR(36)` | NO (PK) | Globally unique event UUID (v4). |
| `timestamp_utc` | `TIMESTAMPTZ` | NO | High-resolution UTC timestamp synchronized via NTP. |
| `user_id` | `VARCHAR(36)` | NO | Unique identifier of the authenticated user. |
| `user_role` | `VARCHAR(20)` | NO | Role at invocation: `'DOCTOR'`, `'NURSE'`, `'PHARMACIST'`, `'RECEPTIONIST'`, `'ADMIN'`. |
| `clinic_id` | `VARCHAR(20)` | NO | Clinic location where the request originated (e.g., `'NC-W-001'`). |
| `patient_id` | `VARCHAR(36)` | YES | ID of citizen whose record was touched (NULL for administrative tasks). |
| `action_category`| `VARCHAR(25)` | NO | Enum: `'RECORD_VIEW'`, `'RECORD_CREATE'`, `'RECORD_UPDATE'`, `'PRESCRIPTION_PRINT'`, `'EXPORT_DOWNLOAD'`, `'LOGIN_SUCCESS'`, `'LOGIN_FAILED'`. |
| `resource_type` | `VARCHAR(30)` | NO | Target entity: `'PATIENT'`, `'ENCOUNTER'`, `'VITALS'`, `'PRESCRIPTION'`, `'LAB_RESULT'`, `'REPORT'`. |
| `resource_id` | `VARCHAR(36)` | YES | Specific record ID accessed or mutated. |
| `client_ip` | `VARCHAR(45)` | NO | Originating IPv4 / IPv6 address. |
| `user_agent` | `VARCHAR(255)`| NO | Browser, OS, and client software version. |
| `session_token_hash`| `VARCHAR(64)`| NO | SHA-256 hash of active session token. |
| `mutation_diff` | `JSONB` | YES | For UPDATE actions: captured `{old_value, new_value}` payload. |
| `prev_record_hash`| `VARCHAR(64)` | NO | SHA-256 hash of the preceding audit record (Chained Blockchain-style). |
| `current_hash` | `VARCHAR(64)` | NO | SHA-256 hash of `[timestamp + user_id + patient_id + action + prev_hash]`. |

---

## 4. Cryptographic Hash Chaining for Tamper Evidence

To prevent unauthorized internal alteration or deletion of audit logs by system administrators or compromised service accounts, records are linked via **cryptographic hash chaining**:

$$\text{current\_hash}_n = \text{SHA256}\left( \text{audit\_event\_id}_n \parallel \text{timestamp}_n \parallel \text{user\_id}_n \parallel \text{patient\_id}_n \parallel \text{action}_n \parallel \text{current\_hash}_{n-1} \right)$$

* If any rogue process modifies an older audit log entry, the hash chain breaks instantly.
* An automated daily verification job executes across the audit log table, alerting the Security Officer if any link in the chain fails verification.

---

## 5. Automated Security Alerts & Anomaly Triggers

The system continuously scans audit streams for anomalous behavioral patterns:

| Alert ID | Trigger Condition | Severity | Automated Action |
| :---: | :--- | :---: | :--- |
| **SEC-01** | Single user views $> 50$ distinct patient profiles within 10 minutes. | 🔴 Critical | User session suspended instantly; SMS alert to Zonal MO & CISO. |
| **SEC-02** | Clinic account access logged outside operating hours (10:00 PM – 06:00 AM).| 🟡 High | Session flagged for mandatory re-authentication via MFA; logged in security queue. |
| **SEC-03** | User IP address changes abruptly mid-session without logout. | 🟡 High | Session invalidated immediately (preventing session hijacking). |
| **SEC-04** | Administrative bulk export requested without two-person approval. | 🔴 Critical | Request blocked; email dispatch to Special Commissioner. |

---

## 6. Retention, Archival & CERT-In Compliance

1. **Active Hot Storage (PostgreSQL):** Accessible for immediate query analysis for **90 calendar days**.
2. **Warm Archive Storage (S3 Standard-IA / Glacier Vault):** Automatically transitioned on day 91 into **WORM (Write Once, Read Many)** storage with object lock enabled for an additional **90 days (180 days total minimum)**.
3. **Disposal:** Automated lifecycle policy triggers after **5 years** in compliance with medical record retention regulations.
