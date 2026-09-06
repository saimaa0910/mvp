"""
gen_db_05_catalog.py
Generates docs/07-database/05-table-catalog.md
Target: 2,500 - 3,500 substantive lines.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from scripts.database.db_core_data import (
    TABLES, ENTITIES, CLASSIFICATIONS, RETENTION_RULES,
    RELATIONSHIPS, INDEXES, PARTITIONS, AUDIT_ENTITIES, TRANSACTIONS,
    TABLE_COLUMNS_MAP
)
from scripts.database.db_gen_common import write_db_doc

def generate_doc_05():
    lines = []

    lines.append("# Phase 07 — Enterprise Table Catalog & Master Entity Registry")
    lines.append("")
    lines.append("> **Document Identifier**: `DB-CATALOG-001`  ")
    lines.append("> **System**: Namma Clinic Digital Health & Operations Platform  ")
    lines.append("> **Municipal Authority**: Greater Bengaluru Authority (GBA) / BBMP Health Department  ")
    lines.append("> **Status**: APPROVED ENTERPRISE CATALOG  ")
    lines.append("> **Catalog Coverage**: 52 Master Relational Tables (`TABLE-001` to `TABLE-052`)  ")
    lines.append("> **Relational Schemas**: `identity`, `intake`, `clinical`, `pharmacy`, `continuity`, `audit`, `sync`  ")
    lines.append("> **Classification Framework**: 5-Tier Data Classification Standard (`CLASS-001` to `CLASS-005`)  ")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Executive Overview
    lines.append("## 1. Executive Summary & Catalog Scope")
    lines.append("")
    lines.append("This document establishes the master enterprise table catalog for the Namma Clinic platform. It serves as the single authoritative encyclopedia detailing the operational purpose, data ownership, schema boundary, lifecycle states, growth projections, data classifications, foreign key dependencies, indexing models, data quality rules, and end-to-end lineage for all 52 relational tables.")
    lines.append("")
    lines.append("Every table profile is engineered to provide complete operational, architectural, and regulatory clarity to database administrators, backend service developers, data protection officers, and clinical governance auditors. Superficial descriptions are prohibited; each entry provides comprehensive specifications covering both operational steady-state behavior and emergency disaster recovery parameters.")
    lines.append("")

    # Summary Statistics Table
    lines.append("## 2. Master Table Inventory Summary Matrix")
    lines.append("")
    lines.append("The 52 tables are categorized across 6 major functional healthcare domains:")
    lines.append("")
    lines.append("| Table ID | Table Name | Schema | Operational Domain | Primary Key | Partition Strategy | Classification | Retention Policy | Estimated Annual Volume |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for tbl in TABLES:
        lines.append(f"| **{tbl['id']}** | `{tbl['name']}` | `{tbl['schema']}` | {tbl['domain']} | `{tbl['pk']}` | {tbl['partition_strategy']} | `{tbl['classification']}` | `{tbl['retention']}` | {tbl['estimated_volume']} |")
    lines.append("")

    # Exhaustive Catalog for all 52 Tables
    lines.append("## 3. Comprehensive Table Catalog (TABLE-001 to TABLE-052)")
    lines.append("")

    for tbl in TABLES:
        tid = tbl["id"]
        tname = tbl["name"]
        schema = tbl["schema"]
        domain = tbl["domain"]
        tcols = TABLE_COLUMNS_MAP.get(tname, [])
        t_indexes = [i for i in INDEXES if i["table_name"] == tname]
        inbound_rels = [r for r in RELATIONSHIPS if r["child"] == tname]
        outbound_rels = [r for r in RELATIONSHIPS if r["parent"] == tname]
        
        lines.append(f"### {tid}: `{schema}.{tname}`")
        lines.append("")
        lines.append(f"#### 1. Identification & Governance Profile")
        lines.append("")
        lines.append(f"- **Table Identifier**: `{tid}`")
        lines.append(f"- **Fully Qualified Name**: `{schema}.{tname}`")
        lines.append(f"- **Functional Domain**: `{domain}`")
        lines.append(f"- **Executive Data Owner**: {tbl['owner']}")
        lines.append(f"- **Primary Key Column**: `{tbl['pk']}` (PostgreSQL 128-bit `{tbl['pk_type']}`)")
        lines.append(f"- **Data Classification**: `{tbl['classification']}` (Governed by DPDP Act 2023 & DISHA)")
        lines.append(f"- **Statutory Retention Policy**: `{tbl['retention']}`")
        lines.append(f"- **Audit Requirements**: {tbl['audit_requirement']}")
        lines.append("")
        lines.append(f"#### 2. Business Purpose & Scope Description")
        lines.append(f"**Operational Role**: {tbl['business_purpose']}")
        lines.append("")
        lines.append(f"{tbl['description']}")
        lines.append("")
        lines.append(f"#### 3. Operational Lifecycle & Volume Projections")
        lines.append(f"- **Lifecycle Stages**: {tbl['lifecycle']}")
        lines.append(f"- **Estimated Storage Footprint**: Baseline capacity: `{tbl['estimated_volume']}`; Expected growth rate: `{tbl['growth_rate']}`.")
        lines.append(f"- **Partitioning Architecture**: `{tbl['partition_strategy']}`")
        lines.append(f"- **Soft Deletion Mechanism**: `deleted_at TIMESTAMPTZ` maintains referential stability while hiding decommissioned tuples from default views.")
        lines.append("")
        lines.append(f"#### 4. Foreign Key Relationships & Relational Dependencies")
        lines.append("")
        lines.append("**Inbound Dependencies (Foreign Keys held by this table):**")
        if inbound_rels:
            lines.append("| Foreign Key | References Table | Parent PK | ON DELETE Action | Relationship Semantic |")
            lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for r in inbound_rels:
                lines.append(f"| `{r['cfk']}` | `{r['parent']}` | `{r['ppk']}` | `{r['on_del']}` | {r['rat']} |")
        else:
            lines.append("*None (Top-level root table in domain hierarchy).*")
        lines.append("")
        lines.append("**Outbound Dependencies (Child tables referencing this table):**")
        if outbound_rels:
            lines.append("| Child Table | Foreign Key Column | Cardinality | Dependency Rationale |")
            lines.append("| :--- | :--- | :--- | :--- |")
            for r in outbound_rels:
                lines.append(f"| `{r['child']}` | `{r['cfk']}` | `{r['card']}` | {r['rat']} |")
        else:
            lines.append("*None (Leaf entity in domain dependency graph).*")
        lines.append("")
        lines.append(f"#### 5. Indexing Architecture & Query Acceleration")
        lines.append(f"The table features {len(t_indexes)} dedicated indexes designed for high-selectivity retrieval:")
        lines.append("")
        lines.append("| Index ID | Type | Columns | Expected Selectivity | Query Pattern Accelerated |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for idx in t_indexes:
            lines.append(f"| `{idx['id']}` | {idx['index_type']} | `({idx['columns']})` | {idx['expected_selectivity']} | `{idx['query_pattern']}` |")
        lines.append("")
        lines.append(f"#### 6. Ecosystem Consumer Systems & Data Flow")
        lines.append(f"- **Upstream Requirements**: `{tbl['source_reqs']}`")
        lines.append(f"- **Upstream Workflows**: `{tbl['workflows']}`")
        lines.append(f"- **REST / GraphQL APIs**: `{tbl['api_consumers']}`")
        lines.append(f"- **Reporting Dashboards**: `{tbl['reporting_consumers']}`")
        lines.append(f"- **Analytical Warehousing**: `{tbl['analytics_consumers']}`")
        lines.append(f"- **AI & Decision Support Models**: `{tbl['ai_consumers']}`")
        lines.append(f"- **Edge Synchronization**: `{tbl['sync_behavior']}`")
        lines.append("")
        lines.append(f"#### 7. Reliability, Disaster Recovery & Data Quality")
        lines.append(f"- **Backup Priority**: `{tbl['backup_priority']}`")
        lines.append(f"- **Recovery Priority**: `{tbl['recovery_priority']}`")
        lines.append(f"- **Migration Sensitivity**: `{tbl['migration_sensitivity']}`")
        lines.append(f"- **Governing Data Quality Rules**: `{tbl['dq_rules']}`")
        lines.append(f"- **Data Lineage Traceability**: `{tbl['lineage_refs']}`")
        lines.append("")

    lines.append("## 4. Conclusion & Cross-Catalog Verification")
    lines.append("")
    lines.append("The 52 table profiles detailed above establish an exhaustive technical catalog. Every table is mapped to its exact schema, domain, owners, indexes, and downstream consumers without ambiguity. This catalog serves as the central operational guide for subsequent database administration and application development.")
    lines.append("")

    content = "\n".join(lines)
    return write_db_doc("05-table-catalog.md", content)

if __name__ == "__main__":
    generate_doc_05()
