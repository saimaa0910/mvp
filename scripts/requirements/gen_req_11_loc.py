#!/usr/bin/env python3
"""
gen_req_11_loc.py
Generates docs/02-requirements/11-localization-requirements.md
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_loc import LOC_REQUIREMENTS
from gen_base import generate_document

def render_loc_invariants(r):
    return [
        f"- **UI Context / Domain:** {r['ui_context']}",
        f"- **Standard Applied:** {r['standard_applied']}",
        f"- **Canonical Kannada Sample:** **{r['kannada_sample']}**",
        f"- **English Parallel Sample:** {r['english_sample']}",
        f"- **Translation Owner:** {r['translation_owner']}",
        f"- **Verification Protocol:** {r['verification_method']}"
    ]

def main():
    exec_summary = (
        "This specification defines the comprehensive localization and linguistic equity requirements baseline "
        "for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. "
        "Comprising 40 detailed localization specifications (`LOC-001` through `LOC-040`), this document guarantees 100% "
        "bilingual parity between Kannada (ಕನ್ನಡ) and English across all clinical and administrative interfaces.\n\n"
        "Frontline healthcare delivery in Bengaluru relies heavily on auxiliary nurses, pharmacists, and lab technicians who "
        "communicate primarily in Kannada. The platform treats Kannada localization not as an optional cosmetic overlay, but as a "
        "core functional prerequisite for patient safety, clinical accuracy, and operational dignity. Every requirement defines strict "
        "Unicode normalization (Unicode 15.0 NFC), Noto Sans Kannada rendering, bilingual thermal printing, and translation governance."
    )

    mermaid_diagram = """graph TD
    subgraph LocaleEngine["Client-Side i18n Engine"]
        TOGGLE["Runtime Locale Switcher: Kannada (kn) | English (en)"]
        CATALOG["JSON Translation Catalog (Offline Service Worker Cached)"]
        FONT["Noto Sans Kannada Typography (Unicode 15.0 NFC)"]
        TOGGLE --> CATALOG --> FONT
    end
    subgraph Formatting["Indian Regional Formatting Engine"]
        DATE["Date/Time: DD/MM/YYYY hh:mm A"]
        CURR["Currency: INR (₹) Lakhs/Crores Formatting"]
        NUM["Numbers: International Numerals & Kannada Numerals"]
    end
    subgraph Output["Multi-Channel Output Tier"]
        SCREEN["High-DPI Responsive Web UI"]
        PRINT["ESC/POS Thermal Printer Raster Font Engine"]
        SMS["Bilingual Unicode SMS Gateway"]
    end
    CATALOG --> Formatting --> Output"""

    domain_cols = ("UI Context Domain", "Standard Applied", "Kannada Sample", "English Parallel", "Translation Owner")
    extractors = [
        lambda r: f"`{r['ui_context']}`",
        lambda r: f"`{r['standard_applied']}`",
        lambda r: f"**{r['kannada_sample']}**",
        lambda r: f"{r['english_sample']}",
        lambda r: f"{r['translation_owner']}"
    ]

    governance = (
        "This Localization Requirements Specification guarantees language equity across Greater Bengaluru's municipal clinics. "
        "All translation bundles undergo review by certified Kannada linguists before promotion to production. "
        "Zero hardcoded English strings or unlocalized UI components are allowed in production builds."
    )

    generate_document(
        doc_num="11",
        doc_slug="11-localization-requirements.md",
        doc_id="DOC-REQ-011-LOC",
        doc_title="Localization & Language Equity Requirements Baseline",
        req_type="Localization Requirement",
        req_range="LOC-001 through LOC-040",
        count=40,
        requirements=LOC_REQUIREMENTS,
        exec_summary=exec_summary,
        mermaid_diagram=mermaid_diagram,
        domain_table_cols=domain_cols,
        domain_col_extractors=extractors,
        domain_invariant_renderer=render_loc_invariants,
        governance_text=governance,
        parent_baseline="03-non-functional-requirements.md",
        counterpart="12-accessibility-requirements.md"
    )

if __name__ == "__main__":
    main()
