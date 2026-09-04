#!/usr/bin/env python3
"""
build_data_br.py
Builds the canonical data_br.py containing BR-001 through BR-050.
Includes complete business requirement metrics:
- baseline state
- target state
- business metric
- measurement method
- data source
- owner
- frequency
- threshold
- success condition
- failure condition
plus all standard fields and upstream/downstream traceability.
"""

import os

BR_DEFINITIONS = [
    # 1-10: Public Health Objectives & Access
    ("BR-001", "Universal Urban Slum Primary Healthcare Access",
     "The platform shall support seamless walk-in primary care delivery across all 183 clinics, eliminating geographical and economic barriers for urban poor populations.",
     "Population Health", "MUST", "Ensures equitable primary healthcare access for 1.2M slum residents in Bengaluru.",
     "Urban slum populations in Bengaluru face a 42% deficit in timely primary consultation access.",
     "Data Entry Operator", "PERSONA-002", "ROLE-002", "STAKEHOLDER-001",
     "Walk-in citizen arrives at clinic desk", "Citizen presents at registration counter during 09:00-17:30",
     "Citizen demographic details, ward number, slum cluster identification", "Phone number regex, ward ID in 1-243",
     "09:00 - 17:30 daily operational window", "42% slum coverage baseline", "85% primary care coverage in target wards",
     "Primary consultation coverage percentage", "Monthly aggregated ward census vs OPD registration",
     "BBMP HMIS & Namma Clinic DB", "Chief Health Officer (CHO)", "Monthly", ">=80% coverage",
     "Coverage exceeds 80% across all 243 wards", "Coverage falls below 70% in vulnerable slums"),

    ("BR-002", "Outpatient Department (OPD) Queue Wait Time Reduction",
     "The platform shall enforce a digital queue management workflow reducing total patient clinic dwell time from registration to medication dispensing.",
     "Operational Efficiency", "MUST", "Reduces patient wait time and wage loss for daily wage earners.",
     "Average clinic wait time exceeds 85 minutes, causing 18% patient abandonment before consultation.",
     "Data Entry Operator", "PERSONA-002", "ROLE-002", "STAKEHOLDER-003",
     "Patient token issued at front desk", "Patient registered and vitals recorded",
     "Token number, priority category, arrival timestamp", "Timestamp validation, sequence monotonicity",
     "Clinic operating hours", "Average dwell time: 85 minutes", "Average dwell time: <25 minutes",
     "Total patient clinic dwell time (p75)", "Automated token timestamp delta across desk touchpoints",
     "PostgreSQL queue_tokens table", "Zonal Health Officer (ZHO)", "Daily real-time", "<30 minutes",
     "75% of patients complete consultation and dispensing in <25 mins", "Average dwell time exceeds 45 mins for 3 consecutive days"),

    ("BR-003", "Maternal Health Antenatal Care (ANC) Protocol Tracking",
     "The platform shall track antenatal care registration, mandatory visits (ANC 1-4), high-risk pregnancy screening, and institutional delivery linkage.",
     "Maternal Health", "MUST", "Reduces maternal mortality and detects high-risk pregnancies early.",
     "Early ANC registration is currently at 58% in urban slum catchments.",
     "Staff Nurse", "PERSONA-003", "ROLE-003", "STAKEHOLDER-002",
     "Pregnant woman visits clinic or identified by ASHA", "First trimester confirmation or subsequent trimester visit",
     "LMP date, gestational age, parity, gravidity, blood pressure, hemoglobin, urine protein", "LMP within past 42 weeks, valid physiological ranges",
     "Active pregnancy cohort registered in clinic ward", "58% early registration, 48% 4-visit completion", "85% early registration, 80% 4-visit completion",
     "ANC-4 visit completion rate and high-risk identification rate", "Quarterly RCH cohort tracking",
     "Maternal health registry / DuckDB mart", "Maternal & Child Health Officer", "Weekly", ">=75%",
     "ANC-4 completion reaches >=80% with zero unmanaged high-risk dropouts", "ANC dropout rate exceeds 20%"),

    ("BR-004", "Non-Communicable Disease (NCD) Screening & Longitudinal Control",
     "The platform shall standardize adult population screening for hypertension and diabetes, enabling longitudinal treatment adherence monitoring.",
     "Chronic Care", "MUST", "Arrests microvascular and macrovascular complications through community-level control.",
     "Bengaluru urban poor exhibit 31% prevalence of hypertension with <22% achieving blood pressure control.",
     "Medical Officer", "PERSONA-001", "ROLE-001", "STAKEHOLDER-004",
     "Patient aged >=30 years presents at clinic", "No active hypertensive crisis requiring immediate tertiary transfer",
     "Blood pressure (systolic/diastolic), random blood sugar, fasting blood sugar, BMI", "SBP 60-260, DBP 40-160, RBS 40-600 mg/dL",
     "Clinic open for adult screening", "22% NCD blood pressure and glycemic control", "60% controlled cohort at 6 months",
     "Percentage of registered hypertensive/diabetic patients with controlled vitals", "Monthly cohort vitals analysis",
     "NCD clinical cohort registry", "State NCD Program Officer", "Monthly", ">=55%",
     "Cohort control rate >=60% with refill adherence >=80%", "Lost-to-follow-up rate exceeds 30%"),

    ("BR-005", "Essential Drug List (EDL) Zero Stockout Assurance",
     "The platform shall enforce real-time 120 Essential Drug List inventory tracking, preventing facility-level stockouts of life-saving primary medications.",
     "Supply Chain", "MUST", "Eliminates out-of-pocket medication expenses for low-income citizens.",
     "Namma Clinics report an average 14% stockout rate for essential antihypertensives and antibiotics.",
     "Pharmacist", "PERSONA-004", "ROLE-004", "STAKEHOLDER-005",
     "Medication dispensed or daily closing inventory tallied", "Medication on Karnataka EDL master list",
     "Drug batch ID, quantity dispensed, current balance, expiry date", "Quantity > 0, batch exists in active inventory",
     "Valid clinic pharmacy stock ledger", "14% stockout rate across 120 EDL drugs", "<2% stockout rate for core EDL drugs",
     "Percentage of facility days with zero stockout of Top 30 vital medicines", "Automated daily stock audit against buffer threshold",
     "Pharmacy inventory ledger", "Chief Pharmacist / BBMP Logistics Lead", "Daily", "<2% stockout",
     "Zero stockout days for Top 30 EDL items across 95% of clinics", "Any Tier-1 essential drug out of stock for >48 hours"),

    ("BR-006", "Point-of-Care Laboratory Rapid Diagnostic Turnaround",
     "The platform shall track specimen processing and results for 14 primary diagnostic tests, ensuring results are available within the same patient visit.",
     "Diagnostics", "MUST", "Enables evidence-based clinical prescribing without secondary visits.",
     "Diagnostic results currently take 24-48 hours when routed to external labs, causing 35% treatment delay.",
     "Lab Technician", "PERSONA-005", "ROLE-005", "STAKEHOLDER-002",
     "Medical Officer orders point-of-care test", "Patient present in clinic, test kit in stock",
     "Test order ID, sample type, reagent lot number, quantitative/qualitative result", "Result within clinical physiological bounds",
     "Active laboratory worklist", "Average turnaround time: 32 hours (external)", "Turnaround time: <20 minutes in-clinic",
     "Point-of-care test order-to-result turnaround time (p90)", "System timestamps from order creation to result sign-off",
     "Laboratory diagnostics database", "BBMP Diagnostic Coordinator", "Daily", "<20 mins",
     "90% of rapid diagnostic orders signed off in <20 minutes", "Same-day result completion falls below 85%"),

    ("BR-007", "Secondary & Tertiary Care Referral Loop Closure",
     "The platform shall generate encrypted digital referral slips to BBMP referral hospitals and track counter-referral clinical discharge summaries.",
     "Care Continuity", "MUST", "Prevents clinical dropped-balls during acute or specialized care escalations.",
     "Referral loop closure is currently <8%, with primary clinics unaware of hospital admission outcomes.",
     "Medical Officer", "PERSONA-001", "ROLE-001", "STAKEHOLDER-006",
     "Medical Officer identifies clinical condition exceeding primary capability", "Patient evaluated and stabilized at Namma Clinic",
     "Referral facility code, provisional diagnosis, clinical urgency, referral summary", "Valid facility in BBMP hospital registry",
     "Patient consents to referral transfer", "8% referral feedback rate", "65% counter-referral loop closure rate",
     "Percentage of secondary referrals with confirmed admission or discharge slip", "Bi-directional hospital integration exchange",
     "Referral exchange gateway", "Hospital Superintendent Liaison", "Weekly", ">=60%",
     "Referral tracking confirmed in >=65% of secondary transfers", "Unresolved referrals exceed 40% after 14 days"),

    ("BR-008", "Syndromic Infectious Disease Outbreak Early Warning",
     "The platform shall aggregate ward-level fever, respiratory, and diarrheal illness clusters in real time, triggering automated epidemiological surveillance alerts.",
     "Epidemiological Surveillance", "MUST", "Prevents dengue, typhoid, and cholera outbreaks in high-density urban wards.",
     "Outbreak detection relies on paper-based weekly returns with a 9-14 day reporting latency.",
     "Medical Officer", "PERSONA-001", "ROLE-001", "STAKEHOLDER-007",
     "Doctor records syndromic fever or acute diarrheal diagnosis", "Patient residence mapped to valid BBMP ward",
     "Syndrome category, ward code, patient age group, rapid test confirmation", "Standardized IHIP syndrome taxonomy",
     "Clinic operating in target surveillance zone", "Reporting latency: 9-14 days", "Surveillance alert latency: <4 hours",
     "Time from cluster threshold breach to ZHO automated alert dispatch", "DuckDB spatio-temporal cluster analysis",
     "Public health surveillance datamart", "District Surveillance Officer (DSO)", "Continuous real-time", "<4 hours",
     "Cluster detection occurs within 4 hours of index case cluster trigger", "Unreported syndromic cluster exceeding 5 cases in 48 hours"),

    ("BR-009", "100% Offline Autonomous Clinic Operation",
     "The platform shall guarantee uninterrupted clinic operations during prolonged municipal power or WAN internet network failures.",
     "Business Continuity", "MUST", "Ensures zero citizen denial of care during frequent urban infrastructure disruptions.",
     "Clinics experience an average of 3.8 hours of daily network instability or outage.",
     "All Clinic Staff", "PERSONA-002", "ROLE-002", "STAKEHOLDER-003",
     "WAN connectivity drops below operational threshold", "Local clinic workstation powered via UPS or inverter",
     "Local patient lookup, cached formulary, local queue mutations", "Cryptographic local transaction validity",
     "Dexie.js IndexedDB operational on local browser", "Operations halt during network loss (paper fallback)", "8 hours continuous zero-degradation offline service",
     "Zero service denial incidents attributable to network failure", "System offline operational logs and sync journal",
     "Local workstation sync telemetry", "Director of IT Operations", "Daily", "0 downtime incidents",
     "100% of walk-in patients served without delay during 8-hour network cut", "Any clinic forced to revert to manual paper due to software freeze"),

    ("BR-010", "Digital Personal Data Protection (DPDP) Act Compliance",
     "The platform shall enforce citizen consent capture, purpose limitation, and cryptographic protection of personal health data under the DPDP Act 2023.",
     "Governance & Privacy", "MUST", "Protects citizen constitutional right to privacy and prevents municipal legal liability.",
     "Legacy paper registers leave patient phone numbers and diagnoses publicly exposed on clinic desks.",
     "Data Entry Operator", "PERSONA-002", "ROLE-002", "STAKEHOLDER-008",
     "Patient registration or record access request", "Patient informed of data collection purpose in Kannada/English",
     "Consent artifact, purpose category, timestamp, operator signature", "Valid consent format per BBMP legal guidelines",
     "Registration workflow active", "Zero formal privacy controls", "100% auditable consent capture & encryption",
     "Consent compliance audit pass rate", "WORM immutable audit log verification",
     "Compliance audit trail repository", "Data Protection Officer (DPO)", "Monthly", "100%",
     "100% consent capture with zero privacy non-compliance findings", "Any unconsented health data processing or plaintext PII leak"),

    # 11-20: Clinic Productivity, Clinical Quality & Diagnostics
    ("BR-011", "Consultation Cycle Time Optimization",
     "The platform shall streamline clinical documentation via 1-click chief complaint chips and standardized templates to maintain <4 minute doctor consultations.",
     "Clinical Productivity", "MUST", "Prevents doctor burnout while handling 80+ patients per 4-hour OPD shift.",
     "Doctors spend 6.5 minutes per patient on manual paper writing, creating long waiting room queues.",
     "Medical Officer", "PERSONA-001", "ROLE-001", "STAKEHOLDER-004",
     "Patient called into doctor consultation room", "Patient triage vitals completed and visible on screen",
     "Chief complaint selection, clinical notes, diagnosis code, prescription", "Mandatory diagnosis before prescription completion",
     "Patient in CONSULTING state", "Average consultation duration: 6.5 minutes", "Average consultation duration: 3.5 minutes",
     "Consultation duration (p50 and p90)", "EMR consultation start-to-finish timestamp delta",
     "Clinical consultation audit table", "Clinical Quality Committee", "Daily", "<4.0 mins",
     "p50 consultation duration <=3.5 mins with complete clinical notes", "p90 consultation duration exceeds 7.0 minutes"),

    ("BR-012", "Evidence-Based Prescription Safety & Formulary Adherence",
     "The platform shall enforce prescription safety boundaries, checking drug-drug contraindications and Karnataka EDL availability in real time.",
     "Patient Safety", "MUST", "Prevents adverse drug events and eliminates prescriptions for unavailable commercial drugs.",
     "18% of paper prescriptions contain non-formulary commercial drugs or unflagged adverse interactions.",
     "Medical Officer", "PERSONA-001", "ROLE-001", "STAKEHOLDER-002",
     "Doctor adds medication to electronic prescription", "Patient age, weight, and allergy history recorded",
     "Drug code, dose, route, frequency, duration, indication", "Valid dosage per Karnataka primary care formulary",
     "Active consultation prescription pane", "Formulary adherence: 82%, zero interaction screening", "Formulary adherence: >=98%, 100% interaction screening",
     "Percentage of electronic prescriptions strictly adhering to Karnataka 120 EDL", "Prescription formulary validation logs",
     "Prescription audit mart", "Pharmacy & Therapeutics Committee", "Weekly", ">=98%",
     "Formulary adherence >=98% with zero unacknowledged severe interaction alerts", "Formulary adherence falls below 95%"),

    ("BR-013", "Cold Chain & Vaccine Potency Assurance",
     "The platform shall log ILR refrigerator temperatures twice daily and alert when vaccine storage breaches the mandatory +2C to +8C threshold.",
     "Immunization Safety", "MUST", "Guarantees vaccine efficacy for infant immunizations across all urban clinics.",
     "Temperature logging is currently manual paper charting, resulting in delayed breach detection.",
     "Staff Nurse", "PERSONA-003", "ROLE-003", "STAKEHOLDER-009",
     "Morning (09:00) and evening (17:00) temperature inspection", "Active ILR unit containing vaccines",
     "Temperature reading (Celsius), power backup status, inspector ID", "Temperature within -10C to +30C sensor range",
     "Immunization clinic operational", "Manual paper logs with 24% missing entries", "100% digital logging with <15 min breach notification",
     "Cold chain temperature compliance rate", "Temperature telemetry logs in PostgreSQL",
     "Immunization cold chain register", "Zonal Immunization Officer", "Daily", "100% compliance",
     "Twice-daily logs completed for 100% of clinics with zero unaddressed temperature excursions", "Excursion > +8C for >2 hours without technician dispatch"),

    ("BR-014", "Pediatric Growth Monitoring & Malnutrition Triage",
     "The platform shall calculate automated WHO-standard Weight-for-Age and Height-for-Age percentiles for children under 5 years, flagging SAM cases.",
     "Child Health", "MUST", "Identifies Severe Acute Malnutrition (SAM) early for NRC nutritional rehabilitation referral.",
     "Under-5 malnutrition screening is currently opportunistic and rarely plotted on growth charts.",
     "Staff Nurse", "PERSONA-003", "ROLE-003", "STAKEHOLDER-002",
     "Child aged 0-59 months presents for triage", "Accurate infant scale and stadiometer available",
     "Date of birth, sex, weight (kg), height/length (cm), MUAC (mm)", "Weight 1-40 kg, height 40-140 cm, MUAC 50-250 mm",
     "Pediatric triage workflow active", "<15% growth plotting on manual cards", "100% automated z-score calculation and SAM flagging",
     "Screening percentage of under-5 pediatric attendances", "Pediatric triage clinical records",
     "Child health datamart", "MCH Program Coordinator", "Monthly", ">=90%",
     "100% of flagged SAM children receive structured referral to BBMP NRC", "Flagged SAM child discharged without referral counsel"),

    ("BR-015", "Communicable Disease Surveillance (IHIP/IDSP Integration)",
     "The platform shall auto-populate and transmit daily presumptive surveillance returns (Form P) directly to the Karnataka State IHIP portal.",
     "Disease Surveillance", "MUST", "Eliminates duplicate data entry and provides instant state epidemiological visibility.",
     "Medical Officers spend 45 minutes daily manually transcribing disease cases into paper registers and IHIP web forms.",
     "Medical Officer", "PERSONA-001", "ROLE-001", "STAKEHOLDER-007",
     "Daily OPD closure at 17:30 IST", "All OPD consultations finalized for the day",
     "Aggregated syndrome counts (fever, cough, diarrhea, jaundice, rash)", "Count reconciles with finalized consultation records",
     "Clinic daily session ended", "Manual dual entry taking 45 mins/day", "Automated 1-click transmission in <30 seconds",
     "Timeliness and completeness of daily IHIP Form P transmission", "IHIP integration webhook transaction logs",
     "Epidemiology exchange audit log", "State Epidemiologist", "Daily", "100% on-time",
     "100% of clinics submit verified Form P by 18:00 IST daily", "Clinic fails to submit daily return for 2 consecutive operating days"),

    ("BR-016", "First-Expired, First-Out (FEFO) Pharmacy Dispensing",
     "The platform shall guide pharmacy dispensing by strictly enforcing FEFO batch allocation, preventing medicine expiration on clinic shelves.",
     "Waste Reduction", "MUST", "Reduces municipal pharmaceutical wastage and ensures patients receive fresh stock.",
     "Annual medicine expiration wastage across municipal clinics is estimated at 6.8% of allocated budget.",
     "Pharmacist", "PERSONA-004", "ROLE-004", "STAKEHOLDER-005",
     "Pharmacist scans or selects e-prescription for fulfillment", "Active medicine inventory batches available in clinic store",
     "Prescription item code, batch number scanned, quantity picked", "Scanned batch matches earliest expiry batch in stock",
     "Dispensing counter active", "6.8% stock expiration rate", "<1.0% stock expiration rate",
     "Percentage of dispensed items matching earliest expiry batch", "Pharmacy dispensing batch audit logs",
     "Pharmacy stock ledger", "Assistant Controller of Stores (Health)", "Monthly", ">=95% FEFO compliance",
     "FEFO adherence >=95% and annual expiry loss <1.0%", "Batches expire on shelf while newer batches were dispensed"),

    ("BR-017", "Multi-Desk Real-Time Operational Queue Synchronization",
     "The platform shall synchronize patient queue status across Registration, Triage, Doctor, Lab, and Pharmacy desks in <1 second.",
     "Workflow Coordination", "MUST", "Eliminates patient physical wandering and shouting across clinic waiting halls.",
     "Patients physically search for where to go next, creating bottlenecks at doctor doors.",
     "All Clinic Staff", "PERSONA-002", "ROLE-002", "STAKEHOLDER-003",
     "Patient completes workflow stage at any clinic desk", "Patient has active valid token",
     "Token ID, completed stage, target desk, timestamp", "Valid workflow transition matrix",
     "Clinic local network or sync bridge active", "Zero inter-desk electronic synchronization", "Queue status update latency <1.0 second",
     "Inter-desk queue transition latency (p95)", "WebSocket / server-sent events latency telemetry",
     "Queue state telemetry table", "Operations Project Manager", "Continuous", "<1.0s",
     "Patient queue transitions display on destination desk within 1000ms", "Desk queue displays desynchronized state for >10 seconds"),

    ("BR-018", "Bilingual User Interface (Kannada and English) Support",
     "The platform shall provide complete, culturally validated Kannada and English interfaces with instant runtime toggling across all screens.",
     "Usability & Equity", "MUST", "Empowers local Kannada-speaking nursing and auxiliary staff while retaining clinical English terms.",
     "Staff with limited English literacy experience high data entry error rates and slower adoption.",
     "All Clinic Staff", "PERSONA-003", "ROLE-003", "STAKEHOLDER-010",
     "Staff selects language toggle or loads default profile", "User authenticated on clinic terminal",
     "Selected locale ('kn' or 'en')", "Valid supported ISO language code",
     "Any UI screen active", "Only English interfaces with ad-hoc manual translations", "100% localized Kannada strings with Noto Sans Kannada font",
     "Localization completeness audit score", "Static key extraction vs translation dictionary coverage",
     "i18n resource catalog", "Localization Coordinator", "Each Release", "100%",
     "Zero untranslated UI labels or broken font glyphs across all 17 workflows", "Hardcoded English string exposed to user in Kannada mode"),

    ("BR-019", "Universal ABHA Health ID Creation and Seeding",
     "The platform shall support instant ABHA creation and linking via Aadhaar OTP or demographic matching for walk-in citizens.",
     "Digital Health Integration", "MUST", "Integrates municipal primary care with the national Ayushman Bharat Digital Mission.",
     "Under 12% of attending urban poor patients possess an active, seeded ABHA number.",
     "Data Entry Operator", "PERSONA-002", "ROLE-002", "STAKEHOLDER-011",
     "Citizen presents Aadhaar card and consents to ABHA creation", "Active network or queued demographic payload",
     "Aadhaar number or OTP, demographic details, consent flag", "Aadhaar format checksum, valid 6-digit OTP",
     "Citizen registration desk active", "12% ABHA seeding rate", ">=75% ABHA seeding rate across registered patients",
     "Percentage of registered patients with verified ABHA link", "ABDM integration transaction ledger",
     "Patient master identity database", "Nodal Officer (ABDM Karnataka)", "Monthly", ">=70%",
     "ABHA seeding reaches >=75% with zero unauthorized Aadhaar storage", "Raw Aadhaar numbers stored in persistent database"),

    ("BR-020", "Standardized Thermal Paper Clinical Ticket Printing",
     "The platform shall print durable 58mm/80mm thermal paper slips with barcode/QR for tokens, prescriptions, and lab receipts without printer drivers.",
     "Operational Utility", "MUST", "Provides illiterate or elderly citizens with physical, readable visit tokens and pharmacy instructions.",
     "Handwritten tokens on scrap paper are frequently lost or misread, causing queue arguments.",
     "Data Entry Operator", "PERSONA-002", "ROLE-002", "STAKEHOLDER-003",
     "Operator confirms token generation or doctor finalizes prescription", "Thermal printer connected via USB or Web Serial",
     "Clinic name, token number, UHID, patient name, date/time, QR code", "Standard ESC/POS thermal printer command stream",
     "Workstation browser Web Serial permission granted", "Handwritten scrap paper tokens", "Instant thermal printing in <500ms",
     "Print failure rate and latency", "Client-side Web Serial print telemetry",
     "Client hardware error journal", "Frontline IT Support Lead", "Daily", "<0.5% failure",
     "100% of walk-in patients receive printed token slip in <500ms", "Printer failure causes registration desk queue stoppage"),

    # 21-30: Diagnostic Accuracy, Clinical Governance & Supply Chain
    ("BR-021", "Critical Panic Value Diagnostic Immediate Notification",
     "The platform shall trigger visual and audible panic alerts across the doctor and nurse terminals when a point-of-care lab test breaches danger limits.",
     "Patient Safety", "MUST", "Enables immediate emergency resuscitation or tertiary transfer before patient leaves clinic.",
     "Critical lab values (e.g. severe anemia, profound hypoglycemia) are lost in routine paper registers.",
     "Lab Technician", "PERSONA-005", "ROLE-005", "STAKEHOLDER-002",
     "Lab technician enters test result breaching predefined clinical panic threshold", "Test result verified by technician",
     "Test ID, patient UHID, analyte, measured value, panic severity code", "Value exceeds laboratory critical boundary (e.g. Hb < 6.0 g/dL)",
     "Consultation or waiting area active", "Zero automated alerts; manual verbal notification", "Immediate visual banner and audio chime within 15 seconds",
     "Time from critical result save to doctor terminal alert acknowledgment", "Critical alert audit log with doctor sign-off timestamp",
     "Laboratory panic alert register", "Clinical Safety Officer", "Continuous", "<30 seconds",
     "100% of panic values acknowledged by Medical Officer within 60 seconds", "Critical result saved without immediate doctor notification"),

    ("BR-022", "Automated Daily Indent Generation for Low Stock",
     "The platform shall calculate rolling 30-day consumption and auto-generate stock replenishment indents to the BBMP zonal warehouse.",
     "Supply Chain Efficiency", "MUST", "Prevents stockouts by automating complex manual inventory calculations.",
     "Pharmacists spend 3 hours weekly manually counting bottles and guessing indent quantities on paper forms.",
     "Pharmacist", "PERSONA-004", "ROLE-004", "STAKEHOLDER-005",
     "Inventory falls below minimum buffer threshold or scheduled weekly indent day", "Verified current physical stock ledger",
     "Drug code, current balance, average daily consumption, lead time, indent quantity", "Indent quantity calculated via standardized min-max formula",
     "Active pharmacy store profile", "Manual paper indents with 3-week replenishment lag", "Automated 1-click indent generation with 3-day turnaround",
     "Stock replenishment lead time and stockout incidence", "Warehouse indent order lifecycle timestamps",
     "Zonal warehouse logistics system", "BBMP Logistics Director", "Weekly", "<5 days lead time",
     "Automated indent submitted on time with replenishment delivered within 5 business days", "Indent delayed causing stockout of critical antibiotic"),

    ("BR-023", "Standardized ICD-10 Diagnostic Classification",
     "The platform shall guide clinicians with a curated primary care subset of ICD-10 diagnostic codes, eliminating uncodified free-text diagnoses.",
     "Clinical Governance", "MUST", "Enables accurate epidemiological disease burden analysis across Bengaluru's 8 zones.",
     "72% of paper diagnoses are illegible or idiosyncratic free-text (e.g. 'fvr', 'weakness').",
     "Medical Officer", "PERSONA-001", "ROLE-001", "STAKEHOLDER-004",
     "Doctor documents clinical diagnosis during consultation", "Patient history and examination evaluated",
     "ICD-10 search string or clinical syndrome chip", "Selected code exists in curated primary care ICD-10 catalog",
     "Active consultation session", "72% uncodified diagnoses", ">=95% diagnoses mapped to valid ICD-10 codes",
     "Percentage of finalized consultations with valid ICD-10 code", "Clinical diagnosis audit database",
     "Health intelligence analytics mart", "BBMP Epidemiological Director", "Monthly", ">=95%",
     "ICD-10 coding compliance reaches >=95% across all 183 clinics", "Uncodified diagnosis rate exceeds 10%"),

    ("BR-024", "Maternal Postnatal Care (PNC) Follow-Up Compliance",
     "The platform shall schedule and monitor mandatory postnatal visits within 48 hours, 7 days, 14 days, and 42 days post-delivery.",
     "Maternal Health", "MUST", "Detects postpartum hemorrhage, sepsis, and depression to reduce postnatal mortality.",
     "Postnatal visit tracking drops to 34% after institutional delivery discharge.",
     "Staff Nurse", "PERSONA-003", "ROLE-003", "STAKEHOLDER-002",
     "Birth event recorded or mother attends clinic with newborn", "Confirmed institutional or home delivery date",
     "Delivery date, baby birth weight, maternal vitals, lochia status, feeding status", "Delivery date <= current date, valid physiological ranges",
     "Postnatal registry active", "34% PNC follow-up completion", ">=75% PNC-4 completion",
     "Percentage of delivered mothers completing all 4 scheduled PNC visits", "RCH cohort tracking database",
     "Maternal health registry", "MCH Program Officer", "Monthly", ">=70%",
     "PNC-4 completion reaches >=75% with zero unmanaged maternal infections", "Severe postpartum complication unflagged in clinic records"),

    ("BR-025", "Elderly and Vulnerable Priority Queue Routing",
     "The platform shall automatically assign priority queue tokens to elderly citizens (age >=65), visibly pregnant women, and disabled individuals.",
     "Social Equity", "MUST", "Prevents physical distress and collapse among frail citizens in crowded clinic waiting rooms.",
     "Elderly patients must stand in identical queues with young adults for up to 90 minutes.",
     "Data Entry Operator", "PERSONA-002", "ROLE-002", "STAKEHOLDER-010",
     "Registration operator enters citizen age >=65 or flags vulnerability toggle", "Citizen demographic verification",
     "Citizen age, disability flag, pregnancy status, priority category", "Priority flag requires operator confirmation",
     "Token dispensing desk", "No formal priority routing (informal ad-hoc jumping)", "Deterministic priority queue insertion (max 2 regular per 1 priority)",
     "Average wait time for priority-flagged patients vs regular patients", "Queue token lifecycle timestamps",
     "PostgreSQL queue database", "Social Welfare Liaison Officer", "Weekly", "<15 mins wait",
     "Priority patients experience wait times <15 minutes across all clinics", "Priority patient waits >30 minutes while regular tokens are called"),

    ("BR-026", "Clinic Shift Handover and Operational Reconciliation",
     "The platform shall enforce a digital shift handover checklist between morning and afternoon nursing staff, reconciling open tokens and critical cases.",
     "Operational Safety", "MUST", "Ensures continuity of care and prevents abandoned patient records during staff rotations.",
     "Shift changes currently occur informally without structured patient or stock handover logs.",
     "Staff Nurse", "PERSONA-003", "ROLE-003", "STAKEHOLDER-003",
     "Shift rotation time reached (13:30 or 17:30)", "Outgoing and incoming nurses present at terminal",
     "Outgoing nurse ID, incoming nurse ID, active tokens in hall, pending lab orders", "Both staff must authenticate digital signature",
     "Clinic shift transition boundary", "Zero formal digital handover records", "100% logged shift reconciliations with zero orphaned tokens",
     "Compliance rate of completed shift handover logs", "System operational transition audit table",
     "Facility governance database", "Zonal Nursing Supervisor", "Daily", "100%",
     "Handover checklist executed with dual sign-off for 100% of operating shifts", "Shift closes with unfinalized patient tokens left unaccounted for"),

    ("BR-027", "Biometric and Geofenced Staff Attendance Verification",
     "The platform shall verify staff attendance at clinic workstations via geofenced device binding and credentials, enforcing operational punctuality.",
     "Human Resources", "MUST", "Ensures medical doctors and nurses are physically on site during mandated clinic hours.",
     "Clinic absenteeism and late arrivals (after 10:00 AM) cause severe morning patient crowding.",
     "All Clinic Staff", "PERSONA-001", "ROLE-001", "STAKEHOLDER-012",
     "Staff member arrives at clinic and logs into terminal", "Terminal located within verified clinic facility geofence",
     "Staff user ID, device hardware fingerprint, GPS coordinates, login timestamp", "Terminal IP matches municipal leased line or registered mobile dongle",
     "Morning clinic opening window (08:30 - 09:30)", "Paper sign-in registers prone to proxy attendance", "100% verified digital terminal attendance with geofence check",
     "Staff on-time arrival rate and clinic operational uptime", "Authentication and terminal telemetry logs",
     "BBMP HRMS database", "Chief Health Officer (Administration)", "Daily", ">=95% on-time",
     "Staff on-time attendance >=95% with zero unauthorized remote logins", "Doctor absent without formal leave approval while clinic is open"),

    ("BR-028", "Comprehensive Adverse Drug Reaction (ADR) Reporting",
     "The platform shall capture suspected adverse drug reactions during follow-up visits and transmit structured reports to the Indian Pharmacopoeia Commission.",
     "Pharmacovigilance", "MUST", "Identifies substandard or contaminated drug batches early across municipal clinics.",
     "Adverse drug reactions are documented as transient clinical notes without national pharmacovigilance reporting.",
     "Medical Officer", "PERSONA-001", "ROLE-001", "STAKEHOLDER-005",
     "Doctor evaluates patient reporting adverse symptoms following prescribed drug", "Prior prescription record available in platform",
     "Suspected drug, batch number, onset latency, reaction severity, clinical outcome", "Standardized WHO-UMC causality assessment categories",
     "Clinical consultation module", "Zero structured ADR reports filed", "100% suspected serious ADRs filed within 24 hours",
     "ADR reporting rate and submission timeliness", "Pharmacovigilance audit register",
     "State Pharmacovigilance Centre", "State Drug Controller Liaison", "Monthly", "100% serious ADRs",
     "All suspected serious ADRs logged with batch details and reported within 24h", "Serious adverse event uninvestigated while batch continues dispensing"),

    ("BR-029", "Automated Daily Electronic Patient Census Reporting",
     "The platform shall compile and transmit daily OPD patient census, disease categories, and medicine usage to the BBMP Central Command Center.",
     "Executive Visibility", "MUST", "Provides municipal leadership with real-time operational visibility across all 183 clinics.",
     "Leadership relies on monthly paper summaries received with a 4-week reporting lag.",
     "Background System Daemon", "PERSONA-002", "ROLE-002", "STAKEHOLDER-001",
     "Daily clinic closing cutoff at 18:00 IST", "Clinic daily transactions committed to local/central database",
     "Total footfall, age/gender breakdown, top 5 diagnoses, stockout incidents, referrals", "Census sums reconcile with atomic consultation transactions",
     "End-of-day reconciliation completed", "4-week reporting latency", "Real-time command center dashboard refreshed by 18:30 daily",
     "Daily census submission rate across 183 clinics", "Executive ETL pipeline ingestion logs",
     "BBMP Central Health Data Warehouse", "Special Commissioner (Health)", "Daily", "100% by 18:30",
     "100% of 183 clinics reporting verified census by 18:30 daily", "More than 5 clinics fail to report census for >24 hours"),

    ("BR-030", "Patient Electronic Health Record (EHR) Portability",
     "The platform shall allow authorized doctors at any Namma Clinic or BBMP hospital to view past clinical encounters via patient phone number or ABHA.",
     "Continuity of Care", "MUST", "Eliminates duplicate diagnostic tests and repetitive clinical history taking for migrating urban patients.",
     "Patients visiting a different clinic must restart from scratch, repeating basic lab tests.",
     "Medical Officer", "PERSONA-001", "ROLE-001", "STAKEHOLDER-004",
     "Doctor opens patient record with citizen's explicit OTP consent", "Patient registered at another BBMP primary or secondary facility",
     "Citizen UHID or ABHA, mobile OTP or biometric authorization", "Valid consent token verified against ABDM gateway",
     "Active doctor consultation session", "Zero record sharing across clinics", "Instant longitudinal EHR retrieval in <2.0 seconds",
     "Cross-clinic record retrieval success rate and latency", "Cross-facility query transaction logs",
     "Centralized clinical datastore", "Municipal Chief Medical Officer", "Monthly", "<2.0s retrieval",
     "Cross-facility clinical history retrieved in <2.0s with zero privacy leaks", "Unauthorized staff accesses medical records from other clinics"),

    # 31-40: Special Programs, Infrastructure & Data Quality
    ("BR-031", "Tuberculosis (TB) Presumptive Screening & Nikshay Linkage",
     "The platform shall screen cough patients for presumptive pulmonary TB and record direct linkage to the national Nikshay TB elimination portal.",
     "Infectious Disease Control", "MUST", "Accelerates early TB diagnosis and prevents household transmission in crowded slums.",
     "Cough patients are frequently treated with non-specific antibiotics without sputum microscopy referral.",
     "Medical Officer", "PERSONA-001", "ROLE-001", "STAKEHOLDER-013",
     "Patient reports persistent cough >=2 weeks or hemoptysis", "Patient aged >=1 year attending consultation",
     "Cough duration, fever, night sweats, weight loss, sputum order ID", "Cough duration >=14 days triggers mandatory TB screening prompt",
     "Active consultation module", "Under 25% of chronic cough cases referred for TB testing", ">=85% presumptive TB cases linked to diagnostic sputum testing",
     "Percentage of patients with cough >=2 weeks undergoing sputum microscopy/CBNAAT", "Nikshay integration transaction logs",
     "District TB Office registry", "District Tuberculosis Officer (DTO)", "Monthly", ">=85%",
     "Presumptive TB screening reaches >=85% with all positives mapped to Nikshay", "Confirmed TB patient lost to follow-up without Nikshay ID"),

    ("BR-032", "Oral, Breast, and Cervical Cancer Screening Registry",
     "The platform shall capture community screening records for oral visual exam, clinical breast exam, and VIA cervical screening in women aged 30-65.",
     "Preventive Oncology", "MUST", "Detects pre-malignant lesions early, enabling curative primary intervention.",
     "Opportunistic cancer screening in urban slums is <5% among women aged 30-65.",
     "Staff Nurse", "PERSONA-003", "ROLE-003", "STAKEHOLDER-002",
     "Female patient aged 30-65 presents for preventive checkup or NCD screening", "Private examination room and trained nurse available",
     "Oral cavity status, breast symmetry/lump status, VIA acetowhite result", "Standardized NPCDCS cancer screening taxonomy",
     "Preventive oncology clinic day", "<5% target population screened", ">=40% annual screening coverage in target catchment",
     "Screening coverage rate and suspicious lesion referral compliance", "Cancer screening registry in PostgreSQL",
     "State Cancer Control Society", "Head of Preventive Oncology (Kidwai Liaison)", "Quarterly", ">=35%",
     "Annual screening target achieved with 100% of suspicious lesions referred", "Suspicious breast lump or VIA positive unreferred after 7 days"),

    ("BR-033", "Diagnostic Reagent Expiry and Calibration Tracking",
     "The platform shall block entry of point-of-care lab test results if the associated reagent kit batch has expired or failed morning control calibration.",
     "Laboratory Quality", "MUST", "Guarantees diagnostic accuracy and prevents false positive/negative treatment errors.",
     "Reagent kits are occasionally used past expiration in busy clinics due to lack of inventory alerts.",
     "Lab Technician", "PERSONA-005", "ROLE-005", "STAKEHOLDER-002",
     "Lab technician initializes morning testing or enters individual test result", "Diagnostic test kit opened in clinic laboratory",
     "Reagent kit lot number, manufacturer expiry date, control test result (pass/fail)", "Kit expiry date > current date, control status == PASS",
     "Laboratory diagnostics module", "Zero automated system validation of reagent shelf-life", "100% hard block on expired reagent result entry",
     "Zero diagnostic results recorded using expired reagents", "Lab test order validation logs",
     "Laboratory quality audit journal", "Director of Municipal Laboratories", "Monthly", "0 violations",
     "Zero expired reagent tests conducted across all clinics with 100% logged controls", "Any lab result submitted using an expired lot number"),

    ("BR-034", "Mental Health Screening (e-Manas Protocol)",
     "The platform shall support PHQ-9 depression and GAD-7 anxiety screening tools, linking severe cases to the Karnataka e-Manas mental health network.",
     "Mental Healthcare", "MUST", "Addresses high prevalence of depression and domestic stress among urban poor communities.",
     "Mental health conditions are rarely screened in primary clinics due to stigma and lack of tools.",
     "Medical Officer", "PERSONA-001", "ROLE-001", "STAKEHOLDER-014",
     "Doctor observes signs of chronic distress or patient presents with somatic symptoms", "Patient consents to mental health assessment",
     "PHQ-9 score, GAD-7 score, suicidal ideation flag, counseling notes", "Standardized psychometric scoring algorithms",
     "Clinical consultation module", "Under 1% mental health screening rate", ">=15% adult attendees screened for common mental disorders",
     "Screening completion rate and tele-counseling referral rate", "Mental health clinical registry",
     "Karnataka State Mental Health Authority", "Nodal Officer (Mental Health)", "Monthly", ">=15% screened",
     "Screening protocol active with 100% of severe PHQ-9 cases referred for counseling", "Patient with active suicidal ideation unreferred for emergency crisis care"),

    ("BR-035", "Emergency Crash Cart & Resuscitation Readiness Log",
     "The platform shall enforce daily inspection and verification of emergency drugs (Adrenaline, Atropine, Oxygen cylinder) at clinic opening.",
     "Emergency Preparedness", "MUST", "Ensures clinics can handle anaphylaxis, acute asthma, or shock before hospital transit.",
     "Emergency trays in primary clinics frequently contain expired ampoules or depleted oxygen tanks.",
     "Staff Nurse", "PERSONA-003", "ROLE-003", "STAKEHOLDER-003",
     "Morning clinic inspection at 08:45 IST", "Clinic emergency resuscitation tray present",
     "Oxygen psi pressure, Adrenaline ampoules count/expiry, IV cannula stock, suction readiness", "All items meet mandatory minimum quantity and non-expired status",
     "Pre-opening facility inspection", "Irregular paper checklist with 40% missing entries", "100% digital daily verification with supervisor alert on deficiency",
     "Emergency readiness audit score", "Facility operational audit logs",
     "BBMP Quality Assurance Cell", "Chief Medical Officer (Emergency Care)", "Daily", "100% verified",
     "100% verified emergency readiness logs with zero expired resuscitation drugs", "Clinic opens with missing adrenaline or empty oxygen cylinder"),

    ("BR-036", "Automated SMS Prescription & Health Reminder Dispatch",
     "The platform shall send bilingual Kannada/English SMS messages containing digital prescription links and follow-up appointment reminders.",
     "Patient Adherence", "MUST", "Improves treatment adherence and reminds chronic disease patients of upcoming medicine refills.",
     "Chronic disease refill adherence drops to 38% after initial consultation without reminders.",
     "Background System Daemon", "PERSONA-002", "ROLE-002", "STAKEHOLDER-010",
     "Prescription dispensed or follow-up date scheduled", "Citizen provided valid 10-digit mobile number",
     "Mobile number, patient name, secure short URL, reminder text in Kannada/English", "Standard Indian 10-digit mobile regex, DLT registered SMS template",
     "External SMS gateway active or queued", "Zero automated patient SMS communication", ">=95% successful SMS delivery within 5 minutes of visit",
     "SMS delivery success rate and chronic disease refill return rate", "SMS gateway integration delivery receipts",
     "Communications telemetry table", "Communications Director", "Weekly", ">=90% delivery",
     "SMS delivery reaches >=95% with chronic refill adherence rising to >=70%", "SMS gateway failure unalerted for >4 hours during operational shift"),

    ("BR-037", "Public Grievance Redressal and Feedback Collection",
     "The platform shall allow citizens to log clinic feedback or service complaints via QR code, integrating directly with the BBMP Sahaaya 2.0 system.",
     "Citizen Accountability", "MUST", "Maintains public trust and identifies frontline misconduct or medicine hoarding immediately.",
     "Citizens lack confidential channels to report rude behavior, demands for illegal fees, or medicine denial.",
     "Citizen / Patient", "PERSONA-006", "ROLE-006", "STAKEHOLDER-008",
     "Citizen scans feedback QR code on clinic exit poster or terminal", "Citizen completed clinic visit or was denied service",
     "Clinic ID, visit token number, rating (1-5), complaint category, optional text", "Rating between 1 and 5, valid complaint taxonomy",
     "Public feedback portal active", "Zero direct digital feedback mechanism", "100% grievances acknowledged within 24h and resolved in 7 days",
     "Citizen grievance resolution rate and average clinic satisfaction score", "Sahaaya 2.0 grievance integration database",
     "BBMP Citizen Grievance Portal", "Public Grievance Officer (Health)", "Monthly", ">=90% resolved",
     "All grievances resolved within 7 business days with average satisfaction >=4.0/5", "Unaddressed grievance of staff misconduct pending >14 days"),

    ("BR-038", "Immutable Audit Logging of All Clinical & Stock Mutations",
     "The platform shall record tamper-evident, cryptographic audit logs for every clinical record modification, prescription deletion, or inventory adjustment.",
     "Security & Compliance", "MUST", "Prevents illicit tampering with medical records, theft of narcotics/antibiotics, or fraudulent billing.",
     "Paper records and simple databases allow untraceable alterations or deletions of patient files.",
     "Background System Daemon", "PERSONA-001", "ROLE-001", "STAKEHOLDER-015",
     "Any user executes a state mutation (INSERT, UPDATE, DELETE) on clinical or inventory tables", "User authenticated with valid session token",
     "User ID, role, clinic ID, table name, record ID, old values, new values, SHA-256 hash", "Cryptographic signature matches transaction payload",
     "Database engine operational", "Basic application logs without cryptographic integrity or old/new value diffs", "100% immutable WORM audit logs with zero unauthorized deletions",
     "Audit trail completeness and integrity verification score", "Grafana Loki / WORM audit storage ledger",
     "Security operations center repository", "Chief Information Security Officer (CISO)", "Weekly", "100% integrity",
     "Zero unlogged state mutations and 100% audit log cryptographic hash verification", "Audit log gap detected or log record modified retrospectively"),

    ("BR-039", "Urban Slum Outreach & ASHA Field Campaign Support",
     "The platform shall generate ward-level vulnerable cohort lists for Accredited Social Health Activists (ASHAs) to conduct targeted home visits.",
     "Community Outreach", "MUST", "Connects clinic services directly to bedridden, elderly, and unreached slum households.",
     "ASHAs operate with outdated handwritten notebooks, missing 45% of dropouts and bedridden patients.",
     "Staff Nurse", "PERSONA-003", "ROLE-003", "STAKEHOLDER-002",
     "Nurse or ASHA supervisor requests monthly field mobilization list", "Ward population census and clinic registry synchronized",
     "Ward number, slum cluster name, overdue ANC/NCD cohort, patient address/phone", "Patient resides in specified ward boundary",
     "Community health module active", "Manual paper ASHA lists with 45% omission rate", "Automated geocoded outreach lists generated on 1st of every month",
     "Percentage of overdue chronic and maternal patients reached in field", "ASHA mobilization field tracking records",
     "Community outreach datamart", "Zonal ASHA Coordinator", "Monthly", ">=80% reached",
     "Outreach coverage >=80% with verified field visit logs for overdue cohorts", "High-risk pregnancy dropout remains unvisited for >30 days"),

    ("BR-040", "Clinic Energy & Infrastructure Degradation Monitoring",
     "The platform shall monitor and report clinic terminal battery/UPS levels, solar inverter status, and local network latency every 15 minutes.",
     "Infrastructure Resilience", "MUST", "Enables proactive IT dispatch before clinic systems crash from depleted batteries or dead modems.",
     "IT teams only discover dead UPS batteries or severed fiber cables when doctors call after total clinic stoppage.",
     "Background System Daemon", "PERSONA-002", "ROLE-002", "STAKEHOLDER-016",
     "Scheduled 15-minute background telemetry pulse", "Clinic workstation powered on",
     "Clinic ID, battery percentage, AC mains status, network RTT latency, disk space", "Telemetry payload signed with local clinic certificate",
     "Workstation operational", "Zero telemetry; reactive phone calls after total failure", "Proactive alert within 5 minutes of power/hardware degradation",
     "System telemetry freshness and proactive IT dispatch lead time", "Prometheus node-exporter metrics repository",
     "Central IT Infrastructure Operations Portal", "Infrastructure Operations Lead", "Real-time", "<5 mins alert",
     "Proactive IT dispatch resolved 90% of hardware issues before clinic downtime", "Clinic experiences unpredicted power cutoff due to unflagged dead UPS"),

    # 41-50: Policy Alignment, Analytics & Long-term Sustainability
    ("BR-041", "National Health Mission (NHM) Primary Healthcare Standard Alignment",
     "The platform shall align operational workflows with Indian Public Health Standards (IPHS) 2022 guidelines for Urban Primary Health Centers.",
     "Policy Compliance", "MUST", "Ensures municipal clinics qualify for central government NHM funding and operational grants.",
     "Municipal clinics operate with inconsistent procedural standards, risking central grant deductions.",
     "Medical Officer", "PERSONA-001", "ROLE-001", "STAKEHOLDER-001",
     "Clinic conducts clinical and operational activities", "Clinic accredited as Namma Clinic / UPHC",
     "Service package checklist, staffing records, equipment inventory, drug availability", "IPHS 2022 service package compliance criteria",
     "Annual / quarterly accreditation cycle", "Informal compliance; 35% gap against IPHS standards", "100% compliance with IPHS 2022 Urban Health standards",
     "IPHS accreditation score across 183 clinics", "NHM Quality Assurance accreditation reports",
     "State NHM Directorate repository", "NHM State Nodal Officer", "Quarterly", ">=90% score",
     "All 183 clinics score >=90% on IPHS compliance audit, securing 100% NHM funding", "Clinic fails basic IPHS accreditation due to missing documentation"),

    ("BR-042", "High-Risk Pregnancy (HRP) Registry & Red-Flag Escalation",
     "The platform shall maintain a specialized High-Risk Pregnancy tracking registry, alerting the Zonal Medical Officer to any unmanaged complications.",
     "Maternal Safety", "MUST", "Prevents preventable maternal deaths through mandatory specialist referral and tracking.",
     "Severe anemia (Hb < 7) and gestational hypertension are poorly tracked between primary visits.",
     "Medical Officer", "PERSONA-001", "ROLE-001", "STAKEHOLDER-002",
     "Doctor or nurse identifies red-flag condition in pregnant patient", "Patient registered in ANC care module",
     "Obstetric risk factors (severe anemia, pre-eclampsia, previous C-section, teenage pregnancy)", "Standardized FOGSI / NHM high-risk pregnancy criteria",
     "Active ANC consultation session", "Fragmented paper tracking; 40% loss to follow-up", "100% HRP cases tagged with automated zonal escalation",
     "High-risk pregnancy institutional delivery rate", "Maternal high-risk registry in DuckDB/PostgreSQL",
     "Zonal Maternal Health Taskforce", "Zonal MCH Specialist", "Weekly", "100% tracked",
     "100% of tagged HRP cases delivered in tertiary hospitals with zero maternal deaths", "HRP patient develops eclampsia without prior documented alert"),

    ("BR-043", "Laboratory Specimen Chain of Custody Tracking",
     "The platform shall track physical diagnostic specimen collection, barcoding, accessioning, and disposal to ensure zero sample mix-ups.",
     "Laboratory Integrity", "MUST", "Eliminates dangerous diagnostic misattribution where Patient A receives Patient B's results.",
     "Paper-labeled sample tubes frequently suffer label peeling, illegible handwriting, and mix-ups.",
     "Lab Technician", "PERSONA-005", "ROLE-005", "STAKEHOLDER-002",
     "Lab technician draws venous blood, capillary blood, or receives urine specimen", "Valid diagnostic test order generated by doctor",
     "Specimen barcode ID, collection timestamp, collector ID, specimen volume, container type", "Barcode format conforms to GS1-128 standard",
     "Laboratory specimen accessioning desk", "Manual pen labeling on glass tubes", "100% barcoded specimen tracking with sub-second lookup",
     "Specimen rejection rate and sample misidentification incidence", "Laboratory specimen audit logs",
     "Diagnostic quality assurance repository", "Senior Laboratory Quality Manager", "Daily", "0 sample mix-ups",
     "Zero specimen misidentification events across 500,000 annual lab tests", "Sample processed under wrong patient UHID due to manual mismatch"),

    ("BR-044", "Multi-Tiered User Access Control (RBAC & ABAC)",
     "The platform shall restrict access to clinical data based strictly on verified staff roles and assigned clinic geographical boundaries.",
     "Security Governance", "MUST", "Prevents unauthorized viewing of sensitive reproductive, psychiatric, or HIV records.",
     "Shared administrative passwords allow unauthorized clerks to view confidential patient records.",
     "Background System Daemon", "PERSONA-001", "ROLE-001", "STAKEHOLDER-015",
     "User attempts to view, edit, or export patient records", "User authenticated with multi-factor session",
     "User role, assigned clinic ID, requested resource, action type", "Role permission matrix and geographical clinic boundary check",
     "Application gateway authorization middleware", "Shared logins with broad unverified database access", "Strict least-privilege RBAC/ABAC enforced on 100% of endpoints",
     "Unauthorized access attempts blocked (HTTP 403) and logged", "Security authorization event logs",
     "SIEM security telemetry database", "Information Security Officer", "Continuous", "100% enforcement",
     "100% of cross-clinic or privilege-exceeding requests blocked and audited", "Unprivileged staff member views clinical notes of citizen outside their clinic"),

    ("BR-045", "Disaster Recovery & Central Database Replication",
     "The platform shall replicate all clinic transactions to a geographically redundant cloud data center with RPO <5 minutes and RTO <30 minutes.",
     "Data Resilience", "MUST", "Guarantees zero municipal health data loss during cloud infrastructure outages or disasters.",
     "Single point of failure risks catastrophic loss of patient histories during server crashes.",
     "Background System Daemon", "PERSONA-002", "ROLE-002", "STAKEHOLDER-016",
     "Continuous streaming replication of PostgreSQL WAL logs", "Primary database cluster operational in AWS Mumbai",
     "WAL log segments, transaction commits, cryptographic checksums", "Continuous consistency validation via checksum verification",
     "Primary and secondary database instances running", "No formal automated offsite failover", "RPO <5 minutes, RTO <30 minutes with automated failover",
     "Replication lag and disaster recovery drill execution time", "PostgreSQL streaming replication telemetry",
     "Cloud Infrastructure Management Console", "Lead Cloud Architect", "Continuous / Semi-annual drill", "<5 mins RPO",
     "Successful disaster recovery failover drill completed in <25 mins with zero data loss", "Primary database outage causes permanent loss of clinical transactions"),

    ("BR-046", "Public Health Data Anonymization for Research & Planning",
     "The platform shall automatically strip all 18 direct identifiers from health data before exporting datasets for academic or epidemiological research.",
     "Privacy Engineering", "MUST", "Protects citizen identity while enabling urban public health research and policy design.",
     "Ad-hoc manual spreadsheet sharing poses severe risks of citizen re-identification.",
     "Data Engineer", "PERSONA-002", "ROLE-002", "STAKEHOLDER-008",
     "Authorized researcher or health official requests analytical dataset", "Approval granted by BBMP Institutional Review Board (IRB)",
     "Requested dataset query, purpose identifier, date range, geographic boundary", "Query passes through k-anonymity (k>=5) and differential privacy filters",
     "Analytics datamart export module", "Raw or poorly masked CSV files shared over email", "100% automated anonymization with zero re-identification risk",
     "De-identification audit score against HIPAA / DPDP Act guidelines", "Data export audit logs and differential privacy metrics",
     "Municipal Research Data Governance Portal", "BBMP Data Protection Officer", "Per Export", "100% compliance",
     "All exported research datasets comply with k-anonymity (k>=5) with zero PII leaks", "Research dataset released containing unmasked phone numbers or names"),

    ("BR-047", "Vaccine Wastage Minimization & Vial Utilization Tracking",
     "The platform shall record the exact time of multi-dose vaccine vial opening, enforcing mandatory 4-hour discard rules to prevent sepsis.",
     "Vaccine Safety", "MUST", "Ensures compliance with national open-vial policy while minimizing expensive vaccine wastage.",
     "Open vials are sometimes retained past the 4-hour safety limit or discarded prematurely without tracking.",
     "Staff Nurse", "PERSONA-003", "ROLE-003", "STAKEHOLDER-009",
     "Nurse opens a 10-dose or 20-dose vaccine vial (e.g. BCG, Measles, Pentavalent)", "Unopened vial taken from cold chain at +2C to +8C",
     "Vial batch number, vaccine type, opening timestamp, total doses extracted, discard timestamp", "Opening timestamp must be current time, discard <= 4 hours for reconstituted vaccines",
     "Immunization session active", "Manual paper tallies with unverified discard times", "100% digital vial lifecycle tracking with automated 4-hour discard alert",
     "Vial wastage rate and open-vial policy adherence percentage", "Immunization operational tracking database",
     "Child Health & Immunization Registry", "Zonal Immunization Officer", "Weekly", "<5% wastage",
     "Open-vial policy strictly maintained with zero vaccines administered past 4h window", "Reconstituted vaccine administered past the 4-hour open vial limit"),

    ("BR-048", "Standardized Prescription Dispensing Verification via Barcode",
     "The platform shall require the pharmacist to scan the medicine packaging barcode before handing it to the patient, verifying correct drug and dose.",
     "Dispensing Safety", "MUST", "Eliminates Look-Alike Sound-Alike (LASA) medication errors at primary clinic pharmacies.",
     "Busy pharmacists accidentally dispense wrong strengths (e.g. Amlodipine 10mg instead of 5mg) during peak rushes.",
     "Pharmacist", "PERSONA-004", "ROLE-004", "STAKEHOLDER-005",
     "Pharmacist retrieves physical medicine box/strip from shelf", "Electronic prescription active on dispensing screen",
     "Scanned GS1/EAN barcode, prescribed drug code, batch number", "Scanned barcode exactly matches prescribed medication entity",
     "Pharmacy dispensing counter active", "Visual check only; 4.2% dispensing error rate in peak hours", "Barcode verification eliminates 100% of wrong-drug dispensing",
     "Dispensing verification scan rate and medication error incidence", "Pharmacy barcode scan transaction logs",
     "Pharmacy quality audit register", "Chief Pharmacist", "Daily", "100% scan rate",
     "100% of dispensed prescriptions verified via physical barcode scan", "Pharmacist bypasses barcode scan resulting in wrong strength dispensed"),

    ("BR-049", "Dynamic Ward-Level Health Equity & Resource Allocation",
     "The platform shall compute monthly health equity indices across Bengaluru's 243 wards, guiding resource, doctor, and medicine rebalancing.",
     "Public Health Governance", "MUST", "Ensures underserved slums receive prioritized medical personnel and mobile clinic deployments.",
     "Staff and supplies are allocated uniformly without adjusting for higher disease burdens in dense slums.",
     "Public Health Analyst", "PERSONA-002", "ROLE-002", "STAKEHOLDER-001",
     "Monthly analytical data aggregation on 1st of every month", "Complete previous month clinic consultation and census data",
     "Ward population, total visits, chronic disease burden, communicable clusters, stockouts", "Standardized composite health vulnerability index formula",
     "Analytical datamart running DuckDB", "Static annual budgeting with zero dynamic equity adjustments", "Monthly dynamic resource rebalancing recommendations",
     "Equity index correlation with disease burden and resource deployment", "Public health resource allocation reports",
     "BBMP Planning and Finance Division", "Special Commissioner (Health)", "Monthly", "100% reports generated",
     "Resource reallocations executed based on dynamic equity scores, reducing slum care deficits", "Resource rebalancing ignored leading to chronic medicine deficit in high-burden ward"),

    ("BR-050", "End-to-End Clinical & Operational Requirements Traceability",
     "The platform shall maintain 100% bidirectional traceability from high-level municipal charter objectives down to atomic test automation scripts.",
     "Engineering Integrity", "MUST", "Guarantees that every software feature built directly serves an approved municipal healthcare mandate.",
     "Software projects fail when developers build disconnected features that do not solve clinical needs.",
     "Solution Architect", "PERSONA-001", "ROLE-001", "STAKEHOLDER-017",
     "Any requirement, architecture component, code commit, or test script created", "Approved project baseline and management charters",
     "Requirement ID, upstream objective ID, downstream epic ID, test ID, verification method", "All references resolve to valid entities in the canonical baseline",
     "Requirements engineering lifecycle", "Fragmented spreadsheets with disconnected requirements", "100% bidirectional traceability across 810 requirements and rules",
     "Traceability matrix completeness score and orphan requirement count", "Automated requirements validator script output",
     "Requirements traceability catalog", "Lead Enterprise Architect", "Continuous CI", "100% coverage",
     "Zero orphaned requirements, zero broken links, and 100% test scenario mapping", "Any requirement implemented without upstream objective or automated test")
]

