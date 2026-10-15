"""AR350-y-AC2: cite check of r41/FILING_HINT_DESIGN_READ.json (AR-y-350, worker 0.9.0_WK_IRPT_ANLREQ~151).

Re-opens every {file, line, text} cite of the record. A file is read from the worktree when it exists there; a file
absent from the worktree (skip-worktree) is read as the record's base blob with git show. Prints CITES-OK <n> of <n>
when every cited line number exists and the cited text is a substring of that line (after stripping); otherwise one
CITES-BAD <file>:<line> per miss and exit 1. ASCII only.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.join(HERE, "r41", "FILING_HINT_DESIGN_READ.json")


def worktree_root():
    cur = HERE
    while True:
        if os.path.isdir(os.path.join(cur, ".tools")) and os.path.isdir(os.path.join(cur, "org")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            sys.exit("CITES-BAD no worktree root above " + HERE)
        cur = parent


def collect(node, out):
    if isinstance(node, dict):
        if {"file", "line", "text"} <= set(node.keys()):
            out.append(node)
        for value in node.values():
            collect(value, out)
    elif isinstance(node, list):
        for value in node:
            collect(value, out)
    return out


def main():
    with open(RECORD, encoding="utf-8") as fh:
        rec = json.load(fh)
    root = worktree_root()
    base = rec.get("base", "")
    cites = collect(rec, [])
    cache = {}
    misses = []
    for c in cites:
        path = c["file"]
        if path not in cache:
            disk = os.path.join(root, path)
            if os.path.isfile(disk):
                with open(disk, encoding="utf-8") as fh:
                    cache[path] = fh.read().split("\n")
            else:
                raw = subprocess.run(["git", "-C", root, "show", base + ":" + path], capture_output=True)
                cache[path] = raw.stdout.decode("utf-8", "replace").split("\n") if raw.returncode == 0 else None
        lines = cache[path]
        ok = False
        if lines is not None and isinstance(c["line"], int) and 1 <= c["line"] <= len(lines):
            ok = c["text"].strip() in lines[c["line"] - 1].strip()
        if not ok:
            misses.append("%s:%s" % (path, c["line"]))
    n = len(cites)
    if misses:
        for m in misses:
            print("CITES-BAD " + m)
        sys.exit(1)
    print("CITES-OK %d of %d" % (n, n))


if __name__ == "__main__":
    main()
