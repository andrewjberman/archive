<task_order>
  <metadata>
    <id>ADVI_49EXEC.002</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to><!-- base; reroute to ~ if needed -->
    <date>2026-04-15</date>
    <status>staged</status><!-- HARD GATE: TO 1 trigger evaluator complete -->
    <project_code>ADVI_49EXEC</project_code>
    <priority>P1 (consumer of TO 1; produces artifact TO 6 reads)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_49EXEC.md §3 (schema) + §5 (security/PII) + §7 TO 2</ref>
    <ref type="prereq">ADVI_49EXEC.001</ref>
    <ref type="prereq_layer">ADVI_49EXEC.003 (anthropic-sdk-deps Lambda layer must be available before this Lambda runs)</ref>
  </references>

  <objective>
    Wrap TO 1's TriggeredSlot output: for each triggered slot, build the prompt, call `claude-sonnet-4-6` via anthropic SDK, validate response against per-slot schema (length cap 240 chars per detail field, URL strip + reject, PII assert, parse). Write final artifact to `s3://opal-data-bd/platinum/advisors/{id}/exec_summary.json` per PRD §3 schema (advisor_id, firm_id, generated_at, model, input_hash, bullets[], permissions_scope).

    Unit tests with mocked anthropic responses covering: happy path per slot, schema-fail (drop slot), PII-detected (assertion error), URL-detected (regex strip + reject).

    **PII assertion mandatory in code path:** `assert PII_PATTERN.search(prompt) is None` per PRD §5.1. Defense-in-depth — pseudonymized inputs should never produce cleartext outputs but the assertion enforces it.

    **Cost telemetry:** emit CloudWatch metrics per PRD §4.2 (`ExecSummaryAdvisorsProcessed`, `ExecSummaryLLMCallsMade`, `ExecSummaryTokensIn/Out`, `ExecSummaryEmptyAdvisors`, `ExecSummarySlotDropped`).

    **Output:** Lambda handler at `infra/aws/lambda/exec-summary-generator/lambda_function.py` + supporting modules. Imports anthropic SDK from layer (TO 3).
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/lambda/exec-summary-generator/lambda_function.py</file>
      <file action="create">infra/aws/lambda/exec-summary-generator/prompts/*.txt (per-slot prompt templates)</file>
      <file action="create">tests/exec_summary/test_llm_generator.py</file>
    </files>
    <s3_writes>
      <write>s3://opal-data-bd/platinum/advisors/{advisor_id}/exec_summary.json — one per advisor per nightly</write>
    </s3_writes>
  </scope>

  <wire_contract>
    Lambda handler input (EventBridge): chain-complete signal payload (TO 7 wires this). Iterates active advisors via platinum/advisors/ enumeration. Lambda IAM (per TO 4 DT spec): `s3:GetObject` on platinum/advisors/* + platinum/leaderboards/*, `s3:PutObject` on platinum/advisors/*/exec_summary.json, `secretsmanager:GetSecretValue` on `anthropic-api-key` ARN, `cloudwatch:PutMetricData`.
  </wire_contract>

  <acceptance_criteria>
    1. Per PRD §3 schema artifact written; all required fields populated.
    2. Per-slot prompt templates produce LLM responses within 240-char detail cap.
    3. URL-strip + PII-assert + schema-parse validation paths all unit-tested.
    4. Cost telemetry metrics emitted per invocation.
    5. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    6. MCP COMPLETE to COO + CTO with: Lambda code path, S3 sample artifact, test pass count, sample CloudWatch metric values from local mock invocation.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-iam service exec-summary-generator</run>
        <expect>Initial run flags MISSING permissions: `s3:PutObject` on `platinum/advisors/*/exec_summary.json` + `secretsmanager:GetSecretValue` on `anthropic-api-key` (TO 4 will add these via iam.tf).</expect>
        <if_mismatch>If permissions already present, TO 4 may have shipped iam.tf early — coordinate.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>pytest tests/exec_summary/test_llm_generator.py -v</run>
        <expect>All cases PASS including PII-assert + URL-strip + schema-fail-drop.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
      <step>
        <run>comp-iam service exec-summary-generator</run>
        <expect>After TO 4 iam.tf landed: zero MISSING permissions.</expect>
        <if_mismatch>Coordinate with DT on TO 4 iam.tf gap.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>aws lambda invoke (after TO 4 deploys) — sample single-advisor invocation</run>
        <expect>S3 artifact written; metrics emitted; no PII assertion failures.</expect>
        <if_mismatch>Investigate prompt or trigger eval.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Consumes TO 1 TriggeredSlot output (DS-internal contract).
    - Writes `platinum/advisors/{id}/exec_summary.json` consumed by TO 6 (DE FE).
    - Imports anthropic SDK from TO 3 layer.
    - Lambda deployed by TO 4 (DT Terraform module owns IAM + EventBridge wiring).
  </cross_domain_coordination>

  <dependencies>
    <dependency to="ADVI_49EXEC.001" status="staged"/>
    <dependency to="ADVI_49EXEC.003" status="staged"/>
  </dependencies>

  <next>
    TO 2 close → TO 4 DT can finalize Terraform pointing to this Lambda code path.
  </next>
</task_order>
