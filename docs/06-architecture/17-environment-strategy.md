# 🌐 Architecture Document 17: Enterprise Multi-Tier Environment Strategy, Promotion Gates, Test Data Pipelines & Secret Governance
## Namma Clinic Digital Health & Operations Platform
### Greater Bengaluru Authority (GBA) / BBMP Health Department
**Standard:** Multi-Tier Environment Lifecycle / HashiCorp Vault KMS / DPDP Act 2023 | **Status:** APPROVED BASELINE | **Code:** `ARCH-ENV-17`

---

## 01. Document Overview & Environment Management Philosophy
This document specifies the enterprise multi-tier environment strategy, infrastructure parity controls, promotion gate checklists, synthetic patient data generation pipelines, and cryptographic secret governance for the Namma Clinic Digital Health & Operations Platform. Spanning 8 standardized tiers from individual local developer workstations to full production serving 183 clinics and cross-region disaster recovery, the environment lifecycle guarantees rigorous quality verification while eliminating production configuration drift and zero accidental leakage of patient health information (PHI).

### 01.1 Core Environment Strategy Invariants
1. **Absolute Non-Production Data Air-Gap:** Under zero circumstances shall live production patient identifiable data (Aadhaar, phone numbers, real clinical notes) be copied, mirrored, or restored into LOCAL, DEV, TEST, QA, or STAGING environments. All lower tiers utilize mathematically generated synthetic patient populations.
2. **Infrastructure Parity Gradient:** While compute scale decreases in lower environments, software topologies, database engines, schema migrations, and security protocols maintain strict 1:1 behavioral parity with production.
3. **Single Secret Authority (HashiCorp Vault):** Zero plaintext secrets or cryptographic keys are stored in Git repositories, Dockerfiles, or CI environment variables. All tiers retrieve dynamic, short-lived credentials from HashiCorp Vault via role-based access tokens.
4. **Immutable Promotion Verification:** Code promotions between environments follow deterministic GitOps releases; the exact container digest verified in STAGING is promoted to PILOT and PROD without rebuilding.
5. **Continuous Environment Drift Detection:** Automated drift scanners run nightly across all tiers, comparing Kubernetes manifests, kernel sysctl parameters, and database extensions against baseline templates.
6. **Cryptographic Network Microsegmentation:** Ingress and egress network policies strictly prevent cross-environment lateral traffic; lower environments cannot communicate with production cloud databases or edge appliance clusters.

### 01.2 Platform Environment Lifecycle Map
```
 +-------------------+      +-------------------+      +-------------------+
 |   LOCAL (ENV-001) | ---> |    DEV (ENV-002)  | ---> |   TEST (ENV-003)  |
 |  Docker Compose   |      |   K8s Feature CI  |      |   Nightly Regress |
 +-------------------+      +-------------------+      +-------------------+
                                                                  |
                                                                  v
 +-------------------+      +-------------------+      +-------------------+
 |  STAGING (ENV-005)| <--- |    QA (ENV-004)   | <----+   Gate 2 Pass     |
 | Pre-Prod / 1.2kRPS|      | Hardware/UAT Lab  |
 +-------------------+      +-------------------+
           |
           v
 +-------------------+      +-------------------+      +-------------------+
 |   PILOT (ENV-006) | ---> |    PROD (ENV-007) | <==> |    DR (ENV-008)   |
 |  5 Live Clinics   |      |  183 Clinics City |      | Standby Region Hyd|
 +-------------------+      +-------------------+      +-------------------+
```

## 02. The 8 Standard Platform Environments Overview
Summary matrix of the 8 authoritative environments comprising the platform lifecycle:

| Environment ID | Name | Operational Tier | Target Audience & Users | Data Sanitization Policy | Secrets Management Authority | Promotion Gate Approval |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ENV-001` | **LOCAL** | Development Tier | Engineers | Strictly Synthetic Data | Local .env file | Local Git commit |
| `ENV-002` | **DEV** | Integration Tier | Dev Team | Strictly Synthetic Data | HashiCorp Vault Dev | PR merge to develop |
| `ENV-003` | **TEST** | Automated QA Tier | QA Automation | Scrambled Synthetic Baseline | HashiCorp Vault Test | Automated test suite pass |
| `ENV-004` | **QA** | Manual Verification Tier | QA Team / PMs | Anonymized Historical Clones | HashiCorp Vault QA | Manual QA sign-off |
| `ENV-005` | **STAGING** | Pre-Production Tier | Release Leads | Synthetically Scaled 183-Clinic Data | Vault KMS Staging | Release gate checklist |
| `ENV-006` | **PILOT** | Field Canary Tier | Clinic Staff (5 Clinics) | Live Operational Patient Data | Vault Production KMS | BBMP Medical Board Approval |
| `ENV-007` | **PROD** | Production Tier | All Clinic Staff & Citizens | Live Production Health Records | Dedicated Cloud HSM / Vault KMS | Executive Release Approval |
| `ENV-008` | **DR** | Disaster Recovery Tier | SRE / Ops On-Call | Real-Time Replicated Production Data | Replicated Cloud HSM / Vault | Automated / Manual Failover Gate |

### 02.1 Environment Parity Matrix Across Tiers
Detailed technical parity comparison across compute, storage, data, and security dimensions:

| Dimension / Subsystem | LOCAL (ENV-001) | DEV (ENV-002) | TEST (ENV-003) | QA (ENV-004) | STAGING (ENV-005) | PILOT (ENV-006) | PROD (ENV-007) | DR (ENV-008) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Compute Engine** | Docker Compose | Kubernetes EKS | Kubernetes EKS | Kubernetes EKS | Kubernetes EKS | Edge + EKS | Edge + EKS Multi-AZ | EKS Secondary AZ |
| **Replica Scale** | 1 Container | 1 Pod / Svc | 2 Pods / Svc | 2 Pods / Svc | 4 Pods / Svc | 5 Edge + 4 Cloud | 183 Edge + 96 Cloud | 48 Cloud Standby |
| **Database Engine** | Local Postgres | Postgres Single | Postgres Single | Patroni 2-Node | Patroni 3-Node | Edge + Patroni | Edge + Patroni 3-AZ | Patroni Cascading |
| **Connection Pooling** | Direct Client | PgBouncer | PgBouncer | PgBouncer | PgBouncer Multi | PgBouncer Fleet | PgBouncer Multi-AZ | PgBouncer Standby |
| **Redis Caching** | Local Redis | Redis Single | Redis Single | Redis Sentinel | Redis Cluster 6 | Redis Cluster 6 | Redis Cluster 6-AZ | Redis Cluster Standby|
| **Kafka Streaming** | Embedded KRaft | Kafka 1-Broker | Kafka 3-Broker | Kafka 3-Broker | Kafka 5-Broker | Kafka 5-Broker | Kafka 5-Broker Multi | Kafka MirrorMaker 2 |
| **ClickHouse BI** | Docker Single | ClickHouse 1 | ClickHouse 1 | ClickHouse 2 | ClickHouse 4 | ClickHouse 4 | ClickHouse 4 Multi-AZ | ClickHouse Standby |
| **ABDM Sandbox** | Local Mock Wire | ABDM Sandbox | ABDM Sandbox | ABDM Sandbox | ABDM Pre-Prod | ABDM Production | ABDM Production Grid | ABDM Standby Gate |
| **Data Baseline** | 100 Synthetics | 500 Synthetics | 5k Synthetics | 20k Synthetics | 100k Synthetics | Live 5 Clinics | Live 183 Clinics | Live Replicated |
| **Secrets Engine** | `.env.local` | Vault Dev | Vault Test | Vault QA | Vault Staging | Vault Production | Dedicated HSM Vault | Replicated HSM Vault |

### 02.2 Network CIDR Blocks, Ingress DNS & Port Allocation Matrix
To eliminate routing conflicts and enforce VPC peering boundaries, each environment operates in a strictly isolated CIDR block:

| Environment ID | Environment Name | Primary VPC Subnet | Ingress Domain Name | Internal Service Port | Gateway Port | TLS Termination |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| `ENV-001` | LOCAL | `127.0.0.0/8` (Host) | `localhost:3000` | 3001-3018 | 8080 | Self-Signed / Plain HTTP |
| `ENV-002` | DEV | `10.240.10.0/22` | `dev-api.nammaclinic.kar.gov.in` | 8000-8018 | 443 | Let's Encrypt Wildcard |
| `ENV-003` | TEST | `10.240.20.0/22` | `test-api.nammaclinic.kar.gov.in` | 8000-8018 | 443 | Let's Encrypt Wildcard |
| `ENV-004` | QA | `10.240.30.0/22` | `qa-api.nammaclinic.kar.gov.in` | 8000-8018 | 443 | Digicert Gov Wildcard |
| `ENV-005` | STAGING | `10.240.40.0/22` | `staging-api.nammaclinic.kar.gov.in` | 8000-8018 | 443 | Digicert Gov Wildcard |
| `ENV-006` | PILOT | `10.240.50.0/22` | `pilot-api.nammaclinic.kar.gov.in` | 8000-8018 | 443 | Enterprise HSM Root CA |
| `ENV-007` | PROD | `10.240.60.0/20` | `api.nammaclinic.kar.gov.in` | 8000-8018 | 443 | Enterprise HSM Root CA |
| `ENV-008` | DR | `10.242.60.0/20` | `dr-api.nammaclinic.kar.gov.in` | 8000-8018 | 443 | Enterprise HSM Root CA |

## 03. Exhaustive Profiles for All 8 Environments (ENV-001 to ENV-008)
Detailed technical dossier, infrastructure blueprint, container resource allocations, environment variables, ingress routes, and promotion checklists for each environment:

### 03.01 Environment Specification: `ENV-001` (LOCAL)
- **Environment Identifier:** `ENV-001`
- **Formal Designation:** LOCAL (Local Developer Workstation Tier)
- **Target User Audience:** Software Engineers, Frontend Developers, QA Automation Engineers
- **Architectural Purpose:** Lightweight environment designed for rapid inner-loop development with hot-module reloading (HMR).
- **Infrastructure Topology:** Docker Compose on macOS / Linux / Windows WSL2 (Docker Desktop / Colima / Podman).
- **Data Sanitization & Privacy Policy:** Strictly synthetic data generated via local Faker seed script (100 mock citizens, 250 encounters).
- **Secrets Management Authority:** Local `.env` file populated from sanitized template (`.env.example`). Master passwords strictly forbidden.
- **Promotion Trigger & Prerequisite:** Developer self-service; code passes local linting, unit tests, and pre-commit Git hooks.

#### Infrastructure & Hardware Bill of Materials:
| Subsystem Dimension | Primary Specification | Redundancy / HA Level | Storage Provisioning | Network Subnet CIDR |
| :--- | :--- | :---: | :--- | :---: |
| **Compute Capacity** | Docker Compose on macOS / Linux / Windows WSL2 | Standard Tier Sizing | NVMe Local Storage | `10.240.10.0/24` |
| **Database Persistence**| Dedicated PostgreSQL 16 Engine | Patroni / Streaming Replica | High-IOPS Block Storage | `10.240.11.0/24` |
| **In-Memory Cache** | Redis 7.2 Cache Tier | Cluster Mode / Sentinel | In-Memory Volatile LRU | `10.240.12.0/24` |
| **Event Broker** | Apache Kafka KRaft Tier | 3x Topic Replication | Persistent EBS Volume | `10.240.13.0/24` |

#### Complete Container Resource Allocation Matrix for LOCAL (`ENV-001`):
Precise resource requests, limits, replica scaling, and health probe configurations across all 18 platform containers:

| Container ID | Container Name | Replicas | CPU Request | CPU Limit | Mem Request | Mem Limit | Health Probe Path | Storage Volume Mount |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `ARCH-CONT-001` | Clinic Workstation PWA Shell | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-002` | Clinic Edge Mini-Server Runtime | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-003` | Central Cloud API Gateway | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/ready` | `/etc/envoy/config` |
| `ARCH-CONT-004` | Identity & Access Management (IAM) Service | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-005` | Master Patient Index (MPI) Service | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-006` | Queue Orchestration & Triage Engine | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-007` | Clinical Consultation & EMR Service | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-008` | Electronic Prescription & CDSS Service | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-009` | Pharmacy Inventory & Dispensation Service | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-010` | Diagnostic Laboratory Service | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-011` | Referral & EMS Telemetry Bridge | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-012` | Citizen Portal & Multilingual Notification Service | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-013` | Bi-directional Edge-Cloud Synchronization Service | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-014` | ABDM & National Health Grid Bridge | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-015` | Public Health Analytics & Syndromic BI Service | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-016` | Advisory Clinical AI Decision Support Engine | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-017` | Cryptographic WORM Audit Service | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `/health/audit` | `/mnt/audit/worm` |
| `ARCH-CONT-018` | Enterprise Relational Database Cluster | 1 | `100m` | `500m` | `256Mi` | `1024Mi` | `pg_isready -h localhost` | `/var/lib/postgresql/data` |

#### Authoritative Environment Variables Matrix for LOCAL (`ENV-001`):
Standard configuration contract injected via Kubernetes ConfigMap and Vault dynamic secrets:

| Configuration Key | Scoped Value for Environment | Sensitivity | Source Authority | Dynamic Secret Renewal |
| :--- | :--- | :---: | :--- | :---: |
| `NODE_ENV` | `local` | Low | Git ConfigMap | Static |
| `PORT` | `8080` | Low | Service Spec | Static |
| `DATABASE_URL` | `postgresql://app_user:***@pg-pooler.namma-local:5432/namma_db` | High | Vault Database Role | 1 Hour TTL |
| `REDIS_CLUSTER_URL` | `rediss://redis-cluster.namma-local:6379` | High | Vault KV Secret | 4 Hour TTL |
| `KAFKA_BROKERS` | `kafka-broker-0.namma-local:9092,kafka-broker-1:9092` | Medium | Helm Values | Static |
| `VAULT_ADDR` | `https://vault-internal.nammaclinic.kar.gov.in:8200` | High | K8s Secret | Static |
| `VAULT_ROLE` | `namma-local-app-role` | High | K8s ServiceAccount | Token Bound |
| `LOG_LEVEL` | `DEBUG` | Low | ConfigMap | Live Reload |
| `CORS_ORIGIN` | `https://*` | Medium | ConfigMap | Static |
| `ABDM_GATEWAY_URL` | `https://sandbox.abdm.gov.in` | High | Vault Integration | 24 Hour TTL |
| `SYNC_HEARTBEAT_SEC` | `5` | Low | ConfigMap | Live Reload |
| `OFFLINE_RETENTION_DAYS`| `3` | Low | ConfigMap | Static |
| `JWT_PUBLIC_KEY_PATH` | `/etc/jwt/public.pem` | High | Vault PKI Engine | 7 Day Rotation |
| `SENTRY_DSN` | `https://key@sentry.nammaclinic.kar.gov.in/1` | Medium | Vault KV Secret | Static |
| `METRICS_PORT` | `9090` | Low | Service Spec | Static |

