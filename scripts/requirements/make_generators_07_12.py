#!/usr/bin/env python3
"""
make_generators_07_12.py
Creates generator scripts:
  - gen_req_07_secr.py
  - gen_req_08_priv.py
  - gen_req_09_perf.py
  - gen_req_10_avail.py
  - gen_req_11_loc.py
  - gen_req_12_a11y.py
"""

import os

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

def create_generators():
    # -------------------------------------------------------------
    # 1. gen_req_07_secr.py
    # -------------------------------------------------------------
    secr_code = '''#!/usr/bin/env python3
"""
gen_req_07_secr.py
Generates docs/02-requirements/07-security-requirements.md.
Targets 3,000 - 3,800+ substantive markdown lines.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_secr import SECR_REQUIREMENTS
from common import p_line, render_metadata_table, format_gherkin

def generate_security_requirements():
    target_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "docs", "02-requirements", "07-security-requirements.md"
    )
    target_path = os.path.abspath(target_path)
    print(f"Generating Document 07 at {target_path}...")

    lines = []

    p_line(lines, "# Security Requirements Specification: Namma Clinic Digital Health Platform")
    p_line(lines)
    render_metadata_table(
        lines,
        doc_id="DOC-REQ-007-SECR",
        doc_title="Master Security Requirements & Cryptographic Controls Baseline",
        req_type="Security Requirements (SECR)",
        req_range="SECR-001 through SECR-050",
        count=50,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="08-privacy-requirements.md"
    )

    p_line(lines, "## 1. Executive Summary & Security Governance Framework")
    p_line(lines, "This specification defines the comprehensive, implementation-ready security requirements baseline for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. Comprising 50 rigorous, verifiable security specifications (`SECR-001` through `SECR-050`), this document establishes mandatory cryptographic invariants, role-based and attribute-based access controls, session hardening, defense-in-depth mitigations against OWASP Top 10 vulnerabilities, immutable audit trails, and strict software supply chain security controls.")
    p_line(lines)
    p_line(lines, "All technical specifications comply with the Digital Information Security in Healthcare Act (DISHA) guidelines, CERT-In cybersecurity directives, National Health Authority (NHA) ABDM security architecture, and ISO/IEC 27001 standards. Every requirement incorporates explicit threat models, concrete attack vectors, defense-in-depth security controls, verification test suites, and executable BDD Gherkin scenarios.")
    p_line(lines)

    p_line(lines, "## 2. Security Architecture & Threat Modeling Framework")
    p_line(lines, "The security controls operate across four distinct defensive tiers: Perimeter & Transport Security, Application & Identity Governance, Client Storage & Offline Hardening, and Infrastructure & Supply Chain Integrity.")
    p_line(lines)
    p_line(lines, "```mermaid")
    p_line(lines, "graph TD")
    p_line(lines, "    subgraph Perimeter[\"Perimeter & Transport Security\"]")
    p_line(lines, "        WAF[\"Cloud WAF \\| Rate Limiter \\| DDoS Mitigation\"]")
    p_line(lines, "        TLS[\"TLS 1.3 Transport Encryption \\| HSTS \\| Forward Secrecy\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph Identity[\"Identity & Access Governance\"]")
    p_line(lines, "        AUTH[\"Argon2id Passwords \\| TOTP MFA \\| Brute-Force Shield\"]")
    p_line(lines, "        RBAC[\"Dual-Layer RBAC \\| Fine-Grained Least Privilege\"]")
    p_line(lines, "        JWT[\"Short-Lived RS256 JWTs \\| Redis Token Revocation\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph Storage[\"Storage & Cryptographic Controls\"]")
    p_line(lines, "        DB_ENC[\"PostgreSQL AES-256-GCM Transparent Data Encryption\"]")
    p_line(lines, "        CLIENT_ENC[\"Web Cryptography AES-256 Client IndexedDB Encryption\"]")
    p_line(lines, "        WORM[\"Immutable Audit Vault \\| HMAC-SHA256 Chaining\"]")
    p_line(lines, "    end")
    p_line(lines, "    WAF --> TLS --> AUTH --> RBAC --> JWT --> DB_ENC")
    p_line(lines, "    AUTH -.-> WORM")
    p_line(lines, "    CLIENT_ENC -.-> WORM")
    p_line(lines, "```")
    p_line(lines)

    p_line(lines, "## 3. Master Security Requirements Inventory Table (SECR-001 to SECR-050)")
    p_line(lines, "| Security Req ID | Security Control Title | Threat Category | Priority | Threat Vector & Attack Scenario | Security Control Specification | Verification Method |")
    p_line(lines, "| :--- | :--- | :--- | :---: | :--- | :--- | :--- |")
    for r in SECR_REQUIREMENTS:
        p_line(lines, f"| [`{r['id']}`](#{r['id'].lower()}) | **{r['title']}** | `{r['domain']}` | `{r['priority']}` | `{r['threat'][:35]}...` | `{r['control'][:40]}...` | {r['verification_method'][:30]}... |")
    p_line(lines)

    p_line(lines, "## 4. Comprehensive Security Requirement Specifications (SECR-001 to SECR-050)")
    p_line(lines, "This section provides exhaustive engineering specifications for each of the 50 security requirements governing the Namma Clinic platform.")
    p_line(lines)

    for i, r in enumerate(SECR_REQUIREMENTS, 1):
        req_id = r["id"]
        title = r["title"]
        p_line(lines, f"### 4.{i} {req_id}: {title}")
        p_line(lines)

        p_line(lines, "| Specification Attribute | Formal Engineering Definition |")
        p_line(lines, "| :--- | :--- |")
        p_line(lines, f"| **Requirement ID** | `{req_id}` |")
        p_line(lines, f"| **Requirement Title** | {title} |")
        p_line(lines, f"| **Requirement Statement**| {r['statement']} |")
        p_line(lines, f"| **Requirement Type** | `{r['type']}` |")
        p_line(lines, f"| **Priority Level** | `{r['priority']}` (Rationale: {r['priority_rationale']}) |")
        p_line(lines, f"| **Business Value** | {r['business_value']} |")
        p_line(lines, f"| **Engineering Rationale**| {r['rationale']} |")
        p_line(lines, f"| **Primary Threat** | **{r['threat']}** |")
        p_line(lines, f"| **Attack Scenario** | {r['attack_scenario']} |")
        p_line(lines, f"| **Security Control** | {r['control']} |")
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
        p_line(lines, f"| **Security & Privacy** | Security: `{r['security_implications']}` \\| Privacy: `{r['privacy_implications']}` |")
        p_line(lines, f"| **Data & Audit** | Data: `{r['data_implications']}` \\| Audit: `{r['audit_requirements']}` |")
        p_line(lines, f"| **Offline & Sync** | Offline: `{r['offline_behavior']}` \\| Sync: `{r['synchronization_implications']}` |")
        p_line(lines, f"| **Quality Expectations**| Perf: `{r['performance_expectations']}` \\| Avail: `{r['availability_expectations']}` |")
        p_line(lines, f"| **Localization & A11y**| Loc: `{r['localization_expectations']}` \\| A11y: `{r['accessibility_expectations']}` |")
        p_line(lines, f"| **Failure & Recovery** | Failure: {r['failure_behavior']} \\| Recovery: {r['recovery_behavior']} |")
        p_line(lines, f"| **Observability** | Logging: `{r['logging_requirements']}` \\| Metrics: `{r['metrics']}` |")
        p_line(lines, f"| **Upstream Traceability**| Obj: [`{r['objective_ref']}`](../01-project-management/02-project-vision-and-objectives.md#{r['objective_ref'].lower()}) \\| Scope: [`{r['scope_ref']}`](../01-project-management/04-in-scope.md#{r['scope_ref'].lower()}) \\| Risk: [`{r['risk_ref']}`](../01-project-management/12-project-risks.md#{r['risk_ref'].lower()}) |")
        p_line(lines, f"| **Downstream Planning** | Epic: `{r['planned_epic']}` \\| Feature: `{r['planned_feature']}` \\| API: `{r['planned_api']}` \\| DB: `{r['planned_db']}` \\| Test: `{r['planned_test']}` |")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".1 Operational Execution Protocol & Security Invariants")
        p_line(lines, "- **Continuous Security Enforcement Workflow:**")
        for step_idx, step in enumerate(r['main_flow'], 1):
            p_line(lines, f"  {step_idx}. {step}")
        p_line(lines, f"- **Degraded State Fallback Path:** {r['alternate_flow']}")
        p_line(lines, f"- **Security Exception & Incident Escalation Path:** {r['exception_flow']}")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".2 Technical Invariants & Threat Mitigation Contract")
        p_line(lines, f"- **Threat Vector:** {r['threat']}")
        p_line(lines, f"- **Attack Scenario Simulation:** {r['attack_scenario']}")
        p_line(lines, f"- **Enforced Security Control:** {r['control']}")
        p_line(lines, f"- **Verification Protocol:** {r['verification_method']}")
        p_line(lines, f"- **Accountable Security Owner:** {r['owner']}")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".3 Executable BDD Acceptance Scenarios")
        gherkin_block = format_gherkin(r)
        for gh_l in gherkin_block:
            p_line(lines, gh_l)
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".4 Verification Protocol & Quality Sign-Off")
        p_line(lines, f"- **Verification Method:** {r['verification_method']}")
        p_line(lines, f"- **Automated Security Test:** `{r['test_id']}` ({r['test_type']}) targeting zero unmitigated vulnerabilities.")
        p_line(lines, f"- **Related Internal Requirements:** {', '.join([f'[`{x}`](#{x.lower()})' if x.startswith('SECR-') else f'`{x}`' for x in r['related_requirements']])}")
        p_line(lines, f"- **Dependencies & Blocking Constraints:** {', '.join(r['dependencies'])} | Constraints: {r['constraints']}")
        p_line(lines, f"- **Architectural Assumptions & Open Questions:** Assumption: {r['assumptions']} | Open Question: {r['open_questions']}")
        p_line(lines)
        p_line(lines, "---")
        p_line(lines)

    p_line(lines, "## 5. End-to-End Cross-Baseline Traceability Matrix")
    p_line(lines, "Relational mapping tracing each Security Requirement upstream to project management objectives and downstream to security test suites:")
    p_line(lines)
    p_line(lines, "| Security Req ID | Upstream Objective | Upstream Scope Ref | Upstream Risk Ref | Security Owner | Downstream Planned Epic | Downstream Test ID | Verification Method |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in SECR_REQUIREMENTS:
        req_id = r["id"]
        obj = r["objective_ref"]
        sc = r["scope_ref"]
        risk = r["risk_ref"]
        owner = r["owner"]
        epic = r["planned_epic"]
        test_id = r["test_id"]
        vmethod = r["verification_method"]
        p_line(lines, f"| [`{req_id}`](#{req_id.lower()}) | [`{obj}`](../01-project-management/02-project-vision-and-objectives.md#{obj.lower()}) | [`{sc}`](../01-project-management/04-in-scope.md#{sc.lower()}) | [`{risk}`](../01-project-management/12-project-risks.md#{risk.lower()}) | {owner} | `{epic}` | `{test_id}` | {vmethod[:30]}... |")
    p_line(lines)

    p_line(lines, "## 6. Security Governance, Continuous Compliance & Threat Sign-Off")
    p_line(lines, "This Security Requirements Specification represents the non-negotiable security baseline for the Namma Clinic Platform. All commits, pull requests, and releases are validated against automated SAST/DAST/Secret scanning tools in CI. Zero critical or high vulnerabilities are permitted in production artifacts.")
    p_line(lines)

    content = "\\n".join(lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated Document 07: {len(lines)} total lines.")

if __name__ == "__main__":
    generate_security_requirements()
'''
    with open(os.path.join(DIR_PATH, "gen_req_07_secr.py"), "w", encoding="utf-8") as f:
        f.write(secr_code)

    # -------------------------------------------------------------
    # 2. gen_req_08_priv.py
    # -------------------------------------------------------------
    priv_code = '''#!/usr/bin/env python3
"""
gen_req_08_priv.py
Generates docs/02-requirements/08-privacy-requirements.md.
Targets 3,000 - 3,800+ substantive markdown lines.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_priv import PRIV_REQUIREMENTS
from common import p_line, render_metadata_table, format_gherkin

def generate_privacy_requirements():
    target_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "docs", "02-requirements", "08-privacy-requirements.md"
    )
    target_path = os.path.abspath(target_path)
    print(f"Generating Document 08 at {target_path}...")

    lines = []

    p_line(lines, "# Privacy & Data Protection Requirements Specification: Namma Clinic Digital Health Platform")
    p_line(lines)
    render_metadata_table(
        lines,
        doc_id="DOC-REQ-008-PRIV",
        doc_title="Master Privacy Requirements & Data Protection Baseline",
        req_type="Privacy Requirements (PRIV)",
        req_range="PRIV-001 through PRIV-050",
        count=50,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="07-security-requirements.md"
    )

    p_line(lines, "## 1. Executive Summary & Privacy Governance Framework")
    p_line(lines, "This specification defines the authoritative, implementation-ready privacy and data protection requirements baseline for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. Comprising 50 comprehensive privacy specifications (`PRIV-001` through `PRIV-050`), this document operationalizes the legal and ethical mandates of India's Digital Personal Data Protection (DPDP) Act 2023, the DISHA guidelines, and the National Health Authority (NHA) ABDM consent framework.")
    p_line(lines)
    p_line(lines, "Every privacy requirement establishes an explicit lawful basis for processing, purposeful data minimization bounds, strict retention and automatic purging schedules, granular patient consent mechanisms, data subject rights (access, correction, erasure, withdrawal), and privacy-preserving de-identification/k-anonymity for public health epidemiology.")
    p_line(lines)

    p_line(lines, "## 2. Privacy Architecture & Data Subject Lifecycle")
    p_line(lines, "The privacy architecture enforces privacy-by-design and privacy-by-default across every transaction, ensuring patient health records remain strictly confidential and accessed solely on a need-to-know clinical basis.")
    p_line(lines)
    p_line(lines, "```mermaid")
    p_line(lines, "graph TD")
    p_line(lines, "    subgraph PatientNotice[\"Notice & Consent Tier\"]")
    p_line(lines, "        NOTICE[\"Bilingual Notice (Kannada/English) \\| Plain Language\"]")
    p_line(lines, "        CONSENT[\"Granular DPDP Consent Capture \\| Digital Thumbprint/Signature\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph Processing[\"Lawful Processing & Boundary Control\"]")
    p_line(lines, "        PURPOSE[\"Purpose Limitation \\| Clinical Care vs Epidemiology\"]")
    p_line(lines, "        MIN[\"Data Minimization \\| Redacted PII on Public Views\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph Governance[\"Rights & Lifecycle Vault\"]")
    p_line(lines, "        RIGHTS[\"Data Subject Rights: Access \\| Rectification \\| Erasure\"]")
    p_line(lines, "        ANON[\"k-Anonymity (k>=5) \\| Differential Privacy Engine\"]")
    p_line(lines, "        PURGE[\"Automated Retention Enforcer \\| Cryptographic Erasure\"]")
    p_line(lines, "    end")
    p_line(lines, "    NOTICE --> CONSENT --> PURPOSE --> MIN --> RIGHTS")
    p_line(lines, "    PURPOSE --> ANON")
    p_line(lines, "    MIN --> PURGE")
    p_line(lines, "```")
    p_line(lines)

    p_line(lines, "## 3. Master Privacy Requirements Inventory Table (PRIV-001 to PRIV-050)")
    p_line(lines, "| Privacy Req ID | Privacy Principle Title | DPDP Domain | Priority | Lawful Processing Basis | Privacy Impact & Invariants | Data Protection Officer |")
    p_line(lines, "| :--- | :--- | :--- | :---: | :--- | :--- | :--- |")
    for r in PRIV_REQUIREMENTS:
        p_line(lines, f"| [`{r['id']}`](#{r['id'].lower()}) | **{r['title']}** | `{r['domain']}` | `{r['priority']}` | `{r['lawful_basis'][:35]}...` | `{r['privacy_impact'][:40]}...` | {r['dpo_owner']} |")
    p_line(lines)

    p_line(lines, "## 4. Comprehensive Privacy Requirement Specifications (PRIV-001 to PRIV-050)")
    p_line(lines, "This section establishes the exhaustive engineering, legal, and operational specifications for each of the 50 privacy requirements governing the Namma Clinic platform.")
    p_line(lines)

    for i, r in enumerate(PRIV_REQUIREMENTS, 1):
        req_id = r["id"]
        title = r["title"]
        p_line(lines, f"### 4.{i} {req_id}: {title}")
        p_line(lines)

        p_line(lines, "| Specification Attribute | Formal Engineering Definition |")
        p_line(lines, "| :--- | :--- |")
        p_line(lines, f"| **Requirement ID** | `{req_id}` |")
        p_line(lines, f"| **Requirement Title** | {title} |")
        p_line(lines, f"| **Requirement Statement**| {r['statement']} |")
        p_line(lines, f"| **Requirement Type** | `{r['type']}` |")
        p_line(lines, f"| **Priority Level** | `{r['priority']}` (Rationale: {r['priority_rationale']}) |")
        p_line(lines, f"| **Business Value** | {r['business_value']} |")
        p_line(lines, f"| **Engineering Rationale**| {r['rationale']} |")
        p_line(lines, f"| **Lawful Basis (DPDP Act)**| **{r['lawful_basis']}** |")
        p_line(lines, f"| **Privacy Impact Analysis**| {r['privacy_impact']} |")
        p_line(lines, f"| **Enforced Privacy Control**| {r['enforced_control']} |")
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
        p_line(lines, f"| **Security & Privacy** | Security: `{r['security_implications']}` \\| Privacy: `{r['privacy_implications']}` |")
        p_line(lines, f"| **Data & Audit** | Data: `{r['data_implications']}` \\| Audit: `{r['audit_requirements']}` |")
        p_line(lines, f"| **Offline & Sync** | Offline: `{r['offline_behavior']}` \\| Sync: `{r['synchronization_implications']}` |")
        p_line(lines, f"| **Quality Expectations**| Perf: `{r['performance_expectations']}` \\| Avail: `{r['availability_expectations']}` |")
        p_line(lines, f"| **Localization & A11y**| Loc: `{r['localization_expectations']}` \\| A11y: `{r['accessibility_expectations']}` |")
        p_line(lines, f"| **Failure & Recovery** | Failure: {r['failure_behavior']} \\| Recovery: {r['recovery_behavior']} |")
        p_line(lines, f"| **Observability** | Logging: `{r['logging_requirements']}` \\| Metrics: `{r['metrics']}` |")
        p_line(lines, f"| **Upstream Traceability**| Obj: [`{r['objective_ref']}`](../01-project-management/02-project-vision-and-objectives.md#{r['objective_ref'].lower()}) \\| Scope: [`{r['scope_ref']}`](../01-project-management/04-in-scope.md#{r['scope_ref'].lower()}) \\| Risk: [`{r['risk_ref']}`](../01-project-management/12-project-risks.md#{r['risk_ref'].lower()}) |")
        p_line(lines, f"| **Downstream Planning** | Epic: `{r['planned_epic']}` \\| Feature: `{r['planned_feature']}` \\| API: `{r['planned_api']}` \\| DB: `{r['planned_db']}` \\| Test: `{r['planned_test']}` |")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".1 Operational Execution Protocol & Privacy Invariants")
        p_line(lines, "- **Frontline Privacy Compliance Workflow:**")
        for step_idx, step in enumerate(r['main_flow'], 1):
            p_line(lines, f"  {step_idx}. {step}")
        p_line(lines, f"- **Offline Consent Capture & Deferred Sync Path:** {r['alternate_flow']}")
        p_line(lines, f"- **Consent Revocation & Emergency Access Path:** {r['exception_flow']}")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".2 Technical Invariants & DPDP Legal Contract")
        p_line(lines, f"- **Lawful Processing Basis:** {r['lawful_basis']}")
        p_line(lines, f"- **Privacy Impact Assessment:** {r['privacy_impact']}")
        p_line(lines, f"- **Technical Control Enforced:** {r['enforced_control']}")
        p_line(lines, f"- **Verification Protocol:** {r['verification_method']}")
        p_line(lines, f"- **Accountable Data Protection Officer:** {r['dpo_owner']}")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".3 Executable BDD Acceptance Scenarios")
        gherkin_block = format_gherkin(r)
        for gh_l in gherkin_block:
            p_line(lines, gh_l)
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".4 Verification Protocol & Quality Sign-Off")
        p_line(lines, f"- **Verification Method:** {r['verification_method']}")
        p_line(lines, f"- **Automated Privacy Compliance Test:** `{r['test_id']}` ({r['test_type']}) targeting zero unlawful data disclosures.")
        p_line(lines, f"- **Related Internal Requirements:** {', '.join([f'[`{x}`](#{x.lower()})' if x.startswith('PRIV-') else f'`{x}`' for x in r['related_requirements']])}")
        p_line(lines, f"- **Dependencies & Blocking Constraints:** {', '.join(r['dependencies'])} | Constraints: {r['constraints']}")
        p_line(lines, f"- **Architectural Assumptions & Open Questions:** Assumption: {r['assumptions']} | Open Question: {r['open_questions']}")
        p_line(lines)
        p_line(lines, "---")
        p_line(lines)

    p_line(lines, "## 5. End-to-End Cross-Baseline Traceability Matrix")
    p_line(lines, "Complete relational mapping linking each Privacy Requirement upstream to Project Management charters and downstream to planned privacy test suites:")
    p_line(lines)
    p_line(lines, "| Privacy Req ID | Upstream Objective | Upstream Scope Ref | Upstream Risk Ref | Accountable DPO | Downstream Planned Epic | Downstream Test ID | Verification Method |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in PRIV_REQUIREMENTS:
        req_id = r["id"]
        obj = r["objective_ref"]
        sc = r["scope_ref"]
        risk = r["risk_ref"]
        owner = r["dpo_owner"]
        epic = r["planned_epic"]
        test_id = r["test_id"]
        vmethod = r["verification_method"]
        p_line(lines, f"| [`{req_id}`](#{req_id.lower()}) | [`{obj}`](../01-project-management/02-project-vision-and-objectives.md#{obj.lower()}) | [`{sc}`](../01-project-management/04-in-scope.md#{sc.lower()}) | [`{risk}`](../01-project-management/12-project-risks.md#{risk.lower()}) | {owner} | `{epic}` | `{test_id}` | {vmethod[:30]}... |")
    p_line(lines)

    p_line(lines, "## 6. Privacy Governance, Data Protection Officer (DPO) Oversight & Regulatory Sign-Off")
    p_line(lines, "This Privacy Requirements Specification defines the binding privacy standard for the Namma Clinic Platform. All data pipelines, client-side caching stores, and analytical views are audited continuously for compliance with DPDP Act 2023 regulations. Any data schema changes introducing new PII elements require sign-off by the Data Protection Officer.")
    p_line(lines)

    content = "\\n".join(lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated Document 08: {len(lines)} total lines.")

if __name__ == "__main__":
    generate_privacy_requirements()
'''
    with open(os.path.join(DIR_PATH, "gen_req_08_priv.py"), "w", encoding="utf-8") as f:
        f.write(priv_code)

    # -------------------------------------------------------------
    # 3. gen_req_09_perf.py
    # -------------------------------------------------------------
    perf_code = '''#!/usr/bin/env python3
"""
gen_req_09_perf.py
Generates docs/02-requirements/09-performance-requirements.md.
Targets 2,800 - 3,500+ substantive markdown lines.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_perf import PERF_REQUIREMENTS
from common import p_line, render_metadata_table, format_gherkin

def generate_performance_requirements():
    target_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "docs", "02-requirements", "09-performance-requirements.md"
    )
    target_path = os.path.abspath(target_path)
    print(f"Generating Document 09 at {target_path}...")

    lines = []

    p_line(lines, "# Performance Requirements Specification: Namma Clinic Digital Health Platform")
    p_line(lines)
    render_metadata_table(
        lines,
        doc_id="DOC-REQ-009-PERF",
        doc_title="Master Performance Requirements & Latency Engineering Baseline",
        req_type="Performance Requirements (PERF)",
        req_range="PERF-001 through PERF-040",
        count=40,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="10-availability-requirements.md"
    )

    p_line(lines, "## 1. Executive Summary & Performance Engineering Framework")
    p_line(lines, "This specification defines the authoritative, measurable performance requirements baseline for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. Comprising 40 rigorous performance engineering specifications (`PERF-001` through `PERF-040`), this document establishes non-negotiable latency budgets, memory limits, client-side indexing throughputs, thermal printing speeds, and background sync performance.")
    p_line(lines)
    p_line(lines, "Because Namma Clinics operate on low-cost, refurbished dual-core workstations with 4GB RAM connected via variable 2G/3G/4G cellular dongles, performance is treated as an indispensable functional prerequisite. Every requirement establishes clear p95 and p99 latency thresholds, explicit measurement tools (k6, Lighthouse, Chrome DevTools, PostgreSQL pg_stat_statements), load profiles, and executable BDD Gherkin scenarios.")
    p_line(lines)

    p_line(lines, "## 2. Performance Architecture & Latency Budget Framework")
    p_line(lines, "Latency budgets are strictly divided between Client Local PWA Operations, Edge/Network Transport, Cloud API Gateway Processing, and Database Index Traversal.")
    p_line(lines)
    p_line(lines, "```mermaid")
    p_line(lines, "graph LR")
    p_line(lines, "    subgraph Client[\"Client Workstation (Refurbished 4GB PC)\"]")
    p_line(lines, "        IDB[\"IndexedDB Commit: <10ms\"]")
    p_line(lines, "        RAM[\"Max PWA Heap: <150MB\"]")
    p_line(lines, "        SEARCH[\"Local Patient Trie Search: <150ms\"]")
    p_line(lines, "        PRINT[\"ESC/POS Thermal Print: <500ms\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph Network[\"Variable Network (2G/3G/4G)\"]")
    p_line(lines, "        SYNC[\"Mutation Sync: 50 mutations/sec\"]")
    p_line(lines, "        PAYLOAD[\"Compressed API Payload: <50KB\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph Cloud[\"Central Cloud Server\"]")
    p_line(lines, "        API[\"API Gateway p95: <120ms\"]")
    p_line(lines, "        DB[\"PostgreSQL Index Scan: <20ms\"]")
    p_line(lines, "        DUCK[\"DuckDB Mart Aggregation: <1.5s\"]")
    p_line(lines, "    end")
    p_line(lines, "    IDB --> SYNC --> API --> DB")
    p_line(lines, "```")
    p_line(lines)

    p_line(lines, "## 3. Master Performance Requirements Inventory Table (PERF-001 to PERF-040)")
    p_line(lines, "| Performance Req ID | Performance Metric Title | Subsystem Domain | Priority | Measurable Quality Target Threshold | Measurement Tool | Lead Owner |")
    p_line(lines, "| :--- | :--- | :--- | :---: | :--- | :--- | :--- |")
    for r in PERF_REQUIREMENTS:
        p_line(lines, f"| [`{r['id']}`](#{r['id'].lower()}) | **{r['title']}** | `{r['domain']}` | `{r['priority']}` | `{r['target_threshold'][:40]}...` | {r['measurement_tool'][:30]}... | {r['owner']} |")
    p_line(lines)

    p_line(lines, "## 4. Comprehensive Performance Requirement Specifications (PERF-001 to PERF-040)")
    p_line(lines, "This section establishes the exhaustive engineering, architectural, and operational specifications for each of the 40 performance requirements governing the Namma Clinic platform.")
    p_line(lines)

    for i, r in enumerate(PERF_REQUIREMENTS, 1):
        req_id = r["id"]
        title = r["title"]
        p_line(lines, f"### 4.{i} {req_id}: {title}")
        p_line(lines)

        p_line(lines, "| Specification Attribute | Formal Engineering Definition |")
        p_line(lines, "| :--- | :--- |")
        p_line(lines, f"| **Requirement ID** | `{req_id}` |")
        p_line(lines, f"| **Requirement Title** | {title} |")
        p_line(lines, f"| **Requirement Statement**| {r['statement']} |")
        p_line(lines, f"| **Requirement Type** | `{r['type']}` |")
        p_line(lines, f"| **Priority Level** | `{r['priority']}` (Rationale: {r['priority_rationale']}) |")
        p_line(lines, f"| **Business Value** | {r['business_value']} |")
        p_line(lines, f"| **Engineering Rationale**| {r['rationale']} |")
        p_line(lines, f"| **Measurable SLA Target**| **{r['target_threshold']}** |")
        p_line(lines, f"| **Measurement Tooling** | {r['measurement_tool']} |")
        p_line(lines, f"| **Production Workload** | {r['workload_condition']} |")
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
        p_line(lines, f"| **Security & Privacy** | Security: `{r['security_implications']}` \\| Privacy: `{r['privacy_implications']}` |")
        p_line(lines, f"| **Data & Audit** | Data: `{r['data_implications']}` \\| Audit: `{r['audit_requirements']}` |")
        p_line(lines, f"| **Offline & Sync** | Offline: `{r['offline_behavior']}` \\| Sync: `{r['synchronization_implications']}` |")
        p_line(lines, f"| **Quality Expectations**| Perf: `{r['performance_expectations']}` \\| Avail: `{r['availability_expectations']}` |")
        p_line(lines, f"| **Localization & A11y**| Loc: `{r['localization_expectations']}` \\| A11y: `{r['accessibility_expectations']}` |")
        p_line(lines, f"| **Failure & Recovery** | Failure: {r['failure_behavior']} \\| Recovery: {r['recovery_behavior']} |")
        p_line(lines, f"| **Observability** | Logging: `{r['logging_requirements']}` \\| Metrics: `{r['metrics']}` |")
        p_line(lines, f"| **Upstream Traceability**| Obj: [`{r['objective_ref']}`](../01-project-management/02-project-vision-and-objectives.md#{r['objective_ref'].lower()}) \\| Scope: [`{r['scope_ref']}`](../01-project-management/04-in-scope.md#{r['scope_ref'].lower()}) \\| Risk: [`{r['risk_ref']}`](../01-project-management/12-project-risks.md#{r['risk_ref'].lower()}) |")
        p_line(lines, f"| **Downstream Planning** | Epic: `{r['planned_epic']}` \\| Feature: `{r['planned_feature']}` \\| API: `{r['planned_api']}` \\| DB: `{r['planned_db']}` \\| Test: `{r['planned_test']}` |")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".1 Operational Execution Protocol & Latency Invariants")
        p_line(lines, "- **Performance Maintenance Flow:**")
        for step_idx, step in enumerate(r['main_flow'], 1):
            p_line(lines, f"  {step_idx}. {step}")
        p_line(lines, f"- **High-Concurrency Degraded State Flow:** {r['alternate_flow']}")
        p_line(lines, f"- **SLA Breach & Shedding Path:** {r['exception_flow']}")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".2 Technical Invariants & SLA Contract")
        p_line(lines, f"- **Target Threshold:** `{r['target_threshold']}`")
        p_line(lines, f"- **Measurement Tooling:** {r['measurement_tool']}")
        p_line(lines, f"- **Production Workload Baseline:** {r['workload_condition']}")
        p_line(lines, f"- **Verification Protocol:** {r['verification_method']}")
        p_line(lines, f"- **Accountable Performance Owner:** {r['owner']}")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".3 Executable BDD Acceptance Scenarios")
        gherkin_block = format_gherkin(r)
        for gh_l in gherkin_block:
            p_line(lines, gh_l)
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".4 Verification Protocol & Quality Sign-Off")
        p_line(lines, f"- **Verification Method:** {r['verification_method']}")
        p_line(lines, f"- **Automated Performance Test:** `{r['test_id']}` ({r['test_type']}) targeting 100% SLA compliance under stress load.")
        p_line(lines, f"- **Related Internal Requirements:** {', '.join([f'[`{x}`](#{x.lower()})' if x.startswith('PERF-') else f'`{x}`' for x in r['related_requirements']])}")
        p_line(lines, f"- **Dependencies & Blocking Constraints:** {', '.join(r['dependencies'])} | Constraints: {r['constraints']}")
        p_line(lines, f"- **Architectural Assumptions & Open Questions:** Assumption: {r['assumptions']} | Open Question: {r['open_questions']}")
        p_line(lines)
        p_line(lines, "---")
        p_line(lines)

    p_line(lines, "## 5. End-to-End Cross-Baseline Traceability Matrix")
    p_line(lines, "Relational mapping linking each Performance Requirement upstream to Project Management charters and downstream to automated load tests:")
    p_line(lines)
    p_line(lines, "| Performance Req ID | Upstream Objective | Upstream Scope Ref | Upstream Risk Ref | Accountable Lead | Downstream Planned Epic | Downstream Test ID | Verification Method |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in PERF_REQUIREMENTS:
        req_id = r["id"]
        obj = r["objective_ref"]
        sc = r["scope_ref"]
        risk = r["risk_ref"]
        owner = r["owner"]
        epic = r["planned_epic"]
        test_id = r["test_id"]
        vmethod = r["verification_method"]
        p_line(lines, f"| [`{req_id}`](#{req_id.lower()}) | [`{obj}`](../01-project-management/02-project-vision-and-objectives.md#{obj.lower()}) | [`{sc}`](../01-project-management/04-in-scope.md#{sc.lower()}) | [`{risk}`](../01-project-management/12-project-risks.md#{risk.lower()}) | {owner} | `{epic}` | `{test_id}` | {vmethod[:30]}... |")
    p_line(lines)

    p_line(lines, "## 6. Performance Budget Governance, Continuous Load Testing & Sign-Off")
    p_line(lines, "This Performance Requirements Specification constitutes the binding technical contract for system responsiveness. Automated load tests run nightly via k6 to prevent performance regressions from entering production bundles.")
    p_line(lines)

    content = "\\n".join(lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated Document 09: {len(lines)} total lines.")

if __name__ == "__main__":
    generate_performance_requirements()
'''
    with open(os.path.join(DIR_PATH, "gen_req_09_perf.py"), "w", encoding="utf-8") as f:
        f.write(perf_code)

    # -------------------------------------------------------------
    # 4. gen_req_10_avail.py
    # -------------------------------------------------------------
    avail_code = '''#!/usr/bin/env python3
"""
gen_req_10_avail.py
Generates docs/02-requirements/10-availability-requirements.md.
Targets 2,800 - 3,500+ substantive markdown lines.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_avail import AVAIL_REQUIREMENTS
from common import p_line, render_metadata_table, format_gherkin

def generate_availability_requirements():
    target_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "docs", "02-requirements", "10-availability-requirements.md"
    )
    target_path = os.path.abspath(target_path)
    print(f"Generating Document 10 at {target_path}...")

    lines = []

    p_line(lines, "# Availability & Resilience Requirements Specification: Namma Clinic Digital Health Platform")
    p_line(lines)
    render_metadata_table(
        lines,
        doc_id="DOC-REQ-010-AVAIL",
        doc_title="Master Availability, Resilience & High Availability Baseline",
        req_type="Availability Requirements (AVAIL)",
        req_range="AVAIL-001 through AVAIL-040",
        count=40,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="09-performance-requirements.md"
    )

    p_line(lines, "## 1. Executive Summary & High Availability Architecture Framework")
    p_line(lines, "This specification defines the authoritative availability, resilience, and business continuity requirements baseline for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. Comprising 40 comprehensive availability specifications (`AVAIL-001` through `AVAIL-040`), this document establishes the engineering safeguards ensuring 99.5% central cloud uptime, 8 hours autonomous offline operation, automated PostgreSQL failover, RPO <5 minutes, and RTO <30 minutes.")
    p_line(lines)
    p_line(lines, "Healthcare delivery at Namma Clinics cannot halt during municipal fiber cuts or power grid failures. The platform architecture guarantees that doctor consultations, nurse vitals entry, lab orders, and pharmacy dispensations proceed uninterrupted during extended network partitions.")
    p_line(lines)

    p_line(lines, "## 2. High Availability Architecture & Fault Isolation Framework")
    p_line(lines, "Resilience is architected across three independent operational layers: Central Cloud Multi-AZ HA, Local Clinic Edge Autonomy, and Client Browser Offline Resilience.")
    p_line(lines)
    p_line(lines, "```mermaid")
    p_line(lines, "graph TD")
    p_line(lines, "    subgraph CloudHA[\"Central Cloud Infrastructure (99.5% Uptime)\"]")
    p_line(lines, "        ALB[\"Dual-AZ Application Load Balancer\"]")
    p_line(lines, "        APP1[\"App Cluster AZ-1\"]")
    p_line(lines, "        APP2[\"App Cluster AZ-2\"]")
    p_line(lines, "        PG_M[\"PostgreSQL Primary\"]")
    p_line(lines, "        PG_S[\"PostgreSQL Hot Standby (Streaming Replication)\"]")
    p_line(lines, "        ALB --> APP1 & APP2")
    p_line(lines, "        APP1 & APP2 --> PG_M")
    p_line(lines, "        PG_M -.-> PG_S")
    p_line(lines, "    end")
    p_line(lines, "    subgraph EdgeAutonomy[\"Clinic Workstation Autonomy (8 Hours Offline)\"]")
    p_line(lines, "        SW[\"Service Worker PWA Offline Cache\"]")
    p_line(lines, "        DEX[\"IndexedDB Dexie.js Local Clinic Store\"]")
    p_line(lines, "        QUEUE[\"Mutation Queue \\| Exponential Backoff Reconnect\"]")
    p_line(lines, "        SW --> DEX --> QUEUE")
    p_line(lines, "    end")
    p_line(lines, "    QUEUE ==\"Auto Reconnect & Sync\"==> ALB")
    p_line(lines, "```")
    p_line(lines)

    p_line(lines, "## 3. Master Availability Requirements Inventory Table (AVAIL-001 to AVAIL-040)")
    p_line(lines, "| Availability Req ID | Resilience Target Title | Resilience Domain | Priority | Measurable Availability SLA | Recovery Mechanism | Accountable Owner |")
    p_line(lines, "| :--- | :--- | :--- | :---: | :--- | :--- | :--- |")
    for r in AVAIL_REQUIREMENTS:
        p_line(lines, f"| [`{r['id']}`](#{r['id'].lower()}) | **{r['title']}** | `{r['domain']}` | `{r['priority']}` | `{r['availability_sla'][:35]}...` | `{r['recovery_mechanism'][:40]}...` | {r['owner']} |")
    p_line(lines)

    p_line(lines, "## 4. Comprehensive Availability Requirement Specifications (AVAIL-001 to AVAIL-040)")
    p_line(lines, "This section establishes the exhaustive engineering, architectural, and operational specifications for each of the 40 availability requirements governing the Namma Clinic platform.")
    p_line(lines)

    for i, r in enumerate(AVAIL_REQUIREMENTS, 1):
        req_id = r["id"]
        title = r["title"]
        p_line(lines, f"### 4.{i} {req_id}: {title}")
        p_line(lines)

        p_line(lines, "| Specification Attribute | Formal Engineering Definition |")
        p_line(lines, "| :--- | :--- |")
        p_line(lines, f"| **Requirement ID** | `{req_id}` |")
        p_line(lines, f"| **Requirement Title** | {title} |")
        p_line(lines, f"| **Requirement Statement**| {r['statement']} |")
        p_line(lines, f"| **Requirement Type** | `{r['type']}` |")
        p_line(lines, f"| **Priority Level** | `{r['priority']}` (Rationale: {r['priority_rationale']}) |")
        p_line(lines, f"| **Business Value** | {r['business_value']} |")
        p_line(lines, f"| **Engineering Rationale**| {r['rationale']} |")
        p_line(lines, f"| **Availability SLA Target**| **{r['availability_sla']}** |")
        p_line(lines, f"| **Recovery Mechanism** | {r['recovery_mechanism']} |")
        p_line(lines, f"| **Verification Protocol** | {r['verification_method']} |")
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
        p_line(lines, f"| **Security & Privacy** | Security: `{r['security_implications']}` \\| Privacy: `{r['privacy_implications']}` |")
        p_line(lines, f"| **Data & Audit** | Data: `{r['data_implications']}` \\| Audit: `{r['audit_requirements']}` |")
        p_line(lines, f"| **Offline & Sync** | Offline: `{r['offline_behavior']}` \\| Sync: `{r['synchronization_implications']}` |")
        p_line(lines, f"| **Quality Expectations**| Perf: `{r['performance_expectations']}` \\| Avail: `{r['availability_expectations']}` |")
        p_line(lines, f"| **Localization & A11y**| Loc: `{r['localization_expectations']}` \\| A11y: `{r['accessibility_expectations']}` |")
        p_line(lines, f"| **Failure & Recovery** | Failure: {r['failure_behavior']} \\| Recovery: {r['recovery_behavior']} |")
        p_line(lines, f"| **Observability** | Logging: `{r['logging_requirements']}` \\| Metrics: `{r['metrics']}` |")
        p_line(lines, f"| **Upstream Traceability**| Obj: [`{r['objective_ref']}`](../01-project-management/02-project-vision-and-objectives.md#{r['objective_ref'].lower()}) \\| Scope: [`{r['scope_ref']}`](../01-project-management/04-in-scope.md#{r['scope_ref'].lower()}) \\| Risk: [`{r['risk_ref']}`](../01-project-management/12-project-risks.md#{r['risk_ref'].lower()}) |")
        p_line(lines, f"| **Downstream Planning** | Epic: `{r['planned_epic']}` \\| Feature: `{r['planned_feature']}` \\| API: `{r['planned_api']}` \\| DB: `{r['planned_db']}` \\| Test: `{r['planned_test']}` |")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".1 Operational Execution Protocol & Resilience Invariants")
        p_line(lines, "- **Operational Continuity Protocol:**")
        for step_idx, step in enumerate(r['main_flow'], 1):
            p_line(lines, f"  {step_idx}. {step}")
        p_line(lines, f"- **Degraded State Autonomy Flow:** {r['alternate_flow']}")
        p_line(lines, f"- **Disaster Recovery & Failover Path:** {r['exception_flow']}")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".2 Technical Invariants & Resilience Contract")
        p_line(lines, f"- **Target SLA:** `{r['availability_sla']}`")
        p_line(lines, f"- **Recovery Protocol:** {r['recovery_mechanism']}")
        p_line(lines, f"- **Verification Protocol:** {r['verification_method']}")
        p_line(lines, f"- **Accountable SRE Lead:** {r['owner']}")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".3 Executable BDD Acceptance Scenarios")
        gherkin_block = format_gherkin(r)
        for gh_l in gherkin_block:
            p_line(lines, gh_l)
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".4 Verification Protocol & Quality Sign-Off")
        p_line(lines, f"- **Verification Method:** {r['verification_method']}")
        p_line(lines, f"- **Automated Chaos & Failover Test:** `{r['test_id']}` ({r['test_type']}) targeting 100% resilience SLA compliance.")
        p_line(lines, f"- **Related Internal Requirements:** {', '.join([f'[`{x}`](#{x.lower()})' if x.startswith('AVAIL-') else f'`{x}`' for x in r['related_requirements']])}")
        p_line(lines, f"- **Dependencies & Blocking Constraints:** {', '.join(r['dependencies'])} | Constraints: {r['constraints']}")
        p_line(lines, f"- **Architectural Assumptions & Open Questions:** Assumption: {r['assumptions']} | Open Question: {r['open_questions']}")
        p_line(lines)
        p_line(lines, "---")
        p_line(lines)

    p_line(lines, "## 5. End-to-End Cross-Baseline Traceability Matrix")
    p_line(lines, "Relational mapping linking each Availability Requirement upstream to Project Management charters and downstream to automated failover tests:")
    p_line(lines)
    p_line(lines, "| Availability Req ID | Upstream Objective | Upstream Scope Ref | Upstream Risk Ref | Accountable SRE | Downstream Planned Epic | Downstream Test ID | Verification Method |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in AVAIL_REQUIREMENTS:
        req_id = r["id"]
        obj = r["objective_ref"]
        sc = r["scope_ref"]
        risk = r["risk_ref"]
        owner = r["owner"]
        epic = r["planned_epic"]
        test_id = r["test_id"]
        vmethod = r["verification_method"]
        p_line(lines, f"| [`{req_id}`](#{req_id.lower()}) | [`{obj}`](../01-project-management/02-project-vision-and-objectives.md#{obj.lower()}) | [`{sc}`](../01-project-management/04-in-scope.md#{sc.lower()}) | [`{risk}`](../01-project-management/12-project-risks.md#{risk.lower()}) | {owner} | `{epic}` | `{test_id}` | {vmethod[:30]}... |")
    p_line(lines)

    p_line(lines, "## 6. Availability Governance, Chaos Engineering & Disaster Recovery Sign-Off")
    p_line(lines, "This Availability Requirements Specification defines the binding operational resilience contract. Monthly automated chaos engineering drills and daily backup restoration validations ensure the platform meets its 99.5% uptime and sub-30-minute RTO guarantees.")
    p_line(lines)

    content = "\\n".join(lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated Document 10: {len(lines)} total lines.")

if __name__ == "__main__":
    generate_availability_requirements()
'''
    with open(os.path.join(DIR_PATH, "gen_req_10_avail.py"), "w", encoding="utf-8") as f:
        f.write(avail_code)

    # -------------------------------------------------------------
    # 5. gen_req_11_loc.py
    # -------------------------------------------------------------
    loc_code = '''#!/usr/bin/env python3
"""
gen_req_11_loc.py
Generates docs/02-requirements/11-localization-requirements.md.
Targets 2,800 - 3,500+ substantive markdown lines.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_loc import LOC_REQUIREMENTS
from common import p_line, render_metadata_table, format_gherkin

def generate_localization_requirements():
    target_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "docs", "02-requirements", "11-localization-requirements.md"
    )
    target_path = os.path.abspath(target_path)
    print(f"Generating Document 11 at {target_path}...")

    lines = []

    p_line(lines, "# Localization & Language Equity Requirements Specification: Namma Clinic Digital Health Platform")
    p_line(lines)
    render_metadata_table(
        lines,
        doc_id="DOC-REQ-011-LOC",
        doc_title="Master Localization & Language Equity Baseline",
        req_type="Localization Requirements (LOC)",
        req_range="LOC-001 through LOC-040",
        count=40,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="12-accessibility-requirements.md"
    )

    p_line(lines, "## 1. Executive Summary & Kannada Linguistic Equity Framework")
    p_line(lines, "This specification defines the comprehensive localization and linguistic equity requirements baseline for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. Comprising 40 detailed localization specifications (`LOC-001` through `LOC-040`), this document guarantees 100% bilingual parity between Kannada (ಕನ್ನಡ) and English across all clinical and administrative interfaces.")
    p_line(lines)
    p_line(lines, "Frontline healthcare delivery in Bengaluru relies heavily on auxiliary nurses, pharmacists, and lab technicians who communicate primarily in Kannada. The platform treats Kannada localization not as an optional cosmetic overlay, but as a core functional prerequisite for patient safety, clinical accuracy, and operational dignity. Every requirement defines strict Unicode normalization (Unicode 15.0 NFC), Noto Sans Kannada rendering, bilingual thermal printing, and translation governance.")
    p_line(lines)

    p_line(lines, "## 2. Localization Architecture & i18n Pipeline")
    p_line(lines, "The i18n architecture enforces zero hardcoded strings, offline translation bundle caching, instant client-side locale toggling, and specialized ESC/POS thermal printer raster bitmap font rendering for Indian scripts.")
    p_line(lines)
    p_line(lines, "```mermaid")
    p_line(lines, "graph TD")
    p_line(lines, "    subgraph LocaleEngine[\"Client-Side i18n Engine\"]")
    p_line(lines, "        TOGGLE[\"Runtime Locale Switcher: Kannada (kn) \\| English (en)\"]")
    p_line(lines, "        CATALOG[\"JSON Translation Catalog (Offline Service Worker Cached)\"]")
    p_line(lines, "        FONT[\"Noto Sans Kannada Typography (Unicode 15.0 NFC)\"]")
    p_line(lines, "        TOGGLE --> CATALOG --> FONT")
    p_line(lines, "    end")
    p_line(lines, "    subgraph Formatting[\"Indian Regional Formatting Engine\"]")
    p_line(lines, "        DATE[\"Date/Time: DD/MM/YYYY hh:mm A\"]")
    p_line(lines, "        CURR[\"Currency: INR (₹) Lakhs/Crores Formatting\"]")
    p_line(lines, "        NUM[\"Numbers: International Numerals & Kannada Numerals\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph Output[\"Multi-Channel Output Tier\"]")
    p_line(lines, "        SCREEN[\"High-DPI Responsive Web UI\"]")
    p_line(lines, "        PRINT[\"ESC/POS Thermal Printer Raster Font Engine\"]")
    p_line(lines, "        SMS[\"Bilingual Unicode SMS Gateway\"]")
    p_line(lines, "    end")
    p_line(lines, "    CATALOG --> Formatting --> Output")
    p_line(lines, "```")
    p_line(lines)

    p_line(lines, "## 3. Master Localization Requirements Inventory Table (LOC-001 to LOC-040)")
    p_line(lines, "| Loc Req ID | Localization Focus Title | UI Context Domain | Standard Applied | Kannada Translation Sample | English Parallel Sample | Verification Method |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in LOC_REQUIREMENTS:
        p_line(lines, f"| [`{r['id']}`](#{r['id'].lower()}) | **{r['title']}** | `{r['ui_context']}` | `{r['standard_applied']}` | `{r['kannada_sample']}` | `{r['english_sample']}` | {r['verification_method'][:30]}... |")
    p_line(lines)

    p_line(lines, "## 4. Comprehensive Localization Requirement Specifications (LOC-001 to LOC-040)")
    p_line(lines, "This section establishes the exhaustive engineering, linguistic, and operational specifications for each of the 40 localization requirements governing the Namma Clinic platform.")
    p_line(lines)

    for i, r in enumerate(LOC_REQUIREMENTS, 1):
        req_id = r["id"]
        title = r["title"]
        p_line(lines, f"### 4.{i} {req_id}: {title}")
        p_line(lines)

        p_line(lines, "| Specification Attribute | Formal Engineering Definition |")
        p_line(lines, "| :--- | :--- |")
        p_line(lines, f"| **Requirement ID** | `{req_id}` |")
        p_line(lines, f"| **Requirement Title** | {title} |")
        p_line(lines, f"| **Requirement Statement**| {r['statement']} |")
        p_line(lines, f"| **Requirement Type** | `{r['type']}` |")
        p_line(lines, f"| **Priority Level** | `{r['priority']}` (Rationale: {r['priority_rationale']}) |")
        p_line(lines, f"| **Business Value** | {r['business_value']} |")
        p_line(lines, f"| **Engineering Rationale**| {r['rationale']} |")
        p_line(lines, f"| **UI Context / Domain** | {r['ui_context']} |")
        p_line(lines, f"| **Standard Applied** | {r['standard_applied']} |")
        p_line(lines, f"| **Kannada Canonical Text**| **{r['kannada_sample']}** |")
        p_line(lines, f"| **English Parallel Text** | {r['english_sample']} |")
        p_line(lines, f"| **Translation Owner** | {r['translation_owner']} |")
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
        p_line(lines, f"| **Security & Privacy** | Security: `{r['security_implications']}` \\| Privacy: `{r['privacy_implications']}` |")
        p_line(lines, f"| **Data & Audit** | Data: `{r['data_implications']}` \\| Audit: `{r['audit_requirements']}` |")
        p_line(lines, f"| **Offline & Sync** | Offline: `{r['offline_behavior']}` \\| Sync: `{r['synchronization_implications']}` |")
        p_line(lines, f"| **Quality Expectations**| Perf: `{r['performance_expectations']}` \\| Avail: `{r['availability_expectations']}` |")
        p_line(lines, f"| **Localization & A11y**| Loc: `{r['localization_expectations']}` \\| A11y: `{r['accessibility_expectations']}` |")
        p_line(lines, f"| **Failure & Recovery** | Failure: {r['failure_behavior']} \\| Recovery: {r['recovery_behavior']} |")
        p_line(lines, f"| **Observability** | Logging: `{r['logging_requirements']}` \\| Metrics: `{r['metrics']}` |")
        p_line(lines, f"| **Upstream Traceability**| Obj: [`{r['objective_ref']}`](../01-project-management/02-project-vision-and-objectives.md#{r['objective_ref'].lower()}) \\| Scope: [`{r['scope_ref']}`](../01-project-management/04-in-scope.md#{r['scope_ref'].lower()}) \\| Risk: [`{r['risk_ref']}`](../01-project-management/12-project-risks.md#{r['risk_ref'].lower()}) |")
        p_line(lines, f"| **Downstream Planning** | Epic: `{r['planned_epic']}` \\| Feature: `{r['planned_feature']}` \\| API: `{r['planned_api']}` \\| DB: `{r['planned_db']}` \\| Test: `{r['planned_test']}` |")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".1 Operational Execution Protocol & Linguistic Invariants")
        p_line(lines, "- **Localization Rendering Protocol:**")
        for step_idx, step in enumerate(r['main_flow'], 1):
            p_line(lines, f"  {step_idx}. {step}")
        p_line(lines, f"- **Linguistic Fallback Path:** {r['alternate_flow']}")
        p_line(lines, f"- **Missing Key & Font Rendering Exception Path:** {r['exception_flow']}")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".2 Technical Invariants & Localization Contract")
        p_line(lines, f"- **Target Standard:** `{r['standard_applied']}`")
        p_line(lines, f"- **Kannada Sample:** {r['kannada_sample']}")
        p_line(lines, f"- **English Sample:** {r['english_sample']}")
        p_line(lines, f"- **Translation Owner:** {r['translation_owner']}")
        p_line(lines, f"- **Verification Protocol:** {r['verification_method']}")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".3 Executable BDD Acceptance Scenarios")
        gherkin_block = format_gherkin(r)
        for gh_l in gherkin_block:
            p_line(lines, gh_l)
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".4 Verification Protocol & Quality Sign-Off")
        p_line(lines, f"- **Verification Method:** {r['verification_method']}")
        p_line(lines, f"- **Automated Translation Coverage Test:** `{r['test_id']}` ({r['test_type']}) targeting zero unlocalized strings.")
        p_line(lines, f"- **Related Internal Requirements:** {', '.join([f'[`{x}`](#{x.lower()})' if x.startswith('LOC-') else f'`{x}`' for x in r['related_requirements']])}")
        p_line(lines, f"- **Dependencies & Blocking Constraints:** {', '.join(r['dependencies'])} | Constraints: {r['constraints']}")
        p_line(lines, f"- **Architectural Assumptions & Open Questions:** Assumption: {r['assumptions']} | Open Question: {r['open_questions']}")
        p_line(lines)
        p_line(lines, "---")
        p_line(lines)

    p_line(lines, "## 5. End-to-End Cross-Baseline Traceability Matrix")
    p_line(lines, "Relational mapping linking each Localization Requirement upstream to Project Management charters and downstream to automated i18n tests:")
    p_line(lines)
    p_line(lines, "| Loc Req ID | Upstream Objective | Upstream Scope Ref | Upstream Risk Ref | Accountable Lead | Downstream Planned Epic | Downstream Test ID | Verification Method |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in LOC_REQUIREMENTS:
        req_id = r["id"]
        obj = r["objective_ref"]
        sc = r["scope_ref"]
        risk = r["risk_ref"]
        owner = r["translation_owner"]
        epic = r["planned_epic"]
        test_id = r["test_id"]
        vmethod = r["verification_method"]
        p_line(lines, f"| [`{req_id}`](#{req_id.lower()}) | [`{obj}`](../01-project-management/02-project-vision-and-objectives.md#{obj.lower()}) | [`{sc}`](../01-project-management/04-in-scope.md#{sc.lower()}) | [`{risk}`](../01-project-management/12-project-risks.md#{risk.lower()}) | {owner} | `{epic}` | `{test_id}` | {vmethod[:30]}... |")
    p_line(lines)

    p_line(lines, "## 6. Localization Governance, Translation Review Board & Linguistic Quality Sign-Off")
    p_line(lines, "This Localization Requirements Specification guarantees language equity across Greater Bengaluru's municipal clinics. All translation bundles undergo review by certified Kannada linguists before promotion to production.")
    p_line(lines)

    content = "\\n".join(lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated Document 11: {len(lines)} total lines.")

if __name__ == "__main__":
    generate_localization_requirements()
'''
    with open(os.path.join(DIR_PATH, "gen_req_11_loc.py"), "w", encoding="utf-8") as f:
        f.write(loc_code)

    # -------------------------------------------------------------
    # 6. gen_req_12_a11y.py
    # -------------------------------------------------------------
    a11y_code = '''#!/usr/bin/env python3
"""
gen_req_12_a11y.py
Generates docs/02-requirements/12-accessibility-requirements.md.
Targets 2,800 - 3,500+ substantive markdown lines.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_a11y import A11Y_REQUIREMENTS
from common import p_line, render_metadata_table, format_gherkin

def generate_accessibility_requirements():
    target_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "docs", "02-requirements", "12-accessibility-requirements.md"
    )
    target_path = os.path.abspath(target_path)
    print(f"Generating Document 12 at {target_path}...")

    lines = []

    p_line(lines, "# Accessibility & Universal Usability Requirements Specification: Namma Clinic Digital Health Platform")
    p_line(lines)
    render_metadata_table(
        lines,
        doc_id="DOC-REQ-012-A11Y",
        doc_title="Master Accessibility & Universal Usability Baseline",
        req_type="Accessibility Requirements (A11Y)",
        req_range="A11Y-001 through A11Y-040",
        count=40,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="11-localization-requirements.md"
    )

    p_line(lines, "## 1. Executive Summary & WCAG 2.1 Level AA Accessibility Framework")
    p_line(lines, "This specification defines the comprehensive accessibility and universal usability requirements baseline for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. Comprising 40 detailed accessibility specifications (`A11Y-001` through `A11Y-040`), this document operationalizes the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA standards and complies with the Rights of Persons with Disabilities (RPwD) Act 2016.")
    p_line(lines)
    p_line(lines, "Healthcare workers operating in fast-paced municipal clinics encounter diverse physical environments, low-cost reflective monitors, keyboard-only workstations, and varying degrees of physical and sensory capabilities. Elderly citizens and persons with disabilities also visit clinics daily. The platform enforces high contrast ratios (4.5:1 text, 7:1 enhanced), complete keyboard navigability with visible focus indicators, screen reader ARIA semantic compatibility, touch targets >=48x48px, and low-literacy iconographic aids.")
    p_line(lines)

    p_line(lines, "## 2. Accessibility Architecture & Inclusive Design System")
    p_line(lines, "The accessible design system embeds inclusive design tokens, keyboard focus traps, screen reader live regions, and automated axe-core audit gates directly into the frontend build pipeline.")
    p_line(lines)
    p_line(lines, "```mermaid")
    p_line(lines, "graph TD")
    p_line(lines, "    subgraph InputMethods[\"Multi-Modal Input Navigation\"]")
    p_line(lines, "        KEYBOARD[\"100% Keyboard Operable \\| Logical Tab Order \\| Focus Ring\"]")
    p_line(lines, "        TOUCH[\"Touch Hit Targets: Minimum 48x48px with 8px Spacing\"]")
    p_line(lines, "        VOICE[\"Screen Reader Semantics \\| ARIA Live Regions \\| NVDA/JAWS\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph VisualPerception[\"Visual Inclusivity & Contrast Engine\"]")
    p_line(lines, "        CONTRAST[\"Color Contrast: >=4.5:1 Normal Text \\| >=3:1 UI Components\"]")
    p_line(lines, "        ZOOM[\"Display Zoom: 200% Lossless Scaling Without Horizontal Scroll\"]")
    p_line(lines, "        THEME[\"High-Contrast Theme \\| Dark/Light Mode Preference\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph CognitiveAids[\"Cognitive & Low-Literacy Usability\"]")
    p_line(lines, "        ICONS[\"Bilingual Text Paired with Universal ISO Healthcare Icons\"]")
    p_line(lines, "        ERRORS[\"Inline Redundant Error Validation (Color + Icon + Text)\"]")
    p_line(lines, "        AUDIO[\"Optional Audio Chimes for Critical Emergency Alerts\"]")
    p_line(lines, "    end")
    p_line(lines, "    InputMethods --> VisualPerception --> CognitiveAids")
    p_line(lines, "```")
    p_line(lines)

    p_line(lines, "## 3. Master Accessibility Requirements Inventory Table (A11Y-001 to A11Y-040)")
    p_line(lines, "| A11y Req ID | Accessibility Feature Title | WCAG Success Criteria | Target User Group | Design Implementation Pattern | Verification Tool | Lead Owner |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in A11Y_REQUIREMENTS:
        p_line(lines, f"| [`{r['id']}`](#{r['id'].lower()}) | **{r['title']}** | `{r['wcag_success_criteria']}` | `{r['target_user_group']}` | `{r['design_implementation'][:35]}...` | {r['verification_method'][:25]}... | {r['owner']} |")
    p_line(lines)

    p_line(lines, "## 4. Comprehensive Accessibility Requirement Specifications (A11Y-001 to A11Y-040)")
    p_line(lines, "This section establishes the exhaustive engineering, design, and operational specifications for each of the 40 accessibility requirements governing the Namma Clinic platform.")
    p_line(lines)

    for i, r in enumerate(A11Y_REQUIREMENTS, 1):
        req_id = r["id"]
        title = r["title"]
        p_line(lines, f"### 4.{i} {req_id}: {title}")
        p_line(lines)

        p_line(lines, "| Specification Attribute | Formal Engineering Definition |")
        p_line(lines, "| :--- | :--- |")
        p_line(lines, f"| **Requirement ID** | `{req_id}` |")
        p_line(lines, f"| **Requirement Title** | {title} |")
        p_line(lines, f"| **Requirement Statement**| {r['statement']} |")
        p_line(lines, f"| **Requirement Type** | `{r['type']}` |")
        p_line(lines, f"| **Priority Level** | `{r['priority']}` (Rationale: {r['priority_rationale']}) |")
        p_line(lines, f"| **Business Value** | {r['business_value']} |")
        p_line(lines, f"| **Engineering Rationale**| {r['rationale']} |")
        p_line(lines, f"| **WCAG Success Criteria**| **{r['wcag_success_criteria']}: {r['accessibility_criterion']}** |")
        p_line(lines, f"| **Target User Group** | {r['target_user_group']} |")
        p_line(lines, f"| **Design Pattern** | {r['design_implementation']} |")
        p_line(lines, f"| **Verification Tooling** | {r['verification_method']} |")
        p_line(lines, f"| **Accessibility Owner** | {r['owner']} |")
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
        p_line(lines, f"| **Security & Privacy** | Security: `{r['security_implications']}` \\| Privacy: `{r['privacy_implications']}` |")
        p_line(lines, f"| **Data & Audit** | Data: `{r['data_implications']}` \\| Audit: `{r['audit_requirements']}` |")
        p_line(lines, f"| **Offline & Sync** | Offline: `{r['offline_behavior']}` \\| Sync: `{r['synchronization_implications']}` |")
        p_line(lines, f"| **Quality Expectations**| Perf: `{r['performance_expectations']}` \\| Avail: `{r['availability_expectations']}` |")
        p_line(lines, f"| **Localization & A11y**| Loc: `{r['localization_expectations']}` \\| A11y: `{r['accessibility_expectations']}` |")
        p_line(lines, f"| **Failure & Recovery** | Failure: {r['failure_behavior']} \\| Recovery: {r['recovery_behavior']} |")
        p_line(lines, f"| **Observability** | Logging: `{r['logging_requirements']}` \\| Metrics: `{r['metrics']}` |")
        p_line(lines, f"| **Upstream Traceability**| Obj: [`{r['objective_ref']}`](../01-project-management/02-project-vision-and-objectives.md#{r['objective_ref'].lower()}) \\| Scope: [`{r['scope_ref']}`](../01-project-management/04-in-scope.md#{r['scope_ref'].lower()}) \\| Risk: [`{r['risk_ref']}`](../01-project-management/12-project-risks.md#{r['risk_ref'].lower()}) |")
        p_line(lines, f"| **Downstream Planning** | Epic: `{r['planned_epic']}` \\| Feature: `{r['planned_feature']}` \\| API: `{r['planned_api']}` \\| DB: `{r['planned_db']}` \\| Test: `{r['planned_test']}` |")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".1 Operational Execution Protocol & Accessibility Invariants")
        p_line(lines, "- **Accessible Navigation & Interaction Flow:**")
        for step_idx, step in enumerate(r['main_flow'], 1):
            p_line(lines, f"  {step_idx}. {step}")
        p_line(lines, f"- **High-Contrast & Assistive Mode Flow:** {r['alternate_flow']}")
        p_line(lines, f"- **Accessibility Trap Mitigation & Escape Path:** {r['exception_flow']}")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".2 Technical Invariants & WCAG Compliance Contract")
        p_line(lines, f"- **WCAG Success Criteria:** {r['wcag_success_criteria']}: {r['accessibility_criterion']}")
        p_line(lines, f"- **Design Pattern Enforced:** {r['design_implementation']}")
        p_line(lines, f"- **Target User Group Beneficiary:** {r['target_user_group']}")
        p_line(lines, f"- **Verification Protocol:** {r['verification_method']}")
        p_line(lines, f"- **Accountable Usability Owner:** {r['owner']}")
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".3 Executable BDD Acceptance Scenarios")
        gherkin_block = format_gherkin(r)
        for gh_l in gherkin_block:
            p_line(lines, gh_l)
        p_line(lines)

        p_line(lines, "#### 4." + str(i) + ".4 Verification Protocol & Quality Sign-Off")
        p_line(lines, f"- **Verification Method:** {r['verification_method']}")
        p_line(lines, f"- **Automated Accessibility Audit Test:** `{r['test_id']}` ({r['test_type']}) targeting zero WCAG 2.1 AA violations.")
        p_line(lines, f"- **Related Internal Requirements:** {', '.join([f'[`{x}`](#{x.lower()})' if x.startswith('A11Y-') else f'`{x}`' for x in r['related_requirements']])}")
        p_line(lines, f"- **Dependencies & Blocking Constraints:** {', '.join(r['dependencies'])} | Constraints: {r['constraints']}")
        p_line(lines, f"- **Architectural Assumptions & Open Questions:** Assumption: {r['assumptions']} | Open Question: {r['open_questions']}")
        p_line(lines)
        p_line(lines, "---")
        p_line(lines)

    p_line(lines, "## 5. End-to-End Cross-Baseline Traceability Matrix")
    p_line(lines, "Relational mapping linking each Accessibility Requirement upstream to Project Management charters and downstream to automated axe-core tests:")
    p_line(lines)
    p_line(lines, "| A11y Req ID | Upstream Objective | Upstream Scope Ref | Upstream Risk Ref | Usability Lead | Downstream Planned Epic | Downstream Test ID | Verification Method |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in A11Y_REQUIREMENTS:
        req_id = r["id"]
        obj = r["objective_ref"]
        sc = r["scope_ref"]
        risk = r["risk_ref"]
        owner = r["owner"]
        epic = r["planned_epic"]
        test_id = r["test_id"]
        vmethod = r["verification_method"]
        p_line(lines, f"| [`{req_id}`](#{req_id.lower()}) | [`{obj}`](../01-project-management/02-project-vision-and-objectives.md#{obj.lower()}) | [`{sc}`](../01-project-management/04-in-scope.md#{sc.lower()}) | [`{risk}`](../01-project-management/12-project-risks.md#{risk.lower()}) | {owner} | `{epic}` | `{test_id}` | {vmethod[:30]}... |")
    p_line(lines)

    p_line(lines, "## 6. Accessibility Governance, Universal Usability Audits & Compliance Sign-Off")
    p_line(lines, "This Accessibility Requirements Specification establishes the binding universal usability contract. Pull requests must pass automated axe-core accessibility gates with zero violations prior to deployment approval.")
    p_line(lines)

    content = "\\n".join(lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated Document 12: {len(lines)} total lines.")

if __name__ == "__main__":
    generate_accessibility_requirements()
'''
    with open(os.path.join(DIR_PATH, "gen_req_12_a11y.py"), "w", encoding="utf-8") as f:
        f.write(a11y_code)

    print("Created gen_req_07_secr.py through gen_req_12_a11y.py successfully.")

if __name__ == "__main__":
    create_generators()
