"""AMGT_CORPUS round 35, CRPS-ak-3 (round-34 analysis ruling 3, row Z-S84) -- the scheduled entry's dry run reads rc 0 with its
plan printed and 0 writes. The issuer's file.

It runs `lib.research.corpus.induction_scheduled --mode dry-run` in-process, with every AWS write operation (PutObject,
CopyObject, DeleteObject, DeleteObjects, CompleteMultipartUpload) counted and REFUSED at botocore's single call point.
  b1 the admit and refresh step lines both read rc 0, and the closing line reads rc 0
  b2 the plan is printed: an `admit population registered <N> without_block <K>` line and a refresh last line ending
     `pulled 0 bloomberg_calls 0`
  c1 0 AWS write operations were attempted
  -> one 'ARM <id> PASS|FAIL <got>' line per arm, then 'ak3 build <p>/2 control <q>/1'
"""
import contextlib
import io
import os
import re
import runpy
import subprocess
import sys

import botocore.client

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
if TOP not in sys.path:
    sys.path.insert(0, TOP)
os.chdir(TOP)

WRITES = {"PutObject", "CopyObject", "DeleteObject", "DeleteObjects", "CompleteMultipartUpload"}
attempted = []
_orig = botocore.client.BaseClient._make_api_call


def _spy(self, operation_name, api_params):
    if operation_name in WRITES:
        attempted.append(operation_name)
        raise RuntimeError("AK3: AWS write %s refused in a dry run" % operation_name)
    return _orig(self, operation_name, api_params)


botocore.client.BaseClient._make_api_call = _spy
sys.argv = ["induction_scheduled", "--mode", "dry-run"]
buf = io.StringIO()
rc = None
with contextlib.redirect_stdout(buf):
    try:
        runpy.run_module("lib.research.corpus.induction_scheduled", run_name="__main__")
    except SystemExit as exc:
        rc = exc.code
out = buf.getvalue().splitlines()

results = []


def arm(aid, ok, got):
    results.append((aid, bool(ok)))
    print("ARM %s %s %s" % (aid, "PASS" if ok else "FAIL", got))


admit = next((ln for ln in out if re.match(r"^induction_scheduled step model_block_admit rc \d+$", ln)), "")
refresh = next((ln for ln in out if re.match(r"^induction_scheduled step model_block_refresh rc \d+$", ln)), "")
closing = next((ln for ln in reversed(out) if ln.startswith("induction_scheduled mode dry-run ")), "")
arm("b1", admit.endswith(" rc 0") and refresh.endswith(" rc 0") and " rc 0 " in closing,
    "admit=[%s] refresh=[%s] closing_rc=[%s]" % (admit, refresh, (re.search(r" rc (\d+) ", closing) or [None, "none"])[1]))

plan_admit = next((ln for ln in out if re.match(r"^admit population registered \d+ without_block \d+", ln)), "")
plan_refresh = [ln for ln in out if ln.startswith("refresh population registered ")]
arm("b2", bool(plan_admit) and bool(plan_refresh) and plan_refresh[-1].endswith("pulled 0 bloomberg_calls 0"),
    "admit_plan=[%s] refresh_last=[%s]" % (plan_admit[:70], plan_refresh[-1] if plan_refresh else "none"))

arm("c1", not attempted, "aws_writes_attempted %d %s" % (len(attempted), attempted[:4]))

b = sum(1 for aid, ok in results if aid.startswith("b") and ok)
c = sum(1 for aid, ok in results if aid.startswith("c") and ok)
print("ak3 build %d/2 control %d/1" % (b, c))
