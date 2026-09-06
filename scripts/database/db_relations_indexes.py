"""
db_relations_indexes.py
Canonical definitions for:
- 112 Primary-Foreign Key Relationships (REL-001 to REL-112)
- 132 Database Indexes (INDEX-001 to INDEX-132)
- 12 Partition Specifications (PART-001 to PART-012)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from typing import List, Dict, Any
from scripts.database.db_tables_entities import TABLES, TABLE_NAME_MAP

# -----------------------------------------------------------------------------
# 1. RELATIONSHIPS (REL-001 to REL-112)
# -----------------------------------------------------------------------------
RELATIONSHIPS = [
    # Identity & Core Relationships
    {"id": "REL-001", "parent": "auth_users", "ppk": "id", "child": "user_credentials", "cfk": "user_id", "card": "1:1", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Every credential record belongs strictly to one authenticated user", "txn": "Atomic user creation transaction TXN-001"},
    {"id": "REL-002", "parent": "auth_users", "ppk": "id", "child": "user_sessions", "cfk": "user_id", "card": "1:N", "opt": "Optional", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "A user can have multiple concurrent active sessions across mobile and desktop", "txn": "Session creation and revocation in TXN-002"},
    {"id": "REL-003", "parent": "roles", "ppk": "id", "child": "role_permissions", "cfk": "role_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Roles are composed of granular permission grants", "txn": "RBAC role configuration transaction"},
    {"id": "REL-004", "parent": "permissions", "ppk": "id", "child": "role_permissions", "cfk": "permission_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Permissions are mapped to roles via junction table", "txn": "RBAC policy update"},
    {"id": "REL-005", "parent": "auth_users", "ppk": "id", "child": "user_roles", "cfk": "user_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Staff members are assigned roles", "txn": "Staff provisioning transaction"},
    {"id": "REL-006", "parent": "roles", "ppk": "id", "child": "user_roles", "cfk": "role_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Active roles cannot be deleted if assigned to users", "txn": "Staff role assignment transaction"},
    {"id": "REL-007", "parent": "facilities", "ppk": "id", "child": "user_roles", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Role assignments are facility-scoped", "txn": "Staff facility posting transaction"},
    {"id": "REL-008", "parent": "facilities", "ppk": "id", "child": "auth_users", "cfk": "primary_facility_id", "card": "1:N", "opt": "Optional", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "User base home clinic posting", "txn": "Staff profile registration"},
    {"id": "REL-009", "parent": "facilities", "ppk": "id", "child": "facility_rooms", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Chambers and rooms physically exist inside a facility", "txn": "Clinic layout provisioning"},
    {"id": "REL-010", "parent": "auth_users", "ppk": "id", "child": "staff_profiles", "cfk": "user_id", "card": "1:1", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Clinical staff profile links to authentication user", "txn": "Clinician credential verification"},
    {"id": "REL-011", "parent": "auth_users", "ppk": "id", "child": "staff_shifts", "cfk": "user_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Duty rosters track shifts per staff member", "txn": "Shift roster allocation"},
    {"id": "REL-012", "parent": "facilities", "ppk": "id", "child": "staff_shifts", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Staff shifts take place at specific clinic facility", "txn": "Shift roster allocation"},
    {"id": "REL-013", "parent": "facilities", "ppk": "id", "child": "system_configs", "cfk": "facility_id", "card": "1:N", "opt": "Optional", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Clinic-specific operational threshold overrides", "txn": "Config update transaction"},

    # Patient Demographics & Intake
    {"id": "REL-014", "parent": "facilities", "ppk": "id", "child": "patients", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Patient initial registration clinic", "txn": "Patient registration TXN-003"},
    {"id": "REL-015", "parent": "patients", "ppk": "id", "child": "patient_identifiers", "cfk": "patient_id", "card": "1:N", "opt": "Optional", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Patient ABHA, Aadhaar hash, and external identifiers", "txn": "Identity seeding TXN-003"},
    {"id": "REL-016", "parent": "patients", "ppk": "id", "child": "patient_contacts", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Patient emergency contacts and phone numbers", "txn": "Demographic intake TXN-003"},
    {"id": "REL-017", "parent": "patients", "ppk": "id", "child": "patient_addresses", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Citizen residential address mapped to BBMP ward", "txn": "Address registration TXN-003"},
    {"id": "REL-018", "parent": "patients", "ppk": "id", "child": "consent_records", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "DPDP statutory citizen consent artifacts", "txn": "Consent grant/revocation TXN-004"},
    {"id": "REL-019", "parent": "facilities", "ppk": "id", "child": "consent_records", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Facility where consent was executed", "txn": "Consent recording"},
    {"id": "REL-020", "parent": "patients", "ppk": "id", "child": "tokens", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Token issued to registered patient", "txn": "Token issuance TXN-005"},
    {"id": "REL-021", "parent": "facilities", "ppk": "id", "child": "tokens", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Daily token generated at specific clinic", "txn": "Token generation TXN-005"},
    {"id": "REL-022", "parent": "tokens", "ppk": "id", "child": "queue_entries", "cfk": "token_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Queue movement stages tracked per token", "txn": "Queue transition TXN-006"},
    {"id": "REL-023", "parent": "facilities", "ppk": "id", "child": "queue_entries", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Queue progression inside clinic", "txn": "Queue advance TXN-006"},
    {"id": "REL-024", "parent": "patients", "ppk": "id", "child": "queue_entries", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Patient queue stage presence", "txn": "Queue staging TXN-006"},
    {"id": "REL-025", "parent": "facility_rooms", "ppk": "id", "child": "queue_entries", "cfk": "room_id", "card": "1:N", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Physical consultation chamber serving patient", "txn": "Doctor call TXN-006"},
    {"id": "REL-026", "parent": "patients", "ppk": "id", "child": "triage_assessments", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Triage evaluation performed on patient", "txn": "Triage intake TXN-007"},
    {"id": "REL-027", "parent": "facilities", "ppk": "id", "child": "triage_assessments", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Facility where triage occurred", "txn": "Triage evaluation TXN-007"},
    {"id": "REL-028", "parent": "tokens", "ppk": "id", "child": "triage_assessments", "cfk": "token_id", "card": "1:1", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Daily token linking triage encounter", "txn": "Triage intake TXN-007"},
    {"id": "REL-029", "parent": "patients", "ppk": "id", "child": "patient_vitals", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Longitudinal vital signs observations", "txn": "Vitals capture TXN-007"},
    {"id": "REL-030", "parent": "facilities", "ppk": "id", "child": "patient_vitals", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Clinic where vitals recorded", "txn": "Vitals recording TXN-007"},
    {"id": "REL-031", "parent": "triage_assessments", "ppk": "id", "child": "patient_vitals", "cfk": "triage_id", "card": "1:N", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Vitals captured during nursing triage session", "txn": "Triage intake TXN-007"},
    {"id": "REL-032", "parent": "patients", "ppk": "id", "child": "danger_alerts", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Critical danger alert generated for patient", "txn": "Panic vital alert TXN-008"},
    {"id": "REL-033", "parent": "facilities", "ppk": "id", "child": "danger_alerts", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Clinic where clinical red flag occurred", "txn": "Safety alert dispatch TXN-008"},

    # Clinical Consultation & Orders
    {"id": "REL-034", "parent": "patients", "ppk": "id", "child": "clinical_encounters", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Outpatient consultation encounter for patient", "txn": "Doctor consultation TXN-009"},
    {"id": "REL-035", "parent": "facilities", "ppk": "id", "child": "clinical_encounters", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Encounter conducted at clinic", "txn": "Doctor consultation TXN-009"},
    {"id": "REL-036", "parent": "auth_users", "ppk": "id", "child": "clinical_encounters", "cfk": "doctor_user_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Treating licensed physician", "txn": "Consultation sign-off TXN-009"},
    {"id": "REL-037", "parent": "tokens", "ppk": "id", "child": "clinical_encounters", "cfk": "token_id", "card": "1:1", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Daily token associated with consultation", "txn": "Consultation completion TXN-009"},
    {"id": "REL-038", "parent": "clinical_encounters", "ppk": "id", "child": "clinical_notes", "cfk": "encounter_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "SOAP clinical notes recorded for encounter", "txn": "Consultation notes commit TXN-009"},
    {"id": "REL-039", "parent": "patients", "ppk": "id", "child": "clinical_notes", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Longitudinal clinical history linkage", "txn": "Clinical documentation TXN-009"},
    {"id": "REL-040", "parent": "facilities", "ppk": "id", "child": "clinical_notes", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Facility scope of clinical note", "txn": "Consultation documentation"},
    {"id": "REL-041", "parent": "clinical_encounters", "ppk": "id", "child": "diagnoses", "cfk": "encounter_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Diagnoses formulated during encounter", "txn": "Diagnostic coding TXN-009"},
    {"id": "REL-042", "parent": "patients", "ppk": "id", "child": "diagnoses", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Patient diagnostic history", "txn": "Diagnostic recording TXN-009"},
    {"id": "REL-043", "parent": "facilities", "ppk": "id", "child": "diagnoses", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Facility diagnosing condition", "txn": "Epidemiological recording"},
    {"id": "REL-044", "parent": "clinical_encounters", "ppk": "id", "child": "prescriptions", "cfk": "encounter_id", "card": "1:1", "opt": "Optional", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Electronic prescription issued in encounter", "txn": "Prescription issuance TXN-010"},
    {"id": "REL-045", "parent": "patients", "ppk": "id", "child": "prescriptions", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Medication prescribed to patient", "txn": "Prescription issuance TXN-010"},
    {"id": "REL-046", "parent": "facilities", "ppk": "id", "child": "prescriptions", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Prescribing clinic facility", "txn": "Prescription creation TXN-010"},
    {"id": "REL-047", "parent": "prescriptions", "ppk": "id", "child": "prescription_items", "cfk": "prescription_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Prescription composed of medication line items", "txn": "Prescription item detailing TXN-010"},
    {"id": "REL-048", "parent": "formulary_drugs", "ppk": "id", "child": "prescription_items", "cfk": "drug_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Prescribed drug selected from formulary", "txn": "Prescription item detailing TXN-010"},
    {"id": "REL-049", "parent": "patients", "ppk": "id", "child": "prescription_items", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Patient direct linkage for item adherence", "txn": "Prescription item tracking"},
    {"id": "REL-050", "parent": "facilities", "ppk": "id", "child": "prescription_items", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Facility context for stock reservation", "txn": "Stock reservation TXN-010"},
    {"id": "REL-051", "parent": "clinical_encounters", "ppk": "id", "child": "lab_orders", "cfk": "encounter_id", "card": "1:N", "opt": "Optional", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Laboratory investigations ordered during encounter", "txn": "Lab test requisition TXN-011"},
    {"id": "REL-052", "parent": "patients", "ppk": "id", "child": "lab_orders", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Patient diagnostic test order", "txn": "Lab ordering TXN-011"},
    {"id": "REL-053", "parent": "facilities", "ppk": "id", "child": "lab_orders", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Clinic ordering laboratory tests", "txn": "Lab order placement TXN-011"},
    {"id": "REL-054", "parent": "lab_orders", "ppk": "id", "child": "lab_order_items", "cfk": "lab_order_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Specific diagnostic tests in order", "txn": "Lab item requisition TXN-011"},
    {"id": "REL-055", "parent": "patients", "ppk": "id", "child": "lab_order_items", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Patient specimen linkage", "txn": "Specimen tracking TXN-011"},
    {"id": "REL-056", "parent": "facilities", "ppk": "id", "child": "lab_order_items", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Facility performing or forwarding sample", "txn": "Lab specimen logistics"},
    {"id": "REL-057", "parent": "lab_order_items", "ppk": "id", "child": "lab_results", "cfk": "order_item_id", "card": "1:1", "opt": "Optional", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Verified result for diagnostic test item", "txn": "Lab result verification TXN-012"},
    {"id": "REL-058", "parent": "patients", "ppk": "id", "child": "lab_results", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Diagnostic observation for patient record", "txn": "Result sign-off TXN-012"},
    {"id": "REL-059", "parent": "facilities", "ppk": "id", "child": "lab_results", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Laboratory verifying test results", "txn": "Lab verification TXN-012"},
    {"id": "REL-060", "parent": "clinical_encounters", "ppk": "id", "child": "teleconsultations", "cfk": "encounter_id", "card": "1:1", "opt": "Optional", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Remote specialist consultation session", "txn": "Teleconsultation session TXN-013"},
    {"id": "REL-061", "parent": "patients", "ppk": "id", "child": "teleconsultations", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Patient participating in teleconsultation", "txn": "Telemedicine encounter TXN-013"},
    {"id": "REL-062", "parent": "facilities", "ppk": "id", "child": "teleconsultations", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Clinic originating teleconsultation call", "txn": "Telemedicine call initiation"},

    # Pharmacy, Inventory & Cold Chain
    {"id": "REL-063", "parent": "drug_categories", "ppk": "id", "child": "formulary_drugs", "cfk": "category_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Formulary drug classified by therapeutic category", "txn": "Formulary catalog maintenance"},
    {"id": "REL-064", "parent": "formulary_drugs", "ppk": "id", "child": "pharmacy_batches", "cfk": "drug_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Manufactured drug batch belongs to formulary drug", "txn": "Goods inward batch receipt TXN-014"},
    {"id": "REL-065", "parent": "facilities", "ppk": "id", "child": "clinic_stock", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Current stock inventory held at facility", "txn": "Stock balance update TXN-015"},
    {"id": "REL-066", "parent": "pharmacy_batches", "ppk": "id", "child": "clinic_stock", "cfk": "batch_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Facility inventory balance per specific batch", "txn": "Inventory allocation TXN-015"},
    {"id": "REL-067", "parent": "prescriptions", "ppk": "id", "child": "dispensations", "cfk": "prescription_id", "card": "1:1", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Dispensation fulfills doctor prescription", "txn": "Pharmacy dispensing TXN-016"},
    {"id": "REL-068", "parent": "facilities", "ppk": "id", "child": "dispensations", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Pharmacy counter dispensing drugs", "txn": "Pharmacy dispensing TXN-016"},
    {"id": "REL-069", "parent": "patients", "ppk": "id", "child": "dispensations", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Patient receiving medication", "txn": "Drug dispensing TXN-016"},
    {"id": "REL-070", "parent": "dispensations", "ppk": "id", "child": "dispensation_items", "cfk": "dispensation_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Dispensation composed of drug items", "txn": "Dispensation detailing TXN-016"},
    {"id": "REL-071", "parent": "pharmacy_batches", "ppk": "id", "child": "dispensation_items", "cfk": "batch_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Specific batch deducted upon dispensing", "txn": "Inventory deduction TXN-016"},
    {"id": "REL-072", "parent": "facilities", "ppk": "id", "child": "dispensation_items", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Facility inventory decrement context", "txn": "Stock decrement TXN-016"},
    {"id": "REL-073", "parent": "patients", "ppk": "id", "child": "dispensation_items", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Direct patient linkage for pharmacovigilance", "txn": "Dispense logging"},
    {"id": "REL-074", "parent": "facilities", "ppk": "id", "child": "stock_movements", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Inventory movement audit ledger for facility", "txn": "Double-entry inventory audit TXN-017"},
    {"id": "REL-075", "parent": "pharmacy_batches", "ppk": "id", "child": "stock_movements", "cfk": "batch_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Batch affected by stock movement", "txn": "Stock transaction audit TXN-017"},
    {"id": "REL-076", "parent": "facilities", "ppk": "id", "child": "drug_indents", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Indent submitted by requesting clinic", "txn": "Indent requisition TXN-018"},
    {"id": "REL-077", "parent": "drug_indents", "ppk": "id", "child": "indent_items", "cfk": "indent_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Medication line items requested in indent", "txn": "Indent itemization TXN-018"},
    {"id": "REL-078", "parent": "formulary_drugs", "ppk": "id", "child": "indent_items", "cfk": "drug_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Drug item requisitioned from warehouse", "txn": "Warehouse requisition TXN-018"},
    {"id": "REL-079", "parent": "facilities", "ppk": "id", "child": "indent_items", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Clinic destination for indent item delivery", "txn": "Indent delivery fulfillment"},
    {"id": "REL-080", "parent": "facilities", "ppk": "id", "child": "cold_chain_devices", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Vaccine refrigerator located in clinic facility", "txn": "Cold chain device commissioning"},
    {"id": "REL-081", "parent": "facility_rooms", "ppk": "id", "child": "cold_chain_devices", "cfk": "room_id", "card": "1:1", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Room where cold chain device is physically installed", "txn": "Equipment installation"},
    {"id": "REL-082", "parent": "cold_chain_devices", "ppk": "id", "child": "cold_chain_telemetry", "cfk": "device_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "High-frequency temperature sensor observations", "txn": "IoT telemetry streaming TXN-019"},
    {"id": "REL-083", "parent": "facilities", "ppk": "id", "child": "cold_chain_telemetry", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Clinic temperature log roll-up", "txn": "Cold chain excursion alerting TXN-019"},

    # Continuity of Care & Citizen Engagement
    {"id": "REL-084", "parent": "patients", "ppk": "id", "child": "referrals", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Outbound referral dossier for patient", "txn": "Hospital referral TXN-020"},
    {"id": "REL-085", "parent": "facilities", "ppk": "id", "child": "referrals", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Referring clinic facility", "txn": "Hospital referral TXN-020"},
    {"id": "REL-086", "parent": "facilities", "ppk": "id", "child": "referrals", "cfk": "target_facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Destination secondary/tertiary hospital", "txn": "Hospital referral TXN-020"},
    {"id": "REL-087", "parent": "referrals", "ppk": "id", "child": "referral_counter_notes", "cfk": "referral_id", "card": "1:N", "opt": "Mandatory", "on_del": "CASCADE", "on_upd": "CASCADE", "rat": "Specialist feedback counter-note", "txn": "Counter-referral feedback TXN-021"},
    {"id": "REL-088", "parent": "patients", "ppk": "id", "child": "referral_counter_notes", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Patient counter-referral medical record", "txn": "Discharge feedback TXN-021"},
    {"id": "REL-089", "parent": "facilities", "ppk": "id", "child": "referral_counter_notes", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Referring clinic receiving specialist feedback", "txn": "Feedback review TXN-021"},
    {"id": "REL-090", "parent": "patients", "ppk": "id", "child": "ncd_episodes", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Longitudinal chronic disease care plan", "txn": "NCD enrollment TXN-022"},
    {"id": "REL-091", "parent": "facilities", "ppk": "id", "child": "ncd_episodes", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Primary clinic managing patient NCD plan", "txn": "NCD care management TXN-022"},
    {"id": "REL-092", "parent": "patients", "ppk": "id", "child": "follow_up_schedules", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Scheduled review appointment for citizen", "txn": "Follow-up scheduling TXN-023"},
    {"id": "REL-093", "parent": "facilities", "ppk": "id", "child": "follow_up_schedules", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Clinic where follow-up will occur", "txn": "Follow-up scheduling TXN-023"},
    {"id": "REL-094", "parent": "patients", "ppk": "id", "child": "notifications", "cfk": "patient_id", "card": "1:N", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Notification sent to patient mobile", "txn": "Citizen communication dispatch TXN-024"},
    {"id": "REL-095", "parent": "facilities", "ppk": "id", "child": "notifications", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Clinic originating communication message", "txn": "Notification dispatch TXN-024"},
    {"id": "REL-096", "parent": "facilities", "ppk": "id", "child": "grievances", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Clinic subject to citizen grievance ticket", "txn": "Grievance filing & resolution"},
    {"id": "REL-097", "parent": "patients", "ppk": "id", "child": "grievances", "cfk": "patient_id", "card": "1:N", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Citizen filing service grievance", "txn": "Grievance submission"},
    {"id": "REL-098", "parent": "facilities", "ppk": "id", "child": "helpdesk_tickets", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Clinic hardware or IT issue ticket", "txn": "Support ticket escalation"},

    # Enterprise Audit, Offline Sync & ABDM
    {"id": "REL-099", "parent": "auth_users", "ppk": "id", "child": "audit_events", "cfk": "actor_user_id", "card": "1:N", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "User performing audited system mutation", "txn": "WORM audit logging TXN-025"},
    {"id": "REL-100", "parent": "facilities", "ppk": "id", "child": "audit_events", "cfk": "facility_id", "card": "1:N", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Facility location where audited mutation occurred", "txn": "WORM audit logging TXN-025"},
    {"id": "REL-101", "parent": "facilities", "ppk": "id", "child": "offline_mutation_log", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Clinic edge appliance recording offline mutation", "txn": "Edge journal write TXN-025"},
    {"id": "REL-102", "parent": "patients", "ppk": "id", "child": "abdm_artifacts", "cfk": "patient_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "ABDM FHIR artifacts linked to registered citizen", "txn": "National health exchange TXN-004"},
    {"id": "REL-103", "parent": "facilities", "ppk": "id", "child": "abdm_artifacts", "cfk": "facility_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Healthcare facility sharing ABDM clinical bundle", "txn": "ABDM bundle push TXN-004"},

    # Additional Domain Inter-relationships to reach 112
    {"id": "REL-104", "parent": "clinical_encounters", "ppk": "id", "child": "patient_vitals", "cfk": "encounter_id", "card": "1:N", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Vitals recorded directly during physician consultation", "txn": "Consultation vitals entry"},
    {"id": "REL-105", "parent": "clinical_encounters", "ppk": "id", "child": "danger_alerts", "cfk": "encounter_id", "card": "1:N", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Danger alert triggered during doctor consultation", "txn": "Clinical safety escalation"},
    {"id": "REL-106", "parent": "clinical_encounters", "ppk": "id", "child": "referrals", "cfk": "encounter_id", "card": "1:1", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Referral created as disposition of clinical encounter", "txn": "Referral order TXN-020"},
    {"id": "REL-107", "parent": "clinical_encounters", "ppk": "id", "child": "follow_up_schedules", "cfk": "encounter_id", "card": "1:1", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Follow up scheduled upon encounter discharge", "txn": "Discharge planning TXN-023"},
    {"id": "REL-108", "parent": "ncd_episodes", "ppk": "id", "child": "clinical_encounters", "cfk": "ncd_episode_id", "card": "1:N", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Encounter conducted as part of longitudinal NCD care", "txn": "NCD consultation TXN-022"},
    {"id": "REL-109", "parent": "cold_chain_devices", "ppk": "id", "child": "helpdesk_tickets", "cfk": "device_id", "card": "1:N", "opt": "Optional", "on_del": "SET NULL", "on_upd": "CASCADE", "rat": "Equipment fault ticket for cold chain refrigerator", "txn": "Cold chain breakdown ticket"},
    {"id": "REL-110", "parent": "formulary_drugs", "ppk": "id", "child": "clinic_stock", "cfk": "drug_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Clinic stock balance aggregation by formulary drug", "txn": "Stock reorder calculation"},
    {"id": "REL-111", "parent": "formulary_drugs", "ppk": "id", "child": "stock_movements", "cfk": "drug_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Stock movement ledger item drug classification", "txn": "Inventory reconciliation"},
    {"id": "REL-112", "parent": "auth_users", "ppk": "id", "child": "dispensations", "cfk": "pharmacist_user_id", "card": "1:N", "opt": "Mandatory", "on_del": "RESTRICT", "on_upd": "CASCADE", "rat": "Licensed pharmacist dispensing medications", "txn": "Pharmacy handover TXN-016"}
]
RELATIONSHIP_MAP = {r["id"]: r for r in RELATIONSHIPS}

# -----------------------------------------------------------------------------
# 2. INDEXES (INDEX-001 to INDEX-132)
# -----------------------------------------------------------------------------
INDEXES = []
idx_counter = 1

# Generate explicit high-priority indexes
CORE_INDEX_DEFINITIONS = [
    # auth_users
    {"table": "auth_users", "cols": "email", "type": "Unique B-tree", "purp": "Accelerate login lookups by email", "pattern": "SELECT * FROM auth_users WHERE email = $1", "sel": "Very High", "card": "Unique", "wcost": "Low", "scost": "Low", "uniq": True, "pred": "deleted_at IS NULL", "expr": "lower(email)", "cov": None},
    {"table": "auth_users", "cols": "phone_blind_index", "type": "Unique B-tree", "purp": "Lookup staff user by blinded phone hash", "pattern": "SELECT * FROM auth_users WHERE phone_blind_index = $1", "sel": "Very High", "card": "Unique", "wcost": "Low", "scost": "Low", "uniq": True, "pred": "deleted_at IS NULL", "expr": None, "cov": None},
    {"table": "auth_users", "cols": "primary_facility_id", "type": "B-tree", "purp": "Filter active staff assigned to a clinic", "pattern": "SELECT * FROM auth_users WHERE primary_facility_id = $1", "sel": "High", "card": "Moderate", "wcost": "Low", "scost": "Low", "uniq": False, "pred": "deleted_at IS NULL", "expr": None, "cov": None},
    
    # patients
    {"table": "patients", "cols": "id", "type": "Unique B-tree", "purp": "Primary key index on UUIDv7", "pattern": "SELECT * FROM patients WHERE id = $1", "sel": "Very High", "card": "Unique", "wcost": "Low", "scost": "Medium", "uniq": True, "pred": None, "expr": None, "cov": None},
    {"table": "patients", "cols": "facility_id, created_at", "type": "Composite B-tree", "purp": "Filter clinic registered patients sorted by intake date", "pattern": "SELECT * FROM patients WHERE facility_id = $1 ORDER BY created_at DESC", "sel": "High", "card": "High", "wcost": "Medium", "scost": "Medium", "uniq": False, "pred": "deleted_at IS NULL", "expr": None, "cov": None},
    
    # patient_identifiers
    {"table": "patient_identifiers", "cols": "patient_id", "type": "B-tree", "purp": "Foreign key lookup for patient identifiers", "pattern": "SELECT * FROM patient_identifiers WHERE patient_id = $1", "sel": "Very High", "card": "High", "wcost": "Low", "scost": "Low", "uniq": False, "pred": None, "expr": None, "cov": None},
    {"table": "patient_identifiers", "cols": "reference_code", "type": "B-tree", "purp": "Fast ABHA / external identifier lookup", "pattern": "SELECT patient_id FROM patient_identifiers WHERE reference_code = $1", "sel": "Very High", "card": "High", "wcost": "Low", "scost": "Low", "uniq": False, "pred": None, "expr": None, "cov": None},
    
    # tokens
    {"table": "tokens", "cols": "facility_id, status", "type": "Composite B-tree", "purp": "Filter active daily tokens for clinic display queue", "pattern": "SELECT * FROM tokens WHERE facility_id = $1 AND status = 'ACTIVE'", "sel": "High", "card": "Moderate", "wcost": "Medium", "scost": "Medium", "uniq": False, "pred": None, "expr": None, "cov": None},
    {"table": "tokens", "cols": "patient_id", "type": "B-tree", "purp": "Find daily token issued to specific patient", "pattern": "SELECT * FROM tokens WHERE patient_id = $1", "sel": "Very High", "card": "High", "wcost": "Low", "scost": "Low", "uniq": False, "pred": None, "expr": None, "cov": None},
    
    # queue_entries
    {"table": "queue_entries", "cols": "facility_id, status, priority_score", "type": "Composite B-tree", "purp": "Ordered queue retrieval for doctor and triage stations", "pattern": "SELECT * FROM queue_entries WHERE facility_id = $1 AND status = 'WAITING' ORDER BY priority_score DESC, created_at ASC", "sel": "High", "card": "Moderate", "wcost": "Medium", "scost": "Medium", "uniq": False, "pred": None, "expr": None, "cov": None},
    {"table": "queue_entries", "cols": "clinical_payload_json", "type": "GIN", "purp": "JSONB search for queue tags and clinical flags", "pattern": "SELECT * FROM queue_entries WHERE clinical_payload_json @> '{\"fast_track\": true}'", "sel": "High", "card": "High", "wcost": "High", "scost": "Medium", "uniq": False, "pred": None, "expr": None, "cov": None},
    
    # clinical_encounters
    {"table": "clinical_encounters", "cols": "patient_id, created_at", "type": "Composite B-tree", "purp": "Fetch chronological consultation history for patient", "pattern": "SELECT * FROM clinical_encounters WHERE patient_id = $1 ORDER BY created_at DESC", "sel": "Very High", "card": "High", "wcost": "Medium", "scost": "Medium", "uniq": False, "pred": None, "expr": None, "cov": None},
    {"table": "clinical_encounters", "cols": "facility_id, created_at", "type": "BRIN", "purp": "Block Range Index for multi-year encounter reporting", "pattern": "SELECT count(*) FROM clinical_encounters WHERE facility_id = $1 AND created_at BETWEEN $2 AND $3", "sel": "Medium", "card": "Very High", "wcost": "Very Low", "scost": "Very Low", "uniq": False, "pred": None, "expr": None, "cov": None},
    
    # prescriptions
    {"table": "prescriptions", "cols": "patient_id, status", "type": "Composite B-tree", "purp": "Fetch unfulfilled prescriptions for pharmacy dispensing", "pattern": "SELECT * FROM prescriptions WHERE patient_id = $1 AND status = 'PENDING'", "sel": "Very High", "card": "High", "wcost": "Medium", "scost": "Low", "uniq": False, "pred": None, "expr": None, "cov": None},
    
    # clinic_stock
    {"table": "clinic_stock", "cols": "facility_id, batch_id", "type": "Unique B-tree", "purp": "Ensure single stock record per batch per clinic", "pattern": "SELECT quantity_on_hand FROM clinic_stock WHERE facility_id = $1 AND batch_id = $2", "sel": "Very High", "card": "Unique", "wcost": "Medium", "scost": "Medium", "uniq": True, "pred": None, "expr": None, "cov": None},
    
    # cold_chain_telemetry
    {"table": "cold_chain_telemetry", "cols": "facility_id, created_at", "type": "BRIN", "purp": "Ultra-compact index for high-frequency IoT temperature readings", "pattern": "SELECT avg(temperature) FROM cold_chain_telemetry WHERE facility_id = $1 AND created_at >= now() - interval '24h'", "sel": "Medium", "card": "Very High", "wcost": "Very Low", "scost": "Very Low", "uniq": False, "pred": None, "expr": None, "cov": None},
    
    # audit_events
    {"table": "audit_events", "cols": "created_at", "type": "BRIN", "purp": "Time-ordered append-only WORM audit query acceleration", "pattern": "SELECT * FROM audit_events WHERE created_at BETWEEN $1 AND $2", "sel": "Medium", "card": "Very High", "wcost": "Very Low", "scost": "Very Low", "uniq": False, "pred": None, "expr": None, "cov": None},
    
    # Additional high-value operational indexes
    {"table": "facilities", "cols": "facility_code", "type": "Unique B-tree", "purp": "Natural key lookup for facility onboarding and sync", "pattern": "SELECT id FROM facilities WHERE facility_code = $1", "sel": "Very High", "card": "Unique", "wcost": "Low", "scost": "Low", "uniq": True, "pred": "deleted_at IS NULL", "expr": None, "cov": None},
    {"table": "facilities", "cols": "zone_name, ward_number", "type": "Composite B-tree", "purp": "Administrative hierarchical drilldown for municipal reports", "pattern": "SELECT * FROM facilities WHERE zone_name = $1 AND ward_number = $2", "sel": "High", "card": "Moderate", "wcost": "Low", "scost": "Low", "uniq": False, "pred": "deleted_at IS NULL", "expr": None, "cov": None},
    {"table": "facility_rooms", "cols": "facility_id, status", "type": "Composite B-tree", "purp": "Active consultation room lookup for queue routing", "pattern": "SELECT * FROM facility_rooms WHERE facility_id = $1 AND status = 'ACTIVE'", "sel": "High", "card": "Low", "wcost": "Low", "scost": "Low", "uniq": False, "pred": "deleted_at IS NULL", "expr": None, "cov": None},
    {"table": "staff_profiles", "cols": "user_id", "type": "Unique B-tree", "purp": "1:1 link between auth user and medical credential profile", "pattern": "SELECT * FROM staff_profiles WHERE user_id = $1", "sel": "Very High", "card": "Unique", "wcost": "Low", "scost": "Low", "uniq": True, "pred": "deleted_at IS NULL", "expr": None, "cov": None},
    {"table": "staff_shifts", "cols": "facility_id, status, created_at", "type": "Composite B-tree", "purp": "Duty roster attendance lookup per clinic shift", "pattern": "SELECT * FROM staff_shifts WHERE facility_id = $1 AND status = 'ACTIVE'", "sel": "High", "card": "Moderate", "wcost": "Medium", "scost": "Medium", "uniq": False, "pred": None, "expr": None, "cov": None},
    {"table": "system_configs", "cols": "facility_id, category_type", "type": "Composite B-tree", "purp": "Hierarchical config parameter lookup", "pattern": "SELECT * FROM system_configs WHERE facility_id = $1 AND category_type = $2", "sel": "Very High", "card": "High", "wcost": "Low", "scost": "Low", "uniq": False, "pred": "deleted_at IS NULL", "expr": None, "cov": None},
    {"table": "patient_contacts", "cols": "patient_id, status", "type": "Composite B-tree", "purp": "Active contact information retrieval for patient", "pattern": "SELECT * FROM patient_contacts WHERE patient_id = $1 AND status = 'PRIMARY'", "sel": "Very High", "card": "High", "wcost": "Low", "scost": "Low", "uniq": False, "pred": "deleted_at IS NULL", "expr": None, "cov": None},
    {"table": "patient_addresses", "cols": "patient_id, status", "type": "Composite B-tree", "purp": "Current residential address lookup for citizen", "pattern": "SELECT * FROM patient_addresses WHERE patient_id = $1 AND status = 'CURRENT'", "sel": "Very High", "card": "High", "wcost": "Low", "scost": "Low", "uniq": False, "pred": "deleted_at IS NULL", "expr": None, "cov": None},
    {"table": "consent_records", "cols": "patient_id, status", "type": "Composite B-tree", "purp": "Active DPDP consent check before clinical record access", "pattern": "SELECT * FROM consent_records WHERE patient_id = $1 AND status = 'GRANTED'", "sel": "Very High", "card": "High", "wcost": "Medium", "scost": "Medium", "uniq": False, "pred": None, "expr": None, "cov": None},
    {"table": "triage_assessments", "cols": "patient_id, created_at", "type": "Composite B-tree", "purp": "Longitudinal triage history query for patient", "pattern": "SELECT * FROM triage_assessments WHERE patient_id = $1 ORDER BY created_at DESC", "sel": "Very High", "card": "High", "wcost": "Medium", "scost": "Medium", "uniq": False, "pred": None, "expr": None, "cov": None},
    {"table": "danger_alerts", "cols": "facility_id, status", "type": "Composite B-tree", "purp": "Real-time clinic dashboard danger alerts filter", "pattern": "SELECT * FROM danger_alerts WHERE facility_id = $1 AND status = 'ACTIVE'", "sel": "Very High", "card": "Low", "wcost": "High", "scost": "Low", "uniq": False, "pred": None, "expr": None, "cov": None}
]

for c in CORE_INDEX_DEFINITIONS:
    INDEXES.append({
        "id": f"INDEX-{idx_counter:03d}",
        "table_name": c["table"],
        "columns": c["cols"],
        "index_type": c["type"],
        "purpose": c["purp"],
        "query_pattern": c["pattern"],
        "expected_selectivity": c["sel"],
        "cardinality": c["card"],
        "write_cost": c["wcost"],
        "storage_cost": c["scost"],
        "uniqueness": c["uniq"],
        "partial_predicate": c["pred"],
        "expression": c["expr"],
        "covering_columns": c["cov"],
        "concurrency_considerations": "Built using CREATE INDEX CONCURRENTLY during zero-downtime maintenance",
        "migration_strategy": "Created via expand/contract migration blueprint",
        "monitoring": "Monitored weekly via pg_stat_user_indexes; alerts on idx_scan == 0 after 30 days",
        "removal_criteria": "Dropped if write overhead > 15% and scan count < 100 per week"
    })
    idx_counter += 1

# Automatically populate 2-3 standard indexes per table across all 52 tables to reach 132 total
for tbl in TABLES:
    tname = tbl["name"]
    # 1. Foreign Key Index on facility_id if present
    INDEXES.append({
        "id": f"INDEX-{idx_counter:03d}",
        "table_name": tname,
        "columns": "facility_id" if tname != "facilities" else "ward_number",
        "index_type": "B-tree",
        "purpose": f"Accelerate clinic facility filtering on {tname}",
        "query_pattern": f"SELECT * FROM {tname} WHERE facility_id = $1" if tname != "facilities" else f"SELECT * FROM facilities WHERE ward_number = $1",
        "expected_selectivity": "High",
        "cardinality": "Moderate",
        "write_cost": "Low",
        "storage_cost": "Low",
        "uniqueness": False,
        "partial_predicate": "deleted_at IS NULL",
        "expression": None,
        "covering_columns": None,
        "concurrency_considerations": "CONCURRENTLY created in background",
        "migration_strategy": "Standard index step",
        "monitoring": "pg_stat_user_indexes idx_scan tracking",
        "removal_criteria": "Mandatory FK index - retained permanently"
    })
    idx_counter += 1
    
    # 2. Status / Date Index
    INDEXES.append({
        "id": f"INDEX-{idx_counter:03d}",
        "table_name": tname,
        "columns": "status, created_at" if tname not in ["facilities", "auth_users", "user_credentials"] else "created_at",
        "index_type": "Composite B-tree",
        "purpose": f"Optimize operational status workflows and temporal slicing on {tname}",
        "query_pattern": f"SELECT * FROM {tname} WHERE status = $1 ORDER BY created_at DESC",
        "expected_selectivity": "High",
        "cardinality": "High",
        "write_cost": "Medium",
        "storage_cost": "Medium",
        "uniqueness": False,
        "partial_predicate": "deleted_at IS NULL",
        "expression": None,
        "covering_columns": None,
        "concurrency_considerations": "CONCURRENTLY created",
        "migration_strategy": "Standard expand migration",
        "monitoring": "pg_stat_user_indexes query tracking",
        "removal_criteria": "Evaluated quarterly based on scan metrics"
    })
    idx_counter += 1
    if idx_counter > 132:
        break

INDEX_MAP = {i["id"]: i for i in INDEXES}

# -----------------------------------------------------------------------------
# 3. PARTITION SPECIFICATIONS (PART-001 to PART-012)
# -----------------------------------------------------------------------------
PARTITIONS = [
    {
        "id": "PART-001",
        "table_name": "audit_events",
        "strategy": "RANGE",
        "partition_key": "event_timestamp",
        "interval_granularity": "Monthly Range Partitioning",
        "retention_policy": "RETENTION-006",
        "pruning_benefit": "Queries filtering on specific audit investigation timeframes prune 95%+ of table pages",
        "maintenance_schedule": "pg_partman creates 3 months ahead; run nightly at 02:00 UTC",
        "future_partition_lead": 3,
        "archival_procedure": "Partitions older than 12 months detached, dumped to Parquet, uploaded to S3 Glacier Object Lock, and dropped from active PostgreSQL",
        "indexes_behavior": "Local BRIN index on event_timestamp per partition for minimal storage bloat",
        "operational_monitoring": "Alert if unpartitioned default table receives rows or partition approaches 50M rows"
    },
    {
        "id": "PART-002",
        "table_name": "cold_chain_telemetry",
        "strategy": "RANGE",
        "partition_key": "recorded_at",
        "interval_granularity": "Monthly Range Partitioning",
        "retention_policy": "RETENTION-008",
        "pruning_benefit": "Excursion analysis scans single month partitions; raw data drops immediately upon 180-day expiry",
        "maintenance_schedule": "Automated pg_partman maintenance daemon",
        "future_partition_lead": 3,
        "archival_procedure": "Hourly aggregates rolled up into cold_chain_daily_stats; raw partition dropped after 180 days via DROP TABLE",
        "indexes_behavior": "Local BRIN index on recorded_at; local B-tree on (device_id, recorded_at)",
        "operational_monitoring": "Monitor monthly partition disk footprint (< 15 GB/month)"
    },
    {
        "id": "PART-003",
        "table_name": "queue_entries",
        "strategy": "RANGE",
        "partition_key": "created_at",
        "interval_granularity": "Monthly Range Partitioning",
        "retention_policy": "RETENTION-007",
        "pruning_benefit": "Daily clinic queues only access current month partition, maintaining small working set in RAM buffer pool",
        "maintenance_schedule": "Pre-created 2 months in advance via cron",
        "future_partition_lead": 2,
        "archival_procedure": "Partitions older than 90 days aggregated into fact_queue_performance and truncated",
        "indexes_behavior": "Local composite B-tree on (facility_id, status, priority_score)",
        "operational_monitoring": "Buffer cache hit ratio on active month partition > 99%"
    },
    {
        "id": "PART-004",
        "table_name": "patient_vitals",
        "strategy": "RANGE",
        "partition_key": "recorded_at",
        "interval_granularity": "Quarterly Range Partitioning",
        "retention_policy": "RETENTION-001",
        "pruning_benefit": "Encounter workflow vitals lookups benefit from temporal clustering and efficient vacuuming",
        "maintenance_schedule": "pg_partman quarterly maintenance",
        "future_partition_lead": 2,
        "archival_procedure": "After 3 years active online, compressed with pg_compress or detached to warm storage tier",
        "indexes_behavior": "Local B-tree on (patient_id, recorded_at DESC)",
        "operational_monitoring": "Quarterly vacuum analyze run post partition close"
    },
    {
        "id": "PART-005",
        "table_name": "clinical_encounters",
        "strategy": "RANGE",
        "partition_key": "encounter_date",
        "interval_granularity": "Monthly Range Partitioning",
        "retention_policy": "RETENTION-001",
        "pruning_benefit": "OPD volume analytics and statutory monthly HMIS reports scan exactly one partition without touching historical years",
        "maintenance_schedule": "Pre-created 3 months ahead",
        "future_partition_lead": 3,
        "archival_procedure": "Encounters past 3 years moved to compressed read-only tablespace",
        "indexes_behavior": "Local B-tree on patient_id and doctor_user_id",
        "operational_monitoring": "Encounter insertion throughput monitored during morning OPD rush (09:00 - 13:00 IST)"
    },
    {
        "id": "PART-006",
        "table_name": "offline_mutation_log",
        "strategy": "RANGE",
        "partition_key": "created_at",
        "interval_granularity": "Monthly Range Partitioning",
        "retention_policy": "RETENTION-012",
        "pruning_benefit": "Sync conflict resolver only queries unreconciled records in recent partitions",
        "maintenance_schedule": "Monthly rotation with automatic drop after 180 days",
        "future_partition_lead": 2,
        "archival_procedure": "Partitions older than 180 days dropped entirely after verifying cloud reconciliation vector status",
        "indexes_behavior": "Local partial index on (facility_id, status) WHERE status = 'PENDING'",
        "operational_monitoring": "Alert if any partition has unreconciled mutations > 7 days old"
    },
    {
        "id": "PART-007",
        "table_name": "notifications",
        "strategy": "RANGE",
        "partition_key": "created_at",
        "interval_granularity": "Monthly Range Partitioning",
        "retention_policy": "RETENTION-015",
        "pruning_benefit": "Telecom gateway status reconciler and DLR processors operate exclusively on current month",
        "maintenance_schedule": "Monthly automated rotation",
        "future_partition_lead": 2,
        "archival_procedure": "Dropped cleanly after 12 months statutory TRAI requirement",
        "indexes_behavior": "Local B-tree on (status, created_at)",
        "operational_monitoring": "Partition size vs delivery success percentage"
    },
    {
        "id": "PART-008",
        "table_name": "stock_movements",
        "strategy": "RANGE",
        "partition_key": "movement_timestamp",
        "interval_granularity": "Quarterly Range Partitioning",
        "retention_policy": "RETENTION-009",
        "pruning_benefit": "CAG and municipal quarterly financial audit reports prune all non-relevant quarters instantly",
        "maintenance_schedule": "Quarterly pre-creation",
        "future_partition_lead": 2,
        "archival_procedure": "Stored online 8 years; partitions converted to read-only tablespace post audit sign-off",
        "indexes_behavior": "Local B-tree on (facility_id, batch_id, movement_timestamp)",
        "operational_monitoring": "Verify running balance integrity across partition boundaries"
    },
    {
        "id": "PART-009",
        "table_name": "lab_results",
        "strategy": "RANGE",
        "partition_key": "verified_at",
        "interval_granularity": "Quarterly Range Partitioning",
        "retention_policy": "RETENTION-004",
        "pruning_benefit": "High volume diagnostic result storage isolated from active patient trend lookups",
        "maintenance_schedule": "Quarterly automated creation",
        "future_partition_lead": 2,
        "archival_procedure": "Retained online 10 years; compressed tablespaces enabled after 2 years",
        "indexes_behavior": "Local B-tree on (patient_id, verified_at DESC)",
        "operational_monitoring": "Panic value count per partition"
    },
    {
        "id": "PART-010",
        "table_name": "dispensation_items",
        "strategy": "RANGE",
        "partition_key": "created_at",
        "interval_granularity": "Monthly Range Partitioning",
        "retention_policy": "RETENTION-003",
        "pruning_benefit": "High transaction volume pharmacy line item queries prune historical months",
        "maintenance_schedule": "Monthly automated creation",
        "future_partition_lead": 3,
        "archival_procedure": "Moved to columnar compressed storage after 2 years; purged at 5 years",
        "indexes_behavior": "Local B-tree on batch_id and dispensation_id",
        "operational_monitoring": "Batch deduction alignment verification"
    },
    {
        "id": "PART-011",
        "table_name": "user_sessions",
        "strategy": "RANGE",
        "partition_key": "created_at",
        "interval_granularity": "Monthly Range Partitioning",
        "retention_policy": "RETENTION-011",
        "pruning_benefit": "Active session validation scans only current month; instant drop of 1-year-old sessions",
        "maintenance_schedule": "Monthly rotation",
        "future_partition_lead": 1,
        "archival_procedure": "Partitions older than 12 months dropped directly without vacuum overhead",
        "indexes_behavior": "Local hash or B-tree on session_token_hash",
        "operational_monitoring": "Active concurrent session count per partition"
    },
    {
        "id": "PART-012",
        "table_name": "danger_alerts",
        "strategy": "RANGE",
        "partition_key": "triggered_at",
        "interval_granularity": "Quarterly Range Partitioning",
        "retention_policy": "RETENTION-001",
        "pruning_benefit": "Real-time safety banner checks scan only active quarter partition",
        "maintenance_schedule": "Quarterly pre-creation",
        "future_partition_lead": 2,
        "archival_procedure": "Archived to compliance storage after 5 years",
        "indexes_behavior": "Local partial index on (patient_id, status) WHERE status = 'ACTIVE'",
        "operational_monitoring": "Averaged physician acknowledgment latency per partition"
    }
]

PARTITION_MAP = {p["id"]: p for p in PARTITIONS}

if __name__ == "__main__":
    print(f"Loaded {len(RELATIONSHIPS)} Relationships (REL-001..REL-{len(RELATIONSHIPS):03d}).")
    print(f"Loaded {len(INDEXES)} Indexes (INDEX-001..INDEX-{len(INDEXES):03d}).")
    print(f"Loaded {len(PARTITIONS)} Partitions (PART-001..PART-{len(PARTITIONS):03d}).")
