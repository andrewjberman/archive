"""AR342-y-AC2: re-open every {file, line, text} cited in the FWD-1 prerequisites record.

Usage: python cite_check.py [record_path]
A cited file is read from the worktree root (this script lives seven folders below it). Each cite must
name an existing line whose stripped text contains the cited text (stripped). Prints CITES-OK <n> of <n>
(rc 0) or one CITES-BAD <file>:<line> per miss (rc 1), always with the denominator n.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, *([os.pardir] * 7)))
DEFAULT = os.path.join(HERE, "r41", "FWD1_PREREQ_READ.json")


def walk(node, out):
    if isinstance(node, dict):
        if {"file", "line", "text"} <= set(node):
            out.append(node)
        for value in node.values():
            walk(value, out)
    elif isinstance(node, list):
        for value in node:
            walk(value, out)
    return out


def main(path):
    if not os.path.isdir(os.path.join(ROOT, ".tools")):
        print("CITES-BAD root-not-found:%s" % ROOT)
        return 1
    with open(path, encoding="utf-8") as fh:
        rec = json.load(fh)
    cites = walk(rec, [])
    n = len(cites)
    misses = []
    cache = {}
    for c in cites:
        rel, line_no, text = c["file"], c["line"], c["text"]
        full = os.path.join(ROOT, rel)
        if rel not in cache:
            try:
                with open(full, encoding="utf-8", errors="replace") as fh:
                    cache[rel] = fh.read().splitlines()
            except OSError:
                cache[rel] = None
        lines = cache[rel]
        ok = False
        if lines is not None and isinstance(line_no, int) and 1 <= line_no <= len(lines):
            ok = isinstance(text, str) and text.strip() != "" and text.strip() in lines[line_no - 1].strip()
        if not ok:
            misses.append("%s:%s" % (rel, line_no))
    for m in misses:
        print("CITES-BAD " + m)
    if misses:
        print("CITES-BAD denominator=%d misses=%d" % (n, len(misses)))
        return 1
    print("CITES-OK %d of %d" % (n, n))
    return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    sys.exit(main(target))
