# 🛡️ Comprehensive Project Risk Register & Mitigation Matrix
## Namma Clinic Digital Health & Operations Platform
### Document Code: PM-RSK-04 | Version: 1.0 | Review Frequency: Monthly
### Last Reviewed: 02-September-2026 | Next Review: 02-October-2026

---

## 1. Risk Management Framework

Risks are assessed using a standard $5 \times 5$ Probability & Impact matrix:
* **Probability (P):** 1 (Very Low: <10%), 2 (Low: 10–25%), 3 (Medium: 26–50%), 4 (High: 51–75%), 5 (Very High: >75%)
* **Impact (I):** 1 (Negligible), 2 (Minor), 3 (Moderate), 4 (Major), 5 (Catastrophic)
* **Risk Score:** $R = P \times I$
  * **Critical (Red):** 15 – 25
  * **High (Amber):** 10 – 14
  * **Medium (Yellow):** 5 – 9
  * **Low (Green):** 1 – 4

---

## 2. Active Risk Register

| Risk ID | Category | Risk Description | P | I | Score | Early Warning Indicator | Mitigation & Preventive Controls | Contingent Action Plan | Owner | Status |
| :---: | :---: | :--- | :---: | :---: | :---: | :--- | :--- | :--- | :---: | :---: |
| **RSK-OP-01** | Operational | **Frontline Clinic Staff Resistance & Paper Reversion**<br>Clinic doctors/nurses revert to handwritten registers during peak hours (9–11 AM) due to typing burden. | 4 | 4 | **16 (Red)** | Digital registration drop below 75% between 9:00 AM and 11:30 AM in daily logs. | • 1-tap quick pick clinical templates.<br>• Minimal mandatory fields.<br>• On-site champion nurse assigned per clinic.<br>• Recognition awards from BBMP for top digital clinics. | Deploy field trainers for 3-day on-site elbow support; conduct peer discussion led by Clinical Advisor. | Field Lead (FL) | Active |
| **RSK-TC-02** | Technical | **Unstable Broadband & 4G Connectivity Disruptions**<br>Intermittent broadband outages during monsoons causing consultation workflow freezing. | 4 | 4 | **16 (Red)** | Offline sync queue depth > 20 records; ping failure on primary gateway. | • Progressive Web App (PWA) with Service Worker.<br>• IndexedDB local offline cache.<br>• Auto-switch to dual-SIM 4G backup router.<br>• Automatic background sync when reconnected. | Continue offline clinic flow; sync batch upload at end of day via mobile hotspot if needed. | Solution Architect (SA) | Active |
| **RSK-SEC-03**| Security | **Unauthorized Health Data Access or Patient Data Leak**<br>Compromise of clinic login credentials or unauthorized extraction of identifiable medical records. | 2 | 5 | **10 (Amber)**| Multiple failed login attempts (>5); anomalous bulk export requests. | • Strict Role-Based Access Control (RBAC).<br>• MFA for administrative and zonal tiers.<br>• AES-256 at rest, TLS 1.3 in transit.<br>• Immutable audit trail logging all record reads. | Immediate account lockout; IP block via WAF; CERT-In incident notification within 6 hours. | Security Lead / SA | Monitored |
| **RSK-INT-04**| Integration| **ABDM / ABHA Sandbox API Breaking Schema Changes**<br>National Health Authority (NHA) introduces unannounced modifications to ABHA M1/M2 endpoints. | 3 | 4 | **12 (Amber)**| Sandbox test failure on automated nightly integration test suite. | • Encapsulate ABDM logic behind an internal microservice adapter.<br>• Maintain fallback to manual demographic registration.<br>• Continuous monitoring of NHA developer release notes. | Gracefully degrade to offline/local demographic capture; queue ABHA linking requests for asynchronous verification. | SA | Monitored |
| **RSK-CLI-05**| Clinical | **Drug Formulary Discrepancies & Stock Unit Mismatch**<br>Frontline doctors prescribe brand names while pharmacy stocks generic bulk or different tablet strengths. | 3 | 3 | **9 (Yellow)**| Helpdesk complaints regarding "medicine not found" in dropdown selector. | • Clinical Advisor-curated master mapped to Karnataka KSDLPS essential drug list.<br>• Automatic generic-to-brand synonym search mapping.<br>• Batch/expiry validation during dispense. | Pharmacist override button with mandatory reason capture and weekly formulary review. | Clinical Advisor (CA) | Active |
| **RSK-GOV-06**| Governance | **Administrative Transfers of Key BBMP Officials**<br>Reassignment of Zonal Medical Officers or IT Coordinators leading to project champion loss. | 3 | 3 | **9 (Yellow)**| Transfer orders gazetted by urban development department. | • Detailed standard operating procedures and governance charter.<br>• Fortnightly documented reporting to Special Commissioner.<br>• Multiple nodal officers briefed in each zone. | Rapid onboarding briefing with incoming officials within 5 working days of joining. | Project Director (PD) | Monitored |
| **RSK-DEV-07**| Technical | **Power Outages & Hardware Malfunction in Clinics**<br>Sudden power drops in peripheral wards without inverter backup corrupting unsaved clinical notes. | 3 | 3 | **9 (Yellow)**| Abrupt session terminations logged on websocket connections. | • 1KVA dedicated UPS with 30-min backup installed for every desktop.<br>• Auto-save draft consultation note to local storage every 15 seconds.<br>• Tablet fallback for triage. | Doctor switches to battery-powered tablet; UPS sustains printer for immediate token slips. | FL | Active |
| **RSK-PRC-08**| Financial | **Procurement & Milestone Invoicing Delays**<br>Bureaucratic processing delays in milestone payment releases causing cash flow strain during citywide scaling. | 2 | 4 | **8 (Yellow)**| Invoice pending with BBMP accounts branch > 20 calendar days past submission. | • Clear, indisputable milestone completion acceptance criteria agreed upfront.<br>• Pre-validation of deliverable packs with Nodal Officer before formal billing. | Pre-arranged project working capital reserve; executive escalation to Special Commissioner. | PD | Monitored |

---

## 3. Monthly Review Log & Audit Trail

| Review Date | Reviewers | Risks Added | Risks Closed | Key Adjustments Made |
| :---: | :--- | :---: | :---: | :--- |
| **02-Sep-2026** | PD, SA, CA, DL, FL | None (Baseline) | None | Initial risk register baselined and approved for Phase 0 completion. |
| **02-Oct-2026** | *(Scheduled)* | — | — | Focus: Post-prototype user feedback risk analysis. |
| **02-Nov-2026** | *(Scheduled)* | — | — | Focus: Pre-pilot field hardware readiness risk audit. |
