#!/usr/bin/env python3
"""MDPF_CANON cell CN-p-1 (draft, round 9) -- the PRODUCER half of the Variant 1 Global AUA Trend: the Global
aggregate-aua-timeseries gains client_supervised_aua[], etf_strategies_aua[], alt_strategies_aua[] and carried_dates[]
(PRD v2.19-v2.21; CRO spec MDPF_CANON_GLOBAL_AUA_TREND_FULL_HISTORY_SPEC_20261014.md @686f769e63, amendment 1), the SMArtX
read comes from the CRO's two registry rows (ff00e3e265), and the category tree drops "Muni SMA" from SMA > ALT Strategies.

  python r9_cn_p_1.py pure      offline: the pure function, the roll-forward, the all-scope apply, the loader on a fake S3, the registry
  python r9_cn_p_1.py seams     static (AST) + two pytest runs: no typed address, the wiring order in build_all, the worker's tests
  python r9_cn_p_1.py oracle    the REAL served 2026-10-13 Global object and the REAL SMArtX partition, read-only get: the amended
                                period-end oracle, the partition identity on every dated row, the 9 carried dates, headline untouched

Each prints `  <ARM> PASS|FAIL <detail>` per arm and `CN-P-1 <NAME>: k of n arms`; exit 0 only when every arm passes.
Prints dates, counts and differences, never an account id and never a firm level. ASCII only. Bounded: <= 12 S3 calls, ~1 min.
R9_ROOT overrides the repo root (the issuer's reference-tree dry-run uses it).

  PURE    M0 CONTROL (passes at base): the grader below FAILS a planted mutant (so a PASS elsewhere can be believed).
          P0 CONTROL (passes at base): the module imports; the overlay/fold entry points and Tax's additive basis are as before.
          P1 compute_trend_groups: client supervised = non_model - Dividend - Growth - Global All Equity TR (SMArtX before
             2026-05-18, Global's carve-outs from it), ETF = Dividend + Growth + sma_additive, ALT = tax_additive; carried_dates exact.
          P2 roll FORWARD only: no group is filled before its first value; a row with no SMArtX leg is None (absent is not zero)
             and, with a prior value, carried; the input is never mutated.
          P3 apply_global_trend_groups: every built scope gains the 4 keys (Global computed, the rest all-None / []), a None scope
             stays None, the input is not mutated, meta.trend_groups names the partition.
          P4 load_smartx_sma_legs on a fake S3: ONE partition (2 gets), the keys are the builder's, role mapping, NaN/None skipped,
             lookback to an earlier partition, none -> ({}, None), AccessDenied / other failure -> C2-SIBLING FAIL-LOUD.
          P5 the category registry: "muni" is no SMA member (resolve_any raises), SMA > ALT Strategies holds exactly Tax.
  SEAMS   S0 CONTROL (passes at base): no new ruled key-set extra; the gold package ships lib/opal_naming.py and legacy_addresses.json;
             pyarrow is not imported at module scope.
          S1 the three functions exist at module level.
          S2 no typed SMArtX address: the loader types no s3 key literal, names both registry row ids, calls the builder; the
             detector is proven on a planted typed literal.
          S3 build_all order: guard_global_min_firms_fold < load_smartx_sma_legs <= apply_global_trend_groups < the first
             _shape_timeseries call.
          T1 the worker's test file passes with >= 5 tests.
          T2 CONTROL (passes at base): test_stratid_round2_inside_model.py passes (its "muni" assertion is the worker's one edit).
  ORACLE  O0 CONTROL (passes at base): the served object has 496 dates and exactly the 9 no-total dates; SMArtX equals Global's
             carve-outs on every overlap date (the spec's premise, measured now).
          O1 the loader on real S3 returns the legs for every pre-2026-05-18 total-bearing date, equal to an independent parse.
          O2 the 9 period-end values of the three groups equal the amended oracle (+-0.05M).
          O3 model_aua + the three groups + the pre-05-15 Global All Equity TR leg equals the total on every dated row (+-0.02).
          O4 carried_dates is exactly the 9 dates; on each, the groups equal the previous dated row's; ALT is None before 2026-09-30.
          O5 apply on the real Global and 49 Financial objects leaves every pre-existing key (and meta but trend_groups) equal.
          Om CONTROL (passes at base): the O2 comparator FAILS a planted mutant (client supervised without the carve-outs).
"""
from __future__ import annotations

