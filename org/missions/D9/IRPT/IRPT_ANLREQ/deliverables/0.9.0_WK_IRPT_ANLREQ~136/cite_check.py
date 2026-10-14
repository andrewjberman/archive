"""AR-y-328 cite check: re-opens every {file, line, text} of r41/RESIDENT_BINDINGS_READ.json.

A cite passes when its file exists under the worktree root, its line number exists, and the cited text (stripped)
is a substring of that line (stripped). Prints CITES-OK <n> of <n> (exit 0), or one CITES-BAD <file>:<line> per miss
and exits 1. The denominator n is every cite in the record. ASCII only.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.join(HERE, "r41", "RESIDENT_BINDINGS_READ.json")


def repo_root(start):
    d = start
    while True:
        if os.path.isdir(os.path.join(d, "org")) and os.path.isdir(os.path.join(d, ".tools")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def collect(doc):
    out = []
    for row in doc.get("q1", []):
        out.append(("q1.read_at", row.get("read_at")))
        out.append(("q1.when_unset_evidence", row.get("when_unset_evidence")))
    for row in doc.get("q2", []):
        for c in row.get("evidence", []):
            out.append(("q2.evidence", c))
    out.extend(("mechanism_evidence", c) for c in doc.get("mechanism_evidence", []))
    for row in doc.get("q3", []):
        for c in row.get("evidence", []):
            out.append(("q3.evidence", c))
    q4 = doc.get("q4", {})
    out.append(("q4.edit_site", q4.get("edit_site")))
    out.extend(("q4.must_agree", c) for c in q4.get("must_agree", []))
    return out


def main():
    root = repo_root(HERE)
    if root is None:
        print("CITES-BAD no worktree root above %s" % HERE)
        return 1
    with open(RECORD, encoding="utf-8") as fh:
        doc = json.load(fh)
    cases = collect(doc)
    n = len(cases)
    bad = []
    cache = {}
    for where, c in cases:
        if not isinstance(c, dict) or not isinstance(c.get("file"), str) or not isinstance(c.get("line"), int):
            bad.append("%s:%s" % (where, "malformed"))
            continue
        path = os.path.join(root, *c["file"].split("/"))
        if path not in cache:
            if not os.path.isfile(path):
                cache[path] = None
            else:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    cache[path] = fh.read().split("\n")
        lines = cache[path]
        if lines is None or not (1 <= c["line"] <= len(lines)):
            bad.append("%s:%s" % (c["file"], c["line"]))
            continue
        needle = str(c.get("text", "")).strip()
        if not needle or needle not in lines[c["line"] - 1].strip():
            bad.append("%s:%s" % (c["file"], c["line"]))
    if bad:
        for b in bad:
            print("CITES-BAD " + b)
        print("CITES-BAD %d of %d cites missed" % (len(bad), n))
        return 1
    print("CITES-OK %d of %d" % (n, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
