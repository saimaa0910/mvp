#!/usr/bin/env python3
"""
common.py
Core rendering and formatting utilities for Namma Clinic Requirements Engineering Documentation.
Provides standardized Markdown generation for requirements, rules, traceability matrices,
Gherkin scenarios, tables, and Mermaid architecture diagrams.
"""

import os
import sys

def p_line(lines, text=""):
    lines.append(text)

def render_metadata_table(lines, doc_id, doc_title, req_type, req_range, count, parent_baseline, counterpart):
    p_line(lines, "| Metadata Attribute | Formal Specification |")
    p_line(lines, "| :--- | :--- |")
    p_line(lines, f"| **Document Identifier** | `{doc_id}` |")
    p_line(lines, f"| **Document Title** | {doc_title} |")
    p_line(lines, f"| **Project Code** | `NAMMA-CLINIC-PLATFORM-2026` |")
    p_line(lines, f"| **Requirement Type** | `{req_type}` |")
    p_line(lines, f"| **Specification Range** | `{req_range}` (Exactly {count} unique requirements) |")
    p_line(lines, f"| **Target Baseline** | `v1.0.0-PROD-BASELINE` |")
    p_line(lines, f"| **Lifecycle Status** | `APPROVED & BASELINED` |")
    p_line(lines, f"| **Target Facility Scope** | 183 Primary Namma Clinics across 8 BBMP Administrative Zones |")
    p_line(lines, f"| **Lead Clinical Authority** | Chief Health Officer (CHO), BBMP Health Department |")
    p_line(lines, f"| **Lead Technical Authority**| Principal Solutions Architect, Kushagramati Analytics Consortium |")
    p_line(lines, f"| **Upstream Baselines** | [`00-project-baseline/`](../00-project-baseline/) \\| [`01-project-management/`](../01-project-management/) |")
    p_line(lines, f"| **Related Specification**| [`{parent_baseline}`](./{parent_baseline}) \\| [`{counterpart}`](./{counterpart}) |")
    p_line(lines)

def render_traceability_summary_table(lines, reqs):
    p_line(lines, "| Requirement ID | Title | Priority | Primary Actor | Upstream Objective | Upstream Scope | Downstream Epic | Downstream API | Verification Method |")
    p_line(lines, "| :--- | :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in reqs:
        req_id = r["id"]
        title = r["title"]
        priority = r.get("priority", "MUST")
        actor = r.get("actor", "Medical Officer")
        obj = r.get("objective_ref", "OBJECTIVE-001")
        scope = r.get("scope_ref", "INSCOPE-001")
        epic = r.get("planned_epic", "PLANNED-EPIC-001")
        api = r.get("planned_api", "PLANNED-API-001")
        vmethod = r.get("verification_method", "Automated Integration Test")
        p_line(lines, f"| [`{req_id}`](#{req_id.lower()}) | **{title}** | `{priority}` | {actor} | [`{obj}`](../01-project-management/02-project-vision-and-objectives.md#{obj.lower()}) | [`{scope}`](../01-project-management/04-in-scope.md#{scope.lower()}) | `{epic}` | `{api}` | {vmethod} |")
    p_line(lines)

def format_gherkin(req):
    req_id = req["id"]
    title = req["title"]
    actor = req.get("actor", "Medical Officer")
    gh = req.get("gherkin", {})
    
    happy = gh.get("happy", {
        "given": f"the {actor} is authenticated and clinic terminal is operational",
        "when": f"the user submits a valid request for {title.lower()}",
        "then": f"the system successfully commits the transaction and emits an audit event"
    })
    validation = gh.get("validation", {
        "given": f"the {actor} attempts to submit an incomplete or malformed payload for {title.lower()}",
        "when": f"the request fails TypeBox schema or domain constraint validation",
        "then": f"the system rejects the input with HTTP 400 and highlights invalid fields in Kannada and English"
    })
    security = gh.get("security", {
        "given": f"an unauthenticated or unauthorized role attempts to invoke {title.lower()}",
        "when": f"the bearer JWT token is missing, expired, or lacks necessary RBAC permission",
        "then": f"the system denies execution with HTTP 403 Forbidden and records a security telemetry alert"
    })
    offline = gh.get("offline", {
        "given": f"the clinic WAN network is completely severed during {title.lower()}",
        "when": f"the operator confirms the local transaction on the workstation",
        "then": f"the mutation is persisted to Dexie.js IndexedDB with a UUIDv7 and queued for background replay"
    })
    recovery = gh.get("recovery", {
        "given": f"the clinic workstation reconnects to the BBMP municipal health WAN",
        "when": f"the background sync daemon processes the pending mutation queue",
        "then": f"all buffered transactions for {req_id} synchronize idempotently with zero data loss"
    })

    gherkin_lines = [
        f"```gherkin",
        f"Feature: {req_id} - {title}",
        f"  As a {actor}",
        f"  I require system enforcement of {title.lower()}",
        f"  In order to ensure municipal healthcare compliance and operational integrity",
        f"",
        f"  Scenario: Happy Path Execution for {req_id}",
        f"    Given {happy['given']}",
        f"    When {happy['when']}",
        f"    Then {happy['then']}",
        f"",
        f"  Scenario: Input Validation and Schema Guard for {req_id}",
        f"    Given {validation['given']}",
        f"    When {validation['when']}",
        f"    Then {validation['then']}",
        f"",
        f"  Scenario: RBAC and Security Access Control for {req_id}",
        f"    Given {security['given']}",
        f"    When {security['when']}",
        f"    Then {security['then']}",
        f"",
        f"  Scenario: Offline Autonomous Execution for {req_id}",
        f"    Given {offline['given']}",
        f"    When {offline['when']}",
        f"    Then {offline['then']}",
        f"",
        f"  Scenario: Network Recovery and Idempotent Sync for {req_id}",
        f"    Given {recovery['given']}",
        f"    When {recovery['when']}",
        f"    Then {recovery['then']}",
        f"```"
    ]
    return gherkin_lines
