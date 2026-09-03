import os
import sys

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

# ==========================================
# PHASE 12: DEVOPS / CI/CD PLAN
# ==========================================

def build_phase_12():
    base_dir = os.path.join("docs", "12-devops")
    
    envs_content = """# 🌐 Six-Tier Environment Strategy & Promotion Pipeline
## Namma Clinic Digital Health & Operations Platform
**Document Code:** DEV-ENV-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Environment Architecture & Isolation Matrix

| Environment | Purpose | Infrastructure & Sizing | Database Strategy | Deployment Trigger | Approval Required |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Local** | Developer workstation development and unit testing. | Docker Compose (Node, PG16, Redis). | Ephemeral Docker container with synthetic seed data. | Manual `docker compose up`. | None (Developer). |
| **Development** | Continuous integration testing and feature branch verification. | AWS ECS Fargate / Single RDS instance (`db.t4g.medium`). | Shared Dev DB with automated daily seed reset. | Push to `feature/*` or `develop`. | Automated CI green. |
| **Test (QA)** | System integration testing, automated regression, and load testing. | AWS ECS Fargate / RDS Multi-AZ (`db.t4g.large`). | Test DB with sanitized synthetic 10k patient datasets. | Automated merge to `develop`. | QA Lead sign-off. |
| **Staging** | Production mirror for UAT, security scans, and rehearsal. | AWS ECS Fargate / RDS Multi-AZ (`db.m6g.xlarge`). | Anonymized production-like data snapshot. | Automated merge to `release/*`. | Architect & PM. |
| **Pilot (20 Clinics)**| Live field deployment in 20 designated pilot Namma Clinics. | Dedicated VPC / Production RDS Multi-AZ (`db.r6g.xlarge`). | Production pilot database with full PITR backups. | Manual release tag `v1.0.0-pilot`. | GBA Steering Gate 11. |
| **Production (183 Clinics)**| Citywide live operational deployment across Bengaluru. | High-Availability Multi-AZ (`db.r6g.2xlarge` + Read Replicas). | Sovereign Production Database with strict encryption. | Manual release tag `v1.0.0`. | Gate 12 Final Approval. |
"""
    write_file(os.path.join(base_dir, "02-environments.md"), envs_content)

    devops_files = [
        ("01-devops-architecture.md", "DevOps & Cloud Operations Blueprint", "GitOps delivery model, automated testing gates, infrastructure-as-code, and cloud security."),
        ("03-git-strategy.md", "Git Workflow & Repository Standards", "Branch naming conventions (`feature/`, `bugfix/`, `release/`), conventional commits (`feat:`, `fix:`)."),
        ("04-branching-strategy.md", "Trunk-Based Branching Model", "Short-lived branches merged to develop via reviewed Pull Requests with zero long-lived divergence."),
        ("05-pr-strategy.md", "Pull Request Governance & Review Rules", "Mandatory 2 approvals, 100% CI pass, SonarQube quality gate, zero merge commits (Squash & Merge)."),
        ("06-ci-pipeline.md", "GitHub Actions CI Pipeline Specification", "Automated pipeline: TypeScript check, Vitest unit tests, Playwright E2E, Docker build, Trivy scan."),
        ("07-cd-pipeline.md", "ArgoCD / GitOps Continuous Delivery Plan", "Declarative Kubernetes / ECS deployment with automated progressive canary rollouts."),
        ("08-docker-strategy.md", "Containerization & Dockerfile Architecture", "Multi-stage unprivileged Alpine-based Docker images with SBOM generation and layer caching."),
        ("09-cloud-architecture.md", "Cloud Infrastructure Blueprint (AWS / SDC)", "VPC architecture with public, private, and database subnets across 3 Availability Zones."),
        ("10-infrastructure-as-code.md", "Terraform Infrastructure as Code Strategy", "Modular Terraform repository defining VPC, ECS, RDS, Redis, WAF, and KMS resources."),
        ("11-secrets.md", "Secrets Management & Vault Architecture", "AWS Secrets Manager / HashiCorp Vault dynamic credential injection into container runtime."),
        ("12-monitoring.md", "Observability & Prometheus Metric Collection", "Monitoring RED metrics (Rate, Errors, Duration), database connection pools, and clinic sync queues."),
        ("13-logging.md", "Centralized Structured Logging (Loki)", "JSON structured logs with trace IDs, redaction of PII, and 90-day searchable retention."),
        ("14-alerting.md", "Alerting Policies & Escalation Matrix", "Alertmanager routing P0 outages to PagerDuty/SMS, P1 errors to Slack engineering channel."),
        ("15-backup.md", "Database Backup & Snapshots Policy", "Automated continuous WAL archiving with 5-minute RPO, daily snapshots stored in immutable S3."),
        ("16-disaster-recovery.md", "Disaster Recovery Playbook & Failover Drills", "Automated multi-AZ failover procedure and cross-region cold standby recovery plan."),
        ("17-rollbacks.md", "Zero-Downtime Rollback Strategy", "Instant container image rollback (<2 mins) and backward-compatible database schema design."),
        ("18-release-management.md", "Release Management & Semantic Versioning", "SemVer 2.0 (`vMAJOR.MINOR.PATCH`), changelog generation, and signed release artifacts."),
        ("19-production-readiness.md", "Production Readiness Review (PRR) Checklist", "Comprehensive 50-point PRR checklist required before citywide go-live authorization.")
    ]

    for fname, title, desc in devops_files:
        write_file(os.path.join(base_dir, fname), f"# 🛠️ DevOps Specification: {title}\n## Namma Clinic Platform\n\n### 1. Specification\n{desc}")

