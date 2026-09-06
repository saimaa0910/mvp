"""
build_canonical_backlog_registry.py
Generates the complete canonical Backlog Registry (5,600 items across 10 datasets)
split across 6 modular files to optimize file size, memory, and validation performance.
"""

import sys
from pathlib import Path

BACKLOG_DIR = Path(__file__).resolve().parent

EPIC_DOMAINS = [
    "Core Foundation & Micro-Frontends",
    "Clinical Workbench & Consultation",
    "Pharmacy Dispensary & Inventory",
    "Laboratory & Diagnostics",
    "Maternal & Child Health Outreach",
    "ABDM National Interoperability",
    "NIC eHospital Secondary Referrals",
    "Telecom SMS & Citizen Notifications",
    "State Public Health Surveillance",
    "File Exports & Analytical Hub",
    "Zero-Trust Security & Cryptography",
    "DevOps SRE & Cloud Infrastructure",
    "Data Engineering & Lakehouse",
    "AI/ML Clinical Decision Support"
]

PERSONAS = [
    "Medical Officer (Treating Clinician)",
    "Staff Nurse (Triage & Vitals)",
    "Pharmacist (Dispensary & Stock)",
    "Lab Technician (Diagnostics)",
    "Zonal Epidemiologist (Surveillance)",
    "Citizen / Patient (Health Consumer)",
    "Zonal Health Administrator",
    "SRE / Platform Operations Engineer"
]

TASK_TYPES = [
    "BACKEND_API_SERVICE",
    "FRONTEND_WEB_COMPONENT",
    "DATABASE_SCHEMA_MIGRATION",
    "INTEGRATION_ADAPTER",
    "AUTOMATED_TEST_SUITE",
    "SECURITY_HARDENING_CONTROL",
    "DEVOPS_CI_CD_PIPELINE",
    "OBSERVABILITY_PROMETHEUS_METRIC"
]

SQUADS = [
    "squad_clinical_experience",
    "squad_pharmacy_logistics",
    "squad_diagnostic_services",
    "squad_integrations_platform",
    "squad_security_governance",
    "squad_devops_infrastructure",
    "squad_data_analytics",
    "squad_ai_decision_support"
]

