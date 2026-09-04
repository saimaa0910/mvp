#!/usr/bin/env python3
"""
data_wf21_to_25.py
Clean, self-contained domain specifications for Workflows 21 to 25:
  - WF-021: Clinical Analytics, Syndromic Surveillance & Population Health Reporting Workflow
  - WF-022: Autonomous Offline Edge Operation, Local Storage & Network Resilience Workflow
  - WF-023: Bidirectional Synchronization, Conflict Resolution & Merkle Ledger Workflow
  - WF-024: Ayushman Bharat Digital Mission (ABDM) Gateway & FHIR Interoperability Workflow
  - WF-025: Clinical Emergency Exception, Fast-Track Bypass & Resuscitation Protocol Workflow

Exports:
  DATA_WF21_TO_25 (dict mapping 'WF-021'..'WF-025' to enriched 67-section workflow dicts)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_factory import build_workflow_object
from build_group5 import get_group5_specs

def get_group5_workflows():
    specs = get_group5_specs()
    return {wfid: build_workflow_object(spec) for wfid, spec in specs.items()}

if __name__ == "__main__":
    from workflow_generator import render_workflow_document
    from common import count_lines, find_duplicate_paragraphs
    print("Testing data_wf21_to_25.py...")
    wfs = get_group5_workflows()
    docs = {}
    for wfid, wf_data in wfs.items():
        doc = render_workflow_document(wf_data)
        docs[wfid] = doc
        counts = count_lines(doc)
        status = "PASS" if counts["substantive"] >= 2000 else "FAIL"
        print(f"  {wfid}: Total = {counts['total']}, Substantive = {counts['substantive']} [{status}]")

    dups = find_duplicate_paragraphs(docs, min_len=60)
    print(f"  Duplicate paragraphs within Group 5: {len(dups)}")
