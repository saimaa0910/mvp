"""
srs_data_specialized.py
Specialized Requirement Registries for Phase 05 SRS:
- Security Requirements (SRS-SEC-001 to 030)
- Privacy Requirements (SRS-PRIV-001 to 020)
- Clinical Requirements (SRS-CR-001 to 020)
- Operational Requirements (SRS-OR-001 to 020)
- Offline Requirements (SRS-OFF-001 to 020)
- Integration Requirements (SRS-INT-001 to 020)
- Data Requirements (SRS-DATA-001 to 020)
- UI Requirements (SRS-UI-001 to 020)
"""

from typing import Dict, List, Any

def _make_records(prefix: str, count: int, titles: Dict[int, str], upstream_pfx: str) -> List[Dict[str, Any]]:
    records = []
    for i in range(1, count + 1):
        t = titles.get(i, f"Standard Requirement {i:02d}")
        rec_id = f"{prefix}-{i:03d}"
        records.append({
            "id": rec_id,
            "title": t,
            "description": f"The Namma Clinic platform shall enforce {t.lower()} across all clinic workstations and central cloud services conforming to municipal health governance standards.",
            "rationale": f"Essential architectural invariant for {t.lower()} safeguarding clinic operations and citizen trust.",
            "upstream_ref": f"{upstream_pfx}-{i:03d}",
            "priority": "MUST" if i <= int(count * 0.75) else "SHOULD",
            "verification_method": f"Automated Compliance Test ({rec_id})",
            "acceptance_criteria": f"Given an operational environment, when {t.lower()} is validated, then the system enforces the specified constraints without failure.",
            "bdd_scenario": [
                f"Given the platform security and architecture subsystem is initialized",
                f"When verification runs for '{t}'",
                f"Then the system passes all invariant checks for {rec_id}",
                "And records zero non-compliance exceptions in the audit log."
            ],
            "downstream_artifacts": [f"PLANNED-{prefix}-{i:03d}"]
        })
    return records

SEC_TITLES = {
    1: "Cryptographic Staff JWT Token Authentication",
    2: "Role-Based Access Control (RBAC) Module Barrier",
    3: "Attribute-Based Access Control (ABAC) for Sensitive Encounters",
    4: "15-Minute Inactive Session Automatic Invalidation",
    5: "Argon2id Salted Staff Password Storage",
    6: "MFA Readiness via TOTP for System Administrators",
    7: "TLS 1.3 Strict Invariant for All Network Transmissions",
    8: "AES-256 GCM Encryption for Sensitive PHI at Rest",
    9: "Master Key Rotation via Central Hardware Security Module (HSM)",
    10: "Database Credential Segregation & Least Privilege Access",
    11: "Immutable WORM Audit Ledger with SHA-256 Hash Chaining",
    12: "Automated Log Tamper Detection & Integrity Verification",
    13: "API Gateway Token Bucket Rate Limiting & Throttling",
    14: "DDoS Mitigation & Layer 7 Abuse Prevention",
    15: "Cross-Site Request Forgery (CSRF) Prevention via SameSite Strict",
    16: "Cross-Site Scripting (XSS) Prevention & Content Security Policy (CSP)",
    17: "Strict SQL Parameterization & ORM Query Escaping",
    18: "Server-Side Request Forgery (SSRF) Whitelist Validation",
    19: "Session Hijacking Defense via Client IP & Fingerprint Binding",
    20: "Hardware Appliance BIOS Password & Secure Boot Enforcement",
    21: "Browser Sandbox Security & Local Cache Scrambling",
    22: "Edge SQLite Local Database SQLCipher Encryption",
    23: "Endpoint Defense Against Removable USB Drive Execution",
    24: "Automated Daily Vulnerability & Dependency CVE Scanning",
    25: "Software Bill of Materials (SBOM) Tracking in CI/CD",
    26: "Static Application Security Testing (SAST) Quality Gate",
    27: "Dynamic Application Security Testing (DAST) Baseline Execution",
    28: "Security Incident Logging & High-Priority CISO Notification",
    29: "Automated IP Blacklisting on Sustained Auth Failures",
    30: "Cryptographic Digital Signature on All Prescription Payloads"
}

