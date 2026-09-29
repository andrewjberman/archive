"""Round 22 AC1 (IB-pr-221) -- holdings_gold.calculate answers an INFLECTION window from its holdings gold, the same
contract as 49F (PRD v0.19 rulings 10-12; ruling 11's order: 49F, then Inflection).

Usage: python p22_1_ac1_inf_gold_fixture.py <worktree root>
On in-memory gold (irpt/inflection/gold/holdings_performance_daily/date=D/data.parquet):
 A. INF YTD 2026-01-01..2026-01-07 for raw account '998' answers prod(1 + r over its OK in-window rows) - 1, provider
    OPAL_HOLDINGS, lineage.tenant_firm_id the Inflection firm id.
 B. The same call with a 49F scope over 49F gold still answers (the 49F path is not broken).
 C. An INF account the gold does not carry refuses as HoldingsGoldRefused. Never a figure.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pkg import GoldS3, install  # noqa: E402

root, package = install(sys.argv[1] if len(sys.argv) > 1 else ".")
import holdings_gold as hg  # noqa: E402
import tenants  # noqa: E402
from ids import opaque_account  # noqa: E402

INF_PREFIX, F49_PREFIX = "irpt/inflection/gold/holdings_performance_daily/", "irpt/49financial/gold/holdings_performance_daily/"
def DAYS(k):
    return {"2025-12-31": [(k, 0.004, 100.0, "OK")], "2026-01-02": [(k, 0.010, 101.0, "OK")],
            "2026-01-05": [(k, -0.005, 100.5, "OK")], "2026-01-06": [(k, 0.003, 100.8, "OK")],
            "2026-01-07": [(k, 0.002, 101.0, "OK")]}
WANT = (1.010 * 0.995 * 1.003 * 1.002) - 1.0


def scope(canonical_firm, short, raw):
    acct = opaque_account(canonical_firm, raw)
    return {"verified_request_firm_id": tenants._LEGACY_SHORT_ID[short], "permitted_account_set": [acct],
            "resolved_scope": {"scope_ids": [acct]}}


def value(rep):
    return rep["returns"]["account_detail"][0]["value"]


ok = True
try:
    rep = hg.calculate(scope(tenants._CANONICAL_INF, "INF", "998"), "2026-01-01", "2026-01-07",
                       hg.HoldingsGoldSource(GoldS3(INF_PREFIX, DAYS("998")), bucket="b", prefix=INF_PREFIX))["report"]
    a = abs(value(rep) - WANT) < 1e-12 and rep["lineage"]["provider"] == "OPAL_HOLDINGS"
    print("arm A (INF YTD): value %.12f want %.12f provider %s -> %s" % (value(rep), WANT, rep["lineage"]["provider"], a))
except Exception as exc:
    print("arm A (INF YTD): %s: %s" % (type(exc).__name__, str(exc)[:120]))
    a = False
try:
    rep = hg.calculate(scope(tenants._CANONICAL_49F, "49F", "0010498003"), "2026-01-01", "2026-01-07",
                       hg.HoldingsGoldSource(GoldS3(F49_PREFIX, DAYS("0010498003")), bucket="b", prefix=F49_PREFIX))["report"]
    b = abs(value(rep) - WANT) < 1e-12
    print("arm B (49F unchanged): %s" % b)
except Exception as exc:
    print("arm B (49F unchanged): %s: %s" % (type(exc).__name__, str(exc)[:120]))
    b = False
try:
    hg.calculate(scope(tenants._CANONICAL_INF, "INF", "77777"), "2026-01-01", "2026-01-07",
                 hg.HoldingsGoldSource(GoldS3(INF_PREFIX, DAYS("998")), bucket="b", prefix=INF_PREFIX))
    c = False
    print("arm C: served a figure for an uncovered account")
except hg.HoldingsGoldRefused as exc:
    c = True
    print("arm C: refused %s" % type(exc).__name__)
ok = a and b and c
print("P22-1-AC1 PASS" if ok else "P22-1-AC1 FAIL")
sys.exit(0 if ok else 1)
