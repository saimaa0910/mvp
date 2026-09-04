# Namma Clinic Digital Health & Operations Platform
## Security & Access Governance: Master Role × Module × Capability Access Matrix

| Metadata Element | Specification Baseline |
| :--- | :--- |
| **Document Identifier** | `DOC-PROD-003-RMM` |
| **Document Title** | Master Role-Based Access Control (RBAC), Attribute-Based Access Control (ABAC) & Entitlement Matrix |
| **Project Code** | `NAMMA-CLINIC-PLATFORM-2026` |
| **Document Version** | `v1.0.0-PROD-BASELINE` |
| **Lifecycle Status** | `APPROVED & RATIFIED` |
| **Role Baseline** | Exactly 30 Formally Modeled Project & Operational Roles (`ROLE-001` to `ROLE-030`) |
| **Module Baseline** | Exactly 30 Production Modules (`MODULE-001` to `MODULE-030`) |
| **Capability Baseline**| Exactly 180 Functional Capabilities (`CAPABILITY-001` to `CAPABILITY-180`) |
| **Matrix Volume** | Exactly 900 Explicit Role-Module Intersections Evaluated |
| **Access Classifications** | `NONE`, `VIEW`, `CREATE`, `EDIT`, `DELETE`, `APPROVE`, `EXECUTE`, `ADMIN`, `AUDIT` |
| **Governance Policies** | Separation of Duties (SoD), Break-Glass Emergency Overrides, Offline Edge Operation |
| **Upstream Anchors** | `docs/00-project-baseline/`, `docs/01-project-management/08-role-and-responsibility-matrix.md`, `docs/02-requirements/` |
| **Downstream Consuming Phases** | Security Architecture (`05-architecture`), API Gateway Auth Middleware (`07-api`), UI Screen Access (`09-frontend`) |

---

## 1. Executive Summary & Security Access Principles
The **Role × Module × Capability Access Matrix** defines the authoritative security boundary, entitlement rights, and operational authority for all 30 user cadres across the Namma Clinic Platform. In a municipal primary healthcare network handling confidential citizen Protected Health Information (PHI) and prescription-controlled pharmaceuticals, access control is the primary defense against medical malpractice, identity theft, unauthorized disclosure, and inventory pilferage.

### 1.1 The Golden Rules of Access Governance
1. **Principle of Least Privilege (PoLP):** Users are granted strictly the minimal permissions necessary to execute their physical workstation duty. A front desk clerk has zero access to clinical diagnostic notes; a doctor cannot decrement pharmacy warehouse stock.
2. **Separation of Duties (SoD):** High-risk, conflicting operational responsibilities are cryptographically bifurcated across distinct roles. The Prescribing Doctor (`ROLE-015`) cannot dispense medication; the Dispensing Pharmacist (`ROLE-017`) cannot author or amend prescriptions.
3. **Cryptographic ABAC Enforcement:** In addition to role claims (RBAC), access is gated by dynamic environmental attributes (ABAC): assigned clinic facility ID, active duty shift status, physical LAN IP subnet, and citizen consent status.
4. **Immutability of Audit Trails:** No role—including Super Administrator (`ROLE-001`) or Lead DBA (`ROLE-008`)—possesses technical authority to delete or modify records in the cryptographic WORM audit ledger (`MODULE-021`).
5. **Deterministic Break-Glass Protocols:** Emergency clinical preemption protocols allow doctors and nurses to override consent barriers during life-threatening trauma resuscitation, with mandatory automated post-hoc audit reviews.

## 2. Master Roles Directory Catalog (ROLE-001 to ROLE-030)
Authoritative catalog of all 30 formally defined enterprise and frontline operational roles:

