#!/usr/bin/env python3
"""
gen_req_03_nfr.py
Generates docs/02-requirements/03-non-functional-requirements.md.
Targets 2,800 - 3,500+ substantive markdown lines.
100% domain-specific engineering quality attributes for Namma Clinic.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_nfr import NFR_REQUIREMENTS
from common import p_line, render_metadata_table, format_gherkin

def generate_non_functional_requirements():
    target_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "docs", "02-requirements", "03-non-functional-requirements.md"
    )
    target_path = os.path.abspath(target_path)
    print(f"Generating Document 03 at {target_path}...")

    lines = []

    # Document Header & Title
    p_line(lines, "# Non-Functional Requirements Specification: Namma Clinic Digital Health Platform")
    p_line(lines)
    render_metadata_table(
        lines,
        doc_id="DOC-REQ-003-NFR",
        doc_title="Master Non-Functional Requirements Specification & Quality Attributes Baseline",
        req_type="Non-Functional Requirements (NFR)",
        req_range="NFR-001 through NFR-050",
        count=50,
        parent_baseline="02-functional-requirements.md",
        counterpart="07-security-requirements.md"
    )

    # Section 1: Executive Summary & Architectural Quality Framework
    p_line(lines, "## 1. Executive Summary & Architectural Quality Framework")
    p_line(lines, "This specification establishes the authoritative, implementation-ready non-functional requirements (NFRs) for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. Comprising 50 rigorous, measurable specifications (`NFR-001` through `NFR-050`), this document defines the engineering boundaries for performance, availability, security, privacy, resilience, accessibility, localization, maintainability, and disaster recovery.")
    p_line(lines)
    p_line(lines, "Every requirement in this specification is quantified with concrete, measurable thresholds, explicit verification methodologies, authoritative owners, and executable BDD Gherkin scenarios. Unambiguous engineering quality gates ensure that all software packages, database models, and client PWA bundles satisfy the municipal healthcare delivery standards mandated by the BBMP Health Department and National Health Mission (NHM).")
    p_line(lines)

    # Section 2: Taxonomy
    p_line(lines, "## 2. Non-Functional Requirements Categorization Taxonomy")
    p_line(lines, "The 50 non-functional requirements are organized across eight specialized architectural quality domains:")
    p_line(lines, "1. **Performance & Scalability (NFR-001 to NFR-007, NFR-031, NFR-037, NFR-038):** Sub-120ms API p95 latency, 150MB client RAM cap, sub-10ms IndexedDB commits, sub-150ms patient search across 500k records, sub-500ms thermal printing, 50 mutations/sec sync throughput, and DuckDB analytical query performance.")
    p_line(lines, "2. **Availability & Business Continuity (NFR-008 to NFR-012, NFR-032):** 99.5% central cloud uptime, 8 hours autonomous offline continuity, RPO <5 minutes, RTO <30 minutes, graceful UI degradation, and zero data loss on unexpected power cuts.")
    p_line(lines, "3. **Security & Cryptography (NFR-013 to NFR-020, NFR-043 to NFR-045):** TLS 1.3 encryption, AES-256-GCM data at rest, Web Cryptography client storage encryption, RBAC least privilege, Argon2id password hashing, brute-force lockout, immutable WORM logging, CSP headers, XSS sanitization, SameSite cookies, and zero container CVEs.")
    p_line(lines, "4. **Privacy & Data Protection (NFR-021 to NFR-022):** DPDP Act 2023 explicit consent architecture, purpose limitation, and k-anonymity (k>=5) for public health analytical exports.")
    p_line(lines, "5. **Localization & Internationalization (NFR-023 to NFR-025):** 100% bilingual Kannada and English interface completeness, Noto Sans Kannada Unicode normalization, and standardized Indian locale formatting (DD/MM/YYYY, INR ₹).")
    p_line(lines, "6. **Accessibility & Inclusive Design (NFR-026 to NFR-030):** WCAG 2.1 Level AA compliance, 4.5:1 text contrast ratios, 100% keyboard navigability, 48x48px touch targets, and ARIA screen reader live region announcements.")
    p_line(lines, "7. **Observability & Operability (NFR-034 to NFR-036, NFR-039, NFR-040):** Structured JSON logs with trace correlation, OpenTelemetry distributed tracing, Prometheus telemetry metrics, zero-installation PWA footprint, and compatibility with refurbished dual-core PCs.")
    p_line(lines, "8. **Maintainability, Resilience & Quality Assurance (NFR-033, NFR-041, NFR-042, NFR-046 to NFR-050):** 85% test statement coverage, zero-downtime rolling deployments, automated daily backup restore verification, circuit breakers, standardized error envelopes, sync idempotency, and automated CI test gates.")
    p_line(lines)

    # Architecture Mermaid Diagram
    p_line(lines, "```mermaid")
    p_line(lines, "graph TD")
    p_line(lines, "    subgraph QualityPillars[\"Architectural Quality Pillars\"]")
    p_line(lines, "        P1[\"Performance & Scalability:<br/>p95 <120ms \\| 150MB RAM\"]")
    p_line(lines, "        P2[\"Availability & Resilience:<br/>99.5% Uptime \\| 8h Offline\"]")
    p_line(lines, "        P3[\"Security & Privacy:<br/>AES-256 \\| DPDP Consent\"]")
    p_line(lines, "        P4[\"Usability & Inclusivity:<br/>Kannada/English \\| WCAG 2.1 AA\"]")
    p_line(lines, "    end")
    p_line(lines, "    subgraph OperationalAssurance[\"Operational Quality Assurance\"]")
    p_line(lines, "        O1[\"Observability:<br/>OpenTelemetry \\| Prometheus \\| Loki WORM\"]")
    p_line(lines, "        O2[\"Disaster Recovery:<br/>RPO <5m \\| RTO <30m \\| Daily Restores\"]")
    p_line(lines, "        O3[\"Software Fitness:<br/>85% Test Coverage \\| Zero CVEs \\| PWA\"]")
    p_line(lines, "    end")
    p_line(lines, "    P1 --> O1")
    p_line(lines, "    P2 --> O2")
    p_line(lines, "    P3 --> O1")
    p_line(lines, "    P4 --> O3")
    p_line(lines, "```")
    p_line(lines)

    # Section 3: Master Inventory Table
    p_line(lines, "## 3. Master Non-Functional Requirements Inventory Table (NFR-001 to NFR-050)")
    p_line(lines, "| Requirement ID | Quality Attribute Title | Quality Domain | Priority | Measurable Quality Target Threshold | Verification Methodology | Accountable Lead |")
    p_line(lines, "| :--- | :--- | :--- | :---: | :--- | :--- | :--- |")
    for r in NFR_REQUIREMENTS:
        p_line(lines, f"| [`{r['id']}`](#{r['id'].lower()}) | **{r['title']}** | `{r['domain']}` | `{r['priority']}` | `{r['measurable_threshold'][:40]}...` | {r['verification_method'][:35]}... | {r['owner']} |")
    p_line(lines)

    # Section 4: Deep Technical & Operational Specifications
    p_line(lines, "## 4. Comprehensive Non-Functional Requirement Specifications (NFR-001 to NFR-050)")
    p_line(lines, "This section establishes the exhaustive engineering, architectural, and operational specifications for each of the 50 non-functional quality attributes committed for production baseline delivery.")
    p_line(lines)

    for i, r in enumerate(NFR_REQUIREMENTS, 1):
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
        p_line(lines, f"| **Security & Privacy** | Security: `{r['security_implications']}` \\| Privacy: `{r['privacy_implications']}` |")
        p_line(lines, f"| **Data & Audit** | Data: `{r['data_implications']}` \\| Audit: `{r['audit_requirements']}` |")
        p_line(lines, f"| **Offline & Sync** | Offline: `{r['offline_behavior']}` \\| Sync: `{r['synchronization_implications']}` |")
        p_line(lines, f"| **Quality Target** | **Measurable SLA:** `{r['measurable_threshold']}` |")
        p_line(lines, f"| **Quality Expectations**| Perf: `{r['performance_expectations']}` \\| Avail: `{r['availability_expectations']}` |")
        p_line(lines, f"| **Localization & A11y**| Loc: `{r['localization_expectations']}` \\| A11y: `{r['accessibility_expectations']}` |")
        p_line(lines, f"| **Failure & Recovery** | Failure: {r['failure_behavior']} \\| Recovery: {r['recovery_behavior']} |")
        p_line(lines, f"| **Observability** | Logging: `{r['logging_requirements']}` \\| Metrics: `{r['metrics']}` |")
        p_line(lines, f"| **Upstream Traceability**| Obj: [`{r['objective_ref']}`](../01-project-management/02-project-vision-and-objectives.md#{r['objective_ref'].lower()}) \\| Scope: [`{r['scope_ref']}`](../01-project-management/04-in-scope.md#{r['scope_ref'].lower()}) \\| Risk: [`{r['risk_ref']}`](../01-project-management/12-project-risks.md#{r['risk_ref'].lower()}) |")
        p_line(lines, f"| **Downstream Planning** | Epic: `{r['planned_epic']}` \\| Feature: `{r['planned_feature']}` \\| API: `{r['planned_api']}` \\| DB: `{r['planned_db']}` \\| Test: `{r['planned_test']}` |")
        p_line(lines)

        # Operational Execution Paths
        p_line(lines, "#### 4." + str(i) + ".1 Operational Execution Protocol & Quality Invariants")
        p_line(lines, "- **Continuous Quality Maintenance Protocol:**")
        for step_idx, step in enumerate(r['main_flow'], 1):
            p_line(lines, f"  {step_idx}. {step}")
        p_line(lines, f"- **Degraded State Mitigation Flow:** {r['alternate_flow']}")
        p_line(lines, f"- **Exception Breach & Circuit Breaker Flow:** {r['exception_flow']}")
        p_line(lines)

        # Technical Architecture Invariants
        p_line(lines, "#### 4." + str(i) + ".2 Technical Invariants & Verification Contract")
        p_line(lines, f"- **Measurable SLA Threshold:** `{r['measurable_threshold']}`")
        p_line(lines, f"- **Measurement Instrumentation:** {r['measurement_method']}")
        p_line(lines, f"- **Verification Protocol:** {r['verification_method']}")
        p_line(lines, f"- **Accountable Quality Owner:** {r['owner']}")
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
        p_line(lines, f"- **Automated Test Suite:** `{r['test_id']}` ({r['test_type']}) targeting 100% quality gate compliance.")
        p_line(lines, f"- **Related Internal Requirements:** {', '.join([f'[`{x}`](#{x.lower()})' if x.startswith('NFR-') else f'`{x}`' for x in r['related_requirements']])}")
        p_line(lines, f"- **Dependencies & Blocking Constraints:** {', '.join(r['dependencies'])} | Constraints: {r['constraints']}")
        p_line(lines, f"- **Architectural Assumptions & Open Questions:** Assumption: {r['assumptions']} | Open Question: {r['open_questions']}")
        p_line(lines)
        p_line(lines, "---")
        p_line(lines)

    # Section 5: End-to-End Traceability Matrix
    p_line(lines, "## 5. End-to-End Cross-Baseline Traceability Matrix")
    p_line(lines, "Complete relational mapping linking each Non-Functional Requirement upstream to Project Management charters and downstream to planned engineering quality gates:")
    p_line(lines)
    p_line(lines, "| Non-Functional Req ID | Upstream Objective | Upstream Scope Ref | Upstream Risk Ref | Accountable Role | Downstream Planned Epic | Downstream Test ID | Verification Method |")
    p_line(lines, "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in NFR_REQUIREMENTS:
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

    # Section 6: Governance & Quality Sign-Off
    p_line(lines, "## 6. Non-Functional Quality Gate Governance & Sign-Off")
    p_line(lines, "This Non-Functional Requirements Specification constitutes the binding technical contract for system performance, security, and availability. Any pull request or deployment that fails to meet these quantified quality gates will be rejected automatically by CI/CD pipeline controls.")
    p_line(lines)
    p_line(lines, "Revisions to quality targets or thresholds require formal evaluation and approval by the Architecture Review Board under [`docs/01-project-management/18-change-management.md`](../01-project-management/18-change-management.md).")
    p_line(lines)

    content = "\n".join(lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated Document 03: {len(lines)} total lines.")

if __name__ == "__main__":
    generate_non_functional_requirements()
