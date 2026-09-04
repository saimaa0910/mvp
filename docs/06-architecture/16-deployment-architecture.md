# 🚀 Architecture Document 16: Enterprise Hybrid Cloud-Edge Deployment Architecture, Infrastructure Topology & Zero-Downtime Release Engineering
## Namma Clinic Digital Health & Operations Platform
### Greater Bengaluru Authority (GBA) / BBMP Health Department
**Standard:** CIS Benchmarks / GitOps ArgoCD / Kubernetes / Edge ZTP | **Status:** APPROVED BASELINE | **Code:** `ARCH-DEPLOY-16`

---

## 01. Document Overview & Deployment Engineering Philosophy
This document specifies the enterprise hybrid cloud-edge deployment architecture, physical hardware topology, operating system hardening, Kubernetes orchestration, and zero-downtime release engineering pipelines for the Namma Clinic Digital Health & Operations Platform. Spanning 183 physical primary health clinics across Greater Bengaluru and a multi-zone cloud control plane, the deployment infrastructure is engineered for zero-touch provisioning (ZTP), extreme edge physical resilience, automated cryptographic attestation, and continuous GitOps delivery.

### 01.1 Core Deployment Invariants & Architectural Invariants
1. **Immutable Infrastructure Principle:** Edge appliance operating system images and cloud container images are built and tested as immutable artifacts. Configuration is injected strictly via environment secrets from HashiCorp Vault; zero manual SSH configuration in production.
2. **Hardware Root of Trust & TPM 2.0 Attestation:** Every physical clinic edge appliance authenticates to the cloud control plane using an embedded Hardware Security Module / Trusted Platform Module (TPM 2.0) chip and device-specific X.509 client certificates.
3. **Zero-Touch Provisioning (ZTP):** Edge appliances boot directly from pre-seeded factory images; upon network connection, appliances autonomously enroll with the central device registry, download encrypted tenant slices, and begin local operations in < 15 minutes.
4. **Zero-Downtime Blue/Green Cloud Upgrades:** Cloud microservices execute production releases using Blue/Green deployment models with automated canary verification; zero dropped HTTP connections or database lock stalls.
5. **Strict Air-Gapped Zonal Canary Rollouts:** Edge fleet software updates are deployed progressively in 4 distinct rollout rings (Canary 5 clinics -> Zone South 25 clinics -> City-wide 183 clinics) over a 14-day bake period.

## 02. Hybrid Cloud-Edge Physical & Logical Topology
Comprehensive physical and logical topology mapping edge clinics to central cloud control plane:
```
 +-----------------------------------------------------------------------------------------------------------------+
 |                                   CENTRAL CLOUD CONTROL PLANE (AWS ap-south-1 / NIC)                            |
 |  +---------------------------------+     +----------------------------------+     +--------------------------+  |
 |  | Ingress Network Load Balancer   | --> | Kubernetes Ingress Controller    | --> | Microservice Pod Tier    |  |
 |  | (Multi-AZ Layer 4 NLB)          |     | (Envoy / Kong API Gateway Pods)  |     | (HPA 96 Stateless Pods)  |  |
 |  +---------------------------------+     +----------------------------------+     +--------------------------+  |
 |                    |                                       |                                    |               |
 |                    v                                       v                                    v               |
 |  +---------------------------------+     +----------------------------------+     +--------------------------+  |
 |  | Patroni PostgreSQL Cluster      |     | Apache Kafka 5-Broker Cluster    |     | Redis 6-Node Cluster     |  |
 |  | (AZ-1 Primary, AZ-2 Sync Standby|     | (KRaft Consensus / NVMe Storage) |     | (3 Masters, 3 Replicas)  |  |
 |  +---------------------------------+     +----------------------------------+     +--------------------------+  |
 +-----------------------------------------------------------------------------------------------------------------+
                                       ^                                            ^
                    mTLS Zstandard Sync|                         mTLS Telemetry Push|
                                       v                                            v
 +-----------------------------------------------------------------------------------------------------------------+
 |                                  NAMMA CLINIC PHYSICAL EDGE DEPLOYMENT (x183)                                   |
 |                                                                                                                 |
 |    +----------------------------------+          +----------------------------------+                           |
 |    | Clinic LAN Switch (PoE+ Managed) | -------> | Intel N100 Edge Mini-Server Box  |                           |
 |    | (Cisco CBS250-8P-E-2G Gigabit)   |          | (Ubuntu 24.04 CIS / Docker / PWA)|                           |
 |    +----------------------------------+          +----------------------------------+                           |
 |        |                 |                                   |                    |                             |
 |        v                 v                                   v                    v                             |
 |  +------------+   +---------------+                   +---------------+    +---------------+                    |
 |  | Workstation|   | Thermal Slip  |                   | APC Smart-UPS |    | 4G/5G LTE     |                    |
 |  | Tablet PCs |   | Receipt Print |                   | 1200VA USB    |    | Failover eSIM |                    |
 |  +------------+   +---------------+                   +---------------+    +---------------+                    |
 +-----------------------------------------------------------------------------------------------------------------+
```

## 03. 12 Canonical Deployment Topologies (ARCH-DEPLOY-001 to ARCH-DEPLOY-012)
Exhaustive technical blueprints and configuration manifests for the 12 canonical deployment topologies:

### 03.01 Topology Specification: `ARCH-DEPLOY-001` (Cloud Kubernetes Multi-AZ Control Plane Deployment)
- **Topology Identifier:** `ARCH-DEPLOY-001`
- **Implementation Technology:** AWS EKS / K8s 1.30+ Multi-AZ Managed Cluster
- **Deployment Tier:** Primary Control Plane Tier
- **Geographic & Architectural Scope:** 3 AZs (ap-south-1a, ap-south-1b, ap-south-1c)
- **Operational Purpose:** Cloud platform microservices, ingress gateways, and background queue workers.
- **Deployment & Scaling Strategy:** Deploy 3 control plane nodes and 12 worker nodes (m6i.2xlarge, 8 vCPU, 32GB RAM) spread equally across 3 AZs.
- **Architectural Resilience Outcome:** Guarantees 99.99% cloud platform availability; survives the complete loss of any single AWS availability zone.

#### Step-by-Step Deployment & Commissioning Procedure:
1. Terraform provisions VPC across 3 AZs with 6 subnets (3 public, 3 private).
2. EKS cluster deployed with managed node groups using Karpenter auto-provisioner.
3. Calico CNI enforces strict Kubernetes NetworkPolicies between microservice namespaces.
4. CoreDNS autoscales with cluster size to ensure sub-millisecond cluster-internal DNS resolution.
5. AWS EBS CSI driver manages persistent volume claims backed by `gp3` NVMe storage.

#### Network Architecture & Port Allocation Matrix:
| Interface / Protocol | Inbound Port | Outbound Destination | Encryption Standard | Network Security Boundary |
| :--- | :---: | :--- | :---: | :--- |
| **Client HTTPS** | 8443 / TCP | API Gateway Service | TLS 1.3 / mTLS | Ingress Boundary WAF Protected |
| **Internal gRPC** | 50051 / TCP | Backend Microservice Tier | Internal mTLS (SPIFFE/SPIRE) | Calico Encrypted Pod Mesh |
| **Telemetry OTLP** | 4317 / gRPC | OpenTelemetry Collector | mTLS Token Auth | Monitoring Private Subnet |

#### Kubernetes NetworkPolicy Security Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cloud-kubernetes-multi-az-control-plane-deployment-netpol
  namespace: namma-prod
spec:
  podSelector:
    matchLabels:
      app: cloud-kubernetes-multi-az-control-plane-deployment
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: envoy-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: pgbouncer
    ports:
    - protocol: TCP
      port: 6432
