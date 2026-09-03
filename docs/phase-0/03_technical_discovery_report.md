# 🔧 Technical Discovery Report
## Namma Clinic Digital Health Platform — Phase 0 Deliverable 0.3
### K Mati | Kushagramati Analytics Pvt Ltd
### Date: September 2026 | Version 1.0

---

## 1. Purpose

This document covers the technical infrastructure assessment, ABDM integration requirements, hosting/cloud strategy, security compliance, and the recommended technology stack for the Namma Clinic Digital Health Platform. It informs architecture decisions in the DPR.

---

## 2. Internet Connectivity Assessment

### 2.1 Connectivity Audit Results (183 clinics)

| Category | Count | % | Connection Quality |
|---|---|---|---|
| Fibre broadband (BSNL / Jio / Airtel) — Reliable | 68 | 37% | Good (10–100 Mbps, <10ms latency) |
| Fibre broadband — Intermittent outages | 42 | 23% | Fair (10–50 Mbps, occasional 1–2h outages) |
| 4G SIM dongle (primary connectivity) | 53 | 29% | Variable (5–20 Mbps, indoor signal issues) |
| No connectivity at all | 20 | 11% | None |

### 2.2 Key Findings

1. **40% of clinics** experience internet downtime at least once per week (ranging from 10 min to 6 hours)
2. **Monsoon months** see 2x increase in outages due to power and telecom infrastructure issues
3. **Indoor 4G signal** is poor in 60% of SIM dongle clinics (ground floor, thick walls)

### 2.3 Connectivity Recommendations

| Action | Implementation | Cost Estimate |
|---|---|---|
| Install BSNL/Jio fiber at all 20 pilot clinics | Before pilot go-live | ₹2,500/month/clinic |
| Provide 4G SIM router as backup at every pilot clinic | Immediate | ₹3,000 one-time + ₹500/month |
| Deploy **offline-first architecture** in the platform | Core platform requirement | Included in dev cost |
| For 20 clinics with no internet: install fiber first | Pre-pilot infrastructure | ₹15,000 one-time + ₹2,500/month |

### 2.4 Offline Architecture Strategy

```
┌─────────────────────────────────────┐
│         CLINIC DEVICE (Browser)     │
│  ┌─────────────┐                    │
│  │ Service Worker│ ← Intercepts API │
│  └──────┬──────┘                    │
│         │                           │
│  ┌──────▼──────┐                    │
│  │ IndexedDB   │ ← Local cache     │
│  │ (Patient,   │                    │
│  │  Visit,     │                    │
│  │  Queue data) │                   │
│  └──────┬──────┘                    │
│         │ Online? → Sync Queue      │
│         │ Offline? → Queue writes   │
└─────────┼───────────────────────────┘
          │
    ┌─────▼─────┐
    │ API Server │ ← Cloud
    │ (Central)  │
    └───────────┘
```

**Sync Strategy:**
1. All **reads** served from local cache (refreshed when online)
2. All **writes** queued in IndexedDB with timestamp
3. When online: writes replayed in order to server
4. **Conflict resolution:** Last-write-wins for patient demographics; append-only for visits and prescriptions (no conflict possible)
5. **Data integrity:** Each write gets a client-generated UUID; server deduplicates on UUID

---

## 3. Power Supply Assessment

### 3.1 Audit Results

| Category | Count | % |
|---|---|---|
| Reliable power (< 2h outage/month) | 98 | 54% |
| Moderate outages (2–8h outage/month) | 57 | 31% |
| Frequent outages (> 8h/month) | 28 | 15% |

### 3.2 UPS Recommendation

| Item | Specification | Per Clinic | Pilot (20 clinics) |
|---|---|---|---|
| UPS (for desktops) | 1KVA, 30-min backup | ₹4,500 x 2 = ₹9,000 | ₹1,80,000 |
| UPS (for router/modem) | 600VA, 60-min backup | ₹2,800 x 1 | ₹56,000 |

> **Critical:** UPS must be installed at every pilot clinic **before go-live**. Platform must also auto-save all form data every 30 seconds to prevent data loss on sudden power cut.

---

## 4. ABDM Integration Requirements

### 4.1 ABDM Overview

