<task_order>
  <metadata>
    <id>0.6.0_AE_PartnerETL-2026-04-15-bdpl-cnprcs-wp3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-15</date>
    <status>staged</status><!-- Flip to pending on BDPL_ASTDIM.W7 closure. AE may begin Phase 1 compiler pre-flight while staged. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W2</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 2)</ref>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (WP-3)</ref>
    <ref type="brief">org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-14_asset_dim_and_canonical_prices_refactor.md (§WP-3)</ref>
  </references>

  <objective>
    Backfill CUSIP into `silver/transactions/{date}.parquet` using BD's AssetDimTXNs_OpalCapital_Daily
    export as the authoritative asset-to-CUSIP lookup. Primary join key in downstream canonical-prices
    + FIFO replay becomes CUSIP, not ticker — required for WP-4 (holdings_lots CUSIP enrichment),
    WP-5 (canonical prices refactor), WP-9 (CUSIP-keyed FIFO replay).

    Pattern: mirror the existing silver/fees/ and silver/bd_assets/ runners. Input = BD asset dim
    (now live via BDPL_ASTDIM W1-W6, bd-v2.24.0). Output = enriched silver/transactions/
    with new `cusip` column, joined on `(date, asset_id)` → `(cusip)`.
  </objective>

  <wire_contract>
    silver/transactions/{date}.parquet gains column `cusip` (string, nullable for cash/synthetic rows).
    All existing columns preserved; no schema-breaking rename. Downstream gold scripts (A_03,
    holdings_lots, canonical_prices) can begin reading `cusip` once backfill lands; nullable column
    means no existing readers break.
  </wire_contract>

  <acceptance_criteria>
    1. silver/transactions/{date}.parquet carries `cusip` column populated for ≥95% of non-cash rows.
    2. Backfill covers full historical window (same range as silver/bd_assets.parquet — 3.19M rows).
    3. `silver/transactions` pipeline stands up in same pattern as silver/fees (EventBridge schedule, Lambda runner, SSM dispatch option).
    4. Null-CUSIP audit committed: documents which asset_ids fail the join and why (expected: cash, synthetic lots, pre-asset-dim rows).
    5. `comp-iam gaps` clean post-deploy.
    6. `bd-v2.X.Y` tag cut; Terraform 0-diff verified.
    7. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    8. MCP COMPLETE to COO with tag + CUSIP coverage %.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io silver/transactions</run>
        <expect>Existing I/O manifest; confirms current column set and downstream consumers.</expect>
        <if_mismatch>Pipeline identity changed; escalate to COO.</if_mismatch>
      </step>
      <step>
        <run>comp-iam service &lt;silver-transactions-lambda-name&gt;</run>
        <expect>Current IAM policy lists silver/transactions read/write + silver/bd_assets read. If bd_assets not present, Phase 1 gap — add in this PR.</expect>
        <if_mismatch>Policy gap detected: record in TO log, include policy diff in PR.</if_mismatch>
      </step>
      <step>
        <run>comp-blast silver/transactions</run>
        <expect>Downstream readers: A_03.positions_cube + FIFO replay consumer. Confirms blast radius for nullable `cusip` column addition.</expect>
        <if_mismatch>Unexpected reader — coordinate before backfill.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>terraform plan</run>
        <expect>0 diff or declared changes only (Lambda code bump, IAM policy diff).</expect>
        <if_mismatch>Investigate drift before apply.</if_mismatch>
      </step>
      <step>
        <run>comp-iam gaps</run>
        <expect>No new cross-reference gaps (CTO auto-rule Phase 2 hit — MANDATORY since iam.tf may change).</expect>
        <if_mismatch>Fix gaps before apply.</if_mismatch>
      </step>
      <step>
        <run>python -m py_compile on Lambda source; unit tests</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit + deploy">
      <step>
        <run>comp-pipescript deployed &lt;silver-transactions-lambda&gt;</run>
        <expect>MATCH (runner has latest source).</expect>
        <if_mismatch>Re-upload; coordinate if persistent.</if_mismatch>
      </step>
      <step>
        <run>Production backfill on full historical window (PROD UPLOAD MODE per Andrew 2026-04-15)</run>
        <expect>≥95% CUSIP coverage on non-cash rows; null-audit committed to diagnostics/.</expect>
        <if_mismatch>Investigate null-CUSIP cohort before signaling downstream DS.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="BDPL_ASTDIM.W7" status="verification-pending" description="silver/bd_assets must be running on scheduled EventBridge fire before WP-3 backfill can read it authoritatively"/>
  </dependencies>

  <next>
    WP-3 clears → DS WP-4 (holdings_lots CUSIP enrichment) and WP-5 (canonical prices CUSIP-primary)
    become actionable. Signal COO on tag cut + coverage confirmed.
  </next>
</task_order>
