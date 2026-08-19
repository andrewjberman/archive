# TO D0_TIGHTENING.TO-2 — T2a BUILD_MANIFEST stamp generalization (LAPTOP)

<task_order id="D0_TIGHTENING.TO-2" project="D0_INFRA_TIGHTENING">
<issued_to>0.8.0_AE_CloudComp</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:45Z</issued>
<dated>with/after TO-1 (same builder window)</dated>
<status>complete -- BUILT + EXERCISED 2026-08-19 @1bd55740e9; proof VALID rc=0. Both homes section-4b COMPLETE (0/2 -> 2/2, denominator printed both sides); sidecar 1/2 -> 2/2; 16/16 build checks + two-sided determinism control 4/4. DEPLOYED plane UNCHANGED BY CONSTRUCTION (no rebuild required by this TO, none done). T2a-3 mechanism stated WITH its measured gap: 0 of 27 EC2 services bundle, so the propagation path is correct and inert.</status>
<priority>P2</priority>
<authority>D0_INFRA_TIGHTENING_PRD.md §4b + §6 row 2 at dispatch vintage @4bf291b26c. Placement: LAPTOP (CTO ruling FINAL 193804Z; §7 notes the deploy chokepoints run laptop today).</authority>
</task_order>

## Objective
Emit `BUILD_MANIFEST` from **both** `build_package.py` homes so the Rule-22a CODE-layer read becomes
a lookup instead of an archaeology exercise. EC2 bundles pick it up at next touch.

## Why this matters (the gap it closes, stated so you can aim at it)
Rule 22a's own words: every applied-truth primitive we have reads CONFIGURATION and PERMISSIONS, so
**a function whose running bytes are older than its built-from bytes passes every rung** — plan
0-diff, `get-function-configuration`, and a green scheduled run all pass on the OLD code. The stamp
is what makes deployed-vs-built-from answerable at all.

## Acceptance criteria
- **T2a-1 BOTH HOMES EMIT.** Both `build_package.py` homes emit `BUILD_MANIFEST`. "Both" is the
  criterion — one home stamping is the two-homes-diverged hazard wearing a success badge.
- **T2a-2 CENSUS COVERAGE RISES:** re-run the coverage census and show the delta, with the
  denominator printed on both sides.
- **T2a-3 EC2 BUNDLES** pick the stamp up at next touch (state the mechanism; no bundle rebuild is
  required by this TO).
- **T2a-4 proof instance VALID rc=0 positional: ids T2a-1..T2a-4.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>T2a-1,T2a-2,T2a-3,T2a-4</expected_criteria>
  <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D0_TIGHTENING.TO-2_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Reporting
COO, cc AE (TO-3 is staged on this and cannot start until stamps exist on checked paths). Session
log w/ Compiler Tools section.
