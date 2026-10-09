<task_order>
  <metadata>
    <id>NFRA_OPSWKF.TO-APPLY-D1.trade-lambdas-ticket-bridge-dell2</id>
    <issued_by>2.0.0_SA_COO~O2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>NFRA_OPSWKF</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_OPSWKF/decompositions/NFRA_OPSWKF_DECOMP.md</decomp_doc> (round 1): issuer cell `OW-d-1`, serving drained cells OW-e-1, OW-e-2, OW-e-3, OW-i-1 (OW-i-1 AMENDMENT 1 @71a1877db0).
<owned_cells>OW-d-1</owned_cells>
</decomp_ref>

  <objective>
    Deploy ONE `safe-apply` of `infra/aws/terraform/trade-pipeline` at box/dell2 pin `71a1877db0`, covering:
    - the code of `trade-submission-handler` (`submission_handler.py` sha256 hex
      `fc59cd256c1797860277a200a39d47a493f06cef56e4c6ac6f10010c1bb146a4`);
    - the code of `trade-workflow-handler` (`workflow_handler.py` sha256 hex
      `49a9607ece5d5c349eb914122bb47273e671910808344edf6d6924824195e86c`);
    - `TICKETS_TABLE` on both functions;
    - the two `TicketBridgeOpalTickets*` statements in `trade-submission-policy`.

    Nothing else. The ticket Lambda `opal-ticket-api` is NOT in this order.
  </objective>

  <context>
    COO half and packet: org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/D1_DEPLOY/OW_D1_DEPLOY_PACKET_20261009.md @ad3f901e17.

    CTO half, GIVEN under conditions 1-3: org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_OW_D1_TRADE_LAMBDAS_CTO_HALF.md @a4c661373b (msg 2742).

    Condition 1 is already met in code at the pin: UpdateItem is narrowed by `ForAllValues:StringEquals` `dynamodb:Attributes` = ticket_id,
    linked_submission_id, events, status. The handlers write no other ticket attribute; the worker confirmed it, and the check is
    `ow_checks.py i1-cond`.

    Artifacts are versioned S3 objects that Terraform pins: `trade-pipeline/trade-submission-handler.zip` and
    `trade-pipeline/trade-workflow-handler.zip` in `opal-313476888478-lambda-artifacts`, with `source_code_hash` taken from the
    `content-sha256` metadata (`lambdas.tf`). Source dirs: `infra/aws/lambda/ci/lambda-source-map.json`. Afterwards, record the deploy with
    `record-terraform-deploy.sh`, as the last trade-pipeline deploy did (v1.22.0 @b8831237).
  </context>

  <steps>
    0. Open the NEVER-2 ledger entry. Condition 3: it states the pin `71a1877db0` and BOTH built sha256 values (zip content and handler
       file). The families on these artifact keys are `trade-submission-handler` and `trade-workflow-handler`, one each.
    1. STOP 1: `git diff --name-only 71a1877db0 HEAD -- infra/aws/lambda/trade-pipeline infra/aws/terraform/trade-pipeline` is empty.
       Anything else is branch B.
    2. BEFORE: record each function's CodeSha256, its current `s3_object_version` (the ROLLBACK pin), its env key names, and the policy
       document of `trade-submission-policy`.
    3. Build each zip from its source dir at the pin and upload it with `content-sha256` metadata. Each zip's handler file must hash to the
       value in the objective; otherwise STOP.
    4. Plan, then `.tools/safe-apply.sh`.
       - Branch A: `0 to add, 3 to change, 0 to destroy`, namely `aws_iam_role_policy.trade_submission_policy`,
         `aws_lambda_function.trade_submission_handler` and `aws_lambda_function.trade_workflow_handler`.
       - Anything else, including any of the other nine functions, the recon role, a bucket, a table or a route, is branch B: STOP and
         report.
    5. AFTER (print each):
       - (a) both CodeSha256 values equal the uploaded zips, and each deployed handler file hashes to the objective's value;
       - (b) env = prior keys + `TICKETS_TABLE`;
       - (c) `simulate-principal-policy` on `trade-submission-lambda-role`:
         - GetItem on `table/opal-tickets` ALLOWED;
         - UpdateItem with context `dynamodb:Attributes` = [ticket_id, linked_submission_id, events] ALLOWED;
         - UpdateItem with `dynamodb:Attributes` = [ticket_id, answers] DENIED (the CTO's negative arm);
         - DeleteItem, PutItem and Scan on it DENIED;
       - (d) an unauthenticated `POST /api/general/trades/submit` through CloudFront is refused (401/403);
       - (e) the replan is 0-diff.
    6. Close the ledger and record the deploy. Report once to `2.0.0_SA_COO~O2`.
  </steps>

  <bounds>
    Rollback, per key, in the same window:
    - re-point each function to the step-2 `s3_object_version`;
    - drop the two statements and the env key by applying the stack at the parent of the four drain merges.

    No change to `BROKERAGE_EMAILS`, SES, routes, the ticket stack, or any other function. Never widen the attribute list at the console:
    if a live read shows the code needs another attribute, STOP and come back (CTO condition 1).
  </bounds>

<proof_of_spec>
  <criterion id="OW-d1-AC1" cell_refs="OW-d-1"><invocation>python org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/R1_CHECKS/ow_checks.py i1-cond</invocation><expect>OW-I1-COND-OK</expect></criterion>
  <criterion id="OW-d1-AC2" cell_refs="OW-d-1" judgment="true"/>
</proof_of_spec>
OW-d1-AC1 runs at the pin, before the upload. OW-d1-AC2 (judgment, graded by the issuer) is step 5: the deployed bytes and the after-reads (a)-(e).

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule, hold or gate is created or consumed by this deploy
comp-iam: DECLARED-NOT-APPLICABLE at the cut; the grant's shape is graded by OW-d1-AC1 and the live policy by the simulate arms in step 5 (c), negative arm included
comp-adversary: DECLARED-NOT-APPLICABLE at the cut; the Execute fence's negative control is a unit test at the drain, and its live 409 is the issuer's OW-r-1
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for an issuer cell (OW-d-1, the deploy of drained cells e-1, e-2, e-3, i-1 at 71a1877db0); not a worker cell.
</task_order>
