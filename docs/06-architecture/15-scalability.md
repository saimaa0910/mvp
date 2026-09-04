# ⚡ Architecture Document 15: Enterprise Scalability, Capacity Planning & Performance Engineering Specification
## Namma Clinic Digital Health & Operations Platform
### Greater Bengaluru Authority (GBA) / BBMP Health Department
**Standard:** Cloud Native Scalability / High Concurrency / Capacity Planning | **Status:** APPROVED BASELINE | **Code:** `ARCH-SCALE-15`

---

## 01. Document Overview & Scalability Engineering Philosophy
This document specifies the enterprise scalability architecture, capacity planning models, performance engineering baselines, and stress testing benchmarks for the Namma Clinic Digital Health & Operations Platform. Spanning 183 physical health centers across 8 municipal zones in Greater Bengaluru, the platform is engineered to effortlessly absorb diurnal citizen surges, municipal immunization drives, and seasonal epidemic outbreaks without degradation of clinical response times or transactional integrity.

### 01.1 Core Scalability Axioms & Mathematical Foundations
1. **Stateless Horizontal Compute Scaling:** All application-tier microservices (NestJS, Go, Fastify) are strictly stateless, delegating persistence to distributed databases and session tokens to client JWTs / Redis, enabling linear scale-out via Kubernetes HPA.
2. **Shared-Nothing Edge Independence:** Clinic edge appliances operate as autonomous compute islands; a spike in registrations at Clinic A (e.g. Malleshwaram) places zero computational or locking overhead on Clinic B (e.g. Whitefield).
3. **Asynchronous Non-Blocking I/O:** Heavy background workflows (ABDM care context publishing, SMS dispatch, ClickHouse analytics CDC, WORM audit verification) are decoupled from interactive clinical request paths via Apache Kafka event streaming.
4. **Universal Scalability Law (USL) Governance:** System concurrency is modeled using Dr. Neil Gunther's USL: `C(N) = N / (1 + \sigma(N - 1) + \kappa N(N - 1))`. Software architecture actively minimizes contention coefficient `\sigma` (via lock-free CRDTs and row-level locking) and coherency penalty `\kappa` (via read-replicas and local edge caching).
5. **Sub-Linear Cost Scaling:** Through aggressive connection pooling, columnar compression, and NVMe edge caching, infrastructure costs scale at less than 0.35x of total transactional data growth.

## 02. Comprehensive Capacity Planning Model Across 183 Clinics
Mathematical workload modeling based on authoritative municipal demographic and clinical operating parameters:

### 02.1 Operational Workload Parameters
| Metric Parameter | Primary Baseline Value | Peak Surge Multiplier | Maximum Dimensioned Capacity | Architectural Impact |
| :--- | :---: | :---: | :---: | :--- |
| **Operating Clinics** | 183 Namma Clinics | 1.25x (230 Projected) | 250 Concurrent Clinics | Scaled across 8 municipal administrative zones |
| **Daily Clinic Operating Hours** | 08:00 to 20:00 (12 Hours) | Extended during crisis | 16 Hours Continuous | Peak morning surge: 08:30 - 11:30 (45% volume) |
| **Average Daily Patient Footfall** | 120 Patients / Clinic / Day | 2.5x (Epidemic Peak) | 300 Patients / Clinic / Day | Daily municipal patient intake: 21,960 - 54,900 |
| **Concurrent Staff Users** | ~25 Staff / Clinic (4,575 Total) | 1.2x Shift Overlap | 5,500 Active Staff Sessions | Concurrent doctors, nurses, pharmacists, lab techs |
| **Average Clinical Consult Duration**| 8.5 Minutes | 4.0 Minutes (Fast Track)| 3.0 Minutes Minimum | Drives encounter creation and e-Rx write rates |
| **Prescription Lines / Encounter** | 3.2 Formulary Medications | 6.0 Lines (Polypharmacy)| 8.0 Lines Maximum | Drives pharmacy inventory decrement transactions |
| **Rapid Lab Tests / 100 Patients**| 35 Diagnostic Orders | 70 Orders (Fever Season)| 100 Orders Maximum | Generates ~7,680 - 15,370 lab panel orders/day |

### 02.2 Throughput & Transaction Rate Calculations
Calculations establishing baseline and peak requests per second (RPS) at central cloud and edge boundaries:
1. **Daily Total HTTP Requests:**
   - Patient intake, queue tokens, triage vitals, consultation drafts (autosaved every 30s), prescription safety checks, pharmacy scans, lab entries, and sync pings.
   - Baseline Daily Requests: `21,960 patients * 85 HTTP operations/patient = 1,866,600 requests/day`.
   - Edge Daemon Telemetry & Sync Heartbeats: `183 clinics * 60 pings/hour * 12 hours = 131,760 requests/day`.
   - Total Central HTTP Requests: ~2,500,000 requests per 12-hour operational day.
2. **Peak Cloud Gateway Ingress Rate:**
   - Average Rate: `2,500,000 / (12 * 3600) = 57.87 requests/second`.
   - Morning Surge Peak Multiplier: ~18x average rate during peak morning token generation and consultation sync bursts.
   - **Dimensioned Cloud API Gateway Peak:** **1,200 requests/second**.
3. **PostgreSQL Database Master Write Concurrency:**
   - Average Write Rate: `(21,960 encounters * 6 state transitions) / 43,200 sec = 3.05 writes/second`.
   - Peak Write Surge Multiplier: ~100x during edge synchronization reconnection after municipal network restoration.
   - **Dimensioned PostgreSQL Master Write Peak:** **500 write transactions/second**.

### 02.3 5-Year Data Volume & Storage Growth Projections
Storage dimensioning model accounting for raw database growth, WAL archiving, ClickHouse analytics, and immutable WORM audit logs:

| Timeline Year | Unique Citizens (MPI) | Clinical Encounters | Prescribed Medications | Diagnostic Lab Tests | WORM Audit Events | PostgreSQL Primary NVMe | ClickHouse Analytics | Cloud Object Storage | Total Storage Footprint |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Year 1 (Baseline)** | 3.5 Million | 8.0 Million | 25.6 Million | 2.8 Million | 150 Million | 120 GB | 450 GB | 1.2 TB | **1.77 TB** |
| **Year 2 (Expansion)** | 5.2 Million | 12.0 Million | 38.4 Million | 4.2 Million | 230 Million | 185 GB | 680 GB | 1.9 TB | **2.76 TB** |
| **Year 3 (Maturity)** | 6.8 Million | 16.0 Million | 51.2 Million | 5.6 Million | 310 Million | 250 GB | 910 GB | 2.5 TB | **3.66 TB** |
| **Year 4 (Integration)** | 8.1 Million | 19.5 Million | 62.4 Million | 6.8 Million | 385 Million | 310 GB | 1,120 GB | 3.1 TB | **4.53 TB** |
| **Year 5 (Full Scale)** | 9.5 Million | 23.0 Million | 73.6 Million | 8.0 Million | 460 Million | 375 GB | 1,350 GB | 3.8 TB | **5.52 TB** |

## 03. 12 Canonical Scalability Dimensions (ARCH-SCALE-001 to ARCH-SCALE-012)
Exhaustive engineering specifications for the 12 scalability dimensions governing platform elasticity:

### 03.01 Dimension Specification: `ARCH-SCALE-001` (Frontend Workstation PWA Asset Delivery & CDN Caching)
- **Dimension Identifier:** `ARCH-SCALE-001`
- **Technical Mechanism:** Cloudflare / Edge CDN + Service Worker Cache-First
- **Baseline Operating Scale:** 183 Clinics * 3 Tablets = 549 Client Nodes
- **Peak Dimensioned Scale Target:** **2,500 Concurrent Client Nodes across 250 Clinics**
- **Target Architectural Bottleneck:** Client PWA asset loading latency and bandwidth consumption on municipal broadband links.
- **Scalability Engineering Strategy:** Deploy cache-first Service Worker with immutable content-hashed bundles. CDN edge caches static JS/Wasm chunks for 365 days.
- **Performance & Scalability Outcome:** Workstation cold boot downloads < 2.5MB; subsequent reloads load instantly from CacheStorage with zero WAN bandwidth.
- **Formal Mathematical Model:** Queue Theory Model: M/M/c queue at CDN edge with c=1000 edge nodes. Zero queuing delay due to edge cache hit ratio > 99%.

