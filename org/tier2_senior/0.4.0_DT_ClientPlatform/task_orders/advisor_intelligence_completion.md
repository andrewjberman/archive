# Task Order: AdvisorIntelligence Deploy Completion — 0.4.0_DT_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-dt-advisor-intelligence-completion</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Deploy all Lambda and EC2 script updates produced by 0.4.0_DS_ClientPlatform as part
    of the AdvisorIntelligence completion work. Four deployment streams: B1 (publisher with
    adv_drill + cla_timeseries), B2 (script 10 stacked bar data), F (advisor-publisher L4
    fields for Books tab), and J (firmId auth refactor — not blocking). Each stream is
    gated by DS committing code and updating data_contract.xml first.
  </objective>

  <references>
    <ref>docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref>org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_map.xml</ref>
    <ref>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</ref>
    <ref>infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</ref>
    <ref>infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py</ref>
    <ref>infra/aws/terraform/bd-pipeline/</ref>
    <ref>docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md</ref>
    <ref>docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md</ref>
  </references>

  <scope>
    <files>
      <file action="modify">infra/aws/terraform/bd-pipeline/lambdas.tf</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="modify">org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_map.xml</file>
      <file action="modify">infra/aws/terraform/bd-pipeline/CHANGELOG.json</file>
    </files>
  </scope>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM B1 — Deploy bd-portal-publisher (adv_drill + cla_timeseries) -->
    <!-- BLOCKED: requires DS A1 + A2 committed + data_contract.xml updated -->
    <!-- ================================================================ -->
    <requirement id="B1.1">
      GATE: Before beginning B1, confirm that 0.4.0_DS has committed changes to
      bd-portal-publisher/lambda_function.py covering both adv_drill (A1) and
      cla_timeseries (A2), AND has updated data_contract.xml for both shapes.
      Do not deploy a partial update — adv_drill and cla_timeseries must deploy together.
    </requirement>
    <requirement id="B1.2">
      Deploy bd-portal-publisher Lambda following LAMBDA_DEPLOYMENT_PROTOCOL.md:
        1. Run build-and-upload.sh for bd-portal-publisher
        2. Update infra/aws/lambda/ci/lambda-source-map.json
        3. git commit (source map update)
        4. terraform plan -target=module.bd_portal_publisher (verify change is code-only, no infra change)
        5. terraform apply
        6. Verify 0-diff plan
        7. Update deployment_map.xml (current_tag to bd-vX.Y.Z+1)
        8. Record deploy + tag + git push --follow-tags
      Target: infra/aws/terraform/bd-pipeline/
      Tag format: bd-vX.Y.Z+1 (increment patch from bd-v2.14.0)
    </requirement>
    <requirement id="B1.3">
      Post-deploy verification: invoke publisher Lambda manually or confirm via CloudWatch
      that the new timeseries_chart.json S3 output contains adv_drill and cla.total fields.
      Document the verification in your session log Deployment Sequence table.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM B2 — Deploy script 10 EC2 update (stacked bar data)       -->
    <!-- BLOCKED: requires DS A3 committed + data_contract.xml updated    -->
    <!-- ================================================================ -->
    <requirement id="B2.1">
      GATE: Before beginning B2, confirm that 0.4.0_DS has committed script 10 changes
      covering stacked_bar (5 periods) and rolling_1y output, AND has updated
      data_contract.xml for the new advisor_rolling_flows.json shape.
    </requirement>
    <requirement id="B2.2">
      Deploy script 10 to the bd-gold-layer-runner EC2 instance following
      EC2_CODE_DEPLOYMENT_STANDARD.md (S3 artifact model):
        1. Write script locally (DS already committed) — upload to S3
        2. EC2 pulls from S3 and executes
        3. Verify advisor_rolling_flows.json output in S3 has stacked_bar and rolling_1y fields
      Do NOT write code directly on EC2. Artifact flows repo -> S3 -> EC2.
      Coordinate with 0.6.0_AE_PartnerETL if EC2 instance requires IAM permission changes.
    </requirement>
    <requirement id="B2.3">
      After successful EC2 run: spot-check advisor_rolling_flows.json in S3.
      Confirm stacked_bar.architects.qtd and stacked_bar.architects.ytd are non-empty.
      Confirm rolling_1y.architects has entries with date + value per point.
      Document spot-check output in session log.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM F — Deploy bd-portal-advisor-publisher (Books L4 fields)  -->
    <!-- BLOCKED: requires Stream E (DS data contract + code) + Stream D  -->
    <!-- ================================================================ -->
    <requirement id="F.1">
      BLOCKED: Do not begin Stream F until both:
        (a) Stream D (Books design thread) has completed with a thread receipt, AND
        (b) Stream E (DS Books data contract + publisher code update) is committed
            with data_contract.xml updated for L4 Books fields.
    </requirement>
    <requirement id="F.2">
      When gates are met: deploy bd-portal-advisor-publisher Lambda following the same
      LAMBDA_DEPLOYMENT_PROTOCOL.md sequence as B1.
      Verify that clients/{clientKey}.json S3 output contains the L4 fields identified
      in Stream E (holdings, lots, tax liability summary).
    </requirement>
    <requirement id="F.3">
      Update deployment_map.xml and tag as bd-vX.Y.Z for this deploy.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM J — firmId auth refactor (NOT BLOCKING COMPLETION)        -->
    <!-- Coordinate with 0.7.0_AE_CloudOps                               -->
    <!-- ================================================================ -->
    <requirement id="J.1">
      Schedule Stream J AFTER all B1, B2, F streams are complete and Books tab
      is implemented. This is a security hardening step, not a completion blocker.
    </requirement>
    <requirement id="J.2">
      When AE CloudOps has confirmed the Cognito custom:firmId claim is configured
      and returns the correct value in the JWT authorizer context:
        Update opal-partners-data Lambda to read firmId from requestContext.authorizer
        (Cognito claim) instead of the query string parameter.
        Remove firmId from all query string handling in that Lambda.
    </requirement>
    <requirement id="J.3">
      Deploy via Terraform (bd-pipeline or portal-notifications module, wherever
      opal-partners-data is managed). Tag and document per standard protocol.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">B1: bd-portal-publisher deployed, 0-diff plan verified, adv_drill and cla.total confirmed in S3 output.</criterion>
    <criterion id="2">B2: script 10 executed on EC2, advisor_rolling_flows.json in S3 has stacked_bar and rolling_1y with non-empty data.</criterion>
    <criterion id="3">F: advisor-publisher deployed, L4 fields (holdings, lots, tax) confirmed in clients/{clientKey}.json.</criterion>
    <criterion id="4">J: opal-partners-data Lambda reads firmId from JWT authorizer context, no query string fallback.</criterion>
    <criterion id="5">deployment_map.xml updated after each deploy. CHANGELOG.json updated. Tags pushed.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>NEVER deploy without DS's data_contract.xml update committed first. That update is the quality gate.</constraint>
    <constraint>NEVER use aws lambda update-function-code. Terraform only.</constraint>
    <constraint>NEVER write code on EC2 directly. S3 artifact model only (EC2_CODE_DEPLOYMENT_STANDARD.md).</constraint>
    <constraint>B1 and B2 are independent — they can deploy in any order once their respective DS gates are met.</constraint>
    <constraint>Stream J must coordinate with 0.7.0_AE_CloudOps. Do not modify Cognito config yourself — AE owns that.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
    <constraint>Update deployment_map.xml AFTER apply reaches 0-diff, BEFORE git tag.</constraint>
    <constraint>NOTE: You have no prior session logs. Your first activation session log will be the pre-flight signal for the COO that you are oriented. Write it after reviewing this task order and your deployment_map.xml.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="B1 blocked by A1+A2; B2 blocked by A3; F blocked by E"/>
    <dependency agent="2.0.0_SA_COO" task="Stream-D-thread" status="pending" note="F blocked until D thread completes"/>
    <dependency agent="0.7.0_AE_CloudOps" task="advisor_intelligence_firmid_auth" status="pending" note="J requires AE Cognito claim config first"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">bd-pipeline terraform tag for B1 deploy (bd-vX.Y.Z+1)</deliverable>
    <deliverable type="commit">EC2 script 10 artifact deployed to S3 + run on bd-gold-layer-runner</deliverable>
    <deliverable type="commit">bd-pipeline terraform tag for F deploy (Books L4 publisher)</deliverable>
    <deliverable type="commit">bd-pipeline terraform tag for J deploy (firmId auth)</deliverable>
    <deliverable type="document">deployment_map.xml updated after each deploy</deliverable>
    <deliverable type="document">Session log with Deployment Sequence tables for B1, B2, F</deliverable>
  </deliverables>
</task_order>
```
