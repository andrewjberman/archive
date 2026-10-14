#!/usr/bin/env python3
"""cite_check.py -- AR329-y-AC2 for IRPT_ANLREQ.TO-AR-y-329.

Re-opens every {file, line, text} cite of the record (paths relative to the worktree root,
found by walking up from this script to the directory that holds .tools). A cite passes when
the line number exists and the cited text, stripped, is a substring of that line (stripped).
Prints CITES-OK <n> of <n> only when every cite passes; otherwise CITES-BAD <file>:<line> per
miss and exit 1. The record path defaults to r41/COMMENTARY_PDF_ROUTE_READ.json; argv[1]
may name another record (used for the mutant control).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.join(HERE, "r41", "COMMENTARY_PDF_ROUTE_READ.json")


def worktree_root():
    probe = HERE
    while True:
        if os.path.isdir(os.path.join(probe, ".tools")):
            return probe
        parent = os.path.dirname(probe)
        if parent == probe:
            return None
        probe = parent


def collect(node, out):
    """Every dict holding file, line and text, at any depth."""
    if isinstance(node, dict):
        if {"file", "line", "text"} <= set(node):
            out.append(node)
        for value in node.values():
            collect(value, out)
    elif isinstance(node, list):
        for value in node:
            collect(value, out)
    return out


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    root = worktree_root()
    if root is None:
        print("CITES-BAD no worktree root (.tools not found above %s)" % HERE)
        return 1
    with open(path, encoding="utf-8") as fh:
        record = json.load(fh)
    cites = collect(record, [])
    misses = []
    cache = {}
    for cite in cites:
        rel, line, text = cite["file"], cite["line"], cite["text"]
        if rel not in cache:
            full = os.path.join(root, *rel.split("/"))
            try:
                with open(full, encoding="utf-8", errors="replace") as fh:
                    cache[rel] = fh.read().splitlines()
            except OSError:
                cache[rel] = None
        lines = cache[rel]
        ok = (lines is not None and isinstance(line, int) and 1 <= line <= len(lines)
              and text.strip() != "" and text.strip() in lines[line - 1].strip())
        if not ok:
            misses.append("%s:%s" % (rel, line))
    n = len(cites)
    if misses:
        for miss in misses:
            print("CITES-BAD " + miss)
        print("CITES-BAD %d of %d cites missed" % (len(misses), n))
        return 1
    print("CITES-OK %d of %d" % (n, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
