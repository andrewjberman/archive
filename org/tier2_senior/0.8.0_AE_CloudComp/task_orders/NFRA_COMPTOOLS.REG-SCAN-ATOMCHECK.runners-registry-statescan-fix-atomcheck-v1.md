# TO NFRA_COMPTOOLS.REG-SCAN-ATOMCHECK — three comp-lane acts: runners_49f registry (R-3) + state_scan self-test fix (J2) + comp-atomcheck v1 (J3)

<task_order id="NFRA_COMPTOOLS.REG-SCAN-ATOMCHECK" project="NFRA_COMPTOOLS">
<issued_to>0.8.0_AE_CloudComp</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T17:10Z</issued>
<dated>groups REG + J2: 2026-08-19 (beside PREFIX-READS) · group J3: 2026-08-20 (usable by DS~B's P4 emit)</dated>
<status>pending -- GO received 2026-08-18T170938Z (COO @dfb5fd8f48); REG+J2 dated 08-19 beside PREFIX-READS, J3 08-20; J1 explicitly NOT released (held at COO)</status>
<priority>P2 — REG closes the coverage gap every runner TO's Phase-1 clause currently fails on; J3 feeds the P4 emit</priority>
<authority>CTO ruling set @CTO_GATE_AND_RULING_SET_20260818_1700Z.md: R-3 (runners_49f registry -> 0.8.0, predicate-derived) + G-C (CRO~A TIGHTENING_ENUMERATION_SPEC @1dceb7d61d RATIFIED; J2/J3 released by COO per the spec's own routing suggestions). J1 (proof-board) is NOT released — deliberately held at COO's allocation.</authority>
</task_order>

## Objective
Three bounded comp-lane acts, one seat, grouped instances:
- **REG (08-19):** the comp-pipescript BD-gold registry gains the `data/assets/scripts/gold/runners_49f/`
  corpus (a00..d14 + runner_common) — PREDICATE-DERIVED over the tree, never a hand list (a predicate
  is not a roster; a roster must be a re-derived predicate), so the next added runner registers itself.
- **J2 (08-19):** the `state_scan.py:68` one-line fix + its self-test leg, exactly per the ratified
  spec's J2 section.
- **J3 (08-20):** `comp-atomcheck` v1 — the 5 checkable atoms per the ratified spec; DS~B's lineage
  declarations at P4-EMIT are its first consumer (interface documented so DS~B can declare against it).

## Compiler tools (three-phase)
Phase 1: read the registry's current enumeration mechanism (extend, don't fork — build ladder rung 2).
Phase 2: commit-gate. Phase 3: the positive/negative exercises below.

## Cross-domain coordination
- shared_resource: the comp-pipescript registry — DS~A's three runner TOs cite `io --pipeline bd` in
  their Phase-1 clauses; MCP DS~A when REG lands so their degraded path retires.
- shared_resource: comp-atomcheck's declaration interface — DS~B consumes at P4-EMIT; MCP DS~B the
  interface when J3 lands.

## Acceptance criteria
- REG-1: `comp-pipescript io a00_dim_account --pipeline bd` resolves (positive) AND a nonexistent id
  still refuses rc!=0 (negative); the corpus membership is derived by a stated predicate over the
  tree, printed with its denominator.
- J2-1: the `:68` fix landed with the self-test leg green; self-test failure exercised once (mutant).
- J3-1: comp-atomcheck v1 runs the 5 atoms per spec; one positive + one negative fixture each,
  results printed; declaration interface documented; MCP'd to DS~B by 08-20.
- RSA-VAL: proof instance per group, rc=0 positional, grammar below.

<proof_of_spec>
  <expected_criteria>REG-1,J2-1,J3-1,RSA-VAL</expected_criteria>
  <instance_path_grammar>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/PROOF_OF_SPEC_COMPTOOLS_{group}_{YYYYMMDD}.json</instance_path_grammar>
</proof_of_spec>

## Do not
- No J1 (proof-board) work under this TO — held at COO. No registry hand-lists. No new entrypoints
  where an existing mechanism extends.

## Reporting
COO (cc CTO, DS~A for REG, DS~B for J3) per group at landed. Surprise channel: one banked line to
COO. Session log with Compiler Tools section = deliverable.
