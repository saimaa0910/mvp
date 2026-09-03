import os
import sys

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

# ==========================================
# PHASE 17: DEPENDENCY MANAGEMENT
# ==========================================

def build_phase_17():
    base_dir = os.path.join("docs", "17-planning")
    
    dag_content = """# 🗺️ Master Dependency Map & Directed Acyclic Graph (DAG)
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PLN-DEP-01 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Master Architectural Dependency DAG

```mermaid
graph TD
    R0[Requirements & SRS] --> A0[System Architecture]
    A0 --> D0[Database Schema & DDL]
    A0 --> API0[API Contracts OpenAPI]
    A0 --> SEC0[Security & RBAC Rules]
    D0 --> BE0[Backend Repository Layer]
    API0 --> BE0
    SEC0 --> BE0
    BE0 --> FE0[Frontend UI Integration]
    D0 --> DW0[Star Schema OLAP Mart]
    BE0 --> SYNC0[Offline Sync Engine]
    FE0 --> QA0[Playwright E2E Tests]
    SYNC0 --> QA0
    QA0 --> PILOT0[20-Clinic Field Pilot]
    PILOT0 --> SCALE0[183-Clinic Citywide Rollout]
    SCALE0 --> AI0[Safe AI & ABDM M1-M3]
```
"""
    write_file(os.path.join(base_dir, "01-master-dependency-map.md"), dag_content)

    cp_content = """# ⏱️ Critical Path Analysis & Milestone Float
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PLN-CRP-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Critical Path Activities (Zero Slack / Zero Float)
1. **Weeks 1-4 (S01-S02):** Core Database Schema DDL & Auth API Infrastructure.
2. **Weeks 5-8 (S03-S04):** Patient Registration, Queue Engine & Triage Vitals.
3. **Weeks 9-12 (S05-S06):** Doctor EMR Console & Electronic Prescribing.
4. **Weeks 13-16 (S07-S08):** Pharmacy Dispense & Batch Inventory Ledger.
5. **Weeks 17-20 (S09-S10):** Offline PWA Storage & Background Sync Hardening.
6. **Weeks 21-24 (S11-S12):** 20-Clinic Field Pilot Go-Live & Validation (Gate 11).
7. **Weeks 25-28 (S13-S14):** Field Stabilization, High-Concurrency Load & Scale.
8. **Weeks 29-32 (S15-S16):** ABDM M1-M3 & Safe AI Decision Support.
9. **Weeks 33-36 (S17-S18):** Citywide 183-Clinic Final Rollout & Handover.
"""
    write_file(os.path.join(base_dir, "02-critical-path.md"), cp_content)

    pln_files = [
        ("03-dependency-register.md", "Dependency Register", "Catalog of 30 internal and external dependencies (DEP-001 to DEP-030) with owners and statuses."),
        ("04-blocker-register.md", "Blocker Management Register", "Procedures for logging, escalating, and resolving blocking technical issues within 24 hours."),
        ("05-risk-adjusted-plan.md", "Risk-Adjusted Schedule Plan", "Incorporate 15% buffer capacity to absorb unexpected hardware or broadband delays."),
        ("06-resource-capacity.md", "Engineering Resource Capacity Model", "Team allocation across 18 specialized roles with 80% focus factor."),
        ("07-velocity-model.md", "Sprint Velocity & Throughput Model", "Target velocity of 45-50 story points per 2-week sprint across 4 squads."),
        ("08-estimation-model.md", "Estimation Framework & Sizing Model", "Modified Fibonacci points (1, 2, 3, 5, 8) calibrated against complexity and clinical risk."),
        ("09-workstream-plan.md", "Multi-Track Workstream Integration Plan", "Managing parallel workstreams: Core Clinical, Supply Chain, Analytics, and Field Ops.")
    ]

    for fname, title, desc in pln_files:
        write_file(os.path.join(base_dir, fname), f"# 📅 Planning Specification: {title}\n## Namma Clinic Platform\n\n### 1. Overview\n{desc}")

# ==========================================
# PHASE 18: SPRINT PLAN (18 SPRINTS)
# ==========================================

