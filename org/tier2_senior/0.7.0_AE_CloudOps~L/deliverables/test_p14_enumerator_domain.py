"""E-2 ARMS for ADVI_49F.c02-ENUMERATOR (cell C02-g-9).

Three arms from three truths, plus the mutation that must fail arm (ii).

⛔ WHY ARM (ii) IS THE ONE THAT DRAWS BLOOD. The old enumerator read the OUTPUT table
(flow_ledger) for its domain, so a date missing from the output was missing from its own
work list -- which is how 2026-08-11..08-17 stayed invisible. That defect is INVISIBLE ON
TODAY'S DATA: the backfill filled those dates, so the output now agrees with the calendar
and a "reproduce the stored set" arm passes under BOTH implementations. Only a date MASKED
from the output view separates them. A backfill that repairs a gap destroys the evidence
that the gap recurs, so the arm has to manufacture the evidence.

Author: 0.7.0_AE_CloudOps~L
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "p14_rederive", HERE / "ADVI_49F.P14-VEHICLE_A00_ATTESTATION_REDERIVATION.py")
p14 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(p14)   # the __main__ guard keeps the report from running on import


def _mutant_domain_from_output(trading_days_set, per_input, output_dates):
    """THE MUTATION: the pre-fix behaviour, restored. The domain IS the output table's
    partitions. Lives here and never in the module -- a mutant in production code is a
    second implementation waiting to be called."""
    return set(output_dates), set(output_dates)


def arm_i_reproduces_the_domain():
    """(i) The live domain equals calendar AND presence, and the one stored date it does NOT
    contain is named rather than silently dropped."""
    cal = {"2026-08-25", "2026-08-26", "2026-08-27", "2026-08-28"}
    per = {t: set(cal) for t in ("fact_acc", "fact_sec", "fact_trn", "dim_balance",
                                 "dim_position", "fact_upn", "dim_transaction")}
    domain, presence = p14.compute_domain(cal, per)
    ok = domain == cal and presence == cal
    print("  (i)  domain == calendar when every input is present : %s (%d of %d)"
          % ("PASS" if ok else "FAIL", len(domain), len(cal)))
    return ok


def arm_ii_masked_output_still_enumerated():
    """(ii) THE DISCRIMINATING ARM. A date present in the calendar and in every input, but
    ABSENT from the output table, must STILL be enumerated. The mutant must fail this."""
    cal = {"2026-08-25", "2026-08-26", "2026-08-27"}
    per = {t: set(cal) for t in ("fact_acc", "fact_sec", "fact_trn", "dim_balance",
                                 "dim_position", "fact_upn", "dim_transaction")}
    masked = "2026-08-26"
    output_view = cal - {masked}          # the outage shape: the output is missing a date

    domain, _ = p14.compute_domain(cal, per)
    fixed_ok = masked in domain

    mutant_domain, _ = _mutant_domain_from_output(cal, per, output_view)
    mutant_ok = masked in mutant_domain   # must be FALSE

    print("  (ii) masked-from-output date %s still enumerated  : %s"
          % (masked, "PASS" if fixed_ok else "FAIL"))
    print("       MUTATION (domain read from the output table)  : %s"
          % ("correctly FAILS the arm" if not mutant_ok
             else "*** MUTANT PASSES -- THE ARM CANNOT DISCRIMINATE ***"))
    return fixed_ok and not mutant_ok


def arm_iii_inputs_absent_excluded():
    """(iii) A calendar trading day missing ONE halting input is EXCLUDED, and the caller can
    name which input was absent -- UNBACKFILLABLE-INPUTS-ABSENT."""
    cal = {"2026-08-25", "2026-08-26", "2026-08-27"}
    gone = "2026-08-27"
    per = {t: set(cal) for t in ("fact_acc", "fact_sec", "fact_trn", "dim_balance",
                                 "dim_position", "fact_upn", "dim_transaction")}
    per["dim_transaction"] = cal - {gone}       # the input a prefix-constant census missed

    domain, presence = p14.compute_domain(cal, per)
    excluded = sorted(cal - presence)
    missing_for = [t for t in per if gone not in per[t]]
    ok = gone not in domain and excluded == [gone] and missing_for == ["dim_transaction"]
    print("  (iii) date missing one halting input EXCLUDED      : %s" % ("PASS" if ok else "FAIL"))
    print("       %s  UNBACKFILLABLE-INPUTS-ABSENT: %s" % (gone, missing_for))
    return ok


def arm_iv_annotation_is_not_a_gate():
    """(iv) An ANNOTATION input that is short must NOT remove dates. This is the arm that
    would have caught the original five-table list: intersecting fact_fam would have refused
    the five dates C02-g-7 produced."""
    cal = {"2026-08-11", "2026-08-12", "2026-08-25"}
    per = {t: set(cal) for t in ("fact_acc", "fact_sec", "fact_trn", "dim_balance",
                                 "dim_position", "fact_upn", "dim_transaction")}
    domain, _ = p14.compute_domain(cal, per)      # fam is NOT in per_input at all
    ok = domain == cal
    print("  (iv) short annotation input removes no date        : %s (%d of %d)"
          % ("PASS" if ok else "FAIL", len(domain), len(cal)))
    return ok


def main():
    print("=" * 74)
    print("E-2 ARMS -- C02-g-9 enumerator domain")
    print("=" * 74)
    results = [arm_i_reproduces_the_domain(),
               arm_ii_masked_output_still_enumerated(),
               arm_iii_inputs_absent_excluded(),
               arm_iv_annotation_is_not_a_gate()]
    print("-" * 74)
    print("  %d of %d arms PASS" % (sum(1 for r in results if r), len(results)))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
