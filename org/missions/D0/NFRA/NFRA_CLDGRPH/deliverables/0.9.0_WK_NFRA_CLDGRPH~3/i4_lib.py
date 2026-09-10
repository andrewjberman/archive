#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-I-4 -- shared instrument for cell CG-s-44.

WHAT THIS FILE IS FOR: every I-4 script reads S3 and none of them writes to it, and
that has to be provable from the artifacts rather than asserted in prose. So every AWS
call this order makes goes through aws_read(), which

  1. REFUSES any verb not in READ_VERBS -- the refusal is at the call site, before the
     subprocess exists, so a write verb cannot be issued even by mistake; and
  2. APPENDS one ledger line BEFORE the subprocess runs, so the ledger counts ATTEMPTS,
     not successes. A ledger written after the fact cannot record a call that hung.

THE LEDGER IS COMMITTED (it lives beside this file, not in .scratch) because it is the
evidence for I4-AC4's S3_READS count, and evidence that a fresh clone cannot see is not
evidence. It cites every object in the grammar this order is arguing for --
bucket/key@ETag -- so the record this cell leaves behind is itself in the new grammar.

TREE RESOLUTION is done here once, by git, from the CALLER's cwd: a linked worktree has a
--git-dir under .git/worktrees/<name> while --git-common-dir points at the main .git. That
is what distinguishes MAIN from WORKTREE, and it is measured, never assumed.

NON-ASCII is refused throughout: OK: / WARN: / ERROR: / SKIP: / BLOCKED:.
"""

import datetime
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "i4_s3_reads.ledger")

BUCKET = "opal-313476888478-globgrph"
PREFIX = "snapshots/"

# Every verb this order is allowed to issue. There is no write verb in this tuple, and
# aws_read() raises on anything outside it -- the enumeration IS the control.
READ_VERBS = (
    ("s3api", "head-object"),
    ("s3api", "list-objects-v2"),
    ("s3api", "list-object-versions"),
    ("s3api", "get-bucket-versioning"),
)


def repo_root():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                         cwd=os.getcwd(), capture_output=True, text=True, timeout=20)
    return out.stdout.strip() if out.returncode == 0 else os.getcwd()


def tree_facts(root):
    """MAIN vs WORKTREE, measured. Returns a dict; every value came from git."""
    def g(*args):
        r = subprocess.run(["git", "-C", root] + list(args),
                           capture_output=True, text=True, timeout=20)
        return r.stdout.strip() if r.returncode == 0 else ""
    gd = g("rev-parse", "--absolute-git-dir")
    cd = g("rev-parse", "--git-common-dir")
    if cd and not os.path.isabs(cd):
        cd = os.path.abspath(os.path.join(root, cd))
    kind = "WORKTREE" if (gd and cd and os.path.normpath(gd) != os.path.normpath(cd)) else "MAIN"
    return {
        "root": root.replace(os.sep, "/"),
        "kind": kind,
        "git_dir": gd.replace(os.sep, "/"),
        "git_common_dir": (cd or "").replace(os.sep, "/"),
        "branch": g("rev-parse", "--abbrev-ref", "HEAD"),
        "head": g("rev-parse", "HEAD"),
    }


def _ledger(line):
    with open(LEDGER, "a", encoding="ascii", newline="\n") as fh:
        fh.write(line + "\n")


def aws_read(root, service, verb, args, note, timeout=60):
    """The ONLY door to AWS in this order. Read verbs only; ledger first, call second."""
    if (service, verb) not in READ_VERBS:
        raise RuntimeError("BLOCKED: %s %s is not a read verb permitted to TO-CG-I-4" % (service, verb))
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    _ledger("READ %s %s-%s s3://%s -- %s" % (stamp, service, verb, BUCKET, note))
    # WHY aws.cmd AND NOT aws: .tools/aws is a bash shim, and CreateProcess on Windows
    # refuses it with WinError 193 ("not a valid Win32 application") from a python parent.
    # Both faces of the shim ship together (CLAUDE.md: "both or neither"); the .cmd face is
    # the one a non-shell parent can exec, and it forwards to the same CLI v1.
    exe = os.path.join(root, ".tools", "aws.cmd")
    if not os.path.exists(exe):
        raise RuntimeError("BLOCKED: %s absent -- the aws shim's .cmd face is missing" % exe)
    cmd = [exe, service, verb] + args + ["--output", "json"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    # CLI v1 through this shim emits CRLF; strip CR before anything parses it.
    out = r.stdout.replace("\r\n", "\n")
    return r.returncode, out, r.stderr.replace("\r\n", "\n")


def live_objects(root):
    """One list call over snapshots/. Coverage is the WHOLE prefix, not the cited subset:
    a live table built only from the keys the record happens to cite could not tell a
    reader that a cited key is MISSING from the bucket, and that is one of the outcomes."""
    rc, out, err = aws_read(root, "s3api", "list-objects-v2",
                            ["--bucket", BUCKET, "--prefix", PREFIX],
                            "the whole snapshots/ prefix -- live table for the classifier")
    if rc != 0:
        raise RuntimeError("ERROR: list-objects-v2 rc=%d %s" % (rc, err.strip()[:200]))
    d = json.loads(out)
    objs = {}
    for o in d.get("Contents", []):
        objs[o["Key"]] = {
            "etag": o["ETag"].strip('"').lower(),
            "last_modified": o["LastModified"],
            "size": int(o["Size"]),
        }
    return objs, {
        "key_count": d.get("KeyCount"),
        "is_truncated": d.get("IsTruncated"),
        "next_token_present": bool(d.get("NextContinuationToken")),
        "returned": len(objs),
    }


def head(root, key, note):
    rc, out, err = aws_read(root, "s3api", "head-object",
                            ["--bucket", BUCKET, "--key", key], note)
    if rc != 0:
        return None
    d = json.loads(out)
    return {
        "etag": d["ETag"].strip('"').lower(),
        "last_modified": d["LastModified"],
        "size": int(d["ContentLength"]),
    }