#### Step-by-Step Implementation Blueprint:
1. Webpack / Vite build generates content-hashed assets (e.g. `app.018f3a5b.js`).
2. Cloudflare CDN serves assets with `Cache-Control: public, max-age=31536000, immutable`.
3. Workstation Service Worker intercepts network fetches, serving assets directly from browser CacheStorage.
4. Background update check queries `/api/v1/version` every 30 minutes; triggers silent cache refresh on version bump.
5. Pre-caches offline translation dictionaries (`kn-IN`, `en-IN`) and offline vector icons in IndexedDB.
6. Service worker implements fallback navigation route `/offline.html` if network disconnects before cache hydration.
7. BroadcastChannel API synchronizes cache invalidation across multiple browser tabs on the same workstation.
8. Performance observer reports Core Web Vitals (LCP < 1.2s, FID < 50ms, CLS < 0.05) to central telemetry.

#### Authoritative Configuration & Implementation Blueprint:
```javascript
// Workstation ServiceWorker Cache-First Strategy
const CACHE_NAME = 'namma-pwa-v1.4.2';
self.addEventListener('fetch', (event) => {
  if (event.request.mode === 'navigate') {
    event.respondWith(caches.match('/app-shell.html').then(res => res || fetch(event.request)));
    return;
  }
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) return cachedResponse;
      return fetch(event.request).then((networkResponse) => {
        if (networkResponse.status === 200 && event.request.url.includes('/assets/')) {
          const clone = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return networkResponse;
      });
    })
  );
});
```

#### Performance Testing & Benchmark Verification:
- **Benchmark Directive:** Benchmark with Chrome Lighthouse: `lighthouse https://clinic.local:8443 --preset=desktop --throttling-method=devtools` (Target Score >= 95).

---

### 03.02 Dimension Specification: `ARCH-SCALE-002` (Clinic Edge Mini-Server Local SQLite & Concurrency Model)
- **Dimension Identifier:** `ARCH-SCALE-002`
- **Technical Mechanism:** SQLite 3.45+ WAL Mode + Busy Handler + Connection Serializer
- **Baseline Operating Scale:** 3 Concurrent Workstations (10 ops/min)
- **Peak Dimensioned Scale Target:** **15 Concurrent Workstations per Clinic (60 ops/min)**
- **Target Architectural Bottleneck:** SQLite file lock contention (`SQLITE_BUSY`) during simultaneous registration, triage, and doctor writes.
- **Scalability Engineering Strategy:** Enable Write-Ahead Logging (`PRAGMA journal_mode = WAL;`) and synchronous normal (`PRAGMA synchronous = NORMAL;`). Dedicate single writer connection thread with pooled read connections.
- **Performance & Scalability Outcome:** Sustains up to 250 local write transactions/sec and 5,000 read queries/sec on Intel N100 NVMe without lock timeouts.
- **Formal Mathematical Model:** Gunther USL Model: Contention parameter sigma = 0.002, coherency kappa = 0. Near-linear scaling across all local reader threads.

#### Step-by-Step Implementation Blueprint:
1. Edge daemon initializes SQLite in WAL mode: `PRAGMA journal_mode = WAL;`.
2. Sets busy timeout to 5,000ms: `PRAGMA busy_timeout = 5000;`.
3. Configures memory mapped I/O: `PRAGMA mmap_size = 268435456;` (256MB).
4. Dedicated write worker processes write mutations sequentially from in-memory queue.
5. 4 read-only connections serve concurrent PWA query requests.
6. Periodic WAL autocheckpoint triggers when log reaches 1,000 pages: `PRAGMA wal_autocheckpoint = 1000;`.
7. SQLite temp store set to memory: `PRAGMA temp_store = MEMORY;`.
8. Prepared statement caching enabled with LRU cache capacity of 256 compiled statements.

#### Authoritative Configuration & Implementation Blueprint:
```bash
# Benchmark SQLite local concurrency
sqlite3 /opt/namma/data/clinic.db << 'EOF'
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA busy_timeout = 5000;
PRAGMA cache_size = -64000;
PRAGMA mmap_size = 268435456;
PRAGMA temp_store = MEMORY;
EOF
```

#### Performance Testing & Benchmark Verification:
- **Benchmark Directive:** Stress test: `python scripts/tests/stress_sqlite.py --workers 10 --duration 60s` (Assert 0 SQLITE_BUSY errors).

---

### 03.03 Dimension Specification: `ARCH-SCALE-003` (Cloud Ingress API Gateway Throughput & Horizontal Scaling)
- **Dimension Identifier:** `ARCH-SCALE-003`
- **Technical Mechanism:** Envoy / Kong Kubernetes Deployment + NLB Layer 4 Multiplexing
- **Baseline Operating Scale:** 150 Requests / Second (Average Morning)
- **Peak Dimensioned Scale Target:** **1,200 Requests / Second (Peak Surge)**
- **Target Architectural Bottleneck:** CPU saturation, TLS handshake overhead, and TCP connection exhaustion at cloud ingress boundary.
- **Scalability Engineering Strategy:** Deploy horizontal Envoy proxy pods across 3 availability zones behind AWS Network Load Balancer (NLB). Enable TLS session resumption and HTTP/2 multiplexing.
- **Performance & Scalability Outcome:** Maintains gateway P99 latency < 15ms under 1,500 req/sec load with zero dropped connections.
- **Formal Mathematical Model:** Queueing Model: M/M/s model where s = 6 Envoy pods. Server utilization rho = 0.55 at peak 1,200 RPS.

#### Step-by-Step Implementation Blueprint:
1. NLB distributes incoming TCP connections evenly across Envoy gateway pods in AZ-1, AZ-2, AZ-3.
2. Envoy enforces TLS 1.3 with session ticket caching, reducing handshake latency to < 5ms.
3. HTTP/2 multiplexing allows 100 concurrent API requests over single persistent TCP connection.
4. Envoy token bucket rate limiter protects backend services from rogue traffic spikes.
5. Dynamic endpoint discovery (EDS) updates routing tables as microservice pods autoscale.
6. Connection keep-alive timeouts tuned to 65 seconds to eliminate connection re-negotiation.
7. Access logging buffers asynchronously to fluent-bit daemon to prevent I/O blocking.
8. Upstream connection pools configure circuit breakers with 5,000 max pending requests.

#### Authoritative Configuration & Implementation Blueprint:
```yaml
# Envoy Gateway HPA manifest snippet
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: envoy-gateway-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: envoy-gateway
  minReplicas: 3
  maxReplicas: 12
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 65
```

#### Performance Testing & Benchmark Verification:
- **Benchmark Directive:** Execute benchmark: `k6 run --vus 500 --duration 5m tests/load/gateway_stress.js`.

---

### 03.04 Dimension Specification: `ARCH-SCALE-004` (Kubernetes Microservice Horizontal Pod Autoscaling (HPA))
- **Dimension Identifier:** `ARCH-SCALE-004`
- **Technical Mechanism:** Kubernetes HPA v2 + Custom Prometheus Metrics (KEDA)
- **Baseline Operating Scale:** 18 Replicas (1 Pod per Service Baseline)
- **Peak Dimensioned Scale Target:** **96 Replicas (Autoscaled Peak Across Services)**
- **Target Architectural Bottleneck:** Microservice CPU throttling and thread pool exhaustion during peak morning consultation hours.
- **Scalability Engineering Strategy:** Configure HPA v2 with dual metrics: CPU utilization (> 70%) and Prometheus requests-per-second (`http_requests_per_second > 100`).
- **Performance & Scalability Outcome:** Rapid scale-out: scales from 18 to 96 pods in < 90 seconds during sudden morning surge.
- **Formal Mathematical Model:** Autoscaling Dynamics: Proportional control algorithm with 15s polling interval and 300s scale-down stabilization window.

#### Step-by-Step Implementation Blueprint:
1. KEDA Prometheus scaler monitors request rate on each microservice service endpoint.
2. When request rate exceeds 100 req/sec per pod, HPA calculates required replica count.
3. Kubernetes scheduler spins up new pods; readiness probe asserts DB pool connection in < 5s.
4. Traffic immediately balances across new pods via Kubernetes ClusterIP service endpoints.
5. Node autoscaler (Karpenter) provisions additional EC2 worker instances if cluster memory saturates.
6. Pod disruption budgets (PDB) ensure minimum 75% availability during rolling cluster node upgrades.
7. Graceful shutdown hooks wait 15 seconds to allow active HTTP requests to drain before pod termination.
8. Resource limits enforce strict CPU and memory bounds to prevent 'noisy neighbor' starvation.

