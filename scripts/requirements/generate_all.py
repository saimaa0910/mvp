#!/usr/bin/env python3
"""
generate_all.py
Master runner script that executes all 17 requirements generator scripts sequentially.
Outputs all 17 requirements markdown specifications in docs/02-requirements/.
"""

import os
import sys
import time

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(DIR_PATH)

GENERATOR_SCRIPTS = [
    ("01", "gen_req_01_br.py", "01-business-requirements.md"),
    ("02", "gen_req_02_fr.py", "02-functional-requirements.md"),
    ("03", "gen_req_03_nfr.py", "03-non-functional-requirements.md"),
    ("04", "gen_req_04_brule.py", "04-business-rules.md"),
    ("05", "gen_req_05_cr.py", "05-clinical-rules.md"),
    ("06", "gen_req_06_or.py", "06-operational-rules.md"),
    ("07", "gen_req_07_secr.py", "07-security-requirements.md"),
    ("08", "gen_req_08_priv.py", "08-privacy-requirements.md"),
    ("09", "gen_req_09_perf.py", "09-performance-requirements.md"),
    ("10", "gen_req_10_avail.py", "10-availability-requirements.md"),
    ("11", "gen_req_11_loc.py", "11-localization-requirements.md"),
    ("12", "gen_req_12_a11y.py", "12-accessibility-requirements.md"),
    ("13", "gen_req_13_off.py", "13-offline-requirements.md"),
    ("14", "gen_req_14_rep.py", "14-reporting-requirements.md"),
    ("15", "gen_req_15_anl.py", "15-analytics-requirements.md"),
    ("16", "gen_req_16_air.py", "16-ai-requirements.md"),
    ("17", "gen_req_17_int.py", "17-integration-requirements.md"),
]

def run_all_generators():
    start_time = time.time()
    print("=" * 70)
    print("NAMMA CLINIC REQUIREMENTS ENGINEERING — MASTER GENERATOR")
    print("Generating all 17 Requirements Engineering documents...")
    print("=" * 70)

    docs_dir = os.path.abspath(os.path.join(DIR_PATH, "..", "..", "docs", "02-requirements"))
    os.makedirs(docs_dir, exist_ok=True)

    summary_results = []
    total_lines_all = 0
    total_substantive_all = 0

    for doc_num, script_name, target_file in GENERATOR_SCRIPTS:
        script_path = os.path.join(DIR_PATH, script_name)
        if not os.path.exists(script_path):
            print(f"[ERROR] Generator script not found: {script_path}")
            sys.exit(1)

        # Import or run module
        mod_name = script_name[:-3]
        if mod_name in sys.modules:
            del sys.modules[mod_name]
        
        # Execute generator
        import importlib
        mod = importlib.import_module(mod_name)
        
        # Determine entry point
        if hasattr(mod, "main"):
            mod.main()
        elif hasattr(mod, "generate_business_requirements"):
            mod.generate_business_requirements()
        elif hasattr(mod, "generate_functional_requirements"):
            mod.generate_functional_requirements()
        elif hasattr(mod, "generate_non_functional_requirements"):
            mod.generate_non_functional_requirements()
        elif hasattr(mod, "generate_business_rules"):
            mod.generate_business_rules()
        elif hasattr(mod, "generate_clinical_rules"):
            mod.generate_clinical_rules()
        elif hasattr(mod, "generate_operational_rules"):
            mod.generate_operational_rules()
        else:
            # Fallback: search for any function starting with generate_
            fns = [getattr(mod, f) for f in dir(mod) if f.startswith("generate_") and callable(getattr(mod, f))]
            if fns:
                fns[0]()
            else:
                print(f"[ERROR] No generator function found in {script_name}")
                sys.exit(1)

        # Audit generated file
        out_path = os.path.join(docs_dir, target_file)
        if not os.path.exists(out_path):
            print(f"[ERROR] Output file was not created: {out_path}")
            sys.exit(1)

        with open(out_path, "r", encoding="utf-8") as f:
            text = f.read()

        lines = text.splitlines()
        substantive = [l for l in lines if l.strip() and not l.strip().startswith('#') and not l.strip() == '---']
        total_lines_all += len(lines)
        total_substantive_all += len(substantive)
        status = "PASS" if len(substantive) >= 2000 else "FAIL (<2000 lines)"

        summary_results.append((doc_num, target_file, len(lines), len(substantive), status))

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"GENERATION COMPLETE ({elapsed:.2f}s)")
    print("=" * 70)
    print(f"{'Doc':4} | {'Target File':36} | {'Total':6} | {'Substantive':11} | {'Status'}")
    print("-" * 70)
    for num, fname, tot, sub, st in summary_results:
        print(f"{num:4} | {fname:36} | {tot:6} | {sub:11} | {st}")
    print("-" * 70)
    print(f"GRAND TOTAL: {total_lines_all:,} total lines | {total_substantive_all:,} substantive lines")
    print("=" * 70)

if __name__ == "__main__":
    run_all_generators()
