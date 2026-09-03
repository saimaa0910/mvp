# 💻 Technology Stack Inventory & Engineering Standards
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PB-STK-03 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Technology Standards & Architectural Selection

| Layer | Selected Technology | Version | Rationale & Enterprise Standards |
| :--- | :--- | :--- | :--- |
| **Runtime & Language** | Node.js / TypeScript | Node 20.x LTS / TS 5.4+ | Enterprise type safety, high concurrency I/O, shared domain types between client and server. |
| **Backend Framework** | Express.js / Fastify | Fastify 4.x / Express 4.19+ | Low-latency HTTP routing, schema-based JSON serialization, robust plugin architecture. |
| **Frontend Framework** | React / Next.js | React 18.3+ / Next.js 14 LTS | Server-side rendering for executive dashboards, PWA capabilities, optimized bundle chunking. |
| **UI Styling & Tokens** | Tailwind CSS / Vanilla CSS | Tailwind 3.4+ / CSS Modules | Design token consistency, zero runtime CSS overhead, accessible contrast ratios. |
| **Primary Database** | PostgreSQL | PostgreSQL 16.3 (RDS Multi-AZ) | ACID compliance, JSONB document querying, temporal table support, native trigram indexing (`pg_trgm`). |
| **Caching & Queue** | Redis | Redis 7.2 (ElastiCache) | Distributed session storage, token queue state, API rate limiting, and pub/sub for clinic notifications. |
| **Offline Storage** | IndexedDB via Dexie.js | Dexie 4.x | Robust browser-level transactional storage, compound indexing, observable queries for offline sync. |
| **Data Validation** | Zod | Zod 3.23+ | Runtime schema validation, automatic TypeScript inference, single source of truth for DTOs. |
| **ORM / Query Builder** | Prisma / Kysely | Prisma 5.x / Kysely 0.27+ | Type-safe database queries, automated migration management, zero raw-SQL injection risks. |
| **Testing Suite** | Vitest / Playwright / k6 | Vitest 1.6+, Playwright 1.44+, k6 v0.51 | Blazing fast unit tests, cross-browser frontline E2E testing, high-concurrency clinic load simulation. |
| **Containerization** | Docker / Docker Compose | Docker Engine 26+, Compose v2 | Reproducible multi-tier local development, immutable production container images. |
| **IaC & Cloud** | Terraform | Terraform 1.8+ | Declarative cloud infrastructure provisioning across AWS India-South (Mumbai) or Karnataka SDC. |
| **Observability** | Prometheus / Grafana / Loki | OpenTelemetry, Grafana 10+ | Structured JSON logging, RED metrics (Rate, Errors, Duration), clinic connectivity telemetry. |

---

### 2. Engineering Invariants & Constraints
1. **Zero Raw SQL in Application Code:** All database access must pass through repository abstractions using validated ORM/query builders.
2. **Strict Schema Validation:** Every incoming API request body, query parameter, and route parameter must be validated against a Zod schema before hitting business logic.
3. **Immutable Audit Trails:** Audit log records (`access_audit_logs`) must be append-only with cryptographic hashing to prevent tampering.
4. **Bilingual Frontline UI:** Every user-facing UI component must support English and Kannada (`kn_IN`) with zero hardcoded UI strings.
