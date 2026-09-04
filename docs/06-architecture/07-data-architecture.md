# 💾 Architecture Document 07: Enterprise Data Architecture & Storage Specification
## Namma Clinic Digital Health & Operations Platform
### Greater Bengaluru Authority (GBA) / BBMP Health Department
**Standard:** C4 Level 3 / DDL Blueprint / Relational & Columnar Storage | **Status:** APPROVED BASELINE | **Code:** `ARCH-DATA-07`

---

## 01. Document Overview & Enterprise Data Philosophy
This document specifies the authoritative enterprise data architecture for the Namma Clinic Digital Health & Operations Platform. The data subsystem must reliably store, process, and synchronize electronic health records (EHR), supply chain movements, clinical orders, and operational metrics across 183 primary health clinics in Bengaluru. It balances strict ACID transactional consistency in central PostgreSQL with edge-local autonomy in SQLite, CDC-streamed analytical aggregations in ClickHouse, and cryptographic immutability in WORM audit ledgers.

### 01.1 Core Data Invariants & Design Principles
1. **Time-Ordered Universal Identifiers (UUIDv7):** All relational entities utilize 128-bit UUIDv7 primary keys. UUIDv7 embeds a 48-bit millisecond Unix timestamp followed by 74 cryptographically random bits. This guarantees monotonic index locality in B-Trees, zero sequence lock contention, and collision-free ID generation across 183 disconnected edge nodes.
2. **UTC Timestamp Standard:** All temporal columns (`created_at`, `updated_at`, `event_time`) are strictly stored as `TIMESTAMPTZ` normalized to UTC. Client and edge display layers format these to Indian Standard Time (IST / `Asia/Kolkata`, UTC+05:30).
3. **Soft-Delete with Bi-Temporal Auditability:** Operational clinical entities are never physically deleted (`DELETE`). Soft deletions set `is_deleted = TRUE`, `deleted_at = NOW()`, and `deleted_by = <staff_uuid>`. Row updates increment an integer `version` counter supporting optimistic concurrency control.
4. **Zero Cross-Module Foreign Key Constraints:** Tables belonging to distinct domain bounded contexts communicate via domain IDs rather than hard database foreign key constraints. This enables future horizontal database sharding and autonomous module lifecycle management.
5. **Encrypted Field Storage (AES-256 GCM):** Patient identifiers (Aadhaar virtual ID, phone numbers, contact addresses) are stored as encrypted byte arrays (`bytea`) encrypted with AES-256 GCM using keys managed in cloud HSM / HashiCorp Vault.
6. **Cryptographic WORM Hash Chaining:** Audit log tables implement SHA-256 HMAC cryptographic hash chaining (`current_hash = SHA256(prev_hash || payload)`) preventing non-detectable historical tampering.

## 02. Canonical Master Data Schemas for All 30 Relational Entities
Exhaustive relational schema specifications, DDL contracts, indexing strategies, and partitioning rules across all 30 system entities:

