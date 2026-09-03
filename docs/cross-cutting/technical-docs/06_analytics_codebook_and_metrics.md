# 📊 Analytics Codebook & Public Health Metric Definitions
## Namma Clinic Digital Health & Operations Platform
### Standardized Formulas, Epidemiological Surveillance Heuristics & KPI Dictionary
### Document Code: TD-ANL-06 | Version: 1.0 | Date: September 2026

---

## 1. Document Objective

This codebook defines the mathematical formulas, grain of measurement, dimensions, thresholds, and reporting definitions for all **Key Performance Indicators (KPIs)**, **Public Health Surveillance Alerts**, and **Operational Governance Metrics** surfaced across the Clinic, Zonal, and Special Commissioner Dashboards.

---

## 2. Frontline Clinic Operations & Service Utilization Metrics

### M-01: Daily Outpatient Footfall (OPD Volume)
* **Definition:** Total count of unique clinical encounter visits registered at a given clinic within a 24-hour calendar day.
* **Formula:**
  $$\text{Daily OPD} = \sum \mathbf{1}_{(\text{clinic\_id}=c \land \text{visit\_date}=d)}$$
* **Dimensions:** Clinic ID, Zone, Ward, Service Category (`GENERAL_OPD`, `FEVER`, `NCD_SCREENING`, `MCH`, `IMMUNIZATION`).
* **Reporting Frequency:** Real-time (refreshed every 60 seconds) & Daily Consolidated.

### M-02: Mean Turnaround Time (TAT) per Patient Station
* **Definition:** Elapsed duration in minutes spent by a citizen across individual clinic stations.
* **Formulas:**
  * $\text{Registration to Triage TAT} = t_{\text{triage\_start}} - t_{\text{check\_in}}$ (Target: $< 5\text{ mins}$)
  * $\text{Triage to Doctor Consultation TAT} = t_{\text{doctor\_start}} - t_{\text{triage\_end}}$ (Target: $< 10\text{ mins}$)
  * $\text{Consultation Duration} = t_{\text{consultation\_complete}} - t_{\text{doctor\_start}}$ (Target: $3 - 6\text{ mins}$)
  * $\text{Doctor to Pharmacy Dispense TAT} = t_{\text{dispensed}} - t_{\text{consultation\_complete}}$ (Target: $< 3\text{ mins}$)
  * **Total Clinic Length of Stay (LoS):** $t_{\text{discharge}} - t_{\text{check\_in}}$ (Target: $< 25\text{ mins}$)

### M-03: Repeat Patient Retention Rate
* **Definition:** Percentage of consultations in a 30-day window performed for citizens who have previously visited any Namma Clinic.
* **Formula:**
  $$\text{Repeat Rate (\%)} = \left( \frac{\text{Visits by Patients with Prior Visits}}{\text{Total Visits Recorded in Period}} \right) \times 100$$
* **Benchmark:** Expected baseline $35–50\%$ for primary health continuity.

---

## 3. Epidemiological Disease Surveillance & Outbreak Heuristics

Aligned with the **Integrated Disease Surveillance Programme (IDSP)** syndromic reporting:

### M-04: Acute Febrile Illness (AFI) / Fever Cluster Alert
* **Clinical Syndromic Definition:** Patient presenting with body temperature $\ge 38.0^\circ\text{C}$ or chief complaint of "Fever" $\le 7$ days.
* **Cluster Anomaly Alert Formula:**
  A **Zonal Fever Outbreak Warning** triggers when the daily fever incidence in a specific BBMP ward exceeds the 30-day moving average ($\mu$) by more than **two standard deviations ($2\sigma$)**:
  $$\text{Alert Triggered if: } X_{\text{ward}, d} > \mu_{30} + 2 \times \sigma_{30} \quad \text{where } X \ge 10\text{ cases}$$
* **Automated Action:** Generates immediate Red Flag tile on Zonal MO & Commissioner dashboard; alerts district epidemiologist for dengue/malaria vector containment.

