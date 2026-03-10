<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-ADHC001-ae-cloudops</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <thread_serial>ADHC_GPTCST-001</thread_serial>
    <thread_ref>org/threads/ADHC_GPTCST-001-openai-cost-audit-caller-inventory/</thread_ref>
  </metadata>

  <objective>
    Implement Phase 3 of ADHC_GPTCST: wire per-function OpenAI token spend into the morning
    infrastructure report. Also fix the two immediately actionable items from the audit:
    SmartX EC2 supervisor model/iteration config and the function name mismatches in the
    existing cost tracker. This work is blocked on ADHC_GPTCST.001 (OpalETL) adding OPENAI_USAGE
    log lines — coordinate or run in parallel once log lines are confirmed deployed.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/infrastructure_monitor/openai_cost_tracker.py</file>
      <file action="modify">infra/aws/lambda/infrastructure_monitor/lambda_function.py</file>
      <file action="modify">infra/aws/ec2/smartx-exporter/ai-supervisor-v2.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Fix function name mismatches in infrastructure_monitor immediately
      (unblocked, can do now):
      - In lambda_function.py: update OPENAI_LAMBDAS to canonical names from lambda-source-map.json:
        ["news-trending-analysis", "opal-news-layer3-curation", "semantic-news-layer3-curation",
        "keyword-intelligence-generator", "opal-trending-image-generator", "opal-infrastructure-monitor"]
      - In openai_cost_tracker.py: align COST_PER_CALL_BY_SERVICE keys to the same canonical names
        (add opal- prefixes where currently missing).</requirement>

    <requirement id="2">Extend openai_cost_tracker.py with token-accurate path (requires OPENAI_USAGE
      log lines from OpalETL task order to be deployed first):
      - New method: query each /aws/lambda/{function} log group for filterPattern='"OPENAI_USAGE"'
        over the last 24h.
      - Parse lines matching: OPENAI_USAGE function=X model=Y prompt=N completion=N total=N
      - Aggregate tokens by function + model.
      - Compute $ cost using a pricing table covering at minimum:
          gpt-4o, gpt-4o-mini, text-embedding-3-small, gpt-4-turbo-preview
      - Fallback: if no OPENAI_USAGE lines found for a function, fall back to existing
        "api.openai.com" call-count x empirical multiplier.</requirement>

    <requirement id="3">Wire cost summary into the morning report email. The report is plain text
      (SES Text body). Add a new section "OPENAI COST (Last 24h)" to format_report() output showing:
      - Per-function: model(s), total_tokens (24h), estimated cost ($)
      - Grand total estimated spend
      - Flag any function with no OPENAI_USAGE lines detected (may indicate log line missing).</requirement>

    <requirement id="4">SmartX EC2 supervisor (ai-supervisor-v2.py): two fixes:
      a. Switch default model from gpt-4o to gpt-4o-mini. Add escalation: only upgrade to gpt-4o
         after 3+ consecutive tool failures.
      b. Fix secret name bug: get_openai_key() currently reads 'ai/claude-api-key' which is the
         wrong secret for OpenAI. Identify the correct canonical OpenAI API key secret name (check
         other Lambdas for how they retrieve it) and update get_openai_key() accordingly.
      Deploy to EC2 via safe-ec2-deploy.sh following EC2_CODE_DEPLOYMENT_STANDARD.md.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">OPENAI_LAMBDAS and COST_PER_CALL_BY_SERVICE keys match lambda-source-map.json
      canonical names exactly.</criterion>
    <criterion id="2">Morning report email includes "OPENAI COST (Last 24h)" section with per-function
      token and cost breakdown.</criterion>
    <criterion id="3">Token-accurate path parses OPENAI_USAGE log lines when present; falls back
      gracefully when absent.</criterion>
    <criterion id="4">SmartX supervisor defaults to gpt-4o-mini. Secret name reads the correct
      OpenAI key secret.</criterion>
    <criterion id="5">Infrastructure monitor deployed and 0-diff confirmed. EC2 supervisor updated
      via safe-ec2-deploy.sh.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Dependency: OPENAI_USAGE log lines (from OpalETL task order ADHC_GPTCST.001) must
      be deployed before the token-accurate path in requirement 2 will produce data. The naming
      fixes in requirement 1 and SmartX fixes in requirement 4 are unblocked.</constraint>
    <constraint>Do not change the morning report format outside the new OPENAI COST section.</constraint>
    <constraint>SmartX supervisor changes go through safe-ec2-deploy.sh. Do not edit directly on EC2.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.5.0_AE_OpalETL"
                task="ADHC_GPTCST.001.openai-caller-optimization"
                status="pending"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">infrastructure_monitor Lambda updated and deployed.</deliverable>
    <deliverable type="commit">SmartX EC2 supervisor updated and deployed via safe-ec2-deploy.sh.</deliverable>
    <deliverable type="document">Session log with verification showing OPENAI COST section
      in a sample morning report output.</deliverable>
  </deliverables>

  <references>
    <ref type="thread">org/threads/ADHC_GPTCST-001-openai-cost-audit-caller-inventory/</ref>
    <ref type="receipt">org/tier2_senior/0.7.0_AE_CloudOps/threads/ADHC_GPTCST-001-openai-cost-audit-caller-inventory_0.5.0_AE_OpalETL.md</ref>
  </references>
</task_order>
