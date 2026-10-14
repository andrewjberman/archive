#!/usr/bin/env python3
"""cite_check -- re-open every {file, line, text} cited in r41/C_SWITCH_READ.json (AR-y-326, criterion AR326-y-AC2).

Paths are relative to the worktree root, which is derived from this file's own location (no hardcoded device path).
A citation passes when the file exists, the line number exists, and the cited text (stripped) is a substring of
that line (stripped). Prints CITES-OK <n> of <n> only when every citation passes; otherwise CITES-BAD <file>:<line>
per miss and exits 1.
"""
import json
import os
import sys


def worktree_root():
    here = os.path.dirname(os.path.abspath(__file__))
    # <root>/org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~135
    return os.path.normpath(os.path.join(here, "..", "..", "..", "..", "..", "..", ".."))


def citations(record):
    out = []
    for key in ("q1", "q2", "q3"):
        block = record.get(key) or {}
        for item in block.get("evidence") or []:
            out.append(item)
    return out


def main():
    root = worktree_root()
    here = os.path.dirname(os.path.abspath(__file__))
    record_path = os.path.join(here, "r41", "C_SWITCH_READ.json")
    try:
        with open(record_path, encoding="utf-8") as fh:
            record = json.load(fh)
    except (OSError, ValueError) as exc:
        print("CITES-BAD record unreadable: %s" % exc.__class__.__name__)
        return 1
    cites = citations(record)
    n = len(cites)
    misses = []
    cache = {}
    for item in cites:
        rel = item.get("file", "")
        line_no = item.get("line")
        text = item.get("text", "")
        tag = "%s:%s" % (rel, line_no)
        if not isinstance(rel, str) or not isinstance(line_no, int) or not isinstance(text, str):
            misses.append(tag)
            continue
        if rel not in cache:
            full = os.path.join(root, *rel.split("/"))
            try:
                with open(full, encoding="utf-8") as fh:
                    cache[rel] = fh.read().splitlines()
            except (OSError, UnicodeDecodeError):
                cache[rel] = None
        lines = cache[rel]
        if lines is None or not (1 <= line_no <= len(lines)):
            misses.append(tag)
            continue
        if text.strip() not in lines[line_no - 1].strip() or not text.strip():
            misses.append(tag)
    if misses:
        for tag in misses:
            print("CITES-BAD %s" % tag)
        print("CITES-BAD %d of %d" % (len(misses), n))
        return 1
    print("CITES-OK %d of %d" % (n, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
