#!/usr/bin/env python3
"""MDPF_CANON cell CN-r-1 (draft, round 10) -- the PRODUCER carries a MISSING Dividend, Growth or sma_additive_aua leg on a
TOTAL-BEARING row at its last known value ONLY IF the carried row still partitions the served Total (PRD v2.22 overrides (c) and
(d); the CTO's ruling, msg 6047): total - model_aua - (Client Supervised + ETF + ALT) - the Global All Equity TR allowance within
0.011. Forward only, never before the leg's first value; the date joins carried_dates ONLY when a leg actually carried. Where the
served Total excludes the leg (sma_additive_aua on 2026-08-31..09-09) the leg stays ABSENT (0 contribution), as today.

  python r10_cn_r_1.py pure      offline fixtures: the carry where the Total contains the leg, the refusal where it does not, each leg
                                 decided alone on a row, never before the first value, the SMArtX boundary, the identity, purity, R11
  python r10_cn_r_1.py seams     the helpers and constants, the worker's tests, the CN-p-1 pure and seams checks still green
  python r10_cn_r_1.py oracle    the REAL served 2026-10-14 Global object and the REAL SMArtX partition (read-only): the 7 sleeve-less
                                 dates stay absent, the oracle / identity / carried_dates / apply / R11 hold, a PLANTED Dividend gap on a
                                 real row is carried
  python r10_cn_r_1.py selftest  base, the reference tree, every planted mutant; prints `CN-R-1 SELFTEST: OK`

Each prints `  <ARM> PASS|FAIL <detail>` per arm and `CN-R-1 <NAME>: k of n arms`; exit 0 only when every arm passes. Prints dates,
counts and differences, never an account id and never a firm level. ASCII only. Bounded: <= 12 S3 calls, ~1 min.
R10_ROOT overrides the repo root (the issuer's reference-tree dry-run uses it).

  PURE    M0 CONTROL: the grader FAILS a planted mutant.   P0 CONTROL: the CN-p-1 fixture still yields exactly its expected arrays.
          R1 gaps in each leg where the Total contains the leg: carried, groups computed from the carried leg, the dates in carried_dates.
          R2 GUARD: a leg is never carried before its first value; those rows are not carried dates.
          R3 the SMArtX legs and the 2026-05-18 boundary share one memory per leg; the Global All Equity TR leg is never carried.
          R4 the partition identity holds on every row of every planted fixture (the Global All Equity TR allowance before it).
          R5 GUARD: purity (inputs untouched, carried_dates sorted and unique).
          R6 the readback's R11 on a newest row lacking a leg: carried by the producer reads CARRIED, withheld or refused reads Branch B.
          R7 GUARD: where the Total EXCLUDES the sleeve the leg stays absent and the date is NOT a carried date.
          R8 each leg is decided alone on a row: a Dividend gap carries even when the sleeve gap on the same row is refused.
          R9 GUARD: a row with no model_aua cannot be shown to partition: no carry (fail closed).
  SEAMS   S0 CONTROL r9_cn_p_1.py pure 7 of 7.  S1 helpers `_leg_present`, `_partitions`, `_leg_carry`, TREND_CARRY_LEGS, TREND_IDENTITY_TOL
          exist and BEHAVE.  S2 the worker's test file passes with >= 13 tests.  S3 CONTROL r9_cn_p_1.py seams 7 of 7.
  ORACLE  O0 CONTROL: 497 dates, 9 no-total dates, sma_additive_aua missing after its first value on total-bearing dates (the 7).
          O1 an independent derivation (this file's own code, algebraic identity) equals the tree's three arrays on EVERY date.
          O2 the 9 period ends equal the amended oracle (+-0.05M; readback R3).   O3 CN-p-1 oracle O3 form: model + groups + allowance = total.
          O4 CN-p-1 oracle O4 form: carried_dates == the 9 no-total dates; groups on them equal the previous dated row; ALT None before 09-30.
          O5 CN-p-1 oracle O5 form: apply changes only the four keys and meta.trend_groups; 49 Financial all-None.
          O6 the readback's R4 limits (+-0.011 after 2025-03-27, the allowance before) on every dated row.
          O7 the sleeve-less dates keep sma ABSENT: ETF = Dividend + Growth there and the dates are not carried dates.
          O8 the readback's R11 (r11_check) on the served object merged with the tree's output.
          O9 PLANTED: a Dividend value deleted on a real row whose Total still contains it is carried (the partition holds); nothing else moves.
          Om CONTROL: the comparator FAILS a planted mutant (ETF zero-filled).
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BUCKET = "opal-data-assets"
G_KEY = "portal/gold/mdpf/global/aggregate-aua-timeseries/2026-10-14.json"
F_KEY = "portal/gold/mdpf/49financial/aggregate-aua-timeseries/2026-10-14.json"
LEGS_TODAY = "2026-10-15"
CUT = "2026-05-18"
TOL = 0.011
GROUPS = ("client_supervised_aua", "etf_strategies_aua", "alt_strategies_aua")
TEST_NEW = "data/mdpf/tests/canon/test_global_trend_groups.py"
# the CRO amended oracle ($M, last dated row on or before the period end): client supervised, ETF, ALT
ORACLE = {"2024-12-31": (356.8, 5.8, 0.0), "2025-03-31": (275.8, 13.1, 0.0), "2025-06-30": (234.3, 17.2, 0.0),
          "2025-09-30": (239.4, 19.9, 0.0), "2025-12-31": (268.8, 22.2, 0.0), "2026-03-31": (250.7, 23.7, 0.0),
          "2026-06-30": (228.6, 23.1, 0.0), "2026-09-30": (266.6, 21.2, 24.8), "2026-10-13": (292.3, 21.5, 29.2)}


def _root() -> str:
    r = os.environ.get("R10_ROOT")
    if r:
        return r
    return subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()


def _load(root: str):
    for sub in ("scripts/silver", "scripts/gold"):
        p = os.path.normpath(os.path.join(root, "data", "mdpf", sub))
        if p not in sys.path:
            sys.path.insert(0, p)
    if root not in sys.path:
        sys.path.insert(0, root)
    for m in [m for m in sys.modules if m == "mdpf_gold_consolidator"]:
        del sys.modules[m]
    return importlib.import_module("mdpf_gold_consolidator")


def _find(rel_candidates):
    for c in rel_candidates:
        if c and os.path.exists(c):
            return c
    return None


def _top():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, cwd=HERE).stdout.strip()


def _p1_check():
    here = os.path.normpath(os.path.join(HERE, "..", "..", "round9", "checks", "r9_cn_p_1.py"))
    alt = os.path.join(_top(), "org", "missions", "D8", "MDPF", "MDPF_CANON", "deliverables", "2.0.0_SA_COO~D1", "round9", "checks", "r9_cn_p_1.py")
    return _find([os.environ.get("R10_P1CHECK", ""), here, alt])


def _readback():
    here = os.path.join(HERE, "r9_trend_groups_readback.py")
    alt = os.path.join(_top(), "org", "missions", "D8", "MDPF", "MDPF_CANON", "deliverables", "2.0.0_SA_COO~D1", "round10", "checks",
                       "r9_trend_groups_readback.py")
    p = _find([here, alt])
    spec = importlib.util.spec_from_file_location("r9_rb_r10", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _Arms:
    def __init__(self):
        self.res = []

    def __call__(self, name, ok, detail):
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))
        self.res.append(bool(ok))

    def done(self, title):
        k = sum(self.res)
        print("CN-R-1 %s: %d of %d arms" % (title, k, len(self.res)))
        return 0 if k == len(self.res) else 1


# ------------------------------------------------------------------ fixtures (flat legs, post cut-off unless stated)
D6 = ["2026-06-01", "2026-06-02", "2026-06-03", "2026-06-04", "2026-06-05", "2026-06-08"]


def _doc(dates, div, growth, sma, model=None, nm=50.0, total=100.0, tax=None):
    """model_aua = total - non_model - the sleeve the Total CONTAINS on that row (so the identity is the served truth)."""
    n = len(dates)
    d = {"dates": list(dates), "opal_aggregate_aua": [total] * n, "non_model_aua": [nm] * n,
         "tax_additive_aua": list(tax) if tax else [None] * n, "sma_additive_aua": list(sma),
         "by_model": {"opal_div_sma": {"model_value": list(div)}, "opal_growth_sma": {"model_value": list(growth)}}}
    if model is not None:
        d["model_aua"] = list(model)
    return d


# Dividend missing 06-03, Growth 06-04, sma_additive 06-05 (first value 06-02); the Total CONTAINS each missing leg
FIX_R = _doc(D6, [6.0, 6.0, None, 6.0, 6.0, 6.0], [4.0, 4.0, 4.0, None, 4.0, 4.0], [None, 2.0, 2.0, 2.0, None, 2.0],
             model=[50.0, 48.0, 48.0, 48.0, 48.0, 48.0])
WANT_R = {"client_supervised_aua": [40.0] * 6, "etf_strategies_aua": [10.0, 12.0, 12.0, 12.0, 12.0, 12.0],
          "alt_strategies_aua": [None] * 6, "carried_dates": ["2026-06-03", "2026-06-04", "2026-06-05"]}
# first values later (Dividend 06-03, sma 06-04): nothing before them is carried
FIX_N = _doc(D6, [None, None, 6.0, 6.0, 6.0, 6.0], [4.0] * 6, [None, None, None, 2.0, 2.0, 2.0], model=[50.0, 50.0, 50.0, 48.0, 48.0, 48.0])
WANT_N = {"client_supervised_aua": [46.0, 46.0, 40.0, 40.0, 40.0, 40.0], "etf_strategies_aua": [4.0, 4.0, 10.0, 12.0, 12.0, 12.0],
          "alt_strategies_aua": [None] * 6, "carried_dates": []}
# the sleeve gap on 06-03 and 06-04: the Total EXCLUDES it there (model_aua 50 = total - non_model): stays absent
FIX_X = _doc(D6, [6.0] * 6, [4.0] * 6, [None, 2.0, None, None, 2.0, 2.0], model=[50.0, 48.0, 50.0, 50.0, 48.0, 48.0])
WANT_X = {"client_supervised_aua": [40.0] * 6, "etf_strategies_aua": [10.0, 12.0, 10.0, 10.0, 12.0, 12.0],
          "alt_strategies_aua": [None] * 6, "carried_dates": []}
# on 06-04 BOTH Dividend and the sleeve are missing; the Total contains the Dividend, excludes the sleeve: Dividend carries, sleeve does not
FIX_M = _doc(D6, [6.0, 6.0, 6.0, None, 6.0, 6.0], [4.0] * 6, [None, 2.0, 2.0, None, 2.0, 2.0], model=[50.0, 48.0, 48.0, 50.0, 48.0, 48.0])
WANT_M = {"client_supervised_aua": [40.0] * 6, "etf_strategies_aua": [10.0, 12.0, 12.0, 10.0, 12.0, 12.0],
          "alt_strategies_aua": [None] * 6, "carried_dates": ["2026-06-04"]}
# FIX_R without model_aua: the partition cannot be shown, nothing carries
FIX_Z = copy.deepcopy(FIX_R)
del FIX_Z["model_aua"]
WANT_Z = {"client_supervised_aua": [40.0, 40.0, 46.0, 44.0, 40.0, 40.0], "etf_strategies_aua": [10.0, 12.0, 6.0, 8.0, 10.0, 12.0],
          "alt_strategies_aua": [None] * 6, "carried_dates": []}
# SMArtX legs before the cut-off, Global's after; Dividend missing on 05-15 (SMArtX) and on 05-18 (Global): one memory; gaetr missing on 05-16
D5 = ["2026-05-13", "2026-05-14", "2026-05-15", "2026-05-16", "2026-05-18"]
FIX_S = {"dates": D5, "opal_aggregate_aua": [100.0] * 5, "non_model_aua": [60.0] * 5, "model_aua": [40.0] * 5,
         "by_model": {"opal_growth_sma": {"model_value": [None, None, None, None, 4.0]}}}
SMX_S = {"2026-05-13": {"div": 6.0, "growth": 4.0, "gaetr": 1.0}, "2026-05-14": {"div": 6.0, "growth": 4.0, "gaetr": 1.0},
         "2026-05-15": {"growth": 4.0, "gaetr": 1.0}, "2026-05-16": {"div": 6.0, "growth": 4.0}}
WANT_S = {"client_supervised_aua": [49.0, 49.0, 49.0, 50.0, 50.0], "etf_strategies_aua": [10.0] * 5,
          "alt_strategies_aua": [None] * 5, "carried_dates": ["2026-05-15", "2026-05-18"]}
# the CN-p-1 fixture (r9_cn_p_1.py FIX_G / FIX_SMX / FIX_WANT): its expected arrays must not move
FIX_G1 = {"dates": ["2026-05-14", "2026-05-15", "2026-05-18", "2026-05-19", "2026-09-29", "2026-09-30", "2026-10-01", "2026-10-02"],
          "opal_aggregate_aua": [100.0, 100.0, 100.0, None, 100.0, 100.0, None, 100.0],
          "non_model_aua": [60.0, 60.0, 50.0, None, 40.0, 40.0, None, 40.0],
          "tax_additive_aua": [None, None, None, None, None, 5.0, None, 5.0],
          "sma_additive_aua": [None, None, None, None, None, 2.0, None, 2.0],
          "by_model": {"opal_div_sma": {"model_value": [None, None, 6.0, None, 6.0, 6.0, None, 6.0]},
                       "opal_growth_sma": {"model_value": [None, None, 4.0, None, 4.0, 4.0, None, 4.0]}}}
SMX_1 = {"2026-05-14": {"div": 6.0, "growth": 4.0, "gaetr": 1.0}, "2026-05-15": {"div": 7.0, "growth": 3.0}}
WANT_1 = {"client_supervised_aua": [49.0, 50.0, 40.0, 40.0, 30.0, 30.0, 30.0, 30.0],
          "etf_strategies_aua": [10.0, 10.0, 10.0, 10.0, 10.0, 12.0, 12.0, 12.0],
          "alt_strategies_aua": [None, None, None, None, None, 5.0, 5.0, 5.0], "carried_dates": ["2026-05-19", "2026-10-01"]}


def _grade(out, want):
    return isinstance(out, dict) and all(out.get(k) == v for k, v in want.items())


def _mutant(g, smx):
    """The planted defect: the base behaviour (a missing leg is zero): nothing carried."""
    return {"client_supervised_aua": [40.0, 40.0, 46.0, 44.0, 40.0, 40.0], "etf_strategies_aua": [10.0, 12.0, 6.0, 8.0, 10.0, 12.0],
            "alt_strategies_aua": [None] * 6, "carried_dates": []}


def _residuals(doc, out, smx=None):
    """total - model_aua - groups - the Global All Equity TR allowance (the SMArtX leg on a pre-cut-off date), per total-bearing row."""
    res = []
    for i, d in enumerate(doc["dates"]):
        gaetr = ((smx or {}).get(d) or {}).get("gaetr", 0.0) if d < CUT else 0.0
        groups = sum(out[k][i] or 0.0 for k in GROUPS)
        res.append(round(doc["opal_aggregate_aua"][i] - doc["model_aua"][i] - groups - gaetr, 4))
    return res


def pure(root: str) -> int:
    arm = _Arms()
    try:
        gc = _load(root)
    except Exception as exc:                                   # noqa: BLE001
        print("  import FAIL: %s: %s" % (type(exc).__name__, str(exc)[:160]))
        print("CN-R-1 PURE: 0 of 11 arms")
        return 1
    fn = getattr(gc, "compute_trend_groups", None)

    arm("M0", _grade(copy.deepcopy(WANT_R), WANT_R) and not _grade(_mutant(FIX_R, {}), WANT_R),
        "the grader accepts the expected arrays and rejects the planted base-behaviour mutant")

    try:
        p0 = _grade(fn(copy.deepcopy(FIX_G1), copy.deepcopy(SMX_1)), WANT_1)
    except Exception:                                          # noqa: BLE001
        p0 = False
    arm("P0", fn is not None and p0, "module imports; the CN-p-1 fixture still yields exactly its expected arrays")

    def run(g, smx):
        try:
            return fn(copy.deepcopy(g), copy.deepcopy(smx))
        except Exception as exc:                               # noqa: BLE001
            return {"error": "%s: %s" % (type(exc).__name__, str(exc)[:120])}

    def show(o):
        return "client %s etf %s carried %s" % (o.get("client_supervised_aua"), o.get("etf_strategies_aua"), o.get("carried_dates"))

    out_r = run(FIX_R, {})
    arm("R1", _grade(out_r, WANT_R), "gaps in Dividend 06-03, Growth 06-04, sleeve 06-05 where the Total contains them: " + show(out_r))

    out_n = run(FIX_N, {})
    arm("R2", _grade(out_n, WANT_N), "legs with a later first value: " + show(out_n))

    out_s = run(FIX_S, SMX_S)
    arm("R3", _grade(out_s, WANT_S), "SMArtX legs + boundary + gaetr: " + show(out_s))

    out_x, out_m = run(FIX_X, {}), run(FIX_M, {})
    resid = {}
    for nm_, doc, o, smx in (("R", FIX_R, out_r, {}), ("X", FIX_X, out_x, {}), ("M", FIX_M, out_m, {}), ("S", FIX_S, out_s, SMX_S)):
        resid[nm_] = _residuals(doc, o, smx) if "error" not in o else [9e9]
    worst = max(abs(x) for v in resid.values() for x in v)
    arm("R4", worst <= TOL, "total - model_aua - groups - allowance on every row of the four planted fixtures: max |residual| = %.4f (limit %.3f)"
        % (worst, TOL))

    g_in, s_in = copy.deepcopy(FIX_R), copy.deepcopy(SMX_S)
    out_a = fn(g_in, s_in) if fn else {}
    sorted_unique = all(isinstance(o.get("carried_dates"), list) and o["carried_dates"] == sorted(set(o["carried_dates"]))
                        for o in (out_a, out_s))
    arm("R5", g_in == FIX_R and s_in == SMX_S and sorted_unique,
        "inputs untouched %s / %s; carried_dates sorted and unique %s" % (g_in == FIX_R, s_in == SMX_S, sorted_unique))

    # R6: the readback's R11 on a fixture whose NEWEST row lacks a leg that had a value the day before
    try:
        rb = _readback()

        def trunc(doc, keep):
            q = copy.deepcopy(doc)
            for k in ("dates", "opal_aggregate_aua", "non_model_aua", "tax_additive_aua", "sma_additive_aua", "model_aua"):
                q[k] = q[k][:keep]
            for k in ("opal_div_sma", "opal_growth_sma"):
                q["by_model"][k]["model_value"] = q["by_model"][k]["model_value"][:keep]
            return q
        q = trunc(FIX_R, 5)                                    # newest row 06-05 lacks the sleeve; the Total contains it
        q["carried_dates"] = fn(copy.deepcopy(q), {})["carried_dates"]
        ok_c, det_c = rb.r11_check(q)
        q2 = copy.deepcopy(q)
        q2["carried_dates"] = []
        ok_w, det_w = rb.r11_check(q2)
        q3 = trunc(_doc(D6, [6.0] * 6, [4.0] * 6, [None, 2.0, 2.0, None, 2.0, 2.0], model=[50.0, 48.0, 48.0, 50.0, 48.0, 48.0]), 4)
        q3["carried_dates"] = fn(copy.deepcopy(q3), {})["carried_dates"]   # the Total excludes the sleeve: refused, not carried
        ok_r, det_r = rb.r11_check(q3)
        arm("R6", ok_c and "CARRIED" in det_c and not ok_w and "Branch B" in det_w and not ok_r and "Branch B" in det_r and q3["carried_dates"] == [],
            "newest row lacks the sleeve: Total contains it -> R11 %s (carried); carried_dates withheld -> %s; Total excludes it -> %s"
            % ("PASS" if ok_c else "FAIL", "PASS" if ok_w else "Branch B", "PASS" if ok_r else "Branch B"))
    except Exception as exc:                                   # noqa: BLE001
        arm("R6", False, "%s: %s" % (type(exc).__name__, str(exc)[:160]))

    arm("R7", _grade(out_x, WANT_X), "the Total excludes the sleeve on 06-03 and 06-04: stays absent, not carried: " + show(out_x))
    arm("R8", _grade(out_m, WANT_M), "06-04 Dividend gap (Total contains it) carries, sleeve gap (Total excludes it) does not: " + show(out_m))
    out_z = run(FIX_Z, {})
    arm("R9", _grade(out_z, WANT_Z), "no model_aua: nothing carries: " + show(out_z))
    return arm.done("PURE")


# ------------------------------------------------------------------ SEAMS
def _pytest(root, rel):
    r = subprocess.run([sys.executable, "-m", "pytest", rel, "-q", "-p", "no:cacheprovider"], cwd=root, capture_output=True, text=True, timeout=110)
    m = re.search(r"(\d+) passed", r.stdout)
    f = re.search(r"(\d+) failed", r.stdout)
    return r.returncode, int(m.group(1)) if m else 0, int(f.group(1)) if f else 0


def _p1(root, mode):
    p = _p1_check()
    if p is None:
        return None, "r9_cn_p_1.py not found"
    env = dict(os.environ, R9_ROOT=root)
    r = subprocess.run([sys.executable, p, mode], capture_output=True, text=True, env=env, timeout=115)
    last = (r.stdout.strip().splitlines() or [""])[-1]
    return r.returncode == 0 and ("7 of 7" in last), last


def seams(root: str) -> int:
    arm = _Arms()
    ok0, last0 = _p1(root, "pure")
    arm("S0", bool(ok0), "r9_cn_p_1.py pure: %s" % last0)
    try:
        gc = _load(root)
        lp, lc, pt = (getattr(gc, n, None) for n in ("_leg_present", "_leg_carry", "_partitions"))
        legs, tol = getattr(gc, "TREND_CARRY_LEGS", None), getattr(gc, "TREND_IDENTITY_TOL", None)
        beh = False
        if lp and lc and pt and legs is not None:
            row = {"total": 100.0, "model": 48.0, "nm": 50.0, "tax": None, "gaetr": 0.0, "vals": {"div": 6.0, "growth": 4.0, "sma": 0.0}}
            row_x = dict(row, model=50.0)                      # the Total excludes the sleeve
            row_n = dict(row, model=None)                      # no model_aua
            last: dict = {}
            a = lc(last, "div", 0.0, row)                      # zero is a value and becomes the memory
            b = lc({}, "sma", None, row)                       # never had one
            c = lc({"sma": 2.0}, "sma", None, row)             # the Total contains it: carried
            d = lc({"sma": 2.0}, "sma", None, row_x)           # the Total excludes it: absent
            e = lc({"sma": 2.0}, "sma", float("nan"), row)     # NaN is absence
            f = lc({"zzz": 1.0}, "zzz", None, row)             # a key outside TREND_CARRY_LEGS is never carried
            h = lc({"sma": 2.0}, "sma", None, row_n)           # no model_aua: absent
            k = lc({"div": 9.0}, "div", None, row_x)           # Dividend cancels: carried even where the sleeve is refused
            beh = (a == (0.0, False) and last == {"div": 0.0} and b == (0.0, False) and c == (2.0, True) and d == (0.0, False)
                   and e == (2.0, True) and f == (0.0, False) and h == (0.0, False) and k == (9.0, True)
                   and lp(0.0) and not lp(None) and not lp(float("nan"))
                   and pt(row, "sma", 2.0) and not pt(row_x, "sma", 2.0) and not pt(row_n, "sma", 2.0))
        arm("S1", tuple(legs or ()) == ("div", "growth", "sma") and tol == 0.011 and beh,
            "helpers present %s, TREND_CARRY_LEGS %s, TREND_IDENTITY_TOL %s, behaviour (zero a value, never-had, carried where the Total "
            "contains it, absent where it does not, NaN, key gate, no model_aua, Dividend cancels) %s" % (bool(lp and lc and pt), legs, tol, beh))
    except Exception as exc:                                   # noqa: BLE001
        arm("S1", False, "%s: %s" % (type(exc).__name__, str(exc)[:140]))
    try:
        rc, passed, failed = _pytest(root, TEST_NEW) if os.path.exists(os.path.join(root, TEST_NEW)) else (2, 0, 0)
        arm("S2", rc == 0 and passed >= 13, "%s: %d passed, %d failed (rc=%d; needs >= 13)" % (TEST_NEW, passed, failed, rc))
    except Exception as exc:                               # noqa: BLE001
        arm("S2", False, "%s: %s" % (type(exc).__name__, str(exc)[:120]))
    ok3, last3 = _p1(root, "seams")
    arm("S3", bool(ok3), "r9_cn_p_1.py seams: %s" % last3)
    return arm.done("SEAMS")


# ------------------------------------------------------------------ ORACLE
def _derive(g, legs):
    """An independent derivation (not the module's code; the identity in its algebraic form: the Dividend, Growth and Global All Equity TR
    legs cancel, so only the sleeve and ALT enter it): (groups, carried_dates, legs_carried_dates, sleeve_refused {date: value})."""
    dates, n = g["dates"], len(g["dates"])

    def col(v):
        v = list(v or [])
        return v + [None] * (n - len(v))
    tot, nm, md = col(g.get("opal_aggregate_aua")), col(g.get("non_model_aua")), col(g.get("model_aua"))
    tx, sm = col(g.get("tax_additive_aua")), col(g.get("sma_additive_aua"))
    bm = g.get("by_model") or {}
    dv, gr = col((bm.get("opal_div_sma") or {}).get("model_value")), col((bm.get("opal_growth_sma") or {}).get("model_value"))
    mem, carried_legs, refused = {}, set(), {}
    cs, etf, alt = [None] * n, [None] * n, [None] * n
    for i, d in enumerate(dates):
        if tot[i] is None or nm[i] is None:
            continue
        if d < CUT:
            lg = legs.get(d)
            if lg is None:
                continue
            raw = {"div": lg.get("div"), "growth": lg.get("growth")}
            gaetr = lg.get("gaetr") or 0.0
        else:
            raw = {"div": dv[i], "growth": gr[i]}
            gaetr = 0.0
        raw["sma"] = sm[i]
        own_sma = float(raw["sma"]) if raw["sma"] is not None and raw["sma"] == raw["sma"] else 0.0
        use = {}
        for k, v in raw.items():
            if v is not None and v == v:
                mem[k] = float(v)
                use[k] = float(v)
            elif k in mem:
                sma_used = mem[k] if k == "sma" else own_sma
                fits = md[i] is not None and abs(tot[i] - md[i] - nm[i] - sma_used - (tx[i] or 0.0)) <= TOL
                if fits:
                    use[k] = mem[k]
                    carried_legs.add(d)
                else:
                    use[k] = 0.0
                    if k == "sma":
                        refused[d] = mem[k]
            else:
                use[k] = 0.0
        cs[i] = round(nm[i] - use["div"] - use["growth"] - gaetr, 2)
        etf[i] = round(use["div"] + use["growth"] + use["sma"], 2)
        alt[i] = None if tx[i] is None else round(tx[i], 2)
    groups, carried = {}, set(carried_legs)
    for k, arr in zip(GROUPS, (cs, etf, alt)):
        last, o = None, []
        for i, d in enumerate(dates):
            v = arr[i]
            if v is not None:
                last = v
            elif last is not None:
                v = last
                carried.add(d)
            o.append(v)
        groups[k] = o
    return groups, sorted(carried), carried_legs, refused


def _diff_count(a, b):
    return sum(1 for k in GROUPS for x, y in zip(a[k], b[k]) if x != y)


def _period_end_diffs(g, groups):
    d, tot = g["dates"], g["opal_aggregate_aua"]
    worst, within = 0.0, 0
    for p, want in ORACLE.items():
        i = max(j for j, x in enumerate(d) if x <= p and tot[j] is not None)
        got = tuple(round((groups[k][i] or 0.0) / 1e6, 1) for k in GROUPS)
        diff = max(abs(a - b) for a, b in zip(got, want))
        worst = max(worst, diff)
        within += diff <= 0.05 + 1e-9
    return round(worst, 2), within


def oracle(root: str) -> int:
    arm = _Arms()
    try:
        gc = _load(root)
        rb = _readback()
        import boto3
        s3 = boto3.client("s3", region_name="us-east-1")
        g = json.loads(s3.get_object(Bucket=BUCKET, Key=G_KEY)["Body"].read())
        f49 = json.loads(s3.get_object(Bucket=BUCKET, Key=F_KEY)["Body"].read())
        legs, part = gc.load_smartx_sma_legs(s3, LEGS_TODAY)
    except Exception as exc:                                   # noqa: BLE001
        print("  setup FAIL: %s: %s" % (type(exc).__name__, str(exc)[:200]))
        print("CN-R-1 ORACLE: 0 of 11 arms")
        return 1
    dates, tot, model = g["dates"], g["opal_aggregate_aua"], g["model_aua"]
    notot = [d for d, t in zip(dates, tot) if t is None]
    want, _all, lcar, refused = _derive(g, legs)
    first_sma = next((d for d, v in zip(dates, g.get("sma_additive_aua") or []) if v is not None), None)
    sleeveless = sorted(d for d, t, v in zip(dates, tot, g["sma_additive_aua"]) if t is not None and v is None and d > (first_sma or "9"))

    arm("O0", len(dates) == 497 and len(notot) == 9 and part is not None and first_sma is not None and len(sleeveless) >= 1,
        "%d dates, %d with no total; SMArtX partition %s; sma_additive_aua first value %s and MISSING after it on %d total-bearing dates %s..%s"
        % (len(dates), len(notot), part, first_sma, len(sleeveless), sleeveless[:1], sleeveless[-1:]))

    fn = getattr(gc, "compute_trend_groups", None)
    out = None
    try:
        out = fn(copy.deepcopy(g), legs) if fn else None
    except Exception as exc:                                   # noqa: BLE001
        print("  (compute raised %s: %s)" % (type(exc).__name__, str(exc)[:140]))
    if out is None:
        for a_ in ("O1", "O2", "O3", "O4", "O6", "O7", "O8"):
            arm(a_, False, "no compute output")
    else:
        nd = _diff_count(want, out)
        arm("O1", nd == 0 and out["carried_dates"] == _all,
            "independent derivation vs the tree: %d differing cells over %d dates x 3 groups; carried_dates equal %s" % (
                nd, len(dates), out["carried_dates"] == _all))
        worst, within = _period_end_diffs(g, out)
        arm("O2", within == len(ORACLE), "%d of %d period ends within 0.05M of the amended oracle; max diff %.2fM" % (within, len(ORACLE), worst))
        w3, n3 = 0.0, 0
        for i, d in enumerate(dates):
            if tot[i] is None:
                continue
            gaetr = (legs.get(d) or {}).get("gaetr", 0.0) if d < "2026-05-15" else 0.0
            w3 = max(w3, abs((model[i] or 0.0) + sum(out[k][i] or 0.0 for k in GROUPS) + gaetr - tot[i]))
            n3 += 1
        arm("O3", n3 == len(dates) - len(notot) and w3 <= 0.02, "%d dated rows (denominator), max |model + groups + allowance - total| = %.4f" % (n3, w3))
        carried = out["carried_dates"]
        prev, last_dated = None, {}
        for i, d in enumerate(dates):
            if tot[i] is not None:
                prev = i
            else:
                last_dated[d] = prev
        same = all(out[k][dates.index(d)] == out[k][last_dated[d]] for d in notot for k in GROUPS[:2])
        alt_none = all(out["alt_strategies_aua"][i] is None for i, d in enumerate(dates) if d < "2026-09-30")
        arm("O4", carried == notot and same and alt_none,
            "carried_dates == the %d no-total dates %s; groups on them equal the previous dated row %s; ALT None before 2026-09-30 %s"
            % (len(notot), carried == notot, same, alt_none))
        bad, cnt = [], 0
        for i, d in enumerate(dates):
            cs_, etf_, alt_ = (out[k][i] for k in GROUPS)
            if tot[i] is None or model[i] is None or cs_ is None or etf_ is None:
                continue
            cnt += 1
            r = tot[i] - model[i] - cs_ - etf_ - (alt_ or 0.0)
            lo, hi = (-rb.IDENTITY_TOL, rb.GAETR_MAX) if d < rb.GAETR_END else (-rb.IDENTITY_TOL, rb.IDENTITY_TOL)
            if not lo <= r <= hi:
                bad.append((d, round(r, 2)))
        arm("O6", cnt > 0 and not bad, "readback R4 limits on %d dated rows; offending %s" % (cnt, bad[:3]))
        div_real = (g.get("by_model") or {}).get("opal_div_sma", {}).get("model_value") or []
        gro_real = (g.get("by_model") or {}).get("opal_growth_sma", {}).get("model_value") or []
        idx = {d: i for i, d in enumerate(dates)}
        etf_ok = all(out["etf_strategies_aua"][idx[d]] == round((div_real[idx[d]] or 0.0) + (gro_real[idx[d]] or 0.0), 2) for d in sleeveless)
        arm("O7", sorted(refused) == sleeveless and etf_ok and not (set(sleeveless) & set(carried)),
            "the %d sleeve-less dates: refused by the derivation %s; ETF = Dividend + Growth on all of them %s; none is a carried date %s"
            % (len(sleeveless), sorted(refused) == sleeveless, etf_ok, not (set(sleeveless) & set(carried))))
        gg = copy.deepcopy(g)
        gg.update(out)
        ok11, det11 = rb.r11_check(gg)
        arm("O8", ok11, "readback R11 on the served object with the tree's groups: %s" % det11[:110])

    ok, detail = False, "no apply_global_trend_groups"
    app = getattr(gc, "apply_global_trend_groups", None)
    if app is not None:
        try:
            res = app({"global": copy.deepcopy(g), "49financial": copy.deepcopy(f49)}, legs, part)

            def same(a, b):
                return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
            gd, fd = res["global"], res["49financial"]
            allowed = set(GROUPS) | {"carried_dates", "meta"}
            diffs = [k for k in g if not same(gd.get(k), g[k]) and k not in allowed]
            meta_diff = [k for k in set(g["meta"]) | set(gd["meta"]) if k != "trend_groups" and not same(gd["meta"].get(k), g["meta"].get(k))]
            fdiffs = [k for k in f49 if not same(fd.get(k), f49[k])]
            ok = not diffs and not meta_diff and not fdiffs
            detail = "Global keys changed outside the four keys and meta %s, meta keys changed %s, 49 Financial keys changed %s" % (diffs, meta_diff, fdiffs)
        except Exception as exc:                               # noqa: BLE001
            detail = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    arm("O5", ok, detail)

    # O9: delete a Dividend value on a real row whose Total still contains it; the carry restores the partition, nothing else moves
    try:
        divv = (g.get("by_model") or {}).get("opal_div_sma", {}).get("model_value") or []
        cand = [i for i in range(len(dates) - 1, 0, -1)
                if dates[i] > "2026-09-15" and tot[i] is not None and divv[i] is not None and any(
                    tot[j] is not None and divv[j] is not None for j in range(i - 1, -1, -1))]
        i9 = cand[2]
        j9 = max(j for j in range(i9) if tot[j] is not None and divv[j] is not None)
        gp = copy.deepcopy(g)
        gp["by_model"]["opal_div_sma"]["model_value"][i9] = None
        base_out = fn(copy.deepcopy(g), legs)
        pl = fn(gp, legs)
        gro9 = (g["by_model"]["opal_growth_sma"]["model_value"][i9] or 0.0)
        sm9 = g["sma_additive_aua"][i9] or 0.0
        exp_etf = round(divv[j9] + gro9 + sm9, 2)
        moved = [(k, i) for k in GROUPS for i in range(len(dates)) if pl[k][i] != base_out[k][i]]
        resid9 = tot[i9] - model[i9] - pl["client_supervised_aua"][i9] - pl["etf_strategies_aua"][i9] - (pl["alt_strategies_aua"][i9] or 0.0)
        arm("O9", pl["etf_strategies_aua"][i9] == exp_etf and dates[i9] in pl["carried_dates"] and dates[i9] not in base_out["carried_dates"]
            and {i for _, i in moved} == {i9} and abs(resid9) <= TOL and pl["carried_dates"] == sorted(set(base_out["carried_dates"]) | {dates[i9]}),
            "Dividend deleted on %s (previous value from %s): ETF = previous Dividend + Growth + sleeve %s, the date is carried %s, the "
            "residual is %.4f, cells moved %s (must be only that row)" % (dates[i9], dates[j9], pl["etf_strategies_aua"][i9] == exp_etf,
                                                                         dates[i9] in pl["carried_dates"], resid9, sorted({i for _, i in moved})))
    except Exception as exc:                                   # noqa: BLE001
        arm("O9", False, "%s: %s" % (type(exc).__name__, str(exc)[:160]))

    mut = copy.deepcopy(want)
    mut["etf_strategies_aua"] = [0.0] * len(dates)
    arm("Om", _diff_count(want, mut) > 0, "planted mutant (ETF zero-filled): %d cells differ (must flag)" % _diff_count(want, mut))
    return arm.done("ORACLE")


# ------------------------------------------------------------------ SELFTEST (issuer only)
def selftest() -> int:
    ref = os.path.join(HERE, "ref", "make_reference_tree_r1.py")
    here = os.path.abspath(__file__)
    ok_all = True
    base = _root()
    exp_base = {"pure": 6, "seams": 2, "oracle": 10}

    def run(root, mode):
        env = dict(os.environ, R10_ROOT=root)
        r = subprocess.run([sys.executable, here, mode], capture_output=True, text=True, env=env, timeout=280)
        m = re.search(r"CN-R-1 \w+: (\d+) of (\d+) arms", r.stdout)
        red = sorted(set(re.findall(r"^  (\w+) FAIL", r.stdout, re.M)))
        return (int(m.group(1)), int(m.group(2)), red) if m else (0, 0, ["no output: " + r.stderr[-120:]])
    print("-- base (the unpatched repo): build arms red, controls and guards green")
    for mode, k in exp_base.items():
        got = run(base, mode)
        ok = got[0] == k
        print("   %s base: %d of %d (expected %d) red=%s -> %s" % (mode, got[0], got[1], k, got[2], "OK" if ok else "UNEXPECTED"))
        ok_all &= ok
    tmp = tempfile.mkdtemp(prefix="r10r1_")
    d0 = os.path.join(tmp, "ref")
    subprocess.run([sys.executable, ref, d0], check=True, capture_output=True)
    print("-- the reference tree: every arm green")
    for mode in ("pure", "seams", "oracle"):
        got = run(d0, mode)
        ok = got[0] == got[1] and got[1] > 0
        print("   %s ref: %d of %d red=%s -> %s" % (mode, got[0], got[1], got[2], "OK" if ok else "NOT GREEN"))
        ok_all &= ok
    p1 = _p1_check()
    if p1:
        r = subprocess.run([sys.executable, p1, "oracle"], capture_output=True, text=True, env=dict(os.environ, R9_ROOT=d0), timeout=280)
        last = (r.stdout.strip().splitlines() or [""])[-1]
        ok = "7 of 7" in last
        print("   CN-p-1 oracle (O3-O5) on the reference tree: %s -> %s" % (last, "OK" if ok else "NOT GREEN"))
        ok_all &= ok
    muts = {"no-carry": [("pure", "R1")], "carry-before-first": [("pure", "R2")], "carry-gaetr": [("pure", "R3")],
            "no-carried-date": [("pure", "R1")], "reset-at-cut": [("pure", "R3")], "mutates-input": [("pure", "R5")],
            "carry-unconditional": [("pure", "R7"), ("oracle", "O7")], "date-when-refused": [("pure", "R7")],
            "fail-open-no-model": [("pure", "R9")], "row-level": [("pure", "R8")]}
    print("-- planted mutants: each must turn its named arm(s) red")
    for name, checks in muts.items():
        dm = os.path.join(tmp, "m_" + name)
        subprocess.run([sys.executable, ref, dm, "--mutant", name], check=True, capture_output=True)
        for mode, arm_id in checks:
            got = run(dm, mode)
            ok = arm_id in got[2]
            print("   %-20s %s red=%s (needs %s) -> %s" % (name, mode, got[2], arm_id, "caught" if ok else "MISSED"))
            ok_all &= ok
    print("CN-R-1 SELFTEST: %s" % ("OK" if ok_all else "FAILED"))
    return 0 if ok_all else 1


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "selftest":
        return selftest()
    fns = {"pure": pure, "seams": seams, "oracle": oracle}
    if mode not in fns:
        print("usage: r10_cn_r_1.py pure|seams|oracle|selftest")
        return 2
    return fns[mode](_root())


if __name__ == "__main__":
    sys.exit(main())
