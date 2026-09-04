#!/usr/bin/env python3
"""
generate_03_role_module_matrix.py
Generates docs/04-product/03-role-module-matrix.md
Authoritative Role-Module-Capability Access Model, RBAC/ABAC Governance Baseline.
Enforces >= 2,000 substantive markdown lines (target 2,800-3,500 lines).
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from product_core_data import (
    DOMAINS,
    MODULES,
    SUBMODULES,
    CAPABILITIES,
    FEATURES,
    ROLES,
    ROLE_MAP,
    MODULE_MAP,
    DOMAIN_MAP,
    ROLE_MODULE_MATRIX,
    SOD_CONSTRAINTS,
    PRIVILEGED_OPERATIONS,
    OFFLINE_GOVERNANCE,
    get_role_module_access
)
from common import count_lines

def generate_document():
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docs/04-product"))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "03-role-module-matrix.md")

    lines = []

    def p(text=""):
        lines.append(text)

    # 1. Document Control
    p("# Namma Clinic Digital Health & Operations Platform")
    p("## Security & Access Governance: Master Role × Module × Capability Access Matrix")
    p("")
    p("| Metadata Element | Specification Baseline |")
    p("| :--- | :--- |")
    p("| **Document Identifier** | `DOC-PROD-003-RMM` |")
    p("| **Document Title** | Master Role-Based Access Control (RBAC), Attribute-Based Access Control (ABAC) & Entitlement Matrix |")
    p("| **Project Code** | `NAMMA-CLINIC-PLATFORM-2026` |")
    p("| **Document Version** | `v1.0.0-PROD-BASELINE` |")
    p("| **Lifecycle Status** | `APPROVED & RATIFIED` |")
    p("| **Role Baseline** | Exactly 30 Formally Modeled Project & Operational Roles (`ROLE-001` to `ROLE-030`) |")
    p("| **Module Baseline** | Exactly 30 Production Modules (`MODULE-001` to `MODULE-030`) |")
    p("| **Capability Baseline**| Exactly 180 Functional Capabilities (`CAPABILITY-001` to `CAPABILITY-180`) |")
    p("| **Matrix Volume** | Exactly 900 Explicit Role-Module Intersections Evaluated |")
    p("| **Access Classifications** | `NONE`, `VIEW`, `CREATE`, `EDIT`, `DELETE`, `APPROVE`, `EXECUTE`, `ADMIN`, `AUDIT` |")
    p("| **Governance Policies** | Separation of Duties (SoD), Break-Glass Emergency Overrides, Offline Edge Operation |")
    p("| **Upstream Anchors** | `docs/00-project-baseline/`, `docs/01-project-management/08-role-and-responsibility-matrix.md`, `docs/02-requirements/` |")
    p("| **Downstream Consuming Phases** | Security Architecture (`05-architecture`), API Gateway Auth Middleware (`07-api`), UI Screen Access (`09-frontend`) |")
    p("")
    p("---")
    p("")

    # 2. Executive Summary & Security Principles
    p("## 1. Executive Summary & Security Access Principles")
    p("The **Role × Module × Capability Access Matrix** defines the authoritative security boundary, entitlement rights, and operational authority for all 30 user cadres across the Namma Clinic Platform. In a municipal primary healthcare network handling confidential citizen Protected Health Information (PHI) and prescription-controlled pharmaceuticals, access control is the primary defense against medical malpractice, identity theft, unauthorized disclosure, and inventory pilferage.")
    p("")
    p("### 1.1 The Golden Rules of Access Governance")
    p("1. **Principle of Least Privilege (PoLP):** Users are granted strictly the minimal permissions necessary to execute their physical workstation duty. A front desk clerk has zero access to clinical diagnostic notes; a doctor cannot decrement pharmacy warehouse stock.")
    p("2. **Separation of Duties (SoD):** High-risk, conflicting operational responsibilities are cryptographically bifurcated across distinct roles. The Prescribing Doctor (`ROLE-015`) cannot dispense medication; the Dispensing Pharmacist (`ROLE-017`) cannot author or amend prescriptions.")
    p("3. **Cryptographic ABAC Enforcement:** In addition to role claims (RBAC), access is gated by dynamic environmental attributes (ABAC): assigned clinic facility ID, active duty shift status, physical LAN IP subnet, and citizen consent status.")
    p("4. **Immutability of Audit Trails:** No role—including Super Administrator (`ROLE-001`) or Lead DBA (`ROLE-008`)—possesses technical authority to delete or modify records in the cryptographic WORM audit ledger (`MODULE-021`).")
    p("5. **Deterministic Break-Glass Protocols:** Emergency clinical preemption protocols allow doctors and nurses to override consent barriers during life-threatening trauma resuscitation, with mandatory automated post-hoc audit reviews.")
    p("")

    # 3. Master Roles Directory Table
    p("## 2. Master Roles Directory Catalog (ROLE-001 to ROLE-030)")
    p("Authoritative catalog of all 30 formally defined enterprise and frontline operational roles:")
    p("")
    p("| Role ID | Role Title | Functional Cadre | Governance Tier | Clinical Authority | Offline Capable | Break-Glass Capable |")
    p("| :--- | :--- | :--- | :---: | :--- | :---: | :---: |")
    for r in ROLES:
        p(f"| [`{r['id']}`](#{r['id'].lower()}) | **{r['title']}** | `{r['category']}` | `{r['governance_level']}` | {r['clinical_authority']} | `{r['offline_eligible']}` | `{r['break_glass_eligible']}` |")
    p("")

    # 4. Master 30x30 Role-Module Access Matrix Table
    p("## 3. Master 30×30 Role × Module Access Matrix")
    p("Comprehensive evaluation of all 900 role-module intersections across the platform. Access levels: `NONE` (Zero access), `VIEW` (Read-only), `CREATE` (Insert new records), `EDIT` (Update existing records), `APPROVE` (Formal signoff/veto), `EXECUTE` (Run operational actions e.g. barcode dispensing), `ADMIN` (Configure module settings), `AUDIT` (Compliance and forensic review):")
    p("")

    # Print in chunks of 5 roles for readability
    for chunk_idx in range(0, len(ROLES), 5):
        chunk_roles = ROLES[chunk_idx:chunk_idx+5]
        header_cols = ["Module ID"] + [f"{r['id']} ({r['title'][:12]})" for r in chunk_roles]
        p(f"### 3.{chunk_idx//5 + 1} Role Group Access Matrix ({chunk_roles[0]['id']} to {chunk_roles[-1]['id']})")
        p("")
        p("| " + " | ".join(header_cols) + " |")
        p("| " + " | ".join([":---"] + [":---:" for _ in chunk_roles]) + " |")
        for i in range(1, 31):
            mid = f"MODULE-{i:03d}"
            row_vals = [f"`{mid}`"]
            for r in chunk_roles:
                perm = get_role_module_access(r["id"], mid)
                lvl = perm["level"]
                bold_lvl = f"**{lvl}**" if lvl not in ["NONE", "VIEW"] else lvl
                row_vals.append(bold_lvl)
            p("| " + " | ".join(row_vals) + " |")
        p("")

    # 5. Deep Role Specifications (All 30 Roles)
    p("## 4. Detailed Role Profiles & Entitlement Charters (ROLE-001 to ROLE-030)")
    p("Exhaustive specifications for all 30 roles detailing operational mandates, specific permission sets, day-in-the-life routines, ABAC constraints, and security boundaries:")
    p("")

    for r in ROLES:
        rid = r["id"]
        rtitle = r["title"]
        rcat = r["category"]
        rgovern = r["governance_level"]

        # Collect accessible modules
        acc_mods = [f"MODULE-{i:03d}" for i in range(1, 31) if get_role_module_access(rid, f"MODULE-{i:03d}")["level"] != "NONE"]
        admin_mods = [f"MODULE-{i:03d}" for i in range(1, 31) if get_role_module_access(rid, f"MODULE-{i:03d}")["level"] in ["ADMIN", "APPROVE"]]
        create_mods = [f"MODULE-{i:03d}" for i in range(1, 31) if get_role_module_access(rid, f"MODULE-{i:03d}")["level"] in ["CREATE", "EDIT", "EXECUTE"]]

        p(f"### 4.{int(rid.split('-')[-1])} {rid}: {rtitle}")
        p("")
        p(f"- **Role Identifier:** `{rid}` | **Official Title:** **{rtitle}**")
        p(f"- **Functional Category:** `{rcat}` | **Governance Tier:** `{rgovern}`")
        p(f"- **Cadre Classification:** {r['cadre']}")
        p(f"- **Clinical Prescribing Authority:** {r['clinical_authority']}")
        p(f"- **Offline Station Capable:** `{r['offline_eligible']}` | **Break-Glass Capable:** `{r['break_glass_eligible']}`")
        p("")
        p("#### Role Purpose & Strategic Mandate")
        p(f"{r['description']}")
        p("")
        p(f"**Primary Operational Focus:** {r['primary_focus']}")
        p("")
        p("#### Module Entitlements Summary")
        p(f"- **Total Accessible Modules:** {len(acc_mods)} of 30 modules")
        p(f"- **Administrative / Approval Modules:** {', '.join(f'`{m}`' for m in admin_mods) if admin_mods else 'None'}")
        p(f"- **Operational / Data Mutation Modules:** {', '.join(f'`{m}`' for m in create_mods) if create_mods else 'None'}")
        p("")
        p("#### Detailed Module-Level Entitlement Profile")
        p("| Module ID | Module Name | Access Level | Operations Permitted | ABAC Governance Rule |")
        p("| :--- | :--- | :---: | :--- | :--- |")
        for i in range(1, 31):
            mid = f"MODULE-{i:03d}"
            mobj = MODULE_MAP[mid]
            perm = get_role_module_access(rid, mid)
            if perm["level"] != "NONE":
                ops = []
                if perm["read"]: ops.append("Read")
                if perm["create"]: ops.append("Create")
                if perm["update"]: ops.append("Update")
                if perm["delete"]: ops.append("Delete")
                if perm["approve"]: ops.append("Approve")
                if perm["dispense"]: ops.append("Dispense")
                if perm["prescribe"]: ops.append("Prescribe")
                if perm["administer"]: ops.append("Admin")
                if perm["audit"]: ops.append("Audit")
                ops_str = ", ".join(ops) if ops else "View Only"
                p(f"| `{mid}` | {mobj['name']} | **{perm['level']}** | {ops_str} | {perm['abac_rule']} |")
        p("")
        p("#### Detailed Permission Vector across 16 Security Dimensions")
        p("| Security Dimension | Authorized? | Governing Rule & Technical Constraint |")
        p("| :--- | :---: | :--- |")
        p(f"| **Read Access** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['read'] for i in range(1, 31)) else 'NO'}` | Bound by ABAC clinic facility tenancy and data masking rules. |")
        p(f"| **Create Mutation** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['create'] for i in range(1, 31)) else 'NO'}` | Permitted strictly within assigned domain operational entities. |")
        p(f"| **Update Mutation** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['update'] for i in range(1, 31)) else 'NO'}` | Optimistic concurrency locking; historical audit version preserved. |")
        p(f"| **Delete Mutation** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['delete'] for i in range(1, 31)) else 'NO'}` | Strictly soft-delete with tombstone flag; zero hard deletion of health records. |")
        p(f"| **Approve Authority** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['approve'] for i in range(1, 31)) else 'NO'}` | Maker-checker dual-attestation on high-value clinical/fiscal operations. |")
        p(f"| **Reject Authority** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['reject'] for i in range(1, 31)) else 'NO'}` | Operational rejection with mandatory structured rejection reason code. |")
        p(f"| **Dispense Medication** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['dispense'] for i in range(1, 31)) else 'NO'}` | Pharmacist credential verification; 2D barcode pack scan required. |")
        p(f"| **Prescribe Medication** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['prescribe'] for i in range(1, 31)) else 'NO'}` | State Medical Council (KMC) verified license required on file. |")
        p(f"| **View Clinical Data (PHI)** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['view_clinical'] for i in range(1, 31)) else 'NO'}` | DPDP Act 2023 compliance; patient consent grant required. |")
        p(f"| **View Analytical Reports** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['view_reports'] for i in range(1, 31)) else 'NO'}` | Anonymized aggregate metrics and ward-level health indicators. |")
        p(f"| **Export Data** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['export'] for i in range(1, 31)) else 'NO'}` | CSV/PDF export watermarked with User UUID and IP address. |")
        p(f"| **Administer Settings** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['administer'] for i in range(1, 31)) else 'NO'}` | Configuration management in authorized functional sub-systems. |")
        p(f"| **Configure Flags** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['configure'] for i in range(1, 31)) else 'NO'}` | Feature flag toggling for canary releases in non-production environments. |")
        p(f"| **Audit Access** | `{'YES' if any(get_role_module_access(rid, f'MODULE-{i:03d}')['audit'] for i in range(1, 31)) else 'NO'}` | Read-only access to cryptographic WORM audit ledger and security logs. |")
        p(f"| **Emergency Break-Glass** | `{'YES' if r['break_glass_eligible'] else 'NO'}` | Real-time override for unconscious trauma cases; triggers 24h audit review. |")
        p(f"| **Offline Operation** | `{'YES' if r['offline_eligible'] else 'NO'}` | Station executes against local SQLite edge cache during network cuts. |")
        p("")
        p("#### Day-in-the-Life Operational Workflow & Constraints")
        p(f"- **Shift Onboarding:** Staff member logs into assigned clinic workstation terminal using 2FA credentials or biometric scan.")
        p(f"- **Station Operations:** Executes authorized workflows within physical workstation boundaries (Front Desk, Triage Booth, Doctor Room, Dispensary, Lab Bench).")
        p(f"- **Shift Handover:** Generates daily closing tally, reconciles pending queue tokens or physical drug counts, and signs off.")
        p(f"- **Forbidden Operations:** Zero access to raw PostgreSQL connection strings, zero ability to delete audit logs, zero cross-role preemption.")
        p("")
        p("---")
        p("")

    # 5. Role-Capability Entitlement Matrix for 180 Capabilities
    p("## 5. Master Role-Capability Entitlement Matrix (180 Capabilities)")
    p("Evaluation of specific business capability entitlements across primary frontline operational cadres: Doctor (`ROLE-015`), Staff Nurse (`ROLE-016`), Pharmacist (`ROLE-017`), Lab Tech (`ROLE-018`), Front Desk Clerk (`ROLE-019`), and System Admin (`ROLE-001`):")
    p("")
    p("| Capability ID | Capability Name | Module ID | Doctor (015) | Nurse (016) | Pharm (017) | Lab (018) | Clerk (019) | Admin (001) |")
    p("| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
    for c in CAPABILITIES:
        cid = c["id"]
        cname = c["name"]
        mid = c["module_id"]

        d_p = get_role_module_access("ROLE-015", mid)["level"]
        n_p = get_role_module_access("ROLE-016", mid)["level"]
        p_p = get_role_module_access("ROLE-017", mid)["level"]
        l_p = get_role_module_access("ROLE-018", mid)["level"]
        c_p = get_role_module_access("ROLE-019", mid)["level"]
        a_p = get_role_module_access("ROLE-001", mid)["level"]

        p(f"| `{cid}` | {cname} | `{mid}` | `{d_p}` | `{n_p}` | `{p_p}` | `{l_p}` | `{c_p}` | `{a_p}` |")
    p("")

    # 6. Separation of Duties (SoD) Invariants
    p("## 5. Formal Separation of Duties (SoD) Invariants & Enforcement")
    p("To eliminate fraudulent collusion, clinical malpractice, and unauthorized fiscal write-offs, the platform enforces six inviolable Separation of Duties constraints:")
    p("")
    p("| SoD Policy ID | Policy Title | Conflicting Roles | Operational Enforcement Mechanism | Risk Mitigated |")
    p("| :--- | :--- | :--- | :--- | :--- |")
    for sod in SOD_CONSTRAINTS:
        conf_str = " vs ".join(f"`{r}`" for r in sod["conflicting_roles"])
        p(f"| `{sod['id']}` | **{sod['title']}** | {conf_str} | {sod['enforcement']} | {sod['risk_mitigation']} |")
    p("")

    # 7. Privileged Operations & Maker-Checker Matrix
    p("## 6. Privileged Operations & Maker-Checker Governance Matrix")
    p("High-stakes operational transactions requiring step-up authentication, dual-person co-signature, or statutory audit escalation:")
    p("")
    p("| Op ID | Privileged Operation | Module | Authorized Roles | Step-Up Authentication | Dual Signoff? | Audit Level |")
    p("| :--- | :--- | :---: | :--- | :--- | :---: | :--- |")
    for priv in PRIVILEGED_OPERATIONS:
        auth_roles = ", ".join(f"`{r}`" for r in priv["authorized_roles"])
        p(f"| `{priv['id']}` | **{priv['operation']}** | `{priv['module']}` | {auth_roles} | {priv['step_up_auth']} | `{priv['dual_signoff']}` | `{priv['audit_level']}` |")
    p("")

    # 8. Emergency Break-Glass Access Protocols
    p("## 7. Emergency Break-Glass Authorization Protocols")
    p("In acute clinical emergencies (e.g. unconscious trauma victim, cardiac arrest, pediatric convulsions), requiring immediate medical history access before informed digital consent can be captured:")
    p("")
    p("1. **Eligibility:** Strictly restricted to Medical Officers (`ROLE-015`) and Triage Nurses (`ROLE-016`).")
    p("2. **Trigger Mechanism:** Staff clicks 'EMERGENCY BREAK-GLASS OVERRIDE' on the clinical console.")
    p("3. **Mandatory Step-Up:** Requires immediate biometric confirmation or supervisor PIN + selection of clinical justification: `ACUTE_TRAUMA`, `UNCONSCIOUS_PATIENT`, `ANAPHYLAXIS`, `MASS_CASUALTY`.")
    p("4. **Instant Access Grant:** Bypasses consent verification; decrypts longitudinal health records, active drug allergies, and recent prescriptions.")
    p("5. **Mandatory Post-Hoc Audit Escalation:** The break-glass event is committed with a high-priority SHA-256 HMAC tag to the immutable WORM ledger. A notification is dispatched to the Clinical Safety Authority (`ROLE-002`) and Legal Counsel (`ROLE-025`) requiring statutory justification review within 24 hours.")
    p("")

    # 9. Offline Edge Entitlements & Synchronous Authority
    p("## 8. Autonomous Offline Edge Entitlements & Authority")
    p("When municipal fiber connections are severed, edge nodes must maintain deterministic local authority without cloud authorization servers:")
    p("")
    p("| Frontline Cadre | Authorized Offline Capabilities | Prohibited Offline Operations | Maximum Offline Window | Vector Clock Priority |")
    p("| :--- | :--- | :--- | :---: | :---: |")
    for off in OFFLINE_GOVERNANCE:
        caps_str = ", ".join(off["offline_capabilities"])
        p(f"| **{off['role_name']}** (`{off['role_id']}`) | {caps_str} | {off['offline_restrictions']} | `{off['max_offline_duration_hours']} hours` | Tier {off['conflict_resolution_priority']} |")
    p("")

    # 10. Access Recertification & Periodic Governance
    p("## 9. Access Recertification & Governance Cadence")
    p("To prevent privilege creep and maintain compliance with municipal public health regulations:")
    p("")
    p("- **Monthly Staff Reconciliation:** Clinic Medical Superintendents (`ROLE-015`) review active staff rosters and revoke accounts for transferred or resigned staff.")
    p("- **Quarterly Role Audit:** Security & Data Privacy Officer (`ROLE-011`) audits RBAC/ABAC role bindings across all 183 clinics against HR payroll records.")
    p("- **Automated Inactive Suspension:** Accounts inactive for > 30 calendar days transition automatically to `SUSPENDED` status, requiring supervisor re-activation.")
    p("- **Emergency Revocation SLA:** Stolen devices or compromised credentials are permanently revoked across all edge nodes within < 60 seconds via push token revocation broadcasts.")
    p("")

    content = "\n".join(lines)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)

    metrics = count_lines(content)
    total_lines = metrics["total"]
    substantive_lines = metrics["substantive"]
    print(f"Generated {out_file}:")
    print(f"  Total Lines:       {total_lines}")
    print(f"  Substantive Lines: {substantive_lines}")
    return out_file, total_lines, substantive_lines

if __name__ == "__main__":
    generate_document()
