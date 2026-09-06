"""
security_gen_common.py
Common generation utilities and quality enforcement for Phase 10 Security Engineering.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines

SEC_DOCS_DIR = PROJECT_ROOT / "docs" / "10-security"

def write_sec_doc(filename: str, content: str, min_substantive: int = 2000) -> Dict[str, int]:
    """
    Writes content to docs/10-security/<filename>.
    Strips trailing whitespace from every line.
    Verifies that substantive line count >= min_substantive.
    """
    SEC_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_path = SEC_DOCS_DIR / filename

    # Strip trailing whitespace on each line
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

def format_security_control(c: Dict[str, Any]) -> List[str]:
    """
    Formats a major security control in the exact 32-field format required:
    ### SEC-ARCH-001 / AUTH-001 / etc.
    Title: ...
    Control Type: ...
    ...
    Status: ...
    """
    lines = [
        f"### {c['id']}",
        f"**Title:** {c['title']}",
        f"**Control Type:** {c.get('control_type', 'Preventive')}",
        f"**Security Domain:** {c.get('security_domain', 'Architecture & Boundary Defense')}",
        f"**Priority:** {c.get('priority', 'P0 - Critical')}",
        f"**Risk:** {c.get('risk', 'High')}",
        f"**Threat:** {c.get('threat', 'Unauthorized Data Disclosure & Tampering')}",
        f"**Asset:** {c.get('asset', 'Electronic Health Record (EHR)')}",
        f"**Actor:** {c.get('actor', 'Adversary / Compromised Client')}",
        f"**Precondition:** {c.get('precondition', 'Network connectivity or physical clinic presence')}",
        f"**Control Objective:** {c.get('control_objective', 'Enforce absolute defense in depth')}",
        f"**Requirement:** {c.get('requirement', 'The platform shall enforce cryptographic controls.')}",
        f"**Implementation Guidance:** {c.get('implementation_guidance', 'Implement using verified libraries.')}",
        f"**Configuration Guidance:** {c.get('configuration_guidance', 'Strict production settings required.')}",
        f"**Failure Behavior:** {c.get('failure_behavior', 'Fail-secure and reject transaction.')}",
        f"**Monitoring:** {c.get('monitoring', 'Alert on security anomaly threshold.')}",
        f"**Audit Event:** {c.get('audit_event', 'SEC_EVENT_AUDIT_01')}",
        f"**Privacy Impact:** {c.get('privacy_impact', 'Supports DPDP Act 2023 compliance.')}",
        f"**Performance Impact:** {c.get('performance_impact', 'Negligible latency overhead (< 5ms).')}",
        f"**Availability Impact:** {c.get('availability_impact', 'Autonomous edge fallback preserves clinic operations.')}",
        f"**Related Requirement:** {c.get('related_requirement', 'SECR-001')}",
        f"**Related Workflow:** {c.get('related_workflow', 'WF-001')}",
        f"**Related API:** {c.get('related_api', 'API-001')}",
        f"**Related Database Entity:** {c.get('related_database_entity', 'TABLE-001 (auth_users)')}",
        f"**Related Architecture Component:** {c.get('related_architecture_component', 'ARCH-CONT-001')}",
        f"**Related Threat:** {c.get('related_threat', 'THREAT-001')}",
        f"**Related Test:** {c.get('related_test', 'SEC-TEST-001')}",
        f"**Acceptance Criteria:** {c.get('acceptance_criteria', '100% automated test pass rate with zero bypass.')}",
        f"**Evidence Required:** {c.get('evidence_required', 'Automated test suite execution logs and audit trail.')}",
        f"**Owner:** {c.get('owner', 'Chief Information Security Officer (CISO)')}",
        f"**Lifecycle:** {c.get('lifecycle', 'Active Baseline Control')}",
        f"**Status:** {c.get('status', 'PLANNED')}",
        "",
    ]
    return lines

def format_threat(t: Dict[str, Any]) -> List[str]:
    """
    Formats a threat in the exact 24-field format required:
    ### THREAT-001
    Title: ...
    Threat Category: ...
    ...
    Evidence: ...
    """
    lines = [
        f"### {t['id']}",
        f"**Title:** {t['title']}",
        f"**Threat Category:** {t.get('threat_category', 'Healthcare Data Breach')}",
        f"**STRIDE Category:** {t.get('stride_category', 'Information Disclosure')}",
        f"**Asset:** {t.get('asset', 'Patient Diagnostic & Prescription Records')}",
        f"**Threat Actor:** {t.get('threat_actor', 'External Adversary / Malicious Insider')}",
        f"**Entry Point:** {t.get('entry_point', 'Public REST API / Local Clinic Workstation')}",
        f"**Trust Boundary:** {t.get('trust_boundary', 'Clinic Edge / Cloud Ingress')}",
        f"**Preconditions:** {t.get('preconditions', 'Network access or local workstation access')}",
        f"**Attack Path:** {t.get('attack_path', 'Adversary probes endpoint or intercepts local queue.')}",
        f"**Potential Impact:** {t.get('potential_impact', 'Exposure of sensitive patient health data and regulatory penalties.')}",
        f"**Likelihood:** {t.get('likelihood', 'Medium')}",
        f"**Severity:** {t.get('severity', 'High')}",
        f"**Detectability:** {t.get('detectability', 'High (via automated SIEM / audit logging)')}",
        f"**Preventive Controls:** {t.get('preventive_controls', 'SEC-ARCH-001, API-SEC-001')}",
        f"**Detective Controls:** {t.get('detective_controls', 'AUDIT-SEC-001, SIEM Anomaly Alerts')}",
        f"**Corrective Controls:** {t.get('corrective_controls', 'INCIDENT-001, Automated Session Revocation')}",
        f"**Related Security Requirement:** {t.get('related_requirement', 'SECR-001')}",
        f"**Related API:** {t.get('related_api', 'API-001')}",
        f"**Related Database Table:** {t.get('related_table', 'TABLE-001 (auth_users)')}",
        f"**Related Workflow:** {t.get('related_workflow', 'WF-001')}",
        f"**Related Test:** {t.get('related_test', 'SEC-TEST-001')}",
        f"**Residual Risk:** {t.get('residual_risk', 'Low (Controlled via layered defenses)')}",
        f"**Risk Owner:** {t.get('risk_owner', 'Security Engineering Lead')}",
        f"**Treatment:** {t.get('treatment', 'Mitigate via defense-in-depth and continuous verification')}",
        f"**Evidence:** {t.get('evidence', 'Automated security test logs, penetration test report')}",
        "",
    ]
    return lines

def format_security_test(t: Dict[str, Any]) -> List[str]:
    """
    Formats a planned security test in the exact 20-field format required:
    ### SEC-TEST-001
    Test Category: ...
    ...
    Traceability: ...
    """
    lines = [
        f"### {t['id']}",
        f"**Test Category:** {t.get('category', 'API Security & Authorization')}",
        f"**Objective:** {t.get('objective', 'Verify cryptographic access barrier')}",
        f"**Security Control:** {t.get('security_control', 'SEC-ARCH-001')}",
        f"**Requirement:** {t.get('requirement', 'SECR-001')}",
        f"**Threat:** {t.get('threat', 'THREAT-001')}",
        f"**Preconditions:** {t.get('preconditions', 'Test client with valid/invalid credentials initialized')}",
        f"**Environment:** {t.get('environment', 'Isolated Security Staging Environment')}",
        f"**Test Data:** {t.get('test_data', 'Synthetic patient records and test JWT keypairs')}",
        f"**Execution Steps:** {t.get('execution_steps', '1. Issue request with forged token. 2. Observe gateway response.')}",
        f"**Expected Result:** {t.get('expected_result', 'Immediate HTTP 401/403 rejection with security audit log entry.')}",
        f"**Failure Criteria:** {t.get('failure_criteria', 'HTTP 200 response or unauthorized data leakage.')}",
        f"**Severity:** {t.get('severity', 'Critical')}",
        f"**Automation Candidate:** {t.get('automation', 'Yes (Automated CI/CD security gate in pytest/k6)')}",
        f"**Evidence:** {t.get('evidence', 'JSON test output report and SIEM audit event record')}",
        f"**Cleanup:** {t.get('cleanup', 'Purge synthetic test tokens and reset test user counters')}",
        f"**Related API:** {t.get('related_api', 'API-001')}",
        f"**Related UI:** {t.get('related_ui', 'SCREEN-001 (Staff Login Screen)')}",
        f"**Related Database:** {t.get('related_database', 'TABLE-001 (auth_users)')}",
        f"**Related Workflow:** {t.get('related_workflow', 'WF-001')}",
        f"**Traceability:** {t.get('traceability', 'PLANNED-TEST-SEC-001')}",
        "",
    ]
    return lines

def format_abac_policy(p: Dict[str, Any]) -> List[str]:
    """Formats an ABAC policy."""
    lines = [
        f"### {p['id']}: {p['title']}",
        f"- **Subject:** {p['subject']}",
        f"- **Resource:** {p['resource']}",
        f"- **Action:** {p['action']}",
        f"- **Environment:** {p['environment']}",
        f"- **Condition:** {p['condition']}",
        f"- **Decision:** {p['decision']}",
        f"- **Reason:** {p['reason']}",
        f"- **Audit Event:** {p['audit_event']}",
        f"- **Failure Response:** {p['failure_response']}",
        f"- **Related Requirement:** {p.get('related_requirement', 'SECR-003')}",
        f"- **Related Test:** {p.get('related_test', 'SEC-TEST-003')}",
        "",
    ]
    return lines

def format_incident_scenario(s: Dict[str, Any]) -> List[str]:
    """Formats a 10-phase Incident Response Scenario."""
    lines = [
        f"### {s['id']}: {s['title']}",
        f"**Incident Classification:** {s.get('classification', 'Severity-1 (Critical)')}",
        f"**Target Assets & Systems:** {s.get('assets', 'Clinic Edge Workstations & Cloud EHR')}",
        f"**1. Detect:** {s.get('detect', 'SIEM anomaly alert or clinic staff report.')}",
        f"**2. Triage:** {s.get('triage', 'Incident Commander assesses blast radius and confirms active exploit.')}",
        f"**3. Contain:** {s.get('contain', 'Revoke compromised credentials, isolate network VLAN, suspend sessions.')}",
        f"**4. Investigate:** {s.get('investigate', 'Analyze WORM audit logs, capture memory dump, inspect network flows.')}",
        f"**5. Eradicate:** {s.get('eradicate', 'Purge malicious implants, rotate all system secrets, patch vulnerability.')}",
        f"**6. Recover:** {s.get('recover', 'Restore verified clean backup, rebuild affected nodes from hardened gold image.')}",
        f"**7. Validate:** {s.get('validate', 'Execute automated security test suite and confirm zero indicator of compromise.')}",
        f"**8. Communicate:** {s.get('communicate', 'Statutory CERT-In 6-hour notification, DPO briefing, BBMP leadership advisory.')}",
        f"**9. Document:** {s.get('document', 'Compile formal forensic post-mortem report and evidentiary dossier.')}",
        f"**10. Lessons Learned:** {s.get('lessons_learned', 'Update threat model, tune detection thresholds, schedule staff training.')}",
        "",
    ]
    return lines

def make_sec_bdd_scenario(title: str, givens: List[str], when: str, thens: List[str]) -> List[str]:
    """Generates a BDD acceptance scenario in Gherkin syntax."""
    lines = [
        f"#### Scenario: {title}",
        "```gherkin",
        "# DOCUMENTATION-ONLY EXAMPLE",
    ]
    for i, g in enumerate(givens):
        prefix = "Given" if i == 0 else "  And"
        lines.append(f"{prefix} {g}")
    lines.append(f"When {when}")
    for i, t in enumerate(thens):
        prefix = "Then" if i == 0 else "  And"
        lines.append(f"{prefix} {t}")
    lines.append("```")
    lines.append("")
    return lines

def format_vapt_scenario(v: Dict[str, Any]) -> List[str]:
    """Formats a Penetration Testing & VAPT scenario."""
    lines = [
        f"### {v['id']}: {v['title']}",
        f"**Target Surface:** {v.get('target_surface', 'Perimeter API & Cloud Ingress')}",
        f"**Reconnaissance Phase:** {v.get('reconnaissance', 'Automated scanning and port enumeration')}",
        f"**Attack Vectors:** {v.get('attack_vectors', 'Network probing and protocol exploitation')}",
        f"**Exploitation Steps:** {v.get('exploitation_steps', '1. Scan target. 2. Probe flaw. 3. Attempt escalation.')}",
        f"**Proof of Concept & Evidence:** {v.get('evidence', 'Terminal capture, HTTP dump, and PoC script')}",
        f"**Remediation SLA:** {v.get('remediation_sla', 'Critical: 24h | High: 7 days | Medium: 30 days')}",
        f"**Retesting Criteria:** {v.get('retesting_criteria', 'Independent validation by CERT-In empaneled auditor')}",
        f"**Related Security Control:** {v.get('related_control', 'SEC-ARCH-001')}",
        f"**Related Threat:** {v.get('related_threat', 'THREAT-001')}",
        "",
    ]
    return lines

