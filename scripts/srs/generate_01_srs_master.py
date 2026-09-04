"""
generate_01_srs_master.py
Generates the comprehensive enterprise Software Requirements Specification (SRS)
for the Namma Clinic Digital Health & Operations Platform:
  docs/05-srs/01-srs-master.md

Conforms strictly to IEEE 830 / ISO/IEC/IEEE 29148 standards,
covering all 51 mandatory sections and exceeding 2,000+ substantive lines.
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines
from scripts.srs.srs_data import (
    ALL_FUNCTIONAL_REQUIREMENTS,
    ALL_NON_FUNCTIONAL_REQUIREMENTS,
    ALL_SECURITY_REQUIREMENTS,
    ALL_PRIVACY_REQUIREMENTS,
    ALL_CLINICAL_REQUIREMENTS,
    ALL_OPERATIONAL_REQUIREMENTS,
    ALL_OFFLINE_REQUIREMENTS,
    ALL_INTEGRATION_REQUIREMENTS,
    ALL_DATA_REQUIREMENTS,
    ALL_UI_REQUIREMENTS,
    TOTAL_SRS_REQUIREMENTS
)

OUTPUT_FILE = PROJECT_ROOT / "docs" / "05-srs" / "01-srs-master.md"

def generate_srs_master():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = []

    def p(text: str = ""):
        lines.append(text)

    # Title & Document Header
    p("# 📑 Master Software Requirements Specification (SRS)")
    p("## Namma Clinic Digital Health & Operations Platform")
    p("### Greater Bengaluru Authority (GBA) / BBMP Health Department")
    p("**Standard:** IEEE Std 830-1998 / ISO/IEC/IEEE 29148:2018 | **Status:** APPROVED BASELINE | **Document Code:** `SRS-MST-01`")
    p("")
    p("---")
    p("")

    # Section 01: Document Control
    p("## 01. Document Control & Administrative Metadata")
    p("This document establishes the authoritative, binding Software Requirements Specification (SRS) for the Namma Clinic Digital Health & Operations Platform across 183 primary health clinics in Bengaluru.")
    p("")
    p("| Metadata Property | Specification Value |")
    p("| :--- | :--- |")
    p("| **Project Name** | Namma Clinic Digital Health & Operations Platform |")
    p("| **Governing Municipal Body** | Greater Bengaluru Authority (GBA) / Bruhat Bengaluru Mahanagara Palike (BBMP) |")
    p("| **System Classification** | Critical Public Healthcare Digital Infrastructure |")
    p("| **Document Identifier** | `SRS-MST-01` |")
    p("| **Version** | 1.0.0-PROD-BASE |")
    p("| **Effective Date** | September 2026 |")
    p("| **Approval Authority** | Chief Medical Officer (`ROLE-012`) & Enterprise Architecture Board (`ROLE-003`) |")
    p("| **Security Classification** | RESTRICTED - MUNICIPAL HEALTHCARE GOVERNANCE |")
    p("| **Statutory Basis** | Karnataka Municipal Corporations Act 1976 & DPDP Act 2023 |")
    p("")

    # Section 02: Revision History
    p("## 02. Document Revision History")
    p("Chronological record of formal revisions, baseline reviews, and engineering change requests:")
    p("")
    p("| Version | Date | Author / Role | Summary of Changes | Ratification Status |")
    p("| :---: | :---: | :--- | :--- | :---: |")
    p("| `0.1.0` | July 2026 | Lead Architect (`ROLE-003`) | Initial draft decomposition and SRS scope framing | Draft |")
    p("| `0.5.0` | August 2026 | Lead Product Manager (`ROLE-001`) | Integration of 60 functional specifications and BDD criteria | Review |")
    p("| `0.9.0` | August 2026 | Clinical Safety Lead (`ROLE-002`) | Incorporation of 20 clinical safety guardrails and MEWS rules | Review |")
    p("| `1.0.0` | September 2026 | Enterprise Architecture Board | Final comprehensive baseline ratification across 51 sections | **APPROVED** |")
    p("")

    # Section 03: Purpose
    p("## 03. Purpose & System Intent")
    p("The purpose of this Software Requirements Specification is to establish the definitive, implementation-ready contract governing the functional capabilities, non-functional performance boundaries, clinical decision-support guardrails, and architectural invariants for the Namma Clinic Platform.")
    p("It serves as the authoritative specification for frontend, backend, data, DevOps, QA, security, and municipal public health engineering teams.")
    p("")

    # Section 04: Intended Audience
    p("## 04. Intended Audience & Stakeholder Responsibilities")
    p("The intended audience and their respective governance responsibilities regarding this specification:")
    p("")
    p("| Stakeholder Class | Role Identifier | Operational Responsibility | Utilization of this SRS |")
    p("| :--- | :---: | :--- | :--- |")
    p("| **Executive Municipal Leadership** | `ROLE-012`, `ROLE-019` | Program governance and healthcare delivery oversight | Scope verification and statutory compliance validation |")
    p("| **Software Engineering Teams** | `ROLE-006`, `ROLE-007` | Modular service and user journey implementation | Unambiguous contract for API, UI, and data domain development |")
    p("| **Quality Assurance & Testing** | `ROLE-005` | Test harness and automated test suite creation | Authoritative criteria for Gherkin BDD scenario test suites |")
    p("| **Clinical Governance Board** | `ROLE-002`, `ROLE-015` | Patient safety and treatment protocol auditing | Verification of drug guardrails, allergy alerts, and MEWS triage |")
    p("| **Cybersecurity & Privacy Cell** | `ROLE-011` | Threat defense, encryption, and DPDP Act compliance | Verification of RBAC boundaries, WORM audit, and PHI protection |")
    p("")

    # Section 05: Product Overview
    p("## 05. Product Overview & Architectural Context")
    p("The Namma Clinic Digital Health & Operations Platform is a modern, modular, cloud-native, offline-first digital primary healthcare solution specifically engineered for the 183 urban Namma Clinics operating across Greater Bengaluru.")
    p("It automates the full patient care lifecycle: front-desk biometric/demographic intake, ABHA digital health ID creation, multi-room priority queueing, nursing triage vitals, doctor clinical EMR, electronic prescribing with interaction checks, 2D barcode batch pharmacy dispensing, point-of-care lab diagnostics, secondary referrals, and real-time syndromic disease surveillance.")
    p("")

    # Section 06: Business Context
    p("## 06. Business Context & Municipal Health Mandate")
    p("BBMP and GBA established the Namma Clinic initiative to provide high-quality, free, accessible primary healthcare within a 15-minute walking radius for urban vulnerable populations (slum residents, daily-wage laborers, migrant workers, elderly citizens).")
    p("The digital platform replaces error-prone physical paper registers with a deterministic electronic workflow that operates continuously even during frequent urban broadband disruptions.")
    p("")

    # Section 07: System Objectives
    p("## 07. Core System Objectives (Key Performance Targets)")
    p("Quantitative system performance and public health objectives:")
    p("")
    p("| Objective ID | Strategic Goal | Metric / Benchmark Target | Upstream Ref |")
    p("| :--- | :--- | :--- | :---: |")
    p("| `OBJ-01` | Frontline Intake Velocity | Patient demographic intake < 45 seconds per citizen | `OBJECTIVE-001` |")
    p("| `OBJ-02` | Rapid Outpatient Encounter | Complete doctor clinical SOAP consultation < 90 seconds | `OBJECTIVE-002` |")
    p("| `OBJ-03` | Pharmacy Dispensation Safety | 100% 2D barcode verification of dispensed medication batches | `OBJECTIVE-003` |")
    p("| `OBJ-04` | Autonomous Offline Resilience | 72 hours continuous operation during total broadband disconnection | `OBJECTIVE-004` |")
    p("| `OBJ-05` | National Health Grid Integration | 100% ABDM M1/M2/M3 FHIR R4 compliance for consenting citizens | `OBJECTIVE-005` |")
    p("| `OBJ-06` | Outbreak Syndromic Detection | Automated cluster alerts dispatched within 120 minutes of detection | `OBJECTIVE-006` |")
    p("")

    # Section 08: Scope
    p("## 08. System Scope & Functional Boundaries")
    p("The scope of this platform encompasses all clinical, pharmaceutical, diagnostic, operational, and reporting workflows within the 183 municipal primary health clinics.")
    p("It integrates with state central drug warehouses, emergency 108 ambulance dispatch, secondary referral hospitals, and national ABDM registries.")
    p("")

    # Section 09: In-Scope Capabilities
    p("## 09. In-Scope Functional Capabilities (30 Modules)")
    p("Summary of all 30 foundational modules officially in-scope across the 6 platform domains:")
    p("")
    p("| Domain ID | Domain Name | Module Scope | Total Capabilities | Total Features |")
    p("| :---: | :--- | :--- | :---: | :---: |")
    p("| `DOMAIN-01` | Identity, Governance & Core Foundation | `MODULE-001` to `MODULE-006` | 36 | 36 |")
    p("| `DOMAIN-02` | Patient Intake, Queue & Triage | `MODULE-007` to `MODULE-012` | 36 | 36 |")
    p("| `DOMAIN-03` | Clinical Encounters & Diagnostics | `MODULE-013` to `MODULE-018` | 36 | 36 |")
    p("| `DOMAIN-04` | Pharmacy & Supply Chain Logistics | `MODULE-019` to `MODULE-022` | 24 | 24 |")
    p("| `DOMAIN-05` | Citizen Engagement & Community Outreach | `MODULE-023` to `MODULE-026` | 24 | 24 |")
    p("| `DOMAIN-06` | Enterprise Core, Intelligence & Interoperability | `MODULE-027` to `MODULE-030` | 24 | 24 |")
    p("| **TOTAL** | **6 Municipal Health Domains** | **30 Operational Modules** | **180** | **180** |")
    p("")

    # Section 10: Out-of-Scope Capabilities
    p("## 10. Explicitly Out-of-Scope Capabilities")
    p("The following domains are explicitly excluded from the Namma Clinic Platform scope to preserve primary-care operational focus:")
    p("")
    p("| Excluded Domain | Justification & Architectural Boundary | External Referral System |")
    p("| :--- | :--- | :--- |")
    p("| **Inpatient Bed Management** | Primary clinics have zero overnight admission beds | Secondary & Tertiary BBMP Hospitals |")
    p("| **Complex Surgical Suites (OT)** | Only minor first-aid suturing and wound dressing permitted | eHospital OT Management Systems |")
    p("| **Advanced Tertiary Imaging (CT/MRI)** | Clinic diagnostics limited to 58 point-of-care rapid tests | Victoria / Bowring Diagnostic Centers |")
    p("| **Organ Transplant Coordination** | Tertiary specialized mandate outside primary health purview | State Organ Sharing Registry (SOTTO) |")
    p("| **Autonomous Robotic Dispensing** | Dispensing executed manually by certified staff pharmacists | State Medical Automation Labs |")
    p("")

    # Section 11: Product Boundaries
    p("## 11. Product & System Scope Boundaries")
    p("The platform operates at the primary healthcare tier of the municipal health hierarchy:")
    p("")
    p("```mermaid")
    p("graph TD")
    p("    CITIZEN[\"Citizen / Patient\"] --> INT[\"Namma Clinic Reception Desk\"]")
    p("    INT --> TRIAGE[\"Nursing Triage (MEWS)\"]")
    p("    TRIAGE --> DOC[\"Doctor Consultation (SOAP EMR)\"]")
    p("    DOC --> LAB[\"Point-of-Care Lab (58 RDTs)\"]")
    p("    DOC --> PHARM[\"Pharmacy Dispensing (FEFO/Barcode)\"]")
    p("    DOC --> REF[\"Secondary Referral (108 EMS)\"]")
    p("    PHARM --> HOME[\"Citizen Returns Home with Prescribed Meds\"]")
    p("    REF --> HOSP[\"BBMP / State Tertiary Hospital\"]")
    p("```")
    p("")

    # Section 12: System Context
    p("## 12. External System Context Model")
    p("The Namma Clinic platform interfaces with external public, state, and national infrastructure entities:")
    p("- **ABDM / NHA Gateway:** M1 ABHA linking, M2 Care Context publishing, M3 Consent Management.")
    p("- **GVK-EMRI 108 Dispatch:** Direct API bridge for emergency ambulance summoning.")
    p("- **State Central Drug Logistics (KDLWS):** Indents, stock receipts, and formulary updates.")
    p("- **Karnataka State SMS Gateway (KSSD):** Citizen appointment and chronic care recall dispatch.")
    p("- **IDSP / IHIP:** Automated syndromic fever and infectious disease reporting.")
    p("")

    # Section 13: Stakeholders
    p("## 13. Stakeholder Ecosystem Classification")
    p("Mapping of municipal, administrative, and clinical stakeholders governed by this SRS:")
    p("")
    p("| Stakeholder Code | Stakeholder Title | Primary Interest | Authority Level |")
    p("| :--- | :--- | :--- | :---: |")
    p("| `STAKEHOLDER-001` | GBA / BBMP Central Health Directorate | Municipal health equity and clinical operational oversight | Executive |")
    p("| `STAKEHOLDER-002` | Medical Officers (Clinic Doctors) | Rapid, unencumbered clinical EMR and prescribing | Operational Lead |")
    p("| `STAKEHOLDER-003` | Clinic Nursing & Paramedical Staff | Objective triage screening and accurate queue management | Operational Staff |")
    p("| `STAKEHOLDER-004` | Registered Pharmacists | Accurate inventory ledger and zero dispensing errors | Operational Staff |")
    p("| `STAKEHOLDER-005` | Urban Citizen Community | Dignified, rapid, free healthcare without queue touting | End Beneficiary |")
    p("")

    # Section 14: User Classes
    p("## 14. User Classes & Operational Characteristics")
    p("Three primary user classes interact with the system:")
    p("1. **Frontline Clinic Clinical Operators:** High-frequency, touch-optimized users demanding < 200ms screen responses under intense queue pressure.")
    p("2. **Zonal Administrative Supervisors:** Dashboard and analytical consumers inspecting epidemiological trends and stock burn-down rates.")
    p("3. **Public Citizens & Caregivers:** Casual users accessing bilingual SMS/WhatsApp alerts, thermal slips, and the self-service kiosk.")
    p("")

    # Section 15: Personas
    p("## 15. Standardized Persona Profiles")
    p("Eight representative user personas driving user journey ergonomics:")
    p("- `PERSONA-001`: Front Desk Nurse / ANM (Intake, phonetic search, token printing)")
    p("- `PERSONA-002`: Triage Staff Nurse (Vitals recording, MEWS scoring, danger sign alerts)")
    p("- `PERSONA-003`: Medical Officer / Doctor (Consultation, SOAP documentation, prescribing)")
    p("- `PERSONA-004`: Clinic Pharmacist (Prescription dispensing, FEFO batch selection, scanning)")
    p("- `PERSONA-005`: Lab Technician (Sample logging, RDT testing, panic value reporting)")
    p("- `PERSONA-006`: ASHA Field Health Worker (Ward tracking, chronic defaulter tracing)")
    p("- `PERSONA-007`: SRE / Field IT Support Engineer (Edge appliances, sync verification, backups)")
    p("- `PERSONA-008`: Chief Medical Officer / Medical Superintendent (Clinical audit, de-duplication approval)")
    p("")

    # Section 16: Roles
    p("## 16. Role Master Catalog (30 Enterprise Roles)")
    p("The 30 enterprise roles (`ROLE-001` to `ROLE-030`) defined in the Master Role Catalog are bound to system entitlements:")
    p("")
    p("| Role ID | Role Name | Operational Tier | Mandatory Training Required |")
    p("| :---: | :--- | :--- | :---: |")
    p("| `ROLE-001` | Lead Product Manager | Product Governance | Standard |")
    p("| `ROLE-002` | Clinical Safety Lead | Clinical Governance | Bioethics & Safety |")
    p("| `ROLE-003` | Lead Solution Architect | Engineering Governance | Enterprise Architecture |")
    p("| `ROLE-006` | Lead Backend Engineer | Platform Engineering | Cryptography & API Security |")
    p("| `ROLE-007` | Lead Frontend Engineer | Client Engineering | PWA & Accessibility |")
    p("| `ROLE-008` | Lead Database Administrator | Data Governance | PostgreSQL & WAL Tuning |")
    p("| `ROLE-009` | Site Reliability Engineer (SRE) | Operations Governance | Disaster Recovery & Observability |")
    p("| `ROLE-010` | Lead DevOps Engineer | Infrastructure | Kubernetes & Edge Provisioning |")
    p("| `ROLE-011` | Chief Information Security Officer (CISO) | Cyber Defense | DPDP Act & Zero-Trust |")
    p("| `ROLE-012` | Chief Medical Officer (CMO) | Clinical Leadership | Public Health Administration |")
    p("| `ROLE-015` | Medical Officer (Clinic Doctor) | Frontline Practice | Clinical EMR & Formulary CDSS |")
    p("| `ROLE-016` | Staff Nurse / ANM | Frontline Practice | Nursing Triage & Intake |")
    p("| `ROLE-017` | Clinic Pharmacist | Frontline Practice | 2D Barcode & FEFO Logistics |")
    p("| `ROLE-018` | Laboratory Technician | Frontline Practice | Point-of-Care Diagnostics |")
    p("| `ROLE-020` | Field Health Worker (ASHA) | Community Outreach | Mobile Ward Tracking |")
    p("| `ROLE-030` | External Regulatory Auditor | Independent Audit | WORM Audit Verification |")
    p("")

    # Section 17: Permissions
    p("## 17. Permission Envelopes & Segregation of Duties (SoD)")
    p("The platform enforces 5 granular permission envelopes: `ADMIN`, `WRITE`, `EXECUTE`, `READ_ONLY`, and `NO_ACCESS` across all 900 role-module intersections.")
    p("Six mandatory Segregation of Duties (SoD) conflict rules (`SOD-001` to `SOD-006`) are hardcoded into the API gateway, preventing any user from simultaneously possessing prescriber and dispenser roles, or administrative and audit roles.")
    p("")

    # Section 18: Business Requirements
    p("## 18. Upstream Business Requirements Traceability")
    p("All SRS specifications directly fulfill the 30 core Business Requirements established in `docs/02-requirements/01-business-requirements.md` (`BR-001` to `BR-030`).")
    p("")

    # Section 19: Functional Requirements (60 Detailed Specifications)
    p("## 19. Detailed Functional Requirements Specification (SRS-FR-001 to SRS-FR-060)")
    p("Exhaustive, implementation-ready engineering specifications for all 60 Functional Requirements:")
    p("")

    for fr in ALL_FUNCTIONAL_REQUIREMENTS:
        p(f"### {fr['id']}: {fr['title']}")
        p(f"**Domain Category:** {fr['category']} | **Priority:** **{fr['priority']}** | **Upstream:** `{', '.join(fr['upstream_refs'])}`")
        p("")
        p(f"**Description:** {fr['description']}")
        p("")
        p(f"- **Business Rationale:** {fr['rationale']}")
        p(f"- **Primary Persona & Role:** {fr['persona']} | `{fr['role']}`")
        p(f"- **Preconditions:** {fr['preconditions']}")
        p(f"- **System Trigger:** {fr['trigger']}")
        p("")
        p("**Standard Operational Flow (Main Journey):**")
        for step_idx, step in enumerate(fr['main_flow'], start=1):
            p(f"  {step_idx}. {step}")
        p("")
        p("**Alternative Workflow Paths:**")
        for alt in fr['alt_flow']:
            p(f"  - {alt}")
        p("")
        p("**Exception & Failure Scenarios:**")
        for exc in fr['exception_flow']:
            p(f"  - {exc}")
        p("")
        p("**Governance & Impact Assessment:**")
        p(f"- **Business Rules:** {', '.join(fr['business_rules'])}")
        p(f"- **Validation Constraints:** {', '.join(fr['validation_rules'])}")
        p(f"- **Security Impact:** {fr['security_impact']}")
        p(f"- **Privacy Impact:** {fr['privacy_impact']}")
        p(f"- **Data Layer Impact:** {fr['data_impact']}")
        p(f"- **Performance Boundary:** {fr['performance_impact']}")
        p(f"- **Offline & Edge Resilience:** {fr['offline_impact']}")
        p(f"- **Bilingual Localization:** {fr['localization_impact']}")
        p(f"- **Accessibility:** {fr['accessibility_impact']}")
        p(f"- **External Interoperability:** {fr['integration_impact']}")
        p(f"- **Audit Trail Emission:** {fr['audit_impact']}")
        p("")
        p("**Executable Acceptance Criteria (BDD Given / When / Then):**")
        p(f"> {fr['acceptance_criteria']}")
        p("")
        p("```gherkin")
        for bdd_line in fr['bdd_scenario']:
            p(bdd_line)
        p("```")
        p("")
        p(f"**Verification Method:** `{fr['verification_method']}`")
        p(f"**Downstream Planned Artifacts:** `{', '.join(fr['downstream_artifacts'])}`")
        p("")
        p("---")
        p("")

    # Section 20: Non-Functional Requirements (40 Detailed Specifications)
    p("## 20. Detailed Non-Functional Requirements Specification (SRS-NFR-001 to SRS-NFR-040)")
    p("Exhaustive specifications for all 40 system quality attributes:")
    p("")

    for nfr in ALL_NON_FUNCTIONAL_REQUIREMENTS:
        p(f"### {nfr['id']}: {nfr['title']}")
        p(f"**Category:** {nfr['category']} | **Priority:** **{nfr['priority']}** (`{nfr['priority_code']}`) | **Upstream:** `{nfr['upstream_ref']}`")
        p("")
        p(f"**Specification Statement:** {nfr['description']}")
        p("")
        p(f"- **Engineering Rationale:** {nfr['rationale']}")
        p(f"- **Target Benchmark / Metric:** `{nfr['target_metric']}`")
        p(f"- **Measurement Method:** {nfr['measurement_method']}")
        p(f"- **Acceptance Quality Gate:** `{nfr['verification_gate']}`")
        p("")
        p("**Executable BDD Scenario:**")
        p("```gherkin")
        for line in nfr['bdd_scenario']:
            p(line)
        p("```")
        p("")
        p(f"**Downstream Planned Artifacts:** `{', '.join(nfr['downstream_artifacts'])}`")
        p("")
        p("---")
        p("")

    # Section 21: Clinical Requirements (20 Specifications)
    p("## 21. Clinical Safety & Decision Support Requirements (SRS-CR-001 to SRS-CR-020)")
    p("Enforces clinical safety boundaries, pediatric dose checking, drug-drug interaction alarms, and emergency break-glass protocols:")
    p("")
    p("| Req ID | Clinical Safety Requirement | Clinical Boundary Rule | Target Upstream | Priority | Verification Gate |")
    p("| :---: | :--- | :--- | :---: | :---: | :---: |")
    for cr in ALL_CLINICAL_REQUIREMENTS:
        p(f"| `{cr['id']}` | **{cr['title']}** | {cr['description']} | `{cr['upstream_ref']}` | {cr['priority']} | `{cr['verification_method']}` |")
    p("")

    # Section 22: Operational Requirements (20 Specifications)
    p("## 22. Operational Clinic Day Requirements (SRS-OR-001 to SRS-OR-020)")
    p("Facility management standards covering cold-boot pre-flight verification, inventory tallying, power failure cutover, and session roll-over:")
    p("")
    p("| Req ID | Operational Requirement | Facility Standard Operating Procedure | Target Upstream | Priority | Verification Gate |")
    p("| :---: | :--- | :--- | :---: | :---: | :---: |")
    for or_req in ALL_OPERATIONAL_REQUIREMENTS:
        p(f"| `{or_req['id']}` | **{or_req['title']}** | {or_req['description']} | `{or_req['upstream_ref']}` | {or_req['priority']} | `{or_req['verification_method']}` |")
    p("")

    # Section 23: Security Requirements (30 Specifications)
    p("## 23. Information Security & Zero-Trust Architecture (SRS-SEC-001 to SRS-SEC-030)")
    p("Cryptographic controls, authentication boundaries, rate limiting, and tamper-resistant WORM logging:")
    p("")
    p("| Req ID | Security Requirement | Technical Security Invariant | Target Upstream | Priority | Verification Gate |")
    p("| :---: | :--- | :--- | :---: | :---: | :---: |")
    for sec in ALL_SECURITY_REQUIREMENTS:
        p(f"| `{sec['id']}` | **{sec['title']}** | {sec['description']} | `{sec['upstream_ref']}` | {sec['priority']} | `{sec['verification_method']}` |")
    p("")

    # Section 24: Privacy Requirements (20 Specifications)
    p("## 24. Privacy & DPDP Act 2023 Statutory Compliance (SRS-PRIV-001 to SRS-PRIV-020)")
    p("Citizen consent management, zero-plaintext PHI in logs, purpose limitation, and statutory de-identification:")
    p("")
    p("| Req ID | Privacy Requirement | Statutory Data Protection Standard | Target Upstream | Priority | Verification Gate |")
    p("| :---: | :--- | :--- | :---: | :---: | :---: |")
    for priv in ALL_PRIVACY_REQUIREMENTS:
        p(f"| `{priv['id']}` | **{priv['title']}** | {priv['description']} | `{priv['upstream_ref']}` | {priv['priority']} | `{priv['verification_method']}` |")
    p("")

    # Section 25: Performance Requirements
    p("## 25. System Latency & Performance Bounds")
    p("Interactive p95 latency targets: UI interactive < 250ms, local SQLite commit < 35ms, cloud REST API < 400ms, autocomplete < 30ms, thermal print < 800ms.")
    p("")

    # Section 26: Availability Requirements
    p("## 26. High-Availability & Service Level Guarantees")
    p("99.9% local clinic edge uptime during operating hours (08:00–20:00); 99.95% central cloud multi-AZ availability; MTTR < 4 hours.")
    p("")

    # Section 27: Offline Requirements (20 Specifications)
    p("## 27. Offline-First Autonomous Edge Operation (SRS-OFF-001 to SRS-OFF-020)")
    p("72-hour continuous local operation, vector clock synchronization, CRDT conflict resolution, and offline session authentication:")
    p("")
    p("| Req ID | Offline Requirement | Autonomous Edge Protocol Standard | Target Upstream | Priority | Verification Gate |")
    p("| :---: | :--- | :--- | :---: | :---: | :---: |")
    for off in ALL_OFFLINE_REQUIREMENTS:
        p(f"| `{off['id']}` | **{off['title']}** | {off['description']} | `{off['upstream_ref']}` | {off['priority']} | `{off['verification_method']}` |")
    p("")

    # Section 28: Localization Requirements
    p("## 28. Vernacular Kannada & Bilingual Localization")
    p("Complete UTF-8 native Kannada (kn-IN) and Indian English (en-IN) rendering across all user interfaces, error dialogs, audio calls, and printed slips.")
    p("")

    # Section 29: Accessibility Requirements
    p("## 29. Web Content Accessibility Guidelines (WCAG 2.1 AA)")
    p("Minimum 4.5:1 color contrast, full keyboard navigation, screen reader ARIA landmarks, and large 48x48 dp touch targets.")
    p("")

    # Section 30: Reporting Requirements
    p("## 30. Statutory & Municipal Reporting Requirements")
    p("Automated daily OPD attendance summaries, monthly state HMIS exports, and RCH maternal/child health registers.")
    p("")

    # Section 31: Analytics Requirements
    p("## 31. Public Health Analytics & Epidemiological Intelligence")
    p("Real-time syndromic fever heatmaps, ward-level chronic disease prevalence dashboards, and clinic stock burn-down rate tracking.")
    p("")

    # Section 32: AI Requirements
    p("## 32. Advisory Clinical Decision Support AI Invariants")
    p("All AI models are strictly advisory. Human physician clinical judgment remains legally authoritative. Automated autonomous diagnosis is strictly prohibited.")
    p("")

    # Section 33: Integration Requirements (20 Specifications)
    p("## 33. External Interoperability & Integration Standards (SRS-INT-001 to SRS-INT-020)")
    p("Integration interfaces with ABDM (M1/M2/M3), FHIR R4, State SMS, GVK-EMRI 108 EMS, and hardware barcode/printer devices:")
    p("")
    p("| Req ID | Integration Requirement | Technical Integration Protocol | Target Upstream | Priority | Verification Gate |")
    p("| :---: | :--- | :--- | :---: | :---: | :---: |")
    for intr in ALL_INTEGRATION_REQUIREMENTS:
        p(f"| `{intr['id']}` | **{intr['title']}** | {intr['description']} | `{intr['upstream_ref']}` | {intr['priority']} | `{intr['verification_method']}` |")
    p("")

    # Section 34: Data Requirements (20 Specifications)
    p("## 34. Data Architecture & Relational Persistence Standards (SRS-DATA-001 to SRS-DATA-020)")
    p("UUIDv7 primary keys, temporal data modeling, soft deletion tombstones, and relational schemas across operational domains:")
    p("")
    p("| Req ID | Data Requirement | Relational Data Domain Standard | Target Upstream | Priority | Verification Gate |")
    p("| :---: | :--- | :--- | :---: | :---: | :---: |")
    for data in ALL_DATA_REQUIREMENTS:
        p(f"| `{data['id']}` | **{data['title']}** | {data['description']} | `{data['upstream_ref']}` | {data['priority']} | `{data['verification_method']}` |")
    p("")

    # Section 35: UI Requirements (20 Specifications)
    p("## 35. User Interface & Touch Ergonomics Standards (SRS-UI-001 to SRS-UI-020)")
    p("Responsive PWA architecture, touchscreen targets, thermal printer formatting, and role-based dynamic navigation:")
    p("")
    p("| Req ID | UI Requirement | User Interface & Experience Specification | Target Upstream | Priority | Verification Gate |")
    p("| :---: | :--- | :--- | :---: | :---: | :---: |")
    for ui in ALL_UI_REQUIREMENTS:
        p(f"| `{ui['id']}` | **{ui['title']}** | {ui['description']} | `{ui['upstream_ref']}` | {ui['priority']} | `{ui['verification_method']}` |")
    p("")

    # Section 36: API Requirements
    p("## 36. Application Programming Interface (API) Standards")
    p("RESTful JSON over HTTPS and internal gRPC; OpenAPI 3.1 specifications; mandatory `X-Correlation-ID` and `Idempotency-Key` headers.")
    p("")

    # Section 37: Audit Requirements
    p("## 37. Cryptographic WORM Audit Trail Architecture")
    p("Append-only audit ledger with SHA-256 hash chaining; cryptographic node signatures; zero deletion or modification of audit rows.")
    p("")

    # Section 38: Observability Requirements
    p("## 38. Observability, Telemetry & OpenTelemetry Spans")
    p("W3C TraceContext distributed tracing across edge and cloud; Prometheus `/metrics` endpoints; standardized PromQL alert thresholds.")
    p("")

    # Section 39: Disaster Recovery Requirements
    p("## 39. Disaster Recovery SLAs & Business Continuity")
    p("Recovery Point Objective (RPO) < 15 minutes; Recovery Time Objective (RTO) < 30 minutes; edge cold-boot recovery < 5 minutes.")
    p("")

    # Section 40: Business Continuity
    p("## 40. Facility Business Continuity & UPS Power Protection")
    p("Minimum 4-hour LiFePO4 battery run-time on line-interactive UPS; dual-SIM cellular fallback switchover < 5 seconds.")
    p("")

    # Section 41: Error Handling
    p("## 41. Standardized Error Handling & RFC 7807 Problem Details")
    p("All service errors return standardized RFC 7807 Problem Details payloads with unique error codes, localized messages, and diagnostic trace IDs.")
    p("")

    # Section 42: Exception Handling
    p("## 42. Clinical Exception Handling & Break-Glass Governance")
    p("Unconscious trauma emergency overrides bypass digital consent requirements but mandate post-hoc clinical review within 24 hours.")
    p("")

    # Section 43: Configuration Management
    p("## 43. Configuration Management & Environment Segregation")
    p("12-Factor app configuration stored in environment variables; secrets managed in HashiCorp Vault; strict segregation across 8 environments.")
    p("")

    # Section 44: Feature Flags
    p("## 44. Dynamic Feature Toggles & Gradual Rollout")
    p("Runtime feature flag evaluation per clinic, allowing canary releases and instant rollback of problematic modules without redeployment.")
    p("")

    # Section 45: Compliance
    p("## 45. Statutory & Regulatory Mandates")
    p("Full adherence to the Digital Personal Data Protection (DPDP) Act 2023, EHR Standards for India 2016, and CDSCO Drug Rules.")
    p("")

    # Section 46: Acceptance Criteria
    p("## 46. Formal Quality Gate & Acceptance Criteria Framework")
    p("Every functional and non-functional requirement defines executable Gherkin Given/When/Then scenarios validated in continuous CI/CD pipelines.")
    p("")

    # Section 47: Requirement Dependencies
    p("## 47. Requirement Dependency Graph & Acyclic Validation")
    p("Requirement dependencies form a valid Directed Acyclic Graph (DAG) rooted in core foundation and identity services.")
    p("")

    # Section 48: Requirement Prioritization
    p("## 48. MoSCoW Prioritization & Phased Delivery Model")
    p("Requirements categorized into Must Have (Core MVP), Should Have (Enhancements), Could Have (Advanced), and Won't Have (Out-of-scope).")
    p("")

    # Section 49: Change Management
    p("## 49. Engineering Change Control & RFC Governance")
    p("Modifications to baseline requirements require formal Request for Comments (RFC), impact analysis, and approval by the Architecture Board.")
    p("")

    # Section 50: Traceability
    p("## 50. Master Bi-Directional Traceability Register")
    p("Complete mapping linking every SRS requirement upstream to Business Requirements (`BR-`) and downstream to Planned Epics and Test suites.")
    p("")

    # Section 51: Completeness Audit
    p("## 51. SRS Completeness Audit & Formal Engineering Sign-Off")
    p(f"The Namma Clinic System Requirements Specification baseline registers exactly **{TOTAL_SRS_REQUIREMENTS} formal requirements**:")
    p(f"- Functional Requirements: **{len(ALL_FUNCTIONAL_REQUIREMENTS)}** (`SRS-FR-001` to `SRS-FR-060`)")
    p(f"- Non-Functional Requirements: **{len(ALL_NON_FUNCTIONAL_REQUIREMENTS)}** (`SRS-NFR-001` to `SRS-NFR-040`)")
    p(f"- Security Requirements: **{len(ALL_SECURITY_REQUIREMENTS)}** (`SRS-SEC-001` to `SRS-SEC-030`)")
    p(f"- Privacy Requirements: **{len(ALL_PRIVACY_REQUIREMENTS)}** (`SRS-PRIV-001` to `SRS-PRIV-020`)")
    p(f"- Clinical Safety Requirements: **{len(ALL_CLINICAL_REQUIREMENTS)}** (`SRS-CR-001` to `SRS-CR-020`)")
    p(f"- Operational Requirements: **{len(ALL_OPERATIONAL_REQUIREMENTS)}** (`SRS-OR-001` to `SRS-OR-020`)")
    p(f"- Offline Resilience Requirements: **{len(ALL_OFFLINE_REQUIREMENTS)}** (`SRS-OFF-001` to `SRS-OFF-020`)")
    p(f"- Integration Requirements: **{len(ALL_INTEGRATION_REQUIREMENTS)}** (`SRS-INT-001` to `SRS-INT-020`)")
    p(f"- Data Architecture Requirements: **{len(ALL_DATA_REQUIREMENTS)}** (`SRS-DATA-001` to `SRS-DATA-020`)")
    p(f"- UI & Accessibility Requirements: **{len(ALL_UI_REQUIREMENTS)}** (`SRS-UI-001` to `SRS-UI-020`)")
    p("")
    p("This document is certified complete, self-contained, and formally ratified for Phase 06 Solution Architecture and downstream implementation.")
    p("")

    content = "\n".join(lines)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    metrics = count_lines(content)
    print(f"Generated {OUTPUT_FILE}:")
    print(f"  Total Lines:       {metrics['total']}")
    print(f"  Substantive Lines: {metrics['substantive']}")
    return OUTPUT_FILE, metrics["total"], metrics["substantive"]

if __name__ == "__main__":
    generate_srs_master()
