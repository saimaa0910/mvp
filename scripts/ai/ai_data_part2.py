"""ai_data_part2.py - ML Features, Evaluation Metrics"""

FEATURES_ML = [   {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 7 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 7d Rolling #001',
        'id': 'FEATURE-ML-001',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_7d_rolling_001',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 30 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 30d Rolling #002',
        'id': 'FEATURE-ML-002',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_30d_rolling_002',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Historical supplier lead time in days for '
                       'replenishment indent',
        'display_title': 'Drug Lead Time Days #003',
        'id': 'FEATURE-ML-003',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_drug_lead_time_days_003',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Doses',
        'description': 'Current usable unexpired inventory doses at clinic '
                       'dispensary',
        'display_title': 'Clinic Stock on Hand Balance #004',
        'id': 'FEATURE-ML-004',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_stock_on_hand_balance_004',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Redis Cache'},
    {   'data_type': 'Integer Count',
        'description': 'Total registered patient encounters for the preceding '
                       'operational day',
        'display_title': 'Clinic Daily Patient Footfall #005',
        'id': 'FEATURE-ML-005',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_daily_patient_footfall_005',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Cases',
        'description': 'Total diagnosed febrile cases in the municipal ward '
                       'over last 72 hours',
        'display_title': 'Fever Syndrome Case Count 3d #006',
        'id': 'FEATURE-ML-006',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_fever_syndrome_case_count_3d_006',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Continuous mm',
        'description': 'Cumulative rainfall in mm across municipal zone over '
                       'last 14 days',
        'display_title': 'Rainfall Rolling Accumulation 14d #007',
        'id': 'FEATURE-ML-007',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_rainfall_rolling_accumulation_14d_007',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Continuous Celsius',
        'description': 'Mean daily temperature in Celsius over last 7 days',
        'display_title': 'Ambient Temperature Mean 7d #008',
        'id': 'FEATURE-ML-008',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_ambient_temperature_mean_7d_008',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Integer mmHg',
        'description': 'Mean systolic BP over past 3 outpatient visits',
        'display_title': 'Patient Systolic Blood Pressure Mean #009',
        'id': 'FEATURE-ML-009',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_systolic_blood_pressure_mean_009',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous mg/dL',
        'description': 'Latest recorded fasting blood glucose laboratory value',
        'display_title': 'Patient Fasting Blood Glucose #010',
        'id': 'FEATURE-ML-010',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_fasting_blood_glucose_010',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Number of days elapsed since scheduled chronic care '
                       'recall date',
        'display_title': 'Days Overdue for Clinical Follow-up #011',
        'id': 'FEATURE-ML-011',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_days_overdue_for_clinical_follow-up_011',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Years',
        'description': 'Chronological patient age in completed solar years',
        'display_title': 'Patient Age in Years #012',
        'id': 'FEATURE-ML-012',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_age_in_years_012',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Demographics'},
    {   'data_type': 'Integer Count',
        'description': 'Number of active diagnosed chronic conditions in '
                       'patient problem list',
        'display_title': 'Patient Chronic Comorbidity Count #013',
        'id': 'FEATURE-ML-013',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_chronic_comorbidity_count_013',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous Score',
        'description': 'Weighted clinical score based on respiratory rate, '
                       'pulse, and mental status',
        'display_title': 'Emergency Triage Danger Score #014',
        'id': 'FEATURE-ML-014',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_emergency_triage_danger_score_014',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Triage Form'},
    {   'data_type': 'Integer Count',
        'description': 'Total number of distinct pharmaceutical lines on '
                       'active prescription',
        'display_title': 'Prescription Item Count #015',
        'id': 'FEATURE-ML-015',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_prescription_item_count_015',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Prescribe API'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 7 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 7d Rolling #016',
        'id': 'FEATURE-ML-016',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_7d_rolling_016',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 30 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 30d Rolling #017',
        'id': 'FEATURE-ML-017',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_30d_rolling_017',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Historical supplier lead time in days for '
                       'replenishment indent',
        'display_title': 'Drug Lead Time Days #018',
        'id': 'FEATURE-ML-018',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_drug_lead_time_days_018',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Doses',
        'description': 'Current usable unexpired inventory doses at clinic '
                       'dispensary',
        'display_title': 'Clinic Stock on Hand Balance #019',
        'id': 'FEATURE-ML-019',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_stock_on_hand_balance_019',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Redis Cache'},
    {   'data_type': 'Integer Count',
        'description': 'Total registered patient encounters for the preceding '
                       'operational day',
        'display_title': 'Clinic Daily Patient Footfall #020',
        'id': 'FEATURE-ML-020',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_daily_patient_footfall_020',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Cases',
        'description': 'Total diagnosed febrile cases in the municipal ward '
                       'over last 72 hours',
        'display_title': 'Fever Syndrome Case Count 3d #021',
        'id': 'FEATURE-ML-021',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_fever_syndrome_case_count_3d_021',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Continuous mm',
        'description': 'Cumulative rainfall in mm across municipal zone over '
                       'last 14 days',
        'display_title': 'Rainfall Rolling Accumulation 14d #022',
        'id': 'FEATURE-ML-022',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_rainfall_rolling_accumulation_14d_022',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Continuous Celsius',
        'description': 'Mean daily temperature in Celsius over last 7 days',
        'display_title': 'Ambient Temperature Mean 7d #023',
        'id': 'FEATURE-ML-023',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_ambient_temperature_mean_7d_023',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Integer mmHg',
        'description': 'Mean systolic BP over past 3 outpatient visits',
        'display_title': 'Patient Systolic Blood Pressure Mean #024',
        'id': 'FEATURE-ML-024',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_systolic_blood_pressure_mean_024',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous mg/dL',
        'description': 'Latest recorded fasting blood glucose laboratory value',
        'display_title': 'Patient Fasting Blood Glucose #025',
        'id': 'FEATURE-ML-025',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_fasting_blood_glucose_025',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Number of days elapsed since scheduled chronic care '
                       'recall date',
        'display_title': 'Days Overdue for Clinical Follow-up #026',
        'id': 'FEATURE-ML-026',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_days_overdue_for_clinical_follow-up_026',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Years',
        'description': 'Chronological patient age in completed solar years',
        'display_title': 'Patient Age in Years #027',
        'id': 'FEATURE-ML-027',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_age_in_years_027',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Demographics'},
    {   'data_type': 'Integer Count',
        'description': 'Number of active diagnosed chronic conditions in '
                       'patient problem list',
        'display_title': 'Patient Chronic Comorbidity Count #028',
        'id': 'FEATURE-ML-028',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_chronic_comorbidity_count_028',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous Score',
        'description': 'Weighted clinical score based on respiratory rate, '
                       'pulse, and mental status',
        'display_title': 'Emergency Triage Danger Score #029',
        'id': 'FEATURE-ML-029',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_emergency_triage_danger_score_029',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Triage Form'},
    {   'data_type': 'Integer Count',
        'description': 'Total number of distinct pharmaceutical lines on '
                       'active prescription',
        'display_title': 'Prescription Item Count #030',
        'id': 'FEATURE-ML-030',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_prescription_item_count_030',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Prescribe API'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 7 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 7d Rolling #031',
        'id': 'FEATURE-ML-031',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_7d_rolling_031',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 30 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 30d Rolling #032',
        'id': 'FEATURE-ML-032',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_30d_rolling_032',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Historical supplier lead time in days for '
                       'replenishment indent',
        'display_title': 'Drug Lead Time Days #033',
        'id': 'FEATURE-ML-033',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_drug_lead_time_days_033',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Doses',
        'description': 'Current usable unexpired inventory doses at clinic '
                       'dispensary',
        'display_title': 'Clinic Stock on Hand Balance #034',
        'id': 'FEATURE-ML-034',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_stock_on_hand_balance_034',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Redis Cache'},
    {   'data_type': 'Integer Count',
        'description': 'Total registered patient encounters for the preceding '
                       'operational day',
        'display_title': 'Clinic Daily Patient Footfall #035',
        'id': 'FEATURE-ML-035',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_daily_patient_footfall_035',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Cases',
        'description': 'Total diagnosed febrile cases in the municipal ward '
                       'over last 72 hours',
        'display_title': 'Fever Syndrome Case Count 3d #036',
        'id': 'FEATURE-ML-036',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_fever_syndrome_case_count_3d_036',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Continuous mm',
        'description': 'Cumulative rainfall in mm across municipal zone over '
                       'last 14 days',
        'display_title': 'Rainfall Rolling Accumulation 14d #037',
        'id': 'FEATURE-ML-037',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_rainfall_rolling_accumulation_14d_037',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Continuous Celsius',
        'description': 'Mean daily temperature in Celsius over last 7 days',
        'display_title': 'Ambient Temperature Mean 7d #038',
        'id': 'FEATURE-ML-038',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_ambient_temperature_mean_7d_038',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Integer mmHg',
        'description': 'Mean systolic BP over past 3 outpatient visits',
        'display_title': 'Patient Systolic Blood Pressure Mean #039',
        'id': 'FEATURE-ML-039',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_systolic_blood_pressure_mean_039',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous mg/dL',
        'description': 'Latest recorded fasting blood glucose laboratory value',
        'display_title': 'Patient Fasting Blood Glucose #040',
        'id': 'FEATURE-ML-040',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_fasting_blood_glucose_040',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Number of days elapsed since scheduled chronic care '
                       'recall date',
        'display_title': 'Days Overdue for Clinical Follow-up #041',
        'id': 'FEATURE-ML-041',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_days_overdue_for_clinical_follow-up_041',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Years',
        'description': 'Chronological patient age in completed solar years',
        'display_title': 'Patient Age in Years #042',
        'id': 'FEATURE-ML-042',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_age_in_years_042',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Demographics'},
    {   'data_type': 'Integer Count',
        'description': 'Number of active diagnosed chronic conditions in '
                       'patient problem list',
        'display_title': 'Patient Chronic Comorbidity Count #043',
        'id': 'FEATURE-ML-043',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_chronic_comorbidity_count_043',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous Score',
        'description': 'Weighted clinical score based on respiratory rate, '
                       'pulse, and mental status',
        'display_title': 'Emergency Triage Danger Score #044',
        'id': 'FEATURE-ML-044',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_emergency_triage_danger_score_044',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Triage Form'},
    {   'data_type': 'Integer Count',
        'description': 'Total number of distinct pharmaceutical lines on '
                       'active prescription',
        'display_title': 'Prescription Item Count #045',
        'id': 'FEATURE-ML-045',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_prescription_item_count_045',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Prescribe API'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 7 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 7d Rolling #046',
        'id': 'FEATURE-ML-046',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_7d_rolling_046',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 30 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 30d Rolling #047',
        'id': 'FEATURE-ML-047',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_30d_rolling_047',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Historical supplier lead time in days for '
                       'replenishment indent',
        'display_title': 'Drug Lead Time Days #048',
        'id': 'FEATURE-ML-048',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_drug_lead_time_days_048',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Doses',
        'description': 'Current usable unexpired inventory doses at clinic '
                       'dispensary',
        'display_title': 'Clinic Stock on Hand Balance #049',
        'id': 'FEATURE-ML-049',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_stock_on_hand_balance_049',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Redis Cache'},
    {   'data_type': 'Integer Count',
        'description': 'Total registered patient encounters for the preceding '
                       'operational day',
        'display_title': 'Clinic Daily Patient Footfall #050',
        'id': 'FEATURE-ML-050',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_daily_patient_footfall_050',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Cases',
        'description': 'Total diagnosed febrile cases in the municipal ward '
                       'over last 72 hours',
        'display_title': 'Fever Syndrome Case Count 3d #051',
        'id': 'FEATURE-ML-051',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_fever_syndrome_case_count_3d_051',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Continuous mm',
        'description': 'Cumulative rainfall in mm across municipal zone over '
                       'last 14 days',
        'display_title': 'Rainfall Rolling Accumulation 14d #052',
        'id': 'FEATURE-ML-052',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_rainfall_rolling_accumulation_14d_052',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Continuous Celsius',
        'description': 'Mean daily temperature in Celsius over last 7 days',
        'display_title': 'Ambient Temperature Mean 7d #053',
        'id': 'FEATURE-ML-053',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_ambient_temperature_mean_7d_053',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Integer mmHg',
        'description': 'Mean systolic BP over past 3 outpatient visits',
        'display_title': 'Patient Systolic Blood Pressure Mean #054',
        'id': 'FEATURE-ML-054',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_systolic_blood_pressure_mean_054',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous mg/dL',
        'description': 'Latest recorded fasting blood glucose laboratory value',
        'display_title': 'Patient Fasting Blood Glucose #055',
        'id': 'FEATURE-ML-055',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_fasting_blood_glucose_055',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Number of days elapsed since scheduled chronic care '
                       'recall date',
        'display_title': 'Days Overdue for Clinical Follow-up #056',
        'id': 'FEATURE-ML-056',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_days_overdue_for_clinical_follow-up_056',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Years',
        'description': 'Chronological patient age in completed solar years',
        'display_title': 'Patient Age in Years #057',
        'id': 'FEATURE-ML-057',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_age_in_years_057',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Demographics'},
    {   'data_type': 'Integer Count',
        'description': 'Number of active diagnosed chronic conditions in '
                       'patient problem list',
        'display_title': 'Patient Chronic Comorbidity Count #058',
        'id': 'FEATURE-ML-058',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_chronic_comorbidity_count_058',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous Score',
        'description': 'Weighted clinical score based on respiratory rate, '
                       'pulse, and mental status',
        'display_title': 'Emergency Triage Danger Score #059',
        'id': 'FEATURE-ML-059',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_emergency_triage_danger_score_059',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Triage Form'},
    {   'data_type': 'Integer Count',
        'description': 'Total number of distinct pharmaceutical lines on '
                       'active prescription',
        'display_title': 'Prescription Item Count #060',
        'id': 'FEATURE-ML-060',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_prescription_item_count_060',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Prescribe API'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 7 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 7d Rolling #061',
        'id': 'FEATURE-ML-061',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_7d_rolling_061',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 30 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 30d Rolling #062',
        'id': 'FEATURE-ML-062',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_30d_rolling_062',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Historical supplier lead time in days for '
                       'replenishment indent',
        'display_title': 'Drug Lead Time Days #063',
        'id': 'FEATURE-ML-063',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_drug_lead_time_days_063',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Doses',
        'description': 'Current usable unexpired inventory doses at clinic '
                       'dispensary',
        'display_title': 'Clinic Stock on Hand Balance #064',
        'id': 'FEATURE-ML-064',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_stock_on_hand_balance_064',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Redis Cache'},
    {   'data_type': 'Integer Count',
        'description': 'Total registered patient encounters for the preceding '
                       'operational day',
        'display_title': 'Clinic Daily Patient Footfall #065',
        'id': 'FEATURE-ML-065',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_daily_patient_footfall_065',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Cases',
        'description': 'Total diagnosed febrile cases in the municipal ward '
                       'over last 72 hours',
        'display_title': 'Fever Syndrome Case Count 3d #066',
        'id': 'FEATURE-ML-066',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_fever_syndrome_case_count_3d_066',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Continuous mm',
        'description': 'Cumulative rainfall in mm across municipal zone over '
                       'last 14 days',
        'display_title': 'Rainfall Rolling Accumulation 14d #067',
        'id': 'FEATURE-ML-067',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_rainfall_rolling_accumulation_14d_067',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Continuous Celsius',
        'description': 'Mean daily temperature in Celsius over last 7 days',
        'display_title': 'Ambient Temperature Mean 7d #068',
        'id': 'FEATURE-ML-068',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_ambient_temperature_mean_7d_068',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Integer mmHg',
        'description': 'Mean systolic BP over past 3 outpatient visits',
        'display_title': 'Patient Systolic Blood Pressure Mean #069',
        'id': 'FEATURE-ML-069',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_systolic_blood_pressure_mean_069',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous mg/dL',
        'description': 'Latest recorded fasting blood glucose laboratory value',
        'display_title': 'Patient Fasting Blood Glucose #070',
        'id': 'FEATURE-ML-070',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_fasting_blood_glucose_070',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Number of days elapsed since scheduled chronic care '
                       'recall date',
        'display_title': 'Days Overdue for Clinical Follow-up #071',
        'id': 'FEATURE-ML-071',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_days_overdue_for_clinical_follow-up_071',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Years',
        'description': 'Chronological patient age in completed solar years',
        'display_title': 'Patient Age in Years #072',
        'id': 'FEATURE-ML-072',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_age_in_years_072',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Demographics'},
    {   'data_type': 'Integer Count',
        'description': 'Number of active diagnosed chronic conditions in '
                       'patient problem list',
        'display_title': 'Patient Chronic Comorbidity Count #073',
        'id': 'FEATURE-ML-073',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_chronic_comorbidity_count_073',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous Score',
        'description': 'Weighted clinical score based on respiratory rate, '
                       'pulse, and mental status',
        'display_title': 'Emergency Triage Danger Score #074',
        'id': 'FEATURE-ML-074',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_emergency_triage_danger_score_074',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Triage Form'},
    {   'data_type': 'Integer Count',
        'description': 'Total number of distinct pharmaceutical lines on '
                       'active prescription',
        'display_title': 'Prescription Item Count #075',
        'id': 'FEATURE-ML-075',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_prescription_item_count_075',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Prescribe API'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 7 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 7d Rolling #076',
        'id': 'FEATURE-ML-076',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_7d_rolling_076',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 30 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 30d Rolling #077',
        'id': 'FEATURE-ML-077',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_30d_rolling_077',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Historical supplier lead time in days for '
                       'replenishment indent',
        'display_title': 'Drug Lead Time Days #078',
        'id': 'FEATURE-ML-078',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_drug_lead_time_days_078',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Doses',
        'description': 'Current usable unexpired inventory doses at clinic '
                       'dispensary',
        'display_title': 'Clinic Stock on Hand Balance #079',
        'id': 'FEATURE-ML-079',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_stock_on_hand_balance_079',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Redis Cache'},
    {   'data_type': 'Integer Count',
        'description': 'Total registered patient encounters for the preceding '
                       'operational day',
        'display_title': 'Clinic Daily Patient Footfall #080',
        'id': 'FEATURE-ML-080',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_daily_patient_footfall_080',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Cases',
        'description': 'Total diagnosed febrile cases in the municipal ward '
                       'over last 72 hours',
        'display_title': 'Fever Syndrome Case Count 3d #081',
        'id': 'FEATURE-ML-081',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_fever_syndrome_case_count_3d_081',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Continuous mm',
        'description': 'Cumulative rainfall in mm across municipal zone over '
                       'last 14 days',
        'display_title': 'Rainfall Rolling Accumulation 14d #082',
        'id': 'FEATURE-ML-082',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_rainfall_rolling_accumulation_14d_082',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Continuous Celsius',
        'description': 'Mean daily temperature in Celsius over last 7 days',
        'display_title': 'Ambient Temperature Mean 7d #083',
        'id': 'FEATURE-ML-083',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_ambient_temperature_mean_7d_083',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Integer mmHg',
        'description': 'Mean systolic BP over past 3 outpatient visits',
        'display_title': 'Patient Systolic Blood Pressure Mean #084',
        'id': 'FEATURE-ML-084',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_systolic_blood_pressure_mean_084',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous mg/dL',
        'description': 'Latest recorded fasting blood glucose laboratory value',
        'display_title': 'Patient Fasting Blood Glucose #085',
        'id': 'FEATURE-ML-085',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_fasting_blood_glucose_085',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Number of days elapsed since scheduled chronic care '
                       'recall date',
        'display_title': 'Days Overdue for Clinical Follow-up #086',
        'id': 'FEATURE-ML-086',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_days_overdue_for_clinical_follow-up_086',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Years',
        'description': 'Chronological patient age in completed solar years',
        'display_title': 'Patient Age in Years #087',
        'id': 'FEATURE-ML-087',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_age_in_years_087',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Demographics'},
    {   'data_type': 'Integer Count',
        'description': 'Number of active diagnosed chronic conditions in '
                       'patient problem list',
        'display_title': 'Patient Chronic Comorbidity Count #088',
        'id': 'FEATURE-ML-088',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_chronic_comorbidity_count_088',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous Score',
        'description': 'Weighted clinical score based on respiratory rate, '
                       'pulse, and mental status',
        'display_title': 'Emergency Triage Danger Score #089',
        'id': 'FEATURE-ML-089',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_emergency_triage_danger_score_089',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Triage Form'},
    {   'data_type': 'Integer Count',
        'description': 'Total number of distinct pharmaceutical lines on '
                       'active prescription',
        'display_title': 'Prescription Item Count #090',
        'id': 'FEATURE-ML-090',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_prescription_item_count_090',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Prescribe API'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 7 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 7d Rolling #091',
        'id': 'FEATURE-ML-091',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_7d_rolling_091',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 30 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 30d Rolling #092',
        'id': 'FEATURE-ML-092',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_30d_rolling_092',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Historical supplier lead time in days for '
                       'replenishment indent',
        'display_title': 'Drug Lead Time Days #093',
        'id': 'FEATURE-ML-093',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_drug_lead_time_days_093',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Doses',
        'description': 'Current usable unexpired inventory doses at clinic '
                       'dispensary',
        'display_title': 'Clinic Stock on Hand Balance #094',
        'id': 'FEATURE-ML-094',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_stock_on_hand_balance_094',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Redis Cache'},
    {   'data_type': 'Integer Count',
        'description': 'Total registered patient encounters for the preceding '
                       'operational day',
        'display_title': 'Clinic Daily Patient Footfall #095',
        'id': 'FEATURE-ML-095',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_daily_patient_footfall_095',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Cases',
        'description': 'Total diagnosed febrile cases in the municipal ward '
                       'over last 72 hours',
        'display_title': 'Fever Syndrome Case Count 3d #096',
        'id': 'FEATURE-ML-096',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_fever_syndrome_case_count_3d_096',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Continuous mm',
        'description': 'Cumulative rainfall in mm across municipal zone over '
                       'last 14 days',
        'display_title': 'Rainfall Rolling Accumulation 14d #097',
        'id': 'FEATURE-ML-097',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_rainfall_rolling_accumulation_14d_097',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Continuous Celsius',
        'description': 'Mean daily temperature in Celsius over last 7 days',
        'display_title': 'Ambient Temperature Mean 7d #098',
        'id': 'FEATURE-ML-098',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_ambient_temperature_mean_7d_098',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Integer mmHg',
        'description': 'Mean systolic BP over past 3 outpatient visits',
        'display_title': 'Patient Systolic Blood Pressure Mean #099',
        'id': 'FEATURE-ML-099',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_systolic_blood_pressure_mean_099',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous mg/dL',
        'description': 'Latest recorded fasting blood glucose laboratory value',
        'display_title': 'Patient Fasting Blood Glucose #100',
        'id': 'FEATURE-ML-100',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_fasting_blood_glucose_100',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Number of days elapsed since scheduled chronic care '
                       'recall date',
        'display_title': 'Days Overdue for Clinical Follow-up #101',
        'id': 'FEATURE-ML-101',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_days_overdue_for_clinical_follow-up_101',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Years',
        'description': 'Chronological patient age in completed solar years',
        'display_title': 'Patient Age in Years #102',
        'id': 'FEATURE-ML-102',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_age_in_years_102',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Demographics'},
    {   'data_type': 'Integer Count',
        'description': 'Number of active diagnosed chronic conditions in '
                       'patient problem list',
        'display_title': 'Patient Chronic Comorbidity Count #103',
        'id': 'FEATURE-ML-103',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_chronic_comorbidity_count_103',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous Score',
        'description': 'Weighted clinical score based on respiratory rate, '
                       'pulse, and mental status',
        'display_title': 'Emergency Triage Danger Score #104',
        'id': 'FEATURE-ML-104',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_emergency_triage_danger_score_104',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Triage Form'},
    {   'data_type': 'Integer Count',
        'description': 'Total number of distinct pharmaceutical lines on '
                       'active prescription',
        'display_title': 'Prescription Item Count #105',
        'id': 'FEATURE-ML-105',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_prescription_item_count_105',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Prescribe API'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 7 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 7d Rolling #106',
        'id': 'FEATURE-ML-106',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_7d_rolling_106',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 30 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 30d Rolling #107',
        'id': 'FEATURE-ML-107',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_30d_rolling_107',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Historical supplier lead time in days for '
                       'replenishment indent',
        'display_title': 'Drug Lead Time Days #108',
        'id': 'FEATURE-ML-108',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_drug_lead_time_days_108',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Doses',
        'description': 'Current usable unexpired inventory doses at clinic '
                       'dispensary',
        'display_title': 'Clinic Stock on Hand Balance #109',
        'id': 'FEATURE-ML-109',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_stock_on_hand_balance_109',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Redis Cache'},
    {   'data_type': 'Integer Count',
        'description': 'Total registered patient encounters for the preceding '
                       'operational day',
        'display_title': 'Clinic Daily Patient Footfall #110',
        'id': 'FEATURE-ML-110',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_daily_patient_footfall_110',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Cases',
        'description': 'Total diagnosed febrile cases in the municipal ward '
                       'over last 72 hours',
        'display_title': 'Fever Syndrome Case Count 3d #111',
        'id': 'FEATURE-ML-111',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_fever_syndrome_case_count_3d_111',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Continuous mm',
        'description': 'Cumulative rainfall in mm across municipal zone over '
                       'last 14 days',
        'display_title': 'Rainfall Rolling Accumulation 14d #112',
        'id': 'FEATURE-ML-112',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_rainfall_rolling_accumulation_14d_112',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Continuous Celsius',
        'description': 'Mean daily temperature in Celsius over last 7 days',
        'display_title': 'Ambient Temperature Mean 7d #113',
        'id': 'FEATURE-ML-113',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_ambient_temperature_mean_7d_113',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Integer mmHg',
        'description': 'Mean systolic BP over past 3 outpatient visits',
        'display_title': 'Patient Systolic Blood Pressure Mean #114',
        'id': 'FEATURE-ML-114',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_systolic_blood_pressure_mean_114',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous mg/dL',
        'description': 'Latest recorded fasting blood glucose laboratory value',
        'display_title': 'Patient Fasting Blood Glucose #115',
        'id': 'FEATURE-ML-115',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_fasting_blood_glucose_115',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Number of days elapsed since scheduled chronic care '
                       'recall date',
        'display_title': 'Days Overdue for Clinical Follow-up #116',
        'id': 'FEATURE-ML-116',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_days_overdue_for_clinical_follow-up_116',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Years',
        'description': 'Chronological patient age in completed solar years',
        'display_title': 'Patient Age in Years #117',
        'id': 'FEATURE-ML-117',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_age_in_years_117',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Demographics'},
    {   'data_type': 'Integer Count',
        'description': 'Number of active diagnosed chronic conditions in '
                       'patient problem list',
        'display_title': 'Patient Chronic Comorbidity Count #118',
        'id': 'FEATURE-ML-118',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_chronic_comorbidity_count_118',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous Score',
        'description': 'Weighted clinical score based on respiratory rate, '
                       'pulse, and mental status',
        'display_title': 'Emergency Triage Danger Score #119',
        'id': 'FEATURE-ML-119',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_emergency_triage_danger_score_119',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Triage Form'},
    {   'data_type': 'Integer Count',
        'description': 'Total number of distinct pharmaceutical lines on '
                       'active prescription',
        'display_title': 'Prescription Item Count #120',
        'id': 'FEATURE-ML-120',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_prescription_item_count_120',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Prescribe API'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 7 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 7d Rolling #121',
        'id': 'FEATURE-ML-121',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_7d_rolling_121',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 30 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 30d Rolling #122',
        'id': 'FEATURE-ML-122',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_30d_rolling_122',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Historical supplier lead time in days for '
                       'replenishment indent',
        'display_title': 'Drug Lead Time Days #123',
        'id': 'FEATURE-ML-123',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_drug_lead_time_days_123',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Doses',
        'description': 'Current usable unexpired inventory doses at clinic '
                       'dispensary',
        'display_title': 'Clinic Stock on Hand Balance #124',
        'id': 'FEATURE-ML-124',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_stock_on_hand_balance_124',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Redis Cache'},
    {   'data_type': 'Integer Count',
        'description': 'Total registered patient encounters for the preceding '
                       'operational day',
        'display_title': 'Clinic Daily Patient Footfall #125',
        'id': 'FEATURE-ML-125',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_daily_patient_footfall_125',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Cases',
        'description': 'Total diagnosed febrile cases in the municipal ward '
                       'over last 72 hours',
        'display_title': 'Fever Syndrome Case Count 3d #126',
        'id': 'FEATURE-ML-126',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_fever_syndrome_case_count_3d_126',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Continuous mm',
        'description': 'Cumulative rainfall in mm across municipal zone over '
                       'last 14 days',
        'display_title': 'Rainfall Rolling Accumulation 14d #127',
        'id': 'FEATURE-ML-127',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_rainfall_rolling_accumulation_14d_127',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Continuous Celsius',
        'description': 'Mean daily temperature in Celsius over last 7 days',
        'display_title': 'Ambient Temperature Mean 7d #128',
        'id': 'FEATURE-ML-128',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_ambient_temperature_mean_7d_128',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Integer mmHg',
        'description': 'Mean systolic BP over past 3 outpatient visits',
        'display_title': 'Patient Systolic Blood Pressure Mean #129',
        'id': 'FEATURE-ML-129',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_systolic_blood_pressure_mean_129',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous mg/dL',
        'description': 'Latest recorded fasting blood glucose laboratory value',
        'display_title': 'Patient Fasting Blood Glucose #130',
        'id': 'FEATURE-ML-130',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_fasting_blood_glucose_130',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Number of days elapsed since scheduled chronic care '
                       'recall date',
        'display_title': 'Days Overdue for Clinical Follow-up #131',
        'id': 'FEATURE-ML-131',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_days_overdue_for_clinical_follow-up_131',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Years',
        'description': 'Chronological patient age in completed solar years',
        'display_title': 'Patient Age in Years #132',
        'id': 'FEATURE-ML-132',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_age_in_years_132',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Demographics'},
    {   'data_type': 'Integer Count',
        'description': 'Number of active diagnosed chronic conditions in '
                       'patient problem list',
        'display_title': 'Patient Chronic Comorbidity Count #133',
        'id': 'FEATURE-ML-133',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_chronic_comorbidity_count_133',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous Score',
        'description': 'Weighted clinical score based on respiratory rate, '
                       'pulse, and mental status',
        'display_title': 'Emergency Triage Danger Score #134',
        'id': 'FEATURE-ML-134',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_emergency_triage_danger_score_134',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Triage Form'},
    {   'data_type': 'Integer Count',
        'description': 'Total number of distinct pharmaceutical lines on '
                       'active prescription',
        'display_title': 'Prescription Item Count #135',
        'id': 'FEATURE-ML-135',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_prescription_item_count_135',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Prescribe API'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 7 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 7d Rolling #136',
        'id': 'FEATURE-ML-136',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_7d_rolling_136',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Continuous Float',
        'description': 'Average daily dispensed doses over last 30 calendar '
                       'days',
        'display_title': 'Historical Drug Consumption 30d Rolling #137',
        'id': 'FEATURE-ML-137',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_historical_drug_consumption_30d_rolling_137',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Historical supplier lead time in days for '
                       'replenishment indent',
        'display_title': 'Drug Lead Time Days #138',
        'id': 'FEATURE-ML-138',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_drug_lead_time_days_138',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Doses',
        'description': 'Current usable unexpired inventory doses at clinic '
                       'dispensary',
        'display_title': 'Clinic Stock on Hand Balance #139',
        'id': 'FEATURE-ML-139',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_stock_on_hand_balance_139',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Redis Cache'},
    {   'data_type': 'Integer Count',
        'description': 'Total registered patient encounters for the preceding '
                       'operational day',
        'display_title': 'Clinic Daily Patient Footfall #140',
        'id': 'FEATURE-ML-140',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_clinic_daily_patient_footfall_140',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Redis Feature Cache'},
    {   'data_type': 'Integer Cases',
        'description': 'Total diagnosed febrile cases in the municipal ward '
                       'over last 72 hours',
        'display_title': 'Fever Syndrome Case Count 3d #141',
        'id': 'FEATURE-ML-141',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_fever_syndrome_case_count_3d_141',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'ClickHouse Feature Store'},
    {   'data_type': 'Continuous mm',
        'description': 'Cumulative rainfall in mm across municipal zone over '
                       'last 14 days',
        'display_title': 'Rainfall Rolling Accumulation 14d #142',
        'id': 'FEATURE-ML-142',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_rainfall_rolling_accumulation_14d_142',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Continuous Celsius',
        'description': 'Mean daily temperature in Celsius over last 7 days',
        'display_title': 'Ambient Temperature Mean 7d #143',
        'id': 'FEATURE-ML-143',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_ambient_temperature_mean_7d_143',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Weather Analytics Store'},
    {   'data_type': 'Integer mmHg',
        'description': 'Mean systolic BP over past 3 outpatient visits',
        'display_title': 'Patient Systolic Blood Pressure Mean #144',
        'id': 'FEATURE-ML-144',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_systolic_blood_pressure_mean_144',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous mg/dL',
        'description': 'Latest recorded fasting blood glucose laboratory value',
        'display_title': 'Patient Fasting Blood Glucose #145',
        'id': 'FEATURE-ML-145',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_fasting_blood_glucose_145',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Days',
        'description': 'Number of days elapsed since scheduled chronic care '
                       'recall date',
        'display_title': 'Days Overdue for Clinical Follow-up #146',
        'id': 'FEATURE-ML-146',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_days_overdue_for_clinical_follow-up_146',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Integer Years',
        'description': 'Chronological patient age in completed solar years',
        'display_title': 'Patient Age in Years #147',
        'id': 'FEATURE-ML-147',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_age_in_years_147',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Demographics'},
    {   'data_type': 'Integer Count',
        'description': 'Number of active diagnosed chronic conditions in '
                       'patient problem list',
        'display_title': 'Patient Chronic Comorbidity Count #148',
        'id': 'FEATURE-ML-148',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_patient_chronic_comorbidity_count_148',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'EHR Feature Store'},
    {   'data_type': 'Continuous Score',
        'description': 'Weighted clinical score based on respiratory rate, '
                       'pulse, and mental status',
        'display_title': 'Emergency Triage Danger Score #149',
        'id': 'FEATURE-ML-149',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_emergency_triage_danger_score_149',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Triage Form'},
    {   'data_type': 'Integer Count',
        'description': 'Total number of distinct pharmaceutical lines on '
                       'active prescription',
        'display_title': 'Prescription Item Count #150',
        'id': 'FEATURE-ML-150',
        'leakage_prevention': 'Strict timestamp truncation strictly before '
                              'prediction event horizon (t0)',
        'name': 'feat_prescription_item_count_150',
        'privacy_classification': 'De-identified Clinical Feature',
        'scaling_imputation': 'RobustScaler with median imputation on missing '
                              'values',
        'serving_store': 'Real-time Prescribe API'}]

EVALUATION_METRICS = [   {   'acceptance_target': '< 15.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-001',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Mean Absolute Percentage Error (MAPE) #001',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 12.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-002',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Weighted Absolute Percentage Error (WAPE) #002',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 25.0 Doses',
        'category': 'Regression Variance',
        'id': 'EVAL-003',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Root Mean Squared Error (RMSE) #003',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Doses'},
    {   'acceptance_target': '> 0.85',
        'category': 'Top-K Ranking Precision',
        'id': 'EVAL-004',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Precision@10 #004',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '> 0.90',
        'category': 'Top-K Outbreak Coverage',
        'id': 'EVAL-005',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Recall@K #005',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 2 False Alarms/Month',
        'category': 'Operational Alarm Fatigue',
        'id': 'EVAL-006',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection False Alarm Rate #006',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Alarms/Month'},
    {   'acceptance_target': '> 0.88',
        'category': 'Discrimination Ability',
        'id': 'EVAL-007',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under ROC (AUROC) #007',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '> 0.80',
        'category': 'Imbalanced Retrieval',
        'id': 'EVAL-008',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under PR (AUPRC) #008',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '0.85 - 1.15',
        'category': 'Fairness Audit',
        'id': 'EVAL-009',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Demographic Parity Ratio (Gender) #009',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '0.80 - 1.25',
        'category': 'Fairness Audit',
        'id': 'EVAL-010',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Disparate Impact Ratio (Socioeconomic Wards) #010',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 15.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-011',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Mean Absolute Percentage Error (MAPE) #011',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 12.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-012',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Weighted Absolute Percentage Error (WAPE) #012',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 25.0 Doses',
        'category': 'Regression Variance',
        'id': 'EVAL-013',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Root Mean Squared Error (RMSE) #013',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Doses'},
    {   'acceptance_target': '> 0.85',
        'category': 'Top-K Ranking Precision',
        'id': 'EVAL-014',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Precision@10 #014',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '> 0.90',
        'category': 'Top-K Outbreak Coverage',
        'id': 'EVAL-015',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Recall@K #015',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 2 False Alarms/Month',
        'category': 'Operational Alarm Fatigue',
        'id': 'EVAL-016',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection False Alarm Rate #016',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Alarms/Month'},
    {   'acceptance_target': '> 0.88',
        'category': 'Discrimination Ability',
        'id': 'EVAL-017',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under ROC (AUROC) #017',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '> 0.80',
        'category': 'Imbalanced Retrieval',
        'id': 'EVAL-018',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under PR (AUPRC) #018',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '0.85 - 1.15',
        'category': 'Fairness Audit',
        'id': 'EVAL-019',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Demographic Parity Ratio (Gender) #019',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '0.80 - 1.25',
        'category': 'Fairness Audit',
        'id': 'EVAL-020',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Disparate Impact Ratio (Socioeconomic Wards) #020',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 15.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-021',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Mean Absolute Percentage Error (MAPE) #021',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 12.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-022',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Weighted Absolute Percentage Error (WAPE) #022',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 25.0 Doses',
        'category': 'Regression Variance',
        'id': 'EVAL-023',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Root Mean Squared Error (RMSE) #023',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Doses'},
    {   'acceptance_target': '> 0.85',
        'category': 'Top-K Ranking Precision',
        'id': 'EVAL-024',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Precision@10 #024',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '> 0.90',
        'category': 'Top-K Outbreak Coverage',
        'id': 'EVAL-025',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Recall@K #025',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 2 False Alarms/Month',
        'category': 'Operational Alarm Fatigue',
        'id': 'EVAL-026',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection False Alarm Rate #026',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Alarms/Month'},
    {   'acceptance_target': '> 0.88',
        'category': 'Discrimination Ability',
        'id': 'EVAL-027',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under ROC (AUROC) #027',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '> 0.80',
        'category': 'Imbalanced Retrieval',
        'id': 'EVAL-028',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under PR (AUPRC) #028',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '0.85 - 1.15',
        'category': 'Fairness Audit',
        'id': 'EVAL-029',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Demographic Parity Ratio (Gender) #029',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '0.80 - 1.25',
        'category': 'Fairness Audit',
        'id': 'EVAL-030',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Disparate Impact Ratio (Socioeconomic Wards) #030',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 15.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-031',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Mean Absolute Percentage Error (MAPE) #031',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 12.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-032',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Weighted Absolute Percentage Error (WAPE) #032',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 25.0 Doses',
        'category': 'Regression Variance',
        'id': 'EVAL-033',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Root Mean Squared Error (RMSE) #033',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Doses'},
    {   'acceptance_target': '> 0.85',
        'category': 'Top-K Ranking Precision',
        'id': 'EVAL-034',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Precision@10 #034',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '> 0.90',
        'category': 'Top-K Outbreak Coverage',
        'id': 'EVAL-035',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Recall@K #035',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 2 False Alarms/Month',
        'category': 'Operational Alarm Fatigue',
        'id': 'EVAL-036',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection False Alarm Rate #036',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Alarms/Month'},
    {   'acceptance_target': '> 0.88',
        'category': 'Discrimination Ability',
        'id': 'EVAL-037',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under ROC (AUROC) #037',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '> 0.80',
        'category': 'Imbalanced Retrieval',
        'id': 'EVAL-038',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under PR (AUPRC) #038',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '0.85 - 1.15',
        'category': 'Fairness Audit',
        'id': 'EVAL-039',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Demographic Parity Ratio (Gender) #039',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '0.80 - 1.25',
        'category': 'Fairness Audit',
        'id': 'EVAL-040',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Disparate Impact Ratio (Socioeconomic Wards) #040',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 15.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-041',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Mean Absolute Percentage Error (MAPE) #041',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 12.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-042',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Weighted Absolute Percentage Error (WAPE) #042',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 25.0 Doses',
        'category': 'Regression Variance',
        'id': 'EVAL-043',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Root Mean Squared Error (RMSE) #043',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Doses'},
    {   'acceptance_target': '> 0.85',
        'category': 'Top-K Ranking Precision',
        'id': 'EVAL-044',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Precision@10 #044',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '> 0.90',
        'category': 'Top-K Outbreak Coverage',
        'id': 'EVAL-045',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Recall@K #045',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 2 False Alarms/Month',
        'category': 'Operational Alarm Fatigue',
        'id': 'EVAL-046',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection False Alarm Rate #046',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Alarms/Month'},
    {   'acceptance_target': '> 0.88',
        'category': 'Discrimination Ability',
        'id': 'EVAL-047',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under ROC (AUROC) #047',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '> 0.80',
        'category': 'Imbalanced Retrieval',
        'id': 'EVAL-048',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under PR (AUPRC) #048',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '0.85 - 1.15',
        'category': 'Fairness Audit',
        'id': 'EVAL-049',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Demographic Parity Ratio (Gender) #049',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '0.80 - 1.25',
        'category': 'Fairness Audit',
        'id': 'EVAL-050',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Disparate Impact Ratio (Socioeconomic Wards) #050',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 15.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-051',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Mean Absolute Percentage Error (MAPE) #051',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 12.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-052',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Weighted Absolute Percentage Error (WAPE) #052',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 25.0 Doses',
        'category': 'Regression Variance',
        'id': 'EVAL-053',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Root Mean Squared Error (RMSE) #053',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Doses'},
    {   'acceptance_target': '> 0.85',
        'category': 'Top-K Ranking Precision',
        'id': 'EVAL-054',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Precision@10 #054',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '> 0.90',
        'category': 'Top-K Outbreak Coverage',
        'id': 'EVAL-055',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Recall@K #055',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 2 False Alarms/Month',
        'category': 'Operational Alarm Fatigue',
        'id': 'EVAL-056',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection False Alarm Rate #056',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Alarms/Month'},
    {   'acceptance_target': '> 0.88',
        'category': 'Discrimination Ability',
        'id': 'EVAL-057',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under ROC (AUROC) #057',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '> 0.80',
        'category': 'Imbalanced Retrieval',
        'id': 'EVAL-058',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under PR (AUPRC) #058',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '0.85 - 1.15',
        'category': 'Fairness Audit',
        'id': 'EVAL-059',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Demographic Parity Ratio (Gender) #059',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '0.80 - 1.25',
        'category': 'Fairness Audit',
        'id': 'EVAL-060',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Disparate Impact Ratio (Socioeconomic Wards) #060',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 15.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-061',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Mean Absolute Percentage Error (MAPE) #061',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 12.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-062',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Weighted Absolute Percentage Error (WAPE) #062',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 25.0 Doses',
        'category': 'Regression Variance',
        'id': 'EVAL-063',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Root Mean Squared Error (RMSE) #063',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Doses'},
    {   'acceptance_target': '> 0.85',
        'category': 'Top-K Ranking Precision',
        'id': 'EVAL-064',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Precision@10 #064',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '> 0.90',
        'category': 'Top-K Outbreak Coverage',
        'id': 'EVAL-065',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Recall@K #065',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 2 False Alarms/Month',
        'category': 'Operational Alarm Fatigue',
        'id': 'EVAL-066',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection False Alarm Rate #066',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Alarms/Month'},
    {   'acceptance_target': '> 0.88',
        'category': 'Discrimination Ability',
        'id': 'EVAL-067',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under ROC (AUROC) #067',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '> 0.80',
        'category': 'Imbalanced Retrieval',
        'id': 'EVAL-068',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under PR (AUPRC) #068',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '0.85 - 1.15',
        'category': 'Fairness Audit',
        'id': 'EVAL-069',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Demographic Parity Ratio (Gender) #069',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '0.80 - 1.25',
        'category': 'Fairness Audit',
        'id': 'EVAL-070',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Disparate Impact Ratio (Socioeconomic Wards) #070',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 15.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-071',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Mean Absolute Percentage Error (MAPE) #071',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 12.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-072',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Weighted Absolute Percentage Error (WAPE) #072',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 25.0 Doses',
        'category': 'Regression Variance',
        'id': 'EVAL-073',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Root Mean Squared Error (RMSE) #073',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Doses'},
    {   'acceptance_target': '> 0.85',
        'category': 'Top-K Ranking Precision',
        'id': 'EVAL-074',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Precision@10 #074',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '> 0.90',
        'category': 'Top-K Outbreak Coverage',
        'id': 'EVAL-075',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Recall@K #075',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 2 False Alarms/Month',
        'category': 'Operational Alarm Fatigue',
        'id': 'EVAL-076',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection False Alarm Rate #076',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Alarms/Month'},
    {   'acceptance_target': '> 0.88',
        'category': 'Discrimination Ability',
        'id': 'EVAL-077',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under ROC (AUROC) #077',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '> 0.80',
        'category': 'Imbalanced Retrieval',
        'id': 'EVAL-078',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under PR (AUPRC) #078',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '0.85 - 1.15',
        'category': 'Fairness Audit',
        'id': 'EVAL-079',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Demographic Parity Ratio (Gender) #079',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '0.80 - 1.25',
        'category': 'Fairness Audit',
        'id': 'EVAL-080',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Disparate Impact Ratio (Socioeconomic Wards) #080',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 15.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-081',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Mean Absolute Percentage Error (MAPE) #081',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 12.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-082',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Weighted Absolute Percentage Error (WAPE) #082',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 25.0 Doses',
        'category': 'Regression Variance',
        'id': 'EVAL-083',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Root Mean Squared Error (RMSE) #083',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Doses'},
    {   'acceptance_target': '> 0.85',
        'category': 'Top-K Ranking Precision',
        'id': 'EVAL-084',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Precision@10 #084',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '> 0.90',
        'category': 'Top-K Outbreak Coverage',
        'id': 'EVAL-085',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Recall@K #085',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 2 False Alarms/Month',
        'category': 'Operational Alarm Fatigue',
        'id': 'EVAL-086',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection False Alarm Rate #086',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Alarms/Month'},
    {   'acceptance_target': '> 0.88',
        'category': 'Discrimination Ability',
        'id': 'EVAL-087',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under ROC (AUROC) #087',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '> 0.80',
        'category': 'Imbalanced Retrieval',
        'id': 'EVAL-088',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under PR (AUPRC) #088',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '0.85 - 1.15',
        'category': 'Fairness Audit',
        'id': 'EVAL-089',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Demographic Parity Ratio (Gender) #089',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '0.80 - 1.25',
        'category': 'Fairness Audit',
        'id': 'EVAL-090',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Disparate Impact Ratio (Socioeconomic Wards) #090',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 15.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-091',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Mean Absolute Percentage Error (MAPE) #091',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 12.0%',
        'category': 'Regression Accuracy',
        'id': 'EVAL-092',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Weighted Absolute Percentage Error (WAPE) #092',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Percentage'},
    {   'acceptance_target': '< 25.0 Doses',
        'category': 'Regression Variance',
        'id': 'EVAL-093',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Forecasting',
        'name': 'Forecasting Root Mean Squared Error (RMSE) #093',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Doses'},
    {   'acceptance_target': '> 0.85',
        'category': 'Top-K Ranking Precision',
        'id': 'EVAL-094',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Precision@10 #094',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '> 0.90',
        'category': 'Top-K Outbreak Coverage',
        'id': 'EVAL-095',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection Recall@K #095',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '< 2 False Alarms/Month',
        'category': 'Operational Alarm Fatigue',
        'id': 'EVAL-096',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Anomaly Detection',
        'name': 'Anomaly Detection False Alarm Rate #096',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Alarms/Month'},
    {   'acceptance_target': '> 0.88',
        'category': 'Discrimination Ability',
        'id': 'EVAL-097',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under ROC (AUROC) #097',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '> 0.80',
        'category': 'Imbalanced Retrieval',
        'id': 'EVAL-098',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Classification',
        'name': 'Classification Area Under PR (AUPRC) #098',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Score (0-1)'},
    {   'acceptance_target': '0.85 - 1.15',
        'category': 'Fairness Audit',
        'id': 'EVAL-099',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Demographic Parity Ratio (Gender) #099',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'},
    {   'acceptance_target': '0.80 - 1.25',
        'category': 'Fairness Audit',
        'id': 'EVAL-100',
        'measurement_cadence': 'Continuous Automated CI Validation & Monthly '
                               'Production Audit',
        'model_domain': 'Algorithmic Fairness',
        'name': 'Disparate Impact Ratio (Socioeconomic Wards) #100',
        'rejection_threshold': 'Failure to meet target blocks deployment '
                               'promotion in model registry.',
        'unit': 'Ratio'}]