The Ayushman Bharat Digital Mission (ABDM) is a national initiative to create a unified digital health infrastructure. Key components relevant to Namma Clinic:

| Component | Description | Namma Clinic Relevance |
|---|---|---|
| **ABHA (Health ID)** | 14-digit unique health identifier for citizens | Capture at registration |
| **HIP (Health Information Provider)** | Facility that creates health records | Namma Clinic is a HIP |
| **HIU (Health Information User)** | Facility that requests health records | Future: to fetch patient history |
| **PHR (Personal Health Record)** | Patient-facing health record locker | Future: push records to patient |
| **HIMS/HMIS Integration** | Standard APIs for health data exchange | Via ABDM gateway |

### 4.2 Phased ABDM Integration

| Phase | Scope | Timeline | Dependencies |
|---|---|---|---|
| **Phase 1 (Pilot)** | ABHA ID capture (manual entry) + verification via ABDM sandbox API | Pilot period | ABDM sandbox credentials |
| **Phase 2 (Post-Pilot)** | ABHA creation for patients who don't have one (OTP-based) | Month 6–8 | ABDM production credentials |
| **Phase 3 (Citywide)** | HIP registration — push visit records to ABHA-linked locker | Month 9–12 | ABDM HIP approval |
| **Phase 4 (Advanced)** | HIU — fetch records from other facilities with patient consent | Month 12+ | ABDM HIU approval + consent manager |

### 4.3 ABDM Technical Requirements

| Requirement | Detail |
|---|---|
| ABDM Sandbox Access | Register at sandbox.abdm.gov.in; obtain client ID and secret |
| ABHA Verification API | `POST /v1/auth/init` → `POST /v1/auth/confirm` (OTP flow) |
| FHIR Standard | Health records must be in FHIR R4 format for HIP/HIU |
| Consent Manager | Patient consent capture for record sharing (UI component) |
| Bridge URL | Callback URL registered with ABDM for HIP notifications |
| Certificate | Valid SSL certificate on the callback endpoint |
| Compliance | Must pass ABDM integration sandbox testing before production |

### 4.4 ABDM Sandbox Access Checklist

- [ ] Register on ABDM Sandbox portal
- [ ] Obtain Client ID and Client Secret
- [ ] Implement ABHA verification flow (init → OTP → confirm)
- [ ] Test ABHA creation flow (optional, Phase 2)
- [ ] Register as HIP on sandbox
- [ ] Implement FHIR R4 bundle creation for visit records
- [ ] Test health record push to sandbox PHR
- [ ] Obtain production credentials from NHA (National Health Authority)

---

## 5. eHospital Integration Assessment

### 5.1 Current State

- **eHospital** (NIC) is deployed at major government hospitals (Victoria, Bowring, Vani Vilas)
- Namma Clinics currently send **paper referrals** to these hospitals
- eHospital exposes limited APIs (registration, appointment — hospital-side only)

### 5.2 Integration Feasibility

| Integration Point | Feasibility | Notes |
|---|---|---|
| Send referral data to eHospital | 🟡 Medium | Requires NIC coordination; no open API |
| Receive referral acknowledgment | 🔴 Low | eHospital doesn't have outbound notification |
| Share patient demographics | 🟡 Medium | Via ABDM bridge (future) |
| Share visit records | 🟢 Via ABDM | Standard HIP → HIU flow |

### 5.3 Recommendation

For the pilot, referrals will be **self-contained** within the Namma Clinic platform (digital slip + SMS to patient). eHospital integration to be pursued post-pilot through NIC coordination and the ABDM bridge.

---

## 6. Hosting & Cloud Strategy

### 6.1 Options Evaluated

| Option | Provider | Data Location | Compliance | Cost (est.) | Recommendation |
|---|---|---|---|---|---|
| **AWS (ap-south-1)** | Amazon | Mumbai, India | MeitY-empanelled | ₹1.5–2.5L/month | ✅ Recommended for Pilot |
| **Azure (Central India)** | Microsoft | Pune, India | MeitY-empanelled | ₹1.5–2.5L/month | ✅ Alternative |
| **NIC Cloud / MeghRaj** | NIC / MeitY | Delhi/Hyderabad | Government-owned | ₹0.8–1.5L/month | ✅ Preferred for Citywide |
| **KSDC (Karnataka State Data Centre)** | Govt of Karnataka | Bengaluru | State-owned | ₹0.5–1.0L/month | 🟡 To be explored |

