<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-DELETE-C449-U7.synthetic-door-input-d2-laptop</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~U7</issued_to>
    <date>2026-10-14</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the act deletes the one version of ONE synthetic stored input in the intake store; nothing reads it (a re-open of it was step D4 of the release-28 sitting, done).
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: RUN-AS-A-READ -- step 2 asks the policy simulator whether YOUR principal may delete this one object version; no IAM change is made by this order.
comp-adversary: RUN -- by reading the dell2 applier's STOP on the same act (an explicit Deny, DenyS3DeletesOnProductionData in cloudops-dell-agent-deploy-policy v7) against this cell; the lens: a delete that matches by prefix or by substring and removes more than the one input, a delete tried through another principal after a refusal, a NoSuchKey read taken from a lagging list. The order selects the key by the FULL 64-hex id, requires exactly one matching key with exactly one version, deletes by VersionId, and reads back both a head-object and a list of versions. It also says: if your principal is denied, STOP; the act then belongs to Andrew's console and nothing is tried through another principal. NOT seen: whether your principal is denied (step 2 reads it).
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R37A_Y.md</decomp_doc> round 37, workstream ZB: the clean-up of the one synthetic input that the release-28 door sitting stored (case D2); carried across boxes as an ORDER by the CTO's ruling (dell2 CTO msg 7604).
<owned_cells>AR-y-307</owned_cells>
</decomp_ref>

  <objective>
    Delete the ONE version of the ONE synthetic stored input of the release-28 door sitting, and nothing else, and read back NoSuchKey; or, if your principal is denied by the policy simulator, STOP at step 2 with nothing changed and report the denial. You change no code and apply nothing.
    **The object:** bucket opal-data-irpt, prefix irpt/49financial/state/normalized_portfolios/, the one key whose name contains the FULL 64-hex 38104be4dc81abe6a67dcb837add8576df86a7cdecc21b08e5de6e33c58be29f (the content-sha256 leaf of input_id portfolio_38104be4dc81abe6a67dcb837add8576df86a7cdecc21b08e5de6e33c58be29f, tenant 49financial). The dell2 applier read it whole on 2026-10-14 ~12:07Z: that prefix holds 11 versions, 0 delete markers, 11 distinct keys; exactly ONE key contains the 64-hex, with exactly ONE version (LastModified 2026-10-14T04:23:53Z, 4586 bytes, IsLatest, not a delete marker); the other 10 keys must stay untouched.
  </objective>

  <context>
    Load /cloud-ops first. **The approval (Andrew, call dell2-20261014T044915Z-c449):** record org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_114xZ_EIGHT_OPEN_CALLS_ANSWERED.md, table row 8, quoted: "dell2 `c449`, the S3 delete of one synthetic stored input | APPROVED | a dell2 CloudOps seat deletes every version of that one named key, reads back NoSuchKey, and closes the row with this file". That wording names a dell2 seat; the dell2 CTO ruled (msg 7598, 7604) that the Dell identities are denied this act on purpose and that the same approved act is carried to a laptop CloudOps seat as this order, and, if the laptop is also denied, it is Andrew's console act. This approval covers THIS ONE VERSION; the release-28 D3 input, the release-29 sitting's objects and every other object are NOT covered. The CTO relay is dell2 CTO msg 7604 (carried by 0.0.0_AB_MSTR~DELL2).
    The dell2 applier's refusal: an explicit Deny `DenyS3DeletesOnProductionData` (s3:DeleteObject* on opal-data-*, no Condition) in policy cloudops-dell-agent-deploy-policy v7. Do NOT look for another principal, a role to assume, a lifecycle rule or a bucket-policy change if yours is denied.
  </context>

  <the_act>
    1. Open the NEVER-2 ledger irpt-c449-delete-u7-20261014 (legs L list, D delete, R read-back) on your box and commit it; read every live worktree's open deploy entries (git worktree list, then ls-tree) and print the denominator: an open entry naming the intake store bucket is a STOP.
    2. THE SIMULATOR FIRST: run simulate-principal-policy for YOUR principal, action s3:DeleteObjectVersion (and s3:DeleteObject), resource arn:aws:s3:::opal-data-irpt/irpt/49financial/state/normalized_portfolios/*. Print the decision and the matched statements. If the decision is not `allowed` (an explicit deny or an implicit deny): STOP. Delete nothing, write org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/irpt_anlreq_c449/C449_DELETE_RESULT.txt with the single line `DENIED <decision> <matched statement id>`, close your ledger as BLOCKED with that reason, and report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 (the act is then Andrew's console act). Do not try another principal.
    3. READ ONLY: list-object-versions on the prefix above, read whole (print the page count and that the listing was not truncated), and select every KEY whose name contains the FULL 64-hex above. Print the key list and, for the selected key, every VersionId with its LastModified, size and delete-marker flag, and the counts as denominators. The selection must equal the object in the objective: exactly 1 key, exactly 1 version, LastModified 2026-10-14T04:23:53Z, 4586 bytes. Any difference (a second key, a second version, a delete marker, another size or date): STOP, delete nothing, report what you found (names and counts only).
    4. Delete: for the one selected key, delete that version by its VersionId, ONE call (no batch-delete over a prefix, no lifecycle rule, no recursive delete). Print the call's result. Do not touch any other key, version or bucket.
    5. Read back: head-object of the key without a VersionId must answer 404/NoSuchKey, and list-object-versions for the exact key (prefix equal to the full key, then keep only the exact match) must return zero versions and zero delete markers; repeat a lagging read in a printed bounded window of 5 minutes. A version still PRESENT after the window is a STOP and a report. Write org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/irpt_anlreq_c449/C449_DELETE_RESULT.txt with ONE line each, exactly: `KEYS_SELECTED 1`, `VERSIONS_BEFORE 1`, `DELETED 1`, `HEAD NoSuchKey`, `VERSIONS_AFTER 0`. No object body, account identifier or name goes into any file, log or message.
    6. Close the ledger and report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 (the path of the result file and its lines). The dell2 issuer closes the open call c449 with Andrew's record; you do not.
  </the_act>

  <bounds>
    Exactly ONE version of ONE key, selected by the full 64-hex input id; no other key, version or bucket, no prefix delete, no lifecycle or policy change, no DynamoDB write, no second input (the D3 input stays). Rollback: none is possible once a version is deleted (the object is synthetic and Andrew approved its removal); a STOP before step 4 changes nothing.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/irpt_anlreq_c449/IRPT_ANLREQ.TO-DELETE-C449-U7.synthetic-door-input-d2-laptop.proof_of_spec.json`.
    <criterion id="C449U7-AC1" cell_refs="AR-y-307">The result file carries either the five lines of a completed delete or the single denial line.<invocation>grep -c -E '^(KEYS_SELECTED 1|VERSIONS_BEFORE 1|DELETED 1|HEAD NoSuchKey|VERSIONS_AFTER 0|DENIED .+)$' org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/irpt_anlreq_c449/C449_DELETE_RESULT.txt</invocation><expect>^(5|1)$</expect></criterion>
    <criterion id="C449U7-AC2" cell_refs="AR-y-307">The ledger irpt-c449-delete-u7-20261014 is closed (CLOSED, or BLOCKED on a denial).<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-c449-delete-u7-20261014_deploy_completion.md</invocation><expect>^\*\*Status:\*\* (CLOSED|BLOCKED)</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a delete order to a tier-2 applier on another box under Andrew's recorded approval of call c449 and the dell2 CTO's ruling (not a worker cell); the cell AR-y-307 is the issuer's, as for TO-DELETE-C449.
