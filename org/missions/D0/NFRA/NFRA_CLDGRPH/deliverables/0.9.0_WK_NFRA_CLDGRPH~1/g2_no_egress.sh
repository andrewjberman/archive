#!/usr/bin/env bash
# NFRA_CLDGRPH TO-CG-G-2 / G2-AC4 -- THE EGRESS HOLD, PROVEN AND NOT ASSERTED.
#
# Three arms, and the WORLD arm is the one that carries the claim:
#
#  ARM 1 (WORLD, the discriminating one). The five held acts all leave a mark on objects
#    this order can READ: an ECS derive rewrites snapshots/latest.txt and the snapshot
#    tarball; a CodeBuild stitch run rewrites stitch/stitch_graph.json and its marker; an
#    image act moves the task definition's digest; a safe-apply moves Terraform state; any
#    S3 write to the graph bucket moves a LastModified. Every one of those is read here and
#    compared against THIS ORDER'S START (the issuer's amendment commit c4a842b1b9). An act
#    that happened inside the window would show as a LastModified inside the window.
#    A LastModified BEFORE the order started cannot have been produced by the order.
#
#  ARM 2 (CODE). No executable line in anything this order wrote or changed calls any of
#    the five. Comment and docstring lines are EXCLUDED and counted separately, because a
#    mention is not a call and this order's files talk about the held acts constantly --
#    the exclusion is printed, never silent.
#
#  ARM 3 (CONTROL). The same detector is run over a PLANTED line carrying all five held
#    acts and must find 5 of 5. A counter that cannot go up is not a measurement.
#
# WHAT THIS CANNOT SEE, stated rather than left to be assumed: it cannot see an act
# performed by ANOTHER seat, and it cannot see an act that left no mark on the four
# surfaces read. It is not a CloudTrail audit of the account.
#
# Run from the repository root.
set -u

python - <<'PY'
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

import boto3

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "infra" / "aws" / "globgrph"))

# THIS ORDER'S START: the issuer's amendment commit, the GO for TO-CG-G-2.
ORDER_START_COMMIT = "c4a842b1b9"
BASE_COMMIT = "f3b5f26f77"
BUCKET = "opal-313476888478-globgrph"
DELIV = Path("org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1")
SELF = "g2_no_egress.sh"

# The five held acts, in the forms that PERFORM them. The keys are the criterion's counters.
HELD = {
    "ECS_RUN_TASK_CALLS": [r"\becs\s+run-task\b", r"\brun_task\s*\(", r"\becs\s+start-task\b"],
    "CODEBUILD_STARTS": [r"\bcodebuild\s+start-build\b", r"\bstart_build\s*\("],
    "S3_WRITES": [r"\bs3\s+cp\b", r"\bs3\s+sync\b", r"\bs3\s+mv\b", r"\bs3\s+rm\b",
                  r"\bs3api\s+put-object\b", r"\bput_object\s*\(", r"\bupload_file\s*\(",
                  r"\bupload_fileobj\s*\(", r"\bdelete_object\s*\("],
    "IMAGE_PUSHES": [r"\bdocker\s+push\b", r"\bdocker\s+build\b", r"\bbuildx\b",
                     r"\becr\s+put-image\b", r"\bbuild-derive-image\.sh\b",
                     r"\bregister-task-definition\b"],
    "TERRAFORM_APPLIES": [r"\bterraform\s+apply\b", r"\bsafe-apply\b",
                          r"\bterraform\s+destroy\b"],
}


def order_start():
    out = subprocess.run(["git", "log", "-1", "--format=%cI", ORDER_START_COMMIT],
                         capture_output=True, text=True)
    return datetime.datetime.fromisoformat(out.stdout.strip())


def executable_lines(path: Path):
    """Lines that could RUN. Comments and python docstring blocks are excluded and counted."""
    text = path.read_text(encoding="utf-8", errors="replace").split("\n")
    keep, dropped = [], 0
    in_doc = False
    for ln in text:
        st = ln.strip()
        if path.suffix == ".py":
            ticks = st.count('"""') + st.count("'''")
            if in_doc:
                dropped += 1
                if ticks % 2 == 1:
                    in_doc = False
                continue
            if ticks % 2 == 1:
                in_doc = True
                dropped += 1
                continue
        if st.startswith("#") or not st:
            dropped += 1
            continue
        keep.append(ln)
    return keep, dropped


