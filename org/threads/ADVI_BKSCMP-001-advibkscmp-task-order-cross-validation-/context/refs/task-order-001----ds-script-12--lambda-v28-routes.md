<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-19-bkscmp-001-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-19</date>
    <status>pending</status>
    <project_code>ADVI_BKSCMP</project_code>
  </metadata>

  <objective>
    Write script 12 (`12_build_composition_artifacts.py`) to pre-compute per-class top-9
    holdings composition artifacts for firm (N1) and all advisors (L2), update
    `run_gold_layer.sh` to include it, and add two new S3-proxy Lambda routes
    (`handle_firm_composition`, `handle_advisor_composition`) to opal-partners-data v2.8.
    These changes unblock the ConsolidatedOverviewPanel holdings panel which currently
    renders empty at N1 and L2 because the composition endpoints return 404.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_BKSCMP_PRD.md (canonical schema §3, algorithm §WS1,
    Lambda changes §WS2, sequencing §5).

    Current state:
    - `handle_books_composition` (line 829 of lambda_function.py) handles ALL entity types
      via in-Lambda computation from parquet. For firm/advisor it either times out or errors.
    - Routing at line 1222: `elif action == 'composition': return handle_books_composition(...)`
      routes firm and advisor to the computation-based handler.
    - L3/L4 (relationship, account) composition works today via `handle_books_composition`
      — do NOT change that behavior.
    - Current Lambda version: 2.7 (deployed at partners-api-v1.4.0).
    - run_gold_layer.sh: both modes have `08b` immediately followed by `06b`.
      Incremental: line 114 (08b), line 115 (06b). Full: line 158 (08b), line 159 (06b).

    advisor_id sanitization canonical transform (ClientsTab.tsx:383):
      name.toLowerCase().trim().replace(/[^a-z0-9_]+/g, '_').replace(/^_+|_+$/g, '') || 'unknown'
    Python equivalent (must match exactly):
      advisor_id = re.sub(r'[^a-z0-9_]+', '_',
                          name.lower().strip()).strip('_')[:60] or 'unknown'
    This is the key cross-agent consistency requirement. Any deviation breaks the S3 key lookup.
  </context>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
      <file action="modify">data/black_diamond/scripts/gold/run_gold_layer.sh</file>
      <file action="modify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" workstream="WS1-script12">
      Write `data/black_diamond/scripts/gold/12_build_composition_artifacts.py`.

      Header comment (required):
        # Classification logic mirrored from 06b_build_client_mix_timeseries.py -- keep in sync
        # Do NOT import from 06b directly (numeric prefix prevents clean imports).

      Inline (copy verbatim from 06b): ETF_CLASSIFICATIONS, ASSET_NAME_TO_TICKER,
      _OPAL_ETF_OVERRIDES, and classify_series(). These are the classification lookup tables.

      Algorithm (per PRD §WS1):
      1. Discover latest holdings_lots parquet: list s3://opal-data-bd/holdings_lots/*.parquet,
         sort by name descending, take the first. Read with pandas. Filter is_open == True.
         If no file found: log ERROR, sys.exit(1).
      2. Apply _OPAL_ETF_OVERRIDES to fix null tickers for Opal/Pathfinder ETFs:
         for rows where ticker is null/NaN but asset_name matches a key in _OPAL_ETF_OVERRIDES,
         set ticker = _OPAL_ETF_OVERRIDES[asset_name].
      3. Add asset_class column: apply classify_series(row.ticker, row.asset_name) per row.
      4. Load rel_architect_lookup.parquet from s3://opal-data-bd/gold/views/rel_architect_lookup.parquet.
         Columns needed: relationship_id, architect (= resolved architect name).
         On any failure: log WARN, fall back to loading
         s3://opal-data-bd/gold/views/client_dimension.parquet, join on relationship_id,
         use primary_architect column, rename to architect. If that also fails: log ERROR, sys.exit(1).
      5. Merge lookup onto holdings by relationship_id (left join, keep all holdings).
      6. Compute firm composition (all rows) — see PRD §WS1 algorithm step 5 for the
         full sequence: total_market_value, class groups, per-class top-9, global top-9,
         global other, unclassified.
         Output schema: exactly as PRD §3 with scope = {"firm_id": "49financial"}.
         Pct conventions (critical — per PRD §3):
           mix[i].pct = class_mv / total_market_value
           mix[i].top_holdings[j].pct = holding_mv / class_mv  (NOT total_market_value)
           top_holdings[j].pct (root) = holding_mv / total_market_value
           other.pct (root) = root_other_mv / total_market_value
           mix[i].other.pct = class_other_mv / class_mv
         Write to: s3://opal-data-bd/gold/views/firm_composition.json
      7. Loop over unique architect values in the merged dataframe.
         For each architect, filter holdings to architect == that_value.
         Compute advisor_id using the canonical transform:
           import re
           advisor_id = re.sub(r'[^a-z0-9_]+', '_', architect.lower().strip()).strip('_')[:60] or 'unknown'
         Compute same composition structure as step 6 but scoped to that advisor.
         scope = {"advisor_id": advisor_id, "firm_id": "49financial"}
         If advisor has 0 open holdings after filter: skip (do not write).
         Write to: s3://opal-data-bd/gold/advisors/{advisor_id}/composition.json
      8. Print summary line:
           print(f'OK: firm_composition.json written. Advisors: {N} written, {M} skipped (empty book).')

      key field: ticker if non-null/non-empty, else re.sub(r'\s+', '_', asset_name.lower())[:40]
      label field: ticker if non-null/non-empty, else asset_name[:30]
    </requirement>

    <requirement id="2" workstream="WS1-run_gold_layer">
      Update `data/black_diamond/scripts/gold/run_gold_layer.sh`.

      In BOTH the incremental section (around line 114) and the full section (around line 158),
      insert script 12 AFTER 08b and BEFORE 06b:

      Incremental (insert between lines 114 and 115):
        run_script "$SCRIPTS_DIR/12_build_composition_artifacts.py"

      Full (insert between lines 158 and 159):
        run_script "$SCRIPTS_DIR/12_build_composition_artifacts.py"

      Script 12 takes no mode flags (runs the same in both modes).
      Do NOT move or change any other script position.
      Update the sequence comments at lines 11 and 16 (header comments) to include 12
      in the script list between 08b and 06b.
    </requirement>

    <requirement id="3" workstream="WS2-lambda-helpers">
      In opal-partners-data lambda_function.py, add two new helper functions AFTER the
      existing `cors_response` function (around line 106) and BEFORE `serve_s3_json`:

      A. `cors_response_nocache(status_code, body)` — exact code from PRD §WS2-A:
        Identical to cors_response but with Cache-Control: 'no-store, no-cache, must-revalidate'
        instead of the existing max-age header. Uses same DecimalEncoder.

      B. `serve_s3_json_nocache(bucket, key)` — PRD §WS2-B:
        Copy the body of the existing `serve_s3_json` function verbatim,
        replacing ALL calls to `cors_response(...)` with `cors_response_nocache(...)`.
        Do not change any S3 logic or error handling.

      These two functions are the only new helpers.
    </requirement>

    <requirement id="4" workstream="WS2-lambda-handlers">
      Add two new handler functions AFTER the existing `handle_advisor_mix_views` function
      (around line 1063) and BEFORE the `# Main Handler` section comment:

      C. `handle_firm_composition(bucket)` — PRD §WS2-C:
        return serve_s3_json_nocache(bucket, 'gold/views/firm_composition.json')

      D. `handle_advisor_composition(bucket, advisor_id)` — PRD §WS2-D:
        Validate: if not advisor_id or '/' in advisor_id or '..' in advisor_id:
          return cors_response_nocache(400, {'error': 'Invalid advisor_id'})
        return serve_s3_json_nocache(bucket, f'gold/advisors/{advisor_id}/composition.json')

      Add docstrings consistent with the existing handlers in the file.
    </requirement>

    <requirement id="5" workstream="WS2-lambda-routing">
      Update the routing block in `lambda_handler` at line 1222.

      Current (single branch handles ALL entity types):
        elif action == 'composition':
            return handle_books_composition(bucket, entity_type, entity_id)

      Replace with (firm/advisor get new S3-proxy handlers; relationship/account keep existing):
        elif action == 'composition' and entity_type == 'firm':
            return handle_firm_composition(bucket)
        elif action == 'composition' and entity_type == 'advisor':
            return handle_advisor_composition(bucket, entity_id)
        elif action == 'composition':
            return handle_books_composition(bucket, entity_type, entity_id)

      This preserves L3/L4 (relationship, account) behavior exactly. Only firm and advisor
      composition are redirected to the new S3-proxy handlers.

      IMPORTANT: the `advisor` composition routing must appear BEFORE the generic
      `elif action == 'composition':` fallback, matching the pattern used for timeseries.
    </requirement>

    <requirement id="6" workstream="WS2-lambda-version">
      Bump the Lambda version constant from 2.7 to 2.8.
      Add the two new routes to the API endpoint docstring at the top of the file:
        GET /api/scoped/partners/books/firm/all/composition?firmId=xxx
        GET /api/scoped/partners/books/advisor/{advisor_id}/composition?firmId=xxx
    </requirement>

    <requirement id="7" workstream="commit">
      Commit both WS1 files (script 12 + run_gold_layer.sh) in ONE commit:
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "feat(bd-gold): script 12 composition artifacts + run_gold_layer.sh update (ADVI_BKSCMP WS1)"

      Commit the Lambda changes (lambda_function.py) in a SEPARATE commit:
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "feat(opal-partners-data): firm+advisor composition routes v2.8 (ADVI_BKSCMP WS2)"

      Report both commit SHAs to COO. The Lambda commit SHA is the gate for DT (ADVI_BKSCMP.003).
      The script 12 + run_gold_layer.sh commit SHA is the gate for AE (ADVI_BKSCMP.004).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">script 12 exists at correct path; runs without import errors in Python 3.12</criterion>
    <criterion id="2">advisor_id sanitization in script 12 matches ClientsTab.tsx:383 exactly</criterion>
    <criterion id="3">pct conventions match PRD §3 table (per-class top_holdings pct / class_mv, not total)</criterion>
    <criterion id="4">run_gold_layer.sh incremental: 08b immediately followed by 12, then 06b (no other reordering)</criterion>
    <criterion id="5">run_gold_layer.sh full: same 12 insertion after 08b, before 06b</criterion>
    <criterion id="6">cors_response_nocache returns Cache-Control: no-store, no-cache, must-revalidate</criterion>
    <criterion id="7">serve_s3_json_nocache is a structural copy of serve_s3_json — only cors_response calls differ</criterion>
    <criterion id="8">Lambda routing: firm+composition → handle_firm_composition; advisor+composition → handle_advisor_composition; relationship/account+composition → handle_books_composition (unchanged)</criterion>
    <criterion id="9">Lambda version = 2.8</criterion>
    <criterion id="10">Two separate commits on CLOUD; SHAs reported to COO</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT import from 06b — inline the classification logic with the required header comment</constraint>
    <constraint>Do NOT change handle_books_composition — it must remain for L3/L4 (relationship, account)</constraint>
    <constraint>Do NOT use DuckDB — pandas only (confirmed present on EC2)</constraint>
    <constraint>advisor_id sanitization must match ClientsTab.tsx:383 exactly — any deviation breaks S3 key lookup</constraint>
    <constraint>All pct fields are 0–1 (not 0–100) — consistent with all other mix artifacts in this repo</constraint>
    <constraint>No emojis anywhere in code or commit messages (CLAUDE.md rule 13)</constraint>
    <constraint>commit to CLOUD parent repo only — no portal changes in this task order</constraint>
    <constraint>Do not modify any other script positions in run_gold_layer.sh</constraint>
    <constraint>If advisor produces 0 open holdings after filter: skip (do not write empty JSON)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      No upstream DS gates — script 12 reads from existing S3 artifacts (holdings_lots from 03,
      rel_architect_lookup from 08b). Both are confirmed present on S3.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">data/black_diamond/scripts/gold/12_build_composition_artifacts.py + run_gold_layer.sh (one commit)</deliverable>
    <deliverable type="commit">opal-partners-data lambda_function.py v2.8 (separate commit)</deliverable>
  </deliverables>
</task_order>
