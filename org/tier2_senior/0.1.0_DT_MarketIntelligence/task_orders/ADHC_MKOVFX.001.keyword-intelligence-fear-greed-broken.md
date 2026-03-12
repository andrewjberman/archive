<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-12-adhc-mkovfx-001</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DT_MarketIntelligence</issued_to>
    <date>2026-03-12</date>
    <status>pending</status>
    <project>ADHC_MKOVFX</project>
  </metadata>

  <objective>
    URGENT: Two market overview features are broken in the portal. Keyword Intelligence
    is showing no data, and Fear &amp; Greed index is broken. Diagnose root cause for
    both and fix immediately.
  </objective>

  <scope>
    <files>
      <!-- Fear & Greed -->
      <file action="investigate">infra/aws/lambda/v2_portal/01_market_overview/lambdas/fear-greed-fetcher/lambda_function.py</file>
      <!-- Keyword Intelligence (news pipeline source) -->
      <file action="investigate">infra/aws/lambda/keyword_intelligence_generator/lambda_function.py</file>
      <file action="investigate">infra/aws/lambda/keyword_drilldown_generator/lambda_function.py</file>
      <!-- Portal data proxy (routes keyword intelligence requests) -->
      <file action="investigate">infra/aws/lambda/portal_data_proxy/lambda_function.py</file>
      <!-- Terraform -->
      <file action="investigate">infra/aws/terraform/market-overview/eventbridge.tf</file>
      <file action="investigate">infra/aws/terraform/market-overview/lambdas.tf</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      FEAR &amp; GREED — Diagnose and fix.

      Investigation checklist:
        1. Check CloudWatch logs for opal-portal-fear-greed-fetcher:
           - Is the Lambda running? When was the last successful invocation?
           - Any errors or exceptions in recent runs?
        2. Check EventBridge schedule: fear-greed-daily-update fires at
           cron(30 14,21 * * ? *) — 9:30 AM + 4:30 PM ET. Is the rule ENABLED?
           Is the target wired correctly?
        3. Check S3 output: s3://opal-data-portal-v2/json/sentiment/fear-greed-index.json
           - Does the file exist? When was it last modified?
           - Is the content valid JSON with recent data?
        4. Check the data source: the fetcher likely pulls from CNN Fear &amp; Greed API
           or similar. Has the upstream API changed, moved, or started returning errors?

      Fix: whatever is breaking the pipeline — deploy fix if code change needed,
      or re-run the Lambda manually if it's a transient issue.
    </requirement>

    <requirement id="2">
      KEYWORD INTELLIGENCE — Diagnose and fix.

      This feature spans two pipelines:
        - news-pipeline: keyword-intelligence-generator and opal-keyword-drilldown-generator
          produce the keyword data
        - market-overview: opal-portal-data-proxy routes POST /v1/sentiment/keyword-intelligence
          requests from the portal to the generator

      Investigation checklist:
        1. Check S3: is keyword intelligence data being written? Look for the output
           files the generators produce.
        2. Check CloudWatch logs for keyword-intelligence-generator:
           - Recent invocations? Errors?
        3. Check CloudWatch logs for opal-portal-data-proxy:
           - Is the proxy receiving requests? Returning errors?
           - Is it routing to the correct generator function?
        4. Check CloudWatch logs for the news trending pipeline (Layer 3 curation
           chain-invokes the publisher). Has the chain broken?
        5. Check if this is related to any recent deployments:
           - news-v2.7.0 (news publisher target_date parameterization)
           - market-overview-v1.6.0 (keyword cache fix from ADHC_GPTCST)
           Were there any regressions from those deploys?

      Fix: restore keyword intelligence data flow. Deploy fix if needed.
    </requirement>

    <requirement id="3">
      After fixing both issues, verify end-to-end:
        - Fear &amp; Greed: portal shows current index value and historical chart
        - Keyword Intelligence: clicking a topic in the TopicCloud opens the
          keyword intelligence modal with populated data
        - Confirm both are running on their scheduled cadences going forward
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Fear &amp; Greed shows current data in the portal. S3 file has a recent
      timestamp. Lambda is executing successfully on schedule.
    </criterion>
    <criterion id="2">
      Keyword Intelligence returns populated data when a topic is clicked.
      No empty responses. Generator Lambda producing output.
    </criterion>
    <criterion id="3">
      Root cause documented in session log for both issues.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Standard deployment protocol if code changes needed: terraform apply only,
    tag after 0-diff, push with --follow-tags.</constraint>
    <constraint>If the fix requires news-pipeline changes, coordinate with 0.5.0_AE_OpalETL
    or handle directly if it's a market-overview-only fix.</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13).</constraint>
  </constraints>

  <context>
    Key Lambdas:
      opal-portal-fear-greed-fetcher — market-overview, EventBridge cron(30 14,21 * * ? *)
        Output: s3://opal-data-portal-v2/json/sentiment/fear-greed-index.json
        Source: infra/aws/lambda/v2_portal/01_market_overview/lambdas/fear-greed-fetcher/

      keyword-intelligence-generator — news-pipeline
        Source: infra/aws/lambda/keyword_intelligence_generator/

      opal-keyword-drilldown-generator — news-pipeline
        Source: infra/aws/lambda/keyword_drilldown_generator/

      opal-portal-data-proxy — market-overview, routes POST /v1/sentiment/keyword-intelligence
        Source: infra/aws/lambda/portal_data_proxy/lambda_function.py
        Note: deployed with bundled openai + Linux pydantic_core wheels — do NOT rebuild
        with local pip. Extract existing zip, swap lambda_function.py, rezip.

    Recent deployments that may be relevant:
      news-v2.7.0 — news publisher target_date parameterization (2026-03-11)
      market-overview-v1.6.0 — keyword cache fix from ADHC_GPTCST (2026-03-10)

    Current pipeline tags:
      market-overview: market-overview-v1.6.0
      news: news-v2.7.0
  </context>

  <deliverables>
    <deliverable type="document">Session log with root cause for both issues and fix applied</deliverable>
    <deliverable type="deploy">Fix deployed if code change needed (tag + push)</deliverable>
  </deliverables>
</task_order>
