# 📜 Annual Data Governance Review Charter & Audit Checklist
## Namma Clinic Digital Health & Operations Platform
### Joint Standing Governance Review: GBA / BBMP & K Mati
### Document Code: DG-REV-05 | Version: 1.0 | Date: September 2026

---

## 1. Governance Committee Mandate

The **Joint Health Data Governance Committee (JHDGC)** is formally chartered to conduct an **Annual Data Governance Review** every September to ensure that all patient data management, system security, access privileges, algorithm outputs, and data exchange interfaces strictly uphold citizen privacy, legal compliance (DPDP Act 2023, IT Act 2000), and public interest objectives.

### Committee Structure

| Position | Designated Official | Organization | Voting Authority |
| :--- | :--- | :--- | :---: |
| **Chairperson** | Special Commissioner (Health) / Additional Director | GBA / BBMP | Casts deciding vote |
| **Vice-Chairperson** | Chief Health Officer (Public Health) | BBMP Health Dept | Standard Member |
| **IT & Security Lead** | IT Cell Coordinator / Senior Cyber Consultant | BBMP | Standard Member |
| **Legal Advisor** | Legal Counsel (Health & Data Protection) | GBA / BBMP | Advisory Member |
| **Vendor Program Rep**| Project Director | K Mati | Standard Member |
| **Vendor Security Rep** | Chief Information Security Officer (CISO) | K Mati | Standard Member |
| **Vendor Clinical Rep** | Lead Clinical Advisor | K Mati | Standard Member |

---

## 2. Review Cycle & Timelines

* **Annual Notification:** August 15 (Formal audit notice issued by BBMP IT Cell).
* **Self-Audit & Evidence Gathering:** August 15 – August 31 (K Mati compiles technical and access logs).
* **Formal Inspection Sessions:** September 1 – September 15 (Joint inspection of server logs, backup media, and clinic endpoints).
* **Review Report & Remediation Directives:** September 20 (Published to the Special Commissioner).
* **Annual Re-Certification Issued:** September 30.

---

## 3. Comprehensive 25-Point Data Governance Audit Checklist

### Domain A: Legal Ownership & Vendor Boundaries
- [ ] **A.1:** Written attestation verified confirming 100% GBA/BBMP ownership of all patient data.
- [ ] **A.2:** Zero commercial monetization or external training of AI models using clinic datasets verified.
- [ ] **A.3:** Source code escrow repository updated with latest production release tag.
- [ ] **A.4:** Physical data residency verified within India across all primary and replica instances.
- [ ] **A.5:** Third-party sub-processors (SMS gateway, cloud hosting) audited for valid NDAs and DPDP compliance.

### Domain B: Access Controls & Identity Management
- [ ] **B.1:** Complete reconciliation of all active clinic user accounts against official BBMP staff rosters.
- [ ] **B.2:** Dormant accounts (> 30 days of inactivity) systematically identified and deactivated.
- [ ] **B.3:** Multi-Factor Authentication (MFA) enforcement verified for 100% of administrative and zonal roles.
- [ ] **B.4:** Privilege escalation checks executed to ensure receptionists/nurses cannot access administrative settings.
- [ ] **B.5:** Emergency "break-glass" access logs audited for valid clinical justifications.

### Domain C: Cryptography, Privacy & Security
- [ ] **C.1:** TLS 1.2+ configuration verified across all domain endpoints (A+ SSL Labs rating).
- [ ] **C.2:** Database encryption at rest (AES-256) verified with AWS KMS / HSM key rotation.
- [ ] **C.3:** Quarterly CERT-In empanelled VAPT audit report reviewed; all high/critical findings resolved.
- [ ] **C.4:** Citizen consent recording verified for all ABHA-linked health information sharing.
- [ ] **C.5:** Pseudonymization / de-identification routines tested on analytical export feeds.

### Domain D: Audit Logging & Disaster Recovery
- [ ] **D.1:** Audit log hash chain integrity verified with zero broken links across the preceding 12 months.
- [ ] **D.2:** 180-day minimum log retention verified in immutable WORM storage.
- [ ] **D.3:** Live disaster recovery restoration drill conducted: Recovery Point Objective (RPO) $< 1$ hour, Recovery Time Objective (RTO) $< 4$ hours.
- [ ] **D.4:** Automated daily snapshot generation verified with automated test restore validation.
- [ ] **D.5:** Security incident log reviewed; confirmation of zero unreported CERT-In breaches.

### Domain E: AI & Algorithmic Governance
- [ ] **E.1:** Stock-out prediction algorithm evaluated for false-positive and false-negative variance.
- [ ] **E.2:** Epidemiological disease cluster anomaly detection verified against field outbreak reality.
- [ ] **E.3:** Confirmation that zero AI models execute autonomous clinical diagnosis without doctor sign-off.
- [ ] **E.4:** Bilingual clinical transliteration accuracy verified across Kannada prescriptions.
- [ ] **E.5:** Patient NCD recall notification logs audited for spam prevention and opt-out compliance.

---

## 4. Annual Certification of Compliance

Upon unanimous satisfaction of the checklist items, the Committee executes the **Annual Health Data Governance Certificate**:

```
CERTIFICATE OF COMPLIANCE — HEALTH DATA GOVERNANCE & SECURITY
Reference: BBMP-HDG-CERT-2026-01

This is to certify that the Namma Clinic Digital Health & Operations Platform has successfully
undergone the Annual Joint Data Governance Review for the year 2026. The platform is declared
fully compliant with the DPDP Act 2023, CERT-In cybersecurity directives, and the Sovereign Data
Ownership Covenant of the Greater Bengaluru Authority / BBMP.

Granted on this 30th day of September 2026.

__________________________________________          __________________________________________
Chairperson, JHDGC                                  IT & Security Lead
Special Commissioner (Health), GBA / BBMP           BBMP Health Department
```
