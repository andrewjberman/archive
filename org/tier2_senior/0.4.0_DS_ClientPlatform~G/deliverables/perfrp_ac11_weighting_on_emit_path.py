"""AC11 -- IS THE WEIGHTED ROLLUP ACTUALLY APPLIED ON THE EMIT PATH?

WHY THIS EXISTS. 0.7.0_AE_CloudOps~G verified the grain fix at 69085 and then said the
thing that makes the pass honest rather than wide:

  "THE GRAIN IS NOW RIGHT. WHETHER THE ROLLUP LAW IS ACTUALLY APPLIED ON THIS PATH IS
   NOT OBSERVABLE IN THIS EMISSION, because every value is NOT_COMPUTED -- there are no
   returns to roll up, so a correct weighted parent and a naive mean are
   indistinguishable at 4,385 nulls."

That is exactly right, and it is a hole I would otherwise be carrying until the D-1
mirror remedy lands at DS~H. Their proposed remedy was to re-run AC11 against real
returns at wire time. THAT IS THE RIGHT LONG-RUN CHECK AND IT IS STILL OWED -- but it
is not the only one available today, and waiting for it would leave the criterion
resting on an emission that structurally cannot discriminate.

WHAT THIS ADDS THAT b-7 DOES NOT. b-7 exercises `rollup()` DIRECTLY and proves the LAW
is correct. It says nothing about whether `_performance` CALLS it, calls it with the
right weights, or quietly averages. The defect AE~G found was precisely of that kind:
a function that accepted an argument and ignored it. A correct library reached through
a wrong call site is the shape at risk here, so the subject of this exercise is THE CALL
SITE, not the law.

METHOD. Inject a frame in which returns DO compute, chosen so that the weighted answer
and the naive mean are not merely different but OPPOSITE IN SIGN. A gap of a few basis
points can hide in rounding; a sign flip cannot be misread.

  relationship REL_SPREAD, two accounts, MV 9:1
    ACCT_BIG    MV 9,000,000   daily +2.00%, +2.00%   window  +4.0400%
    ACCT_SMALL  MV 1,000,000   daily -8.00%, -8.00%   window -15.3600%
  WEIGHTED (correct): each DAY is weighted by MV, then linked
    day0 = (0.02*9M + -0.08*1M)/10M = +1.00%   day1 = +1.00%   linked = +2.0100%
  NAIVE MEAN (the mutant): mean of the two account window returns = -5.6600%
  The two answers are 767 bp apart AND ON OPPOSITE SIDES OF ZERO.

  relationship REL_SOLO, one account -- the control. With a single child, weighted and
  naive coincide by construction, so a PASS there proves nothing about weighting and is
  NOT counted as evidence for it. It is here to prove the fixture does not break the
  ordinary single-account case, which is most of the real book.

WHAT A PASS HERE ESTABLISHES, STATED NARROWLY: on the relationship branch of
`_performance`, parent returns are MV-weighted per day and linked, not averaged across
children. It does NOT establish anything about the live frontier's values, which are
still all NOT_COMPUTED, and it does NOT discharge the wire-time re-run.

EVIDENCE VINTAGE: subject `perfrp_emit_core.py` / `perfrp_rollup.py` at the committing
ref; the fixture is synthetic and carries no live-plane dependency.
"""
from __future__ import annotations

import sys

import pandas as pd

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
import perfrp_emit_core as core  # noqa: E402  the SUBJECT -- imported, never re-typed

ASOF = "2026-08-21"

BIG_MV, SMALL_MV = 9_000_000.0, 1_000_000.0
BIG_DAILY, SMALL_DAILY = 0.02, -0.08
SOLO_MV, SOLO_DAILY = 2_500_000.0, 0.03
NDAYS = 2


