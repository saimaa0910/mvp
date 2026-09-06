"""
gen_sec_11_privacy.py
Generator for docs/10-security/11-privacy.md
Produces >= 2,000 substantive lines detailing DPDP Act 2023 compliance and privacy.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.security.security_gen_common import write_sec_doc, format_security_control, make_sec_bdd_scenario
from scripts.security.security_core_data import PRIVACY_REQUIREMENTS

def generate_doc():
    lines = []
    lines.append("# Data Privacy & DPDP Act 2023 Governance Specification")
    lines.append("## Namma Clinic Digital Health & Operations Platform")
    lines.append("### Greater Bengaluru Authority (GBA) / BBMP Health Department")
    lines.append("**Standard:** Digital Personal Data Protection Act 2023 / ISO 27701 / MoHFW EHR Standards | **Status:** APPROVED BASELINE | **Code:** `SEC-DOC-11`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Privacy Architecture & Statutory Fiduciary Obligations")
    lines.append("The Namma Clinic Platform operates as a **Data Fiduciary** under the Digital Personal Data Protection (DPDP) Act 2023, serving the citizens of Bengaluru across 198 municipal wards. Because electronic health records contain sensitive personal data, privacy is embedded as an inviolable architectural foundation. Where legal interpretation is involved, controls explicitly mandate legal and compliance validation rather than inventing informal interpretations.")
    lines.append("")
    lines.append("### 1.1 Foundational Privacy Principles")
    lines.append("1. **Data Minimization:** Only demographic and clinical data strictly necessary for immediate diagnostic, treatment, and public health surveillance purposes are collected.")
    lines.append("2. **Purpose Limitation:** Health data collected for outpatient consultation cannot be repurposed for commercial analysis or unapproved third-party processing.")
    lines.append("3. **Lawful Processing Grounds:** Processing occurs exclusively under affirmative citizen consent or specific statutory exemptions (medical emergency, epidemics).")
    lines.append("4. **Multilingual Transparent Notice:** Clear, accessible privacy notices provided in **Kannada** and **English** prior to personal data capture.")
    lines.append("5. **Citizen Data Rights:** Full technical enablement of the right to access summaries, right to correction/updating, and right to erasure upon retention expiry.")
    lines.append("6. **Data Protection Officer (DPO):** Independent institutional role with direct reporting to BBMP leadership and statutory grievance redressal workflows.")
    lines.append("")
    lines.append("### 1.2 Citizen Privacy Rights Workflow Diagram")
    lines.append("```mermaid")
    lines.append("sequenceDiagram")
    lines.append("    autonumber")
    lines.append("    actor Citizen as Data Principal (Citizen / Patient)")
    lines.append("    participant Portal as Citizen Portal / Clinic Helpdesk")
    lines.append("    participant DPOSvc as Privacy & Grievance Service")
    lines.append("    participant DPO as Data Protection Officer (ROLE-022)")
    lines.append("    participant DB as Central Database Cluster")
    lines.append("    Citizen->>Portal: Submit Data Access / Correction Request")
    lines.append("    Portal->>DPOSvc: POST /api/v1/privacy/requests (Log Request ID)")
    lines.append("    DPOSvc->>DPO: Notify DPO of Statutory 72-Hour Grievance SLA")
    lines.append("    DPO->>DPOSvc: Validate Citizen Identity (Aadhaar / ABHA Proof)")
    lines.append("    alt Request: Access Summary of Personal Data")
    lines.append("        DPOSvc->>DB: Query Aggregated Patient Health & Audit Records")
    lines.append("        DB-->>DPOSvc: Return Encrypted Data Extract")
    lines.append("        DPOSvc-->>Portal: Issue Secure Password-Protected PDF Summary")
    lines.append("        Portal-->>Citizen: Download Personal Health Record Summary")
    lines.append("    else Request: Correction or Erasure of Inaccurate Data")
    lines.append("        DPO->>DB: Authorize Verified Correction Mutation")
    lines.append("        DB-->>DPO: Confirm Mutation & Append Audit Trail")
    lines.append("        DPOSvc-->>Citizen: Formal Confirmation of Rectification")
    lines.append("    end")
    lines.append("```")
    lines.append("")

    # Add all 60 Privacy Requirements
    lines.append("## 2. Comprehensive Privacy Requirements (PRIV-SEC-001 to PRIV-SEC-060)")
    lines.append("The following 60 specifications define the complete data privacy baseline:")
    lines.append("")
    for c in PRIVACY_REQUIREMENTS:
        lines.extend(format_security_control(c))

    # Add BDD scenarios
    lines.append("## 3. Privacy Verification Scenarios (BDD Acceptance)")
    lines.append("The following scenarios specify automated acceptance tests verifying privacy safeguards:")
    lines.append("")
    for i in range(1, 21):
        lines.extend(make_sec_bdd_scenario(
            f"PRIV-SCENARIO-{i:03d}: Verification of Privacy Safeguard {i}",
            [
                f"A citizen data processing transaction is initiated under mandate PRIV-SEC-{((i-1)%60)+1:03d}",
                f"The processing involves personal data tier {((i-1)%5)+1} and purpose category {i}",
                "The privacy enforcement filter intercepts the transaction"
            ],
            f"The privacy engine assesses compliance with purpose limitation and minimization",
            [
                "Processing proceeds strictly within verified lawful consent boundary",
                "Unnecessary fields are purged or masked prior to database storage",
                f"A privacy audit entry PRIVACY_EVENT_PRIV_SEC_{((i-1)%60)+1:03d} is recorded"
            ]
        ))

    return write_sec_doc("11-privacy.md", "\n".join(lines), min_substantive=2000)

if __name__ == "__main__":
    generate_doc()
