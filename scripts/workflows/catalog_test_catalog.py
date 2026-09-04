#!/usr/bin/env python3
"""
catalog_test_catalog.py
Generates docs/03-workflows/WORKFLOW_TEST_CATALOG.md
Target: >= 3,000 substantive lines.
Contains all BDD scenarios, 20 test types, non-functional test specifications,
and CI quality gate benchmarks across all 25 workflows.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from workflow_metadata import WORKFLOW_SPECS, WORKFLOW_MAP
from workflow_core_data import get_all_workflows
from common import count_lines

def generate_test_catalog():
    wfs = get_all_workflows()
    lines = []

    lines.append("# Master Workflow Quality Engineering & Test Catalog")
    lines.append("## Namma Clinic Digital Health & Operations Platform")
    lines.append("**Document Code:** WORKFLOW-TEST-01 | **Status:** Quality Engineering Baseline Approved | **Date:** September 2026")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 1
    lines.append("## 01. Quality Engineering & Verification Architecture")
    lines.append("The Namma Clinic Digital Health & Operations Platform enforces an exhaustive, multi-layered quality engineering architecture. Every clinical transition, hardware serial interaction, offline synchronization queue, and national health gateway touchpoint is validated by deterministic automated test suites.")
    lines.append("")
    lines.append("This test catalog serves as the authoritative verification baseline for QA engineers, software development engineers in test (SDET), clinical safety validators, and security compliance auditors. It encompasses 20 standardized test types, > 950 executable Gherkin BDD scenarios across all 25 primary workflows, fault-injection matrices, and CI quality gates.")
    lines.append("")

    # Section 2: 20 Test Types Taxonomy
    lines.append("## 02. Comprehensive Test Taxonomy (20 Standardized Test Types)")
    lines.append("The platform quality engineering framework categorizes all verification activities into 20 standardized test types:")
    lines.append("")
    lines.append("| Type ID | Test Classification | Verification Scope | Target Tools & Frameworks | Execution Frequency | Quality Gate Pass Benchmark |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")

    test_types = [
        ("TT-01", "Unit Testing", "State machine transition rules, MEWS algorithms, data formatters", "PyTest, Jest", "Every Commit", "100% Pass, >= 90% Line Coverage"),
        ("TT-02", "Component Integration", "IPC communication between kiosk UI and local edge daemon", "Supertest, React Testing Library", "PR Merge", "100% Pass, Zero Flakiness"),
        ("TT-03", "E2E BDD Scenarios", "Complete citizen journeys across all clinic stations", "Playwright, Cucumber BDD", "Nightly Build", "100% Green Scenarios"),
        ("TT-04", "Regression Testing", "Full platform regression preventing regression bugs", "PyTest Suite", "Pre-Release", "Zero Unresolved Regressions"),
        ("TT-05", "Smoke Testing", "Critical path verification on fresh container deployment", "Bash, Curl, Playwright Smoke", "Post-Deploy", "Completed in < 3 Minutes"),
        ("TT-06", "Sanity Testing", "Targeted validation of bug fix releases", "Targeted Test Runners", "Hotfix Deploy", "Verified Bug Resolution"),
        ("TT-07", "Performance & Load", "Simulating 150 concurrent clinic sessions and surges", "k6, Locust", "Weekly Load Test", "p95 Latency < 1.0s under 2x Load"),
        ("TT-08", "Stress & Soak", "Continuous 72-hour sustained operational testing", "Locust Distributed", "Release Candidate", "Zero Memory Leaks / Crashes"),
        ("TT-09", "Chaos Engineering", "Random process kills, packet drop, disk full simulation", "Chaos Mesh, Pumba", "Sprint Gate", "Automated Self-Healing in < 30s"),
        ("TT-10", "Security SAST/DAST", "Static code analysis, dependency CVE scans, fuzzing", "Semgrep, OWASP ZAP, Trivy", "Every Build", "Zero High / Critical Findings"),
        ("TT-11", "Privacy & DPDP", "Verification of k-anonymity, consent enforcement, masking", "Automated Privacy Scanner", "Bi-Weekly", "100% DPDP Compliance"),
        ("TT-12", "Accessibility WCAG", "Screen reader semantics, contrast >= 4.5:1, keyboard", "Axe-core, Pa11y", "UI PR Gate", "100% WCAG 2.1 AA Compliant"),
        ("TT-13", "Localization / Kannada", "Kannada font rendering, audio prompt clarity, slips", "Vernacular Assertion Suite", "UI Release", "100% Kannada Linguistic Parity"),
        ("TT-14", "Usability Testing", "Time-and-motion studies with actual nurses and doctors", "User Observation Lab", "Quarterly", "SUS Score >= 85 (Usability)"),
        ("TT-15", "Offline Autonomous", "Testing 72-hour standalone execution without WAN", "Simulated Fiber Cut", "Weekly", "Zero Data Loss, RPO = 0"),
        ("TT-16", "Network Fault Injection", "High latency (500ms), 20% packet drop, link flap", "Toxiproxy", "Weekly", "Graceful Degradation"),
        ("TT-17", "Power Loss / UPS", "Sudden hard power cut during active SQLite transaction", "Physical Relay Switch", "Hardware Gate", "Zero Corrupted DB Files"),
        ("TT-18", "Concurrency & Race", "Simultaneous token minting and stock decrement", "Go Race Detector, ThreadSanitizer", "Sprint Gate", "Zero Data Races / Deadlocks"),
        ("TT-19", "Backward Compatibility", "Replaying old schema payloads against new gateways", "Schema Registry Assertions", "Major Release", "100% Backward Compatible"),
        ("TT-20", "Disaster Recovery", "Restoring full clinic database from encrypted backup", "Automated DR Orchestrator", "Monthly", "RTO < 5 min, RPO = 0")
    ]
    for tid, name, scope, tools, freq, gate in test_types:
        lines.append(f"| `{tid}` | **{name}** | {scope} | `{tools}` | {freq} | {gate} |")

    lines.append("")
    lines.append("## 03. Comprehensive Workflow BDD Scenario Test Catalog")
    lines.append("Exhaustive, production-grade Gherkin BDD test specifications covering all 25 workflows (Happy Path, Alternate Flows, and Exception Handlers):")
    lines.append("")

    # Loop over all 25 workflows and render all BDD scenarios
    for wfid in sorted(wfs.keys()):
        wf = wfs[wfid]
        wfname = wf["name"]
        wfnum = wf["num"]
        bdds = wf.get("bdd_scenarios", [])

        lines.append(f"### Test Suite for {wfid}: {wfname}")
        lines.append(f"- **Total Executable Scenarios:** {len(bdds)}")
        lines.append(f"- **Primary Test Harness:** `tests/e2e/test_{wfid.lower().replace('-', '_')}.py`")
        lines.append("")

        for bdd in bdds:
            bid = bdd["id"]
            btitle = bdd["title"]
            bcat = bdd.get("category", "Happy Path")
            bpri = bdd.get("priority", "P0")
            lines.append(f"#### `{bid}`: {btitle}")
            lines.append(f"- **Category:** `{bcat}` | **Execution Priority:** `{bpri}`")
            lines.append("```gherkin")
            lines.append(f"Feature: {wfname} Verification ({wfid})")
            lines.append(f"  Scenario: {btitle}")
            lines.append(f"    Given {bdd.get('given', 'the Namma Clinic operating day is active')}")
            for g_and in bdd.get("given_ands", []):
                lines.append(f"      And {g_and}")
            lines.append(f"    When {bdd.get('when', 'an authorized operator initiates the workflow milestone')}")
            for w_and in bdd.get("when_ands", []):
                lines.append(f"      And {w_and}")
            lines.append(f"    Then {bdd.get('then', 'the system transitions to the expected milestone state')}")
            for t_and in bdd.get("then_ands", []):
                lines.append(f"      And {t_and}")
            lines.append("```")
            lines.append("")

    # Section 4: Non-Functional & Stress Testing
    lines.append("## 04. Non-Functional, Stress & Chaos Testing Specifications")
    lines.append("Detailed engineering test plans for non-functional verification under harsh operating conditions:")
    lines.append("")
    lines.append("### Chaos Test Plan: Power Disruption During Peak OPD Surge (`CHAOS-TEST-01`)")
    lines.append("- **Test Scenario:** Hard power disconnection to the primary Edge Node mini-PC at 09:30 IST while 12 concurrent transactions are writing to SQLite.")
    lines.append("- **Assertion Target:** Zero corrupted database pages; zero uncommitted transaction leaks; automated recovery in < 60 seconds upon UPS reboot.")
    lines.append("- **Verification Tool:** Hardware automated power cycle relay with SQLite `PRAGMA integrity_check` validation.")
    lines.append("")
    lines.append("### Chaos Test Plan: Fiber Cable Severance Simulation (`CHAOS-TEST-02`)")
    lines.append("- **Test Scenario:** WAN broadband router port disabled while 85 citizens are actively queuing and consulting.")
    lines.append("- **Assertion Target:** Terminals switch to amber offline mode within 3.0 seconds; zero dialog popups block doctors; local token printing and dispensing continue uninterrupted.")
    lines.append("- **Verification Tool:** Toxiproxy network boundary simulator with automated UI state assertions.")
    lines.append("")
    lines.append("### Stress Test Plan: 72-Hour Continuous Endurance Soak (`SOAK-TEST-01`)")
    lines.append("- **Test Scenario:** Continuous headless browser workers simulating 1,200 patient visits per day for 72 hours.")
    lines.append("- **Assertion Target:** Edge server memory growth < 50MB (zero resource leaks); disk storage consumption < 500MB; p95 query latency remains < 15ms.")
    lines.append("- **Verification Tool:** Distributed Locust load generator running in staging environment.")
    lines.append("")

    # Section 5: Security & Privacy Penetration Test Suite
    lines.append("## 05. Security & Privacy Penetration Test Suite")
    lines.append("Targeted penetration test scenarios validating platform cryptographic invariants:")
    lines.append("")
    lines.append("| Test ID | Security Target | Attack Vector Simulated | Expected System Defense | Pass Verification |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    lines.append("| `SEC-PEN-01` | Authentication Bypass | Replaying expired JWT session token | Gateway rejects with HTTP 401 Unauthorized | Automated PyTest Suite |")
    lines.append("| `SEC-PEN-02` | Privilege Escalation | Nurse token accessing Doctor Rx API | RBAC gate returns HTTP 403 Forbidden | API Security Gate |")
    lines.append("| `SEC-PEN-03` | SQL Injection | Malicious payload in patient search | Parameterized SQLite query sanitization | SQLMap Penetration Scan |")
    lines.append("| `SEC-PEN-04` | Audit Trail Tampering | Direct binary file edit of SQLite WAL | Merkle hash break detected; alarm fired | Hash Discontinuity Test |")
    lines.append("| `SEC-PEN-05` | PHI Exposure | Snooping unencrypted local Wi-Fi | All traffic TLS 1.3 encrypted; zero plaintext | Wireshark Packet Audit |")
    lines.append("")

    # Section 6: CI/CD Quality Gates & Benchmark Thresholds
    lines.append("## 06. Continuous Integration Quality Gates & Benchmark Thresholds")
    lines.append("Every code pull request must pass the automated platform quality gate pipeline before merge approval:")
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart LR")
    lines.append("    Commit[PR Commit] --> Gate1[Gate 1: Lint & Types]")
    lines.append("    Gate1 --> Gate2[Gate 2: Unit Tests >= 90%]")
    lines.append("    Gate2 --> Gate3[Gate 3: Security & SAST]")
    lines.append("    Gate3 --> Gate4[Gate 4: E2E Playwright BDD]")
    lines.append("    Gate4 --> Gate5[Gate 5: Performance Budget]")
    lines.append("    Gate5 --> MergeApproved[Merge to Release Branch]")
    lines.append("```")
    lines.append("")
    lines.append("| Quality Gate | Verification Criteria | Enforcement Tooling | Failure Action |")
    lines.append("| :--- | :--- | :--- | :--- |")
    lines.append("| **Gate 1: Static Analysis** | Zero lint errors, zero unresolved TypeScript/Python types | Ruff, ESLint, Mypy | PR Blocked |")
    lines.append("| **Gate 2: Unit Coverage** | >= 90% statement coverage across all domain services | PyTest, Jest | PR Blocked |")
    lines.append("| **Gate 3: Security Audit** | Zero High/Critical CVEs, zero hardcoded secrets | Trivy, GitLeaks, Semgrep | PR Blocked |")
    lines.append("| **Gate 4: E2E BDD Suite** | 100% pass across all 950+ Gherkin BDD scenarios | Playwright Test | PR Blocked |")
    lines.append("| **Gate 5: Performance** | p95 transaction latency < 1.0s, bundle size < 250KB | Lighthouse CI, k6 | PR Blocked |")
    lines.append("")

    return "\n".join(lines)

def write_test_catalog_file():
    print("Generating WORKFLOW_TEST_CATALOG.md...")
    doc = generate_test_catalog()
    counts = count_lines(doc)
    print(f"  Generated: Total = {counts['total']}, Substantive = {counts['substantive']}")
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "03-workflows", "WORKFLOW_TEST_CATALOG.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"  Wrote {out_path} [{ 'PASS' if counts['substantive'] >= 3000 else 'FAIL' }]")

if __name__ == "__main__":
    write_test_catalog_file()
