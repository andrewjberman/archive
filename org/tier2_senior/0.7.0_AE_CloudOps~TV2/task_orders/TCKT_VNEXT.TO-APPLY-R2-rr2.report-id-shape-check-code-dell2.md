<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-APPLY-R2-rr2.report-id-shape-check-code-dell2</id>
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
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R2.md</decomp_doc> (round 2): cell `R2-rr-2`, the apply of `R2-rr-1` (drained @a366ce52ec).
<owned_cells>R2-rr-2</owned_cells>
</decomp_ref>

  <objective>
    Deploy the code of `opal-ticket-api` at box/dell2 `a366ce52ec` (`infra/aws/lambda/ticket_center/lambda_function.py` sha256 hex
    `ca3be34307f70079e48c4a26d1f711e47318285f2cf2722fdf0cfdcbd637eade`) with ONE `safe-apply` in
    `infra/aws/terraform/ticket-center`. CODE ONLY. One route's behaviour moves: `POST /api/scoped/tickets/{ticketId}/report` refuses
    a `request_id` that is not `REQ-<24 lower-case hex>`.
  </objective>

  <context>
    Both halves are SIGNED. Read both before any AWS call:
    - packet and COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R2_RUN/R2_RR2_DEPLOY_PACKET_20261011.md` @39ccf5774b;
    - CTO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R2_RR2_REPORT_ID_CHECK_DEPLOY_CTO_HALF.md` @51c5e7538b
      (four conditions; condition 1 is the control on the rollback target).
    Read `/cloud-ops` first. The method is the one `0.7.0_AE_CloudOps~DELL2` used for TO-APPLY-SA1 and TO-APPLY-F10 (ledgers
    `tckt-vnext-sa1-clamp-20261009` and `20261009T0056Z_tckt-vnext-f10-d1-mint-20261009` under
    `org/critical_paths/change_management/`); the build script has a real `BUILD_ONLY=1`.
    This order mints no identity, writes no ticket and touches no other function.
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO. In order:
    0. Open the NEVER-2 ledger entry FIRST. The one function family on the artifact key is `opal-ticket-api`. Read EVERY live
       worktree's `.open_deploys/` (`git worktree list --porcelain`, then
       `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`), union them and print the per-tree denominator. An
       open entry naming `opal-ticket-api` other than your own is a STOP.
    1. STOP 1 (the pin): `git diff --name-only a366ce52ec HEAD -- infra/aws/lambda/ticket_center/lambda_function.py infra/aws/terraform/ticket-center`
       is empty. Anything else is branch B: STOP. (Test files under `ticket_center/tests/` may differ; they are not the handler.)
    2. STOP 2 (the rollback target, CTO condition 1): download the LIVE package and show the deployed `lambda_function.py` sha256 is
       `670686262068808fcf1d3e0c05ce8e92e32441f9382efeb9361c789ab19457a8`. Anything else is a STOP before any plan, reported to the
       issuer and the CTO: the rollback target would be unknown.
    3. BEFORE: record CodeSha256 (expect `HK82TEd0SQWe...`), the 8 env key names, `opal-tickets` ItemCount, and the status fields
       (`status`, `assignee`, `created_by`) of `TCK-20261009-a1052909`.
    4. Build and upload. Record the zip content-sha256. The zip's `lambda_function.py` must hash to `ca3be343...`; otherwise STOP.
       If the zip carries the `tests/` folder, say so in the report.
    5. Plan, then `.tools/safe-apply.sh`. Branch A is `0 to add, 1 to change, 0 to destroy` (source_code_hash only). Anything else
       is branch B: STOP.
    6. AFTER:
       - (a) CodeSha256 equals the zip, and the deployed file is `ca3be343...`;
       - (b) the env is unchanged (8 keys);
       - (c) an unauthenticated POST to `/api/scoped/tickets/TCK-20261009-a1052909/report` through CloudFront is refused 401;
       - (d) ItemCount is unchanged and `TCK-20261009-a1052909` reads the same status fields as in step 3;
       - (e) the replan is 0-diff.
    7. Close the ledger. Report once to `2.0.0_SA_COO~V2`, with the push state of your commits measured by `git ls-remote`.

    Finish in session or roll back and say so loudly. Rollback: re-apply the build of `5a36586b5f` (file `67068626...`), same method.
  </go>

  <bounds>
    No env, IAM, route or permission change. No other function. No ticket write, no identity, no token: both live arms of the new
    check are cell `R2-tr-1`'s, under its own pair. Never `aws lambda update-function-code`. No client data in any tracked file.
    A surprise is ONE row in `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md`
    (`TCKT_VNEXT-D2-S<k>`, next free id; append in binary mode, CRLF kept), never a halt on anything but the STOPs above.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R2-rr-2"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R2_CHECKS/r2_checks.py rr-shape</invocation><expect>RR-SHAPE-OK</expect></criterion>
  <criterion id="AC2" cell_refs="R2-rr-2" judgment="true"/>
</proof_of_spec>
AC1 runs at the pin before the upload. AC2 (judgment, graded by the CVO at L9 on the ledger entry and the after-reads of step 6): the
deployed bytes are the pinned file, and nothing else moved.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (code only; no new AWS call in the 4 inserted lines).
comp-adversary: DECLARED-NOT-APPLICABLE (the refusal arms are tested at the build, rr-shape 4 of 4; the live arms are R2-tr-1's).
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for an issuer cell (the deploy of R2-rr-1, drained @a366ce52ec); not a worker cell.
</task_order>
