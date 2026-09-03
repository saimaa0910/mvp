# 📦 Architecture: C4 Container Model
## Namma Clinic Digital Health & Operations Platform
**Document Code:** ARC-CON-03 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Level 2: Container Diagram

```mermaid
C4Container
    title Container Diagram for Namma Clinic Platform

    Person(staff, "Clinic Staff", "Nurse, Doctor, Pharmacist, Lab Tech")
    Person(admin, "Zonal Health Officer", "Public health administrator")

    Container(spa, "Single-Page App (PWA)", "React / TypeScript / Tailwind", "Responsive frontline UI running in browser with Service Worker and IndexedDB.")
    Container(api_gw, "API Gateway / BFF", "Fastify / Node.js", "Handles routing, JWT auth, rate limiting, and request validation.")
    Container(core_api, "Core Healthcare Service", "Node.js / Express / TypeScript", "Implements patient, visit, consultation, and pharmacy business logic.")
    Container(sync_eng, "Offline Sync Engine", "Node.js / TypeScript", "Processes asynchronous offline mutation batches and conflict resolution.")
    ContainerDb(pg_db, "Primary OLTP Database", "PostgreSQL 16 Multi-AZ", "Stores relational clinical, demographic, inventory, and audit records.")
    ContainerDb(redis, "In-Memory Cache", "Redis 7.2", "Stores active sessions, token queue sequences, and rate limits.")
    ContainerDb(dw, "Analytical Star Schema", "PostgreSQL 16 OLAP Read-Replica", "Stores denormalized fact tables and public health surveillance data.")

    Rel(staff, spa, "Interacts with frontline clinical forms", "HTTPS")
    Rel(admin, spa, "Views zonal surveillance dashboards", "HTTPS")
    Rel(spa, api_gw, "Submits transactions and queries", "JSON / HTTPS")
    Rel(api_gw, core_api, "Dispatches authorized requests", "Internal HTTP / mTLS")
    Rel(api_gw, redis, "Verifies session and rate limits", "Redis Protocol")
    Rel(core_api, pg_db, "Performs ACID transactions", "SQL / Prisma")
    Rel(core_api, sync_eng, "Queues offline reconciliation events", "Internal Bus")
    Rel(pg_db, dw, "Replicates analytical events", "CDC / Debezium")
```
