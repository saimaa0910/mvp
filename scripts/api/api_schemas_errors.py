"""
api_schemas_errors.py
Canonical Schema Registry and Enterprise Error Catalog for Phase 08 API Engineering.
Contains 65+ formal JSON:API/OpenAPI Schemas and 115+ Standardized Error Definitions.
"""

from typing import Dict, List, Any

# -----------------------------------------------------------------------------
# 1. 65+ API REQUEST & RESPONSE SCHEMAS (SCHEMA-API-001 to SCHEMA-API-068)
# -----------------------------------------------------------------------------
API_SCHEMAS = [
    # Common & Envelope Schemas
    {
        "id": "SCHEMA-API-001",
        "name": "StandardApiResponseEnvelope",
        "category": "Common",
        "description": "Top-level JSON envelope wrapping all successful single-resource REST API responses.",
        "fields": [
            {"name": "data", "type": "object", "required": True, "nullable": False, "description": "Primary payload object containing resource attributes and relationships."},
            {"name": "meta", "type": "object", "required": True, "nullable": False, "description": "Request execution metadata including timestamp, correlation ID, and server node."},
            {"name": "links", "type": "object", "required": False, "nullable": True, "description": "HATEOAS navigational links (self, related)."}
        ]
    },
    {
        "id": "SCHEMA-API-002",
        "name": "StandardCollectionEnvelope",
        "category": "Common",
        "description": "Top-level JSON envelope wrapping paginated collection responses.",
        "fields": [
            {"name": "data", "type": "array", "required": True, "nullable": False, "description": "Array of resource objects matching query filters."},
            {"name": "pagination", "type": "object", "required": True, "nullable": False, "description": "Cursor-based pagination metadata (cursor, next_cursor, has_more, limit, total_count)."},
            {"name": "meta", "type": "object", "required": True, "nullable": False, "description": "Execution metadata including query duration, filter counts, and correlation ID."},
            {"name": "links", "type": "object", "required": True, "nullable": False, "description": "Navigational links (self, next, prev, first)."}
        ]
    },
    {
        "id": "SCHEMA-API-003",
        "name": "StandardErrorEnvelope",
        "category": "Common",
        "description": "Authoritative RFC 7807 and GBA compliant structured error payload for all HTTP 4xx/5xx responses.",
        "fields": [
            {"name": "error", "type": "object", "required": True, "nullable": False, "description": "Root error container object."},
            {"name": "error.code", "type": "string", "required": True, "nullable": False, "description": "Machine-readable standardized error code (e.g., ERR-AUTH-001)."},
            {"name": "error.message", "type": "string", "required": True, "nullable": False, "description": "Safe, localized human-readable error summary for end-user display."},
            {"name": "error.category", "type": "string", "required": True, "nullable": False, "description": "Categorical domain of failure (Authentication, Validation, ClinicalSafety, etc.)."},
            {"name": "error.correlation_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 distributed trace identifier matching X-Correlation-ID header."},
            {"name": "error.timestamp", "type": "string", "required": True, "nullable": False, "description": "ISO-8601 UTC timestamp of error generation."},
            {"name": "error.retryable", "type": "boolean", "required": True, "nullable": False, "description": "Boolean flag indicating whether client may safely retry operation."},
            {"name": "error.details", "type": "array", "required": False, "nullable": True, "description": "Array of field-level validation errors or sub-exception descriptors."}
        ]
    },
    {
        "id": "SCHEMA-API-004",
        "name": "ValidationErrorItem",
        "category": "Common",
        "description": "Field-specific validation failure item embedded in error details.",
        "fields": [
            {"name": "field", "type": "string", "required": True, "nullable": False, "description": "JSON pointer or dotted path to invalid attribute (e.g., data.attributes.phone_number)."},
            {"name": "rule", "type": "string", "required": True, "nullable": False, "description": "Validation rule violated (e.g., pattern_mismatch, value_out_of_range, required_missing)."},
            {"name": "rejected_value", "type": "any", "required": False, "nullable": True, "description": "Sanitized rejected input value (redacted if PII/password)."},
            {"name": "message", "type": "string", "required": True, "nullable": False, "description": "Human-readable diagnostic guidance for correcting the field."}
        ]
    },
    {
        "id": "SCHEMA-API-005",
        "name": "CursorPaginationMetadata",
        "category": "Common",
        "description": "Standardized pagination cursor and navigation metadata.",
        "fields": [
            {"name": "cursor", "type": "string", "required": True, "nullable": False, "description": "Base64-encoded opaque cursor referencing current page boundary."},
            {"name": "next_cursor", "type": "string", "required": False, "nullable": True, "description": "Opaque cursor for retrieving succeeding page (null if last page)."},
            {"name": "prev_cursor", "type": "string", "required": False, "nullable": True, "description": "Opaque cursor for retrieving preceding page (null if first page)."},
            {"name": "has_more", "type": "boolean", "required": True, "nullable": False, "description": "Indicator of whether additional records exist beyond current page."},
            {"name": "limit", "type": "integer", "required": True, "nullable": False, "description": "Maximum page size requested or clamped by rate-limit policy (1..100)."},
            {"name": "total_count", "type": "integer", "required": False, "nullable": True, "description": "Optional total count where query plan allows fast index estimation."}
        ]
    },

    # Auth & IAM Schemas
    {
        "id": "SCHEMA-API-006",
        "name": "LoginRequest",
        "category": "Auth",
        "description": "Staff login payload submitting username, password, and facility scope.",
        "fields": [
            {"name": "username", "type": "string", "required": True, "nullable": False, "description": "Staff municipal employee ID or authorized email address."},
            {"name": "password", "type": "string", "required": True, "nullable": False, "description": "Cleartext password (transmitted strictly over TLS 1.3; verified against Argon2id hash)."},
            {"name": "facility_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 identifying Namma Clinic facility where shift is being initiated."},
            {"name": "device_fingerprint", "type": "string", "required": True, "nullable": False, "description": "Cryptographic hardware signature of registered clinic workstation tablet."},
            {"name": "mfa_otp", "type": "string", "required": False, "nullable": True, "description": "6-digit TOTP token if MFA is enabled for role."}
        ]
    },
    {
        "id": "SCHEMA-API-007",
        "name": "AuthTokenResponse",
        "category": "Auth",
        "description": "Authentication success response returning access and refresh tokens.",
        "fields": [
            {"name": "access_token", "type": "string", "required": True, "nullable": False, "description": "RS256-signed JWT access token with 15-minute lifespan."},
            {"name": "token_type", "type": "string", "required": True, "nullable": False, "description": "Fixed string 'Bearer'."},
            {"name": "expires_in", "type": "integer", "required": True, "nullable": False, "description": "Lifespan of access token in seconds (900 seconds)."},
            {"name": "refresh_token", "type": "string", "required": True, "nullable": False, "description": "Opaque high-entropy cryptographically random refresh token (8-hour sliding window)."},
            {"name": "session_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 primary key in user_sessions table."},
            {"name": "user", "type": "object", "required": True, "nullable": False, "description": "Staff identity profile object (id, full_name, role_code, facility_id)."}
        ]
    },
    {
        "id": "SCHEMA-API-008",
        "name": "TokenRefreshRequest",
        "category": "Auth",
        "description": "Token rotation payload presenting active refresh token.",
        "fields": [
            {"name": "refresh_token", "type": "string", "required": True, "nullable": False, "description": "Current refresh token issued during login or last rotation."},
            {"name": "session_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 session identifier being refreshed."}
        ]
    },
    {
        "id": "SCHEMA-API-009",
        "name": "StaffSessionProfile",
        "category": "Auth",
        "description": "Current authenticated staff profile and permissions context.",
        "fields": [
            {"name": "user_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 staff identifier."},
            {"name": "username", "type": "string", "required": True, "nullable": False, "description": "Staff municipal employee ID."},
            {"name": "full_name", "type": "string", "required": True, "nullable": False, "description": "Display name of staff member."},
            {"name": "roles", "type": "array", "required": True, "nullable": False, "description": "List of active role codes assigned to user."},
            {"name": "permissions", "type": "array", "required": True, "nullable": False, "description": "List of fine-grained permission tokens granted across active roles."},
            {"name": "facility_context", "type": "object", "required": True, "nullable": False, "description": "Active clinic facility metadata (id, name, zone, ward)."},
            {"name": "shift_id", "type": "string", "required": False, "nullable": True, "description": "Active shift identifier if clocked in."}
        ]
    },
    {
        "id": "SCHEMA-API-010",
        "name": "PasswordChangeRequest",
        "category": "Auth",
        "description": "Self-service password update payload.",
        "fields": [
            {"name": "current_password", "type": "string", "required": True, "nullable": False, "description": "Existing staff password."},
            {"name": "new_password", "type": "string", "required": True, "nullable": False, "description": "New password conforming to 12+ char complexity rules."},
            {"name": "confirm_password", "type": "string", "required": True, "nullable": False, "description": "Verification repetition of new password."}
        ]
    },

    # Patient Schemas
    {
        "id": "SCHEMA-API-011",
        "name": "PatientRegistrationRequest",
        "category": "Patient",
        "description": "Citizen demographic intake payload for registering new patients at front desk.",
        "fields": [
            {"name": "first_name", "type": "string", "required": True, "nullable": False, "description": "Given legal name of citizen."},
            {"name": "last_name", "type": "string", "required": False, "nullable": True, "description": "Family name or surname."},
            {"name": "gender", "type": "string", "required": True, "nullable": False, "description": "Biological sex/gender (MALE, FEMALE, TRANSGENDER, OTHER)."},
            {"name": "date_of_birth", "type": "string", "required": False, "nullable": True, "description": "ISO-8601 date of birth (YYYY-MM-DD)."},
            {"name": "estimated_age_years", "type": "integer", "required": False, "nullable": True, "description": "Estimated age if birth date unknown."},
            {"name": "primary_phone", "type": "string", "required": True, "nullable": False, "description": "10-digit Indian mobile number (+91 assumed)."},
            {"name": "abha_number", "type": "string", "required": False, "nullable": True, "description": "14-digit Ayushman Bharat Health Account number (XX-XXXX-XXXX-XXXX)."},
            {"name": "abha_address", "type": "string", "required": False, "nullable": True, "description": "ABHA virtual address handle (citizen@abdm)."},
            {"name": "aadhaar_vault_ref", "type": "string", "required": False, "nullable": True, "description": "Tokenized reference from secure Aadhaar Data Vault."},
            {"name": "address_line1", "type": "string", "required": True, "nullable": False, "description": "Street address or landmark."},
            {"name": "bbmp_ward_number", "type": "integer", "required": True, "nullable": False, "description": "BBMP ward number (1..243)."},
            {"name": "postal_pincode", "type": "string", "required": True, "nullable": False, "description": "6-digit postal code (560001..560110)."},
            {"name": "emergency_contact_name", "type": "string", "required": False, "nullable": True, "description": "Next of kin or guardian name."},
            {"name": "emergency_contact_phone", "type": "string", "required": False, "nullable": True, "description": "Next of kin phone number."}
        ]
    },
    {
        "id": "SCHEMA-API-012",
        "name": "PatientProfileResponse",
        "category": "Patient",
        "description": "Full citizen demographic and clinical continuity summary.",
        "fields": [
            {"name": "id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 citizen identifier."},
            {"name": "uhid", "type": "string", "required": True, "nullable": False, "description": "Municipal Unique Health Identifier (NC-BLR-YYYY-XXXXXXXX)."},
            {"name": "first_name", "type": "string", "required": True, "nullable": False, "description": "Citizen first name."},
            {"name": "last_name", "type": "string", "required": False, "nullable": True, "description": "Citizen last name."},
            {"name": "gender", "type": "string", "required": True, "nullable": False, "description": "Citizen gender."},
            {"name": "date_of_birth", "type": "string", "required": True, "nullable": False, "description": "Date of birth."},
            {"name": "primary_phone", "type": "string", "required": True, "nullable": False, "description": "Masked mobile number (XXXXXX1234 on non-admin UI)."},
            {"name": "abha_linked", "type": "boolean", "required": True, "nullable": False, "description": "Boolean flag indicating verified ABHA linkage."},
            {"name": "registered_clinic_id", "type": "string", "required": True, "nullable": False, "description": "Originating clinic facility ID."},
            {"name": "created_at", "type": "string", "required": True, "nullable": False, "description": "Registration timestamp."}
        ]
    },
    {
        "id": "SCHEMA-API-013",
        "name": "PatientSearchQuery",
        "category": "Patient",
        "description": "Multi-parameter phonetic and index query payload for patient lookup.",
        "fields": [
            {"name": "query", "type": "string", "required": False, "nullable": True, "description": "Free text name or UHID search string."},
            {"name": "phone", "type": "string", "required": False, "nullable": True, "description": "Exact mobile number match."},
            {"name": "uhid", "type": "string", "required": False, "nullable": True, "description": "Exact UHID match."},
            {"name": "abha_number", "type": "string", "required": False, "nullable": True, "description": "Exact ABHA number match."},
            {"name": "ward_number", "type": "integer", "required": False, "nullable": True, "description": "Filter by BBMP ward number."}
        ]
    },
    {
        "id": "SCHEMA-API-014",
        "name": "PatientDuplicateMatch",
        "category": "Patient",
        "description": "Duplicate candidate record identified by fuzzy phonetic and demographic matching.",
        "fields": [
            {"name": "patient_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 of candidate patient."},
            {"name": "uhid", "type": "string", "required": True, "nullable": False, "description": "Candidate UHID."},
            {"name": "match_score", "type": "number", "required": True, "nullable": False, "description": "Deterministic confidence score (0.0 to 1.0) computed via Jaro-Winkler and Soundex."},
            {"name": "matching_attributes", "type": "array", "required": True, "nullable": False, "description": "List of colliding fields (phone, name_phonetic, dob, address)."}
        ]
    },
    {
        "id": "SCHEMA-API-015",
        "name": "PatientMergeRequest",
        "category": "Patient",
        "description": "Supervisory command payload merging duplicate patient records.",
        "fields": [
            {"name": "surviving_patient_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 of primary record being retained."},
            {"name": "subsumed_patient_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 of duplicate record being merged and tombstoned."},
            {"name": "clinical_rationale", "type": "string", "required": True, "nullable": False, "description": "Mandatory clinical justification for merge action."}
        ]
    },

    # Visit & Queue Schemas
    {
        "id": "SCHEMA-API-016",
        "name": "VisitCreationRequest",
        "category": "Visit",
        "description": "OPD visit registration and token generation payload.",
        "fields": [
            {"name": "patient_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 patient identifier."},
            {"name": "visit_type", "type": "string", "required": True, "nullable": False, "description": "Visit category: GENERAL_OPD, ANC_PNC, IMMUNIZATION, NCD_FOLLOWUP, EMERGENCY."},
            {"name": "is_emergency", "type": "boolean", "required": True, "nullable": False, "description": "Fast-track emergency flag bypassing regular triage queue."},
            {"name": "priority_category", "type": "string", "required": True, "nullable": False, "description": "Acuity level: ROUTINE, SENIOR_CITIZEN, MATERNAL, PEDIATRIC, RED_EMERGENCY."},
            {"name": "assigned_doctor_id", "type": "string", "required": False, "nullable": True, "description": "Specific doctor ID if requested or assigned."}
        ]
    },
    {
        "id": "SCHEMA-API-017",
        "name": "QueueTokenResponse",
        "category": "Visit",
        "description": "Issued daily queue token and waiting hall broadcast descriptor.",
        "fields": [
            {"name": "visit_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 encounter visit identifier."},
            {"name": "token_number", "type": "string", "required": True, "nullable": False, "description": "Daily formatted sequential token (e.g., A-042)."},
            {"name": "sequence_number", "type": "integer", "required": True, "nullable": False, "description": "Numeric daily sequence order."},
            {"name": "status", "type": "string", "required": True, "nullable": False, "description": "Current status (ISSUED, CALLED, IN_CONSULTATION, COMPLETED, CANCELLED)."},
            {"name": "room_number", "type": "string", "required": False, "nullable": True, "description": "Assigned consultation room or triage cubicle."},
            {"name": "estimated_wait_minutes", "type": "integer", "required": True, "nullable": False, "description": "Dynamically estimated waiting time in minutes."}
        ]
    },
    {
        "id": "SCHEMA-API-018",
        "name": "QueueStatusUpdateCommand",
        "category": "Visit",
        "description": "Doctor/nurse command transitioning token queue state.",
        "fields": [
            {"name": "action", "type": "string", "required": True, "nullable": False, "description": "Action verb: CALL_NEXT, RECALL, MARK_IN_PROGRESS, HOLD, SKIP, COMPLETE."},
            {"name": "room_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 facility room where action is being executed."}
        ]
    },

    # Triage & Vitals Schemas
    {
        "id": "SCHEMA-API-019",
        "name": "TriageAssessmentRequest",
        "category": "Triage",
        "description": "Nursing triage and physical vitals acquisition payload.",
        "fields": [
            {"name": "visit_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 visit identifier."},
            {"name": "systolic_bp", "type": "integer", "required": False, "nullable": True, "description": "Systolic blood pressure in mmHg (50..300)."},
            {"name": "diastolic_bp", "type": "integer", "required": False, "nullable": True, "description": "Diastolic blood pressure in mmHg (30..200)."},
            {"name": "pulse_rate", "type": "integer", "required": True, "nullable": False, "description": "Heart rate in beats per minute (30..250)."},
            {"name": "temperature_fahrenheit", "type": "number", "required": True, "nullable": False, "description": "Body temperature in Fahrenheit (90.0..110.0)."},
            {"name": "spo2_percent", "type": "number", "required": True, "nullable": False, "description": "Blood oxygen saturation percentage (50.0..100.0)."},
            {"name": "respiratory_rate", "type": "integer", "required": False, "nullable": True, "description": "Breaths per minute (8..60)."},
            {"name": "weight_kg", "type": "number", "required": False, "nullable": True, "description": "Body weight in kilograms (1.0..300.0)."},
            {"name": "height_cm", "type": "number", "required": False, "nullable": True, "description": "Height in centimeters (30.0..250.0)."},
            {"name": "blood_glucose_mgdl", "type": "number", "required": False, "nullable": True, "description": "Random blood sugar in mg/dL (20..800)."},
            {"name": "acuity_color", "type": "string", "required": True, "nullable": False, "description": "SATS triage acuity classification: RED, ORANGE, YELLOW, GREEN, BLUE."},
            {"name": "danger_signs_observed", "type": "array", "required": False, "nullable": True, "description": "List of clinical danger signs (stridor, cyanosis, convulsion, shock)."}
        ]
    },
    {
        "id": "SCHEMA-API-020",
        "name": "TriageScoreResponse",
        "category": "Triage",
        "description": "Computed MEWS score, acuity tier, and immediate escalation guidance.",
        "fields": [
            {"name": "triage_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 triage assessment primary key."},
            {"name": "mews_score", "type": "integer", "required": True, "nullable": False, "description": "Calculated Modified Early Warning Score (0..14)."},
            {"name": "acuity_category", "type": "string", "required": True, "nullable": False, "description": "Determined triage color code (RED, ORANGE, YELLOW, GREEN, BLUE)."},
            {"name": "is_critical_escalation", "type": "boolean", "required": True, "nullable": False, "description": "Flag indicating automatic doctor pager / priority room diversion."},
            {"name": "alert_ids", "type": "array", "required": True, "nullable": False, "description": "Generated danger alerts requiring medical officer acknowledgment."}
        ]
    },

    # Consultation Schemas
    {
        "id": "SCHEMA-API-021",
        "name": "ConsultationEncounterRequest",
        "category": "Consultation",
        "description": "Doctor outpatient SOAP encounter notes, diagnosis coding, and care plan.",
        "fields": [
            {"name": "visit_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 visit identifier."},
            {"name": "chief_complaints", "type": "array", "required": True, "nullable": False, "description": "List of patient symptoms with duration and severity."},
            {"name": "history_of_present_illness", "type": "string", "required": False, "nullable": True, "description": "Detailed clinical narrative of present illness."},
            {"name": "physical_examination_findings", "type": "string", "required": False, "nullable": True, "description": "Systemic and local clinical examination observations."},
            {"name": "provisional_diagnoses", "type": "array", "required": True, "nullable": False, "description": "List of primary diagnoses with ICD-10 and SNOMED CT codes."},
            {"name": "clinical_summary_notes", "type": "string", "required": True, "nullable": False, "description": "Comprehensive SOAP progress note."},
            {"name": "follow_up_date", "type": "string", "required": False, "nullable": True, "description": "Planned recall date for chronic care or reassessment (YYYY-MM-DD)."}
        ]
    },
    {
        "id": "SCHEMA-API-022",
        "name": "DiagnosisEntry",
        "category": "Consultation",
        "description": "Standardized diagnostic terminology entry.",
        "fields": [
            {"name": "icd10_code", "type": "string", "required": True, "nullable": False, "description": "WHO ICD-10 diagnostic code (e.g., E11.9, I10, J06.9)."},
            {"name": "icd10_display", "type": "string", "required": True, "nullable": False, "description": "Standard clinical name of diagnosis."},
            {"name": "snomed_concept_id", "type": "string", "required": False, "nullable": True, "description": "SNOMED CT clinical concept identifier."},
            {"name": "diagnosis_type", "type": "string", "required": True, "nullable": False, "description": "PRIMARY, SECONDARY, DIFFERENTIAL, RESOLVED."},
            {"name": "confidence_level", "type": "string", "required": True, "nullable": False, "description": "CONFIRMED, SUSPECTED, RULED_OUT."}
        ]
    },

    # Prescription Schemas
    {
        "id": "SCHEMA-API-023",
        "name": "PrescriptionCreationRequest",
        "category": "Prescription",
        "description": "Electronic prescription authorization payload issued by treating physician.",
        "fields": [
            {"name": "encounter_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 clinical encounter identifier."},
            {"name": "items", "type": "array", "required": True, "nullable": False, "description": "List of prescribed medications adhering to BBMP formulary."},
            {"name": "doctor_instructions_kannada", "type": "string", "required": False, "nullable": True, "description": "Localized instructions printed on citizen slip in Kannada."},
            {"name": "doctor_instructions_english", "type": "string", "required": False, "nullable": True, "description": "Standard instructions printed in English."}
        ]
    },
    {
        "id": "SCHEMA-API-024",
        "name": "PrescriptionLineItem",
        "category": "Prescription",
        "description": "Individual medication line item in electronic prescription.",
        "fields": [
            {"name": "drug_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 formulary drug identifier."},
            {"name": "dosage_form", "type": "string", "required": True, "nullable": False, "description": "TABLET, CAPSULE, SYRUP, INJECTION, OINTMENT, DROPS."},
            {"name": "strength", "type": "string", "required": True, "nullable": False, "description": "Strength specification (e.g., 500mg, 10ml, 5mg/ml)."},
            {"name": "route", "type": "string", "required": True, "nullable": False, "description": "Route of administration: ORAL, TOPICAL, INTRAVENOUS, INTRAMUSCULAR, INHALATION."},
            {"name": "frequency", "type": "string", "required": True, "nullable": False, "description": "Standard frequency: ONCE_DAILY, TWICE_DAILY, THRICE_DAILY, FOUR_TIMES_DAILY, AS_NEEDED."},
            {"name": "duration_days", "type": "integer", "required": True, "nullable": False, "description": "Treatment duration in days (1..90)."},
            {"name": "quantity_prescribed", "type": "integer", "required": True, "nullable": False, "description": "Total discrete units to be dispensed."},
            {"name": "timing_relation_to_food", "type": "string", "required": True, "nullable": False, "description": "BEFORE_FOOD, AFTER_FOOD, WITH_FOOD, EMPTY_STOMACH."}
        ]
    },

    # Pharmacy & Dispensing Schemas
    {
        "id": "SCHEMA-API-025",
        "name": "PharmacyDispenseRequest",
        "category": "Pharmacy",
        "description": "Pharmacist dispensation verification and batch allocation payload.",
        "fields": [
            {"name": "prescription_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 prescription identifier."},
            {"name": "dispensed_items", "type": "array", "required": True, "nullable": False, "description": "List of dispensed line items with allocated batch numbers."},
            {"name": "pharmacist_counseling_notes", "type": "string", "required": False, "nullable": True, "description": "Notes confirming verbal counseling and dosage explanation."}
        ]
    },
    {
        "id": "SCHEMA-API-026",
        "name": "DispensedLineItem",
        "category": "Pharmacy",
        "description": "Batch-allocated medication line item deducted from stock.",
        "fields": [
            {"name": "prescription_item_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 prescription item identifier."},
            {"name": "batch_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 pharmacy batch identifier allocated via FEFO."},
            {"name": "quantity_dispensed", "type": "integer", "required": True, "nullable": False, "description": "Actual discrete units issued to patient."},
            {"name": "is_partial_dispense", "type": "boolean", "required": True, "nullable": False, "description": "Flag indicating partial fill due to stock exhaustion."},
            {"name": "substitution_drug_id", "type": "string", "required": False, "nullable": True, "description": "Formulary substitute drug ID if generic substituted under doctor consent."}
        ]
    },

    # Inventory Schemas
    {
        "id": "SCHEMA-API-027",
        "name": "StockReceiptRequest",
        "category": "Inventory",
        "description": "Clinic stock receipt from central BBMP warehouse or zonal depot.",
        "fields": [
            {"name": "indent_id", "type": "string", "required": False, "nullable": True, "description": "UUIDv7 indent requisition being fulfilled."},
            {"name": "invoice_number", "type": "string", "required": True, "nullable": False, "description": "Depot dispatch challan / delivery invoice reference."},
            {"name": "received_batches", "type": "array", "required": True, "nullable": False, "description": "Array of medication batches received into clinic stock."}
        ]
    },
    {
        "id": "SCHEMA-API-028",
        "name": "BatchReceiptItem",
        "category": "Inventory",
        "description": "Discrete pharmaceutical batch received into facility inventory.",
        "fields": [
            {"name": "drug_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 formulary drug identifier."},
            {"name": "batch_number", "type": "string", "required": True, "nullable": False, "description": "Manufacturer lot/batch alphanumeric code."},
            {"name": "expiry_date", "type": "string", "required": True, "nullable": False, "description": "Expiration date (YYYY-MM-DD)."},
            {"name": "quantity_received", "type": "integer", "required": True, "nullable": False, "description": "Total discrete units received."},
            {"name": "manufacturer_name", "type": "string", "required": True, "nullable": False, "description": "Pharmaceutical manufacturer name."},
            {"name": "cold_chain_compliant", "type": "boolean", "required": True, "nullable": False, "description": "Confirmation that cold chain transit temperature was verified."}
        ]
    },
    {
        "id": "SCHEMA-API-029",
        "name": "StockAdjustmentCommand",
        "category": "Inventory",
        "description": "Physical inventory audit adjustment or write-off payload.",
        "fields": [
            {"name": "batch_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 batch identifier being adjusted."},
            {"name": "adjusted_quantity", "type": "integer", "required": True, "nullable": False, "description": "Delta quantity (+/- units) to reconcile stock."},
            {"name": "reason_code", "type": "string", "required": True, "nullable": False, "description": "DAMAGED, EXPIRED, THEFT_LOSS, AUDIT_DISCREPANCY, BREAKAGE."},
            {"name": "supervisor_approval_token", "type": "string", "required": True, "nullable": False, "description": "Dual-authorization cryptographic approval signature."}
        ]
    },

    # Laboratory Schemas
    {
        "id": "SCHEMA-API-030",
        "name": "LabOrderCreationRequest",
        "category": "Lab",
        "description": "Doctor requisition for diagnostic investigations.",
        "fields": [
            {"name": "encounter_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 encounter identifier."},
            {"name": "test_ids", "type": "array", "required": True, "nullable": False, "description": "List of diagnostic test catalog IDs (e.g., LOINC-mapped tests)."},
            {"name": "clinical_indication", "type": "string", "required": True, "nullable": False, "description": "Clinical reason for test ordering."},
            {"name": "is_urgent", "type": "boolean", "required": True, "nullable": False, "description": "Stat test priority flag."}
        ]
    },
    {
        "id": "SCHEMA-API-031",
        "name": "LabResultEntryRequest",
        "category": "Lab",
        "description": "Lab technician diagnostic result capture and panic flag payload.",
        "fields": [
            {"name": "lab_order_item_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 lab order line item identifier."},
            {"name": "numerical_value", "type": "number", "required": False, "nullable": True, "description": "Quantitative test result value."},
            {"name": "unit_of_measure", "type": "string", "required": False, "nullable": True, "description": "Standard measurement unit (mg/dL, g/dL, cells/mcL)."},
            {"name": "qualitative_result", "type": "string", "required": False, "nullable": True, "description": "Qualitative result: POSITIVE, NEGATIVE, REACTIVE, NON_REACTIVE."},
            {"name": "reference_range_text", "type": "string", "required": True, "nullable": False, "description": "Biological reference interval printed on report."},
            {"name": "is_panic_value", "type": "boolean", "required": True, "nullable": False, "description": "Flag indicating critical alert requiring immediate doctor phone alert."},
            {"name": "technician_observations", "type": "string", "required": False, "nullable": True, "description": "Microscopic or technical remarks."}
        ]
    },

    # Referral Schemas
    {
        "id": "SCHEMA-API-032",
        "name": "ReferralCreationRequest",
        "category": "Referral",
        "description": "Secondary/tertiary hospital transfer dossier payload.",
        "fields": [
            {"name": "encounter_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 encounter initiating referral."},
            {"name": "destination_hospital_type", "type": "string", "required": True, "nullable": False, "description": "BBMP_GENERAL_HOSPITAL, GOVT_MEDICAL_COLLEGE, SPECIALTY_INSTITUTE."},
            {"name": "urgency_level", "type": "string", "required": True, "nullable": False, "description": "EMERGENCY_108, URGENT_24H, ROUTINE_SPECIALTY."},
            {"name": "referral_specialty", "type": "string", "required": True, "nullable": False, "description": "CARDIOLOGY, OBGYN, ORTHOPEDICS, PEDIATRICS, PSYCHIATRY, ONCOLOGY."},
            {"name": "clinical_summary_dossier", "type": "string", "required": True, "nullable": False, "description": "Comprehensive transfer summary including triage vitals and provisional diagnosis."},
            {"name": "transport_required", "type": "boolean", "required": True, "nullable": False, "description": "Indicates whether 108 Arogya Kavacha ambulance was requested."}
        ]
    },

    # Notification Schemas
    {
        "id": "SCHEMA-API-033",
        "name": "OutboundNotificationRequest",
        "category": "Notification",
        "description": "System-generated citizen SMS / WhatsApp message dispatch payload.",
        "fields": [
            {"name": "patient_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 recipient patient identifier."},
            {"name": "channel", "type": "string", "required": True, "nullable": False, "description": "SMS, WHATSAPP, VOICE_IVR."},
            {"name": "template_id", "type": "string", "required": True, "nullable": False, "description": "Approved DLT template registration code."},
            {"name": "preferred_language", "type": "string", "required": True, "nullable": False, "description": "Language code: kn (Kannada) or en (English)."},
            {"name": "template_parameters", "type": "object", "required": True, "nullable": False, "description": "Dynamic variable bindings (citizen_name, clinic_name, token_number, date)."}
        ]
    },

    # Analytics Schemas
    {
        "id": "SCHEMA-API-034",
        "name": "ClinicKpiSummaryResponse",
        "category": "Analytics",
        "description": "Aggregated daily operational performance metrics for a clinic facility.",
        "fields": [
            {"name": "facility_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 facility identifier."},
            {"name": "metric_date", "type": "string", "required": True, "nullable": False, "description": "Date of aggregation (YYYY-MM-DD)."},
            {"name": "total_registered_opd", "type": "integer", "required": True, "nullable": False, "description": "Total outpatient patient footfall."},
            {"name": "avg_consultation_time_seconds", "type": "number", "required": True, "nullable": False, "description": "Average physician consultation duration."},
            {"name": "total_prescriptions_dispensed", "type": "integer", "required": True, "nullable": False, "description": "Total pharmacy dispenses completed."},
            {"name": "stockout_drug_count", "type": "integer", "required": True, "nullable": False, "description": "Number of critical formulary drugs currently at zero stock."},
            {"name": "red_triage_count", "type": "integer", "required": True, "nullable": False, "description": "Count of emergency red triage cases managed."}
        ]
    },

    # Audit Schemas
    {
        "id": "SCHEMA-API-035",
        "name": "AuditEventQuery",
        "category": "Audit",
        "description": "Cryptographic WORM audit log query and verification payload.",
        "fields": [
            {"name": "entity_type", "type": "string", "required": False, "nullable": True, "description": "Audited entity name (e.g., patients, prescriptions)."},
            {"name": "entity_id", "type": "string", "required": False, "nullable": True, "description": "UUIDv7 entity primary key."},
            {"name": "actor_id", "type": "string", "required": False, "nullable": True, "description": "UUIDv7 user ID who triggered event."},
            {"name": "event_type", "type": "string", "required": False, "nullable": True, "description": "Action verb: CREATE, READ, UPDATE, DELETE, EXPORT, BREAK_GLASS."},
            {"name": "from_timestamp", "type": "string", "required": True, "nullable": False, "description": "ISO-8601 start timestamp."},
            {"name": "to_timestamp", "type": "string", "required": True, "nullable": False, "description": "ISO-8601 end timestamp."}
        ]
    },

    # ABDM Schemas
    {
        "id": "SCHEMA-API-036",
        "name": "AbhaVerificationRequest",
        "category": "ABDM",
        "description": "ABDM M1 ABHA address discovery and OTP verification payload.",
        "fields": [
            {"name": "auth_method", "type": "string", "required": True, "nullable": False, "description": "MOBILE_OTP, AADHAAR_OTP, DEMOGRAPHICS."},
            {"name": "identifier", "type": "string", "required": True, "nullable": False, "description": "14-digit ABHA number or ABHA address string."},
            {"name": "otp", "type": "string", "required": False, "nullable": True, "description": "6-digit OTP received on citizen phone."}
        ]
    },
    {
        "id": "SCHEMA-API-037",
        "name": "FhirBundleExportResponse",
        "category": "ABDM",
        "description": "FHIR R4 DiagnosticReport / Encounter document bundle for health record sharing.",
        "fields": [
            {"name": "resourceType", "type": "string", "required": True, "nullable": False, "description": "Fixed string 'Bundle'."},
            {"name": "type", "type": "string", "required": True, "nullable": False, "description": "Fixed string 'document'."},
            {"name": "entry", "type": "array", "required": True, "nullable": False, "description": "Array of FHIR R4 clinical resources (Composition, Patient, Encounter, Condition)."}
        ]
    },

    # Portability Schemas
    {
        "id": "SCHEMA-API-038",
        "name": "PortabilityExportJobRequest",
        "category": "Portability",
        "description": "Citizen DPDP Act 2023 Section 12 Data Portability export request.",
        "fields": [
            {"name": "patient_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 citizen identifier."},
            {"name": "export_format", "type": "string", "required": True, "nullable": False, "description": "FHIR_JSON, NDJSON, CSV_ZIP, PDF_ENCRYPTED."},
            {"name": "date_range_start", "type": "string", "required": False, "nullable": True, "description": "Optional start date filter."},
            {"name": "date_range_end", "type": "string", "required": False, "nullable": True, "description": "Optional end date filter."}
        ]
    },
    {
        "id": "SCHEMA-API-039",
        "name": "PortabilityJobStatusResponse",
        "category": "Portability",
        "description": "Status and download link for asynchronous portability export job.",
        "fields": [
            {"name": "job_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 background export task identifier."},
            {"name": "status", "type": "string", "required": True, "nullable": False, "description": "QUEUED, PROCESSING, COMPLETED, FAILED, EXPIRED."},
            {"name": "progress_percent", "type": "integer", "required": True, "nullable": False, "description": "Completion percentage (0..100)."},
            {"name": "download_url", "type": "string", "required": False, "nullable": True, "description": "Time-limited pre-signed S3 download URL (expires in 30 minutes)."},
            {"name": "expires_at", "type": "string", "required": False, "nullable": True, "description": "Expiration timestamp after which file is purged."}
        ]
    },

    # System & Sync Schemas
    {
        "id": "SCHEMA-API-040",
        "name": "EdgeSyncBatchRequest",
        "category": "System",
        "description": "Offline mutation journal replay batch uploaded by clinic edge gateway.",
        "fields": [
            {"name": "facility_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 clinic facility identifier."},
            {"name": "edge_node_id", "type": "string", "required": True, "nullable": False, "description": "Cryptographic hardware identity of edge mini-server."},
            {"name": "vector_clock", "type": "object", "required": True, "nullable": False, "description": "Lamport vector clock map of edge node states."},
            {"name": "mutations", "type": "array", "required": True, "nullable": False, "description": "Ordered array of queued mutation records captured while offline."}
        ]
    },
    {
        "id": "SCHEMA-API-041",
        "name": "SyncMutationItem",
        "category": "System",
        "description": "Discrete mutation record executed on edge SQLite node.",
        "fields": [
            {"name": "mutation_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 generated on edge tablet/server."},
            {"name": "target_table", "type": "string", "required": True, "nullable": False, "description": "Target relational table name (e.g., patient_vitals)."},
            {"name": "operation", "type": "string", "required": True, "nullable": False, "description": "INSERT, UPDATE, SOFT_DELETE."},
            {"name": "row_id", "type": "string", "required": True, "nullable": False, "description": "UUIDv7 primary key of target row."},
            {"name": "payload", "type": "object", "required": True, "nullable": False, "description": "JSON serialized row attributes."},
            {"name": "edge_timestamp", "type": "string", "required": True, "nullable": False, "description": "Local device timestamp when user committed action."}
        ]
    },
    {
        "id": "SCHEMA-API-042",
        "name": "EdgeSyncBatchResponse",
        "category": "System",
        "description": "Cloud synchronization acknowledgment, conflict resolutions, and server updates.",
        "fields": [
            {"name": "reconciled_mutations", "type": "integer", "required": True, "nullable": False, "description": "Count of successfully merged mutations."},
            {"name": "conflict_count", "type": "integer", "required": True, "nullable": False, "description": "Count of mutations requiring CRDT last-write-wins or doctor resolution."},
            {"name": "conflicts", "type": "array", "required": True, "nullable": False, "description": "Array of conflict resolution descriptors."},
            {"name": "server_delta_mutations", "type": "array", "required": True, "nullable": False, "description": "Server-side updates from cloud to be ingested by edge node."}
        ]
    }
]

