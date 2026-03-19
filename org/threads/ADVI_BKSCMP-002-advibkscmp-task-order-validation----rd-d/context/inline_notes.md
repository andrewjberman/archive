ADVI_BKSCMP task order cross-validation for RD, DT, and AE. DS already validated in ADVI_BKSCMP-001 turn 1. All source file facts needed for verification are pre-injected below -- no tool calls are needed or expected. Each agent reads the pre-injected facts, verifies their task order requirements, and outputs CONFIRMED or DISCREPANCY per requirement.

=== PRE-INJECTED FACTS FOR RD (0.4.2_RD_AdvisorIntelligence) ===

Source: portal/src/pages/AdvisorIntelligence/types.ts (lines 1265-1291, read 2026-03-19)

CURRENT MixItem interface (lines 1265-1270):
  export interface MixItem {
    asset_class: string  // 'equity' | 'fixed_income' | 'hedge' | 'cash' | 'other'
    label: string
    market_value: number
    pct: number
  }
  -- NO top_holdings field. NO other field. Task order req 1 adds both as optional.

CURRENT BooksCompositionResponse interface (lines 1280-1291):
  export interface BooksCompositionResponse {
    generated_at: string
    data_as_of: string
    scope: { relationship_id?: string; account_id?: string }
    mix: MixItem[]
    concentration: {
      top_n: number
      items: ConcentrationItem[]
      other: { market_value: number; pct: number }
    }
    unclassified: { count: number; market_value: number }
  }
  -- scope has NO advisor_id, NO firm_id. NO root top_holdings. NO root other. Task order req 1 adds all four.

ConcentrationItem (lines 1272-1278) -- unchanged by this task order:
  export interface ConcentrationItem {
    key: string
    label: string
    asset_class: string
    market_value: number
    pct: number
  }

Source: portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx (lines 875-884 and 1039-1073, read 2026-03-19)

CURRENT holdings derivation block (lines 875-884) -- exact code task order req 2 replaces:
  const allItems = composition?.concentration.items ?? []
  const filteredItems = selectedAssetClass
    ? allItems.filter(it => it.asset_class === selectedAssetClass)
    : allItems
  const MAX_ITEMS = 9
  const cappedItems = filteredItems.slice(0, MAX_ITEMS)
  const showOther = !selectedAssetClass && composition && composition.concentration.other.pct > 0
  const showFilteredOther = Boolean(selectedAssetClass && filteredItems.length > MAX_ITEMS)
  const maxPct = cappedItems.length > 0 ? cappedItems[0].pct : 1

CURRENT showFilteredOther render block (lines 1039-1054) -- req 3 removes this:
  {showFilteredOther && (
    <div className="flex items-center gap-2.5">
      ...(uses filteredItems.slice(MAX_ITEMS).reduce for pct)...
    </div>
  )}

CURRENT showOther render block (lines 1055-1068) -- req 3 replaces with unified otherEntry block:
  {showOther && composition && (
    <div className="flex items-center gap-2.5">
      ...(uses composition.concentration.other.pct)...
    </div>
  )}

CURRENT empty state (line 1073):
  {!composition ? 'Loading...' : allItems.length === 0 ? 'No holdings data at this level' : 'No holdings for selected class'}
  -- req 4 changes the middle condition from `allItems.length === 0` to `!hasPreAggregated && composition.concentration.items.length === 0`

Note on line numbers: The component function ConsolidatedOverviewPanel starts around line 860. Lines 875-884 are confirmed as the holdings derivation block. All line numbers verified 2026-03-19.

=== PRE-INJECTED FACTS FOR DT (0.4.0_DT_ClientPlatform) ===

Source: infra/aws/lambda/ci/lambda-source-map.json (read 2026-03-19)

CURRENT opal-partners-data entry:
  "opal-partners-data": {
    "source_dir": "infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data",
    "files": ["lambda_function.py", "etf_classification.py"],
    "tf_file": "infra/aws/terraform/partners-api/lambdas.tf",
    "tf_resource": "module.opal_partners_data.aws_lambda_function.this",
    "artifact_s3_key": "partners-api/opal-partners-data.zip",
    "artifact_sha256": "z3hy2abK6/Ks5049Mbu6yWvwGq9FY6Kz1hl6Her08Jc=",
    "last_deployed_commit": "745c44c803b8fc8c1658023c18194b60fecf5d65",
    "last_deployed_at": "2026-03-18T16:13:50Z"
  }
  -- Entry exists. tf_resource and artifact_s3_key are present. Req 3 updates artifact_sha256 after upload.

Source: infra/aws/terraform/partners-api/CHANGELOG.json (read 2026-03-19)
  Latest deployed version: partners-api-v1.4.0
  Previous: partners-api-v1.1.0
  -- Confirmed: partners-api-v1.5.0 is the correct next tag (req 6).

Terraform directory: infra/aws/terraform/partners-api/ -- confirmed to exist (lambdas.tf present).

record-terraform-deploy.sh: infra/aws/lambda/ci/record-terraform-deploy.sh -- confirmed present.

=== PRE-INJECTED FACTS FOR AE (0.6.0_AE_PartnerETL) ===

Source: data/black_diamond/scripts/gold/run_gold_layer.sh (injected in full, read 2026-03-19)

Incremental invocation (line 164): MODE is set via first arg. Run as: ./run_gold_layer.sh --incremental
  -- Req 4 command './run_gold_layer.sh --incremental' matches the script's mode parsing.

S3 sync behavior (line 71):
  aws s3 sync s3://${S3_BUCKET}/code/gold/ "$SCRIPTS_DIR/" --exclude "archive/*" --quiet
  -- ALL .py scripts in s3://opal-data-bd/code/gold/ are automatically pulled to SCRIPTS_DIR at startup.
  -- Script 12 (12_build_composition_artifacts.py) will be pulled automatically after AE uploads it to S3.
  -- S3_BUCKET = opal-data-bd (set in the script header).

run_gold_layer.sh itself is NOT in the gold/ prefix:
  -- It lives at s3://opal-data-bd/code/ (top level), not s3://opal-data-bd/code/gold/
  -- Req 3 says: aws s3 cp s3://opal-data-bd/code/run_gold_layer.sh ~/bd-gold/run_gold_layer.sh
  -- This is correct -- it must be re-pulled separately as the sync only covers gold/

Upload paths (req 2):
  Script 12: s3://opal-data-bd/code/gold/12_build_composition_artifacts.py  -- correct (in gold/ prefix, auto-pulled)
  run_gold_layer.sh: s3://opal-data-bd/code/run_gold_layer.sh  -- correct (top level, manual re-pull)

Source: infra/aws/ec2/EC2_MANIFEST.json (read 2026-03-19)

bd-gold-layer-runner entry exists:
  instance_id: i-01003b035d2988dfb
  _s3_gold: s3://opal-data-bd/code/gold/
  deployed_commit: 8d0546634d8aa807dda7b7f56b29931deab42e39
  deployed_at: 2026-03-18T13:52:07Z
  -- Entry is present and has the correct structure. Req 6 adds a new deployment record to this entry.
  -- Format: update deployed_commit, deployed_at, deployed_by fields for the script 12 + run_gold_layer.sh upload.
