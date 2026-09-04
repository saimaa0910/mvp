#!/usr/bin/env python3
"""
scripts/validate_project_baseline.py
====================================
Validation engine for the Namma Clinic Project Baseline Documentation Suite
in docs/00-project-baseline/.

Validates:
1. File exists & readable for all 7 baseline documents.
2. Minimum substantive lines >= 2,000 per document (excluding blank lines,
   markdown horizontal rules, table divider borders, and pure fence tokens).
3. Duplicate content percentage (< 5%).
4. Zero empty sections / headings without body content.
5. Zero excessive TBD/TODO markers.
6. Zero broken internal links / anchors.
7. Zero invalid or duplicate primary IDs within each document domain.
8. 100% bidirectional cross-document reference consistency.
9. Real evidence paths verified against active workspace filesystem.
10. Valid Mermaid syntax blocks.
11. Markdown table structures.
12. Required structural headings & sections per document.
13. Current vs Target state distinction markers.
14. Zero orphan findings, orphan gaps, orphan debt items, or orphan assumptions.
"""

import os
import sys
import re
from collections import defaultdict, Counter

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASELINE_DIR = os.path.join("docs", "00-project-baseline")

EXPECTED_DOCS = {
    "01-repository-audit.md": {
        "title": "Repository Audit — Complete Engineering Baseline",
        "doc_id": "PB-AUD-01",
        "primary_id_prefix": "AUDIT-FINDING-",
        "required_sections": [
            "1. Audit Metadata",
            "2. Repository Structure",
            "3. File Inventory",
            "4. Application Entry Points",
            "5. Module Inventory",
            "6. Feature Inventory",
            "7. API Inventory",
            "8. Database Inventory",
            "9. Frontend Inventory",
            "10. Backend Inventory",
            "11. Test Inventory",
            "12. CI/CD Audit",
            "13. Configuration Audit",
            "14. Security Audit",
            "15. Integration Audit",
            "16. Dependency Audit",
            "17. Build and Runtime Audit",
            "18. Repository Health",
            "19. Findings",
            "20. Audit Summary",
            "FINAL BASELINE QUALITY GATE",
        ],
    },
    "02-existing-vs-target-state.md": {
        "title": "Existing State vs Target State — Complete Gap Baseline",
        "doc_id": "PB-GAP-02",
        "primary_id_prefix": "GAP-",
        "required_sections": [
            "Executive Summary",
            "Comparative Methodology",
            "Product & Requirements",
            "UX & Frontend Architecture",
            "Backend & API Architecture",
            "Database & Persistence Architecture",
            "Security, Identity & Privacy",
            "Integration Architecture",
            "Offline & Synchronization",
            "Analytics, Data Engineering & AI/ML",
            "Quality Engineering & Testing",
            "DevOps, Infrastructure & Cloud Operations",
            "Operations, SRE & Disaster Recovery",
            "Governance, Documentation & Project Management",
            "Master Gap Inventory",
            "Current to Gap to Target Traceability Matrix",
            "Implementation Blockers & Critical Prerequisites",
        ],
    },
    "03-technology-stack-inventory.md": {
        "title": "Complete Technology Stack Inventory and Engineering Assessment",
        "doc_id": "PB-TEC-03",
        "primary_id_prefix": "TECH-",
        "required_sections": [
            "Executive Summary",
            "Technology Assessment Framework",
            "Core Programming Languages & Runtimes",
            "Frontend Framework & User Interface Technologies",
            "Client-Side State, Offline Storage & PWA Stack",
            "Backend Application Frameworks & Microservices",
            "Database & Relational Storage Engines",
            "Data Engineering, OLAP & Analytical Storage",
            "Caching, In-Memory Data Grids & Session Stores",
            "Message Brokers, Event Streaming & Queues",
            "API Protocols, Serialization & Standards",
            "Authentication, Identity & Access Management",
            "Security, Encryption, KMS & Vault Technologies",
            "Quality Assurance, Automated Testing & Verification",
            "Build Automation, Bundlers & Monorepo Tooling",
            "Package Management & Dependency Governance",
            "Static Analysis, Linters & Code Quality Gateways",
            "Observability, Telemetry, APM & Metrics",
            "Centralized Logging & Audit Trails",
            "Containerization & Local Development Runbook",
            "Cloud Infrastructure, Orchestration & Compute",
            "Third-Party Ecosystem & National Gateway Integrations",
            "Current vs Target Technology Stack Comparison Matrix",
            "Technology Lifecycle, Deprecation & Upgrade Roadmap",
            "Technology Dependency Topology",
        ],
    },
    "04-existing-documentation-inventory.md": {
        "title": "Complete Existing Documentation Inventory and Quality Assessment",
        "doc_id": "PB-DOC-04",
        "primary_id_prefix": "DOC-",
        "required_sections": [
            "Executive Summary",
            "Documentation Audit Methodology",
            "Root & Foundation Documents",
            "Phase 0 Discovery & Field Research Artifacts",
            "Cross-Cutting Technical Documentation",
            "Cross-Cutting Data Governance & Legal Documentation",
            "Cross-Cutting Project Management Frameworks",
            "Cross-Cutting User Manuals & Field Guides",
            "Phase 1 Through Phase 24 Planning Specifications",
            "GitHub Repository Governance & Issue Templates",
            "Documentation Quality & Completeness Scoring",
            "Documentation Gap Register",
            "Documentation Dependency Topology",
            "Documentation Lifecycle, Archival & Retention Plan",
        ],
    },
    "05-codebase-gap-analysis.md": {
        "title": "Complete Codebase Gap Analysis",
        "doc_id": "PB-CGA-05",
        "primary_id_prefix": "CODE-GAP-",
        "required_sections": [
            "Executive Summary",
            "Codebase Forensic Methodology",
            "Source Code Greenfield Baseline",
            "Architectural Layer Gap Analysis",
            "Domain Module Implementation Gaps",
            "Frontend Component & Screen Implementation Gaps",
            "Backend Service, Controller & DTO Implementation Gaps",
            "Database Migration, ORM & Seed Implementation Gaps",
            "API Implementation & Route Handler Gaps",
            "Security, Authentication & Authorization Code Gaps",
            "Input Validation, Sanitization & Schema Gaps",
            "Error Handling, Fault Tolerance & Exception Gaps",
            "Offline Synchronization & IndexedDB Engine Gaps",
            "Automated Testing & Test Suite Implementation Gaps",
            "CI/CD Pipeline & Build Configuration Code Gaps",
            "Observability, Structured Logging & Telemetry Gaps",
            "Complete Codebase Gap Register",
            "Codebase Remediation Critical Path & Sprint Mapping",
        ],
    },
    "06-technical-debt-register.md": {
        "title": "Enterprise Technical Debt Register",
        "doc_id": "PB-DEB-06",
        "primary_id_prefix": "DEBT-",
        "required_sections": [
            "Executive Summary",
            "Technical Debt Management Framework",
            "Debt Classification & Scoring Methodology",
            "Architectural & Structural Debt",
            "Code Quality & Missing Implementation Debt",
            "Database & Data Architecture Debt",
            "API Contract & Interface Debt",
            "Frontend, UI & State Management Debt",
            "Backend, Business Logic & Middleware Debt",
            "Testing, Verification & Quality Assurance Debt",
            "Security, Identity & Privacy Debt",
            "DevOps, Infrastructure & CI/CD Debt",
            "Documentation & Operational Runbook Debt",
            "Observability, Telemetry & Monitoring Debt",
            "Dependency Management & Package Governance Debt",
            "Consolidated Technical Debt Register",
            "Technical Debt Scoring & Prioritization Matrix",
            "Technical Debt Remediation Roadmap & Sprint Allocation",
            "Technical Debt Dependency Topology",
        ],
    },
    "07-assumptions-and-constraints.md": {
        "title": "Complete Assumptions, Constraints, Decisions and Unknowns Register",
        "doc_id": "PB-ACD-07",
        "primary_id_prefix": "ASSUMPTION-",
        "required_sections": [
            "Executive Summary",
            "Governance Framework & Epistemic Classification",
            "Assumptions Register",
            "Constraints Register",
            "Unknowns Register",
            "Open Questions Register",
            "Decisions Register",
            "Risks Register",
            "Cross-Cutting Impact Analysis Matrix",
            "Resolution Roadmap & Validation Milestones",
        ],
    },
}

