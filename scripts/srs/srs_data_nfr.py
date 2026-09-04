"""
srs_data_nfr.py
All 40 Non-Functional Requirements (SRS-NFR-001 through SRS-NFR-040)
for the Namma Clinic Digital Health & Operations Platform.
"""

from typing import Dict, List, Any

NFR_CATEGORIES = [
    ("Performance & Latency", 1, 6),
    ("Availability & Resilience", 7, 12),
    ("Scalability & Capacity", 13, 18),
    ("Security & Cryptography", 19, 24),
    ("Privacy & Data Governance", 25, 28),
    ("Offline & Edge Autonomy", 29, 32),
    ("Usability & Localization", 33, 36),
    ("Observability & Maintainability", 37, 40)
]

NFR_TITLES = {
    1: ("Edge Interactive Screen Latency Boundary", "Interactive UI screens on clinic local edge terminals shall respond to user input within 250 milliseconds at the 95th percentile (p95).", "PERF-001", "P0 - Critical"),
    2: ("Local Database Write Transaction Commit Latency", "Local SQLite edge database write transactions shall complete within 35 milliseconds at p99 to prevent UI thread blocking.", "PERF-002", "P0 - Critical"),
    3: ("Cloud API Gateway Response Latency", "Central cloud API endpoints shall process authenticated read/write payloads within 400 milliseconds at p95 under standard WAN conditions.", "PERF-003", "P1 - High"),
    4: ("Thermal Slip & 2D Barcode Print Execution Latency", "Receipt and prescription thermal slip generation shall emit ESC/POS command stream to hardware printer within 800 milliseconds.", "PERF-004", "P1 - High"),
    5: ("Full-Text Diagnostic & Drug Autocomplete Latency", "Clinical diagnostic and medication search queries shall return matching candidates in under 30 milliseconds.", "PERF-005", "P0 - Critical"),
    6: ("Waiting Hall TV Queue Screen State Broadcast Latency", "Queue token state changes shall propagate to clinic waiting hall TV displays via local MQTT in under 100 milliseconds.", "PERF-006", "P1 - High"),
    7: ("Local Clinic Edge Appliance Autonomous Availability", "The local clinic edge mini-server shall deliver 99.9% uptime during operational clinic hours (08:00 to 20:00).", "AVAIL-001", "P0 - Critical"),
    8: ("Uninterrupted 72-Hour Edge Operation During Total WAN Disconnection", "The clinic software shall operate with full clinical, pharmacy, and triage functionality for at least 72 continuous hours without cloud connectivity.", "AVAIL-002", "P0 - Critical"),
    9: ("Edge Server High-Availability Hot-Standby Failover", "If the primary clinic edge appliance suffers hardware failure, a designated secondary workstation shall assume edge server duties within 180 seconds.", "AVAIL-003", "P1 - High"),
    10: ("Central Cloud Health Platform Multi-Zone Availability", "The central cloud Kubernetes platform and PostgreSQL cluster shall deliver 99.95% annual availability across multiple availability zones.", "AVAIL-004", "P0 - Critical"),
    11: ("Mean Time to Recovery (MTTR) for Edge Appliances", "Clinic field support engineers shall restore or replace a failed edge server within 4 operational hours across all 183 BBMP wards.", "AVAIL-005", "P1 - High"),
    12: ("Scheduled Maintenance Zero-Downtime Guarantee", "System updates and database index maintenance shall execute using zero-downtime rolling blue/green deployments without interrupting clinic operations.", "AVAIL-006", "P2 - Medium"),
    13: ("Concurrency Support for 183 Concurrent Clinic Facilities", "The central cloud platform shall concurrently support active operational loads from all 183 Namma Clinics without service degradation.", "SCALE-001", "P0 - Critical"),
    14: ("Daily Outpatient Consultation Throughput Capacity", "The system architecture shall scale to process at least 25,000 completed patient consultations per operating day across the city.", "SCALE-002", "P0 - Critical"),
    15: ("Concurrent User Session Capacity across Municipal Workforce", "The authentication and session infrastructure shall support at least 1,200 concurrent active staff sessions (doctors, nurses, pharmacists, lab techs).", "SCALE-003", "P1 - High"),
    16: ("Electronic Prescription Generation Peak Throughput", "The prescription and pharmacy dispensing sub-tier shall handle peak burst traffic of 50 new prescriptions per second across the municipality.", "SCALE-004", "P1 - High"),
    17: ("Longitudinal Data Storage Capacity for 5,000,000 Citizens", "The operational and historical data tiers shall comfortably store longitudinal medical records for 5 million urban residents over a 10-year retention horizon.", "SCALE-005", "P1 - High"),
    18: ("Analytics & Syndromic Surveillance Ingestion Throughput", "The streaming event bus shall ingest up to 2,000 clinical and operational telemetry events per second during outbreak periods.", "SCALE-006", "P2 - Medium"),
    19: ("Transport Layer Security (TLS 1.3) Cryptographic Invariant", "All data in transit across LAN, WAN, and external public gateways shall be encrypted using TLS 1.3 with modern cipher suites.", "SECR-001", "P0 - Critical"),
    20: ("AES-256 GCM Cryptographic Encryption at Rest", "All patient demographic, clinical, prescription, and laboratory records stored on edge SSDs and cloud storage shall be encrypted with AES-256 GCM.", "SECR-002", "P0 - Critical"),
    21: ("Role-Based Access Control (RBAC) & Principle of Least Privilege", "Access to system modules and data entities shall be strictly gated by verified user roles, preventing unentitled cross-module read or write.", "SECR-003", "P0 - Critical"),
    22: ("Cryptographic JSON Web Token (JWT) Staff Session Architecture", "Staff sessions shall be authenticated via cryptographically signed JWT tokens with 15-minute idle invalidation and rotating key pairs.", "SECR-004", "P0 - Critical"),
    23: ("Immutable WORM Audit Trail with Cryptographic Hash-Chaining", "All clinical edits, medication dispensations, and login events shall write to an append-only WORM ledger with SHA-256 hash chaining.", "SECR-005", "P0 - Critical"),
    24: ("Automated Vulnerability Management & Dependency Scanning", "The CI/CD pipeline shall enforce zero critical or high Common Vulnerabilities and Exposures (CVEs) before release deployment.", "SECR-006", "P1 - High"),
    25: ("Digital Personal Data Protection (DPDP) Act 2023 Conformance", "The platform shall enforce citizen consent capture, purposeful data limitation, and automated data retention policies conforming to the DPDP Act.", "PRIV-001", "P0 - Critical"),
    26: ("Zero Plaintext Protected Health Information (PHI) in Operational Logs", "Application logs, observability traces, and metrics shall enforce automated redaction of citizen names, phone numbers, and Aadhaar numbers.", "PRIV-002", "P0 - Critical"),
    27: ("Granular Data Access Masking on Administrative Interfaces", "Administrative, analytics, and billing dashboards shall display de-identified or aggregated patient data without exposing direct patient identifiers.", "PRIV-003", "P1 - High"),
    28: ("Citizen Digital Consent Revocation & Data Quarantine", "If a citizen formally revokes consent, the system shall quarantine non-essential shared records from external health exchange networks within 24 hours.", "PRIV-004", "P1 - High"),
    29: ("Local Client-Side Mutation Journaling in IndexedDB", "Frontend browser clients shall log all state mutations into local IndexedDB queues with monotonically increasing sequence numbers.", "OFF-001", "P0 - Critical"),
    30: ("Deterministic Vector Clock Conflict Resolution", "When re-synchronizing after network partitions, the sync engine shall resolve concurrent record updates using deterministic vector clocks and CRDT rules.", "OFF-002", "P0 - Critical"),
    31: ("Bandwidth-Throttled Asynchronous Cloud Replay", "Edge synchronization shall utilize compressed delta payloads and adaptive rate limiting to prevent overwhelming low-bandwidth 2G/3G backup connections.", "OFF-003", "P1 - High"),
    32: ("Offline Session Verification via Local Cryptographic Keystore", "Staff shall remain authenticated during local edge operations using cached Argon2id salted credentials even during internet disconnections.", "OFF-004", "P0 - Critical"),
    33: ("Comprehensive Bilingual Localization in Kannada and English", "100% of user interface screens, error messages, and citizen print slips shall support authentic Kannada (kn-IN) and Indian English (en-IN).", "LOC-001", "P0 - Critical"),
    34: ("Web Content Accessibility Guidelines (WCAG 2.1 AA) Compliance", "All user interfaces shall satisfy WCAG 2.1 AA standards, ensuring minimum 4.5:1 color contrast, full keyboard navigability, and screen reader labels.", "A11Y-001", "P1 - High"),
    35: ("Low-Friction Touch & Ergonomic Form Design for Tablets", "Clinical entry screens shall provide large touch targets (minimum 48x48 dp) and rapid single-tap chips to minimize doctor typing fatigue.", "UX-001", "P1 - High"),
    36: ("Visual & Audible Accessibility Cues for Queue Events", "All queue token calls and clinical danger alerts shall provide synchronized visual flashing banners and synthesized audio voice announcements.", "A11Y-002", "P1 - High"),
    37: ("OpenTelemetry Distributed Tracing & Semantic Conventions", "All cross-service requests, edge sync operations, and database queries shall propagate W3C TraceContext headers with OpenTelemetry spans.", "OBS-001", "P1 - High"),
    38: ("Prometheus Metrics Instrumentation for Operational Telemetry", "Every container and service shall expose standardized Prometheus metric endpoints instrumented with request rates, latencies, and error counters.", "OBS-002", "P1 - High"),
    39: ("Modular Monolith Architectural Boundary Enforcement", "Internal service dependencies shall communicate strictly via explicit domain interfaces and DTOs, strictly forbidding cross-boundary SQL joins.", "MAINT-001", "P0 - Critical"),
    40: ("Disaster Recovery Recovery Point Objective (RPO) < 15 Minutes", "The database replication and backup architecture shall guarantee an RPO of less than 15 minutes and an RTO of less than 30 minutes during disaster recovery.", "DR-001", "P0 - Critical")
}

