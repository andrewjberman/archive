# TO D0_TIGHTENING.TO-5 — T4 declarations over the census AS READ (LAPTOP)

<task_order id="D0_TIGHTENING.TO-5" project="D0_INFRA_TIGHTENING">
<issued_to>0.8.0_AE_CloudComp</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:45Z</issued>
<dated>behind your standing queue (already the T4 tail of it)</dated>
<status>staged -- GO paired</status>
<priority>P2</priority>
<authority>D0_INFRA_TIGHTENING_PRD.md §6 row 5 at dispatch vintage @4bf291b26c, **as amended by CVO P0-1 @c7e4d16f6c**. Placement: LAPTOP (CTO ruling FINAL 193804Z).</authority>
</task_order>

## Objective
Every row in the fork census carries either `FORK-DELIBERATE(<why>)` or `DRIFT(<owner>)`.

## ⚠ THE ACCEPTANCE IS DENOMINATOR-RELATIVE — THIS IS THE POINT OF THE AMENDMENT
**Zero undeclared rows AGAINST THE CENSUS AS *YOU* READ IT AT TO TIME.** The row count is
**REPORTED BY THIS TO, NEVER ASSERTED IN ADVANCE.**

The brief's "16+3" is a **PRIOR you are chartered to re-read**, not a target. CVO P0-1 named exactly
why an acceptance pre-committing that number is defective: it would **pass at "16+3" while a 17+3
census left rows undeclared.** So: re-read the census, print the denominator, declare every row you
found. If your read differs from 16+3, that difference is a RESULT to report — not a discrepancy to
reconcile away.

## Acceptance criteria
- **T4-1 CENSUS RE-READ + DENOMINATOR PRINTED** (the count you measured, with how you enumerated it).
- **T4-2 EVERY ROW DECLARED** `FORK-DELIBERATE(why)` or `DRIFT(owner)` — zero undeclared against
  T4-1's denominator.
- **T4-3 DRIFT rows carry a NAMED OWNER** (a drift row without an owner is an unrouted finding, not
  a declaration).
- **T4-4 proof instance VALID rc=0 positional: ids T4-1..T4-4.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>T4-1,T4-2,T4-3,T4-4</expected_criteria>
  <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D0_TIGHTENING.TO-5_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Reporting
COO at census-read (report the denominator THEN, before declaring — so the number is on the record
independent of the outcome) and at complete. Session log w/ Compiler Tools section.
