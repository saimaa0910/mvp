# 🔒 Data Privacy & Governance Annexure
## Namma Clinic Digital Health Platform
### K Mati | September 2026

---

## 1. Purpose

This annexure establishes the data privacy, protection, governance, and compliance framework for the Namma Clinic Digital Health Platform. It defines roles, responsibilities, data handling procedures, and regulatory compliance measures to ensure the highest standards of patient data protection.

---

## 2. Applicable Regulations

| Regulation | Applicability | Compliance Status |
|---|---|---|
| **Digital Personal Data Protection Act, 2023 (DPDP Act)** | Primary data protection law for India | ✅ Compliant by design |
| **Information Technology Act, 2000** (Section 43A, 72A) | Data security, breach penalties | ✅ Compliant |
| **CERT-In Directions (April 2022)** | Incident reporting, log retention | ✅ Compliant |
| **ABDM Health Data Management Policy** | Health data standards for ABDM ecosystem | ✅ Compliant |
| **EHR Standards (MoHFW, 2016)** | Electronic Health Record standards for India | ✅ Aligned |
| **Clinical Establishments Act** | Clinical record keeping | ✅ Aligned |

---

## 3. Data Classification

### 3.1 Categories

| Category | Classification | Examples | Access Control |
|---|---|---|---|
| **Patient Health Data** | **Highly Sensitive** | Vitals, diagnoses, prescriptions, lab results, conditions | Role-based; encrypted at rest; audit logged |
| **Patient Demographics** | **Sensitive** | Name, age, gender, mobile, address, ABHA ID | Role-based; encrypted at rest |
| **Operational Data** | **Internal** | Stock levels, indents, referral metadata, token queues | Role-based |
| **Analytics / Aggregate Data** | **Internal** | Zone-wise footfall, disease breakdown, stock stats | Dashboard role-based |
| **System Data** | **Confidential** | Audit logs, user credentials, API keys, certificates | Admin only; encrypted |

### 3.2 Data Handling Rules

| Data Category | Collection | Storage | Sharing | Retention |
|---|---|---|---|---|
| Patient Health Data | Explicit purpose (treatment) | Encrypted (AES-256) in cloud DB | Only with patient consent (ABDM) | Indefinite (clinical requirement) |
| Patient Demographics | Registration consent | Encrypted in cloud DB | Internal only; ABDM with consent | Indefinite |
| Operational Data | Automatic from workflows | Cloud DB | Internal dashboards only | 5 years |
| Analytics Data | Aggregated, anonymized | Analytics warehouse | Reports to BBMP officials | 5 years |

---

## 4. Data Ownership & Processing

### 4.1 Roles Under DPDP Act

| DPDP Act Role | Entity | Responsibilities |
|---|---|---|
| **Data Fiduciary** | GBA / BBMP Health Department | Determines purpose and means of processing; ultimate responsibility |
| **Data Processor** | K Mati Analytics Pvt Ltd | Processes data on behalf of and under instruction from Data Fiduciary |
| **Data Principal** | Patient (citizen) | The individual whose data is being processed |

### 4.2 Data Fiduciary Obligations (BBMP)

1. Obtain valid consent from Data Principals (patients) for data collection
2. Process data only for specified healthcare purposes
3. Ensure Data Processor (K Mati) complies with DPDP Act
4. Respond to Data Principal rights requests (access, correction, erasure)
5. Notify Data Protection Board in case of data breach

### 4.3 Data Processor Obligations (K Mati)

1. Process data **only** as instructed by Data Fiduciary
2. Implement appropriate technical and organizational security measures
3. Assist Data Fiduciary in responding to Data Principal rights requests
4. Delete or return all data upon termination of contract
5. Not engage sub-processors without prior written consent of Data Fiduciary
6. Maintain records of all processing activities

---

## 5. Patient Consent Framework

### 5.1 Consent at Registration

At the time of patient registration, the platform will display a consent notice:

> **Consent Notice (English):**
> "Your personal and health information will be recorded digitally by Namma Clinic (BBMP) for the purpose of providing healthcare services. Your data is securely stored and will not be shared without your consent. You have the right to access, correct, or request deletion of your data."

> **ಒಪ್ಪಿಗೆ ಸೂಚನೆ (ಕನ್ನಡ):**
> "ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ಮತ್ತು ಆರೋಗ್ಯ ಮಾಹಿತಿಯನ್ನು ಆರೋಗ್ಯ ಸೇವೆಗಳನ್ನು ಒದಗಿಸುವ ಉದ್ದೇಶಕ್ಕಾಗಿ ನಮ್ಮ ಕ್ಲಿನಿಕ್ (BBMP) ಡಿಜಿಟಲ್ ಆಗಿ ದಾಖಲಿಸಲಾಗುತ್ತದೆ. ನಿಮ್ಮ ಡೇಟಾ ಸುರಕ್ಷಿತವಾಗಿ ಸಂಗ್ರಹಿಸಲಾಗಿದೆ ಮತ್ತು ನಿಮ್ಮ ಒಪ್ಪಿಗೆಯಿಲ್ಲದೆ ಹಂಚಿಕೊಳ್ಳಲಾಗುವುದಿಲ್ಲ."

### 5.2 ABDM Consent

For ABDM health record sharing (Phase 3+), a separate granular consent will be obtained via the ABDM consent manager:
- Patient selects which records to share
- Patient selects with whom to share
- Patient sets consent validity period
- Consent is digitally signed and auditable

