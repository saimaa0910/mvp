"""
db_columns.py
Canonical definitions for 832 Columns across all 52 Relational Tables (COLUMN-001 to COLUMN-832).
Provides comprehensive technical, operational, security, and lineage attributes for every column.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from typing import List, Dict, Any
from scripts.database.db_tables_entities import TABLES, TABLE_MAP

# -----------------------------------------------------------------------------
# SPECIFICATION TEMPLATES FOR 52 TABLES (16 COLUMNS PER TABLE = 832 COLUMNS)
# -----------------------------------------------------------------------------

TABLE_COLUMN_SPECS: Dict[str, List[Dict[str, Any]]] = {
    # -------------------------------------------------------------------------
    # DOMAIN 1: IDENTITY & CORE GOVERNANCE (TABLE-001 to TABLE-012)
    # -------------------------------------------------------------------------
    "auth_users": [
        {"name": "id", "type": "UUID", "len": "128-bit", "null": False, "def": "gen_random_uuid()", "gen": "NONE", "key": "PK", "uniq": True, "val": "UUIDv7 compliant format", "allowed": "Valid UUID", "class": "CLASS-004", "pii": True, "phi": False, "enc": "NONE", "mask": "None", "biz": "Unique immutable system identifier for user account", "tech": "Primary key surrogate identifier using UUIDv7 for temporal index clustering"},
        {"name": "username", "type": "VARCHAR(64)", "len": "64", "null": False, "def": None, "gen": "NONE", "key": "NONE", "uniq": True, "val": "^[a-z0-9_.]{4,64}$", "allowed": "Alphanumeric, dot, underscore", "class": "CLASS-004", "pii": True, "phi": False, "enc": "NONE", "mask": "None", "biz": "Unique staff login handle", "tech": "Case-insensitive unique login identifier for authentication lookup"},
        {"name": "email", "type": "VARCHAR(255)", "len": "255", "null": False, "def": None, "gen": "NONE", "key": "NONE", "uniq": True, "val": "RFC 5322 email regex", "allowed": "Valid email address", "class": "CLASS-004", "pii": True, "phi": False, "enc": "Blind Index (HMAC-SHA256)", "mask": "u***@domain.com", "biz": "Official governmental email address", "tech": "Indexed email with cryptographic blind index for privacy-preserving lookups"},
        {"name": "phone_number", "type": "VARCHAR(20)", "len": "20", "null": False, "def": None, "gen": "NONE", "key": "NONE", "uniq": True, "val": "^\\+91[6-9]\\d{9}$", "allowed": "E.164 format (+91)", "class": "CLASS-004", "pii": True, "phi": False, "enc": "AES-256-GCM Column", "mask": "+91-XXXXX-12345", "biz": "Registered mobile phone for MFA and emergency alerts", "tech": "Encrypted mobile number; searchable via blind index hmac_phone"},
        {"name": "phone_blind_index", "type": "VARCHAR(64)", "len": "64", "null": False, "def": None, "gen": "NONE", "key": "NONE", "uniq": True, "val": "^[a-f0-9]{64}$", "allowed": "SHA-256 hex string", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Deterministic hash for mobile lookup without decrypting", "tech": "HMAC-SHA256 hash using KMS-rotated pepper key for exact match querying"},
        {"name": "first_name", "type": "VARCHAR(100)", "len": "100", "null": False, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "1-100 characters", "allowed": "Unicode text", "class": "CLASS-004", "pii": True, "phi": False, "enc": "AES-256-GCM Column", "mask": "First char + asterisks", "biz": "Staff legal first name", "tech": "Encrypted text field storing verified first name"},
        {"name": "last_name", "type": "VARCHAR(100)", "len": "100", "null": False, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "1-100 characters", "allowed": "Unicode text", "class": "CLASS-004", "pii": True, "phi": False, "enc": "AES-256-GCM Column", "mask": "First char + asterisks", "biz": "Staff legal surname", "tech": "Encrypted text field storing verified last name"},
        {"name": "user_type", "type": "VARCHAR(32)", "len": "32", "null": False, "def": "'CLINICAL'", "gen": "NONE", "key": "NONE", "uniq": False, "val": "IN ('CLINICAL', 'ADMIN', 'PARAMEDICAL', 'INTEGRATION')", "allowed": "Enum values", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Broad organizational role category", "tech": "Categorical string for top-level access routing and security policy application"},
        {"name": "account_status", "type": "VARCHAR(32)", "len": "32", "null": False, "def": "'PENDING_ACTIVATION'", "gen": "NONE", "key": "NONE", "uniq": False, "val": "IN ('ACTIVE', 'SUSPENDED', 'LOCKED', 'DEACTIVATED', 'PENDING_ACTIVATION')", "allowed": "Enum values", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Current account operational lifecycle status", "tech": "State machine transition status; checked on every JWT issuance"},
        {"name": "primary_facility_id", "type": "UUID", "len": "128-bit", "null": True, "def": None, "gen": "NONE", "key": "FK", "uniq": False, "val": "Valid facility UUID", "allowed": "UUID referencing facilities.id", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Home clinic or office where staff is permanently posted", "tech": "Foreign key referencing facilities.id with ON DELETE RESTRICT"},
        {"name": "failed_login_count", "type": "INTEGER", "len": "32-bit", "null": False, "def": "0", "gen": "NONE", "key": "NONE", "uniq": False, "val": ">= 0", "allowed": "Non-negative integer", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Consecutive incorrect authentication attempts", "tech": "Counter reset on success; triggers account lock at threshold (5)"},
        {"name": "lockout_until", "type": "TIMESTAMPTZ", "len": "64-bit", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "Valid UTC timestamp", "allowed": "ISO 8601 UTC timestamp", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Timestamp until which login attempts are rejected", "tech": "Lockout expiry timestamp for brute-force mitigation"},
        {"name": "mfa_enabled", "type": "BOOLEAN", "len": "1-byte", "null": False, "def": "true", "gen": "NONE", "key": "NONE", "uniq": False, "val": "true or false", "allowed": "Boolean", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Mandatory two-factor authentication flag", "tech": "Enforces second factor challenge during session negotiation"},
        {"name": "created_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": False, "def": "clock_timestamp()", "gen": "NONE", "key": "NONE", "uniq": False, "val": "Valid UTC timestamp", "allowed": "ISO 8601 UTC timestamp", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Record creation timestamp", "tech": "Immutable audit creation timestamp in microsecond UTC precision"},
        {"name": "updated_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": False, "def": "clock_timestamp()", "gen": "NONE", "key": "NONE", "uniq": False, "val": "Valid UTC timestamp", "allowed": "ISO 8601 UTC timestamp", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Record last modification timestamp", "tech": "Trigger-managed update timestamp"},
        {"name": "deleted_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "Valid UTC timestamp", "allowed": "ISO 8601 UTC timestamp", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Soft-deletion timestamp", "tech": "Timestamp indicating account retirement without physical tuple removal"}
    ],

    "user_credentials": [
        {"name": "id", "type": "UUID", "len": "128-bit", "null": False, "def": "gen_random_uuid()", "gen": "NONE", "key": "PK", "uniq": True, "val": "UUIDv7", "allowed": "UUID", "class": "CLASS-005", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Surrogate primary key for credentials", "tech": "UUIDv7 primary key"},
        {"name": "user_id", "type": "UUID", "len": "128-bit", "null": False, "def": None, "gen": "NONE", "key": "FK", "uniq": True, "val": "Valid user UUID", "allowed": "UUID referencing auth_users.id", "class": "CLASS-005", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Foreign key to owning user record", "tech": "Unique foreign key to auth_users.id with CASCADE DELETE"},
        {"name": "password_hash", "type": "VARCHAR(255)", "len": "255", "null": False, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "^\\$argon2id\\$v=19\\$.*", "allowed": "Argon2id formatted string", "class": "CLASS-005", "pii": False, "phi": False, "enc": "Argon2id Cryptographic Hash", "mask": "Full Redaction", "biz": "Cryptographically hashed user password", "tech": "Argon2id hash with m=65536, t=3, p=4 parameters"},
        {"name": "password_salt", "type": "VARCHAR(64)", "len": "64", "null": False, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "32-byte hex salt", "allowed": "Cryptographic random salt", "class": "CLASS-005", "pii": False, "phi": False, "enc": "KMS Secret", "mask": "Full Redaction", "biz": "Per-user unique cryptographic salt", "tech": "Random 32-byte cryptographic salt generated via CSPRNG"},
        {"name": "mfa_secret_encrypted", "type": "BYTEA", "len": "Variable", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "Valid ciphertext", "allowed": "Encrypted byte array", "class": "CLASS-005", "pii": False, "phi": False, "enc": "Envelope KMS (AES-256-GCM)", "mask": "Full Redaction", "biz": "Encrypted TOTP secret key for Authenticator apps", "tech": "AES-256-GCM envelope-encrypted TOTP seed with KMS data key"},
        {"name": "mfa_backup_codes_hash", "type": "JSONB", "len": "Variable", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "Valid JSON array of hashes", "allowed": "JSON array of SHA-256 hashes", "class": "CLASS-005", "pii": False, "phi": False, "enc": "SHA-256 Hashes", "mask": "Full Redaction", "biz": "One-time emergency backup recovery codes", "tech": "Array of salted hashes for emergency account access"},
        {"name": "password_changed_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": False, "def": "clock_timestamp()", "gen": "NONE", "key": "NONE", "uniq": False, "val": "Valid UTC timestamp", "allowed": "ISO 8601 UTC timestamp", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Timestamp of last password change", "tech": "Used to enforce 90-day password rotation policy"},
        {"name": "force_password_reset", "type": "BOOLEAN", "len": "1-byte", "null": False, "def": "true", "gen": "NONE", "key": "NONE", "uniq": False, "val": "true or false", "allowed": "Boolean", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Flag forcing user to reset password on next login", "tech": "Set to true for first login or security administrative reset"},
        {"name": "failed_mfa_count", "type": "INTEGER", "len": "32-bit", "null": False, "def": "0", "gen": "NONE", "key": "NONE", "uniq": False, "val": ">= 0", "allowed": "Non-negative integer", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Count of consecutive invalid MFA token entries", "tech": "Triggers step-up authentication or temporary MFA lock"},
        {"name": "security_stamp", "type": "VARCHAR(64)", "len": "64", "null": False, "def": "gen_random_uuid()::text", "gen": "NONE", "key": "NONE", "uniq": False, "val": "Valid random string", "allowed": "Unique string", "class": "CLASS-005", "pii": False, "phi": False, "enc": "NONE", "mask": "Full Redaction", "biz": "Token invalidation stamp", "tech": "Regenerated on credential update to invalidate all active JWTs immediately"},
        {"name": "argon2_memory_cost", "type": "INTEGER", "len": "32-bit", "null": False, "def": "65536", "gen": "NONE", "key": "NONE", "uniq": False, "val": ">= 65536", "allowed": "Integer in KiB", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Cryptographic work factor memory parameter", "tech": "Stored to enable seamless algorithm parameter upgrades"},
        {"name": "argon2_time_cost", "type": "INTEGER", "len": "32-bit", "null": False, "def": "3", "gen": "NONE", "key": "NONE", "uniq": False, "val": ">= 3", "allowed": "Positive integer", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Cryptographic work factor iteration parameter", "tech": "Argon2 iteration count"},
        {"name": "argon2_parallelism", "type": "INTEGER", "len": "32-bit", "null": False, "def": "4", "gen": "NONE", "key": "NONE", "uniq": False, "val": ">= 1", "allowed": "Positive integer", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Cryptographic work factor thread parameter", "tech": "Argon2 thread parallelism parameter"},
        {"name": "created_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": False, "def": "clock_timestamp()", "gen": "NONE", "key": "NONE", "uniq": False, "val": "Valid UTC timestamp", "allowed": "ISO 8601 UTC timestamp", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Record creation timestamp", "tech": "Immutable audit creation timestamp"},
        {"name": "updated_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": False, "def": "clock_timestamp()", "gen": "NONE", "key": "NONE", "uniq": False, "val": "Valid UTC timestamp", "allowed": "ISO 8601 UTC timestamp", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Record modification timestamp", "tech": "Audit update timestamp"},
        {"name": "deleted_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "Valid UTC timestamp", "allowed": "ISO 8601 UTC timestamp", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Soft-deletion timestamp", "tech": "Credential purge timestamp"}
    ]
}

# Generic generator for remaining tables to ensure full coverage of 52 tables x 16 columns = 832 columns
def generate_standard_columns_for_table(tbl: Dict[str, Any]) -> List[Dict[str, Any]]:
    tname = tbl["name"]
    tid = tbl["id"]
    domain = tbl["domain"]
    cls_tier = tbl["classification"]
    ret = tbl["retention"]
    
    # Check if specific template exists
    if tname in TABLE_COLUMN_SPECS:
        return TABLE_COLUMN_SPECS[tname]
        
    cols = []
    # 1. Primary Key
    cols.append({
        "name": "id", "type": "UUID", "len": "128-bit", "null": False, "def": "gen_random_uuid()",
        "gen": "NONE", "key": "PK", "uniq": True, "val": "UUIDv7 format", "allowed": "Valid UUID",
        "class": cls_tier, "pii": False, "phi": False, "enc": "NONE", "mask": "None",
        "biz": f"Surrogate primary key for {tname}", "tech": "Clustered UUIDv7 identifier for high-throughput write performance"
    })
    
    # 2. Facility / Tenant Scope (if applicable) or Parent Reference
    if tname in ["facilities"]:
        cols.append({"name": "facility_code", "type": "VARCHAR(32)", "len": "32", "null": False, "def": None, "gen": "NONE", "key": "NONE", "uniq": True, "val": "^BLR-[A-Z]{2,4}-\\d{3}$", "allowed": "Alphanumeric code", "class": "CLASS-001", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Government facility registration code", "tech": "Unique natural key for clinic identification"})
        cols.append({"name": "facility_name", "type": "VARCHAR(255)", "len": "255", "null": False, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "1-255 chars", "allowed": "Text", "class": "CLASS-001", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Official clinic public name", "tech": "Display name used across UI and reports"})
        cols.append({"name": "ward_number", "type": "INTEGER", "len": "32-bit", "null": False, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "1 to 243", "allowed": "Integer 1-243", "class": "CLASS-001", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "BBMP administrative ward number", "tech": "Indexed integer for spatial and administrative filtering"})
        cols.append({"name": "zone_name", "type": "VARCHAR(64)", "len": "64", "null": False, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "IN ('EAST', 'WEST', 'SOUTH', 'BOMMANAHALLI', 'DASARAHALLI', 'MAHADEVAPURA', 'RR_NAGARA', 'YELAHANKA')", "allowed": "Enum zone strings", "class": "CLASS-001", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "BBMP administrative zone", "tech": "Zonal partition key and regional aggregation attribute"})
        cols.append({"name": "facility_type", "type": "VARCHAR(32)", "len": "32", "null": False, "def": "'NAMMA_CLINIC'", "gen": "NONE", "key": "NONE", "uniq": False, "val": "IN ('NAMMA_CLINIC', 'UPHC', 'REFERRAL_HOSPITAL', 'DIAGNOSTIC_HUB')", "allowed": "Enum strings", "class": "CLASS-001", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Healthcare facility classification tier", "tech": "Type descriptor governing service catalog and staffing rules"})
        cols.append({"name": "latitude", "type": "NUMERIC(10, 7)", "len": "64-bit", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "12.0 to 13.5", "allowed": "Valid latitude in Bengaluru", "class": "CLASS-001", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "GPS geographic latitude", "tech": "WGS 84 coordinate for spatial queries"})
        cols.append({"name": "longitude", "type": "NUMERIC(10, 7)", "len": "64-bit", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "77.3 to 77.8", "allowed": "Valid longitude in Bengaluru", "class": "CLASS-001", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "GPS geographic longitude", "tech": "WGS 84 coordinate for spatial queries"})
        cols.append({"name": "hfr_id", "type": "VARCHAR(64)", "len": "64", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": True, "val": "^IN\\d{8,}$", "allowed": "ABDM HFR identifier", "class": "CLASS-001", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "National Health Facility Registry (HFR) identifier", "tech": "ABDM national registry identifier for digital health exchange"})
        cols.append({"name": "phone_contact", "type": "VARCHAR(20)", "len": "20", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "^\\+91\\d{10}$", "allowed": "E.164 phone", "class": "CLASS-001", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Public telephone contact number", "tech": "Official public inquiry helpline"})
        cols.append({"name": "is_active", "type": "BOOLEAN", "len": "1-byte", "null": False, "def": "true", "gen": "NONE", "key": "NONE", "uniq": False, "val": "true or false", "allowed": "Boolean", "class": "CLASS-001", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Operational active flag", "tech": "Soft activation toggle"})
        cols.append({"name": "operating_hours_json", "type": "JSONB", "len": "Variable", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "Valid JSON", "allowed": "JSON weekly schedule", "class": "CLASS-001", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Weekly working hours and shift schedules", "tech": "Structured JSON schedule format"})
        cols.append({"name": "ip_address_range", "type": "VARCHAR(64)", "len": "64", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "CIDR notation", "allowed": "IPv4/IPv6 CIDR", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Clinic local area network subnet", "tech": "Used for location-bound biometric clock-in and edge node authentication"})
        cols.append({"name": "created_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": False, "def": "clock_timestamp()", "gen": "NONE", "key": "NONE", "uniq": False, "val": "UTC timestamp", "allowed": "ISO 8601", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Record creation timestamp", "tech": "Audit timestamp"})
        cols.append({"name": "updated_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": False, "def": "clock_timestamp()", "gen": "NONE", "key": "NONE", "uniq": False, "val": "UTC timestamp", "allowed": "ISO 8601", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Last modification timestamp", "tech": "Trigger-updated timestamp"})
        cols.append({"name": "deleted_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "UTC timestamp", "allowed": "ISO 8601", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Decommission timestamp", "tech": "Soft-delete timestamp"})
        return cols

    # Domain specific structured columns for all other tables
    # Generate 15 rich columns per table to reach exactly 16 columns
    entity_prefix = tname.rstrip("s")
    cols.append({"name": f"{entity_prefix}_number" if "number" not in tname else "reference_code", "type": "VARCHAR(64)", "len": "64", "null": False, "def": None, "gen": "NONE", "key": "NONE", "uniq": True, "val": "Alphanumeric tracking code", "allowed": "Format string", "class": cls_tier, "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": f"Human-readable tracking identifier for {tname}", "tech": "Unique business tracking number"})
    
    # Facility Linkage
    cols.append({"name": "facility_id", "type": "UUID", "len": "128-bit", "null": False, "def": None, "gen": "NONE", "key": "FK", "uniq": False, "val": "Valid UUID", "allowed": "facilities.id", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Clinic facility where event or entity originated", "tech": "Foreign key referencing facilities.id with ON DELETE RESTRICT"})
    
    # Patient Linkage if clinical / intake / continuity
    if domain in ["Citizen Demographics", "Consent Management", "Queue Management", "Clinical Triage", "Clinical Safety", "Clinical Consultation", "Pharmacy & Prescribing", "Diagnostic Services", "Telemedicine", "Continuity of Care", "Chronic Disease Management", "Citizen Engagement", "Citizen Grievance & Feedback"]:
        cols.append({"name": "patient_id", "type": "UUID", "len": "128-bit", "null": False, "def": None, "gen": "NONE", "key": "FK", "uniq": False, "val": "Valid UUID", "allowed": "patients.id", "class": "CLASS-004", "pii": True, "phi": True, "enc": "NONE", "mask": "None", "biz": "Registered citizen receiving healthcare services", "tech": "Foreign key referencing patients.id with ON DELETE RESTRICT"})
    else:
        cols.append({"name": "created_by_user_id", "type": "UUID", "len": "128-bit", "null": True, "def": None, "gen": "NONE", "key": "FK", "uniq": False, "val": "Valid UUID", "allowed": "auth_users.id", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Staff member who created the record", "tech": "Foreign key referencing auth_users.id"})
        
    # Status / Category
    cols.append({"name": "status", "type": "VARCHAR(32)", "len": "32", "null": False, "def": "'ACTIVE'", "gen": "NONE", "key": "NONE", "uniq": False, "val": "Status Enum", "allowed": "ACTIVE, COMPLETED, CANCELLED, PENDING", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Operational workflow status", "tech": "State machine transition attribute"})
    
    # Type / Subcategory
    cols.append({"name": "category_type", "type": "VARCHAR(64)", "len": "64", "null": False, "def": "'STANDARD'", "gen": "NONE", "key": "NONE", "uniq": False, "val": "Classification string", "allowed": "Standard text category", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Domain classification category", "tech": "Categorical indexing attribute"})
    
    # Primary Data Payload (JSONB or Text)
    cols.append({"name": "clinical_payload_json" if "clinical" in domain.lower() or "triage" in domain.lower() else "metadata_json", "type": "JSONB", "len": "Variable", "null": True, "def": "'{}'::jsonb", "gen": "NONE", "key": "NONE", "uniq": False, "val": "Valid JSONB schema", "allowed": "JSON object", "class": cls_tier, "pii": cls_tier in ["CLASS-004", "CLASS-005"], "phi": cls_tier in ["CLASS-003", "CLASS-005"], "enc": "AES-256-GCM Column" if cls_tier == "CLASS-005" else "NONE", "mask": "Redacted" if cls_tier == "CLASS-005" else "None", "biz": "Detailed structured operational and clinical attributes", "tech": "Extensible JSONB document indexed with GIN"})
    
    # Quantitative measure or Priority
    cols.append({"name": "priority_score", "type": "INTEGER", "len": "32-bit", "null": False, "def": "1", "gen": "NONE", "key": "NONE", "uniq": False, "val": "1 to 5", "allowed": "Integer 1-5", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Operational priority or clinical severity score", "tech": "Numeric ordering attribute for queues and processing"})
    
    # Narrative remarks / Notes
    cols.append({"name": "operational_notes", "type": "TEXT", "len": "Variable", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "Text up to 4000 chars", "allowed": "Unicode text", "class": cls_tier, "pii": False, "phi": cls_tier in ["CLASS-003", "CLASS-005"], "enc": "NONE", "mask": "None", "biz": "Observations and qualitative remarks recorded by staff", "tech": "Unstructured narrative text"})
    
    # Offline sync sequence vector
    cols.append({"name": "sync_version", "type": "BIGINT", "len": "64-bit", "null": False, "def": "1", "gen": "NONE", "key": "NONE", "uniq": False, "val": ">= 1", "allowed": "Monotonic integer", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Optimistic locking and offline synchronization sequence number", "tech": "Monotonically increasing version counter for CRDT and conflict resolution"})
    
    # Edge device source linkage
    cols.append({"name": "edge_device_id", "type": "VARCHAR(64)", "len": "64", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "Device MAC or UUID", "allowed": "Alphanumeric string", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Hardware terminal or tablet identifier where entry occurred", "tech": "Traceability link to physical edge hardware"})
    
    # Cryptographic integrity signature
    cols.append({"name": "record_hash", "type": "VARCHAR(64)", "len": "64", "null": False, "def": "encode(sha256('init'::bytea), 'hex')", "gen": "NONE", "key": "NONE", "uniq": False, "val": "^[a-f0-9]{64}$", "allowed": "SHA-256 hex string", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Cryptographic tamper-detection checksum", "tech": "SHA-256 hash computed over row values for WORM verification"})
    
    # Verification timestamp
    cols.append({"name": "verified_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "UTC timestamp", "allowed": "ISO 8601 UTC", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Official clinical or supervisor verification timestamp", "tech": "Verification audit timestamp"})
    
    # Standard Audit Timestamps
    cols.append({"name": "created_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": False, "def": "clock_timestamp()", "gen": "NONE", "key": "NONE", "uniq": False, "val": "UTC timestamp", "allowed": "ISO 8601 UTC", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Timestamp when record was initially committed", "tech": "Immutable creation timestamp"})
    cols.append({"name": "updated_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": False, "def": "clock_timestamp()", "gen": "NONE", "key": "NONE", "uniq": False, "val": "UTC timestamp", "allowed": "ISO 8601 UTC", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Timestamp when record was last modified", "tech": "Trigger-managed update timestamp"})
    cols.append({"name": "deleted_at", "type": "TIMESTAMPTZ", "len": "64-bit", "null": True, "def": None, "gen": "NONE", "key": "NONE", "uniq": False, "val": "UTC timestamp", "allowed": "ISO 8601 UTC", "class": "CLASS-002", "pii": False, "phi": False, "enc": "NONE", "mask": "None", "biz": "Timestamp of soft-deletion", "tech": "Soft-deletion timestamp preserving historical referential integrity"})
    
    return cols

# Build master column list
COLUMNS: List[Dict[str, Any]] = []
col_counter = 1

for tbl in TABLES:
    tcols = generate_standard_columns_for_table(tbl)
    for c in tcols:
        col_id = f"COLUMN-{col_counter:03d}"
        COLUMNS.append({
            "id": col_id,
            "table_id": tbl["id"],
            "table_name": tbl["name"],
            "column_name": c["name"],
            "business_definition": c["biz"],
            "technical_definition": c["tech"],
            "pg_type": c["type"],
            "length_precision": c["len"],
            "nullable": c["null"],
            "default": c["def"],
            "generated_status": c["gen"],
            "pk_fk_status": c["key"],
            "uniqueness": c["uniq"],
            "validation": c["val"],
            "allowed_values": c["allowed"],
            "classification": c["class"],
            "pii_status": c["pii"],
            "sensitive_health_data": c["phi"],
            "encryption_req": c["enc"],
            "masking_req": c["mask"],
            "retention": tbl["retention"],
            "source": f"{tbl['domain']} Service Engine",
            "target": f"PostgreSQL {tbl['schema']}.{tbl['name']}",
            "lineage": tbl["lineage_refs"].split(", ")[0] if tbl["lineage_refs"] else "LINEAGE-001",
            "api_exposure": "Staff Role Restricted" if c["class"] in ["CLASS-004", "CLASS-005"] else "Internal API",
            "frontend_exposure": c["mask"],
            "analytics_exposure": "De-identified / Aggregated" if c["pii"] or c["phi"] else "Direct",
            "ai_exposure": "Permitted with Patient Consent" if not c["pii"] else "Strictly Excluded",
            "audit_behavior": "Full Change Capture" if c["key"] in ["PK", "FK"] or c["pii"] else "Row Level",
            "data_quality_rules": tbl["dq_rules"]
        })
        col_counter += 1

COLUMN_MAP = {c["id"]: c for c in COLUMNS}
TABLE_COLUMNS_MAP: Dict[str, List[Dict[str, Any]]] = {}
for c in COLUMNS:
    TABLE_COLUMNS_MAP.setdefault(c["table_name"], []).append(c)

if __name__ == "__main__":
    print(f"Generated {len(COLUMNS)} Columns (COLUMN-001..COLUMN-{len(COLUMNS):03d}) across {len(TABLES)} tables.")
