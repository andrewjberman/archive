<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-19-bkscmp-003-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-19</date>
    <status>complete</status>
    <project_code>ADVI_BKSCMP</project_code>
  </metadata>

  <objective>
    Deploy the updated opal-partners-data Lambda (v2.8) after DS commits the WS2 Lambda
    changes (ADVI_BKSCMP.001 req 6 commit). Tag as partners-api-v1.5.0. This brings the
    new firm/advisor composition routes live so AE's gold artifacts become accessible.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_BKSCMP_PRD.md §WS4 (DT actions).
    Deployment reference: docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md.

    Current partners-api tag: partners-api-v1.4.0. Verify with:
      git tag -l "partners-api-v*" | sort -V | tail -5
    Target: partners-api-v1.5.0 (minor bump -- two new routes, new cache-control helper).

    DS gate commit: ADVI_BKSCMP.001 req 6 (Lambda v2.8 commit to CLOUD).
    DS will report the commit SHA. Confirm it exists before building.

    Known workaround: build-and-upload.sh fails on this machine (bun MSYS2 path issue).
    Use PowerShell temp script at C:/Windows/Temp/ as documented in AE5 log.
  </context>

  <scope>
    <files>
      <file action="deploy">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <file action="update">infra/aws/lambda/ci/lambda-source-map.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" priority="gate">
      GATE: Confirm DS has committed the Lambda v2.8 changes to CLOUD.
      Check: git log --oneline -- infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py
      Verify the commit message mentions "v2.8" or "ADVI_BKSCMP WS2". Do not build before confirming.
    </requirement>

    <requirement id="2">
      Build and upload the Lambda artifact:
        Use PowerShell temp script pattern (C:/Windows/Temp/build-partners-data.ps1)
        — build-and-upload.sh is broken on this machine.
      Upload to: s3://opal-313476888478-lambda-artifacts/partners-api/opal-partners-data.zip
      Record SHA256 in session log.
    </requirement>

    <requirement id="3">
      Update infra/aws/lambda/ci/lambda-source-map.json entry for opal-partners-data
      with the new SHA256 and S3 version.
      Commit under DT author:
        git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
          -m "ci(partners-api): upload opal-partners-data v2.8 (ADVI_BKSCMP)"
    </requirement>

    <requirement id="4">
      terraform plan (partners-api module). Expected: 1 to change (opal-partners-data
      in-place — s3_object_version + source_code_hash).
      terraform apply. Verify 0-diff second plan.
    </requirement>

    <requirement id="5">
      Run record-terraform-deploy.sh:
        bash infra/aws/lambda/ci/record-terraform-deploy.sh partners-api partners-api-v1.5.0
      Commit the CHANGELOG.json update:
        git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
          -m "ci: record deploy partners-api @ (commit) [skip ci]"
    </requirement>

    <requirement id="6">
      Tag and push:
        git tag -l "partners-api-v*" | sort -V | tail -5   # verify next version
        git tag -a partners-api-v1.5.0 -m "ADVI_BKSCMP: firm+advisor composition routes (v2.8)"
        git push --follow-tags
    </requirement>

    <requirement id="7">
      Update deployment_map.xml with partners-api-v1.5.0.
    </requirement>

    <requirement id="8">
      Spot-verify new routes are live (optional, can be done before AE gold run):
        Confirm that GET /api/scoped/partners/books/firm/all/composition?firmId=49financial
        returns 503 (expected — artifacts not yet in S3) rather than 404 (wrong route) or 500 (code error).
      Report deploy complete to COO. This is the gate for AE to start gold run verification
      (AE can run the gold layer before the Lambda deploy; the Lambda must be live to serve artifacts).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">DS gate commit confirmed before build</criterion>
    <criterion id="2">Artifact uploaded; SHA256 recorded in session log</criterion>
    <criterion id="3">lambda-source-map.json updated and committed</criterion>
    <criterion id="4">terraform apply complete, 0-diff second plan confirmed</criterion>
    <criterion id="5">partners-api-v1.5.0 tag pushed with --follow-tags</criterion>
    <criterion id="6">CHANGELOG.json updated via record-terraform-deploy.sh</criterion>
    <criterion id="7">Firm composition route returns 503 (not 404/500) before S3 artifacts exist</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>GATE: Do not build before confirming DS Lambda v2.8 commit is on CLOUD</constraint>
    <constraint>Always check actual git tags before tagging -- git tag -l "partners-api-v*" | sort -V | tail -5</constraint>
    <constraint>Use PowerShell temp script for zip + upload (build-and-upload.sh broken on this machine)</constraint>
    <constraint>No emojis in commit messages or Terraform apply output (CLAUDE.md rule 13)</constraint>
    <constraint>lambda-source-map.json must be updated for every Lambda deploy</constraint>
    <constraint>Export MSYS_NO_PATHCONV=1 before AWS CLI commands with ARN or S3 paths</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_BKSCMP.001 req 6" status="pending">
      opal-partners-data v2.8 Lambda committed to CLOUD -- hard gate for build
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">opal-partners-data v2.8 deployed; tagged partners-api-v1.5.0</deliverable>
    <deliverable type="document">Session log with SHA256, 0-diff confirmation, tag</deliverable>
  </deliverables>
</task_order>
