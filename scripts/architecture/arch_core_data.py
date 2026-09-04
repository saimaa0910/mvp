"""
arch_core_data.py
Master Architectural Dataset for Phase 06 Solution Architecture.

Contains canonical, structured technical specifications for:
- 18 System Containers (ARCH-CONT-001 to ARCH-CONT-018)
- 54 Components (ARCH-COMP-001 to ARCH-COMP-054)
- 30 Data Entities (ARCH-DATA-001 to ARCH-DATA-030)
- 30 Security Controls (ARCH-SEC-001 to ARCH-SEC-030)
- 20 Integration Connectors (ARCH-INT-001 to ARCH-INT-020)
- 18 Offline Handlers (ARCH-OFF-001 to ARCH-OFF-018)
- 15 Analytics Indicators (ARCH-ANL-001 to ARCH-ANL-015)
- 12 Advisory AI Models (ARCH-AI-001 to ARCH-AI-012)
- 20 Observability Spans (ARCH-OBS-001 to ARCH-OBS-020)
- 15 Disaster Recovery Runbooks (ARCH-DR-001 to ARCH-DR-015)
- 12 Scalability Dimensions (ARCH-SCALE-001 to ARCH-SCALE-012)
- 12 Deployment Topologies (ARCH-DEPLOY-001 to ARCH-DEPLOY-012)
- 8 Environment Specifications (ARCH-ENV-001 to ARCH-ENV-008)
- 45 Architecture Decision Records (ADR-001 to ADR-045)
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# -------------------------------------------------------------
# 1. 18 Architecture Containers (C4 Level 2)
# -------------------------------------------------------------
CONTAINERS_DATA = [
    ("ARCH-CONT-001", "Clinic Workstation PWA Shell", "Frontend Client", "Next.js / TypeScript / React / TailwindCSS", "Provides responsive touch-first workstation interface for doctors, nurses, pharmacists, and lab techs with offline caching and hardware scanner/printer access.", "Local Workstation / Tablet", "IndexedDB / SQLite Edge", "MODULE-001..026"),
    ("ARCH-CONT-002", "Clinic Edge Mini-Server Runtime", "Edge Computing Node", "Node.js / Express / Bun / SQLite WAL", "Hosts local clinic database, MQTT queue broker, and vector clock sync engine, ensuring 72h autonomous operation.", "Clinic Edge Appliance (Intel N100)", "SQLite WAL Mode (Local SSD)", "MODULE-027, MODULE-028"),
    ("ARCH-CONT-003", "Central Cloud API Gateway", "Ingress & Routing", "Envoy / NGINX / Kong", "Handles TLS termination, rate limiting, JWT token validation, mTLS routing, and request correlation tracing.", "Cloud Ingress Tier", "Redis Token Cache", "MODULE-001, MODULE-005"),
    ("ARCH-CONT-004", "Identity & Access Management (IAM) Service", "Security & Auth", "Node.js / Passport / Argon2id / JOSE", "Issues and verifies cryptographic staff JWT tokens, manages RBAC/ABAC role permissions, and coordinates session invalidation.", "Cloud App Tier / Edge Mirror", "PostgreSQL `auth_users`", "MODULE-001, MODULE-005"),
    ("ARCH-CONT-005", "Master Patient Index (MPI) Service", "Patient Domain", "NestJS / Fastify / TypeScript", "Manages citizen demographic profiles, phonetic fuzzy search, deduplication logic, and ABHA national ID bindings.", "Cloud App Tier / Edge Sync", "PostgreSQL `patients`", "MODULE-007, MODULE-008"),
    ("ARCH-CONT-006", "Queue Orchestration & Triage Engine", "Workflow Domain", "Go / MQTT / WebSockets", "Maintains multi-room priority queues, calculates MEWS vitals scores, and broadcasts token calls to waiting hall TVs.", "Edge Mini-Server / Cloud Sync", "Edge SQLite `clinic_queues`", "MODULE-009, MODULE-010, MODULE-011"),
    ("ARCH-CONT-007", "Clinical Consultation & EMR Service", "Clinical Domain", "NestJS / Prisma / TypeScript", "Captures SOAP clinical progress notes, SNOMED CT / ICD-10 diagnostic coding, and longitudinal medical history.", "Cloud App Tier / Edge Sync", "PostgreSQL `clinical_encounters`", "MODULE-013, MODULE-014"),
    ("ARCH-CONT-008", "Electronic Prescription & CDSS Service", "Clinical Domain", "NestJS / Rule Engine / TypeScript", "Enforces formulary rules, evaluates drug-drug interactions, checks pediatric dosage boundaries, and signs e-prescriptions.", "Cloud App Tier / Edge Sync", "PostgreSQL `prescriptions`", "MODULE-014, MODULE-015"),
    ("ARCH-CONT-009", "Pharmacy Inventory & Dispensation Service", "Logistics Domain", "NestJS / TypeScript", "Enforces FEFO batch allocation, verifies 2D DataMatrix scans, tracks cold-chain storage, and manages depot indenting.", "Cloud App Tier / Edge Sync", "PostgreSQL `pharmacy_batches`", "MODULE-019..022"),
    ("ARCH-CONT-010", "Diagnostic Laboratory Service", "Diagnostics Domain", "NestJS / TypeScript", "Manages test orders for 58 rapid diagnostic tests, specimen chain-of-custody, and critical panic value escalations.", "Cloud App Tier / Edge Sync", "PostgreSQL `lab_orders`", "MODULE-016"),
    ("ARCH-CONT-011", "Referral & EMS Telemetry Bridge", "Care Continuity", "NestJS / REST Gateway", "Assembles clinical referral dossiers, coordinates 108 ambulance dispatch, and tracks secondary hospital counter-referrals.", "Cloud App Tier", "PostgreSQL `referrals`", "MODULE-017"),
    ("ARCH-CONT-012", "Citizen Portal & Multilingual Notification Service", "Citizen Domain", "Node.js / BullMQ / Redis", "Dispatches bilingual SMS/WhatsApp appointment reminders, recall notices, and operates self-service kiosk tokens.", "Cloud App Tier", "Redis Queue / PostgreSQL", "MODULE-023, MODULE-024"),
    ("ARCH-CONT-013", "Bi-directional Edge-Cloud Synchronization Service", "Sync Engine", "Go / gRPC / Vector Clocks", "Executes asynchronous delta synchronization, CRDT conflict resolution, and bandwidth-throttled replay.", "Edge Node & Cloud Worker", "SQLite Mutation Log", "MODULE-028"),
    ("ARCH-CONT-014", "ABDM & National Health Grid Bridge", "Interoperability", "Java / Spring Boot / HAPI FHIR", "Transforms clinical records into FHIR R4 bundles for ABDM M1 (ABHA), M2 (HIP Publishing), and M3 (HIU Consent).", "Cloud DMZ Tier", "PostgreSQL `abdm_artifacts`", "MODULE-029"),
    ("ARCH-CONT-015", "Public Health Analytics & Syndromic BI Service", "Analytics Domain", "Python / ClickHouse / Apache Superset", "Aggregates ward-level disease prevalence, stock burn-down, and syndromic fever surveillance for municipal officers.", "Cloud Analytics Tier", "ClickHouse Star Schema", "MODULE-030"),
    ("ARCH-CONT-016", "Advisory Clinical AI Decision Support Engine", "AI / ML Tier", "Python / FastAPI / ONNX Runtime", "Provides advisory syndromic clustering alerts and non-autonomous medication interaction predictions.", "Cloud Analytics Tier", "Model Registry (MLflow)", "MODULE-015, MODULE-030"),
    ("ARCH-CONT-017", "Cryptographic WORM Audit Service", "Audit & Security", "Go / SHA-256 HMAC / Logstash", "Maintains an immutable append-only audit trail with cryptographic hash chaining conforming to DPDP Act 2023.", "Isolated Cloud Security Subnet", "Encrypted Object Store", "MODULE-004, MODULE-005"),
    ("ARCH-CONT-018", "Enterprise Relational Database Cluster", "Data Tier", "PostgreSQL 16 Multi-AZ with Patroni", "Authoritative central transactional database with streaming physical replication and table partitioning.", "Private Cloud Database Subnet", "NVMe SSD SAN Storage", "ALL MODULES")
]

CONTAINERS = [
    {
        "id": c[0],
        "name": c[1],
        "category": c[2],
        "tech": c[3],
        "description": c[4],
        "deployment": c[5],
        "datastore": c[6],
        "modules": c[7]
    }
    for c in CONTAINERS_DATA
]

CONTAINER_MAP = {c["id"]: c for c in CONTAINERS}

# -------------------------------------------------------------
# 2. 54 Architecture Components (C4 Level 3)
# -------------------------------------------------------------
COMPONENTS = []
for c_idx, cont in enumerate(CONTAINERS, start=1):
    for sub_idx in range(1, 4):
        comp_num = (c_idx - 1) * 3 + sub_idx
        comp_id = f"ARCH-COMP-{comp_num:03d}"
        role_type = ["Controller & Ingress Handler", "Domain Business Logic Service", "Persistence & Integration Adapter"][sub_idx - 1]
        COMPONENTS.append({
            "id": comp_id,
            "container_id": cont["id"],
            "container_name": cont["name"],
            "name": f"{cont['name']} {role_type}",
            "purpose": f"Executes dedicated {role_type.lower()} responsibilities within {cont['name']}.",
            "responsibilities": [
                f"Validates inbound data contracts and enforces permission checks for {cont['name']}.",
                f"Executes core domain invariants and state transitions conforming to {cont['modules']}.",
                f"Coordinates atomic transactional persistence and emits OpenTelemetry spans."
            ],
            "interfaces": [
                f"gRPC / REST endpoint for {cont['name']}",
                f"Internal domain event publisher on message bus"
            ],
            "dependencies": [f"ARCH-CONT-{(c_idx % 18) + 1:03d}"],
            "security": "Enforces TLS 1.3, JWT bearer token claims, and role-based access invariants.",
            "telemetry": f"Emits Prometheus metric `{cont['name'].lower().replace(' ', '_')}_{role_type.lower().replace(' ', '_')}_seconds`.",
            "testing": "Unit tests with Jest/Go testing + Contract verification tests with Pact."
        })

COMP_MAP = {c["id"]: c for c in COMPONENTS}

# -------------------------------------------------------------
# 3. 45 Architecture Decision Records (ADR-001 to ADR-045)
# -------------------------------------------------------------
ADR_DATA = [
    (1, "Adoption of Modular Monolith Backend with Edge Autonomy", "APPROVED", "Architecture Style",
     "The system must support 183 clinics with high reliability, but distributed microservices would introduce excessive network failure modes at the edge.",
     ["Microservices Architecture (20+ services)", "Traditional Monolith", "Modular Monolith with Embedded Edge Engines"],
     "Adopt a Modular Monolith architecture for central cloud with compiled lightweight edge daemons.",
     "Provides strict domain boundary isolation without the operational latency and network failure modes of microservices.",
     ["Low operational complexity", "Fast in-process calls", "Requires discipline to prevent boundary leaks"]),

    (2, "Offline-First Local Persistence with SQLite WAL and Vector Clocks", "APPROVED", "Persistence Strategy",
     "Municipal optical fiber links in urban clinics experience frequent outages (10-15% monthly downtime).",
     ["Cloud-Only Browser Web App", "IndexedDB Client-Only Storage", "Edge Mini-Server with SQLite Write-Ahead Logging (WAL) and Vector Clocks"],
     "Deploy physical edge mini-servers running SQLite in WAL mode synchronized via vector clocks.",
     "Guarantees 72-hour autonomous operation across multiple clinic workstations even during complete WAN disconnection.",
     ["Uninterrupted clinic workflow", "Requires conflict resolution engine", "Local hardware appliance maintenance"]),

    (3, "Progressive Web Application (PWA) Client Architecture", "APPROVED", "Frontend Architecture",
     "Clinic workstations include touch laptops, tablets, and desktop terminals running diverse operating systems.",
     ["Native Windows/Android Apps", "Standard Web Application", "Progressive Web App (PWA) with Service Worker"],
     "Build a responsive PWA using Next.js, React, and TypeScript with Service Worker asset caching.",
     "Enables single codebase across all devices, touch ergonomics, and instant client-side offline launch.",
     ["Universal device compatibility", "Zero manual install updates", "Browser storage quota management"]),

    (4, "Adoption of UUIDv7 for Distributed Entity Identifiers", "APPROVED", "Data Architecture",
     "Entities generated across 183 offline edge nodes must merge into central PostgreSQL without primary key collisions.",
     ["Auto-incrementing Integer IDs", "Random UUIDv4", "Time-ordered UUIDv7"],
     "Adopt UUIDv7 as the universal primary key format across all relational tables.",
     "Combines millisecond Unix timestamp with cryptographically random bits, preserving B-tree indexing performance while preventing merge conflicts.",
     ["Zero key collisions during sync", "Optimized index locality", "Slightly larger storage footprint than 4-byte integers"]),

    (5, "Argon2id Salted Credentials with Rotating JWT Session Tokens", "APPROVED", "Security Architecture",
     "Healthcare workers require secure authentication that withstands offline credential verification and network eavesdropping.",
     ["Plain Session Cookies", "Basic Auth", "Argon2id Hashing with Short-Lived JWTs (15 min) and Refresh Tokens"],
     "Implement Argon2id password hashing with cryptographically signed RS256 JWT tokens.",
     "Protects against offline brute-force attacks and limits blast radius of stolen tokens to 15 minutes.",
     ["High cryptographic security", "CPU intensive during login hashing", "Requires secure client token storage"]),

    (6, "ABDM Milestone 1, 2, and 3 FHIR R4 Integration Standard", "APPROVED", "Interoperability",
     "The National Health Authority (NHA) mandates ABDM compliance for public health software.",
     ["Custom Proprietary Health API", "HL7 v2 Message Stream", "HAPI FHIR R4 Compliant Bundles"],
     "Adopt FHIR R4 clinical resources (Patient, Encounter, Condition, MedicationRequest, Observation) via Spring Boot gateway.",
     "Satisfies national compliance standards and enables seamless longitudinal health record portability.",
     ["Full national compliance", "Complex FHIR data transformations", "Schema validation overhead"]),

    (7, "First-Expiry-First-Out (FEFO) Inventory Allocation Engine", "APPROVED", "Pharmacy Logistics",
     "Expired pharmaceutical stock represents financial waste and severe patient safety risk.",
     ["First-In-First-Out (FIFO)", "Last-In-First-Out (LIFO)", "First-Expiry-First-Out (FEFO) with 2D Barcode Verification"],
     "Enforce strict FEFO allocation during electronic prescription dispensation.",
     "Ensures batches nearest to expiry date are dispensed first, reducing clinic drug waste by > 80%.",
     ["Mitigates expired drug dispensation", "Requires discipline during physical stock loading", "Barcode scanning mandatory"]),

    (8, "Strict Advisory Boundary for Clinical AI & Decision Support", "APPROVED", "AI & Clinical Safety",
     "AI diagnostic tools can suffer from hallucinations, bias, and legal liability in public healthcare.",
     ["Autonomous AI Diagnosis", "Unchecked AI Prescribing", "Strictly Advisory AI Decision Support with Human Physician Override"],
     "Enforce advisory-only clinical decision support; human Medical Officer holds sole statutory authority.",
     "Eliminates algorithmic diagnostic risk and preserves physician clinical autonomy and accountability.",
     ["High patient safety", "Zero regulatory liability for AI", "Physicians can dismiss advisory alerts"]),

    (9, "WORM Immutable Audit Ledger with Cryptographic Hash-Chaining", "APPROVED", "Audit & Compliance",
     "Statutory regulations (DPDP Act, EHR Standards) require non-repudiable logs of all health record modifications.",
     ["Standard Application Database Table", "Logstash Flat Files", "Write-Once-Read-Many (WORM) Ledger with SHA-256 Hash Chaining"],
     "Implement an append-only audit ledger with cryptographic SHA-256 hash chains linking each event to the previous record.",
     "Guarantees that log tampering or deletion is mathematically detectable by external regulatory auditors.",
     ["Tamper-proof compliance", "Storage growth over time", "Requires periodic archival to cold storage"]),

    (10, "Dual-Language Kannada and English Native Interface", "APPROVED", "Localization",
     "Frontline staff and citizens in Bengaluru require vernacular language support alongside clinical English.",
     ["English-Only UI", "Machine Translation on the Fly", "Curated Bilingual Dictionary in Kannada (kn-IN) and English (en-IN)"],
     "Implement static compile-time i18n dictionaries in UTF-8 native Kannada script.",
     "Ensures accurate medical translations and high usability for vernacular nursing and community staff.",
     ["High local adoption", "Zero translation latency", "Requires linguistic curation for new terms"]),

    (11, "PostgreSQL 16 Multi-AZ Cluster with Streaming Replication", "APPROVED", "Data Architecture",
     "Central cloud database requires ACID compliance, high concurrent throughput, and zero data loss.",
     ["MongoDB NoSQL", "MySQL InnoDB", "PostgreSQL 16 Multi-AZ with Patroni HA"],
     "Deploy PostgreSQL 16 with streaming physical replication across 3 availability zones.",
     "Delivers battle-tested ACID transactions, JSONB support for clinical attributes, and sub-second failover.",
     ["High data reliability", "Complex multi-AZ setup", "Requires dedicated DBA monitoring"]),

    (12, "MQTT Broker for Waiting Hall TV and Real-Time Event Bus", "APPROVED", "Messaging Architecture",
     "Queue updates and danger alerts must broadcast instantly to TV screens and workstations without polling.",
     ["HTTP Polling (every 5 seconds)", "Server-Sent Events (SSE)", "Local MQTT Broker (Mosquitto/EMQX) on Edge Mini-Server"],
     "Deploy local lightweight MQTT broker on clinic edge appliance for sub-50ms queue broadcasts.",
     "Eliminates network overhead of polling and functions seamlessly during WAN disconnections.",
     ["Near-zero latency broadcasts", "Low CPU utilization", "Requires MQTT client library on frontend"]),

    (13, "OpenTelemetry Semantic Conventions for Distributed Tracing", "APPROVED", "Observability",
     "Troubleshooting edge-to-cloud synchronization and latency bottlenecks requires end-to-end tracing.",
     ["Custom Application Logging", "Zipkin Tracing", "OpenTelemetry (OTel) with W3C TraceContext Propagation"],
     "Adopt OpenTelemetry standards across frontend, edge mini-servers, and cloud microservices.",
     "Provides vendor-neutral telemetry data compatible with Prometheus, Jaeger, and Grafana.",
     ["Standardized observability", "Tracing context overhead", "Requires sampling tuning at high scale"]),

    (14, "Bi-directional Conflict-Free Replicated Data Types (CRDT)", "APPROVED", "Sync Strategy",
     "Simultaneous edits on patient profiles across disconnected edge and cloud can cause data conflicts.",
     ["Last-Write-Wins (Timestamp Based)", "Manual Operator Reconciliation", "State-based CRDTs with Field-Level Vector Clocks"],
     "Utilize deterministic CRDT register semantics for non-overlapping patient profile attributes.",
     "Allows safe, automated resolution of 95%+ of sync collisions without user intervention.",
     ["Automated conflict resolution", "Consistent final state", "Requires complex register data structures"]),

    (15, "Zero-Plaintext PHI Logging with Automated PII Scrubber", "APPROVED", "Privacy Engineering",
     "Accidental leakage of patient names or Aadhaar numbers into logging systems breaches DPDP Act 2023.",
     ["Manual Developer Review", "Post-hoc Log Masking", "Compile-Time and Middleware PII Scrubber Filtering"],
     "Implement automated middleware regex scrubbers that redact names, phones, and IDs before emission.",
     "Guarantees that log aggregators and observability tools never receive plaintext sensitive health data.",
     ["Strict DPDP compliance", "Minimal CPU parsing cost", "Requires maintenance of redaction patterns"]),

    (16, "Hardware Thermal Printer Direct ESC/POS Driver Integration", "APPROVED", "Peripherals Architecture",
     "Standard browser print dialogs require 3 user clicks and format poorly on 80mm thermal receipt rolls.",
     ["Browser Print Dialog (Ctrl+P)", "Generic Windows Spooler", "Direct ESC/POS Command Generation via Web Serial / Network Raw Socket"],
     "Generate raw ESC/POS binary command streams delivered directly to receipt printers.",
     "Allows 1-click sub-second receipt printing with crisp 2D QR codes and bilingual Kannada fonts.",
     ["Sub-second print speed", "Perfect receipt formatting", "Requires raw socket / USB serial permission"]),

    (17, "2D DataMatrix Handheld Barcode Scanner USB HID Keyboard Emulation", "APPROVED", "Peripherals Architecture",
     "Pharmacists must scan pharmaceutical strips rapidly without complex driver installation.",
     ["Webcam QR Scanner", "Proprietary Scanner SDKs", "USB HID Keyboard Wedge Mode with Hardware Suffix Terminator"],
     "Standardize on plug-and-play USB HID 2D DataMatrix scanners configured with Enter key suffixes.",
     "Zero driver installation required; compatible with all workstation tablets and laptops.",
     ["Universal compatibility", "Instant scanning velocity", "Requires input focus management on UI"]),

    (18, "ClickHouse Columnar Storage for Public Health Epidemiological BI", "APPROVED", "Analytics Architecture",
     "Running complex analytical queries on operational PostgreSQL degrades clinical transaction speeds.",
     ["Run Analytics on PostgreSQL Replicas", "Elasticsearch Analytics", "Dedicated ClickHouse Columnar Database with Debezium CDC"],
     "Stream operational change data capture (CDC) events via Kafka into ClickHouse.",
     "Delivers 100x faster aggregation for syndromic fever surveillance and stock burn-down dashboards.",
     ["Zero impact on clinical OLTP", "Sub-second analytical queries", "Requires CDC pipeline management"]),

    (19, "Line-Interactive UPS with LiFePO4 Battery for 4-Hour Autonomy", "APPROVED", "Hardware Infrastructure",
     "Urban primary clinics suffer intermittent power grid load-shedding and voltage spikes.",
     ["Standard Consumer Inverter", "Diesel Generator Backup", "1.5 kVA Line-Interactive UPS with LiFePO4 External Battery Pack"],
     "Standardize clinic power backup on 1.5 kVA UPS providing minimum 4 hours runtime for edge mini-server.",
     "Guarantees edge computing and Wi-Fi network remain active throughout municipal power outages.",
     ["High battery cycle life", "Zero grid cutover dropouts", "Requires physical battery ventilation"]),

    (20, "Role-Based Dynamic Menu and Capability Toggles", "APPROVED", "Frontend Security",
     "Staff members should only see UI navigation elements and actions authorized for their role.",
     ["Separate Frontend Apps per Role", "Client-Side Hide Only", "Cryptographic Claim-Based Dynamic Menu Rendering with Backend Enforcement"],
     "Evaluate JWT role claims in frontend shell to conditionally render navigation, backed by API guards.",
     "Prevents accidental user confusion while maintaining strict security barriers across roles.",
     ["Intuitive user experience", "Enforces least privilege", "Requires sync between frontend and API roles"]),

    (21, "Standard Treatment Guidelines (STG) Rapid Order Bundles", "APPROVED", "Clinical Workflow",
     "Doctors spend excessive time searching individual drugs for routine ailments (e.g. URI, Gastroenteritis).",
     ["Manual Individual Drug Search", "Unstructured Free Text", "Pre-Configured Coded STG Order Sets with 1-Click Loading"],
     "Provide pre-configured, evidence-based STG order sets for top 20 primary outpatient conditions.",
     "Reduces doctor prescribing time from 60 seconds to 12 seconds while enforcing clinical guidelines.",
     ["Dramatically faster consultation", "Standardizes primary care", "Requires clinical board approval"]),

    (22, "Multi-Tier Rate Limiting with Redis Token Bucket Algorithm", "APPROVED", "API Gateway Security",
     "Public integration gateways are vulnerable to DDoS attacks and misconfigured client retry storms.",
     ["No Rate Limiting", "Fixed Window Limiter", "Distributed Redis Token Bucket Limiter (Tiered by Client Trust)"],
     "Implement Redis token bucket rate limiting on the Envoy/Kong API gateway.",
     "Protects backend infrastructure from volumetric abuse and ensures fair resource distribution.",
     ["Prevents service denial", "Smooth traffic bursts", "Requires Redis operational availability"]),

    (23, "Content Security Policy (CSP) Level 3 and SameSite Strict Cookies", "APPROVED", "Frontend Security",
     "Web applications handling sensitive health records must defend against XSS, clickjacking, and CSRF.",
     ["Relaxed Web Headers", "Basic CORS Headers", "Strict CSP Level 3, HSTS, X-Frame-Options DENY, SameSite=Strict Cookies"],
     "Configure hardened HTTP response headers across all frontend web servers.",
     "Completely prevents execution of unauthorized third-party scripts and cross-site request forgery.",
     ["High frontend security", "Mitigates XSS and CSRF", "Requires inline script nonce management"]),

    (24, "Automated Continuous Integration Vulnerability Gating (Trivy & Snyk)", "APPROVED", "DevSecOps",
     "Dependencies and base container images can introduce critical vulnerabilities into production.",
     ["Manual Security Review", "Periodic Annual Pen-Testing", "Automated CI Pipeline Gating with Trivy and Snyk Scan"],
     "Integrate automated vulnerability scanners into GitHub Actions; block builds with High/Critical CVEs.",
     "Ensures zero known vulnerabilities enter deployment artifacts before reaching clinic servers.",
     ["Proactive vulnerability defense", "Automated enforcement", "Occasional build blocks during zero-day patches"]),

    (25, "Dual-SIM 4G/5G Cellular Gateway Failover Architecture", "APPROVED", "Telecommunications",
     "Single telecom provider connections frequently fail due to physical roadworks and fiber cuts.",
     ["Single Fiber Broadband Connection", "Manual Mobile Hotspot", "Dual-SIM Enterprise Cellular Router with Automatic WAN Health Failover"],
     "Deploy enterprise cellular routers equipped with Airtel and Jio SIM cards configured for failover.",
     "Ensures sub-5-second automatic link failover whenever primary broadband connection drops.",
     ["99.9% network link resilience", "Seamless failover", "Requires monthly dual-data plan maintenance"]),

    (26, "SNOMED CT Clinical Concept and ICD-10 Diagnostic Dual Coding", "APPROVED", "Clinical Terminology",
     "National reporting requires ICD-10 codes, while granular clinical decision support demands SNOMED CT.",
     ["ICD-10 Only", "Free Text Diagnosis", "Dual-Coding Architecture Mapping SNOMED CT Concepts to ICD-10 Codes"],
     "Embed pre-mapped dual coding dictionary in consultation search interface.",
     "Delivers granular clinical meaning for CDSS while fulfilling statutory epidemiological reporting needs.",
     ["International interoperability", "Zero duplicate coding effort", "Dictionary updates require curation"]),

    (27, "Modified Early Warning Score (MEWS) Automated Calculation", "APPROVED", "Clinical Triage",
     "Subjective visual triage by nurses frequently misses occult physiological deterioration.",
     ["Unstructured Nurse Notes", "Triage Color Tags Only", "Standardized MEWS Calculator with Visual/Audible Escalation Alarms"],
     "Embed automated MEWS logic directly in triage vital signs capture screen.",
     "Objectively detects sepsis and respiratory failure, escalating critical patients ahead of routine queues.",
     ["Saves lives through early detection", "Eliminates triage bias", "Requires accurate vital signs entry"]),

    (28, "Central Drug Warehouse (KDLWS) Indent Electronic Data Interchange", "APPROVED", "Supply Chain",
     "Manual paper indents for medication replenishment lead to frequent clinic stockouts.",
     ["Paper Requisitions", "Email PDF Indents", "Direct REST/EDI Protocol with State Central Drug Warehouse"],
     "Automate monthly indent generation based on calculated stock burn-down and reorder levels (ROL).",
     "Prevents stockouts of life-saving antibiotics, insulin, and antihypertensive medications.",
     ["Data-driven replenishment", "Eliminates stockout gaps", "Requires state warehouse API readiness"]),

    (29, "Cold-Chain IoT Sensor Integration and Thermal Breach Invalidation", "APPROVED", "Vaccine Logistics",
     "Vaccines exposed to temperature excursions lose clinical viability and endanger pediatric patients.",
     ["Manual Twice-Daily Paper Log", "Passive Thermometer Checks", "Bluetooth Low Energy (BLE) Temperature Loggers with Automated Batch Lock"],
     "Deploy BLE temperature sensors inside vaccine refrigerators that trigger automated batch locks on breach.",
     "Guarantees that heat-damaged vaccines can never be dispensed or administered to infants.",
     ["Prevents spoiled vaccine delivery", "Statutory cold-chain compliance", "Requires periodic sensor battery replacement"]),

    (30, "Automated SMS and WhatsApp Citizen Recall Notifications", "APPROVED", "Citizen Engagement",
     "Chronic disease patients have high dropout rates when relying solely on physical memory.",
     ["No Follow-up Outreach", "Manual Phone Calls by Nurse", "Automated Multi-Channel SMS and WhatsApp Notification Gateway"],
     "Schedule automated bilingual reminders at T-3 days prior to scheduled NCD return visits.",
     "Improves chronic patient follow-up compliance from 45% to > 80% across municipal wards.",
     ["High citizen attendance", "Reduces nurse administrative load", "Telecom SMS delivery fees"]),

    (31, "Kubernetes (K8s) Cloud Orchestration with Horizontal Pod Autoscaling", "APPROVED", "Cloud Infrastructure",
     "Central cloud platform experiences massive traffic surges during morning clinic opening hours (08:30–11:00).",
     ["Single Virtual Machine", "Static VM Cluster", "Managed Kubernetes with Horizontal Pod Autoscaler (HPA)"],
     "Deploy central backend microservices on Kubernetes with automated CPU/memory-based pod autoscaling.",
     "Maintains sub-200ms response times during morning rush while scaling down during night hours to save cost.",
     ["High cloud elasticity", "Cost-efficient scaling", "Requires Kubernetes operational expertise"]),

    (32, "Redis Clustered Caching for Master Data and Formulary Dictionaries", "APPROVED", "Performance Architecture",
     "Repeatedly querying PostgreSQL for static drug formularies and diagnostic dictionaries wastes database IO.",
     ["Direct Database Queries", "In-Memory Client Cache Only", "Redis Distributed Cache with Automated Invalidation"],
     "Cache essential medicines formulary, SNOMED codes, and clinic rosters in Redis with 1-hour TTL.",
     "Reduces database read load by > 65% and drops dictionary autocomplete latency to < 10ms.",
     ["Ultra-fast query responses", "Saves database IOPS", "Requires cache invalidation on master updates"]),

    (33, "Asynchronous Background Job Processing with BullMQ and Redis", "APPROVED", "Application Architecture",
     "Long-running tasks like SMS dispatch, report generation, and ABDM exports block HTTP request threads.",
     ["Synchronous Execution in HTTP Request", "Cron Scripts", "BullMQ Asynchronous Job Queues with Exponential Backoff"],
     "Offload all non-interactive tasks to background worker processes managed via BullMQ.",
     "Keeps frontline UI response times fast while guaranteeing eventual execution of background tasks.",
     ["Responsive interactive UI", "Automatic retry on external failure", "Requires queue monitoring"]),

    (34, "Client-Side Form State Management with Zustand and React Hook Form", "APPROVED", "Frontend Architecture",
     "Complex clinical forms with dozens of fields cause slow re-renders on low-spec clinic tablets.",
     ["React Context API", "Redux Toolkit", "Zustand with Uncontrolled Inputs via React Hook Form"],
     "Use Zustand for lightweight client state paired with uncontrolled inputs in React Hook Form.",
     "Delivers 60 FPS input performance and prevents typing lag on budget tablets.",
     ["Butter-smooth typing feel", "Minimal bundle size", "Requires discipline with component boundaries"]),

    (35, "Standardized Problem Details (RFC 7807) for API Error Responses", "APPROVED", "API Standards",
     "Inconsistent error responses across backend services complicate frontend error handling and debugging.",
     ["Custom Error JSON Formats", "Plain Text Error Strings", "RFC 7807 Standardized Problem Details JSON"],
     "Enforce RFC 7807 Problem Details schema across all REST endpoints with unique error codes and trace IDs.",
     "Provides structured error context enabling automated localized error dialogs on frontend.",
     ["Consistent error contract", "Easier debugging", "Requires error mapper middleware on all services"]),

    (36, "Database Migrations Managed via Version-Controlled Prisma / Liquibase", "APPROVED", "Database Governance",
     "Ad-hoc manual SQL alterations lead to schema drift between development, staging, and production.",
     ["Manual SQL Scripts Run by DBAs", "ORM Auto-Sync in Production", "Strict Forward-Only Migration Scripts with Version Control"],
     "Manage all schema changes via version-controlled migration files tested in CI before promotion.",
     "Eliminates schema drift and enables automated rollbacks and reproducible staging environments.",
     ["Zero schema drift", "Auditable database evolution", "Requires strict migration review"]),

    (37, "Code Red Break-Glass Clinical Override Architecture", "APPROVED", "Clinical Governance",
     "Unconscious trauma patients requiring emergency resuscitation cannot provide digital informed consent.",
     ["Block Care without Consent", "Ignore Consent Rules Completely", "Cryptographic Break-Glass Override with Mandatory Post-Hoc Audit"],
     "Implement Break-Glass override granting immediate emergency EMR access with high-priority audit flagging.",
     "Protects human life during clinical crises while preserving legal defensibility and preventing abuse.",
     ["Life-saving emergency access", "Non-repudiable audit trail", "Mandates post-hoc supervisor review within 24h"]),

    (38, "Prometheus Metrics and Grafana Dashboard Operational Stack", "APPROVED", "Observability",
     "Operations teams must monitor health, sync lag, and resource usage across 183 clinics simultaneously.",
     ["Manual Server Checks", "Cloud Provider Dashboards", "Central Prometheus Scraping with Custom Grafana Dashboards"],
     "Expose standard `/metrics` endpoints and scrape them centrally for unified municipal health monitoring.",
     "Provides real-time visibility into clinic online/offline states, queue lengths, and sync backlogs.",
     ["Comprehensive municipal monitoring", "Automated alerting via Telegram/PagerDuty", "Requires metric storage capacity"]),

    (39, "Debezium Change Data Capture (CDC) for Zero-Impact ETL", "APPROVED", "Data Engineering",
     "Extracting daily public health reports via batch SQL queries overloads production databases.",
     ["Nightly Full SQL Dumps", "Application-Level Dual Writes", "Debezium CDC Reading PostgreSQL Write-Ahead Log to Kafka"],
     "Deploy Debezium to stream row-level changes directly from PostgreSQL WAL into Kafka without query overhead.",
     "Delivers sub-second data synchronization to analytical ClickHouse storage with zero impact on clinical OLTP.",
     ["Zero database query load", "Near real-time analytics", "Requires Kafka and Debezium operational setup"]),

    (40, "Automated Nightly Edge-to-Cloud Database Backup and Media Rotation", "APPROVED", "Disaster Recovery",
     "Clinic edge mini-servers can suffer hardware failure, theft, or catastrophic physical damage.",
     ["No Local Backup", "Manual Backup to USB by Staff", "Automated Nightly Encrypted Snapshot to Secondary Drive and Cloud"],
     "Execute automated nightly SQLite database backups with AES-256 encryption mirrored to secondary media.",
     "Ensures maximum Recovery Point Objective (RPO) of < 15 minutes and total recovery from local disasters.",
     ["Protects municipal clinical records", "Automated verification test", "Requires local storage management"]),

    (41, "Voluntary Citizen ABHA Linking with Fallback to Municipal ID", "APPROVED", "Statutory Policy",
     "Enforcing mandatory ABHA creation causes citizen exclusion for migrants and illiterate residents.",
     ["Mandatory ABHA Required for Treatment", "No ABHA Support", "Voluntary ABHA Linking with Sovereign Municipal ID Fallback"],
     "Make ABHA integration strictly voluntary; every citizen is guaranteed care via municipal ID.",
     "Satisfies National Health Mission goals while honoring constitutional rights to free healthcare access.",
     ["Universal citizen inclusion", "Zero care denial", "Maintains dual identifier mappings"]),

    (42, "Standardized Lab Diagnostic Catalog for 58 Mandated Namma Tests", "APPROVED", "Diagnostics Governance",
     "Inconsistent lab test naming across clinics prevents municipal quality benchmarking and aggregate analysis.",
     ["Free Text Lab Orders", "Varying Commercial Test Menus", "Standardized 58 Namma Lab Test Catalog with LOINC Mappings"],
     "Standardize all diagnostic orders on the mandated 58 Namma Clinic tests with reference ranges.",
     "Ensures consistent diagnostic quality, standard reference bands, and automated municipal lab statistics.",
     ["Standardized primary care testing", "Accurate aggregate reporting", "Requires clinical catalog maintenance"]),

    (43, "Municipal Outpatient Prescribing Security Barrier (SOD-001)", "APPROVED", "Clinical Governance",
     "Pharmacists creating prescriptions or doctors dispensing medications creates fraud and medical error risks.",
     ["Shared Clinical Login Accounts", "Soft Warnings on UI", "Hard Cryptographic Role Barrier Enforcing Prescriber vs Dispenser Separation"],
     "Enforce cryptographic Segregation of Duties (SOD-001) preventing any user from possessing both roles.",
     "Prevents prescription fraud, medication theft, and adverse clinical medication dispensing errors.",
     ["Eliminates dispensing fraud", "Enforces clinical safety", "Requires distinct staff in every clinic"]),

    (44, "Clinic Appliance Hardware Commissioning Pre-Flight Test Suite", "APPROVED", "Operations Engineering",
     "Deploying uncalibrated hardware leads to scanner failures, printer jams, and clinic morning chaos.",
     ["Plug and Play Deployment", "Informal Check by Field Staff", "Automated 12-Step Hardware Pre-Flight Commissioning Suite"],
     "Require successful execution of an automated pre-flight script before a clinic is marked 'ACTIVE'.",
     "Guarantees that barcode scanners, receipt printers, UPS cutover, and edge servers function flawlessly.",
     ["Zero deployment morning surprises", "Consistent hardware baseline", "Requires 15 minutes commissioning per clinic"]),

    (45, "Blue/Green Zero-Downtime Deployment Strategy for Central Services", "APPROVED", "Release Engineering",
     "Deploying updates during operating hours must never disrupt active patient consultations across Bengaluru.",
     ["In-Place Service Restarts", "Maintenance Outage Windows", "Blue/Green Deployment with Automated Health-Checked Traffic Switch"],
     "Execute all production releases using Blue/Green deployments with automated smoke test verification.",
     "Guarantees zero downtime for clinic users and allows instant one-click rollback if errors emerge.",
     ["100% zero-downtime releases", "Instant rollback safety", "Requires double infrastructure during deployment"])
]

ADRS = [
    {
        "id": f"ADR-{a[0]:03d}",
        "num": a[0],
        "title": a[1],
        "status": a[2],
        "category": a[3],
        "context": a[4],
        "options": a[5],
        "decision": a[6],
        "rationale": a[7],
        "consequences": a[8]
    }
    for a in ADR_DATA
]

ADR_MAP = {a["id"]: a for a in ADRS}

TOTAL_CONTAINERS = len(CONTAINERS)
TOTAL_COMPONENTS = len(COMPONENTS)
TOTAL_ADRS = len(ADRS)
# -------------------------------------------------------------
# 4. 30 Product Modules (MODULE-001 to MODULE-030)
# -------------------------------------------------------------
MODULES_RAW = [
    ("MODULE-001", "Staff Authentication & MFA Engine", "DOMAIN-001", "Core Foundation & Platform Administration", "ARCH-CONT-004", "ARCH-DATA-001", "P0 - Critical", "CORE MVP",
     "Manages staff identities, Argon2id salted credentials, TOTP MFA challenges, session lifecycle, and cryptographic token issuance.",
     "POST /api/v1/auth/login, POST /api/v1/auth/mfa/verify, POST /api/v1/auth/refresh, POST /api/v1/auth/logout",
     "Enforces rate limiting (5 attempts/min), brute-force lockout, and AES-256 encrypted credential caches on edge nodes."),

    ("MODULE-002", "Role-Based Access Control (RBAC) & Entitlements", "DOMAIN-001", "Core Foundation & Platform Administration", "ARCH-CONT-004", "ARCH-DATA-002", "P0 - Critical", "CORE MVP",
     "Defines and enforces granular permissions, capability claims, and segregation of duties (SOD-001) across 30 clinical and administrative roles.",
     "GET /api/v1/rbac/roles, POST /api/v1/rbac/entitlements/evaluate, PUT /api/v1/rbac/staff/:id/roles",
     "Validates role claims per request; denies unauthorized horizontal or vertical privilege escalation."),

    ("MODULE-003", "Healthcare Facility & Organizational Hierarchy", "DOMAIN-001", "Core Foundation & Platform Administration", "ARCH-CONT-002", "ARCH-DATA-003", "P0 - Critical", "CORE MVP",
     "Maintains the municipal hierarchy of 183 clinics, 8 BBMP zones, 225 wards, room allocations, and operational hours.",
     "GET /api/v1/facilities/clinics, GET /api/v1/facilities/zones, POST /api/v1/facilities/clinics/:id/rooms",
     "Edge appliances cache local clinic metadata; updates propagate via delta synchronization."),

    ("MODULE-004", "Clinical & Administrative Staff Directory", "DOMAIN-001", "Core Foundation & Platform Administration", "ARCH-CONT-004", "ARCH-DATA-004", "P0 - Critical", "CORE MVP",
     "Maintains professional profiles, medical registration council numbers (KMC), duty rosters, and shift schedules for clinic personnel.",
     "GET /api/v1/staff/directory, POST /api/v1/staff/roster/assign, GET /api/v1/staff/:id/qualifications",
     "Restricted PII access; medical council numbers verified against statutory state registries."),

    ("MODULE-005", "Patient Registration, Demographics & ABHA Minting", "DOMAIN-002", "Frontline Intake & Citizen Operations", "ARCH-CONT-005", "ARCH-DATA-005", "P0 - Critical", "CORE MVP",
     "Captures citizen demographic profiles, performs phonetic deduplication, mints municipal health IDs, and binds national ABHA numbers.",
     "POST /api/v1/patients/register, POST /api/v1/patients/search/phonetic, POST /api/v1/patients/abha/verify",
     "Full DPDP Act compliance; demographic data encrypted with AES-256 GCM; optional biometric deduplication."),

    ("MODULE-006", "Informed Clinical Consent & DPDP Data Privacy", "DOMAIN-002", "Frontline Intake & Citizen Operations", "ARCH-CONT-005", "ARCH-DATA-006", "P0 - Critical", "CORE MVP",
     "Records affirmative citizen consent for clinical treatment, tele-consultation, and health data sharing per DPDP Act 2023.",
     "POST /api/v1/consent/record, GET /api/v1/consent/status/:patientId, POST /api/v1/consent/revoke",
     "Consent artifacts cryptographically signed; provides emergency break-glass override with audit escalation."),

    ("MODULE-007", "Patient Token Generation & Station Routing", "DOMAIN-002", "Frontline Intake & Citizen Operations", "ARCH-CONT-006", "ARCH-DATA-007", "P0 - Critical", "CORE MVP",
     "Mints daily clinic visit tokens (General, Senior/Vulnerable, Emergency), prints 80mm thermal slips, and routes to initial station.",
     "POST /api/v1/tokens/issue, GET /api/v1/tokens/active/:clinicId, POST /api/v1/tokens/:id/route",
     "Local edge minting guarantees uninterrupted queueing during broadband outages; sub-second print dispatch."),

    ("MODULE-008", "Dynamic Queue Orchestration & Display Boards", "DOMAIN-002", "Frontline Intake & Citizen Operations", "ARCH-CONT-006", "ARCH-DATA-008", "P0 - Critical", "CORE MVP",
     "Manages dynamic multi-room queues, broadcasts next-patient calls to waiting hall TV screens via MQTT, and calculates wait times.",
     "POST /api/v1/queues/call-next, POST /api/v1/queues/transfer, GET /api/v1/queues/board-feed",
     "MQTT broker delivers token calls with < 50ms latency; audio chime and bilingual Kannada display."),

    ("MODULE-009", "Doctor EMR Console & Clinical SOAP Encounter", "DOMAIN-003", "Clinical Care & Diagnostic Orders", "ARCH-CONT-007", "ARCH-DATA-009", "P0 - Critical", "CORE MVP",
     "Provides physician consultation interface for capturing Subjective symptoms, Objective vitals/findings, Assessment, and Plan.",
     "POST /api/v1/encounters/start, PUT /api/v1/encounters/:id/soap, POST /api/v1/encounters/:id/seal",
     "Optimistic locking prevents concurrent overwrite; encounter seal signs record with cryptographic HMAC."),

    ("MODULE-010", "ICD-10 & SNOMED CT Clinical Diagnosis Coding", "DOMAIN-003", "Clinical Care & Diagnostic Orders", "ARCH-CONT-007", "ARCH-DATA-010", "P0 - Critical", "CORE MVP",
     "Enables fast bilingual autocomplete of clinical concepts mapped to SNOMED CT and statutory ICD-10 diagnostic codes.",
     "GET /api/v1/terminology/search, POST /api/v1/terminology/map-dual, GET /api/v1/terminology/stg/:condition",
     "Sub-15ms autocomplete via in-memory Trie/Redis cache; enforces standard treatment guidelines."),

    ("MODULE-011", "Electronic Prescription (e-Rx) & Drug Safety Engine", "DOMAIN-003", "Clinical Care & Diagnostic Orders", "ARCH-CONT-008", "ARCH-DATA-011", "P0 - Critical", "CORE MVP",
     "Authorizes e-prescriptions from essential drug formulary, evaluates drug-drug interactions, and checks pediatric dosage limits.",
     "POST /api/v1/prescriptions/create, POST /api/v1/prescriptions/safety-check, GET /api/v1/prescriptions/:id",
     "Hard stop on severe contraindications; generates bilingual Kannada dosage schedule and thermal print slip."),

    ("MODULE-012", "Point-of-Care Laboratory Testing & Diagnostic Orders", "DOMAIN-003", "Clinical Care & Diagnostic Orders", "ARCH-CONT-010", "ARCH-DATA-012", "P0 - Critical", "CORE MVP",
     "Manages orders and results for 58 rapid point-of-care laboratory diagnostic tests, specimen labelling, and panic value alerts.",
     "POST /api/v1/lab/orders/create, PUT /api/v1/lab/results/enter, POST /api/v1/lab/results/panic-escalate",
     "Panic values trigger instant audible alerts on doctor workstation; specimen labels formatted with barcodes."),

    ("MODULE-013", "Pharmacy Dispensing & 2D Barcode Verification", "DOMAIN-004", "Pharmacy, Dispensing & Inventory Supply Chain", "ARCH-CONT-009", "ARCH-DATA-013", "P0 - Critical", "CORE MVP",
     "Guides pharmacist through prescription dispensation, validates batch expiry via 2D DataMatrix scanning, and prints medicine slips.",
     "GET /api/v1/pharmacy/queue, POST /api/v1/pharmacy/dispense/scan, POST /api/v1/pharmacy/dispense/confirm",
     "Hardware scanner wedge input; prevents dispensing expired or recalled drug batches; updates inventory atomically."),

    ("MODULE-014", "Real-Time Batch Inventory & FEFO Stock Ledger", "DOMAIN-004", "Pharmacy, Dispensing & Inventory Supply Chain", "ARCH-CONT-009", "ARCH-DATA-014", "P0 - Critical", "CORE MVP",
     "Tracks stock levels per batch, enforces First-Expiry-First-Out allocation, monitors storage bins, and flags near-expiry items.",
     "GET /api/v1/inventory/batches, POST /api/v1/inventory/adjust, GET /api/v1/inventory/alerts/expiry",
     "ACID ledger transactions; prohibits negative stock balances; computes daily burn rates per clinic."),

    ("MODULE-015", "Drug Indent Generation, Receiving & Cold-Chain Intake", "DOMAIN-004", "Pharmacy, Dispensing & Inventory Supply Chain", "ARCH-CONT-009", "ARCH-DATA-015", "P0 - Critical", "CORE MVP",
     "Automates monthly replenishment indents to central warehouse (KDLWS), verifies receiving manifests, and logs cold-chain temps.",
     "POST /api/v1/indents/generate, POST /api/v1/indents/submit, POST /api/v1/indents/receive/verify",
     "Electronic Data Interchange with KDLWS; automated reorder level (ROL) calculations based on 30-day usage."),

    ("MODULE-016", "Essential Medicine List (EML) & Formulary Master", "DOMAIN-004", "Pharmacy, Dispensing & Inventory Supply Chain", "ARCH-CONT-009", "ARCH-DATA-016", "P0 - Critical", "CORE MVP",
     "Maintains the municipal primary care drug formulary, generic-brand mappings, therapeutic categories, and dosage forms.",
     "GET /api/v1/formulary/drugs, POST /api/v1/formulary/master/update, GET /api/v1/formulary/categories",
     "Authoritative clinical formulary; restricts prescribing to available clinic stock tiers."),

    ("MODULE-017", "Secondary Referral & 108 Emergency EMS Transit", "DOMAIN-005", "Care Continuity, Referrals & Community Outreach", "ARCH-CONT-011", "ARCH-DATA-017", "P0 - Critical", "CORE MVP",
     "Assembles referral dossiers for secondary hospitals, dispatches 108 emergency ambulance requests, and tracks patient handover.",
     "POST /api/v1/referrals/create, POST /api/v1/referrals/ems108/dispatch, GET /api/v1/referrals/tracking/:id",
     "Integrates with GVK-EMRI 108 CAD API; generates encrypted QR summary dossier for emergency transport."),

    ("MODULE-018", "NCD Longitudinal Follow-Up & Recall Management", "DOMAIN-005", "Care Continuity, Referrals & Community Outreach", "ARCH-CONT-012", "ARCH-DATA-018", "P1 - High", "MVP-PLUS",
     "Maintains disease registries for hypertension, diabetes, and mental health; tracks follow-up compliance and flags defaulters.",
     "POST /api/v1/ncd/enroll, GET /api/v1/ncd/follow-up/roster, POST /api/v1/ncd/recall/trigger",
     "Automated recall queues; generates outreach task lists for ANM and ASHA community health workers."),

    ("MODULE-019", "Citizen Multichannel Notifications & Health Reminders", "DOMAIN-005", "Care Continuity, Referrals & Community Outreach", "ARCH-CONT-012", "ARCH-DATA-019", "P1 - High", "CORE MVP",
     "Dispatches bilingual SMS and WhatsApp reminders for visit follow-ups, test result availability, and vaccination camps.",
     "POST /api/v1/notifications/send, GET /api/v1/notifications/delivery-status, POST /api/v1/notifications/campaigns",
     "DLT-registered templates on Karnataka State SMS Gateway; rate limited to avoid telecommunication spam."),

    ("MODULE-020", "Citizen Feedback, Grievance & Ombudsman Redressal", "DOMAIN-002", "Frontline Intake & Citizen Operations", "ARCH-CONT-012", "ARCH-DATA-020", "P2 - Medium", "MVP-PLUS",
     "Captures citizen feedback on tablet kiosks, tracks facility grievances (e.g. staff absence, drug shortages), and monitors SLAs.",
     "POST /api/v1/feedback/submit, POST /api/v1/grievance/file, GET /api/v1/grievance/sla-status",
     "Escalates unresolved grievances to BBMP Zonal Medical Officer; public rating metrics aggregated anonymously."),

    ("MODULE-021", "Cryptographic Audit Ledger & Compliance (WORM)", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-017", "ARCH-DATA-021", "P0 - Critical", "CORE MVP",
     "Records immutable write-once-read-many (WORM) audit trails with SHA-256 HMAC hash chaining for all clinical and auth events.",
     "POST /api/v1/audit/log, GET /api/v1/audit/verify-chain, GET /api/v1/audit/export/regulatory",
     "Non-repudiable audit proofs; mathematically detects record deletion or tampering; complies with DPDP Act 2023."),

    ("MODULE-022", "Zonal & Ward Operational KPI Dashboards", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-015", "ARCH-DATA-022", "P1 - High", "CORE MVP",
     "Delivers real-time public health indicators, clinic footfalls, stockout alerts, and disease heatmaps to municipal health officers.",
     "GET /api/v1/analytics/kpis/summary, GET /api/v1/analytics/heatmaps/ward, GET /api/v1/analytics/workload",
     "ClickHouse columnar aggregations; sub-second query latency; role-based data anonymization."),

    ("MODULE-023", "Safe AI/ML Clinical Decision Support Safeguards", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-016", "ARCH-DATA-023", "P2 - Medium", "POST-MVP",
     "Provides non-autonomous advisory machine learning predictions (syndromic fever clusters, defaulter risk) with mandatory doctor review.",
     "POST /api/v1/ai/advisory/evaluate, GET /api/v1/ai/models/status, POST /api/v1/ai/advisory/override-feedback",
     "Strict human-in-the-loop requirement; physician override logged; zero automated prescription or diagnostic action."),

    ("MODULE-024", "National Health ABDM Ecosystem Interoperability", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-014", "ARCH-DATA-024", "P1 - High", "CORE MVP",
     "Bridges platform with Ayushman Bharat Digital Mission (M1: ABHA, M2: HIP Care Context, M3: HIU Consent) via FHIR R4.",
     "POST /api/v1/abdm/m1/verify-abha, POST /api/v1/abdm/m2/publish-fhir, POST /api/v1/abdm/m3/fetch-consented",
     "Transforms clinical records to FHIR R4 bundles (Bundle, Condition, MedicationRequest, Observation)."),

    ("MODULE-025", "Autonomous Offline Edge Engine & Conflict Replay", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-013", "ARCH-DATA-025", "P0 - Critical", "CORE MVP",
     "Orchestrates 72-hour edge autonomy on SQLite WAL, journals local mutations with vector clocks, and replays deltas via CRDTs.",
     "POST /api/v1/sync/handshake, POST /api/v1/sync/push-mutations, GET /api/v1/sync/pull-deltas",
     "Deterministic field-level conflict resolution; bandwidth-throttled resume; zero transaction loss during WAN partitions."),

    ("MODULE-026", "Master System Administration & Feature Flagging", "DOMAIN-001", "Core Foundation & Platform Administration", "ARCH-CONT-003", "ARCH-DATA-026", "P0 - Critical", "CORE MVP",
     "Provides system administrators with tenant configuration controls, dynamic feature toggles, maintenance mode, and log levels.",
     "GET /api/v1/admin/configs, PUT /api/v1/admin/feature-flags, POST /api/v1/admin/maintenance-window",
     "Granular canary rollouts by clinic ID; dynamic configuration refresh without pod restart."),

    ("MODULE-027", "State Health HMIS & Statutory Disease Reporting", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-015", "ARCH-DATA-027", "P1 - High", "CORE MVP",
     "Compiles and exports statutory health indicator formats for Karnataka Health Management Information System and IDSP/IHIP.",
     "POST /api/v1/reports/hmis/generate, GET /api/v1/reports/idsp/syndromic, POST /api/v1/reports/statutory/submit",
     "Automates Form P, Form L, and Form S syndromic surveillance feeds; eliminates manual paper report collation."),

    ("MODULE-028", "Facility Operations Helpdesk & Incident Dispatch", "DOMAIN-005", "Care Continuity, Referrals & Community Outreach", "ARCH-CONT-002", "ARCH-DATA-028", "P2 - Medium", "MVP-PLUS",
     "Tracks hardware faults (printer jam, scanner failure, UPS battery warning) and dispatches field technicians across clinics.",
     "POST /api/v1/helpdesk/tickets/create, GET /api/v1/helpdesk/tickets/clinic/:id, PUT /api/v1/helpdesk/tickets/:id/resolve",
     "Automated telemetry alarms from edge mini-servers trigger preventive maintenance tickets."),

    ("MODULE-029", "Telemedicine & Specialist Tele-Consultation Bridge", "DOMAIN-003", "Clinical Care & Diagnostic Orders", "ARCH-CONT-007", "ARCH-DATA-029", "P2 - Medium", "POST-MVP",
     "Connects primary clinic doctors with secondary hospital specialists for real-time video consultation and joint review.",
     "POST /api/v1/telemed/sessions/initiate, GET /api/v1/telemed/specialists/available, POST /api/v1/telemed/sessions/:id/notes",
     "WebRTC encrypted media streams; shared clinical encounter view with real-time vitals and diagnostic telemetry."),

    ("MODULE-030", "Municipal Pilot Command Center & Disaster Operations", "DOMAIN-006", "Intelligence, Governance, Offline & Interoperability", "ARCH-CONT-015", "ARCH-DATA-030", "P2 - Medium", "POST-MVP",
     "Central command console for municipal epidemic surveillance, disaster mass casualty triage, and city-wide resource diversion.",
     "GET /api/v1/command/overview, POST /api/v1/command/alerts/broadcast, POST /api/v1/command/resources/reallocate",
     "City-wide geospatial situational awareness; automated outbreak cluster detection across 183 clinics.")
]

MODULES = [
    {
        "id": m[0],
        "name": m[1],
        "domain_id": m[2],
        "domain_name": m[3],
        "container_id": m[4],
        "data_id": m[5],
        "priority": m[6],
        "mvp_tier": m[7],
        "responsibilities": m[8],
        "endpoints": m[9],
        "security": m[10]
    }
    for m in MODULES_RAW
]

MODULE_MAP = {m["id"]: m for m in MODULES}
TOTAL_MODULES = len(MODULES)

# -------------------------------------------------------------
# 5. 25 Clinic Workflows (WF-001 to WF-025)
# -------------------------------------------------------------
WORKFLOWS_RAW = [
    ("WF-001", "Master Clinic Day Operational Workflow", "DOMAIN-001", "08:00 AM Clinic opening & system startup", "ARCH-CONT-002", ["ARCH-CONT-001", "ARCH-CONT-004", "ARCH-CONT-018"], "Comprehensive clinic operational lifecycle from staff check-in to evening closeout."),
    ("WF-002", "Staff Login, Multi-Factor Authentication & Session Management", "DOMAIN-001", "Staff member launches browser workstation", "ARCH-CONT-004", ["ARCH-CONT-001", "ARCH-CONT-002"], "Salted Argon2id authentication with TOTP MFA and offline PIN fallback."),
    ("WF-003", "Patient Registration, ABHA Creation & Demographic Intake", "DOMAIN-002", "Citizen arrives at clinic intake counter", "ARCH-CONT-005", ["ARCH-CONT-001", "ARCH-CONT-014"], "Bilingual demographic entry, phonetic deduplication, and voluntary ABHA minting."),
    ("WF-004", "Patient Search, Multi-Parametric Lookup & Verification", "DOMAIN-002", "Registration clerk searches returning citizen", "ARCH-CONT-005", ["ARCH-CONT-001", "ARCH-CONT-002"], "Fuzzy phonetic search by name, phone, municipal ID, or national ABHA address."),
    ("WF-005", "Repeat Patient Revisit & Longitudinal Episode Linking", "DOMAIN-002", "Identified returning patient checks in", "ARCH-CONT-005", ["ARCH-CONT-001", "ARCH-CONT-007"], "Links current clinical visit to historical EMR record and chronic disease episodes."),
    ("WF-006", "Informed Clinical & Digital Health Consent", "DOMAIN-002", "Patient begins consultation or data share", "ARCH-CONT-005", ["ARCH-CONT-001", "ARCH-CONT-017"], "Captures affirmative consent for treatment and ABDM record sharing per DPDP Act 2023."),
    ("WF-007", "Token Issuance, Priority Tagging & Queue Entry", "DOMAIN-002", "Citizen registration completed", "ARCH-CONT-006", ["ARCH-CONT-001", "ARCH-CONT-002"], "Mints daily serial token, applies vulnerability tags, and prints 80mm thermal slip."),
    ("WF-008", "Dynamic Multi-Room Queue Orchestration & Display", "DOMAIN-002", "Provider signals readiness for next patient", "ARCH-CONT-006", ["ARCH-CONT-001", "ARCH-CONT-002"], "Advances queue state, publishes MQTT chime, and updates waiting hall TV screen."),
    ("WF-009", "Nursing Triage, Vital Signs & Clinical Acuity Assessment", "DOMAIN-003", "Citizen called into nursing triage booth", "ARCH-CONT-006", ["ARCH-CONT-001", "ARCH-CONT-007"], "Records BP, pulse, SpO2, temp, height/weight, and calculates automated MEWS score."),
    ("WF-010", "Danger Sign Detection, Critical Value Alert & Emergency Escalation", "DOMAIN-003", "MEWS >= 5 or vital signs exceed critical thresholds", "ARCH-CONT-006", ["ARCH-CONT-001", "ARCH-CONT-011"], "Fires audible/visual alerts and escalates patient directly ahead of routine doctor queue."),
    ("WF-011", "Doctor Clinical Consultation, SOAP Documentation & CDSS Advisory", "DOMAIN-003", "Doctor opens active patient consultation", "ARCH-CONT-007", ["ARCH-CONT-001", "ARCH-CONT-016"], "Captures SOAP progress notes, codes diagnoses in SNOMED/ICD-10, and reviews CDSS advice."),
    ("WF-012", "Electronic Prescription, Drug Interaction & Safety Verification", "DOMAIN-003", "Doctor completes clinical evaluation", "ARCH-CONT-008", ["ARCH-CONT-001", "ARCH-CONT-009"], "Formulary e-prescribing, drug interaction verification, and cryptographic signing."),
    ("WF-013", "Pharmacy Dispensing, FEFO Inventory Allocation & Patient Counseling", "DOMAIN-004", "Patient presents token at pharmacy counter", "ARCH-CONT-009", ["ARCH-CONT-001", "ARCH-CONT-014"], "Scans 2D DataMatrix barcodes, verifies FEFO batch rules, and provides Kannada counseling."),
    ("WF-014", "Pharmacy Stock Replenishment, Indenting & Cold-Chain Inventory Control", "DOMAIN-004", "Stock drops below reorder level (ROL) or monthly cycle", "ARCH-CONT-009", ["ARCH-CONT-002", "ARCH-CONT-018"], "Generates automated replenishment indent, tracks KDLWS delivery, and logs cold chain."),
    ("WF-015", "Point-of-Care Laboratory Testing, Barcoding & Panic Value Alert", "DOMAIN-003", "Lab investigation ordered by physician", "ARCH-CONT-010", ["ARCH-CONT-001", "ARCH-CONT-007"], "Collects specimens, runs rapid diagnostic tests (58 panels), and reports panic values."),
    ("WF-016", "Clinical Referral, Higher Center Escalation & Ambulance Transfer", "DOMAIN-005", "Physician determines need for secondary care", "ARCH-CONT-011", ["ARCH-CONT-001", "ARCH-CONT-017"], "Compiles referral dossier, dispatches 108 emergency ambulance, and tracks transit."),
    ("WF-017", "NCD Follow-Up Scheduling, Chronic Disease Recall & Defaulter Tracking", "DOMAIN-005", "Hypertension or diabetes patient completes visit", "ARCH-CONT-012", ["ARCH-CONT-001", "ARCH-CONT-018"], "Schedules return appointment, dispatches reminders, and flags missed follow-ups."),
    ("WF-018", "Omnichannel Patient & Staff Notification, Alerting & Communication", "DOMAIN-005", "System event triggers notification (recall, panic)", "ARCH-CONT-012", ["ARCH-CONT-002", "ARCH-CONT-003"], "Formats and dispatches bilingual SMS and WhatsApp messages via state gateway."),
    ("WF-019", "Citizen Grievance Redressal, Feedback & SLA Escalation", "DOMAIN-002", "Citizen submits feedback or formal complaint", "ARCH-CONT-012", ["ARCH-CONT-001", "ARCH-CONT-015"], "Captures star rating, routes grievance to Zonal Medical Officer, and enforces SLA."),
    ("WF-020", "Cryptographic Audit Trail, Immutable Logging & Tamper Detection", "DOMAIN-006", "Any clinical, prescription, or auth state mutation", "ARCH-CONT-017", ["ARCH-CONT-002", "ARCH-CONT-018"], "Appends event to SHA-256 HMAC hash chain and validates Merkle tree consistency."),
    ("WF-021", "Clinical Analytics, Syndromic Surveillance & Population Health Reporting", "DOMAIN-006", "Scheduled nightly batch or real-time event stream", "ARCH-CONT-015", ["ARCH-CONT-018", "ARCH-CONT-016"], "Extracts CDC events to ClickHouse, aggregates ward KPIs, and flags fever outbreaks."),
    ("WF-022", "Autonomous Offline Edge Operation, Local Storage & Network Resilience", "DOMAIN-006", "WAN optical fiber cut or broadband failure", "ARCH-CONT-002", ["ARCH-CONT-001", "ARCH-CONT-013"], "Switches seamlessly to local SQLite WAL database; guarantees 72h clinic operation."),
    ("WF-023", "Bidirectional Synchronization, Conflict Resolution & Merkle Ledger", "DOMAIN-006", "WAN network connectivity restored", "ARCH-CONT-013", ["ARCH-CONT-002", "ARCH-CONT-018"], "Replays mutation journal with vector clocks, resolves CRDT conflicts, and updates edge."),
    ("WF-024", "Ayushman Bharat Digital Mission (ABDM) Gateway & FHIR Interoperability", "DOMAIN-006", "Citizen consents to publish health record to ABDM", "ARCH-CONT-014", ["ARCH-CONT-007", "ARCH-CONT-018"], "Transforms encounter to FHIR R4 Bundle and publishes care context to national grid."),
    ("WF-025", "Clinical Emergency Exception, Fast-Track Bypass & Resuscitation Protocol", "DOMAIN-003", "Trauma or unconscious patient brought to clinic", "ARCH-CONT-006", ["ARCH-CONT-001", "ARCH-CONT-011"], "Bypasses registration queue, issues emergency token, enables break-glass EMR access.")
]

WORKFLOWS = [
    {
        "id": w[0],
        "name": w[1],
        "domain_id": w[2],
        "trigger": w[3],
        "primary_container": w[4],
        "participating_containers": w[5],
        "description": w[6]
    }
    for w in WORKFLOWS_RAW
]

WORKFLOW_MAP = {w["id"]: w for w in WORKFLOWS}
TOTAL_WORKFLOWS = len(WORKFLOWS)

# -------------------------------------------------------------
# 6. 30 Relational Data Entities (ARCH-DATA-001 to ARCH-DATA-030)
# -------------------------------------------------------------
DATA_ENTITIES_RAW = [
    ("ARCH-DATA-001", "auth_users", "DOMAIN-001", "Staff identities, salted Argon2id hashes, MFA secrets, account status, lockout counters.", "UUIDv7", "CONFIDENTIAL", "Permanent", "Tier 1"),
    ("ARCH-DATA-002", "role_permissions", "DOMAIN-001", "RBAC role definitions, capability claims, resource grants, segregation-of-duty rules.", "UUIDv7", "INTERNAL", "Permanent", "Tier 1"),
    ("ARCH-DATA-003", "facilities", "DOMAIN-001", "183 clinic facilities, ward boundaries, zone assignments, operational rooms, GPS coords.", "UUIDv7", "PUBLIC", "Permanent", "Tier 2"),
    ("ARCH-DATA-004", "staff_profiles", "DOMAIN-001", "Doctor KMC registration, nurse qualifications, shift schedules, clinic assignments.", "UUIDv7", "RESTRICTED", "10 Years", "Tier 2"),
    ("ARCH-DATA-005", "patients", "DOMAIN-002", "Citizen demographic profiles, phonetic Soundex/Metaphone hashes, ABHA addresses, contact info.", "UUIDv7", "RESTRICTED_PHI", "Permanent", "Tier 1"),
    ("ARCH-DATA-006", "consent_records", "DOMAIN-002", "DPDP Act consent grants, purpose codes, expiry dates, revocation timestamps, digital signatures.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-007", "tokens", "DOMAIN-002", "Daily visit tokens, priority tier tags, serial numbers, intake station assignments.", "UUIDv7", "INTERNAL", "3 Years", "Tier 2"),
    ("ARCH-DATA-008", "queue_states", "DOMAIN-002", "Dynamic multi-room queue entries, call timestamps, wait durations, provider allocations.", "UUIDv7", "INTERNAL", "1 Year", "Tier 3"),
    ("ARCH-DATA-009", "clinical_encounters", "DOMAIN-003", "Outpatient visits, SOAP notes, vital signs, physical exam findings, doctor signatures.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-010", "diagnoses", "DOMAIN-003", "Clinical condition assessments, ICD-10 diagnostic codes, SNOMED CT concept identifiers.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-011", "prescriptions", "DOMAIN-003", "Electronic prescription headers, drug items, dosages, frequencies, duration, safety flags.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-012", "lab_orders", "DOMAIN-003", "Rapid test orders (58 panels), specimen barcodes, numerical results, panic value flags.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-013", "dispensations", "DOMAIN-004", "Pharmacy dispensation logs, 2D DataMatrix scans, batch allocations, counseling notes.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-014", "pharmacy_batches", "DOMAIN-004", "Medication batch ledger, manufactured date, expiry date, current stock count, FEFO rank.", "UUIDv7", "INTERNAL", "10 Years", "Tier 1"),
    ("ARCH-DATA-015", "drug_indents", "DOMAIN-004", "Replenishment orders to KDLWS warehouse, line items, approved quantities, dispatch status.", "UUIDv7", "INTERNAL", "5 Years", "Tier 2"),
    ("ARCH-DATA-016", "formulary_master", "DOMAIN-004", "Essential medicine catalog, generic names, therapeutic classes, pediatric dosage bands.", "UUIDv7", "PUBLIC", "Permanent", "Tier 2"),
    ("ARCH-DATA-017", "referrals", "DOMAIN-005", "Secondary hospital referrals, clinical summary dossiers, 108 ambulance dispatch logs.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-018", "ncd_episodes", "DOMAIN-005", "Chronic disease registries (hypertension, diabetes), recall dates, defaulter status.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-019", "notifications", "DOMAIN-005", "Bilingual SMS/WhatsApp messages, delivery receipts, template IDs, recipient numbers.", "UUIDv7", "RESTRICTED", "1 Year", "Tier 3"),
    ("ARCH-DATA-020", "grievances", "DOMAIN-002", "Citizen feedback submissions, grievance categories, resolution notes, ombudsman audit logs.", "UUIDv7", "RESTRICTED", "5 Years", "Tier 2"),
    ("ARCH-DATA-021", "audit_events", "DOMAIN-006", "Immutable WORM audit ledger, SHA-256 HMAC hash chains, user IDs, IP addresses, payloads.", "UUIDv7", "CONFIDENTIAL", "10 Years", "Tier 1"),
    ("ARCH-DATA-022", "kpi_metrics", "DOMAIN-006", "Daily clinic footfall aggregates, consultation durations, antibiotic ratios, stock levels.", "UUIDv7", "PUBLIC_AGGREGATE", "10 Years", "Tier 3"),
    ("ARCH-DATA-023", "cdss_rules", "DOMAIN-006", "Clinical decision support rule definitions, drug-drug contraindication pairs, allergy matrices.", "UUIDv7", "INTERNAL", "Permanent", "Tier 2"),
    ("ARCH-DATA-024", "abdm_artifacts", "DOMAIN-006", "FHIR R4 Bundles, care context links, HIP publishing receipts, consent artifacts.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-025", "mutation_log", "DOMAIN-006", "Edge offline journal, vector clock timestamps, entity mutations, sync status flags.", "UUIDv7", "INTERNAL", "90 Days", "Tier 1"),
    ("ARCH-DATA-026", "system_configs", "DOMAIN-001", "Tenant configuration parameters, dynamic feature flags, clinic operational toggles.", "UUIDv7", "CONFIDENTIAL", "Permanent", "Tier 1"),
    ("ARCH-DATA-027", "hmis_reports", "DOMAIN-006", "Statutory state health reports, Form P/L/S syndromic surveillance summaries.", "UUIDv7", "PUBLIC_AGGREGATE", "10 Years", "Tier 2"),
    ("ARCH-DATA-028", "helpdesk_tickets", "DOMAIN-005", "Facility hardware fault logs, IT support tickets, technician dispatch notes.", "UUIDv7", "INTERNAL", "3 Years", "Tier 3"),
    ("ARCH-DATA-029", "teleconsultations", "DOMAIN-003", "Telemedicine specialist consultation sessions, WebRTC call metadata, joint notes.", "UUIDv7", "RESTRICTED_PHI", "10 Years", "Tier 1"),
    ("ARCH-DATA-030", "command_center_incidents", "DOMAIN-006", "Municipal epidemic outbreak alerts, flood/mass-casualty response incident records.", "UUIDv7", "RESTRICTED", "10 Years", "Tier 1")
]

DATA_ENTITIES = [
    {
        "id": d[0],
        "table": d[1],
        "domain": d[2],
        "description": d[3],
        "pk_type": d[4],
        "classification": d[5],
        "retention": d[6],
        "backup_tier": d[7]
    }
    for d in DATA_ENTITIES_RAW
]

DATA_ENTITY_MAP = {d["id"]: d for d in DATA_ENTITIES}
TOTAL_DATA_ENTITIES = len(DATA_ENTITIES)

# -------------------------------------------------------------
# 7. 16 External Systems (EXT-001 to EXT-016)
# -------------------------------------------------------------
EXTERNAL_SYSTEMS_RAW = [
    ("EXT-001", "ABDM National Health Gateway", "National Health Authority (NHA)", "REST / HTTPS / FHIR R4", "JSON / FHIR Bundle", "100 req/min", "Asynchronous retry queue", "National DMZ"),
    ("EXT-002", "Karnataka Central Drug Warehouse (KDLWS)", "State Health Department", "REST / HTTPS / EDI", "JSON / EDIFACT", "30 req/min", "Local indent cache", "State Intranet"),
    ("EXT-003", "GVK-EMRI 108 Emergency Ambulance Dispatch", "Emergency Management Research Institute", "REST / HTTPS", "JSON / CAD Event", "120 req/min", "Manual phone dispatch escalation", "Emergency Gateway"),
    ("EXT-004", "Karnataka State SMS Gateway (KSSD)", "Centre for e-Governance (CeG)", "HTTPS POST API", "JSON / DLT Template", "500 req/sec", "Message buffer in Redis BullMQ", "State Gateway"),
    ("EXT-005", "Integrated Disease Surveillance Program (IDSP/IHIP)", "National Centre for Disease Control (NCDC)", "REST / HTTPS", "JSON / CSV Format", "50 req/min", "Daily batch retry", "National Health Mesh"),
    ("EXT-006", "BBMP Citizen Health Portal", "Bruhat Bengaluru Mahanagara Palike", "REST / HTTPS / OAuth2", "JSON", "200 req/min", "Cached appointment slots", "Municipal Cloud"),
    ("EXT-007", "National NCD Portal", "Ministry of Health and Family Welfare (MoHFW)", "REST / HTTPS", "JSON / FHIR", "60 req/min", "Offline NCD queue sync", "National Portal"),
    ("EXT-008", "Nikshay Portal (National TB Elimination)", "Central TB Division (CTD)", "REST / HTTPS", "JSON", "60 req/min", "Presumptive TB case queue", "National Health Mesh"),
    ("EXT-009", "Reproductive and Child Health (RCH) Portal", "MoHFW / Karnataka Health", "REST / HTTPS", "JSON", "60 req/min", "Antenatal offline buffer", "National Health Mesh"),
    ("EXT-010", "UIDAI Aadhaar Authentication Service", "Unique Identification Authority of India", "HTTPS / XML / Auth API", "Encrypted XML PID Block", "100 req/min", "Fallback to municipal health ID", "Statutory Sovereign"),
    ("EXT-011", "Zero-Cost Municipal Voucher Billing Gateway", "BBMP Health Accounts", "REST / HTTPS", "JSON / Voucher Token", "150 req/min", "Local voucher offline issue", "Municipal Intranet"),
    ("EXT-012", "Bio-Medical Waste Management (BMWM) Tracking", "Karnataka State Pollution Control Board", "REST / HTTPS", "JSON / Barcode Log", "30 req/min", "Local waste register", "Regulatory Gateway"),
    ("EXT-013", "Central Referral Hospital LIMS", "BBMP Tertiary Hospitals (KC General, Bowring)", "HL7 v2 / FHIR R4", "HL7 ORU_R01 / FHIR", "60 req/min", "Manual result printout", "Hospital Intranet"),
    ("EXT-014", "Central Pollution Control Board (CPCB) & Weather API", "CPCB / IMD Bengaluru", "REST / HTTPS", "JSON / Time-series", "10 req/min", "Last known 24h average", "Public Data"),
    ("EXT-015", "BBMP Municipal GIS & Ward Boundary Service", "BBMP Town Planning Department", "REST / GeoJSON / WFS", "GeoJSON Polygons", "50 req/min", "Cached offline GeoJSON layers", "Municipal Intranet"),
    ("EXT-016", "Cloud Hardware Security Module (KMS / HSM)", "MeitY Empaneled Cloud Provider", "PKCS#11 / REST KMS", "Binary Key Blocks", "1,000 req/sec", "Local TPM 2.0 derived keys", "Secure Hardware Enclave")
]

EXTERNAL_SYSTEMS = [
    {
        "id": s[0],
        "name": s[1],
        "agency": s[2],
        "protocol": s[3],
        "payload": s[4],
        "rate_limit": s[5],
        "fallback": s[6],
        "trust_level": s[7]
    }
    for s in EXTERNAL_SYSTEMS_RAW
]

EXTERNAL_SYSTEM_MAP = {s["id"]: s for s in EXTERNAL_SYSTEMS}
TOTAL_EXTERNAL_SYSTEMS = len(EXTERNAL_SYSTEMS)

# -------------------------------------------------------------
# 8. 8 Standard Environments (ENV-001 to ENV-008)
# -------------------------------------------------------------
ENVIRONMENTS_RAW = [
    ("ENV-001", "LOCAL", "Development Tier", "Individual developer workstation testing with Docker Compose and local SQLite/Postgres.", "Engineers", "Strictly Synthetic Data", "Local .env file", "Local Git commit"),
    ("ENV-002", "DEV", "Integration Tier", "Continuous integration build server, ephemeral feature branch validation.", "Dev Team", "Strictly Synthetic Data", "HashiCorp Vault Dev", "PR merge to develop"),
    ("ENV-003", "TEST", "Automated QA Tier", "Continuous nightly automated regression, contract testing with Pact, API stress testing.", "QA Automation", "Scrambled Synthetic Baseline", "HashiCorp Vault Test", "Automated test suite pass"),
    ("ENV-004", "QA", "Manual Verification Tier", "Manual exploratory testing, peripheral hardware certification (scanners, thermal printers).", "QA Team / PMs", "Anonymized Historical Clones", "HashiCorp Vault QA", "Manual QA sign-off"),
    ("ENV-005", "STAGING", "Pre-Production Tier", "Identical topology to production, performance benchmark runs, disaster recovery failover drill.", "Release Leads", "Synthetically Scaled 183-Clinic Data", "Vault KMS Staging", "Release gate checklist"),
    ("ENV-006", "PILOT", "Field Canary Tier", "Live deployment across 5 designated Namma Clinics in Bengaluru for field beta validation.", "Clinic Staff (5 Clinics)", "Live Operational Patient Data", "Vault Production KMS", "BBMP Medical Board Approval"),
    ("ENV-007", "PROD", "Production Tier", "Authoritative production platform serving all 183 Namma Clinics across Bengaluru.", "All Clinic Staff & Citizens", "Live Production Health Records", "Dedicated Cloud HSM / Vault KMS", "Executive Release Approval"),
    ("ENV-008", "DR", "Disaster Recovery Tier", "Hot-standby replicated environment in secondary cloud region (Mumbai) for instant failover.", "SRE / Ops On-Call", "Real-Time Replicated Production Data", "Replicated Cloud HSM / Vault", "Automated / Manual Failover Gate")
]

ENVIRONMENTS = [
    {
        "id": e[0],
        "name": e[1],
        "tier": e[2],
        "purpose": e[3],
        "users": e[4],
        "data_policy": e[5],
        "secrets": e[6],
        "promotion_gate": e[7]
    }
    for e in ENVIRONMENTS_RAW
]

ENVIRONMENT_MAP = {e["id"]: e for e in ENVIRONMENTS}
TOTAL_ENVIRONMENTS = len(ENVIRONMENTS)

# -------------------------------------------------------------
# 9. 12 Advisory Clinical AI Models (ARCH-AI-001 to ARCH-AI-012)
# -------------------------------------------------------------
AI_MODELS_RAW = [
    ("ARCH-AI-001", "Syndromic Fever Cluster Anomaly Detector", "Epidemiology", "Spatial-Temporal DBSCAN & Poisson Regression", "Ward ID, daily fever counts, rainfall, temperature, rolling 7-day baseline", "Outbreak probability score (0.00-1.00) & anomaly flag", "Mandatory review by District Epidemiologist; no public alert without CMO sign-off.", "Trained on de-identified historical BBMP fever surveillance data."),
    ("ARCH-AI-002", "Drug-Drug Adverse Interaction Advisor", "Clinical Pharmacology", "Rule Engine + BioBERT Embedding Classifier", "Active patient prescription drugs, proposed new medication, known allergy list", "Contraindication severity (MILD, MODERATE, SEVERE, FATAL) & clinical explanation", "Physician can dismiss MILD/MODERATE; SEVERE requires written clinical justification in EMR.", "Zero autonomous cancellation; human prescriber retains sole authority."),
    ("ARCH-AI-003", "Pediatric Dosage Boundary Safety Checker", "Clinical Pediatrics", "Pharmacokinetic Nomogram Boundary Model", "Patient age in months, weight in kg, drug formulary ID, prescribed frequency/dose", "Recommended dose range (mg/kg/day) & overdosing warning alert", "Hard visual warning if proposed dose > 120% of maximum safe pediatric threshold.", "Calibrated to Indian Academy of Pediatrics (IAP) standard formularies."),
    ("ARCH-AI-004", "NCD Defaulter & Follow-up Risk Forecaster", "Chronic Care", "Gradient Boosted Trees (LightGBM)", "Patient age, distance to clinic, previous visit adherence, medication days supply", "Probability of loss-to-follow-up within 30 days (Low, Medium, High)", "Ranks community health worker outreach task list; never denies clinic service.", "Audited for demographic fairness across gender and socioeconomic wards."),
    ("ARCH-AI-005", "Clinic Pharmacy Stockout Predictor", "Supply Chain", "Temporal Fusion Transformer (TFT)", "Historical 90-day drug consumption, seasonality, current batch balance, reorder lead time", "Estimated days until zero stock & recommended indent quantity", "Pharmacist reviews and modifies recommended indent prior to submission to KDLWS.", "Guarantees no stock starvation for essential life-saving medications."),
    ("ARCH-AI-006", "Lab Panic Value Triager", "Diagnostics", "Deterministic Clinical Boundary Classifier", "58 rapid diagnostic test panel codes, quantitative lab result values, patient age/sex", "Normal, Abnormal, Critical Panic Value flag & escalation target", "Instant audible chime and visual red banner on doctor consultation screen.", "Calibrated to NABL accredited hospital laboratory critical thresholds."),
    ("ARCH-AI-007", "Chest X-Ray Screening Assistant (Advisory)", "Pulmonology", "DenseNet-121 Convolutional Neural Network", "Digital DICOM chest radiograph (when available via secondary referral)", "Heatmap bounding box & presumptive TB/pneumonia probability score", "Preliminary triage aid only; definitive diagnosis requires radiologist interpretation.", "Non-autonomous; marked as investigative screening device."),
    ("ARCH-AI-008", "Diabetic Retinopathy Screening Assistant", "Ophthalmology", "ResNet-50 Fundus Image Classifier", "Digital fundus camera image captured at referral hub", "Retinopathy grade (No DR, Mild, Moderate, Severe, Proliferative)", "Flags urgent ophthalmology referral; does not initiate medical therapy.", "Validated against South Indian diabetic retinopathy clinical datasets."),
    ("ARCH-AI-009", "Hypertension Staging & Guideline Advisor", "Cardiology", "Clinical Rule-Based Expert System", "Resting systolic BP, diastolic BP, age, diabetes co-morbidity, tobacco history", "Stage (Elevated, Stage 1, Stage 2, Hypertensive Crisis) & first-line STG recommendation", "Suggests standard treatment guidelines; physician selects final pharmacological regimen.", "Follows Indian Guidelines on Hypertension (IGH-IV)."),
    ("ARCH-AI-010", "Antibiotic Stewardship AWaRe Advisor", "Infectious Disease", "WHO AWaRe Classification Decision Matrix", "Prescribed antibiotic code, provisional clinical diagnosis, patient age", "AWaRe category (Access, Watch, Reserve) & guideline concordance score", "Educational alert encouraging first-line 'Access' antibiotics over 'Watch' class.", "Monitors clinic-wide antibiotic prescribing ratios for municipal health audit."),
    ("ARCH-AI-011", "Vitals MEWS Deterioration Predictor", "Emergency Triage", "Modified Early Warning Score (MEWS) Algorithm", "Systolic BP, heart rate, respiratory rate, body temperature, AVPU consciousness score", "Integer MEWS score (0-14), clinical risk band (Low, Medium, High, Critical)", "MEWS >= 5 triggers automatic visual flashing and escalates queue to Room 1 immediately.", "Deterministic mathematical scoring; zero black-box opacity."),
    ("ARCH-AI-012", "Duplicate Demographic Patient Matcher", "Frontline Intake", "Phonetic Soundex/Metaphone + Jaro-Winkler Metric", "Candidate citizen name, guardian name, date of birth, gender, ward, phone number", "Similarity match confidence (0.00-1.00) & candidate existing patient IDs", "Registration nurse inspects candidate photo and history to confirm or create new record.", "Prevents fragmented medical records while avoiding erroneous identity merges.")
]

AI_MODELS = [
    {
        "id": a[0],
        "name": a[1],
        "domain": a[2],
        "model_type": a[3],
        "inputs": a[4],
        "outputs": a[5],
        "clinical_safeguard": a[6],
        "governance": a[7]
    }
    for a in AI_MODELS_RAW
]

AI_MODEL_MAP = {a["id"]: a for a in AI_MODELS}
TOTAL_AI_MODELS = len(AI_MODELS)


if __name__ == "__main__":
    print(f"Total Architecture Containers: {TOTAL_CONTAINERS}")
    print(f"Total Architecture Components: {TOTAL_COMPONENTS}")
    print(f"Total Architecture Decisions (ADRs): {TOTAL_ADRS}")
    print(f"Total Architecture Modules: {TOTAL_MODULES}")
    print(f"Total Architecture Workflows: {TOTAL_WORKFLOWS}")
    print(f"Total Architecture Data Entities: {TOTAL_DATA_ENTITIES}")
    print(f"Total External Systems: {TOTAL_EXTERNAL_SYSTEMS}")
    print(f"Total Environments: {TOTAL_ENVIRONMENTS}")
    print(f"Total Advisory AI Models: {TOTAL_AI_MODELS}")
