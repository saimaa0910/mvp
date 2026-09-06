"""
timeplan_core_data.py
Authoritative machine-readable timeplan registry for Phase 20: Master Timeplan.
Defines canonical entities for program timeline phases, milestones, workstreams,
teams, roles, capacity models, critical path nodes, pilot phases, and rollout waves.
"""

from typing import Dict, List, Any

PROGRAM_PHASES = [
    {
        "phase_id": "PROGRAM-PHASE-1",
        "name": "Phase 1: Foundation Architecture, Security & Core Outpatient OPD",
        "duration_weeks": 8,
        "sprint_range": "SPRINT-01 to SPRINT-04",
        "calendar_window": "Weeks 01 to 08 (Months 1–2)",
        "lead_workstream": "WORKSTREAM-05",
        "deliverables": [
            "Fastify and PostgreSQL multi-tenant foundation",
            "Keycloak OIDC and WORM audit ledger",
            "Citizen registration and ABHA M1 minting",
            "Patient token generation and queue orchestration"
        ],
        "exit_gate": "QUALITY-GATE-004",
        "status": "APPROVED_SCHEDULE"
    },
    {
        "phase_id": "PROGRAM-PHASE-2",
        "name": "Phase 2: Clinical Outpatient Encounter, Pharmacy & Ancillary Diagnostics",
        "duration_weeks": 8,
        "sprint_range": "SPRINT-05 to SPRINT-08",
        "calendar_window": "Weeks 09 to 16 (Months 3–4)",
        "lead_workstream": "WORKSTREAM-04",
        "deliverables": [
            "Nurse triage workbench and vital signs capture",
            "Doctor clinical consultation console and timeline",
            "ICD-10 and SNOMED CT diagnosis coding",
            "STG-compliant electronic prescription generator"
        ],
        "exit_gate": "QUALITY-GATE-008",
        "status": "APPROVED_SCHEDULE"
    },
    {
        "phase_id": "PROGRAM-PHASE-3",
        "name": "Phase 3: Pharmacy Logistics, POC Laboratory & Secondary Referrals",
        "duration_weeks": 8,
        "sprint_range": "SPRINT-09 to SPRINT-12",
        "calendar_window": "Weeks 17 to 24 (Months 5–6)",
        "lead_workstream": "WORKSTREAM-07",
        "deliverables": [
            "FEFO-allocated pharmacy dispensing counter",
            "Point-of-care rapid diagnostic lab ordering and results",
            "NIC eHospital secondary referral gateway",
            "Automated bilingual patient SMS alerts"
        ],
        "exit_gate": "QUALITY-GATE-012",
        "status": "APPROVED_SCHEDULE"
    },
    {
        "phase_id": "PROGRAM-PHASE-4",
        "name": "Phase 4: Offline Edge Resilience, Lakehouse Analytics & Security Hardening",
        "duration_weeks": 8,
        "sprint_range": "SPRINT-13 to SPRINT-16",
        "calendar_window": "Weeks 25 to 32 (Months 7–8)",
        "lead_workstream": "WORKSTREAM-10",
        "deliverables": [
            "Autonomous client-side SQLite replication engine",
            "Bi-directional sync conflict resolution engine",
            "ClickHouse OLAP lakehouse and Superset dashboards",
            "Zero-trust VAPT security remediation and DR dry-run"
        ],
        "exit_gate": "QUALITY-GATE-016",
        "status": "APPROVED_SCHEDULE"
    },
    {
        "phase_id": "PROGRAM-PHASE-5",
        "name": "Phase 5: 20-Clinic Field Pilot, Clinical UAT & Municipal Production Rollout",
        "duration_weeks": 4,
        "sprint_range": "SPRINT-17 to SPRINT-18",
        "calendar_window": "Weeks 33 to 36 (Month 9)",
        "lead_workstream": "WORKSTREAM-15",
        "deliverables": [
            "20-clinic physical workstation deployment and inspection",
            "Clinic staff training and live shadow operations",
            "14-day live pilot outpatient trial with 24/7 hypercare",
            "Formal clinical UAT ratification and citywide scale cutover"
        ],
        "exit_gate": "QUALITY-GATE-020",
        "status": "APPROVED_SCHEDULE"
    }
]

