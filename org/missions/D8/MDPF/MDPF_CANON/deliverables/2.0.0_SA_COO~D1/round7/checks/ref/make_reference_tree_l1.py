#!/usr/bin/env python
"""Scratch REFERENCE tree for MDPF_CANON round 7 cell CN-l-1. NEVER committed to a product path.

  python make_reference_tree_l1.py --out DIR [--mutant none|nocap|noasof|allkeys|frontiercount]

Copies data/mdpf/ (9 MB) into DIR/data/mdpf/ and applies the reference change to DIR/data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py
(the repo is not touched). Then: python ../r7_cn_l_1.py unit --root DIR   (and seams, real).
Mutants plant one defect each and must turn the named arm red:
  nocap          the 4-day window is dropped (a pooled date of any age carries)      -> U4, R4        (measured)
  noasof         the carried value is served without its `as_of` stamp               -> U2, U3, U7, U8, R2, R3 (measured; S4 on seams)
  allkeys        the dated rule is applied to every model key, not the fold line     -> U6            (measured)
  frontiercount  the carried row's count is the count frontier, not the carried date's -> U7          (measured)
"""
import argparse
import os
import shutil
import subprocess
import sys

OLD_CONST = '''    "other_models",
]
'''
NEW_CONST = '''    "other_models",
]
# CN-l-1 (rows D1-W16-S2, D1-W16-S4; CTO round-6 analysis section 3 item 1): the Global fold line carries its date or it is blank.
OTHER_MODELS_KEY = "other_models"
OTHER_MODELS_CARRY_MAX_DAYS = 4


def _dated_carry(dates: list, values: list, gi: int, max_days: "int | None") -> tuple:
    """(value, date) of the last non-None value at or before index gi, only if that date is within max_days calendar
    days of dates[gi]; otherwise (None, None). A value on the as-of itself is the caller's current value, not a carry."""
    asof = dt.date.fromisoformat(dates[gi])
    for j in range(min(gi, len(values) - 1), -1, -1):
        if values[j] is not None:
            if max_days is not None and (asof - dt.date.fromisoformat(dates[j])).days > max_days:
                return None, None
            return values[j], dates[j]
    return None, None
'''

OLD_LOOP = '''        cur_val = mvals[gi] if gi < len(mvals) else None
        if cur_val is None:
            # a key absent at the frontier (e.g. its carrying firm past-window)
            # falls back to its last real value, honest to the fold's own series.
            cur_val = _frontier(mvals)
        if cur_val is None:
            continue
        cur_val = round(float(cur_val), 2)
        # counts NEVER carried (standing law): the per-key count frontier is the
        # last REAL count in the fold's own series (may lag the value frontier).
        cur_cnt = _frontier(node.get("account_count"))
'''
NEW_LOOP = '''        cur_val = mvals[gi] if gi < len(mvals) else None
        carried_at = None
        if cur_val is None and mk == OTHER_MODELS_KEY:
            # CN-l-1: the fold line carries its date or is blank (within OTHER_MODELS_CARRY_MAX_DAYS calendar days).
            cur_val, carried_at = _dated_carry(dates, mvals, gi, OTHER_MODELS_CARRY_MAX_DAYS)
        elif cur_val is None:
            # a key absent at the frontier (e.g. its carrying firm past-window)
            # falls back to its last real value, honest to the fold's own series.
            cur_val = _frontier(mvals)
        if cur_val is None:
            continue
        cur_val = round(float(cur_val), 2)
        # counts NEVER carried (standing law): the per-key count frontier is the
        # last REAL count in the fold's own series (may lag the value frontier);
        # a dated-carry row reads the count AT its carried date.
        _counts = node.get("account_count") or []
        if carried_at is not None:
            _ci = dates.index(carried_at)
            cur_cnt = _counts[_ci] if _ci < len(_counts) else None
        else:
            cur_cnt = _frontier(_counts)
'''
OLD_APPEND = '''        model_results.append({
            "model_name": SERVED_MODEL_NAME[mk],
            "aum": cur_val,
            "account_count": int(cur_cnt) if cur_cnt is not None else None,
            "q0": calc_metric(cur_val, get_value_at_date(mseries, q0e)),
            "q1": calc_metric(cur_val, get_value_at_date(mseries, q1e)),
            "q2": calc_metric(cur_val, get_value_at_date(mseries, q2e)),
            "q3": calc_metric(cur_val, get_value_at_date(mseries, q3e)),
        })
'''
NEW_APPEND = '''        _row = {
            "model_name": SERVED_MODEL_NAME[mk],
            "aum": cur_val,
            "account_count": int(cur_cnt) if cur_cnt is not None else None,
            "q0": calc_metric(cur_val, get_value_at_date(mseries, q0e)),
            "q1": calc_metric(cur_val, get_value_at_date(mseries, q1e)),
            "q2": calc_metric(cur_val, get_value_at_date(mseries, q2e)),
            "q3": calc_metric(cur_val, get_value_at_date(mseries, q3e)),
        }
        if carried_at is not None:
            _row["as_of"] = carried_at
        model_results.append(_row)
'''


