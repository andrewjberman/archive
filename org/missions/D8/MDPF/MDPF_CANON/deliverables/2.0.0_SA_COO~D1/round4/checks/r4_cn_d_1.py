"""MDPF_CANON round 4, cell CN-d-1 -- the served global total's identity is stated and asserted (W8-S3).

One command, five arms; prints `ROUND 4 IDENTITY: k of 5 arms` and exits 0 only on all five.
Root = $R4_ROOT, else `git rev-parse --show-toplevel` (the invocation runs from inside the worktree).

  A1 the consolidator carries assert_global_served_identity(arts)
  A2 it ACCEPTS a synthetic global whose opal_aggregate_aua = model + non_model + (tax or 0) + (sma or 0),
     including a date where opal is None (skipped) and dates where one or both additive terms are None
  A3 it REFUSES (SystemExit) a synthetic global broken by 1.00 on one date, and names that date
  A4 it ACCEPTS the served global aggregate-aua-timeseries object keyed 2026-10-08 (read-only get), on every
     non-null opal date -- the 24 dates the 2-term identity missed hold under the 4-term one
  A5 build_global_artifact's docstring (dim_mdpf_aggregate_aua_timeseries.py) names tax_additive_aua and
     sma_additive_aua, so the stale "at EVERY date" 2-term claim is stated as the BASE identity
"""
import ast
import importlib
import json
import os
import subprocess
import sys

BUCKET = "opal-data-assets"
SERVED_KEY = "portal/gold/mdpf/global/aggregate-aua-timeseries/2026-10-08.json"


def _root() -> str:
    r = os.environ.get("R4_ROOT")
    if r:
        return r
    return subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()


def _load_consolidator(root: str):
    for sub in ("scripts/silver", "scripts/gold"):
        p = os.path.normpath(os.path.join(root, "data", "mdpf", sub))
        if p not in sys.path:
            sys.path.insert(0, p)
    return importlib.import_module("mdpf_gold_consolidator")


def _synthetic(delta: float = 0.0, bad_index: int = 2) -> dict:
    dates = ["2026-10-01", "2026-10-02", "2026-10-05", "2026-10-06", "2026-10-07"]
    model = [100.0, 110.0, 120.0, 130.0, 140.0]
    non_model = [50.0, 51.0, 52.0, 53.0, 54.0]
    tax = [None, 5.0, None, 5.0, None]
    sma = [None, None, 7.0, 7.0, None]
    opal = [round(m + n + (t or 0.0) + (s or 0.0), 2) for m, n, t, s in zip(model, non_model, tax, sma)]
    opal[4] = None                         # a date with no total: skipped, not refused
    opal[bad_index] = round(opal[bad_index] + delta, 2)
    return {"global": {"dates": dates, "model_aua": model, "non_model_aua": non_model,
                       "opal_aggregate_aua": opal, "tax_additive_aua": tax, "sma_additive_aua": sma}}


def _docstring_of(path: str, func: str):
    tree = ast.parse(open(path, encoding="utf-8").read())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func:
            return ast.get_docstring(node) or ""
    return None


def main() -> int:
    root = _root()
    arms = []

    gc = None
    fn = None
    try:
        gc = _load_consolidator(root)
        fn = getattr(gc, "assert_global_served_identity", None)
    except Exception as exc:                                  # noqa: BLE001 -- an import failure is an arm failure
        print(f"  A1 FAIL: consolidator import raised {type(exc).__name__}: {str(exc)[:160]}")
    if fn is not None:
        print("  A1 PASS: assert_global_served_identity present")
        arms.append(True)
    else:
        if gc is not None:
            print("  A1 FAIL: assert_global_served_identity absent from mdpf_gold_consolidator")
        arms.append(False)

    # A2
    ok = False
    if fn is not None:
        try:
            fn(_synthetic())
            ok = True
            print("  A2 PASS: a conforming synthetic global is accepted")
        except BaseException as exc:                          # noqa: BLE001
            print(f"  A2 FAIL: conforming synthetic refused: {type(exc).__name__}: {str(exc)[:160]}")
    else:
        print("  A2 FAIL: no function")
    arms.append(ok)

    # A3
    ok = False
    if fn is not None:
        try:
            fn(_synthetic(delta=1.0, bad_index=2))
            print("  A3 FAIL: a global broken by 1.00 was accepted")
        except SystemExit as exc:
            if "2026-10-05" in str(exc):
                ok = True
                print("  A3 PASS: refused and named 2026-10-05")
            else:
                print(f"  A3 FAIL: refused but did not name the date: {str(exc)[:160]}")
        except BaseException as exc:                          # noqa: BLE001
            print(f"  A3 FAIL: wrong exception {type(exc).__name__}: {str(exc)[:160]}")
    else:
        print("  A3 FAIL: no function")
    arms.append(ok)

    # A4
    ok = False
    if fn is not None:
        try:
            import boto3
            body = boto3.client("s3", region_name="us-east-1").get_object(Bucket=BUCKET, Key=SERVED_KEY)["Body"].read()
            served = json.loads(body)
            need = ("dates", "model_aua", "non_model_aua", "opal_aggregate_aua", "tax_additive_aua", "sma_additive_aua")
            missing = [k for k in need if k not in served]
            if missing:
                print(f"  A4 FAIL: served object lacks {missing}")
            else:
                nn = sum(1 for v in served["opal_aggregate_aua"] if v is not None)
                fn({"global": {k: served[k] for k in need}})
                ok = True
                print(f"  A4 PASS: served 2026-10-08 object holds the 4-term identity on {nn} non-null dates")
        except SystemExit as exc:
            print(f"  A4 FAIL: served object refused: {str(exc)[:200]}")
        except BaseException as exc:                          # noqa: BLE001
            print(f"  A4 FAIL: {type(exc).__name__}: {str(exc)[:160]}")
    else:
        print("  A4 FAIL: no function")
    arms.append(ok)

    # A5
    doc = _docstring_of(os.path.join(root, "data", "mdpf", "scripts", "gold",
                                     "dim_mdpf_aggregate_aua_timeseries.py"), "build_global_artifact")
    ok = bool(doc) and "tax_additive_aua" in doc and "sma_additive_aua" in doc
    print("  A5 %s: build_global_artifact docstring %s" % (
        "PASS" if ok else "FAIL", "names both additive terms" if ok else "does not name tax_additive_aua and sma_additive_aua"))
    arms.append(ok)

    k = sum(1 for a in arms if a)
    print(f"ROUND 4 IDENTITY: {k} of {len(arms)} arms")
    return 0 if k == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
