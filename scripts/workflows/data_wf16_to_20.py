#!/usr/bin/env python3
"""
data_wf16_to_20.py
Clean, self-contained domain specifications for Workflows 16 to 20:
  - WF-016: Clinical Referral, Higher Center Escalation & Ambulance Transfer Workflow
  - WF-017: NCD Follow-Up Scheduling, Chronic Disease Recall & Defaulter Tracking Workflow
  - WF-018: Omnichannel Patient & Staff Notification, Alerting & Communication Workflow
  - WF-019: Citizen Grievance Redressal, Feedback & SLA Escalation Workflow
  - WF-020: Cryptographic Audit Trail, Immutable Logging & Tamper Detection Workflow

Exports:
  DATA_WF16_TO_20 (dict mapping 'WF-016'..'WF-020' to enriched 67-section workflow dicts)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_factory import build_workflow_object
from build_group4 import get_group4_specs

def get_group4_workflows():
    specs = get_group4_specs()
    return {wfid: build_workflow_object(spec) for wfid, spec in specs.items()}

if __name__ == "__main__":
    from workflow_generator import render_workflow_document
    from common import count_lines, find_duplicate_paragraphs
    print("Testing data_wf16_to_20.py...")
    wfs = get_group4_workflows()
    docs = {}
    for wfid, wf_data in wfs.items():
        doc = render_workflow_document(wf_data)
        docs[wfid] = doc
        counts = count_lines(doc)
        status = "PASS" if counts["substantive"] >= 2000 else "FAIL"
        print(f"  {wfid}: Total = {counts['total']}, Substantive = {counts['substantive']} [{status}]")

    dups = find_duplicate_paragraphs(docs, min_len=60)
    print(f"  Duplicate paragraphs within Group 4: {len(dups)}")