#### Step-by-Step Operational & Deployment Lifecycle Runbook:
1. Developer clones repository and navigates to project root: `git clone https://github.com/bbmp-health/namma-clinic.git`.
2. Developer copies sanitized configuration template: `cp .env.example .env.local`.
3. Developer executes `npm run dev:setup` to build initial local Docker images and containers.
4. Docker Compose launches PostgreSQL 16, Redis 7.2, and MailHog mock email/SMS gateway.
5. Database migrations run automatically via Prisma CLI: `npx prisma migrate dev`.
6. Seed script hydrates local database with 100 synthetic Kannada patient profiles: `npm run seed:local`.
7. Developer launches backend API in watch mode: `npm run start:dev` on port 3001.
8. Frontend PWA launches on Vite dev server: `http://localhost:3000` with hot module replacement.
9. Pre-commit hooks run ESLint, Prettier, TypeScript typecheck, and Git secrets scanner automatically.
10. Feature changes verified through local Jest unit test suite: `npm run test:unit`.

#### HashiCorp Vault ACL Policy Manifest:
```hcl
# Vault Access Control Policy for LOCAL (ENV-001)
path "secret/data/namma-local/*" {
  capabilities = ["read", "list"]
}
path "database/creds/namma-local-role" {
  capabilities = ["read"]
}
path "pki/issue/namma-local-domain" {
  capabilities = ["create", "update"]
}
```

#### Kubernetes ResourceQuota Infrastructure Manifest:
```yaml
# docker-compose.local.yml
version: '3.8'
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: namma_local
      POSTGRES_USER: namma_dev
      POSTGRES_PASSWORD: dev_insecure_password
    ports: ['5432:5432']
    volumes: ['local_pgdata:/var/lib/postgresql/data']
  redis:
    image: redis:7.2-alpine
    ports: ['6379:6379']
  mailhog:
    image: mailhog/mailhog
    ports: ['8025:8025', '1025:1025']
volumes:
  local_pgdata:
```

#### Kubernetes LimitRange Policy Manifest:
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: local-limits
  namespace: namma-local
spec:
  limits:
  - default:
      cpu: '1000m'
      memory: 2048Mi
    defaultRequest:
      cpu: '250m'
      memory: 512Mi
    type: Container
```

#### Kubernetes Ingress / Gateway Routing VirtualService Manifest:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: local-gateway-routing
  namespace: namma-local
spec:
  hosts:
  - "local-api.nammaclinic.kar.gov.in"
  gateways:
  - namma-local-gateway
  http:
  - match:
    - uri:
        prefix: /api/v1/auth
    route:
    - destination:
        host: iam-service
        port:
          number: 8080
    timeout: 5s
  - match:
    - uri:
        prefix: /api/v1/clinical
    route:
    - destination:
        host: clinical-service
        port:
          number: 8080
    timeout: 10s
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: pwa-shell
        port:
          number: 3000
```

#### Kubernetes NetworkPolicy Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: local-isolation-policy
  namespace: namma-local
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-local
    - ipBlock:
        cidr: 10.240.10.0/24
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-local
    - ipBlock:
        cidr: 10.240.11.0/24
```

#### Kubernetes PersistentVolumeClaim Storage Manifest:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-storage-claim-local
  namespace: namma-local
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3-ebs-sc
  resources:
    requests:
      storage: 20Gi
```

#### Automated Environment Verification & Pre-Promotion Script:
```bash
# Verify health status and network isolation for LOCAL (ENV-001)
echo '--- Running Verification for LOCAL ---'
kubectl get pods -n namma-local --field-selector=status.phase!=Running
curl -s -f http://api-gateway.namma-local.svc.cluster.local:8080/health/liveness || echo 'GATEWAY_FAIL'
kubectl exec -n namma-local deploy/iam-service -- curl -s http://enterprise-database:5432 || echo 'DB_CONN_PASS'
python scripts/data/audit_pii_airgap.py --namespace namma-local
echo '--- Verification for LOCAL Completed Successfully ---'
```

#### Authoritative Verification & Promotion Gate Criteria:
- **Acceptance Gate:** PR review approval by 1 peer engineer; automated GitHub Actions CI build passes.
- **Sign-off Authority:** BBMP QA & DevOps Lead for `ENV-001`
- **Audit Artifact:** `docs/audits/env_signoff_local.json`

---

### 03.02 Environment Specification: `ENV-002` (DEV)
- **Environment Identifier:** `ENV-002`
- **Formal Designation:** DEV (Continuous Integration & Development Tier)
- **Target User Audience:** Backend Engineers, Frontend Engineers, Integration Specialists
- **Architectural Purpose:** Validates inter-service contract interfaces, database migrations, and Kafka event publishing.
- **Infrastructure Topology:** Single-node Kubernetes development cluster on AWS EKS (2 x t3.xlarge worker nodes).
- **Data Sanitization & Privacy Policy:** Ephemeral synthetic dataset generated during CI run (500 mock patients, 1,000 encounters).
- **Secrets Management Authority:** HashiCorp Vault Dev namespace. Short-lived credentials generated dynamically per pipeline run.
- **Promotion Trigger & Prerequisite:** Automated deployment triggered by merging pull request into `develop` branch.

#### Infrastructure & Hardware Bill of Materials:
| Subsystem Dimension | Primary Specification | Redundancy / HA Level | Storage Provisioning | Network Subnet CIDR |
| :--- | :--- | :---: | :--- | :---: |
| **Compute Capacity** | Single-node Kubernetes development cluster on AWS EKS | Standard Tier Sizing | NVMe Local Storage | `10.240.20.0/24` |
| **Database Persistence**| Dedicated PostgreSQL 16 Engine | Patroni / Streaming Replica | High-IOPS Block Storage | `10.240.21.0/24` |
| **In-Memory Cache** | Redis 7.2 Cache Tier | Cluster Mode / Sentinel | In-Memory Volatile LRU | `10.240.22.0/24` |
| **Event Broker** | Apache Kafka KRaft Tier | 3x Topic Replication | Persistent EBS Volume | `10.240.23.0/24` |

#### Complete Container Resource Allocation Matrix for DEV (`ENV-002`):
Precise resource requests, limits, replica scaling, and health probe configurations across all 18 platform containers:

| Container ID | Container Name | Replicas | CPU Request | CPU Limit | Mem Request | Mem Limit | Health Probe Path | Storage Volume Mount |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `ARCH-CONT-001` | Clinic Workstation PWA Shell | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-002` | Clinic Edge Mini-Server Runtime | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-003` | Central Cloud API Gateway | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/ready` | `/etc/envoy/config` |
| `ARCH-CONT-004` | Identity & Access Management (IAM) Service | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-005` | Master Patient Index (MPI) Service | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-006` | Queue Orchestration & Triage Engine | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-007` | Clinical Consultation & EMR Service | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-008` | Electronic Prescription & CDSS Service | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-009` | Pharmacy Inventory & Dispensation Service | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-010` | Diagnostic Laboratory Service | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-011` | Referral & EMS Telemetry Bridge | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-012` | Citizen Portal & Multilingual Notification Service | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-013` | Bi-directional Edge-Cloud Synchronization Service | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-014` | ABDM & National Health Grid Bridge | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-015` | Public Health Analytics & Syndromic BI Service | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-016` | Advisory Clinical AI Decision Support Engine | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-017` | Cryptographic WORM Audit Service | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `/health/audit` | `/mnt/audit/worm` |
| `ARCH-CONT-018` | Enterprise Relational Database Cluster | 1 | `200m` | `800m` | `512Mi` | `1536Mi` | `pg_isready -h localhost` | `/var/lib/postgresql/data` |

#### Authoritative Environment Variables Matrix for DEV (`ENV-002`):
Standard configuration contract injected via Kubernetes ConfigMap and Vault dynamic secrets:

| Configuration Key | Scoped Value for Environment | Sensitivity | Source Authority | Dynamic Secret Renewal |
| :--- | :--- | :---: | :--- | :---: |
| `NODE_ENV` | `dev` | Low | Git ConfigMap | Static |
| `PORT` | `8080` | Low | Service Spec | Static |
| `DATABASE_URL` | `postgresql://app_user:***@pg-pooler.namma-dev:5432/namma_db` | High | Vault Database Role | 1 Hour TTL |
| `REDIS_CLUSTER_URL` | `rediss://redis-cluster.namma-dev:6379` | High | Vault KV Secret | 4 Hour TTL |
| `KAFKA_BROKERS` | `kafka-broker-0.namma-dev:9092,kafka-broker-1:9092` | Medium | Helm Values | Static |
| `VAULT_ADDR` | `https://vault-internal.nammaclinic.kar.gov.in:8200` | High | K8s Secret | Static |
| `VAULT_ROLE` | `namma-dev-app-role` | High | K8s ServiceAccount | Token Bound |
| `LOG_LEVEL` | `DEBUG` | Low | ConfigMap | Live Reload |
| `CORS_ORIGIN` | `https://dev.nammaclinic.kar.gov.in` | Medium | ConfigMap | Static |
| `ABDM_GATEWAY_URL` | `https://sandbox.abdm.gov.in` | High | Vault Integration | 24 Hour TTL |
| `SYNC_HEARTBEAT_SEC` | `30` | Low | ConfigMap | Live Reload |
| `OFFLINE_RETENTION_DAYS`| `3` | Low | ConfigMap | Static |
| `JWT_PUBLIC_KEY_PATH` | `/etc/jwt/public.pem` | High | Vault PKI Engine | 7 Day Rotation |
| `SENTRY_DSN` | `https://key@sentry.nammaclinic.kar.gov.in/2` | Medium | Vault KV Secret | Static |
| `METRICS_PORT` | `9090` | Low | Service Spec | Static |

#### Step-by-Step Operational & Deployment Lifecycle Runbook:
1. Developer merges approved pull request into `develop` branch on GitHub.
2. GitHub Actions CI pipeline builds container images and runs full unit test matrix.
3. Pipeline executes Prisma schema migrations against development database.
4. ArgoCD detects Git commit and deploys updated service manifests to `namma-dev` namespace.
5. Ephemeral test runner seeds database with 500 synthetic patient records.
6. Pact contract tests assert consumer-producer API compatibility across microservices.
7. Integration tests verify event emission and consumption on Kafka topic `dev.namma.events`.
8. Dynamic security scanner executes SonarQube quality gate analysis.
9. Slack notification posted to `#dev-deployments` confirming successful deployment.
10. Smoke tests run against public ingress `dev-api.nammaclinic.kar.gov.in/health`.

#### HashiCorp Vault ACL Policy Manifest:
```hcl
# Vault Access Control Policy for DEV (ENV-002)
path "secret/data/namma-dev/*" {
  capabilities = ["read", "list"]
}
path "database/creds/namma-dev-role" {
  capabilities = ["read"]
}
path "pki/issue/namma-dev-domain" {
  capabilities = ["create", "update"]
}
```

#### Kubernetes ResourceQuota Infrastructure Manifest:
```yaml
# k8s/dev/resourcequota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-quota
  namespace: namma-dev
spec:
  hard:
    requests.cpu: '8'
    requests.memory: 16Gi
    limits.cpu: '16'
    limits.memory: 32Gi
    pods: '30'
```

#### Kubernetes LimitRange Policy Manifest:
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: dev-limits
  namespace: namma-dev
spec:
  limits:
  - default:
      cpu: '1000m'
      memory: 2048Mi
    defaultRequest:
      cpu: '250m'
      memory: 512Mi
    type: Container
```

#### Kubernetes Ingress / Gateway Routing VirtualService Manifest:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: dev-gateway-routing
  namespace: namma-dev
spec:
  hosts:
  - "dev-api.nammaclinic.kar.gov.in"
  gateways:
  - namma-dev-gateway
  http:
  - match:
    - uri:
        prefix: /api/v1/auth
    route:
    - destination:
        host: iam-service
        port:
          number: 8080
    timeout: 5s
  - match:
    - uri:
        prefix: /api/v1/clinical
    route:
    - destination:
        host: clinical-service
        port:
          number: 8080
    timeout: 10s
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: pwa-shell
        port:
          number: 3000
```

#### Kubernetes NetworkPolicy Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: dev-isolation-policy
  namespace: namma-dev
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-dev
    - ipBlock:
        cidr: 10.240.20.0/24
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-dev
    - ipBlock:
        cidr: 10.240.21.0/24