---

## 6. Data Security Measures

### 6.1 Technical Controls

| Layer | Control | Implementation |
|---|---|---|
| **Encryption in Transit** | TLS 1.2+ | All API endpoints, no HTTP allowed |
| **Encryption at Rest** | AES-256 | RDS, S3, EBS volumes |
| **Authentication** | Username + Password | bcrypt hashing (cost factor 12) |
| **Multi-Factor Auth** | TOTP (Time-based OTP) | Mandatory for Admin, Commissioner roles |
| **Session Management** | JWT with 15-min expiry | Refresh token rotation |
| **Access Control** | Role-Based (RBAC) | 8 defined roles with least-privilege |
| **API Security** | Rate limiting, input validation | Express middleware + WAF |
| **Database Security** | Private subnet, no public access | VPC, Security Groups |
| **Backup** | Daily automated snapshots | 30-day retention, encrypted |
| **Key Management** | AWS KMS | Managed key rotation |

### 6.2 Organizational Controls

| Control | Implementation |
|---|---|
| Background checks for K Mati employees | Mandatory before project access |
| Individual NDAs | Signed by all team members with production data access |
| Access provisioning workflow | Written request → Manager approval → IT provisioning |
| Access review | Quarterly review of all user accounts; deactivate unused |
| Security awareness training | Annual for all K Mati project staff |
| Clean desk policy | No patient data on personal devices, printouts, or whiteboards |

### 6.3 Incident Response Plan

| Step | Action | Timeline | Responsible |
|---|---|---|---|
| 1 | Detect & Confirm | Immediate | Monitoring alerts / Staff report |
| 2 | Contain | Within 30 minutes | K Mati DevOps + Security Lead |
| 3 | Assess Impact | Within 2 hours | K Mati CISO |
| 4 | Notify BBMP (Data Fiduciary) | Within 4 hours | K Mati Project Director |
| 5 | Report to CERT-In | Within 6 hours | K Mati CISO |
| 6 | Notify affected Data Principals | As directed by DPDP Act | BBMP (assisted by K Mati) |
| 7 | Remediate | Within 24–72 hours | K Mati Development Team |
| 8 | Post-Incident Review | Within 1 week | Joint K Mati + BBMP |

---

## 7. Data Principal Rights

Under the DPDP Act 2023, patients have the following rights:

| Right | Implementation |
|---|---|
| **Right to Access** | Patient can request their health records via clinic reception; data provided within 7 business days |
| **Right to Correction** | Patient can request correction of demographic or health data; processed within 3 business days |
| **Right to Erasure** | Patient can request deletion of non-clinical data; clinical records retained per regulatory requirements |
| **Right to Grievance Redressal** | Complaints routed to BBMP Data Protection Officer |
| **Right to Nominate** | Patient can nominate a representative for data access in case of death/incapacity |

---

## 8. Data Retention & Disposal

| Data Type | Retention Period | Disposal Method |
|---|---|---|
| Patient clinical records | Indefinite (as per Clinical Establishments Act and MCI guidelines) | Not deleted; archived after 10 years of inactivity |
| Patient demographics | Indefinite (linked to clinical records) | Anonymized if requested (name/mobile removed) |
| Audit logs | 5 years (CERT-In: minimum 180 days) | Secure deletion after retention period |
| System backups | 30 days (rolling) | Automatic expiry and deletion |
| User accounts (deactivated) | 1 year after deactivation | Anonymized after 1 year |

---

## 9. Audit & Compliance

### 9.1 Audit Trail

Every action on the platform is logged:

| Log Field | Description |
|---|---|
| `timestamp` | When the action occurred (UTC) |
| `user_id` | Who performed the action |
| `user_role` | Role at time of action |
| `action` | What was done (CREATE, READ, UPDATE, DELETE) |
| `entity` | Which data entity (patient, visit, prescription, etc.) |
| `entity_id` | Specific record ID |
| `ip_address` | Source IP address |
| `clinic_id` | Which clinic |
| `old_value` | Previous value (for UPDATE) |
| `new_value` | New value (for UPDATE) |

### 9.2 Compliance Reviews

| Review | Frequency | Conducted By |
|---|---|---|
| VAPT (Vulnerability Assessment) | Quarterly | CERT-In empanelled auditor |
| Access Control Review | Quarterly | K Mati Security Lead + BBMP IT Cell |
| Data Privacy Impact Assessment | Annually | External privacy consultant |
| Audit Log Review | Monthly | K Mati CISO |
| DPDP Act Compliance Assessment | Annually | External legal advisor |

---

## 10. Data Governance Committee

### Proposed Composition

| Member | Role |
|---|---|
| Addl Director Health, BBMP | Chair |
| K Mati Project Director | Member |
| BBMP IT Cell Coordinator | Member |
| K Mati CISO / Security Lead | Member |
| External Privacy Advisor (if appointed) | Advisor |

### Responsibilities

1. Review and approve data privacy policies annually
2. Review audit findings and remediation plans
3. Approve any new data sharing arrangements
4. Review and respond to data breach incidents
5. Approve changes to data retention policies

---

**Document Control**

| Version | Date | Author | Status |
|---|---|---|---|
| 1.0 | Sep 2, 2026 | K Mati — Legal & Compliance Team | Draft for BBMP Review |

---
*© 2026 Kushagramati Analytics Pvt Ltd. Confidential — Prepared for GBA / BBMP Health Department.*
