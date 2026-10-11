<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-APPLY-R3-rf2.creator-records-report-code-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>3</round>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R3.md</decomp_doc> (round 3, ADDENDUM 2): cell `R3-rf-2`, the apply of `R3-rf-1` (drained @8ef21584f8).
<owned_cells>R3-rf-2</owned_cells>
</decomp_ref>

  <objective>
    Deploy the code of `opal-ticket-api` at box/dell2 `8ef21584f8` (`infra/aws/lambda/ticket_center/lambda_function.py` sha256 hex
    `dc0cd973c61f4b037e7181f4675ec8ffe2ec68414cfd9e036c01f4096f386a15`) with ONE `safe-apply` in
    `infra/aws/terraform/ticket-center`, then record the deploy. CODE ONLY. One route moves,
    `POST /api/scoped/tickets/{ticketId}/report`: besides the ticket's assignee it now admits the ticket's CREATOR, once, on its
    own analysis-request ticket that is not completed, carries an attachment and has no report recorded.
  </objective>

  <context>
    Both halves are SIGNED. Read both before any AWS call:
    - packet and COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R3_RUN/R3_RF2_DEPLOY_PACKET_20261011.md` @4e8b8ea421;
    - CTO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R3_RF2_CREATOR_RECORDS_REPORT_CTO_HALF.md` @4215f3838a.
    The CTO half asked ONE read before the apply, and it is done (this seat, after a fetch; `2.0.0_SA_COO~Y2` reads the same): at
    portal `origin/PROD` 37aa1247ee and `origin/DEV` 582ffe6eb8, `src/pages/TicketCenter/analysisRequest.ts` calls
    `recordTicketReport` in ONE place, inside `requestReport` (PROD :169, DEV :314), the assignee's path; the filing functions do
    not call it. So no product path reaches the new branch today and the after-reads gain no filing.
    THE ORDERING CONDITION: this apply starts only AFTER your own `TCKT_VNEXT.TO-RUN-R3-tr1` step 6 is done (the row delete, not
    before 13:19:00Z) and that run's ledger entry `tckt-vnext-r3-tr1-fwd1-fourth-run-20261011` is CLOSED. The two acts never
    overlap on this function.
    The method is the one you used for TO-APPLY-R2-pk2; do not ride `MSYS_NO_PATHCONV=1` on `safe-apply`. This order mints no
    identity, writes no ticket, touches no other function and sends no request down the YCharts path (CTO msg 4918).
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO, after the ordering condition. In order:
    0. Open the NEVER-2 ledger entry FIRST. The one function family on the artifact key is `opal-ticket-api`. Read EVERY live
       worktree's `.open_deploys/`, union them and print the per-tree denominator. An open entry naming `opal-ticket-api` other than
       your own is a STOP (the fourth run's entry must read closed by now).
    1. STOP 1 (the pin): `git diff --name-only 8ef21584f8 HEAD -- infra/aws/lambda/ticket_center/lambda_function.py infra/aws/terraform/ticket-center`
       is empty. Anything else is a STOP.
    2. STOP 2 (the rollback target): download the LIVE `opal-ticket-api` package and show the deployed `lambda_function.py` sha256 is
       `cf10e19e423b25b7b74ce43efd24e73b90a8a90850094697f3f79ec7145e6e74`. Anything else is a STOP before any plan.
    3. BEFORE: record CodeSha256 (expect `t1EoiJRZ...`), the env key names and their count, `opal-tickets` ItemCount, and the
       status fields (`status`, `assignee`, `created_by`) of `TCK-20261009-a1052909`.
    4. Build and upload. The zip's `lambda_function.py` must hash to `dc0cd973...`; otherwise STOP.
    5. Plan, then `.tools/safe-apply.sh`. Branch A is `0 to add, 1 to change, 0 to destroy` (source_code_hash only). Anything else
       is a STOP.
    6. AFTER:
       - (a) CodeSha256 equals the zip, and the deployed file is `dc0cd973...`;
       - (b) the env is unchanged (same key names, same count);
       - (c) an unauthenticated POST to `/api/scoped/tickets/TCK-20261009-a1052909/report` through CloudFront is refused 401;
       - (d) ItemCount is unchanged and `TCK-20261009-a1052909` reads the same status fields as in step 3;
       - (e) the replan is 0-diff.
    7. RECORD: run `record-terraform-deploy.sh` for `opal-ticket-api` as in `TCKT_VNEXT.TO-RECORD-R3-sm1`. STOP 3: if it lands only
       one of its two halves (the source map entry written and its notice not sent, or the reverse), STOP and report which; do not
       hand-edit the map (row TCKT_VNEXT-D2-S36).
    8. `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r3_rf2/clamp_precheck_table.json`
       reads `READ27 27/27` with the `opal-ticket-api` line CLAMPED on the new build (create the folder first).
    9. Close the ledger. Report once to `2.0.0_SA_COO~V2`: the deployed file hash FIRST, the new CodeSha256, the recorder's commit,
       the precheck line, and the measured push state of your commits. Do not claim the creator branch's live arms were exercised:
       they were not.

    Finish in session or roll back and say so loudly. Rollback: re-apply the build of `be67d1fd38` (file `cf10e19e...`), same method.
  </go>

  <bounds>
    No env, IAM, route or permission change. No other function. No ticket write, no identity, no token. Never
    `aws lambda update-function-code`. No client data in any tracked file. A surprise is ONE row in
    `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (`TCKT_VNEXT-D2-S<k>`, next free id;
    binary append, line endings kept), never a halt on anything but the STOPs above.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
infra/aws/lambda/ci/lambda-source-map.json
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R3-rf-2"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r3_rf2/clamp_precheck_table.json</invocation><expect>READ27 27/27</expect></criterion>
</proof_of_spec>
AC1 at the issuance: `READ27 27/27` on the build now live (the issuer's run, 11:04Z); after the apply it must read the same with
the ticket host on the new build, which it does only if the recorder ran (step 7).

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one apply, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the authorizer and the matrix are untouched).
comp-adversary: RUN -- the unauthenticated POST refused 401 (step 6c) and the precheck's 27-route clamp read on the new build (step 8).
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for an issuer cell (R3-rf-2) under a signed never-widen pair; not a worker cell.
</task_order>
