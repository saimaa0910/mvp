import os
import sys

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

# ==========================================
# PHASE 9: FRONTEND PLAN
# ==========================================

def build_phase_9():
    base_dir = os.path.join("docs", "09-frontend")
    
    screens = [
        ("SCR-01", "Staff Login Screen", "Clinic staff authentication with role selection and clinic picker.", "Nurse, Doctor, Pharmacist"),
        ("SCR-02", "Clinic Reception / Queue Dashboard", "Live view of clinic outpatient queue tokens (Waiting, Triage, Doctor, Done).", "Nurse, ANM"),
        ("SCR-03", "Patient Search & Demographics Screen", "Search by mobile, UHID, ABHA; display existing visit history.", "Nurse, ANM"),
        ("SCR-04", "New Patient Registration Form", "Bilingual entry of demographics, address, and optional ABHA verification.", "Nurse, ANM"),
        ("SCR-05", "Triage & Vitals Entry Screen", "Large touchscreen inputs for BP, Pulse, SpO2, Temperature, Blood Glucose.", "Nurse"),
        ("SCR-06", "Doctor Consultation Workspace", "Consolidated single-screen EMR showing history, vitals, complaint chips, notes.", "Doctor"),
        ("SCR-07", "Electronic Prescription Desk", "Formulary drug search, frequency selectors (1-0-1), duration, food instructions.", "Doctor"),
        ("SCR-08", "Point-of-Care Lab Order Modal", "Quick-order dialog for 14 essential primary care lab tests.", "Doctor"),
        ("SCR-09", "Secondary Referral Letter Modal", "Referral target selector (BBMP Hospital), clinical summary, referral reason.", "Doctor"),
        ("SCR-10", "Pharmacy Dispense Queue", "Pending electronic prescriptions awaiting dispensing.", "Pharmacist"),
        ("SCR-11", "Pharmacy Dispense Confirmation", "Batch selection (FEFO), expiry date verification, print bilingual slip.", "Pharmacist"),
        ("SCR-12", "Clinic Stock Ledger & Physical Count", "Current batch stock levels with quick adjustment for breakage/wastage.", "Pharmacist"),
        ("SCR-13", "Monthly Stock Indent Generator", "1-click generation of monthly medicine requisition to zonal warehouse.", "Pharmacist"),
        ("SCR-14", "Laboratory Worklist & Result Entry", "Pending diagnostic tests, specimen collection log, numeric result entry.", "Lab Tech"),
        ("SCR-15", "Follow-up & NCD Recall Scheduler", "Calendar view of scheduled 30-day recall appointments for diabetes/HTN.", "Nurse"),
        ("SCR-16", "Citizen Feedback Kiosk / QR", "Simple 3-question satisfaction rating (Wait time, Medicine, Staff).", "Citizen"),
        ("SCR-17", "Ward Grievance Submission Desk", "Log citizen service complaints with automated escalation ticket ID.", "ANM"),
        ("SCR-18", "Clinic Operational Performance Dashboard", "Daily footfall, average consultation time, out-of-stock count.", "Doctor, Nurse"),
        ("SCR-19", "Zonal Epidemiological Surveillance Map", "Geo-spatial map of fever clusters, dengue cases, and disease spikes.", "ZHO"),
        ("SCR-20", "Citywide Command Center (GBA/BBMP)", "Executive metrics for Special Commissioner: total footfall, stock health.", "CHO, Commissioner"),
        ("SCR-21", "System Administration & Audit Console", "User role assignment, clinic master data, security audit log inspector.", "SysAdmin")
    ]

    screen_cat = """# 🖥️ Frontend Screen Catalog (21 Master Screens)
## Namma Clinic Digital Health & Operations Platform
**Document Code:** FE-SCR-03 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Catalog of Frontline & Executive Screens

| Screen ID | Screen Name | Functional Scope & Workflow Role | Primary Actors |
| :--- | :--- | :--- | :--- |
"""
    for sid, sname, sdesc, sact in screens:
        screen_cat += f"| **{sid}** | `{sname}` | {sdesc} | {sact} |\n"
    
    write_file(os.path.join(base_dir, "03-screen-catalog.md"), screen_cat)

    fe_files = [
        ("01-design-system.md", "Design System & UI Tokens", "Tailwind typography, accessible color palette, high-contrast states, and clinical icons."),
        ("02-frontend-architecture.md", "Frontend Architecture Specification", "Next.js 14 / React 18 SPA architecture with Service Worker PWA and Dexie.js IndexedDB."),
        ("04-component-catalog.md", "Reusable Component Catalog", "Chips, VitalsInput, DrugSelector, PatientHeader, OfflineSyncBadge, ThermalSlipPreview."),
        ("05-role-screen-matrix.md", "Role-to-Screen Access Matrix", "Mapping staff roles to screens, restricting doctor EMR to doctors, stock to pharmacists."),
        ("06-navigation-map.md", "Information Architecture & Navigation Flow", "Touch-friendly bottom navigation for tablets; keyboard shortcuts (F1-F12) for doctor desktop."),
        ("07-state-management.md", "Client State Management Strategy", "Zustand for active session state, React Query for server cache, Dexie.js for persistent offline store."),
        ("08-offline-ui-states.md", "Offline UI States & Sync Badges", "Visual indicators: Green (Connected), Amber (Offline - Queued), Red (Sync Conflict)."),
        ("09-localization.md", "Bilingual Localization Architecture", "i18next setup with English (`en_IN`) and Kannada (`kn_IN`) JSON catalogs; zero hardcoded strings."),
        ("10-accessibility.md", "Accessibility & WCAG 2.1 AA Compliance", "Minimum 4.5:1 contrast ratios, 48px touch targets, full keyboard accessibility."),
        ("11-responsive-design.md", "Responsive Layout Strategy", "Optimized for 10-inch Android tablets (1280x800) and 21-inch clinic desktops (1920x1080)."),
        ("12-form-validation.md", "Client-Side Form Validation Strategy", "Zod schemas shared with backend for instant field validation and ergonomic error messages."),
        ("13-error-handling.md", "Frontend Fault Tolerance & Error Boundaries", "React error boundaries preventing whole-app crash; non-blocking toast notifications."),
        ("14-loading-states.md", "Optimistic UI & Skeleton Loading States", "Immediate optimistic UI updates on button tap with background async resolution."),
        ("15-printing.md", "Thermal Receipt & Slip Printing Strategy", "CSS `@media print` optimized for 2-inch (58mm) and 3-inch (80mm) thermal printers via USB/Bluetooth."),
        ("16-frontend-testing.md", "Frontend Testing Strategy", "Vitest unit tests, React Testing Library component tests, Playwright visual regression tests.")
    ]

    for fname, title, desc in fe_files:
        write_file(os.path.join(base_dir, fname), f"# 💻 Frontend Specification: {title}\n## Namma Clinic Platform\n\n### 1. Overview\n{desc}")