def build_part1():
    lines = ['"""Phase 16 Canonical Backlog Registry - Part 1: EPICS & BACKLOG_FEATURES"""', '']

    # 1. EPICS (50 items: EPIC-001 to EPIC-050)
    lines.append('EPICS = [')
    for i in range(1, 51):
        dom = EPIC_DOMAINS[(i - 1) % len(EPIC_DOMAINS)]
        squad = SQUADS[(i - 1) % len(SQUADS)]
        rel_target = f"RELEASE-{(i-1)//10 + 1}.0"
        lines.append('    {')
        lines.append(f'        "id": "EPIC-{i:03d}",')
        lines.append(f'        "title": "Delivery Epic {i:03d}: Enterprise {dom}",')
        lines.append(f'        "domain": "{dom}",')
        lines.append(f'        "description": "Architectural and functional delivery epic {i:03d} establishing scalable capabilities for {dom} across 450+ municipal clinics.",')
        lines.append(f'        "business_value": "Eliminates operational latency, enforces clinical safety, and satisfies DPDP/ABDM compliance.",')
        lines.append(f'        "target_release": "{rel_target}",')
        lines.append(f'        "owner_squad": "{squad}",')
        lines.append(f'        "status": "APPROVED_FOR_IMPLEMENTATION",')
        lines.append(f'        "strategic_pillar": "Municipal Healthcare Digital Transformation",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    # 2. BACKLOG_FEATURES (250 items: BFEATURE-001 to BFEATURE-250)
    lines.append('BACKLOG_FEATURES = [')
    for i in range(1, 251):
        epic_id = f"EPIC-{(i - 1) % 50 + 1:03d}"
        up_feature_id = f"FEATURE-{(i - 1) % 180 + 1:03d}"
        complexity = "HIGH" if i % 3 == 0 else ("MEDIUM" if i % 3 == 1 else "LOW")
        sprint_target = f"SPRINT-{(i - 1) % 24 + 1:02d}"
        priority = "P1_CRITICAL" if i % 4 == 0 else ("P2_HIGH" if i % 4 == 1 else "P3_MEDIUM")
        lines.append('    {')
        lines.append(f'        "id": "BFEATURE-{i:03d}",')
        lines.append(f'        "epic_id": "{epic_id}",')
        lines.append(f'        "upstream_feature_id": "{up_feature_id}",')
        lines.append(f'        "title": "Delivery Feature {i:03d} (Traced to {up_feature_id})",')
        lines.append(f'        "description": "Granular implementation feature fulfilling requirements of {up_feature_id} under governance of {epic_id}.",')
        lines.append(f'        "complexity": "{complexity}",')
        lines.append(f'        "target_sprint": "{sprint_target}",')
        lines.append(f'        "priority": "{priority}",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    (BACKLOG_DIR / "backlog_data_part1.py").write_text("\n".join(lines), encoding="utf-8")
    print("Generated backlog_data_part1.py")

def build_part2():
    lines = ['"""Phase 16 Canonical Backlog Registry - Part 2: USER_STORIES"""', '']

    # 3. USER_STORIES (500 items: STORY-001 to STORY-500)
    lines.append('USER_STORIES = [')
    story_pts = [1, 2, 3, 5, 8, 13]
    for i in range(1, 501):
        feat_id = f"BFEATURE-{(i - 1) % 250 + 1:03d}"
        epic_id = f"EPIC-{(i - 1) % 50 + 1:03d}"
        persona = PERSONAS[(i - 1) % len(PERSONAS)]
        pts = story_pts[(i - 1) % len(story_pts)]
        prio = "P1_MUST_HAVE" if i % 3 == 0 else ("P2_SHOULD_HAVE" if i % 3 == 1 else "P3_COULD_HAVE")
        lines.append('    {')
        lines.append(f'        "id": "STORY-{i:03d}",')
        lines.append(f'        "feature_id": "{feat_id}",')
        lines.append(f'        "epic_id": "{epic_id}",')
        lines.append(f'        "persona": "{persona}",')
        lines.append(f'        "title": "User Story {i:03d}: As a {persona}, I need specialized workflow support",')
        lines.append(f'        "as_a": "{persona}",')
        lines.append(f'        "i_want": "seamless, deterministic execution of clinical or operational step {i:03d} without UI lag",')
        lines.append(f'        "so_that": "patient care is delivered safely, auditable records are created, and compliance is maintained",')
        lines.append(f'        "given": "the user is authenticated with active role and the clinic edge node is online or offline",')
        lines.append(f'        "when": "the user initiates action {i:03d} on the clinical or administrative workbench",')
        lines.append(f'        "then": "the system validates inputs, updates local and cloud ledgers, and displays confirmation in < 250ms",')
        lines.append(f'        "story_points": {pts},')
        lines.append(f'        "priority": "{prio}",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    (BACKLOG_DIR / "backlog_data_part2.py").write_text("\n".join(lines), encoding="utf-8")
    print("Generated backlog_data_part2.py")

def build_part3():
    lines = ['"""Phase 16 Canonical Backlog Registry - Part 3: TASKS"""', '']

    # 4. TASKS (1,000 items: TASK-001 to TASK-1000)
    lines.append('TASKS = [')
    for i in range(1, 1001):
        story_id = f"STORY-{(i - 1) % 500 + 1:03d}"
        ttype = TASK_TYPES[(i - 1) % len(TASK_TYPES)]
        squad = SQUADS[(i - 1) % len(SQUADS)]
        hours = 8 + (i % 4) * 4
        lines.append('    {')
        lines.append(f'        "id": "TASK-{i:04d}",')
        lines.append(f'        "story_id": "{story_id}",')
        lines.append(f'        "title": "Technical Implementation Task {i:04d} ({ttype})",')
        lines.append(f'        "task_type": "{ttype}",')
        lines.append(f'        "estimated_hours": {hours},')
        lines.append(f'        "owner_squad": "{squad}",')
        lines.append(f'        "definition_of_done": "Code written, unit tests passing > 90% branch coverage, zero security alerts, PR reviewed and merged into main.",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    (BACKLOG_DIR / "backlog_data_part3.py").write_text("\n".join(lines), encoding="utf-8")
    print("Generated backlog_data_part3.py")

def build_part4():
    lines = ['"""Phase 16 Canonical Backlog Registry - Part 4: MICRO_TASKS"""', '']

    # 5. MICRO_TASKS (2,500 items: UTASK-0001 to UTASK-2500)
    lines.append('MICRO_TASKS = [')
    for i in range(1, 2501):
        task_id = f"TASK-{(i - 1) % 1000 + 1:04d}"
        hours = 2 + (i % 3) * 2
        lines.append('    {')
        lines.append(f'        "id": "UTASK-{i:04d}",')
        lines.append(f'        "task_id": "{task_id}",')
        lines.append(f'        "title": "Micro-Task {i:04d}: Atomic Implementation Work Unit",')
        lines.append(f'        "technical_scope": "Granular coding, schema modification, test case execution, or configuration tuning for {task_id}.",')
        lines.append(f'        "estimated_hours": {hours},')
        lines.append(f'        "verification_criteria": "Compiles cleanly, automated assertion succeeds, and local regression check passes.",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    (BACKLOG_DIR / "backlog_data_part4.py").write_text("\n".join(lines), encoding="utf-8")
    print("Generated backlog_data_part4.py")

def build_part5():
    lines = ['"""Phase 16 Canonical Backlog Registry - Part 5: DEPENDENCIES & TESTS"""', '']

    # 6. BACKLOG_DEPENDENCIES (500 items: DEP-BL-001 to DEP-BL-500)
    lines.append('BACKLOG_DEPENDENCIES = [')
    for i in range(1, 501):
        pred = f"TASK-{i:04d}"
        succ = f"TASK-{(i % 1000) + 1:04d}"
        is_crit = True if i % 5 == 0 else False
        lines.append('    {')
        lines.append(f'        "id": "DEP-BL-{i:03d}",')
        lines.append(f'        "predecessor_task": "{pred}",')
        lines.append(f'        "successor_task": "{succ}",')
        lines.append(f'        "dependency_type": "FINISH_TO_START",')
        lines.append(f'        "lag_days": 0,')
        lines.append(f'        "critical_path": {is_crit},')
        lines.append(f'        "description": "Predecessor task {pred} must successfully complete before successor task {succ} unblocks.",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    # 7. BACKLOG_TESTS (500 items: TEST-BL-001 to TEST-BL-500)
    lines.append('BACKLOG_TESTS = [')
    test_levels = ["UNIT_ISOLATED", "INTEGRATION_CONTRACT", "E2E_WORKFLOW", "SECURITY_VAPT", "ACCESSIBILITY_WCAG"]
    test_tools = ["pytest", "Jest / Vitest", "Playwright", "OWASP ZAP", "axe-core"]
    for i in range(1, 501):
        story_id = f"STORY-{i:03d}"
        tlevel = test_levels[(i - 1) % len(test_levels)]
        ttool = test_tools[(i - 1) % len(test_tools)]
        lines.append('    {')
        lines.append(f'        "id": "TEST-BL-{i:03d}",')
        lines.append(f'        "story_id": "{story_id}",')
        lines.append(f'        "test_name": "Automated Quality Gate {i:03d} for {story_id}",')
        lines.append(f'        "test_level": "{tlevel}",')
        lines.append(f'        "automated": True,')
        lines.append(f'        "test_tool": "{ttool}",')
        lines.append(f'        "assertion": "Verifies that acceptance criteria for {story_id} are 100% satisfied without side effects.",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    (BACKLOG_DIR / "backlog_data_part5.py").write_text("\n".join(lines), encoding="utf-8")
    print("Generated backlog_data_part5.py")

def build_part6():
    lines = ['"""Phase 16 Canonical Backlog Registry - Part 6: RISKS, RELEASES & SPRINTS"""', '']

    # 8. BACKLOG_RISKS (100 items: RISK-BL-001 to RISK-BL-100)
    lines.append('BACKLOG_RISKS = [')
    risk_cats = ["SCHEDULE_DELAY", "TECHNICAL_COMPLEXITY", "PARTNER_DEPENDENCY", "REGULATORY_COMPLIANCE", "CLINICIAN_ADOPTION"]
    for i in range(1, 101):
        rcat = risk_cats[(i - 1) % len(risk_cats)]
        prob = "HIGH" if i % 3 == 0 else ("MEDIUM" if i % 3 == 1 else "LOW")
        imp = "CRITICAL" if i % 4 == 0 else "HIGH"
        lines.append('    {')
        lines.append(f'        "id": "RISK-BL-{i:03d}",')
        lines.append(f'        "title": "Delivery Risk {i:03d}: {rcat} Threat to Milestone",')
        lines.append(f'        "risk_category": "{rcat}",')
        lines.append(f'        "probability": "{prob}",')
        lines.append(f'        "impact": "{imp}",')
        lines.append(f'        "mitigation_strategy": "Implement early spike, establish daily partner sync, and build automated offline buffer.",')
        lines.append(f'        "contingency_plan": "Engage secondary failover provider and reallocate dedicated SRE squad resources.",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    # 9. RELEASE_MAPPINGS (100 items: REL-001 to REL-100)
    lines.append('RELEASE_MAPPINGS = [')
    tiers = ["Pilot Cluster (20 Clinics)", "Zonal Expansion (100 Clinics)", "Full Municipal Rollout (450+ Clinics)"]
    for i in range(1, 101):
        major = (i - 1) // 20 + 1
        minor = ((i - 1) % 20) // 4
        patch = (i - 1) % 4
        ver = f"v{major}.{minor}.{patch}"
        tier = tiers[(i - 1) % len(tiers)]
        lines.append('    {')
        lines.append(f'        "id": "REL-{i:03d}",')
        lines.append(f'        "release_version": "{ver}",')
        lines.append(f'        "release_name": "Municipal Platform Release {ver} ({tier})",')
        lines.append(f'        "target_date": "2026-10-{(i-1)%28+1:02d}",')
        lines.append(f'        "scope_summary": "Rolls out hardened clinical, inventory, and interoperability features to {tier}.",')
        lines.append(f'        "readiness_gate": "Gate PR-RELEASE-{(i-1)%25+1:03d} (100% automated regression test pass)",')
        lines.append(f'        "deployment_tier": "{tier}",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    # 10. SPRINT_MAPPINGS (100 items across 24 Sprints: SPRINT-01 to SPRINT-24)
    lines.append('SPRINT_MAPPINGS = [')
    for i in range(1, 101):
        sprint_num = (i - 1) % 24 + 1
        theme = EPIC_DOMAINS[(i - 1) % len(EPIC_DOMAINS)]
        lines.append('    {')
        lines.append(f'        "id": "SPMAP-{i:03d}",')
        lines.append(f'        "sprint_number": {sprint_num},')
        lines.append(f'        "sprint_code": "SPRINT-{sprint_num:02d}",')
        lines.append(f'        "start_date": "2026-{(sprint_num-1)//2 + 1:02d}-01",')
        lines.append(f'        "end_date": "2026-{(sprint_num-1)//2 + 1:02d}-14",')
        lines.append(f'        "capacity_story_points": {180 + (sprint_num % 5)*20},')
        lines.append(f'        "focus_theme": "{theme}",')
        lines.append(f'        "sprint_goal": "Deliver verified stories for {theme} and satisfy definition of done.",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    (BACKLOG_DIR / "backlog_data_part6.py").write_text("\n".join(lines), encoding="utf-8")
    print("Generated backlog_data_part6.py")

def build_aggregator():
    lines = [
        '"""Phase 16 Canonical Backlog Core Data Aggregator"""',
        '',
        'from scripts.backlog.backlog_data_part1 import EPICS, BACKLOG_FEATURES',
        'from scripts.backlog.backlog_data_part2 import USER_STORIES',
        'from scripts.backlog.backlog_data_part3 import TASKS',
        'from scripts.backlog.backlog_data_part4 import MICRO_TASKS',
        'from scripts.backlog.backlog_data_part5 import BACKLOG_DEPENDENCIES, BACKLOG_TESTS',
        'from scripts.backlog.backlog_data_part6 import BACKLOG_RISKS, RELEASE_MAPPINGS, SPRINT_MAPPINGS',
        '',
        '__all__ = [',
        '    "EPICS",',
        '    "BACKLOG_FEATURES",',
        '    "USER_STORIES",',
        '    "TASKS",',
        '    "MICRO_TASKS",',
        '    "BACKLOG_DEPENDENCIES",',
        '    "BACKLOG_TESTS",',
        '    "BACKLOG_RISKS",',
        '    "RELEASE_MAPPINGS",',
        '    "SPRINT_MAPPINGS",',
        ']',
        ''
    ]
    (BACKLOG_DIR / "backlog_core_data.py").write_text("\n".join(lines), encoding="utf-8")
    print("Generated backlog_core_data.py")

def main():
    build_part1()
    build_part2()
    build_part3()
    build_part4()
    build_part5()
    build_part6()
    build_aggregator()
    print("ALL 6 BACKLOG DATA PARTS & AGGREGATOR BUILT SUCCESSFULLY!")

if __name__ == "__main__":
    main()