#### Authoritative Configuration & Implementation Blueprint:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: consultation-service-scaler
spec:
  scaleTargetRef:
    name: consultation-service
  minReplicaCount: 4
  maxReplicaCount: 16
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus-k8s.monitoring:9090
      metricName: http_requests_total
      query: sum(rate(http_requests_total{service='consultation-service'}[2m]))
      threshold: '100'
```

#### Performance Testing & Benchmark Verification:
- **Benchmark Directive:** Trigger scaling drill: `kubectl scale deployment consultation-service --replicas=1 && k6 run --vus 200 tests/load/spike.js`.

---

### 03.05 Dimension Specification: `ARCH-SCALE-005` (PostgreSQL Primary Write Capacity & Transaction Concurrency)
- **Dimension Identifier:** `ARCH-SCALE-005`
- **Technical Mechanism:** Patroni Master Node + NVMe SSD IOPS + Transaction Optimization
- **Baseline Operating Scale:** 50 Write Transactions / Second
- **Peak Dimensioned Scale Target:** **500 Write Transactions / Second (Batch Sync Replay)**
- **Target Architectural Bottleneck:** Disk I/O bottlenecks and WAL write lock contention on primary PostgreSQL cluster node.
- **Scalability Engineering Strategy:** Provision AWS `io2` Block Storage with 15,000 provisioned IOPS. Batch multiple offline sync mutations into single multi-row SQL INSERT statements.
- **Performance & Scalability Outcome:** Sustains 500 write transactions/sec with WAL commit latency < 4ms and zero lock escalation.
- **Formal Mathematical Model:** Transaction Sizing: Average write transaction size = 4.2KB. Write throughput = 2.1 MB/s, well within 500 MB/s bus capacity.

#### Step-by-Step Implementation Blueprint:
1. Database storage provisioned on 15,000 IOPS NVMe SSD volumes.
2. WAL writes committed to dedicated physical disk array preventing data table I/O contention.
3. Backend sync service aggregates edge mutation journal into multi-row batches (100 rows/statement).
4. Autovacuum tuned with `autovacuum_vacuum_cost_limit = 2000` to prevent table bloat during write surges.
5. Checkpoint parameters tuned: `checkpoint_completion_target = 0.9` and `max_wal_size = 16GB`.
6. Explicit column projections used in all write statements; zero SELECT * queries.
7. Advisory locks replace heavy row-level locking for inventory allocation counters.
8. Background unaccented phonetic indexing uses GIN indexes configured with fastupdate enabled.

#### Authoritative Configuration & Implementation Blueprint:
```sql
-- PostgreSQL primary performance configuration
ALTER SYSTEM SET shared_buffers = '16GB';
ALTER SYSTEM SET work_mem = '64MB';
ALTER SYSTEM SET maintenance_work_mem = '2GB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '64MB';
ALTER SYSTEM SET default_statistics_target = 100;
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;
```

#### Performance Testing & Benchmark Verification:
- **Benchmark Directive:** Benchmark with pgbench: `pgbench -i -s 100 namma_master && pgbench -c 50 -j 8 -T 120 namma_master`.

---

### 03.06 Dimension Specification: `ARCH-SCALE-006` (PostgreSQL Read Replica Scaling & Query Offloading)
- **Dimension Identifier:** `ARCH-SCALE-006`
- **Technical Mechanism:** Streaming Read Replicas + HAProxy Read-Write Splitting
- **Baseline Operating Scale:** 100 Read Queries / Second
- **Peak Dimensioned Scale Target:** **1,500 Read Queries / Second**
- **Target Architectural Bottleneck:** Complex search queries (Soundex MPI lookup, drug catalog lookups) degrading primary write performance.
- **Scalability Engineering Strategy:** Deploy 3 read replicas in availability zones AZ-1, AZ-2, and AZ-3. Route all SELECT queries via HAProxy read pool.
- **Performance & Scalability Outcome:** Offloads 92% of total database query volume from primary master node, maintaining replica replication lag < 10ms.
- **Formal Mathematical Model:** Amdahl's Law Speedup: S(p) = 1 / ((1 - 0.92) + (0.92 / 3)) = 2.58x theoretical speedup across 3 replicas.

#### Step-by-Step Implementation Blueprint:
1. Streaming asynchronous replication maintains 3 read replicas.
2. HAProxy listens on port 6433 (read pool) and distributes queries round-robin.
3. Backend services use separate Prisma / Knex read connection pool pointing to port 6433.
4. HAProxy health check monitors `SELECT pg_is_in_recovery();` to verify replica readiness.
5. Read replicas configure `hot_standby_feedback = on` to prevent query cancellations due to vacuuming.
6. Long-running analytical queries are isolated to a dedicated replica 03 preventing OLTP query stalls.
7. Replica replication lag is monitored continuously; nodes with lag > 1 second are temporarily drained.
8. Covering indexes (INCLUDE clause) eliminate table heap lookups for 80% of common read queries.

#### Authoritative Configuration & Implementation Blueprint:
```ini
# HAProxy Read Pool Configuration
listen postgres-read-pool
  bind *:6433
  mode tcp
  balance roundrobin
  option pgsql-check user pgbouncer
  server db-replica-01 10.240.10.101:5432 check inter 2000 rise 2 fall 3
  server db-replica-02 10.240.10.102:5432 check inter 2000 rise 2 fall 3
  server db-replica-03 10.240.10.103:5432 check inter 2000 rise 2 fall 3
```

#### Performance Testing & Benchmark Verification:
- **Benchmark Directive:** Verify read routing: `psql -h haproxy.db.internal -p 6433 -c 'SELECT pg_is_in_recovery();'` (Must return `t`).

---

### 03.07 Dimension Specification: `ARCH-SCALE-007` (PgBouncer Connection Pooling & Multiplexing)
- **Dimension Identifier:** `ARCH-SCALE-007`
- **Technical Mechanism:** PgBouncer Transaction-Mode Pooling Sidecars
- **Baseline Operating Scale:** 200 Microservice Backend Connections
- **Peak Dimensioned Scale Target:** **5,000 Virtual Connections Multiplexed to 150 Backend Connections**
- **Target Architectural Bottleneck:** PostgreSQL memory exhaustion caused by thousands of idle microservice connections (10MB RAM per backend process).
- **Scalability Engineering Strategy:** Deploy PgBouncer in `pool_mode = transaction`. Multiplex thousands of incoming client connections over a tight pool of 150 physical server connections.
- **Performance & Scalability Outcome:** Reduces PostgreSQL database memory footprint by 88% while supporting 5,000 concurrent client requests.
- **Formal Mathematical Model:** Memory Sizing: 5,000 direct connections would require 50GB RAM. PgBouncer pool requires only 1.5GB RAM for 150 server processes.

#### Step-by-Step Implementation Blueprint:
1. PgBouncer instances intercept connections from microservice pods.
2. Server connections are allocated only during active SQL transaction execution.
3. Upon transaction commit, server connection is immediately released back to pool.
4. Client connections wait in FIFO queue if all server connections are active.
5. Prepared statement support enabled via `max_prepared_statements = 100` in PgBouncer 1.21+.
6. Connection life parameters: `server_idle_timeout = 600` and `client_idle_timeout = 60`.
7. TLS termination offloaded to PgBouncer, reducing CPU load on PostgreSQL core.
8. Separate connection pools configured for OLTP workloads (`namma_oltp`) and batch jobs (`namma_batch`).

#### Authoritative Configuration & Implementation Blueprint:
```ini
[pgbouncer]
logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid
listen_addr = *
listen_port = 6432
auth_type = scram-sha-256
pool_mode = transaction
max_client_conn = 5000
default_pool_size = 50
min_pool_size = 10
reserve_pool_size = 15
reserve_pool_timeout = 5.0
max_prepared_statements = 100
```

#### Performance Testing & Benchmark Verification:
- **Benchmark Directive:** Inspect pool stats: `psql -h 127.0.0.1 -p 6432 -U pgbouncer pgbouncer -c 'SHOW POOLS;'`.

---

### 03.08 Dimension Specification: `ARCH-SCALE-008` (Kafka Event Streaming & Partition Allocation)
- **Dimension Identifier:** `ARCH-SCALE-008`
- **Technical Mechanism:** Apache Kafka 3.6+ / KRaft Mode Cluster + 16 Partitions Per Topic
- **Baseline Operating Scale:** 500 Events / Second
- **Peak Dimensioned Scale Target:** **5,000 Events / Second**
- **Target Architectural Bottleneck:** Message ingestion bottlenecks on high-volume CDC streams (`namma.cdc.encounters`) and notification queues.
- **Scalability Engineering Strategy:** Deploy 5-broker Kafka cluster with KRaft consensus. Provision 16 partitions per high-throughput topic, keyed by `clinic_id`.
- **Performance & Scalability Outcome:** Guarantees total partition ordering per clinic while enabling 16 concurrent consumer worker instances to process 5,000 events/sec.
- **Formal Mathematical Model:** Throughput Calculation: 5,000 msgs/sec * 1.5KB/msg = 7.5 MB/s uncompressed. Zstandard compression yields 1.8 MB/s wire throughput.

#### Step-by-Step Implementation Blueprint:
1. Producers publish events with `clinic_id` partition key, ensuring FIFO ordering per clinic.
2. 16 partitions per topic allow horizontal scaling of consumer group workers up to 16 pods.
3. KRaft metadata mode eliminates ZooKeeper scaling bottlenecks.
4. Segment size set to 1GB with Zstandard compression reduces network bandwidth by 75%.
5. Producer `acks=all` with `min.insync.replicas=2` guarantees zero event loss.
6. Fetch batching tuned: `fetch.min.bytes = 1024` and `fetch.max.wait.ms = 100`.
7. Log retention configured to 7 days for clinical CDC topics and 24 hours for ephemeral telemetry.
8. Consumer group lag alerts fire if lag exceeds 5,000 records for > 2 minutes.

#### Authoritative Configuration & Implementation Blueprint:
```bash
# Kafka topic provisioning with 16 partitions
kafka-topics --bootstrap-server kafka:9092 --create --topic namma.cdc.encounters \
  --partitions 16 --replication-factor 3 --config compression.type=zstd \
  --config min.insync.replicas=2 --config retention.ms=604800000
