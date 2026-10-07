#!/usr/bin/env python3
"""check_trace_round3 -- the saved round-3 trace is the live run, and the live run has no hole, no shared target and no
bare not-asked line (LGIC_BLANKFIX.TO-BF-r-5).

Runs the root check again from the worktree root, compares its output with THREAD_TRACE_round3_bd-pipeline.txt line for
line, and checks the live output. Last line: TRACE-R3 ok=True items=N hole=0 differs=0 (ok=False on any failure, each
named on its own line above).
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([".."] * 7)))  # deliverables/<serial> -> worktree root
SAVED = os.path.join(HERE, "THREAD_TRACE_round3_bd-pipeline.txt")
CMD = [sys.executable, "lib/opal_naming_rootcheck.py", "infra/aws/terraform/bd-pipeline",
       "--map", "infra/logic/registry/root_map.json", "--report-only"]
KINDS = ("RIGHT", "FIX", "NOT-ASKED", "PATTERN", "CARDED", "REFUSED", "HOLE")
LINE_RE = re.compile(r"^(RIGHT|FIX|NOT-ASKED|PATTERN|CARDED|REFUSED|HOLE) (\S+) (.*?) -> (.*)  \[([^\]]*)\]$")
COUNT_RE = re.compile(r"^ROOTCHECK ok=(\w+) root=\S+ items=(\d+) right=(\d+) fix=(\d+) not_asked=(\d+) pattern=(\d+) "
                      r"carded=(\d+) refused=(\d+) hole=(\d+)$")


def main():
    bad = []
    items = hole = differs = 0
    p = subprocess.run(CMD, cwd=ROOT, capture_output=True, timeout=300)
    live = p.stdout.decode("utf-8", "replace").replace("\r\n", "\n").split("\n")
    while live and live[-1] == "":
        live.pop()
    if p.returncode != 0:
        bad.append("the live run exited %d: %s" % (p.returncode, p.stderr.decode("utf-8", "replace")[-300:]))
    try:
        with open(SAVED, "rb") as fh:
            saved = fh.read().decode("utf-8").replace("\r\n", "\n").split("\n")
    except OSError as exc:
        saved = []
        bad.append("the saved trace is unreadable: %s" % (exc,))
    while saved and saved[-1] == "":
        saved.pop()
    for i in range(max(len(live), len(saved))):
        a = live[i] if i < len(live) else None
        b = saved[i] if i < len(saved) else None
        if a != b:
            differs += 1
            bad.append("line %d differs: live=%r saved=%r" % (i + 1, a, b))
    m = COUNT_RE.match(live[-1]) if live else None
    if not m:
        bad.append("the live run's last line is not a ROOTCHECK count line: %r" % (live[-1:],))
    else:
        items, hole = int(m.group(2)), int(m.group(9))
        counts = [int(g) for g in m.groups()[2:]]
        if hole != 0:
            bad.append("hole=%d, not 0" % hole)
        if sum(counts) != items:
            bad.append("the seven counts sum to %d, items=%d" % (sum(counts), items))
        rows = live[:-1]
        if len(rows) != items:
            bad.append("%d lines for items=%d" % (len(rows), items))
        targets = {}
        seen = dict((k, 0) for k in KINDS)
        for line in rows:
            r = LINE_RE.match(line)
            if not r:
                bad.append("a line that is not one of the seven kinds: " + line)
                continue
            kind, typ, cur, detail = r.group(1), r.group(2), r.group(3), r.group(4)
            seen[kind] += 1
            if kind == "FIX":
                if "{" in line:
                    bad.append("a FIX line contains '{': " + line)
                targets.setdefault((typ, detail), set()).add(cur)
            if kind == "NOT-ASKED" and "rename" not in line:
                bad.append("a NOT-ASKED line without 'rename': " + line)
        for (typ, target), names in sorted(targets.items()):
            if len(names) > 1:
                bad.append("%s names %s share the FIX target %s" % (typ, ", ".join(sorted(names)), target))
        if [seen[k] for k in KINDS] != counts:
            bad.append("the lines' kinds %s do not match the count line %s" % ([seen[k] for k in KINDS], counts))
    for b in bad:
        print("FAIL: " + b)
    print("TRACE-R3 ok=%s items=%d hole=%d differs=%d" % (not bad, items, hole, differs))
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
