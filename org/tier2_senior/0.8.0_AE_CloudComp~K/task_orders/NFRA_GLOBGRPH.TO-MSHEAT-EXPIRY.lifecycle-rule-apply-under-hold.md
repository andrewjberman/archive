# TO NFRA_GLOBGRPH.TO-MSHEAT-EXPIRY -- the ms-heat-snapshots-expire-60d S3 lifecycle rule under HOLD entry 20260903T1120Z: write the REBUILDABILITY STATEMENT into the entry as measured lines, THEN safe-apply the declared rule under that entry gated by 1.0.0_SA_CTO, acceptance = an UNSCOPED re-plan of shared-infra at 0 add / 0 change / 0 destroy, the entry closed -- or, if the statement cannot be made, REVERT the declaration so DESIRED matches APPLIED. Andrew's ruling IS the acceptance. Nothing else

# pipeline-override: a ONE-ACT change-management order on a project whose register reads COMPLETE (NFRA_GLOBGRPH: dep_stage absent, fabric absent, no ENDPOINT section, no atom decomposition) -- the spec and the acceptance are Andrew's ruling (93638 item 1, "recs approved", record ANDREW_DIRECT_20260903_130xZ_RECS_APPROVED_LIFECYCLE_EXPIRY_CONDITIONAL_AND_TWO_ENDPOINTS_CONFIRMED.md) applied to a HOLD entry that already names the act, its commit and its acceptance; re-opening a closed project through L2-L5 for one deploy act is not what his word asked for. Audited here; the issuer 2.0.0_SA_COO owns this line.

<task_order>
<id>NFRA_GLOBGRPH.TO-MSHEAT-EXPIRY.lifecycle-rule-apply-under-hold</id>
<to_id>NFRA_GLOBGRPH.TO-MSHEAT-EXPIRY</to_id>
<project>NFRA_GLOBGRPH</project>
<issued_to>0.8.0_AE_CloudComp~K</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_date>2026-09-03</issued_date>
<status>complete -- flipped by the issuer 2.0.0_SA_COO 2026-09-03 17:0xZ on 0.8.0_AE_CloudComp~K's report (16:57Z): the scoped apply landed exactly 0/1/0 (@49c49c218f), live reads two rules, the unscoped control 0/10/0 DISCLOSED whole and NONE applied, ledger 20260903T1418Z CLOSED 5/5 and the HOLD carrier CLOSED @327217feba, the stale unscoped tfplan deleted; proof instance VALID 5/5 at the worker and at this seat; 1.0.0_SA_CTO 93812 item (1) agrees the entry closes on disclosure; CVO grade pending, certifier != author. PRIOR: pending -- GO paired at cut. Authority: Andrew-direct ~13:0xZ at the CTO terminal, "recs approved" on the lifecycle card (1.0.0_SA_CTO 93638 item 1); Andrew-direct ~13:1xZ at the MSTR terminal on how the item reached a Tier-2 seat (0.0.0_AB_MSTR 93650: "cut it as an L6 order now with his ruling as the acceptance; nobody addresses the worker directly again") and ~13:2xZ "Mechanism works" (93654, LD-0529). The base seat 0.8.0_AE_CloudComp holds NFRA_COMPEFFICACY (Rule 27), so this act is seated on a FRESH lane; the base seat's measured finding is this order's INPUT, credited below, and its terminal open call is withdrawn by this order's existence.</status>

