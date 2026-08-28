"""PRF-b-2 offline arms -- everything that does NOT need S3.

Compile is not import and import is not execution, so this actually RUNS the new code
paths. Each arm states what a FAIL would mean; an arm that cannot fail is not an arm.
"""
import datetime as dt
import subprocess
import sys
from pathlib import Path

# Workspace root is DERIVED, never hardcoded (CLAUDE.md: derive, do not hardcode --
# a baked absolute path makes an artifact device-specific and it dies on the next box).
ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/runners_49f"))
sys.path.insert(0, str(ROOT))

import perfrp_emit_core as core  # noqa: E402
from perfrp_rollup import (  # noqa: E402
    STATE_COMPUTED,
    STATE_COMPUTED_PARTIAL,
    link_returns,
    summed_returns_MUTANT,
)

FAILS = []


def check(name, cond, detail=""):
    print("  %-58s %s%s" % (name, "PASS" if cond else "*** FAIL ***",
                            ("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(name)


print("=" * 78)
print("ARM 1 -- the imports resolve AND the contract exports the names")
print("=" * 78)
check("SI_FLOOR_DATE imported", core.SI_FLOOR_DATE == "2024-07-08", core.SI_FLOOR_DATE)
check("STATE_CLASSIFIER_FIELD is 'status'", core.STATE_CLASSIFIER_FIELD == "status",
      core.STATE_CLASSIFIER_FIELD)
check("SI_WINDOW_START_ASSERTED is True", core.SI_WINDOW_START_ASSERTED is True)
check("calendar frontier reachable", callable(core.calendar_source))
print("  calendar_source() = %s" % core.calendar_source())

print("=" * 78)
print("ARM 2 -- _period_window: a WINDOW, not a day (the round-1 defect)")
print("=" * 78)
days, start, clamped = core._period_window("SI", "2024-11-07")
check("SI window is many days, not 1", len(days) > 1, "%d trading days" % len(days))
check("SI starts at the ruled floor", start.isoformat() == core.SI_FLOOR_DATE,
      start.isoformat())
check("first trading day >= floor", days[0].isoformat() >= core.SI_FLOOR_DATE,
      days[0].isoformat())
check("last trading day == as-of", days[-1].isoformat() == "2024-11-07",
      days[-1].isoformat())
qtd, qs, _ = core._period_window("QTD", "2024-11-07")
check("QTD starts at quarter start (Oct 1)", qs == dt.date(2024, 10, 1), qs.isoformat())
check("QTD is shorter than SI", len(qtd) < len(days), "%d vs %d" % (len(qtd), len(days)))
ytd, ys, ycl = core._period_window("YTD", "2024-11-07")
check("YTD clamps to the SI floor (no pre-floor claim)", ycl is True and ys.isoformat() == core.SI_FLOOR_DATE,
      "start=%s clamped=%s" % (ys.isoformat(), ycl))

print("  NEGATIVE CONTROL -- an unruled period must REFUSE, not default:")
try:
    core._period_window("max", "2024-11-07")
    check("'max' refused", False, "it returned a window -- SI/max aliasing is live")
except core.EmitRefused as e:
    check("'max' refused (DATA-defined, not a contract period)", True, str(e)[:60])

print("=" * 78)
print("ARM 3 -- inv-6: geometric linking, and the MUTANT must FAIL")
print("=" * 78)
series = [0.01, 0.02, -0.005]
prod = 1.0
for r in series:
    prod *= (1 + r)
prod -= 1.0
val, state, detail = link_returns(series, expected_days=3)
check("link_returns reproduces PROD(1+r)-1", abs(val - prod) < 1e-12,
      "%.12f vs %.12f" % (val, prod))
check("state COMPUTED at full coverage", state == STATE_COMPUTED, state)
mut = summed_returns_MUTANT(series)
check("MUTANT (summing) DIFFERS from the law", abs(mut - val) > 1e-9,
      "mutant=%.12f law=%.12f delta=%.2e bp" % (mut, val, abs(mut - val) * 1e4))

print("=" * 78)
print("ARM 4 -- expected_days: the arm round 1 could not fail")
print("=" * 78)
# Round 1 passed expected_days=len(series). Show that this CANNOT report a shortfall.
r1_val, r1_state, r1_detail = link_returns([0.01], expected_days=1)
check("ROUND-1 SHAPE reports COMPUTED coverage 1.0 on a 1-day 'window'",
      r1_state == STATE_COMPUTED and r1_detail.get("coverage") == 1.0,
      "state=%s coverage=%s" % (r1_state, r1_detail.get("coverage")))
# Round 2 hands the ruled trading-day count, so the same one-day read is PARTIAL.
r2_val, r2_state, r2_detail = link_returns([0.01], expected_days=len(days))
check("ROUND-2 SHAPE reports PARTIAL on the same data",
      r2_state == STATE_COMPUTED_PARTIAL,
      "state=%s days_missing=%s coverage=%.4f"
      % (r2_state, r2_detail.get("days_missing"), r2_detail.get("coverage")))
print("  ^ SAME INPUT, DIFFERENT VERDICT: this is the discriminator round 1 lacked.")

print("=" * 78)
print("ARM 5 -- NaN is not None, and neither is ever 0.0 (the R1 AC8 regression)")
print("=" * 78)
nan = float("nan")
v_none, s_none, _ = link_returns([0.01, None, 0.02], expected_days=3)
v_nan, s_nan, _ = link_returns([0.01, nan, 0.02], expected_days=3)
check("None day -> PARTIAL, not counted as 0.0", s_none == STATE_COMPUTED_PARTIAL)
check("NaN day -> same state as None", s_nan == s_none, "%s vs %s" % (s_nan, s_none))
check("NaN and None produce the SAME value", abs(v_nan - v_none) < 1e-15,
      "%.12f vs %.12f" % (v_nan, v_none))
# CORRECTED ARM. The first version asserted "substituting 0.0 CHANGES the answer" with
# an `or True` escape, which made it unfailable -- a wrong ACCEPT that certifies in
# silence. It was also FALSE as written: (1 + 0.0) is the multiplicative identity, so a
# zero-substituted day leaves the linked VALUE bit-identical. Measured: both 0.0302.
# THE REAL HAZARD IS THE STATE, NOT THE VALUE. A refused day silently coerced to 0.0
# vanishes from the coverage count, so the window reports COMPUTED over a day nobody
# measured -- it claims "flat that day" when the truth is "unknown that day".
zero_val, zero_state, zero_detail = link_returns([0.01, 0.0, 0.02], expected_days=3)
check("zero-substitution leaves the VALUE identical (identity element)",
      abs(zero_val - v_none) < 1e-15,
      "zero-sub=%.12f none=%.12f -- so VALUE cannot detect the defect" % (zero_val, v_none))
check("zero-substitution FLIPS the state COMPUTED_PARTIAL -> COMPUTED",
      zero_state == STATE_COMPUTED and s_none == STATE_COMPUTED_PARTIAL,
      "zero=%s none=%s" % (zero_state, s_none))
check("...and erases the missing-day count (3 present vs 2)",
      zero_detail.get("days_present") == 3
      and link_returns([0.01, None, 0.02], expected_days=3)[2].get("days_present") == 2,
      "zero=%s none=%s" % (zero_detail.get("days_present"),
                           link_returns([0.01, None, 0.02], expected_days=3)[2].get("days_present")))

print()
print("=" * 78)
if FAILS:
    print("RESULT: %d ARM(S) FAILED: %s" % (len(FAILS), FAILS))
    sys.exit(1)
print("RESULT: ALL ARMS PASS (denominator: every check above)")
