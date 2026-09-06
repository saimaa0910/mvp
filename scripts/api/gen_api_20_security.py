"""
gen_api_20_security.py
Generator for docs/08-api/20-api-security.md
Produces >= 2,100 substantive lines defining zero-trust API security, JWT/JWKS,
mTLS, RBAC/ABAC, break-glass emergency protocols, OWASP API Top 10, and DPDP Act compliance.
"""

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.api.api_gen_common import write_api_doc, make_openapi_snippet, make_bdd_scenario
from scripts.api.api_core_data import API_ENDPOINTS

def generate_doc():
    lines = []
    lines.append("# 🔌 API Specification: Zero-Trust API Security, IAM & Data Protection")
    lines.append("## Namma Clinic Digital Health & Operations Platform")
    lines.append("**Document Code:** API-DOC-20 | **Status:** Authoritative Baseline | **Date:** September 2026")
    lines.append("> **Municipal Health Authority:** Greater Bengaluru Authority (GBA) / BBMP Health Department")
    lines.append("> **Standard Framework:** NIST SP 800-207 (Zero Trust), RFC 7519 (JWT), OWASP API Security Top 10 (2023), DPDP Act 2023")
    lines.append("> **Notice:** All code snippets contained herein are strictly **DOCUMENTATION-ONLY OPENAPI** or **DOCUMENTATION-ONLY EXAMPLE**. Zero application runtime code is executed in this phase.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 1. Executive Summary & Zero-Trust Architecture
    lines.append("## 1. Executive Summary & Zero-Trust Architectural Principles")
    lines.append("")
    lines.append("The Namma Clinic security architecture operates under strict **Zero Trust** principles: *never trust, always verify*. Frontline clinic terminals, edge mini-servers, cloud microservices, and external national health grids must explicitly authenticate and authorize every network transaction. Perimeter defense alone is recognized as insufficient; every API endpoint enforces cryptographic verification, least privilege authorization, hardware-bound identity, and tamper-evident audit logging.")
    lines.append("")
    lines.append("### 1.1 Core Security Invariants")
    lines.append("1. **Cryptographic Identity for All Actors:** Every actor—whether a clinic doctor, triage nurse, edge appliance, or national bridge—must present cryptographically verified credentials (RS256 JWT, mTLS X.509 certificate, or Ed25519 payload signature).")
    lines.append("2. **Hardware Device Binding:** Clinical workstations and tablets are enrolled with unique hardware fingerprints and issued device-bound mTLS client certificates, preventing credential reuse from unmanaged personal devices.")
    lines.append("3. **Contextual ABAC Scoping:** RBAC permissions are strictly evaluated within dynamic ABAC boundaries: clinic facility ID, active shift roster, treating clinician relationship, and citizen consent directives.")
    lines.append("4. **Envelope & Column-Level Encryption:** Sensitive medical progress notes, HIV/STI diagnoses, psychiatric records, and national identifiers are encrypted at rest using AES-256-GCM envelope encryption with keys managed in HashiCorp Vault.")
    lines.append("5. **Continuous Threat Mitigation:** Automated defenses against OWASP API Security Top 10 risks are active at the WAF, API gateway, and microservice layers.")
    lines.append("")

    # 2. Zero-Trust Gateway Architecture Diagram
    lines.append("## 2. Zero-Trust Policy Enforcement Topology")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph TB")
    lines.append("    subgraph FrontlineWorkstation[\"Clinic Frontline Device\"]")
    lines.append("        PWA[\"Clinic PWA Shell\"]")
    lines.append("        mTLSKey[\"Hardware TPM / Keystore Private Key\"]")
    lines.append("    end")
    lines.append("")
    lines.append("    subgraph Perimeter[\"Edge & Cloud Ingress Layer\"]")
    lines.append("        mTLSTerm[\"mTLS 1.3 Termination & Fingerprint Match\"]")
    lines.append("        WAF[\"Cloud WAF & DDoS Shield\"]")
    lines.append("        APIGW[\"API Gateway (PEP - Policy Enforcement Point)\"]")
    lines.append("    end")
    lines.append("")
    lines.append("    subgraph ControlPlane[\"Security & Policy Control Plane\"]")
    lines.append("        IAM[\"IAM Token Authority\"]")
    lines.append("        Vault[\"HashiCorp Vault KMS\"]")
    lines.append("        OPA[\"Open Policy Agent (PDP - Policy Decision Point)\"]")
    lines.append("        Redis[\"Redis Token Revocation & Rate Cache\"]")
    lines.append("    end")
    lines.append("")
    lines.append("    subgraph CoreServices[\"Protected Domain Microservices\"]")
    lines.append("        EMR[\"Clinical EMR Service\"]")
    lines.append("        Pharm[\"Pharmacy & Stock Service\"]")
    lines.append("        Audit[\"WORM Audit Service\"]")
    lines.append("    end")
    lines.append("")
    lines.append("    PWA --> mTLSTerm")
    lines.append("    mTLSKey -.->|Client Cert| mTLSTerm")
    lines.append("    mTLSTerm --> WAF")
    lines.append("    WAF --> APIGW")
    lines.append("    APIGW -->|Check Token Expiry & Revocation| Redis")
    lines.append("    APIGW -->|Evaluate RBAC + ABAC Policy| OPA")
    lines.append("    APIGW -->|Verify RS256 Signature| IAM")
    lines.append("    APIGW -->|Forward with Internal Identity Token| CoreServices")
    lines.append("    CoreServices -->|Fetch Column Encryption Keys| Vault")
    lines.append("    CoreServices -->|Async Append Audit Record| Audit")
    lines.append("```")
    lines.append("")

    # 3. Authentication Framework & JWT/JWKS Standards
    lines.append("## 3. Authentication Standards: RS256 JWT, JWKS & Session Rotation")
    lines.append("")
    lines.append("### 3.1 JWT Claims Structure")
    lines.append("All authenticated access tokens are compact RS256-signed JSON Web Tokens conforming to the following claim schema:")
    lines.append("```json")
    lines.append("// DOCUMENTATION-ONLY EXAMPLE")
    lines.append("{")
    lines.append("  \"iss\": \"https://auth.nammaclinic.bbmp.gov.in\",")
    lines.append("  \"sub\": \"018e3a20-0005-7000-8000-000000000001\",")
    lines.append("  \"aud\": \"https://api.nammaclinic.bbmp.gov.in\",")
    lines.append("  \"jti\": \"018e3a20-8000-7000-8000-000000000001\",")
    lines.append("  \"iat\": 1767225600,")
    lines.append("  \"nbf\": 1767225600,")
    lines.append("  \"exp\": 1767226500,")
    lines.append("  \"user\": {")
    lines.append("    \"username\": \"DOC-BLR-1024\",")
    lines.append("    \"displayName\": \"Dr. Ramesh Kumar\",")
    lines.append("    \"medicalRegistrationNumber\": \"KMC-19842\",")
    lines.append("    \"primaryRole\": \"ROLE-002\",")
    lines.append("    \"assignedRoles\": [\"ROLE-002\", \"ROLE-016\"]")
    lines.append("  },")
    lines.append("  \"context\": {")
    lines.append("    \"facilityId\": \"018e3a20-0008-7000-8000-000000000001\",")
    lines.append("    \"facilityWard\": 142,")
    lines.append("    \"shiftId\": \"018e3a20-0010-7000-8000-000000000001\",")
    lines.append("    \"deviceFingerprint\": \"tab-n100-blr-042\",")
    lines.append("    \"breakGlassActive\": false")
    lines.append("  },")
    lines.append("  \"permissions\": [")
    lines.append("    \"consultations:read\",")
    lines.append("    \"consultations:create\",")
    lines.append("    \"prescriptions:create\",")
    lines.append("    \"lab_orders:create\"")
    lines.append("  ]")
    lines.append("}")
    lines.append("```")
    lines.append("")

    # 4. Emergency Clinical Break-Glass Protocol
    lines.append("## 4. Emergency Clinical Break-Glass Access Architecture")
    lines.append("")
    lines.append("In life-threatening medical emergencies (e.g., unconscious patient, acute trauma), treating physicians require instantaneous access to the patient's longitudinal record, allergies, and chronic conditions—even if citizen consent has not been granted or normal facility scoping restrictions would block access.")
    lines.append("")
    lines.append("```mermaid")
    lines.append("sequenceDiagram")
    lines.append("    autonumber")
    lines.append("    participant Doc as Medical Officer (ROLE-002)")
    lines.append("    participant UI as Doctor Tablet UI")
    lines.append("    participant Auth as IAM Service (/break-glass)")
    lines.append("    participant EMR as Patient EMR")
    lines.append("    participant Alert as Emergency Broadcast")
    lines.append("    participant Audit as Cryptographic WORM Audit")
    lines.append("")
    lines.append("    Doc->>UI: Select 'EMERGENCY BREAK-GLASS OVERRIDE'")
    lines.append("    UI->>Doc: Prompt for Patient UHID & Clinical Justification")
    lines.append("    Doc->>UI: Enter Justification ('Patient unconscious, acute cardiac distress')")
    lines.append("    UI->>Auth: POST /api/v1/auth/break-glass (UHID, Justification)")
    lines.append("    Auth->>Auth: Verify Doctor Credentials & Active Medical License")
    lines.append("    Auth->>Audit: Append Break-Glass Audit Event (HMAC Block)")
    lines.append("    Auth->>Alert: Broadcast Alert to Medical Superintendent & Privacy Officer")
    lines.append("    Auth-->>UI: Issue Elevated 2-Hour Break-Glass JWT Token")
    lines.append("    UI->>EMR: Fetch Full Clinical Dossier with Break-Glass JWT")
    lines.append("    EMR-->>UI: Return Medical History, Allergies, Active Regimens")
    lines.append("    Note over Alert,Audit: Formal 24-Hour Review Triggered for Legal Compliance")
    lines.append("```")
    lines.append("")

    # 5. OWASP API Security Top 10 Mitigation Matrix
    lines.append("## 5. OWASP API Security Top 10 (2023) Mitigation Controls")
    lines.append("")
    owasp_rules = [
        ("API1:2023 - Broken Object Level Authorization (BOLA)", "Every endpoint verifies that requested object belongs to caller's facility context or treating clinician relationship. Synthetic IDs use UUIDv7; direct sequential IDs forbidden."),
        ("API2:2023 - Broken Authentication", "Argon2id password hashing, RS256 JWTs with 15m expiration, sliding-window rate limiting on login, automated account lockout after 5 consecutive failures, mTLS client certificates on workstations."),
        ("API3:2023 - Broken Object Property Level Authorization", "Strict JSON schema validation at gateway; mass assignment prohibited via explicit DTO mapping; response filters strip internal fields (hashes, raw tokens) based on caller role."),
        ("API4:2023 - Unrestricted Resource Consumption", "Token bucket rate limiting per IP and user; strict payload size limits (max 10MB); mandatory cursor pagination on all collection endpoints (default 25, max 100)."),
        ("API5:2023 - Broken Function Level Authorization", "Unified Open Policy Agent (OPA) middleware checks required permission tokens before invoking controllers; admin endpoints isolated on private ingress routes."),
        ("API6:2023 - Unrestricted Access to Sensitive Business Flows", "Critical flows (patient registration, medication dispensing, stock deduction) require X-Idempotency-Key deduplication, transaction locks, and CAPTCHA / rate guards on public portals."),
        ("API7:2023 - Server Side Request Forgery (SSRF)", "All outbound HTTP integrations (SMS gateway, ABDM national router) use fixed DNS egress proxies; user-controlled callback URLs are strictly prohibited."),
        ("API8:2023 - Security Misconfiguration", "All development debug endpoints disabled in production; TLS 1.3 enforced with HSTS (max-age=31536000); detailed stack traces replaced by standard error envelopes matching SCHEMA-API-003."),
        ("API9:2023 - Improper Inventory Management", "Every active endpoint documented in OpenAPI 3.1 baseline; retired endpoints decommissioned via RFC 8594 Sunset headers; shadow APIs prevented by strict gateway route registries."),
        ("API10:2023 - Unsafe Consumption of APIs", "All external data received from national ABDM gateways or carrier SMS webhooks is validated against strict JSON schemas and sanitized before relational persistence.")
    ]
    lines.append("| OWASP Risk Identifier | Platform Defensive Control Implementation | Architectural Enforcement Layer |")
    lines.append("| :--- | :--- | :--- |")
    for rname, rctrl in owasp_rules:
        lines.append(f"| **{rname}** | {rctrl} | Central Gateway + Microservice OPA Guard |")
    lines.append("")

    # 6. Complete Endpoint Security Catalog Table
    lines.append("## 6. Comprehensive Endpoint Security & RBAC Enforcement Catalog")
    lines.append("")
    lines.append("Authoritative security profiles for all 341 platform endpoints:")
    lines.append("")
    lines.append("| Endpoint ID | Route Path | Auth Requirement | Primary RBAC Token | ABAC Context Guard | Security Classification |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for ep in API_ENDPOINTS:
        perm = ep["rbac_permissions"][0] if ep["rbac_permissions"] else "Public / Anonymous"
        lines.append(f"| **{ep['id']}** | `{ep['method']} {ep['path']}` | `{ep['auth']}` | `{perm}` | {ep['abac_rules']} | `{ep['classification']}` |")
    lines.append("")

    # 7. Exhaustive Threat Modeling & OpenAPI Security Specs for Core Endpoints
    lines.append("## 7. Endpoint-Specific Threat Modeling & Defensive Invariants")
    lines.append("")
    lines.append("Detailed threat model, OWASP vectors, and OpenAPI security definitions for primary operational endpoints:")
    lines.append("")
    for i, ep in enumerate(API_ENDPOINTS[:45]):
        lines.append(f"### 7.{i+1} Threat Model: `{ep['id']}` ({ep['title']})")
        lines.append(f"- **Protected Route:** `{ep['method']} {ep['path']}`")
        lines.append(f"- **Functional Domain:** `{ep['domain']}` | **Classification:** `{ep['classification']}`")
        lines.append(f"- **Authentication Standard:** `{ep['auth']}`")
        lines.append(f"- **Required RBAC Scope:** `{', '.join(ep['rbac_permissions']) if ep['rbac_permissions'] else 'None (Public Ingress)'}`")
        lines.append(f"- **Enforced ABAC Boundary:** {ep['abac_rules']}")
        lines.append(f"- **Primary Threat Vectors:** BOLA tampering with URL path parameters, credential replay attacks, rate quota exhaustion.")
        lines.append(f"- **Defensive Gateway Policy:** OPA pre-routing filter checks caller facility matching target entity record; rate limiter enforces `{ep['rate_limit']}`.")
        lines.append(f"- **Cryptographic Audit Action:** On mutation or sensitive view, appends `{ep['audit_event']}` with caller user ID, IP address, and correlation ID.")
        lines.append("")
        lines.append("#### OpenAPI Security Specification")
        sec_snippet = make_openapi_snippet(ep["method"], ep["path"], f"Secure {ep['title']}", [ep["domain"]], req_schema=ep["req_schema"], resp_schema=ep["resp_schema"], status_codes=[200, 401, 403, 429])
        lines.extend(sec_snippet)
        lines.append("")

    # 8. Cryptographic Key Management & Storage Security
    lines.append("## 8. Cryptographic Key Management & Data Protection Lifecycle")
    lines.append("")
    lines.append("The platform implements multi-layered encryption in compliance with DPDP Act Section 8:")
    lines.append("- **Data in Transit:** TLS 1.3 mandatory across all public and internal interfaces. Permitted cipher suites: `TLS_AES_256_GCM_SHA384` and `TLS_CHACHA20_POLY1305_SHA256`. TLS 1.0, 1.1, and 1.2 are disabled.")
    lines.append("- **Data at Rest:** Transparent Data Encryption (TDE) at filesystem layer (LUKS / dm-crypt) combined with column-level AES-256-GCM encryption for sensitive demographic and clinical columns.")
    lines.append("- **Key Rotation Schedule:** Root KMS keys in HashiCorp Vault rotated annually; JWKS token signing keys rotated every 90 days; database connection credentials rotated every 30 days via automated Vault agent.")
    lines.append("")

    # 9. BDD Security Acceptance Criteria
    lines.append("## 9. Security Quality Acceptance Criteria (BDD)")
    lines.append("")
    bdd_sec1 = make_bdd_scenario(
        "Prevent BOLA Access to Patient Record in Different Facility",
        ["an authenticated clinical user assigned strictly to Facility A (Ward 142)", "requesting medical history for a patient registered exclusively at Facility B (Ward 180) without clinical referral"],
        "the clinician sends GET /api/v1/patients/{patientId}/history",
        ["the OPA authorization engine evaluates facility boundaries", "the API gateway rejects the request with HTTP 403 Forbidden", "returns error code 'ERR-AUTH-007'", "emits a security violation audit alert to the WORM log"]
    )
    lines.extend(bdd_sec1)
    lines.append("")

    bdd_sec2 = make_bdd_scenario(
        "Authorize Emergency Break-Glass Access with Mandatory Audit",
        ["an authenticated treating doctor facing an emergency resuscitation encounter", "submitting valid clinical justification to /api/v1/auth/break-glass"],
        "the doctor submits the break-glass request",
        ["the IAM service verifies active clinician credentials", "issues an elevated 2-hour break-glass JWT token", "emits an immutable audit block to the WORM ledger", "dispatches an urgent broadcast to the Medical Superintendent", "allows temporary read access to the patient's critical clinical records"]
    )
    lines.extend(bdd_sec2)
    lines.append("")

    content = "\n".join(lines)
    return write_api_doc("20-api-security.md", content)

if __name__ == "__main__":
    stats = generate_doc()
    print("Done 20-api-security.md:", stats)