### 6.2 Recommended Architecture

```
                    ┌───────────────────────────────────────┐
                    │        AWS ap-south-1 (Mumbai)        │
                    │  ┌─────────────────────────────────┐  │
                    │  │         Load Balancer (ALB)      │  │
                    │  └──────────┬──────────────────────┘  │
                    │             │                          │
                    │  ┌──────────▼──────────┐              │
                    │  │  App Server (ECS/EC2) │             │
                    │  │  Next.js + Node.js    │             │
                    │  │  API Layer            │             │
                    │  └──────────┬──────────┘              │
                    │             │                          │
                    │  ┌──────────▼──────────┐              │
                    │  │  PostgreSQL (RDS)     │             │
                    │  │  Primary + Read Replica│            │
                    │  └──────────┬──────────┘              │
                    │             │                          │
                    │  ┌──────────▼──────────┐              │
                    │  │  Redis (ElastiCache)  │             │
                    │  │  Sessions + Cache     │             │
                    │  └─────────────────────┘              │
                    │                                       │
                    │  ┌─────────────────────┐              │
                    │  │  S3 (Document Store)  │             │
                    │  │  PDFs, Exports        │             │
                    │  └─────────────────────┘              │
                    │                                       │
                    │  ┌─────────────────────┐              │
                    │  │  CloudWatch + Grafana │             │
                    │  │  Monitoring & Alerts  │             │
                    │  └─────────────────────┘              │
                    └───────────────────────────────────────┘
```

### 6.3 Estimated Monthly Cloud Cost (Pilot: 20 clinics)

| Resource | Specification | Monthly Cost |
|---|---|---|
| Application Server (ECS/EC2) | 2x t3.medium (HA) | ₹18,000 |
| PostgreSQL (RDS) | db.t3.medium, Multi-AZ | ₹22,000 |
| Redis (ElastiCache) | cache.t3.micro | ₹4,000 |
| S3 Storage | 50 GB | ₹500 |
| Load Balancer (ALB) | 1 ALB | ₹3,000 |
| CloudWatch | Logs + Metrics | ₹2,000 |
| Data Transfer | ~100 GB/month | ₹2,500 |
| SSL Certificate | ACM (free) | ₹0 |
| **Total** | | **~₹52,000/month** |

> **Note:** For citywide (200 clinics), scale to `t3.xlarge` app servers and `db.r5.large` RDS. Estimated: ₹1.8–2.5L/month.

---

## 7. Security & Compliance

### 7.1 CERT-In Compliance Requirements

| # | Requirement | Implementation |
|---|---|---|
| 1 | Report cyber security incidents within 6 hours | Integrate with CERT-In portal; configure alerts |
| 2 | Maintain logs for 180 days | CloudWatch Logs retention = 180 days |
| 3 | Synchronize system clocks with NTP | All servers sync to NTP pool |
| 4 | Designate a Point of Contact for CERT-In | K Mati CISO / Security Lead |
| 5 | Enable logs on: firewalls, IDS, proxy, auth | All AWS service logs enabled |

### 7.2 Data Security Architecture

| Layer | Measure |
|---|---|
| **Transit** | TLS 1.2+ on all API endpoints; HSTS header; certificate pinning |
| **At Rest** | AES-256 encryption on RDS, S3, EBS volumes |
| **Application** | RBAC with 8 defined roles; JWT tokens with 15-min expiry + refresh |
| **Authentication** | Username/password + MFA (TOTP) for Admin and Commissioner roles |
| **Audit** | Every API call logged with user ID, IP, timestamp, action |
| **Network** | VPC with private subnets for DB; Security Groups; no public DB access |
| **VAPT** | CERT-In empanelled auditor — quarterly VAPT starting before pilot |
| **Backup** | Daily automated RDS snapshots; 30-day retention; tested restore monthly |

### 7.3 Data Ownership

| Aspect | Policy |
|---|---|
| Data Owner | GBA / BBMP Health Department (100%) |
| Data Processor | K Mati (under contract) |
| Data Portability | Open APIs + standard data dictionary; no vendor lock-in |
| Data Retention | Patient records retained indefinitely per clinical requirements |
| Data Deletion | On contract termination: full data handover in open format (CSV/JSON/SQL dump) within 30 days |
| Data Access | Only authorized clinic staff per RBAC; no K Mati employee has clinical data access in production without written authorization |