```

#### Performance Testing & Benchmark Verification:
- **Benchmark Directive:** Inspect consumer lag: `kafka-consumer-groups --bootstrap-server kafka:9092 --describe --group namma-cdc-group`.

---

### 03.09 Dimension Specification: `ARCH-SCALE-009` (Redis Distributed Caching & Master Data Invalidation)
- **Dimension Identifier:** `ARCH-SCALE-009`
- **Technical Mechanism:** Redis 7.2 Cluster Mode (3 Masters, 3 Replicas) + Cache-Aside Pattern
- **Baseline Operating Scale:** 5,000 Cache Operations / Second
- **Peak Dimensioned Scale Target:** **50,000 Cache Operations / Second**
- **Target Architectural Bottleneck:** Repeated SQL queries for static catalogs (400 Essential Drugs, 1,200 ICD-10 codes, 183 clinic profiles).
- **Scalability Engineering Strategy:** Cache static and reference data in Redis with 24-hour TTL. Invalidate cache keys selectively using Redis Pub/Sub broadcast on master data updates.
- **Performance & Scalability Outcome:** 94% cache hit ratio; eliminates 85,000 database queries per hour and maintains catalog lookup latency < 2ms.
- **Formal Mathematical Model:** Memory Footprint: 50,000 items in Redis cluster consumes < 350MB RAM across all master nodes.

#### Step-by-Step Implementation Blueprint:
1. Microservices check Redis before querying database (Cache-Aside pattern).
2. Cache misses query database, populate Redis with TTL, and return result.
3. Administrative catalog updates publish event to `namma.cache.invalidate` channel.
4. Subscribed microservice instances evict local memory cache and reload updated record.
5. Cache stampede protection uses distributed mutex locks (`redlock`) during key re-population.
6. Pipelining used for multi-key lookups (e.g. fetching drug details for polypharmacy prescriptions).
7. Keyspace notifications enabled to track key eviction and expiration events.
8. Redis persistence configured with RDB snapshots every 15 minutes and AOF with `appendfsync everysec`.

#### Authoritative Configuration & Implementation Blueprint:
```typescript
// Redis cache-aside implementation with stampede lock
async function getFormularyDrug(drugId: string): Promise<Drug> {
  const key = `cache:drug:${drugId}`;
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  const lock = await acquireLock(`lock:${key}`, 2000);
  if (lock) {
    try {
      const drug = await db.drugs.findUnique({ where: { id: drugId } });
      await redis.set(key, JSON.stringify(drug), 'EX', 86400);
      return drug;
    } finally {
      await releaseLock(lock);
    }
  } else {
    await sleep(50);
    return getFormularyDrug(drugId);
  }
}
```

#### Performance Testing & Benchmark Verification:
- **Benchmark Directive:** Inspect cache hit ratio: `redis-cli info stats | grep -E 'keyspace_hits|keyspace_misses'`.

---

### 03.10 Dimension Specification: `ARCH-SCALE-010` (ClickHouse Columnar Analytics Compaction & Partition Tiering)
- **Dimension Identifier:** `ARCH-SCALE-010`
- **Technical Mechanism:** ClickHouse 24.3 Cluster (ReplacingMergeTree + S3 Storage Tiering)
- **Baseline Operating Scale:** 10,000 Analytics Records / Day
- **Peak Dimensioned Scale Target:** **150,000 Analytics Records / Day**
- **Target Architectural Bottleneck:** Slow aggregate queries across multi-million row clinical datasets on municipal epidemiological dashboards.
- **Scalability Engineering Strategy:** Organize ClickHouse tables using `ReplacingMergeTree` engine partitioned by month. Automatically migrate partitions older than 90 days to S3 cold tier.
- **Performance & Scalability Outcome:** Municipal aggregate dashboard queries across 10 million clinical rows execute in < 450ms.
- **Formal Mathematical Model:** Compression Ratio: ClickHouse LZ4/ZSTD columnar encoding achieves 8.2x compression over raw CSV/JSON.

#### Step-by-Step Implementation Blueprint:
1. ClickHouse consumes Debezium CDC records from Kafka in micro-batches of 5,000 rows.
2. Columnar format compresses data by 85% compared to raw relational storage.
3. Background merge trees compact parts and apply deduplication rules.
4. Storage tiering policy moves cold partitions to cost-effective S3 storage.
5. Vectorized execution engine processes SIMD instructions across hundreds of thousands of rows/sec.
6. Primary sorting keys (`ORDER BY (clinic_id, encounter_date)`) align with common municipal dashboard filters.
7. Materialized views pre-aggregate hourly fever counts by municipal ward.
8. Distributed table engine shards queries across multiple ClickHouse nodes during city-wide surveillance runs.

#### Authoritative Configuration & Implementation Blueprint:
```sql
CREATE TABLE namma_analytics.encounters_stream (
    encounter_id UUID,
    clinic_id LowCardinality(String),
    ward_id UInt16,
    encounter_date Date,
    diagnosis_code LowCardinality(String)
) ENGINE = ReplacingMergeTree()
PARTITION BY toYYYYMM(encounter_date)
ORDER BY (clinic_id, encounter_date, encounter_id)
TTL encounter_date + INTERVAL 90 DAY TO VOLUME 's3_cold';
```

#### Performance Testing & Benchmark Verification:
- **Benchmark Directive:** Benchmark aggregate query: `clickhouse-client --query 'SELECT ward_id, count(*) FROM namma_analytics.encounters_stream GROUP BY ward_id'`.

---

### 03.11 Dimension Specification: `ARCH-SCALE-011` (Edge-to-Cloud Asynchronous Sync Replay Throttling)
- **Dimension Identifier:** `ARCH-SCALE-011`
- **Technical Mechanism:** Token Bucket Rate Limiter + Zstandard Compressed Micro-Batches
- **Baseline Operating Scale:** 20 Clinics Syncing Concurrently
- **Peak Dimensioned Scale Target:** **183 Clinics Reconnecting Simultaneously Post-Outage**
- **Target Architectural Bottleneck:** Network bandwidth exhaustion and database lock starvation when 183 clinics reconnect simultaneously after city-wide fiber cut.
- **Scalability Engineering Strategy:** Edge daemons implement randomized exponential backoff with jitter and token bucket sync throttling (max 50 batches/sec per cloud gateway pod).
- **Performance & Scalability Outcome:** Prevents cloud gateway collapse; smoothly drains 500,000 queued offline mutations in < 12 minutes without service degradation.
- **Formal Mathematical Model:** Drain Rate Math: 500,000 records / 50 batches/sec / 100 records/batch = 100 seconds per gateway pod. Across 6 pods = < 3 minutes.

#### Step-by-Step Implementation Blueprint:
1. Edge daemon detects network restoration; calculates jittered backoff: `delay = min(300, 2^attempt * 5) + random(0, 30)`.
2. Compresses mutation journal into 250KB Zstandard micro-batches (average 100 mutations/batch).
3. Gateway token bucket admits maximum 50 batches/sec, returning HTTP 429 with `Retry-After` if congested.
4. Cloud sync service processes batches in parallel worker threads, updating sync status flags.
5. Field-level CRDT LWW rules resolve divergent state deterministically with zero human intervention.
6. Edge daemon checkpoints local SQLite journal sequence upon receiving HTTP 200 acknowledgment.
7. Bandwidth throttling limits upload rate to 256 KB/s on 4G cellular failover connections.
8. Sync health metrics stream to Prometheus: `sync_drain_duration_seconds` and `sync_mutations_replayed_total`.

#### Authoritative Configuration & Implementation Blueprint:
```typescript
// Sync jitter backoff calculation
function calculateSyncRetryDelay(attempt: number): number {
  const baseDelay = Math.min(300, Math.pow(2, attempt) * 5);
  const jitter = Math.floor(Math.random() * 30);
  return (baseDelay + jitter) * 1000;
}
```

#### Performance Testing & Benchmark Verification:
- **Benchmark Directive:** Simulate sync reconnect: `python scripts/tests/simulate_mass_reconnect.py --clinics 183 --mutations-per-clinic 2500`.

---

### 03.12 Dimension Specification: `ARCH-SCALE-012` (WORM Audit Ledger Write Throughput & Storage Compaction)
- **Dimension Identifier:** `ARCH-SCALE-012`
- **Technical Mechanism:** SHA-256 HMAC Hash Chaining + Parquet Merkle Tree Archival
- **Baseline Operating Scale:** 50 Audit Events / Second
- **Peak Dimensioned Scale Target:** **500 Audit Events / Second**
- **Target Architectural Bottleneck:** Storage bloat and cryptographic hashing computation bottlenecks on immutable DPDP Act compliance audit ledger.
- **Scalability Engineering Strategy:** Compute SHA-256 HMAC in asynchronous background worker; assemble daily records into compressed Parquet Merkle tree blocks with cryptographic root hash.
- **Performance & Scalability Outcome:** Processes 500 audit events/sec with < 5% CPU overhead; compresses daily audit logs from 12GB raw JSON to 650MB Parquet.
- **Formal Mathematical Model:** Cost Efficiency: S3 Glacier Deep Archive storage of compressed Parquet costs < $15/month for 5 years of municipal health audit logs.

#### Step-by-Step Implementation Blueprint:
1. Applications emit audit events to local non-blocking ring buffer.
2. Audit worker thread calculates SHA-256 HMAC hash linking to previous block hash.
3. Daily rotation script compiles audit records into columnar Parquet format.
4. Merkle root hash is calculated, signed with BBMP private key, and published to immutable S3 Object Lock vault.
5. Parquet Snappy compression achieves 18.5x space reduction over raw JSON text logs.
6. WORM policy enforces strict legal hold compliance; objects cannot be deleted even by root account.
7. Automated daily integrity verification scans verify hash chain consistency across previous 30 days.
8. Audit query service provides fast columnar scanning over Athena / DuckDB for statutory compliance reviews.

#### Authoritative Configuration & Implementation Blueprint:
```python
# Audit Merkle root calculation snippet
import hashlib
def compute_merkle_root(hashes):
    if len(hashes) == 1: return hashes[0]
    new_level = []
    for i in range(0, len(hashes), 2):
        h1 = hashes[i]
        h2 = hashes[i+1] if i+1 < len(hashes) else h1
        new_level.append(hashlib.sha256((h1 + h2).encode()).hexdigest())
    return compute_merkle_root(new_level)