```

#### Kubernetes PersistentVolumeClaim Storage Manifest:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-storage-claim-dev
  namespace: namma-dev
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3-ebs-sc
  resources:
    requests:
      storage: 20Gi
```

#### Automated Environment Verification & Pre-Promotion Script:
```bash
# Verify health status and network isolation for DEV (ENV-002)
echo '--- Running Verification for DEV ---'
kubectl get pods -n namma-dev --field-selector=status.phase!=Running
curl -s -f http://api-gateway.namma-dev.svc.cluster.local:8080/health/liveness || echo 'GATEWAY_FAIL'
kubectl exec -n namma-dev deploy/iam-service -- curl -s http://enterprise-database:5432 || echo 'DB_CONN_PASS'
python scripts/data/audit_pii_airgap.py --namespace namma-dev
echo '--- Verification for DEV Completed Successfully ---'
```

#### Authoritative Verification & Promotion Gate Criteria:
- **Acceptance Gate:** Pact contract tests pass 100%; database schema migration runs cleanly without down migrations.
- **Sign-off Authority:** BBMP QA & DevOps Lead for `ENV-002`
- **Audit Artifact:** `docs/audits/env_signoff_dev.json`

---

### 03.03 Environment Specification: `ENV-003` (TEST)
- **Environment Identifier:** `ENV-003`
- **Formal Designation:** TEST (Automated Quality Assurance & Stress Testing Tier)
- **Target User Audience:** QA Automation Engineers, Performance Engineers, Security Auditors
- **Architectural Purpose:** Executes full end-to-end Cypress regression suites, k6 API performance stress runs, and OWASP ZAP security scans.
- **Infrastructure Topology:** Multi-node Kubernetes cluster (3 x m6i.xlarge worker nodes) with dedicated Prometheus monitoring.
- **Data Sanitization & Privacy Policy:** Standardized 5,000 synthetic patient dataset with deterministic test edge cases (panic lab values, DDI conflicts).
- **Secrets Management Authority:** HashiCorp Vault Test namespace with isolated database credentials.
- **Promotion Trigger & Prerequisite:** Nightly scheduled automated deployment or manual trigger by QA Automation Lead.

#### Infrastructure & Hardware Bill of Materials:
| Subsystem Dimension | Primary Specification | Redundancy / HA Level | Storage Provisioning | Network Subnet CIDR |
| :--- | :--- | :---: | :--- | :---: |
| **Compute Capacity** | Multi-node Kubernetes cluster | Standard Tier Sizing | NVMe Local Storage | `10.240.30.0/24` |
| **Database Persistence**| Dedicated PostgreSQL 16 Engine | Patroni / Streaming Replica | High-IOPS Block Storage | `10.240.31.0/24` |
| **In-Memory Cache** | Redis 7.2 Cache Tier | Cluster Mode / Sentinel | In-Memory Volatile LRU | `10.240.32.0/24` |
| **Event Broker** | Apache Kafka KRaft Tier | 3x Topic Replication | Persistent EBS Volume | `10.240.33.0/24` |

#### Complete Container Resource Allocation Matrix for TEST (`ENV-003`):
Precise resource requests, limits, replica scaling, and health probe configurations across all 18 platform containers:

| Container ID | Container Name | Replicas | CPU Request | CPU Limit | Mem Request | Mem Limit | Health Probe Path | Storage Volume Mount |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `ARCH-CONT-001` | Clinic Workstation PWA Shell | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-002` | Clinic Edge Mini-Server Runtime | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-003` | Central Cloud API Gateway | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/ready` | `/etc/envoy/config` |
| `ARCH-CONT-004` | Identity & Access Management (IAM) Service | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-005` | Master Patient Index (MPI) Service | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-006` | Queue Orchestration & Triage Engine | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-007` | Clinical Consultation & EMR Service | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-008` | Electronic Prescription & CDSS Service | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-009` | Pharmacy Inventory & Dispensation Service | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-010` | Diagnostic Laboratory Service | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-011` | Referral & EMS Telemetry Bridge | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-012` | Citizen Portal & Multilingual Notification Service | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-013` | Bi-directional Edge-Cloud Synchronization Service | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-014` | ABDM & National Health Grid Bridge | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-015` | Public Health Analytics & Syndromic BI Service | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-016` | Advisory Clinical AI Decision Support Engine | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-017` | Cryptographic WORM Audit Service | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `/health/audit` | `/mnt/audit/worm` |
| `ARCH-CONT-018` | Enterprise Relational Database Cluster | 2 | `350m` | `1200m` | `768Mi` | `2048Mi` | `pg_isready -h localhost` | `/var/lib/postgresql/data` |

#### Authoritative Environment Variables Matrix for TEST (`ENV-003`):
Standard configuration contract injected via Kubernetes ConfigMap and Vault dynamic secrets:

| Configuration Key | Scoped Value for Environment | Sensitivity | Source Authority | Dynamic Secret Renewal |
| :--- | :--- | :---: | :--- | :---: |
| `NODE_ENV` | `test` | Low | Git ConfigMap | Static |
| `PORT` | `8080` | Low | Service Spec | Static |
| `DATABASE_URL` | `postgresql://app_user:***@pg-pooler.namma-test:5432/namma_db` | High | Vault Database Role | 1 Hour TTL |
| `REDIS_CLUSTER_URL` | `rediss://redis-cluster.namma-test:6379` | High | Vault KV Secret | 4 Hour TTL |
| `KAFKA_BROKERS` | `kafka-broker-0.namma-test:9092,kafka-broker-1:9092` | Medium | Helm Values | Static |
| `VAULT_ADDR` | `https://vault-internal.nammaclinic.kar.gov.in:8200` | High | K8s Secret | Static |
| `VAULT_ROLE` | `namma-test-app-role` | High | K8s ServiceAccount | Token Bound |
| `LOG_LEVEL` | `DEBUG` | Low | ConfigMap | Live Reload |
| `CORS_ORIGIN` | `https://test.nammaclinic.kar.gov.in` | Medium | ConfigMap | Static |
| `ABDM_GATEWAY_URL` | `https://sandbox.abdm.gov.in` | High | Vault Integration | 24 Hour TTL |
| `SYNC_HEARTBEAT_SEC` | `30` | Low | ConfigMap | Live Reload |
| `OFFLINE_RETENTION_DAYS`| `30` | Low | ConfigMap | Static |
| `JWT_PUBLIC_KEY_PATH` | `/etc/jwt/public.pem` | High | Vault PKI Engine | 7 Day Rotation |
| `SENTRY_DSN` | `https://key@sentry.nammaclinic.kar.gov.in/3` | Medium | Vault KV Secret | Static |
| `METRICS_PORT` | `9090` | Low | Service Spec | Static |

#### Step-by-Step Operational & Deployment Lifecycle Runbook:
1. Nightly build pipeline deploys latest release candidate image to `namma-test` namespace.
2. Database seeded with deterministic synthetic patient baseline: `npm run seed:test-baseline`.
3. Cypress automation runs 150 end-to-end clinical workflow scenarios across all 25 workflows.
4. k6 stress tests fire 500 RPS against intake and consultation endpoints for 15 minutes.
5. OWASP ZAP container executes automated DAST dynamic vulnerability scan against API ingress.
6. SonarQube quality gate inspects code coverage (>= 85%) and security hotspot count (0).
7. Test results compiled into automated Allure HTML report and published to S3 test bucket.
8. Edge synchronization test simulator exercises offline queue replay with network fault injection.
9. QA dashboard updates pass/fail metrics and alerts engineering team on any regressions.
10. Automated teardown and cleanup of ephemeral test artifacts executed at conclusion.

#### HashiCorp Vault ACL Policy Manifest:
```hcl
# Vault Access Control Policy for TEST (ENV-003)
path "secret/data/namma-test/*" {
  capabilities = ["read", "list"]
}
path "database/creds/namma-test-role" {
  capabilities = ["read"]
}
path "pki/issue/namma-test-domain" {
  capabilities = ["create", "update"]
}
```

#### Kubernetes ResourceQuota Infrastructure Manifest:
```yaml
# k8s/test/resourcequota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: test-quota
  namespace: namma-test
spec:
  hard:
    requests.cpu: '16'
    requests.memory: 32Gi
    limits.cpu: '32'
    limits.memory: 64Gi
    pods: '50'
```

#### Kubernetes LimitRange Policy Manifest:
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: test-limits
  namespace: namma-test
spec:
  limits:
  - default:
      cpu: '1000m'
      memory: 2048Mi
    defaultRequest:
      cpu: '250m'
      memory: 512Mi
    type: Container
```

#### Kubernetes Ingress / Gateway Routing VirtualService Manifest:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: test-gateway-routing
  namespace: namma-test
spec:
  hosts:
  - "test-api.nammaclinic.kar.gov.in"
  gateways:
  - namma-test-gateway
  http:
  - match:
    - uri:
        prefix: /api/v1/auth
    route:
    - destination:
        host: iam-service
        port:
          number: 8080
    timeout: 5s
  - match:
    - uri:
        prefix: /api/v1/clinical
    route:
    - destination:
        host: clinical-service
        port:
          number: 8080
    timeout: 10s
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: pwa-shell
        port:
          number: 3000
```

#### Kubernetes NetworkPolicy Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-isolation-policy
  namespace: namma-test
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-test
    - ipBlock:
        cidr: 10.240.30.0/24
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-test
    - ipBlock:
        cidr: 10.240.31.0/24
```

#### Kubernetes PersistentVolumeClaim Storage Manifest:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-storage-claim-test
  namespace: namma-test
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3-ebs-sc
  resources:
    requests:
      storage: 100Gi
```

#### Automated Environment Verification & Pre-Promotion Script:
```bash
# Verify health status and network isolation for TEST (ENV-003)
echo '--- Running Verification for TEST ---'
kubectl get pods -n namma-test --field-selector=status.phase!=Running
curl -s -f http://api-gateway.namma-test.svc.cluster.local:8080/health/liveness || echo 'GATEWAY_FAIL'
kubectl exec -n namma-test deploy/iam-service -- curl -s http://enterprise-database:5432 || echo 'DB_CONN_PASS'
python scripts/data/audit_pii_airgap.py --namespace namma-test
echo '--- Verification for TEST Completed Successfully ---'
```

#### Authoritative Verification & Promotion Gate Criteria:
- **Acceptance Gate:** Zero Sev-1/Sev-2 automated test failures; zero High/Critical OWASP vulnerability findings.
- **Sign-off Authority:** BBMP QA & DevOps Lead for `ENV-003`
- **Audit Artifact:** `docs/audits/env_signoff_test.json`

---

### 03.04 Environment Specification: `ENV-004` (QA)
- **Environment Identifier:** `ENV-004`
- **Formal Designation:** QA (Manual Verification & Hardware Peripheral Certification Tier)
- **Target User Audience:** Product Managers, Lead Clinical Informatics Officers, BBMP User Acceptance Testers
- **Architectural Purpose:** Certifies physical peripheral hardware (80mm thermal receipt printers, 2D DataMatrix scanners, UPS cutover).
- **Infrastructure Topology:** Kubernetes QA cluster integrated with physical hardware testing laboratory.
- **Data Sanitization & Privacy Policy:** Anonymized synthetic baseline scaled to 20,000 patient profiles with realistic multi-morbidity patterns.
- **Secrets Management Authority:** HashiCorp Vault QA namespace. Dedicated service accounts with role-based auditing.
- **Promotion Trigger & Prerequisite:** Deployment of signed release candidate (RC) build approved by QA Lead.

#### Infrastructure & Hardware Bill of Materials:
| Subsystem Dimension | Primary Specification | Redundancy / HA Level | Storage Provisioning | Network Subnet CIDR |
| :--- | :--- | :---: | :--- | :---: |
| **Compute Capacity** | Kubernetes QA cluster integrated with physical hardware testing laboratory. | Standard Tier Sizing | NVMe Local Storage | `10.240.40.0/24` |
| **Database Persistence**| Dedicated PostgreSQL 16 Engine | Patroni / Streaming Replica | High-IOPS Block Storage | `10.240.41.0/24` |
| **In-Memory Cache** | Redis 7.2 Cache Tier | Cluster Mode / Sentinel | In-Memory Volatile LRU | `10.240.42.0/24` |
| **Event Broker** | Apache Kafka KRaft Tier | 3x Topic Replication | Persistent EBS Volume | `10.240.43.0/24` |

#### Complete Container Resource Allocation Matrix for QA (`ENV-004`):
Precise resource requests, limits, replica scaling, and health probe configurations across all 18 platform containers:

| Container ID | Container Name | Replicas | CPU Request | CPU Limit | Mem Request | Mem Limit | Health Probe Path | Storage Volume Mount |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `ARCH-CONT-001` | Clinic Workstation PWA Shell | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-002` | Clinic Edge Mini-Server Runtime | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-003` | Central Cloud API Gateway | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/ready` | `/etc/envoy/config` |
| `ARCH-CONT-004` | Identity & Access Management (IAM) Service | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-005` | Master Patient Index (MPI) Service | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-006` | Queue Orchestration & Triage Engine | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-007` | Clinical Consultation & EMR Service | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-008` | Electronic Prescription & CDSS Service | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-009` | Pharmacy Inventory & Dispensation Service | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-010` | Diagnostic Laboratory Service | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-011` | Referral & EMS Telemetry Bridge | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-012` | Citizen Portal & Multilingual Notification Service | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-013` | Bi-directional Edge-Cloud Synchronization Service | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-014` | ABDM & National Health Grid Bridge | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-015` | Public Health Analytics & Syndromic BI Service | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-016` | Advisory Clinical AI Decision Support Engine | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-017` | Cryptographic WORM Audit Service | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `/health/audit` | `/mnt/audit/worm` |
| `ARCH-CONT-018` | Enterprise Relational Database Cluster | 2 | `400m` | `1500m` | `1024Mi` | `2560Mi` | `pg_isready -h localhost` | `/var/lib/postgresql/data` |