ALL_NON_FUNCTIONAL_REQUIREMENTS: List[Dict[str, Any]] = []

for num, (title, desc, req_ref, priority_str) in NFR_TITLES.items():
    cat_name = "General Architecture"
    for cat, start, end in NFR_CATEGORIES:
        if start <= num <= end:
            cat_name = cat
            break

    nfr_id = f"SRS-NFR-{num:03d}"
    ALL_NON_FUNCTIONAL_REQUIREMENTS.append({
        "id": nfr_id,
        "title": title,
        "category": cat_name,
        "description": desc,
        "rationale": f"Establishes a rigorous engineering boundary for {title.lower()} to ensure enterprise stability, legal compliance, and clinical safety.",
        "target_metric": desc.split("shall")[1].strip() if "shall" in desc else desc,
        "measurement_method": "Automated Synthetic Monitoring & Continuous Performance Benchmarking",
        "verification_gate": f"Phase Quality Gate Test ({nfr_id})",
        "priority": "MUST" if "P0" in priority_str else ("SHOULD" if "P1" in priority_str else "COULD"),
        "priority_code": priority_str,
        "upstream_ref": req_ref,
        "acceptance_criteria": f"Given production or staged test harness load, when benchmark executes, then the system satisfies '{desc}' without failure.",
        "bdd_scenario": [
            f"Given the system is under test for {nfr_id}",
            f"When load conditions evaluate '{title}'",
            f"Then the observed metric satisfies target invariant '{target_metric[:60]}...'",
            "And zero SLA violations are recorded."
        ] if (target_metric := desc.split("shall")[1].strip() if "shall" in desc else desc) else [],
        "downstream_artifacts": [
            f"PLANNED-EPIC-NFR-{num:03d}",
            f"PLANNED-TEST-NFR-{num:03d}"
        ]
    })