**AMENDMENT 2 2026-09-03 16:3xZ (issuer, on the worker's control read, row NFRA_GLOBGRPH-S2 @28b9a1e4d6, and Andrew's word "We can let it continue"):** the scoped apply landed exactly 0/1/0 (@49c49c218f evidence; live: two rules) and the UNSCOPED control read 0 add / 10 change / 0 destroy -- the users-table drift plus NINE `aws_apigatewayv2_route` changes (CUSTOM -> NONE, authorizer -> null) the module would strip. No unscoped apply, correctly. MSH-AC4 is therefore graded on: (i) the lifecycle change GONE from the unscoped plan; (ii) the control DISCLOSED whole -- the summary line and every address listed, none applied; (iii) the live lifecycle read of two rules. The ledger's L5 closes on that disclosed control (a control-disagreement recorded, not an apply). The nine route drifts are a FINDING routed by the issuer to 1.0.0_SA_CTO (the shared-infra module's owner); nothing on them is this order's. **AMENDMENT 2026-09-03 16:1xZ (issuer 2.0.0_SA_COO, executing 1.0.0_SA_CTO's GATE RULING 93765 on the worker's STOP, row NFRA_GLOBGRPH-S1 @3d2daa3ffa):** the SAVED UNSCOPED plan read 0 add / 2 change / 0 destroy -- the lifecycle rule AND `aws_dynamodb_table.opal_users_v2` `deletion_protection_enabled` true -> null (live: true; the module declaration lacks the attribute, so an unscoped apply would strip a served users table's delete guard as a passenger). The STOP was correct; nothing applies as saved. THE APPLY IS NOW SCOPED: `safe-apply` on a NEW saved plan produced with `-target=aws_s3_bucket_lifecycle_configuration.global_graph`, the target declared in the ledger entry (45b641343d) BEFORE the plan; the scoped plan must read exactly 0 add / 1 change / 0 destroy on that one address or it is a STOP again. THE ACCEPTANCE IS TWO-SIDED: (i) the UNSCOPED re-plan of shared-infra AFTER the apply reads exactly 0 add / 1 change / 0 destroy and that one change is the `opal_users_v2` deletion-protection drift and NOTHING else (the lifecycle change gone; the users-table drift present and untouched) -- a scoped apply verified by a scoped re-plan is the measured trap, the unscoped re-plan is the control; (ii) the live `get-bucket-lifecycle-configuration` reads exactly two rules (`abort-incomplete-mpu-7d` unchanged; `ms-heat-snapshots-expire-60d` Enabled, prefix `warehouse/ms_heat/snapshots/`, 60 d). MSH-AC3 and MSH-AC4 below read with this amendment. The users-table drift is remedied by the SEPARATE order NFRA_GLOBGRPH.TO-USERS-DELPROT (same seat), after which the unscoped re-plan reads 0/0/0; the two orders land in either sequence, each with its own unscoped read. The CTO's GATE GO 93751 stands for the scoped shape; no second gate message is needed.