PRIV_TITLES = {
    1: "Informed Digital Consent Logging Prior to Health Data Capture",
    2: "Zero-Plaintext Protected Health Information (PHI) in System Logs",
    3: "Granular Consent Scope Limitation (Treatment vs Research vs External)",
    4: "Citizen Statutory Right to Consent Revocation & Data Quarantine",
    5: "De-identified Data Export for Municipal Epidemiological Analytics",
    6: "Automated Data Retention & Lifecycle Expiration Policy",
    7: "Reproductive & Psychiatric Clinical Record Access Masking",
    8: "Data Protection Officer (DPO) Audit Console & Access Ledger",
    9: "Data Breach Notification & Statutory MeitY Disclosures",
    10: "Aadhaar Number Tokenization & Masking (Zero Plaintext Storage)",
    11: "Purposeful Limitation Invariant for Public Health Registries",
    12: "Citizen Privacy Notice Display in Vernacular Kannada and English",
    13: "Minors & Pediatric Data Consent Authorization by Legal Guardian",
    14: "Right to Data Portability via FHIR R4 Bundle Export",
    15: "Internal Staff Snooping Prevention & Peer Patient Record Shield",
    16: "Third-Party Integration Zero-Knowledge Privacy Boundary",
    17: "Biometric Template Immediate Scrubbing Post-Authentication",
    18: "Emergency Resuscitation Clinical Access Post-Hoc Consent Audit",
    19: "Citizen Grievance Redressal Mechanism for Privacy Concerns",
    20: "Annual Privacy Impact Assessment (PIA) Conformance Verification"
}

CR_TITLES = {
    1: "Drug-Drug Interaction (DDI) Blocking Alert Guardrail",
    2: "Triage Modified Early Warning Score (MEWS) Red-Flag Escalation",
    3: "Pediatric & Geriatric Safe Dosage Boundary Enforcement",
    4: "Emergency Resuscitation Clinical Break-Glass Override Protocol",
    5: "Documented Allergy & Cross-Sensitivity Prescription Hard-Stop",
    6: "Duplicate Therapy & Polypharmacy Reduction Alerts",
    7: "Essential Medicines Formulary Standard Treatment Guideline Compliance",
    8: "Mandatory Chronic Disease Protocol for Hypertension & Diabetes",
    9: "High-Risk Antenatal Care (ANC) Pregnancy Identification",
    10: "Severe Acute Malnutrition (SAM) Pediatric Screening Alarm",
    11: "Notifiable Infectious Disease Immediate Surveillance Flagging",
    12: "Panic Laboratory Critical Value Immediate Doctor Interception",
    13: "Antibiotic Stewardship & Schedule H1 Restrictive Dispensing",
    14: "Cold-Chain Vaccine Viability & Thermal Breach Invalidation",
    15: "Secondary Referral Urgency Triaging (Routine vs Urgent vs Code Red)",
    16: "Unexamined Patient Queue Stall & Clinical Delay Alert",
    17: "Clinical Counter-Signature Requirement for High-Risk Injections",
    18: "Surgical Trauma Initial Stabilization Checklist Enforcement",
    19: "Diagnostic ICD-10 & SNOMED CT Clinical Terminology Binding",
    20: "Physician Clinical Autonomy & Final Prescription Authority"
}

OR_TITLES = {
    1: "Daily Morning Facility Cold-Boot & Hardware Pre-Flight Verification",
    2: "Shift Handover Cashless Queue & Operational Statistics Tally",
    3: "Physical vs Digital Pharmacy Inventory Reconciliation Protocol",
    4: "Clinic Operating Hours & Day Session Lifecycle Management",
    5: "Staff Roster Allocation & Multi-Doctor Room Assignment",
    6: "Citizen Waiting Hall Crowd Management & Overcrowding Alerts",
    7: "Thermal Printer Paper Replenishment & Hardware Peripheral Readiness",
    8: "2D Barcode Handheld Scanner Functional Commissioning Check",
    9: "Edge Mini-Server Daily Local Backup to External Encrypted Media",
    10: "Power Cutover to Line-Interactive UPS & Battery Run-time Monitoring",
    11: "Grid Broadband WAN Outage & Automatic Cellular 4G Switchover",
    12: "End-of-Day Clinic Closure & Unexamined Token Roll-Over Runbook",
    13: "Bio-Medical Waste Bag Weight Logging & Disposal Chain of Custody",
    14: "Clinic Housekeeping & Sanitation Check Interval Verification",
    15: "Emergency First-Aid & Resuscitation Kit Seal Inspection",
    16: "Public Grievance Box Physical Clearance & Digital Ledger Entry",
    17: "ASHA Field Health Worker Monthly Ward Coordination Review",
    18: "Municipal Ward Health Officer (WHO) Monthly Audit Inspection",
    19: "Essential Drug Stock Emergency Inter-Clinic Transfer Protocol",
    20: "Clinic Annual Infrastructure & Equipment Calibration Audit"
}