```

#### Terraform / OpenTofu Infrastructure-as-Code Manifest:
```hcl
# Terraform security and subnet routing definition for ARCH-DEPLOY-001
resource "aws_security_group" "arch_deploy_001_sg" {
  name        = "namma-arch-deploy-001-sg"
  description = "Security group controlling traffic for Cloud Kubernetes Multi-AZ Control Plane Deployment"
  vpc_id      = var.vpc_id

  ingress {
    description = "Internal microservice traffic for ARCH-DEPLOY-001"
    from_port   = 8080
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Outbound dependency egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = "production"
    Topology    = "ARCH-DEPLOY-001"
    ManagedBy   = "terraform"
  }
}
```

#### Self-Healing & Automated Recovery Mechanism:
If container or host failure occurs under `ARCH-DEPLOY-001`, Kubernetes liveness probes detect failure within 30 seconds, automatically evicting the damaged pod and rescheduling on an alternate healthy node across remaining availability zones.

---

### 03.02 Topology Specification: `ARCH-DEPLOY-002` (Cloud Edge Ingress NLB & TLS Termination Topology)
- **Topology Identifier:** `ARCH-DEPLOY-002`
- **Implementation Technology:** AWS Network Load Balancer (NLB) Layer 4 + Envoy Proxy Ingress Tier
- **Deployment Tier:** Cloud Edge Ingress Boundary
- **Geographic & Architectural Scope:** Cross-Zone Active-Active NLB Endpoints
- **Operational Purpose:** TLS termination, DDoS mitigation, mTLS device authentication, and traffic routing.
- **Deployment & Scaling Strategy:** Deploy Layer 4 NLB routing TCP traffic directly to host-networked Envoy pods. NLB preserves client source IP.
- **Architectural Resilience Outcome:** Sustains 50,000 concurrent TCP connections and 1,200 req/sec with TLS handshake latency < 8ms.

#### Step-by-Step Deployment & Commissioning Procedure:
1. AWS NLB provisioned with Elastic IPs across all 3 availability zones.
2. NLB health checks probe `/health/live` on port 8080 of Envoy proxy pods.
3. Envoy terminates TLS 1.3 using ACM wildcard certificate `*.nammahealth.bbmp.gov.in`.
4. Envoy inspects client certificates on `/api/v1/sync/*` using BBMP Device Root CA trust store.
5. Unauthenticated public traffic routed through AWS WAF rate-limiting rules.

#### Network Architecture & Port Allocation Matrix:
| Interface / Protocol | Inbound Port | Outbound Destination | Encryption Standard | Network Security Boundary |
| :--- | :---: | :--- | :---: | :--- |
| **Client HTTPS** | 8443 / TCP | API Gateway Service | TLS 1.3 / mTLS | Ingress Boundary WAF Protected |
| **Internal gRPC** | 50051 / TCP | Backend Microservice Tier | Internal mTLS (SPIFFE/SPIRE) | Calico Encrypted Pod Mesh |
| **Telemetry OTLP** | 4317 / gRPC | OpenTelemetry Collector | mTLS Token Auth | Monitoring Private Subnet |

#### Kubernetes NetworkPolicy Security Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cloud-edge-ingress-nlb-and-tls-termination-topology-netpol
  namespace: namma-prod
spec:
  podSelector:
    matchLabels:
      app: cloud-edge-ingress-nlb-and-tls-termination-topology
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: envoy-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: pgbouncer
    ports:
    - protocol: TCP
      port: 6432
```

#### Terraform / OpenTofu Infrastructure-as-Code Manifest:
```hcl
# Terraform security and subnet routing definition for ARCH-DEPLOY-002
resource "aws_security_group" "arch_deploy_002_sg" {
  name        = "namma-arch-deploy-002-sg"
  description = "Security group controlling traffic for Cloud Edge Ingress NLB & TLS Termination Topology"
  vpc_id      = var.vpc_id

  ingress {
    description = "Internal microservice traffic for ARCH-DEPLOY-002"
    from_port   = 8080
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Outbound dependency egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = "production"
    Topology    = "ARCH-DEPLOY-002"
    ManagedBy   = "terraform"
  }
}
```

#### Self-Healing & Automated Recovery Mechanism:
If container or host failure occurs under `ARCH-DEPLOY-002`, Kubernetes liveness probes detect failure within 30 seconds, automatically evicting the damaged pod and rescheduling on an alternate healthy node across remaining availability zones.

---

### 03.03 Topology Specification: `ARCH-DEPLOY-003` (Central Patroni PostgreSQL Primary/Standby Database Tier)
- **Topology Identifier:** `ARCH-DEPLOY-003`
- **Implementation Technology:** Dedicated EC2 Bare-Metal Instances + NVMe SAN Storage + Patroni DCS
- **Deployment Tier:** Core Relational Persistence Tier
- **Geographic & Architectural Scope:** Multi-AZ Dedicated Subnet (AZ-1, AZ-2, AZ-3)
- **Operational Purpose:** Authoritative transactional relational storage for all 30 platform modules.
- **Deployment & Scaling Strategy:** Deploy 3 dedicated `r6i.4xlarge` (16 vCPU, 128GB RAM) instances: 1 Primary (AZ-1), 1 Synchronous Standby (AZ-2), 1 Asynchronous Standby (AZ-3).
- **Architectural Resilience Outcome:** RPO = 0 across metropolitan AZs; RTO < 30 seconds for automated Patroni leader failover.

#### Step-by-Step Deployment & Commissioning Procedure:
1. Instances provisioned in dedicated, isolated database VPC subnets with no direct internet access.
2. Patroni integrates with 3-node etcd cluster for reliable distributed consensus.
3. Storage provisioned on AWS `io2` Block Express volumes with 15,000 IOPS and 500 MB/s bandwidth.
4. Continuous WAL archiving streams to multi-region S3 bucket via `pgbackrest`.
5. Automated daily backup integrity verification restores snapshot to test container.

#### Network Architecture & Port Allocation Matrix:
| Interface / Protocol | Inbound Port | Outbound Destination | Encryption Standard | Network Security Boundary |
| :--- | :---: | :--- | :---: | :--- |
| **Client HTTPS** | 8443 / TCP | API Gateway Service | TLS 1.3 / mTLS | Ingress Boundary WAF Protected |
| **Internal gRPC** | 50051 / TCP | Backend Microservice Tier | Internal mTLS (SPIFFE/SPIRE) | Calico Encrypted Pod Mesh |
| **Telemetry OTLP** | 4317 / gRPC | OpenTelemetry Collector | mTLS Token Auth | Monitoring Private Subnet |

#### Kubernetes NetworkPolicy Security Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: central-patroni-postgresql-primary/standby-database-tier-netpol
  namespace: namma-prod
spec:
  podSelector:
    matchLabels:
      app: central-patroni-postgresql-primary/standby-database-tier
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: envoy-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: pgbouncer
    ports:
    - protocol: TCP
      port: 6432
```

#### Terraform / OpenTofu Infrastructure-as-Code Manifest:
```hcl
# Terraform security and subnet routing definition for ARCH-DEPLOY-003
resource "aws_security_group" "arch_deploy_003_sg" {
  name        = "namma-arch-deploy-003-sg"
  description = "Security group controlling traffic for Central Patroni PostgreSQL Primary/Standby Database Tier"
  vpc_id      = var.vpc_id

  ingress {
    description = "Internal microservice traffic for ARCH-DEPLOY-003"
    from_port   = 8080
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Outbound dependency egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = "production"
    Topology    = "ARCH-DEPLOY-003"
    ManagedBy   = "terraform"
  }
}
```

#### Self-Healing & Automated Recovery Mechanism:
If container or host failure occurs under `ARCH-DEPLOY-003`, Kubernetes liveness probes detect failure within 30 seconds, automatically evicting the damaged pod and rescheduling on an alternate healthy node across remaining availability zones.

---

### 03.04 Topology Specification: `ARCH-DEPLOY-004` (Redis Multi-AZ In-Memory Cluster Topology)
- **Topology Identifier:** `ARCH-DEPLOY-004`
- **Implementation Technology:** AWS ElastiCache for Redis 7.2 / Self-Managed Redis Cluster
- **Deployment Tier:** In-Memory Caching & Session Store
- **Geographic & Architectural Scope:** 3 Shards (3 Masters + 3 Replicas Across 3 AZs)
- **Operational Purpose:** Session token caching, rate-limiting counters, and static drug formulary lookups.
- **Deployment & Scaling Strategy:** Deploy 6-node Redis cluster with automatic Multi-AZ failover and in-transit TLS encryption.
- **Architectural Resilience Outcome:** Sub-millisecond read/write latency; sustains 50,000 operations/sec with 99.99% availability.

#### Step-by-Step Deployment & Commissioning Procedure:
1. Redis Cluster partitions keys across 16,384 hash slots using CRC16 hash algorithm.
2. Master nodes located in AZ-1, AZ-2, and AZ-3; replicas cross-placed in alternate AZs.
3. Automated failover promotes replica to master in < 10 seconds if master node heartbeats fail.
4. Applications connect via cluster-aware Redis client library (`ioredis` / `go-redis`).
5. Daily automated backup snapshots retained in encrypted S3 bucket for 14 days.

#### Network Architecture & Port Allocation Matrix:
| Interface / Protocol | Inbound Port | Outbound Destination | Encryption Standard | Network Security Boundary |
| :--- | :---: | :--- | :---: | :--- |
| **Client HTTPS** | 8443 / TCP | API Gateway Service | TLS 1.3 / mTLS | Ingress Boundary WAF Protected |
| **Internal gRPC** | 50051 / TCP | Backend Microservice Tier | Internal mTLS (SPIFFE/SPIRE) | Calico Encrypted Pod Mesh |
| **Telemetry OTLP** | 4317 / gRPC | OpenTelemetry Collector | mTLS Token Auth | Monitoring Private Subnet |

#### Kubernetes NetworkPolicy Security Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: redis-multi-az-in-memory-cluster-topology-netpol
  namespace: namma-prod
spec:
  podSelector:
    matchLabels:
      app: redis-multi-az-in-memory-cluster-topology
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: envoy-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: pgbouncer
    ports:
    - protocol: TCP
      port: 6432
```

#### Terraform / OpenTofu Infrastructure-as-Code Manifest:
```hcl
# Terraform security and subnet routing definition for ARCH-DEPLOY-004
resource "aws_security_group" "arch_deploy_004_sg" {
  name        = "namma-arch-deploy-004-sg"
  description = "Security group controlling traffic for Redis Multi-AZ In-Memory Cluster Topology"
  vpc_id      = var.vpc_id

  ingress {
    description = "Internal microservice traffic for ARCH-DEPLOY-004"
    from_port   = 8080
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Outbound dependency egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = "production"
    Topology    = "ARCH-DEPLOY-004"
    ManagedBy   = "terraform"
  }
}
```

#### Self-Healing & Automated Recovery Mechanism:
If container or host failure occurs under `ARCH-DEPLOY-004`, Kubernetes liveness probes detect failure within 30 seconds, automatically evicting the damaged pod and rescheduling on an alternate healthy node across remaining availability zones.

---

### 03.05 Topology Specification: `ARCH-DEPLOY-005` (Apache Kafka Distributed Event Streaming Broker Topology)
- **Topology Identifier:** `ARCH-DEPLOY-005`
- **Implementation Technology:** Apache Kafka 3.6+ Cluster (KRaft Mode) Across 3 AZs
- **Deployment Tier:** Asynchronous Messaging & CDC Ingestion
- **Geographic & Architectural Scope:** 5 Dedicated Broker Instances Across 3 AZs
- **Operational Purpose:** Clinical CDC event streams, SMS notification queues, and ABDM care context publishing.
- **Deployment & Scaling Strategy:** Deploy 5 Kafka broker instances with NVMe storage and KRaft metadata mode (zero ZooKeeper dependency).
- **Architectural Resilience Outcome:** Sustains 10,000 messages/sec with end-to-end publish-to-consume latency < 20ms.

#### Step-by-Step Deployment & Commissioning Procedure:
1. Brokers deployed across 3 AZs (2 in AZ-1, 2 in AZ-2, 1 in AZ-3).
2. High-throughput topics provisioned with 16 partitions and `min.insync.replicas = 2`.
3. KRaft metadata quorum uses 3 dedicated controller nodes for fast leader elections.
4. Producer applications publish with `acks = all` guaranteeing zero message loss.
5. Debezium PostgreSQL connector streams database WAL changes to Kafka CDC topics.

#### Network Architecture & Port Allocation Matrix:
| Interface / Protocol | Inbound Port | Outbound Destination | Encryption Standard | Network Security Boundary |
| :--- | :---: | :--- | :---: | :--- |
| **Client HTTPS** | 8443 / TCP | API Gateway Service | TLS 1.3 / mTLS | Ingress Boundary WAF Protected |
| **Internal gRPC** | 50051 / TCP | Backend Microservice Tier | Internal mTLS (SPIFFE/SPIRE) | Calico Encrypted Pod Mesh |
| **Telemetry OTLP** | 4317 / gRPC | OpenTelemetry Collector | mTLS Token Auth | Monitoring Private Subnet |

#### Kubernetes NetworkPolicy Security Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: apache-kafka-distributed-event-streaming-broker-topology-netpol
  namespace: namma-prod
spec:
  podSelector:
    matchLabels:
      app: apache-kafka-distributed-event-streaming-broker-topology
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: envoy-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: pgbouncer
    ports:
    - protocol: TCP
      port: 6432
```

#### Terraform / OpenTofu Infrastructure-as-Code Manifest:
```hcl
# Terraform security and subnet routing definition for ARCH-DEPLOY-005
resource "aws_security_group" "arch_deploy_005_sg" {
  name        = "namma-arch-deploy-005-sg"
  description = "Security group controlling traffic for Apache Kafka Distributed Event Streaming Broker Topology"
  vpc_id      = var.vpc_id

  ingress {
    description = "Internal microservice traffic for ARCH-DEPLOY-005"
    from_port   = 8080
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Outbound dependency egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = "production"
    Topology    = "ARCH-DEPLOY-005"
    ManagedBy   = "terraform"
  }
}
```

#### Self-Healing & Automated Recovery Mechanism:
If container or host failure occurs under `ARCH-DEPLOY-005`, Kubernetes liveness probes detect failure within 30 seconds, automatically evicting the damaged pod and rescheduling on an alternate healthy node across remaining availability zones.

---

### 03.06 Topology Specification: `ARCH-DEPLOY-006` (ClickHouse Columnar Analytics MPP Cluster Topology)
- **Topology Identifier:** `ARCH-DEPLOY-006`
- **Implementation Technology:** ClickHouse 24.3 Cluster (2 Shards, 2 Replicas Per Shard)
- **Deployment Tier:** Municipal Public Health Data Warehouse
- **Geographic & Architectural Scope:** 4 Dedicated Worker Nodes Across 2 AZs
- **Operational Purpose:** Aggregated epidemiological reporting, syndromic surveillance, and drug consumption analytics.
- **Deployment & Scaling Strategy:** Deploy 4 ClickHouse worker instances in 2x2 shard/replica matrix with automated S3 cold tiering.
- **Architectural Resilience Outcome:** Analytical aggregation queries across 50 million clinical records execute in < 450ms.

#### Step-by-Step Deployment & Commissioning Procedure:
1. ClickHouse nodes run on `r6i.2xlarge` instances with local NVMe cache volumes.
2. Distributed table engine federates analytical queries across shards.
3. ClickHouse Keeper provides lightweight metadata coordination and replica sync.
4. Storage policy tiers data older than 90 days from NVMe SSD to Amazon S3 Standard.
5. Materialized views pre-calculate hourly ward-level disease prevalence summaries.

#### Network Architecture & Port Allocation Matrix:
| Interface / Protocol | Inbound Port | Outbound Destination | Encryption Standard | Network Security Boundary |
| :--- | :---: | :--- | :---: | :--- |
| **Client HTTPS** | 8443 / TCP | API Gateway Service | TLS 1.3 / mTLS | Ingress Boundary WAF Protected |
| **Internal gRPC** | 50051 / TCP | Backend Microservice Tier | Internal mTLS (SPIFFE/SPIRE) | Calico Encrypted Pod Mesh |
| **Telemetry OTLP** | 4317 / gRPC | OpenTelemetry Collector | mTLS Token Auth | Monitoring Private Subnet |

#### Kubernetes NetworkPolicy Security Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: clickhouse-columnar-analytics-mpp-cluster-topology-netpol
  namespace: namma-prod
spec:
  podSelector:
    matchLabels:
      app: clickhouse-columnar-analytics-mpp-cluster-topology
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: envoy-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: pgbouncer
    ports:
    - protocol: TCP
      port: 6432
```

#### Terraform / OpenTofu Infrastructure-as-Code Manifest:
```hcl
# Terraform security and subnet routing definition for ARCH-DEPLOY-006
resource "aws_security_group" "arch_deploy_006_sg" {
  name        = "namma-arch-deploy-006-sg"
  description = "Security group controlling traffic for ClickHouse Columnar Analytics MPP Cluster Topology"
  vpc_id      = var.vpc_id

  ingress {
    description = "Internal microservice traffic for ARCH-DEPLOY-006"
    from_port   = 8080
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Outbound dependency egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = "production"
    Topology    = "ARCH-DEPLOY-006"
    ManagedBy   = "terraform"
  }
}
```

#### Self-Healing & Automated Recovery Mechanism:
If container or host failure occurs under `ARCH-DEPLOY-006`, Kubernetes liveness probes detect failure within 30 seconds, automatically evicting the damaged pod and rescheduling on an alternate healthy node across remaining availability zones.

---

### 03.07 Topology Specification: `ARCH-DEPLOY-007` (HashiCorp Vault KMS Secrets Management Infrastructure)
- **Topology Identifier:** `ARCH-DEPLOY-007`
- **Implementation Technology:** HashiCorp Vault High-Availability Cluster (Raft Storage)
- **Deployment Tier:** Enterprise Security & Cryptographic KMS
- **Geographic & Architectural Scope:** 3 Dedicated Instances Across 3 AZs
- **Operational Purpose:** Management of master database passwords, mTLS Root CA, JWT signing keys, and encryption tokens.
- **Deployment & Scaling Strategy:** Deploy 3-node Vault cluster using integrated Raft storage consensus and AWS KMS auto-unseal.
- **Architectural Resilience Outcome:** Sub-millisecond secret retrieval; guarantees continuous cryptographic availability with zero manual unsealing.

#### Step-by-Step Deployment & Commissioning Procedure:
1. Vault instances run on hardened Amazon Linux 2023 with locked memory limits (`mlock`).
2. AWS KMS master key automatically unseals Vault instances upon reboot.
3. Vault Transit Secrets Engine performs AES-256-GCM encryption-as-a-service for PII fields.
4. PKI Secrets Engine issues short-lived (24-hour) X.509 certificates for microservice mTLS.
5. Dynamic database credentials generate ephemeral PostgreSQL user roles expiring after 1 hour.

#### Network Architecture & Port Allocation Matrix:
| Interface / Protocol | Inbound Port | Outbound Destination | Encryption Standard | Network Security Boundary |
| :--- | :---: | :--- | :---: | :--- |
| **Client HTTPS** | 8443 / TCP | API Gateway Service | TLS 1.3 / mTLS | Ingress Boundary WAF Protected |
| **Internal gRPC** | 50051 / TCP | Backend Microservice Tier | Internal mTLS (SPIFFE/SPIRE) | Calico Encrypted Pod Mesh |
| **Telemetry OTLP** | 4317 / gRPC | OpenTelemetry Collector | mTLS Token Auth | Monitoring Private Subnet |

#### Kubernetes NetworkPolicy Security Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: hashicorp-vault-kms-secrets-management-infrastructure-netpol
  namespace: namma-prod
spec:
  podSelector:
    matchLabels:
      app: hashicorp-vault-kms-secrets-management-infrastructure
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: envoy-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: pgbouncer
    ports:
    - protocol: TCP
      port: 6432
```

#### Terraform / OpenTofu Infrastructure-as-Code Manifest:
```hcl
# Terraform security and subnet routing definition for ARCH-DEPLOY-007
resource "aws_security_group" "arch_deploy_007_sg" {
  name        = "namma-arch-deploy-007-sg"
  description = "Security group controlling traffic for HashiCorp Vault KMS Secrets Management Infrastructure"
  vpc_id      = var.vpc_id

  ingress {
    description = "Internal microservice traffic for ARCH-DEPLOY-007"
    from_port   = 8080
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Outbound dependency egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = "production"
    Topology    = "ARCH-DEPLOY-007"
    ManagedBy   = "terraform"
  }
}
```

#### Self-Healing & Automated Recovery Mechanism:
If container or host failure occurs under `ARCH-DEPLOY-007`, Kubernetes liveness probes detect failure within 30 seconds, automatically evicting the damaged pod and rescheduling on an alternate healthy node across remaining availability zones.

---

### 03.08 Topology Specification: `ARCH-DEPLOY-008` (Clinic Edge Intel N100 Appliance Hardware & OS Architecture)
- **Topology Identifier:** `ARCH-DEPLOY-008`
- **Implementation Technology:** Physical Intel N100 Fanless Mini-Server + Ubuntu Server 24.04 LTS CIS
- **Deployment Tier:** Physical Edge Clinic Computing Node
- **Geographic & Architectural Scope:** 183 Physical Installations Across Greater Bengaluru
- **Operational Purpose:** Hosts local SQLite database, PWA web server, and offline synchronization daemon at clinic site.
- **Deployment & Scaling Strategy:** Deploy rugged fanless Intel N100 mini-server (16GB RAM, dual 512GB NVMe RAID 1) in locked 6U rack.
- **Architectural Resilience Outcome:** Continuous autonomous operation for 72 hours during complete network isolation; survives abrupt power loss.

#### Step-by-Step Deployment & Commissioning Procedure:
1. Intel N100 quad-core processor (up to 3.4GHz) operates fanless with aluminum heatsink.
2. Dual 512GB PCIe 4.0 NVMe SSDs configured in hardware RAID 1 via Linux `mdadm`.
3. Dual Gigabit Ethernet ports isolate clinic LAN traffic from WAN router.
4. Embedded Quectel 4G/5G LTE modem with Airtel/Jio dual-eSIM for cellular failover.
5. BIOS configured for 'AC Power Recovery: Always On' to ensure auto-reboot post-blackout.

#### Network Architecture & Port Allocation Matrix:
| Interface / Protocol | Inbound Port | Outbound Destination | Encryption Standard | Network Security Boundary |
| :--- | :---: | :--- | :---: | :--- |
| **Client HTTPS** | 8443 / TCP | API Gateway Service | TLS 1.3 / mTLS | Ingress Boundary WAF Protected |
| **Internal gRPC** | 50051 / TCP | Backend Microservice Tier | Internal mTLS (SPIFFE/SPIRE) | Calico Encrypted Pod Mesh |
| **Telemetry OTLP** | 4317 / gRPC | OpenTelemetry Collector | mTLS Token Auth | Monitoring Private Subnet |

#### Kubernetes NetworkPolicy Security Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: clinic-edge-intel-n100-appliance-hardware-and-os-architecture-netpol
  namespace: namma-prod
spec:
  podSelector:
    matchLabels:
      app: clinic-edge-intel-n100-appliance-hardware-and-os-architecture
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: envoy-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: pgbouncer
    ports:
    - protocol: TCP
      port: 6432
```

#### Terraform / OpenTofu Infrastructure-as-Code Manifest:
```hcl
# Terraform security and subnet routing definition for ARCH-DEPLOY-008
resource "aws_security_group" "arch_deploy_008_sg" {
  name        = "namma-arch-deploy-008-sg"
  description = "Security group controlling traffic for Clinic Edge Intel N100 Appliance Hardware & OS Architecture"
  vpc_id      = var.vpc_id

  ingress {
    description = "Internal microservice traffic for ARCH-DEPLOY-008"
    from_port   = 8080
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Outbound dependency egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = "production"
    Topology    = "ARCH-DEPLOY-008"
    ManagedBy   = "terraform"
  }
}
```

#### Self-Healing & Automated Recovery Mechanism:
If container or host failure occurs under `ARCH-DEPLOY-008`, Kubernetes liveness probes detect failure within 30 seconds, automatically evicting the damaged pod and rescheduling on an alternate healthy node across remaining availability zones.

---

### 03.09 Topology Specification: `ARCH-DEPLOY-009` (Clinic LAN Micro-Network & Peripheral Hardware Topology)
- **Topology Identifier:** `ARCH-DEPLOY-009`
- **Implementation Technology:** Gigabit PoE+ Managed Switch + Wi-Fi 6 Access Point + Peripherals
- **Deployment Tier:** Clinic Site Physical Networking
- **Geographic & Architectural Scope:** Standardized Physical Clinic Interior Topology
- **Operational Purpose:** Connects doctor, nurse, and pharmacy workstation tablets, thermal receipt printers, and barcode scanners.
- **Deployment & Scaling Strategy:** Deploy Cisco Business CBS250-8P-E-2G Gigabit PoE+ switch and Cisco WAP150 dual-band Wi-Fi 6 AP.
- **Architectural Resilience Outcome:** Secure, segmented clinic Wi-Fi with WPA3-Enterprise; zero cross-talk between staff devices and public visitors.

#### Step-by-Step Deployment & Commissioning Procedure:
1. Switch provides 8 Gigabit PoE+ ports powering Wi-Fi AP and edge mini-server.
2. VLAN 10 (Clinical Staff): Encrypted WPA3-Enterprise Wi-Fi for workstation tablets.
3. VLAN 20 (Edge Server & Peripherals): Wired ports for mini-server, thermal printers, and lab analyzers.
4. VLAN 30 (Guest / Public): Isolated internet-only Wi-Fi for citizen queue status.
5. 80mm thermal receipt printers connect via USB/LAN; 2D barcode scanners connect via USB HID.

#### Network Architecture & Port Allocation Matrix:
| Interface / Protocol | Inbound Port | Outbound Destination | Encryption Standard | Network Security Boundary |
| :--- | :---: | :--- | :---: | :--- |
| **Client HTTPS** | 8443 / TCP | API Gateway Service | TLS 1.3 / mTLS | Ingress Boundary WAF Protected |
| **Internal gRPC** | 50051 / TCP | Backend Microservice Tier | Internal mTLS (SPIFFE/SPIRE) | Calico Encrypted Pod Mesh |
| **Telemetry OTLP** | 4317 / gRPC | OpenTelemetry Collector | mTLS Token Auth | Monitoring Private Subnet |

#### Kubernetes NetworkPolicy Security Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: clinic-lan-micro-network-and-peripheral-hardware-topology-netpol
  namespace: namma-prod
spec:
  podSelector:
    matchLabels:
      app: clinic-lan-micro-network-and-peripheral-hardware-topology
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: envoy-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: pgbouncer
    ports:
    - protocol: TCP
      port: 6432
```

#### Terraform / OpenTofu Infrastructure-as-Code Manifest:
```hcl
# Terraform security and subnet routing definition for ARCH-DEPLOY-009
resource "aws_security_group" "arch_deploy_009_sg" {
  name        = "namma-arch-deploy-009-sg"
  description = "Security group controlling traffic for Clinic LAN Micro-Network & Peripheral Hardware Topology"
  vpc_id      = var.vpc_id

  ingress {
    description = "Internal microservice traffic for ARCH-DEPLOY-009"
    from_port   = 8080
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Outbound dependency egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = "production"
    Topology    = "ARCH-DEPLOY-009"
    ManagedBy   = "terraform"
  }
}
```

#### Self-Healing & Automated Recovery Mechanism:
If container or host failure occurs under `ARCH-DEPLOY-009`, Kubernetes liveness probes detect failure within 30 seconds, automatically evicting the damaged pod and rescheduling on an alternate healthy node across remaining availability zones.

---

### 03.10 Topology Specification: `ARCH-DEPLOY-010` (Zero-Touch Edge Provisioning (ZTP) & Cloud Fleet Commissioning)
- **Topology Identifier:** `ARCH-DEPLOY-010`
- **Implementation Technology:** Automated TPM 2.0 Attestation + Ansible Provisioning + Cloud Registry
- **Deployment Tier:** Edge Fleet Lifecycle Management Tier
- **Geographic & Architectural Scope:** Central ZTP Registration Service + 183 Appliances
- **Operational Purpose:** Automated commissioning and onboarding of new clinic edge appliances with zero manual technician configuration.
- **Deployment & Scaling Strategy:** Pre-seed appliance NVMe with factory OS image. Upon first boot, appliance uses TPM 2.0 to attest identity and pull configuration.
- **Architectural Resilience Outcome:** Full commissioning completed in < 15 minutes; zero plaintext credentials stored on factory disk images.

#### Step-by-Step Deployment & Commissioning Procedure:
1. Technician plugs appliance into clinic power and network; powers unit on.
2. Appliance boots; systemd unit `namma-ztp.service` launches onboarding agent.
3. Agent generates TPM 2.0 quote and submits to central ZTP endpoint with serial number.
4. Cloud registry validates TPM quote against factory hardware procurement manifest.
5. Vault PKI issues clinic-specific device mTLS certificate and private key.
6. Appliance downloads encrypted tenant slice and active drug formulary from cloud sync API.
7. Local SQLite database initialized, schema migrations run, and local PWA web server started.
8. Appliance prints automated commissioning receipt on thermal printer; marks clinic 'ACTIVE'.

#### Network Architecture & Port Allocation Matrix:
| Interface / Protocol | Inbound Port | Outbound Destination | Encryption Standard | Network Security Boundary |
| :--- | :---: | :--- | :---: | :--- |
| **Client HTTPS** | 8443 / TCP | API Gateway Service | TLS 1.3 / mTLS | Ingress Boundary WAF Protected |
| **Internal gRPC** | 50051 / TCP | Backend Microservice Tier | Internal mTLS (SPIFFE/SPIRE) | Calico Encrypted Pod Mesh |
| **Telemetry OTLP** | 4317 / gRPC | OpenTelemetry Collector | mTLS Token Auth | Monitoring Private Subnet |

#### Kubernetes NetworkPolicy Security Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: zero-touch-edge-provisioning-(ztp)-and-cloud-fleet-commissioning-netpol
  namespace: namma-prod
spec:
  podSelector:
    matchLabels:
      app: zero-touch-edge-provisioning-(ztp)-and-cloud-fleet-commissioning
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: envoy-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: pgbouncer
    ports:
    - protocol: TCP
      port: 6432
```

#### Terraform / OpenTofu Infrastructure-as-Code Manifest:
```hcl
# Terraform security and subnet routing definition for ARCH-DEPLOY-010
resource "aws_security_group" "arch_deploy_010_sg" {
  name        = "namma-arch-deploy-010-sg"
  description = "Security group controlling traffic for Zero-Touch Edge Provisioning (ZTP) & Cloud Fleet Commissioning"
  vpc_id      = var.vpc_id

  ingress {
    description = "Internal microservice traffic for ARCH-DEPLOY-010"
    from_port   = 8080
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Outbound dependency egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = "production"
    Topology    = "ARCH-DEPLOY-010"
    ManagedBy   = "terraform"
  }
}
```

#### Self-Healing & Automated Recovery Mechanism:
If container or host failure occurs under `ARCH-DEPLOY-010`, Kubernetes liveness probes detect failure within 30 seconds, automatically evicting the damaged pod and rescheduling on an alternate healthy node across remaining availability zones.

---

### 03.11 Topology Specification: `ARCH-DEPLOY-011` (Blue/Green Zero-Downtime Central Application Release Pipeline)
- **Topology Identifier:** `ARCH-DEPLOY-011`
- **Implementation Technology:** Argo Rollouts + Envoy Service Route Shifting + Automated Analysis
- **Deployment Tier:** Continuous Deployment Release Tier
- **Geographic & Architectural Scope:** Central Cloud Microservice Workloads
- **Operational Purpose:** Zero-downtime production deployment of backend microservice updates across all 183 clinics.
- **Deployment & Scaling Strategy:** Deploy new software versions alongside active production pods (Blue/Green). Shift traffic via Envoy routing rules after automated analysis.
- **Architectural Resilience Outcome:** 100% zero-downtime releases; automated rollback in < 30 seconds if error rates exceed 0.1%.

#### Step-by-Step Deployment & Commissioning Procedure:
1. GitHub Actions CI pipeline builds container images, runs unit tests, and pushes to ECR.
2. ArgoCD detects Git commit to release branch; applies Kubernetes manifest updates.
3. Argo Rollouts creates Green replica deployment alongside active Blue deployment.
4. Automated analysis runs smoke tests and validates synthetic API transactions against Green pods.
5. Envoy shifts 10% of production traffic to Green; monitors P95 latency and HTTP 5xx error rate for 5 minutes.
6. If error rate < 0.1%, Envoy shifts 100% traffic to Green; Blue pods kept idle for 30 minutes before termination.

#### Network Architecture & Port Allocation Matrix:
| Interface / Protocol | Inbound Port | Outbound Destination | Encryption Standard | Network Security Boundary |
| :--- | :---: | :--- | :---: | :--- |
| **Client HTTPS** | 8443 / TCP | API Gateway Service | TLS 1.3 / mTLS | Ingress Boundary WAF Protected |
| **Internal gRPC** | 50051 / TCP | Backend Microservice Tier | Internal mTLS (SPIFFE/SPIRE) | Calico Encrypted Pod Mesh |
| **Telemetry OTLP** | 4317 / gRPC | OpenTelemetry Collector | mTLS Token Auth | Monitoring Private Subnet |

#### Kubernetes NetworkPolicy Security Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: blue/green-zero-downtime-central-application-release-pipeline-netpol
  namespace: namma-prod
spec:
  podSelector:
    matchLabels:
      app: blue/green-zero-downtime-central-application-release-pipeline
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: envoy-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: pgbouncer
    ports:
    - protocol: TCP
      port: 6432
```

#### Terraform / OpenTofu Infrastructure-as-Code Manifest:
```hcl
# Terraform security and subnet routing definition for ARCH-DEPLOY-011
resource "aws_security_group" "arch_deploy_011_sg" {
  name        = "namma-arch-deploy-011-sg"
  description = "Security group controlling traffic for Blue/Green Zero-Downtime Central Application Release Pipeline"
  vpc_id      = var.vpc_id

  ingress {
    description = "Internal microservice traffic for ARCH-DEPLOY-011"
    from_port   = 8080
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Outbound dependency egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = "production"
    Topology    = "ARCH-DEPLOY-011"
    ManagedBy   = "terraform"
  }
}
```

#### Self-Healing & Automated Recovery Mechanism:
If container or host failure occurs under `ARCH-DEPLOY-011`, Kubernetes liveness probes detect failure within 30 seconds, automatically evicting the damaged pod and rescheduling on an alternate healthy node across remaining availability zones.

---

### 03.12 Topology Specification: `ARCH-DEPLOY-012` (Canary & Rolling OTA Edge Fleet Firmware / Application Upgrade)
- **Topology Identifier:** `ARCH-DEPLOY-012`
- **Implementation Technology:** Zonal Ring Deployment + Docker Compose Rolling OTA + Local Rollback
- **Deployment Tier:** Edge Fleet Over-The-Air (OTA) Update Tier
- **Geographic & Architectural Scope:** 183 Physical Clinics Grouped into 4 Zonal Rings
- **Operational Purpose:** Distribution of software updates, bug fixes, and security patches to edge mini-servers across Bengaluru.
- **Deployment & Scaling Strategy:** Deploy updates progressively in 4 rollout rings: Ring 0 (Canary 5 clinics) -> Ring 1 (South 25 clinics) -> Ring 2 (West/East 50 clinics) -> Ring 3 (All 183 clinics).
- **Architectural Resilience Outcome:** Guarantees that a defective edge build can affect at most 5 clinics before automated fleet rollout halt.

#### Step-by-Step Deployment & Commissioning Procedure:
1. Central fleet management console publishes new edge release manifest (`v1.4.3.json`).
2. Edge daemons in Ring 0 (Canary) download container image deltas over night bandwidth window (22:00 - 05:00).
3. Edge daemon executes atomic Docker Compose recreate on secondary container slot.
4. Pre-flight health check script verifies local SQLite migration and PWA asset integrity.
5. If health check passes, traffic routes to new container; old container retained in stopped state.
6. Canary clinics operate for 48 hours; central dashboard monitors edge error telemetry.
7. Upon successful canary validation, release promotes to Ring 1, Ring 2, and Ring 3 sequentially.
8. If edge crashes within 15 minutes of update, local watchdog autonomously rolls back to previous slot.

#### Network Architecture & Port Allocation Matrix:
| Interface / Protocol | Inbound Port | Outbound Destination | Encryption Standard | Network Security Boundary |
| :--- | :---: | :--- | :---: | :--- |
| **Client HTTPS** | 8443 / TCP | API Gateway Service | TLS 1.3 / mTLS | Ingress Boundary WAF Protected |
| **Internal gRPC** | 50051 / TCP | Backend Microservice Tier | Internal mTLS (SPIFFE/SPIRE) | Calico Encrypted Pod Mesh |
| **Telemetry OTLP** | 4317 / gRPC | OpenTelemetry Collector | mTLS Token Auth | Monitoring Private Subnet |

#### Kubernetes NetworkPolicy Security Isolation Manifest:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: canary-and-rolling-ota-edge-fleet-firmware-/-application-upgrade-netpol
  namespace: namma-prod
spec:
  podSelector:
    matchLabels:
      app: canary-and-rolling-ota-edge-fleet-firmware-/-application-upgrade
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: envoy-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: pgbouncer
    ports:
    - protocol: TCP
      port: 6432
```

#### Terraform / OpenTofu Infrastructure-as-Code Manifest:
```hcl
# Terraform security and subnet routing definition for ARCH-DEPLOY-012
resource "aws_security_group" "arch_deploy_012_sg" {
  name        = "namma-arch-deploy-012-sg"
  description = "Security group controlling traffic for Canary & Rolling OTA Edge Fleet Firmware / Application Upgrade"
  vpc_id      = var.vpc_id

  ingress {
    description = "Internal microservice traffic for ARCH-DEPLOY-012"
    from_port   = 8080
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Outbound dependency egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = "production"
    Topology    = "ARCH-DEPLOY-012"
    ManagedBy   = "terraform"
  }
}
```

#### Self-Healing & Automated Recovery Mechanism:
If container or host failure occurs under `ARCH-DEPLOY-012`, Kubernetes liveness probes detect failure within 30 seconds, automatically evicting the damaged pod and rescheduling on an alternate healthy node across remaining availability zones.

---

## 04. Edge Appliance Operating System & CIS Benchmark Hardening
Comprehensive Linux operating system configuration and CIS Level 2 hardening for Intel N100 edge appliances:

### 04.1 Linux Kernel & Security Hardening Parameters (`/etc/sysctl.d/99-namma-hardening.conf`)
```ini
# IP Spoofing protection
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignore ICMP broadcast requests
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Disable source packet routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0

# Ignore send redirects
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Block SYN flood attacks
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2

# Virtual memory and core dump restrictions
fs.suid_dumpable = 0
kernel.randomize_va_space = 2
```

### 04.2 Uncomplicated Firewall (UFW) Edge Port Security Rules
```bash
# Reset UFW rules to default deny
ufw default deny incoming
ufw default allow outgoing

# Allow LAN clinic subnet (VLAN 10 & 20) to access PWA web server
ufw allow from 192.168.10.0/24 to any port 8443 proto tcp comment 'Clinic Tablets HTTPS'
ufw allow from 192.168.20.0/24 to any port 8443 proto tcp comment 'Peripherals HTTPS'

# Allow SSH only from dedicated physical Service Port (eth1: 192.168.100.1)
ufw allow in on eth1 to any port 22 proto tcp comment 'Technician Service Port SSH'

# Enable firewall
ufw --force enable
```

## 05. Kubernetes Helm Chart Architecture & Sub-Chart Values Configurations
Production Helm chart specifications and detailed `values.yaml` manifests for all 15 cloud microservice sub-charts:

### 05.api_gateway Sub-Chart Blueprint: `api-gateway` (ARCH-CONT-003)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/api-gateway`
- **Governing Container:** `ARCH-CONT-003` (Envoy Ingress Gateway)
- **Default Service Port:** `8080` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 3
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/api-gateway
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8080
resources:
  requests:
    cpu: '1000m'
    memory: '1024Mi'
  limits:
    cpu: '4000m'
    memory: '4096Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 12
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-gateway-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: api-gateway-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: api-gateway-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: api-gateway-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: api-gateway-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.auth_service Sub-Chart Blueprint: `auth-service` (ARCH-CONT-004)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/auth-service`
- **Governing Container:** `ARCH-CONT-004` (Identity & Access Management)
- **Default Service Port:** `8081` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 2
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/auth-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8081
resources:
  requests:
    cpu: '500m'
    memory: '512Mi'
  limits:
    cpu: '2000m'
    memory: '2048Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 8
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: auth-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: auth-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: auth-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: auth-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: auth-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.mpi_service Sub-Chart Blueprint: `mpi-service` (ARCH-CONT-005)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/mpi-service`
- **Governing Container:** `ARCH-CONT-005` (Master Patient Index)
- **Default Service Port:** `8082` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 3
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/mpi-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8082
resources:
  requests:
    cpu: '1000m'
    memory: '1024Mi'
  limits:
    cpu: '4000m'
    memory: '4096Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: mpi-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: mpi-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: mpi-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: mpi-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: mpi-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.queue_service Sub-Chart Blueprint: `queue-service` (ARCH-CONT-006)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/queue-service`
- **Governing Container:** `ARCH-CONT-006` (Queue Orchestration & Triage)
- **Default Service Port:** `8083` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 2
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/queue-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8083
resources:
  requests:
    cpu: '500m'
    memory: '512Mi'
  limits:
    cpu: '2000m'
    memory: '2048Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 8
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: queue-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: queue-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: queue-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: queue-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: queue-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.consultation_service Sub-Chart Blueprint: `consultation-service` (ARCH-CONT-007)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/consultation-service`
- **Governing Container:** `ARCH-CONT-007` (Clinical EMR Consultation)
- **Default Service Port:** `8084` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 4
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/consultation-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8084
resources:
  requests:
    cpu: '1000m'
    memory: '1024Mi'
  limits:
    cpu: '4000m'
    memory: '4096Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 4
  maxReplicas: 16
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: consultation-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: consultation-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: consultation-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: consultation-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: consultation-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.prescription_service Sub-Chart Blueprint: `prescription-service` (ARCH-CONT-008)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/prescription-service`
- **Governing Container:** `ARCH-CONT-008` (Drug Safety & e-Prescribing)
- **Default Service Port:** `8085` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 3
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/prescription-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8085
resources:
  requests:
    cpu: '500m'
    memory: '512Mi'
  limits:
    cpu: '2000m'
    memory: '2048Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: prescription-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: prescription-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: prescription-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: prescription-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: prescription-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.pharmacy_service Sub-Chart Blueprint: `pharmacy-service` (ARCH-CONT-009)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/pharmacy-service`
- **Governing Container:** `ARCH-CONT-009` (Pharmacy Inventory & Dispense)
- **Default Service Port:** `8086` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 3
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/pharmacy-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8086
resources:
  requests:
    cpu: '500m'
    memory: '512Mi'
  limits:
    cpu: '2000m'
    memory: '2048Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: pharmacy-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pharmacy-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pharmacy-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: pharmacy-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: pharmacy-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.lab_service Sub-Chart Blueprint: `lab-service` (ARCH-CONT-010)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/lab-service`
- **Governing Container:** `ARCH-CONT-010` (Diagnostic Laboratory Testing)
- **Default Service Port:** `8087` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 2
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/lab-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8087
resources:
  requests:
    cpu: '500m'
    memory: '512Mi'
  limits:
    cpu: '2000m'
    memory: '2048Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 8
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: lab-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: lab-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: lab-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: lab-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: lab-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.referral_service Sub-Chart Blueprint: `referral-service` (ARCH-CONT-011)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/referral-service`
- **Governing Container:** `ARCH-CONT-011` (108 CAD Emergency Referral)
- **Default Service Port:** `8088` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 2
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/referral-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8088
resources:
  requests:
    cpu: '250m'
    memory: '256Mi'
  limits:
    cpu: '1000m'
    memory: '1024Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 6
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: referral-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: referral-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: referral-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: referral-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: referral-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.notification_service Sub-Chart Blueprint: `notification-service` (ARCH-CONT-012)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/notification-service`
- **Governing Container:** `ARCH-CONT-012` (Citizen SMS & Communication)
- **Default Service Port:** `8089` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 2
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/notification-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8089
resources:
  requests:
    cpu: '500m'
    memory: '512Mi'
  limits:
    cpu: '2000m'
    memory: '2048Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 8
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: notification-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: notification-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: notification-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: notification-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: notification-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.sync_service Sub-Chart Blueprint: `sync-service` (ARCH-CONT-013)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/sync-service`
- **Governing Container:** `ARCH-CONT-013` (Edge-Cloud Data Synchronization)
- **Default Service Port:** `8090` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 4
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/sync-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8090
resources:
  requests:
    cpu: '1000m'
    memory: '1024Mi'
  limits:
    cpu: '4000m'
    memory: '4096Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 4
  maxReplicas: 16
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: sync-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: sync-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: sync-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: sync-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: sync-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.abdm_service Sub-Chart Blueprint: `abdm-service` (ARCH-CONT-014)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/abdm-service`
- **Governing Container:** `ARCH-CONT-014` (National ABDM FHIR Gateway)
- **Default Service Port:** `8091` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 2
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/abdm-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8091
resources:
  requests:
    cpu: '1000m'
    memory: '2048Mi'
  limits:
    cpu: '4000m'
    memory: '8192Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 8
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: abdm-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: abdm-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: abdm-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: abdm-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: abdm-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.analytics_service Sub-Chart Blueprint: `analytics-service` (ARCH-CONT-015)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/analytics-service`
- **Governing Container:** `ARCH-CONT-015` (ClickHouse CDC Ingestion)
- **Default Service Port:** `8092` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 2
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/analytics-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8092
resources:
  requests:
    cpu: '1000m'
    memory: '2048Mi'
  limits:
    cpu: '4000m'
    memory: '8192Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 6
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: analytics-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: analytics-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: analytics-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: analytics-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: analytics-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.ai_advisory_service Sub-Chart Blueprint: `ai-advisory-service` (ARCH-CONT-016)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/ai-advisory-service`
- **Governing Container:** `ARCH-CONT-016` (Clinical AI Decision Support)
- **Default Service Port:** `8093` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 2
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/ai-advisory-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8093
resources:
  requests:
    cpu: '1000m'
    memory: '2048Mi'
  limits:
    cpu: '4000m'
    memory: '8192Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 6
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ai-advisory-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ai-advisory-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ai-advisory-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: ai-advisory-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: ai-advisory-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 05.audit_service Sub-Chart Blueprint: `audit-service` (ARCH-CONT-017)
- **Sub-Chart Identifier:** `charts/namma-platform/charts/audit-service`
- **Governing Container:** `ARCH-CONT-017` (WORM Cryptographic Audit Ledger)
- **Default Service Port:** `8094` / TCP

#### Authoritative Sub-Chart `values.yaml` Configuration:
```yaml
replicaCount: 2
image:
  repository: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/audit-service
  tag: 'v1.4.2'
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8094
resources:
  requests:
    cpu: '500m'
    memory: '512Mi'
  limits:
    cpu: '2000m'
    memory: '2048Mi'
env:
  - name: NODE_ENV
    value: 'production'
  - name: LOG_LEVEL
    value: 'info'
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: namma-database-credentials
        key: connection_string
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 6
  targetCPUUtilizationPercentage: 70
```

#### Dedicated Kubernetes RBAC ServiceAccount & RoleBinding Manifest:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: audit-service-sa
  namespace: namma-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: audit-service-role
  namespace: namma-prod
rules:
- apiGroups: ['']
  resources: ['configmaps']
  verbs: ['get', 'watch', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: audit-service-rb
  namespace: namma-prod
subjects:
- kind: ServiceAccount
  name: audit-service-sa
  namespace: namma-prod
roleRef:
  kind: Role
  name: audit-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

## 06. Continuous Integration & GitOps Continuous Delivery Architecture
Automated CI/CD pipeline spanning GitHub Actions, Harbor Container Registry, and ArgoCD:
```yaml
# .github/workflows/deploy-production.yaml
name: Production Deployment Pipeline
on:
  push:
    branches: [main]
    tags: ['v*.*.*']
jobs:
  test-and-build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Run Unit & Integration Tests
      run: npm run test:all
    - name: Run Architecture Fitness Tests
      run: python scripts/validate_srs_architecture.py
    - name: Build & Sign Container Images
      run: |
        docker build -t ecr.ap-south-1.amazonaws.com/namma/consultation:${{ github.sha }} .
        cosign sign --key env://COSIGN_KEY ecr.ap-south-1.amazonaws.com/namma/consultation:${{ github.sha }}
  gitops-sync:
    needs: test-and-build
    runs-on: ubuntu-latest
    steps:
    - name: Update GitOps Repository Image Digest
      run: |
        git clone https://github.com/bbmp-health/namma-gitops.git
        cd namma-gitops
        sed -i 's/tag:.*/tag: ${{ github.sha }}/' environments/prod/values.yaml
        git commit -am 'chore(release): promote ${{ github.sha }} to production'
        git push origin main
