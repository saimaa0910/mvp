# 📦 Architecture Document 03: Container Architecture Specification (C4 Level 2)
## Namma Clinic Digital Health & Operations Platform
### Greater Bengaluru Authority (GBA) / BBMP Health Department
**Standard:** C4 Model / ISO/IEC/IEEE 42010:2022 | **Status:** APPROVED BASELINE | **Code:** `ARCH-CONT-03`

---

## 01. Document Scope & Container Decomposition Principles
This document establishes the canonical engineering specification for the 18 primary software containers comprising the Namma Clinic Digital Health & Operations Platform. In accordance with the C4 model (Level 2), each container represents an independently deployable runtime, execution unit, data store, or client application with dedicated operational responsibilities, network boundaries, storage backends, and failure characteristics.

### 01.1 Container Architectural Principles
1. **Edge-Cloud Runtime Duality:** Critical patient-facing containers are compiled and optimized to execute both within the central Kubernetes cloud cluster and directly on local clinic edge appliances.
2. **Explicit Interface Contracts:** Every inter-container interaction occurs via strictly typed gRPC service definitions, versioned RESTful JSON endpoints, or asynchronous event streams.
3. **Bounded Data Ownership:** Containers maintain strict data sovereignty; cross-domain queries must utilize published APIs or CDC analytical replicas rather than cross-database table joins.
4. **Fault Isolation & Blast Radius Containment:** Container failure shall never cascade across trust boundaries; downstream clients degrade gracefully using circuit breakers and local fallback queues.
5. **Autonomous Liveness & Health Probes:** Every container exposes standardized `/healthz` (liveness) and `/readyz` (readiness) HTTP endpoints evaluated continuously by orchestration daemons.

## 02. Master Container Topology & Classification Matrix (18 Containers)
Exhaustive catalog of the 18 platform containers defining architectural categories, technology implementations, primary datastores, and deployment tiers:

| Container ID | Container Name | Architectural Category | Technology Stack | Deployment Tier | Primary Data Store | Target Availability SLA | Associated Modules |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| `ARCH-CONT-001` | **Clinic Workstation PWA Shell** | Frontend Client | `Next.js / TypeScript / React / TailwindCSS` | Local Workstation / Tablet | `IndexedDB / SQLite Edge` | 99.9% | `MODULE-001..026` |
| `ARCH-CONT-002` | **Clinic Edge Mini-Server Runtime** | Edge Computing Node | `Node.js / Express / Bun / SQLite WAL` | Clinic Edge Appliance (Intel N100) | `SQLite WAL Mode (Local SSD)` | 99.9% | `MODULE-027, MODULE-028` |
| `ARCH-CONT-003` | **Central Cloud API Gateway** | Ingress & Routing | `Envoy / NGINX / Kong` | Cloud Ingress Tier | `Redis Token Cache` | 99.9% | `MODULE-001, MODULE-005` |
| `ARCH-CONT-004` | **Identity & Access Management (IAM) Service** | Security & Auth | `Node.js / Passport / Argon2id / JOSE` | Cloud App Tier / Edge Mirror | `PostgreSQL `auth_users`` | 99.9% | `MODULE-001, MODULE-005` |
| `ARCH-CONT-005` | **Master Patient Index (MPI) Service** | Patient Domain | `NestJS / Fastify / TypeScript` | Cloud App Tier / Edge Sync | `PostgreSQL `patients`` | 99.9% | `MODULE-007, MODULE-008` |
| `ARCH-CONT-006` | **Queue Orchestration & Triage Engine** | Workflow Domain | `Go / MQTT / WebSockets` | Edge Mini-Server / Cloud Sync | `Edge SQLite `clinic_queues`` | 99.9% | `MODULE-009, MODULE-010, MODULE-011` |
| `ARCH-CONT-007` | **Clinical Consultation & EMR Service** | Clinical Domain | `NestJS / Prisma / TypeScript` | Cloud App Tier / Edge Sync | `PostgreSQL `clinical_encounters`` | 99.9% | `MODULE-013, MODULE-014` |
| `ARCH-CONT-008` | **Electronic Prescription & CDSS Service** | Clinical Domain | `NestJS / Rule Engine / TypeScript` | Cloud App Tier / Edge Sync | `PostgreSQL `prescriptions`` | 99.9% | `MODULE-014, MODULE-015` |
| `ARCH-CONT-009` | **Pharmacy Inventory & Dispensation Service** | Logistics Domain | `NestJS / TypeScript` | Cloud App Tier / Edge Sync | `PostgreSQL `pharmacy_batches`` | 99.9% | `MODULE-019..022` |
| `ARCH-CONT-010` | **Diagnostic Laboratory Service** | Diagnostics Domain | `NestJS / TypeScript` | Cloud App Tier / Edge Sync | `PostgreSQL `lab_orders`` | 99.9% | `MODULE-016` |
| `ARCH-CONT-011` | **Referral & EMS Telemetry Bridge** | Care Continuity | `NestJS / REST Gateway` | Cloud App Tier | `PostgreSQL `referrals`` | 99.9% | `MODULE-017` |
| `ARCH-CONT-012` | **Citizen Portal & Multilingual Notification Service** | Citizen Domain | `Node.js / BullMQ / Redis` | Cloud App Tier | `Redis Queue / PostgreSQL` | 99.9% | `MODULE-023, MODULE-024` |
| `ARCH-CONT-013` | **Bi-directional Edge-Cloud Synchronization Service** | Sync Engine | `Go / gRPC / Vector Clocks` | Edge Node & Cloud Worker | `SQLite Mutation Log` | 99.99% | `MODULE-028` |
| `ARCH-CONT-014` | **ABDM & National Health Grid Bridge** | Interoperability | `Java / Spring Boot / HAPI FHIR` | Cloud DMZ Tier | `PostgreSQL `abdm_artifacts`` | 99.9% | `MODULE-029` |
| `ARCH-CONT-015` | **Public Health Analytics & Syndromic BI Service** | Analytics Domain | `Python / ClickHouse / Apache Superset` | Cloud Analytics Tier | `ClickHouse Star Schema` | 99.9% | `MODULE-030` |
| `ARCH-CONT-016` | **Advisory Clinical AI Decision Support Engine** | AI / ML Tier | `Python / FastAPI / ONNX Runtime` | Cloud Analytics Tier | `Model Registry (MLflow)` | 99.9% | `MODULE-015, MODULE-030` |
| `ARCH-CONT-017` | **Cryptographic WORM Audit Service** | Audit & Security | `Go / SHA-256 HMAC / Logstash` | Isolated Cloud Security Subnet | `Encrypted Object Store` | 99.9% | `MODULE-004, MODULE-005` |
| `ARCH-CONT-018` | **Enterprise Relational Database Cluster** | Data Tier | `PostgreSQL 16 Multi-AZ with Patroni` | Private Cloud Database Subnet | `NVMe SSD SAN Storage` | 99.9% | `ALL MODULES` |

## 03. Granular Container Engineering Specifications (18 Containers)
Comprehensive technical blueprints, interface contracts, failure handling, and operational profiles for every container:

### 03.01 `ARCH-CONT-001`: Clinic Workstation PWA Shell
- **Container Identifier:** `ARCH-CONT-001`
- **Formal Architectural Category:** Frontend Client
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Local Workstation / Tablet
- **Runtime Technology Implementation:** `Next.js / TypeScript / React / TailwindCSS`
- **Primary Data Store:** `IndexedDB / SQLite Edge`
- **Associated Platform Modules:** `MODULE-001..026`

#### 03.01.1 Purpose & Domain Scope
The `ARCH-CONT-001` (Clinic Workstation PWA Shell) container operates as the authoritative runtime for provides responsive touch-first workstation interface for doctors, nurses, pharmacists, and lab techs with offline caching and hardware scanner/printer access. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.01.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-001..026`.
3. Manages persistent storage interactions with `IndexedDB / SQLite Edge` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.01.3 Internal Sub-Component Architecture
The `ARCH-CONT-001` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-001`: Clinic Workstation PWA Shell Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-002`: Clinic Workstation PWA Shell Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-003`: Clinic Workstation PWA Shell Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.01.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateClinicWorkstationPWAShellCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateClinicWorkstationPWAShellCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`ClinicWorkstationPWAShellResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0001",
  "containerId": "ARCH-CONT-001",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.clinic.workstation.pwa.shell.v1`