```

#### Performance Testing & Benchmark Verification:
- **Benchmark Directive:** Audit verification: `python scripts/verify_worm_chain.py --start-date 2026-09-01 --end-date 2026-09-04`.

---

## 04. Relational Database Partitioning & Archival Engineering
Declarative table partitioning and lifecycle management for high-growth PostgreSQL tables:

### 04.1 Monthly Range Partitioning Architecture
High-growth clinical tables (`clinical_encounters`, `prescriptions`, `lab_orders`, `offline_mutation_journal`) are partitioned by month:
```sql
-- Declarative monthly partitioning on clinical_encounters
CREATE TABLE clinical_encounters (
    id UUID NOT NULL,
    clinic_id VARCHAR(32) NOT NULL,
    patient_id UUID NOT NULL,
    provider_id UUID NOT NULL,
    encounter_date DATE NOT NULL,
    soap_notes JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT pk_clinical_encounters PRIMARY KEY (encounter_date, id)
) PARTITION BY RANGE (encounter_date);

-- Sample monthly partitions for 2026
CREATE TABLE encounters_2026_09 PARTITION OF clinical_encounters
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
CREATE TABLE encounters_2026_10 PARTITION OF clinical_encounters
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
CREATE TABLE encounters_2026_11 PARTITION OF clinical_encounters
    FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');

