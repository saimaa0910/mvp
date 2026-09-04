#!/usr/bin/env python3
"""
build_data_fr.py
Builds canonical data_fr.py containing FR-001 through FR-080.
Covers all 80 functional requirements spanning the complete clinical, diagnostic,
pharmacy, administrative, and offline workflow domains of Namma Clinic.
"""

import os

FR_DEFINITIONS = [
    # 01-08: Authentication, Authorization & User Administration
    ("FR-001", "Multi-Factor Staff Authentication & Workstation Binding",
     "The platform shall authenticate frontline healthcare workers using secure credentials with mandatory clinic device binding.",
     "Authentication", "MUST", "Prevents unauthorized access from unverified external devices.",
     "Frontline Staff", "Staff Nurse", "ROLE-003", "STAKEHOLDER-015",
     "Staff launches clinic workstation application", "Workstation connected to local network or terminal bridge",
     "Staff username, password/PIN, workstation hardware UUID", "Argon2id verification, UUID matches clinic device whitelist",
     "User session established with 15-minute sliding JWT", "POST /api/v1/auth/login", "auth_sessions", "dexie_auth"),

    ("FR-002", "Role-Based Access Control (RBAC) Permissions Enforcement",
     "The platform shall restrict UI screens and API endpoints based on authenticated user roles (MO, Nurse, Pharmacist, Lab Tech, DEO).",
     "Authorization", "MUST", "Enforces least privilege and regulatory medical confidentiality.",
     "Application Gateway", "System Administrator", "ROLE-008", "STAKEHOLDER-015",
     "User invokes any API action or navigates UI route", "Active valid JWT session token present",
     "JWT bearer token, target endpoint, requested HTTP verb", "Token signature verified via RS256 public key, role in authorized list",
     "Request permitted or rejected with HTTP 403 Forbidden", "ALL /api/v1/*", "auth_roles", "dexie_roles"),

    ("FR-003", "Frontline Staff User Lifecycle Management",
     "The platform shall allow authorized Zonal Health Administrators to provision, suspend, and reassign clinic staff accounts.",
     "User Management", "MUST", "Ensures timely staff account provisioning and immediate revocation upon transfer.",
     "Zonal Administrator", "Zonal Health Officer", "ROLE-007", "STAKEHOLDER-012",
     "Zonal admin submits new staff profile or transfer request", "Admin authenticated with zonal supervisory privileges",
     "Employee ID, full name, clinical role, mobile number, assigned clinic ID", "KMC/KNC registration number format validation, valid clinic ID",
     "Staff account created and assigned to clinic roster", "POST /api/v1/admin/users", "clinic_staff", "dexie_staff"),

    ("FR-004", "Clinic Facility Profile & Operational Configuration",
     "The platform shall maintain clinic facility metadata including ward mapping, zone assignment, physical address, and operating hours.",
     "Clinic Management", "MUST", "Provides accurate facility context for reporting, GIS mapping, and indents.",
     "Facility Admin", "Medical Officer", "ROLE-001", "STAKEHOLDER-003",
     "Admin updates clinic operational attributes or holiday calendar", "Admin has facility administrative role",
     "Clinic ID, ward number (1-243), zone, contact phone, operating hours", "Ward number integer 1-243, valid GPS coordinates within Bengaluru",
     "Clinic profile updated and synchronized to central catalog", "PUT /api/v1/clinics/{id}", "clinic_facilities", "dexie_facility"),

    ("FR-005", "Automated Session Inactivity Lock & Secure Re-Authentication",
     "The platform shall automatically lock the workstation screen after 15 minutes of user inactivity, requiring PIN re-entry.",
     "Session Security", "MUST", "Protects open terminals in busy, shared clinic consultation spaces.",
     "Client Application", "All Clinic Staff", "ROLE-002", "STAKEHOLDER-015",
     "No mouse, keyboard, or touch event detected for 900 seconds", "User session currently in ACTIVE state",
     "Inactivity timer expiration signal, 4-digit re-auth PIN", "PIN matches local encrypted session credential",
     "Session state transitions to LOCKED until PIN re-entered", "POST /api/v1/auth/unlock", "auth_audit_log", "dexie_session"),

    ("FR-006", "Delegated Temporary Role Switching for Cross-Coverage",
     "The platform shall allow Medical Officers to authorize temporary role delegation during staff lunch breaks or emergency leaves.",
     "Operations Management", "SHOULD", "Maintains clinic flow when one staff member is temporarily indisposed.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-003",
     "Doctor activates delegation toggle for specific staff member", "Target staff member has verified baseline credentials",
     "Authorizing doctor ID, target staff ID, delegated role, expiry time", "Delegated role permitted under primary care matrix; max 4h duration",
     "Temporary role assigned with high-severity audit logging", "POST /api/v1/auth/delegate", "role_delegations", "dexie_auth"),

    ("FR-007", "Secure Password Reset via Zonal Admin or Mobile OTP",
     "The platform shall provide a self-service or supervisor-assisted password reset mechanism using verified mobile OTP.",
     "Access Recovery", "MUST", "Minimizes clinic downtime caused by forgotten passwords during morning rush.",
     "Clinic Staff", "Data Entry Operator", "ROLE-002", "STAKEHOLDER-012",
     "Staff clicks 'Forgot Password' on login screen", "Staff mobile number registered in BBMP HRMS",
     "Staff username, 6-digit SMS OTP, new password", "OTP valid within 5 minutes, password meets 12-char complexity rules",
     "Password hash updated in PostgreSQL using Argon2id", "POST /api/v1/auth/reset-password", "clinic_staff", "dexie_auth"),

    ("FR-008", "Immutable User Session & Authentication Audit Logging",
     "The platform shall record every login, logout, failed attempt, and session timeout to a secure, tamper-evident audit store.",
     "Security Telemetry", "MUST", "Enables forensic auditing of unauthorized access attempts.",
     "Security Subsystem", "Security Engineer", "ROLE-009", "STAKEHOLDER-015",
     "Any authentication event occurs at API gateway or client", "Event payload generated by auth middleware",
     "Timestamp, client IP, user ID, event type (SUCCESS/FAIL), user agent", "Structured JSON schema validation",
     "Audit event emitted to WORM storage in Grafana Loki", "POST /api/v1/telemetry/auth-events", "auth_audit_log", "dexie_audit"),

    # 09-18: Patient Registration, Demographics, ABHA & Search
    ("FR-009", "Walk-In Citizen Registration & Demographics Capture",
     "The platform shall capture citizen demographics including name, age/DOB, gender, mobile number, ward, and slum residence status.",
     "Patient Registration", "MUST", "Establishes legal patient identity and municipal demographic profile.",
     "Data Entry Operator", "Data Entry Operator", "ROLE-002", "STAKEHOLDER-001",
     "Unregistered citizen presents at front desk counter", "Front desk terminal operational in online or offline mode",
     "Full name, age or DOB, gender, 10-digit mobile, street address, ward ID", "Mobile regex [6-9][0-9]{9}, mandatory name and gender",
     "Patient master record created with UUIDv7 and municipal UHID", "POST /api/v1/patients", "patients", "dexie_patients"),

    ("FR-010", "Sub-Second Phonetic & Fuzzy Patient Search",
     "The platform shall execute real-time phonetic and fuzzy search across patient records by phone, name, UHID, or ABHA.",
     "Patient Identification", "MUST", "Prevents duplicate registrations and retrieves past medical history in <150ms.",
     "Data Entry Operator", "Data Entry Operator", "ROLE-002", "STAKEHOLDER-003",
     "Operator types query into registration search bar", "Patient index cached locally or central DB connected",
     "Search query string (phone number, partial name, or UHID)", "Minimum 3 characters for name, exact 10 digits for mobile",
     "Matching patient cards displayed ordered by relevance score", "GET /api/v1/patients/search", "patients", "dexie_patients"),

    ("FR-011", "Algorithmic Duplicate Patient Detection & Warning",
     "The platform shall compare incoming patient registrations against existing records using Levenshtein distance and phone matching.",
     "Data Quality", "MUST", "Prevents split medical records for the same citizen across multiple visits.",
     "Registration Engine", "Data Entry Operator", "ROLE-002", "STAKEHOLDER-001",
     "Operator submits new patient registration form", "Patient data passed to client/server validation pipe",
     "Candidate patient demographics (name, DOB, mobile, gender)", "Levenshtein similarity score >=0.85 on name + identical mobile",
     "Duplicate alert dialog displayed with 1-click 'Select Existing' option", "POST /api/v1/patients/check-duplicates", "patients", "dexie_patients"),

    ("FR-012", "Universal Health Identification (UHID) Minting",
     "The platform shall mint a unique, human-readable 14-character municipal UHID encoding year, zone, clinic, and sequential number.",
     "Patient Identity", "MUST", "Provides consistent physical identifier printed on tokens and cards.",
     "Identity Subsystem", "Data Entry Operator", "ROLE-002", "STAKEHOLDER-001",
     "New patient registration committed locally or centrally", "Valid patient record validated without duplication",
     "Clinic code, current year, atomic sequence counter", "Format `NC-YYYY-ZZ-XXXXXX` strictly validated",
     "UHID assigned to patient record and embedded in barcode", "POST /api/v1/patients/mint-uhid", "patients", "dexie_patients"),

    ("FR-013", "ABHA Creation via Aadhaar OTP & Demographic Authentication",
     "The platform shall integrate with the ABDM sandbox/production gateway to create 14-digit ABHA numbers via Aadhaar OTP.",
     "ABDM Integration", "MUST", "Connects municipal patients to the national digital health ecosystem.",
     "Data Entry Operator", "Data Entry Operator", "ROLE-002", "STAKEHOLDER-011",
     "Citizen requests ABHA creation and provides Aadhaar number", "Active WAN internet connectivity to ABDM gateway",
     "12-digit Aadhaar number, citizen consent checkbox, Aadhaar OTP", "Aadhaar Verhoeff algorithm check, 6-digit OTP verification",
     "ABHA number and ABHA address linked to patient UHID", "POST /api/v1/abdm/abha/create-otp", "patient_abha_links", "dexie_abha"),

    ("FR-014", "ABHA Verification via QR Code Scan",
     "The platform shall read and parse physical or digital ABHA QR codes using USB 2D barcode scanners, pre-filling registration fields.",
     "ABDM Integration", "MUST", "Reduces registration data entry time from 90 seconds to under 5 seconds.",
     "Data Entry Operator", "Data Entry Operator", "ROLE-002", "STAKEHOLDER-011",
     "Operator scans citizen's ABHA card QR code", "2D scanner configured in keyboard wedge mode",
     "Scanned JSON payload from ABHA QR code", "ABDM cryptographic signature verification on QR payload",
     "Registration form auto-populated with verified demographic data", "POST /api/v1/abdm/abha/verify-qr", "patient_abha_links", "dexie_abha"),

    ("FR-015", "Patient Demographic Record Correction & Change Auditing",
     "The platform shall allow authorized staff to correct spelling errors, phone numbers, or addresses with mandatory audit logging.",
     "Record Integrity", "MUST", "Ensures demographic accuracy while preventing fraudulent identity swapping.",
     "Facility Supervisor", "Medical Officer", "ROLE-001", "STAKEHOLDER-008",
     "Staff submits request to amend existing patient demographics", "Patient record exists and supervisor approves edit",
     "Patient UHID, field to update, new value, reason for correction", "Mandatory reason text (>10 chars), valid format for target field",
     "Demographics updated; prior values archived in audit history", "PATCH /api/v1/patients/{uhid}", "patient_history", "dexie_patients"),

    ("FR-016", "Family Unit Grouping & Household Health Linking",
     "The platform shall allow linking individual patient records to a common household head via shared ration card or phone number.",
     "Population Health", "SHOULD", "Enables holistic family epidemiological tracking and genetic risk analysis.",
     "Data Entry Operator", "Staff Nurse", "ROLE-003", "STAKEHOLDER-001",
     "Operator links secondary family member to existing primary account", "Both patient records registered in platform",
     "Head of household UHID, member UHID, relationship type", "Valid relationship enum (Spouse, Child, Parent, Sibling)",
     "Family relationship edge created in household graph", "POST /api/v1/patients/household-link", "household_members", "dexie_patients"),

    ("FR-017", "Citizen Consent Capture & Purpose Specification (DPDP Act)",
     "The platform shall capture and persist explicit citizen consent for health data processing, displaying notice in Kannada/English.",
     "Privacy Compliance", "MUST", "Fulfills legal obligations under India Digital Personal Data Protection Act 2023.",
     "Data Entry Operator", "Data Entry Operator", "ROLE-002", "STAKEHOLDER-008",
     "Registration submitted for new or returning patient", "Citizen presented with standardized bilingual consent notice",
     "Patient UHID, consent status (GRANTED/WITHDRAWN), purpose list", "Explicit affirmation required; zero pre-ticked checkboxes",
     "Signed cryptographic consent artifact stored in audit ledger", "POST /api/v1/privacy/consents", "privacy_consents", "dexie_consents"),

    ("FR-018", "Temporary Offline UHID Allocation & Central Reconciliation",
     "The platform shall generate guaranteed-unique offline UHIDs during network outages, reconciling them automatically upon reconnection.",
     "Offline Identity", "MUST", "Allows registration desk to function continuously without internet.",
     "Registration Engine", "Data Entry Operator", "ROLE-002", "STAKEHOLDER-003",
     "Patient registered while workstation is in OFFLINE mode", "Local Dexie.js database active with provisioned sequence pool",
     "Clinic workstation ID, local sequence number, timestamp", "Format `TEMP-ZZ-CCCC-XXXXXXXX` using cryptographically random suffix",
     "Temporary UHID assigned; sync queue holds mapping for server reconciliation", "POST /api/v1/offline/register", "patients", "dexie_patients"),

    # 19-26: OPD Queue, Token Dispensing & Triage Vitals
    ("FR-019", "Sequential Daily OPD Token Dispensing",
     "The platform shall issue sequentially numbered daily OPD tokens (starting from 001 at midnight) with estimated wait times.",
     "Queue Management", "MUST", "Ensures transparent, orderly patient queuing without disputes.",
     "Data Entry Operator", "Data Entry Operator", "ROLE-002", "STAKEHOLDER-003",
     "Patient registration finalized or returning patient checked in", "Patient has valid active UHID",
     "Patient UHID, visit type (General, ANC, NCD, Follow-up)", "Atomic sequence increment within current date boundary",
     "Active token record created in QUEUED state with sequential number", "POST /api/v1/queue/tokens", "queue_tokens", "dexie_queue"),

    ("FR-020", "Web Serial Thermal Slip Printing for OPD Tokens",
     "The platform shall communicate directly with connected ESC/POS thermal printers via Web Serial API to print visit tokens in <500ms.",
     "Peripheral Integration", "MUST", "Delivers physical, durable paper slips to citizens without driver dialogs.",
     "Workstation Client", "Data Entry Operator", "ROLE-002", "STAKEHOLDER-003",
     "Token generation committed locally or centrally", "Thermal printer connected via USB and Web Serial port open",
     "Token number, clinic name, date, patient UHID, QR code", "Standard ESC/POS raster and text commands formatted",
     "Token slip printed with high-contrast text and scannable QR", "CLIENT_WEB_SERIAL_PRINT", "hardware_telemetry", "dexie_queue"),

    ("FR-021", "Automated Priority Queue Insertion for Vulnerable Patients",
     "The platform shall route elderly (age >=65), pregnant, and disabled patients into a prioritized triage queue.",
     "Queue Governance", "MUST", "Protects frail citizens from prolonged physical waiting room distress.",
     "Queue Engine", "Data Entry Operator", "ROLE-002", "STAKEHOLDER-010",
     "Patient age >=65 or vulnerability flag checked during check-in", "Active queue session open for current date",
     "Patient UHID, priority category (ELDERLY, PREGNANT, INFANT, EMERGENCY)", "Priority category validated against demographic age or nurse override",
     "Token flagged PRIORITY and positioned ahead of standard tokens (2:1 ratio)", "PATCH /api/v1/queue/tokens/{id}/priority", "queue_tokens", "dexie_queue"),

    ("FR-022", "Multi-Parameter Nursing Vitals Capture & Validation",
     "The platform shall record blood pressure (systolic/diastolic), pulse rate, respiratory rate, SpO2, and body temperature.",
     "Triage Vitals", "MUST", "Establishes baseline physiological vitals before doctor consultation.",
     "Staff Nurse", "Staff Nurse", "ROLE-003", "STAKEHOLDER-002",
     "Patient arrives at nursing station with active visit token", "Patient called from waiting queue to triage room",
     "SBP (mmHg), DBP (mmHg), Pulse (bpm), SpO2 (%), Temp (F/C)", "SBP 60-260, DBP 40-160, Pulse 30-220, SpO2 50-100%, Temp 90-108F",
     "Vitals recorded and linked to visit; abnormal values highlighted in red", "POST /api/v1/clinical/vitals", "clinical_vitals", "dexie_vitals"),

    ("FR-023", "Automated Body Mass Index (BMI) & Growth Metrics",
     "The platform shall calculate adult BMI and pediatric growth z-scores automatically from measured height and weight.",
     "Clinical Triage", "MUST", "Identifies nutritional risks, obesity, and wasting without manual math.",
     "Staff Nurse", "Staff Nurse", "ROLE-003", "STAKEHOLDER-002",
     "Nurse inputs height and weight on triage screen", "Patient DOB and sex available from demographic record",
     "Height (cm), Weight (kg), Mid-Upper Arm Circumference (MUAC in mm)", "Height 30-220 cm, Weight 1.0-250.0 kg, MUAC 50-250 mm",
     "Calculates BMI = kg/m^2; assigns category (Underweight/Normal/Overweight/Obese)", "POST /api/v1/clinical/vitals/growth", "clinical_vitals", "dexie_vitals"),

    ("FR-024", "Point-of-Care Random Blood Sugar (RBS) Screening at Triage",
     "The platform shall record glucometer blood glucose readings for adults aged >=30 or symptomatic patients during nursing triage.",
     "NCD Screening", "MUST", "Enables instant opportunistic diabetes detection during routine visits.",
     "Staff Nurse", "Staff Nurse", "ROLE-003", "STAKEHOLDER-004",
     "Nurse performs capillary fingerstick blood glucose test", "Glucometer test strip used from verified inventory",
     "Glucose reading (mg/dL), meal state (Fasting, Post-Prandial, Random)", "Glucose reading 20-600 mg/dL, valid meal status",
     "Glucose recorded; values >=200 mg/dL flag diabetes review for doctor", "POST /api/v1/clinical/vitals/glucose", "clinical_vitals", "dexie_vitals"),

    ("FR-025", "Red-Flag Clinical Emergency Triage Alert Chime",
     "The platform shall trigger immediate audible and visual emergency alerts when triage vitals breach life-threatening thresholds.",
     "Patient Safety", "MUST", "Alerts doctor immediately to imminent shock, hypertensive crisis, or severe hypoxia.",
     "Triage Engine", "Staff Nurse", "ROLE-003", "STAKEHOLDER-002",
     "Vitals saved with SBP >=180, DBP >=120, SpO2 <90%, or Pulse >140", "Patient currently in triage room",
     "Measured vital values, patient UHID, token number", "Validation against critical physiological emergency boundaries",
     "Token status escalated to EMERGENCY; audio chime sounds on doctor screen", "POST /api/v1/clinical/triage/escalate", "queue_tokens", "dexie_queue"),

    ("FR-026", "Triage-to-Doctor Desk Handover & Electronic Queue Calling",
     "The platform shall allow Medical Officers to call the next triaged patient with a single click, updating waiting room displays.",
     "Queue Coordination", "MUST", "Eliminates physical nurse shouting and guides patients smoothly into the doctor's room.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-003",
     "Doctor finishes prior consultation and clicks 'Call Next Patient'", "Triaged patients present in doctor queue",
     "Doctor workstation ID, target token ID", "Token must be in TRIAGED state; highest priority called first",
     "Token transitions to CALLING / CONSULTING state; TV display chimes", "POST /api/v1/queue/call-next", "queue_tokens", "dexie_queue"),

    # 27-38: Doctor Consultation, EMR-Lite, ICD-10 & Prescribing
    ("FR-027", "1-Click Chief Complaint & Symptom Chip Selection",
     "The platform shall provide interactive chips for the Top 30 primary care chief complaints (e.g. fever, cough, joint pain, diarrhea).",
     "Clinical Productivity", "MUST", "Reduces clinical documentation typing time to maintain <4 minute consultations.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-004",
     "Doctor opens active patient consultation screen", "Patient token in CONSULTING state",
     "Selected complaint chips, duration (days/weeks), severity (Mild/Mod/Severe)", "Duration integer >= 1, valid severity enum",
     "Chief complaints appended to consultation note structure", "POST /api/v1/clinical/consultations/{id}/complaints", "clinical_encounters", "dexie_encounters"),

    ("FR-028", "Structured Physical Examination & Systemic Findings Notes",
     "The platform shall capture standardized physical examination findings (pallor, icterus, edema, chest auscultation, abdominal tenderness).",
     "Clinical Quality", "MUST", "Ensures structured clinical examination documentation for medicolegal safety.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-004",
     "Doctor examines patient and records systemic findings", "Active consultation encounter open",
     "General exam toggles, cardiovascular, respiratory, GI findings, free text", "Standardized physical examination vocabulary",
     "Examination findings committed to encounter record", "POST /api/v1/clinical/consultations/{id}/exam", "clinical_encounters", "dexie_encounters"),

    ("FR-029", "Curated Primary Care ICD-10 Diagnostic Code Search",
     "The platform shall provide typeahead search across a curated list of 250 primary care ICD-10 codes with Kannada synonyms.",
     "Diagnostic Coding", "MUST", "Eliminates ambiguous free-text diagnoses and enables epidemiological aggregation.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-007",
     "Doctor types diagnosis name or Kannada symptom in diagnosis box", "Active consultation encounter open",
     "Search string (e.g. 'dengue', 'ಜ್ವರ', 'hypertension')", "Minimum 2 characters; returns matching ICD-10 entities",
     "Selected ICD-10 code (e.g. I10, A90, E11.9) linked as primary/secondary diagnosis", "POST /api/v1/clinical/consultations/{id}/diagnosis", "clinical_diagnoses", "dexie_encounters"),

    ("FR-030", "Karnataka 120 Essential Drug List (EDL) Formulary Search",
     "The platform shall restrict medicine prescribing to the approved Karnataka 120 EDL with real-time clinic stock balance indicators.",
     "Formulary Control", "MUST", "Prevents prescribing unavailable drugs and guides doctors to stocked alternatives.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-005",
     "Doctor searches for medication in prescription pane", "Clinic pharmacy inventory loaded in client memory",
     "Drug generic name or brand synonym", "Matches approved 120 EDL catalog; displays current stock quantity",
     "Medication added to prescription with green (in-stock) or yellow (low) indicator", "GET /api/v1/pharmacy/formulary/search", "pharmacy_items", "dexie_formulary"),

    ("FR-031", "Structured Drug Dosage, Route, Frequency & Duration Input",
     "The platform shall enforce standardized dosing inputs (e.g., 500mg, Oral, 1-0-1, 5 days, After Food) with Kannada instruction printing.",
     "Prescription Safety", "MUST", "Eliminates handwritten prescription illegibility and dosage ambiguities.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-002",
     "Doctor selects drug entity from formulary", "Drug item selected in prescription builder",
     "Dose strength, route (Oral/Topical/IM/IV), frequency chip (TDS, BD, OD), duration", "Dosage within safe therapeutic limits for patient age and weight",
     "Structured prescription line item formatted with auto-translated Kannada instructions", "POST /api/v1/clinical/consultations/{id}/prescription-items", "prescription_items", "dexie_prescriptions"),

    ("FR-032", "Real-Time Drug-Drug Interaction (DDI) & Duplicate Alerting",
     "The platform shall evaluate candidate prescriptions against patient history for severe drug interactions and duplicate therapeutic classes.",
     "Patient Safety", "MUST", "Prevents life-threatening adverse drug events (e.g., ACE-I + ARB, NSAID + Anticoagulant).",
     "Clinical Decision Support", "Medical Officer", "ROLE-001", "STAKEHOLDER-002",
     "Doctor adds medication to active prescription list", "Two or more medications present on prescription or active meds list",
     "List of prescribed drug IDs, patient age, pregnancy status", "Rules engine checks contraindication and duplicate class matrix",
     "Displays high-severity warning banner with clinical rationale and override button", "POST /api/v1/clinical/cds/check-ddi", "clinical_rules", "dexie_cds"),

    ("FR-033", "Documented Clinical Override with Mandatory Reason Capture",
     "The platform shall require a structured override reason and clinical note before a doctor can bypass a high-severity clinical alert.",
     "Clinical Governance", "MUST", "Upholds clinician autonomy while maintaining a legal, auditable safety trail.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-002",
     "Doctor clicks 'Override Alert' on clinical safety warning dialog", "High-severity interaction, allergy, or dosage alert active",
     "Selected override category (Benefit Outweighs Risk, Patient Tolerated Previously, Specialist Advised), free-text note", "Mandatory note text (>=15 characters)",
     "Alert dismissed; override event logged with doctor ID and justification to WORM store", "POST /api/v1/clinical/cds/override", "cds_overrides", "dexie_audit"),

    ("FR-034", "Patient Drug Allergy Warning & Cross-Sensitivity Guard",
     "The platform shall check prescribed medications against documented patient drug allergies (e.g., Penicillin, Sulfa, NSAIDs).",
     "Allergy Safety", "MUST", "Prevents severe anaphylaxis and allergic reactions.",
     "Prescription Engine", "Medical Officer", "ROLE-001", "STAKEHOLDER-002",
     "Doctor selects medication for prescription", "Patient has documented allergies recorded in demographic or EMR profile",
     "Candidate drug code, patient allergy entity list", "Checks drug chemical family and known cross-sensitivity classes",
     "Hard-stop modal alert displayed if direct or cross-allergen detected", "POST /api/v1/clinical/cds/check-allergy", "patient_allergies", "dexie_encounters"),

    ("FR-035", "Pediatric Weight-Based Dosage Calculator (mg/kg/day)",
     "The platform shall calculate automated recommended syrup/liquid doses in ml based on pediatric patient weight and drug concentration.",
     "Pediatric Safety", "MUST", "Eliminates dangerous pediatric dosing miscalculations for syrups and suspensions.",
     "Prescription Engine", "Medical Officer", "ROLE-001", "STAKEHOLDER-002",
     "Doctor prescribes pediatric syrup to child (age <12 years)", "Child weight recorded in triage vitals",
     "Drug entity ID, child weight in kg, standard mg/kg/day guideline", "Valid weight > 0; calculated dose compared against maximum adult cap",
     "Pre-populates recommended dose in ml per administration with frequency", "POST /api/v1/clinical/cds/pediatric-dose", "formulary_dosages", "dexie_cds"),

    ("FR-036", "Non-Pharmacological Advice & Dietary Lifestyle Chips",
     "The platform shall provide standardized dietary and lifestyle advice chips (e.g., low salt for HTN, diabetic diet, hydration in fever).",
     "Preventive Counseling", "SHOULD", "Ensures structured preventive health counseling printed on patient slips.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-004",
     "Doctor completes diagnostic evaluation", "Active consultation session open",
     "Selected lifestyle advice chips, physical exercise recommendations, smoking cessation", "Standardized primary care lifestyle counseling taxonomy",
     "Advice items printed in Kannada and English on prescription slip", "POST /api/v1/clinical/consultations/{id}/lifestyle", "clinical_encounters", "dexie_encounters"),

    ("FR-037", "Follow-Up Appointment Date Scheduling & SMS Trigger",
     "The platform shall allow doctors to schedule follow-up dates (e.g., in 7, 14, or 30 days), triggering automated SMS reminders.",
     "Care Continuity", "MUST", "Ensures chronic disease and post-infection patients return for monitoring.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-004",
     "Doctor concludes consultation and selects follow-up interval", "Active consultation encounter open",
     "Follow-up date or interval chip (+1 Week, +2 Weeks, +1 Month), clinical reason", "Date must be a future clinic operating date (excluding holidays)",
     "Follow-up appointment registered; SMS reminder queued for T-24h", "POST /api/v1/clinical/consultations/{id}/follow-up", "appointments", "dexie_appointments"),

    ("FR-038", "Electronic Prescription Finalization & Digital Signature",
     "The platform shall finalize the encounter, generate an encrypted prescription artifact, and transmit it electronically to the pharmacy desk.",
     "Workflow Integration", "MUST", "Transfers orders instantly to the in-house pharmacy without paper transit delays.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-004",
     "Doctor reviews summary and clicks 'Sign & Finalize Consultation'", "Mandatory diagnosis recorded and at least one disposition selected",
     "Encounter ID, doctor digital signature/credential, final disposition", "State validation confirms zero unacknowledged severe CDS alerts",
     "Encounter closed; prescription status set to TRANSMITTED; token moves to PHARMACY queue", "POST /api/v1/clinical/consultations/{id}/finalize", "prescriptions", "dexie_prescriptions"),

    # 39-48: Point-of-Care Diagnostics, Lab Worklists & Panic Results
    ("FR-039", "Point-of-Care Laboratory Test Ordering from EMR",
     "The platform shall allow doctors to order any of the 14 approved rapid primary tests (e.g., Dengue NS1, Malaria RDT, Urine, Hb, Glucose).",
     "Diagnostic Workflow", "MUST", "Routes diagnostic work orders directly to the laboratory bench.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-002",
     "Doctor selects diagnostic test from 14 POC test panel", "Patient in CONSULTING state",
     "Test order codes, clinical indication, urgency (Routine/STAT)", "Selected tests exist in 14 POC master catalog",
     "Lab work order created; token routed to LAB queue; barcode printable", "POST /api/v1/lab/orders", "lab_orders", "dexie_lab"),

    ("FR-040", "Laboratory Worklist Queue & Specimen Accessioning",
     "The platform shall display an active laboratory worklist showing ordered tests, patient names, waiting times, and specimen status.",
     "Laboratory Management", "MUST", "Provides the lab technician with an orderly, prioritized testing bench.",
     "Lab Technician", "Lab Technician", "ROLE-005", "STAKEHOLDER-002",
     "Technician opens laboratory dashboard on clinic workstation", "Workstation authenticated with Lab Technician role",
     "Filter criteria (Pending Collection, In-Process, Completed)", "Standard worklist filter parameters",
     "Displays active patient test cards ordered by arrival timestamp and STAT priority", "GET /api/v1/lab/worklist", "lab_orders", "dexie_lab"),

    ("FR-041", "Specimen Barcode Tube Label Printing",
     "The platform shall print GS1-128 compliant 1D/2D barcode labels for blood and urine collection tubes via thermal label printers.",
     "Specimen Safety", "MUST", "Eliminates handwritten labels and guarantees tube identification.",
     "Lab Technician", "Lab Technician", "ROLE-005", "STAKEHOLDER-002",
     "Technician confirms sample collection from patient", "Patient present at lab bench; test order active",
     "Lab order ID, patient UHID, sample type (Capillary Blood, Venous, Urine)", "Atomic accession number formatted to GS1-128 spec",
     "Barcode label printed instantly; sample status updated to COLLECTED", "POST /api/v1/lab/specimens/print-label", "lab_specimens", "dexie_lab"),

    ("FR-042", "Structured Point-of-Care Qualitative & Quantitative Result Entry",
     "The platform shall provide customized input forms for each of the 14 rapid tests with physiological boundary validation.",
     "Laboratory Results", "MUST", "Prevents transcription typos and enforces standardized result units.",
     "Lab Technician", "Lab Technician", "ROLE-005", "STAKEHOLDER-002",
     "Technician enters observed test strip or device result", "Specimen in COLLECTED status; valid reagent lot logged",
     "Test ID, numeric value or qualitative toggle (Positive/Negative/Indeterminate), notes", "Numeric values bounded by biological plausibility (e.g. Hb 2.0-25.0 g/dL)",
     "Test result committed; status set to VERIFIED; audit log updated", "POST /api/v1/lab/orders/{id}/results", "lab_results", "dexie_lab"),

    ("FR-043", "Automated Reference Range Comparison & Visual Highlighting",
     "The platform shall evaluate entered lab results against age- and sex-specific normal reference ranges, flagging abnormal values.",
     "Diagnostic Safety", "MUST", "Assists clinicians in quickly identifying abnormal laboratory parameters.",
     "Diagnostic Engine", "Lab Technician", "ROLE-005", "STAKEHOLDER-002",
     "Technician saves quantitative laboratory result", "Patient age and gender available from demographic record",
     "Measured analyte value, test analyte code, patient sex/age", "Reference range lookup against standard ICMR primary care norms",
     "Result annotated as LOW, NORMAL, or HIGH with yellow visual flag", "POST /api/v1/lab/results/evaluate-ranges", "lab_reference_ranges", "dexie_lab"),

    ("FR-044", "Sub-30-Second Panic Value Alert Transmission to Doctor Screen",
     "The platform shall immediately broadcast a critical panic value banner and audible chime to the doctor terminal when lab values breach danger limits.",
     "Emergency Response", "MUST", "Ensures immediate clinical action before patient leaves the clinic premises.",
     "Diagnostic Engine", "Medical Officer", "ROLE-001", "STAKEHOLDER-002",
     "Lab result entered with Hb < 6.0 g/dL, Glucose > 400 mg/dL, or positive Dengue NS1 with shock vitals", "Doctor workstation online and patient in clinic",
     "Critical result payload, patient UHID, technician ID, severity code", "Critical boundary trigger validation",
     "Emergency banner overrides doctor screen with audible chime within 15 seconds", "POST /api/v1/lab/alerts/panic", "lab_panic_alerts", "dexie_lab"),

    ("FR-045", "Reagent Kit Lot Tracking & Quality Control Logging",
     "The platform shall record reagent kit lot numbers, expiration dates, and morning control results before allowing daily patient testing.",
     "Laboratory Governance", "MUST", "Guarantees test reliability and prevents use of degraded diagnostic chemicals.",
     "Lab Technician", "Lab Technician", "ROLE-005", "STAKEHOLDER-002",
     "Technician initializes lab testing at start of shift (09:00 IST)", "New or active reagent kit box opened",
     "Test type, manufacturer, lot number, expiry date, control test outcome (PASS/FAIL)", "Expiry date must be in future; control must be PASS",
     "Reagent batch authorized for daily testing; failures block result entry", "POST /api/v1/lab/qc/log-batch", "lab_reagent_batches", "dexie_lab"),

    ("FR-046", "Consolidated Laboratory Diagnostic Report Generation",
     "The platform shall compile all finalized lab results into a printable PDF report with BBMP header and technician digital sign-off.",
     "Diagnostic Reporting", "MUST", "Provides patients and referral hospitals with official documented diagnostic results.",
     "Lab Technician", "Lab Technician", "ROLE-005", "STAKEHOLDER-002",
     "All ordered tests for encounter finalized", "All line items in VERIFIED state",
     "Encounter ID, technician digital signature, verification timestamp", "State validation confirms zero pending tests",
     "Encrypted diagnostic PDF generated and attached to patient EMR", "POST /api/v1/lab/reports/generate-pdf", "lab_reports", "dexie_lab"),

    ("FR-047", "External Diagnostic Sample Referral Tracking",
     "The platform shall track specialized laboratory specimens sent to BBMP central laboratories or external referral centers.",
     "Diagnostic Continuity", "SHOULD", "Tracks specialized samples (e.g. Sputum CBNAAT, Pap smear) to prevent lost specimens.",
     "Lab Technician", "Lab Technician", "ROLE-005", "STAKEHOLDER-006",
     "Technician packages specimen for transport to central lab", "Specialized test ordered by Medical Officer",
     "Specimen ID, destination lab code, courier pickup timestamp, cold box temp", "Destination facility in approved BBMP laboratory network",
     "Specimen status set to IN_TRANSIT; courier manifest generated", "POST /api/v1/lab/external-referrals", "lab_external_referrals", "dexie_lab"),

    ("FR-048", "Rapid Diagnostic Test Cassette Photo Ingestion",
     "The platform shall allow lab technicians to capture and attach a high-resolution smartphone/webcam photo of the rapid test cassette.",
     "Diagnostic Verification", "SHOULD", "Provides verifiable visual proof of test strip bands for remote tele-supervision.",
     "Lab Technician", "Lab Technician", "ROLE-005", "STAKEHOLDER-002",
     "Technician completes rapid lateral flow test (e.g. Dengue, Malaria, Pregnancy)", "Webcam or USB camera connected to terminal",
     "Cassette image stream, order ID, test analyte", "Image resolution >= 720p; JPEG compressed <500KB",
     "Image encrypted and persisted in MinIO/S3 attachment store", "POST /api/v1/lab/orders/{id}/attach-photo", "lab_attachments", "dexie_lab"),

    # 49-58: Pharmacy Dispensing, 120 EDL Inventory & Batch Tracking
    ("FR-049", "Electronic Prescription Retrieval at Pharmacy Counter",
     "The platform shall display finalized prescriptions on the pharmacy terminal upon scanning the patient token barcode or searching UHID.",
     "Pharmacy Workflow", "MUST", "Eliminates paper prescription handling and queuing bottlenecks.",
     "Pharmacist", "Pharmacist", "ROLE-004", "STAKEHOLDER-005",
     "Pharmacist scans token barcode or enters UHID", "Prescription finalized by doctor in TRANSMITTED status",
     "Scanned barcode string or UHID", "Barcode parses to valid active token ID",
     "Prescription displayed with medication list, prescribed quantities, and stock availability", "GET /api/v1/pharmacy/prescriptions/{id}", "prescriptions", "dexie_pharmacy"),

    ("FR-050", "Automated First-Expired, First-Out (FEFO) Batch Recommendation",
     "The platform shall automatically suggest the exact medicine batch with the earliest expiration date for every prescribed drug.",
     "Inventory Optimization", "MUST", "Prevents medicine expiration on clinic shelves and enforces municipal FEFO rules.",
     "Pharmacy Engine", "Pharmacist", "ROLE-004", "STAKEHOLDER-005",
     "Pharmacist selects prescription line item for picking", "Multiple active batches exist in clinic inventory",
     "Drug entity ID, requested quantity, clinic ID", "Sorts inventory batches by expiry_date ASC where balance > 0",
     "Pre-selects earliest expiry batch and highlights shelf rack location", "POST /api/v1/pharmacy/batches/fefo-recommend", "inventory_batches", "dexie_inventory"),

    ("FR-051", "Barcode Scan Verification of Dispensed Medicine Packaging",
     "The platform shall require the pharmacist to scan the physical 1D/2D barcode on the medicine box/strip before dispensing confirmation.",
     "Dispensing Safety", "MUST", "Prevents Look-Alike Sound-Alike (LASA) dispensing errors in busy clinic pharmacies.",
     "Pharmacist", "Pharmacist", "ROLE-004", "STAKEHOLDER-005",
     "Pharmacist picks physical medicine from shelf and scans packaging barcode", "Prescription line item open on dispensing screen",
     "Scanned barcode string (EAN-13, GS1 DataMatrix), selected batch ID", "Scanned barcode exactly matches prescribed drug entity code",
     "Line item verified with green checkmark; sound confirmation emitted", "POST /api/v1/pharmacy/dispense/verify-barcode", "inventory_batches", "dexie_pharmacy"),

    ("FR-052", "Partial Dispensing & Out-of-Stock Counseling Recording",
     "The platform shall support partial dispensing when local stock is insufficient, recording dispensed quantity and counseling note.",
     "Pharmacy Operations", "MUST", "Maintains exact stock ledger while documenting unfulfilled prescription items.",
     "Pharmacist", "Pharmacist", "ROLE-004", "STAKEHOLDER-005",
     "Available batch balance is less than prescribed quantity", "Prescription line item active",
     "Dispensed quantity, balance unfulfilled, reason code (Partial Stock, Stockout)", "Dispensed quantity <= available batch balance",
     "Stock decremented by dispensed quantity; patient receipt notes remaining balance", "POST /api/v1/pharmacy/dispense/partial", "prescription_dispensations", "dexie_pharmacy"),

    ("FR-053", "Real-Time Inventory Balance Decrement & Stock Ledger Audit",
     "The platform shall atomically decrement clinic inventory upon dispensing confirmation, writing an immutable double-entry stock ledger record.",
     "Inventory Ledger", "MUST", "Ensures 100% accurate real-time inventory balances and prevents medicine theft.",
     "Pharmacy Engine", "Pharmacist", "ROLE-004", "STAKEHOLDER-005",
     "Pharmacist clicks 'Confirm Dispensing' for complete prescription", "All line items either verified or explicitly marked unfulfilled",
     "Prescription ID, pharmacist ID, batch IDs, quantities deducted", "Atomic transaction isolation; balances must not go below zero",
     "Inventory batches decremented; stock ledger record committed; receipt printed", "POST /api/v1/pharmacy/dispense/commit", "inventory_ledger", "dexie_inventory"),

    ("FR-054", "Digital Stock Receipt Ingestion from Zonal Warehouse",
     "The platform shall ingest electronic delivery challans from the BBMP zonal medical warehouse, updating clinic stock upon physical receipt.",
     "Stock Receipt", "MUST", "Eliminates manual paper stock entry and reconciles shipments automatically.",
     "Pharmacist", "Pharmacist", "ROLE-004", "STAKEHOLDER-005",
     "Delivery shipment arrives at clinic from BBMP warehouse", "Warehouse delivery challan exists in electronic exchange",
     "Challan number, drug codes, batch numbers, manufacturer, expiry dates, quantities", "Physical verification against digital challan; barcode spot check",
     "New batches created in clinic inventory ledger; electronic receipt acknowledged", "POST /api/v1/pharmacy/stock-receipts", "stock_receipts", "dexie_inventory"),

    ("FR-055", "Automated Buffer Threshold Stockout Alerts",
     "The platform shall generate visual low-stock alerts when any of the 120 EDL medicines breaches its defined 7-day buffer threshold.",
     "Supply Chain Alerting", "MUST", "Enables proactive stock replenishment before total facility stockout occurs.",
     "Inventory Daemon", "Pharmacist", "ROLE-004", "STAKEHOLDER-005",
     "Dispensing decrement or scheduled inventory audit runs", "Clinic inventory active",
     "Current batch balance sum, 30-day average daily consumption (ADC)", "Total balance < (ADC * 7 days buffer threshold)",
     "Drug status flagged as LOW_STOCK; highlighted on dashboard; added to indent list", "POST /api/v1/pharmacy/alerts/stockout", "pharmacy_items", "dexie_inventory"),

    ("FR-056", "Near-Expiry Medicine Quarantine & Return Workflow",
     "The platform shall automatically flag batches expiring within 60 days and provide a structured quarantine and return-to-warehouse workflow.",
     "Waste Reduction", "MUST", "Prevents accidental dispensing of expired stock and facilitates municipal batch re-allocation.",
     "Pharmacist", "Pharmacist", "ROLE-004", "STAKEHOLDER-005",
     "Batch expiry date reaches T-60 days or pharmacist initiates quarantine", "Batch currently in active dispensing status",
     "Batch ID, current balance, quarantine reason, target warehouse", "Requires supervisor digital sign-off to finalize quarantine transfer",
     "Batch status set to QUARANTINED; removed from active dispensing search", "POST /api/v1/pharmacy/batches/{id}/quarantine", "inventory_batches", "dexie_inventory"),

    ("FR-057", "Discrepancy Stock Adjustment with Dual Supervisor Approval",
     "The platform shall allow physical stock adjustments (breakage, spill, theft) only with mandatory reason capture and Medical Officer approval.",
     "Loss Prevention", "MUST", "Prevents unauthorized inventory write-offs and pilferage of essential antibiotics.",
     "Pharmacist", "Pharmacist", "ROLE-004", "STAKEHOLDER-003",
     "Physical count differs from system balance during weekly stock audit", "Adjustment request submitted on pharmacy terminal",
     "Drug ID, batch number, physical count, adjustment delta, adjustment reason", "Adjustment > 10 units requires Medical Officer password authentication",
     "Inventory balance adjusted; variance recorded in loss prevention audit ledger", "POST /api/v1/pharmacy/stock-adjustments", "stock_adjustments", "dexie_inventory"),

    ("FR-058", "Automated Rolling 30-Day Indent Calculation & 1-Click Submission",
     "The platform shall calculate recommended replenishment indents using standard consumption algorithms and submit them to the zonal warehouse.",
     "Supply Chain Automation", "MUST", "Replaces error-prone manual arithmetic with standardized consumption forecasting.",
     "Pharmacist", "Pharmacist", "ROLE-004", "STAKEHOLDER-005",
     "Pharmacist opens weekly indent generation module", "Active clinic stock ledger verified",
     "Historical 30-day dispensing data, current stock, lead time (5 days)", "Applies formula: Indent = (ADC * LeadTime) + SafetyStock - CurrentStock",
     "Structured indent document generated; 1-click transmission to BBMP warehouse", "POST /api/v1/pharmacy/indents/generate", "stock_indents", "dexie_inventory"),

    # 59-66: Referrals, Follow-Up, Maternal & NCD Specialized Care
    ("FR-059", "Secondary Hospital Referral Slip Generation with Bharat QR",
     "The platform shall generate digital referral slips to BBMP secondary hospitals (e.g. KC General, Bowring) with encrypted Bharat QR summaries.",
     "Referral Continuity", "MUST", "Ensures hospital emergency doctors receive vital clinic findings and provisional diagnoses.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-006",
     "Doctor decides patient requires secondary/tertiary hospital care", "Encounter notes, diagnosis, and vitals documented",
     "Referral hospital code, department (OBG, Cardiology, Surgery), urgency, clinical summary", "Hospital code exists in verified BBMP hospital registry",
     "Referral slip printed with secure QR code; referral transaction logged to central hub", "POST /api/v1/referrals/create", "referral_records", "dexie_referrals"),

    ("FR-060", "Counter-Referral Clinical Discharge Note Ingestion",
     "The platform shall capture hospital discharge summaries and counter-referral notes when patients return to their neighborhood Namma Clinic.",
     "Loop Closure", "MUST", "Closes the referral loop, informing neighborhood doctors of hospital treatments.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-006",
     "Referred patient returns to Namma Clinic for follow-up care", "Active referral record exists in platform history",
     "Referral ID, hospital discharge summary text, discharge meds, follow-up advice", "Valid referral ID; doctor verifies hospital documentation",
     "Referral status updated to CLOSED_COMPLETED; counter-referral notes linked to EMR", "POST /api/v1/referrals/{id}/close", "referral_records", "dexie_referrals"),

    ("FR-061", "Maternal Antenatal Care (ANC) Registration & Trimester Tracking",
     "The platform shall register pregnant women, track LMP/EDD, and schedule mandatory ANC 1, 2, 3, and 4 clinical checkups.",
     "Maternal Health", "MUST", "Guarantees comprehensive antenatal care and reduces maternal mortality in urban slums.",
     "Staff Nurse", "Staff Nurse", "ROLE-003", "STAKEHOLDER-002",
     "Pregnant woman visits clinic for initial antenatal checkup", "Pregnancy confirmed by urine test or ultrasound",
     "LMP date, gravidity, parity, living children, blood group, Td immunization history", "LMP date within past 42 weeks; EDD calculated as LMP + 280 days",
     "Patient registered in ANC cohort; personalized visit schedule generated", "POST /api/v1/maternal/anc/register", "maternal_anc_registry", "dexie_maternal"),

    ("FR-062", "High-Risk Pregnancy (HRP) Red-Flag Identification & Tagging",
     "The platform shall evaluate obstetric risk factors and automatically tag high-risk pregnancies, alerting the Zonal MCH Officer.",
     "Maternal Safety", "MUST", "Ensures intensive monitoring and planned institutional delivery for vulnerable mothers.",
     "Clinical Rules Engine", "Staff Nurse", "ROLE-003", "STAKEHOLDER-002",
     "ANC visit saved with SBP >=140, Hb < 7.0 g/dL, teenage pregnancy, or previous C-section", "Patient registered in ANC care module",
     "Measured clinical parameters, past obstetric history", "Rule engine matches criteria against National Health Mission HRP guidelines",
     "Patient tagged with prominent HIGH_RISK_ANC badge; escalated to zonal review list", "POST /api/v1/maternal/anc/{id}/tag-hrp", "maternal_hrp_tags", "dexie_maternal"),

    ("FR-063", "Non-Communicable Disease (NCD) Cohort Enrollment & Longitudinal Monitoring",
     "The platform shall enroll confirmed hypertensive and diabetic patients into an active longitudinal chronic care cohort.",
     "NCD Care", "MUST", "Tracks blood pressure and glycemic control over monthly follow-up visits.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-004",
     "Patient diagnosed with Essential Hypertension (I10) or Type 2 Diabetes (E11)", "Active consultation encounter open",
     "Patient UHID, diagnosis date, baseline SBP/DBP, baseline FBS/HbA1c, assigned nurse", "Valid ICD-10 NCD diagnosis entity",
     "Patient added to clinic NCD cohort; monthly refill appointment cycle initialized", "POST /api/v1/ncd/cohort/enroll", "ncd_cohort", "dexie_ncd"),

    ("FR-064", "NCD Treatment Adherence & Missed Appointment Defaulter Tracking",
     "The platform shall generate weekly lists of NCD patients who missed their scheduled medicine refill visits by more than 7 days.",
     "Adherence Tracking", "MUST", "Enables ASHA workers to conduct home visits before patients suffer strokes or renal failure.",
     "NCD Subsystem", "Staff Nurse", "ROLE-003", "STAKEHOLDER-004",
     "Scheduled Monday morning NCD cohort adherence audit runs", "Clinic NCD cohort active with scheduled follow-up dates",
     "Cohort appointment records, current date", "Identifies patients with scheduled_date < (current_date - 7 days) and no visit",
     "Defaulter list generated for ASHA worker outreach; automated reminder SMS queued", "GET /api/v1/ncd/cohort/defaulters", "ncd_appointments", "dexie_ncd"),

    ("FR-065", "Postnatal Care (PNC) Visit Tracking within 42 Days Post-Delivery",
     "The platform shall track scheduled PNC visits at 48 hours, 7 days, 14 days, and 42 days, monitoring maternal vitals and infant feeding.",
     "Postnatal Safety", "MUST", "Prevents postpartum sepsis, hemorrhage, and infant failure to thrive.",
     "Staff Nurse", "Staff Nurse", "ROLE-003", "STAKEHOLDER-002",
     "Mother and newborn attend clinic for postnatal visit", "Delivery event registered in maternal records",
     "Delivery date, birth weight, maternal BP, lochia status, breastfeeding status, baby temp", "Delivery date within past 42 days; valid maternal and neonatal physiological bounds",
     "PNC visit recorded; immunization schedule for newborn initialized", "POST /api/v1/maternal/pnc/record-visit", "maternal_pnc_registry", "dexie_maternal"),

    ("FR-066", "Pediatric Immunization Cold-Chain Batch Linkage",
     "The platform shall record vaccine administration linking specific child UHIDs to vaccine lot numbers, diluent lots, and injection sites.",
     "Immunization Tracking", "MUST", "Provides complete vaccine traceability and safety monitoring for national immunization.",
     "Staff Nurse", "Staff Nurse", "ROLE-003", "STAKEHOLDER-009",
     "Nurse administers scheduled vaccine (e.g. Pentavalent, MR, BCG) to child", "Child registered in pediatric immunization schedule",
     "Vaccine antigen code, batch lot number, dose number, route/site, adverse reaction check", "Batch lot exists in active clinic cold chain inventory and is not expired",
     "Immunization record committed; next due vaccination date calculated", "POST /api/v1/pediatric/immunizations", "immunization_records", "dexie_immunization"),

    # 67-74: Offline Architecture, Data Sync & Conflict Resolution
    ("FR-067", "Client-Side IndexedDB Offline Data Storage (Dexie.js)",
     "The platform shall persist all patient registrations, triage vitals, consultations, lab results, and stock transactions in local IndexedDB.",
     "Offline Architecture", "MUST", "Guarantees 100% autonomous clinic operation during network failures.",
     "Client Storage Subsystem", "All Clinic Staff", "ROLE-002", "STAKEHOLDER-003",
     "Any operational transaction executed on clinic workstation", "Workstation browser active with IndexedDB support",
     "Transaction payload, monotonic UUIDv7 entity key, table name", "Local schema validation via TypeScript TypeBox definitions",
     "Data written to local Dexie.js store in <10ms; visible instantly in local UI", "LOCAL_DEXIE_TRANSACTION", "dexie_local_db", "dexie_all"),

    ("FR-068", "FIFO Mutation Queue Buffer with Cryptographic Checksums",
     "The platform shall buffer all local state changes into an append-only FIFO mutation queue with SHA-256 integrity checksums.",
     "Offline Synchronization", "MUST", "Guarantees transactional ordering and tamper-evident queuing during offline periods.",
     "Sync Subsystem", "All Clinic Staff", "ROLE-002", "STAKEHOLDER-003",
     "Local transaction commits to IndexedDB store", "Mutation queue manager operational",
     "Mutation sequence ID, entity table, operation (CREATE/UPDATE), payload, timestamp", "Computes SHA-256 hash across sequence ID, timestamp, and JSON payload",
     "Mutation appended to pending sync queue with status QUEUED", "LOCAL_MUTATION_QUEUE_APPEND", "mutation_queue", "dexie_sync"),

    ("FR-069", "Automated Network State Detection & Reconnection Handshake",
     "The platform shall monitor network reachability via WebSocket heartbeats and DNS probes, detecting connectivity state transitions.",
     "Network Resilience", "MUST", "Coordinates smooth transitions between offline, reconnecting, and synchronized states.",
     "Client Network Daemon", "System Administrator", "ROLE-009", "STAKEHOLDER-016",
     "Periodic 5-second network probe or browser online/offline event", "Clinic terminal active",
     "WebSocket ping/pong latency, HTTP health check endpoint status", "Confirms end-to-end API reachability, not merely local Wi-Fi link",
     "Updates global connection state (ONLINE, OFFLINE, RECONNECTING, SYNCING)", "GET /api/v1/health/ping", "network_telemetry", "dexie_telemetry"),

    ("FR-070", "Idempotent Chunked Mutation Synchronization Replay",
     "The platform shall transmit buffered mutations to the central cluster in batches of 50 using unique `X-Idempotency-Key` headers.",
     "Data Synchronization", "MUST", "Prevents duplicate records even if network drops during sync response delivery.",
     "Background Sync Daemon", "System Administrator", "ROLE-009", "STAKEHOLDER-016",
     "Network state transitions to ONLINE and pending mutations exist in queue", "Valid authenticated session with central sync endpoint",
     "Batch of up to 50 mutation records, clinic certificate, idempotency keys", "Server validates idempotency key cache before applying transaction",
     "Mutations committed to central PostgreSQL; sync queue entries updated to COMMITTED", "POST /api/v1/sync/replay-mutations", "mutation_journal", "dexie_sync"),

    ("FR-071", "Deterministic Conflict Resolution Rules Engine",
     "The platform shall resolve synchronization conflicts deterministically using domain-specific rules (e.g. server wins on identity, append on notes).",
     "Conflict Handling", "MUST", "Maintains database integrity without manual developer intervention or data loss.",
     "Sync Conflict Engine", "Solution Architect", "ROLE-001", "STAKEHOLDER-017",
     "Central server detects concurrent edit conflict on synchronized entity", "Incoming mutation timestamp conflicts with committed server version",
     "Incoming mutation payload, existing database record, entity type", "Evaluates conflict resolution matrix: Registrations->Merge; Notes->Append; Stock->Reconcile",
     "Resolved state committed; conflict resolution log entry created for audit", "POST /api/v1/sync/resolve-conflict", "sync_conflicts", "dexie_sync"),

    ("FR-072", "Master Data Catalog Caching & Differential Updates",
     "The platform shall cache master catalogs (120 EDL medicines, ICD-10 codes, staff rosters, clinic metadata) with ETag-based updates.",
     "Client Performance", "MUST", "Enables instant local lookups and minimizes WAN bandwidth consumption.",
     "Client Cache Manager", "Data Entry Operator", "ROLE-002", "STAKEHOLDER-016",
     "Application startup or scheduled daily catalog refresh (08:30 IST)", "Active network connection to central server",
     "Catalog entity name, cached client version/ETag", "Server compares ETags; returns HTTP 304 Not Modified or delta JSON payload",
     "Local Dexie.js master catalogs updated; zero UI latency during daily searches", "GET /api/v1/catalogs/{name}", "master_catalogs", "dexie_catalogs"),

    ("FR-073", "Offline Queue Backlog Monitoring & Health Warnings",
     "The platform shall monitor local mutation queue depth, displaying a visual badge and warning when pending offline items exceed 200.",
     "Operational Telemetry", "MUST", "Alerts staff if local data is failing to synchronize for extended periods.",
     "Client UI Subsystem", "Medical Officer", "ROLE-001", "STAKEHOLDER-003",
     "Queue depth check executed after every local transaction", "Workstation terminal active",
     "Count of uncommitted records in local mutation queue", "Integer count of pending records",
     "Displays green badge (<50), yellow badge (50-200), or red flashing badge (>200 items)", "CLIENT_QUEUE_DEPTH_CHECK", "queue_telemetry", "dexie_sync"),

    ("FR-074", "Cryptographic Local IndexedDB Storage Encryption",
     "The platform shall encrypt sensitive citizen PII and clinical notes stored in IndexedDB using AES-GCM via the Web Cryptography API.",
     "Client Security", "MUST", "Protects patient data at rest on physical clinic workstations against physical disk theft.",
     "Client Crypto Engine", "Security Engineer", "ROLE-009", "STAKEHOLDER-015",
     "Local transaction written to Dexie.js IndexedDB tables", "Workstation initialized with clinic derived encryption key",
     "Plaintext JSON payload, initialization vector (IV), clinic master key", "AES-GCM 256-bit authenticated encryption via native browser crypto",
     "Ciphertext persisted to IndexedDB; plaintext decrypted only in volatile application memory", "CLIENT_WEB_CRYPTO_ENCRYPT", "client_security_log", "dexie_secure"),

    # 75-80: Supervisor Functions, End-of-Day Reconciliation & Admin
    ("FR-075", "Clinic Morning Opening Readiness Checklist",
     "The platform shall enforce a digital morning opening checklist (power, internet, cold chain, printer, stock) before tokens can be dispensed.",
     "Facility Readiness", "MUST", "Ensures clinic infrastructure is fully prepared before patients enter the facility.",
     "Staff Nurse", "Staff Nurse", "ROLE-003", "STAKEHOLDER-003",
     "First staff member logs into clinic terminal at morning opening (08:30 IST)", "Workstation booted and clinic operational profile loaded",
     "ILR temp reading, printer test slip print status, emergency tray check, water/power status", "All mandatory checks marked YES/PASS; non-compliant items require explanation",
     "Clinic status transitions from CLOSED to OPEN; token dispensing counter enabled", "POST /api/v1/clinic/operations/morning-checklist", "clinic_checklists", "dexie_facility"),

    ("FR-076", "End-of-Day (EOD) Clinic Reconciliation & Daily Session Closure",
     "The platform shall require the Medical Officer to execute daily session closure, reconciling open tokens, stock dispenses, and cash/exemptions.",
     "Operational Governance", "MUST", "Guarantees zero unfinalized patient records or missing pharmaceutical tallies at day close.",
     "Medical Officer", "Medical Officer", "ROLE-001", "STAKEHOLDER-003",
     "Clinic operating hours conclude at 17:30 IST", "All consultations completed or explicitly cancelled",
     "Total footfall, finalized visits, unfulfilled prescriptions, daily medicine tally", "Confirms zero tokens remaining in CALLING or CONSULTING states",
     "Daily session locked; final reconciliation summary transmitted to BBMP command center", "POST /api/v1/clinic/operations/eod-closure", "clinic_sessions", "dexie_facility"),

    ("FR-077", "Supervisor Retrospective Data Correction Approval",
     "The platform shall require secondary Zonal Medical Officer approval for any retrospective amendments to finalized clinical encounters.",
     "Audit Integrity", "MUST", "Prevents illicit post-hoc falsification of medicolegal clinical records.",
     "Zonal Medical Officer", "Zonal Health Officer", "ROLE-007", "STAKEHOLDER-008",
     "Doctor submits request to amend finalized consultation notes", "Encounter finalized >24 hours prior",
     "Encounter ID, doctor ID, requested amendment text, formal clinical justification", "Mandatory clinical justification; dual authentication by Zonal MO",
     "Amendment appended as an addendum to encounter; original text preserved in WORM log", "POST /api/v1/admin/approvals/amendment", "encounter_addenda", "dexie_encounters"),

    ("FR-078", "Master Data Synchronization & Formulary Override by Zonal Admin",
     "The platform shall allow Zonal Health Authorities to push emergency formulary additions or disease outbreak alerts across all 183 clinics.",
     "Administrative Control", "MUST", "Enables rapid coordinated municipal response during health crises.",
     "Zonal Administrator", "Chief Health Officer", "ROLE-007", "STAKEHOLDER-001",
     "Zonal admin issues emergency formulary update or epidemic alert", "Authenticated with municipal administrative role",
     "Target clinics (All or Zone-specific), alert message, formulary update payload", "Cryptographic signature from BBMP Health Directorate",
     "Pushed via WebSocket broadcast to all active clinic terminals; acknowledged locally", "POST /api/v1/admin/broadcast-update", "admin_broadcasts", "dexie_telemetry"),

    ("FR-079", "Comprehensive Facility Operational Telemetry Dashboard",
     "The platform shall display real-time operational telemetry for each clinic (active tokens, wait times, consultations, stockouts, sync lag).",
     "Operational Visibility", "MUST", "Gives clinic doctors and zonal supervisors instant visibility into clinic bottlenecks.",
     "Facility Supervisor", "Medical Officer", "ROLE-001", "STAKEHOLDER-003",
     "User opens clinic operational overview tab", "Terminal authenticated with clinic staff or supervisor credentials",
     "Clinic ID, date boundary", "Aggregates real-time in-memory and database metrics",
     "Renders dashboard cards with live wait times, queue counts, and equipment status", "GET /api/v1/telemetry/facility-dashboard", "clinic_telemetry", "dexie_telemetry"),

    ("FR-080", "System-Wide Immutable Audit Trail Search & Export",
     "The platform shall allow authorized municipal audit officers to search and export tamper-evident audit logs across any clinic or user.",
     "Compliance & Audit", "MUST", "Provides comprehensive auditing for municipal oversight, anti-corruption, and legal inquiries.",
     "Municipal Audit Officer", "Chief Health Officer (Administration)", "ROLE-008", "STAKEHOLDER-015",
     "Auditor submits query for clinical mutations, stock adjustments, or user sessions", "Auditor authenticated with specialized read-only audit credentials",
     "Date range, target clinic ID, user ID, event type filter", "Date range <= 90 days per query; valid audit query parameters",
     "Returns cryptographically signed audit log extract with SHA-256 integrity verification", "GET /api/v1/admin/audit-logs/export", "audit_logs", "dexie_audit")
]

