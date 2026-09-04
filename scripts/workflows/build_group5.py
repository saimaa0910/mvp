#!/usr/bin/env python3
"""
build_group5.py
Generates data_wf21_to_25.py covering:
  WF-021: Clinical Analytics, Syndromic Surveillance & Population Health Reporting Workflow
  WF-022: Autonomous Offline Edge Operation, Local Storage & Network Resilience Workflow
  WF-023: Bidirectional Synchronization, Conflict Resolution & Merkle Ledger Workflow
  WF-024: Ayushman Bharat Digital Mission (ABDM) Gateway & FHIR Interoperability Workflow
  WF-025: Clinical Emergency Exception, Fast-Track Bypass & Resuscitation Protocol Workflow
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_factory import build_workflow_object
from workflow_metadata import WORKFLOW_MAP

def get_group5_specs():
    specs = {}

    # =========================================================================
    # WF-021: Analytics & Syndromic Surveillance Workflow
    # =========================================================================
    m21 = WORKFLOW_MAP["WF-021"]
    specs["WF-021"] = {
        "id": "WF-021", "num": "21", "name": m21["name"], "domain": m21["domain"],
        "exec_summary": {
            "purpose": "Aggregates de-identified clinical, diagnostic, and operational event streams from across Namma Clinics into real-time analytical cubes. Computes epidemiological syndromic surveillance spikes (fever clusters, acute diarrheal disease, dengue/chikungunya signals, acute respiratory infections) for the Integrated Disease Surveillance Programme (IDSP), tracks clinic operational KPIs, and generates automated daily health bulletins.",
            "rationale": "Urban outbreaks in high-density informal settlements spread rapidly unless intercepted within 24-48 hours. Real-time syndromic surveillance transforms primary clinics into early-warning sensors for municipal public health authorities, preventing widespread epidemics.",
            "clinical_impact": "Identifies localized disease outbreaks days before formal hospital admissions occur; enables targeted public health fumigation, water chlorination, and mobile medical camp deployment.",
            "system_impact": "Consumes de-identified events via Kafka/RabbitMQ streams; builds OLAP analytical rollups; and exposes secure REST endpoints for BBMP Central Health Command and National IDSP portals.",
            "risk_profile": "Data re-identification through small population cell sizes; delayed data sync from offline edge nodes; false-positive outbreak alarms; and uncalibrated anomaly detection thresholds."
        },
        "objectives": [
            {"id": "OBJ-WF21-01", "title": "Real-Time Outbreak Detection", "desc": "Detect and flag statistical disease clusters (>= 3 SD above 30-day baseline) within 15 minutes of encounter sign-off.", "metric": "Surveillance Alert Latency < 15 min", "verification": "Simulated syndromic spike injection test suite"},
            {"id": "OBJ-WF21-02", "title": "Zero PHI Leakage in Analytics", "desc": "Enforce k-anonymity (k >= 5) and differential privacy across all analytical cubes, stripping 100% of direct identifiers.", "metric": "Direct PHI Leakage = 0", "verification": "Automated privacy audit and penetration query tests"},
            {"id": "OBJ-WF21-03", "title": "Daily IDSP Bulletin Automation", "desc": "Generate and transmit standardized S-Form and P-Form reports to the District Surveillance Officer by 20:30 IST daily.", "metric": "Report Transmission Compliance = 100%", "verification": "State surveillance portal submission receipts"},
            {"id": "OBJ-WF21-04", "title": "Interactive Operational KPIs", "desc": "Render multi-clinic operational performance metrics (wait times, transit times, stockouts) with < 1.0s dashboard query latency.", "metric": "Dashboard Query Latency p95 < 1.0s", "verification": "OLAP analytics engine query benchmarks"}
        ],
        "in_scope": [
            {"area": "Syndromic Signal Tracking", "desc": "Acute Diarrheal Disease (ADD), Fever with Rash, Acute Flaccid Paralysis, Dengue/Chikungunya, and ARI/SARI clusters."},
            {"area": "De-Identification Pipeline", "desc": "Hashing of UHID, masking of exact street addresses to municipal ward level, and age grouping into 5-year cohorts."},
            {"area": "OLAP Aggregation", "desc": "Multi-dimensional indexing by Ward, Clinic, Age Band, Gender, ICD-10 Category, and Diagnosis Date."},
            {"area": "Automated Bulletin Generation", "desc": "Rendering PDF and CSV daily health bulletins for municipal commissioners and health officers."}
        ],
        "out_of_scope": [
            {"area": "Commercial Data Monetization", "desc": "Selling analytics to private pharmaceutical companies; strictly prohibited under municipal public health charter.", "handoff": "None - Strictly Prohibited"},
            {"area": "Genomic Sequencing Analysis", "desc": "Bioinformatics pathogen genomic sequencing; out of scope for primary clinic analytics.", "handoff": "National Centre for Biological Sciences (NCBS)"}
        ],
        "actors": [
            {"id": "ACT-WF21-01", "type": "Human", "name": "Zonal Epidemiologist / Public Health Officer", "responsibilities": "Monitors syndromic spike alerts, investigates ward clusters, coordinates field verification teams.", "permissions": "Analytics Read-Only, Outbreak Flag Confirm, Field Task Issue", "failure_duty": "Manually investigates unexplained clusters via telephonic verification with clinic doctors.", "inputs": "Syndromic surveillance maps, fever cluster alerts", "decisions": "Determines whether a spike represents a genuine public health outbreak.", "outputs": "Outbreak investigation directive, public health advisory", "recovery": "Adjusts statistical baseline parameters to filter seasonal noise."},
            {"id": "ACT-WF21-02", "type": "Human", "name": "Chief Health Officer (BBMP)", "responsibilities": "Reviews citywide executive health dashboard, allocates resources, issues containment orders.", "permissions": "Executive Analytics View, Resource Allocation Authorization", "failure_duty": "Mobilizes emergency health commissioner meetings upon multi-ward epidemic alert.", "inputs": "Citywide daily health bulletins, stockout heat-maps", "decisions": "Authorizes emergency medicine deployments and mobile fever clinics.", "outputs": "Executive public health directives", "recovery": "Orders immediate ground epidemiologic survey."}
        ],
        "personas": [
            {"id": "PERSONA-005", "name": "Dr. Pradeep Kumar", "role": "Zonal Epidemiologist", "env": "BBMP South Zone Health Command Center.", "goals": "Spot a dengue fever cluster in Padmanabhanagar before it becomes an emergency.", "pain_points": "Paper disease surveillance reports arriving two weeks late from peripheral clinics.", "adaptations": "Interactive geospatial heat-map showing live fever cases by ward with automated WhatsApp alerts."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-005", "title": "Zonal Epidemiologist", "read": "De-Identified Analytics, Geospatial Maps", "create": "Outbreak Ticket", "update": "Investigation Status", "delete": "None", "override": "None", "signoff": "Epidemiology Signoff"},
            {"role": "ROLE-006", "title": "Chief Health Officer", "read": "Executive Citywide Analytics", "create": "Containment Order", "update": "Policy Config", "delete": "None", "override": "Executive Action", "signoff": "City Health Bulletin Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF21-01", "desc": "Analytical event ingestion pipeline connected to clinic edge streaming nodes.", "check": "analytics_stream.status == 'CONNECTED'", "on_fail": "Buffer events locally in SQLite analytics delta tables."},
            {"id": "PRE-WF21-02", "desc": "Differential privacy and k-anonymity masking engine initialized with approved epsilon parameter.", "check": "privacy_engine.is_active == TRUE", "on_fail": "Halt analytical query execution; raw PHI must never be exposed."}
        ],
        "triggers": [
            {"id": "TRIG-WF21-01", "class": "Encounter Commit Trigger", "event": "Doctor signs encounter with syndromic diagnosis code (A09, R50, J06, A90)", "source": "Clinical EMR Middleware", "payload": "{ ward_id: 'W085', icd10: 'A90', age_group: 'ADULT' }", "latency": "< 2.0s to update analytical cube"},
            {"id": "TRIG-WF21-02", "class": "Scheduled Cron", "event": "Daily IDSP aggregation executes at 20:00 IST", "source": "Central Cron Worker", "payload": "{ report_date: '2026-09-04' }", "latency": "< 30 sec to compile citywide report"}
        ],
        "inputs": [
            {"name": "ward_id", "type": "String(8)", "req": "Mandatory", "source": "Facility Config", "val": "Valid BBMP ward identifier", "priv": "Operational", "enc": "Plaintext", "ex": "W085", "on_err": "Flag unmapped facility"},
            {"name": "syndrome_category", "type": "Enum(FEVER, DIARRHEA, RESPIRATORY, JAUNDICE, RASH)", "req": "Mandatory", "source": "Diagnosis Classifier", "val": "Defined syndrome", "priv": "Operational", "enc": "Plaintext", "ex": "FEVER", "on_err": "Default to OTHER"}
        ],
        "outputs": {
            "success": [
                {"name": "Real-Time Geospatial Epidemic Alert", "desc": "Push alert dispatched to Zonal Epidemiologist indicating statistical case cluster.", "format": "JSON Alert Payload & Map Marker", "recipient": "Epidemiology Dashboard & SMS"},
                {"name": "Standard IDSP S-Form / P-Form", "desc": "Standardized electronic disease surveillance bulletin.", "format": "PDF / CSV Export", "recipient": "National IDSP Portal & BBMP Health Portal"}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    participant CLIN as Clinic EMR
    participant DEID as De-Identification Pipeline
    participant OLAP as Analytics Cube
    participant ANOM as Anomaly Detector
    actor EPI as Zonal Epidemiologist
    CLIN->>DEID: 1. Event: Encounter Signed (ICD-10 A90 Dengue, Ward 85)
    DEID->>DEID: 2. Strip Patient ID, Mask Age to 35-39, Hash UHID
    DEID->>OLAP: 3. Ingest De-Identified Event into OLAP Cube
    OLAP->>ANOM: 4. Check Ward 85 7-day Moving Average (Baseline: 2 cases/day)
    ANOM->>ANOM: 5. Detected Spike: 9 cases today (> 3 Standard Deviations)
    ANOM->>EPI: 6. Push Urgent Alert: 'Dengue Cluster Detected in Ward 85!'
    EPI->>EPI: 7. Review Geospatial Cluster -> Dispatch Field Larval Team""",
        "activity_diagram": """flowchart TD
    Start([Encounter Committed in Clinic EMR]) --> ExtractClinicalData[Extract Diagnosis, Symptoms, Ward, and Demographics]
    ExtractClinicalData --> RunDeIdentification[De-Identification Pipeline: Strip Name, Exact Address, Phone]
    RunDeIdentification --> CheckKAnonymity{Does Cluster Meet k >= 5 Anonymity?}
    CheckKAnonymity -- No --> GeneralizeCell[Generalize Cell: Broaden Age Group / Ward Boundary]
    GeneralizeCell --> IngestOLAP[Ingest Record into Central OLAP Analytical Cube]
    CheckKAnonymity -- Yes --> IngestOLAP
    IngestOLAP --> CalculateMovingAverage[Calculate 7-Day & 30-Day Moving Averages by Ward]
    CalculateMovingAverage --> DetectAnomaly{Is Current Count > 3 Standard Deviations?}
    DetectAnomaly -- Yes --> TriggerEpidemicAlert[Trigger High-Priority Outbreak Alert on Zonal Map]
    TriggerEpidemicAlert --> NotifyEpidemiologist[Send Instant WhatsApp/SMS to Zonal Epidemiologist]
    DetectAnomaly -- No --> UpdateStandardKPIs[Update Routine Operational Dashboard KPIs]
    NotifyEpidemiologist --> CompileDailyReport[Aggregate Daily IDSP S/P Form Bulletins at 20:00]
    UpdateStandardKPIs --> CompileDailyReport
    CompileDailyReport --> End([Analytics Processing Concluded])""",
        "state_diagram": """stateDiagram-v2
    [*] --> EVENT_INGESTED
    EVENT_INGESTED --> DE_IDENTIFIED: PHI Stripped & Hashed
    DE_IDENTIFIED --> CUBE_UPDATED: Aggregated in OLAP
    CUBE_UPDATED --> SPIKE_DETECTED: Anomaly Threshold Breached
    CUBE_UPDATED --> ROUTINE_LOGGED: Normal Baseline Variation
    SPIKE_DETECTED --> OUTBREAK_ALERTED: Epidemiologist Notified
    OUTBREAK_ALERTED --> INVESTIGATION_ACTIVE: Field Team Deployed
    INVESTIGATION_ACTIVE --> RESOLVED: Containment Measures Complete
    ROUTINE_LOGGED --> [*]
    RESOLVED --> [*]"""
    }

    # =========================================================================
    # WF-022: Offline-First Edge Operations Workflow
    # =========================================================================
    m22 = WORKFLOW_MAP["WF-022"]
    specs["WF-022"] = {
        "id": "WF-022", "num": "22", "name": m22["name"], "domain": m22["domain"],
        "exec_summary": {
            "purpose": "Establishes full operational autonomy for Namma Clinic facilities when wide-area Internet connectivity (WAN/Broadband/4G) is severed. Maintains local clinic Local Area Network (LAN) operations across all workstations, authenticates users via locally salted cryptographic credentials, writes mutations to an encrypted persistent local SQLite Write-Ahead Log (WAL) queue, manages local disk storage quotas, and provides seamless visual degraded-mode indicators.",
            "rationale": "Urban primary health centers in Bengaluru frequently experience fiber cuts from road construction and mobile tower congestion. Under the municipal citizen charter, zero citizens can be turned away due to IT failures. WF-022 ensures the clinic functions with 100% clinical efficacy for up to 72 continuous hours disconnected from the cloud.",
            "clinical_impact": "Completely prevents clinic paralysis during telecommunication failures; enables uninterrupted triage, clinical documentation, drug prescribing, point-of-care lab testing, and dispensing.",
            "system_impact": "Powers the platform's local edge node architecture; utilizes mDNS/Bonjour for terminal discovery; executes local SQLite database transactions; and stages delta batches for deferred synchronization.",
            "risk_profile": "Local edge server physical theft; edge database corruption; edge hard drive disk exhaustion; and clock drift across disconnected workstations."
        },
        "objectives": [
            {"id": "OBJ-WF22-01", "title": "72-Hour Standalone Autonomy", "desc": "Maintain 100% of primary clinical and dispensing functions during continuous 72-hour WAN disconnection.", "metric": "Offline Operational Availability = 100%", "verification": "72-hour network severed physical simulation test"},
            {"id": "OBJ-WF22-02", "title": "Sub-3s Disconnection Detection", "desc": "Detect wide-area network severance and transition all terminals to degraded offline mode within 3.0 seconds.", "metric": "Offline Transition Latency < 3.0s", "verification": "Heartbeat failure telemetry assertion"},
            {"id": "OBJ-WF22-03", "title": "Zero Transaction Loss (RPO = 0)", "desc": "Guarantee zero loss of locally committed patient encounters, vitals, or stock decrements during sudden power off.", "metric": "RPO = 0 lost records", "verification": "Simulated hard power-cut during active writing test"},
            {"id": "OBJ-WF22-04", "title": "Sub-10ms Local Transaction Commit", "desc": "Execute local SQLite write-ahead transactions in < 10.0 milliseconds per operation on low-power edge hardware.", "metric": "Local Write Latency p95 < 10ms", "verification": "Edge hardware write performance benchmark"}
        ],
        "in_scope": [
            {"area": "Network Health Watchdog", "desc": "Continuous heartbeat ping to cloud gateway with automatic graceful degradation upon 3 consecutive missed pings."},
            {"area": "Local Credential Verification", "desc": "Offline authentication against locally cached, scrypt-hashed credentials with rolling 7-day offline validity."},
            {"area": "Encrypted Local Storage", "desc": "SQLCipher / SQLite WAL encrypted database storage with deterministic UUIDv4 primary keys."},
            {"area": "LAN Peer Discovery", "desc": "Local mDNS service broadcasting allowing registration kiosk, triage tablet, and doctor PC to locate edge server without DNS."}
        ],
        "out_of_scope": [
            {"area": "Real-Time National Registry Lookups", "desc": "Querying national Aadhaar/UIDAI or central ABDM registries while internet is offline.", "handoff": "Deferred to Reconnection Sync WF-023"},
            {"area": "Live Telemedicine Video Calls", "desc": "Video streaming to remote specialists; requires active broadband connectivity.", "handoff": "Rescheduled or converted to offline local care"}
        ],
        "actors": [
            {"id": "ACT-WF22-01", "type": "System", "name": "Edge Node Orchestrator", "responsibilities": "Monitors WAN link, switches mode, hosts local SQLite DB and WebSocket hub, manages storage quotas.", "permissions": "System Master, Storage Manage, LAN Discovery Host", "failure_duty": "Reboots daemon in safe recovery mode if SQLite format error occurs.", "inputs": "Cloud heartbeat pings, local LAN terminal requests", "decisions": "Determines whether platform is in Online, Degraded Offline, or Reconnecting mode.", "outputs": "Mode transition events, local transaction receipts", "recovery": "Restores database from hourly local snapshot."},
            {"id": "ACT-WF22-02", "type": "Human", "name": "Frontline Clinical User (Nurse/Doctor)", "responsibilities": "Continues patient care, observes amber 'Offline Mode' indicator, avoids clearing browser caches.", "permissions": "Offline Data Entry, Local Signoff", "failure_duty": "Notifies clinic coordinator if terminal loses LAN Wi-Fi connection.", "inputs": "Patient presence, amber offline banner", "decisions": "Continues normal clinical workflows without alteration.", "outputs": "Committed local encounters", "recovery": "Re-enters transaction if local terminal crashes before commit."}
        ],
        "personas": [
            {"id": "PERSONA-001", "name": "Sister Bhavani Gowda", "role": "Staff Nurse", "env": "High-speed morning intake when underground optical fiber cable is accidentally severed outside.", "goals": "Keep issuing tokens and checking vitals without the software freezing.", "pain_points": "Cloud-only software that locks up with a spinning wheel when internet drops.", "adaptations": "Seamless transition: an amber badge appears in the top corner ('Offline Mode - Data Saved Locally'), but all forms respond instantly."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "Local Cache", "create": "Offline Records", "update": "Local Vitals", "delete": "None", "override": "None", "signoff": "Offline Signoff"},
            {"role": "ROLE-002", "title": "Medical Officer", "read": "Local Cache", "create": "Offline Encounters, Orders", "update": "Local Drafts", "delete": "None", "override": "Offline Emergency Override", "signoff": "Offline Digital Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF22-01", "desc": "Local Edge Server powered on and running on local clinic LAN.", "check": "edge_server.is_alive == TRUE", "on_fail": "Verify UPS battery power and edge hardware physical switch."},
            {"id": "PRE-WF22-02", "desc": "Sufficient free disk storage on edge server (>= 5.0 GB available).", "check": "disk.free_space_gb >= 5.0", "on_fail": "Trigger urgent disk pruning of archived log files."}
        ],
        "triggers": [
            {"id": "TRIG-WF22-01", "class": "Watchdog Trigger", "event": "Heartbeat probe to cloud gateway times out 3 consecutive times (9 seconds)", "source": "Network Watchdog Daemon", "payload": "{ probe_target: 'api.nammaclinic.bbmp.gov.in', timeouts: 3 }", "latency": "Immediate transition to OFFLINE_MODE"}
        ],
        "inputs": [
            {"name": "local_transaction_payload", "type": "Object", "req": "Mandatory", "source": "Client Application", "val": "Complete transaction bundle conforming to local schema", "priv": "Clinical", "enc": "Encrypted at rest", "ex": "{ action: 'CREATE_ENCOUNTER' }", "on_err": "Rollback local transaction"}
        ],
        "outputs": {
            "success": [
                {"name": "Offline Transaction Receipt", "desc": "Locally committed record with cryptographic monotonic sequence number.", "format": "SQLite WAL Commit", "recipient": "Local Client & Outbound Sync Queue"}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    participant UI as Clinical Client
    participant EDGE as Edge Node Daemon
    participant DB as Local SQLite (WAL)
    participant CLOUD as BBMP Cloud Gateway
    Note over EDGE,CLOUD: Fiber Cable Cut Outside Facility!
    EDGE->>CLOUD: 1. Periodic Heartbeat Ping (Timeout 3.0s)
    CLOUD--xEDGE: 2. Connection Refused / No Route to Host
    EDGE->>EDGE: 3. 3 Missed Pings -> Set State: OFFLINE_AUTONOMOUS
    EDGE->>UI: 4. WebSocket Broadcast: SystemOffline(Amber Banner)
    UI->>UI: 5. Display 'Offline Mode - Operational'
    UI->>EDGE: 6. Submit Patient Encounter (Dr. Manjunath)
    EDGE->>DB: 7. Commit Transaction to Encrypted SQLite (WAL Flush < 8ms)
    DB-->>EDGE: 8. Commit Confirmed (Seq: 4891)
    EDGE-->>UI: 9. Transaction Saved Locally Receipt Token""",
        "activity_diagram": """flowchart TD
    Start([System Operating in Online Mode]) --> SendHeartbeat[Watchdog Sends Cloud Heartbeat Ping Every 3s]
    SendHeartbeat --> HeartbeatResponse{Heartbeat Acknowledged?}
    HeartbeatResponse -- Yes --> ContinueOnline[Maintain Standard Cloud-Synced State]
    ContinueOnline --> SendHeartbeat
    HeartbeatResponse -- No (3x Consecutive) --> TriggerOffline[Trigger Offline Degradation Protocol]
    TriggerOffline --> BroadcastLAN[Broadcast Network Severed Event across Clinic LAN]
    BroadcastLAN --> DisplayAmberBanner[All Workstations Display Amber 'Offline Mode' Indicator]
    DisplayAmberBanner --> SwitchToLocalDB[Route All API Requests to Local Edge Server Daemon]
    SwitchToLocalDB --> AuthenticateOffline[Verify Staff Credentials against Locally Cached Scrypt Hashes]
    AuthenticateOffline --> AcceptClinicalTransactions[Accept Full Clinical Intake, Vitals, Rx, and Dispensing]
    AcceptClinicalTransactions --> WriteWAL[Commit Records to Local Encrypted SQLite with WAL Flush]
    WriteWAL --> AppendSyncQueue[Append Mutation to Monotonic Outbound Sync Queue]
    AppendSyncQueue --> CheckDiskQuota{Local Disk Storage Space >= 2GB?}
    CheckDiskQuota -- No / Critical --> PruneOldTelemetry[Prune Old Telemetry Spans & Retain Clinical DB]
    CheckDiskQuota -- Yes --> MonitorLink[Watchdog Continues Probing Cloud Gateway in Background]
    PruneOldTelemetry --> MonitorLink
    MonitorLink --> CheckRestored{WAN Connectivity Restored?}
    CheckRestored -- No --> AcceptClinicalTransactions
    CheckRestored -- Yes (30s Stable) --> TriggerSync[Trigger Reconnection & Sync Engine WF-023]
    TriggerSync --> End([Offline Execution Concluded & Sync Active])""",
        "state_diagram": """stateDiagram-v2
    [*] --> ONLINE_SYNCHRONIZED
    ONLINE_SYNCHRONIZED --> OFFLINE_DEGRADED: 3 Missed Cloud Heartbeats
    OFFLINE_DEGRADED --> OFFLINE_DEGRADED: Transactions Written Locally to WAL
    OFFLINE_DEGRADED --> RECONNECTING: Cloud Heartbeat Restored
    RECONNECTING --> ONLINE_SYNCHRONIZED: Full Sync Queue Flushed WF-023
    RECONNECTING --> OFFLINE_DEGRADED: Connection Flapped / Unstable"""
    }

    # =========================================================================
    # WF-023: Sync Conflict & Replay Workflow
    # =========================================================================
    m23 = WORKFLOW_MAP["WF-023"]
    specs["WF-023"] = {
        "id": "WF-023", "num": "23", "name": m23["name"], "domain": m23["domain"],
        "exec_summary": {
            "purpose": "Governs the deterministic, asynchronous replication, batch delta transmission, vector clock ordering, and conflict arbitration of queued offline mutations upon connectivity restoration between Namma Clinic edge nodes and the BBMP Central Health Cloud. Enforces clinical safety priority rules (clinician explicit clinical actions strictly supersede automated timestamps), isolates unresolvable conflicts into dead-letter review queues, and generates cryptographic reconciliation receipts.",
            "rationale": "Following prolonged offline execution (e.g., 8-24 hours), hundreds of clinical encounters, inventory decrements, and patient profile updates must be merged with central servers where concurrent modifications may have occurred. Flawed conflict resolution can overwrite vital clinical diagnoses or duplicate inventory decrements.",
            "clinical_impact": "Guarantees that patient medical histories are never overwritten or lost during distributed synchronization; preserves every clinical note authored by doctors; and flags any concurrent clinical modifications for human clinical review.",
            "system_impact": "Executes monotonic FIFO queue flushing with SHA-256 idempotency deduplication; enforces transactional 3-way merge algorithms; and emits audit reconciliation reports.",
            "risk_profile": "Network flapping causing partial batch uploads; concurrent edits to the same patient demographic profile; clock skew between edge and cloud servers; and dead-letter queue overflow."
        },
        "objectives": [
            {"id": "OBJ-WF23-01", "title": "Zero Data Loss Reconciliation", "desc": "Reconcile 100% of offline mutations without dropping a single committed transaction.", "metric": "Reconciliation Loss Rate = 0.00%", "verification": "Cryptographic record count parity verification"},
            {"id": "OBJ-WF23-02", "title": "High-Throughput Replay", "desc": "Replay and reconcile offline transaction batches at >= 500 records per minute over standard broadband.", "metric": "Replay Throughput >= 500 records/min", "verification": "Replay performance telemetry benchmarks"},
            {"id": "OBJ-WF23-03", "title": "Deterministic Conflict Resolution", "desc": "Resolve >= 98% of distributed data conflicts automatically using deterministic clinical priority rules.", "metric": "Automated Resolution Rate >= 98%", "verification": "Conflict resolution engine execution logs"},
            {"id": "OBJ-WF23-04", "title": "Dead-Letter Isolation Latency", "desc": "Isolate unresolvable multi-actor conflicts into Dead-Letter Review Queue within 2.0 seconds of detection.", "metric": "DLQ Isolation Latency < 2.0s", "verification": "Dead-letter queue insertion test assertions"}
        ],
        "in_scope": [
            {"area": "Delta Batch Packaging", "desc": "Grouping queued offline SQLite mutations into compressed, encrypted 100-record chunks."},
            {"area": "Monotonic Sequencing", "desc": "Enforcing strict FIFO replay order using vector clocks and edge-generated sequence counters."},
            {"area": "Conflict Arbitration Rules", "desc": "Three-way merge logic: Clinical Diagnosis (Doctor wins), Demographics (Latest wins), Inventory (Atomic additive sum)."},
            {"area": "Dead-Letter Management", "desc": "Visual supervisory console for manual review and approval of conflicting mutations."}
        ],
        "out_of_scope": [
            {"area": "Arbitrary Schema Migration Merging", "desc": "Merging across different major database schema versions during active sync; requires pre-planned software update.", "handoff": "DevOps Migration Pipeline"},
            {"area": "Manual Raw SQL Patching", "desc": "Direct database modification by clinic staff; strictly forbidden.", "handoff": "None - Strictly Prohibited"}
        ],
        "actors": [
            {"id": "ACT-WF23-01", "type": "System", "name": "Cloud Sync Coordinator", "responsibilities": "Receives delta batches, verifies idempotency keys, runs merge algorithms, applies mutations to cloud PostgreSQL.", "permissions": "Replication Master, Conflict Arbiter, DLQ Router", "failure_duty": "Rejects malformed delta batches and requests edge re-transmission.", "inputs": "Encrypted delta chunks, edge signature tokens", "decisions": "Determines whether record can be merged cleanly or requires DLQ isolation.", "outputs": "Reconciliation receipts, DLQ work items", "recovery": "Rolls back partial batch commit upon database failure."},
            {"id": "ACT-WF23-02", "type": "Human", "name": "Data Reconciliation Specialist / Medical Officer", "responsibilities": "Reviews Dead-Letter Queue items, compares conflicting values, selects authoritative truth, approves merge.", "permissions": "DLQ Read, Conflict Resolve, Manual Merge Authorize", "failure_duty": "Escalates unresolved identity conflicts to Zonal Health Officer.", "inputs": "Conflicting field diffs, audit timestamps, operator notes", "decisions": "Determines authoritative data value for ambiguous clinical conflicts.", "outputs": "Manually resolved database transaction", "recovery": "Re-opens conflicting records if citizen clarifies discrepancy."}
        ],
        "personas": [
            {"id": "PERSONA-006", "name": "Kavitha Reddy", "role": "Systems Data Administrator", "env": "Central BBMP health IT command center.", "goals": "Ensure morning sync from 150 clinics finishes smoothly by 11:00 AM without locking cloud databases.", "pain_points": "Huge data sync waves crashing central cloud APIs; unhandled conflict deadlocks.", "adaptations": "Staggered jitter queue flushing with rate-limiting and automatic clinical priority merge rules."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-006", "title": "Data Administrator", "read": "Sync Queues, DLQ Items", "create": "Sync Job", "update": "DLQ Resolution", "delete": "None", "override": "Force Replay", "signoff": "Reconciliation Signoff"},
            {"role": "ROLE-002", "title": "Medical Officer", "read": "Clinical DLQ Items", "create": "Clinical Truth Assertion", "update": "Clinical Record", "delete": "None", "override": "Clinical Merge Authority", "signoff": "Clinical Conflict Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF23-01", "desc": "WAN broadband connectivity stable for at least 30 continuous seconds.", "check": "wan.stability_duration_sec >= 30", "on_fail": "Remain in offline autonomous mode until link stabilizes."},
            {"id": "PRE-WF23-02", "desc": "Cloud gateway mutual TLS (mTLS) certificate validated and session handshake complete.", "check": "mtls_session.is_established == TRUE", "on_fail": "Retry mTLS handshake with exponential backoff."}
        ],
        "triggers": [
            {"id": "TRIG-WF23-01", "class": "Network Event", "event": "Network watchdog detects connectivity restoration to Central Cloud", "source": "Network Watchdog Daemon", "payload": "{ event: 'CONNECTIVITY_RESTORED', link_type: 'BROADBAND' }", "latency": "< 1.0s to initiate sync"}
        ],
        "inputs": [
            {"name": "delta_batch_id", "type": "UUID", "req": "Mandatory", "source": "Edge Sync Queue", "val": "Unique batch identifier", "priv": "Operational", "enc": "Plaintext", "ex": "b1c2d3e4-...", "on_err": "Reject corrupted batch"}
        ],
        "outputs": {
            "success": [
                {"name": "Reconciliation Receipt Token", "desc": "Cryptographic confirmation from central cloud certifying successful batch merge.", "format": "Signed JSON Receipt", "recipient": "Edge Node Ledger"},
                {"name": "Dead-Letter Work Item", "desc": "Dispatched to administrator portal if conflicting mutations cannot be resolved automatically.", "format": "JSON DLQ Item", "recipient": "Admin DLQ Console"}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    participant EDGE as Edge Node Daemon
    participant QUEUE as Offline SQLite Queue
    participant SYNC as Cloud Sync Coordinator
    participant CLOUD_DB as Central PostgreSQL DB
    Note over EDGE,SYNC: Broadband Restored!
    EDGE->>SYNC: 1. Handshake: Link Stable (mTLS Handshake OK)
    EDGE->>QUEUE: 2. Read Next FIFO Delta Batch (Items 100-200)
    EDGE->>SYNC: 3. Post Encrypted Chunk (Batch ID: B-488)
    SYNC->>CLOUD_DB: 4. Check Idempotency Keys & Run Merge Logic
    SYNC->>CLOUD_DB: 5. 99 Items Merged Cleanly, 1 Conflict Detected
    SYNC->>SYNC: 6. Route Conflict to Dead-Letter Queue (DLQ)
    SYNC->>CLOUD_DB: 7. Commit 99 Transactions to PostgreSQL
    SYNC-->>EDGE: 8. Return Receipt: 99 Merged, 1 in DLQ
    EDGE->>QUEUE: 9. Purge Merged Items from Offline Queue""",
        "activity_diagram": """flowchart TD
    Start([Network Watchdog Confirms WAN Restored for 30s]) --> EstablishMTLS[Establish Mutual TLS Session with Central Cloud]
    EstablishMTLS --> QueryPendingQueue[Query Local SQLite Queue for Unreconciled Batches]
    QueryPendingQueue --> HasPendingBatches{Are Pending Batches in Queue?}
    HasPendingBatches -- No --> SetAllSynced[Set Status: FULLY_SYNCHRONIZED & Transition to Online Mode]
    SetAllSynced --> End([Sync Concluded])
    HasPendingBatches -- Yes --> ReadNextBatch[Read Next FIFO Chunk of 100 Transactions]
    ReadNextBatch --> TransmitChunk[Transmit Compressed Chunk to Cloud Sync Coordinator]
    TransmitChunk --> CloudReceive[Cloud Coordinator Receives Batch & Evaluates Idempotency]
    CloudReceive --> CheckConflict{Does Mutation Conflict with Cloud State?}
    CheckConflict -- No Conflict --> MergeDirectly[Apply Mutation Cleanly to Central PostgreSQL]
    CheckConflict -- Conflict Detected --> EvaluateRule{Evaluate Deterministic Conflict Rule}
    EvaluateRule -- Clinical Data --> ClinicianWins[Clinical Priority: Doctor Explicit Note Overrides Timestamp]
    EvaluateRule -- Inventory Decrement --> AdditiveMerge[Additive Sum: Adjust Cloud Stock by Local Delta]
    EvaluateRule -- Ambiguous Conflict --> RouteDLQ[Route Record to Dead-Letter Queue DLQ for Human Review]
    ClinicianWins --> MergeDirectly
    AdditiveMerge --> MergeDirectly
    MergeDirectly --> EmitCloudReceipt[Emit Cryptographic Batch Reconciliation Receipt to Edge]
    RouteDLQ --> EmitCloudReceipt
    EmitCloudReceipt --> PurgeLocalBatch[Edge Purges Reconciled Records from Local SQLite Queue]
    PurgeLocalBatch --> QueryPendingQueue""",
        "state_diagram": """stateDiagram-v2
    [*] --> LINK_RESTORED
    LINK_RESTORED --> BATCH_TRANSMITTING: Delta Chunks Uploading
    BATCH_TRANSMITTING --> BATCH_MERGED: Clean Merge in Cloud
    BATCH_TRANSMITTING --> CONFLICT_IDENTIFIED: Concurrent Edit Detected
    CONFLICT_IDENTIFIED --> AUTO_RESOLVED: Clinical Priority Rule Applied
    CONFLICT_IDENTIFIED --> DLQ_QUARANTINED: Ambiguous Conflict to DLQ
    AUTO_RESOLVED --> BATCH_MERGED
    DLQ_QUARANTINED --> DLQ_MANUAL_REVIEW: Admin / Doctor Resolves
    DLQ_MANUAL_REVIEW --> BATCH_MERGED: Approved Truth Committed
    BATCH_MERGED --> SYNC_COMPLETE: All Local Records Purged
    SYNC_COMPLETE --> [*]"""
    }

    # =========================================================================
    # WF-024: ABDM Integration Workflow
    # =========================================================================
    m24 = WORKFLOW_MAP["WF-024"]
    specs["WF-024"] = {
        "id": "WF-024", "num": "24", "name": m24["name"], "domain": m24["domain"],
        "exec_summary": {
            "purpose": "Specifies deep, full-lifecycle integration with the Ayushman Bharat Digital Mission (ABDM) national health digital public infrastructure in Namma Clinic. Implements Milestone 1 (M1: ABHA creation, Aadhaar OTP/biometric verification, QR Scan & Share), Milestone 2 (M2: Health Information Provider / HIP push of FHIR R4 bundles for OPD Consultation, Prescription, and Diagnostic Report), and Milestone 3 (M3: Health Information User / HIU consent-based pulling of citizen historical health records via the national Consent Manager gateway).",
            "rationale": "ABDM is the mandatory digital health highway of India. Seamless integration ensures that citizens attending municipal Namma Clinics have unbroken longitudinal health records accessible across all government and private hospitals across the country.",
            "clinical_impact": "Enables Namma Clinic physicians to review previous hospital discharge summaries, cardiac evaluations, and surgical reports authored in distant tertiary institutions; eliminates duplicate expensive diagnostic testing.",
            "system_impact": "Acts as the platform's national gateway adapter; maps internal database entities into strictly validated FHIR R4 Indian National Core profiles (NRCES); manages cryptographic consent artifacts; and signs ABDM callbacks.",
            "risk_profile": "ABDM national gateway API outages; UIDAI Aadhaar biometric timeouts; citizen distrust of national digital health IDs; and schema validation rejection of FHIR bundles."
        },
        "objectives": [
            {"id": "OBJ-WF24-01", "title": "Sub-10s ABHA Verification", "desc": "Complete citizen ABHA verification and demographic linking within 10 seconds of QR scan or OTP submission.", "metric": "ABHA Verification Latency < 10.0s", "verification": "ABDM M1 gateway response telemetry"},
            {"id": "OBJ-WF24-02", "title": "100% FHIR R4 Schema Compliance", "desc": "Validate 100% of outbound clinical bundles against NRCES Indian FHIR Core specifications prior to transmission.", "metric": "FHIR Schema Validation Pass Rate = 100%", "verification": "FHIR JSON schema validator assertion suite"},
            {"id": "OBJ-WF24-03", "title": "Reliable M2 Encounter Linking", "desc": "Link and push 100% of signed clinical encounters to the ABDM Health Information Provider (HIP) registry within 24 hours.", "metric": "M2 Record Push Success Rate >= 99%", "verification": "HIP transaction acknowledgment logs"},
            {"id": "OBJ-WF24-04", "title": "Consent-Governed M3 Data Exchange", "desc": "Strictly enforce ABDM Consent Manager digital consent artifacts before requesting or exposing longitudinal health records.", "metric": "Unconsented M3 Data Transfers = 0", "verification": "ABDM consent manager audit log inspection"}
        ],
        "in_scope": [
            {"area": "ABDM Milestone 1 (M1)", "desc": "ABHA Number & ABHA Address creation via Aadhaar/Mobile, QR Scan-and-Share token exchange, and demographic linking."},
            {"area": "ABDM Milestone 2 (M2)", "desc": "HIP role: Generating FHIR R4 DiagnosticReport, MedicationRequest, and OPD Consultation bundles; publishing care contexts."},
            {"area": "ABDM Milestone 3 (M3)", "desc": "HIU role: Raising consent requests via Consent Manager, receiving decrypted health information bundles, rendering external records."},
            {"area": "Cryptographic Key Management", "desc": "Managing ABDM client credentials, RSA public/private keypairs, and AES-GCM data transfer encryption."}
        ],
        "out_of_scope": [
            {"area": "Direct UIDAI Aadhaar Demographic Alteration", "desc": "Modifying citizen official Aadhaar name or birthdate; handled by Aadhaar Seva Kendra.", "handoff": "UIDAI Official Centers"},
            {"area": "Commercial Health Insurance Claims Clearing", "desc": "Processing commercial health claims through National Health Claims Exchange (NHCX); out of scope for day-clinic OPD.", "handoff": "NHCX Portal"}
        ],
        "actors": [
            {"id": "ACT-WF24-01", "type": "System", "name": "ABDM Gateway Connector", "responsibilities": "Manages mTLS tokens, formats FHIR R4 bundles, communicates with NHA gateway, processes webhooks.", "permissions": "ABDM API Master, FHIR Packager, Encryption Enclave", "failure_duty": "Queues outbound transactions in local cryptographic cache during national gateway downtime.", "inputs": "Clinic clinical events, citizen ABHA tokens, ABDM callbacks", "decisions": "Validates FHIR conformance; manages token renewal cycles.", "outputs": "FHIR bundles, ABDM transaction receipts", "recovery": "Refreshes OAuth session token upon 401 Unauthorized."},
            {"id": "ACT-WF24-02", "type": "Human", "name": "Citizen / Patient", "responsibilities": "Scans clinic QR code via ABHA App (Arogya Setu / ABHA SBX), approves consent requests on mobile phone.", "permissions": "ABHA Share, Consent Grant/Deny/Revoke", "failure_duty": "Declares lack of smartphone; requests registration nurse assistance.", "inputs": "Clinic QR posters, mobile consent notification prompts", "decisions": "Grants or denies access to historical medical records.", "outputs": "Authorized ABDM consent artifact", "recovery": "Re-submits OTP if mobile session times out."}
        ],
        "personas": [
            {"id": "PERSONA-008", "name": "Ramesh Kumar", "role": "Citizen with ABHA App", "env": "Clinic reception entrance.", "goals": "Scan the clinic QR code on his phone and skip the long physical registration queue.", "pain_points": "Long paper forms asking for the same address details he already verified in his government ID.", "adaptations": "Prominent 'Scan & Share with ABHA' poster at entrance that instantly prints his queue token."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "ABHA Verification Status", "create": "ABHA Scan Request", "update": "Link Demographics", "delete": "None", "override": "None", "signoff": "Demographic Verification Signoff"},
            {"role": "ROLE-002", "title": "Medical Officer", "read": "External ABDM Records", "create": "M3 Consent Request", "update": "Clinical Notes", "delete": "None", "override": "None", "signoff": "Encounter Push Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF24-01", "desc": "Clinic registered as authorized Health Facility (HFR) with valid HFR-ID on NHA portal.", "check": "facility.hfr_status == 'REGISTERED'", "on_fail": "Halt ABDM operations; facility credentials unverified."},
            {"id": "PRE-WF24-02", "desc": "NHA ABDM Gateway client credentials (client_id and client_secret) active and unexpired.", "check": "abdm_auth.token_valid == TRUE", "on_fail": "Execute automated OAuth client credential token refresh."}
        ],
        "triggers": [
            {"id": "TRIG-WF24-01", "class": "Citizen Trigger", "event": "Citizen scans clinic reception 'Scan & Share' QR code via ABHA mobile application", "source": "ABDM Mobile Gateway Webhook", "payload": "{ abha_number: '91-1234-5678-9012', token_no: '8841' }", "latency": "< 2.0s to push demographic profile to desk"}
        ],
        "inputs": [
            {"name": "abha_id", "type": "String(32)", "req": "Mandatory", "source": "Citizen / ABDM", "val": "ABHA Number regex ^\\d{2}-\\d{4}-\\d{4}-\\d{4}$ or ABHA Address", "priv": "Restricted", "enc": "Encrypted at rest", "ex": "91-8841-2049-1102", "on_err": "Reject invalid ABHA format"}
        ],
        "outputs": {
            "success": [
                {"name": "Linked ABDM Health Record", "desc": "FHIR R4 composition bundle registered with ABDM central care context registry.", "format": "FHIR R4 Bundle JSON-LD", "recipient": "NHA ABDM Gateway & Citizen ABHA Locker"}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor C as Citizen (ABHA App)
    participant QR as Clinic Scan & Share Poster
    participant NHA as NHA ABDM Gateway
    participant EMR as Namma Clinic EMR
    actor D as Medical Officer
    C->>QR: 1. Scan Clinic QR Code via ABHA App
    C->>NHA: 2. Authorize Profile Share with Clinic W085
    NHA->>EMR: 3. Push Webhook: Citizen Demographic Payload
    EMR-->>C: 4. Instant Token SNR-001 Issued & Queue Entry Confirmed
    Note over EMR,D: Doctor Completes Consultation
    D->>EMR: 5. Sign Encounter & Prescription (WF-011 / WF-012)
    EMR->>EMR: 6. Transform to FHIR R4 Bundle (NRCES Core)
    EMR->>NHA: 7. M2 Push: Publish Care Context & Notify Citizen Locker
    NHA-->>C: 8. Notification on Mobile: 'Namma Clinic Record Added'""",
        "activity_diagram": """flowchart TD
    Start([Citizen Arrives or Encounter Concluded]) --> CheckMilestone{Evaluate ABDM Operation Phase}
    CheckMilestone -- M1: Scan & Share --> CitizenScansQR[Citizen Scans Reception QR via ABHA Mobile App]
    CitizenScansQR --> NHAPushesProfile[NHA Gateway Pushes Demographic JSON to Clinic Desk]
    NHAPushesProfile --> AutoCreateProfile[Auto-Populate Patient Profile & Mint Clinic Token]
    AutoCreateProfile --> EndM1([M1 Registration Completed])
    CheckMilestone -- M2: HIP Health Record Push --> DoctorSigns[Doctor Signs Clinical Encounter / Rx in EMR]
    DoctorSigns --> BuildFHIRBundle[Transform Clinical Record into NRCES FHIR R4 Bundle]
    BuildFHIRBundle --> ValidateFHIR{Passes FHIR Schema Validation?}
    ValidateFHIR -- No --> LogSchemaError[Log Schema Discrepancy & Quarantine Bundle]
    ValidateFHIR -- Yes --> PushCareContext[Push Care Context & FHIR Bundle to ABDM Gateway]
    PushCareContext --> NHAAccepts[NHA Acknowledges Receipt & Links to Citizen ABHA]
    NHAAccepts --> EndM2([M2 Record Published to Citizen Locker])
    CheckMilestone -- M3: HIU External Record Fetch --> DoctorRequests[Doctor Requests Past Records via Consent Manager]
    DoctorRequests --> SendConsentPrompt[Send Digital Consent Request to Citizen Mobile Phone]
    SendConsentPrompt --> CitizenConsents{Citizen Approves on Phone?}
    CitizenConsents -- No / Denied --> ShowConsentDenied[Notify Doctor: Consent Refused]
    CitizenConsents -- Yes --> FetchEncryptedData[Pull Encrypted FHIR Bundles from Remote Hospitals]
    FetchEncryptedData --> DecryptInEnclave[Decrypt In Local Enclave & Display Past History to Doctor]
    DecryptInEnclave --> EndM3([M3 External Records Reviewed])""",
        "state_diagram": """stateDiagram-v2
    [*] --> ABDM_INITIATED
    ABDM_INITIATED --> ABHA_VERIFIED: M1 Token Scanned / Verified
    ABHA_VERIFIED --> CARE_CONTEXT_LINKED: Patient Linked to Clinic Facility
    CARE_CONTEXT_LINKED --> FHIR_BUNDLE_COMPOSED: Encounter Signed
    FHIR_BUNDLE_COMPOSED --> HIP_PUBLISHED: M2 Bundle Accepted by NHA
    CARE_CONTEXT_LINKED --> HIU_CONSENT_REQUESTED: M3 Records Requested
    HIU_CONSENT_REQUESTED --> HIU_RECORDS_PULLED: Citizen Approved on Mobile
    HIP_PUBLISHED --> [*]
    HIU_RECORDS_PULLED --> [*]"""
    }

    # =========================================================================
    # WF-025: Emergency Exception Workflow
    # =========================================================================
    m25 = WORKFLOW_MAP["WF-025"]
    specs["WF-025"] = {
        "id": "WF-025", "num": "25", "name": m25["name"], "domain": m25["domain"],
        "exec_summary": {
            "purpose": "Governs the master clinical emergency exception protocols, trauma team mobilization, statutory deemed consent execution, fast-track authentication bypass, emergency crash cart medication authorization, verbal order logging, and 108 inter-facility transfer coordination for acute life-threatening emergencies occurring in Namma Clinic.",
            "rationale": "Medical emergencies (anaphylaxis, sudden cardiac arrest, postpartum hemorrhage, acute pediatric convulsions, multi-casualty trauma) require instant life-saving actions within seconds. Rigid software authentication gates, mandatory demographic data entry, or billing prerequisites during an active resuscitation violate medical ethics and cause preventable deaths. WF-025 provides an unhindered clinical fast-track while preserving forensic accountability through retrospective reconciliation.",
            "clinical_impact": "Guarantees zero software roadblocks during emergency resuscitation; enables immediate delivery of oxygen, IV fluids, adrenaline, and defibrillation; and ensures seamless emergency transfer to tertiary intensive care units.",
            "system_impact": "Acts as the platform's ultimate break-glass state machine; preempts all active client screens across the clinic mesh; unlocks emergency medication trays without prior electronic orders; and generates high-priority audit logs.",
            "risk_profile": "Abuse of break-glass emergency mode for routine consultations; incomplete retrospective documentation; missing physical crash cart drugs; and legal disputes over implied consent."
        },
        "objectives": [
            {"id": "OBJ-WF25-01", "title": "Zero-Latency Emergency Initiation", "desc": "Initiate emergency resuscitation session and display emergency dashboard within 1.0 second of emergency trigger.", "metric": "Emergency Initiation Latency < 1.0s", "verification": "Break-glass button execution telemetry"},
            {"id": "OBJ-WF25-02", "title": "All-Station Queue Preemption", "desc": "Preempt and freeze all routine queues, redirecting medical staff to the emergency crash area within 10 seconds.", "metric": "Staff Alert & Preemption Latency < 10s", "verification": "Simulated multi-station emergency alert broadcast"},
            {"id": "OBJ-WF25-03", "title": "Statutory Implied Consent Compliance", "desc": "Generate legally valid deemed consent record under DPDP Act Sec 7(a) for 100% of unconscious emergency patients.", "metric": "Statutory Deemed Consent Compliance = 100%", "verification": "Emergency legal compliance audit"},
            {"id": "OBJ-WF25-04", "title": "2-Hour Retrospective Reconciliation", "desc": "Complete retrospective clinical notes, verbal order ratification, and crash cart drug reconciliation within 2 hours.", "metric": "Retrospective Reconciliation Adherence = 100%", "verification": "Post-emergency reconciliation timestamp analysis"}
        ],
        "in_scope": [
            {"area": "Break-Glass Mode Activation", "desc": "One-touch bypass of standard registration, demographic capture, and routine authentication gates."},
            {"area": "Provisional UHID Minting", "desc": "Immediate generation of temporary emergency patient identifier (`EMG-YYYYMMDD-XXXX`) for unidentified individuals."},
            {"area": "Verbal Order Audio Logging", "desc": "Rapid digital audio recording or quick-tap entry of doctor emergency verbal orders (e.g., '1mg IV Adrenaline now')."},
            {"area": "Retrospective Reconciliation Protocol", "desc": "Formal post-resuscitation clinical documentation workflow for doctor and nurse signatures."}
        ],
        "out_of_scope": [
            {"area": "Definitive Intensive Care Ventilation", "desc": "Prolonged invasive ICU ventilation; clinic provides bag-valve-mask manual ventilation until 108 ambulance arrives.", "handoff": "Bowring / Victoria Hospital ICU"},
            {"area": "Forensic Medicolegal Autopsies", "desc": "Post-mortem forensic examinations in the event of unsuccessful resuscitation.", "handoff": "Department of Forensic Medicine, Victoria Hospital"}
        ],
        "actors": [
            {"id": "ACT-WF25-01", "type": "Human", "name": "Medical Officer (Resuscitation Lead)", "responsibilities": "Leads ABCDE resuscitation, delivers defibrillation/medications, authorizes verbal orders, signs SBAR transfer.", "permissions": "Emergency Master, Break-Glass Trigger, Verbal Order Issue, Retrospective Sign", "failure_duty": "Performs continuous chest compressions if nurse is establishing intravenous line.", "inputs": "Physical clinical collapse, monitor vital alarms, emergency drugs", "decisions": "Determines resuscitation termination or transfer decision; chooses medications.", "outputs": "Stabilized citizen or SBAR ambulance transfer bundle", "recovery": "Completes retrospective documentation within 2 hours post-event."},
            {"id": "ACT-WF25-02", "type": "Human", "name": "Staff Nurse (Emergency Assistant)", "responsibilities": "Hits Code Red button, manages airway/oxygen, establishes IV access, draws emergency crash cart drugs.", "permissions": "Code Red Trigger, Crash Cart Unlock, BLS Delivery", "failure_duty": "Summons secondary clinic staff to assist with crowd control and CPR rotation.", "inputs": "Doctor verbal orders, patient vital parameters", "decisions": "Selects appropriate size bag-valve-mask and IV cannula.", "outputs": "Administered emergency drugs, recorded time-stamps", "recovery": "Restocks emergency crash cart immediately post-resuscitation."}
        ],
        "personas": [
            {"id": "PERSONA-002", "name": "Dr. Manjunath Swamy", "role": "Senior Medical Officer", "env": "Managing an unconscious 45-year-old road accident victim brought by bystanders.", "goals": "Start resuscitation immediately without the software demanding the patient's Aadhaar or phone number.", "pain_points": "Software refusing to proceed without mandatory demographic fields during an emergency.", "adaptations": "1-click 'UNKNOWN EMERGENCY PATIENT' that generates a provisional chart in 500ms with zero form filling."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-002", "title": "Medical Officer", "read": "Emergency Protocol, All EMR", "create": "Emergency Session, Verbal Order", "update": "Retrospective Record", "delete": "None", "override": "Break-Glass Master Override", "signoff": "Emergency Clinical Signoff"},
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "Emergency Protocols", "create": "Code Red Trigger", "update": "Emergency Vitals", "delete": "None", "override": "Queue Preemption Override", "signoff": "Emergency Medication Administration Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF25-01", "desc": "Emergency resuscitation equipment (Defibrillator, Oxygen, Ambu Bag, Suction) verified functional at morning check.", "check": "resuscitation_kit.status == 'READY'", "on_fail": "Immediate verbal alarm; fetch backup emergency kit from adjacent station."},
            {"id": "PRE-WF25-02", "desc": "Emergency crash cart sealed with unbroken verification tag.", "check": "crash_cart.seal_intact == TRUE", "on_fail": "Break emergency seal immediately; audit contents retrospectively."}
        ],
        "triggers": [
            {"id": "TRIG-WF25-01", "class": "Emergency Trigger", "event": "Staff nurse or doctor taps physical or software 'BREAK-GLASS EMERGENCY' button", "source": "Any Workstation Terminal", "payload": "{ location: 'TRIAGE_STATION', trigger: 'CARDIAC_ARREST' }", "latency": "< 500ms to open emergency workspace"}
        ],
        "inputs": [
            {"name": "emergency_category", "type": "Enum(CARDIAC_ARREST, ANAPHYLAXIS, SEVERE_TRAUMA, MATERNAL_HEMORRHAGE, PEDIATRIC_COLLAPSE)", "req": "Mandatory", "source": "Clinician Tap", "val": "Defined emergency category", "priv": "Clinical", "enc": "Plaintext", "ex": "CARDIAC_ARREST", "on_err": "Default to CARDIAC_ARREST"}
        ],
        "outputs": {
            "success": [
                {"name": "Emergency Resuscitation Record", "desc": "Complete timeline of all administered shocks, drugs, oxygen rates, and clinical timestamps.", "format": "Immutable Emergency FHIR Bundle", "recipient": "Patient EMR & Receiving Tertiary Hospital"},
                {"name": "SBAR Transfer Document", "desc": "Standardized inter-facility handoff bundle printed and pushed to 108 ambulance.", "format": "Signed PDF & FHIR Document", "recipient": "108 Paramedic & District Hospital ER"}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor N as Staff Nurse
    participant UI as Any Clinic Terminal
    actor D as Medical Officer
    participant WS as Clinic Mesh Hub
    actor AMB as 108 Ambulance
    N->>UI: 1. Click 'BREAK-GLASS EMERGENCY' (Unconscious Male, Pulseless)
    UI->>WS: 2. Broadcast High-Priority BreakGlassEvent
    par Multi-Station Preemption
        WS->>D: 3. Siren in Doctor Chamber + Flash Red Screen
        WS->>UI: 4. Open Instant Emergency Resuscitation Workspace
    end
    D->>N: 5. Arrives at Crash Station within 10 seconds
    D->>UI: 6. Tap: 'Defibrillation Shock 200J Delivered'
    D->>UI: 7. Tap: 'Adrenaline 1mg IV Administered'
    D->>UI: 8. Tap: '108 Ambulance Summoned'
    AMB->>D: 9. Paramedic arrives; takes SBAR handover slip
    D->>UI: 10. Post-Event: Complete Retrospective Clinical Notes (2h SLA)""",
        "activity_diagram": """flowchart TD
    Start([Citizen Collapses or Brought Unconscious]) --> TapBreakGlass[Nurse or Doctor Taps 'BREAK-GLASS EMERGENCY']
    TapBreakGlass --> SystemBypass[System Bypasses Registration, Consent, and Login Gates]
    SystemBypass --> MintProvisionalID[Mint Instant Provisional ID: EMG-YYYYMMDD-XXXX]
    SystemBypass --> PreemptClinicScreens[Preempt All Workstation Screens with Audible Siren]
    MintProvisionalID --> OpenEmergencyDashboard[Display Real-Time Resuscitation Action Dashboard]
    OpenEmergencyDashboard --> ABCDEIntervention[Execute ABCDE Protocol: Airway, Breathing, Circulation]
    ABCDEIntervention --> QuickTapOrders[Nurse / Doctor Quick-Taps Administered Drugs: Adrenaline, Atropine, O2]
    QuickTapOrders --> EvaluateResponse{Patient Regains Pulse / Breathing?}
    EvaluateResponse -- Yes --> StabilizeInClinic[Transfer to Observation Bed; Monitor Vitals Every 5 min]
    EvaluateResponse -- No / Critical --> Dispatch108[Dispatch 108 Ambulance & Print Standardized SBAR Slip]
    Dispatch108 --> HandoverParamedic[Handover Patient & SBAR to 108 Paramedic Crew]
    HandoverParamedic --> RetrospectiveReconciliation[Mandatory 2-Hour Retrospective Clinical Documentation]
    StabilizeInClinic --> RetrospectiveReconciliation
    RetrospectiveReconciliation --> DoctorNurseSign[Doctor and Nurse Digitally Ratify All Verbal Orders]
    DoctorNurseSign --> RestockCart[Pharmacy Restocks Emergency Crash Cart & Reseals]
    RestockCart --> End([Emergency Protocol Concluded & Normal OPD Restored])""",
        "state_diagram": """stateDiagram-v2
    [*] --> EMERGENCY_TRIGGERED
    EMERGENCY_TRIGGERED --> RESUSCITATION_ACTIVE: Gates Bypassed & Team Assembled
    RESUSCITATION_ACTIVE --> PATIENT_STABILIZED: Return of Spontaneous Circulation
    RESUSCITATION_ACTIVE --> AMBULANCE_TRANSFERRED: Handed over to 108 Crew
    PATIENT_STABILIZED --> RETROSPECTIVE_RECONCILIATION: Clinical Signoff Underway
    AMBULANCE_TRANSFERRED --> RETROSPECTIVE_RECONCILIATION: Clinical Signoff Underway
    RETROSPECTIVE_RECONCILIATION --> CRASH_CART_RESTOCKED: Inventory Audited
    CRASH_CART_RESTOCKED --> EMERGENCY_CLOSED: Normal Baseline Restored
    EMERGENCY_CLOSED --> [*]"""
    }

    return specs

def write_group5_file():
    specs = get_group5_specs()
    print("Building Group 5 Workflows (WF-021 to WF-025)...")

    header = '''#!/usr/bin/env python3
"""
data_wf21_to_25.py
Clean, self-contained domain specifications for Workflows 21 to 25:
  - WF-021: Clinical Analytics, Syndromic Surveillance & Population Health Reporting Workflow
  - WF-022: Autonomous Offline Edge Operation, Local Storage & Network Resilience Workflow
  - WF-023: Bidirectional Synchronization, Conflict Resolution & Merkle Ledger Workflow
  - WF-024: Ayushman Bharat Digital Mission (ABDM) Gateway & FHIR Interoperability Workflow
  - WF-025: Clinical Emergency Exception, Fast-Track Bypass & Resuscitation Protocol Workflow

Exports:
  DATA_WF21_TO_25 (dict mapping 'WF-021'..'WF-025' to enriched 67-section workflow dicts)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_factory import build_workflow_object
from build_group5 import get_group5_specs

def get_group5_workflows():
    specs = get_group5_specs()
    return {wfid: build_workflow_object(spec) for wfid, spec in specs.items()}

if __name__ == "__main__":
    from workflow_generator import render_workflow_document
    from common import count_lines, find_duplicate_paragraphs
    print("Testing data_wf21_to_25.py...")
    wfs = get_group5_workflows()
    docs = {}
    for wfid, wf_data in wfs.items():
        doc = render_workflow_document(wf_data)
        docs[wfid] = doc
        counts = count_lines(doc)
        status = "PASS" if counts["substantive"] >= 2000 else "FAIL"
        print(f"  {wfid}: Total = {counts['total']}, Substantive = {counts['substantive']} [{status}]")

    dups = find_duplicate_paragraphs(docs, min_len=60)
    print(f"  Duplicate paragraphs within Group 5: {len(dups)}")
'''
    with open('scripts/workflows/data_wf21_to_25.py', 'w', encoding='utf-8') as f:
        f.write(header)
    print("Wrote scripts/workflows/data_wf21_to_25.py")

if __name__ == "__main__":
    write_group5_file()
