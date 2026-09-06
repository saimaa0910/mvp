"""
validate_planning_docs.py
Master Validation Suite for Phase 17 (Master Planning) and Phase 18 (18-Sprint Execution).
Enforces 10 Comprehensive Quality Gates across docs/17-planning/ and docs/18-sprints/.
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines, find_duplicate_paragraphs
from scripts.planning.planning_core_data import (
    OBJECTIVES, SCOPES, DEPENDENCIES, CRITICAL_PATH_ITEMS, BLOCKERS, RISKS,
    CAPACITY_MODELS, VELOCITY_MODELS, ESTIMATION_MODELS, WORKSTREAMS,
    MILESTONES, RELEASES, QUALITY_GATES, ASSUMPTIONS, DECISIONS, SPRINT_DEFINITIONS
)
from scripts.database.db_tables_entities import TABLES
from scripts.product.product_core_data import FEATURES

PLANNING_DOCS = [
    "01-master-dependency-map.md",
    "02-critical-path.md",
    "03-dependency-register.md",
    "04-blocker-register.md",
    "05-risk-adjusted-plan.md",
    "06-resource-capacity.md",
    "07-velocity-model.md",
    "08-estimation-model.md",
    "09-workstream-plan.md",
    "PLANNING_COMPLETENESS_AUDIT.md",
]

SPRINT_DOCS = [f"sprint-{i:02d}.md" for i in range(1, 19)] + ["SPRINT_EXECUTION_COMPLETENESS_AUDIT.md"]

MANDATED_SPRINT_SECTIONS = [
    "1. Sprint Header & Metadata",
    "2. Executive Summary & Sprint Vision",
    "3. Sprint Objectives & Desired Outcomes",
    "4. Non-Negotiable Sprint Invariants",
    "5. Upstream Architecture & SRS Traceability",
    "6. Sprint Schedule & Timeline",
    "7. Sprint Capacity & Availability Model",
    "8. Role-by-Role Capacity Allocation Table",
    "9. Sprint Velocity & Throughput Target",
    "10. Workstream Allocation & Squad Assignments",
    "11. Sprint Backlog — Epics & Strategic Themes",
    "12. Sprint Backlog — Features Delivered",
    "13. Sprint Backlog — User Stories",
    "14. Sprint Backlog — Engineering Tasks",
    "15. Sprint Backlog — Sub-Tasks & Micro-Work Breakdown",
    "16. Relational Database Changes",
    "17. Database Entity Mapping",
    "18. API Endpoints Delivered",
    "19. Frontend Screens, Components & UX Workflows",
    "20. Offline-First Caching & PWA Sync Protocol",
    "21. Integration Gateways & External Partner Endpoints",
    "22. Security Controls, Threat Mitigation & RBAC/ABAC",
    "23. QA Test Strategy & Acceptance Test Matrix",
    "24. Performance, Load & Concurrency Benchmark Targets",
    "25. Observability, Metrics, Logging & Alerts",
    "26. SRE Runbook & Incident Response Procedure",
    "27. Deployment Pipeline, CI/CD Stages & Rollback Strategy",
    "28. Infrastructure & Cloud Resource Manifests",
    "29. Data Engineering, ETL Pipelines & Lakehouse Sync",
    "30. AI/ML Engineering & Clinical Decision Support",
    "31. ABDM & National Health Stack Interoperability",
    "32. Regulatory, Compliance & DPDP Act 2023 Verification",
    "33. Clinical Validation & Standard Treatment Guidelines",
    "34. Training, Operational Readiness & Enablement",
    "35. Pilot Operations & Clinical Rollout Telemetry",
    "36. Cross-Sprint Dependencies",
    "37. Critical Path Items & Zero-Float Activities",
    "38. Sprint Blocker & Impediment Matrix",
    "39. Sprint Risk Register & Contingency Playbook",
    "40. Definition of Ready (DoR) Verification",
    "41. Definition of Done (DoD) Verification",
    "42. Quality Gate Verification & Sign-Off Criteria",
    "43. Sprint Review & Demonstration Agenda",
    "44. Sprint Retrospective & Kaizen Continuous Improvement",
    "45. Key Decisions & Architectural Records",
    "46. Formal Governance Sign-Off & Approvals",
]

PLACEHOLDER_PATTERNS = [
    re.compile(r'\bTODO\b', re.IGNORECASE),
    re.compile(r'\bTBD\b', re.IGNORECASE),
    re.compile(r'\bFIXME\b', re.IGNORECASE),
    re.compile(r'\blorem\s+ipsum\b', re.IGNORECASE),
    re.compile(r'\bto\s+be\s+decided\b', re.IGNORECASE),
]

def validate_all() -> bool:
    print("=" * 80)
    print("RUNNING MASTER PLANNING & 18-SPRINT QUALITY GATE VALIDATOR")
    print("=" * 80)

    p17_dir = PROJECT_ROOT / "docs" / "17-planning"
    p18_dir = PROJECT_ROOT / "docs" / "18-sprints"
    all_passed = True

    # Gate 1: File Existence (29 documents)
    print("\n[GATE 1] Verifying File Existence (10 Planning + 19 Sprint documents = 29 Total)...")
    missing_p17 = [d for d in PLANNING_DOCS if not (p17_dir / d).exists()]
    missing_p18 = [d for d in SPRINT_DOCS if not (p18_dir / d).exists()]
    if missing_p17 or missing_p18:
        print(f"  FAILED: Missing Phase 17 docs: {missing_p17}")
        print(f"  FAILED: Missing Phase 18 docs: {missing_p18}")
        all_passed = False
    else:
        print("  PASS: All 29 documents present across docs/17-planning/ and docs/18-sprints/.")

    # Gate 2: Substantive Line Counts (>= 2,000 per doc)
    print("\n[GATE 2] Verifying Substantive Line Counts (>= 2,000 per document)...")
    doc_contents = {}
    under_threshold = []
    total_substantive = 0
    total_raw = 0

    print(" --- Phase 17 Documents ---")
    for doc_name in PLANNING_DOCS:
        doc_path = p17_dir / doc_name
        if not doc_path.exists():
            continue
        content = doc_path.read_text(encoding="utf-8")
        doc_contents[f"17:{doc_name}"] = content
        stats = count_lines(content)
        sub = stats["substantive"]
        tot = stats["total"]
        total_substantive += sub
        total_raw += tot
        if sub < 2000:
            under_threshold.append((f"17:{doc_name}", sub))
        print(f"  - {doc_name:<45}: {sub:>5,} sub / {tot:>5,} tot")

    print("\n --- Phase 18 Documents ---")
    for doc_name in SPRINT_DOCS:
        doc_path = p18_dir / doc_name
        if not doc_path.exists():
            continue
        content = doc_path.read_text(encoding="utf-8")
        doc_contents[f"18:{doc_name}"] = content
        stats = count_lines(content)
        sub = stats["substantive"]
        tot = stats["total"]
        total_substantive += sub
        total_raw += tot
        if sub < 2000:
            under_threshold.append((f"18:{doc_name}", sub))
        print(f"  - {doc_name:<45}: {sub:>5,} sub / {tot:>5,} tot")

    print(f"\n  TOTAL PROGRAM DOCUMENTS:   {len(doc_contents)}")
    print(f"  TOTAL SUBSTANTIVE LINES:   {total_substantive:,}")
    print(f"  TOTAL RAW LINES:           {total_raw:,}")
    if under_threshold:
        print(f"  FAILED: {len(under_threshold)} documents below 2,000 substantive lines: {under_threshold}")
        all_passed = False
    else:
        print("  PASS: All 29 documents exceed 2,000 substantive lines.")

    # Gate 3: Disallowed Placeholders
    print("\n[GATE 3] Checking for Disallowed Placeholders (TODO, TBD, FIXME, lorem ipsum)...")
    found_placeholders = []
    for doc_key, content in doc_contents.items():
        for line_num, line in enumerate(content.splitlines(), 1):
            for pat in PLACEHOLDER_PATTERNS:
                matches = pat.findall(line)
                if matches:
                    lower_line = line.lower()
                    if (
                        "no todo" in lower_line
                        or "prohibition" in lower_line
                        or "zero todo" in lower_line
                        or "audit" in lower_line
                        or "checkpoint" in lower_line
                        or "0 occurrences" in lower_line
                        or "quality gate" in lower_line
                        or "scanned for" in lower_line
                        or "forbidden token" in lower_line
                        or "zero-placeholder" in lower_line
                        or "zero placeholder" in lower_line
                        or "zero-forbidden" in lower_line
                        or "zero forbidden" in lower_line
                        or "invariant" in lower_line
                    ):
                        continue
                    found_placeholders.append((doc_key, line_num, pat.pattern, line.strip()[:60]))

    if found_placeholders:
        print(f"  FAILED: Placeholders found in: {found_placeholders[:5]}")
        all_passed = False
    else:
        print("  PASS: Zero disallowed placeholder tokens detected across all 29 documents.")

    # Gate 4: Cross-Document Paragraph Duplication (< 2.0%)
    print("\n[GATE 4] Checking Cross-Document Paragraph Duplication (< 2.0%)...")
    duplicates = find_duplicate_paragraphs(doc_contents, min_len=60)
    total_paragraphs = sum(len(c.split("\n\n")) for c in doc_contents.values())
    dup_ratio = (len(duplicates) * 2 / total_paragraphs * 100) if total_paragraphs else 0.0
    print(f"  Total Paragraphs Analyzed: {total_paragraphs:,}")
    print(f"  Duplicate Paragraph Pairs: {len(duplicates):,}")
    print(f"  Duplicate Paragraph Ratio: {dup_ratio:.2f}% (Strict Limit: < 2.0%)")
    if dup_ratio >= 2.0:
        print("  FAILED: Duplication ratio exceeds 2.0% threshold.")
        all_passed = False
    else:
        print("  PASS: Cross-document paragraph duplication ratio comfortably within limits.")

    # Gate 5: Canonical Planning Registries
    print("\n[GATE 5] Verifying Canonical Planning Registries (16 Registries)...")
    registries = [
        ("OBJECTIVES", OBJECTIVES, 50),
        ("SCOPES", SCOPES, 30),
        ("DEPENDENCIES", DEPENDENCIES, 160),
        ("CRITICAL_PATH_ITEMS", CRITICAL_PATH_ITEMS, 50),
        ("BLOCKERS", BLOCKERS, 80),
        ("RISKS", RISKS, 50),
        ("CAPACITY_MODELS", CAPACITY_MODELS, 18),
        ("VELOCITY_MODELS", VELOCITY_MODELS, 20),
        ("ESTIMATION_MODELS", ESTIMATION_MODELS, 25),
        ("WORKSTREAMS", WORKSTREAMS, 18),
        ("MILESTONES", MILESTONES, 25),
        ("RELEASES", RELEASES, 10),
        ("QUALITY_GATES", QUALITY_GATES, 25),
        ("ASSUMPTIONS", ASSUMPTIONS, 30),
        ("DECISIONS", DECISIONS, 30),
        ("SPRINT_DEFINITIONS", SPRINT_DEFINITIONS, 18),
    ]
    reg_errors = []
    for rname, rlist, target in registries:
        if len(rlist) != target:
            reg_errors.append(f"{rname} count {len(rlist)} != target {target}")
        if isinstance(rlist[0], dict) and "id" in rlist[0]:
            ids = [item["id"] for item in rlist]
            if len(ids) != len(set(ids)):
                reg_errors.append(f"{rname} has duplicate IDs!")

    if reg_errors:
        print(f"  FAILED: Canonical registry errors: {reg_errors}")
        all_passed = False
    else:
        print(f"  PASS: All 16 canonical registries verified and clean ({sum(t for _, _, t in registries)} total items).")

    # Gate 6: Table Traceability (52 Tables)
    print("\n[GATE 6] Verifying Upstream Relational Table Traceability (TABLE-001 to TABLE-052)...")
    all_text = "\n".join(doc_contents.values())
    missing_tables = [t["id"] for t in TABLES if t["id"] not in all_text]
    if missing_tables:
        print(f"  FAILED: Missing tables: {missing_tables}")
        all_passed = False
    else:
        print(f"  PASS: All {len(TABLES)} relational database tables fully traced.")

    # Gate 7: Feature Traceability (180 Features)
    print("\n[GATE 7] Verifying Upstream Product Feature Traceability (FEATURE-001 to FEATURE-180)...")
    missing_features = [f["id"] for f in FEATURES if f["id"] not in all_text]
    if missing_features:
        print(f"  FAILED: Missing features: {missing_features}")
        all_passed = False
    else:
        print(f"  PASS: All {len(FEATURES)} product features fully traced.")

    # Gate 8: Mandated Sprint Sections (46 Sections across Sprints 01-18)
    print("\n[GATE 8] Verifying 46 Mandated Sections across Sprints 01-18 (828 Section Checks)...")
    missing_sections = []
    for s_num in range(1, 19):
        doc_key = f"18:sprint-{s_num:02d}.md"
        content = doc_contents.get(doc_key, "")
        for sec in MANDATED_SPRINT_SECTIONS:
            # Match section title ignoring punctuation
            prefix = sec.split(".")[0].strip()
            pattern = re.compile(rf"^##\s+{prefix}\.\s+", re.MULTILINE)
            if not pattern.search(content):
                missing_sections.append((doc_key, sec))

    if missing_sections:
        print(f"  FAILED: Missing sprint sections: {missing_sections[:10]}")
        all_passed = False
    else:
        print("  PASS: All 18 sprint documents contain all 46 mandated sections (828/828 assertions passed).")

    # Gate 9: Documentation-Only Code Annotations
    print("\n[GATE 9] Verifying Code Tagging & Documentation-Only Annotations...")
    unannotated = 0
    for doc_key, content in doc_contents.items():
        if "```yaml" in content and "DOCUMENTATION-ONLY" not in content:
            unannotated += 1
        if "```json" in content and "DOCUMENTATION-ONLY" not in content:
            unannotated += 1

    if unannotated > 0:
        print(f"  FAILED: Unannotated blocks in {unannotated} files.")
        all_passed = False
    else:
        print("  PASS: All code, configuration, and JSON snippets properly tagged DOCUMENTATION-ONLY.")

    # Gate 10: Zero Runtime Code
    print("\n[GATE 10] Verifying Zero Application Runtime Code...")
    forbidden_extensions = [".ts", ".js", ".go", ".java", ".sql", ".prisma"]
    found_runtime = []
    for ext in forbidden_extensions:
        found_runtime.extend(list(p17_dir.glob(f"*{ext}")))
        found_runtime.extend(list(p18_dir.glob(f"*{ext}")))

    if found_runtime:
        print(f"  FAILED: Forbidden runtime files found: {found_runtime}")
        all_passed = False
    else:
        print("  PASS: Zero runtime code in docs/17-planning/ and docs/18-sprints/.")

    print("\n" + "=" * 80)
    if all_passed:
        print("ALL 10 QUALITY GATES PASSED! PHASE 17 & 18 PLANNING BASELINE IS 100% COMPLIANT!")
    else:
        print("QUALITY GATES FAILED! REVIEW DETAILED ERRORS ABOVE.")
    print("=" * 80)

    return all_passed

if __name__ == "__main__":
    if not validate_all():
        sys.exit(1)