def build_phase_18():
    base_dir = os.path.join("docs", "18-sprints")
    
    sprint_goals = [
        ("sprint-01.md", "S01", "Foundation Scaffolding & DB DDL", "REL-00", "Deploy PostgreSQL 16 schema, Fastify API boilerplate, Docker environment, and base domain types."),
        ("sprint-02.md", "S02", "Authentication, RBAC & Audit Log", "REL-00", "Implement Bcrypt auth, JWT token rotation, 12 roles, 48 permissions, and append-only audit logging."),
        ("sprint-03.md", "S03", "Patient Registration & Identity", "REL-01", "Implement patient search with pg_trgm, registration form, DPDP consent, and UHID generator."),
        ("sprint-04.md", "S04", "Queue Management & Triage Vitals", "REL-01", "Implement daily token generator, thermal slip print, touchscreen vitals entry, and danger alerts."),
        ("sprint-05.md", "S05", "Doctor EMR Console & Complaints", "REL-02", "Build doctor consultation workspace, 1-click chief complaint chips, and historical visit preview."),
        ("sprint-06.md", "S06", "Prescription & Diagnosis Coding", "REL-02", "Implement electronic prescription builder, formulary drug lookup, and ICD-10 diagnosis picker."),
        ("sprint-07.md", "S07", "Pharmacy Dispense & Batch Ledger", "REL-03", "Implement pharmacy dispense queue, FEFO batch selection, atomic stock deduction, and bilingual slips."),
        ("sprint-08.md", "S08", "Point-of-Care Lab & Referrals", "REL-03", "Implement 14 PoC lab test ordering/results and outbound secondary referral letters with QR codes."),
        ("sprint-09.md", "S09", "Offline PWA Storage & IndexedDB", "REL-04", "Implement Dexie.js offline cache, Service Worker asset caching, and offline PIN verification."),
        ("sprint-10.md", "S10", "Background Sync & Analytics DW", "REL-04", "Build background sync engine, deterministic conflict resolution, and Star Schema analytics ETL."),
        ("sprint-11.md", "S11", "20-Clinic Pilot Deployment", "REL-05", "Deploy pilot release to 20 representative clinics across 8 zones; initiate frontline staff training."),
        ("sprint-12.md", "S12", "Pilot Stabilization & Field Triage", "REL-05", "Monitor pilot clinic SLA, triage frontline bug reports, optimize thermal printing, and review KPIs."),
        ("sprint-13.md", "S13", "High-Concurrency Scale & Tuning", "REL-06", "Optimize database query plans, tune Redis connection pools, and run 500 req/sec k6 load tests."),
        ("sprint-14.md", "S14", "Zonal Command Dashboards", "REL-06", "Deliver Zonal Health Officer and Special Commissioner dashboards with geo-spatial disease mapping."),
        ("sprint-15.md", "S15", "ABDM M1-M3 Interoperability", "REL-07", "Integrate ABHA verification, FHIR R4 care context linking, and national health gateway push."),
        ("sprint-16.md", "S16", "Safe AI Decision Support", "REL-07", "Deploy stockout forecasting model, fever anomaly detection, and mandatory physician override."),
        ("sprint-17.md", "S17", "Citywide 183-Clinic Wave Rollout", "REL-06", "Execute wave-wise rollout across all 183 clinics; train 500+ doctors and nurses."),
        ("sprint-18.md", "S18", "Final Hardening, Audit & Handover", "REL-06", "Conduct external CERT-In VAPT audit, final documentation sign-off, and handover to BBMP.")
    ]

    for fname, sid, title, rel, goal in sprint_goals:
        content = f"""# ⏱️ Sprint Plan: {sid} — {title}
## Namma Clinic Digital Health & Operations Platform
**Release:** `{rel}` | **Cadence:** 10 Working Days (2 Calendar Weeks) | **Status:** Approved Baseline

---

### 1. Sprint Goal & Objectives
**Goal:** {goal}

### 2. Sprint Parameters & Capacity
- **Target Velocity:** 45 Story Points
- **Team Allocation:** 1 Architect, 2 Backend, 2 Frontend, 1 DB, 1 QA, 1 DevOps
- **Definition of Ready:** Backlog items meet DoR (`docs/01-project-management/16-definition-of-ready.md`)
- **Definition of Done:** Deliverables meet DoD (`docs/01-project-management/17-definition-of-done.md`)

### 3. Day-by-Day Sprint Execution Cadence
- **Day 1:** Sprint Planning, task breakdown, API contract freeze.
- **Day 2-4:** Core domain logic, database queries, frontend components.
- **Day 5:** Mid-sprint internal integration and clinical advisor check-in.
- **Day 6-8:** End-to-end integration, unit test completion (>=85%), offline test.
- **Day 9:** Regression suite execution, security scan, bug fixing.
- **Day 10:** Sprint Review, stakeholder demo, retrospective, release tagging.

### 4. Sprint Quality Gates & Exit Criteria
1. 100% of planned user stories deployed to Test environment.
2. Zero P0 or P1 open defects.
3. Automated Playwright E2E journey passing without retries.
"""
        write_file(os.path.join(base_dir, fname), content)

