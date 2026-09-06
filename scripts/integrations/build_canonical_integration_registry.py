"""
build_canonical_integration_registry.py
Generates the 12 canonical registries for Phase 15 Enterprise Integration Engineering.
Outputs int_data_part1.py through int_data_part4.py and integration_core_data.py.
"""

import sys
from pathlib import Path

INT_DIR = Path(__file__).resolve().parent

DOMAINS = [
    "ABDM / National Digital Health",
    "FHIR R4 Diagnostic & Clinical Exchange",
    "e-Hospital Secondary / Tertiary Referral",
    "SMS & Push Notification Gateway",
    "State Health & IDSP Epidemiological Reporting",
    "Municipal Administrative & Financial Reporting",
    "Diagnostic Laboratory Equipment & Analyzers",
    "Pharmacy Logistics & Central Drug Warehouse",
    "Aadhaar & e-KYC Identity Verification",
    "Citizen Health Locker & Portability Export",
    "Geospatial GIS & BBMP Ward Demographics",
    "ASHA Community Health Worker Sync",
    "Emergency 108 Ambulance Dispatch Exchange",
    "Teleconsultation & Video Gateway",
    "Data Lakehouse & Columnar Analytics CDC"
]

def build_part1():
    lines = ['"""Phase 15 Canonical Integration Registry - Part 1: INTEGRATIONS & EXTERNAL_SYSTEMS"""', '']
    
    # 1. INTEGRATIONS (100 items: INT-001 to INT-100)
    lines.append('INTEGRATIONS = [')
    protocols = ["HTTPS REST", "gRPC", "Kafka Event Stream", "SFTP MFT", "FHIR R4 over HTTPS"]
    auths = ["OAuth 2.0 / Mutual TLS", "Keycloak OIDC JWT", "HMAC-SHA256 Signed Request", "API Key with IP Pinning", "mTLS with PKI Client Cert"]
    classifs = ["RESTRICTED_PHI", "CONFIDENTIAL_CLINICAL", "CONFIDENTIAL_OPERATIONAL", "INTERNAL_ADMINISTRATIVE"]
    
    for i in range(1, 101):
        dom = DOMAINS[(i - 1) % len(DOMAINS)]
        proto = protocols[(i - 1) % len(protocols)]
        auth = auths[(i - 1) % len(auths)]
        cls = classifs[(i - 1) % len(classifs)]
        direction = "OUTBOUND" if i % 3 == 0 else ("INBOUND" if i % 3 == 1 else "BIDIRECTIONAL")
        freq = "REALTIME_STREAM" if i % 4 == 0 else ("SUB_SECOND_RPC" if i % 4 == 1 else ("BATCH_HOURLY" if i % 4 == 2 else "DAILY_RECONCILED"))
        src = "namma_clinic_backend" if direction == "OUTBOUND" else f"ext_system_{(i-1)%50+1:03d}"
        tgt = f"ext_system_{(i-1)%50+1:03d}" if direction == "OUTBOUND" else "namma_clinic_backend"
        
        lines.append('    {')
        lines.append(f'        "id": "INT-{i:03d}",')
        lines.append(f'        "name": "integration_service_flow_{i:03d}",')
        lines.append(f'        "title": "Enterprise Integration Interface {i:03d} ({dom})",')
        lines.append(f'        "description": "Integration boundary managing data exchange, protocol mediation, and encryption for {dom} across Namma Clinic edge nodes.",')
        lines.append(f'        "domain": "{dom}",')
        lines.append(f'        "owner": "squad_integrations_platform",')
        lines.append(f'        "source": "{src}",')
        lines.append(f'        "target": "{tgt}",')
        lines.append(f'        "protocol": "{proto}",')
        lines.append(f'        "authentication": "{auth}",')
        lines.append(f'        "data_classification": "{cls}",')
        lines.append(f'        "direction": "{direction}",')
        lines.append(f'        "frequency": "{freq}",')
        lines.append(f'        "sla": "p95 < {150 + (i%5)*50}ms, availability 99.95%",')
        lines.append(f'        "slo": "Availability >= 99.95%, p99 latency < {300 + (i%5)*100}ms",')
        lines.append(f'        "retry_policy": "RETRY-{(i-1)%25+1:03d}",')
        lines.append(f'        "failure_behavior": "Circuit breaker trip after 5 consecutive failures, route to DLQ-INT-{i:03d}",')
        lines.append(f'        "security_controls": ["SEC-INT-{(i-1)%50+1:03d}", "mTLS", "Payload Encryption AES-256-GCM"],')
        lines.append(f'        "privacy_controls": ["DPDP Consent Verification", "Direct PII Masking", "k-Anonymity Guard"],')
        lines.append(f'        "monitoring": "MON-INT-{(i-1)%75+1:03d}",')
        lines.append(f'        "audit": "Immutable Kafka topic cdc.namma.integration_audit with HMAC-SHA256 signature",')
        lines.append(f'        "upstream_traceability": "REQ-INT-{(i-1)%40+1:03d}",')
        lines.append(f'        "downstream_backlog_reference": "EPIC-INT-{(i-1)%20+1:03d}",')
        lines.append(f'        "test_reference": "TEST-INT-{(i-1)%50+1:03d}",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    # 2. EXTERNAL_SYSTEMS (50 items: EXT-001 to EXT-050)
    lines.append('EXTERNAL_SYSTEMS = [')
    sys_categories = ["National Gateway", "State Health Portal", "Tertiary Hospital", "Diagnostic Equipment", "Telecom Gateway", "Municipal System", "Payment Gateway"]
    for i in range(1, 51):
        cat = sys_categories[(i - 1) % len(sys_categories)]
        lines.append('    {')
        lines.append(f'        "id": "EXT-{i:03d}",')
        lines.append(f'        "name": "external_partner_system_{i:03d}",')
        lines.append(f'        "title": "External System Authority {i:03d} ({cat})",')
        lines.append(f'        "category": "{cat}",')
        lines.append(f'        "governing_agency": "Government of Karnataka / National Health Authority",')
        lines.append(f'        "protocol_supported": "HTTPS REST / FHIR R4 Bundle",')
        lines.append(f'        "sandbox_endpoint": "https://sandbox-api.ext-{i:03d}.karnataka.gov.in/v1",')
        lines.append(f'        "production_endpoint": "https://api.ext-{i:03d}.karnataka.gov.in/v1",')
        lines.append(f'        "data_sovereignty": "Sovereign India Datacenter (MeitY Empaneled)",')
        lines.append(f'        "primary_contact_role": "Zonal Systems Liaison / External Operations Engineer",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    (INT_DIR / "int_data_part1.py").write_text("\n".join(lines), encoding="utf-8")
    print("Generated int_data_part1.py")

def build_part2():
    lines = ['"""Phase 15 Canonical Integration Registry - Part 2: INTEGRATION_INTERFACES & DATA_MAPPINGS"""', '']
    
    # 3. INTEGRATION_INTERFACES (100 items: IFACE-001 to IFACE-100)
    lines.append('INTEGRATION_INTERFACES = [')
    methods = ["POST", "GET", "PUT", "PATCH", "DELETE"]
    for i in range(1, 101):
        m = methods[(i - 1) % len(methods)]
        lines.append('    {')
        lines.append(f'        "id": "IFACE-{i:03d}",')
        lines.append(f'        "name": "api_endpoint_interface_{i:03d}",')
        lines.append(f'        "http_method": "{m}",')
        lines.append(f'        "route": "/api/v1/integrations/endpoint-{i:03d}",')
        lines.append(f'        "bound_integration": "INT-{(i-1)%100+1:03d}",')
        lines.append(f'        "request_schema": "SchemaReqInterface{i:03d}",')
        lines.append(f'        "response_schema": "SchemaResInterface{i:03d}",')
        lines.append(f'        "timeout_ms": {250 + (i%5)*50},')
        lines.append(f'        "rate_limit_rpm": {1200 + (i%5)*300},')
        lines.append(f'        "idempotency_supported": True,')
        lines.append(f'        "description": "Deterministic API endpoint interface {i:03d} with schema validation, rate limiting, and mTLS.",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    # 4. DATA_MAPPINGS (100 items: MAP-001 to MAP-100)
    lines.append('DATA_MAPPINGS = [')
    fhir_res = ["Patient", "Encounter", "Condition", "Observation", "MedicationRequest", "MedicationDispense", "DiagnosticReport", "ServiceRequest", "AllergyIntolerance", "CarePlan"]
    for i in range(1, 101):
        res = fhir_res[(i - 1) % len(fhir_res)]
        lines.append('    {')
        lines.append(f'        "id": "MAP-{i:03d}",')
        lines.append(f'        "source_entity": "public.entity_table_{(i-1)%52+1:03d}",')
        lines.append(f'        "source_field": "field_attr_{(i-1)%20+1:02d}",')
        lines.append(f'        "target_standard": "FHIR R4 / ABDM Profile",')
        lines.append(f'        "target_resource": "{res}",')
        lines.append(f'        "target_element": "{res}.element_{(i-1)%15+1:02d}",')
        lines.append(f'        "transformation_rule": "Deterministic ISO/SNOMED CT/ICD-10 ontology mapping with null-safe default",')
        lines.append(f'        "validation_assertion": "Non-null, regex conformance, and reference integrity check",')
        lines.append(f'        "privacy_handling": "Hashed or de-identified according to DPDP Act 2023 guidelines",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    (INT_DIR / "int_data_part2.py").write_text("\n".join(lines), encoding="utf-8")
    print("Generated int_data_part2.py")

def build_part3():
    lines = ['"""Phase 15 Canonical Integration Registry - Part 3: ERRORS, MONITORING & SECURITY"""', '']
    
    # 5. INTEGRATION_ERRORS (75 items: ERR-INT-001 to ERR-INT-075)
    lines.append('INTEGRATION_ERRORS = [')
    err_cats = ["TRANSPORT_FAILURE", "AUTHENTICATION_FAILED", "AUTHORIZATION_DENIED", "VALIDATION_ERROR", "TIMEOUT_BREACH", "DEPENDENCY_UNAVAILABLE", "SCHEMA_INCOMPATIBLE", "RATE_LIMIT_EXCEEDED"]
    for i in range(1, 76):
        cat = err_cats[(i - 1) % len(err_cats)]
        retryable = True if cat in ["TRANSPORT_FAILURE", "TIMEOUT_BREACH", "RATE_LIMIT_EXCEEDED", "DEPENDENCY_UNAVAILABLE"] else False
        sev = "CRITICAL" if not retryable else "HIGH"
        strat = "Exponential backoff with jitter (initial 500ms, max 3 retries)" if retryable else "No retry; immediate Dead Letter Queue routing"
        lines.append('    {')
        lines.append(f'        "id": "ERR-INT-{i:03d}",')
        lines.append(f'        "code": "E_INT_{cat}_{i:03d}",')
        lines.append(f'        "category": "{cat}",')
        lines.append(f'        "description": "Integration failure scenario {i:03d} arising during external communication.",')
        lines.append(f'        "severity": "{sev}",')
        lines.append(f'        "retryable": {retryable},')
        lines.append(f'        "retry_strategy": "{strat}",')
        lines.append(f'        "dlq_routing": "arn:aws:sqs:ap-south-1:104857620:dlq-int-{i:03d}",')
        lines.append(f'        "user_impact": "Graceful fallback UI display with automated offline synchronization flag",')
        lines.append(f'        "remediation": "Check external endpoint liveness, verify TLS certificates, and validate request payload schema.",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    # 6. INTEGRATION_MONITORING (75 items: MON-INT-001 to MON-INT-075)
    lines.append('INTEGRATION_MONITORING = [')
    mon_types = ["LATENCY_P95", "ERROR_RATE", "THROUGHPUT_RPS", "QUEUE_DEPTH", "DEAD_LETTER_COUNT", "CERT_EXPIRY_DAYS", "SYNC_LAG_SECONDS"]
    for i in range(1, 76):
        mtype = mon_types[(i - 1) % len(mon_types)]
        lines.append('    {')
        lines.append(f'        "id": "MON-INT-{i:03d}",')
        lines.append(f'        "title": "Integration Monitoring Rule {i:03d} ({mtype})",')
        lines.append(f'        "metric_name": "namma_integration_{mtype.lower()}_{i:03d}",')
        lines.append(f'        "metric_type": "{mtype}",')
        lines.append(f'        "warning_threshold": "{100 + i*5}ms / count > {i*2}",')
        lines.append(f'        "critical_threshold": "{200 + i*10}ms / count > {i*5}",')
        lines.append(f'        "evaluation_window": "5 minutes sliding window",')
        lines.append(f'        "alert_destination": "PagerDuty P1 & Slack #integration-ops-alerts",')
        lines.append(f'        "remediation_runbook": "RUNBOOK-INT-{(i-1)%20+1:03d}",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    # 7. INTEGRATION_SECURITY (50 items: SEC-INT-001 to SEC-INT-050)
    lines.append('INTEGRATION_SECURITY = [')
    sec_types = ["MUTUAL_TLS", "OAUTH_OIDC", "SECRET_ROTATION", "PAYLOAD_ENCRYPTION", "IP_ALLOWLIST", "STRIDE_MITIGATION", "INPUT_SANITIZATION"]
    for i in range(1, 51):
        stype = sec_types[(i - 1) % len(sec_types)]
        lines.append('    {')
        lines.append(f'        "id": "SEC-INT-{i:03d}",')
        lines.append(f'        "title": "Integration Security Control {i:03d} ({stype})",')
        lines.append(f'        "control_type": "{stype}",')
        lines.append(f'        "specification": "Enforces strict {stype} cryptographic verification and access boundary enforcement in compliance with MeitY and DPDP Act 2023.",')
        lines.append(f'        "enforcement_point": "Integration Gateway / AWS WAF / Envoy Proxy Ingress",')
        lines.append(f'        "rotation_cadence": "Automated 30-day credential rotation via AWS Secrets Manager",')
        lines.append(f'        "audit_ledger": "Immutable security log with SHA-256 HMAC signature",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    (INT_DIR / "int_data_part3.py").write_text("\n".join(lines), encoding="utf-8")
    print("Generated int_data_part3.py")

def build_part4():
    lines = ['"""Phase 15 Canonical Integration Registry - Part 4: TESTS, DEPENDENCIES, POLICIES & ENVIRONMENTS"""', '']
    
    # 8. INTEGRATION_TESTS (50 items: TEST-INT-001 to TEST-INT-050)
    lines.append('INTEGRATION_TESTS = [')
    test_types = ["CONTRACT_TEST", "MOCK_GATEWAY_TEST", "CHAOS_LATENCY_TEST", "REPLAY_IDEMPOTENCY_TEST", "SECURITY_VAPT_TEST", "END_TO_END_SYNC_TEST"]
    for i in range(1, 51):
        ttype = test_types[(i - 1) % len(test_types)]
        lines.append('    {')
        lines.append(f'        "id": "TEST-INT-{i:03d}",')
        lines.append(f'        "title": "Integration Test Scenario {i:03d} ({ttype})",')
        lines.append(f'        "test_type": "{ttype}",')
        lines.append(f'        "target_integration": "INT-{(i-1)%100+1:03d}",')
        lines.append(f'        "test_assertion": "Verifies zero data loss, schema adherence, and latency SLA conformance under simulated partner conditions.",')
        lines.append(f'        "mock_framework": "WireMock / Pact Consumer-Driven Contract Runner",')
        lines.append(f'        "execution_gate": "CI/CD Pre-Deployment Gate PR-GATE-{(i-1)%25+1:03d}",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    # 9. INTEGRATION_DEPENDENCIES (50 items: DEP-INT-001 to DEP-INT-050)
    lines.append('INTEGRATION_DEPENDENCIES = [')
    dep_types = ["HARD_BLOCKING", "SOFT_ASYNC", "OPTIONAL_ENRICHMENT", "STATUTORY_MANDATE"]
    for i in range(1, 51):
        dtype = dep_types[(i - 1) % len(dep_types)]
        crit = "TIER_1_CRITICAL" if dtype == "HARD_BLOCKING" else "TIER_2_DEGRADABLE"
        lines.append('    {')
        lines.append(f'        "id": "DEP-INT-{i:03d}",')
        lines.append(f'        "source_integration": "INT-{(i-1)%100+1:03d}",')
        lines.append(f'        "target_system": "EXT-{(i-1)%50+1:03d}",')
        lines.append(f'        "dependency_type": "{dtype}",')
        lines.append(f'        "criticality": "{crit}",')
        lines.append(f'        "failover_mechanism": "Local offline SQLite queue with automatic retry upon reconnection",')
        lines.append(f'        "owner": "squad_integrations_platform",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    # 10. RETRY_POLICIES (25 items: RETRY-001 to RETRY-025)
    lines.append('RETRY_POLICIES = [')
    for i in range(1, 26):
        lines.append('    {')
        lines.append(f'        "id": "RETRY-{i:03d}",')
        lines.append(f'        "name": "exponential_backoff_policy_{i:03d}",')
        lines.append(f'        "initial_interval_ms": {200 + i*50},')
        lines.append(f'        "max_interval_ms": {5000 + i*500},')
        lines.append(f'        "multiplier": 2.0,')
        lines.append(f'        "max_retries": 3,')
        lines.append(f'        "jitter_pct": 20,')
        lines.append(f'        "circuit_breaker_threshold": 5,')
        lines.append(f'        "dead_letter_target": "arn:aws:sqs:ap-south-1:104857620:dlq-retry-{i:03d}",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    # 11. RECONCILIATION_POLICIES (25 items: RECON-001 to RECON-025)
    lines.append('RECONCILIATION_POLICIES = [')
    for i in range(1, 26):
        freq_recon = "DAILY_MIDNIGHT_CHECKPOINT" if i % 2 == 0 else "HOURLY_WINDOW"
        lines.append('    {')
        lines.append(f'        "id": "RECON-{i:03d}",')
        lines.append(f'        "name": "reconciliation_cadence_policy_{i:03d}",')
        lines.append(f'        "frequency": "{freq_recon}",')
        lines.append(f'        "reconciliation_target": "INT-{(i-1)%100+1:03d}",')
        lines.append(f'        "discrepancy_threshold_pct": 0.01,')
        lines.append(f'        "automated_remedy": "Trigger two-way ledger comparison and emit discrepancy audit event",')
        lines.append(f'        "escalation_role": "Zonal Data Steward & Integration Lead",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    # 12. INTEGRATION_ENVIRONMENTS (25 items: ENV-INT-001 to ENV-INT-025)
    lines.append('INTEGRATION_ENVIRONMENTS = [')
    env_names = ["Local-Docker", "Development-Cloud", "QA-Test-Tier", "Staging-UAT", "Pilot-20-Clinics", "Production-450-Clinics"]
    for i in range(1, 26):
        ename = env_names[(i - 1) % len(env_names)]
        mock_val = True if "Local" in ename or "Development" in ename else False
        synth_ratio = 1.0 if "Local" in ename or "Dev" in ename or "QA" in ename else 0.0
        lines.append('    {')
        lines.append(f'        "id": "ENV-INT-{i:03d}",')
        lines.append(f'        "environment_name": "{ename}",')
        lines.append(f'        "gateway_endpoint": "https://gateway-{ename.lower()}.internal.bbmp.gov.in/v1",')
        lines.append(f'        "auth_provider": "Keycloak OIDC Realm {ename}",')
        lines.append(f'        "mock_mode_enabled": {mock_val},')
        lines.append(f'        "synthetic_data_ratio": {synth_ratio},')
        lines.append(f'        "compliance_boundary": "DPDP Sovereign In-State Isolated VPC",')
        lines.append('    },')
    lines.append(']')
    lines.append('')

    (INT_DIR / "int_data_part4.py").write_text("\n".join(lines), encoding="utf-8")
    print("Generated int_data_part4.py")

def build_aggregator():
    lines = [
        '"""Phase 15 Canonical Integration Core Data Aggregator"""',
        '',
        'from scripts.integrations.int_data_part1 import INTEGRATIONS, EXTERNAL_SYSTEMS',
        'from scripts.integrations.int_data_part2 import INTEGRATION_INTERFACES, DATA_MAPPINGS',
        'from scripts.integrations.int_data_part3 import INTEGRATION_ERRORS, INTEGRATION_MONITORING, INTEGRATION_SECURITY',
        'from scripts.integrations.int_data_part4 import (',
        '    INTEGRATION_TESTS, INTEGRATION_DEPENDENCIES, RETRY_POLICIES,',
        '    RECONCILIATION_POLICIES, INTEGRATION_ENVIRONMENTS',
        ')',
        '',
        '__all__ = [',
        '    "INTEGRATIONS",',
        '    "EXTERNAL_SYSTEMS",',
        '    "INTEGRATION_INTERFACES",',
        '    "DATA_MAPPINGS",',
        '    "INTEGRATION_ERRORS",',
        '    "INTEGRATION_MONITORING",',
        '    "INTEGRATION_SECURITY",',
        '    "INTEGRATION_TESTS",',
        '    "INTEGRATION_DEPENDENCIES",',
        '    "RETRY_POLICIES",',
        '    "RECONCILIATION_POLICIES",',
        '    "INTEGRATION_ENVIRONMENTS",',
        ']'
    ]
    (INT_DIR / "integration_core_data.py").write_text("\n".join(lines), encoding="utf-8")
    print("Generated integration_core_data.py")

if __name__ == "__main__":
    build_part1()
    build_part2()
    build_part3()
    build_part4()
    build_aggregator()
