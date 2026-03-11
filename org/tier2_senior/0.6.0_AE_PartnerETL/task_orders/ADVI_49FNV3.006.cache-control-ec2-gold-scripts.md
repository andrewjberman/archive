<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-006</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
  </metadata>

  <objective>
    Add Cache-Control metadata to all S3 put_object calls in the two active EC2 gold
    scripts (09 and 10). These scripts write portal-consumed JSON files directly to
    opal-data-bd/gold/ but set no CacheControl header, producing the same browser
    heuristic caching problem that ADVI_49FNV3.005 fixed in the publisher Lambdas.

    Script 09 writes 3 files (header_metrics_{quarterly,monthly,annual}.json) that
    populate the PartnerAnalytics AUA panel. Script 10 writes advisor_rolling_flows.json
    (111MB) consumed by the LeaderboardTab rolling flows chart. Both are served through
    the same CloudFront CachingOptimized behavior and have no Cache-Control today.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/09_generate_partner_analytics.py</file>
      <file action="modify">data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">In script 09, modify the write_s3 function (line 1616) to add
      CacheControl='public, max-age=300, s-maxage=3600' to the s3.put_object call.
      This covers all 3 granularity files (quarterly, monthly, annual).</requirement>
    <requirement id="2">In script 10, modify the s3.put_object call (line 911) to add
      the same CacheControl='public, max-age=300, s-maxage=3600'.</requirement>
    <requirement id="3">Deploy both scripts through the EC2 S3 artifact path:
      modify locally -> upload to S3 -> EC2 pulls on next gold run. Follow
      EC2_CODE_DEPLOYMENT_STANDARD.md (repo -> S3 -> EC2 pulls -> executes).</requirement>
    <requirement id="4">After the next gold pipeline run, verify with:
      aws s3api head-object --bucket opal-data-bd --key gold/partner_analytics/header_metrics_quarterly.json
      aws s3api head-object --bucket opal-data-bd --key gold/advisor_rolling_flows.json
      Both must return CacheControl: 'public, max-age=300, s-maxage=3600'.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">aws s3api head-object on all 4 files (3 from script 09, 1 from
      script 10) shows CacheControl: 'public, max-age=300, s-maxage=3600' after the
      next gold pipeline run.</criterion>
    <criterion id="2">No other changes to scripts 09 or 10 beyond the CacheControl
      parameter addition.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>EC2 deploy path -- not Lambda. Follow safe-ec2-deploy.sh / S3 artifact
      model. Do not modify the Lambdas (those were fixed in ADVI_49FNV3.005).</constraint>
    <constraint>Use the same Cache-Control value as the publisher Lambdas for
      consistency: 'public, max-age=300, s-maxage=3600'.</constraint>
    <constraint>Do not touch archive/ scripts -- only the two active scripts.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL"
                task="ADVI_49FNV3.005.cache-control-s3-metadata"
                status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Modified put_object calls in scripts 09 and 10 with CacheControl parameter.</deliverable>
    <deliverable type="commit">Scripts uploaded to S3 artifact path and deployed to EC2.</deliverable>
  </deliverables>

  <references>
    <ref type="source">data/black_diamond/scripts/gold/09_generate_partner_analytics.py (line 1616, write_s3)</ref>
    <ref type="source">data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py (line 911, put_object)</ref>
    <ref type="protocol">docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md</ref>
    <ref type="task_order">org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADVI_49FNV3.005.cache-control-s3-metadata.md</ref>
  </references>
</task_order>
