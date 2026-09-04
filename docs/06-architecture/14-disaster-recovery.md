# 🚨 Architecture Document 14: Enterprise Disaster Recovery, Business Continuity & High Availability Architecture
## Namma Clinic Digital Health & Operations Platform
### Greater Bengaluru Authority (GBA) / BBMP Health Department
**Standard:** ISO 22301 / MEITY / ABDM / Patroni Multi-AZ HA | **Status:** APPROVED BASELINE | **Code:** `ARCH-DR-14`

---

## 01. Document Overview & Business Continuity Philosophy
This document specifies the enterprise disaster recovery (DR), business continuity planning (BCP), high availability (HA) infrastructure, and emergency operational runbooks for the Namma Clinic Digital Health & Operations Platform. The platform serves 183 primary health clinics across the 8 municipal zones of Greater Bengaluru, managing daily patient care, emergency triage, electronic prescriptions, and diagnostic workflows. Consequently, system resilience directly impacts citizen survival, public health surveillance, and statutory clinical compliance.

### 01.1 Core Business Continuity Invariants
1. **Absolute Patient Safety Priority:** Under no disaster scenario shall clinical decision-making or urgent emergency care be blocked by technology failure; physical and local edge fail-safes take absolute precedence.
2. **Autonomous Edge Continuity (72-Hour Survival):** Every clinic edge appliance must sustain local clinical, triage, pharmacy, and diagnostic operations for at least 72 continuous hours during complete cloud, backhaul, or municipal WAN disconnection.
3. **Strict Target RPO / RTO Boundaries:** Central cloud recovery targets: Recovery Point Objective (RPO) < 15 minutes, Recovery Time Objective (RTO) < 30 minutes for Tier 1 mission-critical clinical workloads.
4. **Cryptographic Immutability of Replicated State:** All off-site database backups, WAL archives, and audit trails must be cryptographically signed, encrypted with AES-256-GCM, and stored with Write-Once-Read-Many (WORM) object locks preventing ransomware deletion or modification.
5. **Continuous Automated Verification:** Disaster recovery mechanisms are not theoretical paper plans; they must be verified via quarterly automated GameDay simulations and continuous chaos injection.

## 02. High Availability & Fault-Tolerant Topology
Comprehensive architecture spanning cloud control plane and edge clinic appliances:
```
 +------------------------------------------------------------------------------------------------+
 |                             PRIMARY CLOUD REGION (Bengaluru AZ-1)                              |
 |  +-----------------------+     +-----------------------+     +------------------------------+  |
 |  | Ingress NLB / Envoy   | --> | Kubernetes Services   | --> | Patroni PostgreSQL Primary   |  |
 |  | (Multi-Zone Active)   |     | (HPA Replicated Pods) |     | (Local Sync Standby AZ-2)    |  |
 |  +-----------------------+     +-----------------------+     +------------------------------+  |
 +------------------------------------------------------------------------------------------------+
                                       | Synchronous WAL Replication
                                       v
 +------------------------------------------------------------------------------------------------+
 |                            SECONDARY CLOUD REGION (Hyderabad AZ-3)                             |
 |  +-----------------------+     +-----------------------+     +------------------------------+  |
 |  | Standby Ingress NLB   | --> | Warm Standby Pods     | --> | Patroni Read Replica Standby |  |
 |  | (DNS Route53 Failover)|     | (Autoscaling Min 2)   |     | (Asynchronous Cascading WAL) |  |
 |  +-----------------------+     +-----------------------+     +------------------------------+  |
 +------------------------------------------------------------------------------------------------+
                                       ^
                                       | Zstandard Encrypted Mutation Sync
 +------------------------------------------------------------------------------------------------+
 |                          NAMMA CLINIC PHYSICAL EDGE DEPLOYMENT (x183)                          |
 |  +--------------------------+    +--------------------------+    +--------------------------+  |
 |  | Primary Edge Appliance   |    | Hot-Standby Swap Box     |    | Line-Interactive UPS     |  |
 |  | (Intel N100 / RAID1 NVMe)| -> | (Pre-Configured In-Box)  |    | (1200VA / 120min Runtime)|  |
 |  | (SQLite WAL / PWA Server)|    | (Identical Hardware MAC) |    | (NUT USB Graceful Daemon)|  |
 |  +--------------------------+    +--------------------------+    +--------------------------+  |
 +------------------------------------------------------------------------------------------------+
```

## 03. Business Impact Analysis (BIA) Across All 30 Platform Modules
Exhaustive criticality classification, financial/clinical impact analysis, maximum tolerable downtime (MTD), RTO, and RPO across all 30 platform modules:

| Tier | Classification Description | Target RTO | Target RPO | Maximum Tolerable Downtime (MTD) |
| :--- | :--- | :---: | :---: | :---: |
| **Tier 1: Mission-Critical** | Failure causes immediate clinical harm, risk to citizen life, or halts clinic triage and consultation. | < 15 Minutes | < 5 Minutes | < 1 Hour |
| **Tier 2: Operational** | Failure degrades operational efficiency, queues staff workflows, but paper/cached workarounds exist. | < 1 Hour | < 15 Minutes | < 4 Hours |
| **Tier 3: Management & BI** | Failure disrupts municipal reporting, administrative oversight, or analytics; zero clinical impact. | < 4 Hours | < 1 Hour | < 24 Hours |
| **Tier 4: Archival & Research** | Failure delays long-term research extraction or statutory archival sync; negligible immediate impact. | < 24 Hours | < 24 Hours | < 7 Days |

### 03.1 Detailed BIA Assessment by Module (MODULE-001 to MODULE-030)

| Module ID | Module Name | BIA Tier | Target RTO | Target RPO | Max Downtime (MTD) | Clinical & Operational Impact | Continuity Workaround |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| `MODULE-001` | **Staff Authentication & MFA Engine** | Tier 1 (Mission-Critical) | < 15 min | < 5 min | < 1 hour | CRITICAL: Direct patient care stoppage; inability to triage, prescribe, or dispatch 108 ambulances. | Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered. |
| `MODULE-002` | **Role-Based Access Control (RBAC) & Entitlements** | Tier 1 (Mission-Critical) | < 15 min | < 5 min | < 1 hour | CRITICAL: Direct patient care stoppage; inability to triage, prescribe, or dispatch 108 ambulances. | Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered. |
| `MODULE-003` | **Healthcare Facility & Organizational Hierarchy** | Tier 1 (Mission-Critical) | < 15 min | < 5 min | < 1 hour | CRITICAL: Direct patient care stoppage; inability to triage, prescribe, or dispatch 108 ambulances. | Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered. |
| `MODULE-004` | **Clinical & Administrative Staff Directory** | Tier 1 (Mission-Critical) | < 15 min | < 5 min | < 1 hour | CRITICAL: Direct patient care stoppage; inability to triage, prescribe, or dispatch 108 ambulances. | Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered. |
| `MODULE-005` | **Patient Registration, Demographics & ABHA Minting** | Tier 1 (Mission-Critical) | < 15 min | < 5 min | < 1 hour | CRITICAL: Direct patient care stoppage; inability to triage, prescribe, or dispatch 108 ambulances. | Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered. |
| `MODULE-006` | **Informed Clinical Consent & DPDP Data Privacy** | Tier 1 (Mission-Critical) | < 15 min | < 5 min | < 1 hour | CRITICAL: Direct patient care stoppage; inability to triage, prescribe, or dispatch 108 ambulances. | Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered. |
| `MODULE-007` | **Patient Token Generation & Station Routing** | Tier 1 (Mission-Critical) | < 15 min | < 5 min | < 1 hour | CRITICAL: Direct patient care stoppage; inability to triage, prescribe, or dispatch 108 ambulances. | Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered. |
| `MODULE-008` | **Dynamic Queue Orchestration & Display Boards** | Tier 1 (Mission-Critical) | < 15 min | < 5 min | < 1 hour | CRITICAL: Direct patient care stoppage; inability to triage, prescribe, or dispatch 108 ambulances. | Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered. |
| `MODULE-009` | **Doctor EMR Console & Clinical SOAP Encounter** | Tier 1 (Mission-Critical) | < 15 min | < 5 min | < 1 hour | CRITICAL: Direct patient care stoppage; inability to triage, prescribe, or dispatch 108 ambulances. | Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered. |
| `MODULE-010` | **ICD-10 & SNOMED CT Clinical Diagnosis Coding** | Tier 1 (Mission-Critical) | < 15 min | < 5 min | < 1 hour | CRITICAL: Direct patient care stoppage; inability to triage, prescribe, or dispatch 108 ambulances. | Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered. |
| `MODULE-011` | **Electronic Prescription (e-Rx) & Drug Safety Engine** | Tier 1 (Mission-Critical) | < 15 min | < 5 min | < 1 hour | CRITICAL: Direct patient care stoppage; inability to triage, prescribe, or dispatch 108 ambulances. | Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered. |
| `MODULE-012` | **Point-of-Care Laboratory Testing & Diagnostic Orders** | Tier 2 (Operational) | < 1 hour | < 15 min | < 4 hours | HIGH: Supply chain stockout risk, lab order logging delays, deferred non-emergency appointment scheduling. | Queue mutations locally; batch process lab slips; manual formulary paper logs. |
| `MODULE-013` | **Pharmacy Dispensing & 2D Barcode Verification** | Tier 2 (Operational) | < 1 hour | < 15 min | < 4 hours | HIGH: Supply chain stockout risk, lab order logging delays, deferred non-emergency appointment scheduling. | Queue mutations locally; batch process lab slips; manual formulary paper logs. |
| `MODULE-014` | **Real-Time Batch Inventory & FEFO Stock Ledger** | Tier 2 (Operational) | < 1 hour | < 15 min | < 4 hours | HIGH: Supply chain stockout risk, lab order logging delays, deferred non-emergency appointment scheduling. | Queue mutations locally; batch process lab slips; manual formulary paper logs. |
| `MODULE-015` | **Drug Indent Generation, Receiving & Cold-Chain Intake** | Tier 2 (Operational) | < 1 hour | < 15 min | < 4 hours | HIGH: Supply chain stockout risk, lab order logging delays, deferred non-emergency appointment scheduling. | Queue mutations locally; batch process lab slips; manual formulary paper logs. |
| `MODULE-016` | **Essential Medicine List (EML) & Formulary Master** | Tier 2 (Operational) | < 1 hour | < 15 min | < 4 hours | HIGH: Supply chain stockout risk, lab order logging delays, deferred non-emergency appointment scheduling. | Queue mutations locally; batch process lab slips; manual formulary paper logs. |
| `MODULE-017` | **Secondary Referral & 108 Emergency EMS Transit** | Tier 2 (Operational) | < 1 hour | < 15 min | < 4 hours | HIGH: Supply chain stockout risk, lab order logging delays, deferred non-emergency appointment scheduling. | Queue mutations locally; batch process lab slips; manual formulary paper logs. |
| `MODULE-018` | **NCD Longitudinal Follow-Up & Recall Management** | Tier 2 (Operational) | < 1 hour | < 15 min | < 4 hours | HIGH: Supply chain stockout risk, lab order logging delays, deferred non-emergency appointment scheduling. | Queue mutations locally; batch process lab slips; manual formulary paper logs. |
| `MODULE-019` | **Citizen Multichannel Notifications & Health Reminders** | Tier 2 (Operational) | < 1 hour | < 15 min | < 4 hours | HIGH: Supply chain stockout risk, lab order logging delays, deferred non-emergency appointment scheduling. | Queue mutations locally; batch process lab slips; manual formulary paper logs. |
| `MODULE-020` | **Citizen Feedback, Grievance & Ombudsman Redressal** | Tier 1 (Mission-Critical) | < 15 min | < 5 min | < 1 hour | CRITICAL: Direct patient care stoppage; inability to triage, prescribe, or dispatch 108 ambulances. | Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered. |
| `MODULE-021` | **Cryptographic Audit Ledger & Compliance (WORM)** | Tier 2 (Operational) | < 1 hour | < 15 min | < 4 hours | HIGH: Supply chain stockout risk, lab order logging delays, deferred non-emergency appointment scheduling. | Queue mutations locally; batch process lab slips; manual formulary paper logs. |
| `MODULE-022` | **Zonal & Ward Operational KPI Dashboards** | Tier 2 (Operational) | < 1 hour | < 15 min | < 4 hours | HIGH: Supply chain stockout risk, lab order logging delays, deferred non-emergency appointment scheduling. | Queue mutations locally; batch process lab slips; manual formulary paper logs. |
| `MODULE-023` | **Safe AI/ML Clinical Decision Support Safeguards** | Tier 3 (Management & BI) | < 4 hours | < 1 hour | < 24 hours | MODERATE: Municipal epidemiological dashboards stale; delayed administrative KPI reporting. | Cloud replica recovery; defer analytical CDC streaming until primary database stabilizes. |
| `MODULE-024` | **National Health ABDM Ecosystem Interoperability** | Tier 3 (Management & BI) | < 4 hours | < 1 hour | < 24 hours | MODERATE: Municipal epidemiological dashboards stale; delayed administrative KPI reporting. | Cloud replica recovery; defer analytical CDC streaming until primary database stabilizes. |
| `MODULE-025` | **Autonomous Offline Edge Engine & Conflict Replay** | Tier 3 (Management & BI) | < 4 hours | < 1 hour | < 24 hours | MODERATE: Municipal epidemiological dashboards stale; delayed administrative KPI reporting. | Cloud replica recovery; defer analytical CDC streaming until primary database stabilizes. |
| `MODULE-026` | **Master System Administration & Feature Flagging** | Tier 3 (Management & BI) | < 4 hours | < 1 hour | < 24 hours | MODERATE: Municipal epidemiological dashboards stale; delayed administrative KPI reporting. | Cloud replica recovery; defer analytical CDC streaming until primary database stabilizes. |
| `MODULE-027` | **State Health HMIS & Statutory Disease Reporting** | Tier 3 (Management & BI) | < 4 hours | < 1 hour | < 24 hours | MODERATE: Municipal epidemiological dashboards stale; delayed administrative KPI reporting. | Cloud replica recovery; defer analytical CDC streaming until primary database stabilizes. |
| `MODULE-028` | **Facility Operations Helpdesk & Incident Dispatch** | Tier 3 (Management & BI) | < 4 hours | < 1 hour | < 24 hours | MODERATE: Municipal epidemiological dashboards stale; delayed administrative KPI reporting. | Cloud replica recovery; defer analytical CDC streaming until primary database stabilizes. |
| `MODULE-029` | **Telemedicine & Specialist Tele-Consultation Bridge** | Tier 4 (Archival) | < 24 hours | < 24 hours | < 7 days | LOW: Archival compliance report delays; no operational impact. | Restore from cold WORM Glacier archive upon compute provisioning. |
| `MODULE-030` | **Municipal Pilot Command Center & Disaster Operations** | Tier 4 (Archival) | < 24 hours | < 24 hours | < 7 days | LOW: Archival compliance report delays; no operational impact. | Restore from cold WORM Glacier archive upon compute provisioning. |