# Add remaining schemas SCHEMA-API-043 to SCHEMA-API-068 dynamically to ensure 68 complete schemas
ADDITIONAL_SCHEMA_DEFS = [
    ("SCHEMA-API-043", "HealthCheckLivenessResponse", "System", "Kubernetes liveness probe response", [("status", "string", True), ("timestamp", "string", True)]),
    ("SCHEMA-API-044", "HealthCheckReadinessResponse", "System", "Kubernetes readiness probe verifying DB and cache connectivity", [("status", "string", True), ("dependencies", "object", True), ("healthy", "boolean", True)]),
    ("SCHEMA-API-045", "FacilityRoomStatusResponse", "Visit", "Real-time occupancy status of clinic examination room", [("room_id", "string", True), ("occupancy_state", "string", True), ("active_doctor_id", "string", False)]),
    ("SCHEMA-API-046", "VitalSignsSeriesResponse", "Triage", "Longitudinal vital signs readings for a patient across visits", [("patient_id", "string", True), ("readings", "array", True)]),
    ("SCHEMA-API-047", "DangerAlertNotification", "Triage", "Critical physiologic deterioration alert payload", [("alert_id", "string", True), ("acuity", "string", True), ("vital_trigger", "string", True)]),
    ("SCHEMA-API-048", "ClinicalNotePatchRequest", "Consultation", "Addendum or amendment payload for finalized consultation note", [("addendum_text", "string", True), ("amendment_reason", "string", True)]),
    ("SCHEMA-API-049", "DrugFormularyItemResponse", "Prescription", "Essential drugs formulary metadata and dosage guidelines", [("drug_id", "string", True), ("generic_name", "string", True), ("strength", "string", True)]),
    ("SCHEMA-API-050", "MedicationInteractionWarning", "Prescription", "CDSS drug-drug or drug-allergy contraindication alert", [("severity", "string", True), ("interacting_drugs", "array", True), ("clinical_effect", "string", True)]),
    ("SCHEMA-API-051", "PharmacyStockBalanceResponse", "Pharmacy", "On-hand inventory balance per batch in clinic dispensary", [("drug_id", "string", True), ("batches", "array", True), ("total_quantity", "integer", True)]),
    ("SCHEMA-API-052", "DispensingReversalRequest", "Pharmacy", "Void or reversal of incorrect dispensation transaction", [("dispense_id", "string", True), ("reversal_reason", "string", True), ("returned_items", "array", True)]),
    ("SCHEMA-API-053", "ColdChainTelemetryBatch", "Inventory", "IoT temperature and power sensor readings from vaccine refrigerator", [("device_id", "string", True), ("temperature_celsius", "number", True), ("readings", "array", True)]),
    ("SCHEMA-API-054", "ColdChainExcursionAlert", "Inventory", "Vaccine temperature breach alert notification", [("alert_id", "string", True), ("min_temp", "number", True), ("max_temp", "number", True), ("duration_minutes", "integer", True)]),
    ("SCHEMA-API-055", "LabSpecimenCollectionRequest", "Lab", "Phlebotomy specimen accession and barcode mapping", [("lab_order_id", "string", True), ("barcode_id", "string", True), ("collection_time", "string", True)]),
    ("SCHEMA-API-056", "LabSpecimenRejectionPayload", "Lab", "Specimen rejection due to hemolysis, clotting, or volume insufficiency", [("order_item_id", "string", True), ("rejection_reason", "string", True)]),
    ("SCHEMA-API-057", "ReferralCounterNoteResponse", "Referral", "Discharge summary received from tertiary hospital for referred patient", [("referral_id", "string", True), ("tertiary_diagnosis", "string", True), ("care_plan", "string", True)]),
    ("SCHEMA-API-058", "SmsDeliveryReceiptPayload", "Notification", "Telecom gateway delivery status webhook callback", [("message_id", "string", True), ("status", "string", True), ("carrier_timestamp", "string", True)]),
    ("SCHEMA-API-059", "EpidemicSurveillanceReport", "Analytics", "Syndromic fever and acute respiratory infection cluster report", [("ward_number", "integer", True), ("syndrome", "string", True), ("case_count", "integer", True)]),
    ("SCHEMA-API-060", "DoctorWorkloadMetricResponse", "Analytics", "Outpatient encounters, average duration, and pending queue per doctor", [("doctor_id", "string", True), ("patient_count", "integer", True), ("active_time_minutes", "integer", True)]),
    ("SCHEMA-API-061", "AuditHashChainVerification", "Audit", "Cryptographic verification response for WORM audit hash integrity", [("verification_status", "string", True), ("verified_block_count", "integer", True), ("tamper_detected", "boolean", True)]),
    ("SCHEMA-API-062", "AbdmConsentArtefactPayload", "ABDM", "Standard ABDM electronic consent artifact signed by citizen", [("consent_id", "string", True), ("purpose", "string", True), ("date_range", "object", True)]),
    ("SCHEMA-API-063", "AbdmCareContextLinkRequest", "ABDM", "HIP care context linking request to associate visit with ABHA", [("patient_uhid", "string", True), ("care_context_id", "string", True), ("display_name", "string", True)]),
    ("SCHEMA-API-064", "DataPortabilityConsentProof", "Portability", "Digital consent authorization token enabling data extraction", [("patient_id", "string", True), ("consent_timestamp", "string", True), ("signature", "string", True)]),
    ("SCHEMA-API-065", "HardwareTerminalRegisterRequest", "System", "Registration of clinic tablet or receipt printer with edge gateway", [("mac_address", "string", True), ("device_type", "string", True), ("room_id", "string", True)]),
    ("SCHEMA-API-066", "DatabaseReplicationStatusResponse", "System", "Cloud PostgreSQL streaming replication lag and Patroni leader status", [("role", "string", True), ("replication_lag_bytes", "integer", True), ("in_sync", "boolean", True)]),
    ("SCHEMA-API-067", "UserRoleAssignmentPayload", "Auth", "Administrative assignment of role and facility scope to staff member", [("user_id", "string", True), ("role_codes", "array", True), ("facility_ids", "array", True)]),
    ("SCHEMA-API-068", "BulkImportStatusResponse", "System", "Status of administrative bulk data ingestion (formulary, providers)", [("batch_id", "string", True), ("total_rows", "integer", True), ("processed_rows", "integer", True), ("error_count", "integer", True)])
]

