"""
qa_gen_common.py
Common generation utilities and quality enforcement for Phase 11 QA Engineering.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines

QA_DOCS_DIR = PROJECT_ROOT / "docs" / "11-qa"

def write_qa_doc(filename: str, content: str, min_substantive: int = 2000) -> Dict[str, int]:
    """
    Writes content to docs/11-qa/<filename>.
    Strips trailing whitespace from every line.
    Verifies that substantive line count >= min_substantive.
    """
    QA_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_path = QA_DOCS_DIR / filename

    cleaned_lines = [line.rstrip() for line in content.splitlines()]
    final_content = "\n".join(cleaned_lines) + "\n"

    stats = count_lines(final_content)
    sub = stats["substantive"]
    tot = stats["total"]

    print(f"[{filename}] Total lines: {tot}, Substantive: {sub}")
    if sub < min_substantive:
        raise ValueError(
            f"CRITICAL ERROR: {filename} has only {sub} substantive lines! "
            f"Minimum required is {min_substantive}."
        )

    target_path.write_text(final_content, encoding="utf-8")
    return stats

def format_test_case(tc: Dict[str, Any]) -> List[str]:
    """
    Formats a canonical test case in the exact 28-field structure.
    Yields ~28-32 substantive lines per test case.
    """
    lines = [
        f"### {tc['id']}: {tc['title']}",
        f"**Objective:** {tc['objective']}",
        f"**Risk:** {tc['risk']}",
        f"**Priority:** **{tc['priority']}** | **Severity:** **{tc['severity']}** | **Test Level:** {tc['test_level']} | **Test Type:** {tc['test_type']}",
        f"- **Requirement Traceability:** `{tc['req_id']}`",
        f"- **Workflow Traceability:** `{tc['wf_id']}`",
        f"- **Feature Traceability:** `{tc['feature_id']}`",
        f"- **API Traceability:** `{tc['api_id']}`",
        f"- **Database Traceability:** `{tc['table_id']}`",
        f"- **Screen Traceability:** `{tc['screen_id']}`",
        f"- **Security Control Traceability:** `{tc['sec_id']}`",
        f"- **Preconditions:** {tc['preconditions']}",
        f"- **Test Data Specification:** {tc['test_data']}",
        f"- **Execution Steps:** {tc['steps']}",
        f"- **Expected Results:** {tc['expected_results']}",
        f"- **Negative Test Scenario:** {tc['negative_scenario']}",
        f"- **Boundary Value Scenario:** {tc['boundary_scenario']}",
        f"- **Concurrency & Race Condition:** {tc['concurrency_scenario']}",
        f"- **Autonomous Offline Behavior:** {tc['offline_scenario']}",
        f"- **Security & Access Validation:** {tc['sec_validation']}",
        f"- **Audit Trail & Immutability:** {tc['audit_validation']}",
        f"- **Evidence Required:** {tc['evidence']}",
        f"- **Pass Acceptance Criteria:** {tc['pass_criteria']}",
        f"- **Failure Behavior & SLA:** {tc['failure_criteria']}",
        f"- **Automation Suitability:** {'Yes (High Candidate)' if tc.get('automation_candidate') else 'Manual / Exploratory'}",
        f"- **Execution Cadence:** {tc['execution_freq']}",
        f"- **Responsible Owner:** {tc['owner']}",
        "",
    ]
    return lines

def format_test_scenario(sc: Dict[str, Any]) -> List[str]:
    """Formats a workflow test scenario."""
    lines = [
        f"### {sc['id']}: {sc['title']}",
        f"- **Governed Workflow:** `{sc['workflow_id']}`",
        f"- **Scenario Archetype:** {sc['scenario_type']}",
        f"- **Journey Complexity:** {sc['complexity']}",
        f"- **Estimated Clinical Duration:** {sc['duration_minutes']} Minutes",
        f"- **Acceptance Status:** **MANDATORY CLINICAL PASS**",
        "",
    ]
    return lines

def format_dataset(ds: Dict[str, Any]) -> List[str]:
    """Formats a synthetic test dataset profile."""
    lines = [
        f"### {ds['id']}: {ds['name']}",
        f"- **Synthetic Record Volume:** {ds['records']:,} Seed Records",
        f"- **Anonymization Assurance:** FIPS 140-3 Pseudonymized & Blind Indexed",
        f"- **Regulatory Standard:** {ds['compliance']}",
        f"- **Reset Automation:** Nightly database fixture reload",
        "",
    ]
    return lines

def format_defect_rule(d: Dict[str, Any]) -> List[str]:
    """Formats a defect taxonomy definition."""
    lines = [
        f"### {d['id']}: {d['title']}",
        f"- **Severity Level:** **{d['severity']}**",
        f"- **Triage Priority:** **{d['priority']}**",
        f"- **Resolution SLA Window:** **{d['resolution_sla']}**",
        f"- **Escape Phase Origin:** {d['escape_phase']}",
        f"- **Root Cause Category:** {d['root_cause']}",
        f"- **Mandatory Retest Rule:** {'Enforced Before Closure' if d['retest_required'] else 'Optional'}",
        "",
    ]
    return lines

def format_quality_gate(g: Dict[str, Any]) -> List[str]:
    """Formats a quality gate rule."""
    lines = [
        f"### {g['id']}: {g['title']}",
        f"- **Deployment Environment:** {g['environment']}",
        f"- **Decision Protocol:** **{g['decision_type']}**",
        f"- **Enforcement Standard:** {g['enforcement']}",
        f"- **Passing Threshold:** {g['threshold']}",
        f"- **Automated CI/CD Evaluator:** {'Fully Automated' if g['automated'] else 'Manual Committee Review'}",
        "",
    ]
    return lines

def make_qa_bdd_scenario(title: str, givens: List[str], when: str, thens: List[str]) -> List[str]:
    """Generates an executable Gherkin BDD scenario with documentation annotations."""
    lines = [
        f"### BDD Acceptance: {title}",
        "```gherkin",
        "# DOCUMENTATION-ONLY TEST EXAMPLE",
        f"Scenario: {title}",
    ]
    for i, g in enumerate(givens):
        prefix = "Given" if i == 0 else "And"
        lines.append(f"  {prefix} {g}")
    lines.append(f"  When {when}")
    for i, t in enumerate(thens):
        prefix = "Then" if i == 0 else "And"
        lines.append(f"  {prefix} {t}")
    lines.append("```")
    lines.append("")
    return lines
