<task_order>
  <metadata>
    <id>ADVI_49EXEC.007</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- deploy complete 2026-04-27, tag exec-summary-v0.1.0. Lambda ImportModuleError blocker → DS fix pending (exec_summary package not vendored) -->
    <project_code>ADVI_49EXEC</project_code>
    <priority>P1 (project closeout — first deploy + tag exec-summary-v0.1.0)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_49EXEC.md §4.1 (data flow) + §7 TO 7</ref>
    <ref type="prereq">ADVI_49EXEC.004 (Terraform module shipped at exec-summary-v0.0.1)</ref>
    <ref type="prereq_ext">AE 0.6 EventBridge signal-format confirmation (COO query 221116Z)</ref>
  </references>

  <objective>
    Wire EventBridge rule from gold-chain-complete signal to `exec-summary-generator` Lambda. Coord with AE 0.6 on the signal's exact event pattern (do NOT assume — confirm from existing chain wiring).

    Initial deploy of the full stack (Lambda + IAM + EventBridge + alarms). Tag `exec-summary-v0.1.0`.

    Post-deploy verification: trigger a manual EventBridge test event (or wait for next nightly chain-complete fire), confirm Lambda invokes, confirm at least one `platinum/advisors/{id}/exec_summary.json` lands on S3 within the timeout window.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/terraform/exec-summary/main.tf (replace EventBridge placeholder rule with real signal pattern from AE 0.6)</file>
      <file action="modify">infra/aws/terraform/exec-summary/CHANGELOG.json (v0.1.0 entry)</file>
    </files>
  </scope>

  <wire_contract>
    EventBridge rule fires `exec-summary-generator` on every gold-chain-complete event. Lambda processes all active advisors; writes one S3 artifact per. Tag `exec-summary-v0.1.0`.
  </wire_contract>

  <acceptance_criteria>
    1. EventBridge event pattern matches AE 0.6 confirmed signal format (exact source + detail-type + bus).
    2. `terraform plan` 0-diff after apply.
    3. Tag `exec-summary-v0.1.0` created + pushed `--follow-tags`.
    4. Post-deploy verification: test event triggers Lambda, Lambda runs to completion (or surfaces clear error), at least one S3 artifact lands.
    5. CloudWatch alarms armed (TokensIn 2x rolling, AdvisorsProcessed > 5000 ceiling).
    6. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    7. MCP COMPLETE to COO + CTO with: tag + EventBridge rule ARN + sample S3 artifact path + CloudWatch metric snapshot.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-routes trace exec-summary-generator</run>
        <expect>Trigger path EventBridge → Lambda complete; reads + writes correct S3 prefixes.</expect>
        <if_mismatch>Investigate trace gaps.</if_mismatch>
      </step>
      <step>
        <run>cat AE 0.6 EventBridge signal-format confirmation MCP (link from inbox)</run>
        <expect>Source + detail-type + bus + payload fields documented.</expect>
        <if_mismatch>Re-query AE 0.6; do NOT assume signal format.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before apply">
      <step>
        <run>terraform plan</run>
        <expect>EventBridge rule pattern updated; no other unintended drift.</expect>
        <if_mismatch>Investigate.</if_mismatch>
      </step>
      <step>
        <run>terraform apply</run>
        <expect>Apply success.</expect>
        <if_mismatch>Surface to COO + CTO.</if_mismatch>
      </step>
      <step>
        <run>terraform plan</run>
        <expect>0-diff post-apply.</expect>
        <if_mismatch>Drift.</if_mismatch>
      </step>
      <step>
        <run>comp-iam gaps</run>
        <expect>No new gaps anywhere.</expect>
        <if_mismatch>Audit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after deploy">
      <step>
        <run>aws events put-events --entries '[{...test event...}]' &amp;&amp; sleep 60 &amp;&amp; aws s3 ls s3://opal-data-bd/platinum/advisors/{test_advisor}/exec_summary.json</run>
        <expect>Test event delivered; sample S3 artifact present.</expect>
        <if_mismatch>Investigate Lambda invocation chain.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Hard-blocker: AE 0.6 EventBridge signal-format confirmation. COO query at 221116Z.
    - Lambda code from TO 2; layer from TO 3; Terraform shell from TO 4. Final wiring + first deploy here.
  </cross_domain_coordination>

  <dependencies>
    <dependency to="ADVI_49EXEC.004" status="staged"/>
    <dependency description="AE 0.6 EventBridge signal-format confirmation (external, query firing now)" status="pending"/>
  </dependencies>

  <next>
    TO 7 close = ADVI_49EXEC v1 LIVE. v1.5 work (Refresh button, cta_path click-through) on backlog.
  </next>
</task_order>
