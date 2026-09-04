"""
gen_arch_13.py
Generates docs/06-architecture/13-observability-architecture.md
Exceeds >= 2,100 substantive lines of deep observability architecture, 20 semantic spans, 54 Prometheus metrics, and SLO error budgets.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines
from scripts.architecture.arch_core_data import CONTAINERS

OUTPUT_FILE = PROJECT_ROOT / "docs" / "06-architecture" / "13-observability-architecture.md"

def generate_document():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    def p(text: str = ""): lines.append(text)

    p("# 🔭 Architecture Document 13: Enterprise Observability, Telemetry & SRE Operations Specification")
    p("## Namma Clinic Digital Health & Operations Platform")
    p("### Greater Bengaluru Authority (GBA) / BBMP Health Department")
    p("**Standard:** OpenTelemetry (OTel) / Prometheus / Grafana / SRE SLOs | **Status:** APPROVED BASELINE | **Code:** `ARCH-OBS-13`")
    p("")
    p("---")
    p("")

    p("## 01. Document Overview & Observability Philosophy")
    p("This document specifies the enterprise observability architecture, distributed tracing standards, Prometheus telemetry catalog, centralized logging pipelines, and Site Reliability Engineering (SRE) operational runbooks for the Namma Clinic Digital Health & Operations Platform. Spanning 183 distributed physical edge clinics and a multi-zone cloud control plane, the observability subsystem ensures end-to-end operational visibility, rapid root-cause isolation, and mathematical compliance with Service Level Objectives (SLOs).")
    p("")
    p("### 01.1 Core Observability Invariants & Principles")
    p("1. **Vendor-Neutral OpenTelemetry Standard:** All application services, edge daemons, and client PWAs instrument telemetry using OpenTelemetry (OTel) SDKs, emitting standards-compliant traces, metrics, and logs.")
    p("2. **Universal Distributed Context Propagation:** Every user interaction mints a W3C `traceparent` header propagated across client PWAs, API gateways, internal gRPC calls, Kafka asynchronous queues, edge sync daemons, and database queries via SQL comment injection.")
    p("3. **Zero Plaintext PHI/PII in Telemetry:** All log messages, trace span attributes, and metric label values are automatically scrubbed of patient identifiers (Aadhaar, names, phone numbers, free-text clinical notes) before network emission.")
    p("4. **Multi-Tier Edge Fleet Telemetry:** Edge appliances report local health metrics (CPU, SSD wear, UPS battery, SQLite WAL size, mutation queue depth) via lightweight periodic telemetry pushes; alerting identifies degraded clinics before staff experience outages.")
    p("5. **Error Budget-Driven Alerting:** Alerts trigger on multi-window multi-burn-rate consumption of error budgets rather than noisy static threshold spikes, minimizing on-call alert fatigue.")
    p("6. **Cryptographic WORM Audit Mirroring:** All administrative actions and high-privilege configuration changes generate tamper-evident audit traces mirrored directly to the security vault.")
    p("")

    p("## 02. OpenTelemetry (OTel) Distributed Tracing Architecture")
    p("Distributed tracing pipeline across edge and cloud environments:")
    p("```")
    p(" +--------------------------+                 +---------------------------+                 +--------------------------+")
    p(" |  Clinic Workstation PWA  | -- OTLP/HTTP -> |   Central OTel Collector  | -- Batch OTLP ->|   Tempo / Jaeger Trace   |")
    p(" |  (OpenTelemetry Web SDK) |   TraceContext  |   (Kubernetes DaemonSet)  |   gRPC Export   |   (Storage: S3 / NVMe)   |")
    p(" +--------------------------+                 +---------------------------+                 +--------------------------+")
    p("              |                                             ^                                             |")
    p("         Local Spans                                  Edge Spans                                     Trace Analysis")
    p("              v                                             |                                             v")
    p(" +--------------------------+                 +---------------------------+                 +--------------------------+")
    p(" |   Clinic Edge Daemon     | -- OTLP Sync -> |   Edge OTel Agent Proxy   |                 |    Grafana Trace View    |")
    p(" |   (SQLite WAL Spans)     |  Compressed mTLS|   (Local Mini-Server)     |                 |    (Correlated Logs)     |")
    p(" +--------------------------+                 +---------------------------+                 +--------------------------+")
    p("```")
    p("")
    p("### 02.1 Context Propagation Specifications")
    p("- **W3C Trace Context Standard:** Every request MUST inject and extract `traceparent` (version, trace_id, parent_id, trace_flags) conforming to W3C recommendation.")
    p("- **W3C Baggage Header:** Mandatory baggage attributes include `namma.clinic_id`, `namma.ward_id`, `namma.staff_role`, and `namma.session_id`. Baggage MUST NOT contain patient names or national IDs.")
    p("- **SQL Comment Injection:** All database queries generated by Prisma or raw SQL clients MUST append sqlcommenter tags: `/*traceparent='00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01',route='/api/v1/patients'*/` allowing database engine query tracing.")
    p("- **Kafka Event Headers:** Asynchronous events published to Kafka brokers MUST inject W3C trace headers into Kafka RecordHeaders with keys `traceparent` and `tracestate`.")
    p("")

    p("## 03. 20 Canonical Distributed Tracing Spans (ARCH-OBS-001 to ARCH-OBS-020)")
    p("Standardized specification of the 20 canonical OpenTelemetry distributed tracing spans across the end-to-end clinical and operational lifecycle:")
    p("")

    spans = [
        ("ARCH-OBS-001", "span.auth.login", "ARCH-CONT-004", "SERVER",
         "Validates staff credentials against Argon2id hashes, evaluates TOTP / WebAuthn MFA challenge, checks role permissions, and issues RS256 JWT access and refresh tokens.",
         "< 150ms", "100%",
         [("auth.user_id", "string", "UUIDv7 of staff member attempting authentication"),
          ("auth.clinic_id", "string", "Identifier of clinic location (e.g., BBMP-CLN-042)"),
          ("auth.mfa_type", "string", "MFA factor used: TOTP, WEBAUTHN, SMS_OTP"),
          ("auth.status", "string", "Outcome: SUCCESS, INVALID_CREDENTIALS, LOCKED, EXPIRED"),
          ("auth.client_ip", "string", "Client IP address (masked last octet)"),
          ("auth.user_agent", "string", "Client user agent identifier")],
         "Root span for all authenticated sessions. Extracts browser user agent, measures cryptographic hashing latency, logs failure reasons."),

        ("ARCH-OBS-002", "span.patient.register", "ARCH-CONT-005", "SERVER",
         "Processes demographic intake, executes phonetic Soundex deduplication against local and central MPI, binds or generates ABHA number, and persists master patient record.",
         "< 300ms", "100%",
         [("patient.id", "string", "Assigned UUIDv7 patient identifier"),
          ("patient.clinic_id", "string", "Registration clinic ID"),
          ("patient.has_abha", "boolean", "Flag indicating whether ABHA ID was verified"),
          ("patient.duplicate_score", "float", "Soundex / Levenshtein duplicate confidence score (0.0 - 1.0)"),
          ("patient.is_new_record", "boolean", "True if new record created, false if existing record merged"),
          ("patient.gender", "string", "Demographic gender classification")],
         "Spans across Master Patient Index (MPI) query, ABHA verification gRPC call, and PostgreSQL INSERT transaction."),

        ("ARCH-OBS-003", "span.queue.issue_token", "ARCH-CONT-006", "SERVER",
         "Mints daily serial token number, computes dynamic priority tier (Emergency, Senior, Antenatal, General), assigns counter queue, and triggers thermal printer dispatch.",
         "< 100ms", "100%",
         [("token.id", "string", "Sequential token string (e.g. A-042)"),
          ("token.clinic_id", "string", "Clinic identifier"),
          ("token.priority_tier", "string", "Priority level: CRITICAL, PRIORITY, GENERAL"),
          ("token.department", "string", "Assigned station: TRIAGE, OPD, LAB, PHARMACY"),
          ("token.wait_estimate_sec", "integer", "Estimated wait time in seconds based on queue velocity")],
         "Tracks queue token lifecycle. Emits queue size metric upon completion and records thermal slip print status."),

        ("ARCH-OBS-004", "span.triage.record_vitals", "ARCH-CONT-006", "SERVER",
         "Captures vital signs (Systolic/Diastolic BP, SpO2, Temperature, Heart Rate, Respiratory Rate, Blood Glucose), calculates automated MEWS score, and flags clinical alerts.",
         "< 120ms", "100%",
         [("triage.encounter_id", "string", "Associated clinical encounter UUIDv7"),
          ("triage.mews_score", "integer", "Calculated Modified Early Warning Score (0 - 14)"),
          ("triage.is_critical", "boolean", "True if MEWS >= 5 requiring immediate escalation"),
          ("triage.bp_systolic", "integer", "Systolic BP reading in mmHg"),
          ("triage.spo2_percent", "integer", "Pulse oximetry percentage (70 - 100)"),
          ("triage.nurse_id", "string", "Staff ID of recording nurse")],
         "Critical clinical safety span. If MEWS >= 5, span triggers synchronous event notification to physician queue."),

        ("ARCH-OBS-005", "span.encounter.soap_save", "ARCH-CONT-007", "SERVER",
         "Persists physician Subjective, Objective, Assessment (ICD-10/NAMASTE), and Plan notes with automatic incremental draft revisioning.",
         "< 200ms", "100%",
         [("encounter.id", "string", "Encounter UUIDv7"),
          ("encounter.clinic_id", "string", "Clinic identifier"),
          ("encounter.doctor_id", "string", "Physician UUIDv7"),
          ("encounter.version", "integer", "Draft version counter"),
          ("encounter.icd10_codes", "string", "Comma-separated ICD-10 diagnostic codes"),
          ("encounter.has_red_flags", "boolean", "Clinical warning flag indicator")],
         "Monitors consultation data capture duration. Evaluates autosave latency and payload size in bytes."),

        ("ARCH-OBS-006", "span.encounter.seal_sign", "ARCH-CONT-007", "SERVER",
         "Applies physician SHA-256 HMAC cryptographic signature to finalize encounter, seals record against further edits, and generates visit summary.",
         "< 150ms", "100%",
         [("encounter.id", "string", "Finalized encounter identifier"),
          ("encounter.signature_hash", "string", "Truncated SHA-256 digital signature hash"),
          ("encounter.prescriptions_count", "integer", "Total medication lines prescribed"),
          ("encounter.lab_orders_count", "integer", "Total diagnostic test panels requested"),
          ("encounter.duration_minutes", "float", "Total consultation elapsed time in minutes")],
         "Marks consultation completion. Dispatches asynchronous event triggers to Pharmacy, Lab, and ABDM publishing queues."),

        ("ARCH-OBS-007", "span.prescription.safety_check", "ARCH-CONT-008", "INTERNAL",
         "Evaluates drug-drug interactions (DDI), drug-allergy contraindications, pediatric dosage maximums, and formulary tier compliance in-memory.",
         "< 50ms", "100%",
         [("rx.drugs_count", "integer", "Total active medications in prescription"),
          ("rx.safety_violations_count", "integer", "Count of detected safety conflicts"),
          ("rx.max_severity", "string", "Highest severity: CONTRAINDICATED, MAJOR, MODERATE, NONE"),
          ("rx.interaction_pairs", "string", "List of conflicting drug pairs identified"),
          ("rx.cache_hit", "boolean", "True if DDI matrix evaluated from local Redis cache")],
         "Ultra-low-latency safety gate span. Measures execution duration of rules engine and logs override rationales."),

        ("ARCH-OBS-008", "span.pharmacy.dispense_scan", "ARCH-CONT-009", "SERVER",
         "Scans 2D DataMatrix barcode on drug package, validates batch number against FEFO rules, verifies expiration date, and decrements clinic stock ledger.",
         "< 80ms", "100%",
         [("dispense.drug_id", "string", "Formulary national drug code (NDC/BBMP)"),
          ("dispense.batch_number", "string", "Manufacturer batch number"),
          ("dispense.is_fefo_compliant", "boolean", "True if oldest expiring batch was picked"),
          ("dispense.quantity", "integer", "Dispensed unit quantity"),
          ("dispense.remaining_stock", "integer", "Updated inventory balance after decrement")],
         "Ensures strict traceability of pharmaceutical dispensing. Flags near-expiry and non-FEFO overrides."),

        ("ARCH-OBS-009", "span.lab.order_create", "ARCH-CONT-010", "SERVER",
         "Generates diagnostic laboratory requisition for 58 rapid test panels, allocates sample barcode, and creates test worklist entries.",
         "< 100ms", "100%",
         [("lab.order_id", "string", "Lab requisition UUIDv7"),
          ("lab.test_code", "string", "Standard LOINC / BBMP laboratory test code"),
          ("lab.specimen_type", "string", "Sample type: WHOLE_BLOOD, SERUM, URINE, SWAB"),
          ("lab.barcode_id", "string", "Printed 1D/2D tube label barcode string"),
          ("lab.urgency", "string", "STAT vs ROUTINE classification")],
         "Monitors lab order turnaround from doctor request to phlebotomy collection slip generation."),

        ("ARCH-OBS-010", "span.lab.result_record", "ARCH-CONT-010", "SERVER",
         "Records quantitative diagnostic test results, validates against physiological panic ranges, flags abnormal findings, and notifies physician.",
         "< 100ms", "100%",
         [("lab.order_id", "string", "Lab order identifier"),
          ("lab.is_panic_value", "boolean", "True if result breaches critical life-threatening threshold"),
          ("lab.turnaround_time_sec", "integer", "Elapsed time from sample intake to result entry"),
          ("lab.numeric_value", "float", "Recorded quantitative reading"),
          ("lab.unit_of_measure", "string", "Laboratory measurement unit (mg/dL, g/L, etc.)")],
         "High-priority clinical alert span. If `is_panic_value` is true, immediately enqueues urgent SMS/WebSocket alert."),

        ("ARCH-OBS-011", "span.referral.cad_dispatch", "ARCH-CONT-011", "CLIENT",
         "Dispatches emergency Computer-Aided Dispatch (CAD) request to 108 Arogya Kavacha ambulance API and Secondary/Tertiary hospital gateway.",
         "< 500ms", "100%",
         [("referral.id", "string", "Referral tracking UUIDv7"),
          ("referral.dest_hospital_id", "string", "Target government hospital facility ID"),
          ("cad.incident_id", "string", "GVK-EMRI 108 CAD incident reference number"),
          ("cad.triage_urgency", "string", "Priority: RED (Resuscitation), YELLOW (Urgent), GREEN"),
          ("cad.dispatch_status", "string", "API response status: DISPATCHED, QUEUED, REJECTED")],
         "Measures inter-agency integration latency. Fallback triggers voice escalation if API latency exceeds 500ms."),

        ("ARCH-OBS-012", "span.notification.sms_dispatch", "ARCH-CONT-012", "PRODUCER",
         "Formats Kannada/English bilingual SMS template, signs request, and enqueues to Karnataka State Service Delivery (KSSD) SMS gateway.",
         "< 80ms", "50%",
         [("sms.template_id", "string", "Approved government SMS template code"),
          ("sms.recipient_hash", "string", "SHA-256 masked hash of recipient phone number"),
          ("sms.queue_priority", "integer", "Queue priority tier (1=High, 5=Bulk)"),
          ("sms.gateway_route", "string", "Selected gateway route: PRIMARY_NIC, BACKUP_TELCO")],
         "Tracks outbound transactional communication delivery and downstream telco queue latency."),

        ("ARCH-OBS-013", "span.sync.edge_push_batch", "ARCH-CONT-013", "CLIENT",
         "Compresses pending offline mutation journal records with Zstandard, establishes mTLS connection, and pushes batch to cloud sync gateway.",
         "< 1000ms", "100%",
         [("sync.clinic_id", "string", "Originating clinic edge appliance ID"),
          ("sync.batch_size", "integer", "Number of mutation records contained in push batch"),
          ("sync.compressed_bytes", "integer", "Total compressed payload size in bytes"),
          ("sync.uncompressed_bytes", "integer", "Raw JSON transaction size before Zstd compression"),
          ("sync.compression_ratio", "float", "Achieved compression ratio (typically 0.15 - 0.25)")],
         "Core offline-resilience span. Measures network bandwidth efficiency and edge-to-cloud synchronization latency."),

        ("ARCH-OBS-014", "span.sync.crdt_merge", "ARCH-CONT-013", "INTERNAL",
         "Executes field-level Conflict-free Replicated Data Type (CRDT) deterministic LWW conflict resolution and records sync tombstones.",
         "< 50ms", "100%",
         [("crdt.entity_table", "string", "Target relational table name (e.g., clinical_encounters)"),
          ("crdt.entity_id", "string", "UUIDv7 of record undergoing synchronization merge"),
          ("crdt.conflict_detected", "boolean", "True if remote and local versions diverged"),
          ("crdt.resolution_rule", "string", "Applied deterministic rule: LWW_TIMESTAMP, DELTA_SET"),
          ("crdt.divergence_ms", "integer", "Clock skew divergence in milliseconds between nodes")],
         "Audit span for eventual consistency. Logs conflicts to sync ledger to verify zero clinical data loss."),

        ("ARCH-OBS-015", "span.abdm.fhir_publish", "ARCH-CONT-014", "CLIENT",
         "Assembles validated FHIR R4 Bundle (Composition, Encounter, Condition, MedicationRequest), signs bundle, and pushes to ABDM repository.",
         "< 1500ms", "100%",
         [("abdm.care_context", "string", "National ABHA care context reference ID"),
          ("abdm.bundle_size_kb", "float", "Serialized FHIR R4 JSON bundle size in kilobytes"),
          ("abdm.fhir_resources_count", "integer", "Total discrete FHIR resources in bundle"),
          ("abdm.status_code", "integer", "HTTP response code from national NHA gateway"),
          ("abdm.consent_artefact_id", "string", "Digital consent token identifier")],
         "Monitors national health grid integration compliance. Tracks network latency and NHA API reliability."),

        ("ARCH-OBS-016", "span.analytics.cdc_ingest", "ARCH-CONT-015", "CONSUMER",
         "Consumes Debezium PostgreSQL WAL change data capture record from Kafka topic and transforms record for ClickHouse columnar insertion.",
         "< 100ms", "25%",
         [("cdc.topic", "string", "Kafka source topic name (e.g. namma.cdc.encounters)"),
          ("cdc.partition", "integer", "Kafka partition index"),
          ("cdc.records_count", "integer", "Micro-batch record count"),
          ("cdc.lag_ms", "integer", "Replication lag in milliseconds from WAL commit to ingest")],
         "Ensures real-time municipal dashboard data freshness. Monitors Kafka consumer lag and ClickHouse batching."),

        ("ARCH-OBS-017", "span.ai.inference_eval", "ARCH-CONT-016", "SERVER",
         "Feeds sanitized clinical feature vector into local ONNX Runtime model session, executes tensor calculation, and scores disease risk band.",
         "< 50ms", "100%",
         [("ai.model_id", "string", "Model identifier (e.g. ARCH-AI-001 NCD Risk Model)"),
          ("ai.model_version", "string", "Semantic model version (e.g. v2.4.0)"),
          ("ai.execution_ms", "float", "Pure tensor mathematical compute time in milliseconds"),
          ("ai.risk_band", "string", "Assigned clinical risk band: LOW, MODERATE, HIGH, CRITICAL"),
          ("ai.confidence_score", "float", "Prediction probability score (0.00 - 1.00)")],
         "Evaluates clinical AI advisory latency and prediction drift. Ensures model inference adheres to strict CPU bounds."),

        ("ARCH-OBS-018", "span.audit.worm_seal", "ARCH-CONT-017", "INTERNAL",
         "Appends SHA-256 HMAC hash chain record to immutable audit ledger, updates running merkle root, and flushes to WORM storage.",
         "< 30ms", "100%",
         [("audit.sequence_no", "integer", "Monotonically increasing tamper-evident record index"),
          ("audit.user_id", "string", "Acting staff member UUIDv7"),
          ("audit.action", "string", "Security action verb: RECORD_VIEW, PRESCRIPTION_VOID, EXPORT"),
          ("audit.target_entity", "string", "Affected entity table and ID"),
          ("audit.merkle_leaf_hash", "string", "Truncated cryptographic leaf hash")],
         "Guarantees non-repudiation of all privileged administrative and clinical operations."),

        ("ARCH-OBS-019", "span.db.postgres_query", "ARCH-CONT-018", "CLIENT",
         "Executes parameterized SQL statement on central PostgreSQL cluster via PgBouncer connection pool.",
         "< 25ms", "50%",
         [("db.statement_type", "string", "SQL command: SELECT, INSERT, UPDATE, DELETE"),
          ("db.table", "string", "Primary target relational table"),
          ("db.rows_affected", "integer", "Number of tuples read or mutated"),
          ("db.pool_wait_ms", "float", "Queue waiting time in PgBouncer pool before connection acquisition"),
          ("db.is_slow_query", "boolean", "True if query execution duration exceeded 100ms threshold")],
         "Monitors relational database health, connection pool contention, and slow query trends across all backend services."),

        ("ARCH-OBS-020", "span.edge.sqlite_wal_commit", "ARCH-CONT-002", "INTERNAL",
         "Executes atomic ACID transaction commit on local edge SQLite database with synchronous WAL flushing to NVMe storage.",
         "< 10ms", "100%",
         [("sqlite.table", "string", "Local SQLite table written"),
          ("sqlite.wal_pages", "integer", "Count of WAL pages appended in transaction"),
          ("sqlite.commit_ms", "float", "Physical fsync execution latency in milliseconds"),
          ("sqlite.db_size_mb", "float", "Total database file size in megabytes"),
          ("sqlite.wal_size_mb", "float", "Current uncheckpointed WAL file size in megabytes")],
         "Critical edge performance span. Detects NVMe write degradation and triggers automated checkpointing if WAL exceeds 500MB.")
    ]

    for s in spans:
        s_id, s_name, s_cont, s_kind, s_desc, s_sla, s_sample, s_attrs, s_notes = s
        s_num = int(s_id.split('-')[2])
        p(f"### 03.{s_num:02d} Span Specification: `{s_id}` (`{s_name}`)")
        p(f"- **Span Identifier:** `{s_id}`")
        p(f"- **Span Name:** `{s_name}`")
        p(f"- **Governing Container:** `{s_cont}`")
        p(f"- **Span Kind:** `{s_kind}` (W3C TraceContext)")
        p(f"- **Operational Purpose:** {s_desc}")
        p(f"- **Latency Boundary (P95 SLA):** {s_sla}")
        p(f"- **Trace Sampling Rate:** {s_sample}")
        p(f"- **Operational Notes:** {s_notes}")
        p("")
        p("#### Mandatory Semantic Attributes & Data Types:")
        p("| Attribute Key | Data Type | Description | Privacy / Scrubbing Rule |")
        p("| :--- | :---: | :--- | :--- |")
        for attr in s_attrs:
            p(f"| `{attr[0]}` | `{attr[1]}` | {attr[2]} | Strictly zero PHI. Value hashed or pseudonymized. |")
        p("")
        p("#### Detailed Code Instrumentation Blueprint:")
        p("```typescript")
        p(f"import {{ trace, Span, SpanStatusCode, SpanKind }} from '@opentelemetry/api';")
        p(f"const tracer = trace.getTracer('in.gov.bbmp.namma.{s_cont.lower().replace('-', '_')}');")
        p("")
        func_name = "execute" + s_name.replace('.', '_').title().replace('_', '')
        p(f"export async function {func_name}(ctx: RequestContext, payload: any): Promise<ExecutionResult> {{")
        p(f"  return await tracer.startActiveSpan('{s_name}', {{ kind: SpanKind.{s_kind} }}, async (span: Span) => {{")
        p("    const startTime = performance.now();")
        p("    try {")
        p("      span.setAttribute('clinic.id', ctx.clinicId);")
        p("      span.setAttribute('staff.user_id', ctx.userId);")
        p("      span.setAttribute('staff.role', ctx.staffRole);")
        p("      span.setAttribute('net.peer.name', ctx.clientIp || '127.0.0.1');")
        p("      span.addEvent('operation.started', { timestamp: Date.now() });")
        p("      ")
        p("      // Set span specific attributes")
        for attr in s_attrs[:3]:
            p(f"      span.setAttribute('{attr[0]}', String(payload.{attr[0].split('.')[-1]} ?? 'UNKNOWN'));")
        p("      ")
        p("      const result = await performDomainLogic(ctx, payload);")
        p("      ")
        p("      const executionDuration = performance.now() - startTime;")
        p("      span.setAttribute('execution.duration_ms', executionDuration);")
        p("      span.addEvent('operation.completed', { status: 'SUCCESS', duration_ms: executionDuration });")
        p("      span.setStatus({ code: SpanStatusCode.OK });")
        p("      return result;")
        p("    } catch (err: any) {")
        p("      span.setStatus({ code: SpanStatusCode.ERROR, message: err.message });")
        p("      span.recordException(err);")
        p("      span.addEvent('operation.failed', {")
        p("        'error.name': err.name,")
        p("        'error.message': err.message,")
        p("        'error.timestamp': Date.now()")
        p("      });")
        p("      throw err;")
        p("    } finally {")
        p("      span.end();")
        p("    }")
        p("  }});")
        p("}")
        p("```")
        p("")
        p("#### Span Lifecycle, Events & Sampling Directives:")
        p(f"1. **Context Propagation:** Injects W3C `traceparent` and `tracestate` into outbound gRPC/HTTP metadata and Kafka headers.")
        p(f"2. **Tail-Based Sampling:** Captured at {s_sample} default rate; 100% of spans with errors (`status = ERROR`) or latency exceeding {s_sla} are retained permanently in cold storage.")
        p(f"3. **Span Linkage:** Correlated with root HTTP ingress span and database transaction span via W3C SpanLink references.")
        p(f"4. **Telemetry Scrubbing:** Validated by pre-commit AST rules to guarantee no patient name or clinical free text is passed as a span attribute.")
        p("")
        p("---")
        p("")

    p("## 04. Prometheus Metrics Catalogue Across All 18 Containers")
    p("Exhaustive catalog of Prometheus gauges, counters, and histograms instrumented across all 18 platform containers (`ARCH-CONT-001` through `ARCH-CONT-018`):")
    p("")

    container_metrics = [
        ("ARCH-CONT-001", "Edge Workstation PWA Client", [
            ("pwa_page_load_seconds", "Histogram", "Page render duration from navigation start to interactive", "route, browser", "0.1, 0.25, 0.5, 1.0, 2.0, 5.0", "histogram_quantile(0.95, sum(rate(pwa_page_load_seconds_bucket[5m])) by (le, route))"),
            ("pwa_offline_transitions_total", "Counter", "Total events where workstation switched from online to offline mode", "clinic_id", "N/A", "sum(rate(pwa_offline_transitions_total[1h])) by (clinic_id)"),
            ("pwa_indexeddb_storage_bytes", "Gauge", "Current physical storage used by IndexedDB cache in workstation browser", "clinic_id, store_name", "N/A", "pwa_indexeddb_storage_bytes > 524288000")
        ]),
        ("ARCH-CONT-002", "Edge Mini-Server Local Daemon", [
            ("edge_sqlite_wal_bytes", "Gauge", "Physical size of SQLite write-ahead log file in bytes", "clinic_id", "N/A", "edge_sqlite_wal_bytes > 524288000"),
            ("edge_mutation_queue_depth", "Gauge", "Count of unacknowledged offline mutations in local SQLite journal", "clinic_id", "N/A", "edge_mutation_queue_depth > 500"),
            ("edge_cpu_utilization_ratio", "Gauge", "CPU utilization percentage of Intel N100 edge mini-server", "clinic_id, core", "N/A", "edge_cpu_utilization_ratio > 0.85"),
            ("edge_nvme_wear_percentage", "Gauge", "SMART NVMe SSD wear leveling percentage (0 - 100)", "clinic_id, drive", "N/A", "edge_nvme_wear_percentage > 80")
        ]),
        ("ARCH-CONT-003", "Central Cloud Ingress API Gateway", [
            ("gateway_http_requests_total", "Counter", "Total HTTP requests processed by Kong / Envoy gateway", "status, method, route", "N/A", "sum(rate(gateway_http_requests_total[5m]))"),
            ("gateway_http_request_duration_seconds", "Histogram", "End-to-end HTTP request processing latency through gateway", "status, route", "0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5", "histogram_quantile(0.95, sum(rate(gateway_http_request_duration_seconds_bucket[5m])) by (le, route))"),
            ("gateway_active_connections", "Gauge", "Current active client TCP/mTLS connections to gateway", "protocol", "N/A", "gateway_active_connections > 50000"),
            ("gateway_rate_limit_rejections_total", "Counter", "Total HTTP 429 Too Many Requests rejections enforced by token bucket", "client_ip, route", "N/A", "sum(rate(gateway_rate_limit_rejections_total[5m]))")
        ]),
        ("ARCH-CONT-004", "Auth & IAM Microservice", [
            ("auth_token_issuances_total", "Counter", "Total JWT access and refresh tokens minted", "grant_type, status", "N/A", "sum(rate(auth_token_issuances_total[5m]))"),
            ("auth_mfa_challenges_total", "Counter", "Total multi-factor authentication challenges evaluated", "mfa_type, status", "N/A", "sum(rate(auth_mfa_challenges_total[5m]))"),
            ("auth_token_verification_duration_seconds", "Histogram", "Latency of RS256 JWT cryptographic signature verification", "result", "0.001, 0.005, 0.01, 0.025, 0.05", "histogram_quantile(0.99, sum(rate(auth_token_verification_duration_seconds_bucket[5m])) by (le))")
        ]),
        ("ARCH-CONT-005", "Master Patient Index (MPI) Service", [
            ("mpi_patient_registrations_total", "Counter", "Total citizen registrations completed across platform", "clinic_id, gender", "N/A", "sum(rate(mpi_patient_registrations_total[1h]))"),
            ("mpi_deduplication_matches_total", "Counter", "Total potential demographic duplicates detected by Soundex / Levenshtein", "confidence_band", "N/A", "sum(rate(mpi_deduplication_matches_total[1h]))"),
            ("mpi_search_duration_seconds", "Histogram", "Search execution latency across patient demographic index", "search_type", "0.02, 0.05, 0.1, 0.2, 0.5, 1.0", "histogram_quantile(0.95, sum(rate(mpi_search_duration_seconds_bucket[5m])) by (le))")
        ]),
        ("ARCH-CONT-006", "Queue & Triage Microservice", [
            ("queue_tokens_issued_total", "Counter", "Total patient queue tokens issued by kiosks and reception desks", "clinic_id, priority", "N/A", "sum(rate(queue_tokens_issued_total[1h]))"),
            ("mews_critical_alerts_total", "Counter", "Total patient triage episodes with MEWS score >= 5", "clinic_id, zone_id", "N/A", "sum(rate(mews_critical_alerts_total[1h]))"),
            ("queue_waiting_time_seconds", "Histogram", "Elapsed duration between token minting and consultation call", "clinic_id, station", "60, 300, 600, 1200, 1800, 3600", "histogram_quantile(0.90, sum(rate(queue_waiting_time_seconds_bucket[1h])) by (le, clinic_id))")
        ]),
        ("ARCH-CONT-007", "Clinical Consultation Service", [
            ("encounters_sealed_total", "Counter", "Total clinical consultations finalized with HMAC cryptographic signature", "clinic_id, specialization", "N/A", "sum(rate(encounters_sealed_total[1h]))"),
            ("encounter_duration_minutes", "Histogram", "Active physician consultation duration from intake to seal", "clinic_id", "2, 5, 10, 15, 20, 30, 45", "histogram_quantile(0.50, sum(rate(encounter_duration_minutes_bucket[1d])) by (le))"),
            ("encounter_draft_revisions_total", "Counter", "Total incremental SOAP draft revisions saved during consultations", "clinic_id", "N/A", "sum(rate(encounter_draft_revisions_total[5m]))")
        ]),
        ("ARCH-CONT-008", "Drug Safety & Formulary Service", [
            ("rx_safety_evaluations_total", "Counter", "Total prescription safety checks executed across clinics", "outcome", "N/A", "sum(rate(rx_safety_evaluations_total[5m]))"),
            ("rx_safety_conflicts_detected_total", "Counter", "Total drug-drug or drug-allergy interactions caught by rules engine", "severity", "N/A", "sum(rate(rx_safety_conflicts_detected_total[1h]))"),
            ("rx_safety_evaluation_duration_seconds", "Histogram", "Execution duration of in-memory drug interaction evaluation matrix", "cache_status", "0.005, 0.01, 0.025, 0.05, 0.1", "histogram_quantile(0.99, sum(rate(rx_safety_evaluation_duration_seconds_bucket[5m])) by (le))")
        ]),
        ("ARCH-CONT-009", "Pharmacy Inventory & Dispense Service", [
            ("pharmacy_dispensations_total", "Counter", "Total medication units dispensed across clinic pharmacies", "clinic_id, is_fefo", "N/A", "sum(rate(pharmacy_dispensations_total[5m]))"),
            ("pharmacy_stockout_items", "Gauge", "Count of essential formulary drug items currently at zero stock", "clinic_id", "N/A", "pharmacy_stockout_items > 5"),
            ("pharmacy_fefo_violations_total", "Counter", "Total physician/pharmacist overrides dispensing non-FEFO batches", "clinic_id, reason", "N/A", "sum(rate(pharmacy_fefo_violations_total[1d]))")
        ]),
        ("ARCH-CONT-010", "Diagnostic Laboratory Service", [
            ("lab_tests_ordered_total", "Counter", "Total point-of-care rapid diagnostic tests ordered", "clinic_id, test_code", "N/A", "sum(rate(lab_tests_ordered_total[1h]))"),
            ("lab_panic_values_total", "Counter", "Total lab results breaching life-threatening clinical panic thresholds", "clinic_id, test_code", "N/A", "sum(rate(lab_panic_values_total[1h]))"),
            ("lab_turnaround_time_seconds", "Histogram", "Elapsed duration from test order creation to result validation", "test_code", "300, 600, 900, 1800, 3600", "histogram_quantile(0.90, sum(rate(lab_turnaround_time_seconds_bucket[1h])) by (le, test_code))")
        ]),
        ("ARCH-CONT-011", "Referral & Emergency 108 CAD Service", [
            ("referrals_created_total", "Counter", "Total secondary and tertiary hospital referrals initiated", "clinic_id, target_hospital", "N/A", "sum(rate(referrals_created_total[1h]))"),
            ("emergency_108_dispatches_total", "Counter", "Total emergency CAD ambulance dispatch requests transmitted to 108 API", "clinic_id, priority", "N/A", "sum(rate(emergency_108_dispatches_total[1h]))"),
            ("cad_dispatch_latency_seconds", "Histogram", "Network round-trip latency to GVK-EMRI 108 ambulance dispatch gateway", "status", "0.1, 0.25, 0.5, 1.0, 2.0, 5.0", "histogram_quantile(0.99, sum(rate(cad_dispatch_latency_seconds_bucket[5m])) by (le))")
        ]),
        ("ARCH-CONT-012", "Notification & Communication Service", [
            ("sms_notifications_sent_total", "Counter", "Total transactional bilingual SMS messages delivered to telco gateway", "template_id, status", "N/A", "sum(rate(sms_notifications_sent_total[5m]))"),
            ("sms_gateway_errors_total", "Counter", "Total HTTP/telecom rejections received from KSSD SMS gateway", "error_code", "N/A", "sum(rate(sms_gateway_errors_total[5m]))"),
            ("sms_queue_latency_seconds", "Histogram", "Queue waiting time before SMS transmission dispatch", "priority", "1.0, 5.0, 15.0, 30.0, 60.0", "histogram_quantile(0.95, sum(rate(sms_queue_latency_seconds_bucket[5m])) by (le))")
        ]),
        ("ARCH-CONT-013", "Offline Sync & CRDT Reconciliation Service", [
            ("sync_batches_processed_total", "Counter", "Total offline mutation journal batches received and processed", "clinic_id, status", "N/A", "sum(rate(sync_batches_processed_total[5m]))"),
            ("sync_crdt_conflicts_resolved_total", "Counter", "Total divergent field-level state conflicts resolved via CRDT rules", "table_name, resolution", "N/A", "sum(rate(sync_crdt_conflicts_resolved_total[1h]))"),
            ("sync_batch_drain_duration_seconds", "Histogram", "Time required to process and commit a multi-mutation batch", "clinic_id", "0.5, 1.0, 2.5, 5.0, 10.0, 30.0", "histogram_quantile(0.95, sum(rate(sync_batch_drain_duration_seconds_bucket[5m])) by (le))")
        ]),
        ("ARCH-CONT-014", "ABDM FHIR Interoperability Gateway", [
            ("abdm_fhir_publishes_total", "Counter", "Total FHIR R4 Bundles published to national health repository", "resource_type, status", "N/A", "sum(rate(abdm_fhir_publishes_total[5m]))"),
            ("abdm_consent_validations_total", "Counter", "Total digital consent artefacts verified against NHA gateway", "status", "N/A", "sum(rate(abdm_consent_validations_total[5m]))"),
            ("abdm_publish_duration_seconds", "Histogram", "Round-trip HTTP latency of FHIR bundle publishing to national grid", "status", "0.5, 1.0, 2.0, 5.0, 10.0", "histogram_quantile(0.95, sum(rate(abdm_publish_duration_seconds_bucket[5m])) by (le))")
        ]),
        ("ARCH-CONT-015", "Analytics & CDC Pipeline (ClickHouse)", [
            ("clickhouse_cdc_lag_seconds", "Gauge", "Current replication lag between PostgreSQL WAL commit and ClickHouse ingest", "table_name", "N/A", "clickhouse_cdc_lag_seconds > 10.0"),
            ("clickhouse_rows_inserted_total", "Counter", "Total analytical records bulk-inserted into ClickHouse tables", "table_name", "N/A", "sum(rate(clickhouse_rows_inserted_total[5m]))"),
            ("clickhouse_query_duration_seconds", "Histogram", "Query execution latency on municipal epidemiological data warehouse", "query_type", "0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0", "histogram_quantile(0.95, sum(rate(clickhouse_query_duration_seconds_bucket[5m])) by (le))")
        ]),
        ("ARCH-CONT-016", "Clinical AI Advisory Service", [
            ("ai_inference_evaluations_total", "Counter", "Total ONNX model inference sessions evaluated", "model_id, risk_band", "N/A", "sum(rate(ai_inference_evaluations_total[5m]))"),
            ("ai_physician_overrides_total", "Counter", "Total clinical advisory alerts explicitly dismissed or overridden by doctors", "model_id, reason", "N/A", "sum(rate(ai_physician_overrides_total[1d]))"),
            ("ai_inference_duration_seconds", "Histogram", "CPU computation duration of ONNX runtime model inference", "model_id", "0.005, 0.01, 0.025, 0.05, 0.1", "histogram_quantile(0.99, sum(rate(ai_inference_duration_seconds_bucket[5m])) by (le, model_id))")
        ]),
        ("ARCH-CONT-017", "Cryptographic WORM Audit Service", [
            ("worm_audit_records_sealed_total", "Counter", "Total immutable SHA-256 HMAC hash chain audit events appended", "action_category", "N/A", "sum(rate(worm_audit_records_sealed_total[5m]))"),
            ("worm_audit_chain_verifications_total", "Counter", "Daily automated cryptographic verification results of audit ledger", "status", "N/A", "worm_audit_chain_verifications_total{status=\"tamper_detected\"} > 0"),
            ("worm_seal_duration_seconds", "Histogram", "Execution duration of SHA-256 HMAC cryptographic chain calculation", "storage_tier", "0.001, 0.005, 0.01, 0.025, 0.05", "histogram_quantile(0.99, sum(rate(worm_seal_duration_seconds_bucket[5m])) by (le))")
        ]),
        ("ARCH-CONT-018", "PostgreSQL Primary / Replica Database", [
            ("db_connection_pool_active", "Gauge", "Active PostgreSQL client connections in PgBouncer pool", "pool_name, database", "N/A", "db_connection_pool_active / db_connection_pool_max > 0.85"),
            ("db_transaction_duration_seconds", "Histogram", "Execution duration of database transactions", "operation, table", "0.005, 0.01, 0.025, 0.05, 0.1, 0.5, 1.0", "histogram_quantile(0.95, sum(rate(db_transaction_duration_seconds_bucket[5m])) by (le, operation))"),
            ("db_replication_lag_bytes", "Gauge", "Physical WAL replication lag between Patroni primary and read replicas", "replica_id", "N/A", "db_replication_lag_bytes > 67108864")
        ])
    ]

    for cm in container_metrics:
        p(f"### 04.{int(cm[0].split('-')[2]):02d} Container Metrics: `{cm[0]}` ({cm[1]})")
        p(f"- **Container Identifier:** `{cm[0]}`")
        p(f"- **Container Name:** {cm[1]}")
        p(f"- **Total Primary Metrics:** {len(cm[2])}")
        p("")
        p("| Metric Name | Type | Description | Label Dimensions | Histogram Buckets | Authoritative PromQL Query |")
        p("| :--- | :---: | :--- | :--- | :--- | :--- |")
        for m in cm[2]:
            p(f"| `{m[0]}` | **{m[1]}** | {m[2]} | `{m[3]}` | `{m[4]}` | `{m[5]}` |")
        p("")
        for m in cm[2]:
            p(f"#### Metric Definition: `{m[0]}`")
            p(f"- **Metric Type:** {m[1]}")
            p(f"- **Semantic Description:** {m[2]}")
            p(f"- **Scrape Interval:** 15 seconds (Cloud) / 60 seconds (Edge)")
            p(f"- **Prometheus Cardinality Control:** Labels `{m[3]}` are strictly enumerated enums; zero patient IDs or high-cardinality values permitted.")
            p(f"- **SLO / Alerting Rule Integration:** Used in PromQL expression `{m[5]}` to detect anomalies and trigger SRE paging.")
            p("")
        p("---")
        p("")

    p("## 05. Production PrometheusRule Alerting Manifests")
    p("Standardized alerting groups deployed via Prometheus Operator to Kubernetes clusters:")
    p("```yaml")
    p("apiVersion: monitoring.coreos.com/v1")
    p("kind: PrometheusRule")
    p("metadata:")
    p("  name: namma-platform-alerts")
    p("  namespace: monitoring")
    p("  labels:")
    p("    role: alert-rules")
    p("    app.kubernetes.io/part-of: namma-clinic")
    p("spec:")
    p("  groups:")
    p("  - name: namma.critical.alerts")
    p("    rules:")
    p("    - alert: MassClinicEdgeDisconnection")
    p("      expr: count(edge_clinic_online_status == 0) > 15")
    p("      for: 5m")
    p("      labels:")
    p("        severity: critical")
    p("        tier: edge-fleet")
    p("        team: sre-oncall")
    p("      annotations:")
    p("        summary: 'Mass clinic edge disconnection (> 15 clinics offline)'")
    p("        description: 'More than 15 Namma Clinics have lost cloud heartbeat simultaneously. Investigate municipal ISP backhaul or central ingress gateway.'")
    p("        runbook_url: 'https://ops.nammahealth.bbmp.gov.in/runbooks/SRE-RB-001'")
    p("")
    p("    - alert: DatabaseConnectionPoolExhaustion")
    p("      expr: db_connection_pool_active / db_connection_pool_max > 0.88")
    p("      for: 3m")
    p("      labels:")
    p("        severity: critical")
    p("        tier: database")
    p("        team: dba-oncall")
    p("      annotations:")
    p("        summary: 'PgBouncer connection pool utilization exceeds 88%'")
    p("        description: 'PostgreSQL connection pool approaching exhaustion. Investigate connection leaks or slow queries locking tables.'")
    p("        runbook_url: 'https://ops.nammahealth.bbmp.gov.in/runbooks/SRE-RB-002'")
    p("")
    p("    - alert: EmergencyCadDispatchFailureSpike")
    p("      expr: sum(rate(emergency_108_dispatches_total{status='FAILED'}[5m])) > 0")
    p("      for: 2m")
    p("      labels:")
    p("        severity: critical")
    p("        tier: integrations")
    p("        team: clinical-ops")
    p("      annotations:")
    p("        summary: '108 Ambulance CAD emergency dispatch integration failure'")
    p("        description: 'Emergency CAD dispatch requests to 108 Arogya Kavacha failed. Immediate voice escalation to GVK-EMRI control center required.'")
    p("        runbook_url: 'https://ops.nammahealth.bbmp.gov.in/runbooks/SRE-RB-003'")
    p("")
    p("    - alert: TamperEvidentAuditChainCorruption")
    p("      expr: worm_audit_chain_verifications_total{status='tamper_detected'} > 0")
    p("      for: 1m")
    p("      labels:")
    p("        severity: critical")
    p("        tier: security")
    p("        team: secops-oncall")
    p("      annotations:")
    p("        summary: 'WORM audit ledger cryptographic hash chain verification failure'")
    p("        description: 'A cryptographic hash chain mismatch was detected in the immutable audit ledger. Potential unauthorized database tampering.'")
    p("        runbook_url: 'https://ops.nammahealth.bbmp.gov.in/runbooks/SRE-RB-004'")
    p("")
    p("  - name: namma.clinical.alerts")
    p("    rules:")
    p("    - alert: MewsCriticalScoreCluster")
    p("      expr: sum(rate(mews_critical_alerts_total[1h])) > 25")
    p("      for: 10m")
    p("      labels:")
    p("        severity: high")
    p("        tier: clinical")
    p("        team: clinical-governance")
    p("      annotations:")
    p("        summary: 'Surge in critical MEWS triage alerts across clinics'")
    p("        description: 'Abnormal spike in MEWS scores >= 5 across multiple primary clinics. Investigate local infectious disease outbreak or heatwave event.'")
    p("        runbook_url: 'https://ops.nammahealth.bbmp.gov.in/runbooks/SRE-RB-005'")
    p("")
    p("    - alert: PharmacyEssentialStockoutSpike")
    p("      expr: count(pharmacy_stockout_items > 5) > 10")
    p("      for: 30m")
    p("      labels:")
    p("        severity: high")
    p("        tier: logistics")
    p("        team: warehouse-ops")
    p("      annotations:")
    p("        summary: 'More than 10 clinics report severe formulary stockouts'")
    p("        description: 'Multiple primary health clinics report > 5 essential medications at zero stock. Trigger emergency warehouse reallocation.'")
    p("        runbook_url: 'https://ops.nammahealth.bbmp.gov.in/runbooks/SRE-RB-006'")
    p("")
    p("    - alert: LabPanicValueBacklog")
    p("      expr: sum(rate(lab_panic_values_total[1h])) > 15")
    p("      for: 15m")
    p("      labels:")
    p("        severity: high")
    p("        tier: clinical")
    p("        team: clinical-ops")
    p("      annotations:")
    p("        summary: 'High volume of laboratory panic values'")
    p("        description: 'More than 15 critical lab panic values recorded in the last hour. Verify rapid physician notification delivery.'")
    p("        runbook_url: 'https://ops.nammahealth.bbmp.gov.in/runbooks/SRE-RB-007'")
    p("```")
    p("")

    p("## 06. Service Level Objectives (SLOs) & Error Budget Burn Rates")
    p("Exhaustive SLO commitments, multi-window PromQL burn-rate calculations, and SRE triage runbooks across 10 critical workflows:")
    p("")

    slos = [
        ("SLO-001", "Citizen Registration & Intake", "99.5% availability, P95 latency < 300ms", "30 Days Rolling", "0.5% (216 minutes downtime)",
         "sum(rate(http_requests_total{route=~'/api/v1/patients.*',status!~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/patients.*'}[1h]))",
         "sum(rate(http_requests_total{route=~'/api/v1/patients.*',status=~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/patients.*'}[1h])) > (14.4 * 0.005)",
         "sum(rate(http_requests_total{route=~'/api/v1/patients.*',status=~'5..'}[6h])) / sum(rate(http_requests_total{route=~'/api/v1/patients.*'}[6h])) > (6.0 * 0.005)",
         [
             "1. Inspect Master Patient Index (MPI) service pod CPU and memory utilization via `kubectl top pods -n namma-prod -l app=mpi-service`.",
             "2. Check PgBouncer active pool connections and query wait queue on PostgreSQL primary: `SELECT count(*) FROM pg_stat_activity WHERE state = 'active' AND query ILIKE '%patients%';`.",
             "3. Verify ABHA verification gateway latency; if NHA gateway is timing out (> 2,000ms), toggle MPI service circuit breaker to queue ABHA validation asynchronously.",
             "4. If pod memory exceeds 80%, scale deployment horizontally: `kubectl scale deployment mpi-service --replicas=6 -n namma-prod`."
         ]),

        ("SLO-002", "Nursing Triage & MEWS Scoring", "99.9% availability, P95 latency < 150ms", "30 Days Rolling", "0.1% (43.2 minutes downtime)",
         "sum(rate(http_requests_total{route=~'/api/v1/triage.*',status!~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/triage.*'}[1h]))",
         "sum(rate(http_requests_total{route=~'/api/v1/triage.*',status=~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/triage.*'}[1h])) > (14.4 * 0.001)",
         "sum(rate(http_requests_total{route=~'/api/v1/triage.*',status=~'5..'}[6h])) / sum(rate(http_requests_total{route=~'/api/v1/triage.*'}[6h])) > (6.0 * 0.001)",
         [
             "1. Verify local edge SQLite queue engine responsiveness on reporting clinic mini-server.",
             "2. Inspect tablet workstation Wi-Fi latency and AP signal strength using edge network diagnostic tool.",
             "3. If triage sync backlog is growing, restart local triage sync daemon: `systemctl restart namma-edge-daemon` on affected mini-server.",
             "4. Confirm MEWS calculation rule engine cache in Redis has not been invalidated."
         ]),

        ("SLO-003", "Doctor SOAP Encounter Consultation", "99.5% availability, P95 latency < 250ms", "30 Days Rolling", "0.5% (216 minutes downtime)",
         "sum(rate(http_requests_total{route=~'/api/v1/encounters.*',status!~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/encounters.*'}[1h]))",
         "sum(rate(http_requests_total{route=~'/api/v1/encounters.*',status=~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/encounters.*'}[1h])) > (14.4 * 0.005)",
         "sum(rate(http_requests_total{route=~'/api/v1/encounters.*',status=~'5..'}[6h])) / sum(rate(http_requests_total{route=~'/api/v1/encounters.*'}[6h])) > (6.0 * 0.005)",
         [
             "1. Check PostgreSQL active lock contention on `clinical_encounters` table: `SELECT relation::regclass, mode, granted FROM pg_locks WHERE NOT granted;`.",
             "2. Inspect autovacuum bloat and index health on `clinical_encounters` using `pg_stat_user_tables`.",
             "3. Verify doctor workstation PWA IndexedDB cache performance; clear stale local draft caches if corrupted.",
             "4. Scale consultation backend pods if CPU throttling detected in Prometheus container metrics."
         ]),

        ("SLO-004", "Electronic Prescribing (e-Rx)", "99.9% availability, P95 latency < 150ms", "30 Days Rolling", "0.1% (43.2 minutes downtime)",
         "sum(rate(http_requests_total{route=~'/api/v1/prescriptions.*',status!~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/prescriptions.*'}[1h]))",
         "sum(rate(http_requests_total{route=~'/api/v1/prescriptions.*',status=~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/prescriptions.*'}[1h])) > (14.4 * 0.001)",
         "sum(rate(http_requests_total{route=~'/api/v1/prescriptions.*',status=~'5..'}[6h])) / sum(rate(http_requests_total{route=~'/api/v1/prescriptions.*'}[6h])) > (6.0 * 0.001)",
         [
             "1. Inspect drug safety rules engine latency in Redis: check key cache hit ratio with `INFO stats`.",
             "2. Verify that formulary drug database has not been locked by an ongoing inventory bulk import.",
             "3. If safety engine latency exceeds 100ms, enable degraded-mode bypass allowing prescription signing with subsequent asynchronous safety auditing.",
             "4. Check for CPU saturation on prescription service pods."
         ]),

        ("SLO-005", "Pharmacy Dispensing & Scan", "99.5% availability, P95 latency < 100ms", "30 Days Rolling", "0.5% (216 minutes downtime)",
         "sum(rate(http_requests_total{route=~'/api/v1/pharmacy.*',status!~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/pharmacy.*'}[1h]))",
         "sum(rate(http_requests_total{route=~'/api/v1/pharmacy.*',status=~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/pharmacy.*'}[1h])) > (14.4 * 0.005)",
         "sum(rate(http_requests_total{route=~'/api/v1/pharmacy.*',status=~'5..'}[6h])) / sum(rate(http_requests_total{route=~'/api/v1/pharmacy.*'}[6h])) > (6.0 * 0.005)",
         [
             "1. Inspect FEFO inventory batch allocation lock queue; verify row-level locks on `pharmacy_batches` are released in < 20ms.",
             "2. Verify barcode scanner serial wedge driver inputs on workstation.",
             "3. Check edge mini-server local SQLite inventory replica sync state.",
             "4. Confirm thermal label printer queue is cleared."
         ]),

        ("SLO-006", "Point-of-Care Lab Diagnostic Orders", "99.5% availability, P95 latency < 150ms", "30 Days Rolling", "0.5% (216 minutes downtime)",
         "sum(rate(http_requests_total{route=~'/api/v1/lab.*',status!~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/lab.*'}[1h]))",
         "sum(rate(http_requests_total{route=~'/api/v1/lab.*',status=~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/lab.*'}[1h])) > (14.4 * 0.005)",
         "sum(rate(http_requests_total{route=~'/api/v1/lab.*',status=~'5..'}[6h])) / sum(rate(http_requests_total{route=~'/api/v1/lab.*'}[6h])) > (6.0 * 0.005)",
         [
             "1. Check diagnostic test catalogue lookup cache in Redis.",
             "2. Verify panic value WebSocket notification connections between lab workstations and physician consoles.",
             "3. Inspect pending lab order table partition indexes in PostgreSQL.",
             "4. Restart lab service worker pods if thread pool starvation is detected."
         ]),

        ("SLO-007", "108 Emergency CAD Dispatch", "99.99% availability, P99 latency < 500ms", "30 Days Rolling", "0.01% (4.32 minutes downtime)",
         "sum(rate(http_requests_total{route=~'/api/v1/referrals/cad.*',status!~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/referrals/cad.*'}[1h]))",
         "sum(rate(http_requests_total{route=~'/api/v1/referrals/cad.*',status=~'5..'}[1h])) / sum(rate(http_requests_total{route=~'/api/v1/referrals/cad.*'}[1h])) > (14.4 * 0.0001)",
         "sum(rate(http_requests_total{route=~'/api/v1/referrals/cad.*',status=~'5..'}[6h])) / sum(rate(http_requests_total{route=~'/api/v1/referrals/cad.*'}[6h])) > (6.0 * 0.0001)",
         [
             "1. CRITICAL: If 108 CAD API returns HTTP 5xx or times out > 500ms, trigger automated voice fallback to GVK-EMRI central dispatch telephone lines.",
             "2. Inspect outbound mTLS connection handshakes and corporate egress NAT gateway bandwidth.",
             "3. Verify CAD dispatch retry queue in Redis; ensure failed dispatches are re-attempted every 30 seconds.",
             "4. Escalate immediately to SRE Incident Commander and BBMP Medical Officer on duty."
         ]),

        ("SLO-008", "Autonomous Edge Sync Replay", "99.0% availability, Sync drain < 15 min", "30 Days Rolling", "1.0% (432 minutes downtime)",
         "sum(rate(sync_replay_success_total[1h])) / sum(rate(sync_replay_attempts_total[1h]))",
         "sum(rate(sync_replay_failed_total[1h])) / sum(rate(sync_replay_attempts_total[1h])) > (14.4 * 0.01)",
         "sum(rate(sync_replay_failed_total[6h])) / sum(rate(sync_replay_attempts_total[6h])) > (6.0 * 0.01)",
         [
             "1. Inspect cloud sync gateway ingress pod count and CPU load.",
             "2. Check clinic edge cellular failover modem connectivity via SMS telemetry ping.",
             "3. Inspect PostgreSQL WAL insertion rates on cloud sync staging tables.",
             "4. If CRDT conflict rate exceeds 5%, verify NTP clock synchronization across edge fleet: `ansible clinics -m command -a 'chronyc tracking'`."
         ]),

        ("SLO-009", "ABDM Care Context Publishing", "99.0% availability, P95 latency < 2,000ms", "30 Days Rolling", "1.0% (432 minutes downtime)",
         "sum(rate(abdm_publish_success_total[1h])) / sum(rate(abdm_publish_attempts_total[1h]))",
         "sum(rate(abdm_publish_failed_total[1h])) / sum(rate(abdm_publish_attempts_total[1h])) > (14.4 * 0.01)",
         "sum(rate(abdm_publish_failed_total[6h])) / sum(rate(abdm_publish_attempts_total[6h])) > (6.0 * 0.01)",
         [
             "1. Verify national ABDM NHA gateway health status and public status dashboard.",
             "2. Check ABDM OAuth 2.0 token expiration in Vault secrets manager.",
             "3. Inspect Kafka DLQ topic `namma.abdm.publish.dlq` for schema validation failures in FHIR R4 Bundles.",
             "4. Re-enqueue failed publication bundles after confirming NHA gateway recovery."
         ]),

        ("SLO-010", "Municipal Real-Time Analytics BI", "99.0% availability, P95 latency < 1,500ms", "30 Days Rolling", "1.0% (432 minutes downtime)",
         "sum(rate(clickhouse_query_success_total[1h])) / sum(rate(clickhouse_query_attempts_total[1h]))",
         "sum(rate(clickhouse_query_failed_total[1h])) / sum(rate(clickhouse_query_attempts_total[1h])) > (14.4 * 0.01)",
         "sum(rate(clickhouse_query_failed_total[6h])) / sum(rate(clickhouse_query_attempts_total[6h])) > (6.0 * 0.01)",
         [
             "1. Inspect ClickHouse cluster memory utilization and disk I/O wait times via `system.metrics`.",
             "2. Check Kafka Connect Debezium consumer lag on CDC topics: `kafka-consumer-groups --bootstrap-server kafka:9092 --describe --group clickhouse-sink`.",
             "3. If ClickHouse mutation queries are blocking, optimize merge operations on ReplacingMergeTree tables.",
             "4. Restart stalled Kafka Connect sink worker tasks."
         ])
    ]

    for slo in slos:
        slo_id, slo_scope, slo_target, slo_period, slo_budget, sli_expr, fast_burn, slow_burn, runbook_steps = slo
        s_num = int(slo_id.split('-')[1])
        p(f"### 06.{s_num:02d} SLO Specification: `{slo_id}` ({slo_scope})")
        p(f"- **SLO Code:** `{slo_id}`")
        p(f"- **Clinical & Operational Scope:** {slo_scope}")
        p(f"- **Target Service Level Indicator (SLI):** {slo_target}")
        p(f"- **Evaluation Period:** {slo_period}")
        p(f"- **Permitted Error Budget:** {slo_budget}")
        p("")
        p("#### SLI PromQL Measurement Calculation:")
        p("```promql")
        p(sli_expr)
        p("```")
        p("")
        p("#### Multi-Burn-Rate Alerting Rules:")
        p("| Alert Window | Burn Rate Multiplier | Error Budget Consumed | Triage Response SLA | Authoritative PromQL Alert Condition |")
        p("| :--- | :---: | :---: | :---: | :--- |")
        p(f"| **Fast Burn (1 Hour)** | 14.4x | 2% in 1 hour | Immediate PagerDuty (5m) | `{fast_burn}` |")
        p(f"| **Slow Burn (6 Hours)** | 6.0x | 5% in 6 hours | Business Hours Jira (30m) | `{slow_burn}` |")
        p("")
        p("#### Authoritative SRE Incident Triage Runbook:")
        for step in runbook_steps:
            p(f"- {step}")
        p("")
        p("---")
        p("")

    p("## 07. Centralized Structured Logging & PII Redaction Pipeline")
    p("Centralized JSON logging architecture guaranteeing zero sensitive health data leakage:")
    p("")
    p("### 07.1 Standard JSON Log Envelope Specification")
    p("Every log line emitted across all edge and cloud containers conforms to the following schema:")
    p("```json")
    p("{")
    p('  "@timestamp": "2026-09-04T11:15:30.452Z",')
    p('  "log.level": "INFO",')
    p('  "service.name": "namma-backend-consultation",')
    p('  "service.version": "1.4.2",')
    p('  "environment": "production",')
    p('  "clinic.id": "BBMP-CLN-042",')
    p('  "trace.id": "4bf92f3577b34da6a3ce929d0e0e4736",')
    p('  "span.id": "00f067aa0ba902b7",')
    p('  "staff.user_id": "usr-uuidv7-staff-0042",')
    p('  "staff.role": "PHYSICIAN",')
    p('  "action.name": "ENCOUNTER_SEALED",')
    p('  "message": "Encounter 018f3a5b-7c12 successfully sealed with HMAC signature.",')
    p('  "http.route": "/api/v1/encounters/018f3a5b-7c12/seal",')
    p('  "http.status_code": 200,')
    p('  "duration_ms": 142.5,')
    p('  "pii_redacted": true')
    p("}")
    p("```")
    p("")
    p("### 07.2 In-Line PII Redaction Engine")
    p("Before logs exit any service process memory boundary, the logging formatter executes deterministic regex-based scrubbing:")
    p("1. **Aadhaar Masking:** Regex `\\b[2-9][0-9]{3}[\\s-]?[0-9]{4}[\\s-]?[0-9]{4}\\b` is replaced by `[REDACTED_AADHAAR]`.")
    p("2. **Phone Number Masking:** Regex `\\b(?:\\+91|91|0)?[6-9][0-9]{9}\\b` is replaced by `[REDACTED_PHONE]`.")
    p("3. **ABHA ID Masking:** Regex `\\b[0-9]{2}-[0-9]{4}-[0-9]{4}-[0-9]{4}\\b` is replaced by `[REDACTED_ABHA]`.")
    p("4. **Free-Text Clinical Notes:** Free-text clinical observation strings are strictly prohibited from log arguments. AST linter rules reject code passing encounter notes to logger methods.")
    p("")
    p("### 07.3 Log Storage, Indexing & Tiering Policy")
    p("| Tier | Storage Engine | Retention Window | Compression | Query SLA | Purpose |")
    p("| :--- | :--- | :---: | :---: | :---: | :--- |")
    p("| **Hot Tier** | OpenSearch Cluster (NVMe) | 30 Days | Zstandard | < 1.0 sec | Real-time debugging, alerting, SRE triage |")
    p("| **Warm Tier** | S3 / Cloud Object Storage | 90 Days | Gzip Parquet | < 10.0 sec | Periodic reporting, compliance trend auditing |")
    p("| **Cold Tier** | WORM S3 Glacier Vault | 7 Years | Encrypted Gzip | < 12 hours | Statutory Indian Digital Personal Data Protection Act compliance |")
    p("")

    p("## 08. Grafana Operational Dashboard Specifications")
    p("Specifications and panel architectures for the 4 core SRE dashboards configured in Grafana:")
    p("")

    dashboards = [
        ("Central Municipal NOC Command Overview Cockpit",
         "Real-time geographical map displaying online/offline status across all 183 clinics, global HTTP throughput, P95 latency, active error budget burn rate dials, and aggregated citizen intake rates.",
         [
             ("Geographical Fleet Health Map", "Geomap", "count(edge_clinic_online_status == 1) by (clinic_id, latitude, longitude)", "Green = Online, Red = Offline (> 5 min disconnection)"),
             ("Platform Total Throughput", "Timeseries", "sum(rate(gateway_http_requests_total[5m]))", "Global requests per second handled by cloud ingress gateway"),
             ("P95 End-to-End Latency", "Timeseries", "histogram_quantile(0.95, sum(rate(gateway_http_request_duration_seconds_bucket[5m])) by (le))", "Target line at 250ms, alert threshold at 500ms"),
             ("Active Error Budget Burn Rates", "Gauge / Stat", "sum(rate(http_requests_total{status=~'5..'}[1h])) / sum(rate(http_requests_total[1h])) / 0.005", "Dials indicating 1h burn rate multiplier (> 14.4 triggers P1)")
         ]),

        ("Clinic Edge Fleet Appliance Health Console",
         "Fleet-wide distribution of edge mini-server SSD wear percentage, CPU temperature, pending offline mutation backlogs, and UPS battery charge percentages.",
         [
             ("Edge Fleet Online Percentage", "Stat", "(count(edge_clinic_online_status == 1) / 183) * 100", "Must stay >= 98.0% during operating hours (8:00 AM - 8:00 PM)"),
             ("Pending Offline Mutation Backlog", "Bar Chart", "topk(10, edge_mutation_queue_depth)", "Top 10 clinics with largest unsynced transaction queues"),
             ("Edge Mini-Server SSD Wear Leveling", "Heatmap", "sum(edge_nvme_wear_percentage) by (clinic_id)", "Identifies storage drives approaching 80% endurance limit"),
             ("Clinic UPS Battery Reserve Charge", "Table", "edge_ups_battery_charge_percent < 30", "Clinics with emergency UPS power running below 30 minutes")
         ]),

        ("Clinical Consultation & Prescription Journey Dashboard",
         "End-to-end trace waterfalls from intake token printing to pharmacy dispensation, PgBouncer database pool utilization, and slow SQL query inspection.",
         [
             ("Consultation Velocity Rate", "Timeseries", "sum(rate(encounters_sealed_total[10m])) by (zone_id)", "Completed doctor consultations per minute grouped by municipal zone"),
             ("Prescription Safety Engine Evaluation Latency", "Histogram", "histogram_quantile(0.99, sum(rate(rx_safety_evaluation_duration_seconds_bucket[5m])) by (le))", "Ensures drug safety checks complete in under 50ms"),
             ("PostgreSQL Connection Pool Saturation", "Gauge", "db_connection_pool_active / db_connection_pool_max", "Pool saturation gauge with warning threshold at 80%"),
             ("Top 5 Slowest Relational Queries", "Table", "topk(5, rate(db_slow_queries_total[1h])) by (query_hash)", "Queries exceeding 100ms execution threshold requiring index tuning")
         ]),

        ("Municipal Epidemiological & Outbreak Surveillance Cockpit",
         "Syndromic surveillance tracking influenza-like illnesses, dengue clusters, hypertension prevalence, and laboratory panic value trends.",
         [
             ("Syndromic Cluster Heatmap", "Heatmap", "sum(rate(encounters_sealed_total{icd10=~'J06.*|A90.*'}[1h])) by (ward_id)", "Identifies spatial concentration of respiratory and dengue symptoms"),
             ("Rapid Lab Panic Value Frequency", "Timeseries", "sum(rate(lab_panic_values_total[1h])) by (test_code)", "Hourly trend of critically abnormal blood sugar, hemoglobin, and electrolytes"),
             ("Hypertension Risk Stratification Breakdown", "Pie Chart", "sum(ai_inference_evaluations_total{model_id='ARCH-AI-001'}) by (risk_band)", "Distribution of low, moderate, and high NCD risk predictions"),
             ("Emergency CAD Ambulance Dispatches", "Timeseries", "sum(rate(emergency_108_dispatches_total[1h])) by (clinic_id)", "Real-time volume of 108 emergency transfers initiated")
         ])
    ]

    for d_idx, d in enumerate(dashboards, start=1):
        p(f"### 08.{d_idx} Grafana Dashboard Blueprint: {d[0]}")
        p(f"- **Dashboard Title:** {d[0]}")
        p(f"- **Operational Purpose:** {d[1]}")
        p(f"- **Refresh Interval:** 15 seconds (NOC) / 60 seconds (Analytics)")
        p("")
        p("#### Panel Layout & PromQL Query Specifications:")
        p("| Panel Title | Visualization Type | Authoritative PromQL Query | Operational Interpretation |")
        p("| :--- | :---: | :--- | :--- |")
        for panel in d[2]:
            p(f"| {panel[0]} | **{panel[1]}** | `{panel[2]}` | {panel[3]} |")
        p("")
        p("#### Panel Configuration Contract (Grafana Schema):")
        p("```json")
        p("{")
        p(f'  "title": "{d[0]}",')
        p('  "refresh": "15s",')
        p('  "schemaVersion": 38,')
        p('  "tags": ["namma-clinic", "sre", "production"],')
        p('  "panels": [')
        for p_idx, panel in enumerate(d[2], start=1):
            comma = "," if p_idx < len(d[2]) else ""
            p('    {')
            p(f'      "id": {p_idx},')
            p(f'      "title": "{panel[0]}",')
            p(f'      "type": "{panel[1].lower().split()[0]}",')
            p(f'      "targets": [{{ "expr": "{panel[2]}", "refId": "A" }}],')
            p('      "gridPos": { "h": 8, "w": 12, "x": ' + str((p_idx-1)%2*12) + ', "y": ' + str((p_idx-1)//2*8) + ' }')
            p(f'    }}{comma}')
        p('  ]')
        p("}")
        p("```")
        p("")
        p("---")
        p("")

    p("## 09. OpenTelemetry Collector Production DaemonSet Configuration")
    p("Production DaemonSet configuration for the central OpenTelemetry Collector deployed in Kubernetes:")
    p("```yaml")
    p("apiVersion: v1")
    p("kind: ConfigMap")
    p("metadata:")
    p("  name: otel-collector-config")
    p("  namespace: monitoring")
    p("  labels:")
    p("    app.kubernetes.io/name: otel-collector")
    p("data:")
    p("  config.yaml: |")
    p("    receivers:")
    p("      otlp:")
    p("        protocols:")
    p("          grpc:")
    p("            endpoint: 0.0.0.0:4317")
    p("          http:")
    p("            endpoint: 0.0.0.0:4318")
    p("      prometheus:")
    p("        config:")
    p("          scrape_configs:")
    p("          - job_name: 'namma-pods'")
    p("            kubernetes_sd_configs:")
    p("            - role: pod")
    p("            relabel_configs:")
    p("            - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]")
    p("              action: keep")
    p("              regex: true")
    p("")
    p("    processors:")
    p("      memory_limiter:")
    p("        check_interval: 1s")
    p("        limit_percentage: 75")
    p("        spike_limit_percentage: 20")
    p("      batch:")
    p("        send_batch_size: 8192")
    p("        timeout: 200ms")
    p("      attributes/scrub:")
    p("        actions:")
    p("        - key: patient.name")
    p("          action: delete")
    p("        - key: patient.aadhaar")
    p("          action: hash")
    p("        - key: patient.phone")
    p("          action: hash")
    p("      tail_sampling:")
    p("        decision_wait: 10s")
    p("        num_traces: 10000")
    p("        expected_new_traces_per_sec: 2000")
    p("        policies:")
    p("        - name: error-policy")
    p("          type: status_code")
    p("          status_code: { status_codes: [ERROR] }")
    p("        - name: latency-policy")
    p("          type: numeric_attribute")
    p("          numeric_attribute: { key: 'execution.duration_ms', value_condition: { greater_than: 500 } }")
    p("        - name: probabilistic-policy")
    p("          type: probabilistic")
    p("          probabilistic: { sampling_percentage: 5.0 }")
    p("")
    p("    exporters:")
    p("      otlp/tempo:")
    p("        endpoint: tempo-distributor.monitoring:4317")
    p("        tls:")
    p("          insecure: true")
    p("      prometheus:")
    p("        endpoint: 0.0.0.0:8889")
    p("      elasticsearch:")
    p("        endpoints: ['https://opensearch.monitoring:9200']")
    p("        index: 'namma-logs-%Y.%m.%d'")
    p("        tls:")
    p("          insecure_skip_verify: false")
    p("          ca_file: /etc/ssl/certs/ca.pem")
    p("")
    p("    service:")
    p("      pipelines:")
    p("        traces:")
    p("          receivers: [otlp]")
    p("          processors: [memory_limiter, attributes/scrub, tail_sampling, batch]")
    p("          exporters: [otlp/tempo]")
    p("        metrics:")
    p("          receivers: [otlp, prometheus]")
    p("          processors: [memory_limiter, batch]")
    p("          exporters: [prometheus]")
    p("        logs:")
    p("          receivers: [otlp]")
    p("          processors: [memory_limiter, attributes/scrub, batch]")
    p("          exporters: [elasticsearch]")
    p("```")
    p("")

    p("## 10. Incident Triage, SRE Escalation Matrix & Runbooks")
    p("Standardized incident classification, escalation protocols, and blameless post-mortem standards:")
    p("")
    p("### 10.1 Incident Severity Levels & Response SLAs")
    p("| Severity | Operational Criteria | Triage SLA | Escalation Target | Notification Channel |")
    p("| :--- | :--- | :---: | :--- | :--- |")
    p("| **SEV-1 (Critical)** | Core clinical system outage, central DB failure, CAD 108 dispatch down, or > 15 clinics offline | < 5 Minutes | SRE Incident Commander, Principal Architect, BBMP Health Commissioner | Automated PagerDuty Phone Call + High-Priority SMS + War Room Bridge |")
    p("| **SEV-2 (Major)** | Single municipal zone offline, prescription safety rules degraded, or ABDM sync queue halted | < 15 Minutes | SRE Primary On-Call, Lead Backend Engineer | PagerDuty Push Alert + Slack #war-room-active |")
    p("| **SEV-3 (Moderate)** | Single clinic edge appliance degraded, non-critical telemetry loss, or slow BI analytical report | < 60 Minutes | Tier 2 Field Support Engineer | Jira Service Management Ticket + Email Notification |")
    p("| **SEV-4 (Minor)** | Minor UI cosmetic glitch, thermal slip formatting defect, or non-blocking audit log delay | < 24 Hours | Product Engineering Team | Backlog Sprint Item |")
    p("")
    p("### 10.2 SRE Escalation Hierarchy")
    p("```")
    p(" +------------------------------------------------------------------------------------------------+")
    p(" |                                  Automated Alert Trigger                                       |")
    p(" |                 (Prometheus AlertManager -> PagerDuty Webhook Integration)                     |")
    p(" +------------------------------------------------------------------------------------------------+")
    p("                                                  |")
    p("                                          0 to 5 Minutes")
    p("                                                  v")
    p(" +------------------------------------------------------------------------------------------------+")
    p(" |                 Tier 1: Primary SRE On-Call Engineer (Acknowledge & Triage)                    |")
    p(" |       - Run diagnostic scripts, inspect Grafana dashboards, check container logs               |")
    p(" +------------------------------------------------------------------------------------------------+")
    p("                                                  |")
    p("                                         Unresolved at 15m")
    p("                                                  v")
    p(" +------------------------------------------------------------------------------------------------+")
    p(" |                 Tier 2: Secondary SRE Lead & Component Tech Lead Escalation                     |")
    p(" |       - Execute stateful failovers, Patroni promote, traffic shedding, rollbacks               |")
    p(" +------------------------------------------------------------------------------------------------+")
    p("                                                  |")
    p("                                         Unresolved at 30m")
    p("                                                  v")
    p(" +------------------------------------------------------------------------------------------------+")
    p(" |                 Tier 3: Incident Commander, Principal Architect & BBMP Leadership              |")
    p(" |       - Declare Major Incident, activate Disaster Recovery site, dispatch field teams          |")
    p(" +------------------------------------------------------------------------------------------------+")
    p("```")
    p("")

    p("## 11. Observability Architecture Fitness Tests & Verification Checklist")
    p("Automated CI/CD quality gates ensuring continuous compliance with observability standards:")
    p("")
    p("### 11.1 Automated Architecture Fitness Tests")
    p("1. **Span Context Propagation Fitness Test:** Synthetic test fires an end-to-end HTTP request through API Gateway; asserts that child span ID and parent span ID match across all 18 service container boundaries.")
    p("2. **PII Leakage Regression Gate:** Injects synthetic Aadhaar and mobile numbers into test logging streams; asserts that regex scrubbing filter replaces them with `[REDACTED]` prior to emission.")
    p("3. **Prometheus Metric Schema Linter:** Validates that all newly instrumented Prometheus metrics conform to naming conventions (ending in `_total`, `_seconds`, `_bytes`) and strictly adhere to enumerated label dimensions.")
    p("4. **High-Cardinality Label Blocker:** Static analysis AST scanner fails pull requests if any metric label uses unbounded values (e.g., patient IDs, timestamps, session tokens).")
    p("5. **Distributed Trace Sampling Verification:** Tests that 100% of HTTP 500 error traces and slow traces (> 500ms) are retained by tail-sampling rules.")
    p("")
    p("### 11.2 Verification Checklist Matrix")
    p("| Verification Item | Automated Check Command / Script | Acceptance Threshold | CI/CD Enforcement Gate |")
    p("| :--- | :--- | :---: | :---: |")
    p("| OpenTelemetry SDK Coverage | `npm run test:otel:coverage` | 100% of API endpoints instrumented | PR Merge Blocker |")
    p("| W3C Traceparent Injection | `npm run test:traceparent:propagation` | Zero unlinked trace spans | PR Merge Blocker |")
    p("| Zero PII in Telemetry | `python scripts/tests/verify_telemetry_pii.py` | 0 plain Aadhaar / phone occurrences | Nightly Security Audit |")
    p("| Prometheus Alert Rules Valid | `promtool check rules alerts/*.yaml` | Zero syntax or PromQL parse errors | Build Pipeline Gate |")
    p("| SLO Burn Rate Alerting Valid | `promtool test rules tests/slo_tests.yaml` | 100% burn-rate test assertions pass | Build Pipeline Gate |")
    p("")

    content = "\n".join(lines)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    metrics = count_lines(content)
    print(f"Generated {OUTPUT_FILE}: Total {metrics['total']}, Substantive {metrics['substantive']}")
    return OUTPUT_FILE, metrics["total"], metrics["substantive"]

if __name__ == "__main__":
    generate_document()