# ==========================================
# PHASE 10: SECURITY & PRIVACY
# ==========================================

def build_phase_10():
    base_dir = os.path.join("docs", "10-security")
    
    stride_content = """# 🛡️ Threat Model & STRIDE Vulnerability Analysis
## Namma Clinic Digital Health & Operations Platform
**Document Code:** SEC-STR-15 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. STRIDE Threat Analysis Matrix across 10 Attack Vectors

| Threat Vector | STRIDE Category | Threat Scenario | Impact | Security Control & Countermeasure | Verification Method |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **TV-01** | Spoofing | Adversary impersonates clinic doctor using stolen credentials. | High | WebAuthn / OTP MFA for sensitive access; automatic 15-min session timeout. | Auth Penetration Test |
| **TV-02** | Tampering | Malicious actor modifies drug stock counts in transit. | High | TLS 1.3 end-to-end encryption; cryptographic HMAC signatures on API requests. | MitM Proxy Inspection |
| **TV-03** | Repudiation | Staff member deletes patient consultation and denies action. | Critical | Append-only partitioned `access_audit_logs` with SHA-256 hash chaining. | Audit Log Integrity Test |
| **TV-04** | Info Disclosure | Unencrypted database dump leaks citizen diagnostic history. | Critical | AES-256-GCM data-at-rest encryption; KMS envelope keys; column-level masking. | Storage Encryption Audit |
| **TV-05** | Denial of Service | Flooding clinic API with bogus requests to halt registrations. | High | Redis leaky-bucket rate limiting; Cloudflare / AWS WAF DDoS mitigation. | k6 Stress Simulation |
| **TV-06** | Elevation of Priv | Staff nurse crafts API request to approve monthly indents. | High | Strict RBAC middleware checking user permissions on every route handler. | Privilege Escalation Test |
| **TV-07** | Offline Theft | Physical theft of clinic Android tablet containing cached visits. | Critical | Full disk encryption (Android dm-crypt); encrypted Dexie.js store; remote wipe. | Device Seizure Test |
| **TV-08** | Token Hijacking | XSS attack steals JWT session token from browser localStorage. | High | Tokens stored strictly in HttpOnly, SameSite=Strict cookies; strict CSP. | XSS Injection Test |
| **TV-09** | SQL Injection | SQL injection via patient search bar compromises database. | Critical | 100% parameterized queries via Prisma / Kysely ORM; zero raw string SQL. | DAST Static Analysis |
| **TV-10** | Supply Chain | Compromised npm dependency injects backdoor into clinic app. | Critical | Automated Dependabot & Snyk scanning; lockfile verification; signed builds. | SBOM & Trivy Scanner |
"""
    write_file(os.path.join(base_dir, "15-threat-model.md"), stride_content)

    sec_files = [
        ("01-security-architecture.md", "Security Architecture Blueprint", "Zero-Trust architecture, defense-in-depth, sovereign cloud boundary isolation."),
        ("02-authentication.md", "Authentication Specification", "Bcrypt (cost 12) password hashing, short-lived JWT access tokens (15m), rotating refresh tokens."),
        ("03-authorization-rbac.md", "Role-Based Access Control (RBAC)", "12 roles, 48 granular permissions, declarative `@RequirePermission` guards."),
        ("04-mfa.md", "Multi-Factor Authentication (MFA)", "Mandatory SMS/TOTP MFA for Zonal and Executive roles; optional biometric WebAuthn for doctors."),
        ("05-session-management.md", "Session Management & Invalidation", "Redis session store, concurrent login limits, 15-minute inactivity auto-lock."),
        ("06-password-policy.md", "Enterprise Password Policy", "Minimum 10 chars, complexity rules, 90-day rotation, 5 failed attempts lockout."),
        ("07-api-security.md", "API Transport & Boundary Hardening", "Strict CORS origin validation, TLS 1.3, CSP, HSTS headers, OWASP Top 10 mitigation."),
        ("08-data-encryption.md", "Cryptographic Architecture & Data Encryption", "AES-256-GCM encryption at rest for RDS/S3, TLS 1.3 in transit, envelope encryption."),
        ("09-key-management.md", "Key Management Strategy", "AWS KMS / HashiCorp Vault managed customer master keys with annual automated rotation."),
        ("10-audit-logging.md", "Immutable Security Audit Logging", "Logging all PII/SPD reads and mutations to append-only partitioned tables."),
        ("11-privacy.md", "Data Privacy & DPDP Act 2023 Compliance", "Enforcing purpose limitation, data minimization, storage limitation, citizen rights."),
        ("12-consent.md", "Explicit Consent Lifecycle Management", "Recording explicit, revocable patient consent prior to demographic and ABDM linkage."),
        ("13-data-classification.md", "Data Classification & Masking Rules", "Automated masking of Aadhaar/Phone on UI screens; PII redacting in logs."),
        ("14-secrets-management.md", "Secrets Management & Credentials Hygiene", "Zero secrets in Git; AWS Secrets Manager / Vault injection via environment variables."),
        ("16-security-testing.md", "Security Testing & SAST/DAST Pipeline", "SonarQube SAST, OWASP ZAP DAST, and automated container scanning in CI/CD."),
        ("17-vapt-plan.md", "Vulnerability Assessment & Penetration Testing (VAPT)", "Formal VAPT scope with CERT-In empanelled auditor prior to citywide go-live."),
        ("18-incident-response.md", "Security Incident Response Playbook", "Severity classification (P0-P3), escalation tree, 6-hour CERT-In breach reporting."),
        ("19-backup-security.md", "Backup Encryption & Security Strategy", "Immutable AWS S3 Glacier backups with Object Lock and cross-region replication."),
        ("20-device-security.md", "Clinic Endpoint & Device Security Policy", "Mobile Device Management (MDM) enrollment, remote lock/wipe, USB port restriction.")
    ]

    for fname, title, desc in sec_files:
        write_file(os.path.join(base_dir, fname), f"# 🔒 Security Specification: {title}\n## Namma Clinic Platform\n\n### 1. Specification\n{desc}")

