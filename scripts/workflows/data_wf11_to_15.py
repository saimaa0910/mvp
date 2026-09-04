#!/usr/bin/env python3
"""
data_wf11_to_15.py
Clean, self-contained domain specifications for Workflows 11 to 15:
  - WF-011: Doctor Clinical Consultation, SOAP Documentation & CDSS Advisory Workflow
  - WF-012: Electronic Prescription, Drug Interaction & Safety Verification Workflow
  - WF-013: Pharmacy Dispensing, FEFO Inventory Allocation & Patient Counseling Workflow
  - WF-014: Pharmacy Stock Replenishment, Indenting & Cold-Chain Inventory Control Workflow
  - WF-015: Point-of-Care Laboratory Testing, Barcoding & Panic Value Alert Workflow

Exports:
  DATA_WF11_TO_15 (dict mapping 'WF-011'..'WF-015' to enriched 67-section workflow dicts)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_factory import build_workflow_object
from build_group3 import get_group3_specs

def get_group3_workflows():
    specs = get_group3_specs()
    return {wfid: build_workflow_object(spec) for wfid, spec in specs.items()}

if __name__ == "__main__":
    from workflow_generator import render_workflow_document
    from common import count_lines, find_duplicate_paragraphs
    print("Testing data_wf11_to_15.py...")
    wfs = get_group3_workflows()
    docs = {}
    for wfid, wf_data in wfs.items():
        doc = render_workflow_document(wf_data)
        docs[wfid] = doc
        counts = count_lines(doc)
        status = "PASS" if counts["substantive"] >= 2000 else "FAIL"
        print(f"  {wfid}: Total = {counts['total']}, Substantive = {counts['substantive']} [{status}]")

    dups = find_duplicate_paragraphs(docs, min_len=60)
    print(f"  Duplicate paragraphs within Group 3: {len(dups)}")
