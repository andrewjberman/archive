#!/usr/bin/env python3
"""i2_grade -- capture, determinism control and grading control for TO-CG-I-2.

Not a criterion. Three jobs:
  1. run each mechanical criterion's EXACT invocation and store its capture
  2. run it a SECOND time and compare the two byte for byte (determinism)
  3. match each capture against the criterion's OWN expect regex, and cross-match one
     criterion's regex against another criterion's capture -- an expect that matches
     anything grades nothing.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE
while WS.name and not (WS / ".git").exists():
    WS = WS.parent
D = "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2"

CRIT = {
    "I2-AC1": (["python", "%s/i2_window.py" % D],
               r"WINDOW_BUILT=true[\s\S]*CHECK_SAYS_CLEAN_WHILE_BLIND=true[\s\S]*"
               r"BASELINE_CAPTURED=true[\s\S]*NODE_ABSENT_EDGE_PRESENT=([1-9][0-9]*)[\s\S]*"
               r"NEGATIVE_CONTROL=FIRED"),
    "I2-AC2": (["python", "%s/i2_consumers.py" % D],
               r"AWS_KEYS_CONSUMERS=([0-9]+) of ([1-9][0-9]*) scanned[\s\S]*"
               r"TREE_READ=(MAIN|WORKTREE)[\s\S]*"
               r"TREE_POSITIVE_CONTROL=(FIRED|N/A-MAIN-TREE)[\s\S]*EACH_CONSUMER_NAMED"),
    "I2-AC3": (["python", "%s/i2_check_sees.py" % D],
               r"REMEDY=(EDGE_SIDE_DROP|AWS_KEYS_MOVED)[\s\S]*WHY printed[\s\S]*"
               r"CHECK_SEES_WINDOW=true[\s\S]*BLIND_BEFORE=true[\s\S]*SEEING_AFTER=true"),
    "I2-AC4": (["bash", "%s/i2_no_egress.sh" % D],
               r"ECS_RUN_TASK_CALLS=0[\s\S]*CODEBUILD_STARTS=0[\s\S]*S3_WRITES=0[\s\S]*"
               r"IMAGE_PUSHES=0[\s\S]*TERRAFORM_APPLIES=0[\s\S]*MAGNITUDE_MANUFACTURED=false"
               r"[\s\S]*EGRESS_PROBE_CONTROL=FIRED"),
}


sys.path.insert(0, str(WS / ".tools"))
from git_bash_resolver import git_bash                              # noqa: E402


def run(cmd):
    # a python-spawned bare `bash` resolves to the System32 WSL stub, not Git Bash
    if cmd and cmd[0] == "bash":
        cmd = [git_bash()] + cmd[1:]
    p = subprocess.run(cmd, cwd=str(WS), capture_output=True, timeout=115)
    return p.returncode, p.stdout.decode("utf-8", "replace").replace("\r\n", "\n")


def graded_lines(txt: str) -> str:
    """The TOKEN lines a criterion's expect actually reads -- the rest is prose that carries
    HEAD hashes and the comp-rail's own telemetry counts, both of which move by construction."""
    keep = [ln for ln in txt.splitlines()
            if re.match(r"^[A-Z][A-Z0-9_]*=", ln) or ln.startswith(("GRADE ", "CROSS-"))]
    return "\n".join(keep)


def main() -> int:
    ok = True
    caps = {}
    for cid, (cmd, _pat) in CRIT.items():
        rc1, out1 = run(cmd)
        rc2, out2 = run(cmd)
        cap = HERE / ("i2_%s_run.txt" % cid.lower().replace("i2-", "").replace("-", "_"))
        cap.write_text(out1, encoding="utf-8", newline="\n")
        caps[cid] = out1
        same = (out1 == out2)
        same_graded = (graded_lines(out1) == graded_lines(out2))
        print("%s rc=%d rc(2nd)=%d bytes=%d DETERMINISM(full stdout)=%s"
              " DETERMINISM(graded token lines)=%s -> %s"
              % (cid, rc1, rc2, len(out1), "STABLE" if same else "UNSTABLE",
                 "STABLE" if same_graded else "UNSTABLE", cap.name))
        if not same:
            for l1, l2 in zip(out1.splitlines(), out2.splitlines()):
                if l1 != l2:
                    print("    DRIFTED: run1 %s" % l1.strip()[:120])
                    print("             run2 %s" % l2.strip()[:120])
        if rc1 != 0 or not same_graded:
            ok = False

    print("")
    for cid, (_cmd, pat) in CRIT.items():
        m = re.search(pat, caps[cid])
        print("GRADE %s own-expect MATCH=%s" % (cid, bool(m)))
        if not m:
            ok = False

    # cross-negative controls: an expect that matches another criterion's capture is not an expect
    for a, b in (("I2-AC1", "I2-AC4"), ("I2-AC3", "I2-AC2"), ("I2-AC4", "I2-AC1")):
        m = re.search(CRIT[a][1], caps[b])
        print("CROSS-NEGATIVE %s pattern vs %s capture MATCH=%s (must be False)"
              % (a, b, bool(m)))
        if m:
            ok = False

    print("")
    print("GRADING_CONTROL=%s" % ("FIRED" if ok else "FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
