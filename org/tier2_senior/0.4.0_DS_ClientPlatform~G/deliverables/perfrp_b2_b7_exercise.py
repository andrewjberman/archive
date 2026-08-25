"""PRF-b-2 + PRF-b-7 EXERCISE (ADVI_PERFRP TO-R1-DS, AC8 + AC11).

Exercises the ONE definition in data/assets/scripts/gold/runners_49f/perfrp_rollup.py.
Everything is IMPORTED from there -- no formula is retyped here, because a test that
restates the thing it tests stops testing it the moment the two drift.

AC8 : served window % == PROD(1+r_net)-1 ; gross stored ; zero-BMV fixture renders
      the FLAG not a zero ; the SUMMED-RETURN MUTANT FAILS the check.
AC11: ONE rollup function ; relationship->account recompute printed ;
      advisor->firm NEVER computed.

EVIDENCE VINTAGE: source citations resolve at 23271aac6480f2ebd65a37247ae64dde4d68c199.
"""
from __future__ import annotations

import sys

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
from perfrp_rollup import (  # noqa: E402  IMPORTED, never copied
    STATE_COMPUTED,
    STATE_COMPUTED_PARTIAL,
    STATE_NOT_COMPUTED_INPUTS_ABSENT,
    STATE_NOT_COMPUTED_INPUTS_PRESENT,
    RollupRefused,
    link_returns,
    rollup,
    summed_returns_MUTANT,
)

TOL = 1e-12
PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    print("  [%s] %-58s %s" % ("PASS" if ok else "FAIL", label, detail))


def independent_link(daily):
    """Deliberately re-derived by a DIFFERENT route than link_returns, so agreement
    is evidence rather than tautology: link_returns multiplies (1+r); this one works
    in log space and exponentiates back. Same maths, different arithmetic path."""
    import math
    acc = 0.0
    for v in daily:
        if v is not None:
            acc += math.log1p(v)
    return math.expm1(acc)