**Directive:** none on the register (NFRA_GLOBGRPH is a COMPLETE flat project; this is change management on its infra) · **Fabric:** laptop (the one where `safe-apply` and the shared-infra state live) · **PRD:** `docs/architecture/NFRA_GLOBGRPH_PRD.md` (2026-06-08; READ for context only -- this order changes no spec) · **The carrier:** `org/critical_paths/change_management/20260903T1120Z_shared-infra-ms-heat-snapshots-expire-60d_hold.md` (the HOLD entry; opened 11:20Z by the base seat on 1.0.0_SA_CTO's decision 93528) · **Lane:** the HOLD entry, `infra/aws/terraform/shared-infra/s3.tf`, a deploy-ledger entry under `org/critical_paths/.open_deploys/`, this lane's deliverables (lanes measured at cut: 5 of 5 admitted). **Rule 27 seating:** `0.8.0_AE_CloudComp~K` holds THIS act only.

---

## THE FACT (from the HOLD entry, verified there against the declaring commit)

`infra/aws/terraform/shared-infra` at its committed state plans **0 add / 1 change / 0 destroy**: `aws_s3_bucket_lifecycle_configuration.global_graph`
would gain rule `ms-heat-snapshots-expire-60d` (prefix `warehouse/ms_heat/snapshots/`, `status = Enabled`, `expiration { days = 60 }`),
declared @`4cd024c5c6` (2026-07-15, `0.8.0_AE_CloudComp~Z`) and never applied (or applied and changed out of band -- the tree cannot
tell; NO live `get-bucket-lifecycle-configuration` read has been taken). The pre-existing rule `abort-incomplete-mpu-7d` is untouched
either way. Every shared-infra apply since 2026-08-19 has been SCOPED AWAY from this resource. An `expiration` rule DELETES objects, so
it took Andrew's word -- which has now been given, CONDITIONALLY.

## ANDREW'S RULING, QUOTED (1.0.0_SA_CTO 93638 item 1, on his "recs approved")

> the ms-heat-snapshots 60-day expiry APPLIES once its owner states IN WRITING that the snapshots are rebuildable -- under the HOLD
> entry @c5dea0f11c through safe-apply, unscoped re-plan 0/0/0 as acceptance; reverted if they are not.
> ... the owner writes the rebuildability statement into the HOLD entry -- what produces the snapshots, what rebuilds them, from what --
> as a measured line, not a belief; THEN the owner applies the rule under that entry through safe-apply (the entry moves from HOLD to
> the ordinary open-then-closed shape), and the acceptance is an UNSCOPED re-plan of shared-infra reading 0 add / 0 change / 0 destroy.
> If the statement cannot be made -- the snapshots are NOT rebuildable -- the owner REVERTS the declaration instead, so DESIRED matches
> APPLIED, and the entry closes on that. Nothing is applied before the statement exists; every shared-infra apply stays scoped away from
> the rule until the entry closes either way. 1.0.0_SA_CTO gates the apply as always.

## THE MEASURED INPUT (the base seat's finding, credited; RE-VERIFY it at source before writing the statement -- it is an input, not the statement)

`org/modules/heatmap/ms_heat_index.py` recomputes the whole index from the live graph on every run, and its 2026-07-15 docstring names
the 60-day lifecycle as the intended retention; the append-only Iceberg table `ms_heat_snap` in `infra/aws/globgrph/snap_store.py`
preserves the day-over-day history. If both read true at source, the snapshots under `warehouse/ms_heat/snapshots/` are REBUILDABLE
(the index from the live graph; the history from the Iceberg table) and the statement can be made. If either does not read true, the
statement cannot be made and the act is the REVERT.

## DELIVERABLE -- in this order

1. **THE STATEMENT, written into the HOLD entry as measured lines** (a new section "REBUILDABILITY STATEMENT (Andrew's condition)"):
   what produces the snapshots (file:line of the writer, the run that writes them, the prefix), what rebuilds them and from what
   (file:line of the recompute path; the Iceberg table's name, location and its append-only property read from its definition), each
   line carrying the instrument it was read with (`comp-read`, a live `s3api list-objects-v2` of the prefix with its denominator, a read
   of the table's metadata) -- never a belief, never "per 93650". State the loss surface honestly: what is NOT rebuildable if anything
   (e.g. a snapshot whose source graph vintage is gone), and whether that changes the answer.
2. **IF THE STATEMENT CAN BE MADE:** open a deploy-ledger entry (`deploy_ledger.py open --slug shared-infra-ms-heat-snapshots-expire-60d
   ...`) at deploy-START with legs: verify (the live `get-bucket-lifecycle-configuration` read BEFORE the apply, so "never applied" vs
   "changed out of band" is finally known), git (the ledger commit), verify (the safe-apply output captured to a FILE, exactly
   `0 added, 1 changed, 0 destroyed` on ONE address), verify (live read-back AFTER: the rule present with prefix / status / 60 days and
   `abort-incomplete-mpu-7d` untouched), verify (the UNSCOPED re-plan of shared-infra reading 0 add / 0 change / 0 destroy -- the
   acceptance; a scoped re-plan is not it). Then, WITH 1.0.0_SA_CTO's GATE (message the CTO with the statement + the pre-read and wait
   for the go -- the one message this order permits to a Tier-1 seat, and it cites this order), `safe-apply` the rule (never bare
   `terraform apply`), close every leg with its proof, `close` the entry, and mark the HOLD entry's checklist and state CLOSED citing the
   ledger entry.
3. **IF THE STATEMENT CANNOT BE MADE:** revert the declaration in `s3.tf` (the rule block removed; `abort-incomplete-mpu-7d` untouched)
   through safe-commit, then the same ledger shape with the unscoped re-plan at 0/0/0 as the acceptance from the other direction; the
   HOLD entry closes on that, stating why the snapshots are not rebuildable.
4. **THE REPORT** to `2.0.0_SA_COO` with the statement's lines, the pre-read and post-read, the apply triple, the re-plan, the ledger's
   closed legs and push state MEASURED; the proof instance at
   `org/tier2_senior/0.8.0_AE_CloudComp~K/deliverables/NFRA_GLOBGRPH.TO-MSHEAT-EXPIRY_PROOF_OF_SPEC.json`.

## ACCEPTANCE -- criterion ids minted at cut

<criterion id="MSH-AC1" cell_refs="HOLD-20260903T1120Z"/> `MSH-AC1` -- THE STATEMENT: the HOLD entry carries the rebuildability statement as measured lines with their instruments (producer, rebuild path, source, loss surface), or the measured reason it cannot be made; nothing applied before it exists (the ledger entry's opened_at is later than the statement's commit).
<criterion id="MSH-AC2" cell_refs="HOLD-20260903T1120Z"/> `MSH-AC2` -- THE PRE-READ: a live `get-bucket-lifecycle-configuration` read BEFORE any act, quoted, settling "never applied" vs "changed out of band".
<criterion id="MSH-AC3" cell_refs="HOLD-20260903T1120Z"/> `MSH-AC3` -- THE ACT UNDER THE LEDGER, GATED: 1.0.0_SA_CTO's go quoted; `safe-apply` (never bare apply) on the SAVED plan produced with `-target=aws_s3_bucket_lifecycle_configuration.global_graph` (the target declared in the ledger entry first; AMENDMENT 16:1xZ), the output captured to a file reading exactly 0 added / 1 changed / 0 destroyed on ONE address (apply path) -- or the revert commit (revert path); the live read-back after, with `abort-incomplete-mpu-7d` untouched.
<criterion id="MSH-AC4" cell_refs="HOLD-20260903T1120Z"/> `MSH-AC4` -- THE ACCEPTANCE (AMENDED 16:1xZ per CTO 93765): an UNSCOPED re-plan of `infra/aws/terraform/shared-infra` AFTER the scoped apply reading exactly 0 add / 1 change / 0 destroy where the one change is `aws_dynamodb_table.opal_users_v2` `deletion_protection_enabled` true -> null and NOTHING else, quoted (0/0/0 once NFRA_GLOBGRPH.TO-USERS-DELPROT has landed), plus the live lifecycle read of exactly two rules; the deploy-ledger entry closed with every leg's proof; the HOLD entry's checklist complete and its state CLOSED citing the ledger entry.
<criterion id="MSH-AC5" cell_refs="HOLD-20260903T1120Z"/> `MSH-AC5` -- push state MEASURED at report; the proof instance VALID (`.tools/proof-of-spec-check.py`); the status flip on this flat-root face is the issuer's on the report; no message to any seat other than the issuer and the one gated message to 1.0.0_SA_CTO citing this order.

<expected_criteria>MSH-AC1, MSH-AC2, MSH-AC3, MSH-AC4, MSH-AC5</expected_criteria>

## BOUNDS

- **ONE act.** No other shared-infra resource changes; every other pending change stays scoped away exactly as the HOLD entry says. No new sensor, alarm or monitor. No S3 object is deleted BY THIS SEAT -- the rule, once applied, is AWS's act on its own schedule, and the statement is what makes that acceptable.
- **`safe-apply` only; never bare `terraform apply`; a saved plan file consumed by the apply; the apply's address list printed.** A triple other than 0/1/0 on the apply path is a STOP with the output pasted, no retry.
- **The gate is real:** 1.0.0_SA_CTO gates the apply; this lane does not proceed to the apply on its own reading of the statement.
- **No investigation beyond this act; no open call at any terminal.** A question is one line to the issuer `2.0.0_SA_COO`; a spec-vs-world divergence is a ROW in `org/surprise_channel/NFRA_GLOBGRPH/INVESTIGATION_v1.md` (create it if absent, lane ANY; surfaced_by = this seat) then keep working.
- **Certifier != author.**

**PUSH (standing law carried onto this CODEX seat's face, 0.0.0_AB_MSTR 93721 on 2.0.0_SA_COO~A's finding 93715, 2026-09-03 15:0xZ):** a shared branch (CLOUD / DEV / PROD / main / SITEZ) is pushed ONLY by `0.0.0_AB_MSTR` or `0.0.0_AB_MSTR~Z`, and only on Andrew's word while he is at the terminal (LD-0367/0368, LD-0522). This seat COMMITS and states its push state as LOCAL; it NEVER runs `git push` on any branch. A Codex runtime carries no Claude hook and no memory of this rule -- this line is the carrier.

<decomp_ref>
<decomp_doc>org/critical_paths/change_management/20260903T1120Z_shared-infra-ms-heat-snapshots-expire-60d_hold.md</decomp_doc> @c5dea0f11c (the HOLD entry is the carrier of record for this act; NFRA_GLOBGRPH has no atom decomposition -- the pipeline-override line above says so and is audited).
<owned_cells>HOLD-20260903T1120Z</owned_cells>
</decomp_ref>

<preflight>
comp-schedule: RUN -- GATES ARMED 21 (read 09:27Z); the HOLD entry itself is the armed gate on this surface (C2 deploy-ledger / the change_management sweep) and this order is its discharge path; no other armed gate names shared-infra's lifecycle resource.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM principal, policy or grant changes; the act is an S3 lifecycle rule on an existing bucket under the seat's standing role; the lens has an empty population at this subject grain.
comp-adversary: RUN -- rc 0 at read-vintage @789c0bc9c5 (2026-09-03T13:32:29Z); 2/2 cited commits VERIFIED, 0 UNVERIFIABLE; cited-path vintage 7 attempted / 5 stable / 2 flagged (the flagged paths are this order's own outputs, GONE by construction at cut); --no-packet (stage 4 pointers only, the caller's choice).
</preflight>

<proof_of_spec>
Criterion ids minted at cut by the issuer: `MSH-AC1`..`MSH-AC5`. The ASSIGNEE fills a `PROOF_OF_SPEC.schema.json` instance at
`org/tier2_senior/0.8.0_AE_CloudComp~K/deliverables/NFRA_GLOBGRPH.TO-MSHEAT-EXPIRY_PROOF_OF_SPEC.json` and validates it BEFORE reporting.
MSH-AC2's pre-read and MSH-AC4's unscoped re-plan are the controls that must be able to FAIL.
</proof_of_spec>

<compiler_tools_mandate>
BEFORE WRITE: `comp-read org/modules/heatmap/ms_heat_index.py --for "what it reads, what it writes, and what its docstring says about retention"`; `comp-read infra/aws/globgrph/snap_store.py --for "the ms_heat_snap table: append-only or not, where it lives"`; `comp-read infra/aws/terraform/shared-infra/s3.tf --for "the global_graph lifecycle configuration and every rule on it"`; the live pre-read via the `.tools/aws` shim. BEFORE THE APPLY: `safe-apply` with a saved plan; the CTO's go. AFTER: the unscoped re-plan; the live read-back.
</compiler_tools_mandate>

**DELIVERABLE REPORT:** to `2.0.0_SA_COO` only. GO = this TO + the dispatch message.
</task_order>
