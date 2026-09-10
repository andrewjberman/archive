#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-I-4 / I4-AC4 helper -- the held-act detector.

ONE detector, run TWICE: over a PLANTED corpus that contains every held act (it MUST find
all five -- that is EGRESS_PROBE_CONTROL) and over this order's real executable artifacts
(it must find none). A detector that has not been shown to fire on a positive is a constant
wearing a measurement's clothes.

THE PATTERNS ARE ASSEMBLED FROM FRAGMENTS, ON PURPOSE. If this file spelled the tokens out,
the detector would match ITSELF and the only way out would be a self-exclusion -- a checker
that skips a file is a checker whose population is no longer the one it claims. Splitting
the literal keeps the population WHOLE.

POPULATION, stated because a corpus choice is itself a claim: the EXECUTABLE artifacts of
this order (i4_*.py, i4_*.sh). Prose in a record that NAMES a forbidden act is not an act,
and a detector that counted it would report a violation for quoting the rule -- this order's
i4_remedy.sh prints six acts NOT to take, in words, and that is not five violations.

usage: python i4_no_write_scan.py <corpus-dir> [label] [prefix]
       python i4_no_write_scan.py --plant <dir>
"""

import os
import re
import sys

P = "p" + "ut-object"
CP = "s3 " + "cp"
SYNC = "s3 " + "sync"
RM = "s3 " + "rm"
DEL = "d" + "elete-object"
RUNTASK = "run-" + "task"
STARTBUILD = "start-" + "build"
DOCKERPUSH = "docker " + "push"
ECRPUT = "put-" + "image"
TFAPPLY = "terraform " + "apply"
SAFEAPPLY = "safe-" + "apply"
BOTO_PUT = "put_" + "object"

ACTS = {
    "S3_WRITES": [P, CP, SYNC, RM, DEL, BOTO_PUT],
    "ECS_RUN_TASK_CALLS": [RUNTASK],
    "CODEBUILD_STARTS": [STARTBUILD],
    "IMAGE_PUSHES": [DOCKERPUSH, ECRPUT],
    "TERRAFORM_APPLIES": [TFAPPLY, SAFEAPPLY],
}

PLANT_TEXT = """# PLANTED POSITIVE for I4-AC4. Inert text, scanned and never run.
aws s3api {p} --bucket b --key k --body f
aws ecs {rt} --cluster c --task-definition t
aws codebuild {sb} --project-name p
{dp} 313476888478.dkr.ecr.us-east-1.amazonaws.com/x:latest
{tf} -auto-approve
"""


def plant(d):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "planted_positive.txt"), "w", encoding="ascii", newline="\n") as fh:
        fh.write(PLANT_TEXT.format(p=P, rt=RUNTASK, sb=STARTBUILD, dp=DOCKERPUSH, tf=TFAPPLY))


def scan(d, prefix=None):
    counts = {k: 0 for k in ACTS}
    hits = []
    files = 0
    for name in sorted(os.listdir(d)):
        if prefix and not name.startswith(prefix):
            continue
        if prefix and not (name.endswith(".py") or name.endswith(".sh")):
            continue
        path = os.path.join(d, name)
        if not os.path.isfile(path):
            continue
        files += 1
        text = open(path, encoding="utf-8", errors="replace").read()
        for act, toks in ACTS.items():
            for t in toks:
                for m in re.finditer(re.escape(t), text):
                    counts[act] += 1
                    line = text.count("\n", 0, m.start()) + 1
                    hits.append("%s:%d %s" % (name, line, act))
    return counts, hits, files


def main():
    if sys.argv[1] == "--plant":
        plant(sys.argv[2])
        print("OK: plant written")
        return 0
    d = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else "CORPUS"
    prefix = sys.argv[3] if len(sys.argv) > 3 else None
    counts, hits, files = scan(d, prefix)
    print("SCAN_LABEL=%s" % label)
    print("SCAN_FILES=%d (population: %s)" % (files, ("%s* .py/.sh" % prefix) if prefix else "every file in the dir"))
    total = 0
    for act in sorted(ACTS):
        print("SCAN_%s=%d" % (act, counts[act]))
        total += 1 if counts[act] else 0
    print("SCAN_TOTAL=%d" % total)
    for h in hits:
        print("SCAN_HIT %s" % h)
    return 0


if __name__ == "__main__":
    sys.exit(main())