# ==========================================
# PHASE 19: RELEASE PLAN (8 RELEASES)
# ==========================================

def build_phase_19():
    base_dir = os.path.join("docs", "19-releases")
    
    releases = [
        ("release-00-foundation.md", "REL-00: Foundation & Core Infra", "S01 - S02", "Deliver database schema, base APIs, authentication, RBAC, CI/CD, and developer tooling."),
        ("release-01-core-patient.md", "REL-01: Core Patient & Queue Management", "S03 - S04", "Deliver citizen registration, demographic search, daily token desk, and triage vitals entry."),
        ("release-02-clinical.md", "REL-02: Clinical Consultation & EMR-Lite", "S05 - S06", "Deliver doctor consultation workspace, ICD-10 diagnosis picker, and electronic prescribing."),
        ("release-03-pharmacy-lab-referral.md", "REL-03: Pharmacy, Diagnostics & Referral", "S07 - S08", "Deliver FEFO pharmacy dispensing, batch stock ledger, 14 lab tests, and secondary referrals."),
        ("release-04-analytics-offline.md", "REL-04: Analytics & Offline Resilience", "S09 - S10", "Deliver IndexedDB offline PWA sync engine, CDC pipeline, and Star Schema data mart."),
        ("release-05-pilot.md", "REL-05: 20-Clinic Field Pilot Release", "S11 - S12", "Field deployment in 20 representative clinics across 8 zones; operational stabilization."),
        ("release-06-production-scale.md", "REL-06: Production Citywide Scale (183 Clinics)", "S13 - S14 / S17 - S18", "Full-scale rollout to all 183 clinics, high-concurrency tuning, and VAPT certification."),
        ("release-07-ai-abdm.md", "REL-07: Safe AI & ABDM National Integration", "S15 - S16", "Deploy stockout forecasting, fever anomaly surveillance, and ABDM M1-M3 FHIR R4 linking.")
    ]

    for fname, title, sprs, desc in releases:
        content = f"""# 🚀 Software Release Plan: {title}
## Namma Clinic Digital Health & Operations Platform
**Sprints:** `{sprs}` | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Release Executive Summary
{desc}

### 2. Release Entry & Exit Criteria
- **Entry Criteria:** Previous release stabilized; all prerequisite sprint DoDs satisfied.
- **Exit Criteria:** 100% test pass rate; zero P0/P1 defects; security scan approved; steering gate sign-off.
- **Rollback Strategy:** Blue/Green container rollback executable in < 2 minutes with zero data loss.
"""
        write_file(os.path.join(base_dir, fname), content)

# ==========================================
# PHASE 20: MASTER TIMEPLAN
# ==========================================

def build_phase_20():
    base_dir = os.path.join("docs", "20-timeplan")
    
    tp_files = [
        ("01-master-timeplan.md", "Master Project Timeplan & 36-Week Gantt", "End-to-end 36-week timeline mapping 18 sprints, 8 releases, and 12 governance approval gates."),
        ("02-team-capacity.md", "Engineering & Operational Capacity Plan", "Staffing allocations across 18 roles totaling 14 full-time equivalents (FTEs)."),
        ("03-resource-plan.md", "Resource Allocation & Budget Schedule", "Resource expenditure model aligned with GBA / BBMP milestone billing terms."),
        ("04-estimation-model.md", "Estimation Calibration & Velocity Model", "Historical calibration of story points to developer hours across backend, frontend, and QA."),
        ("05-workstream-timeline.md", "Cross-Functional Workstream Schedules", "Synchronized timeline across Clinical, Platform, Data Engineering, and Field Deployment teams."),
        ("06-milestone-plan.md", "Master Milestone Verification Plan", "Formal verification checkpoints for M01 through M10 with measurable deliverables."),
        ("07-pilot-plan.md", "20-Clinic Field Pilot Execution Plan", "Clinic selection, hardware readiness check, staff training calendar, and 10-week pilot monitoring."),
        ("08-rollout-plan.md", "Wave-Wise 183-Clinic Citywide Rollout Plan", "Rollout plan structured in 4 waves (45 clinics/wave) with dedicated field support teams.")
    ]

    for fname, title, desc in tp_files:
        write_file(os.path.join(base_dir, fname), f"# 📅 Timeplan Specification: {title}\n## Namma Clinic Platform\n\n### 1. Overview\n{desc}")

def main():
    build_phase_17()
    build_phase_18()
    build_phase_19()
    build_phase_20()

if __name__ == "__main__":
    main()
