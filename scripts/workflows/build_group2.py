#!/usr/bin/env python3
"""
build_group2.py
Generates data_wf06_to_10.py covering:
  WF-006: Informed Clinical & Digital Health Consent Workflow
  WF-007: Token Issuance, Priority Tagging & Queue Entry Workflow
  WF-008: Dynamic Multi-Room Queue Orchestration & Display Workflow
  WF-009: Nursing Triage, Vital Signs & Clinical Acuity Assessment Workflow
  WF-010: Danger Sign Detection, Critical Value Alert & Emergency Escalation Workflow
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_factory import build_workflow_object
from workflow_metadata import WORKFLOW_MAP

def get_group2_specs():
    specs = {}

    # =========================================================================
    # WF-006: Consent Workflow
    # =========================================================================
    m6 = WORKFLOW_MAP["WF-006"]
    specs["WF-006"] = {
        "id": "WF-006", "num": "06", "name": m6["name"], "domain": m6["domain"],
        "exec_summary": {
            "purpose": "Governs the capture, verification, cryptographic signing, enforcement, and revocation of digital and physical informed consent across all care stages in Namma Clinic. Strictly enforces DPDP Act 2023 principles, purpose limitation, bilingual notice presentation (Kannada/English), pediatric legal guardian proxy consent, ABDM Consent Manager (HIP/HIU) artifact exchange, and emergency medical bypass protocols.",
            "rationale": "Patient autonomy and privacy are statutory mandates under the DPDP Act 2023 and ABDM Data Governance standards. Consent must be freely given, specific, informed, unconditional, and unambiguous with a clear affirmative action, while never obstructing emergency resuscitation.",
            "clinical_impact": "Protects patients from unauthorized medical procedures and data exposure while establishing a verifiable audit trail for invasive point-of-care rapid testing, teleconsultation data sharing, and secondary epidemiological research.",
            "system_impact": "Acts as the platform's policy enforcement point (PEP) for clinical data disclosure; binds cryptographic consent receipts to patient records, and orchestrates consent artifact validation with ABDM gateway.",
            "risk_profile": "Consent fatigue leading to blind acceptance; language barrier misunderstandings in illiterate citizens; legal guardian verification challenges for minors; and unauthorized data leakage post-revocation."
        },
        "objectives": [
            {"id": "OBJ-WF06-01", "title": "Bilingual DPDP Consent Presentation", "desc": "Present unambiguous, purpose-specific consent notices in clear Kannada and English with visual iconography prior to data capture.", "metric": "Notice Presentation Compliance = 100%", "verification": "Client-side consent presentation audit logs"},
            {"id": "OBJ-WF06-02", "title": "Cryptographic Consent Artifact Minting", "desc": "Generate SHA-256 tamper-evident digital consent receipts within 1.5 seconds of affirmative citizen authorization.", "metric": "Consent Signing Latency p95 < 1.5s", "verification": "Cryptographic ledger timestamp validation"},
            {"id": "OBJ-WF06-03", "title": "Emergency Medical Bypass Enforcement", "desc": "Enable immediate clinical treatment of unconscious, unattended trauma patients under statutory emergency exception with dual-clinician sign-off.", "metric": "Emergency Bypass Latency < 10 sec", "verification": "Emergency exception audit log inspection"},
            {"id": "OBJ-WF06-04", "title": "Instant Consent Revocation Propagation", "desc": "Propagate citizen consent revocation to all local caches and ABDM health information units within 5 minutes.", "metric": "Revocation Propagation Latency < 300s", "verification": "Revocation event broadcast verification test suite"}
        ],
        "in_scope": [
            {"area": "Clinical Care Consent", "desc": "General outpatient assessment, physical examination, and basic medical care consent."},
            {"area": "Diagnostic Testing Consent", "desc": "Specific consent for capillary blood collection, rapid HIV/HBsAg testing, and pregnancy screening."},
            {"area": "Digital Health Data Sharing", "desc": "ABDM longitudinal health record linking and electronic health information exchange."},
            {"area": "Pediatric Proxy Consent", "desc": "Parental/guardian authorization capture for minors under 18 years of age."},
            {"area": "Emergency Medical Exception", "desc": "Statutory deemed consent protocol for life-threatening emergencies."}
        ],
        "out_of_scope": [
            {"area": "Major Surgical Consent", "desc": "General anesthesia and operating theater major operative consent.", "handoff": "Referral District Hospital surgical unit"},
            {"area": "Clinical Drug Trial Consent", "desc": "Experimental biomedical research protocol consent.", "handoff": "Tertiary Medical College Ethics Committee"}
        ],
        "actors": [
            {"id": "ACT-WF06-01", "type": "Human", "name": "Citizen / Patient / Guardian", "responsibilities": "Reviews bilingual consent notice, selects granular data sharing options, provides physical signature or OTP.", "permissions": "Consent Grant, Selective Scope Adjustment, Consent Revoke", "failure_duty": "Declares inability to read; requests verbal Kannada explanation.", "inputs": "Verbal explanation, digital tablet prompt, SMS OTP", "decisions": "Determines whether to grant full, partial, or zero external data sharing.", "outputs": "Signed digital consent artifact or physical paper signature", "recovery": "Modifies consent preferences via kiosk or reception."},
            {"id": "ACT-WF06-02", "type": "Human", "name": "Staff Nurse / Registration Clerk", "responsibilities": "Explains notice in vernacular Kannada, assists illiterate citizens, witnesses physical signature marks.", "permissions": "Consent Witness, Paper Consent Scan Upload", "failure_duty": "Flags refusal of mandatory treatment consent to Medical Officer.", "inputs": "Citizen responses, thumb impressions, signed slips", "decisions": "Verifies legal guardian relationship for pediatric patients.", "outputs": "Witnessed consent verification record", "recovery": "Re-initiates consent interview if citizen misunderstood."},
            {"id": "ACT-WF06-03", "type": "Human", "name": "Medical Officer", "responsibilities": "Explains clinical procedure risks, executes emergency clinical bypass sign-off.", "permissions": "Emergency Consent Bypass Authorize, Clinical Audit", "failure_duty": "Documents clinical rationale for emergency bypass within 2 hours.", "inputs": "Patient consciousness state, acute triage severity", "decisions": "Determines whether patient lacks capacity and requires emergency treatment bypass.", "outputs": "Signed emergency medical bypass authorization", "recovery": "Obtains retrospective citizen consent upon recovery of consciousness."}
        ],
        "personas": [
            {"id": "PERSONA-007", "name": "Shantamma", "role": "Senior Citizen Patient", "env": "Noisy reception area; illiterate in English, understands spoken Kannada.", "goals": "Understand what healthcare information will be shared with the government.", "pain_points": "Intimidated by complex legal text on digital screens.", "adaptations": "High-contrast Kannada audio prompt and icon-driven consent choices."},
            {"id": "PERSONA-001", "name": "Sister Bhavani Gowda", "role": "Staff Nurse", "env": "High-pressure registration and triage station.", "goals": "Quickly obtain valid consent without holding up the morning patient queue.", "pain_points": "Lengthy multi-step terms and conditions slowing intake.", "adaptations": "One-touch default primary care consent with optional advanced ABDM toggles."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "Patient Consent Status", "create": "Consent Witness Record", "update": "Consent Preferences", "delete": "None", "override": "None", "signoff": "Witness Signoff"},
            {"role": "ROLE-002", "title": "Medical Officer", "read": "All Consent Artifacts", "create": "Emergency Bypass", "update": "Clinical Scope", "delete": "None", "override": "Emergency Consent Bypass", "signoff": "Emergency Treatment Order"},
            {"role": "ROLE-008", "title": "Citizen / Patient", "read": "Own Consent Artifacts", "create": "Consent Grant", "update": "Modify Preferences", "delete": "Revoke Consent", "override": "None", "signoff": "Digital Signature / OTP"}
        ],
        "preconditions": [
            {"id": "PRE-WF06-01", "desc": "Citizen identity verified or provisional emergency UHID minted.", "check": "patient.id != NULL", "on_fail": "Trigger Patient Registration WF-003 first."},
            {"id": "PRE-WF06-02", "desc": "Consent policy templates (DPDP v1.0, ABDM v2.1) loaded into edge cache.", "check": "policy_engine.templates_loaded == TRUE", "on_fail": "Fall back to static local bilingual markdown templates."}
        ],
        "triggers": [
            {"id": "TRIG-WF06-01", "class": "User Trigger", "event": "Citizen registration or return visit intake requires consent verification", "source": "Registration UI", "payload": "{ patient_id, care_context: 'OPD_ENCOUNTER' }", "latency": "< 100ms to render notice"},
            {"id": "TRIG-WF06-02", "class": "Emergency Trigger", "event": "Unconscious trauma patient brought to triage requiring immediate resuscitation", "source": "Triage Nurse Alert", "payload": "{ patient_id, acuity: 'RED', mental_status: 'UNCONSCIOUS' }", "latency": "Immediate emergency bypass modal"}
        ],
        "inputs": [
            {"name": "consent_type", "type": "Enum(TREATMENT, ABDM_SHARE, LAB_TEST)", "req": "Mandatory", "source": "System Context", "val": "Must be valid defined category", "priv": "Operational", "enc": "Plaintext", "ex": "TREATMENT", "on_err": "Default to TREATMENT"},
            {"name": "grant_status", "type": "Enum(GRANTED, DENIED, REVOKED, EMERGENCY_BYPASS)", "req": "Mandatory", "source": "Citizen / MO", "val": "Valid state", "priv": "Operational", "enc": "Plaintext", "ex": "GRANTED", "on_err": "Reject invalid status"},
            {"name": "auth_method", "type": "Enum(DIGITAL_SIGNATURE, AADHAAR_OTP, PHYSICAL_MARK, EMERGENCY_CLINICIAN)", "req": "Mandatory", "source": "Intake Station", "val": "Defined method", "priv": "Operational", "enc": "Plaintext", "ex": "DIGITAL_SIGNATURE", "on_err": "Prompt clerk for verification method"},
            {"name": "guardian_id", "type": "UUID", "req": "Conditional", "source": "Guardian Registry", "val": "Required if patient age < 18", "priv": "Restricted", "enc": "Encrypted", "ex": "a1b2c3d4-...", "on_err": "Prompt for guardian identity"}
        ],
        "outputs": {
            "success": [
                {"name": "Signed Consent Artifact", "desc": "Cryptographically hashed JSON-LD consent record with timestamp and actor claims.", "format": "JSON-LD / PDF Receipt", "recipient": "Patient Medical Record & Audit Ledger"},
                {"name": "Consent Verification Token", "desc": "Short-lived JWT asserting granted consent scopes for downstream station routing.", "format": "JWT Bearer Token", "recipient": "Station Flow Engine"}
            ],
            "failure": [
                {"name": "Consent Denial Record", "desc": "Audit entry recording citizen refusal of data sharing or clinical assessment.", "action": "Restrict EHR sharing; provide standard paper emergency care if life-threatening."},
                {"name": "Guardian Verification Failure", "desc": "Alert indicating unverified adult attempting to consent for pediatric citizen.", "action": "Escalate to Medical Officer for social welfare verification."}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor P as Patient / Guardian
    actor N as Staff Nurse
    participant UI as Kiosk / Tablet UI
    participant CS as Consent Service
    participant DB as Local Database
    participant ABDM as ABDM Gateway
    P->>N: 1. Citizen arrives for care
    N->>UI: 2. Open Consent Capture (Bilingual)
    UI-->>P: 3. Display Kannada/English Purpose Notice
    P->>UI: 4. Tap 'Accept Primary Care & Local EHR'
    UI->>CS: 5. Submit Consent Grant Payload
    CS->>DB: 6. Insert Signed Consent Record (SHA-256)
    CS->>ABDM: 7. Async Register Consent Artefact (if ABDM linked)
    CS-->>UI: 8. Emit Consent Token & Proceed to Triage""",
        "activity_diagram": """flowchart TD
    Start([Patient Intake Initiated]) --> CheckEmergency{Is Patient Unconscious / Critical?}
    CheckEmergency -- Yes --> ExecBypass[Doctor Signs Emergency Medical Bypass]
    ExecBypass --> LogBypass[Log Implied Consent Audit Event]
    LogBypass --> ProceedCare([Proceed Directly to Resuscitation])
    CheckEmergency -- No --> CheckAge{Is Patient Age < 18?}
    CheckAge -- Yes --> VerifyGuardian[Verify Legal Guardian Identity]
    VerifyGuardian --> ShowNotice[Display Bilingual Kannada/English Notice]
    CheckAge -- No --> ShowNotice
    ShowNotice --> CitizenDecision{Citizen Decision}
    CitizenDecision -- Grants Consent --> CaptureSig[Capture Digital Signature / OTP]
    CaptureSig --> SignArtifact[Sign & Hash Consent Artifact]
    SignArtifact --> ProceedCare
    CitizenDecision -- Refuses ABDM Share --> LocalOnly[Enable Local Only OPD Care]
    LocalOnly --> SignArtifact
    CitizenDecision -- Refuses Treatment --> CounselDoctor[Doctor Clinical Counseling]
    CounselDoctor --> DocumentRefusal[Document Informed Refusal & Discharge]""",
        "state_diagram": """stateDiagram-v2
    [*] --> CONSENT_PENDING
    CONSENT_PENDING --> CONSENT_PRESENTED: Notice Displayed to Citizen
    CONSENT_PRESENTED --> CONSENT_GRANTED: Citizen Signs / Authorizes
    CONSENT_PRESENTED --> CONSENT_DENIED: Citizen Refuses Care
    CONSENT_PENDING --> EMERGENCY_BYPASS: Doctor Authorizes Life-Saving Care
    CONSENT_GRANTED --> CONSENT_REVOKED: Citizen Withdraws Consent
    CONSENT_GRANTED --> [*]: Care Episode Concluded
    EMERGENCY_BYPASS --> RETROSPECTIVE_RATIFICATION: Patient Recovers & Authorizes
    RETROSPECTIVE_RATIFICATION --> [*]
    CONSENT_DENIED --> [*]
    CONSENT_REVOKED --> [*]"""
    }

    # =========================================================================
    # WF-007: Token Generation Workflow
    # =========================================================================
    m7 = WORKFLOW_MAP["WF-007"]
    specs["WF-007"] = {
        "id": "WF-007", "num": "07", "name": m7["name"], "domain": m7["domain"],
        "exec_summary": {
            "purpose": "Governs the deterministic minting, priority tagging, physical thermal printing, SMS notification, and queue registration of patient tokens at Namma Clinic intake. Categorizes citizens into clinical priority tiers (Emergency Red, Antenatal Care, Senior Citizen 65+, Pediatric <5, and General OPD), calculates dynamic waiting times, and guarantees collision-free numbering during WAN network partitions.",
            "rationale": "High-density morning arrival surges (80-150 citizens between 08:00 and 10:30) require instant, orderly, and socially equitable queue entry. Deterministic offline token minting ensures zero clinic downtime when BBMP central servers are unreachable.",
            "clinical_impact": "Prevents catastrophic triage delays by immediately recognizing emergency acuity tags (EMG-XXX) and routing vulnerable populations (pregnant mothers, frail elderly, feverish infants) ahead of routine consultations.",
            "system_impact": "Initializes the active daily patient flow pipeline; synchronizes physical slip generation with edge database state, and broadcasts queue updates to waiting area digital displays.",
            "risk_profile": "Thermal printer hardware jams; paper depletion; duplicate token collision during multi-terminal offline operation; and token scalping or jumping."
        },
        "objectives": [
            {"id": "OBJ-WF07-01", "title": "Rapid Token Generation", "desc": "Mint and print physical thermal token slip within 2.0 seconds of intake button press.", "metric": "Token Generation Latency p95 < 2.0s", "verification": "Kiosk print spooler transaction telemetry"},
            {"id": "OBJ-WF07-02", "title": "Zero Token Number Collision", "desc": "Guarantee mathematically collision-free token sequences across multiple intake desks even during 72-hour offline operation.", "metric": "Collision Rate = 0.00%", "verification": "Sequence uniqueness verification script"},
            {"id": "OBJ-WF07-03", "title": "Equitable Priority Categorization", "desc": "Automatically classify 100% of eligible seniors, antenatal mothers, and infants into priority queue streams.", "metric": "Priority Classification Accuracy = 100%", "verification": "Patient demographic vs token tag audit cross-check"},
            {"id": "OBJ-WF07-04", "title": "Dynamic Wait Time Estimation", "desc": "Provide realistic estimated waiting time (+/- 5 minutes accuracy) printed on token slip and sent via SMS.", "metric": "Wait Time Mean Absolute Error <= 5 min", "verification": "Encounter transit time comparison analysis"}
        ],
        "in_scope": [
            {"area": "Category Prefixing", "desc": "EMG (Emergency), ANC (Antenatal), SNR (Senior Citizen), PED (Pediatric), GEN (General)."},
            {"area": "Physical Thermal Printing", "desc": "ESC/POS 58mm/80mm bilingual Kannada/English token slip printing with scannable QR code."},
            {"area": "Virtual SMS Notification", "desc": "Dispatch of automated SMS alert with token number and live queue tracking link."},
            {"area": "Offline Autonomous Sequence", "desc": "Deterministic node-prefixed sequence counter persisting in local SQLite with WAL mode."}
        ],
        "out_of_scope": [
            {"area": "Commercial Token Monetization", "desc": "VIP or paid fast-track queues; strictly prohibited in public primary health centers."},
            {"area": "Tertiary Hospital Appointment Booking", "desc": "Specialist hospital slot reservation; handled by Referral WF-016."}
        ],
        "actors": [
            {"id": "ACT-WF07-01", "type": "Human", "name": "Registration Clerk / Staff Nurse", "responsibilities": "Selects priority category, enters demographic identifier, confirms ticket printing.", "permissions": "Token Mint, Priority Override, Token Cancel", "failure_duty": "Switches to backup manual token book upon printer mechanical failure.", "inputs": "Citizen presence, ID card, apparent clinical distress", "decisions": "Determines whether citizen requires Emergency or Priority tag.", "outputs": "Dispensed physical token ticket", "recovery": "Reprints token if physical slip is torn or jammed."},
            {"id": "ACT-WF07-02", "type": "Human", "name": "Citizen / Patient", "responsibilities": "Takes printed token, waits in designated waiting area, watches digital display.", "permissions": "View Own Token Status", "failure_duty": "Reports lost token ticket to registration clerk.", "inputs": "Verbal declaration, SMS notification", "decisions": "Chooses to wait in clinic or monitor remotely via SMS link.", "outputs": "Presents token slip at triage station", "recovery": "Requests verification via mobile number if slip lost."}
        ],
        "personas": [
            {"id": "PERSONA-008", "name": "Ramesh Kumar", "role": "Working Parent with Toddler", "env": "Crowded waiting hall with crying child.", "goals": "Know exactly when his child will be seen without standing in lines.", "pain_points": "Ambiguous queue positions and unannounced delays.", "adaptations": "Clear Kannada SMS updates and prominent pediatric priority tag."},
            {"id": "PERSONA-007", "name": "Shantamma", "role": "Senior Citizen", "env": "Difficulty standing for long periods.", "goals": "Receive senior citizen priority token without confusion.", "pain_points": "Being pushed back by aggressive younger crowds.", "adaptations": "High-contrast bold font on token slip with 'SNR' prefix and audio callout."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "Queue Stream, Token Metrics", "create": "Token, Priority Tag", "update": "Token Status", "delete": "Cancel Token", "override": "Emergency Tag Override", "signoff": "Intake Batch"},
            {"role": "ROLE-006", "title": "Registration Attendant", "read": "Token Registry", "create": "Standard Token", "update": "Reprint", "delete": "None", "override": "None", "signoff": "None"}
        ],
        "preconditions": [
            {"id": "PRE-WF07-01", "desc": "Active daily clinic operational session initialized (WF-001).", "check": "clinic_session.status == 'ACTIVE'", "on_fail": "Display 'Clinic Session Not Opened'."},
            {"id": "PRE-WF07-02", "desc": "Thermal printer online with paper roll loaded or virtual mode enabled.", "check": "printer.status == 'READY' || system.virtual_token_allowed == TRUE", "on_fail": "Raise printer jam warning and switch to virtual SMS tokens."}
        ],
        "triggers": [
            {"id": "TRIG-WF07-01", "class": "User Trigger", "event": "Registration clerk clicks 'Issue Token' after demographic lookup", "source": "Registration UI", "payload": "{ patient_id, category: 'SNR', desk_id: 'DESK-01' }", "latency": "< 100ms to dispatch print job"},
            {"id": "TRIG-WF07-02", "class": "Kiosk Trigger", "event": "Citizen scans ABHA QR code at self-service intake kiosk", "source": "Self-Service Kiosk", "payload": "{ abha_token, category: 'GEN' }", "latency": "< 1.5s to print slip"}
        ],
        "inputs": [
            {"name": "patient_id", "type": "UUID", "req": "Mandatory", "source": "Registration Record", "val": "Valid patient UUID", "priv": "Restricted", "enc": "Plaintext internal", "ex": "e5f6g7h8-...", "on_err": "Block token issuance"},
            {"name": "category", "type": "Enum(EMG, ANC, SNR, PED, GEN)", "req": "Mandatory", "source": "Clerk / Demographics", "val": "Valid category", "priv": "Operational", "enc": "Plaintext", "ex": "SNR", "on_err": "Default to GEN"},
            {"name": "desk_id", "type": "String(16)", "req": "Mandatory", "source": "Terminal Config", "val": "Desk identifier", "priv": "Operational", "enc": "Plaintext", "ex": "DESK-01", "on_err": "Default to DESK-01"}
        ],
        "outputs": {
            "success": [
                {"name": "Physical Printed Token Ticket", "desc": "Thermal print slip with token number, date, QR code, priority tag, and estimated wait.", "format": "58mm ESC/POS Slip", "recipient": "Patient / Citizen"},
                {"name": "Queue Entry Event", "desc": "WebSocket message emitted to local clinic message broker to update queue displays.", "format": "JSON WebSocket Frame", "recipient": "Signage Display Engine & Triage Workstation"}
            ],
            "failure": [
                {"name": "Printer Fault Alert", "desc": "Hardware sensor indicates paper empty or thermal head overheat.", "action": "Prompt clerk to load roll; route token to virtual SMS queue."}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor C as Citizen
    actor K as Registration Clerk
    participant UI as Registration App
    participant TE as Token Engine
    participant DB as SQLite DB
    participant PR as Thermal Printer
    participant WS as WebSocket Broker
    C->>K: 1. Request token (Age 71, Senior)
    K->>UI: 2. Click 'Issue Senior Token'
    UI->>TE: 3. Mint Token Request (SNR)
    TE->>DB: 4. Atomic Increment & Insert Token SNR-014
    TE->>PR: 5. Send ESC/POS Print Command (Bilingual)
    PR-->>C: 6. Dispense Thermal Paper Slip
    TE->>WS: 7. Broadcast TokenMinted Event
    WS-->>UI: 8. Refresh Queue Dashboard""",
        "activity_diagram": """flowchart TD
    Start([Citizen Arrives at Intake]) --> CheckPriority{Evaluate Priority Criteria}
    CheckPriority -- Red / Acute Distress --> TagEMG[Tag EMG - Emergency Priority]
    CheckPriority -- Pregnant Mother --> TagANC[Tag ANC - Antenatal Priority]
    CheckPriority -- Age >= 65 --> TagSNR[Tag SNR - Senior Citizen Priority]
    CheckPriority -- Age < 5 --> TagPED[Tag PED - Pediatric Priority]
    CheckPriority -- Routine Adult --> TagGEN[Tag GEN - General Priority]
    TagEMG --> GenSeq[Generate Atomic Sequence Number]
    TagANC --> GenSeq
    TagSNR --> GenSeq
    TagPED --> GenSeq
    TagGEN --> GenSeq
    GenSeq --> CheckPrinter{Thermal Printer Ready?}
    CheckPrinter -- Yes --> PrintSlip[Print Bilingual ESC/POS Thermal Slip]
    CheckPrinter -- No / Paper Out --> SendSMS[Send Virtual Token via SMS / WhatsApp]
    PrintSlip --> EmitWS[Broadcast Queue Event via Local WebSockets]
    SendSMS --> EmitWS
    EmitWS --> End([Citizen Directed to Waiting Area])""",
        "state_diagram": """stateDiagram-v2
    [*] --> TOKEN_REQUESTED
    TOKEN_REQUESTED --> SEQUENCE_ALLOCATED: Atomic Sequence Claimed
    SEQUENCE_ALLOCATED --> PRINTING: ESC/POS Spooled
    PRINTING --> ACTIVE_IN_QUEUE: Physical Slip Dispensed
    PRINTING --> VIRTUAL_ACTIVE: Printer Failed - Virtual SMS Dispatched
    ACTIVE_IN_QUEUE --> CALLED_TO_STATION: Station Staff Calls Token
    VIRTUAL_ACTIVE --> CALLED_TO_STATION: Station Staff Calls Token
    ACTIVE_IN_QUEUE --> CANCELLED: Patient Leaves / Cancelled
    CALLED_TO_STATION --> [*]
    CANCELLED --> [*]"""
    }

    # =========================================================================
    # WF-008: Queue Orchestration Workflow
    # =========================================================================
    m8 = WORKFLOW_MAP["WF-008"]
    specs["WF-008"] = {
        "id": "WF-008", "num": "08", "name": m8["name"], "domain": m8["domain"],
        "exec_summary": {
            "purpose": "Governs real-time, multi-station patient routing, room load balancing, digital signage display broadcasting, bilingual audio chime announcements, hold/no-show exception transitions, and station-to-station clinical handovers across Triage, Consultation Rooms 1 & 2, Laboratory, and Pharmacy Dispensing windows in Namma Clinic.",
            "rationale": "Uncontrolled crowd movement and shouting patient names causes severe anxiety, privacy violations, and physical congestion in compact 1,000 sq ft urban clinics. Automated digital queue orchestration ensures fair, dignified, and clinically safe progression through the facility.",
            "clinical_impact": "Enforces strict clinical routing invariants: no patient can jump directly from registration to pharmacy without validated consultation; emergency tokens automatically preempt routine consultations; and infectious tuberculosis/fever suspects are routed to isolated consultation rooms.",
            "system_impact": "Acts as the event-driven backbone of the clinic edge LAN, utilizing local WebSocket pub/sub brokers, low-latency display daemons, and Web Audio API synthesized Kannada/English announcements.",
            "risk_profile": "Network disconnect between server and display TVs; audio amplifier failure; patient missing their call due to noise; and clinician Cherry-picking easier cases."
        },
        "objectives": [
            {"id": "OBJ-WF08-01", "title": "Sub-Second Signage Latency", "desc": "Update all digital signage displays within 500 milliseconds of clinician clicking 'Call Next Patient'.", "metric": "Display Update Latency p95 < 500ms", "verification": "WebSocket round-trip message timestamp telemetry"},
            {"id": "OBJ-WF08-02", "title": "Bilingual Audio Announcement Clarity", "desc": "Trigger clear, studio-grade synthesized Kannada and English audio chimes announcing token and destination room.", "metric": "Audio Chime Success Rate = 100%", "verification": "Audio engine completion event logs"},
            {"id": "OBJ-WF08-03", "title": "Multi-Room Load Balancing", "desc": "Distribute general OPD patients evenly between active doctor consultation rooms with < 15% caseload variance.", "metric": "Clinician Caseload Variance < 15%", "verification": "Shift-end consultation count distribution analysis"},
            {"id": "OBJ-WF08-04", "title": "Deterministic No-Show Management", "desc": "Automatically place non-responsive tokens on 10-minute hold before final cancellation, permitting single-click recall.", "metric": "Hold / Recall Compliance = 100%", "verification": "Queue state transition audit log inspection"}
        ],
        "in_scope": [
            {"area": "Multi-Station Routing", "desc": "Registration -> Triage -> Doctor Consultation -> Lab -> Pharmacy -> Exit."},
            {"area": "Digital Display Signage", "desc": "Full-screen Chromium kiosk display showing Active Calling, Next in Line, and Room Numbers."},
            {"area": "Audio Chime Synthesis", "desc": "Two-tone attention chime followed by 'Token SNR-001, Room 1' in Kannada then English."},
            {"area": "Station Handover Management", "desc": "Automated re-enqueuing of patient to Pharmacy queue upon doctor prescription sign-off."}
        ],
        "out_of_scope": [
            {"area": "Inter-Facility Ambulance Queue", "desc": "108 ambulance dispatch queueing; managed by Emergency WF-025."},
            {"area": "Mobile Geofenced Virtual Queue", "desc": "Offsite GPS queue check-in; reserved for Phase 2 mobile app release."}
        ],
        "actors": [
            {"id": "ACT-WF08-01", "type": "Human", "name": "Medical Officer / Clinician", "responsibilities": "Clicks 'Call Next', manages patient consultation status, clicks 'Complete' or 'Hold'.", "permissions": "Call Token, Hold Token, Mark No-Show, Complete Visit", "failure_duty": "Manually calls patient by token number if audio system fails.", "inputs": "Queue list UI, patient arrival in chamber", "decisions": "Determines whether to call next routine patient or recall held patient.", "outputs": "Room occupancy status change, encounter initiation", "recovery": "Clicks 'Recall' if patient arrived late after being held."},
            {"id": "ACT-WF08-02", "type": "Human", "name": "Staff Nurse / Triage Specialist", "responsibilities": "Calls tokens to triage cubicle, checks vitals, transfers token to doctor queue.", "permissions": "Call Triage Token, Complete Triage Transfer", "failure_duty": "Walks to waiting area to escort elderly or frail patients.", "inputs": "Triage queue dashboard", "decisions": "Assigns urgent priority routing if vitals abnormal.", "outputs": "Token routed to doctor consultation queue", "recovery": "Manually re-assigns token to priority lane if patient condition deteriorates."}
        ],
        "personas": [
            {"id": "PERSONA-002", "name": "Dr. Manjunath Swamy", "role": "Senior Medical Officer", "env": "High-volume consultation chamber.", "goals": "One-click calling of next patient without manual searching or delays.", "pain_points": "Patients wandering into the wrong room; empty chairs while patients wait outside.", "adaptations": "Prominent hotkey (Spacebar / F2) to call next patient instantly."},
            {"id": "PERSONA-007", "name": "Shantamma", "role": "Senior Citizen", "env": "Waiting area with hearing difficulties in background chatter.", "goals": "Easily recognize when her turn has arrived.", "pain_points": "Missing verbal doctor calls; confusing English-only numbers.", "adaptations": "High-contrast flashing red-to-green token display and loud Kannada voice prompt."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-002", "title": "Medical Officer", "read": "Consultation Queue", "create": "Encounter", "update": "Queue State (Call/Hold/Done)", "delete": "None", "override": "Emergency Call Next", "signoff": "Encounter Transfer"},
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "Triage & General Queue", "create": "Triage Transfer", "update": "Triage Queue State", "delete": "None", "override": "Triage Priority Jump", "signoff": "Triage Complete"},
            {"role": "ROLE-003", "title": "Pharmacist", "read": "Pharmacy Queue", "create": "Dispense Event", "update": "Pharmacy Queue State", "delete": "None", "override": "None", "signoff": "Dispense Complete"}
        ],
        "preconditions": [
            {"id": "PRE-WF08-01", "desc": "Local WebSocket broker daemon running on clinic edge server.", "check": "ws_broker.status == 'ONLINE'", "on_fail": "Fall back to HTTP server-sent events or short-polling."},
            {"id": "PRE-WF08-02", "desc": "At least one clinical station (Triage, Doctor, Pharmacy) actively staffed.", "check": "COUNT(active_stations) >= 1", "on_fail": "Display 'Stations Not Ready' on waiting room TV."}
        ],
        "triggers": [
            {"id": "TRIG-WF08-01", "class": "Clinician Trigger", "event": "Doctor clicks 'Call Next' button or hits F2 keyboard hotkey", "source": "Consultation Chamber UI", "payload": "{ room_id: 'ROOM-01', doctor_id: 'DOC-002' }", "latency": "< 200ms to dispatch call"},
            {"id": "TRIG-WF08-02", "class": "Timeout Trigger", "event": "Token in CALLED state exceeds 3 minutes without clinician start", "source": "Queue Monitor Daemon", "payload": "{ token_id: 'SNR-001', elapsed_sec: 180 }", "latency": "Prompts clinician with 'Patient Arrived?' or 'Mark Hold' modal"}
        ],
        "inputs": [
            {"name": "station_id", "type": "String(16)", "req": "Mandatory", "source": "Workstation Client", "val": "Valid station identifier", "priv": "Operational", "enc": "Plaintext", "ex": "ROOM-01", "on_err": "Reject call action"},
            {"name": "action_type", "type": "Enum(CALL, HOLD, RECALL, COMPLETE, TRANSFER)", "req": "Mandatory", "source": "Clinician Action", "val": "Defined transition", "priv": "Operational", "enc": "Plaintext", "ex": "CALL", "on_err": "Ignore invalid action"}
        ],
        "outputs": {
            "success": [
                {"name": "Signage Display Update", "desc": "WebSocket payload rendering token number, destination room, and arrow on TV.", "format": "JSON WebSocket Payload", "recipient": "Waiting Area Smart TVs & Monitors"},
                {"name": "Bilingual Audio Chime", "desc": "Synthesized audio alert played over waiting area public address speaker.", "format": "Audio Stream (MP3 / Web Audio)", "recipient": "Clinic PA Amplifier"}
            ],
            "failure": [
                {"name": "No Patient in Queue Alert", "desc": "Notification indicating active queue is empty for requested station.", "action": "Display empty queue status badge to clinician."}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor D as Medical Officer
    participant UI as Doctor Chamber UI
    participant QE as Queue Engine
    participant DB as Local Database
    participant WS as WebSocket Broker
    participant TV as Waiting Area Display
    participant PA as Audio PA System
    D->>UI: 1. Click 'Call Next' (F2 Hotkey)
    UI->>QE: 2. Request Next Patient (Room 1)
    QE->>DB: 3. Fetch Top Priority Token (SNR-001) & Update State to CALLED
    QE->>WS: 4. Publish Event: TokenCalled(SNR-001, Room 1)
    par Visual & Audio Broadcast
        WS->>TV: 5. Flash Green: 'SNR-001 -> Room 1'
        WS->>PA: 6. Play Audio: 'Token SNR-001, Room 1' (Kannada & English)
    end
    UI-->>D: 7. Display Patient Summary Card & Start Timer""",
        "activity_diagram": """flowchart TD
    Start([Clinician Ready for Next Patient]) --> ClickCall[Click 'Call Next' / Press F2]
    ClickCall --> CheckQueue{Active Queue Empty?}
    CheckQueue -- Yes --> ShowEmpty[Display 'Queue Empty - Please Stand By']
    CheckQueue -- No --> SelectToken[Select Highest Priority Oldest Token]
    SelectToken --> UpdateState[Set State: CALLED, Room: Assigned]
    UpdateState --> BroadcastWS[Publish WebSocket Event]
    BroadcastWS --> ScreenFlash[Flash Token Number on Waiting Room TV]
    BroadcastWS --> PlayChime[Play Bilingual Audio Chime on PA System]
    ScreenFlash --> WaitArrival{Patient Enters Room?}
    PlayChime --> WaitArrival
    WaitArrival -- Yes --> StartEncounter[Click 'Start Encounter' -> State: IN_CONSULTATION]
    WaitArrival -- No / 3 Min Elapsed --> PromptHold[Prompt: Hold or Recall?]
    PromptHold -- Mark Hold --> StateHold[Set State: ON_HOLD, Allow Recall within 10 min]
    PromptHold -- Mark No-Show --> StateNoShow[Set State: NO_SHOW, Cancel Token]""",
        "state_diagram": """stateDiagram-v2
    [*] --> ENQUEUED
    ENQUEUED --> CALLED: Clinician Clicks 'Call Next'
    CALLED --> IN_PROGRESS: Patient Enters & Examination Starts
    CALLED --> ON_HOLD: Patient Does Not Respond within 3 min
    ON_HOLD --> CALLED: Clinician Clicks 'Recall'
    ON_HOLD --> NO_SHOW: 10 min Timeout on Hold
    IN_PROGRESS --> TRANSFERRED: Routed to Lab / Pharmacy
    TRANSFERRED --> ENQUEUED: Enqueued in Next Station Queue
    IN_PROGRESS --> COMPLETED: Consultation Finished & Closed
    NO_SHOW --> [*]
    COMPLETED --> [*]"""
    }

    # =========================================================================
    # WF-009: Nursing Triage Workflow
    # =========================================================================
    m9 = WORKFLOW_MAP["WF-009"]
    specs["WF-009"] = {
        "id": "WF-009", "num": "09", "name": m9["name"], "domain": m9["domain"],
        "exec_summary": {
            "purpose": "Governs the systematic physiological assessment, objective vital sign capture, biological plausibility validation, clinical acuity scoring (Modified Early Warning Score - MEWS / Pediatric PEWS), and emergency triaging of all attending citizens in Namma Clinic. Categorizes patients into Green (Standard OPD), Yellow (Urgent Clinical Attention), or Red (Immediate Life-Threatening Resuscitation) acuity tiers before doctor consultation.",
            "rationale": "Undifferentiated patient presentation in primary care carries high risk of missed sepsis, acute hypertensive crises, silent myocardial infarction, and pediatric respiratory collapse. Mandatory objective triage guarantees clinical deterioration is intercepted before catastrophic deterioration occurs in waiting areas.",
            "clinical_impact": "Prevents avoidable outpatient mortality by immediately isolating and prioritizing unstable patients; enforces vital sign recording as a non-negotiable prerequisite for doctor consultation.",
            "system_impact": "Persists structured FHIR Observation vital sign bundles in edge SQLite and central repositories; drives automated clinical alerting via WebSockets to the Medical Officer's screen.",
            "risk_profile": "Measurement error due to incorrect blood pressure cuff size; uncalibrated pulse oximeter probes; nurse data entry typos; and patient refusal of fingerstick glucometry."
        },
        "objectives": [
            {"id": "OBJ-WF09-01", "title": "Comprehensive Vitals Capture", "desc": "Capture complete core vitals (BP, SpO2, Pulse, Respiratory Rate, Temperature) for 100% of non-emergency visits.", "metric": "Core Vitals Capture Rate >= 98%", "verification": "Encounter vital sign completeness telemetry"},
            {"id": "OBJ-WF09-02", "title": "Automated Acuity Scoring", "desc": "Compute validated MEWS and PEWS clinical acuity score within 200ms of entering vital parameters.", "metric": "Scoring Computation Latency < 200ms", "verification": "Algorithm unit test suite and execution benchmarks"},
            {"id": "OBJ-WF09-03", "title": "Biological Plausibility Validation", "desc": "Intercept 100% of physiologically impossible data entry errors (e.g., Pulse 500, SBP 400) via strict boundary guards.", "metric": "Erroneous Vitals Rejection Rate = 100%", "verification": "Boundary validation assertion tests"},
            {"id": "OBJ-WF09-04", "title": "Instant Code Red Escalation", "desc": "Trigger audible alarm and screen preemption in Doctor Chamber within 15 seconds of committing Red acuity vitals.", "metric": "Code Red Alert Latency < 15 sec", "verification": "Simulated red flag end-to-end telemetry timer"}
        ],
        "in_scope": [
            {"area": "Adult Physiological Vitals", "desc": "Systolic/Diastolic BP, Radial Pulse, SpO2, Oral/Axillary Temp, Respiratory Rate, Random Blood Glucose."},
            {"area": "Pediatric Assessment", "desc": "Age-normed pulse, respiratory rate, weight-for-age, mid-upper arm circumference (MUAC), danger signs."},
            {"area": "Acuity Stratification", "desc": "MEWS scoring (0-14 scale): Green (0-2), Yellow (3-4), Red (>= 5 or any single critical danger value)."},
            {"area": "Communicable Disease Isolation", "desc": "Screening for prolonged cough (>2 weeks) and fever to trigger immediate surgical mask provision."}
        ],
        "out_of_scope": [
            {"area": "Continuous Invasive Arterial Line Monitoring", "desc": "ICU-level hemodynamics; strictly out of scope for primary outpatient clinic."},
            {"area": "Advanced 12-Lead ECG Interpretation", "desc": "Automated ECG analysis; clinic restricted to basic telemetry strip transmission to Tele-ICU."}
        ],
        "actors": [
            {"id": "ACT-WF09-01", "type": "Human", "name": "Staff Nurse / ANM", "responsibilities": "Measures physiological parameters, applies digital monitors, enters data, conducts initial inspection.", "permissions": "Triage Vitals Create, Acuity Commit, Code Red Broadcast", "failure_duty": "Initiates manual BLS/CPR immediately upon detecting pulselessness or apnea.", "inputs": "Physical citizen, digital monitor displays, strip glucometer", "decisions": "Determines whether to trigger immediate Code Red escalation.", "outputs": "Committed vital sign bundle, acuity tag", "recovery": "Re-checks manual BP with mercury/aneroid sphygmomanometer on sensor dispute."},
            {"id": "ACT-WF09-02", "type": "Human", "name": "Medical Officer", "responsibilities": "Reviews committed vitals before patient enters chamber; responds to Code Red alarms.", "permissions": "Vitals Review, Clinical Override, Emergency Care", "failure_duty": "Abandons routine consultation immediately to attend triage crash station.", "inputs": "Committed vitals, MEWS score, automated danger alerts", "decisions": "Confirms clinical acuity; decides whether to admit to observation bed or call 108.", "outputs": "Clinical stabilization orders", "recovery": "Authorizes repeat vitals measurement post-stabilization."}
        ],
        "personas": [
            {"id": "PERSONA-001", "name": "Sister Bhavani Gowda", "role": "Senior Staff Nurse", "env": "Busy triage corner; evaluates 70-100 citizens per morning shift.", "goals": "Enter vitals in under 60 seconds with zero keyboard typos.", "pain_points": "Clunky multi-tab software forms requiring mouse clicking between fields.", "adaptations": "Single-screen tab-indexed vitals form with high-contrast numerical keypad touch controls."},
            {"id": "PERSONA-007", "name": "Shantamma", "role": "Elderly Patient with Dizziness", "env": "Feeling faint while waiting in line.", "goals": "Have blood pressure checked quickly without long delays.", "pain_points": "Anxiety causing white-coat hypertension spikes.", "adaptations": "Quiet triage corner with gentle Kannada reassurance before cuff inflation."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "Patient Demographic, Prior Vitals", "create": "Triage Record, Vitals", "update": "Current Visit Vitals", "delete": "None", "override": "Acuity Upgrade (Yellow to Red)", "signoff": "Triage Vitals Signoff"},
            {"role": "ROLE-002", "title": "Medical Officer", "read": "All Vitals, Historical Graphs", "create": "Repeat Vitals Order", "update": "Clinical Interpretation", "delete": "None", "override": "Clinical Acuity Override", "signoff": "Encounter Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF09-01", "desc": "Citizen holds valid active token slip (WF-007).", "check": "token.status in ('ENQUEUED', 'CALLED')", "on_fail": "Direct citizen to registration desk first."},
            {"id": "PRE-WF09-02", "desc": "Diagnostic instruments (digital BP, pulse oximeter, glucometer) calibrated and battery OK.", "check": "equipment_checklist.vitals_ready == TRUE", "on_fail": "Switch to backup manual sphygmomanometer and alert clinic coordinator."}
        ],
        "triggers": [
            {"id": "TRIG-WF09-01", "class": "Queue Trigger", "event": "Nurse calls token to triage station", "source": "Triage Workstation UI", "payload": "{ token_id: 'SNR-001', station: 'TRIAGE-01' }", "latency": "< 100ms to load patient profile"},
            {"id": "TRIG-WF09-02", "class": "Walk-In Emergency", "event": "Citizen collapses in waiting area or arrives in acute respiratory distress", "source": "Nurse Visual Detection", "payload": "{ emergency_type: 'COLLAPSE', immediate_red: true }", "latency": "Instant emergency triage screen bypass"}
        ],
        "inputs": [
            {"name": "systolic_bp", "type": "Integer", "req": "Mandatory", "source": "BP Monitor", "val": "Range: 50 to 260 mmHg", "priv": "Clinical", "enc": "Plaintext", "ex": "128", "on_err": "Flag out of physiological bounds"},
            {"name": "diastolic_bp", "type": "Integer", "req": "Mandatory", "source": "BP Monitor", "val": "Range: 30 to 160 mmHg", "priv": "Clinical", "enc": "Plaintext", "ex": "82", "on_err": "Flag out of bounds; SBP must be > DBP"},
            {"name": "pulse_bpm", "type": "Integer", "req": "Mandatory", "source": "Pulse Oximeter", "val": "Range: 30 to 220 bpm", "priv": "Clinical", "enc": "Plaintext", "ex": "74", "on_err": "Flag pulse anomaly"},
            {"name": "spo2_pct", "type": "Integer", "req": "Mandatory", "source": "Pulse Oximeter", "val": "Range: 50 to 100 %", "priv": "Clinical", "enc": "Plaintext", "ex": "98", "on_err": "Flag hypoxia (< 94% Yellow, < 90% Red)"},
            {"name": "temp_celsius", "type": "Decimal(4,1)", "req": "Mandatory", "source": "Infrared / Digital Thermometer", "val": "Range: 32.0 to 42.5 C", "priv": "Clinical", "enc": "Plaintext", "ex": "37.0", "on_err": "Flag hypothermia / hyperpyrexia"}
        ],
        "outputs": {
            "success": [
                {"name": "Committed Triage Bundle", "desc": "FHIR-compliant Observation bundle with all vitals, MEWS score, and color acuity badge.", "format": "JSON-LD FHIR Observation", "recipient": "Patient EMR & Doctor Consultation Queue"},
                {"name": "Acuity Tag Event", "desc": "WebSocket event pushing patient to doctor chamber queue with Green/Yellow/Red indicator.", "format": "WebSocket JSON Event", "recipient": "Doctor Chamber Dashboard"}
            ],
            "failure": [
                {"name": "Biological Boundary Violation Notice", "desc": "UI error preventing form submission when numbers are physically impossible.", "action": "Highlight erroneous field in red; require re-measurement or nurse confirmation."}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor C as Citizen
    actor N as Staff Nurse
    participant UI as Triage App
    participant MEWS as Acuity Engine
    participant DB as Local Database
    participant WS as WebSocket Broker
    participant DOC as Doctor Chamber UI
    C->>N: 1. Sits at Triage Desk
    N->>UI: 2. Input BP (160/100), SpO2 (93%), Pulse (104), Temp (38.5C)
    UI->>MEWS: 3. Calculate MEWS Score
    MEWS-->>UI: 4. Return MEWS: 4 (Acuity: YELLOW - Urgent)
    N->>UI: 5. Click 'Commit Vitals & Route to Doctor'
    UI->>DB: 6. Store Vitals Record & Link to Encounter
    UI->>WS: 7. Publish PatientTriaged(Token SNR-001, Acuity: YELLOW)
    WS-->>DOC: 8. Insert at top of Doctor Queue (Yellow Badge)""",
        "activity_diagram": """flowchart TD
    Start([Patient Seated at Triage Desk]) --> MeasureBP[Apply Cuff & Measure Blood Pressure]
    MeasureBP --> MeasurePulseSpO2[Attach Pulse Oximeter: Read Pulse & SpO2]
    MeasurePulseSpO2 --> MeasureTemp[Read Temperature with Infrared Thermometer]
    MeasureTemp --> CheckPediatric{Is Patient Child < 5 Years?}
    CheckPediatric -- Yes --> MeasureWeightMUAC[Measure Weight & MUAC Mid-Upper Arm]
    CheckPediatric -- No --> InputVitals[Input Vitals into Triage UI]
    MeasureWeightMUAC --> InputVitals
    InputVitals --> ValidateBounds{Passes Biological Plausibility?}
    ValidateBounds -- No --> HighlightError[Highlight Field Red: Value Impossible]
    HighlightError --> ReMeasure[Nurse Re-measures Parameter]
    ReMeasure --> InputVitals
    ValidateBounds -- Yes --> CalcMEWS[Compute MEWS / PEWS Score]
    CalcMEWS --> EvaluateAcuity{Evaluate Acuity Tier}
    EvaluateAcuity -- Score >= 5 or Danger Flag --> AcuityRed[Acuity RED: Immediate Danger]
    EvaluateAcuity -- Score 3-4 or SBP >= 160 --> AcuityYellow[Acuity YELLOW: Urgent Attention]
    EvaluateAcuity -- Score 0-2 (Normal) --> AcuityGreen[Acuity GREEN: Standard Routine OPD]
    AcuityRed --> TriggerCodeRed[Trigger Code Red Alarm WF-010 & Summon Doctor]
    AcuityYellow --> RouteUrgent[Route to Priority Slot in Doctor Queue]
    AcuityGreen --> RouteStandard[Route to Standard Doctor Queue]
    TriggerCodeRed --> End([Patient Triaged & Handed Over])
    RouteUrgent --> End
    RouteStandard --> End""",
        "state_diagram": """stateDiagram-v2
    [*] --> TRIAGE_PENDING
    TRIAGE_PENDING --> VITALS_MEASURING: Nurse Attaches Sensors
    VITALS_MEASURING --> VALIDATING_BOUNDS: Data Submitted to Client
    VALIDATING_BOUNDS --> VITALS_MEASURING: Boundary Error (Re-measure)
    VALIDATING_BOUNDS --> ACUITY_EVALUATED: MEWS Computed
    ACUITY_EVALUATED --> ROUTED_GREEN: MEWS 0-2 (Standard)
    ACUITY_EVALUATED --> ROUTED_YELLOW: MEWS 3-4 (Urgent)
    ACUITY_EVALUATED --> ESCALATED_RED: MEWS >= 5 (Code Red)
    ROUTED_GREEN --> [*]: Awaiting Doctor Consultation
    ROUTED_YELLOW --> [*]: Fast-Tracked in Doctor Queue
    ESCALATED_RED --> [*]: Immediate Resuscitation WF-010"""
    }

    # =========================================================================
    # WF-010: Danger Alert Workflow
    # =========================================================================
    m10 = WORKFLOW_MAP["WF-010"]
    specs["WF-010"] = {
        "id": "WF-010", "num": "10", "name": m10["name"], "domain": m10["domain"],
        "exec_summary": {
            "purpose": "Governs the automated detection, instantaneous multi-station alerting, clinical queue preemption, emergency resuscitation mobilization, and 108 emergency medical ambulance handover for patients exhibiting life-threatening danger signs, acute physiological collapse, or critical laboratory panic values in Namma Clinic.",
            "rationale": "In primary healthcare settings, delay in recognizing septic shock, acute coronary syndrome, severe anaphylaxis, or pediatric stridor is the leading cause of preventable death. WF-010 eliminates delays by broadcasting non-ignorable alarms across the clinic mesh and preempting all routine queues.",
            "clinical_impact": "Guarantees that any citizen in critical physiological danger receives immediate medical officer attention within 60 seconds; mobilizes oxygen therapy, IV access, and emergency resuscitation medications without bureaucratic delay.",
            "system_impact": "Broadcasts high-priority Code Red WebSocket frames across all clinic devices; turns doctor workstation screens into urgent modal takeovers with audible sirens; and automatically logs emergency clinical audit trails.",
            "risk_profile": "Alarm fatigue from false positives; staff panic; lack of functional oxygen cylinders or emergency drugs in clinic crash cart; and delays in 108 ambulance arrival."
        },
        "objectives": [
            {"id": "OBJ-WF10-01", "title": "Sub-15s Emergency Escalation", "desc": "Broadcast visual and audible Code Red alarm to Doctor Chamber within 15 seconds of danger sign detection.", "metric": "Alert Escalation Latency < 15 sec", "verification": "Telemetry timer from vital sign commit to alert receipt"},
            {"id": "OBJ-WF10-02", "title": "Zero Routine Queue Interference", "desc": "Immediately freeze routine queue calling and force clinician screen to display emergency resuscitation dashboard.", "metric": "Screen Preemption Success Rate = 100%", "verification": "Doctor workstation client UI state verification"},
            {"id": "OBJ-WF10-03", "title": "Rapid Emergency 108 Dispatch Handover", "desc": "Generate standardized digital SBAR (Situation, Background, Assessment, Recommendation) transfer summary within 3 minutes.", "metric": "SBAR Summary Generation Latency < 180s", "verification": "Referral handoff bundle audit timestamp analysis"},
            {"id": "OBJ-WF10-04", "title": "Complete Emergency Audit Trail", "desc": "Capture immutable, tamper-evident log of all administered emergency medications, oxygen flow, and clinician timestamps.", "metric": "Emergency Event Audit Completeness = 100%", "verification": "Emergency encounter ledger inspection"}
        ],
        "in_scope": [
            {"area": "Adult Red Flag Triggers", "desc": "SpO2 < 90% on room air, SBP < 80 or > 220 mmHg, Pulse < 40 or > 140 bpm, GCS < 9, acute chest pain."},
            {"area": "Pediatric Danger Signs", "desc": "Inability to drink/breastfeed, persistent vomiting, convulsions, lethargy, stridor in calm child."},
            {"area": "Maternal Danger Signs", "desc": "Heavy vaginal bleeding, severe headache with visual disturbance (pre-eclampsia), seizure."},
            {"area": "Clinic Resuscitation Mobilization", "desc": "Oxygen concentrator activation, emergency crash cart unlock, IV line placement."},
            {"area": "108 Ambulance Dispatch", "desc": "Telephonic and digital API dispatch of BBMP / GVK EMRI 108 emergency ambulance."}
        ],
        "out_of_scope": [
            {"area": "In-Clinic Surgical Resuscitation", "desc": "Emergency thoracotomy or complex trauma surgery; clinic stabilizes and transfers.", "handoff": "Bowring & Lady Curzon / Victoria Hospital Emergency Dept"},
            {"area": "Intensive Care Mechanical Ventilation", "desc": "Long-term invasive ventilator care; clinic provides bag-valve-mask (Ambu) ventilation during transit."}
        ],
        "actors": [
            {"id": "ACT-WF10-01", "type": "Human", "name": "Staff Nurse", "responsibilities": "Identifies danger sign, presses 'Code Red' panic button, opens airway, administers high-flow oxygen.", "permissions": "Emergency Code Red Trigger, BLS Administration, Crash Cart Access", "failure_duty": "Performs continuous chest compressions if cardiac arrest occurs.", "inputs": "Severe patient distress, vital monitor alarms, clinical signs", "decisions": "Determines need for immediate Code Red trigger vs urgent doctor call.", "outputs": "Code Red alarm broadcast, vital stabilization actions", "recovery": "Summons secondary nurse from pharmacy/reception to assist."},
            {"id": "ACT-WF10-02", "type": "Human", "name": "Medical Officer", "responsibilities": "Runs Code Red resuscitation, administers IV fluids/emergency drugs, coordinates 108 ambulance transfer.", "permissions": "Emergency Resuscitation Lead, Verbal Order Issuance, SBAR Authorize", "failure_duty": "Accompanies unstable patient in ambulance if paramedic unavailable.", "inputs": "Emergency dashboard, patient clinical state, response to resuscitation", "decisions": "Orders emergency medications (Adrenaline, Atropine, Hydrocortisone, Sorbitrate); decides transfer destination.", "outputs": "Signed SBAR transfer summary, stabilized citizen", "recovery": "Documents verbal orders and retrospective clinical notes post-transfer."}
        ],
        "personas": [
            {"id": "PERSONA-002", "name": "Dr. Manjunath Swamy", "role": "Senior Medical Officer", "env": "Midst of routine consultation when alarm blares.", "goals": "Immediately understand the exact clinical crisis before entering the triage room.", "pain_points": "Vague shouting with no objective vital parameters.", "adaptations": "Doctor screen displays exact reason for Code Red: 'Code Red: 4-year-old child, SpO2 84%, Severe Stridor'."},
            {"id": "PERSONA-001", "name": "Sister Bhavani Gowda", "role": "Staff Nurse", "env": "Critical patient gasping for breath at triage desk.", "goals": "One-touch alarm without typing lengthy descriptions during a crisis.", "pain_points": "Software requiring multiple confirmation dialogs during an emergency.", "adaptations": "Physical or single-tap red emergency button that immediately broadcasts Code Red."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "Emergency Protocol, Crash Cart Log", "create": "Code Red Alert, BLS Event", "update": "Emergency Vitals", "delete": "None", "override": "All Queue Preemption", "signoff": "Nurse BLS Log"},
            {"role": "ROLE-002", "title": "Medical Officer", "read": "All Clinical & Emergency Systems", "create": "Emergency Orders, SBAR", "update": "Resuscitation Notes", "delete": "None", "override": "Emergency Overrule", "signoff": "Emergency Transfer Authorization"}
        ],
        "preconditions": [
            {"id": "PRE-WF10-01", "desc": "Emergency crash cart sealed and verified at morning clinic preflight (WF-001).", "check": "crash_cart.status == 'VERIFIED'", "on_fail": "Break emergency seal immediately; report missing drugs post-resuscitation."},
            {"id": "PRE-WF10-02", "desc": "Oxygen cylinder / concentrator pressure > 100 bar or electric concentrator functional.", "check": "oxygen_source.pressure_ok == TRUE", "on_fail": "Switch to backup portable E-cylinder immediately."}
        ],
        "triggers": [
            {"id": "TRIG-WF10-01", "class": "Automated Trigger", "event": "Triage vitals entry records critical parameter (SpO2 < 90%, SBP < 80)", "source": "Triage Form Validation", "payload": "{ alert_type: 'CRITICAL_VITAL', vital_name: 'SpO2', value: 86 }", "latency": "< 200ms to broadcast alert"},
            {"id": "TRIG-WF10-02", "class": "Nurse Panic Button", "event": "Nurse taps physical / touchscreen 'CODE RED' panic button", "source": "Triage UI / Wall Button", "payload": "{ alert_type: 'MANUAL_CODE_RED', station: 'TRIAGE-01' }", "latency": "< 100ms to sound siren"}
        ],
        "inputs": [
            {"name": "trigger_type", "type": "Enum(VITAL_CRITICAL, CLINICAL_DANGER_SIGN, CARDIAC_ARREST, TRAUMA)", "req": "Mandatory", "source": "Nurse / System", "val": "Defined trigger category", "priv": "Clinical", "enc": "Plaintext", "ex": "VITAL_CRITICAL", "on_err": "Default to CLINICAL_DANGER_SIGN"},
            {"name": "patient_id", "type": "UUID", "req": "Mandatory", "source": "Active Encounter", "val": "Valid patient UUID or emergency token", "priv": "Clinical", "enc": "Plaintext", "ex": "c1d2e3f4-...", "on_err": "Assign provisional emergency UUID"}
        ],
        "outputs": {
            "success": [
                {"name": "Code Red Screen Modal Takeover", "desc": "Fullscreen red pulsating alert on Doctor Chamber and Reception monitors.", "format": "HTML5 Fullscreen Modal WebSocket Event", "recipient": "All Clinic Terminals"},
                {"name": "108 SBAR Transfer Document", "desc": "Standardized electronic handoff bundle printed and sent digitally to 108 ambulance.", "format": "PDF / FHIR Transfer Bundle", "recipient": "108 Paramedic & Receiving District Hospital"}
            ],
            "failure": [
                {"name": "Hardware Alert Failure Warning", "desc": "Edge node logs audio failure and falls back to local visual strobe.", "action": "Nurse verbally shouts 'Code Red Triage' across corridor."}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor N as Staff Nurse
    participant UI as Triage Screen
    participant WS as Edge WebSocket Hub
    actor D as Medical Officer
    participant TV as Clinic Displays
    actor AMB as 108 Ambulance Dispatch
    N->>UI: 1. Tap 'CODE RED' (Child, Severe Stridor, SpO2 84%)
    UI->>WS: 2. Publish Urgent CodeRedEvent
    par Broadcast to Clinic
        WS->>D: 3. Fullscreen Screen Modal + Audible Siren
        WS->>TV: 4. Freeze Routine Displays -> Show 'Emergency in Progress'
    end
    D->>N: 5. Arrives at Triage within 20 seconds
    D->>N: 6. Administer Nebulized Adrenaline & High-Flow Oxygen
    D->>UI: 7. Click 'Dispatch 108 Ambulance'
    UI->>AMB: 8. Send Digital SBAR Referral Bundle & GPS Location
    AMB-->>D: 9. Ambulance Dispatched (ETA 12 min)""",
        "activity_diagram": """flowchart TD
    Start([Danger Sign Identified or Vitals Critical]) --> TapCodeRed[Nurse Hits 'Code Red' Panic Button]
    TapCodeRed --> BroadcastAlarm[Edge Server Fires High-Priority WebSocket Event]
    BroadcastAlarm --> ModalTakeover[Doctor Chamber Screen Overridden with Red Alert Modal]
    BroadcastAlarm --> SoundSiren[Play Audible Klaxon / Strobe on LAN Terminals]
    ModalTakeover --> DoctorArrives[Doctor Abandons OPD & Runs to Triage]
    DoctorArrives --> ABCDEAssessment[Rapid ABCDE Resuscitation Assessment]
    ABCDEAssessment --> OpenAirway[Airway & High-Flow Oxygen via Non-Rebreather Mask]
    OpenAirway --> IVAccess[Establish IV Access & Administer Emergency Drugs]
    IVAccess --> CheckStability{Patient Responds & Stabilizes?}
    CheckStability -- Yes --> ObsBed[Transfer to Clinic Observation Bed for 2-hour monitoring]
    CheckStability -- No / Critical --> Call108[Call 108 Ambulance & Generate SBAR Handover]
    Call108 --> PrintSBAR[Print SBAR Transfer Slip with Vital Trends]
    PrintSBAR --> HandoverParamedic[Handover Patient & SBAR to 108 Paramedic]
    HandoverParamedic --> PostEmergencyLog[Doctor & Nurse Complete Retrospective Emergency Audit]
    ObsBed --> PostEmergencyLog
    PostEmergencyLog --> End([Code Red Concluded & Routine OPD Resumed])""",
        "state_diagram": """stateDiagram-v2
    [*] --> DANGER_DETECTED
    DANGER_DETECTED --> CODE_RED_ACTIVE: Panic Button or Critical Vital Trigger
    CODE_RED_ACTIVE --> RESUSCITATION_IN_PROGRESS: Doctor on Scene & Care Underway
    RESUSCITATION_IN_PROGRESS --> STABILIZED_LOCAL: Vital Signs Recover (MEWS < 3)
    RESUSCITATION_IN_PROGRESS --> AMBULANCE_HANDOVER: 108 Dispatched & Arrives
    STABILIZED_LOCAL --> AUDIT_RETROSPECTIVE: Document Clinical Rationale
    AMBULANCE_HANDOVER --> AUDIT_RETROSPECTIVE: Document SBAR & Paramedic ID
    AUDIT_RETROSPECTIVE --> ROUTINE_RESTORED: Reset Alarms & Resume Queue
    ROUTINE_RESTORED --> [*]"""
    }

    return specs

def write_group2_file():
    specs = get_group2_specs()
    print("Building Group 2 Workflows (WF-006 to WF-010)...")

    header = '''#!/usr/bin/env python3
"""
data_wf06_to_10.py
Clean, self-contained domain specifications for Workflows 06 to 10:
  - WF-006: Informed Clinical & Digital Health Consent Workflow
  - WF-007: Token Issuance, Priority Tagging & Queue Entry Workflow
  - WF-008: Dynamic Multi-Room Queue Orchestration & Display Workflow
  - WF-009: Nursing Triage, Vital Signs & Clinical Acuity Assessment Workflow
  - WF-010: Danger Sign Detection, Critical Value Alert & Emergency Escalation Workflow

Exports:
  DATA_WF06_TO_10 (dict mapping 'WF-006'..'WF-010' to enriched 67-section workflow dicts)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_factory import build_workflow_object
from build_group2 import get_group2_specs

def get_group2_workflows():
    specs = get_group2_specs()
    return {wfid: build_workflow_object(spec) for wfid, spec in specs.items()}

if __name__ == "__main__":
    from workflow_generator import render_workflow_document
    from common import count_lines, find_duplicate_paragraphs
    print("Testing data_wf06_to_10.py...")
    wfs = get_group2_workflows()
    docs = {}
    for wfid, wf_data in wfs.items():
        doc = render_workflow_document(wf_data)
        docs[wfid] = doc
        counts = count_lines(doc)
        status = "PASS" if counts["substantive"] >= 2000 else "FAIL"
        print(f"  {wfid}: Total = {counts['total']}, Substantive = {counts['substantive']} [{status}]")

    dups = find_duplicate_paragraphs(docs, min_len=60)
    print(f"  Duplicate paragraphs within Group 2: {len(dups)}")
'''
    with open('scripts/workflows/data_wf06_to_10.py', 'w', encoding='utf-8') as f:
        f.write(header)
    print("Wrote scripts/workflows/data_wf06_to_10.py")

if __name__ == "__main__":
    write_group2_file()