def _fixture(table, date, tier="canonical"):
    """Stand in for _read_gold. Carries the four TWR operands DELIBERATELY.

    With the operand columns present, `_performance`'s INPUTS_ABSENT refinement must
    NOT fire -- so this fixture also exercises that branch's negative case, which the
    live frontier (9 columns, operands missing) can never reach.
    """
    if table == "twr_daily":
        rows = []
        for acct, r in (("ACCT_BIG", BIG_DAILY), ("ACCT_SMALL", SMALL_DAILY),
                        ("ACCT_SOLO", SOLO_DAILY)):
            for _ in range(NDAYS):
                rows.append({"account_id": acct, "r_net": r,
                             "bmv": 1.0, "emv": 1.0, "cf_net": 0.0, "cf_gross": 0.0})
        return pd.DataFrame(rows)
    if table == "canonical_valuation":
        return pd.DataFrame([
            {"account_id": "ACCT_BIG", "net_mv_plus_cash": BIG_MV},
            {"account_id": "ACCT_SMALL", "net_mv_plus_cash": SMALL_MV},
            {"account_id": "ACCT_SOLO", "net_mv_plus_cash": SOLO_MV}])
    if table == "dim_relationship":
        return pd.DataFrame([
            {"account_id": "ACCT_BIG", "relationship_id": "REL_SPREAD"},
            {"account_id": "ACCT_SMALL", "relationship_id": "REL_SPREAD"},
            {"account_id": "ACCT_SOLO", "relationship_id": "REL_SOLO"}])
    raise AssertionError("fixture asked for an unexpected table: %s" % table)


def _link(daily):
    v = 1.0
    for d in daily:
        v *= (1.0 + d)
    return v - 1.0