#### 03.01.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `CLINIC_WORKSTATION_PWA_SHELL_INITIALIZED`, `CLINIC_WORKSTATION_PWA_SHELL_MUTATED`, `CLINIC_WORKSTATION_PWA_SHELL_COMPLETED`.

#### 03.01.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.01.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.01.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.01.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_001.operation`
- **Prometheus Request Counter:** `arch_cont_001_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_001_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_001_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.01.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-001`, `SRS-NFR-002`, and `BR-002`.
- **Associated Workflows:** Co-executes `WF-002` and `WF-009`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-001`, `PLANNED-API-001`, and `PLANNED-TEST-001`.

---

### 03.02 `ARCH-CONT-002`: Clinic Edge Mini-Server Runtime
- **Container Identifier:** `ARCH-CONT-002`
- **Formal Architectural Category:** Edge Computing Node
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Clinic Edge Appliance (Intel N100)
- **Runtime Technology Implementation:** `Node.js / Express / Bun / SQLite WAL`
- **Primary Data Store:** `SQLite WAL Mode (Local SSD)`
- **Associated Platform Modules:** `MODULE-027, MODULE-028`

#### 03.02.1 Purpose & Domain Scope
The `ARCH-CONT-002` (Clinic Edge Mini-Server Runtime) container operates as the authoritative runtime for hosts local clinic database, mqtt queue broker, and vector clock sync engine, ensuring 72h autonomous operation. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.02.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-027, MODULE-028`.
3. Manages persistent storage interactions with `SQLite WAL Mode (Local SSD)` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.02.3 Internal Sub-Component Architecture
The `ARCH-CONT-002` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-004`: Clinic Edge Mini-Server Runtime Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-005`: Clinic Edge Mini-Server Runtime Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-006`: Clinic Edge Mini-Server Runtime Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.02.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateClinicEdgeMini-ServerRuntimeCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateClinicEdgeMini-ServerRuntimeCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`ClinicEdgeMini-ServerRuntimeResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0002",
  "containerId": "ARCH-CONT-002",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.clinic.edge.mini-server.runtime.v1`

#### 03.02.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `CLINIC_EDGE_MINI-SERVER_RUNTIME_INITIALIZED`, `CLINIC_EDGE_MINI-SERVER_RUNTIME_MUTATED`, `CLINIC_EDGE_MINI-SERVER_RUNTIME_COMPLETED`.

#### 03.02.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.02.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.02.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.02.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_002.operation`
- **Prometheus Request Counter:** `arch_cont_002_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_002_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_002_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.02.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-002`, `SRS-NFR-003`, and `BR-003`.
- **Associated Workflows:** Co-executes `WF-003` and `WF-010`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-002`, `PLANNED-API-002`, and `PLANNED-TEST-002`.

---

### 03.03 `ARCH-CONT-003`: Central Cloud API Gateway
- **Container Identifier:** `ARCH-CONT-003`
- **Formal Architectural Category:** Ingress & Routing
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Cloud Ingress Tier
- **Runtime Technology Implementation:** `Envoy / NGINX / Kong`
- **Primary Data Store:** `Redis Token Cache`
- **Associated Platform Modules:** `MODULE-001, MODULE-005`

#### 03.03.1 Purpose & Domain Scope
The `ARCH-CONT-003` (Central Cloud API Gateway) container operates as the authoritative runtime for handles tls termination, rate limiting, jwt token validation, mtls routing, and request correlation tracing. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.03.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-001, MODULE-005`.
3. Manages persistent storage interactions with `Redis Token Cache` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.03.3 Internal Sub-Component Architecture
The `ARCH-CONT-003` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-007`: Central Cloud API Gateway Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-008`: Central Cloud API Gateway Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-009`: Central Cloud API Gateway Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.03.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateCentralCloudAPIGatewayCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateCentralCloudAPIGatewayCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`CentralCloudAPIGatewayResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0003",
  "containerId": "ARCH-CONT-003",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.central.cloud.api.gateway.v1`

#### 03.03.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `CENTRAL_CLOUD_API_GATEWAY_INITIALIZED`, `CENTRAL_CLOUD_API_GATEWAY_MUTATED`, `CENTRAL_CLOUD_API_GATEWAY_COMPLETED`.

#### 03.03.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.03.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.03.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.03.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_003.operation`
- **Prometheus Request Counter:** `arch_cont_003_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_003_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_003_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.03.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-003`, `SRS-NFR-004`, and `BR-004`.
- **Associated Workflows:** Co-executes `WF-004` and `WF-011`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-003`, `PLANNED-API-003`, and `PLANNED-TEST-003`.

---

### 03.04 `ARCH-CONT-004`: Identity & Access Management (IAM) Service
- **Container Identifier:** `ARCH-CONT-004`
- **Formal Architectural Category:** Security & Auth
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Cloud App Tier / Edge Mirror
- **Runtime Technology Implementation:** `Node.js / Passport / Argon2id / JOSE`
- **Primary Data Store:** `PostgreSQL `auth_users``
- **Associated Platform Modules:** `MODULE-001, MODULE-005`

#### 03.04.1 Purpose & Domain Scope
The `ARCH-CONT-004` (Identity & Access Management (IAM) Service) container operates as the authoritative runtime for issues and verifies cryptographic staff jwt tokens, manages rbac/abac role permissions, and coordinates session invalidation. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.04.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-001, MODULE-005`.
3. Manages persistent storage interactions with `PostgreSQL `auth_users`` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.04.3 Internal Sub-Component Architecture
The `ARCH-CONT-004` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-010`: Identity & Access Management (IAM) Service Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-011`: Identity & Access Management (IAM) Service Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-012`: Identity & Access Management (IAM) Service Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.04.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateIdentityAndAccessManagement(IAM)ServiceCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateIdentityAndAccessManagement(IAM)ServiceCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`IdentityAndAccessManagement(IAM)ServiceResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0004",
  "containerId": "ARCH-CONT-004",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.identity.and.access.management.(iam).service.v1`

#### 03.04.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `IDENTITY_AND_ACCESS_MANAGEMENT_(IAM)_SERVICE_INITIALIZED`, `IDENTITY_AND_ACCESS_MANAGEMENT_(IAM)_SERVICE_MUTATED`, `IDENTITY_AND_ACCESS_MANAGEMENT_(IAM)_SERVICE_COMPLETED`.

#### 03.04.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.04.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.04.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.04.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_004.operation`
- **Prometheus Request Counter:** `arch_cont_004_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_004_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_004_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.04.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-004`, `SRS-NFR-005`, and `BR-005`.
- **Associated Workflows:** Co-executes `WF-005` and `WF-012`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-004`, `PLANNED-API-004`, and `PLANNED-TEST-004`.

---

### 03.05 `ARCH-CONT-005`: Master Patient Index (MPI) Service
- **Container Identifier:** `ARCH-CONT-005`
- **Formal Architectural Category:** Patient Domain
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Cloud App Tier / Edge Sync
- **Runtime Technology Implementation:** `NestJS / Fastify / TypeScript`
- **Primary Data Store:** `PostgreSQL `patients``
- **Associated Platform Modules:** `MODULE-007, MODULE-008`

#### 03.05.1 Purpose & Domain Scope
The `ARCH-CONT-005` (Master Patient Index (MPI) Service) container operates as the authoritative runtime for manages citizen demographic profiles, phonetic fuzzy search, deduplication logic, and abha national id bindings. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.05.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-007, MODULE-008`.
3. Manages persistent storage interactions with `PostgreSQL `patients`` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.05.3 Internal Sub-Component Architecture
The `ARCH-CONT-005` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-013`: Master Patient Index (MPI) Service Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-014`: Master Patient Index (MPI) Service Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-015`: Master Patient Index (MPI) Service Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.05.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateMasterPatientIndex(MPI)ServiceCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateMasterPatientIndex(MPI)ServiceCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`MasterPatientIndex(MPI)ServiceResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0005",
  "containerId": "ARCH-CONT-005",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.master.patient.index.(mpi).service.v1`

#### 03.05.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `MASTER_PATIENT_INDEX_(MPI)_SERVICE_INITIALIZED`, `MASTER_PATIENT_INDEX_(MPI)_SERVICE_MUTATED`, `MASTER_PATIENT_INDEX_(MPI)_SERVICE_COMPLETED`.

#### 03.05.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.05.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.05.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.05.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_005.operation`
- **Prometheus Request Counter:** `arch_cont_005_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_005_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_005_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.05.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-005`, `SRS-NFR-006`, and `BR-006`.
- **Associated Workflows:** Co-executes `WF-006` and `WF-013`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-005`, `PLANNED-API-005`, and `PLANNED-TEST-005`.

---

### 03.06 `ARCH-CONT-006`: Queue Orchestration & Triage Engine
- **Container Identifier:** `ARCH-CONT-006`
- **Formal Architectural Category:** Workflow Domain
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Edge Mini-Server / Cloud Sync
- **Runtime Technology Implementation:** `Go / MQTT / WebSockets`
- **Primary Data Store:** `Edge SQLite `clinic_queues``
- **Associated Platform Modules:** `MODULE-009, MODULE-010, MODULE-011`

#### 03.06.1 Purpose & Domain Scope
The `ARCH-CONT-006` (Queue Orchestration & Triage Engine) container operates as the authoritative runtime for maintains multi-room priority queues, calculates mews vitals scores, and broadcasts token calls to waiting hall tvs. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.06.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-009, MODULE-010, MODULE-011`.
3. Manages persistent storage interactions with `Edge SQLite `clinic_queues`` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.06.3 Internal Sub-Component Architecture
The `ARCH-CONT-006` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-016`: Queue Orchestration & Triage Engine Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-017`: Queue Orchestration & Triage Engine Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-018`: Queue Orchestration & Triage Engine Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.06.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateQueueOrchestrationAndTriageEngineCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateQueueOrchestrationAndTriageEngineCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`QueueOrchestrationAndTriageEngineResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0006",
  "containerId": "ARCH-CONT-006",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.queue.orchestration.and.triage.engine.v1`

#### 03.06.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `QUEUE_ORCHESTRATION_AND_TRIAGE_ENGINE_INITIALIZED`, `QUEUE_ORCHESTRATION_AND_TRIAGE_ENGINE_MUTATED`, `QUEUE_ORCHESTRATION_AND_TRIAGE_ENGINE_COMPLETED`.

#### 03.06.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.06.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.06.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.06.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_006.operation`
- **Prometheus Request Counter:** `arch_cont_006_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_006_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_006_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.06.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-006`, `SRS-NFR-007`, and `BR-007`.
- **Associated Workflows:** Co-executes `WF-007` and `WF-014`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-006`, `PLANNED-API-006`, and `PLANNED-TEST-006`.

---

### 03.07 `ARCH-CONT-007`: Clinical Consultation & EMR Service
- **Container Identifier:** `ARCH-CONT-007`
- **Formal Architectural Category:** Clinical Domain
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Cloud App Tier / Edge Sync
- **Runtime Technology Implementation:** `NestJS / Prisma / TypeScript`
- **Primary Data Store:** `PostgreSQL `clinical_encounters``
- **Associated Platform Modules:** `MODULE-013, MODULE-014`

#### 03.07.1 Purpose & Domain Scope
The `ARCH-CONT-007` (Clinical Consultation & EMR Service) container operates as the authoritative runtime for captures soap clinical progress notes, snomed ct / icd-10 diagnostic coding, and longitudinal medical history. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.07.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-013, MODULE-014`.
3. Manages persistent storage interactions with `PostgreSQL `clinical_encounters`` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.07.3 Internal Sub-Component Architecture
The `ARCH-CONT-007` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-019`: Clinical Consultation & EMR Service Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-020`: Clinical Consultation & EMR Service Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-021`: Clinical Consultation & EMR Service Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.07.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateClinicalConsultationAndEMRServiceCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateClinicalConsultationAndEMRServiceCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`ClinicalConsultationAndEMRServiceResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0007",
  "containerId": "ARCH-CONT-007",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.clinical.consultation.and.emr.service.v1`

#### 03.07.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `CLINICAL_CONSULTATION_AND_EMR_SERVICE_INITIALIZED`, `CLINICAL_CONSULTATION_AND_EMR_SERVICE_MUTATED`, `CLINICAL_CONSULTATION_AND_EMR_SERVICE_COMPLETED`.

#### 03.07.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.07.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.07.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.07.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_007.operation`
- **Prometheus Request Counter:** `arch_cont_007_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_007_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_007_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.07.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-007`, `SRS-NFR-008`, and `BR-008`.
- **Associated Workflows:** Co-executes `WF-008` and `WF-015`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-007`, `PLANNED-API-007`, and `PLANNED-TEST-007`.

---

### 03.08 `ARCH-CONT-008`: Electronic Prescription & CDSS Service
- **Container Identifier:** `ARCH-CONT-008`
- **Formal Architectural Category:** Clinical Domain
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Cloud App Tier / Edge Sync
- **Runtime Technology Implementation:** `NestJS / Rule Engine / TypeScript`
- **Primary Data Store:** `PostgreSQL `prescriptions``
- **Associated Platform Modules:** `MODULE-014, MODULE-015`

#### 03.08.1 Purpose & Domain Scope
The `ARCH-CONT-008` (Electronic Prescription & CDSS Service) container operates as the authoritative runtime for enforces formulary rules, evaluates drug-drug interactions, checks pediatric dosage boundaries, and signs e-prescriptions. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.08.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-014, MODULE-015`.
3. Manages persistent storage interactions with `PostgreSQL `prescriptions`` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.08.3 Internal Sub-Component Architecture
The `ARCH-CONT-008` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-022`: Electronic Prescription & CDSS Service Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-023`: Electronic Prescription & CDSS Service Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-024`: Electronic Prescription & CDSS Service Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.08.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateElectronicPrescriptionAndCDSSServiceCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateElectronicPrescriptionAndCDSSServiceCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`ElectronicPrescriptionAndCDSSServiceResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0008",
  "containerId": "ARCH-CONT-008",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.electronic.prescription.and.cdss.service.v1`

#### 03.08.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `ELECTRONIC_PRESCRIPTION_AND_CDSS_SERVICE_INITIALIZED`, `ELECTRONIC_PRESCRIPTION_AND_CDSS_SERVICE_MUTATED`, `ELECTRONIC_PRESCRIPTION_AND_CDSS_SERVICE_COMPLETED`.

#### 03.08.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.08.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.08.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.08.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_008.operation`
- **Prometheus Request Counter:** `arch_cont_008_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_008_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_008_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.08.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-008`, `SRS-NFR-009`, and `BR-009`.
- **Associated Workflows:** Co-executes `WF-009` and `WF-016`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-008`, `PLANNED-API-008`, and `PLANNED-TEST-008`.

---

### 03.09 `ARCH-CONT-009`: Pharmacy Inventory & Dispensation Service
- **Container Identifier:** `ARCH-CONT-009`
- **Formal Architectural Category:** Logistics Domain
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Cloud App Tier / Edge Sync
- **Runtime Technology Implementation:** `NestJS / TypeScript`
- **Primary Data Store:** `PostgreSQL `pharmacy_batches``
- **Associated Platform Modules:** `MODULE-019..022`

#### 03.09.1 Purpose & Domain Scope
The `ARCH-CONT-009` (Pharmacy Inventory & Dispensation Service) container operates as the authoritative runtime for enforces fefo batch allocation, verifies 2d datamatrix scans, tracks cold-chain storage, and manages depot indenting. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.09.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-019..022`.
3. Manages persistent storage interactions with `PostgreSQL `pharmacy_batches`` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.09.3 Internal Sub-Component Architecture
The `ARCH-CONT-009` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-025`: Pharmacy Inventory & Dispensation Service Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-026`: Pharmacy Inventory & Dispensation Service Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-027`: Pharmacy Inventory & Dispensation Service Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.09.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreatePharmacyInventoryAndDispensationServiceCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreatePharmacyInventoryAndDispensationServiceCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`PharmacyInventoryAndDispensationServiceResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0009",
  "containerId": "ARCH-CONT-009",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.pharmacy.inventory.and.dispensation.service.v1`

#### 03.09.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `PHARMACY_INVENTORY_AND_DISPENSATION_SERVICE_INITIALIZED`, `PHARMACY_INVENTORY_AND_DISPENSATION_SERVICE_MUTATED`, `PHARMACY_INVENTORY_AND_DISPENSATION_SERVICE_COMPLETED`.

#### 03.09.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.09.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.09.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.09.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_009.operation`
- **Prometheus Request Counter:** `arch_cont_009_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_009_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_009_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.09.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-009`, `SRS-NFR-010`, and `BR-010`.
- **Associated Workflows:** Co-executes `WF-010` and `WF-017`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-009`, `PLANNED-API-009`, and `PLANNED-TEST-009`.

---

### 03.10 `ARCH-CONT-010`: Diagnostic Laboratory Service
- **Container Identifier:** `ARCH-CONT-010`
- **Formal Architectural Category:** Diagnostics Domain
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Cloud App Tier / Edge Sync
- **Runtime Technology Implementation:** `NestJS / TypeScript`
- **Primary Data Store:** `PostgreSQL `lab_orders``
- **Associated Platform Modules:** `MODULE-016`

#### 03.10.1 Purpose & Domain Scope
The `ARCH-CONT-010` (Diagnostic Laboratory Service) container operates as the authoritative runtime for manages test orders for 58 rapid diagnostic tests, specimen chain-of-custody, and critical panic value escalations. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.10.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-016`.
3. Manages persistent storage interactions with `PostgreSQL `lab_orders`` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.10.3 Internal Sub-Component Architecture
The `ARCH-CONT-010` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-028`: Diagnostic Laboratory Service Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-029`: Diagnostic Laboratory Service Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-030`: Diagnostic Laboratory Service Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.10.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateDiagnosticLaboratoryServiceCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateDiagnosticLaboratoryServiceCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`DiagnosticLaboratoryServiceResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0010",
  "containerId": "ARCH-CONT-010",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.diagnostic.laboratory.service.v1`

#### 03.10.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `DIAGNOSTIC_LABORATORY_SERVICE_INITIALIZED`, `DIAGNOSTIC_LABORATORY_SERVICE_MUTATED`, `DIAGNOSTIC_LABORATORY_SERVICE_COMPLETED`.

#### 03.10.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.10.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.10.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.10.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_010.operation`
- **Prometheus Request Counter:** `arch_cont_010_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_010_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_010_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.10.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-010`, `SRS-NFR-011`, and `BR-011`.
- **Associated Workflows:** Co-executes `WF-011` and `WF-018`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-010`, `PLANNED-API-010`, and `PLANNED-TEST-010`.

---

### 03.11 `ARCH-CONT-011`: Referral & EMS Telemetry Bridge
- **Container Identifier:** `ARCH-CONT-011`
- **Formal Architectural Category:** Care Continuity
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Cloud App Tier
- **Runtime Technology Implementation:** `NestJS / REST Gateway`
- **Primary Data Store:** `PostgreSQL `referrals``
- **Associated Platform Modules:** `MODULE-017`

#### 03.11.1 Purpose & Domain Scope
The `ARCH-CONT-011` (Referral & EMS Telemetry Bridge) container operates as the authoritative runtime for assembles clinical referral dossiers, coordinates 108 ambulance dispatch, and tracks secondary hospital counter-referrals. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.11.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-017`.
3. Manages persistent storage interactions with `PostgreSQL `referrals`` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.11.3 Internal Sub-Component Architecture
The `ARCH-CONT-011` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-031`: Referral & EMS Telemetry Bridge Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-032`: Referral & EMS Telemetry Bridge Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-033`: Referral & EMS Telemetry Bridge Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.11.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateReferralAndEMSTelemetryBridgeCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateReferralAndEMSTelemetryBridgeCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`ReferralAndEMSTelemetryBridgeResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0011",
  "containerId": "ARCH-CONT-011",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.referral.and.ems.telemetry.bridge.v1`

#### 03.11.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `REFERRAL_AND_EMS_TELEMETRY_BRIDGE_INITIALIZED`, `REFERRAL_AND_EMS_TELEMETRY_BRIDGE_MUTATED`, `REFERRAL_AND_EMS_TELEMETRY_BRIDGE_COMPLETED`.

#### 03.11.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.11.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.11.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.11.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_011.operation`
- **Prometheus Request Counter:** `arch_cont_011_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_011_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_011_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.11.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-011`, `SRS-NFR-012`, and `BR-012`.
- **Associated Workflows:** Co-executes `WF-012` and `WF-019`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-011`, `PLANNED-API-011`, and `PLANNED-TEST-011`.

---

### 03.12 `ARCH-CONT-012`: Citizen Portal & Multilingual Notification Service
- **Container Identifier:** `ARCH-CONT-012`
- **Formal Architectural Category:** Citizen Domain
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Cloud App Tier
- **Runtime Technology Implementation:** `Node.js / BullMQ / Redis`
- **Primary Data Store:** `Redis Queue / PostgreSQL`
- **Associated Platform Modules:** `MODULE-023, MODULE-024`

#### 03.12.1 Purpose & Domain Scope
The `ARCH-CONT-012` (Citizen Portal & Multilingual Notification Service) container operates as the authoritative runtime for dispatches bilingual sms/whatsapp appointment reminders, recall notices, and operates self-service kiosk tokens. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.12.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-023, MODULE-024`.
3. Manages persistent storage interactions with `Redis Queue / PostgreSQL` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.12.3 Internal Sub-Component Architecture
The `ARCH-CONT-012` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-034`: Citizen Portal & Multilingual Notification Service Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-035`: Citizen Portal & Multilingual Notification Service Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-036`: Citizen Portal & Multilingual Notification Service Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.12.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateCitizenPortalAndMultilingualNotificationServiceCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateCitizenPortalAndMultilingualNotificationServiceCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`CitizenPortalAndMultilingualNotificationServiceResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0012",
  "containerId": "ARCH-CONT-012",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.citizen.portal.and.multilingual.notification.service.v1`

#### 03.12.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `CITIZEN_PORTAL_AND_MULTILINGUAL_NOTIFICATION_SERVICE_INITIALIZED`, `CITIZEN_PORTAL_AND_MULTILINGUAL_NOTIFICATION_SERVICE_MUTATED`, `CITIZEN_PORTAL_AND_MULTILINGUAL_NOTIFICATION_SERVICE_COMPLETED`.

#### 03.12.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.12.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.12.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.12.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_012.operation`
- **Prometheus Request Counter:** `arch_cont_012_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_012_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_012_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.12.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-012`, `SRS-NFR-013`, and `BR-013`.
- **Associated Workflows:** Co-executes `WF-013` and `WF-020`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-012`, `PLANNED-API-012`, and `PLANNED-TEST-012`.

---

### 03.13 `ARCH-CONT-013`: Bi-directional Edge-Cloud Synchronization Service
- **Container Identifier:** `ARCH-CONT-013`
- **Formal Architectural Category:** Sync Engine
- **Target Availability SLA:** 99.99% uptime
- **Physical Deployment Tier:** Edge Node & Cloud Worker
- **Runtime Technology Implementation:** `Go / gRPC / Vector Clocks`
- **Primary Data Store:** `SQLite Mutation Log`
- **Associated Platform Modules:** `MODULE-028`

#### 03.13.1 Purpose & Domain Scope
The `ARCH-CONT-013` (Bi-directional Edge-Cloud Synchronization Service) container operates as the authoritative runtime for executes asynchronous delta synchronization, crdt conflict resolution, and bandwidth-throttled replay. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.13.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-028`.
3. Manages persistent storage interactions with `SQLite Mutation Log` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.13.3 Internal Sub-Component Architecture
The `ARCH-CONT-013` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-037`: Bi-directional Edge-Cloud Synchronization Service Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-038`: Bi-directional Edge-Cloud Synchronization Service Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-039`: Bi-directional Edge-Cloud Synchronization Service Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.13.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateBi-directionalEdge-CloudSynchronizationServiceCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateBi-directionalEdge-CloudSynchronizationServiceCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`Bi-directionalEdge-CloudSynchronizationServiceResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0013",
  "containerId": "ARCH-CONT-013",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.bi-directional.edge-cloud.synchronization.service.v1`

#### 03.13.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `BI-DIRECTIONAL_EDGE-CLOUD_SYNCHRONIZATION_SERVICE_INITIALIZED`, `BI-DIRECTIONAL_EDGE-CLOUD_SYNCHRONIZATION_SERVICE_MUTATED`, `BI-DIRECTIONAL_EDGE-CLOUD_SYNCHRONIZATION_SERVICE_COMPLETED`.

#### 03.13.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.13.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.13.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.13.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_013.operation`
- **Prometheus Request Counter:** `arch_cont_013_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_013_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_013_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.13.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-013`, `SRS-NFR-014`, and `BR-014`.
- **Associated Workflows:** Co-executes `WF-014` and `WF-021`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-013`, `PLANNED-API-013`, and `PLANNED-TEST-013`.

---

### 03.14 `ARCH-CONT-014`: ABDM & National Health Grid Bridge
- **Container Identifier:** `ARCH-CONT-014`
- **Formal Architectural Category:** Interoperability
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Cloud DMZ Tier
- **Runtime Technology Implementation:** `Java / Spring Boot / HAPI FHIR`
- **Primary Data Store:** `PostgreSQL `abdm_artifacts``
- **Associated Platform Modules:** `MODULE-029`

#### 03.14.1 Purpose & Domain Scope
The `ARCH-CONT-014` (ABDM & National Health Grid Bridge) container operates as the authoritative runtime for transforms clinical records into fhir r4 bundles for abdm m1 (abha), m2 (hip publishing), and m3 (hiu consent). It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.14.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-029`.
3. Manages persistent storage interactions with `PostgreSQL `abdm_artifacts`` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.14.3 Internal Sub-Component Architecture
The `ARCH-CONT-014` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-040`: ABDM & National Health Grid Bridge Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-041`: ABDM & National Health Grid Bridge Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-042`: ABDM & National Health Grid Bridge Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.14.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateABDMAndNationalHealthGridBridgeCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateABDMAndNationalHealthGridBridgeCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`ABDMAndNationalHealthGridBridgeResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0014",
  "containerId": "ARCH-CONT-014",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.abdm.and.national.health.grid.bridge.v1`

#### 03.14.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `ABDM_AND_NATIONAL_HEALTH_GRID_BRIDGE_INITIALIZED`, `ABDM_AND_NATIONAL_HEALTH_GRID_BRIDGE_MUTATED`, `ABDM_AND_NATIONAL_HEALTH_GRID_BRIDGE_COMPLETED`.

#### 03.14.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.14.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.14.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.14.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_014.operation`
- **Prometheus Request Counter:** `arch_cont_014_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_014_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_014_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.14.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-014`, `SRS-NFR-015`, and `BR-015`.
- **Associated Workflows:** Co-executes `WF-015` and `WF-022`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-014`, `PLANNED-API-014`, and `PLANNED-TEST-014`.

---

### 03.15 `ARCH-CONT-015`: Public Health Analytics & Syndromic BI Service
- **Container Identifier:** `ARCH-CONT-015`
- **Formal Architectural Category:** Analytics Domain
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Cloud Analytics Tier
- **Runtime Technology Implementation:** `Python / ClickHouse / Apache Superset`
- **Primary Data Store:** `ClickHouse Star Schema`
- **Associated Platform Modules:** `MODULE-030`

#### 03.15.1 Purpose & Domain Scope
The `ARCH-CONT-015` (Public Health Analytics & Syndromic BI Service) container operates as the authoritative runtime for aggregates ward-level disease prevalence, stock burn-down, and syndromic fever surveillance for municipal officers. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.15.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-030`.
3. Manages persistent storage interactions with `ClickHouse Star Schema` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.15.3 Internal Sub-Component Architecture
The `ARCH-CONT-015` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-043`: Public Health Analytics & Syndromic BI Service Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-044`: Public Health Analytics & Syndromic BI Service Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-045`: Public Health Analytics & Syndromic BI Service Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.15.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreatePublicHealthAnalyticsAndSyndromicBIServiceCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreatePublicHealthAnalyticsAndSyndromicBIServiceCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`PublicHealthAnalyticsAndSyndromicBIServiceResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0015",
  "containerId": "ARCH-CONT-015",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.public.health.analytics.and.syndromic.bi.service.v1`

#### 03.15.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `PUBLIC_HEALTH_ANALYTICS_AND_SYNDROMIC_BI_SERVICE_INITIALIZED`, `PUBLIC_HEALTH_ANALYTICS_AND_SYNDROMIC_BI_SERVICE_MUTATED`, `PUBLIC_HEALTH_ANALYTICS_AND_SYNDROMIC_BI_SERVICE_COMPLETED`.

#### 03.15.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.15.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.15.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.15.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_015.operation`
- **Prometheus Request Counter:** `arch_cont_015_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_015_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_015_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.15.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-015`, `SRS-NFR-016`, and `BR-016`.
- **Associated Workflows:** Co-executes `WF-016` and `WF-023`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-015`, `PLANNED-API-015`, and `PLANNED-TEST-015`.

---

### 03.16 `ARCH-CONT-016`: Advisory Clinical AI Decision Support Engine
- **Container Identifier:** `ARCH-CONT-016`
- **Formal Architectural Category:** AI / ML Tier
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Cloud Analytics Tier
- **Runtime Technology Implementation:** `Python / FastAPI / ONNX Runtime`
- **Primary Data Store:** `Model Registry (MLflow)`
- **Associated Platform Modules:** `MODULE-015, MODULE-030`

#### 03.16.1 Purpose & Domain Scope
The `ARCH-CONT-016` (Advisory Clinical AI Decision Support Engine) container operates as the authoritative runtime for provides advisory syndromic clustering alerts and non-autonomous medication interaction predictions. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.16.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-015, MODULE-030`.
3. Manages persistent storage interactions with `Model Registry (MLflow)` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.16.3 Internal Sub-Component Architecture
The `ARCH-CONT-016` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-046`: Advisory Clinical AI Decision Support Engine Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-047`: Advisory Clinical AI Decision Support Engine Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-048`: Advisory Clinical AI Decision Support Engine Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.16.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateAdvisoryClinicalAIDecisionSupportEngineCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateAdvisoryClinicalAIDecisionSupportEngineCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`AdvisoryClinicalAIDecisionSupportEngineResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0016",
  "containerId": "ARCH-CONT-016",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.advisory.clinical.ai.decision.support.engine.v1`

#### 03.16.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `ADVISORY_CLINICAL_AI_DECISION_SUPPORT_ENGINE_INITIALIZED`, `ADVISORY_CLINICAL_AI_DECISION_SUPPORT_ENGINE_MUTATED`, `ADVISORY_CLINICAL_AI_DECISION_SUPPORT_ENGINE_COMPLETED`.

#### 03.16.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.16.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.16.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.16.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_016.operation`
- **Prometheus Request Counter:** `arch_cont_016_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_016_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_016_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.16.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-016`, `SRS-NFR-017`, and `BR-017`.
- **Associated Workflows:** Co-executes `WF-017` and `WF-024`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-016`, `PLANNED-API-016`, and `PLANNED-TEST-016`.

---

### 03.17 `ARCH-CONT-017`: Cryptographic WORM Audit Service
- **Container Identifier:** `ARCH-CONT-017`
- **Formal Architectural Category:** Audit & Security
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Isolated Cloud Security Subnet
- **Runtime Technology Implementation:** `Go / SHA-256 HMAC / Logstash`
- **Primary Data Store:** `Encrypted Object Store`
- **Associated Platform Modules:** `MODULE-004, MODULE-005`

#### 03.17.1 Purpose & Domain Scope
The `ARCH-CONT-017` (Cryptographic WORM Audit Service) container operates as the authoritative runtime for maintains an immutable append-only audit trail with cryptographic hash chaining conforming to dpdp act 2023. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.17.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `MODULE-004, MODULE-005`.
3. Manages persistent storage interactions with `Encrypted Object Store` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.17.3 Internal Sub-Component Architecture
The `ARCH-CONT-017` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-049`: Cryptographic WORM Audit Service Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-050`: Cryptographic WORM Audit Service Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-051`: Cryptographic WORM Audit Service Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.17.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateCryptographicWORMAuditServiceCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateCryptographicWORMAuditServiceCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`CryptographicWORMAuditServiceResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0017",
  "containerId": "ARCH-CONT-017",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.cryptographic.worm.audit.service.v1`