import ast
import copy
import datetime as dt
import io
import json
import os
import re
import subprocess
import sys

BUCKET = "opal-data-assets"
G_KEY = "portal/gold/mdpf/global/aggregate-aua-timeseries/2026-10-13.json"
F_KEY = "portal/gold/mdpf/49financial/aggregate-aua-timeseries/2026-10-13.json"
TODAY = "2026-10-14"
CUT = "2026-05-18"
CONSOLIDATOR = "data/mdpf/scripts/gold/mdpf_gold_consolidator.py"
BUILD_PACKAGE = "infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py"
TEST_NEW = "data/mdpf/tests/canon/test_global_trend_groups.py"
TEST_OLD = "data/mdpf/tests/stratid/test_stratid_round2_inside_model.py"
ROW_AUM = "smartx-platform-silver-fact-model-aum-daily"
ROW_ROS = "smartx-platform-silver-fact-model-allocation-roster"
GROUPS = ("client_supervised_aua", "etf_strategies_aua", "alt_strategies_aua")
NO_TOTAL = ["2026-05-30", "2026-05-31", "2026-06-06", "2026-06-07", "2026-06-13", "2026-06-14", "2026-06-19", "2026-06-20",
            "2026-06-21"]
# the CRO amended oracle ($M, last dated row on or before the period end): client supervised, ETF, ALT
ORACLE = {"2024-12-31": (356.8, 5.8, 0.0), "2025-03-31": (275.8, 13.1, 0.0), "2025-06-30": (234.3, 17.2, 0.0),
          "2025-09-30": (239.4, 19.9, 0.0), "2025-12-31": (268.8, 22.2, 0.0), "2026-03-31": (250.7, 23.7, 0.0),
          "2026-06-30": (228.6, 23.1, 0.0), "2026-09-30": (266.6, 21.2, 24.8), "2026-10-13": (292.3, 21.5, 29.2)}


def _root() -> str:
    r = os.environ.get("R9_ROOT")
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
    import importlib
    return importlib.import_module("mdpf_gold_consolidator")


class _Arms:
    def __init__(self):
        self.res = []

    def __call__(self, name, ok, detail):
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))
        self.res.append(bool(ok))

    def done(self, title):
        k = sum(self.res)
        print("CN-P-1 %s: %d of %d arms" % (title, k, len(self.res)))
        return 0 if k == len(self.res) else 1


# ------------------------------------------------------------------ fake S3 + parquet (offline arms)
class _Body:
    def __init__(self, b):
        self._b = b

    def read(self):
        return self._b


class _NoSuchKey(Exception):
    pass


class _ClientError(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.response = {"Error": {"Code": code}}


class FakeS3:
    class exceptions:                                          # noqa: N801 -- mirrors the boto3 client attribute
        NoSuchKey = _NoSuchKey

    def __init__(self, objects, denied=False, boom=False):
        self.objects, self.denied, self.boom, self.gets = dict(objects), denied, boom, []

    def get_object(self, Bucket, Key):                         # noqa: N803
        self.gets.append(Key)
        if self.boom:
            raise ConnectionError("endpoint unreachable")
        if self.denied:
            raise _ClientError("AccessDenied")
        if Key not in self.objects:
            raise _NoSuchKey(Key)
        return {"Body": _Body(self.objects[Key])}


def _parquet(rows):
    import pyarrow as pa
    import pyarrow.parquet as pq
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pylist(rows), buf)
    return buf.getvalue()


