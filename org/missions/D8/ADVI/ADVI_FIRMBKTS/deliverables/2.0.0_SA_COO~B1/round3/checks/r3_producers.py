"""ADVI_FIRMBKTS round 3 check for cell FB-f-9 phase A (the platinum producers' dormant per-output destination),
issuer 2.0.0_SA_COO~B1. CTO ruling: ledger/ROUND_ANALYSIS.round2.md ADDENDUM 2 (form A).

--arms static (4 arms), read-only, over the 14 writer scripts named by PRODUCER_CENSUS.json and the new shared module
`data/black_diamond/scripts/gold/lib/platinum_dest.py`:
  D1 the module compiles and exposes `destination(legacy_key, mode=None) -> (bucket, key)`. Mode unset or `legacy`:
     every one of the F7 manifest's 52,910 keys returns (S3_BUCKET's value, the same key). Mode `canonical`: every
     manifest key returns ("opal-data-49financial", the destination key r2_f7.place() computes from address()). A mode
     the code does not know raises.
  D2 each of the 14 scripts compiles, and each either references `platinum_dest` itself or imports a `lib` module
     (`gold_utils`) that does
  D3 0 string literals that are a bucket name (`'opal-data-<slug>'`) appear in the 14 scripts or in platinum_dest.py: the destination
     comes from address() output, the mode from the environment
  D4 the difference control: keys that are not platinum (gold dimensions, silver, bronze, state) return
     (S3_BUCKET's value, the same key) in `canonical` mode as in `legacy`
--root points at another tree. Never edit this file. Plain ASCII; the last line carries the arm count.
"""
import argparse
import gzip
import importlib.util
import json
import os
import py_compile
import re
import subprocess
import sys
import tempfile

DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
CENSUS = DELIV + "/0.9.0_WK_ADVI_FIRMBKTS~16/PRODUCER_CENSUS.json"
MANIFEST = DELIV + "/0.9.0_WK_ADVI_FIRMBKTS~8/F7_MANIFEST.tsv.gz"
R2F7 = DELIV + "/2.0.0_SA_COO~B1/round2/checks/r2_f7.py"
GOLD = "data/black_diamond/scripts/gold"
MODULE = GOLD + "/lib/platinum_dest.py"
NON_PLATINUM = ("gold/dimensions/accounts_dimension_latest.parquet", "gold/timeseries/account_performance.parquet",
                "silver/allocations/x.parquet", "bronze/bi/x.json", "gold/canonical/holdings/x.parquet",
                "state/watermarks/x.json")
BUCKET_LIT = re.compile(r"""['"]opal-data-[a-z0-9][a-z0-9-]*['"]""")


def _root(a):
    return a or subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _load_r2f7(root):
    spec = importlib.util.spec_from_file_location("r2f7", os.path.join(root, R2F7))
    mod = importlib.util.module_from_spec(spec)
    cwd = os.getcwd()
    os.chdir(root)
    try:
        spec.loader.exec_module(mod)
    finally:
        os.chdir(cwd)
    return mod


