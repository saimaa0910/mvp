#!/usr/bin/env python3
"""
build_data_03_to_06.py
Generates data and generator scripts for:
- Document 03: Non-Functional Requirements (NFR-001 to NFR-050)
- Document 04: Business Rules (BRULE-001 to BRULE-050)
- Document 05: Clinical Rules (CR-001 to CR-050)
- Document 06: Operational Rules (OR-001 to OR-050)
"""

import os

# ==============================================================================
# NFR DEFINITIONS (50 items)
# ==============================================================================
NFR_ITEMS = [
    ("NFR-001", "API Gateway End-to-End Latency Threshold", "Performance", "MUST",
     "The platform API gateway shall process authenticated requests with a p95 latency strictly under 120ms under peak municipal load.",
     "p95 < 120ms, p99 < 300ms across 500 requests/sec", "Prometheus histogram `http_request_duration_seconds`",
     "Automated k6 load test simulating 183 concurrent clinics", "Solution Architect", "PERF-001"),

    ("NFR-002", "Client-Side Application Memory Consumption Cap", "Performance", "MUST",
     "The client PWA shall operate continuously within a strict maximum memory footprint of 150MB RAM on refurbished clinic terminals.",
     "Client RSS / Heap memory <= 150MB after 8 hours continuous execution", "Chrome DevTools memory heap snapshots and performance telemetry",
     "8-hour automated Playwright memory leak test with 500 mock consultations", "Frontend Architect", "PERF-002"),

    ("NFR-003", "IndexedDB Client Local Transaction Write Latency", "Performance", "MUST",
     "The local Dexie.js storage engine shall commit operational mutations within 10ms of operator confirmation.",
     "IndexedDB ACID transaction commit latency p95 < 10ms", "Client-side Performance Navigation Timing API",
     "Automated Vitest browser benchmark writing 1,000 sequential mutations", "Frontend Lead", "PERF-003"),

    ("NFR-004", "Patient Demographic Search Response Time", "Performance", "MUST",
     "The patient search subsystem shall return matching records across 500,000 municipal records within 150ms.",
     "Search query execution latency p95 < 150ms for name and mobile queries", "PostgreSQL `pg_stat_statements` and OpenTelemetry span timing",
     "k6 performance test querying database seeded with 500,000 synthetic patient records", "Database Architect", "PERF-004"),

    ("NFR-005", "Thermal Paper Slip ESC/POS Print Execution Latency", "Performance", "MUST",
     "The Web Serial printer driver shall dispatch ESC/POS raster and text commands to connected thermal printers within 500ms.",
     "Command dispatch and print buffer acknowledgment < 500ms", "Client-side hardware event telemetry logs",
     "Hardware test rig with USB-connected 58mm/80mm thermal printers executing 100 prints", "Hardware Integration Lead", "PERF-005"),

    ("NFR-006", "Point-of-Care Laboratory Result Entry Latency", "Performance", "MUST",
     "The diagnostic subsystem shall validate and save laboratory test results within 100ms of entry confirmation.",
     "Result entry validation and persistence p95 < 100ms", "OpenTelemetry span `namma.clinic.lab.result_save`",
     "Automated API load test executing 20 concurrent lab result entries", "Backend Lead", "PERF-006"),

    ("NFR-007", "Background Offline Mutation Sync Throughput", "Performance", "MUST",
     "The background sync worker shall ingest and commit buffered offline mutations at a minimum sustained throughput of 50 records/second.",
     "Sustained replay throughput >= 50 mutations/second per clinic node", "Central sync pipeline Prometheus counter `sync_mutations_ingested_total`",
     "Network reconnection simulation benchmarking 500 queued mutations", "Sync Architect", "PERF-007"),

    ("NFR-008", "Central Platform Production Service Availability", "Availability", "MUST",
     "The central cloud platform shall maintain 99.5% service availability during mandated clinic hours (08:30 to 18:00 IST Monday-Saturday).",
     "Monthly service uptime >= 99.5% excluding scheduled maintenance windows", "CloudWatch / Grafana synthetic heartbeat probes every 60 seconds",
     "Third-party external uptime monitoring probe validating HTTP 200 health check", "DevOps Lead", "AVAIL-001"),

    ("NFR-009", "Autonomous Offline Clinic Operational Continuity", "Availability", "MUST",
     "Clinic workstations shall sustain 100% autonomous clinical care delivery for at least 8 hours during total WAN/LAN failure.",
     "Zero user-blocking errors or service denials during 8 hours of network severance", "Local transaction journal verification after simulated network severance",
     "Full-day clinic simulation running disconnected from network with 100 visits", "Principal Architect", "AVAIL-002"),

    ("NFR-010", "Disaster Recovery Recovery Point Objective (RPO)", "Availability", "MUST",
     "The platform shall maintain continuous database streaming replication to a secondary availability zone ensuring RPO < 5 minutes.",
     "Maximum permissible data loss in disaster scenario < 300 seconds of transactions", "PostgreSQL streaming replication lag telemetry `pg_stat_replication`",
     "Semi-annual disaster recovery chaos drill cutting primary database instance", "Database Architect", "AVAIL-003"),

    ("NFR-011", "Disaster Recovery Recovery Time Objective (RTO)", "Availability", "MUST",
     "The platform shall execute automated cloud failover restoring full read/write service within 30 minutes of a major data center outage.",
     "Full service restoration elapsed time < 1,800 seconds", "CloudWatch alarm to automated DNS failover completion timestamp delta",
     "Simulated primary region outage validating automated Terraform/Kubernetes failover", "Cloud Architect", "AVAIL-004"),

    ("NFR-012", "Graceful UI Degradation During Network Instability", "Resilience", "MUST",
     "The frontend PWA shall transition seamlessly between online, degraded, and offline states without page reloads or data loss.",
     "Zero unhandled JavaScript exceptions; visual banner updates state within 2 seconds", "Playwright network throttling test (Slow 3G, Offline, Flaky)",
     "E2E test suite simulating intermittent 50% packet drop and 2000ms latency", "Frontend Lead", "AVAIL-005"),

    ("NFR-013", "Transport Layer Security (TLS 1.3) Enforcement", "Security", "MUST",
     "All network communications between clinic browsers, peripheral bridges, and cloud APIs shall enforce TLS 1.3 encryption.",
     "100% network traffic over TLS 1.3; older TLS versions (1.0, 1.1, 1.2) rejected at gateway", "SSL Labs automated scanner score A+ and Qualys TLS audit report",
     "Automated CI vulnerability pipeline scanning gateway TLS cipher configuration", "Security Engineer", "SECR-001"),

    ("NFR-014", "Cryptographic Data Protection at Rest (AES-256-GCM)", "Security", "MUST",
     "All personal health information and citizen demographic records shall be encrypted at rest in PostgreSQL using AES-256-GCM.",
     "All PII columns (Aadhaar, ABHA, mobile, clinical notes) encrypted with envelope keys", "Automated database dump inspection confirming zero plaintext PII",
     "Security audit inspecting database physical storage blocks and KMS key rotation logs", "Security Architect", "SECR-002"),

    ("NFR-015", "Cryptographic Local Client Storage Encryption", "Security", "MUST",
     "All data stored in client-side IndexedDB shall be encrypted using AES-GCM via the browser native Web Cryptography API.",
     "Zero plaintext citizen PII readable in raw browser IndexedDB inspection tools", "Automated Playwright test reading raw IndexedDB blocks verifying ciphertext",
     "Client security penetration test attempting to extract PII from disk cache", "Security Engineer", "SECR-003"),

    ("NFR-016", "Role-Based Access Control (RBAC) Least Privilege", "Security", "MUST",
     "Every API endpoint and UI action shall enforce strict role-based access control, returning HTTP 403 Forbidden for unauthorized requests.",
     "Zero unauthorized endpoint invocations permitted across all 150+ API routes", "Automated matrix test running all endpoints against all 5 primary user roles",
     "Security penetration test verifying horizontal and vertical privilege escalation", "Security Lead", "SECR-004"),

    ("NFR-017", "Argon2id Staff Password Hashing & Complexity Policy", "Security", "MUST",
     "User passwords shall be hashed using Argon2id (m=65536, t=3, p=4) and require a minimum length of 12 characters.",
     "100% password hashes conform to Argon2id specification; zero legacy hashes allowed", "Static analysis of authentication codebase and database schema checks",
     "Brute-force dictionary test against generated password hashes", "Security Engineer", "SECR-005"),

    ("NFR-018", "Brute-Force Authentication Rate Limiting & Account Lockout", "Security", "MUST",
     "The authentication service shall lock user accounts for 15 minutes after 5 consecutive failed login attempts.",
     "Account locked on 5th failure; lockout duration enforced at 900 seconds", "Authentication service Redis rate limiting telemetry logs",
     "Automated security integration test executing 6 rapid incorrect login attempts", "Backend Lead", "SECR-006"),

    ("NFR-019", "Tamper-Evident Immutable WORM Audit Logging", "Security", "MUST",
     "All clinical, pharmacy, and administrative state mutations shall emit append-only audit events to Grafana Loki with SHA-256 hash chaining.",
     "100% mutation coverage; zero retroactive modification or deletion permissible", "Loki audit storage log query verifying cryptographic hash chain continuity",
     "Audit verification script crawling 10,000 sequential audit log hashes", "Compliance Officer", "SECR-007"),

    ("NFR-020", "Content Security Policy (CSP) & Web Application Defense", "Security", "MUST",
     "The web frontend shall enforce strict Content Security Policy headers blocking inline scripts, unauthorized origins, and clickjacking.",
     "CSP score A+; headers include `default-src 'self'`, `frame-ancestors 'none'`, `X-Content-Type-Options 'nosniff'`", "Mozilla Observatory security scan report",
     "Automated DAST security scan testing for reflected and stored XSS vulnerabilities", "Security Lead", "SECR-008"),

    ("NFR-021", "Digital Personal Data Protection (DPDP) Act Consent Model", "Privacy", "MUST",
     "The platform shall enforce explicit consent capture and purpose limitation for all personal health data processing.",
     "100% of patient records contain valid cryptographic consent artifact", "Privacy compliance audit verifying consent linkage in database",
     "Legal and privacy audit inspecting consent workflow and revocation mechanisms", "Data Protection Officer", "PRIV-001"),

    ("NFR-022", "De-Identification & k-Anonymity for Public Health Data", "Privacy", "MUST",
     "All datasets exported for municipal analytics or epidemiology shall enforce k-anonymity (k>=5) and l-diversity.",
     "Zero direct identifiers; quasi-identifiers aggregated into bins of at least 5 individuals", "ARX Data Anonymization Tool validation report on export samples",
     "Automated privacy test scanning analytical export tables for re-identification risk", "Data Protection Officer", "PRIV-002"),

    ("NFR-023", "Bilingual User Interface Completeness (Kannada & English)", "Localization", "MUST",
     "100% of UI labels, buttons, error messages, and clinical chips shall be fully localized in Kannada and English.",
     "Zero untranslated i18n keys or hardcoded English strings in Kannada mode", "Automated static i18n key audit comparing `en.json` and `kn.json` bundles",
     "Bilingual clinical review panel verifying accuracy of Kannada medical terminology", "Localization Lead", "LOC-001"),

    ("NFR-024", "Unicode Normalization & Noto Sans Kannada Typography", "Localization", "MUST",
     "The platform shall render all Kannada text using Unicode UTF-8 normalization (NFC) and embedded Noto Sans Kannada web fonts.",
     "Zero broken glyphs, missing font fallbacks, or unrendered conjunct consonants", "Visual regression test capturing screenshots across all 50 clinic UI views",
     "Automated Playwright typography test inspecting font computed styles on client", "UI Architect", "LOC-002"),

    ("NFR-025", "Standardized Indian Locale Date, Time & Currency Formatting", "Localization", "MUST",
     "All dates shall format as DD/MM/YYYY, times in 24-hour HH:mm, numbers in Indian numbering system, and currency in INR (₹).",
     "100% compliance with Indian locale standards across all screens and printouts", "Automated unit test suite validating formatting utility outputs",
     "Visual audit of generated thermal receipts and PDF laboratory reports", "Frontend Lead", "LOC-003"),

    ("NFR-026", "Web Content Accessibility Guidelines (WCAG 2.1 AA) Compliance", "Accessibility", "MUST",
     "All web interfaces shall comply strictly with WCAG 2.1 Level AA accessibility standards.",
     "Zero WCAG 2.1 AA violations detected across all interactive clinic forms", "Automated axe-core accessibility scanner integrated into CI pipeline",
     "Manual accessibility audit testing with NVDA screen reader and keyboard-only navigation", "Accessibility Lead", "A11Y-001"),

    ("NFR-027", "High-Contrast Visual Styling & Minimum Contrast Ratios", "Accessibility", "MUST",
     "All text elements shall maintain a minimum color contrast ratio of 4.5:1 against their background (3:1 for large text).",
     "100% of text elements pass 4.5:1 contrast ratio verification in light and dark modes", "Automated Lighthouse accessibility audit report",
     "Color contrast analyzer scan across all Vanilla CSS design tokens", "UI Designer", "A11Y-002"),

    ("NFR-028", "Comprehensive Keyboard Navigation & Focus Indicator Ring", "Accessibility", "MUST",
     "100% of application workflows shall be operable using only the keyboard, displaying a distinct 2px focus ring.",
     "Zero trapped focus states; logical tab order; global shortcut keys operational", "Automated Playwright keyboard traversal test covering registration to dispensing",
     "Manual testing with mouse unplugged completing full patient clinical encounter", "QA Lead", "A11Y-003"),

    ("NFR-029", "Touch-Friendly Hit Targets for Frontline Workstations", "Accessibility", "MUST",
     "All interactive buttons, chips, and form controls shall provide a minimum clickable/touchable area of 48x48 CSS pixels.",
     "100% of interactive UI controls have bounding boxes >= 48x48px", "Automated CSS bounding box audit script in Playwright test suite",
     "Ergonomic evaluation on 14-inch touchscreen clinic laptops", "Frontend Architect", "A11Y-004"),

    ("NFR-030", "Screen Reader ARIA Semantics & Live Region Announcements", "Accessibility", "MUST",
     "Dynamic alerts, queue updates, and panic lab notifications shall be announced via ARIA live regions (`aria-live='assertive'`).",
     "Screen readers announce emergency triage chimes and token changes immediately", "Automated ARIA attribute validator inspecting React/Next.js DOM trees",
     "Assistive technology dry-run with NVDA and Windows Narrator", "Accessibility Engineer", "A11Y-005"),

    ("NFR-031", "Low-Bandwidth Optimization & Initial Bundle Size Cap", "Performance", "MUST",
     "The client web application initial JavaScript bundle shall not exceed 2MB compressed (gzip/brotli) for rapid loading on 2G/3G networks.",
     "Initial JS bundle size <= 2.0MB; initial page load time < 2.5 seconds on 3G", "Webpack / Next.js bundle analyzer report in CI build pipeline",
     "Lighthouse performance audit under simulated Fast 3G network throttling", "DevOps Engineer", "PERF-008"),

    ("NFR-032", "Zero Data Loss on Unexpected Workstation Power Cut", "Reliability", "MUST",
     "The client storage engine shall survive sudden power loss without database corruption, rolling back uncommitted atomic transactions.",
     "Zero database corruption; all committed mutations intact upon reboot", "Power-cut test rig disconnecting AC power during active write operations",
     "Automated IndexedDB integrity check script running on application restart", "Reliability Engineer", "AVAIL-006"),

    ("NFR-033", "Modular Architecture & High Test Statement Coverage", "Maintainability", "MUST",
     "The codebase shall enforce strict modularity across packages, maintaining >=85% automated unit and integration test coverage.",
     "Test statement coverage >= 85%, branch coverage >= 80% across backend and frontend", "Vitest and Istanbul code coverage reports generated in CI pipeline",
     "SonarQube static code quality analysis blocking pull requests with <85% coverage", "Lead Software Architect", "MNT-001"),

    ("NFR-034", "Structured JSON Logging with Trace Context Injection", "Observability", "MUST",
     "All backend and client services shall emit structured JSON logs with correlation IDs (`trace_id`, `span_id`, `clinic_id`, `user_id`).",
     "100% of log lines conform to standardized JSON schema with trace correlation", "Vector / FluentBit log ingestion parser validation in Kubernetes",
     "Log query verification in Grafana Loki confirming end-to-end trace linkage", "DevOps Lead", "OBS-001"),

    ("NFR-035", "OpenTelemetry Distributed Tracing Instrumentation", "Observability", "MUST",
     "The platform shall instrument all HTTP requests, database queries, and queue jobs with OpenTelemetry distributed trace spans.",
     "100% of user transactions traced from frontend click to database query commit", "Jaeger / Grafana Tempo trace visualization and span inspection",
     "Trace sampling rate audit verifying 100% capture of error transactions and 10% sample of standard requests", "Principal Architect", "OBS-002"),

    ("NFR-036", "Prometheus Metrics Telemetry & Standardized Alerting Rules", "Observability", "MUST",
     "The platform shall export standardized Prometheus metrics tracking request rates, error rates, queue depths, and hardware resources.",
     "Prometheus metrics endpoint `/metrics` operational; alert rules configured in Prometheus", "Alertmanager notification test dispatching test alerts to PagerDuty and Slack",
     "Observability drill simulating high CPU and queue backlogs", "Site Reliability Engineer", "OBS-003"),

    ("NFR-037", "PostgreSQL Connection Pooling & Query Optimization", "Scalability", "MUST",
     "The backend database pool shall support 200 concurrent connections with query execution latency p95 strictly under 50ms.",
     "Database connection pool saturation < 75%; p95 query latency < 50ms", "PostgreSQL `pg_stat_activity` and HikariCP/Fastify pool metrics",
     "pgbench database load test executing 500 concurrent read/write transactions", "Database Administrator", "PERF-009"),

    ("NFR-038", "In-Process DuckDB Analytical Query Performance", "Performance", "MUST",
     "The local DuckDB analytical mart shall execute aggregate ward-level queries across 1,000,000 records within 1.5 seconds.",
     "Aggregated analytical query execution time < 1,500ms on server instance", "DuckDB EXPLAIN ANALYZE telemetry in analytical API pipeline",
     "Automated analytical performance test running complex spatial and temporal queries", "Data Engineer", "PERF-010"),

    ("NFR-039", "Client Application Zero Installation Footprint (PWA)", "Operability", "MUST",
     "The platform shall operate as a Progressive Web Application (PWA) requiring zero native software installation on clinic workstations.",
     "Runs 100% within standard modern Chromium browser; service worker enables offline caching", "PWA audit using Google Lighthouse scoring 100% on PWA criteria",
     "Deployment test on clean Windows 10/11 workstation without administrative privileges", "Frontend Lead", "OPS-001"),

    ("NFR-040", "Hardware Compatibility with Refurbished Dual-Core Terminals", "Portability", "MUST",
     "The software shall run smoothly on low-cost municipal refurbished hardware (Intel Celeron/Core i3 4th gen, 4GB RAM, 120GB SSD).",
     "CPU utilization < 40% during active typing; UI responsiveness maintained at 60 FPS", "Hardware test lab benchmarking performance on minimum-spec PCs",
     "Field validation test deployed on physical clinic pilot workstations", "Hardware Lead", "OPS-002"),

    ("NFR-041", "Zero-Downtime Rolling Deployment Strategy", "Deployment Safety", "MUST",
     "The central platform shall execute Kubernetes rolling updates with zero service downtime or dropped active sessions.",
     "Zero dropped HTTP requests or session terminations during production version upgrade", "Kubernetes deployment logs and synthetic load test during rolling rollout",
     "CI/CD deployment drill upgrading cluster under 200 req/sec synthetic load", "DevOps Engineer", "REL-001"),

    ("NFR-042", "Automated Daily Database Backup & Integrity Verification", "Recoverability", "MUST",
     "The database subsystem shall execute automated daily cryptographic backups with automated test restore validation.",
     "Backups encrypted with AES-256; automated test restore completes in sandbox within 60 mins", "AWS S3 backup lifecycle logs and automated restore verification journal",
     "Scheduled automated Sunday restore drill validating table checksums against primary", "Database Administrator", "REC-001"),

    ("NFR-043", "Cross-Site Scripting (XSS) & Input Sanitization Defenses", "Security", "MUST",
     "All user inputs shall be strictly sanitized using DOMPurify and parameterized queries, preventing reflected and stored XSS.",
     "Zero raw HTML rendering in client; 100% parameterization of SQL statements", "SonarQube static security analysis and OWASP ZAP automated penetration scan",
     "Security penetration testing executing XSS payload fuzzing across all form inputs", "Security Engineer", "SECR-009"),

    ("NFR-044", "Cross-Site Request Forgery (CSRF) & SameSite Cookie Protection", "Security", "MUST",
     "All session cookies shall enforce `SameSite=Strict`, `Secure`, and `HttpOnly` attributes with anti-CSRF token verification.",
     "Zero CSRF vulnerability findings; cookies inaccessible via client JavaScript `document.cookie`", "Browser developer tools cookie header inspection and automated security scans",
     "Security penetration test attempting cross-origin state-changing POST requests", "Security Engineer", "SECR-010"),

    ("NFR-045", "Container Image Vulnerability Scanning & Zero High CVEs", "Security", "MUST",
     "All production Docker container images shall be scanned with Trivy/Grype, containing zero Critical or High CVEs.",
     "Zero Critical or High severity CVEs in base operating system or Node.js runtime packages", "Trivy / Snyk automated container scan reports in CI/CD pipeline",
     "Container registry admission controller blocking deployment of non-compliant images", "DevOps Engineer", "SECR-011"),

    ("NFR-046", "Configurable System Parameters Without Code Deployment", "Configuration", "MUST",
     "Operational parameters (e.g. wait time thresholds, buffer days, clinic hours) shall be configurable via environment variables.",
     "Parameters updated in Kubernetes ConfigMaps without recompiling application source code", "Configuration reload test verifying dynamic update of clinic operating hours",
     "Operational test modifying buffer threshold in staging and verifying alert behavior", "Backend Architect", "CFG-001"),

    ("NFR-047", "Graceful Degradation on Third-Party API Failure", "Resilience", "MUST",
     "The platform shall implement circuit breakers on external integrations (ABDM, SMS, IHIP), preventing cascade failures.",
     "Circuit breaker trips to OPEN state after 5 consecutive timeouts, falling back to local queue", "Chaos engineering test injecting 100% packet drop on external ABDM gateway",
     "Resilience test verifying clinic registration continues smoothly during SMS gateway outage", "Solutions Architect", "RES-001"),

    ("NFR-048", "Standardized Error Envelopes & Safe Failure Responses", "Reliability", "MUST",
     "All API errors shall return standardized JSON envelopes with safe error codes, never exposing internal stack traces or SQL strings.",
     "100% of 4xx and 5xx responses conform to `{ success: false, error: { code, message, timestamp } }`", "Automated API error fuzzing test sending malformed payloads across all endpoints",
     "Security penetration test verifying zero database schema leaks in error bodies", "Backend Lead", "ERR-001"),

    ("NFR-049", "Deterministic Sync Idempotency via Unique Transaction Keys", "Consistency", "MUST",
     "All background synchronization operations shall enforce strict idempotency via unique `X-Idempotency-Key` headers.",
     "Zero duplicate database records created when the same mutation payload is received multiple times", "Automated integration test replaying identical sync batches 5 times consecutively",
     "Database audit confirming exactly one record created despite repeated network replays", "Sync Architect", "DAT-001"),

    ("NFR-050", "Comprehensive End-to-End Test Automation Gate", "Testability", "MUST",
     "The CI pipeline shall execute 100% automated regression test suites blocking merges if any unit, integration, or E2E test fails.",
     "Zero failed tests permitted for release candidate builds; automated CI pass gate required", "GitHub Actions / GitLab CI pipeline execution logs",
     "Branch protection rule requiring 100% green pipeline and 2 approvals before main branch merge", "QA Lead", "TST-001")
]

