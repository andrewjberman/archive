"""PRF-a-2 -- MUTANT EXERCISE on the gains identity (ADVI_PERFRP TO-R1-DS, AC3).

WHY THIS EXISTS
---------------
AC3 requires: "Gains identity asserted to the cent on the projection's output."
The identity (c00_account_gains.py:6) is

    d_aua (= emv - bmv) = nna_cash + nna_in_kind + income - fees_tax + market_growth

Before asserting it I read how `market_growth` is produced. c00_account_gains.py:113:

    df["market_growth"] = df["d_aua"] - df["nna_total"] - df["income"] + df["fees_tax"]

market_growth is the RESIDUAL. Substituting :113 into the drift check at :145-146:

    drift = d_aua - (nna_total + income - fees_tax + market_growth)
          = d_aua - (nna_total + income - fees_tax
                     + d_aua - nna_total - income + fees_tax)
          = d_aua - d_aua
          = 0                                    <-- algebraically, for ANY inputs

So the assertion CANNOT FAIL. It is a floating-point representation test wearing a
correctness test's clothes -- "an instrument that could not have said otherwise"
(CONTROLS_OVER_CARE). The core's own docstring says so plainly and names the real
discriminator: recon_growth_pct_of_bmv, a DIAGNOSTIC of classification health.
The core is not wrong. The ACCEPTANCE CRITERION is, if read literally.

This file does not argue that from algebra. It RUNS THE MUTANT: it corrupts an
input badly enough that any real correctness check would scream, and shows the
identity still closes to 0.00. A claim that a check is vacuous is itself a claim,
and it is cheap to exercise.

NOT a production script: an acceptance-evidence artifact, deliberately outside
data/assets/scripts/gold/runners_49f/ so it is not in the Rule-13 deploy namespace.
"""
from __future__ import annotations


def drift_as_specified(d_aua, nna_total, income, fees_tax, market_growth):
    """The AC3 assertion exactly as the criterion words it (c00_account_gains.py:145-146)."""
    return abs(d_aua - (nna_total + income - fees_tax + market_growth))


def market_growth_as_built(d_aua, nna_total, income, fees_tax):
    """c00_account_gains.py:113 -- market_growth is the RESIDUAL."""
    return d_aua - nna_total - income + fees_tax


def run_case(label, bmv, emv, nna_total, income, fees_tax):
    d_aua = emv - bmv
    mg = market_growth_as_built(d_aua, nna_total, income, fees_tax)
    drift = drift_as_specified(d_aua, nna_total, income, fees_tax, mg)
    print("  %-46s d_aua=%12.2f  mg=%12.2f  DRIFT=%.10f  %s"
          % (label, d_aua, mg, drift, "PASS" if drift < 0.01 else "FAIL"))
    return drift


def main() -> int:
    print("PRF-a-2 MUTANT EXERCISE -- is the AC3 identity assertion capable of failing?")
    print("=" * 104)

    print("\nBASELINE -- a plausible, well-formed account-window:")
    base = run_case("honest inputs", bmv=1_000_000.0, emv=1_050_000.0,
                    nna_total=20_000.0, income=3_000.0, fees_tax=2_500.0)

    print("\nMUTANTS -- each corrupts an input a real correctness check MUST catch:")
    muts = [
        ("income ZEROED (drops all dividends/interest)",
         1_000_000.0, 1_050_000.0, 20_000.0, 0.0, 2_500.0),
        ("fees SIGN-FLIPPED (fees added, not subtracted)",
         1_000_000.0, 1_050_000.0, 20_000.0, 3_000.0, -2_500.0),
        ("nna INFLATED 100x (a misplaced decimal)",
         1_000_000.0, 1_050_000.0, 2_000_000.0, 3_000.0, 2_500.0),
        ("bmv/emv SWAPPED (return sign inverted)",
         1_050_000.0, 1_000_000.0, 20_000.0, 3_000.0, 2_500.0),
        ("EVERY flow input set to garbage",
         1_000_000.0, 1_050_000.0, -9.9e9, 7.7e9, 1.2e9),
        ("all flows ZERO (whole classification lost)",
         1_000_000.0, 1_050_000.0, 0.0, 0.0, 0.0),
    ]
    drifts = [run_case(lbl, b, e, n, i, f) for lbl, b, e, n, i, f in muts]

    print("\n" + "=" * 104)
    n_pass = sum(1 for d in drifts if d < 0.01)
    print("DENOMINATOR: %d mutants run, each corrupting an input that changes a client-facing "
          "figure." % len(drifts))
    print("  mutants the AC3 assertion CAUGHT:  %d of %d" % (len(drifts) - n_pass, len(drifts)))
    print("  mutants the AC3 assertion PASSED:  %d of %d" % (n_pass, len(drifts)))
    print("  baseline drift: %.10f" % base)

    verdict = (n_pass == len(drifts))
    print("\nVERDICT: %s" % (
        "THE ASSERTION IS VACUOUS. It passed every mutant, including total garbage.\n"
        "         It tests float representation, not correctness. Satisfying AC3 literally\n"
        "         produces a FALSE GREEN on a client-facing figure."
        if verdict else
        "the assertion caught at least one mutant -- re-examine the algebra above."))

    print("\nWHAT DOES DISCRIMINATE (the core's own answer, c00_account_gains.py:8-10, 118):")
    print("  recon_growth_pct_of_bmv = market_growth / bmv -- a DIAGNOSTIC of classification")
    print("  health. A large value flags a mis-signed or missing flow, never a market move.")
    print("  On the mutants above this moves sharply while drift stays 0.00:")
    for lbl, b, e, n, i, f in muts:
        d_aua = e - b
        mg = market_growth_as_built(d_aua, n, i, f)
        print("     %-46s recon_growth_pct_of_bmv = %10.4f" % (lbl, mg / b if b > 0 else 0.0))

    # rc=0 means "the finding reproduces" -- this artifact's job is to demonstrate the
    # vacuity, so a reproduced finding is a successful run.
    return 0 if verdict else 1


if __name__ == "__main__":
    raise SystemExit(main())
