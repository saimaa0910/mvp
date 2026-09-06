"""
gen_sec_16_testing.py
Generator for docs/10-security/16-security-testing.md
Produces >= 2,000 substantive lines detailing planned security testing strategy.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.security.security_gen_common import write_sec_doc, format_security_test, make_sec_bdd_scenario
from scripts.security.security_core_data import SECURITY_TESTS

def generate_doc():
    lines = []
    lines.append("# Security Testing Strategy & Verification Pipeline Specification")
    lines.append("## Namma Clinic Digital Health & Operations Platform")
    lines.append("### Greater Bengaluru Authority (GBA) / BBMP Health Department")
    lines.append("**Standard:** OWASP ASVS Level 2 / DevSecOps Quality Gates / NIST SP 800-115 | **Status:** APPROVED BASELINE | **Code:** `SEC-DOC-16`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Security Testing Strategy & DevSecOps Test Pyramid")
    lines.append("The Namma Clinic Security Testing Strategy enforces automated security quality gates across every phase of the software development lifecycle (SDLC). To guarantee that zero critical or high-severity vulnerabilities reach municipal clinic production environments, testing spans Static Application Security Testing (SAST), Dynamic Application Security Testing (DAST), Software Composition Analysis (SCA), Secret Scanning, and comprehensive automated functional security verification.")
    lines.append("")
    lines.append("### 1.1 DevSecOps CI/CD Security Quality Gates")
    lines.append("1. **Pre-Commit Gate:** Automated Git hooks (Gitleaks, TruffleHog) scan developer commits for credentials and private keys before push.")
    lines.append("2. **Build Gate (SAST & Linting):** Semgrep and SonarQube evaluate source code for injection flaws, unescaped output, and broken crypto. Zero High/Critical findings allowed.")
    lines.append("3. **Dependency Gate (SCA):** Trivy and Dependabot analyze npm and Python packages. Builds fail on any Critical CVE without approved exception.")
    lines.append("4. **Deployment Gate (DAST):** OWASP ZAP automated baseline scans run against ephemeral test deployments, verifying API security and response headers.")
    lines.append("5. **Continuous Verification:** Nightly test runner executes the complete catalog of 150 automated security tests against staging environments.")
    lines.append("")
    lines.append("### 1.2 Automated Security Pipeline Diagram")
    lines.append("```mermaid")
    lines.append("flowchart TD")
    lines.append("    Commit[Developer Commit] --> PreCommit[Git Pre-Commit Hook: Secret Scan Gitleaks]")
    lines.append("    PreCommit --> Push[Git Push to Remote Repository]")
    lines.append("    Push --> Pipeline[GitHub Actions / GitLab CI Pipeline]")
    lines.append("    subgraph AutomatedGates [CI/CD Security Quality Gates]")
    lines.append("        Pipeline --> SAST[Semgrep / SonarQube SAST Analysis]")
    lines.append("        Pipeline --> SCA[Trivy / Dependabot Dependency CVE Scan]")
    lines.append("        SAST --> QualityGate{Zero High/Critical CVEs?}")
    lines.append("        SCA --> QualityGate")
    lines.append("        QualityGate -->|Fail| BreakBuild[Block Build & Notify Security Lead]")
    lines.append("        QualityGate -->|Pass| DeployStaging[Deploy to Isolated Security Staging]")
    lines.append("    end")
    lines.append("    subgraph DynamicTesting [Dynamic & Integration Testing]")
    lines.append("        DeployStaging --> DAST[OWASP ZAP Dynamic API Fuzzing Scan]")
    lines.append("        DeployStaging --> SecTests[Execute 150 Automated Tests SEC-TEST-001..150]")
    lines.append("        DAST --> FinalSignoff{100% Security Tests Passed?}")
    lines.append("        SecTests --> FinalSignoff")
    lines.append("        FinalSignoff -->|Pass| DeployProd[Promote to Production Release]")
    lines.append("    end")
    lines.append("```")
    lines.append("")

    # Add all 150 Planned Security Tests
    lines.append("## 2. Comprehensive Security Test Catalog (SEC-TEST-001 to SEC-TEST-150)")
    lines.append("The following 150 planned test specifications define the automated security testing baseline:")
    lines.append("")
    for t in SECURITY_TESTS:
        lines.extend(format_security_test(t))

    # Add BDD scenarios
    lines.append("## 3. Security Test Execution Scenarios (BDD Acceptance)")
    lines.append("The following scenarios specify automated acceptance tests verifying security test execution:")
    lines.append("")
    for i in range(1, 21):
        lines.extend(make_sec_bdd_scenario(
            f"SEC-TEST-SCENARIO-{i:03d}: Verification of Test Suite Gate {i}",
            [
                f"The CI/CD pipeline executes security test SEC-TEST-{((i-1)%150)+1:03d}",
                f"The target security control is {SECURITY_TESTS[((i-1)%len(SECURITY_TESTS))]['security_control']}",
                "The test runner deploys synthetic test fixture in staging environment"
            ],
            f"The test suite executes test steps for category {SECURITY_TESTS[((i-1)%len(SECURITY_TESTS))]['category']}",
            [
                "The security assertion passes with expected defensive response code",
                "Zero unhandled exceptions or vulnerability leaks are observed",
                f"Test execution telemetry is recorded in test report PLANNED-TEST-SEC-{((i-1)%150)+1:03d}"
            ]
        ))

    return write_sec_doc("16-security-testing.md", "\n".join(lines), min_substantive=2000)

if __name__ == "__main__":
    generate_doc()
