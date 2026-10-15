"""Cite check for the AR-y-348 record r41/STAFF_FIRMS_CATALOGUE_READ.json.

Every {file, line, text} object anywhere in the record is re-opened. A cite with no `ref` is read
from the worktree on disk. A cite with `ref` is read with `git show <ref>:<file>` in the repository
named by `repo` ("worktree" by default, "portal" for the portal repository). A cite passes when its
line number exists and the cited text, stripped, is a substring of that line, stripped.

Prints CITES-OK <n> of <n> when every cite passes; otherwise one CITES-BAD <file>:<line> per miss
and exit 1. ASCII only. Run as: python <this file>
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.join(HERE, "r41", "STAFF_FIRMS_CATALOGUE_READ.json")


def find_root(start):
    cur = start
    while True:
        if os.path.isdir(os.path.join(cur, ".tools")) and os.path.isdir(os.path.join(cur, "org")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


ROOT = find_root(HERE)


def portal_repo():
    cands = []
    if ROOT:
        cands.append(os.path.join(ROOT, "portal"))
        cands.append(os.path.join(os.path.dirname(ROOT), "ajb_workspace", "portal"))
    return cands


def collect(node, out):
    if isinstance(node, dict):
        if "file" in node and "line" in node and "text" in node:
            out.append(node)
        for v in node.values():
            collect(v, out)
    elif isinstance(node, list):
        for v in node:
            collect(v, out)


def read_lines(cite):
    """Return the list of lines the cite names, or None when the source cannot be opened."""
    file_path = cite["file"]
    ref = cite.get("ref")
    if not ref:
        if ROOT is None:
            return None
        full = os.path.join(ROOT, file_path.replace("/", os.sep))
        if not os.path.isfile(full):
            return None
        with open(full, "rb") as fh:
            data = fh.read()
        return data.decode("utf-8").splitlines()
    repo = cite.get("repo", "worktree")
    if repo == "portal":
        cwd_list = portal_repo()
    else:
        cwd_list = [ROOT] if ROOT else []
    for cwd in cwd_list:
        if not cwd or not os.path.isdir(cwd):
            continue
        proc = subprocess.run(["git", "show", "%s:%s" % (ref, file_path)], cwd=cwd,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode == 0:
            return proc.stdout.decode("utf-8").splitlines()
    return None


def main():
    if not os.path.isfile(RECORD):
        print("CITES-BAD r41/STAFF_FIRMS_CATALOGUE_READ.json:0 (record not found)")
        sys.exit(1)
    with open(RECORD, "r", encoding="utf-8") as fh:
        rec = json.load(fh)
    cites = []
    collect(rec, cites)
    misses = []
    for c in cites:
        lines = read_lines(c)
        label = "%s:%s" % (c["file"], c["line"])
        if lines is None:
            misses.append(label)
            continue
        try:
            n = int(c["line"])
        except (TypeError, ValueError):
            misses.append(label)
            continue
        if n < 1 or n > len(lines):
            misses.append(label)
            continue
        want = str(c["text"]).strip()
        got = lines[n - 1].strip()
        if not want or want not in got:
            misses.append(label)
    for m in misses:
        print("CITES-BAD " + m)
    if misses:
        sys.exit(1)
    print("CITES-OK %d of %d" % (len(cites), len(cites)))
    sys.exit(0)


if __name__ == "__main__":
    main()