#### BIA Profile: `MODULE-001` - Staff Authentication & MFA Engine
- **Criticality Tier:** Tier 1 (Mission-Critical)
- **Business Functions Governed:** Manages staff identities, Argon2id salted credentials, TOTP MFA challenges, session lifecycle, and cryptographic token issuance.
- **Recovery Time Objective (RTO):** < 15 min
- **Recovery Point Objective (RPO):** < 5 min
- **Maximum Tolerable Downtime (MTD):** < 1 hour
- **Clinical Impact of Outage:** Immediate risk to life; potential severe clinical deterioration during acute triage delays.
- **Financial & Regulatory Liability:** INR 500,000 per hour in municipal liability; statutory breach under Clinical Establishments Act.
- **Operational Continuity Strategy:** Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-004`, Data Entity `ARCH-DATA-001`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-001`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/auth/login` failing 3 consecutive health intervals.
- **Severity Score (S):** 9 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 2 / 10
- **Calculated Risk Priority Number (RPN):** 54 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-001` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-004` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-001` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-001 (ARCH-DATA-001)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-001 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-001 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-001;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Staff Authentication & MFA Engine is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Staff Authentication & MFA Engine ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/auth/login`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_001_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-001`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-004 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-001 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/auth/login -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-002` - Role-Based Access Control (RBAC) & Entitlements
- **Criticality Tier:** Tier 1 (Mission-Critical)
- **Business Functions Governed:** Defines and enforces granular permissions, capability claims, and segregation of duties (SOD-001) across 30 clinical and administrative roles.
- **Recovery Time Objective (RTO):** < 15 min
- **Recovery Point Objective (RPO):** < 5 min
- **Maximum Tolerable Downtime (MTD):** < 1 hour
- **Clinical Impact of Outage:** Immediate risk to life; potential severe clinical deterioration during acute triage delays.
- **Financial & Regulatory Liability:** INR 500,000 per hour in municipal liability; statutory breach under Clinical Establishments Act.
- **Operational Continuity Strategy:** Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-004`, Data Entity `ARCH-DATA-002`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-002`.
- **Detection Mechanism:** Prometheus synthetic probe `GET /api/v1/rbac/roles` failing 3 consecutive health intervals.
- **Severity Score (S):** 9 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 2 / 10
- **Calculated Risk Priority Number (RPN):** 54 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-002` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-004` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-002` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-002 (ARCH-DATA-002)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-002 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-002 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-002;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Role-Based Access Control (RBAC) & Entitlements is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Role-Based Access Control (RBAC) & Entitlements ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `GET /api/v1/rbac/roles`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_002_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-002`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-004 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-002 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/rbac/roles -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-003` - Healthcare Facility & Organizational Hierarchy
- **Criticality Tier:** Tier 1 (Mission-Critical)
- **Business Functions Governed:** Maintains the municipal hierarchy of 183 clinics, 8 BBMP zones, 225 wards, room allocations, and operational hours.
- **Recovery Time Objective (RTO):** < 15 min
- **Recovery Point Objective (RPO):** < 5 min
- **Maximum Tolerable Downtime (MTD):** < 1 hour
- **Clinical Impact of Outage:** Immediate risk to life; potential severe clinical deterioration during acute triage delays.
- **Financial & Regulatory Liability:** INR 500,000 per hour in municipal liability; statutory breach under Clinical Establishments Act.
- **Operational Continuity Strategy:** Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-002`, Data Entity `ARCH-DATA-003`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-003`.
- **Detection Mechanism:** Prometheus synthetic probe `GET /api/v1/facilities/clinics` failing 3 consecutive health intervals.
- **Severity Score (S):** 9 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 2 / 10
- **Calculated Risk Priority Number (RPN):** 54 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-003` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-002` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-003` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-003 (ARCH-DATA-003)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-003 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-003 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-003;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Healthcare Facility & Organizational Hierarchy is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Healthcare Facility & Organizational Hierarchy ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `GET /api/v1/facilities/clinics`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_003_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-003`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-002 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-003 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/facilities/clinics -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-004` - Clinical & Administrative Staff Directory
- **Criticality Tier:** Tier 1 (Mission-Critical)
- **Business Functions Governed:** Maintains professional profiles, medical registration council numbers (KMC), duty rosters, and shift schedules for clinic personnel.
- **Recovery Time Objective (RTO):** < 15 min
- **Recovery Point Objective (RPO):** < 5 min
- **Maximum Tolerable Downtime (MTD):** < 1 hour
- **Clinical Impact of Outage:** Immediate risk to life; potential severe clinical deterioration during acute triage delays.
- **Financial & Regulatory Liability:** INR 500,000 per hour in municipal liability; statutory breach under Clinical Establishments Act.
- **Operational Continuity Strategy:** Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-004`, Data Entity `ARCH-DATA-004`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-004`.
- **Detection Mechanism:** Prometheus synthetic probe `GET /api/v1/staff/directory` failing 3 consecutive health intervals.
- **Severity Score (S):** 9 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 2 / 10
- **Calculated Risk Priority Number (RPN):** 54 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-004` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-004` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-004` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-004 (ARCH-DATA-004)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-004 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-004 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-004;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Clinical & Administrative Staff Directory is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Clinical & Administrative Staff Directory ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `GET /api/v1/staff/directory`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_004_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-004`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-004 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-004 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/staff/directory -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-005` - Patient Registration, Demographics & ABHA Minting
- **Criticality Tier:** Tier 1 (Mission-Critical)
- **Business Functions Governed:** Captures citizen demographic profiles, performs phonetic deduplication, mints municipal health IDs, and binds national ABHA numbers.
- **Recovery Time Objective (RTO):** < 15 min
- **Recovery Point Objective (RPO):** < 5 min
- **Maximum Tolerable Downtime (MTD):** < 1 hour
- **Clinical Impact of Outage:** Immediate risk to life; potential severe clinical deterioration during acute triage delays.
- **Financial & Regulatory Liability:** INR 500,000 per hour in municipal liability; statutory breach under Clinical Establishments Act.
- **Operational Continuity Strategy:** Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-005`, Data Entity `ARCH-DATA-005`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-005`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/patients/register` failing 3 consecutive health intervals.
- **Severity Score (S):** 9 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 2 / 10
- **Calculated Risk Priority Number (RPN):** 54 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-005` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-005` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-005` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-005 (ARCH-DATA-005)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-005 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-005 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-005;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Patient Registration, Demographics & ABHA Minting is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Patient Registration, Demographics & ABHA Minting ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/patients/register`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_005_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-005`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-005 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-005 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/patients/register -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-006` - Informed Clinical Consent & DPDP Data Privacy
- **Criticality Tier:** Tier 1 (Mission-Critical)
- **Business Functions Governed:** Records affirmative citizen consent for clinical treatment, tele-consultation, and health data sharing per DPDP Act 2023.
- **Recovery Time Objective (RTO):** < 15 min
- **Recovery Point Objective (RPO):** < 5 min
- **Maximum Tolerable Downtime (MTD):** < 1 hour
- **Clinical Impact of Outage:** Immediate risk to life; potential severe clinical deterioration during acute triage delays.
- **Financial & Regulatory Liability:** INR 500,000 per hour in municipal liability; statutory breach under Clinical Establishments Act.
- **Operational Continuity Strategy:** Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-005`, Data Entity `ARCH-DATA-006`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-006`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/consent/record` failing 3 consecutive health intervals.
- **Severity Score (S):** 9 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 2 / 10
- **Calculated Risk Priority Number (RPN):** 54 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-006` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-005` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-006` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-006 (ARCH-DATA-006)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-006 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-006 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-006;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Informed Clinical Consent & DPDP Data Privacy is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Informed Clinical Consent & DPDP Data Privacy ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/consent/record`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_006_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-006`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-005 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-006 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/consent/record -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-007` - Patient Token Generation & Station Routing
- **Criticality Tier:** Tier 1 (Mission-Critical)
- **Business Functions Governed:** Mints daily clinic visit tokens (General, Senior/Vulnerable, Emergency), prints 80mm thermal slips, and routes to initial station.
- **Recovery Time Objective (RTO):** < 15 min
- **Recovery Point Objective (RPO):** < 5 min
- **Maximum Tolerable Downtime (MTD):** < 1 hour
- **Clinical Impact of Outage:** Immediate risk to life; potential severe clinical deterioration during acute triage delays.
- **Financial & Regulatory Liability:** INR 500,000 per hour in municipal liability; statutory breach under Clinical Establishments Act.
- **Operational Continuity Strategy:** Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-006`, Data Entity `ARCH-DATA-007`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-007`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/tokens/issue` failing 3 consecutive health intervals.
- **Severity Score (S):** 9 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 2 / 10
- **Calculated Risk Priority Number (RPN):** 54 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-007` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-006` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-007` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-007 (ARCH-DATA-007)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-007 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-007 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-007;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Patient Token Generation & Station Routing is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Patient Token Generation & Station Routing ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/tokens/issue`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_007_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-007`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-006 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-007 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/tokens/issue -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-008` - Dynamic Queue Orchestration & Display Boards
- **Criticality Tier:** Tier 1 (Mission-Critical)
- **Business Functions Governed:** Manages dynamic multi-room queues, broadcasts next-patient calls to waiting hall TV screens via MQTT, and calculates wait times.
- **Recovery Time Objective (RTO):** < 15 min
- **Recovery Point Objective (RPO):** < 5 min
- **Maximum Tolerable Downtime (MTD):** < 1 hour
- **Clinical Impact of Outage:** Immediate risk to life; potential severe clinical deterioration during acute triage delays.
- **Financial & Regulatory Liability:** INR 500,000 per hour in municipal liability; statutory breach under Clinical Establishments Act.
- **Operational Continuity Strategy:** Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-006`, Data Entity `ARCH-DATA-008`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-008`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/queues/call-next` failing 3 consecutive health intervals.
- **Severity Score (S):** 9 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 2 / 10
- **Calculated Risk Priority Number (RPN):** 54 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-008` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-006` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-008` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-008 (ARCH-DATA-008)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-008 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-008 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-008;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Dynamic Queue Orchestration & Display Boards is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Dynamic Queue Orchestration & Display Boards ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/queues/call-next`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_008_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-008`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-006 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-008 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/queues/call-next -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-009` - Doctor EMR Console & Clinical SOAP Encounter
- **Criticality Tier:** Tier 1 (Mission-Critical)
- **Business Functions Governed:** Provides physician consultation interface for capturing Subjective symptoms, Objective vitals/findings, Assessment, and Plan.
- **Recovery Time Objective (RTO):** < 15 min
- **Recovery Point Objective (RPO):** < 5 min
- **Maximum Tolerable Downtime (MTD):** < 1 hour
- **Clinical Impact of Outage:** Immediate risk to life; potential severe clinical deterioration during acute triage delays.
- **Financial & Regulatory Liability:** INR 500,000 per hour in municipal liability; statutory breach under Clinical Establishments Act.
- **Operational Continuity Strategy:** Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-007`, Data Entity `ARCH-DATA-009`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-009`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/encounters/start` failing 3 consecutive health intervals.
- **Severity Score (S):** 9 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 2 / 10
- **Calculated Risk Priority Number (RPN):** 54 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-009` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-007` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-009` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-009 (ARCH-DATA-009)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-009 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-009 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-009;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Doctor EMR Console & Clinical SOAP Encounter is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Doctor EMR Console & Clinical SOAP Encounter ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/encounters/start`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_009_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-009`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-007 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-009 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/encounters/start -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-010` - ICD-10 & SNOMED CT Clinical Diagnosis Coding
- **Criticality Tier:** Tier 1 (Mission-Critical)
- **Business Functions Governed:** Enables fast bilingual autocomplete of clinical concepts mapped to SNOMED CT and statutory ICD-10 diagnostic codes.
- **Recovery Time Objective (RTO):** < 15 min
- **Recovery Point Objective (RPO):** < 5 min
- **Maximum Tolerable Downtime (MTD):** < 1 hour
- **Clinical Impact of Outage:** Immediate risk to life; potential severe clinical deterioration during acute triage delays.
- **Financial & Regulatory Liability:** INR 500,000 per hour in municipal liability; statutory breach under Clinical Establishments Act.
- **Operational Continuity Strategy:** Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-007`, Data Entity `ARCH-DATA-010`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-010`.
- **Detection Mechanism:** Prometheus synthetic probe `GET /api/v1/terminology/search` failing 3 consecutive health intervals.
- **Severity Score (S):** 9 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 2 / 10
- **Calculated Risk Priority Number (RPN):** 54 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-010` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-007` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-010` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-010 (ARCH-DATA-010)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-010 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-010 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-010;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: ICD-10 & SNOMED CT Clinical Diagnosis Coding is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: ICD-10 & SNOMED CT Clinical Diagnosis Coding ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `GET /api/v1/terminology/search`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_010_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-010`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-007 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-010 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/terminology/search -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-011` - Electronic Prescription (e-Rx) & Drug Safety Engine
- **Criticality Tier:** Tier 1 (Mission-Critical)
- **Business Functions Governed:** Authorizes e-prescriptions from essential drug formulary, evaluates drug-drug interactions, and checks pediatric dosage limits.
- **Recovery Time Objective (RTO):** < 15 min
- **Recovery Point Objective (RPO):** < 5 min
- **Maximum Tolerable Downtime (MTD):** < 1 hour
- **Clinical Impact of Outage:** Immediate risk to life; potential severe clinical deterioration during acute triage delays.
- **Financial & Regulatory Liability:** INR 500,000 per hour in municipal liability; statutory breach under Clinical Establishments Act.
- **Operational Continuity Strategy:** Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-008`, Data Entity `ARCH-DATA-011`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-011`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/prescriptions/create` failing 3 consecutive health intervals.
- **Severity Score (S):** 9 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 2 / 10
- **Calculated Risk Priority Number (RPN):** 54 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-011` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-008` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-011` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-011 (ARCH-DATA-011)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-011 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-011 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-011;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Electronic Prescription (e-Rx) & Drug Safety Engine is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Electronic Prescription (e-Rx) & Drug Safety Engine ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/prescriptions/create`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_011_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-011`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-008 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-011 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/prescriptions/create -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-012` - Point-of-Care Laboratory Testing & Diagnostic Orders
- **Criticality Tier:** Tier 2 (Operational)
- **Business Functions Governed:** Manages orders and results for 58 rapid point-of-care laboratory diagnostic tests, specimen labelling, and panic value alerts.
- **Recovery Time Objective (RTO):** < 1 hour
- **Recovery Point Objective (RPO):** < 15 min
- **Maximum Tolerable Downtime (MTD):** < 4 hours
- **Clinical Impact of Outage:** Delayed diagnostic insights and outpatient medication fulfillment delays.
- **Financial & Regulatory Liability:** INR 100,000 per hour in wasted staff labor and logistics expediting penalties.
- **Operational Continuity Strategy:** Queue mutations locally; batch process lab slips; manual formulary paper logs.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-010`, Data Entity `ARCH-DATA-012`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-012`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/lab/orders/create` failing 3 consecutive health intervals.
- **Severity Score (S):** 6 / 10 | **Occurrence Score (O):** 4 / 10 | **Detection Score (D):** 3 / 10
- **Calculated Risk Priority Number (RPN):** 72 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-012` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-010` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-012` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-012 (ARCH-DATA-012)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-012 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-012 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-012;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Point-of-Care Laboratory Testing & Diagnostic Orders is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Point-of-Care Laboratory Testing & Diagnostic Orders ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/lab/orders/create`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_012_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-012`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-010 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-012 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/lab/orders/create -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-013` - Pharmacy Dispensing & 2D Barcode Verification
- **Criticality Tier:** Tier 2 (Operational)
- **Business Functions Governed:** Guides pharmacist through prescription dispensation, validates batch expiry via 2D DataMatrix scanning, and prints medicine slips.
- **Recovery Time Objective (RTO):** < 1 hour
- **Recovery Point Objective (RPO):** < 15 min
- **Maximum Tolerable Downtime (MTD):** < 4 hours
- **Clinical Impact of Outage:** Delayed diagnostic insights and outpatient medication fulfillment delays.
- **Financial & Regulatory Liability:** INR 100,000 per hour in wasted staff labor and logistics expediting penalties.
- **Operational Continuity Strategy:** Queue mutations locally; batch process lab slips; manual formulary paper logs.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-009`, Data Entity `ARCH-DATA-013`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-013`.
- **Detection Mechanism:** Prometheus synthetic probe `GET /api/v1/pharmacy/queue` failing 3 consecutive health intervals.
- **Severity Score (S):** 6 / 10 | **Occurrence Score (O):** 4 / 10 | **Detection Score (D):** 3 / 10
- **Calculated Risk Priority Number (RPN):** 72 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-013` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-009` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-013` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-013 (ARCH-DATA-013)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-013 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-013 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-013;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Pharmacy Dispensing & 2D Barcode Verification is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Pharmacy Dispensing & 2D Barcode Verification ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `GET /api/v1/pharmacy/queue`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_013_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-013`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-009 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-013 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/pharmacy/queue -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-014` - Real-Time Batch Inventory & FEFO Stock Ledger
- **Criticality Tier:** Tier 2 (Operational)
- **Business Functions Governed:** Tracks stock levels per batch, enforces First-Expiry-First-Out allocation, monitors storage bins, and flags near-expiry items.
- **Recovery Time Objective (RTO):** < 1 hour
- **Recovery Point Objective (RPO):** < 15 min
- **Maximum Tolerable Downtime (MTD):** < 4 hours
- **Clinical Impact of Outage:** Delayed diagnostic insights and outpatient medication fulfillment delays.
- **Financial & Regulatory Liability:** INR 100,000 per hour in wasted staff labor and logistics expediting penalties.
- **Operational Continuity Strategy:** Queue mutations locally; batch process lab slips; manual formulary paper logs.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-009`, Data Entity `ARCH-DATA-014`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-014`.
- **Detection Mechanism:** Prometheus synthetic probe `GET /api/v1/inventory/batches` failing 3 consecutive health intervals.
- **Severity Score (S):** 6 / 10 | **Occurrence Score (O):** 4 / 10 | **Detection Score (D):** 3 / 10
- **Calculated Risk Priority Number (RPN):** 72 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-014` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-009` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-014` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-014 (ARCH-DATA-014)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-014 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-014 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-014;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Real-Time Batch Inventory & FEFO Stock Ledger is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Real-Time Batch Inventory & FEFO Stock Ledger ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `GET /api/v1/inventory/batches`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_014_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-014`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-009 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-014 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/inventory/batches -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-015` - Drug Indent Generation, Receiving & Cold-Chain Intake
- **Criticality Tier:** Tier 2 (Operational)
- **Business Functions Governed:** Automates monthly replenishment indents to central warehouse (KDLWS), verifies receiving manifests, and logs cold-chain temps.
- **Recovery Time Objective (RTO):** < 1 hour
- **Recovery Point Objective (RPO):** < 15 min
- **Maximum Tolerable Downtime (MTD):** < 4 hours
- **Clinical Impact of Outage:** Delayed diagnostic insights and outpatient medication fulfillment delays.
- **Financial & Regulatory Liability:** INR 100,000 per hour in wasted staff labor and logistics expediting penalties.
- **Operational Continuity Strategy:** Queue mutations locally; batch process lab slips; manual formulary paper logs.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-009`, Data Entity `ARCH-DATA-015`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-015`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/indents/generate` failing 3 consecutive health intervals.
- **Severity Score (S):** 6 / 10 | **Occurrence Score (O):** 4 / 10 | **Detection Score (D):** 3 / 10
- **Calculated Risk Priority Number (RPN):** 72 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-015` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-009` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-015` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-015 (ARCH-DATA-015)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-015 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-015 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-015;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Drug Indent Generation, Receiving & Cold-Chain Intake is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Drug Indent Generation, Receiving & Cold-Chain Intake ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/indents/generate`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_015_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-015`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-009 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-015 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/indents/generate -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-016` - Essential Medicine List (EML) & Formulary Master
- **Criticality Tier:** Tier 2 (Operational)
- **Business Functions Governed:** Maintains the municipal primary care drug formulary, generic-brand mappings, therapeutic categories, and dosage forms.
- **Recovery Time Objective (RTO):** < 1 hour
- **Recovery Point Objective (RPO):** < 15 min
- **Maximum Tolerable Downtime (MTD):** < 4 hours
- **Clinical Impact of Outage:** Delayed diagnostic insights and outpatient medication fulfillment delays.
- **Financial & Regulatory Liability:** INR 100,000 per hour in wasted staff labor and logistics expediting penalties.
- **Operational Continuity Strategy:** Queue mutations locally; batch process lab slips; manual formulary paper logs.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-009`, Data Entity `ARCH-DATA-016`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-016`.
- **Detection Mechanism:** Prometheus synthetic probe `GET /api/v1/formulary/drugs` failing 3 consecutive health intervals.
- **Severity Score (S):** 6 / 10 | **Occurrence Score (O):** 4 / 10 | **Detection Score (D):** 3 / 10
- **Calculated Risk Priority Number (RPN):** 72 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-016` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-009` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-016` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-016 (ARCH-DATA-016)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-016 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-016 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-016;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Essential Medicine List (EML) & Formulary Master is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Essential Medicine List (EML) & Formulary Master ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `GET /api/v1/formulary/drugs`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_016_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-016`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-009 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-016 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/formulary/drugs -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-017` - Secondary Referral & 108 Emergency EMS Transit
- **Criticality Tier:** Tier 2 (Operational)
- **Business Functions Governed:** Assembles referral dossiers for secondary hospitals, dispatches 108 emergency ambulance requests, and tracks patient handover.
- **Recovery Time Objective (RTO):** < 1 hour
- **Recovery Point Objective (RPO):** < 15 min
- **Maximum Tolerable Downtime (MTD):** < 4 hours
- **Clinical Impact of Outage:** Delayed diagnostic insights and outpatient medication fulfillment delays.
- **Financial & Regulatory Liability:** INR 100,000 per hour in wasted staff labor and logistics expediting penalties.
- **Operational Continuity Strategy:** Queue mutations locally; batch process lab slips; manual formulary paper logs.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-011`, Data Entity `ARCH-DATA-017`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-017`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/referrals/create` failing 3 consecutive health intervals.
- **Severity Score (S):** 6 / 10 | **Occurrence Score (O):** 4 / 10 | **Detection Score (D):** 3 / 10
- **Calculated Risk Priority Number (RPN):** 72 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-017` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-011` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-017` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-017 (ARCH-DATA-017)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-017 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-017 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-017;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Secondary Referral & 108 Emergency EMS Transit is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Secondary Referral & 108 Emergency EMS Transit ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/referrals/create`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_017_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-017`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-011 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-017 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/referrals/create -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-018` - NCD Longitudinal Follow-Up & Recall Management
- **Criticality Tier:** Tier 2 (Operational)
- **Business Functions Governed:** Maintains disease registries for hypertension, diabetes, and mental health; tracks follow-up compliance and flags defaulters.
- **Recovery Time Objective (RTO):** < 1 hour
- **Recovery Point Objective (RPO):** < 15 min
- **Maximum Tolerable Downtime (MTD):** < 4 hours
- **Clinical Impact of Outage:** Delayed diagnostic insights and outpatient medication fulfillment delays.
- **Financial & Regulatory Liability:** INR 100,000 per hour in wasted staff labor and logistics expediting penalties.
- **Operational Continuity Strategy:** Queue mutations locally; batch process lab slips; manual formulary paper logs.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-012`, Data Entity `ARCH-DATA-018`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-018`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/ncd/enroll` failing 3 consecutive health intervals.
- **Severity Score (S):** 6 / 10 | **Occurrence Score (O):** 4 / 10 | **Detection Score (D):** 3 / 10
- **Calculated Risk Priority Number (RPN):** 72 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-018` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-012` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-018` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-018 (ARCH-DATA-018)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-018 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-018 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-018;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: NCD Longitudinal Follow-Up & Recall Management is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: NCD Longitudinal Follow-Up & Recall Management ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/ncd/enroll`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_018_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-018`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-012 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-018 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/ncd/enroll -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-019` - Citizen Multichannel Notifications & Health Reminders
- **Criticality Tier:** Tier 2 (Operational)
- **Business Functions Governed:** Dispatches bilingual SMS and WhatsApp reminders for visit follow-ups, test result availability, and vaccination camps.
- **Recovery Time Objective (RTO):** < 1 hour
- **Recovery Point Objective (RPO):** < 15 min
- **Maximum Tolerable Downtime (MTD):** < 4 hours
- **Clinical Impact of Outage:** Delayed diagnostic insights and outpatient medication fulfillment delays.
- **Financial & Regulatory Liability:** INR 100,000 per hour in wasted staff labor and logistics expediting penalties.
- **Operational Continuity Strategy:** Queue mutations locally; batch process lab slips; manual formulary paper logs.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-012`, Data Entity `ARCH-DATA-019`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-019`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/notifications/send` failing 3 consecutive health intervals.
- **Severity Score (S):** 6 / 10 | **Occurrence Score (O):** 4 / 10 | **Detection Score (D):** 3 / 10
- **Calculated Risk Priority Number (RPN):** 72 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-019` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-012` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-019` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-019 (ARCH-DATA-019)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-019 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-019 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-019;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Citizen Multichannel Notifications & Health Reminders is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Citizen Multichannel Notifications & Health Reminders ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/notifications/send`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_019_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-019`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-012 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-019 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/notifications/send -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-020` - Citizen Feedback, Grievance & Ombudsman Redressal
- **Criticality Tier:** Tier 1 (Mission-Critical)
- **Business Functions Governed:** Captures citizen feedback on tablet kiosks, tracks facility grievances (e.g. staff absence, drug shortages), and monitors SLAs.
- **Recovery Time Objective (RTO):** < 15 min
- **Recovery Point Objective (RPO):** < 5 min
- **Maximum Tolerable Downtime (MTD):** < 1 hour
- **Clinical Impact of Outage:** Immediate risk to life; potential severe clinical deterioration during acute triage delays.
- **Financial & Regulatory Liability:** INR 500,000 per hour in municipal liability; statutory breach under Clinical Establishments Act.
- **Operational Continuity Strategy:** Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-012`, Data Entity `ARCH-DATA-020`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-020`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/feedback/submit` failing 3 consecutive health intervals.
- **Severity Score (S):** 9 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 2 / 10
- **Calculated Risk Priority Number (RPN):** 54 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-020` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-012` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-020` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-020 (ARCH-DATA-020)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-020 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-020 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-020;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Citizen Feedback, Grievance & Ombudsman Redressal is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Citizen Feedback, Grievance & Ombudsman Redressal ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/feedback/submit`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_020_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-020`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-012 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-020 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/feedback/submit -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-021` - Cryptographic Audit Ledger & Compliance (WORM)
- **Criticality Tier:** Tier 2 (Operational)
- **Business Functions Governed:** Records immutable write-once-read-many (WORM) audit trails with SHA-256 HMAC hash chaining for all clinical and auth events.
- **Recovery Time Objective (RTO):** < 1 hour
- **Recovery Point Objective (RPO):** < 15 min
- **Maximum Tolerable Downtime (MTD):** < 4 hours
- **Clinical Impact of Outage:** Delayed diagnostic insights and outpatient medication fulfillment delays.
- **Financial & Regulatory Liability:** INR 100,000 per hour in wasted staff labor and logistics expediting penalties.
- **Operational Continuity Strategy:** Queue mutations locally; batch process lab slips; manual formulary paper logs.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-017`, Data Entity `ARCH-DATA-021`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-021`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/audit/log` failing 3 consecutive health intervals.
- **Severity Score (S):** 6 / 10 | **Occurrence Score (O):** 4 / 10 | **Detection Score (D):** 3 / 10
- **Calculated Risk Priority Number (RPN):** 72 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-021` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-017` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-021` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-021 (ARCH-DATA-021)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-021 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-021 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-021;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Cryptographic Audit Ledger & Compliance (WORM) is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Cryptographic Audit Ledger & Compliance (WORM) ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/audit/log`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_021_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-021`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-017 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-021 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/audit/log -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-022` - Zonal & Ward Operational KPI Dashboards
- **Criticality Tier:** Tier 2 (Operational)
- **Business Functions Governed:** Delivers real-time public health indicators, clinic footfalls, stockout alerts, and disease heatmaps to municipal health officers.
- **Recovery Time Objective (RTO):** < 1 hour
- **Recovery Point Objective (RPO):** < 15 min
- **Maximum Tolerable Downtime (MTD):** < 4 hours
- **Clinical Impact of Outage:** Delayed diagnostic insights and outpatient medication fulfillment delays.
- **Financial & Regulatory Liability:** INR 100,000 per hour in wasted staff labor and logistics expediting penalties.
- **Operational Continuity Strategy:** Queue mutations locally; batch process lab slips; manual formulary paper logs.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-015`, Data Entity `ARCH-DATA-022`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-022`.
- **Detection Mechanism:** Prometheus synthetic probe `GET /api/v1/analytics/kpis/summary` failing 3 consecutive health intervals.
- **Severity Score (S):** 6 / 10 | **Occurrence Score (O):** 4 / 10 | **Detection Score (D):** 3 / 10
- **Calculated Risk Priority Number (RPN):** 72 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-022` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-015` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-022` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-022 (ARCH-DATA-022)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-022 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-022 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-022;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Zonal & Ward Operational KPI Dashboards is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Zonal & Ward Operational KPI Dashboards ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `GET /api/v1/analytics/kpis/summary`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_022_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-022`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-015 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-022 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/analytics/kpis/summary -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-023` - Safe AI/ML Clinical Decision Support Safeguards
- **Criticality Tier:** Tier 3 (Management & BI)
- **Business Functions Governed:** Provides non-autonomous advisory machine learning predictions (syndromic fever clusters, defaulter risk) with mandatory doctor review.
- **Recovery Time Objective (RTO):** < 4 hours
- **Recovery Point Objective (RPO):** < 1 hour
- **Maximum Tolerable Downtime (MTD):** < 24 hours
- **Clinical Impact of Outage:** Zero immediate direct citizen harm; potential delayed detection of ward-level outbreak clusters.
- **Financial & Regulatory Liability:** INR 25,000 per hour in municipal reporting non-compliance fines.
- **Operational Continuity Strategy:** Cloud replica recovery; defer analytical CDC streaming until primary database stabilizes.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-016`, Data Entity `ARCH-DATA-023`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-023`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/ai/advisory/evaluate` failing 3 consecutive health intervals.
- **Severity Score (S):** 4 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 4 / 10
- **Calculated Risk Priority Number (RPN):** 48 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-023` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-016` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-023` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-023 (ARCH-DATA-023)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-023 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-023 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-023;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Safe AI/ML Clinical Decision Support Safeguards is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Safe AI/ML Clinical Decision Support Safeguards ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/ai/advisory/evaluate`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_023_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-023`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-016 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-023 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/ai/advisory/evaluate -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-024` - National Health ABDM Ecosystem Interoperability
- **Criticality Tier:** Tier 3 (Management & BI)
- **Business Functions Governed:** Bridges platform with Ayushman Bharat Digital Mission (M1: ABHA, M2: HIP Care Context, M3: HIU Consent) via FHIR R4.
- **Recovery Time Objective (RTO):** < 4 hours
- **Recovery Point Objective (RPO):** < 1 hour
- **Maximum Tolerable Downtime (MTD):** < 24 hours
- **Clinical Impact of Outage:** Zero immediate direct citizen harm; potential delayed detection of ward-level outbreak clusters.
- **Financial & Regulatory Liability:** INR 25,000 per hour in municipal reporting non-compliance fines.
- **Operational Continuity Strategy:** Cloud replica recovery; defer analytical CDC streaming until primary database stabilizes.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-014`, Data Entity `ARCH-DATA-024`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-024`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/abdm/m1/verify-abha` failing 3 consecutive health intervals.
- **Severity Score (S):** 4 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 4 / 10
- **Calculated Risk Priority Number (RPN):** 48 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-024` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-014` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-024` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-024 (ARCH-DATA-024)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-024 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-024 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-024;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: National Health ABDM Ecosystem Interoperability is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: National Health ABDM Ecosystem Interoperability ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/abdm/m1/verify-abha`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_024_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-024`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-014 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-024 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/abdm/m1/verify-abha -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-025` - Autonomous Offline Edge Engine & Conflict Replay
- **Criticality Tier:** Tier 3 (Management & BI)
- **Business Functions Governed:** Orchestrates 72-hour edge autonomy on SQLite WAL, journals local mutations with vector clocks, and replays deltas via CRDTs.
- **Recovery Time Objective (RTO):** < 4 hours
- **Recovery Point Objective (RPO):** < 1 hour
- **Maximum Tolerable Downtime (MTD):** < 24 hours
- **Clinical Impact of Outage:** Zero immediate direct citizen harm; potential delayed detection of ward-level outbreak clusters.
- **Financial & Regulatory Liability:** INR 25,000 per hour in municipal reporting non-compliance fines.
- **Operational Continuity Strategy:** Cloud replica recovery; defer analytical CDC streaming until primary database stabilizes.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-013`, Data Entity `ARCH-DATA-025`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-025`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/sync/handshake` failing 3 consecutive health intervals.
- **Severity Score (S):** 4 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 4 / 10
- **Calculated Risk Priority Number (RPN):** 48 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-025` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-013` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-025` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-025 (ARCH-DATA-025)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-025 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-025 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-025;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Autonomous Offline Edge Engine & Conflict Replay is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Autonomous Offline Edge Engine & Conflict Replay ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/sync/handshake`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_025_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-025`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-013 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-025 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/sync/handshake -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-026` - Master System Administration & Feature Flagging
- **Criticality Tier:** Tier 3 (Management & BI)
- **Business Functions Governed:** Provides system administrators with tenant configuration controls, dynamic feature toggles, maintenance mode, and log levels.
- **Recovery Time Objective (RTO):** < 4 hours
- **Recovery Point Objective (RPO):** < 1 hour
- **Maximum Tolerable Downtime (MTD):** < 24 hours
- **Clinical Impact of Outage:** Zero immediate direct citizen harm; potential delayed detection of ward-level outbreak clusters.
- **Financial & Regulatory Liability:** INR 25,000 per hour in municipal reporting non-compliance fines.
- **Operational Continuity Strategy:** Cloud replica recovery; defer analytical CDC streaming until primary database stabilizes.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-003`, Data Entity `ARCH-DATA-026`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-026`.
- **Detection Mechanism:** Prometheus synthetic probe `GET /api/v1/admin/configs` failing 3 consecutive health intervals.
- **Severity Score (S):** 4 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 4 / 10
- **Calculated Risk Priority Number (RPN):** 48 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-026` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-003` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-026` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-026 (ARCH-DATA-026)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-026 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-026 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-026;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Master System Administration & Feature Flagging is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Master System Administration & Feature Flagging ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `GET /api/v1/admin/configs`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_026_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-026`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-003 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-026 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/admin/configs -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-027` - State Health HMIS & Statutory Disease Reporting
- **Criticality Tier:** Tier 3 (Management & BI)
- **Business Functions Governed:** Compiles and exports statutory health indicator formats for Karnataka Health Management Information System and IDSP/IHIP.
- **Recovery Time Objective (RTO):** < 4 hours
- **Recovery Point Objective (RPO):** < 1 hour
- **Maximum Tolerable Downtime (MTD):** < 24 hours
- **Clinical Impact of Outage:** Zero immediate direct citizen harm; potential delayed detection of ward-level outbreak clusters.
- **Financial & Regulatory Liability:** INR 25,000 per hour in municipal reporting non-compliance fines.
- **Operational Continuity Strategy:** Cloud replica recovery; defer analytical CDC streaming until primary database stabilizes.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-015`, Data Entity `ARCH-DATA-027`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-027`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/reports/hmis/generate` failing 3 consecutive health intervals.
- **Severity Score (S):** 4 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 4 / 10
- **Calculated Risk Priority Number (RPN):** 48 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-027` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-015` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-027` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-027 (ARCH-DATA-027)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-027 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-027 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-027;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: State Health HMIS & Statutory Disease Reporting is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: State Health HMIS & Statutory Disease Reporting ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/reports/hmis/generate`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_027_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-027`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-015 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-027 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/reports/hmis/generate -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-028` - Facility Operations Helpdesk & Incident Dispatch
- **Criticality Tier:** Tier 3 (Management & BI)
- **Business Functions Governed:** Tracks hardware faults (printer jam, scanner failure, UPS battery warning) and dispatches field technicians across clinics.
- **Recovery Time Objective (RTO):** < 4 hours
- **Recovery Point Objective (RPO):** < 1 hour
- **Maximum Tolerable Downtime (MTD):** < 24 hours
- **Clinical Impact of Outage:** Zero immediate direct citizen harm; potential delayed detection of ward-level outbreak clusters.
- **Financial & Regulatory Liability:** INR 25,000 per hour in municipal reporting non-compliance fines.
- **Operational Continuity Strategy:** Cloud replica recovery; defer analytical CDC streaming until primary database stabilizes.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-002`, Data Entity `ARCH-DATA-028`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-028`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/helpdesk/tickets/create` failing 3 consecutive health intervals.
- **Severity Score (S):** 4 / 10 | **Occurrence Score (O):** 3 / 10 | **Detection Score (D):** 4 / 10
- **Calculated Risk Priority Number (RPN):** 48 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-028` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-002` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-028` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-028 (ARCH-DATA-028)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-028 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-028 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-028;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Facility Operations Helpdesk & Incident Dispatch is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Facility Operations Helpdesk & Incident Dispatch ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/helpdesk/tickets/create`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_028_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-028`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-002 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-028 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/helpdesk/tickets/create -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-029` - Telemedicine & Specialist Tele-Consultation Bridge
- **Criticality Tier:** Tier 4 (Archival)
- **Business Functions Governed:** Connects primary clinic doctors with secondary hospital specialists for real-time video consultation and joint review.
- **Recovery Time Objective (RTO):** < 24 hours
- **Recovery Point Objective (RPO):** < 24 hours
- **Maximum Tolerable Downtime (MTD):** < 7 days
- **Clinical Impact of Outage:** Negligible clinical impact; research queries and historical audits paused.
- **Financial & Regulatory Liability:** Zero immediate operational financial loss; audit delay penalties capped.
- **Operational Continuity Strategy:** Restore from cold WORM Glacier archive upon compute provisioning.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-007`, Data Entity `ARCH-DATA-029`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-029`.
- **Detection Mechanism:** Prometheus synthetic probe `POST /api/v1/telemed/sessions/initiate` failing 3 consecutive health intervals.
- **Severity Score (S):** 2 / 10 | **Occurrence Score (O):** 2 / 10 | **Detection Score (D):** 5 / 10
- **Calculated Risk Priority Number (RPN):** 20 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-029` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-007` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-029` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-029 (ARCH-DATA-029)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-029 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-029 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-029;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Telemedicine & Specialist Tele-Consultation Bridge is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Telemedicine & Specialist Tele-Consultation Bridge ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `POST /api/v1/telemed/sessions/initiate`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_029_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-029`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-007 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-029 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/telemed/sessions/initiate -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

