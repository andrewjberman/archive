<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-ADHC001-ae-opal</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <thread_serial>ADHC_GPTCST-001</thread_serial>
    <thread_ref>org/threads/ADHC_GPTCST-001-openai-cost-audit-caller-inventory/</thread_ref>
  </metadata>

  <objective>
    Implement Phase 2 optimization changes for OpalETL-owned OpenAI callers identified in thread
    ADHC_GPTCST-001. Four targets ranked by cost impact. Also add the standardized OPENAI_USAGE
    log line to each caller to enable Phase 3 token-accurate cost tracking by CloudOps.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/news_trending_analysis/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/news_layer3_curation/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/semantic-news-layer3-curation/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/keyword_intelligence_generator/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/market_update_generator/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/trending_image_selector/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">OPENAI_USAGE log line: Add the following standardized log line immediately
      after every OpenAI API call in all six files above:
        print(f"OPENAI_USAGE function=LAMBDA_NAME model={model} prompt={usage.prompt_tokens} completion={usage.completion_tokens} total={usage.total_tokens}")
      Use the canonical Lambda name from lambda-source-map.json (not the Python module name).
      Canonical names: news-trending-analysis, opal-news-layer3-curation,
      semantic-news-layer3-curation, keyword-intelligence-generator,
      market-update-generator (confirm in TF), opal-trending-image-generator.
      This log line is REQUIRED for Phase 3 cost tracking to function.</requirement>

    <requirement id="2">Fix keyword-intelligence-generator double-trigger: It is both scheduled on
      EventBridge AND invoked async by news-trending-analysis. Disable the standalone EventBridge
      schedule in Terraform (infra/aws/terraform/news-pipeline/ or other/) so it only runs via
      chained invoke. This eliminates the most likely "2x cost for same work" pattern.</requirement>

    <requirement id="3">news-trending-analysis: Downgrade keyword validation calls from gpt-4o
      to gpt-4o-mini. Keyword validation does not require frontier-model reasoning.</requirement>

    <requirement id="4">market-update-generator: Migrate off gpt-4-turbo-preview to gpt-4o-mini.
      This is a deprecated/expensive model. Add a payload-hash cache key so repeat regeneration
      requests with identical inputs return a cached result rather than calling OpenAI again.</requirement>

    <requirement id="5">semantic-news-layer3-curation: Add an idempotency guard — if it has
      already processed today's data (check a DynamoDB entry or S3 marker), skip the OpenAI call
      and return early. This prevents re-runs from double-billing.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All six Lambda files emit OPENAI_USAGE log lines after every API call.</criterion>
    <criterion id="2">keyword-intelligence-generator EventBridge schedule disabled in Terraform.
      0-diff plan confirmed after apply.</criterion>
    <criterion id="3">news-trending-analysis uses gpt-4o-mini for keyword validation.</criterion>
    <criterion id="4">market-update-generator uses gpt-4o-mini (not gpt-4-turbo-preview) and
      has payload-hash caching.</criterion>
    <criterion id="5">semantic-news-layer3-curation skips processing if today's run already
      completed.</criterion>
    <criterion id="6">All Lambda changes deployed via Terraform. 0-diff plans confirmed. Tags
      updated.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not change the news pipeline architecture or trigger topology beyond disabling
      the redundant keyword-intelligence-generator schedule.</constraint>
    <constraint>OPENAI_USAGE log format must be exact — CloudOps will parse it with a fixed
      regex in openai_cost_tracker.py.</constraint>
    <constraint>Confirm the exact deployed Lambda function name for market-update-generator in
      lambda-source-map.json before adding the OPENAI_USAGE line.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="commit">Lambda source changes + Terraform EventBridge disable committed
      and deployed.</deliverable>
    <deliverable type="document">Session log with deployment sequence, tags, and verification
      that OPENAI_USAGE lines appear in CloudWatch after a test invocation.</deliverable>
  </deliverables>

  <references>
    <ref type="thread">org/threads/ADHC_GPTCST-001-openai-cost-audit-caller-inventory/</ref>
    <ref type="receipt">org/tier2_senior/0.5.0_AE_OpalETL/threads/ADHC_GPTCST-001-openai-cost-audit-caller-inventory_0.7.0_AE_CloudOps.md</ref>
  </references>
</task_order>