PILOT_STAGES = [
    {
        "stage_id": "PILOT-STAGE-1",
        "name": "Clinic Site Selection & Infrastructure Readiness Audit",
        "duration_days": 10,
        "target_window": "Weeks 29 to 30",
        "activities": "Inspect 20 clinics across South, East, and West zones; verify 4G/fiber uplinks, electrical backup, workstation PCs, thermal printers, and barcode scanners.",
        "gate_criteria": "100% of 20 pilot facilities pass infrastructure certification checklist.",
        "owner": "Infrastructure & Field Operations Lead"
    },
    {
        "stage_id": "PILOT-STAGE-2",
        "name": "Staff Onboarding, Credential Provisioning & Sandbox Training",
        "duration_days": 10,
        "target_window": "Weeks 31 to 32",
        "activities": "Provision Keycloak user credentials for 60 clinical staff (20 doctors, 20 nurses, 20 pharmacists); conduct hands-on sandbox workshops using simulated patient cases.",
        "gate_criteria": "100% of pilot staff achieve passing grade on practical workflow assessment.",
        "owner": "Training & Enablement Lead"
    },
    {
        "stage_id": "PILOT-STAGE-3",
        "name": "Shadow Operations & Dry-Run Simulation",
        "duration_days": 5,
        "target_window": "Week 33 (Days 1–5)",
        "activities": "Run parallel digital intake alongside physical paper registers; compare daily totals, reconcile prescription records, and verify offline PWA caching.",
        "gate_criteria": "Zero discrepancies between shadow logs and physical registers over 5 consecutive days.",
        "owner": "Clinical Validation Lead"
    },
    {
        "stage_id": "PILOT-STAGE-4",
        "name": "Live Outpatient Pilot Trial & Hypercare Monitoring",
        "duration_days": 14,
        "target_window": "Weeks 34 to 35",
        "activities": "Primary paperless digital operations across all 20 pilot clinics; 24/7 hypercare war room active; on-site floor support engineers at all clinics.",
        "gate_criteria": "Over 15,000 live patient encounters recorded with >= 99.5% uptime and zero clinical safety defects.",
        "owner": "Program Director & BBMP CMO"
    },
    {
        "stage_id": "PILOT-STAGE-5",
        "name": "UAT Evaluation, Clinical Ratification & Citywide Scale Decision",
        "duration_days": 5,
        "target_window": "Week 36 (Days 1–5)",
        "activities": "Review pilot telemetry, user feedback surveys, and bug reports; convene BBMP Health Steering Committee for formal scale-up authorization.",
        "gate_criteria": "Signed UAT certificate and Cabinet-level authorization for citywide rollout.",
        "owner": "GBA IT Secretary & BBMP Health Commissioner"
    }
]

ROLLOUT_WAVES = [
    {
        "wave_id": "ROLLOUT-WAVE-1",
        "name": "Wave 1: Pilot Cluster (20 Clinics)",
        "clinic_count": 20,
        "zones": ["South Zone (8)", "East Zone (6)", "West Zone (6)"],
        "target_window": "Weeks 33 to 36",
        "support_model": "1 dedicated on-site support engineer per clinic (1:1 ratio)",
        "readiness_gate": "QUALITY-GATE-018",
        "rollback_strategy": "Parallel paper register contingency"
    },
    {
        "wave_id": "ROLLOUT-WAVE-2",
        "name": "Wave 2: Zonal Expansion (100 Clinics)",
        "clinic_count": 100,
        "zones": ["Bommanahalli (25)", "Mahadevapura (25)", "Rajarajeshwarinagar (25)", "Dasarahalli (25)"],
        "target_window": "Months 10 to 11 (Post-Pilot Phase)",
        "support_model": "Mobile roving transit support units (1 engineer per 5 clinics)",
        "readiness_gate": "QUALITY-GATE-020",
        "rollback_strategy": "Zone-isolated deployment rollback"
    },
    {
        "wave_id": "ROLLOUT-WAVE-3",
        "name": "Wave 3: Full Municipal Rollout (Remaining 330+ Clinics)",
        "clinic_count": 330,
        "zones": ["All 8 BBMP Municipal Zones Citywide"],
        "target_window": "Months 12 to 14 (BAU Transition)",
        "support_model": "Permanent 24/7 central NOC/SOC and zonal field dispatch squads",
        "readiness_gate": "QUALITY-GATE-022",
        "rollback_strategy": "Automated canary rolling update with 5-minute circuit breaker"
    }
]

