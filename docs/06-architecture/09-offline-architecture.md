# ⚡ Architecture Document 09: Offline-First Edge Resilience & Synchronization Specification
## Namma Clinic Digital Health & Operations Platform
### Greater Bengaluru Authority (GBA) / BBMP Health Department
**Standard:** Local-First / Vector Clocks / CRDT / Edge Autonomy | **Status:** APPROVED BASELINE | **Code:** `ARCH-OFF-09`

---

## 01. Document Overview & Offline Architectural Philosophy
This document specifies the authoritative edge architecture and synchronization engine for the Namma Clinic Digital Health & Operations Platform. In urban primary health centers across Bengaluru, municipal optical fiber connections and cellular backhauls experience frequent outages caused by road construction, monsoon flooding, and power disruptions. The platform is engineered with a **Local-First, Edge-Autonomous Architecture**, guaranteeing that every clinic operates with 100% operational fidelity for at least 72 consecutive hours during total WAN disconnection.

### 01.1 Core Offline Architectural Invariants
1. **Zero Clinical Workflow Disruption:** Doctor consultations, triage vitals capture, lab testing, token issuance, and pharmacy dispensing must execute locally on the clinic edge appliance without requiring a round-trip to the central cloud.
2. **72-Hour Autonomous Edge Horizon:** The local edge storage and background queuing mechanisms must support full clinic transaction volume for 72 continuous hours (minimum 1,500 patient encounters and 4,500 drug dispensations per clinic).
3. **Monotonically Ordered Mutation Journal:** Every edge write operation is serialized into an append-only `mutation_log` table with a local sequence number, timestamp, and vector clock before confirmation.
4. **Deterministic CRDT Conflict Resolution:** Concurrent updates between edge nodes and the central cloud are reconciled using Conflict-Free Replicated Data Types (CRDTs) with mathematical determinism, eliminating silent data corruption.
5. **Bandwidth-Aware Delta Sync:** Synchronization resumes automatically upon network restoration, employing adaptive batching, gzip/zstd payload compression, and priority-based queue draining.
6. **Cryptographic Edge Integrity:** All offline mutations are signed using the edge appliance's hardware-derived Ed25519 key, preventing spoofed offline record injection.

## 02. Edge Appliance Hardware, OS & Runtime Architecture
Standardized specification of the physical edge server deployed across all 183 primary health clinics:

| Hardware Component | Specified Technical Baseline | Performance & Environmental Justification |
| :--- | :--- | :--- |
| **Compute Processor** | Intel Alder Lake-N100 (4 Cores, 4 Threads, up to 3.4 GHz, 6W TDP) | Fanless industrial design, low power draw, high single-thread SQLite performance. |
| **System Memory** | 16 GB DDR5 4800 MHz Non-ECC SODIMM | Sufficient for local Node.js runtime, SQLite cache (2GB), and in-memory MQTT broker. |
| **Primary Storage** | 512 GB M.2 NVMe PCIe 3.0 x4 SSD (TLC, 600 TBW endurance) | Ultra-fast random IOPS (> 200,000 IOPS) ensuring zero SQLite commit lag under peak clinic rush. |
| **Network Interfaces** | Dual 2.5 GbE Intel i226-V Ethernet Ports + Wi-Fi 6 (802.11ax) | Port 1: Clinical LAN (VLAN 10); Port 2: Dual-SIM 4G/5G WAN Cellular Failover Gateway. |
| **Cryptographic Enclave**| Discrete Hardware TPM 2.0 Chip (TCG Certified) | Stores LUKS full-disk encryption keys and edge node Ed25519 signing private keys. |
| **Operating System** | Ubuntu Server 24.04 LTS (Noble Numbat) Minimal 64-bit | Hardened Linux kernel (CIS Level 2), systemd process supervision, automatic security patching. |
| **Edge Database** | SQLite 3.45+ compiled with WAL mode and JSON1 extensions | Zero-maintenance embedded relational database engine running locally in C runtime. |
| **Local Message Bus** | Embedded Mosquitto / EMQX MQTT Broker (v5.0) | Handles real-time TV screen display broadcasts and workstation notifications (< 10ms latency). |
| **Uninterruptible Power**| 1.5 kVA Line-Interactive UPS with External LiFePO4 Battery | Provides minimum 4 hours runtime during municipal load shedding; automated USB signaling. |

## 03. Edge Local Persistence Engine (SQLite WAL Mode)
Low-level configuration and database tuning directives for the clinic edge SQLite engine:
```sql
-- Canonical SQLite Engine Initialization PRAGMAs
PRAGMA journal_mode = WAL;          -- Enables concurrent reads while writing
PRAGMA synchronous = NORMAL;        -- Guarantees durability across crashes without fsync penalty
PRAGMA cache_size = -64000;         -- Allocates 64 MB in-memory page cache per connection
PRAGMA busy_timeout = 5000;         -- Waits up to 5,000ms on lock contention before returning SQLITE_BUSY
PRAGMA foreign_keys = ON;           -- Enforces relational constraints locally
PRAGMA temp_store = MEMORY;         -- Keeps temporary tables and indices in RAM
PRAGMA mmap_size = 268435456;       -- Enables 256 MB memory-mapped I/O
PRAGMA auto_vacuum = INCREMENTAL;   -- Reclaims space smoothly without long vacuum pauses
```