```

## 07. Zero-Touch Provisioning (ZTP) Execution & TPM 2.0 Attestation Workflow
Complete factory onboarding automation script deployed on Intel N100 edge appliances:
```bash
#!/bin/bash
# /usr/local/bin/namma-ztp-enroll
set -euo pipefail

echo '=== Namma Clinic Edge Appliance Zero-Touch Enrollment ==='
CHIP_SERIAL=$(tpm2_getcap properties-fixed | grep -A 1 'TPM2_PT_MANUFACTURER' | tail -n 1 | awk '{print $2}')
DEVICE_UUID=$(cat /sys/class/dmi/id/product_uuid)
echo "Device UUID: ${DEVICE_UUID}, TPM Manufacturer: ${CHIP_SERIAL}"

# 1. Generate TPM 2.0 Endorsement Key (EK) and Attestation Quote
tpm2_createek -c ek.ctx -G rsa -u ek.pub
tpm2_createak -C ek.ctx -c ak.ctx -G rsa -u ak.pub -n ak.name
tpm2_quote -c ak.ctx -l sha256:0,1,2,3,4,5,6,7 -q 12345678 -m quote.bin -s sig.bin

# 2. Submit Enrollment Payload to Central ZTP Registry
ENROLL_RESP=$(curl -s -X POST https://ztp.nammahealth.bbmp.gov.in/v1/enroll \
  -H 'Content-Type: application/json' \
  -d "{\"device_uuid\":\"${DEVICE_UUID}\",\"quote\":\"$(base64 -w0 quote.bin)\",\"sig\":\"$(base64 -w0 sig.bin)\"}")

