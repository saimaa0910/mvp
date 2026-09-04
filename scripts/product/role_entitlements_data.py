#!/usr/bin/env python3
"""
role_entitlements_data.py
Authoritative role entitlements, access matrices, and security governance rules
for the Namma Clinic Digital Health & Operations Platform (docs/04-product/).

Defines:
- 30 Roles (ROLE-001 to ROLE-030)
- 30 Modules (MODULE-001 to MODULE-030)
- Detailed 30x30 Role-Module Access Matrix (900 evaluated cells)
- Role-Feature & Capability Access Rules
- Privileged Operations & Maker-Checker Policies
- Separation of Duties (SoD) Invariants
- Emergency Break-Glass Authorization Protocols
- Offline Edge Operation Entitlements
- Administrative & Clinical Governance Approvals
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_specs import MODULE_SPECS

ROLES_CATALOG = [
    {
        "id": "ROLE-001",
        "title": "Project Executive Sponsor",
        "category": "Executive",
        "governance_level": "L5-Executive",
        "cadre": "Municipal IAS / Special Commissioner (Health)",
        "description": "BBMP Special Commissioner (Health) holding ultimate administrative, fiscal, and statutory authority across municipal clinic delivery.",
        "primary_focus": "Executive governance, fiscal allocations, statutory policy signoff, inter-agency coordination.",
        "clinical_authority": "Executive Oversight (No direct clinical prescribing)",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-002",
        "title": "Clinical Safety Authority",
        "category": "Clinical",
        "governance_level": "L5-Executive",
        "cadre": "Chief Health Officer (CHO) / Directorate of Health",
        "description": "Chief Health Officer (CHO) holding absolute statutory clinical safety sign-off, protocol veto, and clinical risk governance.",
        "primary_focus": "Clinical protocol ratification, CDSS AI guardrail verification, adverse event investigations, clinical veto.",
        "clinical_authority": "Absolute Clinical Safety Authority & Protocol Veto",
        "offline_eligible": False,
        "break_glass_eligible": True
    },
    {
        "id": "ROLE-003",
        "title": "Lead Delivery Partner / Project Director",
        "category": "Management",
        "governance_level": "L4-Product",
        "cadre": "Program Director / Consortium Lead",
        "description": "Delivery consortium director accountable for program milestones, multi-squad velocity, SLA adherence, and contract milestones.",
        "primary_focus": "Contractual delivery, cross-functional squad coordination, executive progress reporting, milestone signoffs.",
        "clinical_authority": "None",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-004",
        "title": "Chief Solution Architect",
        "category": "Architecture",
        "governance_level": "L3-Architecture",
        "cadre": "Principal Enterprise Systems Architect",
        "description": "Enterprise technical architect governing distributed topology, Fastify/PostgreSQL/DuckDB tech stack, edge mesh sync, and ABDM interfaces.",
        "primary_focus": "Technical architecture, integration schemas, offline conflict resolution policies, security architecture signoff.",
        "clinical_authority": "None",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-005",
        "title": "Delivery Project Manager / Agile Coach",
        "category": "Management",
        "governance_level": "L1-Operational",
        "cadre": "Scrum Master / Agile Delivery Manager",
        "description": "Operational delivery manager coordinating 18-sprint backlog, release train sprints, daily blockers, and squad velocity.",
        "primary_focus": "Sprint execution, sprint backlog readiness, impediment removal, release scheduling.",
        "clinical_authority": "None",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-006",
        "title": "Lead Backend Engineer",
        "category": "Engineering",
        "governance_level": "L2-Technical",
        "cadre": "Senior Staff Backend Engineer (Node/TypeScript)",
        "description": "Technical engineering lead responsible for Fastify microservices, GraphQL/REST APIs, Redis caches, and database query optimizations.",
        "primary_focus": "Backend services, API contracts, database transaction performance, microservice reliability.",
        "clinical_authority": "None",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-007",
        "title": "Lead Frontend Engineer",
        "category": "Engineering",
        "governance_level": "L2-Technical",
        "cadre": "Senior Staff Web/Mobile Engineer (React/Next.js)",
        "description": "Technical engineering lead responsible for Next.js PWA, local SQLite/IndexedDB caching, responsive UI components, and offline UX.",
        "primary_focus": "PWA client architecture, optimistic offline mutations, Kannada UI rendering, accessibility conformance.",
        "clinical_authority": "None",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-008",
        "title": "Lead Database Administrator (DBA)",
        "category": "Data",
        "governance_level": "L2-Technical",
        "cadre": "Principal Database Administrator (PostgreSQL/DuckDB)",
        "description": "Data tier custodian responsible for PostgreSQL schema migrations, WORM table immutability, backup replication, and DuckDB analytical rollups.",
        "primary_focus": "Database DDL/DML governance, index tuning, cryptographic WORM integrity, zero-loss replication.",
        "clinical_authority": "None",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-009",
        "title": "DevOps & SRE Lead",
        "category": "Infrastructure",
        "governance_level": "L2-Technical",
        "cadre": "Principal Site Reliability Engineer",
        "description": "Infrastructure lead managing Kubernetes clusters, edge container runtimes, automated CI/CD pipelines, Prometheus monitoring, and disaster recovery.",
        "primary_focus": "Cluster availability, edge device monitoring, automated telemetry, zero-downtime rolling upgrades.",
        "clinical_authority": "None",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-010",
        "title": "Quality Assurance Lead",
        "category": "Quality",
        "governance_level": "L2-Technical",
        "cadre": "Senior Test Automation Architect",
        "description": "Quality engineering lead governing end-to-end test automation, Playwright E2E suites, offline simulation testing, and release quality gates.",
        "primary_focus": "Automated regression suites, release gate verification, performance profiling, defect triage.",
        "clinical_authority": "None",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-011",
        "title": "Security & Data Privacy Officer",
        "category": "Security",
        "governance_level": "L3-Architecture",
        "cadre": "Chief Information Security Officer (CISO) / DPO",
        "description": "Statutory privacy and security officer governing DPDP Act 2023 compliance, cryptographic key lifecycles, ABAC policies, and threat audits.",
        "primary_focus": "DPDP compliance, vulnerability management, audit log forensic verification, patient privacy audits.",
        "clinical_authority": "Security Audit (No prescribing)",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-012",
        "title": "Clinical Safety Specialist (SME)",
        "category": "Clinical",
        "governance_level": "L3-Architecture",
        "cadre": "Public Health Medical Specialist",
        "description": "Clinical domain expert verifying clinical workflows, drug formulary interactions, ICD-10/SNOMED CT ontologies, and diagnostic guidelines.",
        "primary_focus": "Clinical rule definitions, drug-drug interaction alert thresholds, clinical safety case validation.",
        "clinical_authority": "Protocol Design & Clinical Rule Verification",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-013",
        "title": "Public Health Epidemiologist",
        "category": "Analytics",
        "governance_level": "L3-Architecture",
        "cadre": "Senior Epidemiologist / Health Data Scientist",
        "description": "Public health specialist analyzing syndromic disease trends, municipal outbreak clustering, vaccine coverage, and epidemiological surveillance.",
        "primary_focus": "Disease cluster detection, public health indicator surveillance, predictive syndromic models, HMIS analytics.",
        "clinical_authority": "Population Health Analytics",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-014",
        "title": "Frontline Training Coordinator",
        "category": "Operations",
        "governance_level": "L1-Operational",
        "cadre": "Clinical Operations Trainer",
        "description": "Operational coordinator managing frontline clinic staff onboarding, interactive simulator training, workflow certifications, and user adoption.",
        "primary_focus": "Staff simulation environments, competency assessments, training material curation, end-user feedback.",
        "clinical_authority": "Training Sandbox Operations",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-015",
        "title": "Zonal Clinic Medical Superintendent",
        "category": "Clinical",
        "governance_level": "L1-Operational",
        "cadre": "Senior Medical Officer (MBBS/MD) / Superintendent",
        "description": "Senior doctor and clinic in-charge conducting patient consultations, clinical examinations, e-prescribing, lab ordering, and medical supervision.",
        "primary_focus": "Outpatient clinical diagnosis, e-prescription generation, emergency resuscitation, secondary hospital referral signoff.",
        "clinical_authority": "Full Clinical Prescribing, Diagnosing & Emergency Break-Glass",
        "offline_eligible": True,
        "break_glass_eligible": True
    },
    {
        "id": "ROLE-016",
        "title": "Staff Nurse Supervisor",
        "category": "Clinical",
        "governance_level": "L1-Operational",
        "cadre": "Registered Staff Nurse (B.Sc / GNM)",
        "description": "Senior staff nurse leading vital signs triage, pediatric growth monitoring, danger sign identification, immunization, and emergency bedside care.",
        "primary_focus": "Vital signs measurement, triage acuity scoring, red-flag emergency alert triggers, cold chain logging.",
        "clinical_authority": "Clinical Triage, Vitals Recording, Nursing Administration",
        "offline_eligible": True,
        "break_glass_eligible": True
    },
    {
        "id": "ROLE-017",
        "title": "Chief Pharmacy Supervisor",
        "category": "Pharmacy",
        "governance_level": "L1-Operational",
        "cadre": "Registered Pharmacist (B.Pharm / D.Pharm)",
        "description": "Licensed pharmacist responsible for prescription verification, barcode-scanned medicine dispensing, patient counseling, and stock FEFO control.",
        "primary_focus": "Medication dispensing, 2D barcode batch verification, stock indenting, cold-chain medicine handling, expiry management.",
        "clinical_authority": "Medication Dispensing & Pharmacy Counseling (Strictly Cannot Prescribe)",
        "offline_eligible": True,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-018",
        "title": "Senior Laboratory Supervisor",
        "category": "Laboratory",
        "governance_level": "L1-Operational",
        "cadre": "Medical Laboratory Technologist (B.Sc MLT)",
        "description": "Certified laboratory technician performing rapid point-of-care diagnostic tests, sample processing, result entry, and panic-value escalation.",
        "primary_focus": "Specimen accessioning, diagnostic test processing, critical panic value alerting, laboratory equipment calibration.",
        "clinical_authority": "Diagnostic Test Execution & Result Entry (Cannot Prescribe)",
        "offline_eligible": True,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-019",
        "title": "Front Desk Operations Supervisor",
        "category": "Operations",
        "governance_level": "L1-Operational",
        "cadre": "Clinic Front Desk Coordinator / Receptionist",
        "description": "Frontline receptionist handling citizen intake, demographic data entry, ABHA verification, digital consent, and priority token minting.",
        "primary_focus": "Citizen registration, biometric/OTP ABHA onboarding, digital consent recording, token printing, waiting hall queue call.",
        "clinical_authority": "Non-Clinical Intake (No access to detailed clinical diagnoses)",
        "offline_eligible": True,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-020",
        "title": "Integration Gateway Specialist",
        "category": "Engineering",
        "governance_level": "L2-Technical",
        "cadre": "Integration Solutions Engineer",
        "description": "Technical specialist managing external gateways including ABDM M1/M2/M3 bridges, state HMIS API pipelines, and 108 emergency dispatch interfaces.",
        "primary_focus": "FHIR R4 bundle mapping, ABDM cryptographic token exchange, SMS/WhatsApp delivery webhooks, 108 CAD integration.",
        "clinical_authority": "None",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-021",
        "title": "Data Analytics Engineer",
        "category": "Data",
        "governance_level": "L2-Technical",
        "cadre": "Senior Analytics & Business Intelligence Engineer",
        "description": "Data engineer building DuckDB analytical cubes, municipal health indicators, facility census dashboards, and automated state reports.",
        "primary_focus": "Analytical pipelines, DuckDB columnar modeling, municipal KPI aggregation, operational reports.",
        "clinical_authority": "None (Anonymized data only)",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-022",
        "title": "UI/UX Accessibility Designer",
        "category": "Design",
        "governance_level": "L2-Technical",
        "cadre": "Lead Product Designer & Accessibility Specialist",
        "description": "User experience designer ensuring WCAG 2.1 AA compliance, Kannada localized typography, touch-first tablet interactions, and high-contrast styling.",
        "primary_focus": "Design system tokens, screen reader compatibility, Kannada translation layout fidelity, user workflow ergonomics.",
        "clinical_authority": "None",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-023",
        "title": "Tier-1/2 Helpdesk Coordinator",
        "category": "Support",
        "governance_level": "L1-Operational",
        "cadre": "IT Service Management Support Lead",
        "description": "Centralized IT helpdesk agent managing clinic incident tickets, password resets, hardware trouble tickets, and citizen grievance escalation.",
        "primary_focus": "Incident lifecycle management, clinic operational support, peripheral hardware ticketing, user assistance.",
        "clinical_authority": "None",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-024",
        "title": "Field Hardware Support Engineer",
        "category": "Support",
        "governance_level": "L1-Operational",
        "cadre": "Desktop & Peripheral Field Support Technician",
        "description": "On-site field hardware technician troubleshooting clinic mini-servers, thermal printers, barcode scanners, digital displays, and local LANs.",
        "primary_focus": "Peripheral repair, local edge node re-imaging, biometric scanner calibration, UPS power verification.",
        "clinical_authority": "None",
        "offline_eligible": True,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-025",
        "title": "Municipal Legal & Compliance Counsel",
        "category": "Compliance",
        "governance_level": "L4-Product",
        "cadre": "Legal Advisor / Municipal Data Protection Counsel",
        "description": "Municipal legal counsel governing DPDP Act statutory compliance, patient privacy notices, data disclosure requests, and regulatory contracts.",
        "primary_focus": "DPDP legal interpretation, data processing agreements, compliance audits, statutory regulatory filings.",
        "clinical_authority": "Legal Compliance Review (No clinical access)",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-026",
        "title": "Municipal Finance Auditor",
        "category": "Finance",
        "governance_level": "L4-Product",
        "cadre": "Senior Municipal Auditor / Fiscal Controller",
        "description": "Municipal finance auditor overseeing pharmaceutical stock reconciliation, physical inventory audit trails, procurement indents, and capital assets.",
        "primary_focus": "Stock valuation audits, drug write-off verifications, procurement ledger checks, financial transparency.",
        "clinical_authority": "Fiscal Inventory Audit (No patient PHI access)",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-027",
        "title": "Release Train Engineer",
        "category": "Management",
        "governance_level": "L2-Technical",
        "cadre": "Enterprise Release Manager",
        "description": "Release engineering manager orchestrating phased multi-clinic rollouts, feature flag deployments, canary testing, and release rollbacks.",
        "primary_focus": "Feature flag toggles, progressive delivery, release readiness reviews, operational deployment windows.",
        "clinical_authority": "None",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-028",
        "title": "Performance & Chaos Engineer",
        "category": "Quality",
        "governance_level": "L2-Technical",
        "cadre": "Site Reliability Performance Engineer",
        "description": "Specialized resilience engineer executing simulated network partitions, high-concurrency clinic load injection, and edge sync stress testing.",
        "primary_focus": "Chaos testing, network drop resilience, edge mesh sync recovery, high-load queue benchmarking.",
        "clinical_authority": "None",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-029",
        "title": "Kannada Localization Specialist",
        "category": "Content",
        "governance_level": "L1-Operational",
        "cadre": "Linguistic & Health Translation Specialist",
        "description": "Bilingual language specialist certifying Kannada medical terminology, citizen SMS templates, audio queue announcements, and UI strings.",
        "primary_focus": "Kannada string verification, medical terminology standardization, localized citizen communication, audio cue quality.",
        "clinical_authority": "Localization Content Certification",
        "offline_eligible": False,
        "break_glass_eligible": False
    },
    {
        "id": "ROLE-030",
        "title": "Documentation & Traceability Auditor",
        "category": "Governance",
        "governance_level": "L2-Technical",
        "cadre": "Systems Compliance & Quality Auditor",
        "description": "Governance auditor verifying cross-phase requirement traceability, architectural consistency, audit trail integrity, and documentation baselines.",
        "primary_focus": "Traceability matrix validation, specification consistency, statutory audit trail completeness, documentation verification.",
        "clinical_authority": "Governance Audit",
        "offline_eligible": False,
        "break_glass_eligible": False
    }
]

ROLE_MAP = {r["id"]: r for r in ROLES_CATALOG}

# -----------------------------------------------------------------------------
# MASTER ROLE-MODULE ACCESS RULES
# Matrix defining access level for every role across all 30 modules
# Access levels: NONE, VIEW, CREATE, EDIT, DELETE, APPROVE, EXECUTE, ADMIN, AUDIT
# -----------------------------------------------------------------------------

def get_role_module_access(role_id: str, mod_id: str) -> dict:
    """Computes exact access permissions for a given Role and Module."""
    # Default baseline permissions
    access = {
        "level": "NONE",
        "read": False,
        "create": False,
        "update": False,
        "delete": False,
        "approve": False,
        "reject": False,
        "dispense": False,
        "prescribe": False,
        "view_clinical": False,
        "view_reports": False,
        "export": False,
        "administer": False,
        "configure": False,
        "audit": False,
        "emergency_override": False,
        "offline_operation": False,
        "sync_authority": False,
        "abac_rule": "Default deny"
    }

    # 1. Executive Roles (ROLE-001, ROLE-003, ROLE-025, ROLE-026)
    if role_id == "ROLE-001":  # Project Executive Sponsor
        access["level"] = "AUDIT"
        access["read"] = True
        access["view_reports"] = True
        access["export"] = True
        access["audit"] = True
        access["approve"] = True
        access["abac_rule"] = "Municipal-wide executive view; masked patient PHI; full operational metrics"
        return access

    if role_id == "ROLE-003":  # Lead Delivery Partner
        access["level"] = "AUDIT"
        access["read"] = True
        access["view_reports"] = True
        access["audit"] = True
        access["abac_rule"] = "Project progress tracking across all modules; strictly no raw patient clinical data"
        return access

    if role_id == "ROLE-025":  # Legal & Compliance Counsel
        if mod_id in ["MODULE-007", "MODULE-021", "MODULE-025", "MODULE-020"]:
            access["level"] = "AUDIT"
            access["read"] = True
            access["audit"] = True
            access["export"] = True
            access["abac_rule"] = "Statutory compliance and consent ledger audit; DPDP legal audit authority"
        elif mod_id in ["MODULE-001", "MODULE-004", "MODULE-026"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["abac_rule"] = "Tenant governance and security posture audit"
        return access

    if role_id == "ROLE-026":  # Municipal Finance Auditor
        if mod_id in ["MODULE-013", "MODULE-014", "MODULE-015", "MODULE-016"]:
            access["level"] = "AUDIT"
            access["read"] = True
            access["audit"] = True
            access["view_reports"] = True
            access["export"] = True
            access["abac_rule"] = "Pharmacy inventory valuation and procurement ledger audit; no patient PHI access"
        elif mod_id in ["MODULE-021", "MODULE-022"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["view_reports"] = True
            access["abac_rule"] = "Financial transaction audit logs"
        return access

    # 2. Clinical Safety Authorities (ROLE-002, ROLE-012)
    if role_id in ["ROLE-002", "ROLE-012"]:
        if mod_id in ["MODULE-009", "MODULE-010", "MODULE-011", "MODULE-012", "MODULE-016", "MODULE-023", "MODULE-027", "MODULE-029"]:
            access["level"] = "APPROVE" if role_id == "ROLE-002" else "AUDIT"
            access["read"] = True
            access["approve"] = (role_id == "ROLE-002")
            access["reject"] = (role_id == "ROLE-002")
            access["view_clinical"] = True
            access["view_reports"] = True
            access["audit"] = True
            access["emergency_override"] = (role_id == "ROLE-002")
            access["abac_rule"] = "Clinical protocol governance, safety rule ratification, CDSS AI guardrails"
        elif mod_id in ["MODULE-013", "MODULE-017", "MODULE-018", "MODULE-022"]:
            access["level"] = "AUDIT"
            access["read"] = True
            access["view_clinical"] = True
            access["view_reports"] = True
            access["audit"] = True
            access["abac_rule"] = "Clinical safety monitoring, pharmacovigilance, referral safety"
        else:
            access["level"] = "VIEW"
            access["read"] = True
            access["abac_rule"] = "Platform governance view"
        return access

    # 3. Technical Platform / Engineering Cadre (ROLE-004, ROLE-006, ROLE-007, ROLE-008, ROLE-009, ROLE-027, ROLE-028)
    if role_id == "ROLE-004":  # Chief Solution Architect
        access["level"] = "ADMIN"
        access["read"] = True
        access["configure"] = True
        access["administer"] = True
        access["view_reports"] = True
        access["audit"] = True
        access["abac_rule"] = "Architectural configuration across all microservices; data tier zero-access to unmasked PHI"
        return access

    if role_id in ["ROLE-006", "ROLE-007"]:  # Lead Backend / Frontend Engineers
        if mod_id in ["MODULE-001", "MODULE-003", "MODULE-004", "MODULE-024", "MODULE-026"]:
            access["level"] = "EDIT"
            access["read"] = True
            access["update"] = True
            access["configure"] = True
            access["abac_rule"] = "Technical configuration in staging/dev; production access strictly via CI/CD"
        else:
            access["level"] = "VIEW"
            access["read"] = True
            access["abac_rule"] = "Service endpoint inspection; strictly synthetic or masked data"
        return access

    if role_id == "ROLE-008":  # Lead DBA
        if mod_id in ["MODULE-001", "MODULE-002", "MODULE-004", "MODULE-021", "MODULE-024", "MODULE-026"]:
            access["level"] = "ADMIN"
            access["read"] = True
            access["update"] = True
            access["administer"] = True
            access["audit"] = True
            access["abac_rule"] = "Database DDL/DML migrations; WORM append-only enforcement; no direct raw clinical DML"
        else:
            access["level"] = "VIEW"
            access["read"] = True
            access["abac_rule"] = "Database schema performance monitoring"
        return access

    if role_id == "ROLE-009":  # DevOps & SRE Lead
        if mod_id in ["MODULE-001", "MODULE-003", "MODULE-004", "MODULE-024", "MODULE-026", "MODULE-027"]:
            access["level"] = "ADMIN"
            access["read"] = True
            access["update"] = True
            access["configure"] = True
            access["administer"] = True
            access["audit"] = True
            access["sync_authority"] = True
            access["abac_rule"] = "Infrastructure orchestration, edge node deployment, telemetry ingestion"
        else:
            access["level"] = "VIEW"
            access["read"] = True
            access["abac_rule"] = "System health and cluster metric observation"
        return access

    if role_id == "ROLE-027":  # Release Train Engineer
        if mod_id in ["MODULE-003", "MODULE-026"]:
            access["level"] = "ADMIN"
            access["read"] = True
            access["update"] = True
            access["configure"] = True
            access["abac_rule"] = "Feature flag management and progressive canary release toggles"
        else:
            access["level"] = "VIEW"
            access["read"] = True
            access["view_reports"] = True
            access["abac_rule"] = "Release verification across all functional domains"
        return access

    if role_id == "ROLE-028":  # Performance & Chaos Engineer
        access["level"] = "EXECUTE"
        access["read"] = True
        access["execute"] = True
        access["abac_rule"] = "Synthetic load injection and resilience testing in non-prod / chaos windows"
        return access

    # 4. Security & Governance (ROLE-011, ROLE-030)
    if role_id == "ROLE-011":  # Security & Data Privacy Officer
        if mod_id in ["MODULE-001", "MODULE-004", "MODULE-007", "MODULE-021", "MODULE-026"]:
            access["level"] = "ADMIN"
            access["read"] = True
            access["update"] = True
            access["administer"] = True
            access["audit"] = True
            access["export"] = True
            access["abac_rule"] = "Cryptographic key rotation, ABAC privilege policy enforcement, DPDP audit"
        else:
            access["level"] = "AUDIT"
            access["read"] = True
            access["audit"] = True
            access["abac_rule"] = "Audit access to security logs, access traces, and consent transactions"
        return access

    if role_id == "ROLE-030":  # Documentation & Traceability Auditor
        access["level"] = "AUDIT"
        access["read"] = True
        access["audit"] = True
        access["abac_rule"] = "Documentation compliance and requirement traceability verification"
        return access

    # 5. Frontline Clinic Doctors - ROLE-015 (Zonal Clinic Medical Superintendent)
    if role_id == "ROLE-015":
        # Full clinical consultation, encounter documentation, prescribing, lab ordering
        if mod_id in ["MODULE-010", "MODULE-012", "MODULE-029"]:
            access["level"] = "CREATE"
            access["read"] = True
            access["create"] = True
            access["update"] = True
            access["prescribe"] = True
            access["view_clinical"] = True
            access["emergency_override"] = True
            access["offline_operation"] = True
            access["sync_authority"] = True
            access["abac_rule"] = "Active assigned clinic doctor; full consultation & e-prescribing; break-glass override"
        elif mod_id in ["MODULE-009", "MODULE-011"]:
            access["level"] = "EDIT"
            access["read"] = True
            access["create"] = True
            access["update"] = True
            access["view_clinical"] = True
            access["emergency_override"] = True
            access["offline_operation"] = True
            access["abac_rule"] = "Review triage vitals, order point-of-care laboratory tests"
        elif mod_id in ["MODULE-017", "MODULE-018", "MODULE-027"]:
            access["level"] = "CREATE"
            access["read"] = True
            access["create"] = True
            access["update"] = True
            access["view_clinical"] = True
            access["emergency_override"] = True
            access["offline_operation"] = True
            access["abac_rule"] = "Authorize secondary hospital referrals, manage chronic NCD care, adverse alerts"
        elif mod_id in ["MODULE-005", "MODULE-006", "MODULE-007", "MODULE-008", "MODULE-016", "MODULE-023"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["view_clinical"] = True
            access["offline_operation"] = True
            access["abac_rule"] = "View patient demographics, queue position, formulary, CDSS suggestions"
        elif mod_id in ["MODULE-013", "MODULE-014"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["offline_operation"] = True
            access["abac_rule"] = "View pharmacy dispensing status and clinic stock availability"
        elif mod_id in ["MODULE-024"]:
            access["level"] = "EXECUTE"
            access["read"] = True
            access["offline_operation"] = True
            access["sync_authority"] = True
            access["abac_rule"] = "Trigger manual emergency sync from doctor tablet to local edge"
        return access

    # 6. Frontline Clinic Nurses - ROLE-016 (Staff Nurse Supervisor)
    if role_id == "ROLE-016":
        if mod_id in ["MODULE-009"]:
            access["level"] = "CREATE"
            access["read"] = True
            access["create"] = True
            access["update"] = True
            access["view_clinical"] = True
            access["emergency_override"] = True
            access["offline_operation"] = True
            access["sync_authority"] = True
            access["abac_rule"] = "Record patient vital signs, assign triage category, broadcast red danger alert"
        elif mod_id in ["MODULE-005", "MODULE-007", "MODULE-008"]:
            access["level"] = "CREATE"
            access["read"] = True
            access["create"] = True
            access["update"] = True
            access["offline_operation"] = True
            access["abac_rule"] = "Assisted registration, nurse queue triage calling, consent capture"
        elif mod_id in ["MODULE-010", "MODULE-011", "MODULE-018", "MODULE-027"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["view_clinical"] = True
            access["offline_operation"] = True
            access["abac_rule"] = "View clinical encounters, collect lab samples, monitor chronic follow-up"
        elif mod_id in ["MODULE-014", "MODULE-015"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["abac_rule"] = "View vaccine and consumable stock levels"
        elif mod_id in ["MODULE-024"]:
            access["level"] = "EXECUTE"
            access["read"] = True
            access["offline_operation"] = True
            access["sync_authority"] = True
            access["abac_rule"] = "Nurse station edge cache synchronization"
        return access

    # 7. Clinic Pharmacist - ROLE-017 (Chief Pharmacy Supervisor)
    if role_id == "ROLE-017":
        if mod_id in ["MODULE-013"]:
            access["level"] = "EXECUTE"
            access["read"] = True
            access["update"] = True
            access["dispense"] = True
            access["offline_operation"] = True
            access["sync_authority"] = True
            access["abac_rule"] = "Scan 2D barcode, verify e-prescription, dispense medication, log patient counseling"
        elif mod_id in ["MODULE-014", "MODULE-015"]:
            access["level"] = "CREATE"
            access["read"] = True
            access["create"] = True
            access["update"] = True
            access["approve"] = True
            access["offline_operation"] = True
            access["abac_rule"] = "Manage batch FEFO stock, log physical counts, submit stock replenishment indents"
        elif mod_id in ["MODULE-012"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["view_clinical"] = True
            access["offline_operation"] = True
            access["abac_rule"] = "Read electronic prescription items; strictly NO prescribing or altering Rx"
        elif mod_id in ["MODULE-016"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["abac_rule"] = "View essential medicine list and formulary rules"
        elif mod_id in ["MODULE-005", "MODULE-008"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["offline_operation"] = True
            access["abac_rule"] = "View patient demographics and pharmacy queue position"
        elif mod_id in ["MODULE-024"]:
            access["level"] = "EXECUTE"
            access["read"] = True
            access["offline_operation"] = True
            access["sync_authority"] = True
            access["abac_rule"] = "Dispensary terminal offline sync"
        return access

    # 8. Clinic Lab Technician - ROLE-018 (Senior Laboratory Supervisor)
    if role_id == "ROLE-018":
        if mod_id in ["MODULE-011"]:
            access["level"] = "CREATE"
            access["read"] = True
            access["create"] = True
            access["update"] = True
            access["view_clinical"] = True
            access["offline_operation"] = True
            access["sync_authority"] = True
            access["abac_rule"] = "Accession lab specimen, enter test results, escalate panic values, reject samples"
        elif mod_id in ["MODULE-005", "MODULE-008"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["offline_operation"] = True
            access["abac_rule"] = "View patient demographics and lab queue"
        elif mod_id in ["MODULE-010"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["view_clinical"] = True
            access["abac_rule"] = "View diagnostic order context from doctor note"
        elif mod_id in ["MODULE-014"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["update"] = True
            access["abac_rule"] = "Track rapid test kit reagents and consumables"
        elif mod_id in ["MODULE-024"]:
            access["level"] = "EXECUTE"
            access["read"] = True
            access["offline_operation"] = True
            access["sync_authority"] = True
            access["abac_rule"] = "Lab station offline edge sync"
        return access

    # 9. Front Desk Clerk - ROLE-019 (Front Desk Operations Supervisor)
    if role_id == "ROLE-019":
        if mod_id in ["MODULE-005", "MODULE-006", "MODULE-007", "MODULE-008"]:
            access["level"] = "CREATE"
            access["read"] = True
            access["create"] = True
            access["update"] = True
            access["offline_operation"] = True
            access["sync_authority"] = True
            access["abac_rule"] = "Register citizen, link ABHA, record digital consent, mint queue token, print slip"
        elif mod_id in ["MODULE-020"]:
            access["level"] = "CREATE"
            access["read"] = True
            access["create"] = True
            access["abac_rule"] = "Log walk-in citizen feedback or grievance"
        elif mod_id in ["MODULE-024"]:
            access["level"] = "EXECUTE"
            access["read"] = True
            access["offline_operation"] = True
            access["sync_authority"] = True
            access["abac_rule"] = "Intake desk offline registration cache sync"
        return access

    # 10. Integration & Data Specialists (ROLE-013, ROLE-020, ROLE-021)
    if role_id == "ROLE-013":  # Public Health Epidemiologist
        if mod_id in ["MODULE-022", "MODULE-025"]:
            access["level"] = "AUDIT"
            access["read"] = True
            access["view_reports"] = True
            access["export"] = True
            access["audit"] = True
            access["abac_rule"] = "Execute municipal epidemiological queries and syndromic cluster analysis"
        elif mod_id in ["MODULE-009", "MODULE-010", "MODULE-011", "MODULE-018"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["view_reports"] = True
            access["abac_rule"] = "Anonymized aggregate health trends; no identifying citizen information"
        return access

    if role_id == "ROLE-020":  # Integration Gateway Specialist
        if mod_id in ["MODULE-006", "MODULE-017", "MODULE-019", "MODULE-020", "MODULE-025", "MODULE-030"]:
            access["level"] = "ADMIN"
            access["read"] = True
            access["update"] = True
            access["configure"] = True
            access["abac_rule"] = "Manage ABDM, 108 CAD, SMS gateway, and inter-facility integration webhooks"
        else:
            access["level"] = "VIEW"
            access["read"] = True
            access["abac_rule"] = "Integration health monitoring"
        return access

    if role_id == "ROLE-021":  # Data Analytics Engineer
        if mod_id in ["MODULE-021", "MODULE-022", "MODULE-025"]:
            access["level"] = "ADMIN"
            access["read"] = True
            access["update"] = True
            access["configure"] = True
            access["view_reports"] = True
            access["export"] = True
            access["abac_rule"] = "Build DuckDB analytics views, maintain aggregate data marts, generate reports"
        else:
            access["level"] = "VIEW"
            access["read"] = True
            access["view_reports"] = True
            access["abac_rule"] = "Aggregate reporting across all operational domains"
        return access

    # 11. Support & Operational Roles (ROLE-014, ROLE-022, ROLE-023, ROLE-024, ROLE-029)
    if role_id == "ROLE-014":  # Frontline Training Coordinator
        access["level"] = "VIEW"
        access["read"] = True
        access["abac_rule"] = "Sandbox and training simulation tenant view across workflows"
        return access

    if role_id == "ROLE-022":  # UI/UX Accessibility Designer
        if mod_id in ["MODULE-002", "MODULE-003", "MODULE-005", "MODULE-008", "MODULE-010", "MODULE-019"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["abac_rule"] = "Accessibility and UI component testing"
        return access

    if role_id == "ROLE-023":  # Tier-1/2 Helpdesk Coordinator
        if mod_id in ["MODULE-028", "MODULE-020"]:
            access["level"] = "CREATE"
            access["read"] = True
            access["create"] = True
            access["update"] = True
            access["abac_rule"] = "Create, route, and update facility helpdesk incident tickets and grievances"
        elif mod_id in ["MODULE-001", "MODULE-002", "MODULE-008"]:
            access["level"] = "VIEW"
            access["read"] = True
            access["abac_rule"] = "Check staff account status and clinic facility status to support users"
        return access

    if role_id == "ROLE-024":  # Field Hardware Support Engineer
        if mod_id in ["MODULE-024", "MODULE-028"]:
            access["level"] = "EXECUTE"
            access["read"] = True
            access["update"] = True
            access["execute"] = True
            access["offline_operation"] = True
            access["abac_rule"] = "Diagnose edge mini-server, calibrate thermal printers & barcode scanners"
        return access

    if role_id == "ROLE-029":  # Kannada Localization Specialist
        if mod_id in ["MODULE-003", "MODULE-008", "MODULE-016", "MODULE-019"]:
            access["level"] = "EDIT"
            access["read"] = True
            access["update"] = True
            access["approve"] = True
            access["abac_rule"] = "Translate and certify Kannada strings, citizen SMS notices, and audio cues"
        return access

    # 12. Management Roles (ROLE-005)
    if role_id == "ROLE-005":  # Delivery PM
        access["level"] = "VIEW"
        access["read"] = True
        access["view_reports"] = True
        access["abac_rule"] = "Sprint tracking and milestone verification across all modules"
        return access

    return access

# Precompute full 30x30 matrix
FULL_ROLE_MODULE_MATRIX = []
for r in ROLES_CATALOG:
    for i in range(1, 31):
        mid = f"MODULE-{i:03d}"
        perm = get_role_module_access(r["id"], mid)
        FULL_ROLE_MODULE_MATRIX.append({
            "role_id": r["id"],
            "role_title": r["title"],
            "module_id": mid,
            **perm
        })

# -----------------------------------------------------------------------------
# SEPARATION OF DUTIES (SoD) CONSTRAINTS
# Strict cryptographic and workflow barriers between conflicting roles
# -----------------------------------------------------------------------------
SOD_CONSTRAINTS = [
    {
        "id": "SOD-001",
        "title": "Prescriber vs Dispenser Separation",
        "conflicting_roles": ["ROLE-015 (Doctor)", "ROLE-017 (Pharmacist)"],
        "policy": "A Doctor who prescribes medication cannot dispense it; a Pharmacist dispensing medication cannot modify or create a prescription.",
        "enforcement": "Cryptographic role barrier; digital signature verification on prescription payload; dispensing API rejects caller if role is Prescriber.",
        "risk_mitigation": "Prevents prescription fraud, medication theft, and unauthorized drug distribution."
    },
    {
        "id": "SOD-002",
        "title": "Diagnostic Orderer vs Diagnostic Lab Signer",
        "conflicting_roles": ["ROLE-015 (Doctor)", "ROLE-018 (Lab Technician)"],
        "policy": "A Doctor ordering a laboratory investigation cannot enter or validate the lab test results; the Lab Technician cannot prescribe diagnostic orders.",
        "enforcement": "Specimen accessioning requires distinct MLT credential; doctor accounts blocked from lab result entry endpoints.",
        "risk_mitigation": "Prevents falsified diagnostic records, diagnostic collusion, and unverified clinical claims."
    },
    {
        "id": "SOD-003",
        "title": "Clinical Care Delivery vs Audit & Log Modification",
        "conflicting_roles": ["ROLE-015 / ROLE-016 / ROLE-017", "ROLE-011 / ROLE-025 / ROLE-030"],
        "policy": "Clinical personnel generating care records cannot access or modify audit logs; auditors cannot create or alter clinical records.",
        "enforcement": "Audit tables are write-once-read-many (WORM); HMAC digest signed by HSM; auditors have read-only audit schemas.",
        "risk_mitigation": "Ensures forensic immutability and prevents post-incident tampering with medical negligence evidence."
    },
    {
        "id": "SOD-004",
        "title": "Software Development vs Production Database DML",
        "conflicting_roles": ["ROLE-006 / ROLE-007 (Developers)", "ROLE-008 (Lead DBA)"],
        "policy": "Software engineers authoring application code have zero write access to production PostgreSQL tables; DBA executes schema migrations.",
        "enforcement": "Production database isolated in private VPC; access restricted to automated CI/CD pipeline service accounts and DBA jump host.",
        "risk_mitigation": "Prevents unauthorized database alterations, schema drift, and accidental production data corruption."
    },
    {
        "id": "SOD-005",
        "title": "Pharmacy Stock Custody vs Fiscal Stock Write-off Approval",
        "conflicting_roles": ["ROLE-017 (Pharmacist)", "ROLE-026 (Finance Auditor)"],
        "policy": "Pharmacists managing physical inventory cannot unilaterally approve financial write-offs for expired/damaged drugs above ₹5,000.",
        "enforcement": "Multi-tier maker-checker: Pharmacist flags damage/expiry; Municipal Finance Auditor and Medical Superintendent must co-sign write-off.",
        "risk_mitigation": "Prevents pilferage, inventory leakage, and intentional stock misclassification."
    },
    {
        "id": "SOD-006",
        "title": "User Account Administration vs Security Access Audit",
        "conflicting_roles": ["ROLE-001 / ROLE-026 (Admin)", "ROLE-011 (Security Officer)"],
        "policy": "System administrators provisioning user accounts and role assignments cannot approve security exception audits or alter security policies.",
        "enforcement": "Role provisioning logged to immutable WORM ledger; periodic IAM reconciliation executed by Security Officer.",
        "risk_mitigation": "Prevents shadow admin accounts, privilege creep, and unauthorized privilege escalation."
    }
]

# -----------------------------------------------------------------------------
# PRIVILEGED OPERATIONS & MAKER-CHECKER MATRIX
# Operations requiring step-up authentication, dual sign-off, or statutory break-glass
# -----------------------------------------------------------------------------
PRIVILEGED_OPERATIONS = [
    {
        "id": "PRIV-OP-001",
        "operation": "Emergency Clinical Break-Glass PHI Access",
        "module": "MODULE-007",
        "authorized_roles": ["ROLE-015 (Doctor)", "ROLE-016 (Nurse)"],
        "step_up_auth": "Aadhaar OTP / Supervisor Biometric + Clinical Reason",
        "dual_signoff": "No (Permitted for immediate resuscitation), requires post-hoc audit review within 24h by ROLE-002",
        "audit_level": "CRITICAL_WORM",
        "description": "Unrestricted emergency override to view longitudinal patient records for unconscious trauma patients without explicit digital consent."
    },
    {
        "id": "PRIV-OP-002",
        "operation": "High-Value Pharmaceutical Stock Write-Off (> ₹5,000)",
        "module": "MODULE-014",
        "authorized_roles": ["ROLE-017 (Maker)", "ROLE-026 (Checker)", "ROLE-015 (Co-Signer)"],
        "step_up_auth": "Digital Signature (PKI / USB Token)",
        "dual_signoff": "Yes - 3-tier maker-checker approval workflow",
        "audit_level": "FINANCIAL_AUDIT",
        "description": "De-commissioning of expired, contaminated, or temperature-damaged pharmaceutical batches."
    },
    {
        "id": "PRIV-OP-003",
        "operation": "Clinical Decision Support AI Rule Override",
        "module": "MODULE-023",
        "authorized_roles": ["ROLE-015 (Doctor)"],
        "step_up_auth": "Doctor Password Re-Authentication + Structured Clinical Justification",
        "dual_signoff": "No (Real-time clinical autonomy), logged for retrospective pharmacovigilance review by ROLE-012",
        "audit_level": "CLINICAL_SAFETY",
        "description": "Prescribing a drug despite CDSS Level-1 contraindication alert, citing specific clinical necessity."
    },
    {
        "id": "PRIV-OP-004",
        "operation": "Essential Drug List (EDL) Formulary De-Listing",
        "module": "MODULE-016",
        "authorized_roles": ["ROLE-012 (Initiator)", "ROLE-002 (Approver)"],
        "step_up_auth": "MFA Push / Hardware Security Key",
        "dual_signoff": "Yes - Clinical Safety Authority formal signoff",
        "audit_level": "STATUTORY_POLICY",
        "description": "Removing a pharmaceutical molecule from the municipal formulary due to national drug alerts or supply recalls."
    },
    {
        "id": "PRIV-OP-005",
        "operation": "Emergency Edge Node Mesh Disaster Recovery Re-Sync",
        "module": "MODULE-024",
        "authorized_roles": ["ROLE-009 (DevOps Lead)", "ROLE-024 (Field Engineer)"],
        "step_up_auth": "SSH Ed25519 Hardware Token + Municipal Jump Host MFA",
        "dual_signoff": "Yes - Architect (ROLE-004) or SRE Lead authorization",
        "audit_level": "INFRASTRUCTURE",
        "description": "Forced authoritative reconciliation of divergent local edge database partitions following catastrophic multi-day offline network partition."
    },
    {
        "id": "PRIV-OP-006",
        "operation": "Staff Role Elevation & Administrative Privilege Grant",
        "module": "MODULE-001",
        "authorized_roles": ["ROLE-001 (Sponsor)", "ROLE-011 (Security Officer)"],
        "step_up_auth": "FIDO2 / Hardware WebAuthn Key + Government SSO",
        "dual_signoff": "Yes - Maker-checker required for any tier L3+ privilege elevation",
        "audit_level": "SECURITY_CRITICAL",
        "description": "Assigning Clinical Superintendent, DBA, or Security Officer privileges to user accounts."
    }
]

# -----------------------------------------------------------------------------
# OFFLINE & SYNCHRONIZATION AUTHORITY RULES
# -----------------------------------------------------------------------------
OFFLINE_GOVERNANCE = [
    {
        "role_id": "ROLE-015",
        "role_name": "Doctor (Medical Superintendent)",
        "offline_capabilities": ["Consultation Note Entry", "e-Prescribing", "Point-of-Care Lab Ordering", "Emergency Break-Glass", "Local Sync Trigger"],
        "offline_restrictions": "Cannot modify formulary rules; cannot access external ABDM federated records not pre-cached.",
        "max_offline_duration_hours": 72,
        "conflict_resolution_priority": 1  # Highest clinical priority in vector clock reconciliation
    },
    {
        "role_id": "ROLE-016",
        "role_name": "Staff Nurse Supervisor",
        "offline_capabilities": ["Vital Signs Recording", "Triage Scoring", "Queue Call Next", "Emergency Alarm Broadcast"],
        "offline_restrictions": "Cannot discharge or finalize doctor consultation.",
        "max_offline_duration_hours": 72,
        "conflict_resolution_priority": 2
    },
    {
        "role_id": "ROLE-017",
        "role_name": "Pharmacist",
        "offline_capabilities": ["Barcode Scan Dispensing", "Local Batch Stock Deduction", "Physical Stock Tally"],
        "offline_restrictions": "Cannot transfer stock between clinics; cannot approve financial write-offs.",
        "max_offline_duration_hours": 72,
        "conflict_resolution_priority": 3
    },
    {
        "role_id": "ROLE-018",
        "role_name": "Lab Technician",
        "offline_capabilities": ["Specimen Accessioning", "Rapid Test Result Entry", "Local Panic Alert"],
        "offline_restrictions": "Cannot order tests; cannot alter reference normal ranges.",
        "max_offline_duration_hours": 72,
        "conflict_resolution_priority": 3
    },
    {
        "role_id": "ROLE-019",
        "role_name": "Front Desk Receptionist",
        "offline_capabilities": ["Offline Patient Registration", "Local Token Minting", "Emergency Paper Consent", "Local Queue Calling"],
        "offline_restrictions": "ABHA OTP verification deferred; biometric online deduplication queued for cloud sync.",
        "max_offline_duration_hours": 72,
        "conflict_resolution_priority": 4
    }
]

if __name__ == "__main__":
    print(f"Role Entitlements Data Loaded: {len(ROLES_CATALOG)} roles")
    print(f"Total Role-Module Matrix Cells: {len(FULL_ROLE_MODULE_MATRIX)} (30x30)")
    print(f"Separation of Duties Constraints: {len(SOD_CONSTRAINTS)}")
    print(f"Privileged Operations Defined: {len(PRIVILEGED_OPERATIONS)}")
    print(f"Offline Governance Cadres: {len(OFFLINE_GOVERNANCE)}")
