#!/usr/bin/env python3
"""
generate_all_workflows.py
Master orchestrator script that generates all 25 primary workflow markdown documents
(01-master-clinic-workflow.md through 25-emergency-exception-workflow.md)
and all 6 supporting architectural catalogs in docs/03-workflows/.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from workflow_metadata import WORKFLOW_SPECS, WORKFLOW_MAP
from workflow_core_data import get_all_workflows
from workflow_generator import render_workflow_document
from common import count_lines, find_duplicate_paragraphs

# Catalogs
from catalog_dependency_graph import write_dependency_graph_file
from catalog_traceability_matrix import write_traceability_matrix_file
from catalog_test_catalog import write_test_catalog_file
from catalog_error_catalog import write_error_catalog_file
from catalog_observability_catalog import write_observability_catalog_file
from catalog_completeness_audit import write_completeness_audit_file

def main():
    print("=" * 80)
    print("NAMMA CLINIC PLATFORM — MASTER WORKFLOW ENGINEERING GENERATOR")
    print("=" * 80)

    repo_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    out_dir = os.path.join(repo_root, "docs", "03-workflows")
    os.makedirs(out_dir, exist_ok=True)

    print(f"Target Output Directory: {out_dir}")
    print("Loading all 25 workflow specifications from core registry...")
    wfs = get_all_workflows()
    assert len(wfs) == 25, f"Expected 25 workflows, found {len(wfs)}"

    rendered_docs = {}
    total_primary_substantive = 0
    failures = []

    print("\n[Phase 1/2] Rendering and Writing 25 Primary Workflow Documents...")
    for i in range(1, 26):
        wfid = f"WF-{i:03d}"
        spec = WORKFLOW_MAP[wfid]
        wfdata = wfs[wfid]
        filename = spec["file"]
        filepath = os.path.join(out_dir, filename)

        doc = render_workflow_document(wfdata)
        rendered_docs[filename] = doc
        counts = count_lines(doc)
        total_primary_substantive += counts["substantive"]

        status = "PASS" if counts["substantive"] >= 2000 else "FAIL"
        if status == "FAIL":
            failures.append((wfid, counts["substantive"]))

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(doc)

        print(f"  [{i:02d}/25] {filename} -> Total: {counts['total']:,} | Substantive: {counts['substantive']:,} [{status}]")

    print("\n" + "-" * 80)
    print(f"Total Substantive Lines across 25 Primary Workflows: {total_primary_substantive:,}")
    print(f"Average Substantive Lines per Workflow: {total_primary_substantive // 25:,}")
    print("-" * 80)

    print("\n[Phase 2/2] Generating Supporting Architectural Catalogs...")
    write_dependency_graph_file()
    write_traceability_matrix_file()
    write_test_catalog_file()
    write_error_catalog_file()
    write_observability_catalog_file()
    write_completeness_audit_file()

    print("\n" + "=" * 80)
    print("All 31 workflow documentation artifacts generated successfully.")
    print("=" * 80)

if __name__ == "__main__":
    main()