### 7.4 Privacy Impact Assessment Summary

| Risk | Severity | Mitigation |
|---|---|---|
| Unauthorized access to patient records | High | RBAC + MFA + audit logs + session timeout (15 min) |
| Data breach / exfiltration | High | Encryption at rest + transit; no data on laptops; VPC isolation |
| Staff sharing credentials | Medium | Individual accounts mandatory; shared login detection + alert |
| Device theft at clinic | Medium | No local data storage (browser only); session auto-expires |
| Third-party data exposure | Low | No third-party analytics; data stays in government cloud |

---

## 8. Recommended Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| **Frontend** | Next.js 16 (React, TypeScript) | Server-side rendering for SEO; app router; fast navigation |
| **Frontend (Tablet)** | Progressive Web App (PWA) | Works offline via Service Worker; installable; no app store |
| **Backend API** | Node.js with Express / Fastify | JavaScript ecosystem consistency; high throughput |
| **Database** | PostgreSQL 16 (RDS) | Proven for healthcare; JSONB for flexible schemas; strong ACID |
| **Cache** | Redis 7 | Session storage, queue state caching, rate limiting |
| **Search** | PostgreSQL Full-Text Search (pg_trgm) | No need for Elasticsearch at this scale; simpler ops |
| **Authentication** | Custom JWT + bcrypt | Lightweight; RBAC tables in PostgreSQL |
| **PDF Generation** | Puppeteer (headless Chrome) | Bilingual prescriptions with Kannada fonts |
| **SMS Gateway** | MSG91 (DLT-registered) | India-compliant; Kannada template support |
| **File Storage** | AWS S3 | PDFs, exports, documents |
| **Analytics** | PostgreSQL materialized views + custom dashboards | Keep it simple for MVP; upgrade to ClickHouse/BigQuery post-pilot |
| **Monitoring** | Grafana + Prometheus + Sentry | Open-source; comprehensive dashboards |
| **CI/CD** | GitHub Actions | Integrated with codebase; automated testing and deployment |
| **ABDM** | ABDM SDK (Node.js) | Official sandbox + production APIs |

---

## 9. Performance Requirements

| Metric | Requirement | Notes |
|---|---|---|
| Page load time | < 3 seconds on 4G | Includes first contentful paint |
| API response time (p95) | < 500ms | For search, registration, vitals save |
| Concurrent users per clinic | Up to 5 | Reception + Nurse + Doctor + Pharmacist + Lab |
| Total concurrent users (citywide) | 1,000+ | 200 clinics × 5 users |
| Database queries per second | 500+ | With connection pooling and read replicas |
| Uptime SLA | 99.5% | Excluding planned maintenance windows |
| Data sync latency (offline → online) | < 30 seconds | When connection restores |

---

## 10. Risk Register — Technical Risks

| # | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| T1 | Internet outage at clinic disrupts operations | High | High | Offline-first architecture with sync |
| T2 | Power outage causes data loss | Medium | High | UPS + auto-save every 30 seconds |
| T3 | ABDM sandbox API changes without notice | Medium | Medium | Abstract ABDM calls behind adapter; version-lock APIs |
| T4 | Clinic staff bypass platform, revert to paper | High | High | Mandatory digital-first policy from BBMP; helpdesk support |
| T5 | Cloud hosting cost escalation | Low | Medium | Reserved instances; cost alerts at 80% budget |
| T6 | Security breach due to weak passwords | Medium | Critical | MFA for admins; password policy enforcement |
| T7 | Kannada font rendering inconsistent across devices | Medium | Medium | Use Noto Sans Kannada (Google Fonts); test on all target devices |
| T8 | VAPT reveals critical vulnerabilities before pilot | Low | High | VAPT scheduled 2 weeks before pilot; fix window included |

---

**Document Control**

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | Sep 2, 2026 | K Mati — Solution Architecture Team | Initial release |

---
*© 2026 Kushagramati Analytics Pvt Ltd. Confidential — Prepared for GBA / BBMP Health Department.*
