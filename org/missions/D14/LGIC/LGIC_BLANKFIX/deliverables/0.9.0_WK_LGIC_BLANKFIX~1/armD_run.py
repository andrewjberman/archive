#!/usr/bin/env python3
"""armD_run -- run the FWD-6 design's arm D act on a scratch copy of one schedule file and print the root check's lines.

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~1/armD_run.py

The act: in the scratch copy armD_scratch/directory_cron_edit.tf.txt (beside this file) the expression of the schedule `irpt-directory-refresh`
(a name that carries no cadence word, FIX today) is `cron(0/7 9 ? * MON-FRI *)`, which the cadence reader cannot decide. Only the
cadence reader is pointed at the scratch text (its `_read` is wrapped for that one path); nothing under infra/ is written.
Run from the repository root. Prints the HEAD run, then the scratch run, each with its HOLE count, and one last line.
Python 3.9; ASCII only; standard library only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def repo_root(start):
    d = start
    for _ in range(40):
        if os.path.isdir(os.path.join(d, ".tools")) and os.path.isdir(os.path.join(d, "org")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("ARMD ok=False (no repository root above %s)" % start)


ROOT = repo_root(HERE)
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "lib"))
import opal_naming_cadence  # noqa: E402
import opal_naming_rootcheck  # noqa: E402

TARGET = "infra/aws/terraform/investor-reporting/directory/schedule.tf"
SCRATCH = os.path.join(HERE, "armD_scratch", "directory_cron_edit.tf.txt")
MAP = "infra/logic/registry/root_map.json"
ROOT_DIR = "infra/aws/terraform/investor-reporting/directory"


def run_root():
    buf, sink = [], []
    opal_naming_rootcheck.check_root(ROOT_DIR, MAP, out=buf.append, report_only=True, sink=sink)
    return buf


def main():
    before = run_root()
    real_read = opal_naming_cadence._read

    def read(path):
        if os.path.relpath(path).replace("\\", "/") == TARGET:
            return real_read(SCRATCH)
        return real_read(path)

    opal_naming_cadence._read = read
    try:
        after = run_root()
    finally:
        opal_naming_cadence._read = real_read
    key = "irpt-directory-refresh "
    nb = sum(1 for ln in before if ln.startswith("HOLE "))
    na = sum(1 for ln in after if ln.startswith("HOLE "))
    print("--- HEAD text: the line of the schedule")
    for ln in before:
        if key in ln:
            print(ln)
    print("--- scratch text (cron(0/7 9 ? * MON-FRI *)): the line of the schedule")
    for ln in after:
        if key in ln:
            print(ln)
    print("--- HOLE lines after")
    for ln in after:
        if ln.startswith("HOLE "):
            print(ln)
    print("ARMD ok=%s holes_head=%d holes_scratch=%d grew=%s" % (na > nb, nb, na, na > nb))
    return 0 if na > nb else 1


if __name__ == "__main__":
    sys.exit(main())
