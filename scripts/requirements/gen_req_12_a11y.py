#!/usr/bin/env python3
"""
gen_req_12_a11y.py
Generates docs/02-requirements/12-accessibility-requirements.md
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_a11y import A11Y_REQUIREMENTS
from gen_base import generate_document

def render_a11y_invariants(r):
    return [
        f"- **WCAG Success Criteria:** {r['wcag_success_criteria']}: {r['accessibility_criterion']}",
        f"- **Target Beneficiary User Group:** {r['target_user_group']}",
        f"- **Design Implementation Pattern:** {r['design_implementation']}",
        f"- **Verification Tooling:** {r['verification_method']}",
        f"- **Accountable Accessibility Lead:** {r['owner']}"
    ]

def main():
    exec_summary = (
        "This specification defines the comprehensive accessibility and universal usability requirements baseline "
        "for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. "
        "Comprising 40 detailed accessibility specifications (`A11Y-001` through `A11Y-040`), this document operationalizes the "
        "Web Content Accessibility Guidelines (WCAG) 2.1 Level AA standards and complies with the Rights of Persons with Disabilities "
        "(RPwD) Act 2016.\n\n"
        "Healthcare workers operating in fast-paced municipal clinics encounter diverse physical environments, low-cost reflective monitors, "
        "keyboard-only workstations, and varying degrees of physical and sensory capabilities. Elderly citizens and persons with disabilities "
        "also visit clinics daily. The platform enforces high contrast ratios (4.5:1 text, 7:1 enhanced), complete keyboard navigability with "
        "visible focus indicators, screen reader ARIA semantic compatibility, touch targets >=48x48px, and low-literacy iconographic aids."
    )

    mermaid_diagram = """graph TD
    subgraph InputMethods["Multi-Modal Input Navigation"]
        KEYBOARD["100% Keyboard Operable | Logical Tab Order | Focus Ring"]
        TOUCH["Touch Hit Targets: Minimum 48x48px with 8px Spacing"]
        VOICE["Screen Reader Semantics | ARIA Live Regions | NVDA/JAWS"]
    end
    subgraph VisualPerception["Visual Inclusivity & Contrast Engine"]
        CONTRAST["Color Contrast: >=4.5:1 Normal Text | >=3:1 UI Components"]
        ZOOM["Display Zoom: 200% Lossless Scaling Without Horizontal Scroll"]
        THEME["High-Contrast Theme | Dark/Light Mode Preference"]
    end
    subgraph CognitiveAids["Cognitive & Low-Literacy Usability"]
        ICONS["Bilingual Text Paired with Universal ISO Healthcare Icons"]
        ERRORS["Inline Redundant Error Validation (Color + Icon + Text)"]
        AUDIO["Optional Audio Chimes for Critical Emergency Alerts"]
    end
    InputMethods --> VisualPerception --> CognitiveAids"""

    domain_cols = ("WCAG SC", "Target User Group", "Design Implementation", "Verification Tool", "Owner")
    extractors = [
        lambda r: f"`{r['wcag_success_criteria']}`",
        lambda r: f"{r['target_user_group']}",
        lambda r: f"{r['design_implementation'][:35]}...",
        lambda r: f"{r['verification_method'][:25]}...",
        lambda r: f"{r['owner']}"
    ]

    governance = (
        "This Accessibility Requirements Specification establishes the binding universal usability contract. "
        "Pull requests must pass automated axe-core accessibility gates with zero violations prior to deployment approval. "
        "User testing with disabled healthcare workers and senior citizens is conducted quarterly."
    )

    generate_document(
        doc_num="12",
        doc_slug="12-accessibility-requirements.md",
        doc_id="DOC-REQ-012-A11Y",
        doc_title="Accessibility & Universal Usability Requirements Baseline",
        req_type="Accessibility Requirement",
        req_range="A11Y-001 through A11Y-040",
        count=40,
        requirements=A11Y_REQUIREMENTS,
        exec_summary=exec_summary,
        mermaid_diagram=mermaid_diagram,
        domain_table_cols=domain_cols,
        domain_col_extractors=extractors,
        domain_invariant_renderer=render_a11y_invariants,
        governance_text=governance,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="11-localization-requirements.md"
    )

if __name__ == "__main__":
    main()