#### 03.17.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `CRYPTOGRAPHIC_WORM_AUDIT_SERVICE_INITIALIZED`, `CRYPTOGRAPHIC_WORM_AUDIT_SERVICE_MUTATED`, `CRYPTOGRAPHIC_WORM_AUDIT_SERVICE_COMPLETED`.

#### 03.17.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.17.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.17.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.17.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_017.operation`
- **Prometheus Request Counter:** `arch_cont_017_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_017_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_017_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.17.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-017`, `SRS-NFR-018`, and `BR-018`.
- **Associated Workflows:** Co-executes `WF-018` and `WF-025`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-017`, `PLANNED-API-017`, and `PLANNED-TEST-017`.

---

### 03.18 `ARCH-CONT-018`: Enterprise Relational Database Cluster
- **Container Identifier:** `ARCH-CONT-018`
- **Formal Architectural Category:** Data Tier
- **Target Availability SLA:** 99.9% uptime
- **Physical Deployment Tier:** Private Cloud Database Subnet
- **Runtime Technology Implementation:** `PostgreSQL 16 Multi-AZ with Patroni`
- **Primary Data Store:** `NVMe SSD SAN Storage`
- **Associated Platform Modules:** `ALL MODULES`

#### 03.18.1 Purpose & Domain Scope
The `ARCH-CONT-018` (Enterprise Relational Database Cluster) container operates as the authoritative runtime for authoritative central transactional database with streaming physical replication and table partitioning. It encapsulates all domain services, validation logic, and hardware abstraction layers required to fulfill its operational mandate across both connected cloud and disconnected clinic environments.

#### 03.18.2 Core Engineering Responsibilities
1. Enforces strict input validation against declarative schemas for all inbound traffic before execution.
2. Executes core business invariants and ACID state transitions corresponding to `ALL MODULES`.
3. Manages persistent storage interactions with `NVMe SSD SAN Storage` using connection pooling and optimistic concurrency.
4. Implements local fallback caching, ensuring operational continuity during upstream dependency outages.
5. Emits distributed tracing spans conforming to OpenTelemetry semantic conventions with correlation propagation.
6. Emits standardized Prometheus metrics tracking request rates, execution latencies, and error counters.
7. Produces immutable WORM audit event entries with SHA-256 HMAC signatures for all state-altering mutations.
8. Dispatches domain event notifications to the local MQTT broker and central Kafka message stream.
9. Enforces least-privilege role-based access control (RBAC) on every inbound endpoint.
10. Participates in automated health checking via `/healthz` and `/readyz` endpoints.

#### 03.18.3 Internal Sub-Component Architecture
The `ARCH-CONT-018` container decomposes internally into three discrete architectural components:
1. **`ARCH-COMP-052`: Enterprise Relational Database Cluster Ingress Controller & Validation Handler**
   - Handles TLS 1.3 termination, parses incoming JSON/gRPC payloads, enforces authentication headers, and executes JSON Schema DTO validation.
   - Returns RFC 7807 Problem Details immediately upon parameter malformation or missing correlation IDs.
2. **`ARCH-COMP-053`: Enterprise Relational Database Cluster Core Domain Business Service**
   - Implements transactional business logic, entity state machines, domain invariants, and cross-aggregate business rules.
   - Manages ACID transaction boundaries with pessimistic locking or optimistic timestamp checks.
3. **`ARCH-COMP-054`: Enterprise Relational Database Cluster Persistence & Integration Adapter**
   - Encapsulates database queries, object-relational mappings, local cache queries, and outbound message bus publishing.
   - Implements retry policies and circuit breaker fallbacks for all external input/output operations.

#### 03.18.4 Interface Contracts, DTO Schemas & Protocols
- **Primary Inbound Protocol:** HTTPS REST (TLS 1.3) / gRPC (HTTP/2) with mandatory `X-Correlation-ID` header.
- **Inbound Command DTO Schema (`CreateEnterpriseRelationalDatabaseClusterCommandDTO`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateEnterpriseRelationalDatabaseClusterCommandDTO",
  "type": "object",
  "properties": {
    "transactionId": { "type": "string", "format": "uuid" },
    "clinicId": { "type": "string", "pattern": "^BBMP-CLN-[0-9]{3}$" },
    "operatorId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  },
  "required": ["transactionId", "clinicId", "operatorId", "timestamp", "payload"]
}
```
- **Outbound Response Envelope DTO (`EnterpriseRelationalDatabaseClusterResponseEnvelopeDTO`):**
```json
{
  "status": "SUCCESS",
  "correlationId": "corr-uuidv7-0018",
  "containerId": "ARCH-CONT-018",
  "data": { "result": "COMMITTED" },
  "error": null
}
```
- **Internal Message Bus Topic:** `namma.events.enterprise.relational.database.cluster.v1`

