<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-DELETE-C449.synthetic-door-input-d2-aq2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-14</date>
    <status>staged</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the act deletes every version of ONE synthetic stored input in the intake store; nothing reads it (a re-open of it was step D4 of your own sitting, done).
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; step 1 reads your own grant to list and delete versions on the one key as met and stops if it is missing.
comp-adversary: RUN -- by reading DOOR_INPUTS.txt and DOOR_RESULT.txt against this cell; the lens: a delete that matches by prefix or by substring and removes more than the one input, a delete of the latest version only so the older versions stay, a NoSuchKey read taken from a lagging list. The order selects the key by the FULL input id, requires exactly one matching key, deletes version by version by VersionId, and reads back both a head-object and a list of versions. NOT seen: the bucket and key layout of the intake store (you read them in step 1), any other object holding the same input.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R37A_Y.md</decomp_doc> round 37, workstream ZB: the clean-up of the one synthetic input that your sitting stored (D2).
<owned_cells>AR-y-307</owned_cells>
</decomp_ref>

  <objective>
    Delete every version (and any delete marker) of the ONE synthetic stored input your door sitting created for case D2, and nothing else: tenant 49financial, input_id portfolio_38104be4dc81abe6a67dcb837add8576df86a7cdecc21b08e5de6e33c58be29f (your file org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/DOOR_INPUTS.txt). Then read back NoSuchKey and STOP. You change no code and apply nothing.
  </objective>

  <context>
    Load /cloud-ops first. Andrew approved this delete; the record's table row 8 (the CTO's wording of his answer) reads, quoted, in org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_114xZ_EIGHT_OPEN_CALLS_ANSWERED.md: "dell2 `c449`, the S3 delete of one synthetic stored input | APPROVED | a dell2 CloudOps seat deletes every version of that one named key, reads back NoSuchKey, and closes the row with this file". The relay is 1.0.0_SA_CTO~DELL2 msg 7586. The open call is dell2-20261014T044915Z-c449. This approval covers THIS ONE INPUT; the second synthetic input (case D3) and any other object are NOT covered.
  </context>

  <the_act>
    **AMENDMENT 1 (issuer `2.0.0_SA_COO~Y2`, 2026-10-14 ~12:3xZ, after your STOP, msg 7592; relayed ask: laptop CTO msg 109133 via 0.0.0_AB_MSTR~DELL2 msg 7619).** The act of this order moves to the laptop seat `0.7.0_AE_CloudOps~U7` as crossbox order XB-20261014T121648Z-d847 (dell2 CTO msgs 7598, 7604); steps 3 to 5 below are NOT yours to run. ONE act is yours now, and it does not wait for a GO of the staged status: CLOSE your ledger irpt-c449-delete-20261014 because the delete never landed and U7 stops at its step 1 while your entry is OPEN on the intake bucket: `python .tools/deploy_ledger.py close --slug irpt-c449-delete-20261014 --gate-refused "<the AccessDenied line from your delete-object, plus your head-object by VersionId showing the version still present, with the positive control>"`; commit it; then tell 2.0.0_SA_COO~Y2 that it is closed (the issuer tells U7 through 0.0.0_AB_MSTR~DELL2). Gate limb that graded this amendment: none stated (the issuer amends its own staged order). After that this order stays STAGED and is superseded by U7's result.
    1. Open the NEVER-2 ledger irpt-c449-delete-20261014 (legs: L list, D delete, R read-back) and commit it; read every live worktree's open deploy entries (git worktree list, then ls-tree) and print the denominator: an open entry naming the intake store bucket is a STOP. Find the bucket and key of the intake store's stored input from the code (infra/aws/lambda/investor-reporting/intake/uploads.py and the stored-input contract it names; print the lines you read) and from your sitting's record; the store is the one the door writes to, in opal-data-irpt unless the code says otherwise.
    2. READ ONLY first: list-object-versions on the tenant's input prefix and select every KEY whose name contains the FULL input_id above (all 64 hex characters). Print the key list and, for the selected key, every VersionId with its LastModified, size and delete-marker flag, and the version count as the denominator. If the number of selected keys is not exactly 1, STOP: delete nothing, report the keys you found (names and counts only).
    3. Delete: for the one selected key, delete each version and each delete marker by its VersionId, one call per version (no batch-delete over a prefix, no lifecycle rule, no recursive delete). Print each call's result. Do not touch any other key, version or bucket.
    4. Read back: head-object of the key without a VersionId must answer 404/NoSuchKey, and list-object-versions for the exact key (prefix equal to the full key, then keep only the exact match) must return zero versions and zero delete markers; repeat a lagging read in a printed bounded window of 5 minutes. A version still PRESENT after the window is a STOP and a report. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/C449_DELETE_RESULT.txt with ONE line each, exactly: `KEYS_SELECTED 1`, `VERSIONS_BEFORE <n>`, `DELETED <n>`, `HEAD NoSuchKey`, `VERSIONS_AFTER 0`. No object body, account identifier or name goes into any file, log or message.
    5. Close the ledger and report ONCE to 2.0.0_SA_COO~Y2 (path of the result file and its five lines). The issuer closes the open call c449 with Andrew's record; you do not.
  </the_act>

  <bounds>
    Exactly ONE key (selected by the full 64-hex input id) and every version of it; no other key, no prefix delete, no lifecycle change, no other bucket, no DynamoDB write, no second input (the D3 input stays). Rollback: none is possible once a version is deleted (the object is synthetic and Andrew approved its removal); a STOP before step 3 changes nothing.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/IRPT_ANLREQ.TO-DELETE-C449.synthetic-door-input-d2-aq2.proof_of_spec.json`.
    <criterion id="C449-AC1" cell_refs="AR-y-307">The result file carries the five lines: one key selected, the versions before and deleted equal, NoSuchKey on head, zero versions after.<invocation>grep -cE '^(KEYS_SELECTED 1|VERSIONS_BEFORE [0-9]+|DELETED [0-9]+|HEAD NoSuchKey|VERSIONS_AFTER 0)$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/C449_DELETE_RESULT.txt</invocation><expect>^5$</expect></criterion>
    <criterion id="C449-AC2" cell_refs="AR-y-307">The ledger irpt-c449-delete-20261014 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-c449-delete-20261014_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a delete order to a tier-2 applier under Andrew's recorded approval of call c449 (not a worker cell); the cell AR-y-307 is the issuer's, as for TO-EXERCISE-R28b.

<!-- ISSUER NOTE 2026-10-14 (2.0.0_SA_COO~Y2): parked at step 3 by AQ2's STOP (msg 7592): the one delete-object by VersionId was refused AccessDenied, explicit Deny DenyS3DeletesOnProductionData in cloudops-dell-agent-deploy-policy v7. Steps 1 and 2 are done (1 key, 1 version, 0 delete markers). The order is STAGED until 1.0.0_SA_CTO~DELL2 names the principal or path that may delete this one version; nothing is routed around the deny. -->
