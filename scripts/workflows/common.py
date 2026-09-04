#!/usr/bin/env python3
"""
common.py
Shared utilities, line counting, substantive validation, and formatting helpers
for the Namma Clinic Workflow Engineering Phase (docs/03-workflows/).
"""

import re
from typing import Dict, List, Tuple

SEPARATOR_RE = re.compile(r"^(\s*[-*_]\s*){3,}$")
HEADER_RE = re.compile(r"^#{1,6}\s+")
BULLET_EMPTY_RE = re.compile(r"^[\s*+-]+\s*$")


def count_lines(content: str) -> Dict[str, int]:
    """Calculate total, substantive, blank, heading, and separator lines in markdown content."""
    lines = content.splitlines()
    total = len(lines)
    blank = 0
    heading = 0
    separator = 0
    substantive = 0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            blank += 1
            continue
        if SEPARATOR_RE.match(stripped):
            separator += 1
            continue
        if BULLET_EMPTY_RE.match(stripped):
            blank += 1
            continue
        if HEADER_RE.match(stripped):
            heading += 1
            # A heading with substantive text counts as a substantive line as long as it's not empty
            substantive += 1
            continue

        # Line has content
        substantive += 1

    return {
        "total": total,
        "substantive": substantive,
        "blank": blank,
        "heading": heading,
        "separator": separator,
    }


def find_duplicate_paragraphs(docs: Dict[str, str], min_len: int = 60) -> List[Tuple[str, str, str]]:
    """
    Find duplicate paragraphs >= min_len characters across different documents.
    Returns a list of tuples: (doc1, doc2, paragraph_snippet)
    """
    seen = {}
    duplicates = []

    for doc_name, content in docs.items():
        # Split into paragraphs by double newlines
        paragraphs = content.split("\n\n")
        for p in paragraphs:
            cleaned = " ".join(p.split()).strip()
            # Ignore markdown headers, tables, code blocks, or separator lines for paragraph uniqueness
            if len(cleaned) < min_len:
                continue
            if cleaned.startswith("#") or cleaned.startswith("|") or cleaned.startswith("```"):
                continue
            # Also ignore standard boilerplate references if strictly needed
            if cleaned in seen:
                orig_doc = seen[cleaned]
                if orig_doc != doc_name:
                    duplicates.append((orig_doc, doc_name, cleaned[:80] + "..."))
            else:
                seen[cleaned] = doc_name

    return duplicates