def _smx_fixture(root):
    """aum + roster parquet bytes for one partition: 3 mapped models, 1 unmapped, a NaN and a null closing_equity."""
    d = dt.date
    names = [("R1", "Opal Dividend Income"), ("R2", "Pathfinder Focused Opportunities"),
             ("R3", "Opal Global All Equity Total Return"), ("R4", "Opal Short-Term")]
    roster = [{"rmid": r, "model_name": n, "value": 1.0} for r, n in names]
    nan = float("nan")
    aum = [{"rmid": "R1", "day": d(2026, 5, 14), "closing_equity": 6.004, "total_aum": 9.0},
           {"rmid": "R2", "day": d(2026, 5, 14), "closing_equity": 4.0, "total_aum": 9.0},
           {"rmid": "R3", "day": d(2026, 5, 14), "closing_equity": 1.0, "total_aum": 9.0},
           {"rmid": "R4", "day": d(2026, 5, 14), "closing_equity": 999.0, "total_aum": 9.0},
           {"rmid": "R1", "day": d(2026, 5, 15), "closing_equity": nan, "total_aum": 9.0},
           {"rmid": "R2", "day": d(2026, 5, 15), "closing_equity": 3.0, "total_aum": 9.0},
           {"rmid": "R1", "day": d(2026, 5, 16), "closing_equity": None, "total_aum": 9.0}]
    return _parquet(aum), _parquet(roster)


def _keys(root, day):
    from lib.opal_naming import legacy_address
    return [legacy_address(r, date=day).split("/", 3)[3] for r in (ROW_AUM, ROW_ROS)]


# ------------------------------------------------------------------ the grader and its fixtures
FIX_DATES = ["2026-05-14", "2026-05-15", "2026-05-18", "2026-05-19", "2026-09-29", "2026-09-30", "2026-10-01", "2026-10-02"]
FIX_G = {"dates": FIX_DATES,
         "opal_aggregate_aua": [100.0, 100.0, 100.0, None, 100.0, 100.0, None, 100.0],
         "non_model_aua": [60.0, 60.0, 50.0, None, 40.0, 40.0, None, 40.0],
         "tax_additive_aua": [None, None, None, None, None, 5.0, None, 5.0],
         "sma_additive_aua": [None, None, None, None, None, 2.0, None, 2.0],
         "by_model": {"opal_div_sma": {"model_value": [None, None, 6.0, None, 6.0, 6.0, None, 6.0]},
                      "opal_growth_sma": {"model_value": [None, None, 4.0, None, 4.0, 4.0, None, 4.0]}}}
FIX_SMX = {"2026-05-14": {"div": 6.0, "growth": 4.0, "gaetr": 1.0}, "2026-05-15": {"div": 7.0, "growth": 3.0}}
FIX_WANT = {"client_supervised_aua": [49.0, 50.0, 40.0, 40.0, 30.0, 30.0, 30.0, 30.0],
            "etf_strategies_aua": [10.0, 10.0, 10.0, 10.0, 10.0, 12.0, 12.0, 12.0],
            "alt_strategies_aua": [None, None, None, None, None, 5.0, 5.0, 5.0],
            "carried_dates": ["2026-05-19", "2026-10-01"]}


def _grade(out, want):
    return isinstance(out, dict) and all(out.get(k) == v for k, v in want.items())


def _mutant(g, smx):
    """The planted defect: client supervised is the non-model AUA unchanged (no carve-outs), nothing carried."""
    return {"client_supervised_aua": list(g["non_model_aua"]), "etf_strategies_aua": [0.0] * len(g["dates"]),
            "alt_strategies_aua": [None] * len(g["dates"]), "carried_dates": []}


