# ⏱️ Sprint Cadence, Planning & Review Ceremonies
## Namma Clinic Digital Health & Operations Platform
### Agile Engineering & Governance Operations Framework
### Document Code: PM-AG-02 | Version: 1.0 | Date: September 2026

---

## 1. Operating Model Overview

The Namma Clinic Platform delivery combines a **2-week Scrum cycle** for engineering feature development with **weekly operational cadence meetings** with BBMP Health stakeholders. During active clinic pilot deployments and field hardening, a **1-week rapid stabilization loop** is adopted to address clinic frontline feedback with high agility.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        2-WEEK SPRINT CADENCE                           │
├────────────────────────────────────────────────────────────────────────┤
│ WEEK 1:                                                                │
│  Monday:    Sprint Planning (09:00 - 11:00)                            │
│  Daily:     Daily Standup (09:30 - 09:45)                              │
│  Thursday:  Mid-Sprint Clinical Validation with Clinical Advisor       │
│                                                                        │
│ WEEK 2:                                                                │
│  Daily:     Daily Standup (09:30 - 09:45)                              │
│  Wednesday: Backlog Refinement & Estimation (15:00 - 16:30)            │
│  Friday:    Sprint Review & Stakeholder Demo (15:00 - 16:30)           │
│  Friday:    Sprint Retrospective (16:30 - 17:30)                       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Standard Sprint Ceremonies

### 2.1 Sprint Planning Meeting
* **Schedule:** Alternate Mondays, 09:00 AM – 11:00 AM IST (Duration: 2 hours).
* **Participants:** Mandatory: Solution Architect, Frontend Lead, Backend Lead, Data Lead, QA Lead, Field Lead. Optional/Consulted: Clinical Advisor, Project Director.
* **Prerequisites:**
  1. Product backlog refined with prioritized user stories.
  2. Acceptance criteria clearly documented using Gherkin syntax (`Given-When-Then`).
  3. Non-functional requirements (offline behavior, Kannada transliteration, responsiveness) tagged.
* **Agenda:**
  1. Review Sprint Goal aligned with milestone commitments (15 mins).
  2. Team capacity allocation & holiday/leave factoring (15 mins).
  3. Story-by-story walkthrough, task breakdown, and story point commitment (75 mins).
  4. Final commitment and risk identification (15 mins).
* **Output:** Committed Sprint Backlog, agreed Sprint Goal in Jira/project board, dependency log.

### 2.2 Daily Engineering Standup (Scrum)
* **Schedule:** Monday through Friday, 09:30 AM – 09:45 AM IST (Duration: 15 mins).
* **Format:** Virtual / Hybrid via video conference; strictly time-boxed.
* **Three Core Questions:**
  1. What did I complete yesterday that pushed us toward the Sprint Goal?
  2. What will I complete today to achieve the Sprint Goal?
  3. What impediments or external blockers are slowing progress?
* **Field Addendum (during pilot):** Field Implementation Lead provides a 3-minute summary of active clinic operational metrics (e.g., footfall registered, sync errors, helpdesk tickets).

### 2.3 Backlog Refinement (Grooming)
* **Schedule:** Alternate Wednesdays (Sprint Week 2), 03:00 PM – 04:30 PM IST (Duration: 1.5 hours).
* **Participants:** Solution Architect, Clinical Advisor, Data Lead, Lead Developers.
* **Focus Areas:**
  - Splitting large epics into 2-to-5 story point implementable units.
  - Reviewing clinic bug reports from helpdesk and promoting them to user stories.
  - Updating clinical definitions with Dr. Clinical Advisor (e.g., drug formulary updates, diagnostic units).

### 2.4 Sprint Review & Demo
* **Schedule:** Alternate Fridays (Sprint Week 2), 03:00 PM – 04:30 PM IST (Duration: 1.5 hours).
* **Participants:** Full Delivery Team, Project Director, BBMP Nodal Officer (invited), Zonal MO representatives.
* **Format:**
  - Live software demonstration on staging/sandbox (no PowerPoint slides).
  - Walkthrough of end-to-end patient journey based on sprint deliverables.
  - Direct feedback collection from clinic representatives.
* **Acceptance Protocol:** Stories marked "Done" only when passing Definition of Done (DoD) and accepted by Product/Clinical Leads.

### 2.5 Sprint Retrospective
* **Schedule:** Alternate Fridays (following Demo), 04:30 PM – 05:30 PM IST (Duration: 1 hour).
* **Framework:** "What went well", "What was challenging", "Actionable improvements for next sprint".
* **Output:** Maximum of 3 specific, measurable process improvements tracked into next sprint's backlog.

---

## 3. Definition of Ready (DoR) & Definition of Done (DoD)

### 3.1 Definition of Ready (DoR)
A user story enters Sprint Planning only if:
- [ ] User story contains a clear persona, action, and expected healthcare value.
- [ ] Acceptance criteria documented and testable.
- [ ] Bilingual text requirements identified (Kannada label and English source).
- [ ] Clinical validation complete (signed off by Clinical Advisor for clinical workflows).
- [ ] UI mockup / wireframe available for frontend tasks.
- [ ] Story estimated in Fibonacci points (1, 2, 3, 5, 8).

### 3.2 Definition of Done (DoD)
A story is closed as "Complete" only if:
- [ ] Code implemented in accordance with TypeScript/React/Node conventions.
- [ ] Unit tests written and passing (minimum 80% coverage for business logic).
- [ ] Offline caching and sync edge-cases verified in browser sandbox.
- [ ] Role-based access control (RBAC) enforced on both UI and API layer.
- [ ] Peer code review completed and approved by at least one Senior Engineer.
- [ ] Deployed to staging environment and verified by QA.
- [ ] Clean security scan (no high/critical static analysis warnings).
- [ ] Documentation / API specs updated in Swagger/OpenAPI.

---

## 4. Weekly BBMP Joint Progress Review Meeting

In addition to engineering sprints, a formal weekly sync with BBMP takes place:
* **Schedule:** Every Tuesday, 04:00 PM – 05:00 PM IST.
* **Chaired by:** BBMP Health Nodal Officer & K Mati Project Director.
* **Standard Agenda:**
  1. Pilot clinics digital throughput metrics (last 7 days).
  2. Critical incidents, connectivity outages, or hardware replacements.
  3. Training completion status for upcoming wave clinics.
  4. Inter-departmental coordination (BSNL internet, BESCOM power, drug indents).
  5. Action item review from previous week.
