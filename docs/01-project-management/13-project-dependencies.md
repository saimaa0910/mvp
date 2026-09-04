# Project Dependency Management Baseline & Critical Path Register

| Metadata Element | Project Specification |
| :--- | :--- |
| **Document Identifier** | `DOC-PM-013-DEPENDENCY` |
| **Document Title** | Master Project Dependencies Register, Critical Path Network & Inter-Squad Handoff Baseline |
| **Project Code** | `NAMMA-CLINIC-PLATFORM-2026` |
| **Document Version** | `v1.0.0-PROD-BASELINE` |
| **Status** | `APPROVED & RATIFIED` |
| **Dependency Inventory** | Exactly 75 Formally Governed Dependencies (`DEPENDENCY-001` to `DEPENDENCY-075`) |
| **Executive Sponsor** | Special Commissioner (Health), Greater Bengaluru Authority (GBA) / BBMP |
| **Clinical Safety Authority** | Chief Health Officer (CHO), BBMP Health Department |
| **Lead Delivery Partner** | Kushagramati Analytics (K Mati) Consortium | Technical Project Manager |
| **Upstream Baseline Anchor**| [`01-project-charter.md`](./01-project-charter.md) | [`03-project-scope.md`](./03-project-scope.md) |
| **Downstream Governance** | [`14-project-milestones.md`](./14-project-milestones.md) | [`15-release-strategy.md`](./15-release-strategy.md) | [`18-change-management.md`](./18-change-management.md) |

---

## 1. Executive Summary & Dependency Management Strategy
The **Project Dependency Management Baseline** establishes the comprehensive directed acyclic graph (DAG), critical path sequence, inter-squad handoff protocols, and contingency fallbacks for exactly 75 project dependencies across the 18-sprint / 36-week schedule of the Namma Clinic Digital Health & Operations Platform.

### 1.1 Program Mandate and Complex Inter-Agency Web
Digital transformation across 183 clinics relies heavily on upstream municipal physical infrastructure, state drug supplies, central digital health APIs (ABDM / UIDAI), telco cellular connectivity, and cross-squad software integration handoffs. A delay in physical mini-PC procurement, failure to register Namma Clinics in the National Health Facility Registry (HFR), or late delivery of PostgreSQL schemas instantly cascades across downstream clinical testing and pilot rollouts. Proactive dependency management with hard blocking gates prevents uncoordinated drift.

### 1.2 Dependency Taxonomy & Relationship Types
Every dependency is classified using formal Precedence Diagramming Method (PDM) relationship types:
1. **Finish-to-Start (FS):** Task B cannot start until Task A finishes. (Standard critical path dependency).
2. **Start-to-Start (SS):** Task B can start once Task A has started. (Concurrent engineering).
3. **Finish-to-Finish (FF):** Task B cannot finish until Task A finishes. (Milestone synchronization).
4. **Start-to-Finish (SF):** Task B cannot finish until Task A starts. (Legacy system cutover).

Dependencies are further grouped by boundary ownership:
- **Internal Cross-Squad (INT):** Coordination between Backend, Frontend, Database, and QA squads.
- **Municipal / Government (GOV):** Approvals and hardware provided by BBMP, GBA, or Karnataka State Health Dept.
- **External Ecosystem & Regulators (EXT):** National Health Authority (ABDM), UIDAI (Aadhaar), CERT-In, Cloud Datacenter.
- **Commercial Vendor & Hardware (VEN):** Mini-PC OEMs, thermal printer distributors, and telco 4G providers.

## 2. Critical Path Analysis Across 18 Sprints (36 Weeks)
The critical path represents the minimum sequence of dependent activities directly determining the citywide production launch date:

```mermaid
graph LR
    S01["S01-S02: Baseline & Fastify Core"] --> S03["S03-S04: PostgreSQL & Dexie Offline"]
    S03 --> S05["S05-S06: Clinical Consultation MVP"]
    S05 --> S07["S07-S08: 14 Lab & 120 Drug Pharmacy"]
    S07 --> S09["S09-S10: 20-Clinic Pilot Testbed"]
    S09 --> S11["S11-S12: Pilot Stabilization & Security Audit"]
    S11 --> S13["S13-S14: Scale Phase 1 (80 Clinics)"]
    S13 --> S15["S15-S16: Scale Phase 2 (183 Clinics)"]
    S15 --> S17["S17-S18: Citywide Hypercare & Handover"]
```

### 2.1 Critical Path Invariants
- **Zero Buffer on Critical Path:** Any slip in a Critical Path dependency (`FS` with `Blocking: True`) directly delays Milestone `MILESTONE-022`.
- **Mandatory 48-Hour Early Warning:** Dependency providers must notify the PMO at least 48 hours prior to an anticipated due date breach.
- **Automated Blocker Status Reporting:** Blocked dependencies immediately trigger Amber or Red status in the weekly project health model (`DOC-PM-020`).

## 3. Master Dependencies Directory Table (DEPENDENCY-001 to DEPENDENCY-075)
Authoritative catalog of all 75 formally tracked project dependencies:

| Dep ID | Dependency Title | Category | Type | Provider Cadre | Consumer Cadre | Target Due Date | Criticality | Blocking Status |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: | :---: | :---: |
| [`DEPENDENCY-001`](#dependency-001) | **Hardware Mini-PC Procurement & Staging...** | `Hardware` | `Finish-to-Start (FS)` | BBMP IT Cell | Infrastructure Squad | `Sprint 10` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-002`](#dependency-002) | **1000VA UPS Battery Installation at Clinic Sit...** | `Hardware` | `Finish-to-Start (FS)` | BBMP Electrical Wing | Infrastructure Squad | `Sprint 10` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-003`](#dependency-003) | **Dual-SIM LTE Dongle & Static IP Provisioning...** | `Network` | `Finish-to-Start (FS)` | BBMP IT / Telecom Vendors | Infrastructure Squad | `Sprint 10` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-004`](#dependency-004) | **NHA ABDM Sandbox Gateway Credentials...** | `Regulatory` | `Finish-to-Start (FS)` | National Health Authority | Integrations Squad | `Sprint 06` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-005`](#dependency-005) | **Karnataka State HMIS Daily XML Endpoint Schem...** | `Compliance` | `Finish-to-Start (FS)` | Karnataka State DHS | Integrations Squad | `Sprint 08` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-006`](#dependency-006) | **CDAC Mobile Seva SMS DLT Template Registratio...** | `Telecom` | `Finish-to-Start (FS)` | CDAC / TRAI | Integrations Squad | `Sprint 05` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-007`](#dependency-007) | **Karnataka State EDL Formulary Official Sign-O...** | `Clinical` | `Finish-to-Start (FS)` | Chief Health Officer | Clinical Squad | `Sprint 02` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-008`](#dependency-008) | **Point-of-Care Laboratory 14-Test Kit Validati...** | `Clinical` | `Finish-to-Start (FS)` | Chief Health Officer | Clinical Squad | `Sprint 04` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-009`](#dependency-009) | **Municipal Clinic Staffing Roster & Employee I...** | `Operational` | `Finish-to-Start (FS)` | BBMP Administration | Identity & Auth Squad | `Sprint 04` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-010`](#dependency-010) | **Zonal Clinic Pilot Site Selection (20 Clinics...** | `Operational` | `Finish-to-Start (FS)` | Project Steering Committee | Deployment Squad | `Sprint 08` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-011`](#dependency-011) | **MeghRaj Sovereign Cloud Virtual Machine Alloc...** | `Infrastructure` | `Finish-to-Start (FS)` | NIC Cloud Team | DevOps & SRE Squad | `Sprint 03` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-012`](#dependency-012) | **AWS Mumbai Secondary Availability Zone Hostin...** | `Infrastructure` | `Finish-to-Start (FS)` | Consortium DevOps Lead | DevOps & SRE Squad | `Sprint 02` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-013`](#dependency-013) | **Independent CERT-In Empaneled VAPT Audit Clea...** | `Security` | `Finish-to-Start (FS)` | CERT-In Empaneled Auditor | Security Squad | `Sprint 16` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-014`](#dependency-014) | **DPDP Act 2023 Consent Workflow Legal Clearanc...** | `Legal` | `Finish-to-Start (FS)` | BBMP Legal Cell | Security Squad | `Sprint 10` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-015`](#dependency-015) | **Bilingual Frontline Training Facility Procure...** | `Operations` | `Finish-to-Start (FS)` | BBMP Zonal Health Officers | Training Squad | `Sprint 10` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-016`](#dependency-016) | **Hardware Mini-PC Procurement & Staging #16...** | `Hardware` | `Finish-to-Start (FS)` | BBMP IT Cell | Infrastructure Squad | `Sprint 10` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-017`](#dependency-017) | **1000VA UPS Battery Installation at Clinic Sit...** | `Hardware` | `Finish-to-Start (FS)` | BBMP Electrical Wing | Infrastructure Squad | `Sprint 10` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-018`](#dependency-018) | **Dual-SIM LTE Dongle & Static IP Provisioning ...** | `Network` | `Finish-to-Start (FS)` | BBMP IT / Telecom Vendors | Infrastructure Squad | `Sprint 10` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-019`](#dependency-019) | **NHA ABDM Sandbox Gateway Credentials #19...** | `Regulatory` | `Finish-to-Start (FS)` | National Health Authority | Integrations Squad | `Sprint 06` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-020`](#dependency-020) | **Karnataka State HMIS Daily XML Endpoint Schem...** | `Compliance` | `Finish-to-Start (FS)` | Karnataka State DHS | Integrations Squad | `Sprint 08` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-021`](#dependency-021) | **CDAC Mobile Seva SMS DLT Template Registratio...** | `Telecom` | `Finish-to-Start (FS)` | CDAC / TRAI | Integrations Squad | `Sprint 05` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-022`](#dependency-022) | **Karnataka State EDL Formulary Official Sign-O...** | `Clinical` | `Finish-to-Start (FS)` | Chief Health Officer | Clinical Squad | `Sprint 02` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-023`](#dependency-023) | **Point-of-Care Laboratory 14-Test Kit Validati...** | `Clinical` | `Finish-to-Start (FS)` | Chief Health Officer | Clinical Squad | `Sprint 04` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-024`](#dependency-024) | **Municipal Clinic Staffing Roster & Employee I...** | `Operational` | `Finish-to-Start (FS)` | BBMP Administration | Identity & Auth Squad | `Sprint 04` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-025`](#dependency-025) | **Zonal Clinic Pilot Site Selection (20 Clinics...** | `Operational` | `Finish-to-Start (FS)` | Project Steering Committee | Deployment Squad | `Sprint 08` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-026`](#dependency-026) | **MeghRaj Sovereign Cloud Virtual Machine Alloc...** | `Infrastructure` | `Finish-to-Start (FS)` | NIC Cloud Team | DevOps & SRE Squad | `Sprint 03` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-027`](#dependency-027) | **AWS Mumbai Secondary Availability Zone Hostin...** | `Infrastructure` | `Finish-to-Start (FS)` | Consortium DevOps Lead | DevOps & SRE Squad | `Sprint 02` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-028`](#dependency-028) | **Independent CERT-In Empaneled VAPT Audit Clea...** | `Security` | `Finish-to-Start (FS)` | CERT-In Empaneled Auditor | Security Squad | `Sprint 16` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-029`](#dependency-029) | **DPDP Act 2023 Consent Workflow Legal Clearanc...** | `Legal` | `Finish-to-Start (FS)` | BBMP Legal Cell | Security Squad | `Sprint 10` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-030`](#dependency-030) | **Bilingual Frontline Training Facility Procure...** | `Operations` | `Finish-to-Start (FS)` | BBMP Zonal Health Officers | Training Squad | `Sprint 10` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-031`](#dependency-031) | **Hardware Mini-PC Procurement & Staging #31...** | `Hardware` | `Finish-to-Start (FS)` | BBMP IT Cell | Infrastructure Squad | `Sprint 10` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-032`](#dependency-032) | **1000VA UPS Battery Installation at Clinic Sit...** | `Hardware` | `Finish-to-Start (FS)` | BBMP Electrical Wing | Infrastructure Squad | `Sprint 10` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-033`](#dependency-033) | **Dual-SIM LTE Dongle & Static IP Provisioning ...** | `Network` | `Finish-to-Start (FS)` | BBMP IT / Telecom Vendors | Infrastructure Squad | `Sprint 10` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-034`](#dependency-034) | **NHA ABDM Sandbox Gateway Credentials #34...** | `Regulatory` | `Finish-to-Start (FS)` | National Health Authority | Integrations Squad | `Sprint 06` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-035`](#dependency-035) | **Karnataka State HMIS Daily XML Endpoint Schem...** | `Compliance` | `Finish-to-Start (FS)` | Karnataka State DHS | Integrations Squad | `Sprint 08` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-036`](#dependency-036) | **CDAC Mobile Seva SMS DLT Template Registratio...** | `Telecom` | `Finish-to-Start (FS)` | CDAC / TRAI | Integrations Squad | `Sprint 05` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-037`](#dependency-037) | **Karnataka State EDL Formulary Official Sign-O...** | `Clinical` | `Finish-to-Start (FS)` | Chief Health Officer | Clinical Squad | `Sprint 02` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-038`](#dependency-038) | **Point-of-Care Laboratory 14-Test Kit Validati...** | `Clinical` | `Finish-to-Start (FS)` | Chief Health Officer | Clinical Squad | `Sprint 04` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-039`](#dependency-039) | **Municipal Clinic Staffing Roster & Employee I...** | `Operational` | `Finish-to-Start (FS)` | BBMP Administration | Identity & Auth Squad | `Sprint 04` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-040`](#dependency-040) | **Zonal Clinic Pilot Site Selection (20 Clinics...** | `Operational` | `Finish-to-Start (FS)` | Project Steering Committee | Deployment Squad | `Sprint 08` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-041`](#dependency-041) | **MeghRaj Sovereign Cloud Virtual Machine Alloc...** | `Infrastructure` | `Finish-to-Start (FS)` | NIC Cloud Team | DevOps & SRE Squad | `Sprint 03` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-042`](#dependency-042) | **AWS Mumbai Secondary Availability Zone Hostin...** | `Infrastructure` | `Finish-to-Start (FS)` | Consortium DevOps Lead | DevOps & SRE Squad | `Sprint 02` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-043`](#dependency-043) | **Independent CERT-In Empaneled VAPT Audit Clea...** | `Security` | `Finish-to-Start (FS)` | CERT-In Empaneled Auditor | Security Squad | `Sprint 16` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-044`](#dependency-044) | **DPDP Act 2023 Consent Workflow Legal Clearanc...** | `Legal` | `Finish-to-Start (FS)` | BBMP Legal Cell | Security Squad | `Sprint 10` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-045`](#dependency-045) | **Bilingual Frontline Training Facility Procure...** | `Operations` | `Finish-to-Start (FS)` | BBMP Zonal Health Officers | Training Squad | `Sprint 10` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-046`](#dependency-046) | **Hardware Mini-PC Procurement & Staging #46...** | `Hardware` | `Finish-to-Start (FS)` | BBMP IT Cell | Infrastructure Squad | `Sprint 10` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-047`](#dependency-047) | **1000VA UPS Battery Installation at Clinic Sit...** | `Hardware` | `Finish-to-Start (FS)` | BBMP Electrical Wing | Infrastructure Squad | `Sprint 10` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-048`](#dependency-048) | **Dual-SIM LTE Dongle & Static IP Provisioning ...** | `Network` | `Finish-to-Start (FS)` | BBMP IT / Telecom Vendors | Infrastructure Squad | `Sprint 10` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-049`](#dependency-049) | **NHA ABDM Sandbox Gateway Credentials #49...** | `Regulatory` | `Finish-to-Start (FS)` | National Health Authority | Integrations Squad | `Sprint 06` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-050`](#dependency-050) | **Karnataka State HMIS Daily XML Endpoint Schem...** | `Compliance` | `Finish-to-Start (FS)` | Karnataka State DHS | Integrations Squad | `Sprint 08` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-051`](#dependency-051) | **CDAC Mobile Seva SMS DLT Template Registratio...** | `Telecom` | `Finish-to-Start (FS)` | CDAC / TRAI | Integrations Squad | `Sprint 05` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-052`](#dependency-052) | **Karnataka State EDL Formulary Official Sign-O...** | `Clinical` | `Finish-to-Start (FS)` | Chief Health Officer | Clinical Squad | `Sprint 02` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-053`](#dependency-053) | **Point-of-Care Laboratory 14-Test Kit Validati...** | `Clinical` | `Finish-to-Start (FS)` | Chief Health Officer | Clinical Squad | `Sprint 04` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-054`](#dependency-054) | **Municipal Clinic Staffing Roster & Employee I...** | `Operational` | `Finish-to-Start (FS)` | BBMP Administration | Identity & Auth Squad | `Sprint 04` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-055`](#dependency-055) | **Zonal Clinic Pilot Site Selection (20 Clinics...** | `Operational` | `Finish-to-Start (FS)` | Project Steering Committee | Deployment Squad | `Sprint 08` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-056`](#dependency-056) | **MeghRaj Sovereign Cloud Virtual Machine Alloc...** | `Infrastructure` | `Finish-to-Start (FS)` | NIC Cloud Team | DevOps & SRE Squad | `Sprint 03` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-057`](#dependency-057) | **AWS Mumbai Secondary Availability Zone Hostin...** | `Infrastructure` | `Finish-to-Start (FS)` | Consortium DevOps Lead | DevOps & SRE Squad | `Sprint 02` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-058`](#dependency-058) | **Independent CERT-In Empaneled VAPT Audit Clea...** | `Security` | `Finish-to-Start (FS)` | CERT-In Empaneled Auditor | Security Squad | `Sprint 16` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-059`](#dependency-059) | **DPDP Act 2023 Consent Workflow Legal Clearanc...** | `Legal` | `Finish-to-Start (FS)` | BBMP Legal Cell | Security Squad | `Sprint 10` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-060`](#dependency-060) | **Bilingual Frontline Training Facility Procure...** | `Operations` | `Finish-to-Start (FS)` | BBMP Zonal Health Officers | Training Squad | `Sprint 10` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-061`](#dependency-061) | **Hardware Mini-PC Procurement & Staging #61...** | `Hardware` | `Finish-to-Start (FS)` | BBMP IT Cell | Infrastructure Squad | `Sprint 10` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-062`](#dependency-062) | **1000VA UPS Battery Installation at Clinic Sit...** | `Hardware` | `Finish-to-Start (FS)` | BBMP Electrical Wing | Infrastructure Squad | `Sprint 10` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-063`](#dependency-063) | **Dual-SIM LTE Dongle & Static IP Provisioning ...** | `Network` | `Finish-to-Start (FS)` | BBMP IT / Telecom Vendors | Infrastructure Squad | `Sprint 10` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-064`](#dependency-064) | **NHA ABDM Sandbox Gateway Credentials #64...** | `Regulatory` | `Finish-to-Start (FS)` | National Health Authority | Integrations Squad | `Sprint 06` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-065`](#dependency-065) | **Karnataka State HMIS Daily XML Endpoint Schem...** | `Compliance` | `Finish-to-Start (FS)` | Karnataka State DHS | Integrations Squad | `Sprint 08` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-066`](#dependency-066) | **CDAC Mobile Seva SMS DLT Template Registratio...** | `Telecom` | `Finish-to-Start (FS)` | CDAC / TRAI | Integrations Squad | `Sprint 05` | `MEDIUM` | `Non-Blocking` |
| [`DEPENDENCY-067`](#dependency-067) | **Karnataka State EDL Formulary Official Sign-O...** | `Clinical` | `Finish-to-Start (FS)` | Chief Health Officer | Clinical Squad | `Sprint 02` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-068`](#dependency-068) | **Point-of-Care Laboratory 14-Test Kit Validati...** | `Clinical` | `Finish-to-Start (FS)` | Chief Health Officer | Clinical Squad | `Sprint 04` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-069`](#dependency-069) | **Municipal Clinic Staffing Roster & Employee I...** | `Operational` | `Finish-to-Start (FS)` | BBMP Administration | Identity & Auth Squad | `Sprint 04` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-070`](#dependency-070) | **Zonal Clinic Pilot Site Selection (20 Clinics...** | `Operational` | `Finish-to-Start (FS)` | Project Steering Committee | Deployment Squad | `Sprint 08` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-071`](#dependency-071) | **MeghRaj Sovereign Cloud Virtual Machine Alloc...** | `Infrastructure` | `Finish-to-Start (FS)` | NIC Cloud Team | DevOps & SRE Squad | `Sprint 03` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-072`](#dependency-072) | **AWS Mumbai Secondary Availability Zone Hostin...** | `Infrastructure` | `Finish-to-Start (FS)` | Consortium DevOps Lead | DevOps & SRE Squad | `Sprint 02` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-073`](#dependency-073) | **Independent CERT-In Empaneled VAPT Audit Clea...** | `Security` | `Finish-to-Start (FS)` | CERT-In Empaneled Auditor | Security Squad | `Sprint 16` | `HIGH` | `BLOCKING` |
| [`DEPENDENCY-074`](#dependency-074) | **DPDP Act 2023 Consent Workflow Legal Clearanc...** | `Legal` | `Finish-to-Start (FS)` | BBMP Legal Cell | Security Squad | `Sprint 10` | `HIGH` | `Non-Blocking` |
| [`DEPENDENCY-075`](#dependency-075) | **Bilingual Frontline Training Facility Procure...** | `Operations` | `Finish-to-Start (FS)` | BBMP Zonal Health Officers | Training Squad | `Sprint 10` | `MEDIUM` | `Non-Blocking` |

## 4. Deep Dependency Specifications & Inter-Squad Handoff Protocols
Exhaustive specifications for all 75 dependencies detailing provider/consumer contracts, completion criteria, fallback paths, and critical path impacts:

### 4.1 DEPENDENCY-001: Hardware Mini-PC Procurement & Staging
- **Dependency Identifier:** `DEPENDENCY-001` — **Hardware Mini-PC Procurement & Staging**
- **Functional Category:** `Hardware` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP IT Cell must procure, image, and deliver 183 mini-PCs to clinic sites.
- **Provider Entity (Upstream Authority):** `BBMP IT Cell`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) (Governed by [`GOV-001`](./09-governance-model.md#gov-001)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-001`](./06-stakeholders.md#stakeholder-001).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-001`](./14-project-milestones.md#milestone-001) and deployment gate [`RELEASE-001`](./15-release-strategy.md#release-001).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-001`](./12-project-risks.md#risk-001).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-001`](./10-project-assumptions.md#assumption-001).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-001`](./11-project-constraints.md#constraint-001).
- **Pre-Approved Architectural & Operational Fallback:** Procure refurbished terminals as temporary pilot buffer.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.2 DEPENDENCY-002: 1000VA UPS Battery Installation at Clinic Sites
- **Dependency Identifier:** `DEPENDENCY-002` — **1000VA UPS Battery Installation at Clinic Sites**
- **Functional Category:** `Hardware` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Installation of calibrated UPS power units with dedicated earthing in all clinics.
- **Provider Entity (Upstream Authority):** `BBMP Electrical Wing`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) (Governed by [`GOV-002`](./09-governance-model.md#gov-002)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-002`](./06-stakeholders.md#stakeholder-002).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-002`](./14-project-milestones.md#milestone-002) and deployment gate [`RELEASE-002`](./15-release-strategy.md#release-002).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-002`](./12-project-risks.md#risk-002).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-002`](./10-project-assumptions.md#assumption-002).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-002`](./11-project-constraints.md#constraint-002).
- **Pre-Approved Architectural & Operational Fallback:** Deploy surge protector strips with portable battery packs.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.3 DEPENDENCY-003: Dual-SIM LTE Dongle & Static IP Provisioning
- **Dependency Identifier:** `DEPENDENCY-003` — **Dual-SIM LTE Dongle & Static IP Provisioning**
- **Functional Category:** `Network` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Procurement and static IP assignment for Airtel and Jio SIM cards across 183 clinics.
- **Provider Entity (Upstream Authority):** `BBMP IT / Telecom Vendors`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) (Governed by [`GOV-003`](./09-governance-model.md#gov-003)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-003`](./06-stakeholders.md#stakeholder-003).
- **Execution Preconditions (Start Condition):** `Sprint 03`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-003`](./14-project-milestones.md#milestone-003) and deployment gate [`RELEASE-003`](./15-release-strategy.md#release-003).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-003`](./12-project-risks.md#risk-003).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-003`](./10-project-assumptions.md#assumption-003).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-003`](./11-project-constraints.md#constraint-003).
- **Pre-Approved Architectural & Operational Fallback:** Use dynamic DNS over standard broadband tethering.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.4 DEPENDENCY-004: NHA ABDM Sandbox Gateway Credentials
- **Dependency Identifier:** `DEPENDENCY-004` — **NHA ABDM Sandbox Gateway Credentials**
- **Functional Category:** `Regulatory` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** National Health Authority issuing production API client keys for M1/M2/M3 gateways.
- **Provider Entity (Upstream Authority):** `National Health Authority`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) (Governed by [`GOV-004`](./09-governance-model.md#gov-004)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-004`](./06-stakeholders.md#stakeholder-004).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 06`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 06`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-004`](./14-project-milestones.md#milestone-004) and deployment gate [`RELEASE-004`](./15-release-strategy.md#release-004).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-004`](./12-project-risks.md#risk-004).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-004`](./10-project-assumptions.md#assumption-004).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-004`](./11-project-constraints.md#constraint-004).
- **Pre-Approved Architectural & Operational Fallback:** Utilize ABDM mock sandbox server in local Docker container.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.5 DEPENDENCY-005: Karnataka State HMIS Daily XML Endpoint Schema
- **Dependency Identifier:** `DEPENDENCY-005` — **Karnataka State HMIS Daily XML Endpoint Schema**
- **Functional Category:** `Compliance` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** State DHS delivering finalized XML and JSON schema definitions for daily uploads.
- **Provider Entity (Upstream Authority):** `Karnataka State DHS`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) (Governed by [`GOV-005`](./09-governance-model.md#gov-005)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-005`](./06-stakeholders.md#stakeholder-005).
- **Execution Preconditions (Start Condition):** `Sprint 03`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 08`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 08`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-005`](./14-project-milestones.md#milestone-005) and deployment gate [`RELEASE-005`](./15-release-strategy.md#release-005).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-005`](./12-project-risks.md#risk-005).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-005`](./10-project-assumptions.md#assumption-005).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-005`](./11-project-constraints.md#constraint-005).
- **Pre-Approved Architectural & Operational Fallback:** Generate standardized interim CSV export for manual upload.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.6 DEPENDENCY-006: CDAC Mobile Seva SMS DLT Template Registration
- **Dependency Identifier:** `DEPENDENCY-006` — **CDAC Mobile Seva SMS DLT Template Registration**
- **Functional Category:** `Telecom` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** TRAI portal approval of Kannada and English transactional SMS prescription templates.
- **Provider Entity (Upstream Authority):** `CDAC / TRAI`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) (Governed by [`GOV-006`](./09-governance-model.md#gov-006)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-006`](./06-stakeholders.md#stakeholder-006).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 05`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 05`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-006`](./14-project-milestones.md#milestone-006) and deployment gate [`RELEASE-006`](./15-release-strategy.md#release-006).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-006`](./12-project-risks.md#risk-006).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-006`](./10-project-assumptions.md#assumption-006).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-006`](./11-project-constraints.md#constraint-006).
- **Pre-Approved Architectural & Operational Fallback:** Direct patient to display on-screen QR code for camera capture.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.7 DEPENDENCY-007: Karnataka State EDL Formulary Official Sign-Off
- **Dependency Identifier:** `DEPENDENCY-007` — **Karnataka State EDL Formulary Official Sign-Off**
- **Functional Category:** `Clinical` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Chief Health Officer signing off on canonical 120-drug Karnataka EDL master formulary.
- **Provider Entity (Upstream Authority):** `Chief Health Officer`
- **Consumer Entity (Downstream Squad):** `Clinical Squad`
- **Accountable Delivery Steward:** [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) (Governed by [`GOV-007`](./09-governance-model.md#gov-007)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-007`](./06-stakeholders.md#stakeholder-007).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 02`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 02`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-007`](./14-project-milestones.md#milestone-007) and deployment gate [`RELEASE-007`](./15-release-strategy.md#release-007).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-007`](./12-project-risks.md#risk-007).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-007`](./10-project-assumptions.md#assumption-007).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-007`](./11-project-constraints.md#constraint-007).
- **Pre-Approved Architectural & Operational Fallback:** Base EMR formulary on draft 2024 DHS Essential Drug List.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.8 DEPENDENCY-008: Point-of-Care Laboratory 14-Test Kit Validation
- **Dependency Identifier:** `DEPENDENCY-008` — **Point-of-Care Laboratory 14-Test Kit Validation**
- **Functional Category:** `Clinical` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Clinical validation of diagnostic test list against available clinic rapid test reagents.
- **Provider Entity (Upstream Authority):** `Chief Health Officer`
- **Consumer Entity (Downstream Squad):** `Clinical Squad`
- **Accountable Delivery Steward:** [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) (Governed by [`GOV-008`](./09-governance-model.md#gov-008)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-008`](./06-stakeholders.md#stakeholder-008).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 04`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 04`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-008`](./14-project-milestones.md#milestone-008) and deployment gate [`RELEASE-008`](./15-release-strategy.md#release-008).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-008`](./12-project-risks.md#risk-008).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-008`](./10-project-assumptions.md#assumption-008).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-008`](./11-project-constraints.md#constraint-008).
- **Pre-Approved Architectural & Operational Fallback:** Enable electronic ordering only for confirmed available tests.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.9 DEPENDENCY-009: Municipal Clinic Staffing Roster & Employee IDs
- **Dependency Identifier:** `DEPENDENCY-009` — **Municipal Clinic Staffing Roster & Employee IDs**
- **Functional Category:** `Operational` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP Admin providing verified employee numbers and phone numbers for all 750+ staff.
- **Provider Entity (Upstream Authority):** `BBMP Administration`
- **Consumer Entity (Downstream Squad):** `Identity & Auth Squad`
- **Accountable Delivery Steward:** [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) (Governed by [`GOV-009`](./09-governance-model.md#gov-009)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-009`](./06-stakeholders.md#stakeholder-009).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 04`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 04`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-009`](./14-project-milestones.md#milestone-009) and deployment gate [`RELEASE-009`](./15-release-strategy.md#release-009).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-009`](./12-project-risks.md#risk-009).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-009`](./10-project-assumptions.md#assumption-009).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-009`](./11-project-constraints.md#constraint-009).
- **Pre-Approved Architectural & Operational Fallback:** Generate provisional local clinic accounts validated by doctor.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.10 DEPENDENCY-010: Zonal Clinic Pilot Site Selection (20 Clinics)
- **Dependency Identifier:** `DEPENDENCY-010` — **Zonal Clinic Pilot Site Selection (20 Clinics)**
- **Functional Category:** `Operational` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Steering committee designating exactly 20 clinics across East and West zones for pilot.
- **Provider Entity (Upstream Authority):** `Project Steering Committee`
- **Consumer Entity (Downstream Squad):** `Deployment Squad`
- **Accountable Delivery Steward:** [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) (Governed by [`GOV-010`](./09-governance-model.md#gov-010)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-010`](./06-stakeholders.md#stakeholder-010).
- **Execution Preconditions (Start Condition):** `Sprint 06`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 08`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 08`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-010`](./14-project-milestones.md#milestone-010) and deployment gate [`RELEASE-010`](./15-release-strategy.md#release-010).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-010`](./12-project-risks.md#risk-010).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-010`](./10-project-assumptions.md#assumption-010).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-010`](./11-project-constraints.md#constraint-010).
- **Pre-Approved Architectural & Operational Fallback:** Select top 20 clinics based on discovery audit infrastructure.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.11 DEPENDENCY-011: MeghRaj Sovereign Cloud Virtual Machine Allocation
- **Dependency Identifier:** `DEPENDENCY-011` — **MeghRaj Sovereign Cloud Virtual Machine Allocation**
- **Functional Category:** `Infrastructure` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** NIC provisioning primary Kubernetes compute cluster and managed PostgreSQL instance.
- **Provider Entity (Upstream Authority):** `NIC Cloud Team`
- **Consumer Entity (Downstream Squad):** `DevOps & SRE Squad`
- **Accountable Delivery Steward:** [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) (Governed by [`GOV-011`](./09-governance-model.md#gov-011)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-011`](./06-stakeholders.md#stakeholder-011).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 03`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 03`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-011`](./14-project-milestones.md#milestone-011) and deployment gate [`RELEASE-011`](./15-release-strategy.md#release-011).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-011`](./12-project-risks.md#risk-011).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-011`](./10-project-assumptions.md#assumption-011).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-011`](./11-project-constraints.md#constraint-011).
- **Pre-Approved Architectural & Operational Fallback:** Host initial environments on AWS Mumbai cloud infrastructure.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.12 DEPENDENCY-012: AWS Mumbai Secondary Availability Zone Hosting
- **Dependency Identifier:** `DEPENDENCY-012` — **AWS Mumbai Secondary Availability Zone Hosting**
- **Functional Category:** `Infrastructure` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** AWS consortium account configuration with VPC peering and KMS encryption keys.
- **Provider Entity (Upstream Authority):** `Consortium DevOps Lead`
- **Consumer Entity (Downstream Squad):** `DevOps & SRE Squad`
- **Accountable Delivery Steward:** [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) (Governed by [`GOV-012`](./09-governance-model.md#gov-012)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-012`](./06-stakeholders.md#stakeholder-012).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 02`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 02`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-012`](./14-project-milestones.md#milestone-012) and deployment gate [`RELEASE-012`](./15-release-strategy.md#release-012).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-012`](./12-project-risks.md#risk-012).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-012`](./10-project-assumptions.md#assumption-012).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-012`](./11-project-constraints.md#constraint-012).
- **Pre-Approved Architectural & Operational Fallback:** Operate single-region deployment during development sprints.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.13 DEPENDENCY-013: Independent CERT-In Empaneled VAPT Audit Clearance
- **Dependency Identifier:** `DEPENDENCY-013` — **Independent CERT-In Empaneled VAPT Audit Clearance**
- **Functional Category:** `Security` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Independent cybersecurity auditor completing penetration testing and issuing certificate.
- **Provider Entity (Upstream Authority):** `CERT-In Empaneled Auditor`
- **Consumer Entity (Downstream Squad):** `Security Squad`
- **Accountable Delivery Steward:** [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) (Governed by [`GOV-013`](./09-governance-model.md#gov-013)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-013`](./06-stakeholders.md#stakeholder-013).
- **Execution Preconditions (Start Condition):** `Sprint 14`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 16`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 16`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-013`](./14-project-milestones.md#milestone-013) and deployment gate [`RELEASE-013`](./15-release-strategy.md#release-013).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-013`](./12-project-risks.md#risk-013).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-013`](./10-project-assumptions.md#assumption-013).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-013`](./11-project-constraints.md#constraint-013).
- **Pre-Approved Architectural & Operational Fallback:** Remediate high findings within 48h emergency sprint window.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.14 DEPENDENCY-014: DPDP Act 2023 Consent Workflow Legal Clearance
- **Dependency Identifier:** `DEPENDENCY-014` — **DPDP Act 2023 Consent Workflow Legal Clearance**
- **Functional Category:** `Legal` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP Legal Cell formal written approval of digital patient consent capture mechanism.
- **Provider Entity (Upstream Authority):** `BBMP Legal Cell`
- **Consumer Entity (Downstream Squad):** `Security Squad`
- **Accountable Delivery Steward:** [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) (Governed by [`GOV-014`](./09-governance-model.md#gov-014)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-014`](./06-stakeholders.md#stakeholder-014).
- **Execution Preconditions (Start Condition):** `Sprint 08`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-014`](./14-project-milestones.md#milestone-014) and deployment gate [`RELEASE-014`](./15-release-strategy.md#release-014).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-014`](./12-project-risks.md#risk-014).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-014`](./10-project-assumptions.md#assumption-014).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-014`](./11-project-constraints.md#constraint-014).
- **Pre-Approved Architectural & Operational Fallback:** Proceed with conservative explicit opt-in checkbox model.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.15 DEPENDENCY-015: Bilingual Frontline Training Facility Procurement
- **Dependency Identifier:** `DEPENDENCY-015` — **Bilingual Frontline Training Facility Procurement**
- **Functional Category:** `Operations` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP providing 8 zonal training halls equipped with demo PCs for hands-on labs.
- **Provider Entity (Upstream Authority):** `BBMP Zonal Health Officers`
- **Consumer Entity (Downstream Squad):** `Training Squad`
- **Accountable Delivery Steward:** [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) (Governed by [`GOV-015`](./09-governance-model.md#gov-015)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-015`](./06-stakeholders.md#stakeholder-015).
- **Execution Preconditions (Start Condition):** `Sprint 08`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-015`](./14-project-milestones.md#milestone-015) and deployment gate [`RELEASE-015`](./15-release-strategy.md#release-015).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-015`](./12-project-risks.md#risk-015).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-015`](./10-project-assumptions.md#assumption-015).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-015`](./11-project-constraints.md#constraint-015).
- **Pre-Approved Architectural & Operational Fallback:** Conduct mobile on-site training sessions inside clinic facilities.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.16 DEPENDENCY-016: Hardware Mini-PC Procurement & Staging #16
- **Dependency Identifier:** `DEPENDENCY-016` — **Hardware Mini-PC Procurement & Staging #16**
- **Functional Category:** `Hardware` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP IT Cell must procure, image, and deliver 183 mini-PCs to clinic sites.
- **Provider Entity (Upstream Authority):** `BBMP IT Cell`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) (Governed by [`GOV-016`](./09-governance-model.md#gov-016)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-016`](./06-stakeholders.md#stakeholder-016).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-016`](./14-project-milestones.md#milestone-016) and deployment gate [`RELEASE-016`](./15-release-strategy.md#release-016).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-016`](./12-project-risks.md#risk-016).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-016`](./10-project-assumptions.md#assumption-016).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-016`](./11-project-constraints.md#constraint-016).
- **Pre-Approved Architectural & Operational Fallback:** Procure refurbished terminals as temporary pilot buffer.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.17 DEPENDENCY-017: 1000VA UPS Battery Installation at Clinic Sites #17
- **Dependency Identifier:** `DEPENDENCY-017` — **1000VA UPS Battery Installation at Clinic Sites #17**
- **Functional Category:** `Hardware` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Installation of calibrated UPS power units with dedicated earthing in all clinics.
- **Provider Entity (Upstream Authority):** `BBMP Electrical Wing`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) (Governed by [`GOV-017`](./09-governance-model.md#gov-017)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-017`](./06-stakeholders.md#stakeholder-017).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-017`](./14-project-milestones.md#milestone-017) and deployment gate [`RELEASE-017`](./15-release-strategy.md#release-017).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-017`](./12-project-risks.md#risk-017).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-017`](./10-project-assumptions.md#assumption-017).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-017`](./11-project-constraints.md#constraint-017).
- **Pre-Approved Architectural & Operational Fallback:** Deploy surge protector strips with portable battery packs.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.18 DEPENDENCY-018: Dual-SIM LTE Dongle & Static IP Provisioning #18
- **Dependency Identifier:** `DEPENDENCY-018` — **Dual-SIM LTE Dongle & Static IP Provisioning #18**
- **Functional Category:** `Network` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Procurement and static IP assignment for Airtel and Jio SIM cards across 183 clinics.
- **Provider Entity (Upstream Authority):** `BBMP IT / Telecom Vendors`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) (Governed by [`GOV-018`](./09-governance-model.md#gov-018)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-018`](./06-stakeholders.md#stakeholder-018).
- **Execution Preconditions (Start Condition):** `Sprint 03`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-018`](./14-project-milestones.md#milestone-018) and deployment gate [`RELEASE-018`](./15-release-strategy.md#release-018).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-018`](./12-project-risks.md#risk-018).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-018`](./10-project-assumptions.md#assumption-018).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-018`](./11-project-constraints.md#constraint-018).
- **Pre-Approved Architectural & Operational Fallback:** Use dynamic DNS over standard broadband tethering.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.19 DEPENDENCY-019: NHA ABDM Sandbox Gateway Credentials #19
- **Dependency Identifier:** `DEPENDENCY-019` — **NHA ABDM Sandbox Gateway Credentials #19**
- **Functional Category:** `Regulatory` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** National Health Authority issuing production API client keys for M1/M2/M3 gateways.
- **Provider Entity (Upstream Authority):** `National Health Authority`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) (Governed by [`GOV-019`](./09-governance-model.md#gov-019)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-019`](./06-stakeholders.md#stakeholder-019).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 06`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 06`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-019`](./14-project-milestones.md#milestone-019) and deployment gate [`RELEASE-019`](./15-release-strategy.md#release-019).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-019`](./12-project-risks.md#risk-019).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-019`](./10-project-assumptions.md#assumption-019).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-019`](./11-project-constraints.md#constraint-019).
- **Pre-Approved Architectural & Operational Fallback:** Utilize ABDM mock sandbox server in local Docker container.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.20 DEPENDENCY-020: Karnataka State HMIS Daily XML Endpoint Schema #20
- **Dependency Identifier:** `DEPENDENCY-020` — **Karnataka State HMIS Daily XML Endpoint Schema #20**
- **Functional Category:** `Compliance` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** State DHS delivering finalized XML and JSON schema definitions for daily uploads.
- **Provider Entity (Upstream Authority):** `Karnataka State DHS`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) (Governed by [`GOV-020`](./09-governance-model.md#gov-020)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-020`](./06-stakeholders.md#stakeholder-020).
- **Execution Preconditions (Start Condition):** `Sprint 03`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 08`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 08`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-020`](./14-project-milestones.md#milestone-020) and deployment gate [`RELEASE-020`](./15-release-strategy.md#release-020).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-020`](./12-project-risks.md#risk-020).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-020`](./10-project-assumptions.md#assumption-020).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-020`](./11-project-constraints.md#constraint-020).
- **Pre-Approved Architectural & Operational Fallback:** Generate standardized interim CSV export for manual upload.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.21 DEPENDENCY-021: CDAC Mobile Seva SMS DLT Template Registration #21
- **Dependency Identifier:** `DEPENDENCY-021` — **CDAC Mobile Seva SMS DLT Template Registration #21**
- **Functional Category:** `Telecom` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** TRAI portal approval of Kannada and English transactional SMS prescription templates.
- **Provider Entity (Upstream Authority):** `CDAC / TRAI`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) (Governed by [`GOV-021`](./09-governance-model.md#gov-021)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-021`](./06-stakeholders.md#stakeholder-021).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 05`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 05`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-021`](./14-project-milestones.md#milestone-021) and deployment gate [`RELEASE-021`](./15-release-strategy.md#release-021).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-021`](./12-project-risks.md#risk-021).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-021`](./10-project-assumptions.md#assumption-021).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-021`](./11-project-constraints.md#constraint-021).
- **Pre-Approved Architectural & Operational Fallback:** Direct patient to display on-screen QR code for camera capture.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.22 DEPENDENCY-022: Karnataka State EDL Formulary Official Sign-Off #22
- **Dependency Identifier:** `DEPENDENCY-022` — **Karnataka State EDL Formulary Official Sign-Off #22**
- **Functional Category:** `Clinical` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Chief Health Officer signing off on canonical 120-drug Karnataka EDL master formulary.
- **Provider Entity (Upstream Authority):** `Chief Health Officer`
- **Consumer Entity (Downstream Squad):** `Clinical Squad`
- **Accountable Delivery Steward:** [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) (Governed by [`GOV-022`](./09-governance-model.md#gov-022)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-022`](./06-stakeholders.md#stakeholder-022).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 02`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 02`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-022`](./14-project-milestones.md#milestone-022) and deployment gate [`RELEASE-022`](./15-release-strategy.md#release-022).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-022`](./12-project-risks.md#risk-022).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-022`](./10-project-assumptions.md#assumption-022).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-022`](./11-project-constraints.md#constraint-022).
- **Pre-Approved Architectural & Operational Fallback:** Base EMR formulary on draft 2024 DHS Essential Drug List.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.23 DEPENDENCY-023: Point-of-Care Laboratory 14-Test Kit Validation #23
- **Dependency Identifier:** `DEPENDENCY-023` — **Point-of-Care Laboratory 14-Test Kit Validation #23**
- **Functional Category:** `Clinical` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Clinical validation of diagnostic test list against available clinic rapid test reagents.
- **Provider Entity (Upstream Authority):** `Chief Health Officer`
- **Consumer Entity (Downstream Squad):** `Clinical Squad`
- **Accountable Delivery Steward:** [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) (Governed by [`GOV-023`](./09-governance-model.md#gov-023)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-023`](./06-stakeholders.md#stakeholder-023).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 04`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 04`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-023`](./14-project-milestones.md#milestone-023) and deployment gate [`RELEASE-023`](./15-release-strategy.md#release-023).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-023`](./12-project-risks.md#risk-023).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-023`](./10-project-assumptions.md#assumption-023).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-023`](./11-project-constraints.md#constraint-023).
- **Pre-Approved Architectural & Operational Fallback:** Enable electronic ordering only for confirmed available tests.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.24 DEPENDENCY-024: Municipal Clinic Staffing Roster & Employee IDs #24
- **Dependency Identifier:** `DEPENDENCY-024` — **Municipal Clinic Staffing Roster & Employee IDs #24**
- **Functional Category:** `Operational` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP Admin providing verified employee numbers and phone numbers for all 750+ staff.
- **Provider Entity (Upstream Authority):** `BBMP Administration`
- **Consumer Entity (Downstream Squad):** `Identity & Auth Squad`
- **Accountable Delivery Steward:** [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) (Governed by [`GOV-024`](./09-governance-model.md#gov-024)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-024`](./06-stakeholders.md#stakeholder-024).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 04`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 04`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-024`](./14-project-milestones.md#milestone-024) and deployment gate [`RELEASE-024`](./15-release-strategy.md#release-024).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-024`](./12-project-risks.md#risk-024).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-024`](./10-project-assumptions.md#assumption-024).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-024`](./11-project-constraints.md#constraint-024).
- **Pre-Approved Architectural & Operational Fallback:** Generate provisional local clinic accounts validated by doctor.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.25 DEPENDENCY-025: Zonal Clinic Pilot Site Selection (20 Clinics) #25
- **Dependency Identifier:** `DEPENDENCY-025` — **Zonal Clinic Pilot Site Selection (20 Clinics) #25**
- **Functional Category:** `Operational` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Steering committee designating exactly 20 clinics across East and West zones for pilot.
- **Provider Entity (Upstream Authority):** `Project Steering Committee`
- **Consumer Entity (Downstream Squad):** `Deployment Squad`
- **Accountable Delivery Steward:** [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) (Governed by [`GOV-025`](./09-governance-model.md#gov-025)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-025`](./06-stakeholders.md#stakeholder-025).
- **Execution Preconditions (Start Condition):** `Sprint 06`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 08`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 08`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-025`](./14-project-milestones.md#milestone-025) and deployment gate [`RELEASE-025`](./15-release-strategy.md#release-025).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-025`](./12-project-risks.md#risk-025).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-025`](./10-project-assumptions.md#assumption-025).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-025`](./11-project-constraints.md#constraint-025).
- **Pre-Approved Architectural & Operational Fallback:** Select top 20 clinics based on discovery audit infrastructure.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.26 DEPENDENCY-026: MeghRaj Sovereign Cloud Virtual Machine Allocation #26
- **Dependency Identifier:** `DEPENDENCY-026` — **MeghRaj Sovereign Cloud Virtual Machine Allocation #26**
- **Functional Category:** `Infrastructure` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** NIC provisioning primary Kubernetes compute cluster and managed PostgreSQL instance.
- **Provider Entity (Upstream Authority):** `NIC Cloud Team`
- **Consumer Entity (Downstream Squad):** `DevOps & SRE Squad`
- **Accountable Delivery Steward:** [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) (Governed by [`GOV-026`](./09-governance-model.md#gov-026)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-026`](./06-stakeholders.md#stakeholder-026).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 03`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 03`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-026`](./14-project-milestones.md#milestone-026) and deployment gate [`RELEASE-001`](./15-release-strategy.md#release-001).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-026`](./12-project-risks.md#risk-026).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-026`](./10-project-assumptions.md#assumption-026).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-026`](./11-project-constraints.md#constraint-026).
- **Pre-Approved Architectural & Operational Fallback:** Host initial environments on AWS Mumbai cloud infrastructure.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.27 DEPENDENCY-027: AWS Mumbai Secondary Availability Zone Hosting #27
- **Dependency Identifier:** `DEPENDENCY-027` — **AWS Mumbai Secondary Availability Zone Hosting #27**
- **Functional Category:** `Infrastructure` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** AWS consortium account configuration with VPC peering and KMS encryption keys.
- **Provider Entity (Upstream Authority):** `Consortium DevOps Lead`
- **Consumer Entity (Downstream Squad):** `DevOps & SRE Squad`
- **Accountable Delivery Steward:** [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) (Governed by [`GOV-027`](./09-governance-model.md#gov-027)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-027`](./06-stakeholders.md#stakeholder-027).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 02`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 02`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-027`](./14-project-milestones.md#milestone-027) and deployment gate [`RELEASE-002`](./15-release-strategy.md#release-002).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-027`](./12-project-risks.md#risk-027).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-027`](./10-project-assumptions.md#assumption-027).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-027`](./11-project-constraints.md#constraint-027).
- **Pre-Approved Architectural & Operational Fallback:** Operate single-region deployment during development sprints.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.28 DEPENDENCY-028: Independent CERT-In Empaneled VAPT Audit Clearance #28
- **Dependency Identifier:** `DEPENDENCY-028` — **Independent CERT-In Empaneled VAPT Audit Clearance #28**
- **Functional Category:** `Security` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Independent cybersecurity auditor completing penetration testing and issuing certificate.
- **Provider Entity (Upstream Authority):** `CERT-In Empaneled Auditor`
- **Consumer Entity (Downstream Squad):** `Security Squad`
- **Accountable Delivery Steward:** [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) (Governed by [`GOV-028`](./09-governance-model.md#gov-028)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-028`](./06-stakeholders.md#stakeholder-028).
- **Execution Preconditions (Start Condition):** `Sprint 14`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 16`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 16`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-028`](./14-project-milestones.md#milestone-028) and deployment gate [`RELEASE-003`](./15-release-strategy.md#release-003).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-028`](./12-project-risks.md#risk-028).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-028`](./10-project-assumptions.md#assumption-028).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-028`](./11-project-constraints.md#constraint-028).
- **Pre-Approved Architectural & Operational Fallback:** Remediate high findings within 48h emergency sprint window.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.29 DEPENDENCY-029: DPDP Act 2023 Consent Workflow Legal Clearance #29
- **Dependency Identifier:** `DEPENDENCY-029` — **DPDP Act 2023 Consent Workflow Legal Clearance #29**
- **Functional Category:** `Legal` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP Legal Cell formal written approval of digital patient consent capture mechanism.
- **Provider Entity (Upstream Authority):** `BBMP Legal Cell`
- **Consumer Entity (Downstream Squad):** `Security Squad`
- **Accountable Delivery Steward:** [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) (Governed by [`GOV-029`](./09-governance-model.md#gov-029)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-029`](./06-stakeholders.md#stakeholder-029).
- **Execution Preconditions (Start Condition):** `Sprint 08`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-029`](./14-project-milestones.md#milestone-029) and deployment gate [`RELEASE-004`](./15-release-strategy.md#release-004).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-029`](./12-project-risks.md#risk-029).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-029`](./10-project-assumptions.md#assumption-029).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-029`](./11-project-constraints.md#constraint-029).
- **Pre-Approved Architectural & Operational Fallback:** Proceed with conservative explicit opt-in checkbox model.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.30 DEPENDENCY-030: Bilingual Frontline Training Facility Procurement #30
- **Dependency Identifier:** `DEPENDENCY-030` — **Bilingual Frontline Training Facility Procurement #30**
- **Functional Category:** `Operations` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP providing 8 zonal training halls equipped with demo PCs for hands-on labs.
- **Provider Entity (Upstream Authority):** `BBMP Zonal Health Officers`
- **Consumer Entity (Downstream Squad):** `Training Squad`
- **Accountable Delivery Steward:** [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) (Governed by [`GOV-030`](./09-governance-model.md#gov-030)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-030`](./06-stakeholders.md#stakeholder-030).
- **Execution Preconditions (Start Condition):** `Sprint 08`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-030`](./14-project-milestones.md#milestone-030) and deployment gate [`RELEASE-005`](./15-release-strategy.md#release-005).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-030`](./12-project-risks.md#risk-030).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-030`](./10-project-assumptions.md#assumption-030).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-030`](./11-project-constraints.md#constraint-030).
- **Pre-Approved Architectural & Operational Fallback:** Conduct mobile on-site training sessions inside clinic facilities.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.31 DEPENDENCY-031: Hardware Mini-PC Procurement & Staging #31
- **Dependency Identifier:** `DEPENDENCY-031` — **Hardware Mini-PC Procurement & Staging #31**
- **Functional Category:** `Hardware` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP IT Cell must procure, image, and deliver 183 mini-PCs to clinic sites.
- **Provider Entity (Upstream Authority):** `BBMP IT Cell`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) (Governed by [`GOV-031`](./09-governance-model.md#gov-031)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-031`](./06-stakeholders.md#stakeholder-031).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-031`](./14-project-milestones.md#milestone-031) and deployment gate [`RELEASE-006`](./15-release-strategy.md#release-006).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-031`](./12-project-risks.md#risk-031).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-031`](./10-project-assumptions.md#assumption-031).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-031`](./11-project-constraints.md#constraint-031).
- **Pre-Approved Architectural & Operational Fallback:** Procure refurbished terminals as temporary pilot buffer.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.32 DEPENDENCY-032: 1000VA UPS Battery Installation at Clinic Sites #32
- **Dependency Identifier:** `DEPENDENCY-032` — **1000VA UPS Battery Installation at Clinic Sites #32**
- **Functional Category:** `Hardware` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Installation of calibrated UPS power units with dedicated earthing in all clinics.
- **Provider Entity (Upstream Authority):** `BBMP Electrical Wing`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) (Governed by [`GOV-032`](./09-governance-model.md#gov-032)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-032`](./06-stakeholders.md#stakeholder-032).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-032`](./14-project-milestones.md#milestone-032) and deployment gate [`RELEASE-007`](./15-release-strategy.md#release-007).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-032`](./12-project-risks.md#risk-032).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-032`](./10-project-assumptions.md#assumption-032).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-032`](./11-project-constraints.md#constraint-032).
- **Pre-Approved Architectural & Operational Fallback:** Deploy surge protector strips with portable battery packs.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.33 DEPENDENCY-033: Dual-SIM LTE Dongle & Static IP Provisioning #33
- **Dependency Identifier:** `DEPENDENCY-033` — **Dual-SIM LTE Dongle & Static IP Provisioning #33**
- **Functional Category:** `Network` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Procurement and static IP assignment for Airtel and Jio SIM cards across 183 clinics.
- **Provider Entity (Upstream Authority):** `BBMP IT / Telecom Vendors`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) (Governed by [`GOV-033`](./09-governance-model.md#gov-033)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-033`](./06-stakeholders.md#stakeholder-033).
- **Execution Preconditions (Start Condition):** `Sprint 03`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-033`](./14-project-milestones.md#milestone-033) and deployment gate [`RELEASE-008`](./15-release-strategy.md#release-008).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-033`](./12-project-risks.md#risk-033).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-033`](./10-project-assumptions.md#assumption-033).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-033`](./11-project-constraints.md#constraint-033).
- **Pre-Approved Architectural & Operational Fallback:** Use dynamic DNS over standard broadband tethering.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.34 DEPENDENCY-034: NHA ABDM Sandbox Gateway Credentials #34
- **Dependency Identifier:** `DEPENDENCY-034` — **NHA ABDM Sandbox Gateway Credentials #34**
- **Functional Category:** `Regulatory` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** National Health Authority issuing production API client keys for M1/M2/M3 gateways.
- **Provider Entity (Upstream Authority):** `National Health Authority`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) (Governed by [`GOV-034`](./09-governance-model.md#gov-034)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-034`](./06-stakeholders.md#stakeholder-034).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 06`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 06`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-034`](./14-project-milestones.md#milestone-034) and deployment gate [`RELEASE-009`](./15-release-strategy.md#release-009).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-034`](./12-project-risks.md#risk-034).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-034`](./10-project-assumptions.md#assumption-034).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-034`](./11-project-constraints.md#constraint-034).
- **Pre-Approved Architectural & Operational Fallback:** Utilize ABDM mock sandbox server in local Docker container.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.35 DEPENDENCY-035: Karnataka State HMIS Daily XML Endpoint Schema #35
- **Dependency Identifier:** `DEPENDENCY-035` — **Karnataka State HMIS Daily XML Endpoint Schema #35**
- **Functional Category:** `Compliance` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** State DHS delivering finalized XML and JSON schema definitions for daily uploads.
- **Provider Entity (Upstream Authority):** `Karnataka State DHS`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) (Governed by [`GOV-035`](./09-governance-model.md#gov-035)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-035`](./06-stakeholders.md#stakeholder-035).
- **Execution Preconditions (Start Condition):** `Sprint 03`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 08`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 08`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-035`](./14-project-milestones.md#milestone-035) and deployment gate [`RELEASE-010`](./15-release-strategy.md#release-010).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-035`](./12-project-risks.md#risk-035).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-035`](./10-project-assumptions.md#assumption-035).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-035`](./11-project-constraints.md#constraint-035).
- **Pre-Approved Architectural & Operational Fallback:** Generate standardized interim CSV export for manual upload.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.36 DEPENDENCY-036: CDAC Mobile Seva SMS DLT Template Registration #36
- **Dependency Identifier:** `DEPENDENCY-036` — **CDAC Mobile Seva SMS DLT Template Registration #36**
- **Functional Category:** `Telecom` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** TRAI portal approval of Kannada and English transactional SMS prescription templates.
- **Provider Entity (Upstream Authority):** `CDAC / TRAI`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) (Governed by [`GOV-036`](./09-governance-model.md#gov-036)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-036`](./06-stakeholders.md#stakeholder-036).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 05`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 05`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-036`](./14-project-milestones.md#milestone-036) and deployment gate [`RELEASE-011`](./15-release-strategy.md#release-011).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-036`](./12-project-risks.md#risk-036).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-036`](./10-project-assumptions.md#assumption-036).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-036`](./11-project-constraints.md#constraint-036).
- **Pre-Approved Architectural & Operational Fallback:** Direct patient to display on-screen QR code for camera capture.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.37 DEPENDENCY-037: Karnataka State EDL Formulary Official Sign-Off #37
- **Dependency Identifier:** `DEPENDENCY-037` — **Karnataka State EDL Formulary Official Sign-Off #37**
- **Functional Category:** `Clinical` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Chief Health Officer signing off on canonical 120-drug Karnataka EDL master formulary.
- **Provider Entity (Upstream Authority):** `Chief Health Officer`
- **Consumer Entity (Downstream Squad):** `Clinical Squad`
- **Accountable Delivery Steward:** [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) (Governed by [`GOV-037`](./09-governance-model.md#gov-037)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-037`](./06-stakeholders.md#stakeholder-037).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 02`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 02`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-037`](./14-project-milestones.md#milestone-037) and deployment gate [`RELEASE-012`](./15-release-strategy.md#release-012).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-037`](./12-project-risks.md#risk-037).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-037`](./10-project-assumptions.md#assumption-037).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-037`](./11-project-constraints.md#constraint-037).
- **Pre-Approved Architectural & Operational Fallback:** Base EMR formulary on draft 2024 DHS Essential Drug List.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.38 DEPENDENCY-038: Point-of-Care Laboratory 14-Test Kit Validation #38
- **Dependency Identifier:** `DEPENDENCY-038` — **Point-of-Care Laboratory 14-Test Kit Validation #38**
- **Functional Category:** `Clinical` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Clinical validation of diagnostic test list against available clinic rapid test reagents.
- **Provider Entity (Upstream Authority):** `Chief Health Officer`
- **Consumer Entity (Downstream Squad):** `Clinical Squad`
- **Accountable Delivery Steward:** [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) (Governed by [`GOV-038`](./09-governance-model.md#gov-038)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-038`](./06-stakeholders.md#stakeholder-038).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 04`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 04`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-038`](./14-project-milestones.md#milestone-038) and deployment gate [`RELEASE-013`](./15-release-strategy.md#release-013).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-038`](./12-project-risks.md#risk-038).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-038`](./10-project-assumptions.md#assumption-038).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-038`](./11-project-constraints.md#constraint-038).
- **Pre-Approved Architectural & Operational Fallback:** Enable electronic ordering only for confirmed available tests.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.39 DEPENDENCY-039: Municipal Clinic Staffing Roster & Employee IDs #39
- **Dependency Identifier:** `DEPENDENCY-039` — **Municipal Clinic Staffing Roster & Employee IDs #39**
- **Functional Category:** `Operational` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP Admin providing verified employee numbers and phone numbers for all 750+ staff.
- **Provider Entity (Upstream Authority):** `BBMP Administration`
- **Consumer Entity (Downstream Squad):** `Identity & Auth Squad`
- **Accountable Delivery Steward:** [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) (Governed by [`GOV-039`](./09-governance-model.md#gov-039)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-039`](./06-stakeholders.md#stakeholder-039).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 04`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 04`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-039`](./14-project-milestones.md#milestone-039) and deployment gate [`RELEASE-014`](./15-release-strategy.md#release-014).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-039`](./12-project-risks.md#risk-039).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-039`](./10-project-assumptions.md#assumption-039).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-039`](./11-project-constraints.md#constraint-039).
- **Pre-Approved Architectural & Operational Fallback:** Generate provisional local clinic accounts validated by doctor.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.40 DEPENDENCY-040: Zonal Clinic Pilot Site Selection (20 Clinics) #40
- **Dependency Identifier:** `DEPENDENCY-040` — **Zonal Clinic Pilot Site Selection (20 Clinics) #40**
- **Functional Category:** `Operational` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Steering committee designating exactly 20 clinics across East and West zones for pilot.
- **Provider Entity (Upstream Authority):** `Project Steering Committee`
- **Consumer Entity (Downstream Squad):** `Deployment Squad`
- **Accountable Delivery Steward:** [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) (Governed by [`GOV-040`](./09-governance-model.md#gov-040)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-040`](./06-stakeholders.md#stakeholder-040).
- **Execution Preconditions (Start Condition):** `Sprint 06`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 08`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 08`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-040`](./14-project-milestones.md#milestone-040) and deployment gate [`RELEASE-015`](./15-release-strategy.md#release-015).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-040`](./12-project-risks.md#risk-040).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-040`](./10-project-assumptions.md#assumption-040).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-040`](./11-project-constraints.md#constraint-040).
- **Pre-Approved Architectural & Operational Fallback:** Select top 20 clinics based on discovery audit infrastructure.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.41 DEPENDENCY-041: MeghRaj Sovereign Cloud Virtual Machine Allocation #41
- **Dependency Identifier:** `DEPENDENCY-041` — **MeghRaj Sovereign Cloud Virtual Machine Allocation #41**
- **Functional Category:** `Infrastructure` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** NIC provisioning primary Kubernetes compute cluster and managed PostgreSQL instance.
- **Provider Entity (Upstream Authority):** `NIC Cloud Team`
- **Consumer Entity (Downstream Squad):** `DevOps & SRE Squad`
- **Accountable Delivery Steward:** [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) (Governed by [`GOV-041`](./09-governance-model.md#gov-041)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-041`](./06-stakeholders.md#stakeholder-041).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 03`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 03`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-001`](./14-project-milestones.md#milestone-001) and deployment gate [`RELEASE-016`](./15-release-strategy.md#release-016).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-041`](./12-project-risks.md#risk-041).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-041`](./10-project-assumptions.md#assumption-041).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-041`](./11-project-constraints.md#constraint-041).
- **Pre-Approved Architectural & Operational Fallback:** Host initial environments on AWS Mumbai cloud infrastructure.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.42 DEPENDENCY-042: AWS Mumbai Secondary Availability Zone Hosting #42
- **Dependency Identifier:** `DEPENDENCY-042` — **AWS Mumbai Secondary Availability Zone Hosting #42**
- **Functional Category:** `Infrastructure` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** AWS consortium account configuration with VPC peering and KMS encryption keys.
- **Provider Entity (Upstream Authority):** `Consortium DevOps Lead`
- **Consumer Entity (Downstream Squad):** `DevOps & SRE Squad`
- **Accountable Delivery Steward:** [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) (Governed by [`GOV-042`](./09-governance-model.md#gov-042)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-042`](./06-stakeholders.md#stakeholder-042).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 02`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 02`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-002`](./14-project-milestones.md#milestone-002) and deployment gate [`RELEASE-017`](./15-release-strategy.md#release-017).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-042`](./12-project-risks.md#risk-042).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-042`](./10-project-assumptions.md#assumption-042).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-042`](./11-project-constraints.md#constraint-042).
- **Pre-Approved Architectural & Operational Fallback:** Operate single-region deployment during development sprints.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.43 DEPENDENCY-043: Independent CERT-In Empaneled VAPT Audit Clearance #43
- **Dependency Identifier:** `DEPENDENCY-043` — **Independent CERT-In Empaneled VAPT Audit Clearance #43**
- **Functional Category:** `Security` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Independent cybersecurity auditor completing penetration testing and issuing certificate.
- **Provider Entity (Upstream Authority):** `CERT-In Empaneled Auditor`
- **Consumer Entity (Downstream Squad):** `Security Squad`
- **Accountable Delivery Steward:** [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) (Governed by [`GOV-043`](./09-governance-model.md#gov-043)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-043`](./06-stakeholders.md#stakeholder-043).
- **Execution Preconditions (Start Condition):** `Sprint 14`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 16`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 16`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-003`](./14-project-milestones.md#milestone-003) and deployment gate [`RELEASE-018`](./15-release-strategy.md#release-018).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-043`](./12-project-risks.md#risk-043).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-043`](./10-project-assumptions.md#assumption-043).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-043`](./11-project-constraints.md#constraint-043).
- **Pre-Approved Architectural & Operational Fallback:** Remediate high findings within 48h emergency sprint window.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.44 DEPENDENCY-044: DPDP Act 2023 Consent Workflow Legal Clearance #44
- **Dependency Identifier:** `DEPENDENCY-044` — **DPDP Act 2023 Consent Workflow Legal Clearance #44**
- **Functional Category:** `Legal` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP Legal Cell formal written approval of digital patient consent capture mechanism.
- **Provider Entity (Upstream Authority):** `BBMP Legal Cell`
- **Consumer Entity (Downstream Squad):** `Security Squad`
- **Accountable Delivery Steward:** [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) (Governed by [`GOV-044`](./09-governance-model.md#gov-044)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-044`](./06-stakeholders.md#stakeholder-044).
- **Execution Preconditions (Start Condition):** `Sprint 08`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-004`](./14-project-milestones.md#milestone-004) and deployment gate [`RELEASE-019`](./15-release-strategy.md#release-019).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-044`](./12-project-risks.md#risk-044).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-044`](./10-project-assumptions.md#assumption-044).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-044`](./11-project-constraints.md#constraint-044).
- **Pre-Approved Architectural & Operational Fallback:** Proceed with conservative explicit opt-in checkbox model.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.45 DEPENDENCY-045: Bilingual Frontline Training Facility Procurement #45
- **Dependency Identifier:** `DEPENDENCY-045` — **Bilingual Frontline Training Facility Procurement #45**
- **Functional Category:** `Operations` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP providing 8 zonal training halls equipped with demo PCs for hands-on labs.
- **Provider Entity (Upstream Authority):** `BBMP Zonal Health Officers`
- **Consumer Entity (Downstream Squad):** `Training Squad`
- **Accountable Delivery Steward:** [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) (Governed by [`GOV-045`](./09-governance-model.md#gov-045)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-045`](./06-stakeholders.md#stakeholder-045).
- **Execution Preconditions (Start Condition):** `Sprint 08`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-005`](./14-project-milestones.md#milestone-005) and deployment gate [`RELEASE-020`](./15-release-strategy.md#release-020).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-045`](./12-project-risks.md#risk-045).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-045`](./10-project-assumptions.md#assumption-045).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-045`](./11-project-constraints.md#constraint-045).
- **Pre-Approved Architectural & Operational Fallback:** Conduct mobile on-site training sessions inside clinic facilities.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.46 DEPENDENCY-046: Hardware Mini-PC Procurement & Staging #46
- **Dependency Identifier:** `DEPENDENCY-046` — **Hardware Mini-PC Procurement & Staging #46**
- **Functional Category:** `Hardware` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP IT Cell must procure, image, and deliver 183 mini-PCs to clinic sites.
- **Provider Entity (Upstream Authority):** `BBMP IT Cell`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) (Governed by [`GOV-001`](./09-governance-model.md#gov-001)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-046`](./06-stakeholders.md#stakeholder-046).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-006`](./14-project-milestones.md#milestone-006) and deployment gate [`RELEASE-021`](./15-release-strategy.md#release-021).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-046`](./12-project-risks.md#risk-046).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-046`](./10-project-assumptions.md#assumption-046).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-046`](./11-project-constraints.md#constraint-046).
- **Pre-Approved Architectural & Operational Fallback:** Procure refurbished terminals as temporary pilot buffer.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.47 DEPENDENCY-047: 1000VA UPS Battery Installation at Clinic Sites #47
- **Dependency Identifier:** `DEPENDENCY-047` — **1000VA UPS Battery Installation at Clinic Sites #47**
- **Functional Category:** `Hardware` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Installation of calibrated UPS power units with dedicated earthing in all clinics.
- **Provider Entity (Upstream Authority):** `BBMP Electrical Wing`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) (Governed by [`GOV-002`](./09-governance-model.md#gov-002)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-047`](./06-stakeholders.md#stakeholder-047).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-007`](./14-project-milestones.md#milestone-007) and deployment gate [`RELEASE-022`](./15-release-strategy.md#release-022).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-047`](./12-project-risks.md#risk-047).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-047`](./10-project-assumptions.md#assumption-047).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-047`](./11-project-constraints.md#constraint-047).
- **Pre-Approved Architectural & Operational Fallback:** Deploy surge protector strips with portable battery packs.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.48 DEPENDENCY-048: Dual-SIM LTE Dongle & Static IP Provisioning #48
- **Dependency Identifier:** `DEPENDENCY-048` — **Dual-SIM LTE Dongle & Static IP Provisioning #48**
- **Functional Category:** `Network` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Procurement and static IP assignment for Airtel and Jio SIM cards across 183 clinics.
- **Provider Entity (Upstream Authority):** `BBMP IT / Telecom Vendors`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) (Governed by [`GOV-003`](./09-governance-model.md#gov-003)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-048`](./06-stakeholders.md#stakeholder-048).
- **Execution Preconditions (Start Condition):** `Sprint 03`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-008`](./14-project-milestones.md#milestone-008) and deployment gate [`RELEASE-023`](./15-release-strategy.md#release-023).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-048`](./12-project-risks.md#risk-048).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-048`](./10-project-assumptions.md#assumption-048).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-048`](./11-project-constraints.md#constraint-048).
- **Pre-Approved Architectural & Operational Fallback:** Use dynamic DNS over standard broadband tethering.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.49 DEPENDENCY-049: NHA ABDM Sandbox Gateway Credentials #49
- **Dependency Identifier:** `DEPENDENCY-049` — **NHA ABDM Sandbox Gateway Credentials #49**
- **Functional Category:** `Regulatory` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** National Health Authority issuing production API client keys for M1/M2/M3 gateways.
- **Provider Entity (Upstream Authority):** `National Health Authority`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) (Governed by [`GOV-004`](./09-governance-model.md#gov-004)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-049`](./06-stakeholders.md#stakeholder-049).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 06`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 06`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-009`](./14-project-milestones.md#milestone-009) and deployment gate [`RELEASE-024`](./15-release-strategy.md#release-024).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-049`](./12-project-risks.md#risk-049).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-049`](./10-project-assumptions.md#assumption-049).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-049`](./11-project-constraints.md#constraint-049).
- **Pre-Approved Architectural & Operational Fallback:** Utilize ABDM mock sandbox server in local Docker container.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.50 DEPENDENCY-050: Karnataka State HMIS Daily XML Endpoint Schema #50
- **Dependency Identifier:** `DEPENDENCY-050` — **Karnataka State HMIS Daily XML Endpoint Schema #50**
- **Functional Category:** `Compliance` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** State DHS delivering finalized XML and JSON schema definitions for daily uploads.
- **Provider Entity (Upstream Authority):** `Karnataka State DHS`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) (Governed by [`GOV-005`](./09-governance-model.md#gov-005)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-050`](./06-stakeholders.md#stakeholder-050).
- **Execution Preconditions (Start Condition):** `Sprint 03`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 08`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 08`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-010`](./14-project-milestones.md#milestone-010) and deployment gate [`RELEASE-025`](./15-release-strategy.md#release-025).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-050`](./12-project-risks.md#risk-050).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-050`](./10-project-assumptions.md#assumption-050).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-050`](./11-project-constraints.md#constraint-050).
- **Pre-Approved Architectural & Operational Fallback:** Generate standardized interim CSV export for manual upload.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.51 DEPENDENCY-051: CDAC Mobile Seva SMS DLT Template Registration #51
- **Dependency Identifier:** `DEPENDENCY-051` — **CDAC Mobile Seva SMS DLT Template Registration #51**
- **Functional Category:** `Telecom` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** TRAI portal approval of Kannada and English transactional SMS prescription templates.
- **Provider Entity (Upstream Authority):** `CDAC / TRAI`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) (Governed by [`GOV-006`](./09-governance-model.md#gov-006)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-001`](./06-stakeholders.md#stakeholder-001).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 05`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 05`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-011`](./14-project-milestones.md#milestone-011) and deployment gate [`RELEASE-001`](./15-release-strategy.md#release-001).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-051`](./12-project-risks.md#risk-051).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-001`](./10-project-assumptions.md#assumption-001).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-001`](./11-project-constraints.md#constraint-001).
- **Pre-Approved Architectural & Operational Fallback:** Direct patient to display on-screen QR code for camera capture.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.52 DEPENDENCY-052: Karnataka State EDL Formulary Official Sign-Off #52
- **Dependency Identifier:** `DEPENDENCY-052` — **Karnataka State EDL Formulary Official Sign-Off #52**
- **Functional Category:** `Clinical` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Chief Health Officer signing off on canonical 120-drug Karnataka EDL master formulary.
- **Provider Entity (Upstream Authority):** `Chief Health Officer`
- **Consumer Entity (Downstream Squad):** `Clinical Squad`
- **Accountable Delivery Steward:** [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) (Governed by [`GOV-007`](./09-governance-model.md#gov-007)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-002`](./06-stakeholders.md#stakeholder-002).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 02`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 02`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-012`](./14-project-milestones.md#milestone-012) and deployment gate [`RELEASE-002`](./15-release-strategy.md#release-002).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-052`](./12-project-risks.md#risk-052).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-002`](./10-project-assumptions.md#assumption-002).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-002`](./11-project-constraints.md#constraint-002).
- **Pre-Approved Architectural & Operational Fallback:** Base EMR formulary on draft 2024 DHS Essential Drug List.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.53 DEPENDENCY-053: Point-of-Care Laboratory 14-Test Kit Validation #53
- **Dependency Identifier:** `DEPENDENCY-053` — **Point-of-Care Laboratory 14-Test Kit Validation #53**
- **Functional Category:** `Clinical` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Clinical validation of diagnostic test list against available clinic rapid test reagents.
- **Provider Entity (Upstream Authority):** `Chief Health Officer`
- **Consumer Entity (Downstream Squad):** `Clinical Squad`
- **Accountable Delivery Steward:** [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) (Governed by [`GOV-008`](./09-governance-model.md#gov-008)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-003`](./06-stakeholders.md#stakeholder-003).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 04`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 04`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-013`](./14-project-milestones.md#milestone-013) and deployment gate [`RELEASE-003`](./15-release-strategy.md#release-003).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-053`](./12-project-risks.md#risk-053).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-003`](./10-project-assumptions.md#assumption-003).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-003`](./11-project-constraints.md#constraint-003).
- **Pre-Approved Architectural & Operational Fallback:** Enable electronic ordering only for confirmed available tests.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.54 DEPENDENCY-054: Municipal Clinic Staffing Roster & Employee IDs #54
- **Dependency Identifier:** `DEPENDENCY-054` — **Municipal Clinic Staffing Roster & Employee IDs #54**
- **Functional Category:** `Operational` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP Admin providing verified employee numbers and phone numbers for all 750+ staff.
- **Provider Entity (Upstream Authority):** `BBMP Administration`
- **Consumer Entity (Downstream Squad):** `Identity & Auth Squad`
- **Accountable Delivery Steward:** [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) (Governed by [`GOV-009`](./09-governance-model.md#gov-009)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-004`](./06-stakeholders.md#stakeholder-004).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 04`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 04`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-014`](./14-project-milestones.md#milestone-014) and deployment gate [`RELEASE-004`](./15-release-strategy.md#release-004).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-054`](./12-project-risks.md#risk-054).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-004`](./10-project-assumptions.md#assumption-004).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-004`](./11-project-constraints.md#constraint-004).
- **Pre-Approved Architectural & Operational Fallback:** Generate provisional local clinic accounts validated by doctor.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.55 DEPENDENCY-055: Zonal Clinic Pilot Site Selection (20 Clinics) #55
- **Dependency Identifier:** `DEPENDENCY-055` — **Zonal Clinic Pilot Site Selection (20 Clinics) #55**
- **Functional Category:** `Operational` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Steering committee designating exactly 20 clinics across East and West zones for pilot.
- **Provider Entity (Upstream Authority):** `Project Steering Committee`
- **Consumer Entity (Downstream Squad):** `Deployment Squad`
- **Accountable Delivery Steward:** [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) (Governed by [`GOV-010`](./09-governance-model.md#gov-010)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-005`](./06-stakeholders.md#stakeholder-005).
- **Execution Preconditions (Start Condition):** `Sprint 06`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 08`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 08`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-015`](./14-project-milestones.md#milestone-015) and deployment gate [`RELEASE-005`](./15-release-strategy.md#release-005).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-055`](./12-project-risks.md#risk-055).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-005`](./10-project-assumptions.md#assumption-005).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-005`](./11-project-constraints.md#constraint-005).
- **Pre-Approved Architectural & Operational Fallback:** Select top 20 clinics based on discovery audit infrastructure.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.56 DEPENDENCY-056: MeghRaj Sovereign Cloud Virtual Machine Allocation #56
- **Dependency Identifier:** `DEPENDENCY-056` — **MeghRaj Sovereign Cloud Virtual Machine Allocation #56**
- **Functional Category:** `Infrastructure` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** NIC provisioning primary Kubernetes compute cluster and managed PostgreSQL instance.
- **Provider Entity (Upstream Authority):** `NIC Cloud Team`
- **Consumer Entity (Downstream Squad):** `DevOps & SRE Squad`
- **Accountable Delivery Steward:** [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) (Governed by [`GOV-011`](./09-governance-model.md#gov-011)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-006`](./06-stakeholders.md#stakeholder-006).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 03`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 03`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-016`](./14-project-milestones.md#milestone-016) and deployment gate [`RELEASE-006`](./15-release-strategy.md#release-006).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-056`](./12-project-risks.md#risk-056).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-006`](./10-project-assumptions.md#assumption-006).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-006`](./11-project-constraints.md#constraint-006).
- **Pre-Approved Architectural & Operational Fallback:** Host initial environments on AWS Mumbai cloud infrastructure.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.57 DEPENDENCY-057: AWS Mumbai Secondary Availability Zone Hosting #57
- **Dependency Identifier:** `DEPENDENCY-057` — **AWS Mumbai Secondary Availability Zone Hosting #57**
- **Functional Category:** `Infrastructure` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** AWS consortium account configuration with VPC peering and KMS encryption keys.
- **Provider Entity (Upstream Authority):** `Consortium DevOps Lead`
- **Consumer Entity (Downstream Squad):** `DevOps & SRE Squad`
- **Accountable Delivery Steward:** [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) (Governed by [`GOV-012`](./09-governance-model.md#gov-012)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-007`](./06-stakeholders.md#stakeholder-007).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 02`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 02`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-017`](./14-project-milestones.md#milestone-017) and deployment gate [`RELEASE-007`](./15-release-strategy.md#release-007).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-057`](./12-project-risks.md#risk-057).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-007`](./10-project-assumptions.md#assumption-007).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-007`](./11-project-constraints.md#constraint-007).
- **Pre-Approved Architectural & Operational Fallback:** Operate single-region deployment during development sprints.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.58 DEPENDENCY-058: Independent CERT-In Empaneled VAPT Audit Clearance #58
- **Dependency Identifier:** `DEPENDENCY-058` — **Independent CERT-In Empaneled VAPT Audit Clearance #58**
- **Functional Category:** `Security` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Independent cybersecurity auditor completing penetration testing and issuing certificate.
- **Provider Entity (Upstream Authority):** `CERT-In Empaneled Auditor`
- **Consumer Entity (Downstream Squad):** `Security Squad`
- **Accountable Delivery Steward:** [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) (Governed by [`GOV-013`](./09-governance-model.md#gov-013)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-008`](./06-stakeholders.md#stakeholder-008).
- **Execution Preconditions (Start Condition):** `Sprint 14`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 16`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 16`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-018`](./14-project-milestones.md#milestone-018) and deployment gate [`RELEASE-008`](./15-release-strategy.md#release-008).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-058`](./12-project-risks.md#risk-058).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-008`](./10-project-assumptions.md#assumption-008).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-008`](./11-project-constraints.md#constraint-008).
- **Pre-Approved Architectural & Operational Fallback:** Remediate high findings within 48h emergency sprint window.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.59 DEPENDENCY-059: DPDP Act 2023 Consent Workflow Legal Clearance #59
- **Dependency Identifier:** `DEPENDENCY-059` — **DPDP Act 2023 Consent Workflow Legal Clearance #59**
- **Functional Category:** `Legal` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP Legal Cell formal written approval of digital patient consent capture mechanism.
- **Provider Entity (Upstream Authority):** `BBMP Legal Cell`
- **Consumer Entity (Downstream Squad):** `Security Squad`
- **Accountable Delivery Steward:** [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) (Governed by [`GOV-014`](./09-governance-model.md#gov-014)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-009`](./06-stakeholders.md#stakeholder-009).
- **Execution Preconditions (Start Condition):** `Sprint 08`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-019`](./14-project-milestones.md#milestone-019) and deployment gate [`RELEASE-009`](./15-release-strategy.md#release-009).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-059`](./12-project-risks.md#risk-059).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-009`](./10-project-assumptions.md#assumption-009).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-009`](./11-project-constraints.md#constraint-009).
- **Pre-Approved Architectural & Operational Fallback:** Proceed with conservative explicit opt-in checkbox model.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.60 DEPENDENCY-060: Bilingual Frontline Training Facility Procurement #60
- **Dependency Identifier:** `DEPENDENCY-060` — **Bilingual Frontline Training Facility Procurement #60**
- **Functional Category:** `Operations` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP providing 8 zonal training halls equipped with demo PCs for hands-on labs.
- **Provider Entity (Upstream Authority):** `BBMP Zonal Health Officers`
- **Consumer Entity (Downstream Squad):** `Training Squad`
- **Accountable Delivery Steward:** [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) (Governed by [`GOV-015`](./09-governance-model.md#gov-015)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-010`](./06-stakeholders.md#stakeholder-010).
- **Execution Preconditions (Start Condition):** `Sprint 08`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-020`](./14-project-milestones.md#milestone-020) and deployment gate [`RELEASE-010`](./15-release-strategy.md#release-010).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-060`](./12-project-risks.md#risk-060).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-010`](./10-project-assumptions.md#assumption-010).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-010`](./11-project-constraints.md#constraint-010).
- **Pre-Approved Architectural & Operational Fallback:** Conduct mobile on-site training sessions inside clinic facilities.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.61 DEPENDENCY-061: Hardware Mini-PC Procurement & Staging #61
- **Dependency Identifier:** `DEPENDENCY-061` — **Hardware Mini-PC Procurement & Staging #61**
- **Functional Category:** `Hardware` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP IT Cell must procure, image, and deliver 183 mini-PCs to clinic sites.
- **Provider Entity (Upstream Authority):** `BBMP IT Cell`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) (Governed by [`GOV-016`](./09-governance-model.md#gov-016)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-011`](./06-stakeholders.md#stakeholder-011).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-021`](./14-project-milestones.md#milestone-021) and deployment gate [`RELEASE-011`](./15-release-strategy.md#release-011).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-061`](./12-project-risks.md#risk-061).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-011`](./10-project-assumptions.md#assumption-011).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-011`](./11-project-constraints.md#constraint-011).
- **Pre-Approved Architectural & Operational Fallback:** Procure refurbished terminals as temporary pilot buffer.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.62 DEPENDENCY-062: 1000VA UPS Battery Installation at Clinic Sites #62
- **Dependency Identifier:** `DEPENDENCY-062` — **1000VA UPS Battery Installation at Clinic Sites #62**
- **Functional Category:** `Hardware` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Installation of calibrated UPS power units with dedicated earthing in all clinics.
- **Provider Entity (Upstream Authority):** `BBMP Electrical Wing`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) (Governed by [`GOV-017`](./09-governance-model.md#gov-017)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-012`](./06-stakeholders.md#stakeholder-012).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-022`](./14-project-milestones.md#milestone-022) and deployment gate [`RELEASE-012`](./15-release-strategy.md#release-012).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-062`](./12-project-risks.md#risk-062).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-012`](./10-project-assumptions.md#assumption-012).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-012`](./11-project-constraints.md#constraint-012).
- **Pre-Approved Architectural & Operational Fallback:** Deploy surge protector strips with portable battery packs.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.63 DEPENDENCY-063: Dual-SIM LTE Dongle & Static IP Provisioning #63
- **Dependency Identifier:** `DEPENDENCY-063` — **Dual-SIM LTE Dongle & Static IP Provisioning #63**
- **Functional Category:** `Network` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Procurement and static IP assignment for Airtel and Jio SIM cards across 183 clinics.
- **Provider Entity (Upstream Authority):** `BBMP IT / Telecom Vendors`
- **Consumer Entity (Downstream Squad):** `Infrastructure Squad`
- **Accountable Delivery Steward:** [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) (Governed by [`GOV-018`](./09-governance-model.md#gov-018)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-013`](./06-stakeholders.md#stakeholder-013).
- **Execution Preconditions (Start Condition):** `Sprint 03`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-023`](./14-project-milestones.md#milestone-023) and deployment gate [`RELEASE-013`](./15-release-strategy.md#release-013).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-063`](./12-project-risks.md#risk-063).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-013`](./10-project-assumptions.md#assumption-013).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-013`](./11-project-constraints.md#constraint-013).
- **Pre-Approved Architectural & Operational Fallback:** Use dynamic DNS over standard broadband tethering.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.64 DEPENDENCY-064: NHA ABDM Sandbox Gateway Credentials #64
- **Dependency Identifier:** `DEPENDENCY-064` — **NHA ABDM Sandbox Gateway Credentials #64**
- **Functional Category:** `Regulatory` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** National Health Authority issuing production API client keys for M1/M2/M3 gateways.
- **Provider Entity (Upstream Authority):** `National Health Authority`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) (Governed by [`GOV-019`](./09-governance-model.md#gov-019)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-014`](./06-stakeholders.md#stakeholder-014).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 06`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 06`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-024`](./14-project-milestones.md#milestone-024) and deployment gate [`RELEASE-014`](./15-release-strategy.md#release-014).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-064`](./12-project-risks.md#risk-064).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-014`](./10-project-assumptions.md#assumption-014).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-014`](./11-project-constraints.md#constraint-014).
- **Pre-Approved Architectural & Operational Fallback:** Utilize ABDM mock sandbox server in local Docker container.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.65 DEPENDENCY-065: Karnataka State HMIS Daily XML Endpoint Schema #65
- **Dependency Identifier:** `DEPENDENCY-065` — **Karnataka State HMIS Daily XML Endpoint Schema #65**
- **Functional Category:** `Compliance` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** State DHS delivering finalized XML and JSON schema definitions for daily uploads.
- **Provider Entity (Upstream Authority):** `Karnataka State DHS`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) (Governed by [`GOV-020`](./09-governance-model.md#gov-020)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-015`](./06-stakeholders.md#stakeholder-015).
- **Execution Preconditions (Start Condition):** `Sprint 03`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 08`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 08`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-025`](./14-project-milestones.md#milestone-025) and deployment gate [`RELEASE-015`](./15-release-strategy.md#release-015).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-065`](./12-project-risks.md#risk-065).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-015`](./10-project-assumptions.md#assumption-015).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-015`](./11-project-constraints.md#constraint-015).
- **Pre-Approved Architectural & Operational Fallback:** Generate standardized interim CSV export for manual upload.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.66 DEPENDENCY-066: CDAC Mobile Seva SMS DLT Template Registration #66
- **Dependency Identifier:** `DEPENDENCY-066` — **CDAC Mobile Seva SMS DLT Template Registration #66**
- **Functional Category:** `Telecom` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** TRAI portal approval of Kannada and English transactional SMS prescription templates.
- **Provider Entity (Upstream Authority):** `CDAC / TRAI`
- **Consumer Entity (Downstream Squad):** `Integrations Squad`
- **Accountable Delivery Steward:** [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) (Governed by [`GOV-021`](./09-governance-model.md#gov-021)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-016`](./06-stakeholders.md#stakeholder-016).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 05`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 05`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-026`](./14-project-milestones.md#milestone-026) and deployment gate [`RELEASE-016`](./15-release-strategy.md#release-016).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-066`](./12-project-risks.md#risk-066).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-016`](./10-project-assumptions.md#assumption-016).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-016`](./11-project-constraints.md#constraint-016).
- **Pre-Approved Architectural & Operational Fallback:** Direct patient to display on-screen QR code for camera capture.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.67 DEPENDENCY-067: Karnataka State EDL Formulary Official Sign-Off #67
- **Dependency Identifier:** `DEPENDENCY-067` — **Karnataka State EDL Formulary Official Sign-Off #67**
- **Functional Category:** `Clinical` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Chief Health Officer signing off on canonical 120-drug Karnataka EDL master formulary.
- **Provider Entity (Upstream Authority):** `Chief Health Officer`
- **Consumer Entity (Downstream Squad):** `Clinical Squad`
- **Accountable Delivery Steward:** [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) (Governed by [`GOV-022`](./09-governance-model.md#gov-022)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-017`](./06-stakeholders.md#stakeholder-017).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 02`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 02`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-027`](./14-project-milestones.md#milestone-027) and deployment gate [`RELEASE-017`](./15-release-strategy.md#release-017).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-067`](./12-project-risks.md#risk-067).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-017`](./10-project-assumptions.md#assumption-017).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-017`](./11-project-constraints.md#constraint-017).
- **Pre-Approved Architectural & Operational Fallback:** Base EMR formulary on draft 2024 DHS Essential Drug List.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.68 DEPENDENCY-068: Point-of-Care Laboratory 14-Test Kit Validation #68
- **Dependency Identifier:** `DEPENDENCY-068` — **Point-of-Care Laboratory 14-Test Kit Validation #68**
- **Functional Category:** `Clinical` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Clinical validation of diagnostic test list against available clinic rapid test reagents.
- **Provider Entity (Upstream Authority):** `Chief Health Officer`
- **Consumer Entity (Downstream Squad):** `Clinical Squad`
- **Accountable Delivery Steward:** [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) (Governed by [`GOV-023`](./09-governance-model.md#gov-023)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-018`](./06-stakeholders.md#stakeholder-018).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 04`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 04`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-028`](./14-project-milestones.md#milestone-028) and deployment gate [`RELEASE-018`](./15-release-strategy.md#release-018).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-068`](./12-project-risks.md#risk-068).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-018`](./10-project-assumptions.md#assumption-018).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-018`](./11-project-constraints.md#constraint-018).
- **Pre-Approved Architectural & Operational Fallback:** Enable electronic ordering only for confirmed available tests.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.69 DEPENDENCY-069: Municipal Clinic Staffing Roster & Employee IDs #69
- **Dependency Identifier:** `DEPENDENCY-069` — **Municipal Clinic Staffing Roster & Employee IDs #69**
- **Functional Category:** `Operational` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP Admin providing verified employee numbers and phone numbers for all 750+ staff.
- **Provider Entity (Upstream Authority):** `BBMP Administration`
- **Consumer Entity (Downstream Squad):** `Identity & Auth Squad`
- **Accountable Delivery Steward:** [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) (Governed by [`GOV-024`](./09-governance-model.md#gov-024)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-019`](./06-stakeholders.md#stakeholder-019).
- **Execution Preconditions (Start Condition):** `Sprint 02`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 04`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 04`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-029`](./14-project-milestones.md#milestone-029) and deployment gate [`RELEASE-019`](./15-release-strategy.md#release-019).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-069`](./12-project-risks.md#risk-069).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-019`](./10-project-assumptions.md#assumption-019).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-019`](./11-project-constraints.md#constraint-019).
- **Pre-Approved Architectural & Operational Fallback:** Generate provisional local clinic accounts validated by doctor.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.70 DEPENDENCY-070: Zonal Clinic Pilot Site Selection (20 Clinics) #70
- **Dependency Identifier:** `DEPENDENCY-070` — **Zonal Clinic Pilot Site Selection (20 Clinics) #70**
- **Functional Category:** `Operational` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Steering committee designating exactly 20 clinics across East and West zones for pilot.
- **Provider Entity (Upstream Authority):** `Project Steering Committee`
- **Consumer Entity (Downstream Squad):** `Deployment Squad`
- **Accountable Delivery Steward:** [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) (Governed by [`GOV-025`](./09-governance-model.md#gov-025)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-020`](./06-stakeholders.md#stakeholder-020).
- **Execution Preconditions (Start Condition):** `Sprint 06`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 08`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 08`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-030`](./14-project-milestones.md#milestone-030) and deployment gate [`RELEASE-020`](./15-release-strategy.md#release-020).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-070`](./12-project-risks.md#risk-070).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-020`](./10-project-assumptions.md#assumption-020).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-020`](./11-project-constraints.md#constraint-020).
- **Pre-Approved Architectural & Operational Fallback:** Select top 20 clinics based on discovery audit infrastructure.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.71 DEPENDENCY-071: MeghRaj Sovereign Cloud Virtual Machine Allocation #71
- **Dependency Identifier:** `DEPENDENCY-071` — **MeghRaj Sovereign Cloud Virtual Machine Allocation #71**
- **Functional Category:** `Infrastructure` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** NIC provisioning primary Kubernetes compute cluster and managed PostgreSQL instance.
- **Provider Entity (Upstream Authority):** `NIC Cloud Team`
- **Consumer Entity (Downstream Squad):** `DevOps & SRE Squad`
- **Accountable Delivery Steward:** [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) (Governed by [`GOV-026`](./09-governance-model.md#gov-026)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-021`](./06-stakeholders.md#stakeholder-021).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 03`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 03`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-031`](./14-project-milestones.md#milestone-031) and deployment gate [`RELEASE-021`](./15-release-strategy.md#release-021).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-071`](./12-project-risks.md#risk-071).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-021`](./10-project-assumptions.md#assumption-021).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-021`](./11-project-constraints.md#constraint-021).
- **Pre-Approved Architectural & Operational Fallback:** Host initial environments on AWS Mumbai cloud infrastructure.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.72 DEPENDENCY-072: AWS Mumbai Secondary Availability Zone Hosting #72
- **Dependency Identifier:** `DEPENDENCY-072` — **AWS Mumbai Secondary Availability Zone Hosting #72**
- **Functional Category:** `Infrastructure` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** AWS consortium account configuration with VPC peering and KMS encryption keys.
- **Provider Entity (Upstream Authority):** `Consortium DevOps Lead`
- **Consumer Entity (Downstream Squad):** `DevOps & SRE Squad`
- **Accountable Delivery Steward:** [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) (Governed by [`GOV-027`](./09-governance-model.md#gov-027)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-022`](./06-stakeholders.md#stakeholder-022).
- **Execution Preconditions (Start Condition):** `Sprint 01`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 02`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 02`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-032`](./14-project-milestones.md#milestone-032) and deployment gate [`RELEASE-022`](./15-release-strategy.md#release-022).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-072`](./12-project-risks.md#risk-072).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-022`](./10-project-assumptions.md#assumption-022).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-022`](./11-project-constraints.md#constraint-022).
- **Pre-Approved Architectural & Operational Fallback:** Operate single-region deployment during development sprints.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.73 DEPENDENCY-073: Independent CERT-In Empaneled VAPT Audit Clearance #73
- **Dependency Identifier:** `DEPENDENCY-073` — **Independent CERT-In Empaneled VAPT Audit Clearance #73**
- **Functional Category:** `Security` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** Independent cybersecurity auditor completing penetration testing and issuing certificate.
- **Provider Entity (Upstream Authority):** `CERT-In Empaneled Auditor`
- **Consumer Entity (Downstream Squad):** `Security Squad`
- **Accountable Delivery Steward:** [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) (Governed by [`GOV-028`](./09-governance-model.md#gov-028)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-023`](./06-stakeholders.md#stakeholder-023).
- **Execution Preconditions (Start Condition):** `Sprint 14`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 16`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 16`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `CRITICAL BLOCKER`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-033`](./14-project-milestones.md#milestone-033) and deployment gate [`RELEASE-023`](./15-release-strategy.md#release-023).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-073`](./12-project-risks.md#risk-073).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-023`](./10-project-assumptions.md#assumption-023).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-023`](./11-project-constraints.md#constraint-023).
- **Pre-Approved Architectural & Operational Fallback:** Remediate high findings within 48h emergency sprint window.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.74 DEPENDENCY-074: DPDP Act 2023 Consent Workflow Legal Clearance #74
- **Dependency Identifier:** `DEPENDENCY-074` — **DPDP Act 2023 Consent Workflow Legal Clearance #74**
- **Functional Category:** `Legal` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP Legal Cell formal written approval of digital patient consent capture mechanism.
- **Provider Entity (Upstream Authority):** `BBMP Legal Cell`
- **Consumer Entity (Downstream Squad):** `Security Squad`
- **Accountable Delivery Steward:** [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) (Governed by [`GOV-029`](./09-governance-model.md#gov-029)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-024`](./06-stakeholders.md#stakeholder-024).
- **Execution Preconditions (Start Condition):** `Sprint 08`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `HIGH` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-034`](./14-project-milestones.md#milestone-034) and deployment gate [`RELEASE-024`](./15-release-strategy.md#release-024).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-074`](./12-project-risks.md#risk-074).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-024`](./10-project-assumptions.md#assumption-024).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-024`](./11-project-constraints.md#constraint-024).
- **Pre-Approved Architectural & Operational Fallback:** Proceed with conservative explicit opt-in checkbox model.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

### 4.75 DEPENDENCY-075: Bilingual Frontline Training Facility Procurement #75
- **Dependency Identifier:** `DEPENDENCY-075` — **Bilingual Frontline Training Facility Procurement #75**
- **Functional Category:** `Operations` | **Relationship Type:** `Finish-to-Start (FS)`
- **Boundary Nature:** Detailed inter-agency or cross-squad handoff essential for platform continuity.
- **Authoritative Description:** BBMP providing 8 zonal training halls equipped with demo PCs for hands-on labs.
- **Provider Entity (Upstream Authority):** `BBMP Zonal Health Officers`
- **Consumer Entity (Downstream Squad):** `Training Squad`
- **Accountable Delivery Steward:** [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) (Governed by [`GOV-030`](./09-governance-model.md#gov-030)).
- **Impacted Stakeholder Authority:** Directly interfaces with [`STAKEHOLDER-025`](./06-stakeholders.md#stakeholder-025).
- **Execution Preconditions (Start Condition):** `Sprint 08`.
- **Verifiable Completion Criteria (Handoff Artifact):** `Sprint 10`.
- **Interface Contract & Technical Specification:** Governed by verified OpenAPI 3.1 JSON schemas, PostgreSQL DDL migrations, or hardware RMA checklists.
- **Testing & Verification Sandbox Environment:** Verified in staging sandbox testbed before deployment to live clinic endpoints.
- **Target Schedule Due Date:** Due strictly before `Sprint 10`.
- **Criticality & Schedule Blocking Status:** Criticality: `MEDIUM` | **Blocking Status:** `Non-Blocking Buffer`.
- **Impact on Critical Path if Delayed (>1 Sprint):** Direct schedule slippage of downstream milestone [`MILESTONE-035`](./14-project-milestones.md#milestone-035) and deployment gate [`RELEASE-025`](./15-release-strategy.md#release-025).
- **Escalation Turnaround SLA if Blocked:** Blocked condition triggers immediate PMO triage with an escalation turnaround time of `<4 Hours`.
- **Coupled Monitored Risk:** Shields the platform against risk [`RISK-075`](./12-project-risks.md#risk-075).
- **Coupled Project Assumption:** Validates underlying premise [`ASSUMPTION-025`](./10-project-assumptions.md#assumption-025).
- **Governing Boundary Constraint:** Operates under constraint [`CONSTRAINT-025`](./11-project-constraints.md#constraint-025).
- **Pre-Approved Architectural & Operational Fallback:** Conduct mobile on-site training sessions inside clinic facilities.
- **Escalation Contingency Trigger:** Escalate to Project Steering Committee within 24 hours.
- **Post-Handoff Monitoring Period & Stability Gate:** 48-hour burn-in period required before formal sign-off in sprint tracking.
- **Handoff Verification & Acceptance Gate:** Formal inspection sign-off required by Consumer Lead prior to closing dependency in sprint tracking.
- **Zonal Field Coordination Mechanism:** Zonal IT leads verify physical deployment and connectivity across 183 clinic endpoints.

## 5. External Government & Statutory Agency Dependencies
Critical external dependencies where the platform relies on central or state government nodal agencies:

| Dependency Code | External Agency | Required Interface / Approval | Potential Bottleneck | Pre-Approved Contingency Fallback |
| :--- | :--- | :--- | :--- | :--- |
| **DEP-EXT-01** | National Health Authority (NHA) | ABDM M1/M2/M3 Sandbox Certification & HFR Facility Linking | Sandbox testing queue delays | Decouple local consultation; queue ABDM record sync asynchronously |
| **DEP-EXT-02** | Unique Identification Authority (UIDAI)| Ephemeral Aadhaar Auth API access for citizen registration | Network timeouts on UIDAI cluster | Demographic mobile OTP / Ration card number check-in fallback |
| **DEP-EXT-03** | BBMP Central IT Department | Procurement & staging of 183 x86 mini-PCs & dual-SIM routers | Municipal tendering delay | Deploy pilot software to existing refurbished clinic laptops |
| **DEP-EXT-04** | BESCOM (Bangalore Electricity) | Continuous grid power supply to peripheral urban slum clinics | Load shedding >1 hour | Line-interactive 1000VA UPS with 2-hour battery holdover buffer |
| **DEP-EXT-05** | Karnataka State Drugs Logistics (KDLWS)| Timely replenishment of the 120 Karnataka Essential Drug List | Depot inventory stockouts | Automated syndromic reorder alert sent to zonal warehouse 14 days prior |
| **DEP-EXT-06** | Data Protection Board of India | Formal review of DPDP Act 2023 Digital Consent Architecture | Statutory audit backlog | Proceed under certified legal counsel opinion with strict data minimization |
| **DEP-EXT-07** | BSNL & Airtel Enterprise Telecom | Dual-carrier M2M data SIM provisioning for 183 clinics | SIM activation delays | Mobile hotspot tethering from nurse/DEO official smartphone |
| **DEP-EXT-08** | State Referral Hospitals (Victoria/Bowring)| Electronic intake of secondary care referral QR slips | Secondary hospital system downtime | Issue printed physical referral voucher with cryptographic QR code |
| **DEP-EXT-09** | BBMP Biomedical Waste Contractor | Digital manifest barcoding integration for yellow/red bags | Contractor barcode scanner delay | Manual weight logging in client PWA with tamper-evident serial numbers |
| **DEP-EXT-10** | Karnataka State Drug Control Dept | Pharmacy license endorsements for 183 dispensary counters | Administrative processing queue | Provisional municipal health commissioner operational authorization |
| **DEP-EXT-11** | Karnataka State Data Centre (KSDC) | Secure hybrid cloud interconnect and sovereign firewall rules | Datacenter port opening delays | Encrypted WireGuard VPN tunnel over standard municipal fiber links |
| **DEP-EXT-12** | NIC e-Hospital Project Team | Cross-system citizen Master Patient Index (MPI) deduplication | API rate limiting | Local deterministic hash matching on mobile number and year of birth |

## 6. Cross-Squad Internal Coordination Matrix
Handoff SLA agreements between the four core delivery squads:

| Providing Squad | Consuming Squad | Core Handoff Artifact | Delivery SLA | Verification Protocol |
| :--- | :--- | :--- | :---: | :--- |
| **Database Squad** | Backend Squad | PostgreSQL schema migrations & Prisma/Knex DDL | Sprint Day 2 | Automated migration CI test run |
| **Backend Squad** | Frontend Squad | Fastify OpenAPI 3.1 JSON contract & Mock API | Sprint Day 3 | Prism contract mock validator |
| **Frontend Squad** | QA Squad | Feature-complete Next.js PWA build on Staging | Sprint Day 7 | Automated Playwright E2E test pass |
| **QA Squad** | DevOps / SRE Squad | Certified test report with zero P0/P1 defects | Sprint Day 9 | Release gate quality sign-off |
| **DevOps Squad** | Operations Squad | Blue/Green production container deployment | Sprint Day 10 | Post-deployment smoke test suite |

## 7. Zonal Deployment Dependency Network Across 8 BBMP Zones
Physical deployment dependencies across Bangalore's municipal zones managing 183 clinics:

| Administrative Zone | Clinics | Mini-PCs Required | UPS Units | Telco 4G Routers | Primary Deployment Prerequisite | Local Zonal Sign-off Lead |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **East Zone** | `28` | `56` | `28` | `28` | Ulsoor & Halasuru clinic fiber link inspection | ZHO East (Dr. Savitha K) |
| **West Zone** | `32` | `64` | `32` | `32` | Rajajinagar closed-loop pharmacy hardware setup | ZHO West (Dr. Ramesh B) |
| **South Zone** | `30` | `60` | `30` | `30` | Jayanagar cold chain ILR telemetry logger install | ZHO South (Dr. Manjunath N) |
| **Bommanahalli Zone** | `22` | `44` | `22` | `22` | HSR Layout queue token thermal printer delivery | ZHO Bommanahalli (Dr. Deepa M) |
| **Dasarahalli Zone** | `18` | `36` | `18` | `18` | Peenya industrial power surge suppressor install | ZHO Dasarahalli (Dr. Suresh P) |
| **Mahadevapura Zone** | `24` | `48` | `24` | `24` | Whitefield dual-SIM secondary carrier validation | ZHO Mahadevapura (Dr. Anitha R) |
| **RR Nagar Zone** | `16` | `32` | `16` | `16` | Kengeri secondary hospital QR dispatch printer link | ZHO RR Nagar (Dr. Venkatesh G) |
| **Yelahanka Zone** | `13` | `26` | `13` | `13` | Yelahanka Old clinic tablet inventory audit | ZHO Yelahanka (Dr. Lakshmi T) |

### 7.1 Zonal Deployment Dependency Protocol: East Zone
- **Administrative Scope:** Covers `28 Namma Clinics` within East Zone.
- **Hardware Deliverables Required:** `56 x86 Mini-PCs`, `28 1000VA UPS units`, and `28 4G dual-SIM routers`.
- **Critical Path Prerequisite:** Ulsoor & Halasuru clinic fiber link inspection.
- **Zonal Delivery Authority:** ZHO East (Dr. Savitha K).
- **Handoff Verification SLA:** Hardware must be tested and digitally inventoried within 48 hours of site delivery.
- **Escalation Path:** Unresolved site blockers escalate directly to Operations Manager (`ROLE-016`).

### 7.2 Zonal Deployment Dependency Protocol: West Zone
- **Administrative Scope:** Covers `32 Namma Clinics` within West Zone.
- **Hardware Deliverables Required:** `64 x86 Mini-PCs`, `32 1000VA UPS units`, and `32 4G dual-SIM routers`.
- **Critical Path Prerequisite:** Rajajinagar closed-loop pharmacy hardware setup.
- **Zonal Delivery Authority:** ZHO West (Dr. Ramesh B).
- **Handoff Verification SLA:** Hardware must be tested and digitally inventoried within 48 hours of site delivery.
- **Escalation Path:** Unresolved site blockers escalate directly to Operations Manager (`ROLE-016`).

### 7.3 Zonal Deployment Dependency Protocol: South Zone
- **Administrative Scope:** Covers `30 Namma Clinics` within South Zone.
- **Hardware Deliverables Required:** `60 x86 Mini-PCs`, `30 1000VA UPS units`, and `30 4G dual-SIM routers`.
- **Critical Path Prerequisite:** Jayanagar cold chain ILR telemetry logger install.
- **Zonal Delivery Authority:** ZHO South (Dr. Manjunath N).
- **Handoff Verification SLA:** Hardware must be tested and digitally inventoried within 48 hours of site delivery.
- **Escalation Path:** Unresolved site blockers escalate directly to Operations Manager (`ROLE-016`).

### 7.4 Zonal Deployment Dependency Protocol: Bommanahalli Zone
- **Administrative Scope:** Covers `22 Namma Clinics` within Bommanahalli Zone.
- **Hardware Deliverables Required:** `44 x86 Mini-PCs`, `22 1000VA UPS units`, and `22 4G dual-SIM routers`.
- **Critical Path Prerequisite:** HSR Layout queue token thermal printer delivery.
- **Zonal Delivery Authority:** ZHO Bommanahalli (Dr. Deepa M).
- **Handoff Verification SLA:** Hardware must be tested and digitally inventoried within 48 hours of site delivery.
- **Escalation Path:** Unresolved site blockers escalate directly to Operations Manager (`ROLE-016`).

### 7.5 Zonal Deployment Dependency Protocol: Dasarahalli Zone
- **Administrative Scope:** Covers `18 Namma Clinics` within Dasarahalli Zone.
- **Hardware Deliverables Required:** `36 x86 Mini-PCs`, `18 1000VA UPS units`, and `18 4G dual-SIM routers`.
- **Critical Path Prerequisite:** Peenya industrial power surge suppressor install.
- **Zonal Delivery Authority:** ZHO Dasarahalli (Dr. Suresh P).
- **Handoff Verification SLA:** Hardware must be tested and digitally inventoried within 48 hours of site delivery.
- **Escalation Path:** Unresolved site blockers escalate directly to Operations Manager (`ROLE-016`).

### 7.6 Zonal Deployment Dependency Protocol: Mahadevapura Zone
- **Administrative Scope:** Covers `24 Namma Clinics` within Mahadevapura Zone.
- **Hardware Deliverables Required:** `48 x86 Mini-PCs`, `24 1000VA UPS units`, and `24 4G dual-SIM routers`.
- **Critical Path Prerequisite:** Whitefield dual-SIM secondary carrier validation.
- **Zonal Delivery Authority:** ZHO Mahadevapura (Dr. Anitha R).
- **Handoff Verification SLA:** Hardware must be tested and digitally inventoried within 48 hours of site delivery.
- **Escalation Path:** Unresolved site blockers escalate directly to Operations Manager (`ROLE-016`).

### 7.7 Zonal Deployment Dependency Protocol: RR Nagar Zone
- **Administrative Scope:** Covers `16 Namma Clinics` within RR Nagar Zone.
- **Hardware Deliverables Required:** `32 x86 Mini-PCs`, `16 1000VA UPS units`, and `16 4G dual-SIM routers`.
- **Critical Path Prerequisite:** Kengeri secondary hospital QR dispatch printer link.
- **Zonal Delivery Authority:** ZHO RR Nagar (Dr. Venkatesh G).
- **Handoff Verification SLA:** Hardware must be tested and digitally inventoried within 48 hours of site delivery.
- **Escalation Path:** Unresolved site blockers escalate directly to Operations Manager (`ROLE-016`).

### 7.8 Zonal Deployment Dependency Protocol: Yelahanka Zone
- **Administrative Scope:** Covers `13 Namma Clinics` within Yelahanka Zone.
- **Hardware Deliverables Required:** `26 x86 Mini-PCs`, `13 1000VA UPS units`, and `13 4G dual-SIM routers`.
- **Critical Path Prerequisite:** Yelahanka Old clinic tablet inventory audit.
- **Zonal Delivery Authority:** ZHO Yelahanka (Dr. Lakshmi T).
- **Handoff Verification SLA:** Hardware must be tested and digitally inventoried within 48 hours of site delivery.
- **Escalation Path:** Unresolved site blockers escalate directly to Operations Manager (`ROLE-016`).

## 8. Comprehensive Cross-Document Traceability Matrix
Bidirectional relational mapping linking all 75 Dependencies to Roles, Risks, Milestones, Releases, Assumptions, and Constraints:

| Dependency ID | Accountable Role | Linked Risk | Target Milestone | Software Release | Linked Assumption | Bound Constraint |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [`DEPENDENCY-001`](#dependency-001) | [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) | [`RISK-001`](./12-project-risks.md#risk-001) | [`MILESTONE-001`](./14-project-milestones.md#milestone-001) | [`RELEASE-001`](./15-release-strategy.md#release-001) | [`ASSUMPTION-001`](./10-project-assumptions.md#assumption-001) | [`CONSTRAINT-001`](./11-project-constraints.md#constraint-001) |
| [`DEPENDENCY-002`](#dependency-002) | [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) | [`RISK-002`](./12-project-risks.md#risk-002) | [`MILESTONE-002`](./14-project-milestones.md#milestone-002) | [`RELEASE-002`](./15-release-strategy.md#release-002) | [`ASSUMPTION-002`](./10-project-assumptions.md#assumption-002) | [`CONSTRAINT-002`](./11-project-constraints.md#constraint-002) |
| [`DEPENDENCY-003`](#dependency-003) | [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) | [`RISK-003`](./12-project-risks.md#risk-003) | [`MILESTONE-003`](./14-project-milestones.md#milestone-003) | [`RELEASE-003`](./15-release-strategy.md#release-003) | [`ASSUMPTION-003`](./10-project-assumptions.md#assumption-003) | [`CONSTRAINT-003`](./11-project-constraints.md#constraint-003) |
| [`DEPENDENCY-004`](#dependency-004) | [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) | [`RISK-004`](./12-project-risks.md#risk-004) | [`MILESTONE-004`](./14-project-milestones.md#milestone-004) | [`RELEASE-004`](./15-release-strategy.md#release-004) | [`ASSUMPTION-004`](./10-project-assumptions.md#assumption-004) | [`CONSTRAINT-004`](./11-project-constraints.md#constraint-004) |
| [`DEPENDENCY-005`](#dependency-005) | [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) | [`RISK-005`](./12-project-risks.md#risk-005) | [`MILESTONE-005`](./14-project-milestones.md#milestone-005) | [`RELEASE-005`](./15-release-strategy.md#release-005) | [`ASSUMPTION-005`](./10-project-assumptions.md#assumption-005) | [`CONSTRAINT-005`](./11-project-constraints.md#constraint-005) |
| [`DEPENDENCY-006`](#dependency-006) | [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) | [`RISK-006`](./12-project-risks.md#risk-006) | [`MILESTONE-006`](./14-project-milestones.md#milestone-006) | [`RELEASE-006`](./15-release-strategy.md#release-006) | [`ASSUMPTION-006`](./10-project-assumptions.md#assumption-006) | [`CONSTRAINT-006`](./11-project-constraints.md#constraint-006) |
| [`DEPENDENCY-007`](#dependency-007) | [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) | [`RISK-007`](./12-project-risks.md#risk-007) | [`MILESTONE-007`](./14-project-milestones.md#milestone-007) | [`RELEASE-007`](./15-release-strategy.md#release-007) | [`ASSUMPTION-007`](./10-project-assumptions.md#assumption-007) | [`CONSTRAINT-007`](./11-project-constraints.md#constraint-007) |
| [`DEPENDENCY-008`](#dependency-008) | [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) | [`RISK-008`](./12-project-risks.md#risk-008) | [`MILESTONE-008`](./14-project-milestones.md#milestone-008) | [`RELEASE-008`](./15-release-strategy.md#release-008) | [`ASSUMPTION-008`](./10-project-assumptions.md#assumption-008) | [`CONSTRAINT-008`](./11-project-constraints.md#constraint-008) |
| [`DEPENDENCY-009`](#dependency-009) | [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) | [`RISK-009`](./12-project-risks.md#risk-009) | [`MILESTONE-009`](./14-project-milestones.md#milestone-009) | [`RELEASE-009`](./15-release-strategy.md#release-009) | [`ASSUMPTION-009`](./10-project-assumptions.md#assumption-009) | [`CONSTRAINT-009`](./11-project-constraints.md#constraint-009) |
| [`DEPENDENCY-010`](#dependency-010) | [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) | [`RISK-010`](./12-project-risks.md#risk-010) | [`MILESTONE-010`](./14-project-milestones.md#milestone-010) | [`RELEASE-010`](./15-release-strategy.md#release-010) | [`ASSUMPTION-010`](./10-project-assumptions.md#assumption-010) | [`CONSTRAINT-010`](./11-project-constraints.md#constraint-010) |
| [`DEPENDENCY-011`](#dependency-011) | [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) | [`RISK-011`](./12-project-risks.md#risk-011) | [`MILESTONE-011`](./14-project-milestones.md#milestone-011) | [`RELEASE-011`](./15-release-strategy.md#release-011) | [`ASSUMPTION-011`](./10-project-assumptions.md#assumption-011) | [`CONSTRAINT-011`](./11-project-constraints.md#constraint-011) |
| [`DEPENDENCY-012`](#dependency-012) | [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) | [`RISK-012`](./12-project-risks.md#risk-012) | [`MILESTONE-012`](./14-project-milestones.md#milestone-012) | [`RELEASE-012`](./15-release-strategy.md#release-012) | [`ASSUMPTION-012`](./10-project-assumptions.md#assumption-012) | [`CONSTRAINT-012`](./11-project-constraints.md#constraint-012) |
| [`DEPENDENCY-013`](#dependency-013) | [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) | [`RISK-013`](./12-project-risks.md#risk-013) | [`MILESTONE-013`](./14-project-milestones.md#milestone-013) | [`RELEASE-013`](./15-release-strategy.md#release-013) | [`ASSUMPTION-013`](./10-project-assumptions.md#assumption-013) | [`CONSTRAINT-013`](./11-project-constraints.md#constraint-013) |
| [`DEPENDENCY-014`](#dependency-014) | [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) | [`RISK-014`](./12-project-risks.md#risk-014) | [`MILESTONE-014`](./14-project-milestones.md#milestone-014) | [`RELEASE-014`](./15-release-strategy.md#release-014) | [`ASSUMPTION-014`](./10-project-assumptions.md#assumption-014) | [`CONSTRAINT-014`](./11-project-constraints.md#constraint-014) |
| [`DEPENDENCY-015`](#dependency-015) | [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) | [`RISK-015`](./12-project-risks.md#risk-015) | [`MILESTONE-015`](./14-project-milestones.md#milestone-015) | [`RELEASE-015`](./15-release-strategy.md#release-015) | [`ASSUMPTION-015`](./10-project-assumptions.md#assumption-015) | [`CONSTRAINT-015`](./11-project-constraints.md#constraint-015) |
| [`DEPENDENCY-016`](#dependency-016) | [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) | [`RISK-016`](./12-project-risks.md#risk-016) | [`MILESTONE-016`](./14-project-milestones.md#milestone-016) | [`RELEASE-016`](./15-release-strategy.md#release-016) | [`ASSUMPTION-016`](./10-project-assumptions.md#assumption-016) | [`CONSTRAINT-016`](./11-project-constraints.md#constraint-016) |
| [`DEPENDENCY-017`](#dependency-017) | [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) | [`RISK-017`](./12-project-risks.md#risk-017) | [`MILESTONE-017`](./14-project-milestones.md#milestone-017) | [`RELEASE-017`](./15-release-strategy.md#release-017) | [`ASSUMPTION-017`](./10-project-assumptions.md#assumption-017) | [`CONSTRAINT-017`](./11-project-constraints.md#constraint-017) |
| [`DEPENDENCY-018`](#dependency-018) | [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) | [`RISK-018`](./12-project-risks.md#risk-018) | [`MILESTONE-018`](./14-project-milestones.md#milestone-018) | [`RELEASE-018`](./15-release-strategy.md#release-018) | [`ASSUMPTION-018`](./10-project-assumptions.md#assumption-018) | [`CONSTRAINT-018`](./11-project-constraints.md#constraint-018) |
| [`DEPENDENCY-019`](#dependency-019) | [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) | [`RISK-019`](./12-project-risks.md#risk-019) | [`MILESTONE-019`](./14-project-milestones.md#milestone-019) | [`RELEASE-019`](./15-release-strategy.md#release-019) | [`ASSUMPTION-019`](./10-project-assumptions.md#assumption-019) | [`CONSTRAINT-019`](./11-project-constraints.md#constraint-019) |
| [`DEPENDENCY-020`](#dependency-020) | [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) | [`RISK-020`](./12-project-risks.md#risk-020) | [`MILESTONE-020`](./14-project-milestones.md#milestone-020) | [`RELEASE-020`](./15-release-strategy.md#release-020) | [`ASSUMPTION-020`](./10-project-assumptions.md#assumption-020) | [`CONSTRAINT-020`](./11-project-constraints.md#constraint-020) |
| [`DEPENDENCY-021`](#dependency-021) | [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) | [`RISK-021`](./12-project-risks.md#risk-021) | [`MILESTONE-021`](./14-project-milestones.md#milestone-021) | [`RELEASE-021`](./15-release-strategy.md#release-021) | [`ASSUMPTION-021`](./10-project-assumptions.md#assumption-021) | [`CONSTRAINT-021`](./11-project-constraints.md#constraint-021) |
| [`DEPENDENCY-022`](#dependency-022) | [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) | [`RISK-022`](./12-project-risks.md#risk-022) | [`MILESTONE-022`](./14-project-milestones.md#milestone-022) | [`RELEASE-022`](./15-release-strategy.md#release-022) | [`ASSUMPTION-022`](./10-project-assumptions.md#assumption-022) | [`CONSTRAINT-022`](./11-project-constraints.md#constraint-022) |
| [`DEPENDENCY-023`](#dependency-023) | [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) | [`RISK-023`](./12-project-risks.md#risk-023) | [`MILESTONE-023`](./14-project-milestones.md#milestone-023) | [`RELEASE-023`](./15-release-strategy.md#release-023) | [`ASSUMPTION-023`](./10-project-assumptions.md#assumption-023) | [`CONSTRAINT-023`](./11-project-constraints.md#constraint-023) |
| [`DEPENDENCY-024`](#dependency-024) | [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) | [`RISK-024`](./12-project-risks.md#risk-024) | [`MILESTONE-024`](./14-project-milestones.md#milestone-024) | [`RELEASE-024`](./15-release-strategy.md#release-024) | [`ASSUMPTION-024`](./10-project-assumptions.md#assumption-024) | [`CONSTRAINT-024`](./11-project-constraints.md#constraint-024) |
| [`DEPENDENCY-025`](#dependency-025) | [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) | [`RISK-025`](./12-project-risks.md#risk-025) | [`MILESTONE-025`](./14-project-milestones.md#milestone-025) | [`RELEASE-025`](./15-release-strategy.md#release-025) | [`ASSUMPTION-025`](./10-project-assumptions.md#assumption-025) | [`CONSTRAINT-025`](./11-project-constraints.md#constraint-025) |
| [`DEPENDENCY-026`](#dependency-026) | [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) | [`RISK-026`](./12-project-risks.md#risk-026) | [`MILESTONE-026`](./14-project-milestones.md#milestone-026) | [`RELEASE-001`](./15-release-strategy.md#release-001) | [`ASSUMPTION-026`](./10-project-assumptions.md#assumption-026) | [`CONSTRAINT-026`](./11-project-constraints.md#constraint-026) |
| [`DEPENDENCY-027`](#dependency-027) | [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) | [`RISK-027`](./12-project-risks.md#risk-027) | [`MILESTONE-027`](./14-project-milestones.md#milestone-027) | [`RELEASE-002`](./15-release-strategy.md#release-002) | [`ASSUMPTION-027`](./10-project-assumptions.md#assumption-027) | [`CONSTRAINT-027`](./11-project-constraints.md#constraint-027) |
| [`DEPENDENCY-028`](#dependency-028) | [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) | [`RISK-028`](./12-project-risks.md#risk-028) | [`MILESTONE-028`](./14-project-milestones.md#milestone-028) | [`RELEASE-003`](./15-release-strategy.md#release-003) | [`ASSUMPTION-028`](./10-project-assumptions.md#assumption-028) | [`CONSTRAINT-028`](./11-project-constraints.md#constraint-028) |
| [`DEPENDENCY-029`](#dependency-029) | [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) | [`RISK-029`](./12-project-risks.md#risk-029) | [`MILESTONE-029`](./14-project-milestones.md#milestone-029) | [`RELEASE-004`](./15-release-strategy.md#release-004) | [`ASSUMPTION-029`](./10-project-assumptions.md#assumption-029) | [`CONSTRAINT-029`](./11-project-constraints.md#constraint-029) |
| [`DEPENDENCY-030`](#dependency-030) | [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) | [`RISK-030`](./12-project-risks.md#risk-030) | [`MILESTONE-030`](./14-project-milestones.md#milestone-030) | [`RELEASE-005`](./15-release-strategy.md#release-005) | [`ASSUMPTION-030`](./10-project-assumptions.md#assumption-030) | [`CONSTRAINT-030`](./11-project-constraints.md#constraint-030) |
| [`DEPENDENCY-031`](#dependency-031) | [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) | [`RISK-031`](./12-project-risks.md#risk-031) | [`MILESTONE-031`](./14-project-milestones.md#milestone-031) | [`RELEASE-006`](./15-release-strategy.md#release-006) | [`ASSUMPTION-031`](./10-project-assumptions.md#assumption-031) | [`CONSTRAINT-031`](./11-project-constraints.md#constraint-031) |
| [`DEPENDENCY-032`](#dependency-032) | [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) | [`RISK-032`](./12-project-risks.md#risk-032) | [`MILESTONE-032`](./14-project-milestones.md#milestone-032) | [`RELEASE-007`](./15-release-strategy.md#release-007) | [`ASSUMPTION-032`](./10-project-assumptions.md#assumption-032) | [`CONSTRAINT-032`](./11-project-constraints.md#constraint-032) |
| [`DEPENDENCY-033`](#dependency-033) | [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) | [`RISK-033`](./12-project-risks.md#risk-033) | [`MILESTONE-033`](./14-project-milestones.md#milestone-033) | [`RELEASE-008`](./15-release-strategy.md#release-008) | [`ASSUMPTION-033`](./10-project-assumptions.md#assumption-033) | [`CONSTRAINT-033`](./11-project-constraints.md#constraint-033) |
| [`DEPENDENCY-034`](#dependency-034) | [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) | [`RISK-034`](./12-project-risks.md#risk-034) | [`MILESTONE-034`](./14-project-milestones.md#milestone-034) | [`RELEASE-009`](./15-release-strategy.md#release-009) | [`ASSUMPTION-034`](./10-project-assumptions.md#assumption-034) | [`CONSTRAINT-034`](./11-project-constraints.md#constraint-034) |
| [`DEPENDENCY-035`](#dependency-035) | [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) | [`RISK-035`](./12-project-risks.md#risk-035) | [`MILESTONE-035`](./14-project-milestones.md#milestone-035) | [`RELEASE-010`](./15-release-strategy.md#release-010) | [`ASSUMPTION-035`](./10-project-assumptions.md#assumption-035) | [`CONSTRAINT-035`](./11-project-constraints.md#constraint-035) |
| [`DEPENDENCY-036`](#dependency-036) | [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) | [`RISK-036`](./12-project-risks.md#risk-036) | [`MILESTONE-036`](./14-project-milestones.md#milestone-036) | [`RELEASE-011`](./15-release-strategy.md#release-011) | [`ASSUMPTION-036`](./10-project-assumptions.md#assumption-036) | [`CONSTRAINT-036`](./11-project-constraints.md#constraint-036) |
| [`DEPENDENCY-037`](#dependency-037) | [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) | [`RISK-037`](./12-project-risks.md#risk-037) | [`MILESTONE-037`](./14-project-milestones.md#milestone-037) | [`RELEASE-012`](./15-release-strategy.md#release-012) | [`ASSUMPTION-037`](./10-project-assumptions.md#assumption-037) | [`CONSTRAINT-037`](./11-project-constraints.md#constraint-037) |
| [`DEPENDENCY-038`](#dependency-038) | [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) | [`RISK-038`](./12-project-risks.md#risk-038) | [`MILESTONE-038`](./14-project-milestones.md#milestone-038) | [`RELEASE-013`](./15-release-strategy.md#release-013) | [`ASSUMPTION-038`](./10-project-assumptions.md#assumption-038) | [`CONSTRAINT-038`](./11-project-constraints.md#constraint-038) |
| [`DEPENDENCY-039`](#dependency-039) | [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) | [`RISK-039`](./12-project-risks.md#risk-039) | [`MILESTONE-039`](./14-project-milestones.md#milestone-039) | [`RELEASE-014`](./15-release-strategy.md#release-014) | [`ASSUMPTION-039`](./10-project-assumptions.md#assumption-039) | [`CONSTRAINT-039`](./11-project-constraints.md#constraint-039) |
| [`DEPENDENCY-040`](#dependency-040) | [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) | [`RISK-040`](./12-project-risks.md#risk-040) | [`MILESTONE-040`](./14-project-milestones.md#milestone-040) | [`RELEASE-015`](./15-release-strategy.md#release-015) | [`ASSUMPTION-040`](./10-project-assumptions.md#assumption-040) | [`CONSTRAINT-040`](./11-project-constraints.md#constraint-040) |
| [`DEPENDENCY-041`](#dependency-041) | [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) | [`RISK-041`](./12-project-risks.md#risk-041) | [`MILESTONE-001`](./14-project-milestones.md#milestone-001) | [`RELEASE-016`](./15-release-strategy.md#release-016) | [`ASSUMPTION-041`](./10-project-assumptions.md#assumption-041) | [`CONSTRAINT-041`](./11-project-constraints.md#constraint-041) |
| [`DEPENDENCY-042`](#dependency-042) | [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) | [`RISK-042`](./12-project-risks.md#risk-042) | [`MILESTONE-002`](./14-project-milestones.md#milestone-002) | [`RELEASE-017`](./15-release-strategy.md#release-017) | [`ASSUMPTION-042`](./10-project-assumptions.md#assumption-042) | [`CONSTRAINT-042`](./11-project-constraints.md#constraint-042) |
| [`DEPENDENCY-043`](#dependency-043) | [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) | [`RISK-043`](./12-project-risks.md#risk-043) | [`MILESTONE-003`](./14-project-milestones.md#milestone-003) | [`RELEASE-018`](./15-release-strategy.md#release-018) | [`ASSUMPTION-043`](./10-project-assumptions.md#assumption-043) | [`CONSTRAINT-043`](./11-project-constraints.md#constraint-043) |
| [`DEPENDENCY-044`](#dependency-044) | [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) | [`RISK-044`](./12-project-risks.md#risk-044) | [`MILESTONE-004`](./14-project-milestones.md#milestone-004) | [`RELEASE-019`](./15-release-strategy.md#release-019) | [`ASSUMPTION-044`](./10-project-assumptions.md#assumption-044) | [`CONSTRAINT-044`](./11-project-constraints.md#constraint-044) |
| [`DEPENDENCY-045`](#dependency-045) | [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) | [`RISK-045`](./12-project-risks.md#risk-045) | [`MILESTONE-005`](./14-project-milestones.md#milestone-005) | [`RELEASE-020`](./15-release-strategy.md#release-020) | [`ASSUMPTION-045`](./10-project-assumptions.md#assumption-045) | [`CONSTRAINT-045`](./11-project-constraints.md#constraint-045) |
| [`DEPENDENCY-046`](#dependency-046) | [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) | [`RISK-046`](./12-project-risks.md#risk-046) | [`MILESTONE-006`](./14-project-milestones.md#milestone-006) | [`RELEASE-021`](./15-release-strategy.md#release-021) | [`ASSUMPTION-046`](./10-project-assumptions.md#assumption-046) | [`CONSTRAINT-046`](./11-project-constraints.md#constraint-046) |
| [`DEPENDENCY-047`](#dependency-047) | [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) | [`RISK-047`](./12-project-risks.md#risk-047) | [`MILESTONE-007`](./14-project-milestones.md#milestone-007) | [`RELEASE-022`](./15-release-strategy.md#release-022) | [`ASSUMPTION-047`](./10-project-assumptions.md#assumption-047) | [`CONSTRAINT-047`](./11-project-constraints.md#constraint-047) |
| [`DEPENDENCY-048`](#dependency-048) | [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) | [`RISK-048`](./12-project-risks.md#risk-048) | [`MILESTONE-008`](./14-project-milestones.md#milestone-008) | [`RELEASE-023`](./15-release-strategy.md#release-023) | [`ASSUMPTION-048`](./10-project-assumptions.md#assumption-048) | [`CONSTRAINT-048`](./11-project-constraints.md#constraint-048) |
| [`DEPENDENCY-049`](#dependency-049) | [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) | [`RISK-049`](./12-project-risks.md#risk-049) | [`MILESTONE-009`](./14-project-milestones.md#milestone-009) | [`RELEASE-024`](./15-release-strategy.md#release-024) | [`ASSUMPTION-049`](./10-project-assumptions.md#assumption-049) | [`CONSTRAINT-049`](./11-project-constraints.md#constraint-049) |
| [`DEPENDENCY-050`](#dependency-050) | [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) | [`RISK-050`](./12-project-risks.md#risk-050) | [`MILESTONE-010`](./14-project-milestones.md#milestone-010) | [`RELEASE-025`](./15-release-strategy.md#release-025) | [`ASSUMPTION-050`](./10-project-assumptions.md#assumption-050) | [`CONSTRAINT-050`](./11-project-constraints.md#constraint-050) |
| [`DEPENDENCY-051`](#dependency-051) | [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) | [`RISK-051`](./12-project-risks.md#risk-051) | [`MILESTONE-011`](./14-project-milestones.md#milestone-011) | [`RELEASE-001`](./15-release-strategy.md#release-001) | [`ASSUMPTION-001`](./10-project-assumptions.md#assumption-001) | [`CONSTRAINT-001`](./11-project-constraints.md#constraint-001) |
| [`DEPENDENCY-052`](#dependency-052) | [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) | [`RISK-052`](./12-project-risks.md#risk-052) | [`MILESTONE-012`](./14-project-milestones.md#milestone-012) | [`RELEASE-002`](./15-release-strategy.md#release-002) | [`ASSUMPTION-002`](./10-project-assumptions.md#assumption-002) | [`CONSTRAINT-002`](./11-project-constraints.md#constraint-002) |
| [`DEPENDENCY-053`](#dependency-053) | [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) | [`RISK-053`](./12-project-risks.md#risk-053) | [`MILESTONE-013`](./14-project-milestones.md#milestone-013) | [`RELEASE-003`](./15-release-strategy.md#release-003) | [`ASSUMPTION-003`](./10-project-assumptions.md#assumption-003) | [`CONSTRAINT-003`](./11-project-constraints.md#constraint-003) |
| [`DEPENDENCY-054`](#dependency-054) | [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) | [`RISK-054`](./12-project-risks.md#risk-054) | [`MILESTONE-014`](./14-project-milestones.md#milestone-014) | [`RELEASE-004`](./15-release-strategy.md#release-004) | [`ASSUMPTION-004`](./10-project-assumptions.md#assumption-004) | [`CONSTRAINT-004`](./11-project-constraints.md#constraint-004) |
| [`DEPENDENCY-055`](#dependency-055) | [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) | [`RISK-055`](./12-project-risks.md#risk-055) | [`MILESTONE-015`](./14-project-milestones.md#milestone-015) | [`RELEASE-005`](./15-release-strategy.md#release-005) | [`ASSUMPTION-005`](./10-project-assumptions.md#assumption-005) | [`CONSTRAINT-005`](./11-project-constraints.md#constraint-005) |
| [`DEPENDENCY-056`](#dependency-056) | [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) | [`RISK-056`](./12-project-risks.md#risk-056) | [`MILESTONE-016`](./14-project-milestones.md#milestone-016) | [`RELEASE-006`](./15-release-strategy.md#release-006) | [`ASSUMPTION-006`](./10-project-assumptions.md#assumption-006) | [`CONSTRAINT-006`](./11-project-constraints.md#constraint-006) |
| [`DEPENDENCY-057`](#dependency-057) | [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) | [`RISK-057`](./12-project-risks.md#risk-057) | [`MILESTONE-017`](./14-project-milestones.md#milestone-017) | [`RELEASE-007`](./15-release-strategy.md#release-007) | [`ASSUMPTION-007`](./10-project-assumptions.md#assumption-007) | [`CONSTRAINT-007`](./11-project-constraints.md#constraint-007) |
| [`DEPENDENCY-058`](#dependency-058) | [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) | [`RISK-058`](./12-project-risks.md#risk-058) | [`MILESTONE-018`](./14-project-milestones.md#milestone-018) | [`RELEASE-008`](./15-release-strategy.md#release-008) | [`ASSUMPTION-008`](./10-project-assumptions.md#assumption-008) | [`CONSTRAINT-008`](./11-project-constraints.md#constraint-008) |
| [`DEPENDENCY-059`](#dependency-059) | [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) | [`RISK-059`](./12-project-risks.md#risk-059) | [`MILESTONE-019`](./14-project-milestones.md#milestone-019) | [`RELEASE-009`](./15-release-strategy.md#release-009) | [`ASSUMPTION-009`](./10-project-assumptions.md#assumption-009) | [`CONSTRAINT-009`](./11-project-constraints.md#constraint-009) |
| [`DEPENDENCY-060`](#dependency-060) | [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) | [`RISK-060`](./12-project-risks.md#risk-060) | [`MILESTONE-020`](./14-project-milestones.md#milestone-020) | [`RELEASE-010`](./15-release-strategy.md#release-010) | [`ASSUMPTION-010`](./10-project-assumptions.md#assumption-010) | [`CONSTRAINT-010`](./11-project-constraints.md#constraint-010) |
| [`DEPENDENCY-061`](#dependency-061) | [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) | [`RISK-061`](./12-project-risks.md#risk-061) | [`MILESTONE-021`](./14-project-milestones.md#milestone-021) | [`RELEASE-011`](./15-release-strategy.md#release-011) | [`ASSUMPTION-011`](./10-project-assumptions.md#assumption-011) | [`CONSTRAINT-011`](./11-project-constraints.md#constraint-011) |
| [`DEPENDENCY-062`](#dependency-062) | [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) | [`RISK-062`](./12-project-risks.md#risk-062) | [`MILESTONE-022`](./14-project-milestones.md#milestone-022) | [`RELEASE-012`](./15-release-strategy.md#release-012) | [`ASSUMPTION-012`](./10-project-assumptions.md#assumption-012) | [`CONSTRAINT-012`](./11-project-constraints.md#constraint-012) |
| [`DEPENDENCY-063`](#dependency-063) | [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) | [`RISK-063`](./12-project-risks.md#risk-063) | [`MILESTONE-023`](./14-project-milestones.md#milestone-023) | [`RELEASE-013`](./15-release-strategy.md#release-013) | [`ASSUMPTION-013`](./10-project-assumptions.md#assumption-013) | [`CONSTRAINT-013`](./11-project-constraints.md#constraint-013) |
| [`DEPENDENCY-064`](#dependency-064) | [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) | [`RISK-064`](./12-project-risks.md#risk-064) | [`MILESTONE-024`](./14-project-milestones.md#milestone-024) | [`RELEASE-014`](./15-release-strategy.md#release-014) | [`ASSUMPTION-014`](./10-project-assumptions.md#assumption-014) | [`CONSTRAINT-014`](./11-project-constraints.md#constraint-014) |
| [`DEPENDENCY-065`](#dependency-065) | [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) | [`RISK-065`](./12-project-risks.md#risk-065) | [`MILESTONE-025`](./14-project-milestones.md#milestone-025) | [`RELEASE-015`](./15-release-strategy.md#release-015) | [`ASSUMPTION-015`](./10-project-assumptions.md#assumption-015) | [`CONSTRAINT-015`](./11-project-constraints.md#constraint-015) |
| [`DEPENDENCY-066`](#dependency-066) | [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) | [`RISK-066`](./12-project-risks.md#risk-066) | [`MILESTONE-026`](./14-project-milestones.md#milestone-026) | [`RELEASE-016`](./15-release-strategy.md#release-016) | [`ASSUMPTION-016`](./10-project-assumptions.md#assumption-016) | [`CONSTRAINT-016`](./11-project-constraints.md#constraint-016) |
| [`DEPENDENCY-067`](#dependency-067) | [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) | [`RISK-067`](./12-project-risks.md#risk-067) | [`MILESTONE-027`](./14-project-milestones.md#milestone-027) | [`RELEASE-017`](./15-release-strategy.md#release-017) | [`ASSUMPTION-017`](./10-project-assumptions.md#assumption-017) | [`CONSTRAINT-017`](./11-project-constraints.md#constraint-017) |
| [`DEPENDENCY-068`](#dependency-068) | [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) | [`RISK-068`](./12-project-risks.md#risk-068) | [`MILESTONE-028`](./14-project-milestones.md#milestone-028) | [`RELEASE-018`](./15-release-strategy.md#release-018) | [`ASSUMPTION-018`](./10-project-assumptions.md#assumption-018) | [`CONSTRAINT-018`](./11-project-constraints.md#constraint-018) |
| [`DEPENDENCY-069`](#dependency-069) | [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) | [`RISK-069`](./12-project-risks.md#risk-069) | [`MILESTONE-029`](./14-project-milestones.md#milestone-029) | [`RELEASE-019`](./15-release-strategy.md#release-019) | [`ASSUMPTION-019`](./10-project-assumptions.md#assumption-019) | [`CONSTRAINT-019`](./11-project-constraints.md#constraint-019) |
| [`DEPENDENCY-070`](#dependency-070) | [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) | [`RISK-070`](./12-project-risks.md#risk-070) | [`MILESTONE-030`](./14-project-milestones.md#milestone-030) | [`RELEASE-020`](./15-release-strategy.md#release-020) | [`ASSUMPTION-020`](./10-project-assumptions.md#assumption-020) | [`CONSTRAINT-020`](./11-project-constraints.md#constraint-020) |
| [`DEPENDENCY-071`](#dependency-071) | [`ROLE-011`](./08-role-and-responsibility-matrix.md#role-011) | [`RISK-071`](./12-project-risks.md#risk-071) | [`MILESTONE-031`](./14-project-milestones.md#milestone-031) | [`RELEASE-021`](./15-release-strategy.md#release-021) | [`ASSUMPTION-021`](./10-project-assumptions.md#assumption-021) | [`CONSTRAINT-021`](./11-project-constraints.md#constraint-021) |
| [`DEPENDENCY-072`](#dependency-072) | [`ROLE-012`](./08-role-and-responsibility-matrix.md#role-012) | [`RISK-072`](./12-project-risks.md#risk-072) | [`MILESTONE-032`](./14-project-milestones.md#milestone-032) | [`RELEASE-022`](./15-release-strategy.md#release-022) | [`ASSUMPTION-022`](./10-project-assumptions.md#assumption-022) | [`CONSTRAINT-022`](./11-project-constraints.md#constraint-022) |
| [`DEPENDENCY-073`](#dependency-073) | [`ROLE-013`](./08-role-and-responsibility-matrix.md#role-013) | [`RISK-073`](./12-project-risks.md#risk-073) | [`MILESTONE-033`](./14-project-milestones.md#milestone-033) | [`RELEASE-023`](./15-release-strategy.md#release-023) | [`ASSUMPTION-023`](./10-project-assumptions.md#assumption-023) | [`CONSTRAINT-023`](./11-project-constraints.md#constraint-023) |
| [`DEPENDENCY-074`](#dependency-074) | [`ROLE-014`](./08-role-and-responsibility-matrix.md#role-014) | [`RISK-074`](./12-project-risks.md#risk-074) | [`MILESTONE-034`](./14-project-milestones.md#milestone-034) | [`RELEASE-024`](./15-release-strategy.md#release-024) | [`ASSUMPTION-024`](./10-project-assumptions.md#assumption-024) | [`CONSTRAINT-024`](./11-project-constraints.md#constraint-024) |
| [`DEPENDENCY-075`](#dependency-075) | [`ROLE-015`](./08-role-and-responsibility-matrix.md#role-015) | [`RISK-075`](./12-project-risks.md#risk-075) | [`MILESTONE-035`](./14-project-milestones.md#milestone-035) | [`RELEASE-025`](./15-release-strategy.md#release-025) | [`ASSUMPTION-025`](./10-project-assumptions.md#assumption-025) | [`CONSTRAINT-025`](./11-project-constraints.md#constraint-025) |
| [`DEPENDENCY-001`](#dependency-001) | [`ROLE-016`](./08-role-and-responsibility-matrix.md#role-016) | [`RISK-076`](./12-project-risks.md#risk-076) | [`MILESTONE-036`](./14-project-milestones.md#milestone-036) | [`RELEASE-001`](./15-release-strategy.md#release-001) | [`ASSUMPTION-026`](./10-project-assumptions.md#assumption-026) | [`CONSTRAINT-026`](./11-project-constraints.md#constraint-026) |
| [`DEPENDENCY-002`](#dependency-002) | [`ROLE-017`](./08-role-and-responsibility-matrix.md#role-017) | [`RISK-077`](./12-project-risks.md#risk-077) | [`MILESTONE-037`](./14-project-milestones.md#milestone-037) | [`RELEASE-002`](./15-release-strategy.md#release-002) | [`ASSUMPTION-027`](./10-project-assumptions.md#assumption-027) | [`CONSTRAINT-027`](./11-project-constraints.md#constraint-027) |
| [`DEPENDENCY-003`](#dependency-003) | [`ROLE-018`](./08-role-and-responsibility-matrix.md#role-018) | [`RISK-078`](./12-project-risks.md#risk-078) | [`MILESTONE-038`](./14-project-milestones.md#milestone-038) | [`RELEASE-003`](./15-release-strategy.md#release-003) | [`ASSUMPTION-028`](./10-project-assumptions.md#assumption-028) | [`CONSTRAINT-028`](./11-project-constraints.md#constraint-028) |
| [`DEPENDENCY-004`](#dependency-004) | [`ROLE-019`](./08-role-and-responsibility-matrix.md#role-019) | [`RISK-079`](./12-project-risks.md#risk-079) | [`MILESTONE-039`](./14-project-milestones.md#milestone-039) | [`RELEASE-004`](./15-release-strategy.md#release-004) | [`ASSUMPTION-029`](./10-project-assumptions.md#assumption-029) | [`CONSTRAINT-029`](./11-project-constraints.md#constraint-029) |
| [`DEPENDENCY-005`](#dependency-005) | [`ROLE-020`](./08-role-and-responsibility-matrix.md#role-020) | [`RISK-080`](./12-project-risks.md#risk-080) | [`MILESTONE-040`](./14-project-milestones.md#milestone-040) | [`RELEASE-005`](./15-release-strategy.md#release-005) | [`ASSUMPTION-030`](./10-project-assumptions.md#assumption-030) | [`CONSTRAINT-030`](./11-project-constraints.md#constraint-030) |
| [`DEPENDENCY-006`](#dependency-006) | [`ROLE-021`](./08-role-and-responsibility-matrix.md#role-021) | [`RISK-081`](./12-project-risks.md#risk-081) | [`MILESTONE-001`](./14-project-milestones.md#milestone-001) | [`RELEASE-006`](./15-release-strategy.md#release-006) | [`ASSUMPTION-031`](./10-project-assumptions.md#assumption-031) | [`CONSTRAINT-031`](./11-project-constraints.md#constraint-031) |
| [`DEPENDENCY-007`](#dependency-007) | [`ROLE-022`](./08-role-and-responsibility-matrix.md#role-022) | [`RISK-082`](./12-project-risks.md#risk-082) | [`MILESTONE-002`](./14-project-milestones.md#milestone-002) | [`RELEASE-007`](./15-release-strategy.md#release-007) | [`ASSUMPTION-032`](./10-project-assumptions.md#assumption-032) | [`CONSTRAINT-032`](./11-project-constraints.md#constraint-032) |
| [`DEPENDENCY-008`](#dependency-008) | [`ROLE-023`](./08-role-and-responsibility-matrix.md#role-023) | [`RISK-083`](./12-project-risks.md#risk-083) | [`MILESTONE-003`](./14-project-milestones.md#milestone-003) | [`RELEASE-008`](./15-release-strategy.md#release-008) | [`ASSUMPTION-033`](./10-project-assumptions.md#assumption-033) | [`CONSTRAINT-033`](./11-project-constraints.md#constraint-033) |
| [`DEPENDENCY-009`](#dependency-009) | [`ROLE-024`](./08-role-and-responsibility-matrix.md#role-024) | [`RISK-084`](./12-project-risks.md#risk-084) | [`MILESTONE-004`](./14-project-milestones.md#milestone-004) | [`RELEASE-009`](./15-release-strategy.md#release-009) | [`ASSUMPTION-034`](./10-project-assumptions.md#assumption-034) | [`CONSTRAINT-034`](./11-project-constraints.md#constraint-034) |
| [`DEPENDENCY-010`](#dependency-010) | [`ROLE-025`](./08-role-and-responsibility-matrix.md#role-025) | [`RISK-085`](./12-project-risks.md#risk-085) | [`MILESTONE-005`](./14-project-milestones.md#milestone-005) | [`RELEASE-010`](./15-release-strategy.md#release-010) | [`ASSUMPTION-035`](./10-project-assumptions.md#assumption-035) | [`CONSTRAINT-035`](./11-project-constraints.md#constraint-035) |
| [`DEPENDENCY-011`](#dependency-011) | [`ROLE-026`](./08-role-and-responsibility-matrix.md#role-026) | [`RISK-086`](./12-project-risks.md#risk-086) | [`MILESTONE-006`](./14-project-milestones.md#milestone-006) | [`RELEASE-011`](./15-release-strategy.md#release-011) | [`ASSUMPTION-036`](./10-project-assumptions.md#assumption-036) | [`CONSTRAINT-036`](./11-project-constraints.md#constraint-036) |
| [`DEPENDENCY-012`](#dependency-012) | [`ROLE-027`](./08-role-and-responsibility-matrix.md#role-027) | [`RISK-087`](./12-project-risks.md#risk-087) | [`MILESTONE-007`](./14-project-milestones.md#milestone-007) | [`RELEASE-012`](./15-release-strategy.md#release-012) | [`ASSUMPTION-037`](./10-project-assumptions.md#assumption-037) | [`CONSTRAINT-037`](./11-project-constraints.md#constraint-037) |
| [`DEPENDENCY-013`](#dependency-013) | [`ROLE-028`](./08-role-and-responsibility-matrix.md#role-028) | [`RISK-088`](./12-project-risks.md#risk-088) | [`MILESTONE-008`](./14-project-milestones.md#milestone-008) | [`RELEASE-013`](./15-release-strategy.md#release-013) | [`ASSUMPTION-038`](./10-project-assumptions.md#assumption-038) | [`CONSTRAINT-038`](./11-project-constraints.md#constraint-038) |
| [`DEPENDENCY-014`](#dependency-014) | [`ROLE-029`](./08-role-and-responsibility-matrix.md#role-029) | [`RISK-089`](./12-project-risks.md#risk-089) | [`MILESTONE-009`](./14-project-milestones.md#milestone-009) | [`RELEASE-014`](./15-release-strategy.md#release-014) | [`ASSUMPTION-039`](./10-project-assumptions.md#assumption-039) | [`CONSTRAINT-039`](./11-project-constraints.md#constraint-039) |
| [`DEPENDENCY-015`](#dependency-015) | [`ROLE-030`](./08-role-and-responsibility-matrix.md#role-030) | [`RISK-090`](./12-project-risks.md#risk-090) | [`MILESTONE-010`](./14-project-milestones.md#milestone-010) | [`RELEASE-015`](./15-release-strategy.md#release-015) | [`ASSUMPTION-040`](./10-project-assumptions.md#assumption-040) | [`CONSTRAINT-040`](./11-project-constraints.md#constraint-040) |
| [`DEPENDENCY-016`](#dependency-016) | [`ROLE-001`](./08-role-and-responsibility-matrix.md#role-001) | [`RISK-091`](./12-project-risks.md#risk-091) | [`MILESTONE-011`](./14-project-milestones.md#milestone-011) | [`RELEASE-016`](./15-release-strategy.md#release-016) | [`ASSUMPTION-041`](./10-project-assumptions.md#assumption-041) | [`CONSTRAINT-041`](./11-project-constraints.md#constraint-041) |
| [`DEPENDENCY-017`](#dependency-017) | [`ROLE-002`](./08-role-and-responsibility-matrix.md#role-002) | [`RISK-092`](./12-project-risks.md#risk-092) | [`MILESTONE-012`](./14-project-milestones.md#milestone-012) | [`RELEASE-017`](./15-release-strategy.md#release-017) | [`ASSUMPTION-042`](./10-project-assumptions.md#assumption-042) | [`CONSTRAINT-042`](./11-project-constraints.md#constraint-042) |
| [`DEPENDENCY-018`](#dependency-018) | [`ROLE-003`](./08-role-and-responsibility-matrix.md#role-003) | [`RISK-093`](./12-project-risks.md#risk-093) | [`MILESTONE-013`](./14-project-milestones.md#milestone-013) | [`RELEASE-018`](./15-release-strategy.md#release-018) | [`ASSUMPTION-043`](./10-project-assumptions.md#assumption-043) | [`CONSTRAINT-043`](./11-project-constraints.md#constraint-043) |
| [`DEPENDENCY-019`](#dependency-019) | [`ROLE-004`](./08-role-and-responsibility-matrix.md#role-004) | [`RISK-094`](./12-project-risks.md#risk-094) | [`MILESTONE-014`](./14-project-milestones.md#milestone-014) | [`RELEASE-019`](./15-release-strategy.md#release-019) | [`ASSUMPTION-044`](./10-project-assumptions.md#assumption-044) | [`CONSTRAINT-044`](./11-project-constraints.md#constraint-044) |
| [`DEPENDENCY-020`](#dependency-020) | [`ROLE-005`](./08-role-and-responsibility-matrix.md#role-005) | [`RISK-095`](./12-project-risks.md#risk-095) | [`MILESTONE-015`](./14-project-milestones.md#milestone-015) | [`RELEASE-020`](./15-release-strategy.md#release-020) | [`ASSUMPTION-045`](./10-project-assumptions.md#assumption-045) | [`CONSTRAINT-045`](./11-project-constraints.md#constraint-045) |
| [`DEPENDENCY-021`](#dependency-021) | [`ROLE-006`](./08-role-and-responsibility-matrix.md#role-006) | [`RISK-096`](./12-project-risks.md#risk-096) | [`MILESTONE-016`](./14-project-milestones.md#milestone-016) | [`RELEASE-021`](./15-release-strategy.md#release-021) | [`ASSUMPTION-046`](./10-project-assumptions.md#assumption-046) | [`CONSTRAINT-046`](./11-project-constraints.md#constraint-046) |
| [`DEPENDENCY-022`](#dependency-022) | [`ROLE-007`](./08-role-and-responsibility-matrix.md#role-007) | [`RISK-097`](./12-project-risks.md#risk-097) | [`MILESTONE-017`](./14-project-milestones.md#milestone-017) | [`RELEASE-022`](./15-release-strategy.md#release-022) | [`ASSUMPTION-047`](./10-project-assumptions.md#assumption-047) | [`CONSTRAINT-047`](./11-project-constraints.md#constraint-047) |
| [`DEPENDENCY-023`](#dependency-023) | [`ROLE-008`](./08-role-and-responsibility-matrix.md#role-008) | [`RISK-098`](./12-project-risks.md#risk-098) | [`MILESTONE-018`](./14-project-milestones.md#milestone-018) | [`RELEASE-023`](./15-release-strategy.md#release-023) | [`ASSUMPTION-048`](./10-project-assumptions.md#assumption-048) | [`CONSTRAINT-048`](./11-project-constraints.md#constraint-048) |
| [`DEPENDENCY-024`](#dependency-024) | [`ROLE-009`](./08-role-and-responsibility-matrix.md#role-009) | [`RISK-099`](./12-project-risks.md#risk-099) | [`MILESTONE-019`](./14-project-milestones.md#milestone-019) | [`RELEASE-024`](./15-release-strategy.md#release-024) | [`ASSUMPTION-049`](./10-project-assumptions.md#assumption-049) | [`CONSTRAINT-049`](./11-project-constraints.md#constraint-049) |
| [`DEPENDENCY-025`](#dependency-025) | [`ROLE-010`](./08-role-and-responsibility-matrix.md#role-010) | [`RISK-100`](./12-project-risks.md#risk-100) | [`MILESTONE-020`](./14-project-milestones.md#milestone-020) | [`RELEASE-025`](./15-release-strategy.md#release-025) | [`ASSUMPTION-050`](./10-project-assumptions.md#assumption-050) | [`CONSTRAINT-050`](./11-project-constraints.md#constraint-050) |

## 9. Dependency Management Governance & Sign-off Appendix
This Master Project Dependency Register and Critical Path Baseline has been formally ratified by the Delivery Project Management Office:

| Ratifying Official | Title & Cadre | Department | Ratification Date | Status |
| :--- | :--- | :--- | :---: | :---: |
| **Dr. K. V. Trilok Chandra, IAS** | Special Commissioner (Health), BBMP | Project Executive Sponsor | 2026-03-01 | `APPROVED` |
| **Dr. Nirmala Buggi** | Chief Health Officer (Public Health) | Clinical Safety Authority | 2026-03-01 | `APPROVED` |
| **Sri. S. Vidyashankar** | Managing Director, K-Mati Analytics | Program Director | 2026-03-01 | `APPROVED` |
| **Sri. Venkatesh Prasad** | Technical Project Manager | PMO Critical Path Lead | 2026-03-01 | `APPROVED` |
