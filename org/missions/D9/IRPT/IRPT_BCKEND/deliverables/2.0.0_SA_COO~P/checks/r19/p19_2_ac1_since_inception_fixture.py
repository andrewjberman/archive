"""IB-pr-192 AC1 -- 'Since inception' answers from the account's first data point (UIC-06 backend half, UIC-07).

Usage: python p19_2_ac1_since_inception_fixture.py <worktree root>

Arm A (the built behaviour): a request whose start is the portal's Since-inception sentinel 1970-01-01 answers a
report whose returns.period_returns carries period "SI" and whose dates.actual_start is the account's FIRST OK
business_date in the engine (here 2025-12-31), with a finite value above -1.
Arm B (the control): a 3-year request (start 2023-01-08, not a ruled window and not the sentinel) still refuses as
f49_engine.WindowNotRuled.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _engine_path import install  # noqa: E402

root, package = install(sys.argv[1] if len(sys.argv) > 1 else ".")
sys.path.insert(0, str(package / "tests"))
import test_f49_engine as t  # noqa: E402

f49 = t.f49_engine
GOOD = "0010498003"
DAYS = {
    "2025-12-30": [(GOOD, None, None, None, None)],
    "2025-12-31": [(GOOD, 0.001, 99.0, 100.0, 0.0)],
    "2026-01-02": [(GOOD, 0.010, 100.0, 101.0, 0.0)],
    "2026-01-05": [(GOOD, 0.001, 101.0, 101.1, 0.0)],
    "2026-01-06": [(GOOD, -0.005, 101.1, 100.6, 0.0)],
    "2026-01-07": [(GOOD, 0.002, 100.6, 100.8, 0.0)],
}
END, FIRST_OK = "2026-01-07", "2025-12-31"
ok = True


def calc(start):
    source = f49.EngineSource(t.FakeS3(DAYS), bucket=t.BUCKET, root=t.ROOT_PREFIX, max_workers=2)
    return f49.calculate(t._scope(t.opaque_account(t.tenants._CANONICAL_49F, GOOD)), start, END, source)


try:
    report = calc("1970-01-01")["report"]
    periods = [p.get("period") for p in report["returns"]["period_returns"]]
    actual = report["dates"]["actual_start"]
    value = report["returns"]["account_detail"][0]["value"]
    if "SI" in periods and actual == FIRST_OK and math.isfinite(value) and value > -1.0:
        print("PASS A: SI from %s, value %.6f" % (actual, value))
    else:
        print("FAIL A: periods %r, actual_start %r (want %s), value %r" % (periods, actual, FIRST_OK, value))
        ok = False
except Exception as exc:
    print("FAIL A: the Since-inception request refused as %s" % type(exc).__name__)
    ok = False

try:
    calc("2023-01-08")
    print("FAIL B: a 3-year request was answered")
    ok = False
except f49.WindowNotRuled:
    print("PASS B: a 3-year request refuses as WindowNotRuled")
except Exception as exc:
    print("FAIL B: a 3-year request refused as %s, not WindowNotRuled" % type(exc).__name__)
    ok = False

if ok:
    print("P19-2-AC1 PASS")
else:
    print("P19-2-AC1 FAIL")
sys.exit(0 if ok else 1)