#### 03.18.5 Inputs, Validations & Outbound Emissions
- **Input Constraints:** Enforces non-null checks, regex field patterns, ISO-8601 UTC date validation, and UUIDv7 format validation.
- **Sanitization Pipeline:** Automated XSS filtering and SQL injection prevention via parameterized prepared statements.
- **Domain Events Emitted:** `ENTERPRISE_RELATIONAL_DATABASE_CLUSTER_INITIALIZED`, `ENTERPRISE_RELATIONAL_DATABASE_CLUSTER_MUTATED`, `ENTERPRISE_RELATIONAL_DATABASE_CLUSTER_COMPLETED`.

#### 03.18.6 Security Boundary & Trust Perimeters
- **Network Enclave:** Operates within isolated container namespace with strict egress firewall filtering.
- **Authentication Requirement:** Cryptographic Bearer JWT token validated against IAM RS256 public key.
- **Authorization Strategy:** Fine-grained capability evaluation based on `ROLE-001` through `ROLE-030` claims.
- **Data Protection Invariants:** Zero plaintext storage of PHI attributes; AES-256 GCM envelope encryption.
- **Logging Sanitization:** Automated regex scrubber strips citizen names, Aadhaar, and phone numbers from logs.

#### 03.18.7 Failure Modes, Circuit Breaking & Self-Healing
- **Upstream Outage Handling:** Trips Resilience4j circuit breaker if downstream error rate exceeds 50% over 50 requests.
- **Retry Backoff Strategy:** Exponential backoff with jitter (Initial: 250ms, Factor: 2.0, Max: 10s, Max Retries: 3).
- **Dead-Letter Queue (DLQ):** Failed asynchronous events routed to dedicated Kafka DLQ topic for operational triage.
- **Local Edge Autonomy:** Automatically redirects persistent storage writes to local SQLite WAL database during WAN outages.
- **Self-Healing Runbook:** Kubernetes ReplicaSet automatically recreates crashed pods within 15 seconds.

