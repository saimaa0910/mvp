#!/usr/bin/env python3
"""
generate_all_github_docs.py
Master runner: generates all 10 Phase 22 GitHub Engineering documents sequentially.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scripts.github.gen_github_01_strategy import generate_github_01
from scripts.github.gen_github_02_issue_hierarchy import generate_github_02
from scripts.github.gen_github_03_labels import generate_github_03
from scripts.github.gen_github_04_project_board import generate_github_04
from scripts.github.gen_github_05_milestones import generate_github_05
from scripts.github.gen_github_06_linking import generate_github_06
from scripts.github.gen_github_07_branching import generate_github_07
from scripts.github.gen_github_08_pr import generate_github_08
from scripts.github.gen_github_09_release import generate_github_09
from scripts.github.gen_github_audit import generate_github_audit

GENERATORS = [
    ("01-github-strategy.md", generate_github_01),
    ("02-issue-hierarchy.md", generate_github_02),
    ("03-label-ontology.md", generate_github_03),
    ("04-project-board.md", generate_github_04),
    ("05-milestones.md", generate_github_05),
    ("06-issue-linking.md", generate_github_06),
    ("07-branching-strategy.md", generate_github_07),
    ("08-pr-strategy.md", generate_github_08),
    ("09-release-management.md", generate_github_09),
    ("GITHUB_COMPLETENESS_AUDIT.md", generate_github_audit),
]

def main():
    print("=" * 70)
    print("Phase 22: GitHub Engineering Documentation Generation")
    print("=" * 70)
    results = {}
    for doc_name, gen_func in GENERATORS:
        try:
            res = gen_func()
            results[doc_name] = res
            print(f"  [OK] {doc_name}: {res['total']} total, {res['substantive']} substantive")
        except Exception as e:
            results[doc_name] = {"error": str(e)}
            print(f"  [FAIL] {doc_name}: {e}")

    print("=" * 70)
    all_ok = all("error" not in v for v in results.values())
    total_sub = sum(v.get("substantive", 0) for v in results.values())
    print(f"Total substantive lines across all documents: {total_sub}")
    if all_ok:
        print("STATUS: ALL 10 DOCUMENTS GENERATED SUCCESSFULLY")
    else:
        failed = [k for k, v in results.items() if "error" in v]
        print(f"STATUS: FAILURES DETECTED IN: {', '.join(failed)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
