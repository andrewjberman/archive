<task_order>
  <metadata>
    <id>ADVI_STAUDT.HLOT2b</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <co_adjudicator>1.0.0_SA_CTO (Patch A 73% partial threshold — separate adjudication)</co_adjudicator>
    <date>2026-04-21</date>
    <status>complete</status><!-- Closed 2026-04-22 by 0.4.0_DS_ClientPlatform~B. Commit 74dbad2b (2026-04-21T14:51Z). S3 MATCH confirmed. Chain 2026-04-22 16:27-17:25Z: HLOT2 AUTHORITATIVE RE-OPEN PASS — 79,704/85,156 rows ticker→cusip enriched; 22,148 synth lots / 3,269 accts / MV=$220,793,554; tier1_unrl=21,426, tier2_canon=722; silent_close=7,631, overlap_topup=14,517. Patch A: 4,046 CA_SELL→CA_BUY reclassifications. SSM 87227091 (2026-04-21 --chain full): Success (exit 0). CTO RAVC3 (20260422T202650Z): Patch A 73% PASS; HLOT2b CLOSED on --from B_01 chain; HLOT2 parent holds for nightly 23:00Z. -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P1 — fix-forward on HLOT2 Patch B 100% miss. B_01 bails when canonical/holdings lacks `cusip`; per-day reopen (both Tier 1 + Tier 2) skipped. Ticker-keyed `bd_assets_dim` merge closes the gap. Expected Tier 1 recovery: ~$102.7M split silent/overlap across IEFA+SPYM+IDVZ+IEMG+SPHY.</priority>
    <sla>~2h end-to-end: fix commit → S3 upload → qa-runner re-dispatch `--chain full` (with D-cascade this time) → Patch B attribution re-validation</sla>
    <decision_authority>Andrew 2026-04-21 chat ("you have to do a join to the asset table to get cusip, ask COO about it theyll understand") + COO adjudication MCP `20260421T182813Z` confirming `silver/bd_assets_dim.parquet` ticker→cusip bridge (all 5 HLOT2 targets verified present with valid CUSIPs).</decision_authority>
  </metadata>

  <references>
    <ref type="fork_mcp">20260421T182408Z — DS URGENT FORK MCP identifying Patch B 100% miss + root cause at B_01 L1112-1116 `_build_authoritative_reopen_lots`</ref>
    <ref type="adjudication">20260421T182813Z — COO adjudication: bd_assets_dim on ticker confirmed, all 5 HLOT2 Patch B Tier 1 targets (IEFA=46432F842, SPYM=78464A854, IDVZ=210322707, IEMG=46434G103, SPHY=78468R606) present in dim</ref>
    <ref type="parent_to">ADVI_STAUDT.HLOT2 — original pending TO (this is a fix-forward; parent HLOT2 RAVC4 gates on HLOT2b close + Patch A threshold call)</ref>
    <ref type="parent_commit">5f5d0319 — original HLOT2 B_01 dual-patch commit (Patch A + Patch B code). HLOT2b patches the Patch B path only; Patch A code unchanged.</ref>
    <ref type="dim_schema">silver/bd_assets_dim.parquet — cols include `asset_id, cusip, ..., symbol, ticker, asset_name, ...` (10,937 rows; 7,690 have ticker+cusip both non-null; 70% coverage). B_01 already loads this dim at L281 for the `asset_id → cusip` enrichment on silver/transactions; HLOT2b adds a parallel ticker-keyed lookup on the same DataFrame.</ref>
    <ref type="target_file">data/black_diamond/scripts/gold/B_01.holdings_lots.py — modify `_build_authoritative_reopen_lots` at L1112-1116 + add ticker→cusip enrichment step</ref>
  </references>

  <objective>
    Fix the `canonical/holdings missing cols {'cusip'} -- reopen skipped` bailout in B_01 Patch B path. Add ticker-keyed `bd_assets_dim` merge to enrich canonical/holdings with cusip BEFORE the required-cols check. Both Patch B Tier 1 (silver_unrealized_reopen/topup — expected ~$102.7M on IEFA+SPYM+IDVZ+IEMG+SPHY) and Tier 2 (canonical_holdings_reopen/topup — expected ~25 accts) paths activate post-fix.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/B_01.holdings_lots.py — `_build_authoritative_reopen_lots` function (L1112-1116 required-cols check + upstream ticker→cusip merge)</file>
    </files>
    <non_scope>
      - NO change to C_00 / B_00 / canonical/holdings emission schema. Ticker-keyed enrichment happens at the consumer (B_01), not the producer.
      - NO change to bd_assets_dim or silver_unrealized or silver/transactions upstream artifacts.
      - NO change to Patch A logic (paired_subs CA-Merger classifier at L??? — Patch A 73% partial is a SEPARATE adjudication item for CTO).
      - NO change to the `required_cols = {'account_id', 'cusip', 'asset_name', 'units', 'price'}` set — cusip stays required but is now derivable via the merge.
    </non_scope>
  </scope>

  <deliverables>
    <deliverable id="ticker-to-cusip-enrichment">
      In `_build_authoritative_reopen_lots` BEFORE the `required_cols.issubset(canonical.columns)` check:
      1. Load (or reuse already-loaded) `silver/bd_assets_dim.parquet`.
      2. Build ticker-keyed cusip map: `dim[['ticker','cusip']].drop_duplicates('ticker').dropna(subset=['ticker','cusip'])` — ~7,690 rows covering ~70% of assets.
      3. Merge canonical/holdings → cusip via `pd.merge(canonical, ticker_cusip_map, on='ticker', how='left')`. Rows with ticker not in dim (~30% dim incompleteness + any canonical tickers absent from dim) get NaN cusip.
      4. Keep the `required_cols.issubset` check; now it passes (cusip column exists). But handle per-row NaN cusip:
         - If a row's cusip is still NaN post-merge, EITHER drop it from the reopen input (current skip-lot behavior at row-level), OR log-and-continue with skip flag. Preference: drop + log count so it's visible in attribution pack ("N rows skipped: no cusip via ticker→bd_assets_dim").
      5. Log a one-liner on merge: `[HLOT2 reopen] canonical/holdings ticker→cusip enriched: {N_merged} rows, {N_skipped} rows skipped on missing dim cusip` so attribution pack can quote it.
    </deliverable>
    <deliverable id="smoke-test">
      Local dry-run against 2026-04-17 canonical/holdings fixture (or equivalent). Before commit:
      - Print merge count distribution by ticker for the 5 HLOT2 Patch B Tier 1 targets. Expect non-zero counts on all 5 (IEFA+SPYM+IDVZ+IEMG+SPHY).
      - No NameError / no ImportError / .tools/ds-commit-gate.sh EXIT 0 (CLAUDE.md Rule 14).
    </deliverable>
    <deliverable id="commit-and-preflag">
      1. Commit on CLOUD with `--only --author="0.4.0_DS_ClientPlatform ..." -- data/black_diamond/scripts/gold/B_01.holdings_lots.py` (plus any docstring updates on that file only).
      2. Pre-flag #1 MCP to CTO + COO immediately on commit (A→D-rerun-sensitive per canonical_nna write invariant via downstream D-cascade). Include: commit SHA, ticker merge count spot-check, fix scope summary, expected Patch B recovery target (~$102.7M Tier 1 + ~25 accts Tier 2).
      3. Pre-flag #2 MCP to CTO + COO before `aws s3 cp`. COO gate criteria (same as dfaeddc2 Phase 6a):
         - commit clean + pushed origin/CLOUD
         - comp-pipescript deployed B_01 STALE baseline captured
         - merge-count spot-check evidence attached (smoke-test output)
         - A→D impact statement: fix to Patch B reopen path; no schema change; no concurrent-write risk (no other agent touches B_01 right now).
      4. On COO+CTO ✓: DS-direct `aws s3 cp` per CLAUDE.md Rule 13. Then MCP AE for qa-runner `--from B_00 --chain full` re-dispatch (include `--chain` this time — `51ce2df1` dropped it).
    </deliverable>
    <deliverable id="patch-b-validation">
      Post-run (D-cascade completed this time) comparison pack addendum:
      - Row count per `price_quality` tag: expect non-zero `silver_unrealized_reopen / silver_unrealized_topup / canonical_holdings_reopen / canonical_holdings_topup`.
      - Per-ticker attribution table for IEFA/SPYM/IDVZ/IEMG/SPHY: delta in accumulated market value vs pre-HLOT2b baseline (2026-04-17 partition before HLOT2b fix). Sum should approach ~$102.7M Tier 1 split silent/overlap.
      - Tier 2 canonical_holdings_* tag: ~25 accts enriched via canonical/holdings fallback lane.
      - Firm total_aua invariant: still $1,646.4M (HLOT2b is attribution-shift inside the cap envelope, not a new-AUA addition).
    </deliverable>
  </deliverables>

  <wire_contract>
    - Zero schema change to canonical/holdings (producer stays as-is).
    - Zero change to Patch A logic (73% partial is a SEPARATE CTO-adjudication item).
    - B_01 Patch B path activates — no new script, no new S3 key, no new portal surface.
    - Firm total_aua unchanged at $1,646.4M (post B_01 cap).
    - Attribution shift: per-ticker market value increases on the 5 Tier 1 tickers + ~25 Tier 2 accts; matching offsets in other patch-silent/patch-overlap buckets.
  </wire_contract>

  <acceptance_criteria>
    1. B_01 `_build_authoritative_reopen_lots` merges canonical/holdings with bd_assets_dim on ticker BEFORE the required-cols check, then cleanly handles per-row NaN cusip.
    2. Pre-commit gate `.tools/ds-commit-gate.sh` EXIT 0 (CLAUDE.md Rule 14).
    3. Commit on CLOUD under `0.4.0_DS_ClientPlatform` author with explicit pathspec.
    4. Pre-flag #1 MCP sent to CTO + COO with commit SHA + merge-count evidence.
    5. Pre-flag #2 MCP sent to CTO + COO before `aws s3 cp`; COO ✓ before upload.
    6. comp-pipescript deployed B_01 MATCH post-upload.
    7. Qa-runner `--from B_00 --chain full` re-dispatch (AE; include `--chain` this time) — full A→D cascade completes.
    8. Patch B evidence pack shows non-zero rows with the 4 source_tag values; per-ticker Tier 1 deltas approach ~$102.7M sum.
    9. Firm total_aua invariant verified $1,646.4M post-run.
    10. RAVC4 close bundled with the existing Patch A partial adjudication (pending CTO threshold call from surface MCP `20260421T183825Z`).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Read silver/bd_assets_dim.parquet + verify ticker+cusip column presence + spot-check IEFA/SPYM/IDVZ/IEMG/SPHY presence</run>
        <expect>All 5 HLOT2 Patch B Tier 1 target tickers present with valid CUSIPs. ~7,690/10,937 rows have ticker+cusip non-null (confirmed by COO adjudication 20260421T182813Z).</expect>
        <if_mismatch>If any of the 5 targets missing, surface to COO before authoring fix — may indicate dim refresh lag or data quality issue warranting separate investigation.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io B_01</run>
        <expect>READS include silver/bd_assets_dim (already loaded) + canonical/holdings (no cusip today). WRITES includes gold/timeseries/holdings_lots. No COLUMN GAPS.</expect>
        <if_mismatch>If silver/bd_assets_dim not in READS, add it. If COLUMN GAPS surface on canonical columns referenced post-merge, fix load list.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/B_01.holdings_lots.py + .tools/ds-commit-gate.sh data/black_diamond/scripts/gold/B_01.holdings_lots.py</run>
        <expect>Both EXIT 0. Gate catches any undefined-name regression from the merge addition. Per CLAUDE.md Rule 14.</expect>
        <if_mismatch>STOP. Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>Local smoke: load 2026-04-17 canonical/holdings fixture + run merge; count rows per ticker for the 5 HLOT2 Patch B Tier 1 targets</run>
        <expect>All 5 tickers show non-zero row count. CUSIPs match dim entries (IEFA=46432F842, etc).</expect>
        <if_mismatch>If any ticker missing, investigate — may be absent from canonical/holdings on that date (valid) vs merge broken (invalid).</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed B_01</run>
        <expect>STALE pre-upload (matches current S3 B_01 as 5f5d0319 pre-HLOT2b). Confirms upload path is clean.</expect>
        <if_mismatch>If MATCH pre-upload, someone else uploaded to S3 in parallel — coordinate before firing `aws s3 cp`.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript deployed B_01 (post-upload)</run>
        <expect>MATCH. S3 ETag matches local md5 (byte-identical round-trip per CLAUDE.md Rule 13 DS-direct upload pattern).</expect>
        <if_mismatch>Re-run `aws s3 cp` (may be ETag propagation).</if_mismatch>
      </step>
      <step>
        <run>Qa-runner `--from B_00 --chain full --bg --no-shutdown` (AE dispatches per DS MCP)</run>
        <expect>Full A→D cascade completes this time (prior `51ce2df1` dropped `--chain`). Expected wall ~45-60 min.</expect>
        <if_mismatch>If any script exits non-zero, pull stdout from S3 log path, diagnose, flag to COO.</if_mismatch>
      </step>
      <step>
        <run>Post-run Patch B attribution evidence — per-ticker delta on 5 Tier 1 targets + Tier 2 acct count + firm total_aua invariant</run>
        <expect>5 Tier 1 tickers show non-zero delta summing to ~$102.7M. ~25 Tier 2 accts. Firm total_aua = $1,646.4M (invariant).</expect>
        <if_mismatch>If total sum < 80% of $102.7M target, flag as partial (like Patch A 73% fork — CTO adjudicates threshold). If > 120%, investigate — may be over-reopening.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>**Hard sequencing vs CHART-ALIGN (`62a24746`) + COHORT-A (`3cf43c26`):** Phase 6a RAVC4 closes INDEPENDENTLY of this TO (at C_01 grain). ~B CHART-ALIGN + COHORT-A S3 uploads fire on Phase 6a RAVC4 close, NOT on HLOT2b close. HLOT2b can run in parallel with ~B's upload + qa-runner --group D after 6a closes.</item>
    <item>**AE D re-dispatch:** AE was flagged in COO MCP `20260421T183838Z` on the `--chain` drop. Either AE re-dispatches `--from D_00 --chain full` NOW against the current B+C fresh data (gives HLOT2 Patch A $57M evidence at lot-attribution grain), OR waits for HLOT2b ship + single `--from B_00 --chain full` covering both. DS + AE coordinate to avoid double-run waste.</item>
    <item>**Patch A 73% partial — SEPARATE fork, don't block HLOT2b:** CTO surface MCP `20260421T183825Z` asks for acceptance threshold. That's independent adjudication from HLOT2b. HLOT2b ships regardless of Patch A threshold call.</item>
    <item>**No collision with Schwab Phase 6a (C_01 + lib/schwab_flows) — different files.** No collision with CHART-ALIGN (D_00c) or COHORT-A (D_04) — different files.</item>
  </cross_domain_coordination>

  <dependencies>
    <dependency agent="2.0.0_SA_COO" task="HLOT2b TO authoring" status="in-flight">Direct-dispatch authored on DS pre-drafted fix. No staged→pending flip needed — DS has fix drafted + gate-clean per fork MCP.</dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="qa-runner --chain full dispatch post-HLOT2b upload" status="pending">AE dispatches with --chain flag included (not dropped). Sequencing flexible: can run against fresh B+C now then re-run post-HLOT2b, or single run post-HLOT2b. DS + AE coordinate.</dependency>
    <dependency agent="1.0.0_SA_CTO" task="Patch A 73% partial threshold adjudication" status="pending">Independent of HLOT2b — runs in parallel. MCP `20260421T183825Z` pending CTO response.</dependency>
  </dependencies>

  <next>
    On DS fix commit + pre-flag #1: COO ✓, DS fires `aws s3 cp` per CLAUDE.md Rule 13 DS-direct pattern. Pre-flag #2 before upload, COO gate-check (same as dfaeddc2 Phase 6a), DS uploads, comp-pipescript deployed MATCH, MCP AE for `--from B_00 --chain full` (with `--chain` this time). Post-run: DS produces Patch B evidence (per-ticker Tier 1 + Tier 2 acct + firm invariant) + MCP COO+CTO. On COO+CTO receipt: flip HLOT2b + HLOT2 (both) to complete once Patch A threshold call also landed.
  </next>
</task_order>
