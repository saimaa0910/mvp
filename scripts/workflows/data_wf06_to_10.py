#!/usr/bin/env python3
"""
data_wf06_to_10.py
Clean, self-contained domain specifications for Workflows 06 to 10:
  - WF-006: Informed Clinical & Digital Health Consent Workflow
  - WF-007: Token Issuance, Priority Tagging & Queue Entry Workflow
  - WF-008: Dynamic Multi-Room Queue Orchestration & Display Workflow
  - WF-009: Nursing Triage, Vital Signs & Clinical Acuity Assessment Workflow
  - WF-010: Danger Sign Detection, Critical Value Alert & Emergency Escalation Workflow

Exports:
  DATA_WF06_TO_10 (dict mapping 'WF-006'..'WF-010' to enriched 67-section workflow dicts)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_factory import build_workflow_object
from build_group2 import get_group2_specs

def get_group2_workflows():
    specs = get_group2_specs()
    return {wfid: build_workflow_object(spec) for wfid, spec in specs.items()}

if __name__ == "__main__":
    from workflow_generator import render_workflow_document
    from common import count_lines, find_duplicate_paragraphs
    print("Testing data_wf06_to_10.py...")
    wfs = get_group2_workflows()
    docs = {}
    for wfid, wf_data in wfs.items():
        doc = render_workflow_document(wf_data)
        docs[wfid] = doc
        counts = count_lines(doc)
        status = "PASS" if counts["substantive"] >= 2000 else "FAIL"
        print(f"  {wfid}: Total = {counts['total']}, Substantive = {counts['substantive']} [{status}]")

    dups = find_duplicate_paragraphs(docs, min_len=60)
    print(f"  Duplicate paragraphs within Group 2: {len(dups)}")
