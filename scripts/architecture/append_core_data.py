"""
scripts/architecture/append_core_data.py
Appends comprehensive structured datasets for Modules, Workflows, Data Entities,
External Systems, Environments, and Advisory AI Models to arch_core_data.py.
"""

from pathlib import Path

APPEND_CONTENT = '''
# -------------------------------------------------------------
# 4. 30 Product Modules (MODULE-001 to MODULE-030)
# -------------------------------------------------------------
MODULES_RAW = [
    ("MODULE-001", "Staff Authentication & MFA Engine", "DOMAIN-001", "Core Foundation & Platform Administration", "ARCH-CONT-004", "ARCH-DATA-001", "P0 - Critical", "CORE MVP",
     "Manages staff identities, Argon2id salted credentials, TOTP MFA challenges, session lifecycle, and cryptographic token issuance.",
     "POST /api/v1/auth/login, POST /api/v1/auth/mfa/verify, POST /api/v1/auth/refresh, POST /api/v1/auth/logout",
     "Enforces rate limiting (5 attempts/min), brute-force lockout, and AES-256 encrypted credential caches on edge nodes."),

    ("MODULE-002", "Role-Based Access Control (RBAC) & Entitlements", "DOMAIN-001", "Core Foundation & Platform Administration", "ARCH-CONT-004", "ARCH-DATA-002", "P0 - Critical", "CORE MVP",
     "Defines and enforces granular permissions, capability claims, and segregation of duties (SOD-001) across 30 clinical and administrative roles.",
     "GET /api/v1/rbac/roles, POST /api/v1/rbac/entitlements/evaluate, PUT /api/v1/rbac/staff/:id/roles",
     "Validates role claims per request; denies unauthorized horizontal or vertical privilege escalation."),

    ("MODULE-003", "Healthcare Facility & Organizational Hierarchy", "DOMAIN-001", "Core Foundation & Platform Administration", "ARCH-CONT-002", "ARCH-DATA-003", "P0 - Critical", "CORE MVP",
     "Maintains the municipal hierarchy of 183 clinics, 8 BBMP zones, 225 wards, room allocations, and operational hours.",
     "GET /api/v1/facilities/clinics, GET /api/v1/facilities/zones, POST /api/v1/facilities/clinics/:id/rooms",
     "Edge appliances cache local clinic metadata; updates propagate via delta synchronization."),

    ("MODULE-004", "Clinical & Administrative Staff Directory", "DOMAIN-001", "Core Foundation & Platform Administration", "ARCH-CONT-004", "ARCH-DATA-004", "P0 - Critical", "CORE MVP",
     "Maintains professional profiles, medical registration council numbers (KMC), duty rosters, and shift schedules for clinic personnel.",
     "GET /api/v1/staff/directory, POST /api/v1/staff/roster/assign, GET /api/v1/staff/:id/qualifications",
     "Restricted PII access; medical council numbers verified against statutory state registries."),

    ("MODULE-005", "Patient Registration, Demographics & ABHA Minting", "DOMAIN-002", "Frontline Intake & Citizen Operations", "ARCH-CONT-005", "ARCH-DATA-005", "P0 - Critical", "CORE MVP",
     "Captures citizen demographic profiles, performs phonetic deduplication, mints municipal health IDs, and binds national ABHA numbers.",
     "POST /api/v1/patients/register, POST /api/v1/patients/search/phonetic, POST /api/v1/patients/abha/verify",
     "Full DPDP Act compliance; demographic data encrypted with AES-256 GCM; optional biometric deduplication."),

    ("MODULE-006", "Informed Clinical Consent & DPDP Data Privacy", "DOMAIN-002", "Frontline Intake & Citizen Operations", "ARCH-CONT-005", "ARCH-DATA-006", "P0 - Critical", "CORE MVP",
     "Records affirmative citizen consent for clinical treatment, tele-consultation, and health data sharing per DPDP Act 2023.",
     "POST /api/v1/consent/record, GET /api/v1/consent/status/:patientId, POST /api/v1/consent/revoke",
     "Consent artifacts cryptographically signed; provides emergency break-glass override with audit escalation."),

    ("MODULE-007", "Patient Token Generation & Station Routing", "DOMAIN-002", "Frontline Intake & Citizen Operations", "ARCH-CONT-006", "ARCH-DATA-007", "P0 - Critical", "CORE MVP",
     "Mints daily clinic visit tokens (General, Senior/Vulnerable, Emergency), prints 80mm thermal slips, and routes to initial station.",
     "POST /api/v1/tokens/issue, GET /api/v1/tokens/active/:clinicId, POST /api/v1/tokens/:id/route",
     "Local edge minting guarantees uninterrupted queueing during broadband outages; sub-second print dispatch."),

    ("MODULE-008", "Dynamic Queue Orchestration & Display Boards", "DOMAIN-002", "Frontline Intake & Citizen Operations", "ARCH-CONT-006", "ARCH-DATA-008", "P0 - Critical", "CORE MVP",
     "Manages dynamic multi-room queues, broadcasts next-patient calls to waiting hall TV screens via MQTT, and calculates wait times.",
     "POST /api/v1/queues/call-next, POST /api/v1/queues/transfer, GET /api/v1/queues/board-feed",
     "MQTT broker delivers token calls with < 50ms latency; audio chime and bilingual Kannada display."),

    ("MODULE-009", "Doctor EMR Console & Clinical SOAP Encounter", "DOMAIN-003", "Clinical Care & Diagnostic Orders", "ARCH-CONT-007", "ARCH-DATA-009", "P0 - Critical", "CORE MVP",
     "Provides physician consultation interface for capturing Subjective symptoms, Objective vitals/findings, Assessment, and Plan.",
     "POST /api/v1/encounters/start, PUT /api/v1/encounters/:id/soap, POST /api/v1/encounters/:id/seal",
     "Optimistic locking prevents concurrent overwrite; encounter seal signs record with cryptographic HMAC."),

    ("MODULE-010", "ICD-10 & SNOMED CT Clinical Diagnosis Coding", "DOMAIN-003", "Clinical Care & Diagnostic Orders", "ARCH-CONT-007", "ARCH-DATA-010", "P0 - Critical", "CORE MVP",
     "Enables fast bilingual autocomplete of clinical concepts mapped to SNOMED CT and statutory ICD-10 diagnostic codes.",
     "GET /api/v1/terminology/search, POST /api/v1/terminology/map-dual, GET /api/v1/terminology/stg/:condition",
     "Sub-15ms autocomplete via in-memory Trie/Redis cache; enforces standard treatment guidelines."),

    ("MODULE-011", "Electronic Prescription (e-Rx) & Drug Safety Engine", "DOMAIN-003", "Clinical Care & Diagnostic Orders", "ARCH-CONT-008", "ARCH-DATA-011", "P0 - Critical", "CORE MVP",
     "Authorizes e-prescriptions from essential drug formulary, evaluates drug-drug interactions, and checks pediatric dosage limits.",
     "POST /api/v1/prescriptions/create, POST /api/v1/prescriptions/safety-check, GET /api/v1/prescriptions/:id",
     "Hard stop on severe contraindications; generates bilingual Kannada dosage schedule and thermal print slip."),

    ("MODULE-012", "Point-of-Care Laboratory Testing & Diagnostic Orders", "DOMAIN-003", "Clinical Care & Diagnostic Orders", "ARCH-CONT-010", "ARCH-DATA-012", "P0 - Critical", "CORE MVP",
     "Manages orders and results for 58 rapid point-of-care laboratory diagnostic tests, specimen labelling, and panic value alerts.",
     "POST /api/v1/lab/orders/create, PUT /api/v1/lab/results/enter, POST /api/v1/lab/results/panic-escalate",
     "Panic values trigger instant audible alerts on doctor workstation; specimen labels formatted with barcodes."),

    ("MODULE-013", "Pharmacy Dispensing & 2D Barcode Verification", "DOMAIN-004", "Pharmacy, Dispensing & Inventory Supply Chain", "ARCH-CONT-009", "ARCH-DATA-013", "P0 - Critical", "CORE MVP",
     "Guides pharmacist through prescription dispensation, validates batch expiry via 2D DataMatrix scanning, and prints medicine slips.",
     "GET /api/v1/pharmacy/queue, POST /api/v1/pharmacy/dispense/scan, POST /api/v1/pharmacy/dispense/confirm",
     "Hardware scanner wedge input; prevents dispensing expired or recalled drug batches; updates inventory atomically."),

    ("MODULE-014", "Real-Time Batch Inventory & FEFO Stock Ledger", "DOMAIN-004", "Pharmacy, Dispensing & Inventory Supply Chain", "ARCH-CONT-009", "ARCH-DATA-014", "P0 - Critical", "CORE MVP",
     "Tracks stock levels per batch, enforces First-Expiry-First-Out allocation, monitors storage bins, and flags near-expiry items.",
     "GET /api/v1/inventory/batches, POST /api/v1/inventory/adjust, GET /api/v1/inventory/alerts/expiry",
     "ACID ledger transactions; prohibits negative stock balances; computes daily burn rates per clinic."),

    ("MODULE-015", "Drug Indent Generation, Receiving & Cold-Chain Intake", "DOMAIN-004", "Pharmacy, Dispensing & Inventory Supply Chain", "ARCH-CONT-009", "ARCH-DATA-015", "P0 - Critical", "CORE MVP",
     "Automates monthly replenishment indents to central warehouse (KDLWS), verifies receiving manifests, and logs cold-chain temps.",
     "POST /api/v1/indents/generate, POST /api/v1/indents/submit, POST /api/v1/indents/receive/verify",
     "Electronic Data Interchange with KDLWS; automated reorder level (ROL) calculations based on 30-day usage."),

    ("MODULE-016", "Essential Medicine List (EML) & Formulary Master", "DOMAIN-004", "Pharmacy, Dispensing & Inventory Supply Chain", "ARCH-CONT-009", "ARCH-DATA-016", "P0 - Critical", "CORE MVP",
     "Maintains the municipal primary care drug formulary, generic-brand mappings, therapeutic categories, and dosage forms.",
     "GET /api/v1/formulary/drugs, POST /api/v1/formulary/master/update, GET /api/v1/formulary/categories",
     "Authoritative clinical formulary; restricts prescribing to available clinic stock tiers."),

    ("MODULE-017", "Secondary Referral & 108 Emergency EMS Transit", "DOMAIN-005", "Care Continuity, Referrals & Community Outreach", "ARCH-CONT-011", "ARCH-DATA-017", "P0 - Critical", "CORE MVP",
     "Assembles referral dossiers for secondary hospitals, dispatches 108 emergency ambulance requests, and tracks patient handover.",
     "POST /api/v1/referrals/create, POST /api/v1/referrals/ems108/dispatch, GET /api/v1/referrals/tracking/:id",
     "Integrates with GVK-EMRI 108 CAD API; generates encrypted QR summary dossier for emergency transport."),

    ("MODULE-018", "NCD Longitudinal Follow-Up & Recall Management", "DOMAIN-005", "Care Continuity, Referrals & Community Outreach", "ARCH-CONT-012", "ARCH-DATA-018", "P1 - High", "MVP-PLUS",
     "Maintains disease registries for hypertension, diabetes, and mental health; tracks follow-up compliance and flags defaulters.",
     "POST /api/v1/ncd/enroll, GET /api/v1/ncd/follow-up/roster, POST /api/v1/ncd/recall/trigger",
     "Automated recall queues; generates outreach task lists for ANM and ASHA community health workers."),

    ("MODULE-019", "Citizen Multichannel Notifications & Health Reminders", "DOMAIN-005", "Care Continuity, Referrals & Community Outreach", "ARCH-CONT-012", "ARCH-DATA-019", "P1 - High", "CORE MVP",
     "Dispatches bilingual SMS and WhatsApp reminders for visit follow-ups, test result availability, and vaccination camps.",
     "POST /api/v1/notifications/send, GET /api/v1/notifications/delivery-status, POST /api/v1/notifications/campaigns",
     "DLT-registered templates on Karnataka State SMS Gateway; rate limited to avoid telecommunication spam."),

    ("MODULE-020", "Citizen Feedback, Grievance & Ombudsman Redressal", "DOMAIN-002", "Frontline Intake & Citizen Operations", "ARCH-CONT-012", "ARCH-DATA-020", "P2 - Medium", "MVP-PLUS",
     "Captures citizen feedback on tablet kiosks, tracks facility grievances (e.g. staff absence, drug shortages), and monitors SLAs.",
     "POST /api/v1/feedback/submit, POST /api/v1/grievance/file, GET /api/v1/grievance/sla-status",
     "Escalates unresolved grievances to BBMP Zonal Medical Officer; public rating metrics aggregated anonymously."),

    ("MODULE-021", "Cryptographic Audit Ledger & Compliance (WORM)", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-017", "ARCH-DATA-021", "P0 - Critical", "CORE MVP",
     "Records immutable write-once-read-many (WORM) audit trails with SHA-256 HMAC hash chaining for all clinical and auth events.",
     "POST /api/v1/audit/log, GET /api/v1/audit/verify-chain, GET /api/v1/audit/export/regulatory",
     "Non-repudiable audit proofs; mathematically detects record deletion or tampering; complies with DPDP Act 2023."),

    ("MODULE-022", "Zonal & Ward Operational KPI Dashboards", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-015", "ARCH-DATA-022", "P1 - High", "CORE MVP",
     "Delivers real-time public health indicators, clinic footfalls, stockout alerts, and disease heatmaps to municipal health officers.",
     "GET /api/v1/analytics/kpis/summary, GET /api/v1/analytics/heatmaps/ward, GET /api/v1/analytics/workload",
     "ClickHouse columnar aggregations; sub-second query latency; role-based data anonymization."),

    ("MODULE-023", "Safe AI/ML Clinical Decision Support Safeguards", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-016", "ARCH-DATA-023", "P2 - Medium", "POST-MVP",
     "Provides non-autonomous advisory machine learning predictions (syndromic fever clusters, defaulter risk) with mandatory doctor review.",
     "POST /api/v1/ai/advisory/evaluate, GET /api/v1/ai/models/status, POST /api/v1/ai/advisory/override-feedback",
     "Strict human-in-the-loop requirement; physician override logged; zero automated prescription or diagnostic action."),

    ("MODULE-024", "National Health ABDM Ecosystem Interoperability", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-014", "ARCH-DATA-024", "P1 - High", "CORE MVP",
     "Bridges platform with Ayushman Bharat Digital Mission (M1: ABHA, M2: HIP Care Context, M3: HIU Consent) via FHIR R4.",
     "POST /api/v1/abdm/m1/verify-abha, POST /api/v1/abdm/m2/publish-fhir, POST /api/v1/abdm/m3/fetch-consented",
     "Transforms clinical records to FHIR R4 bundles (Bundle, Condition, MedicationRequest, Observation)."),

    ("MODULE-025", "Autonomous Offline Edge Engine & Conflict Replay", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-013", "ARCH-DATA-025", "P0 - Critical", "CORE MVP",
     "Orchestrates 72-hour edge autonomy on SQLite WAL, journals local mutations with vector clocks, and replays deltas via CRDTs.",
     "POST /api/v1/sync/handshake, POST /api/v1/sync/push-mutations, GET /api/v1/sync/pull-deltas",
     "Deterministic field-level conflict resolution; bandwidth-throttled resume; zero transaction loss during WAN partitions."),

    ("MODULE-026", "Master System Administration & Feature Flagging", "DOMAIN-001", "Core Foundation & Platform Administration", "ARCH-CONT-003", "ARCH-DATA-026", "P0 - Critical", "CORE MVP",
     "Provides system administrators with tenant configuration controls, dynamic feature toggles, maintenance mode, and log levels.",
     "GET /api/v1/admin/configs, PUT /api/v1/admin/feature-flags, POST /api/v1/admin/maintenance-window",
     "Granular canary rollouts by clinic ID; dynamic configuration refresh without pod restart."),

    ("MODULE-027", "State Health HMIS & Statutory Disease Reporting", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-015", "ARCH-DATA-027", "P1 - High", "CORE MVP",
     "Compiles and exports statutory health indicator formats for Karnataka Health Management Information System and IDSP/IHIP.",
     "POST /api/v1/reports/hmis/generate, GET /api/v1/reports/idsp/syndromic, POST /api/v1/reports/statutory/submit",
     "Automates Form P, Form L, and Form S syndromic surveillance feeds; eliminates manual paper report collation."),

    ("MODULE-028", "Facility Operations Helpdesk & Incident Dispatch", "DOMAIN-005", "Care Continuity, Referrals & Community Outreach", "ARCH-CONT-002", "ARCH-DATA-028", "P2 - Medium", "MVP-PLUS",
     "Tracks hardware faults (printer jam, scanner failure, UPS battery warning) and dispatches field technicians across clinics.",
     "POST /api/v1/helpdesk/tickets/create, GET /api/v1/helpdesk/tickets/clinic/:id, PUT /api/v1/helpdesk/tickets/:id/resolve",
     "Automated telemetry alarms from edge mini-servers trigger preventive maintenance tickets."),

    ("MODULE-029", "Telemedicine & Specialist Tele-Consultation Bridge", "DOMAIN-003", "Clinical Care & Diagnostic Orders", "ARCH-CONT-007", "ARCH-DATA-029", "P2 - Medium", "POST-MVP",
     "Connects primary clinic doctors with secondary hospital specialists for real-time video consultation and joint review.",
     "POST /api/v1/telemed/sessions/initiate, GET /api/v1/telemed/specialists/available, POST /api/v1/telemed/sessions/:id/notes",
     "WebRTC encrypted media streams; shared clinical encounter view with real-time vitals and diagnostic telemetry."),

    ("MODULE-030", "Municipal Pilot Command Center & Disaster Operations", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-015", "ARCH-DATA-030", "P2 - Medium", "POST-MVP",
     "Central command console for municipal epidemic surveillance, disaster mass casualty triage, and city-wide resource diversion.",
     "GET /api/v1/command/overview, POST /api/v1/command/alerts/broadcast, POST /api/v1/command/resources/reallocate",
     "City-wide geospatial situational awareness; automated outbreak cluster detection across 183 clinics.")
]

MODULES = [
    {
        "id": m[0],
        "name": m[1],
        "domain_id": m[2],
        "domain_name": m[3],
        "container_id": m[4],
        "data_id": m[5],
        "priority": m[6],
        "mvp_tier": m[7],
        "responsibilities": m[8],
        "endpoints": m[9],
        "security": m[10]
    }
    for m in MODULES_RAW
]

MODULE_MAP = {m["id"]: m for m in MODULES}
TOTAL_MODULES = len(MODULES)

# -------------------------------------------------------------
# 5. 25 Clinic Workflows (WF-001 to WF-025)
# -------------------------------------------------------------
WORKFLOWS_RAW = [
    ("WF-001", "Master Clinic Day Operational Workflow", "DOMAIN-001", "08:00 AM Clinic opening & system startup", "ARCH-CONT-002", ["ARCH-CONT-001", "ARCH-CONT-004", "ARCH-CONT-018"], "Comprehensive clinic operational lifecycle from staff check-in to evening closeout."),
    ("WF-002", "Staff Login, Multi-Factor Authentication & Session Management", "DOMAIN-001", "Staff member launches browser workstation", "ARCH-CONT-004", ["ARCH-CONT-001", "ARCH-CONT-002"], "Salted Argon2id authentication with TOTP MFA and offline PIN fallback."),
    ("WF-003", "Patient Registration, ABHA Creation & Demographic Intake", "DOMAIN-002", "Citizen arrives at clinic intake counter", "ARCH-CONT-005", ["ARCH-CONT-001", "ARCH-CONT-014"], "Bilingual demographic entry, phonetic deduplication, and voluntary ABHA minting."),
    ("WF-004", "Patient Search, Multi-Parametric Lookup & Verification", "DOMAIN-002", "Registration clerk searches returning citizen", "ARCH-CONT-005", ["ARCH-CONT-001", "ARCH-CONT-002"], "Fuzzy phonetic search by name, phone, municipal ID, or national ABHA address."),
    ("WF-005", "Repeat Patient Revisit & Longitudinal Episode Linking", "DOMAIN-002", "Identified returning patient checks in", "ARCH-CONT-005", ["ARCH-CONT-001", "ARCH-CONT-007"], "Links current clinical visit to historical EMR record and chronic disease episodes."),
    ("WF-006", "Informed Clinical & Digital Health Consent", "DOMAIN-002", "Patient begins consultation or data share", "ARCH-CONT-005", ["ARCH-CONT-001", "ARCH-CONT-017"], "Captures affirmative consent for treatment and ABDM record sharing per DPDP Act 2023."),
    ("WF-007", "Token Issuance, Priority Tagging & Queue Entry", "DOMAIN-002", "Citizen registration completed", "ARCH-CONT-006", ["ARCH-CONT-001", "ARCH-CONT-002"], "Mints daily serial token, applies vulnerability tags, and prints 80mm thermal slip."),
    ("WF-008", "Dynamic Multi-Room Queue Orchestration & Display", "DOMAIN-002", "Provider signals readiness for next patient", "ARCH-CONT-006", ["ARCH-CONT-001", "ARCH-CONT-002"], "Advances queue state, publishes MQTT chime, and updates waiting hall TV screen."),
    ("WF-009", "Nursing Triage, Vital Signs & Clinical Acuity Assessment", "DOMAIN-003", "Citizen called into nursing triage booth", "ARCH-CONT-006", ["ARCH-CONT-001", "ARCH-CONT-007"], "Records BP, pulse, SpO2, temp, height/weight, and calculates automated MEWS score."),
    ("WF-010", "Danger Sign Detection, Critical Value Alert & Emergency Escalation", "DOMAIN-003", "MEWS >= 5 or vital signs exceed critical thresholds", "ARCH-CONT-006", ["ARCH-CONT-001", "ARCH-CONT-011"], "Fires audible/visual alerts and escalates patient directly ahead of routine doctor queue."),
    ("WF-011", "Doctor Clinical Consultation, SOAP Documentation & CDSS Advisory", "DOMAIN-003", "Doctor opens active patient consultation", "ARCH-CONT-007", ["ARCH-CONT-001", "ARCH-CONT-016"], "Captures SOAP progress notes, codes diagnoses in SNOMED/ICD-10, and reviews CDSS advice."),
    ("WF-012", "Electronic Prescription, Drug Interaction & Safety Verification", "DOMAIN-003", "Doctor completes clinical evaluation", "ARCH-CONT-008", ["ARCH-CONT-001", "ARCH-CONT-009"], "Formulary e-prescribing, drug interaction verification, and cryptographic signing."),
    ("WF-013", "Pharmacy Dispensing, FEFO Inventory Allocation & Patient Counseling", "DOMAIN-004", "Patient presents token at pharmacy counter", "ARCH-CONT-009", ["ARCH-CONT-001", "ARCH-CONT-014"], "Scans 2D DataMatrix barcodes, verifies FEFO batch rules, and provides Kannada counseling."),
    ("WF-014", "Pharmacy Stock Replenishment, Indenting & Cold-Chain Inventory Control", "DOMAIN-004", "Stock drops below reorder level (ROL) or monthly cycle", "ARCH-CONT-009", ["ARCH-CONT-002", "ARCH-CONT-018"], "Generates automated replenishment indent, tracks KDLWS delivery, and logs cold chain."),
    ("WF-015", "Point-of-Care Laboratory Testing, Barcoding & Panic Value Alert", "DOMAIN-003", "Lab investigation ordered by physician", "ARCH-CONT-010", ["ARCH-CONT-001", "ARCH-CONT-007"], "Collects specimens, runs rapid diagnostic tests (58 panels), and reports panic values."),
    ("WF-016", "Clinical Referral, Higher Center Escalation & Ambulance Transfer", "DOMAIN-005", "Physician determines need for secondary care", "ARCH-CONT-011", ["ARCH-CONT-001", "ARCH-CONT-017"], "Compiles referral dossier, dispatches 108 emergency ambulance, and tracks transit."),
    ("WF-017", "NCD Follow-Up Scheduling, Chronic Disease Recall & Defaulter Tracking", "DOMAIN-005", "Hypertension or diabetes patient completes visit", "ARCH-CONT-012", ["ARCH-CONT-001", "ARCH-CONT-018"], "Schedules return appointment, dispatches reminders, and flags missed follow-ups."),
    ("WF-018", "Omnichannel Patient & Staff Notification, Alerting & Communication", "DOMAIN-005", "System event triggers notification (recall, panic)", "ARCH-CONT-012", ["ARCH-CONT-002", "ARCH-CONT-003"], "Formats and dispatches bilingual SMS and WhatsApp messages via state gateway."),
    ("WF-019", "Citizen Grievance Redressal, Feedback & SLA Escalation", "DOMAIN-002", "Citizen submits feedback or formal complaint", "ARCH-CONT-012", ["ARCH-CONT-001", "ARCH-CONT-015"], "Captures star rating, routes grievance to Zonal Medical Officer, and enforces SLA."),
    ("WF-020", "Cryptographic Audit Trail, Immutable Logging & Tamper Detection", "DOMAIN-006", "Any clinical, prescription, or auth state mutation", "ARCH-CONT-017", ["ARCH-CONT-002", "ARCH-CONT-018"], "Appends event to SHA-256 HMAC hash chain and validates Merkle tree consistency."),
    ("WF-021", "Clinical Analytics, Syndromic Surveillance & Population Health Reporting", "DOMAIN-006", "Scheduled nightly batch or real-time event stream", "ARCH-CONT-015", ["ARCH-CONT-018", "ARCH-CONT-016"], "Extracts CDC events to ClickHouse, aggregates ward KPIs, and flags fever outbreaks."),
    ("WF-022", "Autonomous Offline Edge Operation, Local Storage & Network Resilience", "DOMAIN-006", "WAN optical fiber cut or broadband failure", "ARCH-CONT-002", ["ARCH-CONT-001", "ARCH-CONT-013"], "Switches seamlessly to local SQLite WAL database; guarantees 72h clinic operation."),
    ("WF-023", "Bidirectional Synchronization, Conflict Resolution & Merkle Ledger", "DOMAIN-006", "WAN network connectivity restored", "ARCH-CONT-013", ["ARCH-CONT-002", "ARCH-CONT-018"], "Replays mutation journal with vector clocks, resolves CRDT conflicts, and updates edge."),
    ("WF-024", "Ayushman Bharat Digital Mission (ABDM) Gateway & FHIR Interoperability", "DOMAIN-006", "Citizen consents to publish health record to ABDM", "ARCH-CONT-014", ["ARCH-CONT-007", "ARCH-CONT-018"], "Transforms encounter to FHIR R4 Bundle and publishes care context to national grid."),
    ("WF-025", "Clinical Emergency Exception, Fast-Track Bypass & Resuscitation Protocol", "DOMAIN-003", "Trauma or unconscious patient brought to clinic", "ARCH-CONT-006", ["ARCH-CONT-001", "ARCH-CONT-011"], "Bypasses registration queue, issues emergency token, enables break-glass EMR access.")
]

WORKFLOWS = [
    {
        "id": w[0],
        "name": w[1],
        "domain_id": w[2],
        "trigger": w[3],
        "primary_container": w[4],
        "participating_containers": w[5],
        "description": w[6]
    }
    for w in WORKFLOWS_RAW
]

WORKFLOW_MAP = {w["id"]: w for w in WORKFLOWS}
TOTAL_WORKFLOWS = len(WORKFLOWS)

# -------------------------------------------------------------
# 6. 30 Relational Data Entities (ARCH-DATA-001 to ARCH-DATA-030)
# -------------------------------------------------------------
DATA_ENTITIES_RAW = [
    ("ARCH-DATA-001", "auth_users", "DOMAIN-001", "Staff identities, salted Argon2id hashes, MFA secrets, account status, lockout counters.", "UUIDv7", "CONFIDENTIAL", "Permanent", "Tier 1"),
    ("ARCH-DATA-002", "role_permissions", "DOMAIN-001", "RBAC role definitions, capability claims, resource grants, segregation-of-duty rules.", "UUIDv7", "INTERNAL", "Permanent", "Tier 1"),
    ("ARCH-DATA-003", "facilities", "DOMAIN-001", "183 clinic facilities, ward boundaries, zone assignments, operational rooms, GPS coords.", "UUIDv7", "PUBLIC", "Permanent", "Tier 2"),
    ("ARCH-DATA-004", "staff_profiles", "DOMAIN-001", "Doctor KMC registration, nurse qualifications, shift schedules, clinic assignments.", "UUIDv7", "RESTRICTED", "10 Years", "Tier 2"),
    ("ARCH-DATA-005", "patients", "DOMAIN-002", "Citizen demographic profiles, phonetic Soundex/Metaphone hashes, ABHA addresses, contact info.", "UUIDv7", "RESTRICTED_PHI", "Permanent", "Tier 1"),
    ("ARCH-DATA-006", "consent_records", "DOMAIN-002", "DPDP Act consent grants, purpose codes, expiry dates, revocation timestamps, digital signatures.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-007", "tokens", "DOMAIN-002", "Daily visit tokens, priority tier tags, serial numbers, intake station assignments.", "UUIDv7", "INTERNAL", "3 Years", "Tier 2"),
    ("ARCH-DATA-008", "queue_states", "DOMAIN-002", "Dynamic multi-room queue entries, call timestamps, wait durations, provider allocations.", "UUIDv7", "INTERNAL", "1 Year", "Tier 3"),
    ("ARCH-DATA-009", "clinical_encounters", "DOMAIN-003", "Outpatient visits, SOAP notes, vital signs, physical exam findings, doctor signatures.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-010", "diagnoses", "DOMAIN-003", "Clinical condition assessments, ICD-10 diagnostic codes, SNOMED CT concept identifiers.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-011", "prescriptions", "DOMAIN-003", "Electronic prescription headers, drug items, dosages, frequencies, duration, safety flags.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-012", "lab_orders", "DOMAIN-003", "Rapid test orders (58 panels), specimen barcodes, numerical results, panic value flags.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-013", "dispensations", "DOMAIN-004", "Pharmacy dispensation logs, 2D DataMatrix scans, batch allocations, counseling notes.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-014", "pharmacy_batches", "DOMAIN-004", "Medication batch ledger, manufactured date, expiry date, current stock count, FEFO rank.", "UUIDv7", "INTERNAL", "10 Years", "Tier 1"),
    ("ARCH-DATA-015", "drug_indents", "DOMAIN-004", "Replenishment orders to KDLWS warehouse, line items, approved quantities, dispatch status.", "UUIDv7", "INTERNAL", "5 Years", "Tier 2"),
    ("ARCH-DATA-016", "formulary_master", "DOMAIN-004", "Essential medicine catalog, generic names, therapeutic classes, pediatric dosage bands.", "UUIDv7", "PUBLIC", "Permanent", "Tier 2"),
    ("ARCH-DATA-017", "referrals", "DOMAIN-005", "Secondary hospital referrals, clinical summary dossiers, 108 ambulance dispatch logs.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-018", "ncd_episodes", "DOMAIN-005", "Chronic disease registries (hypertension, diabetes), recall dates, defaulter status.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-019", "notifications", "DOMAIN-005", "Bilingual SMS/WhatsApp messages, delivery receipts, template IDs, recipient numbers.", "UUIDv7", "RESTRICTED", "1 Year", "Tier 3"),
    ("ARCH-DATA-020", "grievances", "DOMAIN-002", "Citizen feedback submissions, grievance categories, resolution notes, ombudsman audit logs.", "UUIDv7", "RESTRICTED", "5 Years", "Tier 2"),
    ("ARCH-DATA-021", "audit_events", "DOMAIN-006", "Immutable WORM audit ledger, SHA-256 HMAC hash chains, user IDs, IP addresses, payloads.", "UUIDv7", "CONFIDENTIAL", "10 Years", "Tier 1"),
    ("ARCH-DATA-022", "kpi_metrics", "DOMAIN-006", "Daily clinic footfall aggregates, consultation durations, antibiotic ratios, stock levels.", "UUIDv7", "PUBLIC_AGGREGATE", "10 Years", "Tier 3"),
    ("ARCH-DATA-023", "cdss_rules", "DOMAIN-006", "Clinical decision support rule definitions, drug-drug contraindication pairs, allergy matrices.", "UUIDv7", "INTERNAL", "Permanent", "Tier 2"),
    ("ARCH-DATA-024", "abdm_artifacts", "DOMAIN-006", "FHIR R4 Bundles, care context links, HIP publishing receipts, consent artifacts.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-025", "mutation_log", "DOMAIN-006", "Edge offline journal, vector clock timestamps, entity mutations, sync status flags.", "UUIDv7", "INTERNAL", "90 Days", "Tier 1"),
    ("ARCH-DATA-026", "system_configs", "DOMAIN-001", "Tenant configuration parameters, dynamic feature flags, clinic operational toggles.", "UUIDv7", "CONFIDENTIAL", "Permanent", "Tier 1"),
    ("ARCH-DATA-027", "hmis_reports", "DOMAIN-006", "Statutory state health reports, Form P/L/S syndromic surveillance summaries.", "UUIDv7", "PUBLIC_AGGREGATE", "10 Years", "Tier 2"),
    ("ARCH-DATA-028", "helpdesk_tickets", "DOMAIN-005", "Facility hardware fault logs, IT support tickets, technician dispatch notes.", "UUIDv7", "INTERNAL", "3 Years", "Tier 3"),
    ("ARCH-DATA-029", "teleconsultations", "DOMAIN-003", "Telemedicine specialist consultation sessions, WebRTC call metadata, joint notes.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-030", "command_center_incidents", "DOMAIN-006", "Municipal epidemic outbreak alerts, flood/mass-casualty response incident records.", "UUIDv7", "RESTRICTED", "10 Years", "Tier 1")
]

DATA_ENTITIES = [
    {
        "id": d[0],
        "table": d[1],
        "domain": d[2],
        "description": d[3],
        "pk_type": d[4],
        "classification": d[5],
        "retention": d[6],
        "backup_tier": d[7]
    }
    for d in DATA_ENTITIES_RAW
]

DATA_ENTITY_MAP = {d["id"]: d for d in DATA_ENTITIES}
TOTAL_DATA_ENTITIES = len(DATA_ENTITIES)

# -------------------------------------------------------------
# 7. 16 External Systems (EXT-001 to EXT-016)
# -------------------------------------------------------------
EXTERNAL_SYSTEMS_RAW = [
    ("EXT-001", "ABDM National Health Gateway", "National Health Authority (NHA)", "REST / HTTPS / FHIR R4", "JSON / FHIR Bundle", "100 req/min", "Asynchronous retry queue", "National DMZ"),
    ("EXT-002", "Karnataka Central Drug Warehouse (KDLWS)", "State Health Department", "REST / HTTPS / EDI", "JSON / EDIFACT", "30 req/min", "Local indent cache", "State Intranet"),
    ("EXT-003", "GVK-EMRI 108 Emergency Ambulance Dispatch", "Emergency Management Research Institute", "REST / HTTPS", "JSON / CAD Event", "120 req/min", "Manual phone dispatch escalation", "Emergency Gateway"),
    ("EXT-004", "Karnataka State SMS Gateway (KSSD)", "Centre for e-Governance (CeG)", "HTTPS POST API", "JSON / DLT Template", "500 req/sec", "Message buffer in Redis BullMQ", "State Gateway"),
    ("EXT-005", "Integrated Disease Surveillance Program (IDSP/IHIP)", "National Centre for Disease Control (NCDC)", "REST / HTTPS", "JSON / CSV Format", "50 req/min", "Daily batch retry", "National Health Mesh"),
    ("EXT-006", "BBMP Citizen Health Portal", "Bruhat Bengaluru Mahanagara Palike", "REST / HTTPS / OAuth2", "JSON", "200 req/min", "Cached appointment slots", "Municipal Cloud"),
    ("EXT-007", "National NCD Portal", "Ministry of Health and Family Welfare (MoHFW)", "REST / HTTPS", "JSON / FHIR", "60 req/min", "Offline NCD queue sync", "National Portal"),
    ("EXT-008", "Nikshay Portal (National TB Elimination)", "Central TB Division (CTD)", "REST / HTTPS", "JSON", "60 req/min", "Presumptive TB case queue", "National Health Mesh"),
    ("EXT-009", "Reproductive and Child Health (RCH) Portal", "MoHFW / Karnataka Health", "REST / HTTPS", "JSON", "60 req/min", "Antenatal offline buffer", "National Health Mesh"),
    ("EXT-010", "UIDAI Aadhaar Authentication Service", "Unique Identification Authority of India", "HTTPS / XML / Auth API", "Encrypted XML PID Block", "100 req/min", "Fallback to municipal health ID", "Statutory Sovereign"),
    ("EXT-011", "Zero-Cost Municipal Voucher Billing Gateway", "BBMP Health Accounts", "REST / HTTPS", "JSON / Voucher Token", "150 req/min", "Local voucher offline issue", "Municipal Intranet"),
    ("EXT-012", "Bio-Medical Waste Management (BMWM) Tracking", "Karnataka State Pollution Control Board", "REST / HTTPS", "JSON / Barcode Log", "30 req/min", "Local waste register", "Regulatory Gateway"),
    ("EXT-013", "Central Referral Hospital LIMS", "BBMP Tertiary Hospitals (KC General, Bowring)", "HL7 v2 / FHIR R4", "HL7 ORU_R01 / FHIR", "60 req/min", "Manual result printout", "Hospital Intranet"),
    ("EXT-014", "Central Pollution Control Board (CPCB) & Weather API", "CPCB / IMD Bengaluru", "REST / HTTPS", "JSON / Time-series", "10 req/min", "Last known 24h average", "Public Data"),
    ("EXT-015", "BBMP Municipal GIS & Ward Boundary Service", "BBMP Town Planning Department", "REST / GeoJSON / WFS", "GeoJSON Polygons", "50 req/min", "Cached offline GeoJSON layers", "Municipal Intranet"),
    ("EXT-016", "Cloud Hardware Security Module (KMS / HSM)", "MeitY Empaneled Cloud Provider", "PKCS#11 / REST KMS", "Binary Key Blocks", "1,000 req/sec", "Local TPM 2.0 derived keys", "Secure Hardware Enclave")
]

EXTERNAL_SYSTEMS = [
    {
        "id": s[0],
        "name": s[1],
        "agency": s[2],
        "protocol": s[3],
        "payload": s[4],
        "rate_limit": s[5],
        "fallback": s[6],
        "trust_level": s[7]
    }
    for s in EXTERNAL_SYSTEMS_RAW
]

EXTERNAL_SYSTEM_MAP = {s["id"]: s for s in EXTERNAL_SYSTEMS}
TOTAL_EXTERNAL_SYSTEMS = len(EXTERNAL_SYSTEMS)

# -------------------------------------------------------------
# 8. 8 Standard Environments (ENV-001 to ENV-008)
# -------------------------------------------------------------
ENVIRONMENTS_RAW = [
    ("ENV-001", "LOCAL", "Development Tier", "Individual developer workstation testing with Docker Compose and local SQLite/Postgres.", "Engineers", "Strictly Synthetic Data", "Local .env file", "Local Git commit"),
    ("ENV-002", "DEV", "Integration Tier", "Continuous integration build server, ephemeral feature branch validation.", "Dev Team", "Strictly Synthetic Data", "HashiCorp Vault Dev", "PR merge to develop"),
    ("ENV-003", "TEST", "Automated QA Tier", "Continuous nightly automated regression, contract testing with Pact, API stress testing.", "QA Automation", "Scrambled Synthetic Baseline", "HashiCorp Vault Test", "Automated test suite pass"),
    ("ENV-004", "QA", "Manual Verification Tier", "Manual exploratory testing, peripheral hardware certification (scanners, thermal printers).", "QA Team / PMs", "Anonymized Historical Clones", "HashiCorp Vault QA", "Manual QA sign-off"),
    ("ENV-005", "STAGING", "Pre-Production Tier", "Identical topology to production, performance benchmark runs, disaster recovery failover drill.", "Release Leads", "Synthetically Scaled 183-Clinic Data", "Vault KMS Staging", "Release gate checklist"),
    ("ENV-006", "PILOT", "Field Canary Tier", "Live deployment across 5 designated Namma Clinics in Bengaluru for field beta validation.", "Clinic Staff (5 Clinics)", "Live Operational Patient Data", "Vault Production KMS", "BBMP Medical Board Approval"),
    ("ENV-007", "PROD", "Production Tier", "Authoritative production platform serving all 183 Namma Clinics across Bengaluru.", "All Clinic Staff & Citizens", "Live Production Health Records", "Dedicated Cloud HSM / Vault KMS", "Executive Release Approval"),
    ("ENV-008", "DR", "Disaster Recovery Tier", "Hot-standby replicated environment in secondary cloud region (Mumbai) for instant failover.", "SRE / Ops On-Call", "Real-Time Replicated Production Data", "Replicated Cloud HSM / Vault", "Automated / Manual Failover Gate")
]

ENVIRONMENTS = [
    {
        "id": e[0],
        "name": e[1],
        "tier": e[2],
        "purpose": e[3],
        "users": e[4],
        "data_policy": e[5],
        "secrets": e[6],
        "promotion_gate": e[7]
    }
    for e in ENVIRONMENTS_RAW
]

ENVIRONMENT_MAP = {e["id"]: e for e in ENVIRONMENTS}
TOTAL_ENVIRONMENTS = len(ENVIRONMENTS)

# -------------------------------------------------------------
# 9. 12 Advisory Clinical AI Models (ARCH-AI-001 to ARCH-AI-012)
# -------------------------------------------------------------
AI_MODELS_RAW = [
    ("ARCH-AI-001", "Syndromic Fever Cluster Anomaly Detector", "Epidemiology", "Spatial-Temporal DBSCAN & Poisson Regression", "Ward ID, daily fever counts, rainfall, temperature, rolling 7-day baseline", "Outbreak probability score (0.00-1.00) & anomaly flag", "Mandatory review by District Epidemiologist; no public alert without CMO sign-off.", "Trained on de-identified historical BBMP fever surveillance data."),
    ("ARCH-AI-002", "Drug-Drug Adverse Interaction Advisor", "Clinical Pharmacology", "Rule Engine + BioBERT Embedding Classifier", "Active patient prescription drugs, proposed new medication, known allergy list", "Contraindication severity (MILD, MODERATE, SEVERE, FATAL) & clinical explanation", "Physician can dismiss MILD/MODERATE; SEVERE requires written clinical justification in EMR.", "Zero autonomous cancellation; human prescriber retains sole authority."),
    ("ARCH-AI-003", "Pediatric Dosage Boundary Safety Checker", "Clinical Pediatrics", "Pharmacokinetic Nomogram Boundary Model", "Patient age in months, weight in kg, drug formulary ID, prescribed frequency/dose", "Recommended dose range (mg/kg/day) & overdosing warning alert", "Hard visual warning if proposed dose > 120% of maximum safe pediatric threshold.", "Calibrated to Indian Academy of Pediatrics (IAP) standard formularies."),
    ("ARCH-AI-004", "NCD Defaulter & Follow-up Risk Forecaster", "Chronic Care", "Gradient Boosted Trees (LightGBM)", "Patient age, distance to clinic, previous visit adherence, medication days supply", "Probability of loss-to-follow-up within 30 days (Low, Medium, High)", "Ranks community health worker outreach task list; never denies clinic service.", "Audited for demographic fairness across gender and socioeconomic wards."),
    ("ARCH-AI-005", "Clinic Pharmacy Stockout Predictor", "Supply Chain", "Temporal Fusion Transformer (TFT)", "Historical 90-day drug consumption, seasonality, current batch balance, reorder lead time", "Estimated days until zero stock & recommended indent quantity", "Pharmacist reviews and modifies recommended indent prior to submission to KDLWS.", "Guarantees no stock starvation for essential life-saving medications."),
    ("ARCH-AI-006", "Lab Panic Value Triager", "Diagnostics", "Deterministic Clinical Boundary Classifier", "58 rapid diagnostic test panel codes, quantitative lab result values, patient age/sex", "Normal, Abnormal, Critical Panic Value flag & escalation target", "Instant audible chime and visual red banner on doctor consultation screen.", "Calibrated to NABL accredited hospital laboratory critical thresholds."),
    ("ARCH-AI-007", "Chest X-Ray Screening Assistant (Advisory)", "Pulmonology", "DenseNet-121 Convolutional Neural Network", "Digital DICOM chest radiograph (when available via secondary referral)", "Heatmap bounding box & presumptive TB/pneumonia probability score", "Preliminary triage aid only; definitive diagnosis requires radiologist interpretation.", "Non-autonomous; marked as investigative screening device."),
    ("ARCH-AI-008", "Diabetic Retinopathy Screening Assistant", "Ophthalmology", "ResNet-50 Fundus Image Classifier", "Digital fundus camera image captured at referral hub", "Retinopathy grade (No DR, Mild, Moderate, Severe, Proliferative)", "Flags urgent ophthalmology referral; does not initiate medical therapy.", "Validated against South Indian diabetic retinopathy clinical datasets."),
    ("ARCH-AI-009", "Hypertension Staging & Guideline Advisor", "Cardiology", "Clinical Rule-Based Expert System", "Resting systolic BP, diastolic BP, age, diabetes co-morbidity, tobacco history", "Stage (Elevated, Stage 1, Stage 2, Hypertensive Crisis) & first-line STG recommendation", "Suggests standard treatment guidelines; physician selects final pharmacological regimen.", "Follows Indian Guidelines on Hypertension (IGH-IV)."),
    ("ARCH-AI-010", "Antibiotic Stewardship AWaRe Advisor", "Infectious Disease", "WHO AWaRe Classification Decision Matrix", "Prescribed antibiotic code, provisional clinical diagnosis, patient age", "AWaRe category (Access, Watch, Reserve) & guideline concordance score", "Educational alert encouraging first-line 'Access' antibiotics over 'Watch' class.", "Monitors clinic-wide antibiotic prescribing ratios for municipal health audit."),
    ("ARCH-AI-011", "Vitals MEWS Deterioration Predictor", "Emergency Triage", "Modified Early Warning Score (MEWS) Algorithm", "Systolic BP, heart rate, respiratory rate, body temperature, AVPU consciousness score", "Integer MEWS score (0-14), clinical risk band (Low, Medium, High, Critical)", "MEWS >= 5 triggers automatic visual flashing and escalates queue to Room 1 immediately.", "Deterministic mathematical scoring; zero black-box opacity."),
    ("ARCH-AI-012", "Duplicate Demographic Patient Matcher", "Frontline Intake", "Phonetic Soundex/Metaphone + Jaro-Winkler Metric", "Candidate citizen name, guardian name, date of birth, gender, ward, phone number", "Similarity match confidence (0.00-1.00) & candidate existing patient IDs", "Registration nurse inspects candidate photo and history to confirm or create new record.", "Prevents fragmented medical records while avoiding erroneous identity merges.")
]

AI_MODELS = [
    {
        "id": a[0],
        "name": a[1],
        "domain": a[2],
        "model_type": a[3],
        "inputs": a[4],
        "outputs": a[5],
        "clinical_safeguard": a[6],
        "governance": a[7]
    }
    for a in AI_MODELS_RAW
]

AI_MODEL_MAP = {a["id"]: a for a in AI_MODELS}
TOTAL_AI_MODELS = len(AI_MODELS)
'''

