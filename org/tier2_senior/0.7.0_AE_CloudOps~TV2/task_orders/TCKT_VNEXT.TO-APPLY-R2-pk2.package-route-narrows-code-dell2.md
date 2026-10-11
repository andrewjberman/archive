<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-APPLY-R2-pk2.package-route-narrows-code-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R2.md</decomp_doc> (round 2, ADDENDUM 2): cell `R2-pk-2`, the apply of `R2-pk-1` (drained @be67d1fd38).
<owned_cells>R2-pk-2</owned_cells>
</decomp_ref>

  <objective>
    Deploy the code of `opal-ticket-api` at box/dell2 `be67d1fd38` (`infra/aws/lambda/ticket_center/lambda_function.py` sha256 hex
    `cf10e19e423b25b7b74ce43efd24e73b90a8a90850094697f3f79ec7145e6e74`) with ONE `safe-apply` in
    `infra/aws/terraform/ticket-center`. CODE ONLY. One route's answers move, for one service principal:
    `POST /api/scoped/tickets/{ticketId}/package` stops returning the ticket (on its 200 and on its changed-under-write 409) and
    its five 409s gain a `code`.
  </objective>

  <context>
    Both halves are SIGNED. Read both before any AWS call:
    - packet and COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R2_RUN/R2_PK2_DEPLOY_PACKET_20261011.md` @472efb3a5b;
    - CTO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R2_PK2_PACKAGE_ROUTE_NARROWS_CTO_HALF.md` @5572ffcbbd
      (the packet's steps 0 to 6 with both STOPs; step 1b names the function it read and its digest; nothing claims the live arms
      were exercised).
    The ordering condition of both halves is met: R2-tr-1's run 3 ended (your report msg 4534, ledger closed).
    The method is the one you used for TO-APPLY-R2-rr2 (ledger `20261011T0403Z_tckt-vnext-r2-rr2-report-id-shape-20261011`); do not
    ride `MSYS_NO_PATHCONV=1` on `safe-apply`.
    This order mints no identity, writes no ticket and touches no other function.
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO. In order:
    0. Open the NEVER-2 ledger entry FIRST. The one function family on the artifact key is `opal-ticket-api`. Read EVERY live
       worktree's `.open_deploys/`, union them and print the per-tree denominator. An open entry naming `opal-ticket-api` other than
       your own is a STOP.
    1. STOP 1 (the pin): `git diff --name-only be67d1fd38 HEAD -- infra/aws/lambda/ticket_center/lambda_function.py infra/aws/terraform/ticket-center`
       is empty. Anything else is a STOP.
    2. STOP 2 (the rollback target): download the LIVE `opal-ticket-api` package and show the deployed `lambda_function.py` sha256 is
       `ca3be34307f70079e48c4a26d1f711e47318285f2cf2722fdf0cfdcbd637eade`. Anything else is a STOP before any plan.
    3. STOP 3 (the one caller, the packet's step 1b): name the Lambda function that runs
       `infra/aws/lambda/investor-reporting/ycharts/research/opal_packager.py`, record its live CodeSha256, download its live
       package, and show that its `attach` call to `/package` discards the answer as the tree's does (tree: the call at `:269`, the
       discarded result at `:183`). If the deployed packager reads `ticket` from the answer, or you cannot find the function, STOP
       and report; do not plan.
    4. BEFORE: record CodeSha256 (expect `W03VREoM...`), the 8 env key names, `opal-tickets` ItemCount, and the status fields
       (`status`, `assignee`, `created_by`) of `TCK-20261009-a1052909`.
    5. Build and upload. The zip's `lambda_function.py` must hash to `cf10e19e...`; otherwise STOP.
    6. Plan, then `.tools/safe-apply.sh`. Branch A is `0 to add, 1 to change, 0 to destroy` (source_code_hash only). Anything else
       is a STOP.
    7. AFTER:
       - (a) CodeSha256 equals the zip, and the deployed file is `cf10e19e...`;
       - (b) the env is unchanged (8 keys);
       - (c) an unauthenticated POST to `/api/scoped/tickets/TCK-20261009-a1052909/package` through CloudFront is refused 401;
       - (d) ItemCount is unchanged and `TCK-20261009-a1052909` reads the same status fields as in step 4;
       - (e) the replan is 0-diff.
    8. Close the ledger. Report once to `2.0.0_SA_COO~V2`: the deployed file hash FIRST (the issuer must add it to its precheck's
       list in the same sitting, row TCKT_VNEXT-D2-S28), the packager function's name and digest, and the measured push state of
       your commits. Do not claim the live arms (a 409 carrying its code, a 200 without `ticket`) were exercised: they were not.

    Finish in session or roll back and say so loudly. Rollback: re-apply the build of `a366ce52ec` (file `ca3be343...`), same method.
  </go>

