"""
gen_db_08_indexes.py
Generates docs/07-database/08-index-strategy.md
Target: 2,500 - 3,500 substantive lines.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from scripts.database.db_core_data import (
    TABLES, INDEXES, INDEX_MAP, TABLE_NAME_MAP
)
from scripts.database.db_gen_common import write_db_doc

def generate_doc_08():
    lines = []

    lines.append("# Phase 07 — Complete Indexing Strategy & Performance Acceleration Blueprint")
    lines.append("")
    lines.append("> **Document Identifier**: `DB-INDEX-001`  ")
    lines.append("> **System**: Namma Clinic Digital Health & Operations Platform  ")
    lines.append("> **Municipal Authority**: Greater Bengaluru Authority (GBA) / BBMP Health Department  ")
    lines.append("> **Status**: APPROVED INDEXING BASELINE  ")
    lines.append(f"> **Total Cataloged Indexes**: {len(INDEXES)} Database Indexes (`INDEX-001` to `INDEX-{len(INDEXES):03d}`)  ")
    lines.append("> **Supported Index Engines**: B-tree, GIN, BRIN, Composite, Partial, and Expression Indexes  ")
    lines.append("> **Operational Rule**: Zero Table Locking — All Production Indexes Built Using `CONCURRENTLY`  ")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Executive Overview
    lines.append("## 1. Executive Summary & Indexing Strategy Objectives")
    lines.append("")
    lines.append("This document establishes the comprehensive database indexing strategy for the Namma Clinic platform on PostgreSQL 16. It details the technical rationale, query patterns, selectivity profiles, write amplification trade-offs, and monitoring runbooks across all 132 designated indexes supporting the 52 canonical tables.")
    lines.append("")
    lines.append("The indexing architecture is engineered to guarantee sub-5 millisecond response times for primary clinical workflows (patient search, doctor call queue, barcode drug dispensing) while strictly controlling write amplification on high-throughput ingestion tables (IoT temperature telemetry, queue state transitions, WORM audit logs).")
    lines.append("")

    # Index Taxonomy & Mechanics
    lines.append("## 2. PostgreSQL Index Type Taxonomy & Use Cases")
    lines.append("")
    lines.append("The platform utilizes five specialized index engines tailored to specific data access patterns:")
    lines.append("")
    lines.append("| Index Engine | Storage & Access Mechanics | Primary Use Case in Namma Clinic | Write & Maintenance Cost |")
    lines.append("| :--- | :--- | :--- | :--- |")
    lines.append("| **B-Tree (Standard)** | Balanced search tree with O(log N) lookup, range scanning, and sort ordering. | Primary keys, foreign keys, unique natural handles (email, phone blind index). | Low to Medium; optimal for high-cardinality keys. |")
    lines.append("| **Composite B-Tree** | Multi-column B-tree indexed in strict left-to-right prefix order. | Multi-predicate filters (e.g. `facility_id` + `status` + `priority_score`). | Medium; order of columns determines index reusability. |")
    lines.append("| **Partial B-Tree** | B-tree index restricted to a subset of rows via a `WHERE` predicate filter. | Filtering active records (`WHERE deleted_at IS NULL`) or pending items. | Very Low; index size is tiny compared to full table. |")
    lines.append("| **BRIN (Block Range)** | Block Range Index storing minimum and maximum values per 128 disk pages. | High-volume append-only time-series (`cold_chain_telemetry`, `audit_events`). | Extremely Low (< 1% of table size); minimal write cost. |")
    lines.append("| **GIN (Generalized Inverted)**| Inverted index mapping terms and paths to tuple IDs. | Extensible JSONB searching on `clinical_payload_json` and metadata. | High write cost; optimized for rich clinical document queries. |")
    lines.append("")

    # Anti-patterns Section
    lines.append("## 3. Database Indexing Anti-Patterns & Prevention Guardrails")
    lines.append("")
    lines.append("To prevent operational degradation under heavy municipal loads, five critical indexing anti-patterns are strictly prohibited across all schemas:")
    lines.append("")
    lines.append("| Anti-Pattern ID | Anti-Pattern Name | Description & Mechanism of Failure | Architectural Prevention Invariant |")
    lines.append("| :--- | :--- | :--- | :--- |")
    lines.append("| **AP-IDX-001** | Redundant Prefix Indexing | Creating a standalone index on column `A` when a composite index already exists on `(A, B)`. | PostgreSQL can utilize `(A, B)` for queries on `A` alone. Standalone index on `A` is redundant and wastes write I/O. |")
    lines.append("| **AP-IDX-002** | Low-Selectivity Boolean Indexing | Building a full B-tree index on low-cardinality columns (e.g. `is_active BOOLEAN`). | Query planner ignores index and performs sequential scan if a value matches > 15% of table rows. Use partial index instead. |")
    lines.append("| **AP-IDX-003** | Unindexed Foreign Keys | Omitting a dedicated B-tree index on a child table foreign key column. | When parent row is updated or deleted, PostgreSQL acquires a share-row lock and scans the entire child table, causing deadlocks. |")
    lines.append("| **AP-IDX-004** | Over-Indexing on High-Ingest Tables | Creating 5+ B-tree indexes on append-heavy tables (`telemetry`, `mutations`). | Every insert must update all B-tree indexes, causing severe write amplification and disk I/O bottlenecks. |")
    lines.append("| **AP-IDX-005** | Unused Index Accumulation | Retaining indexes that are never selected by the PostgreSQL query planner. | Wastes RAM buffer pool memory and slows table vacuuming. Monitored via `pg_stat_user_indexes`. |")
    lines.append("")

    # Master Index Catalog
    lines.append("## 4. Master Index Inventory (INDEX-001 to INDEX-132)")
    lines.append("")
    lines.append("The 132 database indexes deployed across the platform are cataloged below:")
    lines.append("")
    lines.append("| Index ID | Table Name | Columns | Index Engine | Uniqueness | Partial Predicate | Purpose & Query Pattern |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for idx in INDEXES:
        tname = idx["table_name"]
        cols = idx["columns"]
        itype = idx["index_type"]
        uniq = "UNIQUE" if idx["uniqueness"] else "NON-UNIQUE"
        pred = f"`{idx['partial_predicate']}`" if idx["partial_predicate"] else "None (Full)"
        purp = idx["purpose"]
        lines.append(f"| **{idx['id']}** | `{tname}` | `({cols})` | {itype} | {uniq} | {pred} | {purp} |")
    lines.append("")

    # Comprehensive Specifications for all 132 Indexes
    lines.append("## 5. Detailed Index Specifications (INDEX-001 to INDEX-132)")
    lines.append("")
    lines.append("Below is the exhaustive technical specification for every index in the platform, documenting columns, selectivity, query patterns, concurrency considerations, and removal criteria:")
    lines.append("")

    for idx in INDEXES:
        iid = idx["id"]
        tname = idx["table_name"]
        cols = idx["columns"]
        itype = idx["index_type"]
        purp = idx["purpose"]
        pattern = idx["query_pattern"]
        sel = idx["expected_selectivity"]
        card = idx["cardinality"]
        wcost = idx["write_cost"]
        scost = idx["storage_cost"]
        uniq = idx["uniqueness"]
        pred = idx["partial_predicate"]
        expr = idx["expression"]
        cov = idx["covering_columns"]
        
        schema = TABLE_NAME_MAP[tname]["schema"]
        
        lines.append(f"### {iid}: `idx_{tname}_{iid.lower().replace('-', '_')}` on `{schema}.{tname}`")
        lines.append("")
        lines.append(f"- **Index Identifier**: `{iid}`")
        lines.append(f"- **Target Table**: `{schema}.{tname}`")
        lines.append(f"- **Indexed Columns / Expression**: `({cols})`")
        lines.append(f"- **Engine Type**: `{itype}` ({'Unique' if uniq else 'Non-Unique'})")
        lines.append(f"- **Technical Purpose**: {purp}")
        lines.append(f"- **Target Query Pattern**: `{pattern}`")
        lines.append(f"- **Expected Selectivity & Cardinality**: Selectivity `{sel}`; Cardinality `{card}`")
        lines.append(f"- **Resource Impact**: Write Cost `{wcost}`; Storage Footprint `{scost}`")
        lines.append(f"- **Partial Predicate**: `{pred if pred else 'None (Indexes All Tuples)'}`")
        lines.append(f"- **Functional Expression**: `{expr if expr else 'None (Direct Column Values)'}`")
        lines.append(f"- **Covering Columns (INCLUDE)**: `{cov if cov else 'None'}`")
        lines.append(f"- **Concurrency & Rollout**: {idx['concurrency_considerations']}")
        lines.append(f"- **Monitoring Metric**: Track `idx_scan` and `idx_tup_read` via `pg_stat_user_indexes`")
        lines.append(f"- **Decommissioning Criteria**: {idx['removal_criteria']}")
        lines.append("")
        lines.append("```sql")
        lines.append(f"-- DOCUMENTATION-ONLY SQL: Physical Index Creation DDL for {iid}")
        uniq_clause = "UNIQUE " if uniq else ""
        pred_clause = f"\n    WHERE {pred}" if pred else ""
        cov_clause = f"\n    INCLUDE ({cov})" if cov else ""
        lines.append(f"CREATE {uniq_clause}INDEX CONCURRENTLY IF NOT EXISTS idx_{tname}_{iid.lower().replace('-', '_')}")
        lines.append(f"    ON {schema}.{tname} USING {itype.split()[0].lower()} ({cols}){cov_clause}{pred_clause};")
        lines.append("```")
        lines.append("")

    # Index Maintenance & Reindexing Runbook
    lines.append("## 6. Operational Reindexing & Bloat Remediation Runbook")
    lines.append("")
    lines.append("Over time, continuous updates on high-frequency tables cause B-tree index bloat. The following operational runbook governs maintenance without table locks:")
    lines.append("")
    lines.append("### 6.1 Index Bloat Detection Query")
    lines.append("```sql")
    lines.append("-- DOCUMENTATION-ONLY SQL: Index Bloat Detection Query")
    lines.append("SELECT")
    lines.append("    schemaname,")
    lines.append("    relname AS table_name,")
    lines.append("    indexrelname AS index_name,")
    lines.append("    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,")
    lines.append("    idx_scan,")
    lines.append("    idx_tup_read,")
    lines.append("    idx_tup_fetch")
    lines.append("FROM pg_stat_user_indexes")
    lines.append("ORDER BY pg_relation_size(indexrelid) DESC LIMIT 20;")
    lines.append("```")
    lines.append("")
    lines.append("### 6.2 Zero-Downtime Reindexing Runbook")
    lines.append("To compact bloated B-tree indexes without acquiring exclusive table locks:")
    lines.append("1. **Execute Concurrent Reindex**: `REINDEX INDEX CONCURRENTLY <index_name>;`")
    lines.append("2. **Monitor Reindex Progress**: Query `pg_stat_progress_create_index` to observe processing phases.")
    lines.append("3. **Handle Interrupted Builds**: If a reindex is cancelled, drop the temporary invalid index: `DROP INDEX CONCURRENTLY <index_name>_ccnew;`")
    lines.append("")

    lines.append("## 7. Conclusion & Index Verification Baseline")
    lines.append("")
    lines.append(f"The {len(INDEXES)} database indexes cataloged in this specification provide complete, high-selectivity query acceleration for the Namma Clinic platform. Every index has been assigned an explicit engine type, selectivity profile, and zero-downtime concurrent rollout plan.")
    lines.append("")

    content = "\n".join(lines)
    return write_db_doc("08-index-strategy.md", content)

if __name__ == "__main__":
    generate_doc_08()