# ==========================================
# PHASE 13: DATA ENGINEERING & ANALYTICS
# ==========================================

def build_phase_13():
    base_dir = os.path.join("docs", "13-data")
    
    star_content = """# ⭐ Analytics Star Schema Architecture
## Namma Clinic Digital Health & Operations Platform
**Document Code:** DTA-STR-03 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Dimensional Architecture & Star Schema Model

```mermaid
erDiagram
    dim_patient ||--o{ fact_visits : logs
    dim_clinic ||--o{ fact_visits : hosts
    dim_date ||--o{ fact_visits : occurs_on
    dim_diagnosis ||--o{ fact_visits : diagnosed

    dim_clinic ||--o{ fact_medicine_issues : dispensed_at
    dim_medicine ||--o{ fact_medicine_issues : consumes
    dim_date ||--o{ fact_medicine_issues : dispensed_on

    dim_clinic ||--o{ fact_referrals : referred_from
    dim_date ||--o{ fact_referrals : referred_on

    dim_clinic ||--o{ fact_inventory_daily : snapshot_at
    dim_medicine ||--o{ fact_inventory_daily : counts
    dim_date ||--o{ fact_inventory_daily : snapshot_on
```

### 2. Core Fact & Dimension Table Definitions
- `fact_visits`: Outpatient visit counts, wait duration, triage category, consultation time.
- `fact_medicine_issues`: Quantity dispensed by drug, batch, clinic, and patient age bracket.
- `fact_referrals`: Outbound referral volume, destination facility, primary clinical reason.
- `fact_inventory_daily`: End-of-day stock snapshots, days of supply remaining, stockout flags.
- `dim_patient`: Anonymized demographics (age bracket, gender, ward of residence).
- `dim_clinic`: Clinic metadata (Ward, Zone, Medical Officer in charge, operational status).
- `dim_medicine`: Formulary drug metadata (therapeutic class, strength, dosage form).
- `dim_diagnosis`: ICD-10 chapter, syndromic surveillance category (e.g., Acute Febrile Illness).
- `dim_date`: Gregorian calendar date dimension with municipal fiscal year mapping.
"""
    write_file(os.path.join(base_dir, "03-star-schema.md"), star_content)

    data_files = [
        ("01-data-engineering-architecture.md", "Data Engineering & Analytics Architecture", "Architectural overview of OLTP-to-OLAP streaming pipeline and executive reporting."),
        ("02-oltp-olap-separation.md", "OLTP and OLAP Separation Strategy", "Isolating high-write clinic transactions from complex analytical queries via read-replicas."),
        ("04-etl-elt-strategy.md", "Batch ELT & Aggregation Pipeline", "Hourly micro-batches and nightly aggregations transforming transactional tables to Star Schema."),
        ("05-cdc-strategy.md", "Change Data Capture (CDC) Architecture", "Debezium / PostgreSQL logical replication streaming change events to analytical datastore."),
        ("06-data-quality.md", "Data Quality & Anomaly Detection", "Automated data validation rules testing for null foreign keys, negative quantities, and outliers."),
        ("07-data-lineage.md", "Analytics Data Lineage Specification", "End-to-end tracing from frontline patient entry to GBA executive command dashboard."),
        ("08-data-governance.md", "Data Governance & Anonymization Strategy", "Strict removal of Direct Identifiers (Name, Phone, Aadhaar) prior to analytical persistence."),
        ("09-dashboard-metrics.md", "Master Public Health & Operational Metrics", "Catalog of 25 core health KPIs with exact SQL aggregation formulas and refresh schedules."),
        ("10-clinic-kpis.md", "Clinic-Level Performance Indicators", "Daily OPD footfall, average wait time (<15m), stockout rate (<2%), consultation duration."),
        ("11-zonal-kpis.md", "Zonal-Level Public Health KPIs", "Zonal morbidity rankings, dengue/fever cluster rates, referral completion ratios."),
        ("12-city-kpis.md", "Citywide Executive Health Indicators", "Bengaluru urban primary care coverage, total consultations, NCD screening rates."),
        ("13-public-health-metrics.md", "Syndromic Surveillance & Outbreak Metrics", "Threshold triggers for fever spikes, acute diarrheal disease, and respiratory infections."),
        ("14-inventory-analytics.md", "Medicine Inventory & Supply Chain Analytics", "Consumption velocity, lead times, near-expiry drug wastage warnings, stockout risks."),
        ("15-referral-analytics.md", "Secondary Referral Analytics", "Referral loop closure rates, secondary hospital load distribution, high-referral clinics.")
    ]

    for fname, title, desc in data_files:
        write_file(os.path.join(base_dir, fname), f"# 📊 Data Engineering Specification: {title}\n## Namma Clinic Platform\n\n### 1. Overview\n{desc}")

