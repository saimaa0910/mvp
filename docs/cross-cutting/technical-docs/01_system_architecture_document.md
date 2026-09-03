# 🏛️ System Architecture & Engineering Blueprint
## Namma Clinic Digital Health & Operations Platform
### High-Level (C4 Model) & Low-Level Architectural Design Specification
### Document Code: TD-ARC-01 | Version: 1.0 | Date: September 2026

---

## 1. System Context & Architectural Objectives

The Namma Clinic Platform is an enterprise, modular, cloud-native primary healthcare management and epidemiological surveillance system designed for 183+ clinics serving ~4.7 million patient consultations annually across Bengaluru.

### Core Architecture Drivers:
1. **Low-Latency Frontline Experience:** Page transitions and form saves under 300 ms to avoid clinical bottlenecks.
2. **Offline-First Resilience:** Zero work interruption during erratic broadband or 4G drops via browser-level Service Workers and IndexedDB transactional caching.
3. **ABDM Native Readiness:** Architectural hooks for Ayushman Bharat Digital Mission (ABHA verification, Health Information Provider [HIP], Health Information User [HIU]).
4. **Data Separation:** Strict decoupling between transactional OLTP workloads and high-dimensional analytical OLAP workloads.
5. **Zero-Trust Security:** Strict Role-Based Access Control (RBAC), end-to-end TLS 1.3, KMS-backed AES-256 storage, and tamper-evident audit logging.

---

## 2. C4 Architecture Model

### Level 1: System Context Diagram

```
                              ┌────────────────────────────────────────┐
                              │       Bengaluru Citizen / Patient      │
                              └───────────────────┬────────────────────┘
                                                  │ (Visits clinic / receives SMS/WhatsApp)
                                                  ▼
┌─────────────────────────┐   ┌────────────────────────────────────────┐   ┌──────────────────────────┐
│  ABDM / National Health │◄─►│        NAMMA CLINIC PLATFORM           │◄─►│ State Health Analytics / │
│     Authority (NHA)     │   │   (Primary Care Healthcare Engine)     │   │  eHospital / KSDLPS ERP  │
└─────────────────────────┘   └───────────────────┬────────────────────┘   └──────────────────────────┘
                                                  ▲
                                                  │ (Daily clinic workflows & dashboards)
                              ┌───────────────────┴────────────────────┐
                              │    Clinic Doctors, Nurses, Staff,      │
                              │    Zonal Medical Officers, BBMP Admin  │
                              └────────────────────────────────────────┘
```

### Level 2: Container Diagram

```
                                  ┌──────────────────────────────────────────┐
                                  │           CLIENT CONTAINERS              │
                                  │  • Web Application (Desktop Chrome/Edge) │
                                  │  • Progressive Web App (Tablet Chrome)   │
                                  │  • Waiting Queue Display (Smart TV)      │
                                  │  • Local Service Worker + IndexedDB      │
                                  └─────────────────────┬────────────────────┘
                                                        │ HTTPS / WSS (TLS 1.3)
                                                        ▼
                                  ┌──────────────────────────────────────────┐
                                  │            GATEWAY CONTAINER             │
                                  │  • AWS Application Load Balancer / WAF   │
                                  │  • NGINX Reverse Proxy & Rate Limiter    │
                                  │  • JWT Authentication & RBAC Guard       │
                                  └─────────────────────┬────────────────────┘
                                                        │
                      ┌─────────────────────────────────┼─────────────────────────────────┐
                      ▼                                 ▼                                 ▼
         ┌─────────────────────────┐       ┌─────────────────────────┐       ┌─────────────────────────┐
         │ Core Clinical Services  │       │  Pharmacy & Inventory   │       │   Analytics & Engine    │
         │ (Next.js / Node.js API) │       │ (Next.js / Node.js API) │       │ (Python FastAPI / Node) │
         │ • Registration & Queue  │       │ • Stock Ledger          │       │ • Outbreak Cluster Flag │
         │ • Triage & Vitals       │       │ • Dispense Manager      │       │ • Stock-out Forecaster  │
         │ • Doctor EMR & Rx       │       │ • Indent Reorder Engine │       │ • Real-time Dashboards  │
         │ • Lab Orders & Results  │       │ • Expiry Watchdog       │       │ • NCD Recall Worker     │
         └────────────┬────────────┘       └────────────┬────────────┘       └────────────┬────────────┘
                      │                                 │                                 │
                      └─────────────────────────────────┼─────────────────────────────────┘
                                                        │
                                  ┌─────────────────────▼────────────────────┐
                                  │             DATA PERSISTENCE             │
                                  │  • Primary PostgreSQL 16 (Relational OLTP│
                                  │  • Read Replica PostgreSQL (Dashboard)   │
                                  │  • Redis 7 Cluster (Session & Queue)     │
                                  │  • AWS S3 Bucket (Prescriptions & Exports│
                                  │  • WORM Audit Archive (CERT-In Vault)    │
                                  └──────────────────────────────────────────┘
```

