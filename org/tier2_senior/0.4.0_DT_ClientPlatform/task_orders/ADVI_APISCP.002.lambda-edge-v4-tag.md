<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-lambda-edge-v4-tag</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <phase>2</phase>
  </metadata>

  <objective>
    Tag the Lambda@Edge v4 deployment that was committed at 4eff8dee but never tagged.
    Per deployment protocol, all deployments must be tagged for provenance tracking.
    Lambda@Edge is not Terraform-managed, but the deployment still needs a git tag.
  </objective>

  <scope>
    <files>
      <!-- No files to modify. Tag only. -->
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create an annotated git tag for the Lambda@Edge v4 deployment:
        git tag -a shared-advisor-router-v4 4eff8dee -m "Lambda@Edge shared-advisor-router v4 -- dynamic S3 origin routing via X-Firm-Id. Deployed to CloudFront EVTSA9VEHNZVH, Lambda version :4. OAC auth model (E24L6358YRRKAE)."
    </requirement>
    <requirement id="2">
      Push the tag: git push origin shared-advisor-router-v4
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Tag shared-advisor-router-v4 exists on commit 4eff8dee</criterion>
    <criterion id="2">Tag pushed to remote</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Tag the EXISTING commit 4eff8dee. Do not create a new commit.</constraint>
  </constraints>

  <dependencies>
    <!-- None. Deployment already complete. -->
  </dependencies>

  <references>
    <ref type="commit">4eff8dee (feat(lambda-edge): shared-advisor-router v4)</ref>
    <ref type="deploy_log">org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-03-10/advi_apiscp_lambda_edge_v4_deploy.md</ref>
  </references>

  <deliverables>
    <deliverable type="tag">shared-advisor-router-v4 on commit 4eff8dee</deliverable>
  </deliverables>
</task_order>
