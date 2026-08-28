# TO ETFS_INGEST.TO-10-AE — APPLY THE PRODUCER PACKAGE CARRYING THE ETFCLASSIFIER FOLD

<task_order id="ETFS_INGEST.TO-10-AE" project="ETFS_INGEST">
<id>ETFS_INGEST.TO-10-AE.producer-apply-for-the-etfclassifier-fold</id>
<decomp_ref>workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md @fcdf042972 (CERTIFIED) — **NO NEW CELL.** This TO is the **APPLIED rung** of `INGEST-T3-6` and `INGEST-T5-1`, the same cells `ETFS_INGEST.TO-9-AE` served for the TO-6/TO-8 change. <owned_cells>INGEST-T3-6, INGEST-T5-1</owned_cells></decomp_ref>
<issued_to>`0.7.0_AE_CloudOps~I` — seated 2026-08-28T18:34:42Z by `2.0.0_SA_COO~Z`. Rule 27: 0 open TOs at that lane, and it is the lane that ran `TO-9-AE`, the same project's previous apply. Continuity, not a collision.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T18:3xZ</issued>
<status>pending -- CUT AND SEATED. Time-boxed by a scheduled fire, not by a sovereign word.</status>
</task_order>

<proof_of_spec>
  <criterion id="INGEST-TO10-AC1" cell_refs="INGEST-T3-6"/>
  <criterion id="INGEST-TO10-AC2" cell_refs="INGEST-T3-6, INGEST-T5-1"/>
  <criterion id="INGEST-TO10-AC3" cell_refs="INGEST-T5-1"/>
  <criterion id="INGEST-TO10-AC4" cell_refs="INGEST-T3-6"/>
  <expected_criteria>INGEST-TO10-AC1,INGEST-TO10-AC2,INGEST-TO10-AC3,INGEST-TO10-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ETFS_INGEST.TO-10-AE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 4, firm-tokened `INGEST-TO10-ACn`. Cells: 2, both pre-existing — this is an APPLIED rung, no new cell. **AC3 is EVENT-GATED on the next scheduled fire and cannot close on the first filing**; a 3-of-4 instance is the expected first state, not a failure.</alignment_denominators>
</proof_of_spec>

## WHY THIS EXISTS — MEASURED, NOT INFERRED

```
  etf-positioning-producer   deployed LastModified   2026-08-28T02:43:57Z
  the ETFClassifier fold     committed               b0e1f33471, ~18:3xZ
```
**A package deployed at 02:43:57Z cannot contain an 18:3xZ commit.** So the running bytes do not
carry the GICS decode, and **tomorrow's ~13:00Z fire would serve the OLD truncated labels** while
every source-side artifact says the fix shipped.
⚠ **THIS IS THE SAME SHAPE AS THE D1 GOLD-LAMBDA FINDING EARLIER TODAY** — committing is not
executing, and a source read cannot answer a question about the deployed plane.
`0.4.0_DS_ClientPlatform~Q` named this in its completion report (*"Needs an AE apply of the producer
package, THEN a scheduled fire"*) and correctly did not take it: it is not that lane's.

## NEVER-LAW, RIDING EVERY CRITERION

- **`safe-apply` ONLY.** Bare `terraform apply` is a NEVER.
- **Terraform ONLY.** `aws lambda update-function-code` is a NEVER.
- **Ledger entry OPENS AT START, CLOSES AT COMPLETION** (NEVER#6).
  ⚠ `0.4.0_DS_ClientPlatform~Q` hit a real trap here today: **it chained a close-edit and its commit
  with `;` instead of `&&`, the edit aborted, and the commit published the PRE-EDIT state and
  reported success.** Use `&&`.
- **NEVER#1 IS ALREADY SATISFIED — DO NOT RE-RAISE IT.** Both halves given (`1.0.0_SA_CTO~Z` +
  `2.0.0_SA_COO~Z`) against a measured radius of **59 of 189 rows, 7 labels, display text only**.
  Grouping, rollups and joins key on the 4-digit code and do not move.

## ACCEPTANCE CRITERIA

**AC1 `INGEST-TO10-AC1` — THE DEPLOYED BYTES CARRY THE DECODE.**
Pull the deployed package, extract the classifier module, and show the decode is present. **Prefer
`cmp` against the source at the applied commit** — byte-identity against the BUILD INPUT is Rule 22a's
actual ask and needs no pattern. If you use a grep instead, **carry a POSITIVE CONTROL**, and be aware
that today an arm asserting a string must be ABSENT was unsatisfiable because the fix documented the
defect it removed. ⛔ **A changed `CodeSha256` or an advanced `LastModified` is NOT acceptance** — both
are true of any deploy, including one built from the wrong input.

**AC2 `INGEST-TO10-AC2` — DEPLOYED VIA `safe-apply`, LEDGER OPENED AND CLOSED.**
Plan reviewed before apply; added/changed/destroyed recorded. A `plan` 0-diff is not evidence for AC1.

**AC3 `INGEST-TO10-AC3` — EXERCISED: the first SCHEDULED fire after the apply.**
⚠ **EVENT-GATED — CANNOT CLOSE TODAY.** The producer fires ~13:00Z. On the first scheduled fire after
this apply, the served artifact must show the 7 completed labels, with `industry_group_basis` reading
`inferred-from-truncation` on the changed rows and `observed` retained on rows the decode returned
unchanged.
⛔ **NO AD-HOC RUN TO BEAT THE CLOCK** — it would destroy the discriminator the scheduled run exists to
produce, and an ad-hoc artifact is never production evidence.
⚠ **THE 59-OF-189 FIGURE IS A PREDICTION FROM SIMULATION, NOT A SERVED MEASUREMENT.**
`0.4.0_DS_ClientPlatform~Q` recorded it that way deliberately. **The fire is what says it happened** —
score what the artifact does, do not grade it against the prediction.

**AC4 `INGEST-TO10-AC4` — NO REGRESSION.**
`industry_group` key present on the same row count before and after; **0 rows lose a value; 0 rows
gain or lose the key.** The pre-state to compare against is in that seat's completion report.

## BARRED / REPORTING

⛔ Nothing here stamps `ETFS_INGEST` or D4 closed — Andrew ruled "D4 is done" a READ, not a close order.
⛔ **Andrew ordered the naming-detail traffic STOPPED at 18:24Z.** This TO is the DELIVERY of a decided
thing, not further adjudication of it. **Do not re-open the member, the completions, or the radius.**
RAVC to `2.0.0_SA_COO~Z`, **once**. Push is the integrator's act. Off-task findings: one line to the
surprise channel, and keep working.
