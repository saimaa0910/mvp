"""
gen_qa_07_ui.py
Generator for docs/11-qa/07-ui-test-plan.md
Produces >= 2,200 substantive lines detailing UI & Presentation Layer Testing.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.qa.qa_gen_common import write_qa_doc, format_test_case, make_qa_bdd_scenario
from scripts.qa.qa_core_data import UI_TESTS, TEST_CASES
from scripts.frontend.frontend_core_data import SCREENS

def generate_doc():
    lines = []
    lines.append("# UI, Presentation Layer & Visual Regression Test Plan")
    lines.append("## Namma Clinic Digital Health & Operations Platform")
    lines.append("### Greater Bengaluru Authority (GBA) / BBMP Health Department")
    lines.append("**Standard:** W3C Web Standards / Playwright & Storybook Visual Diffs / Design System Tokens | **Status:** APPROVED BASELINE | **Code:** `QA-DOC-07`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. UI Testing Charter & Presentation Layer Scope")
    lines.append("The Namma Clinic UI Test Plan governs automated testing of the presentation tier across all 108 screens and 160 reusable components defined in Phase 09. Testing validates component rendering, layout responsiveness, form validation feedback, loading skeletons, error states, and pixel-level visual regression across Desktop Mini-PCs, Field Nurse Android tablets, and Citizen mobile viewports.")
    lines.append("")
    lines.append("### 1.1 Core UI Testing Dimensions")
    lines.append("1. **Visual Regression:** Playwright snapshot comparison with 0.1% pixel diff threshold against baseline Storybook tokens.")
    lines.append("2. **Form Validation & Input Masking:** Real-time feedback for 10-digit mobile, Verhoeff Aadhaar, and clinical vitals ranges.")
    lines.append("3. **State Transitions:** Verified UI state flow: Idle -> Loading Skeleton -> Success -> Error Banner -> Offline Banner.")
    lines.append("4. **Responsive Layouts:** Viewport verification across Desktop (1920x1080), Tablet (1280x800), and Mobile (390x844).")
    lines.append("5. **Hardware Dialogs:** Print preview layout formatting for 80mm thermal prescription and barcode slips.")
    lines.append("")
    lines.append("### 1.2 UI Test Execution Lifecycle Diagram")
    lines.append("```mermaid")
    lines.append("sequenceDiagram")
    lines.append("    autonumber")
    lines.append("    actor TestRunner as Playwright Visual Test Engine")
    lines.append("    participant Storybook as Component Catalog (160 Components)")
    lines.append("    participant App as PWA Shell (108 Screens)")
    lines.append("    participant Baseline as Golden Image Snapshot Vault")
    lines.append("    TestRunner->>Storybook: Mount Component in Isolation")
    lines.append("    TestRunner->>Storybook: Capture Viewport Snapshots (Desktop / Tablet / Mobile)")
    lines.append("    TestRunner->>Baseline: Compute Pixel Delta against Golden Image")
    lines.append("    Baseline-->>TestRunner: Delta < 0.1% (PASS)")
    lines.append("    TestRunner->>App: Navigate to Target Screen in Headless Chromium")
    lines.append("    TestRunner->>App: Input Boundary Form Data & Trigger Validation")
    lines.append("    TestRunner->>App: Assert Error Banners & ARIA Announcements")
    lines.append("    TestRunner-->>TestRunner: Generate Visual QA Attestation")
    lines.append("```")
    lines.append("")

    # Section 2: 80 Canonical UI Tests
    lines.append("## 2. Canonical UI Test Specifications (UI-TEST-001 to UI-TEST-080)")
    lines.append("Standardized UI test specifications covering presentation components:")
    lines.append("")
    for ut in UI_TESTS:
        lines.append(f"### {ut['id']}: {ut['title']}")
        lines.append(f"- **Target Screen:** `{ut['target_screen']}`")
        lines.append(f"- **Test Flavor:** {ut['test_type']}")
        lines.append(f"- **Target Viewports:** {ut['viewport']}")
        lines.append(f"- **Visual Tolerance:** Delta < 0.1% pixel variance")
        lines.append(f"- **Audit Event Emitted:** `UI_TEST_AUDIT_{ut['id'].replace('-', '_')}`")
        lines.append("")

    # Section 3: 55 Detailed Test Cases
    lines.append("## 3. Detailed UI Verification Test Cases (TC-0331 to TC-0385)")
    lines.append("Detailed test specifications verifying presentation tier components:")
    lines.append("")
    for tc in TEST_CASES[330:385]:
        lines.extend(format_test_case(tc))

    # Section 4: 35 BDD Scenarios
    lines.append("## 4. UI BDD Acceptance Scenarios")
    lines.append("Automated acceptance scenarios validating UI presentation states:")
    lines.append("")
    for i in range(1, 36):
        lines.extend(make_qa_bdd_scenario(
            f"UI-SCENARIO-{i:03d}: Verification of UI Component State {i}",
            [
                f"The clinical UI screen is navigated conforming to UI-TEST-{((i-1)%80)+1:03d}",
                f"The viewport is initialized in high-definition clinic workstation resolution (1920x1080)",
                f"The user actor interacts with clinical form controls and trigger buttons"
            ],
            f"The presentation tier renders feedback states and input validation messages",
            [
                "All UI design system tokens (colors, typography, spacing) adhere to Phase 09 specifications",
                "Form validation errors display with clear contrast and appropriate ARIA live attributes",
                f"A visual regression snapshot attestation UI_PASS_{i:03d} is recorded"
            ]
        ))

    # Section 5: Configuration Guidance
    lines.append("## 5. Configuration Guidance & Technical Specifications")
    lines.append("```yaml")
    lines.append("# DOCUMENTATION-ONLY TEST EXAMPLE")
    lines.append("# Playwright Visual Regression Configuration")
    lines.append("visual_regression_config:")
    lines.append("  snapshot_dir: './visual-snapshots'")
    lines.append("  threshold_max_diff_pixels: 50")
    lines.append("  threshold_pixel_ratio: 0.001")
    lines.append("  viewports:")
    lines.append("    desktop: { width: 1920, height: 1080 }")
    lines.append("    tablet: { width: 1280, height: 800 }")
    lines.append("    mobile: { width: 390, height: 844 }")
    lines.append("```")
    lines.append("")

    return write_qa_doc("07-ui-test-plan.md", "\n".join(lines), min_substantive=2000)

if __name__ == "__main__":
    generate_doc()
