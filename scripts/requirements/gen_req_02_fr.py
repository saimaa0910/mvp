#!/usr/bin/env python3
"""
gen_req_02_fr.py
Generates docs/02-requirements/02-functional-requirements.md.
Targets 3,500 - 5,000+ substantive markdown lines.
100% domain-specific primary healthcare functional depth for Namma Clinic.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_fr import FR_REQUIREMENTS
from common import p_line, render_metadata_table, format_gherkin

def generate_functional_requirements():
    target_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "docs", "02-requirements", "02-functional-requirements.md"
    )
    target_path = os.path.abspath(target_path)
    print(f"Generating Document 02 at {target_path}...")

    lines = []

    # Document Header & Title
    p_line(lines, "# Functional Requirements Specification: Namma Clinic Digital Health Platform")
    p_line(lines)
    render_metadata_table(
        lines,
        doc_id="DOC-REQ-002-FR",
        doc_title="Master Functional Requirements Specification & System Behavior Baseline",
        req_type="Functional Requirements (FR)",
        req_range="FR-001 through FR-080",
        count=80,
        parent_baseline="01-business-requirements.md",
        counterpart="04-business-rules.md"
    )

    # Section 1: Executive Summary & Functional Architecture
    p_line(lines, "## 1. Executive Summary & Functional Architecture Framework")
    p_line(lines, "This specification establishes the authoritative, implementation-ready functional baseline for the Namma Clinic Digital Health & Operations Platform across 183 primary urban healthcare centers in Greater Bengaluru. The 80 functional requirements (`FR-001` through `FR-080`) govern all end-to-end user workflows, client-server interactions, data validation schemas, database state transitions, peripheral device drivers, offline local stores, and background data synchronization protocols.")
    p_line(lines)
    p_line(lines, "Every functional requirement provides unambiguous behavioral rules necessary for frontend engineers, backend developers, database architects, and QA engineers to construct and verify the complete application suite without discovering missing business logic during sprint execution.")
    p_line(lines)

    # Section 2: Functional Requirements Categorization Taxonomy
    p_line(lines, "## 2. Functional Requirements Categorization Taxonomy")
    p_line(lines, "The 80 functional requirements are systematically organized across nine operational domains:")
    p_line(lines, "1. **Authentication, Authorization & User Administration (FR-001 to FR-008):** Multi-factor staff authentication, device hardware binding, RBAC access control, staff provisioning, session inactivity lock, temporary role switching, password resets, and session audit logs.")
    p_line(lines, "2. **Patient Registration, Demographics, ABHA & Search (FR-009 to FR-018):** Walk-in demographic capture, phonetic search, duplicate detection, municipal UHID minting, ABHA creation via Aadhaar OTP, QR code verification, demographic edits, family grouping, DPDP Act consent capture, and temporary offline UHID generation.")
    p_line(lines, "3. **OPD Queue, Token Dispensing & Triage Vitals (FR-019 to FR-026):** Sequential token generation, ESC/POS Web Serial thermal slip printing, priority queue routing, multi-parameter nursing vitals, automated BMI/growth metrics, capillary blood sugar screening, red-flag emergency alert chimes, and electronic patient calling.")
    p_line(lines, "4. **Doctor Consultation, EMR-Lite, ICD-10 & Prescribing (FR-027 to FR-038):** 1-click chief complaint chips, structured physical examination notes, curated ICD-10 diagnosis search, Karnataka 120 EDL formulary lookup, structured dosage chips, drug-drug interaction warnings, clinical override capture, allergy guards, pediatric dosage calculator, lifestyle advice, follow-up scheduling, and digital prescription signing.")
    p_line(lines, "5. **Point-of-Care Diagnostics & Laboratory Worklists (FR-039 to FR-048):** Rapid test ordering, laboratory worklists, GS1-128 specimen barcode labeling, qualitative/quantitative result entry, reference range comparison, sub-30s panic value alerts, reagent lot tracking, PDF report generation, external specimen referral manifests, and rapid test photo ingestion.")
    p_line(lines, "6. **Pharmacy Dispensing, 120 EDL Inventory & Batch Tracking (FR-049 to FR-058):** Electronic prescription retrieval, automated FEFO batch allocation, barcode scan verification, partial dispensing, atomic inventory balance decrements, warehouse delivery challan ingestion, stockout buffer alerts, near-expiry quarantine, discrepancy stock adjustments, and automated 30-day replenishment indents.")
    p_line(lines, "7. **Care Continuity, Referrals & Specialized Cohorts (FR-059 to FR-066):** Secondary hospital referral slips with Bharat QR, counter-referral note ingestion, maternal ANC registration, high-risk pregnancy tagging, NCD cohort enrollment, missed appointment defaulter tracking, postnatal care tracking, and pediatric immunization lot linkage.")
    p_line(lines, "8. **Offline Architecture, Data Sync & Conflict Resolution (FR-067 to FR-074):** Dexie.js IndexedDB storage, FIFO mutation queue with SHA-256 checksums, network reconnection detection, idempotent chunked sync replay, deterministic conflict resolution, master catalog caching, queue backlog monitoring, and local storage encryption.")
    p_line(lines, "9. **Supervisor Functions, End-of-Day Reconciliation & Admin (FR-075 to FR-080):** Morning opening readiness checklist, end-of-day session reconciliation, supervisor retrospective data amendments, zonal formulary broadcasts, facility telemetry dashboards, and system-wide immutable audit trail exports.")
    p_line(lines)

    # Architecture Mermaid Diagram
    p_line(lines, "```mermaid")
    p_line(lines, "graph TD")
    p_line(lines, "    subgraph FrontDesk[\"Front Desk & Registration Desk\"]")
    p_line(lines, "        F1[\"FR-009 / FR-012:<br/>Registration & UHID Minting\"]")
    p_line(lines, "        F2[\"FR-013 / FR-014:<br/>ABHA Aadhaar OTP & QR Verification\"]")
    p_line(lines, "        F3[\"FR-019 / FR-020:<br/>Daily Token & Thermal Slip Print\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph NursingDesk[\"Nursing Station & Triage Desk\"]")
    p_line(lines, "        N1[\"FR-022 / FR-023:<br/>Multi-Vitals & BMI Calculation\"]")
    p_line(lines, "        N2[\"FR-024 / FR-025:<br/>RBS Glucose & Emergency Alert Chime\"]")
    p_line(lines, "        N3[\"FR-061 / FR-066:<br/>ANC Schedule & Immunization Lots\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph DoctorDesk[\"Doctor Consultation Room (EMR-Lite)\"]")
    p_line(lines, "        D1[\"FR-026 / FR-027:<br/>Patient Call & Complaint Chips\"]")
    p_line(lines, "        D2[\"FR-029 / FR-030:<br/>ICD-10 Diagnosis & 120 EDL Search\"]")
    p_line(lines, "        D3[\"FR-032 / FR-034:<br/>DDI Checks & Allergy Warnings\"]")
    p_line(lines, "        D4[\"FR-038 / FR-059:<br/>Digital Rx Sign & Bharat QR Referral\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph DiagnosticPharmacy[\"Laboratory & Pharmacy Desks\"]")
    p_line(lines, "        L1[\"FR-039 / FR-041:<br/>Lab Worklist & Specimen Barcodes\"]")
    p_line(lines, "        L2[\"FR-042 / FR-044:<br/>Results Entry & Sub-30s Panic Alert\"]")
    p_line(lines, "        P1[\"FR-049 / FR-050:<br/>Rx Retrieval & FEFO Allocation\"]")
    p_line(lines, "        P2[\"FR-051 / FR-053:<br/>Barcode Scan & Atomic Stock Decrement\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph CoreEngine[\"Offline Sync & Municipal Governance\"]")
    p_line(lines, "        S1[\"FR-067 / FR-068:<br/>Dexie.js Store & SHA-256 Mutation Queue\"]")
    p_line(lines, "        S2[\"FR-070 / FR-071:<br/>Idempotent Sync Replay & Conflict Rules\"]")
    p_line(lines, "        S3[\"FR-075 / FR-076:<br/>Morning Readiness & EOD Reconciliation\"]")
    p_line(lines, "    end")
    p_line(lines, "    F1 --> F2 --> F3 --> N1 --> N2 --> D1 --> D2 --> D3 --> D4")
    p_line(lines, "    D4 --> P1 --> P2")
    p_line(lines, "    D2 -.-> L1 --> L2 -.-> D1")
    p_line(lines, "    F1 -.-> S1")
    p_line(lines, "    N1 -.-> S1")
    p_line(lines, "    D4 -.-> S1")
    p_line(lines, "    P2 -.-> S1")
    p_line(lines, "    S1 --> S2 --> S3")
    p_line(lines, "```")
    p_line(lines)

    # Section 3: Master Inventory Table
    p_line(lines, "## 3. Master Functional Requirements Inventory Table (FR-001 to FR-080)")
    p_line(lines, "| Requirement ID | Functional Requirement Title | Operational Domain | Priority | Primary Actor | API Contract Endpoint | PostgreSQL Target Table | Local Dexie Store |")
    p_line(lines, "| :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |")
    for r in FR_REQUIREMENTS:
        p_line(lines, f"| [`{r['id']}`](#{r['id'].lower()}) | **{r['title']}** | `{r['domain']}` | `{r['priority']}` | {r['actor']} | `{r['api_endpoint']}` | `{r['db_table']}` | `{r['dexie_store']}` |")
    p_line(lines)

    # Section 4: Deep Technical & Operational Specifications
    p_line(lines, "## 4. Comprehensive Functional Requirement Specifications (FR-001 to FR-080)")
    p_line(lines, "This section establishes the exhaustive engineering, architectural, and operational specifications for each of the 80 functional requirements committed for production baseline delivery.")
    p_line(lines)

    for i, r in enumerate(FR_REQUIREMENTS, 1):
        req_id = r["id"]
        title = r["title"]
        p_line(lines, f"### 4.{i} {req_id}: {title}")
        p_line(lines)

        # Attribute Table
        p_line(lines, "| Specification Attribute | Formal Engineering Definition |")
        p_line(lines, "| :--- | :--- |")
        p_line(lines, f"| **Requirement ID** | `{req_id}` |")
        p_line(lines, f"| **Requirement Title** | {title} |")
        p_line(lines, f"| **Requirement Statement**| {r['statement']} |")
        p_line(lines, f"| **Requirement Type** | `{r['type']}` |")
        p_line(lines, f"| **Priority Level** | `{r['priority']}` (Rationale: {r['priority_rationale']}) |")
        p_line(lines, f"| **Business Value** | {r['business_value']} |")
        p_line(lines, f"| **Engineering Rationale**| {r['rationale']} |")
        p_line(lines, f"| **Primary Actor** | `{r['actor']}` |")
        p_line(lines, f"| **Target User Persona** | [`{r['persona']}`](../01-project-management/07-user-personas.md#{r['persona'].lower()}) |")
        p_line(lines, f"| **Accountable Role** | [`{r['role']}`](../01-project-management/08-role-and-responsibility-matrix.md#{r['role'].lower()}) |")
        p_line(lines, f"| **Key Stakeholder** | [`{r['stakeholder']}`](../01-project-management/06-stakeholders.md#{r['stakeholder'].lower()}) |")
        p_line(lines, f"| **Trigger Condition** | {r['trigger']} |")
        p_line(lines, f"| **System Preconditions** | {r['preconditions']} |")
        p_line(lines, f"| **Input Specifications** | {r['inputs']} |")
        p_line(lines, f"| **Validation Rules** | {r['validation']} |")
        p_line(lines, f"| **Postconditions** | {r['postconditions']} |")
        p_line(lines, f"| **State Mutations** | {r['state_changes']} |")
        p_line(lines, f"| **Associated Rules** | Business: [`{r['business_rules']}`](./04-business-rules.md#{r['business_rules'].lower()}) \\| Clinical: [`{r['clinical_rules']}`](./05-clinical-rules.md#{r['clinical_rules'].lower()}) \\| Operational: [`{r['operational_rules']}`](./06-operational-rules.md#{r['operational_rules'].lower()}) |")
        p_line(lines, f"| **Security & Privacy** | Security: [`{r['security_implications'].split(':')[0]}`](./07-security-requirements.md#{r['security_implications'].split(':')[0].lower()}) \\| Privacy: [`{r['privacy_implications'].split(':')[0]}`](./08-privacy-requirements.md#{r['privacy_implications'].split(':')[0].lower()}) |")
        p_line(lines, f"| **Data & Audit** | Data: `{r['data_implications'][:45]}...` \\| Audit: `{r['audit_requirements'][:45]}...` |")
        p_line(lines, f"| **Offline & Sync** | Offline: [`{r['offline_behavior'].split(':')[0]}`](./13-offline-requirements.md#{r['offline_behavior'].split(':')[0].lower()}) \\| Sync: `{r['synchronization_implications'][:45]}...` |")
        p_line(lines, f"| **Integration Ref** | Integration: [`{r['integration_implications'].split(':')[0]}`](./17-integration-requirements.md#{r['integration_implications'].split(':')[0].lower()}) |")
        p_line(lines, f"| **Quality Expectations**| Perf: [`{r['performance_expectations'].split(':')[0]}`](./09-performance-requirements.md#{r['performance_expectations'].split(':')[0].lower()}) \\| Avail: [`{r['availability_expectations'].split(':')[0]}`](./10-availability-requirements.md#{r['availability_expectations'].split(':')[0].lower()}) |")
        p_line(lines, f"| **Localization & A11y**| Loc: [`{r['localization_expectations'].split(':')[0]}`](./11-localization-requirements.md#{r['localization_expectations'].split(':')[0].lower()}) \\| A11y: [`{r['accessibility_expectations'].split(':')[0]}`](./12-accessibility-requirements.md#{r['accessibility_expectations'].split(':')[0].lower()}) |")
        p_line(lines, f"| **Failure & Recovery** | Failure: {r['failure_behavior']} \\| Recovery: {r['recovery_behavior']} |")
        p_line(lines, f"| **Observability** | Logging: `{r['logging_requirements'][:45]}...` \\| Metrics: `{r['metrics'][:45]}...` |")
        p_line(lines, f"| **Upstream Traceability**| Obj: [`{r['objective_ref']}`](../01-project-management/02-project-vision-and-objectives.md#{r['objective_ref'].lower()}) \\| Scope: [`{r['scope_ref']}`](../01-project-management/04-in-scope.md#{r['scope_ref'].lower()}) \\| Risk: [`{r['risk_ref']}`](../01-project-management/12-project-risks.md#{r['risk_ref'].lower()}) |")
        p_line(lines, f"| **Downstream Planning** | Epic: `{r['planned_epic']}` \\| Feature: `{r['planned_feature']}` \\| API: `{r['planned_api']}` \\| DB: `{r['planned_db']}` \\| Test: `{r['planned_test']}` |")
        p_line(lines)

        # Operational Execution Paths
        p_line(lines, "#### 4." + str(i) + ".1 Frontline Operational Workflow & Execution Paths")
        p_line(lines, "- **Standard Execution Flow (Happy Path):**")
        for step_idx, step in enumerate(r['main_flow'], 1):
            p_line(lines, f"  {step_idx}. {step}")
        p_line(lines, f"- **Alternative Execution Flow:** {r['alternate_flow']}")
        p_line(lines, f"- **Exception & Recovery Flow:** {r['exception_flow']}")
        p_line(lines)

        # Technical Architecture Invariants
        p_line(lines, "#### 4." + str(i) + ".2 Technical Invariants & Architectural Contracts")
        p_line(lines, f"- **Backend REST API Endpoint:** `{r['api_endpoint']}`")
        p_line(lines, f"- **Database Entity Model:** `{r['db_table']}` in PostgreSQL schema `public`.")
        p_line(lines, f"- **Client Offline Store:** Local Dexie.js store `{r['dexie_store']}` with UUIDv7 indexing.")
        p_line(lines, f"- **Distributed Tracing Contract:** OpenTelemetry span `namma.clinic.fr.{req_id.lower()}`.")
        p_line(lines, f"- **Tamper-Evident Audit Event:** Writes WORM audit payload to Grafana Loki tagged `event_type=FUNCTIONAL_MUTATION`, `req_id={req_id}`.")
        p_line(lines)

        # Executable Gherkin Scenarios
        p_line(lines, "#### 4." + str(i) + ".3 Executable BDD Acceptance Scenarios")
        gherkin_block = format_gherkin(r)
        for gh_l in gherkin_block:
            p_line(lines, gh_l)
        p_line(lines)

        # Verification & Quality Sign-Off
        p_line(lines, "#### 4." + str(i) + ".4 Verification Protocol & Quality Sign-Off")
        p_line(lines, f"- **Verification Method:** {r['verification_method']}")
        p_line(lines, f"- **Automated Test Suite:** `{r['test_id']}` ({r['test_type']}) targeting >=90% statement coverage.")
        p_line(lines, f"- **Related Internal Requirements:** {', '.join([f'[`{x}`](#{x.lower()})' if x.startswith('FR-') else f'`{x}`' for x in r['related_requirements']])}")
        p_line(lines, f"- **Dependencies & Blocking Constraints:** {', '.join(r['dependencies'])} | Constraints: {r['constraints']}")
        p_line(lines, f"- **Architectural Assumptions & Open Questions:** Assumption: {r['assumptions']} | Open Question: {r['open_questions']}")
        p_line(lines)
        p_line(lines, "---")
        p_line(lines)

    # Section 5: End-to-End Traceability Matrix
    p_line(lines, "## 5. End-to-End Cross-Baseline Traceability Matrix")
    p_line(lines, "Complete relational mapping linking each Functional Requirement upstream to Project Management charters and downstream to planned engineering epics:")
    p_line(lines)
    p_line(lines, "| Functional Req ID | Upstream Objective | Upstream Scope Ref | Upstream Risk Ref | Accountable Role | Downstream Planned Epic | Downstream API Contract | Downstream Test ID |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in FR_REQUIREMENTS:
        req_id = r["id"]
        obj = r["objective_ref"]
        sc = r["scope_ref"]
        risk = r["risk_ref"]
        role = r["role"]
        epic = r["planned_epic"]
        api = r["planned_api"]
        test_id = r["test_id"]
        p_line(lines, f"| [`{req_id}`](#{req_id.lower()}) | [`{obj}`](../01-project-management/02-project-vision-and-objectives.md#{obj.lower()}) | [`{sc}`](../01-project-management/04-in-scope.md#{sc.lower()}) | [`{risk}`](../01-project-management/12-project-risks.md#{risk.lower()}) | {role} | `{epic}` | `{api}` | `{test_id}` |")
    p_line(lines)

    # Section 6: Governance & Quality Sign-Off
    p_line(lines, "## 6. Functional Baseline Governance & Quality Sign-Off")
    p_line(lines, "This Functional Requirements Specification constitutes the official engineering blueprint for the Namma Clinic Digital Health Platform. Every functional requirement defined herein has been validated against clinical practice guidelines, pharmacy dispensing standards, and municipal data governance regulations.")
    p_line(lines)
    p_line(lines, "Any change to screen workflows, API signatures, database schemas, or validation logic must be submitted as a formal Change Request under [`docs/01-project-management/18-change-management.md`](../01-project-management/18-change-management.md).")
    p_line(lines)

    content = "\n".join(lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated Document 02: {len(lines)} total lines.")

if __name__ == "__main__":
    generate_functional_requirements()