def once(text, old, new, label):
    if text.count(old) != 1:
        sys.exit("ERROR: %s anchor found %d times (want 1) -- the base file moved" % (label, text.count(old)))
    return text.replace(old, new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--mutant", default="none", choices=["none", "nocap", "noasof", "allkeys", "frontiercount"])
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=30).stdout.strip()
    dst = os.path.join(os.path.abspath(a.out), "data")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(os.path.join(root, "data", "mdpf"), os.path.join(dst, "mdpf"),
                    ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    # the gold scripts resolve lib.trading_calendar and lib.opal_naming (and its registry) from <root> (repo layout); lib/ has no __init__.py
    # test_canplat_p1_1.py also reads data/assets/scripts/{gold,silver} (build_cottonwood_mdpf_slice, rebalancer_schemas) and the
    # CVO's committed G2 comparator under org/tier1_exec/3.0.0_SA_CVO/deliverables/MDPF_CANPLAT_G2
    for sub in ("lib", os.path.join("infra", "logic"), os.path.join("data", "assets", "scripts"),
                os.path.join("org", "tier1_exec", "3.0.0_SA_CVO", "deliverables", "MDPF_CANPLAT_G2")):
        d2 = os.path.join(os.path.abspath(a.out), sub)
        if os.path.exists(d2):
            shutil.rmtree(d2)
        if os.path.isdir(os.path.join(root, sub)):
            shutil.copytree(os.path.join(root, sub), d2, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    f = os.path.join(dst, "mdpf", "scripts", "gold", "dim_mdpf_aum_metrics.py")
    with open(f, "rb") as fh:
        text = fh.read().decode("utf-8").replace("\r\n", "\n")
    text = once(text, OLD_CONST, NEW_CONST, "constants")
    text = once(text, OLD_LOOP, NEW_LOOP, "loop")
    text = once(text, OLD_APPEND, NEW_APPEND, "append")
    if a.mutant == "nocap":
        text = text.replace("OTHER_MODELS_CARRY_MAX_DAYS = 4", "OTHER_MODELS_CARRY_MAX_DAYS = None")
    elif a.mutant == "noasof":
        text = text.replace('            _row["as_of"] = carried_at\n', '            pass\n')
    elif a.mutant == "allkeys":
        text = text.replace("if cur_val is None and mk == OTHER_MODELS_KEY:", "if cur_val is None:")
    elif a.mutant == "frontiercount":
        text = text.replace("            cur_cnt = _counts[_ci] if _ci < len(_counts) else None\n",
                            "            cur_cnt = _frontier(_counts)\n")
    with open(f, "wb") as fh:
        fh.write(text.encode("utf-8"))
    print("OK: reference tree (%s) at %s" % (a.mutant, os.path.abspath(a.out)))


if __name__ == "__main__":
    main()