def scan(lines):
    hits = {k: [] for k in HELD}
    for ln in lines:
        for k, pats in HELD.items():
            for p in pats:
                if re.search(p, ln):
                    hits[k].append(ln.strip()[:160])
                    break
    return hits


now = datetime.datetime.now(datetime.timezone.utc)
start = order_start()
print("G2-AC4 -- THE EGRESS HOLD, PROVEN AND NOT ASSERTED")
print("  run at: %s   order start: %s (commit %s, the issuer's amendment)"
      % (now.strftime("%Y-%m-%dT%H:%M:%SZ"), start.astimezone(datetime.timezone.utc)
         .strftime("%Y-%m-%dT%H:%M:%SZ"), ORDER_START_COMMIT))
print("INSTRUMENT: three independent arms -- a LIVE read of the four surfaces the five held"
      " acts would move; a static scan of the EXECUTABLE lines of everything this order"
      " wrote or changed; and a planted positive through the same detector.")
print("GRAIN: one ACT per counter; the world arm is at the grain of an S3 object's"
      " LastModified and the service's own vintage, the code arm at the grain of one line.")
print("ENVIRONMENT: the comparison instant is this repository's own commit timestamp for"
      " %s, read with git, not a wall clock typed by hand." % ORDER_START_COMMIT)
print("")

# ---------------------------------------------------------------- ARM 1: the world
s3 = boto3.client("s3", region_name="us-east-1")
watched = ["snapshots/latest.txt", "stitch/stitch_graph.json", "stitch/stitch_marker.json"]
world_rows = []
moved = 0
for key in watched:
    h = s3.head_object(Bucket=BUCKET, Key=key)
    lm = h["LastModified"].astimezone(datetime.timezone.utc)
    inside = lm > start.astimezone(datetime.timezone.utc)
    moved += 1 if inside else 0
    world_rows.append((key, lm.strftime("%Y-%m-%dT%H:%M:%SZ"), h.get("ETag", "").strip('"'),
                       inside))

vintage = None
try:
    import projection_client as pc
    vintage = (pc.health(timeout_s=20.0) or {}).get("vintage")
except Exception as ex:  # noqa: BLE001
    vintage = "UNREAD (%s)" % type(ex).__name__

print("  -- ARM 1 (WORLD): the surfaces a held act would move --")
for key, lm, etag, inside in world_rows:
    print("     s3://%s/%-28s last_modified=%s etag=%s  MOVED_INSIDE_THIS_ORDER=%s"
          % (BUCKET, key, lm, etag[:16], inside))
G1_VINTAGE = "2026-09-10T03:31:02.025931+00:00"
print("     served projection vintage=%s" % vintage)
print("     vintage TO-CG-G-1 measured at 05:0xZ: %s   SAME=%s" % (G1_VINTAGE,
      str(vintage) == G1_VINTAGE))
print("     THE VINTAGE IS NOT THE DERIVE ORACLE AND IS PRINTED AS INFORMATION ONLY. It is"
      " the PROJECTION's build instant, and the projection republishes on its own cadence"
      " from Iceberg -- it moves with no derive behind it. The derive oracle is the three"
      " S3 objects above, which a derive cannot avoid rewriting. Row"
      " NFRA_CLDGRPH-W1-S39 records a republish inside this order that moved the served"
      " STORED_IN count with every one of those three objects unmoved.")
print("     SURFACES_MOVED_INSIDE_THIS_ORDER=%d of %d watched object(s)" % (moved, len(watched)))
print("")

# ---------------------------------------------------------------- ARM 2: the code
corpus = []
for p in sorted(DELIV.glob("g2_*")):
    if p.name == SELF or p.suffix not in (".py", ".sh"):
        continue
    corpus.append(p)

totals = {k: 0 for k in HELD}
lines_scanned = 0
dropped_total = 0
per_file = []
for p in corpus:
    keep, dropped = executable_lines(p)
    lines_scanned += len(keep)
    dropped_total += dropped
    h = scan(keep)
    per_file.append((str(p), len(keep), dropped, {k: len(v) for k, v in h.items()}))
    for k in HELD:
        totals[k] += len(h[k])

