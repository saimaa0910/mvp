#!/usr/bin/env python3
"""
verify_all_25.py
Validates all 25 primary workflows across all 5 groups.
"""

from data_wf01_to_05 import get_group1_workflows
from data_wf06_to_10 import get_group2_workflows
from data_wf11_to_15 import get_group3_workflows
from data_wf16_to_20 import get_group4_workflows
from data_wf21_to_25 import get_group5_workflows
from workflow_generator import render_workflow_document
from common import find_duplicate_paragraphs, count_lines

def main():
    all_wfs = {}
    all_wfs.update(get_group1_workflows())
    all_wfs.update(get_group2_workflows())
    all_wfs.update(get_group3_workflows())
    all_wfs.update(get_group4_workflows())
    all_wfs.update(get_group5_workflows())

    print(f"Total workflows loaded: {len(all_wfs)}")
    assert len(all_wfs) == 25, f"Expected 25 workflows, got {len(all_wfs)}"

    docs = {}
    total_substantive = 0
    failures = []
    for wfid in sorted(all_wfs.keys()):
        doc = render_workflow_document(all_wfs[wfid])
        docs[wfid] = doc
        c = count_lines(doc)
        total_substantive += c["substantive"]
        status = "PASS" if c["substantive"] >= 2000 else "FAIL"
        if status == "FAIL":
            failures.append((wfid, c["substantive"]))
        print(f"  {wfid}: Total = {c['total']}, Substantive = {c['substantive']} [{status}]")

    print("\n" + "="*60)
    print(f"TOTAL SUBSTANTIVE LINES ACROSS ALL 25 WORKFLOWS: {total_substantive:,}")
    print(f"AVERAGE SUBSTANTIVE LINES PER WORKFLOW: {total_substantive // 25:,}")
    print("="*60)

    dups = find_duplicate_paragraphs(docs, min_len=60)
    print(f"\nDUPLICATE PARAGRAPHS ACROSS ALL 25 WORKFLOWS: {len(dups)}")
    if dups:
        for d in dups[:10]:
            print(f"  DUP between {d[0]} and {d[1]}: {d[2][:60]}...")
    else:
        print("  PERFECT: ZERO DUPLICATE PARAGRAPHS!")

    if failures:
        print(f"\nFAILURES ({len(failures)}): {failures}")
    else:
        print("\nALL 25 PRIMARY WORKFLOWS MEET >= 2,000 SUBSTANTIVE LINES!")

if __name__ == "__main__":
    main()
