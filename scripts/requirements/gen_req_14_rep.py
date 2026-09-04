#!/usr/bin/env python3
"""
gen_req_14_rep.py
Generates docs/02-requirements/14-reporting-requirements.md
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_rep import REP_REQUIREMENTS
from gen_base import generate_document

def render_rep_invariants(r):
    return [
        f"- **Reporting Cadence / Frequency:** {r['report_frequency']}",
        f"- **Target Operational Audience:** {r['target_audience']}",
        f"- **Underlying Data Sources:** `{r['data_sources']}`",
        f"- **Supported Export Formats:** {r['export_formats']}",
        f"- **Verification Protocol:** {r['verification_method']}",
        f"- **Accountable Reporting Owner:** {r['owner']}"
    ]

def main():
    exec_summary = (
        "This specification defines the comprehensive operational, clinical, inventory, epidemiological, and statutory "
        "reporting requirements baseline for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers "
        "in Greater Bengaluru. Comprising 50 exhaustive reporting specifications (`REP-001` through `REP-050`), this document establishes "
        "the automated calculation formulas, aggregation cadences, export formats (PDF, CSV, Excel), and RBAC access permissions for all "
        "municipal health oversight workflows.\n\n"
        "From daily OPD footfall and 120 Essential Drug List (EDL) stockout escalations to statutory IHIP Form P syndromic surveillance "
        "and monthly BBMP Form M consolidation, every report is designed to guarantee administrative transparency, clinical auditability, "
        "and public health accountability."
    )

    mermaid_diagram = """graph TD
    subgraph DataSources["Transactional & Analytical Data Sources"]
        OPD["OPD & Token Tables"]
        RX["Prescription & EDL Inventory"]
        LAB["Lab Diagnostic Orders"]
        SURV["Syndromic Clinical Encounters"]
    end
    subgraph ReportEngine["Automated Reporting Pipeline"]
        CRON["Scheduled Cron & EOD Trigger Engine"]
        AGG["Aggregation & Calculation Processor"]
        MASK["Privacy Masking & k-Anonymity Guard"]
        CRON --> AGG --> MASK
    end
    subgraph Distribution["Multi-Channel Distribution"]
        PDF["Cryptographically Signed PDF"]
        CSV["Structured CSV / Excel Stream"]
        DASH["Live Supervisory Dashboard"]
        SMS["Automated SMS/Email Escalation"]
    end
    DataSources --> ReportEngine --> Distribution"""

    domain_cols = ("Reporting Cadence", "Priority", "Target Audience", "Export Formats", "Owner")
    extractors = [
        lambda r: f"`{r['report_frequency']}`",
        lambda r: f"`{r['priority']}`",
        lambda r: f"{r['target_audience'][:30]}...",
        lambda r: f"`{r['export_formats'][:20]}`",
        lambda r: f"{r['owner']}"
    ]

    governance = (
        "This Reporting Requirements Specification establishes the binding operational and statutory reporting baseline. "
        "All reporting aggregation queries are validated against daily physical audit tallies to guarantee 100% financial and inventory reconciliation. "
        "Any modifications to statutory report formats require prior approval from the BBMP Health Directorate."
    )

    generate_document(
        doc_num="14",
        doc_slug="14-reporting-requirements.md",
        doc_id="DOC-REQ-014-REP",
        doc_title="Reporting Requirements & Statutory Health Register Baseline",
        req_type="Reporting Requirement",
        req_range="REP-001 through REP-050",
        count=50,
        requirements=REP_REQUIREMENTS,
        exec_summary=exec_summary,
        mermaid_diagram=mermaid_diagram,
        domain_table_cols=domain_cols,
        domain_col_extractors=extractors,
        domain_invariant_renderer=render_rep_invariants,
        governance_text=governance,
        parent_baseline="02-functional-requirements.md",
        counterpart="15-analytics-requirements.md"
    )

if __name__ == "__main__":
    main()