-- Local index per partition for fast encounter lookups
CREATE INDEX idx_encounters_2026_09_patient ON encounters_2026_09 (patient_id);
CREATE INDEX idx_encounters_2026_09_clinic ON encounters_2026_09 (clinic_id);
```

### 04.2 Automated Partition Management via `pg_partman`
The `pg_partman` extension automatically creates future monthly partitions and detaches historical partitions:
```sql
-- Configure pg_partman to maintain 3 future partitions and retain 24 historical partitions
SELECT partman.create_parent(
    p_parent_table => 'public.clinical_encounters',
    p_control => 'encounter_date',
    p_type => 'native',
    p_interval => 'monthly',
    p_premake => 3
);
```

## 05. Kubernetes Autoscaling Architecture & Resource Allocations Across All Containers
Comprehensive resource requests, limits, and HPA configurations across all 18 platform containers:

| Container ID | Container Name | CPU Req | CPU Limit | Mem Req | Mem Limit | Min Pods | Max Pods | Target CPU | Target RPS | Description |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `ARCH-CONT-001` | **Edge Workstation PWA Shell** | 100m | 500m | 128Mi | 512Mi | 3 | 15 | N/A | 50 | Client Workstation PWA Shell running in browser |
| `ARCH-CONT-002` | **Edge Mini-Server Local Daemon** | 500m | 2000m | 512Mi | 2048Mi | 1 | 1 | N/A | 100 | Local edge mini-server daemon on Intel N100 hardware |
| `ARCH-CONT-003` | **Central Cloud API Gateway** | 1000m | 4000m | 1024Mi | 4096Mi | 3 | 12 | 65% | 250 | Cloud Envoy/Kong ingress gateway routing all HTTP/gRPC traffic |
| `ARCH-CONT-004` | **Auth & IAM Microservice** | 500m | 2000m | 512Mi | 2048Mi | 2 | 8 | 70% | 150 | Argon2id credential verification and JWT token issuance |
| `ARCH-CONT-005` | **Master Patient Index Service** | 1000m | 4000m | 1024Mi | 4096Mi | 3 | 10 | 65% | 100 | Citizen demographic search, deduplication, and ABHA registration |
| `ARCH-CONT-006` | **Queue Orchestration & Triage** | 500m | 2000m | 512Mi | 2048Mi | 2 | 8 | 70% | 200 | Queue token issuance, TV display broadcast, and MEWS calculations |
| `ARCH-CONT-007` | **Clinical Consultation Service** | 1000m | 4000m | 1024Mi | 4096Mi | 4 | 16 | 65% | 120 | Doctor SOAP notes capture, ICD-10 coding, and consultation sealing |
| `ARCH-CONT-008` | **Electronic Prescription Service** | 500m | 2000m | 512Mi | 2048Mi | 3 | 10 | 70% | 150 | Formulary rule enforcement, DDI safety checks, and e-Rx signing |
| `ARCH-CONT-009` | **Pharmacy Inventory & Dispense** | 500m | 2000m | 512Mi | 2048Mi | 3 | 10 | 70% | 150 | 2D DataMatrix barcode scanning, FEFO batch decrement, and stock indents |
| `ARCH-CONT-010` | **Diagnostic Laboratory Service** | 500m | 2000m | 512Mi | 2048Mi | 2 | 8 | 70% | 100 | 58 rapid diagnostic test panels, result recording, and panic alerts |
| `ARCH-CONT-011` | **Referral & EMS Telemetry Bridge** | 250m | 1000m | 256Mi | 1024Mi | 2 | 6 | 75% | 80 | Referral dossiers, 108 ambulance CAD dispatch, and transit tracking |
| `ARCH-CONT-012` | **Citizen Notification Service** | 500m | 2000m | 512Mi | 2048Mi | 2 | 8 | 70% | 150 | Bilingual SMS and WhatsApp dispatch via KSSD gateway |
| `ARCH-CONT-013` | **Edge-Cloud Sync Gateway** | 1000m | 4000m | 1024Mi | 4096Mi | 4 | 16 | 60% | 100 | Zstandard mutation journal ingestion and CRDT conflict resolution |
| `ARCH-CONT-014` | **ABDM Interoperability Gateway** | 1000m | 4000m | 2048Mi | 8192Mi | 2 | 8 | 70% | 60 | FHIR R4 Bundle transformation and NHA care context publishing |
| `ARCH-CONT-015` | **Analytics & CDC Pipeline** | 1000m | 4000m | 2048Mi | 8192Mi | 2 | 6 | 75% | 100 | Debezium Kafka CDC consumer and ClickHouse columnar ingestion |
| `ARCH-CONT-016` | **Advisory AI Decision Engine** | 1000m | 4000m | 2048Mi | 8192Mi | 2 | 6 | 65% | 80 | ONNX Runtime model execution for clinical advisory alerts |
| `ARCH-CONT-017` | **Cryptographic WORM Audit Service** | 500m | 2000m | 512Mi | 2048Mi | 2 | 6 | 70% | 100 | SHA-256 HMAC append-only hash chain audit ledger sealing |
| `ARCH-CONT-018` | **Enterprise PostgreSQL & PgBouncer** | 2000m | 8000m | 4096Mi | 16384Mi | 3 | 8 | 70% | 500 | Patroni master/standby database nodes with PgBouncer pooling |

### 05.03 HPA Specification: `ARCH-CONT-003` (Central Cloud API Gateway)
- **Container:** `ARCH-CONT-003` - Central Cloud API Gateway
- **Scaling Policy:** Minimum 3 replicas, Maximum 12 replicas.
- **Resource Requests & Limits:** CPU `1000m` / `4000m`, Memory `1024Mi` / `4096Mi`.
- **Trigger Thresholds:** CPU > 65%, Endpoint RPS > 250 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: central-cloud-api-gateway-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: central-cloud-api-gateway
  minReplicas: 3
  maxReplicas: 12
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 65
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '250'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: central-cloud-api-gateway
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: central-cloud-api-gateway
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: central-cloud-api-gateway
  template:
    metadata:
      labels:
        app: central-cloud-api-gateway
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: central-cloud-api-gateway
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/central-cloud-api-gateway:v1.4.2
        resources:
          requests:
            cpu: 1000m
            memory: 1024Mi
          limits:
            cpu: 4000m
            memory: 4096Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: central-cloud-api-gateway-pdb
  namespace: namma-prod
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: central-cloud-api-gateway
```

---

### 05.04 HPA Specification: `ARCH-CONT-004` (Auth & IAM Microservice)
- **Container:** `ARCH-CONT-004` - Auth & IAM Microservice
- **Scaling Policy:** Minimum 2 replicas, Maximum 8 replicas.
- **Resource Requests & Limits:** CPU `500m` / `2000m`, Memory `512Mi` / `2048Mi`.
- **Trigger Thresholds:** CPU > 70%, Endpoint RPS > 150 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: auth-and-iam-microservice-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: auth-and-iam-microservice
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '150'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-and-iam-microservice
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: auth-and-iam-microservice
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: auth-and-iam-microservice
  template:
    metadata:
      labels:
        app: auth-and-iam-microservice
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: auth-and-iam-microservice
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/auth-and-iam-microservice:v1.4.2
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2048Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: auth-and-iam-microservice-pdb
  namespace: namma-prod
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: auth-and-iam-microservice
```

---

### 05.05 HPA Specification: `ARCH-CONT-005` (Master Patient Index Service)
- **Container:** `ARCH-CONT-005` - Master Patient Index Service
- **Scaling Policy:** Minimum 3 replicas, Maximum 10 replicas.
- **Resource Requests & Limits:** CPU `1000m` / `4000m`, Memory `1024Mi` / `4096Mi`.
- **Trigger Thresholds:** CPU > 65%, Endpoint RPS > 100 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: master-patient-index-service-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: master-patient-index-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 65
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '100'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: master-patient-index-service
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: master-patient-index-service
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: master-patient-index-service
  template:
    metadata:
      labels:
        app: master-patient-index-service
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: master-patient-index-service
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/master-patient-index-service:v1.4.2
        resources:
          requests:
            cpu: 1000m
            memory: 1024Mi
          limits:
            cpu: 4000m
            memory: 4096Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: master-patient-index-service-pdb
  namespace: namma-prod
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: master-patient-index-service
```

---

### 05.06 HPA Specification: `ARCH-CONT-006` (Queue Orchestration & Triage)
- **Container:** `ARCH-CONT-006` - Queue Orchestration & Triage
- **Scaling Policy:** Minimum 2 replicas, Maximum 8 replicas.
- **Resource Requests & Limits:** CPU `500m` / `2000m`, Memory `512Mi` / `2048Mi`.
- **Trigger Thresholds:** CPU > 70%, Endpoint RPS > 200 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: queue-orchestration-and-triage-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: queue-orchestration-and-triage
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '200'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: queue-orchestration-and-triage
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: queue-orchestration-and-triage
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: queue-orchestration-and-triage
  template:
    metadata:
      labels:
        app: queue-orchestration-and-triage
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: queue-orchestration-and-triage
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/queue-orchestration-and-triage:v1.4.2
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2048Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: queue-orchestration-and-triage-pdb
  namespace: namma-prod
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: queue-orchestration-and-triage
```

---

### 05.07 HPA Specification: `ARCH-CONT-007` (Clinical Consultation Service)
- **Container:** `ARCH-CONT-007` - Clinical Consultation Service
- **Scaling Policy:** Minimum 4 replicas, Maximum 16 replicas.
- **Resource Requests & Limits:** CPU `1000m` / `4000m`, Memory `1024Mi` / `4096Mi`.
- **Trigger Thresholds:** CPU > 65%, Endpoint RPS > 120 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: clinical-consultation-service-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: clinical-consultation-service
  minReplicas: 4
  maxReplicas: 16
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 65
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '120'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: clinical-consultation-service
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: clinical-consultation-service
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: clinical-consultation-service
  template:
    metadata:
      labels:
        app: clinical-consultation-service
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: clinical-consultation-service
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/clinical-consultation-service:v1.4.2
        resources:
          requests:
            cpu: 1000m
            memory: 1024Mi
          limits:
            cpu: 4000m
            memory: 4096Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: clinical-consultation-service-pdb
  namespace: namma-prod
spec:
  minAvailable: 3
  selector:
    matchLabels:
      app: clinical-consultation-service
```

---

### 05.08 HPA Specification: `ARCH-CONT-008` (Electronic Prescription Service)
- **Container:** `ARCH-CONT-008` - Electronic Prescription Service
- **Scaling Policy:** Minimum 3 replicas, Maximum 10 replicas.
- **Resource Requests & Limits:** CPU `500m` / `2000m`, Memory `512Mi` / `2048Mi`.
- **Trigger Thresholds:** CPU > 70%, Endpoint RPS > 150 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: electronic-prescription-service-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: electronic-prescription-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '150'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: electronic-prescription-service
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: electronic-prescription-service
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: electronic-prescription-service
  template:
    metadata:
      labels:
        app: electronic-prescription-service
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: electronic-prescription-service
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/electronic-prescription-service:v1.4.2
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2048Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: electronic-prescription-service-pdb
  namespace: namma-prod
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: electronic-prescription-service
```

---

### 05.09 HPA Specification: `ARCH-CONT-009` (Pharmacy Inventory & Dispense)
- **Container:** `ARCH-CONT-009` - Pharmacy Inventory & Dispense
- **Scaling Policy:** Minimum 3 replicas, Maximum 10 replicas.
- **Resource Requests & Limits:** CPU `500m` / `2000m`, Memory `512Mi` / `2048Mi`.
- **Trigger Thresholds:** CPU > 70%, Endpoint RPS > 150 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: pharmacy-inventory-and-dispense-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: pharmacy-inventory-and-dispense
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '150'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pharmacy-inventory-and-dispense
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: pharmacy-inventory-and-dispense
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: pharmacy-inventory-and-dispense
  template:
    metadata:
      labels:
        app: pharmacy-inventory-and-dispense
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: pharmacy-inventory-and-dispense
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/pharmacy-inventory-and-dispense:v1.4.2
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2048Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: pharmacy-inventory-and-dispense-pdb
  namespace: namma-prod
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: pharmacy-inventory-and-dispense
```

