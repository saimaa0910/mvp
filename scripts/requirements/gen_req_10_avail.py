#!/usr/bin/env python3
"""
gen_req_10_avail.py
Generates docs/02-requirements/10-availability-requirements.md
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_avail import AVAIL_REQUIREMENTS
from gen_base import generate_document

def render_avail_invariants(r):
    return [
        f"- **Failure Condition:** {r['failure_condition']}",
        f"- **Detection Mechanism:** {r['detection_mechanism']}",
        f"- **System Automated Response:** {r['system_response']}",
        f"- **Fallback Protocol:** {r['fallback_protocol']}",
        f"- **Recovery & Restoral Protocol:** {r['recovery_protocol']}",
        f"- **Verification Protocol:** {r['verification_method']}"
    ]

def main():
    exec_summary = (
        "This specification defines the authoritative availability, resilience, and business continuity requirements "
        "baseline for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. "
        "Comprising 40 comprehensive availability specifications (`AVAIL-001` through `AVAIL-040`), this document establishes the "
        "engineering safeguards ensuring 99.5% central cloud uptime, 8 hours autonomous offline operation, automated PostgreSQL failover, "
        "RPO <5 minutes, and RTO <30 minutes.\n\n"
        "Healthcare delivery at Namma Clinics cannot halt during municipal fiber cuts or power grid failures. The platform architecture "
        "guarantees that doctor consultations, nurse vitals entry, lab orders, and pharmacy dispensations proceed uninterrupted during extended network partitions."
    )

    mermaid_diagram = """graph TD
    subgraph CloudHA["Central Cloud Infrastructure (99.5% Uptime)"]
        ALB["Dual-AZ Application Load Balancer"]
        APP1["App Cluster AZ-1"]
        APP2["App Cluster AZ-2"]
        PG_M["PostgreSQL Primary"]
        PG_S["PostgreSQL Hot Standby (Streaming Replication)"]
        ALB --> APP1 & APP2
        APP1 & APP2 --> PG_M
        PG_M -.-> PG_S
    end
    subgraph EdgeAutonomy["Clinic Workstation Autonomy (8 Hours Offline)"]
        SW["Service Worker PWA Offline Cache"]
        DEX["IndexedDB Dexie.js Local Clinic Store"]
        QUEUE["Mutation Queue | Exponential Backoff Reconnect"]
        SW --> DEX --> QUEUE
    end
    QUEUE =="Auto Reconnect & Sync"==> ALB"""

    domain_cols = ("Resilience Domain", "Priority", "Failure Condition", "System Response", "Recovery Protocol")
    extractors = [
        lambda r: f"`{r['domain']}`",
        lambda r: f"`{r['priority']}`",
        lambda r: f"{r['failure_condition'][:35]}...",
        lambda r: f"{r['system_response'][:35]}...",
        lambda r: f"{r['recovery_protocol'][:35]}..."
    ]

    governance = (
        "This Availability Requirements Specification defines the binding operational resilience contract. "
        "Monthly automated chaos engineering drills and daily backup restoration validations ensure the platform meets its "
        "99.5% uptime and sub-30-minute RTO guarantees. Any architecture changes compromising high availability or offline autonomy "
        "require formal sign-off by the SRE Lead and Municipal Health Officer."
    )

    generate_document(
        doc_num="10",
        doc_slug="10-availability-requirements.md",
        doc_id="DOC-REQ-010-AVAIL",
        doc_title="Availability, Resilience & High Availability Baseline",
        req_type="Availability Requirement",
        req_range="AVAIL-001 through AVAIL-040",
        count=40,
        requirements=AVAIL_REQUIREMENTS,
        exec_summary=exec_summary,
        mermaid_diagram=mermaid_diagram,
        domain_table_cols=domain_cols,
        domain_col_extractors=extractors,
        domain_invariant_renderer=render_avail_invariants,
        governance_text=governance,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="09-performance-requirements.md"
    )

if __name__ == "__main__":
    main()
