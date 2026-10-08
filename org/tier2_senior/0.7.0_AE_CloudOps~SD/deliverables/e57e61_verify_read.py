#!/usr/bin/env python
"""e57e61 L3 verify reader -- grade the producer run against CTO half acceptance 2.

READ-ONLY. Makes no AWS write and no repo write. It answers exactly one question, by the
rule the issuer fixed in TO-DEPLOY-e57e61 amendment 2 (@db8652adbc, msg 851):

    US row      = an item with a NON-EMPTY `name`  (producer's own rule,
                  infra/aws/lambda/v2_portal/_shared/rivalfunds_classification.py:25-26 --
                  "A BLOOMBERG item carries NO `name` ... A US row keeps `name`.")
    US written  = name present AND state == "written"
    US planned  = name present AND state != "present"
    ROLLBACK    <=> US planned > 0 AND US written == 0

WHY A SCRIPT: acceptance 2 names a count that NEITHER artifact reports as a field -- the log's
`counts` dict has no US split and the output items carry no listing_country / input /
sub_asset_class / per-row written flag. The count is derived, so deriving it the same way twice
matters more than deriving it quickly. `source` is deliberately NOT used: amendment 2 says
"source stays out of it", and on 2026-10-07 it is a different axis from name-presence
(canonical_shape=32 / opal_silver=18 against name absent=19 / present=31).

Usage:  python e57e61_verify_read.py [YYYY-MM-DD]      (default: today, UTC)

Prints the log counts dict, the state-by-name cross-tab, both US counts and the verdict --
the four things msg 851 asks the report to carry. Exit code is NOT the oracle: read VERDICT.
"""

from __future__ import annotations

import datetime
import json
import shutil
import subprocess
import sys

BUCKET = "opal-data-etfs"
PREFIX = "mdpf/etfs/gold/new_securities"
LOG_GROUP = "/aws/lambda/mdpf-secclass-new-security-lambda"


def _resolve_aws() -> str:
    """Resolve the AWS CLI for a NATIVE-PYTHON caller.

    `.tools/aws` is an EXTENSIONLESS BASH script: Windows CreateProcess cannot execute it, so
    subprocess raises FileNotFoundError (WinError 2). That is precisely the asymmetry row
    MDPF_SECCLASS-D1-S2 records -- the bash half of the shim pair works while native callers
    need `.tools/aws.cmd`, reached on PATH through ~/bin/aws.cmd. This function was written
    AFTER hitting that trap in this very script.

    Invoking the .cmd directly (no shell) also sidesteps MSYS argv mangling, which matters
    here because LOG_GROUP begins with `/` and a bash-mediated call would rewrite it into a
    Windows path.
    """
    for cand in ("aws.cmd", "aws"):
        found = shutil.which(cand)
        if found:
            return found
    sys.stderr.write("FATAL: no AWS CLI resolved via shutil.which('aws.cmd'/'aws').\n")
    sys.exit(3)


AWS = _resolve_aws()


def sh(args: list) -> str:
    """Run the AWS CLI and return stdout. Never 2>/dev/null -- an empty read here would
    otherwise be indistinguishable from a clean absence, and a failed retrieval returns a
    VALUE (CLAUDE.md rule 22a, RETRIEVAL)."""
    p = subprocess.run([AWS] + args, capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write("AWS CALL FAILED (rc=%d): aws %s\n%s\n" % (p.returncode, " ".join(args), p.stderr.strip()))
        return ""
    return p.stdout


def read_output_object(day: str):
    key = "%s/date=%s/new_securities.json" % (PREFIX, day)
    raw = sh(["s3", "cp", "s3://%s/%s" % (BUCKET, key), "-"])
    if not raw.strip():
        return key, None
    return key, json.loads(raw)


def read_log_line(day: str) -> str:
    """The producer prints one INFO line carrying its counts dict. Find the newest stream
    whose name holds the day, then return the counts line."""
    streams = sh(["logs", "describe-log-streams", "--log-group-name", LOG_GROUP,
                  "--order-by", "LastEventTime", "--descending", "--max-items", "8",
                  "--output", "json"])
    if not streams.strip():
        return ""
    for st in json.loads(streams).get("logStreams", []):
        name = st.get("logStreamName", "")
        if day.replace("-", "/") not in name:
            continue
        ev = sh(["logs", "get-log-events", "--log-group-name", LOG_GROUP,
                 "--log-stream-name", name, "--limit", "60", "--output", "json"])
        if not ev.strip():
            continue
        for e in json.loads(ev).get("events", []):
            if "new-security-classifier" in e.get("message", "") and "counts=" in e.get("message", ""):
                return e["message"].rstrip("\n")
    return ""


def main() -> int:
    day = sys.argv[1] if len(sys.argv) > 1 else datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    print("E57E61-VERIFY run_date=%s  (rule: TO-DEPLOY-e57e61 amendment 2 @db8652adbc)" % day)

    log_line = read_log_line(day)
    print("  LOG LINE: %s" % (log_line if log_line else "NOT FOUND -- the run may not have fired yet"))

    key, doc = read_output_object(day)
    if doc is None:
        print("  OUTPUT:   ABSENT at s3://%s/%s" % (BUCKET, key))
        print("  VERDICT:  CANNOT-GRADE -- no output object. This is NOT a pass and NOT a rollback.")
        return 2

    items = doc.get("items") or []
    print("  OUTPUT:   s3://%s/%s  items=%d  counts=%s" % (BUCKET, key, len(items), json.dumps(doc.get("counts", {}), sort_keys=True)))

    # state-by-name cross-tab, the denominator msg 851 asks for
    tab = {}
    for it in items:
        is_us = bool((it.get("name") or "").strip())
        cell = (it.get("state") or "<none>", "name-present(US)" if is_us else "name-absent(BBG)")
        tab[cell] = tab.get(cell, 0) + 1
    print("  CROSS-TAB (state x name-presence), denominator %d:" % len(items))
    for (state, kind) in sorted(tab):
        print("    %-10s | %-18s -> %d" % (state, kind, tab[(state, kind)]))

    us_written = sum(1 for it in items
                     if (it.get("name") or "").strip() and it.get("state") == "written")
    us_planned = sum(1 for it in items
                     if (it.get("name") or "").strip() and it.get("state") != "present")

    print("  US WRITTEN (name present AND state==written):     %d" % us_written)
    print("  US PLANNED (name present AND state!=present):     %d" % us_planned)

    if us_planned > 0 and us_written == 0:
        print("  VERDICT:  ROLLBACK -- US planned > 0 and US written == 0. Same-day rollback per the entry.")
        return 1
    if us_planned == 0:
        print("  VERDICT:  PASS (no US row needed writing: US planned == 0, so acceptance 2 does not arm)")
        return 0
    print("  VERDICT:  PASS -- US planned %d > 0 and US written %d > 0" % (us_planned, us_written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