---

### 05.10 HPA Specification: `ARCH-CONT-010` (Diagnostic Laboratory Service)
- **Container:** `ARCH-CONT-010` - Diagnostic Laboratory Service
- **Scaling Policy:** Minimum 2 replicas, Maximum 8 replicas.
- **Resource Requests & Limits:** CPU `500m` / `2000m`, Memory `512Mi` / `2048Mi`.
- **Trigger Thresholds:** CPU > 70%, Endpoint RPS > 100 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: diagnostic-laboratory-service-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: diagnostic-laboratory-service
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '100'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: diagnostic-laboratory-service
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: diagnostic-laboratory-service
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: diagnostic-laboratory-service
  template:
    metadata:
      labels:
        app: diagnostic-laboratory-service
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: diagnostic-laboratory-service
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/diagnostic-laboratory-service:v1.4.2
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2048Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: diagnostic-laboratory-service-pdb
  namespace: namma-prod
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: diagnostic-laboratory-service
```

---

### 05.11 HPA Specification: `ARCH-CONT-011` (Referral & EMS Telemetry Bridge)
- **Container:** `ARCH-CONT-011` - Referral & EMS Telemetry Bridge
- **Scaling Policy:** Minimum 2 replicas, Maximum 6 replicas.
- **Resource Requests & Limits:** CPU `250m` / `1000m`, Memory `256Mi` / `1024Mi`.
- **Trigger Thresholds:** CPU > 75%, Endpoint RPS > 80 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: referral-and-ems-telemetry-bridge-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: referral-and-ems-telemetry-bridge
  minReplicas: 2
  maxReplicas: 6
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 75
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '80'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: referral-and-ems-telemetry-bridge
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: referral-and-ems-telemetry-bridge
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: referral-and-ems-telemetry-bridge
  template:
    metadata:
      labels:
        app: referral-and-ems-telemetry-bridge
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: referral-and-ems-telemetry-bridge
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/referral-and-ems-telemetry-bridge:v1.4.2
        resources:
          requests:
            cpu: 250m
            memory: 256Mi
          limits:
            cpu: 1000m
            memory: 1024Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: referral-and-ems-telemetry-bridge-pdb
  namespace: namma-prod
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: referral-and-ems-telemetry-bridge
```

---

### 05.12 HPA Specification: `ARCH-CONT-012` (Citizen Notification Service)
- **Container:** `ARCH-CONT-012` - Citizen Notification Service
- **Scaling Policy:** Minimum 2 replicas, Maximum 8 replicas.
- **Resource Requests & Limits:** CPU `500m` / `2000m`, Memory `512Mi` / `2048Mi`.
- **Trigger Thresholds:** CPU > 70%, Endpoint RPS > 150 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: citizen-notification-service-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: citizen-notification-service
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '150'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: citizen-notification-service
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: citizen-notification-service
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: citizen-notification-service
  template:
    metadata:
      labels:
        app: citizen-notification-service
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: citizen-notification-service
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/citizen-notification-service:v1.4.2
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2048Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: citizen-notification-service-pdb
  namespace: namma-prod
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: citizen-notification-service
```

---

### 05.14 HPA Specification: `ARCH-CONT-014` (ABDM Interoperability Gateway)
- **Container:** `ARCH-CONT-014` - ABDM Interoperability Gateway
- **Scaling Policy:** Minimum 2 replicas, Maximum 8 replicas.
- **Resource Requests & Limits:** CPU `1000m` / `4000m`, Memory `2048Mi` / `8192Mi`.
- **Trigger Thresholds:** CPU > 70%, Endpoint RPS > 60 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: abdm-interoperability-gateway-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: abdm-interoperability-gateway
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '60'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: abdm-interoperability-gateway
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: abdm-interoperability-gateway
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: abdm-interoperability-gateway
  template:
    metadata:
      labels:
        app: abdm-interoperability-gateway
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: abdm-interoperability-gateway
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/abdm-interoperability-gateway:v1.4.2
        resources:
          requests:
            cpu: 1000m
            memory: 2048Mi
          limits:
            cpu: 4000m
            memory: 8192Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: abdm-interoperability-gateway-pdb
  namespace: namma-prod
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: abdm-interoperability-gateway
```

---

### 05.15 HPA Specification: `ARCH-CONT-015` (Analytics & CDC Pipeline)
- **Container:** `ARCH-CONT-015` - Analytics & CDC Pipeline
- **Scaling Policy:** Minimum 2 replicas, Maximum 6 replicas.
- **Resource Requests & Limits:** CPU `1000m` / `4000m`, Memory `2048Mi` / `8192Mi`.
- **Trigger Thresholds:** CPU > 75%, Endpoint RPS > 100 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: analytics-and-cdc-pipeline-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: analytics-and-cdc-pipeline
  minReplicas: 2
  maxReplicas: 6
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 75
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '100'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: analytics-and-cdc-pipeline
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: analytics-and-cdc-pipeline
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: analytics-and-cdc-pipeline
  template:
    metadata:
      labels:
        app: analytics-and-cdc-pipeline
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: analytics-and-cdc-pipeline
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/analytics-and-cdc-pipeline:v1.4.2
        resources:
          requests:
            cpu: 1000m
            memory: 2048Mi
          limits:
            cpu: 4000m
            memory: 8192Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: analytics-and-cdc-pipeline-pdb
  namespace: namma-prod
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: analytics-and-cdc-pipeline
```

---

### 05.16 HPA Specification: `ARCH-CONT-016` (Advisory AI Decision Engine)
- **Container:** `ARCH-CONT-016` - Advisory AI Decision Engine
- **Scaling Policy:** Minimum 2 replicas, Maximum 6 replicas.
- **Resource Requests & Limits:** CPU `1000m` / `4000m`, Memory `2048Mi` / `8192Mi`.
- **Trigger Thresholds:** CPU > 65%, Endpoint RPS > 80 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: advisory-ai-decision-engine-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: advisory-ai-decision-engine
  minReplicas: 2
  maxReplicas: 6
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 65
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '80'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: advisory-ai-decision-engine
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: advisory-ai-decision-engine
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: advisory-ai-decision-engine
  template:
    metadata:
      labels:
        app: advisory-ai-decision-engine
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: advisory-ai-decision-engine
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/advisory-ai-decision-engine:v1.4.2
        resources:
          requests:
            cpu: 1000m
            memory: 2048Mi
          limits:
            cpu: 4000m
            memory: 8192Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: advisory-ai-decision-engine-pdb
  namespace: namma-prod
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: advisory-ai-decision-engine
```

---

### 05.17 HPA Specification: `ARCH-CONT-017` (Cryptographic WORM Audit Service)
- **Container:** `ARCH-CONT-017` - Cryptographic WORM Audit Service
- **Scaling Policy:** Minimum 2 replicas, Maximum 6 replicas.
- **Resource Requests & Limits:** CPU `500m` / `2000m`, Memory `512Mi` / `2048Mi`.
- **Trigger Thresholds:** CPU > 70%, Endpoint RPS > 100 req/sec.

#### Production Kubernetes HPA v2 Manifest:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: cryptographic-worm-audit-service-hpa
  namespace: namma-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: cryptographic-worm-audit-service
  minReplicas: 2
  maxReplicas: 6
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: '100'
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
```

#### Production Kubernetes Deployment & Security Context Manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cryptographic-worm-audit-service
  namespace: namma-prod
  labels:
    app.kubernetes.io/name: cryptographic-worm-audit-service
    app.kubernetes.io/part-of: namma-platform
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: cryptographic-worm-audit-service
  template:
    metadata:
      labels:
        app: cryptographic-worm-audit-service
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: cryptographic-worm-audit-service
        image: 20309228.dkr.ecr.ap-south-1.amazonaws.com/namma/cryptographic-worm-audit-service:v1.4.2
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2048Mi
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ['/bin/sh', '-c', 'sleep 15']
```

