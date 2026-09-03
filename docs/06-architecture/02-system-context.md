# 🏛️ Architecture: C4 System Context Model
## Namma Clinic Digital Health & Operations Platform
**Document Code:** ARC-CTX-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Level 1: System Context Diagram

```mermaid
C4Context
    title System Context Diagram for Namma Clinic Platform

    Person(patient, "Citizen / Patient", "Receives free primary healthcare and prescriptions.")
    Person(nurse, "Staff Nurse / ANM", "Performs registration, queue tokening, and triage vitals.")
    Person(doctor, "Medical Officer (Doctor)", "Examines patients, records diagnoses, and prescribes medications.")
    Person(pharmacist, "Clinic Pharmacist", "Dispenses medicines and manages batch inventory.")
    Person(official, "Health Officer (ZHO/CHO)", "Monitors epidemiological trends and clinic operations.")

    System(namma_system, "Namma Clinic Platform", "Cloud-native, offline-first digital primary health operations platform.")

    System_Ext(abdm, "ABDM / NDHM Gateway", "Ayushman Bharat Digital Mission national health record registry.")
    System_Ext(ehospital, "eHospital / BBMP Hospitals", "Secondary and tertiary referral hospital network.")
    System_Ext(sms_gw, "State SMS Gateway", "Citizen SMS notifications and OTP dispatch.")

    Rel(nurse, namma_system, "Registers patient, captures vitals, issues token", "HTTPS / PWA")
    Rel(doctor, namma_system, "Records EMR, prescribes drugs, orders lab tests", "HTTPS / PWA")
    Rel(pharmacist, namma_system, "Dispenses drugs, verifies batches", "HTTPS / PWA")
    Rel(official, namma_system, "Monitors disease surveillance dashboards", "HTTPS / React")
    Rel(patient, namma_system, "Receives SMS visit summaries and QR slips", "Thermal Print / SMS")

    Rel(namma_system, abdm, "Verifies ABHA, exports FHIR R4 care records", "REST / HTTPS")
    Rel(namma_system, ehospital, "Transmits outbound secondary referrals", "REST / HTTPS")
    Rel(namma_system, sms_gw, "Dispatches patient notification SMS", "HTTPS API")
```
