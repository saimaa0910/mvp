#!/usr/bin/env python3
"""
gen_req_04_brule.py
Generates docs/02-requirements/04-business-rules.md.
Targets 2,800 - 3,500+ substantive markdown lines.
100% domain-specific municipal operational and business logic for Namma Clinic.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_brule import BRULE_RULES
from common import p_line, render_metadata_table, format_gherkin

def generate_business_rules():
    target_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "docs", "02-requirements", "04-business-rules.md"
    )
    target_path = os.path.abspath(target_path)
    print(f"Generating Document 04 at {target_path}...")

    lines = []

    # Document Header & Title
    p_line(lines, "# Business Rules Specification: Namma Clinic Digital Health Platform")
    p_line(lines)
    render_metadata_table(
        lines,
        doc_id="DOC-REQ-004-BRULE",
        doc_title="Master Business Rules Specification & Operational Decision Logic Baseline",
        req_type="Business Rules (BRULE)",
        req_range="BRULE-001 through BRULE-050",
        count=50,
        parent_baseline="01-business-requirements.md",
        counterpart="06-operational-rules.md"
    )

    # Section 1: Executive Summary & Governance Model
    p_line(lines, "## 1. Executive Summary & Business Rule Governance Framework")
    p_line(lines, "This specification establishes the authoritative, implementation-ready catalog of 50 business rules (`BRULE-001` through `BRULE-050`) governing the Namma Clinic Digital Health & Operations Platform across 183 primary urban healthcare centers in Greater Bengaluru. Business rules define the mandatory operational constraints, decision logic, authorization gates, and data integrity boundaries that dictate how clinical, pharmacy, queue, and administrative workflows execute.")
    p_line(lines)
    p_line(lines, "Every rule in this specification is atomic, deterministic, and testable. In accordance with municipal health bylaws and statutory medical regulations, business rules eliminate operational ambiguity, enforce fraud prevention, guarantee patient equity, and protect municipal healthcare assets from administrative misuse.")
    p_line(lines)

    # Section 2: Taxonomy
    p_line(lines, "## 2. Business Rules Categorization Taxonomy")
    p_line(lines, "The 50 business rules are organized across five operational domains:")
    p_line(lines, "1. **Patient Registration & Identity Governance (BRULE-001 to BRULE-010):** Universal walk-in eligibility, shared household phone limits (max 8), mandatory demographic fields, emergency ABHA bypass, age derivation from DOB, 72-hour offline UHID reconciliation, demographic correction audits, household linking consent, DPDP consent withdrawal, and permanent soft-deletion tombstoning.")
    p_line(lines, "2. **OPD Queue & Triage Workflow Governance (BRULE-011 to BRULE-020):** Midnight sequence resets (001), 2:1 priority queue interleaving, 24-hour token expiration, multi-doctor queue load balancing, 150-token waiting hall ceiling, 45-minute uncalled token cancellation, mandatory triage before consultation, red-flag emergency elevation, resuscitation queue bypass, and 2-time shift patient recall limits.")
    p_line(lines, "3. **Pharmacy Dispensing & Inventory Control (BRULE-021 to BRULE-030):** Strict FEFO batch picking, emergency stock adjustment cap (max 10 units), T-60 day near-expiry quarantine, zero dispensing without electronic prescription, partial dispensing rules, restricted antibiotic 7-day limits, dual approval for >50 unit discrepancies, weekly physical inventory audits, 7-day buffer stock reorder indents, and delivery challan barcode scanning.")
    p_line(lines, "4. **Clinical Documentation & Prescription Boundaries (BRULE-031 to BRULE-040):** Mandatory ICD-10 diagnosis before consultation sign-off, commercial drug blocking, max 6 items per prescription, mandatory DDI override justification, documented drug allergy hard blocks, chronic medication 30-day supply caps, mandatory pediatric weight for syrups, 90-day follow-up date horizon, secondary referral justifications, and counter-referral doctor verification.")
    p_line(lines, "5. **Facility Operations, Security & Administrative Control (BRULE-041 to BRULE-050):** Clinic closure blocked with active unfinalized tokens, daily 18:00 IST sync cutoff, retrospective encounter amendment dual approval, emergency formulary broadcast acknowledgment, shift handover dual digital signatures, biometric geofenced logins, 15-minute inactivity screen locks, role privilege escalation blocks, cold chain breach escalation within 15 minutes, and mandatory cryptographic WORM audit chaining.")
    p_line(lines)

    # Architecture Mermaid Diagram
    p_line(lines, "```mermaid")
    p_line(lines, "graph TD")
    p_line(lines, "    subgraph RegistrationQueue['Registration & Queue Rules']")
    p_line(lines, "        B1['BRULE-001 to 010:<br/>Identity & Consent Integrity']")
    p_line(lines, "        B2['BRULE-011 to 020:<br/>2:1 Priority Queue & Triage Gates']")
    p_line(lines, "    end")
    p_line(lines, "    subgraph ClinicalPharmacy['Clinical & Pharmacy Rules']")
    p_line(lines, "        B3['BRULE-021 to 030:<br/>FEFO Dispensing & Inventory Caps']")
    p_line(lines, "        B4['BRULE-031 to 040:<br/>Mandatory ICD-10 & Allergy Blocks']")
    p_line(lines, "    end")
    p_line(lines, "    subgraph FacilityGovernance['Facility & Security Rules']")
    p_line(lines, "        B5['BRULE-041 to 050:<br/>EOD Closure & WORM Audit Chaining']")
    p_line(lines, "    end")
    p_line(lines, "    B1 --> B2 --> B4 --> B3 --> B5")
    p_line(lines, "```")
    p_line(lines)

    # Section 3: Master Inventory Table
    p_line(lines, "## 3. Master Business Rules Inventory Table (BRULE-001 to BRULE-050)")
    p_line(lines, "| Rule ID | Business Rule Title | Primary Actor | Approval Requirement | Decision Trigger | Allowed Operational Outcome |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in BRULE_RULES:
        p_line(lines, f"| [`{r['id']}`](#{r['id'].lower()}) | **{r['title']}** | {r['actor']} | {r['approval_requirement']} | {r['trigger'][:30]}... | {r['allowed_outcome'][:35]}... |")
    p_line(lines)

    # Section 4: Deep Technical & Operational Specifications
    p_line(lines, "## 4. Comprehensive Business Rule Specifications (BRULE-001 to BRULE-050)")
    p_line(lines, "This section establishes the exhaustive engineering, decision logic, and operational specifications for each of the 50 business rules committed for production baseline delivery.")
    p_line(lines)

    for i, r in enumerate(BRULE_RULES, 1):
        rule_id = r["id"]
        title = r["title"]
        p_line(lines, f"### 4.{i} {rule_id}: {title}")
        p_line(lines)

        # Attribute Table
        p_line(lines, "| Specification Attribute | Formal Engineering Definition |")
        p_line(lines, "| :--- | :--- |")
        p_line(lines, f"| **Rule ID** | `{rule_id}` |")
        p_line(lines, f"| **Rule Title** | {title} |")
        p_line(lines, f"| **Rule Statement** | {r['statement']} |")
        p_line(lines, f"| **Rule Type** | `{r['type']}` |")
        p_line(lines, f"| **Priority Level** | `{r['priority']}` (Rationale: {r['priority_rationale']}) |")
        p_line(lines, f"| **Business Value** | {r['business_value']} |")
        p_line(lines, f"| **Policy Rationale** | {r['rationale']} |")
        p_line(lines, f"| **Primary Actor** | `{r['actor']}` |")
        p_line(lines, f"| **Target User Persona** | [`{r['persona']}`](../01-project-management/07-user-personas.md#{r['persona'].lower()}) |")
        p_line(lines, f"| **Accountable Role** | [`{r['role']}`](../01-project-management/08-role-and-responsibility-matrix.md#{r['role'].lower()}) |")
        p_line(lines, f"| **Key Stakeholder** | [`{r['stakeholder']}`](../01-project-management/06-stakeholders.md#{r['stakeholder'].lower()}) |")
        p_line(lines, f"| **Trigger Condition** | {r['trigger']} |")
        p_line(lines, f"| **Decision Logic** | `{r['decision_logic']}` |")
        p_line(lines, f"| **Allowed Outcome** | {r['allowed_outcome']} |")
        p_line(lines, f"| **Rejected Outcome** | {r['rejected_outcome']} |")
        p_line(lines, f"| **Exception Condition**| {r['exception_condition']} |")
        p_line(lines, f"| **Approval Required** | {r['approval_requirement']} |")
        p_line(lines, f"| **Audit Requirement** | `{r['audit_requirement']}` |")
        p_line(lines, f"| **Associated Rules** | Clinical: [`{r['clinical_rules']}`](./05-clinical-rules.md#{r['clinical_rules'].lower()}) \\| Operational: [`{r['operational_rules']}`](./06-operational-rules.md#{r['operational_rules'].lower()}) |")
        p_line(lines, f"| **Security & Privacy** | Security: `{r['security_implications']}` \\| Privacy: `{r['privacy_implications']}` |")
        p_line(lines, f"| **Data & Offline** | Data: `{r['data_implications']}` \\| Offline: `{r['offline_behavior']}` |")
        p_line(lines, f"| **Upstream Traceability**| Obj: [`{r['objective_ref']}`](../01-project-management/02-project-vision-and-objectives.md#{r['objective_ref'].lower()}) \\| Scope: [`{r['scope_ref']}`](../01-project-management/04-in-scope.md#{r['scope_ref'].lower()}) \\| Risk: [`{r['risk_ref']}`](../01-project-management/12-project-risks.md#{r['risk_ref'].lower()}) |")
        p_line(lines, f"| **Downstream Planning** | Epic: `{r['planned_epic']}` \\| Feature: `{r['planned_feature']}` \\| API: `{r['planned_api']}` \\| Test: `{r['planned_test']}` |")
        p_line(lines)

        # Operational Execution Paths
        p_line(lines, "#### 4." + str(i) + ".1 Operational Execution Protocol & Decision Flow")
        p_line(lines, "- **Standard Execution Flow (Happy Path):**")
        for step_idx, step in enumerate(r['main_flow'], 1):
            p_line(lines, f"  {step_idx}. {step}")
        p_line(lines, f"- **Exception Flow & Supervisor Escalation:** {r['alternate_flow']}")
        p_line(lines, f"- **Rejection & Error Handling Flow:** {r['exception_flow']}")
        p_line(lines)

        # Technical Architecture Invariants
        p_line(lines, "#### 4." + str(i) + ".2 Technical Invariants & Verification Contract")
        p_line(lines, f"- **Decision Logic Code Contract:** `{r['decision_logic']}`")
        p_line(lines, f"- **Allowed State Mutation:** {r['allowed_outcome']}")
        p_line(lines, f"- **Rejected State Protection:** {r['rejected_outcome']}")
        p_line(lines, f"- **Mandatory Audit Event:** `{r['audit_requirement']}`")
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
        p_line(lines, f"- **Automated Test Suite:** `{r['test_id']}` ({r['test_type']}) targeting 100% decision branch coverage.")
        p_line(lines, f"- **Related Internal Requirements:** {', '.join([f'[`{x}`](#{x.lower()})' if x.startswith('BRULE-') else f'`{x}`' for x in r['related_requirements']])}")
        p_line(lines, f"- **Dependencies & Blocking Constraints:** {', '.join(r['dependencies'])} | Constraints: {r['constraints']}")
        p_line(lines, f"- **Architectural Assumptions & Open Questions:** Assumption: {r['assumptions']} | Open Question: {r['open_questions']}")
        p_line(lines)
        p_line(lines, "---")
        p_line(lines)

    # Section 5: End-to-End Traceability Matrix
    p_line(lines, "## 5. End-to-End Cross-Baseline Traceability Matrix")
    p_line(lines, "Complete relational mapping linking each Business Rule upstream to Project Management charters and downstream to planned engineering epics:")
    p_line(lines)
    p_line(lines, "| Business Rule ID | Upstream Objective | Upstream Scope Ref | Upstream Risk Ref | Accountable Role | Downstream Planned Epic | Downstream Test ID | Verification Method |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in BRULE_RULES:
        rule_id = r["id"]
        obj = r["objective_ref"]
        sc = r["scope_ref"]
        risk = r["risk_ref"]
        role = r["role"]
        epic = r["planned_epic"]
        test_id = r["test_id"]
        vmethod = r["verification_method"]
        p_line(lines, f"| [`{rule_id}`](#{rule_id.lower()}) | [`{obj}`](../01-project-management/02-project-vision-and-objectives.md#{obj.lower()}) | [`{sc}`](../01-project-management/04-in-scope.md#{sc.lower()}) | [`{risk}`](../01-project-management/12-project-risks.md#{risk.lower()}) | {role} | `{epic}` | `{test_id}` | {vmethod[:30]}... |")
    p_line(lines)

    # Section 6: Governance & Quality Sign-Off
    p_line(lines, "## 6. Business Rule Governance & Sign-Off")
    p_line(lines, "This Business Rules Specification constitutes the official regulatory and operational constraint baseline for the Namma Clinic Digital Health Platform. Every rule defined herein has been validated against BBMP municipal bylaws, clinical protocols, and pharmacy regulations.")
    p_line(lines)
    p_line(lines, "Any change to business rule decision logic or approval workflows requires formal submission to the Change Control Board under [`docs/01-project-management/18-change-management.md`](../01-project-management/18-change-management.md).")
    p_line(lines)

    content = "\n".join(lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated Document 04: {len(lines)} total lines.")

if __name__ == "__main__":
    generate_business_rules()
