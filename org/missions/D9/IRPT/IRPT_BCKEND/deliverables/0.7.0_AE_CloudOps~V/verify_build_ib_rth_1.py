#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rth-1 arm (c) -- verify the K-CODE build in the build store, per function, before any plan.

Packet NEVER_WIDEN_SIGNOFF_PACKET_IB-rth-1.md blob 19389dc50b6e3bfb7436681328cb2721c9c11802; halves COO @6298e74db4,
CTO @5fce993215. Ledger irpt-bckend-ib-rth-1-build.

Per function that stages _authz/loaders.py (7, from lambda-source-map.json):
  - build-store LATEST version: content-sha256 metadata; the object re-downloaded and re-hashed (b64) == metadata;
  - member-by-member diff of that zip against the PRIOR LIVE zip (snapshotted from get-function Code.Location
    before the build, .scratch/rth1_prior/<fn>.zip, sha256 == the packet s4 pre-change CodeSha256): the member SET
    is identical and EXACTLY ONE member differs -- loaders.py -- and its bytes sha256 == the signed fix
    0c086052e6e6...; any other difference is outside what the halves sign;
  - the prior build-store version (the rollback source) still exists and its content-sha256 == the pre-change value;
  - the function's live CodeSha256 is unchanged (nothing applied by the build).
A function whose latest build-store version is still the prior version is reported NOT-BUILT, never passed.
Prints no credential. Writes IB-rth-1_build_verify_output.txt beside itself.
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import io
import json
import os
import subprocess
import sys
import zipfile

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
OUTPUT_PATH = os.path.join(HERE, "IB-rth-1_build_verify_output.txt")
PRIOR_DIR = os.path.join(WS, ".scratch", "rth1_prior")
BUCKET = "opal-313476888478-lambda-artifacts"
FIX_SHA256 = "0c086052e6e65d2cb411f15362862b1656bad0b2320f9756be6a32444b665765"
PRE = {  # function -> (packet s4 pre-change CodeSha256, prior build-store version read at ledger open)
    "irpt-directory-search": ("76LeVyYNfhdyDnQNXR3LzrqSv7k7Vr3POSjpcBzww6E=", "GcjdIsAVfsJXvzGwuySEofStO3gVoEG8"),
    "irpt-status": ("B0AmyfRKxd4uMhcfoklf3cCpPtnDQUBpLsUBADeDcQ0=", "2ER4lGvdlY7ftm5mPgEYt6pnXbozOeIG"),
    "irpt-holdings": ("rAAn3bt7MZXpxFgric7LlrNW9uv0xXgpiZmb+MOf/y0=", "UUJ.iaufP39ypd8gq2NeSYyQewqgNizF"),
    "irpt-narrative": ("o4newc7E9m1pD61k+P/xGdlwHMO7cheYbDfR6Urzgh8=", "jM9scOJ005ovgidfDS3DBRHRmjvLzUwn"),
    "irpt-export-render": ("cn8YKEP2oQdfvAjdpa32Wfp9oJqhAIMGkECv+H4vUg4=", "bEdwSqXfY99WaJSKeLwPkLuBPySCmI39"),
    "irpt-performance-adapter": ("W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=", "M0E32HJhwg54I6jcU4g2e58Ktthey_51"),
    "irpt-ycharts-generate": ("1L60sG1G9IaFfwe+LPNdE84DarlWCHKkdE8M5CyVI8o=", "D6hl_ey9azxF8RJRQ01YkDlO.axHKuHw"),
}

LINES: list[str] = []
s3 = boto3.client("s3", region_name="us-east-1")
lam = boto3.client("lambda", region_name="us-east-1")


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def b64sha(b: bytes) -> str:
    return base64.b64encode(hashlib.sha256(b).digest()).decode()


def members(zbytes: bytes) -> dict[str, str]:
    with zipfile.ZipFile(io.BytesIO(zbytes)) as zf:
        return {n: hashlib.sha256(zf.read(n)).hexdigest() for n in zf.namelist() if not n.endswith("/")}


