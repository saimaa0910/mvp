"""
generate_all_devops_docs.py
Master orchestrator to generate all 20 Phase 12 DevOps Engineering documents.
Enforces >= 2,000 substantive lines on every generated document.
"""

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines

from scripts.devops import (
    gen_devops_01_arch,
    gen_devops_02_environments,
    gen_devops_03_git_strategy,
    gen_devops_04_branching,
    gen_devops_05_pr_strategy,
    gen_devops_06_ci_pipeline,
    gen_devops_07_cd_pipeline,
    gen_devops_08_docker,
    gen_devops_09_cloud_arch,
    gen_devops_10_iac,
    gen_devops_11_secrets,
    gen_devops_12_monitoring,
    gen_devops_13_logging,
    gen_devops_14_alerting,
    gen_devops_15_backup,
    gen_devops_16_dr,
    gen_devops_17_rollbacks,
    gen_devops_18_release,
    gen_devops_19_prr,
    gen_devops_audit,
)

GENERATORS = [
    ("01-devops-architecture.md", gen_devops_01_arch.generate_doc),
    ("02-environments.md", gen_devops_02_environments.generate_doc),
    ("03-git-strategy.md", gen_devops_03_git_strategy.generate_doc),
    ("04-branching-strategy.md", gen_devops_04_branching.generate_doc),
    ("05-pr-strategy.md", gen_devops_05_pr_strategy.generate_doc),
    ("06-ci-pipeline.md", gen_devops_06_ci_pipeline.generate_doc),
    ("07-cd-pipeline.md", gen_devops_07_cd_pipeline.generate_doc),
    ("08-docker-strategy.md", gen_devops_08_docker.generate_doc),
    ("09-cloud-architecture.md", gen_devops_09_cloud_arch.generate_doc),
    ("10-infrastructure-as-code.md", gen_devops_10_iac.generate_doc),
    ("11-secrets.md", gen_devops_11_secrets.generate_doc),
    ("12-monitoring.md", gen_devops_12_monitoring.generate_doc),
    ("13-logging.md", gen_devops_13_logging.generate_doc),
    ("14-alerting.md", gen_devops_14_alerting.generate_doc),
    ("15-backup.md", gen_devops_15_backup.generate_doc),
    ("16-disaster-recovery.md", gen_devops_16_dr.generate_doc),
    ("17-rollbacks.md", gen_devops_17_rollbacks.generate_doc),
    ("18-release-management.md", gen_devops_18_release.generate_doc),
    ("19-production-readiness.md", gen_devops_19_prr.generate_doc),
    ("DEVOPS_COMPLETENESS_AUDIT.md", gen_devops_audit.generate_doc),
]

def main():
    print("=" * 80)
    print("PHASE 12 — DEVOPS ENGINEERING DOCUMENTATION GENERATOR")
    print("Target: 20 Canonical Documents in docs/12-devops/ (>= 2,000 substantive lines each)")
    print("=" * 80)

    start_time = time.time()
    results = []

    for idx, (doc_name, gen_func) in enumerate(GENERATORS, 1):
        print(f"[{idx:02d}/20] Generating {doc_name}...", end=" ", flush=True)
        t0 = time.time()
        stats = gen_func()
        elapsed = time.time() - t0
        sub = stats["substantive"]
        tot = stats["total"]
        status = "PASS" if sub >= 2000 else "FAIL"
        print(f"-> {status} ({sub:,} substantive / {tot:,} total lines in {elapsed:.2f}s)")
        results.append((doc_name, sub, tot, status))

    print("\n" + "=" * 80)
    print(f"{'#':<3} {'Document Name':<35} {'Substantive':<14} {'Total':<10} {'Status':<6}")
    print("-" * 80)
    total_sub = 0
    total_tot = 0
    all_pass = True

    for idx, (doc_name, sub, tot, status) in enumerate(results, 1):
        print(f"{idx:<3} {doc_name:<35} {sub:<14,d} {tot:<10,d} {status:<6}")
        total_sub += sub
        total_tot += tot
        if status != "PASS":
            all_pass = False

    print("-" * 80)
    print(f"{'TOTAL':<39} {total_sub:<14,d} {total_tot:<10,d} {'ALL PASS' if all_pass else 'FAIL'}")
    print("=" * 80)
    print(f"Generation completed in {time.time() - start_time:.2f}s")

    if not all_pass:
        print("ERROR: One or more documents failed to reach the 2,000 substantive line threshold!")
        sys.exit(1)

if __name__ == "__main__":
    main()
