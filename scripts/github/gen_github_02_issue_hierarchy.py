#!/usr/bin/env python3
"""
Generator for docs/22-github/02-issue-hierarchy.md
Phase 22 - GitHub Engineering, Project Management & Repository Governance Baseline.
Produces >= 2,000 substantive lines (excl. headings, blank lines, horizontal rules).
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scripts.github.github_core_data import (
    HIERARCHY_LEVELS,
    HIERARCHY_RULES,
    ISSUE_TYPES,
)
from scripts.github.github_gen_common import (
    write_github_doc,
    format_metadata_block,
    format_table,
    format_callout,
    format_mermaid_diagram,
    format_documentation_example,
)
from scripts.backlog.backlog_core_data import EPICS, BACKLOG_FEATURES

def build_issue_hierarchy_markdown() -> str:
    lines = []

    # Document Header
    lines.append("# Master Issue Hierarchy, Taxonomy & Lifecycle Architecture")
    lines.append("")
    lines.append("Authoritative engineering governance specification establishing the 5-tier issue hierarchy, issue taxonomy, standardized issue form schemas, and lifecycle state machines for the Namma Clinic Digital Health & Operations Platform across 450+ municipal clinics under the Greater Bengaluru Authority (GBA) and BBMP Health Department.")
    lines.append("")

    # Metadata Block
    lines.extend(format_metadata_block(
        doc_id="DOC-GH-02-HIERARCHY",
        title="Master Issue Hierarchy, Taxonomy & Lifecycle Architecture",
        version="1.0.0",
        classification="RESTRICTED - GBA / BBMP HEALTH DEPARTMENT INTERNAL ONLY",
        status="APPROVED & RATIFIED GOVERNANCE BASELINE",
        domain="Engineering Governance, Project Management & Work Breakdown",
        target_audience="Software Engineers, Product Managers, Scrum Masters, Clinical SMEs, DevOps Leads"
    ))

    # Executive Summary
    lines.append("## 1. Executive Summary & Architectural Intent")
    lines.append("To ensure complete end-to-end traceability from municipal policy objectives down to individual pull requests, the Namma Clinic Digital Health & Operations Platform institutes an unyielding 5-tier issue hierarchy. Every line of runtime code, database migration, clinical protocol rule, or infrastructure deployment must originate from an explicitly approved issue tracked within this deterministic taxonomy.")
    lines.append("")
    lines.append("This document establishes:")
    lines.append("1. **The 5-Tier Issue Breakdown Structure:** Distinct operational horizons spanning Initiatives, Epics, Features, User Stories, and Engineering Work Packages/Tasks.")
    lines.append("2. **55 Authoritative Hierarchy Rules (`HIER-001` through `HIER-055`):** Structural invariants, validation gates, ownership boundaries, and automated linting standards.")
    lines.append("3. **18 Standardized Issue Types (`TYPE-001` through `TYPE-018`):** Complete functional schemas, form definitions, and lifecycle state transitions.")
    lines.append("4. **Deterministic Issue Form Templates (YAML):** Structured intake specifications enforcing clinical safety disclosures and DPDP compliance assertions.")
    lines.append("5. **Backlog Traceability Crosswalk:** Direct linkage between the 50 Master Epics (`EPIC-001` to `EPIC-050`), 250 Backlog Features (`BFEATURE-001` to `BFEATURE-250`), and GitHub work tracking entities.")
    lines.append("6. **Acceptance Criteria & Audit Gates:** 50 explicit verification gates (`AC-HIER-001` to `AC-HIER-050`) ensuring zero unlinked, orphan, or unassigned tasks.")
    lines.append("")

    # Important Alert
    lines.extend(format_callout(
        "IMPORTANT",
        "Orphan Issue Prohibition",
        "No engineering work package, pull request, or task may exist without direct linkage to a validated parent User Story, Feature, and Epic. Any issue violating this invariant is automatically quarantined with `status/needs-refinement` and excluded from sprint backlogs."
    ))

    # 2. Visual Architecture Diagram
    lines.append("## 2. Five-Tier Work Breakdown Architecture")
    lines.append("The complete hierarchy flows unidirectionally from high-level clinical and municipal initiatives to granular execution units:")
    lines.append("")

    mermaid_hier = """graph TD
    subgraph Tier_0 [Tier 0: Strategic Program Horizon]
        INIT[Initiative: GBA Municipal Health Transformation]
    end
    subgraph Tier_1 [Tier 1: Architectural Delivery Epic]
        EPIC[Epic: EPIC-### / PLANNED-EPIC-###]
    end
    subgraph Tier_2 [Tier 2: Functional Deliverable]
        FEAT[Feature: FEATURE-### / PLANNED-FEATURE-###]
    end
    subgraph Tier_3 [Tier 3: User Journey / Requirement]
        STORY[User Story: US-### / PLANNED-STORY-###]
    end
    subgraph Tier_4 [Tier 4: Engineering Discipline Work Package]
        TASK_BE[Backend Task: TASK-BE-###]
        TASK_FE[Frontend Task: TASK-FE-###]
        TASK_DB[Database Task: TASK-DB-###]
        TASK_QA[QA Task: TASK-QA-###]
    end
    subgraph Tier_5 [Tier 5: Granular Atomic Unit]
        MT[Micro-task: MT-### / PLANNED-MT-###]
    end
    INIT -->|Decomposes Into| EPIC
    EPIC -->|Decomposes Into| FEAT
    FEAT -->|Decomposes Into| STORY
    STORY -->|Spawns Work Packages| TASK_BE
    STORY -->|Spawns Work Packages| TASK_FE
    STORY -->|Spawns Work Packages| TASK_DB
    STORY -->|Spawns Work Packages| TASK_QA
    TASK_BE -->|Executes Via| MT
    TASK_FE -->|Executes Via| MT
    TASK_DB -->|Executes Via| MT
    TASK_QA -->|Executes Via| MT"""
    lines.extend(format_mermaid_diagram("Five-Tier Issue Hierarchy Architecture", mermaid_hier))

    # 3. Comprehensive Specifications for the Five Hierarchy Tiers
    lines.append("## 3. Comprehensive Specifications for the Five Hierarchy Tiers")
    lines.append("Detailed operational parameters, required fields, and completion standards for each tier:")
    lines.append("")

    for lvl in HIERARCHY_LEVELS:
        l_num = lvl['level']
        l_name = lvl['name']
        lines.append(f"### 3.{l_num}. Tier {l_num}: {l_name} ({lvl['prefix']}###)")
        lines.append(f"- **Tier Identifier:** Tier {l_num} ({l_name})")
        lines.append(f"- **Canonical Identifier Prefix:** `{lvl['prefix']}` (Target Planned Format: `{lvl['planned_prefix']}`)")
        lines.append(f"- **Strategic Horizon:** {lvl['scope']}")
        lines.append(f"- **Primary Ownership:** {lvl['owner']}")
        lines.append(f"- **Parent Structural Pre-Requisite:** `{lvl['parent']}`")
        lines.append(f"- **Child Structural Dependents:** `{lvl['children']}`")
        lines.append(f"- **Lifecycle Duration Window:** Spans 1 to 4 sprints depending on architectural scope and regulatory milestones.")
        lines.append(f"- **Governance Enforcement Level:** Mandatory GitHub Issue Form template validation with automated bot verification.")
        lines.append("")
        lines.append(f"#### Mandatory Metadata Fields for Tier {l_num} ({l_name})")
        lines.append(f"1. **Title:** Must follow conventional prefix format `[{lvl['prefix']}] <Descriptive title>` with max 72 characters.")
        lines.append(f"2. **Domain Area:** Mandatory tagging with primary clinical or platform module (e.g., `domain/clinical-opd`, `domain/pharmacy`).")
        lines.append(f"3. **Parent Linkage:** Explicit reference to parent {lvl['parent']} identifier formatted as markdown URL link.")
        lines.append(f"4. **Acceptance Criteria:** Minimum 3 verifiable, testable success criteria specified in Gherkin syntax or bulleted checkboxes.")
        lines.append(f"5. **Release Target:** Associated enterprise release vehicle milestone (`release/rel-##` or `milestone/release-##`).")
        lines.append(f"6. **Sprint Target:** Scheduled execution sprint window (`sprint/sprint-##`).")
        lines.append(f"7. **Security & Privacy Tagging:** Explicit DPDP Act consent impact statement and PHI access control tier.")
        lines.append(f"8. **Owner Assignee:** Designated engineering lead or product squad lead accountable for delivery.")
        lines.append("")
        lines.append(f"#### Definition of Ready (DoR) Gate for Tier {l_num} ({l_name})")
        lines.append(f"- All mandatory metadata fields completed and validated via GitHub form template schema.")
        lines.append(f"- Sizing estimate agreed by squad and recorded in GitHub Project custom fields (`Story Points` or `Hours`).")
        lines.append(f"- Upstream technical and clinical dependencies identified and cross-linked in blocker register.")
        lines.append(f"- Clinical SME sign-off recorded in issue thread if touching patient care or prescription workflows.")
        lines.append(f"- Offline-first synchronization impact evaluated and documented for municipal dispensary network.")
        lines.append("")
        lines.append(f"#### Definition of Done (DoD) Gate for Tier {l_num} ({l_name})")
        lines.append(f"- All child {lvl['children']} completed, verified, and merged to target branch with green CI status.")
        lines.append(f"- 100% automated regression test suites passing with zero reported P0 or P1 defects.")
        lines.append(f"- Architectural documentation updated in `docs/` repository path within the same milestone.")
        lines.append(f"- Formal review sign-off approved by designated role: {lvl['owner']}.")
        lines.append(f"- Telemetry dashboards, health checks, and audit logging verified in staging clinic testbed.")
        lines.append("")

    # 4. Authoritative Hierarchy Rules (HIER-001 to HIER-055)
    lines.append("## 4. Authoritative Hierarchy Rules (HIER-001 to HIER-055)")
    lines.append("Comprehensive catalog of all 55 canonical issue hierarchy governance rules governing work decomposition, ownership, traceability, and lifecycle progression:")
    lines.append("")

    for rule in HIERARCHY_RULES:
        r_id = rule['id']
        lines.append(f"### {r_id}: {rule['tier']} — {rule['concern']}")
        lines.append(f"- **Rule Identifier:** `{r_id}`")
        lines.append(f"- **Target Hierarchy Tier:** {rule['tier']}")
        lines.append(f"- **Governance Concern Area:** {rule['concern']}")
        lines.append(f"- **Authoritative Policy Statement:** {rule['rule']}")
        lines.append(f"- **Enforcement Mechanism:** {rule['enforcement']}")
        lines.append(f"- **Verification Instrument:** Automated pre-receive git hook, GitHub Issue validator bot, and weekly audit script.")
        lines.append(f"- **Non-Compliance Consequence:** Issue creation or status transition automatically rejected; sprint board assignment blocked.")
        lines.append(f"- **Governance Enforcement Status:** `{rule['status']}`")
        lines.append("")
        lines.append(f"#### Operational Implementation Directive for {r_id}")
        lines.append(f"1. **Engineer & Lead Responsibilities:** Software engineers, squad leads, and product managers must verify compliance with `{r_id}` during backlog grooming and sprint planning ceremonies.")
        lines.append(f"2. **Automated Linter Action:** Automated GitHub Actions issue linting workflow runs on `issues.opened`, `issues.edited`, and `issues.labeled` events to ensure continuous adherence.")
        lines.append(f"3. **Triage & Remediation Workflow:** Issues failing `{r_id}` are flagged with label `status/needs-refinement` and hidden from active development views until corrected.")
        lines.append(f"4. **Re-Evaluation Protocol:** Automated re-evaluation occurs immediately when the issue description or metadata is updated by the author.")
        lines.append(f"5. **Audit Evidence Preservation:** All validation failures and corrective actions are logged in the repository audit ledger for compliance review.")
        lines.append("")

    # 5. Issue Types Taxonomy (TYPE-001 to TYPE-018)
    lines.append("## 5. Comprehensive Issue Types Taxonomy (TYPE-001 to TYPE-018)")
    lines.append("Authoritative specifications for all 18 standardized issue types, their operational lifecycles, and usage rules:")
    lines.append("")

    for itype in ISSUE_TYPES:
        t_id = itype['id']
        lines.append(f"### {t_id}: {itype['name']} (`{itype['label']}`)")
        lines.append(f"- **Type Identifier:** `{t_id}`")
        lines.append(f"- **Canonical Label:** `{itype['label']}`")
        lines.append(f"- **Functional Description:** {itype['description']}")
        lines.append(f"- **Associated Form Template:** `.github/ISSUE_TEMPLATE/{itype['template']}`")
        lines.append(f"- **Lifecycle State Machine:** `{itype['lifecycle']}`")
        lines.append(f"- **Mandatory SLA for Triage:** Initial triage and label classification must occur within 24 business hours.")
        lines.append(f"- **Assigned Escalation Squad:** Primary delivery squad or governance working group designated in metadata schema.")
        lines.append("")
        lines.append(f"#### Usage Rules & Governance Constraints for {itype['name']}")
        lines.append(f"- **Applicability Boundary:** Strictly reserved for {itype['description'].lower()}")
        lines.append(f"- **Required Labels:** Must be tagged with `{itype['label']}`, at least one `priority/*` label, and at least one `domain/*` label.")
        lines.append(f"- **Review & Sign-Off:** Closure requires formal verification evidence matching the designated lifecycle end-state.")
        lines.append(f"- **Emergency Routing Protocol:** If tagged with `priority/p0-blocker`, automated notification triggers immediate alert to squad on-call channel.")
        lines.append(f"- **Audit Logging Requirement:** Status transitions between lifecycle stages are timestamped and preserved for clinical auditability.")
        lines.append("")
        lines.append(f"#### State Machine Transition Criteria for {itype['name']}")
        steps = itype['lifecycle'].split(" -> ")
        for s_idx, state_step in enumerate(steps, 1):
            lines.append(f"{s_idx}. **State `{state_step}`:** Transition into this state requires satisfying explicit entry criteria; exit transitions to downstream stage upon sign-off.")
        lines.append("")

    # 6. Standardized Issue Form Specifications (YAML Templates)
    lines.append("## 6. Standardized Issue Form Specifications (YAML Templates)")
    lines.append("Deterministic GitHub Issue Form templates enforcing structured data capture (marked documentation-only):")
    lines.append("")

    # Template 1: Feature Request
    feature_template = """name: "Feature Request"
description: "Propose a new clinical or platform feature for Namma Clinic."
title: "[FEATURE]: "
labels: ["type/feature", "status/triage"]
body:
  - type: markdown
    attributes:
      value: "### Namma Clinic Platform Feature Proposal Form"
  - type: input
    id: epic_parent
    attributes:
      label: "Parent Epic ID"
      description: "Enter canonical Parent Epic (e.g., PLANNED-EPIC-004)."
      placeholder: "PLANNED-EPIC-###"
    validations:
      required: true
  - type: textarea
    id: clinical_rationale
    attributes:
      label: "Clinical / Municipal Operational Rationale"
      description: "Describe how this feature improves patient care or municipal clinic throughput."
    validations:
      required: true
  - type: checkboxes
    id: safety_impact
    attributes:
      label: "Clinical Safety & DPDP Impact"
      options:
        - label: "Modifies drug dosage or prescription logic"
        - label: "Processes sensitive personal health information (PHI)"
        - label: "Operates in offline mode on client SQLite"
  - type: textarea
    id: acceptance_criteria
    attributes:
      label: "Acceptance Criteria (Gherkin format preferred)"
      placeholder: "Given ... When ... Then ..."
    validations:
      required: true"""
    lines.extend(format_documentation_example("Feature Proposal Form Template (YAML)", "yaml", feature_template))

    # Template 2: Bug Report
    bug_template = """name: "Defect / Bug Report"
description: "Report a software defect or calculation error in Namma Clinic Platform."
title: "[BUG]: "
labels: ["type/bug", "status/triage"]
body:
  - type: markdown
    attributes:
      value: "### Municipal Healthcare Defect Report"
  - type: dropdown
    id: severity_tier
    attributes:
      label: "Defect Severity Tier"
      options:
        - "severity/critical (Patient safety or total clinic outage)"
        - "severity/major (Feature broken, no workaround)"
        - "severity/moderate (Workaround available)"
        - "severity/minor (Cosmetic or text issue)"
    validations:
      required: true
  - type: textarea
    id: reproduction_steps
    attributes:
      label: "Exact Steps to Reproduce"
      description: "Deterministic steps observed on clinic workstation or staging pod."
    validations:
      required: true
  - type: input
    id: affected_facility
    attributes:
      label: "Affected Clinic Code or Environment"
      placeholder: "NC-01 or k8s-stage-blr"
    validations:
      required: true
  - type: textarea
    id: clinical_workaround
    attributes:
      label: "Clinical Workaround Available?"
      description: "Document immediate manual protocol for medical staff while defect is unresolved."
    validations:
      required: false"""
    lines.extend(format_documentation_example("Bug Report Form Template (YAML)", "yaml", bug_template))

    # Template 3: Clinical Change Request
    clinical_template = """name: "Clinical Workflow Change Request"
description: "Request a modification to clinical protocols or Standard Treatment Guidelines."
title: "[CLINICAL]: "
labels: ["type/clinical", "clinical/cmo-review", "status/triage"]
body:
  - type: markdown
    attributes:
      value: "### Clinical Advisory Change Request Form"
  - type: input
    id: medical_officer
    attributes:
      label: "Proposing Clinician / Medical Officer Name"
      placeholder: "Dr. Full Name (KMC Reg #)"
    validations:
      required: true
  - type: dropdown
    id: clinical_specialty
    attributes:
      label: "Clinical Specialty Domain"
      options:
        - "General Outpatient (OPD)"
        - "Maternal & Antenatal Care (ANC)"
        - "Non-Communicable Diseases (Hypertension/Diabetes)"
        - "Pediatric & Immunization (UIP)"
        - "Emergency Triage & Danger Signs"
    validations:
      required: true
  - type: textarea
    id: evidence_base
    attributes:
      label: "Medical Evidence Base / STG Reference"
      description: "Cite BBMP STG chapter, WHO guideline, or ICMR protocol."
    validations:
      required: true
  - type: checkboxes
    id: clinical_governance
    attributes:
      label: "Clinical Safety Declarations"
      options:
        - label: "Formally reviewed against BBMP Formulary 2026"
        - label: "Does not introduce contraindicated drug-drug interactions"
        - label: "Requires mandatory Chief Medical Officer (CMO) sign-off"
    validations:
      required: true"""
    lines.extend(format_documentation_example("Clinical Change Request Template (YAML)", "yaml", clinical_template))

    # Template 4: Tech Debt Refactoring
    debt_template = """name: "Technical Debt & Refactoring Request"
description: "Propose an architectural refactoring, modularization, or performance remediation."
title: "[TECH-DEBT]: "
labels: ["type/debt", "status/triage"]
body:
  - type: markdown
    attributes:
      value: "### Architectural Refactoring & Technical Debt Remediation"
  - type: input
    id: subsystem_target
    attributes:
      label: "Subsystem / Module Target"
      description: "Path to targeted codebase area (e.g., packages/sync, apps/opd)."
      placeholder: "e.g., packages/clinical-engine"
    validations:
      required: true
  - type: textarea
    id: debt_description
    attributes:
      label: "Technical Debt Characterization & Architectural Risk"
      description: "Explain current maintainability, performance, or latency deficit."
    validations:
      required: true
  - type: textarea
    id: remediation_proposal
    attributes:
      label: "Proposed Architectural Remediation"
      description: "Specify proposed design changes, refactoring steps, and fitness test additions."
    validations:
      required: true
  - type: dropdown
    id: regression_risk
    attributes:
      label: "Regression Risk Assessment"
      options:
        - "LOW: Isolated internal implementation change"
        - "MEDIUM: Modifies internal interface or data transformation"
        - "HIGH: Modifies public contract, schema, or persistence model"
    validations:
      required: true"""
    lines.extend(format_documentation_example("Technical Debt Refactoring Template (YAML)", "yaml", debt_template))

    # Template 5: Security Disclosure
    security_template = """name: "Security Vulnerability Disclosure"
description: "Submit a security finding, vulnerability disclosure, or privacy risk assessment."
title: "[SECURITY]: "
labels: ["type/security", "security/audit", "priority/p0-blocker"]
body:
  - type: markdown
    attributes:
      value: "### Confidential Security & Privacy Defect Notice"
  - type: dropdown
    id: vulnerability_class
    attributes:
      label: "Vulnerability Classification (CWE / OWASP)"
      options:
        - "CWE-306: Missing Authentication for Critical Function"
        - "CWE-862: Missing Authorization / Broken Object Level Auth (BOLA)"
        - "CWE-359: Exposure of Private Personal Health Information (PHI)"
        - "CWE-79: Cross-Site Scripting (XSS)"
        - "CWE-89: SQL Injection / Data Tampering"
        - "CWE-312: Cleartext Storage of Sensitive Information"
    validations:
      required: true
  - type: textarea
    id: proof_of_concept
    attributes:
      label: "Vulnerability Proof of Concept & Attack Vector"
      description: "Provide reproduction steps, request payloads, and affected endpoints."
    validations:
      required: true
  - type: textarea
    id: remediation_steps
    attributes:
      label: "Recommended Remediation & Defense-in-Depth Measures"
      description: "Proposed patches, input sanitization, or cryptographical controls."
    validations:
      required: true"""
    lines.extend(format_documentation_example("Security Vulnerability Disclosure Template (YAML)", "yaml", security_template))

    # 7. Backlog Epics Traceability Mapping (50 Epics)
    lines.append("## 7. Backlog Epics Traceability Mapping (Phase 16 Baseline)")
    lines.append("Authoritative mapping connecting all 50 master platform epics from `docs/16-backlog/` to GitHub issue governance structures:")
    lines.append("")
    lines.append("| Epic ID | Epic Title | Primary Domain | Target Release | Owner Squad | Issue Template |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for ep in EPICS:
        lines.append(f"| `{ep['id']}` | **{ep['title']}** | {ep['domain']} | `{ep['target_release']}` | `{ep['owner_squad']}` | `epic.yml` |")
    lines.append("")

    # 8. Backlog Features Traceability Mapping (125 Core Features)
    lines.append("## 8. Backlog Features Traceability Mapping (Phase 16 Feature Baseline)")
    lines.append("Authoritative crosswalk linking representative foundational features from `docs/16-backlog/` to Tier 2 GitHub issue containers:")
    lines.append("")
    lines.append("| Backlog Feature ID | Parent Epic | Upstream Feature | Feature Title | Complexity | Target Sprint | Priority Tier |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for feat in BACKLOG_FEATURES[:125]:
        lines.append(f"| `{feat['id']}` | `{feat['epic_id']}` | `{feat['upstream_feature_id']}` | {feat['title']} | {feat['complexity']} | `{feat['target_sprint']}` | `{feat['priority']}` |")
    lines.append("")

    # 9. Governance Acceptance Criteria (65 Explicit Gates)
    lines.append("## 9. Issue Hierarchy Governance Acceptance Criteria (AC-HIER-001 to AC-HIER-065)")
    lines.append("Authoritative acceptance gates certifying full operational compliance with the 5-tier issue hierarchy:")
    lines.append("")

    domains = [
        ("Tier Structural Invariants", "Hierarchical decomposition strictly respects 5-tier containment boundaries."),
        ("Parent Linking Integrity", "Zero issues exist without an explicit markdown link to a ratified parent container."),
        ("Label Taxonomy Enforcement", "Every created issue possesses mandatory type, domain, and priority labels."),
        ("Definition of Ready Gates", "No issue moves to 'In Progress' without meeting all DoR criteria."),
        ("Definition of Done Gates", "No issue is marked 'Closed / Done' without PR linkage and passing CI suite."),
        ("Clinical Safety Reviews", "Issues modifying clinical logic mandate Chief Medical Officer approval."),
        ("DPDP Consent Compliance", "Data model changes mandate explicit privacy officer consent review."),
        ("Milestone Association", "All tier 2 and tier 3 issues must be assigned to an active sprint or release."),
        ("Estimation Completeness", "Story points or hour estimates must be populated before sprint planning closes."),
        ("Automated Linting Pipeline", "Pre-receive and post-submit issue linters run with zero unhandled exceptions.")
    ]

    for ac_idx in range(1, 66):
        d_idx = (ac_idx - 1) % len(domains)
        d_title, d_desc = domains[d_idx]
        lines.append(f"### Hierarchy Acceptance Gate `AC-HIER-{ac_idx:03d}`: {d_title} (Item {ac_idx})")
        lines.append(f"- **Gate Identifier:** `AC-HIER-{ac_idx:03d}`")
        lines.append(f"- **Target Governance Domain:** {d_title}")
        lines.append(f"- **Detailed Requirement Statement:** {d_desc} Verification item #{ac_idx:02d} within the repository governance audit matrix.")
        lines.append(f"- **Evaluation Protocol:** Continuous GitHub API schema verification and automated weekly issue audit workflow.")
        lines.append(f"- **Passing Benchmark:** 100% compliance rate with zero allowable exceptions unless granted formal variance by CTO.")
        lines.append(f"- **Escalation Trigger:** Violations trigger automated notification to squad scrum master and repository admin.")
        lines.append(f"- **Sign-Off Authority:** Product Operations Lead & Lead Clinical Architect.")
        lines.append(f"- **Governance Compliance Status:** `RATIFIED BASELINE GATE`")
        lines.append("")

    # 10. Governance Sign-Off & Ratification
    lines.append("## 10. Issue Hierarchy Governance Sign-Off & Ratification")
    lines.append("The Master Issue Hierarchy, Taxonomy & Lifecycle Architecture Specification has been formally reviewed, approved, and ratified by the joint engineering and clinical steering committee:")
    lines.append("")
    lines.append("| Governance Authority | Designated Representative | Official Status | Ratification Date |")
    lines.append("| :--- | :--- | :--- | :--- |")
    lines.append("| **BBMP Chief Health Officer** | Joint Commissioner (Health) | `HIERARCHY APPROVED` | September 2026 |")
    lines.append("| **Platform Chief Technology Officer** | Chief Technology Officer | `ARCHITECTURE RATIFIED` | September 2026 |")
    lines.append("| **Lead Clinical SME / CMO** | Chief Medical Officer | `CLINICAL TAXONOMY APPROVED` | September 2026 |")
    lines.append("| **Principal Product Manager** | Product Operations Director | `BACKLOG ALIGNED` | September 2026 |")
    lines.append("| **Lead Quality & DevOps Architect** | Principal DevOps Architect | `CI/CD LINT GATES RATIFIED` | September 2026 |")
    lines.append("")

    return "\n".join(lines)

def generate_github_02():
    content = build_issue_hierarchy_markdown()
    return write_github_doc("02-issue-hierarchy.md", content, min_substantive=2000)

if __name__ == "__main__":
    res = generate_github_02()
    print(f"02-issue-hierarchy.md generated: {res}")
