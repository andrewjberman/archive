#!/usr/bin/env python
"""OG-ap-15 A1: compare each converter's DEPLOYED package bytes to its package dir at base_sha.

This answers two separate asks with one measurement:

  * E1 (the COO's condition on etf, carried by the CTO half): before the apply, the DEPLOYED etf
    package's members must equal the repo package copy the drift was measured against.
  * `deployed_equals_base` (the A1 drain-only route for blackdiamond, orion and eclipse): the
    deployed package must equal the package dir at base_sha before the two drain hunks are applied
    on top of it. Any other delta is a STOP.

Why bytes and not a filename or a hash the producer reports: CLAUDE.md rule 22a's CODE layer --
deployed bytes are diffed against the BUILD INPUT, never trusted from a name, a source map or a
self-reported sha. `CodeSha256` covers the whole zip and cannot say WHICH member moved, which is
exactly what a drain-only build has to know.

Reports three disjoint sets per family, each with its denominator:
  EQUAL        -- member present both sides, bytes identical
  DIFFERING    -- member present both sides, bytes differ  (a STOP for the drain-only route)
  ONLY_ONE_SIDE-- present in the zip but not the package dir at base_sha, or vice versa

A package-dir file that is not packaged (BUILD_MANIFEST.json, notes) is EXPECTED on the
package-dir-only side, so that side is reported rather than treated as a defect; the zip-only side
is never expected and is a STOP.

Usage: python ap15_deployed_vs_base.py <base_sha> <family>...
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

# Native Windows python cannot exec the extensionless bash shim (FileNotFoundError, WinError 2);
# .tools/aws.cmd is its Windows face and CLAUDE.md requires both or neither to exist.
SHIM = os.path.join(".tools", "aws.cmd" if sys.platform == "win32" else "aws")


def run(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise SystemExit("FAILED %s: %s" % (" ".join(cmd[:3]), r.stderr.decode("utf-8", "replace")[:400]))
    return r.stdout.decode("utf-8", "replace").strip()


def git_bytes(ref_path: str) -> bytes | None:
    r = subprocess.run(["git", "show", ref_path], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def package_dir_members(base: str, pkg: str) -> dict:
    out = {}
    listing = subprocess.run(["git", "ls-tree", "--name-only", base, pkg + "/"], capture_output=True)
    for line in listing.stdout.decode("utf-8", "replace").split("\n"):
        line = line.strip().replace("\r", "")
        if not line:
            continue
        b = git_bytes("%s:%s" % (base, line))
        if b is not None:
            out[os.path.basename(line)] = b
    return out


def main() -> int:
    base = sys.argv[1]
    fams = sys.argv[2:]
    report = {"base_sha": base, "method": "deployed zip members vs package dir blobs at base_sha, byte compare", "families": []}
    for fam in fams:
        fn = "opal-assets-silver-%s" % fam
        pkg = "infra/aws/lambda/opal-assets/%s" % fn
        url = run([SHIM, "lambda", "get-function", "--function-name", fn, "--query", "Code.Location", "--output", "text"])
        sha_live = run([SHIM, "lambda", "get-function-configuration", "--function-name", fn, "--query", "CodeSha256", "--output", "text"])
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as fh:
            tmp = fh.name
        urllib.request.urlretrieve(url, tmp)
        raw = io.open(tmp, "rb").read()
        import base64
        zip_sha = base64.b64encode(hashlib.sha256(raw).digest()).decode("ascii")
        base_members = package_dir_members(base, pkg)
        equal, differing, zip_only = [], [], []
        with zipfile.ZipFile(tmp) as z:
            zip_names = [n for n in z.namelist() if not n.endswith("/")]
            for n in zip_names:
                b = z.read(n)
                key = os.path.basename(n)
                if key not in base_members:
                    zip_only.append(n)
                elif base_members[key] == b:
                    equal.append(key)
                else:
                    differing.append(key)
        dir_only = sorted(set(base_members) - {os.path.basename(n) for n in zip_names})
        os.unlink(tmp)
        ok = not differing and not zip_only
        report["families"].append({
            "family": fam, "function": fn,
            "live_code_sha256": sha_live, "downloaded_zip_sha256": zip_sha,
            "sha_matches_configuration": zip_sha == sha_live,
            "zip_members": len(zip_names), "package_dir_members_at_base": len(base_members),
            "equal": len(equal), "differing": differing, "zip_only": zip_only,
            "package_dir_only_not_packaged": dir_only,
            "deployed_equals_base": ok,
        })
        print("%-13s zip members %-3s vs package dir %-3s | EQUAL %-3s DIFFERING %-2s ZIP_ONLY %-2s | deployed_equals_base %s"
              % (fam, len(zip_names), len(base_members), len(equal), len(differing), len(zip_only), ok))
        if differing:
            print("    DIFFERING: " + ", ".join(differing))
        if zip_only:
            print("    ZIP_ONLY (a STOP): " + ", ".join(zip_only))
        if dir_only:
            print("    package-dir-only, not packaged (expected): " + ", ".join(dir_only))
        print("    zip sha256 %s matches get-function-configuration: %s" % (zip_sha, zip_sha == sha_live))
    with io.open("ap15_deployed_vs_base.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(report, fh, indent=1)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