OFF_TITLES = {
    1: "Autonomous 72-Hour Local Clinic Operation without Broadband",
    2: "Deterministic Vector Clock Sync & Conflict Resolution Engine",
    3: "Local Client-Side Mutation Journaling in SQLite / IndexedDB",
    4: "Bandwidth-Throttled Adaptive Cloud Synchronization Engine",
    5: "Local Staff Session Authentication via Argon2id Cached Credentials",
    6: "Offline Clinical Consultation & Electronic Prescription Storage",
    7: "Offline Pharmacy Inventory Batch Decrement & Dispensation Log",
    8: "Offline Rapid Laboratory Diagnostic Test Result Entry",
    9: "Offline Multi-Room Queue Token Generation & TV Audio Calling",
    10: "Network Partition Detection via Heartbeat Ping & Fast Fallback",
    11: "Reconnection Handshake & Transactional Delta Replay Protocol",
    12: "Vector Clock Timestamp Ordering across Edge & Central Cloud",
    13: "CRDT Register Model for Non-Conflicting Data Synchronization",
    14: "Duplicate Mutation Rejection via UUIDv7 Idempotency Keys",
    15: "Physical USB Drive Encrypted State Import for Disaster Sync",
    16: "Local Edge SQLite Write-Ahead Logging (WAL) Concurrency Tuning",
    17: "Offline Data Expiry & Local Cache Scrubbing after 14 Days",
    18: "Sync Progress Indicator & User-Visible Offline Mode Banner",
    19: "High-Priority Emergency Case Synchronous Cloud Preemption",
    20: "Post-Partition Integrity Audit & Data Reconciliation Report"
}

INT_TITLES = {
    1: "ABDM Milestone 1 (M1) ABHA Verification & Profile Linking Gateway",
    2: "ABDM Milestone 2 (M2) HIP FHIR R4 Care Context Publishing",
    3: "ABDM Milestone 3 (M3) HIU Consent Artifact Processing Engine",
    4: "Karnataka State SMS Gateway (KSSD / CDAC) Messaging Bridge",
    5: "Citizen WhatsApp Business API Notification Integration",
    6: "Integrated Disease Surveillance Programme (IDSP) Syndromic Feed",
    7: "GVK-EMRI 108 Emergency Medical Services Ambulance Dispatch API",
    8: "eHospital & BBMP Secondary Referral Bed Management Exchange",
    9: "Direct ESC/POS Thermal Receipt & Barcode Printer Protocol",
    10: "USB/HID 2D DataMatrix Handheld Barcode Scanner Interface",
    11: "Semi-Automated Point-of-Care Laboratory Analyzer ASTM/HL7 Feed",
    12: "Waiting Hall Display TV MQTT Telemetry & Digital Signage Feed",
    13: "State Central Drug Warehouse (KDLWS) Indent & Supply Sync",
    14: "BBMP Municipal Ward GIS Geographic Boundary Mapping Service",
    15: "State Civil Registration System (CRS) Birth/Death Event Sync",
    16: "National TB Elimination Program (Ni-kshay) Referral Interface",
    17: "National Vector Borne Disease Control (NVBDCP) Malaria Reporting",
    18: "UIDAI L1 Fingerprint / Biometric Device Hardware Driver Bridge",
    19: "Municipal Financial Management Cashless Transaction Audit Log",
    20: "OpenAPI 3.1 Documented REST & gRPC Internal Integration Gateway"
}

