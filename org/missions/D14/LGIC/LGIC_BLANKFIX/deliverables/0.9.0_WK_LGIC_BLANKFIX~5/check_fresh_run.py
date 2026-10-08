#!/usr/bin/env python3
"""check_fresh_run.py -- BU7-AC1 of LGIC_BLANKFIX.TO-BF-u-7.

Checks FRESH_RUN_round6.md (beside this file): the five `## ` headings in order, one fenced block under
`Final output`, and counts outside_writes = the `git status --porcelain` entries of this worktree that lie
outside this deliverables folder. `finished` is the record's own `finished: yes|no` line (reported, not required).
Prints exactly one line. ASCII only; standard library only.
"""
import os
import subprocess
import sys

HEADINGS = ["Instructions found", "Steps run", "Final output", "Written for the run",
            "Where the instructions fell short"]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    record = os.path.join(here, "FRESH_RUN_round6.md")
    with open(record, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    # headings: the `## ` lines outside fences, in order
    heads, in_fence, final_fences, finished = [], False, 0, "no"
    current = None
    for ln in lines:
        if ln.startswith("```"):
            in_fence = not in_fence
            if in_fence and current == "Final output":
                final_fences += 1
            continue
        if in_fence:
            continue
        if ln.startswith("## "):
            current = ln[3:].strip()
            heads.append(current)
        elif current == "Final output" and ln.strip().lower() in ("finished: yes", "finished: no"):
            finished = ln.strip().lower().split(":")[1].strip()
    headings_ok = heads == HEADINGS
    block_ok = final_fences == 1 and not in_fence

    top = subprocess.run(["git", "-C", here, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    out = subprocess.run(["git", "-C", top, "status", "--porcelain", "-z", "--untracked-files=all"],
                         capture_output=True, text=True).stdout
    mine = os.path.relpath(here, top).replace("\\", "/") + "/"
    outside = 0
    for ent in [e for e in out.split("\0") if e]:
        path = ent[3:].replace("\\", "/")
        if not path.startswith(mine):
            outside += 1
    ok = headings_ok and block_ok and outside == 0
    print("FRESH-RUN ok=%s headings=%d outside_writes=%d finished=%s" % (
        ok, len(heads) if headings_ok else 0, outside, finished))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
