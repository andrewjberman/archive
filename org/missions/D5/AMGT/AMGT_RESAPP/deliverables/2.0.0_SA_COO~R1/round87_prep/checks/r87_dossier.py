"""AMGT_RESAPP round-87 PREP -- the DEPLOYED scoped-API package carries AMGT_CORPUS dossier.py at a named METHOD (CTO~DELL1
round-86 analysis R1 + AMGT_CORPUS leg p: /9, never /8).

  python r87_dossier.py --want amgt-corpus-dossier/9 [--never amgt-corpus-dossier/8]

Downloads the live function's code package (get-function Code.Location, read only), reads `lib/research/corpus/dossier.py` INSIDE it
and prints its METHOD_VERSION, the function CodeSha256 and LastModified.
    P1 the deployed package's dossier.py METHOD_VERSION equals --want;
    P2 it is not --never.
Verdict: R87 DOSSIER: YES|NO (exit 0|1). At the base (live HZoC2x): NO -- the package reads amgt-corpus-dossier/7.
"""
from __future__ import annotations

import argparse
import io
import re
import sys
import urllib.request
import zipfile

FN = "opal-amgt-scoped-api"
MEMBER = "lib/research/corpus/dossier.py"
METHOD_RE = re.compile(r'^METHOD_VERSION\s*=\s*"([^"]+)"', re.M)


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--want", required=True)
    ap.add_argument("--never", default="amgt-corpus-dossier/8")
    a = ap.parse_args()
    import boto3

    lam = boto3.client("lambda", region_name="us-east-1")
    f = lam.get_function(FunctionName=FN)
    cfg = f["Configuration"]
    print("   function %s CodeSha256 %s LastModified %s" % (FN, cfg["CodeSha256"], cfg["LastModified"]))
    blob = urllib.request.urlopen(f["Code"]["Location"], timeout=120).read()
    z = zipfile.ZipFile(io.BytesIO(blob))
    names = [n for n in z.namelist() if n.replace("\\", "/").endswith(MEMBER)]
    if not names:
        say(False, "P1 %s present in the deployed package: 0 of %d members match" % (MEMBER, len(z.namelist())))
        print("R87 DOSSIER: NO")
        return 1
    m = METHOD_RE.search(z.read(names[0]).decode("utf-8", "replace"))
    got = m.group(1) if m else None
    print("   deployed %s METHOD_VERSION %s (member %s)" % (MEMBER, got, names[0]))
    p1 = say(got == a.want, "P1 deployed METHOD_VERSION is %s: read %s" % (a.want, got))
    p2 = say(got != a.never, "P2 deployed METHOD_VERSION is not %s" % a.never)
    ok = p1 and p2
    print("R87 DOSSIER: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
