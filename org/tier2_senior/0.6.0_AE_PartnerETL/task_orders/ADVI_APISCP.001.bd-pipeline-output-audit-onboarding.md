<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-bd-pipeline-output-audit-onboarding</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
  </metadata>

  <objective>
    Verify and document the bd-pipeline gold output path convention. Confirm the bd-portal-publisher
    Lambda writes all output to opal-data-bd/gold/ with NO side-writes to any other bucket.
    Produce a new partner onboarding checklist as a deliverable. Update pipeline_inventory.xml
    with the bucket separation invariant.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Audit bd-portal-publisher Lambda (infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py):
      - Confirm OUTPUT_BUCKET = 'opal-data-bd' (or equivalent)
      - Confirm all _save_json() calls write to gold/ prefix
      - Confirm ZERO calls to opal-data-portal-v2 for any advisor-intelligence path
      - Check bd-portal-advisor-publisher similarly
    </requirement>
    <requirement id="2">
      Audit EC2 gold scripts (scripts 07, 09, 10, 11 run by bd-gold-detail-generator):
      - Confirm they upload to opal-data-bd/gold/ exclusively
      - Confirm no writes to opal-data-portal-v2
      Reference: infra/aws/ec2/bd-gold-detail-generator/user-data.sh
    </requirement>
    <requirement id="3">
      Verify lambda-source-map.json entries for bd-portal-publisher and
      bd-portal-advisor-publisher are current.
    </requirement>
    <requirement id="4">
      Update pipeline_inventory.xml to document the gold output contract:
        Output: s3://opal-data-bd/gold/{filename}.json
        Pattern: opal-data-{firmId}/gold/ for all partner pipelines
        Never: opal-data-portal-v2/ (any prefix) for partner data
    </requirement>
    <requirement id="5">
      Write a new partner onboarding checklist as a deliverable at:
        org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/partner-onboarding-checklist.md

      Must include:
      1. Create opal-data-{firmId} S3 bucket with versioning enabled
      2. Attach CloudFront access bucket policy to opal-data-{firmId}
         (principal depends on OAC vs OAI — see thread ADVI_APISCP-001 findings;
          DT will document the exact policy template during preflight discovery)
      3. Create FIRM#{firmId} DynamoDB record in opal-users-v2 with s3Bucket: opal-data-{firmId}
      4. Write all gold output to s3://opal-data-{firmId}/gold/
      5. Never write to opal-data-portal-v2
      6. No Lambda@Edge code changes needed (router constructs bucket from firmId)
      NOTE: Thread ADVI_APISCP-001 found that S3 access is per-bucket (no wildcard).
      Step 2 is REQUIRED for CloudFront to serve data from the new bucket.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">bd-portal-publisher confirmed to write only to opal-data-bd/gold/</criterion>
    <criterion id="2">No pipeline writes to opal-data-portal-v2/json/advisor-intelligence/</criterion>
    <criterion id="3">pipeline_inventory.xml documents bucket separation invariant</criterion>
    <criterion id="4">Partner onboarding checklist exists as a deliverable</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>This is audit + documentation only. Do not modify Lambda code or deploy anything.</constraint>
    <constraint>The opal-data-portal-v2/json/advisor-intelligence/ path was deleted 2026-03-10. It must never be recreated by any pipeline.</constraint>
  </constraints>

  <dependencies>
    <!-- No blocking dependencies. Can proceed immediately in parallel with DT. -->
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_APISCP_PRD.md</ref>
  </references>

  <deliverables>
    <deliverable type="document">Partner onboarding checklist (org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/partner-onboarding-checklist.md)</deliverable>
    <deliverable type="document">Updated pipeline_inventory.xml with bucket separation invariant</deliverable>
    <deliverable type="document">Session log with audit findings</deliverable>
  </deliverables>
</task_order>