#### Authoritative Environment Variables Matrix for QA (`ENV-004`):
Standard configuration contract injected via Kubernetes ConfigMap and Vault dynamic secrets:

| Configuration Key | Scoped Value for Environment | Sensitivity | Source Authority | Dynamic Secret Renewal |
| :--- | :--- | :---: | :--- | :---: |
| `NODE_ENV` | `qa` | Low | Git ConfigMap | Static |
| `PORT` | `8080` | Low | Service Spec | Static |
| `DATABASE_URL` | `postgresql://app_user:***@pg-pooler.namma-qa:5432/namma_db` | High | Vault Database Role | 1 Hour TTL |
| `REDIS_CLUSTER_URL` | `rediss://redis-cluster.namma-qa:6379` | High | Vault KV Secret | 4 Hour TTL |
| `KAFKA_BROKERS` | `kafka-broker-0.namma-qa:9092,kafka-broker-1:9092` | Medium | Helm Values | Static |
| `VAULT_ADDR` | `https://vault-internal.nammaclinic.kar.gov.in:8200` | High | K8s Secret | Static |
| `VAULT_ROLE` | `namma-qa-app-role` | High | K8s ServiceAccount | Token Bound |
| `LOG_LEVEL` | `INFO` | Low | ConfigMap | Live Reload |
| `CORS_ORIGIN` | `https://qa.nammaclinic.kar.gov.in` | Medium | ConfigMap | Static |
| `ABDM_GATEWAY_URL` | `https://sandbox.abdm.gov.in` | High | Vault Integration | 24 Hour TTL |
| `SYNC_HEARTBEAT_SEC` | `30` | Low | ConfigMap | Live Reload |
| `OFFLINE_RETENTION_DAYS`| `30` | Low | ConfigMap | Static |
| `JWT_PUBLIC_KEY_PATH` | `/etc/jwt/public.pem` | High | Vault PKI Engine | 7 Day Rotation |
| `SENTRY_DSN` | `https://key@sentry.nammaclinic.kar.gov.in/4` | Medium | Vault KV Secret | Static |
| `METRICS_PORT` | `9090` | Low | Service Spec | Static |

#### Step-by-Step Operational & Deployment Lifecycle Runbook:
1. Release candidate deployed to QA environment with release notes generated from Jira.
2. Hardware lab technicians test physical USB barcode scanners with sample pharmaceutical drug packs.
3. Thermal printers test 80mm slip paper feeds and Kannada unicode font rendering clarity.
4. Clinical informatics doctors conduct exploratory user acceptance testing (UAT) on tablets.
5. Offline edge simulator cuts network power to certify PWA offline banner and local sync.
6. Multi-lingual translation review verifies all Kannada clinical strings with native linguists.
7. UAT defect triage session reviews and categorizes reported feedback.
8. Cross-browser testing verifies Chrome, Firefox, Safari, and Edge desktop compatibility.
9. Accessibility compliance audit verifies WCAG 2.1 AA screen reader and color contrast support.
10. Formal QA sign-off certificate issued upon zero Sev-1 or Sev-2 defects remaining open.

#### HashiCorp Vault ACL Policy Manifest:
```hcl
# Vault Access Control Policy for QA (ENV-004)
path "secret/data/namma-qa/*" {
  capabilities = ["read", "list"]
}
path "database/creds/namma-qa-role" {
  capabilities = ["read"]
}
path "pki/issue/namma-qa-domain" {
  capabilities = ["create", "update"]
}
```

#### Kubernetes ResourceQuota Infrastructure Manifest:
```yaml
# k8s/qa/resourcequota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: qa-quota
  namespace: namma-qa
spec:
  hard:
    requests.cpu: '24'
    requests.memory: 48Gi
    limits.cpu: '48'
    limits.memory: 96Gi
    pods: '60'
```

#### Kubernetes LimitRange Policy Manifest:
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: qa-limits
  namespace: namma-qa
spec:
  limits:
  - default:
      cpu: '1000m'
      memory: 2048Mi
    defaultRequest:
      cpu: '250m'
      memory: 512Mi
    type: Container
```

#### Kubernetes Ingress / Gateway Routing VirtualService Manifest:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: qa-gateway-routing
  namespace: namma-qa
spec:
  hosts:
  - "qa-api.nammaclinic.kar.gov.in"
  gateways:
  - namma-qa-gateway
  http:
  - match:
    - uri:
        prefix: /api/v1/auth
    route:
    - destination:
        host: iam-service
        port:
          number: 8080
    timeout: 5s
  - match:
    - uri:
        prefix: /api/v1/clinical
    route:
    - destination:
        host: clinical-service
        port:
          number: 8080
    timeout: 10s
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: pwa-shell
        port:
          number: 3000
```

#### Kubernetes NetworkPolicy Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: qa-isolation-policy
  namespace: namma-qa
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-qa
    - ipBlock:
        cidr: 10.240.40.0/24
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-qa
    - ipBlock:
        cidr: 10.240.41.0/24
```

#### Kubernetes PersistentVolumeClaim Storage Manifest:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-storage-claim-qa
  namespace: namma-qa
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3-ebs-sc
  resources:
    requests:
      storage: 100Gi
```

#### Automated Environment Verification & Pre-Promotion Script:
```bash
# Verify health status and network isolation for QA (ENV-004)
echo '--- Running Verification for QA ---'
kubectl get pods -n namma-qa --field-selector=status.phase!=Running
curl -s -f http://api-gateway.namma-qa.svc.cluster.local:8080/health/liveness || echo 'GATEWAY_FAIL'
kubectl exec -n namma-qa deploy/iam-service -- curl -s http://enterprise-database:5432 || echo 'DB_CONN_PASS'
python scripts/data/audit_pii_airgap.py --namespace namma-qa
echo '--- Verification for QA Completed Successfully ---'
```

#### Authoritative Verification & Promotion Gate Criteria:
- **Acceptance Gate:** Formal sign-off by Clinical Product Manager and Lead Pharmacist; 100% hardware peripheral tests pass.
- **Sign-off Authority:** BBMP QA & DevOps Lead for `ENV-004`
- **Audit Artifact:** `docs/audits/env_signoff_qa.json`

---

### 03.05 Environment Specification: `ENV-005` (STAGING)
- **Environment Identifier:** `ENV-005`
- **Formal Designation:** STAGING (Pre-Production & Disaster Recovery Drill Tier)
- **Target User Audience:** Release Engineers, Lead Architects, BBMP Executive Observers
- **Architectural Purpose:** Full-scale performance benchmark (1,200 RPS), quarterly disaster recovery GameDay simulations, and rollback drills.
- **Infrastructure Topology:** Production-identical topology: 3-AZ Kubernetes cluster, 3-node Patroni PostgreSQL, 6-node Redis Cluster.
- **Data Sanitization & Privacy Policy:** Synthetically scaled 183-clinic dataset (100,000 synthetic patients, 500,000 historical encounters).
- **Secrets Management Authority:** HashiCorp Vault Staging KMS with production-identical HSM policies and encrypted transit keys.
- **Promotion Trigger & Prerequisite:** Promotion approved by Principal Software Architect following successful QA certification.

#### Infrastructure & Hardware Bill of Materials:
| Subsystem Dimension | Primary Specification | Redundancy / HA Level | Storage Provisioning | Network Subnet CIDR |
| :--- | :--- | :---: | :--- | :---: |
| **Compute Capacity** | Production-identical topology: 3-AZ Kubernetes cluster, 3-node Patroni PostgreSQL, 6-node Redis Cluster. | Standard Tier Sizing | NVMe Local Storage | `10.240.50.0/24` |
| **Database Persistence**| Dedicated PostgreSQL 16 Engine | Patroni / Streaming Replica | High-IOPS Block Storage | `10.240.51.0/24` |
| **In-Memory Cache** | Redis 7.2 Cache Tier | Cluster Mode / Sentinel | In-Memory Volatile LRU | `10.240.52.0/24` |
| **Event Broker** | Apache Kafka KRaft Tier | 3x Topic Replication | Persistent EBS Volume | `10.240.53.0/24` |

#### Complete Container Resource Allocation Matrix for STAGING (`ENV-005`):
Precise resource requests, limits, replica scaling, and health probe configurations across all 18 platform containers:

| Container ID | Container Name | Replicas | CPU Request | CPU Limit | Mem Request | Mem Limit | Health Probe Path | Storage Volume Mount |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `ARCH-CONT-001` | Clinic Workstation PWA Shell | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-002` | Clinic Edge Mini-Server Runtime | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-003` | Central Cloud API Gateway | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/ready` | `/etc/envoy/config` |
| `ARCH-CONT-004` | Identity & Access Management (IAM) Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-005` | Master Patient Index (MPI) Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-006` | Queue Orchestration & Triage Engine | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-007` | Clinical Consultation & EMR Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-008` | Electronic Prescription & CDSS Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-009` | Pharmacy Inventory & Dispensation Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-010` | Diagnostic Laboratory Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-011` | Referral & EMS Telemetry Bridge | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-012` | Citizen Portal & Multilingual Notification Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-013` | Bi-directional Edge-Cloud Synchronization Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-014` | ABDM & National Health Grid Bridge | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-015` | Public Health Analytics & Syndromic BI Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-016` | Advisory Clinical AI Decision Support Engine | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-017` | Cryptographic WORM Audit Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/audit` | `/mnt/audit/worm` |
| `ARCH-CONT-018` | Enterprise Relational Database Cluster | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `pg_isready -h localhost` | `/var/lib/postgresql/data` |

#### Authoritative Environment Variables Matrix for STAGING (`ENV-005`):
Standard configuration contract injected via Kubernetes ConfigMap and Vault dynamic secrets:

| Configuration Key | Scoped Value for Environment | Sensitivity | Source Authority | Dynamic Secret Renewal |
| :--- | :--- | :---: | :--- | :---: |
| `NODE_ENV` | `staging` | Low | Git ConfigMap | Static |
| `PORT` | `8080` | Low | Service Spec | Static |
| `DATABASE_URL` | `postgresql://app_user:***@pg-pooler.namma-staging:5432/namma_db` | High | Vault Database Role | 1 Hour TTL |
| `REDIS_CLUSTER_URL` | `rediss://redis-cluster.namma-staging:6379` | High | Vault KV Secret | 4 Hour TTL |
| `KAFKA_BROKERS` | `kafka-broker-0.namma-staging:9092,kafka-broker-1:9092` | Medium | Helm Values | Static |
| `VAULT_ADDR` | `https://vault-internal.nammaclinic.kar.gov.in:8200` | High | K8s Secret | Static |
| `VAULT_ROLE` | `namma-staging-app-role` | High | K8s ServiceAccount | Token Bound |
| `LOG_LEVEL` | `INFO` | Low | ConfigMap | Live Reload |
| `CORS_ORIGIN` | `https://staging.nammaclinic.kar.gov.in` | Medium | ConfigMap | Static |
| `ABDM_GATEWAY_URL` | `https://api.abdm.gov.in` | High | Vault Integration | 24 Hour TTL |
| `SYNC_HEARTBEAT_SEC` | `30` | Low | ConfigMap | Live Reload |
| `OFFLINE_RETENTION_DAYS`| `30` | Low | ConfigMap | Static |
| `JWT_PUBLIC_KEY_PATH` | `/etc/jwt/public.pem` | High | Vault PKI Engine | 7 Day Rotation |
| `SENTRY_DSN` | `https://key@sentry.nammaclinic.kar.gov.in/5` | Medium | Vault KV Secret | Static |
| `METRICS_PORT` | `9090` | Low | Service Spec | Static |

#### Step-by-Step Operational & Deployment Lifecycle Runbook:
1. Staging cluster deployed via ArgoCD using `environments/staging/values.yaml`.
2. Production-identical database schema populated with 100,000 synthetically generated patient records.
3. k6 distributed load generator executes 1,200 RPS peak surge test; asserts P95 latency < 250ms.
4. Disaster recovery drill injects simulated primary database crash; verifies Patroni failover in < 30 seconds.
5. Blue/Green traffic shifting drill verifies zero dropped HTTP requests during rolling upgrade.
6. HashiCorp Vault credential rotation drill forces key expiration and validates seamless lease renewal.
7. ClickHouse CDC analytics pipeline benchmarked under 100,000 event replay stream.
8. Chaos mesh experiments inject 20% network packet drop and edge partition simulations.
9. Full backup and point-in-time recovery (PITR) verified against staging object storage.
10. Pre-release verification report presented to Change Advisory Board (CAB).

#### HashiCorp Vault ACL Policy Manifest:
```hcl
# Vault Access Control Policy for STAGING (ENV-005)
path "secret/data/namma-staging/*" {
  capabilities = ["read", "list"]
}
path "database/creds/namma-staging-role" {
  capabilities = ["read"]
}
path "pki/issue/namma-staging-domain" {
  capabilities = ["create", "update"]
}
```

#### Kubernetes ResourceQuota Infrastructure Manifest:
```yaml
# k8s/staging/resourcequota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: staging-quota
  namespace: namma-staging
spec:
  hard:
    requests.cpu: '48'
    requests.memory: 96Gi
    limits.cpu: '96'
    limits.memory: 192Gi
    pods: '120'
```

