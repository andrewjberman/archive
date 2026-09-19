#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-12 second pass -- verify the ONE build of the 6 serving functions AT REST (read-only).

Per function, against the built sha256 build-and-upload.sh printed (argv: fn=sha pairs):
  - the build-store latest version is NEW; its content-sha256 metadata == the re-downloaded bytes == the built sha;
  - the ROLLBACK SOURCE (the version the build displaced) is still present and hashes to the prior live CodeSha256;
  - the function's CodeSha256 is UNCHANGED (the build deployed nothing);
  - members == the manifest's files[] @HEAD; every staged member == its blob at its pin (declared sha256); every own
    member == the bytes on disk the builder read, and every own .py member == its HEAD blob;
  - the DELTA vs the LIVE zip == exactly the added member(s) (raw_keys.json, + firm_registry.json on the S99 four) PLUS
    the seam member's line endings where the live zip carries the CRLF hand copy (S101, accepted); every other member
    byte-identical to live, m of m; the own members that sit CRLF on this checkout byte-identical to live.
Prints no URL and no credential. Writes IB-rtf-12_build_verify_output.txt beside itself.
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
import urllib.request
import zipfile

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
OUTPUT_PATH = os.path.join(HERE, "IB-rtf-12_build_verify_output.txt")
BUCKET = "opal-313476888478-lambda-artifacts"
SEAM = "data/custodian_key_seam.json"
RAW_REPO = "infra/aws/lambda/investor-reporting/_ids/raw_keys.json"
REG_REPO = "data/firm_registry.json"
# The prior LIVE state, read at the ledger's open (@0414444120): (CodeSha256, the build-store version that held it).
PRIOR = {
    "irpt-directory-search": ("HOpXPDoHhrVK/ayqsx1uKgzt9mWOjDlK+Ix2CPbCamI=", "hk9OUfwHZxlcwZDqN7cEknbJOXtvB3jd"),
    "irpt-status": ("LHprxKSP1lM3VhoP2ijEcUVCtI+yeZt8tPRkZwpRBdY=", "QNerDSUu9GMYB0bZrjon6n_6VG9q3aR6"),
    "irpt-holdings": ("78XvypHOpeybejwKd5KLCwNcgat2jbQr6O3PhdwaFSU=", "XGnVW2ED9FW0zOpRr0V5K12adFHrpeO7"),
    "irpt-narrative": ("sgolF/uXedgXpePoBoi5y1dIgOybQkgcokihEJFM+0I=", "Pu2QRmDx58Qo3hHwVM8L_gyotsmQ8h_6"),
    "irpt-export-render": ("4Dp6e0Vy+SfziPY+9wUSWSBS4JzS9diUtduOTxIqclQ=", "5tV41pNz.TpJ8O1f6zZCAJ9M6BRqoYlI"),
    "irpt-performance-adapter": ("/Cn8XUZoSn1EGBax3+/UaVjJSAQiybZQ84vRVwiRcWs=", "KI0U8m08xPkCgvem5bLmcU2fuWwOCLzs"),
}
LINES: list[str] = []


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def b64sha(b: bytes) -> str:
    return base64.b64encode(hashlib.sha256(b).digest()).decode()


def git_blob(ref: str, path: str) -> bytes | None:
    p = subprocess.run(["git", "show", "%s:%s" % (ref, path)], cwd=WS, capture_output=True)
    return p.stdout if p.returncode == 0 else None


