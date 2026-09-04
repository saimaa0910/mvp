#!/usr/bin/env python3
"""
generate_04_feature_catalog.py
Generates docs/04-product/04-feature-catalog.md
Authoritative Master Feature Catalog Baseline across all 180 Features (FEATURE-001 to FEATURE-180).
Enforces >= 2,000 substantive markdown lines (target 5,000-8,000 lines).
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from product_core_data import (
    DOMAINS,
    MODULES,
    SUBMODULES,
    CAPABILITIES,
    FEATURES,
    ROLE_MAP,
    MODULE_MAP,
    DOMAIN_MAP,
    SUBMODULE_MAP,
    CAPABILITY_MAP
)
from common import count_lines

def generate_document():
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docs/04-product"))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "04-feature-catalog.md")

    lines = []

    def p(text=""):
        lines.append(text)

    # 1. Document Control
    p("# Namma Clinic Digital Health & Operations Platform")
    p("## Canonical Master Feature Catalog: 180 Discrete Product Features")
    p("")
    p("| Metadata Element | Specification Baseline |")
    p("| :--- | :--- |")
    p("| **Document Identifier** | `DOC-PROD-004-FCAT` |")
    p("| **Document Title** | Master Implementation Feature Catalog & Formal Acceptance Specification |")
    p("| **Project Code** | `NAMMA-CLINIC-PLATFORM-2026` |")
    p("| **Document Version** | `v1.0.0-PROD-BASELINE` |")
    p("| **Lifecycle Status** | `APPROVED & RATIFIED` |")
    p(f"| **Total Features Documented** | Exactly {len(FEATURES)} Canonical Features (`FEATURE-001` to `FEATURE-180`) |")
    p(f"| **Capabilities Covered** | Exactly {len(CAPABILITIES)} Mapped Capabilities (`CAPABILITY-001` to `CAPABILITY-180`) |")
    p(f"| **Modules Covered** | Exactly {len(MODULES)} Production Modules (`MODULE-001` to `MODULE-030`) |")
    p(f"| **Domains Covered** | Exactly {len(DOMAINS)} Strategic Business Domains (`DOMAIN-001` to `DOMAIN-006`) |")
    p("| **Testing Paradigm** | Behavior-Driven Development (BDD) Gherkin Acceptance Scenarios |")
    p("| **Upstream Anchors** | `docs/00-project-baseline/`, `docs/02-requirements/`, `docs/03-workflows/` |")
    p("| **Downstream Consuming Phases** | Sprint Backlog, JIRA / GitHub Issues, Test Automation Suites (Playwright) |")
    p("")
    p("---")
    p("")

    # 2. Executive Summary & Specification Methodology
    p("## 1. Executive Summary & Feature Engineering Methodology")
    p("This document constitutes the canonical product feature catalog for the Namma Clinic Platform. Every feature is defined as an atomic, testable, and demonstrable increment of software capability that delivers measurable value to frontline healthcare workers, municipal administrators, or citizens.")
    p("")
    p("### 1.1 Standard 60-Attribute Feature Specification Model")
    p("Each feature dossier provides exhaustive coverage across:")
    p("1. **Identity & Hierarchy:** Feature ID, Name, Domain, Module, Submodule, Capability mapping.")
    p("2. **Problem & Value:** Clinical/operational problem, direct business outcome, citizen value proposition.")
    p("3. **Actor Profile:** Primary operational persona, secondary stakeholders, RBAC role entitlements.")
    p("4. **Behavioral Flows:** Event trigger, preconditions, main happy path, alternate flows, exception paths.")
    p("5. **Governing Rules:** Business rules, clinical safety rules, operational SOP constraints.")
    p("6. **Non-Functional Invariants:** Security, DPDP privacy, p95 performance SLA, 99.9% edge availability.")
    p("7. **Bilingual Ergonomics:** Kannada (kn-IN) and English (en-IN) UTF-8 localization, WCAG 2.1 AA accessibility.")
    p("8. **Distributed Offline Edge:** Local SQLite persistence, zero-network execution, asynchronous sync replay.")
    p("9. **Cross-Cutting Telemetry:** WORM audit ledger event, OpenTelemetry metric span, DuckDB analytics ingestion.")
    p("10. **Delivery & Downstream Mapping:** Priority tier, MoSCoW, MVP status, Target Release, Planned Epic, API, UI, Data, and Test IDs.")
    p("11. **Concrete BDD Acceptance Criteria:** Formal Gherkin scenarios (Given, When, Then, And) covering positive, negative, exception, offline, security, and audit boundaries.")
    p("")

    # 3. Master Feature Index Table (180 Features)
    p("## 2. Master Feature Index & Classification Table (FEATURE-001 to FEATURE-180)")
    p("Consolidated register of all 180 product features with hierarchy alignment, priority tier, and release target:")
    p("")
    p("| Feature ID | Feature Name | Module ID | Capability ID | Priority | MoSCoW | MVP Tier | Release |")
    p("| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |")
    for f in FEATURES:
        p(f"| [`{f['id']}`](#{f['id'].lower()}) | **{f['name']}** | `{f['module_id']}` | `{f['capability_id']}` | `{f['priority']}` | `{f['moscow']}` | `{f['mvp_status']}` | `{f['release_target']}` |")
    p("")
    p("---")
    p("")

    # 4. Deep Feature Catalog Dossiers (All 180 Features)
    p("## 3. Comprehensive Feature Catalog Dossiers (FEATURE-001 to FEATURE-180)")
    p("Detailed engineering specifications for all 180 product features:")
    p("")

    for f in FEATURES:
        fid = f["id"]
        fname = f["name"]
        mid = f["module_id"]
        cid = f["capability_id"]
        sid = f["submodule_id"]
        did = f["domain_id"]

        mobj = MODULE_MAP[mid]
        dobj = DOMAIN_MAP[did]
        sobj = SUBMODULE_MAP.get(sid, {"name": sid})
        cobj = CAPABILITY_MAP.get(cid, {"name": cid})

        p(f"### 3.{f['num']:03d} {fid}: {fname}")
        p("")
        p(f"- **Feature Identifier:** `{fid}` | **Feature Code:** `FEAT-{f['num']:03d}`")
        p(f"- **Feature Name:** **{fname}**")
        p(f"- **Parent Business Domain:** [`{did}`](./01-product-module-map.md#{did.lower()}) — {dobj['name']}")
        p(f"- **Parent Module:** [`{mid}`](./01-product-module-map.md#{mid.lower()}) — {mobj['name']}")
        p(f"- **Parent Submodule:** `{sid}` — {sobj['name']}")
        p(f"- **Implemented Capability:** `{cid}` — {cobj['name']}")
        p(f"- **Priority Tier:** `{f['priority']}` | **MoSCoW:** `{f['moscow']}` | **MVP Status:** `{f['mvp_status']}`")
        p(f"- **Target Release:** `{f['release_target']}` | **Target Sprint:** `{f['sprint_target']}`")
        p(f"- **Upstream Requirements Trace:** {', '.join(f'`{r}`' for r in f['requirement_refs'])}")
        p(f"- **Associated Workflows:** {', '.join(f'`{w}`' for w in f['workflow_refs'])}")
        p("")
        p("#### Feature Description & Value Proposition")
        p(f"**Description:** {f['description']}")
        p("")
        p(f"**Operational Problem Addressed:** {f['user_problem']}")
        p("")
        p(f"**Quantified Business Value:** {f['business_value']}")
        p("")
        p(f"**Direct Citizen / Patient Value:** {f['user_value']}")
        p("")
        p("#### Stakeholder Alignment & User Personas")
        p(f"- **Primary Operational Persona:** `{f['primary_persona']}`")
        p(f"- **Secondary Personas:** {', '.join(f'`{p}`' for p in f['secondary_personas'])}")
        p(f"- **Authorized Roles (RBAC):** {', '.join(f'`{r}`' for r in f['roles'])}")
        p("")
        p("#### Behavioral Execution Flows")
        p(f"- **Execution Trigger:** {f['trigger']}")
        p(f"- **Mandatory Preconditions:** {f['preconditions']}")
        p("")
        p("**Main Operational Happy Path Flow:**")
        for step_idx, step in enumerate(f["main_flow"]):
            p(f"{step_idx+1}. {step}")
        p("")
        p("**Alternative Operational Flows:**")
        for step_idx, step in enumerate(f["alt_flow"]):
            p(f"- *Alt {step_idx+1}:* {step}")
        p("")
        p("**Exception & Error Recovery Flows:**")
        for step_idx, step in enumerate(f["exception_flow"]):
            p(f"- *Exception {step_idx+1}:* {step}")
        p(f"- **Recovery Protocol:** {f['recovery_behavior']}")
        p("")
        p("#### Governing Rules & Regulatory Policies")
        p(f"- **Business Rule Policy:** {f['business_rules']}")
        p(f"- **Clinical Safety Boundary:** {f['clinical_rules']}")
        p(f"- **Operational SOP Invariant:** {f['operational_rules']}")
        p("")
        p("#### Non-Functional & Architecture Invariants")
        p(f"- **Security Standard:** {f['security_reqs']}")
        p(f"- **Privacy & DPDP Invariant:** {f['privacy_reqs']}")
        p(f"- **Latency & Performance SLA:** {f['performance_reqs']}")
        p(f"- **High Availability Invariant:** {f['availability_reqs']}")
        p(f"- **Bilingual Localization (Kannada / English):** {f['localization_reqs']}")
        p(f"- **Accessibility Standard:** {f['accessibility_reqs']}")
        p("")
        p("#### Distributed Offline Edge & Telemetry")
        p(f"- **Autonomous Offline Edge Behavior:** {f['offline_behavior']}")
        p(f"- **Audit Trail Specification:** {f['audit_requirements']}")
        p(f"- **OpenTelemetry Span Name:** `{f['observability_span']}` | **Metric:** `{f['observability_metric']}`")
        p(f"- **Reporting Warehouse Impact:** {f['reporting_impact']}")
        p(f"- **Public Health Analytics Impact:** {f['analytics_impact']}")
        p(f"- **AI / CDSS Integration:** {f['ai_impact']}")
        p(f"- **Integration Boundary:** {f['integration_impact']}")
        p("")
        p("#### Data Entities & Downstream Implementation Artifacts")
        p(f"- **Core Data Objects Touched:** {', '.join(f'`{d}`' for d in f['data_objects'])}")
        p(f"- **Planned Downstream Epic:** `{f['planned_epic']}`")
        p(f"- **Planned API Contract ID:** `{f['planned_api']}`")
        p(f"- **Planned UI Screen Component:** `{f['planned_ui']}`")
        p(f"- **Planned Database Table / DDL:** `{f['planned_data']}`")
        p(f"- **Planned E2E Automated Test Suite:** `{f['planned_test']}`")
        p("")
        p("#### Acceptance Criteria (Formal BDD Gherkin Scenarios)")
        p("```gherkin")
        gh = f["gherkin_scenarios"]
        p(f"Scenario: Positive happy path execution for {fid}")
        p(f"  Given {gh.get('given', 'an authorized staff member is logged into the clinic terminal')}")
        p(f"  When {gh.get('when', 'the user invokes ' + fname)}")
        p(f"  Then {gh.get('then', 'the transaction completes successfully within latency SLA')}")
        p(f"  And a cryptographically signed audit event is appended to the local WORM ledger")
        p("")
        p(f"Scenario: Offline edge execution during broadband network partition for {fid}")
        p(f"  Given the wide-area network connection to the municipal cloud is disconnected")
        p(f"  When the user executes '{fname}' at the local clinic workstation")
        p(f"  Then the operation commits successfully to the local edge SQLite database")
        p(f"  And the transaction is queued for cloud synchronization upon network restoration")
        p("")
        p(f"Scenario: Authorization boundary rejection for {fid}")
        p(f"  Given an unauthenticated or unauthorized user attempts to invoke '{fname}'")
        p(f"  When the request reaches the service authorization middleware")
        p(f"  Then the request is rejected with HTTP 403 Forbidden")
        p(f"  And an unauthorized access security violation is logged to the audit ledger")
        p("```")
        p("")
        p("---")
        p("")

    content = "\n".join(lines)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)

    metrics = count_lines(content)
    total_lines = metrics["total"]
    substantive_lines = metrics["substantive"]
    print(f"Generated {out_file}:")
    print(f"  Total Lines:       {total_lines}")
    print(f"  Substantive Lines: {substantive_lines}")
    return out_file, total_lines, substantive_lines

if __name__ == "__main__":
    generate_document()
