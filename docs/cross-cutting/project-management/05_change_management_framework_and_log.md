# 🔄 Change Management Framework & Scope Control Log
## Namma Clinic Digital Health & Operations Platform
### Document Code: PM-CM-05 | Version: 1.0 | Date: September 2026

---

## 1. Objective & Scope

This framework defines the formal procedure for proposing, evaluating, approving, and implementing any modifications to the agreed **Project Scope, System Architecture, Functional Requirements, Deliverables, Schedule, or Commercial Baseline** as established in the approved Detailed Project Report (DPR).

Uncontrolled alterations ("scope creep") pose severe risks to project timelines, software stability, and clinic field adoption. No technical or operational modifications outside the approved baseline will be executed without following this procedure.

---

## 2. Change Control Board (CCB)

The CCB is the governing body authorized to review, approve, defer, or reject Change Requests (CRs).

### CCB Membership

| Role | Representative | Organization | Function in CCB |
| :--- | :--- | :--- | :--- |
| **Chairperson** | Special Commissioner (Health) / Additional Director | GBA / BBMP | Final executive approval for schedule/commercial variances |
| **Project Sponsor Nodal** | BBMP Health Nodal Officer | GBA / BBMP | Operational requirement validation and field feasibility |
| **Vendor Program Lead** | Project Director | K Mati | Contractual, timeline, and commercial impact evaluation |
| **Technical Authority** | Solution Architect | K Mati | Architecture, technical feasibility, security impact |
| **Clinical Authority** | Lead Clinical Advisor | K Mati | Patient safety, clinical protocol conformity, medical usability |

*Meeting Cadence: Monthly, or on-demand within 72 hours for urgent P1 changes.*

---

## 3. Change Request (CR) Lifecycle Workflow

```
[Frontline User / BBMP Official / Tech Team]
                    │
                    ▼
[Step 1: Submission of Change Request Form (CRF)]
                    │
                    ▼
[Step 2: Impact Assessment (Within 5 Working Days)]
  • Technical & Architecture Complexity (Solution Architect)
  • Clinical Usability & Protocol Fit (Clinical Advisor)
  • Effort in Story Points / Person-Days (Engineering Leads)
  • Impact on Milestones & Budget (Project Director)
                    │
                    ▼
[Step 3: CCB Review & Classification]
  ┌─────────────────┼─────────────────┐
  ▼                 ▼                 ▼
[Approved]      [Rejected]        [Deferred]
  │                 │                 │
  ▼                 ▼                 ▼
[Logged into     [Reason logged,   [Targeted to future
Active Backlog]   requestor notified] Phase / Version]
```

### 3.1 Change Classification Tiers
* **Tier 1 (Minor / Operational):** UI copy adjustment, additional common medicine in dropdown, minor report filter. Effort < 3 person-days, zero budget/timeline impact. *Approved by Solution Architect + BBMP Nodal Officer.*
* **Tier 2 (Moderate / Functional):** New laboratory test workflow, additional notification channel (WhatsApp), revised referral hierarchy. Effort 4–15 person-days, timeline variance < 2 weeks. *Approved by CCB Core (Project Director + Clinical Advisor + BBMP Nodal).*
* **Tier 3 (Major / Contractual):** New integration (e.g., third-party municipal ERP), major hardware specification changes, expansion of pilot clinic count. *Requires formal written sign-off by Special Commissioner (BBMP) & K Mati Managing Director.*

---

## 4. Change Request Form (CRF) Template

```
╔════════════════════════════════════════════════════════════════════════════════╗
║ CHANGE REQUEST FORM (CRF)                                                      ║
║ CR Reference: CR-NC-[YYYY]-[NNN]                Date Submitted: [DD-MMM-YYYY]  ║
╚════════════════════════════════════════════════════════════════════════════════╝

1. REQUESTOR INFORMATION
   Name: _______________________________  Designation: __________________________
   Organization: [ ] GBA / BBMP  [ ] K Mati  [ ] Frontline Clinic (Specify: ______)
   Email: ______________________________  Phone: ________________________________

2. CHANGE DESCRIPTION & JUSTIFICATION
   Title of Proposed Change: ____________________________________________________
   Detailed Description:
   _____________________________________________________________________________
   Clinical / Operational Justification:
   _____________________________________________________________________________

3. IMPACT ASSESSMENT (Completed by K Mati Technical & Clinical Leads)
   Impacted Modules: [ ] Registration  [ ] Triage  [ ] EMR  [ ] Pharmacy  [ ] Lab  [ ] Analytics
   Technical Architecture Impact: [ ] None  [ ] Minor  [ ] Major (Requires Schema Change)
   Clinical Protocol Impact:     [ ] None  [ ] Approved by Clinical Advisor  [ ] Conflicts
   Effort Estimate: _________ Person-Days / _________ Story Points
   Schedule Impact: [ ] Zero Variance  [ ] Delays Milestone [M_] by ______ Calendar Days
   Commercial Impact: [ ] Covered within contingency  [ ] Additional Cost: ₹__________

4. CCB DECISION
   Status: [ ] APPROVED  [ ] REJECTED  [ ] DEFERRED to Phase: _________
   Authorized Signature (BBMP): _______________________ Date: ___________________
   Authorized Signature (K Mati): _____________________ Date: ___________________
```

---

## 5. Master Change Control Log

| CR ID | Date Logged | Requestor | Change Summary | Tier | Effort (Days) | Cost (₹) | Schedule Impact | Status | Resolution Date |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **CR-001** | 25-Aug-2026 | Dr. Ashok Kumar (NC MO) | Include Kannada transliteration on thermal printed token slip. | Tier 1 | 2 | ₹0 | None | ✅ Approved | 28-Aug-2026 |
| **CR-002** | 28-Aug-2026 | Addl Director (Health) | Add automated SMS notification to pregnant mothers for ANC 2nd visit. | Tier 2 | 5 | Covered | None | ✅ Approved | 30-Aug-2026 |
| **CR-003** | 02-Sep-2026 | IT Cell BBMP | Direct API push to Karnataka State Health Portal for weekly fever counts. | Tier 2 | 8 | Covered | None | ⏳ In Review | — |
