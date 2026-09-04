#!/usr/bin/env python3
"""
build_features.py
Generates the authoritative feature definitions across all 6 domains:
- features_d1.py (Features 001-030)
- features_d2.py (Features 031-060)
- features_d3.py (Features 061-090)
- features_d4.py (Features 091-114)
- features_d5.py (Features 115-138)
- features_d6.py (Features 139-180)
Total: exactly 180 features mapped 1:1 to all 180 capabilities.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from domain_specs import ALL_CAPABILITIES, MODULE_MAP, DOMAIN_MAP

# Domain to Release and Sprint mapping defaults
DOMAIN_DEFAULTS = {
    "DOMAIN-001": {"rel": "REL-00", "sprint_base": 1, "persona": "PERSONA-001", "sec_personas": ["PERSONA-002", "PERSONA-003"]},
    "DOMAIN-002": {"rel": "REL-01", "sprint_base": 3, "persona": "PERSONA-006", "sec_personas": ["PERSONA-007", "PERSONA-008"]},
    "DOMAIN-003": {"rel": "REL-01", "sprint_base": 4, "persona": "PERSONA-002", "sec_personas": ["PERSONA-003", "PERSONA-005"]},
    "DOMAIN-004": {"rel": "REL-01", "sprint_base": 5, "persona": "PERSONA-004", "sec_personas": ["PERSONA-002", "PERSONA-007"]},
    "DOMAIN-005": {"rel": "REL-02", "sprint_base": 7, "persona": "PERSONA-003", "sec_personas": ["PERSONA-002", "PERSONA-008"]},
    "DOMAIN-006": {"rel": "REL-01", "sprint_base": 2, "persona": "PERSONA-029", "sec_personas": ["PERSONA-001", "PERSONA-030"]},
}

# Special release assignments for advanced modules
MODULE_RELEASE_OVERRIDES = {
    "MODULE-020": {"rel": "REL-02", "sprint": "Sprint 07", "mvp": "MVP-PLUS", "prio": "P2 - Medium", "moscow": "SHOULD"},
    "MODULE-028": {"rel": "REL-02", "sprint": "Sprint 08", "mvp": "MVP-PLUS", "prio": "P2 - Medium", "moscow": "SHOULD"},
    "MODULE-029": {"rel": "REL-03", "sprint": "Sprint 11", "mvp": "POST-MVP", "prio": "P2 - Medium", "moscow": "COULD"},
    "MODULE-023": {"rel": "REL-06", "sprint": "Sprint 21", "mvp": "POST-MVP", "prio": "P2 - Medium", "moscow": "COULD"},
    "MODULE-030": {"rel": "REL-04", "sprint": "Sprint 15", "mvp": "POST-MVP", "prio": "P2 - Medium", "moscow": "COULD"},
    "MODULE-018": {"rel": "REL-02", "sprint": "Sprint 07", "mvp": "MVP-PLUS", "prio": "P1 - High", "moscow": "SHOULD"},
}

def generate_domain_features(domain_id: str, out_file: str, var_name: str):
    caps = [c for c in ALL_CAPABILITIES if c["domain_id"] == domain_id]
    base_name = os.path.basename(out_file)
    lines = []
    lines.append("#!/usr/bin/env python3")
    lines.append(f'"""\n{base_name}\nAuthoritative feature definitions for {domain_id} ({DOMAIN_MAP[domain_id]["name"]}).\nContains {len(caps)} features.\n"""')
    lines.append("")
    lines.append("import sys")
    lines.append("import os")
    lines.append("sys.path.append(os.path.dirname(os.path.abspath(__file__)))")
    lines.append("from feature_factory import make_feature")
    lines.append("")
    lines.append(f"{var_name} = [")

    for idx, c in enumerate(caps):
        cap_num = int(c["id"].split("-")[-1])
        feat_id = f"FEATURE-{cap_num:03d}"
        mod_id = c["module_id"]
        mod = MODULE_MAP[mod_id]
        submod_id = c["submodule_id"]
        dom_id = c["domain_id"]
        d_cfg = DOMAIN_DEFAULTS[dom_id]

        # Name and basic attributes
        name = c["name"]
        desc = f"Executes {c['name'].lower()} within the operational scope of {mod['name']} ({mod_id}), supporting primary health workflows across Greater Bengaluru Namma Clinics."
        user_problem = f"Healthcare workers and citizens face operational friction when {c['name'].lower()} is handled manually on paper or delayed by network bottlenecks."
        business_value = f"Eliminates manual paperwork, establishes auditable digital logs, accelerates clinic throughput, and guarantees statutory compliance in {mod['name']}."
        user_value = f"Empowers facility staff to perform {c['name'].lower()} in < 250ms with clear visual feedback in Kannada and English."

        # Persona & roles
        primary_persona = d_cfg["persona"]
        sec_personas = d_cfg["sec_personas"]
        roles = mod["roles"]

        # Trigger & preconditions
        trigger = f"Operator at clinic station triggers {name} action on client terminal UI."
        preconditions = f"Station terminal authenticated under {mod_id}; local SQLite edge database online and verified."

        # Flows
        main_flow = [
            f"1. Operator navigates to {mod['name']} workspace and activates {name}.",
            f"2. System validates input fields and verifies session authorization under {mod_id}.",
            f"3. Core business and clinical rules are evaluated against local edge SQLite store.",
            f"4. Transaction is committed atomically to local WAL with cryptographic HMAC signature.",
            f"5. UI renders confirmation banner in Kannada and English; dispatches local IPC event."
        ]
        alt_flow = [
            f"1. Broadband network link is unavailable during {name} initiation.",
            f"2. System detects offline mode and executes transaction against local edge cache.",
            f"3. Mutation is committed locally and appended to outbound cloud synchronization queue.",
            f"4. Operator receives green offline status checkmark indicating data is safely persisted."
        ]
        exception_flow = [
            f"1. Input data fails schema format validation or violates integrity boundary.",
            f"2. System rejects mutation, highlights invalid fields in red, and emits localized Kannada prompt.",
            f"3. Uncommitted transaction is rolled back; error is logged in error catalog."
        ]

        # Prioritization & release
        if mod_id in MODULE_RELEASE_OVERRIDES:
            ovr = MODULE_RELEASE_OVERRIDES[mod_id]
            rel = ovr["rel"]
            sprint = ovr["sprint"]
            mvp = ovr["mvp"]
            prio = ovr["prio"]
            moscow = ovr["moscow"]
        else:
            rel = d_cfg["rel"]
            sprint_num = d_cfg["sprint_base"] + (idx // 6)
            sprint = f"Sprint {sprint_num:02d}"
            mvp = mod.get("mvp_status", "CORE MVP")
            prio = mod.get("priority", "P1 - High")
            moscow = "MUST" if "CORE" in mvp else "SHOULD"

        req_refs = mod.get("requirements", ["BR-001", "FR-001"])[:4]
        wf_refs = mod.get("workflows", ["WF-001"])

        # Gherkin Scenarios
        gherkin = {
            "happy": {
                "given": f"the operator is authenticated with role {roles[0]} and {mod['name']} is active",
                "when": f"the operator submits valid parameters for {name}",
                "then": f"the system successfully commits the transaction to local SQLite storage",
                "and": f"an immutable audit event AUD-FEAT-{cap_num:03d} is recorded with SHA-256 hash"
            },
            "negative": {
                "given": f"an unauthenticated user or unauthorized role attempts to access {name}",
                "when": f"the execution request is evaluated by the authorization gate",
                "then": f"the system blocks execution with HTTP 403 Forbidden",
                "and": f"a security warning log is dispatched to the zonal audit monitor"
            },
            "edge": {
                "given": f"the clinic terminal experiences unexpected power disruption during {name} commit",
                "when": f"the workstation edge server boots back up on battery UPS",
                "then": f"the SQLite Write-Ahead Log automatically restores database state to pre-crash consistency",
                "and": f"no partial or corrupted records remain in {mod['name']}"
            },
            "offline": {
                "given": f"the clinic broadband connection is severed before invoking {name}",
                "when": f"the operator performs {name} on local edge workstation",
                "then": f"the operation completes in under 50ms without cloud roundtrip",
                "and": f"the payload is queued in local SQLite table for automated background cloud replay"
            }
        }

        edge_cases = [
            f"Rapid successive clicks on {name} submit button handled by idempotent request deduplication token.",
            f"Handling legacy character encodings and non-standard Kannada vowel glyph combinations without font breakage.",
            f"Graceful degradation when peripheral hardware (scanner/printer) disconnects during {name} execution."
        ]

        failure_scenarios = [
            f"Local disk storage drops below 2.0GB: {name} locks non-essential logging and triggers automated WAL checkpoint.",
            f"SQLite table lock contention timeout (> 2,000ms): transaction aborts safely and prompts operator to retry."
        ]

        recovery_behavior = f"Automated state rollback; UI alerts operator with SOP recovery instruction SOP-FEAT-{cap_num:03d}."
        data_objects = [f"{name.replace(' ', '')}Record", "AuditTrailEntry", "OutboundQueueMutation"]
        observability_span = f"span.namma_clinic.{mod_id.lower().replace('-', '_')}.feat_{cap_num:03d}"
        observability_metric = f"namma_clinic_{mod_id.lower().replace('-', '_')}_feat_{cap_num:03d}_seconds"

        success_metrics = [
            f"P95 transaction response time < 250ms on local edge appliance.",
            f"Zero data loss during unexpected station power loss."
        ]
        kpis = [f"Operational efficiency in {mod['name']} >= 99.5%."]
        out_of_scope = f"Third-party commercial marketing integration and non-health municipal billing."

        # Dependencies
        deps = []
        if cap_num > 1:
            prev_cap = f"FEATURE-{cap_num - 1:03d}"
            deps.append(prev_cap)

        lines.append("    make_feature(")
        lines.append(f'        feat_id="{feat_id}",')
        lines.append(f'        name="{name}",')
        lines.append(f'        cap_id="{c["id"]}",')
        lines.append(f'        submod_id="{submod_id}",')
        lines.append(f'        mod_id="{mod_id}",')
        lines.append(f'        dom_id="{dom_id}",')
        lines.append(f'        desc="{desc}",')
        lines.append(f'        user_problem="{user_problem}",')
        lines.append(f'        business_value="{business_value}",')
        lines.append(f'        user_value="{user_value}",')
        lines.append(f'        primary_persona="{primary_persona}",')
        lines.append(f'        secondary_personas={sec_personas},')
        lines.append(f'        roles={roles},')
        lines.append(f'        trigger="{trigger}",')
        lines.append(f'        preconditions="{preconditions}",')
        lines.append(f'        main_flow={main_flow},')
        lines.append(f'        alt_flow={alt_flow},')
        lines.append(f'        exception_flow={exception_flow},')
        lines.append(f'        req_refs={req_refs},')
        lines.append(f'        wf_refs={wf_refs},')
        lines.append(f'        priority="{prio}",')
        lines.append(f'        moscow="{moscow}",')
        lines.append(f'        mvp_status="{mvp}",')
        lines.append(f'        release_target="{rel}",')
        lines.append(f'        sprint_target="{sprint}",')
        lines.append(f'        gherkin_scenarios={gherkin},')
        lines.append(f'        edge_cases={edge_cases},')
        lines.append(f'        failure_scenarios={failure_scenarios},')
        lines.append(f'        recovery_behavior="{recovery_behavior}",')
        lines.append(f'        data_objects={data_objects},')
        lines.append(f'        observability_span="{observability_span}",')
        lines.append(f'        observability_metric="{observability_metric}",')
        lines.append(f'        success_metrics={success_metrics},')
        lines.append(f'        kpis={kpis},')
        lines.append(f'        out_of_scope="{out_of_scope}",')
        lines.append(f'        dependencies={deps}')
        lines.append("    ),")

    lines.append("]")
    lines.append("")
    lines.append(f'if __name__ == "__main__":')
    lines.append(f'    print(f"Total features in {var_name}: {{len({var_name})}}")')
    lines.append("")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {out_file} with {len(caps)} features.")

def main():
    repo_root = os.path.dirname(os.path.abspath(__file__))
    domains = [
        ("DOMAIN-001", os.path.join(repo_root, "features_d1.py"), "D1_FEATURES"),
        ("DOMAIN-002", os.path.join(repo_root, "features_d2.py"), "D2_FEATURES"),
        ("DOMAIN-003", os.path.join(repo_root, "features_d3.py"), "D3_FEATURES"),
        ("DOMAIN-004", os.path.join(repo_root, "features_d4.py"), "D4_FEATURES"),
        ("DOMAIN-005", os.path.join(repo_root, "features_d5.py"), "D5_FEATURES"),
        ("DOMAIN-006", os.path.join(repo_root, "features_d6.py"), "D6_FEATURES"),
    ]

    for dom_id, out_file, var_name in domains:
        generate_domain_features(dom_id, out_file, var_name)

if __name__ == "__main__":
    main()
