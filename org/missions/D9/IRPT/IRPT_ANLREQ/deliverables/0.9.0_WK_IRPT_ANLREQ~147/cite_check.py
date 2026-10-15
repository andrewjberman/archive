"""AR343-y-AC2: re-open every {file, line, text} cite of r41/FWD1_RUN_MECHANICS_READ.json.

A cite is a path relative to the worktree root. A cite carrying a "ref" key is read from the git
blob at that ref (the portal repository; a leading "portal/" is stripped for git). Each cited line
number must exist and the cited text must be a substring of that line after stripping.

Prints CITES-OK <n> of <n> when every cite holds; otherwise CITES-BAD <file>:<line> per miss, exit 1.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# HERE is <root>/org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/<serial>; seven levels up is <root>.
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
PORTAL = os.path.join(ROOT, "portal")
REC = os.path.join(HERE, "r41", "FWD1_RUN_MECHANICS_READ.json")


def collect(node, out):
    if isinstance(node, dict):
        if {"file", "line", "text"} <= set(node.keys()):
            out.append(node)
        for v in node.values():
            collect(v, out)
    elif isinstance(node, list):
        for v in node:
            collect(v, out)
    return out


def lines_of(cite):
    path = cite["file"]
    ref = cite.get("ref")
    if ref:
        rel = path[len("portal/"):] if path.startswith("portal/") else path
        proc = subprocess.run(["git", "-C", PORTAL, "show", "%s:%s" % (ref, rel)],
                              capture_output=True)
        if proc.returncode != 0:
            return None
        return proc.stdout.decode("utf-8", "replace").splitlines()
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full):
        return None
    with open(full, encoding="utf-8", errors="replace") as fh:
        return fh.read().splitlines()


def main():
    with open(REC, encoding="utf-8") as fh:
        rec = json.load(fh)
    cites = collect(rec, [])
    if not cites:
        print("CITES-BAD none: the record carries no {file, line, text} cite")
        sys.exit(1)
    misses = []
    for c in cites:
        where = "%s:%s" % (c["file"], c["line"])
        try:
            n = int(c["line"])
        except (TypeError, ValueError):
            misses.append(where)
            continue
        body = lines_of(c)
        if body is None or n < 1 or n > len(body):
            misses.append(where)
            continue
        needle = str(c["text"]).strip()
        if not needle or needle not in body[n - 1].strip():
            misses.append(where)
    for w in misses:
        print("CITES-BAD " + w)
    if misses:
        sys.exit(1)
    print("CITES-OK %d of %d" % (len(cites), len(cites)))


if __name__ == "__main__":
    main()
