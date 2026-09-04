# Enterprise Risk Management Register & Quantitative Threat Baseline

| Metadata Element | Project Specification |
| :--- | :--- |
| **Document Identifier** | `DOC-PM-012-RISK` |
| **Document Title** | Master Project Risk Register, 5x5 Heat Modeling & Preventive Mitigation Baseline |
| **Project Code** | `NAMMA-CLINIC-PLATFORM-2026` |
| **Document Version** | `v1.0.0-PROD-BASELINE` |
| **Status** | `APPROVED & RATIFIED` |
| **Risk Inventory** | Exactly 100 Formally Monitored Threats (`RISK-001` to `RISK-100`) |
| **Executive Sponsor** | Special Commissioner (Health), Greater Bengaluru Authority (GBA) / BBMP |
| **Clinical Safety Authority** | Chief Health Officer (CHO), BBMP Health Department |
| **Lead Delivery Partner** | Kushagramati Analytics (K Mati) Consortium | Delivery Risk Manager |
| **Upstream Baseline Anchor**| [`06-technical-debt-register.md`](../00-project-baseline/06-technical-debt-register.md) | [`01-project-charter.md`](./01-project-charter.md) |
| **Downstream Governance** | [`13-project-dependencies.md`](./13-project-dependencies.md) | [`14-project-milestones.md`](./14-project-milestones.md) | [`18-change-management.md`](./18-change-management.md) |

---

## 1. Executive Summary & Risk Management Methodology
The **Enterprise Risk Management Register** defines the proactive identification, quantitative probability/impact scoring, continuous monitoring, and structured mitigation protocols for exactly 100 project risks across the 18-sprint / 36-week lifecycle of the Namma Clinic Digital Health & Operations Platform.

### 1.1 Context and Public Healthcare Risk Mandate
Unlike standard commercial web applications, public healthcare systems operating in 183 neighborhood clinics carry immediate clinical, legal, and operational repercussions. Software crashes during morning rush hours delay life-saving diagnoses; prescription synchronization errors risk adverse drug interactions; and non-compliance with the Digital Personal Data Protection (DPDP) Act 2023 incurs statutory penalties up to ₹250 Crore. Risk management is therefore an active, automated engineering discipline integrated into sprint planning and CI/CD pipelines.

### 1.2 Quantitative Scoring & Heat Matrix Formula
Each risk is assessed on a 5-point Probability ($P$) and 5-point Impact ($I$) scale:
$$\text{Risk Exposure Score} = \text{Probability } (1-5) \times \text{Impact } (1-5)$$
The resulting score (1 to 25) determines the threat severity tier and mandatory governance escalation path:
- **Critical (Red: 20 - 25):** Severe threat to patient safety, statutory compliance, or citywide rollout. Bi-weekly review by Executive Steering Committee (`GOV-001`).
- **High (Amber: 12 - 19):** Major operational defect or schedule delay (>2 weeks). Weekly review by Change Control Board (`GOV-003`).
- **Medium (Yellow: 6 - 11):** Moderate technical debt or localized clinic friction. Managed at squad level by Agile Coach (`ROLE-005`).
- **Low (Green: 1 - 5):** Minor cosmetic or administrative issue. Monitored in regular sprint backlog grooming.

## 2. 5x5 Risk Heat Matrix Distribution
Summary distribution of all 100 project risks mapped across probability and impact dimensions:

```mermaid
quadrantChart
    title Namma Clinic 100-Risk Exposure Matrix
    x-axis Low Impact --> Critical Impact
    y-axis Low Probability --> High Probability
    quadrant-1 High Impact / High Probability (Critical Red)
    quadrant-2 Low Impact / High Probability (Operational Amber)
    quadrant-3 Low Impact / Low Probability (Monitor Green)
    quadrant-4 High Impact / Low Probability (Severe Contingency)
    BESCOM Grid Blackout: [0.95, 0.95]
    Lone MO Illness: [0.75, 0.90]
    Slum Fiber Cut: [0.85, 0.90]
    DPDP Non-Consent Penalty: [0.95, 0.40]
    Karnataka EDL Stockout: [0.70, 0.75]
    ABDM Gateway Latency: [0.55, 0.85]
    Thermal Printer Driver Jam: [0.40, 0.70]
    DuckDB Memory Bloat: [0.80, 0.50]
```

## 3. Master Risk Register Summary Table (RISK-001 to RISK-100)
Authoritative catalog of all 100 formally monitored project threats:

| Risk ID | Threat Title | Category | Prob (1-5) | Imp (1-5) | Score (1-25) | Severity | Accountable Role ID | Target Milestone | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| [`RISK-001`](#risk-001) | **BESCOM Grid Blackout Exceeding 1000VA UPS Run...** | `Infrastructure` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) | [`MILESTONE-001`](./14-project-milestones.md#milestone-001) | `MONITORED` |
| [`RISK-002`](#risk-002) | **Dexie.js IndexedDB Quota Eviction on Low-Disk...** | `Technical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) | [`MILESTONE-002`](./14-project-milestones.md#milestone-002) | `MONITORED` |
| [`RISK-003`](#risk-003) | **Web Serial API Disconnects with Thermal Recei...** | `Hardware` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) | [`MILESTONE-003`](./14-project-milestones.md#milestone-003) | `MONITORED` |
| [`RISK-004`](#risk-004) | **Local Clock Skew Causing Outpatient Sync Sequ...** | `Technical` | `2` | `2` | `4` | `LOW` | [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) | [`MILESTONE-004`](./14-project-milestones.md#milestone-004) | `MONITORED` |
| [`RISK-005`](#risk-005) | **Pharmacist Dispensing Sound-Alike Look-Alike ...** | `Clinical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) | [`MILESTONE-005`](./14-project-milestones.md#milestone-005) | `MONITORED` |
| [`RISK-006`](#risk-006) | **High-Dose Pediatric Amoxicillin Calculation E...** | `Clinical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) | [`MILESTONE-006`](./14-project-milestones.md#milestone-006) | `MONITORED` |
| [`RISK-007`](#risk-007) | **Unreconciled FEFO Expiry Dates Dispensing Exp...** | `Clinical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) | [`MILESTONE-007`](./14-project-milestones.md#milestone-007) | `MONITORED` |
| [`RISK-008`](#risk-008) | **Missing Drug Allergy Contraindication in Fast...** | `Clinical` | `2` | `2` | `4` | `LOW` | [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) | [`MILESTONE-008`](./14-project-milestones.md#milestone-008) | `MONITORED` |
| [`RISK-009`](#risk-009) | **Point-of-Care Urine Strip Reader Serial Port ...** | `Hardware` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) | [`MILESTONE-009`](./14-project-milestones.md#milestone-009) | `MONITORED` |
| [`RISK-010`](#risk-010) | **Critical Hemoglobin (<7.0 g/dL) Panic Value D...** | `Clinical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) | [`MILESTONE-010`](./14-project-milestones.md#milestone-010) | `MONITORED` |
| [`RISK-011`](#risk-011) | **Doctor Bypassing Digital Prescription Due to ...** | `Operational` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) | [`MILESTONE-011`](./14-project-milestones.md#milestone-011) | `MONITORED` |
| [`RISK-012`](#risk-012) | **Staff Nurse Omitting Diastolic Blood Pressure...** | `Clinical` | `2` | `2` | `4` | `LOW` | [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) | [`MILESTONE-012`](./14-project-milestones.md#milestone-012) | `MONITORED` |
| [`RISK-013`](#risk-013) | **Walk-in Patient Misidentification in Rapid Qu...** | `Clinical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) | [`MILESTONE-013`](./14-project-milestones.md#milestone-013) | `MONITORED` |
| [`RISK-014`](#risk-014) | **ABHA M1 OTP Gateway Latency Exceeding 45 Seco...** | `Interoperability` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) | [`MILESTONE-014`](./14-project-milestones.md#milestone-014) | `MONITORED` |
| [`RISK-015`](#risk-015) | **Cellular 4G Tower Congestion During Monsoon H...** | `Network` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) | [`MILESTONE-015`](./14-project-milestones.md#milestone-015) | `MONITORED` |
| [`RISK-016`](#risk-016) | **PostgreSQL Connection Starvation During Morni...** | `Technical` | `2` | `2` | `4` | `LOW` | [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) | [`MILESTONE-016`](./14-project-milestones.md#milestone-016) | `MONITORED` |
| [`RISK-017`](#risk-017) | **Redis Queue Memory Saturation from Delayed Sy...** | `Technical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) | [`MILESTONE-017`](./14-project-milestones.md#milestone-017) | `MONITORED` |
| [`RISK-018`](#risk-018) | **Prisma ORM Cold Start Penalty on Micro-VM Nod...** | `Technical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) | [`MILESTONE-018`](./14-project-milestones.md#milestone-018) | `MONITORED` |
| [`RISK-019`](#risk-019) | **DuckDB Memory Footprint Exceeding 2GB Contain...** | `Technical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) | [`MILESTONE-019`](./14-project-milestones.md#milestone-019) | `MONITORED` |
| [`RISK-020`](#risk-020) | **RabbitMQ Dead-Letter Exchange Pile-Up on Malf...** | `Technical` | `2` | `2` | `4` | `LOW` | [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) | [`MILESTONE-020`](./14-project-milestones.md#milestone-020) | `MONITORED` |
| [`RISK-021`](#risk-021) | **Service Worker Cache Poisoning on Production ...** | `Technical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) | [`MILESTONE-021`](./14-project-milestones.md#milestone-021) | `MONITORED` |
| [`RISK-022`](#risk-022) | **Kannada Unicode Font (Noto Sans) Rendering Gl...** | `Usability` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) | [`MILESTONE-022`](./14-project-milestones.md#milestone-022) | `MONITORED` |
| [`RISK-023`](#risk-023) | **Missing Patient Consent Artifacts Under India...** | `Compliance` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) | [`MILESTONE-023`](./14-project-milestones.md#milestone-023) | `MONITORED` |
| [`RISK-024`](#risk-024) | **Thermal Paper Roll Depletion Halting Token Is...** | `Operational` | `2` | `2` | `4` | `LOW` | [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) | [`MILESTONE-024`](./14-project-milestones.md#milestone-024) | `MONITORED` |
| [`RISK-025`](#risk-025) | **Unencrypted Thermal Print Spool Files Retaini...** | `Security` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) | [`MILESTONE-025`](./14-project-milestones.md#milestone-025) | `MONITORED` |
| [`RISK-026`](#risk-026) | **BESCOM Grid Blackout Exceeding 1000VA UPS Run...** | `Infrastructure` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) | [`MILESTONE-026`](./14-project-milestones.md#milestone-026) | `MONITORED` |
| [`RISK-027`](#risk-027) | **Dexie.js IndexedDB Quota Eviction on Low-Disk...** | `Technical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) | [`MILESTONE-027`](./14-project-milestones.md#milestone-027) | `MONITORED` |
| [`RISK-028`](#risk-028) | **Web Serial API Disconnects with Thermal Recei...** | `Hardware` | `2` | `2` | `4` | `LOW` | [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) | [`MILESTONE-028`](./14-project-milestones.md#milestone-028) | `MONITORED` |
| [`RISK-029`](#risk-029) | **Local Clock Skew Causing Outpatient Sync Sequ...** | `Technical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) | [`MILESTONE-029`](./14-project-milestones.md#milestone-029) | `MONITORED` |
| [`RISK-030`](#risk-030) | **Pharmacist Dispensing Sound-Alike Look-Alike ...** | `Clinical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) | [`MILESTONE-030`](./14-project-milestones.md#milestone-030) | `MONITORED` |
| [`RISK-031`](#risk-031) | **High-Dose Pediatric Amoxicillin Calculation E...** | `Clinical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) | [`MILESTONE-031`](./14-project-milestones.md#milestone-031) | `MONITORED` |
| [`RISK-032`](#risk-032) | **Unreconciled FEFO Expiry Dates Dispensing Exp...** | `Clinical` | `2` | `2` | `4` | `LOW` | [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) | [`MILESTONE-032`](./14-project-milestones.md#milestone-032) | `MONITORED` |
| [`RISK-033`](#risk-033) | **Missing Drug Allergy Contraindication in Fast...** | `Clinical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) | [`MILESTONE-033`](./14-project-milestones.md#milestone-033) | `MONITORED` |
| [`RISK-034`](#risk-034) | **Point-of-Care Urine Strip Reader Serial Port ...** | `Hardware` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) | [`MILESTONE-034`](./14-project-milestones.md#milestone-034) | `MONITORED` |
| [`RISK-035`](#risk-035) | **Critical Hemoglobin (<7.0 g/dL) Panic Value D...** | `Clinical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) | [`MILESTONE-035`](./14-project-milestones.md#milestone-035) | `MONITORED` |
| [`RISK-036`](#risk-036) | **Doctor Bypassing Digital Prescription Due to ...** | `Operational` | `2` | `2` | `4` | `LOW` | [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) | [`MILESTONE-036`](./14-project-milestones.md#milestone-036) | `MONITORED` |
| [`RISK-037`](#risk-037) | **Staff Nurse Omitting Diastolic Blood Pressure...** | `Clinical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) | [`MILESTONE-037`](./14-project-milestones.md#milestone-037) | `MONITORED` |
| [`RISK-038`](#risk-038) | **Walk-in Patient Misidentification in Rapid Qu...** | `Clinical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) | [`MILESTONE-038`](./14-project-milestones.md#milestone-038) | `MONITORED` |
| [`RISK-039`](#risk-039) | **ABHA M1 OTP Gateway Latency Exceeding 45 Seco...** | `Interoperability` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) | [`MILESTONE-039`](./14-project-milestones.md#milestone-039) | `MONITORED` |
| [`RISK-040`](#risk-040) | **Cellular 4G Tower Congestion During Monsoon H...** | `Network` | `2` | `2` | `4` | `LOW` | [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) | [`MILESTONE-040`](./14-project-milestones.md#milestone-040) | `MONITORED` |
| [`RISK-041`](#risk-041) | **PostgreSQL Connection Starvation During Morni...** | `Technical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) | [`MILESTONE-001`](./14-project-milestones.md#milestone-001) | `MONITORED` |
| [`RISK-042`](#risk-042) | **Redis Queue Memory Saturation from Delayed Sy...** | `Technical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) | [`MILESTONE-002`](./14-project-milestones.md#milestone-002) | `MONITORED` |
| [`RISK-043`](#risk-043) | **Prisma ORM Cold Start Penalty on Micro-VM Nod...** | `Technical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) | [`MILESTONE-003`](./14-project-milestones.md#milestone-003) | `MONITORED` |
| [`RISK-044`](#risk-044) | **DuckDB Memory Footprint Exceeding 2GB Contain...** | `Technical` | `2` | `2` | `4` | `LOW` | [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) | [`MILESTONE-004`](./14-project-milestones.md#milestone-004) | `MONITORED` |
| [`RISK-045`](#risk-045) | **RabbitMQ Dead-Letter Exchange Pile-Up on Malf...** | `Technical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) | [`MILESTONE-005`](./14-project-milestones.md#milestone-005) | `MONITORED` |
| [`RISK-046`](#risk-046) | **Service Worker Cache Poisoning on Production ...** | `Technical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) | [`MILESTONE-006`](./14-project-milestones.md#milestone-006) | `MONITORED` |
| [`RISK-047`](#risk-047) | **Kannada Unicode Font (Noto Sans) Rendering Gl...** | `Usability` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) | [`MILESTONE-007`](./14-project-milestones.md#milestone-007) | `MONITORED` |
| [`RISK-048`](#risk-048) | **Missing Patient Consent Artifacts Under India...** | `Compliance` | `2` | `2` | `4` | `LOW` | [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) | [`MILESTONE-008`](./14-project-milestones.md#milestone-008) | `MONITORED` |
| [`RISK-049`](#risk-049) | **Thermal Paper Roll Depletion Halting Token Is...** | `Operational` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) | [`MILESTONE-009`](./14-project-milestones.md#milestone-009) | `MONITORED` |
| [`RISK-050`](#risk-050) | **Unencrypted Thermal Print Spool Files Retaini...** | `Security` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) | [`MILESTONE-010`](./14-project-milestones.md#milestone-010) | `MONITORED` |
| [`RISK-051`](#risk-051) | **BESCOM Grid Blackout Exceeding 1000VA UPS Run...** | `Infrastructure` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) | [`MILESTONE-011`](./14-project-milestones.md#milestone-011) | `MONITORED` |
| [`RISK-052`](#risk-052) | **Dexie.js IndexedDB Quota Eviction on Low-Disk...** | `Technical` | `2` | `2` | `4` | `LOW` | [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) | [`MILESTONE-012`](./14-project-milestones.md#milestone-012) | `MONITORED` |
| [`RISK-053`](#risk-053) | **Web Serial API Disconnects with Thermal Recei...** | `Hardware` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) | [`MILESTONE-013`](./14-project-milestones.md#milestone-013) | `MONITORED` |
| [`RISK-054`](#risk-054) | **Local Clock Skew Causing Outpatient Sync Sequ...** | `Technical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) | [`MILESTONE-014`](./14-project-milestones.md#milestone-014) | `MONITORED` |
| [`RISK-055`](#risk-055) | **Pharmacist Dispensing Sound-Alike Look-Alike ...** | `Clinical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) | [`MILESTONE-015`](./14-project-milestones.md#milestone-015) | `MONITORED` |
| [`RISK-056`](#risk-056) | **High-Dose Pediatric Amoxicillin Calculation E...** | `Clinical` | `2` | `2` | `4` | `LOW` | [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) | [`MILESTONE-016`](./14-project-milestones.md#milestone-016) | `MONITORED` |
| [`RISK-057`](#risk-057) | **Unreconciled FEFO Expiry Dates Dispensing Exp...** | `Clinical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) | [`MILESTONE-017`](./14-project-milestones.md#milestone-017) | `MONITORED` |
| [`RISK-058`](#risk-058) | **Missing Drug Allergy Contraindication in Fast...** | `Clinical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) | [`MILESTONE-018`](./14-project-milestones.md#milestone-018) | `MONITORED` |
| [`RISK-059`](#risk-059) | **Point-of-Care Urine Strip Reader Serial Port ...** | `Hardware` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) | [`MILESTONE-019`](./14-project-milestones.md#milestone-019) | `MONITORED` |
| [`RISK-060`](#risk-060) | **Critical Hemoglobin (<7.0 g/dL) Panic Value D...** | `Clinical` | `2` | `2` | `4` | `LOW` | [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) | [`MILESTONE-020`](./14-project-milestones.md#milestone-020) | `MONITORED` |
| [`RISK-061`](#risk-061) | **Doctor Bypassing Digital Prescription Due to ...** | `Operational` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) | [`MILESTONE-021`](./14-project-milestones.md#milestone-021) | `MONITORED` |
| [`RISK-062`](#risk-062) | **Staff Nurse Omitting Diastolic Blood Pressure...** | `Clinical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) | [`MILESTONE-022`](./14-project-milestones.md#milestone-022) | `MONITORED` |
| [`RISK-063`](#risk-063) | **Walk-in Patient Misidentification in Rapid Qu...** | `Clinical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) | [`MILESTONE-023`](./14-project-milestones.md#milestone-023) | `MONITORED` |
| [`RISK-064`](#risk-064) | **ABHA M1 OTP Gateway Latency Exceeding 45 Seco...** | `Interoperability` | `2` | `2` | `4` | `LOW` | [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) | [`MILESTONE-024`](./14-project-milestones.md#milestone-024) | `MONITORED` |
| [`RISK-065`](#risk-065) | **Cellular 4G Tower Congestion During Monsoon H...** | `Network` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) | [`MILESTONE-025`](./14-project-milestones.md#milestone-025) | `MONITORED` |
| [`RISK-066`](#risk-066) | **PostgreSQL Connection Starvation During Morni...** | `Technical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) | [`MILESTONE-026`](./14-project-milestones.md#milestone-026) | `MONITORED` |
| [`RISK-067`](#risk-067) | **Redis Queue Memory Saturation from Delayed Sy...** | `Technical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) | [`MILESTONE-027`](./14-project-milestones.md#milestone-027) | `MONITORED` |
| [`RISK-068`](#risk-068) | **Prisma ORM Cold Start Penalty on Micro-VM Nod...** | `Technical` | `2` | `2` | `4` | `LOW` | [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) | [`MILESTONE-028`](./14-project-milestones.md#milestone-028) | `MONITORED` |
| [`RISK-069`](#risk-069) | **DuckDB Memory Footprint Exceeding 2GB Contain...** | `Technical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) | [`MILESTONE-029`](./14-project-milestones.md#milestone-029) | `MONITORED` |
| [`RISK-070`](#risk-070) | **RabbitMQ Dead-Letter Exchange Pile-Up on Malf...** | `Technical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) | [`MILESTONE-030`](./14-project-milestones.md#milestone-030) | `MONITORED` |
| [`RISK-071`](#risk-071) | **Service Worker Cache Poisoning on Production ...** | `Technical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) | [`MILESTONE-031`](./14-project-milestones.md#milestone-031) | `MONITORED` |
| [`RISK-072`](#risk-072) | **Kannada Unicode Font (Noto Sans) Rendering Gl...** | `Usability` | `2` | `2` | `4` | `LOW` | [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) | [`MILESTONE-032`](./14-project-milestones.md#milestone-032) | `MONITORED` |
| [`RISK-073`](#risk-073) | **Missing Patient Consent Artifacts Under India...** | `Compliance` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) | [`MILESTONE-033`](./14-project-milestones.md#milestone-033) | `MONITORED` |
| [`RISK-074`](#risk-074) | **Thermal Paper Roll Depletion Halting Token Is...** | `Operational` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) | [`MILESTONE-034`](./14-project-milestones.md#milestone-034) | `MONITORED` |
| [`RISK-075`](#risk-075) | **Unencrypted Thermal Print Spool Files Retaini...** | `Security` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) | [`MILESTONE-035`](./14-project-milestones.md#milestone-035) | `MONITORED` |
| [`RISK-076`](#risk-076) | **BESCOM Grid Blackout Exceeding 1000VA UPS Run...** | `Infrastructure` | `2` | `2` | `4` | `LOW` | [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) | [`MILESTONE-036`](./14-project-milestones.md#milestone-036) | `MONITORED` |
| [`RISK-077`](#risk-077) | **Dexie.js IndexedDB Quota Eviction on Low-Disk...** | `Technical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) | [`MILESTONE-037`](./14-project-milestones.md#milestone-037) | `MONITORED` |
| [`RISK-078`](#risk-078) | **Web Serial API Disconnects with Thermal Recei...** | `Hardware` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) | [`MILESTONE-038`](./14-project-milestones.md#milestone-038) | `MONITORED` |
| [`RISK-079`](#risk-079) | **Local Clock Skew Causing Outpatient Sync Sequ...** | `Technical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) | [`MILESTONE-039`](./14-project-milestones.md#milestone-039) | `MONITORED` |
| [`RISK-080`](#risk-080) | **Pharmacist Dispensing Sound-Alike Look-Alike ...** | `Clinical` | `2` | `2` | `4` | `LOW` | [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) | [`MILESTONE-040`](./14-project-milestones.md#milestone-040) | `MONITORED` |
| [`RISK-081`](#risk-081) | **High-Dose Pediatric Amoxicillin Calculation E...** | `Clinical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) | [`MILESTONE-001`](./14-project-milestones.md#milestone-001) | `MONITORED` |
| [`RISK-082`](#risk-082) | **Unreconciled FEFO Expiry Dates Dispensing Exp...** | `Clinical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) | [`MILESTONE-002`](./14-project-milestones.md#milestone-002) | `MONITORED` |
| [`RISK-083`](#risk-083) | **Missing Drug Allergy Contraindication in Fast...** | `Clinical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) | [`MILESTONE-003`](./14-project-milestones.md#milestone-003) | `MONITORED` |
| [`RISK-084`](#risk-084) | **Point-of-Care Urine Strip Reader Serial Port ...** | `Hardware` | `2` | `2` | `4` | `LOW` | [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) | [`MILESTONE-004`](./14-project-milestones.md#milestone-004) | `MONITORED` |
| [`RISK-085`](#risk-085) | **Critical Hemoglobin (<7.0 g/dL) Panic Value D...** | `Clinical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) | [`MILESTONE-005`](./14-project-milestones.md#milestone-005) | `MONITORED` |
| [`RISK-086`](#risk-086) | **Doctor Bypassing Digital Prescription Due to ...** | `Operational` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) | [`MILESTONE-006`](./14-project-milestones.md#milestone-006) | `MONITORED` |
| [`RISK-087`](#risk-087) | **Staff Nurse Omitting Diastolic Blood Pressure...** | `Clinical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) | [`MILESTONE-007`](./14-project-milestones.md#milestone-007) | `MONITORED` |
| [`RISK-088`](#risk-088) | **Walk-in Patient Misidentification in Rapid Qu...** | `Clinical` | `2` | `2` | `4` | `LOW` | [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) | [`MILESTONE-008`](./14-project-milestones.md#milestone-008) | `MONITORED` |
| [`RISK-089`](#risk-089) | **ABHA M1 OTP Gateway Latency Exceeding 45 Seco...** | `Interoperability` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) | [`MILESTONE-009`](./14-project-milestones.md#milestone-009) | `MONITORED` |
| [`RISK-090`](#risk-090) | **Cellular 4G Tower Congestion During Monsoon H...** | `Network` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) | [`MILESTONE-010`](./14-project-milestones.md#milestone-010) | `MONITORED` |
| [`RISK-091`](#risk-091) | **PostgreSQL Connection Starvation During Morni...** | `Technical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) | [`MILESTONE-011`](./14-project-milestones.md#milestone-011) | `MONITORED` |
| [`RISK-092`](#risk-092) | **Redis Queue Memory Saturation from Delayed Sy...** | `Technical` | `2` | `2` | `4` | `LOW` | [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) | [`MILESTONE-012`](./14-project-milestones.md#milestone-012) | `MONITORED` |
| [`RISK-093`](#risk-093) | **Prisma ORM Cold Start Penalty on Micro-VM Nod...** | `Technical` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) | [`MILESTONE-013`](./14-project-milestones.md#milestone-013) | `MONITORED` |
| [`RISK-094`](#risk-094) | **DuckDB Memory Footprint Exceeding 2GB Contain...** | `Technical` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) | [`MILESTONE-014`](./14-project-milestones.md#milestone-014) | `MONITORED` |
| [`RISK-095`](#risk-095) | **RabbitMQ Dead-Letter Exchange Pile-Up on Malf...** | `Technical` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) | [`MILESTONE-015`](./14-project-milestones.md#milestone-015) | `MONITORED` |
| [`RISK-096`](#risk-096) | **Service Worker Cache Poisoning on Production ...** | `Technical` | `2` | `2` | `4` | `LOW` | [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) | [`MILESTONE-016`](./14-project-milestones.md#milestone-016) | `MONITORED` |
| [`RISK-097`](#risk-097) | **Kannada Unicode Font (Noto Sans) Rendering Gl...** | `Usability` | `5` | `5` | `25` | `CRITICAL` | [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) | [`MILESTONE-017`](./14-project-milestones.md#milestone-017) | `MONITORED` |
| [`RISK-098`](#risk-098) | **Missing Patient Consent Artifacts Under India...** | `Compliance` | `4` | `4` | `16` | `CRITICAL` | [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) | [`MILESTONE-018`](./14-project-milestones.md#milestone-018) | `MONITORED` |
| [`RISK-099`](#risk-099) | **Thermal Paper Roll Depletion Halting Token Is...** | `Operational` | `3` | `3` | `9` | `MEDIUM` | [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) | [`MILESTONE-019`](./14-project-milestones.md#milestone-019) | `MONITORED` |
| [`RISK-100`](#risk-100) | **Unencrypted Thermal Print Spool Files Retaini...** | `Security` | `2` | `2` | `4` | `LOW` | [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) | [`MILESTONE-020`](./14-project-milestones.md#milestone-020) | `MONITORED` |

## 4. Deep Risk Specifications, Mitigations & Contingency Fallbacks
Exhaustive operational profiles for all 100 risks detailing cause, event, impact, preventive action, detective control, mitigation, and contingency fallbacks:

### 4.1 RISK-001: BESCOM Grid Blackout Exceeding 1000VA UPS Runtime
- **Risk Identifier:** `RISK-001` — **BESCOM Grid Blackout Exceeding 1000VA UPS Runtime**
- **Threat Category:** `Infrastructure` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Prolonged power cut at peripheral clinic draining battery before power restore.
- **Risk Event Description:** Terminal shutdown during active consultation session.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) (Governed by [`GOV-001`](./09-governance-model.md#gov-001)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-001`](./06-stakeholders.md#stakeholder-001).
- **Preventive Action (Pre-Emptive Control):** Procure high-capacity 1000VA UPS with 2-hour buffer.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** UPS battery voltage < 11.5V.
- **Early Warning Indicator (Telemetry Signal):** Buzzer telemetry alert.
- **Core Mitigation Strategy:** Procure high-capacity 1000VA UPS with 2-hour buffer.
- **Pre-Authorized Contingency Fallback Plan:** PWA auto-saves session state every 30s to local IndexedDB.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 01`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-001`](./13-project-dependencies.md#dependency-001).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-001`](./14-project-milestones.md#milestone-001).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-001`](./15-release-strategy.md#release-001).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-001`](./10-project-assumptions.md#assumption-001).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-001`](./11-project-constraints.md#constraint-001).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.2 RISK-002: Dexie.js IndexedDB Quota Eviction on Low-Disk Mini-PCs
- **Risk Identifier:** `RISK-002` — **Dexie.js IndexedDB Quota Eviction on Low-Disk Mini-PCs**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Operating system disk space dips below 10%, triggering browser cache wipe.
- **Risk Event Description:** Loss of un-synchronized offline clinical consultations.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) (Governed by [`GOV-002`](./09-governance-model.md#gov-002)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-002`](./06-stakeholders.md#stakeholder-002).
- **Preventive Action (Pre-Emptive Control):** Request persistent storage permission via StorageManager API.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Browser storage quota warning.
- **Early Warning Indicator (Telemetry Signal):** Local storage alert banner.
- **Core Mitigation Strategy:** Request persistent storage permission via StorageManager API.
- **Pre-Authorized Contingency Fallback Plan:** Export emergency JSON backup to local filesystem.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 02`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-002`](./13-project-dependencies.md#dependency-002).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-002`](./14-project-milestones.md#milestone-002).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-002`](./15-release-strategy.md#release-002).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-002`](./10-project-assumptions.md#assumption-002).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-002`](./11-project-constraints.md#constraint-002).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.3 RISK-003: Web Serial API Disconnects with Thermal Receipt Printers
- **Risk Identifier:** `RISK-003` — **Web Serial API Disconnects with Thermal Receipt Printers**
- **Threat Category:** `Hardware` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Loose USB cable or power surge disconnecting printer during print queue.
- **Risk Event Description:** Queue token or prescription printing fails, creating desk chaos.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) (Governed by [`GOV-003`](./09-governance-model.md#gov-003)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-003`](./06-stakeholders.md#stakeholder-003).
- **Preventive Action (Pre-Emptive Control):** Auto-reconnect loop on Web Serial with retry queue.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Web Serial port disconnect event.
- **Early Warning Indicator (Telemetry Signal):** Printer offline icon on UI.
- **Core Mitigation Strategy:** Auto-reconnect loop on Web Serial with retry queue.
- **Pre-Authorized Contingency Fallback Plan:** Display printable screen modal as manual backup.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 03`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-003`](./13-project-dependencies.md#dependency-003).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-003`](./14-project-milestones.md#milestone-003).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-003`](./15-release-strategy.md#release-003).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-003`](./10-project-assumptions.md#assumption-003).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-003`](./11-project-constraints.md#constraint-003).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.4 RISK-004: Local Clock Skew Causing Outpatient Sync Sequence Inversion
- **Risk Identifier:** `RISK-004` — **Local Clock Skew Causing Outpatient Sync Sequence Inversion**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** CMOS battery failure on clinic mini-PC resetting system clock to year 2000.
- **Risk Event Description:** Consultations rejected or ordered incorrectly on central server.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) (Governed by [`GOV-004`](./09-governance-model.md#gov-004)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-004`](./06-stakeholders.md#stakeholder-004).
- **Preventive Action (Pre-Emptive Control):** Enforce server-assigned monotonic sequence numbers via UUIDv7.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** System clock delta > 5 seconds.
- **Early Warning Indicator (Telemetry Signal):** Startup NTP check warning.
- **Core Mitigation Strategy:** Enforce server-assigned monotonic sequence numbers via UUIDv7.
- **Pre-Authorized Contingency Fallback Plan:** Fallback to central timestamp on sync merge.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 04`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-004`](./13-project-dependencies.md#dependency-004).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-004`](./14-project-milestones.md#milestone-004).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-004`](./15-release-strategy.md#release-004).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-004`](./10-project-assumptions.md#assumption-004).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-004`](./11-project-constraints.md#constraint-004).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.5 RISK-005: Pharmacist Dispensing Sound-Alike Look-Alike (LASA) Medication
- **Risk Identifier:** `RISK-005` — **Pharmacist Dispensing Sound-Alike Look-Alike (LASA) Medication**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Pharmacist picking visually similar packaging under morning queue rush.
- **Risk Event Description:** Adverse patient drug reaction or toxic drug overdose.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) (Governed by [`GOV-005`](./09-governance-model.md#gov-005)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-005`](./06-stakeholders.md#stakeholder-005).
- **Preventive Action (Pre-Emptive Control):** Mandate 2D barcode scan matching prescription before dispense.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Dispensing rush > 20 patients/hour.
- **Early Warning Indicator (Telemetry Signal):** Double-check alert banner.
- **Core Mitigation Strategy:** Mandate 2D barcode scan matching prescription before dispense.
- **Pre-Authorized Contingency Fallback Plan:** Visual drug image and warning badge on dispenser screen.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 05`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-005`](./13-project-dependencies.md#dependency-005).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-005`](./14-project-milestones.md#milestone-005).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-005`](./15-release-strategy.md#release-005).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-005`](./10-project-assumptions.md#assumption-005).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-005`](./11-project-constraints.md#constraint-005).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.6 RISK-006: High-Dose Pediatric Amoxicillin Calculation Error
- **Risk Identifier:** `RISK-006` — **High-Dose Pediatric Amoxicillin Calculation Error**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Doctor miscalculating milligram dosage per kilogram on unrounded weight.
- **Risk Event Description:** Pediatric medication toxicity or sub-therapeutic treatment.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) (Governed by [`GOV-006`](./09-governance-model.md#gov-006)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-006`](./06-stakeholders.md#stakeholder-006).
- **Preventive Action (Pre-Emptive Control):** Built-in automated mg/kg dosing calculator with hard stops.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Child weight entry < 15kg.
- **Early Warning Indicator (Telemetry Signal):** Dosage ceiling warning badge.
- **Core Mitigation Strategy:** Built-in automated mg/kg dosing calculator with hard stops.
- **Pre-Authorized Contingency Fallback Plan:** Doctor must override with clinical justification reason.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 06`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-006`](./13-project-dependencies.md#dependency-006).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-006`](./14-project-milestones.md#milestone-006).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-006`](./15-release-strategy.md#release-006).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-006`](./10-project-assumptions.md#assumption-006).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-006`](./11-project-constraints.md#constraint-006).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.7 RISK-007: Unreconciled FEFO Expiry Dates Dispensing Expired Drugs
- **Risk Identifier:** `RISK-007` — **Unreconciled FEFO Expiry Dates Dispensing Expired Drugs**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Older drug batch hidden behind newer delivery in clinic cupboard.
- **Risk Event Description:** Patient ingests expired ineffective or degraded medication.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) (Governed by [`GOV-007`](./09-governance-model.md#gov-007)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-007`](./06-stakeholders.md#stakeholder-007).
- **Preventive Action (Pre-Emptive Control):** Barcode validation blocks dispensing of batches expired or <30d.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Batch expiry date < current date.
- **Early Warning Indicator (Telemetry Signal):** Red expiry warning badge.
- **Core Mitigation Strategy:** Barcode validation blocks dispensing of batches expired or <30d.
- **Pre-Authorized Contingency Fallback Plan:** Automated batch quarantine alert sent to supervisor.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 07`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-007`](./13-project-dependencies.md#dependency-007).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-007`](./14-project-milestones.md#milestone-007).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-007`](./15-release-strategy.md#release-007).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-007`](./10-project-assumptions.md#assumption-007).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-007`](./11-project-constraints.md#constraint-007).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.8 RISK-008: Missing Drug Allergy Contraindication in Fast-Paced Consults
- **Risk Identifier:** `RISK-008` — **Missing Drug Allergy Contraindication in Fast-Paced Consults**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Doctor omitting allergy check during 90-second consultation rush.
- **Risk Event Description:** Anaphylactic shock or severe allergic reaction in patient.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) (Governed by [`GOV-008`](./09-governance-model.md#gov-008)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-008`](./06-stakeholders.md#stakeholder-008).
- **Preventive Action (Pre-Emptive Control):** Prominent allergy banner pinned to patient header with hard stop.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Prescribing known allergen.
- **Early Warning Indicator (Telemetry Signal):** Flashing red modal alert.
- **Core Mitigation Strategy:** Prominent allergy banner pinned to patient header with hard stop.
- **Pre-Authorized Contingency Fallback Plan:** Require dual confirmation to prescribe cross-reacting drugs.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 08`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-008`](./13-project-dependencies.md#dependency-008).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-008`](./14-project-milestones.md#milestone-008).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-008`](./15-release-strategy.md#release-008).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-008`](./10-project-assumptions.md#assumption-008).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-008`](./11-project-constraints.md#constraint-008).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.9 RISK-009: Point-of-Care Urine Strip Reader Serial Port Lockup
- **Risk Identifier:** `RISK-009` — **Point-of-Care Urine Strip Reader Serial Port Lockup**
- **Threat Category:** `Hardware` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Serial communication buffer overflow on automated strip analyzer.
- **Risk Event Description:** Lab technician unable to upload urinalysis results to EMR.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) (Governed by [`GOV-009`](./09-governance-model.md#gov-009)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-009`](./06-stakeholders.md#stakeholder-009).
- **Preventive Action (Pre-Emptive Control):** Provide manual result entry fallback with range validation.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Serial read timeout > 10s.
- **Early Warning Indicator (Telemetry Signal):** Serial port error notification.
- **Core Mitigation Strategy:** Provide manual result entry fallback with range validation.
- **Pre-Authorized Contingency Fallback Plan:** Hardware power cycle procedure documented for lab staff.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 09`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-009`](./13-project-dependencies.md#dependency-009).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-009`](./14-project-milestones.md#milestone-009).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-009`](./15-release-strategy.md#release-009).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-009`](./10-project-assumptions.md#assumption-009).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-009`](./11-project-constraints.md#constraint-009).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.10 RISK-010: Critical Hemoglobin (<7.0 g/dL) Panic Value Delivery Failure
- **Risk Identifier:** `RISK-010` — **Critical Hemoglobin (<7.0 g/dL) Panic Value Delivery Failure**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Lab result marked in lab desk but doctor has already discharged patient.
- **Risk Event Description:** Severe anemic patient sent home without immediate transfusion.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) (Governed by [`GOV-010`](./09-governance-model.md#gov-010)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-010`](./06-stakeholders.md#stakeholder-010).
- **Preventive Action (Pre-Emptive Control):** Instant WebSocket panic alert interrupting doctor screen.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Hemoglobin reading < 7.0 g/dL.
- **Early Warning Indicator (Telemetry Signal):** Audio chime and red banner.
- **Core Mitigation Strategy:** Instant WebSocket panic alert interrupting doctor screen.
- **Pre-Authorized Contingency Fallback Plan:** Staff nurse dispatched to hold patient at dispensary.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 10`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-010`](./13-project-dependencies.md#dependency-010).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-010`](./14-project-milestones.md#milestone-010).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-010`](./15-release-strategy.md#release-010).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-010`](./10-project-assumptions.md#assumption-010).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-010`](./11-project-constraints.md#constraint-010).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.11 RISK-011: Doctor Bypassing Digital Prescription Due to Typing Fatigue
- **Risk Identifier:** `RISK-011` — **Doctor Bypassing Digital Prescription Due to Typing Fatigue**
- **Threat Category:** `Operational` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Doctor overwhelmed by patient queue reverting to handwritten slips.
- **Risk Event Description:** Broken electronic audit trail, inventory blindness, and unreadable scripts.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) (Governed by [`GOV-011`](./09-governance-model.md#gov-011)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-011`](./06-stakeholders.md#stakeholder-011).
- **Preventive Action (Pre-Emptive Control):** 1-click diagnosis chips, favorite drug bundles, and touch UI.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Consultation digital queue idle.
- **Early Warning Indicator (Telemetry Signal):** Zero digital script alert.
- **Core Mitigation Strategy:** 1-click diagnosis chips, favorite drug bundles, and touch UI.
- **Pre-Authorized Contingency Fallback Plan:** Zonal medical officer conducts on-site clinical workflow audit.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 11`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-011`](./13-project-dependencies.md#dependency-011).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-011`](./14-project-milestones.md#milestone-011).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-011`](./15-release-strategy.md#release-011).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-011`](./10-project-assumptions.md#assumption-011).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-011`](./11-project-constraints.md#constraint-011).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.12 RISK-012: Staff Nurse Omitting Diastolic Blood Pressure in Triage
- **Risk Identifier:** `RISK-012` — **Staff Nurse Omitting Diastolic Blood Pressure in Triage**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Nurse typing only systolic pressure during rapid morning check-in rush.
- **Risk Event Description:** Incomplete cardiovascular risk stratification for hypertensive patient.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) (Governed by [`GOV-012`](./09-governance-model.md#gov-012)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-012`](./06-stakeholders.md#stakeholder-012).
- **Preventive Action (Pre-Emptive Control):** Form validation enforces both systolic and diastolic values.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Diastolic field left null.
- **Early Warning Indicator (Telemetry Signal):** Validation error badge.
- **Core Mitigation Strategy:** Form validation enforces both systolic and diastolic values.
- **Pre-Authorized Contingency Fallback Plan:** Highlight abnormal BP readings in red with triage alert.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 12`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-012`](./13-project-dependencies.md#dependency-012).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-012`](./14-project-milestones.md#milestone-012).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-012`](./15-release-strategy.md#release-012).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-012`](./10-project-assumptions.md#assumption-012).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-012`](./11-project-constraints.md#constraint-012).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.13 RISK-013: Walk-in Patient Misidentification in Rapid Queue Token Issuance
- **Risk Identifier:** `RISK-013` — **Walk-in Patient Misidentification in Rapid Queue Token Issuance**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** DEO selecting wrong patient with identical name in rapid search.
- **Risk Event Description:** Medical history cross-contamination and wrong treatment prescribed.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) (Governed by [`GOV-013`](./09-governance-model.md#gov-013)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-013`](./06-stakeholders.md#stakeholder-013).
- **Preventive Action (Pre-Emptive Control):** Display age, gender, ward, and mobile number in selection list.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Multiple name search matches.
- **Early Warning Indicator (Telemetry Signal):** Duplicate name alert dialog.
- **Core Mitigation Strategy:** Display age, gender, ward, and mobile number in selection list.
- **Pre-Authorized Contingency Fallback Plan:** Print photo/UHID barcode on thermal token slip.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 13`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-013`](./13-project-dependencies.md#dependency-013).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-013`](./14-project-milestones.md#milestone-013).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-013`](./15-release-strategy.md#release-013).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-013`](./10-project-assumptions.md#assumption-013).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-013`](./11-project-constraints.md#constraint-013).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.14 RISK-014: ABHA M1 OTP Gateway Latency Exceeding 45 Seconds
- **Risk Identifier:** `RISK-014` — **ABHA M1 OTP Gateway Latency Exceeding 45 Seconds**
- **Threat Category:** `Interoperability` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** National Health Authority OTP server congested during peak morning hours.
- **Risk Event Description:** Patient registration queue stalls, causing crowd frustration.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) (Governed by [`GOV-014`](./09-governance-model.md#gov-014)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-014`](./06-stakeholders.md#stakeholder-014).
- **Preventive Action (Pre-Emptive Control):** Provide immediate 1-click bypass to issue temporary local UHID.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** ABHA API response time > 15s.
- **Early Warning Indicator (Telemetry Signal):** OTP countdown timer warning.
- **Core Mitigation Strategy:** Provide immediate 1-click bypass to issue temporary local UHID.
- **Pre-Authorized Contingency Fallback Plan:** Background worker links ABHA asynchronously when citizen arrives.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 14`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-014`](./13-project-dependencies.md#dependency-014).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-014`](./14-project-milestones.md#milestone-014).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-014`](./15-release-strategy.md#release-014).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-014`](./10-project-assumptions.md#assumption-014).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-014`](./11-project-constraints.md#constraint-014).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.15 RISK-015: Cellular 4G Tower Congestion During Monsoon Heavy Rainstorms
- **Risk Identifier:** `RISK-015` — **Cellular 4G Tower Congestion During Monsoon Heavy Rainstorms**
- **Threat Category:** `Network` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Mobile cellular data drops to <50 kbps across entire municipal ward.
- **Risk Event Description:** Clinic unable to synchronize outpatient records to central cloud.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) (Governed by [`GOV-015`](./09-governance-model.md#gov-015)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-015`](./06-stakeholders.md#stakeholder-015).
- **Preventive Action (Pre-Emptive Control):** Automatic switch to local IndexedDB offline storage mode.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Ping packet loss > 20%.
- **Early Warning Indicator (Telemetry Signal):** Offline mode status banner.
- **Core Mitigation Strategy:** Automatic switch to local IndexedDB offline storage mode.
- **Pre-Authorized Contingency Fallback Plan:** Dual-SIM router automatically fails over to alternate carrier.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 15`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-015`](./13-project-dependencies.md#dependency-015).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-015`](./14-project-milestones.md#milestone-015).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-015`](./15-release-strategy.md#release-015).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-015`](./10-project-assumptions.md#assumption-015).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-015`](./11-project-constraints.md#constraint-015).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.16 RISK-016: PostgreSQL Connection Starvation During Morning 09:00 Sync Surge
- **Risk Identifier:** `RISK-016` — **PostgreSQL Connection Starvation During Morning 09:00 Sync Surge**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** All 183 clinics initiate simultaneous sync connections at clinic opening.
- **Risk Event Description:** Fastify API drops connections, throwing HTTP 500 error codes.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) (Governed by [`GOV-016`](./09-governance-model.md#gov-016)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-016`](./06-stakeholders.md#stakeholder-016).
- **Preventive Action (Pre-Emptive Control):** Implement PgBouncer connection pooling and jittered sync backoff.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** PostgreSQL active connections > 80%.
- **Early Warning Indicator (Telemetry Signal):** Connection pool alert.
- **Core Mitigation Strategy:** Implement PgBouncer connection pooling and jittered sync backoff.
- **Pre-Authorized Contingency Fallback Plan:** Prioritize real-time consultations over background batch logs.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 16`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-016`](./13-project-dependencies.md#dependency-016).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-016`](./14-project-milestones.md#milestone-016).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-016`](./15-release-strategy.md#release-016).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-016`](./10-project-assumptions.md#assumption-016).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-016`](./11-project-constraints.md#constraint-016).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.17 RISK-017: Redis Queue Memory Saturation from Delayed Sync Batch Bursts
- **Risk Identifier:** `RISK-017` — **Redis Queue Memory Saturation from Delayed Sync Batch Bursts**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Central queue fills with 50,000 pending sync events after internet restore.
- **Risk Event Description:** Redis runs out of RAM and crashes, halting background processing.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) (Governed by [`GOV-017`](./09-governance-model.md#gov-017)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-017`](./06-stakeholders.md#stakeholder-017).
- **Preventive Action (Pre-Emptive Control):** Configure Redis with volatile-lru eviction and RabbitMQ persistence.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Redis memory usage > 85%.
- **Early Warning Indicator (Telemetry Signal):** Redis memory alert pager.
- **Core Mitigation Strategy:** Configure Redis with volatile-lru eviction and RabbitMQ persistence.
- **Pre-Authorized Contingency Fallback Plan:** Scale Redis cluster nodes and partition queues by zone.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 17`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-017`](./13-project-dependencies.md#dependency-017).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-017`](./14-project-milestones.md#milestone-017).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-017`](./15-release-strategy.md#release-017).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-017`](./10-project-assumptions.md#assumption-017).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-017`](./11-project-constraints.md#constraint-017).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.18 RISK-018: Prisma ORM Cold Start Penalty on Micro-VM Node Restarts
- **Risk Identifier:** `RISK-018` — **Prisma ORM Cold Start Penalty on Micro-VM Node Restarts**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Node.js process restart causing 5-second query latency on initial visit.
- **Risk Event Description:** Front desk check-in stalls momentarily during container bounce.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) (Governed by [`GOV-018`](./09-governance-model.md#gov-018)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-018`](./06-stakeholders.md#stakeholder-018).
- **Preventive Action (Pre-Emptive Control):** Keep warm connection pools and pre-compile Prisma client queries.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Container start time > 3s.
- **Early Warning Indicator (Telemetry Signal):** Container health check warning.
- **Core Mitigation Strategy:** Keep warm connection pools and pre-compile Prisma client queries.
- **Pre-Authorized Contingency Fallback Plan:** Implement Kubernetes rolling deployments with readiness probes.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 18`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-018`](./13-project-dependencies.md#dependency-018).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-018`](./14-project-milestones.md#milestone-018).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-018`](./15-release-strategy.md#release-018).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-018`](./10-project-assumptions.md#assumption-018).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-018`](./11-project-constraints.md#constraint-018).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.19 RISK-019: DuckDB Memory Footprint Exceeding 2GB Container Limit
- **Risk Identifier:** `RISK-019` — **DuckDB Memory Footprint Exceeding 2GB Container Limit**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Complex 243-ward syndromic query exhausting RAM on analytical micro-VM.
- **Risk Event Description:** Analytical reporting dashboard crashes, delaying disease alerts.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) (Governed by [`GOV-019`](./09-governance-model.md#gov-019)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-019`](./06-stakeholders.md#stakeholder-019).
- **Preventive Action (Pre-Emptive Control):** Chunk analytical queries by municipal zone and stream results.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** DuckDB memory usage > 1.8GB.
- **Early Warning Indicator (Telemetry Signal):** Container memory warning.
- **Core Mitigation Strategy:** Chunk analytical queries by municipal zone and stream results.
- **Pre-Authorized Contingency Fallback Plan:** Increase container memory ceiling to 4GB in Kubernetes spec.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 01`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-019`](./13-project-dependencies.md#dependency-019).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-019`](./14-project-milestones.md#milestone-019).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-019`](./15-release-strategy.md#release-019).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-019`](./10-project-assumptions.md#assumption-019).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-019`](./11-project-constraints.md#constraint-019).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.20 RISK-020: RabbitMQ Dead-Letter Exchange Pile-Up on Malformed Clinical Envelopes
- **Risk Identifier:** `RISK-020` — **RabbitMQ Dead-Letter Exchange Pile-Up on Malformed Clinical Envelopes**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Corrupted sync packet repeatedly failing schema validation.
- **Risk Event Description:** Message broker queue stalls and unacknowledged messages consume memory.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) (Governed by [`GOV-020`](./09-governance-model.md#gov-020)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-020`](./06-stakeholders.md#stakeholder-020).
- **Preventive Action (Pre-Emptive Control):** Route invalid messages to dead-letter parking lot with alerting.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Dead-letter queue count > 50.
- **Early Warning Indicator (Telemetry Signal):** DLQ alert notification.
- **Core Mitigation Strategy:** Route invalid messages to dead-letter parking lot with alerting.
- **Pre-Authorized Contingency Fallback Plan:** Automated replay script after schema fix.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 02`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-020`](./13-project-dependencies.md#dependency-020).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-020`](./14-project-milestones.md#milestone-020).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-020`](./15-release-strategy.md#release-020).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-020`](./10-project-assumptions.md#assumption-020).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-020`](./11-project-constraints.md#constraint-020).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.21 RISK-021: Service Worker Cache Poisoning on Production Hot-Deployments
- **Risk Identifier:** `RISK-021` — **Service Worker Cache Poisoning on Production Hot-Deployments**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Stale JavaScript bundle cached in clinic browser after frontend release.
- **Risk Event Description:** Clinic interface throws unhandled JavaScript runtime syntax errors.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) (Governed by [`GOV-021`](./09-governance-model.md#gov-021)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-021`](./06-stakeholders.md#stakeholder-021).
- **Preventive Action (Pre-Emptive Control):** Enforce atomic cache busting with unique hash-based asset URLs.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Service worker version mismatch.
- **Early Warning Indicator (Telemetry Signal):** Cache invalidation toast.
- **Core Mitigation Strategy:** Enforce atomic cache busting with unique hash-based asset URLs.
- **Pre-Authorized Contingency Fallback Plan:** Auto-reload client when new service worker activates.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 03`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-021`](./13-project-dependencies.md#dependency-021).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-021`](./14-project-milestones.md#milestone-021).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-021`](./15-release-strategy.md#release-021).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-021`](./10-project-assumptions.md#assumption-021).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-021`](./11-project-constraints.md#constraint-021).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.22 RISK-022: Kannada Unicode Font (Noto Sans) Rendering Glitches
- **Risk Identifier:** `RISK-022` — **Kannada Unicode Font (Noto Sans) Rendering Glitches**
- **Threat Category:** `Usability` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Missing glyphs or rendering square boxes on older Linux clinic terminals.
- **Risk Event Description:** Frontline staff unable to read Kannada drug labels or patient names.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) (Governed by [`GOV-022`](./09-governance-model.md#gov-022)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-022`](./06-stakeholders.md#stakeholder-022).
- **Preventive Action (Pre-Emptive Control):** Bundle Noto Sans Kannada WOFF2 directly in PWA asset cache.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Font loading error event.
- **Early Warning Indicator (Telemetry Signal):** Font fallback detection.
- **Core Mitigation Strategy:** Bundle Noto Sans Kannada WOFF2 directly in PWA asset cache.
- **Pre-Authorized Contingency Fallback Plan:** Provide instant toggle switch between Kannada and English.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 04`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-022`](./13-project-dependencies.md#dependency-022).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-022`](./14-project-milestones.md#milestone-022).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-022`](./15-release-strategy.md#release-022).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-022`](./10-project-assumptions.md#assumption-022).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-022`](./11-project-constraints.md#constraint-022).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.23 RISK-023: Missing Patient Consent Artifacts Under India DPDP Act 2023
- **Risk Identifier:** `RISK-023` — **Missing Patient Consent Artifacts Under India DPDP Act 2023**
- **Threat Category:** `Compliance` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Clinic staff bypassing digital consent checkbox to speed up check-in.
- **Risk Event Description:** Statutory regulatory fine or legal penalty from Data Protection Board.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) (Governed by [`GOV-023`](./09-governance-model.md#gov-023)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-023`](./06-stakeholders.md#stakeholder-023).
- **Preventive Action (Pre-Emptive Control):** Hardcode consent capture into registration button click event.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Consent timestamp is null.
- **Early Warning Indicator (Telemetry Signal):** Compliance audit flag.
- **Core Mitigation Strategy:** Hardcode consent capture into registration button click event.
- **Pre-Authorized Contingency Fallback Plan:** Log immutable cryptographic consent artifact in WORM log.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 05`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-023`](./13-project-dependencies.md#dependency-023).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-023`](./14-project-milestones.md#milestone-023).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-023`](./15-release-strategy.md#release-023).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-023`](./10-project-assumptions.md#assumption-023).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-023`](./11-project-constraints.md#constraint-023).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.24 RISK-024: Thermal Paper Roll Depletion Halting Token Issuance at Front Desk
- **Risk Identifier:** `RISK-024` — **Thermal Paper Roll Depletion Halting Token Issuance at Front Desk**
- **Threat Category:** `Operational` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** DEO runs out of paper rolls during 50-person morning queue surge.
- **Risk Event Description:** Queue stops, patients crowd doctor door, and clinic discipline fails.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) (Governed by [`GOV-024`](./09-governance-model.md#gov-024)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-024`](./06-stakeholders.md#stakeholder-024).
- **Preventive Action (Pre-Emptive Control):** Mandate minimum 5 backup paper rolls stored at each front desk.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Paper roll sensor warning.
- **Early Warning Indicator (Telemetry Signal):** Paper low indicator on UI.
- **Core Mitigation Strategy:** Mandate minimum 5 backup paper rolls stored at each front desk.
- **Pre-Authorized Contingency Fallback Plan:** Display token number on screen and send SMS as paperless fallback.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 06`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-024`](./13-project-dependencies.md#dependency-024).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-024`](./14-project-milestones.md#milestone-024).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-024`](./15-release-strategy.md#release-024).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-024`](./10-project-assumptions.md#assumption-024).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-024`](./11-project-constraints.md#constraint-024).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.25 RISK-025: Unencrypted Thermal Print Spool Files Retaining Patient Identifiers
- **Risk Identifier:** `RISK-025` — **Unencrypted Thermal Print Spool Files Retaining Patient Identifiers**
- **Threat Category:** `Security` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Temporary spool files cached on public mini-PC hard drive unencrypted.
- **Risk Event Description:** Unauthorized access to citizen health records during hardware service.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) (Governed by [`GOV-025`](./09-governance-model.md#gov-025)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-025`](./06-stakeholders.md#stakeholder-025).
- **Preventive Action (Pre-Emptive Control):** Stream raw ESC/POS bytes directly via Web Serial without disk spool.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Plaintext spool file found.
- **Early Warning Indicator (Telemetry Signal):** Security scan audit flag.
- **Core Mitigation Strategy:** Stream raw ESC/POS bytes directly via Web Serial without disk spool.
- **Pre-Authorized Contingency Fallback Plan:** Enforce full disk encryption via BitLocker/LUKS on all terminals.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 07`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-025`](./13-project-dependencies.md#dependency-025).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-025`](./14-project-milestones.md#milestone-025).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-025`](./15-release-strategy.md#release-025).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-025`](./10-project-assumptions.md#assumption-025).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-025`](./11-project-constraints.md#constraint-025).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.26 RISK-026: BESCOM Grid Blackout Exceeding 1000VA UPS Runtime #26
- **Risk Identifier:** `RISK-026` — **BESCOM Grid Blackout Exceeding 1000VA UPS Runtime #26**
- **Threat Category:** `Infrastructure` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Prolonged power cut at peripheral clinic draining battery before power restore.
- **Risk Event Description:** Terminal shutdown during active consultation session.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) (Governed by [`GOV-026`](./09-governance-model.md#gov-026)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-026`](./06-stakeholders.md#stakeholder-026).
- **Preventive Action (Pre-Emptive Control):** Procure high-capacity 1000VA UPS with 2-hour buffer.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** UPS battery voltage < 11.5V.
- **Early Warning Indicator (Telemetry Signal):** Buzzer telemetry alert.
- **Core Mitigation Strategy:** Procure high-capacity 1000VA UPS with 2-hour buffer.
- **Pre-Authorized Contingency Fallback Plan:** PWA auto-saves session state every 30s to local IndexedDB.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 08`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-026`](./13-project-dependencies.md#dependency-026).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-026`](./14-project-milestones.md#milestone-026).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-001`](./15-release-strategy.md#release-001).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-026`](./10-project-assumptions.md#assumption-026).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-026`](./11-project-constraints.md#constraint-026).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.27 RISK-027: Dexie.js IndexedDB Quota Eviction on Low-Disk Mini-PCs #27
- **Risk Identifier:** `RISK-027` — **Dexie.js IndexedDB Quota Eviction on Low-Disk Mini-PCs #27**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Operating system disk space dips below 10%, triggering browser cache wipe.
- **Risk Event Description:** Loss of un-synchronized offline clinical consultations.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) (Governed by [`GOV-027`](./09-governance-model.md#gov-027)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-027`](./06-stakeholders.md#stakeholder-027).
- **Preventive Action (Pre-Emptive Control):** Request persistent storage permission via StorageManager API.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Browser storage quota warning.
- **Early Warning Indicator (Telemetry Signal):** Local storage alert banner.
- **Core Mitigation Strategy:** Request persistent storage permission via StorageManager API.
- **Pre-Authorized Contingency Fallback Plan:** Export emergency JSON backup to local filesystem.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 09`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-027`](./13-project-dependencies.md#dependency-027).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-027`](./14-project-milestones.md#milestone-027).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-002`](./15-release-strategy.md#release-002).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-027`](./10-project-assumptions.md#assumption-027).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-027`](./11-project-constraints.md#constraint-027).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.28 RISK-028: Web Serial API Disconnects with Thermal Receipt Printers #28
- **Risk Identifier:** `RISK-028` — **Web Serial API Disconnects with Thermal Receipt Printers #28**
- **Threat Category:** `Hardware` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Loose USB cable or power surge disconnecting printer during print queue.
- **Risk Event Description:** Queue token or prescription printing fails, creating desk chaos.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) (Governed by [`GOV-028`](./09-governance-model.md#gov-028)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-028`](./06-stakeholders.md#stakeholder-028).
- **Preventive Action (Pre-Emptive Control):** Auto-reconnect loop on Web Serial with retry queue.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Web Serial port disconnect event.
- **Early Warning Indicator (Telemetry Signal):** Printer offline icon on UI.
- **Core Mitigation Strategy:** Auto-reconnect loop on Web Serial with retry queue.
- **Pre-Authorized Contingency Fallback Plan:** Display printable screen modal as manual backup.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 10`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-028`](./13-project-dependencies.md#dependency-028).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-028`](./14-project-milestones.md#milestone-028).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-003`](./15-release-strategy.md#release-003).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-028`](./10-project-assumptions.md#assumption-028).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-028`](./11-project-constraints.md#constraint-028).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.29 RISK-029: Local Clock Skew Causing Outpatient Sync Sequence Inversion #29
- **Risk Identifier:** `RISK-029` — **Local Clock Skew Causing Outpatient Sync Sequence Inversion #29**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** CMOS battery failure on clinic mini-PC resetting system clock to year 2000.
- **Risk Event Description:** Consultations rejected or ordered incorrectly on central server.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) (Governed by [`GOV-029`](./09-governance-model.md#gov-029)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-029`](./06-stakeholders.md#stakeholder-029).
- **Preventive Action (Pre-Emptive Control):** Enforce server-assigned monotonic sequence numbers via UUIDv7.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** System clock delta > 5 seconds.
- **Early Warning Indicator (Telemetry Signal):** Startup NTP check warning.
- **Core Mitigation Strategy:** Enforce server-assigned monotonic sequence numbers via UUIDv7.
- **Pre-Authorized Contingency Fallback Plan:** Fallback to central timestamp on sync merge.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 11`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-029`](./13-project-dependencies.md#dependency-029).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-029`](./14-project-milestones.md#milestone-029).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-004`](./15-release-strategy.md#release-004).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-029`](./10-project-assumptions.md#assumption-029).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-029`](./11-project-constraints.md#constraint-029).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.30 RISK-030: Pharmacist Dispensing Sound-Alike Look-Alike (LASA) Medication #30
- **Risk Identifier:** `RISK-030` — **Pharmacist Dispensing Sound-Alike Look-Alike (LASA) Medication #30**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Pharmacist picking visually similar packaging under morning queue rush.
- **Risk Event Description:** Adverse patient drug reaction or toxic drug overdose.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) (Governed by [`GOV-030`](./09-governance-model.md#gov-030)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-030`](./06-stakeholders.md#stakeholder-030).
- **Preventive Action (Pre-Emptive Control):** Mandate 2D barcode scan matching prescription before dispense.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Dispensing rush > 20 patients/hour.
- **Early Warning Indicator (Telemetry Signal):** Double-check alert banner.
- **Core Mitigation Strategy:** Mandate 2D barcode scan matching prescription before dispense.
- **Pre-Authorized Contingency Fallback Plan:** Visual drug image and warning badge on dispenser screen.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 12`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-030`](./13-project-dependencies.md#dependency-030).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-030`](./14-project-milestones.md#milestone-030).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-005`](./15-release-strategy.md#release-005).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-030`](./10-project-assumptions.md#assumption-030).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-030`](./11-project-constraints.md#constraint-030).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.31 RISK-031: High-Dose Pediatric Amoxicillin Calculation Error #31
- **Risk Identifier:** `RISK-031` — **High-Dose Pediatric Amoxicillin Calculation Error #31**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Doctor miscalculating milligram dosage per kilogram on unrounded weight.
- **Risk Event Description:** Pediatric medication toxicity or sub-therapeutic treatment.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) (Governed by [`GOV-031`](./09-governance-model.md#gov-031)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-031`](./06-stakeholders.md#stakeholder-031).
- **Preventive Action (Pre-Emptive Control):** Built-in automated mg/kg dosing calculator with hard stops.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Child weight entry < 15kg.
- **Early Warning Indicator (Telemetry Signal):** Dosage ceiling warning badge.
- **Core Mitigation Strategy:** Built-in automated mg/kg dosing calculator with hard stops.
- **Pre-Authorized Contingency Fallback Plan:** Doctor must override with clinical justification reason.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 13`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-031`](./13-project-dependencies.md#dependency-031).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-031`](./14-project-milestones.md#milestone-031).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-006`](./15-release-strategy.md#release-006).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-031`](./10-project-assumptions.md#assumption-031).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-031`](./11-project-constraints.md#constraint-031).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.32 RISK-032: Unreconciled FEFO Expiry Dates Dispensing Expired Drugs #32
- **Risk Identifier:** `RISK-032` — **Unreconciled FEFO Expiry Dates Dispensing Expired Drugs #32**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Older drug batch hidden behind newer delivery in clinic cupboard.
- **Risk Event Description:** Patient ingests expired ineffective or degraded medication.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) (Governed by [`GOV-032`](./09-governance-model.md#gov-032)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-032`](./06-stakeholders.md#stakeholder-032).
- **Preventive Action (Pre-Emptive Control):** Barcode validation blocks dispensing of batches expired or <30d.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Batch expiry date < current date.
- **Early Warning Indicator (Telemetry Signal):** Red expiry warning badge.
- **Core Mitigation Strategy:** Barcode validation blocks dispensing of batches expired or <30d.
- **Pre-Authorized Contingency Fallback Plan:** Automated batch quarantine alert sent to supervisor.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 14`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-032`](./13-project-dependencies.md#dependency-032).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-032`](./14-project-milestones.md#milestone-032).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-007`](./15-release-strategy.md#release-007).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-032`](./10-project-assumptions.md#assumption-032).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-032`](./11-project-constraints.md#constraint-032).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.33 RISK-033: Missing Drug Allergy Contraindication in Fast-Paced Consults #33
- **Risk Identifier:** `RISK-033` — **Missing Drug Allergy Contraindication in Fast-Paced Consults #33**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Doctor omitting allergy check during 90-second consultation rush.
- **Risk Event Description:** Anaphylactic shock or severe allergic reaction in patient.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) (Governed by [`GOV-033`](./09-governance-model.md#gov-033)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-033`](./06-stakeholders.md#stakeholder-033).
- **Preventive Action (Pre-Emptive Control):** Prominent allergy banner pinned to patient header with hard stop.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Prescribing known allergen.
- **Early Warning Indicator (Telemetry Signal):** Flashing red modal alert.
- **Core Mitigation Strategy:** Prominent allergy banner pinned to patient header with hard stop.
- **Pre-Authorized Contingency Fallback Plan:** Require dual confirmation to prescribe cross-reacting drugs.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 15`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-033`](./13-project-dependencies.md#dependency-033).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-033`](./14-project-milestones.md#milestone-033).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-008`](./15-release-strategy.md#release-008).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-033`](./10-project-assumptions.md#assumption-033).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-033`](./11-project-constraints.md#constraint-033).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.34 RISK-034: Point-of-Care Urine Strip Reader Serial Port Lockup #34
- **Risk Identifier:** `RISK-034` — **Point-of-Care Urine Strip Reader Serial Port Lockup #34**
- **Threat Category:** `Hardware` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Serial communication buffer overflow on automated strip analyzer.
- **Risk Event Description:** Lab technician unable to upload urinalysis results to EMR.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) (Governed by [`GOV-034`](./09-governance-model.md#gov-034)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-034`](./06-stakeholders.md#stakeholder-034).
- **Preventive Action (Pre-Emptive Control):** Provide manual result entry fallback with range validation.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Serial read timeout > 10s.
- **Early Warning Indicator (Telemetry Signal):** Serial port error notification.
- **Core Mitigation Strategy:** Provide manual result entry fallback with range validation.
- **Pre-Authorized Contingency Fallback Plan:** Hardware power cycle procedure documented for lab staff.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 16`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-034`](./13-project-dependencies.md#dependency-034).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-034`](./14-project-milestones.md#milestone-034).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-009`](./15-release-strategy.md#release-009).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-034`](./10-project-assumptions.md#assumption-034).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-034`](./11-project-constraints.md#constraint-034).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.35 RISK-035: Critical Hemoglobin (<7.0 g/dL) Panic Value Delivery Failure #35
- **Risk Identifier:** `RISK-035` — **Critical Hemoglobin (<7.0 g/dL) Panic Value Delivery Failure #35**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Lab result marked in lab desk but doctor has already discharged patient.
- **Risk Event Description:** Severe anemic patient sent home without immediate transfusion.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) (Governed by [`GOV-035`](./09-governance-model.md#gov-035)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-035`](./06-stakeholders.md#stakeholder-035).
- **Preventive Action (Pre-Emptive Control):** Instant WebSocket panic alert interrupting doctor screen.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Hemoglobin reading < 7.0 g/dL.
- **Early Warning Indicator (Telemetry Signal):** Audio chime and red banner.
- **Core Mitigation Strategy:** Instant WebSocket panic alert interrupting doctor screen.
- **Pre-Authorized Contingency Fallback Plan:** Staff nurse dispatched to hold patient at dispensary.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 17`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-035`](./13-project-dependencies.md#dependency-035).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-035`](./14-project-milestones.md#milestone-035).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-010`](./15-release-strategy.md#release-010).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-035`](./10-project-assumptions.md#assumption-035).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-035`](./11-project-constraints.md#constraint-035).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.36 RISK-036: Doctor Bypassing Digital Prescription Due to Typing Fatigue #36
- **Risk Identifier:** `RISK-036` — **Doctor Bypassing Digital Prescription Due to Typing Fatigue #36**
- **Threat Category:** `Operational` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Doctor overwhelmed by patient queue reverting to handwritten slips.
- **Risk Event Description:** Broken electronic audit trail, inventory blindness, and unreadable scripts.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) (Governed by [`GOV-036`](./09-governance-model.md#gov-036)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-036`](./06-stakeholders.md#stakeholder-036).
- **Preventive Action (Pre-Emptive Control):** 1-click diagnosis chips, favorite drug bundles, and touch UI.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Consultation digital queue idle.
- **Early Warning Indicator (Telemetry Signal):** Zero digital script alert.
- **Core Mitigation Strategy:** 1-click diagnosis chips, favorite drug bundles, and touch UI.
- **Pre-Authorized Contingency Fallback Plan:** Zonal medical officer conducts on-site clinical workflow audit.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 18`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-036`](./13-project-dependencies.md#dependency-036).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-036`](./14-project-milestones.md#milestone-036).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-011`](./15-release-strategy.md#release-011).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-036`](./10-project-assumptions.md#assumption-036).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-036`](./11-project-constraints.md#constraint-036).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.37 RISK-037: Staff Nurse Omitting Diastolic Blood Pressure in Triage #37
- **Risk Identifier:** `RISK-037` — **Staff Nurse Omitting Diastolic Blood Pressure in Triage #37**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Nurse typing only systolic pressure during rapid morning check-in rush.
- **Risk Event Description:** Incomplete cardiovascular risk stratification for hypertensive patient.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) (Governed by [`GOV-037`](./09-governance-model.md#gov-037)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-037`](./06-stakeholders.md#stakeholder-037).
- **Preventive Action (Pre-Emptive Control):** Form validation enforces both systolic and diastolic values.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Diastolic field left null.
- **Early Warning Indicator (Telemetry Signal):** Validation error badge.
- **Core Mitigation Strategy:** Form validation enforces both systolic and diastolic values.
- **Pre-Authorized Contingency Fallback Plan:** Highlight abnormal BP readings in red with triage alert.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 01`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-037`](./13-project-dependencies.md#dependency-037).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-037`](./14-project-milestones.md#milestone-037).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-012`](./15-release-strategy.md#release-012).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-037`](./10-project-assumptions.md#assumption-037).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-037`](./11-project-constraints.md#constraint-037).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.38 RISK-038: Walk-in Patient Misidentification in Rapid Queue Token Issuance #38
- **Risk Identifier:** `RISK-038` — **Walk-in Patient Misidentification in Rapid Queue Token Issuance #38**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** DEO selecting wrong patient with identical name in rapid search.
- **Risk Event Description:** Medical history cross-contamination and wrong treatment prescribed.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) (Governed by [`GOV-038`](./09-governance-model.md#gov-038)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-038`](./06-stakeholders.md#stakeholder-038).
- **Preventive Action (Pre-Emptive Control):** Display age, gender, ward, and mobile number in selection list.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Multiple name search matches.
- **Early Warning Indicator (Telemetry Signal):** Duplicate name alert dialog.
- **Core Mitigation Strategy:** Display age, gender, ward, and mobile number in selection list.
- **Pre-Authorized Contingency Fallback Plan:** Print photo/UHID barcode on thermal token slip.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 02`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-038`](./13-project-dependencies.md#dependency-038).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-038`](./14-project-milestones.md#milestone-038).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-013`](./15-release-strategy.md#release-013).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-038`](./10-project-assumptions.md#assumption-038).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-038`](./11-project-constraints.md#constraint-038).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.39 RISK-039: ABHA M1 OTP Gateway Latency Exceeding 45 Seconds #39
- **Risk Identifier:** `RISK-039` — **ABHA M1 OTP Gateway Latency Exceeding 45 Seconds #39**
- **Threat Category:** `Interoperability` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** National Health Authority OTP server congested during peak morning hours.
- **Risk Event Description:** Patient registration queue stalls, causing crowd frustration.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) (Governed by [`GOV-039`](./09-governance-model.md#gov-039)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-039`](./06-stakeholders.md#stakeholder-039).
- **Preventive Action (Pre-Emptive Control):** Provide immediate 1-click bypass to issue temporary local UHID.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** ABHA API response time > 15s.
- **Early Warning Indicator (Telemetry Signal):** OTP countdown timer warning.
- **Core Mitigation Strategy:** Provide immediate 1-click bypass to issue temporary local UHID.
- **Pre-Authorized Contingency Fallback Plan:** Background worker links ABHA asynchronously when citizen arrives.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 03`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-039`](./13-project-dependencies.md#dependency-039).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-039`](./14-project-milestones.md#milestone-039).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-014`](./15-release-strategy.md#release-014).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-039`](./10-project-assumptions.md#assumption-039).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-039`](./11-project-constraints.md#constraint-039).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.40 RISK-040: Cellular 4G Tower Congestion During Monsoon Heavy Rainstorms #40
- **Risk Identifier:** `RISK-040` — **Cellular 4G Tower Congestion During Monsoon Heavy Rainstorms #40**
- **Threat Category:** `Network` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Mobile cellular data drops to <50 kbps across entire municipal ward.
- **Risk Event Description:** Clinic unable to synchronize outpatient records to central cloud.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) (Governed by [`GOV-040`](./09-governance-model.md#gov-040)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-040`](./06-stakeholders.md#stakeholder-040).
- **Preventive Action (Pre-Emptive Control):** Automatic switch to local IndexedDB offline storage mode.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Ping packet loss > 20%.
- **Early Warning Indicator (Telemetry Signal):** Offline mode status banner.
- **Core Mitigation Strategy:** Automatic switch to local IndexedDB offline storage mode.
- **Pre-Authorized Contingency Fallback Plan:** Dual-SIM router automatically fails over to alternate carrier.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 04`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-040`](./13-project-dependencies.md#dependency-040).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-040`](./14-project-milestones.md#milestone-040).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-015`](./15-release-strategy.md#release-015).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-040`](./10-project-assumptions.md#assumption-040).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-040`](./11-project-constraints.md#constraint-040).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.41 RISK-041: PostgreSQL Connection Starvation During Morning 09:00 Sync Surge #41
- **Risk Identifier:** `RISK-041` — **PostgreSQL Connection Starvation During Morning 09:00 Sync Surge #41**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** All 183 clinics initiate simultaneous sync connections at clinic opening.
- **Risk Event Description:** Fastify API drops connections, throwing HTTP 500 error codes.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) (Governed by [`GOV-041`](./09-governance-model.md#gov-041)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-041`](./06-stakeholders.md#stakeholder-041).
- **Preventive Action (Pre-Emptive Control):** Implement PgBouncer connection pooling and jittered sync backoff.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** PostgreSQL active connections > 80%.
- **Early Warning Indicator (Telemetry Signal):** Connection pool alert.
- **Core Mitigation Strategy:** Implement PgBouncer connection pooling and jittered sync backoff.
- **Pre-Authorized Contingency Fallback Plan:** Prioritize real-time consultations over background batch logs.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 05`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-041`](./13-project-dependencies.md#dependency-041).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-001`](./14-project-milestones.md#milestone-001).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-016`](./15-release-strategy.md#release-016).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-041`](./10-project-assumptions.md#assumption-041).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-041`](./11-project-constraints.md#constraint-041).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.42 RISK-042: Redis Queue Memory Saturation from Delayed Sync Batch Bursts #42
- **Risk Identifier:** `RISK-042` — **Redis Queue Memory Saturation from Delayed Sync Batch Bursts #42**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Central queue fills with 50,000 pending sync events after internet restore.
- **Risk Event Description:** Redis runs out of RAM and crashes, halting background processing.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) (Governed by [`GOV-042`](./09-governance-model.md#gov-042)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-042`](./06-stakeholders.md#stakeholder-042).
- **Preventive Action (Pre-Emptive Control):** Configure Redis with volatile-lru eviction and RabbitMQ persistence.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Redis memory usage > 85%.
- **Early Warning Indicator (Telemetry Signal):** Redis memory alert pager.
- **Core Mitigation Strategy:** Configure Redis with volatile-lru eviction and RabbitMQ persistence.
- **Pre-Authorized Contingency Fallback Plan:** Scale Redis cluster nodes and partition queues by zone.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 06`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-042`](./13-project-dependencies.md#dependency-042).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-002`](./14-project-milestones.md#milestone-002).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-017`](./15-release-strategy.md#release-017).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-042`](./10-project-assumptions.md#assumption-042).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-042`](./11-project-constraints.md#constraint-042).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.43 RISK-043: Prisma ORM Cold Start Penalty on Micro-VM Node Restarts #43
- **Risk Identifier:** `RISK-043` — **Prisma ORM Cold Start Penalty on Micro-VM Node Restarts #43**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Node.js process restart causing 5-second query latency on initial visit.
- **Risk Event Description:** Front desk check-in stalls momentarily during container bounce.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) (Governed by [`GOV-043`](./09-governance-model.md#gov-043)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-043`](./06-stakeholders.md#stakeholder-043).
- **Preventive Action (Pre-Emptive Control):** Keep warm connection pools and pre-compile Prisma client queries.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Container start time > 3s.
- **Early Warning Indicator (Telemetry Signal):** Container health check warning.
- **Core Mitigation Strategy:** Keep warm connection pools and pre-compile Prisma client queries.
- **Pre-Authorized Contingency Fallback Plan:** Implement Kubernetes rolling deployments with readiness probes.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 07`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-043`](./13-project-dependencies.md#dependency-043).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-003`](./14-project-milestones.md#milestone-003).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-018`](./15-release-strategy.md#release-018).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-043`](./10-project-assumptions.md#assumption-043).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-043`](./11-project-constraints.md#constraint-043).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.44 RISK-044: DuckDB Memory Footprint Exceeding 2GB Container Limit #44
- **Risk Identifier:** `RISK-044` — **DuckDB Memory Footprint Exceeding 2GB Container Limit #44**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Complex 243-ward syndromic query exhausting RAM on analytical micro-VM.
- **Risk Event Description:** Analytical reporting dashboard crashes, delaying disease alerts.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) (Governed by [`GOV-044`](./09-governance-model.md#gov-044)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-044`](./06-stakeholders.md#stakeholder-044).
- **Preventive Action (Pre-Emptive Control):** Chunk analytical queries by municipal zone and stream results.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** DuckDB memory usage > 1.8GB.
- **Early Warning Indicator (Telemetry Signal):** Container memory warning.
- **Core Mitigation Strategy:** Chunk analytical queries by municipal zone and stream results.
- **Pre-Authorized Contingency Fallback Plan:** Increase container memory ceiling to 4GB in Kubernetes spec.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 08`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-044`](./13-project-dependencies.md#dependency-044).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-004`](./14-project-milestones.md#milestone-004).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-019`](./15-release-strategy.md#release-019).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-044`](./10-project-assumptions.md#assumption-044).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-044`](./11-project-constraints.md#constraint-044).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.45 RISK-045: RabbitMQ Dead-Letter Exchange Pile-Up on Malformed Clinical Envelopes #45
- **Risk Identifier:** `RISK-045` — **RabbitMQ Dead-Letter Exchange Pile-Up on Malformed Clinical Envelopes #45**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Corrupted sync packet repeatedly failing schema validation.
- **Risk Event Description:** Message broker queue stalls and unacknowledged messages consume memory.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) (Governed by [`GOV-045`](./09-governance-model.md#gov-045)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-045`](./06-stakeholders.md#stakeholder-045).
- **Preventive Action (Pre-Emptive Control):** Route invalid messages to dead-letter parking lot with alerting.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Dead-letter queue count > 50.
- **Early Warning Indicator (Telemetry Signal):** DLQ alert notification.
- **Core Mitigation Strategy:** Route invalid messages to dead-letter parking lot with alerting.
- **Pre-Authorized Contingency Fallback Plan:** Automated replay script after schema fix.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 09`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-045`](./13-project-dependencies.md#dependency-045).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-005`](./14-project-milestones.md#milestone-005).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-020`](./15-release-strategy.md#release-020).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-045`](./10-project-assumptions.md#assumption-045).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-045`](./11-project-constraints.md#constraint-045).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.46 RISK-046: Service Worker Cache Poisoning on Production Hot-Deployments #46
- **Risk Identifier:** `RISK-046` — **Service Worker Cache Poisoning on Production Hot-Deployments #46**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Stale JavaScript bundle cached in clinic browser after frontend release.
- **Risk Event Description:** Clinic interface throws unhandled JavaScript runtime syntax errors.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) (Governed by [`GOV-001`](./09-governance-model.md#gov-001)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-046`](./06-stakeholders.md#stakeholder-046).
- **Preventive Action (Pre-Emptive Control):** Enforce atomic cache busting with unique hash-based asset URLs.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Service worker version mismatch.
- **Early Warning Indicator (Telemetry Signal):** Cache invalidation toast.
- **Core Mitigation Strategy:** Enforce atomic cache busting with unique hash-based asset URLs.
- **Pre-Authorized Contingency Fallback Plan:** Auto-reload client when new service worker activates.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 10`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-046`](./13-project-dependencies.md#dependency-046).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-006`](./14-project-milestones.md#milestone-006).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-021`](./15-release-strategy.md#release-021).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-046`](./10-project-assumptions.md#assumption-046).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-046`](./11-project-constraints.md#constraint-046).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.47 RISK-047: Kannada Unicode Font (Noto Sans) Rendering Glitches #47
- **Risk Identifier:** `RISK-047` — **Kannada Unicode Font (Noto Sans) Rendering Glitches #47**
- **Threat Category:** `Usability` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Missing glyphs or rendering square boxes on older Linux clinic terminals.
- **Risk Event Description:** Frontline staff unable to read Kannada drug labels or patient names.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) (Governed by [`GOV-002`](./09-governance-model.md#gov-002)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-047`](./06-stakeholders.md#stakeholder-047).
- **Preventive Action (Pre-Emptive Control):** Bundle Noto Sans Kannada WOFF2 directly in PWA asset cache.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Font loading error event.
- **Early Warning Indicator (Telemetry Signal):** Font fallback detection.
- **Core Mitigation Strategy:** Bundle Noto Sans Kannada WOFF2 directly in PWA asset cache.
- **Pre-Authorized Contingency Fallback Plan:** Provide instant toggle switch between Kannada and English.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 11`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-047`](./13-project-dependencies.md#dependency-047).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-007`](./14-project-milestones.md#milestone-007).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-022`](./15-release-strategy.md#release-022).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-047`](./10-project-assumptions.md#assumption-047).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-047`](./11-project-constraints.md#constraint-047).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.48 RISK-048: Missing Patient Consent Artifacts Under India DPDP Act 2023 #48
- **Risk Identifier:** `RISK-048` — **Missing Patient Consent Artifacts Under India DPDP Act 2023 #48**
- **Threat Category:** `Compliance` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Clinic staff bypassing digital consent checkbox to speed up check-in.
- **Risk Event Description:** Statutory regulatory fine or legal penalty from Data Protection Board.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) (Governed by [`GOV-003`](./09-governance-model.md#gov-003)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-048`](./06-stakeholders.md#stakeholder-048).
- **Preventive Action (Pre-Emptive Control):** Hardcode consent capture into registration button click event.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Consent timestamp is null.
- **Early Warning Indicator (Telemetry Signal):** Compliance audit flag.
- **Core Mitigation Strategy:** Hardcode consent capture into registration button click event.
- **Pre-Authorized Contingency Fallback Plan:** Log immutable cryptographic consent artifact in WORM log.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 12`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-048`](./13-project-dependencies.md#dependency-048).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-008`](./14-project-milestones.md#milestone-008).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-023`](./15-release-strategy.md#release-023).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-048`](./10-project-assumptions.md#assumption-048).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-048`](./11-project-constraints.md#constraint-048).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.49 RISK-049: Thermal Paper Roll Depletion Halting Token Issuance at Front Desk #49
- **Risk Identifier:** `RISK-049` — **Thermal Paper Roll Depletion Halting Token Issuance at Front Desk #49**
- **Threat Category:** `Operational` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** DEO runs out of paper rolls during 50-person morning queue surge.
- **Risk Event Description:** Queue stops, patients crowd doctor door, and clinic discipline fails.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) (Governed by [`GOV-004`](./09-governance-model.md#gov-004)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-049`](./06-stakeholders.md#stakeholder-049).
- **Preventive Action (Pre-Emptive Control):** Mandate minimum 5 backup paper rolls stored at each front desk.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Paper roll sensor warning.
- **Early Warning Indicator (Telemetry Signal):** Paper low indicator on UI.
- **Core Mitigation Strategy:** Mandate minimum 5 backup paper rolls stored at each front desk.
- **Pre-Authorized Contingency Fallback Plan:** Display token number on screen and send SMS as paperless fallback.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 13`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-049`](./13-project-dependencies.md#dependency-049).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-009`](./14-project-milestones.md#milestone-009).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-024`](./15-release-strategy.md#release-024).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-049`](./10-project-assumptions.md#assumption-049).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-049`](./11-project-constraints.md#constraint-049).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.50 RISK-050: Unencrypted Thermal Print Spool Files Retaining Patient Identifiers #50
- **Risk Identifier:** `RISK-050` — **Unencrypted Thermal Print Spool Files Retaining Patient Identifiers #50**
- **Threat Category:** `Security` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Temporary spool files cached on public mini-PC hard drive unencrypted.
- **Risk Event Description:** Unauthorized access to citizen health records during hardware service.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) (Governed by [`GOV-005`](./09-governance-model.md#gov-005)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-050`](./06-stakeholders.md#stakeholder-050).
- **Preventive Action (Pre-Emptive Control):** Stream raw ESC/POS bytes directly via Web Serial without disk spool.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Plaintext spool file found.
- **Early Warning Indicator (Telemetry Signal):** Security scan audit flag.
- **Core Mitigation Strategy:** Stream raw ESC/POS bytes directly via Web Serial without disk spool.
- **Pre-Authorized Contingency Fallback Plan:** Enforce full disk encryption via BitLocker/LUKS on all terminals.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 14`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-050`](./13-project-dependencies.md#dependency-050).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-010`](./14-project-milestones.md#milestone-010).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-025`](./15-release-strategy.md#release-025).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-050`](./10-project-assumptions.md#assumption-050).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-050`](./11-project-constraints.md#constraint-050).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.51 RISK-051: BESCOM Grid Blackout Exceeding 1000VA UPS Runtime #51
- **Risk Identifier:** `RISK-051` — **BESCOM Grid Blackout Exceeding 1000VA UPS Runtime #51**
- **Threat Category:** `Infrastructure` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Prolonged power cut at peripheral clinic draining battery before power restore.
- **Risk Event Description:** Terminal shutdown during active consultation session.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) (Governed by [`GOV-006`](./09-governance-model.md#gov-006)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-001`](./06-stakeholders.md#stakeholder-001).
- **Preventive Action (Pre-Emptive Control):** Procure high-capacity 1000VA UPS with 2-hour buffer.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** UPS battery voltage < 11.5V.
- **Early Warning Indicator (Telemetry Signal):** Buzzer telemetry alert.
- **Core Mitigation Strategy:** Procure high-capacity 1000VA UPS with 2-hour buffer.
- **Pre-Authorized Contingency Fallback Plan:** PWA auto-saves session state every 30s to local IndexedDB.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 15`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-051`](./13-project-dependencies.md#dependency-051).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-011`](./14-project-milestones.md#milestone-011).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-001`](./15-release-strategy.md#release-001).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-001`](./10-project-assumptions.md#assumption-001).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-001`](./11-project-constraints.md#constraint-001).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.52 RISK-052: Dexie.js IndexedDB Quota Eviction on Low-Disk Mini-PCs #52
- **Risk Identifier:** `RISK-052` — **Dexie.js IndexedDB Quota Eviction on Low-Disk Mini-PCs #52**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Operating system disk space dips below 10%, triggering browser cache wipe.
- **Risk Event Description:** Loss of un-synchronized offline clinical consultations.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) (Governed by [`GOV-007`](./09-governance-model.md#gov-007)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-002`](./06-stakeholders.md#stakeholder-002).
- **Preventive Action (Pre-Emptive Control):** Request persistent storage permission via StorageManager API.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Browser storage quota warning.
- **Early Warning Indicator (Telemetry Signal):** Local storage alert banner.
- **Core Mitigation Strategy:** Request persistent storage permission via StorageManager API.
- **Pre-Authorized Contingency Fallback Plan:** Export emergency JSON backup to local filesystem.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 16`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-052`](./13-project-dependencies.md#dependency-052).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-012`](./14-project-milestones.md#milestone-012).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-002`](./15-release-strategy.md#release-002).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-002`](./10-project-assumptions.md#assumption-002).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-002`](./11-project-constraints.md#constraint-002).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.53 RISK-053: Web Serial API Disconnects with Thermal Receipt Printers #53
- **Risk Identifier:** `RISK-053` — **Web Serial API Disconnects with Thermal Receipt Printers #53**
- **Threat Category:** `Hardware` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Loose USB cable or power surge disconnecting printer during print queue.
- **Risk Event Description:** Queue token or prescription printing fails, creating desk chaos.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) (Governed by [`GOV-008`](./09-governance-model.md#gov-008)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-003`](./06-stakeholders.md#stakeholder-003).
- **Preventive Action (Pre-Emptive Control):** Auto-reconnect loop on Web Serial with retry queue.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Web Serial port disconnect event.
- **Early Warning Indicator (Telemetry Signal):** Printer offline icon on UI.
- **Core Mitigation Strategy:** Auto-reconnect loop on Web Serial with retry queue.
- **Pre-Authorized Contingency Fallback Plan:** Display printable screen modal as manual backup.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 17`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-053`](./13-project-dependencies.md#dependency-053).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-013`](./14-project-milestones.md#milestone-013).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-003`](./15-release-strategy.md#release-003).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-003`](./10-project-assumptions.md#assumption-003).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-003`](./11-project-constraints.md#constraint-003).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.54 RISK-054: Local Clock Skew Causing Outpatient Sync Sequence Inversion #54
- **Risk Identifier:** `RISK-054` — **Local Clock Skew Causing Outpatient Sync Sequence Inversion #54**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** CMOS battery failure on clinic mini-PC resetting system clock to year 2000.
- **Risk Event Description:** Consultations rejected or ordered incorrectly on central server.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) (Governed by [`GOV-009`](./09-governance-model.md#gov-009)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-004`](./06-stakeholders.md#stakeholder-004).
- **Preventive Action (Pre-Emptive Control):** Enforce server-assigned monotonic sequence numbers via UUIDv7.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** System clock delta > 5 seconds.
- **Early Warning Indicator (Telemetry Signal):** Startup NTP check warning.
- **Core Mitigation Strategy:** Enforce server-assigned monotonic sequence numbers via UUIDv7.
- **Pre-Authorized Contingency Fallback Plan:** Fallback to central timestamp on sync merge.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 18`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-054`](./13-project-dependencies.md#dependency-054).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-014`](./14-project-milestones.md#milestone-014).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-004`](./15-release-strategy.md#release-004).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-004`](./10-project-assumptions.md#assumption-004).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-004`](./11-project-constraints.md#constraint-004).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.55 RISK-055: Pharmacist Dispensing Sound-Alike Look-Alike (LASA) Medication #55
- **Risk Identifier:** `RISK-055` — **Pharmacist Dispensing Sound-Alike Look-Alike (LASA) Medication #55**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Pharmacist picking visually similar packaging under morning queue rush.
- **Risk Event Description:** Adverse patient drug reaction or toxic drug overdose.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) (Governed by [`GOV-010`](./09-governance-model.md#gov-010)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-005`](./06-stakeholders.md#stakeholder-005).
- **Preventive Action (Pre-Emptive Control):** Mandate 2D barcode scan matching prescription before dispense.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Dispensing rush > 20 patients/hour.
- **Early Warning Indicator (Telemetry Signal):** Double-check alert banner.
- **Core Mitigation Strategy:** Mandate 2D barcode scan matching prescription before dispense.
- **Pre-Authorized Contingency Fallback Plan:** Visual drug image and warning badge on dispenser screen.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 01`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-055`](./13-project-dependencies.md#dependency-055).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-015`](./14-project-milestones.md#milestone-015).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-005`](./15-release-strategy.md#release-005).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-005`](./10-project-assumptions.md#assumption-005).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-005`](./11-project-constraints.md#constraint-005).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.56 RISK-056: High-Dose Pediatric Amoxicillin Calculation Error #56
- **Risk Identifier:** `RISK-056` — **High-Dose Pediatric Amoxicillin Calculation Error #56**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Doctor miscalculating milligram dosage per kilogram on unrounded weight.
- **Risk Event Description:** Pediatric medication toxicity or sub-therapeutic treatment.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) (Governed by [`GOV-011`](./09-governance-model.md#gov-011)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-006`](./06-stakeholders.md#stakeholder-006).
- **Preventive Action (Pre-Emptive Control):** Built-in automated mg/kg dosing calculator with hard stops.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Child weight entry < 15kg.
- **Early Warning Indicator (Telemetry Signal):** Dosage ceiling warning badge.
- **Core Mitigation Strategy:** Built-in automated mg/kg dosing calculator with hard stops.
- **Pre-Authorized Contingency Fallback Plan:** Doctor must override with clinical justification reason.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 02`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-056`](./13-project-dependencies.md#dependency-056).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-016`](./14-project-milestones.md#milestone-016).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-006`](./15-release-strategy.md#release-006).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-006`](./10-project-assumptions.md#assumption-006).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-006`](./11-project-constraints.md#constraint-006).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.57 RISK-057: Unreconciled FEFO Expiry Dates Dispensing Expired Drugs #57
- **Risk Identifier:** `RISK-057` — **Unreconciled FEFO Expiry Dates Dispensing Expired Drugs #57**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Older drug batch hidden behind newer delivery in clinic cupboard.
- **Risk Event Description:** Patient ingests expired ineffective or degraded medication.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) (Governed by [`GOV-012`](./09-governance-model.md#gov-012)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-007`](./06-stakeholders.md#stakeholder-007).
- **Preventive Action (Pre-Emptive Control):** Barcode validation blocks dispensing of batches expired or <30d.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Batch expiry date < current date.
- **Early Warning Indicator (Telemetry Signal):** Red expiry warning badge.
- **Core Mitigation Strategy:** Barcode validation blocks dispensing of batches expired or <30d.
- **Pre-Authorized Contingency Fallback Plan:** Automated batch quarantine alert sent to supervisor.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 03`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-057`](./13-project-dependencies.md#dependency-057).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-017`](./14-project-milestones.md#milestone-017).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-007`](./15-release-strategy.md#release-007).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-007`](./10-project-assumptions.md#assumption-007).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-007`](./11-project-constraints.md#constraint-007).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.58 RISK-058: Missing Drug Allergy Contraindication in Fast-Paced Consults #58
- **Risk Identifier:** `RISK-058` — **Missing Drug Allergy Contraindication in Fast-Paced Consults #58**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Doctor omitting allergy check during 90-second consultation rush.
- **Risk Event Description:** Anaphylactic shock or severe allergic reaction in patient.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) (Governed by [`GOV-013`](./09-governance-model.md#gov-013)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-008`](./06-stakeholders.md#stakeholder-008).
- **Preventive Action (Pre-Emptive Control):** Prominent allergy banner pinned to patient header with hard stop.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Prescribing known allergen.
- **Early Warning Indicator (Telemetry Signal):** Flashing red modal alert.
- **Core Mitigation Strategy:** Prominent allergy banner pinned to patient header with hard stop.
- **Pre-Authorized Contingency Fallback Plan:** Require dual confirmation to prescribe cross-reacting drugs.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 04`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-058`](./13-project-dependencies.md#dependency-058).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-018`](./14-project-milestones.md#milestone-018).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-008`](./15-release-strategy.md#release-008).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-008`](./10-project-assumptions.md#assumption-008).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-008`](./11-project-constraints.md#constraint-008).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.59 RISK-059: Point-of-Care Urine Strip Reader Serial Port Lockup #59
- **Risk Identifier:** `RISK-059` — **Point-of-Care Urine Strip Reader Serial Port Lockup #59**
- **Threat Category:** `Hardware` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Serial communication buffer overflow on automated strip analyzer.
- **Risk Event Description:** Lab technician unable to upload urinalysis results to EMR.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) (Governed by [`GOV-014`](./09-governance-model.md#gov-014)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-009`](./06-stakeholders.md#stakeholder-009).
- **Preventive Action (Pre-Emptive Control):** Provide manual result entry fallback with range validation.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Serial read timeout > 10s.
- **Early Warning Indicator (Telemetry Signal):** Serial port error notification.
- **Core Mitigation Strategy:** Provide manual result entry fallback with range validation.
- **Pre-Authorized Contingency Fallback Plan:** Hardware power cycle procedure documented for lab staff.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 05`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-059`](./13-project-dependencies.md#dependency-059).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-019`](./14-project-milestones.md#milestone-019).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-009`](./15-release-strategy.md#release-009).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-009`](./10-project-assumptions.md#assumption-009).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-009`](./11-project-constraints.md#constraint-009).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.60 RISK-060: Critical Hemoglobin (<7.0 g/dL) Panic Value Delivery Failure #60
- **Risk Identifier:** `RISK-060` — **Critical Hemoglobin (<7.0 g/dL) Panic Value Delivery Failure #60**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Lab result marked in lab desk but doctor has already discharged patient.
- **Risk Event Description:** Severe anemic patient sent home without immediate transfusion.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) (Governed by [`GOV-015`](./09-governance-model.md#gov-015)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-010`](./06-stakeholders.md#stakeholder-010).
- **Preventive Action (Pre-Emptive Control):** Instant WebSocket panic alert interrupting doctor screen.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Hemoglobin reading < 7.0 g/dL.
- **Early Warning Indicator (Telemetry Signal):** Audio chime and red banner.
- **Core Mitigation Strategy:** Instant WebSocket panic alert interrupting doctor screen.
- **Pre-Authorized Contingency Fallback Plan:** Staff nurse dispatched to hold patient at dispensary.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 06`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-060`](./13-project-dependencies.md#dependency-060).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-020`](./14-project-milestones.md#milestone-020).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-010`](./15-release-strategy.md#release-010).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-010`](./10-project-assumptions.md#assumption-010).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-010`](./11-project-constraints.md#constraint-010).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.61 RISK-061: Doctor Bypassing Digital Prescription Due to Typing Fatigue #61
- **Risk Identifier:** `RISK-061` — **Doctor Bypassing Digital Prescription Due to Typing Fatigue #61**
- **Threat Category:** `Operational` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Doctor overwhelmed by patient queue reverting to handwritten slips.
- **Risk Event Description:** Broken electronic audit trail, inventory blindness, and unreadable scripts.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) (Governed by [`GOV-016`](./09-governance-model.md#gov-016)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-011`](./06-stakeholders.md#stakeholder-011).
- **Preventive Action (Pre-Emptive Control):** 1-click diagnosis chips, favorite drug bundles, and touch UI.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Consultation digital queue idle.
- **Early Warning Indicator (Telemetry Signal):** Zero digital script alert.
- **Core Mitigation Strategy:** 1-click diagnosis chips, favorite drug bundles, and touch UI.
- **Pre-Authorized Contingency Fallback Plan:** Zonal medical officer conducts on-site clinical workflow audit.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 07`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-061`](./13-project-dependencies.md#dependency-061).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-021`](./14-project-milestones.md#milestone-021).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-011`](./15-release-strategy.md#release-011).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-011`](./10-project-assumptions.md#assumption-011).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-011`](./11-project-constraints.md#constraint-011).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.62 RISK-062: Staff Nurse Omitting Diastolic Blood Pressure in Triage #62
- **Risk Identifier:** `RISK-062` — **Staff Nurse Omitting Diastolic Blood Pressure in Triage #62**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Nurse typing only systolic pressure during rapid morning check-in rush.
- **Risk Event Description:** Incomplete cardiovascular risk stratification for hypertensive patient.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) (Governed by [`GOV-017`](./09-governance-model.md#gov-017)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-012`](./06-stakeholders.md#stakeholder-012).
- **Preventive Action (Pre-Emptive Control):** Form validation enforces both systolic and diastolic values.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Diastolic field left null.
- **Early Warning Indicator (Telemetry Signal):** Validation error badge.
- **Core Mitigation Strategy:** Form validation enforces both systolic and diastolic values.
- **Pre-Authorized Contingency Fallback Plan:** Highlight abnormal BP readings in red with triage alert.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 08`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-062`](./13-project-dependencies.md#dependency-062).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-022`](./14-project-milestones.md#milestone-022).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-012`](./15-release-strategy.md#release-012).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-012`](./10-project-assumptions.md#assumption-012).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-012`](./11-project-constraints.md#constraint-012).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.63 RISK-063: Walk-in Patient Misidentification in Rapid Queue Token Issuance #63
- **Risk Identifier:** `RISK-063` — **Walk-in Patient Misidentification in Rapid Queue Token Issuance #63**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** DEO selecting wrong patient with identical name in rapid search.
- **Risk Event Description:** Medical history cross-contamination and wrong treatment prescribed.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) (Governed by [`GOV-018`](./09-governance-model.md#gov-018)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-013`](./06-stakeholders.md#stakeholder-013).
- **Preventive Action (Pre-Emptive Control):** Display age, gender, ward, and mobile number in selection list.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Multiple name search matches.
- **Early Warning Indicator (Telemetry Signal):** Duplicate name alert dialog.
- **Core Mitigation Strategy:** Display age, gender, ward, and mobile number in selection list.
- **Pre-Authorized Contingency Fallback Plan:** Print photo/UHID barcode on thermal token slip.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 09`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-063`](./13-project-dependencies.md#dependency-063).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-023`](./14-project-milestones.md#milestone-023).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-013`](./15-release-strategy.md#release-013).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-013`](./10-project-assumptions.md#assumption-013).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-013`](./11-project-constraints.md#constraint-013).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.64 RISK-064: ABHA M1 OTP Gateway Latency Exceeding 45 Seconds #64
- **Risk Identifier:** `RISK-064` — **ABHA M1 OTP Gateway Latency Exceeding 45 Seconds #64**
- **Threat Category:** `Interoperability` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** National Health Authority OTP server congested during peak morning hours.
- **Risk Event Description:** Patient registration queue stalls, causing crowd frustration.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) (Governed by [`GOV-019`](./09-governance-model.md#gov-019)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-014`](./06-stakeholders.md#stakeholder-014).
- **Preventive Action (Pre-Emptive Control):** Provide immediate 1-click bypass to issue temporary local UHID.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** ABHA API response time > 15s.
- **Early Warning Indicator (Telemetry Signal):** OTP countdown timer warning.
- **Core Mitigation Strategy:** Provide immediate 1-click bypass to issue temporary local UHID.
- **Pre-Authorized Contingency Fallback Plan:** Background worker links ABHA asynchronously when citizen arrives.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 10`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-064`](./13-project-dependencies.md#dependency-064).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-024`](./14-project-milestones.md#milestone-024).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-014`](./15-release-strategy.md#release-014).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-014`](./10-project-assumptions.md#assumption-014).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-014`](./11-project-constraints.md#constraint-014).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.65 RISK-065: Cellular 4G Tower Congestion During Monsoon Heavy Rainstorms #65
- **Risk Identifier:** `RISK-065` — **Cellular 4G Tower Congestion During Monsoon Heavy Rainstorms #65**
- **Threat Category:** `Network` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Mobile cellular data drops to <50 kbps across entire municipal ward.
- **Risk Event Description:** Clinic unable to synchronize outpatient records to central cloud.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) (Governed by [`GOV-020`](./09-governance-model.md#gov-020)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-015`](./06-stakeholders.md#stakeholder-015).
- **Preventive Action (Pre-Emptive Control):** Automatic switch to local IndexedDB offline storage mode.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Ping packet loss > 20%.
- **Early Warning Indicator (Telemetry Signal):** Offline mode status banner.
- **Core Mitigation Strategy:** Automatic switch to local IndexedDB offline storage mode.
- **Pre-Authorized Contingency Fallback Plan:** Dual-SIM router automatically fails over to alternate carrier.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 11`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-065`](./13-project-dependencies.md#dependency-065).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-025`](./14-project-milestones.md#milestone-025).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-015`](./15-release-strategy.md#release-015).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-015`](./10-project-assumptions.md#assumption-015).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-015`](./11-project-constraints.md#constraint-015).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.66 RISK-066: PostgreSQL Connection Starvation During Morning 09:00 Sync Surge #66
- **Risk Identifier:** `RISK-066` — **PostgreSQL Connection Starvation During Morning 09:00 Sync Surge #66**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** All 183 clinics initiate simultaneous sync connections at clinic opening.
- **Risk Event Description:** Fastify API drops connections, throwing HTTP 500 error codes.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) (Governed by [`GOV-021`](./09-governance-model.md#gov-021)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-016`](./06-stakeholders.md#stakeholder-016).
- **Preventive Action (Pre-Emptive Control):** Implement PgBouncer connection pooling and jittered sync backoff.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** PostgreSQL active connections > 80%.
- **Early Warning Indicator (Telemetry Signal):** Connection pool alert.
- **Core Mitigation Strategy:** Implement PgBouncer connection pooling and jittered sync backoff.
- **Pre-Authorized Contingency Fallback Plan:** Prioritize real-time consultations over background batch logs.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 12`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-066`](./13-project-dependencies.md#dependency-066).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-026`](./14-project-milestones.md#milestone-026).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-016`](./15-release-strategy.md#release-016).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-016`](./10-project-assumptions.md#assumption-016).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-016`](./11-project-constraints.md#constraint-016).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.67 RISK-067: Redis Queue Memory Saturation from Delayed Sync Batch Bursts #67
- **Risk Identifier:** `RISK-067` — **Redis Queue Memory Saturation from Delayed Sync Batch Bursts #67**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Central queue fills with 50,000 pending sync events after internet restore.
- **Risk Event Description:** Redis runs out of RAM and crashes, halting background processing.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) (Governed by [`GOV-022`](./09-governance-model.md#gov-022)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-017`](./06-stakeholders.md#stakeholder-017).
- **Preventive Action (Pre-Emptive Control):** Configure Redis with volatile-lru eviction and RabbitMQ persistence.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Redis memory usage > 85%.
- **Early Warning Indicator (Telemetry Signal):** Redis memory alert pager.
- **Core Mitigation Strategy:** Configure Redis with volatile-lru eviction and RabbitMQ persistence.
- **Pre-Authorized Contingency Fallback Plan:** Scale Redis cluster nodes and partition queues by zone.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 13`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-067`](./13-project-dependencies.md#dependency-067).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-027`](./14-project-milestones.md#milestone-027).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-017`](./15-release-strategy.md#release-017).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-017`](./10-project-assumptions.md#assumption-017).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-017`](./11-project-constraints.md#constraint-017).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.68 RISK-068: Prisma ORM Cold Start Penalty on Micro-VM Node Restarts #68
- **Risk Identifier:** `RISK-068` — **Prisma ORM Cold Start Penalty on Micro-VM Node Restarts #68**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Node.js process restart causing 5-second query latency on initial visit.
- **Risk Event Description:** Front desk check-in stalls momentarily during container bounce.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) (Governed by [`GOV-023`](./09-governance-model.md#gov-023)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-018`](./06-stakeholders.md#stakeholder-018).
- **Preventive Action (Pre-Emptive Control):** Keep warm connection pools and pre-compile Prisma client queries.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Container start time > 3s.
- **Early Warning Indicator (Telemetry Signal):** Container health check warning.
- **Core Mitigation Strategy:** Keep warm connection pools and pre-compile Prisma client queries.
- **Pre-Authorized Contingency Fallback Plan:** Implement Kubernetes rolling deployments with readiness probes.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 14`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-068`](./13-project-dependencies.md#dependency-068).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-028`](./14-project-milestones.md#milestone-028).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-018`](./15-release-strategy.md#release-018).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-018`](./10-project-assumptions.md#assumption-018).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-018`](./11-project-constraints.md#constraint-018).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.69 RISK-069: DuckDB Memory Footprint Exceeding 2GB Container Limit #69
- **Risk Identifier:** `RISK-069` — **DuckDB Memory Footprint Exceeding 2GB Container Limit #69**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Complex 243-ward syndromic query exhausting RAM on analytical micro-VM.
- **Risk Event Description:** Analytical reporting dashboard crashes, delaying disease alerts.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) (Governed by [`GOV-024`](./09-governance-model.md#gov-024)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-019`](./06-stakeholders.md#stakeholder-019).
- **Preventive Action (Pre-Emptive Control):** Chunk analytical queries by municipal zone and stream results.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** DuckDB memory usage > 1.8GB.
- **Early Warning Indicator (Telemetry Signal):** Container memory warning.
- **Core Mitigation Strategy:** Chunk analytical queries by municipal zone and stream results.
- **Pre-Authorized Contingency Fallback Plan:** Increase container memory ceiling to 4GB in Kubernetes spec.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 15`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-069`](./13-project-dependencies.md#dependency-069).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-029`](./14-project-milestones.md#milestone-029).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-019`](./15-release-strategy.md#release-019).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-019`](./10-project-assumptions.md#assumption-019).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-019`](./11-project-constraints.md#constraint-019).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.70 RISK-070: RabbitMQ Dead-Letter Exchange Pile-Up on Malformed Clinical Envelopes #70
- **Risk Identifier:** `RISK-070` — **RabbitMQ Dead-Letter Exchange Pile-Up on Malformed Clinical Envelopes #70**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Corrupted sync packet repeatedly failing schema validation.
- **Risk Event Description:** Message broker queue stalls and unacknowledged messages consume memory.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) (Governed by [`GOV-025`](./09-governance-model.md#gov-025)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-020`](./06-stakeholders.md#stakeholder-020).
- **Preventive Action (Pre-Emptive Control):** Route invalid messages to dead-letter parking lot with alerting.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Dead-letter queue count > 50.
- **Early Warning Indicator (Telemetry Signal):** DLQ alert notification.
- **Core Mitigation Strategy:** Route invalid messages to dead-letter parking lot with alerting.
- **Pre-Authorized Contingency Fallback Plan:** Automated replay script after schema fix.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 16`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-070`](./13-project-dependencies.md#dependency-070).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-030`](./14-project-milestones.md#milestone-030).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-020`](./15-release-strategy.md#release-020).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-020`](./10-project-assumptions.md#assumption-020).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-020`](./11-project-constraints.md#constraint-020).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.71 RISK-071: Service Worker Cache Poisoning on Production Hot-Deployments #71
- **Risk Identifier:** `RISK-071` — **Service Worker Cache Poisoning on Production Hot-Deployments #71**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Stale JavaScript bundle cached in clinic browser after frontend release.
- **Risk Event Description:** Clinic interface throws unhandled JavaScript runtime syntax errors.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) (Governed by [`GOV-026`](./09-governance-model.md#gov-026)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-021`](./06-stakeholders.md#stakeholder-021).
- **Preventive Action (Pre-Emptive Control):** Enforce atomic cache busting with unique hash-based asset URLs.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Service worker version mismatch.
- **Early Warning Indicator (Telemetry Signal):** Cache invalidation toast.
- **Core Mitigation Strategy:** Enforce atomic cache busting with unique hash-based asset URLs.
- **Pre-Authorized Contingency Fallback Plan:** Auto-reload client when new service worker activates.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 17`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-071`](./13-project-dependencies.md#dependency-071).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-031`](./14-project-milestones.md#milestone-031).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-021`](./15-release-strategy.md#release-021).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-021`](./10-project-assumptions.md#assumption-021).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-021`](./11-project-constraints.md#constraint-021).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.72 RISK-072: Kannada Unicode Font (Noto Sans) Rendering Glitches #72
- **Risk Identifier:** `RISK-072` — **Kannada Unicode Font (Noto Sans) Rendering Glitches #72**
- **Threat Category:** `Usability` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Missing glyphs or rendering square boxes on older Linux clinic terminals.
- **Risk Event Description:** Frontline staff unable to read Kannada drug labels or patient names.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) (Governed by [`GOV-027`](./09-governance-model.md#gov-027)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-022`](./06-stakeholders.md#stakeholder-022).
- **Preventive Action (Pre-Emptive Control):** Bundle Noto Sans Kannada WOFF2 directly in PWA asset cache.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Font loading error event.
- **Early Warning Indicator (Telemetry Signal):** Font fallback detection.
- **Core Mitigation Strategy:** Bundle Noto Sans Kannada WOFF2 directly in PWA asset cache.
- **Pre-Authorized Contingency Fallback Plan:** Provide instant toggle switch between Kannada and English.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 18`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-072`](./13-project-dependencies.md#dependency-072).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-032`](./14-project-milestones.md#milestone-032).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-022`](./15-release-strategy.md#release-022).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-022`](./10-project-assumptions.md#assumption-022).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-022`](./11-project-constraints.md#constraint-022).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.73 RISK-073: Missing Patient Consent Artifacts Under India DPDP Act 2023 #73
- **Risk Identifier:** `RISK-073` — **Missing Patient Consent Artifacts Under India DPDP Act 2023 #73**
- **Threat Category:** `Compliance` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Clinic staff bypassing digital consent checkbox to speed up check-in.
- **Risk Event Description:** Statutory regulatory fine or legal penalty from Data Protection Board.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) (Governed by [`GOV-028`](./09-governance-model.md#gov-028)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-023`](./06-stakeholders.md#stakeholder-023).
- **Preventive Action (Pre-Emptive Control):** Hardcode consent capture into registration button click event.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Consent timestamp is null.
- **Early Warning Indicator (Telemetry Signal):** Compliance audit flag.
- **Core Mitigation Strategy:** Hardcode consent capture into registration button click event.
- **Pre-Authorized Contingency Fallback Plan:** Log immutable cryptographic consent artifact in WORM log.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 01`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-073`](./13-project-dependencies.md#dependency-073).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-033`](./14-project-milestones.md#milestone-033).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-023`](./15-release-strategy.md#release-023).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-023`](./10-project-assumptions.md#assumption-023).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-023`](./11-project-constraints.md#constraint-023).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.74 RISK-074: Thermal Paper Roll Depletion Halting Token Issuance at Front Desk #74
- **Risk Identifier:** `RISK-074` — **Thermal Paper Roll Depletion Halting Token Issuance at Front Desk #74**
- **Threat Category:** `Operational` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** DEO runs out of paper rolls during 50-person morning queue surge.
- **Risk Event Description:** Queue stops, patients crowd doctor door, and clinic discipline fails.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) (Governed by [`GOV-029`](./09-governance-model.md#gov-029)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-024`](./06-stakeholders.md#stakeholder-024).
- **Preventive Action (Pre-Emptive Control):** Mandate minimum 5 backup paper rolls stored at each front desk.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Paper roll sensor warning.
- **Early Warning Indicator (Telemetry Signal):** Paper low indicator on UI.
- **Core Mitigation Strategy:** Mandate minimum 5 backup paper rolls stored at each front desk.
- **Pre-Authorized Contingency Fallback Plan:** Display token number on screen and send SMS as paperless fallback.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 02`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-074`](./13-project-dependencies.md#dependency-074).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-034`](./14-project-milestones.md#milestone-034).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-024`](./15-release-strategy.md#release-024).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-024`](./10-project-assumptions.md#assumption-024).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-024`](./11-project-constraints.md#constraint-024).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.75 RISK-075: Unencrypted Thermal Print Spool Files Retaining Patient Identifiers #75
- **Risk Identifier:** `RISK-075` — **Unencrypted Thermal Print Spool Files Retaining Patient Identifiers #75**
- **Threat Category:** `Security` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Temporary spool files cached on public mini-PC hard drive unencrypted.
- **Risk Event Description:** Unauthorized access to citizen health records during hardware service.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) (Governed by [`GOV-030`](./09-governance-model.md#gov-030)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-025`](./06-stakeholders.md#stakeholder-025).
- **Preventive Action (Pre-Emptive Control):** Stream raw ESC/POS bytes directly via Web Serial without disk spool.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Plaintext spool file found.
- **Early Warning Indicator (Telemetry Signal):** Security scan audit flag.
- **Core Mitigation Strategy:** Stream raw ESC/POS bytes directly via Web Serial without disk spool.
- **Pre-Authorized Contingency Fallback Plan:** Enforce full disk encryption via BitLocker/LUKS on all terminals.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 03`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-075`](./13-project-dependencies.md#dependency-075).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-035`](./14-project-milestones.md#milestone-035).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-025`](./15-release-strategy.md#release-025).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-025`](./10-project-assumptions.md#assumption-025).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-025`](./11-project-constraints.md#constraint-025).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.76 RISK-076: BESCOM Grid Blackout Exceeding 1000VA UPS Runtime #76
- **Risk Identifier:** `RISK-076` — **BESCOM Grid Blackout Exceeding 1000VA UPS Runtime #76**
- **Threat Category:** `Infrastructure` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Prolonged power cut at peripheral clinic draining battery before power restore.
- **Risk Event Description:** Terminal shutdown during active consultation session.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) (Governed by [`GOV-031`](./09-governance-model.md#gov-031)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-026`](./06-stakeholders.md#stakeholder-026).
- **Preventive Action (Pre-Emptive Control):** Procure high-capacity 1000VA UPS with 2-hour buffer.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** UPS battery voltage < 11.5V.
- **Early Warning Indicator (Telemetry Signal):** Buzzer telemetry alert.
- **Core Mitigation Strategy:** Procure high-capacity 1000VA UPS with 2-hour buffer.
- **Pre-Authorized Contingency Fallback Plan:** PWA auto-saves session state every 30s to local IndexedDB.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 04`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-001`](./13-project-dependencies.md#dependency-001).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-036`](./14-project-milestones.md#milestone-036).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-001`](./15-release-strategy.md#release-001).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-026`](./10-project-assumptions.md#assumption-026).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-026`](./11-project-constraints.md#constraint-026).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.77 RISK-077: Dexie.js IndexedDB Quota Eviction on Low-Disk Mini-PCs #77
- **Risk Identifier:** `RISK-077` — **Dexie.js IndexedDB Quota Eviction on Low-Disk Mini-PCs #77**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Operating system disk space dips below 10%, triggering browser cache wipe.
- **Risk Event Description:** Loss of un-synchronized offline clinical consultations.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) (Governed by [`GOV-032`](./09-governance-model.md#gov-032)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-027`](./06-stakeholders.md#stakeholder-027).
- **Preventive Action (Pre-Emptive Control):** Request persistent storage permission via StorageManager API.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Browser storage quota warning.
- **Early Warning Indicator (Telemetry Signal):** Local storage alert banner.
- **Core Mitigation Strategy:** Request persistent storage permission via StorageManager API.
- **Pre-Authorized Contingency Fallback Plan:** Export emergency JSON backup to local filesystem.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 05`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-002`](./13-project-dependencies.md#dependency-002).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-037`](./14-project-milestones.md#milestone-037).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-002`](./15-release-strategy.md#release-002).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-027`](./10-project-assumptions.md#assumption-027).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-027`](./11-project-constraints.md#constraint-027).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.78 RISK-078: Web Serial API Disconnects with Thermal Receipt Printers #78
- **Risk Identifier:** `RISK-078` — **Web Serial API Disconnects with Thermal Receipt Printers #78**
- **Threat Category:** `Hardware` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Loose USB cable or power surge disconnecting printer during print queue.
- **Risk Event Description:** Queue token or prescription printing fails, creating desk chaos.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) (Governed by [`GOV-033`](./09-governance-model.md#gov-033)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-028`](./06-stakeholders.md#stakeholder-028).
- **Preventive Action (Pre-Emptive Control):** Auto-reconnect loop on Web Serial with retry queue.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Web Serial port disconnect event.
- **Early Warning Indicator (Telemetry Signal):** Printer offline icon on UI.
- **Core Mitigation Strategy:** Auto-reconnect loop on Web Serial with retry queue.
- **Pre-Authorized Contingency Fallback Plan:** Display printable screen modal as manual backup.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 06`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-003`](./13-project-dependencies.md#dependency-003).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-038`](./14-project-milestones.md#milestone-038).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-003`](./15-release-strategy.md#release-003).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-028`](./10-project-assumptions.md#assumption-028).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-028`](./11-project-constraints.md#constraint-028).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.79 RISK-079: Local Clock Skew Causing Outpatient Sync Sequence Inversion #79
- **Risk Identifier:** `RISK-079` — **Local Clock Skew Causing Outpatient Sync Sequence Inversion #79**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** CMOS battery failure on clinic mini-PC resetting system clock to year 2000.
- **Risk Event Description:** Consultations rejected or ordered incorrectly on central server.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) (Governed by [`GOV-034`](./09-governance-model.md#gov-034)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-029`](./06-stakeholders.md#stakeholder-029).
- **Preventive Action (Pre-Emptive Control):** Enforce server-assigned monotonic sequence numbers via UUIDv7.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** System clock delta > 5 seconds.
- **Early Warning Indicator (Telemetry Signal):** Startup NTP check warning.
- **Core Mitigation Strategy:** Enforce server-assigned monotonic sequence numbers via UUIDv7.
- **Pre-Authorized Contingency Fallback Plan:** Fallback to central timestamp on sync merge.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 07`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-004`](./13-project-dependencies.md#dependency-004).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-039`](./14-project-milestones.md#milestone-039).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-004`](./15-release-strategy.md#release-004).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-029`](./10-project-assumptions.md#assumption-029).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-029`](./11-project-constraints.md#constraint-029).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.80 RISK-080: Pharmacist Dispensing Sound-Alike Look-Alike (LASA) Medication #80
- **Risk Identifier:** `RISK-080` — **Pharmacist Dispensing Sound-Alike Look-Alike (LASA) Medication #80**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Pharmacist picking visually similar packaging under morning queue rush.
- **Risk Event Description:** Adverse patient drug reaction or toxic drug overdose.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) (Governed by [`GOV-035`](./09-governance-model.md#gov-035)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-030`](./06-stakeholders.md#stakeholder-030).
- **Preventive Action (Pre-Emptive Control):** Mandate 2D barcode scan matching prescription before dispense.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Dispensing rush > 20 patients/hour.
- **Early Warning Indicator (Telemetry Signal):** Double-check alert banner.
- **Core Mitigation Strategy:** Mandate 2D barcode scan matching prescription before dispense.
- **Pre-Authorized Contingency Fallback Plan:** Visual drug image and warning badge on dispenser screen.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 08`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-005`](./13-project-dependencies.md#dependency-005).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-040`](./14-project-milestones.md#milestone-040).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-005`](./15-release-strategy.md#release-005).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-030`](./10-project-assumptions.md#assumption-030).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-030`](./11-project-constraints.md#constraint-030).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.81 RISK-081: High-Dose Pediatric Amoxicillin Calculation Error #81
- **Risk Identifier:** `RISK-081` — **High-Dose Pediatric Amoxicillin Calculation Error #81**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Doctor miscalculating milligram dosage per kilogram on unrounded weight.
- **Risk Event Description:** Pediatric medication toxicity or sub-therapeutic treatment.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) (Governed by [`GOV-036`](./09-governance-model.md#gov-036)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-031`](./06-stakeholders.md#stakeholder-031).
- **Preventive Action (Pre-Emptive Control):** Built-in automated mg/kg dosing calculator with hard stops.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Child weight entry < 15kg.
- **Early Warning Indicator (Telemetry Signal):** Dosage ceiling warning badge.
- **Core Mitigation Strategy:** Built-in automated mg/kg dosing calculator with hard stops.
- **Pre-Authorized Contingency Fallback Plan:** Doctor must override with clinical justification reason.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 09`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-006`](./13-project-dependencies.md#dependency-006).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-001`](./14-project-milestones.md#milestone-001).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-006`](./15-release-strategy.md#release-006).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-031`](./10-project-assumptions.md#assumption-031).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-031`](./11-project-constraints.md#constraint-031).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.82 RISK-082: Unreconciled FEFO Expiry Dates Dispensing Expired Drugs #82
- **Risk Identifier:** `RISK-082` — **Unreconciled FEFO Expiry Dates Dispensing Expired Drugs #82**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Older drug batch hidden behind newer delivery in clinic cupboard.
- **Risk Event Description:** Patient ingests expired ineffective or degraded medication.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) (Governed by [`GOV-037`](./09-governance-model.md#gov-037)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-032`](./06-stakeholders.md#stakeholder-032).
- **Preventive Action (Pre-Emptive Control):** Barcode validation blocks dispensing of batches expired or <30d.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Batch expiry date < current date.
- **Early Warning Indicator (Telemetry Signal):** Red expiry warning badge.
- **Core Mitigation Strategy:** Barcode validation blocks dispensing of batches expired or <30d.
- **Pre-Authorized Contingency Fallback Plan:** Automated batch quarantine alert sent to supervisor.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 10`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-007`](./13-project-dependencies.md#dependency-007).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-002`](./14-project-milestones.md#milestone-002).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-007`](./15-release-strategy.md#release-007).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-032`](./10-project-assumptions.md#assumption-032).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-032`](./11-project-constraints.md#constraint-032).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.83 RISK-083: Missing Drug Allergy Contraindication in Fast-Paced Consults #83
- **Risk Identifier:** `RISK-083` — **Missing Drug Allergy Contraindication in Fast-Paced Consults #83**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Doctor omitting allergy check during 90-second consultation rush.
- **Risk Event Description:** Anaphylactic shock or severe allergic reaction in patient.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) (Governed by [`GOV-038`](./09-governance-model.md#gov-038)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-033`](./06-stakeholders.md#stakeholder-033).
- **Preventive Action (Pre-Emptive Control):** Prominent allergy banner pinned to patient header with hard stop.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Prescribing known allergen.
- **Early Warning Indicator (Telemetry Signal):** Flashing red modal alert.
- **Core Mitigation Strategy:** Prominent allergy banner pinned to patient header with hard stop.
- **Pre-Authorized Contingency Fallback Plan:** Require dual confirmation to prescribe cross-reacting drugs.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 11`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-008`](./13-project-dependencies.md#dependency-008).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-003`](./14-project-milestones.md#milestone-003).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-008`](./15-release-strategy.md#release-008).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-033`](./10-project-assumptions.md#assumption-033).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-033`](./11-project-constraints.md#constraint-033).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.84 RISK-084: Point-of-Care Urine Strip Reader Serial Port Lockup #84
- **Risk Identifier:** `RISK-084` — **Point-of-Care Urine Strip Reader Serial Port Lockup #84**
- **Threat Category:** `Hardware` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Serial communication buffer overflow on automated strip analyzer.
- **Risk Event Description:** Lab technician unable to upload urinalysis results to EMR.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) (Governed by [`GOV-039`](./09-governance-model.md#gov-039)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-034`](./06-stakeholders.md#stakeholder-034).
- **Preventive Action (Pre-Emptive Control):** Provide manual result entry fallback with range validation.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Serial read timeout > 10s.
- **Early Warning Indicator (Telemetry Signal):** Serial port error notification.
- **Core Mitigation Strategy:** Provide manual result entry fallback with range validation.
- **Pre-Authorized Contingency Fallback Plan:** Hardware power cycle procedure documented for lab staff.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 12`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-009`](./13-project-dependencies.md#dependency-009).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-004`](./14-project-milestones.md#milestone-004).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-009`](./15-release-strategy.md#release-009).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-034`](./10-project-assumptions.md#assumption-034).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-034`](./11-project-constraints.md#constraint-034).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.85 RISK-085: Critical Hemoglobin (<7.0 g/dL) Panic Value Delivery Failure #85
- **Risk Identifier:** `RISK-085` — **Critical Hemoglobin (<7.0 g/dL) Panic Value Delivery Failure #85**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Lab result marked in lab desk but doctor has already discharged patient.
- **Risk Event Description:** Severe anemic patient sent home without immediate transfusion.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) (Governed by [`GOV-040`](./09-governance-model.md#gov-040)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-035`](./06-stakeholders.md#stakeholder-035).
- **Preventive Action (Pre-Emptive Control):** Instant WebSocket panic alert interrupting doctor screen.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Hemoglobin reading < 7.0 g/dL.
- **Early Warning Indicator (Telemetry Signal):** Audio chime and red banner.
- **Core Mitigation Strategy:** Instant WebSocket panic alert interrupting doctor screen.
- **Pre-Authorized Contingency Fallback Plan:** Staff nurse dispatched to hold patient at dispensary.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 13`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-010`](./13-project-dependencies.md#dependency-010).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-005`](./14-project-milestones.md#milestone-005).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-010`](./15-release-strategy.md#release-010).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-035`](./10-project-assumptions.md#assumption-035).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-035`](./11-project-constraints.md#constraint-035).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.86 RISK-086: Doctor Bypassing Digital Prescription Due to Typing Fatigue #86
- **Risk Identifier:** `RISK-086` — **Doctor Bypassing Digital Prescription Due to Typing Fatigue #86**
- **Threat Category:** `Operational` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Doctor overwhelmed by patient queue reverting to handwritten slips.
- **Risk Event Description:** Broken electronic audit trail, inventory blindness, and unreadable scripts.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) (Governed by [`GOV-041`](./09-governance-model.md#gov-041)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-036`](./06-stakeholders.md#stakeholder-036).
- **Preventive Action (Pre-Emptive Control):** 1-click diagnosis chips, favorite drug bundles, and touch UI.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Consultation digital queue idle.
- **Early Warning Indicator (Telemetry Signal):** Zero digital script alert.
- **Core Mitigation Strategy:** 1-click diagnosis chips, favorite drug bundles, and touch UI.
- **Pre-Authorized Contingency Fallback Plan:** Zonal medical officer conducts on-site clinical workflow audit.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 14`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-011`](./13-project-dependencies.md#dependency-011).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-006`](./14-project-milestones.md#milestone-006).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-011`](./15-release-strategy.md#release-011).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-036`](./10-project-assumptions.md#assumption-036).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-036`](./11-project-constraints.md#constraint-036).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.87 RISK-087: Staff Nurse Omitting Diastolic Blood Pressure in Triage #87
- **Risk Identifier:** `RISK-087` — **Staff Nurse Omitting Diastolic Blood Pressure in Triage #87**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Nurse typing only systolic pressure during rapid morning check-in rush.
- **Risk Event Description:** Incomplete cardiovascular risk stratification for hypertensive patient.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) (Governed by [`GOV-042`](./09-governance-model.md#gov-042)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-037`](./06-stakeholders.md#stakeholder-037).
- **Preventive Action (Pre-Emptive Control):** Form validation enforces both systolic and diastolic values.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Diastolic field left null.
- **Early Warning Indicator (Telemetry Signal):** Validation error badge.
- **Core Mitigation Strategy:** Form validation enforces both systolic and diastolic values.
- **Pre-Authorized Contingency Fallback Plan:** Highlight abnormal BP readings in red with triage alert.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 15`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-012`](./13-project-dependencies.md#dependency-012).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-007`](./14-project-milestones.md#milestone-007).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-012`](./15-release-strategy.md#release-012).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-037`](./10-project-assumptions.md#assumption-037).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-037`](./11-project-constraints.md#constraint-037).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.88 RISK-088: Walk-in Patient Misidentification in Rapid Queue Token Issuance #88
- **Risk Identifier:** `RISK-088` — **Walk-in Patient Misidentification in Rapid Queue Token Issuance #88**
- **Threat Category:** `Clinical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** DEO selecting wrong patient with identical name in rapid search.
- **Risk Event Description:** Medical history cross-contamination and wrong treatment prescribed.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) (Governed by [`GOV-043`](./09-governance-model.md#gov-043)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-038`](./06-stakeholders.md#stakeholder-038).
- **Preventive Action (Pre-Emptive Control):** Display age, gender, ward, and mobile number in selection list.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Multiple name search matches.
- **Early Warning Indicator (Telemetry Signal):** Duplicate name alert dialog.
- **Core Mitigation Strategy:** Display age, gender, ward, and mobile number in selection list.
- **Pre-Authorized Contingency Fallback Plan:** Print photo/UHID barcode on thermal token slip.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 16`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-013`](./13-project-dependencies.md#dependency-013).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-008`](./14-project-milestones.md#milestone-008).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-013`](./15-release-strategy.md#release-013).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-038`](./10-project-assumptions.md#assumption-038).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-038`](./11-project-constraints.md#constraint-038).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.89 RISK-089: ABHA M1 OTP Gateway Latency Exceeding 45 Seconds #89
- **Risk Identifier:** `RISK-089` — **ABHA M1 OTP Gateway Latency Exceeding 45 Seconds #89**
- **Threat Category:** `Interoperability` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** National Health Authority OTP server congested during peak morning hours.
- **Risk Event Description:** Patient registration queue stalls, causing crowd frustration.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) (Governed by [`GOV-044`](./09-governance-model.md#gov-044)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-039`](./06-stakeholders.md#stakeholder-039).
- **Preventive Action (Pre-Emptive Control):** Provide immediate 1-click bypass to issue temporary local UHID.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** ABHA API response time > 15s.
- **Early Warning Indicator (Telemetry Signal):** OTP countdown timer warning.
- **Core Mitigation Strategy:** Provide immediate 1-click bypass to issue temporary local UHID.
- **Pre-Authorized Contingency Fallback Plan:** Background worker links ABHA asynchronously when citizen arrives.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 17`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-014`](./13-project-dependencies.md#dependency-014).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-009`](./14-project-milestones.md#milestone-009).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-014`](./15-release-strategy.md#release-014).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-039`](./10-project-assumptions.md#assumption-039).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-039`](./11-project-constraints.md#constraint-039).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.90 RISK-090: Cellular 4G Tower Congestion During Monsoon Heavy Rainstorms #90
- **Risk Identifier:** `RISK-090` — **Cellular 4G Tower Congestion During Monsoon Heavy Rainstorms #90**
- **Threat Category:** `Network` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Mobile cellular data drops to <50 kbps across entire municipal ward.
- **Risk Event Description:** Clinic unable to synchronize outpatient records to central cloud.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) (Governed by [`GOV-045`](./09-governance-model.md#gov-045)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-040`](./06-stakeholders.md#stakeholder-040).
- **Preventive Action (Pre-Emptive Control):** Automatic switch to local IndexedDB offline storage mode.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Ping packet loss > 20%.
- **Early Warning Indicator (Telemetry Signal):** Offline mode status banner.
- **Core Mitigation Strategy:** Automatic switch to local IndexedDB offline storage mode.
- **Pre-Authorized Contingency Fallback Plan:** Dual-SIM router automatically fails over to alternate carrier.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 18`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-015`](./13-project-dependencies.md#dependency-015).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-010`](./14-project-milestones.md#milestone-010).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-015`](./15-release-strategy.md#release-015).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-040`](./10-project-assumptions.md#assumption-040).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-040`](./11-project-constraints.md#constraint-040).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.91 RISK-091: PostgreSQL Connection Starvation During Morning 09:00 Sync Surge #91
- **Risk Identifier:** `RISK-091` — **PostgreSQL Connection Starvation During Morning 09:00 Sync Surge #91**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** All 183 clinics initiate simultaneous sync connections at clinic opening.
- **Risk Event Description:** Fastify API drops connections, throwing HTTP 500 error codes.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) (Governed by [`GOV-001`](./09-governance-model.md#gov-001)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-041`](./06-stakeholders.md#stakeholder-041).
- **Preventive Action (Pre-Emptive Control):** Implement PgBouncer connection pooling and jittered sync backoff.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** PostgreSQL active connections > 80%.
- **Early Warning Indicator (Telemetry Signal):** Connection pool alert.
- **Core Mitigation Strategy:** Implement PgBouncer connection pooling and jittered sync backoff.
- **Pre-Authorized Contingency Fallback Plan:** Prioritize real-time consultations over background batch logs.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 01`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-016`](./13-project-dependencies.md#dependency-016).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-011`](./14-project-milestones.md#milestone-011).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-016`](./15-release-strategy.md#release-016).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-041`](./10-project-assumptions.md#assumption-041).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-041`](./11-project-constraints.md#constraint-041).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.92 RISK-092: Redis Queue Memory Saturation from Delayed Sync Batch Bursts #92
- **Risk Identifier:** `RISK-092` — **Redis Queue Memory Saturation from Delayed Sync Batch Bursts #92**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Central queue fills with 50,000 pending sync events after internet restore.
- **Risk Event Description:** Redis runs out of RAM and crashes, halting background processing.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) (Governed by [`GOV-002`](./09-governance-model.md#gov-002)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-042`](./06-stakeholders.md#stakeholder-042).
- **Preventive Action (Pre-Emptive Control):** Configure Redis with volatile-lru eviction and RabbitMQ persistence.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Redis memory usage > 85%.
- **Early Warning Indicator (Telemetry Signal):** Redis memory alert pager.
- **Core Mitigation Strategy:** Configure Redis with volatile-lru eviction and RabbitMQ persistence.
- **Pre-Authorized Contingency Fallback Plan:** Scale Redis cluster nodes and partition queues by zone.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 02`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-017`](./13-project-dependencies.md#dependency-017).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-012`](./14-project-milestones.md#milestone-012).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-017`](./15-release-strategy.md#release-017).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-042`](./10-project-assumptions.md#assumption-042).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-042`](./11-project-constraints.md#constraint-042).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.93 RISK-093: Prisma ORM Cold Start Penalty on Micro-VM Node Restarts #93
- **Risk Identifier:** `RISK-093` — **Prisma ORM Cold Start Penalty on Micro-VM Node Restarts #93**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Node.js process restart causing 5-second query latency on initial visit.
- **Risk Event Description:** Front desk check-in stalls momentarily during container bounce.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) (Governed by [`GOV-003`](./09-governance-model.md#gov-003)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-043`](./06-stakeholders.md#stakeholder-043).
- **Preventive Action (Pre-Emptive Control):** Keep warm connection pools and pre-compile Prisma client queries.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Container start time > 3s.
- **Early Warning Indicator (Telemetry Signal):** Container health check warning.
- **Core Mitigation Strategy:** Keep warm connection pools and pre-compile Prisma client queries.
- **Pre-Authorized Contingency Fallback Plan:** Implement Kubernetes rolling deployments with readiness probes.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 03`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-018`](./13-project-dependencies.md#dependency-018).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-013`](./14-project-milestones.md#milestone-013).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-018`](./15-release-strategy.md#release-018).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-043`](./10-project-assumptions.md#assumption-043).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-043`](./11-project-constraints.md#constraint-043).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.94 RISK-094: DuckDB Memory Footprint Exceeding 2GB Container Limit #94
- **Risk Identifier:** `RISK-094` — **DuckDB Memory Footprint Exceeding 2GB Container Limit #94**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Complex 243-ward syndromic query exhausting RAM on analytical micro-VM.
- **Risk Event Description:** Analytical reporting dashboard crashes, delaying disease alerts.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) (Governed by [`GOV-004`](./09-governance-model.md#gov-004)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-044`](./06-stakeholders.md#stakeholder-044).
- **Preventive Action (Pre-Emptive Control):** Chunk analytical queries by municipal zone and stream results.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** DuckDB memory usage > 1.8GB.
- **Early Warning Indicator (Telemetry Signal):** Container memory warning.
- **Core Mitigation Strategy:** Chunk analytical queries by municipal zone and stream results.
- **Pre-Authorized Contingency Fallback Plan:** Increase container memory ceiling to 4GB in Kubernetes spec.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 04`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-019`](./13-project-dependencies.md#dependency-019).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-014`](./14-project-milestones.md#milestone-014).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-019`](./15-release-strategy.md#release-019).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-044`](./10-project-assumptions.md#assumption-044).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-044`](./11-project-constraints.md#constraint-044).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.95 RISK-095: RabbitMQ Dead-Letter Exchange Pile-Up on Malformed Clinical Envelopes #95
- **Risk Identifier:** `RISK-095` — **RabbitMQ Dead-Letter Exchange Pile-Up on Malformed Clinical Envelopes #95**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** Corrupted sync packet repeatedly failing schema validation.
- **Risk Event Description:** Message broker queue stalls and unacknowledged messages consume memory.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) (Governed by [`GOV-005`](./09-governance-model.md#gov-005)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-045`](./06-stakeholders.md#stakeholder-045).
- **Preventive Action (Pre-Emptive Control):** Route invalid messages to dead-letter parking lot with alerting.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Dead-letter queue count > 50.
- **Early Warning Indicator (Telemetry Signal):** DLQ alert notification.
- **Core Mitigation Strategy:** Route invalid messages to dead-letter parking lot with alerting.
- **Pre-Authorized Contingency Fallback Plan:** Automated replay script after schema fix.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 05`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-020`](./13-project-dependencies.md#dependency-020).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-015`](./14-project-milestones.md#milestone-015).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-020`](./15-release-strategy.md#release-020).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-045`](./10-project-assumptions.md#assumption-045).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-045`](./11-project-constraints.md#constraint-045).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.96 RISK-096: Service Worker Cache Poisoning on Production Hot-Deployments #96
- **Risk Identifier:** `RISK-096` — **Service Worker Cache Poisoning on Production Hot-Deployments #96**
- **Threat Category:** `Technical` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Stale JavaScript bundle cached in clinic browser after frontend release.
- **Risk Event Description:** Clinic interface throws unhandled JavaScript runtime syntax errors.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) (Governed by [`GOV-006`](./09-governance-model.md#gov-006)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-046`](./06-stakeholders.md#stakeholder-046).
- **Preventive Action (Pre-Emptive Control):** Enforce atomic cache busting with unique hash-based asset URLs.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Service worker version mismatch.
- **Early Warning Indicator (Telemetry Signal):** Cache invalidation toast.
- **Core Mitigation Strategy:** Enforce atomic cache busting with unique hash-based asset URLs.
- **Pre-Authorized Contingency Fallback Plan:** Auto-reload client when new service worker activates.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 06`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-021`](./13-project-dependencies.md#dependency-021).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-016`](./14-project-milestones.md#milestone-016).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-021`](./15-release-strategy.md#release-021).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-046`](./10-project-assumptions.md#assumption-046).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-046`](./11-project-constraints.md#constraint-046).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.97 RISK-097: Kannada Unicode Font (Noto Sans) Rendering Glitches #97
- **Risk Identifier:** `RISK-097` — **Kannada Unicode Font (Noto Sans) Rendering Glitches #97**
- **Threat Category:** `Usability` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `5/5` | Impact: `5/5` | **Risk Exposure Score:** `25/25` (`CRITICAL`)
- **Root Cause Analysis:** Missing glyphs or rendering square boxes on older Linux clinic terminals.
- **Risk Event Description:** Frontline staff unable to read Kannada drug labels or patient names.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) (Governed by [`GOV-007`](./09-governance-model.md#gov-007)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-047`](./06-stakeholders.md#stakeholder-047).
- **Preventive Action (Pre-Emptive Control):** Bundle Noto Sans Kannada WOFF2 directly in PWA asset cache.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Font loading error event.
- **Early Warning Indicator (Telemetry Signal):** Font fallback detection.
- **Core Mitigation Strategy:** Bundle Noto Sans Kannada WOFF2 directly in PWA asset cache.
- **Pre-Authorized Contingency Fallback Plan:** Provide instant toggle switch between Kannada and English.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 07`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-022`](./13-project-dependencies.md#dependency-022).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-017`](./14-project-milestones.md#milestone-017).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-022`](./15-release-strategy.md#release-022).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-047`](./10-project-assumptions.md#assumption-047).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-047`](./11-project-constraints.md#constraint-047).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.98 RISK-098: Missing Patient Consent Artifacts Under India DPDP Act 2023 #98
- **Risk Identifier:** `RISK-098` — **Missing Patient Consent Artifacts Under India DPDP Act 2023 #98**
- **Threat Category:** `Compliance` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `4/5` | Impact: `4/5` | **Risk Exposure Score:** `16/25` (`CRITICAL`)
- **Root Cause Analysis:** Clinic staff bypassing digital consent checkbox to speed up check-in.
- **Risk Event Description:** Statutory regulatory fine or legal penalty from Data Protection Board.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) (Governed by [`GOV-008`](./09-governance-model.md#gov-008)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-048`](./06-stakeholders.md#stakeholder-048).
- **Preventive Action (Pre-Emptive Control):** Hardcode consent capture into registration button click event.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Consent timestamp is null.
- **Early Warning Indicator (Telemetry Signal):** Compliance audit flag.
- **Core Mitigation Strategy:** Hardcode consent capture into registration button click event.
- **Pre-Authorized Contingency Fallback Plan:** Log immutable cryptographic consent artifact in WORM log.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 08`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-023`](./13-project-dependencies.md#dependency-023).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-018`](./14-project-milestones.md#milestone-018).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-023`](./15-release-strategy.md#release-023).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-048`](./10-project-assumptions.md#assumption-048).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-048`](./11-project-constraints.md#constraint-048).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.99 RISK-099: Thermal Paper Roll Depletion Halting Token Issuance at Front Desk #99
- **Risk Identifier:** `RISK-099` — **Thermal Paper Roll Depletion Halting Token Issuance at Front Desk #99**
- **Threat Category:** `Operational` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `3/5` | Impact: `3/5` | **Risk Exposure Score:** `9/25` (`MEDIUM`)
- **Root Cause Analysis:** DEO runs out of paper rolls during 50-person morning queue surge.
- **Risk Event Description:** Queue stops, patients crowd doctor door, and clinic discipline fails.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) (Governed by [`GOV-009`](./09-governance-model.md#gov-009)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-049`](./06-stakeholders.md#stakeholder-049).
- **Preventive Action (Pre-Emptive Control):** Mandate minimum 5 backup paper rolls stored at each front desk.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Paper roll sensor warning.
- **Early Warning Indicator (Telemetry Signal):** Paper low indicator on UI.
- **Core Mitigation Strategy:** Mandate minimum 5 backup paper rolls stored at each front desk.
- **Pre-Authorized Contingency Fallback Plan:** Display token number on screen and send SMS as paperless fallback.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 09`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-024`](./13-project-dependencies.md#dependency-024).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-019`](./14-project-milestones.md#milestone-019).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-024`](./15-release-strategy.md#release-024).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-049`](./10-project-assumptions.md#assumption-049).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-049`](./11-project-constraints.md#constraint-049).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

### 4.100 RISK-100: Unencrypted Thermal Print Spool Files Retaining Patient Identifiers #100
- **Risk Identifier:** `RISK-100` — **Unencrypted Thermal Print Spool Files Retaining Patient Identifiers #100**
- **Threat Category:** `Security` | **Current Lifecycle Status:** `MONITORED`
- **Quantitative Assessment:** Probability: `2/5` | Impact: `2/5` | **Risk Exposure Score:** `4/25` (`LOW`)
- **Root Cause Analysis:** Temporary spool files cached on public mini-PC hard drive unencrypted.
- **Risk Event Description:** Unauthorized access to citizen health records during hardware service.
- **Direct Clinical & Operational Impact:** Breach of clinical safety SLA, operational delay, or data integrity loss..
- **Accountable Risk Steward:** [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) (Governed by [`GOV-010`](./09-governance-model.md#gov-010)).
- **Impacted Stakeholder Group:** Directly affects [`STAKEHOLDER-050`](./06-stakeholders.md#stakeholder-050).
- **Preventive Action (Pre-Emptive Control):** Stream raw ESC/POS bytes directly via Web Serial without disk spool.
- **Detective Control (Early Warning Metric):** Continuous synthetic monitoring and automated health checks.
- **Contingency Activation Trigger:** Plaintext spool file found.
- **Early Warning Indicator (Telemetry Signal):** Security scan audit flag.
- **Core Mitigation Strategy:** Stream raw ESC/POS bytes directly via Web Serial without disk spool.
- **Pre-Authorized Contingency Fallback Plan:** Enforce full disk encryption via BitLocker/LUKS on all terminals.
- **Post-Mitigation Residual Risk:** `LOW` | **Target Resolution Date:** `Sprint 10`.
- **Coupled Project Dependency:** Tied to delivery of [`DEPENDENCY-025`](./13-project-dependencies.md#dependency-025).
- **Coupled Delivery Milestone:** Threatens successful exit gate of [`MILESTONE-020`](./14-project-milestones.md#milestone-020).
- **Coupled Software Release:** Governs deployment gate of [`RELEASE-025`](./15-release-strategy.md#release-025).
- **Linked Project Assumption:** Originates from uncertainty in [`ASSUMPTION-050`](./10-project-assumptions.md#assumption-050).
- **Governing Boundary Constraint:** Constrained by non-negotiable rule [`CONSTRAINT-050`](./11-project-constraints.md#constraint-050).
- **Frontline Operational Guidance:** Clinic staff must follow standardized fallback SOPs without panic; local offline queue preserves encounter state.
- **Zonal Field Audit Mechanism:** Zonal compliance officer inspects facility telemetry and physical backups monthly.

## 5. Top 10 Critical Risks Architectural & Clinical Deep Dive
Exhaustive analysis of the top 10 highest-scoring existential threats to the platform:

### 5.1 Critical Risk Review: RISK-001 — BESCOM Grid Blackout Exceeding 1000VA UPS Runtime
- **Risk Exposure Score:** `25/25` (`CRITICAL`) | **Category:** `Infrastructure`
- **Primary Threat Vector:** Prolonged power cut at peripheral clinic draining battery before power restore leading to Terminal shutdown during active consultation session.
- **Worst-Case Catastrophic Impact:** Complete stoppage of primary outpatient care across multiple wards, severe data loss, or patient safety breach.
- **Architectural Defense-in-Depth:**
  - Multi-tier redundancy: local client IndexedDB caching, automated Fastify retry queues, dual-SIM cellular failover, and line-interactive UPS holdover.
  - Complete decoupling of offline clinical workflows from central cloud database availability.
- **Accountable Executive Lead:** [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) with reporting line directly to the Special Commissioner (Health).
- **Continuous Verification Cadence:** Monitored daily in automated Prometheus dashboards and reviewed weekly at CCB meetings.

### 5.2 Critical Risk Review: RISK-002 — Dexie.js IndexedDB Quota Eviction on Low-Disk Mini-PCs
- **Risk Exposure Score:** `16/25` (`CRITICAL`) | **Category:** `Technical`
- **Primary Threat Vector:** Operating system disk space dips below 10%, triggering browser cache wipe leading to Loss of un-synchronized offline clinical consultations.
- **Worst-Case Catastrophic Impact:** Complete stoppage of primary outpatient care across multiple wards, severe data loss, or patient safety breach.
- **Architectural Defense-in-Depth:**
  - Multi-tier redundancy: local client IndexedDB caching, automated Fastify retry queues, dual-SIM cellular failover, and line-interactive UPS holdover.
  - Complete decoupling of offline clinical workflows from central cloud database availability.
- **Accountable Executive Lead:** [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) with reporting line directly to the Special Commissioner (Health).
- **Continuous Verification Cadence:** Monitored daily in automated Prometheus dashboards and reviewed weekly at CCB meetings.

### 5.3 Critical Risk Review: RISK-003 — Web Serial API Disconnects with Thermal Receipt Printers
- **Risk Exposure Score:** `9/25` (`MEDIUM`) | **Category:** `Hardware`
- **Primary Threat Vector:** Loose USB cable or power surge disconnecting printer during print queue leading to Queue token or prescription printing fails, creating desk chaos.
- **Worst-Case Catastrophic Impact:** Complete stoppage of primary outpatient care across multiple wards, severe data loss, or patient safety breach.
- **Architectural Defense-in-Depth:**
  - Multi-tier redundancy: local client IndexedDB caching, automated Fastify retry queues, dual-SIM cellular failover, and line-interactive UPS holdover.
  - Complete decoupling of offline clinical workflows from central cloud database availability.
- **Accountable Executive Lead:** [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) with reporting line directly to the Special Commissioner (Health).
- **Continuous Verification Cadence:** Monitored daily in automated Prometheus dashboards and reviewed weekly at CCB meetings.

### 5.4 Critical Risk Review: RISK-004 — Local Clock Skew Causing Outpatient Sync Sequence Inversion
- **Risk Exposure Score:** `4/25` (`LOW`) | **Category:** `Technical`
- **Primary Threat Vector:** CMOS battery failure on clinic mini-PC resetting system clock to year 2000 leading to Consultations rejected or ordered incorrectly on central server.
- **Worst-Case Catastrophic Impact:** Complete stoppage of primary outpatient care across multiple wards, severe data loss, or patient safety breach.
- **Architectural Defense-in-Depth:**
  - Multi-tier redundancy: local client IndexedDB caching, automated Fastify retry queues, dual-SIM cellular failover, and line-interactive UPS holdover.
  - Complete decoupling of offline clinical workflows from central cloud database availability.
- **Accountable Executive Lead:** [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) with reporting line directly to the Special Commissioner (Health).
- **Continuous Verification Cadence:** Monitored daily in automated Prometheus dashboards and reviewed weekly at CCB meetings.

### 5.5 Critical Risk Review: RISK-005 — Pharmacist Dispensing Sound-Alike Look-Alike (LASA) Medication
- **Risk Exposure Score:** `25/25` (`CRITICAL`) | **Category:** `Clinical`
- **Primary Threat Vector:** Pharmacist picking visually similar packaging under morning queue rush leading to Adverse patient drug reaction or toxic drug overdose.
- **Worst-Case Catastrophic Impact:** Complete stoppage of primary outpatient care across multiple wards, severe data loss, or patient safety breach.
- **Architectural Defense-in-Depth:**
  - Multi-tier redundancy: local client IndexedDB caching, automated Fastify retry queues, dual-SIM cellular failover, and line-interactive UPS holdover.
  - Complete decoupling of offline clinical workflows from central cloud database availability.
- **Accountable Executive Lead:** [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) with reporting line directly to the Special Commissioner (Health).
- **Continuous Verification Cadence:** Monitored daily in automated Prometheus dashboards and reviewed weekly at CCB meetings.

### 5.6 Critical Risk Review: RISK-006 — High-Dose Pediatric Amoxicillin Calculation Error
- **Risk Exposure Score:** `16/25` (`CRITICAL`) | **Category:** `Clinical`
- **Primary Threat Vector:** Doctor miscalculating milligram dosage per kilogram on unrounded weight leading to Pediatric medication toxicity or sub-therapeutic treatment.
- **Worst-Case Catastrophic Impact:** Complete stoppage of primary outpatient care across multiple wards, severe data loss, or patient safety breach.
- **Architectural Defense-in-Depth:**
  - Multi-tier redundancy: local client IndexedDB caching, automated Fastify retry queues, dual-SIM cellular failover, and line-interactive UPS holdover.
  - Complete decoupling of offline clinical workflows from central cloud database availability.
- **Accountable Executive Lead:** [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) with reporting line directly to the Special Commissioner (Health).
- **Continuous Verification Cadence:** Monitored daily in automated Prometheus dashboards and reviewed weekly at CCB meetings.

### 5.7 Critical Risk Review: RISK-007 — Unreconciled FEFO Expiry Dates Dispensing Expired Drugs
- **Risk Exposure Score:** `9/25` (`MEDIUM`) | **Category:** `Clinical`
- **Primary Threat Vector:** Older drug batch hidden behind newer delivery in clinic cupboard leading to Patient ingests expired ineffective or degraded medication.
- **Worst-Case Catastrophic Impact:** Complete stoppage of primary outpatient care across multiple wards, severe data loss, or patient safety breach.
- **Architectural Defense-in-Depth:**
  - Multi-tier redundancy: local client IndexedDB caching, automated Fastify retry queues, dual-SIM cellular failover, and line-interactive UPS holdover.
  - Complete decoupling of offline clinical workflows from central cloud database availability.
- **Accountable Executive Lead:** [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) with reporting line directly to the Special Commissioner (Health).
- **Continuous Verification Cadence:** Monitored daily in automated Prometheus dashboards and reviewed weekly at CCB meetings.

### 5.8 Critical Risk Review: RISK-008 — Missing Drug Allergy Contraindication in Fast-Paced Consults
- **Risk Exposure Score:** `4/25` (`LOW`) | **Category:** `Clinical`
- **Primary Threat Vector:** Doctor omitting allergy check during 90-second consultation rush leading to Anaphylactic shock or severe allergic reaction in patient.
- **Worst-Case Catastrophic Impact:** Complete stoppage of primary outpatient care across multiple wards, severe data loss, or patient safety breach.
- **Architectural Defense-in-Depth:**
  - Multi-tier redundancy: local client IndexedDB caching, automated Fastify retry queues, dual-SIM cellular failover, and line-interactive UPS holdover.
  - Complete decoupling of offline clinical workflows from central cloud database availability.
- **Accountable Executive Lead:** [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) with reporting line directly to the Special Commissioner (Health).
- **Continuous Verification Cadence:** Monitored daily in automated Prometheus dashboards and reviewed weekly at CCB meetings.

### 5.9 Critical Risk Review: RISK-009 — Point-of-Care Urine Strip Reader Serial Port Lockup
- **Risk Exposure Score:** `25/25` (`CRITICAL`) | **Category:** `Hardware`
- **Primary Threat Vector:** Serial communication buffer overflow on automated strip analyzer leading to Lab technician unable to upload urinalysis results to EMR.
- **Worst-Case Catastrophic Impact:** Complete stoppage of primary outpatient care across multiple wards, severe data loss, or patient safety breach.
- **Architectural Defense-in-Depth:**
  - Multi-tier redundancy: local client IndexedDB caching, automated Fastify retry queues, dual-SIM cellular failover, and line-interactive UPS holdover.
  - Complete decoupling of offline clinical workflows from central cloud database availability.
- **Accountable Executive Lead:** [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) with reporting line directly to the Special Commissioner (Health).
- **Continuous Verification Cadence:** Monitored daily in automated Prometheus dashboards and reviewed weekly at CCB meetings.

### 5.10 Critical Risk Review: RISK-010 — Critical Hemoglobin (<7.0 g/dL) Panic Value Delivery Failure
- **Risk Exposure Score:** `16/25` (`CRITICAL`) | **Category:** `Clinical`
- **Primary Threat Vector:** Lab result marked in lab desk but doctor has already discharged patient leading to Severe anemic patient sent home without immediate transfusion.
- **Worst-Case Catastrophic Impact:** Complete stoppage of primary outpatient care across multiple wards, severe data loss, or patient safety breach.
- **Architectural Defense-in-Depth:**
  - Multi-tier redundancy: local client IndexedDB caching, automated Fastify retry queues, dual-SIM cellular failover, and line-interactive UPS holdover.
  - Complete decoupling of offline clinical workflows from central cloud database availability.
- **Accountable Executive Lead:** [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) with reporting line directly to the Special Commissioner (Health).
- **Continuous Verification Cadence:** Monitored daily in automated Prometheus dashboards and reviewed weekly at CCB meetings.

## 6. Zonal Risk Profiling Across 8 BBMP Administrative Zones
Localized risk profiles and specific field vulnerabilities mapped across Bangalore's municipal zones:

| Administrative Zone | Clinic Count | Dominant Risk Category | Top Local Threat | Primary Mitigating Infrastructure | Local Escalation SLA |
| :--- | :---: | :--- | :--- | :--- | :---: |
| **East Zone** | `28` | `Network & Queue` | Fiber cuts during road works causing network disconnect; extreme morning footfall surges. | Dual-SIM 4G router failover + local IndexedDB queue token engine. | `< 2 Hours` |
| **West Zone** | `32` | `Clinical & Pharmacy` | Chronic disease medication stockouts; geriatric consultation UI friction. | Closed-loop FEFO perpetual inventory + high-contrast bilingual Kannada UI. | `< 2 Hours` |
| **South Zone** | `30` | `Hardware & Cold Chain` | Vaccine storage ILR temperature fluctuations during electrical load shedding. | IoT temperature telemetry logger + 1000VA UPS backup holdover. | `< 2 Hours` |
| **Bommanahalli Zone** | `22` | `Operational Footfall` | Industrial garment worker surges between 08:30 and 10:00 overwhelming single doctor. | Multi-counter triage tokens + mobile nurse vital intake station. | `< 2 Hours` |
| **Dasarahalli Zone** | `18` | `Electrical Infrastructure` | Industrial power grid voltage spikes damaging mini-PC power supplies. | Heavy-duty voltage stabilizer + isolated ground circuit in clinic mini-PCs. | `< 2 Hours` |
| **Mahadevapura Zone** | `24` | `Epidemiological` | High seasonal dengue / waterborne fever clusters overwhelming diagnostic kits. | DuckDB syndromic surveillance query triggers automated depot restock. | `< 2 Hours` |
| **RR Nagar Zone** | `16` | `Logistical Referral` | Transport distance to secondary referral hospitals during acute emergencies. | Encrypted digital referral QR slip + ambulance direct dispatch integration. | `< 2 Hours` |
| **Yelahanka Zone** | `13` | `Geographic Dispersal` | Peripheral travel distance for zonal field support technicians during hardware failure. | Depot spare mini-PCs and pre-configured printers held at Zonal Health Office. | `< 2 Hours` |

## 7. Comprehensive Cross-Document Traceability Matrix
Bidirectional relational mapping linking all 100 Risks to Roles, Dependencies, Milestones, Releases, Assumptions, and Constraints:

| Risk ID | Accountable Role | Bound Dependency | Target Milestone | Software Release | Linked Assumption | Governing Constraint |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [`RISK-001`](#risk-001) | [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) | [`DEPENDENCY-001`](./13-project-dependencies.md#dependency-001) | [`MILESTONE-001`](./14-project-milestones.md#milestone-001) | [`RELEASE-001`](./15-release-strategy.md#release-001) | [`ASSUMPTION-001`](./10-project-assumptions.md#assumption-001) | [`CONSTRAINT-001`](./11-project-constraints.md#constraint-001) |
| [`RISK-002`](#risk-002) | [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) | [`DEPENDENCY-002`](./13-project-dependencies.md#dependency-002) | [`MILESTONE-002`](./14-project-milestones.md#milestone-002) | [`RELEASE-002`](./15-release-strategy.md#release-002) | [`ASSUMPTION-002`](./10-project-assumptions.md#assumption-002) | [`CONSTRAINT-002`](./11-project-constraints.md#constraint-002) |
| [`RISK-003`](#risk-003) | [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) | [`DEPENDENCY-003`](./13-project-dependencies.md#dependency-003) | [`MILESTONE-003`](./14-project-milestones.md#milestone-003) | [`RELEASE-003`](./15-release-strategy.md#release-003) | [`ASSUMPTION-003`](./10-project-assumptions.md#assumption-003) | [`CONSTRAINT-003`](./11-project-constraints.md#constraint-003) |
| [`RISK-004`](#risk-004) | [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) | [`DEPENDENCY-004`](./13-project-dependencies.md#dependency-004) | [`MILESTONE-004`](./14-project-milestones.md#milestone-004) | [`RELEASE-004`](./15-release-strategy.md#release-004) | [`ASSUMPTION-004`](./10-project-assumptions.md#assumption-004) | [`CONSTRAINT-004`](./11-project-constraints.md#constraint-004) |
| [`RISK-005`](#risk-005) | [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) | [`DEPENDENCY-005`](./13-project-dependencies.md#dependency-005) | [`MILESTONE-005`](./14-project-milestones.md#milestone-005) | [`RELEASE-005`](./15-release-strategy.md#release-005) | [`ASSUMPTION-005`](./10-project-assumptions.md#assumption-005) | [`CONSTRAINT-005`](./11-project-constraints.md#constraint-005) |
| [`RISK-006`](#risk-006) | [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) | [`DEPENDENCY-006`](./13-project-dependencies.md#dependency-006) | [`MILESTONE-006`](./14-project-milestones.md#milestone-006) | [`RELEASE-006`](./15-release-strategy.md#release-006) | [`ASSUMPTION-006`](./10-project-assumptions.md#assumption-006) | [`CONSTRAINT-006`](./11-project-constraints.md#constraint-006) |
| [`RISK-007`](#risk-007) | [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) | [`DEPENDENCY-007`](./13-project-dependencies.md#dependency-007) | [`MILESTONE-007`](./14-project-milestones.md#milestone-007) | [`RELEASE-007`](./15-release-strategy.md#release-007) | [`ASSUMPTION-007`](./10-project-assumptions.md#assumption-007) | [`CONSTRAINT-007`](./11-project-constraints.md#constraint-007) |
| [`RISK-008`](#risk-008) | [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) | [`DEPENDENCY-008`](./13-project-dependencies.md#dependency-008) | [`MILESTONE-008`](./14-project-milestones.md#milestone-008) | [`RELEASE-008`](./15-release-strategy.md#release-008) | [`ASSUMPTION-008`](./10-project-assumptions.md#assumption-008) | [`CONSTRAINT-008`](./11-project-constraints.md#constraint-008) |
| [`RISK-009`](#risk-009) | [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) | [`DEPENDENCY-009`](./13-project-dependencies.md#dependency-009) | [`MILESTONE-009`](./14-project-milestones.md#milestone-009) | [`RELEASE-009`](./15-release-strategy.md#release-009) | [`ASSUMPTION-009`](./10-project-assumptions.md#assumption-009) | [`CONSTRAINT-009`](./11-project-constraints.md#constraint-009) |
| [`RISK-010`](#risk-010) | [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) | [`DEPENDENCY-010`](./13-project-dependencies.md#dependency-010) | [`MILESTONE-010`](./14-project-milestones.md#milestone-010) | [`RELEASE-010`](./15-release-strategy.md#release-010) | [`ASSUMPTION-010`](./10-project-assumptions.md#assumption-010) | [`CONSTRAINT-010`](./11-project-constraints.md#constraint-010) |
| [`RISK-011`](#risk-011) | [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) | [`DEPENDENCY-011`](./13-project-dependencies.md#dependency-011) | [`MILESTONE-011`](./14-project-milestones.md#milestone-011) | [`RELEASE-011`](./15-release-strategy.md#release-011) | [`ASSUMPTION-011`](./10-project-assumptions.md#assumption-011) | [`CONSTRAINT-011`](./11-project-constraints.md#constraint-011) |
| [`RISK-012`](#risk-012) | [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) | [`DEPENDENCY-012`](./13-project-dependencies.md#dependency-012) | [`MILESTONE-012`](./14-project-milestones.md#milestone-012) | [`RELEASE-012`](./15-release-strategy.md#release-012) | [`ASSUMPTION-012`](./10-project-assumptions.md#assumption-012) | [`CONSTRAINT-012`](./11-project-constraints.md#constraint-012) |
| [`RISK-013`](#risk-013) | [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) | [`DEPENDENCY-013`](./13-project-dependencies.md#dependency-013) | [`MILESTONE-013`](./14-project-milestones.md#milestone-013) | [`RELEASE-013`](./15-release-strategy.md#release-013) | [`ASSUMPTION-013`](./10-project-assumptions.md#assumption-013) | [`CONSTRAINT-013`](./11-project-constraints.md#constraint-013) |
| [`RISK-014`](#risk-014) | [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) | [`DEPENDENCY-014`](./13-project-dependencies.md#dependency-014) | [`MILESTONE-014`](./14-project-milestones.md#milestone-014) | [`RELEASE-014`](./15-release-strategy.md#release-014) | [`ASSUMPTION-014`](./10-project-assumptions.md#assumption-014) | [`CONSTRAINT-014`](./11-project-constraints.md#constraint-014) |
| [`RISK-015`](#risk-015) | [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) | [`DEPENDENCY-015`](./13-project-dependencies.md#dependency-015) | [`MILESTONE-015`](./14-project-milestones.md#milestone-015) | [`RELEASE-015`](./15-release-strategy.md#release-015) | [`ASSUMPTION-015`](./10-project-assumptions.md#assumption-015) | [`CONSTRAINT-015`](./11-project-constraints.md#constraint-015) |
| [`RISK-016`](#risk-016) | [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) | [`DEPENDENCY-016`](./13-project-dependencies.md#dependency-016) | [`MILESTONE-016`](./14-project-milestones.md#milestone-016) | [`RELEASE-016`](./15-release-strategy.md#release-016) | [`ASSUMPTION-016`](./10-project-assumptions.md#assumption-016) | [`CONSTRAINT-016`](./11-project-constraints.md#constraint-016) |
| [`RISK-017`](#risk-017) | [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) | [`DEPENDENCY-017`](./13-project-dependencies.md#dependency-017) | [`MILESTONE-017`](./14-project-milestones.md#milestone-017) | [`RELEASE-017`](./15-release-strategy.md#release-017) | [`ASSUMPTION-017`](./10-project-assumptions.md#assumption-017) | [`CONSTRAINT-017`](./11-project-constraints.md#constraint-017) |
| [`RISK-018`](#risk-018) | [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) | [`DEPENDENCY-018`](./13-project-dependencies.md#dependency-018) | [`MILESTONE-018`](./14-project-milestones.md#milestone-018) | [`RELEASE-018`](./15-release-strategy.md#release-018) | [`ASSUMPTION-018`](./10-project-assumptions.md#assumption-018) | [`CONSTRAINT-018`](./11-project-constraints.md#constraint-018) |
| [`RISK-019`](#risk-019) | [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) | [`DEPENDENCY-019`](./13-project-dependencies.md#dependency-019) | [`MILESTONE-019`](./14-project-milestones.md#milestone-019) | [`RELEASE-019`](./15-release-strategy.md#release-019) | [`ASSUMPTION-019`](./10-project-assumptions.md#assumption-019) | [`CONSTRAINT-019`](./11-project-constraints.md#constraint-019) |
| [`RISK-020`](#risk-020) | [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) | [`DEPENDENCY-020`](./13-project-dependencies.md#dependency-020) | [`MILESTONE-020`](./14-project-milestones.md#milestone-020) | [`RELEASE-020`](./15-release-strategy.md#release-020) | [`ASSUMPTION-020`](./10-project-assumptions.md#assumption-020) | [`CONSTRAINT-020`](./11-project-constraints.md#constraint-020) |
| [`RISK-021`](#risk-021) | [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) | [`DEPENDENCY-021`](./13-project-dependencies.md#dependency-021) | [`MILESTONE-021`](./14-project-milestones.md#milestone-021) | [`RELEASE-021`](./15-release-strategy.md#release-021) | [`ASSUMPTION-021`](./10-project-assumptions.md#assumption-021) | [`CONSTRAINT-021`](./11-project-constraints.md#constraint-021) |
| [`RISK-022`](#risk-022) | [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) | [`DEPENDENCY-022`](./13-project-dependencies.md#dependency-022) | [`MILESTONE-022`](./14-project-milestones.md#milestone-022) | [`RELEASE-022`](./15-release-strategy.md#release-022) | [`ASSUMPTION-022`](./10-project-assumptions.md#assumption-022) | [`CONSTRAINT-022`](./11-project-constraints.md#constraint-022) |
| [`RISK-023`](#risk-023) | [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) | [`DEPENDENCY-023`](./13-project-dependencies.md#dependency-023) | [`MILESTONE-023`](./14-project-milestones.md#milestone-023) | [`RELEASE-023`](./15-release-strategy.md#release-023) | [`ASSUMPTION-023`](./10-project-assumptions.md#assumption-023) | [`CONSTRAINT-023`](./11-project-constraints.md#constraint-023) |
| [`RISK-024`](#risk-024) | [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) | [`DEPENDENCY-024`](./13-project-dependencies.md#dependency-024) | [`MILESTONE-024`](./14-project-milestones.md#milestone-024) | [`RELEASE-024`](./15-release-strategy.md#release-024) | [`ASSUMPTION-024`](./10-project-assumptions.md#assumption-024) | [`CONSTRAINT-024`](./11-project-constraints.md#constraint-024) |
| [`RISK-025`](#risk-025) | [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) | [`DEPENDENCY-025`](./13-project-dependencies.md#dependency-025) | [`MILESTONE-025`](./14-project-milestones.md#milestone-025) | [`RELEASE-025`](./15-release-strategy.md#release-025) | [`ASSUMPTION-025`](./10-project-assumptions.md#assumption-025) | [`CONSTRAINT-025`](./11-project-constraints.md#constraint-025) |
| [`RISK-026`](#risk-026) | [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) | [`DEPENDENCY-026`](./13-project-dependencies.md#dependency-026) | [`MILESTONE-026`](./14-project-milestones.md#milestone-026) | [`RELEASE-001`](./15-release-strategy.md#release-001) | [`ASSUMPTION-026`](./10-project-assumptions.md#assumption-026) | [`CONSTRAINT-026`](./11-project-constraints.md#constraint-026) |
| [`RISK-027`](#risk-027) | [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) | [`DEPENDENCY-027`](./13-project-dependencies.md#dependency-027) | [`MILESTONE-027`](./14-project-milestones.md#milestone-027) | [`RELEASE-002`](./15-release-strategy.md#release-002) | [`ASSUMPTION-027`](./10-project-assumptions.md#assumption-027) | [`CONSTRAINT-027`](./11-project-constraints.md#constraint-027) |
| [`RISK-028`](#risk-028) | [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) | [`DEPENDENCY-028`](./13-project-dependencies.md#dependency-028) | [`MILESTONE-028`](./14-project-milestones.md#milestone-028) | [`RELEASE-003`](./15-release-strategy.md#release-003) | [`ASSUMPTION-028`](./10-project-assumptions.md#assumption-028) | [`CONSTRAINT-028`](./11-project-constraints.md#constraint-028) |
| [`RISK-029`](#risk-029) | [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) | [`DEPENDENCY-029`](./13-project-dependencies.md#dependency-029) | [`MILESTONE-029`](./14-project-milestones.md#milestone-029) | [`RELEASE-004`](./15-release-strategy.md#release-004) | [`ASSUMPTION-029`](./10-project-assumptions.md#assumption-029) | [`CONSTRAINT-029`](./11-project-constraints.md#constraint-029) |
| [`RISK-030`](#risk-030) | [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) | [`DEPENDENCY-030`](./13-project-dependencies.md#dependency-030) | [`MILESTONE-030`](./14-project-milestones.md#milestone-030) | [`RELEASE-005`](./15-release-strategy.md#release-005) | [`ASSUMPTION-030`](./10-project-assumptions.md#assumption-030) | [`CONSTRAINT-030`](./11-project-constraints.md#constraint-030) |
| [`RISK-031`](#risk-031) | [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) | [`DEPENDENCY-031`](./13-project-dependencies.md#dependency-031) | [`MILESTONE-031`](./14-project-milestones.md#milestone-031) | [`RELEASE-006`](./15-release-strategy.md#release-006) | [`ASSUMPTION-031`](./10-project-assumptions.md#assumption-031) | [`CONSTRAINT-031`](./11-project-constraints.md#constraint-031) |
| [`RISK-032`](#risk-032) | [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) | [`DEPENDENCY-032`](./13-project-dependencies.md#dependency-032) | [`MILESTONE-032`](./14-project-milestones.md#milestone-032) | [`RELEASE-007`](./15-release-strategy.md#release-007) | [`ASSUMPTION-032`](./10-project-assumptions.md#assumption-032) | [`CONSTRAINT-032`](./11-project-constraints.md#constraint-032) |
| [`RISK-033`](#risk-033) | [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) | [`DEPENDENCY-033`](./13-project-dependencies.md#dependency-033) | [`MILESTONE-033`](./14-project-milestones.md#milestone-033) | [`RELEASE-008`](./15-release-strategy.md#release-008) | [`ASSUMPTION-033`](./10-project-assumptions.md#assumption-033) | [`CONSTRAINT-033`](./11-project-constraints.md#constraint-033) |
| [`RISK-034`](#risk-034) | [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) | [`DEPENDENCY-034`](./13-project-dependencies.md#dependency-034) | [`MILESTONE-034`](./14-project-milestones.md#milestone-034) | [`RELEASE-009`](./15-release-strategy.md#release-009) | [`ASSUMPTION-034`](./10-project-assumptions.md#assumption-034) | [`CONSTRAINT-034`](./11-project-constraints.md#constraint-034) |
| [`RISK-035`](#risk-035) | [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) | [`DEPENDENCY-035`](./13-project-dependencies.md#dependency-035) | [`MILESTONE-035`](./14-project-milestones.md#milestone-035) | [`RELEASE-010`](./15-release-strategy.md#release-010) | [`ASSUMPTION-035`](./10-project-assumptions.md#assumption-035) | [`CONSTRAINT-035`](./11-project-constraints.md#constraint-035) |
| [`RISK-036`](#risk-036) | [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) | [`DEPENDENCY-036`](./13-project-dependencies.md#dependency-036) | [`MILESTONE-036`](./14-project-milestones.md#milestone-036) | [`RELEASE-011`](./15-release-strategy.md#release-011) | [`ASSUMPTION-036`](./10-project-assumptions.md#assumption-036) | [`CONSTRAINT-036`](./11-project-constraints.md#constraint-036) |
| [`RISK-037`](#risk-037) | [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) | [`DEPENDENCY-037`](./13-project-dependencies.md#dependency-037) | [`MILESTONE-037`](./14-project-milestones.md#milestone-037) | [`RELEASE-012`](./15-release-strategy.md#release-012) | [`ASSUMPTION-037`](./10-project-assumptions.md#assumption-037) | [`CONSTRAINT-037`](./11-project-constraints.md#constraint-037) |
| [`RISK-038`](#risk-038) | [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) | [`DEPENDENCY-038`](./13-project-dependencies.md#dependency-038) | [`MILESTONE-038`](./14-project-milestones.md#milestone-038) | [`RELEASE-013`](./15-release-strategy.md#release-013) | [`ASSUMPTION-038`](./10-project-assumptions.md#assumption-038) | [`CONSTRAINT-038`](./11-project-constraints.md#constraint-038) |
| [`RISK-039`](#risk-039) | [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) | [`DEPENDENCY-039`](./13-project-dependencies.md#dependency-039) | [`MILESTONE-039`](./14-project-milestones.md#milestone-039) | [`RELEASE-014`](./15-release-strategy.md#release-014) | [`ASSUMPTION-039`](./10-project-assumptions.md#assumption-039) | [`CONSTRAINT-039`](./11-project-constraints.md#constraint-039) |
| [`RISK-040`](#risk-040) | [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) | [`DEPENDENCY-040`](./13-project-dependencies.md#dependency-040) | [`MILESTONE-040`](./14-project-milestones.md#milestone-040) | [`RELEASE-015`](./15-release-strategy.md#release-015) | [`ASSUMPTION-040`](./10-project-assumptions.md#assumption-040) | [`CONSTRAINT-040`](./11-project-constraints.md#constraint-040) |
| [`RISK-041`](#risk-041) | [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) | [`DEPENDENCY-041`](./13-project-dependencies.md#dependency-041) | [`MILESTONE-001`](./14-project-milestones.md#milestone-001) | [`RELEASE-016`](./15-release-strategy.md#release-016) | [`ASSUMPTION-041`](./10-project-assumptions.md#assumption-041) | [`CONSTRAINT-041`](./11-project-constraints.md#constraint-041) |
| [`RISK-042`](#risk-042) | [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) | [`DEPENDENCY-042`](./13-project-dependencies.md#dependency-042) | [`MILESTONE-002`](./14-project-milestones.md#milestone-002) | [`RELEASE-017`](./15-release-strategy.md#release-017) | [`ASSUMPTION-042`](./10-project-assumptions.md#assumption-042) | [`CONSTRAINT-042`](./11-project-constraints.md#constraint-042) |
| [`RISK-043`](#risk-043) | [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) | [`DEPENDENCY-043`](./13-project-dependencies.md#dependency-043) | [`MILESTONE-003`](./14-project-milestones.md#milestone-003) | [`RELEASE-018`](./15-release-strategy.md#release-018) | [`ASSUMPTION-043`](./10-project-assumptions.md#assumption-043) | [`CONSTRAINT-043`](./11-project-constraints.md#constraint-043) |
| [`RISK-044`](#risk-044) | [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) | [`DEPENDENCY-044`](./13-project-dependencies.md#dependency-044) | [`MILESTONE-004`](./14-project-milestones.md#milestone-004) | [`RELEASE-019`](./15-release-strategy.md#release-019) | [`ASSUMPTION-044`](./10-project-assumptions.md#assumption-044) | [`CONSTRAINT-044`](./11-project-constraints.md#constraint-044) |
| [`RISK-045`](#risk-045) | [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) | [`DEPENDENCY-045`](./13-project-dependencies.md#dependency-045) | [`MILESTONE-005`](./14-project-milestones.md#milestone-005) | [`RELEASE-020`](./15-release-strategy.md#release-020) | [`ASSUMPTION-045`](./10-project-assumptions.md#assumption-045) | [`CONSTRAINT-045`](./11-project-constraints.md#constraint-045) |
| [`RISK-046`](#risk-046) | [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) | [`DEPENDENCY-046`](./13-project-dependencies.md#dependency-046) | [`MILESTONE-006`](./14-project-milestones.md#milestone-006) | [`RELEASE-021`](./15-release-strategy.md#release-021) | [`ASSUMPTION-046`](./10-project-assumptions.md#assumption-046) | [`CONSTRAINT-046`](./11-project-constraints.md#constraint-046) |
| [`RISK-047`](#risk-047) | [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) | [`DEPENDENCY-047`](./13-project-dependencies.md#dependency-047) | [`MILESTONE-007`](./14-project-milestones.md#milestone-007) | [`RELEASE-022`](./15-release-strategy.md#release-022) | [`ASSUMPTION-047`](./10-project-assumptions.md#assumption-047) | [`CONSTRAINT-047`](./11-project-constraints.md#constraint-047) |
| [`RISK-048`](#risk-048) | [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) | [`DEPENDENCY-048`](./13-project-dependencies.md#dependency-048) | [`MILESTONE-008`](./14-project-milestones.md#milestone-008) | [`RELEASE-023`](./15-release-strategy.md#release-023) | [`ASSUMPTION-048`](./10-project-assumptions.md#assumption-048) | [`CONSTRAINT-048`](./11-project-constraints.md#constraint-048) |
| [`RISK-049`](#risk-049) | [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) | [`DEPENDENCY-049`](./13-project-dependencies.md#dependency-049) | [`MILESTONE-009`](./14-project-milestones.md#milestone-009) | [`RELEASE-024`](./15-release-strategy.md#release-024) | [`ASSUMPTION-049`](./10-project-assumptions.md#assumption-049) | [`CONSTRAINT-049`](./11-project-constraints.md#constraint-049) |
| [`RISK-050`](#risk-050) | [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) | [`DEPENDENCY-050`](./13-project-dependencies.md#dependency-050) | [`MILESTONE-010`](./14-project-milestones.md#milestone-010) | [`RELEASE-025`](./15-release-strategy.md#release-025) | [`ASSUMPTION-050`](./10-project-assumptions.md#assumption-050) | [`CONSTRAINT-050`](./11-project-constraints.md#constraint-050) |
| [`RISK-051`](#risk-051) | [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) | [`DEPENDENCY-051`](./13-project-dependencies.md#dependency-051) | [`MILESTONE-011`](./14-project-milestones.md#milestone-011) | [`RELEASE-001`](./15-release-strategy.md#release-001) | [`ASSUMPTION-001`](./10-project-assumptions.md#assumption-001) | [`CONSTRAINT-001`](./11-project-constraints.md#constraint-001) |
| [`RISK-052`](#risk-052) | [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) | [`DEPENDENCY-052`](./13-project-dependencies.md#dependency-052) | [`MILESTONE-012`](./14-project-milestones.md#milestone-012) | [`RELEASE-002`](./15-release-strategy.md#release-002) | [`ASSUMPTION-002`](./10-project-assumptions.md#assumption-002) | [`CONSTRAINT-002`](./11-project-constraints.md#constraint-002) |
| [`RISK-053`](#risk-053) | [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) | [`DEPENDENCY-053`](./13-project-dependencies.md#dependency-053) | [`MILESTONE-013`](./14-project-milestones.md#milestone-013) | [`RELEASE-003`](./15-release-strategy.md#release-003) | [`ASSUMPTION-003`](./10-project-assumptions.md#assumption-003) | [`CONSTRAINT-003`](./11-project-constraints.md#constraint-003) |
| [`RISK-054`](#risk-054) | [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) | [`DEPENDENCY-054`](./13-project-dependencies.md#dependency-054) | [`MILESTONE-014`](./14-project-milestones.md#milestone-014) | [`RELEASE-004`](./15-release-strategy.md#release-004) | [`ASSUMPTION-004`](./10-project-assumptions.md#assumption-004) | [`CONSTRAINT-004`](./11-project-constraints.md#constraint-004) |
| [`RISK-055`](#risk-055) | [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) | [`DEPENDENCY-055`](./13-project-dependencies.md#dependency-055) | [`MILESTONE-015`](./14-project-milestones.md#milestone-015) | [`RELEASE-005`](./15-release-strategy.md#release-005) | [`ASSUMPTION-005`](./10-project-assumptions.md#assumption-005) | [`CONSTRAINT-005`](./11-project-constraints.md#constraint-005) |
| [`RISK-056`](#risk-056) | [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) | [`DEPENDENCY-056`](./13-project-dependencies.md#dependency-056) | [`MILESTONE-016`](./14-project-milestones.md#milestone-016) | [`RELEASE-006`](./15-release-strategy.md#release-006) | [`ASSUMPTION-006`](./10-project-assumptions.md#assumption-006) | [`CONSTRAINT-006`](./11-project-constraints.md#constraint-006) |
| [`RISK-057`](#risk-057) | [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) | [`DEPENDENCY-057`](./13-project-dependencies.md#dependency-057) | [`MILESTONE-017`](./14-project-milestones.md#milestone-017) | [`RELEASE-007`](./15-release-strategy.md#release-007) | [`ASSUMPTION-007`](./10-project-assumptions.md#assumption-007) | [`CONSTRAINT-007`](./11-project-constraints.md#constraint-007) |
| [`RISK-058`](#risk-058) | [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) | [`DEPENDENCY-058`](./13-project-dependencies.md#dependency-058) | [`MILESTONE-018`](./14-project-milestones.md#milestone-018) | [`RELEASE-008`](./15-release-strategy.md#release-008) | [`ASSUMPTION-008`](./10-project-assumptions.md#assumption-008) | [`CONSTRAINT-008`](./11-project-constraints.md#constraint-008) |
| [`RISK-059`](#risk-059) | [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) | [`DEPENDENCY-059`](./13-project-dependencies.md#dependency-059) | [`MILESTONE-019`](./14-project-milestones.md#milestone-019) | [`RELEASE-009`](./15-release-strategy.md#release-009) | [`ASSUMPTION-009`](./10-project-assumptions.md#assumption-009) | [`CONSTRAINT-009`](./11-project-constraints.md#constraint-009) |
| [`RISK-060`](#risk-060) | [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) | [`DEPENDENCY-060`](./13-project-dependencies.md#dependency-060) | [`MILESTONE-020`](./14-project-milestones.md#milestone-020) | [`RELEASE-010`](./15-release-strategy.md#release-010) | [`ASSUMPTION-010`](./10-project-assumptions.md#assumption-010) | [`CONSTRAINT-010`](./11-project-constraints.md#constraint-010) |
| [`RISK-061`](#risk-061) | [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) | [`DEPENDENCY-061`](./13-project-dependencies.md#dependency-061) | [`MILESTONE-021`](./14-project-milestones.md#milestone-021) | [`RELEASE-011`](./15-release-strategy.md#release-011) | [`ASSUMPTION-011`](./10-project-assumptions.md#assumption-011) | [`CONSTRAINT-011`](./11-project-constraints.md#constraint-011) |
| [`RISK-062`](#risk-062) | [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) | [`DEPENDENCY-062`](./13-project-dependencies.md#dependency-062) | [`MILESTONE-022`](./14-project-milestones.md#milestone-022) | [`RELEASE-012`](./15-release-strategy.md#release-012) | [`ASSUMPTION-012`](./10-project-assumptions.md#assumption-012) | [`CONSTRAINT-012`](./11-project-constraints.md#constraint-012) |
| [`RISK-063`](#risk-063) | [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) | [`DEPENDENCY-063`](./13-project-dependencies.md#dependency-063) | [`MILESTONE-023`](./14-project-milestones.md#milestone-023) | [`RELEASE-013`](./15-release-strategy.md#release-013) | [`ASSUMPTION-013`](./10-project-assumptions.md#assumption-013) | [`CONSTRAINT-013`](./11-project-constraints.md#constraint-013) |
| [`RISK-064`](#risk-064) | [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) | [`DEPENDENCY-064`](./13-project-dependencies.md#dependency-064) | [`MILESTONE-024`](./14-project-milestones.md#milestone-024) | [`RELEASE-014`](./15-release-strategy.md#release-014) | [`ASSUMPTION-014`](./10-project-assumptions.md#assumption-014) | [`CONSTRAINT-014`](./11-project-constraints.md#constraint-014) |
| [`RISK-065`](#risk-065) | [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) | [`DEPENDENCY-065`](./13-project-dependencies.md#dependency-065) | [`MILESTONE-025`](./14-project-milestones.md#milestone-025) | [`RELEASE-015`](./15-release-strategy.md#release-015) | [`ASSUMPTION-015`](./10-project-assumptions.md#assumption-015) | [`CONSTRAINT-015`](./11-project-constraints.md#constraint-015) |
| [`RISK-066`](#risk-066) | [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) | [`DEPENDENCY-066`](./13-project-dependencies.md#dependency-066) | [`MILESTONE-026`](./14-project-milestones.md#milestone-026) | [`RELEASE-016`](./15-release-strategy.md#release-016) | [`ASSUMPTION-016`](./10-project-assumptions.md#assumption-016) | [`CONSTRAINT-016`](./11-project-constraints.md#constraint-016) |
| [`RISK-067`](#risk-067) | [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) | [`DEPENDENCY-067`](./13-project-dependencies.md#dependency-067) | [`MILESTONE-027`](./14-project-milestones.md#milestone-027) | [`RELEASE-017`](./15-release-strategy.md#release-017) | [`ASSUMPTION-017`](./10-project-assumptions.md#assumption-017) | [`CONSTRAINT-017`](./11-project-constraints.md#constraint-017) |
| [`RISK-068`](#risk-068) | [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) | [`DEPENDENCY-068`](./13-project-dependencies.md#dependency-068) | [`MILESTONE-028`](./14-project-milestones.md#milestone-028) | [`RELEASE-018`](./15-release-strategy.md#release-018) | [`ASSUMPTION-018`](./10-project-assumptions.md#assumption-018) | [`CONSTRAINT-018`](./11-project-constraints.md#constraint-018) |
| [`RISK-069`](#risk-069) | [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) | [`DEPENDENCY-069`](./13-project-dependencies.md#dependency-069) | [`MILESTONE-029`](./14-project-milestones.md#milestone-029) | [`RELEASE-019`](./15-release-strategy.md#release-019) | [`ASSUMPTION-019`](./10-project-assumptions.md#assumption-019) | [`CONSTRAINT-019`](./11-project-constraints.md#constraint-019) |
| [`RISK-070`](#risk-070) | [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) | [`DEPENDENCY-070`](./13-project-dependencies.md#dependency-070) | [`MILESTONE-030`](./14-project-milestones.md#milestone-030) | [`RELEASE-020`](./15-release-strategy.md#release-020) | [`ASSUMPTION-020`](./10-project-assumptions.md#assumption-020) | [`CONSTRAINT-020`](./11-project-constraints.md#constraint-020) |
| [`RISK-071`](#risk-071) | [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) | [`DEPENDENCY-071`](./13-project-dependencies.md#dependency-071) | [`MILESTONE-031`](./14-project-milestones.md#milestone-031) | [`RELEASE-021`](./15-release-strategy.md#release-021) | [`ASSUMPTION-021`](./10-project-assumptions.md#assumption-021) | [`CONSTRAINT-021`](./11-project-constraints.md#constraint-021) |
| [`RISK-072`](#risk-072) | [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) | [`DEPENDENCY-072`](./13-project-dependencies.md#dependency-072) | [`MILESTONE-032`](./14-project-milestones.md#milestone-032) | [`RELEASE-022`](./15-release-strategy.md#release-022) | [`ASSUMPTION-022`](./10-project-assumptions.md#assumption-022) | [`CONSTRAINT-022`](./11-project-constraints.md#constraint-022) |
| [`RISK-073`](#risk-073) | [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) | [`DEPENDENCY-073`](./13-project-dependencies.md#dependency-073) | [`MILESTONE-033`](./14-project-milestones.md#milestone-033) | [`RELEASE-023`](./15-release-strategy.md#release-023) | [`ASSUMPTION-023`](./10-project-assumptions.md#assumption-023) | [`CONSTRAINT-023`](./11-project-constraints.md#constraint-023) |
| [`RISK-074`](#risk-074) | [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) | [`DEPENDENCY-074`](./13-project-dependencies.md#dependency-074) | [`MILESTONE-034`](./14-project-milestones.md#milestone-034) | [`RELEASE-024`](./15-release-strategy.md#release-024) | [`ASSUMPTION-024`](./10-project-assumptions.md#assumption-024) | [`CONSTRAINT-024`](./11-project-constraints.md#constraint-024) |
| [`RISK-075`](#risk-075) | [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) | [`DEPENDENCY-075`](./13-project-dependencies.md#dependency-075) | [`MILESTONE-035`](./14-project-milestones.md#milestone-035) | [`RELEASE-025`](./15-release-strategy.md#release-025) | [`ASSUMPTION-025`](./10-project-assumptions.md#assumption-025) | [`CONSTRAINT-025`](./11-project-constraints.md#constraint-025) |
| [`RISK-076`](#risk-076) | [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) | [`DEPENDENCY-001`](./13-project-dependencies.md#dependency-001) | [`MILESTONE-036`](./14-project-milestones.md#milestone-036) | [`RELEASE-001`](./15-release-strategy.md#release-001) | [`ASSUMPTION-026`](./10-project-assumptions.md#assumption-026) | [`CONSTRAINT-026`](./11-project-constraints.md#constraint-026) |
| [`RISK-077`](#risk-077) | [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) | [`DEPENDENCY-002`](./13-project-dependencies.md#dependency-002) | [`MILESTONE-037`](./14-project-milestones.md#milestone-037) | [`RELEASE-002`](./15-release-strategy.md#release-002) | [`ASSUMPTION-027`](./10-project-assumptions.md#assumption-027) | [`CONSTRAINT-027`](./11-project-constraints.md#constraint-027) |
| [`RISK-078`](#risk-078) | [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) | [`DEPENDENCY-003`](./13-project-dependencies.md#dependency-003) | [`MILESTONE-038`](./14-project-milestones.md#milestone-038) | [`RELEASE-003`](./15-release-strategy.md#release-003) | [`ASSUMPTION-028`](./10-project-assumptions.md#assumption-028) | [`CONSTRAINT-028`](./11-project-constraints.md#constraint-028) |
| [`RISK-079`](#risk-079) | [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) | [`DEPENDENCY-004`](./13-project-dependencies.md#dependency-004) | [`MILESTONE-039`](./14-project-milestones.md#milestone-039) | [`RELEASE-004`](./15-release-strategy.md#release-004) | [`ASSUMPTION-029`](./10-project-assumptions.md#assumption-029) | [`CONSTRAINT-029`](./11-project-constraints.md#constraint-029) |
| [`RISK-080`](#risk-080) | [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) | [`DEPENDENCY-005`](./13-project-dependencies.md#dependency-005) | [`MILESTONE-040`](./14-project-milestones.md#milestone-040) | [`RELEASE-005`](./15-release-strategy.md#release-005) | [`ASSUMPTION-030`](./10-project-assumptions.md#assumption-030) | [`CONSTRAINT-030`](./11-project-constraints.md#constraint-030) |
| [`RISK-081`](#risk-081) | [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) | [`DEPENDENCY-006`](./13-project-dependencies.md#dependency-006) | [`MILESTONE-001`](./14-project-milestones.md#milestone-001) | [`RELEASE-006`](./15-release-strategy.md#release-006) | [`ASSUMPTION-031`](./10-project-assumptions.md#assumption-031) | [`CONSTRAINT-031`](./11-project-constraints.md#constraint-031) |
| [`RISK-082`](#risk-082) | [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) | [`DEPENDENCY-007`](./13-project-dependencies.md#dependency-007) | [`MILESTONE-002`](./14-project-milestones.md#milestone-002) | [`RELEASE-007`](./15-release-strategy.md#release-007) | [`ASSUMPTION-032`](./10-project-assumptions.md#assumption-032) | [`CONSTRAINT-032`](./11-project-constraints.md#constraint-032) |
| [`RISK-083`](#risk-083) | [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) | [`DEPENDENCY-008`](./13-project-dependencies.md#dependency-008) | [`MILESTONE-003`](./14-project-milestones.md#milestone-003) | [`RELEASE-008`](./15-release-strategy.md#release-008) | [`ASSUMPTION-033`](./10-project-assumptions.md#assumption-033) | [`CONSTRAINT-033`](./11-project-constraints.md#constraint-033) |
| [`RISK-084`](#risk-084) | [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) | [`DEPENDENCY-009`](./13-project-dependencies.md#dependency-009) | [`MILESTONE-004`](./14-project-milestones.md#milestone-004) | [`RELEASE-009`](./15-release-strategy.md#release-009) | [`ASSUMPTION-034`](./10-project-assumptions.md#assumption-034) | [`CONSTRAINT-034`](./11-project-constraints.md#constraint-034) |
| [`RISK-085`](#risk-085) | [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) | [`DEPENDENCY-010`](./13-project-dependencies.md#dependency-010) | [`MILESTONE-005`](./14-project-milestones.md#milestone-005) | [`RELEASE-010`](./15-release-strategy.md#release-010) | [`ASSUMPTION-035`](./10-project-assumptions.md#assumption-035) | [`CONSTRAINT-035`](./11-project-constraints.md#constraint-035) |
| [`RISK-086`](#risk-086) | [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) | [`DEPENDENCY-011`](./13-project-dependencies.md#dependency-011) | [`MILESTONE-006`](./14-project-milestones.md#milestone-006) | [`RELEASE-011`](./15-release-strategy.md#release-011) | [`ASSUMPTION-036`](./10-project-assumptions.md#assumption-036) | [`CONSTRAINT-036`](./11-project-constraints.md#constraint-036) |
| [`RISK-087`](#risk-087) | [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) | [`DEPENDENCY-012`](./13-project-dependencies.md#dependency-012) | [`MILESTONE-007`](./14-project-milestones.md#milestone-007) | [`RELEASE-012`](./15-release-strategy.md#release-012) | [`ASSUMPTION-037`](./10-project-assumptions.md#assumption-037) | [`CONSTRAINT-037`](./11-project-constraints.md#constraint-037) |
| [`RISK-088`](#risk-088) | [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) | [`DEPENDENCY-013`](./13-project-dependencies.md#dependency-013) | [`MILESTONE-008`](./14-project-milestones.md#milestone-008) | [`RELEASE-013`](./15-release-strategy.md#release-013) | [`ASSUMPTION-038`](./10-project-assumptions.md#assumption-038) | [`CONSTRAINT-038`](./11-project-constraints.md#constraint-038) |
| [`RISK-089`](#risk-089) | [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) | [`DEPENDENCY-014`](./13-project-dependencies.md#dependency-014) | [`MILESTONE-009`](./14-project-milestones.md#milestone-009) | [`RELEASE-014`](./15-release-strategy.md#release-014) | [`ASSUMPTION-039`](./10-project-assumptions.md#assumption-039) | [`CONSTRAINT-039`](./11-project-constraints.md#constraint-039) |
| [`RISK-090`](#risk-090) | [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) | [`DEPENDENCY-015`](./13-project-dependencies.md#dependency-015) | [`MILESTONE-010`](./14-project-milestones.md#milestone-010) | [`RELEASE-015`](./15-release-strategy.md#release-015) | [`ASSUMPTION-040`](./10-project-assumptions.md#assumption-040) | [`CONSTRAINT-040`](./11-project-constraints.md#constraint-040) |
| [`RISK-091`](#risk-091) | [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) | [`DEPENDENCY-016`](./13-project-dependencies.md#dependency-016) | [`MILESTONE-011`](./14-project-milestones.md#milestone-011) | [`RELEASE-016`](./15-release-strategy.md#release-016) | [`ASSUMPTION-041`](./10-project-assumptions.md#assumption-041) | [`CONSTRAINT-041`](./11-project-constraints.md#constraint-041) |
| [`RISK-092`](#risk-092) | [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) | [`DEPENDENCY-017`](./13-project-dependencies.md#dependency-017) | [`MILESTONE-012`](./14-project-milestones.md#milestone-012) | [`RELEASE-017`](./15-release-strategy.md#release-017) | [`ASSUMPTION-042`](./10-project-assumptions.md#assumption-042) | [`CONSTRAINT-042`](./11-project-constraints.md#constraint-042) |
| [`RISK-093`](#risk-093) | [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) | [`DEPENDENCY-018`](./13-project-dependencies.md#dependency-018) | [`MILESTONE-013`](./14-project-milestones.md#milestone-013) | [`RELEASE-018`](./15-release-strategy.md#release-018) | [`ASSUMPTION-043`](./10-project-assumptions.md#assumption-043) | [`CONSTRAINT-043`](./11-project-constraints.md#constraint-043) |
| [`RISK-094`](#risk-094) | [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) | [`DEPENDENCY-019`](./13-project-dependencies.md#dependency-019) | [`MILESTONE-014`](./14-project-milestones.md#milestone-014) | [`RELEASE-019`](./15-release-strategy.md#release-019) | [`ASSUMPTION-044`](./10-project-assumptions.md#assumption-044) | [`CONSTRAINT-044`](./11-project-constraints.md#constraint-044) |
| [`RISK-095`](#risk-095) | [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) | [`DEPENDENCY-020`](./13-project-dependencies.md#dependency-020) | [`MILESTONE-015`](./14-project-milestones.md#milestone-015) | [`RELEASE-020`](./15-release-strategy.md#release-020) | [`ASSUMPTION-045`](./10-project-assumptions.md#assumption-045) | [`CONSTRAINT-045`](./11-project-constraints.md#constraint-045) |
| [`RISK-096`](#risk-096) | [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) | [`DEPENDENCY-021`](./13-project-dependencies.md#dependency-021) | [`MILESTONE-016`](./14-project-milestones.md#milestone-016) | [`RELEASE-021`](./15-release-strategy.md#release-021) | [`ASSUMPTION-046`](./10-project-assumptions.md#assumption-046) | [`CONSTRAINT-046`](./11-project-constraints.md#constraint-046) |
| [`RISK-097`](#risk-097) | [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) | [`DEPENDENCY-022`](./13-project-dependencies.md#dependency-022) | [`MILESTONE-017`](./14-project-milestones.md#milestone-017) | [`RELEASE-022`](./15-release-strategy.md#release-022) | [`ASSUMPTION-047`](./10-project-assumptions.md#assumption-047) | [`CONSTRAINT-047`](./11-project-constraints.md#constraint-047) |
| [`RISK-098`](#risk-098) | [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) | [`DEPENDENCY-023`](./13-project-dependencies.md#dependency-023) | [`MILESTONE-018`](./14-project-milestones.md#milestone-018) | [`RELEASE-023`](./15-release-strategy.md#release-023) | [`ASSUMPTION-048`](./10-project-assumptions.md#assumption-048) | [`CONSTRAINT-048`](./11-project-constraints.md#constraint-048) |
| [`RISK-099`](#risk-099) | [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) | [`DEPENDENCY-024`](./13-project-dependencies.md#dependency-024) | [`MILESTONE-019`](./14-project-milestones.md#milestone-019) | [`RELEASE-024`](./15-release-strategy.md#release-024) | [`ASSUMPTION-049`](./10-project-assumptions.md#assumption-049) | [`CONSTRAINT-049`](./11-project-constraints.md#constraint-049) |
| [`RISK-100`](#risk-100) | [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) | [`DEPENDENCY-025`](./13-project-dependencies.md#dependency-025) | [`MILESTONE-020`](./14-project-milestones.md#milestone-020) | [`RELEASE-025`](./15-release-strategy.md#release-025) | [`ASSUMPTION-050`](./10-project-assumptions.md#assumption-050) | [`CONSTRAINT-050`](./11-project-constraints.md#constraint-050) |

## 8. Risk Management Governance & Sign-off Appendix
This Master Project Risk Register has been formally reviewed and ratified by the Project Steering Committee:

| Ratifying Official | Title & Cadre | Department | Ratification Date | Status |
| :--- | :--- | :--- | :---: | :---: |
| **Dr. K. V. Trilok Chandra, IAS** | Special Commissioner (Health), BBMP | Project Executive Sponsor | 2026-03-01 | `APPROVED` |
| **Dr. Nirmala Buggi** | Chief Health Officer (Public Health) | Clinical Safety Authority | 2026-03-01 | `APPROVED` |
| **Sri. S. Vidyashankar** | Managing Director, K-Mati Analytics | Program Director | 2026-03-01 | `APPROVED` |
| **Dr. Anand S.** | Chief Healthcare Solutions Architect | Chief Risk Officer | 2026-03-01 | `APPROVED` |