#### 03.18.8 Scaling Model & Resource Limits
- **Base Resource Allocation:** Memory: 512MiB request / 1024MiB limit; CPU: 250m request / 1000m limit.
- **Horizontal Pod Autoscaling (HPA):** Scales between 2 and 10 replicas when average CPU exceeds 70% or memory exceeds 80%.
- **Connection Pool Sizing:** Dedicated HikariCP / pgBouncer pool (Max connections: 25, Min idle: 5, Timeout: 30s).
- **Edge Appliance Tuning:** Compiled as lightweight single-process runtime consuming < 80MB RAM on Intel N100 mini-PC.

#### 03.18.9 Observability, Metrics & Telemetry Spans
- **OpenTelemetry Trace Span:** `span.arch_cont_018.operation`
- **Prometheus Request Counter:** `arch_cont_018_requests_total{status="success|failure"}`
- **Prometheus Duration Histogram:** `arch_cont_018_duration_seconds{le="0.1|0.25|0.5|1.0|2.5"}`
- **Active Connections Gauge:** `arch_cont_018_active_connections`
- **Structured Log Format:** JSON logs conforming to Elastic Common Schema (ECS) with embedded `trace_id`.

#### 03.18.10 Upstream & Downstream Traceability
- **Upstream Requirements:** Fulfills `SRS-FR-018`, `SRS-NFR-019`, and `BR-019`.
- **Associated Workflows:** Co-executes `WF-019` and `WF-001`.
- **Downstream Planned Artifacts:** Traces to `PLANNED-CONTAINER-018`, `PLANNED-API-018`, and `PLANNED-TEST-018`.