# ==========================================
# PHASE 14: AI / ML PLAN
# ==========================================

def build_phase_14():
    base_dir = os.path.join("docs", "14-ai")
    
    gov_content = """# 🤖 AI Clinical Governance & Ethical Guardrails
## Namma Clinic Digital Health & Operations Platform
**Document Code:** AI-GOV-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Mandatory Clinical AI Principles

```
+-------------------------------------------------------------------------+
|                      MANDATORY AI SAFETY INVARIANTS                     |
+-------------------------------------------------------------------------+
| 1. ZERO AUTONOMOUS DIAGNOSIS                                            |
|    Under zero circumstances will the system generate an autonomous      |
|    clinical diagnosis, triage decision, or final prescription.          |
+-------------------------------------------------------------------------+
| 2. STRICT DECISION SUPPORT ONLY                                         |
|    AI outputs are restricted to decision-support suggestions:           |
|    - Medicine stockout risk forecasting (Supply Chain)                  |
|    - Syndromic fever anomaly detection (Surveillance)                   |
|    - NCD follow-up recall prioritization (Chronic Care)                 |
+-------------------------------------------------------------------------+
| 3. MANDATORY PHYSICIAN OVERRIDE & AUDIT                                 |
|    Every clinical suggestion must be explicitly accepted or rejected by |
|    a licensed Medical Officer; rejections are logged for model tuning.  |
+-------------------------------------------------------------------------+
| 4. EXPLAINABLE INFERENCE & CONFIDENCE SCORES                            |
|    Every prediction must display its confidence score and contributing  |
|    features (e.g. 'Fever cases increased 3.2x above 14-day ward mean'). |
+-------------------------------------------------------------------------+
```
"""
    write_file(os.path.join(base_dir, "02-ai-governance.md"), gov_content)

    ai_files = [
        ("01-ai-strategy.md", "AI Strategy & Roadmap", "Deploying high-impact, low-risk machine learning models for public health operations."),
        ("03-ai-use-cases.md", "Catalog of Approved AI Use Cases", "Use Case 1: Stockout Forecasting, Use Case 2: Fever Outbreak, Use Case 3: NCD Recall."),
        ("04-stock-forecasting.md", "Medicine Stockout Forecasting Model", "Time-series forecasting (Prophet / LightGBM) predicting 30-day clinic drug depletion."),
        ("05-fever-anomaly-detection.md", "Syndromic Outbreak Anomaly Detection Model", "Spatial-temporal anomaly detection (Isolation Forest / CUSUM) flagging ward fever spikes."),
        ("06-ncd-recall-prioritization.md", "NCD Patient Recall Prioritization Model", "Risk scoring algorithm ranking hypertensive/diabetic patients overdue for checkups."),
        ("07-feature-engineering.md", "Feature Engineering & Input Pipelines", "Aggregating historical encounter counts, seasonality, temperature, and holiday calendars."),
        ("08-model-data-requirements.md", "Training Data Requirements & Anonymization", "Strictly anonymized historical clinic records; zero PII ingested into ML training sets."),
        ("09-model-evaluation.md", "Model Evaluation & Offline Validation", "Evaluation metrics: RMSE for stock forecasts, Precision/Recall (F1 >= 0.82) for anomalies."),
        ("10-model-monitoring.md", "Model Drift & Performance Monitoring", "Automated monitoring of data drift, feature drift, and prediction accuracy degradation."),
        ("11-human-approval.md", "Human-in-the-Loop Sign-off Workflows", "Doctor and pharmacist review interfaces with 1-click confirmation or override reasons."),
        ("12-ai-safety.md", "AI Safety & Bias Mitigation Policy", "Regular algorithmic bias audits across demographic groups, age brackets, and clinic zones."),
        ("13-model-versioning.md", "MLOps Pipeline & Model Versioning", "Model registry tracking versioned model weights, hyperparameters, and lineage.")
    ]

    for fname, title, desc in ai_files:
        write_file(os.path.join(base_dir, fname), f"# 🤖 AI Specification: {title}\n## Namma Clinic Platform\n\n### 1. Overview\n{desc}")

