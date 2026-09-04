#!/usr/bin/env python3
"""
gen_req_09_perf.py
Generates docs/02-requirements/09-performance-requirements.md
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_perf import PERF_REQUIREMENTS
from gen_base import generate_document

def render_perf_invariants(r):
    return [
        f"- **Performance Metric:** {r['performance_metric']}",
        f"- **Target SLA Threshold:** `{r['target_threshold']}`",
        f"- **Test Workload Condition:** {r['test_workload']}",
        f"- **Metric Classification:** {r['metric_classification']}",
        f"- **Verification Protocol:** {r['verification_method']}",
        f"- **Accountable Performance Lead:** {r['owner']}"
    ]

def main():
    exec_summary = (
        "This specification defines the authoritative, measurable performance requirements baseline for the Namma Clinic "
        "Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. Comprising 40 rigorous "
        "performance engineering specifications (`PERF-001` through `PERF-040`), this document establishes non-negotiable latency "
        "budgets, memory limits, client-side indexing throughputs, thermal printing speeds, and background sync performance.\n\n"
        "Because Namma Clinics operate on low-cost, refurbished dual-core workstations with 4GB RAM connected via variable 2G/3G/4G "
        "cellular dongles, performance is treated as an indispensable functional prerequisite. Every requirement establishes clear "
        "p95 and p99 latency thresholds, explicit measurement tools (k6, Lighthouse, Chrome DevTools, PostgreSQL pg_stat_statements), "
        "load profiles, and executable BDD Gherkin scenarios."
    )

    mermaid_diagram = """graph LR
    subgraph Client["Client Workstation (Refurbished 4GB PC)"]
        IDB["IndexedDB Commit: <10ms"]
        RAM["Max PWA Heap: <150MB"]
        SEARCH["Local Patient Trie Search: <150ms"]
        PRINT["ESC/POS Thermal Print: <500ms"]
    end
    subgraph Network["Variable Network (2G/3G/4G)"]
        SYNC["Mutation Sync: 50 mutations/sec"]
        PAYLOAD["Compressed API Payload: <50KB"]
    end
    subgraph Cloud["Central Cloud Server"]
        API["API Gateway p95: <120ms"]
        DB["PostgreSQL Index Scan: <20ms"]
        DUCK["DuckDB Mart Aggregation: <1.5s"]
    end
    IDB --> SYNC --> API --> DB"""

    domain_cols = ("Subsystem Domain", "Priority", "Target Threshold", "Workload Condition", "Verification Method")
    extractors = [
        lambda r: f"`{r['domain']}`",
        lambda r: f"`{r['priority']}`",
        lambda r: f"`{r['target_threshold'][:35]}`",
        lambda r: f"{r['test_workload'][:35]}...",
        lambda r: f"{r['verification_method'][:30]}..."
    ]

    governance = (
        "This Performance Requirements Specification constitutes the binding technical contract for system responsiveness. "
        "Automated load tests run nightly via k6 to prevent performance regressions from entering production bundles. "
        "Any pull request introducing >10% latency regression is automatically blocked by CI performance quality gates."
    )

    generate_document(
        doc_num="09",
        doc_slug="09-performance-requirements.md",
        doc_id="DOC-REQ-009-PERF",
        doc_title="Performance Requirements & Latency Engineering Baseline",
        req_type="Performance Requirement",
        req_range="PERF-001 through PERF-040",
        count=40,
        requirements=PERF_REQUIREMENTS,
        exec_summary=exec_summary,
        mermaid_diagram=mermaid_diagram,
        domain_table_cols=domain_cols,
        domain_col_extractors=extractors,
        domain_invariant_renderer=render_perf_invariants,
        governance_text=governance,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="10-availability-requirements.md"
    )

if __name__ == "__main__":
    main()
