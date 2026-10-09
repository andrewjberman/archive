<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-V12.ticket-package-principal-code-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R1.md</decomp_doc> (round 1, workstream ~V2 TICKET): the apply leg of cell `AR-v-12` (drained @86454002bf).
<owned_cells>AR-v-12</owned_cells>
</decomp_ref>

  <objective>
    Deploy the code of `opal-ticket-api` at box/dell2 `86454002bf` (`lambda_function.py` sha256 hex
    `04f5727bebf83e7c19493f944bc1c8ed2f7a28404b5137d6cf2cb32b699f9a38`) with ONE `safe-apply` in
    `infra/aws/terraform/ticket-center`. CODE ONLY.
  </objective>

  <context>
    CTO half GIVEN: org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_AR_V12_PACKAGE_PRINCIPAL_CTO_HALF.md @7319f84a6e (msg 2646). Conditions: the plan shows exactly ONE change, on opal-ticket-api; you apply with a pinned ledger; (the packager mint pair names its exact firm list -- a later pair, not this order).

    Packet and COO half: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/AR_V12_DEPLOY_PACKET_20261009.md`.

    Repeat your TO-APPLY-SA1 method exactly. Its ledger is `tckt-vnext-sa1-clamp-20261009`. `s3_object_version` moves with the
    source hash, as it did there.
  </context>

  <steps>
    0. Open the NEVER-2 ledger entry. The one family on the artifact key is `opal-ticket-api`.
    1. STOP 1: `git diff --name-only 86454002bf HEAD -- infra/aws/lambda/ticket_center infra/aws/terraform/ticket-center` is empty;
       anything else is branch B.
    2. BEFORE: CodeSha256 (expect `ywAvsfx...`), the 8 env key names, and ItemCount.
    3. Build and upload. The zip's `lambda_function.py` must hash to `04f5727b...`; otherwise STOP.
    4. Plan, then `.tools/safe-apply.sh`. Branch A: `0 to add, 1 to change, 0 to destroy` (the source hash with s3_object_version).
       Anything else is branch B: STOP.
    5. AFTER:
       - (a) the deployed file is `04f5727b...`;
       - (b) env unchanged;
       - (c) an unauthenticated POST is refused;
       - (d) ItemCount unchanged;
       - (e) replan 0-diff.
    6. Close the ledger. Report once to `2.0.0_SA_COO~V2`.
  </steps>

  <bounds>
    Rollback: re-apply the SA-k-1 build (`6e19a53535`, file `21fe06e0...`). No env, IAM, route or permission change.
  </bounds>

<proof_of_spec>
  <criterion id="AC1" cell_refs="AR-v-12"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/AR_V_CHECKS/ar_v_checks.py v12-packager</invocation><expect>V12-PACKAGER-OK</expect></criterion>
  <criterion id="AC2" cell_refs="AR-v-12" judgment="true"/>
</proof_of_spec>
AC1 runs at the pin before the upload. AC2 (judgment, graded at L9) is the step-5 after-reads.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE (code only; the role's existing users-table read). comp-adversary: DECLARED-NOT-APPLICABLE (inert until the packager is minted).
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for an issuer cell (the deploy of AR-v-12, drained @86454002bf); not a worker cell.
</task_order>