def _load_module(root):
    gold = os.path.join(root, GOLD)
    sys.path.insert(0, gold)
    sys.path.insert(0, os.path.join(root, "lib"))
    spec = importlib.util.spec_from_file_location("platinum_dest_under_test", os.path.join(root, MODULE))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def static(root):
    res = []
    with open(os.path.join(root, CENSUS), encoding="utf-8") as fh:
        census = json.load(fh)
    scripts = sorted({w["script"] for e in census["classes"] for w in e.get("writers") or []})
    print("  writer scripts named by the census: %d" % len(scripts))
    keys = []
    with gzip.open(os.path.join(root, MANIFEST), "rt", encoding="ascii") as fh:
        for line in fh:
            if line.strip() and not line.startswith("#"):
                keys.append(line.split("\t")[0])
    d1 = False
    d4 = False
    try:
        mod = _load_module(root)
        r2 = _load_r2f7(root)
        table = r2.classes()
        naming = r2._builders()
        cfg = importlib.import_module("lib.config")
        old = getattr(cfg, "S3_BUCKET", None)
        ok = callable(getattr(mod, "destination", None)) and bool(old)
        bad_legacy = bad_canon = n_checked = 0
        for k in keys:
            if mod.destination(k) != (old, k) or mod.destination(k, "legacy") != (old, k):
                bad_legacy += 1
            want, why = r2.place(k, table, naming)
            got = mod.destination(k, "canonical")
            if why or got != (r2.DST_BUCKET, want):
                bad_canon += 1
            n_checked += 1
        try:
            mod.destination(keys[0], "no-such-mode")
            refuses = False
        except Exception:  # noqa: BLE001
            refuses = True
        print("  destination(): keys=%d legacy mismatches=%d canonical mismatches=%d unknown mode refused=%s"
              % (n_checked, bad_legacy, bad_canon, refuses))
        d1 = ok and not bad_legacy and not bad_canon and refuses and n_checked > 0
        d4 = ok and all(mod.destination(k, "canonical") == (old, k) and mod.destination(k, "legacy") == (old, k)
                        for k in NON_PLATINUM)
    except Exception as e:  # noqa: BLE001
        print("  module not usable: %s: %s" % (type(e).__name__, str(e)[:160]))
    res.append(("D1 platinum_dest.destination() is the identity in legacy mode and equals the F7 placement in canonical "
                "mode for all 52,910 manifest keys, and refuses an unknown mode", d1))

    d2 = True
    n_ref = 0
    gu = os.path.join(root, GOLD, "lib", "gold_utils.py")
    gu_ref = os.path.isfile(gu) and "platinum_dest" in open(gu, encoding="utf-8", errors="replace").read()
    for s in scripts:
        p = os.path.join(root, s)
        try:
            py_compile.compile(p, cfile=os.path.join(tempfile.gettempdir(), "r3_prod_check.pyc"), doraise=True)
        except Exception as e:  # noqa: BLE001
            print("    COMPILE %s %s" % (s, type(e).__name__))
            d2 = False
            continue
        text = open(p, encoding="utf-8", errors="replace").read()
        if "platinum_dest" in text or (gu_ref and re.search(r"gold_utils", text)):
            n_ref += 1
        else:
            print("    NO-SEAM %s" % s)
            d2 = False
    print("  scripts referencing the seam (directly or through gold_utils)=%d of %d" % (n_ref, len(scripts)))
    res.append(("D2 each of the 14 writers compiles and reaches the platinum_dest seam, directly or through gold_utils",
                d2 and n_ref == len(scripts) and bool(scripts)))

    lits = []
    for s in scripts + [MODULE]:
        p = os.path.join(root, s)
        if not os.path.isfile(p):
            lits.append((s, 0, "ABSENT"))
            continue
        for i, line in enumerate(open(p, encoding="utf-8", errors="replace").read().split("\n"), 1):
            if line.lstrip().startswith("#"):
                continue
            m = BUCKET_LIT.search(line)
            if m:
                lits.append((s, i, m.group(0)))
    for s, i, b in lits[:8]:
        print("    LITERAL %s:%d %s" % (s, i, b))
    print("  literal bucket names in the writers and the module=%d" % len(lits))
    res.append(("D3 0 literal bucket names in the 14 writers and the module (the destination is address() output, "
                "the mode comes from the environment)", not lits))
    res.append(("D4 non-platinum keys return the same bucket and key in canonical mode as in legacy mode", d4))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("static",), required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = static(root)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable (%s: %s)" % (type(e).__name__, str(e)[:160]))
        res = [("the census, the manifest and the module read", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 3 PRODUCERS STATIC: %d of 4 arms" % n)
    sys.exit(0 if n == 4 else 1)


if __name__ == "__main__":
    main()