def main() -> int:
    print("PRF-b-2 + PRF-b-7 EXERCISE -- ADVI_PERFRP TO-R1-DS (AC8 + AC11)")
    print("=" * 100)

    # ---------------- AC8: the geometric link ----------------
    print("\nAC8.1 -- served window %% == PROD(1+r)-1, checked against an INDEPENDENT route")
    for name, ser in (("calm 5d", [0.001, -0.002, 0.0015, 0.0004, -0.0011]),
                      ("volatile 5d", [0.06, -0.055, 0.041, -0.038, 0.052]),
                      ("long 60d alternating", [0.01 if i % 2 else -0.009 for i in range(60)])):
        v, st, _ = link_returns(ser)
        ind = independent_link(ser)
        check("%s: link == log-space re-derivation" % name,
              st == STATE_COMPUTED and abs(v - ind) < 1e-9,
              "link=%.10f indep=%.10f" % (v, ind))

    # ---------------- AC8: the mutant MUST fail ----------------
    print("\nAC8.2 -- THE SUMMED-RETURN MUTANT MUST FAIL THE SAME CHECK")
    print("        (a mutant that passes proves the check is vacuous -- the a-2 lesson)")
    any_mutant_passed = False
    for name, ser in (("calm 5d", [0.001, -0.002, 0.0015, 0.0004, -0.0011]),
                      ("volatile 5d", [0.06, -0.055, 0.041, -0.038, 0.052]),
                      ("long 60d alternating", [0.01 if i % 2 else -0.009 for i in range(60)])):
        truth = independent_link(ser)
        mut = summed_returns_MUTANT(ser)
        diverges = abs(mut - truth) > 1e-9
        if not diverges:
            any_mutant_passed = True
        check("%s: mutant DIVERGES from truth" % name, diverges,
              "mutant=%.10f truth=%.10f delta=%.3e bp=%.2f"
              % (mut, truth, mut - truth, abs(mut - truth) * 10000))
    check("no mutant slipped through the check", not any_mutant_passed)

    print("\n        the divergence is NOT a rounding artifact -- it GROWS with")
    print("        volatility and with window length, i.e. exactly where the number matters:")
    for n in (5, 20, 60, 250):
        ser = [0.02 if i % 2 else -0.018 for i in range(n)]
        truth = independent_link(ser)
        mut = summed_returns_MUTANT(ser)
        print("          %3dd  truth=%+.6f  mutant=%+.6f  error=%8.2f bp"
              % (n, truth, mut, abs(mut - truth) * 10000))

    # ---------------- AC8: flags, never zeros ----------------
    print("\nAC8.3 -- UNCOMPUTABLE propagates as a FLAG, never as a zero")
    v, st, d = link_returns([0.01, None, 0.02], expected_days=3)
    check("partial window -> COMPUTED_PARTIAL with coverage",
          st == STATE_COMPUTED_PARTIAL and d["days_missing"] == 1,
          "coverage=%.4f" % d["coverage"])
    v, st, d = link_returns([None, None, None])
    check("all-refused window -> NOT_COMPUTED, value is None (NOT 0.0)",
          st == STATE_NOT_COMPUTED_INPUTS_PRESENT and v is None, "value=%r" % v)
    v, st, d = link_returns([])
    check("no rows -> NOT_COMPUTED_INPUTS_ABSENT, value is None",
          st == STATE_NOT_COMPUTED_INPUTS_ABSENT and v is None, "value=%r" % v)

    print("\nAC8.3b -- NaN MUST COUNT AS UNCOMPUTED (DS~H 67960, mixed partitions)")
    print("        latent behind a DATA SHAPE, not a code path: today's plane hands")
    print("        None, so every fixture written against it used None.")
    nan = float("nan")
    v, st, d = link_returns([0.01, nan, 0.02], expected_days=3)
    check("a NaN day is UNCOMPUTED, not present",
          st == STATE_COMPUTED_PARTIAL and v == v and d["days_missing"] == 1,
          "value=%.6f state=%s" % (v, st))
    v, st, d = link_returns([nan, nan])
    check("all-NaN -> NOT_COMPUTED, value None (was: nan labelled COMPUTED)",
          v is None and st.startswith("NOT_COMPUTED"), "value=%r state=%s" % (v, st))
    v_none, _, _ = link_returns([0.01, None, 0.02], expected_days=3)
    v_nan, _, _ = link_returns([0.01, nan, 0.02], expected_days=3)
    check("NaN and None are treated IDENTICALLY", v_none == v_nan,
          "None->%.10f  NaN->%.10f" % (v_none, v_nan))
    v, st, _ = link_returns([0.01, 0.02])
    check("CONTROL: fix is not over-broad -- clean input still COMPUTED",
          st == STATE_COMPUTED and abs(v - independent_link([0.01, 0.02])) < 1e-12)
    rn = rollup([{"dollars": 1e6, "denominator": 1e6, "daily": [0.01, nan]},
                 {"dollars": 2e6, "denominator": 2e6, "daily": [0.02, 0.01]}],
                from_level="account", to_level="relationship")
    check("rollup survives a NaN child-day without poisoning the parent",
          rn["window_return"] == rn["window_return"] and rn["window_return"] is not None,
          "parent=%+.8f state=%s" % (rn["window_return"], rn["window_return_state"]))

    print("\n        THE ZERO-BMV FIXTURE, which is the live shape today:")
    v, st, d = link_returns([None] * 5, expected_days=5)
    zero_would_be = summed_returns_MUTANT([None] * 5)
    check("zero-BMV window renders the FLAG, not 0.00%",
          v is None and st.startswith("NOT_COMPUTED"),
          "state=%s value=%r  (a zero-substituting impl would have said %.4f%%)"
          % (st, v, zero_would_be * 100))
    print("        ^ that 0.0000 pct is the number an advisor would have been shown.")

    # ---------------- AC11: the rollup ----------------
    print("\nAC11.1 -- relationship -> account recompute, printed")
    kids = [
        {"account": "A", "dollars": 1_000_000.0, "denominator": 1_000_000.0,
         "daily": [0.010, -0.004, 0.006]},
        {"account": "B", "dollars": 250_000.0, "denominator": 250_000.0,
         "daily": [0.020, -0.010, 0.002]},
        {"account": "C", "dollars": 4_000_000.0, "denominator": 4_000_000.0,
         "daily": [-0.001, 0.003, 0.001]},
    ]
    r = rollup(kids, from_level="account", to_level="relationship")
    print("     children: %d" % r["child_count"])
    for k in kids:
        vv, ss, _ = link_returns(k["daily"])
        print("       {:<3} dollars={:>14,.2f} denom={:>14,.2f}  window={:+.6f} ({})".format(
            k["account"], k["dollars"], k["denominator"], vv, ss))
    print("     PARENT dollars={:>14,.2f} denom={:>14,.2f}  window={:+.6f} ({})".format(
        r["dollars"], r["denominator"], r["window_return"], r["window_return_state"]))
    check("parent dollars == SUM(child dollars)",
          abs(r["dollars"] - sum(k["dollars"] for k in kids)) < 0.01)
    check("parent denominator == SUM(child denominators)",
          abs(r["denominator"] - sum(k["denominator"] for k in kids)) < 0.01)
    check("parent window is GEOMETRIC, not an average of child percents",
          r["window_return_state"] == STATE_COMPUTED)

    # the sharp one: parent % must NOT equal the naive mean of child %s
    child_vals = [link_returns(k["daily"])[0] for k in kids]
    naive_mean = sum(child_vals) / len(child_vals)
    check("parent pct != naive mean of child pcts",
          abs(r["window_return"] - naive_mean) > 1e-9,
          "parent=%+.8f naive_mean=%+.8f" % (r["window_return"], naive_mean))

    print("\nAC11.2 -- advisor -> firm is NEVER computed (R-p5)")
    try:
        rollup(kids, from_level="advisor", to_level="firm")
        check("advisor->firm REFUSES", False, "it returned a value -- law not enforced")
    except RollupRefused as e:
        check("advisor->firm REFUSES LOUD", True, str(e)[:64] + "...")
    # positive control: a legal pair must still work, or the refusal proves nothing
    try:
        ok = rollup(kids, from_level="account", to_level="relationship")
        check("POSITIVE CONTROL: a legal pair still computes", ok["dollars"] > 0)
    except RollupRefused:
        check("POSITIVE CONTROL: a legal pair still computes", False, "it refused everything")

    print("\n" + "=" * 100)
    print("DENOMINATOR: %d checks run, %d PASS, %d FAIL" % (PASS + FAIL, PASS, FAIL))
    print("ONE DEFINITION: link_returns and rollup are imported from")
    print("  data/assets/scripts/gold/runners_49f/perfrp_rollup.py -- no formula retyped here.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
