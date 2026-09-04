#!/usr/bin/env python3
"""
validation.py
Reusable verification and validation logic for Namma Clinic Requirements Engineering.
Implements audit rules 1 through 30.
"""

import os
import re
from collections import Counter

def is_substantive_line(line: str) -> bool:
    """Check if a line is substantive (not blank, not just header, not horizontal rule)."""
    s = line.strip()
    if not s:
        return False
    if s.startswith("#"):
        return False
    if s == "---":
        return False
    if s in ("| :--- | :--- |", "| :--- | :---: |"):
        return False
    return True

def count_lines_and_substantive(filepath: str):
    """Return (total_lines, substantive_lines) for a markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()
    substantive = [l for l in lines if is_substantive_line(l)]
    return len(lines), len(substantive)

def find_duplicate_paragraphs(filepath: str, min_len: int = 60) -> dict:
    """Find repeated paragraphs above a certain length in a markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) >= min_len]
    counts = Counter(paragraphs)
    return {p: c for p, c in counts.items() if c > 1}

def extract_requirement_ids_from_text(text: str) -> list:
    """Extract all requirement IDs matching standard prefixes from text."""
    pattern = r"\b(BR-\d{3}|FR-\d{3}|NFR-\d{3}|BRULE-\d{3}|CR-\d{3}|OR-\d{3}|SECR-\d{3}|PRIV-\d{3}|PERF-\d{3}|AVAIL-\d{3}|LOC-\d{3}|A11Y-\d{3}|OFF-\d{3}|REP-\d{3}|ANL-\d{3}|AIR-\d{3}|INT-\d{3})\b"
    return list(set(re.findall(pattern, text)))

def check_no_cycles(dep_graph: dict) -> tuple:
    """Detect cycles in dependency graph using DFS. Returns (has_cycle, cycle_path)."""
    visited = {}  # 0: unvisited, 1: visiting, 2: visited
    parent = {}

    def dfs(node):
        visited[node] = 1
        for neighbor in dep_graph.get(node, []):
            if neighbor not in dep_graph:
                continue
            if visited.get(neighbor, 0) == 1:
                # Cycle found
                cycle = [neighbor, node]
                curr = node
                while curr in parent and parent[curr] != neighbor:
                    curr = parent[curr]
                    cycle.append(curr)
                cycle.append(neighbor)
                cycle.reverse()
                return True, cycle
            elif visited.get(neighbor, 0) == 0:
                parent[neighbor] = node
                has_c, c_path = dfs(neighbor)
                if has_c:
                    return True, c_path
        visited[node] = 2
        return False, []

    for n in dep_graph:
        if visited.get(n, 0) == 0:
            has_c, c_path = dfs(n)
            if has_c:
                return True, c_path
    return False, []
