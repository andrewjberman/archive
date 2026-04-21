<task_order>
  <metadata>
    <id>ADVI_ROLLUP.CP-DS1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-17</date>
    <status>complete</status>
    <closeout date="2026-04-21" resolved_by="joint CTO+COO audit" cto_decision="20260421T141326Z Option A">
      CANCELLED-AS-PENDING closeout 2026-04-21 — code shipped 2026-04-17 across 8 commits (7e57576f/c693d5a3/d39c4dff/cd00ff2c/c4ebde9a/f5f19e77/1db831aa/ec2c1efc), validated Run 11 $3.587B→$1.758B per CTO session 32. HLOT2 2026-04-21 `5f5d0319` proceeded on same B_01.holdings_lots.py without reverting CP-DS1 gates = de-facto acceptance after 4-day no-objection window. Follow-up items moved to ADVI_ROLLUP blocking as standalone (asset_class join hardening TO; Top Positions 'Opal models only' filter TO; cap-timing-rule disposition if Andrew ever wants explicit). Reconciled by joint CTO+COO audit 2026-04-21.
    </closeout>
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P0 — permanent fix for chronic B_01 SAFETY HALT</priority>
    <supersedes>BDPL_CNPRCS.WP-4, BDPL_CNPRCS.WP-9 (30-day dry-run replaced by single validation run per Andrew 2026-04-17)</supersedes>
    <guardrail_override>30-day dry-run requirement on WP-9 lifted by Andrew 2026-04-17. Single nightly validation run is sufficient gate.</guardrail_override>
  </metadata>

  <context>
    B_01.holdings_lots.py _apply_rps_lot_corrections (L1169) keys the FIFO lot match on
    (account_id, asset_name). For ~261 accounts, asset_name has drifted (fund renames, share
    class changes) so B_01 cannot find the matching RPS entry. It force-closes those lots,
    producing a >200-account cohort that trips the SAFETY HALT every nightly run.

    Fix: key on (account_id, cusip) instead of (account_id, asset_name). CUSIPs are stable
    identifiers. The ~261 false-mismatch accounts will match correctly and no longer be
    force-closed. The chronic halt disappears.

    Andrew's completion target for the full gold chain: ~$1.65B firm AUA (range $1.6B-$1.7B),
    all accounts mapped. This cutover is the prerequisite for accurate nightly gold output.
  </context>

  <objective>
    1. Plumb CUSIP through B_01.holdings_lots.py (WP-4 scope): join lots to silver/bd_assets
       on asset_id to add cusip column to the lot stack.
    2. Modify _apply_rps_lot_corrections to key on (account_id, cusip) where cusip is non-null,
       with (account_id, asset_name) fallback for null-CUSIP lots.
    3. Confirm RPS records carry CUSIP (gate from ~A audit — see council research below).
       If RPS has no CUSIP: build a CUSIP lookup from silver/bd_assets and apply it to RPS
       records before the match. ~A will advise the correct strategy.
    4. Run a single nightly validation on bd-gold-qa-runner with BD_FORCE_CLOSE_OVERRIDE=0
       (no override). Gate: force-close cohort < 50 and chain completes clean.
  </objective>

  <council_research_gates>
    Before writing any code, collect answers from the parallel council research dispatched
    by COO on 2026-04-17:

    ~A (RPS schema audit): Does silver/rps/ or the raw RPS source carry a cusip column?
      - YES: proceed with direct (account_id, cusip) keying in _apply_rps_lot_corrections.
      - NO: DS must also CUSIP-enrich the RPS side via bd_assets lookup before the match.
        ~A will specify the join key available in RPS data.

    ~B (acceptance target): What is the expected post-cutover force-close cohort size?
      Target is < 50 accounts (WP-9 residual: genuine data-quality accounts, not name-drift).
      ~B will confirm the number.

    ~C (coverage baseline): Current silver/transactions CUSIP coverage before CP-AE1.
      Informs fallback strategy sizing (how many rows will use asset_name fallback).
  </council_research_gates>

  <tasks>
    Phase 1 — Enrichment (after CP-AE1 COMPLETE + council answers):
      1. In B_01, at the point where lot stacks are built from silver/transactions,
         join on asset_id to silver/bd_assets.parquet to populate `cusip` on each lot row.
         Fallback: if asset_id not found in bd_assets, cusip remains null.
      2. Pass `cusip` column through to _apply_rps_lot_corrections.

    Phase 2 — RPS key cutover:
      3. In _apply_rps_lot_corrections:
         - Build a CUSIP-keyed merge: match FIFO lots to RPS entries on (account_id, cusip)
           where lot.cusip IS NOT NULL and RPS record has CUSIP (or lookup applied).
         - For remaining unmatched lots (null CUSIP or RPS no-CUSIP): fall back to
           (account_id, asset_name) match exactly as today.
         - Log: accounts matched via CUSIP path vs asset_name fallback path.
      4. Update B_02.canonical_lots.py to carry cusip column downstream (WP-4 scope).

    Phase 3 — Validation:
      5. Run on bd-gold-qa-runner:
         python B_01.holdings_lots.py --date 2026-04-15 (or latest silver/allocations date)
         No BD_FORCE_CLOSE_OVERRIDE. Confirm:
           - force-close cohort < 50
           - SAFETY HALT does not fire
           - lot output row count within 5% of last clean run
           - No new ERROR lines
      6. If validation passes: DT commits + pushes. AE uploads to S3 + triggers PROD.
      7. If cohort >= 50 but < 200 and halt does not fire: PASS (threshold not exceeded).
         If halt fires (cohort >= 200): escalate to CTO with ~A + ~B data — structural issue
         beyond name-drift.
  </tasks>

  <acceptance_criteria>
    1. _apply_rps_lot_corrections uses (account_id, cusip) as primary key with asset_name fallback.
    2. B_01 lot stack carries `cusip` column (null-safe).
    3. B_02.canonical_lots carries `cusip` downstream.
    4. QA validation run: SAFETY HALT does not fire. Diagnostic artifacts (DS-DIAG 41629ee1) confirm:
         (a) rps_force_close_alerts/{date}.parquet row count < 200 (halt-clearing gate)
         (b) rps_force_close_resolved/{date}.parquet row count < 50 (clean acceptance gate)
       Population A (472 chronic-with-open-lots) is exempt from both artifacts via dryrun_mode=True.
       Their AUA gap is addressed by CP-VETO-AUTH + CP-MAP in parallel (separate TOs).
    5. CUSIP-path vs fallback-path counts logged per run.
    6. comp-validate exits 0 on QA output.
    7. comp-pipescript deployed MATCH confirmed before PROD trigger.
    8. MCP COMPLETE to COO with: commit hash, QA force-close count, CUSIP-path %, S3 MATCH status.
  </acceptance_criteria>

  <completion_target>
    Post-cutover nightly gold chain must produce:
    - Firm non-cash AUA within 2% of silver/allocations/2026-04-15 non-cash subtotal:
        Target: $1,660,325,206.81  |  2% band: $1,626,919,000 – $1,693,731,000
        (B_01 does NOT emit cash lots; cash $34,323,539 is WP-5 scope, out of this TO)
        Headline silver/allocations/2026-04-15 total: $1,694,648,746 (6,543 accounts)
    - Force-close cohort on QA run: PASS <50, WARN 50-100, FAIL >100
        (Point estimate 50-95 post-cutover; ~155-210 name-drift false-positives removed by CUSIP fix;
         ~40-80 txn-orphan FIFO residual remain — separate fix lane)
    - All 6,543 accounts mapped — no phantom cohort, no unexplained lot voids.
    - BD_FORCE_CLOSE_OVERRIDE=0 in nightly gold_dispatch.sh (override removed permanently).
    Source: ~B deliverable cp_ds1_acceptance_targets_2026-04-17.md, observed S3 2026-04-17.
  </completion_target>

  <compiler_tools_mandate>
    Phase 1 (before write):
      comp-pipescript io B_01.holdings_lots.py — confirm current I/O, column reads.
      comp-blast B_01.holdings_lots — blast radius of adding cusip column.
      comp-pipescript overlap B_01.holdings_lots B_02.canonical_lots — confirm shared artifacts.
    Phase 2 (before commit):
      python -m py_compile B_01.holdings_lots.py B_02.canonical_lots.py.
      comp-pipescript deployed B_01.holdings_lots.py — MATCH required.
    Phase 3 (after QA validation):
      comp-validate B_01 --artifact /tmp/holdings_lots_{date}.parquet — must exit 0.
  </compiler_tools_mandate>

  <dependencies>
    <dependency task="ADVI_ROLLUP.CP-AE1" agent="0.6.0_AE_PartnerETL" status="active"
      description="silver/transactions must carry cusip column before B_01 enrichment."/>
    <dependency task="ADVI_ROLLUP.CP-W4" agent="0.4.0_DS_ClientPlatform" status="active"
      description="silver/bd_assets.parquet blend verified — CUSIP source trustworthy."/>
    <dependency task="council-research-~A" agent="0.4.0_DS_ClientPlatform~A" status="dispatched"
      description="RPS schema audit — does silver/rps/ carry cusip? Determines join strategy."/>
  </dependencies>

  <cto_design_flags date="2026-04-17">
    Appended per CTO pre-flight (T045048Z):
    1. RPS ticker whitespace — .str.strip() on ALL RPS join keys (cusip + ticker) before any match.
    2. bd_assets_dim has NULL cusip for ~9.5% of asset_ids (cash, MMKT, synthetic, uncatalogued).
       DS must: fallback to (account_id, asset_name) when cusip is null on EITHER side of the match.
    3. bd_assets_dim.alternative_identifier may carry aliased tickers — check if ticker-fallback
       join needs it; probably not needed if asset_name fallback covers the null-CUSIP cohort cleanly.
    4. WP-10b recon harness (cff234b5) should flag asset_ids not yet in bd_assets_dim post-DS1.
       Monitoring gate, not blocking. Wire in nightly after DS1 ships.
    5. cusip_to_name bridge (built from silver/unrealized) becomes dead code post-DS1 — remove it.
       The 8eda12a3 CUSIP exemption also becomes a no-op — remove.
    6. Log CUSIP-path vs asset_name-fallback match counts per B_01 run for observability.
  </cto_design_flags>

  <next>
    CP-DS1 validation pass -> DT commit/push -> AE S3 upload -> PROD run -> ADVI_ROLLUP
    gold chain completes at silver/allocations/2026-04-15 total_aua. BD_FORCE_CLOSE_OVERRIDE
    removed from gold_dispatch.sh permanently.
  </next>
</task_order>
