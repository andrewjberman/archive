"""MDPF_CANON round 4, cell CN-d-1, criterion AC2 -- the global account-distribution names the vintage of the cottonwood
leg it folded (CTO ADDENDUM 1 @187b53dbe6, AC3 re-cut; no served value moves, one key set added under `meta`).

One command, three arms, offline (the units function and the sidecar are replaced by synthetic ones; no AWS call);
prints `ROUND 4 VINTAGE: k of 3 arms` and exits 0 only on all three.
Root = $R4_ROOT, else `git rev-parse --show-toplevel`.

  V1 a sidecar dated TODAY -> meta.cottonwood_fold.value_date == that date and age_trading_days == 0
  V2 a sidecar dated 2026-10-07 -> value_date == '2026-10-07' and age_trading_days is an int >= 1
  V3 no served value moves: `total` and `by_model` are identical between V1 and V2, and the cottonwood_fold key set is
     exactly {accounts_folded, by_model_folded, source, note, value_date, age_trading_days}
"""
import copy
import datetime as dt
import importlib
import os
import subprocess
import sys

EXPECT_KEYS = {"accounts_folded", "by_model_folded", "source", "note", "value_date", "age_trading_days"}


def _root() -> str:
    r = os.environ.get("R4_ROOT")
    if r:
        return r
    return subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()


def _units():
    import pandas as pd
    return (pd.DataFrame({"unit_id": ["a1", "a2", "a3", "a4"],
                          "model_key": ["opal_intermediate"] * 4,
                          "value": [1000.0, 2500.0, 4000.0, 9000.0]}), 4, "2026-10-08", "UNIT-TEST")


def _sidecar(value_date: str) -> dict:
    return {"value_date": value_date, "total_unit_values": [1500.0, 3000.0],
            "by_model_unit_values": {"opal_intermediate": [1500.0, 3000.0]}}


def _build(mod, value_date: str) -> dict:
    mod._FIRM_UNITS["global"] = _units
    mod._cottonwood_sidecar = lambda: _sidecar(value_date)
    return mod.build_firm_distribution("global", "Global")


def main() -> int:
    root = _root()
    for sub in ("scripts/silver", "scripts/gold"):
        p = os.path.normpath(os.path.join(root, "data", "mdpf", sub))
        if p not in sys.path:
            sys.path.insert(0, p)
    try:
        mod = importlib.import_module("dim_mdpf_account_distribution")
    except Exception as exc:                                  # noqa: BLE001
        print(f"  V1 FAIL: module import raised {type(exc).__name__}: {str(exc)[:160]}")
        print("ROUND 4 VINTAGE: 0 of 3 arms")
        return 1

    today = dt.date.today().isoformat()
    past = "2026-10-07"
    arms = []
    out1 = out2 = None

    try:
        out1 = _build(mod, today)
        f1 = (out1.get("meta") or {}).get("cottonwood_fold") or {}
        ok = f1.get("value_date") == today and f1.get("age_trading_days") == 0
        print("  V1 %s: today-dated sidecar -> value_date=%r age_trading_days=%r" % (
            "PASS" if ok else "FAIL", f1.get("value_date"), f1.get("age_trading_days")))
        arms.append(ok)
    except BaseException as exc:                              # noqa: BLE001
        print(f"  V1 FAIL: {type(exc).__name__}: {str(exc)[:160]}")
        arms.append(False)

    try:
        out2 = _build(mod, past)
        f2 = (out2.get("meta") or {}).get("cottonwood_fold") or {}
        age = f2.get("age_trading_days")
        ok = f2.get("value_date") == past and isinstance(age, int) and not isinstance(age, bool) and age >= 1
        print("  V2 %s: %s-dated sidecar -> value_date=%r age_trading_days=%r" % (
            "PASS" if ok else "FAIL", past, f2.get("value_date"), age))
        arms.append(ok)
    except BaseException as exc:                              # noqa: BLE001
        print(f"  V2 FAIL: {type(exc).__name__}: {str(exc)[:160]}")
        arms.append(False)

    ok = False
    if out1 is not None and out2 is not None:
        same = (copy.deepcopy(out1.get("total")) == copy.deepcopy(out2.get("total"))
                and copy.deepcopy(out1.get("by_model")) == copy.deepcopy(out2.get("by_model")))
        keys = set(((out1.get("meta") or {}).get("cottonwood_fold") or {}).keys())
        ok = same and keys == EXPECT_KEYS
        print("  V3 %s: served total/by_model identical across vintages=%s; cottonwood_fold keys %s" % (
            "PASS" if ok else "FAIL", same, "exact" if keys == EXPECT_KEYS else "differ: " + str(sorted(keys ^ EXPECT_KEYS))))
    else:
        print("  V3 FAIL: V1 or V2 did not build")
    arms.append(ok)

    k = sum(1 for a in arms if a)
    print(f"ROUND 4 VINTAGE: {k} of {len(arms)} arms")
    return 0 if k == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