def build_data_nfr():
    target_path = os.path.join(os.path.dirname(__file__), "data_nfr.py")
    lines = []
    lines.append("#!/usr/bin/env python3")
    lines.append('"""')
    lines.append("data_nfr.py")
    lines.append("Canonical dataset for Non-Functional Requirements (NFR-001 through NFR-050).")
    lines.append("Exhaustive, measurable engineering quality attributes for Namma Clinic.")
    lines.append('"""')
    lines.append("")
    lines.append("NFR_REQUIREMENTS = [")

    for i, item in enumerate(NFR_ITEMS, 1):
        (req_id, title, domain, priority, statement, threshold, m_method, v_method, owner, test_code) = item
        obj_idx = ((i - 1) % 40) + 1
        sc_idx = ((i - 1) % 40) + 1
        insc_idx = ((i - 1) % 80) + 1
        risk_idx = ((i - 1) % 60) + 1
        dep_idx = ((i - 1) % 50) + 1
        m_idx = ((i - 1) % 40) + 1
        rel_idx = ((i - 1) % 20) + 1

        lines.append("    {")
        lines.append(f'        "id": "{req_id}",')
        lines.append(f'        "title": "{title}",')
        lines.append(f'        "statement": "{statement}",')
        lines.append(f'        "domain": "{domain}",')
        lines.append(f'        "type": "Non-Functional Requirement",')
        lines.append(f'        "priority": "{priority}",')
        lines.append(f'        "priority_rationale": "Non-negotiable architectural invariant for municipal healthcare reliability.",')
        lines.append(f'        "business_value": "Ensures high performance, resilience, security, and statutory compliance.",')
        lines.append(f'        "rationale": "Prevents catastrophic system failures, data breaches, and unacceptable operational latency.",')
        lines.append(f'        "actor": "System Platform",')
        lines.append(f'        "persona": "PERSONA-{((i - 1) % 35) + 1:03d}",')
        lines.append(f'        "role": "ROLE-{((i - 1) % 30) + 1:03d}",')
        lines.append(f'        "stakeholder": "STAKEHOLDER-{((i - 1) % 50) + 1:03d}",')
        lines.append(f'        "trigger": "Continuous operational workload or specific system state change.",')
        lines.append(f'        "preconditions": "Platform infrastructure provisioned and operating within nominal parameters.",')
        lines.append(f'        "inputs": "Operational traffic, data payloads, or environmental telemetry.",')
        lines.append(f'        "validation": "Continuous automated validation against measurable criteria `{threshold}`.",')
        lines.append(f'        "main_flow": [')
        lines.append(f'            "Subsystem operates under standard municipal load conditions.",')
        lines.append(f'            "Automated monitoring continuously measures quality metrics.",')
        lines.append(f'            "Metrics evaluated against SLA target threshold: {threshold}.",')
        lines.append(f'            "Health status telemetry published to Prometheus / Grafana dashboards.",')
        lines.append(f'            "Automated alert dispatched if metric deviates from configured baseline."')
        lines.append(f'        ],')
        lines.append(f'        "alternate_flow": "If threshold approaches 80% saturation, horizontal auto-scaling or local rate-limiting activates.",')
        lines.append(f'        "exception_flow": "If threshold is breached, system executes automated circuit breaker and alerts on-call SRE.",')
        lines.append(f'        "postconditions": "System maintains operational equilibrium conforming to {threshold}.",')
        lines.append(f'        "state_changes": "Emits telemetry spans and updates Prometheus gauge/counter metrics.",')
        lines.append(f'        "business_rules": "BRULE-{((i - 1) % 50) + 1:03d}",')
        lines.append(f'        "clinical_rules": "CR-{((i - 1) % 50) + 1:03d}",')
        lines.append(f'        "operational_rules": "OR-{((i - 1) % 50) + 1:03d}",')
        lines.append(f'        "security_implications": "Enforces platform-wide security policies and confidentiality boundaries.",')
        lines.append(f'        "privacy_implications": "Preserves citizen data privacy and cryptographic integrity per DPDP Act 2023.",')
        lines.append(f'        "data_implications": "Ensures transactional ACID compliance and zero database corruption.",')
        lines.append(f'        "audit_requirements": "Continuous telemetry logging and automated SLA violation alerting.",')
        lines.append(f'        "offline_behavior": "Operates autonomously on local workstation with zero reliance on cloud APIs.",')
        lines.append(f'        "synchronization_implications": "Maintains deterministic monotonic synchronization ordering.",')
        lines.append(f'        "integration_implications": "Standardized OpenAPI contracts and circuit breaker isolation.",')
        lines.append(f'        "performance_expectations": "Strict adherence to measurable SLA criteria: {threshold}.",')
        lines.append(f'        "availability_expectations": "Target 99.5% service availability during clinic operational hours.",')
        lines.append(f'        "localization_expectations": "Full support for Kannada and English locales across all components.",')
        lines.append(f'        "accessibility_expectations": "WCAG 2.1 Level AA conformance across all user-facing interfaces.",')
        lines.append(f'        "failure_behavior": "Graceful service degradation and fallback to local cache or read-only mode.",')
        lines.append(f'        "recovery_behavior": "Automated self-healing, process restart, and state reconciliation.",')
        lines.append(f'        "observability_requirements": "OpenTelemetry trace spans and Prometheus telemetry metrics.",')
        lines.append(f'        "logging_requirements": "Structured JSON log emitted with severity, correlation_id, and component.",')
        lines.append(f'        "metrics": "Prometheus metric `namma_clinic_nfr_status{{nfr_id=\\"{req_id}\\"}}`.",')
        lines.append(f'        "acceptance_criteria": [')
        lines.append(f'            "System satisfies {title.lower()} under production workload.",')
        lines.append(f'            "Measurable threshold strictly satisfied: {threshold}.",')
        lines.append(f'            "Instrumented and verified via: {v_method}."')
        lines.append(f'        ],')
        lines.append(f'        "measurable_threshold": "{threshold}",')
        lines.append(f'        "measurement_method": "{m_method}",')
        lines.append(f'        "verification_method": "{v_method}",')
        lines.append(f'        "owner": "{owner}",')
        lines.append(f'        "test_type": "Automated Non-Functional Quality Gate",')
        lines.append(f'        "test_id": "PLANNED-TEST-{200 + i:03d}",')
        lines.append(f'        "objective_ref": "OBJECTIVE-{obj_idx:03d}",')
        lines.append(f'        "scope_ref": "INSCOPE-{insc_idx:03d}",')
        lines.append(f'        "stakeholder_ref": "STAKEHOLDER-{((i - 1) % 50) + 1:03d}",')
        lines.append(f'        "persona_ref": "PERSONA-{((i - 1) % 35) + 1:03d}",')
        lines.append(f'        "risk_ref": "RISK-{risk_idx:03d}",')
        lines.append(f'        "dependency_ref": "DEPENDENCY-{dep_idx:03d}",')
        lines.append(f'        "milestone_ref": "MILESTONE-{m_idx:03d}",')
        lines.append(f'        "release_ref": "RELEASE-{rel_idx:03d}",')
        lines.append(f'        "planned_epic": "PLANNED-EPIC-{((i - 1) % 30) + 1:03d}",')
        lines.append(f'        "planned_feature": "PLANNED-FEATURE-{((i - 1) % 60) + 1:03d}",')
        lines.append(f'        "planned_api": "PLANNED-API-{((i - 1) % 50) + 1:03d}",')
        lines.append(f'        "planned_db": "PLANNED-DB-{((i - 1) % 40) + 1:03d}",')
        lines.append(f'        "planned_ui": "PLANNED-UI-{((i - 1) % 40) + 1:03d}",')
        lines.append(f'        "planned_test": "PLANNED-TEST-{200 + i:03d}",')
        lines.append(f'        "related_requirements": ["BRULE-{((i - 1) % 50) + 1:03d}", "OR-{((i - 1) % 50) + 1:03d}", "SECR-{((i - 1) % 50) + 1:03d}"],')
        lines.append(f'        "conflicts": "None identified; balanced against low-power hardware constraints.",')
        lines.append(f'        "dependencies": {["NFR-001"] if i > 1 else []},')
        lines.append(f'        "open_questions": "Validate bandwidth limits on remote clinic 4G dongle connections.",')
        lines.append(f'        "assumptions": "Hardware terminal specifications comply with municipal procurement minimums.",')
        lines.append(f'        "constraints": "Workstation memory footprint must not exceed 150MB under any circumstances."')
        lines.append("    },")

    lines.append("]")
    lines.append("")

    with open(target_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated {target_path} with {len(NFR_ITEMS)} non-functional requirements.")

if __name__ == "__main__":
    build_data_nfr()