CLINIC_ID=$(echo "${ENROLL_RESP}" | jq -r '.clinic_id')
echo "Device enrolled successfully as Clinic ID: ${CLINIC_ID}"

# 3. Download and Install Issued Device Client Certificate
echo "${ENROLL_RESP}" | jq -r '.client_certificate' > /etc/ssl/certs/namma-device.crt
echo "${ENROLL_RESP}" | jq -r '.ca_chain' > /etc/ssl/certs/namma-ca-chain.crt
chmod 600 /etc/ssl/certs/namma-device.crt

# 4. Initialize Local SQLite Database and Start Edge Services
docker compose -f /opt/namma/docker-compose.yml up -d
echo '=== Zero-Touch Commissioning Complete ==='
```

## 08. Blue/Green Zero-Downtime Release Runbook & Analysis Template
Argo Rollouts automated canary analysis template and emergency rollback runbook:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate-and-latency
  namespace: namma-prod
spec:
  metrics:
  - name: success-rate
    interval: 60s
    successCondition: result[0] >= 0.999
    failureLimit: 2
    provider:
      prometheus:
        address: http://prometheus-k8s.monitoring:9090
        query: |
          sum(rate(http_requests_total{status!~'5..',app='consultation-preview'}[2m]))
          /
          sum(rate(http_requests_total{app='consultation-preview'}[2m]))
  - name: p95-latency
    interval: 60s
    successCondition: result[0] <= 0.250
    failureLimit: 2
    provider:
      prometheus:
        address: http://prometheus-k8s.monitoring:9090
        query: |
          histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{app='consultation-preview'}[2m])) by (le))
```

