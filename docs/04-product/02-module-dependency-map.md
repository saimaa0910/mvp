# 🔗 Module Dependency Map & Build Order
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PRD-DEP-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Architectural Module Prerequisites
1. **Tier 0 (Prerequisites):** MOD-01 (Auth), MOD-02 (RBAC), MOD-03 (Org), MOD-04 (Staff).
2. **Tier 1 (Patient Intake):** MOD-05 (Patient), MOD-06 (Consent), MOD-07 (Queue), MOD-08 (Triage).
3. **Tier 2 (Clinical Care):** MOD-09 (Doctor), MOD-10 (Diagnosis), MOD-11 (Prescription), MOD-12 (Lab).
4. **Tier 3 (Fulfillment):** MOD-13 (Pharmacy), MOD-14 (Stock), MOD-17 (Referrals).
5. **Tier 4 (Advanced):** MOD-21 (Audit), MOD-22 (Analytics), MOD-24 (ABDM), MOD-25 (Offline Sync).