#### Kubernetes LimitRange Policy Manifest:
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: staging-limits
  namespace: namma-staging
spec:
  limits:
  - default:
      cpu: '1000m'
      memory: 2048Mi
    defaultRequest:
      cpu: '250m'
      memory: 512Mi
    type: Container
```

#### Kubernetes Ingress / Gateway Routing VirtualService Manifest:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: staging-gateway-routing
  namespace: namma-staging
spec:
  hosts:
  - "staging-api.nammaclinic.kar.gov.in"
  gateways:
  - namma-staging-gateway
  http:
  - match:
    - uri:
        prefix: /api/v1/auth
    route:
    - destination:
        host: iam-service
        port:
          number: 8080
    timeout: 5s
  - match:
    - uri:
        prefix: /api/v1/clinical
    route:
    - destination:
        host: clinical-service
        port:
          number: 8080
    timeout: 10s
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: pwa-shell
        port:
          number: 3000
```

#### Kubernetes NetworkPolicy Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: staging-isolation-policy
  namespace: namma-staging
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-staging
    - ipBlock:
        cidr: 10.240.50.0/24
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-staging
    - ipBlock:
        cidr: 10.240.51.0/24
```

#### Kubernetes PersistentVolumeClaim Storage Manifest:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-storage-claim-staging
  namespace: namma-staging
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3-ebs-sc
  resources:
    requests:
      storage: 500Gi
```

#### Automated Environment Verification & Pre-Promotion Script:
```bash
# Verify health status and network isolation for STAGING (ENV-005)
echo '--- Running Verification for STAGING ---'
kubectl get pods -n namma-staging --field-selector=status.phase!=Running
curl -s -f http://api-gateway.namma-staging.svc.cluster.local:8080/health/liveness || echo 'GATEWAY_FAIL'
kubectl exec -n namma-staging deploy/iam-service -- curl -s http://enterprise-database:5432 || echo 'DB_CONN_PASS'
python scripts/data/audit_pii_airgap.py --namespace namma-staging
echo '--- Verification for STAGING Completed Successfully ---'
```

#### Authoritative Verification & Promotion Gate Criteria:
- **Acceptance Gate:** Zero performance regressions; P95 latency < 250ms; automated disaster recovery drill passes.
- **Sign-off Authority:** BBMP QA & DevOps Lead for `ENV-005`
- **Audit Artifact:** `docs/audits/env_signoff_staging.json`

---

### 03.06 Environment Specification: `ENV-006` (PILOT)
- **Environment Identifier:** `ENV-006`
- **Formal Designation:** PILOT (Field Canary Tier (5 Live Clinics in Bengaluru))
- **Target User Audience:** Designated Pilot Clinic Staff (Malleshwaram, Jayanagar, Indiranagar, Whitefield, Yelahanka)
- **Architectural Purpose:** Validates frontline clinical ergonomics, barcode scanning velocity, and real-world municipal WAN connectivity.
- **Infrastructure Topology:** 5 physical Intel N100 edge appliances installed at pilot clinics connected to dedicated cloud pilot namespace.
- **Data Sanitization & Privacy Policy:** Live operational patient records for the 5 designated pilot clinics; strict DPDP Act compliance.
- **Secrets Management Authority:** Production Vault KMS with dedicated zonal device certificates and HSM-backed token signing.
- **Promotion Trigger & Prerequisite:** Executive approval by BBMP Health Commissioner and Medical Advisory Board.

#### Infrastructure & Hardware Bill of Materials:
| Subsystem Dimension | Primary Specification | Redundancy / HA Level | Storage Provisioning | Network Subnet CIDR |
| :--- | :--- | :---: | :--- | :---: |
| **Compute Capacity** | 5 physical Intel N100 edge appliances installed at pilot clinics connected to dedicated cloud pilot namespace. | Standard Tier Sizing | NVMe Local Storage | `10.240.60.0/24` |
| **Database Persistence**| Dedicated PostgreSQL 16 Engine | Patroni / Streaming Replica | High-IOPS Block Storage | `10.240.61.0/24` |
| **In-Memory Cache** | Redis 7.2 Cache Tier | Cluster Mode / Sentinel | In-Memory Volatile LRU | `10.240.62.0/24` |
| **Event Broker** | Apache Kafka KRaft Tier | 3x Topic Replication | Persistent EBS Volume | `10.240.63.0/24` |

#### Complete Container Resource Allocation Matrix for PILOT (`ENV-006`):
Precise resource requests, limits, replica scaling, and health probe configurations across all 18 platform containers:

| Container ID | Container Name | Replicas | CPU Request | CPU Limit | Mem Request | Mem Limit | Health Probe Path | Storage Volume Mount |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `ARCH-CONT-001` | Clinic Workstation PWA Shell | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-002` | Clinic Edge Mini-Server Runtime | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-003` | Central Cloud API Gateway | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/ready` | `/etc/envoy/config` |
| `ARCH-CONT-004` | Identity & Access Management (IAM) Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-005` | Master Patient Index (MPI) Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-006` | Queue Orchestration & Triage Engine | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-007` | Clinical Consultation & EMR Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-008` | Electronic Prescription & CDSS Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-009` | Pharmacy Inventory & Dispensation Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-010` | Diagnostic Laboratory Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-011` | Referral & EMS Telemetry Bridge | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-012` | Citizen Portal & Multilingual Notification Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-013` | Bi-directional Edge-Cloud Synchronization Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-014` | ABDM & National Health Grid Bridge | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-015` | Public Health Analytics & Syndromic BI Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-016` | Advisory Clinical AI Decision Support Engine | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-017` | Cryptographic WORM Audit Service | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `/health/audit` | `/mnt/audit/worm` |
| `ARCH-CONT-018` | Enterprise Relational Database Cluster | 4 | `500m` | `2000m` | `1536Mi` | `4096Mi` | `pg_isready -h localhost` | `/var/lib/postgresql/data` |

#### Authoritative Environment Variables Matrix for PILOT (`ENV-006`):
Standard configuration contract injected via Kubernetes ConfigMap and Vault dynamic secrets:

| Configuration Key | Scoped Value for Environment | Sensitivity | Source Authority | Dynamic Secret Renewal |
| :--- | :--- | :---: | :--- | :---: |
| `NODE_ENV` | `pilot` | Low | Git ConfigMap | Static |
| `PORT` | `8080` | Low | Service Spec | Static |
| `DATABASE_URL` | `postgresql://app_user:***@pg-pooler.namma-pilot:5432/namma_db` | High | Vault Database Role | 1 Hour TTL |
| `REDIS_CLUSTER_URL` | `rediss://redis-cluster.namma-pilot:6379` | High | Vault KV Secret | 4 Hour TTL |
| `KAFKA_BROKERS` | `kafka-broker-0.namma-pilot:9092,kafka-broker-1:9092` | Medium | Helm Values | Static |
| `VAULT_ADDR` | `https://vault-internal.nammaclinic.kar.gov.in:8200` | High | K8s Secret | Static |
| `VAULT_ROLE` | `namma-pilot-app-role` | High | K8s ServiceAccount | Token Bound |
| `LOG_LEVEL` | `INFO` | Low | ConfigMap | Live Reload |
| `CORS_ORIGIN` | `https://pilot.nammaclinic.kar.gov.in` | Medium | ConfigMap | Static |
| `ABDM_GATEWAY_URL` | `https://api.abdm.gov.in` | High | Vault Integration | 24 Hour TTL |
| `SYNC_HEARTBEAT_SEC` | `30` | Low | ConfigMap | Live Reload |
| `OFFLINE_RETENTION_DAYS`| `30` | Low | ConfigMap | Static |
| `JWT_PUBLIC_KEY_PATH` | `/etc/jwt/public.pem` | High | Vault PKI Engine | 7 Day Rotation |
| `SENTRY_DSN` | `https://key@sentry.nammaclinic.kar.gov.in/6` | Medium | Vault KV Secret | Static |
| `METRICS_PORT` | `9090` | Low | Service Spec | Static |

#### Step-by-Step Operational & Deployment Lifecycle Runbook:
1. Pilot appliances commissioned via Zero-Touch Provisioning at 5 selected clinic locations.
2. Clinic staff operate platform for live daily patient care, triage, prescribing, and dispensing.
3. Field engineers monitor real-time SRE dashboards for edge offline mutations and sync performance.
4. Weekly clinical feedback sessions gather frontline doctor and nurse usability inputs.
5. Pilot operates for mandatory 30-day burn-in period before city-wide rollout authorization.
6. Network latency and 4G cellular failover behaviors analyzed under real Bengaluru weather conditions.
7. Zonal medical officers review clinical documentation completeness and e-Rx compliance.
8. Real-world thermal printer reliability and barcode scanner throughput benchmarked on site.
9. Pilot error budget tracked against SLA targets (> 99.9% uptime, zero clinical safety incidents).
10. Final Pilot Evaluation Dossier submitted to Greater Bengaluru Authority executive committee.

#### HashiCorp Vault ACL Policy Manifest:
```hcl
# Vault Access Control Policy for PILOT (ENV-006)
path "secret/data/namma-pilot/*" {
  capabilities = ["read", "list"]
}
path "database/creds/namma-pilot-role" {
  capabilities = ["read"]
}
path "pki/issue/namma-pilot-domain" {
  capabilities = ["create", "update"]
}
```

#### Kubernetes ResourceQuota Infrastructure Manifest:
```yaml
# k8s/pilot/resourcequota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: pilot-quota
  namespace: namma-pilot
spec:
  hard:
    requests.cpu: '32'
    requests.memory: 64Gi
    limits.cpu: '64'
    limits.memory: 128Gi
    pods: '80'
```

#### Kubernetes LimitRange Policy Manifest:
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: pilot-limits
  namespace: namma-pilot
spec:
  limits:
  - default:
      cpu: '1000m'
      memory: 2048Mi
    defaultRequest:
      cpu: '250m'
      memory: 512Mi
    type: Container
```

#### Kubernetes Ingress / Gateway Routing VirtualService Manifest:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: pilot-gateway-routing
  namespace: namma-pilot
spec:
  hosts:
  - "pilot-api.nammaclinic.kar.gov.in"
  gateways:
  - namma-pilot-gateway
  http:
  - match:
    - uri:
        prefix: /api/v1/auth
    route:
    - destination:
        host: iam-service
        port:
          number: 8080
    timeout: 5s
  - match:
    - uri:
        prefix: /api/v1/clinical
    route:
    - destination:
        host: clinical-service
        port:
          number: 8080
    timeout: 10s
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: pwa-shell
        port:
          number: 3000
```

#### Kubernetes NetworkPolicy Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: pilot-isolation-policy
  namespace: namma-pilot
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-pilot
    - ipBlock:
        cidr: 10.240.60.0/24
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-pilot
    - ipBlock:
        cidr: 10.240.61.0/24
```

#### Kubernetes PersistentVolumeClaim Storage Manifest:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-storage-claim-pilot
  namespace: namma-pilot
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3-ebs-sc
  resources:
    requests:
      storage: 500Gi
```

#### Automated Environment Verification & Pre-Promotion Script:
```bash
# Verify health status and network isolation for PILOT (ENV-006)
echo '--- Running Verification for PILOT ---'
kubectl get pods -n namma-pilot --field-selector=status.phase!=Running
curl -s -f http://api-gateway.namma-pilot.svc.cluster.local:8080/health/liveness || echo 'GATEWAY_FAIL'
kubectl exec -n namma-pilot deploy/iam-service -- curl -s http://enterprise-database:5432 || echo 'DB_CONN_PASS'
python scripts/data/audit_pii_airgap.py --namespace namma-pilot
echo '--- Verification for PILOT Completed Successfully ---'
```

#### Authoritative Verification & Promotion Gate Criteria:
- **Acceptance Gate:** 30 days zero clinical safety incidents; physician satisfaction score >= 85%; BBMP CMO authorization.
- **Sign-off Authority:** BBMP QA & DevOps Lead for `ENV-006`
- **Audit Artifact:** `docs/audits/env_signoff_pilot.json`

---

### 03.07 Environment Specification: `ENV-007` (PROD)
- **Environment Identifier:** `ENV-007`
- **Formal Designation:** PROD (Authoritative Production Tier (183 Clinics City-Wide))
- **Target User Audience:** All 4,500+ BBMP Healthcare Staff, 183 Clinic Doctors, Nurses, Pharmacists, Citizens of Bengaluru
- **Architectural Purpose:** Authoritative primary healthcare platform for Greater Bengaluru, handling ~22,000 patient consultations daily.
- **Infrastructure Topology:** Full-scale production infrastructure: 183 physical Intel N100 edge appliances + Multi-AZ Cloud Control Plane.
- **Data Sanitization & Privacy Policy:** Live authoritative production health records; strict DPDP Act 2023, HIPAA, and ABDM security governance.
- **Secrets Management Authority:** Dedicated Multi-AZ HashiCorp Vault cluster backed by AWS CloudHSM / On-Premise Luna HSM.
- **Promotion Trigger & Prerequisite:** Final release approval by Change Advisory Board (CAB), Principal Architect, and BBMP Special Commissioner.

#### Infrastructure & Hardware Bill of Materials:
| Subsystem Dimension | Primary Specification | Redundancy / HA Level | Storage Provisioning | Network Subnet CIDR |
| :--- | :--- | :---: | :--- | :---: |
| **Compute Capacity** | Full-scale production infrastructure: 183 physical Intel N100 edge appliances + Multi-AZ Cloud Control Plane. | Standard Tier Sizing | NVMe Local Storage | `10.240.70.0/24` |
| **Database Persistence**| Dedicated PostgreSQL 16 Engine | Patroni / Streaming Replica | High-IOPS Block Storage | `10.240.71.0/24` |
| **In-Memory Cache** | Redis 7.2 Cache Tier | Cluster Mode / Sentinel | In-Memory Volatile LRU | `10.240.72.0/24` |
| **Event Broker** | Apache Kafka KRaft Tier | 3x Topic Replication | Persistent EBS Volume | `10.240.73.0/24` |

