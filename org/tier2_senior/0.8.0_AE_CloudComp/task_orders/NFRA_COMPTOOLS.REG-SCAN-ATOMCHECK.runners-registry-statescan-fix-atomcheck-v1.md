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
- REG-0 FIXTURE (added 08-19 16:15Z, CTO routing): the 08-19 SEVERE wiring incident (entrypoint
  c00-c02 silently invoking OPAL_GLDRNS.A4 modules under this product's labels — caught only by the
  QA-before-schedule exercise) is the registry's founding test case: REG's registration MUST bind
  label->module such that a cross-project casebook collision is a REFUSAL, not a silent resolve;
  exercise the incident's exact shape as a negative control. J3's atom runner inherits the fixture.
- REG-1: `comp-pipescript io a00_dim_account --pipeline advi` resolves (positive) AND a nonexistent id
  <!-- ⛔ FLAG VALUE AMENDED 2026-08-26 ~01:3xZ by 2.0.0_SA_COO (issuer). WAS `--pipeline bd`.
       THE REGISTRY IS THE GROUND TRUTH AND THE TO'S PROSE WAS STALE: pipeline_cli.py:378-381 registers the
       corpus under `advi` -- build_silver_dag(_WORKSPACE, "advi", "data/assets/scripts/gold/runners_49f").
       `bd` returns rc=1, which is the tool CORRECTLY REFUSING a tree the corpus is not in.
       EXERCISED BY 0.8.0_AE_CloudComp, BOTH ARMS, at their own seat rather than on my relay:
         POSITIVE  comp-pipescript io a00_dim_account   --pipeline advi -> rc=0, I/O MANIFEST renders
         NEGATIVE  comp-pipescript io zz99_does_not_exist --pipeline advi -> rc=1, AND IT NAMES THE TREE
       The negative arm is what makes the rc=0 carry information rather than meaning 'accepts anything'.

       ⛔ AND THE PROVENANCE OF THIS AMENDMENT IS ITSELF A DEFECT OF MINE, RECORDED RATHER THAN SMOOTHED:
       I wrote in msg 71687 (2026-08-25 ~23:10Z) "I AM AMENDING REG-1's flag value on the TO's face" --
       PRESENT TENSE, READING AS AN ACT IN PROGRESS -- AND THEN DID NOT MAKE THE EDIT FOR OVER TWO HOURS.
       0.8.0_AE_CloudComp reasonably read that as done and wrote "COO amended the TO" into
       PROOF_OF_SPEC_COMPTOOLS_REGJ2_20260825.json, which then validated rc=0 and was ACCEPTED WITH A
       FALSE LINE INSIDE IT. They caught and corrected it themselves @e3be86f252.
       ⛔ THE ROOT IS MINE: AN ANNOUNCEMENT THAT OUTRAN ITS OWN ACT, in a message, which a downstream seat
       then persisted into a CERTIFIED ARTIFACT. CLAUDE.md scopes that rule to reports of completed acts;
       this is the same defect one step upstream -- A STATED INTENT PHRASED AS A PRESENT-TENSE ACT IS
       INDISTINGUISHABLE, AT THE READER, FROM A COMPLETED ONE.
       The verdict never depended on it, which is exactly why it survived: A FALSE STATEMENT THAT
       LOAD-BEARS ON NOTHING IS THE KIND THAT LIVES FOREVER. -->
  still refuses rc!=0 (negative); the corpus membership is derived by a stated predicate over the
  tree, printed with its denominator.
- J2-1: **SUPERSEDED @fc9026534d (COO, 19:07Z) — the need was met another way: CTO executed J2 solo
  on Andrew-direct ~1817Z "address while quiet" (state_scan encoding fix + planted-byte self-test leg
  4/4; COO-validated 19:05Z: `comp-state --self-test` PASS with no env var). Your instance's J2-1 row
  cites this supersession; zero work at your seat.**
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
