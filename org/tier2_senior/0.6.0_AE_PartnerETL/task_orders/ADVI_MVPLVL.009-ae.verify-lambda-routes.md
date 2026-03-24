<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-23-mvplvl-009-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-23</date>
    <status>complete</status>
    <project_code>ADVI_MVPLVL</project_code>
    <thread_serial>ADVI_MVPLVL-006</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-006-mix-and-composition-e2e-trace----broken/</thread_ref>
  </metadata>

  <objective>
    REVISED 2026-03-23 (COO): Phase 1 HTTP verification revealed ALL 4 endpoints
    return 500 (Runtime.ImportModuleError: No module named 'etf_classifier').

    Root cause: The deployed Lambda zip is missing the real ETFClassifier. The file
    at infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/etf_classifier.py
    is a dummy stub (11 lines, no classify() method). The real DynamoDB-backed
    ETFClassifier lives at data/black_diamond/scripts/gold/lib/etf_classifier.py
    (134 lines, scans bd-securities DynamoDB table on cold start, O(1) lookups after).

    The Lambda imports etf_classifier at module level (line 63), so the stub causes
    an immediate import failure -- no request can be processed.

    S3 gold artifacts exist but have data issues (DS Phase 1 findings):
    - Script 12 on EC2 is pre-ETFClassifier (produces structured_notes instead
      of alternatives). Repo version correct but never deployed to EC2.
    - Script 06b advisor IDs used raw display names; DS fixed this (f6a4b5b8).
    - firm_mix_views.json has only 1 period per granularity (needs full rebuild).

    This task order has TWO tracks:

    TRACK A — Lambda fix (Req 1-5): COMPLETE (AE finished).
    1. Replace the dummy etf_classifier.py stub with the real DynamoDB-backed class
    2. Fix the source map to include etf_classifier.py in the zip
    3. Fix the advisor mix-timeseries S3 key (handle_advisor_mix_timeseries)
    4. Rebuild artifact + commit

    TRACK B — EC2 gold script deploy + full rebuild (Req 6-8): NEW.
    DS verification (f6a4b5b8 + findings report) revealed the deployed EC2
    gold scripts are stale. AE must deploy repo versions and run a full rebuild
    to produce correct artifacts for the Lambda to serve.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/etf_classifier.py</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="modify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      CRITICAL: Replace the dummy etf_classifier.py stub with the real
      DynamoDB-backed ETFClassifier.

      Source (canonical, used by gold scripts 06b + 12):
        data/black_diamond/scripts/gold/lib/etf_classifier.py (134 lines)

      Destination (Lambda source directory):
        infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/etf_classifier.py

      Copy the file verbatim. Do NOT modify the class. The Lambda already imports
      it correctly at line 63:
        from etf_classifier import ETFClassifier as _ETFClassifier

      The real ETFClassifier:
      - Scans bd-securities DynamoDB table on cold start (full table scan)
      - All subsequent classify() calls are O(1) dict lookups
      - Returns 'equity' | 'fixed_income' | 'alternatives' | '' (empty = cash residual)
      - 4-layer classification: ticker lookup -> name alias -> regex pattern -> alpha heuristic
      - This is the ONLY classifier that matters. bd-securities DynamoDB is the single
        source of truth for security classification.

      Do NOT use etf_classification.py (the 44KB Yang pipeline hardcoded dict module).
      That file is unrelated to BD classification and is dead weight in this Lambda.
      It can remain in the directory (nothing imports it from lambda_function.py) but
      do not confuse it with the real classifier.
    </requirement>

    <requirement id="2">
      Fix lambda-source-map.json: ensure the files array for opal-partners-data
      includes etf_classifier.py.

      The previous source map listed only lambda_function.py and etf_classification.py,
      which is why the real etf_classifier.py was never packaged into the zip.
    </requirement>

    <requirement id="3">
      Fix advisor mix-timeseries S3 key bug in lambda_function.py:
      - In handle_advisor_mix_timeseries(), change S3 key from
        gold/advisors/{advisor_id}/mix.json to gold/advisors/{advisor_id}/mix_timeseries.json
      - This is a one-line fix at approximately line 1056.
    </requirement>

    <requirement id="4">
      Commit all three fixes to CLOUD. Then rebuild the Lambda artifact:
        bash infra/aws/lambda/ci/build-and-upload.sh partners-api opal-partners-data

      Commit the updated source map hash. Do NOT run terraform apply -- DT handles that.
    </requirement>

    <requirement id="5">
      After DT deploys Lambda, re-verify all 4 endpoints return 200:
      1. GET /api/scoped/partners/books/firm/all/mix-views?firmId=49financial
      2. GET /api/scoped/partners/books/firm/all/composition?firmId=49financial
      3. GET /api/scoped/partners/books/advisor/{sample_id}/composition?firmId=49financial
      4. GET /api/scoped/partners/books/relationship/{sample_id}/composition?firmId=49financial

      All should now return 200 with valid JSON (S3 artifacts confirmed present).
    </requirement>

    <!-- ============================================================ -->
    <!-- TRACK B: EC2 gold script deploy + full rebuild (NEW)         -->
    <!-- DS Phase 1 findings require AE to redeploy and rebuild       -->
    <!-- ============================================================ -->

    <requirement id="6">
      Deploy updated gold scripts 06b + 12 to EC2 gold runner via safe-ec2-deploy.sh.

      Both scripts must be the repo HEAD versions:
      - 06b: commit f6a4b5b8 (DS fix: _advisor_id() snake_case normalization)
      - 12: commit 5c6fd9d0 (ETFClassifier migration, uses bd-securities DynamoDB)

      The currently deployed EC2 copies are stale:
      - Script 12 was uploaded 2026-03-19, BEFORE the ETFClassifier migration.
        It produces structured_notes instead of alternatives. This is wrong.
        DynamoDB bd-securities only has equity/fixed_income/alternatives -- no
        structured_notes.
      - Script 06b was writing advisor IDs with raw display names (spaces)
        instead of snake_case, causing S3 key mismatches with script 12.

      Follow EC2 code deployment standard: repo -> S3 -> EC2 pulls.
    </requirement>

    <requirement id="7">
      Run a FULL gold rebuild (not incremental) after deploying updated scripts.

      Full rebuild is required because:
      (a) Script 12 taxonomy must change from structured_notes to alternatives
          across ALL composition artifacts (firm + every advisor)
      (b) Script 06b advisor ID paths must be rewritten from display names to
          snake_case across ALL advisor mix files
      (c) firm_mix_views.json currently has only 1 period per granularity --
          full rebuild produces the complete date range

      An incremental run would only process new dates and leave stale artifacts.
    </requirement>

    <requirement id="8">
      After gold rebuild completes, verify regenerated artifacts:

      1. firm_composition.json uses 'alternatives' (NOT 'structured_notes'):
         aws s3 cp s3://opal-data-bd/gold/views/firm_composition.json - | python3 -c "
         import json,sys; d=json.load(sys.stdin)
         classes = [m['asset_class'] for m in d.get('mix',[])]
         print(f'classes: {classes}')
         assert 'structured_notes' not in classes, 'FAIL: structured_notes still present'
         assert 'alternatives' in classes, 'FAIL: alternatives missing'
         print('PASS: 4-class taxonomy correct')"

      2. firm_mix_views.json has full date range (more than 1 period per granularity):
         aws s3 cp s3://opal-data-bd/gold/firm_mix_views.json - | python3 -c "
         import json,sys; d=json.load(sys.stdin)
         for g in ['quarterly','monthly','annually']:
             n = len(d['views'][g])
             print(f'{g}: {n} periods')
             assert n > 1, f'FAIL: {g} has only {n} period(s)'"

      3. Advisor paths use snake_case consistently:
         aws s3 ls s3://opal-data-bd/gold/advisors/ | head -10
         # Should show snake_case dirs (josh_henson/), NOT display names (Josh Henson/)
    </requirement>
  </requirements>

  <acceptance_criteria>
    <!-- Track A (Lambda) -->
    <criterion id="1">etf_classifier.py in Lambda source is the real DynamoDB-backed class (134 lines, imports boto3, has classify() method with 4-layer lookup) — DONE</criterion>
    <criterion id="2">lambda-source-map.json includes etf_classifier.py in the opal-partners-data files array — DONE</criterion>
    <criterion id="3">handle_advisor_mix_timeseries uses mix_timeseries.json S3 key (not mix.json) — DONE</criterion>
    <criterion id="4">Lambda artifact rebuilt and uploaded to S3 (build-and-upload.sh) — DONE</criterion>
    <criterion id="5">Source map hash committed to CLOUD — DONE</criterion>
    <criterion id="6">After DT deploy: all 4 endpoints return 200 with valid JSON</criterion>
    <!-- Track B (EC2 gold rebuild) -->
    <criterion id="7">Updated scripts 06b (f6a4b5b8) + 12 (5c6fd9d0) deployed to EC2 via safe-ec2-deploy.sh</criterion>
    <criterion id="8">Full gold rebuild completed (not incremental)</criterion>
    <criterion id="9">firm_composition.json uses alternatives (not structured_notes)</criterion>
    <criterion id="10">firm_mix_views.json has full date range (more than 1 period per granularity)</criterion>
    <criterion id="11">Advisor paths use snake_case consistently (no display names with spaces)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT deploy Lambda changes via Terraform -- DT bundles and deploys.</constraint>
    <constraint>Do NOT modify the real ETFClassifier class. Copy it verbatim.</constraint>
    <constraint>Do NOT use etf_classification.py (Yang hardcoded dicts) for BD classification. The ONLY classifier is the DynamoDB-backed ETFClassifier reading from bd-securities.</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13).</constraint>
    <constraint>Commit with --author="0.6.0_AE_PartnerETL &lt;0.6.0_AE_PartnerETL@opal.agent&gt;"</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      Lambda partners-api-v1.8.0 deployed (but broken at import).
      Real ETFClassifier source available at data/black_diamond/scripts/gold/lib/etf_classifier.py.
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVPLVL.009-ds.verify-s3-data" status="complete">
      DS Phase 1 verification complete. 06b fix committed (f6a4b5b8).
      Three findings delivered. Track B requirements sourced from DS report.
    </dependency>
  </dependencies>

  <deliverables>
    <!-- Track A (Lambda) — COMPLETE -->
    <deliverable type="commit">Three fixes committed to CLOUD: (1) real etf_classifier.py, (2) source map fix, (3) mix_timeseries S3 key fix — DELIVERED</deliverable>
    <deliverable type="commit">Lambda artifact rebuilt and uploaded (build-and-upload.sh) — DELIVERED</deliverable>
    <deliverable type="document">Post-deploy HTTP verification report (after DT deploys)</deliverable>
    <!-- Track B (EC2 gold rebuild) — PENDING -->
    <deliverable type="deploy">Updated scripts 06b + 12 deployed to EC2 gold runner</deliverable>
    <deliverable type="verify">Full gold rebuild completed with correct taxonomy + consistent advisor IDs + full date range</deliverable>
  </deliverables>
</task_order>
