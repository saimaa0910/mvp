# 🚀 Software Release Strategy (Releases 00 through 07)
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-REL-15 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Phased Release Architecture

| Release ID | Name / Codename | Sprints | Primary Focus & Deliverables |
| :--- | :--- | :--- | :--- |
| **REL-00** | Foundation & Core Infra | S01 - S02 | DB Schema, Base APIs, Auth/RBAC, Audit Logging, CI/CD pipelines. |
| **REL-01** | Core Patient & Queue | S03 - S04 | Patient Registration, Demographics, Token Generation, Vitals Triage. |
| **REL-02** | Clinical Encounter & EMR | S05 - S06 | Doctor Console, Diagnosis Coding, Electronic Prescription, History. |
| **REL-03** | Pharmacy, Lab & Referral| S07 - S08 | Drug Dispensing, Batch Tracking, 14 Lab Tests, Outbound Referrals. |
| **REL-04** | Analytics & Offline Core | S09 - S10 | IndexedDB Offline Cache, Background Sync, Public Health Metrics DW. |
| **REL-05** | 20-Clinic Pilot Release | S11 - S12 | Field Deployment across 20 Clinics, SLA Monitoring, User Feedback. |
| **REL-06** | Production Citywide Scale| S13 - S14 | Performance Tuning, High-Concurrency Load, Rollout to 183 Clinics. |
| **REL-07** | AI Insights & ABDM Native| S15 - S16 | Stock Forecasting, Fever Anomaly Alerts, ABHA Linking, FHIR R4. |
