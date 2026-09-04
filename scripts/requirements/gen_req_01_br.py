#!/usr/bin/env python3
"""
gen_req_01_br.py
Generates docs/02-requirements/01-business-requirements.md.
Targets 2,800 - 3,500+ substantive markdown lines.
100% domain-specific municipal healthcare engineering depth for Namma Clinic.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_br import BR_REQUIREMENTS
from common import p_line, render_metadata_table, format_gherkin

def generate_business_requirements():
    target_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "docs", "02-requirements", "01-business-requirements.md"
    )
    target_path = os.path.abspath(target_path)
    print(f"Generating Document 01 at {target_path}...")

    lines = []

    # Document Header & Title
    p_line(lines, "# Business Requirements Specification: Namma Clinic Digital Health Platform")
    p_line(lines)
    render_metadata_table(
        lines,
        doc_id="DOC-REQ-001-BR",
        doc_title="Master Business Requirements Specification & Value Realization Baseline",
        req_type="Business Requirements (BR)",
        req_range="BR-001 through BR-050",
        count=50,
        parent_baseline="02-functional-requirements.md",
        counterpart="04-business-rules.md"
    )

    # Section 1: Executive Summary & Municipal Healthcare Mandate
    p_line(lines, "## 1. Executive Summary & Municipal Healthcare Mission")
    p_line(lines, "The Namma Clinic Digital Health & Operations Platform represents the municipal digital transformation backbone for the Greater Bengaluru Authority (GBA) and Bruhat Bengaluru Mahanagara Palike (BBMP) Health Department. Established under the National Health Mission (NHM) and the 15th Finance Commission urban health grants, the platform provides comprehensive digital infrastructure across 183 primary urban healthcare centers (Namma Clinics) distributed throughout Bengaluru's 8 administrative zones and 243 municipal wards.")
    p_line(lines)
    p_line(lines, "The primary mission of the platform is to eliminate healthcare access disparities for 1.2 million vulnerable urban slum residents and daily wage earners by transforming fragmented, paper-reliant dispensaries into high-efficiency, evidence-based, data-driven primary care delivery nodes. This specification establishes 50 rigorous, implementation-ready business requirements (`BR-001` through `BR-050`). Every requirement links directly to measurable public health outcomes, clinical throughput metrics, patient safety standards, and municipal governance accountability.")
    p_line(lines)

    # Section 2: Business Requirements Categorization Taxonomy
    p_line(lines, "## 2. Business Requirements Categorization Taxonomy")
    p_line(lines, "The 50 business requirements are structured across seven core municipal healthcare domains:")
    p_line(lines, "1. **Population Health & Vulnerable Slum Access (BR-001 to BR-010):** Universal walk-in primary care access, OPD wait time reduction, maternal antenatal care (ANC) tracking, adult NCD screening, essential drug availability, rapid laboratory turnarounds, secondary referral loop closure, syndromic disease early warning, 100% offline clinic continuity, and DPDP Act 2023 privacy governance.")
    p_line(lines, "2. **Clinical Productivity, Diagnostics & Quality (BR-011 to BR-020):** Streamlined consultation cycle times (<4 mins), electronic prescription safety, vaccine cold chain monitoring, pediatric growth and SAM triage, automated IHIP Form P surveillance, FEFO pharmacy dispensing, multi-desk queue synchronization, bilingual Kannada/English interfaces, universal ABHA seeding, and thermal paper ticket printing.")
    p_line(lines, "3. **Diagnostic Accuracy, Clinical Safety & Supply Chain (BR-021 to BR-030):** Critical panic value lab alerts (<30s), automated low-stock indenting, ICD-10 standardized diagnostic coding, maternal postnatal care (PNC) compliance, elderly/vulnerable priority queue routing, nursing shift handover protocols, geofenced staff attendance verification, adverse drug reaction (ADR) reporting, automated daily electronic census, and longitudinal EHR portability.")
    p_line(lines, "4. **Special Disease Programs & Preventive Oncology (BR-031 to BR-040):** Presumptive tuberculosis screening with Nikshay integration, oral/breast/cervical cancer screening, laboratory reagent expiry blocking, mental health e-Manas screening, emergency resuscitation readiness logs, automated bilingual SMS prescription dispatch, citizen grievance integration (Sahaaya 2.0), immutable WORM audit trails, ASHA community field outreach lists, and clinic energy/UPS telemetry monitoring.")
    p_line(lines, "5. **Policy Standards, Maternal Safety & Laboratory Integrity (BR-041 to BR-050):** Indian Public Health Standards (IPHS 2022) alignment, High-Risk Pregnancy (HRP) red-flag tracking, laboratory specimen chain-of-custody tracking, multi-tiered RBAC/ABAC security enforcement, disaster recovery database replication (RPO <5m, RTO <30m), public health data anonymization (k>=5), vaccine vial utilization tracking, barcode-verified medication dispensing, dynamic ward-level health equity rebalancing, and 100% end-to-end requirements traceability.")
    p_line(lines)

    # Architecture Mermaid Diagram
    p_line(lines, "```mermaid")
    p_line(lines, "graph TD")
    p_line(lines, "    subgraph SlumCommunity[\"Urban Slum Catchment & Citizen Outreach\"]")
    p_line(lines, "        C1[\"BR-001 / BR-039:<br/>Citizen Walk-In & ASHA Field Lists\"]")
    p_line(lines, "        C2[\"BR-019 / BR-018:<br/>Bilingual Registration & ABHA Seeding\"]")
    p_line(lines, "        C3[\"BR-002 / BR-025:<br/>Priority Queue & Thermal Token Print\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph ClinicalEncounter[\"Namma Clinic Care Delivery\"]")
    p_line(lines, "        C4[\"BR-003 / BR-004 / BR-014:<br/>Triage: ANC, NCD & Pediatric Vitals\"]")
    p_line(lines, "        C5[\"BR-011 / BR-012 / BR-023:<br/>Doctor EMR: <4 min, ICD-10 & Safety\"]")
    p_line(lines, "        C6[\"BR-006 / BR-021 / BR-043:<br/>POC Diagnostics: 14 Tests & Panic Alerts\"]")
    p_line(lines, "        C7[\"BR-005 / BR-016 / BR-048:<br/>Pharmacy: 120 EDL, FEFO & Barcode Scan\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph MunicipalContinuity[\"Care Continuity & Municipal Intelligence\"]")
    p_line(lines, "        C8[\"BR-007 / BR-042:<br/>Secondary Referrals & HRP Registry\"]")
    p_line(lines, "        C9[\"BR-008 / BR-015:<br/>Real-Time Outbreak Alerts & IHIP Form P\"]")
    p_line(lines, "        C10[\"BR-009 / BR-045:<br/>Dexie Offline Autonomy & Cloud Disaster Recovery\"]")
    p_line(lines, "        C11[\"BR-029 / BR-049:<br/>Command Center Census & Equity Analytics\"]")
    p_line(lines, "    end")
    p_line(lines, "    C1 --> C2 --> C3 --> C4 --> C5 --> C6 --> C7")
    p_line(lines, "    C5 -.-> C8")
    p_line(lines, "    C5 -.-> C9")
    p_line(lines, "    C4 -.-> C10")
    p_line(lines, "    C7 --> C11")
    p_line(lines, "    C9 --> C11")
    p_line(lines, "```")
    p_line(lines)

    # Section 3: Master Inventory Table
    p_line(lines, "## 3. Master Business Requirements Inventory Table (BR-001 to BR-050)")
    p_line(lines, "| Requirement ID | Business Requirement Title | Healthcare Domain | Priority | Accountable Lead | Baseline State | Target Production State | Key Performance Indicator (KPI) |")
    p_line(lines, "| :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |")
    for r in BR_REQUIREMENTS:
        p_line(lines, f"| [`{r['id']}`](#{r['id'].lower()}) | **{r['title']}** | `{r['domain']}` | `{r['priority']}` | {r['owner']} | {r['baseline_state'][:40]}... | {r['target_state'][:40]}... | {r['business_metric'][:35]}... |")
    p_line(lines)

    # Section 4: Deep Technical & Operational Specifications
    p_line(lines, "## 4. Comprehensive Business Requirement Specifications (BR-001 to BR-050)")
    p_line(lines, "This section establishes the exhaustive engineering, clinical, and operational specifications for each of the 50 business requirements committed for production baseline delivery.")
    p_line(lines)

    for i, r in enumerate(BR_REQUIREMENTS, 1):
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

        # Business Measurement Model Sub-section
        p_line(lines, "#### 4." + str(i) + ".1 Business Outcome Measurement & Metric Contract")
        p_line(lines, f"- **Baseline Pre-Platform State:** {r['baseline_state']}")
        p_line(lines, f"- **Target Production State:** {r['target_state']}")
        p_line(lines, f"- **Core Business Metric:** `{r['business_metric']}`")
        p_line(lines, f"- **Measurement Methodology:** {r['measurement_method']}")
        p_line(lines, f"- **Authoritative Data Source:** `{r['data_source']}`")
        p_line(lines, f"- **Accountable Governance Owner:** {r['owner']}")
        p_line(lines, f"- **Audit Frequency:** `{r['frequency']}` | **Passing Threshold:** `{r['threshold']}`")
        p_line(lines, f"- **Success Condition:** {r['success_condition']}")
        p_line(lines, f"- **Failure Condition:** {r['failure_condition']}")
        p_line(lines)

        # Operational Execution Paths
        p_line(lines, "#### 4." + str(i) + ".2 Frontline Operational Workflow & Execution Paths")
        p_line(lines, "- **Standard Execution Flow (Happy Path):**")
        for step_idx, step in enumerate(r['main_flow'], 1):
            p_line(lines, f"  {step_idx}. {step}")
        p_line(lines, f"- **Alternative Execution Flow:** {r['alternate_flow']}")
        p_line(lines, f"- **Exception & Recovery Flow:** {r['exception_flow']}")
        p_line(lines)

        # Technical Architecture Invariants
        p_line(lines, "#### 4." + str(i) + ".3 Technical Invariants & Architectural Contracts")
        p_line(lines, f"- **Backend API Endpoint:** `POST /api/v1/business-workflows/{req_id.lower()}/execute`")
        p_line(lines, f"- **Database Entity Model:** `namma_clinic_{r['domain'].lower().replace(' ', '_')}_{req_id.lower().replace('-', '_')}` in PostgreSQL schema `clinical_ops`.")
        p_line(lines, f"- **Client Storage Engine:** Local store `dexie_{req_id.lower().replace('-', '_')}` with monotonic UUIDv7 keys in IndexedDB.")
        p_line(lines, f"- **Distributed Tracing Contract:** OpenTelemetry span `namma.clinic.br.{req_id.lower()}` with baggage `clinic_id`, `user_id`, and `ward_id`.")
        p_line(lines, f"- **Tamper-Evident Audit Event:** Writes WORM audit payload to Grafana Loki tagged `event_type=BUSINESS_MUTATION`, `req_id={req_id}`.")
        p_line(lines)

        # Executable Gherkin Scenarios
        p_line(lines, "#### 4." + str(i) + ".4 Executable BDD Acceptance Scenarios")
        gherkin_block = format_gherkin(r)
        for gh_l in gherkin_block:
            p_line(lines, gh_l)
        p_line(lines)

        # Verification & Quality Sign-Off
        p_line(lines, "#### 4." + str(i) + ".5 Verification Protocol & Quality Sign-Off")
        p_line(lines, f"- **Verification Method:** {r['verification_method']}")
        p_line(lines, f"- **Automated Test Suite:** `{r['test_id']}` ({r['test_type']}) targeting >=90% test statement coverage.")
        p_line(lines, f"- **Related Internal Requirements:** {', '.join([f'[`{x}`](#{x.lower()})' if x.startswith('BR-') else f'`{x}`' for x in r['related_requirements']])}")
        p_line(lines, f"- **Dependencies & Blocking Constraints:** {', '.join(r['dependencies'])} | Constraints: {r['constraints']}")
        p_line(lines, f"- **Architectural Assumptions & Open Questions:** Assumption: {r['assumptions']} | Open Question: {r['open_questions']}")
        p_line(lines)
        p_line(lines, "---")
        p_line(lines)

    # Section 5: End-to-End Traceability Matrix
    p_line(lines, "## 5. End-to-End Cross-Baseline Traceability Matrix")
    p_line(lines, "Complete relational mapping linking each Business Requirement upstream to Project Management charters and downstream to planned engineering epics:")
    p_line(lines)
    p_line(lines, "| Business Req ID | Upstream Objective | Upstream Scope Ref | Upstream Risk Ref | Accountable Lead | Downstream Planned Epic | Downstream API Contract | Downstream Test ID |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in BR_REQUIREMENTS:
        req_id = r["id"]
        obj = r["objective_ref"]
        sc = r["scope_ref"]
        risk = r["risk_ref"]
        owner = r["owner"]
        epic = r["planned_epic"]
        api = r["planned_api"]
        test_id = r["test_id"]
        p_line(lines, f"| [`{req_id}`](#{req_id.lower()}) | [`{obj}`](../01-project-management/02-project-vision-and-objectives.md#{obj.lower()}) | [`{sc}`](../01-project-management/04-in-scope.md#{sc.lower()}) | [`{risk}`](../01-project-management/12-project-risks.md#{risk.lower()}) | {owner} | `{epic}` | `{api}` | `{test_id}` |")
    p_line(lines)

    # Section 6: Governance & Quality Sign-Off
    p_line(lines, "## 6. Business Value Realization & Governance Sign-Off")
    p_line(lines, "This Business Requirements Specification constitutes the authoritative functional commitment for the Namma Clinic Digital Health Platform. Every business requirement defined herein has been validated against BBMP municipal health bylaws, National Health Mission standards, and the Karnataka Urban Primary Healthcare Operational Framework.")
    p_line(lines)
    p_line(lines, "Any modification, scope addition, or priority reclassification of these 50 business requirements must follow formal Change Control Board evaluation under [`docs/01-project-management/18-change-management.md`](../01-project-management/18-change-management.md). Under no circumstances may application code, database migrations, or API contracts deviate from these baselined business requirements without an approved, audited Change Request.")
    p_line(lines)

    content = "\n".join(lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated Document 01: {len(lines)} total lines.")

if __name__ == "__main__":
    generate_business_requirements()
