<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-DELETE-SYNTH-INTAKE.fwd1-sets-r33-and-run3-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-16</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is exactly 24 named object versions in the intake bucket opal-data-irpt, each fabric-made synthetic or test and listed by key and VersionId in four committed records; no prefix, no listing-driven delete, no other object.
comp-routes: DECLARED-NOT-APPLICABLE -- no route. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; if the operator's own role is refused (AccessDenied) the order STOPS and reports; no policy is edited and no other identity is used.
comp-adversary: RUN -- by reading the CTO's record @c2b2f1e950 (Andrew-direct: synthetic and test files are deletable at any time, by listed key and VersionId, only fabric-made synthetic or test objects, read back absent) and the four records against this cell; the lens: a delete by prefix or by a listing, a key in the list that another seat or a real client wrote, a VersionId that is not the one the record names, a delete marker created instead of a version removed, an object a still-open ledger or a graded run needs, a retry loop on AccessDenied. The order requires each object to be head-read by key AND VersionId first, matched to the record, deleted by that VersionId, and read back absent. NOT seen (blind): whether the operator role may delete versions in this bucket (an earlier delete of c449 was AccessDenied for the dell2 role and was done by the laptop seat); denominator: 24 versions, 4 records.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ37: the delete of FWD-1's synthetic intake objects, on Andrew's standing word.
<owned_cells>AR-y-376</owned_cells>
</decomp_ref>

  <objective>
    Delete the 24 fabric-made synthetic intake objects that FWD-1's probe sets, the release-33 sitting and run 3 wrote, each by its listed key AND VersionId, and read each back absent. Report to 2.0.0_SA_COO~Y2 (cc 1.0.0_SA_CTO~DELL2). NO prefix delete, NO listing-driven delete, NO retry on AccessDenied.
  </objective>

  <context>
    Load /cloud-ops first. Authority: Andrew-direct, relayed by the CTO (msgs 9395 and 9402; record org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261016_134xZ_SYNTHETIC_TEST_DELETES_NEED_NO_CALL_OPAL_TERMINAL_GONE_DELL2.md @c2b2f1e950): "you can delete synthetic and test files any time, i do not need an open call or reserved call for that kind of behavior." Deletes go by listed key and VersionId, only of fabric-made synthetic or test objects, read back absent. THE LISTS (each `OBJ <bucket> <key> <VersionId>` line is one object; the denominator is 24): in org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_fwd1_r3/OBJECTS_WRITTEN_FWD1_R3.txt: the first probe set (the 5 `OBJ ` lines above the first `OBJ_COUNT 5`), the `SET2 OBJ ` lines (5), the `SET3 OBJ ` lines (5) and the `RUN OBJ ` line (1); and in org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r33/OBJECTS_WRITTEN_R33.txt the 8 `OBJ ` lines (release-33 sitting, `normalized_portfolios`). NOT in this order: the 6 objects of org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r29/OBJECTS_WRITTEN_R29.txt (an earlier delete, c449, covered that sitting; do not touch them), window 4 (it wrote 0 objects), and any object not named in the four lines above.
  </context>

  <the_act>
    GO: start at step 1. ANY red before the first delete means NOTHING is deleted: report which read.
    1. Open the NEVER-2 ledger irpt-synth-intake-delete-<YYYYMMDD of today> (one leg per record: P probe-set-1 and SET 2 and SET 3 and RUN, Q release-33) and commit it; read every live worktree's org/critical_paths/.open_deploys/ FIRST (git worktree list, then git -C <wt> ls-tree) and print the denominator: another open entry naming the intake bucket or the 49financial prefix is a STOP.
    2. Build the list: parse the four sets of lines above into one table of (key, VersionId); print the count (must be exactly 24) and the number of distinct keys; a duplicate (key, VersionId) or a count other than 24 is a STOP.
    3. For EACH row: `head-object` by key AND VersionId (print the ContentLength, the ETag and whether it is a delete marker); the object must exist, must not be a delete marker, and its key must start with `irpt/49financial/state/original_holdings/` or `irpt/49financial/state/normalized_portfolios/`; any other state is a STOP for that row, written down, and the other rows go on. Print the number of rows that passed.
    4. Delete each passing row with `delete-object` naming its VersionId (never without `--version-id`, never a key-only delete that would only add a delete marker, never a prefix, never `--recursive`). If the FIRST delete returns AccessDenied, STOP: delete nothing else, write the AccessDenied line and a head-object by VersionId showing the version still present with a positive control (a head of an object that does exist), and report; the issuer routes the act to the laptop seat. No retry, no policy edit, no other identity.
    5. Read back each deleted row with `head-object` by key AND VersionId (must be NoSuchVersion / 404) and `list-object-versions --prefix <the exact key>`: the version is absent and no new delete marker was created for that key by you; print the per-row result and the totals (deleted, still present, failed).
    6. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_synth_delete/A_DELETE_SYNTH.txt with, ONE line each: `DEL <key> <VersionId> ABSENT` for every deleted row and `DEL <key> <VersionId> FAIL <what was read>` otherwise; then `DEL_TOTAL deleted=<n> failed=<m> denominator=24`. Commit with .tools/safe-commit.sh under your author line, close the ledger only when every row reads ABSENT or its failure is written, and report ONCE to 2.0.0_SA_COO~Y2 (cc 1.0.0_SA_CTO~DELL2): "synthetic intake delete closed" with the totals, the output path and the commit.
  </the_act>

  <bounds>
    24 named object versions in opal-data-irpt, deleted by VersionId only. No other object, no prefix, no listing-driven delete, no lifecycle or bucket-policy change, no IAM change, no other identity, no retry on AccessDenied. Not in this order: the r29 sitting's 6 objects, any ticket, request, job row, report or user row, any delete outside the intake bucket. Rollback: none (the objects are synthetic and the version delete is permanent; that is the act).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_synth_delete/IRPT_ANLREQ.TO-DELETE-SYNTH-INTAKE.fwd1-sets-r33-and-run3-ib2.proof_of_spec.json`.
    <criterion id="DEL1-AC1" cell_refs="AR-y-376">Every one of the 24 versions reads absent.<invocation>grep -c -E '^DEL irpt/49financial/state/(original_holdings|normalized_portfolios)/ART-[0-9a-f]{64}/[0-9a-f]{64}\.(csv|json) [A-Za-z0-9._-]+ ABSENT$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_synth_delete/A_DELETE_SYNTH.txt</invocation><expect>^24$</expect></criterion>
    <criterion id="DEL1-AC2" cell_refs="AR-y-376">The total line reads 24 deleted, none failed.<invocation>grep -c -E '^DEL_TOTAL deleted=24 failed=0 denominator=24$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_synth_delete/A_DELETE_SYNTH.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="DEL1-AC3" cell_refs="AR-y-376">The ledger irpt-synth-intake-delete-<date> is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-synth-intake-delete-*_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a DELETE order to a tier-2 applier on Andrew's standing word (CTO record @c2b2f1e950), not a worker cell; the cell AR-y-376 is the issuer's, as for the other IRPT applier orders.
