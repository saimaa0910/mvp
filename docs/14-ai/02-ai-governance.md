# 🤖 AI Clinical Governance & Ethical Guardrails
## Namma Clinic Digital Health & Operations Platform
**Document Code:** AI-GOV-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Mandatory Clinical AI Principles

```
+-------------------------------------------------------------------------+
|                      MANDATORY AI SAFETY INVARIANTS                     |
+-------------------------------------------------------------------------+
| 1. ZERO AUTONOMOUS DIAGNOSIS                                            |
|    Under zero circumstances will the system generate an autonomous      |
|    clinical diagnosis, triage decision, or final prescription.          |
+-------------------------------------------------------------------------+
| 2. STRICT DECISION SUPPORT ONLY                                         |
|    AI outputs are restricted to decision-support suggestions:           |
|    - Medicine stockout risk forecasting (Supply Chain)                  |
|    - Syndromic fever anomaly detection (Surveillance)                   |
|    - NCD follow-up recall prioritization (Chronic Care)                 |
+-------------------------------------------------------------------------+
| 3. MANDATORY PHYSICIAN OVERRIDE & AUDIT                                 |
|    Every clinical suggestion must be explicitly accepted or rejected by |
|    a licensed Medical Officer; rejections are logged for model tuning.  |
+-------------------------------------------------------------------------+
| 4. EXPLAINABLE INFERENCE & CONFIDENCE SCORES                            |
|    Every prediction must display its confidence score and contributing  |
|    features (e.g. 'Fever cases increased 3.2x above 14-day ward mean'). |
+-------------------------------------------------------------------------+
```
