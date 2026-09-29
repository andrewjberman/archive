"""IB-pr-202 AC1 -- after the switch, a 49F report retained from the old ENGINE recomputes from the holdings gold; it is
never reopened (PRD v0.19 rulings 10 and 12; the NEW-01 lesson: the page reads retained reports, so a switch that
leaves them reopening changes nothing on the page).

Usage: python p20_2_ac1_retained_recompute.py <worktree root>
The check persists a 49F report through the PRE-switch retained.py (read from git at ae8da14d12, with the engine port
over in-memory twr_daily), then asks the worktree's RetainedPerformance(holdings_source=...) for the SAME firm, account
and window on the same table and store.
Arm A: the answer's provider is OPAL_HOLDINGS and its value is the gold chain -- the engine report is not reopened.
Arm B: asking again reopens the holdings report unchanged, with no second gold read.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pkg import install  # noqa: E402

root, package = install(sys.argv[1] if len(sys.argv) > 1 else ".")
import pytest  # noqa: E402

TEST = r'''
import importlib, subprocess, types
from _pkg import GoldS3
trp = importlib.import_module("test_retained_performance")
wired, case, retention_world = trp.wired, trp.case, trp.retention_world
engine_tests = importlib.import_module("test_f49_engine")
retained = importlib.import_module("retained")
tenants = importlib.import_module("tenants")
PREFIX = "irpt/49financial/gold/holdings_performance_daily/"
RAW = engine_tests.RAW
GOLD = {d: [(RAW, r, 100.0, "OK")] for d, r in
        (("2025-12-31", 0.001), ("2026-01-02", 0.02), ("2026-01-05", -0.01), ("2026-01-06", 0.005))}
WANT = (1.02 * 0.99 * 1.005) - 1.0

def base_retained():
    src = subprocess.run(["git", "-C", ROOT, "show", "ae8da14d12:infra/aws/lambda/investor-reporting/performance/retained.py"],
                         capture_output=True, check=True).stdout.decode("utf-8")
    mod = types.ModuleType("retained_preswitch")
    exec(compile(src, "retained_preswitch.py", "exec"), mod.__dict__)
    return mod

def test_engine_report_recomputes_from_the_gold_and_then_reopens(wired):
    w = wired.w
    w.principal = {"firm_id": tenants._CANONICAL_49F, "principal_id": "test-viewer"}
    w.owner = {**w.principal, "account_ids": [engine_tests.ACCOUNT]}
    scope = engine_tests._scope()
    common = dict(table=w.table, s3=w.s3, reporting_policy=w.policy.reporting_policy,
                  reporting_destination=w.service.destination, load_mapping=w.service.load_mapping,
                  transport_factory=w.service.transport_factory, clock=lambda: w.state.now)
    old = base_retained().RetainedPerformance(engine_source=engine_tests._source(), **common)
    first = old.compute(scope, "2026-01-01", "2026-01-06", principal=w.principal, owner=w.owner, authorize=w.policy.authorize)
    assert first["report"]["lineage"]["provider"] == "OPAL_ENGINE"
    gold_s3 = GoldS3(PREFIX, GOLD)
    new = retained.RetainedPerformance(holdings_source=importlib.import_module("holdings_gold").HoldingsGoldSource(gold_s3, bucket="b", prefix=PREFIX), **common)
    after = new.compute(scope, "2026-01-01", "2026-01-06", principal=w.principal, owner=w.owner, authorize=w.policy.authorize)
    assert after["report"]["lineage"]["provider"] == "OPAL_HOLDINGS"
    assert abs(after["report"]["returns"]["account_detail"][0]["value"] - WANT) < 1e-12
    reads = len(gold_s3.gets)
    again = new.compute(scope, "2026-01-01", "2026-01-06", principal=w.principal, owner=w.owner, authorize=w.policy.authorize)
    assert again == after and len(gold_s3.gets) == reads
'''


def main():
    tmp = Path(__file__).resolve().parent / "_p20_2_ac1_test.py"
    tmp.write_text("ROOT = %r\n" % str(root) + TEST, encoding="utf-8")
    try:
        rc = pytest.main(["-q", "-p", "no:cacheprovider", str(tmp)])
    finally:
        tmp.unlink()
    if rc == 0:
        print("P20-2-AC1 PASS")
    else:
        print("P20-2-AC1 FAIL")
    sys.exit(0 if rc == 0 else 1)


main()