---

## 04. Container Interaction & Cross-Communication Matrix
Detailed mapping of inter-container communication channels, protocols, and data payloads across the platform:

| Calling Container ID | Target Container ID | Interaction Purpose | Communication Protocol | Payload Format | Authentication Scheme | Circuit Breaker Policy |
| :---: | :---: | :--- | :--- | :--- | :--- | :--- |
| `ARCH-CONT-001` | `ARCH-CONT-002` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-001` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-002` | `ARCH-CONT-003` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-002` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-003` | `ARCH-CONT-004` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-003` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-004` | `ARCH-CONT-005` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-004` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-005` | `ARCH-CONT-006` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-005` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-006` | `ARCH-CONT-007` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-006` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-007` | `ARCH-CONT-008` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-007` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-008` | `ARCH-CONT-009` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-008` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-009` | `ARCH-CONT-010` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-009` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-010` | `ARCH-CONT-011` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-010` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-011` | `ARCH-CONT-012` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-011` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-012` | `ARCH-CONT-013` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-012` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-013` | `ARCH-CONT-014` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-013` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-014` | `ARCH-CONT-015` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-014` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-015` | `ARCH-CONT-016` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-015` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-016` | `ARCH-CONT-017` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-016` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-017` | `ARCH-CONT-018` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-017` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |
| `ARCH-CONT-018` | `ARCH-CONT-001` | Inter-container state synchronization and domain command dispatch | gRPC over HTTP/2 | Protocol Buffers | Mutual TLS + JWT Bearer Token | 50% failure trip; 10s sleep |
| `ARCH-CONT-018` | `ARCH-CONT-018` | Transactional data persistence and entity state query | PostgreSQL Wire Protocol | Parameterized SQL | Scram-SHA-256 + TLS 1.3 | PgBouncer pool retry |

## 05. Comprehensive Container Kubernetes & Edge Appliance Sizing Specification
Resource quotas, autoscaling parameters, persistent storage volumes, and probe configurations across all 18 containers:

| Container ID | Container Name | CPU Req/Limit | RAM Req/Limit | Storage Volume / PVC | HPA Min/Max | Ingress Port | Liveness Probe Path |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `ARCH-CONT-001` | **Clinic Workstation PWA Shell** | 250m / 1000m | 512Mi / 1024Mi | 10Gi gp3 | 3 / 15 pods | `8001` | `GET /healthz` |
| `ARCH-CONT-002` | **Clinic Edge Mini-Server Runtime** | 250m / 1000m | 512Mi / 1024Mi | 100Gi NVMe | 2 / 6 pods | `8002` | `GET /healthz` |
| `ARCH-CONT-003` | **Central Cloud API Gateway** | 250m / 1000m | 512Mi / 1024Mi | 10Gi gp3 | 3 / 15 pods | `8003` | `GET /healthz` |
| `ARCH-CONT-004` | **Identity & Access Management (IAM) Service** | 500m / 2000m | 1024Mi / 2048Mi | 10Gi gp3 | 2 / 6 pods | `8004` | `GET /healthz` |
| `ARCH-CONT-005` | **Master Patient Index (MPI) Service** | 250m / 1000m | 512Mi / 1024Mi | 10Gi gp3 | 3 / 15 pods | `8005` | `GET /healthz` |
| `ARCH-CONT-006` | **Queue Orchestration & Triage Engine** | 250m / 1000m | 512Mi / 1024Mi | 10Gi gp3 | 2 / 6 pods | `8006` | `GET /healthz` |
| `ARCH-CONT-007` | **Clinical Consultation & EMR Service** | 500m / 2000m | 1024Mi / 2048Mi | 10Gi gp3 | 3 / 15 pods | `8007` | `GET /healthz` |
| `ARCH-CONT-008` | **Electronic Prescription & CDSS Service** | 250m / 1000m | 512Mi / 1024Mi | 10Gi gp3 | 2 / 6 pods | `8008` | `GET /healthz` |
| `ARCH-CONT-009` | **Pharmacy Inventory & Dispensation Service** | 250m / 1000m | 512Mi / 1024Mi | 10Gi gp3 | 3 / 15 pods | `8009` | `GET /healthz` |
| `ARCH-CONT-010` | **Diagnostic Laboratory Service** | 250m / 1000m | 512Mi / 1024Mi | 10Gi gp3 | 2 / 6 pods | `8010` | `GET /healthz` |
| `ARCH-CONT-011` | **Referral & EMS Telemetry Bridge** | 250m / 1000m | 512Mi / 1024Mi | 10Gi gp3 | 2 / 6 pods | `8011` | `GET /healthz` |
| `ARCH-CONT-012` | **Citizen Portal & Multilingual Notification Service** | 250m / 1000m | 512Mi / 1024Mi | 10Gi gp3 | 2 / 6 pods | `8012` | `GET /healthz` |
| `ARCH-CONT-013` | **Bi-directional Edge-Cloud Synchronization Service** | 500m / 2000m | 1024Mi / 2048Mi | 10Gi gp3 | 2 / 6 pods | `8013` | `GET /healthz` |
| `ARCH-CONT-014` | **ABDM & National Health Grid Bridge** | 250m / 1000m | 512Mi / 1024Mi | 10Gi gp3 | 2 / 6 pods | `8014` | `GET /healthz` |
| `ARCH-CONT-015` | **Public Health Analytics & Syndromic BI Service** | 250m / 1000m | 1024Mi / 2048Mi | 10Gi gp3 | 2 / 6 pods | `8015` | `GET /healthz` |
| `ARCH-CONT-016` | **Advisory Clinical AI Decision Support Engine** | 250m / 1000m | 512Mi / 1024Mi | 10Gi gp3 | 2 / 6 pods | `8016` | `GET /healthz` |
| `ARCH-CONT-017` | **Cryptographic WORM Audit Service** | 250m / 1000m | 512Mi / 1024Mi | 100Gi NVMe | 2 / 6 pods | `8017` | `GET /healthz` |
| `ARCH-CONT-018` | **Enterprise Relational Database Cluster** | 500m / 2000m | 1024Mi / 2048Mi | 100Gi NVMe | 2 / 6 pods | `8018` | `GET /healthz` |

## 06. Detailed Inter-Container Call Topology & Latency Budgets (18 Containers)
Exhaustive call topologies, latency SLA boundaries, and downstream failure isolations for each container:

### 06.01 Call Topology for `ARCH-CONT-001` (Clinic Workstation PWA Shell)
- **Originating Container:** `ARCH-CONT-001` | **Primary Downstream Dependency:** `ARCH-CONT-002`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_001`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.02 Call Topology for `ARCH-CONT-002` (Clinic Edge Mini-Server Runtime)
- **Originating Container:** `ARCH-CONT-002` | **Primary Downstream Dependency:** `ARCH-CONT-003`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_002`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.03 Call Topology for `ARCH-CONT-003` (Central Cloud API Gateway)
- **Originating Container:** `ARCH-CONT-003` | **Primary Downstream Dependency:** `ARCH-CONT-004`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_003`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.04 Call Topology for `ARCH-CONT-004` (Identity & Access Management (IAM) Service)
- **Originating Container:** `ARCH-CONT-004` | **Primary Downstream Dependency:** `ARCH-CONT-005`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_004`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.05 Call Topology for `ARCH-CONT-005` (Master Patient Index (MPI) Service)
- **Originating Container:** `ARCH-CONT-005` | **Primary Downstream Dependency:** `ARCH-CONT-006`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_005`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.06 Call Topology for `ARCH-CONT-006` (Queue Orchestration & Triage Engine)
- **Originating Container:** `ARCH-CONT-006` | **Primary Downstream Dependency:** `ARCH-CONT-007`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_006`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.07 Call Topology for `ARCH-CONT-007` (Clinical Consultation & EMR Service)
- **Originating Container:** `ARCH-CONT-007` | **Primary Downstream Dependency:** `ARCH-CONT-008`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_007`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.08 Call Topology for `ARCH-CONT-008` (Electronic Prescription & CDSS Service)
- **Originating Container:** `ARCH-CONT-008` | **Primary Downstream Dependency:** `ARCH-CONT-009`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_008`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.09 Call Topology for `ARCH-CONT-009` (Pharmacy Inventory & Dispensation Service)
- **Originating Container:** `ARCH-CONT-009` | **Primary Downstream Dependency:** `ARCH-CONT-010`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_009`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.10 Call Topology for `ARCH-CONT-010` (Diagnostic Laboratory Service)
- **Originating Container:** `ARCH-CONT-010` | **Primary Downstream Dependency:** `ARCH-CONT-011`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_010`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.11 Call Topology for `ARCH-CONT-011` (Referral & EMS Telemetry Bridge)
- **Originating Container:** `ARCH-CONT-011` | **Primary Downstream Dependency:** `ARCH-CONT-012`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_011`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.12 Call Topology for `ARCH-CONT-012` (Citizen Portal & Multilingual Notification Service)
- **Originating Container:** `ARCH-CONT-012` | **Primary Downstream Dependency:** `ARCH-CONT-013`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_012`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.13 Call Topology for `ARCH-CONT-013` (Bi-directional Edge-Cloud Synchronization Service)
- **Originating Container:** `ARCH-CONT-013` | **Primary Downstream Dependency:** `ARCH-CONT-014`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_013`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.14 Call Topology for `ARCH-CONT-014` (ABDM & National Health Grid Bridge)
- **Originating Container:** `ARCH-CONT-014` | **Primary Downstream Dependency:** `ARCH-CONT-015`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_014`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.15 Call Topology for `ARCH-CONT-015` (Public Health Analytics & Syndromic BI Service)
- **Originating Container:** `ARCH-CONT-015` | **Primary Downstream Dependency:** `ARCH-CONT-016`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_015`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.16 Call Topology for `ARCH-CONT-016` (Advisory Clinical AI Decision Support Engine)
- **Originating Container:** `ARCH-CONT-016` | **Primary Downstream Dependency:** `ARCH-CONT-017`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_016`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.17 Call Topology for `ARCH-CONT-017` (Cryptographic WORM Audit Service)
- **Originating Container:** `ARCH-CONT-017` | **Primary Downstream Dependency:** `ARCH-CONT-018`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_017`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.18 Call Topology for `ARCH-CONT-018` (Enterprise Relational Database Cluster)
- **Originating Container:** `ARCH-CONT-018` | **Primary Downstream Dependency:** `ARCH-CONT-001`
- **Direct Call Protocol:** gRPC over HTTP/2 with mTLS mutual certificate authentication.
- **Contracted Latency Budget:** Interactive calls must return in < 45ms (p95); background sync calls < 250ms.
- **Downstream Circuit Breaker:** Trips to OPEN state upon 5 consecutive connection timeouts; returns RFC 7807 fallback.
- **Database Persistence Channel:** Dedicated connection pool to `ARCH-CONT-018` with 25 maximum connections.
- **Event Bus Emission:** Publishes state transitions to Kafka topic `namma.events.arch_cont_018`.
- **Trace Context Propagation:** Injects W3C `traceparent` and `tracestate` headers into all outbound HTTP/gRPC requests.