### M-05: Acute Respiratory Infection (ARI) Trend Index
* **Clinical Definition:** Cases presenting with cough, sore throat, or breathlessness with or without fever.
* **Seasonal Comparison:** Ratio of current week's respiratory visits compared to the same calendar week of the preceding year.

---

## 4. Non-Communicable Disease (NCD) Burden & Management Metrics

Aligned with the **National Programme for Prevention & Control of Cancer, Diabetes, Cardiovascular Diseases & Stroke (NP-NCD)**:

### M-06: Adult Population NCD Screening Coverage Rate
* **Definition:** Proportion of registered adult citizens ($\ge 30$ years old) who have undergone mandatory blood pressure and blood glucose screening.
* **Formula:**
  $$\text{NCD Screening Coverage (\%)} = \left( \frac{\text{Unique Patients Aged } \ge 30 \text{ Screened for BP \& Sugar}}{\text{Total Registered Patients Aged } \ge 30} \right) \times 100$$

### M-07: Uncontrolled Hypertension Burden
* **Definition:** Proportion of screened patients exhibiting systolic blood pressure $\ge 140\text{ mmHg}$ or diastolic blood pressure $\ge 90\text{ mmHg}$.
* **Formula:**
  $$\text{HTN Positivity Rate (\%)} = \left( \frac{\text{Screened Patients with BP } \ge 140/90\text{ mmHg}}{\text{Total Patients with Blood Pressure Recorded}} \right) \times 100$$

### M-08: Diabetic Glycemic Control Rate
* **Definition:** Proportion of known diabetic patients on active pharmacotherapy who maintain random blood sugar $< 160\text{ mg/dL}$ (or Fasting $< 126\text{ mg/dL}$).

### M-09: NCD Follow-up Defaulter Index (Recall Cohort)
* **Definition:** Count of diagnosed hypertensive or diabetic patients whose scheduled 30-day medication refill visit is overdue by $> 14\text{ calendar days}$.
* **Automated Trigger:** Feeds daily into the automated bilingual SMS recall queue.

---

## 5. Pharmacy Supply Chain & Inventory Metrics

### M-10: Medicine Stock-Out Rate
* **Definition:** Percentage of the 45 essential primary care formulary medications currently at zero on-hand quantity in a clinic.
* **Formula:**
  $$\text{Stock-Out Rate (\%)} = \left( \frac{\text{Count of Essential Medicines with Stock } = 0}{\text{Total Formulary Items (45)}} \right) \times 100$$
* **SLA Threshold:** Must be $< 5\%$ across all operational clinics.

### M-11: Predictive Days of Inventory Remaining (DIR)
* **Definition:** Estimated number of days before a specific medication is fully depleted based on recent 14-day average consumption velocity.
* **Formula:**
  $$\text{DIR} = \frac{\text{Current Available Quantity (Pills)}}{\text{Average Daily Dispense Velocity (Pills/Day)}}$$
* **Thresholds:**
  * $\text{DIR} \le 3\text{ Days}$: 🔴 **Critical Stock-out Warning** (Emergency transfer required).
  * $4 \le \text{DIR} \le 7\text{ Days}$: 🟡 **Reorder Indent Alert** (Central store indent triggered).
  * $\text{DIR} > 30\text{ Days}$: 🟢 **Normal Stock Reserve**.

---

## 6. Referral Continuum of Care Metrics

### M-12: Digital Referral Initiation & Closure Rate
* **Formulas:**
  * $\text{Referral Outbound Rate (\%)} = \left( \frac{\text{Referrals Issued}}{\text{Total OPD Consultations}} \right) \times 100$ (Normal primary care benchmark: $3 - 6\%$).
  * $\text{Referral Closure Rate (\%)} = \left( \frac{\text{Referrals Acknowledged/Treated at Destination}}{\text{Total Outbound Referrals Initiated}} \right) \times 100$.
