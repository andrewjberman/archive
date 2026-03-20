<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-20-clspt2-002-ae</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-20</date>
    <status>pending</status>
    <project_code>ADVI_CLSPT2</project_code>
  </metadata>

  <objective>
    Upload classify_bd_securities.py to S3 and run it on bd-gold-layer-runner EC2
    to enrich the bd-securities DynamoDB table beyond the 116 Yang-seeded items.
    This populates ETFClassifier with the full BD client securities universe so
    that mix classification in the gold layer is accurate for all holdings.
  </objective>

  <context>
    File: data/black_diamond/scripts/classification/classify_bd_securities.py
    S3 target: s3://opal-data-bd/code/classification/classify_bd_securities.py

    The script:
    1. Reads the latest holdings_lots parquet from s3://opal-data-bd/gold/holdings_lots/
    2. Scans bd-securities DynamoDB for already-classified tickers
    3. Batches new (ticker, asset_name) pairs to OpenAI gpt-4o-mini (50 per call)
    4. Writes classified items back to bd-securities with asset_class, sub_asset_class,
       confidence, needs_review fields
    5. Writes summary manifest to s3://opal-data-bd/gold/manifests/classification_{date}.json

    Runtime: 30-60 minutes (depends on number of new securities).
    Cost: ~$0.01-0.05 for gpt-4o-mini on ~2000 securities.

    Pre-requisite: DS must finish the script implementation first (CLSPT2.001).
    The current version is a stub with commented-out OpenAI logic.
  </context>

  <scope>
    <files>
      <file action="upload-to-s3">data/black_diamond/scripts/classification/classify_bd_securities.py</file>
      <file action="run-on-ec2">classify_bd_securities.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PRE-FLIGHT: Verify DS has finished the script implementation.
        git log --oneline -5 data/black_diamond/scripts/classification/classify_bd_securities.py

      The latest commit should NOT be the runtime stub (ca118d1c). There should be
      a newer commit with real OpenAI implementation. If the script still has
      commented-out placeholder code at lines 64-112, STOP -- DS CLSPT2.001 is not done.

      Also verify:
        grep -c "client.chat.completions.create" data/black_diamond/scripts/classification/classify_bd_securities.py
      Expected: >= 1 (real OpenAI call present)

        grep -c "mocked_response" data/black_diamond/scripts/classification/classify_bd_securities.py
      Expected: 0 (no mock code remaining)
    </requirement>

    <requirement id="2">
      PRE-FLIGHT: Verify bd-securities table is accessible and seeded.
        export AWS_EC2_METADATA_DISABLED=true
        aws dynamodb scan --table-name bd-securities --select COUNT --region us-east-1 \
          --query 'Count' --output text
      Expected: >= 116

      Verify openai-api-key secret is accessible:
        aws secretsmanager get-secret-value --secret-id openai-api-key --region us-east-1 \
          --query 'Name' --output text
      Expected: openai-api-key (not an error)
    </requirement>

    <requirement id="3">
      Upload script to S3:
        export AWS_EC2_METADATA_DISABLED=true
        export MSYS_NO_PATHCONV=1
        aws s3 cp data/black_diamond/scripts/classification/classify_bd_securities.py \
          s3://opal-data-bd/code/classification/classify_bd_securities.py
    </requirement>

    <requirement id="4">
      Dry run first on EC2:
        Start bd-gold-layer-runner if not running.
        SSM or SSH to the instance.
        aws s3 cp s3://opal-data-bd/code/classification/classify_bd_securities.py /tmp/classify.py
        python3 /tmp/classify.py --dry-run 2>&amp;1 | tail -20

      Verify: prints count of new securities to classify, does NOT write to DynamoDB.
      If errors, STOP and report.
    </requirement>

    <requirement id="5">
      Production run:
        python3 /tmp/classify.py 2>&amp;1 | tee /tmp/classify_output.log

      Monitor for:
      - Progress prints every 100 items
      - No unhandled exceptions
      - Completion message with item count
      Runtime: 30-60 minutes.
    </requirement>

    <requirement id="6">
      Post-run verification:
        aws dynamodb scan --table-name bd-securities --select COUNT --region us-east-1 \
          --query 'Count' --output text
      Expected: > 500 (BD client universe is large)

      Spot-check 5 random items:
        aws dynamodb scan --table-name bd-securities --max-items 5 --region us-east-1 \
          --query 'Items[*].{ticker:ticker.S,class:asset_class.S,conf:confidence.N,review:needs_review.BOOL}'
      Verify: asset_class is one of equity|fixed_income|alternatives, confidence is 0-1.

      Check manifest was written:
        aws s3 ls s3://opal-data-bd/gold/manifests/ | grep classification
      Expected: classification_{today}.json present
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">DS CLSPT2.001 complete (no stub code in classify_bd_securities.py)</criterion>
    <criterion id="2">Script uploaded to s3://opal-data-bd/code/classification/</criterion>
    <criterion id="3">Dry run completes without errors</criterion>
    <criterion id="4">Production run completes without unhandled exceptions</criterion>
    <criterion id="5">bd-securities item count > 500 after run</criterion>
    <criterion id="6">All items have asset_class in equity|fixed_income|alternatives</criterion>
    <criterion id="7">Classification manifest written to S3</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT run production classify without dry-run first</constraint>
    <constraint>Do NOT modify classify_bd_securities.py -- DS owns the code, AE runs it</constraint>
    <constraint>Export AWS_EC2_METADATA_DISABLED=true before any AWS CLI or botocore command</constraint>
    <constraint>Export MSYS_NO_PATHCONV=1 before S3 path commands on Git Bash</constraint>
    <constraint>No emojis in SSM commands or log output (CLAUDE.md rule 13)</constraint>
    <constraint>If ETFClassifier scan errors appear, STOP and report to COO</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_CLSPT2.001" status="pending">
      DS must finish classify_bd_securities.py implementation (replace stub with real
      OpenAI chat completions calls). Pre-flight check in req 1 verifies this.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">classify_bd_securities.py uploaded to S3 and executed on EC2</deliverable>
    <deliverable type="verify">bd-securities DynamoDB enriched to > 500 items</deliverable>
    <deliverable type="document">Session log with verification output and item counts</deliverable>
  </deliverables>
</task_order>
