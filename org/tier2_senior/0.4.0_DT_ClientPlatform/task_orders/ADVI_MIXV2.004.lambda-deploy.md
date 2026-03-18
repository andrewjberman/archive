<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-03-17-004-dt-lambda-deploy</id>
    <issued_by>0.4.0_DS_ClientPlatform</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-17</date>
    <status>complete</status>
    <project_code>ADVI_MIXV2</project_code>
  </metadata>

  <objective>
    Deploy two rounds of Lambda changes to opal-partners-data:
      (1) pct scale fix from ADVI_MIXV2.001 — immediate, unblocks the 5000% display bug
      (2) new firm/mix-views and advisor/mix-views endpoints from ADVI_MIXV2.002
    Both rounds go through Terraform. Full instructions in
    docs/briefs/devops-brief-mixv2-001.md and docs/briefs/devops-brief-mixv2-002.md.
  </objective>

  <scope>
    <files>
      <file action="deploy">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      DEPENDENCY: Do not begin until DS confirms both ADVI_MIXV2.001 (pct fix) and
      ADVI_MIXV2.002 (new endpoints) are committed to CLOUD. Read the two devops briefs
      before executing. Both rounds can be deployed together as a single Terraform cycle
      if DS has committed both before DT begins — no need to split into two separate deploys.
    </requirement>

    <requirement id="2">
      Follow the Lambda Deployment Protocol (org/ref/LAMBDA_DEPLOYMENT_PROTOCOL.md):
        1. build-and-upload.sh for opal-partners-data
        2. Update infra/aws/lambda/ci/lambda-source-map.json
        3. git commit source map
        4. terraform plan (infra/aws/terraform/partners-api/ or whichever module owns opal-partners-data)
        5. terraform apply
        6. 0-diff verify
        7. git tag partners-api-vX.Y.Z (increment from current partners-api-v1.0.0)
        8. git push --follow-tags
    </requirement>

    <requirement id="3">
      Verify pct fix (WS1): after deploy, open Assets Overview on portal → Mix toggle →
      FirmCompositionSnapshot pie should show percentages like "62.5%", not "6250.0%".
    </requirement>

    <requirement id="4">
      Verify new endpoints (WS3/WS6): curl both new endpoints and confirm 200 responses
      with the correct shape. If AE (task order 003) has not yet run 06b to produce the
      S3 artifacts, endpoints will return 503 — this is expected behavior (serve_s3_json
      returns 503 for missing artifacts). Document this state in the session log.
    </requirement>

    <requirement id="5">
      Update deployment_map.xml after 0-diff plan.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Terraform apply reaches 0-diff</criterion>
    <criterion id="2">Portal composition snapshots show correct percentages (0-100%, not 3000-6000%)</criterion>
    <criterion id="3">partners-api-vX.Y.Z tag created and pushed</criterion>
    <criterion id="4">deployment_map.xml updated</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Terraform is the only Lambda deployment mechanism — no aws lambda update-function-code</constraint>
    <constraint>Commit before apply per CLAUDE.md deployment rules</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MIXV2.001" status="pending">
      DS pct fix must be committed before DT deploys
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MIXV2.002" status="pending">
      DS new endpoints must be committed before DT deploys (can deploy both together)
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Source map update committed</deliverable>
    <deliverable type="commit">deployment_map.xml updated</deliverable>
    <deliverable type="document">partners-api-vX.Y.Z tag pushed</deliverable>
    <deliverable type="document">Session log confirming pct fix verified on portal</deliverable>
  </deliverables>
</task_order>
