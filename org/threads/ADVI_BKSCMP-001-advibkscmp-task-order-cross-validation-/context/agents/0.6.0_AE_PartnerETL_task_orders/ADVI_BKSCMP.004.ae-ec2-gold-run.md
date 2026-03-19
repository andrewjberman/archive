<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-19-bkscmp-004-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-19</date>
    <status>pending</status>
    <project_code>ADVI_BKSCMP</project_code>
  </metadata>

  <objective>
    Upload script 12 and the updated run_gold_layer.sh to S3, then run the gold layer
    in incremental mode on bd-gold-layer-runner. Verify firm_composition.json and
    per-advisor composition.json artifacts are written to S3.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_BKSCMP_PRD.md §WS4 (AE actions), §7 (acceptance criteria).
    Deployment standard: docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md.

    DS gate commit: ADVI_BKSCMP.001 req 7 (script 12 + run_gold_layer.sh commit to CLOUD).
    DS will report the commit SHA. Verify with:
      git log --oneline -- data/black_diamond/scripts/gold/12_build_composition_artifacts.py

    IMPORTANT gate: DT must have deployed opal-partners-data v2.8 (partners-api-v1.5.0)
    BEFORE verifying artifacts in the browser/portal. However, AE can run the gold layer
    (and produce the S3 artifacts) before the Lambda deploy. The artifacts just won't be
    serveable until partners-api-v1.5.0 is live. Run the gold layer as soon as the DS
    gate clears -- do not wait on DT.

    Run mode: INCREMENTAL is sufficient (holdings_lots is available incrementally;
    script 12 reads the latest parquet regardless of mode). Do NOT run FULL unless
    specifically requested.

    Note: This task order covers ONLY script 12 artifacts. The ADVI_MVP318.003 full gold
    run (for architect attribution, MIXV2, WS5 advisor timeseries) is a SEPARATE task order
    that AE should also execute. Both can be run in the same session.
  </context>

  <scope>
    <files>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/run_gold_layer.sh</file>
      <file action="run-on-ec2">run_gold_layer.sh --incremental</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" priority="gate">
      GATE: Confirm DS committed script 12 and updated run_gold_layer.sh to CLOUD.
      Check: git log --oneline -- data/black_diamond/scripts/gold/12_build_composition_artifacts.py
      And:   git log --oneline -- data/black_diamond/scripts/gold/run_gold_layer.sh
      Both must show the ADVI_BKSCMP.001 WS1 commit. Do not upload uncommitted code.
    </requirement>

    <requirement id="2">
      Upload script 12 to S3:
        export MSYS_NO_PATHCONV=1
        aws s3 cp data/black_diamond/scripts/gold/12_build_composition_artifacts.py \
          s3://opal-data-bd/code/gold/12_build_composition_artifacts.py
      Upload updated run_gold_layer.sh:
        aws s3 cp data/black_diamond/scripts/gold/run_gold_layer.sh \
          s3://opal-data-bd/code/
      Confirm both uploads succeed (HTTP 200 from aws s3 cp).
    </requirement>

    <requirement id="3">
      On bd-gold-layer-runner EC2 (via SSM or SSH), pull the updated scripts from S3.
      The run_gold_layer.sh s3 sync at startup pulls all scripts automatically, but
      run_gold_layer.sh itself must be re-pulled separately:
        aws s3 cp s3://opal-data-bd/code/run_gold_layer.sh ~/bd-gold/run_gold_layer.sh
      (Script 12 is pulled automatically via the `aws s3 sync s3://.../code/gold/ SCRIPTS_DIR/` at line 71.)
      Do NOT write code directly to EC2 -- pull from S3 only.
    </requirement>

    <requirement id="4">
      Run the gold layer in incremental mode:
        ./run_gold_layer.sh --incremental
      Monitor for errors. If the run fails at script 12 specifically, report the full
      stdout/stderr from that script to COO before retrying.
      Expected runtime for incremental: 15-30 min (script 12 adds holdings parquet read
      + pandas groupby computation; estimate 2-5 min for script 12 itself).
    </requirement>

    <requirement id="5">
      Verify artifacts after run completes:

      A. Firm composition:
        export MSYS_NO_PATHCONV=1
        aws s3 ls s3://opal-data-bd/gold/views/firm_composition.json
        aws s3 cp s3://opal-data-bd/gold/views/firm_composition.json - | python3 -m json.tool | head -40
        Confirm: file exists, parseable JSON, has "mix" array with top_holdings inside each class,
        has root "top_holdings" array, pct values are 0-1.

      B. Advisor compositions (spot-check):
        aws s3 ls s3://opal-data-bd/gold/advisors/ | head -20
        Confirm at least 5 advisors have a composition.json:
          aws s3 ls s3://opal-data-bd/gold/advisors/ | awk '{print $4}' | while read adv; do
            aws s3 ls s3://opal-data-bd/gold/advisors/${adv}composition.json 2>/dev/null &amp;&amp; echo "OK: $adv"
          done | head -5

      C. Pct sanity check on firm_composition.json:
        python3 -c "
        import json, boto3
        s3 = boto3.client('s3')
        data = json.loads(s3.get_object(Bucket='opal-data-bd', Key='gold/views/firm_composition.json')['Body'].read())
        for cls in data['mix']:
            th_sum = sum(h['pct'] for h in cls.get('top_holdings', []))
            other_pct = cls.get('other', {}).get('pct', 0)
            total = th_sum + other_pct
            print(f'{cls[\"asset_class\"]}: top_holdings pct sum={th_sum:.4f} + other={other_pct:.4f} = {total:.4f} (should be ~1.0)')
        "
        All class totals (top_holdings sum + other) should be approximately 1.0 (within 0.01).
    </requirement>

    <requirement id="6">
      Register the script 12 deployment in EC2_MANIFEST.json per the safe-ec2-deploy.sh protocol.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">DS gate commit confirmed before S3 upload</criterion>
    <criterion id="2">Script 12 and run_gold_layer.sh uploaded to S3 from committed CLOUD code</criterion>
    <criterion id="3">Incremental gold run completes without errors (all scripts including 12)</criterion>
    <criterion id="4">gold/views/firm_composition.json exists and is valid JSON matching PRD §3 schema</criterion>
    <criterion id="5">gold/advisors/{id}/composition.json exists for at least 5 advisors</criterion>
    <criterion id="6">Pct sanity: per-class top_holdings pct + other pct sums to ~1.0 per class</criterion>
    <criterion id="7">EC2_MANIFEST.json updated with deployment record</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>GATE: Do not upload before DS gate commit confirmed</constraint>
    <constraint>INCREMENTAL mode only -- FULL mode not required for script 12 (reads latest holdings_lots regardless)</constraint>
    <constraint>Do NOT write code directly to EC2 -- S3 is the artifact store (EC2_CODE_DEPLOYMENT_STANDARD.md)</constraint>
    <constraint>Do NOT inline script content in SSM commands</constraint>
    <constraint>No emojis in any SSM commands or log output (CLAUDE.md rule 13)</constraint>
    <constraint>Export MSYS_NO_PATHCONV=1 before any AWS CLI commands with S3 paths</constraint>
    <constraint>DT Lambda deploy (ADVI_BKSCMP.003) is NOT required before running the gold layer -- run as soon as DS gate clears</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_BKSCMP.001 req 7" status="pending">
      Script 12 + run_gold_layer.sh committed to CLOUD -- gate for S3 upload
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="verify">Incremental gold run complete; firm_composition.json and advisor compositions verified in S3</deliverable>
    <deliverable type="document">Session log with pct sanity check output and advisor count</deliverable>
    <deliverable type="document">EC2_MANIFEST.json updated</deliverable>
  </deliverables>
</task_order>