PROGRAM_SCHEDULE_TABLE = [
    {"sprint": "SPRINT-01", "weeks": "W01–W02", "theme": "Foundation Scaffolding & Architecture Readiness", "release": "RELEASE-00", "phase": "PROGRAM-PHASE-1"},
    {"sprint": "SPRINT-02", "weeks": "W03–W04", "theme": "Identity, Authentication & Security Foundation", "release": "RELEASE-00", "phase": "PROGRAM-PHASE-1"},
    {"sprint": "SPRINT-03", "weeks": "W05–W06", "theme": "Patient Registration & Demographics", "release": "RELEASE-01", "phase": "PROGRAM-PHASE-1"},
    {"sprint": "SPRINT-04", "weeks": "W07–W08", "theme": "Patient Search, Repeat Visits & Consent", "release": "RELEASE-01", "phase": "PROGRAM-PHASE-1"},
    {"sprint": "SPRINT-05", "weeks": "W09–W10", "theme": "Token Generation & Queue Management", "release": "RELEASE-01", "phase": "PROGRAM-PHASE-2"},
    {"sprint": "SPRINT-06", "weeks": "W11–W12", "theme": "Clinical Triage, Vitals & Danger Alerts", "release": "RELEASE-02", "phase": "PROGRAM-PHASE-2"},
    {"sprint": "SPRINT-07", "weeks": "W13–W14", "theme": "Doctor Consultation Workbench", "release": "RELEASE-02", "phase": "PROGRAM-PHASE-2"},
    {"sprint": "SPRINT-08", "weeks": "W15–W16", "theme": "Diagnosis & Electronic Prescriptions", "release": "RELEASE-02", "phase": "PROGRAM-PHASE-2"},
    {"sprint": "SPRINT-09", "weeks": "W17–W18", "theme": "Pharmacy Dispensation & FEFO Allocation", "release": "RELEASE-03", "phase": "PROGRAM-PHASE-3"},
    {"sprint": "SPRINT-10", "weeks": "W19–W20", "theme": "Offline-First Resilience & Sync", "release": "RELEASE-04", "phase": "PROGRAM-PHASE-3"},
    {"sprint": "SPRINT-11", "weeks": "W21–W22", "theme": "Laboratory & Point-of-Care Diagnostics", "release": "RELEASE-03", "phase": "PROGRAM-PHASE-3"},
    {"sprint": "SPRINT-12", "weeks": "W23–W24", "theme": "Secondary Referrals & Bilingual SMS", "release": "RELEASE-03", "phase": "PROGRAM-PHASE-3"},
    {"sprint": "SPRINT-13", "weeks": "W25–W26", "theme": "Drug Inventory & Supply Chain", "release": "RELEASE-03", "phase": "PROGRAM-PHASE-4"},
    {"sprint": "SPRINT-14", "weeks": "W27–W28", "theme": "Population Health Analytics & Reporting", "release": "RELEASE-04", "phase": "PROGRAM-PHASE-4"},
    {"sprint": "SPRINT-15", "weeks": "W29–W30", "theme": "AI/ML Clinical Decision Support", "release": "RELEASE-07", "phase": "PROGRAM-PHASE-4"},
    {"sprint": "SPRINT-16", "weeks": "W31–W32", "theme": "ABDM National Interoperability", "release": "RELEASE-07", "phase": "PROGRAM-PHASE-4"},
    {"sprint": "SPRINT-17", "weeks": "W33–W34", "theme": "Zero-Trust Security Hardening & DR", "release": "RELEASE-05", "phase": "PROGRAM-PHASE-5"},
    {"sprint": "SPRINT-18", "weeks": "W35–W36", "theme": "Pilot Validation & Production Cutover", "release": "RELEASE-05", "phase": "PROGRAM-PHASE-5"},
]
