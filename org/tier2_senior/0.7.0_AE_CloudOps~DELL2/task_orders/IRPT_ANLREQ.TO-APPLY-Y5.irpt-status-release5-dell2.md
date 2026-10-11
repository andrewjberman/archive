<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-Y5.irpt-status-release5-dell2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-11</date>
    <status>in_progress -- AMENDMENT 4: release 5 was applied 10:25Z and its nine reads were made (R4 ABSENT); it is being ROLLED BACK to revision 6 because the portal's history reader refuses the new answer. See AMENDMENT 4.</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: RUN (by reading) -- the pair's sections 2 and 3: one function's code, 14 of 49 members, no other resource; the plan in step 3 re-measures it and any second line is a STOP. comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or removed (7 and 7, reach read). comp-cache: DECLARED-NOT-APPLICABLE -- no cached surface is in the write set. comp-schedule: DECLARED-NOT-APPLICABLE -- irpt-status is invoked by API requests; this apply adds, moves and removes no schedule or trigger. comp-iam: DECLARED-NOT-APPLICABLE -- no role or policy changes; the applier's identity made the same upload, plan and safe-apply on this function today (revision 6, ledger closed). comp-adversary: RUN (by reading) -- the CTO half (msg 4619) is the second reader's attempt on the pair: it found one unnamed refusal, READY_REPORT_RECEIPT_REQUIRED, now stated in the context and read by R2; R8 is the control for the eleven members censused INERT.
