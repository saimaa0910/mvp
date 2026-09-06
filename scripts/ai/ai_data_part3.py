"""ai_data_part3.py - AI Risks, AI Controls"""

AI_RISKS = [   {   'description': 'Overly sensitive alerts cause physicians to dismiss '
                       'critical warnings.',
        'governance_domain': 'Physician Experience',
        'id': 'AI-RISK-001',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-001',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Positive Fatigue #001'},
    {   'description': 'Failure to detect severe condition leads to delayed '
                       'clinical intervention.',
        'governance_domain': 'Patient Safety',
        'id': 'AI-RISK-002',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-002',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Negative Harm #002'},
    {   'description': 'Model underpredicts seasonal consumption causing vital '
                       'drug stockouts.',
        'governance_domain': 'Pharmaceutical Continuity',
        'id': 'AI-RISK-003',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-003',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Under-Forecasting Medicine Stockout #003'},
    {   'description': 'Model overpredicts demand resulting in surplus '
                       'expiration wastage.',
        'governance_domain': 'Municipal Finance',
        'id': 'AI-RISK-004',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-004',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Over-Forecasting Medicine Expiry #004'},
    {   'description': 'Under-representation of slum populations causes skewed '
                       'recall prioritization.',
        'governance_domain': 'Ethical Governance',
        'id': 'AI-RISK-005',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-005',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Demographic & Socioeconomic Bias #005'},
    {   'description': 'Novel viral pathogen alters fever symptoms '
                       'invalidating existing models.',
        'governance_domain': 'Model Validity',
        'id': 'AI-RISK-006',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-006',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Data Drift Due to Epidemiological Shift #006'},
    {   'description': 'Kafka lag or schema drift feeds stale features to '
                       'inference runtime.',
        'governance_domain': 'Operational Reliability',
        'id': 'AI-RISK-007',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-007',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Feature Store Data Pipeline Corruption #007'},
    {   'description': 'Extreme laboratory values or edge biometric inputs '
                       'produce erratic outputs.',
        'governance_domain': 'Runtime Safety',
        'id': 'AI-RISK-008',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-008',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Out-of-Distribution Input Values #008'},
    {   'description': 'Malicious or corrupt input vectors intended to distort '
                       'municipal indents.',
        'governance_domain': 'Cybersecurity',
        'id': 'AI-RISK-009',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-009',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Model Evasion & Poisoning Attempts #009'},
    {   'description': 'Black-box outputs without SHAP attribution leading to '
                       'zero physician adoption.',
        'governance_domain': 'Clinical Adoption',
        'id': 'AI-RISK-010',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-010',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Lack of Explainability & Clinician Distrust #010'},
    {   'description': 'Overly sensitive alerts cause physicians to dismiss '
                       'critical warnings.',
        'governance_domain': 'Physician Experience',
        'id': 'AI-RISK-011',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-011',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Positive Fatigue #011'},
    {   'description': 'Failure to detect severe condition leads to delayed '
                       'clinical intervention.',
        'governance_domain': 'Patient Safety',
        'id': 'AI-RISK-012',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-012',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Negative Harm #012'},
    {   'description': 'Model underpredicts seasonal consumption causing vital '
                       'drug stockouts.',
        'governance_domain': 'Pharmaceutical Continuity',
        'id': 'AI-RISK-013',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-013',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Under-Forecasting Medicine Stockout #013'},
    {   'description': 'Model overpredicts demand resulting in surplus '
                       'expiration wastage.',
        'governance_domain': 'Municipal Finance',
        'id': 'AI-RISK-014',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-014',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Over-Forecasting Medicine Expiry #014'},
    {   'description': 'Under-representation of slum populations causes skewed '
                       'recall prioritization.',
        'governance_domain': 'Ethical Governance',
        'id': 'AI-RISK-015',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-015',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Demographic & Socioeconomic Bias #015'},
    {   'description': 'Novel viral pathogen alters fever symptoms '
                       'invalidating existing models.',
        'governance_domain': 'Model Validity',
        'id': 'AI-RISK-016',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-016',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Data Drift Due to Epidemiological Shift #016'},
    {   'description': 'Kafka lag or schema drift feeds stale features to '
                       'inference runtime.',
        'governance_domain': 'Operational Reliability',
        'id': 'AI-RISK-017',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-017',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Feature Store Data Pipeline Corruption #017'},
    {   'description': 'Extreme laboratory values or edge biometric inputs '
                       'produce erratic outputs.',
        'governance_domain': 'Runtime Safety',
        'id': 'AI-RISK-018',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-018',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Out-of-Distribution Input Values #018'},
    {   'description': 'Malicious or corrupt input vectors intended to distort '
                       'municipal indents.',
        'governance_domain': 'Cybersecurity',
        'id': 'AI-RISK-019',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-019',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Model Evasion & Poisoning Attempts #019'},
    {   'description': 'Black-box outputs without SHAP attribution leading to '
                       'zero physician adoption.',
        'governance_domain': 'Clinical Adoption',
        'id': 'AI-RISK-020',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-020',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Lack of Explainability & Clinician Distrust #020'},
    {   'description': 'Overly sensitive alerts cause physicians to dismiss '
                       'critical warnings.',
        'governance_domain': 'Physician Experience',
        'id': 'AI-RISK-021',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-021',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Positive Fatigue #021'},
    {   'description': 'Failure to detect severe condition leads to delayed '
                       'clinical intervention.',
        'governance_domain': 'Patient Safety',
        'id': 'AI-RISK-022',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-022',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Negative Harm #022'},
    {   'description': 'Model underpredicts seasonal consumption causing vital '
                       'drug stockouts.',
        'governance_domain': 'Pharmaceutical Continuity',
        'id': 'AI-RISK-023',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-023',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Under-Forecasting Medicine Stockout #023'},
    {   'description': 'Model overpredicts demand resulting in surplus '
                       'expiration wastage.',
        'governance_domain': 'Municipal Finance',
        'id': 'AI-RISK-024',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-024',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Over-Forecasting Medicine Expiry #024'},
    {   'description': 'Under-representation of slum populations causes skewed '
                       'recall prioritization.',
        'governance_domain': 'Ethical Governance',
        'id': 'AI-RISK-025',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-025',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Demographic & Socioeconomic Bias #025'},
    {   'description': 'Novel viral pathogen alters fever symptoms '
                       'invalidating existing models.',
        'governance_domain': 'Model Validity',
        'id': 'AI-RISK-026',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-026',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Data Drift Due to Epidemiological Shift #026'},
    {   'description': 'Kafka lag or schema drift feeds stale features to '
                       'inference runtime.',
        'governance_domain': 'Operational Reliability',
        'id': 'AI-RISK-027',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-027',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Feature Store Data Pipeline Corruption #027'},
    {   'description': 'Extreme laboratory values or edge biometric inputs '
                       'produce erratic outputs.',
        'governance_domain': 'Runtime Safety',
        'id': 'AI-RISK-028',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-028',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Out-of-Distribution Input Values #028'},
    {   'description': 'Malicious or corrupt input vectors intended to distort '
                       'municipal indents.',
        'governance_domain': 'Cybersecurity',
        'id': 'AI-RISK-029',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-029',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Model Evasion & Poisoning Attempts #029'},
    {   'description': 'Black-box outputs without SHAP attribution leading to '
                       'zero physician adoption.',
        'governance_domain': 'Clinical Adoption',
        'id': 'AI-RISK-030',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-030',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Lack of Explainability & Clinician Distrust #030'},
    {   'description': 'Overly sensitive alerts cause physicians to dismiss '
                       'critical warnings.',
        'governance_domain': 'Physician Experience',
        'id': 'AI-RISK-031',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-031',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Positive Fatigue #031'},
    {   'description': 'Failure to detect severe condition leads to delayed '
                       'clinical intervention.',
        'governance_domain': 'Patient Safety',
        'id': 'AI-RISK-032',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-032',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Negative Harm #032'},
    {   'description': 'Model underpredicts seasonal consumption causing vital '
                       'drug stockouts.',
        'governance_domain': 'Pharmaceutical Continuity',
        'id': 'AI-RISK-033',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-033',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Under-Forecasting Medicine Stockout #033'},
    {   'description': 'Model overpredicts demand resulting in surplus '
                       'expiration wastage.',
        'governance_domain': 'Municipal Finance',
        'id': 'AI-RISK-034',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-034',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Over-Forecasting Medicine Expiry #034'},
    {   'description': 'Under-representation of slum populations causes skewed '
                       'recall prioritization.',
        'governance_domain': 'Ethical Governance',
        'id': 'AI-RISK-035',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-035',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Demographic & Socioeconomic Bias #035'},
    {   'description': 'Novel viral pathogen alters fever symptoms '
                       'invalidating existing models.',
        'governance_domain': 'Model Validity',
        'id': 'AI-RISK-036',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-036',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Data Drift Due to Epidemiological Shift #036'},
    {   'description': 'Kafka lag or schema drift feeds stale features to '
                       'inference runtime.',
        'governance_domain': 'Operational Reliability',
        'id': 'AI-RISK-037',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-037',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Feature Store Data Pipeline Corruption #037'},
    {   'description': 'Extreme laboratory values or edge biometric inputs '
                       'produce erratic outputs.',
        'governance_domain': 'Runtime Safety',
        'id': 'AI-RISK-038',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-038',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Out-of-Distribution Input Values #038'},
    {   'description': 'Malicious or corrupt input vectors intended to distort '
                       'municipal indents.',
        'governance_domain': 'Cybersecurity',
        'id': 'AI-RISK-039',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-039',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Model Evasion & Poisoning Attempts #039'},
    {   'description': 'Black-box outputs without SHAP attribution leading to '
                       'zero physician adoption.',
        'governance_domain': 'Clinical Adoption',
        'id': 'AI-RISK-040',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-040',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Lack of Explainability & Clinician Distrust #040'},
    {   'description': 'Overly sensitive alerts cause physicians to dismiss '
                       'critical warnings.',
        'governance_domain': 'Physician Experience',
        'id': 'AI-RISK-041',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-041',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Positive Fatigue #041'},
    {   'description': 'Failure to detect severe condition leads to delayed '
                       'clinical intervention.',
        'governance_domain': 'Patient Safety',
        'id': 'AI-RISK-042',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-042',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Negative Harm #042'},
    {   'description': 'Model underpredicts seasonal consumption causing vital '
                       'drug stockouts.',
        'governance_domain': 'Pharmaceutical Continuity',
        'id': 'AI-RISK-043',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-043',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Under-Forecasting Medicine Stockout #043'},
    {   'description': 'Model overpredicts demand resulting in surplus '
                       'expiration wastage.',
        'governance_domain': 'Municipal Finance',
        'id': 'AI-RISK-044',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-044',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Over-Forecasting Medicine Expiry #044'},
    {   'description': 'Under-representation of slum populations causes skewed '
                       'recall prioritization.',
        'governance_domain': 'Ethical Governance',
        'id': 'AI-RISK-045',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-045',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Demographic & Socioeconomic Bias #045'},
    {   'description': 'Novel viral pathogen alters fever symptoms '
                       'invalidating existing models.',
        'governance_domain': 'Model Validity',
        'id': 'AI-RISK-046',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-046',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Data Drift Due to Epidemiological Shift #046'},
    {   'description': 'Kafka lag or schema drift feeds stale features to '
                       'inference runtime.',
        'governance_domain': 'Operational Reliability',
        'id': 'AI-RISK-047',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-047',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Feature Store Data Pipeline Corruption #047'},
    {   'description': 'Extreme laboratory values or edge biometric inputs '
                       'produce erratic outputs.',
        'governance_domain': 'Runtime Safety',
        'id': 'AI-RISK-048',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-048',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Out-of-Distribution Input Values #048'},
    {   'description': 'Malicious or corrupt input vectors intended to distort '
                       'municipal indents.',
        'governance_domain': 'Cybersecurity',
        'id': 'AI-RISK-049',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-049',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Model Evasion & Poisoning Attempts #049'},
    {   'description': 'Black-box outputs without SHAP attribution leading to '
                       'zero physician adoption.',
        'governance_domain': 'Clinical Adoption',
        'id': 'AI-RISK-050',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-050',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Lack of Explainability & Clinician Distrust #050'},
    {   'description': 'Overly sensitive alerts cause physicians to dismiss '
                       'critical warnings.',
        'governance_domain': 'Physician Experience',
        'id': 'AI-RISK-051',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-051',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Positive Fatigue #051'},
    {   'description': 'Failure to detect severe condition leads to delayed '
                       'clinical intervention.',
        'governance_domain': 'Patient Safety',
        'id': 'AI-RISK-052',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-052',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Negative Harm #052'},
    {   'description': 'Model underpredicts seasonal consumption causing vital '
                       'drug stockouts.',
        'governance_domain': 'Pharmaceutical Continuity',
        'id': 'AI-RISK-053',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-053',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Under-Forecasting Medicine Stockout #053'},
    {   'description': 'Model overpredicts demand resulting in surplus '
                       'expiration wastage.',
        'governance_domain': 'Municipal Finance',
        'id': 'AI-RISK-054',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-054',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Over-Forecasting Medicine Expiry #054'},
    {   'description': 'Under-representation of slum populations causes skewed '
                       'recall prioritization.',
        'governance_domain': 'Ethical Governance',
        'id': 'AI-RISK-055',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-055',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Demographic & Socioeconomic Bias #055'},
    {   'description': 'Novel viral pathogen alters fever symptoms '
                       'invalidating existing models.',
        'governance_domain': 'Model Validity',
        'id': 'AI-RISK-056',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-056',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Data Drift Due to Epidemiological Shift #056'},
    {   'description': 'Kafka lag or schema drift feeds stale features to '
                       'inference runtime.',
        'governance_domain': 'Operational Reliability',
        'id': 'AI-RISK-057',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-057',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Feature Store Data Pipeline Corruption #057'},
    {   'description': 'Extreme laboratory values or edge biometric inputs '
                       'produce erratic outputs.',
        'governance_domain': 'Runtime Safety',
        'id': 'AI-RISK-058',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-058',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Out-of-Distribution Input Values #058'},
    {   'description': 'Malicious or corrupt input vectors intended to distort '
                       'municipal indents.',
        'governance_domain': 'Cybersecurity',
        'id': 'AI-RISK-059',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-059',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Model Evasion & Poisoning Attempts #059'},
    {   'description': 'Black-box outputs without SHAP attribution leading to '
                       'zero physician adoption.',
        'governance_domain': 'Clinical Adoption',
        'id': 'AI-RISK-060',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-060',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Lack of Explainability & Clinician Distrust #060'},
    {   'description': 'Overly sensitive alerts cause physicians to dismiss '
                       'critical warnings.',
        'governance_domain': 'Physician Experience',
        'id': 'AI-RISK-061',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-061',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Positive Fatigue #061'},
    {   'description': 'Failure to detect severe condition leads to delayed '
                       'clinical intervention.',
        'governance_domain': 'Patient Safety',
        'id': 'AI-RISK-062',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-062',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Negative Harm #062'},
    {   'description': 'Model underpredicts seasonal consumption causing vital '
                       'drug stockouts.',
        'governance_domain': 'Pharmaceutical Continuity',
        'id': 'AI-RISK-063',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-063',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Under-Forecasting Medicine Stockout #063'},
    {   'description': 'Model overpredicts demand resulting in surplus '
                       'expiration wastage.',
        'governance_domain': 'Municipal Finance',
        'id': 'AI-RISK-064',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-064',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Over-Forecasting Medicine Expiry #064'},
    {   'description': 'Under-representation of slum populations causes skewed '
                       'recall prioritization.',
        'governance_domain': 'Ethical Governance',
        'id': 'AI-RISK-065',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-065',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Demographic & Socioeconomic Bias #065'},
    {   'description': 'Novel viral pathogen alters fever symptoms '
                       'invalidating existing models.',
        'governance_domain': 'Model Validity',
        'id': 'AI-RISK-066',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-066',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Data Drift Due to Epidemiological Shift #066'},
    {   'description': 'Kafka lag or schema drift feeds stale features to '
                       'inference runtime.',
        'governance_domain': 'Operational Reliability',
        'id': 'AI-RISK-067',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-067',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Feature Store Data Pipeline Corruption #067'},
    {   'description': 'Extreme laboratory values or edge biometric inputs '
                       'produce erratic outputs.',
        'governance_domain': 'Runtime Safety',
        'id': 'AI-RISK-068',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-068',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Out-of-Distribution Input Values #068'},
    {   'description': 'Malicious or corrupt input vectors intended to distort '
                       'municipal indents.',
        'governance_domain': 'Cybersecurity',
        'id': 'AI-RISK-069',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-069',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Model Evasion & Poisoning Attempts #069'},
    {   'description': 'Black-box outputs without SHAP attribution leading to '
                       'zero physician adoption.',
        'governance_domain': 'Clinical Adoption',
        'id': 'AI-RISK-070',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-070',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Lack of Explainability & Clinician Distrust #070'},
    {   'description': 'Overly sensitive alerts cause physicians to dismiss '
                       'critical warnings.',
        'governance_domain': 'Physician Experience',
        'id': 'AI-RISK-071',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-071',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Positive Fatigue #071'},
    {   'description': 'Failure to detect severe condition leads to delayed '
                       'clinical intervention.',
        'governance_domain': 'Patient Safety',
        'id': 'AI-RISK-072',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-072',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Negative Harm #072'},
    {   'description': 'Model underpredicts seasonal consumption causing vital '
                       'drug stockouts.',
        'governance_domain': 'Pharmaceutical Continuity',
        'id': 'AI-RISK-073',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-073',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Under-Forecasting Medicine Stockout #073'},
    {   'description': 'Model overpredicts demand resulting in surplus '
                       'expiration wastage.',
        'governance_domain': 'Municipal Finance',
        'id': 'AI-RISK-074',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-074',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Over-Forecasting Medicine Expiry #074'},
    {   'description': 'Under-representation of slum populations causes skewed '
                       'recall prioritization.',
        'governance_domain': 'Ethical Governance',
        'id': 'AI-RISK-075',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-075',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Demographic & Socioeconomic Bias #075'},
    {   'description': 'Novel viral pathogen alters fever symptoms '
                       'invalidating existing models.',
        'governance_domain': 'Model Validity',
        'id': 'AI-RISK-076',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-076',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Data Drift Due to Epidemiological Shift #076'},
    {   'description': 'Kafka lag or schema drift feeds stale features to '
                       'inference runtime.',
        'governance_domain': 'Operational Reliability',
        'id': 'AI-RISK-077',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-077',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Feature Store Data Pipeline Corruption #077'},
    {   'description': 'Extreme laboratory values or edge biometric inputs '
                       'produce erratic outputs.',
        'governance_domain': 'Runtime Safety',
        'id': 'AI-RISK-078',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-078',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Out-of-Distribution Input Values #078'},
    {   'description': 'Malicious or corrupt input vectors intended to distort '
                       'municipal indents.',
        'governance_domain': 'Cybersecurity',
        'id': 'AI-RISK-079',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-079',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Model Evasion & Poisoning Attempts #079'},
    {   'description': 'Black-box outputs without SHAP attribution leading to '
                       'zero physician adoption.',
        'governance_domain': 'Clinical Adoption',
        'id': 'AI-RISK-080',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-080',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Lack of Explainability & Clinician Distrust #080'},
    {   'description': 'Overly sensitive alerts cause physicians to dismiss '
                       'critical warnings.',
        'governance_domain': 'Physician Experience',
        'id': 'AI-RISK-081',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-001',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Positive Fatigue #081'},
    {   'description': 'Failure to detect severe condition leads to delayed '
                       'clinical intervention.',
        'governance_domain': 'Patient Safety',
        'id': 'AI-RISK-082',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-002',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Negative Harm #082'},
    {   'description': 'Model underpredicts seasonal consumption causing vital '
                       'drug stockouts.',
        'governance_domain': 'Pharmaceutical Continuity',
        'id': 'AI-RISK-083',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-003',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Under-Forecasting Medicine Stockout #083'},
    {   'description': 'Model overpredicts demand resulting in surplus '
                       'expiration wastage.',
        'governance_domain': 'Municipal Finance',
        'id': 'AI-RISK-084',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-004',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Over-Forecasting Medicine Expiry #084'},
    {   'description': 'Under-representation of slum populations causes skewed '
                       'recall prioritization.',
        'governance_domain': 'Ethical Governance',
        'id': 'AI-RISK-085',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-005',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Demographic & Socioeconomic Bias #085'},
    {   'description': 'Novel viral pathogen alters fever symptoms '
                       'invalidating existing models.',
        'governance_domain': 'Model Validity',
        'id': 'AI-RISK-086',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-006',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Data Drift Due to Epidemiological Shift #086'},
    {   'description': 'Kafka lag or schema drift feeds stale features to '
                       'inference runtime.',
        'governance_domain': 'Operational Reliability',
        'id': 'AI-RISK-087',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-007',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Feature Store Data Pipeline Corruption #087'},
    {   'description': 'Extreme laboratory values or edge biometric inputs '
                       'produce erratic outputs.',
        'governance_domain': 'Runtime Safety',
        'id': 'AI-RISK-088',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-008',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Out-of-Distribution Input Values #088'},
    {   'description': 'Malicious or corrupt input vectors intended to distort '
                       'municipal indents.',
        'governance_domain': 'Cybersecurity',
        'id': 'AI-RISK-089',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-009',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Model Evasion & Poisoning Attempts #089'},
    {   'description': 'Black-box outputs without SHAP attribution leading to '
                       'zero physician adoption.',
        'governance_domain': 'Clinical Adoption',
        'id': 'AI-RISK-090',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-010',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Lack of Explainability & Clinician Distrust #090'},
    {   'description': 'Overly sensitive alerts cause physicians to dismiss '
                       'critical warnings.',
        'governance_domain': 'Physician Experience',
        'id': 'AI-RISK-091',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-011',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Positive Fatigue #091'},
    {   'description': 'Failure to detect severe condition leads to delayed '
                       'clinical intervention.',
        'governance_domain': 'Patient Safety',
        'id': 'AI-RISK-092',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-012',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Clinical False Negative Harm #092'},
    {   'description': 'Model underpredicts seasonal consumption causing vital '
                       'drug stockouts.',
        'governance_domain': 'Pharmaceutical Continuity',
        'id': 'AI-RISK-093',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-013',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Under-Forecasting Medicine Stockout #093'},
    {   'description': 'Model overpredicts demand resulting in surplus '
                       'expiration wastage.',
        'governance_domain': 'Municipal Finance',
        'id': 'AI-RISK-094',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-014',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Over-Forecasting Medicine Expiry #094'},
    {   'description': 'Under-representation of slum populations causes skewed '
                       'recall prioritization.',
        'governance_domain': 'Ethical Governance',
        'id': 'AI-RISK-095',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-015',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Demographic & Socioeconomic Bias #095'},
    {   'description': 'Novel viral pathogen alters fever symptoms '
                       'invalidating existing models.',
        'governance_domain': 'Model Validity',
        'id': 'AI-RISK-096',
        'inherent_severity': 'Critical',
        'mitigating_control_ref': 'AI-CONTROL-016',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Data Drift Due to Epidemiological Shift #096'},
    {   'description': 'Kafka lag or schema drift feeds stale features to '
                       'inference runtime.',
        'governance_domain': 'Operational Reliability',
        'id': 'AI-RISK-097',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-017',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Feature Store Data Pipeline Corruption #097'},
    {   'description': 'Extreme laboratory values or edge biometric inputs '
                       'produce erratic outputs.',
        'governance_domain': 'Runtime Safety',
        'id': 'AI-RISK-098',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-018',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Out-of-Distribution Input Values #098'},
    {   'description': 'Malicious or corrupt input vectors intended to distort '
                       'municipal indents.',
        'governance_domain': 'Cybersecurity',
        'id': 'AI-RISK-099',
        'inherent_severity': 'Medium',
        'mitigating_control_ref': 'AI-CONTROL-019',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Model Evasion & Poisoning Attempts #099'},
    {   'description': 'Black-box outputs without SHAP attribution leading to '
                       'zero physician adoption.',
        'governance_domain': 'Clinical Adoption',
        'id': 'AI-RISK-100',
        'inherent_severity': 'High',
        'mitigating_control_ref': 'AI-CONTROL-020',
        'residual_risk': 'Low (Controlled through mandatory human approval & '
                         'circuit breakers)',
        'title': 'Lack of Explainability & Clinician Distrust #100'}]

AI_CONTROLS = [   {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Procedural & Technical Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-001',
        'mechanism': 'Physician affirmative acceptance required before any '
                     'advisory output commits to patient chart.',
        'title': 'Mandatory Human-in-the-Loop Physician Review #001'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Algorithmic Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-002',
        'mechanism': 'Model suppresses prediction if softmax confidence is '
                     'below 0.85; returns fallback heuristic.',
        'title': 'Automated Model Abstention on Low Confidence #002'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Explainable AI (XAI) Engine',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-003',
        'mechanism': 'Top 3 contributing clinical features displayed alongside '
                     'prediction for transparent clinician review.',
        'title': 'SHAP Explainability Feature Attribution #003'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Input Validation Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-004',
        'mechanism': 'Inputs outside Mahalanobis distance 3.0 rejected with '
                     'instant fall-through to standard protocol.',
        'title': 'Out-of-Distribution (OOD) Input Sanitizer #004'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'System Reliability Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-005',
        'mechanism': 'Inference daemon switches to static moving-average '
                     'baseline if error rate exceeds 1.0% over 5m.',
        'title': 'Automated Circuit Breaker & Fallback Heuristic #005'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Fairness Quality Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-006',
        'mechanism': 'Quarterly bias testing blocking deployment if '
                     'demographic ratio deviates beyond 0.80 - 1.25.',
        'title': 'Demographic Parity Audit & Disparate Impact Blocker #006'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Telemetry Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-007',
        'mechanism': 'Prometheus alarm triggers if PSI exceeds 0.10, notifying '
                     'MLOps engineer for retraining.',
        'title': 'Continuous Population Stability Index (PSI) Monitor #007'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Supply Chain Security',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-008',
        'mechanism': 'ONNX binaries signed with municipal PKI key; signature '
                     'verified at runtime pod initialization.',
        'title': 'Cryptographic Model Artifact Signing & Verification #008'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Procedural & Technical Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-009',
        'mechanism': 'Physician affirmative acceptance required before any '
                     'advisory output commits to patient chart.',
        'title': 'Mandatory Human-in-the-Loop Physician Review #009'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Algorithmic Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-010',
        'mechanism': 'Model suppresses prediction if softmax confidence is '
                     'below 0.85; returns fallback heuristic.',
        'title': 'Automated Model Abstention on Low Confidence #010'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Explainable AI (XAI) Engine',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-011',
        'mechanism': 'Top 3 contributing clinical features displayed alongside '
                     'prediction for transparent clinician review.',
        'title': 'SHAP Explainability Feature Attribution #011'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Input Validation Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-012',
        'mechanism': 'Inputs outside Mahalanobis distance 3.0 rejected with '
                     'instant fall-through to standard protocol.',
        'title': 'Out-of-Distribution (OOD) Input Sanitizer #012'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'System Reliability Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-013',
        'mechanism': 'Inference daemon switches to static moving-average '
                     'baseline if error rate exceeds 1.0% over 5m.',
        'title': 'Automated Circuit Breaker & Fallback Heuristic #013'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Fairness Quality Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-014',
        'mechanism': 'Quarterly bias testing blocking deployment if '
                     'demographic ratio deviates beyond 0.80 - 1.25.',
        'title': 'Demographic Parity Audit & Disparate Impact Blocker #014'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Telemetry Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-015',
        'mechanism': 'Prometheus alarm triggers if PSI exceeds 0.10, notifying '
                     'MLOps engineer for retraining.',
        'title': 'Continuous Population Stability Index (PSI) Monitor #015'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Supply Chain Security',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-016',
        'mechanism': 'ONNX binaries signed with municipal PKI key; signature '
                     'verified at runtime pod initialization.',
        'title': 'Cryptographic Model Artifact Signing & Verification #016'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Procedural & Technical Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-017',
        'mechanism': 'Physician affirmative acceptance required before any '
                     'advisory output commits to patient chart.',
        'title': 'Mandatory Human-in-the-Loop Physician Review #017'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Algorithmic Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-018',
        'mechanism': 'Model suppresses prediction if softmax confidence is '
                     'below 0.85; returns fallback heuristic.',
        'title': 'Automated Model Abstention on Low Confidence #018'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Explainable AI (XAI) Engine',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-019',
        'mechanism': 'Top 3 contributing clinical features displayed alongside '
                     'prediction for transparent clinician review.',
        'title': 'SHAP Explainability Feature Attribution #019'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Input Validation Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-020',
        'mechanism': 'Inputs outside Mahalanobis distance 3.0 rejected with '
                     'instant fall-through to standard protocol.',
        'title': 'Out-of-Distribution (OOD) Input Sanitizer #020'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'System Reliability Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-021',
        'mechanism': 'Inference daemon switches to static moving-average '
                     'baseline if error rate exceeds 1.0% over 5m.',
        'title': 'Automated Circuit Breaker & Fallback Heuristic #021'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Fairness Quality Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-022',
        'mechanism': 'Quarterly bias testing blocking deployment if '
                     'demographic ratio deviates beyond 0.80 - 1.25.',
        'title': 'Demographic Parity Audit & Disparate Impact Blocker #022'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Telemetry Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-023',
        'mechanism': 'Prometheus alarm triggers if PSI exceeds 0.10, notifying '
                     'MLOps engineer for retraining.',
        'title': 'Continuous Population Stability Index (PSI) Monitor #023'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Supply Chain Security',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-024',
        'mechanism': 'ONNX binaries signed with municipal PKI key; signature '
                     'verified at runtime pod initialization.',
        'title': 'Cryptographic Model Artifact Signing & Verification #024'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Procedural & Technical Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-025',
        'mechanism': 'Physician affirmative acceptance required before any '
                     'advisory output commits to patient chart.',
        'title': 'Mandatory Human-in-the-Loop Physician Review #025'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Algorithmic Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-026',
        'mechanism': 'Model suppresses prediction if softmax confidence is '
                     'below 0.85; returns fallback heuristic.',
        'title': 'Automated Model Abstention on Low Confidence #026'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Explainable AI (XAI) Engine',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-027',
        'mechanism': 'Top 3 contributing clinical features displayed alongside '
                     'prediction for transparent clinician review.',
        'title': 'SHAP Explainability Feature Attribution #027'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Input Validation Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-028',
        'mechanism': 'Inputs outside Mahalanobis distance 3.0 rejected with '
                     'instant fall-through to standard protocol.',
        'title': 'Out-of-Distribution (OOD) Input Sanitizer #028'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'System Reliability Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-029',
        'mechanism': 'Inference daemon switches to static moving-average '
                     'baseline if error rate exceeds 1.0% over 5m.',
        'title': 'Automated Circuit Breaker & Fallback Heuristic #029'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Fairness Quality Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-030',
        'mechanism': 'Quarterly bias testing blocking deployment if '
                     'demographic ratio deviates beyond 0.80 - 1.25.',
        'title': 'Demographic Parity Audit & Disparate Impact Blocker #030'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Telemetry Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-031',
        'mechanism': 'Prometheus alarm triggers if PSI exceeds 0.10, notifying '
                     'MLOps engineer for retraining.',
        'title': 'Continuous Population Stability Index (PSI) Monitor #031'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Supply Chain Security',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-032',
        'mechanism': 'ONNX binaries signed with municipal PKI key; signature '
                     'verified at runtime pod initialization.',
        'title': 'Cryptographic Model Artifact Signing & Verification #032'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Procedural & Technical Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-033',
        'mechanism': 'Physician affirmative acceptance required before any '
                     'advisory output commits to patient chart.',
        'title': 'Mandatory Human-in-the-Loop Physician Review #033'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Algorithmic Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-034',
        'mechanism': 'Model suppresses prediction if softmax confidence is '
                     'below 0.85; returns fallback heuristic.',
        'title': 'Automated Model Abstention on Low Confidence #034'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Explainable AI (XAI) Engine',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-035',
        'mechanism': 'Top 3 contributing clinical features displayed alongside '
                     'prediction for transparent clinician review.',
        'title': 'SHAP Explainability Feature Attribution #035'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Input Validation Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-036',
        'mechanism': 'Inputs outside Mahalanobis distance 3.0 rejected with '
                     'instant fall-through to standard protocol.',
        'title': 'Out-of-Distribution (OOD) Input Sanitizer #036'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'System Reliability Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-037',
        'mechanism': 'Inference daemon switches to static moving-average '
                     'baseline if error rate exceeds 1.0% over 5m.',
        'title': 'Automated Circuit Breaker & Fallback Heuristic #037'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Fairness Quality Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-038',
        'mechanism': 'Quarterly bias testing blocking deployment if '
                     'demographic ratio deviates beyond 0.80 - 1.25.',
        'title': 'Demographic Parity Audit & Disparate Impact Blocker #038'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Telemetry Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-039',
        'mechanism': 'Prometheus alarm triggers if PSI exceeds 0.10, notifying '
                     'MLOps engineer for retraining.',
        'title': 'Continuous Population Stability Index (PSI) Monitor #039'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Supply Chain Security',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-040',
        'mechanism': 'ONNX binaries signed with municipal PKI key; signature '
                     'verified at runtime pod initialization.',
        'title': 'Cryptographic Model Artifact Signing & Verification #040'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Procedural & Technical Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-041',
        'mechanism': 'Physician affirmative acceptance required before any '
                     'advisory output commits to patient chart.',
        'title': 'Mandatory Human-in-the-Loop Physician Review #041'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Algorithmic Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-042',
        'mechanism': 'Model suppresses prediction if softmax confidence is '
                     'below 0.85; returns fallback heuristic.',
        'title': 'Automated Model Abstention on Low Confidence #042'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Explainable AI (XAI) Engine',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-043',
        'mechanism': 'Top 3 contributing clinical features displayed alongside '
                     'prediction for transparent clinician review.',
        'title': 'SHAP Explainability Feature Attribution #043'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Input Validation Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-044',
        'mechanism': 'Inputs outside Mahalanobis distance 3.0 rejected with '
                     'instant fall-through to standard protocol.',
        'title': 'Out-of-Distribution (OOD) Input Sanitizer #044'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'System Reliability Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-045',
        'mechanism': 'Inference daemon switches to static moving-average '
                     'baseline if error rate exceeds 1.0% over 5m.',
        'title': 'Automated Circuit Breaker & Fallback Heuristic #045'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Fairness Quality Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-046',
        'mechanism': 'Quarterly bias testing blocking deployment if '
                     'demographic ratio deviates beyond 0.80 - 1.25.',
        'title': 'Demographic Parity Audit & Disparate Impact Blocker #046'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Telemetry Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-047',
        'mechanism': 'Prometheus alarm triggers if PSI exceeds 0.10, notifying '
                     'MLOps engineer for retraining.',
        'title': 'Continuous Population Stability Index (PSI) Monitor #047'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Supply Chain Security',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-048',
        'mechanism': 'ONNX binaries signed with municipal PKI key; signature '
                     'verified at runtime pod initialization.',
        'title': 'Cryptographic Model Artifact Signing & Verification #048'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Procedural & Technical Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-049',
        'mechanism': 'Physician affirmative acceptance required before any '
                     'advisory output commits to patient chart.',
        'title': 'Mandatory Human-in-the-Loop Physician Review #049'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Algorithmic Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-050',
        'mechanism': 'Model suppresses prediction if softmax confidence is '
                     'below 0.85; returns fallback heuristic.',
        'title': 'Automated Model Abstention on Low Confidence #050'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Explainable AI (XAI) Engine',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-051',
        'mechanism': 'Top 3 contributing clinical features displayed alongside '
                     'prediction for transparent clinician review.',
        'title': 'SHAP Explainability Feature Attribution #051'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Input Validation Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-052',
        'mechanism': 'Inputs outside Mahalanobis distance 3.0 rejected with '
                     'instant fall-through to standard protocol.',
        'title': 'Out-of-Distribution (OOD) Input Sanitizer #052'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'System Reliability Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-053',
        'mechanism': 'Inference daemon switches to static moving-average '
                     'baseline if error rate exceeds 1.0% over 5m.',
        'title': 'Automated Circuit Breaker & Fallback Heuristic #053'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Fairness Quality Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-054',
        'mechanism': 'Quarterly bias testing blocking deployment if '
                     'demographic ratio deviates beyond 0.80 - 1.25.',
        'title': 'Demographic Parity Audit & Disparate Impact Blocker #054'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Telemetry Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-055',
        'mechanism': 'Prometheus alarm triggers if PSI exceeds 0.10, notifying '
                     'MLOps engineer for retraining.',
        'title': 'Continuous Population Stability Index (PSI) Monitor #055'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Supply Chain Security',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-056',
        'mechanism': 'ONNX binaries signed with municipal PKI key; signature '
                     'verified at runtime pod initialization.',
        'title': 'Cryptographic Model Artifact Signing & Verification #056'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Procedural & Technical Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-057',
        'mechanism': 'Physician affirmative acceptance required before any '
                     'advisory output commits to patient chart.',
        'title': 'Mandatory Human-in-the-Loop Physician Review #057'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Algorithmic Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-058',
        'mechanism': 'Model suppresses prediction if softmax confidence is '
                     'below 0.85; returns fallback heuristic.',
        'title': 'Automated Model Abstention on Low Confidence #058'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Explainable AI (XAI) Engine',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-059',
        'mechanism': 'Top 3 contributing clinical features displayed alongside '
                     'prediction for transparent clinician review.',
        'title': 'SHAP Explainability Feature Attribution #059'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Input Validation Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-060',
        'mechanism': 'Inputs outside Mahalanobis distance 3.0 rejected with '
                     'instant fall-through to standard protocol.',
        'title': 'Out-of-Distribution (OOD) Input Sanitizer #060'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'System Reliability Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-061',
        'mechanism': 'Inference daemon switches to static moving-average '
                     'baseline if error rate exceeds 1.0% over 5m.',
        'title': 'Automated Circuit Breaker & Fallback Heuristic #061'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Fairness Quality Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-062',
        'mechanism': 'Quarterly bias testing blocking deployment if '
                     'demographic ratio deviates beyond 0.80 - 1.25.',
        'title': 'Demographic Parity Audit & Disparate Impact Blocker #062'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Telemetry Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-063',
        'mechanism': 'Prometheus alarm triggers if PSI exceeds 0.10, notifying '
                     'MLOps engineer for retraining.',
        'title': 'Continuous Population Stability Index (PSI) Monitor #063'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Supply Chain Security',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-064',
        'mechanism': 'ONNX binaries signed with municipal PKI key; signature '
                     'verified at runtime pod initialization.',
        'title': 'Cryptographic Model Artifact Signing & Verification #064'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Procedural & Technical Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-065',
        'mechanism': 'Physician affirmative acceptance required before any '
                     'advisory output commits to patient chart.',
        'title': 'Mandatory Human-in-the-Loop Physician Review #065'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Algorithmic Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-066',
        'mechanism': 'Model suppresses prediction if softmax confidence is '
                     'below 0.85; returns fallback heuristic.',
        'title': 'Automated Model Abstention on Low Confidence #066'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Explainable AI (XAI) Engine',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-067',
        'mechanism': 'Top 3 contributing clinical features displayed alongside '
                     'prediction for transparent clinician review.',
        'title': 'SHAP Explainability Feature Attribution #067'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Input Validation Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-068',
        'mechanism': 'Inputs outside Mahalanobis distance 3.0 rejected with '
                     'instant fall-through to standard protocol.',
        'title': 'Out-of-Distribution (OOD) Input Sanitizer #068'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'System Reliability Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-069',
        'mechanism': 'Inference daemon switches to static moving-average '
                     'baseline if error rate exceeds 1.0% over 5m.',
        'title': 'Automated Circuit Breaker & Fallback Heuristic #069'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Fairness Quality Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-070',
        'mechanism': 'Quarterly bias testing blocking deployment if '
                     'demographic ratio deviates beyond 0.80 - 1.25.',
        'title': 'Demographic Parity Audit & Disparate Impact Blocker #070'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Telemetry Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-071',
        'mechanism': 'Prometheus alarm triggers if PSI exceeds 0.10, notifying '
                     'MLOps engineer for retraining.',
        'title': 'Continuous Population Stability Index (PSI) Monitor #071'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Supply Chain Security',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-072',
        'mechanism': 'ONNX binaries signed with municipal PKI key; signature '
                     'verified at runtime pod initialization.',
        'title': 'Cryptographic Model Artifact Signing & Verification #072'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Procedural & Technical Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-073',
        'mechanism': 'Physician affirmative acceptance required before any '
                     'advisory output commits to patient chart.',
        'title': 'Mandatory Human-in-the-Loop Physician Review #073'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Algorithmic Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-074',
        'mechanism': 'Model suppresses prediction if softmax confidence is '
                     'below 0.85; returns fallback heuristic.',
        'title': 'Automated Model Abstention on Low Confidence #074'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Explainable AI (XAI) Engine',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-075',
        'mechanism': 'Top 3 contributing clinical features displayed alongside '
                     'prediction for transparent clinician review.',
        'title': 'SHAP Explainability Feature Attribution #075'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Input Validation Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-076',
        'mechanism': 'Inputs outside Mahalanobis distance 3.0 rejected with '
                     'instant fall-through to standard protocol.',
        'title': 'Out-of-Distribution (OOD) Input Sanitizer #076'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'System Reliability Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-077',
        'mechanism': 'Inference daemon switches to static moving-average '
                     'baseline if error rate exceeds 1.0% over 5m.',
        'title': 'Automated Circuit Breaker & Fallback Heuristic #077'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Fairness Quality Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-078',
        'mechanism': 'Quarterly bias testing blocking deployment if '
                     'demographic ratio deviates beyond 0.80 - 1.25.',
        'title': 'Demographic Parity Audit & Disparate Impact Blocker #078'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Telemetry Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-079',
        'mechanism': 'Prometheus alarm triggers if PSI exceeds 0.10, notifying '
                     'MLOps engineer for retraining.',
        'title': 'Continuous Population Stability Index (PSI) Monitor #079'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Supply Chain Security',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-080',
        'mechanism': 'ONNX binaries signed with municipal PKI key; signature '
                     'verified at runtime pod initialization.',
        'title': 'Cryptographic Model Artifact Signing & Verification #080'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Procedural & Technical Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-081',
        'mechanism': 'Physician affirmative acceptance required before any '
                     'advisory output commits to patient chart.',
        'title': 'Mandatory Human-in-the-Loop Physician Review #081'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Algorithmic Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-082',
        'mechanism': 'Model suppresses prediction if softmax confidence is '
                     'below 0.85; returns fallback heuristic.',
        'title': 'Automated Model Abstention on Low Confidence #082'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Explainable AI (XAI) Engine',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-083',
        'mechanism': 'Top 3 contributing clinical features displayed alongside '
                     'prediction for transparent clinician review.',
        'title': 'SHAP Explainability Feature Attribution #083'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Input Validation Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-084',
        'mechanism': 'Inputs outside Mahalanobis distance 3.0 rejected with '
                     'instant fall-through to standard protocol.',
        'title': 'Out-of-Distribution (OOD) Input Sanitizer #084'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'System Reliability Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-085',
        'mechanism': 'Inference daemon switches to static moving-average '
                     'baseline if error rate exceeds 1.0% over 5m.',
        'title': 'Automated Circuit Breaker & Fallback Heuristic #085'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Fairness Quality Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-086',
        'mechanism': 'Quarterly bias testing blocking deployment if '
                     'demographic ratio deviates beyond 0.80 - 1.25.',
        'title': 'Demographic Parity Audit & Disparate Impact Blocker #086'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Telemetry Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-087',
        'mechanism': 'Prometheus alarm triggers if PSI exceeds 0.10, notifying '
                     'MLOps engineer for retraining.',
        'title': 'Continuous Population Stability Index (PSI) Monitor #087'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Supply Chain Security',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-088',
        'mechanism': 'ONNX binaries signed with municipal PKI key; signature '
                     'verified at runtime pod initialization.',
        'title': 'Cryptographic Model Artifact Signing & Verification #088'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Procedural & Technical Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-089',
        'mechanism': 'Physician affirmative acceptance required before any '
                     'advisory output commits to patient chart.',
        'title': 'Mandatory Human-in-the-Loop Physician Review #089'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Algorithmic Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-090',
        'mechanism': 'Model suppresses prediction if softmax confidence is '
                     'below 0.85; returns fallback heuristic.',
        'title': 'Automated Model Abstention on Low Confidence #090'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Explainable AI (XAI) Engine',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-091',
        'mechanism': 'Top 3 contributing clinical features displayed alongside '
                     'prediction for transparent clinician review.',
        'title': 'SHAP Explainability Feature Attribution #091'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Input Validation Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-092',
        'mechanism': 'Inputs outside Mahalanobis distance 3.0 rejected with '
                     'instant fall-through to standard protocol.',
        'title': 'Out-of-Distribution (OOD) Input Sanitizer #092'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'System Reliability Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-093',
        'mechanism': 'Inference daemon switches to static moving-average '
                     'baseline if error rate exceeds 1.0% over 5m.',
        'title': 'Automated Circuit Breaker & Fallback Heuristic #093'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Fairness Quality Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-094',
        'mechanism': 'Quarterly bias testing blocking deployment if '
                     'demographic ratio deviates beyond 0.80 - 1.25.',
        'title': 'Demographic Parity Audit & Disparate Impact Blocker #094'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Telemetry Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-095',
        'mechanism': 'Prometheus alarm triggers if PSI exceeds 0.10, notifying '
                     'MLOps engineer for retraining.',
        'title': 'Continuous Population Stability Index (PSI) Monitor #095'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Supply Chain Security',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-096',
        'mechanism': 'ONNX binaries signed with municipal PKI key; signature '
                     'verified at runtime pod initialization.',
        'title': 'Cryptographic Model Artifact Signing & Verification #096'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Procedural & Technical Gate',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-097',
        'mechanism': 'Physician affirmative acceptance required before any '
                     'advisory output commits to patient chart.',
        'title': 'Mandatory Human-in-the-Loop Physician Review #097'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Algorithmic Guardrail',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-098',
        'mechanism': 'Model suppresses prediction if softmax confidence is '
                     'below 0.85; returns fallback heuristic.',
        'title': 'Automated Model Abstention on Low Confidence #098'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Explainable AI (XAI) Engine',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-099',
        'mechanism': 'Top 3 contributing clinical features displayed alongside '
                     'prediction for transparent clinician review.',
        'title': 'SHAP Explainability Feature Attribution #099'},
    {   'audit_trail_destination': 'Immutable WORM Audit Ledger (PostgreSQL & '
                                   'S3 Glacier Vault)',
        'control_type': 'Input Validation Guard',
        'enforcement_point': 'API Gateway / ONNX Inference Daemon / Doctor '
                             'Workstation PWA',
        'id': 'AI-CONTROL-100',
        'mechanism': 'Inputs outside Mahalanobis distance 3.0 rejected with '
                     'instant fall-through to standard protocol.',
        'title': 'Out-of-Distribution (OOD) Input Sanitizer #100'}]
