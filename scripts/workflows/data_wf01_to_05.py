#!/usr/bin/env python3
"""
data_wf01_to_05.py
Clean, self-contained domain specifications for Workflows 01 to 05:
  - WF-001: Master Clinic Day Operational Workflow
  - WF-002: Staff Login, Multi-Factor Authentication & Session Management Workflow
  - WF-003: Patient Registration, ABHA Creation & Demographic Intake Workflow
  - WF-004: Patient Search, Multi-Parametric Lookup & Verification Workflow
  - WF-005: Repeat Patient Revisit & Longitudinal Episode Linking Workflow

Exports:
  DATA_WF01_TO_05 (dict mapping 'WF-001'..'WF-005' to enriched 67-section workflow dicts)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_factory import build_workflow_object
from workflow_metadata import WORKFLOW_MAP

def make_wf01_data():
    wf_meta = WORKFLOW_MAP["WF-001"]
    spec = {
        "id": "WF-001", "num": "01", "name": WORKFLOW_MAP["WF-001"]["name"], "domain": WORKFLOW_MAP["WF-001"]["domain"],
        "exec_summary": {
            "purpose": "Governs the complete daily operating lifecycle of an urban Namma Clinic facility, orchestrating multi-role staff synchronization, offline-capable digital queue progression, point-of-care diagnostics, electronic prescribing, pharmacy dispensing, and end-of-day administrative reconciliation from 07:30 to 20:00 IST.",
            "rationale": "Urban primary healthcare centers face extreme morning demand surges, frequent wide-area network drops, and complex inter-station handovers. WF-001 establishes an unbroken chain of operational continuity, ensuring that zero citizens are turned away due to IT failures while enforcing strict clinical audit trails.",
            "clinical_impact": "Enforces clinical safety gates across every station transition: vital signs must be captured before doctor entry; danger signs immediately trigger clinical escalation; allergy cross-checks guard prescribing; and pharmacy dispensing is tied to FEFO inventory batch allocation.",
            "system_impact": "Serves as the master state machine orchestrator for the clinic edge node, binding local SQLite/IndexedDB write-ahead logs, WebSerial thermal printing, local WebSocket signage, and asynchronous cloud sync pipelines into a cohesive resilient edge mesh.",
            "risk_profile": "High operational risk during morning rush hour (08:30-11:00); hardware single points of failure (thermal printer jam, pulse oximeter battery failure); local edge node power loss; and network partition reconciliation backlog."
        },
        "objectives": [
            {"id": "OBJ-WF01-01", "title": "Rapid Clinic Day Initialization", "desc": "Complete edge verification, device self-tests, and morning queue initialization within 15 minutes of facility unlock.", "metric": "Time to First Token < 15 min from unlock", "verification": "Automated system startup audit log timestamp analysis"},
            {"id": "OBJ-WF01-02", "title": "Total Patient Transit Time Optimization", "desc": "Maintain median total transit time (Registration to Pharmacy exit) under 25 minutes for routine non-emergency visits.", "metric": "Median Transit Time <= 25 min", "verification": "Encounter timestamp duration aggregation across all stations"},
            {"id": "OBJ-WF01-03", "title": "Zero Operational Data Loss", "desc": "Guarantee zero loss of clinical, prescription, or dispensing records during wide-area network disconnection.", "metric": "RPO = 0 records lost during 8h network severed", "verification": "Cryptographic hash verification of local vs cloud sync logs"},
            {"id": "OBJ-WF01-04", "title": "Dangerous Deterioration Preemption", "desc": "Detect and route 100% of triage-flagged critical danger signs to the Medical Officer within 60 seconds.", "metric": "Acuity Red Triage Escalation Latency < 60 sec", "verification": "Telemetry timer between triage red flag commit and doctor room audible alarm"}
        ],
        "in_scope": [
            {"area": "Facility Initialization", "desc": "Physical door unlock, solar-UPS power check, Edge Node self-test, local LAN verification, and staff biometric check-in."},
            {"area": "Patient Registration & Triage", "desc": "Bilingual token issuance, ABHA/UHID lookup, physiological vital sign capture, and MEWS clinical acuity scoring."},
            {"area": "Consultation & Diagnostics", "desc": "Outpatient clinical examination, SOAP documentation, ICD-10 coding, point-of-care rapid lab test execution, and e-prescribing."},
            {"area": "Pharmacy & Dispensing", "desc": "Digital prescription receipt, FEFO batch selection, Kannada packaging label printing, patient counseling, and inventory decrement."}
        ],
        "out_of_scope": [
            {"area": "Inpatient Hospitalization", "desc": "Overnight admission and continuous ward nursing care; out of scope for day-clinic OPD.", "handoff": "Referral transfer to Taluk / District Hospital"},
            {"area": "Surgical Interventions", "desc": "Major operating theater surgical procedures; clinic restricted to minor wound suturing.", "handoff": "Emergency 108 ambulance dispatch to Bowring / Victoria Hospital"}
        ],
        "actors": [
            {"id": "ACT-WF01-01", "type": "Human", "name": "Clinic Coordinator", "responsibilities": "Facility unlock, queue setup, token issuance, day-end reconciliation.", "permissions": "Registration Create/Update, Token Mint, Session Close", "failure_duty": "Switches to manual paper tokens if printer fails.", "inputs": "Citizen declarations, physical ID cards", "decisions": "Determines queue priority category.", "outputs": "Printed token slips, daily closing ledger", "recovery": "Re-checks physical counts upon variance."},
            {"id": "ACT-WF01-02", "type": "Human", "name": "Staff Nurse", "responsibilities": "Cold chain temperature logging, vital signs triage, emergency crash cart check.", "permissions": "Triage Vitals Create, Acuity Score Commit, Danger Broadcast", "failure_duty": "Initiates manual CPR upon patient collapse.", "inputs": "Digital monitor readings (BP, SpO2, Pulse, Temp)", "decisions": "Assigns triage acuity color (Green, Yellow, Red).", "outputs": "Committed triage vital records, danger alarms", "recovery": "Re-reads manual blood pressure cuff on sensor error."},
            {"id": "ACT-WF01-03", "type": "Human", "name": "Medical Officer", "responsibilities": "Outpatient clinical examination, diagnosis, e-prescribing, lab ordering, referral authorization.", "permissions": "Encounter Full, Diagnosis Signoff, Rx Signature", "failure_duty": "Manages resuscitation emergencies; signs verbal orders retrospectively.", "inputs": "Longitudinal history, triage vitals, lab reports", "decisions": "Formulates clinical diagnosis and drug regimen.", "outputs": "Signed clinical encounter, e-prescription, lab orders", "recovery": "Signs emergency verbal orders within 2 hours."}
        ],
        "personas": [
            {"id": "PERSONA-001", "name": "Sister Bhavani Gowda", "role": "Frontline Staff Nurse", "env": "High-noise, high-footfall triage station in Govindaraja Nagar Namma Clinic.", "goals": "Rapidly capture accurate vitals without manual paper transcription.", "pain_points": "System freezes during internet drops; clunky UI menus.", "adaptations": "High-contrast touch UI with single-screen vitals entry."},
            {"id": "PERSONA-002", "name": "Dr. Manjunath Swamy", "role": "Senior Medical Officer", "env": "Consultation chamber conducting 70+ visits per shift.", "goals": "Review previous visit history in under 5 seconds; prescribe generic drugs safely.", "pain_points": "Repetitive manual data entry; delayed lab results.", "adaptations": "Keyboard accelerators and 1-click favorite prescription sets."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "Patient, Vitals, Triage, Queue", "create": "Vitals, Triage, Token", "update": "Triage Vitals", "delete": "None", "override": "Emergency Triage Preemption", "signoff": "Triage Record"},
            {"role": "ROLE-002", "title": "Medical Officer", "read": "Complete Patient Profile", "create": "Encounter, Rx, Lab Order", "update": "Clinical Notes", "delete": "None", "override": "Clinical Override", "signoff": "Encounter & Prescription"},
            {"role": "ROLE-006", "title": "Clinic Coordinator", "read": "Registration, Queue, Census", "create": "Patient File, Token", "update": "Demographics", "delete": "None", "override": "Queue Re-tagging", "signoff": "Day Closing Census"}
        ],
        "preconditions": [
            {"id": "PRE-WF01-01", "desc": "Clinic edge server powered on with battery backup UPS operational.", "check": "Edge system daemon reports battery status OK", "on_fail": "Trigger acoustic UPS warning; halt non-essential peripherals."},
            {"id": "PRE-WF01-02", "desc": "Pharmacy cold-chain vaccine refrigerator temperature logged between +2C and +8C.", "check": "Digital temperature sensor log < 8C and > 2C", "on_fail": "Alarm Nurse & Pharmacist; quarantine biologicals."}
        ],
        "triggers": [
            {"id": "TRIG-WF01-01", "class": "User Trigger", "event": "Clinic Coordinator clicks 'Open Daily Clinic Session'", "source": "Registration UI Portal", "payload": "{ clinic_id, coordinator_id, shift: 'MORNING' }", "latency": "< 500ms to session active state"},
            {"id": "TRIG-WF01-02", "class": "Emergency Trigger", "event": "Triage vital signs breach critical MEWS danger threshold (Red Acuity)", "source": "Triage Screen Save", "payload": "{ patient_id, token_no, acuity: 'RED', mews: 6 }", "latency": "< 500ms to audible room klaxon"}
        ],
        "inputs": [
            {"name": "clinic_session_id", "type": "UUIDv4", "req": "Mandatory", "source": "Edge Orchestrator", "val": "Unique session key for clinic day", "priv": "Operational", "enc": "Plaintext indexed", "ex": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d", "on_err": "Fatal session startup abort"},
            {"name": "triage_systolic_bp", "type": "Integer", "req": "Mandatory", "source": "Staff Nurse", "val": "50 <= SBP <= 260 mmHg", "priv": "PHI", "enc": "AES-256 at rest", "ex": "138", "on_err": "Reject out-of-range value; prompt re-measurement"},
            {"name": "triage_spo2", "type": "Integer", "req": "Mandatory", "source": "Staff Nurse", "val": "50 <= SpO2 <= 100 percentage", "priv": "PHI", "enc": "AES-256 at rest", "ex": "98", "on_err": "Trigger immediate oxygen probe re-check"}
        ],
        "outputs": {
            "success": [
                {"name": "Daily Clinic Operational Session Record", "desc": "Closed and cryptographically sealed daily clinic ledger.", "format": "JSON-LD & PDF Signed Archive", "recipient": "Central BBMP Health Information Warehouse"},
                {"name": "Patient Clinical Encounter Records", "desc": "Structured longitudinal consultation summaries for all treated citizens.", "format": "FHIR R4 Composition Bundles", "recipient": "ABDM Health Information Provider (HIP) Repository"}
            ],
            "partial": [
                {"name": "Unsynchronized Offline Transaction Spool", "desc": "Local mutations buffered during WAN network outages awaiting cloud sync.", "format": "Encrypted SQLite WAL Journal", "fallback": "Automatic retry upon network reconnection"}
            ],
            "error": [
                {"name": "Morning System Initialization Failure Report", "desc": "Generated when edge server or key peripheral fails pre-flight check.", "code": "ERR-WF01-INIT-001", "msg": "Clinic Edge Node Peripheral Failure. Switch to Manual Backup."}
            ],
            "events": [
                {"topic": "namma.clinic.ops.session_opened", "desc": "Published when morning clinic session is successfully activated.", "schema": "{ clinic_id, session_id, open_timestamp, staff_roster }"}
            ]
        },
        "happy_path": [
            {"title": "Facility Door Unlock & Power Verification", "actor": "Clinic Coordinator (`ACT-WF01-01`)", "input": "Physical key, biometric reader scan, AC mains electrical switch toggle", "action": "Unlocks clinic facility at 07:30 IST, activates solar-UPS main power breakers, and observes edge server LED status.", "sys_behavior": "Edge server boots up, executes BIOS power-on self-test, initializes local systemd background services.", "validation": "`CHECK_UPS_BATTERY_CHARGE >= 90%` and `CHECK_SERVER_BOOT == SUCCESS`", "db_effect": "Inserts row in `system_event_logs` with event `FACILITY_UNLOCKED`", "ui_effect": "Registration kiosk terminal screen lights up with Namma Clinic OS logo.", "api_effect": "POST /api/v1/system/boot-telemetry", "audit_effect": "WFAUDIT-001-001 (System Boot Initialized)", "output": "Facility powered; Edge node operational", "next_state": "WFSTATE-001-002", "failure_possibility": "UPS failure; server storage failure; power trip."},
            {"title": "Automated Edge Peripheral Self-Test", "actor": "Edge Orchestrator", "input": "Hardware device probes (WebSerial, USB, HDMI, Ethernet/Wi-Fi)", "action": "Orchestrator daemon queries connected devices: thermal printer, barcode scanner, webcam, digital display TV.", "sys_behavior": "Executes loopback queries on `/dev/ttyUSB0`, verifies HDMI CEC connection to waiting room display board.", "validation": "`DEVICE_STATUS(printer) == READY` and `DEVICE_STATUS(tv_display) == CONNECTED`", "db_effect": "Updates `clinic_hardware_inventory` status columns to `ONLINE`", "ui_effect": "Coordinator dashboard displays green checkmarks across all peripheral hardware tiles.", "api_effect": "GET /api/v1/hardware/status", "audit_effect": "WFAUDIT-001-002 (Hardware Self-Test Passed)", "output": "Hardware diagnostic green report", "next_state": "WFSTATE-001-003", "failure_possibility": "Thermal printer out of paper; USB cable disconnected."},
            {"title": "Staff Morning Biometric Check-In & Roster Lock", "actor": "Staff Nurse & Doctor", "input": "Biometric fingerprint on USB sensor and staff PIN credentials", "action": "Frontline clinical staff check in on terminal; system matches biometric templates against local encrypted cache.", "sys_behavior": "Validates credentials, checks duty roster schedule, issues role-bound session JWT with 15-minute inactivity timer.", "validation": "`STAFF_ROLE IN ['DOCTOR', 'NURSE', 'PHARMACIST']` and `SCHEDULED_TODAY == TRUE`", "db_effect": "Inserts row in `staff_attendance_sessions` with check-in timestamp", "ui_effect": "Unlocks Doctor Room terminal and Triage Nurse tablet with user profile avatar.", "api_effect": "POST /api/v1/auth/staff-checkin", "audit_effect": "WFAUDIT-001-003 (Staff Check-In Recorded)", "output": "Authenticated clinical sessions", "next_state": "WFSTATE-001-004", "failure_possibility": "Biometric mismatch; unassigned staff member; network auth timeout."},
            {"title": "Cold-Chain Vaccine Refrigerator Safety Check", "actor": "Staff Nurse (`ACT-WF01-02`)", "input": "Digital temperature logger reading from vaccine refrigerator", "action": "Inspects thermometer, verifies temperature within mandated safe biological envelope (+2.0C to +8.0C), enters value.", "sys_behavior": "Validates temperature against safety limits; if within limits, unlocks vaccine inventory for clinical orders.", "validation": "`2.0 <= TEMP_CELSIUS <= 8.0`", "db_effect": "Inserts row in `cold_chain_temperature_logs` with nurse digital signature", "ui_effect": "Cold chain widget updates to green badge: 'Cold Chain Normal: 4.2C'.", "api_effect": "POST /api/v1/inventory/cold-chain-log", "audit_effect": "WFAUDIT-001-004 (Cold Chain Verified)", "output": "Vaccine safety clearance certificate", "next_state": "WFSTATE-001-005", "failure_possibility": "Temperature breach (>8C); sensor battery flat."},
            {"title": "Queue Management & Waiting Room Signage Startup", "actor": "Clinic Coordinator (`ACT-WF01-01`)", "input": "Click 'Start OPD Queue' button on Coordinator console", "action": "Initializes daily queue counters (starts at Token 001), resets display board, tests audio chime in Kannada.", "sys_behavior": "WebSocket channel `ws://edge-node:8080/queue/display` sends greeting broadcast to waiting lounge TV.", "validation": "`QUEUE_INITIALIZED == TRUE` and `DAY_COUNTER == 1`", "db_effect": "Creates new row in `daily_queue_sessions` with state `ACTIVE`", "ui_effect": "Waiting room TV shows: 'Namma Clinic Welcome - OPD Open. Please collect token.' in Kannada & English.", "api_effect": "POST /api/v1/queue/session/init", "audit_effect": "WFAUDIT-001-005 (Queue Session Activated)", "output": "Active digital queue engine", "next_state": "WFSTATE-001-005", "failure_possibility": "WebSocket connection failure; audio speaker muted."}
        ],
        "alternate_flows": [
            {
                "id": "WFALT-001-001", "title": "Citizen Arrives Without Mobile Phone",
                "condition": "Citizen does not possess or remember an active mobile phone number during registration.",
                "from_step": "WFSTEP-001-005",
                "steps": [
                    "Coordinator toggles 'No Mobile Phone Available' checkbox on registration form.",
                    "System generates local clinic-scoped identifier and prints physical thermal token slip with scannable QR code.",
                    "Coordinator explains that all prescription and queue details are encoded directly on the physical paper token slip.",
                    "Patient proceeds directly to triage queue using physical token slip without SMS dependency."
                ],
                "rejoin": "Rejoins main flow at Triage Vitals Measurement upon condition clearance.",
                "audit": "WFAUDIT-001-ALT01 (Non-Mobile Citizen Intake)"
            }
        ],
        "exception_flows": [
            {
                "id": "WFEX-001-001", "title": "Edge Server Hardware Boot Failure",
                "trigger": "Edge server BIOS hardware check fails during morning startup.",
                "detection": "No heartbeat on LAN; monitor shows hardware error beep code.",
                "containment": "Coordinator activates Secondary Standby Edge Terminal (Mini-PC) running hot database replica.",
                "msg_en": "Primary Edge Server hardware fault. Failover to Standby Edge Terminal in progress.",
                "msg_kn": "ಪ್ರಾಥಮಿಕ ಸರ್ವರ್ ದೋಷ. ಬ್ಯಾಕಪ್ ಸಿಸ್ಟಮ್‌ಗೆ ಬದಲಾಯಿಸಲಾಗುತ್ತಿದೆ.",
                "recovery": "Standby terminal assumes local master IP 192.168.1.100; loads latest hourly snapshot.",
                "audit": "WFAUDIT-001-EX01", "severity": "CRITICAL"
            }
        ],
        "emergency_flow": {
            "triggers": "Patient sudden cardiac arrest, maternal postpartum hemorrhage, severe anaphylactic shock, acute status epilepticus.",
            "escalation": "Staff Nurse hits wall-mounted Code Red push button. Triage and Doctor screens instantly flash persistent pulsing red banner with audible alarm.",
            "preemption": "Immediately interrupts doctor consultation queue. All routine queue progression paused.",
            "bypass_rules": "Bypasses standard registration, ABHA verification, demographic entry, and token printing.",
            "safety_controls": "Emergency drug crash cart unlocked electronically. Verbal physician orders permitted.",
            "reconciliation": "Medical Officer and Nurse review and sign off retrospective resuscitation encounter chart within 2 hours.",
            "audit_event": "WFAUDIT-001-EMERGENCY", "signoff_sla": "2 hours post-incident sign-off"
        },
        "states": [
            {"name": "FACILITY_LOCKED", "desc": "Clinic doors locked; server in low-power surveillance mode.", "allowed": "Biometric unlock, power check", "prohibited": "Queue operations", "actor": "Clinic Coordinator"},
            {"name": "SYSTEM_PREFLIGHT", "desc": "Edge node booting; hardware self-tests verifying printers, screens, UPS.", "allowed": "Diagnostic checks", "prohibited": "Token issuance", "actor": "Edge Orchestrator"},
            {"name": "STAFF_AUTHENTICATION", "desc": "Morning muster; clinical staff authenticating credentials.", "allowed": "Biometric / PIN login", "prohibited": "Patient examination", "actor": "Staff Nurse & Doctor"},
            {"name": "CLINIC_SESSION_ACTIVE", "desc": "Standard clinic operating hours; queues active across all stations.", "allowed": "Full registration, triage, consultation, lab, pharmacy", "prohibited": "Unreconciled session close", "actor": "All Clinic Staff"}
        ],
        "transitions": [
            {"from_state": "WFSTATE-001-001", "event": "Unlock Facility & Power On", "actor": "Coordinator", "condition": "Physical key used, UPS powered on", "validation": "Power check positive", "to_state": "WFSTATE-001-002", "side_effects": "Server boots, logs startup", "audit": "WFAUDIT-001-TR01"},
            {"from_state": "WFSTATE-001-002", "event": "Peripherals Self-Test Passed", "actor": "Orchestrator", "condition": "Printers, screens responsive", "validation": "Hardware diagnostic OK", "to_state": "WFSTATE-001-003", "side_effects": "Displays login prompt", "audit": "WFAUDIT-001-TR02"},
            {"from_state": "WFSTATE-001-003", "event": "Clinical Roster Logged In", "actor": "Doctor & Nurse", "condition": "Biometric match and valid credentials", "validation": "Auth claims verified", "to_state": "WFSTATE-001-004", "side_effects": "Unlocks clinical stations", "audit": "WFAUDIT-001-TR03"}
        ],
        "decision_tables": [
            {
                "id": "WFDEC-001-001", "title": "Morning Clinic Operational Readiness Evaluation",
                "desc": "Determines whether the clinic can safely open its doors to citizens based on prerequisite infrastructure checks.",
                "conditions": ["Edge Server Online", "UPS Power >= 90%", "Doctor Present", "Nurse Present"],
                "actions": ["Permit Public Intake", "Initiate Full Queue", "Trigger Yellow Warning", "Halt Clinic Opening"],
                "rows": [
                    {"rule": "R1", "cond_vals": ["YES", "YES", "YES", "YES"], "act_vals": ["YES", "YES", "NO", "NO"]},
                    {"rule": "R2", "cond_vals": ["YES", "YES", "NO", "YES"], "act_vals": ["NO", "NO", "YES", "NO"]},
                    {"rule": "R3", "cond_vals": ["NO", "ANY", "ANY", "ANY"], "act_vals": ["NO", "NO", "YES", "YES"]}
                ]
            }
        ],
        "validation_rules": [
            {"id": "WFVAL-001-001", "field": "facility_unlock_time", "expr": "07:00 <= unlock_time <= 08:30 IST", "code": "ERR-VAL-001", "msg_en": "Facility unlock time outside standard opening window.", "msg_kn": "ಕ್ಲಿನಿಕ್ ತೆರೆಯುವ ಸಮಯ ನಿಗದಿತ ಮಿತಿಯ ಹೊರಗಿದೆ.", "recovery": "Enter supervisor override justification note.", "test_ref": "WFTEST-001-001"}
        ],
        "business_rules": [
            {"id": "BRULE-WF01-001", "title": "Zero Out-of-Pocket Expense Mandate", "req": "BRULE-001", "spec": "All primary outpatient consultations, point-of-care lab tests, and formulary medications shall be provided to citizens 100% free of charge.", "enforcement": "System blocks any fee creation on standard OPD workflows; billing module disabled.", "consequence": "Any financial extortion attempt triggers immediate administrative audit alarm."}
        ],
        "clinical_rules": [
            {"id": "CR-WF01-001", "title": "Mandatory Triage Vitals Gate Before Doctor Consultation", "req": "CR-001", "rationale": "Unscreened walk-in patients may harbor occult severe hypertension, hypoxia, or sepsis.", "logic": "Token cannot enter Doctor Queue until BP, SpO2, Pulse, and Temp are committed by Staff Nurse.", "override_policy": "Emergency Code Red exception bypasses this gate directly to resuscitation room.", "safety_invariant": "Zero routine outpatient encounters may be documented without validated triage vital signs."}
        ],
        "operational_rules": [
            {"id": "OR-WF01-001", "title": "Mandatory Dual-Signoff for Day-End Ledger Closeout", "req": "OR-001", "mandate": "Both the Medical Officer and Clinic Coordinator must enter digital signatures to seal the daily operating ledger.", "boundary": "Clinic premises at end of day between 19:30 and 20:30 IST.", "exception": "If doctor is incapacitated, Zonal Health Officer may sign remotely after phone verification."}
        ],
        "security_controls": [
            {"domain": "Authentication", "id": "SEC-WF01-01", "spec": "Staff login protected by Argon2id / bcrypt password hashing with TOTP multi-factor challenge.", "param": "Argon2id (m=64MB, t=3, p=4)", "threat": "Credential stuffing & brute force", "compliance": "SECR-001"}
        ],
        "privacy_controls": [
            {"principle": "Purpose Limitation", "id": "PRIV-WF01-01", "spec": "Citizen health data collected strictly for outpatient clinical care, pharmacy dispensing, and statutory disease surveillance.", "invariant": "No commercial monetization or third-party sharing", "right": "Right to be informed (DPDP Act 2023 Sec 5)"}
        ],
        "offline_behavior": {
            "online_mode": "Real-time bidirectional synchronization with BBMP central cloud; ABHA KYC verification via ABDM gateway; SMS dispatch via telecom gateway.",
            "detection_latency": "Edge network monitor detects WAN failure within 3 consecutive 1-second ICMP ping drops.",
            "local_storage": "Encrypted local SQLite database holding complete 90-day patient historical cache, full EML drug formulary, and ICD-10 diagnostic index.",
            "queue_mechanics": "Local write-ahead log (WAL) records every mutation; assigns deterministic UUIDv4 and Lamport timestamps; queues records in `offline_mutation_spool`.",
            "degraded_scope": "Full clinic operations continue unhindered: registration with provisional UHID, vital capture, doctor consultation, lab tests, pharmacy dispensing, and thermal slip printing.",
            "sync_convergence": "Upon WAN reconnection, edge daemon replays mutation spool sequentially; cloud coordinator resolves conflicts using deterministic clinician-authority rules.",
            "conflict_invariants": "Doctor clinical decisions committed offline are never overwritten by administrative cloud updates; unique UUID keys eliminate ID collisions."
        },
        "diagrams": {
            "data_flow": """flowchart TD
    Actor_Citizen["Citizen Patient"] -->|Presents at Desk| UI_Reg["Registration Kiosk UI"]
    UI_Reg -->|Mint Token| Edge_Daemon["Edge Orchestrator Daemon"]
    Edge_Daemon -->|Store Token| DB_Local[("Encrypted Local SQLite DB")]
    Edge_Daemon -->|Print Slip| HW_Printer["Thermal Slip Printer"]
    Edge_Daemon -->|Push Token| Display_TV["Waiting Lounge TV Screen"]
    Edge_Daemon -.->|Sync Batch| Cloud_Gateway["Central API Gateway"]""",
            "sequence": """sequenceDiagram
    autonumber
    actor C as Citizen Patient
    actor N as Staff Nurse
    actor D as Medical Officer
    participant E as Edge Orchestrator
    participant DB as Local SQLite DB
    C->>N: 1. Arrives at Desk & requests token
    N->>E: 2. Input details & select Senior Priority
    E->>DB: 3. Insert Token SNR-001 (Queued)
    E-->>C: 4. Dispense printed thermal token slip
    N->>E: 5. Measure & commit BP, SpO2, Pulse, Temp
    D->>E: 6. Click 'Call Next Patient'
    E-->>C: 7. Audio chime: Token SNR-001 to Room 1""",
            "activity": """flowchart TD
    Start([07:30 Facility Unlock]) --> CheckPower{UPS Power OK?}
    CheckPower -- Yes --> BootServer[Boot Edge Server & Run Self-Test]
    BootServer --> CheckColdChain{Cold Chain 2-8C?}
    CheckColdChain -- Yes --> OpenSession[Activate Clinic Daily Queue Session]
    OpenSession --> PatientArrives[Citizen Arrives at Registration]
    PatientArrives --> IssueToken[Issue Bilingual Priority Token]
    IssueToken --> End([Enqueued to Triage])""",
            "state": """stateDiagram-v2
    [*] --> FACILITY_LOCKED
    FACILITY_LOCKED --> SYSTEM_PREFLIGHT: Unlock Door & Power On
    SYSTEM_PREFLIGHT --> STAFF_AUTHENTICATION: Hardware Checks Passed
    STAFF_AUTHENTICATION --> CLINIC_SESSION_ACTIVE: Staff Logged In
    CLINIC_SESSION_ACTIVE --> [*]"""
        },
        "data_flow_nodes": [
            {"name": "UI_Reg", "desc": "Registration Kiosk Touchscreen UI running in Chromium kiosk mode.", "protocol": "HTTPS / Local IPC", "encryption": "TLS 1.3"},
            {"name": "Edge_Daemon", "desc": "Local Go / Node edge daemon managing queue, hardware serial links, and DB.", "protocol": "HTTP / WebSockets", "encryption": "Loopback IPC"}
        ],
        "failure_tree": [
            {"id": "FT-001-001", "cat": "Hardware", "root": "Thermal paper jam in registration printer", "vector": "Mechanical roller slip", "impact": "Prevents physical token printing", "detection": "ESC/POS status query error", "mitigation": "Alert screen modal; reprint option"}
        ],
        "recovery_procedures": [
            {"id": "REC-WF01-01", "title": "Edge Server Database Corruption Recovery", "trigger": "SQLite reports file format error upon boot.", "containment": "Orchestrator moves corrupted DB to quarantine.", "steps": ["Locate latest valid hourly snapshot.", "Execute integrity check.", "Restore snapshot and reapply WAL log.", "Start edge daemon."], "rollback": "Rolls back uncommitted state.", "resumption": "Staff resume operations.", "audit": "WFAUDIT-001-REC01"}
        ],
        "audit_events": [
            {"id": "WFAUDIT-001-001", "event": "FACILITY_UNLOCKED", "actor": "Coordinator", "meta": "{ clinic_id, timestamp }", "state_before": "LOCKED", "state_after": "UNLOCKED", "hmac": "HMAC-SHA256", "retention": "7 Years", "compliance": "DPDP / ISO 27001"}
        ],
        "notifications": [
            {"id": "WFNOTIF-001-01", "trigger": "Token Generated", "recipient": "Patient", "channel": "SMS / WhatsApp", "text_en": "Welcome to Namma Clinic. Your token is SNR-001.", "text_kn": "ನಮ್ಮ ಕ್ಲಿನಿಕ್‌ಗೆ ಸುಸ್ವಾಗತ. ನಿಮ್ಮ ಟೋಕನ್ ಸಂಖ್ಯೆ SNR-001.", "priority": "High", "retry": "1 retry", "fallback": "Thermal Slip"}
        ],
        "planned_apis": [
            {"id": "PLANNED-API-001-01", "method": "POST", "path": "/api/v1/ops/session/init", "desc": "Initializes daily clinic operating session.", "scope": "ops:session:write", "req_schema": "{\n  \"clinic_id\": \"uuid\",\n  \"shift_type\": \"MORNING\"\n}", "res_schema": "{\n  \"session_id\": \"uuid\",\n  \"status\": \"ACTIVE\"\n}", "errors": "400 Bad Request, 401 Unauthorized", "idempotency": "Mandatory", "rate_limit": "5 req/min", "offline_support": "Local execution on edge server"}
        ],
        "planned_db": [
            {"id": "PLANNED-DB-001-01", "table": "clinic_daily_sessions", "purpose": "Manages operational lifecycle of each daily clinic opening.", "pk": "session_id (UUID)", "fks": "coordinator_id -> users", "cols": [
                {"name": "session_id", "type": "UUID", "null": "NOT NULL", "notes": "Primary Key"},
                {"name": "clinic_id", "type": "VARCHAR(36)", "null": "NOT NULL", "notes": "Clinic ID"},
                {"name": "status", "type": "VARCHAR(30)", "null": "NOT NULL", "notes": "ACTIVE | CLOSED"}
            ], "indexes": "INDEX(clinic_id, status)", "concurrency": "Optimistic Locking", "retention": "10 years"}
        ],
        "planned_ui": [
            {"id": "PLANNED-UI-001-01", "screen": "Morning Preflight Dashboard", "route": "/ops/opening", "persona": "Clinic Coordinator", "components": "Hardware checklist, battery gauge, temp log, 'Start Session' button.", "states": "Initial, Validating, Ready, Active.", "validations": "Hardware checks must be green.", "a11y": "Keyboard accessible.", "localization": "Kannada parity.", "offline_ui": "Shows offline banner."}
        ],
        "backend_reqs": {
            "domain_services": "Orchestrates SessionManager, QueueEngine, TriageService.",
            "transactions": "Enforces strict ACID transaction boundaries.",
            "async_workers": "Background workers handle printing, WebSockets, and sync.",
            "circuit_breakers": "Fails open to local offline database after 3 timeouts."
        },
        "integrations": [
            {"id": "INT-WF01-01", "system": "BBMP Central Cloud", "protocol": "mTLS REST", "payload": "Census bundles", "direction": "Outbound", "timeout": "10 sec", "fallback": "Local SQLite WAL"}
        ],
        "reports": [
            {"id": "REP-WF01-01", "title": "Daily OPD Census Report", "freq": "Daily at 20:00", "audience": "Medical Officer", "grain": "Per clinic, per hour", "ref": "REP-001"}
        ],
        "analytics": [
            {"id": "ANL-WF01-01", "kpi": "Median Transit Time", "formula": "MEDIAN(exit - entry)", "dimensions": "Category", "target": "<= 25 min", "alert": "Transit > 40 min"}
        ],
        "ai_reqs": {
            "id": "AIR-WF01-01", "purpose": "Advisory Sepsis Deterioration Risk Prediction", "features": "Age, vitals, symptoms",
            "output_signal": "Sepsis Risk Score (0-1)", "confidence": "Flagged if score >= 0.72", "explainability": "Explains contributor vitals.",
            "authority": "Advisory only; nurse confirms.", "audit": "WFAUDIT-001-AI01"
        },
        "stride_threats": [
            {"id": "STRIDE-WF01-01", "cat": "Spoofing", "asset": "Staff Login", "scenario": "Attacker guesses password.", "likelihood": "Medium", "impact": "High", "mitigation": "TOTP MFA.", "residual": "Low", "test_ref": "WFTEST-001-001"}
        ],
        "linddun_threats": [
            {"id": "LINDDUN-WF01-01", "cat": "Linkability", "asset": "Token Number", "vector": "Observer links token to neighbor.", "likelihood": "Medium", "impact": "Low", "mitigation": "Tokens reset daily.", "compliance": "DPDP Act"}
        ],
        "performance": {
            "e2e_latency": "Token print < 1.5s.", "ui_render": "UI render < 100ms.",
            "db_budget": "SQLite query < 15ms.", "concurrency": "50 connections.",
            "payload": "Payload < 8KB.", "hardware": "RAM < 250MB."
        },
        "availability": {
            "sla": "99.9% uptime.", "rto": "< 5 min.", "rpo": "0 lost.",
            "offline_autonomy": "72h offline autonomy.", "failover": "Dual-homed network."
        },
        "accessibility": {
            "screen_reader": "ARIA labels present.", "contrast": "Contrast >= 4.5:1.",
            "keyboard": "Full keyboard navigation.", "touch": "Targets >= 48px.", "cognitive": "Clean visual design."
        },
        "localization": {
            "clinical_terms": "English/Latin with Kannada vernacular.", "printed_material": "Kannada UTF-8 slips.",
            "audio_prompts": "Studio-recorded Kannada voice."
        },
        "test_gates": [
            {"level": "Unit Testing", "scope": "Token generator, MEWS scoring", "tooling": "PyTest", "coverage": ">= 90%", "gate": "Zero failures"},
            {"level": "E2E BDD", "scope": "Complete clinic day journey", "tooling": "Playwright", "coverage": "100%", "gate": "Green run"}
        ],
        "bdd_scenarios": [
            {
                "id": "WFTEST-001-001", "title": "Successful Routine Patient Journey from Registration to Pharmacy",
                "category": "Happy Path", "priority": "P0",
                "given": "the Namma Clinic operating day is active and edge node is online",
                "given_ands": ["Staff Nurse and Medical Officer are authenticated at their stations"],
                "when": "a 68-year-old citizen arrives and requests a general outpatient checkup",
                "when_ands": ["Coordinator issues Senior Citizen token SNR-001", "Nurse records BP 138/88 and SpO2 98% with MEWS 1", "Doctor diagnoses Essential Hypertension and prescribes Amlodipine 5mg x 30 days"],
                "then": "Pharmacist scans batch barcode and dispenses 30 tablets with Kannada dosage counseling",
                "then_ands": ["the patient encounter is marked completed within 20 minutes total transit time", "an immutable audit record WFAUDIT-001-012 is written to the cryptographic ledger"]
            }
        ],
        "acceptance_criteria": [
            {"id": "AC-WF-001-001", "criterion": "Facility unlock to first token in < 15 min.", "method": "Timestamp check", "threshold": "p95 <= 15m", "gate": "Core Gate"}
        ],
        "dependencies": [
            {"id": "WFDEP-001-01", "upstream": "WF-002", "downstream": "WF-001", "nature": "Staff Authentication", "blocking": "BLOCKING", "impact": "Cannot open without staff.", "resilience": "Offline cached login."}
        ],
        "critical_path": {
            "path": "Unlock -> Preflight -> Staff Login -> Cold Chain -> Queue Init -> OPD -> Closeout.",
            "bottleneck": "Doctor Consultation Chamber (6-8 min/patient).",
            "load_balancing": "Nurse triage pre-populates vitals.",
            "recovery_bottlenecks": "Re-syncing 100+ offline records."
        },
        "rollback_strategy": {
            "db_rollback": "Atomic ACID rollback.", "saga_compensation": "Compensate dispense restores stock.",
            "notification_reversal": "Send correction SMS.", "audit_preservation": "Append-only WORM log.",
            "offline_rollback": "Quarantine invalid offline mutations."
        },
        "idempotency": {
            "key_schema": "UUIDv4 on clinic+station+time.", "cache_store": "LRU in-memory cache.",
            "replay_behavior": "Returns cached response.", "ttl": "24 hours.", "offline_replay": "Cloud deduplicates safely."
        },
        "concurrency": {
            "occ": "Optimistic locking on charts.", "pessimistic": "Row-level locks on stock.",
            "queue_locking": "Atomic sequence counter.", "deadlock_policy": "Alphabetical table locking."
        },
        "invariants": [
            {"id": "INVARIANT-WF-001-01", "statement": "Every patient admitted to doctor chamber must have validated triage vitals.", "scope": "Consultation Queue", "enforcement": "API blocks missing triage.", "consequence": "Hard blocking error."}
        ],
        "observability": [
            {"cat": "Metric", "name": "namma_clinic_active_patients_gauge", "type": "Gauge", "labels": "clinic_id", "target": "Prometheus", "alert": "Patients > 80"}
        ],
        "runbook": {
            "morning_sop": "Arrive 07:30. Unlock door, check UPS, boot server, verify cold chain, staff login, start queue.",
            "live_sop": "Maintain queue order, assist elderly, watch for Code Red alarms, conduct midday handover.",
            "troubleshooting_sop": "If broadband drops: continue in offline mode. If printer jams: reload paper roll.",
            "closing_sop": "19:30 announce last token, doctor signs all encounters, seal daily ledger, lock doors."
        },
        "sla_slo": [
            {"name": "OPD Service Uptime", "target": "99.9%", "window": "Monthly", "warning": "< 99.5%", "escalation": "DevOps alerted"}
        ],
        "traceability": [
            {"req": "BR-001", "type": "Business Req", "step": "WFSTEP-001-005", "state": "WFSTATE-001-004", "api": "PLANNED-API-001-01", "db": "PLANNED-DB-001-01", "ui": "PLANNED-UI-001-01", "test": "WFTEST-001-001"}
        ],
        "open_questions": [
            {"id": "OQ-WF01-01", "subject": "Sunday Half-Day Clinic", "query": "Should clinics open for emergency triage on Sundays?", "impact": "Staffing schedule.", "owner": "BBMP Health", "milestone": "M2"}
        ],
        "assumptions": [
            {"id": "ASM-WF01-01", "cat": "Hardware", "statement": "Clinic has 4-hour solar UPS.", "status": "CONFIRMED", "risk": "Power generator required."}
        ],
        "risks": [
            {"id": "RSK-WF01-01", "desc": "Morning surge exceeds seating.", "prob": "High", "impact": "Medium", "mitigation": "Outdoor canopy seating.", "contingency": "Deploy roving ANM.", "owner": "Coordinator"}
        ],
        "change_impact": [
            {"vector": "Operating Hours Extension", "scenario": "Clinic expanded to night shifts.", "components": "Roster, shift handover", "severity": "MEDIUM", "testing": "Shift tests"}
        ],
        "definition_of_ready": [
            {"id": "DOR-WF01-01", "criterion": "Workflow specification approved by Architect.", "artifact": "WF-001 Doc", "signoff": "Lead Architect"}
        ],
        "definition_of_done": [
            {"id": "DOD-WF01-01", "criterion": "100% pass on automated BDD test suite.", "method": "Automated report", "benchmark": "100% pass"}
        ],
        "related_workflows": [
            {"rel": "Authentication Dependency", "id": "WF-002", "name": "Staff Login Workflow", "interface": "JWT Session Auth"}
        ]
    }
    return build_workflow_object(spec)

def make_wf02_data():
    wf_meta = WORKFLOW_MAP["WF-002"]
    wfid = "WF-002"
    wfnum = "02"

    spec = {
        "id": wfid, "num": wfnum, "name": wf_meta["name"], "domain": wf_meta["domain"],
        "exec_summary": {
            "purpose": "Governs frontline clinical and administrative personnel authentication, multi-factor verification (TOTP/SMS), role claim issuance, cryptographic session token minting (JWT), inactivity auto-lock (15 min), brute-force defense, emergency offline PIN verification using locally salted scrypt hashes, and concurrent session revocation.",
            "rationale": "Clinical workstations in busy public primary care clinics handle highly sensitive Protected Health Information (PHI) under the DPDP Act 2023. Strict authentication is essential, yet must not hinder frontline clinical speed during emergency or offline conditions.",
            "clinical_impact": "Prevents unauthorized prescription authoring, fraudulent laboratory result commitments, and malicious tampering with patient electronic medical records.",
            "system_impact": "Acts as the cryptographic security gateway for all platform APIs and edge storage, establishing authenticated principal identities, tenant isolation, and auditable non-repudiation.",
            "risk_profile": "Credential stuffing, unattended terminal hijacking, session hijacking via compromised local Wi-Fi, and lockouts during network severance."
        },
        "objectives": [
            {"id": "OBJ-WF02-01", "title": "Rapid Staff Authentication", "desc": "Authenticate authorized personnel within 3 seconds of credential submission.", "metric": "Auth Latency p95 < 3.0s", "verification": "Authentication span duration telemetry"},
            {"id": "OBJ-WF02-02", "title": "Zero Unauthorized Clinic Session Breaches", "desc": "Prevent 100% of brute-force and credential stuffing attacks via progressive delay and lockout.", "metric": "Breach Rate = 0.00%", "verification": "Automated security penetration audit logs"},
            {"id": "OBJ-WF02-03", "title": "Autonomous Offline Staff Login", "desc": "Enable scheduled clinical staff to log in during total WAN internet dropouts using cached credentials.", "metric": "Offline Login Success Rate = 100%", "verification": "Offline login simulation audit verification"},
            {"id": "OBJ-WF02-04", "title": "Inactivity Terminal Protection", "desc": "Automatically lock unattended terminal screens after 15 minutes of zero operator input.", "metric": "Idle Auto-Lock Enforced at 15:00 min", "verification": "Browser client inactivity timer assertion tests"}
        ],
        "in_scope": [
            {"area": "Credential Verification", "desc": "Username, password (Argon2id/scrypt), and TOTP MFA token validation."},
            {"area": "Session Lifecycle", "desc": "JWT minting, httpOnly cookie issuance, 15-min idle lock, and explicit logout."},
            {"area": "Offline Credential Cache", "desc": "Locally salted PIN and biometric token verification on edge server."},
            {"area": "RBAC Claim Binding", "desc": "Binding role codes (ROLE-001 to ROLE-008) and municipal ward boundaries."}
        ],
        "out_of_scope": [
            {"area": "Citizen Public Login", "desc": "Citizen self-service portal authentication; out of scope for staff terminal.", "handoff": "BBMP Citizen Health Portal"},
            {"area": "Central Active Directory Administration", "desc": "Creation of municipal government employee accounts.", "handoff": "BBMP Central HRMS / LDAP Directory"}
        ],
        "actors": [
            {"id": "ACT-WF02-01", "type": "Human", "name": "Frontline Clinical User", "responsibilities": "Submits credentials, verifies MFA challenge, locks screen upon leaving.", "permissions": "Session Create/Lock/Logout", "failure_duty": "Reports compromised passwords immediately to IT administrator.", "inputs": "Username, password, TOTP 6-digit code, PIN", "decisions": "Determines whether to lock terminal temporarily or log out fully.", "outputs": "Authenticated user session", "recovery": "Uses self-service password reset or contacts supervisor."},
            {"id": "ACT-WF02-02", "type": "System", "name": "Edge Auth Security Daemon", "responsibilities": "Verifies scrypt hashes, checks rate limits, issues JWT tokens, monitors idle timer.", "permissions": "System Security Master", "failure_duty": "Locks accounts upon detecting brute-force attack; alerts security team.", "inputs": "Auth requests, client IP, heartbeat pings", "decisions": "Authorizes or denies session creation; enforces lockout thresholds.", "outputs": "Signed JWT session, audit logs", "recovery": "Restores cached credential store from secure enclave."}
        ],
        "personas": [
            {"id": "PERSONA-001", "name": "Sister Bhavani Gowda", "role": "Staff Nurse", "env": "High-noise triage cubicle; needs fast PIN-based screen unlock between patients.", "goals": "Unlock tablet in < 2 seconds without typing long passwords repeatedly.", "pain_points": "Repeated full logouts during brief 2-minute patient escort movements.", "adaptations": "Quick 4-digit PIN re-unlock for locked sessions within 2 hours."},
            {"id": "PERSONA-002", "name": "Dr. Manjunath Swamy", "role": "Medical Officer", "env": "Chamber consultation; switches between clinical EHR and national ABDM portal.", "goals": "Maintain secure session without interrupting consultation flow.", "pain_points": "Session timeout in the middle of typing complex clinical notes.", "adaptations": "Subtle visual countdown warning at 13 minutes idle with 1-click extension."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "Own Profile, Triage Station", "create": "Session, Unlock", "update": "Own PIN", "delete": "Session (Logout)", "override": "None", "signoff": "Own Session"},
            {"role": "ROLE-002", "title": "Medical Officer", "read": "Own Profile, Doctor Chamber", "create": "Session, Unlock", "update": "Own PIN", "delete": "Session (Logout)", "override": "Emergency Fast-Unlock", "signoff": "Own Session"},
            {"role": "ROLE-006", "title": "Clinic Coordinator / Admin", "read": "All Staff Profiles, Audit Logs", "create": "Staff Account, Temporary PIN", "update": "Account Status", "delete": "Revoke Session", "override": "Account Unlock", "signoff": "Staff Roster"}
        ],
        "preconditions": [
            {"id": "PRE-WF02-01", "desc": "Staff user has an active, non-suspended account in clinic directory.", "check": "account.status == 'ACTIVE'", "on_fail": "Display 'Account Inactive - Contact Clinic Admin'."},
            {"id": "PRE-WF02-02", "desc": "Edge auth service running and cryptographic keys accessible in secure storage.", "check": "auth_service.status == 'HEALTHY'", "on_fail": "Switch to emergency offline auth daemon."}
        ],
        "triggers": [
            {"id": "TRIG-WF02-01", "class": "User Trigger", "event": "Staff user accesses clinic web portal login page", "source": "Browser UI", "payload": "{ client_ip, user_agent }", "latency": "< 100ms to render form"},
            {"id": "TRIG-WF02-02", "class": "System Trigger", "event": "Session inactivity timer reaches 15 minutes", "source": "Client Inactivity Daemon", "payload": "{ session_id, idle_seconds: 900 }", "latency": "Immediate screen lock"}
        ],
        "inputs": [
            {"name": "username", "type": "String(32)", "req": "Mandatory", "source": "Staff User", "val": "Alphanumeric username regex ^[a-z0-9_]{4,32}$", "priv": "Operational", "enc": "Plaintext", "ex": "nurse_bhavani", "on_err": "Prompt valid username format"},
            {"name": "password", "type": "String(64)", "req": "Mandatory", "source": "Staff User", "val": "Min 8 chars, mixed case, number, symbol", "priv": "Restricted", "enc": "Argon2id hash", "ex": "P@ssw0rd!2026", "on_err": "Increment failure count"},
            {"name": "totp_code", "type": "String(6)", "req": "Mandatory", "source": "Authenticator App / SMS", "val": "6-digit numeric string regex ^\\d{6}$", "priv": "Restricted", "enc": "Plaintext in transit", "ex": "482910", "on_err": "Reject MFA token; allow 2 retries"},
            {"name": "offline_pin", "type": "String(4)", "req": "Optional", "source": "Staff User", "val": "4-digit numeric PIN regex ^\\d{4}$", "priv": "Restricted", "enc": "Scrypt salted hash", "ex": "8492", "on_err": "Lock offline cache after 3 failures"}
        ],
        "outputs": {
            "success": [
                {"name": "Cryptographic JWT Session Token", "desc": "RS256 signed access token with role and ward claims.", "format": "JWT String in httpOnly Cookie", "recipient": "Browser Client Storage"},
                {"name": "Authenticated User Context", "desc": "Staff profile, assigned station, permissions, and shift bounds.", "format": "JSON Object", "recipient": "Client Application State Store"}
            ],
            "partial": [
                {"name": "Locked Screen State Context", "desc": "Retains user workspace in background while locking screen display.", "format": "Local Encrypted Session", "fallback": "Requires 4-digit PIN to unlock"}
            ],
            "error": [
                {"name": "Authentication Failure Envelope", "desc": "Structured error response detailing failure category without leaking existence.", "code": "ERR-AUTH-INVALID-CREDENTIALS", "msg": "Invalid username or password. 4 attempts remaining."}
            ],
            "events": [
                {"topic": "namma.clinic.auth.login_success", "desc": "Emitted upon successful credential and MFA verification.", "schema": "{ user_id, role, terminal_id, timestamp }"},
                {"topic": "namma.clinic.auth.account_locked", "desc": "Emitted when account exceeds brute force threshold.", "schema": "{ user_id, attempts: 5, client_ip, lockout_until }"}
            ]
        },
        "happy_path": [
            {"title": "Staff Accesses Clinic Portal Login", "actor": "Staff User (`ACT-WF02-01`)", "input": "Browser URL `https://clinic.local/login`", "action": "Opens clinic web portal in browser.", "sys_behavior": "Serves login page over TLS 1.3; initializes CSRF token.", "validation": "CSRF token valid", "db_effect": "None", "ui_effect": "Bilingual login form displayed in Kannada/English.", "api_effect": "GET /login", "audit_effect": "None", "output": "Login form rendered", "next_state": "WFSTATE-002-001", "failure_possibility": "TLS handshake failure."},
            {"title": "Username & Password Submission", "actor": "Staff User (`ACT-WF02-01`)", "input": "Username and password entered", "action": "Submits credentials.", "sys_behavior": "Checks rate limiter; verifies Argon2id hash against DB.", "validation": "Password hash matches", "db_effect": "Updates `last_login_attempt`", "ui_effect": "Shows loading spinner on button.", "api_effect": "POST /api/v1/auth/login", "audit_effect": "WFAUDIT-002-001 (Credentials Checked)", "output": "Password verified", "next_state": "WFSTATE-002-002", "failure_possibility": "Invalid credentials; account locked."},
            {"title": "MFA Challenge Presentation", "actor": "Edge Auth Security Daemon (`ACT-WF02-02`)", "input": "Valid password verification", "action": "Presents 6-digit TOTP input modal.", "sys_behavior": "Generates temporary pre-auth session token (TTL: 3 min).", "validation": "Pre-auth token active", "db_effect": "None", "ui_effect": "Displays TOTP entry dialog with 3-minute timer.", "api_effect": "None", "audit_effect": "WFAUDIT-002-002 (MFA Challenged)", "output": "MFA prompt visible", "next_state": "WFSTATE-002-003", "failure_possibility": "Authenticator app desync."},
            {"title": "MFA Code Verification & JWT Issuance", "actor": "Staff User (`ACT-WF02-01`)", "input": "Enters 6-digit TOTP code from authenticator app", "action": "Submits MFA code.", "sys_behavior": "Verifies RFC 6238 TOTP window (+/- 1 step); mints RS256 JWT.", "validation": "TOTP code matches", "db_effect": "Inserts row in `user_active_sessions`", "ui_effect": "Redirects to assigned station dashboard.", "api_effect": "POST /api/v1/auth/mfa/verify", "audit_effect": "WFAUDIT-002-003 (Session Established)", "output": "Active JWT session cookie", "next_state": "WFSTATE-002-004", "failure_possibility": "Expired TOTP code."},
            {"title": "Station Dashboard Initialization", "actor": "Staff User (`ACT-WF02-01`)", "input": "Session cookie present", "action": "Loads station workspace (Triage, Doctor Room, Pharmacy).", "sys_behavior": "Evaluates RBAC claims; renders station controls.", "validation": "RBAC claims valid", "db_effect": "None", "ui_effect": "Unlocks functional station screens.", "api_effect": "GET /api/v1/user/context", "audit_effect": "WFAUDIT-002-004 (Workspace Loaded)", "output": "Station active", "next_state": "WFSTATE-002-005", "failure_possibility": "Unauthorized role for station."},
            {"title": "Inactivity Timer Monitoring", "actor": "Edge Auth Security Daemon (`ACT-WF02-02`)", "input": "User DOM events (clicks, keys, mouse moves)", "action": "Monitors operator activity.", "sys_behavior": "Resets 15-minute countdown on any valid user input.", "validation": "Countdown active", "db_effect": "None", "ui_effect": "Inactivity indicator hidden.", "api_effect": "None", "audit_effect": "None", "output": "Active session", "next_state": "WFSTATE-002-005", "failure_possibility": "Background tab throttling timer."},
            {"title": "Inactivity Lock Engagement", "actor": "Edge Auth Security Daemon (`ACT-WF02-02`)", "input": "No user input for 15:00 minutes", "action": "Locks station screen.", "sys_behavior": "Masks clinical data with privacy shield; retains state in memory.", "validation": "Idle duration >= 900s", "db_effect": "Updates session state to `IDLE_LOCKED`", "ui_effect": "Displays lock modal: 'Screen Locked due to Inactivity'.", "api_effect": "POST /api/v1/auth/session/lock", "audit_effect": "WFAUDIT-002-005 (Screen Locked)", "output": "Locked screen", "next_state": "WFSTATE-002-006", "failure_possibility": "Screen unlocked by passerby."},
            {"title": "Quick PIN Unlock", "actor": "Staff User (`ACT-WF02-01`)", "input": "Staff returns; enters 4-digit PIN", "action": "Submits quick PIN.", "sys_behavior": "Validates PIN against locally salted scrypt hash.", "validation": "PIN hash matches", "db_effect": "Updates session state to `ACTIVE`", "ui_effect": "Removes privacy shield; restores exact clinical state.", "api_effect": "POST /api/v1/auth/session/unlock", "audit_effect": "WFAUDIT-002-006 (Screen Unlocked)", "output": "Workspace restored", "next_state": "WFSTATE-002-005", "failure_possibility": "Incorrect PIN (locks after 3)."},
            {"title": "Explicit Session Logout", "actor": "Staff User (`ACT-WF02-01`)", "input": "Click 'Sign Out / ನಿರ್ಗಮನ'", "action": "Logs out at end of shift.", "sys_behavior": "Invalidates JWT on server blacklist; clears browser cookie.", "validation": "Cookie cleared", "db_effect": "Updates session record to `LOGGED_OUT`", "ui_effect": "Redirects to clean login screen.", "api_effect": "POST /api/v1/auth/logout", "audit_effect": "WFAUDIT-002-007 (Session Terminated)", "output": "Clean login screen", "next_state": "WFSTATE-002-001", "failure_possibility": "Network timeout on logout."}
        ],
        "alternate_flows": [
            {
                "id": "WFALT-002-001", "title": "Offline PIN Authentication During WAN Outage",
                "condition": "Broadband internet is down when staff arrives to log in.",
                "from_step": "WFSTEP-002-002",
                "steps": [
                    "User enters username and 4-digit offline PIN.",
                    "Edge daemon verifies PIN against local scrypt salted cache `/var/auth/credentials.db`.",
                    "Issues local edge session token valid for 8 hours on clinic LAN.",
                    "Displays amber banner: 'Authenticated via Local Offline Cache'."
                ],
                "rejoin": "Rejoins main flow at Step WFSTEP-002-005 (Station Dashboard Initialization).",
                "audit": "WFAUDIT-002-ALT01 (Offline Login Succeeded)"
            },
            {
                "id": "WFALT-002-002", "title": "SMS-Based MFA Fallback When Authenticator Unavailable",
                "condition": "Staff user does not have smartphone authenticator app.",
                "from_step": "WFSTEP-002-003",
                "steps": [
                    "User clicks 'Send Code via SMS to registered mobile'.",
                    "Gateway generates 6-digit cryptographic OTP and dispatches via SMS.",
                    "User receives SMS in Kannada/English and enters code within 3 minutes.",
                    "System verifies OTP and advances to session creation."
                ],
                "rejoin": "Rejoins main flow at Step WFSTEP-002-004.",
                "audit": "WFAUDIT-002-ALT02 (SMS MFA Fallback Utilized)"
            }
        ],
        "exception_flows": [
            {
                "id": "WFEX-002-001", "title": "Account Locked Due to Brute Force Attempts",
                "trigger": "5 consecutive failed password submissions within 10 minutes.",
                "detection": "Security filter checks failure counter on username and IP.",
                "containment": "Locks account for 30 minutes; returns generic error message.",
                "msg_en": "Account temporarily locked due to repeated failed login attempts.",
                "msg_kn": "ಸತತ ವಿಫಲ ಲಾಗಿನ್ ಪ್ರಯತ್ನಗಳಿಂದಾಗಿ ಖಾತೆಯನ್ನು ತಾತ್ಕಾಲಿಕವಾಗಿ ಲಾಕ್ ಮಾಡಲಾಗಿದೆ.",
                "recovery": "Staff contacts Clinic Coordinator to reset lockout after identity verification.",
                "audit": "WFAUDIT-002-EX01", "severity": "HIGH"
            },
            {
                "id": "WFEX-002-002", "title": "Concurrent Device Login Conflict",
                "trigger": "User attempts to log in from Room 2 while active session exists in Room 1.",
                "detection": "Session manager detects active session ID for user in `user_active_sessions`.",
                "containment": "Displays prompt: 'Active session detected in Room 1. Terminate other session?'.",
                "msg_en": "You are currently signed in on another terminal. Terminate previous session to proceed.",
                "msg_kn": "ನೀವು ಈಗಾಗಲೇ ಮತ್ತೊಂದು ಟರ್ಮಿನಲ್‌ನಲ್ಲಿ ಲಾಗಿನ್ ಆಗಿದ್ದೀರಿ. ಮುಂದುವರಿಯಲು ಹಿಂದಿನ ಸೆಷನ್ ಮುಕ್ತಾಯಗೊಳಿಸಿ.",
                "recovery": "User confirms; previous terminal revoked immediately over WebSocket.",
                "audit": "WFAUDIT-002-EX02", "severity": "MEDIUM"
            }
        ],
        "emergency_flow": {
            "triggers": "Critical mass casualty or trauma patient arrives while terminal is locked and doctor credentials temporarily forgotten.",
            "escalation": "Nurse uses physical Emergency Break-Glass RFID Card to instantly unlock terminal into 'EMERGENCY_GUEST' mode.",
            "preemption": "Immediately opens emergency resuscitation chart with full clinical privileges.",
            "bypass_rules": "Bypasses password and MFA challenge; logs emergency RFID serial number.",
            "safety_controls": "Restricted strictly to active resuscitation encounter; blocked from accessing other patient records.",
            "reconciliation": "Medical Officer must sign off emergency actions using formal credentials within 2 hours.",
            "audit_event": "WFAUDIT-002-BREAKGLASS (Emergency RFID Access Unlocked)",
            "signoff_sla": "2 hours post-emergency sign-off"
        },
        "states": [
            {"name": "UNAUTHENTICATED", "desc": "No active user session on terminal.", "allowed": "Login attempt", "prohibited": "Any clinical data access", "actor": "Anonymous"},
            {"name": "CREDENTIALS_ENTERED", "desc": "Username and password submitted for evaluation.", "allowed": "Hash verification", "prohibited": "Session creation", "actor": "Auth Daemon"},
            {"name": "MFA_CHALLENGED", "desc": "Awaiting 6-digit TOTP/SMS code.", "allowed": "MFA code entry, resend", "prohibited": "Accessing dashboard", "actor": "Staff User"},
            {"name": "SESSION_ACTIVE", "desc": "Fully authenticated session with active JWT.", "allowed": "All role-permitted station actions", "prohibited": "Unpermitted roles", "actor": "Staff User"},
            {"name": "SESSION_LOCKED_IDLE", "desc": "15-minute inactivity lock engaged; clinical view masked.", "allowed": "PIN unlock, full logout", "prohibited": "Viewing patient records", "actor": "Staff User"},
            {"name": "ACCOUNT_LOCKED_BRUTEFORCE", "desc": "Account locked after 5 failed attempts.", "allowed": "Admin unlock only", "prohibited": "All login attempts", "actor": "Admin"}
        ],
        "transitions": [
            {"from_state": "UNAUTHENTICATED", "event": "Submit Credentials", "actor": "Staff User", "condition": "Username and password provided", "validation": "Format valid", "to_state": "CREDENTIALS_ENTERED", "side_effects": "Check rate limiter", "audit": "WFAUDIT-002-TR01"},
            {"from_state": "CREDENTIALS_ENTERED", "event": "Password Validated", "actor": "Auth Daemon", "condition": "Argon2id matches", "validation": "Hash matches", "to_state": "MFA_CHALLENGED", "side_effects": "Generate pre-auth token", "audit": "WFAUDIT-002-TR02"},
            {"from_state": "MFA_CHALLENGED", "event": "MFA Verified", "actor": "Staff User", "condition": "TOTP code valid", "validation": "RFC 6238 check", "to_state": "SESSION_ACTIVE", "side_effects": "Issue JWT cookie", "audit": "WFAUDIT-002-TR03"},
            {"from_state": "SESSION_ACTIVE", "event": "Inactivity Timeout (15m)", "actor": "Security Daemon", "condition": "Idle duration >= 900s", "validation": "Timer check", "to_state": "SESSION_LOCKED_IDLE", "side_effects": "Mask screen", "audit": "WFAUDIT-002-TR04"},
            {"from_state": "SESSION_LOCKED_IDLE", "event": "PIN Unlocked", "actor": "Staff User", "condition": "4-digit PIN matches", "validation": "PIN hash check", "to_state": "SESSION_ACTIVE", "side_effects": "Unmask screen", "audit": "WFAUDIT-002-TR05"},
            {"from_state": "SESSION_ACTIVE", "event": "Click Logout", "actor": "Staff User", "condition": "User confirms exit", "validation": "Session valid", "to_state": "UNAUTHENTICATED", "side_effects": "Revoke JWT", "audit": "WFAUDIT-002-TR06"}
        ],
        "decision_tables": [
            {
                "id": "WFDEC-002-001", "title": "Staff Login Authentication Path Decision",
                "desc": "Determines authentication pathway based on network status and MFA modality.",
                "conditions": ["WAN Online", "Password Correct", "MFA Token Valid", "Offline PIN Correct"],
                "actions": ["Issue Central JWT", "Issue Offline JWT", "Present MFA Challenge", "Reject Login & Alert"],
                "rows": [
                    {"rule": "A1", "cond_vals": ["YES", "YES", "YES", "ANY"], "act_vals": ["YES", "NO", "NO", "NO"]},
                    {"rule": "A2", "cond_vals": ["YES", "YES", "NO", "ANY"], "act_vals": ["NO", "NO", "YES", "NO"]},
                    {"rule": "A3", "cond_vals": ["NO", "ANY", "ANY", "YES"], "act_vals": ["NO", "YES", "NO", "NO"]},
                    {"rule": "A4", "cond_vals": ["ANY", "NO", "ANY", "NO"], "act_vals": ["NO", "NO", "NO", "YES"]}
                ]
            }
        ],
        "validation_rules": [
            {"id": "WFVAL-002-001", "field": "password", "expr": "len(password) >= 8 and has_upper and has_lower and has_digit", "code": "ERR-VAL-02-01", "msg_en": "Password must be at least 8 characters with mixed case and digits.", "msg_kn": "ಪಾಸ್‌ವರ್ಡ್ ಕನಿಷ್ಠ 8 ಅಕ್ಷರಗಳು, ದೊಡ್ಡಕ್ಷರ ಮತ್ತು ಅಂಕಿಗಳನ್ನು ಹೊಂದಿರಬೇಕು.", "recovery": "Enter compliant password.", "test_ref": "WFTEST-002-001"},
            {"id": "WFVAL-002-002", "field": "totp_code", "expr": "regex_match('^\\d{6}$', totp)", "code": "ERR-VAL-02-02", "msg_en": "MFA code must be exactly 6 digits.", "msg_kn": "MFA ಕೋಡ್ ನಿಖರವಾಗಿ 6 ಅಂಕಿಗಳಾಗಿರಬೇಕು.", "recovery": "Re-enter 6-digit token.", "test_ref": "WFTEST-002-002"}
        ],
        "business_rules": [
            {"id": "BRULE-WF02-001", "title": "Mandatory Inactivity Screen Lock", "req": "BRULE-002", "spec": "Every clinic workstation shall automatically mask screen displays and lock session after 15 minutes of zero operator input.", "enforcement": "Client-side daemon enforces timer; server rejects API calls from locked sessions.", "consequence": "Prevents unauthorized PHI access on abandoned terminals."}
        ],
        "clinical_rules": [
            {"id": "CR-WF02-001", "title": "Zero Interruption During Emergency Resuscitation", "req": "CR-002", "rationale": "Clinical staff resuscitating a patient must not be locked out by software inactivity timers.", "logic": "Active Code Red mode suspends 15-minute lock timer on resuscitation terminal.", "override_policy": "Automated extension while emergency status is active.", "safety_invariant": "Life-saving emergency clinical care supersedes routine session lockout."}
        ],
        "operational_rules": [
            {"id": "OR-WF02-001", "title": "Prohibition of Shared Generic Accounts", "req": "OR-002", "mandate": "Every staff member must log in using their own individually assigned credentials. Generic shared accounts are strictly prohibited.", "boundary": "All clinic terminals.", "exception": "None. Roving staff issued individual roving accounts."}
        ],
        "security_controls": [
            {"domain": "Password Storage", "id": "SEC-WF02-01", "spec": "Passwords hashed with Argon2id (m=64MB, t=3, p=4).", "param": "Argon2id", "threat": "Credential database dump attacks", "compliance": "SECR-002"},
            {"domain": "Session Token", "id": "SEC-WF02-02", "spec": "JWT signed with RS256 private key; stored in httpOnly, Secure, SameSite=Strict cookie.", "param": "RS256 2048-bit", "threat": "XSS token theft", "compliance": "SECR-002"}
        ],
        "privacy_controls": [
            {"principle": "Access Limitation", "id": "PRIV-WF02-01", "spec": "Staff permissions strictly limited to assigned station and ward.", "invariant": "Need-to-know access only", "right": "DPDP Act Sec 6"}
        ],
        "offline_behavior": {
            "online_mode": "Cloud LDAP / Auth service verification with real-time audit logging.",
            "detection_latency": "Auth daemon detects WAN status in < 1 second.",
            "local_storage": "Encrypted local SQLite credentials cache storing salted scrypt hashes of scheduled staff.",
            "queue_mechanics": "Offline login events queued in local audit log; synced upon reconnection.",
            "degraded_scope": "Permits full clinical workstation operation using cached staff credentials.",
            "sync_convergence": "Reconciles session logs with central audit trail upon reconnection.",
            "conflict_invariants": "Revoked accounts on cloud immediately lock local sessions upon reconnection."
        },
        "diagrams": {
            "data_flow": """flowchart TD
    User["Staff User"] -->|Enter Credentials| UI["Web Login Form"]
    UI -->|POST /auth/login| Gateway["API Gateway Auth Filter"]
    Gateway -->|Verify Hash| DB[("User Credentials DB")]
    Gateway -->|Verify TOTP| MFA["MFA Verification Engine"]
    Gateway -->|Issue JWT| Cookie["httpOnly Secure Cookie"]
    Cookie --> UI
    Gateway -->|Append Audit| Audit[("Immutable Audit Log")]""",
            "sequence": """sequenceDiagram
    actor U as Staff User
    participant UI as Login Screen
    participant G as Auth Gateway
    participant DB as User DB
    U->>UI: 1. Enter username & password
    UI->>G: 2. POST /auth/login
    G->>DB: 3. Verify Argon2id hash
    DB-->>G: 4. Password valid
    G-->>UI: 5. Present MFA modal
    U->>UI: 6. Enter 6-digit TOTP
    UI->>G: 7. POST /auth/mfa/verify
    G->>G: 8. Mint RS256 JWT
    G-->>UI: 9. Set httpOnly cookie & redirect
    UI-->>U: 10. Station dashboard loaded""",
            "activity": """flowchart TD
    Start([Open Portal]) --> EnterCreds[Enter Username & Password]
    EnterCreds --> VerifyPW{Password Correct?}
    VerifyPW -- No --> IncFail[Increment Failure Counter] --> CheckLock{Failures >= 5?}
    CheckLock -- Yes --> LockAcct[Lock Account 30 Min] --> End([Access Denied])
    CheckLock -- No --> EnterCreds
    VerifyPW -- Yes --> PromptMFA[Prompt 6-Digit TOTP Code]
    PromptMFA --> VerifyMFA{TOTP Valid?}
    VerifyMFA -- No --> PromptMFA
    VerifyMFA -- Yes --> MintJWT[Issue RS256 JWT Token]
    MintJWT --> StationActive[Station Workspace Active]
    StationActive --> IdleCheck{Idle >= 15 Min?}
    IdleCheck -- Yes --> LockScreen[Mask Screen & Prompt PIN]
    LockScreen --> EnterPIN[Enter 4-Digit PIN] --> StationActive
    IdleCheck -- No --> Logout{User Logged Out?}
    Logout -- Yes --> Terminate[Revoke JWT & Clear Cookie] --> End""",
            "state": """stateDiagram-v2
    [*] --> UNAUTHENTICATED
    UNAUTHENTICATED --> CREDENTIALS_ENTERED: Submit Username/Password
    CREDENTIALS_ENTERED --> MFA_CHALLENGED: Password Verified
    CREDENTIALS_ENTERED --> UNAUTHENTICATED: Invalid Password
    MFA_CHALLENGED --> SESSION_ACTIVE: TOTP Verified
    SESSION_ACTIVE --> SESSION_LOCKED_IDLE: Inactivity (15 min)
    SESSION_LOCKED_IDLE --> SESSION_ACTIVE: 4-Digit PIN Verified
    SESSION_ACTIVE --> UNAUTHENTICATED: Explicit Logout
    SESSION_LOCKED_IDLE --> UNAUTHENTICATED: Logout / Session Expired"""
        },
        "data_flow_nodes": [
            {"name": "UI", "desc": "React / Vanilla JS login view with bilingual support.", "protocol": "HTTPS", "encryption": "TLS 1.3"},
            {"name": "Gateway", "desc": "Go-based edge security gateway enforcing JWT validation.", "protocol": "HTTP / IPC", "encryption": "TLS 1.3"},
            {"name": "DB", "desc": "PostgreSQL (Cloud) / SQLite (Edge) credential store.", "protocol": "Encrypted SQL", "encryption": "AES-256 at rest"}
        ],
        "failure_tree": [
            {"id": "FT-002-001", "cat": "Security", "root": "Brute force password guessing attack", "vector": "Automated script", "impact": "Account lockout", "detection": "5 failed attempts in 10 min", "mitigation": "Progressive delay + 30 min lockout"},
            {"id": "FT-002-002", "cat": "Hardware", "root": "Staff mobile phone battery dead (No TOTP)", "vector": "Dead battery", "impact": "Cannot complete MFA", "detection": "User clicks fallback", "mitigation": "Fallback to SMS or supervisor emergency unlock"},
            {"id": "FT-002-003", "cat": "Network", "root": "WAN broadband fiber severed", "vector": "Physical cut", "impact": "Cannot reach cloud auth server", "detection": "DNS / HTTP timeout", "mitigation": "Auto-switch to edge local scrypt PIN auth"}
        ],
        "recovery_procedures": [
            {"id": "REC-WF02-01", "title": "Staff Account Lockout Reset Runbook", "trigger": "Staff account locked after 5 failed attempts.", "containment": "Account locked automatically.", "steps": ["Coordinator verifies staff physical identity card.", "Coordinator accesses Admin Console: 'Unlock User Account'.", "System resets failure counter and prompts staff for password."], "rollback": "None", "resumption": "Staff logs in normally.", "audit": "WFAUDIT-002-REC01"}
        ],
        "audit_events": [
            {"id": "WFAUDIT-002-001", "event": "STAFF_PASSWORD_VERIFIED", "actor": "Staff User", "meta": "{ username, client_ip }", "state_before": "UNAUTH", "state_after": "MFA_PENDING", "hmac": "HMAC-SHA256", "retention": "7 Years", "compliance": "SECR-002"},
            {"id": "WFAUDIT-002-002", "event": "STAFF_MFA_CHALLENGED", "actor": "Security Daemon", "meta": "{ username, method: 'TOTP' }", "state_before": "MFA_PENDING", "state_after": "MFA_SENT", "hmac": "HMAC-SHA256", "retention": "7 Years", "compliance": "SECR-002"},
            {"id": "WFAUDIT-002-003", "event": "STAFF_SESSION_ESTABLISHED", "actor": "Staff User", "meta": "{ user_id, role, jwt_id }", "state_before": "MFA_SENT", "state_after": "ACTIVE", "hmac": "HMAC-SHA256", "retention": "7 Years", "compliance": "SECR-002"}
        ],
        "notifications": [
            {"id": "WFNOTIF-002-01", "trigger": "Login from New Device", "recipient": "Staff User", "channel": "SMS", "text_en": "Namma Clinic security: Login to your account from terminal Room 2.", "text_kn": "ನಮ್ಮ ಕ್ಲಿನಿಕ್ ಭದ್ರತೆ: ಟರ್ಮಿನಲ್ ಕೊಠಡಿ 2 ರಿಂದ ನಿಮ್ಮ ಖಾತೆಗೆ ಲಾಗಿನ್ ಆಗಿದೆ.", "priority": "High", "retry": "None", "fallback": "Email"}
        ],
        "planned_apis": [
            {"id": "PLANNED-API-002-01", "method": "POST", "path": "/api/v1/auth/login", "desc": "Submits username and password for authentication.", "scope": "public", "req_schema": "{\n  \"username\": \"string\",\n  \"password\": \"string\"\n}", "res_schema": "{\n  \"status\": \"MFA_REQUIRED\",\n  \"pre_auth_token\": \"string\"\n}", "errors": "400 Bad Request, 401 Invalid Credentials, 429 Too Many Requests", "idempotency": "Not Required", "rate_limit": "5 req/min per IP", "offline_support": "Local verification against edge scrypt cache"}
        ],
        "planned_db": [
            {"id": "PLANNED-DB-002-01", "table": "user_active_sessions", "purpose": "Tracks active authenticated JWT sessions and terminal bindings.", "pk": "session_id (UUID)", "fks": "user_id -> users(user_id)", "cols": [
                {"name": "session_id", "type": "UUID", "null": "NOT NULL", "notes": "Primary Key"},
                {"name": "user_id", "type": "UUID", "null": "NOT NULL", "notes": "Foreign Key to users"},
                {"name": "token_jti", "type": "VARCHAR(64)", "null": "NOT NULL", "notes": "JWT Unique ID"},
                {"name": "status", "type": "VARCHAR(20)", "null": "NOT NULL", "notes": "ACTIVE | IDLE_LOCKED | REVOKED"},
                {"name": "last_active_at", "type": "TIMESTAMPTZ", "null": "NOT NULL", "notes": "Heartbeat timestamp"}
            ], "indexes": "UNIQUE(token_jti), INDEX(user_id, status)", "concurrency": "Optimistic Locking", "retention": "Purged after 30 days"}
        ],
        "planned_ui": [
            {"id": "PLANNED-UI-002-01", "screen": "Staff Login Screen", "route": "/login", "persona": "Staff Nurse / Doctor", "components": "Bilingual login form, Kannada language switch, TOTP challenge modal, offline mode badge.", "states": "Initial, Validating, MFA Prompt, Locked, Success.", "validations": "Username and password required; PIN format 4 digits.", "a11y": "Full keyboard navigation and ARIA labels.", "localization": "Complete Kannada parity.", "offline_ui": "Shows 'Offline Local Auth Available' badge."}
        ],
        "backend_reqs": {
            "domain_services": "Orchestrates `AuthenticationService`, `SessionManager`, `RateLimiter`, and `MfaEngine`.",
            "transactions": "Atomic session record creation and audit emission in single transaction.",
            "async_workers": "Background token cleanup worker purges expired JWT records every hour.",
            "circuit_breakers": "Cloud LDAP circuit breaker trips after 3 timeouts; falls back to edge local cache."
        },
        "integrations": [
            {"id": "INT-WF02-01", "system": "BBMP Central Directory", "protocol": "LDAP / TLS", "payload": "User account verification", "direction": "Outbound", "timeout": "3 sec", "fallback": "Local cached credentials"}
        ],
        "reports": [
            {"id": "REP-WF02-01", "title": "Staff Authentication & Security Access Audit", "freq": "Daily", "audience": "CISO, Zonal Health Officer", "grain": "Per clinic, per user login", "ref": "SECR-002"}
        ],
        "analytics": [
            {"id": "ANL-WF02-01", "kpi": "Authentication Failure Rate", "formula": "(failed_logins / total_attempts) * 100", "dimensions": "Clinic, Role", "target": "< 5%", "alert": "Failure rate > 15% triggers security alert"}
        ],
        "ai_reqs": {
            "id": "AIR-WF02-01", "purpose": "Anomalous Login Detection", "features": "Time of day, Terminal IP, Failed attempts count",
            "output_signal": "Anomaly Risk Score (0-1)", "confidence": "Flagged if score >= 0.85", "explainability": "Explains: 'Login outside scheduled shift hours'.",
            "authority": "Advisory alert to security officer.", "audit": "WFAUDIT-002-AI01"
        },
        "stride_threats": [
            {"id": "STRIDE-WF02-01", "cat": "Spoofing", "asset": "Staff Password", "scenario": "Attacker guesses weak nurse password.", "likelihood": "Medium", "impact": "High", "mitigation": "Enforce TOTP MFA and strong password policy.", "residual": "Low", "test_ref": "WFTEST-002-001"}
        ],
        "linddun_threats": [
            {"id": "LINDDUN-WF02-01", "cat": "Identifiability", "asset": "Session Logs", "vector": "Unencrypted IP reveals staff home location.", "likelihood": "Low", "impact": "Low", "mitigation": "Mask internal IPs in public logs.", "compliance": "DPDP Act"}
        ],
        "performance": {
            "e2e_latency": "Auth completed in < 1.5 seconds.", "ui_render": "Login form renders in < 100ms.",
            "db_budget": "Credential lookup < 5ms.", "concurrency": "50 concurrent login attempts/sec.",
            "payload": "JWT size < 1KB.", "hardware": "RAM usage < 50MB."
        },
        "availability": {
            "sla": "99.99% login availability.", "rto": "< 1 min.", "rpo": "0 sessions lost.",
            "offline_autonomy": "Full offline login supported via local scrypt cache.", "failover": "Dual-node edge redundancy."
        },
        "accessibility": {
            "screen_reader": "Full ARIA landmarks.", "contrast": "Contrast ratio >= 4.5:1.",
            "keyboard": "Tab order logical with focus outline.", "touch": "Buttons >= 48px.", "cognitive": "Simple, clean login screen."
        },
        "localization": {
            "clinical_terms": "Standard terminology.", "printed_material": "N/A",
            "audio_prompts": "Bilingual audio chime on error."
        },
        "test_gates": [
            {"level": "Unit Testing", "scope": "Argon2id hashing, TOTP validation", "tooling": "PyTest", "coverage": ">= 95%", "gate": "Zero failures on pre-commit"},
            {"level": "Security Testing", "scope": "Brute force and session hijacking tests", "tooling": "OWASP ZAP", "coverage": "100% of auth endpoints", "gate": "Zero critical vulnerabilities"}
        ],
        "bdd_scenarios": [
            {
                "id": "WFTEST-002-001", "title": "Successful Multi-Factor Staff Login",
                "category": "Happy Path", "priority": "P0",
                "given": "the staff nurse enters a valid username and password",
                "given_ands": ["the clinic auth service is healthy and connected"],
                "when": "the nurse submits the credentials and enters the correct 6-digit TOTP code",
                "when_ands": ["clicks 'Verify and Sign In'"],
                "then": "the system issues a signed JWT session cookie",
                "then_ands": ["redirects the nurse to the Triage Station workspace within 2 seconds"]
            },
            {
                "id": "WFTEST-002-002", "title": "Automatic Screen Lock After 15 Minutes Inactivity",
                "category": "Security Control", "priority": "P0",
                "given": "the medical officer is logged into the consultation workspace",
                "given_ands": ["leaves the terminal unattended for 15 consecutive minutes"],
                "when": "the client inactivity timer reaches 900 seconds",
                "when_ands": ["no keyboard or mouse movement is detected"],
                "then": "the system masks all clinical data with a privacy shield",
                "then_ands": ["displays the PIN unlock dialog requiring a 4-digit PIN to restore access"]
            }
        ],
        "acceptance_criteria": [
            {"id": "AC-WF-002-001", "criterion": "Successful login with MFA completes in < 3.0s.", "method": "Telemetry timer", "threshold": "p95 < 3.0s", "gate": "Security Baseline Gate"},
            {"id": "AC-WF-002-002", "criterion": "Account locked after exactly 5 failed password attempts.", "method": "Automated security test", "threshold": "Lockout on attempt 5", "gate": "Security Baseline Gate"}
        ],
        "dependencies": [
            {"id": "WFDEP-002-01", "upstream": "None", "downstream": "WF-001", "nature": "Core Security Prerequisite", "blocking": "BLOCKING", "impact": "Clinic day cannot open without authenticated staff.", "resilience": "Offline cached credentials allow autonomous local login."}
        ],
        "critical_path": {
            "path": "Username/Password Submit -> Argon2id Hash Check -> MFA Challenge -> TOTP Verification -> JWT Issuance.",
            "bottleneck": "Argon2id computation takes ~150ms on edge hardware (by design for security).",
            "load_balancing": "Local cache eliminates central LDAP latency.",
            "recovery_bottlenecks": "Admin unlock requires supervisor presence."
        },
        "rollback_strategy": {
            "db_rollback": "Failed session creation rolls back cleanly.",
            "saga_compensation": "Revoked session deletes token record and notifies client.",
            "notification_reversal": "None.",
            "audit_preservation": "All login attempts (success and fail) permanently logged.",
            "offline_rollback": "Offline cache corruption triggers auto-restore from backup."
        },
        "idempotency": {
            "key_schema": "UUIDv4 on pre-auth token.",
            "cache_store": "In-memory session registry.",
            "replay_behavior": "Replaying login request does not generate duplicate sessions.",
            "ttl": "24 hours.", "offline_replay": "Syncs login audit events to cloud."
        },
        "concurrency": {
            "occ": "Session records use versioning.",
            "pessimistic": "Account lockout counter uses atomic increment.",
            "queue_locking": "None.", "deadlock_policy": "Standard database transaction timeout."
        },
        "invariants": [
            {"id": "INVARIANT-WF-002-01", "statement": "No clinical data shall be accessible without an active, non-expired cryptographic session.", "scope": "All Platform APIs", "enforcement": "API gateway rejects unauthenticated requests with HTTP 401.", "consequence": "Hard blocking error."}
        ],
        "observability": [
            {"cat": "Metric", "name": "namma_clinic_active_sessions_count", "type": "Gauge", "labels": "clinic_id, role", "target": "Prometheus", "alert": "None"}
        ],
        "runbook": {
            "morning_sop": "Staff members authenticate individually at their designated stations using username, password, and TOTP code.",
            "live_sop": "If stepping away, click 'Lock Screen'. Enter 4-digit PIN upon return.",
            "troubleshooting_sop": "If internet is offline: Enter username and 4-digit offline PIN to log in via local cache.",
            "closing_sop": "Click 'Sign Out' at end of shift. Confirm session terminated."
        },
        "sla_slo": [
            {"name": "Auth API Latency", "target": "< 2.0s", "window": "Monthly", "warning": "> 3.0s", "escalation": "DevOps alerted"}
        ],
        "traceability": [
            {"req": "SECR-002", "type": "Security Req", "step": "WFSTEP-002-004", "state": "WFSTATE-002-004", "api": "PLANNED-API-002-01", "db": "PLANNED-DB-002-01", "ui": "PLANNED-UI-002-01", "test": "WFTEST-002-001"}
        ],
        "open_questions": [
            {"id": "OQ-WF02-01", "subject": "Hardware FIDO2 Security Keys", "query": "Should staff be issued physical USB FIDO2 tokens instead of mobile phone authenticator apps?", "impact": "Improves security and removes personal phone dependency.", "owner": "CISO", "milestone": "Milestone 3"}
        ],
        "assumptions": [
            {"id": "ASM-WF02-01", "cat": "Staff", "statement": "All clinic staff have registered mobile phones or authenticator devices.", "status": "CONFIRMED", "risk": "Backup SMS pathway required."}
        ],
        "risks": [
            {"id": "RSK-WF02-01", "desc": "Staff writing passwords on sticky notes attached to monitors.", "prob": "High", "impact": "High", "mitigation": "Quick 4-digit PIN unlock reduces password entry friction; physical security audits.", "contingency": "Enforce mandatory password changes.", "owner": "Clinic Coordinator"}
        ],
        "change_impact": [
            {"vector": "MFA Policy Mandate Change", "scenario": "Government mandates biometric MFA for all government healthcare logins.", "components": "Login UI, biometric driver bridge, auth gateway", "severity": "MEDIUM", "testing": "Biometric hardware integration regression suite"}
        ],
        "definition_of_ready": [
            {"id": "DOR-WF02-01", "criterion": "Auth specification approved by Security Officer.", "artifact": "WF-002 Doc", "signoff": "CISO"}
        ],
        "definition_of_done": [
            {"id": "DOD-WF02-01", "criterion": "100% pass on OWASP authentication security test suite.", "method": "Automated penetration test", "benchmark": "Zero high/critical findings"}
        ],
        "related_workflows": [
            {"rel": "Dependent Workflow", "id": "WF-001", "name": "Master Clinic Operational Day", "interface": "Staff Authentication Prerequisite"}
        ]
    }
    return build_workflow_object(spec)

def make_wf03_data():
    wf_meta = WORKFLOW_MAP["WF-003"]
    wfid = "WF-003"
    wfnum = "03"

    spec = {
        "id": wfid, "num": wfnum, "name": wf_meta["name"], "domain": wf_meta["domain"],
        "exec_summary": {
            "purpose": "Governs the intake and registration of citizens into the Namma Clinic primary care ecosystem. Captures bilingual demographics, executes Aadhaar OTP / Biometric ABHA creation, mints local municipal UHID identifiers, runs duplicate detection heuristics (Levenshtein distance & Soundex), links pediatric guardians, and generates physical barcoded clinic cards.",
            "rationale": "Accurate patient identification is the bedrock of longitudinal clinical care, chronic disease tracking, and DPDP Act compliance. Rapid intake without duplicate records prevents fragmented medical histories and ensures universal primary care access.",
            "clinical_impact": "Establishes the patient's master clinical index, linking all future diagnoses, vitals, prescriptions, and lab tests to a single verified healthcare identity.",
            "system_impact": "Feeds new citizen records into local SQLite and central PostgreSQL repositories; orchestrates ABDM M1 Milestone touchpoints via the National Health Authority gateway.",
            "risk_profile": "Duplicate record proliferation, identity theft, Aadhaar OTP delivery timeouts, misspelling of regional names, and paper card loss."
        },
        "objectives": [
            {"id": "OBJ-WF03-01", "title": "Rapid Citizen Registration", "desc": "Complete new citizen registration and card printing within 90 seconds.", "metric": "Intake Latency p95 <= 90 sec", "verification": "Registration session duration telemetry"},
            {"id": "OBJ-WF03-02", "title": "ABDM ABHA Generation Rate", "desc": "Achieve >= 80% ABHA linking for citizens presenting valid Aadhaar credentials.", "metric": "ABHA Generation Success Rate >= 80%", "verification": "ABDM Gateway transaction receipts"},
            {"id": "OBJ-WF03-03", "title": "Zero Duplicate Patient Creation", "desc": "Identify and prevent 100% of duplicate patient records using phonetic and demographic matching.", "metric": "Duplicate Creation Rate = 0.00%", "verification": "Periodic deduplication audit queries"},
            {"id": "OBJ-WF03-04", "title": "Autonomous Offline Registration", "desc": "Enable provisional registration during total internet outages without blocking patient care.", "metric": "Offline Intake Availability = 100%", "verification": "Offline registration queue sync verification"}
        ],
        "in_scope": [
            {"area": "Demographic Capture", "desc": "Full name, age/DOB, gender, mobile phone, ward address in English and Kannada."},
            {"area": "ABHA Creation & Linking", "desc": "Aadhaar OTP and demographic-based ABHA creation via ABDM M1 APIs."},
            {"area": "Local UHID Minting", "desc": "Municipal hierarchical ID generation (`BLR-W085-YYYYMMDD-XXXX`)."},
            {"area": "Deduplication Screening", "desc": "Soundex, double-metaphone, and phone number collision detection."},
            {"area": "Physical Card Output", "desc": "Thermal printing of 58mm/80mm clinic cards with scannable QR code."}
        ],
        "out_of_scope": [
            {"area": "National Passport/Visa Validation", "desc": "Citizenship immigration verification.", "handoff": "Ministry of External Affairs Portal"},
            {"area": "UIDAI Demographic Updates", "desc": "Updating official Aadhaar residential address.", "handoff": "Aadhaar Seva Kendra Centers"}
        ],
        "actors": [
            {"id": "ACT-WF03-01", "type": "Human", "name": "Registration Clerk / Staff Nurse", "responsibilities": "Collects demographics, assists citizen with ABHA OTP, captures photo, prints card.", "permissions": "Patient Create, Demographics Edit, Card Print", "failure_duty": "Issues manual paper slip if printer fails; flags duplicate candidates.", "inputs": "Citizen declarations, Aadhaar card, phone number", "decisions": "Determines priority category (Senior, ANC, Pediatric, General).", "outputs": "Registered patient profile, printed thermal card", "recovery": "Re-enters corrected demographic fields."},
            {"id": "ACT-WF03-02", "type": "Human", "name": "Citizen / Patient", "responsibilities": "Declares personal information, provides Aadhaar consent, declares phone number.", "permissions": "Self-Declaration, Consent Grant/Withdraw", "failure_duty": "Provides alternative ID if Aadhaar unavailable.", "inputs": "Verbal information, Aadhaar OTP from phone", "decisions": "Consents to ABHA creation and data sharing.", "outputs": "Receives physical card and SMS", "recovery": "Requests correction of misspelled name."},
            {"id": "ACT-WF03-03", "type": "System", "name": "ABDM Gateway Bridge Daemon", "responsibilities": "Communicates with National Health Authority servers for Aadhaar OTP and ABHA tokens.", "permissions": "ABDM API Invocation", "failure_duty": "Falls back to local provisional registration during national gateway outages.", "inputs": "Encrypted Aadhaar OTP requests", "decisions": "Verifies e-KYC response payload integrity.", "outputs": "ABHA Address, ABHA Number, e-KYC profile", "recovery": "Retries failed transactions with exponential backoff."}
        ],
        "personas": [
            {"id": "PERSONA-007", "name": "Lakshmamma", "role": "Elderly Citizen Patient", "env": "Arrives at registration counter; speaks only Kannada; holds paper Aadhaar slip.", "goals": "Get registered quickly without complicated questions; receive a durable card.", "pain_points": "Cannot read English letters; forgets mobile phone OTP; fear of digital scanners.", "adaptations": "Clerk enters details in Kannada; biometric thumbprint option for ABHA."},
            {"id": "PERSONA-001", "name": "Sister Bhavani Gowda", "role": "Registration Nurse", "env": "High-speed registration counter handling 100+ citizens in 2 hours.", "goals": "Complete registration in under 60 seconds per patient without typos.", "pain_points": "Typing Kannada names phonetically; slow OTP arrivals; printer jams.", "adaptations": "Auto-transliteration engine converts English typing to accurate Kannada script."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-001", "title": "Staff Nurse / ANM", "read": "Patient Demographics, Vitals", "create": "Patient Profile, UHID, Card", "update": "Phone, Address, Priority", "delete": "None", "override": "Provisional Registration", "signoff": "Intake Form"},
            {"role": "ROLE-006", "title": "Registration Clerk", "read": "Patient Demographics", "create": "Patient Profile, UHID, Card", "update": "Demographics", "delete": "None", "override": "None", "signoff": "Intake Form"},
            {"role": "ROLE-002", "title": "Medical Officer", "read": "Complete Patient Profile", "create": "None", "update": "Medical Alerts, Allergies", "delete": "None", "override": "Merge Duplicate Records", "signoff": "Record Merge"}
        ],
        "preconditions": [
            {"id": "PRE-WF03-01", "desc": "Clinic operating session is active and registration counter unlocked.", "check": "clinic_session.status == 'ACTIVE'", "on_fail": "Coordinator must initialize daily session."},
            {"id": "PRE-WF03-02", "desc": "Thermal slip printer loaded with 58mm/80mm continuous paper roll.", "check": "printer.paper_status == 'OK'", "on_fail": "Load paper roll before starting registration."}
        ],
        "triggers": [
            {"id": "TRIG-WF03-01", "class": "User Trigger", "event": "Citizen arrives at clinic and Clerk clicks 'New Patient Registration'", "source": "Registration UI", "payload": "{ desk_id: 1, operator_id }", "latency": "< 100ms to load intake form"},
            {"id": "TRIG-WF03-02", "class": "External Trigger", "event": "Citizen scans clinic ABDM QR code via smartphone (Scan & Share)", "source": "ABDM Gateway Webhook", "payload": "{ abha_address, ekyc_profile }", "latency": "< 2 sec to auto-populate form"}
        ],
        "inputs": [
            {"name": "full_name_en", "type": "String(100)", "req": "Mandatory", "source": "Citizen / Clerk", "val": "Alphabetic string with spaces regex ^[A-Za-z\\s.]{2,100}$", "priv": "PII", "enc": "AES-256 at rest", "ex": "Lakshmamma Gowda", "on_err": "Prompt valid name"},
            {"name": "full_name_kn", "type": "String(100)", "req": "Mandatory", "source": "Auto-Transliteration", "val": "Unicode Kannada UTF-8 string", "priv": "PII", "enc": "AES-256 at rest", "ex": "ಲಕ್ಷ್ಮಮ್ಮ ಗೌಡ", "on_err": "Manual Kannada keyboard input"},
            {"name": "mobile_phone", "type": "String(10)", "req": "Optional", "source": "Citizen", "val": "10-digit Indian mobile regex ^[6-9]\\d{9}$", "priv": "PII", "enc": "AES-256 at rest", "ex": "9845012345", "on_err": "Flag as provisional phone"},
            {"name": "gender", "type": "Enum", "req": "Mandatory", "source": "Citizen", "val": "FEMALE | MALE | TRANSGENDER | OTHER", "priv": "PII", "enc": "Plaintext indexed", "ex": "FEMALE", "on_err": "Select gender option"},
            {"name": "age_years", "type": "Integer", "req": "Mandatory", "source": "Citizen", "val": "0 <= age <= 125", "priv": "PII", "enc": "Plaintext indexed", "ex": "68", "on_err": "Enter valid age in years"},
            {"name": "ward_number", "type": "String(10)", "req": "Mandatory", "source": "Clerk", "val": "BBMP Ward Code (e.g. Ward 085)", "priv": "Operational", "enc": "Plaintext indexed", "ex": "Ward 085", "on_err": "Select ward from list"},
            {"name": "aadhaar_number", "type": "String(12)", "req": "Optional", "source": "Citizen (Encrypted Pad)", "val": "12-digit numeric Aadhaar (masked; never stored)", "priv": "Restricted PII", "enc": "Zero storage; transient hash", "ex": "XXXXXXXX4829", "on_err": "Prompt 12-digit Aadhaar"}
        ],
        "outputs": {
            "success": [
                {"name": "Master Patient Record", "desc": "Longitudinal patient index record created in database.", "format": "Database Entity & FHIR Patient Resource", "recipient": "Master Patient Index"},
                {"name": "Physical Thermal Clinic Card", "desc": "58mm thermal paper slip with UHID, photo, name, and QR code.", "format": "ESC/POS Thermal Printout", "recipient": "Citizen Patient"},
                {"name": "Welcome SMS Notification", "desc": "Kannada SMS confirming registration and providing UHID.", "format": "Bilingual SMS", "recipient": "Citizen Mobile Phone"}
            ],
            "partial": [
                {"name": "Provisional Unverified Record", "desc": "Registration saved without ABHA or Aadhaar KYC verification.", "format": "Local Database Record", "fallback": "Marked 'Provisional'; prompt ABHA link on return"}
            ],
            "error": [
                {"name": "Registration Rejection Notice", "desc": "Returned when duplicate citizen record is confirmed.", "code": "ERR-REG-DUPLICATE-CITIZEN", "msg": "Citizen already registered under UHID BLR-W085-202601-0042."}
            ],
            "events": [
                {"topic": "namma.clinic.patient.registered", "desc": "Emitted upon successful creation of new patient profile.", "schema": "{ patient_id, uhid, abha_address, ward, created_at }"}
            ]
        },
        "happy_path": [
            {"title": "Citizen Intake Initiation", "actor": "Registration Clerk (`ACT-WF03-01`)", "input": "Citizen approaches desk", "action": "Clicks 'New Patient Intake' button.", "sys_behavior": "Renders bilingual intake form; checks thermal printer readiness.", "validation": "Printer ready", "db_effect": "None", "ui_effect": "Displays registration fields with cursor on Name.", "api_effect": "GET /api/v1/registration/form", "audit_effect": "None", "output": "Intake form ready", "next_state": "WFSTATE-003-001", "failure_possibility": "Terminal lag."},
            {"title": "Identity Document Screening", "actor": "Registration Clerk (`ACT-WF03-01`)", "input": "Citizen presents physical Aadhaar card", "action": "Inspects document; selects 'Aadhaar ABHA Registration'.", "sys_behavior": "Activates encrypted Aadhaar number input field.", "validation": "Aadhaar format valid", "db_effect": "None", "ui_effect": "Displays Aadhaar consent modal in Kannada.", "api_effect": "None", "audit_effect": "None", "output": "Consent modal open", "next_state": "WFSTATE-003-002", "failure_possibility": "Citizen refuses consent."},
            {"title": "Aadhaar Consent & OTP Request", "actor": "Citizen (`PERSONA-007`) & Clerk", "input": "Citizen verbally consents; enters 12-digit Aadhaar number", "action": "Clerk clicks 'Send Aadhaar OTP'.", "sys_behavior": "Transmits request to ABDM Bridge; UIDAI sends 6-digit OTP.", "validation": "Aadhaar checksum valid", "db_effect": "Logs OTP request timestamp", "ui_effect": "Shows 60-second OTP countdown timer.", "api_effect": "POST /api/v1/abdm/m1/aadhaar/send-otp", "audit_effect": "WFAUDIT-003-001 (Aadhaar OTP Requested)", "output": "OTP dispatched", "next_state": "WFSTATE-003-003", "failure_possibility": "UIDAI gateway timeout."},
            {"title": "OTP Verification & e-KYC Retrieval", "actor": "Citizen (`PERSONA-007`) & Clerk", "input": "Citizen reads 6-digit OTP from mobile phone", "action": "Clerk enters OTP and submits.", "sys_behavior": "ABDM Bridge verifies OTP; retrieves e-KYC profile (Name, DOB, Gender, Address).", "validation": "OTP valid and unexpired", "db_effect": "None", "ui_effect": "Auto-populates registration form fields.", "api_effect": "POST /api/v1/abdm/m1/aadhaar/verify-otp", "audit_effect": "WFAUDIT-003-002 (e-KYC Retrieved)", "output": "Populated demographics", "next_state": "WFSTATE-003-004", "failure_possibility": "Invalid OTP."},
            {"title": "Bilingual Demographics Transliteration", "actor": "Registration Clerk (`ACT-WF03-01`)", "input": "Populated English demographic data", "action": "Reviews auto-transliterated Kannada name: 'ಲಕ್ಷ್ಮಮ್ಮ ಗೌಡ'.", "sys_behavior": "Transliteration engine checks regional phonetic dictionary.", "validation": "Kannada string valid UTF-8", "db_effect": "None", "ui_effect": "Displays verified Kannada text box.", "api_effect": "POST /api/v1/util/transliterate", "audit_effect": "None", "output": "Bilingual demographic record", "next_state": "WFSTATE-003-005", "failure_possibility": "Phonetic misspelling."},
            {"title": "Local Contact & Ward Details Entry", "actor": "Registration Clerk (`ACT-WF03-01`)", "input": "Local phone number, ward, emergency contact name", "action": "Enters local municipal details.", "sys_behavior": "Validates ward against BBMP master ward registry.", "validation": "Ward exists in BBMP registry", "db_effect": "None", "ui_effect": "Ward selector marks Green checkmark.", "api_effect": "None", "audit_effect": "None", "output": "Completed demographic set", "next_state": "WFSTATE-003-006", "failure_possibility": "Invalid ward."},
            {"title": "Webcam Photo Capture", "actor": "Registration Clerk (`ACT-WF03-01`)", "input": "Citizen sits before USB webcam", "action": "Captures facial portrait photo.", "sys_behavior": "Compresses image to 150x150 JPEG (size < 15KB); applies auto-crop.", "validation": "Image size <= 15KB", "db_effect": "Saves thumbnail blob to local DB", "ui_effect": "Displays portrait photo preview on card preview tile.", "api_effect": "None", "audit_effect": "None", "output": "Patient photo asset", "next_state": "WFSTATE-003-007", "failure_possibility": "Webcam disconnected."},
            {"title": "Real-Time Deduplication Screening", "actor": "System (`ACT-WF03-03`)", "input": "Name, phone, age, gender, ward", "action": "Executes fuzzy matching against master database.", "sys_behavior": "Runs Soundex + Levenshtein distance check across 50,000 ward records.", "validation": "Deduplication score < 0.80 (Zero exact match)", "db_effect": "None", "ui_effect": "Green banner: 'No Duplicate Records Found'.", "api_effect": "POST /api/v1/patients/dedup-check", "audit_effect": "WFAUDIT-003-003 (Deduplication Screened)", "output": "Clearance for new UHID", "next_state": "WFSTATE-003-008", "failure_possibility": "Duplicate candidate detected (>0.85)."},
            {"title": "UHID Minting & Master Record Creation", "actor": "System (`ACT-WF03-03`)", "input": "Verified registration dataset", "action": "Allocates next sequential UHID: `BLR-W085-202609-0012`.", "sys_behavior": "Inserts record into `patients` table within atomic transaction.", "validation": "UHID globally unique", "db_effect": "Inserts row in `patients` and `patient_identities`", "ui_effect": "Displays final card preview with minted UHID.", "api_effect": "POST /api/v1/patients/create", "audit_effect": "WFAUDIT-003-004 (Patient Created)", "output": "Active patient entity", "next_state": "WFSTATE-003-009", "failure_possibility": "UUID collision (near-zero probability)."},
            {"title": "Thermal Clinic Card Printing", "actor": "Registration Clerk (`ACT-WF03-01`)", "input": "Click 'Print Clinic Card & Issue Token'", "action": "Spools print job to thermal slip printer.", "sys_behavior": "Generates 58mm ESC/POS bitmap with photo, Kannada name, UHID, and QR code.", "validation": "ESC/POS buffer acknowledge OK", "db_effect": "Logs card print event in audit table", "ui_effect": "Thermal printer dispenses physical card slip.", "api_effect": "POST /api/v1/hardware/printer/print-card", "audit_effect": "WFAUDIT-003-005 (Card Printed)", "output": "Physical clinic card", "next_state": "WFSTATE-003-010", "failure_possibility": "Paper jam."},
            {"title": "Welcome SMS & Queue Token Auto-Enqueue", "actor": "System (`ACT-WF03-03`)", "input": "Patient ID, phone number", "action": "Sends Kannada SMS welcome and queues patient for triage.", "sys_behavior": "Dispatches SMS via telecom gateway; inserts token into Triage Queue.", "validation": "SMS queued successfully", "db_effect": "Inserts row in `patient_queue_tokens`", "ui_effect": "Screen shows: 'Patient Enqueued to Triage - Token GEN-002'.", "api_effect": "POST /api/v1/tokens/generate", "audit_effect": "WFAUDIT-003-006 (Enqueued to Triage)", "output": "Citizen directed to Triage station", "next_state": "WFSTATE-003-011", "failure_possibility": "SMS gateway failure."}
        ],
        "alternate_flows": [
            {
                "id": "WFALT-003-001", "title": "Registration Without Aadhaar (Non-ABHA Track)",
                "condition": "Citizen does not have or declines to use Aadhaar card.",
                "from_step": "WFSTEP-003-002",
                "steps": [
                    "Clerk selects 'Alternative ID Registration' (Ration Card, Voter ID, Driving License, or Self-Declaration).",
                    "Clerk enters ID type and number; manually fills demographic fields.",
                    "System flags profile as 'Local Only - Non-ABDM'.",
                    "Proceeds with local UHID allocation and card printing."
                ],
                "rejoin": "Rejoins main flow at Step WFSTEP-003-006 (Local Contact Entry).",
                "audit": "WFAUDIT-003-ALT01 (Alternative ID Registration)"
            },
            {
                "id": "WFALT-003-002", "title": "Pediatric Registration (< 18 Years) with Guardian Linking",
                "condition": "Citizen being registered is an infant or child under 18 years old.",
                "from_step": "WFSTEP-003-001",
                "steps": [
                    "Clerk enters child DOB; system activates 'Parent / Guardian Mandatory' fields.",
                    "Clerk scans mother or father's existing clinic card UHID.",
                    "System links child record as dependent to parent's master household index.",
                    "Parent signs digital consent on behalf of minor."
                ],
                "rejoin": "Rejoins main flow at Step WFSTEP-003-007 (Photo Capture).",
                "audit": "WFAUDIT-003-ALT02 (Pediatric Guardian Linked)"
            },
            {
                "id": "WFALT-003-003", "title": "Offline Registration During Total Network Outage",
                "condition": "Clinic broadband is severed; ABDM gateway unreachable.",
                "from_step": "WFSTEP-003-002",
                "steps": [
                    "System automatically disables online Aadhaar OTP verification.",
                    "Enters 'Local Provisional Registration Mode'.",
                    "Mints provisional UHID prefixed with `BLR-W085-PROV-XXXX`.",
                    "Buffers registration record in local encrypted write-ahead log for cloud sync."
                ],
                "rejoin": "Rejoins main flow at Step WFSTEP-003-005 with provisional record.",
                "audit": "WFAUDIT-003-ALT03 (Provisional Offline Registration)"
            }
        ],
        "exception_flows": [
            {
                "id": "WFEX-003-001", "title": "Aadhaar OTP Delivery Timeout",
                "trigger": "Citizen does not receive 6-digit OTP after 60 seconds due to telecom delay.",
                "detection": "UI countdown timer expires.",
                "containment": "Offers 'Resend OTP' button (max 2 retries) or 'Switch to Manual Registration'.",
                "msg_en": "Aadhaar OTP delayed. You can resend OTP or proceed with manual registration.",
                "msg_kn": "ಆಧಾರ್ OTP ಬಂದಿಲ್ಲ. ಮರುಕಳುಹಿಸಿ ಅಥವಾ ಹಸ್ತಚಾಲಿತ ನೋಂದಣಿಯೊಂದಿಗೆ ಮುಂದುವರಿಯಿರಿ.",
                "recovery": "Clerk switches to alternative ID registration without denying care.",
                "audit": "WFAUDIT-003-EX01", "severity": "LOW"
            },
            {
                "id": "WFEX-003-002", "title": "High-Confidence Duplicate Citizen Match Detected",
                "trigger": "Soundex and phone number match existing patient with 92% confidence score.",
                "detection": "Deduplication screening query returns candidate record.",
                "containment": "Halts new record creation; displays side-by-side comparison modal.",
                "msg_en": "Potential duplicate record detected. Please verify if citizen is already registered.",
                "msg_kn": "ಈಗಾಗಲೇ ನೋಂದಾಯಿತವಾಗಿರುವ ಸಾಧ್ಯತೆ ಇದೆ. ದಯವಿಟ್ಟು ಪರಿಶೀಲಿಸಿ.",
                "recovery": "Clerk verifies photo and details; if same person, opens existing record under WF-005.",
                "audit": "WFAUDIT-003-EX02", "severity": "MEDIUM"
            }
        ],
        "emergency_flow": {
            "triggers": "Unconscious trauma patient or acute collapse arriving at clinic door.",
            "escalation": "Clerk hits 'Emergency Fast-Track Bypass' button.",
            "preemption": "Skips all demographic entry, Aadhaar OTP, and consent dialogs.",
            "bypass_rules": "Auto-mints emergency proxy identity `EMG-PROXY-YYYYMMDD-01` in < 2 seconds.",
            "safety_controls": "Allows immediate triage and doctor examination without waiting for registration.",
            "reconciliation": "Clerk or ASHA worker completes formal identity intake post-stabilization.",
            "audit_event": "WFAUDIT-003-EMERGENCY (Emergency Proxy Created)",
            "signoff_sla": "4 hours post-stabilization administrative reconciliation"
        },
        "states": [
            {"name": "REGISTRATION_IDLE", "desc": "Counter ready for new citizen intake.", "allowed": "Start intake, scan QR", "prohibited": "Unassigned token print", "actor": "Registration Clerk"},
            {"name": "DEMOGRAPHICS_ENTRY", "desc": "Capturing personal, contact, and ward information.", "allowed": "Field entry, transliteration", "prohibited": "Encounter creation", "actor": "Registration Clerk"},
            {"name": "ABDM_KYC_PENDING", "desc": "Awaiting Aadhaar OTP verification from UIDAI.", "allowed": "OTP entry, resend, cancel", "prohibited": "UHID minting", "actor": "Citizen & Clerk"},
            {"name": "DEDUP_SCREENING", "desc": "System evaluating phonetic and demographic uniqueness.", "allowed": "Matching evaluation", "prohibited": "Manual override", "actor": "System Daemon"},
            {"name": "CARD_PRINTING", "desc": "Spooling thermal clinic card to hardware printer.", "allowed": "Print, paper status check", "prohibited": "Queue advancement", "actor": "Edge Orchestrator"},
            {"name": "REGISTRATION_COMPLETED", "desc": "Citizen registered, card issued, queued for triage.", "allowed": "Queue advancement, SMS dispatch", "prohibited": "Duplicate entry", "actor": "System"}
        ],
        "transitions": [
            {"from_state": "REGISTRATION_IDLE", "event": "Click New Patient", "actor": "Clerk", "condition": "Session active", "validation": "Session check", "to_state": "DEMOGRAPHICS_ENTRY", "side_effects": "Render form", "audit": "WFAUDIT-003-TR01"},
            {"from_state": "DEMOGRAPHICS_ENTRY", "event": "Request Aadhaar OTP", "actor": "Citizen", "condition": "Aadhaar provided", "validation": "Checksum valid", "to_state": "ABDM_KYC_PENDING", "side_effects": "Call ABDM API", "audit": "WFAUDIT-003-TR02"},
            {"from_state": "ABDM_KYC_PENDING", "event": "OTP Verified", "actor": "Clerk", "condition": "OTP matches", "validation": "ABDM ACK OK", "to_state": "DEDUP_SCREENING", "side_effects": "Populate eKYC", "audit": "WFAUDIT-003-TR03"},
            {"from_state": "DEDUP_SCREENING", "event": "Zero Duplicate Found", "actor": "System", "condition": "Score < 0.80", "validation": "Index check", "to_state": "CARD_PRINTING", "side_effects": "Mint UHID", "audit": "WFAUDIT-003-TR04"},
            {"from_state": "CARD_PRINTING", "event": "Print Acknowledged", "actor": "Printer", "condition": "Paper dispensed", "validation": "ESC/POS OK", "to_state": "REGISTRATION_COMPLETED", "side_effects": "Enqueue to Triage", "audit": "WFAUDIT-003-TR05"}
        ],
        "decision_tables": [
            {
                "id": "WFDEC-003-001", "title": "Patient Priority Category Allocation Matrix",
                "desc": "Determines queue category prefix based on citizen demographic and physiological markers.",
                "conditions": ["Age >= 65", "Pregnant / ANC", "Pediatric Age < 5", "Acute Danger Sign Present"],
                "actions": ["Assign EMG Prefix", "Assign ANC Prefix", "Assign SNR Prefix", "Assign PED Prefix", "Assign GEN Prefix"],
                "rows": [
                    {"rule": "P1", "cond_vals": ["ANY", "ANY", "ANY", "YES"], "act_vals": ["YES", "NO", "NO", "NO", "NO"]},
                    {"rule": "P2", "cond_vals": ["ANY", "YES", "NO", "NO"], "act_vals": ["NO", "YES", "NO", "NO", "NO"]},
                    {"rule": "P3", "cond_vals": ["YES", "NO", "NO", "NO"], "act_vals": ["NO", "NO", "YES", "NO", "NO"]},
                    {"rule": "P4", "cond_vals": ["NO", "NO", "YES", "NO"], "act_vals": ["NO", "NO", "NO", "YES", "NO"]},
                    {"rule": "P5", "cond_vals": ["NO", "NO", "NO", "NO"], "act_vals": ["NO", "NO", "NO", "NO", "YES"]}
                ]
            }
        ],
        "validation_rules": [
            {"id": "WFVAL-003-001", "field": "full_name_en", "expr": "len(name) >= 2 and regex_match('^[A-Za-z\\s.]+$', name)", "code": "ERR-VAL-03-01", "msg_en": "Full name must be at least 2 characters and contain only letters.", "msg_kn": "ಪೂರ್ಣ ಹೆಸರು ಕನಿಷ್ಠ 2 ಅಕ್ಷರಗಳನ್ನು ಹೊಂದಿರಬೇಕು.", "recovery": "Re-enter name.", "test_ref": "WFTEST-003-001"},
            {"id": "WFVAL-003-002", "field": "mobile_phone", "expr": "phone == null or regex_match('^[6-9]\\d{9}$', phone)", "code": "ERR-VAL-03-02", "msg_en": "Mobile number must be a valid 10-digit Indian number starting with 6-9.", "msg_kn": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ 10 ಅಂಕಿಗಳ ಮಾನ್ಯ ಸಂಖ್ಯೆಯಾಗಿರಬೇಕು.", "recovery": "Re-enter 10-digit phone.", "test_ref": "WFTEST-003-002"}
        ],
        "business_rules": [
            {"id": "BRULE-WF03-001", "title": "Free Registration Card Issuance", "req": "BRULE-003", "spec": "Every citizen shall receive their initial registration and printed clinic card completely free of charge.", "enforcement": "System does not feature any fee generation in registration module.", "consequence": "Zero financial barrier to healthcare access."}
        ],
        "clinical_rules": [
            {"id": "CR-WF03-001", "title": "Mandatory Age-Appropriate Clinical Routing", "req": "CR-003", "rationale": "Infants < 5 and seniors >= 65 have higher physiological vulnerability to rapid deterioration.", "logic": "System tags priority tokens to expedite nurse triage queue entry.", "override_policy": "None. Priority queueing is automatic.", "safety_invariant": "Vulnerable cohorts receive priority queue allocation."}
        ],
        "operational_rules": [
            {"id": "OR-WF03-001", "title": "Zero Document Rejection Policy", "req": "OR-003", "mandate": "No citizen shall be turned away due to lack of identity documentation.", "boundary": "Registration desk.", "exception": "None. Universal provisional registration must be offered."}
        ],
        "security_controls": [
            {"domain": "Data Encryption", "id": "SEC-WF03-01", "spec": "Patient PII encrypted with AES-256-GCM at rest; Aadhaar number never stored.", "param": "AES-256-GCM", "threat": "Identity database leakage", "compliance": "SECR-003"}
        ],
        "privacy_controls": [
            {"principle": "Consent Verification", "id": "PRIV-WF03-01", "spec": "Digital consent captured before linking ABDM ABHA health records.", "invariant": "Explicit consent recorded", "right": "DPDP Act Sec 6"}
        ],
        "offline_behavior": {
            "online_mode": "Real-time ABHA verification via ABDM Gateway; deduplication across central municipal database.",
            "detection_latency": "< 1 second.",
            "local_storage": "Local encrypted SQLite table storing provisional registrations.",
            "queue_mechanics": "Queues provisional records in local mutation log; syncs upon reconnection.",
            "degraded_scope": "Full registration supported using local UHID prefix `BLR-W085-PROV-`.",
            "sync_convergence": "Reconciles provisional records with central repository upon reconnection.",
            "conflict_invariants": "Provisional UHID preserved as secondary alias during central merge."
        },
        "diagrams": {
            "data_flow": """flowchart TD
    Citizen["Citizen Patient"] -->|Declares Demographics| Clerk["Registration Clerk"]
    Clerk -->|Inputs Form| UI["Registration UI"]
    UI -->|Aadhaar OTP| Bridge["ABDM Gateway Bridge"]
    Bridge -->|e-KYC Response| UI
    UI -->|Dedup Query| LocalDB[("Local SQLite DB")]
    UI -->|Mint UHID| LocalDB
    UI -->|Print Command| Printer["Thermal Slip Printer"]
    Printer --> Card["Printed Clinic Card with QR"]
    Card --> Citizen""",
            "sequence": """sequenceDiagram
    actor C as Citizen
    actor N as Registration Clerk
    participant UI as Registration UI
    participant G as ABDM Gateway
    participant DB as SQLite DB
    C->>N: 1. Presents for registration
    N->>UI: 2. Enter demographics & Aadhaar
    UI->>G: 3. Request Aadhaar OTP
    G-->>C: 4. SMS OTP delivered to mobile
    C->>N: 5. Declares 6-digit OTP
    N->>UI: 6. Submit OTP
    UI->>G: 7. Verify OTP
    G-->>UI: 8. Return verified e-KYC
    UI->>DB: 9. Dedup check & Mint UHID
    DB-->>UI: 10. UHID allocated
    UI-->>N: 11. Trigger thermal card print
    N-->>C: 12. Hand over printed clinic card""",
            "activity": """flowchart TD
    Start([Citizen at Desk]) --> SelectType{Has Aadhaar?}
    SelectType -- Yes --> EnterAadhaar[Enter Aadhaar on Keypad] --> SendOTP[Send OTP via ABDM Bridge]
    SendOTP --> EnterOTP[Enter 6-Digit OTP] --> VerifyKYC{OTP Valid?}
    VerifyKYC -- Yes --> PopulateFields[Auto-Populate e-KYC Data] --> TranslitKannada[Transliterate to Kannada]
    VerifyKYC -- No --> RetryOTP{Retry OTP?}
    RetryOTP -- Yes --> SendOTP
    RetryOTP -- No --> ManualIntake
    SelectType -- No --> ManualIntake[Manual Demographic Intake] --> TranslitKannada
    TranslitKannada --> CapturePhoto[Capture Webcam Photo] --> DedupCheck{Duplicate Exists?}
    DedupCheck -- Yes --> AlertDuplicate[Alert Duplicate Candidate] --> OpenExisting[Open Existing Record]
    DedupCheck -- No --> MintUHID[Mint Unique Local UHID] --> PrintCard[Print Thermal Card with QR]
    PrintCard --> EnqueueTriage[Auto-Enqueue to Triage] --> End([Intake Complete])""",
            "state": """stateDiagram-v2
    [*] --> REGISTRATION_IDLE
    REGISTRATION_IDLE --> DEMOGRAPHICS_ENTRY: Start New Intake
    DEMOGRAPHICS_ENTRY --> ABDM_KYC_PENDING: Request Aadhaar OTP
    ABDM_KYC_PENDING --> DEDUP_SCREENING: OTP Verified
    DEMOGRAPHICS_ENTRY --> DEDUP_SCREENING: Manual Intake Selected
    DEDUP_SCREENING --> CARD_PRINTING: Zero Duplicate Match
    DEDUP_SCREENING --> REGISTRATION_IDLE: Duplicate Record Opened
    CARD_PRINTING --> REGISTRATION_COMPLETED: Card Printed & Token Issued
    REGISTRATION_COMPLETED --> [*]"""
        },
        "data_flow_nodes": [
            {"name": "UI", "desc": "Registration web application running in kiosk mode.", "protocol": "HTTPS", "encryption": "TLS 1.3"},
            {"name": "Bridge", "desc": "ABDM connector microservice communicating with NHA gateway.", "protocol": "HTTPS JSON-LD", "encryption": "TLS 1.3 with NHA Cert"},
            {"name": "Printer", "desc": "58mm thermal slip printer connected via USB Virtual COM.", "protocol": "ESC/POS", "encryption": "Hardware Bus"}
        ],
        "failure_tree": [
            {"id": "FT-003-001", "cat": "External", "root": "UIDAI Aadhaar OTP gateway outage", "vector": "Cloud network timeout", "impact": "Cannot complete Aadhaar ABHA linking", "detection": "HTTP 504 from ABDM", "mitigation": "Switch to alternative manual registration pathway"},
            {"id": "FT-003-002", "cat": "Hardware", "root": "Thermal printer cutter jam", "vector": "Paper thickness mismatch", "impact": "Cannot dispense physical card", "detection": "Printer status error code", "mitigation": "Clear cutter jam, manual tear-off, reprint card"},
            {"id": "FT-003-003", "cat": "Software", "root": "Kannada transliteration dictionary failure", "vector": "Missing Unicode glyph", "impact": "Incorrect regional name spelling", "detection": "Clerk visual check", "mitigation": "Activate onscreen virtual Kannada keyboard"}
        ],
        "recovery_procedures": [
            {"id": "REC-WF03-01", "title": "Registration Card Reprint Runbook", "trigger": "Printer jammed or paper wrinkled during card issuance.", "containment": "Clear paper path.", "steps": ["Open printer lid and realign 58mm paper roll.", "Click 'Reprint Last Clinic Card' on Registration screen.", "System verifies identical UHID and outputs fresh card slip."], "rollback": "None", "resumption": "Hand over card to citizen.", "audit": "WFAUDIT-003-REC01"}
        ],
        "audit_events": [
            {"id": "WFAUDIT-003-001", "event": "PATIENT_INTAKE_INITIATED", "actor": "Clerk", "meta": "{ desk_id: 1 }", "state_before": "IDLE", "state_after": "INTAKE", "hmac": "HMAC-SHA256", "retention": "7 Years", "compliance": "DPDP Act"},
            {"id": "WFAUDIT-003-002", "event": "ABHA_OTP_VERIFIED", "actor": "Citizen", "meta": "{ abha_status: 'LINKED' }", "state_before": "PENDING", "state_after": "VERIFIED", "hmac": "HMAC-SHA256", "retention": "7 Years", "compliance": "ABDM Baseline"},
            {"id": "WFAUDIT-003-003", "event": "PATIENT_RECORD_CREATED", "actor": "System", "meta": "{ patient_id, uhid, ward }", "state_before": "NONE", "state_after": "CREATED", "hmac": "HMAC-SHA256", "retention": "7 Years", "compliance": "Clinical Records Act"}
        ],
        "notifications": [
            {"id": "WFNOTIF-003-01", "trigger": "Registration Complete", "recipient": "Citizen", "channel": "SMS", "text_en": "Namma Clinic: Welcome! Your registration is complete. UHID: BLR-W085-202609-0012.", "text_kn": "ನಮ್ಮ ಕ್ಲಿನಿಕ್: ಸುಸ್ವಾಗತ! ನಿಮ್ಮ ನೋಂದಣಿ ಪೂರ್ಣಗೊಂಡಿದೆ. UHID: BLR-W085-202609-0012.", "priority": "High", "retry": "1 retry after 30s", "fallback": "Physical Card"}
        ],
        "planned_apis": [
            {"id": "PLANNED-API-003-01", "method": "POST", "path": "/api/v1/patients/create", "desc": "Creates new patient master record and mints unique UHID.", "scope": "patients:create", "req_schema": "{\n  \"full_name_en\": \"Lakshmamma Gowda\",\n  \"full_name_kn\": \"ಲಕ್ಷ್ಮಮ್ಮ ಗೌಡ\",\n  \"gender\": \"FEMALE\",\n  \"age_years\": 68,\n  \"phone\": \"9845012345\",\n  \"ward\": \"Ward 085\"\n}", "res_schema": "{\n  \"patient_id\": \"string (UUID)\",\n  \"uhid\": \"BLR-W085-202609-0012\",\n  \"created_at\": \"2026-09-04T08:35:00Z\"\n}", "errors": "400 Invalid Input, 409 Duplicate Patient Detected", "idempotency": "Mandatory (Key: clerk_id + patient_phone + date)", "rate_limit": "60 req/min", "offline_support": "Local execution with provisional prefix"}
        ],
        "planned_db": [
            {"id": "PLANNED-DB-003-01", "table": "patients", "purpose": "Master longitudinal patient demographic and identity registry.", "pk": "patient_id (UUID)", "fks": "None", "cols": [
                {"name": "patient_id", "type": "UUID", "null": "NOT NULL", "notes": "Primary Key"},
                {"name": "uhid", "type": "VARCHAR(30)", "null": "NOT NULL", "notes": "Unique Health Identifier"},
                {"name": "full_name_en", "type": "VARCHAR(100)", "null": "NOT NULL", "notes": "English name"},
                {"name": "full_name_kn", "type": "VARCHAR(100)", "null": "NOT NULL", "notes": "Kannada name"},
                {"name": "gender", "type": "VARCHAR(15)", "null": "NOT NULL", "notes": "Gender classification"},
                {"name": "age_years", "type": "INTEGER", "null": "NOT NULL", "notes": "Calculated or declared age"},
                {"name": "phone", "type": "VARCHAR(10)", "null": "NULL", "notes": "10-digit mobile number"},
                {"name": "ward", "type": "VARCHAR(20)", "null": "NOT NULL", "notes": "BBMP Ward code"},
                {"name": "abha_number", "type": "VARCHAR(20)", "null": "NULL", "notes": "ABDM ABHA number"},
                {"name": "abha_address", "type": "VARCHAR(50)", "null": "NULL", "notes": "ABDM ABHA address"},
                {"name": "photo_blob_url", "type": "VARCHAR(255)", "null": "NULL", "notes": "Portrait photo path"},
                {"name": "created_at", "type": "TIMESTAMPTZ", "null": "NOT NULL", "notes": "Creation timestamp"}
            ], "indexes": "UNIQUE(uhid), INDEX(phone), INDEX(full_name_en), INDEX(ward)", "concurrency": "Optimistic Locking (version int)", "retention": "Permanent (10 years post-last visit)"}
        ],
        "planned_ui": [
            {"id": "PLANNED-UI-003-01", "screen": "Patient Intake Form", "route": "/patients/new", "persona": "Registration Clerk", "components": "Bilingual input fields, Aadhaar OTP modal, webcam portrait box, live card preview, 'Save & Print Card' button.", "states": "Initial, OTP Challenged, e-KYC Loaded, Duplicate Checking, Card Printing, Success.", "validations": "Mandatory fields validated in real-time with inline green checkmarks.", "a11y": "Keyboard tab order optimized for sub-60-second completion.", "localization": "Complete Kannada parity with automatic transliteration.", "offline_ui": "Amber banner indicates 'Local Provisional UHID Mode'."}
        ],
        "backend_reqs": {
            "domain_services": "Orchestrates `PatientRegistrationService`, `AbdmBridgeConnector`, `DeduplicationEngine`, and `CardSpoolerService`.",
            "transactions": "Atomic insertion across `patients`, `patient_identities`, and `patient_queue_tokens`.",
            "async_workers": "Background worker dispatches welcome SMS and synchronizes records to central cloud.",
            "circuit_breakers": "ABDM Gateway circuit breaker trips after 3 timeouts; switches to provisional mode."
        },
        "integrations": [
            {"id": "INT-WF03-01", "system": "ABDM National Gateway", "protocol": "HTTPS JSON-LD", "payload": "Aadhaar OTP request and e-KYC profile retrieval", "direction": "Bidirectional", "timeout": "5 sec", "fallback": "Local provisional registration track"}
        ],
        "reports": [
            {"id": "REP-WF03-01", "title": "Daily Citizen Registration Census", "freq": "Daily", "audience": "Medical Officer, Zonal Health Officer", "grain": "Per clinic, per ward, per demographic cohort", "ref": "REP-003"}
        ],
        "analytics": [
            {"id": "ANL-WF03-01", "kpi": "Registration Intake Speed", "formula": "AVG(completed_at - started_at)", "dimensions": "Clerk ID, ID Type", "target": "<= 90 seconds", "alert": "Average speed > 150s flags usability issue"}
        ],
        "ai_reqs": {
            "id": "AIR-WF03-01", "purpose": "Phonetic Deduplication Confidence Scoring", "features": "Name phonetic tokens, phone digits, birth year, ward",
            "output_signal": "Duplicate Confidence Score (0.00 to 1.00)", "confidence": "Flags candidate if score >= 0.85", "explainability": "Highlights matching phone and similar phonetic soundex.",
            "authority": "Advisory prompt to clerk; clerk retains final merge or create authority.", "audit": "WFAUDIT-003-AI01"
        },
        "stride_threats": [
            {"id": "STRIDE-WF03-01", "cat": "Information Disclosure", "asset": "Citizen Phone Number", "scenario": "Clerk leaves printed card with phone number exposed on desk.", "likelihood": "Medium", "impact": "Medium", "mitigation": "Physical handoff directly to citizen; cards never left unattended.", "residual": "Low", "test_ref": "WFTEST-003-001"}
        ],
        "linddun_threats": [
            {"id": "LINDDUN-WF03-01", "cat": "Linkability", "asset": "UHID to Aadhaar", "vector": "Correlation of UHID with public Aadhaar records.", "likelihood": "Low", "impact": "High", "mitigation": "Aadhaar numbers strictly never stored in platform database.", "compliance": "Aadhaar Act / DPDP Act"}
        ],
        "performance": {
            "e2e_latency": "Registration to card print < 60 seconds.", "ui_render": "Intake form renders in < 100ms.",
            "db_budget": "Deduplication query executes in < 25ms.", "concurrency": "20 concurrent registrations per second.",
            "payload": "Patient profile payload < 5KB.", "hardware": "RAM usage < 50MB."
        },
        "availability": {
            "sla": "99.95% registration availability.", "rto": "< 2 min.", "rpo": "0 patients lost.",
            "offline_autonomy": "100% registration continuity via local provisional UHIDs.", "failover": "Local SQLite fallback."
        },
        "accessibility": {
            "screen_reader": "Full ARIA labels on all form inputs.", "contrast": "Contrast ratio >= 4.5:1.",
            "keyboard": "Fast tab order with Enter to submit.", "touch": "Large touch targets on kiosk.", "cognitive": "Simple, clean bilingual layout."
        },
        "localization": {
            "clinical_terms": "N/A", "printed_material": "Thermal cards print Kannada and English.",
            "audio_prompts": "Kannada voice confirmation."
        },
        "test_gates": [
            {"level": "Unit Testing", "scope": "Transliteration engine, dedup algorithm", "tooling": "PyTest", "coverage": ">= 90%", "gate": "Zero test failures on pre-commit"},
            {"level": "E2E Testing", "scope": "Full registration and card print flow", "tooling": "Playwright", "coverage": "100% happy and alternate flows", "gate": "Green run on CI staging"}
        ],
        "bdd_scenarios": [
            {
                "id": "WFTEST-003-001", "title": "Successful New Citizen Registration with Aadhaar ABHA Linking",
                "category": "Happy Path", "priority": "P0",
                "given": "the registration desk is active and the thermal printer is loaded with paper",
                "given_ands": ["a 68-year-old citizen arrives with their physical Aadhaar card"],
                "when": "the clerk enters the citizen's Aadhaar number and requests an OTP",
                "when_ands": ["the citizen provides the 6-digit OTP received via SMS", "the clerk confirms the auto-populated demographic details in Kannada and English"],
                "then": "the system mints a unique UHID BLR-W085-202609-0012",
                "then_ands": ["the thermal printer dispenses a complete clinic card with embedded QR code within 60 seconds"]
            },
            {
                "id": "WFTEST-003-002", "title": "Deduplication System Detects Existing Patient Record",
                "category": "Deduplication", "priority": "P0",
                "given": "a patient is already registered under UHID BLR-W085-202601-0042 with mobile 9845012345",
                "given_ands": ["the patient returns to clinic having lost their physical card"],
                "when": "the clerk attempts to create a new registration using the same phone number",
                "when_ands": ["the deduplication engine evaluates the entered name and phone"],
                "then": "the system halts new record creation with a 95% confidence duplicate alert",
                "then_ands": ["displays the existing patient profile allowing the clerk to reprint the card instead"]
            }
        ],
        "acceptance_criteria": [
            {"id": "AC-WF-003-001", "criterion": "New patient registration completed in <= 90 seconds.", "method": "Telemetry timer", "threshold": "p95 <= 90s", "gate": "Milestone 1 Core Gate"},
            {"id": "AC-WF-003-002", "criterion": "Thermal clinic card printed with scannable QR code in <= 2 seconds.", "method": "Hardware print timer", "threshold": "p99 <= 2.0s", "gate": "Milestone 1 Core Gate"}
        ],
        "dependencies": [
            {"id": "WFDEP-003-01", "upstream": "WF-001", "downstream": "WF-003", "nature": "Operational Prerequisite", "blocking": "BLOCKING", "impact": "Cannot register patients without active clinic session.", "resilience": "None."},
            {"id": "WFDEP-003-02", "upstream": "WF-003", "downstream": "WF-007", "nature": "Token Issuance Trigger", "blocking": "BLOCKING", "impact": "Patient cannot enter queue without registered UHID.", "resilience": "Emergency exception bypass."}
        ],
        "critical_path": {
            "path": "Citizen Intake -> Aadhaar OTP -> Demographic Transliteration -> Dedup Check -> UHID Mint -> Card Print.",
            "bottleneck": "Aadhaar OTP delivery via telecom gateway can take 15-30 seconds depending on carrier.",
            "load_balancing": "Multiple registration desks active during morning rush; manual alternative ID track available.",
            "recovery_bottlenecks": "Thermal printer paper roll exhaustion."
        },
        "rollback_strategy": {
            "db_rollback": "Failed registration aborts transaction; zero orphaned records created.",
            "saga_compensation": "If card print fails, re-triggers print job without re-creating patient entity.",
            "notification_reversal": "None.",
            "audit_preservation": "All registration attempts logged permanently.",
            "offline_rollback": "Provisional records retain local state until reconciled."
        },
        "idempotency": {
            "key_schema": "UUIDv4 on `clerk_id + citizen_phone + date`.",
            "cache_store": "SQLite unique index.",
            "replay_behavior": "Replay returns existing UHID without creating duplicate.",
            "ttl": "24 hours.", "offline_replay": "Cloud sync reconciles using local UHID alias."
        },
        "concurrency": {
            "occ": "Patient table uses versioning.",
            "pessimistic": "UHID sequence counter uses atomic transaction lock.",
            "queue_locking": "None.", "deadlock_policy": "Standard database timeout."
        },
        "invariants": [
            {"id": "INVARIANT-WF-003-01", "statement": "Every registered patient must possess a globally unique UHID.", "scope": "Master Patient Index", "enforcement": "Database UNIQUE constraint on `uhid`.", "consequence": "Transaction aborts on collision."}
        ],
        "observability": [
            {"cat": "Metric", "name": "namma_clinic_registrations_total", "type": "Counter", "labels": "clinic_id, id_type", "target": "Prometheus", "alert": "Zero registrations in 2 hours during OPD alerts supervisor"}
        ],
        "runbook": {
            "morning_sop": "Check registration desk thermal printer paper. Ensure webcam is connected and aligned.",
            "live_sop": "Greet citizen respectfully in Kannada. Inquire if they have visited before. Assist with OTP.",
            "troubleshooting_sop": "If Aadhaar OTP fails twice: Click 'Alternative ID' and register using Voter ID or Ration Card.",
            "closing_sop": "Count total registered cards. Verify paper roll has sufficient stock for tomorrow."
        },
        "sla_slo": [
            {"name": "Registration Intake Time", "target": "< 90 seconds", "window": "Per patient", "warning": "> 120s", "escalation": "Coordinator alerted"}
        ],
        "traceability": [
            {"req": "FR-001", "type": "Functional Req", "step": "WFSTEP-003-009", "state": "WFSTATE-003-004", "api": "PLANNED-API-003-01", "db": "PLANNED-DB-003-01", "ui": "PLANNED-UI-003-01", "test": "WFTEST-003-001"}
        ],
        "open_questions": [
            {"id": "OQ-WF03-01", "subject": "Biometric Fingerprint Scanners at Desk", "query": "Should registration desks be equipped with optical fingerprint scanners for non-smartphone Aadhaar verification?", "impact": "Allows biometric e-KYC for citizens whose phone numbers are not linked to Aadhaar.", "owner": "Technical Architecture Board", "milestone": "Milestone 2"}
        ],
        "assumptions": [
            {"id": "ASM-WF03-01", "cat": "Connectivity", "statement": "ABDM Gateway is reachable via broadband fiber during clinic hours.", "status": "CONFIRMED", "risk": "Provisional offline registration fallback must be tested regularly."}
        ],
        "risks": [
            {"id": "RSK-WF03-01", "desc": "Citizens forgetting or losing physical paper clinic cards between visits.", "prob": "High", "impact": "Low", "mitigation": "Phone number search and QR card reprint allows instant recovery.", "contingency": "Reprint card in < 5 seconds.", "owner": "Registration Clerk"}
        ],
        "change_impact": [
            {"vector": "ABDM FHIR Patient Resource Schema Revision", "scenario": "NHA updates ABDM M1 Patient profile schema.", "components": "ABDM Bridge, e-KYC parser", "severity": "MEDIUM", "testing": "ABDM contract testing suite"}
        ],
        "definition_of_ready": [
            {"id": "DOR-WF03-01", "criterion": "Registration specification approved by Operations and ABDM leads.", "artifact": "WF-003 Doc", "signoff": "Product Manager"}
        ],
        "definition_of_done": [
            {"id": "DOD-WF03-01", "criterion": "100% pass on automated Playwright registration BDD test suite.", "method": "Automated test report", "benchmark": "Zero failures across 30 simulated intakes"}
        ],
        "related_workflows": [
            {"rel": "Upstream Dependency", "id": "WF-001", "name": "Master Clinic Day Operational Workflow", "interface": "Facility Session Active"},
            {"rel": "Downstream Workflow", "id": "WF-007", "name": "Token Generation & Queue Entry Workflow", "interface": "UHID Handoff for Queue Entry"}
        ]
    }
    return build_workflow_object(spec)

def make_wf04_data():
    wf_meta = WORKFLOW_MAP["WF-004"]
    wfid = "WF-004"
    wfnum = "04"

    spec = {
        "id": wfid, "num": wfnum, "name": wf_meta["name"], "domain": wf_meta["domain"],
        "exec_summary": {
            "purpose": "Establishes high-speed multi-parametric search heuristics to rapidly locate patient records, eliminating duplicate registrations using Kannada/English phonetic match (Soundex/Metaphone), partial mobile number, ABHA ID QR scanning, barcoded physical clinic cards, and birth year range filters.",
            "rationale": "In busy outpatient clinics handling 100+ patients daily, patients frequently forget their UHID or leave their clinic cards at home. Fast, error-tolerant search in local languages prevents duplicate file creation and ensures clinical continuity.",
            "clinical_impact": "Prevents dangerous medical history fragmentation, ensuring that chronic diseases (hypertension, diabetes), past allergic reactions, and previous lab investigations are instantly linked.",
            "system_impact": "Powers search bars across all clinic workstations (Registration, Triage, Doctor Room, Pharmacy) with < 15ms indexed lookups on local SQLite and cloud PostgreSQL.",
            "risk_profile": "Phonetic false positives, misidentifying patients with common names, slow unindexed queries degrading terminal performance, and unauthorized PHI browsing."
        },
        "objectives": [
            {"id": "OBJ-WF04-01", "title": "Sub-Second Patient Lookup", "desc": "Return matching patient records within 150ms of query submission.", "metric": "Search Latency p95 <= 150ms", "verification": "Query execution span telemetry"},
            {"id": "OBJ-WF04-02", "title": "Bilingual Phonetic Error Tolerance", "desc": "Locate correct patient despite minor spelling variations or transliteration differences.", "metric": "Phonetic Recall Rate >= 98%", "verification": "Synthetic misspelled query benchmark suite"},
            {"id": "OBJ-WF04-03", "title": "Instant QR Card Scan Verification", "desc": "Open patient record in < 50ms upon hardware barcode scanner read.", "metric": "QR Scan Lookup Latency <= 50ms", "verification": "WebSerial hardware event logs"}
        ],
        "in_scope": [
            {"area": "Exact UHID QR Scanning", "desc": "Hardware barcode scanner direct lookup on primary index."},
            {"area": "10-Digit Mobile Search", "desc": "Locates all household family members sharing a contact phone."},
            {"area": "Bilingual Phonetic Search", "desc": "Metaphone and Soundex matching across Kannada and English names."},
            {"area": "Demographic Range Filters", "desc": "Filtering candidates by age range (+/- 2 years), gender, and ward."}
        ],
        "out_of_scope": [
            {"area": "National Criminal Database Searches", "desc": "Law enforcement forensic queries.", "handoff": "Police Criminal Record Gateway"}
        ],
        "actors": [
            {"id": "ACT-WF04-01", "type": "Human", "name": "Frontline Staff Operator", "responsibilities": "Enters search query, reviews candidate photos, asks verification challenge questions.", "permissions": "Patient Search & Lookup", "failure_duty": "Refines search parameters if candidate list too broad.", "inputs": "QR code scan, mobile number, patient name", "decisions": "Selects verified patient from candidate cards.", "outputs": "Selected patient context", "recovery": "Asks for alternative identifier."},
            {"id": "ACT-WF04-02", "type": "System", "name": "Edge Search Engine", "responsibilities": "Executes FTS5 SQLite queries, computes phonetic distance, ranks candidates.", "permissions": "Read-Only Patient Index", "failure_duty": "Falls back to exact phone search if fuzzy index corrupted.", "inputs": "Search query tokens", "decisions": "Ranks candidates by relevance score.", "outputs": "Ranked candidate JSON payload", "recovery": "Rebuilds local FTS index in background."}
        ],
        "personas": [
            {"id": "PERSONA-001", "name": "Sister Bhavani Gowda", "role": "Staff Nurse", "env": "Triage cubicle; patient arrives without card.", "goals": "Find patient record in under 5 seconds by typing their mobile number.", "pain_points": "Long candidate lists with identical names.", "adaptations": "Shows age and ward badge prominently on candidate cards."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "Patient Demographic Search", "create": "None", "update": "None", "delete": "None", "override": "None", "signoff": "Search Action"},
            {"role": "ROLE-002", "title": "Medical Officer", "read": "Full Patient Search & EHR", "create": "None", "update": "None", "delete": "None", "override": "Break-Glass Search", "signoff": "Record Access"}
        ],
        "preconditions": [
            {"id": "PRE-WF04-01", "desc": "Staff user is authenticated with active JWT session.", "check": "session.is_valid()", "on_fail": "Prompt login screen."}
        ],
        "triggers": [
            {"id": "TRIG-WF04-01", "class": "User Trigger", "event": "Operator scans QR code or enters search query in search bar", "source": "Search UI Bar", "payload": "{ query_string, filter_type }", "latency": "< 50ms"}
        ],
        "inputs": [
            {"name": "search_query", "type": "String(50)", "req": "Mandatory", "source": "Operator / Scanner", "val": "UHID, 10-digit phone, or patient name", "priv": "PII Search Token", "enc": "Plaintext in transit", "ex": "9845012345", "on_err": "Prompt valid search query"}
        ],
        "outputs": {
            "success": [
                {"name": "Ranked Patient Candidates", "desc": "List of matching patient profile summaries with photo and ward.", "format": "JSON Array of Patient Summaries", "recipient": "Client Search Modal"}
            ],
            "partial": [],
            "error": [
                {"name": "Zero Match Found Notice", "desc": "Returned when no candidate meets threshold.", "code": "ERR-SEARCH-NO-MATCH", "msg": "No patient found matching search criteria."}
            ],
            "events": [
                {"topic": "namma.clinic.patient.searched", "desc": "Audit event logging search query and actor.", "schema": "{ actor_id, query_hash, candidates_returned, timestamp }"}
            ]
        },
        "happy_path": [
            {"title": "Operator Focuses Universal Search Bar", "actor": "Staff Operator (`ACT-WF04-01`)", "input": "Presses `/` shortcut key", "action": "Focuses search input on terminal.", "sys_behavior": "Activates barcode listener and displays search modal.", "validation": "Search bar active", "db_effect": "None", "ui_effect": "Search modal appears with recent searches.", "api_effect": "None", "audit_effect": "None", "output": "Search ready", "next_state": "WFSTATE-004-001", "failure_possibility": "UI focus trap."},
            {"title": "Barcode Scanner Reads Clinic Card QR", "actor": "Staff Operator (`ACT-WF04-01`)", "input": "Card presented under 2D scanner", "action": "Scans QR code on physical card.", "sys_behavior": "WebSerial receives payload `UHID:BLR-W085-202609-0012`.", "validation": "UHID format valid", "db_effect": "None", "ui_effect": "Inputs UHID into search bar automatically.", "api_effect": "GET /api/v1/patients/lookup?uhid=BLR-W085-202609-0012", "audit_effect": "WFAUDIT-004-001 (QR Lookup Executed)", "output": "UHID query token", "next_state": "WFSTATE-004-002", "failure_possibility": "Scratched QR code."},
            {"title": "Instant Direct Index Match Lookup", "actor": "Edge Search Engine (`ACT-WF04-02`)", "input": "UHID token", "action": "Executes primary key query against local SQLite DB.", "sys_behavior": "Direct B-tree lookup completes in 4 milliseconds.", "validation": "Record exists in database", "db_effect": "None", "ui_effect": "Renders exact match card with citizen photo.", "api_effect": "None", "audit_effect": "None", "output": "Patient profile loaded", "next_state": "WFSTATE-004-003", "failure_possibility": "Record not found (new clinic card)."},
            {"title": "Identity Confirmation Verification", "actor": "Staff Operator (`ACT-WF04-01`)", "input": "Visual inspection of citizen and photo", "action": "Verifies name and asks birth year confirmation.", "sys_behavior": "Compares verbal answer with recorded DOB.", "validation": "Identity verified", "db_effect": "None", "ui_effect": "Operator clicks 'Confirm & Open Patient Chart'.", "api_effect": "POST /api/v1/patients/access-log", "audit_effect": "WFAUDIT-004-002 (Identity Confirmed)", "output": "Confirmed patient context", "next_state": "WFSTATE-004-004", "failure_possibility": "Identity mismatch."},
            {"title": "Patient Workspace Loading", "actor": "Staff Operator (`ACT-WF04-01`)", "input": "Confirmed patient ID", "action": "Loads active station view for patient.", "sys_behavior": "Pre-populates clinical history and allergy alerts.", "validation": "Workspace loaded", "db_effect": "Inserts row in `patient_access_logs`", "ui_effect": "Displays patient banner at top of screen.", "api_effect": "GET /api/v1/patients/{id}/summary", "audit_effect": "WFAUDIT-004-003 (Patient Record Opened)", "output": "Active station context", "next_state": "WFSTATE-004-005", "failure_possibility": "Workspace crash."}
        ],
        "alternate_flows": [
            {
                "id": "WFALT-004-001", "title": "Search by 10-Digit Mobile Number",
                "condition": "Patient has no physical card but knows mobile phone number.",
                "from_step": "WFSTEP-004-001",
                "steps": [
                    "Operator types 10-digit mobile number into search bar.",
                    "System queries indexed `phone` column across local database.",
                    "Returns candidate cards for all family members sharing that phone number.",
                    "Operator identifies patient by name and age."
                ],
                "rejoin": "Rejoins main flow at Step WFSTEP-004-004 (Identity Confirmation).",
                "audit": "WFAUDIT-004-ALT01 (Phone Search Executed)"
            },
            {
                "id": "WFALT-004-002", "title": "Bilingual Phonetic Fuzzy Name Search",
                "condition": "Patient has no card and mobile phone is unknown or unregistered.",
                "from_step": "WFSTEP-004-001",
                "steps": [
                    "Operator types patient name in Kannada or English (e.g. 'Lakshmamma').",
                    "System executes double-metaphone phonetic query with Levenshtein distance <= 2.",
                    "Filters candidates by BBMP Ward and approximate age (+/- 3 years).",
                    "Displays ranked candidate list with portrait photos."
                ],
                "rejoin": "Rejoins main flow at Step WFSTEP-004-004.",
                "audit": "WFAUDIT-004-ALT02 (Phonetic Search Executed)"
            }
        ],
        "exception_flows": [
            {
                "id": "WFEX-004-001", "title": "Zero Search Candidates Found",
                "trigger": "Query returns 0 matching records across local and cloud databases.",
                "detection": "Search result set length == 0.",
                "containment": "Displays prompt: 'No patient record found. Would you like to register a new citizen?'.",
                "msg_en": "No patient found matching search criteria. Click below to register new patient.",
                "msg_kn": "ಯಾವುದೇ ರೋಗಿ ದಾಖಲೆ ಕಂಡುಬಂದಿಲ್ಲ. ಹೊಸ ರೋಗಿ ನೋಂದಣಿಗೆ ಕೆಳಗೆ ಕ್ಲಿಕ್ ಮಾಡಿ.",
                "recovery": "Operator clicks 'Register New Patient' and transitions directly to WF-003.",
                "audit": "WFAUDIT-004-EX01", "severity": "LOW"
            }
        ],
        "emergency_flow": {
            "triggers": "Unconscious trauma patient arriving without identity.",
            "escalation": "Operator clicks 'Emergency Anonymous Bypass'.",
            "preemption": "Skips search entirely; opens emergency proxy file.",
            "bypass_rules": "Bypasses lookup; allows retrospective search post-stabilization.",
            "safety_controls": "Full clinical care provided immediately.",
            "reconciliation": "Search executed later using facial photo or family member declaration.",
            "audit_event": "WFAUDIT-004-EMERGENCY",
            "signoff_sla": "2 hours"
        },
        "states": [
            {"name": "SEARCH_IDLE", "desc": "Search bar ready for input.", "allowed": "Query input, QR scan", "prohibited": "Accessing records", "actor": "Operator"},
            {"name": "SEARCHING", "desc": "Query executing across B-tree and FTS5 indexes.", "allowed": "Cancel", "prohibited": "Concurrent search", "actor": "Search Engine"},
            {"name": "CANDIDATES_DISPLAYED", "desc": "Search results displayed with photos and age.", "allowed": "Select candidate, refine filter", "prohibited": "Modifying records", "actor": "Operator"},
            {"name": "PATIENT_SELECTED", "desc": "Patient confirmed and workspace loaded.", "allowed": "Station workflows", "prohibited": "Search actions", "actor": "Operator"}
        ],
        "transitions": [
            {"from_state": "SEARCH_IDLE", "event": "Submit Query", "actor": "Operator", "condition": "Query non-empty", "validation": "Sanitized", "to_state": "SEARCHING", "side_effects": "Execute query", "audit": "WFAUDIT-004-TR01"},
            {"from_state": "SEARCHING", "event": "Results Returned", "actor": "Search Engine", "condition": "Matches >= 1", "validation": "Results valid", "to_state": "CANDIDATES_DISPLAYED", "side_effects": "Render cards", "audit": "WFAUDIT-004-TR02"},
            {"from_state": "CANDIDATES_DISPLAYED", "event": "Select Candidate", "actor": "Operator", "condition": "Citizen verified", "validation": "ID confirmed", "to_state": "PATIENT_SELECTED", "side_effects": "Open chart", "audit": "WFAUDIT-004-TR03"}
        ],
        "decision_tables": [
            {
                "id": "WFDEC-004-001", "title": "Search Query Routing & Optimization Matrix",
                "desc": "Determines optimal database index based on input format.",
                "conditions": ["Query starts with 'BLR-'", "Query is 10 digits", "Query is alphabetic text", "Query is ABHA format"],
                "actions": ["Primary Key B-Tree Index", "Phone Column B-Tree Index", "FTS5 Phonetic Index", "ABHA Hash Index"],
                "rows": [
                    {"rule": "S1", "cond_vals": ["YES", "NO", "NO", "NO"], "act_vals": ["YES", "NO", "NO", "NO"]},
                    {"rule": "S2", "cond_vals": ["NO", "YES", "NO", "NO"], "act_vals": ["NO", "YES", "NO", "NO"]},
                    {"rule": "S3", "cond_vals": ["NO", "NO", "YES", "NO"], "act_vals": ["NO", "NO", "YES", "NO"]},
                    {"rule": "S4", "cond_vals": ["NO", "NO", "NO", "YES"], "act_vals": ["NO", "NO", "NO", "YES"]}
                ]
            }
        ],
        "validation_rules": [
            {"id": "WFVAL-004-001", "field": "search_query", "expr": "len(query) >= 2 and not contains_sql_injection(query)", "code": "ERR-VAL-04-01", "msg_en": "Search query must be at least 2 characters.", "msg_kn": "ಹುಡುಕಾಟದ ಪದವು ಕನಿಷ್ಠ 2 ಅಕ್ಷರಗಳನ್ನು ಹೊಂದಿರಬೇಕು.", "recovery": "Enter longer query.", "test_ref": "WFTEST-004-001"}
        ],
        "business_rules": [
            {"id": "BRULE-WF04-001", "title": "Mandatory Search Before New Registration", "req": "BRULE-004", "spec": "Clerks must execute a search before creating a new patient record to avoid duplicate creation.", "enforcement": "System tracks search query before unlocking new registration form.", "consequence": "Direct registration without search triggers audit warning."}
        ],
        "clinical_rules": [
            {"id": "CR-WF04-001", "title": "Prominent Allergy Banner Upon Patient Selection", "req": "CR-004", "rationale": "Clinicians must be immediately aware of life-threatening allergies.", "logic": "If patient has documented allergies, system renders high-visibility red banner on open.", "override_policy": "None. Display is mandatory.", "safety_invariant": "Allergies visible on all patient views."}
        ],
        "operational_rules": [
            {"id": "OR-WF04-001", "title": "Identity Verification Challenge Mandate", "req": "OR-004", "mandate": "Operators must verbally confirm at least two demographic data points before opening chart.", "boundary": "All stations.", "exception": "Unconscious emergency patients."}
        ],
        "security_controls": [
            {"domain": "Audit Trail", "id": "SEC-WF04-01", "spec": "Every search query and chart view is logged with operator ID and timestamp.", "param": "WORM audit table", "threat": "Unauthorized PHI browsing", "compliance": "SECR-004"}
        ],
        "privacy_controls": [
            {"principle": "Need to Know", "id": "PRIV-WF04-01", "spec": "Search candidate cards show only name, photo, age, gender, and ward. Full clinical history hidden until selected.", "invariant": "Minimization in search results", "right": "DPDP Act Sec 6"}
        ],
        "offline_behavior": {
            "online_mode": "Queries cloud master patient index with fallback to local.",
            "detection_latency": "< 1 second.",
            "local_storage": "SQLite FTS5 full-text search index holding local clinic records.",
            "queue_mechanics": "Search queries logged in local audit log.",
            "degraded_scope": "Full search capability across all patients previously registered or treated at this clinic.",
            "sync_convergence": "Local FTS index updated automatically during background sync.",
            "conflict_invariants": "Read-only search operations have zero conflict potential."
        },
        "diagrams": {
            "data_flow": """flowchart TD
    Op["Staff Operator"] -->|Enters Query| Bar["Search Bar UI"]
    Bar -->|Dispatch Query| Engine["Search Index Engine"]
    Engine -->|Exact Match| BTree[("B-Tree Index (UHID / Phone)")]
    Engine -->|Fuzzy Match| FTS[("FTS5 Phonetic Index (Name)")]
    BTree --> Results["Ranked Candidate Cards"]
    FTS --> Results
    Results --> Bar
    Bar -->|Confirm Patient| Chart["Patient Workspace Chart"]""",
            "sequence": """sequenceDiagram
    actor O as Operator
    participant UI as Search UI
    participant E as Search Engine
    participant DB as SQLite DB
    O->>UI: 1. Input phone number '9845012345'
    UI->>E: 2. Query /patients/search?phone=9845012345
    E->>DB: 3. Indexed lookup on phone column
    DB-->>E: 4. Return 2 household member records
    E-->>UI: 5. Display candidate cards with photos
    O->>UI: 6. Select 'Lakshmamma (Age 68)'
    UI->>DB: 7. Log chart access audit event
    UI-->>O: 8. Patient chart opened successfully""",
            "activity": """flowchart TD
    Start([Focus Search Bar]) --> InputQuery[Scan QR or Enter Query]
    InputQuery --> QueryType{Query Type?}
    QueryType -- UHID / QR --> ExactLookup[Direct B-Tree Lookup < 10ms]
    QueryType -- 10-Digit Phone --> PhoneLookup[Phone B-Tree Lookup < 15ms]
    QueryType -- Name --> FuzzyLookup[FTS5 Phonetic Metaphone Lookup]
    ExactLookup --> DisplayResults[Display Candidate Cards]
    PhoneLookup --> DisplayResults
    FuzzyLookup --> DisplayResults
    DisplayResults --> Matches{Candidates Found?}
    Matches -- Yes --> VerifyID[Operator Verifies Photo & Age] --> OpenChart[Open Patient Chart]
    Matches -- No --> PromptNew[Prompt Register New Patient] --> End([Search Complete])
    OpenChart --> End""",
            "state": """stateDiagram-v2
    [*] --> SEARCH_IDLE
    SEARCH_IDLE --> SEARCHING: Input Query / Scan QR
    SEARCHING --> CANDIDATES_DISPLAYED: Matches Found
    SEARCHING --> SEARCH_IDLE: No Matches (Prompt New)
    CANDIDATES_DISPLAYED --> PATIENT_SELECTED: Confirm Patient
    PATIENT_SELECTED --> SEARCH_IDLE: Clear Patient Context
    PATIENT_SELECTED --> [*]"""
        },
        "data_flow_nodes": [
            {"name": "Bar", "desc": "Universal search input component with debounce.", "protocol": "HTTPS / IPC", "encryption": "TLS 1.3"},
            {"name": "Engine", "desc": "Local search daemon executing parameterized queries.", "protocol": "SQLite C-API", "encryption": "In-memory"}
        ],
        "failure_tree": [
            {"id": "FT-004-001", "cat": "Software", "root": "FTS5 index corruption after crash", "vector": "Unclean shutdown", "impact": "Name searches fail", "detection": "SQLite error 'table corrupted'", "mitigation": "Automated `REINDEX` command runs on boot"}
        ],
        "recovery_procedures": [
            {"id": "REC-WF04-01", "title": "Search Index Rebuild Runbook", "trigger": "FTS search returns database error.", "containment": "Falls back to exact phone lookup.", "steps": ["Click Admin Tools -> 'Rebuild Search Index'.", "System drops and recreates FTS5 virtual table from master records in 3 seconds."], "rollback": "None", "resumption": "Phonetic search restored.", "audit": "WFAUDIT-004-REC01"}
        ],
        "audit_events": [
            {"id": "WFAUDIT-004-001", "event": "PATIENT_SEARCH_EXECUTED", "actor": "Operator", "meta": "{ query_type: 'PHONE', matches: 2 }", "state_before": "IDLE", "state_after": "RESULTS", "hmac": "HMAC-SHA256", "retention": "7 Years", "compliance": "DPDP Act"},
            {"id": "WFAUDIT-004-002", "event": "PATIENT_RECORD_VIEWED", "actor": "Operator", "meta": "{ patient_id, station: 'TRIAGE' }", "state_before": "RESULTS", "state_after": "OPENED", "hmac": "HMAC-SHA256", "retention": "7 Years", "compliance": "SECR-004"}
        ],
        "notifications": [
            {"id": "WFNOTIF-004-01", "trigger": "VIP Record Accessed", "recipient": "Security Officer", "channel": "System Alert", "text_en": "Audit alert: Protected medical record accessed.", "text_kn": "ಭದ್ರತಾ ಎಚ್ಚರಿಕೆ: ರಕ್ಷಿತ ವೈದ್ಯಕೀಯ ದಾಖಲೆಯನ್ನು ವೀಕ್ಷಿಸಲಾಗಿದೆ.", "priority": "High", "retry": "None", "fallback": "Log only"}
        ],
        "planned_apis": [
            {"id": "PLANNED-API-004-01", "method": "GET", "path": "/api/v1/patients/search", "desc": "Executes multi-parametric patient search.", "scope": "patients:read", "req_schema": "{\n  \"query\": \"9845012345\",\n  \"filter\": \"phone\"\n}", "res_schema": "{\n  \"candidates\": [{\n    \"patient_id\": \"uuid\",\n    \"uhid\": \"BLR-W085-202609-0012\",\n    \"full_name\": \"Lakshmamma Gowda\",\n    \"age\": 68,\n    \"gender\": \"FEMALE\"\n  }]\n}", "errors": "400 Invalid Query, 401 Unauthorized", "idempotency": "Not Required (Read-Only)", "rate_limit": "120 req/min", "offline_support": "Full local SQLite FTS5 search"}
        ],
        "planned_db": [
            {"id": "PLANNED-DB-004-01", "table": "patient_search_fts", "purpose": "SQLite FTS5 virtual table for high-speed phonetic full-text indexing.", "pk": "rowid", "fks": "None", "cols": [
                {"name": "uhid", "type": "TEXT", "null": "NOT NULL", "notes": "UHID token"},
                {"name": "name_en", "type": "TEXT", "null": "NOT NULL", "notes": "English name tokens"},
                {"name": "name_kn", "type": "TEXT", "null": "NOT NULL", "notes": "Kannada name tokens"},
                {"name": "phone", "type": "TEXT", "null": "NULL", "notes": "10-digit phone token"}
            ], "indexes": "FTS5 Virtual Index", "concurrency": "Read-Heavy", "retention": "Mirrors patients table"}
        ],
        "planned_ui": [
            {"id": "PLANNED-UI-004-01", "screen": "Universal Search Modal", "route": "/search", "persona": "All Staff Roles", "components": "Search input, camera scan button, candidate card list with photos and age, keyboard shortcut helper.", "states": "Empty, Searching, Results, No Match.", "validations": "Debounced 250ms; query sanitized.", "a11y": "Arrow keys navigate candidates; Enter opens record.", "localization": "Bilingual candidate display.", "offline_ui": "Shows 'Offline Search Active' badge."}
        ],
        "backend_reqs": {
            "domain_services": "Orchestrates `PatientSearchService`, `PhoneticMatcher`, and `AccessAuditor`.",
            "transactions": "Read-only queries; audit log writes in separate asynchronous thread.",
            "async_workers": "Background FTS indexer syncs new patient registrations within 500ms.",
            "circuit_breakers": "Cloud search fallback to local SQLite index on any error."
        },
        "integrations": [
            {"id": "INT-WF04-01", "system": "ABDM Scan & Share Bridge", "protocol": "HTTPS", "payload": "QR payload resolution", "direction": "Bidirectional", "timeout": "3 sec", "fallback": "Local lookup"}
        ],
        "reports": [
            {"id": "REP-WF04-01", "title": "Patient Search Quality & Latency Report", "freq": "Weekly", "audience": "DevOps, Product Manager", "grain": "Per query type, latency p95", "ref": "PERF-004"}
        ],
        "analytics": [
            {"id": "ANL-WF04-01", "kpi": "Search Latency", "formula": "AVG(query_duration_ms)", "dimensions": "Search Type", "target": "<= 150ms", "alert": "Latency > 300ms triggers index alert"}
        ],
        "ai_reqs": {
            "id": "AIR-WF04-01", "purpose": "Phonetic Candidate Re-ranking", "features": "Levenshtein distance, Soundex, clinic ward affinity",
            "output_signal": "Candidate Re-ranked Order", "confidence": "Ranks highest probability candidate first", "explainability": "Explains: 'Ranked top due to matching ward and age'.",
            "authority": "Advisory ordering only.", "audit": "None"
        },
        "stride_threats": [
            {"id": "STRIDE-WF04-01", "cat": "Information Disclosure", "asset": "Patient Directory", "scenario": "Operator searches random names out of curiosity.", "likelihood": "Medium", "impact": "High", "mitigation": "Audit logging of every search query; periodic supervisory audits.", "residual": "Low", "test_ref": "WFTEST-004-001"}
        ],
        "linddun_threats": [
            {"id": "LINDDUN-WF04-01", "cat": "Identifiability", "asset": "Candidate List", "vector": "Overhearing candidate names in waiting area.", "likelihood": "Medium", "impact": "Low", "mitigation": "Terminal screens positioned away from public waiting seats.", "compliance": "DPDP Act"}
        ],
        "performance": {
            "e2e_latency": "Search response in < 150ms.", "ui_render": "Candidate cards render in < 50ms.",
            "db_budget": "SQLite query < 15ms.", "concurrency": "50 searches/sec.",
            "payload": "Payload size < 10KB.", "hardware": "RAM < 40MB."
        },
        "availability": {
            "sla": "99.99% search availability.", "rto": "< 1 min.", "rpo": "0 data lost.",
            "offline_autonomy": "Full search across all local clinic patients.", "failover": "Local FTS5 index."
        },
        "accessibility": {
            "screen_reader": "ARIA live announcements for candidate counts.", "contrast": "High contrast ratio.",
            "keyboard": "Full arrow key navigation.", "touch": "Large candidate tap cards.", "cognitive": "Clear, uncluttered presentation."
        },
        "localization": {
            "clinical_terms": "N/A", "printed_material": "N/A",
            "audio_prompts": "N/A"
        },
        "test_gates": [
            {"level": "Unit Testing", "scope": "Phonetic matching, query parsing", "tooling": "PyTest", "coverage": ">= 95%", "gate": "Zero test failures"},
            {"level": "Performance Testing", "scope": "k6 search benchmark on 500,000 records", "tooling": "k6", "coverage": "All query types", "gate": "p95 < 150ms"}
        ],
        "bdd_scenarios": [
            {
                "id": "WFTEST-004-001", "title": "Exact Lookup via 2D Barcode Scan on Clinic Card",
                "category": "Happy Path", "priority": "P0",
                "given": "a registered citizen presents their physical thermal clinic card",
                "given_ands": ["the staff nurse has focused the universal search bar"],
                "when": "the barcode scanner reads the QR code payload",
                "when_ands": ["the system executes an indexed B-tree query on the UHID"],
                "then": "the matching patient profile is opened within 50 milliseconds",
                "then_ands": ["displays active clinical allergy alerts prominently on the top banner"]
            },
            {
                "id": "WFTEST-004-002", "title": "Bilingual Phonetic Fuzzy Search with Minor Name Misspelling",
                "category": "Fuzzy Search", "priority": "P1",
                "given": "a citizen registered as 'Lakshmamma' has forgotten their clinic card",
                "given_ands": ["the clerk types 'Laxmamma' in the search box with filter Ward 085"],
                "when": "the search engine executes a double-metaphone phonetic query",
                "when_ands": ["evaluates Levenshtein distance against local FTS5 index"],
                "then": "the system successfully returns 'Lakshmamma Gowda (Age 68)' as the top candidate",
                "then_ands": ["displays the citizen's portrait photo for visual confirmation"]
            }
        ],
        "acceptance_criteria": [
            {"id": "AC-WF-004-001", "criterion": "QR card lookup loads patient in <= 50ms.", "method": "Telemetry timer", "threshold": "p99 <= 50ms", "gate": "Performance Gate"},
            {"id": "AC-WF-004-002", "criterion": "Phonetic search recall >= 98% on test corpus.", "method": "Automated accuracy benchmark", "threshold": ">= 98% recall", "gate": "Search Quality Gate"}
        ],
        "dependencies": [
            {"id": "WFDEP-004-01", "upstream": "WF-003", "downstream": "WF-004", "nature": "Data Ingestion Prerequisite", "blocking": "BLOCKING", "impact": "Search operates on registered patient index.", "resilience": "None."},
            {"id": "WFDEP-004-02", "upstream": "WF-004", "downstream": "WF-005", "nature": "Repeat Patient Look-up", "blocking": "BLOCKING", "impact": "Repeat patient workflow begins with search.", "resilience": "Direct QR scan bypasses search modal."}
        ],
        "critical_path": {
            "path": "Input Query -> Query Parser -> B-Tree / FTS Lookup -> Candidate Ranking -> Confirm Patient.",
            "bottleneck": "Unindexed full-text queries if search string has < 2 characters.",
            "load_balancing": "Enforces minimum 2-character requirement; debounces input by 250ms.",
            "recovery_bottlenecks": "Rebuilding local FTS index takes 3 seconds."
        },
        "rollback_strategy": {
            "db_rollback": "None (Read-Only queries).", "saga_compensation": "None.",
            "notification_reversal": "None.", "audit_preservation": "All searches permanently logged.",
            "offline_rollback": "None."
        },
        "idempotency": {
            "key_schema": "Read-only GET requests are inherently idempotent.",
            "cache_store": "Local memory cache for recent lookups.", "replay_behavior": "Returns cached results.",
            "ttl": "5 minutes.", "offline_replay": "Syncs search audit logs."
        },
        "concurrency": {
            "occ": "None (Read-only).", "pessimistic": "None.",
            "queue_locking": "None.", "deadlock_policy": "None."
        },
        "invariants": [
            {"id": "INVARIANT-WF-004-01", "statement": "Every search query returning Protected Health Information must be auditable to an authenticated operator.", "scope": "Search API Gateway", "enforcement": "Middleware writes audit log before returning response.", "consequence": "Unauthenticated searches rejected with HTTP 401."}
        ],
        "observability": [
            {"cat": "Metric", "name": "namma_clinic_patient_search_duration_ms", "type": "Histogram", "labels": "type, clinic_id", "target": "Prometheus", "alert": "p95 > 250ms triggers performance alert"}
        ],
        "runbook": {
            "morning_sop": "Test barcode scanner with sample card. Ensure scanner emits clean beep.",
            "live_sop": "Ask returning citizens for physical card first. If card absent, ask for mobile phone.",
            "troubleshooting_sop": "If search is slow: Check if multiple staff are running wildcards. Restart local browser.",
            "closing_sop": "Verify search audit logs synchronized to central server."
        },
        "sla_slo": [
            {"name": "Search Query Latency", "target": "< 150ms", "window": "Monthly", "warning": "> 200ms", "escalation": "DevOps alerted"}
        ],
        "traceability": [
            {"req": "FR-004", "type": "Functional Req", "step": "WFSTEP-004-003", "state": "WFSTATE-004-003", "api": "PLANNED-API-004-01", "db": "PLANNED-DB-004-01", "ui": "PLANNED-UI-004-01", "test": "WFTEST-004-001"}
        ],
        "open_questions": [
            {"id": "OQ-WF04-01", "subject": "Facial Recognition Patient Identification", "query": "Can captured webcam photos be indexed for 1:N facial biometric lookup to eliminate card and phone dependency?", "impact": "Significant privacy considerations under DPDP Act 2023.", "owner": "CISO & Privacy Board", "milestone": "Milestone 4"}
        ],
        "assumptions": [
            {"id": "ASM-WF04-01", "cat": "Hardware", "statement": "Hardware 2D barcode scanners emulate standard USB HID keyboard input.", "status": "CONFIRMED", "risk": "WebSerial API needed if HID mode unsupported."}
        ],
        "risks": [
            {"id": "RSK-WF04-01", "desc": "Citizens having identical names and similar ages in the same ward.", "prob": "High", "impact": "Medium", "mitigation": "Candidate card displays photo and father/husband name for positive identification.", "contingency": "Ask for birth year challenge question.", "owner": "Staff Operator"}
        ],
        "change_impact": [
            {"vector": "PostgreSQL FTS to Meilisearch Migration", "scenario": "Cloud platform switches search engine for higher throughput.", "components": "Search index daemon, API query builder", "severity": "LOW", "testing": "Full search regression suite"}
        ],
        "definition_of_ready": [
            {"id": "DOR-WF04-01", "criterion": "Search specification approved by Architecture team.", "artifact": "WF-004 Doc", "signoff": "Search Lead"}
        ],
        "definition_of_done": [
            {"id": "DOD-WF04-01", "criterion": "k6 search latency benchmark passes under 500 req/sec load.", "method": "Automated k6 report", "benchmark": "p95 < 150ms"}
        ],
        "related_workflows": [
            {"rel": "Upstream Dependency", "id": "WF-003", "name": "Patient Registration Workflow", "interface": "Master Patient Index Ingestion"},
            {"rel": "Downstream Workflow", "id": "WF-005", "name": "Repeat Patient Revisit Workflow", "interface": "Patient Context Handoff"}
        ]
    }
    return build_workflow_object(spec)

def make_wf05_data():
    wf_meta = WORKFLOW_MAP["WF-005"]
    wfid = "WF-005"
    wfnum = "05"

    spec = {
        "id": wfid, "num": wfnum, "name": wf_meta["name"], "domain": wf_meta["domain"],
        "exec_summary": {
            "purpose": "Governs the intake and care continuity for returning citizens. Retrieves longitudinal medical histories, links active chronic disease episodes (Hypertension, Diabetes Mellitus, Epilepsy, TB DOTS), highlights documented drug allergies, detects overdue follow-up appointments, clears defaulter flags in NCD tracking registries, and issues prioritized repeat visit tokens.",
            "rationale": "Urban primary healthcare centers deliver vital chronic disease management where 60-70% of daily patient traffic represents return visits. Smooth episode linking ensures that longitudinal treatment trajectories are maintained without restarting clinical evaluations from scratch.",
            "clinical_impact": "Enables clinicians to review vital sign trends over time (e.g. 6-month blood pressure curves), assess medication adherence, prevent duplicated diagnostic tests, and verify drug tolerance.",
            "system_impact": "Links individual clinical encounters to overarching master episode identifiers in local SQLite and central PostgreSQL; emits milestone events to National NCD Portal.",
            "risk_profile": "Creating disconnected orphan visits instead of linking to active episodes, missed chronic disease defaulter alerts, overlooking documented adverse drug reactions, and stale demographic details."
        },
        "objectives": [
            {"id": "OBJ-WF05-01", "title": "Rapid Repeat Patient Intake", "desc": "Complete return visit intake and token generation in under 30 seconds.", "metric": "Repeat Intake Latency p95 <= 30 sec", "verification": "Intake timestamp telemetry"},
            {"id": "OBJ-WF05-02", "title": "100% Chronic Episode Continuity", "desc": "Link 100% of returning NCD patients to their active longitudinal chronic disease care plan.", "metric": "Episode Linkage Rate = 100.0%", "verification": "Clinical database relational integrity audits"},
            {"id": "OBJ-WF05-03", "title": "Automated Defaulter Status Clearing", "desc": "Automatically clear overdue defaulter flags upon citizen clinic presentation and notify ASHA worker.", "metric": "Defaulter Clear Latency < 5 sec", "verification": "NCD cohort status transition logs"},
            {"id": "OBJ-WF05-04", "title": "Historical Baseline Vitals Pre-Population", "desc": "Pre-populate last 3 recorded blood pressure and glucose readings on nurse and doctor screens.", "metric": "Pre-Population Success Rate = 100%", "verification": "EMR UI render assertion tests"}
        ],
        "in_scope": [
            {"area": "Revisit Record Retrieval", "desc": "Instant loading of longitudinal record via card QR scan or search."},
            {"area": "Demographic Delta Check", "desc": "Verifying and updating changed phone numbers or residential addresses."},
            {"area": "Chronic Episode Linking", "desc": "Binding new encounter to ongoing Hypertension, Diabetes, or ANC episode."},
            {"area": "Defaulter Flag Resolution", "desc": "Clearing overdue follow-up alerts and closing community outreach tasks."},
            {"area": "Repeat Priority Token Issuance", "desc": "Mints prioritized queue ticket with episode and category tags."}
        ],
        "out_of_scope": [
            {"area": "Initial Primary Registration", "desc": "Intake of first-time citizens; handled under WF-003.", "handoff": "WF-003 Patient Registration"},
            {"area": "Tertiary Hospital Admission", "desc": "Transfer to higher medical center; handled under WF-016.", "handoff": "WF-016 Referral Workflow"}
        ],
        "actors": [
            {"id": "ACT-WF05-01", "type": "Human", "name": "Registration Clerk", "responsibilities": "Scans return card, verifies phone number, confirms revisit reason, issues token.", "permissions": "Patient Read, Demographic Update, Token Issue", "failure_duty": "Replaces lost card; updates changed phone numbers.", "inputs": "Clinic card QR, verbal declaration of revisit reason", "decisions": "Determines whether visit is routine chronic follow-up or new acute illness.", "outputs": "Repeat token slip, updated demographic delta", "recovery": "Searches by phone if card not presented."},
            {"id": "ACT-WF05-02", "type": "Human", "name": "Staff Nurse", "responsibilities": "Reviews previous baseline vitals, captures current vitals, monitors NCD adherence.", "permissions": "Triage Vitals Record, Care Plan Read", "failure_duty": "Alerts doctor if blood pressure severely elevated compared to baseline.", "inputs": "Current physiological measurements, patient pill adherence report", "decisions": "Evaluates vital sign trend compared to last 3 visits.", "outputs": "Committed triage vitals linked to episode", "recovery": "Repeats blood pressure measurement after 5 min rest."},
            {"id": "ACT-WF05-03", "type": "Human", "name": "Medical Officer", "responsibilities": "Reviews longitudinal treatment response, assesses control, refines medication dosage.", "permissions": "Encounter Full, Care Plan Update, Rx Authoring", "failure_duty": "Adjusts antihypertensive therapy if target BP (<140/90) not achieved.", "inputs": "Longitudinal blood pressure chart, current lab results, adherence history", "decisions": "Decides whether to maintain current regimen, titrate dosage, or add second drug.", "outputs": "Signed repeat encounter note, updated e-prescription, next recall date", "recovery": "Orders point-of-care serum creatinine if medication adjustment needed."}
        ],
        "personas": [
            {"id": "PERSONA-007", "name": "Lakshmamma", "role": "Elderly Chronic Patient (Age 68)", "env": "Returns for monthly Hypertension checkup and 30-day Amlodipine refill.", "goals": "Get her blood pressure checked, confirm it is normal, collect medicines quickly.", "pain_points": "Long waits when returning only for routine medication refills.", "adaptations": "Fast-track return queue ticket; doctor reviews historical baseline in 3 seconds."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "Patient History, Vitals Trends", "create": "Triage Vitals, Repeat Token", "update": "Phone Number", "delete": "None", "override": "Fast-Track Triage", "signoff": "Triage Record"},
            {"role": "ROLE-002", "title": "Medical Officer", "read": "Full Longitudinal EHR", "create": "Encounter, Rx, Follow-Up", "update": "Care Plan, Regimen", "delete": "None", "override": "Clinical Override", "signoff": "Encounter & Prescription"}
        ],
        "preconditions": [
            {"id": "PRE-WF05-01", "desc": "Citizen has an existing, registered master record in clinic database.", "check": "patient.exists() == TRUE", "on_fail": "Redirect to WF-003 for new registration."},
            {"id": "PRE-WF05-02", "desc": "Clinic daily operating session is active and queues running.", "check": "clinic_session.status == 'ACTIVE'", "on_fail": "Wait for coordinator morning opening."}
        ],
        "triggers": [
            {"id": "TRIG-WF05-01", "class": "User Trigger", "event": "Returning citizen presents clinic card at desk; clerk scans QR code", "source": "Barcode Scanner", "payload": "{ uhid: 'BLR-W085-202609-0012' }", "latency": "< 50ms to load record"}
        ],
        "inputs": [
            {"name": "uhid", "type": "String(30)", "req": "Mandatory", "source": "Clinic Card QR / Search", "val": "Valid clinic UHID format", "priv": "Operational", "enc": "Plaintext indexed", "ex": "BLR-W085-202609-0012", "on_err": "Search by phone number"},
            {"name": "revisit_reason", "type": "Enum", "req": "Mandatory", "source": "Citizen Declaration", "val": "CHRONIC_NCD_REFILL | ACUTE_NEW_COMPLAINT | LAB_REPORT_REVIEW | POST_OP_DRESSING", "priv": "PHI", "enc": "Plaintext indexed", "ex": "CHRONIC_NCD_REFILL", "on_err": "Default to General OPD"},
            {"name": "phone_changed", "type": "Boolean", "req": "Mandatory", "source": "Clerk Inquiry", "val": "TRUE | FALSE", "priv": "Operational", "enc": "Plaintext", "ex": "FALSE", "on_err": "Assume false"}
        ],
        "outputs": {
            "success": [
                {"name": "Repeat Patient Token", "desc": "Printed thermal queue token tagged with repeat visit and episode ID.", "format": "58mm Thermal Printout", "recipient": "Citizen Patient"},
                {"name": "Linked Clinical Encounter", "desc": "Encounter entity bound to master longitudinal episode.", "format": "Database Entity", "recipient": "Doctor EMR Console"}
            ],
            "partial": [],
            "error": [
                {"name": "Episode Closed Error", "desc": "Returned if previous episode was formally closed/discharged.", "code": "ERR-EPISODE-CLOSED", "msg": "Previous treatment episode is closed. New episode will be initialized."}
            ],
            "events": [
                {"topic": "namma.clinic.patient.revisited", "desc": "Emitted upon check-in of returning patient.", "schema": "{ patient_id, episode_id, visit_number, timestamp }"}
            ]
        },
        "happy_path": [
            {"title": "Card Scan & Longitudinal History Retrieval", "actor": "Registration Clerk (`ACT-WF05-01`)", "input": "Clinic card QR scanned", "action": "Scans card; system loads longitudinal record in 15ms.", "sys_behavior": "Retrieves last 5 encounters, active care plan, and allergy history.", "validation": "UHID exists", "db_effect": "None", "ui_effect": "Displays returning patient summary with photo and active diagnoses.", "api_effect": "GET /api/v1/patients/{uhid}/revisit-summary", "audit_effect": "WFAUDIT-005-001 (Revisit Summary Loaded)", "output": "Patient history loaded", "next_state": "WFSTATE-005-001", "failure_possibility": "Card unreadable."},
            {"title": "Allergy & Medical Alert Verification", "actor": "Registration Clerk (`ACT-WF05-01`)", "input": "System allergy flag", "action": "Inspects screen alert: 'No Known Drug Allergies (NKDA)'.", "sys_behavior": "Verifies allergy status was reviewed within past 12 months.", "validation": "Allergy status recorded", "db_effect": "None", "ui_effect": "Green 'Allergies Verified' badge displayed.", "api_effect": "None", "audit_effect": "None", "output": "Allergy clearance", "next_state": "WFSTATE-005-002", "failure_possibility": "New allergy reported."},
            {"title": "Demographic Delta Check & Contact Confirmation", "actor": "Registration Clerk (`ACT-WF05-01`)", "input": "Asks: 'Is your phone still 9845012345?'", "action": "Citizen confirms phone and address unchanged.", "sys_behavior": "Updates `last_contact_verified_at` timestamp.", "validation": "Confirmation recorded", "db_effect": "Updates `patients.last_verified_at`", "ui_effect": "Marks demographic delta green.", "api_effect": "POST /api/v1/patients/{id}/verify-contact", "audit_effect": "None", "output": "Contact confirmed", "next_state": "WFSTATE-005-003", "failure_possibility": "Phone changed."},
            {"title": "Active Chronic Episode Linking", "actor": "Registration Clerk (`ACT-WF05-01`)", "input": "Revisit reason: Monthly Hypertension refill", "action": "Selects active episode: `EPISODE-NCD-HYP-2026`.", "sys_behavior": "Links new visit to existing chronic care cohort.", "validation": "Episode active", "db_effect": "Inserts row in `episode_visits`", "ui_effect": "Displays episode badge: 'Visit #5 of 12'.", "api_effect": "POST /api/v1/episodes/{id}/link-visit", "audit_effect": "WFAUDIT-005-002 (Episode Linked)", "output": "Linked episode", "next_state": "WFSTATE-005-004", "failure_possibility": "Episode expired."},
            {"title": "Defaulter Flag Resolution", "actor": "System", "input": "Follow-up schedule check", "action": "Checks if appointment was overdue; resolves alert.", "sys_behavior": "Updates NCD tracker status from `OVERDUE` to `ATTENDED`.", "validation": "Flag cleared", "db_effect": "Updates `ncd_followups.status = 'ATTENDED'`", "ui_effect": "Notification badge cleared.", "api_effect": "POST /api/v1/ncd/defaulter/clear", "audit_effect": "WFAUDIT-005-003 (Defaulter Flag Cleared)", "output": "Defaulter status cleared", "next_state": "WFSTATE-005-005", "failure_possibility": "None."},
            {"title": "Repeat Priority Token Issuance", "actor": "Registration Clerk (`ACT-WF05-01`)", "input": "Click 'Issue Repeat Token'", "action": "Prints thermal token tagged with 'NCD Revisit - Senior'.", "sys_behavior": "Mints Token SNR-003; enqueues into Nurse Triage Queue.", "validation": "Token generated", "db_effect": "Inserts row in `patient_queue_tokens`", "ui_effect": "Thermal printer dispenses token slip.", "api_effect": "POST /api/v1/tokens/generate", "audit_effect": "WFAUDIT-005-004 (Repeat Token Issued)", "output": "Printed repeat token slip", "next_state": "WFSTATE-005-006", "failure_possibility": "Printer jam."}
        ],
        "alternate_flows": [
            {
                "id": "WFALT-005-001", "title": "Citizen Reports New Contact Phone Number",
                "condition": "Citizen changed SIM card or mobile phone number since last visit.",
                "from_step": "WFSTEP-005-003",
                "steps": [
                    "Clerk clicks 'Update Phone Number'.",
                    "Enters new 10-digit number; system validates regex `^[6-9]\\d{9}$`.",
                    "Sends instant verification OTP or records verbal declaration.",
                    "Updates primary phone on master record and prints updated card if requested."
                ],
                "rejoin": "Rejoins main flow at Step WFSTEP-005-004 (Episode Linking).",
                "audit": "WFAUDIT-005-ALT01 (Phone Number Updated)"
            }
        ],
        "exception_flows": [
            {
                "id": "WFEX-005-001", "title": "Lost Clinic Card Replacement",
                "trigger": "Patient arrives stating physical card was misplaced or washed.",
                "detection": "Patient cannot present card for QR scan.",
                "containment": "Clerk performs phone number lookup to find existing master record.",
                "msg_en": "Lost card reported. Found master record. Issuing replacement card free of charge.",
                "msg_kn": "ಕಳೆದುಹೋದ ಕಾರ್ಡ್ ವರದಿಯಾಗಿದೆ. ಹೊಸ ಕಾರ್ಡ್ ಅನ್ನು ಉಚಿತವಾಗಿ ನೀಡಲಾಗುತ್ತಿದೆ.",
                "recovery": "Clerk clicks 'Print Replacement Card'; system prints identical card with existing UHID.",
                "audit": "WFAUDIT-005-EX01", "severity": "LOW"
            }
        ],
        "emergency_flow": {
            "triggers": "Returning patient experiences acute chest pain while waiting at desk.",
            "escalation": "Immediate Code Red button activation.",
            "preemption": "Bypasses check-in; moves directly to doctor chamber.",
            "bypass_rules": "Doctor immediately opens existing record using UHID.",
            "safety_controls": "Full previous medical history available to doctor instantly.",
            "reconciliation": "Token issued retrospectively post-stabilization.",
            "audit_event": "WFAUDIT-005-EMERGENCY",
            "signoff_sla": "2 hours"
        },
        "states": [
            {"name": "REVISIT_LOOKUP", "desc": "Scanning card and retrieving longitudinal record.", "allowed": "Scan, search", "prohibited": "Token print", "actor": "Clerk"},
            {"name": "DELTA_VERIFY", "desc": "Confirming phone and address changes.", "allowed": "Update contact", "prohibited": "Encounter start", "actor": "Clerk"},
            {"name": "EPISODE_LINKING", "desc": "Binding visit to active care plan.", "allowed": "Link care plan", "prohibited": "Deleting episodes", "actor": "Clerk"},
            {"name": "TOKEN_DISPENSED", "desc": "Repeat token printed; enqueued for triage.", "allowed": "Queue advancement", "prohibited": "Re-intake", "actor": "System"}
        ],
        "transitions": [
            {"from_state": "REVISIT_LOOKUP", "event": "Record Loaded", "actor": "Clerk", "condition": "UHID valid", "validation": "Record found", "to_state": "DELTA_VERIFY", "side_effects": "Show delta", "audit": "WFAUDIT-005-TR01"},
            {"from_state": "DELTA_VERIFY", "event": "Contact Confirmed", "actor": "Clerk", "condition": "Confirmed", "validation": "Delta OK", "to_state": "EPISODE_LINKING", "side_effects": "Check episode", "audit": "WFAUDIT-005-TR02"},
            {"from_state": "EPISODE_LINKING", "event": "Episode Bound", "actor": "Clerk", "condition": "Episode active", "validation": "Link OK", "to_state": "TOKEN_DISPENSED", "side_effects": "Print token", "audit": "WFAUDIT-005-TR03"}
        ],
        "decision_tables": [
            {
                "id": "WFDEC-005-001", "title": "Repeat Visit Triage Fast-Track Decision Table",
                "desc": "Determines whether returning patient requires full vital signs screening or focused check.",
                "conditions": ["Visit within 7 days", "Routine Chronic Refill", "No New Symptoms", "Baseline Stable"],
                "actions": ["Full Vitals Panel Required", "Focused BP/Sugar Check Only", "Fast-Track Doctor Call", "Immediate Emergency Call"],
                "rows": [
                    {"rule": "R1", "cond_vals": ["YES", "YES", "YES", "YES"], "act_vals": ["NO", "YES", "YES", "NO"]},
                    {"rule": "R2", "cond_vals": ["NO", "ANY", "ANY", "ANY"], "act_vals": ["YES", "NO", "NO", "NO"]},
                    {"rule": "R3", "cond_vals": ["ANY", "NO", "YES", "ANY"], "act_vals": ["YES", "NO", "NO", "NO"]}
                ]
            }
        ],
        "validation_rules": [
            {"id": "WFVAL-005-001", "field": "uhid", "expr": "patient_exists(uhid)", "code": "ERR-VAL-05-01", "msg_en": "UHID not found in master clinic registry.", "msg_kn": "UHID ಕ್ಲಿನಿಕ್ ದಾಖಲೆಯಲ್ಲಿ ಕಂಡುಬಂದಿಲ್ಲ.", "recovery": "Search by phone number.", "test_ref": "WFTEST-005-001"}
        ],
        "business_rules": [
            {"id": "BRULE-WF05-001", "title": "Chronic Care Episode Continuity Invariant", "req": "BRULE-005", "spec": "All visits for existing chronic disease management shall be linked to the primary episode ID to maintain longitudinal audit records.", "enforcement": "System mandates episode selection for chronic visit types.", "consequence": "Prevents fragmented treatment records."}
        ],
        "clinical_rules": [
            {"id": "CR-WF05-001", "title": "Mandatory Blood Pressure Trend Graph Display", "req": "CR-005", "rationale": "Hypertension control must be evaluated based on trajectory, not single isolated reading.", "logic": "EMR renders interactive 6-month blood pressure line chart upon encounter open.", "override_policy": "None. Graph is standard EMR view.", "safety_invariant": "Historical trend always visible to clinician."}
        ],
        "operational_rules": [
            {"id": "OR-WF05-001", "title": "Free Replacement Card Policy", "req": "OR-005", "mandate": "Lost or damaged clinic cards must be reprinted immediately without charging any fee.", "boundary": "Registration desk.", "exception": "None."}
        ],
        "security_controls": [
            {"domain": "Access Control", "id": "SEC-WF05-01", "spec": "Revisit intake restricted to authenticated staff terminals.", "param": "JWT verification", "threat": "Unauthorized access", "compliance": "SECR-002"}
        ],
        "privacy_controls": [
            {"principle": "Data Accuracy", "id": "PRIV-WF05-01", "spec": "Demographic verification at each return visit ensures personal data remains accurate and up to date.", "invariant": "Right to correction active", "right": "DPDP Act Sec 12"}
        ],
        "offline_behavior": {
            "online_mode": "Fetches complete multi-year cloud medical history.",
            "detection_latency": "< 1 second.",
            "local_storage": "SQLite database holding 90-day local encounter history for all clinic patients.",
            "queue_mechanics": "Episode links queued in local mutation log; replayed on reconnect.",
            "degraded_scope": "Full repeat visit workflow operates smoothly using local 90-day cached history.",
            "sync_convergence": "Reconciles episode visits with cloud database upon reconnection.",
            "conflict_invariants": "Episode linkage records are append-only with zero merge conflicts."
        },
        "diagrams": {
            "data_flow": """flowchart TD
    Patient["Returning Citizen"] -->|Presents Card| Clerk["Registration Clerk"]
    Clerk -->|Scan QR| Scanner["Barcode Scanner"]
    Scanner --> UI["Revisit Intake UI"]
    UI -->|Load History| LocalDB[("Local 90-Day SQLite DB")]
    UI -->|Link Episode| LocalDB
    UI -->|Print Repeat Token| Printer["Thermal Slip Printer"]
    Printer --> Token["Repeat Token SNR-003"]
    Token --> Patient""",
            "sequence": """sequenceDiagram
    actor C as Citizen
    actor K as Clerk
    participant UI as Revisit Screen
    participant DB as SQLite DB
    C->>K: 1. Presents return clinic card
    K->>UI: 2. Scan QR code
    UI->>DB: 3. Query patient & active episodes
    DB-->>UI: 4. Return history: Hypertension Episode #5
    K->>UI: 5. Confirm phone unchanged
    K->>UI: 6. Select 'Link to Hypertension Episode'
    UI->>DB: 7. Commit visit link & clear defaulter flag
    UI-->>K: 8. Trigger thermal repeat token print
    K-->>C: 9. Hand over Token SNR-003 & direct to Triage""",
            "activity": """flowchart TD
    Start([Citizen Presents Card]) --> ScanCard[Scan Clinic Card QR]
    ScanCard --> LoadRecord[Load Longitudinal History]
    LoadRecord --> VerifyPhone{Phone Number Changed?}
    VerifyPhone -- Yes --> UpdatePhone[Update Primary Contact Phone] --> CheckEpisode
    VerifyPhone -- No --> CheckEpisode[Identify Active Chronic Episode]
    CheckEpisode --> Defaulter{Was Follow-Up Overdue?}
    Defaulter -- Yes --> ClearDefaulter[Clear Defaulter Alert in NCD Tracker] --> MintToken
    Defaulter -- No --> MintToken[Mint Repeat Priority Token]
    MintToken --> PrintSlip[Print Thermal Token Slip with Episode Tag]
    PrintSlip --> EnqueueTriage[Auto-Enqueue into Triage Queue] --> End([Revisit Intake Done])""",
            "state": """stateDiagram-v2
    [*] --> REVISIT_LOOKUP
    REVISIT_LOOKUP --> DELTA_VERIFY: Card Scanned & Record Loaded
    DELTA_VERIFY --> EPISODE_LINKING: Contact Verified
    EPISODE_LINKING --> TOKEN_DISPENSED: Episode Linked & Defaulter Cleared
    TOKEN_DISPENSED --> [*]"""
        },
        "data_flow_nodes": [
            {"name": "UI", "desc": "Repeat patient intake component in registration module.", "protocol": "HTTPS", "encryption": "TLS 1.3"},
            {"name": "LocalDB", "desc": "SQLite database with SQLCipher encryption storing active episodes.", "protocol": "SQLite C-API", "encryption": "AES-256 at rest"}
        ],
        "failure_tree": [
            {"id": "FT-005-001", "cat": "Software", "root": "Episode table lock timeout", "vector": "Concurrent visit linking", "impact": "Delay in token generation", "detection": "SQLite lock error", "mitigation": "Auto-retry with exponential backoff"}
        ],
        "recovery_procedures": [
            {"id": "REC-WF05-01", "title": "Orphan Visit Reconciliation Runbook", "trigger": "Visit created without episode link due to network timeout.", "containment": "Flags visit in unlinked queue.", "steps": ["Clerk opens 'Unlinked Visits' tab.", "Selects patient and clicks 'Link to Existing Episode'.", "System binds encounter to episode retroactively."], "rollback": "None", "resumption": "Episode linkage restored.", "audit": "WFAUDIT-005-REC01"}
        ],
        "audit_events": [
            {"id": "WFAUDIT-005-001", "event": "REVISIT_INTAKE_RECORDED", "actor": "Clerk", "meta": "{ patient_id, uhid, visit_no: 5 }", "state_before": "IDLE", "state_after": "INTAKE", "hmac": "HMAC-SHA256", "retention": "7 Years", "compliance": "Clinical Records Act"},
            {"id": "WFAUDIT-005-002", "event": "CHRONIC_EPISODE_LINKED", "actor": "Clerk", "meta": "{ patient_id, episode_id: 'NCD-HYP-01' }", "state_before": "UNLINKED", "state_after": "LINKED", "hmac": "HMAC-SHA256", "retention": "7 Years", "compliance": "NCD Guidelines"}
        ],
        "notifications": [
            {"id": "WFNOTIF-005-01", "trigger": "Repeat Token Generated", "recipient": "Citizen", "channel": "SMS", "text_en": "Namma Clinic: Welcome back! Token SNR-003 issued for Hypertension review.", "text_kn": "ನಮ್ಮ ಕ್ಲಿನಿಕ್: ಮರಳಿ ಸ್ವಾಗತ! ರಕ್ತದೊತ್ತಡ ತಪಾಸಣೆಗಾಗಿ ಟೋಕನ್ SNR-003 ನೀಡಲಾಗಿದೆ.", "priority": "High", "retry": "1 retry", "fallback": "Thermal Slip"}
        ],
        "planned_apis": [
            {"id": "PLANNED-API-005-01", "method": "POST", "path": "/api/v1/episodes/link-visit", "desc": "Links returning patient visit to active chronic disease care plan.", "scope": "episodes:write", "req_schema": "{\n  \"patient_id\": \"uuid\",\n  \"episode_id\": \"uuid\",\n  \"visit_type\": \"CHRONIC_FOLLOWUP\"\n}", "res_schema": "{\n  \"visit_id\": \"uuid\",\n  \"episode_status\": \"ACTIVE\",\n  \"total_visits\": 5\n}", "errors": "400 Invalid Episode, 404 Patient Not Found", "idempotency": "Mandatory (Key: patient_id + episode_id + date)", "rate_limit": "60 req/min", "offline_support": "Local execution on edge node"}
        ],
        "planned_db": [
            {"id": "PLANNED-DB-005-01", "table": "chronic_care_episodes", "purpose": "Tracks longitudinal episodes for chronic disease management.", "pk": "episode_id (UUID)", "fks": "patient_id -> patients(patient_id)", "cols": [
                {"name": "episode_id", "type": "UUID", "null": "NOT NULL", "notes": "Primary Key"},
                {"name": "patient_id", "type": "UUID", "null": "NOT NULL", "notes": "Foreign Key to patients"},
                {"name": "condition_code", "type": "VARCHAR(20)", "null": "NOT NULL", "notes": "ICD-10 (e.g. I10 Hypertension)"},
                {"name": "status", "type": "VARCHAR(20)", "null": "NOT NULL", "notes": "ACTIVE | CONTROLLED | UNCONTROLLED | CLOSED"},
                {"name": "start_date", "type": "DATE", "null": "NOT NULL", "notes": "Episode start date"},
                {"name": "last_visit_date", "type": "DATE", "null": "NOT NULL", "notes": "Date of latest visit"}
            ], "indexes": "INDEX(patient_id, status), INDEX(condition_code)", "concurrency": "Optimistic Locking", "retention": "Permanent (10 years longitudinal archive)"}
        ],
        "planned_ui": [
            {"id": "PLANNED-UI-005-01", "screen": "Repeat Patient Revisit Dashboard", "route": "/patients/revisit", "persona": "Registration Clerk", "components": "Card scan listener, longitudinal timeline, active care plans, phone update field, 'Issue Repeat Token' button.", "states": "Scan Ready, History Loaded, Confirming Delta, Printing Token.", "validations": "Ensures active care plan selected before token generation.", "a11y": "Large action buttons; full keyboard navigation.", "localization": "Complete bilingual Kannada parity.", "offline_ui": "Shows 'Local History Cache (90 Days)' badge."}
        ],
        "backend_reqs": {
            "domain_services": "Orchestrates `EpisodeManagementService`, `NcdDefaulterTracker`, and `LongitudinalEhrService`.",
            "transactions": "Atomic episode linkage and token generation in single transaction.",
            "async_workers": "Background worker updates central NCD registry upon cloud reconnection.",
            "circuit_breakers": "Falls back to local cached episode state on cloud timeout."
        },
        "integrations": [
            {"id": "INT-WF05-01", "system": "National NCD Portal", "protocol": "REST / JSON", "payload": "Chronic patient visit attendance and adherence update", "direction": "Outbound", "timeout": "10 sec", "fallback": "Local buffer"}
        ],
        "reports": [
            {"id": "REP-WF05-01", "title": "NCD Cohort Attendance & Defaulter Monthly Report", "freq": "Monthly", "audience": "Zonal Health Officer, NCD Program Officer", "grain": "Per ward, per chronic condition", "ref": "REP-005"}
        ],
        "analytics": [
            {"id": "ANL-WF05-01", "kpi": "NCD Follow-Up Compliance Rate", "formula": "(attended_on_time / scheduled_followups) * 100", "dimensions": "Condition, Ward", "target": ">= 85.0%", "alert": "Compliance < 70% triggers ASHA outreach"}
        ],
        "ai_reqs": {
            "id": "AIR-WF05-01", "purpose": "Chronic Disease Control Risk Evaluation", "features": "Historical BP readings, pill count adherence, missed visits count",
            "output_signal": "Uncontrolled Hypertension Risk Score (0-1)", "confidence": "High risk if score >= 0.75", "explainability": "Explains: 'BP trending upward over past 3 consecutive visits'.",
            "authority": "Advisory alert to doctor.", "audit": "WFAUDIT-005-AI01"
        },
        "stride_threats": [
            {"id": "STRIDE-WF05-01", "cat": "Tampering", "asset": "Episode History", "scenario": "Unauthorized modification of past prescription history.", "likelihood": "Low", "impact": "High", "mitigation": "Past clinical encounters are cryptographically sealed and read-only.", "residual": "Zero", "test_ref": "WFTEST-005-001"}
        ],
        "linddun_threats": [
            {"id": "LINDDUN-WF05-01", "cat": "Detectability", "asset": "Chronic Disease Status", "vector": "Token label revealing sensitive chronic illness.", "likelihood": "Low", "impact": "Medium", "mitigation": "Token displays general category 'SNR / GEN'; never prints disease name.", "compliance": "DPDP Act"}
        ],
        "performance": {
            "e2e_latency": "Revisit lookup to token print < 30 seconds.", "ui_render": "History timeline renders in < 150ms.",
            "db_budget": "Episode lookup query < 15ms.", "concurrency": "30 revisits/second.",
            "payload": "Payload size < 8KB.", "hardware": "RAM < 50MB."
        },
        "availability": {
            "sla": "99.95% revisit intake availability.", "rto": "< 1 min.", "rpo": "0 visits lost.",
            "offline_autonomy": "100% operational autonomy using 90-day local cache.", "failover": "Local SQLite fallback."
        },
        "accessibility": {
            "screen_reader": "Full ARIA landmark coverage.", "contrast": "Contrast ratio >= 4.5:1.",
            "keyboard": "Tab order logical.", "touch": "Large touch targets.", "cognitive": "Clean visual timeline."
        },
        "localization": {
            "clinical_terms": "Standard ICD-10 with Kannada vernacular.", "printed_material": "Bilingual token slip.",
            "audio_prompts": "Kannada audio chime."
        },
        "test_gates": [
            {"level": "Unit Testing", "scope": "Episode linking, defaulter clearing logic", "tooling": "PyTest", "coverage": ">= 90%", "gate": "Zero failures on pre-commit"},
            {"level": "E2E Testing", "scope": "Revisit intake and longitudinal timeline render", "tooling": "Playwright", "coverage": "100% happy and alternate flows", "gate": "Green run on CI staging"}
        ],
        "bdd_scenarios": [
            {
                "id": "WFTEST-005-001", "title": "Successful Repeat Patient Revisit and Chronic Episode Linking",
                "category": "Happy Path", "priority": "P0",
                "given": "a registered 68-year-old patient with an active Hypertension care plan returns to clinic",
                "given_ands": ["the registration clerk scans the patient's thermal clinic card QR code"],
                "when": "the clerk confirms contact phone details and selects 'Monthly Hypertension Refill'",
                "when_ands": ["the system binds the visit to active episode EPISODE-NCD-HYP-2026"],
                "then": "the system clears any overdue defaulter alerts in the NCD tracking database",
                "then_ands": ["prints Token SNR-003 tagged with 'NCD Revisit' and pre-populates baseline vitals on Nurse screen within 20 seconds"]
            },
            {
                "id": "WFTEST-005-002", "title": "Lost Clinic Card Recovery and Free Replacement Issuance",
                "category": "Card Replacement", "priority": "P1",
                "given": "a returning chronic patient presents having misplaced their physical clinic card",
                "given_ands": ["the clerk executes a phone number search on the universal search bar"],
                "when": "the clerk locates the patient's master record and clicks 'Issue Replacement Card'",
                "when_ands": ["the thermal printer outputs an identical card with original UHID and QR code"],
                "then": "the patient's complete longitudinal history remains seamlessly connected",
                "then_ands": ["zero replacement fee is charged in strict accordance with the free primary care mandate"]
            }
        ],
        "acceptance_criteria": [
            {"id": "AC-WF-005-001", "criterion": "Repeat patient intake completed in <= 30 seconds.", "method": "Telemetry timer", "threshold": "p95 <= 30s", "gate": "Milestone 1 Core Gate"},
            {"id": "AC-WF-005-002", "criterion": "100% of returning NCD patients linked to active care plan.", "method": "Database audit query", "threshold": "100.0% linkage", "gate": "Clinical Governance Gate"}
        ],
        "dependencies": [
            {"id": "WFDEP-005-01", "upstream": "WF-004", "downstream": "WF-005", "nature": "Patient Lookup Dependency", "blocking": "BLOCKING", "impact": "Revisit requires looking up existing record.", "resilience": "Direct QR scan bypasses search modal."},
            {"id": "WFDEP-005-02", "upstream": "WF-005", "downstream": "WF-009", "nature": "Triage Handoff", "blocking": "BLOCKING", "impact": "Token routed to Nurse Triage queue.", "resilience": "None."}
        ],
        "critical_path": {
            "path": "Card Scan -> History Load -> Delta Check -> Episode Link -> Defaulter Clear -> Token Print.",
            "bottleneck": "Demographic confirmation conversation with citizen.",
            "load_balancing": "Dedicated repeat patient intake window during morning surge.",
            "recovery_bottlenecks": "Rebuilding local cache if SQLite disk corrupted."
        },
        "rollback_strategy": {
            "db_rollback": "Failed episode link rolls back transaction cleanly.",
            "saga_compensation": "None.", "notification_reversal": "None.",
            "audit_preservation": "All intake attempts permanently logged.",
            "offline_rollback": "None."
        },
        "idempotency": {
            "key_schema": "UUIDv4 on `patient_id + episode_id + date`.",
            "cache_store": "SQLite unique index.", "replay_behavior": "Returns existing token without double-enqueueing.",
            "ttl": "24 hours.", "offline_replay": "Reconciles visits cleanly on cloud."
        },
        "concurrency": {
            "occ": "Episode records use versioning.", "pessimistic": "None.",
            "queue_locking": "Atomic token counter.", "deadlock_policy": "Database timeout."
        },
        "invariants": [
            {"id": "INVARIANT-WF-005-01", "statement": "No repeat visit for an active chronic condition shall be recorded as an unlinked orphan encounter.", "scope": "Clinical Continuity Ledger", "enforcement": "System mandates episode selection for chronic visit types.", "consequence": "Blocks intake submission until episode linked."}
        ],
        "observability": [
            {"cat": "Metric", "name": "namma_clinic_revisit_intake_seconds", "type": "Histogram", "labels": "clinic_id, category", "target": "Prometheus", "alert": "p95 > 45s alerts coordinator"}
        ],
        "runbook": {
            "morning_sop": "Check barcode scanner. Verify printer has paper for repeat tokens.",
            "live_sop": "Scan card QR. Verify phone number verbally. Issue repeat token in < 30 seconds.",
            "troubleshooting_sop": "If card lost: Search by phone number. Reprint card free of charge.",
            "closing_sop": "Review daily NCD revisit tally. Ensure all visits linked to episodes."
        },
        "sla_slo": [
            {"name": "Revisit Intake Latency", "target": "< 30 seconds", "window": "Per patient", "warning": "> 45s", "escalation": "Coordinator alerted"}
        ],
        "traceability": [
            {"req": "FR-005", "type": "Functional Req", "step": "WFSTEP-005-004", "state": "WFSTATE-005-004", "api": "PLANNED-API-005-01", "db": "PLANNED-DB-005-01", "ui": "PLANNED-UI-005-01", "test": "WFTEST-005-001"}
        ],
        "open_questions": [
            {"id": "OQ-WF05-01", "subject": "Automated Fast-Track Pharmacy Refill for Stable NCDs", "query": "Can stable hypertension patients with normal home BP readings bypass the doctor consultation room and proceed directly from triage to pharmacy refill?", "impact": "Would reduce doctor room load by 35%.", "owner": "Chief Medical Officer", "milestone": "Milestone 3"}
        ],
        "assumptions": [
            {"id": "ASM-WF05-01", "cat": "Clinical", "statement": "Returning patients carry their physical clinic card in >= 80% of visits.", "status": "CONFIRMED", "risk": "Fast phone search handles the remaining 20%."}
        ],
        "risks": [
            {"id": "RSK-WF05-01", "desc": "Patients failing to report new symptoms, assuming visit is only for pill refill.", "prob": "Medium", "impact": "High", "mitigation": "Triage nurse explicitly asks standardized symptom review questions.", "contingency": "Doctor conducts full review if BP elevated.", "owner": "Staff Nurse"}
        ],
        "change_impact": [
            {"vector": "National NCD Portal API Specification Update", "scenario": "Central government updates NCD portal sync protocol.", "components": "NCD sync worker, episode mapping schema", "severity": "MEDIUM", "testing": "NCD portal integration regression tests"}
        ],
        "definition_of_ready": [
            {"id": "DOR-WF05-01", "criterion": "Repeat patient specification approved by NCD clinical lead.", "artifact": "WF-005 Doc", "signoff": "Clinical Director"}
        ],
        "definition_of_done": [
            {"id": "DOD-WF05-01", "criterion": "100% pass on automated Playwright repeat patient test suite.", "method": "Automated test report", "benchmark": "Zero failures across 30 simulated return visits"}
        ],
        "related_workflows": [
            {"rel": "Upstream Dependency", "id": "WF-004", "name": "Patient Search Workflow", "interface": "Patient Lookup"},
            {"rel": "Downstream Workflow", "id": "WF-009", "name": "Nursing Triage & Vitals Workflow", "interface": "Triage Queue Entry"}
        ]
    }
    return build_workflow_object(spec)

def get_group1_workflows():
    return {
        "WF-001": make_wf01_data(),
        "WF-002": make_wf02_data(),
        "WF-003": make_wf03_data(),
        "WF-004": make_wf04_data(),
        "WF-005": make_wf05_data(),
    }

if __name__ == "__main__":
    from workflow_generator import render_workflow_document
    from common import count_lines
    print("Testing data_wf01_to_05.py...")
    wfs = get_group1_workflows()
    for wfid, wf_data in wfs.items():
        doc = render_workflow_document(wf_data)
        counts = count_lines(doc)
        status = "PASS" if counts["substantive"] >= 2000 else "FAIL"
        print(f"  {wfid}: Total = {counts['total']}, Substantive = {counts['substantive']} [{status}]")
