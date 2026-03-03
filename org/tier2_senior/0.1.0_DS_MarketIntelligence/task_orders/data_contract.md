# Task Order — Data Contract: MarketIntelligence

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-data-contract-market-intelligence</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-03-02</date>
    <status>complete</status>
  </metadata>

  <objective>
    Produce a data_contract.xml that maps exactly what data each MarketIntelligence
    portal page consumes, which Lambda functions produce it, where it is stored,
    and what shape it has. This is your permanent activation document — the DS
    equivalent of the RD page_inventory and DE pod_inventory. It answers: "For
    every page in my pod, where does the data come from and what does it look like?"
  </objective>

  <scope>
    <files>
      <!-- Primary inputs — read these first -->
      <file action="read">org/tier2_senior/0.1.0_DE_MarketIntelligence/deliverables/pod_inventory.xml</file>

      <!-- Lambda source code — your primary investigation targets -->
      <file action="read">infra/aws/lambda/opal_market_overview_tiered_generator/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_market_regime_classifier/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_market_rsi_tiered_generator/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_precompute_market_metrics/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_portal_fear_greed_fetcher/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_portal_volatility_fetcher/lambda_function.py</file>
      <file action="read">infra/aws/lambda/causality_themes_fetcher/lambda_function.py</file>
      <file action="read">infra/aws/lambda/causality_analysis_generator/lambda_function.py</file>
      <file action="read">infra/aws/lambda/causality_ai_query_handler/lambda_function.py</file>
      <file action="read">infra/aws/lambda/causality_market_update_generator/lambda_function.py</file>
      <file action="read">infra/aws/lambda/keyword_intelligence_generator/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_trending_topics_portal_publisher/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_news_ai_sentiment/lambda_function.py</file>

      <!-- Portal endpoint files — what shape the portal expects -->
      <file action="read">portal/src/api/endpoints/market.ts</file>
      <file action="read">portal/src/api/endpoints/market-precomputed.ts</file>
      <file action="read">portal/src/api/endpoints/causality-endpoints.ts</file>
      <file action="read">portal/src/api/endpoints/sentiment.ts</file>
      <file action="read">portal/src/api/endpoints/trending.ts</file>

      <!-- Lambda source map for S3 paths and metadata -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>

      <!-- Output -->
      <file action="create">org/tier2_senior/0.1.0_DS_MarketIntelligence/deliverables/data_contract.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read pod_inventory.xml first. Use the api_calls and api_endpoints sections
      to identify every endpoint the pod's pages hit. These are the entry points
      you trace backward into Lambda code.
    </requirement>
    <requirement id="2">
      For each Lambda function listed, read the source code and extract:
      (a) what S3 keys or DynamoDB tables it reads from as input,
      (b) what S3 keys or DynamoDB tables it writes to as output,
      (c) the top-level shape of the JSON it produces (key names and types),
      (d) what triggers it (EventBridge schedule, S3 event, API Gateway, manual).
    </requirement>
    <requirement id="3">
      If a Lambda source file is not found at the path listed, search for it
      using Glob with the function name. Lambda source directories may use
      underscores vs hyphens differently. Document the actual path found.
    </requirement>
    <requirement id="4">
      For the MarketPerformance page specifically: trace the full data flow from
      the tiered CloudFront endpoint system through to the market overview generator
      Lambda. Document where the tiered data is stored in S3 and what keys are used.
    </requirement>
    <requirement id="5">
      For the CausalityEngine page: trace the causality themes, analysis, and
      AI query handler Lambdas. Document the DynamoDB tables or S3 paths they
      read/write and the shape of the causality data structures.
    </requirement>
    <requirement id="6">
      Produce data_contract.xml following the schema in acceptance criteria.
      All data shapes must come from reading actual Lambda code or portal endpoint
      TypeScript types — no inference or fabrication.
    </requirement>
    <requirement id="7">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      data_contract.xml exists at org/tier2_senior/0.1.0_DS_MarketIntelligence/deliverables/data_contract.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;data_contract&gt;
        &lt;metadata&gt; agent, pod, date &lt;/metadata&gt;

        &lt;page_contracts&gt;
          One &lt;page&gt; per pod page:
            name,
            &lt;data_sources&gt;
              One &lt;source&gt; per distinct data feed:
                lambda_function, trigger, s3_output_key_pattern (or dynamodb_table),
                &lt;response_shape&gt; top-level keys and value types &lt;/response_shape&gt;,
                &lt;portal_endpoint&gt; which endpoint.ts function fetches this &lt;/portal_endpoint&gt;
            &lt;/data_sources&gt;
            &lt;data_freshness&gt; how often data is updated (EventBridge schedule or on-demand) &lt;/data_freshness&gt;
        &lt;/page_contracts&gt;

        &lt;shared_data_sources&gt;
          Data sources consumed by more than one page in this pod
        &lt;/shared_data_sources&gt;

        &lt;upstream_dependencies&gt;
          External data feeds this pod's Lambdas pull from:
          e.g., Yahoo Finance, FRED, Fear & Greed API, news sources
        &lt;/upstream_dependencies&gt;

        &lt;data_quality_notes&gt;
          Known data issues, fallback behaviors, stale-data handling
        &lt;/data_quality_notes&gt;

        &lt;gaps&gt;
          Pages or data sources where the contract is incomplete or unknown
        &lt;/gaps&gt;
      &lt;/data_contract&gt;
    </criterion>
    <criterion id="3">
      response_shape entries must reflect actual Lambda output structure,
      not assumed structure. If the shape cannot be determined from code, mark
      it as unknown and explain what was looked at.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any Lambda source files or portal files.</constraint>
    <constraint>Do not run any Lambda functions or AWS CLI commands.</constraint>
    <constraint>
      If a Lambda file path is not found, use Glob to search:
      infra/aws/lambda/**/{function_name_variant}/lambda_function.py
      Document the actual path found rather than assuming.
    </constraint>
    <constraint>
      The news and sentiment pipeline (finbert, news-ingestion, news-semantic-clustering,
      opal-news-ai-sentiment) feeds the SentimentPanel on MarketPerformance.
      Trace it even though it is a multi-stage pipeline — document each stage's
      output as a separate source.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.1.0_DE_MarketIntelligence" task="pod_inventory" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.1.0_DS_MarketIntelligence/deliverables/data_contract.xml
    </deliverable>
  </deliverables>
</task_order>
```