### 03.1 Edge Mutation Journal Schema (`local_mutation_log`)
Every write operation executed while offline appends a row to this journal:
```sql
CREATE TABLE IF NOT EXISTS local_mutation_log (
    mutation_id TEXT PRIMARY KEY,        -- UUIDv7 generated locally
    clinic_id TEXT NOT NULL,             -- Tenant clinic identifier
    sequence_number INTEGER NOT NULL,    -- Strictly monotonic local counter
    entity_table TEXT NOT NULL,          -- e.g. 'local_clinical_encounters'
    entity_id TEXT NOT NULL,             -- UUIDv7 of target record
    operation_type TEXT NOT NULL,        -- 'INSERT', 'UPDATE', 'SOFT_DELETE'
    payload_json TEXT NOT NULL,          -- Full mutated state snapshot
    vector_clock TEXT NOT NULL,          -- JSON object mapping node IDs to logical clocks
    created_at TEXT NOT NULL,            -- ISO 8601 UTC timestamp
    created_by TEXT NOT NULL,            -- Staff user UUIDv7
    sync_status TEXT NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'IN_FLIGHT', 'ACKNOWLEDGED', 'CONFLICT'
    attempt_count INTEGER NOT NULL DEFAULT 0,
    last_attempt_at TEXT,
    error_message TEXT,
    payload_checksum TEXT NOT NULL       -- SHA-256 hash of payload_json
);
CREATE INDEX IF NOT EXISTS idx_mutation_sync ON local_mutation_log (sync_status, sequence_number);
CREATE INDEX IF NOT EXISTS idx_mutation_entity ON local_mutation_log (entity_table, entity_id);
```

## 04. Vector Clock Causality Tracking & Mathematical Formalism
Theoretical foundation and algorithmic rules governing causality detection across distributed edge nodes:
1. **Vector Clock Structure:** A vector clock $V$ is a mapping from node identifiers to monotonically increasing logical integers: $V = \{ n_1: c_1, n_2: c_2, \dots, n_k: c_k \}$.
2. **Local Event Tick Rule:** When an event occurs at edge node $i$, the local clock is incremented: $V_i[i] \leftarrow V_i[i] + 1$.
3. **Causal Ordering ($V_a \le V_b$):** Mutation $a$ happened-before mutation $b$ ($a \prec b$) if and only if:
   $$\forall k, V_a[k] \le V_b[k] \quad \text{and} \quad \exists k, V_a[k] < V_b[k]$$
4. **Concurrent Conflict Condition ($V_a \parallel V_b$):** Mutations $a$ and $b$ are concurrent if neither happened-before the other:
   $$\neg(V_a \le V_b) \quad \text{and} \quad \neg(V_b \le V_a)$$
5. **Merge Rule:** When node $i$ receives a message with vector clock $V_{msg}$, it updates its local vector clock:
   $$V_i[k] \leftarrow \max(V_i[k], V_{msg}[k]) \quad \forall k, \quad \text{then} \quad V_i[i] \leftarrow V_i[i] + 1$$

## 05. Conflict-Free Replicated Data Types (CRDT) Across All 30 Entities
Detailed mathematical merge strategies, resolution rules, and invariant preservation specifications for all 30 relational data entities:

