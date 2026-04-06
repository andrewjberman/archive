<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-auth-tfimpt-001-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-06</date>
    <status>staged</status>
    <project_code>AUTH_TFIMPT</project_code>
    <priority>high</priority>
  </metadata>

  <objective>
    Import CloudFront distribution EVTSA9VEHNZVH into Terraform state under
    the portal-auth pipeline. This is the highest-risk import in the project --
    the distribution is currently console-managed and serves all portal traffic.
  </objective>

  <scope>
    <files>
      <file action="write">infra/aws/terraform/portal-auth/cloudfront-distribution.tf</file>
      <file action="read">infra/aws/terraform/portal-auth/cloudfront.tf</file>
      <file action="read">infra/aws/terraform/portal-auth/lambda-edge.tf</file>
      <file action="read">infra/aws/terraform/portal-auth/main.tf</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="cf-import">
      **CloudFront Distribution Import**

      1. **Describe the live distribution** via AWS CLI:
         `aws cloudfront get-distribution --id EVTSA9VEHNZVH`
         Capture: origins, behaviors (paths, Lambda@Edge associations, cache policies),
         viewer certificate, aliases, WAF, error pages, geo restrictions.

      2. **Write the TF resource** in `cloudfront-distribution.tf`:
         `aws_cloudfront_distribution.portal` — match every field to the live config.
         Reference existing TF resources where possible:
         - Lambda@Edge functions from `lambda-edge.tf`
         - Cache policy from `cloudfront.tf`
         - IAM roles from `iam.tf`

      3. **Import into state**:
         `export MSYS_NO_PATHCONV=1`
         `.tools/terraform.exe -chdir=infra/aws/terraform/portal-auth import aws_cloudfront_distribution.portal EVTSA9VEHNZVH`

      4. **Achieve 0-drift**: Run `terraform plan` and resolve ALL diffs.
         CloudFront distributions have many optional fields that default differently
         between console and Terraform. Every diff must be resolved by matching the
         TF resource to the live config, NOT by letting Terraform change the live
         distribution.

      5. **Verify**: `terraform plan` shows "No changes" (0-diff).
    </deliverable>
  </deliverables>

  <tooling>
    MANDATORY: Run these compiler modules BEFORE writing any TF resource.
    They establish the dependency map that prevents phantom references.

    1. **crossref_graph** (org/modules/interpret/crossref_graph.py)
       Scope: infra/aws/terraform/portal-auth/ + infra/aws/lambda/v2_portal/auth/
       Purpose: Map all references between Lambda@Edge functions and TF resources.
       Identifies which edge functions reference which IAM roles, cache policies,
       origins, and behaviors. The graph output tells you exactly which TF resources
       the CloudFront distribution must reference -- preventing dangling refs.
       Output: authority ranking (most-referenced files), blast radius per file.

    2. **ast_extractor** (org/modules/interpret/ast_extractor.py)
       Scope: All 5 Lambda@Edge source files + portal-auth TF files
       Purpose: Extract function signatures, imports, and string literals.
       String literals contain ARN patterns, S3 paths, and CloudFront behavior
       path patterns that must match the distribution TF resource.

    3. **coverage_auditor** (org/modules/adapt/coverage_auditor.py)
       Scope: Run AFTER writing the TF resource, BEFORE import.
       Source = live CloudFront behaviors (from AWS CLI describe output).
       Registry = TF resource behaviors.
       Purpose: Verify every live behavior is represented in TF. Any gap = a
       behavior that TF would delete on apply.

    Run crossref_graph + ast_extractor first. Write TF. Run coverage_auditor.
    Then import + plan. This is the ANONYM.014 lesson: dependency maps first.
  </tooling>

  <notes>
    - THIS IS A READ-ONLY IMPORT. Do NOT run `terraform apply` until 0-diff is confirmed.
      A bad apply could take down the portal.
    - The distribution likely has many behaviors (10+) with different Lambda@Edge
      associations. Each behavior must be represented in the TF resource.
    - Cache policy `opal-scoped-advisor-by-firm` is already in cloudfront.tf --
      reference it via `aws_cloudfront_cache_policy.opal_scoped_advisor_by_firm.id`.
    - The 5 Lambda@Edge functions are already in lambda-edge.tf -- reference their
      qualified_arn for CloudFront associations.
    - CloudFront distributions are global resources -- `us-east-1` provider is correct.
    - Follow CLAUDE.md deployment rules: commit before apply, update source map, tag after deploy.
  </notes>

  <references>
    <ref type="existing_tf">infra/aws/terraform/portal-auth/</ref>
    <ref type="deployment_protocol">docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md</ref>
  </references>

  <dependencies>
    None. Can begin immediately on GO.
  </dependencies>
</task_order>
