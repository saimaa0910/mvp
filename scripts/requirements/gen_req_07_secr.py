#!/usr/bin/env python3
"""
gen_req_07_secr.py
Generates docs/02-requirements/07-security-requirements.md
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_secr import SECR_REQUIREMENTS
from gen_base import generate_document

def render_secr_invariants(r):
    return [
        f"- **Threat Vector:** {r['threat_description']}",
        f"- **Attack Scenario Simulation:** {r['attack_scenario']}",
        f"- **Enforced Security Control:** {r['security_control']}",
        f"- **Implementation Expectation:** {r['implementation_expectation']}",
        f"- **Verification Protocol:** {r['verification_method']}",
        f"- **Audit Evidence Vault:** {r['audit_evidence']}"
    ]

def main():
    exec_summary = (
        "This specification defines the comprehensive, implementation-ready security requirements baseline "
        "for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. "
        "Comprising 50 rigorous, verifiable security specifications (`SECR-001` through `SECR-050`), this document "
        "establishes mandatory cryptographic invariants, role-based and attribute-based access controls, session hardening, "
        "defense-in-depth mitigations against OWASP Top 10 vulnerabilities, immutable audit trails, and strict software "
        "supply chain security controls.\n\n"
        "All technical specifications comply with the Digital Information Security in Healthcare Act (DISHA) guidelines, "
        "CERT-In cybersecurity directives, National Health Authority (NHA) ABDM security architecture, and ISO/IEC 27001 standards."
    )

    mermaid_diagram = """graph TD
    subgraph Perimeter["Perimeter & Transport Security"]
        WAF["Cloud WAF | Rate Limiter | DDoS Mitigation"]
        TLS["TLS 1.3 Transport Encryption | HSTS | Forward Secrecy"]
    end
    subgraph Identity["Identity & Access Governance"]
        AUTH["Argon2id Passwords | TOTP MFA | Brute-Force Shield"]
        RBAC["Dual-Layer RBAC | Fine-Grained Least Privilege"]
        JWT["Short-Lived RS256 JWTs | Redis Token Revocation"]
    end
    subgraph Storage["Storage & Cryptographic Controls"]
        DB_ENC["PostgreSQL AES-256-GCM Transparent Data Encryption"]
        CLIENT_ENC["Web Cryptography AES-256 Client IndexedDB Encryption"]
        WORM["Immutable Audit Vault | HMAC-SHA256 Chaining"]
    end
    WAF --> TLS --> AUTH --> RBAC --> JWT --> DB_ENC
    AUTH -.-> WORM
    CLIENT_ENC -.-> WORM"""

    domain_cols = ("Threat Category", "Priority", "Threat Vector", "Security Control", "Verification Method")
    extractors = [
        lambda r: f"`{r['domain']}`",
        lambda r: f"`{r['priority']}`",
        lambda r: f"{r['threat_description'][:35]}...",
        lambda r: f"{r['security_control'][:40]}...",
        lambda r: f"{r['verification_method'][:30]}..."
    ]

    governance = (
        "This Security Requirements Specification represents the non-negotiable security baseline for the Namma Clinic Platform. "
        "All commits, pull requests, and container images are validated against automated SAST/DAST/Secret scanning tools in CI. "
        "Zero critical or high vulnerabilities are permitted in production artifacts. Any exception requires written sign-off by the CISO."
    )

    generate_document(
        doc_num="07",
        doc_slug="07-security-requirements.md",
        doc_id="DOC-REQ-007-SECR",
        doc_title="Security Requirements Specification & Cryptographic Controls Baseline",
        req_type="Security Requirement",
        req_range="SECR-001 through SECR-050",
        count=50,
        requirements=SECR_REQUIREMENTS,
        exec_summary=exec_summary,
        mermaid_diagram=mermaid_diagram,
        domain_table_cols=domain_cols,
        domain_col_extractors=extractors,
        domain_invariant_renderer=render_secr_invariants,
        governance_text=governance,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="08-privacy-requirements.md"
    )

if __name__ == "__main__":
    main()