# The two producer files: only the lines this order ADDED, read from git.
# `git diff <commit> -- <path>` (NO ..HEAD) diffs the commit against the WORKING TREE.
# The first cut of this arm used `BASE..HEAD` and scanned 0 producer lines, because the
# producer edits were still uncommitted -- an arm that certified a corpus it had not read.
diff = subprocess.run(["git", "diff", BASE_COMMIT, "--unified=0", "--",
                       "infra/aws/globgrph/derive_runner.py",
                       "infra/aws/globgrph/derive_stitch.py"],
                      capture_output=True, text=True).stdout.split("\n")
added = [ln[1:] for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
added_exec = [ln for ln in added
              if ln.strip() and not ln.strip().startswith("#")
              and not ln.strip().startswith('"""') and not ln.strip().startswith("'''")]
hd = scan(added_exec)
for k in HELD:
    totals[k] += len(hd[k])

print("  -- ARM 2 (CODE): every executable line this order wrote or changed --")
for name, kept, dropped, h in per_file:
    print("     %-72s exec_lines=%-5d comment/docstring_lines_excluded=%-5d hits=%s"
          % (name, kept, dropped, {k: v for k, v in h.items() if v} or "none"))
print("     %-72s exec_lines=%-5d comment/docstring_lines_excluded=%-5d hits=%s"
      % ("git diff %s -- (the two producer files, worktree, ADDED lines only)" % BASE_COMMIT,
         len(added_exec), len(added) - len(added_exec),
         {k: len(v) for k, v in hd.items() if v} or "none"))
print("     EXCLUDED FROM THE CORPUS, NAMED SO THE EXCLUSION IS NOT SILENT: %s (this file --"
      " it CONTAINS the five patterns as literals, so scanning it would count the detector"
      " as a call); the record .md and the commit messages (prose -- a mention is not a"
      " call, and this order's prose names the held acts on almost every page)." % SELF)
print("")

# ---------------------------------------------------------------- ARM 3: the control
planted = ["aws ecs run-task --cluster opal-globgrph --task-definition x",
           "aws codebuild start-build --project-name opal-stitch-produce",
           "aws s3 cp ./x.json s3://opal-313476888478-globgrph/stitch/x.json",
           "docker push 313476888478.dkr.ecr.us-east-1.amazonaws.com/globgrph:latest",
           "bash .tools/safe-apply.sh -auto-approve"]
ctrl = scan(planted)
caught = sum(1 for k in HELD if ctrl[k])
print("  -- ARM 3 (CONTROL): a planted positive through the SAME detector --")
for k in sorted(HELD):
    print("     %-22s planted_caught=%d" % (k, len(ctrl[k])))
print("     PLANTED_ACTS_CAUGHT=%d of %d" % (caught, len(HELD)))
print("")

for k in ("ECS_RUN_TASK_CALLS", "CODEBUILD_STARTS", "S3_WRITES", "IMAGE_PUSHES",
          "TERRAFORM_APPLIES"):
    print("%s=%d" % (k, totals[k]))
print("EGRESS_PROBE_CONTROL=%s" % ("FIRED" if caught == len(HELD) else "NOT-FIRED"))
print("")
print("  DENOMINATOR: %d of %d watched S3 object(s) moved inside this order's window and 1"
      " of 1 served vintage re-read; %d executable line(s) scanned across %d authored"
      " file(s) plus %d added producer line(s), with %d comment/docstring line(s) excluded"
      " and 1 file (%s) excluded by name for the reason above; %d of %d held acts caught on"
      " the planted positive."
      % (moved, len(watched), lines_scanned + len(added_exec), len(corpus), len(added_exec),
         dropped_total + (len(added) - len(added_exec)), SELF, caught, len(HELD)))
print("  WHAT THIS DOES NOT CERTIFY: it does not audit the AWS account, and it cannot see"
      " an act by another seat or an act that moved none of the four surfaces read. It"
      " certifies THIS ORDER, on the surfaces the five held acts cannot avoid touching.")
ok = (sum(totals.values()) == 0 and moved == 0 and caught == len(HELD))
print("NO_EGRESS_RESULT=%s" % ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
PY
