"""Round 21 AC1 (IB-pr-214) -- PRD v0.20 ruling 16: the fresh path refuses any series point at or below -1, as the reopen
path does, so the two readers of a 49F figure agree (4.0.0_SA_CRO half @eca8083ad2 section 6 item 3).

Usage: python p21_4_ac1_fresh_path_refuses_implausible.py <worktree root>
On in-memory gold, through the worktree's RetainedPerformance(holdings_source=...).compute (the served fresh path):
Arm A: an OK day with daily_return -1.2 in the window -> a NAMED refusal (retained.implausible_engine_series's shape,
       raised as f49_engine.EngineReturnImplausible), never a figure.
Arm B (control): the same day carried as status NOT_COMPUTABLE -> an OPAL_HOLDINGS figure over the other days.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pkg import install  # noqa: E402

root, package = install(sys.argv[1] if len(sys.argv) > 1 else ".")
import pytest  # noqa: E402

TEST = r'''
import importlib
from _pkg import GoldS3
trp = importlib.import_module("test_retained_performance")
wired, case, retention_world = trp.wired, trp.case, trp.retention_world
engine_tests = importlib.import_module("test_f49_engine")
retained = importlib.import_module("retained")
tenants = importlib.import_module("tenants")
f49 = importlib.import_module("f49_engine")
hg = importlib.import_module("holdings_gold")
PREFIX = "irpt/49financial/gold/holdings_performance_daily/"
RAW = engine_tests.RAW

def gold(status):
    return {d: [(RAW, r, 100.0, s)] for d, r, s in (("2025-12-31", 0.001, "OK"), ("2026-01-02", 0.02, "OK"),
            ("2026-01-05", -1.2, status), ("2026-01-06", 0.005, "OK"))}

def svc(w, days):
    common = dict(table=w.table, s3=w.s3, reporting_policy=w.policy.reporting_policy,
                  reporting_destination=w.service.destination, load_mapping=w.service.load_mapping,
                  transport_factory=w.service.transport_factory, clock=lambda: w.state.now)
    return retained.RetainedPerformance(holdings_source=hg.HoldingsGoldSource(GoldS3(PREFIX, days), bucket="b", prefix=PREFIX), **common)

def setup(w):
    w.principal = {"firm_id": tenants._CANONICAL_49F, "principal_id": "test-viewer"}
    w.owner = {**w.principal, "account_ids": [engine_tests.ACCOUNT]}

def test_arm_a_ok_day_below_minus_one_refuses(wired):
    w = wired.w; setup(w)
    try:
        out = svc(w, gold("OK")).compute(engine_tests._scope(), "2026-01-01", "2026-01-06", principal=w.principal, owner=w.owner, authorize=w.policy.authorize)
    except f49.EngineReturnImplausible:
        return
    raise AssertionError("served a figure: %r" % out["report"]["returns"]["account_detail"][0].get("value"))

def test_arm_b_not_computable_day_is_skipped(wired):
    w = wired.w; setup(w)
    out = svc(w, gold("NOT_COMPUTABLE")).compute(engine_tests._scope(), "2026-01-01", "2026-01-06", principal=w.principal, owner=w.owner, authorize=w.policy.authorize)
    assert out["report"]["lineage"]["provider"] == "OPAL_HOLDINGS"
    assert abs(out["report"]["returns"]["account_detail"][0]["value"] - (1.02 * 1.005 - 1.0)) < 1e-12
'''


def main():
    tmp = Path(__file__).resolve().parent / "_p21_4_ac1_test.py"
    tmp.write_text(TEST, encoding="utf-8")
    try:
        rc = pytest.main(["-q", "-p", "no:cacheprovider", str(tmp)])
    finally:
        tmp.unlink()
    print("P21-4-AC1 PASS" if rc == 0 else "P21-4-AC1 FAIL")
    sys.exit(0 if rc == 0 else 1)


main()