def main() -> int:
    print("AC11 -- WEIGHTED ROLLUP ON THE EMIT PATH (subject: _performance relationship branch)")
    print("raised by 0.7.0_AE_CloudOps~G 69085: the live emission cannot discriminate,"
          " every value is NOT_COMPUTED")
    print("=" * 108)

    # The expectations are DERIVED here rather than pasted, so the fixture and the
    # oracle cannot drift apart silently.
    w_day = (BIG_DAILY * BIG_MV + SMALL_DAILY * SMALL_MV) / (BIG_MV + SMALL_MV)
    expect_weighted = _link([w_day] * NDAYS)
    big_win, small_win = _link([BIG_DAILY] * NDAYS), _link([SMALL_DAILY] * NDAYS)
    expect_naive = (big_win + small_win) / 2.0
    gap_bp = abs(expect_weighted - expect_naive) * 10_000

    print("\n1. THE FIXTURE, and why it discriminates")
    print("   {:<12} {:>14} {:>12} {:>14}".format("account", "MV", "daily", "window"))
    print("   {:<12} {:>14,.2f} {:>11.2f}% {:>13.4f}%".format(
        "ACCT_BIG", BIG_MV, BIG_DAILY * 100, big_win * 100))
    print("   {:<12} {:>14,.2f} {:>11.2f}% {:>13.4f}%".format(
        "ACCT_SMALL", SMALL_MV, SMALL_DAILY * 100, small_win * 100))
    print("   WEIGHTED parent (correct) {:>13.4f}%".format(expect_weighted * 100))
    print("   NAIVE MEAN    (mutant)    {:>13.4f}%".format(expect_naive * 100))
    print("   gap {:,.0f} bp, and OPPOSITE SIGNS -- rounding cannot produce this".format(gap_bp))
    assert expect_weighted > 0 > expect_naive, "fixture lost its sign flip; it no longer discriminates"

    # FIXTURE SELF-CHECK, added after the first run of this file. My first choice of
    # SOLO_DAILY made REL_SOLO and REL_SPREAD both come out at 2.0100% -- the CONTROL
    # and the SUBJECT returning the identical number. All eight checks passed, and
    # would have passed just as cleanly if the two buckets had cross-contaminated,
    # because each was compared against a value the other also satisfied. I caught it
    # by reading the emitted table, not from the PASS line, which is the whole reason
    # the table is printed above the checks.
    expect_solo = _link([SOLO_DAILY] * NDAYS)
    assert abs(expect_solo - expect_weighted) > 1e-6, (
        "the control and the subject expect the SAME value (%.6f); a bucket-mixing "
        "defect would pass every check below. Change SOLO_DAILY." % expect_solo)

    # ---------- exercise the REAL call site ----------
    real = core._read_gold
    core._read_gold = _fixture
    try:
        rel_rows = core._performance(ASOF, "relationship")
        acct_rows = core._performance(ASOF, "account")
    finally:
        core._read_gold = real          # restored in finally: a leaked patch would
                                        # silently poison every later call in-process

    rel = {r["key"]: r for r in rel_rows}
    acct = {r["key"]: r for r in acct_rows}

    print("\n2. WHAT THE EMIT PATH ACTUALLY RETURNED")
    for k in sorted(rel):
        r = rel[k]
        print("   {:<12} accounts={} window_return={:>11.4f}%  state={}".format(
            k, r.get("accounts"), (r["window_return"] or 0.0) * 100, r["figure_state"]))

    checks = []

    def chk(name, got, want, note=""):
        ok = got == want
        checks.append(ok)
        print("   [{}] {:<56} got={!s:<8} want={!s}{}".format(
            "PASS" if ok else "FAIL", name, got, want, ("  -- " + note) if note else ""))

    print("\n3. THE DISCRIMINATING CHECKS")
    got = rel["REL_SPREAD"]["window_return"]
    chk("REL_SPREAD equals the MV-WEIGHTED parent", round(got, 10),
        round(expect_weighted, 10), "the law is applied at this call site")
    chk("REL_SPREAD is NOT the naive mean of child windows",
        abs(got - expect_naive) > 1e-9, True, "the mutant is rejected")
    chk("REL_SPREAD is POSITIVE where the naive answer is negative",
        got > 0 > expect_naive, True, "sign flip -- unmissable if the call site regresses")
    chk("REL_SPREAD child_count", rel["REL_SPREAD"].get("accounts"), 2)

    print("\n4. CONTROLS -- these must NOT be read as evidence of weighting")
    chk("REL_SOLO passes a single child through unchanged",
        round(rel["REL_SOLO"]["window_return"], 10), round(_link([SOLO_DAILY] * NDAYS), 10),
        "single child: weighted == naive BY CONSTRUCTION")
    chk("account leaf still emits ACCOUNT keys", sorted(acct),
        ["ACCT_BIG", "ACCT_SMALL", "ACCT_SOLO"], "the limb that HAD to stay true")
    chk("the two relationships return DIFFERENT values",
        abs(rel["REL_SOLO"]["window_return"] - rel["REL_SPREAD"]["window_return"]) > 1e-6,
        True, "without this, bucket cross-contamination passes every other check")
    chk("relationship keys are NOT account keys",
        set(rel) & set(acct), set(), "AE~G set-equality limb, on the fixture")
    chk("INPUTS_ABSENT refinement does NOT fire when operands present",
        rel["REL_SPREAD"]["figure_state"] != core.STATE_NOT_COMPUTED_INPUTS_ABSENT, True,
        "negative case of the refine branch, unreachable on the live 9-col frontier")

    npass = sum(1 for c in checks if c)
    print("\n" + "=" * 108)
    print("DENOMINATOR: {}/{} checks PASS ({} discriminating, {} controls)".format(
        npass, len(checks), 4, len(checks) - 4))
    print("SCOPE, stated so this cannot be read wider than it is:")
    print("  ESTABLISHED -- on the relationship branch of _performance, parent returns are")
    print("    MV-weighted per day and linked, NOT averaged across children.")
    print("  NOT ESTABLISHED -- anything about live values. The frontier is still all")
    print("    NOT_COMPUTED. The wire-time re-run against real returns is STILL OWED")
    print("    (AE~G 69085), and this exercise does not discharge it.")
    return 0 if npass == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