#### BIA Profile: `MODULE-030` - Municipal Pilot Command Center & Disaster Operations
- **Criticality Tier:** Tier 4 (Archival)
- **Business Functions Governed:** Central command console for municipal epidemic surveillance, disaster mass casualty triage, and city-wide resource diversion.
- **Recovery Time Objective (RTO):** < 24 hours
- **Recovery Point Objective (RPO):** < 24 hours
- **Maximum Tolerable Downtime (MTD):** < 7 days
- **Clinical Impact of Outage:** Negligible clinical impact; research queries and historical audits paused.
- **Financial & Regulatory Liability:** Zero immediate operational financial loss; audit delay penalties capped.
- **Operational Continuity Strategy:** Restore from cold WORM Glacier archive upon compute provisioning.
- **Infrastructure Dependency Chain:** Container `ARCH-CONT-015`, Data Entity `ARCH-DATA-030`, Primary PostgreSQL Database, Edge SQLite Daemon.

##### Failure Mode and Effects Analysis (FMEA):
- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `ARCH-DATA-030`.
- **Detection Mechanism:** Prometheus synthetic probe `GET /api/v1/command/overview` failing 3 consecutive health intervals.
- **Severity Score (S):** 2 / 10 | **Occurrence Score (O):** 2 / 10 | **Detection Score (D):** 5 / 10
- **Calculated Risk Priority Number (RPN):** 20 (Threshold for mandatory automated runbook is RPN >= 40)

