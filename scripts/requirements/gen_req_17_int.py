#!/usr/bin/env python3
"""
gen_req_17_int.py
Generates docs/02-requirements/17-integration-requirements.md
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_int import INT_REQUIREMENTS
from gen_base import generate_document

def render_int_invariants(r):
    return [
        f"- **External Interoperability System:** {r['external_system']}",
        f"- **Integration Protocol:** `{r['integration_protocol']}`",
        f"- **Payload & Schema Standard:** `{r['payload_standard']}`",
        f"- **Verification Protocol:** {r['verification_method']}",
        f"- **Accountable Integration Lead:** {r['owner']}"
    ]

def main():
    exec_summary = (
        "This specification defines the comprehensive external interoperability, national digital health exchange (ABDM), "
        "disease surveillance sync (IHIP), and clinical peripheral hardware integration requirements baseline for the Namma Clinic "
        "Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. Comprising 50 rigorous integration "
        "specifications (`INT-001` through `INT-050`), this document establishes the protocol boundaries, mutual TLS authentication, "
        "FHIR R4 resource mapping, and hardware device communication standards.\n\n"
        "Key integration frontiers include the Ayushman Bharat Digital Mission (ABDM Milestones 1, 2, 3), Integrated Health Information "
        "Platform (IHIP Form P), Nikshay TB surveillance, Web Serial thermal printing (ESC/POS), USB barcode scanners, and point-of-care "
        "diagnostic analyzers."
    )

    mermaid_diagram = """graph TD
    subgraph NationalEcosystem["National Health Stack (ABDM / MoHFW)"]
        ABHA["ABDM M1: ABHA Registration (Aadhaar/Mobile OTP)"]
        HIP["ABDM M2: Health Information Provider (FHIR R4)"]
        HIU["ABDM M3: Health Information User (Consent & ECDH)"]
        IHIP["IHIP / NCDC: Form P Syndromic Surveillance"]
        NIKSHAY["Nikshay TB Notification & Registry"]
    end
    subgraph GatewayAdapter["Namma Clinic Integration Gateway"]
        AUTH["mTLS & OAuth 2.0 Token Exchange"]
        FHIR_MAP["FHIR R4 Profile Transformer"]
        CIRCUIT["Circuit Breaker & Exponential Backoff Queue"]
        AUTH --> FHIR_MAP --> CIRCUIT
    end
    subgraph ClinicHardware["Frontline Hardware Peripherals"]
        PRINTER["ESC/POS Thermal Printer (Web Serial API)"]
        BARCODE["1D/2D Barcode Scanner (USB HID)"]
        DIAGNOSTIC["POC Glucometer / Hemoglobinometer (Serial/BT)"]
    end
    NationalEcosystem <--> GatewayAdapter
    GatewayAdapter <--> ClinicHardware"""

    domain_cols = ("Target System", "Priority", "Protocol", "Payload Standard", "Integration Lead")
    extractors = [
        lambda r: f"`{r['external_system'][:25]}`",
        lambda r: f"`{r['priority']}`",
        lambda r: f"`{r['integration_protocol'][:25]}`",
        lambda r: f"{r['payload_standard'][:30]}...",
        lambda r: f"{r['owner']}"
    ]

    governance = (
        "This Integration Requirements Specification establishes the binding interoperability standard. "
        "All external transmissions must satisfy national security and privacy guidelines under ABDM and DISHA. "
        "Pact-based contract testing runs continuously in CI to prevent breaking schema changes across ecosystem upgrades."
    )

    generate_document(
        doc_num="17",
        doc_slug="17-integration-requirements.md",
        doc_id="DOC-REQ-017-INT",
        doc_title="Integration Requirements & Interoperability Baseline",
        req_type="Integration Requirement",
        req_range="INT-001 through INT-050",
        count=50,
        requirements=INT_REQUIREMENTS,
        exec_summary=exec_summary,
        mermaid_diagram=mermaid_diagram,
        domain_table_cols=domain_cols,
        domain_col_extractors=extractors,
        domain_invariant_renderer=render_int_invariants,
        governance_text=governance,
        parent_baseline="02-functional-requirements.md",
        counterpart="07-security-requirements.md"
    )

if __name__ == "__main__":
    main()
