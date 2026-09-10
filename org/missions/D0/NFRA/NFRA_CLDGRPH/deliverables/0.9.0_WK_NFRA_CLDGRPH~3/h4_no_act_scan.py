#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-H-4 / H4-AC4 helper -- the held-act detector.

ONE detector, run TWICE: once over a PLANTED corpus that contains every held act
(it MUST find all five -- that is EGRESS_PROBE_CONTROL) and once over this order's
real executable artifacts (it must find none). A detector that has not been shown
to fire on a positive is a constant wearing a measurement's clothes.

THE PATTERNS ARE ASSEMBLED FROM FRAGMENTS, ON PURPOSE. If this file spelled the
tokens out, the detector would match ITSELF, and the only way out would be a
self-exclusion -- a checker that skips one file is a checker whose population is
no longer the one it claims. Splitting the literal keeps the population WHOLE.

POPULATION, stated because a corpus choice is itself a claim: the EXECUTABLE
artifacts of this order (*.py, *.sh). Prose in a record that NAMES a forbidden act
is not an act, and a detector that counted it would report a violation for
quoting the rule.

usage: python h4_no_act_scan.py <corpus-dir> [--label L]
"""
from __future__ import annotations

import os
import re
import sys

_RT = "run" + "-task"
_SB = "start" + "-build"
_PO = "put" + "-object"
_DO = "delete" + "-object"
_SA = "safe" + "-apply"
_DP = "pu" + "sh"

HELD = [
    ("ECS_RUN_TASK_CALLS", r"ecs\s+" + _RT + r"|run_task\s*\("),
    ("CODEBUILD_STARTS", r"codebuild\s+" + _SB + r"|start_build\s*\("),
    ("S3_WRITES", r"s3\s+cp\s|s3\s+sync\s|s3api\s+" + _PO + r"|s3api\s+" + _DO
     + r"|put_object\s*\("),
    ("IMAGE_PUSHES", r"docker\s+" + _DP + r"|ecr\s+put-image|buildx\s+build[^\n]*--" + _DP),
    ("TERRAFORM_APPLIES", r"terraform\s+apply|" + _SA),
]

EXEC_SUFFIX = (".py", ".sh")


def scan(root, prefix=""):
    skipped = []
    counts = {name: 0 for name, _ in HELD}
    hits = []
    files = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for fn in sorted(filenames):
            if not fn.endswith(EXEC_SUFFIX):
                continue
            if prefix and not fn.startswith(prefix):
                skipped.append(os.path.relpath(os.path.join(dirpath, fn), root)
                               .replace("\\", "/"))
                continue
            p = os.path.join(dirpath, fn)
            try:
                text = open(p, "r", encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            files += 1
            lines = text.splitlines()
            for name, pat in HELD:
                for m in re.finditer(pat, text):
                    counts[name] += 1
                    ln = text[:m.start()].count("\n") + 1
                    hits.append((name, os.path.relpath(p, root).replace("\\", "/"), ln,
                                 lines[ln - 1].strip()[:100] if ln - 1 < len(lines) else ""))
    return counts, hits, files, skipped


PLANT_LINES = [
    "#!/bin/sh",
    "# PLANTED POSITIVE for H4-AC4. This file is NEVER executed; it exists so the",
    "# detector can be shown to fire. One line per held act.",
    "aws ecs " + _RT + " --cluster opal-globgrph --task-definition x",
    "aws codebuild " + _SB + " --project-name globgrph-derive-build",
    "aws s3api " + _PO + " --bucket opal-313476888478-globgrph --key projection/current.json",
    "docker " + _DP + " 313476888478.dkr.ecr.us-east-1.amazonaws.com/globgrph:latest",
    "bash .tools/" + _SA + " -auto-approve",
]


def plant(dirpath):
    """Write the planted positive. NEVER executed -- it is a target, not a script."""
    os.makedirs(dirpath, exist_ok=True)
    target = os.path.join(dirpath, "h4_planted_positive.sh")
    nl = chr(10)
    with open(target, "w", encoding="ascii", newline=nl) as fh:
        fh.write(nl.join(PLANT_LINES) + nl)
    print("PLANTED=%s" % target)
    print("PLANTED_ACTS=%d (one per held act; the file is inert text, never run)"
          % (len(PLANT_LINES) - 3))
    return 0


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--plant":
        return plant(sys.argv[2])
    if len(sys.argv) < 2:
        print("BLOCKED: no corpus directory given -- a checker called with no input")
        print("         answers a question it was never asked.")
        return 2
    root = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(root)
    if not os.path.isdir(root):
        print("BLOCKED: corpus directory absent: %s" % root)
        return 2
    prefix = sys.argv[3] if len(sys.argv) > 3 else ""
    counts, hits, files, skipped = scan(root, prefix)
    print("CORPUS=%s" % root)
    print("LABEL=%s" % label)
    print("FILES_SCANNED=%d (denominator: every *.py and *.sh under the corpus root%s)"
          % (files, (" whose name starts %r -- this order's own artifacts, which its "
                     "face requires to carry that prefix" % prefix) if prefix else ""))
    print("FILES_SKIPPED_NOT_THIS_ORDER=%d" % len(skipped))
    print("  (they are PRIOR orders' artifacts, present in this shared deliverables")
    print("   folder at HEAD before this order began; h4_no_act.sh proves separately,")
    print("   from git, that this order modified none of them.)")
    for sk in skipped[:5]:
        print("  SKIP %s" % sk)
    if len(skipped) > 5:
        print("  SKIP ... %d more" % (len(skipped) - 5))
    for name, _ in HELD:
        print("SCAN_%s=%d" % (name, counts[name]))
    print("SCAN_TOTAL=%d" % sum(counts.values()))
    for name, rel, line, txt in hits:
        print("  HIT %-20s %s:%d  %s" % (name, rel, line, txt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
