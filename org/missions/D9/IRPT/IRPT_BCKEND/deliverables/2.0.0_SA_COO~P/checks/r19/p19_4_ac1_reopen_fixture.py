"""IB-pr-194 AC1 -- a 49F report retained BEFORE the NEW-01 guard is refused by name at reopen, never re-served.

Usage: python p19_4_ac1_reopen_fixture.py <worktree root>

The retained store is the second reader of the served figure (4.0.0_SA_CRO D1 RESULT @5f82151a2e): the page reopens
the accepted report and never re-runs f49_engine.calculate. This check writes a report through the PRE-guard engine
(f49_engine.py as served before hcZpXDDo, read from git at 8d7a8b10fe) exactly as the live store holds one, then
reopens it with the current code.

Arm A: the NEW-01 shape, retained pre-guard (series reaches -1.0), reopens as f49_engine.EngineReturnImplausible.
Arm B (control): a clean account retained the same way reopens with the SAME report, and no second engine read.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _engine_path import install  # noqa: E402

root, package = install(sys.argv[1] if len(sys.argv) > 1 else ".")
for p in (package / "tests", package.parent / "reports", package.parent / "reports" / "tests"):
    sys.path.insert(0, str(p))

import pytest  # noqa: E402

TEST = r'''
import importlib, subprocess, sys, types
import pytest
trp = importlib.import_module("test_retained_performance")
wired, case, retention_world = trp.wired, trp.case, trp.retention_world
engine_tests = importlib.import_module("test_f49_engine")
retained = importlib.import_module("retained")
f49 = importlib.import_module("f49_engine")
tenants = importlib.import_module("tenants")

BAD, GOOD = "0049615236", "0010498003"
DAYS = {
    "2025-12-31": [(BAD, None, None, None, None), (GOOD, 0.001, 99.0, 100.0, 0.0)],
    "2026-01-02": [(BAD, 0.0, 13360.59, 13360.59, 0.0), (GOOD, 0.010, 100.0, 101.0, 0.0)],
    "2026-01-05": [(BAD, -1.0, 13360.59, 0.0, 0.0), (GOOD, 0.001, 101.0, 101.1, 0.0)],
    "2026-01-06": [(BAD, None, None, None, None), (GOOD, -0.005, 101.1, 100.6, 0.0)],
    "2026-01-07": [(BAD, 0.01, 100000.0, 101000.0, 0.0), (GOOD, 0.002, 100.6, 100.8, 0.0)],
}

def preguard_engine():
    src = subprocess.run(["git", "-C", ROOT, "show", "8d7a8b10fe:infra/aws/lambda/investor-reporting/performance/f49_engine.py"],
                         capture_output=True, check=True).stdout.decode("utf-8")
    mod = types.ModuleType("f49_engine_preguard")
    exec(compile(src, "f49_engine_preguard.py", "exec"), mod.__dict__)
    return mod

def retain_then_reopen(wired, raw):
    w = wired.w
    source = f49.EngineSource(engine_tests.FakeS3(DAYS), bucket=engine_tests.BUCKET, root=engine_tests.ROOT_PREFIX, max_workers=2)
    w.service.engine_source = source
    account = engine_tests.opaque_account(tenants._CANONICAL_49F, raw)
    w.principal = {"firm_id": tenants._CANONICAL_49F, "principal_id": "test-viewer"}
    w.owner = {**w.principal, "account_ids": [account]}
    scope = engine_tests._scope(account)
    current = retained.f49_engine
    retained.f49_engine = preguard_engine()
    try:
        first = w.service.compute(scope, "2026-01-01", "2026-01-07", principal=w.principal, owner=w.owner, authorize=w.policy.authorize)
    finally:
        retained.f49_engine = current
    reads = len(source.s3.gets)
    return first, (lambda: w.service.compute(scope, "2026-01-01", "2026-01-07", principal=w.principal, owner=w.owner, authorize=w.policy.authorize)), source, reads

def test_arm_a_preguard_retained_new01_refuses_at_reopen(wired):
    first, again, _, _ = retain_then_reopen(wired, BAD)
    assert min(p["cumulative"] if not isinstance(p["cumulative"], dict) else p["cumulative"]["value"]
               for p in first["report"]["returns"]["daily_cumulative_series"]) <= -1.0
    with pytest.raises(f49.EngineReturnImplausible):
        again()

def test_arm_b_clean_retained_report_reopens_unchanged(wired):
    first, again, source, reads = retain_then_reopen(wired, GOOD)
    assert again() == first and len(source.s3.gets) == reads
'''


def main():
    tmp = Path(__file__).resolve().parent / "_p19_4_ac1_test.py"
    tmp.write_text("ROOT = %r\n" % str(root) + TEST, encoding="utf-8")
    try:
        rc = pytest.main(["-q", "-p", "no:cacheprovider", str(tmp)])
    finally:
        tmp.unlink()
    if rc == 0:
        print("P19-4-AC1 PASS")
    else:
        print("P19-4-AC1 FAIL")
    sys.exit(0 if rc == 0 else 1)


main()
