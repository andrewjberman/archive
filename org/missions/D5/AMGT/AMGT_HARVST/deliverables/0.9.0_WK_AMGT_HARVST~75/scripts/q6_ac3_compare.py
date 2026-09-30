"""HVST-q-6 AC3: compare the pinned BASE pytest run of lib/opal_data_harvest/ (commit ff4405d3d5) with the
AFTER run. Reads the two saved `pytest -rA` outputs; prints both counts, the set difference of PASSED
test ids, and the failed count. Local file reads only.

Run: python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~75/scripts/q6_ac3_compare.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIVERABLE = HERE.parent
BASE_COMMIT = "ff4405d3d5"


def read(name):
    text = (DELIVERABLE / name).read_text(encoding="utf-8")
    passed = {line[len("PASSED "):].strip() for line in text.splitlines() if line.startswith("PASSED ")}
    failed = [line for line in text.splitlines() if line.startswith(("FAILED ", "ERROR "))]
    summary = [line for line in text.splitlines() if re.search(r"\d+ passed", line)][-1].strip("= ")
    return passed, failed, summary


def main():
    base, base_failed, base_summary = read("q6_ac3_base_output.txt")
    after, after_failed, after_summary = read("q6_ac3_after_output.txt")
    lost = sorted(base - after)
    gained = sorted(after - base)
    print("BASE  (%s, lib/opal_data_harvest identical to worktree HEAD 0cfb3406bf): %s" % (BASE_COMMIT, base_summary))
    print("AFTER (this branch)                                       : %s" % after_summary)
    print("BASE  passed=%d failed=%d" % (len(base), len(base_failed)))
    print("AFTER passed=%d failed=%d" % (len(after), len(after_failed)))
    print("passed at base and not passing after: %d of %d %s" % (len(lost), len(base), lost))
    new_files = {g.split("::")[0] for g in gained}
    print("newly passing after: %d, all in %s" % (len(gained), sorted(new_files)))
    print("%d failed" % len(after_failed))
    return 1 if lost or after_failed else 0


if __name__ == "__main__":
    sys.exit(main())