# ==========================================
# PHASE 11: QA / TEST STRATEGY
# ==========================================

def build_phase_11():
    base_dir = os.path.join("docs", "11-qa")
    
    e2e_content = """# 🧪 End-to-End (E2E) Test Plan & Patient Journey Scenarios
## Namma Clinic Digital Health & Operations Platform
**Document Code:** QA-E2E-06 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Primary Patient Journey E2E Scenarios (Playwright Automation)

#### Scenario E2E-01: Standard Outpatient Visit (Registration -> Triage -> Doctor -> Pharmacy)
- **Preconditions:** Active clinic session in Ward 150; nurse, doctor, and pharmacist logged in.
- **Step 1 (Nurse):** Register new patient (Name: Ramesh, Age: 45, Gender: Male). System issues Token `T-001`.
- **Step 2 (Nurse):** Capture vitals (BP: 130/85, Pulse: 74, Temp: 98.4°F, Glucose: 110 mg/dL). Vitals saved.
- **Step 3 (Doctor):** Doctor selects Token `T-001` from queue. Reviews vitals. Selects chief complaint 'Headache x 3 days'. Selects provisional diagnosis 'Tension Headache'. Prescribes Paracetamol 500mg (1-0-1 x 3 days). Signs prescription.
- **Step 4 (Pharmacist):** Pharmacist opens pending queue. Sees `T-001`. Scans batch `PARA-2026-08`. Confirms 6 tablets dispensed. Clicks 'Dispense'.
- **Verification:** Visit status transitions to 'Completed'; stock ledger for Paracetamol decreases by 6; patient receives SMS confirmation; audit record created.

#### Scenario E2E-02: Offline Emergency Consultation with Background Sync
- **Preconditions:** Clinic tablet loses internet connectivity (airplane mode simulated).
- **Step 1:** Nurse registers walk-in emergency trauma patient. Token `E-001` generated in local IndexedDB.
- **Step 2:** Doctor documents emergency wound dressing and tetanus toxoid administration.
- **Step 3:** Network reconnected. Background sync engine triggers.
- **Verification:** Token `E-001` and encounter data sync to server within 15 seconds; zero data loss; no duplicate IDs created.
"""
    write_file(os.path.join(base_dir, "06-e2e-test-plan.md"), e2e_content)

    qa_files = [
        ("01-test-strategy.md", "Master Quality Assurance & Testing Strategy", "Test pyramid: 70% Unit tests, 20% Integration tests, 10% E2E tests."),
        ("02-test-levels.md", "Test Levels & Scope Definition", "Unit (Vitest), Integration (Supertest), E2E (Playwright), Performance (k6)."),
        ("03-unit-test-plan.md", "Unit Testing Specification", "Target >=85% code coverage on business logic, calculation engines, and DTO validators."),
        ("04-integration-test-plan.md", "Integration Testing Specification", "Testing database transactions, repository queries, and service boundary contracts."),
        ("05-api-test-plan.md", "API Contract Testing Plan", "Automated validation of all 65+ REST endpoints against OpenAPI 3.1 schema schemas."),
        ("07-ui-test-plan.md", "Frontend Component & UI Testing Plan", "React Testing Library suites verifying form validation, state transitions, and error toasts."),
        ("08-performance-test-plan.md", "Performance & Load Testing Strategy", "Simulating 183 clinics with peak 500 req/sec; verifying p95 latency < 300ms."),
        ("09-security-test-plan.md", "Security Testing & Vulnerability Scanning", "Automated OWASP ZAP scans, dependency checks, and broken auth test cases."),
        ("10-offline-test-plan.md", "Offline Resilience & Partition Testing", "Simulating intermittent network drops, browser refresh during sync, and conflict merges."),
        ("11-data-quality-test-plan.md", "Data Quality & Migration Validation Plan", "Great Expectations suites verifying seed data, check constraints, and referential integrity."),
        ("12-accessibility-test-plan.md", "Accessibility & WCAG Testing Plan", "Axe-core automated scans ensuring 100% WCAG 2.1 Level AA compliance."),
        ("13-localization-test-plan.md", "Localization & Kannada Language Testing", "Automated check for missing translation keys across all 21 frontend screens."),
        ("14-regression-strategy.md", "Automated Regression Testing Framework", "Full regression suite running on every pull request before merging to main."),
        ("15-uat-plan.md", "User Acceptance Testing (UAT) Plan", "1-week structured UAT with 10 BBMP doctors and 10 staff nurses."),
        ("16-pilot-test-plan.md", "20-Clinic Pilot Operational Test Plan", "Field acceptance criteria across 20 representative high/medium/low clinics."),
        ("17-test-data-strategy.md", "Synthetic Test Data Generation Strategy", "Generating 10,000 synthetic patient records and realistic clinic encounters."),
        ("18-test-environment.md", "Test Environment Provisioning & Data Isolation", "Dedicated Test environment mirroring production database configuration."),
        ("19-quality-gates.md", "Quality Gates & Pipeline Pass/Fail Criteria", "Zero critical bugs, 85% test coverage, clean security scans required for release.")
    ]

    for fname, title, desc in qa_files:
        write_file(os.path.join(base_dir, fname), f"# 🧪 QA Specification: {title}\n## Namma Clinic Platform\n\n### 1. Overview\n{desc}")

def main():
    build_phase_9()
    build_phase_10()
    build_phase_11()

if __name__ == "__main__":
    main()