## 09. Deployment Architecture Fitness Tests & Quality Gate Checklist
Automated CI/CD validation gates ensuring zero deployment configuration drift:

### 07.1 Automated Architecture Fitness Tests
1. **Container Image Signature Verification Gate:** Admission controller (Kyverno / Cosign) rejects any container image not cryptographically signed by the BBMP CI pipeline key.
2. **Non-Root User Enforcement Gate:** CI linter verifies that all Dockerfiles and Kubernetes pod manifests enforce `runAsNonRoot: true` and non-zero UID.
3. **Resource Requests & Limits Mandatory Gate:** Helm lint fails if any Kubernetes container deployment omits explicit CPU and memory requests and limits.
4. **Edge ZTP Attestation Test:** Nightly automated integration test spins up virtual QEMU edge appliance with vTPM 2.0; asserts successful enrollment in < 10 minutes.
5. **Blue/Green Rollout Verification:** Pipeline simulates traffic shift during synthetic load test; asserts zero HTTP 5xx responses during switchover.

### 09.2 Deployment Quality Gate Checklist Matrix
| Verification Item | Automated Verification Command | Acceptance Threshold | Enforcement Gate |
| :--- | :--- | :---: | :---: |
| Container Cryptographic Signature | `cosign verify --key cosign.pub $IMAGE` | Valid signature verified | Kubernetes Admission Webhook |
| Helm Chart Syntax & Values | `helm lint charts/namma-platform` | 0 errors, 0 warnings | PR Merge Blocker |
| CIS Benchmark OS Compliance | `inspec exec https://github.com/dev-sec/linux-baseline` | Score >= 95.0% | Edge Image Build Gate |
| Zero SSH Root Access | `ssh -o BatchMode=yes root@clinic.local` | Connection rejected | Automated Security Scan |
| Blue/Green Rollout Success | `kubectl argo rollouts status rollout/consultation` | Status: Healthy | Production Deployment Gate |

