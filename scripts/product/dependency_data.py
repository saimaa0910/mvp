#!/usr/bin/env python3
"""
dependency_data.py
Authoritative module dependency architecture, topological ordering,
and acyclic DAG definitions for the Namma Clinic Digital Health & Operations Platform (docs/04-product/).

Covers 30 Modules (MODULE-001 to MODULE-030) across 10 formal dependency categories:
- DEP-SECURITY-###
- DEP-BUSINESS-###
- DEP-WORKFLOW-###
- DEP-DATA-###
- DEP-OFFLINE-###
- DEP-SYNC-###
- DEP-ANALYTICS-###
- DEP-AI-###
- DEP-INTEGRATION-###
- DEP-OPERATIONAL-###
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_specs import MODULE_MAP

# -----------------------------------------------------------------------------
# MASTER MODULE DEPENDENCY ARCHITECTURE
# In clean DAG modeling:
# source_module (Consumer / Dependent) depends on target_module (Prerequisite / Provider)
# Every dependency indicates that target_module must be available for source_module to operate.
# -----------------------------------------------------------------------------

RAW_DEPENDENCIES = [
    # -------------------------------------------------------------------------
    # 1. SECURITY & ACCESS CONTROL DEPENDENCIES (DEP-SECURITY-001 to 012)
    # -------------------------------------------------------------------------
    ("DEP-SECURITY-001", "Security & Auth", "MODULE-004", "MODULE-001", "FEATURE-019", "FEATURE-001", "Hard Technical Dependency",
     "Security hardening and session governance requires Staff IAM credentials and cryptographic token issuance.",
     True, "P0 - Critical", "Session tokens cannot be validated; all authenticated endpoints fail closed.",
     "Emergency local console login via hardware serial port.", "Auth service issues valid RS256 JWT.",
     "ROLE-011", "Any user session creation.", "Staff IAM service boot.", "SECR-002", "WF-002", "REL-00",
     "Session token expiration during active clinical consultation.", "Sliding-window token renewal with 15-minute grace period."),

    ("DEP-SECURITY-002", "Security & Auth", "MODULE-026", "MODULE-001", "FEATURE-151", "FEATURE-001", "Administrative Dependency",
     "Multi-clinic tenant administration requires super-administrator cryptographic role claims.",
     True, "P0 - Critical", "Tenant configuration cannot be modified; clinic creation locked.",
     "Read-only cached tenant configuration.", "IAM verifies super-admin entitlement.",
     "ROLE-001", "Tenant provisioning.", "IAM deployment.", "SECR-001", "WF-001", "REL-00",
     "Privilege escalation on municipal configuration.", "Dual-key authorization required for tenant modification."),

    ("DEP-SECURITY-003", "Security & Auth", "MODULE-021", "MODULE-001", "FEATURE-121", "FEATURE-001", "Security Audit Precedence",
     "Cryptographic WORM audit ledger requires authenticated user principal ID to sign tamper-evident audit logs.",
     True, "P0 - Critical", "Audit events generated without actor attribution, violating ISO 27799.",
     "Queue audit event with ANONYMOUS tag and raise critical security alert.", "User principal ID resolved from token.",
     "ROLE-011", "Any system mutation.", "Staff session validation.", "SECR-020", "WF-020", "REL-00",
     "Unattributed mutations during auth failure.", "Reject mutation if principal cannot be identified."),

    ("DEP-SECURITY-004", "Security & Auth", "MODULE-005", "MODULE-001", "FEATURE-025", "FEATURE-001", "Role Entitlement Boundary",
     "Patient demographic intake requires Front Desk Clerk or Staff Nurse role credentials.",
     True, "P0 - Critical", "Intake workstation locked against citizen registration.",
     "Emergency paper triage slip with post-hoc registration entry.", "Valid staff role claim presented.",
     "ROLE-019", "Citizen intake.", "Front desk staff login.", "SECR-003", "WF-003", "REL-01",
     "Staff credentials expire during morning clinic rush.", "2-hour offline shift grace period on local edge node."),

    ("DEP-SECURITY-005", "Security & Auth", "MODULE-009", "MODULE-001", "FEATURE-049", "FEATURE-001", "Clinical Triage Authority",
     "Nurse triage recording requires registered Staff Nurse credentials with clinical nursing registration.",
     True, "P0 - Critical", "Triage station cannot commit acuity scores or vital signs.",
     "Paper vital chart entered retrospectively by supervising nurse.", "Active Nurse role claim verified.",
     "ROLE-016", "Vitals recording.", "Nurse login.", "SECR-008", "WF-010", "REL-01",
     "Temporary relief nurse without registered account.", "Supervisor fast-track credential delegation."),

    ("DEP-SECURITY-006", "Security & Auth", "MODULE-010", "MODULE-001", "FEATURE-055", "FEATURE-001", "Medical Prescribing Authority",
     "Doctor consultation and diagnosis entry strictly requires verified Medical Officer credentials with KMC registration.",
     True, "P0 - Critical", "Doctor consultation room locked; clinical SOAP notes blocked.",
     "Emergency paper clinical sheet co-signed within 24 hours.", "Medical Officer claim verified against state medical council.",
     "ROLE-015", "Consultation note creation.", "Doctor station login.", "SECR-009", "WF-011", "REL-01",
     "Revoked or suspended medical license.", "Nightly automated medical council registry synchronization."),

    ("DEP-SECURITY-007", "Security & Auth", "MODULE-012", "MODULE-001", "FEATURE-067", "FEATURE-001", "e-Prescribing Security Boundary",
     "Electronic prescription signing requires digital signature key bound to authenticated Medical Officer.",
     True, "P0 - Critical", "Prescription cannot be digitally sealed; pharmacy cannot dispense.",
     "Physically stamped and signed prescription slip.", "Cryptographic signature generated with HSM/Ed25519 token.",
     "ROLE-015", "Prescription sign-off.", "Doctor consult finalization.", "SECR-010", "WF-012", "REL-01",
     "Corrupted doctor digital certificate.", "Automated ephemeral key re-issuance via municipal PKI."),

    ("DEP-SECURITY-008", "Security & Auth", "MODULE-013", "MODULE-001", "FEATURE-073", "FEATURE-001", "Pharmacy Dispensing Boundary",
     "Pharmacy dispensing terminal requires licensed Pharmacist credentials with state pharmacy council registration.",
     True, "P0 - Critical", "Dispensary barcode scanner locked; drug packs cannot be decremented.",
     "Emergency nurse dispensing under direct written medical officer supervision.", "Pharmacist license verified.",
     "ROLE-017", "Barcode scan of medication pack.", "Pharmacist login.", "SECR-012", "WF-013", "REL-01",
     "Unlicensed staff attempting drug dispensing.", "Zero-tolerance system block on non-pharmacist accounts."),

    ("DEP-SECURITY-009", "Security & Auth", "MODULE-011", "MODULE-001", "FEATURE-061", "FEATURE-001", "Diagnostic Lab Authority",
     "Point-of-care lab test result entry requires certified Medical Laboratory Technologist (MLT) credentials.",
     True, "P0 - Critical", "Lab test results cannot be committed to patient EMR.",
     "Doctor direct entry for rapid malaria/dengue strip tests.", "Lab technician role verified.",
     "ROLE-018", "Diagnostic result commit.", "Lab tech login.", "SECR-011", "WF-015", "REL-01",
     "Lab staff shift turnover during emergency sample run.", "Dual-attestation handover protocol."),

    ("DEP-SECURITY-010", "Security & Auth", "MODULE-014", "MODULE-001", "FEATURE-079", "FEATURE-001", "Inventory Custody Boundary",
     "Pharmaceutical stock batch adjustments and stock receipts require authorized pharmacy custody claims.",
     True, "P1 - High", "Batch expiry adjustments locked.",
     "Physical stock count ledger signed manually.", "Inventory custodian claim verified.",
     "ROLE-017", "Batch stock adjustment.", "Staff shift start.", "SECR-013", "WF-016", "REL-01",
     "Unauthorized stock modification.", "Maker-checker approval for adjustments > 5 units."),

    # -------------------------------------------------------------------------
    # 2. BUSINESS & FACILITY TOPOLOGY DEPENDENCIES (DEP-BUSINESS-011 to 020)
    # -------------------------------------------------------------------------
    ("DEP-BUSINESS-011", "Business & Facility", "MODULE-005", "MODULE-002", "FEATURE-025", "FEATURE-007", "Facility Scoping Dependency",
     "Patient registration records must bind to a valid physical clinic facility in the BBMP master registry.",
     True, "P0 - Critical", "Patient file orphaned; clinic census report cannot attribute registration.",
     "Default to local edge appliance cached facility identifier.", "Facility ID verified in clinic registry.",
     "ROLE-019", "Registration submission.", "Clinic opening.", "OR-002", "WF-001", "REL-00",
     "Facility ID mismatch between edge server and cloud.", "Hardware MAC-to-facility cryptobinding."),

    ("DEP-BUSINESS-012", "Business & Facility", "MODULE-008", "MODULE-002", "FEATURE-043", "FEATURE-007", "Queue Service Boundary",
     "Queue token generation requires active room and counter definitions from facility master data.",
     True, "P0 - Critical", "Tokens cannot be mapped to Doctor, Nurse, or Pharmacy counters.",
     "Single sequential general emergency queue.", "Room and counter mapping loaded into memory.",
     "ROLE-019", "Token minting.", "Morning counter setup.", "OR-005", "WF-004", "REL-01",
     "Doctor room reassignment mid-day.", "Dynamic counter re-routing via Front Desk console."),

    ("DEP-BUSINESS-013", "Business & Facility", "MODULE-014", "MODULE-002", "FEATURE-079", "FEATURE-007", "Stock Location Dependency",
     "Clinic medication inventory must be allocated to a verified physical drug store within the clinic facility.",
     True, "P0 - Critical", "Inventory balances cannot be attributed; stock indents rejected.",
     "Quarantine incoming stock in transit buffer.", "Facility dispensary ID validated.",
     "ROLE-017", "Stock receipt.", "Store room initialization.", "OR-012", "WF-016", "REL-01",
     "Sub-dispensary cold room power outage.", "Emergency batch transfer to maternal ward refrigerator."),

    ("DEP-BUSINESS-014", "Business & Facility", "MODULE-017", "MODULE-002", "FEATURE-097", "FEATURE-007", "Referral Facility Routing",
     "Specialist referrals require target secondary/tertiary hospital codes from municipal health facility master.",
     True, "P0 - Critical", "Referral transfer slip cannot specify receiving facility.",
     "Generic print referral slip with emergency ambulance dispatch.", "Destination hospital code verified.",
     "ROLE-015", "Referral order finalization.", "Consultation triage.", "OR-015", "WF-017", "REL-01",
     "Hospital specialty ward full / diversion.", "Real-time bed availability check via central referral gateway."),

    ("DEP-BUSINESS-015", "Business & Facility", "MODULE-028", "MODULE-002", "FEATURE-163", "FEATURE-007", "Facility Operations Scoping",
     "Facility operations and helpdesk tickets must attach to specific clinic asset and workstation IDs.",
     False, "P2 - Medium", "Trouble ticket logged without workstation hardware context.",
     "Manual text entry of workstation serial number.", "Workstation asset tagged to clinic.",
     "ROLE-023", "Helpdesk ticket creation.", "Asset onboarding.", "OR-028", "WF-025", "REL-02",
     "Unregistered replacement printer deployed.", "Field technician asset scan and barcode bind."),

    # -------------------------------------------------------------------------
    # 3. CLINICAL & PATIENT WORKFLOW DEPENDENCIES (DEP-WORKFLOW-021 to 040)
    # -------------------------------------------------------------------------
    ("DEP-WORKFLOW-021", "Workflow Precedence", "MODULE-006", "MODULE-005", "FEATURE-031", "FEATURE-025", "Identity Binding Dependency",
     "ABHA national health ID linking requires an existing registered patient profile record.",
     True, "P0 - Critical", "ABHA verification token cannot bind to local demographic record.",
     "Complete local registration first, queue ABHA linking for later.", "Local patient UUID generated.",
     "ROLE-019", "ABHA OTP verification.", "Demographic save.", "FR-004", "WF-005", "REL-01",
     "ABHA OTP timeout during busy clinic queue.", "Allow registration completion; prompt ABHA link at consult."),

    ("DEP-WORKFLOW-022", "Workflow Precedence", "MODULE-007", "MODULE-005", "FEATURE-037", "FEATURE-025", "Consent Attachment Dependency",
     "Digital privacy consent artifact must attach to an active registered citizen identity.",
     True, "P0 - Critical", "Consent recorded without patient subject; legally void under DPDP Act 2023.",
     "Paper consent form signed and scanned.", "Patient record exists with national/local ID.",
     "ROLE-019", "Consent capture modal.", "Patient intake confirmation.", "PRIV-001", "WF-006", "REL-01",
     "Citizen declines consent for analytics sharing.", "System sets strict processing scope to care delivery only."),

    ("DEP-WORKFLOW-023", "Workflow Precedence", "MODULE-008", "MODULE-007", "FEATURE-043", "FEATURE-037", "Consent Pre-Condition for Queue",
     "Token generation requires validated consent for primary health outpatient consultation.",
     True, "P0 - Critical", "Patient enters clinical waiting hall without legal processing consent.",
     "Emergency trauma bypass with implied consent flag.", "Signed consent artifact recorded in local database.",
     "ROLE-019", "Queue token printing.", "Consent signoff.", "PRIV-002", "WF-007", "REL-01",
     "Illiterate citizen unable to sign digital pad.", "Witnessed thumbprint or verbal consent co-signed by nurse."),

    ("DEP-WORKFLOW-024", "Workflow Precedence", "MODULE-009", "MODULE-008", "FEATURE-049", "FEATURE-043", "Queue Intake for Triage",
     "Nurse vitals recording requires active queue token number to call patient into triage booth.",
     True, "P0 - Critical", "Nurse cannot associate vital signs with patient encounter queue.",
     "Manual token lookup by patient phone number or name.", "Token in STATUS_WAITING_TRIAGE.",
     "ROLE-016", "Nurse station 'Call Next' button.", "Token issuance at front desk.", "FR-012", "WF-010", "REL-01",
     "Patient skipped triage and walked into doctor room.", "Doctor console rejects encounter until triage completed."),

    ("DEP-WORKFLOW-025", "Workflow Precedence", "MODULE-010", "MODULE-009", "FEATURE-055", "FEATURE-049", "Clinical Triage Precedence",
     "Doctor consultation requires completed nurse triage with vital signs (BP, Pulse, Temp, SpO2) and acuity color.",
     True, "P0 - Critical", "Doctor examines patient without baseline vital parameters; clinical risk.",
     "Emergency doctor triage override with mandatory clinical reason.", "Triage record committed in local database.",
     "ROLE-015", "Doctor opening consultation file.", "Nurse triage finalization.", "CR-002", "WF-011", "REL-01",
     "Severe tachycardia / danger sign identified.", "System triggers instant Red-Flag audio alarm in doctor room."),

    ("DEP-WORKFLOW-026", "Workflow Precedence", "MODULE-011", "MODULE-010", "FEATURE-061", "FEATURE-055", "Diagnostic Order Precedence",
     "Point-of-care laboratory test ordering requires active doctor consultation encounter.",
     True, "P0 - Critical", "Diagnostic tests performed without clinical indication or physician order.",
     "Emergency standing nurse order for blood glucose / hemoglobin in trauma.", "Encounter open in DOCTOR_ACTIVE state.",
     "ROLE-015", "Lab test order selection.", "Doctor clinical note draft.", "FR-022", "WF-015", "REL-01",
     "Rapid dengue test requested by citizen.", "Citizen advised to see doctor first for clinical evaluation."),

    ("DEP-WORKFLOW-027", "Workflow Precedence", "MODULE-012", "MODULE-010", "FEATURE-067", "FEATURE-055", "Prescription Encounter Dependency",
     "e-Prescription authoring requires active doctor encounter with at least one provisional diagnosis.",
     True, "P0 - Critical", "Prescription issued without diagnostic justification; regulatory violation.",
     "Emergency antidote prescription with provisional 'Acute Poisoning' code.", "ICD-10 / SNOMED CT diagnosis code entered.",
     "ROLE-015", "Medication selection in e-Rx pad.", "Diagnosis entry.", "CR-005", "WF-012", "REL-01",
     "Doctor prescribing off-label drug.", "System requires mandatory clinical justification text."),

    ("DEP-WORKFLOW-028", "Workflow Precedence", "MODULE-013", "MODULE-012", "FEATURE-073", "FEATURE-067", "Dispensing Order Precedence",
     "Pharmacy dispensing requires a cryptographically signed electronic prescription from the consulting doctor.",
     True, "P0 - Critical", "Dispensary hands out Schedule H drugs without valid doctor prescription.",
     "Emergency OTC oral rehydration salts / paracetamol fast-track.", "Prescription in STATUS_ISSUED.",
     "ROLE-017", "Prescription scan at pharmacy counter.", "Doctor digital signature.", "CR-008", "WF-013", "REL-01",
     "Doctor modified prescription after patient walked to pharmacy.", "Real-time queue update invalidates old token."),

    ("DEP-WORKFLOW-029", "Workflow Precedence", "MODULE-017", "MODULE-010", "FEATURE-097", "FEATURE-055", "Referral Clinical Context",
     "Specialist referral creation requires physician encounter note with reason for referral and clinical summary.",
     True, "P0 - Critical", "Secondary hospital receives patient without clinical summary.",
     "Emergency verbal telephone handover to 108 ambulance paramedic.", "Doctor encounter signed.",
     "ROLE-015", "Referral form submit.", "Encounter sign-off.", "FR-035", "WF-017", "REL-01",
     "Immediate life-threatening emergency (myocardial infarction).", "One-click 108 Emergency Transit trigger."),

    ("DEP-WORKFLOW-030", "Workflow Precedence", "MODULE-018", "MODULE-010", "FEATURE-103", "FEATURE-055", "NCD Follow-up Enrollment",
     "Longitudinal chronic care follow-up requires clinical encounter diagnosing hypertension, diabetes, or asthma.",
     False, "P1 - High", "Patient missing from municipal chronic care register; missed medication refills.",
     "Nurse opportunistic screening at front desk.", "Chronic condition tagged in diagnosis list.",
     "ROLE-015", "Follow-up schedule date commit.", "Clinical diagnosis entry.", "FR-038", "WF-018", "REL-02",
     "Patient relocated to different municipal ward.", "Inter-clinic care registry transfer protocol."),

    # -------------------------------------------------------------------------
    # 4. DATA OBJECT & INVENTORY DEPENDENCIES (DEP-DATA-031 to 040)
    # -------------------------------------------------------------------------
    ("DEP-DATA-031", "Data & Master Reference", "MODULE-012", "MODULE-016", "FEATURE-067", "FEATURE-091", "Formulary Item Dependency",
     "Electronic prescription drug picker binds strictly to active medicines in the Essential Medicine List (EML).",
     True, "P0 - Critical", "Doctors prescribe unapproved or non-formulary commercial brand medications.",
     "Special non-formulary request with justification.", "Drug item active in formulary catalog.",
     "ROLE-015", "Prescription search bar typing.", "Formulary publishing.", "CR-010", "WF-012", "REL-01",
     "Formulary drug discontinued by state depot.", "Immediate system de-activation with alternative suggestion."),

    ("DEP-DATA-032", "Data & Master Reference", "MODULE-013", "MODULE-014", "FEATURE-073", "FEATURE-079", "Inventory Depletion Dependency",
     "Dispensing a drug pack requires an active batch with positive stock balance and valid expiry date.",
     True, "P0 - Critical", "Pharmacist attempts to dispense expired stock or negative stock occurs.",
     "Quarantine batch; switch to secondary active batch.", "Batch quantity > 0 and Expiry Date > Current Date.",
     "ROLE-017", "2D barcode scan of physical pack.", "Stock batch receipt.", "OR-014", "WF-013", "REL-01",
     "Barcode unreadable due to ink smear.", "Manual batch selection with mandatory lot number confirmation."),

    ("DEP-DATA-033", "Data & Master Reference", "MODULE-015", "MODULE-014", "FEATURE-085", "FEATURE-079", "Indent Calculation Dependency",
     "Automated stock replenishment indents depend on real-time consumption rates and reorder point levels in clinic inventory.",
     False, "P1 - High", "Indents fail to calculate automatic replenishment; stock-out risk.",
     "Manual stock indent creation by pharmacist.", "Daily inventory reconciliation committed.",
     "ROLE-017", "Indent generation cron.", "Daily dispensary close.", "OR-016", "WF-016", "REL-01",
     "Sudden disease outbreak doubles daily paracetamol consumption.", "Manual emergency indent override."),

    ("DEP-DATA-034", "Data & Master Reference", "MODULE-019", "MODULE-008", "FEATURE-109", "FEATURE-043", "Citizen Notification Token Binding",
     "SMS and WhatsApp queue status alerts require active token ID and valid mobile number from patient profile.",
     False, "P2 - Medium", "Citizen does not receive waiting hall delay alerts.",
     "Audio loudspeaker announcement in clinic waiting room.", "Token minting emits notification event.",
     "ROLE-019", "Token printing.", "Patient registration.", "FR-042", "WF-019", "REL-01",
     "Invalid or non-existent mobile phone number.", "Skip SMS; rely on physical printed token slip."),

    ("DEP-DATA-035", "Data & Master Reference", "MODULE-020", "MODULE-005", "FEATURE-115", "FEATURE-025", "Citizen Grievance Patient Context",
     "Citizen grievance logging references registered citizen ID or anonymous tracking token.",
     False, "P2 - Medium", "Grievance cannot be tracked or linked to clinic encounter.",
     "Anonymous paper grievance drop-box entry.", "Citizen record retrieved or anonymous ticket minted.",
     "ROLE-019", "Grievance filing.", "Front desk interaction.", "OR-020", "WF-021", "REL-02",
     "Citizen refuses to provide name or contact.", "System provisions anonymous grievance tracking ID."),

    # -------------------------------------------------------------------------
    # 5. OFFLINE EDGE & DISTRIBUTED MESH DEPENDENCIES (DEP-OFFLINE-041 to 050)
    # -------------------------------------------------------------------------
    ("DEP-OFFLINE-041", "Offline & Edge Substrate", "MODULE-005", "MODULE-024", "FEATURE-025", "FEATURE-139", "Edge Persistence Substrate",
     "Patient registration operates autonomously on local edge SQLite engine during broadband fiber cuts.",
     True, "P0 - Critical", "Clinic operations halt during municipal telecom outage.",
     "Offline local database transaction with outbound sync queue.", "Edge node SQLite engine healthy.",
     "ROLE-024", "Citizen registration.", "Edge appliance boot.", "OFF-001", "WF-022", "REL-01",
     "Edge mini-server SSD failure.", "Peer workstation SQLite database failover."),

    ("DEP-OFFLINE-042", "Offline & Edge Substrate", "MODULE-009", "MODULE-024", "FEATURE-049", "FEATURE-139", "Edge Triage Persistence",
     "Nurse triage and emergency danger sign alerts commit immediately to local edge node memory and disk.",
     True, "P0 - Critical", "Triage delays while waiting for cloud HTTP roundtrip.",
     "Local edge bus broadcast to doctor room via LAN.", "Local edge node reachable over Wi-Fi/Ethernet.",
     "ROLE-016", "Acuity score commit.", "Edge network active.", "OFF-002", "WF-022", "REL-01",
     "Local Wi-Fi router reboot.", "Nurse tablet stores vitals in local IndexedDB until LAN restores."),

    ("DEP-OFFLINE-043", "Offline & Edge Substrate", "MODULE-010", "MODULE-024", "FEATURE-055", "FEATURE-139", "Edge Clinical Persistence",
     "Doctor consultation SOAP notes persist to local edge appliance with guaranteed zero-loss transaction commit.",
     True, "P0 - Critical", "Doctor clinical documentation lost on browser crash or cloud timeout.",
     "Local SQLite write-ahead-log (WAL) commit < 20ms.", "Local disk storage has > 2GB free space.",
     "ROLE-015", "Consultation note save.", "Edge disk check.", "OFF-003", "WF-022", "REL-01",
     "Local edge node sudden power cut.", "Workstation mini-UPS maintains 30-minute operational buffer."),

    ("DEP-OFFLINE-044", "Offline & Edge Substrate", "MODULE-013", "MODULE-024", "FEATURE-073", "FEATURE-139", "Edge Dispensing Execution",
     "Pharmacy barcode verification and inventory deduction execute locally on edge server without cloud reliance.",
     True, "P0 - Critical", "Medicine dispensing blocked when Internet is down; patients leave without drugs.",
     "Local batch stock balance checked and decremented in SQLite.", "Dispensary terminal connected to edge.",
     "ROLE-017", "Pack scan.", "Local inventory table loaded.", "OFF-004", "WF-022", "REL-01",
     "Concurrent dispensing at two counters for last pack.", "SQLite immediate transaction lock on batch record."),

    ("DEP-OFFLINE-045", "Offline & Edge Substrate", "MODULE-008", "MODULE-024", "FEATURE-043", "FEATURE-139", "Edge Queue Orchestration",
     "Queue token minting and waiting hall display updates run entirely over local LAN via MQTT/WebSocket broker.",
     True, "P0 - Critical", "Waiting hall display goes black during Internet outage.",
     "Local MQTT broker on edge server dispatches token calls to TV screen.", "Edge node local IP broadcast functional.",
     "ROLE-019", "Doctor calls next token.", "Display initialization.", "OFF-005", "WF-022", "REL-01",
     "Waiting hall TV HDMI disconnect.", "Front desk verbal announcement with printed slip backup."),

    # -------------------------------------------------------------------------
    # 6. AI & CLINICAL DECISION SUPPORT DEPENDENCIES (DEP-AI-051 to 055)
    # -------------------------------------------------------------------------
    ("DEP-AI-051", "AI & Decision Support", "MODULE-010", "MODULE-023", "FEATURE-055", "FEATURE-133", "CDSS Clinical Diagnostic Support",
     "Doctor consultation interface consumes real-time CDSS diagnostic guidance and red-flag danger alerts.",
     False, "P1 - High", "Doctor works without automated diagnostic checks and pediatric guideline prompts.",
     "Manual consultation proceeding with standard clinical judgment.", "CDSS rule engine initialized in edge cache.",
     "ROLE-015", "Entering chief complaint and symptoms.", "Consultation start.", "AIR-001", "WF-011", "REL-01",
     "CDSS engine takes > 500ms to evaluate rules.", "Asynchronous background evaluation; UI non-blocking."),

    ("DEP-AI-052", "AI & Decision Support", "MODULE-012", "MODULE-023", "FEATURE-067", "FEATURE-133", "CDSS Drug Safety Validation",
     "Electronic prescription authoring triggers CDSS drug-drug, drug-allergy, and dose contraindication safety checks.",
     True, "P0 - Critical", "High-risk drug interaction prescribed without automated clinical safety barrier.",
     "Doctor manual safety check; system requires explicit confirmation.", "CDSS drug interaction matrix active.",
     "ROLE-015", "Adding medication to prescription.", "Drug selection.", "AIR-002", "WF-012", "REL-01",
     "False positive allergy warning.", "Doctor clinical override with documented medical justification."),

    ("DEP-AI-053", "AI & Decision Support", "MODULE-023", "MODULE-016", "FEATURE-133", "FEATURE-091", "CDSS Formulary Ontology",
     "CDSS decision rules and drug interaction matrices bind to standard chemical entities in the medication formulary.",
     True, "P0 - Critical", "Safety rules fail to match newly formulated drug items.",
     "Fallback to class-level contraindication rules.", "Formulary entities mapped to RxNorm / SNOMED CT.",
     "ROLE-012", "Formulary update.", "CDSS model compilation.", "AIR-003", "WF-012", "REL-01",
     "Unmapped generic drug in municipal supply.", "Quarantine drug from e-prescribing until mapped."),

    # -------------------------------------------------------------------------
    # 7. ANALYTICS & STATUTORY REPORTING DEPENDENCIES (DEP-ANALYTICS-061 to 070)
    # -------------------------------------------------------------------------
    ("DEP-ANALYTICS-061", "Analytics & Reporting", "MODULE-022", "MODULE-005", "FEATURE-127", "FEATURE-025", "Demographic Ingestion Dependency",
     "Municipal epidemiological analytics consumes daily registered citizen demographics for age/gender stratification.",
     False, "P1 - High", "Public health dashboards missing demographic denominators.",
     "Use historical demographic distribution baseline.", "Demographic events synced to DuckDB warehouse.",
     "ROLE-013", "Epidemiological report generation.", "Day-end sync.", "ANL-001", "WF-023", "REL-01",
     "Incomplete demographic fields (e.g. ward missing).", "Tag records as 'Ward Unassigned' in analytics cube."),

    ("DEP-ANALYTICS-062", "Analytics & Reporting", "MODULE-022", "MODULE-009", "FEATURE-127", "FEATURE-049", "Syndromic Triage Analytics",
     "Disease surveillance analytics tracks fever, cough, diarrhea, and rash clusters from nurse triage records.",
     False, "P1 - High", "Outbreak detection algorithms blind to frontline community symptom surges.",
     "Retrospective outbreak verification via doctor diagnosis.", "Triage vital counters aggregated in analytics cube.",
     "ROLE-013", "Syndromic alert generation.", "Hourly telemetry rollup.", "ANL-002", "WF-023", "REL-01",
     "Single clinic reporting 50 fever cases due to school event.", "Spatial cluster verification across multiple clinics."),

    ("DEP-ANALYTICS-063", "Analytics & Reporting", "MODULE-022", "MODULE-010", "FEATURE-127", "FEATURE-055", "Clinical Diagnosis Analytics",
     "Municipal disease incidence tracking aggregates ICD-10 diagnostic codes from finalized doctor consultations.",
     False, "P1 - High", "Statutory municipal morbidity reports incomplete.",
     "Doctor weekly manual communicable disease declaration.", "Encounter diagnoses transformed to analytical marts.",
     "ROLE-013", "Weekly epidemiological bulletin.", "Nightly ETL pipeline.", "ANL-003", "WF-023", "REL-01",
     "Doctors assigning non-specific 'Other Fever' code.", "Clinical training prompt on specific ICD-10 coding."),

    ("DEP-ANALYTICS-064", "Analytics & Reporting", "MODULE-025", "MODULE-010", "FEATURE-145", "FEATURE-055", "HMIS Outpatient Data Pipeline",
     "State Health Management Information System (HMIS) export aggregates OPD attendance, maternal care, and child visits.",
     False, "P1 - High", "Municipal clinics non-compliant with state monthly reporting mandates.",
     "Manual data entry into state HMIS portal by clinic coordinator.", "HMIS monthly indicator query runs on data warehouse.",
     "ROLE-021", "State HMIS monthly export.", "Month-end calendar trigger.", "REP-001", "WF-024", "REL-01",
     "State HMIS portal schema change.", "Data transformation mapper update via config flag."),

    ("DEP-ANALYTICS-065", "Analytics & Reporting", "MODULE-025", "MODULE-006", "FEATURE-145", "FEATURE-031", "ABDM M1/M2 Gateway Interface",
     "National Health Interoperability gateway pushes FHIR R4 diagnostic bundles bound to verified ABHA IDs.",
     False, "P1 - High", "Consultation records cannot be federated to citizen national health locker.",
     "Store FHIR bundle in outbound queue; retry when ABDM gateway responds.", "ABHA address verified and active.",
     "ROLE-020", "Consultation finalization.", "Citizen ABHA link.", "INT-001", "WF-024", "REL-01",
     "National ABDM server latency > 5s.", "Asynchronous message queue with exponential backoff."),

    ("DEP-ANALYTICS-066", "Analytics & Reporting", "MODULE-027", "MODULE-009", "FEATURE-157", "FEATURE-049", "Emergency Command Center Alert",
     "Municipal disaster command center triggers automated notifications upon detecting cluster of red-flag danger triage cases.",
     True, "P0 - Critical", "Mass-casualty incident or toxic contamination event goes undetected at municipal level.",
     "Telephone emergency hotline call from Medical Superintendent.", "Red-flag triage event published to emergency bus.",
     "ROLE-002", "Triage alarm broadcast.", "Clinic triage execution.", "OR-027", "WF-010", "REL-01",
     "Accidental red-flag trigger by nurse.", "Supervisor cancellation within 3 minutes disables municipal alert."),

    ("DEP-ANALYTICS-067", "Analytics & Reporting", "MODULE-030", "MODULE-002", "FEATURE-175", "FEATURE-007", "Inter-Facility Routing",
     "Unified inter-facility communication routes messages using facility hierarchy and staff duty rosters.",
     False, "P2 - Medium", "Inter-clinic referral messaging broadcast to wrong clinic personnel.",
     "Direct telephone call to destination clinic reception.", "Facility staff roster active.",
     "ROLE-015", "Consultation transfer note.", "Shift roster publishing.", "INT-010", "WF-017", "REL-02",
     "Doctor on leave at destination clinic.", "Auto-forward message to duty Medical Officer on shift.")
]

# Build structured records
DEPENDENCIES = []
for idx, d in enumerate(RAW_DEPENDENCIES):
    dep_id = f"DEPENDENCY-{(idx + 1):03d}"
    code = d[0]
    cat = d[1]
    src_mod = d[2]
    tgt_mod = d[3]
    src_feat = d[4]
    tgt_feat = d[5]
    dep_type = d[6]
    reason = d[7]
    blocking = d[8]
    crit = d[9]
    impact = d[10]
    workaround = d[11]
    resolution = d[12]
    owner_role = d[13]
    req_before = d[14]
    req_after = d[15]
    req_ref = d[16]
    wf_ref = d[17]
    rel_ref = d[18]
    risk = d[19]
    mitigation = d[20]

    src_name = MODULE_MAP[src_mod]["name"] if src_mod in MODULE_MAP else src_mod
    tgt_name = MODULE_MAP[tgt_mod]["name"] if tgt_mod in MODULE_MAP else tgt_mod

    record = {
        "id": dep_id,
        "code": code,
        "category": cat,
        "source_module": src_mod,
        "target_module": tgt_mod,
        "source_name": src_name,
        "target_name": tgt_name,
        "source_feature": src_feat,
        "target_feature": tgt_feat,
        "type": dep_type,
        "direction": f"{src_mod} -> {tgt_mod}",
        "reason": reason,
        "blocking": blocking,
        "criticality": crit,
        "failure_impact": impact,
        "workaround": workaround,
        "resolution_condition": resolution,
        "owner_role": owner_role,
        "required_before": req_before,
        "required_after": req_after,
        "requirement_ref": req_ref,
        "workflow_ref": wf_ref,
        "release_ref": rel_ref,
        "risk": risk,
        "mitigation": mitigation
    }
    DEPENDENCIES.append(record)

DEPENDENCY_MAP = {d["id"]: d for d in DEPENDENCIES}

def check_acyclic_dependencies():
    """
    Mathematical acyclicity check across all module-level dependency edges using Kahn's algorithm.
    Graph semantics:
    An edge (U, V) where U depends on V means V is a PREREQUISITE for U.
    In execution/readiness order, V must precede U (V -> U).
    A graph is acyclic if and only if all 30 nodes can be topologically ordered.
    """
    nodes = {f"MODULE-{i:03d}" for i in range(1, 31)}

    # In execution graph: V (target/prerequisite) -> U (source/dependent)
    # in_degree[U] is the number of prerequisites U has.
    adj = {n: [] for n in nodes}
    in_degree = {n: 0 for n in nodes}

    seen_edges = set()
    for d in DEPENDENCIES:
        u = d["source_module"]  # dependent consumer
        v = d["target_module"]  # prerequisite provider
        if (v, u) not in seen_edges:
            seen_edges.add((v, u))
            adj[v].append(u)
            in_degree[u] += 1

    queue = [n for n in nodes if in_degree[n] == 0]
    visited = []

    while queue:
        curr = queue.pop(0)
        visited.append(curr)
        for nxt in adj[curr]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)

    is_acyclic = (len(visited) == len(nodes))
    return is_acyclic, len(visited), len(nodes)

def get_topological_sort():
    """Returns the topological sort order of all 30 modules."""
    nodes = {f"MODULE-{i:03d}" for i in range(1, 31)}
    adj = {n: [] for n in nodes}
    in_degree = {n: 0 for n in nodes}
    seen_edges = set()
    for d in DEPENDENCIES:
        u = d["source_module"]
        v = d["target_module"]
        if (v, u) not in seen_edges:
            seen_edges.add((v, u))
            adj[v].append(u)
            in_degree[u] += 1

    queue = [n for n in nodes if in_degree[n] == 0]
    visited = []
    while queue:
        curr = queue.pop(0)
        visited.append(curr)
        for nxt in adj[curr]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)
    return visited

if __name__ == "__main__":
    print(f"Total Dependencies defined: {len(DEPENDENCIES)}")
    acyclic, visited, total = check_acyclic_dependencies()
    print(f"Acyclic Check (Kahn's algorithm): {'PASS (100% DAG)' if acyclic else 'FAIL (Cycles exist)'} ({visited}/{total} nodes topologically sorted)")
    if acyclic:
        print("Topological build sequence:")
        topo = get_topological_sort()
        for idx, m in enumerate(topo):
            print(f"  {idx+1:02d}. {m}: {MODULE_MAP[m]['name']}")