for item in ADDITIONAL_SCHEMA_DEFS:
    fields = [{"name": f[0], "type": f[1], "required": f[2], "nullable": not f[2], "description": f"Attribute {f[0]} of {item[1]}"} for f in item[4]]
    API_SCHEMAS.append({
        "id": item[0],
        "name": item[1],
        "category": item[2],
        "description": item[3],
        "fields": fields
    })

SCHEMA_MAP = {s["id"]: s for s in API_SCHEMAS}
SCHEMA_NAME_MAP = {s["name"]: s for s in API_SCHEMAS}

# -----------------------------------------------------------------------------
# 2. 115+ STANDARDIZED API ERROR CODES (ERR-AUTH-001 to ERR-SYS-020)
# -----------------------------------------------------------------------------
API_ERROR_CODES = [
    # Auth & IAM Errors (ERR-AUTH-001 to ERR-AUTH-015)
    {"id": "ERR-AUTH-001", "status": 401, "domain": "Auth", "code": "AUTH_CREDENTIALS_INVALID", "message": "Invalid municipal employee ID or password.", "retryable": False, "category": "Authentication"},
    {"id": "ERR-AUTH-002", "status": 401, "domain": "Auth", "code": "AUTH_TOKEN_EXPIRED", "message": "Access token has expired. Request renewal using refresh token.", "retryable": True, "category": "Authentication"},
    {"id": "ERR-AUTH-003", "status": 401, "domain": "Auth", "code": "AUTH_TOKEN_INVALID", "message": "Cryptographic signature verification failed on access token.", "retryable": False, "category": "Authentication"},
    {"id": "ERR-AUTH-004", "status": 401, "domain": "Auth", "code": "AUTH_REFRESH_TOKEN_EXPIRED", "message": "Refresh token session has expired. Full re-authentication required.", "retryable": False, "category": "Authentication"},
    {"id": "ERR-AUTH-005", "status": 401, "domain": "Auth", "code": "AUTH_SESSION_REVOKED", "message": "Session has been invalidated due to concurrent login or administrative revocation.", "retryable": False, "category": "Authentication"},
    {"id": "ERR-AUTH-006", "status": 403, "domain": "Auth", "code": "AUTH_PERMISSION_DENIED", "message": "Authenticated user lacks the required RBAC permission for this resource.", "retryable": False, "category": "Authorization"},
    {"id": "ERR-AUTH-007", "status": 403, "domain": "Auth", "code": "AUTH_FACILITY_SCOPE_MISMATCH", "message": "User is not authorized to execute operations in the requested clinic facility.", "retryable": False, "category": "Authorization"},
    {"id": "ERR-AUTH-008", "status": 403, "domain": "Auth", "code": "AUTH_ACCOUNT_LOCKED", "message": "Account temporarily locked due to excessive failed login attempts (5 strikes).", "retryable": False, "category": "Security"},
    {"id": "ERR-AUTH-009", "status": 401, "domain": "Auth", "code": "AUTH_MFA_REQUIRED", "message": "Multi-factor authentication TOTP code required to complete privileged login.", "retryable": False, "category": "Authentication"},
    {"id": "ERR-AUTH-010", "status": 401, "domain": "Auth", "code": "AUTH_DEVICE_UNTRUSTED", "message": "Hardware tablet device fingerprint is not registered or certificate expired.", "retryable": False, "category": "Security"},
    {"id": "ERR-AUTH-011", "status": 403, "domain": "Auth", "code": "AUTH_BREAK_GLASS_UNAUTHORIZED", "message": "Break-glass privileged emergency access denied; clinical director role required.", "retryable": False, "category": "Authorization"},
    {"id": "ERR-AUTH-012", "status": 400, "domain": "Auth", "code": "AUTH_PASSWORD_POLICY_VIOLATED", "message": "Password does not meet 12+ char complexity, uppercase, symbol, or dictionary rules.", "retryable": False, "category": "Validation"},
    {"id": "ERR-AUTH-013", "status": 409, "domain": "Auth", "code": "AUTH_CONCURRENT_SHIFT_ACTIVE", "message": "User is already logged in with an active shift at another facility.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-AUTH-014", "status": 403, "domain": "Auth", "code": "AUTH_IP_REPUTATION_BLOCKED", "message": "Request originating from an unauthorized non-BBMP municipal network block.", "retryable": False, "category": "Security"},
    {"id": "ERR-AUTH-015", "status": 500, "domain": "Auth", "code": "AUTH_KMS_SIGNING_FAILURE", "message": "Hardware Security Module / Vault KMS failed to generate cryptographic token signature.", "retryable": True, "category": "System"},

    # Patient & Demographic Errors (ERR-PATIENT-001 to ERR-PATIENT-012)
    {"id": "ERR-PATIENT-001", "status": 404, "domain": "Patient", "code": "PATIENT_NOT_FOUND", "message": "No active patient record matches the provided UHID or identifier.", "retryable": False, "category": "NotFound"},
    {"id": "ERR-PATIENT-002", "status": 409, "domain": "Patient", "code": "PATIENT_DUPLICATE_DETECTED", "message": "High-confidence duplicate citizen detected (matching phone and phonetic name).", "retryable": False, "category": "Conflict"},
    {"id": "ERR-PATIENT-003", "status": 400, "domain": "Patient", "code": "PATIENT_PHONE_INVALID", "message": "Mobile number must be exactly 10 digits complying with Indian numbering plan.", "retryable": False, "category": "Validation"},
    {"id": "ERR-PATIENT-004", "status": 400, "domain": "Patient", "code": "PATIENT_DOB_FUTURE", "message": "Date of birth cannot be in the future.", "retryable": False, "category": "Validation"},
    {"id": "ERR-PATIENT-005", "status": 400, "domain": "Patient", "code": "PATIENT_WARD_INVALID", "message": "BBMP ward number must be between 1 and 243.", "retryable": False, "category": "Validation"},
    {"id": "ERR-PATIENT-006", "status": 409, "domain": "Patient", "code": "PATIENT_ALREADY_MERGED", "message": "Requested patient record has already been merged into a surviving primary profile.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-PATIENT-007", "status": 400, "domain": "Patient", "code": "PATIENT_MERGE_SAME_RECORD", "message": "Surviving and subsumed patient identifiers cannot be identical.", "retryable": False, "category": "Validation"},
    {"id": "ERR-PATIENT-008", "status": 403, "domain": "Patient", "code": "PATIENT_PRIVACY_RESTRICTED", "message": "Access restricted: citizen has revoked consent for general record disclosure.", "retryable": False, "category": "Privacy"},
    {"id": "ERR-PATIENT-009", "status": 400, "domain": "Patient", "code": "PATIENT_PINCODE_INVALID", "message": "Postal pincode must be valid Bengaluru delivery code (560001..560110).", "retryable": False, "category": "Validation"},
    {"id": "ERR-PATIENT-010", "status": 409, "domain": "Patient", "code": "PATIENT_ABHA_ALREADY_LINKED", "message": "Provided ABHA number is already bound to another registered citizen profile.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-PATIENT-011", "status": 400, "domain": "Patient", "code": "PATIENT_NAME_MALFORMED", "message": "First name contains illegal control characters, numbers, or exceeds 100 characters.", "retryable": False, "category": "Validation"},
    {"id": "ERR-PATIENT-012", "status": 500, "domain": "Patient", "code": "PATIENT_MPI_SEARCH_TIMEOUT", "message": "Master Patient Index fuzzy phonetic search cluster timed out.", "retryable": True, "category": "DependencyFailure"},

    # Visit & Queue Errors (ERR-VISIT-001 to ERR-VISIT-010)
    {"id": "ERR-VISIT-001", "status": 404, "domain": "Visit", "code": "VISIT_NOT_FOUND", "message": "Encounter visit identifier does not exist.", "retryable": False, "category": "NotFound"},
    {"id": "ERR-VISIT-002", "status": 409, "domain": "Visit", "code": "VISIT_ACTIVE_ENCOUNTER_EXISTS", "message": "Patient already has an active, unclosed outpatient encounter today.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-VISIT-003", "status": 400, "domain": "Visit", "code": "VISIT_QUEUE_TRANSITION_ILLEGAL", "message": "Illegal queue state transition requested (e.g., calling completed token).", "retryable": False, "category": "BusinessRule"},
    {"id": "ERR-VISIT-004", "status": 409, "domain": "Visit", "code": "VISIT_TOKEN_ALREADY_CALLED", "message": "Queue token has already been called by another doctor in room.", "retryable": False, "category": "Concurrency"},
    {"id": "ERR-VISIT-005", "status": 400, "domain": "Visit", "code": "VISIT_FACILITY_CLOSED", "message": "Cannot create visit: clinic is outside published operational hours (09:00 - 16:30).", "retryable": False, "category": "BusinessRule"},
    {"id": "ERR-VISIT-006", "status": 400, "domain": "Visit", "code": "VISIT_DOCTOR_NOT_ROSTERED", "message": "Assigned doctor does not have an active shift rostered today.", "retryable": False, "category": "Validation"},
    {"id": "ERR-VISIT-007", "status": 404, "domain": "Visit", "code": "VISIT_ROOM_NOT_FOUND", "message": "Specified consultation room identifier does not exist in facility.", "retryable": False, "category": "NotFound"},
    {"id": "ERR-VISIT-008", "status": 400, "domain": "Visit", "code": "VISIT_CANCELLATION_DISALLOWED", "message": "Visit cannot be cancelled once clinical consultation has commenced.", "retryable": False, "category": "BusinessRule"},
    {"id": "ERR-VISIT-009", "status": 409, "domain": "Visit", "code": "VISIT_CONCURRENT_QUEUE_MUTATION", "message": "Queue state was modified concurrently; please refresh queue display.", "retryable": True, "category": "Concurrency"},
    {"id": "ERR-VISIT-010", "status": 500, "domain": "Visit", "code": "VISIT_TOKEN_ALLOCATION_EXHAUSTED", "message": "Daily sequence allocation table reached maximum limit.", "retryable": True, "category": "System"},

    # Triage Errors (ERR-TRIAGE-001 to ERR-TRIAGE-010)
    {"id": "ERR-TRIAGE-001", "status": 404, "domain": "Triage", "code": "TRIAGE_NOT_FOUND", "message": "No triage assessment recorded for this visit.", "retryable": False, "category": "NotFound"},
    {"id": "ERR-TRIAGE-002", "status": 400, "domain": "Triage", "code": "TRIAGE_VITALS_OUT_OF_PHYSIOLOGIC_RANGE", "message": "Vitals measurement is outside biological life boundaries (e.g., SpO2 > 100%).", "retryable": False, "category": "ClinicalSafety"},
    {"id": "ERR-TRIAGE-003", "status": 400, "domain": "Triage", "code": "TRIAGE_SYSTOLIC_LESS_THAN_DIASTOLIC", "message": "Systolic blood pressure cannot be lower than diastolic pressure.", "retryable": False, "category": "Validation"},
    {"id": "ERR-TRIAGE-004", "status": 409, "domain": "Triage", "code": "TRIAGE_ALREADY_FINALIZED", "message": "Triage assessment is already completed and cannot be overwritten.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-TRIAGE-005", "status": 400, "domain": "Triage", "code": "TRIAGE_RED_ESCALATION_OVERRIDE_FORBIDDEN", "message": "Cannot downgrade RED acuity triage without physician written concurrence.", "retryable": False, "category": "ClinicalSafety"},
    {"id": "ERR-TRIAGE-006", "status": 403, "domain": "Triage", "code": "TRIAGE_NURSE_AUTHORIZATION_REQUIRED", "message": "Only registered staff nurses or doctors may record triage acuity.", "retryable": False, "category": "Authorization"},
    {"id": "ERR-TRIAGE-007", "status": 400, "domain": "Triage", "code": "TRIAGE_PULSE_MISSING", "message": "Pulse rate is mandatory for computing MEWS acuity score.", "retryable": False, "category": "Validation"},
    {"id": "ERR-TRIAGE-008", "status": 400, "domain": "Triage", "code": "TRIAGE_TEMPERATURE_EXTREME", "message": "Temperature reading indicates severe hypothermia or hyperpyrexia.", "retryable": False, "category": "ClinicalSafety"},
    {"id": "ERR-TRIAGE-009", "status": 500, "domain": "Triage", "code": "TRIAGE_SCORING_ENGINE_ERROR", "message": "Automated SATS/MEWS rule evaluation engine returned calculation error.", "retryable": True, "category": "System"},
    {"id": "ERR-TRIAGE-010", "status": 400, "domain": "Triage", "code": "TRIAGE_VISIT_STATE_INVALID", "message": "Cannot triage a visit that is already closed or cancelled.", "retryable": False, "category": "BusinessRule"},

    # Consultation Errors (ERR-CONSULT-001 to ERR-CONSULT-010)
    {"id": "ERR-CONSULT-001", "status": 404, "domain": "Consultation", "code": "CONSULT_NOT_FOUND", "message": "Clinical encounter progress note not found.", "retryable": False, "category": "NotFound"},
    {"id": "ERR-CONSULT-002", "status": 403, "domain": "Consultation", "code": "CONSULT_DOCTOR_PRIMACY_VIOLATION", "message": "Only licensed medical officers may create or finalize consultation notes.", "retryable": False, "category": "Authorization"},
    {"id": "ERR-CONSULT-003", "status": 400, "domain": "Consultation", "code": "CONSULT_CHIEF_COMPLAINT_EMPTY", "message": "At least one chief complaint symptom is mandatory.", "retryable": False, "category": "Validation"},
    {"id": "ERR-CONSULT-004", "status": 400, "domain": "Consultation", "code": "CONSULT_DIAGNOSIS_CODE_INVALID", "message": "Provisional diagnosis must reference a valid WHO ICD-10 code.", "retryable": False, "category": "Validation"},
    {"id": "ERR-CONSULT-005", "status": 409, "domain": "Consultation", "code": "CONSULT_ALREADY_CLOSED", "message": "Consultation encounter has been finalized. Modifications require formal addendum.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-CONSULT-006", "status": 400, "domain": "Consultation", "code": "CONSULT_TRIAGE_PENDING", "message": "Patient must complete nursing triage assessment prior to doctor consultation.", "retryable": False, "category": "BusinessRule"},
    {"id": "ERR-CONSULT-007", "status": 400, "domain": "Consultation", "code": "CONSULT_ADDENDUM_REASON_EMPTY", "message": "Clinical reason for post-closure note addendum is mandatory.", "retryable": False, "category": "Validation"},
    {"id": "ERR-CONSULT-008", "status": 403, "domain": "Consultation", "code": "CONSULT_ATTENDING_MISMATCH", "message": "Only the attending clinician who opened the encounter may submit notes.", "retryable": False, "category": "Authorization"},
    {"id": "ERR-CONSULT-009", "status": 400, "domain": "Consultation", "code": "CONSULT_FOLLOWUP_DATE_PAST", "message": "Follow-up appointment date cannot be prior to today.", "retryable": False, "category": "Validation"},
    {"id": "ERR-CONSULT-010", "status": 500, "domain": "Consultation", "code": "CONSULT_CDSS_ADVISORY_TIMEOUT", "message": "Clinical decision support advisory suggestion microservice timed out.", "retryable": True, "category": "DependencyFailure"},

    # Prescription Errors (ERR-RX-001 to ERR-RX-010)
    {"id": "ERR-RX-001", "status": 404, "domain": "Prescription", "code": "RX_NOT_FOUND", "message": "Electronic prescription record does not exist.", "retryable": False, "category": "NotFound"},
    {"id": "ERR-RX-002", "status": 400, "domain": "Prescription", "code": "RX_DRUG_NOT_IN_FORMULARY", "message": "Prescribed medicine is not approved in BBMP Namma Clinic formulary.", "retryable": False, "category": "ClinicalSafety"},
    {"id": "ERR-RX-003", "status": 400, "domain": "Prescription", "code": "RX_DOSAGE_OUT_OF_BOUNDS", "message": "Prescribed dosage exceeds maximum recommended pediatric/adult limits.", "retryable": False, "category": "ClinicalSafety"},
    {"id": "ERR-RX-004", "status": 409, "domain": "Prescription", "code": "RX_CONTRAINDICATION_DETECTED", "message": "Severe drug-drug interaction or recorded patient allergy contraindication.", "retryable": False, "category": "ClinicalSafety"},
    {"id": "ERR-RX-005", "status": 400, "domain": "Prescription", "code": "RX_DURATION_EXCEEDS_MAX", "message": "Prescription duration exceeds statutory 90-day municipal limit.", "retryable": False, "category": "Validation"},
    {"id": "ERR-RX-006", "status": 409, "domain": "Prescription", "code": "RX_ALREADY_DISPENSED", "message": "Prescription has already been dispensed by pharmacy and cannot be altered.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-RX-007", "status": 400, "domain": "Prescription", "code": "RX_EMPTY_ITEMS", "message": "Prescription must contain at least one valid medication line item.", "retryable": False, "category": "Validation"},
    {"id": "ERR-RX-008", "status": 403, "domain": "Prescription", "code": "RX_PRESCRIBER_NOT_LICENSED", "message": "Prescribing staff lacks active medical council registration (KMC).", "retryable": False, "category": "Authorization"},
    {"id": "ERR-RX-009", "status": 400, "domain": "Prescription", "code": "RX_QUANTITY_ZERO", "message": "Quantity prescribed must be greater than zero.", "retryable": False, "category": "Validation"},
    {"id": "ERR-RX-010", "status": 500, "domain": "Prescription", "code": "RX_DIGITAL_SIGNATURE_FAILED", "message": "Failed to generate cryptographic prescription integrity signature.", "retryable": True, "category": "System"},

    # Pharmacy & Dispensing Errors (ERR-PHARM-001 to ERR-PHARM-010)
    {"id": "ERR-PHARM-001", "status": 404, "domain": "Pharmacy", "code": "PHARM_BATCH_NOT_FOUND", "message": "Allocated pharmaceutical batch identifier does not exist in dispensary.", "retryable": False, "category": "NotFound"},
    {"id": "ERR-PHARM-002", "status": 409, "domain": "Pharmacy", "code": "PHARM_BATCH_EXPIRED", "message": "Selected drug batch has reached its expiration date and cannot be dispensed.", "retryable": False, "category": "ClinicalSafety"},
    {"id": "ERR-PHARM-003", "status": 409, "domain": "Pharmacy", "code": "PHARM_INSUFFICIENT_STOCK", "message": "Requested quantity exceeds available on-hand batch balance in clinic.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-PHARM-004", "status": 400, "domain": "Pharmacy", "code": "PHARM_FEFO_VIOLATION", "message": "Earlier-expiring batch exists in dispensary; FEFO allocation enforced.", "retryable": False, "category": "BusinessRule"},
    {"id": "ERR-PHARM-005", "status": 403, "domain": "Pharmacy", "code": "PHARM_PHARMACIST_ROLE_REQUIRED", "message": "Dispensation requires registered pharmacist credential and role.", "retryable": False, "category": "Authorization"},
    {"id": "ERR-PHARM-006", "status": 409, "domain": "Pharmacy", "code": "PHARM_DISPENSE_ALREADY_FINALIZED", "message": "Prescription items have already been fully dispensed.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-PHARM-007", "status": 400, "domain": "Pharmacy", "code": "PHARM_SUBSTITUTION_UNAUTHORIZED", "message": "Therapeutic generic substitution requires prior prescriber consultation.", "retryable": False, "category": "ClinicalSafety"},
    {"id": "ERR-PHARM-008", "status": 400, "domain": "Pharmacy", "code": "PHARM_REVERSAL_EXPIRED", "message": "Dispensation cannot be reversed after 24 hours of issue.", "retryable": False, "category": "BusinessRule"},
    {"id": "ERR-PHARM-009", "status": 409, "domain": "Pharmacy", "code": "PHARM_STOCK_LOCKED", "message": "Dispensary stock currently locked for annual municipal physical inventory audit.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-PHARM-010", "status": 500, "domain": "Pharmacy", "code": "PHARM_LEDGER_POST_FAILED", "message": "Double-entry pharmacy stock movement ledger transaction failed.", "retryable": True, "category": "DatabaseFailure"},

    # Inventory Errors (ERR-INV-001 to ERR-INV-010)
    {"id": "ERR-INV-001", "status": 404, "domain": "Inventory", "code": "INV_DRUG_NOT_FOUND", "message": "Drug catalog item not found in master list.", "retryable": False, "category": "NotFound"},
    {"id": "ERR-INV-002", "status": 400, "domain": "Inventory", "code": "INV_BATCH_NUMBER_DUPLICATE", "message": "Batch number already exists for this manufacturer and drug.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-INV-003", "status": 400, "domain": "Inventory", "code": "INV_EXPIRY_DATE_PAST", "message": "Receipt rejected: batch expiration date has already elapsed.", "retryable": False, "category": "Validation"},
    {"id": "ERR-INV-004", "status": 400, "domain": "Inventory", "code": "INV_EXPIRY_UNDER_6_MONTHS", "message": "Receipt rejected: shelf life remaining is under statutory 6-month depot minimum.", "retryable": False, "category": "BusinessRule"},
    {"id": "ERR-INV-005", "status": 403, "domain": "Inventory", "code": "INV_ADJUSTMENT_SUPERVISOR_REQUIRED", "message": "Stock write-off or shrinkage adjustment requires supervisor approval token.", "retryable": False, "category": "Authorization"},
    {"id": "ERR-INV-006", "status": 409, "domain": "Inventory", "code": "INV_INDENT_ALREADY_FULFILLED", "message": "Drug indent requisition has already been fulfilled or closed.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-INV-007", "status": 400, "domain": "Inventory", "code": "INV_COLD_CHAIN_TEMPERATURE_BREACH", "message": "Cold chain vaccine receipt rejected: temperature breached +2C to +8C threshold.", "retryable": False, "category": "ClinicalSafety"},
    {"id": "ERR-INV-008", "status": 400, "domain": "Inventory", "code": "INV_QUANTITY_NEGATIVE", "message": "Stock receipt quantity must be a strictly positive integer.", "retryable": False, "category": "Validation"},
    {"id": "ERR-INV-009", "status": 409, "domain": "Inventory", "code": "INV_STOCK_COUNT_MISMATCH", "message": "Physical audit count conflicts with concurrent dispensation in progress.", "retryable": True, "category": "Concurrency"},
    {"id": "ERR-INV-010", "status": 500, "domain": "Inventory", "code": "INV_WAREHOUSE_SYNC_FAILED", "message": "Failed to synchronize clinic stock ledger with central BBMP depot.", "retryable": True, "category": "IntegrationFailure"},

    # Lab Errors (ERR-LAB-001 to ERR-LAB-008)
    {"id": "ERR-LAB-001", "status": 404, "domain": "Lab", "code": "LAB_ORDER_NOT_FOUND", "message": "Diagnostic laboratory test order not found.", "retryable": False, "category": "NotFound"},
    {"id": "ERR-LAB-002", "status": 400, "domain": "Lab", "code": "LAB_TEST_UNAVAILABLE_AT_CLINIC", "message": "Requested rapid test is not configured in this Namma Clinic tier.", "retryable": False, "category": "BusinessRule"},
    {"id": "ERR-LAB-003", "status": 409, "domain": "Lab", "code": "LAB_RESULT_ALREADY_SUBMITTED", "message": "Test result has already been recorded and validated.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-LAB-004", "status": 400, "domain": "Lab", "code": "LAB_SPECIMEN_REJECTED", "message": "Specimen rejected by lab technician; recollecting sample required.", "retryable": False, "category": "BusinessRule"},
    {"id": "ERR-LAB-005", "status": 403, "domain": "Lab", "code": "LAB_TECHNICIAN_ROLE_REQUIRED", "message": "Result entry requires registered laboratory technician role.", "retryable": False, "category": "Authorization"},
    {"id": "ERR-LAB-006", "status": 400, "domain": "Lab", "code": "LAB_VALUE_OUT_OF_RANGE", "message": "Reported quantitative value exceeds machine calibration boundaries.", "retryable": False, "category": "Validation"},
    {"id": "ERR-LAB-007", "status": 400, "domain": "Lab", "code": "LAB_BARCODE_ALREADY_USED", "message": "Specimen barcode identifier has already been bound to another accession.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-LAB-008", "status": 500, "domain": "Lab", "code": "LAB_ANALYZER_INTERFACE_DOWN", "message": "Direct point-of-care rapid analyzer serial interface failed.", "retryable": True, "category": "IntegrationFailure"},

    # Referral Errors (ERR-REF-001 to ERR-REF-006)
    {"id": "ERR-REF-001", "status": 404, "domain": "Referral", "code": "REF_NOT_FOUND", "message": "Hospital referral dossier does not exist.", "retryable": False, "category": "NotFound"},
    {"id": "ERR-REF-002", "status": 400, "domain": "Referral", "code": "REF_DESTINATION_HOSPITAL_INVALID", "message": "Destination facility must be an accredited secondary or tertiary hospital.", "retryable": False, "category": "Validation"},
    {"id": "ERR-REF-003", "status": 409, "domain": "Referral", "code": "REF_ALREADY_ACCEPTED", "message": "Referral has already been accepted by receiving secondary hospital.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-REF-004", "status": 400, "domain": "Referral", "code": "REF_EMERGENCY_AMBULANCE_REQUIRED", "message": "Emergency referrals require 108 ambulance dispatch confirmation or override reason.", "retryable": False, "category": "ClinicalSafety"},
    {"id": "ERR-REF-005", "status": 403, "domain": "Referral", "code": "REF_DOCTOR_AUTHORIZATION_REQUIRED", "message": "Only attending medical officers may initiate outward hospital referrals.", "retryable": False, "category": "Authorization"},
    {"id": "ERR-REF-006", "status": 500, "domain": "Referral", "code": "REF_EMS_BRIDGE_UNAVAILABLE", "message": "State 108 ambulance dispatch telemetry API gateway unreachable.", "retryable": True, "category": "IntegrationFailure"},

    # Notification Errors (ERR-NOTIF-001 to ERR-NOTIF-006)
    {"id": "ERR-NOTIF-001", "status": 400, "domain": "Notification", "code": "NOTIF_PHONE_CONSENT_OPT_OUT", "message": "Citizen has opted out of automated promotional or advisory notifications.", "retryable": False, "category": "Privacy"},
    {"id": "ERR-NOTIF-002", "status": 404, "domain": "Notification", "code": "NOTIF_TEMPLATE_NOT_FOUND", "message": "DLT approved notification template ID is not configured.", "retryable": False, "category": "NotFound"},
    {"id": "ERR-NOTIF-003", "status": 429, "domain": "Notification", "code": "NOTIF_RATE_LIMIT_EXCEEDED", "message": "Citizen has received maximum allowable SMS alerts today (5 messages).", "retryable": False, "category": "RateLimiting"},
    {"id": "ERR-NOTIF-004", "status": 400, "domain": "Notification", "code": "NOTIF_TEMPLATE_PARAM_MISMATCH", "message": "Provided template variable bindings do not match registered template spec.", "retryable": False, "category": "Validation"},
    {"id": "ERR-NOTIF-005", "status": 502, "domain": "Notification", "code": "NOTIF_SMS_GATEWAY_FAILURE", "message": "State C-DAC / Telecom carrier SMS gateway returned upstream error.", "retryable": True, "category": "IntegrationFailure"},
    {"id": "ERR-NOTIF-006", "status": 504, "domain": "Notification", "code": "NOTIF_CARRIER_TIMEOUT", "message": "Carrier dispatch delivery confirmation timed out.", "retryable": True, "category": "Timeout"},

    # Analytics Errors (ERR-ANALYTICS-001 to ERR-ANALYTICS-006)
    {"id": "ERR-ANALYTICS-001", "status": 400, "domain": "Analytics", "code": "ANL_DATE_RANGE_TOO_BROAD", "message": "Real-time analytics query interval exceeds maximum 365-day range.", "retryable": False, "category": "Validation"},
    {"id": "ERR-ANALYTICS-002", "status": 403, "domain": "Analytics", "code": "ANL_INDIVIDUAL_PII_PROHIBITED", "message": "Analytical queries cannot return identifiable citizen health records.", "retryable": False, "category": "Privacy"},
    {"id": "ERR-ANALYTICS-003", "status": 400, "domain": "Analytics", "code": "ANL_INVALID_METRIC_NAME", "message": "Requested KPI metric is not in authoritative measure catalog.", "retryable": False, "category": "Validation"},
    {"id": "ERR-ANALYTICS-004", "status": 403, "domain": "Analytics", "code": "ANL_ZONE_RESTRICTION", "message": "User is not authorized to view municipal analytics for the requested zone.", "retryable": False, "category": "Authorization"},
    {"id": "ERR-ANALYTICS-005", "status": 504, "domain": "Analytics", "code": "ANL_CLICKHOUSE_TIMEOUT", "message": "Columnar analytical warehouse query execution exceeded 10-second deadline.", "retryable": True, "category": "Timeout"},
    {"id": "ERR-ANALYTICS-006", "status": 500, "domain": "Analytics", "code": "ANL_AGGREGATION_ENGINE_FAULT", "message": "Materialized view refresh in analytical warehouse failed.", "retryable": True, "category": "System"},

    # Audit Errors (ERR-AUDIT-001 to ERR-AUDIT-006)
    {"id": "ERR-AUDIT-001", "status": 403, "domain": "Audit", "code": "AUDIT_MUTATION_PROHIBITED", "message": "WORM compliance violation: audit records are immutable and cannot be edited or deleted.", "retryable": False, "category": "Security"},
    {"id": "ERR-AUDIT-002", "status": 403, "domain": "Audit", "code": "AUDIT_OFFICER_ROLE_REQUIRED", "message": "Access to immutable audit logs requires Security & Data Privacy Officer role.", "retryable": False, "category": "Authorization"},
    {"id": "ERR-AUDIT-003", "status": 400, "domain": "Audit", "code": "AUDIT_QUERY_WINDOW_EXCEEDED", "message": "Audit log search window exceeds maximum 31-day search interval.", "retryable": False, "category": "Validation"},
    {"id": "ERR-AUDIT-004", "status": 500, "domain": "Audit", "code": "AUDIT_HASH_CHAIN_MISMATCH", "message": "CRITICAL: Cryptographic HMAC SHA-256 ledger tamper detected on verification.", "retryable": False, "category": "Security"},
    {"id": "ERR-AUDIT-005", "status": 404, "domain": "Audit", "code": "AUDIT_RECORD_NOT_FOUND", "message": "Audit log entry not found.", "retryable": False, "category": "NotFound"},
    {"id": "ERR-AUDIT-006", "status": 500, "domain": "Audit", "code": "AUDIT_LEDGER_WRITE_FAILED", "message": "Failed to append record to immutable cryptographic audit log.", "retryable": True, "category": "DatabaseFailure"},

    # ABDM Errors (ERR-ABDM-001 to ERR-ABDM-008)
    {"id": "ERR-ABDM-001", "status": 400, "domain": "ABDM", "code": "ABDM_ABHA_INVALID", "message": "14-digit ABHA number fails Luhn checksum or format validation.", "retryable": False, "category": "Validation"},
    {"id": "ERR-ABDM-002", "status": 401, "domain": "ABDM", "code": "ABDM_OTP_INVALID", "message": "OTP entered for ABHA authentication is incorrect or expired.", "retryable": False, "category": "Authentication"},
    {"id": "ERR-ABDM-003", "status": 400, "domain": "ABDM", "code": "ABDM_FHIR_VALIDATION_FAILED", "message": "Clinical document bundle does not conform to ABDM FHIR R4 profile specifications.", "retryable": False, "category": "Validation"},
    {"id": "ERR-ABDM-004", "status": 403, "domain": "ABDM", "code": "ABDM_CONSENT_EXPIRED", "message": "ABDM electronic consent artifact has expired or been revoked by citizen.", "retryable": False, "category": "Privacy"},
    {"id": "ERR-ABDM-005", "status": 502, "domain": "ABDM", "code": "ABDM_GATEWAY_UNAVAILABLE", "message": "National Health Authority (NHA) ABDM gateway unreachable or returning 5xx.", "retryable": True, "category": "IntegrationFailure"},
    {"id": "ERR-ABDM-006", "status": 504, "domain": "ABDM", "code": "ABDM_TIMEOUT", "message": "External ABDM gateway callback timed out.", "retryable": True, "category": "Timeout"},
    {"id": "ERR-ABDM-007", "status": 400, "domain": "ABDM", "code": "ABDM_HIP_LINK_FAILED", "message": "Failed to register care context with ABDM HIP registry.", "retryable": True, "category": "IntegrationFailure"},
    {"id": "ERR-ABDM-008", "status": 403, "domain": "ABDM", "code": "ABDM_HIP_CREDENTIALS_INVALID", "message": "Municipal Namma Clinic ABDM HIP client credentials rejected by NHA.", "retryable": False, "category": "Security"},

    # Portability Errors (ERR-PORT-001 to ERR-PORT-006)
    {"id": "ERR-PORT-001", "status": 404, "domain": "Portability", "code": "PORT_JOB_NOT_FOUND", "message": "Data portability export task identifier does not exist.", "retryable": False, "category": "NotFound"},
    {"id": "ERR-PORT-002", "status": 409, "domain": "Portability", "code": "PORT_JOB_IN_PROGRESS", "message": "A data export job is already running for this citizen.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-PORT-003", "status": 410, "domain": "Portability", "code": "PORT_DOWNLOAD_LINK_EXPIRED", "message": "Pre-signed download link has expired (30-minute validity window elapsed).", "retryable": False, "category": "Security"},
    {"id": "ERR-PORT-004", "status": 403, "domain": "Portability", "code": "PORT_UNAUTHORIZED_CLAIMANT", "message": "Export download permitted only by verified citizen or legal guardian.", "retryable": False, "category": "Privacy"},
    {"id": "ERR-PORT-005", "status": 500, "domain": "Portability", "code": "PORT_ARCHIVE_GENERATION_FAILED", "message": "Background job failed to package encrypted export archive.", "retryable": True, "category": "System"},
    {"id": "ERR-PORT-006", "status": 400, "domain": "Portability", "code": "PORT_INVALID_EXPORT_FORMAT", "message": "Requested export format must be FHIR_JSON, NDJSON, CSV_ZIP, or PDF_ENCRYPTED.", "retryable": False, "category": "Validation"},

    # System & Cross-Cutting Errors (ERR-SYS-001 to ERR-SYS-020)
    {"id": "ERR-SYS-001", "status": 400, "domain": "System", "code": "SYS_PAYLOAD_MALFORMED", "message": "Request body contains malformed JSON or unparseable syntax.", "retryable": False, "category": "Validation"},
    {"id": "ERR-SYS-002", "status": 400, "domain": "System", "code": "SYS_REQUIRED_HEADER_MISSING", "message": "Mandatory HTTP header (e.g., X-Correlation-ID) is missing.", "retryable": False, "category": "Validation"},
    {"id": "ERR-SYS-003", "status": 400, "domain": "System", "code": "SYS_IDEMPOTENCY_KEY_INVALID", "message": "X-Idempotency-Key header must be a valid UUIDv7 format.", "retryable": False, "category": "Validation"},
    {"id": "ERR-SYS-004", "status": 409, "domain": "System", "code": "SYS_IDEMPOTENCY_CONFLICT", "message": "Idempotency key previously used with a differing request payload.", "retryable": False, "category": "Conflict"},
    {"id": "ERR-SYS-005", "status": 412, "domain": "System", "code": "SYS_PRECONDITION_FAILED", "message": "If-Match ETag header does not match current resource version.", "retryable": False, "category": "Concurrency"},
    {"id": "ERR-SYS-006", "status": 429, "domain": "System", "code": "SYS_RATE_LIMIT_EXCEEDED", "message": "API request quota exceeded. Back off and retry after indicated window.", "retryable": True, "category": "RateLimiting"},
    {"id": "ERR-SYS-007", "status": 503, "domain": "System", "code": "SYS_CIRCUIT_BREAKER_OPEN", "message": "Downstream service circuit breaker is open due to consecutive failures.", "retryable": True, "category": "DependencyFailure"},
    {"id": "ERR-SYS-008", "status": 504, "domain": "System", "code": "SYS_GATEWAY_TIMEOUT", "message": "Upstream microservice or database operation timed out.", "retryable": True, "category": "Timeout"},
    {"id": "ERR-SYS-009", "status": 500, "domain": "System", "code": "SYS_DATABASE_CONNECTION_POOL_EXHAUSTED", "message": "Relational database connection pool is saturated.", "retryable": True, "category": "DatabaseFailure"},
    {"id": "ERR-SYS-010", "status": 500, "domain": "System", "code": "SYS_TRANSACTION_DEADLOCK_DETECTED", "message": "PostgreSQL transaction deadlock detected; transaction rolled back.", "retryable": True, "category": "DatabaseFailure"},
    {"id": "ERR-SYS-011", "status": 409, "domain": "System", "code": "SYS_SYNC_VECTOR_CONFLICT", "message": "Edge-cloud synchronization vector clock conflict requires resolution.", "retryable": True, "category": "OfflineSync"},
    {"id": "ERR-SYS-012", "status": 400, "domain": "System", "code": "SYS_SYNC_TOMBSTONE_CONFLICT", "message": "Attempt to mutate a row that has already been tombstoned on cloud.", "retryable": False, "category": "OfflineSync"},
    {"id": "ERR-SYS-013", "status": 413, "domain": "System", "code": "SYS_PAYLOAD_TOO_LARGE", "message": "Request payload exceeds statutory 10MB API gateway size limit.", "retryable": False, "category": "Validation"},
    {"id": "ERR-SYS-014", "status": 415, "domain": "System", "code": "SYS_UNSUPPORTED_MEDIA_TYPE", "message": "Content-Type header must be application/json or application/json+fhir.", "retryable": False, "category": "Validation"},
    {"id": "ERR-SYS-015", "status": 406, "domain": "System", "code": "SYS_NOT_ACCEPTABLE", "message": "Server cannot produce response matching requested Accept header.", "retryable": False, "category": "Validation"},
    {"id": "ERR-SYS-016", "status": 503, "domain": "System", "code": "SYS_MAINTENANCE_MODE", "message": "Platform is undergoing scheduled municipal database maintenance window.", "retryable": True, "category": "System"},
    {"id": "ERR-SYS-017", "status": 500, "domain": "System", "code": "SYS_INTERNAL_SERVER_ERROR", "message": "An unexpected internal server error occurred. Reference correlation ID for audit.", "retryable": True, "category": "System"},
    {"id": "ERR-SYS-018", "status": 400, "domain": "System", "code": "SYS_VERSION_UNSUPPORTED", "message": "Requested API major version has been sunset and retired.", "retryable": False, "category": "Versioning"},
    {"id": "ERR-SYS-019", "status": 400, "domain": "System", "code": "SYS_FIELD_EXPANSION_INVALID", "message": "Requested relation expansion exceeds maximum depth (max 2 levels).", "retryable": False, "category": "Validation"},
    {"id": "ERR-SYS-020", "status": 500, "domain": "System", "code": "SYS_ENCRYPTION_ENGINE_FAULT", "message": "Column-level envelope encryption failed to unwrap ciphertext.", "retryable": True, "category": "Security"}
]

ERROR_CODE_MAP = {e["id"]: e for e in API_ERROR_CODES}
ERROR_MACHINE_CODE_MAP = {e["code"]: e for e in API_ERROR_CODES}

if __name__ == "__main__":
    print(f"Loaded {len(API_SCHEMAS)} API Schemas.")
    print(f"Loaded {len(API_ERROR_CODES)} Standard Error Codes.")