### 06.1 Detailed Step-by-Step Sequence Flows for Core Container Operations
Execution lifecycle tracing request reception, validation, mutation, and persistence across all 18 containers:

#### 06.1.01 Operational Lifecycle: `ARCH-CONT-001` (Clinic Workstation PWA Shell)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `IndexedDB / SQLite Edge`.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.02 Operational Lifecycle: `ARCH-CONT-002` (Clinic Edge Mini-Server Runtime)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `SQLite WAL Mode (Local SSD)`.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.03 Operational Lifecycle: `ARCH-CONT-003` (Central Cloud API Gateway)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `Redis Token Cache`.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.04 Operational Lifecycle: `ARCH-CONT-004` (Identity & Access Management (IAM) Service)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `PostgreSQL `auth_users``.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.05 Operational Lifecycle: `ARCH-CONT-005` (Master Patient Index (MPI) Service)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `PostgreSQL `patients``.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.06 Operational Lifecycle: `ARCH-CONT-006` (Queue Orchestration & Triage Engine)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `Edge SQLite `clinic_queues``.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.07 Operational Lifecycle: `ARCH-CONT-007` (Clinical Consultation & EMR Service)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `PostgreSQL `clinical_encounters``.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.08 Operational Lifecycle: `ARCH-CONT-008` (Electronic Prescription & CDSS Service)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `PostgreSQL `prescriptions``.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.09 Operational Lifecycle: `ARCH-CONT-009` (Pharmacy Inventory & Dispensation Service)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `PostgreSQL `pharmacy_batches``.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.10 Operational Lifecycle: `ARCH-CONT-010` (Diagnostic Laboratory Service)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `PostgreSQL `lab_orders``.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.11 Operational Lifecycle: `ARCH-CONT-011` (Referral & EMS Telemetry Bridge)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `PostgreSQL `referrals``.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.12 Operational Lifecycle: `ARCH-CONT-012` (Citizen Portal & Multilingual Notification Service)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `Redis Queue / PostgreSQL`.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.13 Operational Lifecycle: `ARCH-CONT-013` (Bi-directional Edge-Cloud Synchronization Service)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `SQLite Mutation Log`.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.14 Operational Lifecycle: `ARCH-CONT-014` (ABDM & National Health Grid Bridge)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `PostgreSQL `abdm_artifacts``.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.15 Operational Lifecycle: `ARCH-CONT-015` (Public Health Analytics & Syndromic BI Service)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `ClickHouse Star Schema`.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.16 Operational Lifecycle: `ARCH-CONT-016` (Advisory Clinical AI Decision Support Engine)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `Model Registry (MLflow)`.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.17 Operational Lifecycle: `ARCH-CONT-017` (Cryptographic WORM Audit Service)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `Encrypted Object Store`.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

