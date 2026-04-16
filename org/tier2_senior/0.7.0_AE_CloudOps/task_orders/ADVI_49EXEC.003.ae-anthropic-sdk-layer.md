<task_order>
  <metadata>
    <id>ADVI_49EXEC.003</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- Executed by AE 0.6 opportunistically (commit c0a00bcc 2026-04-16) while AE 0.7 was on CDRS_TFIMPT sprint. Layer anthropic-sdk-deps built per pins. Owner reassignment AE 0.7 -> AE 0.6 not re-scoped in filename; evidence commit is authoritative. -->
    <project_code>ADVI_49EXEC</project_code>
    <priority>P1 (gates TO 2 + TO 4 — Lambda layer prerequisite)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_49EXEC.md §4.2 + §7 TO 3</ref>
    <ref type="related">infra/aws/lambda/layers/news-trending-deps/requirements.txt (existing Python 3.12 layer pattern reference)</ref>
  </references>

  <objective>
    New Lambda layer `anthropic-sdk-deps` for Python 3.12. Pinned versions of `anthropic` + `httpx` + `httpcore` (and any transitive deps anthropic needs that aren't in the runtime).

    Manifest at `infra/aws/lambda/layers/anthropic-sdk-deps/requirements.txt`.

    Build + upload to `s3://opal-313476888478-lambda-layers/anthropic-sdk-deps.zip` per the existing layer convention.

    Output: layer ARN registered, version logged for downstream Lambda config (TO 4 DT consumes).
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/lambda/layers/anthropic-sdk-deps/requirements.txt</file>
      <file action="create">infra/aws/lambda/layers/anthropic-sdk-deps/build.sh (or follow existing pattern in news-trending-deps)</file>
    </files>
    <s3_writes>
      <write>s3://opal-313476888478-lambda-layers/anthropic-sdk-deps.zip</write>
    </s3_writes>
    <terraform>
      <write>infra/aws/terraform/shared-infra/layers.tf (or wherever existing layers are declared) — `aws_lambda_layer_version.anthropic_sdk_deps`</write>
    </terraform>
  </scope>

  <wire_contract>
    Layer ARN: `arn:aws:lambda:us-east-1:313476888478:layer:anthropic-sdk-deps:{version}`. Compatible runtimes: `python3.12`. TO 4 DT references this ARN in Lambda function config.
  </wire_contract>

  <acceptance_criteria>
    1. requirements.txt with pinned versions (anthropic, httpx, httpcore, plus any transitive non-runtime deps).
    2. Layer zip built + uploaded to `s3://opal-313476888478-lambda-layers/anthropic-sdk-deps.zip` with documented etag.
    3. Terraform `aws_lambda_layer_version` resource declared, applied 0-diff, ARN logged.
    4. Tag `shared-infra-v{X.Y.Z}` (next patch in series) created + pushed `--follow-tags`.
    5. CHANGELOG.json entry recorded.
    6. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    7. MCP COMPLETE to COO + CTO with: layer ARN+version, requirements.txt content, S3 etag, terraform tag.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat infra/aws/lambda/layers/news-trending-deps/requirements.txt</run>
        <expect>Existing pattern visible; informs build script reuse.</expect>
        <if_mismatch>Reference an alternative existing layer build script.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit + apply">
      <step>
        <run>terraform plan</run>
        <expect>Adds `aws_lambda_layer_version.anthropic_sdk_deps` only; no other diffs.</expect>
        <if_mismatch>Investigate unexpected drift.</if_mismatch>
      </step>
      <step>
        <run>terraform apply</run>
        <expect>Apply success; ARN populated.</expect>
        <if_mismatch>Surface to COO + CTO.</if_mismatch>
      </step>
      <step>
        <run>terraform plan</run>
        <expect>0-diff post-apply.</expect>
        <if_mismatch>Drift; fix before tag.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Layer consumed by TO 4 (DT Lambda config) and indirectly by TO 2 (DS Lambda code imports).
  </cross_domain_coordination>

  <dependencies>
    <none/>
  </dependencies>

  <next>
    TO 3 close → unblocks TO 4 (DT can declare Lambda function config with layer ARN).
  </next>
</task_order>
