# 👥 Role-to-Module Access & Entitlement Matrix
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PRD-ROL-03 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Entitlement Matrix across 12 Roles

| Role Name | Registration & Queue | Triage & Vitals | Doctor EMR | Pharmacy | Lab Orders | Zonal Analytics | Audit Console | Admin |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Registration Clerk / ANM** | Full | View | No | No | No | No | No | No |
| **Staff Nurse** | Full | Full | Read | Read | Read | No | No | No |
| **Medical Officer (Doctor)** | Read | Full | Full | Read | Full | Clinic | Read Own | No |
| **Pharmacist** | Read | No | Read | Full | No | Clinic | Read Own | No |
| **Lab Technician** | Read | No | Read | No | Full | Clinic | Read Own | No |
| **Zonal Health Officer (ZHO)** | Read | Read | Read | Read | Read | Full Zonal | Read Zonal | No |
| **Chief Health Officer (CHO)** | Read | Read | Read | Read | Read | Full City | Read All | No |
| **System Administrator** | No | No | No | No | No | System | Full | Full |
