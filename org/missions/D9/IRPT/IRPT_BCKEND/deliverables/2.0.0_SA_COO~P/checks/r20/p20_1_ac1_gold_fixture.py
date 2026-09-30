"""IB-pr-201 AC1 -- holdings_gold.calculate answers a 49F window from the holdings-basis gold (PRD v0.19 rulings 6, 10, 11).

Usage: python p20_1_ac1_gold_fixture.py <worktree root>
Arms, on in-memory gold partitions (irpt/49financial/gold/holdings_performance_daily/date=D/data.parquet):
 A. YTD 2026-01-01..2026-01-07 for the thread account answers prod(1 + daily_return over its OK in-window rows) - 1,
    provider OPAL_HOLDINGS, dates.actual_start 2026-01-02, a daily_cumulative_series ending at that value.
 B. Since inception (start 1970-01-01) starts at the account's FIRST landed day (2025-12-31) (ruling 6).
 C. An account the gold does not carry refuses as holdings_gold.HoldingsGoldRefused; a 3-year window refuses as
    holdings_gold.HoldingsWindowNotRuled (a subclass). Never a figure.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pkg import GoldS3, install  # noqa: E402

root, package = install(sys.argv[1] if len(sys.argv) > 1 else ".")
ok = True
try:
    import holdings_gold as hg
except Exception as exc:
    print("FAIL: holdings_gold does not import (%s)" % type(exc).__name__)
    print("P20-1-AC1 FAIL")
    sys.exit(1)
import tenants  # noqa: E402
from ids import opaque_account  # noqa: E402

PREFIX = "irpt/49financial/gold/holdings_performance_daily/"
T, OTHER = "0010498003", "0012347125"
DAYS = {
    "2025-12-31": [(T, 0.004, 100.0, "OK"), (OTHER, 0.001, 50.0, "OK")],
    "2026-01-02": [(T, 0.010, 101.0, "OK"), (OTHER, 0.002, 50.1, "OK")],
    "2026-01-05": [(T, -0.005, 100.5, "OK"), (OTHER, 0.001, 50.2, "OK")],
    "2026-01-06": [(T, 0.003, 100.8, "OK"), (OTHER, 0.000, 50.2, "OK")],
    "2026-01-07": [(T, 0.002, 101.0, "OK"), (OTHER, 0.001, 50.3, "OK")],
}


def scope(raw):
    acct = opaque_account(tenants._CANONICAL_49F, raw)
    return {"verified_request_firm_id": tenants._LEGACY_SHORT_ID["49F"], "permitted_account_set": [acct],
            "resolved_scope": {"scope_ids": [acct]}}


def calc(raw, start, end="2026-01-07"):
    return hg.calculate(scope(raw), start, end, hg.HoldingsGoldSource(GoldS3(PREFIX, DAYS), bucket="b", prefix=PREFIX))


def value(report):
    return report["returns"]["account_detail"][0]["value"]


try:
    rep = calc(T, "2026-01-01")["report"]
    want = (1.010 * 0.995 * 1.003 * 1.002) - 1.0
    ser = rep["returns"]["daily_cumulative_series"]
    last = ser[-1]["cumulative"]
    last = last.get("value") if isinstance(last, dict) else last
    good = (abs(value(rep) - want) < 1e-12 and rep["lineage"]["provider"] == "OPAL_HOLDINGS"
            and rep["dates"]["actual_start"] == "2026-01-02" and abs(float(last) - want) < 1e-12)
    print("%s A: YTD %.12f (want %.12f) provider %s start %s" % ("PASS" if good else "FAIL", value(rep), want,
          rep["lineage"].get("provider"), rep["dates"].get("actual_start")))
    ok = ok and good
except Exception as exc:
    print("FAIL A: %s" % type(exc).__name__)
    ok = False

try:
    rep = calc(T, "1970-01-01")["report"]
    good = rep["dates"]["actual_start"] == "2025-12-31" and math.isfinite(value(rep))
    print("%s B: SI actual_start %s" % ("PASS" if good else "FAIL", rep["dates"].get("actual_start")))
    ok = ok and good
except Exception as exc:
    print("FAIL B: SI refused as %s" % type(exc).__name__)
    ok = False

for label, raw, start, cls in (("C1 unknown account", "0099999999", "2026-01-01", "HoldingsGoldRefused"),
                               ("C2 3-year window", T, "2023-01-08", "HoldingsWindowNotRuled")):
    try:
        calc(raw, start)
        print("FAIL %s: answered a figure" % label)
        ok = False
    except Exception as exc:
        target = getattr(hg, cls, None)
        good = target is not None and isinstance(exc, target)
        print("%s %s: refused as %s" % ("PASS" if good else "FAIL", label, type(exc).__name__))
        ok = ok and good

if ok:
    print("P20-1-AC1 PASS")
else:
    print("P20-1-AC1 FAIL")
sys.exit(0 if ok else 1)
