# 🛡️ Comprehensive Project Risk Register
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-RSK-12 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Top Project Risks & Mitigation Strategies

| Risk ID | Category | Risk Description | Probability | Impact | Score | Mitigation Strategy | Owner |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **RSK-001** | Technical | Prolonged clinic internet outage causing offline sync queue buildup. | High | High | **16** | Robust IndexedDB offline queue with progressive chunked sync and conflict resolution. | Tech Lead |
| **RSK-002** | User Adoption | Doctor resistance to typing electronic prescriptions during peak hours. | High | Critical | **20** | 1-click pre-configured medication bundles; chief complaint chips; minimal typing UX. | Clinical Lead |
| **RSK-003** | Operational | Hardware theft or physical tablet damage in clinic premises. | Med | Med | **9** | Device MDM lock; encrypted local storage; fast spare swap provisioning within 4 hours. | DevOps Lead |
| **RSK-004** | Compliance | Non-compliance with evolving DPDP Act rules regarding minor consent. | Med | High | **12** | Mandatory guardian consent workflow for patients under 18 years old. | Legal / Sec Lead |