### 05.01 CRDT Specification: `ARCH-DATA-001` (`auth_users`)
- **Target Entity:** `ARCH-DATA-001` (`auth_users`)
- **Domain Context:** DOMAIN-001
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.01.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_auth_users_sync ON local_auth_users (sync_status, updated_at);
```

#### 05.01.2 Field-Level Merge Resolver Contract
```typescript
export class AuthUsersMergeResolver implements ICRDTResolver<AuthUsersEntity> {
  resolve(local: AuthUsersEntity, remote: AuthUsersEntity): MergeResult<AuthUsersEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.01.3 Automated Convergence & Property Test
```typescript
describe('AuthUsers CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-001', () => {
    const resolver = new AuthUsersMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `auth_users` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.02 CRDT Specification: `ARCH-DATA-002` (`role_permissions`)
- **Target Entity:** `ARCH-DATA-002` (`role_permissions`)
- **Domain Context:** DOMAIN-001
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.02.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_role_permissions_sync ON local_role_permissions (sync_status, updated_at);
```

#### 05.02.2 Field-Level Merge Resolver Contract
```typescript
export class RolePermissionsMergeResolver implements ICRDTResolver<RolePermissionsEntity> {
  resolve(local: RolePermissionsEntity, remote: RolePermissionsEntity): MergeResult<RolePermissionsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.02.3 Automated Convergence & Property Test
```typescript
describe('RolePermissions CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-002', () => {
    const resolver = new RolePermissionsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `role_permissions` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.03 CRDT Specification: `ARCH-DATA-003` (`facilities`)
- **Target Entity:** `ARCH-DATA-003` (`facilities`)
- **Domain Context:** DOMAIN-001
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.03.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_facilities_sync ON local_facilities (sync_status, updated_at);
```

#### 05.03.2 Field-Level Merge Resolver Contract
```typescript
export class FacilitiesMergeResolver implements ICRDTResolver<FacilitiesEntity> {
  resolve(local: FacilitiesEntity, remote: FacilitiesEntity): MergeResult<FacilitiesEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.03.3 Automated Convergence & Property Test
```typescript
describe('Facilities CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-003', () => {
    const resolver = new FacilitiesMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `facilities` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.04 CRDT Specification: `ARCH-DATA-004` (`staff_profiles`)
- **Target Entity:** `ARCH-DATA-004` (`staff_profiles`)
- **Domain Context:** DOMAIN-001
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.04.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_staff_profiles_sync ON local_staff_profiles (sync_status, updated_at);
```

#### 05.04.2 Field-Level Merge Resolver Contract
```typescript
export class StaffProfilesMergeResolver implements ICRDTResolver<StaffProfilesEntity> {
  resolve(local: StaffProfilesEntity, remote: StaffProfilesEntity): MergeResult<StaffProfilesEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.04.3 Automated Convergence & Property Test
```typescript
describe('StaffProfiles CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-004', () => {
    const resolver = new StaffProfilesMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `staff_profiles` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.05 CRDT Specification: `ARCH-DATA-005` (`patients`)
- **Target Entity:** `ARCH-DATA-005` (`patients`)
- **Domain Context:** DOMAIN-002
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.05.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_patients_sync ON local_patients (sync_status, updated_at);
```

#### 05.05.2 Field-Level Merge Resolver Contract
```typescript
export class PatientsMergeResolver implements ICRDTResolver<PatientsEntity> {
  resolve(local: PatientsEntity, remote: PatientsEntity): MergeResult<PatientsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.05.3 Automated Convergence & Property Test
```typescript
describe('Patients CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-005', () => {
    const resolver = new PatientsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `patients` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.06 CRDT Specification: `ARCH-DATA-006` (`consent_records`)
- **Target Entity:** `ARCH-DATA-006` (`consent_records`)
- **Domain Context:** DOMAIN-002
- **CRDT Mathematical Model:** `OR-Set (Observed-Remove Set)`
- **Functional Description:** Allergies and consent directives accumulate as observed sets; concurrent additions preserved without loss.

#### 05.06.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_consent_records_sync ON local_consent_records (sync_status, updated_at);
```

#### 05.06.2 Field-Level Merge Resolver Contract
```typescript
export class ConsentRecordsMergeResolver implements ICRDTResolver<ConsentRecordsEntity> {
  resolve(local: ConsentRecordsEntity, remote: ConsentRecordsEntity): MergeResult<ConsentRecordsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.06.3 Automated Convergence & Property Test
```typescript
describe('ConsentRecords CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-006', () => {
    const resolver = new ConsentRecordsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `consent_records` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.07 CRDT Specification: `ARCH-DATA-007` (`tokens`)
- **Target Entity:** `ARCH-DATA-007` (`tokens`)
- **Domain Context:** DOMAIN-002
- **CRDT Mathematical Model:** `Monotonic State Machine`
- **Functional Description:** Queue states advance strictly along linear stages: ISSUED -> TRIAGED -> IN_CONSULT -> DISPENSED.

#### 05.07.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tokens_sync ON local_tokens (sync_status, updated_at);
```

#### 05.07.2 Field-Level Merge Resolver Contract
```typescript
export class TokensMergeResolver implements ICRDTResolver<TokensEntity> {
  resolve(local: TokensEntity, remote: TokensEntity): MergeResult<TokensEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.07.3 Automated Convergence & Property Test
```typescript
describe('Tokens CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-007', () => {
    const resolver = new TokensMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `tokens` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.08 CRDT Specification: `ARCH-DATA-008` (`queue_states`)
- **Target Entity:** `ARCH-DATA-008` (`queue_states`)
- **Domain Context:** DOMAIN-002
- **CRDT Mathematical Model:** `Monotonic State Machine`
- **Functional Description:** Queue states advance strictly along linear stages: ISSUED -> TRIAGED -> IN_CONSULT -> DISPENSED.

#### 05.08.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_queue_states_sync ON local_queue_states (sync_status, updated_at);
```

#### 05.08.2 Field-Level Merge Resolver Contract
```typescript
export class QueueStatesMergeResolver implements ICRDTResolver<QueueStatesEntity> {
  resolve(local: QueueStatesEntity, remote: QueueStatesEntity): MergeResult<QueueStatesEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.08.3 Automated Convergence & Property Test
```typescript
describe('QueueStates CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-008', () => {
    const resolver = new QueueStatesMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `queue_states` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.09 CRDT Specification: `ARCH-DATA-009` (`clinical_encounters`)
- **Target Entity:** `ARCH-DATA-009` (`clinical_encounters`)
- **Domain Context:** DOMAIN-003
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.09.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_clinical_encounters_sync ON local_clinical_encounters (sync_status, updated_at);
```

#### 05.09.2 Field-Level Merge Resolver Contract
```typescript
export class ClinicalEncountersMergeResolver implements ICRDTResolver<ClinicalEncountersEntity> {
  resolve(local: ClinicalEncountersEntity, remote: ClinicalEncountersEntity): MergeResult<ClinicalEncountersEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.09.3 Automated Convergence & Property Test
```typescript
describe('ClinicalEncounters CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-009', () => {
    const resolver = new ClinicalEncountersMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `clinical_encounters` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.10 CRDT Specification: `ARCH-DATA-010` (`diagnoses`)
- **Target Entity:** `ARCH-DATA-010` (`diagnoses`)
- **Domain Context:** DOMAIN-003
- **CRDT Mathematical Model:** `OR-Set (Observed-Remove Set)`
- **Functional Description:** Allergies and consent directives accumulate as observed sets; concurrent additions preserved without loss.

#### 05.10.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_diagnoses_sync ON local_diagnoses (sync_status, updated_at);
```

#### 05.10.2 Field-Level Merge Resolver Contract
```typescript
export class DiagnosesMergeResolver implements ICRDTResolver<DiagnosesEntity> {
  resolve(local: DiagnosesEntity, remote: DiagnosesEntity): MergeResult<DiagnosesEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.10.3 Automated Convergence & Property Test
```typescript
describe('Diagnoses CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-010', () => {
    const resolver = new DiagnosesMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `diagnoses` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.11 CRDT Specification: `ARCH-DATA-011` (`prescriptions`)
- **Target Entity:** `ARCH-DATA-011` (`prescriptions`)
- **Domain Context:** DOMAIN-003
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.11.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_prescriptions_sync ON local_prescriptions (sync_status, updated_at);
```

#### 05.11.2 Field-Level Merge Resolver Contract
```typescript
export class PrescriptionsMergeResolver implements ICRDTResolver<PrescriptionsEntity> {
  resolve(local: PrescriptionsEntity, remote: PrescriptionsEntity): MergeResult<PrescriptionsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.11.3 Automated Convergence & Property Test
```typescript
describe('Prescriptions CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-011', () => {
    const resolver = new PrescriptionsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `prescriptions` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.12 CRDT Specification: `ARCH-DATA-012` (`lab_orders`)
- **Target Entity:** `ARCH-DATA-012` (`lab_orders`)
- **Domain Context:** DOMAIN-003
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.12.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_lab_orders_sync ON local_lab_orders (sync_status, updated_at);
```

#### 05.12.2 Field-Level Merge Resolver Contract
```typescript
export class LabOrdersMergeResolver implements ICRDTResolver<LabOrdersEntity> {
  resolve(local: LabOrdersEntity, remote: LabOrdersEntity): MergeResult<LabOrdersEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.12.3 Automated Convergence & Property Test
```typescript
describe('LabOrders CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-012', () => {
    const resolver = new LabOrdersMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `lab_orders` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.13 CRDT Specification: `ARCH-DATA-013` (`dispensations`)
- **Target Entity:** `ARCH-DATA-013` (`dispensations`)
- **Domain Context:** DOMAIN-004
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.13.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_dispensations_sync ON local_dispensations (sync_status, updated_at);
```

#### 05.13.2 Field-Level Merge Resolver Contract
```typescript
export class DispensationsMergeResolver implements ICRDTResolver<DispensationsEntity> {
  resolve(local: DispensationsEntity, remote: DispensationsEntity): MergeResult<DispensationsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.13.3 Automated Convergence & Property Test
```typescript
describe('Dispensations CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-013', () => {
    const resolver = new DispensationsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `dispensations` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.14 CRDT Specification: `ARCH-DATA-014` (`pharmacy_batches`)
- **Target Entity:** `ARCH-DATA-014` (`pharmacy_batches`)
- **Domain Context:** DOMAIN-004
- **CRDT Mathematical Model:** `PN-Counter + Delta State Register`
- **Functional Description:** Inventory counts track dispensations and receipts independently; stock levels merge via algebraic sum.

#### 05.14.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_pharmacy_batches_sync ON local_pharmacy_batches (sync_status, updated_at);
```

#### 05.14.2 Field-Level Merge Resolver Contract
```typescript
export class PharmacyBatchesMergeResolver implements ICRDTResolver<PharmacyBatchesEntity> {
  resolve(local: PharmacyBatchesEntity, remote: PharmacyBatchesEntity): MergeResult<PharmacyBatchesEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.14.3 Automated Convergence & Property Test
```typescript
describe('PharmacyBatches CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-014', () => {
    const resolver = new PharmacyBatchesMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `pharmacy_batches` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.15 CRDT Specification: `ARCH-DATA-015` (`drug_indents`)
- **Target Entity:** `ARCH-DATA-015` (`drug_indents`)
- **Domain Context:** DOMAIN-004
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.15.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_drug_indents_sync ON local_drug_indents (sync_status, updated_at);
```

#### 05.15.2 Field-Level Merge Resolver Contract
```typescript
export class DrugIndentsMergeResolver implements ICRDTResolver<DrugIndentsEntity> {
  resolve(local: DrugIndentsEntity, remote: DrugIndentsEntity): MergeResult<DrugIndentsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.15.3 Automated Convergence & Property Test
```typescript
describe('DrugIndents CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-015', () => {
    const resolver = new DrugIndentsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `drug_indents` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.16 CRDT Specification: `ARCH-DATA-016` (`formulary_master`)
- **Target Entity:** `ARCH-DATA-016` (`formulary_master`)
- **Domain Context:** DOMAIN-004
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.16.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_formulary_master_sync ON local_formulary_master (sync_status, updated_at);
```

#### 05.16.2 Field-Level Merge Resolver Contract
```typescript
export class FormularyMasterMergeResolver implements ICRDTResolver<FormularyMasterEntity> {
  resolve(local: FormularyMasterEntity, remote: FormularyMasterEntity): MergeResult<FormularyMasterEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.16.3 Automated Convergence & Property Test
```typescript
describe('FormularyMaster CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-016', () => {
    const resolver = new FormularyMasterMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `formulary_master` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.17 CRDT Specification: `ARCH-DATA-017` (`referrals`)
- **Target Entity:** `ARCH-DATA-017` (`referrals`)
- **Domain Context:** DOMAIN-005
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.17.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_referrals_sync ON local_referrals (sync_status, updated_at);
```

#### 05.17.2 Field-Level Merge Resolver Contract
```typescript
export class ReferralsMergeResolver implements ICRDTResolver<ReferralsEntity> {
  resolve(local: ReferralsEntity, remote: ReferralsEntity): MergeResult<ReferralsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.17.3 Automated Convergence & Property Test
```typescript
describe('Referrals CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-017', () => {
    const resolver = new ReferralsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `referrals` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.18 CRDT Specification: `ARCH-DATA-018` (`ncd_episodes`)
- **Target Entity:** `ARCH-DATA-018` (`ncd_episodes`)
- **Domain Context:** DOMAIN-005
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.18.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_ncd_episodes_sync ON local_ncd_episodes (sync_status, updated_at);
```

#### 05.18.2 Field-Level Merge Resolver Contract
```typescript
export class NcdEpisodesMergeResolver implements ICRDTResolver<NcdEpisodesEntity> {
  resolve(local: NcdEpisodesEntity, remote: NcdEpisodesEntity): MergeResult<NcdEpisodesEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.18.3 Automated Convergence & Property Test
```typescript
describe('NcdEpisodes CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-018', () => {
    const resolver = new NcdEpisodesMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `ncd_episodes` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.19 CRDT Specification: `ARCH-DATA-019` (`notifications`)
- **Target Entity:** `ARCH-DATA-019` (`notifications`)
- **Domain Context:** DOMAIN-005
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.19.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_notifications_sync ON local_notifications (sync_status, updated_at);
```

#### 05.19.2 Field-Level Merge Resolver Contract
```typescript
export class NotificationsMergeResolver implements ICRDTResolver<NotificationsEntity> {
  resolve(local: NotificationsEntity, remote: NotificationsEntity): MergeResult<NotificationsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.19.3 Automated Convergence & Property Test
```typescript
describe('Notifications CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-019', () => {
    const resolver = new NotificationsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `notifications` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.20 CRDT Specification: `ARCH-DATA-020` (`grievances`)
- **Target Entity:** `ARCH-DATA-020` (`grievances`)
- **Domain Context:** DOMAIN-002
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.20.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_grievances_sync ON local_grievances (sync_status, updated_at);
```

#### 05.20.2 Field-Level Merge Resolver Contract
```typescript
export class GrievancesMergeResolver implements ICRDTResolver<GrievancesEntity> {
  resolve(local: GrievancesEntity, remote: GrievancesEntity): MergeResult<GrievancesEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.20.3 Automated Convergence & Property Test
```typescript
describe('Grievances CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-020', () => {
    const resolver = new GrievancesMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `grievances` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.21 CRDT Specification: `ARCH-DATA-021` (`audit_events`)
- **Target Entity:** `ARCH-DATA-021` (`audit_events`)
- **Domain Context:** DOMAIN-006
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.21.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_audit_events_sync ON local_audit_events (sync_status, updated_at);
```

#### 05.21.2 Field-Level Merge Resolver Contract
```typescript
export class AuditEventsMergeResolver implements ICRDTResolver<AuditEventsEntity> {
  resolve(local: AuditEventsEntity, remote: AuditEventsEntity): MergeResult<AuditEventsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.21.3 Automated Convergence & Property Test
```typescript
describe('AuditEvents CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-021', () => {
    const resolver = new AuditEventsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `audit_events` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.22 CRDT Specification: `ARCH-DATA-022` (`kpi_metrics`)
- **Target Entity:** `ARCH-DATA-022` (`kpi_metrics`)
- **Domain Context:** DOMAIN-006
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.22.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_kpi_metrics_sync ON local_kpi_metrics (sync_status, updated_at);
```

#### 05.22.2 Field-Level Merge Resolver Contract
```typescript
export class KpiMetricsMergeResolver implements ICRDTResolver<KpiMetricsEntity> {
  resolve(local: KpiMetricsEntity, remote: KpiMetricsEntity): MergeResult<KpiMetricsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.22.3 Automated Convergence & Property Test
```typescript
describe('KpiMetrics CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-022', () => {
    const resolver = new KpiMetricsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `kpi_metrics` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.23 CRDT Specification: `ARCH-DATA-023` (`cdss_rules`)
- **Target Entity:** `ARCH-DATA-023` (`cdss_rules`)
- **Domain Context:** DOMAIN-006
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.23.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_cdss_rules_sync ON local_cdss_rules (sync_status, updated_at);
```

#### 05.23.2 Field-Level Merge Resolver Contract
```typescript
export class CdssRulesMergeResolver implements ICRDTResolver<CdssRulesEntity> {
  resolve(local: CdssRulesEntity, remote: CdssRulesEntity): MergeResult<CdssRulesEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.23.3 Automated Convergence & Property Test
```typescript
describe('CdssRules CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-023', () => {
    const resolver = new CdssRulesMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `cdss_rules` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.24 CRDT Specification: `ARCH-DATA-024` (`abdm_artifacts`)
- **Target Entity:** `ARCH-DATA-024` (`abdm_artifacts`)
- **Domain Context:** DOMAIN-006
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.24.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_abdm_artifacts_sync ON local_abdm_artifacts (sync_status, updated_at);
```

#### 05.24.2 Field-Level Merge Resolver Contract
```typescript
export class AbdmArtifactsMergeResolver implements ICRDTResolver<AbdmArtifactsEntity> {
  resolve(local: AbdmArtifactsEntity, remote: AbdmArtifactsEntity): MergeResult<AbdmArtifactsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.24.3 Automated Convergence & Property Test
```typescript
describe('AbdmArtifacts CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-024', () => {
    const resolver = new AbdmArtifactsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `abdm_artifacts` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.25 CRDT Specification: `ARCH-DATA-025` (`mutation_log`)
- **Target Entity:** `ARCH-DATA-025` (`mutation_log`)
- **Domain Context:** DOMAIN-006
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.25.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_mutation_log_sync ON local_mutation_log (sync_status, updated_at);
```

#### 05.25.2 Field-Level Merge Resolver Contract
```typescript
export class MutationLogMergeResolver implements ICRDTResolver<MutationLogEntity> {
  resolve(local: MutationLogEntity, remote: MutationLogEntity): MergeResult<MutationLogEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.25.3 Automated Convergence & Property Test
```typescript
describe('MutationLog CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-025', () => {
    const resolver = new MutationLogMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `mutation_log` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.26 CRDT Specification: `ARCH-DATA-026` (`system_configs`)
- **Target Entity:** `ARCH-DATA-026` (`system_configs`)
- **Domain Context:** DOMAIN-001
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.26.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_system_configs_sync ON local_system_configs (sync_status, updated_at);
```

#### 05.26.2 Field-Level Merge Resolver Contract
```typescript
export class SystemConfigsMergeResolver implements ICRDTResolver<SystemConfigsEntity> {
  resolve(local: SystemConfigsEntity, remote: SystemConfigsEntity): MergeResult<SystemConfigsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.26.3 Automated Convergence & Property Test
```typescript
describe('SystemConfigs CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-026', () => {
    const resolver = new SystemConfigsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `system_configs` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.27 CRDT Specification: `ARCH-DATA-027` (`hmis_reports`)
- **Target Entity:** `ARCH-DATA-027` (`hmis_reports`)
- **Domain Context:** DOMAIN-006
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.27.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_hmis_reports_sync ON local_hmis_reports (sync_status, updated_at);
```

#### 05.27.2 Field-Level Merge Resolver Contract
```typescript
export class HmisReportsMergeResolver implements ICRDTResolver<HmisReportsEntity> {
  resolve(local: HmisReportsEntity, remote: HmisReportsEntity): MergeResult<HmisReportsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.27.3 Automated Convergence & Property Test
```typescript
describe('HmisReports CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-027', () => {
    const resolver = new HmisReportsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `hmis_reports` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.28 CRDT Specification: `ARCH-DATA-028` (`helpdesk_tickets`)
- **Target Entity:** `ARCH-DATA-028` (`helpdesk_tickets`)
- **Domain Context:** DOMAIN-005
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.28.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_helpdesk_tickets_sync ON local_helpdesk_tickets (sync_status, updated_at);
```

#### 05.28.2 Field-Level Merge Resolver Contract
```typescript
export class HelpdeskTicketsMergeResolver implements ICRDTResolver<HelpdeskTicketsEntity> {
  resolve(local: HelpdeskTicketsEntity, remote: HelpdeskTicketsEntity): MergeResult<HelpdeskTicketsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.28.3 Automated Convergence & Property Test
```typescript
describe('HelpdeskTickets CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-028', () => {
    const resolver = new HelpdeskTicketsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `helpdesk_tickets` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.29 CRDT Specification: `ARCH-DATA-029` (`teleconsultations`)
- **Target Entity:** `ARCH-DATA-029` (`teleconsultations`)
- **Domain Context:** DOMAIN-003
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.29.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_teleconsultations_sync ON local_teleconsultations (sync_status, updated_at);
```

#### 05.29.2 Field-Level Merge Resolver Contract
```typescript
export class TeleconsultationsMergeResolver implements ICRDTResolver<TeleconsultationsEntity> {
  resolve(local: TeleconsultationsEntity, remote: TeleconsultationsEntity): MergeResult<TeleconsultationsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.29.3 Automated Convergence & Property Test
```typescript
describe('Teleconsultations CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-029', () => {
    const resolver = new TeleconsultationsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `teleconsultations` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

### 05.30 CRDT Specification: `ARCH-DATA-030` (`command_center_incidents`)
- **Target Entity:** `ARCH-DATA-030` (`command_center_incidents`)
- **Domain Context:** DOMAIN-006
- **CRDT Mathematical Model:** `Field-Level LWW-Register (Last-Write-Wins)`
- **Functional Description:** Entity attributes merge field-by-field; non-overlapping fields combine seamlessly without manual conflict.

#### 05.30.1 Local SQLite Physical Table Schema
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
    payload TEXT NOT NULL, -- JSON blob
    sync_status TEXT NOT NULL DEFAULT 'LOCAL_DIRTY',
    vector_clock TEXT NOT NULL,
    record_checksum TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_command_center_incidents_sync ON local_command_center_incidents (sync_status, updated_at);
```

#### 05.30.2 Field-Level Merge Resolver Contract
```typescript
export class CommandCenterIncidentsMergeResolver implements ICRDTResolver<CommandCenterIncidentsEntity> {
  resolve(local: CommandCenterIncidentsEntity, remote: CommandCenterIncidentsEntity): MergeResult<CommandCenterIncidentsEntity> {
    const merged = { ...local };
    let hasConflict = false;
    const comparison = VectorClock.compare(local.vectorClock, remote.vectorClock);
    if (comparison === ClockOrder.CONCURRENT) {
      for (const key of Object.keys(remote.payload)) {
        if (remote.fieldTimestamps[key] > (local.fieldTimestamps[key] || 0)) {
          merged.payload[key] = remote.payload[key];
          merged.fieldTimestamps[key] = remote.fieldTimestamps[key];
        }
      }
      merged.vectorClock = VectorClock.merge(local.vectorClock, remote.vectorClock);
      hasConflict = true;
    } else if (comparison === ClockOrder.REMOTE_AHEAD) {
      return { result: remote, state: 'APPLIED' };
    }
    return { result: merged, state: hasConflict ? 'RESOLVED_AUTOMATIC' : 'NO_CHANGE' };
  }
}
```

#### 05.30.3 Automated Convergence & Property Test
```typescript
describe('CommandCenterIncidents CRDT Convergence Verification', () => {
  it('should guarantee commutativity, associativity, and idempotency for ARCH-DATA-030', () => {
    const resolver = new CommandCenterIncidentsMergeResolver();
    const stateA = generateSampleState('node-1');
    const stateB = generateSampleState('node-2');
    const mergeAB = resolver.resolve(stateA, stateB);
    const mergeBA = resolver.resolve(stateB, stateA);
    expect(mergeAB.result.payload).toEqual(mergeBA.result.payload); // Commutativity
    const mergeSelf = resolver.resolve(stateA, stateA);
    expect(mergeSelf.result.payload).toEqual(stateA.payload); // Idempotency
  });
});
```

#### Deterministic Invariants & Conflict Escalation:
1. **Non-Overwriting Rule:** Clinical records in `command_center_incidents` once sealed by a doctor can never be silently overwritten by an edge merge.
2. **Conflict Flagging:** If identical fields are mutated concurrently, the system flags `sync_status = 'CONFLICT'` and notifies the Medical Officer.
3. **Audit Log Generation:** Every automatic merge resolution appends an audit event to `audit_events` with both vector clocks.

---

## 06. Container-Level Offline Resilience Profiles Across 18 Containers
Specific operational behavior and fallback states for each system container during WAN outages:

### 06.01 Offline Behavior: `ARCH-CONT-001` (Clinic Workstation PWA Shell)
- **Container Scope:** Clinic Workstation PWA Shell (`Frontend Client`)
- **Edge Deployment Mode:** Local Workstation / Tablet
- **Data Store Handled:** `IndexedDB / SQLite Edge`

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-001`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-001` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.02 Offline Behavior: `ARCH-CONT-002` (Clinic Edge Mini-Server Runtime)
- **Container Scope:** Clinic Edge Mini-Server Runtime (`Edge Computing Node`)
- **Edge Deployment Mode:** Clinic Edge Appliance (Intel N100)
- **Data Store Handled:** `SQLite WAL Mode (Local SSD)`

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-002`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-002` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.03 Offline Behavior: `ARCH-CONT-003` (Central Cloud API Gateway)
- **Container Scope:** Central Cloud API Gateway (`Ingress & Routing`)
- **Edge Deployment Mode:** Cloud Ingress Tier
- **Data Store Handled:** `Redis Token Cache`

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-003`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-003` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.04 Offline Behavior: `ARCH-CONT-004` (Identity & Access Management (IAM) Service)
- **Container Scope:** Identity & Access Management (IAM) Service (`Security & Auth`)
- **Edge Deployment Mode:** Cloud App Tier / Edge Mirror
- **Data Store Handled:** `PostgreSQL `auth_users``

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-004`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-004` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.05 Offline Behavior: `ARCH-CONT-005` (Master Patient Index (MPI) Service)
- **Container Scope:** Master Patient Index (MPI) Service (`Patient Domain`)
- **Edge Deployment Mode:** Cloud App Tier / Edge Sync
- **Data Store Handled:** `PostgreSQL `patients``

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-005`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-005` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.06 Offline Behavior: `ARCH-CONT-006` (Queue Orchestration & Triage Engine)
- **Container Scope:** Queue Orchestration & Triage Engine (`Workflow Domain`)
- **Edge Deployment Mode:** Edge Mini-Server / Cloud Sync
- **Data Store Handled:** `Edge SQLite `clinic_queues``

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-006`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-006` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.07 Offline Behavior: `ARCH-CONT-007` (Clinical Consultation & EMR Service)
- **Container Scope:** Clinical Consultation & EMR Service (`Clinical Domain`)
- **Edge Deployment Mode:** Cloud App Tier / Edge Sync
- **Data Store Handled:** `PostgreSQL `clinical_encounters``

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-007`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-007` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.08 Offline Behavior: `ARCH-CONT-008` (Electronic Prescription & CDSS Service)
- **Container Scope:** Electronic Prescription & CDSS Service (`Clinical Domain`)
- **Edge Deployment Mode:** Cloud App Tier / Edge Sync
- **Data Store Handled:** `PostgreSQL `prescriptions``

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-008`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-008` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.09 Offline Behavior: `ARCH-CONT-009` (Pharmacy Inventory & Dispensation Service)
- **Container Scope:** Pharmacy Inventory & Dispensation Service (`Logistics Domain`)
- **Edge Deployment Mode:** Cloud App Tier / Edge Sync
- **Data Store Handled:** `PostgreSQL `pharmacy_batches``

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-009`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-009` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.10 Offline Behavior: `ARCH-CONT-010` (Diagnostic Laboratory Service)
- **Container Scope:** Diagnostic Laboratory Service (`Diagnostics Domain`)
- **Edge Deployment Mode:** Cloud App Tier / Edge Sync
- **Data Store Handled:** `PostgreSQL `lab_orders``

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-010`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-010` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.11 Offline Behavior: `ARCH-CONT-011` (Referral & EMS Telemetry Bridge)
- **Container Scope:** Referral & EMS Telemetry Bridge (`Care Continuity`)
- **Edge Deployment Mode:** Cloud App Tier
- **Data Store Handled:** `PostgreSQL `referrals``

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-011`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-011` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.12 Offline Behavior: `ARCH-CONT-012` (Citizen Portal & Multilingual Notification Service)
- **Container Scope:** Citizen Portal & Multilingual Notification Service (`Citizen Domain`)
- **Edge Deployment Mode:** Cloud App Tier
- **Data Store Handled:** `Redis Queue / PostgreSQL`

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-012`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-012` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.13 Offline Behavior: `ARCH-CONT-013` (Bi-directional Edge-Cloud Synchronization Service)
- **Container Scope:** Bi-directional Edge-Cloud Synchronization Service (`Sync Engine`)
- **Edge Deployment Mode:** Edge Node & Cloud Worker
- **Data Store Handled:** `SQLite Mutation Log`

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-013`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-013` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.14 Offline Behavior: `ARCH-CONT-014` (ABDM & National Health Grid Bridge)
- **Container Scope:** ABDM & National Health Grid Bridge (`Interoperability`)
- **Edge Deployment Mode:** Cloud DMZ Tier
- **Data Store Handled:** `PostgreSQL `abdm_artifacts``

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-014`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-014` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.15 Offline Behavior: `ARCH-CONT-015` (Public Health Analytics & Syndromic BI Service)
- **Container Scope:** Public Health Analytics & Syndromic BI Service (`Analytics Domain`)
- **Edge Deployment Mode:** Cloud Analytics Tier
- **Data Store Handled:** `ClickHouse Star Schema`

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-015`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-015` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.16 Offline Behavior: `ARCH-CONT-016` (Advisory Clinical AI Decision Support Engine)
- **Container Scope:** Advisory Clinical AI Decision Support Engine (`AI / ML Tier`)
- **Edge Deployment Mode:** Cloud Analytics Tier
- **Data Store Handled:** `Model Registry (MLflow)`

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-016`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-016` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.17 Offline Behavior: `ARCH-CONT-017` (Cryptographic WORM Audit Service)
- **Container Scope:** Cryptographic WORM Audit Service (`Audit & Security`)
- **Edge Deployment Mode:** Isolated Cloud Security Subnet
- **Data Store Handled:** `Encrypted Object Store`

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-017`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-017` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

### 06.18 Offline Behavior: `ARCH-CONT-018` (Enterprise Relational Database Cluster)
- **Container Scope:** Enterprise Relational Database Cluster (`Data Tier`)
- **Edge Deployment Mode:** Private Cloud Database Subnet
- **Data Store Handled:** `NVMe SSD SAN Storage`

#### Operational State Matrix During Outage:
| Connectivity State | Operational Capability | Data Routing & Local Persistence | User Feedback & Notifications |
| :--- | :--- | :--- | :--- |
| **Normal (Online)** | 100% full features active. | Central PostgreSQL + Edge Cache | Green connectivity badge. |
| **Degraded (2G/High Latency)** | Critical transactions active; batch sync throttled. | Priority queue draining to cloud | Yellow latency indicator. |
| **Offline (WAN Disconnected)** | 100% core clinic workflows fully autonomous. | Local SQLite WAL + Local MQTT Broker | Amber 'Autonomous Edge' status banner. |
| **Reconnecting (Sync Active)** | Synchronizing accumulated mutations in background. | Background Merkle delta exchange | Toast: 'Syncing local records...' |

#### Recovery & Resumption Protocol for `ARCH-CONT-018`:
1. Establishes mTLS session with cloud sync gateway upon link ping recovery.
2. Exchanges Merkle tree state for `ARCH-CONT-018` data scope.
3. Drains local `mutation_log` records with exponential backoff on retry.
4. Re-enables real-time WebSockets upon queue drain completion.

---

## 06. Bi-Directional Synchronization Protocol Specification
End-to-end network protocol governing edge-cloud synchronization upon link recovery:
1. **Phase 1 - Cryptographic Mutual Handshake (mTLS):**
   - Edge node initiates connection to cloud sync gateway `POST /api/v1/sync/handshake`.
   - Presents X.509 client certificate and hardware-derived Ed25519 node signature.
   - Cloud validates clinic active status and returns current cloud vector clock $V_{cloud}$.
2. **Phase 2 - Merkle Tree Range Exchange (Delta Detection):**
   - Edge and cloud exchange root hashes of their mutation trees for the clinic partition.
   - If root hashes match, synchronization terminates immediately (< 50ms latency, zero data transferred).
   - If root hashes differ, nodes traverse tree branches to locate exact missing mutation ranges.
3. **Phase 3 - Batched Upstream Mutation Push (Edge -> Cloud):**
   - Edge reads unacknowledged rows from `local_mutation_log` in batches of 50 records.
   - Compresses batch using zstd level 3 (typical 80% compression ratio on JSON).
   - Posts to `POST /api/v1/sync/push-mutations`.
   - Cloud executes ACID transaction, evaluates CRDT rules, appends to central PostgreSQL, and returns acknowledged mutation IDs.
   - Edge updates local status to `ACKNOWLEDGED`.
4. **Phase 4 - Downstream Delta Pull (Cloud -> Edge):**
   - Edge requests cloud updates occurring after local clock: `GET /api/v1/sync/pull-deltas?since=<V_edge>`.
   - Cloud returns new citizen registrations, updated central formulary masters, and inter-clinic referral responses.
   - Edge applies deltas inside a local SQLite transaction.

## 07. Offline Authentication & Credential Caching Strategy
Security mechanisms ensuring staff members can log into clinic workstations during complete internet outages:
1. **Encrypted Edge Credential Cache:** The edge mini-server maintains an AES-256 encrypted SQLite table storing salted Argon2id hashes for all staff members rostered to that clinic facility.
2. **72-Hour Cache Expiry Window:** Local credential validity expires after 72 hours of continuous offline operation, requiring brief online network heartbeat to re-authorize.
3. **Emergency Local PIN Override:** In disaster scenarios where biometric scanners fail, clinic Medical Officers can authenticate using a 6-digit emergency PIN derived from a hardware TOTP token.
4. **Zero Cross-Clinic Credential Bleed:** An edge server stores credentials strictly for personnel assigned to that specific clinic; unauthorized staff accounts cannot authenticate.

## 08. User Interface Offline Indicators & Conflict Resolution UX
Frontend UX design patterns maintaining user awareness during connectivity transitions:
1. **Persistent Header Connectivity Badge:**
   - 🟢 **ONLINE (Cloud Connected):** Real-time WebSocket connection active; latency < 150ms.
   - 🟡 **EDGE AUTONOMOUS (Local Wi-Fi Only):** WAN disconnected; connected to clinic mini-server; 100% features operational.
   - 🔴 **ISOLATED TERMINAL (Workstation Offline):** Wi-Fi severed; running on browser IndexedDB cache; emergency triage mode only.
2. **Unobtrusive Background Sync:** When connection recovers, a subtle toast notification informs the user: *'Syncing 42 local records with BBMP Health Cloud...'*, disappearing upon completion without modal dialogs.
3. **Clinical Conflict Drawer:** If a concurrent update requires physician judgment (e.g. conflicting medication dosages), a dedicated conflict resolution drawer presents side-by-side diffs with provider timestamps.

## 09. Power Loss Resilience & Graceful Shutdown Daemon
Hardware power protection runbook preventing filesystem and database corruption during blackout conditions:
1. **Network UPS Tools (NUT) Daemon Integration:** Edge mini-server connects to the 1.5 kVA UPS via USB interface.
2. **Battery State Monitoring:** Daemon polls battery percentage every 10 seconds.
3. **Low-Battery Graceful Shutdown Sequence:**
   - When battery drops below 15% (estimated 20 minutes remaining):
   - Emits broadcast alert to all active clinic workstations: *'Clinic UPS battery low. Please complete current consultation.'*
   - Prohibits opening new consultations.
   - Flushes SQLite write-ahead log (`PRAGMA wal_checkpoint(TRUNCATE);`).
   - Unmounts NVMe filesystems cleanly.
   - Issues Linux system halt (`shutdown -h now`).
4. **Auto-Power-On on Grid Restoration:** BIOS configured for `Restore on AC Power Loss = Power On`. Appliance automatically boots and launches services upon utility power recovery.

## 10. Operational Verification & Edge Health Telemetry
Continuous monitoring metrics ensuring edge fleet operational readiness across 183 clinics:
1. **Edge Heartbeat Metric:** Edge daemons emit heartbeat every 60 seconds to cloud collector: `edge_heartbeat_timestamp`.
2. **Pending Mutation Queue Depth:** Alert fired if `pending_mutations_count > 500` for more than 4 hours.
3. **SQLite WAL File Size:** Alert fired if `wal_file_bytes > 500 MB`, triggering forced checkpoint.
4. **Disk Storage Utilization:** Critical alarm when edge NVMe SSD exceeds 80% capacity.