| Role ID | Role Title | Functional Cadre | Governance Tier | Clinical Authority | Offline Capable | Break-Glass Capable |
| :--- | :--- | :--- | :---: | :--- | :---: | :---: |
| [`ROLE-001`](#role-001) | **Project Executive Sponsor** | `Executive` | `L5-Executive` | Executive Oversight (No direct clinical prescribing) | `False` | `False` |
| [`ROLE-002`](#role-002) | **Clinical Safety Authority** | `Clinical` | `L5-Executive` | Absolute Clinical Safety Authority & Protocol Veto | `False` | `True` |
| [`ROLE-003`](#role-003) | **Lead Delivery Partner / Project Director** | `Management` | `L4-Product` | None | `False` | `False` |
| [`ROLE-004`](#role-004) | **Chief Solution Architect** | `Architecture` | `L3-Architecture` | None | `False` | `False` |
| [`ROLE-005`](#role-005) | **Delivery Project Manager / Agile Coach** | `Management` | `L1-Operational` | None | `False` | `False` |
| [`ROLE-006`](#role-006) | **Lead Backend Engineer** | `Engineering` | `L2-Technical` | None | `False` | `False` |
| [`ROLE-007`](#role-007) | **Lead Frontend Engineer** | `Engineering` | `L2-Technical` | None | `False` | `False` |
| [`ROLE-008`](#role-008) | **Lead Database Administrator (DBA)** | `Data` | `L2-Technical` | None | `False` | `False` |
| [`ROLE-009`](#role-009) | **DevOps & SRE Lead** | `Infrastructure` | `L2-Technical` | None | `False` | `False` |
| [`ROLE-010`](#role-010) | **Quality Assurance Lead** | `Quality` | `L2-Technical` | None | `False` | `False` |
| [`ROLE-011`](#role-011) | **Security & Data Privacy Officer** | `Security` | `L3-Architecture` | Security Audit (No prescribing) | `False` | `False` |
| [`ROLE-012`](#role-012) | **Clinical Safety Specialist (SME)** | `Clinical` | `L3-Architecture` | Protocol Design & Clinical Rule Verification | `False` | `False` |
| [`ROLE-013`](#role-013) | **Public Health Epidemiologist** | `Analytics` | `L3-Architecture` | Population Health Analytics | `False` | `False` |
| [`ROLE-014`](#role-014) | **Frontline Training Coordinator** | `Operations` | `L1-Operational` | Training Sandbox Operations | `False` | `False` |
| [`ROLE-015`](#role-015) | **Zonal Clinic Medical Superintendent** | `Clinical` | `L1-Operational` | Full Clinical Prescribing, Diagnosing & Emergency Break-Glass | `True` | `True` |
| [`ROLE-016`](#role-016) | **Staff Nurse Supervisor** | `Clinical` | `L1-Operational` | Clinical Triage, Vitals Recording, Nursing Administration | `True` | `True` |
| [`ROLE-017`](#role-017) | **Chief Pharmacy Supervisor** | `Pharmacy` | `L1-Operational` | Medication Dispensing & Pharmacy Counseling (Strictly Cannot Prescribe) | `True` | `False` |
| [`ROLE-018`](#role-018) | **Senior Laboratory Supervisor** | `Laboratory` | `L1-Operational` | Diagnostic Test Execution & Result Entry (Cannot Prescribe) | `True` | `False` |
| [`ROLE-019`](#role-019) | **Front Desk Operations Supervisor** | `Operations` | `L1-Operational` | Non-Clinical Intake (No access to detailed clinical diagnoses) | `True` | `False` |
| [`ROLE-020`](#role-020) | **Integration Gateway Specialist** | `Engineering` | `L2-Technical` | None | `False` | `False` |
| [`ROLE-021`](#role-021) | **Data Analytics Engineer** | `Data` | `L2-Technical` | None (Anonymized data only) | `False` | `False` |
| [`ROLE-022`](#role-022) | **UI/UX Accessibility Designer** | `Design` | `L2-Technical` | None | `False` | `False` |
| [`ROLE-023`](#role-023) | **Tier-1/2 Helpdesk Coordinator** | `Support` | `L1-Operational` | None | `False` | `False` |
| [`ROLE-024`](#role-024) | **Field Hardware Support Engineer** | `Support` | `L1-Operational` | None | `True` | `False` |
| [`ROLE-025`](#role-025) | **Municipal Legal & Compliance Counsel** | `Compliance` | `L4-Product` | Legal Compliance Review (No clinical access) | `False` | `False` |
| [`ROLE-026`](#role-026) | **Municipal Finance Auditor** | `Finance` | `L4-Product` | Fiscal Inventory Audit (No patient PHI access) | `False` | `False` |
| [`ROLE-027`](#role-027) | **Release Train Engineer** | `Management` | `L2-Technical` | None | `False` | `False` |
| [`ROLE-028`](#role-028) | **Performance & Chaos Engineer** | `Quality` | `L2-Technical` | None | `False` | `False` |
| [`ROLE-029`](#role-029) | **Kannada Localization Specialist** | `Content` | `L1-Operational` | Localization Content Certification | `False` | `False` |
| [`ROLE-030`](#role-030) | **Documentation & Traceability Auditor** | `Governance` | `L2-Technical` | Governance Audit | `False` | `False` |

## 3. Master 30×30 Role × Module Access Matrix
Comprehensive evaluation of all 900 role-module intersections across the platform. Access levels: `NONE` (Zero access), `VIEW` (Read-only), `CREATE` (Insert new records), `EDIT` (Update existing records), `APPROVE` (Formal signoff/veto), `EXECUTE` (Run operational actions e.g. barcode dispensing), `ADMIN` (Configure module settings), `AUDIT` (Compliance and forensic review):

### 3.1 Role Group Access Matrix (ROLE-001 to ROLE-005)

| Module ID | ROLE-001 (Project Exec) | ROLE-002 (Clinical Saf) | ROLE-003 (Lead Deliver) | ROLE-004 (Chief Soluti) | ROLE-005 (Delivery Pro) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `MODULE-001` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-002` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-003` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-004` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-005` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-006` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-007` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-008` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-009` | **AUDIT** | **APPROVE** | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-010` | **AUDIT** | **APPROVE** | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-011` | **AUDIT** | **APPROVE** | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-012` | **AUDIT** | **APPROVE** | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-013` | **AUDIT** | **AUDIT** | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-014` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-015` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-016` | **AUDIT** | **APPROVE** | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-017` | **AUDIT** | **AUDIT** | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-018` | **AUDIT** | **AUDIT** | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-019` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-020` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-021` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-022` | **AUDIT** | **AUDIT** | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-023` | **AUDIT** | **APPROVE** | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-024` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-025` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-026` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-027` | **AUDIT** | **APPROVE** | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-028` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-029` | **AUDIT** | **APPROVE** | **AUDIT** | **ADMIN** | VIEW |
| `MODULE-030` | **AUDIT** | VIEW | **AUDIT** | **ADMIN** | VIEW |

### 3.2 Role Group Access Matrix (ROLE-006 to ROLE-010)

| Module ID | ROLE-006 (Lead Backend) | ROLE-007 (Lead Fronten) | ROLE-008 (Lead Databas) | ROLE-009 (DevOps & SRE) | ROLE-010 (Quality Assu) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `MODULE-001` | **EDIT** | **EDIT** | **ADMIN** | **ADMIN** | NONE |
| `MODULE-002` | VIEW | VIEW | **ADMIN** | VIEW | NONE |
| `MODULE-003` | **EDIT** | **EDIT** | VIEW | **ADMIN** | NONE |
| `MODULE-004` | **EDIT** | **EDIT** | **ADMIN** | **ADMIN** | NONE |
| `MODULE-005` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-006` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-007` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-008` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-009` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-010` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-011` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-012` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-013` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-014` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-015` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-016` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-017` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-018` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-019` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-020` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-021` | VIEW | VIEW | **ADMIN** | VIEW | NONE |
| `MODULE-022` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-023` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-024` | **EDIT** | **EDIT** | **ADMIN** | **ADMIN** | NONE |
| `MODULE-025` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-026` | **EDIT** | **EDIT** | **ADMIN** | **ADMIN** | NONE |
| `MODULE-027` | VIEW | VIEW | VIEW | **ADMIN** | NONE |
| `MODULE-028` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-029` | VIEW | VIEW | VIEW | VIEW | NONE |
| `MODULE-030` | VIEW | VIEW | VIEW | VIEW | NONE |

### 3.3 Role Group Access Matrix (ROLE-011 to ROLE-015)

| Module ID | ROLE-011 (Security & D) | ROLE-012 (Clinical Saf) | ROLE-013 (Public Healt) | ROLE-014 (Frontline Tr) | ROLE-015 (Zonal Clinic) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `MODULE-001` | **ADMIN** | VIEW | NONE | VIEW | NONE |
| `MODULE-002` | **AUDIT** | VIEW | NONE | VIEW | NONE |
| `MODULE-003` | **AUDIT** | VIEW | NONE | VIEW | NONE |
| `MODULE-004` | **ADMIN** | VIEW | NONE | VIEW | NONE |
| `MODULE-005` | **AUDIT** | VIEW | NONE | VIEW | VIEW |
| `MODULE-006` | **AUDIT** | VIEW | NONE | VIEW | VIEW |
| `MODULE-007` | **ADMIN** | VIEW | NONE | VIEW | VIEW |
| `MODULE-008` | **AUDIT** | VIEW | NONE | VIEW | VIEW |
| `MODULE-009` | **AUDIT** | **AUDIT** | VIEW | VIEW | **EDIT** |
| `MODULE-010` | **AUDIT** | **AUDIT** | VIEW | VIEW | **CREATE** |
| `MODULE-011` | **AUDIT** | **AUDIT** | VIEW | VIEW | **EDIT** |
| `MODULE-012` | **AUDIT** | **AUDIT** | NONE | VIEW | **CREATE** |
| `MODULE-013` | **AUDIT** | **AUDIT** | NONE | VIEW | VIEW |
| `MODULE-014` | **AUDIT** | VIEW | NONE | VIEW | VIEW |
| `MODULE-015` | **AUDIT** | VIEW | NONE | VIEW | NONE |
| `MODULE-016` | **AUDIT** | **AUDIT** | NONE | VIEW | VIEW |
| `MODULE-017` | **AUDIT** | **AUDIT** | NONE | VIEW | **CREATE** |
| `MODULE-018` | **AUDIT** | **AUDIT** | VIEW | VIEW | **CREATE** |
| `MODULE-019` | **AUDIT** | VIEW | NONE | VIEW | NONE |
| `MODULE-020` | **AUDIT** | VIEW | NONE | VIEW | NONE |
| `MODULE-021` | **ADMIN** | VIEW | NONE | VIEW | NONE |
| `MODULE-022` | **AUDIT** | **AUDIT** | **AUDIT** | VIEW | NONE |
| `MODULE-023` | **AUDIT** | **AUDIT** | NONE | VIEW | VIEW |
| `MODULE-024` | **AUDIT** | VIEW | NONE | VIEW | **EXECUTE** |
| `MODULE-025` | **AUDIT** | VIEW | **AUDIT** | VIEW | NONE |
| `MODULE-026` | **ADMIN** | VIEW | NONE | VIEW | NONE |
| `MODULE-027` | **AUDIT** | **AUDIT** | NONE | VIEW | **CREATE** |
| `MODULE-028` | **AUDIT** | VIEW | NONE | VIEW | NONE |
| `MODULE-029` | **AUDIT** | **AUDIT** | NONE | VIEW | **CREATE** |
| `MODULE-030` | **AUDIT** | VIEW | NONE | VIEW | NONE |

### 3.4 Role Group Access Matrix (ROLE-016 to ROLE-020)

| Module ID | ROLE-016 (Staff Nurse ) | ROLE-017 (Chief Pharma) | ROLE-018 (Senior Labor) | ROLE-019 (Front Desk O) | ROLE-020 (Integration ) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `MODULE-001` | NONE | NONE | NONE | NONE | VIEW |
| `MODULE-002` | NONE | NONE | NONE | NONE | VIEW |
| `MODULE-003` | NONE | NONE | NONE | NONE | VIEW |
| `MODULE-004` | NONE | NONE | NONE | NONE | VIEW |
| `MODULE-005` | **CREATE** | VIEW | VIEW | **CREATE** | VIEW |
| `MODULE-006` | NONE | NONE | NONE | **CREATE** | **ADMIN** |
| `MODULE-007` | **CREATE** | NONE | NONE | **CREATE** | VIEW |
| `MODULE-008` | **CREATE** | VIEW | VIEW | **CREATE** | VIEW |
| `MODULE-009` | **CREATE** | NONE | NONE | NONE | VIEW |
| `MODULE-010` | VIEW | NONE | VIEW | NONE | VIEW |
| `MODULE-011` | VIEW | NONE | **CREATE** | NONE | VIEW |
| `MODULE-012` | NONE | VIEW | NONE | NONE | VIEW |
| `MODULE-013` | NONE | **EXECUTE** | NONE | NONE | VIEW |
| `MODULE-014` | VIEW | **CREATE** | VIEW | NONE | VIEW |
| `MODULE-015` | VIEW | **CREATE** | NONE | NONE | VIEW |
| `MODULE-016` | NONE | VIEW | NONE | NONE | VIEW |
| `MODULE-017` | NONE | NONE | NONE | NONE | **ADMIN** |
| `MODULE-018` | VIEW | NONE | NONE | NONE | VIEW |
| `MODULE-019` | NONE | NONE | NONE | NONE | **ADMIN** |
| `MODULE-020` | NONE | NONE | NONE | **CREATE** | **ADMIN** |
| `MODULE-021` | NONE | NONE | NONE | NONE | VIEW |
| `MODULE-022` | NONE | NONE | NONE | NONE | VIEW |
| `MODULE-023` | NONE | NONE | NONE | NONE | VIEW |
| `MODULE-024` | **EXECUTE** | **EXECUTE** | **EXECUTE** | **EXECUTE** | VIEW |
| `MODULE-025` | NONE | NONE | NONE | NONE | **ADMIN** |
| `MODULE-026` | NONE | NONE | NONE | NONE | VIEW |
| `MODULE-027` | VIEW | NONE | NONE | NONE | VIEW |
| `MODULE-028` | NONE | NONE | NONE | NONE | VIEW |
| `MODULE-029` | NONE | NONE | NONE | NONE | VIEW |
| `MODULE-030` | NONE | NONE | NONE | NONE | **ADMIN** |

### 3.5 Role Group Access Matrix (ROLE-021 to ROLE-025)

| Module ID | ROLE-021 (Data Analyti) | ROLE-022 (UI/UX Access) | ROLE-023 (Tier-1/2 Hel) | ROLE-024 (Field Hardwa) | ROLE-025 (Municipal Le) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `MODULE-001` | VIEW | NONE | VIEW | NONE | VIEW |
| `MODULE-002` | VIEW | VIEW | VIEW | NONE | NONE |
| `MODULE-003` | VIEW | VIEW | NONE | NONE | NONE |
| `MODULE-004` | VIEW | NONE | NONE | NONE | VIEW |
| `MODULE-005` | VIEW | VIEW | NONE | NONE | NONE |
| `MODULE-006` | VIEW | NONE | NONE | NONE | NONE |
| `MODULE-007` | VIEW | NONE | NONE | NONE | **AUDIT** |
| `MODULE-008` | VIEW | VIEW | VIEW | NONE | NONE |
| `MODULE-009` | VIEW | NONE | NONE | NONE | NONE |
| `MODULE-010` | VIEW | VIEW | NONE | NONE | NONE |
| `MODULE-011` | VIEW | NONE | NONE | NONE | NONE |
| `MODULE-012` | VIEW | NONE | NONE | NONE | NONE |
| `MODULE-013` | VIEW | NONE | NONE | NONE | NONE |
| `MODULE-014` | VIEW | NONE | NONE | NONE | NONE |
| `MODULE-015` | VIEW | NONE | NONE | NONE | NONE |
| `MODULE-016` | VIEW | NONE | NONE | NONE | NONE |
| `MODULE-017` | VIEW | NONE | NONE | NONE | NONE |
| `MODULE-018` | VIEW | NONE | NONE | NONE | NONE |
| `MODULE-019` | VIEW | VIEW | NONE | NONE | NONE |
| `MODULE-020` | VIEW | NONE | **CREATE** | NONE | **AUDIT** |
| `MODULE-021` | **ADMIN** | NONE | NONE | NONE | **AUDIT** |
| `MODULE-022` | **ADMIN** | NONE | NONE | NONE | NONE |
| `MODULE-023` | VIEW | NONE | NONE | NONE | NONE |
| `MODULE-024` | VIEW | NONE | NONE | **EXECUTE** | NONE |
| `MODULE-025` | **ADMIN** | NONE | NONE | NONE | **AUDIT** |
| `MODULE-026` | VIEW | NONE | NONE | NONE | VIEW |
| `MODULE-027` | VIEW | NONE | NONE | NONE | NONE |
| `MODULE-028` | VIEW | NONE | **CREATE** | **EXECUTE** | NONE |
| `MODULE-029` | VIEW | NONE | NONE | NONE | NONE |
| `MODULE-030` | VIEW | NONE | NONE | NONE | NONE |

### 3.6 Role Group Access Matrix (ROLE-026 to ROLE-030)

| Module ID | ROLE-026 (Municipal Fi) | ROLE-027 (Release Trai) | ROLE-028 (Performance ) | ROLE-029 (Kannada Loca) | ROLE-030 (Documentatio) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `MODULE-001` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-002` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-003` | NONE | **ADMIN** | **EXECUTE** | **EDIT** | **AUDIT** |
| `MODULE-004` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-005` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-006` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-007` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-008` | NONE | VIEW | **EXECUTE** | **EDIT** | **AUDIT** |
| `MODULE-009` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-010` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-011` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-012` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-013` | **AUDIT** | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-014` | **AUDIT** | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-015` | **AUDIT** | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-016` | **AUDIT** | VIEW | **EXECUTE** | **EDIT** | **AUDIT** |
| `MODULE-017` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-018` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-019` | NONE | VIEW | **EXECUTE** | **EDIT** | **AUDIT** |
| `MODULE-020` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-021` | VIEW | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-022` | VIEW | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-023` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-024` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-025` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-026` | NONE | **ADMIN** | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-027` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-028` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-029` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |
| `MODULE-030` | NONE | VIEW | **EXECUTE** | NONE | **AUDIT** |

## 4. Detailed Role Profiles & Entitlement Charters (ROLE-001 to ROLE-030)
Exhaustive specifications for all 30 roles detailing operational mandates, specific permission sets, day-in-the-life routines, ABAC constraints, and security boundaries:

### 4.1 ROLE-001: Project Executive Sponsor

- **Role Identifier:** `ROLE-001` | **Official Title:** **Project Executive Sponsor**
- **Functional Category:** `Executive` | **Governance Tier:** `L5-Executive`
- **Cadre Classification:** Municipal IAS / Special Commissioner (Health)
- **Clinical Prescribing Authority:** Executive Oversight (No direct clinical prescribing)
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
BBMP Special Commissioner (Health) holding ultimate administrative, fiscal, and statutory authority across municipal clinic delivery.

**Primary Operational Focus:** Executive governance, fiscal allocations, statutory policy signoff, inter-agency coordination.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-004` | Clinical & Administrative Staff Directory | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-007` | Patient Token Generation & Station Routing | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-026` | Master System Administration & Feature Flagging | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **AUDIT** | Read, Approve, Audit | Municipal-wide executive view; masked patient PHI; full operational metrics |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `YES` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `YES` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `YES` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `YES` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.2 ROLE-002: Clinical Safety Authority

- **Role Identifier:** `ROLE-002` | **Official Title:** **Clinical Safety Authority**
- **Functional Category:** `Clinical` | **Governance Tier:** `L5-Executive`
- **Cadre Classification:** Chief Health Officer (CHO) / Directorate of Health
- **Clinical Prescribing Authority:** Absolute Clinical Safety Authority & Protocol Veto
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `True`

#### Role Purpose & Strategic Mandate
Chief Health Officer (CHO) holding absolute statutory clinical safety sign-off, protocol veto, and clinical risk governance.

**Primary Operational Focus:** Clinical protocol ratification, CDSS AI guardrail verification, adverse event investigations, clinical veto.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** `MODULE-009`, `MODULE-010`, `MODULE-011`, `MODULE-012`, `MODULE-016`, `MODULE-023`, `MODULE-027`, `MODULE-029`
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **VIEW** | Read | Platform governance view |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **VIEW** | Read | Platform governance view |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **VIEW** | Read | Platform governance view |
| `MODULE-004` | Clinical & Administrative Staff Directory | **VIEW** | Read | Platform governance view |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | Platform governance view |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **VIEW** | Read | Platform governance view |
| `MODULE-007` | Patient Token Generation & Station Routing | **VIEW** | Read | Platform governance view |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | Platform governance view |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **APPROVE** | Read, Approve, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **APPROVE** | Read, Approve, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **APPROVE** | Read, Approve, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **APPROVE** | Read, Approve, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **AUDIT** | Read, Audit | Clinical safety monitoring, pharmacovigilance, referral safety |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read | Platform governance view |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **VIEW** | Read | Platform governance view |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **APPROVE** | Read, Approve, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **AUDIT** | Read, Audit | Clinical safety monitoring, pharmacovigilance, referral safety |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **AUDIT** | Read, Audit | Clinical safety monitoring, pharmacovigilance, referral safety |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **VIEW** | Read | Platform governance view |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **VIEW** | Read | Platform governance view |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **VIEW** | Read | Platform governance view |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **AUDIT** | Read, Audit | Clinical safety monitoring, pharmacovigilance, referral safety |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **APPROVE** | Read, Approve, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **VIEW** | Read | Platform governance view |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **VIEW** | Read | Platform governance view |
| `MODULE-026` | Master System Administration & Feature Flagging | **VIEW** | Read | Platform governance view |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **APPROVE** | Read, Approve, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **VIEW** | Read | Platform governance view |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **APPROVE** | Read, Approve, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **VIEW** | Read | Platform governance view |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `YES` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `YES` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `YES` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `YES` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `YES` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `YES` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.3 ROLE-003: Lead Delivery Partner / Project Director

- **Role Identifier:** `ROLE-003` | **Official Title:** **Lead Delivery Partner / Project Director**
- **Functional Category:** `Management` | **Governance Tier:** `L4-Product`
- **Cadre Classification:** Program Director / Consortium Lead
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Delivery consortium director accountable for program milestones, multi-squad velocity, SLA adherence, and contract milestones.

**Primary Operational Focus:** Contractual delivery, cross-functional squad coordination, executive progress reporting, milestone signoffs.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-004` | Clinical & Administrative Staff Directory | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-007` | Patient Token Generation & Station Routing | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-026` | Master System Administration & Feature Flagging | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **AUDIT** | Read, Audit | Project progress tracking across all modules; strictly no raw patient clinical data |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `YES` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `YES` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.4 ROLE-004: Chief Solution Architect

- **Role Identifier:** `ROLE-004` | **Official Title:** **Chief Solution Architect**
- **Functional Category:** `Architecture` | **Governance Tier:** `L3-Architecture`
- **Cadre Classification:** Principal Enterprise Systems Architect
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Enterprise technical architect governing distributed topology, Fastify/PostgreSQL/DuckDB tech stack, edge mesh sync, and ABDM interfaces.

**Primary Operational Focus:** Technical architecture, integration schemas, offline conflict resolution policies, security architecture signoff.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** `MODULE-001`, `MODULE-002`, `MODULE-003`, `MODULE-004`, `MODULE-005`, `MODULE-006`, `MODULE-007`, `MODULE-008`, `MODULE-009`, `MODULE-010`, `MODULE-011`, `MODULE-012`, `MODULE-013`, `MODULE-014`, `MODULE-015`, `MODULE-016`, `MODULE-017`, `MODULE-018`, `MODULE-019`, `MODULE-020`, `MODULE-021`, `MODULE-022`, `MODULE-023`, `MODULE-024`, `MODULE-025`, `MODULE-026`, `MODULE-027`, `MODULE-028`, `MODULE-029`, `MODULE-030`
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-004` | Clinical & Administrative Staff Directory | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-007` | Patient Token Generation & Station Routing | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-026` | Master System Administration & Feature Flagging | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **ADMIN** | Read, Admin, Audit | Architectural configuration across all microservices; data tier zero-access to unmasked PHI |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `YES` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `YES` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `YES` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `YES` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.5 ROLE-005: Delivery Project Manager / Agile Coach

- **Role Identifier:** `ROLE-005` | **Official Title:** **Delivery Project Manager / Agile Coach**
- **Functional Category:** `Management` | **Governance Tier:** `L1-Operational`
- **Cadre Classification:** Scrum Master / Agile Delivery Manager
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Operational delivery manager coordinating 18-sprint backlog, release train sprints, daily blockers, and squad velocity.

**Primary Operational Focus:** Sprint execution, sprint backlog readiness, impediment removal, release scheduling.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-004` | Clinical & Administrative Staff Directory | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-007` | Patient Token Generation & Station Routing | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-026` | Master System Administration & Feature Flagging | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **VIEW** | Read | Sprint tracking and milestone verification across all modules |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **VIEW** | Read | Sprint tracking and milestone verification across all modules |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `YES` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.6 ROLE-006: Lead Backend Engineer

- **Role Identifier:** `ROLE-006` | **Official Title:** **Lead Backend Engineer**
- **Functional Category:** `Engineering` | **Governance Tier:** `L2-Technical`
- **Cadre Classification:** Senior Staff Backend Engineer (Node/TypeScript)
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Technical engineering lead responsible for Fastify microservices, GraphQL/REST APIs, Redis caches, and database query optimizations.

**Primary Operational Focus:** Backend services, API contracts, database transaction performance, microservice reliability.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** `MODULE-001`, `MODULE-003`, `MODULE-004`, `MODULE-024`, `MODULE-026`

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **EDIT** | Read, Update | Technical configuration in staging/dev; production access strictly via CI/CD |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **EDIT** | Read, Update | Technical configuration in staging/dev; production access strictly via CI/CD |
| `MODULE-004` | Clinical & Administrative Staff Directory | **EDIT** | Read, Update | Technical configuration in staging/dev; production access strictly via CI/CD |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-007` | Patient Token Generation & Station Routing | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **EDIT** | Read, Update | Technical configuration in staging/dev; production access strictly via CI/CD |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-026` | Master System Administration & Feature Flagging | **EDIT** | Read, Update | Technical configuration in staging/dev; production access strictly via CI/CD |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `YES` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.7 ROLE-007: Lead Frontend Engineer

- **Role Identifier:** `ROLE-007` | **Official Title:** **Lead Frontend Engineer**
- **Functional Category:** `Engineering` | **Governance Tier:** `L2-Technical`
- **Cadre Classification:** Senior Staff Web/Mobile Engineer (React/Next.js)
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Technical engineering lead responsible for Next.js PWA, local SQLite/IndexedDB caching, responsive UI components, and offline UX.

**Primary Operational Focus:** PWA client architecture, optimistic offline mutations, Kannada UI rendering, accessibility conformance.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** `MODULE-001`, `MODULE-003`, `MODULE-004`, `MODULE-024`, `MODULE-026`

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **EDIT** | Read, Update | Technical configuration in staging/dev; production access strictly via CI/CD |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **EDIT** | Read, Update | Technical configuration in staging/dev; production access strictly via CI/CD |
| `MODULE-004` | Clinical & Administrative Staff Directory | **EDIT** | Read, Update | Technical configuration in staging/dev; production access strictly via CI/CD |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-007` | Patient Token Generation & Station Routing | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **EDIT** | Read, Update | Technical configuration in staging/dev; production access strictly via CI/CD |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-026` | Master System Administration & Feature Flagging | **EDIT** | Read, Update | Technical configuration in staging/dev; production access strictly via CI/CD |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **VIEW** | Read | Service endpoint inspection; strictly synthetic or masked data |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `YES` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.8 ROLE-008: Lead Database Administrator (DBA)

- **Role Identifier:** `ROLE-008` | **Official Title:** **Lead Database Administrator (DBA)**
- **Functional Category:** `Data` | **Governance Tier:** `L2-Technical`
- **Cadre Classification:** Principal Database Administrator (PostgreSQL/DuckDB)
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Data tier custodian responsible for PostgreSQL schema migrations, WORM table immutability, backup replication, and DuckDB analytical rollups.

**Primary Operational Focus:** Database DDL/DML governance, index tuning, cryptographic WORM integrity, zero-loss replication.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** `MODULE-001`, `MODULE-002`, `MODULE-004`, `MODULE-021`, `MODULE-024`, `MODULE-026`
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **ADMIN** | Read, Update, Admin, Audit | Database DDL/DML migrations; WORM append-only enforcement; no direct raw clinical DML |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **ADMIN** | Read, Update, Admin, Audit | Database DDL/DML migrations; WORM append-only enforcement; no direct raw clinical DML |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-004` | Clinical & Administrative Staff Directory | **ADMIN** | Read, Update, Admin, Audit | Database DDL/DML migrations; WORM append-only enforcement; no direct raw clinical DML |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-007` | Patient Token Generation & Station Routing | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **ADMIN** | Read, Update, Admin, Audit | Database DDL/DML migrations; WORM append-only enforcement; no direct raw clinical DML |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **ADMIN** | Read, Update, Admin, Audit | Database DDL/DML migrations; WORM append-only enforcement; no direct raw clinical DML |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-026` | Master System Administration & Feature Flagging | **ADMIN** | Read, Update, Admin, Audit | Database DDL/DML migrations; WORM append-only enforcement; no direct raw clinical DML |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **VIEW** | Read | Database schema performance monitoring |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **VIEW** | Read | Database schema performance monitoring |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `YES` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `YES` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.9 ROLE-009: DevOps & SRE Lead

- **Role Identifier:** `ROLE-009` | **Official Title:** **DevOps & SRE Lead**
- **Functional Category:** `Infrastructure` | **Governance Tier:** `L2-Technical`
- **Cadre Classification:** Principal Site Reliability Engineer
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Infrastructure lead managing Kubernetes clusters, edge container runtimes, automated CI/CD pipelines, Prometheus monitoring, and disaster recovery.

**Primary Operational Focus:** Cluster availability, edge device monitoring, automated telemetry, zero-downtime rolling upgrades.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** `MODULE-001`, `MODULE-003`, `MODULE-004`, `MODULE-024`, `MODULE-026`, `MODULE-027`
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **ADMIN** | Read, Update, Admin, Audit | Infrastructure orchestration, edge node deployment, telemetry ingestion |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **ADMIN** | Read, Update, Admin, Audit | Infrastructure orchestration, edge node deployment, telemetry ingestion |
| `MODULE-004` | Clinical & Administrative Staff Directory | **ADMIN** | Read, Update, Admin, Audit | Infrastructure orchestration, edge node deployment, telemetry ingestion |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-007` | Patient Token Generation & Station Routing | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **ADMIN** | Read, Update, Admin, Audit | Infrastructure orchestration, edge node deployment, telemetry ingestion |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-026` | Master System Administration & Feature Flagging | **ADMIN** | Read, Update, Admin, Audit | Infrastructure orchestration, edge node deployment, telemetry ingestion |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **ADMIN** | Read, Update, Admin, Audit | Infrastructure orchestration, edge node deployment, telemetry ingestion |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **VIEW** | Read | System health and cluster metric observation |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **VIEW** | Read | System health and cluster metric observation |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `YES` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `YES` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `YES` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.10 ROLE-010: Quality Assurance Lead

- **Role Identifier:** `ROLE-010` | **Official Title:** **Quality Assurance Lead**
- **Functional Category:** `Quality` | **Governance Tier:** `L2-Technical`
- **Cadre Classification:** Senior Test Automation Architect
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Quality engineering lead governing end-to-end test automation, Playwright E2E suites, offline simulation testing, and release quality gates.

**Primary Operational Focus:** Automated regression suites, release gate verification, performance profiling, defect triage.

#### Module Entitlements Summary
- **Total Accessible Modules:** 0 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `NO` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.11 ROLE-011: Security & Data Privacy Officer

- **Role Identifier:** `ROLE-011` | **Official Title:** **Security & Data Privacy Officer**
- **Functional Category:** `Security` | **Governance Tier:** `L3-Architecture`
- **Cadre Classification:** Chief Information Security Officer (CISO) / DPO
- **Clinical Prescribing Authority:** Security Audit (No prescribing)
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Statutory privacy and security officer governing DPDP Act 2023 compliance, cryptographic key lifecycles, ABAC policies, and threat audits.

**Primary Operational Focus:** DPDP compliance, vulnerability management, audit log forensic verification, patient privacy audits.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** `MODULE-001`, `MODULE-004`, `MODULE-007`, `MODULE-021`, `MODULE-026`
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **ADMIN** | Read, Update, Admin, Audit | Cryptographic key rotation, ABAC privilege policy enforcement, DPDP audit |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-004` | Clinical & Administrative Staff Directory | **ADMIN** | Read, Update, Admin, Audit | Cryptographic key rotation, ABAC privilege policy enforcement, DPDP audit |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-007` | Patient Token Generation & Station Routing | **ADMIN** | Read, Update, Admin, Audit | Cryptographic key rotation, ABAC privilege policy enforcement, DPDP audit |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **ADMIN** | Read, Update, Admin, Audit | Cryptographic key rotation, ABAC privilege policy enforcement, DPDP audit |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-026` | Master System Administration & Feature Flagging | **ADMIN** | Read, Update, Admin, Audit | Cryptographic key rotation, ABAC privilege policy enforcement, DPDP audit |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **AUDIT** | Read, Audit | Audit access to security logs, access traces, and consent transactions |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `YES` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `YES` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `YES` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.12 ROLE-012: Clinical Safety Specialist (SME)

- **Role Identifier:** `ROLE-012` | **Official Title:** **Clinical Safety Specialist (SME)**
- **Functional Category:** `Clinical` | **Governance Tier:** `L3-Architecture`
- **Cadre Classification:** Public Health Medical Specialist
- **Clinical Prescribing Authority:** Protocol Design & Clinical Rule Verification
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Clinical domain expert verifying clinical workflows, drug formulary interactions, ICD-10/SNOMED CT ontologies, and diagnostic guidelines.

**Primary Operational Focus:** Clinical rule definitions, drug-drug interaction alert thresholds, clinical safety case validation.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **VIEW** | Read | Platform governance view |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **VIEW** | Read | Platform governance view |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **VIEW** | Read | Platform governance view |
| `MODULE-004` | Clinical & Administrative Staff Directory | **VIEW** | Read | Platform governance view |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | Platform governance view |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **VIEW** | Read | Platform governance view |
| `MODULE-007` | Patient Token Generation & Station Routing | **VIEW** | Read | Platform governance view |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | Platform governance view |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **AUDIT** | Read, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **AUDIT** | Read, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **AUDIT** | Read, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **AUDIT** | Read, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **AUDIT** | Read, Audit | Clinical safety monitoring, pharmacovigilance, referral safety |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read | Platform governance view |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **VIEW** | Read | Platform governance view |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **AUDIT** | Read, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **AUDIT** | Read, Audit | Clinical safety monitoring, pharmacovigilance, referral safety |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **AUDIT** | Read, Audit | Clinical safety monitoring, pharmacovigilance, referral safety |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **VIEW** | Read | Platform governance view |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **VIEW** | Read | Platform governance view |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **VIEW** | Read | Platform governance view |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **AUDIT** | Read, Audit | Clinical safety monitoring, pharmacovigilance, referral safety |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **AUDIT** | Read, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **VIEW** | Read | Platform governance view |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **VIEW** | Read | Platform governance view |
| `MODULE-026` | Master System Administration & Feature Flagging | **VIEW** | Read | Platform governance view |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **AUDIT** | Read, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **VIEW** | Read | Platform governance view |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **AUDIT** | Read, Audit | Clinical protocol governance, safety rule ratification, CDSS AI guardrails |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **VIEW** | Read | Platform governance view |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `YES` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `YES` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `YES` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.13 ROLE-013: Public Health Epidemiologist

- **Role Identifier:** `ROLE-013` | **Official Title:** **Public Health Epidemiologist**
- **Functional Category:** `Analytics` | **Governance Tier:** `L3-Architecture`
- **Cadre Classification:** Senior Epidemiologist / Health Data Scientist
- **Clinical Prescribing Authority:** Population Health Analytics
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Public health specialist analyzing syndromic disease trends, municipal outbreak clustering, vaccine coverage, and epidemiological surveillance.

**Primary Operational Focus:** Disease cluster detection, public health indicator surveillance, predictive syndromic models, HMIS analytics.

#### Module Entitlements Summary
- **Total Accessible Modules:** 6 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **VIEW** | Read | Anonymized aggregate health trends; no identifying citizen information |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **VIEW** | Read | Anonymized aggregate health trends; no identifying citizen information |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **VIEW** | Read | Anonymized aggregate health trends; no identifying citizen information |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **VIEW** | Read | Anonymized aggregate health trends; no identifying citizen information |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **AUDIT** | Read, Audit | Execute municipal epidemiological queries and syndromic cluster analysis |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **AUDIT** | Read, Audit | Execute municipal epidemiological queries and syndromic cluster analysis |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `YES` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `YES` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `YES` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.14 ROLE-014: Frontline Training Coordinator

- **Role Identifier:** `ROLE-014` | **Official Title:** **Frontline Training Coordinator**
- **Functional Category:** `Operations` | **Governance Tier:** `L1-Operational`
- **Cadre Classification:** Clinical Operations Trainer
- **Clinical Prescribing Authority:** Training Sandbox Operations
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Operational coordinator managing frontline clinic staff onboarding, interactive simulator training, workflow certifications, and user adoption.

**Primary Operational Focus:** Staff simulation environments, competency assessments, training material curation, end-user feedback.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-004` | Clinical & Administrative Staff Directory | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-007` | Patient Token Generation & Station Routing | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-026` | Master System Administration & Feature Flagging | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **VIEW** | Read | Sandbox and training simulation tenant view across workflows |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.15 ROLE-015: Zonal Clinic Medical Superintendent

- **Role Identifier:** `ROLE-015` | **Official Title:** **Zonal Clinic Medical Superintendent**
- **Functional Category:** `Clinical` | **Governance Tier:** `L1-Operational`
- **Cadre Classification:** Senior Medical Officer (MBBS/MD) / Superintendent
- **Clinical Prescribing Authority:** Full Clinical Prescribing, Diagnosing & Emergency Break-Glass
- **Offline Station Capable:** `True` | **Break-Glass Capable:** `True`

#### Role Purpose & Strategic Mandate
Senior doctor and clinic in-charge conducting patient consultations, clinical examinations, e-prescribing, lab ordering, and medical supervision.

**Primary Operational Focus:** Outpatient clinical diagnosis, e-prescription generation, emergency resuscitation, secondary hospital referral signoff.

#### Module Entitlements Summary
- **Total Accessible Modules:** 17 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** `MODULE-009`, `MODULE-010`, `MODULE-011`, `MODULE-012`, `MODULE-017`, `MODULE-018`, `MODULE-024`, `MODULE-027`, `MODULE-029`

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | View patient demographics, queue position, formulary, CDSS suggestions |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **VIEW** | Read | View patient demographics, queue position, formulary, CDSS suggestions |
| `MODULE-007` | Patient Token Generation & Station Routing | **VIEW** | Read | View patient demographics, queue position, formulary, CDSS suggestions |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | View patient demographics, queue position, formulary, CDSS suggestions |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **EDIT** | Read, Create, Update | Review triage vitals, order point-of-care laboratory tests |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **CREATE** | Read, Create, Update, Prescribe | Active assigned clinic doctor; full consultation & e-prescribing; break-glass override |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **EDIT** | Read, Create, Update | Review triage vitals, order point-of-care laboratory tests |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **CREATE** | Read, Create, Update, Prescribe | Active assigned clinic doctor; full consultation & e-prescribing; break-glass override |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **VIEW** | Read | View pharmacy dispensing status and clinic stock availability |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read | View pharmacy dispensing status and clinic stock availability |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **VIEW** | Read | View patient demographics, queue position, formulary, CDSS suggestions |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **CREATE** | Read, Create, Update | Authorize secondary hospital referrals, manage chronic NCD care, adverse alerts |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **CREATE** | Read, Create, Update | Authorize secondary hospital referrals, manage chronic NCD care, adverse alerts |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **VIEW** | Read | View patient demographics, queue position, formulary, CDSS suggestions |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **EXECUTE** | Read | Trigger manual emergency sync from doctor tablet to local edge |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **CREATE** | Read, Create, Update | Authorize secondary hospital referrals, manage chronic NCD care, adverse alerts |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **CREATE** | Read, Create, Update, Prescribe | Active assigned clinic doctor; full consultation & e-prescribing; break-glass override |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `YES` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `YES` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `YES` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `YES` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `YES` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.16 ROLE-016: Staff Nurse Supervisor

- **Role Identifier:** `ROLE-016` | **Official Title:** **Staff Nurse Supervisor**
- **Functional Category:** `Clinical` | **Governance Tier:** `L1-Operational`
- **Cadre Classification:** Registered Staff Nurse (B.Sc / GNM)
- **Clinical Prescribing Authority:** Clinical Triage, Vitals Recording, Nursing Administration
- **Offline Station Capable:** `True` | **Break-Glass Capable:** `True`

#### Role Purpose & Strategic Mandate
Senior staff nurse leading vital signs triage, pediatric growth monitoring, danger sign identification, immunization, and emergency bedside care.

**Primary Operational Focus:** Vital signs measurement, triage acuity scoring, red-flag emergency alert triggers, cold chain logging.

#### Module Entitlements Summary
- **Total Accessible Modules:** 11 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** `MODULE-005`, `MODULE-007`, `MODULE-008`, `MODULE-009`, `MODULE-024`

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **CREATE** | Read, Create, Update | Assisted registration, nurse queue triage calling, consent capture |
| `MODULE-007` | Patient Token Generation & Station Routing | **CREATE** | Read, Create, Update | Assisted registration, nurse queue triage calling, consent capture |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **CREATE** | Read, Create, Update | Assisted registration, nurse queue triage calling, consent capture |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **CREATE** | Read, Create, Update | Record patient vital signs, assign triage category, broadcast red danger alert |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **VIEW** | Read | View clinical encounters, collect lab samples, monitor chronic follow-up |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **VIEW** | Read | View clinical encounters, collect lab samples, monitor chronic follow-up |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read | View vaccine and consumable stock levels |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **VIEW** | Read | View vaccine and consumable stock levels |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **VIEW** | Read | View clinical encounters, collect lab samples, monitor chronic follow-up |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **EXECUTE** | Read | Nurse station edge cache synchronization |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **VIEW** | Read | View clinical encounters, collect lab samples, monitor chronic follow-up |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `YES` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `YES` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `YES` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `YES` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.17 ROLE-017: Chief Pharmacy Supervisor

- **Role Identifier:** `ROLE-017` | **Official Title:** **Chief Pharmacy Supervisor**
- **Functional Category:** `Pharmacy` | **Governance Tier:** `L1-Operational`
- **Cadre Classification:** Registered Pharmacist (B.Pharm / D.Pharm)
- **Clinical Prescribing Authority:** Medication Dispensing & Pharmacy Counseling (Strictly Cannot Prescribe)
- **Offline Station Capable:** `True` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Licensed pharmacist responsible for prescription verification, barcode-scanned medicine dispensing, patient counseling, and stock FEFO control.

**Primary Operational Focus:** Medication dispensing, 2D barcode batch verification, stock indenting, cold-chain medicine handling, expiry management.

#### Module Entitlements Summary
- **Total Accessible Modules:** 8 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** `MODULE-013`, `MODULE-014`, `MODULE-015`, `MODULE-024`

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | View patient demographics and pharmacy queue position |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | View patient demographics and pharmacy queue position |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **VIEW** | Read | Read electronic prescription items; strictly NO prescribing or altering Rx |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **EXECUTE** | Read, Update, Dispense | Scan 2D barcode, verify e-prescription, dispense medication, log patient counseling |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **CREATE** | Read, Create, Update, Approve | Manage batch FEFO stock, log physical counts, submit stock replenishment indents |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **CREATE** | Read, Create, Update, Approve | Manage batch FEFO stock, log physical counts, submit stock replenishment indents |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **VIEW** | Read | View essential medicine list and formulary rules |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **EXECUTE** | Read | Dispensary terminal offline sync |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `YES` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `YES` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `YES` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `YES` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `YES` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.18 ROLE-018: Senior Laboratory Supervisor

- **Role Identifier:** `ROLE-018` | **Official Title:** **Senior Laboratory Supervisor**
- **Functional Category:** `Laboratory` | **Governance Tier:** `L1-Operational`
- **Cadre Classification:** Medical Laboratory Technologist (B.Sc MLT)
- **Clinical Prescribing Authority:** Diagnostic Test Execution & Result Entry (Cannot Prescribe)
- **Offline Station Capable:** `True` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Certified laboratory technician performing rapid point-of-care diagnostic tests, sample processing, result entry, and panic-value escalation.

**Primary Operational Focus:** Specimen accessioning, diagnostic test processing, critical panic value alerting, laboratory equipment calibration.

#### Module Entitlements Summary
- **Total Accessible Modules:** 6 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** `MODULE-011`, `MODULE-024`

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | View patient demographics and lab queue |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | View patient demographics and lab queue |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **VIEW** | Read | View diagnostic order context from doctor note |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **CREATE** | Read, Create, Update | Accession lab specimen, enter test results, escalate panic values, reject samples |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read, Update | Track rapid test kit reagents and consumables |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **EXECUTE** | Read | Lab station offline edge sync |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `YES` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `YES` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `YES` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.19 ROLE-019: Front Desk Operations Supervisor

- **Role Identifier:** `ROLE-019` | **Official Title:** **Front Desk Operations Supervisor**
- **Functional Category:** `Operations` | **Governance Tier:** `L1-Operational`
- **Cadre Classification:** Clinic Front Desk Coordinator / Receptionist
- **Clinical Prescribing Authority:** Non-Clinical Intake (No access to detailed clinical diagnoses)
- **Offline Station Capable:** `True` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Frontline receptionist handling citizen intake, demographic data entry, ABHA verification, digital consent, and priority token minting.

**Primary Operational Focus:** Citizen registration, biometric/OTP ABHA onboarding, digital consent recording, token printing, waiting hall queue call.

#### Module Entitlements Summary
- **Total Accessible Modules:** 6 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** `MODULE-005`, `MODULE-006`, `MODULE-007`, `MODULE-008`, `MODULE-020`, `MODULE-024`

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **CREATE** | Read, Create, Update | Register citizen, link ABHA, record digital consent, mint queue token, print slip |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **CREATE** | Read, Create, Update | Register citizen, link ABHA, record digital consent, mint queue token, print slip |
| `MODULE-007` | Patient Token Generation & Station Routing | **CREATE** | Read, Create, Update | Register citizen, link ABHA, record digital consent, mint queue token, print slip |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **CREATE** | Read, Create, Update | Register citizen, link ABHA, record digital consent, mint queue token, print slip |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **CREATE** | Read, Create | Log walk-in citizen feedback or grievance |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **EXECUTE** | Read | Intake desk offline registration cache sync |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `YES` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `YES` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.20 ROLE-020: Integration Gateway Specialist

- **Role Identifier:** `ROLE-020` | **Official Title:** **Integration Gateway Specialist**
- **Functional Category:** `Engineering` | **Governance Tier:** `L2-Technical`
- **Cadre Classification:** Integration Solutions Engineer
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Technical specialist managing external gateways including ABDM M1/M2/M3 bridges, state HMIS API pipelines, and 108 emergency dispatch interfaces.

**Primary Operational Focus:** FHIR R4 bundle mapping, ABDM cryptographic token exchange, SMS/WhatsApp delivery webhooks, 108 CAD integration.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** `MODULE-006`, `MODULE-017`, `MODULE-019`, `MODULE-020`, `MODULE-025`, `MODULE-030`
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **VIEW** | Read | Integration health monitoring |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **VIEW** | Read | Integration health monitoring |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **VIEW** | Read | Integration health monitoring |
| `MODULE-004` | Clinical & Administrative Staff Directory | **VIEW** | Read | Integration health monitoring |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | Integration health monitoring |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **ADMIN** | Read, Update | Manage ABDM, 108 CAD, SMS gateway, and inter-facility integration webhooks |
| `MODULE-007` | Patient Token Generation & Station Routing | **VIEW** | Read | Integration health monitoring |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | Integration health monitoring |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **VIEW** | Read | Integration health monitoring |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **VIEW** | Read | Integration health monitoring |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **VIEW** | Read | Integration health monitoring |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **VIEW** | Read | Integration health monitoring |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **VIEW** | Read | Integration health monitoring |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read | Integration health monitoring |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **VIEW** | Read | Integration health monitoring |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **VIEW** | Read | Integration health monitoring |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **ADMIN** | Read, Update | Manage ABDM, 108 CAD, SMS gateway, and inter-facility integration webhooks |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **VIEW** | Read | Integration health monitoring |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **ADMIN** | Read, Update | Manage ABDM, 108 CAD, SMS gateway, and inter-facility integration webhooks |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **ADMIN** | Read, Update | Manage ABDM, 108 CAD, SMS gateway, and inter-facility integration webhooks |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **VIEW** | Read | Integration health monitoring |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **VIEW** | Read | Integration health monitoring |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **VIEW** | Read | Integration health monitoring |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **VIEW** | Read | Integration health monitoring |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **ADMIN** | Read, Update | Manage ABDM, 108 CAD, SMS gateway, and inter-facility integration webhooks |
| `MODULE-026` | Master System Administration & Feature Flagging | **VIEW** | Read | Integration health monitoring |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **VIEW** | Read | Integration health monitoring |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **VIEW** | Read | Integration health monitoring |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **VIEW** | Read | Integration health monitoring |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **ADMIN** | Read, Update | Manage ABDM, 108 CAD, SMS gateway, and inter-facility integration webhooks |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `YES` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.21 ROLE-021: Data Analytics Engineer

- **Role Identifier:** `ROLE-021` | **Official Title:** **Data Analytics Engineer**
- **Functional Category:** `Data` | **Governance Tier:** `L2-Technical`
- **Cadre Classification:** Senior Analytics & Business Intelligence Engineer
- **Clinical Prescribing Authority:** None (Anonymized data only)
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Data engineer building DuckDB analytical cubes, municipal health indicators, facility census dashboards, and automated state reports.

**Primary Operational Focus:** Analytical pipelines, DuckDB columnar modeling, municipal KPI aggregation, operational reports.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** `MODULE-021`, `MODULE-022`, `MODULE-025`
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-004` | Clinical & Administrative Staff Directory | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-007` | Patient Token Generation & Station Routing | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **ADMIN** | Read, Update | Build DuckDB analytics views, maintain aggregate data marts, generate reports |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **ADMIN** | Read, Update | Build DuckDB analytics views, maintain aggregate data marts, generate reports |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **ADMIN** | Read, Update | Build DuckDB analytics views, maintain aggregate data marts, generate reports |
| `MODULE-026` | Master System Administration & Feature Flagging | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **VIEW** | Read | Aggregate reporting across all operational domains |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **VIEW** | Read | Aggregate reporting across all operational domains |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `YES` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `YES` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `YES` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.22 ROLE-022: UI/UX Accessibility Designer

- **Role Identifier:** `ROLE-022` | **Official Title:** **UI/UX Accessibility Designer**
- **Functional Category:** `Design` | **Governance Tier:** `L2-Technical`
- **Cadre Classification:** Lead Product Designer & Accessibility Specialist
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
User experience designer ensuring WCAG 2.1 AA compliance, Kannada localized typography, touch-first tablet interactions, and high-contrast styling.

**Primary Operational Focus:** Design system tokens, screen reader compatibility, Kannada translation layout fidelity, user workflow ergonomics.

#### Module Entitlements Summary
- **Total Accessible Modules:** 6 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **VIEW** | Read | Accessibility and UI component testing |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **VIEW** | Read | Accessibility and UI component testing |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | Accessibility and UI component testing |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | Accessibility and UI component testing |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **VIEW** | Read | Accessibility and UI component testing |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **VIEW** | Read | Accessibility and UI component testing |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.23 ROLE-023: Tier-1/2 Helpdesk Coordinator

- **Role Identifier:** `ROLE-023` | **Official Title:** **Tier-1/2 Helpdesk Coordinator**
- **Functional Category:** `Support` | **Governance Tier:** `L1-Operational`
- **Cadre Classification:** IT Service Management Support Lead
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Centralized IT helpdesk agent managing clinic incident tickets, password resets, hardware trouble tickets, and citizen grievance escalation.

**Primary Operational Focus:** Incident lifecycle management, clinic operational support, peripheral hardware ticketing, user assistance.

#### Module Entitlements Summary
- **Total Accessible Modules:** 5 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** `MODULE-020`, `MODULE-028`

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **VIEW** | Read | Check staff account status and clinic facility status to support users |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **VIEW** | Read | Check staff account status and clinic facility status to support users |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | Check staff account status and clinic facility status to support users |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **CREATE** | Read, Create, Update | Create, route, and update facility helpdesk incident tickets and grievances |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **CREATE** | Read, Create, Update | Create, route, and update facility helpdesk incident tickets and grievances |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `YES` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.24 ROLE-024: Field Hardware Support Engineer

- **Role Identifier:** `ROLE-024` | **Official Title:** **Field Hardware Support Engineer**
- **Functional Category:** `Support` | **Governance Tier:** `L1-Operational`
- **Cadre Classification:** Desktop & Peripheral Field Support Technician
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `True` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
On-site field hardware technician troubleshooting clinic mini-servers, thermal printers, barcode scanners, digital displays, and local LANs.

**Primary Operational Focus:** Peripheral repair, local edge node re-imaging, biometric scanner calibration, UPS power verification.

#### Module Entitlements Summary
- **Total Accessible Modules:** 2 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** `MODULE-024`, `MODULE-028`

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **EXECUTE** | Read, Update | Diagnose edge mini-server, calibrate thermal printers & barcode scanners |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **EXECUTE** | Read, Update | Diagnose edge mini-server, calibrate thermal printers & barcode scanners |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `YES` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.25 ROLE-025: Municipal Legal & Compliance Counsel

- **Role Identifier:** `ROLE-025` | **Official Title:** **Municipal Legal & Compliance Counsel**
- **Functional Category:** `Compliance` | **Governance Tier:** `L4-Product`
- **Cadre Classification:** Legal Advisor / Municipal Data Protection Counsel
- **Clinical Prescribing Authority:** Legal Compliance Review (No clinical access)
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Municipal legal counsel governing DPDP Act statutory compliance, patient privacy notices, data disclosure requests, and regulatory contracts.

**Primary Operational Focus:** DPDP legal interpretation, data processing agreements, compliance audits, statutory regulatory filings.

#### Module Entitlements Summary
- **Total Accessible Modules:** 7 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **VIEW** | Read | Tenant governance and security posture audit |
| `MODULE-004` | Clinical & Administrative Staff Directory | **VIEW** | Read | Tenant governance and security posture audit |
| `MODULE-007` | Patient Token Generation & Station Routing | **AUDIT** | Read, Audit | Statutory compliance and consent ledger audit; DPDP legal audit authority |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **AUDIT** | Read, Audit | Statutory compliance and consent ledger audit; DPDP legal audit authority |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **AUDIT** | Read, Audit | Statutory compliance and consent ledger audit; DPDP legal audit authority |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **AUDIT** | Read, Audit | Statutory compliance and consent ledger audit; DPDP legal audit authority |
| `MODULE-026` | Master System Administration & Feature Flagging | **VIEW** | Read | Tenant governance and security posture audit |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `YES` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `YES` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.26 ROLE-026: Municipal Finance Auditor

- **Role Identifier:** `ROLE-026` | **Official Title:** **Municipal Finance Auditor**
- **Functional Category:** `Finance` | **Governance Tier:** `L4-Product`
- **Cadre Classification:** Senior Municipal Auditor / Fiscal Controller
- **Clinical Prescribing Authority:** Fiscal Inventory Audit (No patient PHI access)
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Municipal finance auditor overseeing pharmaceutical stock reconciliation, physical inventory audit trails, procurement indents, and capital assets.

**Primary Operational Focus:** Stock valuation audits, drug write-off verifications, procurement ledger checks, financial transparency.

#### Module Entitlements Summary
- **Total Accessible Modules:** 6 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **AUDIT** | Read, Audit | Pharmacy inventory valuation and procurement ledger audit; no patient PHI access |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **AUDIT** | Read, Audit | Pharmacy inventory valuation and procurement ledger audit; no patient PHI access |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **AUDIT** | Read, Audit | Pharmacy inventory valuation and procurement ledger audit; no patient PHI access |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **AUDIT** | Read, Audit | Pharmacy inventory valuation and procurement ledger audit; no patient PHI access |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **VIEW** | Read | Financial transaction audit logs |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **VIEW** | Read | Financial transaction audit logs |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `YES` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `YES` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `YES` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.27 ROLE-027: Release Train Engineer

- **Role Identifier:** `ROLE-027` | **Official Title:** **Release Train Engineer**
- **Functional Category:** `Management` | **Governance Tier:** `L2-Technical`
- **Cadre Classification:** Enterprise Release Manager
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Release engineering manager orchestrating phased multi-clinic rollouts, feature flag deployments, canary testing, and release rollbacks.

**Primary Operational Focus:** Feature flag toggles, progressive delivery, release readiness reviews, operational deployment windows.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** `MODULE-003`, `MODULE-026`
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **ADMIN** | Read, Update | Feature flag management and progressive canary release toggles |
| `MODULE-004` | Clinical & Administrative Staff Directory | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-007` | Patient Token Generation & Station Routing | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-026` | Master System Administration & Feature Flagging | **ADMIN** | Read, Update | Feature flag management and progressive canary release toggles |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **VIEW** | Read | Release verification across all functional domains |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **VIEW** | Read | Release verification across all functional domains |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `YES` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `YES` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.28 ROLE-028: Performance & Chaos Engineer

- **Role Identifier:** `ROLE-028` | **Official Title:** **Performance & Chaos Engineer**
- **Functional Category:** `Quality` | **Governance Tier:** `L2-Technical`
- **Cadre Classification:** Site Reliability Performance Engineer
- **Clinical Prescribing Authority:** None
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Specialized resilience engineer executing simulated network partitions, high-concurrency clinic load injection, and edge sync stress testing.

**Primary Operational Focus:** Chaos testing, network drop resilience, edge mesh sync recovery, high-load queue benchmarking.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** `MODULE-001`, `MODULE-002`, `MODULE-003`, `MODULE-004`, `MODULE-005`, `MODULE-006`, `MODULE-007`, `MODULE-008`, `MODULE-009`, `MODULE-010`, `MODULE-011`, `MODULE-012`, `MODULE-013`, `MODULE-014`, `MODULE-015`, `MODULE-016`, `MODULE-017`, `MODULE-018`, `MODULE-019`, `MODULE-020`, `MODULE-021`, `MODULE-022`, `MODULE-023`, `MODULE-024`, `MODULE-025`, `MODULE-026`, `MODULE-027`, `MODULE-028`, `MODULE-029`, `MODULE-030`

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-004` | Clinical & Administrative Staff Directory | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-007` | Patient Token Generation & Station Routing | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-026` | Master System Administration & Feature Flagging | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **EXECUTE** | Read | Synthetic load injection and resilience testing in non-prod / chaos windows |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.29 ROLE-029: Kannada Localization Specialist

- **Role Identifier:** `ROLE-029` | **Official Title:** **Kannada Localization Specialist**
- **Functional Category:** `Content` | **Governance Tier:** `L1-Operational`
- **Cadre Classification:** Linguistic & Health Translation Specialist
- **Clinical Prescribing Authority:** Localization Content Certification
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Bilingual language specialist certifying Kannada medical terminology, citizen SMS templates, audio queue announcements, and UI strings.

**Primary Operational Focus:** Kannada string verification, medical terminology standardization, localized citizen communication, audio cue quality.

#### Module Entitlements Summary
- **Total Accessible Modules:** 4 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** `MODULE-003`, `MODULE-008`, `MODULE-016`, `MODULE-019`

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **EDIT** | Read, Update, Approve | Translate and certify Kannada strings, citizen SMS notices, and audio cues |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **EDIT** | Read, Update, Approve | Translate and certify Kannada strings, citizen SMS notices, and audio cues |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **EDIT** | Read, Update, Approve | Translate and certify Kannada strings, citizen SMS notices, and audio cues |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **EDIT** | Read, Update, Approve | Translate and certify Kannada strings, citizen SMS notices, and audio cues |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `YES` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `YES` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `NO` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

### 4.30 ROLE-030: Documentation & Traceability Auditor

- **Role Identifier:** `ROLE-030` | **Official Title:** **Documentation & Traceability Auditor**
- **Functional Category:** `Governance` | **Governance Tier:** `L2-Technical`
- **Cadre Classification:** Systems Compliance & Quality Auditor
- **Clinical Prescribing Authority:** Governance Audit
- **Offline Station Capable:** `False` | **Break-Glass Capable:** `False`

#### Role Purpose & Strategic Mandate
Governance auditor verifying cross-phase requirement traceability, architectural consistency, audit trail integrity, and documentation baselines.

**Primary Operational Focus:** Traceability matrix validation, specification consistency, statutory audit trail completeness, documentation verification.

#### Module Entitlements Summary
- **Total Accessible Modules:** 30 of 30 modules
- **Administrative / Approval Modules:** None
- **Operational / Data Mutation Modules:** None

#### Detailed Module-Level Entitlement Profile
| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |
| :--- | :--- | :---: | :--- | :--- |
| `MODULE-001` | Staff Authentication & MFA Engine | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-002` | Role-Based Access Control (RBAC) & Entitlements | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-003` | Healthcare Facility & Organizational Hierarchy | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-004` | Clinical & Administrative Staff Directory | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-005` | Patient Registration, Demographics & ABHA Minting | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-006` | Informed Clinical Consent & DPDP Data Privacy | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-007` | Patient Token Generation & Station Routing | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-008` | Dynamic Queue Orchestration & Display Boards | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-009` | Doctor EMR Console & Clinical SOAP Encounter | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-010` | ICD-10 & SNOMED CT Clinical Diagnosis Coding | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-011` | Electronic Prescription (e-Rx) & Drug Safety Engine | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-012` | Point-of-Care Laboratory Testing & Diagnostic Orders | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-013` | Pharmacy Dispensing & 2D Barcode Verification | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-014` | Real-Time Batch Inventory & FEFO Stock Ledger | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-015` | Drug Indent Generation, Receiving & Cold-Chain Intake | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-016` | Essential Medicine List (EML) & Formulary Master | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-017` | Secondary Referral & 108 Emergency EMS Transit | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-018` | NCD Longitudinal Follow-Up & Recall Management | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-019` | Citizen Multichannel Notifications & Health Reminders | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-020` | Citizen Feedback, Grievance & Ombudsman Redressal | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-021` | Cryptographic Audit Ledger & Compliance (WORM) | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-022` | Zonal & Ward Operational KPI Dashboards | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-023` | Safe AI/ML Clinical Decision Support Safeguards | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-024` | National Health ABDM Ecosystem Interoperability | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-025` | Autonomous Offline Edge Engine & Conflict Replay | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-026` | Master System Administration & Feature Flagging | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-027` | State Health HMIS & Statutory Disease Reporting | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-028` | Facility Operations Helpdesk & Incident Dispatch | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-029` | Telemedicine & Specialist Tele-Consultation Bridge | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |
| `MODULE-030` | Municipal Pilot Command Center & Disaster Operations | **AUDIT** | Read, Audit | Documentation compliance and requirement traceability verification |

#### Detailed Permission Vector across 16 Security Dimensions
| Security Dimension | Authorized? | Governing Rule & Technical Constraint |
| :--- | :---: | :--- |
| **Read Access** | `YES` | Bound by ABAC clinic facility tenancy and data masking rules. |
| **Create Mutation** | `NO` | Permitted strictly within assigned domain operational entities. |
| **Update Mutation** | `NO` | Optimistic concurrency locking; historical audit version preserved. |
| **Delete Mutation** | `NO` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |
| **Approve Authority** | `NO` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |
| **Reject Authority** | `NO` | Operational rejection with mandatory structured rejection reason code. |
| **Dispense Medication** | `NO` | Pharmacist credential verification; 2D barcode pack scan required. |
| **Prescribe Medication** | `NO` | State Medical Council (KMC) verified license required on file. |
| **View Clinical Data (PHI)** | `NO` | DPDP Act 2023 compliance; patient consent grant required. |
| **View Analytical Reports** | `NO` | Anonymized aggregate metrics and ward-level health indicators. |
| **Export Data** | `NO` | CSV/PDF export watermarked with User UUID and IP address. |
| **Administer Settings** | `NO` | Configuration management in authorized functional sub-systems. |
| **Configure Flags** | `NO` | Feature flag toggling for canary releases in non-production environments. |
| **Audit Access** | `YES` | Read-only access to cryptographic WORM audit ledger and security logs. |
| **Emergency Break-Glass** | `NO` | Real-time override for unconscious trauma cases; triggers 24h audit review. |
| **Offline Operation** | `NO` | Station executes against local SQLite edge cache during network cuts. |

#### Day-in-the-Life Operational Workflow & Constraints
- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.
- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).
- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.
- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.

---

## 5. Master Role-Capability Entitlement Matrix (180 Capabilities)
Evaluation of specific business capability entitlements across primary frontline operational cadres: Doctor (`ROLE-015`), Staff Nurse (`ROLE-016`), Pharmacist (`ROLE-017`), Lab Tech (`ROLE-018`), Front Desk Clerk (`ROLE-019`), and System Admin (`ROLE-001`):

| Capability ID | Capability Name | Module ID | Doctor (015) | Nurse (016) | Pharm (017) | Lab (018) | Clerk (019) | Admin (001) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `CAPABILITY-001` | Credential Verification | `MODULE-001` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-002` | Session Token Minting | `MODULE-001` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-003` | MFA Challenge Dispatch | `MODULE-001` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-004` | Biometric Authentication Bridge | `MODULE-001` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-005` | Local PIN Verification | `MODULE-001` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-006` | Session Inactivity Lockout | `MODULE-001` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-007` | Permission Evaluation | `MODULE-002` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-008` | Dynamic Role Assignment | `MODULE-002` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-009` | Conflict-of-Interest Prevention | `MODULE-002` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-010` | Maker-Checker Authorization | `MODULE-002` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-011` | Break-Glass Privilege Elevation | `MODULE-002` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-012` | Privilege Elevation Audit | `MODULE-002` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-013` | Hierarchy Node Management | `MODULE-003` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-014` | NIN / HFR Registry Linking | `MODULE-003` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-015` | Station Terminal Mapping | `MODULE-003` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-016` | Facility Capacity Configuration | `MODULE-003` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-017` | Operating Hours Enforcement | `MODULE-003` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-018` | Special Camp Calendar | `MODULE-003` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-019` | Staff Onboarding & KYC | `MODULE-004` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-020` | Professional License Verification | `MODULE-004` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-021` | Duty Roster Generation | `MODULE-004` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-022` | Biometric Attendance Linking | `MODULE-004` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-023` | Digital Signature Enrollment | `MODULE-004` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-024` | Signature Revocation | `MODULE-004` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-025` | Targeted Flag Activation | `MODULE-026` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-026` | Emergency Feature Killswitch | `MODULE-026` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-027` | System Parameter Tuning | `MODULE-026` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-028` | Edge Configuration Distribution | `MODULE-026` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-029` | Edge Migration Orchestration | `MODULE-026` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-030` | Health Probe Monitoring | `MODULE-026` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-031` | Bilingual Intake UI | `MODULE-005` | `VIEW` | `CREATE` | `VIEW` | `VIEW` | `CREATE` | `AUDIT` |
| `CAPABILITY-032` | Vulnerable Citizen Flagging | `MODULE-005` | `VIEW` | `CREATE` | `VIEW` | `VIEW` | `CREATE` | `AUDIT` |
| `CAPABILITY-033` | Aadhaar OTP ABHA Bridge | `MODULE-005` | `VIEW` | `CREATE` | `VIEW` | `VIEW` | `CREATE` | `AUDIT` |
| `CAPABILITY-034` | Demographic ABHA Creation | `MODULE-005` | `VIEW` | `CREATE` | `VIEW` | `VIEW` | `CREATE` | `AUDIT` |
| `CAPABILITY-035` | Deterministic UHID Minting | `MODULE-005` | `VIEW` | `CREATE` | `VIEW` | `VIEW` | `CREATE` | `AUDIT` |
| `CAPABILITY-036` | Soundex / Double-Metaphone Matching | `MODULE-005` | `VIEW` | `CREATE` | `VIEW` | `VIEW` | `CREATE` | `AUDIT` |
| `CAPABILITY-037` | Bilingual Consent Presentation | `MODULE-006` | `VIEW` | `NONE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-038` | Digital Signature / Thumbprint Capture | `MODULE-006` | `VIEW` | `NONE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-039` | Granular Purpose-Based Consent | `MODULE-006` | `VIEW` | `NONE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-040` | Consent Revocation Workflow | `MODULE-006` | `VIEW` | `NONE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-041` | Guardian Relationship Verification | `MODULE-006` | `VIEW` | `NONE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-042` | Implied Emergency Consent | `MODULE-006` | `VIEW` | `NONE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-043` | Daily Token Counter | `MODULE-007` | `VIEW` | `CREATE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-044` | Station Route Calculation | `MODULE-007` | `VIEW` | `CREATE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-045` | Acuity-Based Insertion | `MODULE-007` | `VIEW` | `CREATE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-046` | Vulnerable Citizen Interleaving | `MODULE-007` | `VIEW` | `CREATE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-047` | ESC/POS Thermal Printing | `MODULE-007` | `VIEW` | `CREATE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-048` | Virtual SMS Token Fallback | `MODULE-007` | `VIEW` | `CREATE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-049` | Next-Patient Call Action | `MODULE-008` | `VIEW` | `CREATE` | `VIEW` | `VIEW` | `CREATE` | `AUDIT` |
| `CAPABILITY-050` | No-Show & Recall Management | `MODULE-008` | `VIEW` | `CREATE` | `VIEW` | `VIEW` | `CREATE` | `AUDIT` |
| `CAPABILITY-051` | HDMI Waiting Hall Display | `MODULE-008` | `VIEW` | `CREATE` | `VIEW` | `VIEW` | `CREATE` | `AUDIT` |
| `CAPABILITY-052` | Text-to-Speech Audio Chime | `MODULE-008` | `VIEW` | `CREATE` | `VIEW` | `VIEW` | `CREATE` | `AUDIT` |
| `CAPABILITY-053` | Dynamic Load Distribution | `MODULE-008` | `VIEW` | `CREATE` | `VIEW` | `VIEW` | `CREATE` | `AUDIT` |
| `CAPABILITY-054` | Queue Pausing & Resumption | `MODULE-008` | `VIEW` | `CREATE` | `VIEW` | `VIEW` | `CREATE` | `AUDIT` |
| `CAPABILITY-055` | Kiosk Exit Rating | `MODULE-020` | `NONE` | `NONE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-056` | Medicine Receipt Confirmation | `MODULE-020` | `NONE` | `NONE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-057` | Multilingual Ticket Intake | `MODULE-020` | `NONE` | `NONE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-058` | Automated SLA Timer | `MODULE-020` | `NONE` | `NONE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-059` | Zonal Escalation Trigger | `MODULE-020` | `NONE` | `NONE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-060` | Citizen Resolution Feedback | `MODULE-020` | `NONE` | `NONE` | `NONE` | `NONE` | `CREATE` | `AUDIT` |
| `CAPABILITY-061` | Longitudinal History Viewer | `MODULE-009` | `EDIT` | `CREATE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-062` | Vitals Telemetry Banner | `MODULE-009` | `EDIT` | `CREATE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-063` | Rapid Clinical Templates | `MODULE-009` | `EDIT` | `CREATE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-064` | Keyboard Shortcut Navigation | `MODULE-009` | `EDIT` | `CREATE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-065` | Cryptographic Note Locking | `MODULE-009` | `EDIT` | `CREATE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-066` | Clinical Addendum Workflow | `MODULE-009` | `EDIT` | `CREATE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-067` | Primary Care Curated Coding | `MODULE-010` | `CREATE` | `VIEW` | `NONE` | `VIEW` | `NONE` | `AUDIT` |
| `CAPABILITY-068` | Synonym & Local Name Mapping | `MODULE-010` | `CREATE` | `VIEW` | `NONE` | `VIEW` | `NONE` | `AUDIT` |
| `CAPABILITY-069` | Chronic Condition Tagging | `MODULE-010` | `CREATE` | `VIEW` | `NONE` | `VIEW` | `NONE` | `AUDIT` |
| `CAPABILITY-070` | Provisional vs. Confirmed Status | `MODULE-010` | `CREATE` | `VIEW` | `NONE` | `VIEW` | `NONE` | `AUDIT` |
| `CAPABILITY-071` | IDSP Notifiable Flagging | `MODULE-010` | `CREATE` | `VIEW` | `NONE` | `VIEW` | `NONE` | `AUDIT` |
| `CAPABILITY-072` | Outbreak Geographic Dispatch | `MODULE-010` | `CREATE` | `VIEW` | `NONE` | `VIEW` | `NONE` | `AUDIT` |
| `CAPABILITY-073` | Generic Drug Selection | `MODULE-011` | `EDIT` | `VIEW` | `NONE` | `CREATE` | `NONE` | `AUDIT` |
| `CAPABILITY-074` | Standard Sig Frequency Picker | `MODULE-011` | `EDIT` | `VIEW` | `NONE` | `CREATE` | `NONE` | `AUDIT` |
| `CAPABILITY-075` | Drug-Drug Interaction Alert | `MODULE-011` | `EDIT` | `VIEW` | `NONE` | `CREATE` | `NONE` | `AUDIT` |
| `CAPABILITY-076` | Allergy Cross-Check | `MODULE-011` | `EDIT` | `VIEW` | `NONE` | `CREATE` | `NONE` | `AUDIT` |
| `CAPABILITY-077` | Weight-Based Pediatric Dosing | `MODULE-011` | `EDIT` | `VIEW` | `NONE` | `CREATE` | `NONE` | `AUDIT` |
| `CAPABILITY-078` | Electronic Prescription Sign & Dispatch | `MODULE-011` | `EDIT` | `VIEW` | `NONE` | `CREATE` | `NONE` | `AUDIT` |
| `CAPABILITY-079` | Electronic Order Queue | `MODULE-012` | `CREATE` | `NONE` | `VIEW` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-080` | Sample Barcode Labeling | `MODULE-012` | `CREATE` | `NONE` | `VIEW` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-081` | Rapid Diagnostic Result Entry | `MODULE-012` | `CREATE` | `NONE` | `VIEW` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-082` | POC Analyzer Serial Bridge | `MODULE-012` | `CREATE` | `NONE` | `VIEW` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-083` | Panic Value Threshold Detector | `MODULE-012` | `CREATE` | `NONE` | `VIEW` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-084` | Urgent Doctor Notification Push | `MODULE-012` | `CREATE` | `NONE` | `VIEW` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-085` | Specialist Specialty Directory | `MODULE-029` | `CREATE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-086` | Store-and-Forward Tele-Dermatology | `MODULE-029` | `CREATE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-087` | Low-Bandwidth Adaptive WebRTC | `MODULE-029` | `CREATE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-088` | Synchronized Clinical Note Viewer | `MODULE-029` | `CREATE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-089` | Specialist e-Sign Endorsement | `MODULE-029` | `CREATE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-090` | Tele-Consultation Compliance Audit | `MODULE-029` | `CREATE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-091` | Pharmacy Electronic Worklist | `MODULE-013` | `VIEW` | `NONE` | `EXECUTE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-092` | Partial Dispense & Substitute Handling | `MODULE-013` | `VIEW` | `NONE` | `EXECUTE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-093` | Barcode Scanner Hardware Interface | `MODULE-013` | `VIEW` | `NONE` | `EXECUTE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-094` | FEFO Expiry Enforcement | `MODULE-013` | `VIEW` | `NONE` | `EXECUTE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-095` | Bilingual Label Generator | `MODULE-013` | `VIEW` | `NONE` | `EXECUTE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-096` | Dispense Commit & Ledger Deduction | `MODULE-013` | `VIEW` | `NONE` | `EXECUTE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-097` | Perpetual Stock Balance Tracking | `MODULE-014` | `VIEW` | `VIEW` | `CREATE` | `VIEW` | `NONE` | `AUDIT` |
| `CAPABILITY-098` | Low Stock Threshold Alert | `MODULE-014` | `VIEW` | `VIEW` | `CREATE` | `VIEW` | `NONE` | `AUDIT` |
| `CAPABILITY-099` | Automated FEFO Shelf Guidance | `MODULE-014` | `VIEW` | `VIEW` | `CREATE` | `VIEW` | `NONE` | `AUDIT` |
| `CAPABILITY-100` | Expired Drug Quarantine Lock | `MODULE-014` | `VIEW` | `VIEW` | `CREATE` | `VIEW` | `NONE` | `AUDIT` |
| `CAPABILITY-101` | Physical Stock Count Sheet | `MODULE-014` | `VIEW` | `VIEW` | `CREATE` | `VIEW` | `NONE` | `AUDIT` |
| `CAPABILITY-102` | Variance Adjustment Signoff | `MODULE-014` | `VIEW` | `VIEW` | `CREATE` | `VIEW` | `NONE` | `AUDIT` |
| `CAPABILITY-103` | Automated Reorder Quantity Formula | `MODULE-015` | `NONE` | `VIEW` | `CREATE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-104` | Emergency Indent Escalation | `MODULE-015` | `NONE` | `VIEW` | `CREATE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-105` | Electronic Delivery Challan Inward | `MODULE-015` | `NONE` | `VIEW` | `CREATE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-106` | Carton Barcode Verification | `MODULE-015` | `NONE` | `VIEW` | `CREATE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-107` | IoT Temperature Sensor Bridge | `MODULE-015` | `NONE` | `VIEW` | `CREATE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-108` | Thermal Breach SMS Alert | `MODULE-015` | `NONE` | `VIEW` | `CREATE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-109` | Central Formulary Publishing | `MODULE-016` | `VIEW` | `NONE` | `VIEW` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-110` | Dosage Unit Standardization | `MODULE-016` | `VIEW` | `NONE` | `VIEW` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-111` | Brand Cross-Reference Search | `MODULE-016` | `VIEW` | `NONE` | `VIEW` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-112` | Controlled Drug Scheduling Flag | `MODULE-016` | `VIEW` | `NONE` | `VIEW` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-113` | Approved Substitution Matrix | `MODULE-016` | `VIEW` | `NONE` | `VIEW` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-114` | Formulary Restriction Enforcer | `MODULE-016` | `VIEW` | `NONE` | `VIEW` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-115` | SBAR Summary Generation | `MODULE-017` | `CREATE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-116` | Receiving Hospital Capacity Check | `MODULE-017` | `CREATE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-117` | 108 Ambulance CAD Integration | `MODULE-017` | `CREATE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-118` | Ambulance ETA Telemetry | `MODULE-017` | `CREATE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-119` | Referral Handover Verification | `MODULE-017` | `CREATE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-120` | Post-Referral Counter-Referral Push | `MODULE-017` | `CREATE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-121` | NCD Target Protocol Tracking | `MODULE-018` | `CREATE` | `VIEW` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-122` | Medication Possession Ratio (MPR) | `MODULE-018` | `CREATE` | `VIEW` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-123` | Automated 30-Day Refill Scheduling | `MODULE-018` | `CREATE` | `VIEW` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-124` | Overdue Defaulter Detector | `MODULE-018` | `CREATE` | `VIEW` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-125` | ASHA Ward Tracing Export | `MODULE-018` | `CREATE` | `VIEW` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-126` | Home Visit Adherence Verification | `MODULE-018` | `CREATE` | `VIEW` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-127` | DLT-Compliant Bilingual SMS | `MODULE-019` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-128` | Queue Delay Alert | `MODULE-019` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-129` | Lab Report PDF Download via WhatsApp | `MODULE-019` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-130` | Queue Position Bot | `MODULE-019` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-131` | Targeted Ward Health Advisory | `MODULE-019` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-132` | Opt-Out Preference Management | `MODULE-019` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-133` | 1-Click Diagnostic Dump | `MODULE-028` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-134` | Peripheral Self-Test Wizard | `MODULE-028` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-135` | Zonal Field Engineer Dispatch | `MODULE-028` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-136` | SLA Clock & Breach Escalation | `MODULE-028` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-137` | Hardware Asset Lifecycle Tracking | `MODULE-028` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-138` | Preventive Maintenance Scheduler | `MODULE-028` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-139` | Sequential Hash Chaining | `MODULE-021` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-140` | Zero-Plaintext PHI Masking | `MODULE-021` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-141` | Ledger Integrity Verification | `MODULE-021` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-142` | Forensic Actor Search | `MODULE-021` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-143` | Encrypted Glacier Export | `MODULE-021` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-144` | Statutory 7-Year Retention Enforcer | `MODULE-021` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-145` | Citywide KPI Aggregate Stat Panels | `MODULE-022` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-146` | Code Red Emergency Monitor | `MODULE-022` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-147` | Zonal Performance Ranking | `MODULE-022` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-148` | Chronic Disease Control Tracker | `MODULE-022` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-149` | Clinic Bottleneck Heatmap | `MODULE-022` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-150` | Automated PDF Executive Briefing | `MODULE-022` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-151` | Deterministic Rule Pre-Screening | `MODULE-023` | `VIEW` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-152` | Antibiotic Stewardship Nudge | `MODULE-023` | `VIEW` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-153` | Evidence Citation Display | `MODULE-023` | `VIEW` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-154` | Clinician Autonomy Guarantee | `MODULE-023` | `VIEW` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-155` | AI Override Logging | `MODULE-023` | `VIEW` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-156` | Demographic Parity Audit | `MODULE-023` | `VIEW` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-157` | ABHA Verification & Linking | `MODULE-024` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `AUDIT` |
| `CAPABILITY-158` | ABHA Scan-and-Share QR Intake | `MODULE-024` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `AUDIT` |
| `CAPABILITY-159` | FHIR Care Context Publishing | `MODULE-024` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `AUDIT` |
| `CAPABILITY-160` | HIP Data Transfer Encryption | `MODULE-024` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `AUDIT` |
| `CAPABILITY-161` | Consent Artifact Request Dispatch | `MODULE-024` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `AUDIT` |
| `CAPABILITY-162` | External FHIR Record Viewer | `MODULE-024` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `EXECUTE` | `AUDIT` |
| `CAPABILITY-163` | Autonomous Local Execution | `MODULE-025` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-164` | Local Encryption-at-Rest | `MODULE-025` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-165` | Atomic Mutation Enqueue | `MODULE-025` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-166` | Background Network Probing & Replay | `MODULE-025` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-167` | Deterministic CRDT Merge | `MODULE-025` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-168` | Inventory Discrepancy Quarantine | `MODULE-025` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-169` | Automated HMIS Metric Aggregator | `MODULE-027` | `CREATE` | `VIEW` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-170` | HMIS XML / Excel Export | `MODULE-027` | `CREATE` | `VIEW` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-171` | ANC Trimester Registration Tracker | `MODULE-027` | `CREATE` | `VIEW` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-172` | Immunization Drop-Out Rate Calculator | `MODULE-027` | `CREATE` | `VIEW` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-173` | IDSP Form S Syndromic Extraction | `MODULE-027` | `CREATE` | `VIEW` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-174` | Medical Officer Report Signoff | `MODULE-027` | `CREATE` | `VIEW` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-175` | Disaster Mode Protocol Activation | `MODULE-030` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-176` | Flood / Outbreak Geospatial GIS Overlay | `MODULE-030` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-177` | Mobile Van GPS Dispatch | `MODULE-030` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-178` | Satellite / Cellular Backup Link | `MODULE-030` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-179` | Inter-Clinic Emergency Stock Transfer | `MODULE-030` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |
| `CAPABILITY-180` | Disaster Situation Report (SITREP) | `MODULE-030` | `NONE` | `NONE` | `NONE` | `NONE` | `NONE` | `AUDIT` |

## 5. Formal Separation of Duties (SoD) Invariants & Enforcement
To eliminate fraudulent collusion, clinical malpractice, and unauthorized fiscal write-offs, the platform enforces six inviolable Separation of Duties constraints:

| SoD Policy ID | Policy Title | Conflicting Roles | Operational Enforcement Mechanism | Risk Mitigated |
| :--- | :--- | :--- | :--- | :--- |
| `SOD-001` | **Prescriber vs Dispenser Separation** | `ROLE-015 (Doctor)` vs `ROLE-017 (Pharmacist)` | Cryptographic role barrier; digital signature verification on prescription payload; dispensing API rejects caller if role is Prescriber. | Prevents prescription fraud, medication theft, and unauthorized drug distribution. |
| `SOD-002` | **Diagnostic Orderer vs Diagnostic Lab Signer** | `ROLE-015 (Doctor)` vs `ROLE-018 (Lab Technician)` | Specimen accessioning requires distinct MLT credential; doctor accounts blocked from lab result entry endpoints. | Prevents falsified diagnostic records, diagnostic collusion, and unverified clinical claims. |
| `SOD-003` | **Clinical Care Delivery vs Audit & Log Modification** | `ROLE-015 / ROLE-016 / ROLE-017` vs `ROLE-011 / ROLE-025 / ROLE-030` | Audit tables are write-once-read-many (WORM); HMAC digest signed by HSM; auditors have read-only audit schemas. | Ensures forensic immutability and prevents post-incident tampering with medical negligence evidence. |
| `SOD-004` | **Software Development vs Production Database DML** | `ROLE-006 / ROLE-007 (Developers)` vs `ROLE-008 (Lead DBA)` | Production database isolated in private VPC; access restricted to automated CI/CD pipeline service accounts and DBA jump host. | Prevents unauthorized database alterations, schema drift, and accidental production data corruption. |
| `SOD-005` | **Pharmacy Stock Custody vs Fiscal Stock Write-off Approval** | `ROLE-017 (Pharmacist)` vs `ROLE-026 (Finance Auditor)` | Multi-tier maker-checker: Pharmacist flags damage/expiry; Municipal Finance Auditor and Medical Superintendent must co-sign write-off. | Prevents pilferage, inventory leakage, and intentional stock misclassification. |
| `SOD-006` | **User Account Administration vs Security Access Audit** | `ROLE-001 / ROLE-026 (Admin)` vs `ROLE-011 (Security Officer)` | Role provisioning logged to immutable WORM ledger; periodic IAM reconciliation executed by Security Officer. | Prevents shadow admin accounts, privilege creep, and unauthorized privilege escalation. |

## 6. Privileged Operations & Maker-Checker Governance Matrix
High-stakes operational transactions requiring step-up authentication, dual-person co-signature, or statutory audit escalation:

| Op ID | Privileged Operation | Module | Authorized Roles | Step-Up Authentication | Dual Signoff? | Audit Level |
| :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| `PRIV-OP-001` | **Emergency Clinical Break-Glass PHI Access** | `MODULE-007` | `ROLE-015 (Doctor)`, `ROLE-016 (Nurse)` | Aadhaar OTP / Supervisor Biometric + Clinical Reason | `No (Permitted for immediate resuscitation), requires post-hoc audit review within 24h by ROLE-002` | `CRITICAL_WORM` |
| `PRIV-OP-002` | **High-Value Pharmaceutical Stock Write-Off (> ₹5,000)** | `MODULE-014` | `ROLE-017 (Maker)`, `ROLE-026 (Checker)`, `ROLE-015 (Co-Signer)` | Digital Signature (PKI / USB Token) | `Yes - 3-tier maker-checker approval workflow` | `FINANCIAL_AUDIT` |
| `PRIV-OP-003` | **Clinical Decision Support AI Rule Override** | `MODULE-023` | `ROLE-015 (Doctor)` | Doctor Password Re-Authentication + Structured Clinical Justification | `No (Real-time clinical autonomy), logged for retrospective pharmacovigilance review by ROLE-012` | `CLINICAL_SAFETY` |
| `PRIV-OP-004` | **Essential Drug List (EDL) Formulary De-Listing** | `MODULE-016` | `ROLE-012 (Initiator)`, `ROLE-002 (Approver)` | MFA Push / Hardware Security Key | `Yes - Clinical Safety Authority formal signoff` | `STATUTORY_POLICY` |
| `PRIV-OP-005` | **Emergency Edge Node Mesh Disaster Recovery Re-Sync** | `MODULE-024` | `ROLE-009 (DevOps Lead)`, `ROLE-024 (Field Engineer)` | SSH Ed25519 Hardware Token + Municipal Jump Host MFA | `Yes - Architect (ROLE-004) or SRE Lead authorization` | `INFRASTRUCTURE` |
| `PRIV-OP-006` | **Staff Role Elevation & Administrative Privilege Grant** | `MODULE-001` | `ROLE-001 (Sponsor)`, `ROLE-011 (Security Officer)` | FIDO2 / Hardware WebAuthn Key + Government SSO | `Yes - Maker-checker required for any tier L3+ privilege elevation` | `SECURITY_CRITICAL` |

## 7. Emergency Break-Glass Authorization Protocols
In acute clinical emergencies (e.g. unconscious trauma victim, cardiac arrest, pediatric convulsions), requiring immediate medical history access before informed digital consent can be captured:

1. **Eligibility:** Strictly restricted to Medical Officers (`ROLE-015`) and Triage Nurses (`ROLE-016`).
2. **Trigger Mechanism:** Staff clicks 'EMERGENCY BREAK-GLASS OVERRIDE' on the clinical console.
3. **Mandatory Step-Up:** Requires immediate biometric confirmation or supervisor PIN + selection of clinical justification: `ACUTE_TRAUMA`, `UNCONSCIOUS_PATIENT`, `ANAPHYLAXIS`, `MASS_CASUALTY`.
4. **Instant Access Grant:** Bypasses consent verification; decrypts longitudinal health records, active drug allergies, and recent prescriptions.
5. **Mandatory Post-Hoc Audit Escalation:** The break-glass event is committed with a high-priority SHA-256 HMAC tag to the immutable WORM ledger. A notification is dispatched to the Clinical Safety Authority (`ROLE-002`) and Legal Counsel (`ROLE-025`) requiring statutory justification review within 24 hours.

## 8. Autonomous Offline Edge Entitlements & Authority
When municipal fiber connections are severed, edge nodes must maintain deterministic local authority without cloud authorization servers:

| Frontline Cadre | Authorized Offline Capabilities | Prohibited Offline Operations | Maximum Offline Window | Vector Clock Priority |
| :--- | :--- | :--- | :---: | :---: |
| **Doctor (Medical Superintendent)** (`ROLE-015`) | Consultation Note Entry, e-Prescribing, Point-of-Care Lab Ordering, Emergency Break-Glass, Local Sync Trigger | Cannot modify formulary rules; cannot access external ABDM federated records not pre-cached. | `72 hours` | Tier 1 |
| **Staff Nurse Supervisor** (`ROLE-016`) | Vital Signs Recording, Triage Scoring, Queue Call Next, Emergency Alarm Broadcast | Cannot discharge or finalize doctor consultation. | `72 hours` | Tier 2 |
| **Pharmacist** (`ROLE-017`) | Barcode Scan Dispensing, Local Batch Stock Deduction, Physical Stock Tally | Cannot transfer stock between clinics; cannot approve financial write-offs. | `72 hours` | Tier 3 |
| **Lab Technician** (`ROLE-018`) | Specimen Accessioning, Rapid Test Result Entry, Local Panic Alert | Cannot order tests; cannot alter reference normal ranges. | `72 hours` | Tier 3 |
| **Front Desk Receptionist** (`ROLE-019`) | Offline Patient Registration, Local Token Minting, Emergency Paper Consent, Local Queue Calling | ABHA OTP verification deferred; biometric online deduplication queued for cloud sync. | `72 hours` | Tier 4 |

## 9. Access Recertification & Governance Cadence
To prevent privilege creep and maintain compliance with municipal public health regulations:

- **Monthly Staff Reconciliation:** Clinic Medical Superintendents (`ROLE-015`) review active staff rosters and revoke accounts for transferred or resigned staff.
- **Quarterly Role Audit:** Security & Data Privacy Officer (`ROLE-011`) audits RBAC/ABAC role bindings across all 183 clinics against HR payroll records.
- **Automated Inactive Suspension:** Accounts inactive for > 30 calendar days transition automatically to `SUSPENDED` status, requiring supervisor re-activation.
- **Emergency Revocation SLA:** Stolen devices or compromised credentials are permanently revoked across all edge nodes within < 60 seconds via push token revocation broadcasts.
