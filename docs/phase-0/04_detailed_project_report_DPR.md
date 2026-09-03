# 📑 Detailed Project Report (DPR)
## Namma Clinic Digital Health & Operations Platform
### Submitted by: Kushagramati Analytics Pvt Ltd (K Mati)
### Submitted to: Greater Bengaluru Authority (GBA) / BBMP Health Department
### Attn: Sri Venkata Rao Chalapathi, IAS, Special Commissioner
### Date: September 2026 | Version 1.0

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement & Opportunity](#2-problem-statement--opportunity)
3. [Project Scope & Objectives](#3-project-scope--objectives)
4. [Functional Architecture](#4-functional-architecture)
5. [Technical Architecture](#5-technical-architecture)
6. [Implementation Roadmap](#6-implementation-roadmap)
7. [Pilot Plan (20 Clinics)](#7-pilot-plan-20-clinics)
8. [Training & Change Management](#8-training--change-management)
9. [Data Governance & Security](#9-data-governance--security)
10. [Financial Estimates](#10-financial-estimates)
11. [Risk Management](#11-risk-management)
12. [Success Criteria & KPIs](#12-success-criteria--kpis)
13. [Team Structure](#13-team-structure)
14. [Annexures](#14-annexures)

---

## 1. Executive Summary

The **Namma Clinic Digital Health & Operations Platform** is a comprehensive, EMR-lite, ABDM-ready primary care platform designed to digitize all clinical and operational workflows across Bengaluru's 183+ operational Namma Clinics.

### Why This Matters

| Today (Manual) | With Platform (Digital) |
|---|---|
| Paper registers, lost records | Searchable digital patient database |
| Illegible prescriptions | Bilingual (Kannada + English) digital prescriptions |
| No real-time visibility for zonal/city officers | Live dashboards: footfall, stock, diseases |
| Stock-outs discovered after depletion | Predictive stock alerts 7–14 days before stock-out |
| Referrals lost as paper slips | Tracked digital referrals with SMS follow-up |
| Monthly reports take 2–3 days to compile | Auto-generated, real-time reports |
| No NCD follow-up tracking | Automated recall system for HTN/DM patients |
| No ABDM/ABHA integration | ABHA-ready from day one |

### Key Numbers

| Metric | Current | With Platform |
|---|---|---|
| Patient registration time | 4–6 min (new) | 2–4 min (new), 1–2 min (repeat) |
| Prescription generation | 6–10 min (handwritten) | 3–6 min (template + digital) |
| Monthly report compilation | 2–3 days/clinic | Automated (zero manual effort) |
| Referral tracking rate | < 5% | 100% digital tracking |
| Stock-out early warning | None | 7–14 day predictive alert |
| Clinics covered | 0 (all paper) | 183+ (phased rollout) |

### Investment Summary

| Scope | Year 1 Cost | Year 2+ Annual Cost |
|---|---|---|
| 20-Clinic Pilot | ₹1.65 Crore | — |
| 200-Clinic Citywide | ₹12.80 Crore | ₹5.4–5.8 Crore/year |

---

## 2. Problem Statement & Opportunity

### 2.1 Current Challenges

1. **No Digital Records:** All 183 clinics operate on paper registers. Patient history is unavailable across visits.
2. **No Governance Visibility:** BBMP Health HQ has no real-time view of clinic operations. Issues surface weeks later.
3. **Medication Stock-Outs:** Pharmacies run out of essential medicines with no predictive system. Patients turned away.
4. **Lost Referrals:** Paper referral slips have < 5% follow-through rate. Patients fall through cracks.
5. **Manual Reporting Burden:** Nurses and DEOs spend 2–3 days/month compiling reports, reducing clinical time.
6. **No NCD Tracking:** Hypertension and diabetes patients who miss follow-ups are never recalled.
7. **No ABDM Compliance:** State mandate to capture ABHA IDs is unfulfilled.

### 2.2 Opportunity

Bengaluru's Namma Clinics serve **~395,000 patients/month** across **183 operational locations** — the largest urban primary healthcare network in Karnataka. Digitizing this network creates:

- **India's largest city-level primary care digital health dataset**
- **Real-time disease surveillance** covering all zones of Bengaluru
- **A replicable model** for other cities and states under NHM/ABDM

---

## 3. Project Scope & Objectives

### 3.1 In Scope

| Module | Description |
|---|---|
| Patient Registration & Queue | Digital patient master, ABHA capture, token generation |
| Triage / Nurse Station | Vitals capture, danger flag detection, chief complaints |
| Doctor EMR Console | Clinical notes, templates, prescriptions, lab orders, referrals |
| Pharmacy & Inventory | Dispense tracking, stock ledger, alerts, indent management |
| Lab & Diagnostics | Test ordering, sample tracking, result entry |
| Referrals | Digital referral slips, status tracking, SMS notifications |
| Analytics & Dashboards | Clinic / Zone / Commissioner dashboards, AI flags |
| ABDM Integration | ABHA capture and verification (Phase 1) |
| Offline Support | Service Worker + IndexedDB caching for clinic resilience |
| Bilingual Output | Kannada + English prescriptions, slips, SMS |

### 3.2 Out of Scope (for this project phase)

- Hospital Information System (HIS) for secondary/tertiary hospitals
- Patient-facing mobile app (future Phase 5)
- Telemedicine video integration (future Phase 5)
- Insurance/billing/payment processing
- Biometric authentication

### 3.3 Guiding Principles

1. **Clinic-first:** Minimum typing, maximum quick-picks and templates
2. **Citizen-first:** Bilingual output, SMS reminders, clear prescriptions
3. **ABDM-ready:** ABHA from day one; full integration in phases
4. **Data-governed:** 100% government-owned data; no vendor lock-in
5. **Outcome-led:** Real-time KPIs, not just software deployment

---

## 4. Functional Architecture

### 4.1 Module Map

```
┌───────────────────────────────────────────────────────────────┐
│                    NAMMA CLINIC PLATFORM                      │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────┐  ┌────────┐  ┌──────────┐  ┌──────────┐       │
│  │Reception │→│ Triage  │→│ Doctor   │→│ Pharmacy │        │
│  │& Queue   │  │(Nurse)  │  │ EMR      │  │& Stock   │        │
│  └──────────┘  └────────┘  └──────────┘  └──────────┘       │
│       ↕                        ↕              ↕               │
│  ┌──────────┐           ┌──────────┐  ┌──────────┐          │
│  │ Patient  │           │ Lab &    │  │ Referral │          │
│  │ Master   │           │ Diagnost.│  │ Tracking │          │
│  └──────────┘           └──────────┘  └──────────┘          │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│  ANALYTICS LAYER                                              │
│  ┌──────────────┐ ┌───────────────┐ ┌───────────────────┐   │
│  │ Clinic Dash  │ │ Zone Dash     │ │Commissioner Dash  │   │
│  └──────────────┘ └───────────────┘ └───────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ AI: Stock Forecast | Disease Clusters | NCD Recall   │   │
│  └──────────────────────────────────────────────────────┘   │
├───────────────────────────────────────────────────────────────┤
│  CROSS-CUTTING: ABDM | Offline Sync | Bilingual | SMS       │
└───────────────────────────────────────────────────────────────┘
```

### 4.2 User Roles & Access Matrix

| Role | Registration | Triage | Doctor EMR | Pharmacy | Lab | Referrals | Analytics |
|---|---|---|---|---|---|---|---|
| Reception Clerk | ✅ Full | ❌ | ❌ | ❌ | ❌ | 👁 View | ❌ |
| Nurse | ✅ Full | ✅ Full | 👁 View | ❌ | ❌ | 👁 View | ❌ |
| Doctor (MO) | 👁 View | 👁 View | ✅ Full | ❌ | 👁 View | ✅ Full | 👁 Clinic |
| Pharmacist | ❌ | ❌ | 👁 View Rx | ✅ Full | ❌ | ❌ | ❌ |
| Lab Technician | ❌ | ❌ | 👁 View Orders | ❌ | ✅ Full | ❌ | ❌ |
| Clinic Admin | ✅ Full | 👁 View | 👁 View | 👁 View | 👁 View | 👁 View | ✅ Clinic |
| Zonal MO | ❌ | ❌ | ❌ | ❌ | ❌ | 👁 Zone | ✅ Zone |
| Commissioner | ❌ | ❌ | ❌ | ❌ | ❌ | 👁 All | ✅ City |

---

## 5. Technical Architecture

### 5.1 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   CLIENT TIER                           │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Desktop     │  │ Android      │  │ Queue Display│  │
│  │ (Browser)   │  │ Tablet (PWA) │  │ (Browser)    │  │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                │                  │           │
│         └────────────────┼──────────────────┘           │
│                          │ HTTPS                        │
└──────────────────────────┼──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│                   API GATEWAY                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Load Balancer (ALB) + WAF + Rate Limiting       │   │
│  └─────────────────────┬───────────────────────────┘   │
│                        │                                │
│         ┌──────────────┼──────────────┐                │
│         ▼              ▼              ▼                │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐         │
│  │ App Server │ │ App Server │ │ App Server │         │
│  │ (Node.js)  │ │ (Node.js)  │ │ (Node.js)  │         │
│  └──────┬─────┘ └──────┬─────┘ └──────┬─────┘         │
│         └──────────────┼──────────────┘                │
│                        │                                │
│  ┌─────────────────────▼───────────────────────────┐   │
│  │                DATA TIER                         │   │
│  │  ┌───────────┐  ┌──────┐  ┌───────┐  ┌──────┐ │   │
│  │  │PostgreSQL │  │Redis │  │  S3   │  │ABDM  │ │   │
│  │  │(Primary + │  │Cache │  │Storage│  │Bridge│ │   │
│  │  │ Replica)  │  │      │  │       │  │      │ │   │
│  │  └───────────┘  └──────┘  └───────┘  └──────┘ │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ MONITORING: Grafana + Prometheus + Sentry        │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Database Schema (Core Entities)

| Entity | Key Fields | Relationships |
|---|---|---|
| `patients` | id, patient_id, name, name_kn, age, gender, mobile, abha_id, address, blood_group, known_conditions | 1:N → visits |
| `visits` | id, patient_id, token, service_type, status, date, clinic_id, doctor_id | 1:1 → vitals, 1:N → prescriptions, lab_orders, referrals |
| `vitals` | id, visit_id, bp_sys, bp_dia, pulse, temp, spo2, blood_sugar, weight, height, bmi, chief_complaint | N:1 → visit |
| `prescriptions` | id, visit_id, medicine, dosage, frequency, duration, instructions, dispensed | N:1 → visit |
| `stock` | id, clinic_id, medicine, category, current_stock, min_threshold, expiry_date, batch_no | Per clinic |
| `lab_orders` | id, visit_id, test_name, status, result, result_value, ordered_at, completed_at | N:1 → visit |
| `referrals` | id, visit_id, patient_id, destination, reason, status, created_at | N:1 → visit |
| `users` | id, name, role, clinic_id, email, password_hash, mfa_enabled | RBAC |
| `clinics` | id, code, name, zone, ward, address, status | Master |
| `audit_log` | id, user_id, action, entity, entity_id, timestamp, ip_address | Compliance |

### 5.3 API Design (Core Endpoints)

| Endpoint | Method | Description | Auth |
|---|---|---|---|
| `/api/patients` | POST | Create patient | Reception, Nurse |
| `/api/patients/search` | GET | Search by mobile/ID/ABHA/name | All clinic roles |
| `/api/patients/:id` | GET/PUT | Get/update patient | Clinic roles |
| `/api/visits` | POST | Create visit + token | Reception, Nurse |
| `/api/visits/:id/vitals` | PUT | Save vitals | Nurse |
| `/api/visits/:id/clinical-note` | PUT | Save consultation | Doctor |
| `/api/visits/:id/prescriptions` | POST | Add prescription | Doctor |
| `/api/visits/:id/lab-orders` | POST | Order lab tests | Doctor |
| `/api/visits/:id/referrals` | POST | Create referral | Doctor |
| `/api/pharmacy/pending` | GET | Get pending prescriptions | Pharmacist |
| `/api/pharmacy/dispense` | POST | Mark dispensed | Pharmacist |
| `/api/stock` | GET/PUT | Stock ledger | Pharmacist |
| `/api/lab/pending` | GET | Pending lab orders | Lab Tech |
| `/api/lab/:id/result` | PUT | Enter result | Lab Tech |
| `/api/dashboard/:level` | GET | Analytics data | By role/level |
| `/api/abdm/verify-abha` | POST | Verify ABHA ID | Reception |

---

## 6. Implementation Roadmap

| Phase | Duration | Activities | Deliverables |
|---|---|---|---|
| **Phase 0: Discovery & DPR** | 4 weeks ✅ | Field research, workflow mapping, DPR drafting | This document + supporting reports |
| **Phase 1: Prototype** | 4 weeks | Clickable prototype, sandbox environment, design system | Interactive demo for stakeholder sign-off |
| **Phase 2: Core Development** | 8–10 weeks | Full platform build: all 7 modules + offline + ABDM | Working platform on staging |
| **Phase 3: Pilot (20 clinics)** | 10 weeks | Hardware deployment, training, go-live, support | 20 clinics live |
| **Phase 4: Hardening** | 4 weeks | Bug fixes, VAPT, performance tuning, UX refinement | VAPT-cleared, production-ready build |
| **Phase 5: Citywide Rollout** | 4–6 months | Wave deployment (40 → 50 → 50 → remaining) | All 183+ clinics live |
| **Phase 6: Optimization** | 3 months | AI features, advanced analytics, patient app | AI flags, disease surveillance, chatbot |

### Timeline Visualization

```
Month:  1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18
        ├────┤    ├────┤    ├──────────┤    ├──────────┤    ├────┤    ├──────────────────────────┤    ├──────────┤
Phase:  P0        P1        P2              P3              P4        P5 (Citywide)                   P6 (Opt)
        Discovery Proto     Core Dev        Pilot           Harden    Wave 1→2→3→4                    AI/ML
```

---

## 7. Pilot Plan (20 Clinics)

### 7.1 Clinic Selection Criteria

| Criterion | Rationale |
|---|---|
| Representation from all 5 zones | 4 clinics per zone |
| Mix of footfall volumes | 7 high (>80/day), 8 medium (50–80/day), 5 low (<50/day) |
| Reliable internet availability | Preferably fiber; 4G backup must be in place |
| Willing staff / supportive MO | Doctor should be digitally amenable |
| Functional lab facility | At least 12 of 20 should have lab tech |

### 7.2 Proposed Pilot Clinics

| # | Zone | Clinic Code | Name | Footfall | Internet |
|---|---|---|---|---|---|
| 1 | North | NC-N-001 | Yelahanka New Town | 82 | Fiber |
| 2 | North | NC-N-003 | Sahakarnagar | 74 | Fiber |
| 3 | North | NC-N-005 | Hebbal | 91 | Fiber |
| 4 | North | NC-N-004 | Dasarahalli | 55 | 4G |
| 5 | South | NC-S-001 | Bommanahalli | 95 | Fiber |
| 6 | South | NC-S-002 | BTM 2nd Stage | 88 | Fiber |
| 7 | South | NC-S-004 | Koramangala | 103 | Fiber |
| 8 | South | NC-S-005 | JP Nagar | 79 | Fiber |
| 9 | East | NC-E-001 | Mahadevapura | 64 | Fiber |
| 10 | East | NC-E-003 | Whitefield | 76 | Fiber |
| 11 | East | NC-E-002 | KR Puram | 58 | 4G |
| 12 | East | NC-E-005 | Hoodi | 61 | 4G |
| 13 | West | NC-W-001 | Rajajinagar | 88 | Fiber |
| 14 | West | NC-W-002 | Vijayanagar | 81 | Fiber |
| 15 | West | NC-W-003 | Nagarbhavi | 72 | 4G |
| 16 | West | NC-W-004 | Basaveshwaranagar | 66 | Fiber |
| 17 | Central | NC-C-001 | Shivajinagar | 112 | Fiber |
| 18 | Central | NC-C-002 | Chickpet | 98 | Fiber |
| 19 | Central | NC-C-003 | Basavanagudi | 85 | Fiber |
| 20 | Central | NC-C-004 | Chamarajpet | 63 | 4G |

### 7.3 Pilot Success Criteria

| KPI | Target | Measurement |
|---|---|---|
| Digital registration adoption | ≥ 80% of daily OPD captured digitally | Platform data vs. manual register count |
| Prescription digitization | ≥ 70% of prescriptions via platform | Digital Rx count vs. total consultations |
| Dashboard availability | Real-time, < 5 min data delay | System monitoring |
| Stock alert accuracy | 100% of stock-outs predicted ≥ 3 days ahead | Stock-out events vs. alerts generated |
| User satisfaction (staff) | ≥ 3.5 / 5 rating | Post-pilot staff survey |
| Patient satisfaction | ≥ 4.0 / 5 rating | Exit survey sample (n=100) |
| System uptime | ≥ 99% | Monitoring dashboard |
| Security | Zero critical VAPT findings unresolved | VAPT report |

---

## 8. Training & Change Management

### 8.1 Training Plan

| Role | Duration | Method | Materials |
|---|---|---|---|
| Reception Clerk | 4 hours | In-person at clinic | Laminated quick-ref card, video guide (Kannada) |
| Nurse | 6 hours | In-person at clinic | Quick-ref card, vitals entry practice session |
| Doctor (MO) | 4 hours | In-person + sandbox practice | Template guide, prescription demo, shortcut sheet |
| Pharmacist | 4 hours | In-person at clinic | Stock management guide, dispensing practice |
| Lab Technician | 3 hours | In-person at clinic | Lab module walkthrough, result entry practice |
| Clinic Admin | 2 hours | Online/in-person | Dashboard training, report generation |
| Zonal MO | 2 hours | Online session | Dashboard drill-down, alert management |

### 8.2 Change Management Strategy

| Challenge | Strategy |
|---|---|
| Staff resistance to digital | Start with "digital + paper parallel" for 2 weeks, then phase out paper |
| Typing aversion | Quick-pick buttons for complaints; dropdowns for medicines; minimal free-text |
| Fear of technology | On-site champion at each clinic (usually the youngest staff member) |
| Lack of incentive | Recognition: "Digital Clinic of the Month" award from BBMP Commissioner |
| Ongoing support | Helpdesk: phone + WhatsApp during working hours; response SLA < 30 min |

---

## 9. Data Governance & Security

*See Deliverable 0.3 (Technical Discovery Report) for full details. Key highlights:*

| Aspect | Commitment |
|---|---|
| **Data Ownership** | 100% GBA / BBMP Health Department |
| **Hosting** | MeitY-empanelled cloud, India region |
| **Encryption** | TLS 1.2+ in transit, AES-256 at rest |
| **Access Control** | RBAC with 8 roles; MFA for admin/commissioner |
| **Audit** | Every action logged with user ID, timestamp, IP |
| **VAPT** | CERT-In empanelled auditor; quarterly testing |
| **Backup** | Daily automated backups; 30-day retention |
| **Data Portability** | Open APIs, standard data dictionary; no vendor lock-in |

---

## 10. Financial Estimates

### 10.1 Pilot Budget (20 Clinics)

| Line Item | Amount (₹) |
|---|---|
| Discovery & clinic selection | 15,00,000 |
| Platform configuration & prototype | 45,00,000 |
| Clinic devices & peripherals | 25,00,000 |
| Training & change management | 16,00,000 |
| Hosting, helpdesk & support (10 weeks) | 18,00,000 |
| Analytics & reporting setup | 25,00,000 |
| Security (VAPT) & contingency | 21,00,000 |
| **Total Pilot Cost** | **₹1,65,00,000 (₹1.65 Crore)** |

### 10.2 Citywide Budget (200 Clinics)

| Line Item | Year 1 (₹) | Year 2+ (₹/year) |
|---|---|---|
| Platform development | 2,25,00,000 | — |
| Clinic hardware & peripherals | 2,50,00,000 | 25,00,000 (replacements) |
| Hosting, helpdesk & support | 4,40,00,000 | 3,80,00,000 |
| Training & change management | 1,60,00,000 | 40,00,000 |
| Dashboards & analytics | 95,00,000 | 30,00,000 |
| ABDM & API integration | 75,00,000 | 15,00,000 |
| VAPT & security | 55,00,000 | 25,00,000 |
| PMO & governance | 40,00,000 | 25,00,000 |
| Contingency (10%) | 1,15,00,000 | — |
| **Year Total** | **₹12,80,00,000 (₹12.80 Cr)** | **₹5,40,00,000 (₹5.4 Cr)** |

### 10.3 Payment Milestones

| Milestone | % | Amount (Pilot) | Trigger |
|---|---|---|---|
| Kickoff | 10% | ₹16.5L | Contract execution |
| DPR Approval | 10% | ₹16.5L | DPR signed by BBMP |
| Prototype Demo | 15% | ₹24.75L | Prototype accepted |
| Pilot Go-Live | 20% | ₹33.0L | 20 clinics live |
| Pilot Acceptance | 15% | ₹24.75L | Success criteria met |
| Rollout Completion | 20% | ₹33.0L | All waves deployed |
| Final Handover | 10% | ₹16.5L | Documentation + handover |

---

## 11. Risk Management

| # | Risk | Probability | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | Staff resistance to digital adoption | High | High | Parallel run, on-site champions, incentives | K Mati Field Lead |
| R2 | Internet outages at clinics | High | High | Offline-first architecture; 4G backup | K Mati Tech Lead |
| R3 | Budget approval delays | Medium | High | Present pilot (₹1.65 Cr) separately for faster approval | K Mati Project Director |
| R4 | ABDM API changes mid-project | Medium | Medium | Abstraction layer; version-lock API calls | K Mati Solution Architect |
| R5 | Staff transfers/reassignment | Medium | Medium | Train-the-trainer model; video training library | K Mati Training Lead |
| R6 | Security breach / data leak | Low | Critical | VAPT, encryption, MFA, audit logs, incident response plan | K Mati CISO |
| R7 | Vendor dependency / lock-in concern from BBMP | Low | Medium | Open APIs, standard data formats, full data handover clause | K Mati Project Director |
| R8 | Scope creep during development | Medium | Medium | Change control board; signed-off DPR as scope baseline | K Mati PM |

---

## 12. Success Criteria & KPIs

### 12.1 Pilot Phase KPIs (10 weeks)

| Category | KPI | Target |
|---|---|---|
| **Adoption** | % of OPD registrations captured digitally | ≥ 80% |
| **Adoption** | % of prescriptions generated digitally | ≥ 70% |
| **Efficiency** | Average time from registration to prescription print | < 20 min |
| **Stock** | % of stock-outs predicted ≥ 3 days in advance | 100% |
| **Quality** | Referral digital tracking rate | 100% |
| **Dashboard** | Data freshness on Commissioner dashboard | < 5 min lag |
| **Satisfaction** | Staff NPS (Net Promoter Score) | > +20 |
| **Technical** | System uptime | ≥ 99% |
| **Security** | Unresolved critical VAPT findings | 0 |

### 12.2 Citywide Phase KPIs (annual)

| KPI | Year 1 Target |
|---|---|
| Clinics live on platform | 183+ |
| Total patients registered digitally | > 4 million records |
| NCD patients with active follow-up | > 50,000 |
| Stock-out incidents (after platform) | < 5% of pre-platform rate |
| Disease cluster alerts generated | Real-time |
| ABHA IDs captured | > 1 million |

---

## 13. Team Structure

### K Mati Core Delivery Team

| Role | Responsibility | Allocation |
|---|---|---|
| **Project Director** | Overall delivery, BBMP liaison, escalations | Full-time |
| **Clinical Advisor** (Doctor) | Workflow accuracy, template design, training content | Part-time (3 days/week) |
| **Solution Architect** | System design, tech stack, ABDM integration | Full-time |
| **Frontend Lead** | UI/UX, responsive design, Kannada rendering | Full-time |
| **Backend Lead** | API development, database, integrations | Full-time |
| **Data/Analytics Lead** | Dashboard design, ETL, AI decision support | Full-time |
| **QA Lead** | Testing, VAPT coordination, UAT | Full-time |
| **Field Implementation Lead** | Clinic site prep, hardware, training, go-live support | Full-time |
| **DevOps Engineer** | CI/CD, cloud infra, monitoring, backups | Full-time |
| **Helpdesk (2 agents)** | L1 support: phone + WhatsApp during clinic hours | Full-time |

### BBMP / GBA Counterparts (Required)

| Role | Responsibility |
|---|---|
| **Project Sponsor** | Budget approval, policy decisions (Special Commissioner) |
| **Nodal Officer** | Day-to-day coordination, clinic access facilitation |
| **Zonal Medical Officers (5)** | Zone-level coordination, staff alignment |
| **IT Cell Coordinator** | NIC / KSDC coordination, ABDM liaison |

---

## 14. Annexures

| Annexure | Document | Location |
|---|---|---|
| A | Stakeholder & Field Research Report | [`01_stakeholder_field_research_report.md`](./01_stakeholder_field_research_report.md) |
| B | Workflow Mapping Document (all 12 workflows) | [`02_workflow_mapping.md`](./02_workflow_mapping.md) |
| C | Technical Discovery Report | [`03_technical_discovery_report.md`](./03_technical_discovery_report.md) |
| D | Executive Pitch Deck (10 slides) | [`05_executive_pitch_deck.md`](./05_executive_pitch_deck.md) |
| E | Pilot Commercial Term Sheet | [`06_pilot_term_sheet.md`](./06_pilot_term_sheet.md) |
| F | Data Privacy & Governance Annexure | [`07_data_privacy_governance.md`](./07_data_privacy_governance.md) |
| G | Cover Letter to Special Commissioner | [`08_cover_letter.md`](./08_cover_letter.md) |
| H | Hardware Audit Template | [`templates/hardware_audit_template.md`](./templates/hardware_audit_template.md) |
| I | Stakeholder Interview Template | [`templates/stakeholder_interview_template.md`](./templates/stakeholder_interview_template.md) |
| J | Workshop Agenda Template | [`templates/workshop_agenda.md`](./templates/workshop_agenda.md) |

---

**Document Control**

| Version | Date | Author | Reviewed By | Status |
|---|---|---|---|---|
| 1.0 | Sep 2, 2026 | K Mati — Project Director | — | Draft for BBMP Review |
| — | — | — | Special Commissioner, GBA | Pending Approval |

---
*© 2026 Kushagramati Analytics Pvt Ltd. Confidential — Prepared for GBA / BBMP Health Department.*
