<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-005</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
  </metadata>

  <objective>
    Add Cache-Control metadata to all S3 put_object calls in both BD portal publisher
    Lambdas (bd-portal-publisher and bd-portal-advisor-publisher). Without this header,
    S3 returns no Cache-Control directive, CloudFront's CachingOptimized policy applies
    a 24-hour default TTL, and browsers apply heuristic caching based on Last-Modified
    age. This caused the portal to display stale data ($1.55B / 2026-03-02) even after
    CloudFront invalidation because browser-side heuristic cache was never busted.
    InPrivate/incognito windows worked immediately (empty cache), confirming the browser
    cache as the root cause.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">In both Lambdas, modify the _save_json function's s3.put_object
      call to include CacheControl='public, max-age=300, s-maxage=3600' alongside the
      existing ContentType parameter.
      - max-age=300: browser caches for 5 minutes max (eliminates heuristic caching)
      - s-maxage=3600: CloudFront edge caches for 1 hour (overrides CachingOptimized 24h default)
    </requirement>
    <requirement id="2">The change is identical in both files. The _save_json function
      in bd-portal-publisher is at line 163; in bd-portal-advisor-publisher at line 58.
      Both currently pass only Bucket, Key, Body, and ContentType.</requirement>
    <requirement id="3">Deploy both Lambdas through the standard Terraform cycle:
      code change -> build-and-upload.sh -> update source map -> commit -> terraform plan
      -> terraform apply -> 0-diff -> tag -> push.</requirement>
    <requirement id="4">After deploy, trigger a re-run of the gold pipeline (or wait for
      the nightly run) so the S3 objects are rewritten with the new Cache-Control metadata.
      Verify with: aws s3api head-object --bucket opal-data-bd --key gold/timeseries_chart.json
      -- the CacheControl field must show 'public, max-age=300, s-maxage=3600' (currently null).</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">aws s3api head-object on gold/timeseries_chart.json returns
      CacheControl: 'public, max-age=300, s-maxage=3600' after the next publisher run.</criterion>
    <criterion id="2">Browser response headers for /api/scoped/advisor-intelligence/timeseries_chart.json
      include Cache-Control: public, max-age=300, s-maxage=3600 (visible in DevTools Network tab).</criterion>
    <criterion id="3">Both Lambdas deployed at 0-diff. bd-pipeline tag incremented.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not change the CloudFront cache policy or behavior configuration.
      The CachingOptimized policy (658327ea-f89d-4fab-a63d-7e88639e58f6) honors
      s-maxage from origin responses, so the S3 metadata fix is sufficient.</constraint>
    <constraint>Do not change cache-control-injector Lambda@Edge -- it is not attached
      to the advisor-intelligence behavior and should stay that way. The fix belongs
      at the origin (S3 metadata), not at the edge.</constraint>
    <constraint>Both Lambdas must get the same change. Do not fix one and forget the other.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL"
                task="ADVI_49FNV3.004.gold-pipeline-staleness-investigation"
                status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Modified _save_json in both publisher Lambdas with CacheControl parameter.</deliverable>
    <deliverable type="commit">Terraform deploy of bd-pipeline with updated Lambda artifacts.</deliverable>
  </deliverables>

  <references>
    <ref type="source">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py (line 163-172, _save_json)</ref>
    <ref type="source">infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py (line 58-66, _save_json)</ref>
    <ref type="source">infra/aws/scripts/build-cf-behaviors.sh (line 78-100, advisor-intelligence behavior)</ref>
    <ref type="evidence">aws s3api head-object confirms CacheControl: null on gold/timeseries_chart.json as of 2026-03-10</ref>
    <ref type="task_order">org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADVI_49FNV3.004.gold-pipeline-staleness-investigation.md</ref>
  </references>
</task_order>
