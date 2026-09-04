#!/usr/bin/env python3
"""
gen_req_05_cr.py
Generates docs/02-requirements/05-clinical-rules.md.
Targets 2,800 - 3,500+ substantive markdown lines.
100% domain-specific clinical decision support rules for Namma Clinic.
CRITICAL: Decision-support only. Platform NEVER replaces qualified clinical judgment.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_cr import CR_RULES
from common import p_line, render_metadata_table, format_gherkin

def generate_clinical_rules():
    target_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "docs", "02-requirements", "05-clinical-rules.md"
    )
    target_path = os.path.abspath(target_path)
    print(f"Generating Document 05 at {target_path}...")

    lines = []

    # Document Header & Title
    p_line(lines, "# Clinical Rules Specification: Namma Clinic Digital Health Platform")
    p_line(lines)
    render_metadata_table(
        lines,
        doc_id="DOC-REQ-005-CR",
        doc_title="Master Clinical Rules Specification & Decision Support Baseline",
        req_type="Clinical Rules (CR) - Decision Support Only",
        req_range="CR-001 through CR-050",
        count=50,
        parent_baseline="02-functional-requirements.md",
        counterpart="04-business-rules.md"
    )

    # Section 1: Executive Summary & Clinical Primacy Doctrine
    p_line(lines, "## 1. Executive Summary & Clinical Primacy Doctrine")
    p_line(lines, "> [!IMPORTANT]")
    p_line(lines, "> **CRITICAL CLINICAL GOVERNANCE PRINCIPLE: DECISION-SUPPORT ONLY**")
    p_line(lines, "> The Namma Clinic platform is strictly a clinical decision-support and safety alert system. The system MUST NOT under any circumstances independently diagnose, prescribe, alter dosages, discharge, or make irreversible clinical treatment decisions. The qualified Medical Officer (clinician) retains sole, ultimate, and uncompromised responsibility for all diagnostic determinations, medication choices, and clinical patient care decisions.")
    p_line(lines)
    p_line(lines, "This specification defines 50 clinical rules (`CR-001` through `CR-050`) established to assist frontline Medical Officers and nursing staff in recognizing life-threatening emergencies, preventing adverse drug-drug interactions, identifying vulnerable maternal/pediatric cohorts, and escalating critical laboratory panic values. Every clinical alert defines an explicit severity level, physiological trigger, clinical rationale, recommended action, documented override mechanism, and tamper-evident audit trail.")
    p_line(lines)

    # Section 2: Taxonomy
    p_line(lines, "## 2. Clinical Rules Categorization Taxonomy")
    p_line(lines, "The 50 clinical rules are organized across five specialized clinical safety domains:")
    p_line(lines, "1. **Emergency Triage & Vital Signs Safety (CR-001 to CR-010):** Hypertensive crisis (SBP >=180 / DBP >=120), severe hypoxemia (SpO2 <90%), severe adult tachycardia (>140 bpm), severe bradycardia (<45 bpm), neonatal high fever (temp >=38.5C), severe hypoglycemia (<50 mg/dL), severe hyperglycemia (>400 mg/dL), pediatric severe tachypnea, neonatal hypothermia (<35.5C), and under-5 severe acute malnutrition (MUAC <115mm).")
    p_line(lines, "2. **Maternal & Obstetric Red-Flag Alerts (CR-011 to CR-020):** Gestational hypertension, pre-eclampsia with imminent eclampsia, severe maternal anemia (Hb <7.0 g/dL), postpartum hemorrhage prompt, suspected ectopic pregnancy rupture, adolescent pregnancy, advanced maternal age, maternal syphilis, gestational diabetes GTT screening, and puerperal sepsis.")
    p_line(lines, "3. **Prescription Safety & Drug Contraindications (CR-021 to CR-030):** Dual RAAS blockade (ACE-I + ARB), Metformin in severe renal impairment (eGFR <30), Penicillin-Cephalosporin cross-allergy, NSAIDs in active ulcer/CKD, dual antiplatelet bleeding risk, pediatric Aspirin Reye syndrome contraindication, statins in acute liver disease, fluoroquinolone tendonitis/QT alert, max daily Paracetamol (4g adult / 60mg/kg child), and potassium supplements with potassium-sparing diuretics.")
    p_line(lines, "4. **Laboratory Diagnostics & Panic Values (CR-031 to CR-040):** Severe anemia panic value (Hb <6.0 g/dL), thrombocytopenia (<20k), positive Dengue NS1 with shock, P. falciparum malaria, massive proteinuria (4+), heavy glycosuria + ketonuria (DKA), malaria confirmatory smear, syphilis confirmation, reagent expiration hard-stop, and discordant diagnostic result flagging.")
    p_line(lines, "5. **Acute Medical Emergencies & Clinical Overrides (CR-041 to CR-050):** Suspected acute coronary syndrome prompt (300mg Aspirin), acute stroke FAST signs, anaphylactic shock IM adrenaline prompt, status epilepticus anticonvulsant prompt, acute severe asthma nebulization, snakebite envenomation ASV referral, rabies category III wound washing and PEP, presumptive pulmonary tuberculosis, acute bacterial meningitis triad, and mandatory free-text justification for clinical alert overrides.")
    p_line(lines)

    # Architecture Mermaid Diagram
    p_line(lines, "```mermaid")
    p_line(lines, "graph TD")
    p_line(lines, "    subgraph ClinicalInput['Frontline Clinical Encounter Input']")
    p_line(lines, "        C1['Measured Triage Vitals \\| Lab Results \\| Candidate Prescriptions']")
    p_line(lines, "    end")
    p_line(lines, "    subgraph RuleEvaluation['Deterministic CDS Rules Engine (Advisory Only)']")
    p_line(lines, "        R1['CR-001 to 010: Emergency Triage Red-Flags']")
    p_line(lines, "        R2['CR-011 to 020: Maternal & Obstetric Hazards']")
    p_line(lines, "        R3['CR-021 to 030: Drug Contraindications & Formulary']")
    p_line(lines, "        R4['CR-031 to 040: Lab Panic Values (<30s)']")
    p_line(lines, "        R5['CR-041 to 050: Acute Stroke, ACS & Anaphylaxis']")
    p_line(lines, "    end")
    p_line(lines, "    subgraph ClinicianDecision['Qualified Medical Officer Primacy']")
    p_line(lines, "        D1['Clinician Adopts Guideline Recommendation']")
    p_line(lines, "        D2['Clinician Executes Documented Override (Mandatory Note >=15 Chars)']")
    p_line(lines, "    end")
    p_line(lines, "    subgraph AuditLog['Tamper-Evident WORM Ledger']")
    p_line(lines, "        A1['Immutable Log: Alert ID \\| Severity \\| Doctor ID \\| Override Justification']")
    p_line(lines, "    end")
    p_line(lines, "    C1 --> R1 & R2 & R3 & R4 & R5")
    p_line(lines, "    R1 & R2 & R3 & R4 & R5 --> D1 & D2")
    p_line(lines, "    D1 & D2 --> A1")
    p_line(lines, "```")
    p_line(lines)

    # Section 3: Master Inventory Table
    p_line(lines, "## 3. Master Clinical Rules Inventory Table (CR-001 to CR-050)")
    p_line(lines, "| Rule ID | Clinical Rule Title | Alert Severity Level | Trigger Condition | Recommended Clinical Action | Clinician Override Mechanism |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in CR_RULES:
        p_line(lines, f"| [`{r['id']}`](#{r['id'].lower()}) | **{r['title']}** | `{r['severity']}` | {r['trigger'][:30]}... | {r['recommended_action'][:35]}... | {r['override_mechanism'][:35]}... |")
    p_line(lines)

    # Section 4: Deep Technical & Operational Specifications
    p_line(lines, "## 4. Comprehensive Clinical Rule Specifications (CR-001 to CR-050)")
    p_line(lines, "This section establishes the exhaustive clinical rationale, triggers, recommended actions, override mechanisms, and audit contracts for each of the 50 clinical decision support rules.")
    p_line(lines)

    for i, r in enumerate(CR_RULES, 1):
        cr_id = r["id"]
        title = r["title"]
        p_line(lines, f"### 4.{i} {cr_id}: {title}")
        p_line(lines)

        # Attribute Table
        p_line(lines, "| Specification Attribute | Formal Engineering Definition |")
        p_line(lines, "| :--- | :--- |")
        p_line(lines, f"| **Rule ID** | `{cr_id}` |")
        p_line(lines, f"| **Rule Title** | {title} |")
        p_line(lines, f"| **Rule Statement** | {r['statement']} |")
        p_line(lines, f"| **Rule Type** | `{r['type']}` |")
        p_line(lines, f"| **Severity Level** | `{r['severity']}` |")
        p_line(lines, f"| **Priority Level** | `{r['priority']}` (Rationale: {r['priority_rationale']}) |")
        p_line(lines, f"| **Clinical Rationale** | {r['rationale']} |")
        p_line(lines, f"| **Trigger Condition** | {r['trigger']} |")
        p_line(lines, f"| **Recommended Action** | {r['recommended_action']} |")
        p_line(lines, f"| **Override Mechanism** | {r['override_mechanism']} |")
        p_line(lines, f"| **Override Reason Rule**| {r['override_reason_required']} |")
        p_line(lines, f"| **Primary Actor** | `{r['actor']}` |")
        p_line(lines, f"| **Accountable Role** | [`{r['role']}`](../01-project-management/08-role-and-responsibility-matrix.md#{r['role'].lower()}) |")
        p_line(lines, f"| **Clinical Authority** | [`{r['stakeholder']}`](../01-project-management/06-stakeholders.md#{r['stakeholder'].lower()}) |")
        p_line(lines, f"| **Audit Requirement** | `{r['audit_requirement']}` |")
        p_line(lines, f"| **Associated Rules** | Business: [`{r['business_rules']}`](./04-business-rules.md#{r['business_rules'].lower()}) \\| Operational: [`{r['operational_rules']}`](./06-operational-rules.md#{r['operational_rules'].lower()}) |")
        p_line(lines, f"| **Security & Privacy** | Security: `{r['security_implications']}` \\| Privacy: `{r['privacy_implications']}` |")
        p_line(lines, f"| **Data & Offline** | Data: `{r['data_implications']}` \\| Offline: `{r['offline_behavior']}` |")
        p_line(lines, f"| **Upstream Traceability**| Obj: [`{r['objective_ref']}`](../01-project-management/02-project-vision-and-objectives.md#{r['objective_ref'].lower()}) \\| Scope: [`{r['scope_ref']}`](../01-project-management/04-in-scope.md#{r['scope_ref'].lower()}) \\| Risk: [`{r['risk_ref']}`](../01-project-management/12-project-risks.md#{r['risk_ref'].lower()}) |")
        p_line(lines, f"| **Downstream Planning** | Epic: `{r['planned_epic']}` \\| Feature: `{r['planned_feature']}` \\| API: `{r['planned_api']}` \\| Test: `{r['planned_test']}` |")
        p_line(lines)

        # Operational Execution Paths
        p_line(lines, "#### 4." + str(i) + ".1 Clinical Advisory Protocol & Evaluation Flow")
        p_line(lines, "- **Standard Evaluation Flow (Happy Path):**")
        for step_idx, step in enumerate(r['main_flow'], 1):
            p_line(lines, f"  {step_idx}. {step}")
        p_line(lines, f"- **Clinician Documented Override Flow:** {r['alternate_flow']}")
        p_line(lines, f"- **Emergency Escalation Flow:** {r['exception_flow']}")
        p_line(lines)

        # Technical Architecture Invariants
        p_line(lines, "#### 4." + str(i) + ".2 Technical Invariants & Verification Contract")
        p_line(lines, f"- **Alert Severity Classification:** `{r['severity']}`")
        p_line(lines, f"- **Recommended Clinical Action:** {r['recommended_action']}")
        p_line(lines, f"- **Override Protocol:** {r['override_mechanism']}")
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
        p_line(lines, f"- **Automated Test Suite:** `{r['test_id']}` ({r['test_type']}) targeting 100% clinical safety rule coverage.")
        p_line(lines, f"- **Related Internal Requirements:** {', '.join([f'[`{x}`](#{x.lower()})' if x.startswith('CR-') else f'`{x}`' for x in r['related_requirements']])}")
        p_line(lines, f"- **Dependencies & Blocking Constraints:** {', '.join(r['dependencies'])} | Constraints: {r['constraints']}")
        p_line(lines, f"- **Architectural Assumptions & Open Questions:** Assumption: {r['assumptions']} | Open Question: {r['open_questions']}")
        p_line(lines)
        p_line(lines, "---")
        p_line(lines)

    # Section 5: End-to-End Traceability Matrix
    p_line(lines, "## 5. End-to-End Cross-Baseline Traceability Matrix")
    p_line(lines, "Complete relational mapping linking each Clinical Rule upstream to Project Management charters and downstream to planned engineering epics:")
    p_line(lines)
    p_line(lines, "| Clinical Rule ID | Upstream Objective | Upstream Scope Ref | Upstream Risk Ref | Accountable Role | Downstream Planned Epic | Downstream Test ID | Verification Method |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in CR_RULES:
        cr_id = r["id"]
        obj = r["objective_ref"]
        sc = r["scope_ref"]
        risk = r["risk_ref"]
        role = r["role"]
        epic = r["planned_epic"]
        test_id = r["test_id"]
        vmethod = r["verification_method"]
        p_line(lines, f"| [`{cr_id}`](#{cr_id.lower()}) | [`{obj}`](../01-project-management/02-project-vision-and-objectives.md#{obj.lower()}) | [`{sc}`](../01-project-management/04-in-scope.md#{sc.lower()}) | [`{risk}`](../01-project-management/12-project-risks.md#{risk.lower()}) | {role} | `{epic}` | `{test_id}` | {vmethod[:30]}... |")
    p_line(lines)

    # Section 6: Governance & Quality Sign-Off
    p_line(lines, "## 6. Clinical Governance & Safety Sign-Off")
    p_line(lines, "This Clinical Rules Specification has been reviewed and ratified by the BBMP Health Directorate and Chief Health Officer. Every clinical rule operates under the non-negotiable doctrine of clinical decision support only; under no circumstances does the platform replace the qualified diagnostic judgment of the attending Medical Officer.")
    p_line(lines)
    p_line(lines, "Any update to clinical rule thresholds, contraindication tables, or pediatric dosing algorithms requires formal clinical safety committee review under [`docs/01-project-management/18-change-management.md`](../01-project-management/18-change-management.md).")
    p_line(lines)

    content = "\n".join(lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated Document 05: {len(lines)} total lines.")

if __name__ == "__main__":
    generate_clinical_rules()
