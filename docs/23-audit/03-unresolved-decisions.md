# ⚖️ Unresolved Decisions & Open Architectural Choices Register
## Namma Clinic Digital Health & Operations Platform
**Document Code:** AUD-DEC-03 | **Status:** Open Baseline | **Date:** September 2026

---

### 1. Catalog of Open Architectural & Operational Decisions

| Decision ID | Decision Question & Context | Evaluated Options | Recommended Position | Impact | Owner | Due Date | Blocking Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **DEC-001** | Cloud Hosting Tenancy: SDC Karnataka vs MeitY GCC (AWS/Azure)? | A: Karnataka SDC<br>B: AWS GCC India-South | **Option B:** AWS GCC for pilot; evaluate SDC hybrid for citywide. | High | Cloud Architect | Sprint 02 | Blocking Infra |
| **DEC-002** | Citizen Primary Identifier: State UHID vs Pure ABHA ID? | A: Pure ABHA ID<br>B: Clinic UHID with ABHA link | **Option B:** Clinic UHID primary; voluntary ABHA link (DPDP compliant). | Critical | Solutions Architect | Sprint 01 | Blocking Patient DB |
| **DEC-003** | Frontline Offline Token Hardware: Bluetooth vs USB Thermal Printer? | A: USB OTG<br>B: Bluetooth ESC/POS | **Option A:** USB OTG for reliable, jam-free physical printing. | Medium | Field Ops Lead | Sprint 04 | Non-Blocking |
| **DEC-004** | SMS Gateway Provider: National Informatics Centre (NIC) vs Commercial DLT? | A: NIC Gateway<br>B: DLT Approved Vendor | **Option B:** DLT vendor for guaranteed < 10s OTP delivery. | High | PM / GBA | Sprint 03 | Blocking SMS |
| **DEC-005** | Offline Sync Conflict Resolution: Pure LWW vs Interactive Clinician Prompt? | A: Pure Last-Write-Wins<br>B: Field-level LWW + Flag | **Option B:** Field-level LWW for vitals; manual flag for concurrent prescription edit. | Critical | Lead Architect | Sprint 07 | Blocking Sync Engine |