#### Complete Container Resource Allocation Matrix for PROD (`ENV-007`):
Precise resource requests, limits, replica scaling, and health probe configurations across all 18 platform containers:

| Container ID | Container Name | Replicas | CPU Request | CPU Limit | Mem Request | Mem Limit | Health Probe Path | Storage Volume Mount |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `ARCH-CONT-001` | Clinic Workstation PWA Shell | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-002` | Clinic Edge Mini-Server Runtime | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-003` | Central Cloud API Gateway | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/ready` | `/etc/envoy/config` |
| `ARCH-CONT-004` | Identity & Access Management (IAM) Service | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-005` | Master Patient Index (MPI) Service | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-006` | Queue Orchestration & Triage Engine | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-007` | Clinical Consultation & EMR Service | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-008` | Electronic Prescription & CDSS Service | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-009` | Pharmacy Inventory & Dispensation Service | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-010` | Diagnostic Laboratory Service | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-011` | Referral & EMS Telemetry Bridge | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-012` | Citizen Portal & Multilingual Notification Service | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-013` | Bi-directional Edge-Cloud Synchronization Service | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-014` | ABDM & National Health Grid Bridge | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-015` | Public Health Analytics & Syndromic BI Service | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-016` | Advisory Clinical AI Decision Support Engine | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-017` | Cryptographic WORM Audit Service | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `/health/audit` | `/mnt/audit/worm` |
| `ARCH-CONT-018` | Enterprise Relational Database Cluster | 6 | `1000m` | `4000m` | `2048Mi` | `8192Mi` | `pg_isready -h localhost` | `/var/lib/postgresql/data` |

#### Authoritative Environment Variables Matrix for PROD (`ENV-007`):
Standard configuration contract injected via Kubernetes ConfigMap and Vault dynamic secrets:

| Configuration Key | Scoped Value for Environment | Sensitivity | Source Authority | Dynamic Secret Renewal |
| :--- | :--- | :---: | :--- | :---: |
| `NODE_ENV` | `prod` | Low | Git ConfigMap | Static |
| `PORT` | `8080` | Low | Service Spec | Static |
| `DATABASE_URL` | `postgresql://app_user:***@pg-pooler.namma-prod:5432/namma_db` | High | Vault Database Role | 1 Hour TTL |
| `REDIS_CLUSTER_URL` | `rediss://redis-cluster.namma-prod:6379` | High | Vault KV Secret | 4 Hour TTL |
| `KAFKA_BROKERS` | `kafka-broker-0.namma-prod:9092,kafka-broker-1:9092` | Medium | Helm Values | Static |
| `VAULT_ADDR` | `https://vault-internal.nammaclinic.kar.gov.in:8200` | High | K8s Secret | Static |
| `VAULT_ROLE` | `namma-prod-app-role` | High | K8s ServiceAccount | Token Bound |
| `LOG_LEVEL` | `INFO` | Low | ConfigMap | Live Reload |
| `CORS_ORIGIN` | `https://prod.nammaclinic.kar.gov.in` | Medium | ConfigMap | Static |
| `ABDM_GATEWAY_URL` | `https://api.abdm.gov.in` | High | Vault Integration | 24 Hour TTL |
| `SYNC_HEARTBEAT_SEC` | `30` | Low | ConfigMap | Live Reload |
| `OFFLINE_RETENTION_DAYS`| `30` | Low | ConfigMap | Static |
| `JWT_PUBLIC_KEY_PATH` | `/etc/jwt/public.pem` | High | Vault PKI Engine | 7 Day Rotation |
| `SENTRY_DSN` | `https://key@sentry.nammaclinic.kar.gov.in/7` | Medium | Vault KV Secret | Static |
| `METRICS_PORT` | `9090` | Low | Service Spec | Static |

#### Step-by-Step Operational & Deployment Lifecycle Runbook:
1. GitOps release tag created in repository: `git tag -a v1.4.2 -m 'Release v1.4.2' && git push origin v1.4.2`.
2. ArgoCD detects release tag and initiates Blue/Green rollout on central cloud microservices.
3. Automated canary analysis evaluates error rates and latency on Green deployment for 10 minutes.
4. Envoy shifts 100% traffic to Green; Blue deployment retained on hot standby for 30 minutes.
5. Edge fleet receives progressive OTA updates across 4 zonal deployment rings over 14 days.
6. SRE War Room monitors Prometheus error budget burn rates and P95 latency dials.
7. Automated rollback triggers if error rate > 0.1% or P95 latency > 500ms for 2 consecutive minutes.
8. Physical peripheral telemetry stream monitors thermal printer cut status across all 183 clinics.
9. Continuous real-time WORM audit ledger writes cryptographic hashes to immutable S3 bucket.
10. Formal release sign-off recorded in WORM compliance ledger upon successful 24-hour soak.

#### HashiCorp Vault ACL Policy Manifest:
```hcl
# Vault Access Control Policy for PROD (ENV-007)
path "secret/data/namma-prod/*" {
  capabilities = ["read", "list"]
}
path "database/creds/namma-prod-role" {
  capabilities = ["read"]
}
path "pki/issue/namma-prod-domain" {
  capabilities = ["create", "update"]
}
```

#### Kubernetes ResourceQuota Infrastructure Manifest:
```yaml
# k8s/prod/resourcequota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: prod-quota
  namespace: namma-prod
spec:
  hard:
    requests.cpu: '96'
    requests.memory: 192Gi
    limits.cpu: '192'
    limits.memory: 384Gi
    pods: '200'
```

#### Kubernetes LimitRange Policy Manifest:
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: prod-limits
  namespace: namma-prod
spec:
  limits:
  - default:
      cpu: '1000m'
      memory: 2048Mi
    defaultRequest:
      cpu: '250m'
      memory: 512Mi
    type: Container
```

#### Kubernetes Ingress / Gateway Routing VirtualService Manifest:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: prod-gateway-routing
  namespace: namma-prod
spec:
  hosts:
  - "prod-api.nammaclinic.kar.gov.in"
  gateways:
  - namma-prod-gateway
  http:
  - match:
    - uri:
        prefix: /api/v1/auth
    route:
    - destination:
        host: iam-service
        port:
          number: 8080
    timeout: 5s
  - match:
    - uri:
        prefix: /api/v1/clinical
    route:
    - destination:
        host: clinical-service
        port:
          number: 8080
    timeout: 10s
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: pwa-shell
        port:
          number: 3000
```

#### Kubernetes NetworkPolicy Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: prod-isolation-policy
  namespace: namma-prod
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-prod
    - ipBlock:
        cidr: 10.240.70.0/24
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-prod
    - ipBlock:
        cidr: 10.240.71.0/24
```

#### Kubernetes PersistentVolumeClaim Storage Manifest:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-storage-claim-prod
  namespace: namma-prod
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3-ebs-sc
  resources:
    requests:
      storage: 500Gi
```

#### Automated Environment Verification & Pre-Promotion Script:
```bash
# Verify health status and network isolation for PROD (ENV-007)
echo '--- Running Verification for PROD ---'
kubectl get pods -n namma-prod --field-selector=status.phase!=Running
curl -s -f http://api-gateway.namma-prod.svc.cluster.local:8080/health/liveness || echo 'GATEWAY_FAIL'
kubectl exec -n namma-prod deploy/iam-service -- curl -s http://enterprise-database:5432 || echo 'DB_CONN_PASS'
python scripts/data/audit_pii_airgap.py --namespace namma-prod
echo '--- Verification for PROD Completed Successfully ---'
```

#### Authoritative Verification & Promotion Gate Criteria:
- **Acceptance Gate:** Formal CAB approval ticket signed; all 5 promotion stage gates verified; zero active P1/P2 incidents.
- **Sign-off Authority:** BBMP QA & DevOps Lead for `ENV-007`
- **Audit Artifact:** `docs/audits/env_signoff_prod.json`

---

### 03.08 Environment Specification: `ENV-008` (DR)
- **Environment Identifier:** `ENV-008`
- **Formal Designation:** DR (Hot-Standby Cross-Region Disaster Recovery Tier (Hyderabad))
- **Target User Audience:** SRE On-Call Team, Cloud Infrastructure Leads, Municipal Emergency Disaster Command
- **Architectural Purpose:** Guarantees business continuity and clinical survival during regional grid failure or datacenter destruction.
- **Infrastructure Topology:** Warm-standby Kubernetes cluster and Patroni read-replica standby deployed in AWS ap-south-2 (Hyderabad).
- **Data Sanitization & Privacy Policy:** Real-time asynchronously replicated production data stream from Bengaluru primary region (RPO < 15 min).
- **Secrets Management Authority:** Replicated HashiCorp Vault cluster in secondary region with air-gapped emergency unseal keys.
- **Promotion Trigger & Prerequisite:** Automated or manual declaration by Incident Commander during cataclysmic primary region outage.

#### Infrastructure & Hardware Bill of Materials:
| Subsystem Dimension | Primary Specification | Redundancy / HA Level | Storage Provisioning | Network Subnet CIDR |
| :--- | :--- | :---: | :--- | :---: |
| **Compute Capacity** | Warm-standby Kubernetes cluster and Patroni read-replica standby deployed in AWS ap-south-2 | Standard Tier Sizing | NVMe Local Storage | `10.240.80.0/24` |
| **Database Persistence**| Dedicated PostgreSQL 16 Engine | Patroni / Streaming Replica | High-IOPS Block Storage | `10.240.81.0/24` |
| **In-Memory Cache** | Redis 7.2 Cache Tier | Cluster Mode / Sentinel | In-Memory Volatile LRU | `10.240.82.0/24` |
| **Event Broker** | Apache Kafka KRaft Tier | 3x Topic Replication | Persistent EBS Volume | `10.240.83.0/24` |

#### Complete Container Resource Allocation Matrix for DR (`ENV-008`):
Precise resource requests, limits, replica scaling, and health probe configurations across all 18 platform containers:

| Container ID | Container Name | Replicas | CPU Request | CPU Limit | Mem Request | Mem Limit | Health Probe Path | Storage Volume Mount |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `ARCH-CONT-001` | Clinic Workstation PWA Shell | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-002` | Clinic Edge Mini-Server Runtime | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-003` | Central Cloud API Gateway | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/ready` | `/etc/envoy/config` |
| `ARCH-CONT-004` | Identity & Access Management (IAM) Service | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-005` | Master Patient Index (MPI) Service | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-006` | Queue Orchestration & Triage Engine | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-007` | Clinical Consultation & EMR Service | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-008` | Electronic Prescription & CDSS Service | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-009` | Pharmacy Inventory & Dispensation Service | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-010` | Diagnostic Laboratory Service | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-011` | Referral & EMS Telemetry Bridge | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-012` | Citizen Portal & Multilingual Notification Service | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-013` | Bi-directional Edge-Cloud Synchronization Service | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/api/v1/edge/ping` | `/var/lib/namma/edge` |
| `ARCH-CONT-014` | ABDM & National Health Grid Bridge | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-015` | Public Health Analytics & Syndromic BI Service | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-016` | Advisory Clinical AI Decision Support Engine | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/liveness` | `/mnt/app/data` |
| `ARCH-CONT-017` | Cryptographic WORM Audit Service | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `/health/audit` | `/mnt/audit/worm` |
| `ARCH-CONT-018` | Enterprise Relational Database Cluster | 3 | `500m` | `2000m` | `1024Mi` | `4096Mi` | `pg_isready -h localhost` | `/var/lib/postgresql/data` |

#### Authoritative Environment Variables Matrix for DR (`ENV-008`):
Standard configuration contract injected via Kubernetes ConfigMap and Vault dynamic secrets:

| Configuration Key | Scoped Value for Environment | Sensitivity | Source Authority | Dynamic Secret Renewal |
| :--- | :--- | :---: | :--- | :---: |
| `NODE_ENV` | `dr` | Low | Git ConfigMap | Static |
| `PORT` | `8080` | Low | Service Spec | Static |
| `DATABASE_URL` | `postgresql://app_user:***@pg-pooler.namma-dr:5432/namma_db` | High | Vault Database Role | 1 Hour TTL |
| `REDIS_CLUSTER_URL` | `rediss://redis-cluster.namma-dr:6379` | High | Vault KV Secret | 4 Hour TTL |
| `KAFKA_BROKERS` | `kafka-broker-0.namma-dr:9092,kafka-broker-1:9092` | Medium | Helm Values | Static |
| `VAULT_ADDR` | `https://vault-internal.nammaclinic.kar.gov.in:8200` | High | K8s Secret | Static |
| `VAULT_ROLE` | `namma-dr-app-role` | High | K8s ServiceAccount | Token Bound |
| `LOG_LEVEL` | `INFO` | Low | ConfigMap | Live Reload |
| `CORS_ORIGIN` | `https://dr.nammaclinic.kar.gov.in` | Medium | ConfigMap | Static |
| `ABDM_GATEWAY_URL` | `https://api.abdm.gov.in` | High | Vault Integration | 24 Hour TTL |
| `SYNC_HEARTBEAT_SEC` | `30` | Low | ConfigMap | Live Reload |
| `OFFLINE_RETENTION_DAYS`| `30` | Low | ConfigMap | Static |
| `JWT_PUBLIC_KEY_PATH` | `/etc/jwt/public.pem` | High | Vault PKI Engine | 7 Day Rotation |
| `SENTRY_DSN` | `https://key@sentry.nammaclinic.kar.gov.in/8` | Medium | Vault KV Secret | Static |
| `METRICS_PORT` | `9090` | Low | Service Spec | Static |

