#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-H-4 / CG-s-39 -- shared READ-ONLY plumbing.

READ ONLY BY CONSTRUCTION. Every AWS verb this module can issue is enumerated in
READ_VERBS below and asserted before the subprocess runs; a write verb raises.
Nothing here publishes, runs a task, starts a build, applies Terraform or puts an
S3 object. The one thing an investigator of a republish must not do is republish.

TREE CONTROL (the comp-rail worktree clause on this order's face): every census
this order claims prints TREE_READ -- the absolute worktree root plus a file that
exists ONLY on this branch -- so a well-formed number cannot come from a tree the
reader did not mean to read.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
# THE SHIM, AND WHY THE CHOICE IS EXPLICIT: `.tools/aws` is a POSIX shell script and
# a native Windows python cannot exec it (WinError 193). `.tools/aws.cmd` is the
# same shim's cmd face -- CLAUDE.md ships them "both or neither". Resolved here so
# every caller gets the SAME instrument.
AWS = os.path.join(ROOT, ".tools", "aws.cmd" if sys.platform == "win32" else "aws")
BUCKET = "opal-313476888478-globgrph"
LEDGER = os.path.join(ROOT, ".scratch", "h4_read_ledger.txt")

# The complete set of AWS verbs this order may issue. Read-only, by the task
# order's EGRESS HOLD ("PERMITTED AND CENTRAL TO THIS ORDER: every AWS READ").
READ_VERBS = {
    ("s3api", "list-objects-v2"), ("s3api", "get-object"), ("s3api", "head-object"),
    ("s3api", "get-bucket-versioning"),
    ("logs", "describe-log-groups"), ("logs", "filter-log-events"),
    ("codebuild", "list-projects"), ("codebuild", "list-builds-for-project"),
    ("codebuild", "batch-get-builds"),
    ("ecs", "list-clusters"), ("ecs", "list-services"), ("ecs", "describe-services"),
    ("ecs", "list-tasks"), ("ecs", "describe-tasks"),
    ("cloudtrail", "lookup-events"), ("cloudtrail", "describe-trails"),
    ("sts", "get-caller-identity"),
}


def _record_read(service, verb):
    try:
        os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
        with open(LEDGER, "a", encoding="ascii") as fh:
            fh.write("%s %s\n" % (service, verb))
    except OSError:
        pass


def aws_json(service, verb, *args, timeout=60):
    """Run ONE read-only aws call and return parsed JSON (or None). Never a write."""
    if (service, verb) not in READ_VERBS:
        raise RuntimeError("REFUSED: %s %s is not in this order's READ_VERBS" % (service, verb))
    argv = [AWS, service, verb] + list(args) + ["--output", "json"]
    _record_read(service, verb)
    p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    out = (p.stdout or "").replace("\r", "").strip()
    if p.returncode != 0:
        return {"__rc": p.returncode, "__err": (p.stderr or "").replace("\r", "").strip()[:400]}
    if not out:
        return {}
    try:
        return json.loads(out)
    except ValueError:
        return {"__rc": 0, "__raw": out[:400]}


def aws_get_object(key, dest, timeout=60):
    """Download ONE object. A GET is a read; the destination is scratch, never S3."""
    _record_read("s3api", "get-object")
    argv = [AWS, "s3api", "get-object", "--bucket", BUCKET, "--key", key, dest]
    p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    return p.returncode


def list_all(prefix, delimiter=None, timeout=90):
    """Auto-paginate list-objects-v2 CLIENT-SIDE. A page is not an answer."""
    keys, prefixes, token = [], [], None
    while True:
        args = ["--bucket", BUCKET, "--prefix", prefix, "--max-items", "1000"]
        if delimiter:
            args += ["--delimiter", delimiter]
        if token:
            args += ["--starting-token", token]
        d = aws_json("s3api", "list-objects-v2", *args, timeout=timeout)
        if not isinstance(d, dict) or "__rc" in d:
            break
        for c in d.get("Contents", []) or []:
            keys.append((c["Key"], c.get("LastModified", ""), c.get("Size", 0)))
        for c in d.get("CommonPrefixes", []) or []:
            prefixes.append(c["Prefix"])
        token = d.get("NextToken")
        if not token:
            break
    return keys, prefixes


def logs_all(group, start_ms, end_ms, pattern=None, timeout=90):
    """Auto-paginate filter-log-events CLIENT-SIDE. Returns [] on a missing group."""
    events, token = [], None
    while True:
        args = ["--log-group-name", group, "--start-time", str(start_ms),
                "--end-time", str(end_ms)]
        if pattern:
            args += ["--filter-pattern", pattern]
        if token:
            args += ["--next-token", token]
        d = aws_json("logs", "filter-log-events", *args, timeout=timeout)
        if not isinstance(d, dict) or "__rc" in d:
            break
        events += d.get("events", []) or []
        token = d.get("nextToken")
        if not token:
            break
    return events


def tree_read(tag):
    """TREE_READ + the one-file positive control. Costs one file; proves the tree."""
    ctl = os.path.join(HERE, "h4_lib.py")
    branch = subprocess.run(["git", "-C", ROOT, "rev-parse", "--abbrev-ref", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    head = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    print("TREE_READ      : %s" % ROOT)
    print("  branch       : %s   HEAD: %s" % (branch, head))
    print("  positive ctl : %s -> %s" % (os.path.relpath(ctl, ROOT).replace("\\", "/"),
                                         "PRESENT" if os.path.isfile(ctl) else "ABSENT"))
    print("  tag          : %s" % tag)
    if not os.path.isfile(ctl):
        print("BLOCKED: tree control absent -- this census is not about this tree")
        sys.exit(2)


def ms(iso_utc):
    """'2026-09-10T03:31:02Z'-ish -> epoch millis. UTC only, no local clock."""
    import datetime
    s = iso_utc.replace("Z", "+00:00")
    return int(datetime.datetime.fromisoformat(s).timestamp() * 1000)


def hhmmss(millis):
    import datetime
    return datetime.datetime.fromtimestamp(
        millis / 1000.0, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def logs_probe(group, start_ms, end_ms, limit=50, timeout=60):
    """ONE bounded page -- a LIVENESS probe, never a census. Used only to tell a
    silent instrument (0 events of any kind) from an instrument that saw the
    window. It prints its own bound wherever it is quoted."""
    d = aws_json("logs", "filter-log-events", "--log-group-name", group,
                 "--start-time", str(start_ms), "--end-time", str(end_ms),
                 "--limit", str(limit), timeout=timeout)
    if not isinstance(d, dict) or "__rc" in d:
        return None
    return d.get("events", []) or []
