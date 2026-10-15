#!/usr/bin/env python3
"""AR-y-357 cite check: every {file, line, text} object in r41/PACKAGE_REFUSAL_READ.json is re-read.

Each cited file is read at the record's own base sha (git show <base>:<file>), because the infra/ tree is
skip-worktree and is not on disk. A citation passes when its line number exists and its stripped text is a
substring of that line (stripped). Prints CITES-OK <n> of <n> (exit 0), or CITES-BAD <file>:<line> (exit 1).
ASCII only; no AWS.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]  # <worktree>/org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/<serial>
RECORD = HERE / "r41" / "PACKAGE_REFUSAL_READ.json"


def collect(node, out):
    if isinstance(node, dict):
        if {"file", "line", "text"} <= set(node):
            out.append(node)
        for value in node.values():
            collect(value, out)
    elif isinstance(node, list):
        for value in node:
            collect(value, out)
    return out


def blob_lines(base, path):
    proc = subprocess.run(["git", "-C", str(ROOT), "show", "%s:%s" % (base, path)],
                          capture_output=True, check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", errors="replace").splitlines()


def main():
    rec = json.loads(RECORD.read_text(encoding="utf-8"))
    base = rec["base"]
    cites = collect(rec, [])
    cache = {}
    for cite in cites:
        path, line, text = cite["file"], cite["line"], cite["text"]
        if path not in cache:
            cache[path] = blob_lines(base, path)
        lines = cache[path]
        if lines is None or not isinstance(line, int) or not 1 <= line <= len(lines):
            print("CITES-BAD %s:%s" % (path, line))
            return 1
        if not isinstance(text, str) or not text.strip() or text.strip() not in lines[line - 1].strip():
            print("CITES-BAD %s:%s" % (path, line))
            return 1
    print("CITES-OK %d of %d" % (len(cites), len(cites)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
