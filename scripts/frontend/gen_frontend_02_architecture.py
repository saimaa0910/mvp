"""
gen_frontend_02_architecture.py
Generator for docs/09-frontend/02-frontend-architecture.md.
Produces >= 2,000 substantive lines detailing the frontend architecture, application shell,
state flow, IndexedDB/Dexie offline boundaries, and Mermaid diagrams.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.frontend.frontend_gen_common import write_fe_doc
from scripts.frontend.frontend_core_data import SCREENS, COMPONENTS, ROLES

def generate_doc():
    lines = []
    lines.append("# Namma Clinic Frontend Architecture Specification")
    lines.append("")
    lines.append("## 1. Architectural Vision & Operational Context")
    lines.append("The Namma Clinic Frontend Architecture provides an enterprise-grade, local-first, highly responsive web application framework designed to run autonomously within 183 primary healthcare clinics under the Greater Bengaluru Authority (GBA) / BBMP Health Department. Due to frequent metropolitan telecommunication fiber disruptions, power fluctuations, and variable cellular reception across Bengaluru's municipal wards, the frontend architecture treats **offline execution as a primary operational state**, rather than an exceptional failure mode.")
    lines.append("")

    lines.append("## 2. Comprehensive Architecture Topology")
    lines.append("The client-side topology is organized into six strictly decoupled architectural tiers:")
    lines.append("1. **Presentation & UI Component Tier:** Design system primitives, form controls, clinical status widgets, and accessible shell layouts.")
    lines.append("2. **Domain Feature Module Tier:** 30 domain-isolated feature modules encapsulating clinical workflows (Registration, Triage, Consultation, Dispensing, Lab, Inventory).")
    lines.append("3. **State Management Tier:** TanStack Query for server cache, Zustand for client UI state, and local Dexie / IndexedDB for durable persistence.")
    lines.append("4. **Data Access & API Gateway Client Tier:** Strongly-typed Axios / Fetch client with RS256 JWT interception, automatic token refresh, and request signing.")
    lines.append("5. **Offline Synchronization & Write-Ahead Log (WAL) Tier:** Background sync worker capturing mutations during outages, managing local SQLite / Dexie queues, and handling conflict resolution.")
    lines.append("6. **Hardware & Peripheral Bridge Tier:** Web Serial, Web USB, and ESC/POS thermal printer interfaces connecting barcode scanners, receipt printers, and medical analyzer devices.")
    lines.append("")

    lines.append("### 2.1 Logical Architecture Diagram")
    lines.append("```mermaid")
    lines.append("flowchart TD")
    lines.append("    subgraph PresentationTier [Presentation & UI Shell]")
    lines.append("        Shell[AppShell & Header] --> Nav[Dynamic RoleSidebar]")
    lines.append("        Shell --> RouteOutlet[React Router Viewport]")
    lines.append("        RouteOutlet --> ClinicalViews[Domain Clinical Modules]")
    lines.append("    end")
    lines.append("    subgraph StateTier [State Management Tier]")
    lines.append("        ClinicalViews --> Zustand[Client UI State Zustand]")
    lines.append("        ClinicalViews --> QueryCache[TanStack Server Query Cache]")
    lines.append("    end")
    lines.append("    subgraph StorageTier [Local Storage & Persistence]")
    lines.append("        QueryCache --> Dexie[IndexedDB / Dexie Database]")
    lines.append("        Dexie --> MutationQueue[Local WAL Mutation Queue]")
    lines.append("    end")
    lines.append("    subgraph SyncTier [Offline Sync Worker Tier]")
    lines.append("        MutationQueue --> SyncWorker[Web Worker Sync Engine]")
    lines.append("        SyncWorker --> ConflictEngine[Conflict Resolution Engine]")
    lines.append("    end")
    lines.append("    subgraph GatewayTier [API Gateway & Cloud]")
    lines.append("        SyncWorker -->|HTTPS / TLS 1.3| APIGateway[Cloud API Gateway]")
    lines.append("        APIGateway --> Microservices[Namma Clinic Backend Services]")
    lines.append("    end")
    lines.append("```")
    lines.append("")

    lines.append("### 2.2 Offline Synchronization Lifecycle")
    lines.append("```mermaid")
    lines.append("sequenceDiagram")
    lines.append("    autonumber")
    lines.append("    actor Clinician as Staff Nurse / Doctor")
    lines.append("    participant UI as Clinical Form UI")
    lines.append("    participant Cache as Dexie Local WAL")
    lines.append("    participant Worker as Sync Web Worker")
    lines.append("    participant Gateway as Cloud API Gateway")
    lines.append("    Clinician->>UI: Submit Clinical Encounter (Vitals / Rx)")
    lines.append("    UI->>Cache: Persist Mutation to 'pending_mutations' (IndexedDB)")
    lines.append("    UI-->>Clinician: Instant UI Confirmation (Optimistic Update)")
    lines.append("    Worker->>Cache: Poll for Un-synced Mutations")
    lines.append("    alt Network Online")
    lines.append("        Worker->>Gateway: POST /api/v1/sync/batch (Encrypted Payload)")
    lines.append("        Gateway-->>Worker: HTTP 200 OK (Acknowledge Transaction IDs)")
    lines.append("        Worker->>Cache: Mark Mutations as SYNCED (or Purge)")
    lines.append("    else Network Degraded / Offline")
    lines.append("        Worker->>Worker: Exponential Backoff (1s, 2s, 4s... max 60s)")
    lines.append("        UI->>Clinician: Display 'Offline: Queued for Sync' Badge")
    lines.append("    end")
    lines.append("```")
    lines.append("")

    lines.append("## 3. Module & Feature Boundaries")
    lines.append("The codebase follows strict architectural boundary rules. Cross-module direct imports are prohibited; modules interact exclusively through defined domain event contracts or shared core primitives.")
    lines.append("")

    for s in SCREENS:
        sid = s["id"]
        sname = s["name"]
        mod = s["module"]
        route = s["route"]
        role = s["primary_role"]
        desc = s["description"]
        apis = ", ".join(s["api_dependencies"])
        dbs = ", ".join(s["database_dependencies"])
        off = s["offline_support"]
        tid = s["test_id"]

        lines.append(f"### Architectural Specification for Screen: {sid} — {sname}")
        lines.append(f"- **Module Assignment:** `{mod}` | **Primary Route:** `{route}`")
        lines.append(f"- **Primary Role Entitlement:** `{role}` | **Offline Tier:** `{off}`")
        lines.append(f"- **API Gateways:** `{apis}` | **Underlying Entities:** `{dbs}`")
        lines.append(f"- **Automated Test Binding:** `{tid}`")
        lines.append("")
        lines.append("#### Boundary Invariants & Data Flow")
        lines.append(f"The `{sname}` screen governs the operational boundary for {desc}. Data flow initiates via TanStack Query hooks checking the local IndexedDB cache before making network dispatch. During offline periods, state is maintained locally with zero latency disruption to the clinical operator.")
        lines.append("")
        lines.append("#### Architectural Error Boundaries & Fallback")
        lines.append(f"Screen `{sid}` is wrapped in a dedicated React Error Boundary (`COMP-017 / COMP-019`). Unhandled component crashes or corrupt local IndexedDB schemas trigger an isolated error fallback without terminating the overall AppShell, allowing adjacent clinic workstations to remain operational.")
        lines.append("")
        lines.append("#### Documentation-Only TypeScript Architecture Definition")
        lines.append("```typescript")
        lines.append("// DOCUMENTATION-ONLY TYPESCRIPT")
        lines.append(f"export interface {sid.replace('-', '_')}_ArchitectureContract {{")
        lines.append(f"  screenId: '{sid}';")
        lines.append(f"  routePath: '{route}';")
        lines.append(f"  moduleDomain: '{mod}';")
        lines.append(f"  offlineCapability: '{off}';")
        lines.append(f"  primaryApiDependency: '{s['api_dependencies'][0] if s['api_dependencies'] else 'NONE'}';")
        lines.append(f"  localCacheTable: '{s['database_dependencies'][0] if s['database_dependencies'] else 'NONE'}';")
        lines.append("  maxStaleTimeMs: number; // 300000 ms (5 min default)")
        lines.append("  isCriticalClinicalFlow: boolean; // Triggers immediate WAL sync")
        lines.append("}")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## 4. Performance, Caching & Security Architecture")
    lines.append("1. **Bundle Budget:** Core application shell bundle size must remain under 180 KB gzipped. All domain modules are code-split and lazy-loaded on demand.")
    lines.append("2. **IndexedDB Compaction:** The local Dexie database automatically prunes completed clinical encounters older than 72 hours, preserving local disk quota on 64GB clinic mini-PCs.")
    lines.append("3. **Zero Trust Browser Security:** Content Security Policy (CSP) strictly disallows `unsafe-eval` and inline scripts. Tokens are stored in memory with encrypted refresh tokens bound to hardware fingerprints.")
    lines.append("4. **Telemetry & Telematics:** Client-side error telemetry logs are queued locally and batched to the central observability collector (`API-AUD-001`) during network reconnection.")
    lines.append("")

    content = "\n".join(lines)
    return write_fe_doc("02-frontend-architecture.md", content, min_substantive=2000)

if __name__ == "__main__":
    generate_doc()