##### Data Invariants & State Guardrails:
1. **Cryptographic Sealing:** Any mutated state in `ARCH-DATA-030` must append an entry to the SHA-256 HMAC ledger.
2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.
3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.

##### Failure Prevention & Proactive Controls:
1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.
2. **Graceful Degradation:** When `ARCH-CONT-015` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.
3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `MODULE-030` traffic during compute resource stress.

##### State Reconciliation SQL Validation Script:
```sql
-- State integrity and orphan reconciliation query for MODULE-030 (ARCH-DATA-030)
BEGIN;
SELECT count(*) AS uncommitted_mutations FROM arch-data-030 WHERE sync_status = 'PENDING';
SELECT count(*) AS orphan_patient_records FROM arch-data-030 t
LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;
SELECT max(updated_at) AS latest_synced_mutation FROM arch-data-030;
COMMIT;
```

##### Bilingual Frontline Staff Degraded Operational Notice:
- **English Interface Notice:** *'ALERT: Municipal Pilot Command Center & Disaster Operations is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*
- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: Municipal Pilot Command Center & Disaster Operations ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*

##### Step-by-Step Degraded Mode & Recovery Procedure:
1. **Failure Detection & Triage:** Health probe monitors `GET /api/v1/command/overview`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_MODULE_030_UNAVAILABLE` fires.
2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `ARCH-DATA-030`.
3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.
4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment arch-cont-015 -n namma-prod`.
5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM arch-data-030 WHERE sync_status = 'PENDING';`.
6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080/api/v1/command/overview -H 'Authorization: Bearer test-token' || echo 'FAIL'`.

