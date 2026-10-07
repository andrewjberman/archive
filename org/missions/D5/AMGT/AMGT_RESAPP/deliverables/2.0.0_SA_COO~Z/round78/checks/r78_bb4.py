"""AMGT_RESAPP round 78 -- AMGT-bb-4: the slash-safe officers reader (row AMGT_RESAPP-Z-S365).

  --crit AC1|AC2|AC3 --where local

The cell repairs `lib.research.management.bloomberg_fallback.StoredBloombergInput.newest_key` so it lists the SAME
folder the writer writes (`lib.research.harvest.store.entity_partition`), and leaves `security_key()` returning what
it returns today.

AC1 (build, the seam against the real store; reads only):
    C1 newest_key("BP/ LN Equity") and newest_key("NG/ LN Equity") each return the newest object in that name's folder;
    C2 the control: newest_key("AMD US Equity") still returns the newest object in its folder;
    C3 the denominator: for every stored officer folder, the reader finds that folder's newest object (N of N printed);
    C4 the officer chain serves a Bloomberg officer list for BP/_LN_Equity and for NG/_LN_Equity, and still for
       AMD_US_Equity, and neither slash name says a new Bloomberg request is needed.
AC2 (build): the plant tests in lib/research/management/tests/test_stored_officers_slash_key.py pass.
AC3 (bound, must hold before and after): `security_key()` returns the same text as before for a plain and a slash
    name (the writer hands that text to the store, which makes it slash-safe once; a second encoding is refused), and
    the three existing test files that exercise this reader pass.
Verdict: R78 BB4 <CRIT> SERVED: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

BUCKET = "opal-data-harvest"
PREFIX = "bloomberg/harvest/bronze/exec_officers/"
TEST = "lib/research/management/tests/test_stored_officers_slash_key.py"
EXISTING = (
    "lib/research/management/tests/test_fwd7_stored_fallback.py",
    "lib/research/management/tests/test_bloomberg_fallback.py",
    "lib/research/api/tests/test_exec_roster_chain.py",
)


def _pytest(paths):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + list(paths), capture_output=True,
                       timeout=100)
    tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1]
    print("   " + tail)
    return p.returncode == 0 and " passed" in tail and "failed" not in tail, "rc=%d" % p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.crit == "AC2":
        if not os.path.isfile(TEST):
            clause("C1 the plant test file exists", False, TEST)
            return verdict(a, ok)
        passed, detail = _pytest([TEST])
        clause("C1 every plant case passes", passed, detail)
        return verdict(a, ok)

    from lib.research.management import bloomberg_fallback as bf

    if a.crit == "AC3":
        plain, slash = bf.security_key("AMD US Equity"), bf.security_key("BP/ LN Equity")
        clause("C1 security_key() returns what it returned before", plain == "AMD_US_Equity" and slash == "BP/_LN_Equity",
               "%r %r" % (plain, slash))
        passed, detail = _pytest(EXISTING)
        clause("C2 the existing tests of this reader pass", passed, detail)
        return verdict(a, ok)

    import boto3

    from lib.research.identity import crosswalk
    from lib.research.management import exec_roster_chain

    s3 = boto3.client("s3", region_name="us-east-1")
    newest = {}
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
        for obj in page.get("Contents", []) or []:
            parts = obj["Key"][len(PREFIX):].split("/")
            if len(parts) == 2 and parts[0].startswith("security_key=") and parts[1].endswith(".json"):
                folder = parts[0][len("security_key="):]
                newest[folder] = max(newest.get(folder, ""), obj["Key"])
    reader = bf.StoredBloombergInput(s3=s3)

    def read(security):
        try:
            return reader.newest_key(security)
        except Exception as err:  # noqa: BLE001 -- a raise is a counted miss, named
            return "raised %s" % type(err).__name__

    got = {s: read(s) for s in ("BP/ LN Equity", "NG/ LN Equity", "AMD US Equity")}
    for security, key in got.items():
        print("   newest_key(%r) = %s" % (security, key))
    clause("C1 the two slash names read their newest stored object",
           got["BP/ LN Equity"] is not None and got["BP/ LN Equity"] == newest.get("BP-SLASH-_LN_Equity")
           and got["NG/ LN Equity"] is not None and got["NG/ LN Equity"] == newest.get("NG-SLASH-_LN_Equity"))
    clause("C2 the control name still reads its newest stored object",
           got["AMD US Equity"] is not None and got["AMD US Equity"] == newest.get("AMD_US_Equity"))
    missed = []
    for folder, key in sorted(newest.items()):
        security = crosswalk.security_key_from_slash_safe(folder).replace("_", " ")
        if read(security) != key:
            missed.append(security)
    print("   stored officer folders %d; read %d; not read %s" % (len(newest), len(newest) - len(missed), missed[:4]))
    clause("C3 every stored officer folder is read", bool(newest) and not missed,
           "%d of %d" % (len(newest) - len(missed), len(newest)))
    chain_ok = []
    for key in ("BP/_LN_Equity", "NG/_LN_Equity", "AMD_US_Equity"):
        result = exec_roster_chain.run_chain(key, s3)
        legs = {e.get("leg"): e for e in result.get("chain_tried") or []}
        bloomberg = legs.get("bloomberg") or {}
        served = result.get("served") or {}
        count = len((served.get("document") or {}).get("officers") or [])
        print("   chain %s: served by %s, %d officer(s); Bloomberg leg %r" % (key, served.get("leg"), count, bloomberg.get("outcome")))
        chain_ok.append(count >= 1 and not bloomberg.get("needs_new_pull")
                        and (served.get("leg") != "bloomberg" or bloomberg.get("outcome") == "served officers"))
    clause("C4 the chain serves officers for both slash names and for the control", all(chain_ok))
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R78 BB4 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