#### PodDisruptionBudget (PDB) Manifest:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: cryptographic-worm-audit-service-pdb
  namespace: namma-prod
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: cryptographic-worm-audit-service
```

---

## 06. Performance Testing, Stress Benchmarking & Load Injection
Production load testing methodology using k6 to validate platform elasticity under peak surge conditions:

### 06.1 Scenario A: Peak Diurnal Morning Surge (1,200 RPS)
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 200 },   // Warm-up to 200 virtual users
    { duration: '5m', target: 1200 },  // Ramp-up to peak 1,200 RPS
    { duration: '10m', target: 1200 }, // Sustain peak surge
    { duration: '3m', target: 200 },   // Step down
    { duration: '1m', target: 0 },     // Cool down
  ],
  thresholds: {
    http_req_duration: ['p(95)<250', 'p(99)<500'], // P95 < 250ms, P99 < 500ms
    http_req_failed: ['rate<0.001'],               // Less than 0.1% error rate
  },
};

const BASE_URL = __ENV.TARGET_URL || 'https://api.nammahealth.bbmp.gov.in';

export default function () {
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${__ENV.TEST_JWT_TOKEN}`,
      'X-Clinic-ID': 'BBMP-CLN-042',
    },
  };

  // 1. Patient Search Query
  const searchRes = http.get(`${BASE_URL}/api/v1/patients/search?q=Kumar&ward=112`, params);
  check(searchRes, { 'search status 200': (r) => r.status === 200 });

  // 2. Triage Vitals Submission
  const vitalsPayload = JSON.stringify({
    patient_id: '018f3a5b-7c12-789a-bcde-f0123456789a',
    bp_systolic: 128,
    bp_diastolic: 82,
    pulse_rate: 76,
    spo2: 98,
    temperature: 98.4,
  });
  const vitalsRes = http.post(`${BASE_URL}/api/v1/triage/vitals`, vitalsPayload, params);
  check(vitalsRes, { 'vitals recorded': (r) => r.status === 201 });

  sleep(1);
}
```

### 06.2 Scenario B: Post-Outage Mass Edge Sync Drain Benchmark
Simulates 183 clinics reconnecting and pushing mutation batches simultaneously:
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    mass_sync: {
      executor: 'per-vu-iterations',
      vus: 183,
      iterations: 25, // 25 batches per clinic = 4,575 batches (457,500 mutations)
      maxDuration: '15m',
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const clinicIndex = __VU;
  const clinicId = `BBMP-CLN-${String(clinicIndex).padStart(3, '0')}`;
  const batchPayload = JSON.stringify({
    clinic_id: clinicId,
    batch_sequence: __ITER,
    mutations_count: 100,
    payload_compressed_zst: 'BASE64_MOCK_DATA_ZST_BYTES',
  });
  const res = http.post('https://sync.nammahealth.bbmp.gov.in/v1/push', batchPayload, {
    headers: { 'Content-Type': 'application/json', 'X-Device-Cert-CN': clinicId }
  });
  check(res, { 'sync batch accepted 200': (r) => r.status === 200 });
  sleep(0.5);
}
```

### 06.3 Scenario C: Epidemic Outbreak Stress Test (3,000 RPS)
Simulates severe municipal dengue / respiratory viral outbreak causing 2.5x normal patient footfall:
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '3m', target: 500 },
    { duration: '5m', target: 3000 },  // Peak 3,000 RPS
    { duration: '15m', target: 3000 }, // Sustain peak
    { duration: '5m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<400', 'p(99)<1000'],
    http_req_failed: ['rate<0.005'],
  },
};

export default function () {
  const res = http.get('https://api.nammahealth.bbmp.gov.in/api/v1/lab/tests/catalogue');
  check(res, { 'catalogue fetched 200': (r) => r.status === 200 });
  sleep(0.2);
}
```

### 06.4 Scenario D: 24-Hour Continuous Endurance & Memory Leak Soak Test
Executes 24 hours of sustained 500 RPS traffic to verify zero Node.js heap leaks or connection pool exhaustion:
```bash
# Run 24-hour soak test with Prometheus memory scraping
k6 run --vus 500 --duration 24h tests/load/soak_test.js
```

## 07. Universal Scalability Law (USL) Calibration & Capacity Modeling
Mathematical validation of system scalability using Dr. Neil Gunther's Universal Scalability Law (USL):
```python
# scripts/perf/usl_model.py
import numpy as np
from scipy.optimize import curve_fit

def usl_model(N, gamma, sigma, kappa):
    """
    N: Number of concurrent workers / load clients
    gamma: Linear scaling coefficient (requests per second per client at N=1)
    sigma: Contention coefficient (serialization delay penalty)
    kappa: Coherency coefficient (inter-node crosstalk / cache invalidation penalty)
    """
    return (gamma * N) / (1 + sigma * (N - 1) + kappa * N * (N - 1))

# Experimental benchmark data from k6 stress runs across 183 clinics
concurrency_levels = np.array([1, 10, 50, 100, 250, 500, 1000, 1500, 2000])
measured_throughput = np.array([15.2, 148.0, 710.0, 1340.0, 2850.0, 4800.0, 6800.0, 7400.0, 7150.0])

popt, pcov = curve_fit(usl_model, concurrency_levels, measured_throughput, p0=[15.0, 0.002, 0.00005])
gamma_est, sigma_est, kappa_est = popt

print(f"Calibrated USL Parameters:")
print(f"  Gamma (Linear Scale):    {gamma_est:.4f} RPS/VU")
print(f"  Sigma (Contention):      {sigma_est:.6f}")
print(f"  Kappa (Coherency):       {kappa_est:.8f}")

# Calculate maximum theoretical capacity and concurrency limit N_max
N_max = np.sqrt((1 - sigma_est) / kappa_est)
X_max = usl_model(N_max, gamma_est, sigma_est, kappa_est)
print(f"  Theoretical Peak Concurrency N_max: {int(N_max)} concurrent users")
print(f"  Maximum Achievable Throughput X_max:  {int(X_max)} requests/second")
```

## 08. Scalability Architecture Fitness Tests & Verification Checklist
Automated CI/CD performance testing gates enforcing architectural scalability invariants:

### 08.1 Automated Scalability Fitness Tests
1. **Gateway Latency Fitness Test:** Synthetic test injects 1,200 concurrent requests; asserts P95 latency stays under 250ms and zero connections dropped.
2. **Connection Leak Regression Gate:** Continuous integration test runs 5,000 parallel transactions through PgBouncer; asserts active server connections do not exceed pool limit of 150.
3. **SQLite Write Concurrency Gate:** Simulates 10 concurrent writes on Intel N100 test appliance; asserts zero `SQLITE_BUSY` errors and commit duration < 15ms.
4. **Kafka Partition Balance Gate:** Verifies that message keys evenly distribute events across all 16 topic partitions (coefficient of variation < 0.15).
5. **USL Concurrency Regression Test:** Automated load sweep tests concurrency up to 500 threads; asserts contention coefficient `\sigma < 0.005`.

### 08.2 Scalability Verification Checklist Matrix
| Verification Item | Automated Verification Command | Acceptance Threshold | CI/CD Enforcement Gate |
| :--- | :--- | :---: | :---: |
| P95 End-to-End Latency | `npm run test:perf:latency` | P95 < 250ms at 1,200 RPS | Release Gate Blocker |
| Database Connection Pool Sizing | `psql -c 'SHOW POOLS;'` | Active connections <= 150 | Production Monitoring |
| Redis Cache Hit Ratio | `redis-cli info stats` | Hit ratio >= 90.0% | Nightly Audit |
| ClickHouse Query Duration | `npm run test:analytics:benchmark` | P90 query latency < 500ms | Nightly Audit |
| Zero SQLite Lock Timeouts | `python scripts/tests/test_sqlite_concurrency.py`| 0 SQLITE_BUSY exceptions | Build Pipeline Gate |
| Kafka Consumer Lag | `kafka-consumer-groups --describe` | Lag < 1,000 records per partition | Continuous Telemetry |
