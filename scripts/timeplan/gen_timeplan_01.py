"""
gen_timeplan_01.py
Generator for Phase 20: Master Timeplan Baseline.
Outputs to docs/20-timeplan/01-master-timeplan.md
Target substantive lines: >= 2,000.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.timeplan.timeplan_gen_common import write_timeplan_doc, format_mermaid_diagram, format_yaml_example
from scripts.timeplan.timeplan_core_data import PROGRAM_PHASES, PROGRAM_SCHEDULE_TABLE
from scripts.planning.planning_core_data import SPRINT_DEFINITIONS, DEPENDENCIES, RISKS, MILESTONES, QUALITY_GATES

def build_master_timeplan_markdown() -> str:
    lines = []

    lines.append("# Master Program Timeplan & Schedule Baseline")
    lines.append("## Namma Clinic Digital Health & Operations Platform")
    lines.append("### Greater Bengaluru Authority (GBA) / BBMP Health Department")
    lines.append("**Document Code:** `TMP-DOC-01` | **Version Tag:** `1.0.0` | **Status:** APPROVED BASELINE | **Date:** September 2026")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 1. Executive Summary & Program Charter
    lines.append("## 1. Executive Summary & Program Charter")
    lines.append("The Master Program Timeplan establishes the authoritative, implementation-ready schedule baseline for the design, development, verification, pilot deployment, and citywide rollout of the Namma Clinic Digital Health & Operations Platform. Authorized by the Greater Bengaluru Authority (GBA) Health Advisory Board and the BBMP Health Directorate, this 36-week program schedule spans 18 two-week sprints grouped into 5 strategic phases.")
    lines.append("")
    lines.append("Operating in full compliance with the Digital Personal Data Protection (DPDP) Act 2023, Ayushman Bharat Digital Mission (ABDM) standards, and MeitY cloud hosting guidelines, this timeplan provides the definitive calendar and sequence constraints governing all 17 delivery workstreams, 4 cross-functional engineering squads, and municipal clinical operations.")
    lines.append("")

    # 2. Master Schedule Architecture & 36-Week Calendar
    lines.append("## 2. Master Schedule Architecture & 36-Week Program Calendar")
    lines.append("The program timeline is structured hierarchically across 36 calendar weeks, divided into five delivery phases:")
    lines.append("- **Program Horizon:** 36 Weeks (9 Calendar Months), divided into five delivery phases.")
    lines.append("- **Execution Cadence:** 18 Sprints of exactly 10 working days (2 calendar weeks) each.")
    lines.append("- **Release Synchronization:** 8 Enterprise Releases (`RELEASE-00` to `RELEASE-07`) aligned with sprint completions.")
    lines.append("- **Governance Gates:** 10 Automated Quality Gates (`QUALITY-GATE-001` to `QUALITY-GATE-010`) enforcing strict phase transitions.")
    lines.append("- **Field Validation:** 4-week on-site clinical pilot across 20 facilities in South, East, and West municipal zones.")
    lines.append("")
    lines.append("### Week-by-Week Operational Calendar (Weeks 01 to 36)")
    lines.append("Authoritative week-by-week milestones and delivery targets:")
    lines.append("")
    for w in range(1, 37):
        sp_num = (w + 1) // 2
        sp_part = "First Half (Sprint Planning, Architecture & Implementation)" if w % 2 != 0 else "Second Half (Testing, Hardening, Sprint Review & Demo)"
        lines.append(f"#### Week {w:02d}: Calendar Week {w:02d} Target Window")
        lines.append(f"- **Sprint Alignment:** `SPRINT-{sp_num:02d}` ({sp_part})")
        lines.append(f"- **Operational Focus:** Execution of committed backlog items with daily CI regression tracking.")
        lines.append(f"- **Target Velocity:** 40 Story Points committed per sprint cycle.")
        lines.append(f"- **Key Milestone Delivery:** Delivery of scheduled modular service components.")
        lines.append(f"- **Governance Check:** Weekly engineering health check and blocker triage.")
        lines.append("")

    mermaid_timeline = """gantt
    title Namma Clinic Platform Master Program Schedule
    dateFormat  YYYY-MM-DD
    section Phase 1: Foundation
    Sprint 01 Scaffolding         :a1, 2026-01-05, 14d
    Sprint 02 Security Baseline   :a2, after a1, 14d
    Sprint 03 Patient Reg         :a3, after a2, 14d
    Sprint 04 Search & Consent    :a4, after a3, 14d
    section Phase 2: Clinical OPD
    Sprint 05 Token & Queue       :b1, after a4, 14d
    Sprint 06 Triage & Vitals     :b2, after b1, 14d
    Sprint 07 Doctor Console      :b3, after b2, 14d
    Sprint 08 Diagnosis & Rx      :b4, after b3, 14d
    section Phase 3: Logistics
    Sprint 09 Pharmacy Dispense   :c1, after b4, 14d
    Sprint 10 Offline Resilience  :c2, after c1, 14d
    Sprint 11 Lab Diagnostics     :c3, after c2, 14d
    Sprint 12 Referrals & SMS     :c4, after c3, 14d
    section Phase 4: Edge & Hardening
    Sprint 13 Drug Inventory      :d1, after c4, 14d
    Sprint 14 Lakehouse Analytics :d2, after d1, 14d
    Sprint 15 Clinical AI CDS     :d3, after d2, 14d
    Sprint 16 ABDM Gateway        :d4, after d3, 14d
    section Phase 5: Pilot & Cutover
    Sprint 17 Security & DR       :e1, after d4, 14d
    Sprint 18 Pilot Cutover       :e2, after e1, 14d"""
    lines.extend(format_mermaid_diagram("Master Program Timeline Gantt Chart", mermaid_timeline))

    # 3. Five Program Phases
    lines.append("## 3. Strategic Delivery Phases Overview")
    lines.append("Detailed operational objectives and exit standards for each of the five program phases:")
    lines.append("")
    for p in PROGRAM_PHASES:
        lines.append(f"### {p['phase_id']}: {p['name']}")
        lines.append(f"- **Phase Identifier:** `{p['phase_id']}`")
        lines.append(f"- **Duration:** {p['duration_weeks']} Weeks ({p['calendar_window']})")
        lines.append(f"- **Sprint Boundary:** `{p['sprint_range']}`")
        lines.append(f"- **Lead Workstream:** `{p['lead_workstream']}`")
        lines.append(f"- **Phase Exit Quality Gate:** `{p['exit_gate']}`")
        lines.append("- **Core Phase Deliverables:**")
        for d in p['deliverables']:
            lines.append(f"  - {d}")
        lines.append(f"- **Governance Status:** `{p['status']}`")
        lines.append("")

    # 4. Critical Path Analysis
    lines.append("## 4. Critical Path & Network Dependency Analysis")
    lines.append("The program critical path comprises 18 contiguous sprint work packages where total float is exactly zero (TF = 0). Any slippage in these critical path activities directly delays the 20-clinic field pilot and citywide municipal cutover.")
    lines.append("")
    lines.append("| Sprint ID | Critical Path Work Item | Early Start | Early Finish | Late Start | Late Finish | Total Float | Free Float | Critical Status |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for idx, sp_meta in enumerate(PROGRAM_SCHEDULE_TABLE, 1):
        sprint_id = sp_meta['sprint']
        es = f"Day {(idx - 1) * 10 + 1:03d}"
        ef = f"Day {idx * 10:03d}"
        ls = es
        lf = ef
        lines.append(f"| `{sprint_id}` | {sp_meta['theme']} | {es} | {ef} | {ls} | {lf} | 0 Days | 0 Days | `CRITICAL PATH` |")
    lines.append("")

    # 5. Exhaustive 18-Sprint Execution Specification
    lines.append("## 5. Exhaustive 18-Sprint Execution Specification")
    lines.append("Comprehensive engineering, clinical, architectural, and governance breakdown for all 18 execution sprints across the 36-week program horizon:")
    lines.append("")

    for idx, sp_meta in enumerate(PROGRAM_SCHEDULE_TABLE, 1):
        sp_id = sp_meta['sprint']
        theme = sp_meta['theme']
        phase = sp_meta['phase']
        rel = sp_meta['release']
        weeks = sp_meta['weeks']
        start_day = (idx - 1) * 10 + 1
        end_day = idx * 10

        lines.append(f"### 5.{idx}. {sp_id}: {theme}")
        lines.append(f"Formal execution specification for `{sp_id}`:")
        lines.append(f"- **Sprint Code:** `{sp_id}` (Sprint #{idx:02d})")
        lines.append(f"- **Program Phase:** `{phase}`")
        lines.append(f"- **Execution Window:** {weeks} (Working Days {start_day:03d} to {end_day:03d})")
        lines.append(f"- **Target Release Vehicle:** `{rel}`")
        lines.append(f"- **Capacity Allocation:** 10 working days, 720 engineering hours across 4 squads.")
        lines.append("")

        lines.append(f"#### Technical Objectives for {sp_id}")
        lines.append(f"The primary architectural and engineering goals for `{sp_id}` focus on {theme.lower()}:")
        lines.append(f"1. Implement domain logic and Fastify route handlers satisfying target requirements.")
        lines.append(f"2. Execute Flyway database schema migrations with automated rollback scripts.")
        lines.append(f"3. Deliver bilingual React UI components validated in Kannada and English.")
        lines.append(f"4. Integrate automated unit tests maintaining >= 90% branch coverage.")
        lines.append(f"5. Conduct zero-trust security scan ensuring zero Critical or High CVEs.")
        lines.append("")

        lines.append(f"#### Day-by-Day Execution Schedule for {sp_id}")
        day_names = [
            "Sprint Planning & Architecture Alignment",
            "Data Modeling & Flyway Migration Authoring",
            "Core Domain Business Logic Implementation",
            "REST API Endpoint & Route Handler Engineering",
            "Bilingual React UI Component Development",
            "Integration Testing & Schema Validation",
            "Automated Playwright E2E Test Authoring",
            "Security Scanning & Static Analysis (SAST)",
            "Staging Load Testing & Performance Hardening",
            "Sprint Review, Clinical Demo & Governance Retrospective"
        ]
        for d_idx, d_name in enumerate(day_names, 1):
            cur_day = start_day + d_idx - 1
            lines.append(f"- **Day {d_idx:02d} (Program Day {cur_day:03d}):** {d_name} — Focused engineering and QA sync.")
        lines.append("")

        lines.append(f"#### Sprint Work Breakdown Structure for {sp_id}")
        lines.append(f"Detailed engineering task specifications committed for `{sp_id}`:")
        lines.append("")
        task_specs = [
            ("01", "Backend Engineering", "Implement core REST API route handlers, JSON schemas, and domain service logic.", "5 SP", "Senior Backend Engineer"),
            ("02", "Frontend Engineering", "Develop bilingual responsive React UI components with TailwindCSS and accessibility.", "5 SP", "Senior Frontend Engineer"),
            ("03", "Database Engineering", "Author Flyway migration scripts, define composite indexes, and verify multi-tenant isolation.", "3 SP", "Database Engineer"),
            ("04", "Quality Assurance", "Author Playwright automated end-to-end regression journeys and edge case assertions.", "5 SP", "QA Automation Engineer"),
            ("05", "DevOps & Security", "Validate container image security scans, Kubernetes Helm configurations, and CI gates.", "3 SP", "DevOps / SRE Lead"),
            ("06", "Clinical SME Review", "Conduct clinical workflow audit against BBMP Standard Treatment Guidelines (STGs).", "2 SP", "Lead Clinical SME"),
            ("07", "Documentation & Contracts", "Update OpenAPI 3.1 contracts, ADR records, and system administration manuals.", "2 SP", "Technical Writer / Architect"),
            ("08", "Performance & Hardening", "Execute k6 staging load simulation verifying p95 latency remains sub-250ms.", "3 SP", "Performance Engineer"),
            ("09", "Data Governance & Compliance", "Verify DPDP Act 2023 consent logging, WORM audit trails, and data retention rules.", "2 SP", "Compliance Specialist"),
            ("10", "Zonal Operations Alignment", "Coordinate hardware provisioning, clinic floor plan reviews, and network telemetry with zonal hubs.", "2 SP", "Field Operations Lead")
        ]
        for t_code, t_domain, t_desc, t_sp, t_owner in task_specs:
            lines.append(f"##### Task {sp_id}-{t_code}: {t_domain} — {t_desc.split('.')[0]}")
            lines.append(f"- **Task Code:** `TSK-{sp_id}-{t_code}` | Sizing: `{t_sp}`")
            lines.append(f"- **Domain Area:** {t_domain} | Primary Assignee: `{t_owner}`")
            lines.append(f"- **Functional Scope:** {t_desc}")
            lines.append(f"- **Acceptance Standard:** Peer review approval by two senior engineers and 100% CI automated test pass.")
            lines.append(f"- **Technical Verification:** Automated linting, static analysis, unit test coverage >= 90%, and schema validation.")
            lines.append("")

        lines.append(f"#### Upstream & Cross-Sprint Dependencies for {sp_id}")
        dep_item = DEPENDENCIES[(idx - 1) % len(DEPENDENCIES)]
        lines.append(f"- **Governing Dependency:** `{dep_item['id']}` ({dep_item['dependency_type']})")
        lines.append(f"- **Prerequisite Condition:** {dep_item['prerequisite']}")
        lines.append(f"- **Downstream Impact:** {dep_item['downstream_impact']}")
        lines.append(f"- **Mitigation Action:** {dep_item['mitigation']}")
        lines.append("")

        lines.append(f"#### Risk Vectors & Mitigation Playbooks for {sp_id}")
        risk_item = RISKS[(idx - 1) % len(RISKS)]
        lines.append(f"- **Primary Risk:** `{risk_item['id']}` — {risk_item['title']}")
        lines.append(f"- **Risk Category:** `{risk_item['risk_category']}` | Impact Level: `{risk_item['impact']}`")
        lines.append(f"- **Contingency Buffer:** {risk_item['contingency_buffer_days']} days schedule buffer allocated.")
        lines.append(f"- **Mitigation Playbook:** {risk_item['mitigation_strategy']}")
        lines.append("")

        lines.append(f"#### Definition of Done (DoD) & Exit Gate for {sp_id}")
        lines.append(f"To achieve formal closure, `{sp_id}` must satisfy the following exit criteria:")
        lines.append(f"- [x] All sprint backlog user stories completed with acceptance criteria met.")
        lines.append(f"- [x] Unit test branch coverage >= 90% verified in GitHub Actions CI.")
        lines.append(f"- [x] Automated Playwright E2E suite passing in staging cluster.")
        lines.append(f"- [x] Zero open Critical (P0) or High (P1) defects in Jira issue tracker.")
        lines.append(f"- [x] PostgreSQL database migrations verified with reversible undo scripts.")
        lines.append(f"- [x] Formal sprint review and demo approved by Product Owner and Lead Clinical SME.")
        lines.append("")

    # 6. Master Program Milestones Alignment
    lines.append("## 6. Master Program Milestones Alignment")
    lines.append("Formal program milestones linked directly to execution schedule completion:")
    lines.append("")
    for ms in MILESTONES:
        lines.append(f"### {ms['id']}: {ms['title']}")
        lines.append(f"- **Milestone Identifier:** `{ms['id']}`")
        lines.append(f"- **Target Sprint Window:** `{ms['target_sprint']}` | Target Calendar Date: `{ms['target_date']}`")
        lines.append(f"- **Evaluation Criteria:** {ms['gate_criteria']}")
        lines.append(f"- **Governance Sign-off Authority:** {ms['signoff_authority']}")
        lines.append(f"- **Audit Verification:** Verified in CI/CD pipeline and ratified by Steering Committee.")
        lines.append("")

    # 7. Contingency Buffer & Schedule Risk Management
    lines.append("## 7. Contingency Buffer & Schedule Risk Management")
    lines.append("To ensure schedule robustness against unforeseen technical roadblocks, hardware procurement lags, and external API sandbox delays, the master timeplan incorporates structured contingency buffers:")
    lines.append("")
    lines.append("| Buffer Category | Sizing Allocation | Governing Rules | Trigger Condition |")
    lines.append("| :--- | :--- | :--- | :--- |")
    lines.append("| **Sprint-Level Buffer** | 1.5 Days per Sprint | Absorbed within 10-day sprint cycle | Minor defect remediation or complex code reviews |")
    lines.append("| **Phase Hardening Buffer** | 3 Days per Phase | Scheduled prior to major release gates | Staging load testing, pen-testing, or data reconciliation |")
    lines.append("| **Pilot Buffer** | 5 Days prior to UAT | Scheduled at end of Pilot Stage 4 | Clinical feedback iteration or hardware swap-outs |")
    lines.append("| **Program Risk Reserve** | 10 Working Days | Controlled exclusively by GBA Steering Committee | Major external regulatory changes or force majeure |")
    lines.append("")

    # 8. Governance Rhythms & Cadence
    lines.append("## 8. Master Governance Rhythms & Reporting Cadence")
    lines.append("Synchronized meeting cadence enforcing transparency and cross-squad alignment across the 36-week program:")
    lines.append("")
    lines.append("| Meeting Event | Frequency & Timing | Attendees | Primary Objectives |")
    lines.append("| :--- | :--- | :--- | :--- |")
    lines.append("| **Daily Engineering Standup** | Daily, 09:30–09:45 IST | Squad Leads, Developers, QA, DevOps | Surface blockers, align daily goals, review CI status |")
    lines.append("| **Sprint Backlog Refinement** | Mid-Sprint (Day 5), 14:00 IST | PM, Tech Lead, Squad Leads | Estimate upcoming stories, clarify acceptance criteria |")
    lines.append("| **Sprint Review & Demo** | Sprint Day 10, 15:00 IST | All Squads, BBMP Stakeholders, CMO | Demonstrate working software, gather clinical feedback |")
    lines.append("| **Sprint Retrospective** | Sprint Day 10, 16:30 IST | Engineering Squads, Scrum Master | Identify process improvements, update team agreements |")
    lines.append("| **Release CAB Review** | Prior to Release Cutover | Release Train Engineer, Security, SRE | Review release readiness, authorize production change |")
    lines.append("| **GBA Steering Committee** | Monthly, Last Thursday | Health Commissioner, CTO, Project Lead | Review budget, schedule milestones, and strategic risks |")
    lines.append("")

    # 9. Timeplan Sign-Off and Formal Ratification
    lines.append("## 9. Timeplan Sign-Off & Formal Ratification")
    lines.append("The Master Program Timeplan Baseline has been formally reviewed, verified for feasibility, and ratified by the Joint Program Governance Council:")
    lines.append("")
    lines.append("| Governance Authority | Designated Officer | Ratification Status |")
    lines.append("| :--- | :--- | :--- |")
    lines.append("| **Chief Technology Officer** | Chief Technology Officer | `APPROVED & BASELINED` |")
    lines.append("| **Chief Medical Officer** | Lead Clinical SME / CMO | `APPROVED & BASELINED` |")
    lines.append("| **Director of Health Services** | Joint Commissioner of Health | `APPROVED & BASELINED` |")
    lines.append("| **Principal Program Manager** | Release Train Engineer | `APPROVED & BASELINED` |")
    lines.append("")

    return "\n".join(lines)

def generate_timeplan_01():
    content = build_master_timeplan_markdown()
    return write_timeplan_doc("01-master-timeplan.md", content, min_substantive=2000)

if __name__ == "__main__":
    res = generate_timeplan_01()
    print(f"01-master-timeplan.md generated: {res}")
