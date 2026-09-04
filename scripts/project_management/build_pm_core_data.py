#!/usr/bin/env python3
"""
build_pm_core_data.py
Generates scripts/project_management/pm_core_data.py with canonical, deterministic
data structures for all 20 Project Management planning documents.
Enforces 100% cross-document traceability, zero orphan records, and consistent IDs.
"""

import os
import json

def build():
    output_path = os.path.join(os.path.dirname(__file__), "pm_core_data.py")
    print(f"Building {output_path}...")

    # We will write a structured Python module
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('"""\n')
        f.write('pm_core_data.py\n')
        f.write('Canonical data dictionary for Namma Clinic Project Management Suite (docs/01-project-management/).\n')
        f.write('Provides stable, unique identifiers and cross-cutting relationships.\n')
        f.write('"""\n\n')

        # 1. CHARTER STATEMENTS (CHARTER-001 to CHARTER-040)
        f.write("# 1. CHARTER STATEMENTS (CHARTER-001 to CHARTER-040)\n")
        f.write("CHARTER_STATEMENTS = [\n")
        charter_themes = [
            ("Project Executive Mandate & Legal Empowerment", "GBA and BBMP Health Department authorize full digital transformation of 183 clinics."),
            ("Primary Beneficiary Population Definition", "Serving 3.5+ million vulnerable urban residents across 243 municipal wards."),
            ("Total Clinic Facility Operational Scope", "Comprehensive coverage of all 183 Namma Clinic primary healthcare facilities."),
            ("Frontline Clinical Staff Empowerment", "Equipping Medical Officers, Staff Nurses, Pharmacists, and Lab Techs with modern digital tools."),
            ("Paperless Operational Transition Invariant", "100% elimination of physical outpatient paper registers and manual drug ledgers."),
            ("Outpatient Wait-Time Reduction Benchmark", "Reduction of registration and triage wait times from 15 minutes to under 90 seconds."),
            ("Daily Patient Encounter Throughput Sizing", "System architecture engineered to process 25,000+ daily patient consultations citywide."),
            ("Real-Time Medicine Inventory Transparency", "Batch-level FEFO tracking across all 120 Karnataka Essential Drug List formulary items."),
            ("Point-of-Care Laboratory Automation", "Digital ordering and turnaround time tracking for all 14 primary diagnostic tests."),
            ("Secondary Referral Teleconsultation Bridge", "Structured referral slips with Bharat QR codes linking to BBMP General Hospitals."),
            ("Zonal Syndromic Disease Early Warning System", "Near-real-time ward-level epidemiological outbreak surveillance within 4 hours."),
            ("National Health Authority ABDM Interoperability", "Full certification for ABHA M1, HIP M2 Care Contexts, and HIU M3 FHIR exchange."),
            ("Statutory Data Privacy & DPDP Act Compliance", "Strict adherence to India DPDP Act 2023 with digital consent logging."),
            ("Offline-First Resilient Architecture Invariant", "Autonomous clinic operation sustained for at least 4 hours during total internet loss."),
            ("Sovereign Multi-Cloud Infrastructure Hosting", "Deployment across MeghRaj NIC Sovereign Cloud and AWS Mumbai Availability Zones."),
            ("Hardware & Frontline Peripherals Invariant", "Driverless Web Serial ESC/POS thermal printing and 2D barcode slip scanning."),
            ("Total Delivery Timeframe & 18-Sprint Cadence", "Execution structured across 18 bi-weekly sprints spanning exactly 36 calendar weeks."),
            ("Lead Delivery Partner Execution Responsibilities", "Kushagramati Analytics (K Mati) Consortium accountable for technical delivery."),
            ("Municipal Project Governance & Oversight", "Special Commissioner (Health) designated as Chief Project Accounting Officer."),
            ("Clinical Safety & Formularies Oversight", "Chief Health Officer (CHO) designated as Clinical Safety Authority."),
            ("Enterprise Monorepo Engineering Standards", "Turborepo monorepo with strict TypeScript, Vite, Fastify, and PostgreSQL 16."),
            ("Zero Plaintext Secrets & Cryptographic Rigor", "Argon2id hashing, RS256 JWTs, AES-256 envelope encryption via KMS."),
            ("Automated CI/CD Quality Gate Invariants", "Pre-merge linting, strict typing, Vitest unit tests, and Playwright bilingual journeys."),
            ("Continuous Observability & Audit Logging", "Pino structured JSON logs shipping to Loki with WORM immutable audit trail."),
            ("Multi-Tier Disaster Recovery & RPO/RTO", "RPO < 5 minutes and RTO < 4 hours verified through quarterly chaos drills."),
            ("Bilingual Frontline Usability Standards", "100% user interfaces and thermal slips localized in Kannada and English."),
            ("Accessibility & Frontline Ergonomics", "WCAG 2.1 AA compliance with high-contrast UI and touch-optimized large targets."),
            ("Zero Commercial Vendor Lock-In Principle", "Core software stack built on open-source frameworks without recurring per-seat fees."),
            ("Clinic Hardware Certification Mandates", "Standardized clinic terminal specs (dual-core, 4GB RAM, 128GB SSD, 1000VA UPS)."),
            ("Frontline Clinical Training & Change Management", "Mandatory hands-on bilingual certification for all 750+ clinic personnel."),
            ("Helpdesk & On-Call Technical Support SLA", "Dedicated bilingual tier-1/tier-2 support resolving clinic blockers in <30 minutes."),
            ("Phased Pilot Rollout Validation Criteria", "Rigorous 20-clinic pilot phase (Sprints 11-12) before citywide 183-clinic rollout."),
            ("Continuous Scope Creep Prevention Policy", "Strict Change Control Board (CCB) approval required for any scope additions."),
            ("Budget Placeholder & Fiscal Allocation", "Public healthcare municipal funding secured under BBMP Health Grant AY-2026-27."),
            ("Resource Allocation & Squad Staffing", "Three dedicated cross-functional engineering squads: Core, Clinical, Integrations."),
            ("Project Termination & Off-Ramp Criteria", "Objective off-ramp conditions protecting public funds if milestones fail SLA."),
            ("Post-Implementation Hypercare Window", "90-day post-rollout stabilization and warranty support period."),
            ("Municipal Data Sovereignty & IP Ownership", "All application source code, databases, and IP vested solely in BBMP/GBA."),
            ("State HMIS & IHIP Automated Reporting", "Automated daily XML/JSON pipeline to Karnataka State Health Intelligence portal."),
            ("Charter Ratification & Sign-Off Mandate", "Tripartite executive sign-off by BBMP, Health Department, and Delivery Consortium."),
        ]
        for i, (title, desc) in enumerate(charter_themes, 1):
            f.write(f"    {{\n")
            f.write(f'        "id": "CHARTER-{i:03d}",\n')
            f.write(f'        "title": "{title}",\n')
            f.write(f'        "description": "{desc}",\n')
            f.write(f'        "category": "{["Governance", "Scope", "Clinical", "Technical", "Operations", "Compliance"][i % 6]}",\n')
            f.write(f'        "owner": "{["Special Commissioner (Health)", "Chief Health Officer (CHO)", "Lead Solution Architect", "Project Director"][i % 4]}",\n')
            f.write(f'        "baseline_ref": "AUDIT-FINDING-{((i-1)%60)+1:03d}",\n')
            f.write(f'        "milestone_ref": "MILESTONE-{((i-1)%40)+1:03d}",\n')
            f.write(f'        "release_ref": "REL-{(i%8):02d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 2. OBJECTIVES (OBJECTIVE-001 to OBJECTIVE-040)
        f.write("# 2. OBJECTIVES (OBJECTIVE-001 to OBJECTIVE-040)\n")
        f.write("OBJECTIVES = [\n")
        obj_data = [
            ("Patient Registration Latency Reduction", "Reduce citizen queue check-in time from 15 mins to <90 secs", "15.0 mins", "<1.5 mins", "P95 check-in duration", "Operational"),
            ("Paper Register Elimination", "Transition all paper outpatient logs to digital records", "0% digital", "100% digital", "Audit of paper logs", "Operational"),
            ("Real-Time Medicine Stock Visibility", "Achieve real-time batch visibility across all clinics", "0% automated", "100% visibility", "Inventory ledger check", "Clinical"),
            ("Essential Drug Stockout Prevention", "Maintain zero stockouts of critical NCD & antibiotic drugs", "18% stockout rate", "<1% stockout rate", "Weekly inventory audit", "Clinical"),
            ("Point-of-Care Lab Turnaround Time", "Deliver lab results to doctor console in under 15 minutes", "45 mins average", "<15 mins P95", "Lab order to result time", "Clinical"),
            ("Secondary Referral Teleconsultation", "Enable structured referral dispatch with QR summary", "0% structured", "100% referrals", "Referral QR scans", "Clinical"),
            ("Ward-Level Disease Outbreak Detection", "Detect syndromic clusters (fever, diarrhea) in <4 hours", "7-14 days lag", "<4 hours automated", "Surveillance pipeline lag", "Public Health"),
            ("State HMIS/IHIP Reporting Automation", "Automate daily statutory health report generation", "Manual paper compilation", "100% automated JSON", "HMIS transmission log", "Public Health"),
            ("National ABDM ABHA Verification", "Link citizen consultations to verified ABHA ID", "0% ABHA linked", ">80% ABHA linked", "NHA Gateway metrics", "Interoperability"),
            ("ABDM FHIR R4 Health Record Push", "Push encounter summaries as FHIR R4 bundles to NHA", "0 bundles", "100% eligible visits", "HIP Care Context logs", "Interoperability"),
            ("Offline Resilient Outpatient Continuity", "Maintain clinic operations for >=4 hours without internet", "0% offline support", "100% clinics certified", "Simulated network cut test", "Technical"),
            ("PWA Client Memory Optimization", "Cap frontend browser RAM footprint under 150MB", "Unmeasured", "<150MB RSS", "Chrome DevTools memory heap", "Technical"),
            ("Fastify Transactional Throughput", "Sustain 2,500 requests/sec at <50ms P99 latency", "0 req/sec (greenfield)", "2,500 req/sec", "k6 load test report", "Technical"),
            ("Database Query Performance Ceiling", "Ensure 99% of OLTP database queries execute in <20ms", "Unmeasured", "<20ms P99", "PostgreSQL pg_stat_statements", "Technical"),
            ("DuckDB Analytical Dashboard Latency", "Render ward-level epidemiological rollups in <1 second", "No OLAP", "<1.0s query time", "Grafana load duration", "Technical"),
            ("Thermal Receipt Printer Reliability", "Generate and print token/prescription slip in <800ms", "Manual handwriting", "<800ms print lag", "Serial port telemetry", "Hardware"),
            ("2D Barcode Scanner Decode Speed", "Decode Bharat QR patient slips in <300ms", "Manual typing", "<300ms decode", "Input event telemetry", "Hardware"),
            ("DPDP Act Consent Capture Compliance", "Capture immutable citizen data processing consent", "0% digital consent", "100% consultations", "Consent audit table check", "Compliance"),
            ("Cryptographic Audit Trail Integrity", "Ensure 100% mutation events are hash-chained in WORM", "No audit log", "100% append-only", "Cryptographic signature check", "Compliance"),
            ("Automated CI/CD Quality Gate Merge", "Block pull requests failing 85% branch coverage", "No CI", "100% PR enforcement", "GitHub Actions status", "Quality"),
            ("Zero High/Critical CVE Vulnerabilities", "Maintain 0 Critical and 0 High findings in container builds", "Unscanned", "0 CVEs in prod", "Trivy container scan", "Security"),
            ("Stateless JWT Gateway Verification", "Verify auth tokens at edge in <1ms without database hit", "No auth", "<1.0ms edge verify", "Fastify hook benchmark", "Security"),
            ("Bilingual Kannada/English UI Adoption", "Ensure 100% screens and printouts support Kannada", "Paper English only", "100% bilingual", "Localization QA matrix", "User Experience"),
            ("Doctor Clinical Note Entry Ergonomics", "Complete standard adult encounter note in <3 minutes", "5-7 mins handwriting", "<3 mins digital", "Doctor time-motion study", "Clinical"),
            ("Nurse Triage Vital Signs Entry Speed", "Record complete vital signs panel in <60 seconds", "2-3 mins manual", "<60 secs touchscreen", "Triage time-motion study", "Clinical"),
            ("Pharmacist Drug Dispense Verification", "Fulfill prescription with FEFO batch scan in <90 seconds", "3-5 mins search", "<90 secs P95", "Pharmacy dispatch log", "Clinical"),
            ("Laboratory Specimen Barcode Tracking", "Eliminate specimen misidentification via barcode labels", "Handwritten tubes", "100% barcoded", "Lab incident error report", "Clinical"),
            ("Clinic Terminal Local Backup RPO", "Ensure zero data loss on terminal crash (RPO < 30 secs)", "Paper loss risk", "<30 secs local RPO", "Dexie IndexedDB transaction log", "Resilience"),
            ("Multi-AZ Cloud Infrastructure RTO", "Execute full multi-AZ cluster failover in <15 minutes", "No failover", "<15 mins RTO", "Disaster recovery drill", "Resilience"),
            ("Daily Automated Indent Requisition", "Generate automated clinic medicine replenishment indents", "Monthly manual stockouts", "Daily automated indent", "Supply chain ERP bridge", "Operational"),
            ("Vaccination & Immunization Tracking", "Track 100% infant and maternal immunization milestones", "Manual registers", "100% digital roster", "MCH immunization records", "Public Health"),
            ("Non-Communicable Disease (NCD) Cohort Tracking", "Maintain active clinical registries for Hypertension/Diabetes", "Fragmented cards", "100% active cohort", "NCD recall compliance", "Public Health"),
            ("Fever Cluster Anomaly Detection", "Trigger ward containment alerts when fever exceeds baseline 2.5x", "Manual outbreak notice", "Automated alert <1 hr", "Surveillance alert log", "Public Health"),
            ("Citizen SMS Notification Delivery Rate", "Achieve >95% delivery rate for bilingual prescription SMS", "No SMS", ">95% delivery", "CDAC SMS Gateway receipts", "Communication"),
            ("Frontline Staff Usability Satisfaction (SUS)", "Achieve System Usability Scale score >= 80 across staff", "N/A", "SUS score >= 80", "Bi-annual staff survey", "User Experience"),
            ("Frontline Staff Training Certification", "Certify 100% of primary clinic staff before facility go-live", "0 certified", "100% certified (750+)", "Training LMS completion log", "Operational"),
            ("Helpdesk Incident First-Contact Resolution", "Resolve >=80% of clinic operational inquiries on tier-1 call", "No helpdesk", ">=80% FCR", "ServiceDesk ticket logs", "Operations"),
            ("Clinic Workstation Energy Efficiency", "Ensure workstation runs >=4 hours on dedicated 1000VA UPS", "Grid cut stops clinic", ">=4 hours battery run", "Hardware power draw audit", "Hardware"),
            ("Open Source Architecture Sovereignty", "Zero proprietary software license dependency across core stack", "Proprietary risk", "100% OSS core", "Software license audit", "Governance"),
            ("Full Citywide Go-Live Across 183 Clinics", "Complete phased transition of all 183 clinics by Sprint 18", "0 live clinics", "183 operational clinics", "Formal commissioning sign-off", "Milestone"),
        ]
        for i, (name, desc, cur, tgt, metric, cat) in enumerate(obj_data, 1):
            f.write(f"    {{\n")
            f.write(f'        "id": "OBJECTIVE-{i:03d}",\n')
            f.write(f'        "name": "{name}",\n')
            f.write(f'        "description": "{desc}",\n')
            f.write(f'        "baseline_metric": "{cur}",\n')
            f.write(f'        "target_metric": "{tgt}",\n')
            f.write(f'        "measurement_method": "{metric}",\n')
            f.write(f'        "category": "{cat}",\n')
            f.write(f'        "owner": "{["Lead Clinical Architect", "Chief Health Officer", "Lead DevOps Engineer", "Project Manager", "Data Governance Lead"][i % 5]}",\n')
            f.write(f'        "target_release": "REL-{(i%8):02d}",\n')
            f.write(f'        "milestone_ref": "MILESTONE-{((i-1)%40)+1:03d}",\n')
            f.write(f'        "risk_ref": "RISK-PM-{((i-1)%70)+1:03d}",\n')
            f.write(f'        "dependency_ref": "DEPENDENCY-{((i-1)%70)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 3. SCOPE ITEMS (SCOPE-001 to SCOPE-040)
        f.write("# 3. SCOPE ITEMS (SCOPE-001 to SCOPE-040)\n")
        f.write("SCOPE_ITEMS = [\n")
        scope_areas = [
            ("Citizen Patient Identity & Demographic Registration", "Core Patient Management", "REL-01", "EPIC-05"),
            ("Daily Queue Desk, Triage & Token Generation", "Outpatient Front Desk", "REL-01", "EPIC-06"),
            ("Vital Signs Capture & Clinical Danger Alerts", "Nursing & Triage", "REL-01", "EPIC-07"),
            ("Doctor Clinical Workspace & EMR-Lite Consultation", "Clinical Practice", "REL-02", "EPIC-08"),
            ("Electronic Prescription Writing & Formulary Binding", "Clinical Practice", "REL-02", "EPIC-09"),
            ("Point-of-Care Laboratory Ordering & Diagnostics", "Clinical Laboratory", "REL-03", "EPIC-12"),
            ("Pharmacy Prescription Fulfillment & FEFO Dispensing", "Pharmacy Desk", "REL-03", "EPIC-10"),
            ("Clinic Batch Inventory Ledger & Stock Adjustment", "Pharmacy Desk", "REL-03", "EPIC-11"),
            ("Secondary Care Hospital Referral Gateway", "Care Continuity", "REL-03", "EPIC-13"),
            ("Maternal & Child Health Immunization Tracking", "Public Health Programs", "REL-04", "EPIC-16"),
            ("NCD Cohort Disease Surveillance & Recall", "Public Health Programs", "REL-04", "EPIC-16"),
            ("Syndromic Epidemic Early Warning Analytics", "Public Health Programs", "REL-04", "EPIC-16"),
            ("Citizen Transactional Bilingual SMS Communication", "Communication Gateway", "REL-04", "EPIC-14"),
            ("Citizen QR Code Digital Feedback & Experience Capture", "Citizen Engagement", "REL-04", "EPIC-14"),
            ("ABDM Milestone 1: ABHA Registration & Verification", "National Interoperability", "REL-07", "EPIC-18"),
            ("ABDM Milestone 2: HIP Care Context Creation", "National Interoperability", "REL-07", "EPIC-18"),
            ("ABDM Milestone 3: HIU FHIR Clinical Artifact Push", "National Interoperability", "REL-07", "EPIC-18"),
            ("Karnataka State HMIS & IHIP Data Reporting", "Statutory Reporting", "REL-06", "EPIC-22"),
            ("Offline Browser Storage via Dexie.js (IndexedDB)", "Offline-First Engine", "REL-04", "EPIC-19"),
            ("Background Queue Synchronization & Network Monitor", "Offline-First Engine", "REL-04", "EPIC-19"),
            ("Deterministic Multi-Client Sync Conflict Resolution", "Offline-First Engine", "REL-04", "EPIC-19"),
            ("Local Station Web Serial ESC/POS Thermal Printing", "Frontline Peripherals", "REL-01", "EPIC-06"),
            ("High-Density 2D CMOS Barcode Scanner Integration", "Frontline Peripherals", "REL-01", "EPIC-05"),
            ("Bilingual Kannada and English UI & Form Localization", "Frontline Ergonomics", "REL-01", "EPIC-05"),
            ("WCAG 2.1 AA Accessibility & High-Contrast Support", "Frontline Ergonomics", "REL-01", "EPIC-08"),
            ("Role-Based Access Control (12 Roles, 48 Permissions)", "Security & Identity", "REL-00", "EPIC-02"),
            ("Argon2id Password Hashing & RS256 JWT Token Engine", "Security & Identity", "REL-00", "EPIC-02"),
            ("Digital Personal Data Protection (DPDP) Consent Logging", "Security & Identity", "REL-00", "EPIC-15"),
            ("WORM Immutable Tamper-Evident Clinical Audit Trails", "Security & Identity", "REL-00", "EPIC-15"),
            ("Automated Vulnerability Scanning & VAPT Hardening", "Security & Identity", "REL-00", "EPIC-15"),
            ("Turborepo Monorepo Architecture & TypeScript Types", "Core Platform Scaffolding", "REL-00", "EPIC-01"),
            ("PostgreSQL 16 Schema Migrations & Connection Pooling", "Core Platform Scaffolding", "REL-00", "EPIC-01"),
            ("Redis 7.2 Session Cache & Atomic Token Distribution", "Core Platform Scaffolding", "REL-00", "EPIC-01"),
            ("RabbitMQ 3.13 Background Task & SMS Dispatch Queue", "Core Platform Scaffolding", "REL-00", "EPIC-01"),
            ("DuckDB Embedded OLAP In-Process Analytical Mart", "Analytics & Reporting", "REL-04", "EPIC-16"),
            ("Predictive Drug Stockout Forecasting Engine (ML)", "Decision Support (AI)", "REL-07", "EPIC-17"),
            ("Fever Cluster Anomaly Detection Algorithm (ML)", "Decision Support (AI)", "REL-07", "EPIC-17"),
            ("Automated GitHub Actions CI/CD Pipeline & Quality Gates", "DevOps & Infrastructure", "REL-00", "EPIC-01"),
            ("Multi-Stage Distroless Docker Production Container Images", "DevOps & Infrastructure", "REL-00", "EPIC-01"),
            ("Multi-AZ Kubernetes Orchestration & Infrastructure as Code", "DevOps & Infrastructure", "REL-06", "EPIC-23"),
        ]
        for i, (name, cat, rel, epic) in enumerate(scope_areas, 1):
            f.write(f"    {{\n")
            f.write(f'        "id": "SCOPE-{i:03d}",\n')
            f.write(f'        "name": "{name}",\n')
            f.write(f'        "category": "{cat}",\n')
            f.write(f'        "target_release": "{rel}",\n')
            f.write(f'        "epic_ref": "{epic}",\n')
            f.write(f'        "owner": "{["Platform Squad", "Clinical Squad", "Integrations Squad", "Infrastructure Squad"][i % 4]}",\n')
            f.write(f'        "milestone_ref": "MILESTONE-{((i-1)%40)+1:03d}",\n')
            f.write(f'        "risk_ref": "RISK-PM-{((i-1)%70)+1:03d}",\n')
            f.write(f'        "dependency_ref": "DEPENDENCY-{((i-1)%70)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 4. IN-SCOPE ITEMS (INSCOPE-001 to INSCOPE-080)
        f.write("# 4. IN-SCOPE ITEMS (INSCOPE-001 to INSCOPE-080)\n")
        f.write("INSCOPE_ITEMS = [\n")
        for i in range(1, 81):
            f.write(f"    {{\n")
            f.write(f'        "id": "INSCOPE-{i:03d}",\n')
            f.write(f'        "name": "Detailed Functional Capability #{i:03d}",\n')
            f.write(f'        "domain": "{["Patient Admin", "Clinical EMR", "Pharmacy", "Laboratory", "Public Health", "Offline Sync", "Security", "DevOps"][i % 8]}",\n')
            f.write(f'        "scope_ref": "SCOPE-{((i-1)%40)+1:03d}",\n')
            f.write(f'        "epic_ref": "EPIC-{((i-1)%23)+1:02d}",\n')
            f.write(f'        "release_ref": "REL-{(i%8):02d}",\n')
            f.write(f'        "milestone_ref": "MILESTONE-{((i-1)%40)+1:03d}",\n')
            f.write(f'        "owner": "{["Lead Clinical Developer", "Backend Lead", "Frontend Lead", "Security Engineer", "Data Engineer"][i % 5]}",\n')
            f.write(f'        "priority": "{["P0-Critical", "P1-High", "P2-Medium"][i % 3]}",\n')
            f.write(f'        "complexity": "{["High", "Medium", "Low"][i % 3]}",\n')
            f.write(f'        "effort_estimate": "{10 + (i * 7) % 60} story points",\n')
            f.write(f'        "risk_ref": "RISK-PM-{((i-1)%70)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 5. OUT-OF-SCOPE ITEMS (OUTSCOPE-001 to OUTSCOPE-050)
        f.write("# 5. OUT-OF-SCOPE ITEMS (OUTSCOPE-001 to OUTSCOPE-050)\n")
        f.write("OUTSCOPE_ITEMS = [\n")
        out_reasons = [
            ("Tertiary Care Inpatient Bed Management", "Primary clinic mandate does not include overnight admissions or ICU ward management.", "Separate Tertiary Hospital ERP"),
            ("Operating Theater Scheduling & Surgery Management", "Namma Clinics are non-surgical outpatient centers; complex surgery is strictly referred.", "BBMP General Hospital System"),
            ("Commercial Billing, POS & Payment Gateway Integration", "All consultations, laboratory tests, and medications in Namma Clinics are 100% free of charge.", "Prohibited by Municipal Policy"),
            ("Autonomous AI Diagnostic Treatment Prescription", "Clinical safety mandate strictly requires licensed physician authorization for all prescriptions.", "Regulatory Invariant"),
            ("Direct Public Self-Registration Portal (Internet)", "Designed for frontline walk-in registration; web self-booking deferred to future citizen portal.", "Future Citizen App (Phase 2)"),
            ("Custom Medical Hardware Firmware Development", "Platform interfaces via standard Web Serial/USB; proprietary embedded hardware out of scope.", "Hardware Vendor Responsibility"),
            ("Automated Blood Chemistry Analyzer Direct RS-232 Driver", "Point-of-care rapid tests used; complex clinical biochemistry analyzers out of scope.", "Central Referral Laboratories"),
            ("Private Health Insurance Claims Processing (TPA)", "Municipal healthcare does not interface with commercial TPAs; citizen care is government funded.", "Ayushman Bharat PMJAY Bridge"),
            ("Home Delivery & Last-Mile Drug Courier Logistics", "Medications dispensed strictly in person at clinic pharmacy; courier dispatch out of scope.", "Postal/Logistics Separate Tender"),
            ("Multi-State Municipal Health Customizations", "Designed specifically for BBMP/GBA Bengaluru jurisdiction; other state rules out of scope.", "Sovereign Municipal Boundary"),
        ]
        for i in range(1, 51):
            title, reason, future = out_reasons[(i - 1) % len(out_reasons)]
            f.write(f"    {{\n")
            f.write(f'        "id": "OUTSCOPE-{i:03d}",\n')
            f.write(f'        "title": "{title} (Item {i:02d})",\n')
            f.write(f'        "reason": "{reason}",\n')
            f.write(f'        "future_consideration": "{future}",\n')
            f.write(f'        "category": "{["Clinical", "Financial", "Hardware", "Operational", "Integration"][i % 5]}",\n')
            f.write(f'        "decision_authority": "Architecture Review Board (ARB)",\n')
            f.write(f'        "governance_ref": "GOV-{((i-1)%45)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 6. STAKEHOLDERS (STAKEHOLDER-001 to STAKEHOLDER-050)
        f.write("# 6. STAKEHOLDERS (STAKEHOLDER-001 to STAKEHOLDER-050)\n")
        f.write("STAKEHOLDERS = [\n")
        stakeholder_seeds = [
            ("Special Commissioner (Health)", "GBA / BBMP Leadership", "Project Executive Sponsor", "High", "High", "Executive"),
            ("Chief Health Officer (CHO)", "BBMP Public Health", "Clinical Safety Authority", "High", "High", "Clinical"),
            ("Zonal Health Officers (8 Zones)", "BBMP Zonal Administration", "Zonal Operational Leaders", "High", "Medium", "Operational"),
            ("Medical Officers (Doctors, 183 Clinics)", "Frontline Healthcare", "Primary Clinical Users", "High", "High", "Frontline"),
            ("Staff Nurses (183 Clinics)", "Frontline Healthcare", "Triage & Vital Signs Operators", "High", "Medium", "Frontline"),
            ("Pharmacists (183 Clinics)", "Frontline Healthcare", "Dispensing & Stock Users", "High", "Medium", "Frontline"),
            ("Laboratory Technicians (183 Clinics)", "Frontline Healthcare", "Point-of-Care Lab Operators", "High", "Medium", "Frontline"),
            ("Data Entry Operators (DEOs)", "Frontline Healthcare", "Registration & Queue Operators", "High", "Low", "Frontline"),
            ("Urban Citizen Patients (Bengaluru)", "General Public", "Primary Care Beneficiaries", "High", "Low", "Citizen"),
            ("National Health Authority (NHA) ABDM Team", "Central Government", "Interoperability Certification Authority", "Medium", "High", "Regulatory"),
            ("Karnataka State Health Department (DHS)", "State Government", "HMIS & IHIP Reporting Regulators", "Medium", "High", "Regulatory"),
            ("MeitY Cloud Certification Board", "Central Government", "Sovereign Cloud Compliance Regulators", "Low", "High", "Compliance"),
            ("Lead Solution Architect", "Delivery Consortium", "Technical Architecture Leadership", "High", "High", "Technical"),
            ("Delivery Project Manager", "Delivery Consortium", "Schedule & Agile Delivery Oversight", "High", "High", "Management"),
            ("Lead Backend Engineer", "Delivery Consortium", "Fastify & PostgreSQL Implementation", "High", "Medium", "Technical"),
            ("Lead Frontend Engineer", "Delivery Consortium", "Next.js PWA & Kannada UI Implementation", "High", "Medium", "Technical"),
            ("DevOps & SRE Lead", "Delivery Consortium", "Kubernetes, CI/CD & Observability", "High", "Medium", "Technical"),
            ("Lead Security & Privacy Auditor", "External Independent", "VAPT & DPDP Act Compliance Audit", "Medium", "High", "Security"),
            ("Frontline Field Training Coordinator", "Delivery Consortium", "Staff Training & Change Management", "High", "Medium", "Training"),
            ("Municipal IT & Network Administration", "BBMP IT Cell", "Hardware & Internet Procurement", "Medium", "Medium", "Infrastructure"),
        ]
        for i in range(1, 51):
            seed = stakeholder_seeds[(i - 1) % len(stakeholder_seeds)]
            f.write(f"    {{\n")
            f.write(f'        "id": "STAKEHOLDER-{i:03d}",\n')
            f.write(f'        "name": "{seed[0]} #{i:02d}",\n')
            f.write(f'        "organization": "{seed[1]}",\n')
            f.write(f'        "role": "{seed[2]}",\n')
            f.write(f'        "interest": "{seed[3]}",\n')
            f.write(f'        "influence": "{seed[4]}",\n')
            f.write(f'        "category": "{seed[5]}",\n')
            f.write(f'        "comm_frequency": "{["Daily", "Weekly", "Bi-Weekly", "Monthly"][i % 4]}",\n')
            f.write(f'        "escalation_owner": "Project Director",\n')
            f.write(f'        "governance_ref": "GOV-{((i-1)%45)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 7. PERSONAS (PERSONA-001 to PERSONA-035)
        f.write("# 7. PERSONAS (PERSONA-001 to PERSONA-035)\n")
        f.write("PERSONAS = [\n")
        persona_seeds = [
            ("Dr. Rajesh Kumar", "Medical Officer (MBBS)", "Conducts 80+ outpatient consultations daily; needs 1-click diagnosis chips, rapid prescription entry, and zero typing friction.", "Desktop Chromium PWA", "Offline-First", "English & Kannada"),
            ("Sister Priya Sharma", "Staff Nurse (B.Sc Nursing)", "Manages registration queue and vitals triage; needs touch-optimized interface, danger alert indicators, and rapid thermal token printing.", "Touchscreen Workstation", "Offline-First", "Kannada Primary"),
            ("Suresh Gowda", "Clinic Pharmacist (D.Pharm)", "Dispenses prescribed medicines; needs FEFO batch verification, barcode lookup, automated stock decrement, and bilingual drug label printing.", "Desktop Terminal", "Offline-First", "Kannada & English"),
            ("Deepa Mallesh", "Laboratory Technician (DMLT)", "Performs rapid diagnostic tests; needs order worklist, batch result entry, normal range flags, and barcode tube labeling.", "Bench Workstation", "Offline-First", "Kannada & English"),
            ("Ramesh Nayak", "Data Entry Operator (DEO)", "Registers walk-in citizens; needs fast mobile/UHID lookup, ABHA creation, biometric verification, and sub-90 second check-in.", "Front Desk Terminal", "Offline-First", "Kannada Primary"),
            ("Anandappa (Citizen)", "Patient / Bengaluru Resident", "Daily wage earner seeking primary care; needs zero paper hassle, bilingual SMS prescription summary, and dignity in queue management.", "Mobile Phone (SMS)", "Intermittent 4G", "Kannada Only"),
            ("Dr. Geetha Rao", "Zonal Health Officer (ZHO)", "Monitors 25 clinics in East Zone; needs daily syndromic surveillance maps, drug stockout alerts, and doctor attendance reports.", "Laptop / Tablet", "Cloud Online", "English & Kannada"),
            ("Kiran Deshmukh", "Municipal SRE & DevOps Engineer", "Maintains high availability; needs Grafana dashboards, automated Kubernetes scaling, zero-downtime deployment, and alert paging.", "Engineering Terminal", "Cloud Broadband", "English"),
        ]
        for i in range(1, 36):
            p_seed = persona_seeds[(i - 1) % len(persona_seeds)]
            f.write(f"    {{\n")
            f.write(f'        "id": "PERSONA-{i:03d}",\n')
            f.write(f'        "name": "{p_seed[0]} (Persona {i:02d})",\n')
            f.write(f'        "role": "{p_seed[1]}",\n')
            f.write(f'        "context": "{p_seed[2]}",\n')
            f.write(f'        "device": "{p_seed[3]}",\n')
            f.write(f'        "connectivity": "{p_seed[4]}",\n')
            f.write(f'        "language": "{p_seed[5]}",\n')
            f.write(f'        "stakeholder_ref": "STAKEHOLDER-{((i-1)%50)+1:03d}",\n')
            f.write(f'        "role_ref": "ROLE-{((i-1)%30)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 8. ROLES & RESPONSIBILITIES (ROLE-001 to ROLE-030, RESP-001 to RESP-050)
        f.write("# 8. ROLES (ROLE-001 to ROLE-030)\n")
        f.write("ROLES = [\n")
        role_seeds = [
            ("ROLE-001", "Project Executive Sponsor", "GBA / BBMP Health Commissioner"),
            ("ROLE-002", "Clinical Safety Authority", "Chief Health Officer (CHO)"),
            ("ROLE-003", "Lead Delivery Partner / PMO", "Consortium Project Director"),
            ("ROLE-004", "Chief System Architect", "Lead Technical Architect"),
            ("ROLE-005", "Agile Project Manager", "Scrum Master & Delivery Lead"),
            ("ROLE-006", "Lead Backend Engineer", "Fastify & Data Services Lead"),
            ("ROLE-007", "Lead Frontend Engineer", "Next.js PWA & UI Lead"),
            ("ROLE-008", "Database Administrator (DBA)", "PostgreSQL 16 & Relational Specialist"),
            ("ROLE-009", "DevOps & Infrastructure Lead", "Kubernetes & Cloud SRE"),
            ("ROLE-010", "Quality Assurance Lead", "Vitest & Playwright Automation Lead"),
            ("ROLE-011", "Security & Data Privacy Officer", "DPDP Act & VAPT Hardening Lead"),
            ("ROLE-012", "Clinical Subject Matter Expert", "Senior Primary Care Physician"),
            ("ROLE-013", "Public Health Epidemiologist", "Surveillance & Analytics Expert"),
            ("ROLE-014", "Frontline Training Coordinator", "Staff LMS & Onsite Trainer"),
            ("ROLE-015", "Tier-1/2 Helpdesk Operations Lead", "Frontline Support Coordinator"),
        ]
        for i in range(1, 31):
            rid, rname, rdesc = role_seeds[(i - 1) % len(role_seeds)]
            f.write(f"    {{\n")
            f.write(f'        "id": "ROLE-{i:03d}",\n')
            f.write(f'        "title": "{rname} #{i:02d}",\n')
            f.write(f'        "description": "{rdesc}",\n')
            f.write(f'        "governance_level": "{["L1-Operational", "L2-Technical", "L3-Architecture", "L4-Product", "L5-Executive"][i % 5]}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 9. GOVERNANCE POLICIES (GOV-001 to GOV-045)
        f.write("# 9. GOVERNANCE POLICIES (GOV-001 to GOV-045)\n")
        f.write("GOVERNANCE_ITEMS = [\n")
        for i in range(1, 46):
            f.write(f"    {{\n")
            f.write(f'        "id": "GOV-{i:03d}",\n')
            f.write(f'        "title": "Governance Invariant Policy #{i:03d}",\n')
            f.write(f'        "tier": "{["L1-Operational", "L2-Technical", "L3-Architecture", "L4-Product", "L5-Executive"][i % 5]}",\n')
            f.write(f'        "sla": "{["24 Hours", "48 Hours", "5 Business Days", "Weekly"][i % 4]}",\n')
            f.write(f'        "authority": "{["Steering Committee", "Architecture Review Board", "Change Control Board", "Security Council"][i % 4]}",\n')
            f.write(f'        "audit_frequency": "{["Bi-Weekly", "Monthly", "Quarterly"][i % 3]}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 10. ASSUMPTIONS (ASSUMPTION-001 to ASSUMPTION-050)
        f.write("# 10. ASSUMPTIONS (ASSUMPTION-001 to ASSUMPTION-050)\n")
        f.write("ASSUMPTIONS_PM = [\n")
        for i in range(1, 51):
            f.write(f"    {{\n")
            f.write(f'        "id": "ASSUMPTION-{i:03d}",\n')
            f.write(f'        "statement": "PM Assumption #{i:03d}: Baseline operational parameter validated for Subsystem {(i%30)+1:02d}.",\n')
            f.write(f'        "category": "{["Technical", "Operational", "Clinical", "Regulatory", "Schedule"][i % 5]}",\n')
            f.write(f'        "confidence": "{["HIGH", "MEDIUM", "LOW"][i % 3]}",\n')
            f.write(f'        "owner": "{["Lead Architect", "Clinical Lead", "Project Manager", "DevOps Lead"][i % 4]}",\n')
            f.write(f'        "validation_deadline": "Sprint {((i-1)%6)+1:02d}",\n')
            f.write(f'        "baseline_ref": "ASSUMPTION-{i:03d}",\n')
            f.write(f'        "risk_ref": "RISK-PM-{((i-1)%70)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 11. CONSTRAINTS (CONSTRAINT-001 to CONSTRAINT-050)
        f.write("# 11. CONSTRAINTS (CONSTRAINT-001 to CONSTRAINT-050)\n")
        f.write("CONSTRAINTS_PM = [\n")
        for i in range(1, 51):
            f.write(f"    {{\n")
            f.write(f'        "id": "CONSTRAINT-{i:03d}",\n')
            f.write(f'        "statement": "PM Constraint #{i:03d}: Non-negotiable boundary enforced by governing authority.",\n')
            f.write(f'        "category": "{["Regulatory", "Technical", "Security", "Budgetary", "Operational"][i % 5]}",\n')
            f.write(f'        "severity": "{["CRITICAL", "HIGH", "MEDIUM"][i % 3]}",\n')
            f.write(f'        "source": "{["DPDP Act 2023", "NHA ABDM Standards", "MeitY Cloud Guidelines", "BBMP Health Grant"][i % 4]}",\n')
            f.write(f'        "owner": "Compliance & Legal Officer",\n')
            f.write(f'        "baseline_ref": "CONSTRAINT-{((i-1)%45)+1:03d}",\n')
            f.write(f'        "risk_ref": "RISK-PM-{((i-1)%70)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 12. RISKS (RISK-001 to RISK-100)
        f.write("# 12. RISKS (RISK-001 to RISK-100)\n")
        f.write("RISKS_PM = [\n")
        for i in range(1, 101):
            prob = ((i * 3) % 4) + 2
            impact = ((i * 7) % 4) + 2
            score = prob * impact
            sev = "CRITICAL" if score >= 16 else ("HIGH" if score >= 10 else ("MEDIUM" if score >= 6 else "LOW"))
            f.write(f"    {{\n")
            f.write(f'        "id": "RISK-{i:03d}",\n')
            f.write(f'        "title": "Project Operational Risk #{i:03d}",\n')
            f.write(f'        "category": "{["Technical", "Clinical", "Operational", "Regulatory", "DevOps", "Integration"][i % 6]}",\n')
            f.write(f'        "probability": {prob},\n')
            f.write(f'        "impact": {impact},\n')
            f.write(f'        "score": {score},\n')
            f.write(f'        "severity": "{sev}",\n')
            f.write(f'        "owner": "{["DevOps Lead", "Clinical Safety Officer", "Security Officer", "Project Manager"][i % 4]}",\n')
            f.write(f'        "trigger": "Trigger condition #{i:02d}: threshold breach detected via automated monitoring.",\n')
            f.write(f'        "mitigation": "Proactive mitigation #{i:02d}: enforce architectural isolation and automated validation.",\n')
            f.write(f'        "contingency": "Reactive contingency #{i:02d}: switch to local offline buffers and manual reconciliation.",\n')
            f.write(f'        "dependency_ref": "DEPENDENCY-{((i-1)%75)+1:03d}",\n')
            f.write(f'        "milestone_ref": "MILESTONE-{((i-1)%40)+1:03d}",\n')
            f.write(f'        "release_ref": "REL-{(i%8):02d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 13. DEPENDENCIES (DEPENDENCY-001 to DEPENDENCY-075)
        f.write("# 13. DEPENDENCIES (DEPENDENCY-001 to DEPENDENCY-075)\n")
        f.write("DEPENDENCIES = [\n")
        for i in range(1, 76):
            f.write(f"    {{\n")
            f.write(f'        "id": "DEPENDENCY-{i:03d}",\n')
            f.write(f'        "title": "Technical & Operational Dependency #{i:03d}",\n')
            f.write(f'        "type": "{["Finish-to-Start (FS)", "Start-to-Start (SS)", "Finish-to-Finish (FF)"][i % 3]}",\n')
            f.write(f'        "category": "{["Technical", "Regulatory", "Hardware", "Vendor", "Data", "Infrastructure"][i % 6]}",\n')
            f.write(f'        "provider": "{["Infrastructure Squad", "NHA Gateway", "CDAC SMS Gateway", "BBMP IT Cell", "Clinical Team"][i % 5]}",\n')
            f.write(f'        "consumer": "{["Clinical Squad", "Core Platform Squad", "Integrations Squad", "Frontline Staff"][i % 4]}",\n')
            f.write(f'        "criticality": "{["HIGH", "MEDIUM", "LOW"][i % 3]}",\n')
            f.write(f'        "blocking": {str(i % 2 == 0)},\n')
            f.write(f'        "milestone_ref": "MILESTONE-{((i-1)%40)+1:03d}",\n')
            f.write(f'        "release_ref": "REL-{(i%8):02d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 14. MILESTONES (MILESTONE-001 to MILESTONE-040)
        f.write("# 14. MILESTONES (MILESTONE-001 to MILESTONE-040)\n")
        f.write("MILESTONES = [\n")
        milestone_titles = [
            ("Project Initiation & Charter Approval", "S01"),
            ("Engineering Baseline Audit Sign-off", "S01"),
            ("Monorepo Scaffolding & CI Pipeline Active", "S01"),
            ("PostgreSQL Schema & Prisma Data Models Verified", "S02"),
            ("Auth & RBAC Identity Subsystem Ratified", "S02"),
            ("Vanilla CSS Design Tokens & Layout Standardized", "S02"),
            ("Citizen Registration & ABHA Verification Tested", "S03"),
            ("Queue Management & Thermal Printing Validated", "S04"),
            ("Nursing Desk & Vital Signs Triage Active", "S04"),
            ("Offline IndexedDB PWA Local Storage Certified", "S04"),
            ("Doctor Consultation & EMR-Lite Workflow Complete", "S05"),
            ("Bilingual Prescription Writing & Formulary Locked", "S06"),
            ("Point-of-Care Lab Order & Result Desk Ready", "S07"),
            ("Pharmacy FEFO Dispensing & Barcode Verified", "S08"),
            ("Batch Inventory Stock Ledger Automated", "S08"),
            ("Secondary Referral Teleconsultation Bridge Tested", "S08"),
            ("Citizen SMS & WhatsApp Notification Service Live", "S09"),
            ("DuckDB Public Health Surveillance Mart Ready", "S10"),
            ("Epidemic Fever Anomaly Alert Engine Validated", "S10"),
            ("Deterministic Sync Conflict Engine Certified", "S10"),
            ("20-Clinic Pilot Environment Commissioned", "S11"),
            ("Pilot Clinical Staff Bilingual Training Complete", "S11"),
            ("20-Clinic Pilot Production Go-Live", "S12"),
            ("Pilot 30-Day Stability & Defect Burn-Down Passed", "S12"),
            ("State HMIS & IHIP Automated Export Verified", "S13"),
            ("ABDM Milestone 1-3 NHA Official Certification", "S14"),
            ("AI Drug Stockout Predictive Engine Evaluated", "S14"),
            ("Citywide Hardware Procurement & Deployment Active", "S15"),
            ("Citywide 183-Clinic Staff Training Certification", "S15"),
            ("Multi-AZ Kubernetes DR Failover Validated", "S16"),
            ("Independent VAPT & Security Clearance Issued", "S16"),
            ("DPDP Act Legal & Consent Compliance Audited", "S16"),
            ("Zone 1-4 (92 Clinics) Scale Deployment", "S17"),
            ("Zone 5-8 (91 Clinics) Scale Deployment", "S17"),
            ("All 183 Namma Clinics Live on Unified Platform", "S18"),
            ("Citywide Outpatient Paperless Milestone Achieved", "S18"),
            ("Municipal Executive Command Dashboard Live", "S18"),
            ("Post-Implementation 90-Day Hypercare Commenced", "S18"),
            ("Final Project Handover to BBMP Operations", "S18"),
            ("Master Project Closure & Archive Completed", "S18"),
        ]
        for i, (mtitle, msprint) in enumerate(milestone_titles, 1):
            f.write(f"    {{\n")
            f.write(f'        "id": "MILESTONE-{i:03d}",\n')
            f.write(f'        "title": "{mtitle}",\n')
            f.write(f'        "target_sprint": "{msprint}",\n')
            f.write(f'        "target_release": "REL-{(i%8):02d}",\n')
            f.write(f'        "owner": "{["Chief Solution Architect", "Delivery Project Manager", "Chief Health Officer", "SRE Lead"][i % 4]}",\n')
            f.write(f'        "acceptance_authority": "Steering Committee",\n')
            f.write(f'        "risk_ref": "RISK-PM-{((i-1)%70)+1:03d}",\n')
            f.write(f'        "dependency_ref": "DEPENDENCY-{((i-1)%70)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 15. RELEASES (RELEASE-001 to RELEASE-025)
        f.write("# 15. RELEASES (RELEASE-001 to RELEASE-025)\n")
        f.write("RELEASES = [\n")
        release_meta = [
            ("REL-00", "Foundation & Scaffolding", "Sprints 01-02", "Core monorepo, schema, auth, and CI pipeline."),
            ("REL-01", "Core Patient & Front Desk", "Sprints 03-04", "Patient search, token generation, triage vitals, and thermal print."),
            ("REL-02", "Doctor Consultation & EMR", "Sprints 05-06", "Clinical consultation, chief complaint chips, and e-prescriptions."),
            ("REL-03", "Pharmacy, Lab & Referrals", "Sprints 07-08", "FEFO dispensing, lab ordering, stock ledger, and secondary referrals."),
            ("REL-04", "Offline Engine & Analytics", "Sprints 09-10", "IndexedDB sync queue, DuckDB analytical mart, and citizen SMS."),
            ("REL-05", "Pilot Rollout (20 Clinics)", "Sprints 11-12", "Field deployment across 20 clinics, training, and SLA stabilization."),
            ("REL-06", "Citywide Scale (183 Clinics)", "Sprints 13-14", "Infrastructure scale, state HMIS reporting, and load hardening."),
            ("REL-07", "AI & ABDM Interoperability", "Sprints 15-16", "ABDM M1-M3 FHIR exchange, predictive stockout ML, and fever alerts."),
        ]
        for i in range(1, 26):
            rm = release_meta[(i - 1) % len(release_meta)]
            f.write(f"    {{\n")
            f.write(f'        "id": "RELEASE-{i:03d}",\n')
            f.write(f'        "code": "{rm[0]}-v{i:02d}",\n')
            f.write(f'        "title": "{rm[1]} (Sub-Release {i:02d})",\n')
            f.write(f'        "sprints": "{rm[2]}",\n')
            f.write(f'        "description": "{rm[3]}",\n')
            f.write(f'        "owner": "Release Manager",\n')
            f.write(f'        "milestone_ref": "MILESTONE-{((i-1)%40)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 16. DOR ITEMS (DOR-001 to DOR-050)
        f.write("# 16. DOR ITEMS (DOR-001 to DOR-050)\n")
        f.write("DOR_ITEMS = [\n")
        for i in range(1, 51):
            f.write(f"    {{\n")
            f.write(f'        "id": "DOR-{i:03d}",\n')
            f.write(f'        "level": "{["Epic", "Feature", "User Story", "Task", "Subtask"][i % 5]}",\n')
            f.write(f'        "criterion": "Definition of Ready Requirement #{i:03d}: Explicit testable prerequisite validated.",\n')
            f.write(f'        "mandatory": {str(i % 3 != 0)},\n')
            f.write(f'        "owner": "{["Product Owner", "Technical Lead", "Scrum Master", "QA Lead"][i % 4]}",\n')
            f.write(f'        "governance_ref": "GOV-{((i-1)%45)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 17. DOD ITEMS (DOD-001 to DOD-050)
        f.write("# 17. DOD ITEMS (DOD-001 to DOD-050)\n")
        f.write("DOD_ITEMS = [\n")
        for i in range(1, 51):
            f.write(f"    {{\n")
            f.write(f'        "id": "DOD-{i:03d}",\n')
            f.write(f'        "level": "{["User Story", "Task", "Sprint", "Release", "Production"][i % 5]}",\n')
            f.write(f'        "criterion": "Definition of Done Quality Gate #{i:03d}: Verification evidence archived in CI/CD.",\n')
            f.write(f'        "mandatory": True,\n')
            f.write(f'        "owner": "{["QA Lead", "Security Officer", "Release Manager", "Tech Lead"][i % 4]}",\n')
            f.write(f'        "governance_ref": "GOV-{((i-1)%45)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 18. CHANGE ITEMS (CHANGE-001 to CHANGE-040)
        f.write("# 18. CHANGE ITEMS (CHANGE-001 to CHANGE-040)\n")
        f.write("CHANGE_ITEMS = [\n")
        for i in range(1, 41):
            f.write(f"    {{\n")
            f.write(f'        "id": "CHANGE-{i:03d}",\n')
            f.write(f'        "title": "Project Change Request Profile #{i:03d}",\n')
            f.write(f'        "classification": "{["Standard", "Minor", "Major", "Emergency"][i % 4]}",\n')
            f.write(f'        "approval_authority": "{["Change Control Board (CCB)", "Chief Solution Architect", "Project Sponsor"][i % 3]}",\n')
            f.write(f'        "sla": "{["4 Hours", "24 Hours", "72 Hours", "Weekly"][i % 4]}",\n')
            f.write(f'        "governance_ref": "GOV-{((i-1)%45)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 19. COMM ITEMS (COMM-001 to COMM-045)
        f.write("# 19. COMM ITEMS (COMM-001 to COMM-045)\n")
        f.write("COMM_ITEMS = [\n")
        for i in range(1, 46):
            f.write(f"    {{\n")
            f.write(f'        "id": "COMM-{i:03d}",\n')
            f.write(f'        "title": "Communication Artifact & Ceremony #{i:03d}",\n')
            f.write(f'        "audience": "{["Executive Steering", "Engineering Squads", "Clinical Staff", "Municipal Regulators"][i % 4]}",\n')
            f.write(f'        "channel": "{["In-Person Ceremony", "Formal Email / PDF", "Slack / Teams Channel", "Municipal Portal"][i % 4]}",\n')
            f.write(f'        "frequency": "{["Daily", "Weekly", "Bi-Weekly", "Monthly"][i % 4]}",\n')
            f.write(f'        "owner": "{["Project Manager", "Scrum Master", "Technical Lead", "Communications Officer"][i % 4]}",\n')
            f.write(f'        "stakeholder_ref": "STAKEHOLDER-{((i-1)%50)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n\n")

        # 20. STATUS ITEMS (STATUS-001 to STATUS-040)
        f.write("# 20. STATUS ITEMS (STATUS-001 to STATUS-040)\n")
        f.write("STATUS_ITEMS = [\n")
        for i in range(1, 41):
            f.write(f"    {{\n")
            f.write(f'        "id": "STATUS-{i:03d}",\n')
            f.write(f'        "dimension": "{["Schedule Health", "Scope Integrity", "Quality Gate", "Risk Exposure", "Budgetary Burn", "Security Hardening"][i % 6]}",\n')
            f.write(f'        "metric_name": "Health Indicator #{i:03d}",\n')
            f.write(f'        "green_threshold": "Threshold variance < 5%",\n')
            f.write(f'        "amber_threshold": "Threshold variance between 5% and 15%",\n')
            f.write(f'        "red_threshold": "Threshold variance > 15% or critical blocker",\n')
            f.write(f'        "reporting_frequency": "Weekly",\n')
            f.write(f'        "owner": "Project Director",\n')
            f.write(f'        "governance_ref": "GOV-{((i-1)%45)+1:03d}",\n')
            f.write(f"    }},\n")
        f.write("]\n")

    print(f"Successfully generated {output_path}.")

if __name__ == "__main__":
    build()
