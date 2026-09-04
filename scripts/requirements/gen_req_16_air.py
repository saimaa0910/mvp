#!/usr/bin/env python3
"""
gen_req_16_air.py
Generates docs/02-requirements/16-ai-requirements.md
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from data_air import AIR_REQUIREMENTS
from gen_base import generate_document

def render_air_invariants(r):
    return [
        f"- **Clinical Advisory Scope:** {r['clinical_advisory_scope']}",
        f"- **Advisory Model Architecture:** `{r['ml_model_family']}`",
        f"- **Mandatory Human Override Protocol:** {r['human_override_protocol']}",
        f"- **Verification Protocol:** {r['verification_method']}",
        f"- **Accountable Clinical AI Lead:** {r['owner']}"
    ]

def main():
    exec_summary = (
        "This specification defines the comprehensive artificial intelligence, machine learning, and clinical decision-support "
        "requirements baseline for the Namma Clinic Digital Health Platform across 183 primary urban healthcare centers in Greater Bengaluru. "
        "Comprising 40 rigorous specifications (`AIR-001` through `AIR-040`), this document operationalizes the ethical, clinical, and "
        "governance boundaries for syndromic anomaly detection, Essential Drug List (EDL) demand forecasting, maternal risk stratification, "
        "drug-drug interaction checking, and explainable AI feature attribution.\n\n"
        "**CRITICAL CLINICAL PRIMACY DOCTRINE:** The platform provides clinical decision support exclusively in an advisory capacity. "
        "The system MUST NOT independently diagnose, prescribe, discharge, or make irreversible clinical decisions. The qualified Medical "
        "Officer retains sole legal and professional responsibility for all clinical interventions. Mandatory human-in-the-loop override "
        "mechanisms and immutable WORM audit logs are enforced across 100% of AI recommendations."
    )

    mermaid_diagram = """graph TD
    subgraph ClinicalInput["Frontline Clinical Encounter"]
        PATIENT["Patient Symptoms & Vital Signs"]
        RX["Prescription & Drug Selection"]
        LAB["Lab Diagnostic Findings"]
    end
    subgraph AdvisoryEngine["Advisory Intelligence Tier (Non-Autonomous)"]
        CDS["Clinical Decision Support Rules"]
        ML_MODEL["Advisory ML Models (ONNX / Scikit-Learn)"]
        CONF["Confidence Evaluator (<70% Suppresses Prompt)"]
        EXPLAIN["SHAP Feature Attribution Explainer"]
        CDS --> ML_MODEL --> CONF --> EXPLAIN
    end
    subgraph HumanOversight["Mandatory Human-in-the-Loop Gateway"]
        DOCTOR["Licensed Medical Officer (Sole Decision Authority)"]
        ACTION{"Doctor Decision"}
        ACCEPT["Accept Recommendation"]
        OVERRIDE["Override with Justification Reason"]
        DOCTOR --> ACTION
        ACTION --> ACCEPT
        ACTION --> OVERRIDE
    end
    subgraph AuditVault["Immutable Compliance Vault"]
        WORM["WORM Log: Model Version | Prompt | Doctor Action | Reason"]
        ACCEPT --> WORM
        OVERRIDE --> WORM
    end
    ClinicalInput --> AdvisoryEngine --> HumanOversight"""

    domain_cols = ("Advisory Scope", "Priority", "Model Family", "Human Override Protocol", "Clinical Lead")
    extractors = [
        lambda r: f"`{r['clinical_advisory_scope']}`",
        lambda r: f"`{r['priority']}`",
        lambda r: f"`{r['ml_model_family'][:30]}`",
        lambda r: f"{r['human_override_protocol'][:35]}...",
        lambda r: f"{r['owner']}"
    ]

    governance = (
        "This AI Requirements Specification establishes the binding clinical and algorithmic governance baseline. "
        "Under no circumstances may an AI component execute clinical decisions without qualified human oversight. "
        "All models are subject to annual retrospective clinical audits and continuous concept drift monitoring."
    )

    generate_document(
        doc_num="16",
        doc_slug="16-ai-requirements.md",
        doc_id="DOC-REQ-016-AIR",
        doc_title="Artificial Intelligence & Clinical Decision Support Requirements Baseline",
        req_type="AI Decision-Support Requirement",
        req_range="AIR-001 through AIR-040",
        count=40,
        requirements=AIR_REQUIREMENTS,
        exec_summary=exec_summary,
        mermaid_diagram=mermaid_diagram,
        domain_table_cols=domain_cols,
        domain_col_extractors=extractors,
        domain_invariant_renderer=render_air_invariants,
        governance_text=governance,
        parent_baseline="05-clinical-rules.md",
        counterpart="07-security-requirements.md"
    )

if __name__ == "__main__":
    main()
