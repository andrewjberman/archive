<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-auth-tfimpt-003-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-06</date>
    <status>complete</status>
    <project_code>AUTH_TFIMPT</project_code>
  </metadata>

  <objective>
    Assess the opal-portal-lambda-role (shared by 13 Lambda functions across
    multiple pipelines) and determine which Terraform pipeline should own it.
    Currently referenced as a data source in portal-auth/iam.tf. Needs to
    become a managed resource in exactly one pipeline.
  </objective>

  <scope>
    <files>
      <file action="read">infra/aws/terraform/portal-auth/iam.tf</file>
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="read">infra/aws/terraform/*/lambdas.tf</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="role-assessment">
      **Shared Role Ownership Assessment**

      1. **Inventory all 13 functions** using opal-portal-lambda-role:
         `aws iam list-role-policies --role-name opal-portal-lambda-role`
         `aws iam list-attached-role-policies --role-name opal-portal-lambda-role`
         Cross-reference with lambda-source-map.json to identify which pipelines
         deploy which functions.

      2. **Map role policies** to the resources they grant access to:
         Which DynamoDB tables, S3 buckets, Secrets Manager paths, etc.?
         Which policies are shared vs function-specific?

      3. **Recommend ownership**:
         - Option A: portal-auth owns the role (centralized auth infra)
         - Option B: shared-infra owns the role (shared resource pattern)
         - Option C: Split the role into per-pipeline roles (cleanest but most work)
         Recommend one option with rationale. Consider: which pipeline deploys
         most frequently? Which has the broadest blast radius if the role changes?

      4. **Write migration plan**: Step-by-step to move from data source to
         managed resource in the chosen pipeline. Include rollback steps.
         Do NOT execute the migration -- deliverable is the plan only.
    </deliverable>
  </deliverables>

  <tooling>
    MANDATORY: Run these compiler modules BEFORE writing the assessment.
    The crossref_graph is the primary tool here -- it answers the ownership
    question with data instead of guesswork.

    1. **crossref_graph** (org/modules/interpret/crossref_graph.py)
       Scope: ALL Lambda source dirs that use opal-portal-lambda-role +
       ALL TF pipeline dirs (portal-auth/, bd-pipeline/, partners-api/,
       yang-pipeline/, news-pipeline/, market-overview/, shared-infra/).
       Purpose: Build the full dependency graph of which files reference
       the shared role. The authority ranking tells you which pipeline has
       the most integrations with this role -- that's the natural owner.
       Blast radius = in_degree of the role resource node.

    2. **ast_extractor** (org/modules/interpret/ast_extractor.py)
       Scope: All 13 Lambda functions using the role.
       Purpose: Extract imports and function signatures to understand what
       each Lambda actually does. Categorize by: auth functions, data functions,
       routing functions. The category split informs whether one role makes
       sense or whether per-pipeline split (Option C) is warranted.

    3. **coverage_auditor** (org/modules/adapt/coverage_auditor.py)
       Scope: Source = IAM policies attached to the role (from AWS CLI).
       Registry = resource ARNs across all TF pipelines.
       Purpose: Find policy grants that don't map to any TF-managed resource
       (orphaned permissions) or TF resources that aren't in the policy
       (missing grants). This reveals whether the role is cleanly scoped
       or has accumulated drift.

    The crossref_graph output IS the assessment's primary data source.
    If the graph shows 10/13 functions are in partners-api, that's the answer.
  </tooling>

  <notes>
    - This is an ASSESSMENT, not an execution task. Deliverable is a written
      plan with recommendation. COO and CTO review before execution.
    - The role is currently console-managed. Importing it into TF changes nothing
      about the role itself, but the owning pipeline's `terraform apply` will
      then manage it -- so the choice of pipeline matters.
    - Check deployment_map.xml for function-to-pipeline mappings.
    - Consider blast radius: if portal-auth owns it and an auth deploy goes wrong,
      it could affect all 13 functions.
  </notes>

  <references>
    <ref type="existing_tf">infra/aws/terraform/portal-auth/iam.tf</ref>
    <ref type="source_map">infra/aws/lambda/ci/lambda-source-map.json</ref>
  </references>

  <dependencies>
    None. Can run in parallel with .001 and .002.
  </dependencies>
</task_order>
