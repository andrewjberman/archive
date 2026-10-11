<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-t1.commentary-store-and-lambda-first-apply-dell2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R1.md</decomp_doc>
<owned_cells>AR-t-12</owned_cells>
<decomp_context>Round 1, workstream ~T: the apply of AR-t-11 + AR-t-12 (with the AR-t-13 store under AMENDMENT 4), drained @77adb5a035. HELD: the GO is a separate message, sent only after IB-pr-391 (the composition reader) is applied and read back.</decomp_context>
</decomp_ref>

  <reassignment>
    AMENDMENT 2 (issuer, 2026-10-09 ~13:3xZ): RELEASED. The composition reader is LIVE under IB-pr-397 (0.7.0_AE_CloudOps~IB2 msg 3355:
    `irpt-commentary-composition-read-lambda` CodeSha256 ZZmWOFSA..., `irpt-commentary-composition-invoke-policy` exists), which is step 0's
    read. Row IRPT_BCKEND-D2-S50 is fixed at @36b0bc0423: the draft store's root log group is removed and the yang-lambda module owns it
    (`log_retention_days = 14`), so step 1 targets no root log group. The pin MUST carry 36b0bc0423
    (`git merge-base --is-ancestor 36b0bc0423 <pin>`); a pin without it half-lands step 1 (ResourceAlreadyExistsException).
  </reassignment>

  <reassignment>
    AMENDMENT 3 (issuer, 2026-10-09 ~15:5xZ): t1 STOPPED at the build (msg 3562). Fixed by TO-AR-t-12 AMENDMENTS 7-8: the draft store's nine
    repo-root files are staged_from members, and the build runs with `BAU_PARITY_SKIP=1` (the seven unregistered siblings in the shared
    source_dir are outside the store's measured import closure; ruling in AMENDMENT 8). The pin MUST carry that drain (named in the GO).
  </reassignment>

  <reassignment>
    AMENDMENT 5 (2026-10-11 ~05:4xZ, by `2.0.0_SA_COO~Y2`, IRPT_ANLREQ's interim driver per 1.0.0_SA_CTO~DELL2 msg 3904; the issuer `2.0.0_SA_COO~T2` now
    drives NFRA_TRNSPT. Numbered 5 because this order's context already uses "AMENDMENT 4" for another document): ONE inserted step, B2, between
    step 4 and step 5 -- a code-only re-apply of the commentary function onto the pull function's zip.
    REPORT TO `2.0.0_SA_COO~Y2` from here on. Row `IRPT_ANLREQ-D2-S23`: steps A2 and B ran at pin `4901eece20` without the zip re-read of CTO msg 3939.
    Pair amendment: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/t1/NEVER_WIDEN_T1_COMMENTARY_CODE_REAPPLY_PAIR_AMENDMENT.md`
    @abbb4ac3ac (blob 6ef85fba67, COO half signed); CTO half AMENDMENT @2287c83ba4 (msg 4192), SIGNED against that blob. Read both in full first.
    STEP B2: from your detached worktree at pin `4901eece20`, `infra/aws/terraform/transcripts`, `-target=aws_lambda_function.commentary`. Keep the
    pin's own built zip (`plVgBIIX`) beside the dist path, untouched, as the rollback source. Add one leg to the open ledger before the apply.
    The CTO's six conditions, verbatim:
    1. **The bytes are the pull function's package, fetched, not rebuilt.** Before the plan: the file at `local.pull_zip`'s path
       hashes to `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=`, and the pull function's live CodeSha256, re-read then, equals it.
       A pull function that moved is a STOP.
    2. **The queue is read before the apply:** `ApproximateNumberOfMessages` and `ApproximateNumberOfMessagesNotVisible` on
       `outlook-global-commentary-draft-analysis-ready-queue`, both recorded. The event-source mapping is Enabled, so a message
       present means the function may already have run on the old bytes: that is recorded with the function's invocation count
       since 05:26:35Z, and it does not stop the act.
    3. **The plan is 0 to add, 1 to change, 0 to destroy;** the one change is `aws_lambda_function.commentary` and its changed
       argument is `source_code_hash` with what follows from it. Anything else is a STOP. The plan text is committed first.
    4. **After:** the commentary function's live CodeSha256 equals the pull's; State Active; LastUpdateStatus Successful; the
       pull function and the mail function unmoved; a targeted re-plan reads 0.
    5. **Branch B is the packet's:** the kept `plVgBIIX` zip re-applied through the same targeted path. No destroy on any branch.
    6. **Not covered:** the mail function, any other resource of the root, any environment variable, IAM statement, queue or
       mapping, a rebuild at any pin.
    The pull function is `teams-global-transcripts-pull-lambda`; the mail function is `outlook-global-transcripts-pull-lambda` (`VGIq85Xx...` at the
    cut). Then step 5 (re-read the simulate on the function as it now stands) and step 6 (the ONE test invoke) run on those bytes; the hold on step 6
    lifts when condition 4 is met.
  </reassignment>

  <objective>
    The FIRST apply of the commentary DRAFT store (IRPT export root) and the commentary Lambda (transcripts root), in the order the pair
    fixes: A (store, policy row PENDING) -> A2 (row ACTIVE + store code rebuilt) -> B (commentary). Report counts and stages only.
  </objective>

  <context>
    The pair binds; read both halves in full first:
    COO half `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/NEVER_WIDEN_IRPT_ANLREQ_COO_HALF_COMMENTARY_STORE_AND_LAMBDA_20261009.md`
    (@20ab65040d + ADDENDUM 1 @1f6a8f453d); CTO half
    `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COMMENTARY_STORE_AND_LAMBDA_FIRST_APPLY_CTO_HALF.md`
    (@5e467d90af + AMENDMENT 1 @f4203149ad). W41-S1 precondition MET @00d37e622f (the built transcripts-pull zip admits analysis_ready;
    negative control refuses). H1 withdrawn (CTO @19c5067e12).
  </context>

  <the_act>
    0. Open a change ledger in org/critical_paths/change_management/ naming the pin (box/dell2 commit you apply from) and each zip's sha256
       (deploy-gate pin rule, MSTR msg 2681). Read back that `irpt-commentary-composition-read-lambda` and
       `irpt-commentary-composition-invoke-policy` EXIST (IB-pr-391 applied). Absent = STOP.
    1. STEP A, `infra/aws/terraform/investor-reporting/export`: safe-apply targeted to the draft-store module (which now owns the function's
       log group, AMENDMENT 2), its role, role policy and `commentary_draft_store_invoke` policy. The plan must show exactly those creates and 0 change / 0 destroy; anything else = STOP.
    2. STEP A2: set `irpt-anlreq-x10-v1` ACTIVE in `infra/logic/registry/reporting_policies.json` with `enforcement_ref` = the full
       40-character hash of the merge carrying the store (read with git rev-parse), a one-row registry commit; rebuild the store zip from that
       commit; re-apply the store function's code only; put the rebuilt zip's sha256 in the ledger. Read the row ACTIVE at the applied pin.
    3. CTO condition: print the transcripts key ARN beside the request_compositions key ARN; they must differ (equal = STOP).
    4. STEP B, `infra/aws/terraform/transcripts`: safe-apply targeted to the `commentary.tf` resources the COO half lists (log group, the five
       queues + two queue policies, role, policy, three attachments, KMS grant, function, event-source mapping). Exact creates only.
    5. CTO condition: simulate as the commentary role -- `dynamodb:GetItem` and `kms:Decrypt` on the IRPT table/key DENIED;
       `lambda:InvokeFunction` on the reader and the store ALLOWED. (A key-policy-only grant reads implicitDeny in the simulator; read the key
       policy where the simulator is blind, as you did on TO-RUN-a17.)
    6. ONE test invoke with a synthetic `analysis_ready` for a 49financial test request; report the stages only (no composition, no text).
    7. Close the ledger. ROLLBACK, if asked: `terraform destroy -target` of the created resources -- a destroy is Andrew's word, never this seat's.
  </the_act>

  <bounds>
    - Only the resources named in the COO half; no other root, key policy or table. No vendor call beyond the ONE test invoke's model call.
    - No content in any file or message. No delete.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
    org/critical_paths/change_management/
    infra/logic/registry/reporting_policies.json
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule; the trigger is I3 (the resident's analysis_ready), not created here.
comp-iam: RUN -- the commentary role's statements read at 77adb5a035 (own policy + two IRPT invoke attachments + transcripts KMS grant; no IRPT S3/KMS/DynamoDB); the store role scoped to one family prefix and the requests table; verified by step 5's simulate.
comp-adversary: RUN -- a wrong apply order (A before the reader, B before A2: steps 0 and 2 gate); a plan wider than the named creates (step 1/4 STOP); a shared key (step 3); a leaked grant (step 5); content in a report (counts and stages only); BLIND: the resident's I3 sender (~G2's AR-g-11), not exercised by the test invoke.
lane: the applier's deliverables, logs, the change ledger, and the one registry row (A2).
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="AR-t-12"><invocation>aws lambda get-function --function-name outlook-global-commentary-draft-lambda --query "Configuration.State"</invocation><expect>"Active"</expect></criterion>
</proof_of_spec>
  AC1's row also states the test invoke's stages, step 5's four simulate verdicts and the ledger path.

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: the ledger path; each step's plan line (creates/changes/destroys); A2's registry commit and rebuilt zip
    sha256; the two key ARNs' inequality; the four simulate verdicts; the test invoke's stages; commit hashes and the measured push state.
    Leave the status flip to the issuer (write the proof_of_spec instance in your deliverables).
  </report>
</task_order>