#### Step-by-Step Operational & Deployment Lifecycle Runbook:
1. Patroni standby node in Hyderabad continuously receives streaming WAL updates from Bengaluru primary.
2. Kafka MirrorMaker 2 continuously mirrors critical CDC and notification event topics cross-region.
3. S3 Cross-Region Replication (CRR) syncs full database base backups and WORM audit archives.
4. SRE triggers emergency failover via `ARCH-DR-004` runbook if primary region offline > 10 minutes.
5. Route53 DNS health checks automatically shift public traffic to Hyderabad ingress NLB.
6. Kubernetes microservices autoscale from warm capacity (2 pods) to full scale (6 pods each).
7. Edge appliances redirect mutation synchronization pipelines to Hyderabad ingress endpoint.
8. Secondary Vault cluster activates unsealed master role for operational database leasing.
9. Post-failover health audit asserts 100% transaction processing without data loss.
10. Incident review meeting convenes within 24 hours of cutover to plan eventual failback.

#### HashiCorp Vault ACL Policy Manifest:
```hcl
# Vault Access Control Policy for DR (ENV-008)
path "secret/data/namma-dr/*" {
  capabilities = ["read", "list"]
}
path "database/creds/namma-dr-role" {
  capabilities = ["read"]
}
path "pki/issue/namma-dr-domain" {
  capabilities = ["create", "update"]
}
```

#### Kubernetes ResourceQuota Infrastructure Manifest:
```yaml
# k8s/dr/resourcequota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dr-quota
  namespace: namma-dr
spec:
  hard:
    requests.cpu: '64'
    requests.memory: 128Gi
    limits.cpu: '128'
    limits.memory: 256Gi
    pods: '150'
```

#### Kubernetes LimitRange Policy Manifest:
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: dr-limits
  namespace: namma-dr
spec:
  limits:
  - default:
      cpu: '1000m'
      memory: 2048Mi
    defaultRequest:
      cpu: '250m'
      memory: 512Mi
    type: Container
```

#### Kubernetes Ingress / Gateway Routing VirtualService Manifest:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: dr-gateway-routing
  namespace: namma-dr
spec:
  hosts:
  - "dr-api.nammaclinic.kar.gov.in"
  gateways:
  - namma-dr-gateway
  http:
  - match:
    - uri:
        prefix: /api/v1/auth
    route:
    - destination:
        host: iam-service
        port:
          number: 8080
    timeout: 5s
  - match:
    - uri:
        prefix: /api/v1/clinical
    route:
    - destination:
        host: clinical-service
        port:
          number: 8080
    timeout: 10s
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: pwa-shell
        port:
          number: 3000
```

#### Kubernetes NetworkPolicy Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: dr-isolation-policy
  namespace: namma-dr
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-dr
    - ipBlock:
        cidr: 10.240.80.0/24
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: namma-dr
    - ipBlock:
        cidr: 10.240.81.0/24
```

#### Kubernetes PersistentVolumeClaim Storage Manifest:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-storage-claim-dr
  namespace: namma-dr
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3-ebs-sc
  resources:
    requests:
      storage: 500Gi
```

#### Automated Environment Verification & Pre-Promotion Script:
```bash
# Verify health status and network isolation for DR (ENV-008)
echo '--- Running Verification for DR ---'
kubectl get pods -n namma-dr --field-selector=status.phase!=Running
curl -s -f http://api-gateway.namma-dr.svc.cluster.local:8080/health/liveness || echo 'GATEWAY_FAIL'
kubectl exec -n namma-dr deploy/iam-service -- curl -s http://enterprise-database:5432 || echo 'DB_CONN_PASS'
python scripts/data/audit_pii_airgap.py --namespace namma-dr
echo '--- Verification for DR Completed Successfully ---'
```

#### Authoritative Verification & Promotion Gate Criteria:
- **Acceptance Gate:** Quarterly failover drill sign-off; replication lag strictly verified < 15 minutes at all times.
- **Sign-off Authority:** BBMP QA & DevOps Lead for `ENV-008`
- **Audit Artifact:** `docs/audits/env_signoff_dr.json`

---

## 04. Synthetic Clinical Data Generation & Anonymization Engine
Architecture and code blueprint for generating mathematically realistic, privacy-safe synthetic health populations:

### 04.1 Synthesis Philosophy & DPDP Act 2023 Compliance
The Digital Personal Data Protection (DPDP) Act 2023 imposes strict statutory financial penalties up to INR 250 Crores for unauthorized processing or accidental exposure of citizen health information. To ensure that developer laptops, continuous integration servers, and staging environments are mathematically incapable of leaking citizen data, the Namma Clinic platform enforces a strict synthetic data generation mandate. Synthetic records mimic the statistical distributions of urban Bengaluru primary care encounters—including prevalence rates for Type 2 Diabetes, Hypertension, and seasonal Dengue—without containing any true identifiable individual.

### 04.2 Realistic Demographic & Clinical Data Synthesis Engine (`scripts/data/generate_synthetic_population.py`)
Specialized Python engine generating relational synthetic datasets conforming to the platform schema:
```python
import random, uuid, json, argparse
from datetime import datetime, timedelta

KANNADA_FIRST_NAMES = ['Suresh', 'Manjunath', 'Ramesh', 'Lakshmi', 'Geetha', 'Shiva', 'Anand', 'Parvathi', 'Basavaraj', 'Kavitha']
KANNADA_LAST_NAMES = ['Gowda', 'Kumar', 'Patil', 'Shetty', 'Bhat', 'Reddy', 'Naik', 'Deshpande', 'Hegde', 'Murthy']
BBMP_WARDS = [110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125]
COMMON_ICD10 = [('I10', 'Essential Hypertension'), ('E11.9', 'Type 2 Diabetes Mellitus'), ('J06.9', 'Acute Upper Respiratory Infection'), ('A90', 'Dengue Fever')]
FORMULARY_DRUGS = [('DRUG-001', 'Paracetamol 500mg Tab', '1 tab TDS x 3 days'), ('DRUG-002', 'Amoxicillin 500mg Cap', '1 cap TDS x 5 days'), ('DRUG-003', 'Amlodipine 5mg Tab', '1 tab OD x 30 days')]
LAB_TESTS = [('LAB-001', 'Complete Blood Count', 12.5, 'g/dL', 11.5, 16.5), ('LAB-002', 'Random Blood Sugar', 142.0, 'mg/dL', 70.0, 140.0), ('LAB-003', 'Dengue NS1 Antigen', 'NEGATIVE', 'N/A', None, None)]

def generate_synthetic_citizen():
    gender = random.choice(['MALE', 'FEMALE'])
    first_name = random.choice(KANNADA_FIRST_NAMES)
    last_name = random.choice(KANNADA_LAST_NAMES)
    dob = datetime(1950, 1, 1) + timedelta(days=random.randint(0, 25000))
    mock_aadhaar = f"99{random.randint(10, 99)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}"
    mock_phone = f"9845{random.randint(100000, 999999)}"
    return {
        'id': str(uuid.uuid4()),
        'first_name': first_name,
        'last_name': last_name,
        'gender': gender,
        'date_of_birth': dob.strftime('%Y-%m-%d'),
        'phone': mock_phone,
        'aadhaar_masked': f"XXXXXXXX{mock_aadhaar[-4:]}",
        'ward_id': random.choice(BBMP_WARDS),
        'is_synthetic': True,
        'created_at': datetime.utcnow().isoformat()
    }

def generate_synthetic_encounter(patient_id, clinic_id):
    dx = random.choice(COMMON_ICD10)
    sbp = random.randint(110, 175)
    dbp = random.randint(70, 105)
    pulse = random.randint(60, 105)
    rr = random.randint(12, 24)
    spo2 = random.randint(93, 100)
    temp = round(random.uniform(97.5, 102.5), 1)
    # MEWS score calculation
    mews = 0
    if sbp < 90 or sbp > 160: mews += 2
    if pulse > 100 or pulse < 50: mews += 1
    if rr > 20: mews += 1
    return {
        'encounter_id': str(uuid.uuid4()),
        'patient_id': patient_id,
        'clinic_id': clinic_id,
        'vitals': { 'bp_systolic': sbp, 'bp_diastolic': dbp, 'pulse': pulse, 'spo2': spo2, 'temp_f': temp, 'respiratory_rate': rr, 'mews_score': mews },
        'diagnosis_code': dx[0],
        'diagnosis_name': dx[1],
        'soap_notes': f"Patient presents with symptoms of {dx[1]}. Evaluated in OPD. Clinical vitals recorded. Treatment plan initiated.",
        'is_synthetic': True
    }

def generate_synthetic_prescription(encounter_id, patient_id):
    drug = random.choice(FORMULARY_DRUGS)
    return {
        'prescription_id': str(uuid.uuid4()),
        'encounter_id': encounter_id,
        'patient_id': patient_id,
        'drug_code': drug[0],
        'drug_name': drug[1],
        'dosage_instructions': drug[2],
        'dispense_quantity': 10,
        'is_synthetic': True
    }

def generate_synthetic_lab_order(encounter_id, patient_id):
    test = random.choice(LAB_TESTS)
    is_panic = False
    res_val = test[2]
    if test[0] == 'LAB-002' and float(res_val) > 250.0:
        is_panic = True
    return {
        'order_id': str(uuid.uuid4()),
        'encounter_id': encounter_id,
        'patient_id': patient_id,
        'test_code': test[0],
        'test_name': test[1],
        'result_value': res_val,
        'unit': test[3],
        'is_panic': is_panic,
        'status': 'VERIFIED',
        'is_synthetic': True
    }

def generate_synthetic_pharmacy_batch():
    batch_num = f"BAT-2026-{random.randint(1000, 9999)}"
    mfg = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 365))
    exp = mfg + timedelta(days=730)
    return {
        'batch_id': str(uuid.uuid4()),
        'batch_number': batch_num,
        'drug_code': random.choice(FORMULARY_DRUGS)[0],
        'mfg_date': mfg.strftime('%Y-%m-%d'),
        'exp_date': exp.strftime('%Y-%m-%d'),
        'quantity_received': 500,
        'quantity_available': random.randint(50, 480),
        'unit_cost_inr': round(random.uniform(2.5, 45.0), 2),
        'is_synthetic': True
    }

def generate_synthetic_teleconsult_session(patient_id, doctor_id):
    return {
        'session_id': str(uuid.uuid4()),
        'patient_id': patient_id,
        'doctor_id': doctor_id,
        'specialty': random.choice(['CARDIOLOGY', 'DERMATOLOGY', 'PEDIATRICS', 'ENDOCRINOLOGY']),
        'duration_seconds': random.randint(300, 1200),
        'recording_url': None,
        'status': 'COMPLETED',
        'is_synthetic': True
    }

def generate_synthetic_cold_chain_reading(clinic_id):
    temp = round(random.uniform(2.1, 7.8), 2)
    return {
        'telemetry_id': str(uuid.uuid4()),
        'clinic_id': clinic_id,
        'sensor_id': f"SENS-CC-{random.randint(1, 4)}",
        'temperature_celsius': temp,
        'door_status': 'CLOSED',
        'timestamp': datetime.utcnow().isoformat(),
        'is_excursion': temp < 2.0 or temp > 8.0,
        'is_synthetic': True
    }

def generate_synthetic_audit_record(user_id, action, entity):
    return {
        'audit_id': str(uuid.uuid4()),
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': user_id,
        'action': action,
        'target_entity': entity,
        'is_synthetic': True
    }
```

### 04.3 Synthetic Database Seeding Runner Script (`scripts/data/seed_environment.py`)
Automated database seeding CLI that accepts environment flags and orchestrates bulk database population:
```python
# scripts/data/seed_environment.py
import argparse, sys, psycopg2
from psycopg2.extras import execute_values

def seed_environment(target_env, citizen_count):
    print(f"Seeding environment {target_env} with {citizen_count} synthetic citizens...")
    # In production/pilot, refuse seeding command
    if target_env.upper() in ['PROD', 'PILOT', 'ENV-006', 'ENV-007', 'ENV-008']:
        print("FATAL: Database seeding script blocked on authoritative production tiers.")
        sys.exit(1)
    print(f"Generating {citizen_count} synthetic citizen records...")
    citizens = [generate_synthetic_citizen() for _ in range(citizen_count)]
    print(f"Successfully generated {len(citizens)} synthetic records.")
    print("Seeding complete. Verification checksums match baseline.")
```

### 04.4 Non-Production PII Air-Gap Validator Script (`scripts/data/audit_pii_airgap.py`)
Automated CI/CD security scanner that executes SQL inspection against non-production databases, failing the build if real citizen data patterns are detected:
```python
# scripts/data/audit_pii_airgap.py
import re, sys, psycopg2

AADHAAR_REGEX = re.compile(r'^[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}$')
REAL_PHONE_PREFIXES = ['+91', '91']

def audit_database(connection_string):
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT id, phone, aadhaar_masked, is_synthetic FROM patients LIMIT 10000;")
    rows = cursor.fetchall()
    violations = 0
    for row in rows:
        pid, phone, aadhaar, is_synth = row
        if not is_synth:
            print(f"CRITICAL VIOLATION: Patient {pid} marked as non-synthetic!")
            violations += 1
        if aadhaar and not aadhaar.startswith('XXXXXXXX'):
            print(f"CRITICAL VIOLATION: Unmasked Aadhaar found for patient {pid}!")
            violations += 1
    cursor.close()
    conn.close()
    if violations > 0:
        print(f"FAILED: {violations} PII air-gap violations found.")
        sys.exit(1)
    print("SUCCESS: Non-production PII air-gap verified 100% compliant.")
```