def main() -> int:
    built = dict(a.split("=", 1) for a in sys.argv[1:])
    s3 = boto3.client("s3", region_name="us-east-1")
    lam = boto3.client("lambda", region_name="us-east-1")
    head_commit = subprocess.run(["git", "rev-parse", "--short=10", "HEAD"], cwd=WS, capture_output=True, text=True).stdout.strip()
    emit("IB-rtf-12 build verification -- run at %s as %s -- worktree HEAD %s" % (
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        boto3.client("sts").get_caller_identity()["Arn"], head_commit))
    sm = json.loads(git_blob("HEAD", "infra/aws/lambda/ci/lambda-source-map.json").decode("utf-8"))["functions"]
    ok_fns = 0
    crlf_same = crlf_total = 0
    for fn, (prior_live, prior_ver) in PRIOR.items():
        e = sm[fn]
        want = built[fn]
        key = "investor-reporting/%s.zip" % fn
        h = s3.head_object(Bucket=BUCKET, Key=key)
        latest, meta = h["VersionId"], (h.get("Metadata") or {}).get("content-sha256")
        body = s3.get_object(Bucket=BUCKET, Key=key, VersionId=latest)["Body"].read()
        prior_bytes = s3.get_object(Bucket=BUCKET, Key=key, VersionId=prior_ver)["Body"].read()
        live_now = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
        live_zip = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(lam.get_function(FunctionName=fn)["Code"]["Location"], timeout=120).read()))
        live_m = {n: live_zip.read(n) for n in live_zip.namelist() if not n.endswith("/")}
        z = zipfile.ZipFile(io.BytesIO(body))
        new_m = {n: z.read(n) for n in z.namelist() if not n.endswith("/")}
        staged = {s["packaged_as"]: s for s in e.get("staged_from", [])}
        added_expected = {s["packaged_as"] for s in e.get("staged_from", []) if s["repo_path"] in (RAW_REPO, REG_REPO)}
        checks = {
            "new version latest": latest != prior_ver,
            "metadata == bytes == built": meta == want and b64sha(body) == want,
            "rollback source == prior live": b64sha(prior_bytes) == prior_live,
            "function unchanged": live_now == prior_live,
            "members == files[]": sorted(new_m) == sorted(e["files"]),
        }
        src_ok = 0
        for m, b in new_m.items():
            if m in staged:
                good = b == git_blob(staged[m]["pin"], staged[m]["repo_path"]) and hashlib.sha256(b).hexdigest() == staged[m]["sha256"]
            else:
                disk = open(os.path.join(WS, e["source_dir"], m), "rb").read()
                good = b == disk and (not m.endswith(".py") or b == git_blob("HEAD", e["source_dir"] + "/" + m))
            src_ok += good
        checks["each member == its source (staged: pin blob; own: disk, .py also HEAD blob)"] = src_ok == len(new_m)
        added = sorted(set(new_m) - set(live_m))
        removed = sorted(set(live_m) - set(new_m))
        changed = sorted(m for m in new_m if m in live_m and new_m[m] != live_m[m])
        seam_ok = all(m == SEAM and live_m[m].count(b"\r") > 0 and new_m[m].count(b"\r") == 0
                      and live_m[m].replace(b"\r\n", b"\n") == new_m[m] for m in changed)
        same = sum(1 for m in new_m if m in live_m and new_m[m] == live_m[m])
        checks["delta == the added member(s) + the seam line endings where applicable"] = (
            set(added) == added_expected and not removed and seam_ok and same == len(live_m) - len(changed))
        own_crlf = [m for m in new_m if m not in staged and new_m[m].count(b"\r") > 0]
        crlf_total += len(own_crlf)
        crlf_same += sum(1 for m in own_crlf if live_m.get(m) == new_m[m])
        good_fn = all(checks.values())
        ok_fns += good_fn
        emit("")
        emit("%s: built %s -> version %s (%d bytes); rollback source %s (== prior live %s)" % (fn, want, latest, len(body), prior_ver, prior_live))
        emit("  members %d (files[] %d); each == its source %d of %d; delta vs live: added %s, removed %s, changed %s; other members byte-identical to live %d of %d"
             % (len(new_m), len(e["files"]), src_ok, len(new_m), added, removed or "none", changed or "none", same, len(live_m) - len(changed)))
        for m in changed:
            emit("    %s: live %d bytes CR %d -> built %d bytes CR %d; the same bytes once CRLF is normalised: %s"
                 % (m, len(live_m[m]), live_m[m].count(b"\r"), len(new_m[m]), new_m[m].count(b"\r"),
                    live_m[m].replace(b"\r\n", b"\n") == new_m[m]))
        for m in added:
            emit("    ADDED %-20s %d bytes sha256 %s (== the pin blob: %s)" % (m, len(new_m[m]), hashlib.sha256(new_m[m]).hexdigest()[:16],
                                                                       m in staged and new_m[m] == git_blob(staged[m]["pin"], staged[m]["repo_path"])))
        emit("  own members CRLF on this checkout: %d, byte-identical to live %d" % (len(own_crlf), sum(1 for m in own_crlf if live_m.get(m) == new_m[m])))
        for k, v in checks.items():
            emit("  CHECK %s: %s" % (k, "OK" if v else "FAIL"))
    emit("")
    emit("own CRLF members byte-identical to live: %d of %d" % (crlf_same, crlf_total))
    emit("RESULT: %d of %d functions verified at rest" % (ok_fns, len(PRIOR)))
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return 0 if ok_fns == len(PRIOR) and crlf_same == crlf_total else 1


if __name__ == "__main__":
    sys.exit(main())