# ------------------------------------------------------------------ PURE
def pure(root: str) -> int:
    arm = _Arms()
    try:
        gc = _load(root)
    except Exception as exc:                                   # noqa: BLE001
        print("  import FAIL: %s: %s" % (type(exc).__name__, str(exc)[:160]))
        print("CN-P-1 PURE: 0 of 7 arms")
        return 1
    reg = gc.registry
    fn = getattr(gc, "compute_trend_groups", None)
    app = getattr(gc, "apply_global_trend_groups", None)
    lod = getattr(gc, "load_smartx_sma_legs", None)

    arm("M0", _grade(copy.deepcopy(FIX_WANT), FIX_WANT) and not _grade(_mutant(FIX_G, FIX_SMX), FIX_WANT),
        "the grader accepts the expected arrays and rejects the planted mutant")

    arm("P0", hasattr(gc, "apply_sma_sleeve_overlay") and hasattr(gc, "guard_global_min_firms_fold")
        and reg.sma_basis_of("tax") == "additive" and reg.sma_basis_of("divz") == "carve_out",
        "module imports; overlay + fold entry points present; tax additive, divz carve_out")

    # P1
    ok, detail = False, "no compute_trend_groups"
    if fn is not None:
        try:
            out = fn(copy.deepcopy(FIX_G), copy.deepcopy(FIX_SMX))
            ok = _grade(out, FIX_WANT)
            detail = "client %s etf %s alt %s carried %s" % (out.get("client_supervised_aua"), out.get("etf_strategies_aua"),
                                                              out.get("alt_strategies_aua"), out.get("carried_dates"))
        except Exception as exc:                               # noqa: BLE001
            detail = "%s: %s" % (type(exc).__name__, str(exc)[:140])
    arm("P1", ok, detail)

    # P2
    ok, detail = False, "no compute_trend_groups"
    if fn is not None:
        try:
            a = fn({"dates": ["2026-06-01", "2026-06-02", "2026-06-03"], "opal_aggregate_aua": [None, 100.0, 100.0],
                    "non_model_aua": [None, 50.0, 50.0], "by_model": {}},
                   {"2026-06-02": {"div": 1.0}, "2026-06-03": {"div": 1.0}})
            # a: June dates are past the cut-off, so Global's own (empty) carve-outs apply; row 0 has no total and no prior value
            b = fn({"dates": ["2026-05-14", "2026-05-15", "2026-05-16"], "opal_aggregate_aua": [100.0, 100.0, 100.0],
                    "non_model_aua": [60.0, 60.0, 60.0], "by_model": {}}, {"2026-05-14": {"div": 6.0, "growth": 4.0}})
            c = fn({"dates": ["2026-05-14", "2026-05-15"], "opal_aggregate_aua": [100.0, 100.0],
                    "non_model_aua": [60.0, 60.0], "by_model": {}}, {})
            src = copy.deepcopy(FIX_G)
            fn(src, copy.deepcopy(FIX_SMX))
            ok = (a["client_supervised_aua"] == [None, 50.0, 50.0] and a["carried_dates"] == []
                  and b["client_supervised_aua"] == [50.0, 50.0, 50.0] and b["carried_dates"] == ["2026-05-15", "2026-05-16"]
                  and c["client_supervised_aua"] == [None, None] and c["carried_dates"] == []
                  and src == FIX_G)
            detail = "first-row-None %s | carried-with-prior %s %s | no-leg-no-prior %s %s | input untouched %s" % (
                a["client_supervised_aua"], b["client_supervised_aua"], b["carried_dates"], c["client_supervised_aua"],
                c["carried_dates"], src == FIX_G)
        except Exception as exc:                               # noqa: BLE001
            detail = "%s: %s" % (type(exc).__name__, str(exc)[:140])
    arm("P2", ok, detail)

    # P3
    ok, detail = False, "no apply_global_trend_groups"
    if app is not None and fn is not None:
        try:
            arts = {"global": copy.deepcopy(FIX_G), "49financial": {"dates": ["2026-05-14", "2026-05-15"], "x": 1},
                    "inflection": {"dates": ["2026-05-14", "2026-05-15"]}, "cottonwood": None}
            arts["global"]["meta"] = {"keep": 1}
            before = copy.deepcopy(arts)
            out = app(arts, copy.deepcopy(FIX_SMX), "2026-10-14")
            want = fn(copy.deepcopy(FIX_G), copy.deepcopy(FIX_SMX))
            added = {s: {k for k in d if k in GROUPS + ("carried_dates",)} for s, d in out.items() if d is not None}
            ok = (arts == before and out["cottonwood"] is None
                  and all(v == set(GROUPS) | {"carried_dates"} for v in added.values())
                  and all(out["49financial"][k] == [None, None] for k in GROUPS) and out["inflection"]["carried_dates"] == []
                  and all(out["global"][k] == want[k] for k in want)
                  and out["global"]["meta"].get("keep") == 1
                  and (out["global"]["meta"].get("trend_groups") or {}).get("smartx_partition") == "2026-10-14"
                  and out["49financial"]["x"] == 1)
            detail = "input untouched %s; keys on %d scopes; None scope stays None %s; meta.trend_groups %s" % (
                arts == before, len(added), out["cottonwood"] is None, (out["global"].get("meta") or {}).get("trend_groups"))
        except Exception as exc:                               # noqa: BLE001
            detail = "%s: %s" % (type(exc).__name__, str(exc)[:140])
    arm("P3", ok, detail)

    # P4
    ok, detail = False, "no load_smartx_sma_legs"
    if lod is not None:
        try:
            aum_b, ros_b = _smx_fixture(root)
            kt, k1 = _keys(root, TODAY), _keys(root, "2026-10-13")
            want = {"2026-05-14": {"div": 6.0, "growth": 4.0, "gaetr": 1.0}, "2026-05-15": {"growth": 3.0}}
            f1 = FakeS3({kt[0]: aum_b, kt[1]: ros_b, k1[0]: b"x", k1[1]: b"x"})
            r1 = lod(f1, TODAY)
            f2 = FakeS3({k1[0]: aum_b, k1[1]: ros_b})
            r2 = lod(f2, TODAY)
            f3 = FakeS3({})
            r3 = lod(f3, TODAY)
            e4 = e5 = ""
            try:
                lod(FakeS3({}, denied=True), TODAY)
            except RuntimeError as exc:
                e4 = str(exc)
            try:
                lod(FakeS3({}, boom=True), TODAY)
            except RuntimeError as exc:
                e5 = str(exc)
            ok = (r1 == (want, TODAY) and f1.gets == kt and r2 == (want, "2026-10-13") and f2.gets[-2:] == k1
                  and r3 == ({}, None) and e4.startswith("C2-SIBLING FAIL-LOUD:") and e5.startswith("C2-SIBLING FAIL-LOUD:"))
            detail = ("today's partition: %s, %d gets (builder keys %s) | one day back: %s | none: %s, %d gets | denied raises %s | "
                      "other failure raises %s") % (r1[1], len(f1.gets), f1.gets == kt, r2[1], r3, len(f3.gets),
                                                     e4.startswith("C2-SIBLING FAIL-LOUD:"), e5.startswith("C2-SIBLING FAIL-LOUD:"))
        except Exception as exc:                               # noqa: BLE001
            detail = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    arm("P4", ok, detail)

    # P5
    try:
        try:
            reg.resolve_any("muni")
            gone = False
        except reg.UnknownMemberError:
            gone = True
        alt = sorted(m.member_id for m in reg.members_for("SMA > ALT Strategies"))
        sma = sorted(r[0] for r in reg.SMA_MEMBERS)
        arm("P5", gone and alt == ["tax"] and sma == ["divz", "idvz", "pfde", "pfoe", "tax"],
            "resolve_any('muni') raises %s; SMA > ALT Strategies members %s; SMA members %s" % (gone, alt, sma))
    except Exception as exc:                                   # noqa: BLE001
        arm("P5", False, "%s: %s" % (type(exc).__name__, str(exc)[:140]))
    return arm.done("PURE")