---

## 3. Offline-First Synchronization Architecture

To eliminate reliance on continuous internet connectivity in basement or peripheral clinics:

```
[User Action: Save Vitals / Issue Rx]
               │
               ▼
   [Service Worker Interceptor]
               │
       Is Network Online?
       ├───► YES: Direct API call to Central Server
       │
       └───► NO:
             1. Assign deterministic client-side UUID (v4)
             2. Write record to browser IndexedDB (`pending_sync_queue`)
             3. Update UI state optimistically (Show "Cached Offline" badge)
             4. Register Background Sync API event (`namma-sync-task`)
```

### Reconnection & Conflict Resolution Protocol
1. **Network Detection:** The client listens to `navigator.onLine` and initiates a WebSocket heartbeat.
2. **Batch Replay:** Cached mutations are pushed sequentially in order of creation timestamp (`created_at`).
3. **Idempotency:** The backend checks the incoming record UUID. If already present, it is ignored without error.
4. **Conflict Rules:**
   * **Visits, Vitals, Prescriptions, Lab Results:** Strictly **append-only**. Conflicts are logically impossible since each encounter generates unique record IDs.
   * **Patient Demographics:** **Last-Write-Wins (LWW)** with conflict logging if two clinics update the same mobile profile within 10 minutes.
   * **Pharmacy Stock Ledger:** Reconciled via transactional delta ledger rather than absolute stock overrides.

---

## 4. Ayushman Bharat Digital Mission (ABDM) Integration Flow

```
[Citizen at Reception]
          │
          ▼  (1) Citizen presents 14-digit ABHA Number or Scan-and-Share QR
[Reception Console]
          │
          ▼  (2) POST /api/v1/abdm/v3/hip/auth/init (Auth Mode: AADHAAR_OTP or MOBILE_OTP)
[Namma ABDM Adapter Service]
          │
          ▼  (3) Proxies to NHA ABDM Gateway
[NHA ABDM Production Gateway]
          │
          ▼  (4) OTP sent to citizen's registered mobile
[Citizen supplies OTP]
          │
          ▼  (5) POST /api/v1/abdm/v3/hip/auth/confirm
[ABDM Gateway responds with verified KYC (Name, Gender, DOB, Address, Photo)]
          │
          ▼  (6) Auto-populates Namma Clinic Patient Master & links ABHA handle
```

---

## 5. Network & Security Topology

1. **VPC Isolation:** All database instances and internal microservices reside in private subnets with no public IPv4 addresses.
2. **Egress Control:** Outbound traffic passes through dual-redundant NAT Gateways with strict IP whitelisting for ABDM and SMS endpoints.
3. **WAF & DDoS Mitigation:** AWS WAF enforces rate-limiting (maximum 2,000 requests per IP per 5 minutes), SQL injection inspection, and cross-site scripting (XSS) filtering.
4. **Session Security:** JWT bearer tokens signed using RS256 with 15-minute access token lifespan and HTTP-only, secure, SameSite=Strict refresh cookies.
