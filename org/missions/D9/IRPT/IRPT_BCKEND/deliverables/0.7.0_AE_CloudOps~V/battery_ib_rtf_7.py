#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-7 battery -- STEP 4 ATTEMPTED BY EVERY CREDENTIAL THE SEAT HOLDS.

Authority: Andrew-direct 2026-09-19 ~06:3xZ (record
org/tier1_exec/2.0.0_SA_COO~B/deliverables/ANDREW_DIRECT_20260919_063xZ_STEP4_BUCKET_POLICY_AE_ATTEMPT_THEN_PROCEED.md).
The act: remove the bucket ACCESS POLICY (never the bucket) on exactly two buckets.

Command set, fixed by the issuer's nudge (2.0.0_SA_COO~B, this session) and nothing wider:
  1. aws sts get-caller-identity --query Arn --output text      -> the identity ARN
  2. aws s3api delete-bucket-policy --bucket <b>, per bucket     -> the response verbatim
  3. ONLY on a delete success: aws s3api get-bucket-policy --bucket <b> on both buckets
     -> NoSuchBucketPolicy is the discriminator (the face, arm (b)).
No profile enumeration and no credential-file read: the identity set is the ambient default
credential chain, N = 1. No credential VALUE is printed; ARNs only.

Every run RE-ATTEMPTS every delete (a denial is re-measured, never remembered), so a run is a
change attempt against a live fence: run it only under an OPEN change-management ledger entry.

Prints IBR64-STEP4-BUCKET-POLICY-REMOVED-2-OF-2 only when 2 of 2 buckets read NoSuchBucketPolicy
after the attempt; otherwise a FAIL line and the carry line verbatim.
"""
from __future__ import annotations

import datetime
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# .../deliverables/0.7.0_AE_CloudOps~V -> up 7 to the worktree root
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
AWS = os.path.join(WS, ".tools", "aws.cmd")
BUCKETS = ("opal-data-inflection", "opal-data-cottonwood")
OUTPUT_PATH = os.path.join(HERE, "IB-rtf-7_R64-AC1_battery_output.txt")
TOKEN = "IBR64-STEP4-BUCKET-POLICY-REMOVED-2-OF-2"
CALL_TIMEOUT_S = 120

LINES: list[str] = []


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_aws(args: list[str]) -> dict:
    """One aws call; rc, stdout, stderr returned verbatim. A timeout is recorded as rc 124."""
    for a in args:
        if a.startswith("opal-data-") and a not in BUCKETS:
            sys.exit("STOP: bucket %s is outside the two this order names" % a)
    started = now()
    try:
        out = subprocess.run([AWS] + args, capture_output=True, text=True, timeout=CALL_TIMEOUT_S)
        rc, so, se = out.returncode, out.stdout, out.stderr
    except subprocess.TimeoutExpired:
        rc, so, se = 124, "", "TIMEOUT after %ss" % CALL_TIMEOUT_S
    return {"cmd": "aws " + " ".join(args), "at": started, "rc": rc,
            "stdout": so.strip(), "stderr": se.strip()}


def show(res: dict) -> None:
    emit("  $ %s" % res["cmd"])
    emit("    at: %s  rc: %s" % (res["at"], res["rc"]))
    emit("    stdout: %s" % (res["stdout"] if res["stdout"] else "<empty>"))
    emit("    stderr: %s" % (res["stderr"] if res["stderr"] else "<empty>"))


def git_head() -> str:
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=WS, capture_output=True, text=True,
                         timeout=30)
    return out.stdout.strip() or "UNREAD"


def main() -> int:
    emit("IB-rtf-7 R64-AC1 battery -- run at %s -- worktree HEAD %s" % (now(), git_head()))
    emit("")
    emit("(a) IDENTITIES -- the ambient default credential chain (no profile enumeration, "
         "no credential-file read, per the issuer's command set)")
    ident = run_aws(["sts", "get-caller-identity", "--query", "Arn", "--output", "text"])
    show(ident)
    identities = [ident["stdout"]] if ident["rc"] == 0 and ident["stdout"].startswith("arn:") else []
    n = len(identities)
    emit("  identities enumerated: N = %d%s" % (n, (" -> " + identities[0]) if n else
                                              " (identity read FAILED; attempts still made)"))
    emit("")
    emit("(b) ATTEMPTS -- delete-bucket-policy per identity per bucket")
    attempts = []
    for b in BUCKETS:
        res = run_aws(["s3api", "delete-bucket-policy", "--bucket", b])
        show(res)
        res["bucket"] = b
        res["denied"] = "AccessDenied" in res["stderr"]
        res["succeeded"] = res["rc"] == 0
        attempts.append(res)
    n_id = max(n, 1)
    n_attempts = len(attempts)
    n_success = sum(1 for a in attempts if a["succeeded"])
    n_denied = sum(1 for a in attempts if a["denied"])
    n_other = n_attempts - n_success - n_denied
    emit("  attempts: %d of %d (2N, N = %d); succeeded %d of %d; AccessDenied %d of %d; "
         "other failure %d of %d" % (n_attempts, 2 * n_id, n_id, n_success, n_attempts,
                                      n_denied, n_attempts, n_other, n_attempts))
    emit("")
    emit("(c) DISCRIMINATOR -- get-bucket-policy -> NoSuchBucketPolicy, run only on a delete success")
    removed = 0
    if n_success:
        for b in BUCKETS:
            res = run_aws(["s3api", "get-bucket-policy", "--bucket", b])
            show(res)
            if "NoSuchBucketPolicy" in res["stderr"]:
                removed += 1
        emit("  NoSuchBucketPolicy: %d of %d buckets" % (removed, len(BUCKETS)))
    else:
        emit("  SKIP: 0 of %d deletes succeeded -- no read-back taken; NoSuchBucketPolicy 0 of %d"
             % (n_attempts, len(BUCKETS)))
    emit("")
    if removed == len(BUCKETS):
        emit("RESULT: step 4 DONE -- bucket access policy removed on %d of %d buckets"
             % (removed, len(BUCKETS)))
        emit(TOKEN)
        rc = 0
    else:
        emit("RESULT: R64-AC1 FAIL -- NoSuchBucketPolicy %d of %d; %d of %d attempts denied"
             % (removed, len(BUCKETS), n_denied, n_attempts))
        emit("CARRY: step 4 -- Andrew at the console when next present; %d identities tried, "
             "%d of %d denied" % (n_id, n_denied, 2 * n_id))
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