# ------------------------------------------------------------------ SEAMS
TYPED_NEEDLES = ("smartx/", "fact_model", "silver/", "opal-data-assets", "date=", ".parquet")


def _typed_literals(src: str, func: str):
    """String constants inside `func` that look like a typed SMArtX s3 address (docstring excluded)."""
    tree = ast.parse(src)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func:
            doc = ast.get_docstring(node, clean=False)
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str) and sub.value != doc:
                    if any(n in sub.value for n in TYPED_NEEDLES):
                        out.append(sub.value)
    return out


def _call_lines(src: str, fname: str, within: str):
    tree = ast.parse(src)
    lines = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == within:
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call):
                    f = sub.func
                    nm = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
                    if nm == fname:
                        lines.append(sub.lineno)
    return sorted(lines)


def _pytest(root, rel):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "--color=no", "-p", "no:cacheprovider", rel], cwd=root,
                       capture_output=True, text=True, timeout=100)
    m = re.search(r"(\d+) passed", p.stdout)
    f = re.search(r"(\d+) failed", p.stdout)
    return p.returncode, int(m.group(1)) if m else 0, int(f.group(1)) if f else 0


def seams(root: str) -> int:
    arm = _Arms()
    with open(os.path.join(root, CONSOLIDATOR), encoding="utf-8") as fh:
        src = fh.read()
    tree = ast.parse(src)
    top = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}

    # S0 control
    mod_scope_heavy = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))
                       and any(a.name.split(".")[0] in ("pyarrow", "pandas") for a in
                               (n.names if isinstance(n, ast.Import) else [ast.alias(name=n.module or "")]))]
    extras = None
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "R2_RULED_EXTRAS" for t in n.targets):
            extras = [k.value for v in n.value.values if isinstance(v, ast.Dict) for k in v.keys]
    with open(os.path.join(root, BUILD_PACKAGE), encoding="utf-8") as fh:
        bp = fh.read()
    arm("S0", extras == ["inflection_non_model_aua"] and "lib/opal_naming.py" in bp and "infra/logic/registry/legacy_addresses.json" in bp
        and not mod_scope_heavy,
        "ruled extras %s; package ships opal_naming + legacy_addresses; module-scope pyarrow/pandas imports %d"
        % (extras, len(mod_scope_heavy)))

    need = ("compute_trend_groups", "load_smartx_sma_legs", "apply_global_trend_groups")
    arm("S1", all(n in top for n in need), "module-level functions present: %s" % {n: n in top for n in need})

    # S2
    has_fn = "load_smartx_sma_legs" in top
    typed = _typed_literals(src, "load_smartx_sma_legs") if has_fn else ["<no function>"]
    consts = {n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
    imp = [(a.name, a.asname) for n in tree.body if isinstance(n, ast.ImportFrom) and n.module == "lib.opal_naming" for a in n.names]
    alias = next((a or n for n, a in imp if n == "legacy_address"), None)
    calls = _call_lines(src, alias, "load_smartx_sma_legs") if (has_fn and alias) else []
    mutant_src = 'def load_smartx_sma_legs(s3, today):\n    key = "smartx/platform/silver/fact_model_aum_daily/date=%s/data.parquet" % today\n    return key\n'
    mutant_hit = _typed_literals(mutant_src, "load_smartx_sma_legs")
    arm("S2", has_fn and not typed and ROW_AUM in consts and ROW_ROS in consts and len(calls) >= 1 and len(mutant_hit) >= 1,
        "typed literals in the loader %s; row ids named %s/%s; builder calls %d; detector flags the planted literal %s"
        % (typed, ROW_AUM in consts, ROW_ROS in consts, len(calls), len(mutant_hit) >= 1))

    # S3
    g = _call_lines(src, "guard_global_min_firms_fold", "build_all")
    ld = _call_lines(src, "load_smartx_sma_legs", "build_all")
    a = _call_lines(src, "apply_global_trend_groups", "build_all")
    s = _call_lines(src, "_shape_timeseries", "build_all")
    arm("S3", bool(g and ld and a and s) and g[0] < ld[0] <= a[0] < s[0],
        "build_all call lines: fold %s, load %s, apply %s, first shape %s" % (g[:1], ld[:1], a[:1], s[:1]))

    # T1, T2
    try:
        rc, passed, failed = _pytest(root, TEST_NEW) if os.path.exists(os.path.join(root, TEST_NEW)) else (2, 0, 0)
        arm("T1", rc == 0 and passed >= 5, "%s: %d passed, %d failed (rc=%d; needs >= 5)" % (TEST_NEW, passed, failed, rc))
    except Exception as exc:                                   # noqa: BLE001
        arm("T1", False, "%s: %s" % (type(exc).__name__, str(exc)[:120]))
    try:
        rc, passed, failed = _pytest(root, TEST_OLD)
        arm("T2", rc == 0 and passed >= 1, "%s: %d passed, %d failed (rc=%d)" % (TEST_OLD, passed, failed, rc))
    except Exception as exc:                                   # noqa: BLE001
        arm("T2", False, "%s: %s" % (type(exc).__name__, str(exc)[:120]))
    return arm.done("SEAMS")


# ------------------------------------------------------------------ ORACLE
def _independent_legs(s3, root):
    """The SMArtX legs parsed here, independent of the module: {iso date: {role: closing_equity}}."""
    import pyarrow.parquet as pq
    k = _keys(root, TODAY)
    aum = pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=k[0])["Body"].read()), columns=["rmid", "day", "closing_equity"]).to_pylist()
    ros = pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=k[1])["Body"].read()), columns=["rmid", "model_name"]).to_pylist()
    names = {r["rmid"]: r["model_name"] for r in ros}
    role = {"Opal Dividend Income": "div", "Pathfinder Focused Opportunities": "growth",
            "Opal Global All Equity Total Return": "gaetr"}
    out = {}
    for r in aum:
        ro, v = role.get(names.get(r["rmid"])), r["closing_equity"]
        if ro is None or v is None or v != v:
            continue
        out.setdefault(str(r["day"])[:10], {})[ro] = round(float(v), 2)
    return out


