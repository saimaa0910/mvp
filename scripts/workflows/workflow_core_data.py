#!/usr/bin/env python3
"""
workflow_core_data.py
Unified master accessor and aggregator for all 25 primary workflows in Namma Clinic Platform.
Exports:
  get_workflow(wfid: str) -> dict
  get_all_workflows() -> dict
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_wf01_to_05 import get_group1_workflows
from data_wf06_to_10 import get_group2_workflows
from data_wf11_to_15 import get_group3_workflows
from data_wf16_to_20 import get_group4_workflows
from data_wf21_to_25 import get_group5_workflows

_ALL_WORKFLOWS = None

def get_all_workflows():
    global _ALL_WORKFLOWS
    if _ALL_WORKFLOWS is None:
        all_wfs = {}
        all_wfs.update(get_group1_workflows())
        all_wfs.update(get_group2_workflows())
        all_wfs.update(get_group3_workflows())
        all_wfs.update(get_group4_workflows())
        all_wfs.update(get_group5_workflows())
        _ALL_WORKFLOWS = all_wfs
    return _ALL_WORKFLOWS

def get_workflow(wfid: str):
    wfs = get_all_workflows()
    if wfid not in wfs:
        raise KeyError(f"Workflow ID '{wfid}' not found in registry (available: WF-001 through WF-025)")
    return wfs[wfid]

if __name__ == "__main__":
    wfs = get_all_workflows()
    print(f"Loaded all {len(wfs)} workflows successfully.")