DATA_TITLES = {
    1: "UUIDv7 Monotonically Increasing Primary Key Identifier Strategy",
    2: "Temporal Data Model & Historical Audit Timestamp Tracking",
    3: "Soft Deletion Architecture with Tombstone Records (Zero Hard Deletes)",
    4: "Master Patient Index (MPI) Relational Schema & Demographic Store",
    5: "Clinical Encounter & SOAP Progress Notes Relational Schema",
    6: "SNOMED CT & ICD-10 Dual-Coded Diagnosis Association Schema",
    7: "Electronic Prescription & Dosage Timing Structured Data Domain",
    8: "Pharmacy Inventory, Bin Locations & FEFO Batch Ledger Schema",
    9: "Point-of-Care Laboratory Order & Quantitative Result Schema",
    10: "Queue Token, Consultation Room & State Transition Event Store",
    11: "Secondary Hospital Referral & Clinical Dossier Relational Model",
    12: "Digital Informed Consent Artifacts & DPDP Scope Storage",
    13: "Immutable WORM Audit Ledger with Cryptographic Hash Linkage",
    14: "Role, Staff Persona & Granular Entitlement Permission Matrix",
    15: "Offline Mutation Journal & Vector Clock Replication Store",
    16: "Dimensional Star Schema for Municipal Public Health BI (Facts & Dims)",
    17: "PostgreSQL 16 Enterprise Relational Schema & Partitioning Strategy",
    18: "Edge SQLite 3 Relational Mirror Schema & Index Configuration",
    19: "Automated Nightly Incremental & Full Database Backup Architecture",
    20: "Database Migration Versioning & Backward-Compatible Schema Evolution"
}

UI_TITLES = {
    1: "Responsive Progressive Web Application (PWA) Application Shell",
    2: "Bilingual Kannada (kn-IN) and English (en-IN) Interface Rendering",
    3: "Web Content Accessibility Guidelines (WCAG 2.1 AA) Design Standard",
    4: "Touch-Optimized Form Controls with 48x48 dp Minimum Hit Targets",
    5: "High-Contrast Visual Indicators for Clinical Danger Sign Banners",
    6: "Keyboard-Navigable Clinical Entry Workflow (Alt+Key Accelerators)",
    7: "Waiting Hall Public Display TV Large-Font Queue Token Canvas",
    8: "Front Desk Rapid Patient Intake & Demographic Search Interface",
    9: "Nursing Triage Vital Signs & MEWS Visual Score Calculator Screen",
    10: "Doctor Outpatient Consultation SOAP Note & Diagnostic Workspace",
    11: "Electronic Prescription Formulary Search with Auto-Complete Chips",
    12: "Pharmacy Counter Dispensing & Barcode Verification Modal",
    13: "Laboratory Rapid Result Entry & Critical Value Warning Prompts",
    14: "Secondary Referral Dispatch & Emergency Ambulance Status HUD",
    15: "Offline Operational Status Persistent Header Banner & Sync Badge",
    16: "Thermal Printer 80mm ESC/POS Layout Designer & Preview Engine",
    17: "Citizen Self-Service Token Kiosk Touchscreen Welcome Interface",
    18: "Role-Based Dynamic Navigation Menu & Security Feature Toggles",
    19: "Color-Blind Safe Palette Selection for Triage and Status Codes",
    20: "Comprehensive Form Validation Error Summary & Contextual Guidance"
}

ALL_SECURITY_REQUIREMENTS = _make_records("SRS-SEC", 30, SEC_TITLES, "SECR")
ALL_PRIVACY_REQUIREMENTS = _make_records("SRS-PRIV", 20, PRIV_TITLES, "PRIV")
ALL_CLINICAL_REQUIREMENTS = _make_records("SRS-CR", 20, CR_TITLES, "CR")
ALL_OPERATIONAL_REQUIREMENTS = _make_records("SRS-OR", 20, OR_TITLES, "OR")
ALL_OFFLINE_REQUIREMENTS = _make_records("SRS-OFF", 20, OFF_TITLES, "OFF")
ALL_INTEGRATION_REQUIREMENTS = _make_records("SRS-INT", 20, INT_TITLES, "INT")
ALL_DATA_REQUIREMENTS = _make_records("SRS-DATA", 20, DATA_TITLES, "DATA")
ALL_UI_REQUIREMENTS = _make_records("SRS-UI", 20, UI_TITLES, "UI")
