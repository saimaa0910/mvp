#!/usr/bin/env python3
"""
gen_req_08_priv.py
Generates docs/02-requirements/08-privacy-requirements.md
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_priv import PRIV_REQUIREMENTS
from gen_base import generate_document

def render_priv_invariants(r):
    return [
        f"- **DPDP Act Principle:** {r['dpdp_principle']}",
        f"- **Legal Classification:** {r['legal_classification']}",
        f"- **Enforced Privacy Control:** {r['privacy_control']}",
        f"- **Lawful Processing Basis:** {r['lawful_basis']}",
        f"- **Data Subject Rights Impact:** {r['data_subject_rights_impact']}",
        f"- **Audit Evidence Record:** {r['audit_evidence']}"
    ]

def main():
    exec_summary = (
        "This specification defines the authoritative, implementation-ready privacy and data protection requirements "
        "baseline for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. "
        "Comprising 50 comprehensive privacy specifications (`PRIV-001` through `PRIV-050`), this document operationalizes the legal "
        "and ethical mandates of India's Digital Personal Data Protection (DPDP) Act 2023, the DISHA guidelines, and the National Health "
        "Authority (NHA) ABDM consent framework.\n\n"
        "Every privacy requirement establishes an explicit lawful basis for processing, purposeful data minimization bounds, "
        "strict retention and automatic purging schedules, granular patient consent mechanisms, data subject rights "
        "(access, correction, erasure, withdrawal), and privacy-preserving de-identification/k-anonymity for public health epidemiology."
    )

    mermaid_diagram = """graph TD
    subgraph PatientNotice["Notice & Consent Tier"]
        NOTICE["Bilingual Notice (Kannada/English) | Plain Language"]
        CONSENT["Granular DPDP Consent Capture | Digital Thumbprint/Signature"]
    end
    subgraph Processing["Lawful Processing & Boundary Control"]
        PURPOSE["Purpose Limitation | Clinical Care vs Epidemiology"]
        MIN["Data Minimization | Redacted PII on Public Views"]
    end
    subgraph Governance["Rights & Lifecycle Vault"]
        RIGHTS["Data Subject Rights: Access | Rectification | Erasure"]
        ANON["k-Anonymity (k>=5) | Differential Privacy Engine"]
        PURGE["Automated Retention Enforcer | Cryptographic Erasure"]
    end
    NOTICE --> CONSENT --> PURPOSE --> MIN --> RIGHTS
    PURPOSE --> ANON
    MIN --> PURGE"""

    domain_cols = ("DPDP Domain", "Priority", "Lawful Processing Basis", "Enforced Privacy Control", "Audit Evidence")
    extractors = [
        lambda r: f"`{r['domain']}`",
        lambda r: f"`{r['priority']}`",
        lambda r: f"{r['lawful_basis'][:35]}...",
        lambda r: f"{r['privacy_control'][:40]}...",
        lambda r: f"{r['audit_evidence'][:30]}..."
    ]

    governance = (
        "This Privacy Requirements Specification defines the binding privacy standard for the Namma Clinic Platform. "
        "All data pipelines, client-side caching stores, and analytical views are audited continuously for compliance with DPDP Act 2023 regulations. "
        "Any data schema changes introducing new PII elements require formal sign-off by the Data Protection Officer (DPO)."
    )

    generate_document(
        doc_num="08",
        doc_slug="08-privacy-requirements.md",
        doc_id="DOC-REQ-008-PRIV",
        doc_title="Privacy & Data Protection Requirements Baseline",
        req_type="Privacy Requirement",
        req_range="PRIV-001 through PRIV-050",
        count=50,
        requirements=PRIV_REQUIREMENTS,
        exec_summary=exec_summary,
        mermaid_diagram=mermaid_diagram,
        domain_table_cols=domain_cols,
        domain_col_extractors=extractors,
        domain_invariant_renderer=render_priv_invariants,
        governance_text=governance,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="07-security-requirements.md"
    )

if __name__ == "__main__":
    main()
