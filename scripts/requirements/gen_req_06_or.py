#!/usr/bin/env python3
"""
gen_req_06_or.py
Generates docs/02-requirements/06-operational-rules.md.
Targets 2,800 - 3,500+ substantive markdown lines.
100% domain-specific facility governance and standard operating procedures for Namma Clinic.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_or import OR_RULES
from common import p_line, render_metadata_table, format_gherkin

def generate_operational_rules():
    target_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "docs", "02-requirements", "06-operational-rules.md"
    )
    target_path = os.path.abspath(target_path)
    print(f"Generating Document 06 at {target_path}...")

    lines = []

    # Document Header & Title
    p_line(lines, "# Operational Rules Specification: Namma Clinic Digital Health Platform")
    p_line(lines)
    render_metadata_table(
        lines,
        doc_id="DOC-REQ-006-OR",
        doc_title="Master Operational Rules Specification & Facility Governance Baseline",
        req_type="Operational Rules (OR)",
        req_range="OR-001 through OR-050",
        count=50,
        parent_baseline="01-business-requirements.md",
        counterpart="04-business-rules.md"
    )

    # Section 1: Executive Summary & Facility Governance Framework
    p_line(lines, "## 1. Executive Summary & Facility Governance Framework")
    p_line(lines, "This specification establishes the authoritative standard operating procedures (SOPs) and operational rules (`OR-001` through `OR-050`) governing the daily operation, hardware readiness, shift handovers, emergency escalations, and end-of-day reconciliations across all 183 Namma Clinics in Greater Bengaluru. Operational rules bridge software capabilities with physical facility discipline, ensuring that computers, power backups, cold-chain refrigerators, thermal printers, diagnostic reagents, and staff rosters maintain continuous operational readiness.")
    p_line(lines)
    p_line(lines, "Every operational rule defines explicit pre-flight trigger events, standard operating protocols, hardware verification checks, offline resilience protocols, shift handover mandates, daily reconciliation requirements, supervisor sign-off gates, and tamper-evident audit trails.")
    p_line(lines)

    # Section 2: Taxonomy
    p_line(lines, "## 2. Operational Rules Categorization Taxonomy")
    p_line(lines, "The 50 operational rules are structured across five specialized facility operational domains:")
    p_line(lines, "1. **Morning Opening & Hardware Readiness Protocols (OR-001 to OR-010):** 08:30 IST facility unlocking, crash cart verification, cold chain temperature check (+2C to +8C), thermal printer test slip, dual-desk hardware verification, IndexedDB database integrity check, pending sync queue backlog verification, 2D barcode scanner calibration, potable water inspection, and biometric roster attendance.")
    p_line(lines, "2. **Clinical Desk Preparation & Session Initialization (OR-011 to OR-020):** Daily token pool start (001), nursing diagnostic kit setup, doctor KMC credential verification, lab reagent temperature check, pharmacy scanner activation, battery/UPS status check, network DNS baseline probe, master formulary differential sync, daily token ceiling configuration, and wheelchair accessibility verification.")
    p_line(lines, "3. **Midday Operational Management & Queue Balancing (OR-021 to OR-030):** 13:00 IST queue load balancing, midday pharmacy stock spot-checks, staggered lunch rotations, sudden network outage offline mode activation, extended power outage battery conservation, emergency patient fast-track protocol, biomedical waste color-coded segregation, sharps container 75% fill replacement, lab waste chemical decontamination, and midday facility sanitation.")
    p_line(lines, "4. **Evening Facility Closure & Reconciliation (OR-031 to OR-040):** 17:30 IST closure checklist, open patient token reconciliation, unfulfilled prescription review, physical pharmacy count vs digital ledger audit, near-expiry quarantine verification, lab specimen clearance, daily OPD census sign-off, daily IHIP Form P surveillance submission, final sync queue flushing (18:00 IST cutoff), and terminal lockdown.")
    p_line(lines, "5. **Escalations, Maintenance & Supervisory Audits (OR-041 to OR-050):** IT helpdesk 30-minute breakdown escalation, cold chain breach 15-minute escalation, emergency drug stockout indenting, staff conflict de-escalation, infrastructure failure hospital divert, weekly deep cleaning and autoclaving, bi-weekly fire safety inspection, monthly offline restoration drills, quarterly zonal inspection readiness, and mandatory 3-year archival of signed reconciliation slips.")
    p_line(lines)

    # Architecture Mermaid Diagram
    p_line(lines, "```mermaid")
    p_line(lines, "graph TD")
    p_line(lines, "    subgraph MorningShift['Morning Opening Phase: 08:30 - 09:00 IST']")
    p_line(lines, "        M1['OR-001 to 010:<br/>Facility Unlock, Power & Hardware Readiness']")
    p_line(lines, "        M2['OR-011 to 020:<br/>Desk Setup, Cold Chain & Roster Login']")
    p_line(lines, "    end")
    p_line(lines, "    subgraph MiddayShift['Operational Midday Phase: 09:00 - 17:30 IST']")
    p_line(lines, "        D1['OR-021 to 030:<br/>Queue Balancing, Offline Fallback & Waste SOP']")
    p_line(lines, "    end")
    p_line(lines, "    subgraph EveningShift['Evening Reconciliation Phase: 17:30 - 18:05 IST']")
    p_line(lines, "        E1['OR-031 to 040:<br/>Token Reconciliation, Stock Audit & Sync Flush']")
    p_line(lines, "    end")
    p_line(lines, "    subgraph SupervisoryAssurance['Governance & Escalation Protocols']")
    p_line(lines, "        S1['OR-041 to 050:<br/>Helpdesk SLAs, Cold Chain Alerts & Drills']")
    p_line(lines, "    end")
    p_line(lines, "    M1 --> M2 --> D1 --> E1")
    p_line(lines, "    D1 -.-> S1")
    p_line(lines, "    E1 --> S1")
    p_line(lines, "```")
    p_line(lines)

    # Section 3: Master Inventory Table
    p_line(lines, "## 3. Master Operational Rules Inventory Table (OR-001 to OR-050)")
    p_line(lines, "| Rule ID | Operational Rule Title | Milestone Trigger | Standard Operational Protocol | Hardware Readiness Expectation | Supervisor Approval Gate |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in OR_RULES:
        p_line(lines, f"| [`{r['id']}`](#{r['id'].lower()}) | **{r['title']}** | {r['trigger'][:30]}... | {r['operational_protocol'][:35]}... | {r['hardware_readiness'][:35]}... | {r['supervisor_approval'][:30]}... |")
    p_line(lines)

    # Section 4: Deep Technical & Operational Specifications
    p_line(lines, "## 4. Comprehensive Operational Rule Specifications (OR-001 to OR-050)")
    p_line(lines, "This section establishes the exhaustive standard operating procedures, hardware readiness expectations, offline behavior, and audit requirements for each of the 50 operational facility rules.")
    p_line(lines)

    for i, r in enumerate(OR_RULES, 1):
        or_id = r["id"]
        title = r["title"]
        p_line(lines, f"### 4.{i} {or_id}: {title}")
        p_line(lines)

        # Attribute Table
        p_line(lines, "| Specification Attribute | Formal Engineering Definition |")
        p_line(lines, "| :--- | :--- |")
        p_line(lines, f"| **Rule ID** | `{or_id}` |")
        p_line(lines, f"| **Rule Title** | {title} |")
        p_line(lines, f"| **Rule Statement** | {r['statement']} |")
        p_line(lines, f"| **Rule Type** | `{r['type']}` |")
        p_line(lines, f"| **Priority Level** | `{r['priority']}` (Rationale: {r['priority_rationale']}) |")
        p_line(lines, f"| **Business Value** | {r['business_value']} |")
        p_line(lines, f"| **Operational Rationale**| {r['rationale']} |")
        p_line(lines, f"| **Trigger Condition** | {r['trigger']} |")
        p_line(lines, f"| **Standard Operating Protocol**| {r['operational_protocol']} |")
        p_line(lines, f"| **Hardware Readiness** | {r['hardware_readiness']} |")
        p_line(lines, f"| **Offline Mode Behavior**| {r['offline_behavior']} |")
        p_line(lines, f"| **Shift Handover Mandate**| {r['shift_handover']} |")
        p_line(lines, f"| **Daily Reconciliation** | {r['daily_reconciliation']} |")
        p_line(lines, f"| **Supervisor Approval Gate**| {r['supervisor_approval']} |")
        p_line(lines, f"| **Primary Actor** | `{r['actor']}` |")
        p_line(lines, f"| **Accountable Role** | [`{r['role']}`](../01-project-management/08-role-and-responsibility-matrix.md#{r['role'].lower()}) |")
        p_line(lines, f"| **Key Stakeholder** | [`{r['stakeholder']}`](../01-project-management/06-stakeholders.md#{r['stakeholder'].lower()}) |")
        p_line(lines, f"| **Audit Requirement** | `{r['audit_requirement']}` |")
        p_line(lines, f"| **Associated Rules** | Business: [`{r['business_rules']}`](./04-business-rules.md#{r['business_rules'].lower()}) \\| Clinical: [`{r['clinical_rules']}`](./05-clinical-rules.md#{r['clinical_rules'].lower()}) |")
        p_line(lines, f"| **Security & Privacy** | Security: `{r['security_implications']}` \\| Privacy: `{r['privacy_implications']}` |")
        p_line(lines, f"| **Data & Offline** | Data: `{r['data_implications']}` \\| Sync: `{r['synchronization_implications']}` |")
        p_line(lines, f"| **Upstream Traceability**| Obj: [`{r['objective_ref']}`](../01-project-management/02-project-vision-and-objectives.md#{r['objective_ref'].lower()}) \\| Scope: [`{r['scope_ref']}`](../01-project-management/04-in-scope.md#{r['scope_ref'].lower()}) \\| Risk: [`{r['risk_ref']}`](../01-project-management/12-project-risks.md#{r['risk_ref'].lower()}) |")
        p_line(lines, f"| **Downstream Planning** | Epic: `{r['planned_epic']}` \\| Feature: `{r['planned_feature']}` \\| API: `{r['planned_api']}` \\| Test: `{r['planned_test']}` |")
        p_line(lines)

        # Operational Execution Paths
        p_line(lines, "#### 4." + str(i) + ".1 Standard Operating Procedure & Execution Sequence")
        p_line(lines, "- **Standard Execution Flow (Happy Path):**")
        for step_idx, step in enumerate(r['main_flow'], 1):
            p_line(lines, f"  {step_idx}. {step}")
        p_line(lines, f"- **Offline Fallback Execution Flow:** {r['alternate_flow']}")
        p_line(lines, f"- **Deficiency Escalation Flow:** {r['exception_flow']}")
        p_line(lines)

        # Technical Architecture Invariants
        p_line(lines, "#### 4." + str(i) + ".2 Technical Invariants & Hardware Readiness Contract")
        p_line(lines, f"- **Hardware Readiness Mandate:** {r['hardware_readiness']}")
        p_line(lines, f"- **Offline Resilience Protocol:** {r['offline_behavior']}")
        p_line(lines, f"- **Supervisor Sign-Off Gate:** {r['supervisor_approval']}")
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
        p_line(lines, f"- **Automated Test Suite:** `{r['test_id']}` ({r['test_type']}) targeting 100% facility SOP compliance.")
        p_line(lines, f"- **Related Internal Requirements:** {', '.join([f'[`{x}`](#{x.lower()})' if x.startswith('OR-') else f'`{x}`' for x in r['related_requirements']])}")
        p_line(lines, f"- **Dependencies & Blocking Constraints:** {', '.join(r['dependencies'])} | Constraints: {r['constraints']}")
        p_line(lines, f"- **Architectural Assumptions & Open Questions:** Assumption: {r['assumptions']} | Open Question: {r['open_questions']}")
        p_line(lines)
        p_line(lines, "---")
        p_line(lines)

    # Section 5: End-to-End Traceability Matrix
    p_line(lines, "## 5. End-to-End Cross-Baseline Traceability Matrix")
    p_line(lines, "Complete relational mapping linking each Operational Rule upstream to Project Management charters and downstream to planned engineering epics:")
    p_line(lines)
    p_line(lines, "| Operational Rule ID | Upstream Objective | Upstream Scope Ref | Upstream Risk Ref | Accountable Role | Downstream Planned Epic | Downstream Test ID | Verification Method |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in OR_RULES:
        or_id = r["id"]
        obj = r["objective_ref"]
        sc = r["scope_ref"]
        risk = r["risk_ref"]
        role = r["role"]
        epic = r["planned_epic"]
        test_id = r["test_id"]
        vmethod = r["verification_method"]
        p_line(lines, f"| [`{or_id}`](#{or_id.lower()}) | [`{obj}`](../01-project-management/02-project-vision-and-objectives.md#{obj.lower()}) | [`{sc}`](../01-project-management/04-in-scope.md#{sc.lower()}) | [`{risk}`](../01-project-management/12-project-risks.md#{risk.lower()}) | {role} | `{epic}` | `{test_id}` | {vmethod[:30]}... |")
    p_line(lines)

    # Section 6: Governance & Quality Sign-Off
    p_line(lines, "## 6. Facility Operational Governance & Quality Sign-Off")
    p_line(lines, "This Operational Rules Specification constitutes the authoritative standard operating procedure baseline for all 183 primary Namma Clinics in Greater Bengaluru. Compliance with these rules is subject to random inspection audits by BBMP Zonal Health Officers.")
    p_line(lines)
    p_line(lines, "Revisions to facility operational checklists, cold chain thresholds, or daily closing protocols must follow formal Change Control Board evaluation under [`docs/01-project-management/18-change-management.md`](../01-project-management/18-change-management.md).")
    p_line(lines)

    content = "\n".join(lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated Document 06: {len(lines)} total lines.")

if __name__ == "__main__":
    generate_operational_rules()