## 10. Multi-Zone Disaster Recovery Network Topology & BGP Anycast Routing
Global traffic management and metropolitan network routing specifications:

### 10.1 Route53 DNS Failover & Health Checking Specification
```json
{
  "HealthCheckConfig": {
    "IPAddress": "203.0.113.10",
    "Port": 443,
    "Type": "HTTPS",
    "ResourcePath": "/health/liveness",
    "FullyQualifiedDomainName": "primary.api.nammahealth.bbmp.gov.in",
    "RequestInterval": 10,
    "FailureThreshold": 2
  }
}
```

### 10.2 Linux Auditd Security Invariant Rules (`/etc/audit/rules.d/99-namma.rules`)
```ini
# Monitor unauthorized changes to system time
-a always,exit -F arch=b64 -S adjtimex -S settimeofday -k time-change
-a always,exit -F arch=b64 -S clock_settime -k time-change
-w /etc/localtime -p wa -k time-change

# Monitor unauthorized modifications to user accounts and passwords
-w /etc/group -p wa -k identity
-w /etc/passwd -p wa -k identity
-w /etc/gshadow -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/security/opasswd -p wa -k identity

# Monitor network configuration changes
-a always,exit -F arch=b64 -S sethostname -S setdomainname -k system-locale
-w /etc/issue -p wa -k system-locale
-w /etc/issue.net -p wa -k system-locale
-w /etc/hosts -p wa -k system-locale
-w /etc/network -p wa -k system-locale

# Lock audit configuration preventing runtime changes
-e 2
```

### 10.3 TPM 2.0 LUKS Disk Encryption Setup Protocol
```bash
# Format NVMe data partition with LUKS2 encryption
cryptsetup luksFormat --type luks2 --cipher aes-xts-plain64 --key-size 512 /dev/nvme0n1p3

# Bind LUKS keyslot to hardware TPM 2.0 PCR registers (0: Firmware, 2: Extended ROM, 7: Secure Boot)
systemd-cryptenroll /dev/nvme0n1p3 --tpm2-device=auto --tpm2-pcrs=0+2+7

# Verify crypttab binding for automatic hardware-attested unlock
echo 'namma_data /dev/nvme0n1p3 none tpm2-device=auto' >> /etc/crypttab
```
