"""
db_olap_dq_lineage.py
Canonical definitions for:
- 10 OLAP Star Schema Fact Tables (FACT-001 to FACT-010)
- 12 OLAP Star Schema Dimension Tables (DIM-001 to DIM-012)
- 50 Analytical Measures (MEASURE-001 to MEASURE-050)
- 50 Data Quality Rules (DQ-001 to DQ-050)
- 25 End-to-End Data Lineage Pathways (LINEAGE-001 to LINEAGE-025)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from typing import List, Dict, Any

# -----------------------------------------------------------------------------
# 1. 10 OLAP FACT TABLES (FACT-001 to FACT-010)
# -----------------------------------------------------------------------------
FACTS = [
    {
        "id": "FACT-001",
        "name": "fact_opd_encounters",
        "grain": "One row per completed outpatient clinical consultation encounter",
        "description": "Captures patient footfall, consultation duration, wait time before consult, and disposition category.",
        "dimensions": ["dim_date", "dim_time_of_day", "dim_facility", "dim_provider", "dim_patient_demographics", "dim_diagnosis"],
        "measures": ["encounter_count", "consultation_duration_seconds", "wait_to_consult_seconds", "is_first_visit_flag", "telemedicine_flag"],
        "scd_strategy": "SCD Type 1 for encounter facts; dimensions link to prevailing surrogate keys at encounter sign-off",
        "etl_source": "clinical.clinical_encounters, clinical.clinical_notes, intake.queue_entries",
        "freshness": "Hourly micro-batch ELT pipeline"
    },
    {
        "id": "FACT-002",
        "name": "fact_queue_performance",
        "grain": "One row per patient transition through a clinic service stage",
        "description": "Measures queue latency, service duration, bottleneck stages, and SLA breaches across registration, triage, doctor, and pharmacy.",
        "dimensions": ["dim_date", "dim_time_of_day", "dim_facility", "dim_queue_stage", "dim_triage_acuity"],
        "measures": ["transition_count", "stage_wait_duration_seconds", "service_duration_seconds", "sla_breach_flag", "abandoned_flag"],
        "scd_strategy": "SCD Type 1 event fact",
        "etl_source": "intake.queue_entries, intake.tokens",
        "freshness": "15-minute near-real-time streaming ELT"
    },
    {
        "id": "FACT-003",
        "name": "fact_doctor_workload",
        "grain": "One row per doctor shift day",
        "description": "Aggregates clinician consultation throughput, average consultation minutes, diagnosis diversity, and prescription intensity.",
        "dimensions": ["dim_date", "dim_facility", "dim_provider"],
        "measures": ["total_consultations", "active_consultation_minutes", "average_consult_duration_minutes", "prescriptions_authored_count", "referrals_ordered_count"],
        "scd_strategy": "Daily pre-aggregated summary fact table",
        "etl_source": "clinical.clinical_encounters, identity.staff_shifts",
        "freshness": "Daily nightly batch run at 01:00 UTC"
    },
    {
        "id": "FACT-004",
        "name": "fact_pharmacy_dispensations",
        "grain": "One row per dispensed medication line item",
        "description": "Tracks pharmaceutical fulfillment volume, dispensed units, financial value, stock batch utilization, and fulfillment lag.",
        "dimensions": ["dim_date", "dim_facility", "dim_medication", "dim_patient_demographics"],
        "measures": ["dispensed_quantity", "unit_cost_inr", "total_dispensation_value_inr", "prescription_to_dispense_seconds", "generic_substitution_flag"],
        "scd_strategy": "SCD Type 1 immutable transactional fact",
        "etl_source": "pharmacy.dispensations, pharmacy.dispensation_items, pharmacy.pharmacy_batches",
        "freshness": "Hourly batch ELT"
    },
    {
        "id": "FACT-005",
        "name": "fact_inventory_stockouts",
        "grain": "One row per stockout event per drug per clinic facility",
        "description": "Records essential drug stockout incidents, duration of zero inventory, affected patients, and indent emergency reorders.",
        "dimensions": ["dim_date", "dim_facility", "dim_medication"],
        "measures": ["stockout_incident_count", "stockout_duration_hours", "unfulfilled_prescriptions_count", "buffer_depletion_velocity", "emergency_indent_flag"],
        "scd_strategy": "Accumulating snapshot fact table updated until stock replenished",
        "etl_source": "pharmacy.clinic_stock, pharmacy.stock_movements",
        "freshness": "Real-time trigger on clinic_stock = 0"
    },
    {
        "id": "FACT-006",
        "name": "fact_laboratory_investigations",
        "grain": "One row per completed laboratory test observation",
        "description": "Quantifies diagnostic test throughput, specimen turnaround time (TAT), abnormal findings rate, and critical panic value escalations.",
        "dimensions": ["dim_date", "dim_facility", "dim_laboratory_test", "dim_patient_demographics"],
        "measures": ["test_count", "specimen_to_result_minutes", "abnormal_flag", "panic_value_flag", "reagent_cost_inr"],
        "scd_strategy": "SCD Type 1 transactional fact",
        "etl_source": "clinical.lab_orders, clinical.lab_order_items, clinical.lab_results",
        "freshness": "Hourly batch pipeline"
    },
    {
        "id": "FACT-007",
        "name": "fact_patient_referrals",
        "grain": "One row per secondary/tertiary hospital referral dossier",
        "description": "Monitors outbound clinical referrals, specialist counter-referral feedback rates, destination hospital congestion, and loop closure delay.",
        "dimensions": ["dim_date", "dim_facility", "dim_referral_facility", "dim_diagnosis", "dim_triage_acuity"],
        "measures": ["referral_count", "counter_referral_received_flag", "referral_closure_days", "emergency_transfer_flag", "patient_admitted_flag"],
        "scd_strategy": "Accumulating snapshot fact closed upon counter-note receipt",
        "etl_source": "continuity.referrals, continuity.referral_counter_notes",
        "freshness": "Daily batch sync"
    },
    {
        "id": "FACT-008",
        "name": "fact_maternal_ncd_continuity",
        "grain": "One row per registered chronic disease / antenatal patient per calendar month",
        "description": "Measures longitudinal care adherence, monthly BP/sugar control status, scheduled follow-up attendance, and ASHA outreach visits.",
        "dimensions": ["dim_date", "dim_facility", "dim_patient_demographics", "dim_diagnosis"],
        "measures": ["enrolled_patients_count", "attended_monthly_visit_flag", "condition_controlled_flag", "missed_follow_up_count", "complication_escalated_flag"],
        "scd_strategy": "Periodic monthly snapshot fact table",
        "etl_source": "continuity.ncd_episodes, continuity.follow_up_schedules, intake.patient_vitals",
        "freshness": "Monthly batch snapshot run on 1st of each month"
    },
    {
        "id": "FACT-009",
        "name": "fact_disease_surveillance",
        "grain": "One row per communicable disease diagnosis per ward per day",
        "description": "Tracks epidemiological disease incidence (Dengue, Typhoid, Acute Diarrheal Disease, Tuberculosis, COVID-19) for outbreak detection.",
        "dimensions": ["dim_date", "dim_facility", "dim_diagnosis", "dim_patient_demographics"],
        "measures": ["case_count", "hospitalization_count", "ward_incidence_rate_per_10k", "epidemic_threshold_breach_flag", "lab_confirmed_case_count"],
        "scd_strategy": "Daily aggregated fact table",
        "etl_source": "clinical.diagnoses, intake.patient_addresses",
        "freshness": "Daily automated pipeline feeding IDSP national portal"
    },
    {
        "id": "FACT-010",
        "name": "fact_clinic_operational_kpis",
        "grain": "One row per clinic facility per operational day",
        "description": "Executive dashboard fact summarizing daily patient intake, staff attendance, cold chain integrity, stock availability, and Sakala grievances.",
        "dimensions": ["dim_date", "dim_facility"],
        "measures": ["total_footfall", "doctor_hours_delivered", "cold_chain_excursion_count", "formulary_availability_percentage", "open_grievances_count"],
        "scd_strategy": "Daily executive rollup fact table",
        "etl_source": "All domain transaction tables",
        "freshness": "Nightly batch run at 02:30 UTC"
    }
]

FACT_MAP = {f["id"]: f for f in FACTS}

# -----------------------------------------------------------------------------
# 2. 12 OLAP DIMENSION TABLES (DIM-001 to DIM-012)
# -----------------------------------------------------------------------------
DIMENSIONS = [
    {
        "id": "DIM-001",
        "name": "dim_date",
        "type": "Role-Playing Conformed Dimension",
        "pk": "date_key",
        "description": "Calendar dates from 2024 to 2035 with financial year, quarter, month, week, day of week, Kannada local holidays, and monsoon season indicators.",
        "scd_type": "SCD Type 0 (Static Pre-populated)",
        "attributes": ["date_key", "full_date", "day_of_week", "day_name", "month_number", "month_name", "quarter", "calendar_year", "financial_year", "is_weekend", "is_gazetted_holiday", "monsoon_season_flag"]
    },
    {
        "id": "DIM-002",
        "name": "dim_time_of_day",
        "type": "Conformed Dimension",
        "pk": "time_key",
        "description": "Minutes of the day (00:00 to 23:59 = 1,440 rows) with hour, shift band (Morning OPD, Afternoon OPD, Evening Clinic, Off-hours), and rush-hour flags.",
        "scd_type": "SCD Type 0 (Static Pre-populated)",
        "attributes": ["time_key", "time_of_day", "hour_24", "minute", "shift_band", "opd_operational_flag", "peak_rush_period_flag"]
    },
    {
        "id": "DIM-003",
        "name": "dim_facility",
        "type": "Core Dimension",
        "pk": "facility_key",
        "description": "Namma Clinics, UPHCs, and referral hospitals with BBMP administrative zone, ward number, assembly constituency, and facility tier.",
        "scd_type": "SCD Type 2 (History tracking for ward delimitation and MOIC reassignments)",
        "attributes": ["facility_key", "facility_id", "facility_code", "facility_name", "ward_number", "ward_name", "zone_name", "constituency_name", "facility_type", "hfr_id", "row_effective_date", "row_expiry_date", "is_current_flag"]
    },
    {
        "id": "DIM-004",
        "name": "dim_provider",
        "type": "Core Dimension",
        "pk": "provider_key",
        "description": "Healthcare professionals (Medical Officers, Specialists, Staff Nurses, Pharmacists, Lab Techs) with medical council registration and tenure.",
        "scd_type": "SCD Type 2 (Tracks facility postings and role promotions)",
        "attributes": ["provider_key", "user_id", "staff_full_name", "professional_role", "specialization", "kmc_registration_number", "primary_facility_code", "row_effective_date", "row_expiry_date", "is_current_flag"]
    },
    {
        "id": "DIM-005",
        "name": "dim_patient_demographics",
        "type": "Conformed Dimension",
        "pk": "demographic_key",
        "description": "De-identified demographic cohorts: age bands (Pediatric 0-5, School 6-17, Adult 18-59, Geriatric 60+), gender, socio-economic proxy, and home ward.",
        "scd_type": "SCD Type 1 (No PII stored; aggregated demographic strata)",
        "attributes": ["demographic_key", "age_group", "gender", "home_zone", "home_ward_number", "bpl_ration_card_holder_flag", "abha_linked_flag"]
    },
    {
        "id": "DIM-006",
        "name": "dim_diagnosis",
        "type": "Conformed Clinical Dimension",
        "pk": "diagnosis_key",
        "description": "Standardized diagnosis hierarchy mapped to WHO ICD-10 chapters, blocks, specific 3-character codes, and communicable/chronic flags.",
        "scd_type": "SCD Type 1",
        "attributes": ["diagnosis_key", "icd10_code", "diagnosis_display_name", "icd10_chapter_number", "icd10_chapter_title", "icd10_block_name", "is_communicable_disease", "is_chronic_ncd", "idsp_surveillance_priority_flag"]
    },
    {
        "id": "DIM-007",
        "name": "dim_medication",
        "type": "Conformed Formulary Dimension",
        "pk": "medication_key",
        "description": "Pharmaceutical products from NLEM formulary with WHO ATC level 1 to 5 hierarchy, strength, dosage form, and antibiotic classification (AWaRe).",
        "scd_type": "SCD Type 1",
        "attributes": ["medication_key", "drug_id", "generic_name", "strength", "dosage_form", "atc_level1_anatomical", "atc_level3_pharmacological", "who_aware_classification", "is_essential_nlem_flag"]
    },
    {
        "id": "DIM-008",
        "name": "dim_laboratory_test",
        "type": "Diagnostic Dimension",
        "pk": "test_key",
        "description": "Diagnostic investigation catalog categorized by clinical pathology, biochemistry, microbiology, LOINC code, and specimen requirements.",
        "scd_type": "SCD Type 1",
        "attributes": ["test_key", "loinc_code", "test_name", "laboratory_section", "specimen_type", "turnaround_sla_minutes", "point_of_care_flag"]
    },
    {
        "id": "DIM-009",
        "name": "dim_queue_stage",
        "type": "Operational Dimension",
        "pk": "stage_key",
        "description": "Clinic workflow service points (Reception/Token, Nursing Triage, Consultation Chamber, Pharmacy Window, Sample Collection).",
        "scd_type": "SCD Type 0",
        "attributes": ["stage_key", "stage_code", "stage_name", "target_service_sla_seconds", "target_wait_sla_seconds", "clinical_service_flag"]
    },
    {
        "id": "DIM-010",
        "name": "dim_referral_facility",
        "type": "Continuity Dimension",
        "pk": "referral_facility_key",
        "description": "Destination referral institutions including BBMP General Hospitals, Victoria Hospital, Bowring, and specialized institutes (NIMHANS, Kidwai).",
        "scd_type": "SCD Type 1",
        "attributes": ["referral_facility_key", "hospital_name", "institution_type", "distance_category", "specialties_offered_json", "abdm_integrated_flag"]
    },
    {
        "id": "DIM-011",
        "name": "dim_triage_acuity",
        "type": "Clinical Triage Dimension",
        "pk": "acuity_key",
        "description": "South African Triage Scale (SATS) acuity levels (Red: Emergency, Orange: Very Urgent, Yellow: Urgent, Green: Routine, Blue: Deceased).",
        "scd_type": "SCD Type 0",
        "attributes": ["acuity_key", "sats_color_code", "acuity_title", "target_physician_response_minutes", "immediate_resuscitation_flag"]
    },
    {
        "id": "DIM-012",
        "name": "dim_grievance_category",
        "type": "Governance Dimension",
        "pk": "grievance_category_key",
        "description": "Karnataka Sakala public service guarantee grievance classifications and statutory resolution deadlines.",
        "scd_type": "SCD Type 1",
        "attributes": ["grievance_category_key", "category_code", "category_name", "sakala_guaranteed_days", "escalation_authority_role"]
    }
]

DIMENSION_MAP = {d["id"]: d for d in DIMENSIONS}

# -----------------------------------------------------------------------------
# 3. 50 ANALYTICAL MEASURES (MEASURE-001 to MEASURE-050)
# -----------------------------------------------------------------------------
MEASURES = [
    # FACT-001: OPD Encounters (1-5)
    {"id": "MEASURE-001", "fact_id": "FACT-001", "name": "total_opd_encounters", "agg": "SUM(encounter_count)", "unit": "Encounters", "description": "Total outpatient consultations completed across clinics"},
    {"id": "MEASURE-002", "fact_id": "FACT-001", "name": "avg_consultation_minutes", "agg": "AVG(consultation_duration_seconds)/60.0", "unit": "Minutes", "description": "Average duration spent by physician per patient consultation"},
    {"id": "MEASURE-003", "fact_id": "FACT-001", "name": "avg_wait_to_consult_minutes", "agg": "AVG(wait_to_consult_seconds)/60.0", "unit": "Minutes", "description": "Average time patient waited in clinic before doctor consult"},
    {"id": "MEASURE-004", "fact_id": "FACT-001", "name": "first_visit_ratio", "agg": "SUM(is_first_visit_flag)::float / COUNT(*)", "unit": "Percentage", "description": "Percentage of encounters representing first-time clinic patients"},
    {"id": "MEASURE-005", "fact_id": "FACT-001", "name": "teleconsultation_percentage", "agg": "SUM(telemedicine_flag)::float / COUNT(*)", "unit": "Percentage", "description": "Percentage of consultations utilizing remote specialist teleconsultation"},

    # FACT-002: Queue Performance (6-10)
    {"id": "MEASURE-006", "fact_id": "FACT-002", "name": "total_queue_transitions", "agg": "SUM(transition_count)", "unit": "Transitions", "description": "Total stage progressions completed across clinic service points"},
    {"id": "MEASURE-007", "fact_id": "FACT-002", "name": "avg_triage_wait_minutes", "agg": "AVG(stage_wait_duration_seconds) FILTER (WHERE stage_code = 'TRIAGE')/60.0", "unit": "Minutes", "description": "Average wait time in hall before nursing triage"},
    {"id": "MEASURE-008", "fact_id": "FACT-002", "name": "avg_pharmacy_wait_minutes", "agg": "AVG(stage_wait_duration_seconds) FILTER (WHERE stage_code = 'PHARMACY')/60.0", "unit": "Minutes", "description": "Average wait time at pharmacy dispensing window"},
    {"id": "MEASURE-009", "fact_id": "FACT-002", "name": "queue_sla_breach_rate", "agg": "SUM(sla_breach_flag)::float / COUNT(*)", "unit": "Percentage", "description": "Proportion of patient queue stages exceeding maximum allowable wait SLA"},
    {"id": "MEASURE-010", "fact_id": "FACT-002", "name": "patient_dropout_rate", "agg": "SUM(abandoned_flag)::float / COUNT(*)", "unit": "Percentage", "description": "Percentage of issued tokens where patient left clinic before consultation"},

    # FACT-003: Doctor Workload (11-15)
    {"id": "MEASURE-011", "fact_id": "FACT-003", "name": "consultations_per_doctor_day", "agg": "AVG(total_consultations)", "unit": "Patients/Day", "description": "Average daily patient volume handled by each on-duty doctor"},
    {"id": "MEASURE-012", "fact_id": "FACT-003", "name": "doctor_clinical_utilization", "agg": "SUM(active_consultation_minutes) / (COUNT(*) * 360.0)", "unit": "Percentage", "description": "Proportion of 6-hour shift time actively spent in patient consultation"},
    {"id": "MEASURE-013", "fact_id": "FACT-003", "name": "prescriptions_per_encounter_rate", "agg": "SUM(prescriptions_authored_count)::float / SUM(total_consultations)", "unit": "Prescriptions/Encounter", "description": "Prescription issuance propensity per clinical consultation"},
    {"id": "MEASURE-014", "fact_id": "FACT-003", "name": "referral_escalation_rate", "agg": "SUM(referrals_ordered_count)::float / SUM(total_consultations)", "unit": "Percentage", "description": "Proportion of doctor consultations resulting in secondary hospital referral"},
    {"id": "MEASURE-015", "fact_id": "FACT-003", "name": "active_doctor_shift_days", "agg": "COUNT(DISTINCT (provider_key, date_key))", "unit": "Shift Days", "description": "Total doctor duty days delivered across the clinic network"},

    # FACT-004: Pharmacy Dispensations (16-20)
    {"id": "MEASURE-016", "fact_id": "FACT-004", "name": "total_units_dispensed", "agg": "SUM(dispensed_quantity)", "unit": "Doses/Tablets", "description": "Total physical units of medication dispensed to citizens"},
    {"id": "MEASURE-017", "fact_id": "FACT-004", "name": "total_pharmacy_expenditure_inr", "agg": "SUM(total_dispensation_value_inr)", "unit": "INR (Rupees)", "description": "Total value of pharmaceutical drugs dispensed at government procurement cost"},
    {"id": "MEASURE-018", "fact_id": "FACT-004", "name": "avg_dispensing_lag_minutes", "agg": "AVG(prescription_to_dispense_seconds)/60.0", "unit": "Minutes", "description": "Average time between doctor prescription sign-off and pharmacy handover"},
    {"id": "MEASURE-019", "fact_id": "FACT-004", "name": "generic_substitution_rate", "agg": "SUM(generic_substitution_flag)::float / COUNT(*)", "unit": "Percentage", "description": "Percentage of prescribed drugs substituted with equivalent generic formulation"},
    {"id": "MEASURE-020", "fact_id": "FACT-004", "name": "antibiotic_dispensation_percentage", "agg": "SUM(dispensed_quantity) FILTER (WHERE atc_level1 = 'J')::float / SUM(dispensed_quantity)", "unit": "Percentage", "description": "Proportion of total dispensed drugs categorized as systemic antibiotics"},

    # FACT-005: Inventory Stockouts (21-25)
    {"id": "MEASURE-021", "fact_id": "FACT-005", "name": "total_stockout_incidents", "agg": "SUM(stockout_incident_count)", "unit": "Incidents", "description": "Total count of zero-inventory events recorded for essential formulary drugs"},
    {"id": "MEASURE-022", "fact_id": "FACT-005", "name": "cumulative_stockout_hours", "agg": "SUM(stockout_duration_hours)", "unit": "Hours", "description": "Total hours during which clinics lacked required essential medications"},
    {"id": "MEASURE-023", "fact_id": "FACT-005", "name": "unfulfilled_prescriptions_due_to_stockout", "agg": "SUM(unfulfilled_prescriptions_count)", "unit": "Prescriptions", "description": "Citizen prescriptions unable to be dispensed due to pharmacy stockout"},
    {"id": "MEASURE-024", "fact_id": "FACT-005", "name": "average_stockout_resolution_days", "agg": "AVG(stockout_duration_hours)/24.0", "unit": "Days", "description": "Mean time taken from stock depletion to central warehouse replenishment"},
    {"id": "MEASURE-025", "fact_id": "FACT-005", "name": "emergency_indent_frequency", "agg": "SUM(emergency_indent_flag)", "unit": "Requisitions", "description": "Count of expedited emergency drug requisitions placed due to imminent stockout"},

    # FACT-006: Diagnostic Laboratory (26-30)
    {"id": "MEASURE-026", "fact_id": "FACT-006", "name": "total_lab_tests_performed", "agg": "SUM(test_count)", "unit": "Tests", "description": "Total diagnostic investigations completed and verified"},
    {"id": "MEASURE-027", "fact_id": "FACT-006", "name": "avg_lab_turnaround_minutes", "agg": "AVG(specimen_to_result_minutes)", "unit": "Minutes", "description": "Average duration from sample collection to verified result availability"},
    {"id": "MEASURE-028", "fact_id": "FACT-006", "name": "abnormal_lab_result_rate", "agg": "SUM(abnormal_flag)::float / COUNT(*)", "unit": "Percentage", "description": "Proportion of completed lab tests yielding values outside biological reference range"},
    {"id": "MEASURE-029", "fact_id": "FACT-006", "name": "critical_panic_alert_count", "agg": "SUM(panic_value_flag)", "unit": "Panic Values", "description": "Count of life-threatening critical lab values requiring immediate doctor telephone alert"},
    {"id": "MEASURE-030", "fact_id": "FACT-006", "name": "total_diagnostic_reagent_cost_inr", "agg": "SUM(reagent_cost_inr)", "unit": "INR", "description": "Total direct cost of reagents consumed in clinic point-of-care testing"},

    # FACT-007: Patient Referrals (31-35)
    {"id": "MEASURE-031", "fact_id": "FACT-007", "name": "total_outbound_referrals", "agg": "SUM(referral_count)", "unit": "Referrals", "description": "Total patients transferred to secondary/tertiary public hospitals"},
    {"id": "MEASURE-032", "fact_id": "FACT-007", "name": "referral_loop_closure_rate", "agg": "SUM(counter_referral_received_flag)::float / COUNT(*)", "unit": "Percentage", "description": "Percentage of outbound referrals receiving specialist discharge counter-notes"},
    {"id": "MEASURE-033", "fact_id": "FACT-007", "name": "avg_referral_closure_days", "agg": "AVG(referral_closure_days)", "unit": "Days", "description": "Mean time taken from primary clinic referral to completed feedback loop"},
    {"id": "MEASURE-034", "fact_id": "FACT-007", "name": "emergency_referral_percentage", "agg": "SUM(emergency_transfer_flag)::float / COUNT(*)", "unit": "Percentage", "description": "Proportion of referrals categorized as critical/emergency medical transfers"},
    {"id": "MEASURE-035", "fact_id": "FACT-007", "name": "referred_patient_admission_rate", "agg": "SUM(patient_admitted_flag)::float / COUNT(*)", "unit": "Percentage", "description": "Proportion of referred patients admitted as inpatients at destination hospital"},

    # FACT-008: Maternal & NCD Care Continuity (36-40)
    {"id": "MEASURE-036", "fact_id": "FACT-008", "name": "total_active_ncd_cohort", "agg": "SUM(enrolled_patients_count)", "unit": "Citizens", "description": "Active registered population living with chronic diabetes or hypertension"},
    {"id": "MEASURE-037", "fact_id": "FACT-008", "name": "monthly_ncd_visit_adherence_rate", "agg": "SUM(attended_monthly_visit_flag)::float / SUM(enrolled_patients_count)", "unit": "Percentage", "description": "Proportion of enrolled NCD patients attending mandatory monthly checkup"},
    {"id": "MEASURE-038", "fact_id": "FACT-008", "name": "glycemic_blood_pressure_control_rate", "agg": "SUM(condition_controlled_flag)::float / SUM(attended_monthly_visit_flag)", "unit": "Percentage", "description": "Percentage of attending NCD patients achieving target clinical thresholds"},
    {"id": "MEASURE-039", "fact_id": "FACT-008", "name": "cumulative_missed_follow_up_visits", "agg": "SUM(missed_follow_up_count)", "unit": "Missed Visits", "description": "Total missed chronic disease review appointments requiring ASHA home outreach"},
    {"id": "MEASURE-040", "fact_id": "FACT-008", "name": "ncd_complication_escalation_rate", "agg": "SUM(complication_escalated_flag)::float / SUM(enrolled_patients_count)", "unit": "Percentage", "description": "Rate of chronic disease complications (diabetic foot, nephropathy, stroke) detected"},

    # FACT-009: Disease Surveillance & IDSP (41-45)
    {"id": "MEASURE-041", "fact_id": "FACT-009", "name": "total_notifiable_disease_cases", "agg": "SUM(case_count)", "unit": "Cases", "description": "Cumulative communicable disease diagnoses reported under IDSP surveillance"},
    {"id": "MEASURE-042", "fact_id": "FACT-009", "name": "ward_incidence_rate", "agg": "AVG(ward_incidence_rate_per_10k)", "unit": "Cases/10,000 Pop", "description": "Normalized population disease incidence rate per administrative ward"},
    {"id": "MEASURE-043", "fact_id": "FACT-009", "name": "epidemic_outbreak_cluster_count", "agg": "SUM(epidemic_threshold_breach_flag)", "unit": "Outbreaks", "description": "Count of ward clusters exceeding statistical historical baseline threshold"},
    {"id": "MEASURE-044", "fact_id": "FACT-009", "name": "laboratory_confirmation_ratio", "agg": "SUM(lab_confirmed_case_count)::float / SUM(case_count)", "unit": "Percentage", "description": "Percentage of syndromic diagnoses confirmed by positive laboratory assay"},
    {"id": "MEASURE-045", "fact_id": "FACT-009", "name": "surveillance_hospitalization_rate", "agg": "SUM(hospitalization_count)::float / SUM(case_count)", "unit": "Percentage", "description": "Severity index representing proportion of disease cases requiring inpatient admission"},

    # FACT-010: Executive Operational KPIs (46-50)
    {"id": "MEASURE-046", "fact_id": "FACT-010", "name": "network_daily_footfall", "agg": "SUM(total_footfall)", "unit": "Citizens/Day", "description": "Total aggregate citizen volume served across all 450 Namma Clinics daily"},
    {"id": "MEASURE-047", "fact_id": "FACT-010", "name": "total_physician_hours_delivered", "agg": "SUM(doctor_hours_delivered)", "unit": "Doctor Hours", "description": "Total cumulative licensed medical officer duty hours delivered"},
    {"id": "MEASURE-048", "fact_id": "FACT-010", "name": "cold_chain_thermal_breach_incidents", "agg": "SUM(cold_chain_excursion_count)", "unit": "Excursions", "description": "Total vaccine refrigerator temperature excursion alerts lasting > 15 minutes"},
    {"id": "MEASURE-049", "fact_id": "FACT-010", "name": "network_formulary_availability_index", "agg": "AVG(formulary_availability_percentage)", "unit": "Percentage", "description": "Percentage of 100 mandatory primary care formulary drugs in stock network-wide"},
    {"id": "MEASURE-050", "fact_id": "FACT-010", "name": "unresolved_sakala_grievance_backlog", "agg": "SUM(open_grievances_count)", "unit": "Tickets", "description": "Count of citizen grievances pending resolution past statutory SLA deadline"}
]

MEASURE_MAP = {m["id"]: m for m in MEASURES}

# -----------------------------------------------------------------------------
# 4. 50 DATA QUALITY RULES (DQ-001 to DQ-050)
# -----------------------------------------------------------------------------
DQ_RULES = [
    {"id": "DQ-001", "dataset": "identity.auth_users", "target": "email", "cond": "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'", "sev": "CRITICAL", "thresh": "100%", "det": "Automated regex check", "rem": "Reject registration on invalid email format", "owner": "CISO"},
    {"id": "DQ-002", "dataset": "identity.auth_users", "target": "phone_blind_index", "cond": "phone_blind_index IS NOT NULL AND length(phone_blind_index) = 64", "sev": "CRITICAL", "thresh": "100%", "det": "Check constraint validation", "rem": "Regenerate HMAC blind index on record save", "owner": "Security Architect"},
    {"id": "DQ-003", "dataset": "identity.user_credentials", "target": "password_hash", "cond": "password_hash LIKE '$argon2id$v=19$%'", "sev": "CRITICAL", "thresh": "100%", "det": "Argon2id format inspection", "rem": "Enforce Argon2id hashing in credential service", "owner": "Security Architect"},
    {"id": "DQ-004", "dataset": "identity.user_credentials", "target": "failed_login_count", "cond": "failed_login_count >= 0 AND failed_login_count <= 100", "sev": "HIGH", "thresh": "100%", "det": "Numeric range check", "rem": "Reset counter to zero on lock expiration", "owner": "SOC Team"},
    {"id": "DQ-005", "dataset": "identity.user_sessions", "target": "expires_at", "cond": "expires_at > created_at", "sev": "CRITICAL", "thresh": "100%", "det": "Timestamp chronological check", "rem": "Enforce valid TTL in session generator", "owner": "Auth Lead"},
    {"id": "DQ-006", "dataset": "identity.role_permissions", "target": "role_id, permission_id", "cond": "UNIQUE (role_id, permission_id)", "sev": "CRITICAL", "thresh": "100%", "det": "Composite uniqueness check", "rem": "Prevent duplicate entitlement grants", "owner": "RBAC Lead"},
    {"id": "DQ-007", "dataset": "identity.facilities", "target": "latitude, longitude", "cond": "latitude BETWEEN 12.0 AND 13.5 AND longitude BETWEEN 77.3 AND 77.8", "sev": "HIGH", "thresh": "100%", "det": "Bengaluru municipal bounding box check", "rem": "Reject out-of-bounds clinic coordinates", "owner": "GIS Specialist"},
    {"id": "DQ-008", "dataset": "identity.staff_profiles", "target": "kmc_registration_number", "cond": "kmc_registration_number IS NOT NULL WHEN professional_role = 'DOCTOR'", "sev": "CRITICAL", "thresh": "100%", "det": "Conditional non-null rule", "rem": "Block doctor onboarding without valid KMC license", "owner": "Medical Superintendent"},
    {"id": "DQ-009", "dataset": "identity.system_configs", "target": "config_value_json", "cond": "jsonb_typeof(config_value_json) = 'object'", "sev": "HIGH", "thresh": "100%", "det": "JSON schema structural check", "rem": "Reject malformed configuration payload", "owner": "DevOps Architect"},
    {"id": "DQ-010", "dataset": "intake.patients", "target": "dob", "cond": "dob >= '1900-01-01'::date AND dob <= CURRENT_DATE", "sev": "CRITICAL", "thresh": "100%", "det": "Date boundary verification", "rem": "Reject negative age or future date of birth", "owner": "Lead Registrar"},
    {"id": "DQ-011", "dataset": "intake.patients", "target": "gender", "cond": "gender IN ('MALE', 'FEMALE', 'TRANSGENDER', 'OTHER')", "sev": "CRITICAL", "thresh": "100%", "det": "Enum domain check", "rem": "Restrict input to standardized gender enum", "owner": "Lead Registrar"},
    {"id": "DQ-012", "dataset": "intake.patient_identifiers", "target": "reference_code", "cond": "length(reference_code) >= 6", "sev": "HIGH", "thresh": "100%", "det": "String length constraint", "rem": "Reject truncated national identity strings", "owner": "ABDM Lead"},
    {"id": "DQ-013", "dataset": "intake.patient_contacts", "target": "phone_number", "cond": "phone_number ~ '^\\+91[6-9][0-9]{9}$'", "sev": "CRITICAL", "thresh": "99.9%", "det": "Indian mobile number format regex", "rem": "Prompt user for valid 10-digit mobile number", "owner": "Lead Registrar"},
    {"id": "DQ-014", "dataset": "intake.patient_addresses", "target": "pin_code", "cond": "pin_code ~ '^560[0-9]{3}$'", "sev": "HIGH", "thresh": "99.5%", "det": "Bengaluru postal code regex", "rem": "Verify ward and postal code concordance", "owner": "GIS Specialist"},
    {"id": "DQ-015", "dataset": "intake.consent_records", "target": "valid_until", "cond": "valid_until >= granted_at", "sev": "CRITICAL", "thresh": "100%", "det": "Temporal sequence check", "rem": "Ensure consent expiry is in the future", "owner": "DPO"},
    {"id": "DQ-016", "dataset": "intake.tokens", "target": "sequence_number", "cond": "sequence_number >= 1 AND sequence_number <= 2000", "sev": "CRITICAL", "thresh": "100%", "det": "Daily sequence range check", "rem": "Advisory lock prevents duplicate sequence numbers", "owner": "Queue Lead"},
    {"id": "DQ-017", "dataset": "intake.triage_assessments", "target": "acuity_score", "cond": "acuity_score IN ('RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE')", "sev": "CRITICAL", "thresh": "100%", "det": "SATS protocol category validation", "rem": "Restrict nurse entry to verified SATS scale", "owner": "Nursing Lead"},
    {"id": "DQ-018", "dataset": "intake.patient_vitals", "target": "systolic_bp, diastolic_bp", "cond": "systolic_bp > diastolic_bp AND systolic_bp BETWEEN 40 AND 280 AND diastolic_bp BETWEEN 20 AND 180", "sev": "CRITICAL", "thresh": "100%", "det": "Physiological cross-validation check", "rem": "Reject physiologically impossible blood pressure pairs", "owner": "CMO"},
    {"id": "DQ-019", "dataset": "intake.danger_alerts", "target": "status", "cond": "status IN ('ACTIVE', 'ACKNOWLEDGED', 'RESOLVED', 'FALSE_ALARM')", "sev": "CRITICAL", "thresh": "100%", "det": "State transition check", "rem": "Enforce doctor sign-off to resolve clinical panic alert", "owner": "Clinical Safety Lead"},
    {"id": "DQ-020", "dataset": "clinical.clinical_encounters", "target": "end_time", "cond": "end_time >= start_time", "sev": "CRITICAL", "thresh": "100%", "det": "Encounter chronology check", "rem": "Ensure consultation end timestamp post-dates start", "owner": "CMO"},
    {"id": "DQ-021", "dataset": "clinical.clinical_notes", "target": "clinical_narrative", "cond": "length(trim(clinical_narrative)) >= 10", "sev": "HIGH", "thresh": "99.0%", "det": "Minimum clinical narrative length check", "rem": "Prompt physician to provide meaningful clinical note", "owner": "Medical Director"},
    {"id": "DQ-022", "dataset": "clinical.diagnoses", "target": "icd10_code", "cond": "icd10_code ~ '^[A-Z][0-9]{2}(\\.[0-9]{1,2})?$'", "sev": "CRITICAL", "thresh": "100%", "det": "WHO ICD-10 syntax check", "rem": "Restrict diagnostic selection to verified ICD-10 catalog", "owner": "Public Health Director"},
    {"id": "DQ-023", "dataset": "clinical.prescriptions", "target": "prescription_items", "cond": "COUNT(prescription_items) >= 1", "sev": "CRITICAL", "thresh": "100%", "det": "Child item existence check", "rem": "Prevent empty prescription header without line items", "owner": "Chief Pharmacist"},
    {"id": "DQ-024", "dataset": "clinical.lab_order_items", "target": "loinc_code", "cond": "loinc_code ~ '^[0-9]{3,5}-[0-9]$'", "sev": "CRITICAL", "thresh": "100%", "det": "LOINC standard syntax check", "rem": "Enforce standard LOINC catalog mapping", "owner": "Pathology Head"},
    {"id": "DQ-025", "dataset": "clinical.lab_results", "target": "numeric_value", "cond": "numeric_value >= 0 WHEN unit_of_measure IN ('mg/dL', 'g/dL', 'cells/mcL')", "sev": "CRITICAL", "thresh": "100%", "det": "Non-negative physiological observation check", "rem": "Reject negative lab test concentrations", "owner": "Pathology Head"},
    {"id": "DQ-026", "dataset": "clinical.teleconsultations", "target": "session_duration_seconds", "cond": "session_duration_seconds >= 0 AND session_duration_seconds <= 7200", "sev": "HIGH", "thresh": "100%", "det": "Session duration sanity check", "rem": "Flag consultations exceeding 2 hours for audit", "owner": "Telemedicine Director"},
    {"id": "DQ-027", "dataset": "pharmacy.formulary_drugs", "target": "generic_name", "cond": "length(trim(generic_name)) >= 3", "sev": "CRITICAL", "thresh": "100%", "det": "Formulary drug string check", "rem": "Prevent empty or single-letter drug names", "owner": "Essential Drugs Lead"},
    {"id": "DQ-028", "dataset": "pharmacy.pharmacy_batches", "target": "expiry_date", "cond": "expiry_date > manufacture_date", "sev": "CRITICAL", "thresh": "100%", "det": "Shelf-life chronology check", "rem": "Reject batch where expiry precedes manufacture", "owner": "Procurement Lead"},
    {"id": "DQ-029", "dataset": "pharmacy.clinic_stock", "target": "quantity_on_hand", "cond": "quantity_on_hand >= 0", "sev": "CRITICAL", "thresh": "100%", "det": "Non-negative physical stock check", "rem": "Prevent negative inventory balance under all conditions", "owner": "Chief Pharmacist"},
    {"id": "DQ-030", "dataset": "pharmacy.dispensations", "target": "dispensed_at", "cond": "dispensed_at >= created_at", "sev": "CRITICAL", "thresh": "100%", "det": "Dispensing timestamp chronological check", "rem": "Validate timestamp sequence on dispense event", "owner": "Chief Pharmacist"},
    {"id": "DQ-031", "dataset": "pharmacy.stock_movements", "target": "quantity_change", "cond": "quantity_change != 0", "sev": "CRITICAL", "thresh": "100%", "det": "Zero-movement prohibition check", "rem": "Reject stock movements with zero quantity delta", "owner": "CFO & Audit Lead"},
    {"id": "DQ-032", "dataset": "pharmacy.drug_indents", "target": "indent_status", "cond": "indent_status IN ('DRAFT', 'SUBMITTED', 'APPROVED', 'DISPATCHED', 'RECEIVED', 'CANCELLED')", "sev": "CRITICAL", "thresh": "100%", "det": "State transition lifecycle verification", "rem": "Enforce sequential warehouse requisition lifecycle", "owner": "Warehouse Manager"},
    {"id": "DQ-033", "dataset": "pharmacy.cold_chain_devices", "target": "min_safe_temp, max_safe_temp", "cond": "min_safe_temp < max_safe_temp AND min_safe_temp >= -30.0 AND max_safe_temp <= 15.0", "sev": "CRITICAL", "thresh": "100%", "det": "Temperature threshold sanity check", "rem": "Enforce standard +2C to +8C vaccine bounds", "owner": "Immunization Officer"},
    {"id": "DQ-034", "dataset": "pharmacy.cold_chain_telemetry", "target": "temperature_celsius", "cond": "temperature_celsius BETWEEN -40.0 AND 50.0", "sev": "CRITICAL", "thresh": "99.99%", "det": "IoT sensor reading boundary check", "rem": "Filter hardware sensor fault spikes (e.g. -999.0C)", "owner": "IoT Tech Lead"},
    {"id": "DQ-035", "dataset": "continuity.referrals", "target": "referral_urgency", "cond": "referral_urgency IN ('ROUTINE', 'PRIORITY', 'EMERGENCY')", "sev": "CRITICAL", "thresh": "100%", "det": "Referral category enum check", "rem": "Require urgency classification on all hospital transfers", "owner": "DHO"},
    {"id": "DQ-036", "dataset": "continuity.ncd_episodes", "target": "condition_category", "cond": "condition_category IN ('HYPERTENSION', 'TYPE_2_DIABETES', 'COPD', 'CARDIOVASCULAR', 'CANCER_SCREENING')", "sev": "CRITICAL", "thresh": "100%", "det": "NCD category check", "rem": "Enforce standard national NCD program categories", "owner": "NCD Officer"},
    {"id": "DQ-037", "dataset": "continuity.follow_up_schedules", "target": "scheduled_date", "cond": "scheduled_date >= CURRENT_DATE - INTERVAL '1 day'", "sev": "HIGH", "thresh": "100%", "det": "Follow up future date validation", "rem": "Prevent scheduling clinic review dates in the past", "owner": "Clinic Ops Lead"},
    {"id": "DQ-038", "dataset": "continuity.notifications", "target": "channel", "cond": "channel IN ('SMS', 'WHATSAPP', 'VOICE_CALL', 'IN_APP')", "sev": "CRITICAL", "thresh": "100%", "det": "Communication channel verification", "rem": "Restrict outbound dispatch to approved telecom channels", "owner": "Comms Lead"},
    {"id": "DQ-039", "dataset": "continuity.grievances", "target": "sla_deadline", "cond": "sla_deadline >= filed_at", "sev": "CRITICAL", "thresh": "100%", "det": "Sakala statutory SLA deadline check", "rem": "Automatically calculate statutory SLA deadline on filing", "owner": "Sakala Officer"},
    {"id": "DQ-040", "dataset": "continuity.helpdesk_tickets", "target": "ticket_status", "cond": "ticket_status IN ('OPEN', 'ASSIGNED', 'IN_PROGRESS', 'RESOLVED', 'CLOSED')", "sev": "HIGH", "thresh": "100%", "det": "ITSM ticket status check", "rem": "Enforce standard IT support lifecycle", "owner": "IT Lead"},
    {"id": "DQ-041", "dataset": "audit.audit_events", "target": "previous_state_hash, new_state_hash", "cond": "length(previous_state_hash) = 64 AND length(new_state_hash) = 64", "sev": "CRITICAL", "thresh": "100%", "det": "SHA-256 HMAC hash length verification", "rem": "Halt mutation if cryptographic hash chaining fails", "owner": "CISO"},
    {"id": "DQ-042", "dataset": "sync.offline_mutation_log", "target": "sync_version", "cond": "sync_version >= 1", "sev": "CRITICAL", "thresh": "100%", "det": "Monotonic version sequence check", "rem": "Reject non-monotonic sequence vectors from edge nodes", "owner": "Edge Architect"},
    {"id": "DQ-043", "dataset": "sync.abdm_artifacts", "target": "health_info_type", "cond": "health_info_type IN ('OPConsultation', 'Prescription', 'DiagnosticReport', 'ImmunizationRecord')", "sev": "CRITICAL", "thresh": "100%", "det": "ABDM standard document type check", "rem": "Enforce national FHIR document profile taxonomy", "owner": "ABDM Lead"},
    {"id": "DQ-044", "dataset": "clinical.prescription_items", "target": "duration_days", "cond": "duration_days >= 1 AND duration_days <= 90", "sev": "HIGH", "thresh": "100%", "det": "Prescription duration bounds check", "rem": "Require clinical override justification for prescriptions > 90 days", "owner": "Chief Pharmacist"},
    {"id": "DQ-045", "dataset": "intake.patient_vitals", "target": "spo2_percentage", "cond": "spo2_percentage BETWEEN 50.0 AND 100.0", "sev": "CRITICAL", "thresh": "100%", "det": "Pulse oximeter physiological range check", "rem": "Reject SpO2 values exceeding 100% or below 50%", "owner": "CMO"},
    {"id": "DQ-046", "dataset": "intake.patient_vitals", "target": "pulse_rate_bpm", "cond": "pulse_rate_bpm BETWEEN 30 AND 250", "sev": "CRITICAL", "thresh": "100%", "det": "Pulse rate physiological range check", "rem": "Reject impossible heart rates outside 30-250 bpm", "owner": "CMO"},
    {"id": "DQ-047", "dataset": "intake.patient_vitals", "target": "temperature_fahrenheit", "cond": "temperature_fahrenheit BETWEEN 90.0 AND 108.0", "sev": "CRITICAL", "thresh": "100%", "det": "Body temperature physiological range check", "rem": "Verify clinical thermometer reading bounds", "owner": "CMO"},
    {"id": "DQ-048", "dataset": "pharmacy.dispensation_items", "target": "quantity_dispensed", "cond": "quantity_dispensed > 0", "sev": "CRITICAL", "thresh": "100%", "det": "Positive dispensed quantity check", "rem": "Prevent zero or negative quantity in dispensing items", "owner": "Chief Pharmacist"},
    {"id": "DQ-049", "dataset": "identity.facilities", "target": "ward_number", "cond": "ward_number BETWEEN 1 AND 243", "sev": "CRITICAL", "thresh": "100%", "det": "BBMP administrative ward range check", "rem": "Validate ward against gazetted municipal list", "owner": "GIS Specialist"},
    {"id": "DQ-050", "dataset": "identity.auth_users", "target": "account_status", "cond": "account_status IN ('ACTIVE', 'SUSPENDED', 'LOCKED', 'DEACTIVATED', 'PENDING_ACTIVATION')", "sev": "CRITICAL", "thresh": "100%", "det": "Account lifecycle status enum check", "rem": "Enforce valid user account lifecycle transitions", "owner": "CISO"}
]

DQ_MAP = {r["id"]: r for r in DQ_RULES}

# -----------------------------------------------------------------------------
# 5. 25 DATA LINEAGE PATHWAYS (LINEAGE-001 to LINEAGE-025)
# -----------------------------------------------------------------------------
LINEAGE_PATHS = [
    {
        "id": "LINEAGE-001",
        "name": "Staff Onboarding & Identity Provisioning Lineage",
        "source": "BBMP HR Administrative Portal",
        "ingestion": "REST HTTPS JSON with mTLS",
        "validation": "KMC Medical Registration Verification & Email/Mobile Validation (DQ-001, DQ-008)",
        "target_table": "identity.auth_users, identity.user_credentials, identity.user_roles",
        "transformation": "Argon2id password hashing + Blind index derivation on phone",
        "business_rule": "Every clinician assigned role must hold active KMC/NMC registration number",
        "downstream": "Auth Service -> Doctor EMR Console -> Staff Duty Dashboard",
        "classification": "CLASS-004",
        "retention": "RETENTION-006"
    },
    {
        "id": "LINEAGE-002",
        "name": "Biometric Clock-in & Staff Shift Duty Lineage",
        "source": "Clinic Edge Biometric Scanner / Tablet Camera",
        "ingestion": "Encrypted MQTT WebSocket push",
        "validation": "Subnet IP check & facial biometric vector comparison",
        "target_table": "identity.staff_shifts",
        "transformation": "Clock-in punch time rounded to nearest minute + shift status set to ACTIVE",
        "business_rule": "Clock-in valid within 30 minutes of scheduled shift start",
        "downstream": "Staff Attendance Dashboard -> Duty Roster SLA Monitor -> Payroll Link",
        "classification": "CLASS-002",
        "retention": "RETENTION-002"
    },
    {
        "id": "LINEAGE-003",
        "name": "Facility Metadata & Geo-boundary Lineage",
        "source": "Karnataka Urban Development Department (UDD) GIS",
        "ingestion": "Shapefile / GeoJSON ETL ingestion",
        "validation": "Bengaluru municipal bounding box validation (DQ-007, DQ-049)",
        "target_table": "identity.facilities, identity.facility_rooms",
        "transformation": "Coordinate projection to WGS84 + Ward polygon spatial join",
        "business_rule": "Every clinic must resolve to exactly one BBMP ward and zone",
        "downstream": "Clinic Locator Public Portal -> GIS Disease Heatmap -> Supply Chain Logistics",
        "classification": "CLASS-001",
        "retention": "RETENTION-006"
    },
    {
        "id": "LINEAGE-004",
        "name": "Citizen Intake & Master Patient Demographics Lineage",
        "source": "Clinic Reception Desk / Citizen Mobile App",
        "ingestion": "Reception UI Form / ABDM QR Scan",
        "validation": "Age bounds, Indian mobile format, and deduplication blind index (DQ-010, DQ-013)",
        "target_table": "intake.patients, intake.patient_identifiers, intake.patient_contacts, intake.patient_addresses",
        "transformation": "Surrogate UUIDv7 allocation + Column-level AES-256-GCM encryption on PII",
        "business_rule": "Patient uniquely identified by composite of phone hash, DOB, and gender if ABHA absent",
        "downstream": "Doctor Consultation EMR -> Master Patient Index -> ABDM Gateway",
        "classification": "CLASS-004",
        "retention": "RETENTION-001"
    },
    {
        "id": "LINEAGE-005",
        "name": "DPDP Citizen Consent & ABDM Health Artifact Lineage",
        "source": "Citizen Consent Terminal / ABDM Consent Manager",
        "ingestion": "ABDM M2 Gateway Webhook / OTP Challenge",
        "validation": "Cryptographic signature validation + validity window checks (DQ-015, DQ-043)",
        "target_table": "intake.consent_records, sync.abdm_artifacts",
        "transformation": "Consent artifact JSON serialization + SHA-256 HMAC digital seal",
        "business_rule": "No clinical data shared externally without active consent record",
        "downstream": "Policy Enforcement Point (PEP) -> ABDM Document Bridge -> DPO Compliance Audit",
        "classification": "CLASS-004",
        "retention": "RETENTION-005"
    },
    {
        "id": "LINEAGE-006",
        "name": "Daily Intake Token & Queue Stage Progression Lineage",
        "source": "Reception Kiosk / Token Printer Hardware",
        "ingestion": "Local edge queue controller API",
        "validation": "Daily sequence range check & active token duplicate check (DQ-016)",
        "target_table": "intake.tokens, intake.queue_entries",
        "transformation": "Advisory lock sequential numbering (e.g. A-042) + initial TRIAGE stage creation",
        "business_rule": "Daily token valid only for date of issue at issuing clinic facility",
        "downstream": "Waiting Hall Display TV -> Nurse Station Worklist -> Doctor Call Queue",
        "classification": "CLASS-002",
        "retention": "RETENTION-007"
    },
    {
        "id": "LINEAGE-007",
        "name": "Nursing Triage Vitals & Clinical Danger Alert Lineage",
        "source": "Nurse Station Bluetooth Blood Pressure / SpO2 Sensor & Tablet",
        "ingestion": "BLE Peripheral Sync / Touchscreen Input",
        "validation": "Physiological range checks (DQ-018, DQ-045, DQ-046, DQ-047)",
        "target_table": "intake.triage_assessments, intake.patient_vitals, intake.danger_alerts",
        "transformation": "SATS score calculation + Automated threshold evaluation for immediate doctor alert",
        "business_rule": "Systolic BP >= 180 or SpO2 <= 92% triggers mandatory instant danger alert",
        "downstream": "Doctor Consultation Workstation Alert Banner -> Emergency Triage Priority Queue",
        "classification": "CLASS-003",
        "retention": "RETENTION-001"
    },
    {
        "id": "LINEAGE-008",
        "name": "Doctor Clinical Consultation Encounter & SOAP Notes Lineage",
        "source": "Doctor Consultation Workstation",
        "ingestion": "EMR Form Submit via HTTPS mTLS",
        "validation": "Mandatory diagnosis check + narrative length check (DQ-020, DQ-021)",
        "target_table": "clinical.clinical_encounters, clinical.clinical_notes",
        "transformation": "Doctor digital signature cryptographic token embedding + SOAP note JSON packaging",
        "business_rule": "Signed encounter becomes permanently immutable; corrections require addendum",
        "downstream": "Citizen Health Record -> Referral Dossier Service -> Clinical NLP Summarizer",
        "classification": "CLASS-005",
        "retention": "RETENTION-001"
    },
    {
        "id": "LINEAGE-009",
        "name": "Diagnostic Coding & Disease Surveillance Lineage",
        "source": "Doctor Consultation Workstation Diagnostic Selector",
        "ingestion": "Coded Search Input",
        "validation": "WHO ICD-10 standard code validation (DQ-022)",
        "target_table": "clinical.diagnoses",
        "transformation": "Mapping ICD-10 code to IDSP communicable category + NCD chronic classification",
        "business_rule": "Communicable diseases (Dengue, Cholera) trigger automated public health surveillance rollup",
        "downstream": "IDSP Outbreak Early Warning Engine -> Ward Epidemic Heatmap -> HMIS Monthly Return",
        "classification": "CLASS-003",
        "retention": "RETENTION-001"
    },
    {
        "id": "LINEAGE-010",
        "name": "Electronic Prescription & Dosage Safety Lineage",
        "source": "Doctor Consultation EMR Prescribing Module",
        "ingestion": "Prescription Form Submit",
        "validation": "Formulary drug active check + dosage ceiling validation (DQ-023, DQ-044)",
        "target_table": "clinical.prescriptions, clinical.prescription_items",
        "transformation": "Prescription hash generation + Drug-Drug Interaction evaluation + Pharmacy queue routing",
        "business_rule": "Prescriptions valid for 7 days from date of issuance for dispensing",
        "downstream": "Pharmacy Dispensing Queue -> Citizen Mobile SMS Link -> Antibiotic Stewardship Monitor",
        "classification": "CLASS-003",
        "retention": "RETENTION-003"
    },
    {
        "id": "LINEAGE-011",
        "name": "Laboratory Investigation Order to Result Verification Lineage",
        "source": "Lab Technician Workstation / Semi-automated Hematology Analyzer",
        "ingestion": "ASTM / HL7 interface via RS232-to-Ethernet gateway",
        "validation": "LOINC syntax validation + non-negative numeric boundary check (DQ-024, DQ-025)",
        "target_table": "clinical.lab_orders, clinical.lab_order_items, clinical.lab_results",
        "transformation": "Parser converts analyzer ASTM packets to structured observation rows + panic flag evaluation",
        "business_rule": "Panic lab value (e.g. Platelets < 20,000) generates automated urgent SMS to doctor",
        "downstream": "Doctor EMR Results Viewer -> ABDM Diagnostic Report Bundle -> Citizen Portal",
        "classification": "CLASS-003",
        "retention": "RETENTION-004"
    },
    {
        "id": "LINEAGE-012",
        "name": "Doctor-to-Specialist Teleconsultation Session Lineage",
        "source": "Clinic Telemedicine Chamber WebRTC Client",
        "ingestion": "WebRTC Signaling Gateway",
        "validation": "Specialist credential check + session duration boundaries (DQ-026)",
        "target_table": "clinical.teleconsultations",
        "transformation": "WebRTC session metadata recording + joint clinical consultation summary",
        "business_rule": "Teleconsultation conducted strictly in compliance with MCI Telemedicine Guidelines",
        "downstream": "Specialist Utilization Dashboard -> Referral Avoidance Analytics",
        "classification": "CLASS-003",
        "retention": "RETENTION-016"
    },
    {
        "id": "LINEAGE-013",
        "name": "Master Formulary Drug Catalog & NLEM Lineage",
        "source": "BBMP Essential Drugs Committee Administration Portal",
        "ingestion": "Admin UI Batch Upload",
        "validation": "ATC category check & generic salt name validation (DQ-027)",
        "target_table": "pharmacy.formulary_drugs, pharmacy.drug_categories",
        "transformation": "Formulary version increment + Global edge broadcast push to all 450 clinic nodes",
        "business_rule": "Only NLEM approved drugs available for outpatient primary care prescribing",
        "downstream": "Doctor Prescribing Autocomplete -> Pharmacy Inventory Catalog -> Procurement Indent",
        "classification": "CLASS-001",
        "retention": "RETENTION-009"
    },
    {
        "id": "LINEAGE-014",
        "name": "Warehouse Goods Inward & Drug Batch Onboarding Lineage",
        "source": "BBMP Central Medical Stores Warehouse Management System (WMS)",
        "ingestion": "Warehouse Barcode Dispatch Webhook",
        "validation": "Shelf life chronology check & procurement voucher verification (DQ-028)",
        "target_table": "pharmacy.pharmacy_batches, pharmacy.clinic_stock",
        "transformation": "Batch onboarding + FEFO sorting index assignment + clinic stock balance increment",
        "business_rule": "Batches with shelf life < 6 months rejected at inward dock",
        "downstream": "Pharmacy Dispensing POS -> Batch Near-Expiry Alert -> Central Procurement Analytics",
        "classification": "CLASS-002",
        "retention": "RETENTION-009"
    },
    {
        "id": "LINEAGE-015",
        "name": "Pharmacy Drug Dispensation & Double-Entry Stock Decrement Lineage",
        "source": "Pharmacy Dispensing Counter Barcode Scanner",
        "ingestion": "Point of Sale UI Event",
        "validation": "Non-negative stock check + positive quantity validation (DQ-029, DQ-031, DQ-048)",
        "target_table": "pharmacy.dispensations, pharmacy.dispensation_items, pharmacy.clinic_stock, pharmacy.stock_movements",
        "transformation": "Pessimistic FEFO batch deduction + atomic double-entry movement ledger write",
        "business_rule": "Physical stock balance MUST NEVER drop below zero under any transaction",
        "downstream": "Stockout Early Warning System -> Citizen SMS Receipt -> CAG Financial Audit Ledger",
        "classification": "CLASS-003",
        "retention": "RETENTION-003"
    },
    {
        "id": "LINEAGE-016",
        "name": "Clinic Drug Indent Requisition to Warehouse Lineage",
        "source": "Clinic Pharmacist Indent Terminal",
        "ingestion": "Requisition Workflow API",
        "validation": "AMC calculation check + MOIC digital approval validation (DQ-032)",
        "target_table": "pharmacy.drug_indents, pharmacy.indent_items",
        "transformation": "Stock depletion velocity calculation + Suggested reorder quantity generation",
        "business_rule": "Indents auto-calculated based on 30-day average monthly consumption (AMC)",
        "downstream": "Central Warehouse Picking List -> Supply Chain Lead-Time Analytics",
        "classification": "CLASS-002",
        "retention": "RETENTION-009"
    },
    {
        "id": "LINEAGE-017",
        "name": "Cold-Chain IoT Temperature Telemetry & Excursion Alert Lineage",
        "source": "Vaccine Refrigerator IoT Gateway (Sensors in ILR units)",
        "ingestion": "MQTT Message Broker -> Apache Kafka Stream Pipeline",
        "validation": "IoT sensor range checks & boundary filtering (DQ-033, DQ-034)",
        "target_table": "pharmacy.cold_chain_devices, pharmacy.cold_chain_telemetry, intake.danger_alerts",
        "transformation": "Time-series stream aggregation + Moving average calculation + Alert trigger on excursion",
        "business_rule": "Temperature > +8C or < +2C for > 15 minutes triggers emergency SMS escalation to MOIC",
        "downstream": "Cold Chain Real-Time Dashboard -> Vaccine Wastage Risk Model -> UIP Audit Log",
        "classification": "CLASS-002",
        "retention": "RETENTION-008"
    },
    {
        "id": "LINEAGE-018",
        "name": "Hospital Referral Dossier & Counter-Referral Feedback Lineage",
        "source": "Referring Namma Clinic Doctor -> Receiving Hospital Specialty EMR",
        "ingestion": "Inter-Hospital Referral Exchange API",
        "validation": "Target hospital existence check & clinical transfer summary validation (DQ-035)",
        "target_table": "continuity.referrals, continuity.referral_counter_notes",
        "transformation": "Referral dossier bundling (clinical encounter, vitals, lab results) -> ABDM FHIR Referral Bundle",
        "business_rule": "Emergency referrals automatically dispatch ambulance alert and bed reservation request",
        "downstream": "Receiving Hospital Triage Station -> Primary Doctor Follow-up Inbox -> Referral KPI Report",
        "classification": "CLASS-003",
        "retention": "RETENTION-010"
    },
    {
        "id": "LINEAGE-019",
        "name": "Longitudinal NCD Care Episode & Risk Stratification Lineage",
        "source": "Doctor Consultation EMR / ACD Screening Camp",
        "ingestion": "NCD Registry Enrollment Form",
        "validation": "Confirmed diagnosis code check & condition category verification (DQ-036)",
        "target_table": "continuity.ncd_episodes, continuity.follow_up_schedules",
        "transformation": "Cardio-metabolic risk score calculation + Automated 30-day review schedule generation",
        "business_rule": "Enrolled NCD citizens must be scheduled for monthly clinical vitals and medication review",
        "downstream": "ASHA Community Line-List -> NP-NCD National Portal -> Population Health Analytics",
        "classification": "CLASS-003",
        "retention": "RETENTION-013"
    },
    {
        "id": "LINEAGE-020",
        "name": "Care Continuity Follow-up Reminder & Outreach Lineage",
        "source": "Encounter Discharge Workflow Scheduler",
        "ingestion": "Automated Cron Scheduler Engine",
        "validation": "Future date validation & citizen opt-in verification (DQ-037)",
        "target_table": "continuity.follow_up_schedules, continuity.notifications",
        "transformation": "Reminder dispatch timeline calculation (T-3 days, T-1 day, T-day) -> SMS/WhatsApp template rendering",
        "business_rule": "Citizen missing scheduled review by > 7 days flagged for ASHA home visit",
        "downstream": "Citizen SMS Gateway -> ASHA Mobile Outreach App -> Clinic Daily Appointment Roster",
        "classification": "CLASS-003",
        "retention": "RETENTION-001"
    },
    {
        "id": "LINEAGE-021",
        "name": "Citizen Communication Dispatch & DLR Reconciliation Lineage",
        "source": "Notification Engine Trigger (Appointments, Prescriptions, Lab Alerts)",
        "ingestion": "Telecom Aggregator REST API (Karix / ValueFirst)",
        "validation": "Indian mobile number validation & approved telecom template check (DQ-038)",
        "target_table": "continuity.notifications",
        "transformation": "Message text token substitution + Delivery receipt webhook status update",
        "business_rule": "Transactional clinical messages exempt from TRAI promotional DND restrictions",
        "downstream": "Citizen Mobile Device -> Telecom SLA Report -> Communication Cost Accounting",
        "classification": "CLASS-003",
        "retention": "RETENTION-015"
    },
    {
        "id": "LINEAGE-022",
        "name": "Sakala Citizen Grievance & SLA Escalation Lineage",
        "source": "Sakala Portal / 1533 BBMP Helpline / Clinic QR Form",
        "ingestion": "Karnataka Sakala API Gateway",
        "validation": "Service code check & statutory deadline computation (DQ-039)",
        "target_table": "continuity.grievances",
        "transformation": "Sakala ticket generation + Automatic assignment to Ward MOIC based on clinic code",
        "business_rule": "Grievance unresolved after 7 days automatically escalates to Chief Health Officer",
        "downstream": "MOIC Grievance Workbench -> Sakala State Dashboard -> Public Grievance Scorecard",
        "classification": "CLASS-002",
        "retention": "RETENTION-014"
    },
    {
        "id": "LINEAGE-023",
        "name": "Facility IT Hardware & Cold-Chain Breakdown Ticket Lineage",
        "source": "Clinic Staff / Automated Cold Chain Sensor Alert",
        "ingestion": "ITSM Portal Form / Automated Failure Webhook",
        "validation": "Asset serial number validation & vendor SLA category check (DQ-040)",
        "target_table": "continuity.helpdesk_tickets",
        "transformation": "Severity assignment + Vendor dispatch dispatch notification via SMS/Email",
        "business_rule": "Cold-chain ILR breakdown requires technician on-site response within 4 hours",
        "downstream": "Field Engineer Dispatch App -> Hardware Uptime Dashboard -> Vendor Penalty Ledger",
        "classification": "CLASS-002",
        "retention": "RETENTION-019"
    },
    {
        "id": "LINEAGE-024",
        "name": "Cryptographic WORM Audit Event & Tamper Proofing Lineage",
        "source": "PostgreSQL Database Engine Triggers & Application Security Interceptors",
        "ingestion": "Transactional Append-Only Pipeline",
        "validation": "SHA-256 HMAC hash length & previous chain link check (DQ-041)",
        "target_table": "audit.audit_events",
        "transformation": "HMAC calculation using KMS secret key + Appending to immutable hash-chained partition",
        "business_rule": "Audit rows are write-once-read-many (WORM); updates and deletes strictly forbidden",
        "downstream": "SIEM (Splunk / Elastic) -> Forensic Investigation Queries -> ISO 27001 Compliance Audit",
        "classification": "CLASS-004",
        "retention": "RETENTION-006"
    },
    {
        "id": "LINEAGE-025",
        "name": "Clinic Edge Offline Mutation Journal & Cloud Reconciliation Lineage",
        "source": "Clinic Edge SQLite / Local PostgreSQL Database",
        "ingestion": "Encrypted Sync Agent Worker over HTTPS",
        "validation": "Sync sequence monotonic check & conflict vector validation (DQ-042)",
        "target_table": "sync.offline_mutation_log, All domain OLTP tables",
        "transformation": "Conflict resolution via Last-Write-Wins / Doctor-Wins rule + Replaying mutations to cloud tables",
        "business_rule": "Local edge writes must reconcile within 24 hours of connectivity restoration",
        "downstream": "Cloud Central Database -> Edge Sync Health Monitor -> Offline Continuity Report",
        "classification": "CLASS-003",
        "retention": "RETENTION-012"
    }
]

LINEAGE_MAP = {l["id"]: l for l in LINEAGE_PATHS}

if __name__ == "__main__":
    print(f"Loaded {len(FACTS)} Fact Tables (FACT-001..FACT-{len(FACTS):03d}).")
    print(f"Loaded {len(DIMENSIONS)} Dimension Tables (DIM-001..DIM-{len(DIMENSIONS):03d}).")
    print(f"Loaded {len(MEASURES)} Analytical Measures (MEASURE-001..MEASURE-{len(MEASURES):03d}).")
    print(f"Loaded {len(DQ_RULES)} Data Quality Rules (DQ-001..DQ-{len(DQ_RULES):03d}).")
    print(f"Loaded {len(LINEAGE_PATHS)} Data Lineage Pathways (LINEAGE-001..LINEAGE-{len(LINEAGE_PATHS):03d}).")
