#!/usr/bin/env python3
"""Build a REFERENCE TREE for the CN-p-1 issuer checks (the dry-run that proves the arms CAN pass).

  python make_reference_tree_p1.py <dest-dir> [--mutant NAME]

Copies, read-only from the repo at the current checkout, data/mdpf/scripts, data/mdpf/tests, lib/, the naming registry and the
gold package's build_package.py into <dest-dir>, applies the cell's change as the ISSUER'S REFERENCE (never a worker's code,
never committed to the repo), and drops a test file. Then:   R9_ROOT=<dest-dir> python r9_cn_p_1.py pure|seams|oracle

--mutant NAME applies the reference WITH ONE DEFECT so the issuer can show an arm fails on it (an arm that cannot fail is not
an arm):  typed-literal | no-gaetr | no-test-edit | keep-muni | no-allscope | mutates-input

Every patch asserts it applied exactly once; a drift in a target file fails loud instead of silently skipping.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

IMPORT_OLD = "from lib.opal_naming import address as taxsma_address  # noqa: E402 -- TX-a-2's own two\n"
IMPORT_NEW = ("from lib.opal_naming import legacy_address as smartx_legacy_address  # noqa: E402 -- MDPF_CANON CN-p-1: the two SMArtX\n"
              "                                                                      # read keys come from registry rows, never typed\n"
              + IMPORT_OLD)

BLOCK = '''# --------------------------------------------------------------------------
# MDPF_CANON CN-p-1 (PRD v2.19-v2.21, the Variant 1 Global AUA Trend): the Trend groups the portal draws, SERVED on the
# Global series so the page reads them and never recomposes them (FIELD-READ LAW).
#   client_supervised_aua  = non_model_aua - Dividend - Growth - Opal Global All Equity Total Return   (a difference)
#   etf_strategies_aua     = Dividend + Growth + sma_additive_aua (PFDE)
#   alt_strategies_aua     = tax_additive_aua   (Tax-Managed ONLY; Muni is a custom model, not an SMA)
# Dividend and Growth come from SMArtX `closing_equity` before TREND_SMARTX_UNTIL (the dollars sit inside 49F non_model_aua
# then) and from Global's own carve-outs from that date (SMArtX equals them to $0.00 on all overlap dates). A group with no
# value on a row takes its LAST KNOWN value (roll FORWARD only, never before the group's first value) and the row is named
# in `carried_dates`. Every other scope gains the same keys all-None / [] (the L-1 key-set identity has no ruled extra).
# --------------------------------------------------------------------------
TREND_GROUP_KEYS = ("client_supervised_aua", "etf_strategies_aua", "alt_strategies_aua")
TREND_CARRIED_KEY = "carried_dates"
TREND_SMARTX_UNTIL = "2026-05-18"
SMARTX_AUM_ROW = "smartx-platform-silver-fact-model-aum-daily"
SMARTX_ROSTER_ROW = "smartx-platform-silver-fact-model-allocation-roster"
SMARTX_ROLE_OF_MODEL = {"Opal Dividend Income": "div", "Pathfinder Focused Opportunities": "growth",
                        "Opal Global All Equity Total Return": "gaetr"}
SMARTX_LOOKBACK_DAYS = 10


def compute_trend_groups(g: dict, smartx: dict) -> dict:
    """The three Trend group series and carried_dates for one Global timeseries dict. `smartx` is {iso date: {"div": $,
    "growth": $, "gaetr": $}}. Reads only: `g` is never mutated. A row with no total (or no non_model_aua) has no value of its
    own; before TREND_SMARTX_UNTIL a row with no SMArtX leg has none either (absent is not zero). Then each group rolls
    forward from its last known value."""
    dates = list(g.get("dates") or [])
    n = len(dates)

    def _col(v):
        v = list(v or [])
        return v + [None] * (n - len(v))

    total, nm = _col(g.get("opal_aggregate_aua")), _col(g.get("non_model_aua"))
    tax, sma = _col(g.get("tax_additive_aua")), _col(g.get(SMA_ADDITIVE_KEY))
    bm = g.get("by_model") or {}
    div_g, growth_g = _col((bm.get("opal_div_sma") or {}).get("model_value")), _col((bm.get("opal_growth_sma") or {}).get("model_value"))
    raw = {k: [None] * n for k in TREND_GROUP_KEYS}
    for i, d in enumerate(dates):
        if total[i] is None or nm[i] is None:
            continue
        if d < TREND_SMARTX_UNTIL:
            leg = smartx.get(d)
            if leg is None:
                continue
            div, growth, gaetr = (leg.get(r) or 0.0 for r in ("div", "growth", "gaetr"))
        else:
            div, growth, gaetr = div_g[i] or 0.0, growth_g[i] or 0.0, 0.0
        raw["client_supervised_aua"][i] = round(nm[i] - div - growth - gaetr, 2)
        raw["etf_strategies_aua"][i] = round(div + growth + (sma[i] or 0.0), 2)
        raw["alt_strategies_aua"][i] = None if tax[i] is None else round(tax[i], 2)
    out: dict = {}
    carried: set = set()
    for k in TREND_GROUP_KEYS:
        last, col = None, []
        for i, d in enumerate(dates):
            v = raw[k][i]
            if v is not None:
                last = v
            elif last is not None:
                v = last
                carried.add(d)
            col.append(v)
        out[k] = col
    out[TREND_CARRIED_KEY] = sorted(carried)
    return out


def load_smartx_sma_legs(s3, today: str, lookback: int = SMARTX_LOOKBACK_DAYS) -> tuple:
    """Read ONE SMArtX partition (each carries the full history): the newest of `today` and the `lookback`-1 days before it
    that exists. Returns ({iso date: {"div"|"growth"|"gaetr": closing_equity}}, partition date). No partition exists -> ({}, None),
    a WARN (honest absent; the Trend groups before TREND_SMARTX_UNTIL then stay None). A denied or failed read is NEVER an
    absence: it raises RuntimeError whose message STARTS `C2-SIBLING FAIL-LOUD:`. Both keys come from the registry rows."""
    import io
    import pyarrow.parquet as pq   # noqa: PLC0415 -- the layer's pyarrow, as mdpf_gold_parquet imports it
    day0 = dt.date.fromisoformat(today)
    denied: list = []
    for k in range(lookback):
        d = (day0 - dt.timedelta(days=k)).isoformat()
        keys = [smartx_legacy_address(row, date=d).split("/", 3)[3] for row in (SMARTX_AUM_ROW, SMARTX_ROSTER_ROW)]
        try:
            bodies = [s3.get_object(Bucket=ASSETS_BUCKET, Key=key)["Body"].read() for key in keys]
        except s3.exceptions.NoSuchKey:
            continue
        except Exception as e:  # noqa: BLE001 -- deliberate breadth BECAUSE it re-raises
            code = ((getattr(e, "response", None) or {}).get("Error") or {}).get("Code")
            if code in ("AccessDenied", "403"):
                denied.append(d)
                continue
            raise RuntimeError(f"C2-SIBLING FAIL-LOUD: SMArtX partition read FAILED (NOT absent) for {keys[0]} "
                               f"({type(e).__name__}: {e})") from e
        names = {r["rmid"]: r["model_name"] for r in
                 pq.read_table(io.BytesIO(bodies[1]), columns=["rmid", "model_name"]).to_pylist()}
        legs: dict = {}
        for r in pq.read_table(io.BytesIO(bodies[0]), columns=["rmid", "day", "closing_equity"]).to_pylist():
            role, v = SMARTX_ROLE_OF_MODEL.get(names.get(r["rmid"])), r["closing_equity"]
            if role is None or v is None or v != v:
                continue
            legs.setdefault(str(r["day"])[:10], {})[role] = round(float(v), 2)
        return legs, d
    if denied:
        raise RuntimeError(f"C2-SIBLING FAIL-LOUD: SMArtX partition read DENIED on {denied} (NOT absent)")
    log(f"  WARN trend-groups: no SMArtX partition in the {lookback} days to {today} -> the Trend groups before "
        f"{TREND_SMARTX_UNTIL} stay honest-None")
    return {}, None


def apply_global_trend_groups(arts: dict, smartx: dict, smartx_partition: "str | None" = None) -> dict:
    """Every built scope gains the three group keys and carried_dates; Global's are computed (compute_trend_groups), every
    other scope's are all-None / []. Returns new dicts: the input `arts` is never mutated. Global also gains
    meta.trend_groups (the SMArtX partition read and the date the SMArtX legs end)."""
    out = {k: (dict(v) if v is not None else None) for k, v in arts.items()}
    for scope, doc in out.items():
        if doc is None:
            continue
        for k in TREND_GROUP_KEYS:
            doc[k] = [None] * len(doc.get("dates") or [])
        doc[TREND_CARRIED_KEY] = []
    g = out.get("global")
    if g is not None:
        g.update(compute_trend_groups(g, smartx))
        meta = dict(g.get("meta") or {})
        meta["trend_groups"] = {"smartx_partition": smartx_partition, "smartx_legs_until": TREND_SMARTX_UNTIL,
                                "smartx_dates": len(smartx)}
        g["meta"] = meta
    return out


'''

WIRE_OLD = ("    arts, fold_report = guard_global_min_firms_fold(arts, _isolated)   # CN-f-1: Global per-model lines shown only "
            "where >= 2 firms hold them\n")
WIRE_NEW = WIRE_OLD + (
    "    # MDPF_CANON CN-p-1: the Trend groups (client supervised / ETF / ALT) and carried_dates, after every fold that moves a Global figure.\n"
    "    _smx = _isolated(\"global\", lambda: load_smartx_sma_legs(s3, process_start.date().isoformat())) or ({}, None)\n"
    "    arts = apply_global_trend_groups(arts, _smx[0], _smx[1])\n")

ANCHOR = "def write_taxsma_category_gold(s3, scope: str, knowledge_date: str, category_doc: dict,\n"

MUNI_OLD = '''    # muni: Andrew-direct -- "Muni to my knowledge does not exist yet". It has no
    # accounts, so the master test returns nothing and this basis is UNVERIFIED. It is
    # declared anyway, because the alternative is a default, and it is declared
    # CARVE_OUT as the SAFE direction: a wrong CARVE_OUT understates Client (visible in
    # a number Andrew already watches); a wrong ADDITIVE inflates the FIRM TOTAL by
    # double-counting (invisible). ''' + chr(0x26a0) + ''' 3.0.0_SA_CVO~Z 15942 names muni the member most
    # likely to be given a basis by omission -- it is not omitted, it is UNVERIFIED and
    # says so here. Verify before its first dollar.
    ("muni", "muni", "Muni SMA", True, "ALT Strategies", SMA_BASIS_CARVE_OUT),
'''
MUNI_NEW = ('    # muni: removed (Andrew-direct 2026-10-14: "no muni in SMAs, Muni is no longer SMA" / "muni is just a custom model").\n')

TEST_OLD = '    assert set(rows) >= {"divz", "pfoe", "muni", "tax", "idvz", "pfde"}\n'
TEST_NEW = '    assert set(rows) >= {"divz", "pfoe", "tax", "idvz", "pfde"} and "muni" not in rows\n'

REF_TEST = '''"""CN-p-1 REFERENCE test (issuer dry-run only; the worker writes its own)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
for sub in ("scripts/silver", "scripts/gold"):
    sys.path.insert(0, os.path.join(ROOT, "data", "mdpf", sub))
