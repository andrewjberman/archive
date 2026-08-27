# TO NFRA_TFSGLINT.CBD-PAIR — plan-time lint: new/changed aws_security_group without create_before_destroy beside a persistent aws_instance (Andrew-approved ~1537Z)

<task_order id="NFRA_TFSGLINT.CBD-PAIR" project="NFRA_TFSGLINT">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:55Z</issued>
<dated>2026-08-24 — behind your full 49F push stack (fixture -> TO-4 -> P2 -> P4 IAM -> P5 opens 08-23). Not urgent; dated so it does not evaporate.</dated>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "NFRA_TFSGLINT" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: pending -- GO 165431Z @3bc88957c8; dated 08-24, sequenced behind the full 49F stack (fixture -> TO-4 -> P2 -> P4 -> P5)</status>
<priority>P3 — closes the 08-15 class (TF plan is END-STATE, not PATH: replacement ORDER + in-place stop/start invisible in plan rows; an SG replace beside a live instance)</priority>
<authority>Andrew-direct 2026-08-18 ~1537Z at the CTO terminal (verbatim: fourth section of org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260818_ALL_RECS_APPROVED_49F_END_TO_END_PUSH_AND_MDPF_UNUSED_DELETE.md): YOUR banked lint proposal APPROVED — deny new aws_security_group without create_before_destroy beside a persistent aws_instance, audited override. CTO gates the lint text (their routing note 164931Z). This TO carries the explicit Andrew word the no-new-gates rule requires — cite it in the lint's header.</authority>
</task_order>

## Objective
A plan-time check in the `safe-apply` path that DENIES when the plan contains BOTH (a) a new or
replaced `aws_security_group` lacking `create_before_destroy` AND (b) a persistent `aws_instance`
in the same plan — with an audited inline override marker per the house pattern (never a silent
bypass). Fires on the PAIR only; an SG change with no live instance beside it passes untouched.

## Compiler tools (three-phase)
Phase 1: `comp-blast` on safe-apply's existing check chain (do not fork a second entrypoint — rung 2
of the build ladder: extend the existing HALTGT/check stage). Phase 2: commit-gate. Phase 3: the
exercise matrix below IS phase 3.

## Cross-domain coordination
- shared_resource: `.tools/safe-apply.sh` — the never-rules-gate + HALTGT live there; MCP CTO with
  the lint text BEFORE landing (their gate); MCP COO at landed.

## Acceptance criteria
- SG-1 FIRES ON THE PAIR: a fixture plan with (new SG, no CBD, persistent aws_instance) → DENY, the
  message naming both members and the override marker syntax.
- SG-2 PASSES THE NON-PAIR, both directions: (SG-no-CBD, NO instance) → pass; (SG WITH CBD, instance)
  → pass. Three fixture plans minimum, results printed.
- SG-3 OVERRIDE AUDITED: the inline marker permits the apply AND lands an audit line (file + reason),
  exercised once in a fixture.
- SG-4 PLAN-TIME ONLY: zero new TF resources, zero AWS calls — the lint reads the plan artifact; no
  alarms/notifications (moratorium).
- SG-5 proof instance VALID rc=0 positional: ids SG-1,SG-2,SG-3,SG-4,SG-5.

<proof_of_spec>
  <expected_criteria>SG-1,SG-2,SG-3,SG-4,SG-5</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_TFSGLINT.CBD-PAIR_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- Do not widen the deny beyond the approved pair (no generic SG lint — the approval is the pair).
- Do not let this precede any 49F push row at your seat.

## Reporting
COO (cc CTO gate, MSTR) at lint-text-agreed and at landed with the fixture matrix. Surprise channel:
one banked line to COO. Session log with Compiler Tools section = deliverable.
