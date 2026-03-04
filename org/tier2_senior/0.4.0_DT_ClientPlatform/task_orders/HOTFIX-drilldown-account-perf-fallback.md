# Hotfix Task Order: Snapshot Drilldown Broken — account_performance Fallback Deploy

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-04-hotfix-drilldown-acct-perf-fallback</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-04</date>
    <status>URGENT — production drilldown broken</status>
  </metadata>

  <root_cause>
    Snapshot mode geo and adv drilldowns are broken (cities/clients all empty).

    Failure chain:
      1. Incremental gold runs (daily) advance client_performance.parquet to today (March 4).
      2. account_performance.parquet stays at ~March 1 — 05b runs full mode only (monthly).
      3. Script 09 on EC2 (S3 code at deployed_commit dab7c6fc) has NO date fallback logic.
         It looks for today's date in account_performance → not found → ap_day is empty.
      4. Empty ap_day → acct_geo empty → _build_cities() returns [] for every state segment.
         Same for _build_clients() → [] for every architect segment.
      5. partner_analytics/header_metrics.json written with cities:[] and clients:[] for ALL segments.
      6. Frontend snapshot drilldown reads segment.cities / segment.clients → empty → no drill.

    Fix committed at: f97addf8 (fix(bd-gold-09): account_performance date fallback for incremental runs)
    Fix is in CLOUD workspace but NOT deployed to S3. EC2_MANIFEST still shows deployed_commit: dab7c6fc.
    The fix adds _acct_date_fallback: for each target date missing from account_performance, use
    the closest prior date that IS available (e.g., March 4 falls back to March 1 or Feb 28).
  </root_cause>

  <requirements>

    <requirement id="H1">
      Deploy current CLOUD scripts to S3 via safe-ec2-deploy.sh. This pushes f97addf8
      (and all subsequent commits including bd-v2.16.0 run_gold_layer.sh changes) to
      s3://opal-data-bd/code/gold/.

        export PATH="/c/Users/AndrewBerman/Desktop/ajb_workspace/.tools:$PATH"
        export AWS_EC2_METADATA_DISABLED=true
        export MSYS_NO_PATHCONV=1
        export AGENT_NAME="0.4.0_DT_ClientPlatform"

        bash infra/aws/ec2/safe-ec2-deploy.sh bd-gold-layer-runner \
            infra/aws/ec2/bd-gold-layer-runner/deploy-to-ec2.sh

      Verify manifest updated: EC2_MANIFEST.json deployed_commit should advance past dab7c6fc.
    </requirement>

    <requirement id="H2">
      Commit the manifest update (safe-ec2-deploy.sh auto-commits EC2_MANIFEST.json).
      Verify: git log --oneline -2 shows the auto-generated manifest commit.
    </requirement>

    <requirement id="H3">
      Start the EC2 for a fresh incremental run:

        export AWS_EC2_METADATA_DISABLED=true
        aws ec2 start-instances --instance-ids i-01003b035d2988dfb --region us-east-1

      The instance boots, pulls the updated scripts from S3 (including the f97addf8 fix),
      runs incremental mode (02 -> 05 -> 07 -> 08 -> 09 -> 10), shuts down.

      Script 09 will now:
        - Detect that account_performance.parquet doesn't have today's date
        - Fall back to the closest prior date (e.g., March 1)
        - Use March 1 account data for today's cities/distributions
        - Write cities[] and clients[] populated for all segments
    </requirement>

    <requirement id="H4">
      Monitor run completion:

        aws s3 ls s3://opal-data-bd/logs/gold-layer/ --recursive | sort | tail -5

      Wait for a log file dated today. Then verify cities are populated:

        aws s3 cp s3://opal-data-bd/gold/summary/partner_analytics/header_metrics.json - \
          | python3 -c "
        import json, sys
        d = json.load(sys.stdin)
        geo = d['views']['geo']['current']['donut']['segments']
        print('Segments:', len(geo))
        for s in geo[:3]:
            print(f\"  {s['key']}: cities={len(s.get('cities', []))}\")"

      Expected: at least 2-3 cities per top segment. Empty [] = fix did not take effect.
      Also check adv:

        aws s3 cp s3://opal-data-bd/gold/summary/partner_analytics/header_metrics.json - \
          | python3 -c "
        import json, sys
        d = json.load(sys.stdin)
        adv = d['views']['adv']['current']['donut']['segments']
        print('Adv segments:', len(adv))
        for s in adv[:3]:
            print(f\"  {s['key']}: clients={len(s.get('clients', []))}\")"
    </requirement>

    <requirement id="H5">
      After confirming cities/clients populated:
        git tag -a bd-v2.16.1 -m "hotfix(bd-gold-09): account_performance date fallback deployed (CLOUD-drilldown-fix)"
        git push --follow-tags

      Update deployment_map.xml with the new deployed commit.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">safe-ec2-deploy.sh runs clean. EC2_MANIFEST deployed_commit advances past dab7c6fc.</criterion>
    <criterion id="2">Incremental gold run completes. Log shows COMPLETE -- INCREMENTAL.</criterion>
    <criterion id="3">partner_analytics/header_metrics.json has cities.length >= 2 for top geo segments.</criterion>
    <criterion id="4">partner_analytics/header_metrics.json has clients.length >= 1 for top adv segments.</criterion>
    <criterion id="5">Portal snapshot drilldown functional (geo cities drill, adv client drill).</criterion>
    <criterion id="6">bd-v2.16.1 tag pushed.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT run in full mode — incremental is sufficient and much faster. Full mode takes ~30 min and rebuilds all parquets.</constraint>
    <constraint>Do NOT run 05b manually — the fallback logic in the updated script 09 handles the date gap correctly.</constraint>
    <constraint>CloudFront invalidation is automatic (run_gold_layer.sh handles it). Do not invalidate manually.</constraint>
    <constraint>Do NOT use emojis in any log output.</constraint>
    <constraint>export AWS_EC2_METADATA_DISABLED=true before all AWS CLI commands.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <why_not_script_09_on_runner>
    The deployed run_gold_layer.sh (on S3 at dab7c6fc) downloads script 09 from S3 each run.
    It was downloading the OLD script 09 (without the fallback). After H1 (safe-ec2-deploy.sh),
    the new script 09 (with f97addf8 fallback) will be on S3. The next EC2 boot downloads it
    and the fallback logic runs. No manual script editing on the instance needed.
  </why_not_script_09_on_runner>

</task_order>
```
