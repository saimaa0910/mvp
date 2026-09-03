# 🛠️ Cloud Operations, Disaster Recovery & Incident Runbook
## Namma Clinic Digital Health & Operations Platform
### DevOps Engineering, Site Reliability & 24/7 Production Incident Playbook
### Document Code: TD-OPS-04 | Version: 1.0 | Date: September 2026

---

## 1. System Reliability Objectives & SLAs

* **High Availability Target:** $99.9\%$ uptime during core clinic operating hours (08:00 AM – 06:00 PM IST, Monday through Saturday).
* **Recovery Point Objective (RPO):** $< 15\text{ minutes}$ (Maximum tolerable clinical data loss).
* **Recovery Time Objective (RTO):** $< 60\text{ minutes}$ for complete cluster recovery to hot-standby region.
* **Incident Classification & Response Windows:**
  * **P1 (Critical Outage):** Response $< 15$ mins | Workaround $< 2$ hours | Fix $< 12$ hours.
  * **P2 (Major Module Failure):** Response $< 30$ mins | Workaround $< 4$ hours | Fix $< 24$ hours.
  * **P3 (Moderate Defect):** Response $< 2$ hours | Fix within next sprint release.
  * **P4 (Minor / Cosmetic):** Response $< 1$ business day | Scheduled release.

---

## 2. CI/CD Deployment Standard Operating Procedure (SOP)

```
[Git Push to `main`] ──► [GitHub Actions CI]
                             │
                             ├──► Linting & Static Code Analysis (ESLint, SonarQube)
                             ├──► Automated Unit & Integration Tests (Jest, Supertest)
                             ├──► Container Security Scan (Trivy CVE Audit)
                             │
                             ▼
                 [Build & Push Docker Image] (AWS ECR / Private Registry)
                             │
                             ▼
                 [Zero-Downtime Blue/Green Deployment] (AWS ECS Fargate)
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
      [Canary Check]                    [Full Cutover]
  (Health probes on port 3000)      (ALB switches 100% traffic)
```

### Rollback Procedure
If p99 response times exceed 1,500 ms or error rate exceeds $0.5\%$ within 10 minutes of cutover:
```bash
# Automated or manual instant rollback to preceding stable container task definition
aws ecs update-service \
  --cluster namma-clinic-prod-cluster \
  --service namma-clinic-core-service \
  --task-definition namma-clinic-core-service:PREV_STABLE_VERSION \
  --force-new-deployment
```

---

## 3. Database Backup & Restore Standard Operating Procedure

### 3.1 Automated Snapshot Schedule
1. **Continuous WAL Archival:** PostgreSQL Write-Ahead Logs (WAL) streamed continuously to an encrypted S3 bucket via `pgBackRest`, providing Point-in-Time Recovery (PITR) down to the second.
2. **Automated RDS Daily Snapshots:** Triggered at 01:00 AM IST with 35-day automated retention.
3. **Weekly Logical GPG-Encrypted Dump:** Full logical `pg_dump` exported every Sunday at 02:00 AM IST and copied to cold storage at the Karnataka State Data Centre (KSDC).

### 3.2 Point-In-Time Restoration Procedure (Step-by-Step)
```bash
# 1. Identify recovery target timestamp (e.g., 5 minutes before corrupting transaction)
TARGET_TIME="2026-09-02 14:25:00 UTC"

# 2. Restore RDS instance from point-in-time to temporary validation instance
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier namma-clinic-prod-db \
  --target-db-instance-identifier namma-clinic-restore-test \
  --restore-time "${TARGET_TIME}" \
  --db-instance-class db.t3.medium \
  --no-publicly-accessible

# 3. Verify integrity of patient tables and row counts on restored instance
psql -h namma-clinic-restore-test.internal -U dbadmin -d nammaclinic \
  -c "SELECT count(*) FROM patients; SELECT count(*) FROM visits WHERE visit_date = CURRENT_DATE;"

# 4. Repoint Route53 DNS CNAME database endpoint to the restored instance
aws route53 change-resource-record-sets --hosted-zone-id Z12345 --change-batch file://repoint-db.json
```

---

## 4. Monitoring, Health Checks & Telemetry

### 4.1 Monitoring Stack
* **Metrics:** Prometheus server scraping Node.js `/metrics` and PostgreSQL exporter.
* **Dashboards:** Dedicated Grafana instance displaying:
  * Active clinic concurrent users & websocket sessions.
  * p50, p95, p99 API latency across key endpoints (`/visits`, `/prescriptions`).
  * Database connection pool saturation (Max 150 connections).
  * Disk utilization (Alert threshold: $\ge 80\%$).
* **Real-time Error Tracking:** Sentry.io capturing unhandled frontend and API runtime exceptions.

### 4.2 Automated Health Check Endpoints
* **Liveness Probe (`GET /healthz/live`):** Returns `HTTP 200 OK` if the Node.js event loop is responsive.
* **Readiness Probe (`GET /healthz/ready`):** Returns `HTTP 200 OK` only if:
  1. PostgreSQL connection query (`SELECT 1;`) returns $< 50\text{ ms}$.
  2. Redis cache heartbeat (`PING -> PONG`) succeeds.
  3. S3 bucket connection is reachable.

---

## 5. Incident Response Playbooks

### Playbook 1: Total Platform Outage (P1 Severity)
1. **Detection:** PagerDuty alert fires to on-call DevOps Lead & Project Director (Synthetic probe failed 3 consecutive times).
2. **First 15 Minutes:**
   - Verify cloud provider status (AWS ap-south-1 Mumbai health status).
   - Check ALB access logs: Are requests reaching the gateway?
   - If ECS tasks crashed, review CloudWatch container exit logs (`OutOfMemoryError` or unhandled promise).
   - Scale ECS service by $+2$ instances or restart task definitions.
3. **If Database Failure:**
   - Execute automated failover to RDS Multi-AZ secondary replica.
   - Failover executes automatically within 60–120 seconds.
4. **Clinic Communication:**
   - Auto-trigger emergency broadcast to Clinic WhatsApp Channel: *"Central sync delayed. All clinics remain in offline mode on tablets/desktops. Work normally."*
5. **Post-Mortem:**
   - Conduct Root Cause Analysis (RCA) within 24 hours; submit formal report to Special Commissioner.

### Playbook 2: Widespread Clinic Network Disconnection (P2 Severity)
1. **Scenario:** BESCOM power surge or BSNL regional fiber cut affecting multiple wards in East/North Zone.
2. **Action:**
   - Frontline staff instructed to confirm 4G backup router operation.
   - PWA offline caching automatically absorbs consultations.
   - Review pending sync queue volume on Grafana: monitor buffer until connectivity is restored.
   - When fiber recovers, monitor sync worker throttling to prevent database thundering herd.
