<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-R13.ticket-joint-i5p-i7-trade-request-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    <status>withdrawn</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R2.md</decomp_doc> (round 2, workstream ~V2 TICKET): the apply leg of cell `AR-v-21` (drained @53cbcad426), carrying NFRA_OPSWKF OW-l-1 under its own COO half.
<owned_cells>AR-v-21</owned_cells>
</decomp_ref>

  <objective>
    Deploy the code of `opal-ticket-api` at box/dell2 `ba6fcb1c14` (`lambda_function.py` sha256 hex
    `670686262068808fcf1d3e0c05ce8e92e32441f9382efeb9361c789ab19457a8`) with ONE `safe-apply` in
    `infra/aws/terraform/ticket-center`. CODE ONLY. Run it AFTER `IRPT_ANLREQ.TO-APPLY-V12` is complete.
  </objective>

  <context>
    Packet: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/TICKET_R13_JOINT_DEPLOY_PACKET_20261009.md` @cc15159703.
    COO halves: `~V2` (AR-v-21, in the packet); `~O2` (OW-l-1) at
    `org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/D1_DEPLOY/COO_HALF_OW_L1_TICKET_R13_JOINT_20261009.md` @37a9fac095.
    CTO half GIVEN: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_TICKET_R13_JOINT_RELEASE_CTO_HALF.md`
    @11a11e67e2 (msg 2896). Its conditions are steps 1, 4 and 0 below.

    Build in a DETACHED worktree at `ba6fcb1c14` (`git worktree add --detach <abs-path> ba6fcb1c14`), as for V12 AMENDMENT 1, so later
    commits on box/dell2 cannot enter the build. Remove the worktree after the ledger closes.
  </context>

  <steps>
    0. Open the NEVER-2 ledger entry, pinned to `ba6fcb1c14` and file `67068626...`. The one family on the artifact key is `opal-ticket-api`.
    1. STOP 1: the live function's deployed `lambda_function.py` is V12's `04f5727b...`. Anything else: STOP, report, apply nothing.
    2. BEFORE: CodeSha256, the 8 env key names, and ItemCount.
    3. Build and upload from the detached worktree. The zip's `lambda_function.py` must hash to `67068626...`; otherwise STOP.
    4. Plan, then `.tools/safe-apply.sh`. Branch A: `0 to add, 1 to change, 0 to destroy` (the source hash with s3_object_version).
       Anything else is branch B: STOP.
    5. AFTER:
       - (a) the deployed file is `67068626...`;
       - (b) env unchanged;
       - (c) an unauthenticated POST is refused;
       - (d) ItemCount unchanged;
       - (e) replan 0-diff.
    6. Close the ledger. Report once to `2.0.0_SA_COO~V2`, with the deployed CodeSha256.
  </steps>

  <amendment n="1" date="2026-10-09" source="CTO msg 3199 (UB-20261009T110751Z-9119 fold @6f1a091a2f); standing ruling @5ff94852a6">
    WITHDRAWN from `0.7.0_AE_CloudOps~DELL2`, which never read the issuer's msgs 3154 and the 11:21Z re-send. Nothing was built or
    applied under this order. The same apply, with the same halves (COO `~V2` in the packet, COO `~O2` @37a9fac095, CTO @11a11e67e2)
    and the same pin, steps and after-reads, is re-issued to an MSTR-seated CloudOps lane for IRPT_ANLREQ only, under ruling
    @5ff94852a6 item 2. Only the applier's name changes. The re-issued order names this ruling and the half, and its ledger names the
    substitute lane. Two appliers never hold one order.
  </amendment>

  <bounds>
    Rollback: re-apply V12's build (pin `86454002bf`, file `04f5727b...`). No env, IAM, route or permission change.
  </bounds>

<proof_of_spec>
  <criterion id="AC1" cell_refs="AR-v-21"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/AR_V_CHECKS/ar_v_checks.py v21-package</invocation><expect>V21-PACKAGE-OK</expect></criterion>
  <criterion id="AC2" cell_refs="AR-v-21" judgment="true"/>
</proof_of_spec>
AC1 runs in the detached worktree at the pin, before the upload, with invalid AWS keys. AC2 (judgment, graded at L9) is the step-5 after-reads.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE (code only). comp-adversary: DECLARED-NOT-APPLICABLE (the package route's new refusal reaches no live caller: no packager token or PROFILE row exists).
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for an issuer cell (the deploy of AR-v-21, drained @53cbcad426, joint with OW-l-1 under its own COO half); not a worker cell.
</task_order>
