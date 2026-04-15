<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-bdpl-cnprcs-wp11</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-15</date>
    <status>in_progress</status><!-- CODE COMPLETE 2026-04-15 (~D). Commit 864b6d7a pushed to origin/CLOUD; silver scripts on S3 (bd_price_update.py etag 72521f9a..., inject_scoped_overrides.py etag 13915b2c...). GAP FOUND + FIXED: morning canonical_prices rebuild at 09:29 ET wiped overrides without re-injection (Apr-06 incident pattern); ran inject_scoped_overrides.py --upload at 15:22 ET to backfill. canonical_prices.parquet (85.8MB, +5,064 rows) spot-checks PASS: BNP/WFC/NEWMONT @ derived NAVs with source=bd_txn_price. comp-validate canonical_prices exit 0 (SKIP: no config entry yet — flag to COO for gold_validate_config.yaml addition). 3-bond tactical TO marked complete per acceptance #5. Awaiting: 49F cohort re-run for AUA delta (~$24.3M expected) + comp-blast canonical_prices (Phase 3 post-commit). -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W0</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 0 item #2)</ref>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (WP-11)</ref>
    <ref type="brief">org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-14_asset_dim_and_canonical_prices_refactor.md (§WP-11)</ref>
    <ref type="brief">org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-15_post_presentation_master_summary.md (§2)</ref>
    <ref type="companion">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/3-bond-phantom-scoped-exceptions.md (tactical coded; this TO formalizes)</ref>
  </references>

  <objective>
    Formalize the tactical 3-bond scoped-exceptions blocklist (BNP/WFC/NEWMONT phantom fix) into
    the permanent `_SCOPED_PRICE_OVERRIDES` path so it survives the BDPL_CNPRCS canonical-prices
    refactor independently of WP-5 landing.

    Integrate into:
      - `data/black_diamond/scripts/gold/bd_price_update.py` → `_SCOPED_PRICE_OVERRIDES` constant
      - `data/black_diamond/scripts/gold/inject_scoped_overrides.py` → `_INCEPTION_DATES` constant

    Inception dates + unit prices (per DS brief §2):
      - BNP PARIBAS SA (CUSIP 05613L3H2): ticker BOND_BNP_05613L3H2, price 1.02, 2024-10-15
      - WELLS FARGO &amp; CO 4.15% 01/24/2029: ticker BOND_WFC_415_2029, price 0.95, ~2023-Q1
      - NEWMONT CORP 2.8% 10/01/2029: ticker BOND_NEM_28_2029, price 0.87, ~2023-Q2

    Persistent CUSIP-keyed hard override with `force_source='bd_txn_price'`. Orthogonal to
    `ticker_overrides.json` — this is a BLOCK, not a reroute.

    Eliminates ~$24.3M phantom 49F firmwide (23M BNP + 860K WFC + 595K NEWMONT).
  </objective>

  <wire_contract>
    canonical_prices ledger carries `price_quality='custodial_override'` for the three CUSIPs
    with `force_source` set. Downstream: bd_txn_price pins the value at inception price,
    multiplied by BD-txn face-value units — not Yahoo equity price × face-value units.
  </wire_contract>

  <acceptance_criteria>
    1. `_SCOPED_PRICE_OVERRIDES` and `_INCEPTION_DATES` constants grep-able in both scripts.
    2. `comp-pipescript postdeps build_canonical_prices` confirms inject_scoped_overrides.py runs after rebuild.
    3. Dry-run on 49F cohort: BNP + WFC + NEWMONT phantom valuations eliminated; total firmwide 49F alternatives AUA drops by ~$24.3M vs pre-fix baseline.
    4. `comp-validate canonical_prices --artifact /tmp/canonical_prices.parquet` exits 0.
    5. 3-bond tactical TO (`3-bond-phantom-scoped-exceptions.md`) marked complete by this one — WP-11 supersedes.
    6. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    7. MCP COMPLETE to COO with commit hash + 49F pre/post AUA delta.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>grep -n '_SCOPED_PRICE_OVERRIDES\|_INCEPTION_DATES' data/black_diamond/scripts/gold/bd_price_update.py data/black_diamond/scripts/gold/inject_scoped_overrides.py</run>
        <expect>Existing constants present; extend them with the 3 bond entries.</expect>
        <if_mismatch>If constants not found, add at module level with same naming convention.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript postdeps build_canonical_prices</run>
        <expect>BLOCKING post-step: inject_scoped_overrides.py; reason cites 2026-04-06 BNP incident ($22M phantom on Delaney account).</expect>
        <if_mismatch>If dep link broken, STOP and escalate — ordering must be intact to prevent phantom re-introduction.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/bd_price_update.py data/black_diamond/scripts/gold/inject_scoped_overrides.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>comp-validate canonical_prices --artifact /tmp/canonical_prices.parquet</run>
        <expect>Exit 0; BNP/WFC/NEWMONT CUSIPs emit price_quality='custodial_override' with force_source='bd_txn_price'.</expect>
        <if_mismatch>Iterate on the override logic.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast canonical_prices</run>
        <expect>Consumer set unchanged; downstream readers (A_03.positions_cube, holdings_lots, etc.) treat 'custodial_override' as valid quality tag.</expect>
        <if_mismatch>If new consumer or consumer breaks on quality tag, coordinate with COO before signaling.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency description="Andrew AUA-freeze thaw" status="pending" gate="thaw_signal"/>
  </dependencies>

  <next>
    On commit: run build_canonical_prices_v2 + inject_scoped_overrides in order. 49F nightly
    picks up the eliminated phantoms automatically. After 3 consecutive clean nightlies,
    close as Wave 0 item #2 success.
  </next>
</task_order>