sys.path.insert(0, ROOT)
import mdpf_gold_consolidator as gc  # noqa: E402

G = {"dates": ["2026-05-14", "2026-05-18", "2026-05-19"], "opal_aggregate_aua": [100.0, 100.0, None],
     "non_model_aua": [60.0, 50.0, None], "tax_additive_aua": [None, None, None], "sma_additive_aua": [None, None, None],
     "by_model": {"opal_div_sma": {"model_value": [None, 6.0, None]}, "opal_growth_sma": {"model_value": [None, 4.0, None]}}}
SMX = {"2026-05-14": {"div": 6.0, "growth": 4.0, "gaetr": 0.0}}


def test_difference_and_roll_forward():
    out = gc.compute_trend_groups(G, SMX)
    assert out["client_supervised_aua"] == [50.0, 40.0, 40.0] and out["etf_strategies_aua"] == [10.0, 10.0, 10.0]
    assert out["carried_dates"] == ["2026-05-19"]


def test_no_smartx_leg_is_none_not_zero():
    out = gc.compute_trend_groups(G, {})
    assert out["client_supervised_aua"][0] is None and out["carried_dates"] == ["2026-05-19"]


def test_alt_never_back_filled():
    out = gc.compute_trend_groups(G, SMX)
    assert out["alt_strategies_aua"] == [None, None, None]


