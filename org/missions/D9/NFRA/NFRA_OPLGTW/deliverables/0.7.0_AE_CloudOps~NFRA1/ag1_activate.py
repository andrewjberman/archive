#!/usr/bin/env python
"""OG-ap-35 Phase B: ONE `activate` under opal-gateway-access-admin through the admin module's own CLI.

usage: python ag1_activate.py narrow|restore   (from the repo root)

narrow  = X/alyssa_narrow_candidate.json (operations minus download_filtered).
restore = X/alyssa_restore_candidate.json (the before scope), used only on a failed read-back.
The CLI prints prepare()'s diff, which can carry values, so the whole output goes to X (off-repo); only the lines that begin
ACTIVATED or REFUSED are printed here. No retry: a REFUSED, a stale base or a nonzero exit is reported as is."""
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
SOURCE_AUTH = ("CTO ruling CTO_RULING_OPLGTW_BD68_ALYSSA_DOWNLOADS_ENFORCE_HIS_WORD_20261017_Z (commit aed4469fa6); never-widen ask OG-ap-35 "
               "sha256 224a80d88a52, halves CTO df73e21192 COO 4aea561614 CVO 03311f4476; Phase B GO msg 35330")
SUMMARY = {
    "narrow": ("OG-ap-35: remove download_filtered from one restricted client principal's Schwab data grant (describe, list, query unchanged). "
               "approver field = data owner per the writer's schema; this act enforces his 2026-10-08 word under CTO ruling aed4469fa6; "
               "he did not approve this act in person."),
    "restore": ("OG-ap-35 ROLLBACK: restore the before scope (download_filtered back) after a failed read-back. "
                "approver field = data owner per the writer's schema; this act restores the state before OG-ap-35; he did not approve this act in person."),
}
CAND = {"narrow": "alyssa_narrow_candidate.json", "restore": "alyssa_restore_candidate.json"}


def x_dir() -> str:
    d = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "opal", "og-salt", "ag1")
    if os.path.realpath(d).startswith(os.path.realpath(".")):
        raise SystemExit("REFUSED: X resolves inside the worktree")
    return d


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in CAND:
        raise SystemExit("usage: ag1_activate.py narrow|restore")
    mode = sys.argv[1]
    X = x_dir()
    cand = os.path.join(X, CAND[mode])
    if not os.path.isfile(cand):
        raise SystemExit("STOP: %s not found" % cand)
    r = subprocess.run([SHIM, "sts", "assume-role", "--role-arn", ROLE, "--role-session-name", "ag1-phaseb-%s" % mode,
                        "--duration-seconds", "900", "--output", "json"], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("STOP: assume-role failed: " + r.stderr.decode("utf-8", "replace")[:300])
    c = json.loads(r.stdout.decode("utf-8"))["Credentials"]
    env = dict(os.environ, AWS_ACCESS_KEY_ID=c["AccessKeyId"], AWS_SECRET_ACCESS_KEY=c["SecretAccessKey"],
               AWS_SESSION_TOKEN=c["SessionToken"], AWS_DEFAULT_REGION="us-east-1", AWS_REGION="us-east-1")
    env.pop("AWS_PROFILE", None)
    p = subprocess.run([sys.executable, CLI, "activate", "--candidate", cand, "--approver", APPROVER,
                        "--source-authorization", SOURCE_AUTH, "--summary", SUMMARY[mode]],
                       capture_output=True, env=env)
    out = p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")
    with io.open(os.path.join(X, "ag1_%s_activate_out.txt" % mode), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    keep = [ln for ln in out.splitlines() if ln.startswith(("ACTIVATED", "REFUSED"))]
    print("%s: exit=%d output_lines=%d (full output off-repo in X)" % (mode, p.returncode, len(out.splitlines())))
    for ln in keep:
        print(ln)
    if not keep:
        print("NO ACTIVATED/REFUSED line; last non-diff line: " + (out.strip().splitlines()[-1][:160] if out.strip() else "(empty)"))
    return p.returncode


if __name__ == "__main__":
    sys.exit(main())
