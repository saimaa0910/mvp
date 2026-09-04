#!/usr/bin/env python3
"""
build_group3.py
Generates data_wf11_to_15.py covering:
  WF-011: Doctor Clinical Consultation, SOAP Documentation & CDSS Advisory Workflow
  WF-012: Electronic Prescription, Drug Interaction & Safety Verification Workflow
  WF-013: Pharmacy Dispensing, FEFO Inventory Allocation & Patient Counseling Workflow
  WF-014: Pharmacy Stock Replenishment, Indenting & Cold-Chain Inventory Control Workflow
  WF-015: Point-of-Care Laboratory Testing, Barcoding & Panic Value Alert Workflow
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_factory import build_workflow_object
from workflow_metadata import WORKFLOW_MAP

def get_group3_specs():
    specs = {}

    # =========================================================================
    # WF-011: Doctor Consultation Workflow
    # =========================================================================
    m11 = WORKFLOW_MAP["WF-011"]
    specs["WF-011"] = {
        "id": "WF-011", "num": "11", "name": m11["name"], "domain": m11["domain"],
        "exec_summary": {
            "purpose": "Governs the primary outpatient medical encounter between the citizen and the Medical Officer in Namma Clinic. Implements structured SOAP (Subjective, Objective, Assessment, Plan) documentation, ICD-10 diagnostic coding, SNOMED CT clinical terms, evidence-based Clinical Decision Support System (CDSS) alerts, diagnostic lab ordering, and digital encounter sign-off.",
            "rationale": "High outpatient volume (60-90 patients per doctor per shift) creates risk of clinical cognitive overload, missed red flags, diagnostic coding omissions, and hurried consultations. A streamlined, high-speed clinical EMR ensures comprehensive clinical documentation within 5-7 minutes per patient while preserving complete clinician autonomy.",
            "clinical_impact": "Ensures standardized medical recording across the BBMP urban clinic network; provides instant access to longitudinal visit histories and vital trends; prevents conflicting diagnostic formulations and therapeutic oversights.",
            "system_impact": "Acts as the central clinical state mutation engine; composes FHIR R4 ClinicalEncounter, Condition, and Observation resources; dispatches downstream orders to Laboratory and Pharmacy stations via internal pub/sub queues.",
            "risk_profile": "Clinician alert fatigue from aggressive CDSS popups; unrecorded verbal advice; delayed laboratory result availability; and session timeout during complex case documentation."
        },
        "objectives": [
            {"id": "OBJ-WF11-01", "title": "Rapid Encounter Documentation", "desc": "Complete comprehensive SOAP documentation, ICD-10 coding, and orders in < 4.0 minutes for routine consultations.", "metric": "Documentation Duration p50 < 240s", "verification": "Encounter active timer telemetry logs"},
            {"id": "OBJ-WF11-02", "title": "Longitudinal History Instant Recall", "desc": "Load past 12-month clinical timeline, vitals trends, and chronic medication history in < 1.0 second.", "metric": "Timeline Fetch Latency p95 < 1000ms", "verification": "Client database query span duration benchmark"},
            {"id": "OBJ-WF11-03", "title": "Standardized Diagnostic Coding", "desc": "Achieve >= 95% primary diagnosis capture linked to standard ICD-10 / SNOMED CT terminology.", "metric": "Standard Coded Diagnosis Rate >= 95%", "verification": "Encounter diagnostic coding audit"},
            {"id": "OBJ-WF11-04", "title": "Advisory CDSS Non-Intrusiveness", "desc": "Present clinical guidelines and drug contraindication warnings with zero modal dialog interruptions.", "metric": "Passive Advisory Presentation = 100%", "verification": "UI component telemetry asserting non-modal CDSS rendering"}
        ],
        "in_scope": [
            {"area": "SOAP Clinical Capture", "desc": "Chief complaints, history of presenting illness, physical examination findings, differential diagnosis, and clinical care plan."},
            {"area": "Terminology Binding", "desc": "Search and auto-completion across WHO ICD-10 primary care subset and National SNOMED CT edition."},
            {"area": "Clinical Decision Support", "desc": "Standard Treatment Guidelines (STG) recommendations for Hypertension, Diabetes, ARI, and Acute Diarrheal Disease."},
            {"area": "Integrated Order Entry", "desc": "Direct electronic generation of lab test requests and prescription orders within the consultation screen."}
        ],
        "out_of_scope": [
            {"area": "Inpatient Ward Rounds", "desc": "Continuous inpatient clinical progress notes; out of scope for primary day clinic.", "handoff": "Referral District Hospital inpatient EMR"},
            {"area": "Specialist Tele-Radiology Review", "desc": "Formal radiological reporting for CT/MRI; clinic restricted to X-ray teleradiology referral.", "handoff": "Tertiary Tele-ICU / Tele-Radiology Hub"}
        ],
        "actors": [
            {"id": "ACT-WF11-01", "type": "Human", "name": "Medical Officer (Doctor)", "responsibilities": "Conducts patient interview, performs clinical exam, reviews vitals, documents SOAP notes, signs encounter.", "permissions": "Encounter Create/Sign, Diagnosis Add, Order Authorize, Referral Mint", "failure_duty": "Manually documents clinical notes on paper encounter sheet if workstation fails.", "inputs": "Patient history, physical exam, triage vitals, lab results", "decisions": "Determines clinical diagnosis, drug regimen, diagnostic tests, and referral need.", "outputs": "Signed clinical encounter, e-prescription, lab orders", "recovery": "Signs draft encounter from temporary local autosave store."},
            {"id": "ACT-WF11-02", "type": "Human", "name": "Citizen / Patient", "responsibilities": "Describes symptoms, health history, responds to physician queries, discusses treatment plan.", "permissions": "Health History Disclosure, Care Plan Agreement", "failure_duty": "Requests Kannada explanation if medical terms are not understood.", "inputs": "Doctor queries, advice", "decisions": "Agrees to prescribed therapy and lifestyle modifications.", "outputs": "Informed agreement, receipt of treatment plan", "recovery": "Asks follow-up questions to clarify medication instructions."}
        ],
        "personas": [
            {"id": "PERSONA-002", "name": "Dr. Manjunath Swamy", "role": "Senior Medical Officer", "env": "High-speed OPD chamber seeing 80 patients per day.", "goals": "Document diagnoses and orders with minimal clicks; review past diabetes control in seconds.", "pain_points": "Tedious text entry, excessive drop-down menus, and sluggish cloud loading.", "adaptations": "Keyboard accelerators (Ctrl+Enter to Sign, F3 for Rx, F4 for Lab) and customizable chief complaint templates."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-002", "title": "Medical Officer", "read": "Complete Patient History, Vitals, Labs", "create": "Encounter, Diagnosis, Orders", "update": "Current Draft Encounter", "delete": "None", "override": "Clinical CDSS Override", "signoff": "Encounter Digital Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF11-01", "desc": "Citizen has completed triage vitals assessment (WF-009) or emergency preemption active.", "check": "patient_encounter.triage_status == 'COMPLETED'", "on_fail": "Direct patient back to triage station."},
            {"id": "PRE-WF11-02", "desc": "Doctor actively authenticated with valid cryptographic session (WF-002).", "check": "session.role == 'ROLE-002' && session.is_valid == TRUE", "on_fail": "Prompt doctor to authenticate."}
        ],
        "triggers": [
            {"id": "TRIG-WF11-01", "class": "Queue Trigger", "event": "Doctor clicks 'Start Consultation' on called patient token", "source": "Doctor Chamber UI", "payload": "{ token_id: 'SNR-001', room_id: 'ROOM-01' }", "latency": "< 200ms to open consultation workspace"}
        ],
        "inputs": [
            {"name": "chief_complaint", "type": "String(255)", "req": "Mandatory", "source": "Doctor Entry", "val": "Text complaint with duration (e.g., 'Fever x 3 days')", "priv": "Clinical", "enc": "Plaintext internal", "ex": "Headache and dizziness x 4 days", "on_err": "Prompt for primary complaint"},
            {"name": "icd10_code", "type": "String(10)", "req": "Mandatory", "source": "ICD-10 Search", "val": "Standard ICD-10 code regex ^[A-Z][0-9]{2}(\\.[0-9]{1,2})?$", "priv": "Clinical", "enc": "Plaintext", "ex": "I10", "on_err": "Require diagnosis selection before sign-off"},
            {"name": "soap_plan", "type": "Text", "req": "Mandatory", "source": "Doctor Entry", "val": "Management plan text", "priv": "Clinical", "enc": "Plaintext", "ex": "Start Amlodipine, repeat BP in 14 days, low salt diet", "on_err": "Flag empty plan"}
        ],
        "outputs": {
            "success": [
                {"name": "Signed Clinical Encounter", "desc": "Cryptographically signed FHIR ClinicalEncounter bundle with SOAP notes and diagnosis.", "format": "FHIR R4 Bundle JSON", "recipient": "Patient Longitudinal Record & EMR Store"},
                {"name": "Downstream Order Triggers", "desc": "Automated dispatch of pending prescription to Pharmacy and lab orders to Laboratory.", "format": "Internal WebSocket Event", "recipient": "Pharmacy & Lab Workstations"}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor P as Patient
    actor D as Medical Officer
    participant UI as Doctor Chamber UI
    participant CDSS as CDSS Engine
    participant DB as Local SQLite DB
    participant WS as WebSocket Hub
    P->>D: 1. Patient seated in chamber
    D->>UI: 2. Click 'Start Encounter'
    UI->>DB: 3. Fetch Vitals (BP 154/96, Pulse 82) & History
    UI-->>D: 4. Display Vitals Card & Historical Timeline
    D->>UI: 5. Enter Symptoms & Select Diagnosis: I10 (Essential Hypertension)
    UI->>CDSS: 6. Query Treatment Guidelines for I10 + Age 68
    CDSS-->>UI: 7. Suggest STG 1st Line: CCB (Amlodipine 5mg)
    D->>UI: 8. Authorize Rx & Click 'Sign Encounter' (Ctrl+Enter)
    UI->>DB: 9. Commit Signed Encounter & Generate FHIR Bundle
    UI->>WS: 10. Route Patient to Pharmacy Queue""",
        "activity_diagram": """flowchart TD
    Start([Patient Enters Consultation Chamber]) --> OpenChart[Doctor Opens Active Encounter Chart]
    OpenChart --> ReviewVitals[Review Triage Vitals & Historical Timeline]
    ReviewVitals --> InterviewPatient[Conduct Clinical Interview: Subjective Symptoms]
    InterviewPatient --> PhysicalExam[Perform Physical Examination: Objective Signs]
    PhysicalExam --> SelectDiagnosis[Search & Select ICD-10 Primary Diagnosis]
    SelectDiagnosis --> RunCDSS[CDSS Evaluates Diagnosis against Age, Sex, Allergies]
    RunCDSS --> CheckAlerts{CDSS Critical Alert Generated?}
    CheckAlerts -- Yes --> DisplayAdvisory[Display Subtle Clinical Advisory Card with Guideline Reference]
    CheckAlerts -- No --> PrescribeOrders[Author e-Prescription & Laboratory Orders]
    DisplayAdvisory --> PrescribeOrders
    PrescribeOrders --> CounselPatient[Provide Bilingual Vernacular Counseling]
    CounselPatient --> SignEncounter[Doctor Enters PIN / Clicks Sign Encounter]
    SignEncounter --> CommitRecord[Commit Cryptographic Encounter to SQLite]
    CommitRecord --> DispatchOrders[Dispatch Orders to Pharmacy & Lab Queues]
    DispatchOrders --> End([Consultation Concluded & Patient Directed to Pharmacy])""",
        "state_diagram": """stateDiagram-v2
    [*] --> WAITING_FOR_DOCTOR
    WAITING_FOR_DOCTOR --> CONSULTATION_ACTIVE: Doctor Clicks 'Start Encounter'
    CONSULTATION_ACTIVE --> DIAGNOSIS_SELECTED: ICD-10 Code Assigned
    DIAGNOSIS_SELECTED --> ORDERS_ATTACHED: Prescription / Lab Tests Added
    ORDERS_ATTACHED --> SIGNED_OFF: Doctor Cryptographically Signs Encounter
    CONSULTATION_ACTIVE --> ENCOUNTER_HELD: Doctor Places Encounter on Hold
    ENCOUNTER_HELD --> CONSULTATION_ACTIVE: Doctor Resumes Encounter
    SIGNED_OFF --> [*]"""
    }

    # =========================================================================
    # WF-012: Prescription Workflow
    # =========================================================================
    m12 = WORKFLOW_MAP["WF-012"]
    specs["WF-012"] = {
        "id": "WF-012", "num": "12", "name": m12["name"], "domain": m12["domain"],
        "exec_summary": {
            "purpose": "Drives the digital authoring, real-time clinical safety verification, drug-drug interaction screening, allergy cross-checking, Karnataka Essential Medicines List (EML) formulary validation, bilingual dosage instruction rendering, and cryptographic signing of electronic prescriptions in Namma Clinic.",
            "rationale": "Illegible handwriting, dosage miscalculations, adverse drug-drug interactions, and prescribing of non-formulary expensive branded drugs are primary causes of outpatient adverse drug events. An intelligent digital prescription engine ensures 100% generic prescribing from the approved state formulary with instant safety verification.",
            "clinical_impact": "Completely eliminates prescribing errors stemming from illegible handwriting; blocks lethal drug combinations (e.g., ACE inhibitors + ARBs, dual NSAIDs); ensures pediatric weight-based dosage accuracy; and renders clear Kannada instructions on packaging.",
            "system_impact": "Directly feeds the pharmacy dispensing queue; reserves batch inventory in the edge database; composes FHIR R4 MedicationRequest resources; and synchronizes with the BBMP central drug repository.",
            "risk_profile": "Over-riding critical drug interaction warnings; selecting wrong drug concentration; unrecorded patient allergy history; and network delay in transmitting prescription to pharmacy counter."
        },
        "objectives": [
            {"id": "OBJ-WF12-01", "title": "100% Generic EML Compliance", "desc": "Enforce authoring of all prescriptions exclusively using generic INN names from the Karnataka EML formulary.", "metric": "Generic Prescribing Rate = 100%", "verification": "Prescription formulary audit report"},
            {"id": "OBJ-WF12-02", "title": "Sub-100ms Drug Safety Screening", "desc": "Execute comprehensive drug-drug, drug-allergy, and duplicate therapy checks in under 100 milliseconds.", "metric": "Interaction Check Latency < 100ms", "verification": "Safety engine transaction benchmark"},
            {"id": "OBJ-WF12-03", "title": "Bilingual Kannada Instructions", "desc": "Generate precise bilingual dosage, frequency, route, and meal timing instructions for 100% of prescribed items.", "metric": "Bilingual Instruction Coverage = 100%", "verification": "Prescription rendering assertion tests"},
            {"id": "OBJ-WF12-04", "title": "Zero Lethal Drug Contraindications", "desc": "Intercept and require explicit clinical rationale for any Tier-1 severe drug interaction before sign-off.", "metric": "Unacknowledged Tier-1 Alerts = 0", "verification": "Prescription override ledger inspection"}
        ],
        "in_scope": [
            {"area": "Generic EML Formulary", "desc": "Selection from 180+ essential drugs categorized by therapeutic class with real-time stock indicators."},
            {"area": "Dosing & Frequency Configuration", "desc": "Standard frequency codes (OD, BD, TID, QID, SOS), duration in days, and meal relationship (Before/After Food)."},
            {"area": "Drug-Drug Interaction Matrix", "desc": "Local in-memory interaction graph categorizing warnings into Minor, Moderate, and Severe Contraindications."},
            {"area": "Allergy Cross-Checking", "desc": "Cross-referencing drug class with patient recorded drug allergies (e.g., Penicillin, Sulfa, NSAIDs)."}
        ],
        "out_of_scope": [
            {"area": "Chemotherapy & Biological Regimens", "desc": "Specialized oncology chemotherapeutic dosing; out of scope for primary care.", "handoff": "Tertiary Cancer Institute"},
            {"area": "Schedule X Controlled Narcotics", "desc": "Injectable narcotics requiring triplicate physical government registers; referred to District Hospital.", "handoff": "District Civil Hospital"}
        ],
        "actors": [
            {"id": "ACT-WF12-01", "type": "Human", "name": "Medical Officer", "responsibilities": "Selects generic medications, configures dosage and duration, reviews interaction warnings, signs e-prescription.", "permissions": "Prescription Author, Interaction Override, Digital Signature", "failure_duty": "Issues handwritten carbon-copy paper prescription if workstation is blocked.", "inputs": "Diagnosis, patient weight, recorded allergies, current formulary stock", "decisions": "Determines drug selection, dosing frequency, and evaluates CDSS interaction alerts.", "outputs": "Cryptographically signed e-prescription", "recovery": "Modifies drug order if pharmacist raises stock or allergy query."},
            {"id": "ACT-WF12-02", "type": "Human", "name": "Pharmacist", "responsibilities": "Reviews signed digital prescription, verifies safety notes, executes dispensing.", "permissions": "Prescription Read, Dispense Confirm, Pharmacist Query", "failure_duty": "Contacts doctor immediately if suspected contraindication was overridden inappropriately.", "inputs": "Digital prescription, physical stock", "decisions": "Validates prescription authenticity and batch allocation.", "outputs": "Dispensed medicine package with Kannada label", "recovery": "Requests doctor amendment for out-of-stock items."}
        ],
        "personas": [
            {"id": "PERSONA-002", "name": "Dr. Manjunath Swamy", "role": "Senior Medical Officer", "env": "High-pressure consultation room.", "goals": "Prescribe standard chronic medications (e.g., Metformin + Glimepiride + Amlodipine) in 3 clicks.", "pain_points": "Typing dosage instructions repeatedly for common regimens.", "adaptations": "One-click 'Favorite Regimens' and automated default frequency/duration settings."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-002", "title": "Medical Officer", "read": "Formulary, Stock, History", "create": "Prescription Order", "update": "Draft Rx", "delete": "Cancel Draft", "override": "Drug Interaction Override", "signoff": "Cryptographic Rx Signoff"},
            {"role": "ROLE-003", "title": "Pharmacist", "read": "Signed Prescriptions", "create": "Dispense Verification", "update": "Dispense Status", "delete": "None", "override": "None", "signoff": "Dispense Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF12-01", "desc": "Active clinical encounter with primary diagnosis selected (WF-011).", "check": "encounter.status == 'IN_PROGRESS' && encounter.diagnosis_id != NULL", "on_fail": "Require diagnosis selection before prescribing."},
            {"id": "PRE-WF12-02", "desc": "Local formulary database loaded and stock counts synchronized.", "check": "formulary.count > 0", "on_fail": "Display offline stock warning badge."}
        ],
        "triggers": [
            {"id": "TRIG-WF12-01", "class": "Doctor Action", "event": "Doctor clicks 'Add Medication' in consultation chart", "source": "Prescription Workspace UI", "payload": "{ encounter_id: 'ENC-001' }", "latency": "< 50ms to open search"}
        ],
        "inputs": [
            {"name": "drug_id", "type": "String(16)", "req": "Mandatory", "source": "Formulary Catalog", "val": "Valid EML generic drug identifier", "priv": "Clinical", "enc": "Plaintext", "ex": "DRG-AMLO-05", "on_err": "Reject unknown drug"},
            {"name": "dosage_freq", "type": "Enum(OD, BD, TID, QID, SOS)", "req": "Mandatory", "source": "Doctor Selection", "val": "Defined frequency code", "priv": "Clinical", "enc": "Plaintext", "ex": "OD", "on_err": "Default to OD"},
            {"name": "duration_days", "type": "Integer", "req": "Mandatory", "source": "Doctor Entry", "val": "Range: 1 to 90 days", "priv": "Clinical", "enc": "Plaintext", "ex": "30", "on_err": "Flag duration > 90 days"},
            {"name": "food_relation", "type": "Enum(BEFORE_FOOD, AFTER_FOOD, WITH_FOOD)", "req": "Mandatory", "source": "Doctor Selection", "val": "Food relation enum", "priv": "Clinical", "enc": "Plaintext", "ex": "AFTER_FOOD", "on_err": "Default to AFTER_FOOD"}
        ],
        "outputs": {
            "success": [
                {"name": "Signed Digital Prescription", "desc": "FHIR MedicationRequest bundle with cryptographic doctor signature and bilingual metadata.", "format": "FHIR R4 JSON-LD", "recipient": "Pharmacy Counter Queue & Patient EMR"}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor D as Medical Officer
    participant UI as Rx Interface
    participant DDI as Interaction Engine
    participant DB as SQLite DB
    participant PHARM as Pharmacy Workstation
    D->>UI: 1. Search 'Amlodipine' -> Select 5mg Tablet
    D->>UI: 2. Set Dose: 1 Tab, OD (Morning), After Food, 30 Days
    UI->>DDI: 3. Cross-check with Patient Active Rx & Allergies
    DDI-->>UI: 4. Safety Checks Passed (0 Severe Interactions)
    D->>UI: 5. Click 'Sign & Authorize Prescription'
    UI->>DB: 6. Insert Prescription Record & Reserve 30 Tablets
    UI->>PHARM: 7. Push Prescription to Pharmacy Counter Queue""",
        "activity_diagram": """flowchart TD
    Start([Doctor Opens Prescription Screen]) --> SearchDrug[Search Generic Drug Name in EML]
    SearchDrug --> SelectItem[Select Drug, Strength, and Dosage Form]
    SelectItem --> CheckStock{Item in Stock at Clinic?}
    CheckStock -- No / Low Stock --> ShowStockWarning[Display Amber Warning: Low Inventory]
    CheckStock -- Yes --> SetDose[Configure Frequency, Duration, Food Relation]
    ShowStockWarning --> SetDose
    SetDose --> RunSafetyChecks[Safety Engine Evaluates Drug-Drug & Allergy Matrix]
    RunSafetyChecks --> InteractionFound{Severe Contraindication Detected?}
    InteractionFound -- Yes --> ShowSevereModal[Display Red Alert: Lethal Drug Interaction]
    ShowSevereModal --> DocAction{Doctor Decision}
    DocAction -- Abort Order --> SearchDrug
    DocAction -- Override with Rationale --> EnterRationale[Enter Clinical Justification for Override]
    InteractionFound -- No --> ReadySign[Prescription Ready for Authorization]
    EnterRationale --> ReadySign
    ReadySign --> SignRx[Doctor Cryptographically Signs e-Prescription]
    SignRx --> TransmitPharm[Push e-Prescription to Pharmacy Dispensing Station]
    TransmitPharm --> End([Prescription Complete & Queued for Dispensing])""",
        "state_diagram": """stateDiagram-v2
    [*] --> DRAFT_RX
    DRAFT_RX --> SAFETY_CHECKED: Drug Added & DDI Validated
    SAFETY_CHECKED --> INTERACTION_FLAGGED: Interaction Detected
    INTERACTION_FLAGGED --> DRAFT_RX: Clinician Cancels Item
    INTERACTION_FLAGGED --> OVERRIDDEN: Clinician Submits Rationale
    SAFETY_CHECKED --> SIGNED: Doctor Signs Order
    OVERRIDDEN --> SIGNED: Doctor Signs Order
    SIGNED --> QUEUED_IN_PHARMACY: Pushed to Pharmacy Station
    QUEUED_IN_PHARMACY --> [*]"""
    }

    # =========================================================================
    # WF-013: Pharmacy Dispensing Workflow
    # =========================================================================
    m13 = WORKFLOW_MAP["WF-013"]
    specs["WF-013"] = {
        "id": "WF-013", "num": "13", "name": m13["name"], "domain": m13["domain"],
        "exec_summary": {
            "purpose": "Governs pharmacy counter operations in Namma Clinic: electronic prescription receipt, First-Expiry First-Out (FEFO) batch inventory allocation, barcode verification of physical medicine packages, partial dispensing during stock constraints, bilingual verbal counseling in Kannada, thermal dosage label printing, and atomic inventory decrement.",
            "rationale": "Medication errors at the dispensing stage—such as handing out expired batches, wrong strength tablets, or inadequate verbal instruction to elderly citizens—directly cause therapeutic failure and poisonings. A closed-loop barcode-assisted dispensing process guarantees that the right patient receives the right drug, in the right dose, with complete vernacular understanding.",
            "clinical_impact": "Prevents dispensing of expired or recalled pharmaceuticals; ensures 100% adherence counseling in Kannada; and provides documented confirmation of every tablet handed to citizens.",
            "system_impact": "Executes atomic inventory decrements against SQLite batch tables; resolves concurrency races across multi-counter dispensaries; and emits FHIR R4 MedicationDispense events.",
            "risk_profile": "Barcode scanner hardware failure; stock discrepancy between physical shelf and database; crowded patient queue causing rushed counseling; and patient leaving without taking full course."
        },
        "objectives": [
            {"id": "OBJ-WF13-01", "title": "Closed-Loop Barcode Verification", "desc": "Verify 100% of dispensed medication strips via 2D/1D barcode scanner before counter handoff.", "metric": "Barcode Verification Rate = 100%", "verification": "Dispensing scanner telemetry logs"},
            {"id": "OBJ-WF13-02", "title": "Strict FEFO Batch Allocation", "desc": "Automatically allocate medicine batches with the earliest expiration date, preventing expired shelf waste.", "metric": "FEFO Adherence Rate = 100%", "verification": "Inventory batch allocation audit"},
            {"id": "OBJ-WF13-03", "title": "Bilingual Counseling Completion", "desc": "Complete structured Kannada/English dosage and meal counseling for 100% of attending citizens.", "metric": "Counseling Confirmation Rate = 100%", "verification": "Pharmacist dispensing sign-off checklist"},
            {"id": "OBJ-WF13-04", "title": "Atomic Inventory Reconciliation", "desc": "Update local inventory balances with strict ACID transaction boundaries in < 50 milliseconds.", "metric": "Inventory Decrement Latency < 50ms", "verification": "Database transaction commit duration benchmarks"}
        ],
        "in_scope": [
            {"area": "Electronic Prescription Ingestion", "desc": "Automated retrieval of signed e-prescriptions from doctor consultation chamber."},
            {"area": "FEFO Batch Selection", "desc": "System-directed picking of nearest-expiry unexpired stock from active dispensary shelf."},
            {"area": "Barcode Verification Scan", "desc": "Physical scan of medicine box/strip GTIN/GS1 barcode to confirm correct product and batch."},
            {"area": "Bilingual Label Generation", "desc": "Thermal printing of Kannada packaging labels showing dosage iconography (Sun/Moon for Morning/Night)."},
            {"area": "Stock Adjustment", "desc": "Immediate atomic decrement of physical inventory count upon dispense confirmation."}
        ],
        "out_of_scope": [
            {"area": "Compounding Pharmacy Operations", "desc": "Manual compounding of sterile solutions or extemporaneous ointments; clinic uses factory pre-packaged drugs.", "handoff": "District Hospital Pharmacy"},
            {"area": "Commercial Sales & Cash Billing", "desc": "All medicines in Namma Clinics are provided 100% free of charge by the Government of Karnataka.", "handoff": "None - Free Public Healthcare"}
        ],
        "actors": [
            {"id": "ACT-WF13-01", "type": "Human", "name": "Pharmacist", "responsibilities": "Calls prescription, retrieves physical stock, scans barcode, prints label, counsels patient, confirms dispense.", "permissions": "Dispense Execute, Batch Select, Partial Dispense, Inventory Decrement", "failure_duty": "Manually records dispensed quantities in physical register if scanner fails.", "inputs": "Digital prescription, physical stock boxes, citizen questions", "decisions": "Determines batch selection; confirms patient comprehension of dosage.", "outputs": "Dispensed medicine package, counseling confirmation", "recovery": "Re-reads prescription with doctor if quantity or strength is ambiguous."},
            {"id": "ACT-WF13-02", "type": "Human", "name": "Citizen / Patient", "responsibilities": "Presents token slip, listens to counseling, verifies medicine packet, confirms understanding.", "permissions": "Receive Medication, Ask Questions", "failure_duty": "Requests repeat of dosage instructions if unclear.", "inputs": "Physical packets, verbal Kannada counseling", "decisions": "Confirms understanding of how to take medicine with food.", "outputs": "Leaves facility with medication and dosage instructions", "recovery": "Returns to counter if instructions forgotten."}
        ],
        "personas": [
            {"id": "PERSONA-003", "name": "Nagaraj Patil", "role": "Clinic Pharmacist", "env": "Busy pharmacy dispensing window facing morning crowd.", "goals": "Dispense 70+ prescriptions per morning without picking errors.", "pain_points": "Scanning delays; having to search for obscure batch numbers manually.", "adaptations": "Auto-suggested top FEFO batch with visual shelf location coordinate (e.g., 'Shelf B, Row 3')."},
            {"id": "PERSONA-007", "name": "Shantamma", "role": "Elderly Patient", "env": "Standing at counter with multiple medicine strips.", "goals": "Know clearly which pill to take in the morning and which at night.", "pain_points": "Cannot read small English text on blister packs.", "adaptations": "Color-coded sticker labels with Morning Sun and Night Moon icons."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-003", "title": "Pharmacist", "read": "Prescriptions, Inventory, Batch Data", "create": "Dispense Event, Label Job", "update": "Stock Balance", "delete": "None", "override": "Batch Override (Damaged)", "signoff": "Dispense Complete Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF13-01", "desc": "Cryptographically signed digital prescription available (WF-012).", "check": "prescription.status == 'SIGNED'", "on_fail": "Prescription cannot be dispensed without doctor signature."},
            {"id": "PRE-WF13-02", "desc": "Barcode scanner connected and operational on pharmacy USB/HID port.", "check": "scanner.status == 'READY'", "on_fail": "Allow manual batch entry with mandatory supervisor override reason."}
        ],
        "triggers": [
            {"id": "TRIG-WF13-01", "class": "Queue Trigger", "event": "Pharmacist clicks 'Call Patient' on pharmacy queue screen", "source": "Pharmacy Counter UI", "payload": "{ token_id: 'SNR-001', counter: 'PHARM-01' }", "latency": "< 100ms to load prescription items"}
        ],
        "inputs": [
            {"name": "prescription_id", "type": "UUID", "req": "Mandatory", "source": "Prescription Record", "val": "Valid prescription UUID", "priv": "Clinical", "enc": "Plaintext internal", "ex": "p1q2r3s4-...", "on_err": "Reject dispense"},
            {"name": "scanned_barcode", "type": "String(32)", "req": "Mandatory", "source": "Barcode Scanner", "val": "Scanned GS1/EAN barcode", "priv": "Operational", "enc": "Plaintext", "ex": "8901234567890", "on_err": "Barcode mismatch alert; block dispense"},
            {"name": "batch_id", "type": "String(20)", "req": "Mandatory", "source": "Inventory Shelf", "val": "Active unexpired batch code", "priv": "Operational", "enc": "Plaintext", "ex": "BAT-2026-088", "on_err": "Block expired batch"}
        ],
        "outputs": {
            "success": [
                {"name": "Dispensed Medication Package", "desc": "Physical medicine packs with printed Kannada dosage instruction stickers.", "format": "Physical Blister Pack with Label", "recipient": "Patient / Citizen"},
                {"name": "Dispense Completion Event", "desc": "FHIR MedicationDispense record committed and stock decremented in SQLite.", "format": "JSON-LD Event Frame", "recipient": "Central Inventory Ledger & Patient EMR"}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor C as Citizen
    actor P as Pharmacist
    participant UI as Pharmacy Terminal
    participant DB as SQLite DB
    participant PR as Label Printer
    C->>P: 1. Citizen arrives at Pharmacy Counter
    P->>UI: 2. Call Next Token SNR-001 -> View Prescription
    UI-->>P: 3. Display: Amlodipine 5mg x 30 Tab (FEFO: Batch B88, Shelf A2)
    P->>UI: 4. Scan Physical Pack Barcode
    UI->>UI: 5. Barcode Matches Prescribed Drug
    P->>PR: 6. Print Kannada Dosage Label (Sun Icon - Morning)
    PR-->>P: 7. Dispense Thermal Label Sticker
    P->>C: 8. Handover Medicine & Explain in Vernacular Kannada
    P->>UI: 9. Click 'Confirm Dispensed'
    UI->>DB: 10. Atomic Decrement 30 Tabs from Batch B88""",
        "activity_diagram": """flowchart TD
    Start([Citizen Arrives at Dispensing Window]) --> CallToken[Pharmacist Calls Token on Screen]
    CallToken --> LoadRx[Load Signed e-Prescription & Active Items]
    LoadRx --> SuggestBatch[System Highlights Earliest Expiring FEFO Batch]
    SuggestBatch --> PickMedicine[Pharmacist Retrieves Physical Box from Shelf]
    PickMedicine --> ScanBarcode[Scan GS1 Barcode on Medicine Strip]
    ScanBarcode --> ValidateMatch{Does Scanned Item Match Prescription?}
    ValidateMatch -- No --> BeepError[Audible Error: Item / Batch Mismatch!]
    BeepError --> PickMedicine
    ValidateMatch -- Yes --> CheckExpiry{Batch Expiry Date Valid > 30 Days?}
    CheckExpiry -- No / Expired --> QuarantineBatch[Quarantine Batch & Alert Coordinator]
    QuarantineBatch --> PickMedicine
    CheckExpiry -- Yes --> PrintLabel[Print Kannada Dosage Sticker with Visual Icons]
    PrintLabel --> CounselPatient[Conduct Verbal Kannada Dosage & Meal Counseling]
    CounselPatient --> ConfirmDispense[Click 'Complete Dispensing' on Terminal]
    ConfirmDispense --> DecrementStock[Atomic Decrement of Inventory in Local SQLite]
    DecrementStock --> End([Dispensing Finished & Encounter Closed])""",
        "state_diagram": """stateDiagram-v2
    [*] --> READY_TO_DISPENSE
    READY_TO_DISPENSE --> BATCH_SELECTED: FEFO Batch Picked
    BATCH_SELECTED --> BARCODE_VERIFIED: Barcode Scanned & Matched
    BATCH_SELECTED --> MISMATCH_ERROR: Wrong Drug Scanned
    MISMATCH_ERROR --> BATCH_SELECTED: Rescan Correct Item
    BARCODE_VERIFIED --> COUNSELED: Vernacular Explanation Provided
    COUNSELED --> DISPENSED_AND_CLOSED: Stock Decremented & Handed Over
    DISPENSED_AND_CLOSED --> [*]"""
    }

    # =========================================================================
    # WF-014: Stock Replenishment Workflow
    # =========================================================================
    m14 = WORKFLOW_MAP["WF-014"]
    specs["WF-014"] = {
        "id": "WF-014", "num": "14", "name": m14["name"], "domain": m14["domain"],
        "exec_summary": {
            "purpose": "Controls clinic pharmacy stock levels, automated reorder threshold triggers, electronic indent generation to the BBMP Central Drug Warehouse / KSDL, receipt verification, batch-level cold-chain tracking (2-8 C vaccines and insulins), discrepancy reporting, quarantine of damaged/expired medicines, and monthly inventory reconciliation.",
            "rationale": "Stockouts of critical anti-hypertensives, oral anti-diabetics, or pediatric rehydration salts cause immediate treatment abandonment and citizen distrust in primary healthcare. Automated predictive indenting prevents stock ruptures while eliminating manual paper indent delays.",
            "clinical_impact": "Guarantees unbroken continuity of chronic NCD pharmacotherapy; ensures cold-chain integrity of vaccines and insulins from central depot to patient arm; and prevents administration of degraded pharmaceuticals.",
            "system_impact": "Interfaces with BBMP Central Drug Inventory and state DVDMS (e-Aushadhi) supply chain portals; maintains immutable batch ledger with cryptographic signature receipts.",
            "risk_profile": "Power outages compromising vaccine refrigerator; delayed delivery truck from central warehouse; shipment damage or transit thermal rupture; and inventory discrepancy between physical count and software ledger."
        },
        "objectives": [
            {"id": "OBJ-WF14-01", "title": "Zero Essential Drug Stockouts", "desc": "Maintain 100% availability of Top 40 Core Essential Drugs via predictive buffer threshold indenting.", "metric": "Core Drug Availability = 100%", "verification": "Daily automated inventory status scan"},
            {"id": "OBJ-WF14-02", "title": "Continuous Cold Chain Compliance", "desc": "Monitor and log vaccine/insulin refrigerator temperature (2-8 C) at 15-minute intervals without gaps.", "metric": "Cold Chain Uptime (2-8 C) = 100%", "verification": "IoT digital temperature datalogger audit"},
            {"id": "OBJ-WF14-03", "title": "Automated Indent Generation", "desc": "Generate and dispatch monthly replenishment indent to Central Warehouse within 5 minutes of threshold trigger.", "metric": "Indent Generation Duration < 300s", "verification": "Indent creation timestamp telemetry"},
            {"id": "OBJ-WF14-04", "title": "Discrepancy Reporting & Reconciliation", "desc": "Record and report 100% of shipment delivery variances (damaged, short-shipped, wrong batch) within 24 hours.", "metric": "Variance Reporting Compliance = 100%", "verification": "Goods receipt discrepancy audit logs"}
        ],
        "in_scope": [
            {"area": "Buffer Threshold Calculation", "desc": "Dynamic minimum stock level computation based on average daily consumption and lead time."},
            {"area": "Electronic Indent Authoring", "desc": "Drafting and approval of periodic replenishment indents by Pharmacist and Medical Officer."},
            {"area": "Goods Receipt Verification", "desc": "Physical box count, barcode scan, batch number check, and expiration date recording upon shipment arrival."},
            {"area": "Cold-Chain Temperature Tracking", "desc": "Integration with digital data loggers in ice-lined refrigerators (ILR) for vaccines and insulins."}
        ],
        "out_of_scope": [
            {"area": "Central Government Procurement Tenders", "desc": "State-level pharmaceutical manufacturer bidding and pricing; managed by KSMSCL.", "handoff": "Karnataka State Medical Supplies Corp"},
            {"area": "Hazardous Bio-Medical Waste Destruction", "desc": "Incineration of expired pharmaceuticals; handled by authorized biomedical waste vendor.", "handoff": "BBMP Waste Management Protocol"}
        ],
        "actors": [
            {"id": "ACT-WF14-01", "type": "Human", "name": "Pharmacist", "responsibilities": "Monitors stock, drafts replenishment indent, receives shipments, inspects cold chain, reports variances.", "permissions": "Indent Create, Goods Receipt, Batch Stock In, Discrepancy Log", "failure_duty": "Manually records refrigerator temperature with analog thermometer if digital logger fails.", "inputs": "Current inventory, consumption trends, physical shipments", "decisions": "Determines required reorder quantities; accepts or rejects damaged boxes.", "outputs": "Electronic indents, goods receipt verification records", "recovery": "Re-counts physical stock to resolve software variance."},
            {"id": "ACT-WF14-02", "type": "Human", "name": "Medical Officer", "responsibilities": "Reviews and authorizes replenishment indents; signs monthly stock reconciliation.", "permissions": "Indent Authorize, Stock Write-off Approve", "failure_duty": "Escalates critical stock ruptures directly to BBMP Chief Health Officer.", "inputs": "Draft indent, consumption reports", "decisions": "Approves indent quantities; authorizes disposal of expired batches.", "outputs": "Authorized electronic indent", "recovery": "Authorizes emergency inter-clinic stock borrowing."}
        ],
        "personas": [
            {"id": "PERSONA-003", "name": "Nagaraj Patil", "role": "Clinic Pharmacist", "env": "Pharmacy store room managing 180+ drug lines.", "goals": "Never run out of Metformin or Amlodipine; complete stocktaking in under 1 hour.", "pain_points": "Manual spreadsheet indents prone to formula errors; surprise stockouts.", "adaptations": "1-click 'Auto-Populate Indent' based on 30-day average daily consumption."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-003", "title": "Pharmacist", "read": "Stock, Indents, Receipts", "create": "Draft Indent, GRN Receipt", "update": "Physical Counts", "delete": "None", "override": "None", "signoff": "Pharmacist Stock Check"},
            {"role": "ROLE-002", "title": "Medical Officer", "read": "All Inventory Data", "create": "Emergency Indent", "update": "None", "delete": "None", "override": "Emergency Write-off", "signoff": "Indent Digital Authorization"}
        ],
        "preconditions": [
            {"id": "PRE-WF14-01", "desc": "Clinic edge database operational and inventory ledger accessible.", "check": "inventory_service.status == 'ONLINE'", "on_fail": "Use cached offline stock register."},
            {"id": "PRE-WF14-02", "desc": "Cold-chain storage refrigerator verified operational between 2.0 and 8.0 C.", "check": "refrigerator.temp >= 2.0 && refrigerator.temp <= 8.0", "on_fail": "Trigger urgent cold-chain breach alert."}
        ],
        "triggers": [
            {"id": "TRIG-WF14-01", "class": "Automated Trigger", "event": "Item stock falls below defined minimum reorder buffer threshold", "source": "Inventory Watchdog Daemon", "payload": "{ drug_id: 'DRG-AMLO-05', current_stock: 120, buffer_threshold: 300 }", "latency": "< 1.0s to flag low stock"},
            {"id": "TRIG-WF14-02", "class": "Shipment Arrival", "event": "Central warehouse delivery vehicle arrives with supplies", "source": "Pharmacist Intake", "payload": "{ challan_no: 'CH-2026-991', boxes: 8 }", "latency": "< 5 min to initiate goods receipt"}
        ],
        "inputs": [
            {"name": "indent_items", "type": "Array<Object>", "req": "Mandatory", "source": "Pharmacist / System", "val": "List of drug IDs and requested quantities", "priv": "Operational", "enc": "Plaintext", "ex": "[{ drug_id: 'DRG-AMLO-05', qty: 1000 }]", "on_err": "Flag empty indent"},
            {"name": "delivery_challan", "type": "String(32)", "req": "Mandatory", "source": "Delivery Driver", "val": "Warehouse delivery invoice number", "priv": "Operational", "enc": "Plaintext", "ex": "CH-BLR-2026-4412", "on_err": "Require valid invoice number"}
        ],
        "outputs": {
            "success": [
                {"name": "Authorized Electronic Indent", "desc": "Signed PDF and JSON payload transmitted to BBMP Central Warehouse portal.", "format": "JSON-LD & Signed PDF", "recipient": "BBMP Central Warehouse & DVDMS Portal"},
                {"name": "Goods Receipt Note (GRN)", "desc": "Cryptographic record confirming verified receipt and batch additions.", "format": "Immutable DB Record", "recipient": "Facility Audit Ledger"}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor P as Pharmacist
    participant UI as Stock Console
    actor D as Medical Officer
    participant WH as BBMP Warehouse
    actor DRV as Delivery Driver
    P->>UI: 1. Review Low Stock Alerts (Amlodipine, Metformin)
    P->>UI: 2. Click 'Auto-Generate Monthly Indent'
    UI->>D: 3. Route Indent for MO Approval
    D->>UI: 4. Review & Cryptographically Sign Indent
    UI->>WH: 5. Transmit Electronic Indent to Central Depot
    Note over WH,DRV: 48 Hours Later: Dispatch
    DRV->>P: 6. Deliver 8 Boxes with Challan
    P->>UI: 7. Scan Inbound Batch Barcodes & Confirm Quantities
    UI-->>P: 8. Stock Added to Shelf Inventory & GRN Generated""",
        "activity_diagram": """flowchart TD
    Start([Stock Falls Below Reorder Threshold]) --> TriggerAlert[System Raises Low Stock Alert Badge]
    TriggerAlert --> OpenIndentScreen[Pharmacist Opens Indenting Workspace]
    OpenIndentScreen --> AutoCalculate[System Calculates 30-day Consumption + Buffer]
    AutoCalculate --> ReviewQuantities[Pharmacist Reviews & Adjusts Requested Quantities]
    ReviewQuantities --> SubmitToDoctor[Submit Draft Indent to Medical Officer]
    SubmitToDoctor --> DoctorReview{Doctor Approves Indent?}
    DoctorReview -- No --> ReturnEdit[Return to Pharmacist for Adjustment]
    ReturnEdit --> ReviewQuantities
    DoctorReview -- Yes --> SignIndent[Doctor Signs Indent with Digital Credentials]
    SignIndent --> SendWarehouse[Transmit Indent via API to BBMP Warehouse]
    SendWarehouse --> AwaitShipment[Warehouse Dispatches Supplies to Clinic]
    AwaitShipment --> ShipmentArrives[Delivery Truck Arrives with Physical Stock]
    ShipmentArrives --> InspectBoxes[Inspect Physical Boxes: Check Seals & Temp Indicator]
    InspectBoxes --> CheckColdChain{Cold Chain 2-8C Maintained?}
    CheckColdChain -- No / Ruptured --> RejectShipment[Reject Shipment, Log Cold-Chain Breach]
    CheckColdChain -- Yes --> ScanBoxes[Scan Inbound Batch Barcodes & Log Expiry Dates]
    ScanBoxes --> MatchChallan{Counts Match Delivery Challan?}
    MatchChallan -- Discrepancy Found --> LogDiscrepancy[Record Discrepancy Note in GRN]
    MatchChallan -- Counts Match --> ApproveGRN[Approve Goods Receipt Note GRN]
    LogDiscrepancy --> ApproveGRN
    ApproveGRN --> StockIn[Increment Active Pharmacy Inventory in SQLite]
    StockIn --> End([Replenishment Complete & Stock Available for Dispensing])""",
        "state_diagram": """stateDiagram-v2
    [*] --> THRESHOLD_BREACHED
    THRESHOLD_BREACHED --> INDENT_DRAFTED: Auto-Calculated by System
    INDENT_DRAFTED --> INDENT_AUTHORIZED: Medical Officer Signs
    INDENT_AUTHORIZED --> DISPATCHED_TO_WAREHOUSE: Transmitted to Central Portal
    DISPATCHED_TO_WAREHOUSE --> SHIPMENT_IN_TRANSIT: Warehouse Fulfills Order
    SHIPMENT_IN_TRANSIT --> GOODS_RECEIVED_VERIFYING: Shipment Arrives at Clinic
    GOODS_RECEIVED_VERIFYING --> STOCKED_IN: Inspection Passed & Batches Added
    GOODS_RECEIVED_VERIFYING --> DISCREPANCY_QUARANTINED: Variance / Cold Chain Breach
    STOCKED_IN --> [*]
    DISCREPANCY_QUARANTINED --> [*]"""
    }

    # =========================================================================
    # WF-015: Laboratory Testing Workflow
    # =========================================================================
    m15 = WORKFLOW_MAP["WF-015"]
    specs["WF-015"] = {
        "id": "WF-015", "num": "15", "name": m15["name"], "domain": m15["domain"],
        "exec_summary": {
            "purpose": "Governs point-of-care laboratory diagnostics in Namma Clinic: electronic test order reception, barcoded specimen tube labeling, blood/urine sample collection, rapid diagnostic kit / dry chemistry analyzer execution, double-verification result entry, automated biological reference range validation, panic value critical alerting, and real-time electronic result delivery to the Medical Officer's screen.",
            "rationale": "Point-of-care diagnostics (Hemoglobin, Random Blood Sugar, Urine Albumin/Sugar, Rapid Malaria/Dengue/HIV, Pregnancy) provide crucial same-day clinical answers in primary care. Delays, sample mislabeling, or uncommunicated panic values (e.g., Blood Sugar < 40 or > 450 mg/dL, Hb < 5.0 g/dL) lead to catastrophic diagnostic delays.",
            "clinical_impact": "Enables rapid, definitive evidence-based diagnosis within 15-20 minutes of doctor ordering; prevents wrong-patient specimen errors through barcode scanning; and immediately alerts clinicians to life-threatening panic values.",
            "system_impact": "Composes FHIR R4 Specimen and DiagnosticReport resources; integrates with local point-of-care laboratory analyzers via serial/Bluetooth bridges; broadcasts results via local WebSockets.",
            "risk_profile": "Hemolyzed or clotted capillary blood samples; expired rapid test cassettes; specimen tube labeling confusion; and power loss during analyzer centrifugation."
        },
        "objectives": [
            {"id": "OBJ-WF15-01", "title": "Rapid Turnaround Time", "desc": "Deliver verified test results to the Medical Officer's screen within 20 minutes of specimen collection.", "metric": "Diagnostic Turnaround Time p90 < 20 min", "verification": "Specimen accessioning to result sign-off duration logs"},
            {"id": "OBJ-WF15-02", "title": "Zero Specimen Mislabeling", "desc": "Guarantee 100% barcode labeling of all collection tubes at the patient chair before phlebotomy.", "metric": "Tube Barcode Compliance = 100%", "verification": "Accessioning scan verification records"},
            {"id": "OBJ-WF15-03", "title": "Instant Panic Value Escalation", "desc": "Broadcast visual and audible panic alert to Doctor Chamber within 30 seconds of committing critical test value.", "metric": "Panic Value Alert Latency < 30 sec", "verification": "Panic value telemetry timer assertion"},
            {"id": "OBJ-WF15-04", "title": "Internal Quality Control (IQC) Enforcement", "desc": "Enforce mandatory daily negative/positive control test validation on analyzers before patient processing.", "metric": "Daily IQC Compliance = 100%", "verification": "Laboratory morning quality control log"}
        ],
        "in_scope": [
            {"area": "Core Point-of-Care Tests", "desc": "Hb (Hemocue), Blood Glucose (Glucometer), Urine Albumin/Sugar/Pregnancy (Dipstick), Rapid Malaria Ag, Dengue NS1, HIV 1/2, Syphilis, Typhoid."},
            {"area": "Barcoded Specimen Tracking", "desc": "Printing and scanning 30mm x 20mm specimen barcodes tied to the unique encounter ID."},
            {"area": "Reference Range Validation", "desc": "Automated evaluation against age- and sex-adjusted biological reference intervals."},
            {"area": "Electronic Diagnostic Report", "desc": "Generation of digital diagnostic report with lab tech electronic sign-off."}
        ],
        "out_of_scope": [
            {"area": "Microbiology Bacterial Cultures", "desc": "Blood culture and antibiotic sensitivity testing (72-hour incubation); referred to District Hospital.", "handoff": "Bowring Hospital Central Microbiology Lab"},
            {"area": "Histopathology & Biopsies", "desc": "Tissue biopsy tissue processing; referred to Medical College Pathology Dept.", "handoff": "Victoria Hospital Pathology"}
        ],
        "actors": [
            {"id": "ACT-WF15-01", "type": "Human", "name": "Laboratory Technician", "responsibilities": "Collects specimen, prints/affixes barcode, runs test on analyzer, enters/verifies results, executes daily QC.", "permissions": "Lab Test Accession, Result Entry, Panic Alert Trigger, QC Log", "failure_duty": "Performs manual micro-cuvette testing if automated analyzer malfunctions.", "inputs": "Patient token, test orders, biological specimen", "decisions": "Determines sample adequacy; verifies result validity before commit.", "outputs": "Signed diagnostic report, panic value alerts", "recovery": "Requests repeat specimen collection if sample is hemolyzed or clotted."},
            {"id": "ACT-WF15-02", "type": "Human", "name": "Medical Officer", "responsibilities": "Reviews committed lab results, interprets in clinical context, adjusts treatment plan.", "permissions": "Lab Order Create, Result Review, Diagnostic Finalize", "failure_duty": "Responds immediately to laboratory panic value call.", "inputs": "Committed diagnostic report, panic alert notification", "decisions": "Determines clinical significance of abnormal lab values.", "outputs": "Adjusted prescription or emergency referral", "recovery": "Orders confirmatory testing if clinical picture conflicts with result."}
        ],
        "personas": [
            {"id": "PERSONA-004", "name": "Roopa Mary", "role": "Clinic Lab Technician", "env": "Compact lab corner running 30-50 tests per morning.", "goals": "Enter test results quickly without switching screens; never confuse tubes.", "pain_points": "Manual transcription from analyzer paper tape into computer forms.", "adaptations": "Auto-sync from digital glucometer/Hemocue via USB serial bridge and single-key result commit."}
        ],
        "rbac_matrix": [
            {"role": "ROLE-004", "title": "Laboratory Technician", "read": "Lab Orders, Patient Demographics", "create": "Specimen Record, Test Result", "update": "Draft Result", "delete": "None", "override": "Panic Value Flag", "signoff": "Lab Technician Result Signoff"},
            {"role": "ROLE-002", "title": "Medical Officer", "read": "Lab Results, Historical Graphs", "create": "Lab Order", "update": "Clinical Note", "delete": "None", "override": "None", "signoff": "Diagnostic Interpretation Signoff"}
        ],
        "preconditions": [
            {"id": "PRE-WF15-01", "desc": "Electronic lab test order created and signed by Medical Officer (WF-011).", "check": "lab_order.status == 'ORDERED'", "on_fail": "Technician cannot collect blood without valid doctor order."},
            {"id": "PRE-WF15-02", "desc": "Daily morning calibration and quality control check logged and passed.", "check": "lab_qc.daily_status == 'PASSED'", "on_fail": "Block patient testing until daily QC control test passed."}
        ],
        "triggers": [
            {"id": "TRIG-WF15-01", "class": "Queue Trigger", "event": "Technician calls patient token to laboratory collection chair", "source": "Lab Station UI", "payload": "{ token_id: 'SNR-001', station: 'LAB-01' }", "latency": "< 100ms to load ordered test panels"}
        ],
        "inputs": [
            {"name": "specimen_type", "type": "Enum(CAPILLARY_BLOOD, VENOUS_BLOOD, URINE, SPUTUM)", "req": "Mandatory", "source": "Collection Protocol", "val": "Valid specimen category", "priv": "Clinical", "enc": "Plaintext", "ex": "CAPILLARY_BLOOD", "on_err": "Default to CAPILLARY_BLOOD"},
            {"name": "test_code", "type": "String(16)", "req": "Mandatory", "source": "Test Catalog", "val": "Valid test identifier", "priv": "Clinical", "enc": "Plaintext", "ex": "LAB-HEMOGLOBIN", "on_err": "Reject unknown test"},
            {"name": "test_value", "type": "Decimal(6,2)", "req": "Mandatory", "source": "Analyzer / Technician", "val": "Numeric test result", "priv": "Clinical", "enc": "Plaintext", "ex": "13.4", "on_err": "Flag out of plausible range"}
        ],
        "outputs": {
            "success": [
                {"name": "Signed Diagnostic Report", "desc": "FHIR DiagnosticReport with quantitative value, unit, reference interval, and flag.", "format": "FHIR R4 JSON", "recipient": "Doctor Chamber Screen & Patient EMR"},
                {"name": "Lab Result Notification", "desc": "WebSocket event alerting doctor that lab results are ready for review.", "format": "WebSocket JSON Event", "recipient": "Doctor Chamber Dashboard"}
            ],
            "failure": [
                {"name": "Panic Value Emergency Alert", "desc": "Critical value alert dispatched immediately to Doctor Chamber screen.", "action": "Sounds audible chime and flashes red banner on Doctor workstation."}
            ]
        },
        "sequence_diagram": """sequenceDiagram
    autonumber
    actor P as Patient
    actor L as Lab Technician
    participant UI as Lab Workstation
    participant DB as SQLite DB
    participant WS as WebSocket Hub
    actor D as Medical Officer
    P->>L: 1. Citizen arrives at Lab Chair
    L->>UI: 2. Call Token SNR-001 -> View Orders: Hb & Blood Sugar
    UI-->>L: 3. Print 2 Barcode Labels (Tube & Slide)
    L->>P: 4. Fingerprick & Fill Micro-cuvette
    L->>UI: 5. Hemocue Analyzer: Hb = 13.4 g/dL, Glucometer: Sugar = 142 mg/dL
    L->>UI: 6. Click 'Verify & Commit Results'
    UI->>DB: 7. Store FHIR DiagnosticReport (Status: FINAL)
    UI->>WS: 8. Publish LabResultsReady(Token SNR-001)
    WS-->>D: 9. Pop-up on Doctor Screen: 'Lab Results Ready for SNR-001'""",
        "activity_diagram": """flowchart TD
    Start([Citizen Arrives at Lab Desk]) --> CallPatient[Technician Calls Token on Workstation]
    CallPatient --> LoadOrders[Display Ordered Tests from Doctor Consultation]
    LoadOrders --> PrintBarcode[Print Scannable Barcode Labels]
    PrintBarcode --> CollectSpecimen[Collect Capillary Blood / Urine Specimen]
    CollectSpecimen --> AffixBarcode[Affix Barcode Label to Collection Tube / Cuvette]
    AffixBarcode --> ExecuteTest[Insert into Analyzer / Process Rapid Cassette]
    ExecuteTest --> ReadResult[Read Result Value from Device Display]
    ReadResult --> InputResult[Enter Result into Lab Form]
    InputResult --> CheckBounds{Value Within Biological Range?}
    CheckBounds -- No / Impossible --> PromptRetest[Prompt: Value Plausibility Violation! Retest.]
    PromptRetest --> ExecuteTest
    CheckBounds -- Yes --> EvaluatePanic{Does Value Breach Panic Value Threshold?}
    EvaluatePanic -- Yes (e.g. Sugar > 450) --> FlagPanic[Mark CRITICAL PANIC VALUE]
    FlagPanic --> BroadcastPanic[Broadcast Instant Red Audio/Visual Panic Alert to Doctor]
    EvaluatePanic -- No --> MarkNormal[Mark Normal / Borderline]
    BroadcastPanic --> CommitReport[Commit Electronic Diagnostic Report]
    MarkNormal --> CommitReport
    CommitReport --> PushWebSocket[Push Results via Local WebSocket to Doctor Chamber]
    PushWebSocket --> End([Testing Complete & Doctor Reviews Results])""",
        "state_diagram": """stateDiagram-v2
    [*] --> ORDER_RECEIVED
    ORDER_RECEIVED --> SPECIMEN_COLLECTED: Barcode Affixed & Blood Drawn
    SPECIMEN_COLLECTED --> ANALYSIS_IN_PROGRESS: In Analyzer / Incubating
    ANALYSIS_IN_PROGRESS --> RESULTS_ENTERED: Raw Result Transcribed
    RESULTS_ENTERED --> PANIC_ESCALATED: Panic Value Threshold Breached
    RESULTS_ENTERED --> VERIFIED_FINAL: Normal / Non-critical Value
    PANIC_ESCALATED --> VERIFIED_FINAL: Panic Alert Delivered & Acknowledged
    VERIFIED_FINAL --> [*]"""
    }

    return specs

def write_group3_file():
    specs = get_group3_specs()
    print("Building Group 3 Workflows (WF-011 to WF-015)...")

    header = '''#!/usr/bin/env python3
"""
data_wf11_to_15.py
Clean, self-contained domain specifications for Workflows 11 to 15:
  - WF-011: Doctor Clinical Consultation, SOAP Documentation & CDSS Advisory Workflow
  - WF-012: Electronic Prescription, Drug Interaction & Safety Verification Workflow
  - WF-013: Pharmacy Dispensing, FEFO Inventory Allocation & Patient Counseling Workflow
  - WF-014: Pharmacy Stock Replenishment, Indenting & Cold-Chain Inventory Control Workflow
  - WF-015: Point-of-Care Laboratory Testing, Barcoding & Panic Value Alert Workflow

Exports:
  DATA_WF11_TO_15 (dict mapping 'WF-011'..'WF-015' to enriched 67-section workflow dicts)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_factory import build_workflow_object
from build_group3 import get_group3_specs

def get_group3_workflows():
    specs = get_group3_specs()
    return {wfid: build_workflow_object(spec) for wfid, spec in specs.items()}

if __name__ == "__main__":
    from workflow_generator import render_workflow_document
    from common import count_lines, find_duplicate_paragraphs
    print("Testing data_wf11_to_15.py...")
    wfs = get_group3_workflows()
    docs = {}
    for wfid, wf_data in wfs.items():
        doc = render_workflow_document(wf_data)
        docs[wfid] = doc
        counts = count_lines(doc)
        status = "PASS" if counts["substantive"] >= 2000 else "FAIL"
        print(f"  {wfid}: Total = {counts['total']}, Substantive = {counts['substantive']} [{status}]")

    dups = find_duplicate_paragraphs(docs, min_len=60)
    print(f"  Duplicate paragraphs within Group 3: {len(dups)}")
'''
    with open('scripts/workflows/data_wf11_to_15.py', 'w', encoding='utf-8') as f:
        f.write(header)
    print("Wrote scripts/workflows/data_wf11_to_15.py")

if __name__ == "__main__":
    write_group3_file()