#### 06.1.18 Operational Lifecycle: `ARCH-CONT-018` (Enterprise Relational Database Cluster)
1. **Ingress & Handshake:** Client connects via TLS 1.3; container validates JWT bearer token and extracts `clinic_id` claim.
2. **Schema & Rule Gate:** Ingress controller executes declarative DTO validation and verifies correlation ID existence.
3. **Domain Transaction:** Domain service executes business logic within an explicit transactional boundary on `NVMe SSD SAN Storage`.
4. **Persistence & Journal:** Mutation is committed to disk, local vector clock increments, and delta journals to sync engine.
5. **Telemetry & Audit Emission:** OpenTelemetry span closes, Prometheus counter increments, and WORM audit record is sealed.

## 07. Container Verification & Quality Gates
Mandatory testing and deployment validation gates enforced for all 18 containers:
1. **Zero-Vulnerability Base Images:** Every container image must pass automated Trivy and Snyk scans in CI with zero High or Critical CVEs.
2. **Non-Root Execution:** All containers must enforce non-root user execution (`USER 10001`) with read-only root filesystems.
3. **Contract Verification:** All gRPC and REST endpoints must possess automated Pact contract verification tests.
4. **Graceful Termination:** Containers must handle `SIGTERM` signals cleanly, draining active connections within 30 seconds before exiting.
