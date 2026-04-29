<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.DIAGFIX.012</id>
    <project>ADVI_INFLEC</project>
    <title>Orion daily positions MV refactor — kill TRN-as-price reconstruction; INF_B_00 becomes pass-through over silver/positions_mv</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>staged</status>
    <priority>high</priority>
    <estimated_effort>4-6h code + 150min one-shot 30-day backfill</estimated_effort>
  </metadata>

  <references>
    <ref type="parent_to">DIAGFIX.009-NEW (ds-holdings-pricing-strategy.md, filed 394c34606 by AE 0.6.1 2026-04-29)</ref>
    <ref type="phase1_verdict">DIAGFIX.009-NEW Phase 1 RAVC (DS 20260429T2320Z, commit 91da4d6a1) — VERDICT PATH A: existing endpoint serves arbitrary historical dates with full 58-col schema and asOfDate echoed; no new endpoint discovery needed; no Yahoo Finance fallback needed</ref>
    <ref type="endpoint">GET /api/v1/Portfolio/Clients/{clientId}/Assets/{MM-DD-YYYY}?$top=50000&amp;includeCostBasis=false</ref>
    <ref type="probe_artifact">s3://opal-data-inf/bronze/orion-api/probe/probe_diagfix009_findings.json</ref>
    <ref type="andrew_directive">Andrew 2026-04-29: "if they have time series that accounts for nav value on a daily basis then awesome lets grab it right from the source. if they do not have that, then the simple mechanism is what we do for 49financial whereby there are type A B and C assets" — Path A confirmed available, Path B no longer needed</ref>
    <ref type="downstream_deltas">DIAGFIX.010 firm-level: $190.5M holdings vs $182.55M aum_snapshot vs $197.86M Orion bronze (~$7-15M sourcing deltas). DIAGFIX.011 advisor-level: Brandenburg $16.15M accounts_v2 vs $14.62M composition.json (same-pattern $1.5M delta). Both resolve at source after this refactor.</ref>
  </references>

  <context>
    DIAGFIX.009-NEW Phase 1 confirmed Orion's `/Portfolio/Clients/{cid}/Assets/{date}` endpoint
    serves real per-day position MV at any historical date — not period-end carry-forward, not
    smoothed, not synthesized. Same endpoint already used for `silver/api_dims/assets_v2`.
    Different `currentValue` totals across the 5 dates probed (today + 1d + 3d + 7d + 30d back)
    confirm Orion is serving real intraday/intraperiod MV, not artifact.

    This makes the entire TRN-as-price-source architecture in INF_B_00 unnecessary. The current
    flow reconstructs `market_value = units × nav_price` where `nav_price` comes from Orion TRN
    rows using "last seen wins" — corrupted by non-trade events (advisory fee debits, journal
    entries, income distributions with nav_price=0) and stale by definition between trades. Even
    after the nav_price guard fix shipped earlier today (`if nav > 0: update`), the price used
    is the LAST TRADE price, which may be days or weeks stale.

    The fix: replace position-level MV reconstruction with direct lookup from a new silver dim
    populated by daily Orion API pulls. INF_B_00 becomes a thin pass-through. Downstream
    timeseries / concentration_risk / composition / advisor-level views all auto-correct.

    SCOPE BOUNDARY: This TO refactors holdings pricing only. Asset classification (DIAGFIX.010,
    Orion-native productCategory + assetClass) stays in INF_I_D03. Advisor attribution
    (DIAGFIX.011, accounts_v2 rep_id JOIN) stays in convert_orion_api_to_silver.py +
    INF_I_D03 advisor_key override. This TO sits below those two — they continue working as-is.

    The aggregate AUA views (donut totals, leaderboard, partner_analytics) already source from
    `aum_snapshot.managed_value` and remain authoritative; this TO does NOT modify aum_snapshot
    flow. This TO ONLY affects position-level dollars and downstream views that consume them.
  </context>

  <scope>
    PHASE 2 — bronze pull script:
    Create `data/orion/manual_api/pull_inflection_positions_daily.py`. MUST begin with
    `from __future__ import annotations`.

    Pattern after existing `pull_inflection_assets_v2.py`. New iteration shape:
      for date in date_range:
        for clientId in inflection_clientIds:
          GET /api/v1/Portfolio/Clients/{clientId}/Assets/{MM-DD-YYYY}?$top=50000&includeCostBasis=false
          write to bronze/orion-api-v2/{date}/positions/client_{clientId}.json (or batch into one file per date)

    CLI flags:
      --date YYYY-MM-DD            single-date mode (default: today)
      --backfill-days N            iterate today, today-1, ..., today-(N-1)
      --start YYYY-MM-DD --end YYYY-MM-DD   explicit date range
      --upload-bronze              S3 upload toggle
      --dry-run                    print plan without API calls

    Behavior requirements:
      - Pagination: $top=50000 covers all cases (HAR sample showed 53 assets/client max)
      - Retry: 429/5xx exponential backoff (max 3 retries; same retry/backoff helper as assets_v2)
      - Rate limiting: 100ms sleep between calls (proven safe in DIAGFIX.010)
      - Output: one parquet file per date at bronze/orion-api-v2/{date}/positions.parquet (preferred)
        OR JSON-per-clientId at bronze/orion-api-v2/{date}/positions/client_{cid}.json (acceptable)
      - Capture ALL 58 columns. Do not pre-filter.

    Test: smoke pull --backfill-days 2 (today + yesterday) for 5-10 clientIds before full run.

    PHASE 3 — silver dim builder:
    Extend `data/orion/scripts/silver/convert_orion_api_to_silver.py` with `build_positions_mv()`
    function (or `build_positions_mv_v2()` if you want versioning).

    Output: `silver/positions_mv/snapshot_date={date}/data.parquet`
    Schema: one row per (account_id, ticker, date), all 58 source cols typed appropriately:
      - account_id: Int64
      - ticker: string
      - snapshot_date: date32 (partition column)
      - current_value: float64 (= EndingMV)
      - current_shares: float64
      - current_price: float64 (= current_value / current_shares; verify Orion's currentPrice if present)
      - cost_basis: float64 (when includeCostBasis flag set)
      - registration_type, custodian, model_name, asset_class, product_category, etc. — all 58 cols

    Dim is partitioned by snapshot_date so historical lookback is cheap.

    PHASE 4 — INF_B_00 refactor:
    Replace `_load_trn()` + `_apply_nav_price()` + `_apply_units_x_price()` reconstruction with:
      _load_positions_mv(snapshot_date) → silver/positions_mv/snapshot_date={date}/data.parquet
      _join_holdings_with_positions_mv() → JOIN on (account_id, ticker, snapshot_date)
      market_value = positions_mv.current_value (DIRECT, no reconstruction)

    DELETE dead code:
      - nav_price guard helpers (now dead — no nav_price column needed)
      - "last seen wins" lookup (now dead)
      - any TRN-row-as-price processing

    KEEP TRN feed for what it's actually for: trade events feeding lots, FIFO basis, holdings
    lifecycle (open/close dates, NMNC/NMEC). TRN is a transaction log, not a price source.

    Dependency note: INF_B_00 currently runs early in the chain (B-tier). Adding silver/positions_mv
    as a dependency is straightforward; CHAIN_FULL / CHAIN_INCREMENTAL ordering update needed
    (AE 0.6.1 cross-domain).

    PHASE 5 — re-run + validate:
      A. Position-level: verify market_value matches Orion's currentValue per (account, ticker)
         within rounding tolerance (no drift between consecutive days unless trades happened).
      B. Firm-level: post-chain holdings sum should match Orion API total ($197.86M today)
         within $1M (intra-day delta acceptable). The $7-15M deltas observed in DIAGFIX.010
         and DIAGFIX.011 should resolve.
      C. Advisor-level: Brandenburg's composition.json total should land near $16.15M
         (his accounts_v2 attribution). Same alignment for Lee, Scanlan, IWM books.
      D. Downstream views: timeseries, concentration_risk, mix_summary should auto-update
         via INF_B_00 → INF_I_D03 → INF_I_D02d cascade.

    PHASE 6 — RAVC4 close to COO + AE 0.6.1.

    Backfill window: 30 days from today (covers W4.13b chain re-run cycle + a buffer).
    Forward maintenance: extend chain to call positions_mv pull daily (AE 0.6.1 chain registration).
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_B_00</run>
        <expect>Document current READS (silver/holdings, silver/trn, etc.) + WRITES (gold/canonical/holdings_*.parquet). New READ added: silver/positions_mv. Same registry-gap precedent as DIAGFIX.010 / .011 if Orion scripts not in BD-pipeline graph — SKIP acceptable, document gap.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/manual_api/pull_inflection_positions_daily.py
                                       data/orion/scripts/silver/convert_orion_api_to_silver.py
                                       data/orion/scripts/gold/INF_B_00.holdings.py</run>
        <expect>Exit 0. py_compile + AST + ruff all pass on every file.</expect>
        <if_mismatch>STOP. Fix gate failures first.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after S3 upload">
      <step>
        <run>MD5 MATCH verification for each uploaded script (registry gap precedent)</run>
        <expect>Local md5 == S3 ETag for each.</expect>
        <if_mismatch>Re-upload. Do not dispatch chain re-run until MATCH.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      bronze/orion-api-v2/{date}/positions.parquet (or .json) exists for every date in the
      30-day backfill window. ~8,880 rows × 58 cols expected per day for full 296-clientId pull.
      Evidence: aws s3 ls + python parse showing column count + row count for sample dates.
    </criterion>
    <criterion id="2">
      silver/positions_mv/snapshot_date={date}/data.parquet exists for the 30-day window.
      One row per (account_id, ticker, snapshot_date). asset_class + product_category 100% non-null.
      Evidence: python parse + dtypes printout + partition listing.
    </criterion>
    <criterion id="3">
      INF_B_00 refactored — TRN-as-price reconstruction code DELETED. No imports of nav_price guard
      helpers remain. Diff shows net code reduction. INF_B_00 becomes a JOIN over silver/positions_mv.
      Evidence: diff in commit + grep showing no `nav_price` references in INF_B_00 (TRN feed retained
      for trade-events / FIFO / lifecycle as documented).
    </criterion>
    <criterion id="4">
      Post-refactor chain re-run: `gold/canonical/holdings_{date}.parquet` market_value matches
      `silver/positions_mv` `current_value` per (account_id, ticker) within rounding tolerance.
      Evidence: python diff script comparing per-row market_value across both artifacts.
    </criterion>
    <criterion id="5">
      Firm-level holdings sum reconciles to Orion API total ($197.86M today) within $1M intra-day delta.
      Brandenburg's composition.json total reconciles to his accounts_v2 attribution ($16.15M today)
      within $0.5M. Evidence: comparison table in RAVC.
    </criterion>
    <criterion id="6">
      ds-commit-gate.sh exit 0 on all modified scripts. S3 deploy MATCH for each.
    </criterion>
    <criterion id="7">
      RAVC to 2.0.0_SA_COO + cc 0.6.1_AE_PartnerETL: commit hashes, S3 deploy MATCH, before/after
      reconciliation table (firm + Brandenburg + 1-2 sample clients), downstream view spot-checks
      (timeseries non-flat, concentration_risk reasonable, mix_summary unchanged from DIAGFIX.010
      since classification didn't change).
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" status="complete">DIAGFIX.009-NEW Phase 1 — endpoint discovered, schema documented, probe artifacts on S3</dependency>
    <dependency agent="0.6.1_AE_PartnerETL" status="will_engage">
      Chain registration of new bronze pull + extended silver builder in `orion-gold-dispatch.sh`
      CATALOG / CHAIN_FULL / CHAIN_INCREMENTAL after Phase 2+3 land. New ordering:
      pull_inflection_positions_daily → convert_orion_api_to_silver --dim positions_mv → INF_B_00
      → INF_I_D03 → INF_I_D02d. DS RAVCs to AE for registration after S3 upload.
    </dependency>
    <dependency agent="0.6.1_AE_PartnerETL" status="continuing">
      Earlier-queued chain registration for DIAGFIX.011 scripts (`pull_inflection_representatives.py`
      + new dim names representatives + household_rep_mapping) is still pending. This TO adds a
      third registration; AE can batch all three in a single dispatch.sh update.
    </dependency>
  </dependencies>

  <cross_domain_coordination>
    <coordination>
      AE 0.6.1: register new bronze pull script + new silver dim name (positions_mv) +
      INF_B_00 dependency update in orion-gold-dispatch.sh. Same pattern as DIAGFIX.010 +
      DIAGFIX.011 registrations. DS RAVCs with script paths and dependency ordering.
    </coordination>
    <coordination>
      DE: no immediate action. Position-level views (concentration_risk, top_holdings,
      composition mix) will auto-update on next portal cache cycle once new gold artifacts land.
      Numbers will move (correctly) — flag to DE for visual smoke-check post-deploy.
    </coordination>
    <coordination>
      AE 0.7.0: separately on the JWT pipeline structural fix (Terraform lift of inf-jwt-trigger-kms
      IAM policy + Option A wiring fix for SSM doc Mode parameter) — this TO assumes the JWT auto-cron
      will work tomorrow morning OR DS uses the manual SSM workaround. If JWT is stale at execution
      time, DS holds + COO + AE 0.7.0 unblock per existing path.
    </coordination>
  </cross_domain_coordination>

  <commit_identity>
    Phase 2 (bronze pull):
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
      -m "feat(ADVI_INFLEC.DIAGFIX.012 Phase 2): Orion daily positions MV bronze pull" \
      -- data/orion/manual_api/pull_inflection_positions_daily.py

    Phase 3 (silver builder):
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
      -m "feat(ADVI_INFLEC.DIAGFIX.012 Phase 3): silver positions_mv dim builder" \
      -- data/orion/scripts/silver/convert_orion_api_to_silver.py

    Phase 4 (INF_B_00 refactor):
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
      -m "refactor(ADVI_INFLEC.DIAGFIX.012 Phase 4): INF_B_00 — kill TRN-as-price reconstruction; pass-through over silver/positions_mv" \
      -- data/orion/scripts/gold/INF_B_00.holdings.py
  </commit_identity>

  <notes>
    DS offered to draft a brief INF_B_00 refactor design doc tonight as an optional preparatory
    artifact (RAVC ACK 20260429T2326Z). If Andrew picks Option B (stage til morning), the design
    doc is welcome but not required — Phase 4 design space is small and well-bounded.

    If Andrew picks Option A (GO tonight), expect Phase 2-3 ship tonight + Phase 4 ship + 30-day
    backfill kicks off; Phase 5 validation lands tomorrow morning.
  </notes>
</task_order>
