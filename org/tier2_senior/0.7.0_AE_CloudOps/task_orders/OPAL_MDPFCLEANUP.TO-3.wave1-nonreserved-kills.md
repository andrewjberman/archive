# TO OPAL_MDPFCLEANUP.TO-3 — WAVE-1 KILLS (non-reserved) ⛔ STAGED

<task_order id="OPAL_MDPFCLEANUP.TO-3" project="OPAL_MDPFCLEANUP">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T17:2xZ</issued>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project OPAL_MDPFCLEANUP, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged — gate: TO-1 authorized set (K1/K2 rows); K3 rows additionally gate on TO-2 acceptance; CTO apply GOs per the charter-symmetry pattern</status>
<priority>Strict sequence position 4 (PRD §4)</priority>
</task_order>

**PRD:** `docs/architecture/OPAL_MDPFCLEANUP_PRD.md` v1.1 @9f75dcb996 §4 TO-3, verbatim.

## Objective

TF-destroys of the RATIFIED rules/schedules/Lambdas/alarms/DLQ — **consumers first, binary last;
one class per apply; expected-rows-only plans; 0-diff + tag each**. Rollback = revert commit within
the same window. Removing alarms is not building them (moratorium untouched). All applies via
`safe-apply`; deploy-completion ledger entries opened/closed per NEVER law.

## Acceptance

Per-kill claims carry the two §7 kill fields: `consumer_exercise` (the test that would have FAILED
were a consumer live) and `rollback` (the same-window revert act). Every apply 0-diff + tagged.
No reserved-category act rides this TO (EC2 stops and S3 deletes are TO-4).

<proof_of_spec>
<expected_criteria>ratified-set-only; consumers-first-binary-last; one-class-per-apply-expected-rows-only; consumer-exercise-per-kill; rollback-act-per-kill; zero-diff-and-tag-each; no-reserved-acts</expected_criteria>
<instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_MDPFCLEANUP/proof_TO-3.json</instance_path>
</proof_of_spec>
