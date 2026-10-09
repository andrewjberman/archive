<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-APPLY-SA1.ticket-firm-scope-clamp-code-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    <status>complete -- SUPERSEDED. Applied by `0.7.0_AE_CloudOps~DELL2` at 04:57:46Z (ledger `tckt-vnext-sa1-clamp-20261009` CLOSED 05:01:11Z, branch A, deployed file `21fe06e0...`) but never flipped. Picked up later as `pending`, STOP 1 refused a re-run and nothing was re-applied (row TCKT_VNEXT-D2-S2); issuer `2.0.0_SA_COO~V2` msg 3281 confirmed the stop and ruled it WORLD-DONE -- no re-pin, no re-run. Cell SA-k-1 is carried forward by TO-APPLY-V12 and R13b, so the clamp is live in `67068626`. Proof instance VALID rc=0.</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_SA.md</decomp_doc> (workstream SA): the apply leg of cell `SA-k-1` (drained @6e19a53535).
<owned_cells>SA-k-1</owned_cells>
</decomp_ref>

  <objective>
    Deploy the code of `opal-ticket-api` at box/dell2 `6e19a53535` (`lambda_function.py` sha256 hex
    `21fe06e0d46bbfe5fd7ff5effff0dd8ef6b3eaacc612dff837b5e98711df3598`) with ONE `safe-apply` in
    `infra/aws/terraform/ticket-center`. CODE ONLY.
  </objective>

  <context>
    CTO half GIVEN: org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_SA_K1_FIRM_SCOPE_CLAMP_CTO_HALF.md (msg 2429). Its condition is met: 13 items scanned in opal-tickets at ~04:3xZ, all 12 tickets inside the 6 firms; the 1 item outside is _CONFIG:intake-cursor (no firm, no status; not a ticket).

    Packet and COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/SA_DEPLOY/SA_K1_DEPLOY_PACKET_20261009.md`.

    The previous deploy is your TO-APPLY-F10, ledger `20261009T0056Z_tckt-vnext-f10-d1-mint-20261009`. Repeat leg D's method. The build
    script now has a real `BUILD_ONLY=1` (TO-F10-l4); your step-3 upload is the normal path.
  </context>

  <steps>
    0. Open the NEVER-2 ledger entry. The one function family on the artifact key is `opal-ticket-api`.
    1. STOP 1: `git diff --name-only 6e19a53535 HEAD -- infra/aws/lambda/ticket_center infra/aws/terraform/ticket-center` is empty;
       anything else is branch B.
    2. BEFORE: record CodeSha256 (expect `RFRuryx...`), the 8 env key names and ItemCount.
    3. Build and upload. Record the zip content-sha256. The zip's `lambda_function.py` must hash to `21fe06e0...`; otherwise STOP.
    4. Plan, then `.tools/safe-apply.sh`. Branch A is `0 to add, 1 to change, 0 to destroy` (source_code_hash only). Anything else
       is branch B: STOP.
    5. AFTER:
       - (a) CodeSha256 equals the zip, and the deployed file is `21fe06e0...`;
       - (b) the env is unchanged (8 keys);
       - (c) an unauthenticated POST through CloudFront is refused;
       - (d) ItemCount is unchanged;
       - (e) the replan is 0-diff.
    6. Close the ledger. Report once to `2.0.0_SA_COO~V2`.
  </steps>

  <bounds>
    Rollback: re-apply the F10 v2 build at `3b04c040fc` (file `01534e2d...`). No env, IAM, route or permission change. No other
    function.
  </bounds>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SA-k-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/SA_CHECKS/sa_checks.py sa-clamp-scope</invocation><expect>SA-CLAMP-SCOPE-OK</expect></criterion>
  <criterion id="AC2" cell_refs="SA-k-1" judgment="true"/>
</proof_of_spec>
AC1 runs at the pin before the upload. AC2 (judgment, graded by the issuer) is step 5, the deployed bytes and the after-reads.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: DECLARED-NOT-APPLICABLE -- code only; the new lookup uses the role's existing opal-users-v2 read (the same calls _directory_snapshot makes).
comp-adversary: DECLARED-NOT-APPLICABLE -- the clamp's fail-closed arms are tested at the build; the live one-firm proof is the seat run's step 0.
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for an issuer cell (the deploy of SA-k-1, drained @6e19a53535); not a worker cell.
</task_order>
