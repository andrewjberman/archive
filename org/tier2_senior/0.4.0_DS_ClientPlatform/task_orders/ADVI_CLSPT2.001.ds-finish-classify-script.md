<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-20-clspt2-001-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-20</date>
    <status>complete</status>
    <project_code>ADVI_CLSPT2</project_code>
  </metadata>

  <objective>
    Finish the classify_bd_securities.py implementation. The script exists but
    the OpenAI classification logic (lines 64-112) is entirely stubbed/commented out.
    Wire real OpenAI chat completions API calls using the spec in the PRD
    (docs/architecture/ADVI_CLSPT2_PRD.md section WS2).
  </objective>

  <context>
    File: data/black_diamond/scripts/classification/classify_bd_securities.py

    Current state: The script correctly reads holdings_lots parquet from S3,
    extracts unique (ticker, asset_name) pairs, scans bd-securities for existing
    tickers, and filters to new pairs. But lines 64-112 are commented-out
    placeholder code with a fake API URL (https://api.openai.com/v1/classify).
    The actual OpenAI chat completions call was never implemented.

    Also: lines 126-134 contain dead code (_classify_holding function referencing
    undefined _clf). Remove these.

    OpenAI key: stored in AWS Secrets Manager as 'openai-api-key'. The script
    already has the secrets_manager client and retrieval code at line 65-66.

    PRD spec (ADVI_CLSPT2_PRD.md WS2) defines:
    - System prompt with canonical sub-asset class vocabulary
    - Batch size: 50 items per API call
    - Model: gpt-4o-mini
    - Response format: JSON array "results"
    - Key scheme: ticker as PK for 1-5 alpha tickers, NAME::{normalize} for CUSIPs
    - Confidence scoring, needs_review threshold at 0.7
    - Idempotent (skip existing), exponential backoff
    - Summary manifest at gold/manifests/classification_{date}.json
  </context>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/classification/classify_bd_securities.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Replace the stubbed OpenAI logic (lines 64-112) with real implementation:

      Use the openai Python library (already available in the EC2 environment):
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

      For each batch of 50 new (ticker, asset_name) pairs, call:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': json.dumps(batch_items)}
            ],
            response_format={'type': 'json_object'},
            temperature=0.1
        )

      Parse the JSON response and extract asset_class, sub_asset_class, confidence,
      rationale for each item.
    </requirement>

    <requirement id="2">
      Use the system prompt from the PRD (ADVI_CLSPT2_PRD.md WS2):

      Classify each security. Use EXACTLY these asset_class values:
        equity | fixed_income | alternatives

      Sub-asset class vocabulary and confidence scoring per the PRD.

      Return JSON object with "results" array.
    </requirement>

    <requirement id="3">
      Key scheme per PRD:
      - Standard 1-5 alpha tickers: use ticker as PK
      - CUSIP-based (9-char alphanumeric starting with digit): use NAME::{normalized_asset_name}
      - normalize_key() already exists in detect_new_securities.py for reference
    </requirement>

    <requirement id="4">
      Write each classified item to bd-securities DynamoDB:
        table.put_item(Item={
            'ticker': pk,
            'asset_class': result['asset_class'],
            'sub_asset_class': result['sub_asset_class'],
            'confidence': Decimal(str(result['confidence'])),
            'needs_review': result['confidence'] < 0.7,
            'classified_by': 'gpt-4o-mini',
            'rationale': result.get('rationale', ''),
            'asset_name_raw': asset_name,
            'last_updated': datetime.utcnow().isoformat() + 'Z'
        })

      Respect --dry-run flag: print what would be written but don't call put_item.
    </requirement>

    <requirement id="5">
      Add exponential backoff for rate limiting (gpt-4o-mini: 500 RPM).
      Print progress every 100 items.
      At completion, write summary to stdout and to
      gold/manifests/classification_{date}.json on S3.
    </requirement>

    <requirement id="6">
      Remove dead code at lines 126-134 (_classify_holding function).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Script runs to completion with --dry-run without errors</criterion>
    <criterion id="2">OpenAI API is called with correct model, system prompt, and response_format</criterion>
    <criterion id="3">No items written with asset_class outside equity|fixed_income|alternatives</criterion>
    <criterion id="4">Dead code at bottom of file removed</criterion>
    <criterion id="5">Idempotent: re-running skips already-classified items</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT change detect_new_securities.py -- it is complete and correct</constraint>
    <constraint>Do NOT change lib/etf_classifier.py -- it is deployed and live</constraint>
    <constraint>Do NOT change lambda_function.py -- WS1 is already deployed at partners-api-v1.7.0</constraint>
    <constraint>OpenAI key is 'openai-api-key' in AWS Secrets Manager -- do not hardcode</constraint>
    <constraint>Commit with --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;"</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      bd-securities table ACTIVE with 116 seeded items (shared-infra-v1.5.0).
      ETFClassifier live at partners-api-v1.7.0. No blockers.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">classify_bd_securities.py with real OpenAI implementation, committed to CLOUD</deliverable>
  </deliverables>
</task_order>
