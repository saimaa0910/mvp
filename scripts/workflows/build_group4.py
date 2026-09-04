#!/usr/bin/env python3
"""
build_group4.py
Generates data_wf16_to_20.py covering:
  WF-016: Clinical Referral, Higher Center Escalation & Ambulance Transfer Workflow
  WF-017: NCD Follow-Up Scheduling, Chronic Disease Recall & Defaulter Tracking Workflow
  WF-018: Omnichannel Patient & Staff Notification, Alerting & Communication Workflow
  WF-019: Citizen Grievance Redressal, Feedback & SLA Escalation Workflow
  WF-020: Cryptographic Audit Trail, Immutable Logging & Tamper Detection Workflow
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_factory import build_workflow_object
from workflow_metadata import WORKFLOW_MAP

def get_group4_specs():
    specs = {}

    # =========================================================================
    # WF-016: Referral Workflow
    # =========================================================================
    m16 = WORKFLOW_MAP["WF-016"]
    specs["WF-016"] = {
        "id": "WF-016", "num": "16", "name": m16["name"], "domain": m16["domain"],
        "exec_summary": {
            "purpose": "Coordinates emergency and elective clinical patient referrals from Namma Clinic to secondary municipal hospitals (Taluk/General Hospitals) and tertiary medical centers (Bowring & Lady Curzon, Victoria Hospital, KC General). Generates standardized e-Referral summaries (SBAR protocol), dispatches 108 Emergency Medical Ambulances with real-time GPS tracking, transmits continuous vital sign streams, and tracks referral loop closure upon patient admission or return.",
            "rationale": "Fragmented referrals without structured clinical summaries result in repeated testing, delayed emergency surgical interventions, and lost-to-follow-up patients. A digital referral pipeline ensures the receiving specialist has complete diagnostic data before the ambulance arrives at the emergency bay.",
            "clinical_impact": "Reduces inter-facility door-to-needle and door-to-balloon times for acute myocardial infarction, acute stroke, and severe sepsis; guarantees clinical continuity across primary, secondary, and tertiary healthcare tiers.",
            "system_impact": "Binds local encounters to ABDM Health Information Exchange (HIE-CM); dispatches digital referral payloads to receiving facility EMRs; and streams telemetric GPS/vital telemetry to the 108 emergency dispatch center.",
            "risk_profile": "Traffic congestion delaying 108 ambulance response; receiving hospital bed unavailability; network failure during emergency transfer summary push; and patient refusing transfer due to cost/distance fears."
        },
        "objectives": [
            {"id": "OBJ-WF16-01", "title": "Rapid e-Referral Generation", "desc": "Generate and cryptographically sign standardized SBAR clinical transfer summary within 2 minutes of referral decision.", "metric": "Referral Generation Latency < 120s", "verification": "Referral creation audit timestamp analysis"},
            {"id": "OBJ-WF16-02", "title": "Sub-Minute 108 Ambulance Dispatch", "desc": "Transmit electronic dispatch request with patient location and acuity to GVK EMRI 108 within 60 seconds.", "metric": "108 Dispatch API Latency < 60s", "verification": "108 gateway transaction receipts"},
            {"id": "OBJ-WF16-03", "title": "Closed-Loop Referral Tracking", "desc": "Achieve >= 90% referral loop closure confirmation (admission, discharge, or counter-referral) within 72 hours.", "metric": "Referral Loop Closure Rate >= 90%", "verification": "Central ABDM referral status registry audit"},
            {"id": "OBJ-WF16-04", "title": "Offline Referral Continuity", "desc": "Print emergency encrypted QR code referral slip during total network outage for physical paramedic transport.", "metric": "Offline Slip Generation Availability = 100%", "verification": "Offline referral print simulation test"}
        ],
        "in_scope": [
            {"area": "Emergency Escalation", "desc": "Immediate 108 ambulance summon for acute coronary syndrome, severe trauma, stroke, and obstetric emergencies."},
            {"area": "Elective Specialist Referral", "desc": "Outpatient scheduling for Ophthalmology, Orthopedics, ENT, Psychiatry, and advanced Sonography."},
            {"area": "Standardized SBAR Summary", "desc": "Situation, Background, Assessment, Recommendation structured summary generation in PDF and FHIR format."},
            {"area": "Bed Availability Inquiry", "desc": "Real-time query of BBMP secondary hospital ICU and maternity bed occupancy."}
        ],
        "out_of_scope": [
            {"area": "Air Ambulance Evacuation", "desc": "Helicopter emergency medical services; out of scope for urban primary clinics.", "handoff": "State Disaster Management Authority"},
            {"area": "Private Hospital Referral Subsidies", "desc": "Processing private commercial hospital insurance claims; out of scope.", "handoff": "Suvarna Arogya Suraksha Trust (SAST)"}
        ],
        "actors": [
            {"id": "ACT-WF16-01", "type": "Human", "name": "Medical Officer", "responsibilities": "Decides need for referral, selects receiving hospital, explains transfer rationale, signs SBAR referral.", "permissions": "Referral Create/Sign, 108 Emergency Dispatch, Bed Hold", "failure_duty": "Accompanies critical patient in ambulance if patient is actively deteriorating.", "inputs": "Encounter notes, vital trends, lab results, patient condition", "decisions": "Determines transport urgency (Red Emergency vs Green Elective) and destination specialty.", "outputs": "Signed e-Referral document, 108 dispatch order", "recovery": "Authorizes telephone referral handover if digital gateway unreachable."},
            {"id": "ACT-WF16-02", "type": "Human", "name": "108 Ambulance Paramedic", "responsibilities": "Arrives at clinic, takes clinical handover, connects transport monitor, safely transports citizen.", "permissions": "Transport Takeover, In-Transit Vital Stream", "failure_duty": "Initiates en-route CPR if cardiac arrest occurs during transit.", "inputs": "SBAR print slip, verbal doctor handover, monitor vitals", "decisions": "Selects fastest transit route; notifies receiving emergency room of ETA.", "outputs": "Signed transfer acceptance receipt", "recovery": "Communicates via emergency wireless radio if mobile broadband drops."}
        ],
        "personas": [
            {"id": "PERSONA-002", "name": "Dr. Manjunath Swamy", "role": "Senior Medical Officer", "env": "Stabilizing a 58-year-old male with acute chest pain (ST-elevation MI).", "goals": "Get 108 ambulance rolling immediately and alert Victoria Hospital cardiology team.", "pain_points": "Long phone hold times with ambulance dispatchers; repetitive dictation.", "adaptations": "1-click 'EMERGENCY 108 DISPATCH' button that pushes patient GPS, age, vitals, and ECG strip instantly."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-002", "title": "Medical Officer", "read": "Referral Registry, Bed Matrix", "create": "Referral Order, SBAR", "update": "Referral Status", "delete": "None", "override": "Emergency Bypass", "signoff": "Referral Digital Signoff"},
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "Referral Orders", "create": "Transport Vitals Note", "update": "Handoff Status", "delete": "None", "override": "None", "signoff": "Paramedic Handoff Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF16-01", "desc": "Active clinical encounter with documented clinical assessment (WF-011).", "check": "encounter.status == 'IN_PROGRESS' || encounter.status == 'CODE_RED'", "on_fail": "Require active encounter before initiating referral."},
            {"id": "PRE-WF16-02", "desc": "Citizen / Guardian informed consent obtained or emergency exception documented (WF-006).", "check": "consent.referral_status in ('GRANTED', 'EMERGENCY_BYPASS')", "on_fail": "Document informed refusal if citizen refuses transfer."}
        ],
        "triggers": [
            {"id": "TRIG-WF16-01", "class": "Emergency Trigger", "event": "Doctor clicks 'Emergency Referral' or Code Red alert escalated", "source": "Doctor Chamber UI", "payload": "{ urgency: 'RED', suspected_condition: 'ACUTE_CORONARY_SYNDROME' }", "latency": "< 100ms to open transfer modal"}
        ],
        "inputs": [
            {"name": "receiving_facility_id", "type": "String(16)", "req": "Mandatory", "source": "Facility Directory", "val": "Valid BBMP hospital ID", "priv": "Operational", "enc": "Plaintext", "ex": "HOSP-VICTORIA", "on_err": "Default to nearest General Hospital"},
            {"name": "referral_reason", "type": "Text", "req": "Mandatory", "source": "Doctor Entry", "val": "Clinical indication for transfer", "priv": "Clinical", "enc": "Plaintext", "ex": "Anterior Wall STEMI requiring emergency catheterization", "on_err": "Require clinical indication"}
        ],
        "outputs": {
            "success": [
                {"name": "Signed SBAR e-Referral Document", "desc": "FHIR ServiceRequest and CarePlan bundle with complete clinical handover data.", "format": "Signed PDF & FHIR JSON", "recipient": "108 Paramedic & Receiving Hospital ER"},
                {"name": "108 Ambulance Dispatch Token", "desc": "Electronic tracking identifier with live ambulance GPS location updates.", "format": "JSON Telemetry Stream", "recipient": "Doctor Workstation Screen"}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor D as Medical Officer
    participant UI as Doctor Chamber UI
    participant REF as Referral Engine
    participant EMRI as 108 Dispatch Gateway
    actor AMB as 108 Paramedic
    participant HOSP as Receiving Hospital ER
    D->>UI: 1. Click 'Emergency Referral' (Acute STEMI)
    D->>UI: 2. Select: Victoria Hospital ER -> Click 'Dispatch 108'
    UI->>REF: 3. Generate SBAR Summary & Sign with Doctor Key
    REF->>EMRI: 4. API Call: Dispatch Nearest Ambulance (P0 Red)
    EMRI-->>UI: 5. Ambulance Dispatched (KA-01-G-1082, ETA 8 min)
    REF->>HOSP: 6. Pre-arrival Notification: Cath Lab Alert
    AMB->>D: 7. Paramedic arrives, verifies SBAR, takes patient
    D->>UI: 8. Confirm Patient Handover Completed""",
        "activity_diagram": """flowchart TD
    Start([Doctor Decides Patient Requires Referral]) --> DetermineUrgency{Evaluate Referral Urgency}
    DetermineUrgency -- Red / Emergency --> OpenEmergReferral[Open Emergency 108 Referral Protocol]
    DetermineUrgency -- Green / Elective --> OpenElective[Open Elective Specialist Referral]
    OpenEmergReferral --> AutoPopulateSBAR[Auto-populate SBAR from Vitals, Notes, and Labs]
    AutoPopulateSBAR --> SelectReceivingHospital[Select Receiving Hospital: Victoria / Bowring]
    SelectReceivingHospital --> Dispatch108[Dispatch 108 Ambulance via API Gateway]
    Dispatch108 --> PrintThermalSBAR[Print Thermal SBAR Slip with Offline QR Code]
    PrintThermalSBAR --> PreArrivalAlert[Push Digital Pre-Arrival Alert to Receiving ER]
    PreArrivalAlert --> AwaitAmbulance[Stabilize Patient in Clinic while Awaiting Vehicle]
    AwaitAmbulance --> ParamedicArrival[108 Ambulance Arrives at Clinic Door]
    ParamedicArrival --> HandoverPatient[Doctor Conducts Verbal Handover to Paramedic]
    HandoverPatient --> SignTransfer[Paramedic Scans Barcode & Signs Receipt]
    SignTransfer --> EndEmergency([Patient in Transit & Referral Loop Open])
    OpenElective --> BookSlot[Book Outpatient Specialist Appointment]
    BookSlot --> PrintAppointmentSlip[Print Bilingual Appointment Slip for Citizen]
    PrintAppointmentSlip --> EndElective([Citizen Departs with Referral Slip])""",
        "state_diagram": """stateDiagram-v2
    [*] --> REFERRAL_INITIATED
    REFERRAL_INITIATED --> AMBULANCE_DISPATCHED: Emergency 108 Summoned
    AMBULANCE_DISPATCHED --> IN_TRANSIT: Paramedic Handover Complete
    IN_TRANSIT --> ADMITTED_AT_RECEIVING: Receiving Hospital Confirms Arrival
    ADMITTED_AT_RECEIVING --> LOOP_CLOSED: Counter-Referral / Discharge Summary Received
    REFERRAL_INITIATED --> ELECTIVE_SCHEDULED: Outpatient Slot Confirmed
    ELECTIVE_SCHEDULED --> LOOP_CLOSED: Specialist Visit Completed
    LOOP_CLOSED --> [*]"""
    }

    # =========================================================================
    # WF-017: Follow-Up Workflow
    # =========================================================================
    m17 = WORKFLOW_MAP["WF-017"]
    specs["WF-017"] = {
        "id": "WF-017", "num": "17", "name": m17["name"], "domain": m17["domain"],
        "exec_summary": {
            "purpose": "Governs chronic non-communicable disease (Hypertension, Type 2 Diabetes, Epilepsy) and infectious disease (TB DOTS) appointment scheduling, automated multilingual recall notifications, appointment defaulter tracking (+7 days overdue), ASHA / ANM community home-visit task generation, and treatment adherence monitoring in Namma Clinic.",
            "rationale": "High patient drop-out rates in chronic disease care lead to uncontrolled hypertension, diabetic retinopathy/nephropathy, and drug-resistant tuberculosis. Proactive community recall and doorstep tasking of ASHA workers ensures sustained therapy adherence and early complication detection.",
            "clinical_impact": "Maintains patient blood pressure (< 140/90) and HbA1c (< 7.0%) control; reduces stroke and myocardial infarction incidence; and prevents default in national tuberculosis control programs.",
            "system_impact": "Generates automated cron recall jobs; interfaces with National NCD Portal and Reproductive Child Health (RCH) gateways; and exports daily task lists to ASHA mobile tablets.",
            "risk_profile": "Changed or invalid citizen mobile numbers; ASHA worker workload fatigue; citizen relocation out of clinic ward; and stigma-related refusal of home visits."
        },
        "objectives": [
            {"id": "OBJ-WF17-01", "title": "Automated Follow-Up Scheduling", "desc": "Schedule next clinical follow-up appointment within 1.0 second of doctor consultation sign-off.", "metric": "Scheduling Latency < 1.0s", "verification": "Follow-up ledger creation timestamp benchmark"},
            {"id": "OBJ-WF17-02", "title": "Bilingual Reminder Dispatch", "desc": "Dispatch automated Kannada and English SMS reminders at T-48h and T-24h prior to appointment.", "metric": "Reminder Dispatch Compliance = 100%", "verification": "SMS gateway delivery callback logs"},
            {"id": "OBJ-WF17-03", "title": "Automated Defaulter Identification", "desc": "Flag 100% of citizens failing to attend within 7 calendar days of scheduled recall.", "metric": "Defaulter Detection Rate = 100%", "verification": "Nightly defaulter detection batch query"},
            {"id": "OBJ-WF17-04", "title": "ASHA Home-Visit Task Routing", "desc": "Route verified defaulters to ward-specific ASHA worker mobile task queues within 24 hours of default.", "metric": "ASHA Task Routing Latency < 24h", "verification": "Community task assignment audit logs"}
        ],
        "in_scope": [
            {"area": "Chronic Care Appointment Booking", "desc": "14-day, 30-day, and 90-day return visit scheduling with time-slot allocations."},
            {"area": "Omnichannel Recall Reminders", "desc": "Automated SMS, WhatsApp, and outbound IVR voice calls in spoken Kannada."},
            {"area": "Defaulter Cohort Analytics", "desc": "Categorization of missed appointments into Grade 1 (1-7 days), Grade 2 (8-30 days), and Lost to Follow-Up (>30 days)."},
            {"area": "ASHA Doorstep Task Allocation", "desc": "Geographic ward-based routing of home visit requests for physical medication adherence checks."}
        ],
        "out_of_scope": [
            {"area": "Tertiary Inpatient Palliative Care", "desc": "Continuous hospice home nursing care; out of scope for primary outpatient clinic.", "handoff": "Kidwai / District Palliative Care Team"},
            {"area": "Private Medical Specialist Appointments", "desc": "Booking private commercial clinics; out of scope.", "handoff": "None - Public Health Scope"}
        ],
        "actors": [
            {"id": "ACT-WF17-01", "type": "Human", "name": "Staff Nurse", "responsibilities": "Reviews daily follow-up roster, checks in arriving recall patients, reviews defaulter list.", "permissions": "Follow-up Reschedule, Defaulter Flag, ASHA Task Dispatch", "failure_duty": "Manually phones high-risk defaulters (uncontrolled BP/TB) from clinic landline.", "inputs": "Daily appointment roster, attendance records", "decisions": "Determines whether to trigger urgent ASHA home visit.", "outputs": "Updated appointment status, ASHA task assignments", "recovery": "Re-schedules appointment if citizen was hospitalized elsewhere."},
            {"id": "ACT-WF17-02", "type": "Human", "name": "ASHA Worker / ANM", "responsibilities": "Receives home-visit task, visits citizen residence, assesses drug adherence, encourages clinic revisit.", "permissions": "Community Task Update, Home Adherence Report", "failure_duty": "Reports non-traceable or relocated citizens to clinic coordinator.", "inputs": "ASHA mobile app task list, citizen address", "decisions": "Assesses barrier to clinic visit (lack of transport, family conflict, illness).", "outputs": "Completed home-visit report, confirmed return date", "recovery": "Attempts second visit during evening hours if citizen was away at work."}
        ],
        "personas": [
            {"id": "PERSONA-001", "name": "Sister Bhavani Gowda", "role": "Staff Nurse", "env": "Triage desk managing chronic disease register.", "goals": "Know exactly which diabetes patients missed their medication refill this week.", "pain_points": "Sorting through hundreds of paper register cards to find defaulters.", "adaptations": "One-click 'Defaulter Dashboard' sorted by risk acuity (TB > Uncontrolled HTN > Stable HTN)."},
            {"id": "PERSONA-007", "name": "Shantamma", "role": "Elderly Chronic Patient", "env": "Home in Govindaraja Nagar; often forgets date to refill BP medicine.", "goals": "Get a simple reminder so she does not run out of tablets.", "pain_points": "Complex text messages she cannot read.", "adaptations": "Recorded Kannada voice call: 'Shantamma-avare, tomorrow is your blood pressure check at Namma Clinic'."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-001", "title": "Staff Nurse", "read": "Follow-up Register, ASHA Tasks", "create": "Recall Schedule, ASHA Task", "update": "Attendance Status", "delete": "None", "override": "None", "signoff": "Roster Check Signoff"},
            {"role": "ROLE-007", "title": "ASHA / Community Worker", "read": "Assigned Ward Tasks", "create": "Home Visit Report", "update": "Task Status", "delete": "None", "override": "None", "signoff": "Home Visit Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF17-01", "desc": "Patient has completed primary encounter and has valid contact number or ward address.", "check": "patient.phone != NULL || patient.ward_address != NULL", "on_fail": "Obtain neighbor/guardian contact details before discharge."},
            {"id": "PRE-WF17-02", "desc": "Notification service worker operational for automated message dispatch.", "check": "notification_daemon.status == 'ONLINE'", "on_fail": "Queue reminder tasks in local database for deferred batch processing."}
        ],
        "triggers": [
            {"id": "TRIG-WF17-01", "class": "Encounter Close Trigger", "event": "Doctor signs encounter specifying follow-up interval (e.g., 'Review in 30 days')", "source": "Consultation Chamber UI", "payload": "{ patient_id: 'PAT-001', interval_days: 30 }", "latency": "< 500ms to register appointment"},
            {"id": "TRIG-WF17-02", "class": "Cron Schedule Trigger", "event": "Nightly cron executes defaulter evaluation at 23:00 IST", "source": "Edge Server Cron Engine", "payload": "{ scan_date: '2026-09-04' }", "latency": "< 5 sec to scan clinic ledger"}
        ],
        "inputs": [
            {"name": "recall_date", "type": "Date", "req": "Mandatory", "source": "Doctor Order", "val": "Future date within 180 days", "priv": "Operational", "enc": "Plaintext", "ex": "2026-10-04", "on_err": "Default to 30 days"},
            {"name": "chronic_category", "type": "Enum(HTN, DM, TB, ANC, PEDIATRIC)", "req": "Mandatory", "source": "Encounter Context", "val": "Defined category", "priv": "Clinical", "enc": "Plaintext", "ex": "HTN", "on_err": "Default to HTN"}
        ],
        "outputs": {
            "success": [
                {"name": "Scheduled Appointment Record", "desc": "Confirmed follow-up slot with unique appointment reference number.", "format": "JSON Record & SMS Notice", "recipient": "Patient EMR & Citizen Mobile"},
                {"name": "ASHA Community Task", "desc": "Assigned task payload dispatched to designated ward ASHA mobile application.", "format": "JSON REST Payload", "recipient": "ASHA Mobile Worker App"}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor D as Medical Officer
    participant UI as Clinic App
    participant SCH as Follow-Up Engine
    participant DB as SQLite DB
    participant SMS as SMS Gateway
    actor P as Patient
    actor ASHA as ASHA Worker
    D->>UI: 1. Sign Encounter -> 'Follow-up in 30 Days (Oct 4)'
    UI->>SCH: 2. Schedule Recall for Oct 4, 2026
    SCH->>DB: 3. Insert Appointment Record
    SCH->>SMS: 4. Send Kannada SMS: 'Your next visit is on Oct 4'
    SMS-->>P: 5. Citizen receives SMS
    Note over SCH,DB: Oct 11 (7 Days Past Due - No Show)
    SCH->>DB: 6. Mark Status: DEFAULTER_GRADE_1
    SCH->>ASHA: 7. Dispatch Doorstep Home Visit Task to Ward ASHA
    ASHA->>P: 8. ASHA visits home, checks BP, accompanies to clinic""",
        "activity_diagram": """flowchart TD
    Start([Encounter Concluded with Follow-Up Order]) --> CalculateDate[System Calculates Exact Recall Date]
    CalculateDate --> CheckSlotAvailability[Verify Clinic Operating Schedule for Target Date]
    CheckSlotAvailability --> BookSlot[Book Follow-Up Slot in Clinic Master Calendar]
    BookSlot --> SendConfirmSMS[Send Immediate Confirmation SMS in Kannada]
    SendConfirmSMS --> AwaitRecallDate[System Monitors Calendar Progression]
    AwaitRecallDate --> ReminderT48[Send Reminder SMS at T-48 Hours]
    ReminderT48 --> ReminderT24[Send Automated Voice Call at T-24 Hours]
    ReminderT24 --> CheckAttendance{Citizen Attends on Scheduled Date?}
    CheckAttendance -- Yes --> MarkAttended[Mark Appointment Completed & Link Episode]
    MarkAttended --> End([Follow-up Completed])
    CheckAttendance -- No / Missed --> MonitorGracePeriod[Wait 7-Day Grace Period]
    MonitorGracePeriod --> CheckGraceAttendance{Citizen Attended within 7 Days?}
    CheckGraceAttendance -- Yes --> MarkAttended
    CheckGraceAttendance -- No --> FlagDefaulter[Flag as Defaulter Grade 1]
    FlagDefaulter --> GenerateASHATask[Generate Home-Visit Task for Ward ASHA Worker]
    GenerateASHATask --> ASHAHighestPriority[ASHA Conducts Doorstep Visit & Counsels Citizen]
    ASHAHighestPriority --> ReVisitClinic[Citizen Returns to Clinic with ASHA]
    ReVisitClinic --> MarkAttended""",
        "state_diagram": """stateDiagram-v2
    [*] --> SCHEDULED
    SCHEDULED --> REMINDER_SENT: T-48h Reminder Dispatched
    REMINDER_SENT --> ATTENDED: Patient Visits on Time
    REMINDER_SENT --> MISSED_GRACE: Appointment Date Passed
    MISSED_GRACE --> ATTENDED: Patient Attends within 7 Days
    MISSED_GRACE --> DEFAULTER_ACTIVE: 7 Days Elapsed without Visit
    DEFAULTER_ACTIVE --> ASHA_TASKED: Home Visit Assigned to ASHA
    ASHA_TASKED --> ATTENDED: ASHA Escorts Citizen to Clinic
    ASHA_TASKED --> LOST_TO_FOLLOW_UP: Citizen Relocated / Untraceable
    ATTENDED --> [*]
    LOST_TO_FOLLOW_UP --> [*]"""
    }

    # =========================================================================
    # WF-018: Notification Workflow
    # =========================================================================
    m18 = WORKFLOW_MAP["WF-018"]
    specs["WF-018"] = {
        "id": "WF-018", "num": "18", "name": m18["name"], "domain": m18["domain"],
        "exec_summary": {
            "purpose": "Controls multichannel transactional messaging pipelines in Namma Clinic: National SMS gateway integration, WhatsApp Business API messaging, automated Outbound Dialing (IVR) voice calls in Kannada, and clinic waiting area audio chimes. Enforces Telecom Regulatory Authority of India (TRAI) DND compliance, exponential backoff retries, failover channel routing, privacy masking (zero clinical PHI on lockscreens), and delivery receipt auditing.",
            "rationale": "Digital health platforms depend on reliable communication for token tracking, lab report readiness, prescription pick-up alerts, and chronic disease recall. Poor mobile delivery rates or privacy breaches through unencrypted SMS undermine platform credibility and violate citizen privacy.",
            "clinical_impact": "Alerts citizens to critical lab panic values; prevents abandoned prescriptions at pharmacy counters; and ensures timely attendance of antenatal mothers for scheduled immunizations.",
            "system_impact": "Acts as the platform's outbound communication message broker; queues messages in SQLite WAL queues; dispatches through state-approved telecom aggregator gateways; and maintains delivery status webhooks.",
            "risk_profile": "Telecom network congestion delaying SMS delivery; TRAI DND blocking transactional messages; invalid citizen mobile numbers; and vendor gateway downtime."
        },
        "objectives": [
            {"id": "OBJ-WF18-01", "title": "Sub-5s Token SMS Delivery", "desc": "Deliver initial token registration SMS to citizen handset within 5 seconds of token generation.", "metric": "Token SMS Delivery Latency p90 < 5.0s", "verification": "Telecom gateway delivery timestamp analysis"},
            {"id": "OBJ-WF18-02", "title": "Zero PHI Exposure on Lockscreen", "desc": "Enforce strict DPDP privacy masking: SMS notifications must never display clinical diagnosis or medication names on lockscreen previews.", "metric": "Lockscreen PHI Exposure = 0", "verification": "Template privacy compliance review"},
            {"id": "OBJ-WF18-03", "title": "Automated Channel Failover", "desc": "Automatically failover from WhatsApp to SMS, then to IVR voice call upon primary channel delivery failure.", "metric": "Failover Trigger Latency < 60s", "verification": "Simulated channel failure test suite"},
            {"id": "OBJ-WF18-04", "title": "Delivery Audit Trail Completeness", "desc": "Capture 100% of carrier delivery receipts (Delivered, Bounced, DND Blocked) with cryptographic timestamps.", "metric": "Delivery Receipt Capture Rate = 100%", "verification": "Notification audit ledger queries"}
        ],
        "in_scope": [
            {"area": "SMS Gateway Integration", "desc": "Integration with C-DAC / NIC transactional SMS gateway using approved DLT templates."},
            {"area": "WhatsApp Business Messaging", "desc": "Rich messaging for appointment slips, prescription summaries, and clinic navigation links."},
            {"area": "Outbound IVR Voice Calls", "desc": "Synthesized and studio-recorded spoken Kannada voice calls for illiterate elderly citizens."},
            {"area": "Delivery Status Webhooks", "desc": "Real-time processing of carrier delivery receipts and failure categorization."}
        ],
        "out_of_scope": [
            {"area": "Commercial Marketing Campaigns", "desc": "Promotional or political advertising; strictly prohibited on public health platform.", "handoff": "None - Prohibited"},
            {"area": "Personal Staff Chat Messaging", "desc": "Informal peer-to-peer messaging between healthcare workers.", "handoff": "BBMP Official Intra-Net"}
        ],
        "actors": [
            {"id": "ACT-WF18-01", "type": "System", "name": "Notification Message Broker", "responsibilities": "Ingests notification jobs, renders templates, checks DND status, dispatches payloads, monitors webhooks.", "permissions": "Message Dispatch, Gateway Access, Retry Schedule", "failure_duty": "Switches to secondary telecom gateway upon primary aggregator outage.", "inputs": "Trigger events, template IDs, recipient mobile numbers", "decisions": "Selects optimal delivery channel based on recipient preference and urgency.", "outputs": "Dispatched messages, delivery status records", "recovery": "Executes exponential backoff retry up to 3 attempts."},
            {"id": "ACT-WF18-02", "type": "Human", "name": "Citizen / Patient", "responsibilities": "Receives SMS/WhatsApp, reads instructions, presents token/appointment link at clinic.", "permissions": "Opt-In/Out Preferences, Channel Selection", "failure_duty": "Reports non-receipt of messages to clinic registration desk.", "inputs": "SMS text, WhatsApp message, voice call", "decisions": "Follows instructions to attend clinic or review report.", "outputs": "Encounter attendance or report view", "recovery": "Updates mobile phone number at clinic kiosk."}
        ],
        "personas": [
            {"id": "PERSONA-007", "name": "Shantamma", "role": "Elderly Illiterate Patient", "env": "Feature phone user; cannot read English or Kannada text SMS.", "goals": "Receive voice phone call reminders she can listen to in Kannada.", "pain_points": "Unopened text messages accumulating on feature phone.", "adaptations": "Auto-detection of feature phone user profile to trigger outbound IVR Kannada voice calls."},
            {"id": "PERSONA-008", "name": "Ramesh Kumar", "role": "Tech-Savvy Working Father", "env": "Smartphone user on WhatsApp.", "goals": "Receive PDF child immunization card directly on WhatsApp.", "pain_points": "Paper slips getting lost in home.", "adaptations": "Official verified WhatsApp Business green-badge PDF delivery."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-006", "title": "System Administrator", "read": "Delivery Logs, Gateway Status", "create": "Template Draft", "update": "Gateway Config", "delete": "None", "override": "Emergency Broadcast Override", "signoff": "Template DLT Signoff"},
            {"role": "ROLE-008", "title": "Citizen / Patient", "read": "Own Notifications", "create": "None", "update": "Notification Preferences", "delete": "Opt-Out Non-Critical", "override": "None", "signoff": "None"}
        ],
        "preconditions": [
            {"id": "PRE-WF18-01", "desc": "Message templates approved and registered on TRAI DLT (Distributed Ledger Technology) portal.", "check": "template.dlt_status == 'APPROVED'", "on_fail": "Carrier gateway will reject unregistered templates."},
            {"id": "PRE-WF18-02", "desc": "Valid Indian mobile phone number (10 digits, regex ^[6-9]\\d{9}$).", "check": "phone.is_valid == TRUE", "on_fail": "Skip SMS dispatch; fall back to physical printed slip."}
        ],
        "triggers": [
            {"id": "TRIG-WF18-01", "class": "Event Bus Trigger", "event": "Platform event published (TokenMinted, LabReady, FollowUpDue)", "source": "Internal Event Hub", "payload": "{ event_type: 'TOKEN_MINTED', recipient: '9876543210' }", "latency": "< 50ms to queue notification"}
        ],
        "inputs": [
            {"name": "template_id", "type": "String(32)", "req": "Mandatory", "source": "Template Registry", "val": "Approved DLT template identifier", "priv": "Operational", "enc": "Plaintext", "ex": "DLT-NAMMA-TOKEN-01", "on_err": "Reject unknown template"},
            {"name": "recipient_phone", "type": "String(10)", "req": "Mandatory", "source": "Patient Profile", "val": "10-digit mobile number", "priv": "Restricted", "enc": "Encrypted at rest", "ex": "9845012345", "on_err": "Abort dispatch"}
        ],
        "outputs": {
            "success": [
                {"name": "Dispatched Telecommunication Message", "desc": "SMS / WhatsApp payload delivered to citizen device with carrier acknowledgment.", "format": "SMPP PDU / WhatsApp JSON", "recipient": "Citizen Mobile Handset"},
                {"name": "Delivery Receipt Record", "desc": "Carrier delivery report logging timestamp, status code, and latency.", "format": "JSON Delivery Webhook", "recipient": "Notification Audit Store"}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    participant SYS as Clinic Flow Engine
    participant NB as Notification Broker
    participant GW as Telecom Gateway (SMS/DLT)
    actor C as Citizen Handset
    SYS->>NB: 1. Event: LabResultsReady(Token SNR-001)
    NB->>NB: 2. Render Template: 'Your test results are ready at Namma Clinic'
    NB->>GW: 3. Submit SMPP Message (Kannada UTF-8)
    GW-->>C: 4. Deliver SMS to Mobile Handset
    C-->>GW: 5. Carrier Handset Delivery Acknowledgment
    GW->>NB: 6. Webhook: Status DELIVERED (Latency 2.8s)
    NB->>SYS: 7. Mark Notification Delivered in Encounter Ledger""",
        "activity_diagram": """flowchart TD
    Start([Platform Event Triggered]) --> CheckChannelPref{Evaluate Recipient Channel Preference}
    CheckChannelPref -- WhatsApp Preferred --> AttemptWhatsApp[Dispatch via WhatsApp Business API]
    CheckChannelPref -- SMS Default --> AttemptSMS[Dispatch via C-DAC Transactional SMS Gateway]
    CheckChannelPref -- Elderly / Voice Preferred --> AttemptIVR[Initiate Outbound Automated Voice Call]
    AttemptWhatsApp --> WhatsAppResponse{Delivered within 30s?}
    WhatsAppResponse -- Yes --> LogSuccess[Log Message Delivered in Audit Ledger]
    WhatsAppResponse -- No / Unregistered --> AttemptSMS
    AttemptSMS --> SMSResponse{Carrier Handset Acknowledgment?}
    SMSResponse -- Yes --> LogSuccess
    SMSResponse -- No / Timeout --> CheckUrgency{Is Notification Urgent / Panic?}
    CheckUrgency -- Yes --> AttemptIVR
    CheckUrgency -- No --> RetryQueue[Queue for Exponential Backoff Retry (Max 3)]
    AttemptIVR --> IVRResponse{Call Answered?}
    IVRResponse -- Yes --> PlayKannadaAudio[Play Kannada Studio Voice Message]
    PlayKannadaAudio --> LogSuccess
    IVRResponse -- No --> RetryQueue
    LogSuccess --> End([Notification Completed])
    RetryQueue --> End""",
        "state_diagram": """stateDiagram-v2
    [*] --> QUEUED
    QUEUED --> DISPATCHED: Handed to Telecom Gateway
    DISPATCHED --> DELIVERED: Carrier Handset Receipt Confirmed
    DISPATCHED --> RETRYING: Network Delivery Failure
    RETRYING --> DISPATCHED: Backoff Timeout Elapsed
    RETRYING --> FAILED_EXHAUSTED: 3 Retries Failed
    DELIVERED --> [*]
    FAILED_EXHAUSTED --> [*]"""
    }

    # =========================================================================
    # WF-019: Grievance Workflow
    # =========================================================================
    m19 = WORKFLOW_MAP["WF-019"]
    specs["WF-019"] = {
        "id": "WF-019", "num": "19", "name": m19["name"], "domain": m19["domain"],
        "exec_summary": {
            "purpose": "Governs citizen grievance lodging, multi-modal feedback capture (Touchscreen Kiosk, QR code posters, 24/7 Helpline, Reception Desk Forms), automated ticket classification (Wait Times, Drug Stockouts, Staff Demeanor, Sanitation), SLA-driven resolution tracking (24h/72h), escalation hierarchy to the BBMP Zonal Health Officer, and citizen resolution feedback loops in Namma Clinic.",
            "rationale": "Public healthcare facilities require transparent accountability to build civic trust and eliminate systemic deficiencies. A frictionless, multilingual grievance redressal mechanism ensures citizen concerns are heard without fear of retaliation and resolved under strict statutory timelines.",
            "clinical_impact": "Identifies recurring clinical quality issues (e.g., rushed consultations, medication stock ruptures, unclean diagnostic spaces) and triggers corrective and preventive action (CAPA) plans.",
            "system_impact": "Interfaces with the BBMP Sahaaya 2.0 citizen grievance portal; logs encrypted ticket records with cryptographic receipt IDs; and broadcasts resolution alerts via SMS to citizens.",
            "risk_profile": "Vexatious or frivolous complaints; citizen fear of retribution from local clinic staff; delayed review by supervisory health officers; and unclosed feedback loops."
        },
        "objectives": [
            {"id": "OBJ-WF19-01", "title": "Rapid Ticket Lodging", "desc": "Complete grievance submission and issue tracking ticket ID to citizen in < 60 seconds.", "metric": "Lodging Duration p95 < 60s", "verification": "Kiosk and mobile web submission telemetry"},
            {"id": "OBJ-WF19-02", "title": "24-Hour Critical Redressal SLA", "desc": "Acknowledge and initiate investigation for 100% of critical grievances (medication denial, emergency delay) within 24 hours.", "metric": "Critical SLA Adherence = 100%", "verification": "Grievance resolution lifecycle audit"},
            {"id": "OBJ-WF19-03", "title": "Automated Escalation Hierarchy", "desc": "Automatically escalate unaddressed grievances to the Zonal Health Officer upon 48-hour SLA breach.", "metric": "Escalation Execution Rate = 100%", "verification": "SLA breach watchdog execution logs"},
            {"id": "OBJ-WF19-04", "title": "Bilingual Citizen Feedback", "desc": "Deliver written resolution summary in vernacular Kannada and English via SMS link upon ticket closure.", "metric": "Resolution Communication Rate = 100%", "verification": "Ticket closure notification audit"}
        ],
        "in_scope": [
            {"area": "Multi-Modal Intake", "desc": "Exit kiosk survey, scannable poster QR code (mobile web form), toll-free voice helpline, paper complaint box."},
            {"area": "Category Taxonomy", "desc": "Wait Time > 45m, Medicine Out of Stock, Staff Demeanor, Facility Cleanliness, Diagnostic Test Delay."},
            {"area": "SLA & Escalation Engine", "desc": "Level 1: Clinic Coordinator (24h), Level 2: Medical Officer (48h), Level 3: BBMP Zonal Health Officer (72h)."},
            {"area": "Resolution & Verification", "desc": "Documenting corrective action, citizen satisfaction confirmation, and root-cause analysis."}
        ],
        "out_of_scope": [
            {"area": "Criminal Malpractice Prosecution", "desc": "Formal police investigation of criminal negligence; handled by state law enforcement.", "handoff": "Karnataka State Police / Karnataka Medical Council"},
            {"area": "Civil Monetary Compensation Claims", "desc": "Consumer court financial damages litigations; out of scope for administrative redressal.", "handoff": "District Consumer Disputes Redressal Commission"}
        ],
        "actors": [
            {"id": "ACT-WF19-01", "type": "Human", "name": "Citizen / Complainant", "responsibilities": "Submits complaint, selects category, provides narrative details or voice clip, receives ticket ID.", "permissions": "Grievance Create, Status Check, Satisfaction Rating", "failure_duty": "Declares illiteracy; dictates complaint verbally to reception clerk.", "inputs": "Personal experience, receipt token, evidence photos", "decisions": "Determines whether to lodge complaint anonymously or with contact details.", "outputs": "Submitted grievance ticket", "recovery": "Checks status using tracking reference code."},
            {"id": "ACT-WF19-02", "type": "Human", "name": "Clinic Coordinator / Medical Officer", "responsibilities": "Investigates grievance, interviews staff, reviews logs, formulates corrective action, marks resolved.", "permissions": "Grievance Investigate, Status Update, Corrective Action Commit", "failure_duty": "Refers unresolved grievance to Zonal Health Officer if beyond clinic authority.", "inputs": "Grievance ticket, clinic audit logs, staff statements", "decisions": "Determines validity of complaint and appropriate corrective action.", "outputs": "Investigation report, resolution notice", "recovery": "Re-opens investigation if citizen expresses dissatisfaction with outcome."}
        ],
        "personas": [
            {"id": "PERSONA-007", "name": "Shantamma", "role": "Elderly Patient", "env": "Clinic exit area; waited 50 minutes and found blood pressure medicine was out of stock.", "goals": "Voice frustration without getting in trouble with the doctor.", "pain_points": "Fear of retaliation if she complains publicly.", "adaptations": "Option for confidential voice recording in Kannada at the exit kiosk with no name required."},
            {"id": "PERSONA-006", "name": "Dr. Savitha Murthy", "role": "BBMP Zonal Health Officer", "env": "Zonal municipal health office overseeing 12 Namma Clinics.", "goals": "Spot clinic-level supply chain bottlenecks and staffing shortages through aggregate complaint trends.", "pain_points": "Delayed paper reports reaching her desk weeks after an incident.", "adaptations": "Real-time zonal dashboard showing heat-map of grievances by category and SLA breach status."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-006", "title": "Clinic Coordinator", "read": "Clinic Grievances", "create": "Investigation Note", "update": "Ticket Status", "delete": "None", "override": "None", "signoff": "Level 1 Resolution Signoff"},
            {"role": "ROLE-005", "title": "Zonal Health Officer", "read": "All Zonal Grievances", "create": "Administrative Action", "update": "Escalated Tickets", "delete": "None", "override": "Zonal Decision Override", "signoff": "Final Redressal Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF19-01", "desc": "Grievance intake channel (Kiosk / Web / Helpline) active and connected to edge or cloud ledger.", "check": "grievance_service.status == 'ONLINE'", "on_fail": "Store complaint in local offline SQLite queue with signed cryptographic hash."},
            {"id": "PRE-WF19-02", "desc": "Designated grievance redressal officer assigned in clinic directory.", "check": "clinic.gro_assigned == TRUE", "on_fail": "Default grievance routing to BBMP Zonal Health Office."}
        ],
        "triggers": [
            {"id": "TRIG-WF19-01", "class": "Citizen Action", "event": "Citizen taps 'File Feedback / Complaint' on clinic kiosk or scans poster QR code", "source": "Kiosk / Mobile Web UI", "payload": "{ clinic_id: 'NC-W085', channel: 'QR_CODE' }", "latency": "< 100ms to open form"}
        ],
        "inputs": [
            {"name": "category", "type": "Enum(WAIT_TIME, STOCKOUT, STAFF_BEHAVIOR, HYGIENE, BILLING_ERROR, OTHER)", "req": "Mandatory", "source": "Citizen Selection", "val": "Defined category", "priv": "Operational", "enc": "Plaintext", "ex": "STOCKOUT", "on_err": "Default to OTHER"},
            {"name": "description", "type": "Text", "req": "Mandatory", "source": "Citizen Entry", "val": "Narrative text or recorded audio clip", "priv": "Restricted", "enc": "Encrypted at rest", "ex": "Amlodipine 5mg was not available at pharmacy counter", "on_err": "Require minimum 10 characters description"}
        ],
        "outputs": {
            "success": [
                {"name": "Grievance Tracking Ticket", "desc": "Unique grievance reference number (e.g., GRV-2026-085-0012) and SMS tracking link.", "format": "SMS / Digital Receipt", "recipient": "Citizen Complainant"},
                {"name": "Investigation Work Item", "desc": "Actionable task routed to Clinic Coordinator with SLA countdown timer.", "format": "Internal Portal Task", "recipient": "Clinic Coordinator & ZHO Dashboard"}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor C as Citizen
    participant K as Kiosk / QR Web
    participant GS as Grievance Engine
    actor CO as Clinic Coordinator
    actor ZHO as Zonal Health Officer
    C->>K: 1. Scan QR Code at Exit -> Select 'Medicine Stockout'
    K-->>C: 2. Display: Enter details & mobile number (Optional)
    C->>K: 3. Submit Complaint: 'No Amlodipine at counter'
    K->>GS: 4. Register Ticket GRV-2026-044
    GS-->>C: 5. SMS Sent: 'Your ticket GRV-044 is registered. SLA: 24h'
    GS->>CO: 6. Task Assigned: Investigate stockout at Ward 85
    Note over GS,CO: 48 Hours Elapsed - No Resolution
    GS->>ZHO: 7. SLA Breach Escalation to Zonal Health Officer!
    ZHO->>CO: 8. Order Emergency Stock Replenishment from Central Depot
    CO->>GS: 9. Mark Resolved: 'Stock replenished from Depot; Citizen notified'""",
        "activity_diagram": """flowchart TD
    Start([Citizen Initiates Feedback / Grievance]) --> ChooseChannel[Select Intake: Exit Kiosk, QR Poster, or Desk Form]
    ChooseChannel --> SelectCategory[Select Issue Category: Wait Time, Medicine Stockout, Behavior, Hygiene]
    SelectCategory --> EnterDetails[Provide Description / Record Kannada Voice Clip]
    EnterDetails --> AnonymityChoice{Choose Anonymous or Provide Mobile?}
    AnonymityChoice -- Anonymous --> SetAnonFlag[Mark Complainant Anonymous]
    AnonymityChoice -- Provide Mobile --> AttachPhone[Attach Phone for SMS Status Updates]
    SetAnonFlag --> SubmitTicket[Submit Ticket to Grievance Engine]
    AttachPhone --> SubmitTicket
    SubmitTicket --> GenerateTicketID[Mint Unique Ticket ID: GRV-YYYY-XXXX]
    GenerateTicketID --> SendSMSReceipt[Send SMS with Tracking Link & SLA Target]
    SendSMSReceipt --> RouteTicket[Route Ticket to Clinic Coordinator Dashboard]
    RouteTicket --> MonitorSLA{Coordinator Resolves within 48 Hours?}
    MonitorSLA -- Yes --> EnterCAPA[Coordinator Documents Corrective Action]
    MonitorSLA -- No / SLA Breached --> EscalateZHO[Escalate Ticket to BBMP Zonal Health Officer]
    EscalateZHO --> ZonalIntervention[Zonal Officer Investigates & Orders Resolution]
    ZonalIntervention --> EnterCAPA
    EnterCAPA --> CloseTicket[Mark Ticket Resolved & Push Kannada Resolution SMS]
    CloseTicket --> CitizenRating{Citizen Confirms Resolution?}
    CitizenRating -- Satisfied --> End([Grievance Closed Successfully])
    CitizenRating -- Unsatisfied --> ReopenTicket[Re-open Ticket for Zonal Review]
    ReopenTicket --> EscalateZHO""",
        "state_diagram": """stateDiagram-v2
    [*] --> LODGED
    LODGED --> UNDER_INVESTIGATION: Coordinator Reviews Ticket
    UNDER_INVESTIGATION --> RESOLVED_LEVEL1: Resolved within 24-48 Hours
    UNDER_INVESTIGATION --> ESCALATED_LEVEL2: 48h SLA Breached
    ESCALATED_LEVEL2 --> RESOLVED_LEVEL2: Zonal Officer Resolves Ticket
    RESOLVED_LEVEL1 --> CITIZEN_VERIFIED: Citizen Approves Outcome
    RESOLVED_LEVEL2 --> CITIZEN_VERIFIED: Citizen Approves Outcome
    RESOLVED_LEVEL1 --> REOPENED: Citizen Dissatisfied
    REOPENED --> ESCALATED_LEVEL2
    CITIZEN_VERIFIED --> CLOSED: Final Archival
    CLOSED --> [*]"""
    }

    # =========================================================================
    # WF-020: Audit Trail Workflow
    # =========================================================================
    m20 = WORKFLOW_MAP["WF-020"]
    specs["WF-020"] = {
        "id": "WF-020", "num": "20", "name": m20["name"], "domain": m20["domain"],
        "exec_summary": {
            "purpose": "Implements an immutable, append-only cryptographic event ledger for every state transition, Protected Health Information (PHI) access, clinical prescription signature, emergency override, and administrative change across the Namma Clinic platform. Constructs SHA-256 Merkle tree verification checkpoints, triggers instant alerts upon hash chain disruption, and exports verifiable compliance bundles under the Digital Personal Data Protection (DPDP) Act 2023 and ISO 27001.",
            "rationale": "Healthcare records are frequent targets of unauthorized tampering, illicit snooping, and forensic denial. A tamper-evident cryptographic audit trail ensures complete non-repudiation, statutory regulatory compliance, and rapid forensic investigation of data breaches.",
            "clinical_impact": "Protects patient confidentiality by deterring unauthorized chart viewing; guarantees the unalterable integrity of diagnostic records and prescription authoring.",
            "system_impact": "Embeds cryptographic hashing (HMAC-SHA256) into local SQLite write pipelines; anchors periodic Merkle roots to central immutable cloud storage; and operates independently of application runtime state.",
            "risk_profile": "Storage exhaustion from verbose audit logging; local database corruption breaking hash verification; and administrative key compromise."
        },
        "objectives": [
            {"id": "OBJ-WF20-01", "title": "Zero-Overhead Audit Logging", "desc": "Commit cryptographic audit event record in < 5.0 milliseconds without degrading UI responsiveness.", "metric": "Audit Commit Overhead < 5.0ms", "verification": "Database write benchmark telemetry"},
            {"id": "OBJ-WF20-02", "title": "Cryptographic Hash Chain Integrity", "desc": "Maintain 100% mathematical continuity of SHA-256 chained hash blocks across all local transactions.", "metric": "Hash Chain Discontinuity = 0", "verification": "Nightly cryptographic ledger verification scan"},
            {"id": "OBJ-WF20-03", "title": "Instant Tamper Detection", "desc": "Trigger security alarm within 10 seconds of detecting unauthorized modification or record deletion.", "metric": "Tamper Alarm Latency < 10s", "verification": "Simulated unauthorized database modification test"},
            {"id": "OBJ-WF20-04", "title": "Statutory Retention Compliance", "desc": "Enforce 7-year immutable retention policy for all clinical and administrative audit event entries.", "metric": "Retention Policy Conformance = 100%", "verification": "Storage tier policy inspection"}
        ],
        "in_scope": [
            {"area": "Clinical Event Auditing", "desc": "Every view, creation, update, or export of patient clinical notes, diagnoses, prescriptions, and lab values."},
            {"area": "Administrative Event Auditing", "desc": "Staff logins, MFA challenges, permission changes, system configuration updates, and shift closures."},
            {"area": "Emergency Override Logging", "desc": "Break-glass emergency consent bypass and triage preemption event capture with mandatory justification."},
            {"area": "Cryptographic Hash Chaining", "desc": "Linking each audit record to the preceding record hash via HMAC-SHA256 with node-specific salt."}
        ],
        "out_of_scope": [
            {"area": "Operating System Kernel Syscall Auditing", "desc": "Host Linux OS kernel syscall tracing; managed by OS-level auditd / SELinux.", "handoff": "Host OS Security Layer"},
            {"area": "Physical CCTV Surveillance Video", "desc": "Physical facility security camera recording; managed by BBMP Facility Security.", "handoff": "BBMP Physical Security System"}
        ],
        "actors": [
            {"id": "ACT-WF20-01", "type": "System", "name": "Cryptographic Audit Engine", "responsibilities": "Intercepts mutations, computes SHA-256 hash chains, writes append-only records, computes Merkle roots.", "permissions": "Audit Write-Only, Hash Chain Compute, Tamper Alarm Trigger", "failure_duty": "Halts system state mutations if audit database is full or write fails.", "inputs": "Application state mutation events, actor claims, timestamps", "decisions": "Validates hash chain continuity; detects anomalous access patterns.", "outputs": "Immutable audit records, Merkle verification proofs", "recovery": "Quarantines corrupted blocks and alerts Security Officer."},
            {"id": "ACT-WF20-02", "type": "Human", "name": "Data Protection Officer (DPO)", "responsibilities": "Conducts monthly security audits, reviews unauthorized access alerts, signs compliance certificates.", "permissions": "Audit Read-Only, Forensic Query, Compliance Export", "failure_duty": "Reports confirmed data breaches to Data Protection Board of India within 72 hours.", "inputs": "Audit reports, anomaly alerts, forensic queries", "decisions": "Determines whether anomalous access constitutes a reportable breach.", "outputs": "Signed compliance reports, breach notifications", "recovery": "Executes incident response protocol."}
        ],
        "personas": [
            {"id": "PERSONA-006", "name": "Kavitha Reddy", "role": "Data Protection Officer", "env": "Central security operations monitoring 150 Namma Clinics.", "goals": "Verify that no staff member is snooping on neighbor medical records; pass DPDP compliance audits effortlessly.", "pain_points": "Parsing through gigabytes of raw unstructured server logs.", "adaptations": "Structured forensic dashboard with automated alerts for 'Staff viewing patient outside their ward' or 'Unusual midnight access'."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-006", "title": "Data Protection Officer", "read": "Complete Audit Ledger", "create": "Compliance Verification", "update": "None (WORM Log)", "delete": "None (Strictly Forbidden)", "override": "None", "signoff": "Audit Compliance Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF20-01", "desc": "Local cryptographic secure key enclave initialized and HMAC secret loaded.", "check": "audit_engine.secret_loaded == TRUE", "on_fail": "Halt node startup; security keys missing."},
            {"id": "PRE-WF20-02", "desc": "Dedicated append-only audit database table active with WAL mode enabled.", "check": "audit_store.status == 'READY'", "on_fail": "Fail-safe block: cannot execute mutations without audit trail."}
        ],
        "triggers": [
            {"id": "TRIG-WF20-01", "class": "System Interceptor", "event": "Any state mutation, data view, or authentication event in platform", "source": "API Middleware / Database Hook", "payload": "{ action: 'PATIENT_RECORD_VIEW', actor_id: 'DOC-002', record_id: 'PAT-001' }", "latency": "< 2ms to append audit log"}
        ],
        "inputs": [
            {"name": "event_type", "type": "String(32)", "req": "Mandatory", "source": "Application Context", "val": "Defined event taxonomy code", "priv": "Operational", "enc": "Plaintext", "ex": "ENCOUNTER_SIGNED", "on_err": "Reject unclassified event"},
            {"name": "actor_id", "type": "UUID", "req": "Mandatory", "source": "Session Token", "val": "Authenticated principal UUID", "priv": "Operational", "enc": "Plaintext", "ex": "d1e2f3a4-...", "on_err": "Flag unauthenticated action"}
        ],
        "outputs": {
            "success": [
                {"name": "Immutable Cryptographic Audit Record", "desc": "Appended record with monotonic sequence ID, SHA-256 previous hash, and HMAC signature.", "format": "WORM SQLite Row", "recipient": "Local Audit Database & Central Ledger"},
                {"name": "Merkle Tree Checkpoint Proof", "desc": "Periodic cryptographic root hash certifying ledger integrity at a point in time.", "format": "SHA-256 Merkle Proof JSON", "recipient": "Cloud Compliance Archive"}
            ],
            "failure": [
                {"name": "Tamper Alarm Security Alert", "desc": "High-priority security notification indicating broken hash chain or record modification.", "action": "Fires immediate webhook to Security Operations and locks compromised table."}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor U as Doctor
    participant API as Platform API Gateway
    participant AUD as Audit Engine
    participant DB as SQLite Audit WORM
    participant SEC as Security Dashboard
    U->>API: 1. Sign Encounter ENC-001
    API->>AUD: 2. Intercept Event: ENCOUNTER_SIGNED
    AUD->>DB: 3. Fetch PrevHash (0x7a8f...) & Seq (10482)
    AUD->>AUD: 4. Compute NewHash = HMAC-SHA256(PrevHash + EventData + Timestamp)
    AUD->>DB: 5. Append Row (Seq: 10483, Hash: NewHash)
    DB-->>AUD: 6. Write Confirmed (Commit < 2ms)
    AUD-->>API: 7. Audit Acknowledged -> Complete Request
    Note over DB,SEC: Nightly Integrity Scan (02:00 IST)
    AUD->>DB: 8. Verify all 10,483 chain hashes
    AUD->>SEC: 9. Emit Integrity Certificate: 100% Valid""",
        "activity_diagram": """flowchart TD
    Start([Application State Mutation Triggered]) --> InterceptEvent[Audit Middleware Intercepts Operation]
    InterceptEvent --> ExtractClaims[Extract Authenticated Actor, Role, IP, and Timestamp]
    ExtractClaims --> ReadLastHash[Read Previous Block Hash from Immutable Ledger]
    ReadLastHash --> AssembleBlock[Assemble Canonical JSON Payload]
    AssembleBlock --> ComputeHMAC[Compute HMAC-SHA256(PrevHash + Payload + Salt)]
    ComputeHMAC --> AppendWORM[Insert Row into Append-Only Audit Table]
    AppendWORM --> VerifyCommit{Write Succeeded to Disk?}
    VerifyCommit -- No --> PanicHalt[Trigger Fail-Safe: Halt Mutation & Alert Admin]
    VerifyCommit -- Yes --> CheckThreshold{Is 100th Transaction Checkpoint?}
    CheckThreshold -- Yes --> ComputeMerkleRoot[Compute Merkle Root & Push to Cloud Backup]
    CheckThreshold -- No --> CompleteAudit[Acknowledge Audit Commit]
    ComputeMerkleRoot --> CompleteAudit
    CompleteAudit --> End([Audit Complete & Application Resumes])""",
        "state_diagram": """stateDiagram-v2
    [*] --> EVENT_INTERCEPTED
    EVENT_INTERCEPTED --> HASH_COMPUTED: HMAC Calculated with Previous Block
    HASH_COMPUTED --> APPENDED_TO_WORM: Written to Append-Only Storage
    APPENDED_TO_WORM --> MERKLE_CHECKPOINTED: 100-Block Merkle Root Pushed
    APPENDED_TO_WORM --> TAMPER_DETECTED: Hash Verification Mismatch
    TAMPER_DETECTED --> SECURITY_LOCKED: Audit Table Locked & Alarm Fired
    MERKLE_CHECKPOINTED --> [*]"""
    }

    return specs

def write_group4_file():
    specs = get_group4_specs()
    print("Building Group 4 Workflows (WF-016 to WF-020)...")

    header = '''#!/usr/bin/env python3
"""
data_wf16_to_20.py
Clean, self-contained domain specifications for Workflows 16 to 20:
  - WF-016: Clinical Referral, Higher Center Escalation & Ambulance Transfer Workflow
  - WF-017: NCD Follow-Up Scheduling, Chronic Disease Recall & Defaulter Tracking Workflow
  - WF-018: Omnichannel Patient & Staff Notification, Alerting & Communication Workflow
  - WF-019: Citizen Grievance Redressal, Feedback & SLA Escalation Workflow
  - WF-020: Cryptographic Audit Trail, Immutable Logging & Tamper Detection Workflow

Exports:
  DATA_WF16_TO_20 (dict mapping 'WF-016'..'WF-020' to enriched 67-section workflow dicts)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_factory import build_workflow_object
from build_group4 import get_group4_specs

def get_group4_workflows():
    specs = get_group4_specs()
    return {wfid: build_workflow_object(spec) for wfid, spec in specs.items()}

if __name__ == "__main__":
    from workflow_generator import render_workflow_document
    from common import count_lines, find_duplicate_paragraphs
    print("Testing data_wf16_to_20.py...")
    wfs = get_group4_workflows()
    docs = {}
    for wfid, wf_data in wfs.items():
        doc = render_workflow_document(wf_data)
        docs[wfid] = doc
        counts = count_lines(doc)
        status = "PASS" if counts["substantive"] >= 2000 else "FAIL"
        print(f"  {wfid}: Total = {counts['total']}, Substantive = {counts['substantive']} [{status}]")

    dups = find_duplicate_paragraphs(docs, min_len=60)
    print(f"  Duplicate paragraphs within Group 4: {len(dups)}")
'''
    with open('scripts/workflows/data_wf16_to_20.py', 'w', encoding='utf-8') as f:
        f.write(header)
    print("Wrote scripts/workflows/data_wf16_to_20.py")

if __name__ == "__main__":
    write_group4_file()
