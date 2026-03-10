<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-ADHC002</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
  </metadata>

  <objective>
    Fix the keyword intelligence system so the pre-computed cache is actually used.
    Three targeted changes: (1) add DynamoDB write-back on cache miss in portal_data_proxy
    so the first click per keyword per day populates the cache for all subsequent users,
    (2) shift pre-computation to run earlier so morning users hit the cache instead of
    falling through to live compute, (3) reduce pre-computation from top 20 to top 10
    keywords to halve web search cost while keeping the pre-computed dataset for
    potential downstream use.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/portal_data_proxy/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/keyword_intelligence_generator/lambda_function.py</file>
      <file action="modify">infra/aws/terraform/news-pipeline/eventbridge.tf</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">portal_data_proxy: Add DynamoDB write-back after live computation.
      When get_keyword_intelligence() computes a result via the live path (cache MISS),
      write the result to intelligence_table (opal-keyword-intelligence) using the same
      schema as keyword-intelligence-generator:
        PK = keyword (lowercase)
        SK = today's date (YYYY-MM-DD, UTC)
        all response fields as attributes
      Write must be fire-and-forget with graceful failure (log WARN on exception, never
      let a write failure block the response). After this change, the first click on any
      keyword each day is slow (live compute), every subsequent click that day is instant
      (cache hit).</requirement>

    <requirement id="2">keyword-intelligence-generator: Reduce MAX_KEYWORDS from 20 to 10.
      Change the environment variable default from '20' to '10'. This cuts web search
      queries from 40/run to 20/run (80/day to 40/day), halving pre-computation cost.
      The pre-computed dataset is kept for potential downstream use.</requirement>

    <requirement id="3">eventbridge.tf: Shift keyword-intelligence-generator schedule from
      cron(50 14,21 * * ? *) (9:50 AM / 4:50 PM ET) to cron(0 8,20 * * ? *)
      (3:00 AM / 3:00 PM ET / 8 AM and 8 PM UTC). This ensures the pre-computed cache
      has today's date as SK before US markets open, so the first user of the day hits
      a cache hit rather than a 15-second live compute. The rule remains DISABLED in
      Terraform state (it is invoked via chained async call from news-trending-analysis,
      not directly by EventBridge) — only update the schedule_expression comment so it
      reflects the intended timing if the fallback rule is ever re-enabled.
      NOTE: The actual timing change that matters is in news-trending-analysis — it
      invokes keyword-intelligence-generator asynchronously after writing
      keyword-sentiments.json. The news-trending-analysis EventBridge rule fires at
      cron(30 14,21 * * ? *) per eventbridge.tf. That means pre-computation runs at
      ~2:50 PM and ~9:50 PM ET = ~6:50 PM and ~1:50 AM UTC. Read eventbridge.tf to
      confirm the actual news-trending-analysis schedule before deciding if a timing
      change is needed. If news-trending-analysis already runs early enough that the
      pre-computed entries have today's date when US markets open (9:30 AM ET = 1:30 PM
      UTC), no schedule change is needed — document the finding in the session log and
      skip this change.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">After portal_data_proxy is deployed: CloudWatch logs show
      "[keyword_intelligence] Cache HIT" on the second request for any keyword within
      the same UTC day (verifiable via test invocation or CloudWatch log tail).</criterion>
    <criterion id="2">keyword-intelligence-generator MAX_KEYWORDS defaults to 10.
      Deployed and 0-diff confirmed.</criterion>
    <criterion id="3">eventbridge.tf schedule_expression updated (or documented as
      acceptable with rationale in session log).</criterion>
    <criterion id="4">All changes deployed via Terraform. 0-diff plans confirmed.
      Tags updated.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>The write-back in portal_data_proxy must NEVER block or throw — wrap
      in try/except, log on failure, always return the computed response.</constraint>
    <constraint>Do not change the DynamoDB schema — use exact same PK/SK/attribute
      structure as keyword-intelligence-generator writes.</constraint>
    <constraint>Do not change the live computation logic in portal_data_proxy — only
      add the write-back after the existing cors_response is built.</constraint>
    <constraint>Read eventbridge.tf before touching the schedule — confirm actual
      news-trending-analysis trigger time before deciding if timing change is needed.
      Do not change schedules without understanding the full chain.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="commit">portal_data_proxy + keyword-intelligence-generator
      source changes committed and deployed.</deliverable>
    <deliverable type="commit">eventbridge.tf updated (or documented as no-change
      with rationale).</deliverable>
    <deliverable type="document">Session log with deployment sequence, 0-diff
      confirmation, and cache hit verification.</deliverable>
  </deliverables>
</task_order>
