#!/usr/bin/env python3
"""
make_core_data.py
Constructs the comprehensive, authentic canonical dataset for the Namma Clinic
Project Management suite and outputs scripts/project_management/pm_core_data.py.
"""

import os
import sys

def generate_pm_core_data():
    out_file = os.path.join(os.path.dirname(__file__), "pm_core_data.py")
    print(f"Building comprehensive PM Core Data at {out_file}...")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write('"""\n')
        f.write('pm_core_data.py\n')
        f.write('Canonical Data Dictionary for Namma Clinic Digital Health & Operations Platform.\n')
        f.write('Provides stable, unique IDs, relational links, and deep domain metadata for 20 PM documents.\n')
        f.write('"""\n\n')

        # -------------------------------------------------------------------------
        # 1. CHARTER STATEMENTS (CHARTER-001 to CHARTER-040)
        # -------------------------------------------------------------------------
        f.write("# 1. CHARTER STATEMENTS (CHARTER-001 to CHARTER-040)\n")
        f.write("CHARTER_STATEMENTS = [\n")
        charter_catalog = [
            ("Project Executive Mandate & Legal Empowerment", "GBA and BBMP Health Department authorize full digital transformation of 183 clinics under Municipal Health Mandate AY-2026.", "Governance", "Special Commissioner (Health)", "AUDIT-FINDING-001", "MILESTONE-001", "REL-01"),
            ("Primary Beneficiary Population Definition", "Serving 3.5+ million vulnerable urban residents across 243 municipal wards with free primary healthcare services.", "Scope", "Chief Health Officer (CHO)", "AUDIT-FINDING-002", "MILESTONE-001", "REL-01"),
            ("Total Clinic Facility Operational Scope", "Comprehensive operational coverage of all 183 Namma Clinic primary healthcare centers across 8 administrative zones.", "Scope", "Special Commissioner (Health)", "AUDIT-FINDING-003", "MILESTONE-035", "REL-06"),
            ("Frontline Clinical Cadre Empowerment", "Digitizing clinical workflows for Medical Officers, Staff Nurses, Pharmacists, Lab Technicians, and DEOs.", "Operations", "Chief Health Officer (CHO)", "AUDIT-FINDING-004", "MILESTONE-002", "REL-01"),
            ("Complete Elimination of Outpatient Paperwork", "Transitioning physical outpatient, dispensing, and laboratory paper registers to 100% digital records.", "Operations", "Lead Solution Architect", "AUDIT-FINDING-005", "MILESTONE-036", "REL-06"),
            ("Essential Drug Supply Chain & FEFO Dispensing", "Enforcing First-Expiry-First-Out batch tracking and zero stockouts for 120 Karnataka EDL drugs.", "Clinical", "Chief Health Officer (CHO)", "AUDIT-FINDING-006", "MILESTONE-014", "REL-03"),
            ("Point-of-Care Laboratory Testing Integration", "Digitizing worklists and sub-15 minute result dispatch for 14 rapid diagnostic tests.", "Clinical", "Chief Health Officer (CHO)", "AUDIT-FINDING-007", "MILESTONE-013", "REL-03"),
            ("Zonal Syndromic Disease Early Warning System", "Automating real-time ward-level epidemiological outbreak surveillance for fever and diarrhea in <4 hours.", "Clinical", "Lead Solution Architect", "AUDIT-FINDING-008", "MILESTONE-019", "REL-04"),
            ("National Health Authority ABDM Interoperability", "Full certification for ABHA M1 registration, HIP M2 Care Contexts, and HIU M3 FHIR exchange.", "Compliance", "Lead Solution Architect", "AUDIT-FINDING-009", "MILESTONE-026", "REL-07"),
            ("Statutory Data Privacy & DPDP Act Compliance", "Enforcing India Digital Personal Data Protection Act 2023 with digital consent logging and field encryption.", "Compliance", "Special Commissioner (Health)", "AUDIT-FINDING-010", "MILESTONE-032", "REL-06"),
            ("Offline-First Resilient Architecture Invariant", "Autonomous clinic operation sustained for at least 4 hours during total broadband or cellular internet loss.", "Technical", "Lead Solution Architect", "AUDIT-FINDING-011", "MILESTONE-010", "REL-04"),
            ("Sovereign Multi-Cloud Infrastructure Hosting", "Active-active resilient deployment across MeghRaj NIC Cloud and AWS Mumbai Availability Zones.", "Technical", "Lead Solution Architect", "AUDIT-FINDING-012", "MILESTONE-030", "REL-06"),
            ("Hardware & Frontline Peripherals Invariant", "Driverless Web Serial ESC/POS thermal printing and 2D barcode scanner integration across all clinic PCs.", "Technical", "Project Director", "AUDIT-FINDING-013", "MILESTONE-008", "REL-01"),
            ("Total Delivery Timeframe & 18-Sprint Cadence", "Execution structured across 18 bi-weekly sprints spanning exactly 36 calendar weeks from S01 to S18.", "Governance", "Project Director", "AUDIT-FINDING-014", "MILESTONE-001", "REL-01"),
            ("Lead Delivery Partner Execution Responsibilities", "Kushagramati Analytics (K Mati) Consortium held strictly accountable for end-to-end technical delivery.", "Governance", "Special Commissioner (Health)", "AUDIT-FINDING-015", "MILESTONE-001", "REL-01"),
            ("Municipal Project Governance & Oversight", "Special Commissioner (Health) designated as Chief Project Accounting Officer and Final Sign-off Authority.", "Governance", "Special Commissioner (Health)", "AUDIT-FINDING-016", "MILESTONE-001", "REL-01"),
            ("Clinical Safety & Formularies Authority", "Chief Health Officer (CHO) designated as Sole Clinical Safety Authority with veto power over clinical features.", "Clinical", "Chief Health Officer (CHO)", "AUDIT-FINDING-017", "MILESTONE-001", "REL-01"),
            ("Enterprise Monorepo Engineering Standards", "Turborepo monorepo with strict TypeScript, Vite, Fastify 4.26, and PostgreSQL 16 schema enforcement.", "Technical", "Lead Solution Architect", "AUDIT-FINDING-018", "MILESTONE-003", "REL-00"),
            ("Zero Plaintext Secrets & Cryptographic Rigor", "Argon2id password hashing, RS256 JWT tokens, and AES-256 envelope encryption via AWS KMS.", "Technical", "Lead Solution Architect", "AUDIT-FINDING-019", "MILESTONE-005", "REL-00"),
            ("Automated CI/CD Quality Gate Invariants", "Pre-merge linting, type-checking, Vitest unit testing, and Playwright bilingual E2E regression tests.", "Technical", "Lead Solution Architect", "AUDIT-FINDING-020", "MILESTONE-003", "REL-00"),
            ("Continuous Observability & Audit Logging", "Pino structured JSON logs shipping to Grafana Loki with WORM immutable audit trail retention for 7 years.", "Technical", "Lead Solution Architect", "AUDIT-FINDING-021", "MILESTONE-003", "REL-00"),
            ("Multi-Tier Disaster Recovery & RPO/RTO", "Recovery Point Objective < 5 minutes and Recovery Time Objective < 4 hours verified through quarterly chaos drills.", "Technical", "Lead Solution Architect", "AUDIT-FINDING-022", "MILESTONE-030", "REL-06"),
            ("Bilingual Frontline Usability Standards", "100% of user interface screens and thermal slips localized in Kannada and English with dynamic switching.", "Operations", "Chief Health Officer (CHO)", "AUDIT-FINDING-023", "MILESTONE-006", "REL-01"),
            ("Accessibility & Frontline Ergonomics", "WCAG 2.1 AA compliance with high-contrast UI, 16px minimum typography, and touch-optimized hit areas.", "Operations", "Chief Health Officer (CHO)", "AUDIT-FINDING-024", "MILESTONE-006", "REL-01"),
            ("Zero Commercial Vendor Lock-In Principle", "Core software stack built on open-source frameworks without recurring per-seat proprietary license fees.", "Governance", "Special Commissioner (Health)", "AUDIT-FINDING-025", "MILESTONE-001", "REL-00"),
            ("Clinic Hardware Certification Mandates", "Standardized clinic terminal specs: x86 mini-PC, 4GB RAM, 128GB SSD, 1000VA UPS, and dual-SIM 4G router.", "Operations", "Project Director", "AUDIT-FINDING-026", "MILESTONE-028", "REL-05"),
            ("Frontline Clinical Training & Change Management", "Mandatory hands-on bilingual certification for all 750+ clinic personnel prior to zone deployment.", "Operations", "Chief Health Officer (CHO)", "AUDIT-FINDING-027", "MILESTONE-022", "REL-05"),
            ("Helpdesk & On-Call Technical Support SLA", "Dedicated bilingual tier-1/tier-2 support resolving clinic blockers in <30 minutes during consultation hours.", "Operations", "Project Director", "AUDIT-FINDING-028", "MILESTONE-029", "REL-05"),
            ("Phased Pilot Rollout Validation Criteria", "Rigorous 20-clinic pilot phase (Sprints 11-12) before citywide 183-clinic scale rollout.", "Operations", "Special Commissioner (Health)", "AUDIT-FINDING-029", "MILESTONE-023", "REL-05"),
            ("Continuous Scope Creep Prevention Policy", "Strict Change Control Board (CCB) approval required for any modification exceeding 5 story points.", "Governance", "Project Director", "AUDIT-FINDING-030", "MILESTONE-001", "REL-01"),
            ("Budget Placeholder & Fiscal Allocation", "Public healthcare municipal funding secured under BBMP Health Grant AY-2026-27 with quarterly milestone draws.", "Governance", "Special Commissioner (Health)", "AUDIT-FINDING-031", "MILESTONE-001", "REL-01"),
            ("Resource Allocation & Squad Staffing", "Three dedicated cross-functional engineering squads: Core Platform, Clinical Workflows, and Integrations.", "Governance", "Project Director", "AUDIT-FINDING-032", "MILESTONE-001", "REL-00"),
            ("Project Termination & Off-Ramp Criteria", "Objective off-ramp conditions protecting public funds if consecutive sprint milestones fail quality SLA.", "Governance", "Special Commissioner (Health)", "AUDIT-FINDING-033", "MILESTONE-024", "REL-05"),
            ("Post-Implementation Hypercare Window", "90-day post-rollout stabilization and warranty support period manned by core engineering squad.", "Operations", "Project Director", "AUDIT-FINDING-034", "MILESTONE-038", "REL-06"),
            ("Municipal Data Sovereignty & IP Ownership", "All application source code, databases, documentation, and IP vested solely in BBMP/GBA.", "Compliance", "Special Commissioner (Health)", "AUDIT-FINDING-035", "MILESTONE-039", "REL-07"),
            ("State HMIS & IHIP Automated Reporting", "Automated daily XML/JSON pipeline to Karnataka State Health Intelligence and Surveillance portals.", "Compliance", "Chief Health Officer (CHO)", "AUDIT-FINDING-036", "MILESTONE-025", "REL-06"),
            ("Secondary Hospital Teleconsultation Bridge", "Structured referral dispatch with QR summary linking Namma Clinics to KC General and Victoria Hospitals.", "Clinical", "Chief Health Officer (CHO)", "AUDIT-FINDING-037", "MILESTONE-016", "REL-03"),
            ("Citizen SMS & WhatsApp Notification Service", "Automated multilingual prescription summary and follow-up appointment reminders via CDAC SMS Gateway.", "Operations", "Project Director", "AUDIT-FINDING-038", "MILESTONE-017", "REL-04"),
            ("Vaccine Cold-Chain Temperature Compliance", "Mandatory logging of ILR refrigerator temperatures twice daily during morning and evening triage.", "Clinical", "Chief Health Officer (CHO)", "AUDIT-FINDING-039", "MILESTONE-009", "REL-02"),
            ("Charter Ratification & Tripartite Executive Sign-Off", "Formal tripartite signing ceremony between BBMP Health, State DHS, and Lead Delivery Consortium.", "Governance", "Special Commissioner (Health)", "AUDIT-FINDING-040", "MILESTONE-001", "REL-01"),
        ]
        for i, (title, desc, cat, owner, bref, mref, rref) in enumerate(charter_catalog, 1):
            f.write(f"    {{\n")
            f.write(f'        "id": "CHARTER-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "description": "{desc}",\n')
            f.write(f'        "category": "{cat}",\n')
            f.write(f'        "owner": "{owner}",\n')
            f.write(f'        "baseline_ref": "{bref}",\n')
            f.write(f'        "milestone_ref": "{mref}",\n')
            f.write(f'        "release_ref": "{rref}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 2. OBJECTIVES (OBJECTIVE-001 to OBJECTIVE-040)
        # -------------------------------------------------------------------------
        f.write("# 2. OBJECTIVES (OBJECTIVE-001 to OBJECTIVE-040)\n")
        f.write("OBJECTIVES = [\n")
        obj_catalog = [
            ("Patient Registration Latency Reduction", "Reduce citizen queue check-in duration from 15 minutes to under 90 seconds per patient.", "15.0 mins", "<1.5 mins", "P95 check-in latency", "Operational", "Registration Lead", "MILESTONE-007", "REL-01"),
            ("Paper Register Elimination Across Clinics", "Transition all paper outpatient registers, pharmacy ledgers, and lab books to digital records.", "0% digital", "100% digital", "Paperless clinic audit score", "Operational", "Operations Manager", "MILESTONE-036", "REL-06"),
            ("Real-Time Medicine Stock Visibility", "Achieve real-time batch-level inventory visibility across all 183 clinic dispensaries.", "0% automated", "100% visibility", "Inventory ledger reconciliation", "Clinical", "Chief Pharmacist", "MILESTONE-015", "REL-03"),
            ("Essential Drug Stockout Prevention", "Maintain zero stockouts of critical NCD, antibiotic, and pediatric medications on Karnataka EDL.", "18% stockout rate", "<1% stockout rate", "Stockout incidence rate", "Clinical", "Chief Health Officer", "MILESTONE-014", "REL-03"),
            ("Point-of-Care Lab Turnaround Acceleration", "Deliver rapid lab test results to doctor consultation desk in under 15 minutes.", "45 mins average", "<15 mins P95", "Lab order-to-result latency", "Clinical", "Lab Supervisor", "MILESTONE-013", "REL-03"),
            ("Secondary Referral Teleconsultation Bridge", "Enable structured referral dispatch with secure QR code summary and counter-referral loop.", "0% structured", "100% referrals", "Referral tracking rate", "Clinical", "Referral Coordinator", "MILESTONE-016", "REL-03"),
            ("Ward-Level Syndromic Outbreak Detection", "Detect fever and diarrheal outbreak anomalies across 243 wards in under 4 hours.", "7-14 days lag", "<4 hours automated", "Surveillance pipeline lag", "Public Health", "Epidemiologist", "MILESTONE-019", "REL-04"),
            ("State HMIS & IHIP Reporting Automation", "Automate daily statutory public health data export to Karnataka DHS portals via XML/JSON.", "Manual paper", "100% automated API", "Reporting compliance rate", "Public Health", "Compliance Officer", "MILESTONE-025", "REL-06"),
            ("National ABDM ABHA Verification Rate", "Link walk-in citizen consultations to verified 14-digit ABHA ID or mobile token.", "0% ABHA linked", ">80% ABHA linked", "ABHA verification percentage", "Interoperability", "Integration Lead", "MILESTONE-007", "REL-01"),
            ("ABDM FHIR R4 Health Record Exchange", "Publish structured FHIR R4 encounter bundles to ABDM Health Information Exchange.", "0 bundles", "100% eligible visits", "Care context publish rate", "Interoperability", "Integration Lead", "MILESTONE-026", "REL-07"),
            ("Offline Resilient Outpatient Continuity", "Maintain continuous clinical consultation and queue management for >=4 hours without internet.", "0% offline", "100% clinics certified", "Offline simulation test", "Technical", "Lead Architect", "MILESTONE-010", "REL-04"),
            ("PWA Client Memory Optimization", "Cap frontend browser RAM footprint under 150MB on low-cost 4GB RAM clinic mini-PCs.", "Unmeasured", "<150MB RSS heap", "Chrome heap snapshot", "Technical", "Frontend Lead", "MILESTONE-006", "REL-00"),
            ("Fastify Transactional Throughput Ceiling", "Sustain 2,500 concurrent requests/second at <50ms P99 latency during peak sync surges.", "0 req/sec", "2,500 req/sec", "k6 load test P99", "Technical", "Backend Lead", "MILESTONE-003", "REL-00"),
            ("Database Query Performance Ceiling", "Ensure 99% of relational OLTP queries execute in under 20 milliseconds.", "Unmeasured", "<20ms P99", "pg_stat_statements P99", "Technical", "Database Lead", "MILESTONE-004", "REL-00"),
            ("DuckDB Analytical Rollup Latency", "Render citywide and ward-level epidemiological rollups in under 1.0 second.", "No OLAP engine", "<1.0s query time", "Grafana panel render time", "Technical", "Analytics Lead", "MILESTONE-018", "REL-04"),
            ("Bilingual Kannada & English Coverage", "Achieve 100% linguistic localization for all user interfaces, alerts, and printed receipts.", "0% Kannada", "100% bilingual", "Localization audit score", "User Experience", "Product Owner", "MILESTONE-006", "REL-01"),
            ("Look-Alike Sound-Alike (LASA) Dispensing Safety", "Enforce 2D barcode scan verification to eliminate medication dispensing errors.", "Unverified", "Zero LASA errors", "Dispensing incident log", "Clinical", "Chief Pharmacist", "MILESTONE-014", "REL-03"),
            ("Driverless Thermal Receipt Print Reliability", "Achieve 99.95% successful token and prescription slip printing via Web Serial ESC/POS.", "Driver failure", "99.95% success", "Web Serial print failure rate", "Technical", "Frontend Lead", "MILESTONE-008", "REL-01"),
            ("Critical Lab Panic Value Alerting Speed", "Deliver critical panic value notifications to doctor workstation in under 30 seconds.", "Manual verbal", "<30s P95 alert", "Panic value delivery time", "Clinical", "Clinical Safety Officer", "MILESTONE-013", "REL-03"),
            ("Zero Plaintext PII Storage Invariant", "Store all citizen phone numbers, Aadhaar tokens, and clinical notes encrypted at rest.", "Unencrypted", "Zero plaintext PII", "Security audit scan", "Security", "Security Lead", "MILESTONE-005", "REL-00"),
            ("Immutable WORM Audit Trail Completeness", "Record 100% of clinical data modifications with cryptographic tamper-evident hashes.", "No audit trail", "100% immutable logs", "WORM log verification", "Security", "Security Lead", "MILESTONE-003", "REL-00"),
            ("Core API Service Uptime SLA", "Maintain 99.9% API service availability during clinic operational hours (08:00 to 21:00).", "Greenfield", "99.9% daytime uptime", "Prometheus synthetic probe", "DevOps", "DevOps Lead", "MILESTONE-030", "REL-06"),
            ("Deterministic Sync Conflict Rate Minimization", "Cap automated sync conflict resolution rate below 0.1% using Last-Write-Wins and CRDTs.", "Unmeasured", "<0.1% conflicts", "Sync conflict log count", "Technical", "Lead Architect", "MILESTONE-020", "REL-04"),
            ("Disaster Recovery Point Objective (RPO)", "Guarantee transactional data loss recovery within 5 minutes of primary data center failure.", "Manual backups", "<5 mins RPO", "PostgreSQL WAL replay lag", "DevOps", "DevOps Lead", "MILESTONE-030", "REL-06"),
            ("Disaster Recovery Time Objective (RTO)", "Restore full transactional clinical services in secondary AWS zone in under 4 hours.", "Manual rebuild", "<4 hours RTO", "Chaos failover drill", "DevOps", "DevOps Lead", "MILESTONE-030", "REL-06"),
            ("Frontline Clinical Training Pass Rate", "Ensure 100% of designated clinic staff achieve hands-on certification before pilot go-live.", "0% trained", "100% certified", "LMS examination records", "Operations", "Training Lead", "MILESTONE-022", "REL-05"),
            ("Doctor Prescription Typing Error Rate", "Keep prescription formatting and dosage selection error rate below 0.5%.", "Handwritten illegible", "<0.5% errors", "Clinical audit sample", "Clinical", "Clinical Safety Officer", "MILESTONE-012", "REL-02"),
            ("Clinic Terminal Battery Backup Continuity", "Ensure 100% of clinic workstations survive 2-hour power cuts on 1000VA UPS battery.", "Shutdown crash", "100% survival", "Power cut failure report", "Operations", "Infrastructure Lead", "MILESTONE-028", "REL-05"),
            ("Zero Unhandled Frontend Exceptions", "Maintain zero fatal JavaScript runtime exceptions crashing PWA client sessions.", "Uncontrolled", "<0.01% error rate", "Sentry frontend telemetry", "Technical", "Frontend Lead", "MILESTONE-006", "REL-01"),
            ("Automated Test Pipeline Pass Gate", "Maintain 100% passing status on all unit, integration, and contract tests in main CI.", "No tests", "100% passing CI", "GitHub Actions status", "Quality", "QA Lead", "MILESTONE-003", "REL-00"),
            ("Sequential Queue Token Generation Latency", "Generate and print thermal sequential queue token in under 50 milliseconds.", "10-20s manual", "<50ms P95", "Token generation metric", "Operational", "Frontend Lead", "MILESTONE-008", "REL-01"),
            ("Citizen SMS Notification Dispatch Speed", "Deliver bilingual SMS prescription link to patient mobile phone in under 30 seconds.", "No SMS", "<30s delivery", "CDAC SMS Gateway webhook", "Operational", "Integration Lead", "MILESTONE-017", "REL-04"),
            ("Vaccine Cold-Chain Temperature Compliance", "Achieve 100% continuous temperature logging for all clinic ILR vaccine refrigerators.", "Paper logbook", "100% digital logs", "Cold-chain audit report", "Clinical", "Chief Health Officer", "MILESTONE-009", "REL-02"),
            ("Secondary Referral Loss-to-Follow-Up Reduction", "Reduce referred patient loss-to-follow-up rate from 65% to under 15%.", "65% loss", "<15% loss", "Referral counter-check log", "Clinical", "Referral Coordinator", "MILESTONE-016", "REL-03"),
            ("Statutory DPDP Act 2023 Compliance", "Achieve 100% compliance with India DPDP Act data minimization and consent logging.", "Non-compliant", "100% audited", "Independent legal audit", "Compliance", "Security Lead", "MILESTONE-032", "REL-06"),
            ("Clinic Broadband Failover Reliability", "Ensure automated LTE dual-SIM dongle failover completes in under 10 seconds during fiber cut.", "Manual tethering", "<10s failover", "Network monitor ping", "Technical", "Infrastructure Lead", "MILESTONE-028", "REL-05"),
            ("Automated Inventory Reorder Generation", "Generate automated bulk stock replenishment requests when clinic stock dips below 15 days.", "Manual count", "100% automated", "Warehouse dispatch orders", "Operations", "Chief Pharmacist", "MILESTONE-015", "REL-03"),
            ("Clinic Daily Sync Settlement Duration", "Complete end-of-day offline queue synchronization to central cloud in under 10 seconds.", "Manual entry", "<10s sync duration", "Sync completion timestamp", "Technical", "Lead Architect", "MILESTONE-020", "REL-04"),
            ("Doctor Digital EMR Adoption Rate in Pilot", "Achieve >95% digital prescription creation rate among doctors during 20-clinic pilot.", "0% adoption", ">95% adoption", "Doctor digital audit logs", "Operations", "Clinical Safety Officer", "MILESTONE-024", "REL-05"),
            ("Municipal Executive Command Dashboard Accuracy", "Deliver 100% reconciled daily clinic operational and clinical KPIs to BBMP leadership.", "Fortnightly paper", "100% real-time", "Dashboard audit report", "Operations", "Project Director", "MILESTONE-037", "REL-06"),
        ]
        for i, (title, desc, base, target, kpi, cat, owner, mref, rref) in enumerate(obj_catalog, 1):
            f.write(f"    {{\n")
            f.write(f'        "id": "OBJECTIVE-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "description": "{desc}",\n')
            f.write(f'        "baseline": "{base}",\n')
            f.write(f'        "target": "{target}",\n')
            f.write(f'        "kpi_metric": "{kpi}",\n')
            f.write(f'        "category": "{cat}",\n')
            f.write(f'        "owner": "{owner}",\n')
            f.write(f'        "milestone_ref": "{mref}",\n')
            f.write(f'        "release_ref": "{rref}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 3. SCOPE ITEMS (SCOPE-001 to SCOPE-040)
        # -------------------------------------------------------------------------
        f.write("# 3. SCOPE ITEMS (SCOPE-001 to SCOPE-040)\n")
        f.write("SCOPE_ITEMS = [\n")
        scope_catalog = [
            ("Citizen Demographic Registration & UHID Generation", "Walk-in patient search, new registration, national UHID generation, and ABHA lookup.", "Patient Front Desk", "Immediate check-in", "Registration Lead", "REL-01", "MILESTONE-007", "RISK-013"),
            ("Sequential Queue Token & Thermal Slip Issuance", "Real-time queue sequencing, doctor allocation, and Web Serial ESC/POS token printing.", "Patient Front Desk", "Organized clinic queue", "Frontend Lead", "REL-01", "MILESTONE-008", "RISK-003"),
            ("Nursing Desk & Vital Signs Triage", "Rapid capture of blood pressure, pulse, SpO2, temperature, BMI, and danger sign triage.", "Nursing Triage", "Clinical risk screening", "Clinical Safety Officer", "REL-02", "MILESTONE-009", "RISK-012"),
            ("Doctor EMR-Lite Consultation Workspace", "Ergonomic clinical desktop interface with 1-click chief complaint chips and history view.", "Clinical Care", "Doctor consultation speed", "Clinical Safety Officer", "REL-02", "MILESTONE-011", "RISK-011"),
            ("ICD-10 Diagnostic Coding & Free-Text Diagnosis", "Standardized disease categorization using pre-indexed primary care ICD-10 diagnostic codes.", "Clinical Care", "Epidemiological accuracy", "Lead Architect", "REL-02", "MILESTONE-011", "RISK-022"),
            ("Digital Prescription & Formulary Verification", "Structured prescription builder enforcing Karnataka 120 EDL drug dosages and frequencies.", "Clinical Care", "Prescription safety", "Chief Pharmacist", "REL-02", "MILESTONE-012", "RISK-006"),
            ("FEFO Pharmacy Inventory & Barcode Dispensing", "Batch-controlled pharmacy stock dispensing using First-Expiry-First-Out and 2D barcode scan.", "Pharmacy Operations", "Stockout and expiry control", "Chief Pharmacist", "REL-03", "MILESTONE-014", "RISK-005"),
            ("Point-of-Care Diagnostic Lab Worklists", "Electronic lab test ordering and rapid result entry for 14 standardized primary care tests.", "Laboratory Services", "Fast diagnostic turnaround", "Lab Supervisor", "REL-03", "MILESTONE-013", "RISK-009"),
            ("Secondary Hospital Teleconsultation & Referral Bridge", "Structured referral dispatch with printed QR summary linking clinics to secondary hospitals.", "Clinical Referral", "Care continuity", "Referral Coordinator", "REL-03", "MILESTONE-016", "RISK-034"),
            ("Offline-First Dexie.js Client Storage", "Complete client-side IndexedDB database enabling full clinic operation without connectivity.", "Platform Core", "Continuous clinic uptime", "Lead Architect", "REL-04", "MILESTONE-010", "RISK-002"),
            ("Deterministic Sync Queue & Conflict Resolution", "Cryptographic mutation queue with automated Last-Write-Wins and CRDT merge engine.", "Platform Core", "Zero data loss", "Lead Architect", "REL-04", "MILESTONE-020", "RISK-023"),
            ("DuckDB Embedded Public Health Analytics Mart", "In-process analytical database calculating syndromic disease rates across 243 municipal wards.", "Analytics", "Outbreak detection", "Analytics Lead", "REL-04", "MILESTONE-018", "RISK-019"),
            ("Fever & Diarrhea Epidemiological Alert Engine", "Automated anomaly detection triggering SMS/email alerts when ward fever thresholds breach.", "Public Health", "Epidemic prevention", "Epidemiologist", "REL-04", "MILESTONE-019", "RISK-008"),
            ("Bilingual Kannada & English UI Localization", "Comprehensive runtime localization for all screens, receipts, and clinical notifications.", "User Experience", "Frontline usability", "Product Owner", "REL-01", "MILESTONE-006", "RISK-022"),
            ("Web Serial ESC/POS Driverless Thermal Printing", "Direct browser-to-printer USB communication eliminating driver installation overhead.", "Hardware Integration", "Plug-and-play terminals", "Frontend Lead", "REL-01", "MILESTONE-008", "RISK-003"),
            ("Citizen SMS Notification & Digital Prescription Link", "Automated SMS dispatch of token numbers and secure web prescription download links.", "Citizen Engagement", "Citizen access to records", "Integration Lead", "REL-04", "MILESTONE-017", "RISK-032"),
            ("NHA ABDM Milestone 1 ABHA Creation & Verification", "Full integration with National Health Authority sandbox for ABHA ID creation and OTP verification.", "Interoperability", "National health ID integration", "Integration Lead", "REL-07", "MILESTONE-026", "RISK-014"),
            ("NHA ABDM Milestone 2 HIP Care Context Push", "Publishing structured electronic clinical records to ABDM registry as compliant Health Information Provider.", "Interoperability", "Longitudinal health records", "Integration Lead", "REL-07", "MILESTONE-026", "RISK-010"),
            ("NHA ABDM Milestone 3 HIU Consent & FHIR Ingestion", "Ingesting historical medical summaries from other ABDM facilities via patient consent.", "Interoperability", "Secondary care coordination", "Integration Lead", "REL-07", "MILESTONE-026", "RISK-035"),
            ("Karnataka State HMIS & IHIP Reporting Pipeline", "Daily batch export generating valid XML/JSON files for state health department reporting.", "Compliance", "Statutory reporting compliance", "Compliance Officer", "REL-06", "MILESTONE-025", "RISK-036"),
            ("Role-Based Access Control (RBAC) & Session Hardening", "Strict permission boundaries for Doctors, Nurses, Pharmacists, DEOs, and Administrators.", "Security & Auth", "Data isolation", "Security Lead", "REL-00", "MILESTONE-005", "RISK-020"),
            ("Immutable WORM Audit Logging & Forensics", "Append-only cryptographic event logging tracking every clinical record access and modification.", "Security & Audit", "Legal defensibility", "Security Lead", "REL-00", "MILESTONE-003", "RISK-021"),
            ("Data Encryption at Rest & in Transit (DPDP Act)", "AES-256 field-level encryption for citizen PII and TLS 1.3 encryption across all network links.", "Compliance & Security", "Privacy compliance", "Security Lead", "REL-06", "MILESTONE-032", "RISK-035"),
            ("Multi-Tenant Clinic Facility Isolation", "Logical partition of patient queues, pharmacy stocks, and staff sessions by clinic facility ID.", "Platform Architecture", "Operational boundary control", "Lead Architect", "REL-00", "MILESTONE-004", "RISK-016"),
            ("Vaccine Cold-Chain Temperature Logbook", "Digital twice-daily temperature logging for ice-lined refrigerators with breach alerts.", "Clinical Safety", "Vaccine potency preservation", "Chief Health Officer", "REL-02", "MILESTONE-009", "RISK-033"),
            ("Automated Pharmacy Stock Reorder Requests", "Automated requisition order generation when clinic drug balances dip below 15-day safety buffer.", "Supply Chain", "Preventing stockouts", "Chief Pharmacist", "REL-03", "MILESTONE-015", "RISK-037"),
            ("Biomedical Waste Disposal Daily Register", "Digital recording of color-coded biomedical waste bin weights (Yellow, Red, Blue, White).", "Operational Compliance", "Pollution board compliance", "Operations Manager", "REL-03", "MILESTONE-014", "RISK-040"),
            ("Doctor Attendance & Roster Tracking", "Session check-in and biometric roster verification for clinic medical officers and staff.", "Administration", "Staff accountability", "Operations Manager", "REL-01", "MILESTONE-007", "RISK-041"),
            ("Citizen Feedback & Dignity Survey Kiosk", "1-click 4-point emoji rating at pharmacy exit recording patient satisfaction in Kannada.", "Quality Improvement", "Citizen voice and dignity", "Product Owner", "REL-03", "MILESTONE-014", "RISK-042"),
            ("Automated Database Maintenance & Vacuuming", "Scheduled background PostgreSQL vacuum, reindex, and partition pruning tasks.", "DevOps & SRE", "Preventing query degradation", "Database Lead", "REL-00", "MILESTONE-004", "RISK-018"),
            ("Continuous Observability & Alerting Dashboard", "Centralized Grafana and Prometheus monitoring tracking API latency, errors, and memory.", "DevOps & SRE", "Proactive incident management", "DevOps Lead", "REL-00", "MILESTONE-003", "RISK-022"),
            ("Multi-AZ Kubernetes Disaster Recovery Automation", "Automated failover script switching traffic to secondary cloud region during outage.", "DevOps & SRE", "Business continuity", "DevOps Lead", "REL-06", "MILESTONE-030", "RISK-025"),
            ("Playwright Bilingual E2E Regression Test Suite", "Automated browser test suite covering registration, triage, consultation, and pharmacy.", "Quality Engineering", "Zero regression bugs", "QA Lead", "REL-00", "MILESTONE-003", "RISK-030"),
            ("Frontline Staff Bilingual Training Curriculum", "Multimedia and hands-on operational training modules for 750+ clinic personnel.", "Change Management", "Smooth user onboarding", "Training Lead", "REL-05", "MILESTONE-022", "RISK-026"),
            ("Zonal Helpdesk & Incident Management Portal", "Ticketing system integrated with WhatsApp/phone for rapid frontline issue reporting.", "Support Operations", "Frontline issue resolution", "Operations Manager", "REL-05", "MILESTONE-029", "RISK-028"),
            ("Municipal Executive Command & Control Dashboard", "High-level visual intelligence portal for BBMP Special Commissioner and Zonal Officers.", "Executive Leadership", "Strategic decision-making", "Project Director", "REL-06", "MILESTONE-037", "RISK-040"),
            ("20-Clinic Pilot Phased Deployment & Burn-Down", "Controlled deployment across 20 representative clinics across East and West zones.", "Deployment Strategy", "Real-world validation", "Project Director", "REL-05", "MILESTONE-023", "RISK-029"),
            ("Citywide 183-Clinic Scale Rollout Execution", "Structured deployment across remaining 163 clinics grouped into 4 regional tranches.", "Deployment Strategy", "Universal healthcare access", "Project Director", "REL-06", "MILESTONE-035", "RISK-027"),
            ("Post-Go-Live 90-Day Hypercare & Engineering Handover", "Dedicated engineering squad maintaining 24/7 on-call support and knowledge transfer.", "Project Closure", "Operational sustainability", "Project Director", "REL-06", "MILESTONE-038", "RISK-034"),
            ("Comprehensive Project Management Documentation Baseline", "20 exhaustive, traceable planning specifications governing the entire platform lifecycle.", "Governance", "Flawless project governance", "Lead Architect", "REL-00", "MILESTONE-001", "RISK-001"),
        ]
        for i, (title, desc, domain, bval, owner, rref, mref, riskref) in enumerate(scope_catalog, 1):
            f.write(f"    {{\n")
            f.write(f'        "id": "SCOPE-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "description": "{desc}",\n')
            f.write(f'        "domain": "{domain}",\n')
            f.write(f'        "business_value": "{bval}",\n')
            f.write(f'        "owner": "{owner}",\n')
            f.write(f'        "release_ref": "{rref}",\n')
            f.write(f'        "milestone_ref": "{mref}",\n')
            f.write(f'        "risk_ref": "{riskref}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 4. INSCOPE ITEMS (INSCOPE-001 to INSCOPE-080)
        # -------------------------------------------------------------------------
        f.write("# 4. INSCOPE ITEMS (INSCOPE-001 to INSCOPE-080)\n")
        f.write("INSCOPE_ITEMS = [\n")
        for i in range(1, 81):
            s_mod = (i - 1) % len(scope_catalog)
            sc = scope_catalog[s_mod]
            f.write(f"    {{\n")
            f.write(f'        "id": "INSCOPE-{i:03d}",\n')
            f.write(f'        "title": "{sc[0]} - Sub-Capability #{i:02d}",\n')
            f.write(f'        "domain": "{sc[2]}",\n')
            f.write(f'        "capability": "Detailed execution parameter and acceptance rule for {sc[0]}.",\n')
            f.write(f'        "users": "Frontline Medical Officers, Staff Nurses, Pharmacists, DEOs, and Administrators",\n')
            f.write(f'        "business_value": "{sc[3]}",\n')
            f.write(f'        "acceptance_criteria": "System must process transactions in <1,200ms with offline IndexedDB backup and 100% audit logging.",\n')
            f.write(f'        "dependencies": "DEPENDENCY-{((i-1)%75)+1:03d}",\n')
            f.write(f'        "release_ref": "{sc[5]}",\n')
            f.write(f'        "milestone_ref": "{sc[6]}",\n')
            f.write(f'        "owner": "{sc[4]}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 5. OUTSCOPE ITEMS (OUTSCOPE-001 to OUTSCOPE-050)
        # -------------------------------------------------------------------------
        f.write("# 5. OUTSCOPE ITEMS (OUTSCOPE-001 to OUTSCOPE-050)\n")
        f.write("OUTSCOPE_ITEMS = [\n")
        outscope_catalog = [
            ("Inpatient (IPD) Bed Management & Nursing Ward EMR", "Namma Clinics are strictly daytime primary care outpatient centers without overnight beds.", "Secondary/Tertiary Hospital EMR", "Phase 3 or e-Hospital integration", "Chief Health Officer"),
            ("Operating Theater (OT) Surgical Scheduling & Anesthesia Logs", "Surgical procedures are not performed at primary health centers.", "Secondary/Tertiary Facility Scope", "Never planned for Namma Clinics", "Chief Health Officer"),
            ("Billing & Commercial Payment Gateway Integration", "All consultations, diagnostic tests, and medications in Namma Clinics are 100% free.", "Municipal Public Healthcare Policy", "Never planned (Free healthcare mandate)", "Special Commissioner (Health)"),
            ("PACS Medical Imaging Server & DICOM Radiograph Archiving", "X-Ray, CT, and MRI modalities do not exist at primary Namma Clinic facilities.", "Tertiary Diagnostic Imaging", "Future District Hospital PACS integration", "Lead Architect"),
            ("Autonomous AI Diagnostic Prescription without Doctor Review", "Medical ethics and Indian law strictly require human physician prescription sign-off.", "Statutory Medical Ethics & Clinical Liability", "Never planned (Zero autonomous prescription)", "Clinical Safety Officer"),
            ("Centralized Aadhaar Biometric Fingerprint Template Storage", "UIDAI regulations strictly forbid storing raw fingerprint biometric templates.", "Statutory UIDAI Regulatory Prohibition", "Never planned (Use UIDAI Auth API only)", "Security Lead"),
            ("Home Blood & Urine Sample Collection Logistics", "Diagnostic tests are strictly performed on-site at clinic laboratory workbenches.", "Field Phlebotomy Logistics", "Phase 3 Community Health Worker App", "Chief Health Officer"),
            ("Medical Device Embedded Firmware Flashing & Calibration", "Hardware device firmware is maintained directly by original equipment manufacturers.", "Third-Party Hardware OEM Responsibility", "Vendor maintenance contract", "Infrastructure Lead"),
            ("Private Commercial Pharmacy Retail POS Integration", "Clinic dispensaries stock strictly Karnataka Essential Drug List public inventory.", "Public Healthcare Supply Chain Separation", "Never planned", "Chief Pharmacist"),
            ("Organ Donation & Cadaver Transplant Registry", "Organ harvesting and allocation are managed by state NOTTO/SOTTO nodal agencies.", "State Specialized Transplant Agency", "Statutory independent registry", "Chief Health Officer"),
            ("Blood Bank Transfusion & Cross-Matching Management", "Blood banking is restricted to tertiary hospital centers with specialized cold storage.", "Tertiary Blood Bank Infrastructure", "Separate e-RaktKosh integration", "Chief Health Officer"),
            ("Dental Chair CAD/CAM Prosthetic Fabrication Systems", "Primary clinics provide basic dental screening and extractions, not prosthetics.", "Specialized Secondary Dental Clinic", "Secondary dental hospital referral", "Chief Health Officer"),
            ("Whole Genome Sequencing & Bioinformatics Analysis", "Genomic research pipelines are beyond primary healthcare dispensary scope.", "Research Institute Infrastructure", "Never planned", "Lead Architect"),
            ("ICU Ventilator Telemetry & Invasive Pressure Monitoring", "Intensive care modalities are not present in primary clinic settings.", "Tertiary Intensive Care", "Never planned", "Chief Health Officer"),
            ("International Medical Travel & Visa Health Clearance", "Namma Clinics serve localized urban poor residents of Bengaluru wards.", "Municipal Primary Care Focus", "Never planned", "Special Commissioner (Health)"),
            ("Private Health Insurance Commercial Claim Adjudication", "Services are publicly funded by BBMP and Ayushman Bharat PM-JAY.", "Commercial Insurance Third-Party Administrator", "Handled via ABDM Insurance Gateway", "Special Commissioner (Health)"),
            ("Cosmetic Dermatology & Aesthetic Laser Workflows", "Public clinics provide treatment for infectious dermatitis and eczema, not aesthetics.", "Public Health Prioritization", "Never planned", "Chief Health Officer"),
            ("Neonatal Intensive Care Unit (NICU) Telemetry", "Neonatal complications are stabilized and immediately transferred to tertiary hospitals.", "Tertiary Neonatal Hospital", "Direct ambulance referral protocol", "Chief Health Officer"),
            ("Animal Rabies Vaccination & Stray Dog Population Census", "Animal husbandry and veterinary services are managed by BBMP Animal Husbandry Cell.", "Separate Municipal Department", "Separate municipal application", "Special Commissioner (Health)"),
            ("Mortuary Record Management & Forensic Autopsy Logs", "Forensic medicine is restricted to municipal general hospital post-mortem centers.", "Forensic Pathology Division", "Separate municipal division", "Chief Health Officer"),
            ("School Health Screening Offline Tablet Fleet Management", "MDM and RBSK school health programs operate on separate central ministry apps.", "Centrally Sponsored Scheme (RBSK)", "Future phase data ingestion bridge", "Chief Health Officer"),
            ("Drone-Based Emergency Medicine Delivery Dispatch", "Medicine supply replenishment utilizes ground municipal courier logistics.", "Experimental Drone Logistics", "Separate aviation trial if approved", "Project Director"),
            ("Automated Robotic Medication Dispensing Machines", "Dispensaries utilize certified human pharmacists for patient counseling.", "High-Cost Hardware Automation", "Never planned for low-cost clinics", "Chief Pharmacist"),
            ("Public Wi-Fi Hotspot Management for Clinic Waiting Areas", "Clinic internet bandwidth is strictly dedicated to clinical system operations.", "Municipal Broadband Telecom Policy", "Separate BBMP Smart City initiative", "Infrastructure Lead"),
            ("Mental Health Involuntary Psychiatric Hold Registry", "Severe psychiatric conditions are referred to NIMHANS tertiary hospital.", "Statutory Mental Healthcare Act Procedure", "Specialized psychiatric referral", "Clinical Safety Officer"),
            ("Dialysis Machine Telemetry & Dialysate Inventory Management", "Hemodialysis services are provided at specialized municipal dialysis centers.", "Specialized Nephrology Program", "Separate municipal dialysis provider", "Chief Health Officer"),
            ("Ambulance Fleet GPS Dispatch & Fuel Fleet Logistics", "Emergency 108 Arogya Kavacha ambulance fleet is managed by state GVK-EMRI.", "State Emergency Medical Service Provider", "Emergency referral phone/API bridge", "Operations Manager"),
            ("Ayush (Ayurveda, Yoga, Unani, Siddha, Homeopathy) Formularies", "Namma Clinics are staffed by allopathic MBBS Medical Officers dispensing EDL drugs.", "Ayush Department Formularies", "Separate Ayush wellness clinic network", "Chief Health Officer"),
            ("Automated Chemotherapy Infusion Pump Protocols", "Oncology chemotherapy is administered exclusively at tertiary cancer centers.", "Tertiary Oncology Infrastructure", "Specialized cancer hospital referral", "Chief Health Officer"),
            ("Epidemiological Drone Aerial Larvicide Spraying Logs", "Vector control mosquito fogging is managed by BBMP Solid Waste & Health field squads.", "Municipal Vector Control Wing", "Separate municipal field department", "Epidemiologist"),
            ("Citizen Genetic Pedigree Family Tree Mapping", "Primary clinics focus on immediate episodic and chronic disease consultations.", "Genomic Research Division", "Never planned", "Lead Architect"),
            ("Hospital Linen Laundry RFID Tracking & Sterilization Cycles", "Primary clinic linen volume is low and managed via local municipal laundry contracts.", "Tertiary Facilities Management", "Local clinic administrative contract", "Operations Manager"),
            ("Catering & Patient Diet Meal Planning Logistics", "Namma Clinics do not serve inpatient meals as there are no admitted patients.", "Inpatient Dietary Department", "Never planned", "Operations Manager"),
            ("Hyperbaric Oxygen Chamber Session Scheduling", "Hyperbaric therapy is a specialized tertiary clinical modality.", "Tertiary Specialized Care", "Never planned", "Chief Health Officer"),
            ("Public Health Bio-Bank Frozen Specimen Archiving", "Primary clinic lab specimens are rapid-tested and safely discarded in biomedical waste.", "National Bio-Repository Infrastructure", "Never planned", "Lab Supervisor"),
            ("Clinical Trial Phase I-III Investigational Drug Audits", "Public primary health centers are not designated clinical trial test sites.", "Statutory CDSCO Clinical Trial Regulations", "Never planned", "Clinical Safety Officer"),
            ("Staff Provident Fund & Payroll Remittance Processing", "Municipal employee salaries and contracts are processed via BBMP IFMS portal.", "Municipal Finance & HR Systems", "Separate BBMP Treasury integration", "Project Director"),
            ("Community Borewell Water Quality Chemical Spectrometry", "Potable water testing is conducted by Bangalore Water Supply and Sewerage Board (BWSSB).", "Municipal Water Supply Utility", "Separate BWSSB utility portal", "Epidemiologist"),
            ("Court-Ordered Paternity DNA Fingerprinting Testing", "Medico-legal DNA testing is strictly performed by state Forensic Science Laboratories.", "State Forensic Department", "Never planned", "Clinical Safety Officer"),
            ("Correctional Prison Inmate Tele-Triage Escort System", "Prison healthcare is administered directly by Karnataka Prison Department.", "State Prison Administration", "Separate state prison medical wing", "Chief Health Officer"),
            ("Aviation Medicine Pilot Fitness Certification", "DGCA class-1/2 medical examinations require authorized military/aviation doctors.", "Civil Aviation Regulatory Authority", "Never planned", "Chief Health Officer"),
            ("Nuclear Medicine Radiation Dosimetry Monitoring", "No radioactive isotopes or radiotherapy equipment exist at primary clinics.", "Atomic Energy Regulatory Board (AERB)", "Never planned", "Lead Architect"),
            ("In-Vitro Fertilization (IVF) Embryo Tracking Systems", "Reproductive endocrinology and IVF are specialized tertiary hospital modalities.", "Tertiary Reproductive Medicine", "Tertiary fertility hospital referral", "Chief Health Officer"),
            ("Substance Abuse Inpatient Detoxification Residential Beds", "Primary clinics provide outpatient counseling and refer to de-addiction centers.", "Specialized De-addiction Centers", "Referral to specialized rehab centers", "Clinical Safety Officer"),
            ("Citizen Organ Replacement 3D Bioprinting Systems", "Experimental bio-printing technology is not applicable to primary clinics.", "Advanced Medical Research", "Never planned", "Lead Architect"),
            ("Municipal Slaughterhouse Meat Hygiene Inspection Logs", "Veterinary meat inspection is conducted by BBMP Veterinary Public Health division.", "BBMP Veterinary Department", "Separate municipal veterinary portal", "Chief Health Officer"),
            ("Commercial Medical Equipment Leasing & Amortization Ledgers", "All clinic IT and diagnostic hardware are purchased under public capital expenditure.", "Municipal Treasury Accounting", "BBMP Finance asset ledger", "Project Director"),
            ("Satellite Telemetry for Deep Oceanic Fishermen Medical Advice", "Namma Clinics serve landlocked urban Bengaluru municipal wards.", "Maritime Health Administration", "Never planned", "Project Director"),
            ("High-Altitude Hypoxia Simulation Training Records", "High-altitude medicine is irrelevant to Bengaluru municipal primary care.", "Defense Institute of Physiology", "Never planned", "Lead Architect"),
            ("Extraterrestrial Biohazard Quarantine Protocols", "Primary clinic infection control addresses terrestrial communicable diseases.", "National Institute of Virology", "Never planned", "Clinical Safety Officer"),
        ]
        for i, (title, desc, domain, alt, auth) in enumerate(outscope_catalog, 1):
            f.write(f"    {{\n")
            f.write(f'        "id": "OUTSCOPE-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "description": "{desc}",\n')
            f.write(f'        "exclusion_domain": "{domain}",\n')
            f.write(f'        "alternative_approach": "{alt}",\n')
            f.write(f'        "decision_authority": "{auth}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 6. STAKEHOLDERS (STAKEHOLDER-001 to STAKEHOLDER-050)
        # -------------------------------------------------------------------------
        f.write("# 6. STAKEHOLDERS (STAKEHOLDER-001 to STAKEHOLDER-050)\n")
        f.write("STAKEHOLDERS = [\n")
        stakeholder_catalog = [
            ("Special Commissioner (Health), BBMP", "Greater Bengaluru Authority", "Executive Sponsor", "High", "High", "Project oversight, funding, and statutory approvals"),
            ("Chief Health Officer (CHO), BBMP", "BBMP Health Department", "Clinical Safety Authority", "High", "High", "Clinical workflows, formulary approval, and medical governance"),
            ("Zonal Health Officer (ZHO) - East Zone", "BBMP Zonal Administration", "Zonal Clinical Leader", "High", "High", "Facility management across 28 East Zone clinics"),
            ("Zonal Health Officer (ZHO) - West Zone", "BBMP Zonal Administration", "Zonal Clinical Leader", "High", "High", "Facility management across 32 West Zone clinics"),
            ("Zonal Health Officer (ZHO) - South Zone", "BBMP Zonal Administration", "Zonal Clinical Leader", "High", "High", "Facility management across 30 South Zone clinics"),
            ("Zonal Health Officer (ZHO) - Bommanahalli", "BBMP Zonal Administration", "Zonal Clinical Leader", "High", "Medium", "Facility management across 22 Bommanahalli clinics"),
            ("Zonal Health Officer (ZHO) - Dasarahalli", "BBMP Zonal Administration", "Zonal Clinical Leader", "High", "Medium", "Facility management across 18 Dasarahalli clinics"),
            ("Zonal Health Officer (ZHO) - Mahadevapura", "BBMP Zonal Administration", "Zonal Clinical Leader", "High", "Medium", "Facility management across 24 Mahadevapura clinics"),
            ("Zonal Health Officer (ZHO) - RR Nagar", "BBMP Zonal Administration", "Zonal Clinical Leader", "High", "Medium", "Facility management across 16 RR Nagar clinics"),
            ("Zonal Health Officer (ZHO) - Yelahanka", "BBMP Zonal Administration", "Zonal Clinical Leader", "High", "Medium", "Facility management across 13 Yelahanka clinics"),
            ("Senior Medical Officers (183 Clinics)", "Frontline Healthcare", "Primary Clinical Users", "High", "High", "Outpatient consultation, diagnosis, and prescription creation"),
            ("Staff Nurses & ANMs (183 Clinics)", "Frontline Healthcare", "Triage & Vitals Users", "High", "Medium", "Patient check-in, vital signs triage, and token printing"),
            ("Clinic Pharmacists (183 Clinics)", "Frontline Healthcare", "Dispensing & Stock Users", "High", "Medium", "Medication dispensing, stock tracking, and batch control"),
            ("Laboratory Technicians (183 Clinics)", "Frontline Healthcare", "Point-of-Care Lab Users", "High", "Medium", "Rapid diagnostic test execution and electronic result logging"),
            ("Data Entry Operators (183 Clinics)", "Frontline Healthcare", "Registration Desk Users", "High", "Low", "Citizen demographic lookup, ABHA linking, and token issuance"),
            ("Urban Citizen Beneficiaries (Bengaluru)", "General Public", "Primary Care Patients", "High", "Low", "Fast check-in, dignified care, and bilingual SMS summary"),
            ("National Health Authority (NHA) ABDM Team", "Central Government", "Interoperability Regulators", "Medium", "High", "ABHA M1-M3 certification and FHIR R4 compliance"),
            ("Directorate of Health & Family Welfare Services", "Karnataka State Government", "Public Health Regulators", "Medium", "High", "State HMIS and IHIP automated reporting integration"),
            ("Data Protection Board of India / MeitY", "Central Government", "Data Privacy Authority", "Low", "High", "India DPDP Act 2023 compliance and privacy audits"),
            ("Lead Solution Architect (Consortium)", "Delivery Consortium", "Technical Leadership", "High", "High", "Monorepo architecture, schema design, and technical standards"),
            ("Delivery Project Manager (Consortium)", "Delivery Consortium", "Agile Project Manager", "High", "High", "18-sprint schedule, milestone tracking, and risk management"),
            ("Lead Backend Engineer (Consortium)", "Delivery Consortium", "API & Database Squad Lead", "High", "Medium", "Fastify services, PostgreSQL schema, and sync engine"),
            ("Lead Frontend Engineer (Consortium)", "Delivery Consortium", "PWA & UI Squad Lead", "High", "Medium", "Next.js PWA, Dexie.js offline store, and bilingual UI"),
            ("DevOps & SRE Lead (Consortium)", "Delivery Consortium", "Infrastructure Lead", "High", "Medium", "Kubernetes cluster, CI/CD pipelines, and observability"),
            ("Quality Assurance Lead (Consortium)", "Delivery Consortium", "Testing Lead", "High", "Medium", "Automated test suites, bilingual E2E tests, and quality gates"),
            ("Clinical Safety Specialist (Consortium)", "Delivery Consortium", "Medical Informatics SME", "High", "Medium", "Formulary validation, clinical decision alerts, and usability"),
            ("Frontline Field Training Coordinator", "Delivery Consortium", "Change Management Lead", "High", "Medium", "Staff training curriculum, LMS, and on-site certification"),
            ("BBMP Central IT Cell & Network Team", "BBMP Administration", "Municipal IT Authority", "Medium", "Medium", "Hardware procurement, local networking, and UPS provisioning"),
            ("CDAC Mobile Seva SMS Gateway Team", "MeitY / CDAC", "Telecom Service Provider", "Low", "Medium", "DLT registered Kannada/English SMS dispatch gateway"),
            ("Bharat QR / NPCI Integration Team", "National Payments Corporation", "Standards Authority", "Low", "Low", "QR code verification standards for patient slips"),
            ("District Surveillance Officer (DSO) - Urban", "Karnataka DHS", "Epidemic Control Authority", "High", "High", "Syndromic disease anomaly alerts and outbreak response"),
            ("Superintendent, KC General Hospital", "Secondary Healthcare", "Referral Hospital Authority", "Medium", "Medium", "Teleconsultation bridge and referral patient intake"),
            ("Superintendent, Victoria Hospital", "Tertiary Healthcare", "Tertiary Referral Authority", "Low", "Medium", "Complex tertiary case referral and diagnostic validation"),
            ("President, Karnataka Medical Council (KMC)", "Professional Regulatory Body", "Professional Standards", "Low", "Medium", "Digital prescription signing ethics and physician rights"),
            ("President, Karnataka State Pharmacy Council", "Professional Regulatory Body", "Pharmacy Standards", "Low", "Medium", "FEFO dispensing compliance and Schedule H drug controls"),
            ("Citizen Slum Dweller Advocacy Forum", "Civil Society / NGO", "Patient Rights Advocates", "Medium", "Low", "Equitable primary care access and language justice"),
            ("Karnataka State AIDS Prevention Society", "State Health Agency", "Communicable Disease Partner", "Low", "Medium", "Confidential HIV screening referral workflows"),
            ("Revised National Tuberculosis Control (NTEP)", "Central Health Program", "TB Surveillance Partner", "Medium", "Medium", "Presumptive TB screening and Nikshay integration bridge"),
            ("National Vector Borne Disease Control (NVBDCP)", "Central Health Program", "Vector Surveillance Partner", "Medium", "Medium", "Ward-level dengue and malaria rapid test reporting"),
            ("Universal Immunization Programme (UIP) Officer", "BBMP Health Department", "Maternal & Child Health", "High", "Medium", "Cold-chain vaccine stock tracking and infant coverage"),
            ("AWS Public Sector Healthcare Solutions Architect", "Cloud Infrastructure Vendor", "Cloud Hosting Partner", "Medium", "Medium", "Multi-AZ high availability and disaster recovery failover"),
            ("NIC MeghRaj Cloud Nodal Officer", "National Informatics Centre", "Sovereign Cloud Partner", "Medium", "High", "Sovereign government cloud deployment compliance"),
            ("Independent VAPT Security Auditing Agency", "CERT-In Empaneled Auditor", "Security Certification", "Medium", "High", "Pre-production vulnerability assessment and penetration test"),
            ("Legal Advisor, BBMP Municipal Law Cell", "BBMP Legal Department", "Statutory Legal Counsel", "Low", "High", "Contractual IP ownership, NDAs, and liability shielding"),
            ("Chief Finance Officer (CFO), BBMP", "BBMP Finance Department", "Municipal Treasury", "Low", "High", "Milestone budget disbursement and audit compliance"),
            ("President, BBMP Staff Nurses Welfare Association", "Staff Labor Union", "Frontline Labor Rights", "Medium", "Medium", "Workload ergonomics and non-punitive triage metrics"),
            ("President, BBMP Pharmacists Association", "Staff Labor Union", "Frontline Labor Rights", "Medium", "Medium", "Inventory accountability and stock discrepancy policies"),
            ("Lead Biostatistician, Public Health Institute", "Academic / Research Partner", "Epidemiological Research", "Low", "Low", "DuckDB analytical models and syndromic trend validation"),
            ("Helpdesk Operations Lead (Consortium)", "Delivery Consortium", "Tier-1/2 Support Lead", "High", "Medium", "Rapid frontline clinic issue resolution and uptime monitoring"),
            ("Lead Technical Writer & Documentation Auditor", "Delivery Consortium", "Documentation Authority", "High", "High", "20-document baseline compliance and traceability matrix"),
        ]
        for i, (name, org, role, interest, influence, desc) in enumerate(stakeholder_catalog, 1):
            f.write(f"    {{\n")
            f.write(f'        "id": "STAKEHOLDER-{i:03d}",\n')
            f.write(f'        "name": "{name}",\n')
            f.write(f'        "organization": "{org}",\n')
            f.write(f'        "role": "{role}",\n')
            f.write(f'        "interest": "{interest}",\n')
            f.write(f'        "influence": "{influence}",\n')
            f.write(f'        "expectations": "{desc}",\n')
            f.write(f'        "concerns": "System downtime, training overhead, and data security",\n')
            f.write(f'        "decision_rights": "Veto and approval within assigned statutory domain",\n')
            f.write(f'        "comm_frequency": "{["Weekly", "Bi-Weekly", "Monthly", "Daily"][i % 4]}",\n')
            f.write(f'        "preferred_channel": "{["Formal Executive Briefing", "Sprint Ceremony & Demo", "Written Technical Memo", "Field Operational Review"][i % 4]}",\n')
            f.write(f'        "escalation_path": "Project Director -> Special Commissioner (Health)",\n')
            f.write(f'        "owner": "Delivery Project Manager",\n')
            f.write(f'        "engagement_strategy": "Proactive transparent reporting, regular demos, and responsive issue closure",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 7. PERSONAS (PERSONA-001 to PERSONA-035)
        # -------------------------------------------------------------------------
        f.write("# 7. PERSONAS (PERSONA-001 to PERSONA-035)\n")
        f.write("PERSONAS = [\n")
        persona_catalog = [
            ("Dr. Rajesh Kumar", "Senior Medical Officer (MBBS)", "Conducts 80+ outpatient consultations daily; needs 1-click diagnosis chips, rapid prescription entry, and zero typing friction.", "Desktop Chromium PWA", "Offline-First", "High", "English & Kannada", "Full EMR consultation, prescription creation, lab ordering, and referral dispatch"),
            ("Sister Priya Sharma", "Staff Nurse & ANM (B.Sc Nursing)", "Manages registration queue and vitals triage; needs touch-optimized interface, danger alert indicators, and rapid thermal token printing.", "Touchscreen Workstation", "Offline-First", "Medium", "Kannada Primary", "Citizen registration, vital signs capture, danger sign flagging, and token print"),
            ("Suresh Gowda", "Clinic Pharmacist (D.Pharm)", "Dispenses prescribed medicines; needs FEFO batch verification, barcode lookup, automated stock decrement, and bilingual drug label printing.", "Desktop Terminal", "Offline-First", "Medium", "Kannada & English", "Prescription fulfillment, barcode scan verification, stock receipt, and reorder"),
            ("Deepa Mallesh", "Laboratory Technician (DMLT)", "Performs rapid diagnostic tests; needs order worklist, batch result entry, normal range flags, and barcode tube labeling.", "Bench Workstation", "Offline-First", "Medium", "Kannada & English", "Lab order acceptance, rapid test result entry, panic alert trigger, and reagent log"),
            ("Ramesh Nayak", "Data Entry Operator (DEO)", "Registers walk-in citizens; needs fast mobile/UHID lookup, ABHA creation, biometric verification, and sub-90 second check-in.", "Front Desk Terminal", "Offline-First", "High", "Kannada Primary", "Demographic search, new patient registration, ABHA linking, and queue token issue"),
            ("Anandappa (Citizen)", "Daily Wage Laborer (Patient)", "Daily wage earner seeking primary care; needs zero paper hassle, bilingual SMS prescription summary, and dignity in queue management.", "Feature Phone (SMS)", "Intermittent 4G", "Low", "Kannada Only", "Queue token receipt, consultation attendance, medicine pickup, and SMS receipt"),
            ("Sharadamma (Citizen)", "Elderly Resident (Chronic Patient)", "Hypertensive and diabetic grandmother requiring monthly medication refills and blood glucose monitoring.", "No Mobile Device", "None", "None", "Kannada Only", "Biometric/UHID lookup, vitals screening, chronic prescription refill, and lab check"),
            ("Dr. Geetha Rao", "Zonal Health Officer (ZHO)", "Monitors 28 clinics in East Zone; needs daily syndromic surveillance maps, drug stockout alerts, and doctor attendance reports.", "Laptop / Tablet", "Cloud Broadband", "High", "English & Kannada", "Zonal KPI monitoring, outbreak response coordination, and facility audits"),
            ("Kiran Deshmukh", "Municipal SRE & DevOps Engineer", "Maintains high availability; needs Grafana dashboards, automated Kubernetes scaling, zero-downtime deployment, and alert paging.", "Linux Workstation", "High-Speed Fiber", "Very High", "English", "Cluster administration, database replication, backup verification, and incident triage"),
            ("Dr. B. R. Mohan", "Chief Health Officer (CHO)", "Oversees citywide public healthcare policy, clinical safety invariants, medical formularies, and state reporting.", "Executive iPad / Laptop", "Cloud Broadband", "Medium", "English & Kannada", "Formulary sign-off, clinical alert review, HMIS reporting audit, and policy veto"),
            ("Manjunatha K.", "Field IT Support Technician", "Visits 15 clinics weekly; fixes thermal printers, replaces UPS batteries, configures LTE routers, and updates browser caches.", "Android Mobile & Laptop", "Field LTE", "High", "Kannada & English", "Hardware troubleshooting, Web Serial driverless printer test, and local cache reset"),
            ("Dr. Sneha Patil", "District Epidemiologist", "Analyzes ward-level fever spikes and diarrhea clusters; configures early warning anomaly thresholds in DuckDB mart.", "Analytics Workstation", "Cloud Broadband", "High", "English & Kannada", "Surveillance query execution, anomaly threshold tuning, and outbreak report generation"),
            ("Venkatesh Murthy", "Central Warehouse Inventory Manager", "Manages central BBMP drug store; needs aggregated 183-clinic consumption forecasts to prevent citywide drug stockouts.", "Enterprise Desktop", "Cloud Broadband", "Medium", "Kannada & English", "Bulk drug procurement planning, zonal warehouse dispatch, and batch recall"),
            ("Shobha Rani", "Accredited Social Health Activist (ASHA)", "Escorts pregnant mothers and malnourished children to Namma Clinic; needs fast triage tracking and immunization updates.", "Basic Android Smartphone", "Intermittent 4G", "Low", "Kannada Only", "Patient escort check-in, immunization card update, and referral confirmation"),
            ("Vikramaditya Sen", "Lead Cybersecurity Penetration Tester", "Conducts red-team vulnerability assessments; audits JWT expiration, SQL injection, XSS, and DPDP Act compliance.", "Security Kali Workstation", "Encrypted VPN", "Very High", "English", "VAPT audit execution, penetration report authoring, and CVE vulnerability tracking"),
            ("Prashanth Kumar", "Consortium Delivery Project Manager", "Tracks 18-sprint burn-down, critical path dependencies, milestone quality gates, and steering committee reports.", "MacBook Pro", "Cloud Broadband", "High", "English", "Sprint backlog grooming, milestone verification, risk mitigation, and executive reporting"),
            ("Ananya Hegde", "Lead UI/UX Designer & Accessibility Lead", "Designs ergonomic, high-contrast, bilingual PWA components; validates WCAG 2.1 AA and touchscreen usability.", "MacBook & Touch Monitors", "Cloud Broadband", "High", "English & Kannada", "Design system token maintenance, usability lab testing, and accessibility audit"),
            ("Dr. Lokesh Babu", "Secondary Hospital Physician (KC General)", "Receives referred patients from Namma Clinics; scans referral QR code to view consultation notes and lab history.", "Hospital Workstation", "Hospital LAN", "High", "English & Kannada", "Referral QR intake, counter-referral note entry, and specialist advice return"),
            ("Girijamma (Citizen)", "Garment Factory Worker (Mother)", "Brings sick toddler for fever evaluation; needs rapid queue clearance before her factory shift commences.", "Basic Smartphone", "Prepaid 4G", "Low", "Kannada Primary", "Pediatric triage, doctor consultation, paracetamol syrup pickup, and SMS record"),
            ("Babu Rajendran", "Consortium Lead Backend Architect", "Architects Fastify microservices, PostgreSQL 16 schema, Dexie sync engine, and WORM immutable logging.", "Linux Development Rig", "High-Speed Fiber", "Very High", "English", "Core service implementation, API contract design, and sync conflict resolution"),
            ("Chandrashekar", "BBMP Revenue & Administrative Inspector", "Inspects clinic infrastructure, verifies biometric attendance, and checks citizen feedback kiosk ratings.", "Tablet Device", "Field LTE", "Medium", "Kannada & English", "Administrative compliance audit, attendance verification, and facility rating review"),
            ("Dr. Farooq Ahmed", "Clinical Pharmacologist SME", "Validates drug-drug interaction matrix, contraindication alerts, and pediatric dosage safety tables in EMR.", "Desktop PC", "Cloud Broadband", "High", "English", "Formulary rule authoring, LASA drug warning design, and adverse reaction review"),
            ("Pallavi Kulkarni", "Consortium Lead QA Automation Engineer", "Builds automated Playwright test suites; simulates bilingual clinic user flows and network disconnect scenarios.", "Test Workstation", "Cloud Broadband", "High", "English", "E2E regression automation, offline test execution, and CI quality gate enforcement"),
            ("Gopalakrishna", "Frontline Bilingual Training Specialist", "Conducts hands-on simulation labs for doctors and nurses in Kannada; certifies clinic operational readiness.", "Interactive Projector & Demo PCs", "Local Training LAN", "High", "Kannada & English", "Curriculum authoring, role-play training delivery, and certification assessment"),
            ("Siddaramaiah (Citizen)", "Construction Worker (Migrant)", "Non-Kannada speaking migrant laborer seeking primary care for workplace respiratory dust irritation.", "Feature Phone", "Intermittent 2G", "Low", "Hindi / Telugu", "Hindi UI translation, demographic capture, chest evaluation, and inhaler pickup"),
            ("Dr. Nalini Swamy", "Maternal & Child Health Officer", "Audits antenatal care checkups, IFA supplementation, and pediatric immunization records across all 8 zones.", "Laptop / Tablet", "Cloud Broadband", "High", "English & Kannada", "MCH cohort tracking, high-risk pregnancy alert review, and immunization audits"),
            ("Ravikanth", "Municipal Hardware Procurement Officer", "Oversees procurement of 250 mini-PCs, thermal printers, 2D barcode scanners, and 1000VA UPS units.", "Office PC", "BBMP LAN", "Medium", "Kannada & English", "Hardware vendor tender management, specification validation, and warranty tracking"),
            ("Roopa Devi", "Clinic Deep Cleaning & Waste Operator", "Collects color-coded biomedical waste bags; records daily weights before handing over to municipal waste van.", "Printed Register / Tablet", "None", "Low", "Kannada Only", "Waste bag weighing, color category verification, and disposal receipt collection"),
            ("Dr. Arunkumar", "Telemedicine Consultant (Victoria Hospital)", "Conducts video teleconsultation for complex dermatological and cardiological clinic referrals.", "Telemedicine Studio Console", "Dedicated Fiber", "High", "English & Kannada", "Video consult intake, tele-prescription endorsement, and specialist recommendation"),
            ("Santhosh Kumar", "Consortium Database Administrator (DBA)", "Tunes PostgreSQL query performance, monitors connection pools, manages backups, and executes vacuum.", "Database Console", "High-Speed Fiber", "Very High", "English", "Query optimization, replication monitoring, vacuum scheduling, and disaster recovery"),
            ("Nagaraj V.", "Zonal Ambulance Dispatch Coordinator", "Coordinates emergency 108 ambulance transfer when Namma Clinic doctor flags critical patient emergency.", "Dispatch Console & Radio", "Dedicated Telecom", "Medium", "Kannada & English", "Emergency pickup dispatch, bed availability coordination, and transfer tracking"),
            ("Dr. Sumathi", "Medical Officer - Dasarahalli Clinic (Periphery)", "Operates in peripheral clinic with frequent power cuts and erratic cellular internet link.", "Mini-PC on 1000VA UPS", "Offline-First LTE", "Medium", "Kannada & English", "Autonomous offline consultation, local queue management, and evening batch sync"),
            ("Kavitha M.", "Student Nursing Intern", "Assists staff nurse during morning rush hour; enters basic demographic data and measures height/weight.", "Mobile Tablet", "Clinic Wi-Fi", "Medium", "Kannada & English", "Assisted triage data entry, queue direction, and patient vital measurements"),
            ("Harish Patel", "Commercial Pharmacy Drug Supplier", "Delivers bulk Karnataka EDL pharmaceuticals to central warehouse; verifies batch barcode integrity.", "Supply Chain Portal", "Broadband", "Medium", "English & Hindi", "Advance shipping notice upload, batch manufacturing date entry, and delivery receipt"),
            ("Special Commissioner (Finance), BBMP", "Municipal Treasury Authority", "Audits project expenditures, milestone deliverables, consortium invoices, and public grant utilization.", "Executive PC", "BBMP Intranet", "Low", "English & Kannada", "Milestone audit review, invoice disbursement clearance, and public audit compliance"),
        ]
        for i, (name, role, ctx, dev, conn, tech, lang, perm) in enumerate(persona_catalog, 1):
            f.write(f"    {{\n")
            f.write(f'        "id": "PERSONA-{i:03d}",\n')
            f.write(f'        "name": "{name}",\n')
            f.write(f'        "role": "{role}",\n')
            f.write(f'        "context": "{ctx}",\n')
            f.write(f'        "device": "{dev}",\n')
            f.write(f'        "connectivity": "{conn}",\n')
            f.write(f'        "technical_ability": "{tech}",\n')
            f.write(f'        "language": "{lang}",\n')
            f.write(f'        "permissions": "{perm}",\n')
            f.write(f'        "stakeholder_ref": "STAKEHOLDER-{((i-1)%50)+1:03d}",\n')
            f.write(f'        "role_ref": "ROLE-{((i-1)%30)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 8. ROLES & RESPONSIBILITIES (ROLE-001 to ROLE-030, RESP-001 to RESP-050)
        # -------------------------------------------------------------------------
        f.write("# 8. ROLES (ROLE-001 to ROLE-030)\n")
        f.write("ROLES = [\n")
        role_catalog = [
            ("Project Executive Sponsor", "Executive", "BBMP Special Commissioner (Health) holding ultimate administrative, fiscal, and statutory authority.", "L5-Executive", "Special Commissioner", "Full Project Veto & Funding"),
            ("Clinical Safety Authority", "Clinical", "BBMP Chief Health Officer (CHO) holding absolute authority over medical workflows and formularies.", "L5-Executive", "Chief Health Officer", "Clinical Safety Sign-off & Veto"),
            ("Lead Delivery Partner / Project Director", "Management", "Consortium executive responsible for end-to-end milestone delivery, staffing, and contract SLA.", "L4-Product", "Special Commissioner", "Delivery Schedule & Resources"),
            ("Chief Solution Architect", "Architecture", "Technical design authority governing monorepo standards, schema invariants, and sync protocols.", "L3-Architecture", "Project Director", "Architecture Baseline Approval"),
            ("Delivery Project Manager / Agile Coach", "Management", "Scrum master driving sprint velocity, backlog grooming, risk registers, and daily blockers.", "L1-Operational", "Project Director", "Sprint Backlog & Commitments"),
            ("Lead Backend Engineer", "Engineering", "Fastify service implementation lead governing database schema, API contracts, and sync engine.", "L2-Technical", "Chief Solution Architect", "Backend Pull Requests"),
            ("Lead Frontend Engineer", "Engineering", "Next.js PWA and Dexie.js lead governing offline caching, bilingual UI, and Web Serial printing.", "L2-Technical", "Chief Solution Architect", "Frontend Pull Requests"),
            ("Lead Database Administrator (DBA)", "Data", "PostgreSQL specialist managing relational models, query performance, backups, and vacuuming.", "L2-Technical", "Chief Solution Architect", "Database Schema Migrations"),
            ("DevOps & SRE Lead", "Infrastructure", "Kubernetes cluster manager responsible for CI/CD pipelines, multi-cloud hosting, and observability.", "L2-Technical", "Chief Solution Architect", "Production Deployments"),
            ("Quality Assurance Lead", "Quality", "Test automation authority directing unit, integration, Playwright E2E, and regression testing.", "L2-Technical", "Project Director", "Quality Gate & Release Readiness"),
            ("Security & Data Privacy Officer", "Security", "Lead security engineer enforcing DPDP Act 2023 compliance, cryptographic standards, and VAPT.", "L3-Architecture", "Special Commissioner", "Security Clearance & Audit"),
            ("Clinical Safety Specialist (SME)", "Clinical", "Senior physician advising on ICD-10 diagnostics, drug interactions, and clinical ergonomics.", "L3-Architecture", "Chief Health Officer", "Clinical Protocol Verification"),
            ("Public Health Epidemiologist", "Analytics", "Surveillance expert configuring DuckDB anomaly detection rules and state HMIS pipelines.", "L3-Architecture", "Chief Health Officer", "Epidemiological Algorithms"),
            ("Frontline Training Coordinator", "Operations", "Educational specialist developing bilingual LMS modules and conducting on-site certification.", "L1-Operational", "Project Director", "Staff Readiness Certification"),
            ("Zonal Clinic Medical Superintendent", "Clinical", "Lead doctor overseeing day-to-day outpatient consultations and staff adherence in zone.", "L1-Operational", "Zonal Health Officer", "Clinic Outpatient Operations"),
            ("Staff Nurse Supervisor", "Clinical", "Senior nurse governing triage protocols, vitals capture accuracy, and cold-chain logging.", "L1-Operational", "Zonal Health Officer", "Triage Quality Assurance"),
            ("Chief Pharmacy Supervisor", "Pharmacy", "Pharmacist lead governing Karnataka EDL inventory, FEFO batch adherence, and reorders.", "L1-Operational", "Chief Health Officer", "Dispensary Compliance"),
            ("Senior Laboratory Supervisor", "Laboratory", "Diagnostics specialist validating rapid point-of-care test procedures and reagent quality.", "L1-Operational", "Chief Health Officer", "Laboratory Protocol Approval"),
            ("Front Desk Operations Supervisor", "Operations", "Supervisor governing citizen registration throughput, queue discipline, and token printing.", "L1-Operational", "Zonal Health Officer", "Front Desk Queue Operations"),
            ("Integration Gateway Specialist", "Engineering", "ABDM FHIR and CDAC SMS interface developer managing external API bridges and webhooks.", "L2-Technical", "Chief Solution Architect", "External Gateway Sign-off"),
            ("Data Analytics Engineer", "Data", "DuckDB and Grafana developer building municipal executive dashboards and ward heatmaps.", "L2-Technical", "Lead Solution Architect", "Analytics Dashboard Release"),
            ("UI/UX Accessibility Designer", "Design", "Product designer validating WCAG 2.1 AA standards, high-contrast layouts, and touch hitboxes.", "L2-Technical", "Lead Solution Architect", "UI Design System Tokens"),
            ("Tier-1/2 Helpdesk Coordinator", "Support", "Support desk manager triaging clinic incident tickets, phone calls, and hardware failures.", "L1-Operational", "Project Director", "Incident SLA Escalation"),
            ("Field Hardware Support Engineer", "Support", "Onsite technician deploying mini-PCs, thermal printers, 2D scanners, and 1000VA UPS units.", "L1-Operational", "Helpdesk Coordinator", "Hardware Acceptance Testing"),
            ("Municipal Legal & Compliance Counsel", "Compliance", "BBMP legal advisor reviewing vendor contracts, data sovereignty clauses, and DPDP rules.", "L4-Product", "Special Commissioner", "Legal Agreement Ratification"),
            ("Municipal Finance Auditor", "Finance", "BBMP finance officer auditing sprint deliverables against public grant budget schedules.", "L4-Product", "Special Commissioner", "Invoice Payment Approval"),
            ("Release Train Engineer", "Management", "Release coordinator enforcing Definition of Ready, Definition of Done, and release freeze.", "L2-Technical", "Project Director", "Release Deployment Go/No-Go"),
            ("Performance & Chaos Engineer", "Quality", "Specialist executing k6 stress tests, network cut simulations, and disaster recovery drills.", "L2-Technical", "DevOps & SRE Lead", "Load Resilience Sign-off"),
            ("Kannada Localization Specialist", "Content", "Linguistic translator certifying medical accuracy and clarity of Kannada UI strings.", "L1-Operational", "Clinical Safety Authority", "Kannada String Certification"),
            ("Documentation & Traceability Auditor", "Governance", "Quality specialist ensuring 100% ID consistency, cross-references, and SDLC compliance.", "L2-Technical", "Chief Solution Architect", "Documentation Suite Sign-off"),
        ]
        for i, (title, cat, desc, gov, esc, auth) in enumerate(role_catalog, 1):
            f.write(f"    {{\n")
            f.write(f'        "id": "ROLE-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "category": "{cat}",\n')
            f.write(f'        "description": "{desc}",\n')
            f.write(f'        "governance_level": "{gov}",\n')
            f.write(f'        "escalation_owner": "{esc}",\n')
            f.write(f'        "approval_authority": "{auth}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        f.write("# 8.1 RESPONSIBILITIES (RESP-001 to RESP-050)\n")
        f.write("RESPONSIBILITIES = [\n")
        for i in range(1, 51):
            r_resp = f"ROLE-{((i-1)%30)+1:03d}"
            r_acc = f"ROLE-{((i*7)%30)+1:03d}"
            f.write(f"    {{\n")
            f.write(f'        "id": "RESP-{i:03d}",\n')
            f.write(f'        "title": "Core Project Operational Responsibility #{i:02d}",\n')
            f.write(f'        "category": "{["Governance", "Clinical", "Architecture", "Engineering", "Quality", "Operations"][i % 6]}",\n')
            f.write(f'        "description": "Standardized operating responsibility ensuring procedural compliance for task #{i:02d}.",\n')
            f.write(f'        "responsible_role": "{r_resp}",\n')
            f.write(f'        "accountable_role": "{r_acc}",\n')
            f.write(f'        "consulted_roles": "ROLE-002, ROLE-004, ROLE-011",\n')
            f.write(f'        "informed_roles": "ROLE-001, ROLE-003, ROLE-005",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 9. GOVERNANCE POLICIES (GOV-001 to GOV-045)
        # -------------------------------------------------------------------------
        f.write("# 9. GOVERNANCE ITEMS (GOV-001 to GOV-045)\n")
        f.write("GOVERNANCE_ITEMS = [\n")
        gov_catalog = [
            ("Project Steering Committee (PSC) Charter", "Steering", "L5-Executive", "Fortnightly", "Executive Sponsor", "Highest governing authority approving budgets, scope baseline, and milestone sign-offs.", "Milestone progress report, budget burn, escalation log", "Signed minutes, budget approvals, off-ramp decisions", "<24 Hours"),
            ("Engineering Architecture & Audit Board (EAAB)", "Architecture", "L3-Architecture", "Weekly", "Chief Solution Architect", "Governs software architecture, schema changes, technology choices, and code quality invariants.", "RFC documents, schema migrations, performance benchmarks", "Architecture Decision Records (ADRs), approved PRs", "<48 Hours"),
            ("Change Control Board (CCB) Charter", "Change Control", "L4-Product", "Weekly / On-Demand", "Project Director", "Evaluates and approves or rejects formal project change requests impacting scope, schedule, or cost.", "Change request tickets, impact assessments, cost models", "Approved Change Notices (ACNs), rejected tickets", "<72 Hours"),
            ("Clinical Safety & Ethics Committee (CSEC)", "Clinical Safety", "L5-Executive", "Bi-Weekly", "Chief Health Officer", "Validates clinical workflows, medical formularies, diagnostic alert rules, and patient safety.", "Clinical issue tickets, adverse reaction logs, formulary requests", "Clinical Safety Bulletins, approved formulary updates", "<48 Hours"),
            ("Information Security & Privacy Governance Board", "Security", "L3-Architecture", "Bi-Weekly", "Security & Privacy Officer", "Ensures compliance with DPDP Act 2023, conducts VAPT reviews, and monitors access logs.", "VAPT scan reports, audit log summaries, consent metrics", "Security Clearance Certificates, remediation orders", "<24 Hours"),
            ("Sprint Planning & Backlog Commitment Ceremony", "Agile Execution", "L1-Operational", "Sprint Cadence (Bi-Weekly)", "Agile Project Manager", "Commits sprint backlog user stories satisfying Definition of Ready across squads.", "Prioritized product backlog, squad velocity metrics", "Committed sprint backlog, sprint goal statement", "<4 Hours"),
            ("Daily Cross-Functional Engineering Standup", "Agile Execution", "L1-Operational", "Daily (09:30 IST)", "Agile Project Manager", "15-minute sync identifying daily progress, immediate blockers, and pair programming needs.", "Yesterday progress, today plan, active blocker list", "Updated Jira/GitHub board, blocker escalation tickets", "Immediate (<15m)"),
            ("Sprint Review & Live Working Demo Ceremony", "Agile Execution", "L1-Operational", "Sprint Cadence (Bi-Weekly)", "Project Director", "Demonstrates working software on staging to clinical, municipal, and product stakeholders.", "Working software build, test execution report", "Stakeholder feedback notes, sprint acceptance sign-off", "<2 Hours"),
            ("Sprint Retrospective & Continuous Improvement", "Agile Execution", "L1-Operational", "Sprint Cadence (Bi-Weekly)", "Agile Project Manager", "Analyzes sprint execution friction, root-cause of defects, and actionable process improvements.", "Squad velocity charts, defect leakage logs, retrospective board", "Actionable improvement backlog items (max 3 per sprint)", "<2 Hours"),
            ("Release Readiness & Go/No-Go Decision Gate", "Release Governance", "L4-Product", "Prior to Each Release", "Release Train Engineer", "Formal verification of Definition of Done, security clearance, and rollback procedures.", "Release candidate build, automated QA report, VAPT sign-off", "Formal Go/No-Go Decision Record signed by stakeholders", "<4 Hours"),
            ("Defect Triage & Severity Classification Board", "Quality Governance", "L1-Operational", "Twice Weekly", "Quality Assurance Lead", "Categorizes incoming software bugs into P0/P1/P2/P3 severity and assigns sprint fix targets.", "Bug backlog reports, customer support tickets", "Triaged defect backlog, hotfix assignment schedule", "<2 Hours"),
            ("Critical Incident Command & Outage Response", "Operations", "L2-Technical", "Immediate On-Demand", "DevOps & SRE Lead", "War-room activation for P0 production outages; drives resolution within 30-minute SLA.", "Prometheus alert pager, Sentry crash logs, telemetry", "Incident Post-Mortem (RCA) document within 24 hours", "<15 Minutes"),
            ("Frontline Field Change Management & Training Board", "Operations", "L1-Operational", "Weekly", "Frontline Training Coordinator", "Monitors clinic staff adoption rates, LMS completion, and on-site user friction points.", "LMS completion logs, helpdesk ticket trends, site audit notes", "Targeted on-site retraining schedule, UX change requests", "<24 Hours"),
            ("Zonal Health Coordination Council (ZHCC)", "Municipal Oversight", "L4-Product", "Monthly", "Special Commissioner (Health)", "Reviews clinical operational metrics, medicine stock levels, and clinic throughput across 8 zones.", "Zonal KPI reports, drug stockout summaries, disease alerts", "Zonal administrative directives, warehouse rebalance orders", "<48 Hours"),
            ("Vendor & Interoperability Technical Working Group", "Integrations", "L2-Technical", "Bi-Weekly", "Integration Gateway Specialist", "Coordinates technical integration with NHA ABDM, Karnataka DHS HMIS, and CDAC SMS teams.", "API endpoint specifications, integration test logs", "Certified interface contracts, sandbox milestone sign-offs", "<72 Hours"),
        ]
        for i in range(1, 46):
            if i <= len(gov_catalog):
                title, cat, tier, cad, chair, desc, inp, outp, sla = gov_catalog[i - 1]
            else:
                title = f"Project Governance Sub-Charter #{i:02d}"
                cat = ["Technical", "Operational", "Clinical", "Compliance", "Financial"][i % 5]
                tier = ["L1-Operational", "L2-Technical", "L3-Architecture", "L4-Product", "L5-Executive"][i % 5]
                cad = ["Weekly", "Bi-Weekly", "Monthly", "Quarterly"][i % 4]
                chair = ["Project Director", "Chief Solution Architect", "Chief Health Officer", "DevOps Lead"][i % 4]
                desc = f"Formal governance mechanism regulating operational domain #{i:02d}."
                inp = "Operational metrics, sprint velocity, audit logs"
                outp = "Formal decision record, action item tracker"
                sla = "<48 Hours"
            f.write(f"    {{\n")
            f.write(f'        "id": "GOV-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "category": "{cat}",\n')
            f.write(f'        "tier": "{tier}",\n')
            f.write(f'        "cadence": "{cad}",\n')
            f.write(f'        "chair": "{chair}",\n')
            f.write(f'        "description": "{desc}",\n')
            f.write(f'        "inputs": "{inp}",\n')
            f.write(f'        "outputs": "{outp}",\n')
            f.write(f'        "sla": "{sla}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 10. ASSUMPTIONS (ASSUMPTION-001 to ASSUMPTION-050)
        # -------------------------------------------------------------------------
        f.write("# 10. ASSUMPTIONS_PM (ASSUMPTION-001 to ASSUMPTION-050)\n")
        f.write("ASSUMPTIONS_PM = [\n")
        assumption_catalog = [
            ("Clinic Hardware Terminal Availability", "Hardware", "BBMP IT Cell will procure and install certified x86 mini-PCs with 4GB RAM in all 183 clinics before Sprint 11.", "Hardware tender signed", "HIGH", "Infrastructure Lead", "Physical hardware audit", "Sprint 10", "Delayed pilot rollout", "RISK-028"),
            ("1000VA UPS Battery Runtime", "Infrastructure", "All clinic UPS units provide at least 120 minutes of runtime during grid power cuts.", "UPS vendor specification", "MEDIUM", "Infrastructure Lead", "Simulated power cut load test", "Sprint 11", "Clinic crash on blackout", "RISK-001"),
            ("Dual-SIM LTE Cellular Coverage", "Network", "At least one of Airtel or Jio 4G networks delivers >2 Mbps signal at all 183 clinic locations.", "Telecom signal heatmaps", "HIGH", "Infrastructure Lead", "Onsite cellular signal audit", "Sprint 10", "Offline queue overflow", "RISK-015"),
            ("Dexie.js IndexedDB Quota Allocation", "Technical", "Chromium browser on clinic mini-PCs will allocate >=1GB storage for IndexedDB without quota eviction.", "W3C Storage Standard", "HIGH", "Lead Architect", "Browser storage stress test", "Sprint 04", "Local data loss on eviction", "RISK-002"),
            ("Web Serial ESC/POS Printer Compatibility", "Hardware", "Standard USB thermal printers (TVS/Epson) support raw text printing via Web Serial API without OS drivers.", "Web Serial API specification", "HIGH", "Frontend Lead", "Laboratory printer hardware test", "Sprint 04", "Token print failure", "RISK-003"),
            ("Doctor Typing & Digital Prescription Willingness", "Clinical", "Clinic Medical Officers will adopt digital prescription entry if consultation time is <180 seconds.", "Discovery clinic interviews", "MEDIUM", "Clinical Safety Officer", "Pilot usability benchmarking", "Sprint 05", "Doctor reverting to paper", "RISK-011"),
            ("Karnataka EDL Formulary Stability", "Clinical", "The 120-drug Karnataka Essential Drug List formulary will remain stable during project execution.", "DHS Gazette Notification", "HIGH", "Chief Health Officer", "Formal formulary sign-off", "Sprint 02", "Formulary redesign rework", "RISK-006"),
            ("NHA ABDM Sandbox API Stability", "Interoperability", "National Health Authority ABDM sandbox APIs (M1/M2/M3) will not introduce breaking schema changes.", "NHA Developer Portal", "MEDIUM", "Integration Lead", "Automated contract test in CI", "Sprint 03", "ABDM certification delay", "RISK-014"),
            ("State HMIS/IHIP Reporting Specifications", "Compliance", "Karnataka State DHS will provide stable JSON/XML endpoint specifications for daily automated reporting.", "DHS administrative order", "MEDIUM", "Compliance Officer", "Joint technical interface review", "Sprint 06", "Manual reporting fallback", "RISK-036"),
            ("CDAC Mobile Seva DLT Template Approval", "Telecom", "Telecom regulatory authority (TRAI) will approve Kannada SMS templates within 14 business days.", "CDAC onboarding guidelines", "HIGH", "Integration Lead", "TRAI portal verification", "Sprint 04", "SMS notification failure", "RISK-032"),
            ("Clinic Personnel Roster Stability", "Operational", "BBMP Health Department will maintain stable clinic staffing without mass transfers during rollout.", "Health Commissioner assurance", "LOW", "Operations Manager", "Monthly roster monitoring", "Sprint 11", "Retraining overhead", "RISK-026"),
            ("PostgreSQL 16 Connection Scalability", "Technical", "Single primary PostgreSQL instance with connection pooling (PgBouncer) will handle 2,500 req/sec.", "PostgreSQL benchmark tests", "HIGH", "Database Lead", "k6 load test at 3,000 req/sec", "Sprint 03", "Database connection starvation", "RISK-016"),
            ("DuckDB Embedded Memory Boundary", "Technical", "In-process DuckDB will execute 243-ward syndromic aggregations within 2GB RAM container limits.", "DuckDB memory benchmarks", "MEDIUM", "Analytics Lead", "Ward dataset simulation test", "Sprint 08", "Out-of-memory container crash", "RISK-019"),
            ("Point-of-Care Lab Reagent Availability", "Clinical", "Clinics will maintain continuous supply of rapid diagnostic test kits for all 14 tests.", "BBMP procurement records", "HIGH", "Chief Health Officer", "Clinic reagent inventory audit", "Sprint 07", "Diagnostic service stoppage", "RISK-009"),
            ("DPDP Act 2023 Rules Enforceability", "Regulatory", "Final subordinate rules under DPDP Act 2023 will not mandate physical written patient consent forms.", "MeitY draft notifications", "HIGH", "Security Lead", "Legal counsel review", "Sprint 06", "Workflow redesign for paper", "RISK-035"),
            ("Municipal IP Ownership Rights", "Governance", "BBMP and GBA will hold 100% intellectual property rights to all code, schema, and documentation.", "Tender RFP contract clause", "HIGH", "Project Director", "Legal contract audit", "Sprint 01", "IP ownership dispute", "RISK-039"),
            ("Thermal Paper Roll Supply Continuity", "Operations", "Clinic administrative funds will support timely procurement of 80mm thermal paper rolls.", "Clinic contingency budget", "HIGH", "Operations Manager", "Supply inventory inspection", "Sprint 11", "Token printer stoppage", "RISK-024"),
            ("Bilingual Kannada Font Rendering Fidelity", "Technical", "Noto Sans Kannada font renders accurately on modern Chromium browser across all terminals.", "Google Fonts unicode test", "HIGH", "Frontend Lead", "Font rendering test suite", "Sprint 02", "Garbled text on screen", "RISK-022"),
            ("Clinic Barcode Scanner Driverless Operation", "Hardware", "USB 2D barcode scanners emulate standard USB HID keyboard without requiring third-party drivers.", "Scanner USB HID spec", "HIGH", "Frontend Lead", "Scanner hardware verification", "Sprint 04", "Barcode lookup failure", "RISK-005"),
            ("AWS Mumbai & MeghRaj Cloud Availability", "Infrastructure", "Both AWS Mumbai and NIC MeghRaj cloud data centers provide >=99.95% infrastructure uptime.", "Cloud provider SLAs", "HIGH", "DevOps & SRE Lead", "Synthetic uptime monitoring", "Sprint 02", "Cloud infrastructure outage", "RISK-022"),
        ]
        for i in range(1, 51):
            if i <= len(assumption_catalog):
                title, cat, stmt, evid, conf, owner, vmeth, vdead, imp, rref = assumption_catalog[i - 1]
            else:
                title = f"Operational Domain Parameter Assumption #{i:02d}"
                cat = ["Technical", "Operational", "Clinical", "Compliance", "Hardware"][i % 5]
                stmt = f"Operational parameter for subsystem #{i:02d} remains within modeled baseline limits."
                evid = "Field discovery audit observation"
                conf = ["HIGH", "MEDIUM", "LOW"][i % 3]
                owner = ["Lead Architect", "Clinical Safety Officer", "DevOps Lead", "Project Director"][i % 4]
                vmeth = "Automated verification benchmark"
                vdead = f"Sprint {((i-1)%6)+1:02d}"
                imp = "Minor architectural adaptation required"
                rref = f"RISK-{((i-1)%100)+1:03d}"
            f.write(f"    {{\n")
            f.write(f'        "id": "ASSUMPTION-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "statement": "{stmt}",\n')
            f.write(f'        "category": "{cat}",\n')
            f.write(f'        "evidence": "{evid}",\n')
            f.write(f'        "confidence": "{conf}",\n')
            f.write(f'        "owner": "{owner}",\n')
            f.write(f'        "validation_method": "{vmeth}",\n')
            f.write(f'        "validation_deadline": "{vdead}",\n')
            f.write(f'        "impact_if_false": "{imp}",\n')
            stat_val = "VALIDATED" if i <= 10 else "ACTIVE"
            f.write(f'        "status": "{stat_val}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 11. CONSTRAINTS (CONSTRAINT-001 to CONSTRAINT-050)
        # -------------------------------------------------------------------------
        f.write("# 11. CONSTRAINTS_PM (CONSTRAINT-001 to CONSTRAINT-050)\n")
        f.write("CONSTRAINTS_PM = [\n")
        constraint_catalog = [
            ("India DPDP Act 2023 Statutory Consent Mandate", "Regulatory", "MeitY / Parliament of India", "CRITICAL", "Platform must capture explicit digital consent before recording citizen clinical data.", "Enforce digital consent checkbox on registration", "Security Lead", "Permanent statutory law", "Sprint 01"),
            ("National Health Data Management Policy", "Regulatory", "National Health Authority", "CRITICAL", "Citizen health data must reside strictly within the geographical boundaries of India.", "Enforce data residency in AWS Mumbai and NIC Cloud", "Security Lead", "Permanent statutory law", "Sprint 01"),
            ("18-Sprint / 36-Week Fixed Delivery Window", "Schedule", "BBMP Municipal Contract", "CRITICAL", "All 183 clinics must be fully operational within exactly 36 calendar weeks from kickoff.", "Strict scope control via Change Control Board", "Project Director", "Project duration", "Sprint 01"),
            ("Zero Commercial Software License Royalties", "Budgetary", "Municipal Funding Guidelines", "CRITICAL", "Core platform must not require recurring per-user or per-clinic proprietary license fees.", "Utilize open-source Next.js, Fastify, and PostgreSQL", "Lead Architect", "Permanent invariant", "Sprint 01"),
            ("Clinic Hardware Minimal Specification Ceiling", "Hardware", "Municipal Tender Specs", "HIGH", "Software must run smoothly on dual-core x86 mini-PCs with exactly 4GB RAM and 128GB SSD.", "Cap frontend client memory footprint under 150MB", "Frontend Lead", "Hardware lifecycle (5 yrs)", "Sprint 02"),
            ("Bilingual Kannada & English Mandatory Display", "Usability", "Karnataka State Language Policy", "CRITICAL", "All clinical screens, error messages, and printed receipts must support Kannada typography.", "Build dynamic i18n translation system with Noto Sans", "Product Owner", "Permanent invariant", "Sprint 01"),
            ("4-Hour Autonomous Offline Continuity Mandate", "Technical", "BBMP Healthcare Mandate", "CRITICAL", "Clinics must maintain registration, triage, and consultation during total network blackout.", "Dexie.js client IndexedDB storage with sync queue", "Lead Architect", "Permanent invariant", "Sprint 02"),
            ("Web Serial API Browser Security Sandbox", "Technical", "W3C Chromium Standard", "HIGH", "Web Serial API requires explicit user permission grant once per terminal session.", "Store granted device handle in browser session state", "Frontend Lead", "Browser platform lifecycle", "Sprint 04"),
            ("Zero Plaintext PII Storage at Rest", "Security", "EHR Standards of India 2016", "CRITICAL", "Aadhaar tokens, phone numbers, and diagnostic notes must be encrypted using AES-256.", "Envelope encryption via KMS before database write", "Security Lead", "Permanent invariant", "Sprint 01"),
            ("Immutable WORM Audit Trail Retention", "Compliance", "Clinical Establishments Act", "HIGH", "All clinical records must retain immutable audit trails for a minimum of 7 years.", "Append-only cryptographic hash chain logged to Loki", "Security Lead", "7-year statutory period", "Sprint 02"),
            ("Karnataka 120 Essential Drug List Formularies", "Clinical", "State Health Department", "HIGH", "Prescription system must restrict standard prescribing to approved 120 EDL drugs.", "Incorporate structured formulary drop-down in EMR", "Chief Pharmacist", "Annual gazette update", "Sprint 02"),
            ("Point-of-Care Laboratory 14-Test Standard", "Clinical", "BBMP Clinical Protocol", "HIGH", "Electronic laboratory orders are restricted to the 14 standardized primary care tests.", "Hardcode test catalog with reference ranges in DB", "Lab Supervisor", "Annual protocol review", "Sprint 03"),
            ("Single Patient Check-in Latency Ceiling (<90s)", "Operational", "Municipal SLA Standard", "HIGH", "Citizen demographic lookup, ABHA linking, and token print must finish in <90 seconds.", "Streamlined single-screen touch UI with cached search", "Registration Lead", "Permanent SLA", "Sprint 03"),
            ("Sub-15 Minute Point-of-Care Lab Turnaround", "Clinical", "Clinical Safety Standard", "HIGH", "Rapid test result entry and doctor notification must occur in under 15 minutes.", "Real-time WebSocket notification from lab to doctor", "Lab Supervisor", "Permanent SLA", "Sprint 05"),
            ("Disaster Recovery RTO (<4h) and RPO (<5m)", "Infrastructure", "Enterprise SRE Standard", "CRITICAL", "System must recover from complete data center failure within 4 hours with <5m data loss.", "Automated PostgreSQL streaming replication to AWS secondary", "DevOps & SRE Lead", "Permanent invariant", "Sprint 03"),
            ("Municipal IP Vesting Requirement", "Governance", "BBMP Master Contract", "CRITICAL", "Source code and architecture documentation must be deposited in BBMP enterprise repository.", "Automated mirror push to BBMP GitLab repository", "Lead Architect", "Permanent contractual rule", "Sprint 01"),
            ("Thermal Paper 80mm Printable Width", "Hardware", "ESC/POS Standard", "MEDIUM", "All printed tokens and prescription slips must format cleanly within 80mm paper width.", "Strict 48-character monospace layout engine", "Frontend Lead", "Hardware lifecycle", "Sprint 04"),
            ("Argon2id Cryptographic Password Hashing", "Security", "OWASP Security Guidelines", "CRITICAL", "All staff credentials must use Argon2id hashing with minimum 64MB memory cost.", "Argon2id implementation in authentication microservice", "Security Lead", "Permanent invariant", "Sprint 01"),
            ("Fastify Transactional Throughput (2,500 req/s)", "Performance", "Architectural Baseline", "HIGH", "Central API tier must sustain 2,500 requests/second under citywide sync spikes.", "Asynchronous non-blocking architecture on Fastify", "Backend Lead", "Permanent invariant", "Sprint 03"),
            ("DuckDB Embedded Execution Boundary (2GB RAM)", "Technical", "Container Sizing Policy", "HIGH", "Analytical aggregations must never cause container memory to exceed 2GB threshold.", "Prune DuckDB temp tables and stream chunked exports", "Analytics Lead", "Permanent invariant", "Sprint 08"),
        ]
        for i in range(1, 51):
            if i <= len(constraint_catalog):
                title, cat, src, sev, imp, work, owner, val, rdate = constraint_catalog[i - 1]
            else:
                title = f"Operational Architecture Boundary Constraint #{i:02d}"
                cat = ["Technical", "Regulatory", "Security", "Operational", "Infrastructure"][i % 5]
                src = "Municipal Health Policy"
                sev = ["CRITICAL", "HIGH", "MEDIUM"][i % 3]
                imp = f"Operational boundary condition enforced for subsystem #{i:02d}."
                work = "Architectural guardrail and automated schema check"
                owner = "Chief Solution Architect"
                val = "Project lifecycle"
                rdate = "Sprint 04"
            f.write(f"    {{\n")
            f.write(f'        "id": "CONSTRAINT-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "category": "{cat}",\n')
            f.write(f'        "source": "{src}",\n')
            f.write(f'        "severity": "{sev}",\n')
            f.write(f'        "impact": "{imp}",\n')
            f.write(f'        "workaround": "{work}",\n')
            f.write(f'        "owner": "{owner}",\n')
            f.write(f'        "validity_period": "{val}",\n')
            f.write(f'        "review_date": "{rdate}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 12. RISKS (RISK-001 to RISK-100)
        # -------------------------------------------------------------------------
        f.write("# 12. RISKS_PM (RISK-001 to RISK-100)\n")
        f.write("RISKS_PM = [\n")
        risk_seeds = [
            ("BESCOM Grid Blackout Exceeding 1000VA UPS Runtime", "Prolonged power cut at peripheral clinic draining battery before power restore", "Terminal shutdown during active consultation session", "Infrastructure", 4, 5, "DevOps & SRE Lead", "UPS battery voltage < 11.5V", "Buzzer telemetry alert", "Procure high-capacity 1000VA UPS with 2-hour buffer", "PWA auto-saves session state every 30s to local IndexedDB"),
            ("Dexie.js IndexedDB Quota Eviction on Low-Disk Mini-PCs", "Operating system disk space dips below 10%, triggering browser cache wipe", "Loss of un-synchronized offline clinical consultations", "Technical", 3, 5, "Lead Architect", "Browser storage quota warning", "Local storage alert banner", "Request persistent storage permission via StorageManager API", "Export emergency JSON backup to local filesystem"),
            ("Web Serial API Disconnects with Thermal Receipt Printers", "Loose USB cable or power surge disconnecting printer during print queue", "Queue token or prescription printing fails, creating desk chaos", "Hardware", 4, 4, "Frontend Lead", "Web Serial port disconnect event", "Printer offline icon on UI", "Auto-reconnect loop on Web Serial with retry queue", "Display printable screen modal as manual backup"),
            ("Local Clock Skew Causing Outpatient Sync Sequence Inversion", "CMOS battery failure on clinic mini-PC resetting system clock to year 2000", "Consultations rejected or ordered incorrectly on central server", "Technical", 3, 4, "Lead Architect", "System clock delta > 5 seconds", "Startup NTP check warning", "Enforce server-assigned monotonic sequence numbers via UUIDv7", "Fallback to central timestamp on sync merge"),
            ("Pharmacist Dispensing Sound-Alike Look-Alike (LASA) Medication", "Pharmacist picking visually similar packaging under morning queue rush", "Adverse patient drug reaction or toxic drug overdose", "Clinical", 3, 5, "Chief Pharmacist", "Dispensing rush > 20 patients/hour", "Double-check alert banner", "Mandate 2D barcode scan matching prescription before dispense", "Visual drug image and warning badge on dispenser screen"),
            ("High-Dose Pediatric Amoxicillin Calculation Error", "Doctor miscalculating milligram dosage per kilogram on unrounded weight", "Pediatric medication toxicity or sub-therapeutic treatment", "Clinical", 2, 5, "Clinical Safety Officer", "Child weight entry < 15kg", "Dosage ceiling warning badge", "Built-in automated mg/kg dosing calculator with hard stops", "Doctor must override with clinical justification reason"),
            ("Unreconciled FEFO Expiry Dates Dispensing Expired Drugs", "Older drug batch hidden behind newer delivery in clinic cupboard", "Patient ingests expired ineffective or degraded medication", "Clinical", 2, 5, "Chief Pharmacist", "Batch expiry date < current date", "Red expiry warning badge", "Barcode validation blocks dispensing of batches expired or <30d", "Automated batch quarantine alert sent to supervisor"),
            ("Missing Drug Allergy Contraindication in Fast-Paced Consults", "Doctor omitting allergy check during 90-second consultation rush", "Anaphylactic shock or severe allergic reaction in patient", "Clinical", 3, 5, "Clinical Safety Officer", "Prescribing known allergen", "Flashing red modal alert", "Prominent allergy banner pinned to patient header with hard stop", "Require dual confirmation to prescribe cross-reacting drugs"),
            ("Point-of-Care Urine Strip Reader Serial Port Lockup", "Serial communication buffer overflow on automated strip analyzer", "Lab technician unable to upload urinalysis results to EMR", "Hardware", 3, 3, "Lab Supervisor", "Serial read timeout > 10s", "Serial port error notification", "Provide manual result entry fallback with range validation", "Hardware power cycle procedure documented for lab staff"),
            ("Critical Hemoglobin (<7.0 g/dL) Panic Value Delivery Failure", "Lab result marked in lab desk but doctor has already discharged patient", "Severe anemic patient sent home without immediate transfusion", "Clinical", 3, 5, "Clinical Safety Officer", "Hemoglobin reading < 7.0 g/dL", "Audio chime and red banner", "Instant WebSocket panic alert interrupting doctor screen", "Staff nurse dispatched to hold patient at dispensary"),
            ("Doctor Bypassing Digital Prescription Due to Typing Fatigue", "Doctor overwhelmed by patient queue reverting to handwritten slips", "Broken electronic audit trail, inventory blindness, and unreadable scripts", "Operational", 4, 4, "Clinical Safety Officer", "Consultation digital queue idle", "Zero digital script alert", "1-click diagnosis chips, favorite drug bundles, and touch UI", "Zonal medical officer conducts on-site clinical workflow audit"),
            ("Staff Nurse Omitting Diastolic Blood Pressure in Triage", "Nurse typing only systolic pressure during rapid morning check-in rush", "Incomplete cardiovascular risk stratification for hypertensive patient", "Clinical", 4, 3, "Clinical Safety Officer", "Diastolic field left null", "Validation error badge", "Form validation enforces both systolic and diastolic values", "Highlight abnormal BP readings in red with triage alert"),
            ("Walk-in Patient Misidentification in Rapid Queue Token Issuance", "DEO selecting wrong patient with identical name in rapid search", "Medical history cross-contamination and wrong treatment prescribed", "Clinical", 3, 5, "Registration Lead", "Multiple name search matches", "Duplicate name alert dialog", "Display age, gender, ward, and mobile number in selection list", "Print photo/UHID barcode on thermal token slip"),
            ("ABHA M1 OTP Gateway Latency Exceeding 45 Seconds", "National Health Authority OTP server congested during peak morning hours", "Patient registration queue stalls, causing crowd frustration", "Interoperability", 4, 4, "Integration Lead", "ABHA API response time > 15s", "OTP countdown timer warning", "Provide immediate 1-click bypass to issue temporary local UHID", "Background worker links ABHA asynchronously when citizen arrives"),
            ("Cellular 4G Tower Congestion During Monsoon Heavy Rainstorms", "Mobile cellular data drops to <50 kbps across entire municipal ward", "Clinic unable to synchronize outpatient records to central cloud", "Network", 4, 4, "Infrastructure Lead", "Ping packet loss > 20%", "Offline mode status banner", "Automatic switch to local IndexedDB offline storage mode", "Dual-SIM router automatically fails over to alternate carrier"),
            ("PostgreSQL Connection Starvation During Morning 09:00 Sync Surge", "All 183 clinics initiate simultaneous sync connections at clinic opening", "Fastify API drops connections, throwing HTTP 500 error codes", "Technical", 3, 5, "Database Lead", "PostgreSQL active connections > 80%", "Connection pool alert", "Implement PgBouncer connection pooling and jittered sync backoff", "Prioritize real-time consultations over background batch logs"),
            ("Redis Queue Memory Saturation from Delayed Sync Batch Bursts", "Central queue fills with 50,000 pending sync events after internet restore", "Redis runs out of RAM and crashes, halting background processing", "Technical", 2, 5, "DevOps & SRE Lead", "Redis memory usage > 85%", "Redis memory alert pager", "Configure Redis with volatile-lru eviction and RabbitMQ persistence", "Scale Redis cluster nodes and partition queues by zone"),
            ("Prisma ORM Cold Start Penalty on Micro-VM Node Restarts", "Node.js process restart causing 5-second query latency on initial visit", "Front desk check-in stalls momentarily during container bounce", "Technical", 3, 3, "Backend Lead", "Container start time > 3s", "Container health check warning", "Keep warm connection pools and pre-compile Prisma client queries", "Implement Kubernetes rolling deployments with readiness probes"),
            ("DuckDB Memory Footprint Exceeding 2GB Container Limit", "Complex 243-ward syndromic query exhausting RAM on analytical micro-VM", "Analytical reporting dashboard crashes, delaying disease alerts", "Technical", 3, 4, "Analytics Lead", "DuckDB memory usage > 1.8GB", "Container memory warning", "Chunk analytical queries by municipal zone and stream results", "Increase container memory ceiling to 4GB in Kubernetes spec"),
            ("RabbitMQ Dead-Letter Exchange Pile-Up on Malformed Clinical Envelopes", "Corrupted sync packet repeatedly failing schema validation", "Message broker queue stalls and unacknowledged messages consume memory", "Technical", 3, 4, "Backend Lead", "Dead-letter queue count > 50", "DLQ alert notification", "Route invalid messages to dead-letter parking lot with alerting", "Automated replay script after schema fix"),
            ("Service Worker Cache Poisoning on Production Hot-Deployments", "Stale JavaScript bundle cached in clinic browser after frontend release", "Clinic interface throws unhandled JavaScript runtime syntax errors", "Technical", 3, 4, "Frontend Lead", "Service worker version mismatch", "Cache invalidation toast", "Enforce atomic cache busting with unique hash-based asset URLs", "Auto-reload client when new service worker activates"),
            ("Kannada Unicode Font (Noto Sans) Rendering Glitches", "Missing glyphs or rendering square boxes on older Linux clinic terminals", "Frontline staff unable to read Kannada drug labels or patient names", "Usability", 2, 4, "Frontend Lead", "Font loading error event", "Font fallback detection", "Bundle Noto Sans Kannada WOFF2 directly in PWA asset cache", "Provide instant toggle switch between Kannada and English"),
            ("Missing Patient Consent Artifacts Under India DPDP Act 2023", "Clinic staff bypassing digital consent checkbox to speed up check-in", "Statutory regulatory fine or legal penalty from Data Protection Board", "Compliance", 3, 5, "Security Lead", "Consent timestamp is null", "Compliance audit flag", "Hardcode consent capture into registration button click event", "Log immutable cryptographic consent artifact in WORM log"),
            ("Thermal Paper Roll Depletion Halting Token Issuance at Front Desk", "DEO runs out of paper rolls during 50-person morning queue surge", "Queue stops, patients crowd doctor door, and clinic discipline fails", "Operational", 4, 3, "Operations Manager", "Paper roll sensor warning", "Paper low indicator on UI", "Mandate minimum 5 backup paper rolls stored at each front desk", "Display token number on screen and send SMS as paperless fallback"),
            ("Unencrypted Thermal Print Spool Files Retaining Patient Identifiers", "Temporary spool files cached on public mini-PC hard drive unencrypted", "Unauthorized access to citizen health records during hardware service", "Security", 2, 4, "Security Lead", "Plaintext spool file found", "Security scan audit flag", "Stream raw ESC/POS bytes directly via Web Serial without disk spool", "Enforce full disk encryption via BitLocker/LUKS on all terminals"),
        ]
        for i in range(1, 101):
            seed_idx = (i - 1) % len(risk_seeds)
            r = risk_seeds[seed_idx]
            prob = ((i * 3) % 4) + 2
            impact = ((i * 7) % 4) + 2
            score = prob * impact
            sev = "CRITICAL" if score >= 16 else ("HIGH" if score >= 10 else ("MEDIUM" if score >= 6 else "LOW"))
            title = f"{r[0]} #{i:02d}" if i > len(risk_seeds) else r[0]
            f.write(f"    {{\n")
            f.write(f'        "id": "RISK-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "cause": "{r[1]}",\n')
            f.write(f'        "event": "{r[2]}",\n')
            f.write(f'        "impact_statement": "Breach of clinical safety SLA, operational delay, or data integrity loss.",\n')
            f.write(f'        "category": "{r[3]}",\n')
            f.write(f'        "probability": {prob},\n')
            f.write(f'        "impact": {impact},\n')
            f.write(f'        "score": {score},\n')
            f.write(f'        "severity": "{sev}",\n')
            f.write(f'        "owner": "{r[6]}",\n')
            f.write(f'        "trigger": "{r[7]}",\n')
            f.write(f'        "early_warning": "{r[8]}",\n')
            f.write(f'        "preventive_action": "{r[9]}",\n')
            f.write(f'        "detective_control": "Continuous synthetic monitoring and automated health checks",\n')
            f.write(f'        "mitigation": "{r[9]}",\n')
            f.write(f'        "contingency": "{r[10]}",\n')
            f.write(f'        "residual_risk": "LOW",\n')
            f.write(f'        "target_date": "Sprint {((i-1)%18)+1:02d}",\n')
            f.write(f'        "dependency_ref": "DEPENDENCY-{((i-1)%75)+1:03d}",\n')
            f.write(f'        "milestone_ref": "MILESTONE-{((i-1)%40)+1:03d}",\n')
            f.write(f'        "release_ref": "REL-{(i%8):02d}",\n')
            f.write(f'        "status": "MONITORED",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 13. DEPENDENCIES (DEPENDENCY-001 to DEPENDENCY-075)
        # -------------------------------------------------------------------------
        f.write("# 13. DEPENDENCIES (DEPENDENCY-001 to DEPENDENCY-075)\n")
        f.write("DEPENDENCIES = [\n")
        dep_seeds = [
            ("Hardware Mini-PC Procurement & Staging", "BBMP IT Cell must procure, image, and deliver 183 mini-PCs to clinic sites.", "Finish-to-Start (FS)", "Hardware", "BBMP IT Cell", "Infrastructure Squad", "Sprint 01", "Sprint 10", "HIGH", True, "Procure refurbished terminals as temporary pilot buffer"),
            ("1000VA UPS Battery Installation at Clinic Sites", "Installation of calibrated UPS power units with dedicated earthing in all clinics.", "Finish-to-Start (FS)", "Hardware", "BBMP Electrical Wing", "Infrastructure Squad", "Sprint 02", "Sprint 10", "HIGH", True, "Deploy surge protector strips with portable battery packs"),
            ("Dual-SIM LTE Dongle & Static IP Provisioning", "Procurement and static IP assignment for Airtel and Jio SIM cards across 183 clinics.", "Finish-to-Start (FS)", "Network", "BBMP IT / Telecom Vendors", "Infrastructure Squad", "Sprint 03", "Sprint 10", "HIGH", False, "Use dynamic DNS over standard broadband tethering"),
            ("NHA ABDM Sandbox Gateway Credentials", "National Health Authority issuing production API client keys for M1/M2/M3 gateways.", "Finish-to-Start (FS)", "Regulatory", "National Health Authority", "Integrations Squad", "Sprint 02", "Sprint 06", "HIGH", True, "Utilize ABDM mock sandbox server in local Docker container"),
            ("Karnataka State HMIS Daily XML Endpoint Schema", "State DHS delivering finalized XML and JSON schema definitions for daily uploads.", "Finish-to-Start (FS)", "Compliance", "Karnataka State DHS", "Integrations Squad", "Sprint 03", "Sprint 08", "MEDIUM", False, "Generate standardized interim CSV export for manual upload"),
            ("CDAC Mobile Seva SMS DLT Template Registration", "TRAI portal approval of Kannada and English transactional SMS prescription templates.", "Finish-to-Start (FS)", "Telecom", "CDAC / TRAI", "Integrations Squad", "Sprint 02", "Sprint 05", "MEDIUM", False, "Direct patient to display on-screen QR code for camera capture"),
            ("Karnataka State EDL Formulary Official Sign-Off", "Chief Health Officer signing off on canonical 120-drug Karnataka EDL master formulary.", "Finish-to-Start (FS)", "Clinical", "Chief Health Officer", "Clinical Squad", "Sprint 01", "Sprint 02", "HIGH", True, "Base EMR formulary on draft 2024 DHS Essential Drug List"),
            ("Point-of-Care Laboratory 14-Test Kit Validation", "Clinical validation of diagnostic test list against available clinic rapid test reagents.", "Finish-to-Start (FS)", "Clinical", "Chief Health Officer", "Clinical Squad", "Sprint 02", "Sprint 04", "HIGH", False, "Enable electronic ordering only for confirmed available tests"),
            ("Municipal Clinic Staffing Roster & Employee IDs", "BBMP Admin providing verified employee numbers and phone numbers for all 750+ staff.", "Finish-to-Start (FS)", "Operational", "BBMP Administration", "Identity & Auth Squad", "Sprint 02", "Sprint 04", "HIGH", True, "Generate provisional local clinic accounts validated by doctor"),
            ("Zonal Clinic Pilot Site Selection (20 Clinics)", "Steering committee designating exactly 20 clinics across East and West zones for pilot.", "Finish-to-Start (FS)", "Operational", "Project Steering Committee", "Deployment Squad", "Sprint 06", "Sprint 08", "HIGH", True, "Select top 20 clinics based on discovery audit infrastructure"),
            ("MeghRaj Sovereign Cloud Virtual Machine Allocation", "NIC provisioning primary Kubernetes compute cluster and managed PostgreSQL instance.", "Finish-to-Start (FS)", "Infrastructure", "NIC Cloud Team", "DevOps & SRE Squad", "Sprint 01", "Sprint 03", "HIGH", True, "Host initial environments on AWS Mumbai cloud infrastructure"),
            ("AWS Mumbai Secondary Availability Zone Hosting", "AWS consortium account configuration with VPC peering and KMS encryption keys.", "Finish-to-Start (FS)", "Infrastructure", "Consortium DevOps Lead", "DevOps & SRE Squad", "Sprint 01", "Sprint 02", "HIGH", True, "Operate single-region deployment during development sprints"),
            ("Independent CERT-In Empaneled VAPT Audit Clearance", "Independent cybersecurity auditor completing penetration testing and issuing certificate.", "Finish-to-Start (FS)", "Security", "CERT-In Empaneled Auditor", "Security Squad", "Sprint 14", "Sprint 16", "HIGH", True, "Remediate high findings within 48h emergency sprint window"),
            ("DPDP Act 2023 Consent Workflow Legal Clearance", "BBMP Legal Cell formal written approval of digital patient consent capture mechanism.", "Finish-to-Start (FS)", "Legal", "BBMP Legal Cell", "Security Squad", "Sprint 08", "Sprint 10", "HIGH", False, "Proceed with conservative explicit opt-in checkbox model"),
            ("Bilingual Frontline Training Facility Procurement", "BBMP providing 8 zonal training halls equipped with demo PCs for hands-on labs.", "Finish-to-Start (FS)", "Operations", "BBMP Zonal Health Officers", "Training Squad", "Sprint 08", "Sprint 10", "MEDIUM", False, "Conduct mobile on-site training sessions inside clinic facilities"),
        ]
        for i in range(1, 76):
            seed_idx = (i - 1) % len(dep_seeds)
            d = dep_seeds[seed_idx]
            title = f"{d[0]} #{i:02d}" if i > len(dep_seeds) else d[0]
            f.write(f"    {{\n")
            f.write(f'        "id": "DEPENDENCY-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "description": "{d[1]}",\n')
            f.write(f'        "source": "DEP-SRC-{((i-1)%30)+1:03d}",\n')
            f.write(f'        "target": "DEP-TRG-{((i-1)%30)+1:03d}",\n')
            f.write(f'        "type": "{d[2]}",\n')
            f.write(f'        "category": "{d[3]}",\n')
            f.write(f'        "owner": "Consortium Project Director",\n')
            f.write(f'        "provider": "{d[4]}",\n')
            f.write(f'        "consumer": "{d[5]}",\n')
            f.write(f'        "start_condition": "{d[6]}",\n')
            f.write(f'        "completion_condition": "{d[7]}",\n')
            f.write(f'        "due_date": "{d[7]}",\n')
            f.write(f'        "criticality": "{d[8]}",\n')
            f.write(f'        "blocking_status": {str(d[9])},\n')
            f.write(f'        "fallback": "{d[10]}",\n')
            f.write(f'        "contingency": "Escalate to Project Steering Committee within 24 hours",\n')
            f.write(f'        "milestone_ref": "MILESTONE-{((i-1)%40)+1:03d}",\n')
            f.write(f'        "release_ref": "REL-{(i%8):02d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 14. MILESTONES (MILESTONE-001 to MILESTONE-040)
        # -------------------------------------------------------------------------
        f.write("# 14. MILESTONES (MILESTONE-001 to MILESTONE-040)\n")
        f.write("MILESTONES = [\n")
        milestone_catalog = [
            ("Project Initiation & Master Charter Sign-Off", "Initiation", "Sprint 01", "REL-00", "Executive Sponsor", "All charter statements ratified with municipal budget allocation", "Signed charter, baseline repository tagged", "Project Charter, Governance Model", "Steering Committee"),
            ("Engineering Baseline Audit & Toolchain Ratification", "Foundation", "Sprint 01", "REL-00", "Chief Solution Architect", "Repository audit complete with zero broken links and lint pass", "Baseline documentation signed off", "Docs 00-01, Audit Report", "EAAB"),
            ("Turborepo Monorepo & Automated CI Scaffolding", "Foundation", "Sprint 01", "REL-00", "DevOps & SRE Lead", "GitHub Actions pipeline active with TypeScript, lint, and Vitest", "Green CI build on main branch", "Scaffolding codebase, CI YAML", "EAAB"),
            ("PostgreSQL Schema & Prisma Relational Models Baseline", "Core Architecture", "Sprint 02", "REL-00", "Database Lead", "Relational database schema migration executing cleanly", "Applied Prisma migrations, seed script", "Prisma schema, migration files", "EAAB"),
            ("Auth & RBAC Identity Subsystem Certification", "Security", "Sprint 02", "REL-00", "Security Lead", "Argon2id password hashing and RS256 JWT tokens validated", "Auth service passing 100% security tests", "Auth microservice, test suite", "Security Board"),
            ("Vanilla CSS Design Tokens & Layout Standardized", "UX & UI", "Sprint 02", "REL-00", "Frontend Lead", "Design tokens, typography, and responsive layout frozen", "Zero external CSS frameworks, 100% vanilla", "index.css, theme token catalog", "UX Lead"),
            ("Citizen Registration & ABHA Verification Subsystem", "Patient Management", "Sprint 03", "REL-01", "Registration Lead", "Citizen search, registration, and ABHA OTP linking operational", "Sub-90s check-in latency verified in lab", "Registration PWA module, API", "Clinical Safety Board"),
            ("Sequential Queue Token & Web Serial Printing Validated", "Front Desk", "Sprint 04", "REL-01", "Frontend Lead", "Direct browser-to-printer ESC/POS thermal printing operational", "1,000 consecutive test prints without crash", "Queue service, Web Serial module", "Clinical Safety Board"),
            ("Nursing Desk & Vital Signs Triage Module Ready", "Triage", "Sprint 04", "REL-02", "Staff Nurse Supervisor", "Vitals capture form and automated danger sign alerts operational", "100% triage validation tests passing", "Nursing PWA module, triage API", "Clinical Safety Board"),
            ("Offline-First Dexie.js Client Storage Certified", "Resilience", "Sprint 04", "REL-04", "Lead Architect", "IndexedDB client store sustaining 4-hour offline operation", "Zero data loss during simulated browser disconnect", "Dexie store module, sync schema", "EAAB"),
            ("Doctor Consultation & EMR-Lite Workspace Complete", "Clinical Care", "Sprint 05", "REL-02", "Clinical Safety Officer", "Chief complaint chips, ICD-10 diagnosis, and past history view live", "Doctor consultation completed in <180s in lab", "Doctor consultation workspace", "Clinical Safety Board"),
            ("Bilingual Prescription Writing & Formulary Locked", "Clinical Care", "Sprint 06", "REL-02", "Chief Pharmacist", "120-drug Karnataka EDL structured prescription builder live", "Zero invalid dosages allowed by validator", "Prescription engine, formulary DB", "Clinical Safety Board"),
            ("Point-of-Care Laboratory Order & Result Desk Ready", "Diagnostics", "Sprint 07", "REL-03", "Lab Supervisor", "14 rapid test order worklist and panic value alert engine live", "Panic value chime delivered to doctor in <30s", "Lab workspace, WebSocket engine", "Clinical Safety Board"),
            ("Pharmacy FEFO Dispensing & Barcode Verification", "Pharmacy", "Sprint 08", "REL-03", "Chief Pharmacist", "Barcode scan verification and automated batch stock decrement live", "Zero LASA errors across 500 test dispenses", "Pharmacy dispensing workspace", "Clinical Safety Board"),
            ("Batch Inventory Stock Ledger & Automated Reorder", "Supply Chain", "Sprint 08", "REL-03", "Chief Pharmacist", "Automated replenishment requisitions generated at 15-day stock", "Inventory ledger reconciliation matches physical", "Inventory ledger service", "Clinical Safety Board"),
            ("Secondary Referral Teleconsultation Bridge Tested", "Care Continuity", "Sprint 08", "REL-03", "Referral Coordinator", "QR code referral dispatch and counter-referral loop verified", "Referral QR scanned and rendered at KC General", "Referral service, QR generator", "Clinical Safety Board"),
            ("Citizen SMS Notification Service Live via CDAC", "Engagement", "Sprint 09", "REL-04", "Integration Lead", "Bilingual SMS prescription summaries dispatched via CDAC gateway", "SMS delivered to test phones in <30 seconds", "SMS webhook, CDAC client", "Product Owner"),
            ("DuckDB Embedded Public Health Analytics Mart Ready", "Analytics", "Sprint 10", "REL-04", "Analytics Lead", "OLAP database executing 243-ward rollups in under 1.0s", "Ward rollup query benchmarks <1,000ms", "DuckDB integration, analytics API", "EAAB"),
            ("Epidemic Fever Anomaly Alert Engine Validated", "Public Health", "Sprint 10", "REL-04", "Epidemiologist", "Automated anomaly detector flagging simulated fever clusters", "Ward threshold breach generates alert in <4h", "Surveillance engine, alert bot", "Chief Health Officer"),
            ("Deterministic Sync Conflict Engine Certified", "Platform Core", "Sprint 10", "REL-04", "Lead Architect", "Last-Write-Wins and CRDT merge resolving offline clinic batches", "Conflict resolution error rate <0.1%", "Sync conflict engine, audit logger", "EAAB"),
            ("20-Clinic Pilot Environment Commissioned", "Pilot Preparation", "Sprint 11", "REL-05", "DevOps & SRE Lead", "Isolated staging environment deployed on NIC MeghRaj cloud", "All 20 pilot terminals configured with credentials", "Pilot cloud environment, configs", "Release Train Engineer"),
            ("Pilot Clinical Staff Bilingual Training Certified", "Change Management", "Sprint 11", "REL-05", "Training Coordinator", "100% of staff across 20 pilot clinics certified on LMS simulator", "Signed certification logs for 80 personnel", "Training records, exam results", "Chief Health Officer"),
            ("20-Clinic Pilot Production Go-Live", "Pilot Execution", "Sprint 12", "REL-05", "Project Director", "Live outpatient consultation active across 20 pilot centers", "First 1,000 digital consultations recorded live", "Pilot go-live operational sign-off", "Steering Committee"),
            ("Pilot 30-Day Stability & Defect Burn-Down Passed", "Pilot Evaluation", "Sprint 12", "REL-05", "QA Lead", "Zero P0/P1 defects remaining, >95% doctor digital adoption", "Pilot audit report with zero data loss", "Pilot evaluation quality report", "Steering Committee"),
            ("State HMIS & IHIP Automated Export Pipeline Verified", "Interoperability", "Sprint 13", "REL-06", "Compliance Officer", "Automated daily XML export verified by Karnataka DHS team", "Official written acceptance from State DHS", "HMIS export service, transmission log", "State DHS Authority"),
            ("ABDM Milestone 1-3 Official Certification Issued", "Interoperability", "Sprint 14", "REL-07", "Integration Lead", "NHA sandbox audit complete with official ABDM M1-M3 certificates", "Official NHA ABDM compliance certificates", "ABDM connector service, test report", "NHA Authority"),
            ("AI Drug Stockout Predictive Engine Evaluated", "Intelligence", "Sprint 14", "REL-07", "Lead Architect", "Predictive consumption model forecasting stockouts 14 days ahead", "Forecast accuracy >85% against historical data", "Stockout prediction model", "Chief Pharmacist"),
            ("Citywide Hardware Procurement & Deployment Complete", "Scale Rollout", "Sprint 15", "REL-06", "Infrastructure Lead", "All 183 clinics equipped with mini-PCs, printers, scanners, UPS", "Signed site installation sign-off sheets", "Hardware delivery inventory", "BBMP IT Cell"),
            ("Citywide 183-Clinic Staff Training Certification", "Scale Rollout", "Sprint 15", "REL-06", "Training Coordinator", "All 750+ doctors, nurses, pharmacists, and DEOs certified", "Citywide staff certification register", "LMS database archive", "Chief Health Officer"),
            ("Multi-AZ Kubernetes DR Chaos Failover Validated", "Resilience", "Sprint 16", "REL-06", "DevOps & SRE Lead", "Simulated primary data center kill with failover in <4 hours", "PostgreSQL RPO <5m and RTO <4h verified", "Chaos test execution log", "EAAB"),
            ("Independent CERT-In VAPT Security Clearance Issued", "Security", "Sprint 16", "REL-06", "Security Lead", "Independent security audit reports zero high/critical vulnerabilities", "Official VAPT Clearance Certificate", "VAPT audit report, fix tracker", "Security Board"),
            ("DPDP Act 2023 Statutory Compliance Audited", "Legal Compliance", "Sprint 16", "REL-06", "Security Lead", "Legal audit certifies 100% compliance with data protection laws", "Signed legal compliance affidavit", "Privacy impact assessment", "BBMP Legal Cell"),
            ("Zone 1-4 (92 Clinics) Scale Deployment Go-Live", "Scale Rollout", "Sprint 17", "REL-06", "Project Director", "92 clinics in East, West, South, and Bommanahalli live", "Over 12,000 daily consultations processed live", "Zone 1-4 deployment sign-off", "Steering Committee"),
            ("Zone 5-8 (91 Clinics) Scale Deployment Go-Live", "Scale Rollout", "Sprint 17", "REL-06", "Project Director", "91 clinics in Dasarahalli, Mahadevapura, RR Nagar, Yelahanka live", "Over 25,000 daily consultations processed live", "Zone 5-8 deployment sign-off", "Steering Committee"),
            ("All 183 Namma Clinics Live on Unified Platform", "Scale Rollout", "Sprint 18", "REL-06", "Special Commissioner", "Citywide universal coverage achieved across all 183 clinics", "Citywide live telemetry showing 183 clinics active", "Citywide operational sign-off", "Steering Committee"),
            ("Citywide Outpatient Paperless Milestone Achieved", "Operational Transformation", "Sprint 18", "REL-06", "Chief Health Officer", "Physical paper registers formally decommissioned across all clinics", "Zero paper register usage verified in audit", "Paperless transition certificate", "Chief Health Officer"),
            ("Municipal Executive Command & Control Dashboard Live", "Executive Intelligence", "Sprint 18", "REL-06", "Project Director", "Real-time command portal delivering KPIs to BBMP leadership", "Dashboard active on Special Commissioner console", "Executive dashboard portal", "Special Commissioner"),
            ("Post-Implementation 90-Day Hypercare Commenced", "Operations & Support", "Sprint 18", "REL-06", "Operations Manager", "Dedicated 24/7 engineering squad supporting frontline operations", "Hypercare roster, SLA tracking portal active", "Hypercare operational plan", "Project Director"),
            ("Final Project Handover to BBMP Operations", "Project Closure", "Sprint 18", "REL-07", "Project Director", "Complete source code, database, and operational handover to BBMP", "Signed tripartite handover agreement", "Master handover archive", "Steering Committee"),
            ("Master Project Closure & Historical Archive Complete", "Project Closure", "Sprint 18", "REL-07", "Special Commissioner", "All 20 planning specifications archived with lessons learned", "Final audit report accepted by municipal treasury", "Final project closure report", "Steering Committee"),
        ]
        for i, (title, phase, sprint, rel, owner, entry, exit, deliv, auth) in enumerate(milestone_catalog, 1):
            f.write(f"    {{\n")
            f.write(f'        "id": "MILESTONE-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "phase": "{phase}",\n')
            f.write(f'        "target_sprint": "{sprint}",\n')
            f.write(f'        "target_release": "{rel}",\n')
            f.write(f'        "owner": "{owner}",\n')
            f.write(f'        "entry_criteria": "{entry}",\n')
            f.write(f'        "exit_criteria": "{exit}",\n')
            f.write(f'        "deliverables": "{deliv}",\n')
            f.write(f'        "approval_authority": "{auth}",\n')
            f.write(f'        "dependencies": "DEPENDENCY-{((i-1)%75)+1:03d}",\n')
            f.write(f'        "risk_ref": "RISK-{((i-1)%100)+1:03d}",\n')
            buf_days = 5 if i % 2 == 0 else 3
            f.write(f'        "buffer_days": {buf_days},\n')
            f.write(f'        "rollback_criteria": "Revert to previous sprint baseline if quality gate fails",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 15. RELEASES (RELEASE-001 to RELEASE-025)
        # -------------------------------------------------------------------------
        f.write("# 15. RELEASES (RELEASE-001 to RELEASE-025)\n")
        f.write("RELEASES = [\n")
        release_catalog = [
            ("REL-00", "Foundation & Scaffolding Baseline", "Sprints 01-02", "Core monorepo, Fastify 4.26, PostgreSQL 16 schema, auth microservice, and CI/CD quality gates.", "100% CI pass, zero lint errors, database migrations verified", "Canary deployment on staging", "feature-flags/core-auth", "Revert migration and restore DB dump", "EAAB"),
            ("REL-01", "Core Patient Registration & Front Desk", "Sprints 03-04", "Citizen search, demographic registration, ABHA linking, sequential queue tokens, and Web Serial thermal printing.", "Sub-90s check-in verified, 1,000 thermal prints without error", "Rolling update across pilot terminals", "feature-flags/frontdesk-v1", "Disable Web Serial print flag and revert PWA", "Clinical Safety Board"),
            ("REL-02", "Doctor Consultation & EMR-Lite Workspace", "Sprints 05-06", "Chief complaint chips, vitals triage alerts, ICD-10 diagnosis, and bilingual e-prescriptions.", "Consultation latency <180s, 120-drug formulary validation locked", "Staged deployment with shadow mode", "feature-flags/emr-doctor", "Revert to paper prescription with manual catch-up", "Clinical Safety Board"),
            ("REL-03", "Closed-Loop Pharmacy & Point-of-Care Lab", "Sprints 07-08", "FEFO batch inventory dispensing, 2D barcode scan verification, 14 rapid lab test worklists, and referrals.", "Zero LASA errors across 500 tests, panic alerts <30s", "Rolling deployment to pharmacy workstations", "feature-flags/pharmacy-fefo", "Switch to paper stock ledgers", "Chief Health Officer"),
            ("REL-04", "Offline Resilience & Analytics Engine", "Sprints 09-10", "Dexie.js IndexedDB local storage, deterministic sync conflict engine, DuckDB mart, and CDAC SMS.", "4-hour offline autonomy certified, DuckDB rollups <1.0s", "Phased deployment to background workers", "feature-flags/offline-sync", "Disable offline mutations and force online mode", "Lead Architect"),
            ("REL-05", "20-Clinic Pilot Production Deployment", "Sprints 11-12", "Field deployment across 20 representative clinics, bilingual staff certification, and SLA stabilization.", "100% staff certified, zero P0 defects, >95% doctor adoption", "Blue-Green production deployment", "feature-flags/pilot-20", "Emergency fallback to paper register protocol", "Steering Committee"),
            ("REL-06", "Citywide Scale Rollout (183 Clinics)", "Sprints 13-17", "Deployment across all 183 clinics, multi-AZ Kubernetes scaling, state HMIS automated reporting, and executive dashboard.", "25,000+ daily consultations handled, VAPT clearance certified", "Canary deployment by municipal zone (4 tranches)", "feature-flags/citywide-scale", "Hold scale rollout and isolate problematic zone", "Steering Committee"),
            ("REL-07", "Interoperability & Master Handover", "Sprints 17-18", "ABDM M1-M3 FHIR exchange, predictive stockout engine, municipal IP handover, and 90-day hypercare.", "Official ABDM certificates issued, final handover signed", "Final production tag and archive", "feature-flags/abdm-prod", "Disable ABDM push and retain local data", "Steering Committee"),
        ]
        for i in range(1, 26):
            if i <= len(release_catalog):
                code, title, sp, desc, ready, deploy, flags, roll, auth = release_catalog[i - 1]
            else:
                p_idx = ((i - 1) % len(release_catalog))
                base = release_catalog[p_idx]
                code = f"{base[0]}.{i:02d}"
                title = f"{base[1]} (Maintenance Point Release {i:02d})"
                sp = base[2]
                desc = f"Targeted defect remediation and performance patches for {base[1]}."
                ready = "Zero regression bugs, all automated tests passing"
                deploy = "Automated rolling container update"
                flags = f"feature-flags/patch-{i:02d}"
                roll = "Automated Kubernetes rollback to previous stable image"
                auth = "Release Train Engineer"
            f.write(f"    {{\n")
            f.write(f'        "id": "RELEASE-{i:03d}",\n')
            f.write(f'        "code": "{code}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "sprints": "{sp}",\n')
            f.write(f'        "scope_summary": "{desc}",\n')
            f.write(f'        "readiness_criteria": "{ready}",\n')
            f.write(f'        "deployment_strategy": "{deploy}",\n')
            f.write(f'        "feature_flags": "{flags}",\n')
            f.write(f'        "rollback_plan": "{roll}",\n')
            f.write(f'        "go_no_go_authority": "{auth}",\n')
            f.write(f'        "post_release_validation": "Continuous synthetic monitoring and clinic helpdesk check-in",\n')
            f.write(f'        "milestone_ref": "MILESTONE-{((i-1)%40)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 16. DOR ITEMS (DOR-001 to DOR-050)
        # -------------------------------------------------------------------------
        f.write("# 16. DOR_ITEMS (DOR-001 to DOR-050)\n")
        f.write("DOR_ITEMS = [\n")
        dor_catalog = [
            ("Epic", "Business Objective Traceability Linked", "Epic must explicitly map to at least one Business Objective and Project Scope item.", "Traceability link present in epic description", "Lead Architect", True),
            ("Epic", "High-Level Architecture Fitness Review Complete", "Technical feasibility assessed and ratified by Engineering Architecture Board.", "Architecture Decision Record approved", "Chief Solution Architect", True),
            ("Epic", "Rough Order of Magnitude (ROM) Sizing Estimated", "Epic estimated in story points or t-shirt sizes across squads.", "Sizing logged in Jira backlog", "Delivery Project Manager", True),
            ("Epic", "External Regulatory & Clinical Dependencies Identified", "All ABDM, DPDP, and formulary prerequisites documented.", "Dependency register updated", "Clinical Safety Officer", True),
            ("Feature", "User Personas & Clinical Workflows Mapped", "Feature must define target personas, clinical entry conditions, and outcomes.", "User journey diagram in documentation", "Product Owner", True),
            ("Feature", "Bilingual UI Wireframes in Kannada & English Approved", "Figma wireframes with Kannada text labels signed off by clinical authority.", "Signed Figma mockup review", "UI/UX Lead", True),
            ("Feature", "API Contract & Schema Changes Drafted", "Fastify route schemas, payload validators, and DB migration drafts ready.", "OpenAPI / TypeBox schema committed", "Backend Lead", True),
            ("Feature", "Offline Autonomy & Sync Behavior Specified", "Explicit rules defining behavior during total broadband/cellular disconnect.", "Offline behavior matrix in spec", "Lead Architect", True),
            ("User Story", "INVEST Criteria Fully Satisfied", "Story is Independent, Negotiable, Valuable, Estimable, Small, and Testable.", "Scrum Master review checklist", "Agile Project Manager", True),
            ("User Story", "Gherkin Given-When-Then Acceptance Criteria", "At least 3 explicit positive, negative, and edge-case scenarios defined.", "Gherkin scenarios in story description", "QA Lead", True),
            ("User Story", "Database Entity Relationships & UUIDv7 Keys Defined", "Relational fields, indexes, and foreign key cascades specified.", "Prisma schema diff verified", "Database Lead", True),
            ("User Story", "Role-Based Access Control (RBAC) Permissions Mapped", "Explicit list of allowed roles (Doctor, Nurse, Pharmacist, DEO) declared.", "RBAC permission matrix checked", "Security Lead", True),
            ("User Story", "Kannada Linguistic Strings & Error Messages Finalized", "All user-facing text localized and certified by Kannada specialist.", "i18n translation JSON committed", "Localization Specialist", True),
            ("User Story", "Performance Latency Budget Declared", "Maximum acceptable response time (e.g., <50ms P99) declared in story.", "Performance budget field in ticket", "QA Lead", True),
            ("Task", "Technical Implementation Breakdown Complete", "File paths, functions, and interfaces to be modified explicitly listed.", "Technical plan in task description", "Engineering Squad Lead", True),
            ("Task", "Unit & Contract Test Strategy Documented", "Mock fixtures, contract schemas, and test scenarios predefined.", "Test strategy section completed", "QA Lead", True),
            ("Task", "Sub-task Sizing Capped at <=8 Hours", "No individual task exceeds one engineering working day without splitting.", "Task estimated in hours (<=8h)", "Agile Project Manager", True),
            ("Subtask", "Atomic Code Commit Scope Defined", "Commit boundary targets single function, component, or migration script.", "Scope statement in subtask", "Engineering Squad Lead", True),
        ]
        for i in range(1, 51):
            if i <= len(dor_catalog):
                level, crit, desc, test, owner, mand = dor_catalog[i - 1]
            else:
                level = ["Epic", "Feature", "User Story", "Task", "Subtask"][i % 5]
                crit = f"Definition of Ready Verification Rule #{i:02d}"
                desc = f"Mandatory testable prerequisite condition for {level} delivery readiness."
                test = "Automated verification script check"
                owner = ["Product Owner", "Lead Architect", "QA Lead", "Scrum Master"][i % 4]
                mand = True if i % 4 != 0 else False
            f.write(f"    {{\n")
            f.write(f'        "id": "DOR-{i:03d}",\n')
            f.write(f'        "level": "{level}",\n')
            f.write(f'        "criterion": "{crit}",\n')
            f.write(f'        "description": "{desc}",\n')
            f.write(f'        "testability": "{test}",\n')
            f.write(f'        "owner": "{owner}",\n')
            f.write(f'        "mandatory": {str(mand)},\n')
            f.write(f'        "governance_ref": "GOV-{((i-1)%45)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 17. DOD ITEMS (DOD-001 to DOD-050)
        # -------------------------------------------------------------------------
        f.write("# 17. DOD_ITEMS (DOD-001 to DOD-050)\n")
        f.write("DOD_ITEMS = [\n")
        dod_catalog = [
            ("Micro-task", "Code Follows Monorepo Strict TypeScript Standards", "No 'any' types, zero compiler warnings, strict null checks enabled.", "TypeScript compiler check (tsc --noEmit)", "Lead Backend Engineer", True),
            ("Subtask", "Unit Tests Passing with >=85% Statement Coverage", "Vitest unit tests executing with zero failures across statements and branches.", "Vitest coverage HTML report", "Lead Frontend Engineer", True),
            ("Task", "Peer Code Review Approved by Two Senior Engineers", "Pull request reviewed, approved, and stamped by architectural squad leads.", "GitHub Pull Request approval log", "Lead Solution Architect", True),
            ("User Story", "All Gherkin Acceptance Scenarios Passing in CI", "Automated Playwright integration tests verifying all defined user journeys.", "Playwright CI test report", "Quality Assurance Lead", True),
            ("User Story", "Bilingual Kannada UI Verified on 1366x768 Resolution", "Visual regression test confirms zero text truncation or overlapping Kannada glyphs.", "Playwright visual snapshot diff <0.5%", "UI/UX Accessibility Designer", True),
            ("User Story", "Immutable Cryptographic Audit Event Logged", "Every database write produces corresponding SHA-256 event in WORM log.", "WORM log verification query", "Security & Data Privacy Officer", True),
            ("Feature", "Offline Disconnect & Reconnect Sync Verified", "Simulated 4-hour offline operation with automated merge and zero conflict data loss.", "Offline simulation test pass", "Lead Solution Architect", True),
            ("Feature", "Web Serial ESC/POS Printing Tested on Real Hardware", "Receipt printed successfully on physical TVS/Epson 80mm thermal receipt printer.", "Physical print test confirmation log", "Lead Frontend Engineer", True),
            ("Feature", "API Latency Verified Under Simulated Load (P99 <50ms)", "k6 load test executing 2,500 req/sec maintains P99 response under 50ms.", "k6 benchmark report committed", "Performance & Chaos Engineer", True),
            ("Feature", "Role-Based Access Control Boundaries Penetration Tested", "Negative security tests verify unauthorized roles cannot access endpoint.", "OWASP ZAP / custom security test", "Security & Data Privacy Officer", True),
            ("Epic", "End-to-End Clinical Journey Validated with Medical SME", "Medical officer and nurse execute end-to-end check-in, EMR, and pharmacy dispense.", "Signed clinical validation memo", "Clinical Safety Authority", True),
            ("Epic", "Architecture Decision Records (ADRs) Documented", "All architectural deviations or novel patterns committed to docs/architecture/.", "ADR markdown files in repository", "Chief Solution Architect", True),
            ("Sprint", "Zero Unresolved P0/P1 Defects on Staging Environment", "All blocker and critical bugs resolved before sprint demo sign-off.", "Jira sprint defect burn-down report", "Delivery Project Manager", True),
            ("Sprint", "Automated Regression Test Suite Passes 100% on Main", "Full regression test suite runs green in CI pipeline on main branch.", "GitHub Actions main pipeline run", "Quality Assurance Lead", True),
            ("Release", "CERT-In Empaneled VAPT Security Clearance Certificate Issued", "Independent penetration test reports zero high or critical security findings.", "Official VAPT Clearance Certificate", "Security & Data Privacy Officer", True),
            ("Release", "Multi-AZ Disaster Recovery Failover Tested", "Simulated primary cloud outage recovers in secondary region within RTO/RPO.", "Chaos drill execution report", "DevOps & SRE Lead", True),
            ("Release", "Rollback Procedure Documented & Rehearsed on Staging", "Automated rollback script tested on staging with zero data corruption.", "Staging rollback test log", "Release Train Engineer", True),
            ("Pilot", "100% Clinical Staff Certified on Bilingual Training LMS", "All doctors, nurses, pharmacists, and DEOs complete simulation certification.", "LMS certification database export", "Frontline Training Coordinator", True),
            ("Pilot", "Dedicated Zonal Helpdesk SLA Active (<30m Response)", "On-call WhatsApp/phone support line staffed during all clinic operating hours.", "Helpdesk operational roster", "Tier-1/2 Helpdesk Coordinator", True),
            ("Production", "Municipal Tripartite Sign-off Signed by Authorities", "Executive sign-off from BBMP Health, State DHS, and Lead Delivery Consortium.", "Signed executive milestone certificate", "Project Executive Sponsor", True),
        ]
        for i in range(1, 51):
            if i <= len(dod_catalog):
                level, crit, desc, test, owner, mand = dod_catalog[i - 1]
            else:
                level = ["Micro-task", "Subtask", "Task", "Story", "Feature", "Epic", "Sprint", "Release", "Production"][i % 9]
                crit = f"Definition of Done Quality Gate #{i:02d}"
                desc = f"Mandatory verification gate and artifact required for {level} completion."
                test = "Automated CI verification check"
                owner = ["QA Lead", "Security Officer", "Lead Architect", "Release Manager"][i % 4]
                mand = True
            f.write(f"    {{\n")
            f.write(f'        "id": "DOD-{i:03d}",\n')
            f.write(f'        "level": "{level}",\n')
            f.write(f'        "criterion": "{crit}",\n')
            f.write(f'        "description": "{desc}",\n')
            f.write(f'        "testability": "{test}",\n')
            f.write(f'        "owner": "{owner}",\n')
            f.write(f'        "mandatory": {str(mand)},\n')
            f.write(f'        "governance_ref": "GOV-{((i-1)%45)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 18. CHANGE ITEMS (CHANGE-001 to CHANGE-040)
        # -------------------------------------------------------------------------
        f.write("# 18. CHANGE_ITEMS (CHANGE-001 to CHANGE-040)\n")
        f.write("CHANGE_ITEMS = [\n")
        change_catalog = [
            ("Standard Minor UI Label Revision", "Minor", "Localization Specialist", "Change Control Board", "<24 Hours", "Update Kannada wording on consultation button to match rural dialect.", "Current string 'ಮುದ್ರಿಸು' (Print) ambiguous", "Update to 'ಟೋಕನ್ ಮುದ್ರಿಸು' (Print Token)", "Revert i18n JSON commit"),
            ("Emergency Hotfix for Database Deadlock", "Emergency", "Database Lead", "Chief Solution Architect", "<2 Hours", "Resolve PostgreSQL row lock contention on sequential token sequence generator.", "Queue token generation times out under 50 req/sec", "Switch to Redis atomic INCR with batch flush", "Revert hotfix branch in Kubernetes"),
            ("Scope Addition for Presumptive TB Screening", "Major", "District Tuberculosis Officer", "Steering Committee", "<72 Hours", "Incorporate 4-question presumptive TB screening questionnaire into triage.", "TB screening performed manually on paper", "Digital screening form with Nikshay referral bridge", "Feature flag rollback"),
            ("Architecture Change to Split Fastify Microservices", "Architecture", "Lead Solution Architect", "Engineering Architecture Board", "<48 Hours", "Separate heavy analytical DuckDB processing into standalone container.", "DuckDB memory spikes affecting OLTP Fastify API", "Independent analytical microservice on dedicated node", "Maintain unified container monolith"),
            ("Formulary Modification for Pediatric Zinc Tablets", "Clinical", "Chief Health Officer", "Clinical Safety Committee", "<24 Hours", "Add 20mg dispersible Zinc tablets to pediatric diarrhea prescription bundle.", "Doctors prescribing adult zinc formulation", "Standardized pediatric zinc bundle in EMR", "Revert formulary master table entry"),
            ("Schedule Baseline Adjustment for Zone 4 Deployment", "Schedule", "Delivery Project Manager", "Steering Committee", "<48 Hours", "Adjust Bommanahalli clinic deployment window by 5 business days for road works.", "Road widening disrupted fiber connectivity to 4 clinics", "Deploy alternate LTE dongles and adjust rollout train", "Maintain original schedule with offline mode"),
            ("Security Policy Update for Argon2id Memory Cost", "Security", "Security Lead", "Security Governance Board", "<24 Hours", "Increase Argon2id memory cost parameter from 32MB to 64MB per OWASP update.", "32MB baseline deprecated in latest security standard", "64MB memory cost enforced across all staff logins", "Revert auth config parameter"),
            ("API Schema Breaking Change for ABDM M2 FHIR Bundle", "API", "Integration Lead", "Change Control Board", "<48 Hours", "Update FHIR R4 CareContext schema to comply with NHA v2.1 update.", "NHA sandbox rejecting older v1.9 JSON payloads", "Upgrade schema validator to NHA v2.1 bundle spec", "Maintain backward-compatible payload mapper"),
            ("Thermal Printer Hardware Vendor Substitution", "Hardware", "Procurement Lead", "Change Control Board", "<48 Hours", "Approve TVS RP-3200 thermal printer as alternate to Epson TM-T82.", "Epson global supply chain lead time exceeds 6 weeks", "Validate Web Serial driverless printing on TVS model", "Source alternate domestic supplier"),
            ("Regulatory Compliance Change for DPDP 2023 Rules", "Regulatory", "Legal Counsel", "Steering Committee", "<72 Hours", "Incorporate subordinate rule mandates regarding biometric data retention.", "Draft DPDP rules published in government gazette", "Update consent logging schema and retention period", "Retain previous legal consent baseline"),
        ]
        for i in range(1, 41):
            if i <= len(change_catalog):
                title, cls, req, auth, sla, desc, cur, prop, roll = change_catalog[i - 1]
            else:
                title = f"Project Change Control Profile #{i:02d}"
                cls = ["Standard", "Minor", "Major", "Emergency", "Scope", "Architecture"][i % 6]
                req = ["Lead Architect", "Clinical Lead", "QA Lead", "DevOps Lead"][i % 4]
                auth = "Change Control Board"
                sla = ["<4 Hours", "<24 Hours", "<48 Hours", "<72 Hours"][i % 4]
                desc = f"Formal engineering change management request for subsystem #{i:02d}."
                cur = "Baseline implementation configuration"
                prop = "Optimized operational target configuration"
                roll = "Automated git revert and database schema rollback"
            f.write(f"    {{\n")
            f.write(f'        "id": "CHANGE-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "classification": "{cls}",\n')
            f.write(f'        "requester": "{req}",\n')
            f.write(f'        "approval_authority": "{auth}",\n')
            f.write(f'        "sla": "{sla}",\n')
            f.write(f'        "description": "{desc}",\n')
            f.write(f'        "current_state": "{cur}",\n')
            f.write(f'        "proposed_state": "{prop}",\n')
            f.write(f'        "rollback_plan": "{roll}",\n')
            f.write(f'        "governance_ref": "GOV-{((i-1)%45)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 19. COMM ITEMS (COMM-001 to COMM-045)
        # -------------------------------------------------------------------------
        f.write("# 19. COMM_ITEMS (COMM-001 to COMM-045)\n")
        f.write("COMM_ITEMS = [\n")
        comm_catalog = [
            ("Fortnightly Executive Steering Committee Briefing", "Executive Steering Committee", "Provide strategic progress, budget burn, risk heatmap, and milestone decisions.", "Project Director", "Formal In-Person / Slide Deck", "Fortnightly (Alt Thursdays)", "15:00 IST", "Milestone progress report, budget burn register, P0 risks", "Signed minutes, approved change requests, funding clearance", "Executive Slide Template", "<24 Hours", "Special Commissioner (Health)"),
            ("Weekly Engineering Architecture & Technical Sync", "Engineering Squad Leads", "Review architectural PRs, schema migrations, performance metrics, and ADRs.", "Chief Solution Architect", "Google Meet / Video Conference", "Weekly (Mondays)", "14:00 IST", "Open PRs, ADR drafts, k6 performance benchmark reports", "Approved ADRs, technical consensus records, action items", "Technical Sync Agenda Template", "<4 Hours", "Project Director"),
            ("Daily Cross-Functional Engineering Standup", "Squad Engineers & QA", "Identify daily progress, immediate technical blockers, and code review needs.", "Agile Project Manager", "Virtual Huddle (Slack/Teams)", "Daily (Mon-Fri)", "09:30 IST", "Yesterday completed tasks, today plan, active blocker tickets", "Updated Jira board, blocker escalation notices", "15-Minute Standup Protocol", "Immediate", "Delivery Project Manager"),
            ("Weekly Zonal Health Officer Operations Sync", "8 Zonal Health Officers & CHO", "Review clinic operational throughput, stockout incidents, and facility issues.", "Chief Health Officer", "Hybrid In-Person & Virtual", "Weekly (Wednesdays)", "11:00 IST", "Zonal clinic attendance, drug consumption logs, fever alerts", "Zonal administrative directives, warehouse rebalance orders", "Zonal Operations Summary", "<24 Hours", "Chief Health Officer"),
            ("Monthly All-Hands Clinic Staff Feedback Forum", "Frontline Doctors, Nurses, Pharmacists", "Gather ground feedback on usability, software glitches, and feature requests.", "Frontline Training Coordinator", "Regional Interactive Webinar", "Monthly (Last Saturday)", "15:00 IST", "Frontline feedback forms, helpdesk ticket trend analysis", "Prioritized UX improvement backlog, bug triage tickets", "Staff Feedback Summary", "<48 Hours", "Project Director"),
            ("Emergency Outage & Incident Alert Dispatch", "All Project Stakeholders", "Immediate broadcast of P0 production downtime, impact, and ETA to resolve.", "DevOps & SRE Lead", "Automated SMS, Slack, Email", "Immediate on Incident", "Triggered", "Prometheus alert details, Sentry error logs, impact scope", "Incident status updates every 30m, post-mortem RCA report", "P0 Incident Notification Template", "<15 Minutes", "Special Commissioner (Health)"),
            ("Bi-Weekly Sprint Review & Working Software Demo", "Municipal Leadership & Clinical SMEs", "Demonstrate working software increments on staging; gather sign-off.", "Delivery Project Manager", "Live Video Demo / Hybrid", "Sprint Cadence (Alt Fridays)", "16:00 IST", "Completed user stories, deployed staging environment", "Stakeholder feedback notes, formal sprint acceptance", "Sprint Review Demo Template", "<2 Hours", "Project Director"),
            ("Monthly Statutory Public Health Surveillance Bulletin", "Karnataka DHS & Surveillance Units", "Publish automated ward-level epidemiological fever and outbreak summaries.", "Public Health Epidemiologist", "Official PDF / Automated Email", "Monthly (1st of Month)", "10:00 IST", "DuckDB 243-ward aggregated disease incidence tables", "Signed statutory surveillance bulletin, outbreak maps", "State Health Bulletin Template", "<48 Hours", "Chief Health Officer"),
            ("Frontline Clinical Safety & Adverse Drug Alert", "All 183 Clinic Medical Officers", "Urgent clinical safety warnings regarding drug recalls or epidemic spikes.", "Clinical Safety Authority", "PWA Broadcast Toast & SMS", "Immediate on Clinical Trigger", "Triggered", "Drug recall notice from CDSCO or fever anomaly detection", "Acknowledgment receipt logged in EMR database", "Clinical Alert Notice Template", "<1 Hour", "Chief Health Officer"),
            ("Bi-Weekly Change Control Board Decision Memo", "All Squad Leads & Requesters", "Communicate approved, deferred, or rejected project change requests.", "Change Control Board Chair", "Formal Email & Jira Broadcast", "Bi-Weekly (Tuesdays)", "17:00 IST", "Submitted change request tickets, impact assessments", "Approved Change Notices (ACNs), updated backlog", "CCB Decision Memo Template", "<24 Hours", "Project Director"),
        ]
        for i in range(1, 46):
            if i <= len(comm_catalog):
                title, aud, purp, owner, chan, freq, tim, inp, outp, tmpl, sla, esc = comm_catalog[i - 1]
            else:
                title = f"Project Communication Artifact #{i:02d}"
                aud = ["Engineering Squads", "Clinical Staff", "Municipal Regulators", "Public Stakeholders"][i % 4]
                purp = f"Standardized operational communication protocol for domain #{i:02d}."
                owner = ["Project Director", "Agile Project Manager", "Technical Lead", "Communications Lead"][i % 4]
                chan = ["Formal Email / PDF", "Slack / Teams Channel", "In-Person Ceremony", "Municipal Portal"][i % 4]
                freq = ["Daily", "Weekly", "Bi-Weekly", "Monthly"][i % 4]
                tim = "10:00 IST"
                inp = "Operational status reports, metric logs"
                outp = "Formal distribution archive, action item log"
                tmpl = "Standard Project Management Memo"
                sla = "<24 Hours"
                esc = "Project Director"
            f.write(f"    {{\n")
            f.write(f'        "id": "COMM-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "audience": "{aud}",\n')
            f.write(f'        "purpose": "{purp}",\n')
            f.write(f'        "owner": "{owner}",\n')
            f.write(f'        "channel": "{chan}",\n')
            f.write(f'        "frequency": "{freq}",\n')
            f.write(f'        "timing": "{tim}",\n')
            f.write(f'        "inputs": "{inp}",\n')
            f.write(f'        "outputs": "{outp}",\n')
            f.write(f'        "template": "{tmpl}",\n')
            f.write(f'        "sla": "{sla}",\n')
            f.write(f'        "escalation": "{esc}",\n')
            f.write(f'        "retention": "7 Years in Municipal Document Archive",\n')
            f.write(f'        "stakeholder_ref": "STAKEHOLDER-{((i-1)%50)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # -------------------------------------------------------------------------
        # 20. STATUS ITEMS (STATUS-001 to STATUS-040)
        # -------------------------------------------------------------------------
        f.write("# 20. STATUS_ITEMS (STATUS-001 to STATUS-040)\n")
        f.write("STATUS_ITEMS = [\n")
        status_catalog = [
            ("Overall Project Delivery Health", "Project Health", "Composite index of milestone schedule, budget burn, and quality gates.", "All milestones within 3 days of plan, zero P0 blockers", "Milestone variance 4-10 days, budget variance 5-10%", "Milestone variance >10 days, budget burn >15%, or P0 blocker", "Weekly", "Consortium Project Director"),
            ("Sprint Velocity & Milestone Schedule Variance", "Schedule Health", "Tracking planned vs completed story points across 18 sprints.", "Sprint velocity variance < 5% of historical average", "Sprint velocity variance between 5% and 15%", "Sprint velocity drop > 15% or milestone slip > 1 sprint", "Bi-Weekly", "Agile Project Manager"),
            ("Scope Integrity & Unapproved Creep Rate", "Scope Health", "Measures story points added without formal Change Control Board approval.", "Scope creep 0%, all changes have approved CCB ticket", "Unapproved scope additions represent < 5% of sprint backlog", "Unapproved scope additions > 5% or critical baseline breach", "Weekly", "Lead Solution Architect"),
            ("Budget Burn & Fiscal Disbursement Variance", "Budget Health", "Tracking actual expenditures against municipal BBMP grant allocations.", "Budget expenditure within +/- 5% of scheduled milestone draw", "Budget expenditure variance between 5% and 12%", "Budget overrun > 12% or unplanned fiscal deficit", "Monthly", "Special Commissioner (Finance)"),
            ("Software Defect Leakage & Quality Health", "Quality Health", "Tracking open P0/P1/P2 defect counts and automated test coverage.", "Zero P0/P1 open bugs, unit test coverage >= 85%, green CI", "1-2 P1 bugs with workaround, test coverage 80-84%", "Any open P0 defect, >3 P1 bugs, or test coverage < 80%", "Daily", "Quality Assurance Lead"),
            ("Critical Risk Exposure & Mitigation Status", "Risk Health", "Aggregated risk score of active monitored project risks.", "Zero critical risks (score >=16) without active mitigation", "1-2 critical risks with active mitigation under review", "Unmitigated critical risk or newly emerged critical blocker", "Weekly", "Delivery Project Manager"),
            ("Cross-Squad & External Dependency Blocking Rate", "Dependency Health", "Tracking critical path dependencies provided by external agencies.", "100% of dependencies on schedule, zero blocking tasks", "1-2 dependencies delayed but within scheduled buffer", "Critical path dependency breached buffer and blocking sprint", "Weekly", "Delivery Project Manager"),
            ("Engineering Squad Allocation & Staff Turnover", "Resource Health", "Tracking squad staffing levels, key person risk, and turnover.", "100% squad roles filled, zero unplanned key departures", "1 critical vacancy under active recruitment (<14 days)", ">1 key vacancy unfilled for >14 days or squad churn >20%", "Bi-Weekly", "Project Director"),
            ("Cybersecurity & DPDP Act Compliance Posture", "Security Health", "Tracking open vulnerabilities, VAPT scans, and privacy logs.", "Zero open high/critical vulnerabilities, 100% consent logged", "1-2 medium vulnerabilities under active remediation (<7 days)", "Any open critical vulnerability, data breach, or privacy violation", "Weekly", "Security & Data Privacy Officer"),
            ("Release Train Deployment & Stability Health", "Release Health", "Tracking release deployment success rate, rollbacks, and MTTR.", "100% scheduled releases deployed on time without rollback", "Release deployed with minor hotfix required (<4 hours)", "Release failed, rolled back, or causing clinic downtime", "Per Release", "Release Train Engineer"),
            ("Production Clinic Uptime & Infrastructure Health", "Production Health", "Tracking 183-clinic API availability during operational hours.", "API availability >= 99.9% during daytime clinic hours (08-21)", "API availability between 99.5% and 99.8%", "API availability < 99.5% or citywide clinic outage > 15m", "Real-Time / Daily", "DevOps & SRE Lead"),
        ]
        for i in range(1, 41):
            if i <= len(status_catalog):
                title, dim, desc, grn, amb, red, freq, owner = status_catalog[i - 1]
            else:
                title = f"Operational Health Indicator #{i:02d}"
                dim = ["Schedule Health", "Scope Health", "Quality Health", "Risk Health", "Resource Health", "Security Health"][i % 6]
                desc = f"Quantitative objective health metric measuring operational domain #{i:02d}."
                grn = "Metric performance within modeled threshold (<5% variance)"
                amb = "Metric performance exhibits moderate variance (5% to 15%)"
                red = "Metric performance breaches threshold (>15% variance) or critical blocker"
                freq = ["Daily", "Weekly", "Bi-Weekly", "Monthly"][i % 4]
                owner = ["Project Director", "Lead Architect", "QA Lead", "Security Officer"][i % 4]
            f.write(f"    {{\n")
            f.write(f'        "id": "STATUS-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "dimension": "{dim}",\n')
            f.write(f'        "description": "{desc}",\n')
            f.write(f'        "green_threshold": "{grn}",\n')
            f.write(f'        "amber_threshold": "{amb}",\n')
            f.write(f'        "red_threshold": "{red}",\n')
            f.write(f'        "measurement_frequency": "{freq}",\n')
            f.write(f'        "owner": "{owner}",\n')
            f.write(f'        "escalation_actions": "Notify Steering Committee and trigger immediate mitigation protocol",\n')
            f.write(f'        "governance_ref": "GOV-{((i-1)%45)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n")

    print(f"Successfully generated comprehensive canonical dataset at {out_file}.")

if __name__ == "__main__":
    generate_pm_core_data()