# ==========================================
# PHASE 15: INTEGRATION PLAN
# ==========================================

def build_phase_15():
    base_dir = os.path.join("docs", "15-integrations")
    
    abdm_content = """# 🇮🇳 Ayushman Bharat Digital Mission (ABDM) Integration
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
"""
    write_file(os.path.join(base_dir, "02-abha-abdm.md"), abdm_content)

    int_files = [
        ("01-integration-architecture.md", "Integration Architecture & Middleware Blueprint", "Enterprise service bus, asynchronous retry queues, webhook handlers, and mTLS security."),
        ("03-fhir.md", "HL7 FHIR R4 Bundle Specification", "Detailed JSON mapping of Namma Clinic clinical records to Indian national FHIR profiles."),
        ("04-eHospital.md", "eHospital & Secondary Facility Referral Bridge", "Outbound referral JSON payload transmission to BBMP General Hospitals and Bowring College."),
        ("05-sms.md", "Karnataka State SMS Gateway (KSDG) Integration", "Transactional SMS dispatch for queue tokens, prescription summaries, and doctor alerts."),
        ("06-state-reporting.md", "Karnataka HMIS / IHIP Reporting Bridge", "Automated daily export of syndromic disease counts to Integrated Health Information Platform."),
        ("07-file-export.md", "Standardized Data Portability & File Exports", "Citizen right to data portability under DPDP Act: downloadable JSON, PDF, and CSV summaries."),
        ("08-integration-security.md", "Integration Security & Mutual TLS (mTLS)", "Enforcing mTLS, OAuth2 Client Credentials, and digital signature validation for external APIs."),
        ("09-integration-error-handling.md", "External Fault Tolerance & Dead Letter Queues", "Exponential backoff, circuit breakers, and dead letter queues for resilient external calls."),
        ("10-integration-monitoring.md", "Third-Party API Latency & Uptime Monitoring", "Real-time tracking of ABDM gateway response times and SMS provider delivery rates."),
        ("11-sandbox-vs-production.md", "Sandbox Validation & Production Cutover Plan", "Step-by-step checklist for promoting external integrations from sandbox to live production.")
    ]

    for fname, title, desc in int_files:
        write_file(os.path.join(base_dir, fname), f"# 🔌 Integration Specification: {title}\n## Namma Clinic Platform\n\n### 1. Overview\n{desc}")

def main():
    build_phase_12()
    build_phase_13()
    build_phase_14()
    build_phase_15()

if __name__ == "__main__":
    main()