def test_apply_all_scope_and_pure():
    arts = {"global": dict(G), "49financial": {"dates": ["2026-05-14"]}, "cottonwood": None}
    out = gc.apply_global_trend_groups(arts, SMX, "2026-10-14")
    assert out["49financial"]["carried_dates"] == [] and out["49financial"]["etf_strategies_aua"] == [None]
    assert "etf_strategies_aua" not in arts["global"] and out["cottonwood"] is None


def test_registry_muni_gone():
    assert "muni" not in {r[0] for r in gc.registry.SMA_MEMBERS}
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
    g = os.path.join(dest, "data", "mdpf", "scripts", "gold")
    con = os.path.join(g, "mdpf_gold_consolidator.py")
    block = BLOCK
    if mutant == "typed-literal":
        block = block.replace('keys = [smartx_legacy_address(row, date=d).split("/", 3)[3] for row in (SMARTX_AUM_ROW, SMARTX_ROSTER_ROW)]',
                              'keys = ["smartx/platform/silver/fact_model_aum_daily/date=%s/data.parquet" % d, '
                              '"smartx/platform/silver/fact_model_allocation_roster/date=%s/data.parquet" % d]')
    if mutant == "no-gaetr":
        block = block.replace("round(nm[i] - div - growth - gaetr, 2)", "round(nm[i] - div - growth, 2)")
    if mutant == "no-allscope":
        block = block.replace("    for scope, doc in out.items():\n        if doc is None:\n            continue\n        for k in TREND_GROUP_KEYS:",
                              "    for scope, doc in out.items():\n        if doc is None or scope != \"global\":\n            continue\n        for k in TREND_GROUP_KEYS:")
    if mutant == "mutates-input":
        block = block.replace("    out = {k: (dict(v) if v is not None else None) for k, v in arts.items()}\n    for scope, doc in out.items():\n        if doc is None:\n            continue\n        for k in TREND_GROUP_KEYS:",
                              "    out = arts\n    for scope, doc in out.items():\n        if doc is None:\n            continue\n        for k in TREND_GROUP_KEYS:")
    _sub(con, IMPORT_OLD, IMPORT_NEW)
    _sub(con, ANCHOR, block + ANCHOR)
    _sub(con, WIRE_OLD, WIRE_NEW)
    if mutant != "keep-muni":
        _sub(os.path.join(g, "mdpf_category_registry.py"), MUNI_OLD, MUNI_NEW)
    if mutant not in ("no-test-edit", "keep-muni"):
        _sub(os.path.join(dest, "data", "mdpf", "tests", "stratid", "test_stratid_round2_inside_model.py"), TEST_OLD, TEST_NEW)
    td = os.path.join(dest, "data", "mdpf", "tests", "canon")
    os.makedirs(td, exist_ok=True)
    with open(os.path.join(td, "test_global_trend_groups.py"), "w", encoding="utf-8") as fh:
        fh.write(REF_TEST)
    print("reference tree at", dest, "(mutant=%s)" % mutant)
    return 0


if __name__ == "__main__":
    sys.exit(main())
