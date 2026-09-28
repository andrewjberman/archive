"""IB-pr-191 AC1 -- a linked engine day with r_net <= -1 is a NAMED refusal, never a served figure (NEW-01, row S177).

Usage: python p19_1_ac1_implausible_fixture.py <worktree root>
Prints PASS or FAIL lines; exit 0 only when every arm passes.

Arm A (the built behaviour): the measured NEW-01 shape -- one OK day at bmv = emv = 13,360.59, the next OK day
emv 0.0 with cf_net 0.0 (r_net -1.0), zero-base days after, then a re-funded OK day -- must raise
f49_engine.EngineReturnImplausible, a subclass of f49_engine.EnginePerformanceRefused.
Arm B (the control): a sibling account on the same partitions with ordinary returns still computes a finite value
above -1.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _engine_path import install  # noqa: E402

root, package = install(sys.argv[1] if len(sys.argv) > 1 else ".")
sys.path.insert(0, str(package / "tests"))
import test_f49_engine as t  # noqa: E402  (FakeS3, _scope, ids -- the suite's own fixtures)

f49 = t.f49_engine
BAD, GOOD = "0049615236", "0010498003"
DAYS = {
    "2025-12-31": [(BAD, None, None, None, None), (GOOD, 0.001, 99.0, 100.0, 0.0)],
    "2026-01-02": [(BAD, 0.0, 13360.59, 13360.59, 0.0), (GOOD, 0.010, 100.0, 101.0, 0.0)],
    "2026-01-05": [(BAD, -1.0, 13360.59, 0.0, 0.0), (GOOD, 0.001, 101.0, 101.1, 0.0)],
    "2026-01-06": [(BAD, None, None, None, None), (GOOD, -0.005, 101.1, 100.6, 0.0)],
    "2026-01-07": [(BAD, 0.01, 100000.0, 101000.0, 0.0), (GOOD, 0.002, 100.6, 100.8, 0.0)],
}
START, END = "2026-01-01", "2026-01-07"
ok = True


def source():
    return f49.EngineSource(t.FakeS3(DAYS), bucket=t.BUCKET, root=t.ROOT_PREFIX, max_workers=2)


def scope(raw):
    return t._scope(t.opaque_account(t.tenants._CANONICAL_49F, raw))


cls = getattr(f49, "EngineReturnImplausible", None)
if cls is None or not issubclass(cls, f49.EnginePerformanceRefused):
    print("FAIL A: f49_engine.EngineReturnImplausible (subclass of EnginePerformanceRefused) is not defined")
    ok = False
else:
    try:
        out = f49.calculate(scope(BAD), START, END, source())
        value = out["report"]["returns"]["account_detail"][0]["value"]
        print("FAIL A: the NEW-01 shape was SERVED, value %r" % value)
        ok = False
    except cls as exc:
        print("PASS A: the NEW-01 shape refuses as %s" % type(exc).__name__)
    except Exception as exc:  # a refusal of another class is not the named one
        print("FAIL A: refused as %s, not EngineReturnImplausible" % type(exc).__name__)
        ok = False

try:
    out = f49.calculate(scope(GOOD), START, END, source())
    value = out["report"]["returns"]["account_detail"][0]["value"]
    if math.isfinite(value) and value > -1.0:
        print("PASS B: the control account computes %.6f" % value)
    else:
        print("FAIL B: the control account computes %r" % value)
        ok = False
except Exception as exc:
    print("FAIL B: the control account refused as %s" % type(exc).__name__)
    ok = False

if ok:
    print("P19-1-AC1 PASS")
else:
    print("P19-1-AC1 FAIL")
sys.exit(0 if ok else 1)
