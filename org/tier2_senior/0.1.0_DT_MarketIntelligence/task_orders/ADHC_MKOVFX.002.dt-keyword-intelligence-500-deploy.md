<task_order>
  <metadata>
    <id>0.1.0_DS-2026-03-25-adhc-mkovfx-002</id>
    <issued_by>0.1.0_DS_MarketIntelligence</issued_by>
    <issued_to>0.1.0_DT_MarketIntelligence</issued_to>
    <date>2026-03-25</date>
    <status>complete</status>
    <project>ADHC_MKOVFX</project>
  </metadata>

  <objective>
    Deploy two fixes for the TopicCloud keyword intelligence 500 error. DS has already
    made the code changes — DT needs to build artifacts, update Terraform, and deploy.
  </objective>

  <scope>
    <files>
      <file action="build-and-deploy">infra/aws/lambda/portal_data_proxy/lambda_function.py</file>
      <file action="build-and-deploy">infra/aws/lambda/keyword_intelligence_generator/lambda_function.py</file>
      <file action="update">infra/aws/terraform/news-pipeline/lambdas.tf</file>
      <file action="apply">infra/aws/terraform/news-pipeline/</file>
      <file action="apply">infra/aws/terraform/market-overview/</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      FIX 1 — portal_data_proxy: try/except for keyword-intelligence route.

      DS added a try/except wrapper around the `get_keyword_intelligence(keyword)` call
      in `lambda_handler` (around line 2406). This matches every other route handler in
      the file. Without it, any unhandled exception in the function body crashes the
      Lambda and API Gateway returns its default `{"message":"Internal Server Error"}`.

      Deploy steps:
        1. Extract the existing production zip from S3:
           `s3://opal-313476888478-lambda-artifacts/market-overview/opal-portal-data-proxy.zip`
        2. Swap in the updated `lambda_function.py` (preserve all vendored deps — openai,
           pydantic_core wheels are pre-built Linux-compatible, do NOT rebuild)
        3. Re-zip with PowerShell, upload to S3
        4. `terraform plan` + `terraform apply` in `infra/aws/terraform/market-overview/`
        5. Verify 0-diff plan
    </requirement>

    <requirement id="2">
      FIX 2 — keyword-intelligence-generator: MAX_KEYWORDS 10 -> 20.

      The TopicCloud shows 20 keywords but the generator only pre-computes intelligence
      for the top 10. Clicking keywords 11-20 forces live computation through the
      portal_data_proxy, which is the path that was crashing.

      Two changes needed:
        a. Code default already changed by DS: line 49 of
           `infra/aws/lambda/keyword_intelligence_generator/lambda_function.py`
           (`'10'` -> `'20'`)
        b. Terraform env var override (THIS IS THE CRITICAL ONE — it overrides the code):
           `infra/aws/terraform/news-pipeline/lambdas.tf` line 332:
           Change `MAX_KEYWORDS = "10"` to `MAX_KEYWORDS = "20"`

      Deploy steps:
        1. Edit lambdas.tf line 332: `"10"` -> `"20"`
        2. Build updated keyword-intelligence-generator.zip (vendored deps in _build_tmp)
        3. Upload to `s3://opal-313476888478-lambda-artifacts/news-pipeline/keyword-intelligence-generator.zip`
        4. `terraform plan` + `terraform apply` in `infra/aws/terraform/news-pipeline/`
        5. Verify 0-diff plan
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">portal_data_proxy returns `cors_response(500, ...)` on unhandled errors instead of crashing the Lambda process</criterion>
    <criterion id="2">keyword-intelligence-generator pre-computes for 20 keywords (matching TopicCloud count)</criterion>
    <criterion id="3">Terraform 0-diff plan for both news-pipeline and market-overview after apply</criterion>
    <criterion id="4">Click any keyword in the TopicCloud — modal loads without 500 error</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Follow LAMBDA_DEPLOYMENT_PROTOCOL.md — commit before apply, tag after deploy</constraint>
    <constraint>Do NOT rebuild openai/pydantic_core wheels in portal_data_proxy zip — swap lambda_function.py only</constraint>
    <constraint>No emojis in code or logs (CLAUDE.md rule 13)</constraint>
  </constraints>

  <context>
    Root cause analysis (by 0.1.0_DS, 2026-03-25):
    - User-facing error: "API request failed: 500 Internal Server Error - {"message":"Internal Server Error"}"
    - The `{"message":"Internal Server Error"}` body is API Gateway's default — NOT the Lambda's error format
    - This means the Lambda was crashing with an unhandled exception
    - The `get_keyword_intelligence()` function had internal try/excepts for cache, S3, DynamoDB, and GPT
      but NO top-level try/except — and lambda_handler had no global catch-all
    - The crash was most likely triggered on cache-miss keywords (11-20) entering the live computation path
    - CloudWatch logs would confirm the specific exception type
  </context>
</task_order>