def _period_end_diffs(g, groups):
    """max |diff| in $M of the 9 period-end rows against ORACLE, and the count within 0.05M."""
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
        import boto3
        s3 = boto3.client("s3", region_name="us-east-1")
        g = json.loads(s3.get_object(Bucket=BUCKET, Key=G_KEY)["Body"].read())
        f49 = json.loads(s3.get_object(Bucket=BUCKET, Key=F_KEY)["Body"].read())
        leg = _independent_legs(s3, root)
    except Exception as exc:                                   # noqa: BLE001
        print("  setup FAIL: %s: %s" % (type(exc).__name__, str(exc)[:200]))
        print("CN-P-1 ORACLE: 0 of 7 arms")
        return 1
    dates, tot = g["dates"], g["opal_aggregate_aua"]
    notot = [d for d, t in zip(dates, tot) if t is None]
    bm = g["by_model"]

    # O0 control
    worst, n_ov = 0.0, 0
    for i, d in enumerate(dates):
        if d >= CUT and d in leg:
            for role, key in (("div", "opal_div_sma"), ("growth", "opal_growth_sma")):
                gv = bm[key]["model_value"][i]
                if gv is not None and role in leg[d]:
                    worst = max(worst, abs(gv - leg[d][role]))
            n_ov += 1
    arm("O0", len(dates) == 496 and notot == NO_TOTAL and n_ov >= 100 and worst <= 0.01,
        "%d dates, %d with no total (the 9 named: %s); SMArtX vs Global carve-outs over %d overlap dates, max diff %.2f"
        % (len(dates), len(notot), notot == NO_TOTAL, n_ov, worst))

    fn = getattr(gc, "compute_trend_groups", None)
    lod = getattr(gc, "load_smartx_sma_legs", None)
    app = getattr(gc, "apply_global_trend_groups", None)

    # O1
    legs, part = None, None
    ok, detail = False, "no load_smartx_sma_legs"
    if lod is not None:
        try:
            legs, part = lod(s3, TODAY)
            need = [d for d, t in zip(dates, tot) if d < CUT and t is not None]
            miss = [d for d in need if d not in legs]
            bad = [d for d in need if d in legs and any(abs(legs[d].get(r, 0.0) - leg.get(d, {}).get(r, 0.0)) > 0.005
                                                         for r in ("div", "growth", "gaetr"))]
            ok = part is not None and not miss and not bad
            detail = "partition %s; %d pre-cut-off dated rows, %d missing, %d differ from the independent parse" % (
                part, len(need), len(miss), len(bad))
        except Exception as exc:                               # noqa: BLE001
            detail = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    arm("O1", ok, detail)

    out = None
    if fn is not None and legs is not None:
        try:
            out = fn(copy.deepcopy(g), legs)
        except Exception as exc:                               # noqa: BLE001
            print("  (compute raised %s: %s)" % (type(exc).__name__, str(exc)[:140]))

    # O2
    if out is None:
        arm("O2", False, "no compute output")
    else:
        worst, within = _period_end_diffs(g, out)
        arm("O2", within == len(ORACLE), "%d of %d period ends within 0.05M of the amended oracle; max diff %.2fM"
            % (within, len(ORACLE), worst))

    # O3
    if out is None:
        arm("O3", False, "no compute output")
    else:
        worst, n = 0.0, 0
        for i, d in enumerate(dates):
            if tot[i] is None:
                continue
            gaetr = (legs.get(d) or {}).get("gaetr", 0.0) if d < "2026-05-15" else 0.0
            s = (g["model_aua"][i] or 0.0) + sum(out[k][i] or 0.0 for k in GROUPS) + gaetr
            worst = max(worst, abs(s - tot[i]))
            n += 1
        arm("O3", n == 487 and worst <= 0.02, "%d dated rows (denominator), max |sum - total| = %.4f" % (n, worst))

    # O4
    if out is None:
        arm("O4", False, "no compute output")
    else:
        carried = out["carried_dates"]
        last_dated = {}
        prev = None
        for i, d in enumerate(dates):
            if tot[i] is not None:
                prev = i
            else:
                last_dated[d] = prev
        same = all(out[k][dates.index(d)] == out[k][last_dated[d]] for d in NO_TOTAL for k in GROUPS[:2])
        alt_none = all(out["alt_strategies_aua"][i] is None for i, d in enumerate(dates) if d < "2026-09-30")
        arm("O4", carried == NO_TOTAL and same and alt_none,
            "carried_dates == the 9 no-total dates %s; groups on them equal the previous dated row %s; ALT None before 2026-09-30 %s"
            % (carried == NO_TOTAL, same, alt_none))

    # O5
    ok, detail = False, "no apply_global_trend_groups"
    if app is not None and legs is not None:
        try:
            arts = {"global": copy.deepcopy(g), "49financial": copy.deepcopy(f49)}
            res = app(arts, legs, part)
            new = set(GROUPS) | {"carried_dates"}

            def _same(a, b):
                return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
            gd, fd = res["global"], res["49financial"]
            diffs = [k for k in g if k != "meta" and not _same(gd.get(k), g[k])]
            meta_diff = [k for k in set(g["meta"]) | set(gd["meta"]) if k != "trend_groups" and not _same(gd["meta"].get(k), g["meta"].get(k))]
            fdiffs = [k for k in f49 if not _same(fd.get(k), f49[k])]
            ok = (not diffs and not meta_diff and not fdiffs and new <= set(gd) and new <= set(fd)
                  and all(v is None for v in fd["client_supervised_aua"]))
            detail = "Global keys changed %s, meta keys changed %s, 49 Financial keys changed %s; new keys on both scopes %s" % (
                diffs, meta_diff, fdiffs, new <= set(gd) and new <= set(fd))
        except Exception as exc:                               # noqa: BLE001
            detail = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    arm("O5", ok, detail)

    # Om control: the O2 comparator on the planted mutant must find a difference
    mut = _mutant(g, {})
    mut["etf_strategies_aua"] = [0.0] * len(dates)
    worst, within = _period_end_diffs(g, mut)
    arm("Om", within < len(ORACLE) and worst > 0.05, "planted mutant: %d of %d period ends within 0.05M, max diff %.2fM (must flag)"
        % (within, len(ORACLE), worst))
    return arm.done("ORACLE")


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    fns = {"pure": pure, "seams": seams, "oracle": oracle}
    if mode not in fns:
        print("usage: r9_cn_p_1.py pure|seams|oracle")
        return 2
    return fns[mode](_root())


if __name__ == "__main__":
    sys.exit(main())
