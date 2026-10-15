#!/usr/bin/env python3
"""Build a REFERENCE TREE for the CN-r-1 issuer checks (the dry-run that proves the arms CAN pass).

  python make_reference_tree_r1.py <dest-dir> [--mutant NAME]

Copies, read-only from the repo at the current checkout, data/mdpf/scripts, data/mdpf/tests, lib/, the naming registry and the gold
package's build_package.py into <dest-dir>, applies the cell's change as the ISSUER'S REFERENCE (never a worker's code, never
committed to the repo) and appends six tests to the CN-p-1 test file. Then:   R10_ROOT=<dest-dir> python r10_cn_r_1.py pure|seams|oracle

--mutant NAME applies the reference WITH ONE DEFECT so the issuer can show an arm fails on it (an arm that cannot fail is not an arm):
  no-carry | carry-before-first | carry-gaetr | no-carried-date | reset-at-cut | mutates-input |
  carry-unconditional | date-when-refused | fail-open-no-model | row-level

Every patch asserts it applied exactly once; a drift in a target file fails loud instead of silently skipping.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONST_OLD = "SMARTX_LOOKBACK_DAYS = 10\n"
CONST_NEW = ("SMARTX_LOOKBACK_DAYS = 10\n"
             "# MDPF_CANON CN-r-1 (PRD v2.22, override (c) and (d)): the legs whose MISSING value on a total-bearing row carries the\n"
             "# leg's last known value ONLY IF the carried row still partitions the served Total (forward only, never before the\n"
             "# leg's first value). The Global All Equity TR leg is a terminated SMArtX-only model and is not in this tuple.\n"
             "TREND_CARRY_LEGS = (\"div\", \"growth\", \"sma\")\n"
             "TREND_IDENTITY_TOL = 0.011   # the readback's IDENTITY_TOL: three 2-decimal roundings\n")

REF_TEST = '''

# ---- MDPF_CANON CN-r-1: a missing leg carries its last known value only if the carried row still partitions the Total ----------
def _gaps_doc():
    """Post-cut-off, flat legs; Dividend missing on 06-03, Growth on 06-04, sma_additive on 06-05 (first value 06-02). The served
    Total contains every missing leg: model_aua = total - non_model - the true sleeve."""
    return {"dates": ["2026-06-01", "2026-06-02", "2026-06-03", "2026-06-04", "2026-06-05", "2026-06-08"],
            "opal_aggregate_aua": [100.0] * 6, "non_model_aua": [50.0] * 6, "model_aua": [50.0, 48.0, 48.0, 48.0, 48.0, 48.0],
            "sma_additive_aua": [None, 2.0, 2.0, 2.0, None, 2.0],
            "by_model": {"opal_div_sma": {"model_value": [6.0, 6.0, None, 6.0, 6.0, 6.0]},
                         "opal_growth_sma": {"model_value": [4.0, 4.0, 4.0, None, 4.0, 4.0]}}}


def test_missing_leg_carries_when_the_total_contains_it_and_the_date_is_carried():
    out = gc.compute_trend_groups(_gaps_doc(), {})
    assert out["client_supervised_aua"] == [40.0] * 6
    assert out["etf_strategies_aua"] == [10.0, 12.0, 12.0, 12.0, 12.0, 12.0]
    assert out["carried_dates"] == ["2026-06-03", "2026-06-04", "2026-06-05"]


def test_a_leg_the_total_excludes_stays_absent_and_the_date_is_not_carried():
    g = _gaps_doc()
    g["by_model"]["opal_div_sma"]["model_value"] = [6.0] * 6
    g["by_model"]["opal_growth_sma"]["model_value"] = [4.0] * 6
    g["sma_additive_aua"] = [None, 2.0, None, None, 2.0, 2.0]
    g["model_aua"] = [50.0, 48.0, 50.0, 50.0, 48.0, 48.0]
    out = gc.compute_trend_groups(g, {})
    assert out["etf_strategies_aua"] == [10.0, 12.0, 10.0, 10.0, 12.0, 12.0]
    assert out["client_supervised_aua"] == [40.0] * 6
    assert out["carried_dates"] == []


def test_each_leg_is_decided_alone_on_a_row():
    g = _gaps_doc()
    g["by_model"]["opal_div_sma"]["model_value"] = [6.0, 6.0, 6.0, None, 6.0, 6.0]
    g["by_model"]["opal_growth_sma"]["model_value"] = [4.0] * 6
    g["sma_additive_aua"] = [None, 2.0, 2.0, None, 2.0, 2.0]
    g["model_aua"] = [50.0, 48.0, 48.0, 50.0, 48.0, 48.0]
    out = gc.compute_trend_groups(g, {})
    assert out["client_supervised_aua"] == [40.0] * 6
    assert out["etf_strategies_aua"] == [10.0, 12.0, 12.0, 10.0, 12.0, 12.0]
    assert out["carried_dates"] == ["2026-06-04"]


def test_a_leg_is_never_carried_before_its_first_value():
    g = _gaps_doc()
    g["by_model"]["opal_div_sma"]["model_value"] = [None, None, 6.0, 6.0, 6.0, 6.0]
    g["by_model"]["opal_growth_sma"]["model_value"] = [4.0] * 6
    g["sma_additive_aua"] = [None, None, None, 2.0, 2.0, 2.0]
    g["model_aua"] = [50.0, 50.0, 50.0, 48.0, 48.0, 48.0]
    out = gc.compute_trend_groups(g, {})
    assert out["client_supervised_aua"] == [46.0, 46.0, 40.0, 40.0, 40.0, 40.0]
    assert out["etf_strategies_aua"] == [4.0, 4.0, 10.0, 12.0, 12.0, 12.0]
    assert out["carried_dates"] == []


def test_the_smartx_leg_and_the_cutoff_boundary_share_one_memory_and_gaetr_is_never_carried():
    g = {"dates": ["2026-05-13", "2026-05-14", "2026-05-15", "2026-05-16", "2026-05-18"],
         "opal_aggregate_aua": [100.0] * 5, "non_model_aua": [60.0] * 5, "model_aua": [40.0] * 5,
         "by_model": {"opal_growth_sma": {"model_value": [None, None, None, None, 4.0]}}}
    smx = {"2026-05-13": {"div": 6.0, "growth": 4.0, "gaetr": 1.0}, "2026-05-14": {"div": 6.0, "growth": 4.0, "gaetr": 1.0},
           "2026-05-15": {"growth": 4.0, "gaetr": 1.0}, "2026-05-16": {"div": 6.0, "growth": 4.0}}
    out = gc.compute_trend_groups(g, smx)
    assert out["client_supervised_aua"] == [49.0, 49.0, 49.0, 50.0, 50.0]
    assert out["etf_strategies_aua"] == [10.0] * 5
    assert out["carried_dates"] == ["2026-05-15", "2026-05-18"]


def test_no_model_aua_means_no_carry_and_the_input_is_not_mutated():
    g = _gaps_doc()
    del g["model_aua"]
    before = copy.deepcopy(g)
    out = gc.compute_trend_groups(g, {})
    assert g == before
    assert out["carried_dates"] == []
    assert out["client_supervised_aua"] == [40.0, 40.0, 46.0, 44.0, 40.0, 40.0]
'''


def _sub(path: str, old: str, new: str) -> None:
    with open(path, encoding="utf-8", newline="") as fh:
        s = fh.read()
    nl = "\r\n" if "\r\n" in s else "\n"
    if nl == "\r\n":
        old = old.replace("\n", "\r\n")
        new = new.replace("\n", "\r\n")
    if s.count(old) != 1:
        raise SystemExit("PATCH DRIFT: %r occurs %d times in %s" % (old[:70], s.count(old), path))
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(s.replace(old, new))


def _replace_compute(path: str, new_src: str) -> None:
    with open(path, encoding="utf-8", newline="") as fh:
        s = fh.read()
    nl = "\r\n" if "\r\n" in s else "\n"
    s = s.replace("\r\n", "\n")
    if s.count("def compute_trend_groups(") != 1 or s.count("def load_smartx_sma_legs(") != 1:
        raise SystemExit("PATCH DRIFT: compute_trend_groups / load_smartx_sma_legs markers")
    a = s.index("def compute_trend_groups(")
    b = s.index("def load_smartx_sma_legs(")
    s = s[:a] + new_src.rstrip("\n") + "\n\n\n" + s[b:]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(s.replace("\n", nl))


def _mutate(src: str, old: str, new: str) -> str:
    if src.count(old) != 1:
        raise SystemExit("MUTANT DRIFT: %r occurs %d times" % (old[:70], src.count(old)))
    return src.replace(old, new)


def _apply_mutant(mutant, src, const_new):
    if mutant == "no-carry":
        const_new = _mutate(const_new, 'TREND_CARRY_LEGS = ("div", "growth", "sma")', "TREND_CARRY_LEGS = ()")
    if mutant == "carry-gaetr":
        src = _mutate(src, 'gaetr = leg.get("gaetr") if _leg_present(leg.get("gaetr")) else 0.0',
                      'if _leg_present(leg.get("gaetr")):\n                last["gaetr_m"] = float(leg["gaetr"])\n'
                      '            gaetr = last.get("gaetr_m", 0.0)')
    if mutant == "carry-before-first":
        src = _mutate(src, "    last: dict = {}\n",
                      "    last: dict = {}\n    for _k, _arr in ((\"div\", div_g), (\"growth\", growth_g), (\"sma\", sma)):\n"
                      "        _first = next((x for x in _arr if _leg_present(x)), None)\n"
                      "        if _first is not None:\n            last[_k] = float(_first)\n")
    if mutant == "no-carried-date":
        src = _mutate(src, "            leg_carried.add(d)\n", "            pass\n")
    if mutant == "reset-at-cut":
        src = _mutate(src, '            legs_raw = {"div": div_g[i], "growth": growth_g[i], "sma": sma[i]}\n',
                      '            if "_reset" not in last:\n                last.clear()\n                last["_reset"] = 1.0\n'
                      '            legs_raw = {"div": div_g[i], "growth": growth_g[i], "sma": sma[i]}\n')
    if mutant == "mutates-input":
        src = _mutate(src, '    dates = list(g.get("dates") or [])\n', '    dates = list(g.get("dates") or [])\n    g["_touched"] = True\n')
    if mutant == "carry-unconditional":
        src = _mutate(src, "key in last and _partitions(row, key, last[key]):", "key in last:")
    if mutant == "date-when-refused":
        src = _mutate(src, "    return 0.0, False\n\n\ndef compute_trend_groups(",
                      "    return 0.0, (key in TREND_CARRY_LEGS and key in last)\n\n\ndef compute_trend_groups(")
    if mutant == "fail-open-no-model":
        src = _mutate(src, '    if row["model"] is None:\n        return False\n', '    if row["model"] is None:\n        return True\n')
    if mutant == "row-level":
        src = _mutate(src, "    v[key] = cand\n",
                      "    v[key] = cand\n    for _k in (\"div\", \"growth\", \"sma\"):\n"
                      "        if _k in row[\"last\"] and row[\"vals\"][_k] == 0.0:\n            v[_k] = row[\"last\"][_k]\n")
        src = _mutate(src, 'row = {"total": total[i],', 'row = {"last": last, "total": total[i],')
    return src, const_new


def main() -> int:
    args = sys.argv[1:]
    mutant = None
    if "--mutant" in args:
        i = args.index("--mutant")
        mutant = args[i + 1]
        del args[i:i + 2]
    dest = os.path.abspath(args[0])
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    if os.path.exists(dest):
        raise SystemExit("dest exists: " + dest)
    ign = shutil.ignore_patterns("__pycache__", "*.pyc")
    for rel in (("data", "mdpf", "scripts"), ("data", "mdpf", "tests"), ("lib",), ("infra", "logic", "registry")):
        shutil.copytree(os.path.join(root, *rel), os.path.join(dest, *rel), ignore=ign)
    os.makedirs(os.path.join(dest, "org", "standards"), exist_ok=True)
    shutil.copy2(os.path.join(root, "org", "standards", "NAMING_SCHEMA.json"),
                 os.path.join(dest, "org", "standards", "NAMING_SCHEMA.json"))
    bp = os.path.join("infra", "aws", "lambda", "mdpf-pipeline", "mdpf-gold-lambda")
    os.makedirs(os.path.join(dest, bp), exist_ok=True)
    shutil.copy2(os.path.join(root, bp, "build_package.py"), os.path.join(dest, bp, "build_package.py"))
    con = os.path.join(dest, "data", "mdpf", "scripts", "gold", "mdpf_gold_consolidator.py")
    with open(os.path.join(HERE, "ref_compute_r1.txt"), encoding="utf-8") as fh:
        src = fh.read()
    src, const_new = _apply_mutant(mutant, src, CONST_NEW)
    _sub(con, CONST_OLD, const_new)
    _replace_compute(con, src)
    td = os.path.join(dest, "data", "mdpf", "tests", "canon", "test_global_trend_groups.py")
    with open(td, "a", encoding="utf-8", newline="") as fh:
        fh.write(REF_TEST)
    print("reference tree at", dest, "(mutant=%s)" % mutant)
    return 0


if __name__ == "__main__":
    sys.exit(main())