def staged_functions() -> list[str]:
    with open(os.path.join(WS, "infra", "aws", "lambda", "ci", "lambda-source-map.json"), encoding="utf-8") as fh:
        fns = json.load(fh)["functions"]
    return sorted(n for n, s in fns.items() if any(str(f).endswith("loaders.py") for f in (s.get("files") or [])))


def main() -> int:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=WS, capture_output=True, text=True).stdout.strip()
    emit("IB-rth-1 arm (c) build verify -- run at %s -- HEAD %s" % (
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), head))
    fns = staged_functions()
    emit("functions staging loaders.py (lambda-source-map.json): %d: %s" % (len(fns), fns))
    emit("denominator: %d; packet s4 table rows: %d; set equal: %s" % (len(fns), len(PRE), set(fns) == set(PRE)))
    emit("")
    built_ok = []
    not_built = []
    failed = []
    for fn in fns:
        pre_sha, pre_ver = PRE[fn]
        key = "investor-reporting/%s.zip" % fn
        h = s3.head_object(Bucket=BUCKET, Key=key)
        ver, meta = h.get("VersionId"), h.get("Metadata", {}).get("content-sha256")
        live = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
        emit("%s" % fn)
        emit("  build-store latest: version %s, content-sha256 %s, LastModified %s" % (
            ver, meta, h["LastModified"].isoformat()))
        emit("  live CodeSha256: %s (pre-change %s) -> %s" % (live, pre_sha, "UNCHANGED" if live == pre_sha else "MOVED"))
        if ver == pre_ver:
            emit("  latest version == the prior version -> NOT BUILT (nothing uploaded)")
            not_built.append(fn)
            emit("")
            continue
        body = s3.get_object(Bucket=BUCKET, Key=key, VersionId=ver)["Body"].read()
        rb = b64sha(body)
        emit("  re-download sha256(b64) %s -> %s metadata" % (rb, "==" if rb == meta else "!="))
        prior_path = os.path.join(PRIOR_DIR, fn + ".zip")
        prior = open(prior_path, "rb").read()
        emit("  prior live snapshot %s sha256(b64) %s -> %s pre-change" % (
            os.path.relpath(prior_path, WS), b64sha(prior), "==" if b64sha(prior) == pre_sha else "!="))
        new_m, old_m = members(body), members(prior)
        same_set = set(new_m) == set(old_m)
        diff = sorted(n for n in new_m if n in old_m and new_m[n] != old_m[n])
        emit("  members: new %d, prior %d, same set %s; differing: %s" % (len(new_m), len(old_m), same_set, diff))
        lsha = new_m.get("loaders.py")
        emit("  loaders.py sha256 %s -> %s the signed fix" % (lsha, "==" if lsha == FIX_SHA256 else "!="))
        ph = s3.head_object(Bucket=BUCKET, Key=key, VersionId=pre_ver)
        prior_meta = ph.get("Metadata", {}).get("content-sha256")
        emit("  rollback source version %s still present, content-sha256 %s -> %s pre-change" % (
            pre_ver, prior_meta, "==" if prior_meta == pre_sha else "!="))
        ok = (rb == meta and b64sha(prior) == pre_sha and same_set and diff == ["loaders.py"]
              and lsha == FIX_SHA256 and prior_meta == pre_sha and live == pre_sha)
        emit("  -> %s" % ("BUILT-OK (exactly loaders.py moved, to the fix)" if ok else "FAIL"))
        (built_ok if ok else failed).append((fn, meta, ver))
        emit("")
    emit("BUILT-OK: %d of %d: %s" % (len(built_ok), len(fns), [(f, s, v) for f, s, v in built_ok]))
    emit("NOT BUILT: %d of %d: %s" % (len(not_built), len(fns), not_built))
    emit("FAIL: %d of %d: %s" % (len(failed), len(fns), [f for f, _, _ in failed]))
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
