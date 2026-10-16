#!/usr/bin/env python
"""OG-mg-1 Phase B step 6: ONE `activate` of ONE record, under opal-gateway-access-admin, through the admin module's own CLI.

usage: python mg1_activate.py r1|r2   (from the repo root)

Assumes the operator role (a fresh STS session named for the record), hands those credentials to the CLI process only, and runs
`schwab_entitlement_admin.py activate --candidate X/<rec>_candidate.json`. The CLI prints prepare()'s diff, which can carry values, so the
whole output goes to X (off-repo); only the lines that begin ACTIVATED or REFUSED are printed here and are what W/MG1_WRITE.md records.
No retry: a REFUSED, a stale base or a nonzero exit is reported as is and writes nothing further."""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys

ROLE = "arn:aws:iam::313476888478:role/opal-gateway-access-admin"
SHIM = os.path.join(".tools", "aws.cmd" if sys.platform == "win32" else "aws")
CLI = os.path.join("infra", "aws", "ec2", "opal-gateway", "ops", "schwab_entitlement_admin.py")
APPROVER = "Andrew Berman"
SOURCE_AUTH = ("CTO ruling msg 32383 (v2.2-width profile, 13 months, Bloomberg mirrors in r30); decomposition R3-T.31; PRD v2.3 item 1 "
               "(Andrew-direct 2026-10-09); CTO ruling msg 33850; never-widen ask OG-mg-1 sha256 757f5146afee, halves COO 020264306c "
               "CTO c92d6c7c07 CVO 5c4025b899; Phase B GO msg 34954")
SUMMARY = {"r1": "OG-mg-1 R1: Andrew's principal, restricted profile with the contract-maximal Schwab data-grant scope, 13 calendar months",
           "r2": "OG-mg-1 R2: the Bloomberg concierge principal, the exact mirror of R1 (PRD v2.3 item 1)"}


def x_dir() -> str:
    d = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "opal", "og-salt", "mg1")
    if os.path.realpath(d).startswith(os.path.realpath(".")):
        raise SystemExit("REFUSED: X resolves inside the worktree")
    return d


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in ("r1", "r2"):
        raise SystemExit("usage: mg1_activate.py r1|r2")
    rec = sys.argv[1]
    X = x_dir()
    cand = os.path.join(X, "%s_candidate.json" % rec)
    if not os.path.isfile(cand):
        raise SystemExit("STOP: %s not found" % cand)
    r = subprocess.run([SHIM, "sts", "assume-role", "--role-arn", ROLE, "--role-session-name", "mg1-phaseb-%s" % rec,
                        "--duration-seconds", "900", "--output", "json"], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("STOP: assume-role failed: " + r.stderr.decode("utf-8", "replace")[:300])
    c = json.loads(r.stdout.decode("utf-8"))["Credentials"]
    env = dict(os.environ, AWS_ACCESS_KEY_ID=c["AccessKeyId"], AWS_SECRET_ACCESS_KEY=c["SecretAccessKey"],
               AWS_SESSION_TOKEN=c["SessionToken"], AWS_DEFAULT_REGION="us-east-1", AWS_REGION="us-east-1")
    env.pop("AWS_PROFILE", None)
    p = subprocess.run([sys.executable, CLI, "activate", "--candidate", cand, "--approver", APPROVER,
                        "--source-authorization", SOURCE_AUTH, "--summary", SUMMARY[rec]],
                       capture_output=True, env=env)
    out = p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")
    with io.open(os.path.join(X, "%s_activate_out.txt" % rec), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    keep = [ln for ln in out.splitlines() if ln.startswith(("ACTIVATED", "REFUSED"))]
    print("%s: exit=%d output_lines=%d (full output off-repo in X)" % (rec, p.returncode, len(out.splitlines())))
    for ln in keep:
        print(ln)
    if not keep:
        print("NO ACTIVATED/REFUSED line; last non-diff line: " + (out.strip().splitlines()[-1][:160] if out.strip() else "(empty)"))
    return p.returncode


if __name__ == "__main__":
    sys.exit(main())
