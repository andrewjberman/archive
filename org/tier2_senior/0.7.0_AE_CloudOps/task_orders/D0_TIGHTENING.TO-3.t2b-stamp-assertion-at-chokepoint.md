# TO D0_TIGHTENING.TO-3 — T2b stamp assertion at the deploy chokepoint (LAPTOP)

<task_order id="D0_TIGHTENING.TO-3" project="D0_INFRA_TIGHTENING">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:45Z</issued>
<dated>ONLY after TO-2's stamps exist on checked paths</dated>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "D0_TIGHTENING" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged -- HARD-GATED ON TO-2 (asserting on a stamp that does not exist yet is a gate that fails on everything)</status>
<priority>P2</priority>
<authority>D0_INFRA_TIGHTENING_PRD.md §4b + §6 row 3 at dispatch vintage @4bf291b26c. Placement: LAPTOP (CTO ruling FINAL; T2b's exercise needs a real deploy window, which lives here).</authority>
</task_order>

## Objective
Classify at the deploy chokepoint — **classify, never block** (except the one stop-shape below).
The PRD is explicit that this layer's job is to tell the three cases apart.

## THE CLASSIFICATION IS THE DELIVERABLE
Rule 22a's gate-candidate wording is the bar: a detector that **cannot tell a hold from neglect
manufactures the wrong reflex**, and the reflex a bare drift alert invites is "deploy" — which is
exactly wrong for a deliberately-held function. So the output must discriminate:
- **STALE-BY-NEGLECT** — the S5 replay **REFUSES** until acknowledged.
- **DELIBERATELY-HELD** — **proceeds**, and the proceed is PRINTED (a silent proceed is
  indistinguishable from no check having run).
- **TWO-HOMES-DIVERGED** — one logical producer, two independently-editable homes. This is the real
  defect and it reads CLEAN to a filename-resolved check.

## Acceptance criteria
- **T2b-1 S5 REPLAY REFUSES** with `class=STALE-BY-NEGLECT` until acknowledged. Exercise the refusal
  — a passing assertion never made to fail has never been tested.
- **T2b-2 DELIBERATELY-HELD PROCEEDS, PRINTED.**
- **T2b-3 POSITIVE CONTROL:** a genuinely-current path classifies clean and is NOT refused (run it
  as a SEPARATE invocation from the target — a control sharing an invocation with its target is not
  a control).
- **T2b-4 proof instance VALID rc=0 positional: ids T2b-1..T2b-4.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>T2b-1,T2b-2,T2b-3,T2b-4</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D0_TIGHTENING.TO-3_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- Do not start before TO-2's stamps are on the checked paths.
- Do not turn this into a blocking gate beyond the named STALE-BY-NEGLECT stop-shape — that shape is
  already worded in the brief and is the only one authorized.

## Reporting
COO, cc CTO (chokepoint surface). Session log w/ Compiler Tools section.
