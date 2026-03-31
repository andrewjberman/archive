<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-20-gldpre-005-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-20</date>
    <status>complete</status>
    <project_code>ADVI_GLDPRE</project_code>
  </metadata>

  <objective>
    Deploy all GLDPRE code changes to AWS and run a FULL gold layer rebuild.
    Three deployment targets: (1) Lambda opal-partners-data via Terraform (WS3 mix.json fix),
    (2) EC2 gold scripts via S3 sync (WS1 06b ETFClassifier), (3) full gold rerun to produce
    4-class firm_mix_views.json with cash-as-residual. WS2 (client_performance total
    substitution) was committed to 06b at 61f76c8b — all code gates are cleared.
  </objective>

  <context>
    Reference:
    - docs/architecture/ADVI_GLDPRE_PRD.md (full PRD)
    - docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md (Lambda deploy sequence)
    - docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md (repo -> S3 -> EC2 pull)
    - infra/aws/lambda/ci/lambda-source-map.json (source of truth for Lambda versions)
    - infra/aws/ec2/EC2_MANIFEST.json (source of truth for EC2 services)

    Commits already on CLOUD:
    - 3ede9fc4: [GLDPRE] WS1+WS3 -- 06b ETFClassifier 4-class + Lambda mix.json fix
    - Lambda source map last deploy: ca118d1c (partners-api-v1.7.0, 2026-03-19)
    - EC2 gold scripts last deploy: 8d0546634d (2026-03-18)

    What changed:
    - data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py
      ETFClassifier wired, 4-class taxonomy, cash residual, ~219 lines static dicts removed
    - infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py
      Line 1056: mix_timeseries.json -> mix.json (handle_advisor_mix_timeseries)
    - data/black_diamond/scripts/gold/09_generate_partner_analytics.py (WS2, pending DS commit)
      aua_mix section -- will be committed by DS before this task order executes

    Pending DS commit (WS2 gate):
    WS2 landed in 06b (61f76c8b), not script 09. All code gates cleared.
      No script 09 changes needed. Proceed with all phases.
  </context>

  <scope>
    <files>
      <file action="lambda-deploy">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/lib/etf_classifier.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/lib/__init__.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/run_gold_layer.sh</file>
      <file action="upload-to-s3">data/black_diamond/scripts/silver/bd_price_update.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/silver/inject_scoped_overrides.py</file>
      <!-- script 09 not changed — WS2 went into 06b instead -->
      <file action="run-on-ec2">run_gold_layer.sh --full</file>
    </files>
  </scope>

  <requirements>
    <!-- ============================================================ -->
    <!-- PHASE 1: Lambda deploy (WS3) — no dependencies, do first     -->
    <!-- ============================================================ -->

    <requirement id="1" priority="phase-1">
      Deploy opal-partners-data Lambda with the WS3 fix (mix.json).
      Follow the LAMBDA_DEPLOYMENT_PROTOCOL exactly:

      Step 1: Build and upload artifact to S3:
        export MSYS_NO_PATHCONV=1
        bash infra/aws/lambda/ci/build-and-upload.sh partners-api opal-partners-data
      Expected output: prints SHA256 and 'Complete -- 1 function(s) built and uploaded'

      Step 2: Commit the source map update:
        git add infra/aws/lambda/ci/lambda-source-map.json
        git commit --author="0.6.0_AE_PartnerETL &lt;0.6.0_AE_PartnerETL@opal.agent&gt;" \
          -m "ci(partners-api): upload opal-partners-data artifact (GLDPRE WS3 mix.json fix)"

      Step 3: Terraform plan (read-only verify):
        cd infra/aws/terraform/partners-api
        export MSYS_NO_PATHCONV=1
        ../../../../.tools/terraform.exe plan -no-color 2>&amp;1 | tail -10
      Must show: 1 to change (s3_object_version on the Lambda), 0 to destroy.

      Step 4: Terraform apply:
        ../../../../.tools/terraform.exe apply -auto-approve -no-color 2>&amp;1 | tail -10

      Step 5: 0-diff verify:
        ../../../../.tools/terraform.exe plan -no-color 2>&amp;1 | tail -5
      Must show: No changes. Your infrastructure matches the configuration.

      Step 6: Tag:
        git tag -l "partners-api-v*" | sort -V | tail -3
        (Check actual latest tag before tagging. Do NOT assume v1.8.0 — verify.)
        git tag -a partners-api-v{NEXT} -m "GLDPRE WS3: advisor mix filename fix (mix_timeseries -> mix)"

      Step 7: Record deploy:
        bash infra/aws/lambda/ci/record-terraform-deploy.sh partners-api --version partners-api-v{NEXT}
        git add infra/aws/lambda/ci/lambda-source-map.json infra/aws/terraform/partners-api/CHANGELOG.json
        git commit --author="0.6.0_AE_PartnerETL &lt;0.6.0_AE_PartnerETL@opal.agent&gt;" \
          -m "ci: record deploy partners-api @ $(git rev-parse --short HEAD) [skip ci]"

      Step 8: Push with tags:
        git push --follow-tags
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE 1b: Silver scripts deploy (scoped overrides)           -->
    <!-- ============================================================ -->

    <requirement id="1b" priority="phase-1">
      CRITICAL: Deploy scoped price override fix to EC2 silver scripts.
      Without this, the next daily bd_price_update.py run will re-introduce the
      BNP Yahoo price ($96.63 vs correct $0.75), causing ~$20.6M AUA error.
      Commit a6b68032 restored these changes after they were lost during
      GLDPRE stash operations.

      Upload to S3:
        aws s3 cp data/black_diamond/scripts/silver/bd_price_update.py \
          s3://opal-data-bd/code/silver/bd_price_update.py
        aws s3 cp data/black_diamond/scripts/silver/inject_scoped_overrides.py \
          s3://opal-data-bd/code/silver/inject_scoped_overrides.py

      Verify scoped overrides are in the uploaded file:
        aws s3 cp s3://opal-data-bd/code/silver/bd_price_update.py /tmp/bpu_check.py
        grep -c "_SCOPED_PRICE_OVERRIDES" /tmp/bpu_check.py
      Expected: >= 2 (definition + lookup map)

      This is TIME-SENSITIVE — the daily price run could execute before the gold rerun.
      Deploy silver scripts BEFORE starting Phase 2.
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE 2: EC2 code deploy (WS1) — no dependencies             -->
    <!-- ============================================================ -->

    <requirement id="2" priority="phase-2">
      Upload updated gold scripts to S3 per EC2_CODE_DEPLOYMENT_STANDARD.md.

      Upload 06b (changed), lib/etf_classifier.py (dependency), lib/__init__.py (required for import),
      script 12 (BKSCMP composition artifacts — new), and run_gold_layer.sh (updated to include 12):
        export AWS_EC2_METADATA_DISABLED=true
        export MSYS_NO_PATHCONV=1
        aws s3 cp data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py \
          s3://opal-data-bd/code/gold/06b_build_client_mix_timeseries.py
        aws s3 cp data/black_diamond/scripts/gold/lib/etf_classifier.py \
          s3://opal-data-bd/code/gold/lib/etf_classifier.py
        aws s3 cp data/black_diamond/scripts/gold/lib/__init__.py \
          s3://opal-data-bd/code/gold/lib/__init__.py
        aws s3 cp data/black_diamond/scripts/gold/12_build_composition_artifacts.py \
          s3://opal-data-bd/code/gold/12_build_composition_artifacts.py
        aws s3 cp data/black_diamond/scripts/gold/run_gold_layer.sh \
          s3://opal-data-bd/code/gold/run_gold_layer.sh

      CRITICAL: lib/__init__.py must be uploaded or `from lib.etf_classifier import ETFClassifier`
      will fail with ModuleNotFoundError on EC2. If lib/__init__.py does not exist locally, create
      an empty one: `touch data/black_diamond/scripts/gold/lib/__init__.py`

      CRITICAL: script 12 and the updated run_gold_layer.sh MUST be uploaded. Script 12 is
      wired into run_gold_layer.sh at lines 116 (incremental) and 163 (full). If script 12
      is missing from S3, run_gold_layer.sh will fail when it tries to execute it.
      This covers ADVI_BKSCMP.004 (AE EC2 gold run).

      Do NOT upload uncommitted files. Do NOT write code directly to EC2.
    </requirement>

    <requirement id="3" priority="phase-2">
      run_gold_layer.sh syncs code from S3 to /tmp/gold_layer_scripts/ automatically
      before execution. The S3 upload in req 2 is sufficient — no manual EC2 pull needed.

      After the S3 upload, verify the ETFClassifier import will resolve by checking
      that lib/__init__.py exists in S3:
        aws s3 ls s3://opal-data-bd/code/gold/lib/
      Expected output should show __init__.py and etf_classifier.py.

      If you want to pre-verify on EC2 before the gold run:
        cd /tmp/gold_layer_scripts  (or wherever run_gold_layer.sh syncs to)
        python3 -c "from lib.etf_classifier import ETFClassifier; print('OK:', len(ETFClassifier.instance()._ticker_map), 'tickers')"
      Expected: OK: {N} tickers (N >= 116, seeded by CLSUNI)
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE 3: WS2 gate — wait for DS commit                       -->
    <!-- ============================================================ -->

    <requirement id="4" priority="gate">
      WS2 GATE: CLEARED. DS committed WS2 to 06b (not script 09) at 61f76c8b.
      WS2 substitutes client_performance total into 06b's compute_period_views.
      Since 06b is already uploaded in Phase 2 (req 2), no additional S3 upload
      is needed for WS2. Proceed directly to Phase 4.

      Verify WS2 commit is on CLOUD:
        git log --oneline -1 61f76c8b
      Expected: [GLDPRE] WS2: substitute client_performance total into 06b firm_mix_views

      IMPORTANT: The 06b uploaded in Phase 2 must be from HEAD (which includes
      both WS1 at 3ede9fc4 AND WS2 at 61f76c8b). If you already uploaded 06b
      before WS2 was committed, re-upload it:
        aws s3 cp data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py \
          s3://opal-data-bd/code/gold/06b_build_client_mix_timeseries.py
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE 4: Full gold rerun                                      -->
    <!-- ============================================================ -->

    <requirement id="5">
      Run FULL gold layer on bd-gold-layer-runner:
        cd ~/bd-gold/data/black_diamond/scripts/gold
        ./run_gold_layer.sh full

      FULL mode is required because 06b classification logic changed (ETFClassifier
      replaces static dicts). All client_timeseries, firm_mix_views, and advisor mix
      files must be regenerated with the 4-class taxonomy.

      Expected runtime: 60-90 min. Monitor for errors. ETFClassifier.instance() will
      do one DynamoDB table scan on first call (~2s for 116+ items), then O(1) lookups.
      If ETFClassifier scan fails (IAM or table issue), 06b will log the error and
      fall back to empty maps — all positions will classify as equity. This is WRONG.
      If you see "ETFClassifier: scan failed" in the output, STOP and report to COO.
    </requirement>

    <requirement id="6">
      After gold run completes, verify GLDPRE acceptance criteria:

      Check 1: firm_mix_views.json has exactly 4 classes per period:
        aws s3 cp s3://opal-data-bd/gold/firm_mix_views.json /tmp/fmv.json
        python3 -c "
        import json
        d = json.load(open('/tmp/fmv.json'))
        for p in d['views']['quarterly'][-3:]:
            classes = [k for k in p if k not in ('period','label','end_date','total_aua')]
            print(f\"{p['period']}: {classes}, total={p['total_aua']}\")
            assert set(classes) == {'equity','fixed_income','alternatives','cash'}, f'Wrong classes: {classes}'
            s = sum(p[c]['value'] for c in classes)
            assert abs(s - p['total_aua']) < 0.02, f'Sum {s} != total {p[\"total_aua\"]}'
        print('PASS: 4 classes, sum matches total')
        "

      Check 2: Cash is residual (not independently classified):
        python3 -c "
        import json
        d = json.load(open('/tmp/fmv.json'))
        p = d['views']['quarterly'][-1]
        eq_fi_alt = p['equity']['value'] + p['fixed_income']['value'] + p['alternatives']['value']
        cash = p['cash']['value']
        print(f'eq+fi+alt={eq_fi_alt:.2f}, cash={cash:.2f}, total={p[\"total_aua\"]:.2f}')
        assert abs(eq_fi_alt + cash - p['total_aua']) < 0.02, 'Cash residual mismatch'
        print('PASS: cash = total - classified')
        "

      Check 3: Advisor mix files exist with 4 classes:
        aws s3 ls s3://opal-data-bd/gold/advisors/ --recursive | grep mix.json | head -5
        (Should show mix.json for multiple advisors)

      Check 4: firm_mix_views.json total_aua matches client_performance (WS2):
        python3 -c "
        import json, boto3, pandas as pd
        from io import BytesIO
        s3 = boto3.client('s3', region_name='us-east-1')
        fmv = json.load(open('/tmp/fmv.json'))
        obj = s3.get_object(Bucket='opal-data-bd', Key='gold/client_performance.parquet')
        cp = pd.read_parquet(BytesIO(obj['Body'].read()))
        latest = cp['date'].max()
        cp_total = cp[cp['date'] == latest]['total_aua'].sum()
        fmv_total = fmv['views']['quarterly'][-1]['total_aua']
        diff = abs(fmv_total - cp_total)
        print(f'client_performance total: {cp_total:,.2f}')
        print(f'firm_mix_views total:     {fmv_total:,.2f}')
        print(f'diff: {diff:,.2f}')
        assert diff < 1.0, f'Total divergence too large: {diff}'
        print('PASS: firm_mix_views total matches client_performance')
        "

      Check 5: No structured_notes, other, or 5-class data in output:
        python3 -c "
        import json
        d = json.load(open('/tmp/fmv.json'))
        text = json.dumps(d)
        for bad in ['structured_notes', '\"other\"']:
            assert bad not in text, f'Found {bad} in firm_mix_views.json'
        print('PASS: no legacy classes in output')
        "
    </requirement>

    <requirement id="7">
      Update EC2_MANIFEST.json with the deployment record.
      Use safe-ec2-deploy.sh or manually update the bd-gold-layer-runner entry:
        export PATH="/c/Users/AndrewBerman/Desktop/ajb_workspace/.tools:$PATH"
        deployed_commit=$(git rev-parse --short HEAD)
        deployed_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

      Update fields in EC2_MANIFEST.json:
        deployed_commit: {current HEAD}
        deployed_at: {timestamp}
        deployed_by: 0.6.0_AE_PartnerETL
        last_deploy: {YYYY-MM-DD}
        last_deploy_commit: {short SHA}
        last_deploy_note: "GLDPRE: 06b ETFClassifier 4-class + 09 aua_mix + full gold rerun"

      Commit:
        git add infra/aws/ec2/EC2_MANIFEST.json
        git commit --author="0.6.0_AE_PartnerETL &lt;0.6.0_AE_PartnerETL@opal.agent&gt;" \
          -m "ci: record EC2 deploy bd-gold-layer-runner @ $(git rev-parse --short HEAD) (GLDPRE)"
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Lambda opal-partners-data deployed via Terraform; 0-diff plan passes; tag pushed</criterion>
    <criterion id="2">06b + lib/etf_classifier.py uploaded to S3 and pulled to EC2</criterion>
    <criterion id="3">ETFClassifier.instance() resolves on EC2 with >= 116 tickers</criterion>
    <criterion id="4">WS2 commit (61f76c8b) included in uploaded 06b — verify by checking HEAD includes both WS1+WS2</criterion>
    <criterion id="5">FULL gold layer completes without errors</criterion>
    <criterion id="6">firm_mix_views.json: exactly 4 classes, sum equals total_aua, cash is residual</criterion>
    <criterion id="7">Advisor mix.json files present for >= 10 advisors</criterion>
    <criterion id="8">firm_mix_views.json total_aua matches client_performance total for same date (within $1)</criterion>
    <criterion id="9">No structured_notes or other in firm_mix_views.json</criterion>
    <criterion id="10">EC2_MANIFEST.json updated with deployment record</criterion>
    <criterion id="11">lambda-source-map.json updated; CHANGELOG.json written; tag pushed</criterion>
    <criterion id="12">BKSCMP: 12_build_composition_artifacts.py uploaded to S3 and executed in gold run</criterion>
    <criterion id="13">BKSCMP: firm_composition.json exists in S3 (s3://opal-data-bd/gold/firm_composition.json)</criterion>
    <criterion id="14">BKSCMP: per-advisor composition.json files exist (s3://opal-data-bd/gold/advisors/*/composition.json — expect >= 10)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Follow LAMBDA_DEPLOYMENT_PROTOCOL exactly — Terraform is the only Lambda deploy mechanism</constraint>
    <constraint>Follow EC2_CODE_DEPLOYMENT_STANDARD — repo -> S3 -> EC2 pull, never write code directly to EC2</constraint>
    <constraint>Do NOT upload uncommitted code to S3 — verify HEAD includes WS2 commit 61f76c8b before uploading 06b</constraint>
    <constraint>Do NOT start gold run until ETFClassifier.instance() resolves on EC2 (req 3 verify)</constraint>
    <constraint>If ETFClassifier scan fails during gold run, STOP and report — do not let it silently fall back</constraint>
    <constraint>FULL mode only — incremental will not reclassify existing positions with new taxonomy</constraint>
    <constraint>Export MSYS_NO_PATHCONV=1 before AWS CLI commands with S3/ARN paths on Git Bash</constraint>
    <constraint>Export AWS_EC2_METADATA_DISABLED=true before any AWS CLI or botocore command</constraint>
    <constraint>No emojis in any SSM commands, scripts, or log output (CLAUDE.md rule 13)</constraint>
    <constraint>Tag version: check actual latest with git tag -l, do NOT assume next number</constraint>
    <constraint>Commit before apply — code must be committed to CLOUD before terraform plan/apply</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="GLDPRE WS2" status="complete">
      DS committed WS2 to 06b at 61f76c8b on CLOUD. Gate cleared.
      06b now reads client_performance total instead of independent positions_cube sum.
    </dependency>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ClientsTab.tsx fix" status="complete">
      DT committed a466a7b on portal DEV. Gate cleared.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">Lambda opal-partners-data at partners-api-v{NEXT} (mix.json fix)</deliverable>
    <deliverable type="deploy">06b + lib/etf_classifier.py on EC2 via S3</deliverable>
    <!-- Script 09 not changed — WS2 went into 06b -->
    <deliverable type="verify">FULL gold layer run complete; all acceptance criteria verified</deliverable>
    <deliverable type="document">EC2_MANIFEST.json updated</deliverable>
    <deliverable type="document">lambda-source-map.json updated, CHANGELOG.json written</deliverable>
    <deliverable type="document">Session log with verification output</deliverable>
  </deliverables>
</task_order>
