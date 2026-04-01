<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADVI_ANONYM-004-dt-deploy</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-01</date>
    <status>complete</status>
    <!-- Completed 2026-04-01. Track B: auth-validator-edge:8 on CF behaviors 13+14. Track A: partners-api-v1.11.0 (commit 4485ec1c). Track C: auth-validator-edge v9, P0 gate removed (commit 92ae074c). All 10 CF behaviors updated. E2E verified. -->
    <priority>high</priority>
    <type>deploy</type>
    <project>ADVI_ANONYM</project>
  </metadata>

  <objective>
    Deploy the ADVI_ANONYM P1 Lambda changes and update CloudFront behaviors to
    complete the pseudonymization rollout. This has three sequential sub-tasks:

    Track A -- Deploy updated opal-partners-data Lambda (after DS commits pseudonymizer)
    Track B -- Attach auth-validator-edge to CloudFront behaviors 13 and 14
    Track C -- Remove P0 role gate from auth-validator-edge (LAST, after end-to-end verification)

    Tracks A and B can proceed in parallel. Track C is the final step and must not
    happen until the pseudonymizer is verified working for advisor/user requests.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_ANONYM_PRD.md -- Phase 1, Deployment Ordering</ref>
    <ref type="ds_to">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_ANONYM.002.ds-pseudonymizer-lambda.md</ref>
    <ref type="ae_to">org/tier2_senior/0.7.0_AE_CloudOps/task_orders/ADVI_ANONYM.003.ae-secrets-provisioning.md</ref>
    <ref type="lambda_path">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/</ref>
    <ref type="edge_path">infra/aws/lambda-edge/auth-validator-edge/index.mjs</ref>
    <ref type="cf_distribution">EVTSA9VEHNZVH (opalinvest.dev -- console-managed, NOT in Terraform)</ref>
  </references>

  <pre_verified_facts>
    COO verified the following before issuing this TO:

    1. portal_authorizer does NOT need redeployment. It was deployed 2026-03-04 and
       already returns role in the authorizer context (line 198 of the deployed source).
       Do not touch portal_authorizer.

    2. CloudFront distribution EVTSA9VEHNZVH is console-managed (not in Terraform).
       CloudFront behavior updates (Track B) are manual AWS CLI or console operations.
       This was established in ADVI_ANONYM.001 (DT session log 2026-03-31).

    3. CloudFront behaviors 13 (/api/scoped/partners/*) and 14 (/api/partners)
       were added 2026-03-31 (DT session log) and do NOT currently have auth-validator-edge
       Lambda@Edge attached. They authenticate via JWT in the Lambda itself.

    4. auth-validator-edge v8 (deployed via ADVI_ANONYM.001) contains the P0 role gate
       at lines 58-66 of index.mjs. This gate MUST remain active until Track A pseudonymizer
       is verified end-to-end. Track C removes it last.
  </pre_verified_facts>

  <requirements>

    <requirement id="A1">
      TRACK A -- DEPLOY opal-partners-data Lambda.
      PREREQUISITE: Confirm DS has committed ADVI_ANONYM.002 changes (pseudonymizer.py + 
      lambda_function.py wiring). Check git log:
      `git log --oneline --author="0.4.0_DS" -5`
      If the commit is not there, wait for DS before proceeding with Track A.
    </requirement>

    <requirement id="A2">
      TRACK A -- Check DS session log for any IAM blocker notes. If DS flagged that
      opal-partners-data Lambda execution role is missing secretsmanager:GetSecretValue
      for opal/pseudonym/*, confirm AE has completed ADVI_ANONYM.003 and Terraform is
      at 0-diff before deploying the Lambda. The Lambda will crash on cold start if it
      cannot read Secrets Manager.
    </requirement>

    <requirement id="A3">
      TRACK A -- Build and deploy opal-partners-data Lambda via standard Terraform sequence:
      ```
      export TMPDIR="C:/Windows/Temp"
      cd infra/aws/terraform/partners-api
      bash ../../../scripts/build-and-upload.sh opal-partners-data
      .tools/terraform plan
      .tools/terraform apply
      .tools/terraform plan   # MUST show No changes
      ```
      Pipeline: partners-api. Read LAMBDA_DEPLOYMENT_PROTOCOL.md before executing.
      Verify 0-diff. Tag: increment partners-api version. Push with --follow-tags.
    </requirement>

    <requirement id="A4">
      TRACK A -- Verify the deployed Lambda works correctly:
      Test 1 (internal user JWT):
        curl -H "Authorization: Bearer {internal_jwt}" \
          "https://opalinvest.dev/api/shared/advisor-intelligence/summary?firmId={test_firm}"
        Expect 200 with cleartext names.

      Test 2 (advisor-user JWT -- after P0 gate removal in Track C):
        This cannot be fully verified until Track C. Note it as deferred.
        Interim test: invoke the Lambda directly (aws lambda invoke) with a mock event
        where auth_context has tier=advisor, role=user. Verify response contains
        hashed names (Client xxxxxxxx format).
    </requirement>

    <requirement id="B1">
      TRACK B -- Attach auth-validator-edge Lambda@Edge to CloudFront behaviors 13 and 14.
      This can run in parallel with Track A.

      Current state (confirmed by DT 2026-03-31 log):
      - Behavior 13: /api/scoped/partners/* -- no auth-validator-edge
      - Behavior 14: /api/partners -- no auth-validator-edge

      Steps:
      1. Get the current auth-validator-edge ARN (versioned -- must be a numbered version, not $LATEST):
         `aws lambda list-versions-by-function --function-name auth-validator-edge \
           --query "Versions[-1].FunctionArn" --output text`

      2. For each of behaviors 13 and 14 in CloudFront distribution EVTSA9VEHNZVH:
         Add Lambda@Edge association for viewer-request event with the versioned ARN.
         This must be done via AWS CLI (distribution is console-managed):
         ```
         # Get current distribution config
         aws cloudfront get-distribution-config --id EVTSA9VEHNZVH > dist_config.json
         # Edit: add LambdaFunctionAssociations for behaviors 13 and 14
         # Update distribution with new ETag
         aws cloudfront update-distribution --id EVTSA9VEHNZVH ...
         ```
         Alternatively: use the AWS console to add the Lambda@Edge association.

      3. Wait for CloudFront distribution status: Deployed.

      4. Verify behaviors 13+14 now enforce auth:
         curl without Authorization header -> 401 (auth-validator-edge blocks unauthenticated).
         curl with valid JWT -> request reaches Lambda.
    </requirement>

    <requirement id="C1">
      TRACK C -- Remove P0 role gate from auth-validator-edge.
      PREREQUISITE: Tracks A and B must be COMPLETE and verified.
      Specifically: pseudonymizer must be confirmed working (advisor/user gets hashed names,
      not cleartext), AND behaviors 13+14 must have auth-validator-edge attached.

      The P0 gate is in infra/aws/lambda-edge/auth-validator-edge/index.mjs lines 58-66.
      The gate currently returns 403 for any user where role != 'admin' on
      advisor-intelligence paths. Remove these lines.

      Commit the change:
      ```
      git commit --author="0.4.0_DT_ClientPlatform <0.4.0_DT_ClientPlatform@opal.agent>" \
          -m "security(ADVI_ANONYM P1): remove P0 role gate -- pseudonymizer handles graduated access"
      ```

      Rebuild and redeploy auth-validator-edge:
      1. npm install in infra/aws/lambda-edge/auth-validator-edge/
      2. Zip index.mjs + node_modules/
      3. aws lambda update-function-code (Lambda@Edge deployment -- NOT via Terraform)
      4. aws lambda publish-version
      5. Update CloudFront distribution viewer-request associations for behaviors 2 and 5
         (the existing advisor-intelligence behaviors) to the new version ARN.
      6. Wait for CloudFront status: Deployed.

      Verify Track C:
      Test with advisor-user JWT on /api/shared/advisor-intelligence/summary -> 200 with hashed names.
      Test with advisor-user JWT on /api/scoped/partners/books/advisor/{id}/timeseries -> 200.
      Test with internal JWT -> 200 with cleartext names.
    </requirement>

    <requirement id="C2">
      TRACK C -- After verifying Track C end-to-end, update ADVI_ANONYM.001.dt-deploy-auth-validator-v8.md
      with a completion note and set status to archived. Write session log.
    </requirement>

    <requirement id="D1">
      Write a session log at:
      org/tier2_senior/0.4.0_DT_ClientPlatform/logs/YYYY-MM-DD/advi_anonym_p1_deploy.md

      Include: DS commit hash used for Lambda build, Terraform tag applied, Track B verification
      results (CloudFront behaviors), Track C verification curls and results.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">opal-partners-data Lambda deployed with pseudonymizer. Terraform at 0-diff. partners-api tag incremented.</criterion>
    <criterion id="2">auth-validator-edge attached to CloudFront behaviors 13 (/api/scoped/partners/*) and 14 (/api/partners). Distribution status: Deployed.</criterion>
    <criterion id="3">P0 role gate removed from auth-validator-edge. New version deployed to CloudFront behaviors 2 and 5.</criterion>
    <criterion id="4">End-to-end verification: advisor/user JWT gets 200 with hashed client names on summary endpoint. Internal JWT gets 200 with cleartext.</criterion>
    <criterion id="5">CloudFront distribution EVTSA9VEHNZVH at Deployed status after all changes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Track C (P0 gate removal) MUST come LAST. If pseudonymizer has a bug, the gate is the safety net. Do not remove it until advisor/user pseudonymized response is verified.</constraint>
    <constraint>Do NOT touch portal_authorizer. It is already correctly deployed with role context.</constraint>
    <constraint>CloudFront distribution EVTSA9VEHNZVH is console-managed. Do not attempt to import it into Terraform as part of this task.</constraint>
    <constraint>Lambda@Edge functions must be in us-east-1.</constraint>
    <constraint>auth-validator-edge deploys via manual aws lambda commands (not Terraform). This is established by prior DT sessions.</constraint>
    <constraint>No emojis in code per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ANONYM.002.ds-pseudonymizer-lambda" status="staged">
      Track A requires DS commit of pseudonymizer.py + lambda_function.py wiring.
    </dependency>
    <dependency agent="0.7.0_AE_CloudOps" task="ADVI_ANONYM.003.ae-secrets-provisioning" status="staged">
      Track A requires AE to have updated Lambda execution role IAM policy (Secrets Manager access).
      Without this the Lambda cold start will fail when pseudonymizer calls GetSecretValue.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">opal-partners-data Lambda deployed with pseudonymizer module</deliverable>
    <deliverable type="deploy">auth-validator-edge attached to CloudFront behaviors 13 and 14</deliverable>
    <deliverable type="deploy">P0 role gate removed from auth-validator-edge. New version on behaviors 2 and 5.</deliverable>
    <deliverable type="document">Session log with verification results and Terraform tag</deliverable>
  </deliverables>
</task_order>