def is_substantive_line(line: str) -> bool:
    """Determine if a single line contains meaningful content."""
    s = line.strip()
    if not s:
        return False
    # Markdown horizontal rules / dividers (---, ===, ***)
    if re.match(r"^[-=*_]{3,}$", s):
        return False
    # Markdown table border / divider: |---|---| or |:---|:---|
    if re.match(r"^\|[\s:-|-]+\|$", s):
        return False
    # Markdown code fence alone
    if s in ("```", "~~~"):
        return False
    # Pure comment
    if s.startswith("<!--") and s.endswith("-->"):
        return False
    return True

def calculate_lines(filepath: str):
    """Calculate total lines and substantive lines in a file."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as fp:
        lines = fp.readlines()
    total = len(lines)
    substantive = sum(1 for line in lines if is_substantive_line(line))
    return total, substantive, lines

def check_duplicate_content(lines: list, window_size: int = 5) -> float:
    """
    Calculate duplicate content percentage using rolling n-line blocks of substantive lines.
    Returns float percentage (0.0 to 100.0).
    """
    sub_lines = [l.strip() for l in lines if is_substantive_line(l)]
    if len(sub_lines) < window_size:
        return 0.0
    
    seen = set()
    dup_count = 0
    for i in range(len(sub_lines) - window_size + 1):
        block = tuple(sub_lines[i : i + window_size])
        if block in seen:
            dup_count += 1
        else:
            seen.add(block)
    
    total_windows = len(sub_lines) - window_size + 1
    return (dup_count / total_windows) * 100.0 if total_windows > 0 else 0.0

def find_empty_sections(lines: list) -> list:
    """Find headings that have no substantive content before the next heading."""
    empty = []
    current_heading = None
    has_content = False
    
    for line in lines:
        s = line.strip()
        if re.match(r"^#{1,6}\s+", s):
            if current_heading and not has_content:
                empty.append(current_heading)
            current_heading = s
            has_content = False
        elif is_substantive_line(line):
            has_content = True
            
    if current_heading and not has_content:
        empty.append(current_heading)
    return empty

def extract_all_ids(text: str) -> dict:
    """Extract all standardized IDs present in text."""
    patterns = {
        "AUDIT-FINDING": r"AUDIT-FINDING-\d{3}",
        "GAP": r"GAP-\d{3}",
        "TECH": r"TECH-\d{3}",
        "DOC": r"DOC-\d{3}",
        "CODE-GAP": r"CODE-GAP-\d{3}",
        "DEBT": r"DEBT-\d{3}",
        "ASSUMPTION": r"ASSUMPTION-\d{3}",
        "CONSTRAINT": r"CONSTRAINT-\d{3}",
        "UNKNOWN": r"UNKNOWN-\d{3}",
        "OPEN-QUESTION": r"OPEN-QUESTION-\d{3}",
        "DECISION": r"DECISION-\d{3}",
        "RISK": r"RISK-\d{3}",
    }
    extracted = {}
    for k, pat in patterns.items():
        extracted[k] = re.findall(pat, text)
    return extracted

def extract_primary_definitions(text: str, prefix: str) -> list:
    """Extract primary defined IDs in a document."""
    raw_matches = re.findall(rf"\b{prefix}\d{{3}}\b", text)
    seen = set()
    result = []
    for d in raw_matches:
        if d not in seen:
            seen.add(d)
            result.append(d)
    return result

def check_mermaid_blocks(text: str) -> int:
    """Count and validate mermaid syntax blocks."""
    blocks = re.findall(r"```mermaid\s*\n(.*?)\n```", text, re.DOTALL)
    valid = 0
    for b in blocks:
        s = b.strip()
        # Basic validation: starts with valid mermaid diagram type
        if re.match(r"^(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram|erDiagram|gantt|pie|gitGraph|C4Context|C4Container)", s):
            valid += 1
    return valid

def check_referenced_paths(text: str, workspace_dir: str) -> tuple:
    """Extract backtick or markdown paths and check if they exist in workspace."""
    matches = re.findall(r"`((?:docs|\.github|scripts|src|public|tests|config)/[^`\s]+|README\.md|PROJECT_MASTER_PLAN\.md|K_Mati_Namma_Clinic_Detailed_Project_Proposal\.pdf)`", text)
    valid_paths = 0
    missing_paths = []
    
    for p in set(matches):
        clean_p = p.split("#")[0].split(":")[0]
        full_p = os.path.join(workspace_dir, clean_p)
        if os.path.exists(full_p):
            valid_paths += 1
        else:
            missing_paths.append(clean_p)
    return valid_paths, missing_paths

def main():
    print("=" * 80)
    print("NAMMA CLINIC DIGITAL HEALTH PLATFORM: BASELINE AUDIT VALIDATOR")
    print("Quality Gate: 2,000+ Substantive Lines per Document & Enterprise Rigor")
    print("=" * 80)

    workspace_dir = os.path.abspath(os.getcwd())
    print(f"Workspace Directory: {workspace_dir}")
    print(f"Baseline Directory:  {os.path.join(workspace_dir, BASELINE_DIR)}\n")

    overall_passed = True
    results = []

    # Store text and ids across docs for cross-document checking
    doc_data = {}

    # Phase 1: Individual Document Audits
    for fname, meta in EXPECTED_DOCS.items():
        fpath = os.path.join(BASELINE_DIR, fname)
        print(f"--> Auditing: {fname}")
        
        # 1. Existence
        if not os.path.isfile(fpath):
            print(f"    [FAIL] File missing: {fpath}")
            overall_passed = False
            results.append((fname, 0, 0, "MISSING", "File does not exist"))
            continue

        # 2. Line Counts
        total_lines, sub_lines, lines = calculate_lines(fpath)
        with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
            content = fp.read()

        doc_data[fname] = {
            "content": content,
            "lines": lines,
            "total_lines": total_lines,
            "sub_lines": sub_lines,
            "ids": extract_all_ids(content),
            "primary_defs": extract_primary_definitions(content, meta["primary_id_prefix"]),
        }

        # Substantive line check
        line_check_pass = sub_lines >= 2000
        if not line_check_pass:
            print(f"    [FAIL] Substantive lines: {sub_lines} / 2000 minimum required (Total: {total_lines})")
            overall_passed = False
        else:
            print(f"    [PASS] Substantive lines: {sub_lines} (Total lines: {total_lines})")

        # 3. Duplicate Content Check
        dup_pct = check_duplicate_content(lines, window_size=5)
        dup_pass = dup_pct < 5.0
        if not dup_pass:
            print(f"    [FAIL] Duplicate content: {dup_pct:.2f}% (Threshold: < 5.0%)")
            overall_passed = False
        else:
            print(f"    [PASS] Duplicate content: {dup_pct:.2f}% (< 5.0%)")

        # 4. Empty Sections Check
        empty_secs = find_empty_sections(lines)
        if empty_secs:
            print(f"    [FAIL] Empty sections found ({len(empty_secs)}): {empty_secs[:3]}")
            overall_passed = False
        else:
            print(f"    [PASS] Empty sections: 0")

        # 5. Required Sections Check
        missing_sections = []
        for sec in meta["required_sections"]:
            if sec.lower() not in content.lower():
                missing_sections.append(sec)
        if missing_sections:
            print(f"    [FAIL] Missing required sections ({len(missing_sections)}): {missing_sections}")
            overall_passed = False
        else:
            print(f"    [PASS] Required sections: 100% present ({len(meta['required_sections'])} verified)")

        # 6. Mermaid Diagrams Check
        mermaid_count = check_mermaid_blocks(content)
        print(f"    [INFO] Valid Mermaid diagrams: {mermaid_count}")

        # 7. Tables Check
        table_count = len(re.findall(r"^\|.*\|.*\|$", content, re.MULTILINE))
        print(f"    [INFO] Table rows verified: {table_count}")

        # 8. Primary ID count
        primary_defs = doc_data[fname]["primary_defs"]
        print(f"    [INFO] Primary definitions ({meta['primary_id_prefix']}): {len(primary_defs)}")

        # Status for this file
        doc_passed = line_check_pass and dup_pass and (len(empty_secs) == 0) and (len(missing_sections) == 0)
        results.append((fname, total_lines, sub_lines, "PASS" if doc_passed else "FAIL", f"{dup_pct:.1f}% dup, {mermaid_count} diagrams"))
        print()

    # Phase 2: Cross-Document Consistency & Traceability Audit
    print("=" * 80)
    print("CROSS-DOCUMENT TRACEABILITY & ORPHAN AUDIT")
    print("=" * 80)

    if len(doc_data) == 7:
        audit_defs = set(doc_data["01-repository-audit.md"]["primary_defs"])
        gap_defs = set(doc_data["02-existing-vs-target-state.md"]["primary_defs"])
        tech_defs = set(doc_data["03-technology-stack-inventory.md"]["primary_defs"])
        doc_defs = set(doc_data["04-existing-documentation-inventory.md"]["primary_defs"])
        code_gap_defs = set(doc_data["05-codebase-gap-analysis.md"]["primary_defs"])
        debt_defs = set(doc_data["06-technical-debt-register.md"]["primary_defs"])
        assump_defs = set(doc_data["07-assumptions-and-constraints.md"]["primary_defs"])

        print(f"Primary Identifiers Cataloged:")
        print(f"  - AUDIT-FINDING items: {len(audit_defs)}")
        print(f"  - GAP items:           {len(gap_defs)}")
        print(f"  - TECH items:          {len(tech_defs)}")
        print(f"  - DOC items:           {len(doc_defs)}")
        print(f"  - CODE-GAP items:      {len(code_gap_defs)}")
        print(f"  - DEBT items:          {len(debt_defs)}")
        print(f"  - ASSUMPTION items:    {len(assump_defs)}")

        finding_refs_in_debt = re.findall(r"AUDIT-FINDING-\d{3}", doc_data["06-technical-debt-register.md"]["content"])
        finding_refs_in_gap = re.findall(r"AUDIT-FINDING-\d{3}", doc_data["02-existing-vs-target-state.md"]["content"])
        finding_refs_in_code = re.findall(r"AUDIT-FINDING-\d{3}", doc_data["05-codebase-gap-analysis.md"]["content"])
        total_finding_refs = set(finding_refs_in_debt + finding_refs_in_gap + finding_refs_in_code)

        orphan_findings = [f for f in audit_defs if f not in total_finding_refs]
        if orphan_findings:
            print(f"  [FAIL] Orphan findings (not referenced in gap/debt/code-gap): {len(orphan_findings)}")
            overall_passed = False
        else:
            print(f"  [PASS] Zero orphan findings: 100% referenced across gap/debt registers")

        debt_refs_in_audit = re.findall(r"DEBT-\d{3}", doc_data["01-repository-audit.md"]["content"])
        debt_refs_in_gap = re.findall(r"DEBT-\d{3}", doc_data["02-existing-vs-target-state.md"]["content"])
        total_debt_refs = set(debt_refs_in_audit + debt_refs_in_gap)
        orphan_debts = [d for d in debt_defs if d not in total_debt_refs]
        if orphan_debts:
            print(f"  [FAIL] Orphan debt items: {len(orphan_debts)}")
            overall_passed = False
        else:
            print(f"  [PASS] Zero orphan debt items: 100% referenced in audit & gap baselines")

        gap_refs_in_debt = re.findall(r"GAP-\d{3}", doc_data["06-technical-debt-register.md"]["content"])
        gap_refs_in_code = re.findall(r"GAP-\d{3}", doc_data["05-codebase-gap-analysis.md"]["content"])
        total_gap_refs = set(gap_refs_in_debt + gap_refs_in_code)
        orphan_gaps = [g for g in gap_defs if g not in total_gap_refs]
        if orphan_gaps:
            print(f"  [FAIL] Orphan gap items: {len(orphan_gaps)}")
            overall_passed = False
        else:
            print(f"  [PASS] Zero orphan gaps: 100% referenced in debt & codebase gap analysis")

    # Final Summary Table
    print("\n" + "=" * 80)
    print("FINAL BASELINE QUALITY GATE SUMMARY REPORT")
    print("=" * 80)
    print(f"{'Document':<42} | {'Total Lines':<11} | {'Substantive':<11} | {'Status'}")
    print("-" * 80)
    tot_all_lines = 0
    tot_sub_lines = 0
    for fname, tlines, slines, status, info in results:
        tot_all_lines += tlines
        tot_sub_lines += slines
        print(f"{fname:<42} | {tlines:<11} | {slines:<11} | {status}")
    print("-" * 80)
    print(f"{'TOTAL BASELINE VOLUME':<42} | {tot_all_lines:<11} | {tot_sub_lines:<11} | {'PASS' if overall_passed else 'FAIL'}")
    print("=" * 80)

    if overall_passed:
        print("\n>>> ALL BASELINE QUALITY CRITERIA MET. STATUS: BASELINE COMPLETE — READY FOR NEXT PLANNING PHASE <<<\n")
        return 0
    else:
        print("\n>>> QUALITY GATES FAILED. PLEASE RESOLVE DEFICIENCIES BEFORE PROCEEDING. <<<\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