def generate_data_fr():
    target_path = os.path.join(os.path.dirname(__file__), "data_fr.py")
    lines = []
    lines.append("#!/usr/bin/env python3")
    lines.append('"""')
    lines.append("data_fr.py")
    lines.append("Canonical dataset for Functional Requirements (FR-001 through FR-080).")
    lines.append("Complete, domain-specific primary healthcare functional specifications for Namma Clinic.")
    lines.append('"""')
    lines.append("")
    lines.append("FR_REQUIREMENTS = [")

    for i, item in enumerate(FR_DEFINITIONS, 1):
        (req_id, title, statement, domain, priority, b_val,
         actor, persona_role, role, stakeholder, trigger, precond,
         inputs, validation, postcond, api_endpoint, db_table, dexie_store) = item

        obj_idx = ((i - 1) % 40) + 1
        sc_idx = ((i - 1) % 40) + 1
        insc_idx = i
        risk_idx = ((i - 1) % 60) + 1
        dep_idx = ((i - 1) % 50) + 1
        m_idx = ((i - 1) % 40) + 1
        rel_idx = ((i - 1) % 20) + 1
        persona_idx = ((i - 1) % 35) + 1

        brule_ref = f"BRULE-{((i - 1) % 50) + 1:03d}"
        cr_ref = f"CR-{((i - 1) % 50) + 1:03d}"
        or_ref = f"OR-{((i - 1) % 50) + 1:03d}"
        secr_ref = f"SECR-{((i - 1) % 50) + 1:03d}"
        priv_ref = f"PRIV-{((i - 1) % 50) + 1:03d}"
        perf_ref = f"PERF-{((i - 1) % 40) + 1:03d}"
        avail_ref = f"AVAIL-{((i - 1) % 40) + 1:03d}"
        loc_ref = f"LOC-{((i - 1) % 40) + 1:03d}"
        a11y_ref = f"A11Y-{((i - 1) % 40) + 1:03d}"
        off_ref = f"OFF-{((i - 1) % 50) + 1:03d}"
        int_ref = f"INT-{((i - 1) % 50) + 1:03d}"

        lines.append("    {")
        lines.append(f'        "id": "{req_id}",')
        lines.append(f'        "title": "{title}",')
        lines.append(f'        "statement": "{statement}",')
        lines.append(f'        "domain": "{domain}",')
        lines.append(f'        "type": "Functional Requirement",')
        lines.append(f'        "priority": "{priority}",')
        lines.append(f'        "priority_rationale": "Essential functional capability for urban primary clinic workflows.",')
        lines.append(f'        "business_value": "{b_val}",')
        lines.append(f'        "rationale": "Standardizes primary care workflows and eliminates paper-based operational bottlenecks.",')
        lines.append(f'        "actor": "{actor}",')
        lines.append(f'        "persona": "PERSONA-{persona_idx:03d}",')
        lines.append(f'        "role": "{role}",')
        lines.append(f'        "stakeholder": "{stakeholder}",')
        lines.append(f'        "trigger": "{trigger}",')
        lines.append(f'        "preconditions": "{precond}",')
        lines.append(f'        "inputs": "{inputs}",')
        lines.append(f'        "validation": "{validation}",')
        lines.append(f'        "main_flow": [')
        lines.append(f'            "Authorized actor invokes {title.lower()} on clinic terminal.",')
        lines.append(f'            "System validates inputs against strict TypeBox schemas and business rule constraints.",')
        lines.append(f'            "Mutation written locally to Dexie.js store with monotonic UUIDv7 key in <10ms.",')
        lines.append(f'            "State change appended to sync mutation queue and transmitted to central Fastify API.",')
        lines.append(f'            "Central database commits transaction and emits structured WORM audit log event."')
        lines.append(f'        ],')
        lines.append(f'        "alternate_flow": "If terminal is offline, transaction commits autonomously to IndexedDB and queues for background replay.",')
        lines.append(f'        "exception_flow": "If validation fails, system highlights offending fields in Kannada/English and aborts state mutation.",')
        lines.append(f'        "postconditions": "{postcond}",')
        lines.append(f'        "state_changes": "Mutates local IndexedDB and central PostgreSQL table `{db_table}`.",')
        lines.append(f'        "business_rules": "{brule_ref}",')
        lines.append(f'        "clinical_rules": "{cr_ref}",')
        lines.append(f'        "operational_rules": "{or_ref}",')
        lines.append(f'        "security_implications": "{secr_ref}: Requires verified JWT session with {role} privileges.",')
        lines.append(f'        "privacy_implications": "{priv_ref}: PII encrypted at rest; consent verified per DPDP Act 2023.",')
        lines.append(f'        "data_implications": "Persisted in PostgreSQL table `{db_table}` and replicated to DuckDB.",')
        lines.append(f'        "audit_requirements": "Emits audit record with actor, timestamp, clinic_id, and transaction payload hash.",')
        lines.append(f'        "offline_behavior": "{off_ref}: Fully supported in local Dexie store `{dexie_store}` without WAN connection.",')
        lines.append(f'        "synchronization_implications": "Monotonic replay via mutation queue with idempotency key headers.",')
        lines.append(f'        "integration_implications": "{int_ref}: Integrates with peripheral hardware or state health APIs.",')
        lines.append(f'        "performance_expectations": "{perf_ref}: Sub-second response time; API p95 <120ms.",')
        lines.append(f'        "availability_expectations": "{avail_ref}: 99.5% service uptime with 8 hours offline resilience.",')
        lines.append(f'        "localization_expectations": "{loc_ref}: 100% localized in Kannada and English.",')
        lines.append(f'        "accessibility_expectations": "{a11y_ref}: WCAG 2.1 AA compliant keyboard navigation and hit targets.",')
        lines.append(f'        "failure_behavior": "Workstation displays local error banner and preserves uncommitted input.",')
        lines.append(f'        "recovery_behavior": "Automated background sync replay upon network connectivity restoration.",')
        lines.append(f'        "observability_requirements": "OpenTelemetry span `namma.clinic.fr.{req_id.lower()}`.",')
        lines.append(f'        "logging_requirements": "JSON log with request_id, clinic_id, and actor_id.",')
        lines.append(f'        "metrics": "Prometheus counter `namma_clinic_fr_executions_total{{req_id=\\"{req_id}\\"}}`.",')
        lines.append(f'        "api_endpoint": "{api_endpoint}",')
        lines.append(f'        "db_table": "{db_table}",')
        lines.append(f'        "dexie_store": "{dexie_store}",')
        lines.append(f'        "acceptance_criteria": [')
        lines.append(f'            "System enforces {title.lower()} across online and offline operating modes.",')
        lines.append(f'            "Rejects unauthorized roles with HTTP 403 Forbidden.",')
        lines.append(f'            "Validates all mandatory input fields and displays localized error messages.",')
        lines.append(f'            "Generates immutable audit event logged to Loki with zero missing fields."')
        lines.append(f'        ],')
        lines.append(f'        "verification_method": "Automated Vitest Integration & Playwright E2E Test",')
        lines.append(f'        "test_type": "Integration & E2E Test",')
        lines.append(f'        "test_id": "PLANNED-TEST-{100 + i:03d}",')
        lines.append(f'        "objective_ref": "OBJECTIVE-{obj_idx:03d}",')
        lines.append(f'        "scope_ref": "INSCOPE-{insc_idx:03d}",')
        lines.append(f'        "stakeholder_ref": "{stakeholder}",')
        lines.append(f'        "persona_ref": "PERSONA-{persona_idx:03d}",')
        lines.append(f'        "risk_ref": "RISK-{risk_idx:03d}",')
        lines.append(f'        "dependency_ref": "DEPENDENCY-{dep_idx:03d}",')
        lines.append(f'        "milestone_ref": "MILESTONE-{m_idx:03d}",')
        lines.append(f'        "release_ref": "RELEASE-{rel_idx:03d}",')
        lines.append(f'        "planned_epic": "PLANNED-EPIC-{((i - 1) % 30) + 1:03d}",')
        lines.append(f'        "planned_feature": "PLANNED-FEATURE-{((i - 1) % 60) + 1:03d}",')
        lines.append(f'        "planned_api": "PLANNED-API-{((i - 1) % 50) + 1:03d}",')
        lines.append(f'        "planned_db": "PLANNED-DB-{((i - 1) % 40) + 1:03d}",')
        lines.append(f'        "planned_ui": "PLANNED-UI-{((i - 1) % 40) + 1:03d}",')
        lines.append(f'        "planned_test": "PLANNED-TEST-{100 + i:03d}",')
        lines.append(f'        "related_requirements": ["{brule_ref}", "{cr_ref}", "{or_ref}", "{secr_ref}", "{off_ref}"],')
        lines.append(f'        "conflicts": "None identified; compliant with primary health operating standards.",')
        lines.append(f'        "dependencies": ["{brule_ref}", "{secr_ref}", "{off_ref}"],')
        lines.append(f'        "open_questions": "Verify hardware driver-free thermal printing performance across all tested USB hubs.",')
        lines.append(f'        "assumptions": "Clinic workstations equipped with modern Chromium-based browser supporting Web Serial and IndexedDB.",')
        lines.append(f'        "constraints": "Workstation memory footprint must remain under 150MB during full-day operation."')
        lines.append("    },")

    lines.append("]")
    lines.append("")

    with open(target_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated {target_path} with {len(FR_DEFINITIONS)} functional requirements.")

if __name__ == "__main__":
    generate_data_fr()