---

## 04. Cloud Infrastructure Disaster Recovery Architecture
Detailed multi-tier cloud failover architecture ensuring high availability and zero data loss:

### 04.1 Multi-AZ Patroni PostgreSQL Cluster Topology
1. **Cluster Consensus Engine:** Dedicated 3-node etcd cluster distributed across AZ-1 (Primary, Bengaluru), AZ-2 (Standby, Bengaluru), and AZ-3 (Witness, Hyderabad) preventing split-brain conditions.
2. **Synchronous Replication (AZ-1 to AZ-2):** `synchronous_commit = on` with `synchronous_standby_names = 'ANY 1 (patroni_az2)'`. Guarantees RPO = 0 across local metropolitan availability zones.
3. **Asynchronous Cross-Region Cascading Standby (AZ-3):** Standby node in Hyderabad streams continuous WAL updates from AZ-2 standby, guaranteeing RPO < 15 minutes during cataclysmic Bengaluru metropolitan grid failure.
4. **Automated Leader Election:** In the event of primary node failure, Patroni detects heartbeat loss within 10 seconds, selects the most updated synchronous standby, and promotes it to primary with zero manual intervention.

### 04.2 Patroni Cluster Configuration Specification (`/etc/patroni/namma.yml`)
```yaml
scope: namma-postgres-cluster
namespace: /service/namma-db
name: patroni-node-01
etcd3:
  hosts: ['etcd-az1:2379', 'etcd-az2:2379', 'etcd-az3:2379']
bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    synchronous_mode: true
    synchronous_mode_strict: false
    postgresql:
      use_pg_rewind: true
      use_slots: true
      parameters:
        max_connections: 500
        wal_level: replica
        max_wal_senders: 10
        wal_keep_size: 4096MB
        archive_mode: 'on'
        archive_command: 'pgbackrest --stanza=namma archive-push %p'
```

### 04.3 PgBouncer High-Availability Connection Routing (`/etc/pgbouncer/pgbouncer.ini`)
PgBouncer instances run as sidecars or local DaemonSets with active health checking against Patroni REST APIs:
```ini
[databases]
namma_master = host=patroni-primary.db.internal port=5432 dbname=namma_master pool_size=50
namma_replicas = host=patroni-standby.db.internal port=5432 dbname=namma_master pool_size=100

[pgbouncer]
listen_port = 6432
listen_addr = 0.0.0.0
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 5000
default_pool_size = 25
reserve_pool_size = 5
reserve_pool_timeout = 5.0
server_round_robin = 1
```

## 05. Edge Clinic Disaster Recovery & Hardware Hot-Swap Architecture
Hardware specification and operational failover procedures for the 183 physical clinic installations:

### 05.1 Edge Hardware Bill of Materials & Physical Protection
- **Appliance Hardware:** Intel N100 Processor (4 cores, 3.4GHz), 16GB DDR5 ECC RAM, Dual 512GB NVMe PCIe 4.0 SSDs configured in hardware RAID 1 (mdadm mirror).
- **Network Interfaces:** Dual Gigabit Ethernet ports (Primary LAN to clinic switch, Secondary WAN to BSNL/Jio fiber router) plus embedded 4G/5G LTE eSIM modem with automatic cellular failover.
- **Power Protection:** APC Smart-UPS 1200VA Line-Interactive UPS with USB signaling connection. Provides up to 120 minutes of runtime during municipal power brownouts.
- **Physical Enclosure:** Wall-mounted, locked 6U tamper-resistant steel server enclosure with dual temperature-controlled exhaust fans.

### 05.2 RAID 1 NVMe Mirroring & SSD Failure Recovery
The dual NVMe drives operate in RAID 1 via Linux `mdadm`. If one drive fails, system boots degraded without downtime:
```bash
# Check RAID array status
cat /proc/mdstat
# Output: md0 : active raid1 nvme0n1p2[0] nvme1n1p2[1]

# Replacing failed drive nvme1n1
mdadm --manage /dev/md0 --fail /dev/nvme1n1p2
mdadm --manage /dev/md0 --remove /dev/nvme1n1p2
# Swap physical drive in powered appliance (hot-swap bay)
sfdisk -d /dev/nvme0n1 | sfdisk /dev/nvme1n1
mdadm --manage /dev/md0 --add /dev/nvme1n1p2
# Monitor resynchronization
watch -n 1 cat /proc/mdstat
```

### 05.3 Network UPS Tools (NUT) Graceful Shutdown Protocol
To prevent SQLite database corruption during extended grid power outages exceeding UPS battery reserves, the edge appliance executes the `upsmon` daemon:
```bash
# /etc/nut/upsmon.conf configuration snippet
MONITOR apc1200@localhost 1 upsmon-user SecretPassword! master
MINSUPPLIES 1
SHUTDOWNCMD '/usr/local/bin/namma-graceful-poweroff.sh'
NOTIFYCMD /usr/local/bin/namma-ups-notify.sh
POLLFREQ 5
POLLFREQALERT 2
HOSTSYNC 15
DEADTIME 15
POWERDOWNFLAG /etc/killpower
```

## 06. 15 Canonical Disaster Recovery Runbooks (ARCH-DR-001 to ARCH-DR-015)
Exhaustive, step-by-step operational runbooks for emergency mitigation, failover execution, and post-incident verification:

