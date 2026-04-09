<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-09-49push-019-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-09</date>
    <status>complete</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>5</wave>
    <phase>P3</phase>
  </metadata>

  <objective>
    Deploy the updated shared-advisor-router (Lambda@Edge) and opal-partners-data (Lambda)
    via Terraform. These contain the platinum routing rules and M1 Lambda handlers committed
    in .011 + M1.
  </objective>

  <context>
    Gold rebuild is complete. Platinum files are in S3. The serving layer code changes
    are committed (commits 393b0f25). Now Terraform needs to deploy them.

    Changes to deploy:
    - shared-advisor-router/index.mjs: platinum/ rewrite rules + selective PII block (403 for
      advisor/client summary.json, allow firm/* and non-PII entity paths)
    - opal-partners-data/lambda_function.py: 2 new platinum handlers
      (handle_platinum_advisor_summary, handle_platinum_client_summary) + 2 route swaps
      (mix-timeseries, concentration reading from platinum/)

    Deployment protocol: docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md
    Terraform strategy: infra/aws/TERRAFORM_PIPELINE_STRATEGY.md
  </context>

  <requirements>
    <requirement id="1">
      Push commits to remote first: git push origin CLOUD
    </requirement>

    <requirement id="2">
      For shared-advisor-router (Lambda@Edge):
      - Build and upload artifact via build-and-upload.sh
      - Terraform plan in the portal-auth pipeline (shared-advisor-router is managed there)
      - Terraform apply
      - Verify 0-diff plan after apply
    </requirement>

    <requirement id="3">
      For opal-partners-data (Lambda):
      - Build and upload artifact via build-and-upload.sh
      - Terraform plan in the partners-api pipeline
      - Terraform apply
      - Verify 0-diff plan after apply
    </requirement>

    <requirement id="4">
      After both deploys, verify:
      - CloudFront invalidation for Lambda@Edge (may take a few minutes to propagate)
      - Hit a platinum firm-level URL and confirm 200 (e.g., /api/scoped/advisor-intelligence/platinum/firm/leaderboard.json)
      - Hit a blocked entity URL and confirm 403 (e.g., /api/scoped/advisor-intelligence/platinum/advisors/test/summary.json)
    </requirement>

    <requirement id="5">
      Tag after successful deploy:
      - partners-api tag (check latest: git tag -l "partners-api-v*" | sort -V | tail -5)
      - portal-auth tag (check latest: git tag -l "portal-auth-v*" | sort -V | tail -5)
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>Both Lambdas deployed via Terraform with 0-diff verification</deliverable>
    <deliverable>Tags created and pushed</deliverable>
    <deliverable>Message to COO confirming deploy + verification results</deliverable>
  </deliverables>
</task_order>