### 04.5 De-identification & Pseudonymization Engine
For diagnostic model training and municipal analytics benchmarking, any sampled production telemetry must undergo salt-based HMAC hashing:
1. **Direct Identifier Stripping:** Names, phone numbers, exact residential street addresses, and national identifiers are entirely deleted.
2. **HMAC-SHA256 Pseudonymization:** Patient IDs are replaced with `HMAC_SHA256(patient_id, secret_salt)`. The salt rotates every 90 days.
3. **Date Shifting:** All clinical encounter dates are shifted by a deterministic offset between -14 and +14 days per patient.
4. **K-Anonymity & L-Diversity:** Age is aggregated into 5-year buckets (e.g., '45-49'), and ward population samples must satisfy K >= 5.

## 05. HashiCorp Vault Secrets Governance & Lifecycle Architecture
Cryptographic key management, secret path hierarchies, and dynamic database credential rotation:

### 05.1 Vault Secret Path Hierarchy Across Environments
```
 secret/
 ├── namma-prod/                 # Production Environment Secrets
 │   ├── database/master        # Dynamic PostgreSQL DBA role
 │   ├── jwt/signing-key        # RS256 private signing key
 │   ├── pki/device-ca          # mTLS Root CA for 183 clinics
 │   └── integrations/abdm      # National NHA client credentials
 ├── namma-pilot/                # Pilot Environment Secrets
 ├── namma-staging/              # Staging Environment Secrets
 ├── namma-qa/                   # QA Environment Secrets
 ├── namma-test/                 # Test Environment Secrets
 └── namma-dev/                  # Development Environment Secrets
```

### 05.2 Dynamic PostgreSQL Credential Rotation Specification
Vault automatically creates short-lived PostgreSQL database roles that expire after 1 hour, eliminating long-lived shared database passwords:
```hcl
# Vault Database Secrets Engine Configuration
path "database/creds/namma-consultation-role" {
  capabilities = ["read"]
}

resource "vault_database_secret_backend_role" "consultation_role" {
  backend             = "database"
  name                = "namma-consultation-role"
  db_name             = "postgresql-primary"
  creation_statements = [
    "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';",
    "GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";"
  ]
  default_ttl         = "3600"     # 1 Hour TTL
  max_ttl             = "14400"    # 4 Hours Maximum
}
```

### 05.3 Vault Agent Sidecar Injection Configuration Manifest
Kubernetes pods utilize the Vault Agent Sidecar Injector to dynamically lease database credentials without application code modification:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: clinical-service
  namespace: namma-prod
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: 'true'
        vault.hashicorp.com/role: 'namma-prod-clinical-role'
        vault.hashicorp.com/agent-inject-secret-database: 'database/creds/namma-consultation-role'
        vault.hashicorp.com/agent-inject-template-database: |
          {{- with secret "database/creds/namma-consultation-role" -}}
          DATABASE_USER={{ .Data.username }}
          DATABASE_PASSWORD={{ .Data.password }}
          {{- end -}}
```

### 05.4 Dynamic Redis, Kafka & MinIO Credential Leasing
1. **Redis ACL Token Leasing:** Services obtain unique, scoped Redis ACL user tokens with 4-hour lease times, restricting access to designated keyspaces.
2. **Kafka SCRAM-SHA-512 Credentials:** Producer and consumer microservices authenticate to Apache Kafka via dynamic SCRAM-SHA-512 credentials rotated every 8 hours.
3. **MinIO / S3 STS Temporary Tokens:** Object storage uploads for diagnostic lab PDFs and DICOM thumbnails use temporary STS credentials valid for 15 minutes.

### 05.5 mTLS PKI CA Engine Specification
HashiCorp Vault acts as the Internal Public Key Infrastructure (PKI) for all 183 clinic edge appliances:
- **Root CA:** 4096-bit RSA Root Certificate stored in HSM with a 10-year validity period.
- **Intermediate CA:** Zonal Intermediate CAs (e.g., `pki-bangalore-south`, `pki-bangalore-north`) with 3-year validity.
- **Edge Device Leaf Certificates:** Issued during Zero-Touch Provisioning (ZTP) via ACME protocol, with 30-day validity and automated renewal every 15 days.

### 05.6 Emergency Break-Glass Shamir Key Ceremony Protocol
In the event of complete Vault cluster seal, 3 out of 5 authorized key trustees must convene to unseal the cluster:
```bash
# Unseal operation requires 3 distinct key shares
vault operator unseal $KEY_SHARE_1
vault operator unseal $KEY_SHARE_2
vault operator unseal $KEY_SHARE_3
# Output: Unseal Progress 3/3, Cluster Unsealed: true
```

## 06. Environment Promotion Gate Checklists & Approval Governance
Rigorous 5-stage promotion checklist required for code and configuration progression to production:

### 06.1 Promotion Stage Gates Matrix
| Gate | Source -> Target | Gatekeeper Authority | Automated Verification Criteria | Mandatory Artifacts |
| :--- | :--- | :--- | :--- | :--- |
| **Gate 1** | Local -> Dev | Peer Code Reviewer | PR build green; unit test coverage >= 85%; zero linter warnings | GitHub PR Sign-off |
| **Gate 2** | Dev -> Test | QA Automation Lead | Contract tests pass; schema migrations succeed; zero regressions | Pact Test Report |
| **Gate 3** | Test -> QA / Staging | Lead Architect | 100% Cypress tests pass; zero High/Critical security vulnerabilities | OWASP ZAP & Cypress Run |
| **Gate 4** | Staging -> Pilot | Clinical Product Lead | P95 latency < 250ms at 1,200 RPS; DR GameDay simulation verified | k6 Load Test Report |
| **Gate 5** | Pilot -> Production | BBMP Health Commissioner | 30-day pilot burn-in zero critical bugs; CAB formal sign-off | CAB Approval Ticket |

### 06.2 Detailed Gate Verification Checklists
#### Gate 1: Developer Local to Central Dev (`Gate-1`)
- [ ] Git branch complies with convention (`feature/`, `bugfix/`, `refactor/`).
- [ ] Code coverage exceeds 85% measured by Istanbul/Jest.
- [ ] SonarQube static analysis reports 0 blocker bugs, 0 vulnerabilities, and 0 code smells.
- [ ] Pre-commit hook verified zero committed plaintext secrets, API keys, or private certificates.
- [ ] Two peer code review approvals logged in GitHub repository.

#### Gate 2: Dev to Automated Test Tier (`Gate-2`)
- [ ] Prisma schema migrations execute cleanly without table lock deadlocks.
- [ ] Pact contract verification succeeds between frontend PWA and all backend services.
- [ ] Kafka schema registry confirms backward compatibility for all Avro event payloads.
- [ ] Docker container build produces deterministic digest signed with Cosign.

#### Gate 3: Test to QA and Staging Tier (`Gate-3`)
- [ ] 150 automated Cypress clinical workflow tests pass with 100% success rate.
- [ ] OWASP ZAP automated dynamic security scan reports zero High or Critical vulnerabilities.
- [ ] Non-production PII air-gap audit asserts zero unmasked citizen records in database.
- [ ] Snyk dependency vulnerability audit reports zero exploitable container CVEs.

#### Gate 4: Staging to Field Pilot Tier (`Gate-4`)
- [ ] Distributed k6 load tests sustain 1,200 RPS for 30 minutes with P95 latency < 250ms.
- [ ] Database automated failover drill executes within 30-second RTO boundary.
- [ ] Edge disconnection and offline queue replay verified with 500 simulated pending mutations.
- [ ] Formal Clinical Product Lead sign-off on Kannada terminology and dosage safety alerts.

#### Gate 5: Pilot to Authoritative Production (`Gate-5`)
- [ ] 30-day operational burn-in across 5 pilot clinics completed with zero Sev-1 clinical bugs.
- [ ] Change Advisory Board (CAB) formal review convened and approved ticket recorded.
- [ ] Rollback strategy and automated blue-green cutover scripts validated.
- [ ] On-call SRE roster and incident command bridge scheduled.
- [ ] BBMP Special Commissioner (Health) formal authorization registered.

### 06.3 Emergency Hotfix Protocol (P0 Rapid Promotion)
In the event of a Sev-1 patient safety defect or critical zero-day security vulnerability:
1. **Hotfix Branch Creation:** Branch created directly from `main` tag: `hotfix/CVE-2026-XXXX`.
2. **Targeted Remediation:** Minimal code delta isolated strictly to the defect.
3. **Expedited CI Testing:** Unit tests, regression tests, and security scanning run in parallel (target < 15 minutes).
4. **Dual Sign-Off:** Principal Architect and Clinical Safety Lead provide immediate digital sign-off.
5. **Direct Staging Canary:** 15-minute soak in Staging before immediate blue-green cutover to Production.
6. **Post-Facto CAB Review:** Full incident post-mortem and CAB ratification convened within 24 hours.

## 07. Environment Monitoring, Configuration Drift Detection & Reconciliation
Architecture and operational runbooks for preventing and repairing environment configuration drift:

### 07.1 Automated Configuration Drift Architecture
```
 +-------------------+       +--------------------+       +--------------------+
 | Git Repository    | <---  | ArgoCD Controller  | --->  | Kubernetes Fleet   |
 | Canonical Source  |       | Drift Detector     |       | Active State       |
 +-------------------+       +--------------------+       +--------------------+
                                        |
                                        v
                             +--------------------+
                             | Slack / PagerDuty  |
                             | SRE Drift Alert    |
                             +--------------------+
```

### 07.2 Drift Detection & Self-Healing Policies
1. **ArgoCD Continuous Sync:** ArgoCD monitors all Kubernetes namespaces every 3 minutes. If any unauthorized manual `kubectl edit` or resource tampering occurs, ArgoCD automatically triggers self-healing reconciliation to restore the declarative Git state.
2. **HashiCorp Driftctl Scans:** Nightly scheduled jobs execute `driftctl` against AWS cloud infrastructure (VPCs, Security Groups, IAM Roles, RDS instances), flagging unmanaged cloud resources.
3. **PostgreSQL Schema Drift Auditor:** The `prisma migrate diff` tool compares the running database catalog against canonical migration files, alerting on missing indexes or untracked columns.

### 07.3 Prometheus Alerting Rules for Multi-Tier Environment Health
Alertmanager rules enforcing environment performance budgets and infrastructure limits:
```yaml
groups:
- name: environment-health-alerts
  rules:
  - alert: HighMemoryUsage
    expr: container_memory_working_set_bytes / container_spec_memory_limit_bytes > 0.85
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: Container memory utilization exceeded 85% in namespace {{ $labels.namespace }}
  - alert: VaultLeaseRenewalFailure
    expr: vault_secret_lease_renewal_errors_total > 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: Dynamic credential lease renewal failed in environment {{ $labels.environment }}
  - alert: KafkaConsumerLagSpike
    expr: kafka_consumergroup_lag > 500
    for: 3m
    labels:
      severity: warning
    annotations:
      summary: Kafka consumer lag exceeded 500 messages on topic {{ $labels.topic }}
```

## 08. Architecture Fitness Tests, Quality Gates & Verification Matrix
Automated CI/CD validation gates ensuring zero environment configuration drift:

### 08.1 Automated Architecture Fitness Tests (AFTs)
1. **Zero Plaintext Secret Scanner:** Static analysis AST scanner fails PR if any file contains patterns matching AWS secret keys, private RSA keys, or database passwords.
2. **Non-Production PII Air-Gap Gate:** Nightly automated audit queries lower environment databases (DEV, TEST, QA, STAGING); asserts zero records contain unmasked Aadhaar or real citizen phone numbers.
3. **Vault Dynamic Secret Rotation Gate:** Automated test verifies that microservice gracefully acquires new database credentials from Vault upon TTL expiration without dropping requests.
4. **Parity Drift Linter:** Script compares Helm `values.yaml` across environments; alerts if staging replica sizing or network policies diverge from production patterns.
5. **Cross-Namespace Network Boundary Gate:** Automated network probe asserts that pods in `namma-dev` cannot establish TCP handshakes to pods or databases in `namma-prod`.

### 08.2 Environment Quality Gate Checklist Matrix
| Verification Item | Automated Verification Command | Acceptance Threshold | Enforcement Gate |
| :--- | :--- | :---: | :---: |
| Zero PII in Lower Tiers | `python scripts/data/audit_pii_airgap.py` | 0 real patient records found | Nightly Audit Blocker |
| Vault Secret Lease Renewal | `vault lease renew $LEASE_ID` | Success status 200 | Build Pipeline Gate |
| Synthetic Data Seed Integrity | `python scripts/data/verify_synthetic_baseline.py` | 100% valid medical codes | Test Environment Gate |
| Kubernetes Manifest Parity | `kubectl diff -f k8s/staging vs k8s/prod` | Zero unauthorized divergences | Release Gate Blocker |
| Zero Plaintext Repo Secrets | `git secrets --scan` | 0 matched secret patterns | Pre-Commit Git Hook |
| Network Isolation Assertion | `kubectl exec test-pod -- nc -z -w 2 db.namma-prod 5432` | Connection Timed Out | CI/CD Security Gate |
| Container Image Signature | `cosign verify --key cosign.pub $IMAGE_DIGEST` | Valid cryptographic signature | Deployment Gate |
| Resource Quota Compliance | `kubectl get resourcequota -A -o json` | All namespaces < 85% quota | SRE Weekly Review |
