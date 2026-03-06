# Task Order: Partner Identity Table — J1/J2/J3 Issuance — 2.0.0_SA_COO

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-04-partner-identity-table</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>2.0.0_SA_COO</issued_to>
    <date>2026-03-04</date>
    <status>complete</status>
    <completed>2026-03-06</completed>
    <completion_note>J1 (DynamoDB table opal-partner-49financial): deployed shared-infra-v1.3.0, ACTIVE. J2/J3 (portal-auth handler + authorizer): portal-auth commits de023eed + ba0cbc19 + 67a400b3, deployed. All three confirmed by DE audit log 2026-03-05/task_order_completeness_audit.md.</completion_note>
    <priority>HIGH — blocking 0.4.0_DT Books tab auth gating (J4)</priority>
  </metadata>

  <objective>
    DS A5 investigation confirmed: opal-users-v2 has no advisorId/advisorKey fields and
    architects have zero portal accounts. The original Stream J (Cognito firmId refactor,
    issued to AE on 2026-03-03) is SUPERSEDED. The new architecture is a per-partner
    DynamoDB identity table joined to opal-users-v2 by email.

    PRD is complete: docs/architecture/PARTNER_IDENTITY_TABLE.md (committed 2026-03-04).

    Your task: issue J1 to AE and J2/J3 to DT using the pre-drafted task orders below.
    Then mark the stale AE firmId task order as superseded.
    J4 task orders are NOT issued yet — they wait for J3 completion + ADVI-006 brief.
  </objective>

  <references>
    <ref type="prd" priority="PRIMARY">docs/architecture/PARTNER_IDENTITY_TABLE.md</ref>
    <ref type="prd-parent">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="superseded-task-order">org/tier2_senior/0.7.0_AE_CloudOps/task_orders/advisor_intelligence_firmid_auth.md</ref>
    <ref type="shared-infra-tf">infra/aws/terraform/shared-infra/</ref>
    <ref type="auth-handler-lambda">infra/aws/opalinvest_dev/lambda/auth-handler/</ref>
    <ref type="portal-authorizer-lambda">infra/aws/users/lambda/portal-authorizer/</ref>
    <ref type="portal-auth-tf-module">infra/aws/terraform/ (portal-auth module, commit 1660ed82)</ref>
    <ref type="lambda-deploy-protocol">docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md</ref>
  </references>

  <requirements>

    <!-- ================================================================ -->
    <!-- STEP 0 — Supersede stale AE task order                          -->
    <!-- ================================================================ -->
    <requirement id="COO.0">
      Mark org/tier2_senior/0.7.0_AE_CloudOps/task_orders/advisor_intelligence_firmid_auth.md
      status as SUPERSEDED. Add a note: "Superseded by partner_identity_table.md J1 task order
      (2026-03-04). Cognito firmId approach abandoned. New approach: DynamoDB per-partner
      identity table read by auth-handler Lambda."
      Do NOT delete the file — keep it as a record.
    </requirement>

    <!-- ================================================================ -->
    <!-- STEP 1 — Issue J1 to 0.7.0_AE_CloudOps                         -->
    <!-- ================================================================ -->
    <requirement id="COO.1">
      Issue the pre-drafted J1 task order to 0.7.0_AE_CloudOps.
      Pre-draft: org/tier2_senior/0.7.0_AE_CloudOps/task_orders/ADVI-J1-partner-identity-dynamo.md
      (CTO has written this file — COO reviews and issues it.)

      J1 scope: Create aws_dynamodb_table.opal_partner_49financial in shared-infra Terraform.
      J1 owner: 0.7.0_AE_CloudOps
      J1 unblocked: immediately (no dependencies)
    </requirement>

    <!-- ================================================================ -->
    <!-- STEP 2 — Issue J2/J3 to 0.4.0_DT_ClientPlatform                -->
    <!-- ================================================================ -->
    <requirement id="COO.2">
      Issue the pre-drafted J2/J3 task order to 0.4.0_DT_ClientPlatform.
      Pre-draft: org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/ADVI-J2-J3-auth-handler-authorizer.md
      (CTO has written this file — COO reviews and issues it.)

      J2 scope: auth-handler Lambda reads opal-partner-49financial, injects advisorKey/advisorRole/firmId into JWT.
      J3 scope: portal-authorizer passes those claims through to Lambda context.
      J2/J3 owner: 0.4.0_DT_ClientPlatform
      J2 dependency: J1 complete (table must exist before Lambda reads it)
      J3 dependency: J2 complete (claims must be in JWT before authorizer can pass them)
    </requirement>

    <!-- ================================================================ -->
    <!-- STEP 3 — Hold J4                                                 -->
    <!-- ================================================================ -->
    <requirement id="COO.3">
      Do NOT issue J4 task orders yet.
      J4 (Books tab auth gating: DE + RD) requires:
        - J3 complete (authorizer context available)
        - ADVI-006 Books design brief written (not yet scheduled)
      Schedule ADVI-006 thread separately. Flag to CTO when J3 is confirmed deployed
      so the Books design brief can be initiated.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">advisor_intelligence_firmid_auth.md marked SUPERSEDED with note.</criterion>
    <criterion id="2">J1 task order issued to 0.7.0_AE_CloudOps and confirmed received.</criterion>
    <criterion id="3">J2/J3 task order issued to 0.4.0_DT_ClientPlatform with J2 blocked-on-J1 dependency noted.</criterion>
    <criterion id="4">J4 NOT issued. ADVI-006 flagged as next scheduling item after J3 completes.</criterion>
  </acceptance_criteria>

  <dependency_chain>
    J1 (AE: create DynamoDB table)
      -> J2 (DT: auth-handler reads table, adds JWT claims)
        -> J3 (DT: portal-authorizer passes claims to Lambda context)
          -> J4 (DE+RD: Books tab renders from advisorRole/advisorKey)  [blocked on J3 + ADVI-006]
  </dependency_chain>

  <urgency_note>
    0.4.0_DT is blocked on J1+J2+J3 for the Books tab (J4).
    DT's current unblocked work (B1/B2 deploys) is complete.
    This is the next DT stream. Prioritize J1 issuance immediately so AE can begin
    and DT can proceed to J2/J3 as soon as the table exists.
  </urgency_note>

</task_order>
```