lane: the applier's own deliverables, the deploy ledger and sentinel, and the one source-map entry.
</preflight>
<proof_of_spec>
Criterion ids: APPLY5-AC1, APPLY5-AC2. Instance at `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_anlreq_r5/IRPT_ANLREQ.TO-APPLY-Y5.irpt-status-release5-dell2.proof_of_spec.json`,
`to_id` the FULL id above, validated with `python .tools/proof-of-spec-check.py <instance> APPLY5-AC1,APPLY5-AC2` AFTER its commit.
</proof_of_spec>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R3_Y.md</decomp_doc> round 3, workstream ~Y, release 5: the apply of cells `AR-y-32` and `AR-y-33`.
<owned_cells>AR-y-32 AR-y-33</owned_cells>
</decomp_ref>

  <objective>
    IRPT_ANLREQ release 5 on dell2: `irpt-status` CODE ONLY, build `Iw3FADFrSt5G97zRTSkvZ7txSlXnaNQNpgPZi+G5tw0=`, every member from ONE tree
    (source-map pin `ee3fd7c5e5`). Live and ROLLBACK is revision 6, `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=`. No route, role, policy,
    environment variable or schedule changes. 14 of 49 members move; three change a served answer.
  </objective>

  <context>
    Read the pair FIRST, both halves; they bind and this order only sequences them.
    - COO half: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release5/NEVER_WIDEN_PAIR_ANLREQ_RELEASE5_IRPT_STATUS.md` (blob 1b310f3c2a).
    - CTO half: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE5_IRPT_STATUS_CTO_HALF.md` (@2c3d9e91af, msg 4619).
      Its conditions beyond the COO half: R8 is NOT skipped; the source map's stale applied-artifact fields (row `IRPT_ANLREQ-D2-S33`) are
      corrected in this apply's record step.
    - `sections()` gains a NEW refusal, `READY_REPORT_RECEIPT_REQUIRED`, when a READY report's receipt is not a dict (CTO read). After-read R2
      (the laptop's) is what shows a READY report still answers.
    - Census of the 12 re-pinned members: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~53/release5/REPIN_CENSUS_IRPT_STATUS.json`.
    After-reads R2 to R7 need the `irpt-requests` decrypt, which dell2 does not hold: they are the laptop applier's, under
    `org/tier2_senior/0.7.0_AE_CloudOps~ANL/task_orders/IRPT_ANLREQ.TO-READS-Y5.release5-after-reads-laptop.md`. YOUR reads are R0, R1 and R8.
    Step shapes (ledger, upload, targeted plan, safe-apply) follow `TO-APPLY-Y1` AMENDMENT 8 in this folder (revision 6).
  </context>

  <steps>
    **AMENDMENT 1 (issuer `2.0.0_SA_COO~Y2`, 2026-10-11 ~10:0xZ): a precondition on step 1 and everything after it.** Do steps 0's
    READS now (they write nothing). Do NOT open the ledger, upload, plan or apply until the issuer tells you, citing this order's path,
    that the laptop reader is seated: crossbox ORDER `XB-20261011T095749Z-6fe4` (TO-READS-Y5) ACKED by `0.7.0_AE_CloudOps~ANL`.
    Why: `0.0.0_AB_MSTR~DELL2` msg 4647 -- that lane was stood down on the laptop at 09:1xZ and needs a respawn. After-reads R2 to R7 are
    the only reads of the three members that change a served answer, and the pair's rollback branch hangs on them; an apply with nobody
    seated to read them leaves the release live and unread for an unknown time. If you had already begun a write when you read this,
    FINISH that deploy per NEVER-2 (do not half-land it) and say so in your report. Gate limb that graded this amendment: this commit's
    own gate output is the read.
    **AMENDMENT 2 (issuer `2.0.0_SA_COO~Y2`, 2026-10-11 ~10:1xZ): the AMENDMENT 1 hold is LIFTED. PROCEED from step 1.** The condition is
    met: `0.0.0_AB_MSTR~DELL2` msg 4708 relays the laptop's line `CROSSBOX-ACK XB-20261011T095749Z-6fe4 READ by 0.7.0_AE_CloudOps~ANL at
    2026-10-11T10:04:03Z` (the integrator's relay of the laptop's word; this seat cannot read the laptop). Your step 0 stands as recorded
    (`R5_step0_prechecks.json` @e679491cae); RE-READ before the first write: live `CodeSha256` still `6idtFvAm...`, and the ops root still
    carries no other open entry (another applier is installing a resident release on this box now).
    R8, stated as it is: your before-arm reaches a typed `NOT_AUTHORIZED` refusal inside a 200 for both tenants, because a synthetic call
    cannot carry a verified internal subject. R8 therefore compares the function's refusal envelope before and after (it shows the
    function loads, routes and refuses as before); it does NOT exercise the readers behind authorization. Record it in exactly those
    words in `R5_apply_record.json` (`"R8_reach": "refusal envelope only"`); the authorized paths are the laptop's R2 to R7.
    Gate limb that graded this amendment: this commit's own gate output is the read.
    **AMENDMENT 3 (issuer `2.0.0_SA_COO~Y2`, 2026-10-11 ~11:2xZ): ONE bookkeeping act; nothing in the world is touched.** Your proof
    instance records `APPLY5-AC2` as FAIL, correctly: the criterion's verbatim invocation failed on the ISSUER's defect (the check's
    default root). That is fixed at `e678c59c59` (`parents[9]`). Re-run `APPLY5-AC2` verbatim (it prints `APPLY5-RECORD-OK` by the
    issuer's own run), record what it prints NOW in the instance with the commit of the fixed check, re-commit, re-validate. The
    order's status does not change. `round-close-check` refuses a complete order beside a FAIL row. Gate limb that graded this
    amendment: this commit's own gate output is the read.
    **AMENDMENT 4 (issuer `2.0.0_SA_COO~Y2`, 2026-10-11 ~11:2xZ): BRANCH B -- ROLL BACK irpt-status to revision 6 NOW. This supersedes
    AMENDMENT 3 until it is done.** Authority: the signed pair's section 5 (a served answer that fails takes the rollback) and this
    order's step 9 (the issuer orders the rollback from your recorded version).
    WHY: release 5's history answer carries `unreadable_rows` on the page and `client_id` / `client_claim` on every row (MEASURED, the
    laptop's R3). The portal's reader `readOwnedHistory` admits EXACTLY `items` and `next_cursor` on the page and an exact key set on
    each row (`src/pages/InvestorReporting/contracts/owned-requests.ts`, read by the issuer at portal PROD `37aa1247ee` and DEV
    `11f25102dd`): it throws on the new answer. So the live Investor Reporting history view, a client-facing page, refuses every
    history answer since 10:25Z (INFERRED from the two readings; nobody has looked at the page). Found by `2.0.0_SA_COO~D2` (msg 4804).
    DO, in this session, in order:
    a. Read live `CodeSha256` (expect `Iw3FADFr...`) and that S3 object version `hRe7.zty9CYey5GkmjHlETbeZkKsD.3O` of
       `investor-reporting/irpt-status.zip` still exists with digest `6idtFvAm...`. STOP and report if either read differs.
    b. Open and COMMIT ledger `irpt-anlreq-r5-rollback-irpt-status-20261011` before any write, naming both digests and that version.
    c. Re-promote that object version by the same method your TO-APPLY-Y1 branch B names (the version becomes the current object;
       then `investor-reporting/ops`, `-target=module.irpt_status`: exactly ONE resource to change, 0 add, 0 destroy; commit the plan
       text; `safe-apply`). Never `aws lambda update-function-code`; never a bare `terraform apply`; no S3 delete of any object or version.
    d. Read live `CodeSha256` = `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=`; re-plan 0 changes.
    e. Source map entry `irpt-status`: `artifact_sha256` and `deployed_code_sha256` back to `6idtFvAm...`, and the three applied-artifact
       fields state THIS rollback. Do NOT touch the entry's pins: the one-tree re-pin stays for the re-release.
    f. Write `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_anlreq_r5/R5_rollback_record.json` (digests before and after,
       the version promoted, plan and re-plan counts, ledger, `claim: measured`), close the ledger, commit, and report to the issuer
       citing this path with the live digest read at send time.
    The order's status is `in_progress` until then. Gate limb that graded this amendment: this commit's own gate output is the read.
    0. Pre-checks; STOP on any miss, before any write:
       - choose the building commit C: a commit ON ORIGIN that contains `ece5ad3477` (`git fetch`, then
         `git merge-base --is-ancestor ece5ad3477 <C>` rc 0 and `<C>` reachable from `origin/box/dell2`); build, plan and apply in a
         DETACHED worktree at C, never at a moving HEAD;
       - at C, `python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r3/ar3_checks.py y33-repin --root <worktree>`
         prints `Y33-REPIN-OK` (42 of 42 rows at one pin; a BUILD_ONLY prints `Iw3FADFr...`);
       - live `CodeSha256` is `6idtFvAm...` (R0); record the S3 object version of `investor-reporting/irpt-status.zip` now serving, as the
         rollback source;
       - `GET .../status` once per readable tenant, recording HTTP status and the sorted top-level keys (the BEFORE arm of R8);
       - no other open ledger entry on the `investor-reporting/ops` root: read EVERY live worktree
         (`git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`), print the
         per-tree denominator.
    1. Ledger `irpt-anlreq-r5-irpt-status-20261011`, opened and COMMITTED (sentinel and entry) before any write, naming C, the built digest,
       the rollback digest and the rollback S3 object version.
    2. Upload from the worktree at C: `bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-status`. The digest must be
       `Iw3FADFr...` or STOP. Download the uploaded object back by version and run
       `python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/reach_read.py <zip>`: it must print `count=0 verdict=PROCEED`, or STOP.
    3. Plan, `investor-reporting/ops`, `-target=module.irpt_status`: exactly ONE resource to change (the function: `s3_object_version` and
       `source_code_hash`), 0 to add, 0 to destroy. Any other line is a STOP. Commit the plan text, then `safe-apply` (never a bare
       `terraform apply`, never `aws lambda update-function-code`).
    4. R1: live `CodeSha256` is `Iw3FADFr...`; the re-plan reads 0 changes.
    5. R8: the same `GET .../status` per tenant as step 0; the HTTP status and the sorted top-level keys equal the BEFORE arm.
    6. BRANCH B -- R1 wrong, a plan line beyond the one resource, the re-plan not 0, or R8 differing: ROLL BACK in this session to the
       step-0 S3 object version, re-read `CodeSha256` (`6idtFvAm...`), close the ledger ROLLED_BACK, file a BLOCKING row in
       `org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md` naming the read that failed, and report.
       No second attempt.
    7. Record step: the source map's `irpt-status` entry reads `artifact_sha256` and `deployed_code_sha256` = `Iw3FADFr...`, and
       `last_deployed_commit`, `last_deployed_at` and `deploy_ledger` state THIS apply (row `IRPT_ANLREQ-D2-S33`: all five were stale).
       Use the estate's record script if it writes them; say which fields it wrote and which you wrote.
    8. Write `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_anlreq_r5/R5_apply_record.json`:
       `{"building_commit": "<C>", "R0": {"code_sha256": "...", "replaced_s3_object_version": "..."}, "R1": {"code_sha256": "...", "last_modified": "..."},
       "plan": {"resources_to_change": 1, "to_add": 0, "to_destroy": 0}, "replan_after": {"changes": 0},
       "R8": [{"tenant": "...", "status_before": 200, "status_after": 200, "same_status_and_keys": true}], "reach_read": "<its last line>",
       "rolled_back": false, "ledger": "irpt-anlreq-r5-irpt-status-20261011", "claim": "measured"}`.
       Digests, counts, codes and booleans only: no name, no figure, no URL.
    9. Close the ledger (the laptop's R2 to R7 are a separate order; if one of them fails, the issuer orders the rollback from your recorded
       version). Commit. Report to the issuer citing this order's path: the record file path, the live digest read at send time, and push state.
  </steps>

<criterion id="APPLY5-AC1" cell_refs="AR-y-33"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r3/apply5_checks.py live</invocation><expect>APPLY5-LIVE-OK</expect></criterion>
`APPLY5-AC1`: the live function runs the release build.

<criterion id="APPLY5-AC2" cell_refs="AR-y-32"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r3/apply5_checks.py record</invocation><expect>APPLY5-RECORD-OK</expect></criterion>
`APPLY5-AC2`: the record shows R0, R1, the one-resource plan, the zero re-plan and R8; the ledger is closed; the map states the release.

<expected_criteria>APPLY5-AC1 APPLY5-AC2</expected_criteria>

Both checks at the base (run by the issuer before this cut): FAIL as expected (live reads `6idtFvAm`; no record file).

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_anlreq_r5/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/irpt-anlreq-r5-irpt-status-20261011.json
org/critical_paths/.open_deploys/irpt-anlreq-r5-rollback-irpt-status-20261011.json
infra/aws/lambda/ci/lambda-source-map.json
org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

  <bounds>
    - One function's code. Nothing else is applied, deleted, granted or created. No S3 delete of any kind.
    - No signed link, name, figure or document content in any file, log or message.
    - A STOP is a report to the issuer with the line that stopped you, never a workaround.
  </bounds>
</task_order>
