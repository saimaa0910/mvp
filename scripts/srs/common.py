"""
common.py
Shared utilities for line counting, duplicate paragraph detection,
and Markdown formatting for SRS and Architecture documentation.
"""

import re
from typing import Dict, List, Tuple

HEADER_RE = re.compile(r"^#{1,6}\s+")
TABLE_ROW_RE = re.compile(r"^\|.*\|$")
TABLE_SEP_RE = re.compile(r"^\|(\s*:?-+:?\s*\|)+$")
BLOCK_QUOTE_RE = re.compile(r"^>\s*")

def count_lines(content: str) -> Dict[str, int]:
    """
    Substantive line counting algorithm:
    - Blank lines: 0
    - Pure markdown separators (---, ***): 0
    - Repeated markdown table divider rows (| :--- | :--- |): 0
    - Headings with text: 1 substantive line
    - Table content rows: 1 substantive line
    - Mermaid diagram code lines: 1 substantive line
    - Code block lines: 1 substantive line
    - Normal paragraphs / bullets / lists: 1 substantive line
    """
    lines = content.splitlines()
    total = len(lines)
    substantive = 0
    blank = 0
    heading = 0
    separator = 0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            blank += 1
            continue
        if stripped in ["---", "***", "___"]:
            separator += 1
            continue
        if TABLE_SEP_RE.match(stripped):
            separator += 1
            continue
        if HEADER_RE.match(stripped):
            heading += 1
            substantive += 1
            continue

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
        paragraphs = content.split("\n\n")
        for p in paragraphs:
            cleaned = " ".join(p.split()).strip()
            if len(cleaned) < min_len:
                continue
            if cleaned.startswith("#") or cleaned.startswith("|") or cleaned.startswith("```"):
                continue
            if cleaned in seen:
                orig_doc = seen[cleaned]
                if orig_doc != doc_name:
                    duplicates.append((orig_doc, doc_name, cleaned[:80] + "..."))
            else:
                seen[cleaned] = doc_name

    return duplicates
