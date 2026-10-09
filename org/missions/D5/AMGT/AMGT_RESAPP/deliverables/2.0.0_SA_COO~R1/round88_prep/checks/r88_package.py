"""AMGT_RESAPP round-88 PREP -- the DEPLOYED scoped-API package carries a named module byte-equal to a git ref.

  python r88_package.py --member lib/research/api/scoped_amgt.py [--ref HEAD]

Downloads the live function's code package (get-function Code.Location, read only), reads --member INSIDE it, and compares its bytes
with `git show <ref>:<member>` in the current checkout (run it in the build worktree at the pin, where HEAD is the pin).
    K1 the member is present in the deployed package;
    K2 the deployed member is byte-equal to <ref>'s (both sha256 printed).
Verdict: R88 PACKAGE: YES|NO (exit 0|1). It discriminates a redeploy only once <ref> differs from the live package's source.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import subprocess
import sys
import urllib.request
import zipfile

FN = "opal-amgt-scoped-api"


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--member", required=True)
    ap.add_argument("--ref", default="HEAD")
    a = ap.parse_args()
    want = subprocess.run(["git", "show", "%s:%s" % (a.ref, a.member)], capture_output=True)
    if want.returncode != 0 or not want.stdout:
        print("ERROR: git show %s:%s read nothing (rc %s)" % (a.ref, a.member, want.returncode))
        return 2
    import boto3

    f = boto3.client("lambda", region_name="us-east-1").get_function(FunctionName=FN)
    cfg = f["Configuration"]
    print("   function %s CodeSha256 %s LastModified %s" % (FN, cfg["CodeSha256"], cfg["LastModified"]))
    z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(f["Code"]["Location"], timeout=120).read()))
    names = [n for n in z.namelist() if n.replace("\\", "/").endswith(a.member)]
    k1 = say(bool(names), "K1 %s present in the deployed package (%d members)" % (a.member, len(z.namelist())))
    got = z.read(names[0]) if names else b""
    print("   deployed sha256 %s (%d bytes) | %s sha256 %s (%d bytes)" % (
        hashlib.sha256(got).hexdigest()[:16], len(got), a.ref, hashlib.sha256(want.stdout).hexdigest()[:16], len(want.stdout)))
    k2 = say(got == want.stdout, "K2 the deployed member is byte-equal to %s's" % a.ref)
    ok = k1 and k2
    print("R88 PACKAGE: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
