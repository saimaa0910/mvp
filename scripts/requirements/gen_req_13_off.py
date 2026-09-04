#!/usr/bin/env python3
"""
gen_req_13_off.py
Generates docs/02-requirements/13-offline-requirements.md
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_off import OFF_REQUIREMENTS
from gen_base import generate_document

def render_off_invariants(r):
    return [
        f"- **Offline Operational State:** {r['offline_mode_state']}",
        f"- **IndexedDB Dexie.js Schema:** `{r['local_store_schema']}`",
        f"- **Conflict Resolution Protocol:** {r['conflict_resolution_strategy']}",
        f"- **Verification Protocol:** {r['verification_method']}",
        f"- **Accountable Mobile/Offline Lead:** {r['owner']}"
    ]

def main():
    exec_summary = (
        "This specification defines the comprehensive offline operation, local persistence, mutation queuing, and "
        "reconciliation requirements baseline for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers "
        "in Greater Bengaluru. Comprising 50 rigorous offline specifications (`OFF-001` through `OFF-050`), this document guarantees "
        "that all clinical consultations, vital sign entries, lab orders, pharmacy dispensations, and token issuances proceed with "
        "100% autonomy during extended network outages.\n\n"
        "Frontline urban healthcare centers in Bengaluru frequently experience fiber cuts, power grid fluctuations, and erratic cellular "
        "dongle coverage. The platform implements an offline-first architecture powered by Dexie.js IndexedDB local storage, deterministic "
        "UUIDv7 primary keys, priority-ordered mutation queues, automatic exponential backoff reconnection, and field-level clinical "
        "conflict resolution."
    )

    mermaid_diagram = """graph TD
    subgraph ClientPWA["Client PWA Workstation (Offline First)"]
        SW["Service Worker (CacheStorage Assets & Bundles)"]
        IDB["Dexie.js IndexedDB Store (Clinical & Demographic Data)"]
        QUEUE["FIFO Mutation Queue (UUIDv7 Keys | Priority Order)"]
        RESOLVE["Conflict Resolver (Field Merge | Clinician Authority)"]
        SW --> IDB --> QUEUE
    end
    subgraph NetworkState["Network Transition Engine"]
        DETECT["Online/Offline Detector (Heartbeat & Navigator)"]
        BACKOFF["Exponential Backoff & Jitter Scheduler"]
        DETECT --> BACKOFF
    end
    subgraph CentralServer["Central Cloud Sync Gateway"]
        SYNC_API["Idempotent Delta Sync API"]
        PG_DB["PostgreSQL Master Database"]
        CDC["Logical Replication & Change Data Capture"]
        SYNC_API --> PG_DB --> CDC
    end
    QUEUE =="Auto Batch Flush"==> SYNC_API
    SYNC_API =="Reconciliation Ack"==> RESOLVE"""

    domain_cols = ("Operational State", "Priority", "Local Store Schema", "Conflict Resolution Strategy", "Owner")
    extractors = [
        lambda r: f"`{r['domain']}`",
        lambda r: f"`{r['priority']}`",
        lambda r: f"`{r['local_store_schema'][:35]}`",
        lambda r: f"{r['conflict_resolution_strategy'][:35]}...",
        lambda r: f"{r['owner']}"
    ]

    governance = (
        "This Offline Requirements Specification defines the non-negotiable operational continuity standard for the Namma Clinic Platform. "
        "All client-side features must function autonomously without active internet connectivity. Automated chaos disconnection tests "
        "run continuously in CI to verify that zero data loss occurs across unexpected browser crashes or power outages."
    )

    generate_document(
        doc_num="13",
        doc_slug="13-offline-requirements.md",
        doc_id="DOC-REQ-013-OFF",
        doc_title="Offline Operation, Local Persistence & Sync Requirements Baseline",
        req_type="Offline Autonomy Requirement",
        req_range="OFF-001 through OFF-050",
        count=50,
        requirements=OFF_REQUIREMENTS,
        exec_summary=exec_summary,
        mermaid_diagram=mermaid_diagram,
        domain_table_cols=domain_cols,
        domain_col_extractors=extractors,
        domain_invariant_renderer=render_off_invariants,
        governance_text=governance,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="10-availability-requirements.md"
    )

if __name__ == "__main__":
    main()