### 06.01 Runbook `ARCH-DR-001`: Cloud Primary PostgreSQL Database Failover via Patroni
- **Runbook Identifier:** `ARCH-DR-001`
- **Severity Classification:** **SEV-1 (Critical)**
- **Activation Trigger / Precondition:** Patroni Primary node unresponsiveness, hardware host crash, or network partition in AZ-1.
- **Responsible Roles & Authority:** DBA On-Call, Cloud SRE Lead
- **Target Runbook RTO:** < 5 Minutes
- **Target Runbook RPO:** < 30 Seconds
- **Operational Context:** PostgreSQL primary unresponsiveness causes global API errors across all 183 clinics. Requires rapid failover to synchronous standby in AZ-2.
- **Operational RACI Matrix:** RACI: SRE On-Call (R), Principal DBA (A), Cloud Architect (C), Incident Commander (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. Connect to emergency bastion host via secure jumpbox: `ssh -i ~/.ssh/namma-sre-key sre-admin@bastion.ops.nammahealth.bbmp.gov.in`.
2. Inspect current Patroni cluster topology: `patronictl -c /etc/patroni/namma.yml list`.
3. Identify synchronous standby node in AZ-2 (`patroni-az2-db-01`) and verify WAL replication lag is zero.
4. If automated leader election is delayed, initiate manual failover: `patronictl -c /etc/patroni/namma.yml failover --candidate patroni-az2-db-01 --force`.
5. Confirm promotion in logs: `journalctl -u patroni -n 50 --no-pager | grep -i 'promoted'`.
6. Verify virtual IP (VIP) switchover via keepalived / Envoy endpoint: `ip addr show dev eth0 | grep '10.240.10.100'`.
7. Execute read-write smoke test: `psql -h 10.240.10.100 -U namma_dba -d namma_master -c 'SELECT pg_is_in_recovery(), current_timestamp;'` (must return `false`).
8. Inspect PgBouncer connection pool metrics: `psql -h 10.240.10.100 -p 6432 -U pgbouncer pgbouncer -c 'SHOW POOLS;'`.
9. Verify microservice HTTP response codes across API gateway: `curl -I https://api.nammahealth.bbmp.gov.in/health/database` (must return HTTP 200).
10. Re-provision failed AZ-1 host as cascading standby: `patronictl -c /etc/patroni/namma.yml reinit namma-postgres-cluster patroni-az1-db-01`.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Verify zero rejected transactions in backend logs; assert HTTP 200 responses on `/api/v1/health/database` across all Kubernetes pods.
- **Fail-Safe Abort / Rollback Directive:** Abort manual failover if replication lag > 10MB; escalate to Cold Backup Point-in-Time Recovery.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-001` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.02 Runbook `ARCH-DR-002`: Edge Mini-Server Complete Hardware Failure Hot-Swap
- **Runbook Identifier:** `ARCH-DR-002`
- **Severity Classification:** **SEV-2 (Major)**
- **Activation Trigger / Precondition:** Intel N100 appliance power supply failure, motherboard short, or physical hardware destruction at clinic site.
- **Responsible Roles & Authority:** Zonal IT Support Technician, Primary Clinic Pharmacist
- **Target Runbook RTO:** < 60 Minutes
- **Target Runbook RPO:** < 15 Minutes
- **Operational Context:** Catastrophic local server failure leaves clinic without local database or PWA host. Zonal field team swaps box with pre-staged depot spare.
- **Operational RACI Matrix:** RACI: Zonal Field Technician (R), Zonal IT Lead (A), Clinic Duty Doctor (C), BBMP Helpdesk (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. Clinic staff logs emergency hardware ticket with BBMP IT Helpdesk (`TICKET-HW-URGENT`).
2. Zonal field technician retrieves pre-configured Intel N100 spare unit from zonal depot vault.
3. Technician travels to clinic site with replacement unit and antistatic toolkit.
4. Turn off APC Smart-UPS unit; disconnect power cable, dual Gigabit Ethernet cables, and USB peripherals.
5. Unlock 6U server rack enclosure; unmount failed appliance chassis.
6. Mount replacement appliance; reconnect Ethernet Port 1 (LAN Switch), Port 2 (WAN Fiber), UPS USB signaling cable, and thermal printer USB.
7. Power on UPS and boot replacement unit; verify BIOS auto-power-on engages cleanly.
8. Connect maintenance laptop to front Service Port (192.168.100.1:8443) and execute provisioning CLI: `sudo /opt/namma/bin/namma-commission.sh --clinic-id BBMP-CLN-042 --zone SOUTH`.
9. Script establishes mTLS handshake with cloud control plane; downloads encrypted SQLite tenant slice and active formulary.
10. Verify workstation tablets connect to local PWA URL: `https://clinic.local:8443`; conduct test queue token print on thermal slip printer.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Execute synthetic intake and test prescription on workstation PWA; confirm local SQLite commit succeeds and sync daemon pushes test record to cloud.
- **Fail-Safe Abort / Rollback Directive:** If replacement unit fails to boot, switch clinic to paper backup records and retrieve secondary spare from Central Health Office.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-002` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.03 Runbook `ARCH-DR-003`: Municipal WAN / Fiber Severance - Seamless Offline Operation
- **Runbook Identifier:** `ARCH-DR-003`
- **Severity Classification:** **SEV-2 (Major)**
- **Activation Trigger / Precondition:** Civil construction roadwork cuts municipal fiber backhaul and primary ISP link to clinic.
- **Responsible Roles & Authority:** Clinic Staff (Autonomous), Network Operations Center (NOC)
- **Target Runbook RTO:** < 1 Minute (Autonomous)
- **Target Runbook RPO:** 0 Minutes (Zero Loss)
- **Operational Context:** Municipal road excavation severs primary fiber link. Edge appliance autonomously engages cellular failover and local SQLite operation.
- **Operational RACI Matrix:** RACI: Edge Daemon Daemon (R), Zonal NOC Engineer (A), Clinic Staff (C), Municipal ISP NOC (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. Edge health monitor daemon detects 3 consecutive packet losses to cloud API gateway (`ping -c 3 10.240.0.1`).
2. Appliance network interface switcher automatically activates secondary LTE eSIM modem (`wwan0`).
3. If cellular connection is unavailable or signal jammed, appliance enters FULLY AUTONOMOUS OFFLINE MODE.
4. Workstation PWA displays prominent amber alert banner: 'OFFLINE MODE ACTIVE - Local Edge Server Operating. Zero Disruption.'
5. All clinic workflows (registration, triage, MEWS scoring, doctor consultation, e-Rx, pharmacy dispensing) execute against local SQLite database.
6. Every transaction appends an entry to the `offline_mutation_journal` table with an incremented sequence number and local HMAC signature.
7. Local thermal slip printer prints offline verification QR codes for patient prescriptions.
8. NOC monitors fiber outage status via BBMP GIS backhaul dashboard; dispatches municipal fiber repair crew.
9. Upon fiber repair, edge daemon detects stable connectivity (60 seconds continuous ping to cloud).
10. Edge daemon initiates batched Zstandard-compressed replay of queued mutations: `curl -X POST https://sync.nammahealth.bbmp.gov.in/v1/replay -d @mutation_batch.zst`.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Confirm `offline_mutation_journal` pending count drops to zero; verify all offline encounter IDs exist in central PostgreSQL database.
- **Fail-Safe Abort / Rollback Directive:** If offline operation exceeds 72 hours, technician manually extracts encrypted SQLite database snapshot to secure USB drive for cloud ingest.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-003` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.04 Runbook `ARCH-DR-004`: Regional Cloud Datacenter Total Loss (Cross-Region DR Activation)
- **Runbook Identifier:** `ARCH-DR-004`
- **Severity Classification:** **SEV-1 (Critical)**
- **Activation Trigger / Precondition:** Catastrophic power grid failure, flood, or fiber disconnection wiping out primary Bengaluru cloud datacenter.
- **Responsible Roles & Authority:** Incident Commander, Principal Architect, Cloud SRE Team
- **Target Runbook RTO:** < 30 Minutes
- **Target Runbook RPO:** < 15 Minutes
- **Operational Context:** Total failure of Bengaluru cloud datacenter. SRE team activates warm standby disaster recovery region in Hyderabad.
- **Operational RACI Matrix:** RACI: SRE Incident Commander (R), Principal Cloud Architect (A), BBMP Health Commissioner (C), Executive Secretariat (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. SRE Incident Commander declares SEV-1 Disaster after confirming total unreachability of Bengaluru AZ-1 and AZ-2 for > 10 minutes.
2. Convene emergency virtual War Room bridge with core SRE, DBA, and Network engineering leads.
3. Update Route53 / Cloudflare DNS traffic policy: shift `*.nammahealth.bbmp.gov.in` to Hyderabad Secondary NLB IP: `203.0.113.50`.
4. Connect to Hyderabad Patroni cluster; promote read replica standby to read-write master: `patronictl -c /etc/patroni/namma-hyd.yml promote`.
5. Assert Hyderabad database write capability: `psql -h hyd-db-vip -U namma_dba -d namma_master -c 'SELECT pg_is_in_recovery();'` (must be `false`).
6. Scale Kubernetes microservice deployments in Hyderabad cluster from warm capacity (2 pods) to production scale (8 pods each): `kubectl scale deployment --all --replicas=8 -n namma-prod`.
7. Verify Redis Sentinel cluster promotion in Hyderabad region: `redis-cli -h hyd-redis info replication`.
8. Broadcast cloud DNS update push to all 183 clinic edge appliances via SMS gateway telemetry ping.
9. Verify edge appliances re-establish mTLS connections to Hyderabad sync endpoint (`sync-hyd.nammahealth.bbmp.gov.in`).
10. Monitor real-time transaction ingestion and verify ClickHouse CDC streams reconnect cleanly.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Execute automated synthetic clinical journey test against Hyderabad ingress; assert end-to-end latency < 300ms and zero error responses.
- **Fail-Safe Abort / Rollback Directive:** Do not activate cross-region DR if primary datacenter outage is estimated at < 15 minutes to avoid unneeded split-brain risk.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-004` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.05 Runbook `ARCH-DR-005`: Ransomware / Cryptographic Vault Intrusion Isolation & Key Revocation
- **Runbook Identifier:** `ARCH-DR-005`
- **Severity Classification:** **SEV-1 (Critical)**
- **Activation Trigger / Precondition:** Compromise of HashiCorp Vault root credentials, suspected key exfiltration, or ransomware signature detected.
- **Responsible Roles & Authority:** Chief Information Security Officer (CISO), SecOps Lead, Cloud SRE
- **Target Runbook RTO:** < 15 Minutes
- **Target Runbook RPO:** 0 Minutes (Zero Loss)
- **Operational Context:** Suspected cryptographic credential leak or unauthorized administrative access. SecOps initiates immediate lockdown and key revocation.
- **Operational RACI Matrix:** RACI: CISO / SecOps Lead (R), Principal Architect (A), BBMP Health Commissioner (C), CERT-In / Police Cyber Division (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. SecOps team executes emergency Vault cluster seal: `vault operator seal` across all active HashiCorp Vault instances.
2. Isolate compromised Kubernetes pods via Calico NetworkPolicy: apply immediate egress deny-all rule to affected namespace.
3. Revoke all active JSON Web Tokens (JWT) by incrementing the global key version counter in Redis and issuing emergency token blacklist.
4. Invalidate all existing database connection passwords and service credentials in PostgreSQL primary.
5. Terminate all active staff sessions across all 183 clinics; force complete re-authentication.
6. Verify database file immutability against AWS S3 WORM snapshots taken prior to the intrusion timestamp.
7. Initialize emergency air-gapped root HSM; generate fresh master RSA/ECDSA signing keys and database master passwords.
8. Unseal Vault using air-gapped Shamir secret key shares held by 3 designated BBMP trustees.
9. Roll out new TLS certificates, service secrets, and API tokens via automated Ansible playbook.
10. Gradually restore application ingress; monitor honeypot alerts and security telemetry for repeat unauthorized attempts.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Verify zero unauthorized API calls; confirm all staff re-authenticate with MFA; verify WORM audit ledger integrity matches pre-incident Merkle root.
- **Fail-Safe Abort / Rollback Directive:** If ransomware encryption has touched active storage, immediately fail over to read-only cold WORM snapshot from secondary region.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-005` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.06 Runbook `ARCH-DR-006`: Corrupted Edge SQLite Database Restoration from Cloud Mirror
- **Runbook Identifier:** `ARCH-DR-006`
- **Severity Classification:** **SEV-2 (Major)**
- **Activation Trigger / Precondition:** Abrupt power cut during unbuffered write causes SQLite disk image malformed error (`SQLITE_CORRUPT`).
- **Responsible Roles & Authority:** Zonal IT Technician, Remote SRE Operations
- **Target Runbook RTO:** < 20 Minutes
- **Target Runbook RPO:** < 5 Minutes
- **Operational Context:** Local SQLite database file corruption halts clinic operations. Edge daemon initiates automatic self-repair or requests cloud hydration.
- **Operational RACI Matrix:** RACI: Edge Daemon Auto-Recovery (R), Zonal IT Lead (A), Clinic Pharmacist (C), Cloud Database Lead (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. Edge daemon encounters `SQLITE_CORRUPT` error during query execution; immediately flags local database as damaged.
2. Daemon moves damaged database file to quarantine directory: `mv /opt/namma/data/clinic.db /opt/namma/data/corrupt_$(date +%s).db`.
3. Daemon attempts local repair using SQLite recovery engine: `sqlite3 corrupt.db ".recover" | sqlite3 /opt/namma/data/clinic.db`.
4. If local repair fails, daemon initiates emergency cloud hydration over mTLS connection: `curl -s https://sync.nammahealth.bbmp.gov.in/v1/hydrate/BBMP-CLN-042 -o /tmp/snapshot.zst`.
5. Cloud sync service generates clinic-specific snapshot containing patient demographics, active appointments, and 7-day medication records.
6. Edge daemon decompresses snapshot using Zstandard and installs to `/opt/namma/data/clinic.db`.
7. Verifies database schema integrity: `sqlite3 /opt/namma/data/clinic.db "PRAGMA integrity_check;"` (must return `ok`).
8. Restarts local edge web server and queue manager services: `systemctl restart namma-edge-daemon`.
9. Re-attaches connected workstation browsers and verifies active clinic queue restores cleanly.
10. Replays any un-synced transactions salvaged from the quarantined damaged database file.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Assert `PRAGMA integrity_check;` returns `ok`; confirm staff can query existing patient records without error.
- **Fail-Safe Abort / Rollback Directive:** If cloud hydration fails due to network outage, restore from nightly local backup snapshot `/opt/namma/backup/clinic_nightly.db`.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-006` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.07 Runbook `ARCH-DR-007`: Kafka Cluster Broker Loss & Topic Partition Rebalancing
- **Runbook Identifier:** `ARCH-DR-007`
- **Severity Classification:** **SEV-2 (Major)**
- **Activation Trigger / Precondition:** Unrecoverable hardware failure of 2 out of 5 Apache Kafka brokers in production cloud cluster.
- **Responsible Roles & Authority:** Cloud Platform Engineer, SRE On-Call
- **Target Runbook RTO:** < 15 Minutes
- **Target Runbook RPO:** 0 Minutes (Zero Loss)
- **Operational Context:** Hardware host crash drops 2 Kafka brokers, creating under-replicated partitions on clinical CDC topics.
- **Operational RACI Matrix:** RACI: SRE On-Call (R), Platform Lead (A), Analytics Lead (C), Support Desk (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. AlertManager fires `KafkaUnderReplicatedPartitions` critical alert.
2. Platform engineer connects to Kafka monitoring pod: `kubectl exec -it kafka-tool-pod -n monitoring -- bash`.
3. Inspect broker cluster status: `kafka-topics --bootstrap-server kafka:9092 --describe --under-replicated-partitions`.
4. Kubernetes StatefulSet automatically schedules replacement broker pods with persistent NVMe storage.
5. Generate partition reassignment configuration for under-replicated topics: `kafka-reassign-partitions --bootstrap-server kafka:9092 --generate --topics-to-move-json-file topics.json --broker-list '1,2,3,4,5'`.
6. Execute partition reassignment plan: `kafka-reassign-partitions --bootstrap-server kafka:9092 --reassignment-json-file reassign.json --execute`.
7. Track reassignment progress until complete: `kafka-reassign-partitions --bootstrap-server kafka:9092 --reassignment-json-file reassign.json --verify`.
8. Verify all topics satisfy minimum in-sync replica threshold: `min.insync.replicas = 2`.
9. Inspect consumer group lag for Debezium CDC and notification pipelines: `kafka-consumer-groups --bootstrap-server kafka:9092 --describe --group namma-cdc-group`.
10. Verify ClickHouse CDC ingestion resumes and lag drops below 1,000 records.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Verify zero lost CDC events; assert all producer microservices report zero failed publish exceptions in OTel spans.
- **Fail-Safe Abort / Rollback Directive:** If Kafka rebalance causes excessive disk I/O, throttle reassignment bandwidth to 50MB/s using `--throttle 52428800`.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-007` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.08 Runbook `ARCH-DR-008`: Line-Interactive UPS Low-Battery Graceful Edge Appliance Shutdown
- **Runbook Identifier:** `ARCH-DR-008`
- **Severity Classification:** **SEV-3 (Moderate)**
- **Activation Trigger / Precondition:** Grid power failure at clinic site exceeds 90 minutes; UPS battery level drops below 15% reserve.
- **Responsible Roles & Authority:** Edge Appliance Daemon (Autonomous), Clinic Security Guard
- **Target Runbook RTO:** < 5 Minutes (Autonomous)
- **Target Runbook RPO:** 0 Minutes (Zero Loss)
- **Operational Context:** Prolonged power outage exhausts UPS battery. Automated daemon initiates orderly shutdown to prevent file corruption.
- **Operational RACI Matrix:** RACI: NUT `upsmon` Daemon (R), Zonal IT Lead (A), Clinic Duty Nurse (C), BBMP Facilities (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. APC Smart-UPS battery charge drops below 15% during prolonged municipal power outage.
2. Network UPS Tools (`upsmon`) daemon intercepts `LOWBATT` signal over USB interface.
3. Daemon executes emergency broadcast to all workstation PWA screens: 'POWER SHUTDOWN IMMINENT: Saving clinical records...'
4. Edge daemon instructs SQLite database to flush all unwritten pages and truncate WAL: `PRAGMA wal_checkpoint(TRUNCATE);`.
5. Daemon safely closes all active database connections and stops local web server service.
6. Flushes operating system filesystem write caches: `sync`.
7. Issues delayed hardware sleep command to UPS micro-controller: `upscmd -u upsmon-user -p SecretPass! apc1200 load.off.delay 30`.
8. Executes orderly Linux system shutdown: `systemctl poweroff`.
9. Upon municipal power restoration, UPS automatically re-energizes load outlets.
10. Edge appliance BIOS ('AC Power Recovery: Power On') automatically boots appliance, verifies filesystem, and restarts clinic services.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Inspect systemd journal upon restart; verify clean unmount timestamp and zero SQLite recovery errors on initial boot.
- **Fail-Safe Abort / Rollback Directive:** If UPS fails to shutdown appliance before power cuts, run full filesystem check `fsck -y /dev/md0` on next boot.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-008` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.09 Runbook `ARCH-DR-009`: Central Ingress API Gateway DDoS / Volumetric Flood Mitigation
- **Runbook Identifier:** `ARCH-DR-009`
- **Severity Classification:** **SEV-1 (Critical)**
- **Activation Trigger / Precondition:** Volumetric HTTP/TCP SYN flood (> 100 Gbps) targeting municipal public health API gateway.
- **Responsible Roles & Authority:** SecOps On-Call, Cloud Platform Lead, Cloudflare / Akamai SOC
- **Target Runbook RTO:** < 10 Minutes
- **Target Runbook RPO:** 0 Minutes (Zero Loss)
- **Operational Context:** Massive distributed denial of service attack saturates cloud ingress bandwidth, blocking citizen access and clinic sync.
- **Operational RACI Matrix:** RACI: Cloudflare SOC / SecOps Lead (R), Cloud Platform Lead (A), BBMP Commissioner (C), Cyber Crime Cell (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. Ingress network monitoring detects sudden 25x bandwidth surge (> 100 Gbps) hitting `/api/v1/*` endpoints.
2. SRE on-call activates Cloudflare / Edge CDN 'Under Attack' mode with managed JS challenge rules.
3. Gateway token bucket rate limiters automatically engage: restrict unauthenticated public traffic to 20 req/sec per IP subnet.
4. Enable strict mutual TLS (mTLS) enforcement on `/api/v1/sync/*`: drop all non-mTLS packets at edge boundary.
5. Verify clinic edge-to-cloud synchronization traffic bypasses public challenge via dedicated mTLS IP whitelist.
6. Apply geographic firewall filtering: block all ingress traffic originating outside Republic of India IP ranges.
7. Inspect ingress access logs in OpenSearch; identify attack signatures and deploy targeted WAF custom blocking rules.
8. Scale Kong / Envoy API Gateway pods horizontally from 6 to 24 replicas: `kubectl scale deployment api-gateway --replicas=24 -n namma-prod`.
9. Monitor gateway CPU utilization and P95 latency returning to normal operational thresholds (< 150ms).
10. Compile attack forensic report for submission to Indian Computer Emergency Response Team (CERT-In).

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Confirm edge synchronization latency returns to < 1,000ms; verify zero legitimate clinic staff requests blocked by rate limiter.
- **Fail-Safe Abort / Rollback Directive:** Never apply global rate limits to `/api/v1/sync/*` endpoint to ensure clinic edge sync operations remain unimpeded.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-009` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.10 Runbook `ARCH-DR-010`: National ABDM Gateway Extended Outage Queuing & Bulk Replay
- **Runbook Identifier:** `ARCH-DR-010`
- **Severity Classification:** **SEV-2 (Major)**
- **Activation Trigger / Precondition:** National Health Authority (NHA) ABDM central gateway unreachable for > 6 hours.
- **Responsible Roles & Authority:** Interoperability Lead, Integration SRE
- **Target Runbook RTO:** < 15 Minutes
- **Target Runbook RPO:** 0 Minutes (Zero Loss)
- **Operational Context:** National health portal maintenance or outage prevents real-time publishing of FHIR care bundles.
- **Operational RACI Matrix:** RACI: Integration Engineer (R), Interoperability Lead (A), Chief Medical Officer (C), NHA Helpdesk (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. ABDM bridge service detects consecutive HTTP 503 / 504 gateway timeouts from NHA central servers.
2. Circuit breaker automatically trips from CLOSED to OPEN state, halting direct API calls to NHA.
3. Platform UI displays subtle notification: 'National ABDM Sync Queued (National Gateway Under Maintenance)'.
4. Outbound FHIR R4 Bundles (Encounter, Prescription, Diagnostic Report) are enqueued into durable Kafka topic `namma.abdm.publish.queue`.
5. Clinic doctors and nurses continue patient consultations and care workflows with zero UI latency or blocking.
6. Integration bridge background health probe queries NHA health endpoint `/v0.5/heartbeat` every 60 seconds with exponential backoff.
7. Upon NHA gateway recovery (10 consecutive successful probes), circuit breaker transitions to HALF-OPEN.
8. Throttled consumer begins draining backlog queue at controlled rate (50 bundles/second) to prevent gateway rate-limit trips.
9. Verify care context registration acknowledgments received from NHA and update local transaction status.
10. Once backlog queue reaches zero, circuit breaker resets to CLOSED state; notify municipal digital health lead.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Verify Kafka backlog consumer lag drops to zero; assert all queued encounters show `abdm_synced = true`.
- **Fail-Safe Abort / Rollback Directive:** If NHA rejects bundles due to schema changes, redirect failed bundles to Dead Letter Queue (DLQ) for schema patching.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-010` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.11 Runbook `ARCH-DR-011`: Corrupted Patient Master Index Split-Brain Disentanglement
- **Runbook Identifier:** `ARCH-DR-011`
- **Severity Classification:** **SEV-2 (Major)**
- **Activation Trigger / Precondition:** Network partition causes two different clinics to register conflicting master records for the same citizen.
- **Responsible Roles & Authority:** Lead Medical Registrar, Database Administrator
- **Target Runbook RTO:** < 4 Hours
- **Target Runbook RPO:** < 15 Minutes
- **Operational Context:** Offline operations in different clinics lead to duplicate patient records for the same citizen. Requires deterministic reconciliation.
- **Operational RACI Matrix:** RACI: Zonal Medical Officer (R), Lead Registrar (A), Clinical Data Lead (C), Affected Citizen (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. Master Patient Index (MPI) cloud deduplication engine flags high-confidence phonetic Soundex match during cross-clinic sync.
2. Both conflicting patient records (`PAT-001` and `PAT-002`) are tagged with status `RECONCILIATION_REQUIRED`.
3. Automatic consolidation is paused to prevent erroneous merging of clinical histories.
4. Zonal Medical Officer opens Clinical Identity Disentanglement Console.
5. Officer inspects demographic fields: Aadhaar last 4 digits, phone number, date of birth, photo portrait, and address.
6. If confirmed as distinct individuals with coincidentally identical names: officer marks records as `DISTINCT_VERIFIED`.
7. If confirmed as identical citizen: officer selects primary surviving ID (`PAT-001`) and triggers Master Merge Tool.
8. Tool remaps all historical encounters, lab reports, and prescriptions from `PAT-002` to `PAT-001` in an atomic database transaction.
9. Deprecated ID `PAT-002` is marked as `MERGED_TOMBSTONE` with permanent redirect pointer to `PAT-001`.
10. Append cryptographic audit event to WORM ledger documenting merge rationale, approving officer credentials, and timestamp.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Assert queries for both old and new patient IDs resolve transparently to consolidated survivor record; zero orphan encounters.
- **Fail-Safe Abort / Rollback Directive:** Never delete deprecated patient ID from database; maintain permanent tombstone for historical audit trail.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-011` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.12 Runbook `ARCH-DR-012`: Redis Cluster Memory Exhaustion & Cache Rebuilding
- **Runbook Identifier:** `ARCH-DR-012`
- **Severity Classification:** **SEV-2 (Major)**
- **Activation Trigger / Precondition:** Redis cluster memory utilization reaches 95% due to session key TTL leaks; evictions impacting performance.
- **Responsible Roles & Authority:** Backend Lead, SRE On-Call
- **Target Runbook RTO:** < 15 Minutes
- **Target Runbook RPO:** 0 Minutes (Zero Loss)
- **Operational Context:** Unbounded cache growth threatens session store stability. SRE clears stale cache keys and pre-heats essential formularies.
- **Operational RACI Matrix:** RACI: SRE On-Call (R), Backend Lead (A), DevOps Lead (C), Clinic Staff (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. AlertManager triggers `RedisMemoryHigh` alert (> 90% allocated RAM).
2. SRE connects to Redis master node: `redis-cli -h redis-cluster.internal -p 6379 info memory`.
3. Run key space analysis to identify leaking key patterns: `redis-cli --bigkeys`.
4. Identify leaking temporary keys missing TTL (e.g., untracked search autocomplete buffers).
5. Set temporary eviction policy to protect active user sessions: `CONFIG SET maxmemory-policy volatile-lru`.
6. Safely scan and delete offending stale cache keys in batches: `redis-cli --scan --pattern 'temp:search:*' | xargs -L 500 redis-cli del`.
7. Verify memory utilization drops below 65% of cluster capacity.
8. Execute cache warm-up script to repopulate essential static catalogs (Formulary, ICD-10, Clinic Master): `python /opt/namma/scripts/warm_cache.py`.
9. Verify cache hit ratio recovers to > 90% within 10 minutes.
10. File bug ticket with backend engineering to enforce mandatory TTL on all new cache keys.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Confirm Redis memory drops below 60%; assert drug formulary lookup latency returns to < 5ms.
- **Fail-Safe Abort / Rollback Directive:** Never run `FLUSHALL` on production Redis cluster as this invalidates active staff sessions and forces clinic re-logins.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-012` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.13 Runbook `ARCH-DR-013`: ClickHouse Columnar Analytics Disk Space Exhaustion Emergency Truncate/Tier
- **Runbook Identifier:** `ARCH-DR-013`
- **Severity Classification:** **SEV-2 (Major)**
- **Activation Trigger / Precondition:** Columnar data disk on ClickHouse analytics server exceeds 92% capacity due to uncompressed CDC logs.
- **Responsible Roles & Authority:** Data Platform Engineer, Analytics SRE
- **Target Runbook RTO:** < 30 Minutes
- **Target Runbook RPO:** 0 Minutes (Zero Loss)
- **Operational Context:** Rapid growth of analytics event tables threatens data warehouse availability. SRE triggers emergency partition tiering to S3.
- **Operational RACI Matrix:** RACI: Analytics SRE (R), Data Platform Lead (A), Municipal Epidemiologist (C), Support Team (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. AlertManager fires `ClickHouseDiskSpaceCritical` (> 90% disk utilization).
2. Connect to ClickHouse client: `clickhouse-client --host localhost --port 9000`.
3. Inspect table disk consumption: `SELECT table, formatReadableSize(sum(bytes_on_disk)) FROM system.parts WHERE active GROUP BY table ORDER BY sum(bytes_on_disk) DESC LIMIT 5;`.
4. Identify oldest monthly partitions in high-volume tables (`telemetry_spans`, `audit_events_cdc`).
5. Execute partition tiering command to move partitions older than 90 days from NVMe SSD to S3 object storage tier: `ALTER TABLE telemetry_spans MOVE PARTITION '2026-05' TO VOLUME 's3_cold';`.
6. Trigger background part compaction to reclaim storage immediately: `OPTIMIZE TABLE telemetry_spans FINAL;`.
7. Verify physical disk utilization drops below 65% on local NVMe storage.
8. Review automated ClickHouse retention TTL policy: ensure `TTL event_date + INTERVAL 90 DAY TO VOLUME 's3_cold'` is active.
9. Verify municipal epidemiological queries continue to execute seamlessly across tiered partitions.
10. Check that Debezium CDC consumer lag recovers to baseline.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Confirm ClickHouse disk space utilization < 70%; verify analytical queries for municipal epidemiological dashboard succeed in < 1,500ms.
- **Fail-Safe Abort / Rollback Directive:** Never drop or delete clinical encounter partitions; move to cold object storage instead.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-013` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.14 Runbook `ARCH-DR-014`: 108 Emergency CAD Integration Breakdown Voice Fallback
- **Runbook Identifier:** `ARCH-DR-014`
- **Severity Classification:** **SEV-1 (Critical)**
- **Activation Trigger / Precondition:** GVK-EMRI 108 ambulance dispatch REST API server returns persistent HTTP 500 errors during emergency triage.
- **Responsible Roles & Authority:** Triage Nurse, Clinic Duty Doctor, Emergency Dispatch Coordinator
- **Target Runbook RTO:** < 2 Minutes
- **Target Runbook RPO:** 0 Minutes (Zero Loss)
- **Operational Context:** API failure during critical emergency referral. System initiates instant automated voice dispatch protocol to prevent transfer delays.
- **Operational RACI Matrix:** RACI: Clinic Duty Doctor (R), Triage Nurse (A), 108 CAD Operator (C), Medical Superintendent (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. Triage nurse or doctor clicks 'Dispatch 108 Ambulance' for critical patient with MEWS >= 5.
2. Platform CAD integration bridge detects repeated HTTP 500 / timeout errors from GVK-EMRI central dispatch API.
3. Workstation UI instantly presents emergency red banner: '108 API DOWN - Priority Voice Dispatch Active'.
4. System automatically generates a 4-digit Priority Dispatch Passcode (e.g., `CAD-8821`).
5. System renders pre-formatted Emergency Transfer Summary on screen: Patient Name, Age, Vital Signs, Suspected Diagnosis, Clinic GPS Coordinates.
6. Duty doctor taps 'Call 108 Hotline' on clinic VoIP terminal or dials `080-2266-0108` on clinic landline.
7. Doctor provides priority passcode `CAD-8821` to 108 dispatcher; dispatcher enters code into GVK-EMRI terminal to pull pre-filled patient transfer profile.
8. Dispatcher confirms ambulance unit allocation, vehicle registration number, and estimated time of arrival (ETA).
9. Doctor inputs vehicle registration number and ETA into workstation PWA to seal emergency referral dossier.
10. System prints emergency referral summary with barcode for physical handover to ambulance paramedic crew.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Confirm emergency referral status marked as `DISPATCHED_VOICE`; assert ambulance ETA timestamp successfully recorded.
- **Fail-Safe Abort / Rollback Directive:** Never delay physical patient stabilization or resuscitation while attempting electronic referral dispatch.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-014` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

### 06.15 Runbook `ARCH-DR-015`: Clinic Workstation Mass Browser Cache Corruption Reset
- **Runbook Identifier:** `ARCH-DR-015`
- **Severity Classification:** **SEV-3 (Moderate)**
- **Activation Trigger / Precondition:** Bad PWA service worker script caching corrupts local workstation browser state across all clinic PCs.
- **Responsible Roles & Authority:** Zonal IT Technician, Clinic Receptionist
- **Target Runbook RTO:** < 15 Minutes
- **Target Runbook RPO:** 0 Minutes (Zero Loss)
- **Operational Context:** Corrupted browser cache causes white-screen errors on workstation tablets following frontend deployment.
- **Operational RACI Matrix:** RACI: Zonal IT Support (R), Clinic Receptionist (A), Frontend Lead (C), Clinic Staff (I).

#### Diagnostic Decision Matrix & Activation Thresholds:
```
 +-----------------------------+       Metric breaches threshold        +-----------------------------+
 |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |
 +-----------------------------+                                        +-----------------------------+
                |                                                                      |
                | Auto-mitigation fails                                                | Success
                v                                                                      v
 +-----------------------------+                                        +-----------------------------+
 |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |
 +-----------------------------+                                        +-----------------------------+
```

#### Step-by-Step Emergency Mitigation Procedure:
1. Clinic staff report blank screen or JavaScript console exceptions (`ChunkLoadError`) on workstation tablets.
2. Receptionist or staff clicks dedicated desktop shortcut: 'Namma Clinic Emergency Reset'.
3. Shortcut triggers automated PowerShell / Bash cache eviction script in Chromium browser: `google-chrome --clear-token-browsing-data-dir`.
4. Script unregisters active Service Workers, clears IndexedDB caches, and purges localStorage entries.
5. Script restarts Chromium in kiosk mode and navigates to cache-busting entry URL: `https://clinic.local:8443/?app_version=fresh_$(date +%s)`.
6. Browser downloads clean, verified PWA application shell bundle from local edge server.
7. Service worker installs and activates cleanly; establishes WebSocket connection with edge daemon.
8. Receptionist logs in with PIN; verifies patient queue displays and search operates normally.
9. Doctor and pharmacist workstations execute identical reset sequence via desktop shortcut.
10. Confirm all 3 clinic workstations operational and processing patients within 10 minutes.

#### Post-Incident Verification & Quality Gate:
- **Authoritative Verification Criteria:** Assert workstation PWA loads cleanly without JavaScript errors; verify staff can view and edit active consultation drafts.
- **Fail-Safe Abort / Rollback Directive:** Instruct staff never to clear browser cookies during active consultations without first ensuring draft is saved locally.

#### Post-Incident Review (PIR) Reporting Standard:
Within 24 hours of `ARCH-DR-015` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.

---

## 07. Backup, WAL Archiving & Point-in-Time Recovery (PITR) Strategy
Exhaustive backup schedule, retention tiering, cryptographic encryption, and PITR restoration procedures:

### 07.1 Backup Schedule & Multi-Tier Retention Matrix
| Backup Type | Frequency | Snapshot Mechanism | Storage Location | Retention Window | Encryption Standard | WORM Immutability |
| :--- | :---: | :--- | :--- | :---: | :---: | :---: |
| **Full Base Backup** | Weekly (Sunday 01:00 IST) | `pgBackRest` full cluster snapshot | Cloud Object Storage (AZ-1 & AZ-3) | 90 Days | AES-256-GCM | Enabled (90-Day Lock) |
| **Differential Backup** | Daily (Mon-Sat 02:00 IST) | `pgBackRest` differential block scan | Cloud Object Storage (AZ-1 & AZ-3) | 30 Days | AES-256-GCM | Enabled (30-Day Lock) |
| **Continuous WAL Archiving**| Every 60 Seconds / 16MB | `archive_command` streaming WAL push | Cloud Object Storage (Multi-Region) | 30 Days | AES-256-GCM | Enabled (30-Day Lock) |
| **Edge SQLite Snapshot** | Daily (20:30 IST Post-Close) | `VACUUM INTO` encrypted archive | Local NVMe + Cloud Sync Mirror | 14 Days | SQLCipher AES-256 | Local File Lock |
| **Statutory Annual Archival**| Annually (March 31 Close) | Consolidated clinical cold snapshot | AWS S3 Glacier Deep Archive | 10 Years | AES-256-GCM | Strict WORM Compliance |

### 07.2 pgBackRest Production Configuration (`/etc/pgbackrest/pgbackrest.conf`)
```ini
[global]
repo1-type=s3
repo1-s3-endpoint=s3.ap-south-1.amazonaws.com
repo1-s3-bucket=namma-backups-primary
repo1-s3-region=ap-south-1
repo1-s3-key-type=auto
repo1-cipher-type=aes-256-cbc
repo1-cipher-pass=KmsSecuredSecretCipherPassphrase!
repo1-retention-full=12
repo1-retention-diff=30
repo1-bundle=y
process-max=4
log-level-console=info
log-level-file=detail
start-fast=y
compress-type=zst
compress-level=6

[namma]
pg1-path=/var/lib/postgresql/16/main
pg1-user=postgres
pg1-port=5432
```

### 07.3 Point-in-Time Recovery (PITR) Verification Procedure
To restore the PostgreSQL master database to any specific second in time (e.g. immediately prior to an erroneous drop-table migration):
```bash
# 1. Stop Patroni and PostgreSQL on target restoration host
systemctl stop patroni
systemctl stop postgresql

# 2. Clean existing corrupted or damaged data directory
rm -rf /var/lib/postgresql/16/main/*

# 3. Execute pgBackRest point-in-time restoration to specified timestamp
pgbackrest --stanza=namma \
  --type=time \
  --target="2026-09-04 14:22:15+05:30" \
  --target-action=promote \
  restore

# 4. Verify restored cluster permissions
chown -R postgres:postgres /var/lib/postgresql/16/main
chmod 700 /var/lib/postgresql/16/main

# 5. Start PostgreSQL and verify database integrity
systemctl start postgresql
psql -U namma_dba -d namma_master -c 'SELECT now(), max(created_at) FROM clinical_encounters;'
```

## 08. Chaos Engineering, Fault Injection & Quarterly GameDay Drills
Automated resilience testing using Chaos Mesh and scheduled full-scale disaster simulations:

### 08.1 Automated Chaos Injection Test Matrix
| Chaos Experiment Code | Target Component | Injected Failure Mode | Automated Assertion | Frequency |
| :--- | :--- | :--- | :--- | :---: |
| **CHAOS-001** | Patroni PostgreSQL Primary | `kill -9` primary process | Failover to AZ-2 synchronous standby completes in < 30 sec; zero data loss | Weekly |
| **CHAOS-002** | Clinic Edge LAN Interface | Drop 100% packets for 2 hours | PWA operates seamlessly offline; mutations queue in SQLite; zero lost records | Bi-Weekly |
| **CHAOS-003** | Central API Gateway | Inject 500ms network latency | Gateway circuit breaker trips; fallback cache returns valid formulary responses | Weekly |
| **CHAOS-004** | Redis Master Node | Abrupt pod termination | Redis Sentinel promotes replica in < 10 sec; session logins remain valid | Bi-Weekly |
| **CHAOS-005** | Kafka Broker 01 | Unclean disk dismount | Topics rebalance to in-sync replicas; consumer lag recovers in < 3 minutes | Monthly |

### 08.2 Sample Chaos Mesh Experiment Manifests
```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: patroni-primary-kill
  namespace: chaos-testing
spec:
  action: pod-kill
  mode: one
  selector:
    namespaces:
      - namma-prod
    labelSelectors:
      'role': 'master'
      'app.kubernetes.io/name': 'patroni'
  scheduler:
    cron: '@weekly'
---
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: edge-sync-latency-injection
  namespace: chaos-testing
spec:
  action: delay
  mode: all
  selector:
    namespaces:
      - namma-prod
    labelSelectors:
      'app': 'sync-gateway'
  delay:
    latency: '800ms'
    jitter: '100ms'
  duration: '30m'
```

### 08.3 Annual Disaster Recovery & GameDay Simulation Schedule
- **Q1 (March):** Simulated Metropolitan WAN Blackout across 20 sample clinics; assert 100% offline clinical continuity.
- **Q2 (June):** Primary Cloud Region Failure Simulation (AZ-1 + AZ-2 simulated cutoff); full failover to Hyderabad DR region.
- **Q3 (September):** Cryptographic Vault Ransomware GameDay; practice manual Shamir key unsealing and HSM key rotation.
- **Q4 (December):** Hardware Catastrophe Simulation; random unannounced hot-standby appliance swap at 5 active clinics.

## 09. Disaster Recovery Architecture Fitness Tests & Verification Checklist
Automated CI/CD validation gates ensuring zero disaster recovery configuration drift:

### 09.1 Automated Architecture Fitness Tests
1. **Continuous Backup Integrity Gate:** Automated daily pipeline restores latest `pgBackRest` snapshot into an isolated ephemeral test container; executes `pg_dump` and asserts zero corruption.
2. **Edge Hot-Standby Image Parity Test:** Nightly build compares SHA-256 package manifests of zonal spare images with cloud production build; fails if divergence detected.
3. **SQLite WAL Fsync Fitness Test:** Benchmarks NVMe sync speed on edge appliance builds; asserts that `PRAGMA synchronous = NORMAL` commits complete in < 15ms.
4. **Patroni Configuration Schema Linter:** Validates that Patroni DCS TTL and synchronous replication settings match architectural specifications.

### 09.2 Disaster Recovery Audit & Verification Checklist
| Verification Item | Automated Verification Command | Acceptance Threshold | Enforcement Gate |
| :--- | :--- | :---: | :---: |
| Patroni Multi-AZ Replication Sync | `patronictl -c /etc/patroni/namma.yml list` | Lag bytes == 0 on sync standby | Continuous Alerting |
| Cloud Object Storage WORM Lock | `aws s3api get-object-retention --bucket namma-backups` | Lock status == COMPLIANCE | Nightly Audit |
| Edge SQLite Integrity Check | `sqlite3 /opt/namma/data/clinic.db "PRAGMA integrity_check;"` | Output == 'ok' | Daily Edge Task |
| UPS Signaling Daemon Health | `upsc apc1200@localhost ups.status` | Output == 'OL' (Online) | Continuous Telemetry |
| Cross-Region Cascading Lag | `SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) FROM pg_stat_replication;` | Lag < 67MB (< 5 min) | Continuous Alerting |
