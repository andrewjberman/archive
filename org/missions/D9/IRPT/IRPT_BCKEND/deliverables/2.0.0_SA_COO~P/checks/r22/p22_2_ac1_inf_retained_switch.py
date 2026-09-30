"""Round 22 AC1 (IB-pr-222) -- the Inflection switch reaches the RETAINED reader too (1.0.0_SA_CTO round-19 analysis
section 2: an order that changes a served figure names every reader). PRD v0.19 ruling 12: the Orion read retires
for INF in the same act; a pre-switch INF pointer is never reopened.

Usage: python p22_2_ac1_inf_retained_switch.py <worktree root>
Through the worktree's retained.RetainedPerformance(holdings_sources={<INF canonical firm id>: HoldingsGoldSource},
**common).compute for an INF owner on raw account '998':
 Arm A: a pointer planted at the PRE-switch accepted key (no basis) naming a report that does not exist is never
        consulted: the answer is OPAL_HOLDINGS at the gold chain.
 Arm B: asking again reopens that answer unchanged, with no second gold read.
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
retained = importlib.import_module("retained")
repository = importlib.import_module("repository")
tenants = importlib.import_module("tenants")
hg = importlib.import_module("holdings_gold")
from ids import opaque_account
PREFIX = "irpt/inflection/gold/holdings_performance_daily/"
RAW = "998"
GOLD = {d: [(RAW, r, 100.0, "OK")] for d, r in (("2025-12-31", 0.001), ("2026-01-02", 0.02), ("2026-01-05", -0.01), ("2026-01-06", 0.005))}
WANT = (1.02 * 0.99 * 1.005) - 1.0

def test_inf_switch_reaches_the_retained_reader(wired):
    w = wired.w
    acct = opaque_account(tenants._CANONICAL_INF, RAW)
    w.principal = {"firm_id": tenants._CANONICAL_INF, "principal_id": "test-viewer"}
    w.owner = {**w.principal, "account_ids": [acct]}
    scope = {"verified_request_firm_id": tenants._LEGACY_SHORT_ID["INF"], "permitted_account_set": [acct],
             "resolved_scope": {"scope_ids": [acct]}}
    start, end = "2026-01-01", "2026-01-06"
    old_key = {"firm_id": tenants._CANONICAL_INF, "account_ids": [acct], "start": start, "end": end}
    repository.DynamoReportIndex(w.table).publish({"schema_version": "irpt-performance-accepted-v2",
        "tenant": tenants._CANONICAL_INF, "request_revision": "PERFORMANCE_ACCEPTED#" + repository.digest(old_key),
        "accepted_key": old_key, "ref": {"report_id": "RPT-does-not-exist", "revision": "r0", "report_kind": "PERFORMANCE"}})
    common = dict(table=w.table, s3=w.s3, reporting_policy=w.policy.reporting_policy,
                  reporting_destination=w.service.destination, load_mapping=w.service.load_mapping,
                  transport_factory=w.service.transport_factory, clock=lambda: w.state.now)
    gold_s3 = GoldS3(PREFIX, GOLD)
    svc = retained.RetainedPerformance(holdings_sources={tenants._CANONICAL_INF: hg.HoldingsGoldSource(gold_s3, bucket="b", prefix=PREFIX)}, **common)
    first = svc.compute(scope, start, end, principal=w.principal, owner=w.owner, authorize=w.policy.authorize)
    assert first["report"]["lineage"]["provider"] == "OPAL_HOLDINGS"
    assert abs(first["report"]["returns"]["account_detail"][0]["value"] - WANT) < 1e-12
    reads = len(gold_s3.gets)
    again = svc.compute(scope, start, end, principal=w.principal, owner=w.owner, authorize=w.policy.authorize)
    assert again == first and len(gold_s3.gets) == reads
'''


def main():
    tmp = Path(__file__).resolve().parent / "_p22_2_ac1_test.py"
    tmp.write_text(TEST, encoding="utf-8")
    try:
        rc = pytest.main(["-q", "-p", "no:cacheprovider", str(tmp)])
    finally:
        tmp.unlink()
    print("P22-2-AC1 PASS" if rc == 0 else "P22-2-AC1 FAIL")
    sys.exit(0 if rc == 0 else 1)


main()