<amendment n="1" date="2026-10-11" source="your STOP 3 (msg 4582, row TCKT_VNEXT-D2-S34); CTO ruling msg 4587; 2.0.0_SA_COO~G2 msg 4594">
    Your STOP 3 was right to fire as written, and the issuer's order was wrong about WHERE the caller runs: it said "the Lambda
    function that runs opal_packager.py". The packager's host is the RESIDENT, which is not a Lambda, so a sweep of 17 Lambdas
    could not find it or rule it out. That was the issuer's error.

    The CTO ruled (msg 4587): PROCEED after one more read over the right population. That read is in, by `2.0.0_SA_COO~G2`
    (msg 4594): in the running resident root's package tar (`e606008994-st27.tar.gz`, sha256 `20916261074c356a...`, 270 members),
    `ycharts/research/opal_packager.py` is ABSENT, 0 member names contain "packager", and the root's bindings carry no packager
    key. Its stated limit: this is the BUILD INPUT of the running root, not a file listing of the host. By the CTO's rule, absent
    or unbound means nothing can call the route, and the apply proceeds.

    STOP 3 IS RESTATED: it is met by the record, not by a function digest. In the ledger entry and your report write, beside each
    other: "N=17 Lambdas swept by content, 0 carry opal_packager.py" (your read) and "running resident root e606008994-st27:
    opal_packager.py absent, no packager binding; build input, host bytes not listed" (msg 4594). Do not claim a deployed caller
    was read. You do NOT need to list the host.

    SECOND GO, by `2.0.0_SA_COO~V2`, 2026-10-11: run steps 0-8 again from step 0 with a NEW ledger entry. STOPs 1 and 2 are read
    again, live. Step 3 is the restated record above. Everything else stands.
  </amendment>

  <bounds>
    No env, IAM, route or permission change. No other function. No ticket write, no identity, no token. Never
    `aws lambda update-function-code`. No client data in any tracked file. A surprise is ONE row in
    `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (`TCKT_VNEXT-D2-S<k>`, next free id;
    binary append, CRLF kept), never a halt on anything but the STOPs above.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R2-pk-2"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R2_CHECKS/r2_checks.py pk-200</invocation><expect>PK-200-OK</expect></criterion>
  <criterion id="AC2" cell_refs="R2-pk-2" judgment="true"/>
</proof_of_spec>
AC1 runs at the pin before the upload. AC2 (judgment, graded by the CVO at L9 on the ledger entry and the after-reads of step 7): the
deployed bytes are the pinned file, the one caller was read first, and nothing else moved.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (code only; no new AWS call).
comp-adversary: DECLARED-NOT-APPLICABLE (the refusal and no-ticket arms are tested at the build, pk-codes 5 of 5 and pk-200 2 of 2; the live arms belong to the packager's next attach or to IRPT_ANLREQ's AR-g-32).
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for an issuer cell (the deploy of R2-pk-1, drained @be67d1fd38); not a worker cell.
</task_order>
