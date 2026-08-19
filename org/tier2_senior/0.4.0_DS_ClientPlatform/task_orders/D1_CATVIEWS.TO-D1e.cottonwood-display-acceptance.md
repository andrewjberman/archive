# TO D1_CATVIEWS.TO-D1e — Cottonwood display acceptance (JOINT DS+DE; chain close)

<task_order id="D1_CATVIEWS.TO-D1e" project="MDPF_CATVIEWS">
<issued_to>0.4.0_DS_ClientPlatform (measurement) + 0.4.0_DE_ClientPlatform (display verify)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:35Z</issued>
<dated>on TO-D1d's rendered view</dated>
<status>staged -- GATED ON TO-D1d; this row closes D1's DONE definition</status>
<priority>P1-program (the DONE gate -- D1 is not done without it)</priority>
<authority>D1_ASSET_CATEGORY_VIEWS_PRD.md §6 item 5 + DONE, at dispatch vintage @3e589fa1eb. Placement: EITHER -> LAPTOP by the standing default (read-only S3 + rendered check).</authority>
</task_order>

## Objective
Measure Cottonwood's Custom and Client figures from cot BD data and verify the global view displays
them under the correct nodes. This is the acceptance that turns "the view renders" into "the view is
right for a firm whose data has a known trap."

## THE TRAP, NAMED UP FRONT (read before you measure)
**cot BD `fact_holdings` is RELATIONSHIP-grain** — one row per Relationship x Account x Asset. **A
naive SUM DOUBLE-COUNTS.** Collapse via `collapse_relationship_grain()` before any figure leaves
your hands (Andrew-direct 2026-08-04; R9 in the PRD's evidence table). A number produced without the
collapse will look plausible and be wrong — and it would land on a served display.

**cot is a COMPLETELY SEPARATE FIRM PIPELINE from bd — never mirror, never sync, never read across**
(gate + IAM enforced).

## Acceptance criteria
- **D1e-1 MEASURED, COLLAPSED:** Custom and Client figures measured from cot BD data with the
  relationship-grain collapse APPLIED and the collapse shown (pre-collapse vs post-collapse figure
  both printed — that delta is the evidence the trap was avoided, and it is the one number a reader
  can check).
- **D1e-2 THE ESTIMATES ARE PRIORS, NOT TARGETS.** The PRD's ~$7M Custom / ~$30M Client are
  estimates the measurement **REPLACES**. A measured $12M is a PASS, not a discrepancy. **Do not
  tune anything to hit the estimate** — if the measured figure diverges materially, that is a
  finding to report, never a reason to adjust the pipeline.
- **D1e-3 DISPLAY CORRECT:** the global view shows the measured Custom and Client figures under the
  correct nodes (DE verifies on the rendered view; cite the render, not the JSON alone).
- **D1e-4 SUM INVARIANT HOLDS for cot** as for the others: five-node sum == total_aua.
- **D1e-5 proof instance VALID rc=0 positional: ids D1e-1..D1e-5.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>D1e-1,D1e-2,D1e-3,D1e-4,D1e-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D1_CATVIEWS.TO-D1e_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- Do not adjust the projection to make a measured figure match an estimate (D1e-2).
- Do not read bd artifacts to "sanity check" cot — separate firms, gate-blocked.

## Reporting
COO at measured and at display-verified — this row's close is what lets me report D1 DONE.
Distinguish success from silent fallback. Session log w/ Compiler Tools section.