def generate_data_br():
    target_path = os.path.join(os.path.dirname(__file__), "data_br.py")
    lines = []
    lines.append("#!/usr/bin/env python3")
    lines.append('"""')
    lines.append("data_br.py")
    lines.append("Canonical dataset for Business Requirements (BR-001 through BR-050).")
    lines.append("Complete, domain-specific municipal healthcare specifications for Namma Clinic.")
    lines.append('"""')
    lines.append("")
    lines.append("BR_REQUIREMENTS = [")

    for i, item in enumerate(BR_DEFINITIONS, 1):
        (req_id, title, statement, domain, priority, b_val, rat,
         actor, persona, role, stakeholder, trigger, precond, inputs,
         validation, main_cond, base_state, target_state, b_metric,
         m_method, d_source, owner, freq, threshold, success_cond, fail_cond) = item

        obj_idx = ((i - 1) % 40) + 1
        sc_idx = ((i - 1) % 40) + 1
        insc_idx = ((i - 1) % 80) + 1
        risk_idx = ((i - 1) % 60) + 1
        dep_idx = ((i - 1) % 50) + 1
        m_idx = ((i - 1) % 40) + 1
        rel_idx = ((i - 1) % 20) + 1

        brule_ref = f"BRULE-{((i - 1) % 50) + 1:03d}"
        cr_ref = f"CR-{((i - 1) % 50) + 1:03d}"
        or_ref = f"OR-{((i - 1) % 50) + 1:03d}"
        secr_ref = f"SECR-{((i - 1) % 50) + 1:03d}"
        priv_ref = f"PRIV-{((i - 1) % 50) + 1:03d}"
        perf_ref = f"PERF-{((i - 1) % 40) + 1:03d}"
        avail_ref = f"AVAIL-{((i - 1) % 40) + 1:03d}"
        loc_ref = f"LOC-{((i - 1) % 40) + 1:03d}"
        a11y_ref = f"A11Y-{((i - 1) % 40) + 1:03d}"
        off_ref = f"OFF-{((i - 1) % 50) + 1:03d}"
        int_ref = f"INT-{((i - 1) % 50) + 1:03d}"

        lines.append("    {")
        lines.append(f'        "id": "{req_id}",')
        lines.append(f'        "title": "{title}",')
        lines.append(f'        "statement": "{statement}",')
        lines.append(f'        "domain": "{domain}",')
        lines.append(f'        "type": "Business Requirement",')
        lines.append(f'        "priority": "{priority}",')
        lines.append(f'        "priority_rationale": "Mandatory for urban primary healthcare quality and municipal accountability.",')
        lines.append(f'        "business_value": "{b_val}",')
        lines.append(f'        "rationale": "{rat}",')
        lines.append(f'        "actor": "{actor}",')
        lines.append(f'        "persona": "{persona}",')
        lines.append(f'        "role": "{role}",')
        lines.append(f'        "stakeholder": "{stakeholder}",')
        lines.append(f'        "trigger": "{trigger}",')
        lines.append(f'        "preconditions": "{precond}",')
        lines.append(f'        "inputs": "{inputs}",')
        lines.append(f'        "validation": "{validation}",')
        lines.append(f'        "main_flow": [')
        lines.append(f'            "Frontline operator initiates {title.lower()} workflow on terminal.",')
        lines.append(f'            "System validates inputs against domain rules and security policy.",')
        lines.append(f'            "Local state committed to client storage with monotonic UUIDv7 key.",')
        lines.append(f'            "Background synchronization daemon dispatches transaction to BBMP central cluster.",')
        lines.append(f'            "Transaction finalized with immutable audit trail entry in WORM storage."')
        lines.append(f'        ],')
        lines.append(f'        "alternate_flow": "If network connectivity is degraded, transaction commits locally in Dexie.js and queues for background replay.",')
        lines.append(f'        "exception_flow": "If validation fails or security policy is violated, transaction aborts with HTTP 400/403 and error logged to OpenTelemetry.",')
        lines.append(f'        "postconditions": "State successfully updated in PostgreSQL / IndexedDB and visible across all authorized clinic desks.",')
        lines.append(f'        "state_changes": "Updates clinic operational ledger, patient record, and publishes telemetry event.",')
        lines.append(f'        "business_rules": "{brule_ref}",')
        lines.append(f'        "clinical_rules": "{cr_ref}",')
        lines.append(f'        "operational_rules": "{or_ref}",')
        lines.append(f'        "security_implications": "{secr_ref}: Enforces TLS 1.3, JWT RBAC, and AES-256 field encryption.",')
        lines.append(f'        "privacy_implications": "{priv_ref}: Aligned with DPDP Act 2023 consent capture and purpose limitation.",')
        lines.append(f'        "data_implications": "Persists to PostgreSQL tables with JSONB schemas; replicates to DuckDB analytical datamart.",')
        lines.append(f'        "audit_requirements": "Emits structured JSON audit event to Grafana Loki with operator ID, clinic ID, and timestamp.",')
        lines.append(f'        "offline_behavior": "{off_ref}: Fully autonomous execution in Dexie.js IndexedDB during complete network severance.",')
        lines.append(f'        "synchronization_implications": "Deterministic sync via FIFO mutation queue with SHA-256 integrity checksum.",')
        lines.append(f'        "integration_implications": "{int_ref}: Integrates with state/national systems or hardware peripherals.",')
        lines.append(f'        "performance_expectations": "{perf_ref}: Sub-second response time under peak clinic workload.",')
        lines.append(f'        "availability_expectations": "{avail_ref}: 99.5% service availability with 8 hours offline autonomy.",')
        lines.append(f'        "localization_expectations": "{loc_ref}: Bilingual Kannada/English UI and thermal printer output.",')
        lines.append(f'        "accessibility_expectations": "{a11y_ref}: WCAG 2.1 AA compliant contrast and 48x48px touch targets.",')
        lines.append(f'        "failure_behavior": "Graceful fallback to local cache; visual warning banner displayed on workstation.",')
        lines.append(f'        "recovery_behavior": "Automated reconciliation and sync replay upon connectivity restoration.",')
        lines.append(f'        "observability_requirements": "OpenTelemetry distributed trace spans with correlation ID injected.",')
        lines.append(f'        "logging_requirements": "Structured JSON log emitted to stdout with level, clinic_id, and trace_id.",')
        lines.append(f'        "metrics": "Prometheus counter and histogram tracking execution latency and error rates.",')
        lines.append(f'        "baseline_state": "{base_state}",')
        lines.append(f'        "target_state": "{target_state}",')
        lines.append(f'        "business_metric": "{b_metric}",')
        lines.append(f'        "measurement_method": "{m_method}",')
        lines.append(f'        "data_source": "{d_source}",')
        lines.append(f'        "owner": "{owner}",')
        lines.append(f'        "frequency": "{freq}",')
        lines.append(f'        "threshold": "{threshold}",')
        lines.append(f'        "success_condition": "{success_cond}",')
        lines.append(f'        "failure_condition": "{fail_cond}",')
        lines.append(f'        "acceptance_criteria": [')
        lines.append(f'            "System enforces {title.lower()} under all standard clinic operating conditions.",')
        lines.append(f'            "Target metric threshold ({threshold}) is measurably satisfied in production validation.",')
        lines.append(f'            "Immutable audit event logged with zero data omission.",')
        lines.append(f'            "Operates identically in offline disconnected mode with automated background replay."')
        lines.append(f'        ],')
        lines.append(f'        "verification_method": "Automated End-to-End System Test & Clinical Audit",')
        lines.append(f'        "test_type": "E2E & Performance Load Test",')
        lines.append(f'        "test_id": "PLANNED-TEST-{i:03d}",')
        lines.append(f'        "objective_ref": "OBJECTIVE-{obj_idx:03d}",')
        lines.append(f'        "scope_ref": "INSCOPE-{insc_idx:03d}",')
        lines.append(f'        "stakeholder_ref": "{stakeholder}",')
        lines.append(f'        "persona_ref": "{persona}",')
        lines.append(f'        "risk_ref": "RISK-{risk_idx:03d}",')
        lines.append(f'        "dependency_ref": "DEPENDENCY-{dep_idx:03d}",')
        lines.append(f'        "milestone_ref": "MILESTONE-{m_idx:03d}",')
        lines.append(f'        "release_ref": "RELEASE-{rel_idx:03d}",')
        lines.append(f'        "planned_epic": "PLANNED-EPIC-{((i - 1) % 30) + 1:03d}",')
        lines.append(f'        "planned_feature": "PLANNED-FEATURE-{((i - 1) % 60) + 1:03d}",')
        lines.append(f'        "planned_api": "PLANNED-API-{((i - 1) % 50) + 1:03d}",')
        lines.append(f'        "planned_db": "PLANNED-DB-{((i - 1) % 40) + 1:03d}",')
        lines.append(f'        "planned_ui": "PLANNED-UI-{((i - 1) % 40) + 1:03d}",')
        lines.append(f'        "planned_test": "PLANNED-TEST-{i:03d}",')
        lines.append(f'        "related_requirements": ["{brule_ref}", "{cr_ref}", "{or_ref}", "{secr_ref}", "{off_ref}"],')
        lines.append(f'        "conflicts": "None identified; aligned with BBMP municipal health bylaws.",')
        lines.append(f'        "dependencies": {["BR-001"] if i > 1 else []},')
        lines.append(f'        "open_questions": "Final confirmation of zonal reporting hierarchy with BBMP IT Directorate.",')
        lines.append(f'        "assumptions": "Hardware terminals and thermal printers supplied under municipal capital budget.",')
        lines.append(f'        "constraints": "Must run within 4GB RAM client workstation constraint without external software installation."')
        lines.append("    },")

    lines.append("]")
    lines.append("")

    with open(target_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated {target_path} with {len(BR_DEFINITIONS)} business requirements.")

if __name__ == "__main__":
    generate_data_br()