def main():
    core_path = Path("scripts/architecture/arch_core_data.py")
    text = core_path.read_text(encoding="utf-8")

    # Remove existing main block if present
    if 'if __name__ == "__main__":' in text:
        text = text.split('if __name__ == "__main__":')[0]

    # Append new datasets
    text = text.strip() + "\n" + APPEND_CONTENT.strip() + "\n\n"

    # Add new main block
    new_main = '''
if __name__ == "__main__":
    print(f"Total Architecture Containers: {TOTAL_CONTAINERS}")
    print(f"Total Architecture Components: {TOTAL_COMPONENTS}")
    print(f"Total Architecture Decisions (ADRs): {TOTAL_ADRS}")
    print(f"Total Architecture Modules: {TOTAL_MODULES}")
    print(f"Total Architecture Workflows: {TOTAL_WORKFLOWS}")
    print(f"Total Architecture Data Entities: {TOTAL_DATA_ENTITIES}")
    print(f"Total External Systems: {TOTAL_EXTERNAL_SYSTEMS}")
    print(f"Total Environments: {TOTAL_ENVIRONMENTS}")
    print(f"Total Advisory AI Models: {TOTAL_AI_MODELS}")
'''
    text += new_main
    core_path.write_text(text, encoding="utf-8")
    print("Successfully enriched arch_core_data.py!")

if __name__ == "__main__":
    main()
