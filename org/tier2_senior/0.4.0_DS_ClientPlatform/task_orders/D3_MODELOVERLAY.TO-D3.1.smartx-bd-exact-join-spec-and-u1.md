# TO D3_MODELOVERLAY.TO-D3.1 — SMARTX_BD_EXACT_JOIN spec + the U1 model-identity edge (LAPTOP; STARTABLE NOW)

<task_order id="D3_MODELOVERLAY.TO-D3.1" project="D3_ACCOUNT_MODEL_OVERLAY">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:50Z</issued>
<dated>startable NOW -- gates on nothing (CVO's dispatch-order note names it in the startable set)</dated>
<status>staged -- GO paired; UNGATED CHAIN HEAD</status>
<priority>P1 -- precondition for the whole D3 chain AND its residual enum gates D6's TO-G</priority>
<authority>D3_ACCOUNT_MODEL_OVERLAY_PRD.md §4.1 + §6 item 1 at dispatch vintage @52a85baf08 (CVO verdict @3e5038ebd3, ACCEPT 0 P0). Placement: LAPTOP -- the PREFER-SITEZ export exception for this row is RETIRED per CTO's final placement ruling 193804Z.</authority>
</task_order>

## Objective
Author the SMARTX_BD_EXACT_JOIN spec, census the residual, and locate the U1 model-identity edge at
source (opal-smartx-ingestion-pipeline + the 0824 silver schemas).

## YOUR RESIDUAL ENUM IS A LOAD-BEARING EXPORT — D6 CONSUMES IT
This is not a D3-local artifact. D6's TO-G (the entity-resolution service) GATES on this TO's
residual ENUM specifically, and TO-G's disambiguation classes are DRAWN FROM it — one residual
vocabulary for one identity plane. CTO's ruled reason: a resolver built before the enum lands would
assign confidence over a universe whose residual is unclassified, making "unresolvable" and
"resolvable-but-in-the-residual" indistinguishable. Author the enum as a public contract, not as
working notes.

## Mandate
- Phase 1: re-run the a06 coverage read; enumerate residual sets WITH DENOMINATORS.
- Phases 2/3: n/a — document + spec deliverable.
- Bucket discipline: 08242234 = MDPF Model Portfolios. Write the FULL 8-digit account, never the
  4-digit prefix — the truncated form is what makes the two Schwab buckets confusable.

## Acceptance criteria
- D3.1-1 RESIDUAL ENUM IS MECE — mutually exclusive, collectively exhaustive (Rule 24(i)), at ONE
  grain (24(ii)), serving ONE intent (24(iii)), with the stability frame named (24(iv): say which
  values move together under one remedy and which do not).
- D3.1-2 EVERY NON-JOINING ACCOUNT CLASSIFIED against a printed denominator — accounts examined,
  not only accounts that failed to join.
- D3.1-3 U1 ANSWERED WITH file:line @ commit — a vintage-bearing citation. A line citation without
  a vintage is not a citation; it resolves at every vintage, to different code. U1's owner is INSIDE
  this TO (§7 Q1: no Andrew input needed).
- D3.1-4 THE ENUM IS PUBLISHED AS A CONSUMABLE CONTRACT at a stable path, and the report NAMES
  D6/TO-G as a downstream reader so the coupling is visible from both ends.
- D3.1-5 proof instance VALID rc=0 positional: ids D3.1-1..D3.1-5. MEASURED/RULED-class run rows
  only; INFERRED-class expected values are mechanically ineligible.

<proof_of_spec>
  <expected_criteria>D3.1-1,D3.1-2,D3.1-3,D3.1-4,D3.1-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D3_MODELOVERLAY.TO-D3.1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Reporting
COO at spec-drafted and at enum-published; cc CTO (the enum is a cross-package contract). Session
log w/ Compiler Tools section = deliverable.
