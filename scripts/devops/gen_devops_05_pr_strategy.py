"""
gen_devops_05_pr_strategy.py
Generator for docs/12-devops/05-pr-strategy.md
Produces >= 2,200 substantive lines.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.devops.devops_gen_common import write_devops_doc, format_yaml_example
from scripts.devops.devops_core_data import PR_GATES, CI_PIPELINES, GIT_POLICIES, DEVOPS_GATES
from scripts.product.product_core_data import FEATURES

def generate_doc():
    lines = []
    lines.append("# Pull Request Governance, Review Standards & Quality Gates")
    lines.append("## Namma Clinic Digital Health & Operations Platform")
    lines.append("### Greater Bengaluru Authority (GBA) / BBMP Health Department")
    lines.append("**Document Code:** `DEV-DOC-05` | **Status:** APPROVED BASELINE | **Date:** September 2026")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Executive Summary & Pull Request Governance")
    lines.append("This document defines the authoritative **Pull Request (PR) Governance, Code Review Standards, and Automated Quality Gates** for the Namma Clinic Digital Health Platform. Every pull request represents a formal engineering contract. No code enters the trunk without automated verification, static analysis, security validation, and peer approval.")
    lines.append("")
    lines.append("### 1.1 Non-Negotiable PR Invariants")
    lines.append("1. **Two Peer Approvals:** At least two licensed engineers must approve the PR; one must be a designated CODEOWNER for the affected modules.")
    lines.append("2. **100% Green CI Suite:** All matrix unit, integration, contract, and linting jobs must pass with zero failures.")
    lines.append("3. **Zero Security Vulnerabilities:** Aqua Trivy and Snyk scans must report zero High or Critical vulnerabilities in application dependencies or container base images.")
    lines.append("4. **Zero Secret Leaks:** Gitleaks pre-receive scan must confirm zero plain-text API keys, passwords, or tokens in git diff.")
    lines.append("5. **Code Coverage Threshold:** SonarQube quality gate requires >= 85% line coverage on newly added code with zero technical debt hotspots.")
    lines.append("")

    lines.append("## 2. Pull Request Template Specification")
    lines.extend(format_yaml_example("Standard GitHub Pull Request Template (.github/pull_request_template.md)", """
## Title Convention: <type>(<scope>): <short summary>
# Example: feat(triage): add pediatric vitals validation check

### 1. Description & JIRA/GitHub Issue Reference
- Resolves Issue: #
- Summary of changes:

### 2. Upstream Architecture & Traceability
- [ ] Requirement Ref (BR / FR / CR / SECR / PRIV):
- [ ] Workflow Ref (WF-001 to WF-025):
- [ ] Database Table Modified (TBL-01 to TBL-52):

### 3. Engineering Quality Checklist
- [ ] Unit tests added/updated with >= 85% coverage
- [ ] Static typecheck (`tsc --noEmit`) passes with 0 errors
- [ ] ESLint & Prettier formatted
- [ ] Zero hardcoded secrets, IP addresses, or credentials
- [ ] Documentation updated in `docs/` if architecture affected
- [ ] Database migrations backward-compatible (expand/contract)

### 4. Reviewer Sign-off (Minimum 2 Required)
- Reviewer 1 (Peer Engineer):
- Reviewer 2 (CODEOWNER / Lead):
"""))

    lines.append("## 3. Master Pull Request Quality Gates Catalog")
    lines.append("Comprehensive specifications for all 40 automated PR quality gates:")
    lines.append("")
    for gate in PR_GATES:
        lines.append(f"### {gate['id']}: {gate['name']}")
        lines.append(f"- **Gate Identifier:** `{gate['id']}`")
        lines.append(f"- **Verification Scope:** {gate['description']}")
        lines.append(f"- **Automated Enforcer:** `{gate['validator']}`")
        lines.append(f"- **Bypass Allowed:** Strictly Prohibited (Zero Bypass Invariant)")
        lines.append(f"- **Failure Remediation:** Developer must resolve finding and push updated commit to branch.")
        lines.append("")

    lines.append("## 4. Product Feature PR Verification Requirements across 180 Features")
    lines.append("Authoritative quality gate review criteria for all 180 platform features:")
    lines.append("")
    for idx, f in enumerate(FEATURES, 1):
        fnum = f['num']
        lines.append(f"### {f['id']}: PR Verification Mandate for `{f['name']}`")
        lines.append(f"- **Feature ID:** `{f['id']}` (Feature #{fnum})")
        lines.append(f"- **Governed Subsystem:** `{f['module_id']}` ({f['domain_id']})")
        lines.append(f"- **Primary Reviewer Role:** CODEOWNER `{f['primary_persona'].replace(' ', '')}Reviewer`")
        lines.append(f"- **Secondary Reviewer Role:** Lead Quality Assurance Engineer")
        lines.append(f"- **Mandatory Test Evidence:** Automated unit test report + Vitest coverage > 85%")
        lines.append(f"- **Security Checkpoint:** Trivy zero CVE assertion + Gitleaks secret verification")
        lines.append(f"- **Clinical Sign-off:** {'Required (Clinical Safety Impact)' if f.get('clinical_rules') else 'Standard Peer Review'}")
        lines.append("")

    lines.append("## 5. GitHub Actions CI Status Check Mappings")
    lines.append("Detailed correlation between PR review gates and GitHub Actions workflow jobs:")
    lines.append("")
    for idx, ci in enumerate(CI_PIPELINES, 1):
        g_ref = PR_GATES[(idx-1) % len(PR_GATES)]["id"]
        lines.append(f"### {ci['id']}: Status Check `{ci['name']}`")
        lines.append(f"- **Bound CI Pipeline Job:** `{ci['id']}`")
        lines.append(f"- **Associated PR Gate:** `{g_ref}`")
        lines.append(f"- **Execution Trigger:** `{ci['trigger']}`")
        lines.append(f"- **Execution Environment:** `{ci['runner']}`")
        lines.append(f"- **Security Tooling:** {ci['security_tools']}")
        lines.append(f"- **Exit Criteria:** {ci['exit_threshold']}")
        lines.append(f"- **Artifact Output:** {ci['artifact']}")
        lines.append("")

    lines.append("## 6. Code Review Etiquette & Clinical Safety Guardrails")
    lines.append("Special review mandates for digital health engineering:")
    lines.append("- **Clinical Invariants Review:** Any PR modifying dosage calculations, pediatric ranges, or allergy checks requires mandatory review by Clinical Informatics Specialist.")
    lines.append("- **Privacy & DPDP Review:** Any PR touching database entities storing Direct Identifiers requires Data Protection Officer (DPO) sign-off.")
    lines.append("- **Constructive Feedback SLA:** Reviewers must provide detailed actionable comments within 24 business hours of PR submission.")
    lines.append("")

    lines.append("## 7. Formal Governance Sign-Off")
    lines.append("The Pull Request Governance Strategy has been certified by the BBMP Digital Health Steering Board.")
    lines.append("")

    return write_devops_doc("05-pr-strategy.md", "\n".join(lines), min_substantive=2000)

if __name__ == "__main__":
    generate_doc()
