# TO OPAL_MDPFCLEANUP.TO-5 — POST-KILL ACCEPTANCE ⛔ STAGED

<task_order id="OPAL_MDPFCLEANUP.TO-5" project="OPAL_MDPFCLEANUP">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T17:2xZ</issued>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project OPAL_MDPFCLEANUP, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged — gate: after each kill wave (TO-3 / TO-4)</status>
<priority>Strict sequence position 6 (PRD §4); the project's close evidence</priority>
</task_order>

**PRD:** `docs/architecture/OPAL_MDPFCLEANUP_PRD.md` v1.1 @9f75dcb996 §4 TO-5, verbatim.

## Objective

After each wave: **one full UNATTENDED canonical cycle green** (all three firms T-1 with the
value-leg discipline per TRGALN v1.3/v1.4 — labels + value legs, nothing fresh on a label) + a
**zero-dangling-references sweep** (TF state, comp-kuzu edges, no rule targeting a deleted Lambda,
no orphan alarms) + registry/law truth-up (project JSON, any law lines naming killed resources).

## Acceptance

Per-wave claims: unattended-cycle evidence (scheduled fire stamps, per-firm labels + value legs)
+ the dangling-reference sweep with denominators printed. Project CLOSED-form goes to CTO (RAVC)
on the final wave's PASS.

<proof_of_spec>
<expected_criteria>unattended-cycle-green-per-wave-labels-plus-value-legs; zero-dangling-references-tf-kuzu-rules-alarms; registry-and-law-truth-up; denominators-printed</expected_criteria>
<instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_MDPFCLEANUP/proof_TO-5.json</instance_path>
</proof_of_spec>