### 02.01 Relational Entity Specification: `ARCH-DATA-001` (`auth_users`)
- **Entity Identifier:** `ARCH-DATA-001`
- **Target Database Table:** `auth_users`
- **Domain Bounded Context:** DOMAIN-001 (Governing Module: `MODULE-001` - Staff Authentication & MFA Engine)
- **Data Security Classification:** `CONFIDENTIAL` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** Permanent
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.auth_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_auth_users_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_auth_users_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_auth_users_clinic_active ON public.auth_users (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_auth_users_updated_sync ON public.auth_users (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_auth_users_created_brin ON public.auth_users USING BRIN (created_at);
CREATE INDEX idx_auth_users_payload_gin ON public.auth_users USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_auth_users (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_auth_users_sync ON local_auth_users (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-001` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for Permanent.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.02 Relational Entity Specification: `ARCH-DATA-002` (`role_permissions`)
- **Entity Identifier:** `ARCH-DATA-002`
- **Target Database Table:** `role_permissions`
- **Domain Bounded Context:** DOMAIN-001 (Governing Module: `MODULE-002` - Role-Based Access Control (RBAC) & Entitlements)
- **Data Security Classification:** `INTERNAL` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** Permanent
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.role_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_role_permissions_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_role_permissions_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_role_permissions_clinic_active ON public.role_permissions (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_role_permissions_updated_sync ON public.role_permissions (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_role_permissions_created_brin ON public.role_permissions USING BRIN (created_at);
CREATE INDEX idx_role_permissions_payload_gin ON public.role_permissions USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_role_permissions (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_role_permissions_sync ON local_role_permissions (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-002` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for Permanent.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.03 Relational Entity Specification: `ARCH-DATA-003` (`facilities`)
- **Entity Identifier:** `ARCH-DATA-003`
- **Target Database Table:** `facilities`
- **Domain Bounded Context:** DOMAIN-001 (Governing Module: `MODULE-003` - Healthcare Facility & Organizational Hierarchy)
- **Data Security Classification:** `PUBLIC` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** Permanent
- **Backup & Disaster Recovery Tier:** Tier 2 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.facilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_facilities_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_facilities_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_facilities_clinic_active ON public.facilities (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_facilities_updated_sync ON public.facilities (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_facilities_created_brin ON public.facilities USING BRIN (created_at);
CREATE INDEX idx_facilities_payload_gin ON public.facilities USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_facilities (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_facilities_sync ON local_facilities (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-003` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for Permanent.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.04 Relational Entity Specification: `ARCH-DATA-004` (`staff_profiles`)
- **Entity Identifier:** `ARCH-DATA-004`
- **Target Database Table:** `staff_profiles`
- **Domain Bounded Context:** DOMAIN-001 (Governing Module: `MODULE-004` - Clinical & Administrative Staff Directory)
- **Data Security Classification:** `RESTRICTED` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 2 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.staff_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_staff_profiles_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_staff_profiles_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_staff_profiles_clinic_active ON public.staff_profiles (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_staff_profiles_updated_sync ON public.staff_profiles (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_staff_profiles_created_brin ON public.staff_profiles USING BRIN (created_at);
CREATE INDEX idx_staff_profiles_payload_gin ON public.staff_profiles USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_staff_profiles (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_staff_profiles_sync ON local_staff_profiles (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-004` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.05 Relational Entity Specification: `ARCH-DATA-005` (`patients`)
- **Entity Identifier:** `ARCH-DATA-005`
- **Target Database Table:** `patients`
- **Domain Bounded Context:** DOMAIN-002 (Governing Module: `MODULE-005` - Patient Registration, Demographics & ABHA Minting)
- **Data Security Classification:** `RESTRICTED_PHI` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** Permanent
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_patients_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_patients_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_patients_clinic_active ON public.patients (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_patients_updated_sync ON public.patients (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_patients_created_brin ON public.patients USING BRIN (created_at);
CREATE INDEX idx_patients_payload_gin ON public.patients USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_patients (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_patients_sync ON local_patients (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-005` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for Permanent.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.06 Relational Entity Specification: `ARCH-DATA-006` (`consent_records`)
- **Entity Identifier:** `ARCH-DATA-006`
- **Target Database Table:** `consent_records`
- **Domain Bounded Context:** DOMAIN-002 (Governing Module: `MODULE-006` - Informed Clinical Consent & DPDP Data Privacy)
- **Data Security Classification:** `RESTRICTED_PHI` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.consent_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_consent_records_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_consent_records_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_consent_records_clinic_active ON public.consent_records (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_consent_records_updated_sync ON public.consent_records (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_consent_records_created_brin ON public.consent_records USING BRIN (created_at);
CREATE INDEX idx_consent_records_payload_gin ON public.consent_records USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_consent_records (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_consent_records_sync ON local_consent_records (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-006` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.07 Relational Entity Specification: `ARCH-DATA-007` (`tokens`)
- **Entity Identifier:** `ARCH-DATA-007`
- **Target Database Table:** `tokens`
- **Domain Bounded Context:** DOMAIN-002 (Governing Module: `MODULE-007` - Patient Token Generation & Station Routing)
- **Data Security Classification:** `INTERNAL` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 3 Years
- **Backup & Disaster Recovery Tier:** Tier 2 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_tokens_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_tokens_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_tokens_clinic_active ON public.tokens (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_tokens_updated_sync ON public.tokens (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_tokens_created_brin ON public.tokens USING BRIN (created_at);
CREATE INDEX idx_tokens_payload_gin ON public.tokens USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_tokens (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_tokens_sync ON local_tokens (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-007` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 3 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.08 Relational Entity Specification: `ARCH-DATA-008` (`queue_states`)
- **Entity Identifier:** `ARCH-DATA-008`
- **Target Database Table:** `queue_states`
- **Domain Bounded Context:** DOMAIN-002 (Governing Module: `MODULE-008` - Dynamic Queue Orchestration & Display Boards)
- **Data Security Classification:** `INTERNAL` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 1 Year
- **Backup & Disaster Recovery Tier:** Tier 3 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.queue_states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_queue_states_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_queue_states_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_queue_states_clinic_active ON public.queue_states (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_queue_states_updated_sync ON public.queue_states (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_queue_states_created_brin ON public.queue_states USING BRIN (created_at);
CREATE INDEX idx_queue_states_payload_gin ON public.queue_states USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_queue_states (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_queue_states_sync ON local_queue_states (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-008` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 1 Year.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.09 Relational Entity Specification: `ARCH-DATA-009` (`clinical_encounters`)
- **Entity Identifier:** `ARCH-DATA-009`
- **Target Database Table:** `clinical_encounters`
- **Domain Bounded Context:** DOMAIN-003 (Governing Module: `MODULE-009` - Doctor EMR Console & Clinical SOAP Encounter)
- **Data Security Classification:** `RESTRICTED_PHI` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.clinical_encounters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_clinical_encounters_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_clinical_encounters_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_clinical_encounters_clinic_active ON public.clinical_encounters (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_clinical_encounters_updated_sync ON public.clinical_encounters (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_clinical_encounters_created_brin ON public.clinical_encounters USING BRIN (created_at);
CREATE INDEX idx_clinical_encounters_payload_gin ON public.clinical_encounters USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_clinical_encounters (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_clinical_encounters_sync ON local_clinical_encounters (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-009` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.10 Relational Entity Specification: `ARCH-DATA-010` (`diagnoses`)
- **Entity Identifier:** `ARCH-DATA-010`
- **Target Database Table:** `diagnoses`
- **Domain Bounded Context:** DOMAIN-003 (Governing Module: `MODULE-010` - ICD-10 & SNOMED CT Clinical Diagnosis Coding)
- **Data Security Classification:** `RESTRICTED_PHI` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.diagnoses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_diagnoses_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_diagnoses_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_diagnoses_clinic_active ON public.diagnoses (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_diagnoses_updated_sync ON public.diagnoses (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_diagnoses_created_brin ON public.diagnoses USING BRIN (created_at);
CREATE INDEX idx_diagnoses_payload_gin ON public.diagnoses USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_diagnoses (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_diagnoses_sync ON local_diagnoses (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-010` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.11 Relational Entity Specification: `ARCH-DATA-011` (`prescriptions`)
- **Entity Identifier:** `ARCH-DATA-011`
- **Target Database Table:** `prescriptions`
- **Domain Bounded Context:** DOMAIN-003 (Governing Module: `MODULE-011` - Electronic Prescription (e-Rx) & Drug Safety Engine)
- **Data Security Classification:** `RESTRICTED_PHI` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.prescriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_prescriptions_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_prescriptions_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_prescriptions_clinic_active ON public.prescriptions (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_prescriptions_updated_sync ON public.prescriptions (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_prescriptions_created_brin ON public.prescriptions USING BRIN (created_at);
CREATE INDEX idx_prescriptions_payload_gin ON public.prescriptions USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_prescriptions (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_prescriptions_sync ON local_prescriptions (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-011` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.12 Relational Entity Specification: `ARCH-DATA-012` (`lab_orders`)
- **Entity Identifier:** `ARCH-DATA-012`
- **Target Database Table:** `lab_orders`
- **Domain Bounded Context:** DOMAIN-003 (Governing Module: `MODULE-012` - Point-of-Care Laboratory Testing & Diagnostic Orders)
- **Data Security Classification:** `RESTRICTED_PHI` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.lab_orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_lab_orders_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_lab_orders_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_lab_orders_clinic_active ON public.lab_orders (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_lab_orders_updated_sync ON public.lab_orders (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_lab_orders_created_brin ON public.lab_orders USING BRIN (created_at);
CREATE INDEX idx_lab_orders_payload_gin ON public.lab_orders USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_lab_orders (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_lab_orders_sync ON local_lab_orders (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-012` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.13 Relational Entity Specification: `ARCH-DATA-013` (`dispensations`)
- **Entity Identifier:** `ARCH-DATA-013`
- **Target Database Table:** `dispensations`
- **Domain Bounded Context:** DOMAIN-004 (Governing Module: `MODULE-013` - Pharmacy Dispensing & 2D Barcode Verification)
- **Data Security Classification:** `RESTRICTED_PHI` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.dispensations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_dispensations_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_dispensations_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_dispensations_clinic_active ON public.dispensations (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_dispensations_updated_sync ON public.dispensations (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_dispensations_created_brin ON public.dispensations USING BRIN (created_at);
CREATE INDEX idx_dispensations_payload_gin ON public.dispensations USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_dispensations (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_dispensations_sync ON local_dispensations (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-013` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.14 Relational Entity Specification: `ARCH-DATA-014` (`pharmacy_batches`)
- **Entity Identifier:** `ARCH-DATA-014`
- **Target Database Table:** `pharmacy_batches`
- **Domain Bounded Context:** DOMAIN-004 (Governing Module: `MODULE-014` - Real-Time Batch Inventory & FEFO Stock Ledger)
- **Data Security Classification:** `INTERNAL` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.pharmacy_batches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_pharmacy_batches_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_pharmacy_batches_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_pharmacy_batches_clinic_active ON public.pharmacy_batches (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_pharmacy_batches_updated_sync ON public.pharmacy_batches (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_pharmacy_batches_created_brin ON public.pharmacy_batches USING BRIN (created_at);
CREATE INDEX idx_pharmacy_batches_payload_gin ON public.pharmacy_batches USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_pharmacy_batches (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_pharmacy_batches_sync ON local_pharmacy_batches (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-014` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.15 Relational Entity Specification: `ARCH-DATA-015` (`drug_indents`)
- **Entity Identifier:** `ARCH-DATA-015`
- **Target Database Table:** `drug_indents`
- **Domain Bounded Context:** DOMAIN-004 (Governing Module: `MODULE-015` - Drug Indent Generation, Receiving & Cold-Chain Intake)
- **Data Security Classification:** `INTERNAL` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 5 Years
- **Backup & Disaster Recovery Tier:** Tier 2 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.drug_indents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_drug_indents_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_drug_indents_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_drug_indents_clinic_active ON public.drug_indents (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_drug_indents_updated_sync ON public.drug_indents (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_drug_indents_created_brin ON public.drug_indents USING BRIN (created_at);
CREATE INDEX idx_drug_indents_payload_gin ON public.drug_indents USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_drug_indents (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_drug_indents_sync ON local_drug_indents (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-015` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 5 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.16 Relational Entity Specification: `ARCH-DATA-016` (`formulary_master`)
- **Entity Identifier:** `ARCH-DATA-016`
- **Target Database Table:** `formulary_master`
- **Domain Bounded Context:** DOMAIN-004 (Governing Module: `MODULE-016` - Essential Medicine List (EML) & Formulary Master)
- **Data Security Classification:** `PUBLIC` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** Permanent
- **Backup & Disaster Recovery Tier:** Tier 2 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.formulary_master (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_formulary_master_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_formulary_master_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_formulary_master_clinic_active ON public.formulary_master (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_formulary_master_updated_sync ON public.formulary_master (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_formulary_master_created_brin ON public.formulary_master USING BRIN (created_at);
CREATE INDEX idx_formulary_master_payload_gin ON public.formulary_master USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_formulary_master (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_formulary_master_sync ON local_formulary_master (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-016` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for Permanent.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.17 Relational Entity Specification: `ARCH-DATA-017` (`referrals`)
- **Entity Identifier:** `ARCH-DATA-017`
- **Target Database Table:** `referrals`
- **Domain Bounded Context:** DOMAIN-005 (Governing Module: `MODULE-017` - Secondary Referral & 108 Emergency EMS Transit)
- **Data Security Classification:** `RESTRICTED_PHI` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.referrals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_referrals_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_referrals_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_referrals_clinic_active ON public.referrals (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_referrals_updated_sync ON public.referrals (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_referrals_created_brin ON public.referrals USING BRIN (created_at);
CREATE INDEX idx_referrals_payload_gin ON public.referrals USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_referrals (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_referrals_sync ON local_referrals (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-017` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.18 Relational Entity Specification: `ARCH-DATA-018` (`ncd_episodes`)
- **Entity Identifier:** `ARCH-DATA-018`
- **Target Database Table:** `ncd_episodes`
- **Domain Bounded Context:** DOMAIN-005 (Governing Module: `MODULE-018` - NCD Longitudinal Follow-Up & Recall Management)
- **Data Security Classification:** `RESTRICTED_PHI` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.ncd_episodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_ncd_episodes_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_ncd_episodes_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_ncd_episodes_clinic_active ON public.ncd_episodes (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_ncd_episodes_updated_sync ON public.ncd_episodes (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_ncd_episodes_created_brin ON public.ncd_episodes USING BRIN (created_at);
CREATE INDEX idx_ncd_episodes_payload_gin ON public.ncd_episodes USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_ncd_episodes (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_ncd_episodes_sync ON local_ncd_episodes (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-018` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.19 Relational Entity Specification: `ARCH-DATA-019` (`notifications`)
- **Entity Identifier:** `ARCH-DATA-019`
- **Target Database Table:** `notifications`
- **Domain Bounded Context:** DOMAIN-005 (Governing Module: `MODULE-019` - Citizen Multichannel Notifications & Health Reminders)
- **Data Security Classification:** `RESTRICTED` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 1 Year
- **Backup & Disaster Recovery Tier:** Tier 3 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_notifications_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_notifications_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_notifications_clinic_active ON public.notifications (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_notifications_updated_sync ON public.notifications (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_notifications_created_brin ON public.notifications USING BRIN (created_at);
CREATE INDEX idx_notifications_payload_gin ON public.notifications USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_notifications (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_notifications_sync ON local_notifications (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-019` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 1 Year.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.20 Relational Entity Specification: `ARCH-DATA-020` (`grievances`)
- **Entity Identifier:** `ARCH-DATA-020`
- **Target Database Table:** `grievances`
- **Domain Bounded Context:** DOMAIN-002 (Governing Module: `MODULE-020` - Citizen Feedback, Grievance & Ombudsman Redressal)
- **Data Security Classification:** `RESTRICTED` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 5 Years
- **Backup & Disaster Recovery Tier:** Tier 2 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.grievances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_grievances_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_grievances_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_grievances_clinic_active ON public.grievances (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_grievances_updated_sync ON public.grievances (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_grievances_created_brin ON public.grievances USING BRIN (created_at);
CREATE INDEX idx_grievances_payload_gin ON public.grievances USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_grievances (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_grievances_sync ON local_grievances (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-020` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 5 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.21 Relational Entity Specification: `ARCH-DATA-021` (`audit_events`)
- **Entity Identifier:** `ARCH-DATA-021`
- **Target Database Table:** `audit_events`
- **Domain Bounded Context:** DOMAIN-006 (Governing Module: `MODULE-021` - Cryptographic Audit Ledger & Compliance (WORM))
- **Data Security Classification:** `CONFIDENTIAL` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.audit_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_audit_events_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_audit_events_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_audit_events_clinic_active ON public.audit_events (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_audit_events_updated_sync ON public.audit_events (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_audit_events_created_brin ON public.audit_events USING BRIN (created_at);
CREATE INDEX idx_audit_events_payload_gin ON public.audit_events USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_audit_events (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_audit_events_sync ON local_audit_events (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-021` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.22 Relational Entity Specification: `ARCH-DATA-022` (`kpi_metrics`)
- **Entity Identifier:** `ARCH-DATA-022`
- **Target Database Table:** `kpi_metrics`
- **Domain Bounded Context:** DOMAIN-006 (Governing Module: `MODULE-022` - Zonal & Ward Operational KPI Dashboards)
- **Data Security Classification:** `PUBLIC_AGGREGATE` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 3 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.kpi_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_kpi_metrics_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_kpi_metrics_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_kpi_metrics_clinic_active ON public.kpi_metrics (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_kpi_metrics_updated_sync ON public.kpi_metrics (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_kpi_metrics_created_brin ON public.kpi_metrics USING BRIN (created_at);
CREATE INDEX idx_kpi_metrics_payload_gin ON public.kpi_metrics USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_kpi_metrics (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_kpi_metrics_sync ON local_kpi_metrics (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-022` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.23 Relational Entity Specification: `ARCH-DATA-023` (`cdss_rules`)
- **Entity Identifier:** `ARCH-DATA-023`
- **Target Database Table:** `cdss_rules`
- **Domain Bounded Context:** DOMAIN-006 (Governing Module: `MODULE-023` - Safe AI/ML Clinical Decision Support Safeguards)
- **Data Security Classification:** `INTERNAL` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** Permanent
- **Backup & Disaster Recovery Tier:** Tier 2 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.cdss_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_cdss_rules_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_cdss_rules_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_cdss_rules_clinic_active ON public.cdss_rules (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_cdss_rules_updated_sync ON public.cdss_rules (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_cdss_rules_created_brin ON public.cdss_rules USING BRIN (created_at);
CREATE INDEX idx_cdss_rules_payload_gin ON public.cdss_rules USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_cdss_rules (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_cdss_rules_sync ON local_cdss_rules (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-023` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for Permanent.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.24 Relational Entity Specification: `ARCH-DATA-024` (`abdm_artifacts`)
- **Entity Identifier:** `ARCH-DATA-024`
- **Target Database Table:** `abdm_artifacts`
- **Domain Bounded Context:** DOMAIN-006 (Governing Module: `MODULE-024` - National Health ABDM Ecosystem Interoperability)
- **Data Security Classification:** `RESTRICTED_PHI` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.abdm_artifacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_abdm_artifacts_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_abdm_artifacts_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_abdm_artifacts_clinic_active ON public.abdm_artifacts (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_abdm_artifacts_updated_sync ON public.abdm_artifacts (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_abdm_artifacts_created_brin ON public.abdm_artifacts USING BRIN (created_at);
CREATE INDEX idx_abdm_artifacts_payload_gin ON public.abdm_artifacts USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_abdm_artifacts (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_abdm_artifacts_sync ON local_abdm_artifacts (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-024` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.25 Relational Entity Specification: `ARCH-DATA-025` (`mutation_log`)
- **Entity Identifier:** `ARCH-DATA-025`
- **Target Database Table:** `mutation_log`
- **Domain Bounded Context:** DOMAIN-006 (Governing Module: `MODULE-025` - Autonomous Offline Edge Engine & Conflict Replay)
- **Data Security Classification:** `INTERNAL` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 90 Days
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.mutation_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_mutation_log_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_mutation_log_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_mutation_log_clinic_active ON public.mutation_log (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_mutation_log_updated_sync ON public.mutation_log (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_mutation_log_created_brin ON public.mutation_log USING BRIN (created_at);
CREATE INDEX idx_mutation_log_payload_gin ON public.mutation_log USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_mutation_log (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_mutation_log_sync ON local_mutation_log (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-025` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 90 Days.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.26 Relational Entity Specification: `ARCH-DATA-026` (`system_configs`)
- **Entity Identifier:** `ARCH-DATA-026`
- **Target Database Table:** `system_configs`
- **Domain Bounded Context:** DOMAIN-001 (Governing Module: `MODULE-026` - Master System Administration & Feature Flagging)
- **Data Security Classification:** `CONFIDENTIAL` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** Permanent
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.system_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_system_configs_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_system_configs_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_system_configs_clinic_active ON public.system_configs (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_system_configs_updated_sync ON public.system_configs (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_system_configs_created_brin ON public.system_configs USING BRIN (created_at);
CREATE INDEX idx_system_configs_payload_gin ON public.system_configs USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_system_configs (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_system_configs_sync ON local_system_configs (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-026` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for Permanent.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.27 Relational Entity Specification: `ARCH-DATA-027` (`hmis_reports`)
- **Entity Identifier:** `ARCH-DATA-027`
- **Target Database Table:** `hmis_reports`
- **Domain Bounded Context:** DOMAIN-006 (Governing Module: `MODULE-027` - State Health HMIS & Statutory Disease Reporting)
- **Data Security Classification:** `PUBLIC_AGGREGATE` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 2 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.hmis_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_hmis_reports_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_hmis_reports_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_hmis_reports_clinic_active ON public.hmis_reports (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_hmis_reports_updated_sync ON public.hmis_reports (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_hmis_reports_created_brin ON public.hmis_reports USING BRIN (created_at);
CREATE INDEX idx_hmis_reports_payload_gin ON public.hmis_reports USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_hmis_reports (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_hmis_reports_sync ON local_hmis_reports (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-027` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.28 Relational Entity Specification: `ARCH-DATA-028` (`helpdesk_tickets`)
- **Entity Identifier:** `ARCH-DATA-028`
- **Target Database Table:** `helpdesk_tickets`
- **Domain Bounded Context:** DOMAIN-005 (Governing Module: `MODULE-028` - Facility Operations Helpdesk & Incident Dispatch)
- **Data Security Classification:** `INTERNAL` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 3 Years
- **Backup & Disaster Recovery Tier:** Tier 3 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.helpdesk_tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_helpdesk_tickets_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_helpdesk_tickets_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_helpdesk_tickets_clinic_active ON public.helpdesk_tickets (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_helpdesk_tickets_updated_sync ON public.helpdesk_tickets (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_helpdesk_tickets_created_brin ON public.helpdesk_tickets USING BRIN (created_at);
CREATE INDEX idx_helpdesk_tickets_payload_gin ON public.helpdesk_tickets USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_helpdesk_tickets (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_helpdesk_tickets_sync ON local_helpdesk_tickets (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-028` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 3 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.29 Relational Entity Specification: `ARCH-DATA-029` (`teleconsultations`)
- **Entity Identifier:** `ARCH-DATA-029`
- **Target Database Table:** `teleconsultations`
- **Domain Bounded Context:** DOMAIN-003 (Governing Module: `MODULE-029` - Telemedicine & Specialist Tele-Consultation Bridge)
- **Data Security Classification:** `RESTRICTED_PHI` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.teleconsultations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_teleconsultations_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_teleconsultations_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_teleconsultations_clinic_active ON public.teleconsultations (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_teleconsultations_updated_sync ON public.teleconsultations (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_teleconsultations_created_brin ON public.teleconsultations USING BRIN (created_at);
CREATE INDEX idx_teleconsultations_payload_gin ON public.teleconsultations USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_teleconsultations (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_teleconsultations_sync ON local_teleconsultations (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-029` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

### 02.30 Relational Entity Specification: `ARCH-DATA-030` (`command_center_incidents`)
- **Entity Identifier:** `ARCH-DATA-030`
- **Target Database Table:** `command_center_incidents`
- **Domain Bounded Context:** DOMAIN-006 (Governing Module: `MODULE-030` - Municipal Pilot Command Center & Disaster Operations)
- **Data Security Classification:** `RESTRICTED` (DPDP Act 2023 Protected)
- **Statutory Retention Period:** 10 Years
- **Backup & Disaster Recovery Tier:** Tier 1 (RPO < 15 min)
- **Primary Key Type:** UUIDv7 (Monotonically Sortable)

#### 02.{idx:02d}.1 PostgreSQL DDL Specification Blueprint
```sql
CREATE TABLE public.command_center_incidents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UUIDv7 in application runtime
    clinic_id VARCHAR(32) NOT NULL, -- Format: BBMP-CLN-XXX
    entity_version INT NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    deleted_by UUID NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    sync_status VARCHAR(20) NOT NULL DEFAULT 'SYNCED', -- PENDING, SYNCED, CONFLICT
    vector_clock JSONB NOT NULL DEFAULT '{}'::jsonb,
    record_checksum CHAR(64) NOT NULL,
    CONSTRAINT ck_command_center_incidents_clinic CHECK (clinic_id ~ '^BBMP-CLN-[0-9]{3}$'),
    CONSTRAINT ck_command_center_incidents_version CHECK (entity_version >= 1)
);
```

#### 02.{idx:02d}.2 Indexing & Performance Optimization
Indexes tailored for high-concurrency OLTP reads, clinic tenancy filters, and sync queries:
```sql
CREATE INDEX idx_command_center_incidents_clinic_active ON public.command_center_incidents (clinic_id, is_active) WHERE is_deleted = FALSE;
CREATE INDEX idx_command_center_incidents_updated_sync ON public.command_center_incidents (updated_at) WHERE sync_status = 'PENDING';
CREATE INDEX idx_command_center_incidents_created_brin ON public.command_center_incidents USING BRIN (created_at);
CREATE INDEX idx_command_center_incidents_payload_gin ON public.command_center_incidents USING GIN (payload jsonb_path_ops);
```

#### 02.{idx:02d}.3 Edge SQLite Mirroring Definition
Lightweight local table mirrored on the clinic Intel N100 mini-server running SQLite in WAL mode:
```sql
CREATE TABLE IF NOT EXISTS local_command_center_incidents (
    id TEXT PRIMARY KEY,
    clinic_id TEXT NOT NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    deleted_at TEXT,
    deleted_by TEXT,
    payload TEXT NOT NULL,
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_local_command_center_incidents_sync ON local_command_center_incidents (sync_status);
```

#### 02.{idx:02d}.4 Field-Level Data Dictionary & Constraints
| Column Name | Logical Type | Nullable | Default | Encryption | Business Invariant & Validation Rules |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `id` | UUIDv7 | NO | Generated | None | Unique time-sortable primary key. |
| `clinic_id` | VARCHAR(32) | NO | Mandatory | None | Tenant clinic identifier conforming to BBMP pattern. |
| `entity_version` | INTEGER | NO | 1 | None | Incremented on each update for optimistic concurrency. |
| `is_active` | BOOLEAN | NO | TRUE | None | Functional availability flag. |
| `is_deleted` | BOOLEAN | NO | FALSE | None | Soft-deletion flag. Row remains for statutory audit. |
| `created_at` | TIMESTAMPTZ | NO | NOW() | None | Monotonic creation timestamp in UTC. |
| `created_by` | UUID | NO | Mandatory | None | Foreign key reference to staff member in `auth_users`. |
| `updated_at` | TIMESTAMPTZ | NO | NOW() | None | Last modification timestamp in UTC. |
| `updated_by` | UUID | NO | Mandatory | None | Staff UUID performing last modification. |
| `deleted_at` | TIMESTAMPTZ | YES | NULL | None | Timestamp of soft-deletion execution. |
| `deleted_by` | UUID | YES | NULL | None | Staff UUID performing soft deletion. |
| `payload` | JSONB | NO | '{}' | Selective | Domain-specific attributes conforming to `ARCH-DATA-030` schema. |
| `sync_status` | VARCHAR(20) | NO | 'SYNCED' | None | Distributed replication state (`SYNCED`, `PENDING`, `CONFLICT`). |
| `vector_clock` | JSONB | NO | '{}' | None | Logical node clock mappings for CRDT merge resolution. |
| `record_checksum`| CHAR(64) | NO | Mandatory | None | SHA-256 hash of immutable fields for tamper detection. |

#### 02.{idx:02d}.5 Lifecycle, Archival & Purging Rules
- **Active Retention:** Hot storage in central PostgreSQL for 10 Years.
- **Cold Archival:** Partition drops after active window; exported to encrypted Parquet files in S3-compatible cold tier.
- **Purging Policy:** Absolute physical purge forbidden for clinical records; soft-deleted records retained permanently for legal liability protection.

---

## 03. Database Partitioning & Sharding Strategy
PostgreSQL table partitioning architecture optimizing query latency and storage management across 183 clinics:
1. **Time-Range Partitioning for High-Velocity Tables:**
   - Tables `clinical_encounters`, `lab_orders`, `prescriptions`, `dispensations`, `queue_states`, and `audit_events` are partitioned by `RANGE (created_at)` on a monthly cadence.
   - Automated partition management via `pg_partman` generates partitions 2 months in advance and drops cold partitions into archival storage.
2. **Tenancy Hash Partitioning Feasibility:**
   - Clinic-level tenancy isolation is enforced logically via `WHERE clinic_id = :clinic_id` in application repositories.
   - Multi-tenant shared schemas are retained for Phase 06; horizontal database sharding across BBMP zones is planned for Phase 08 if clinic volume scales beyond 500 facilities.

## 04. Write-Ahead Logging (WAL) & Distributed Transaction Architecture
Transactional guarantees across cloud and edge tiers:
1. **Cloud PostgreSQL WAL Settings:**
   - `wal_level = replica`
   - `max_wal_size = 16GB`
   - `min_wal_size = 1GB`
   - `checkpoint_completion_target = 0.9`
   - Synchronous replication to 1 standby AZ node; asynchronous replication to disaster recovery AZ node.
2. **Edge Mini-Server SQLite WAL Configuration:**
   - `PRAGMA journal_mode = WAL;` (Enables concurrent reads during writes)
   - `PRAGMA synchronous = NORMAL;` (Protects against corruption on unexpected power loss)
   - `PRAGMA busy_timeout = 5000;` (Prevents immediate lock failure during concurrent workstation writes)
   - `PRAGMA foreign_keys = ON;` (Enforces referential integrity locally)

## 05. Debezium Change Data Capture (CDC) & Kafka Pipeline
Streaming operational transaction deltas into the analytical ClickHouse cluster without degrading OLTP IOPS:
1. **PostgreSQL Logical Decoding:** Configured with `wal_level = logical` and `pgoutput` plugin.
2. **Debezium PostgreSQL Connector:** Connects to central database replica; captures row-level INSERT, UPDATE, and DELETE operations.
3. **Apache Kafka Topics:** Topic structure `cdc.namma.<table_name>` (e.g. `cdc.namma.prescriptions`, `cdc.namma.dispensations`). Messages encoded using Apache Avro with Confluent Schema Registry.
4. **Kafka Connect ClickHouse Sink:** Consumes Avro topics and executes micro-batch inserts into ClickHouse `ReplacingMergeTree` tables every 2,000ms.

## 06. Columnar Storage Architecture (ClickHouse Star Schema)
ClickHouse analytical engine architecture supporting sub-second epidemiological queries across 183 clinics:
1. **Fact Tables:**
   - `fact_consultations`: 1 row per clinical consultation encounter with duration, diagnosis code, vitals, and provider.
   - `fact_dispensations`: 1 row per dispensed drug line item with batch, quantity, and cost.
   - `fact_lab_investigations`: 1 row per diagnostic test result with turnaround time and panic flag.
   - `fact_queue_waits`: 1 row per token journey tracking wait time at registration, nursing, doctor, and pharmacy.
2. **Dimension Tables:**
   - `dim_clinics`: Facility attributes, ward, zone, latitude, longitude, operational status.
   - `dim_drugs`: Formulary catalog, therapeutic class, generic name, dosage form.
   - `dim_diagnoses`: SNOMED CT and ICD-10 diagnostic hierarchy.
   - `dim_calendar`: Time dimension by hour, day, week, month, quarter, and municipal holiday.
3. **ClickHouse Table Engine Strategy:** Engine `ReplacingMergeTree(version)` keyed on `(clinic_id, created_date, id)` ensuring automatic deduplication of streaming CDC events.

## 07. Cryptographic WORM Audit Data Architecture
Technical mechanics of the tamper-evident audit ledger conforming to DPDP Act 2023:
1. **Hash Chain Schema (`audit_events`):**
   - `event_id`: UUIDv7
   - `sequence_number`: BIGSERIAL (Strictly monotonic)
   - `previous_hash`: CHAR(64) (SHA-256 of preceding row)
   - `payload_digest`: CHAR(64) (SHA-256 of serialized event JSON)
   - `current_hash`: CHAR(64) (`SHA256(sequence_number || previous_hash || timestamp || user_id || payload_digest)`)
   - `hmac_signature`: CHAR(64) (HMAC-SHA256 calculated using HSM private secret)
2. **Tamper Invalidation Proof:** If an attacker modifies or deletes a historical record, all subsequent `previous_hash` references fail validation, instantly triggering an automated security alarm.

## 08. Data Protection, Anonymization & DPDP Act 2023 Compliance
Mechanisms enforcing statutory personal data protection mandates:
1. **Anonymization & Pseudonymization Engine:** Analytical queries exported to municipal public dashboards automatically pass through a k-anonymity filter (k >= 5). Demographic cells with fewer than 5 patients in a ward are suppressed.
2. **Right to Erasure Handling:** For operational data, statutory clinical record retention mandates supersede erasure requests (minimum 10 years per National Medical Commission guidelines). For marketing or SMS notification preferences, records are scrubbed within 24 hours.
3. **Cryptographic Key Management:** Database volumes are encrypted at rest using LUKS / AWS KMS. Sensitive PHI columns are encrypted at application level before persistence.

## 09. Database Migration, Seeding & Governance Runbook
Disciplined lifecycle management preventing schema drift across environments:
1. **Version-Controlled Forward Migrations:** Managed using Prisma Migrate / Liquibase; raw unversioned SQL modifications are strictly prohibited.
2. **Pre-Deployment CI Validation:** All migration scripts are automatically tested against a 100,000-row synthetic PostgreSQL database in CI to verify that zero exclusive table locks exceed 200ms.
3. **Seed Data Governance:** Pre-packaged seed fixtures populate the essential drug list (300 items), SNOMED primary care terminology (5,000 concepts), and 183 BBMP clinic facility records.

## 10. Data Architecture Verification & Health Gateways
Automated health checks and operational monitors:
1. **Replication Lag Monitoring:** Alert triggered if streaming replication lag to standby database exceeds 5,000ms.
2. **Edge Sync Backlog:** Alert triggered if local `mutation_log` on clinic mini-server exceeds 1,000 pending transactions.
3. **Disk Space Watermark:** Database storage alerts at 75% capacity warning and 85% critical threshold.
4. **Index Bloat Inspection:** Nightly automated vacuum and re-indexing daemon prevents B-tree degradation.
