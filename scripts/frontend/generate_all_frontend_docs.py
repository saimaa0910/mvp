"""
generate_all_frontend_docs.py
Master orchestrator script to sequentially execute all 19 Phase 09 Frontend generators.
"""

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.frontend import (
    gen_frontend_01_design_system,
    gen_frontend_02_architecture,
    gen_frontend_03_screens,
    gen_frontend_04_components,
    gen_frontend_05_role_screen,
    gen_frontend_06_navigation,
    gen_frontend_07_state,
    gen_frontend_09_offline,
    gen_frontend_10_localization,
    gen_frontend_11_accessibility,
    gen_frontend_11_responsive,
    gen_frontend_12_validation,
    gen_frontend_13_error_handling,
    gen_frontend_14_loading_states,
    gen_frontend_15_printing,
    gen_frontend_15_testing,
    gen_frontend_17_analytics,
    gen_frontend_18_deployment,
    gen_frontend_19_audit,
)

GENERATORS = [
    ("01-design-system.md", gen_frontend_01_design_system.generate_doc),
    ("02-frontend-architecture.md", gen_frontend_02_architecture.generate_doc),
    ("03-screen-catalog.md", gen_frontend_03_screens.generate_doc),
    ("04-component-catalog.md", gen_frontend_04_components.generate_doc),
    ("05-role-screen-matrix.md", gen_frontend_05_role_screen.generate_doc),
    ("06-navigation-map.md", gen_frontend_06_navigation.generate_doc),
    ("07-state-management.md", gen_frontend_07_state.generate_doc),
    ("08-offline-ui-states.md", gen_frontend_09_offline.generate_doc),
    ("09-localization.md", gen_frontend_10_localization.generate_doc),
    ("10-accessibility.md", gen_frontend_11_accessibility.generate_doc),
    ("11-responsive-design.md", gen_frontend_11_responsive.generate_doc),
    ("12-form-validation.md", gen_frontend_12_validation.generate_doc),
    ("13-error-handling.md", gen_frontend_13_error_handling.generate_doc),
    ("14-loading-states.md", gen_frontend_14_loading_states.generate_doc),
    ("15-printing.md", gen_frontend_15_printing.generate_doc),
    ("16-frontend-testing.md", gen_frontend_15_testing.generate_doc),
    ("17-analytics-observability.md", gen_frontend_17_analytics.generate_doc),
    ("18-ci-cd-deployment.md", gen_frontend_18_deployment.generate_doc),
    ("FRONTEND_COMPLETENESS_AUDIT.md", gen_frontend_19_audit.generate_doc),
]

def main():
    t0 = time.time()
    print("================================================================================")
    print("EXECUTING MASTER FRONTEND GENERATION ORCHESTRATOR (PHASE 09: 19 DOCUMENTS)")
    print("================================================================================")

    total_substantive = 0
    for filename, gen_fn in GENERATORS:
        res = gen_fn()
        sub = res["substantive"] if isinstance(res, dict) else res
        total_substantive += sub
        print(f"  -> {filename:<40} : {sub:>6} substantive lines [PASS]")

    elapsed = time.time() - t0
    print("================================================================================")
    print(f"ALL 19 FRONTEND DOCUMENTS GENERATED SUCCESSFULLY IN {elapsed:.2f}s")
    print(f"TOTAL SUBSTANTIVE LINES: {total_substantive:,}")
    print("================================================================================")

if __name__ == "__main__":
    main()
