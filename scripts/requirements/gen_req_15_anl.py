#!/usr/bin/env python3
"""
gen_req_15_anl.py
Generates docs/02-requirements/15-analytics-requirements.md
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_anl import ANL_REQUIREMENTS
from gen_base import generate_document

def render_anl_invariants(r):
    return [
        f"- **Analytical Dimension:** {r['analytical_dimension']}",
        f"- **Aggregation Cadence:** {r['aggregation_cadence']}",
        f"- **Analytical Storage Target:** `{r['duckdb_query_target']}`",
        f"- **Verification Protocol:** {r['verification_method']}",
        f"- **Accountable Data Lead:** {r['owner']}"
    ]

def main():
    exec_summary = (
        "This specification defines the comprehensive analytics architecture, OLTP/OLAP decoupling, dimensional modeling, "
        "and epidemiological intelligence requirements baseline for the Namma Clinic Digital Health Platform across 183 primary "
        "urban healthcare centers in Greater Bengaluru. Comprising 40 detailed analytics specifications (`ANL-001` through `ANL-040`), "
        "this document establishes the star-schema data models, embedded DuckDB execution pipelines, change data capture (CDC) SLAs, "
        "and privacy-preserving k-anonymity safeguards governing all municipal business intelligence.\n\n"
        "To ensure that analytical workloads never contend with or degrade frontline doctor consultations, the architecture enforces "
        "strict separation between transactional PostgreSQL stores and embedded DuckDB / Parquet analytical marts."
    )

    mermaid_diagram = """graph TD
    subgraph OLTP["Transactional Tier (PostgreSQL)"]
        CLINIC_DB["PostgreSQL Master Database"]
        WAL["Write-Ahead Log & Logical Replication"]
        CLINIC_DB --> WAL
    end
    subgraph Pipeline["Change Data Capture (CDC) Pipeline"]
        DEBEZIUM["CDC Event Streamer"]
        DUCK_LOCAL["Embedded DuckDB Local Mart (clinic_mart.duckdb)"]
        WAL --> DEBEZIUM --> DUCK_LOCAL
    end
    subgraph Lakehouse["Cloud Analytical Lakehouse (OLAP)"]
        S3_PARQUET["Parquet Partitions (/year/month/clinic/)"]
        STAR_SCHEMA["Star Schema: Fact_Consultation | Dim_Clinic | Dim_Date"]
        BI_DASH["BBMP Municipal Executive Health Dashboard"]
        DEBEZIUM --> S3_PARQUET --> STAR_SCHEMA --> BI_DASH
    end"""

    domain_cols = ("Analytical Dimension", "Priority", "Cadence", "Storage Target", "Lead Owner")
    extractors = [
        lambda r: f"`{r['analytical_dimension']}`",
        lambda r: f"`{r['priority']}`",
        lambda r: f"`{r['aggregation_cadence']}`",
        lambda r: f"`{r['duckdb_query_target'][:35]}`",
        lambda r: f"{r['owner']}"
    ]

    governance = (
        "This Analytics Requirements Specification defines the binding data intelligence baseline. "
        "All analytical models and queries are subject to automated regression testing to guarantee sub-1.5s execution times and zero OLTP impact. "
        "Public health analytics feeds must satisfy differential privacy standards (k>=5) before release."
    )

    generate_document(
        doc_num="15",
        doc_slug="15-analytics-requirements.md",
        doc_id="DOC-REQ-015-ANL",
        doc_title="Analytics Architecture & Public Health Data Platform Baseline",
        req_type="Analytics Requirement",
        req_range="ANL-001 through ANL-040",
        count=40,
        requirements=ANL_REQUIREMENTS,
        exec_summary=exec_summary,
        mermaid_diagram=mermaid_diagram,
        domain_table_cols=domain_cols,
        domain_col_extractors=extractors,
        domain_invariant_renderer=render_anl_invariants,
        governance_text=governance,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="14-reporting-requirements.md"
    )

if __name__ == "__main__":
    main()
