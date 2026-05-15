<task_order>
  <metadata>
    <id>ADVI_INFINC.004</id>
    <slug>dsd-pattern-c-per-hh-timeseries-cache</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-05-15</date>
    <status>active</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED — INFINC.003 RAVC2 received (c6493139f). Phase 4 authorized.</dispatch_unblock_condition>
    <project_code>ADVI_INFINC</project_code>
    <priority>P1 — Pattern C eliminates ~7,500 historical anchor reads per chain run across INF_D_06/D_05/D_09</priority>
    <sla>~3-4h wall actual per Pod 4 velocity (more complex than A/B)</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inf-incremental-pipeline-design-20260514.md §2.3 (Pattern C mechanics)</ref>
    <ref type="phase3">ADVI_INFINC.003 RAVC2 (c6493139f) — Pattern B complete; Phase 4 authorized</ref>
    <ref type="lib_phase1">data/orion/scripts/gold/lib/skip_gate.py — NOT used in Pattern C (per-HH cache is script-internal); schema_version.py IS used</ref>
  </references>

  <context>
    Pattern C = per-HH historical-replay artifact cache. Three scripts currently rebuild all HH artifacts from full historical anchor reads on every run:

    INF_D_06 client_timeseries:
      Current: for each of ~300 HHs, walks ~25 quarters of historical anchor reads → platinum/clients/{hh}/timeseries.json
      Bottleneck: ~7,500 historical anchor lookups per run

    INF_D_05 client_top_holdings:
      Same structure. Output: platinum/clients/{hh}/top_holdings.json

    INF_D_09 account_timeseries:
      Same structure. Output: platinum/clients/{hh}/accounts/{acct}/timeseries.json

    Total bottleneck: 25 quarters × 300 HHs × 3 scripts = ~22,500 historical anchor reads eliminated per chain run.

    v1 optimization per brief §2.3:
      Keep the current "rebuild all HHs" structural loop.
      Add a cache parquet: gold/cache/hh_timeseries_anchors.parquet
        - Key: (hh_id, period, script_id) — e.g., ('HH12345', '2025-Q4', 'INF_D_06')
        - Value: anchor_holdings_date (the resolved holdings_{date}.parquet date for that period)
      On each run, for each HH × period:
        1. Check cache: if (hh_id, period, script_id) is in cache AND the holdings_{date}.parquet mtime hasn't changed → use cached anchor, skip the historical lookup.
        2. If not in cache or stale mtime: do the historical anchor lookup, then write to cache.
      Current quarter always recomputed (no cache) — only past quarter-ends are cached.

    Cache invalidation:
      Per-period invalidation: if holdings_{date}.parquet for that period's anchor date has changed mtime (or is missing from S3) → cache entry stale → recompute and update.
      Full cache flush: INFINC_REBUILD=true → delete cache parquet + full rebuild.
      Schema version guard: if SCHEMA_VERSION bumped vs gold/meta/schemas/{script}.json → full rebuild + cache flush.

    Serial discipline:
      INF_D_06 first (client_timeseries — highest-impact). Then INF_D_05. Then INF_D_09.
      ds-commit-gate.sh PASS on each before touching next.
  </context>

  <objective>
    Add per-HH timeseries anchor cache (gold/cache/hh_timeseries_anchors.parquet) to INF_D_06, INF_D_05, INF_D_09. Skip historical anchor reads for past quarter-ends where cache is fresh. Eliminate ~22,500 anchor reads per chain run.
  </objective>

  <scope>
    <files>
      <file action="modify">data/orion/scripts/gold/INF_D_06.client_timeseries.py — Pattern C anchor cache</file>
      <file action="modify">data/orion/scripts/gold/INF_D_05.client_top_holdings.py — Pattern C anchor cache</file>
      <file action="modify">data/orion/scripts/gold/INF_D_09.account_timeseries.py — Pattern C anchor cache</file>
      <file action="readonly_reference">data/orion/scripts/gold/lib/schema_version.py — schema version tracking</file>
      <file action="readonly_reference">docs/briefs/inf-incremental-pipeline-design-20260514.md §2.3 — Pattern C specification</file>
    </files>
  </scope>

  <phase id="0" when="before write — I/O surface">
    <step>
      <run>comp-pipescript io INF_D_06 — confirm: (a) historical anchor lookup pattern (how holdings dates are resolved per quarter), (b) per-HH output path, (c) current loop structure for HH iteration.</run>
      <expect>Loop structure understood. Anchor lookup pattern identified. Cache insertion points mapped.</expect>
    </step>
    <step>
      <run>comp-pipescript io INF_D_05, comp-pipescript io INF_D_09 — same for each. Identify if all three share the same anchor-lookup helper or have separate implementations.</run>
      <expect>Anchor lookup pattern identified for all three scripts. Shared helper = single cache implementation location. Separate = three implementations.</expect>
    </step>
    <step>
      <run>Read current S3 path for gold/cache/ — confirm s3://opal-data-inf/gold/cache/ is writable and not used by other scripts. If cache path conflicts, use gold/cache/hh_timeseries_anchors_{script_id}.parquet per-script.</run>
      <expect>Cache S3 path confirmed. No conflicts.</expect>
    </step>
  </phase>

  <phase id="1" when="implementation — INF_D_06 first, then D_05, then D_09">
    <step>
      <run>INF_D_06 Pattern C migration:
        1. Import schema_version.py. Set SCHEMA_VERSION constant at top.
        2. Add _load_anchor_cache(script_id) → DataFrame: read gold/cache/hh_timeseries_anchors.parquet from S3; if absent return empty DataFrame.
        3. Add _save_anchor_cache(cache_df, script_id): write updated cache to S3.
        4. In main(): if INFINC_REBUILD=true or schema version mismatch: flush cache + full rebuild.
        5. In per-HH loop: for each past quarter-end period, check cache first. If (hh_id, period) cached and holdings anchor still valid (check S3 mtime or etag): use cached anchor. Else: do full anchor lookup + update cache entry.
        6. Current quarter: always recompute (no cache).
        7. Write cache back to S3 after all HH iterations complete.
        ds-commit-gate.sh INF_D_06 before proceeding to D_05.</run>
      <expect>Anchor cache working. Historical periods skip for cached HHs. 3-gate PASS.</expect>
      <if_mismatch>Fix INF_D_06 before touching INF_D_05. Serial discipline.</if_mismatch>
    </step>
    <step>
      <run>INF_D_05 client_top_holdings: same Pattern C migration. Per-script cache key: script_id='INF_D_05'. ds-commit-gate.sh INF_D_05.</run>
      <expect>3-gate PASS.</expect>
    </step>
    <step>
      <run>INF_D_09 account_timeseries: same Pattern C migration. Per-script cache key: script_id='INF_D_09'. ds-commit-gate.sh INF_D_09.</run>
      <expect>3-gate PASS.</expect>
    </step>
  </phase>

  <phase id="2" when="validation">
    <step>
      <run>First-run validation: run INF_D_06 with empty cache (or INFINC_REBUILD=true). Verify: (a) all HH artifacts written, (b) cache parquet written to S3 with HH × period entries for all past quarter-ends.</run>
      <expect>Cache populated on first run. All HH artifacts written correctly.</expect>
    </step>
    <step>
      <run>Second-run validation: run INF_D_06 again (cache populated). Verify: (a) historical periods skipped for cached entries, (b) only current quarter recomputed, (c) wall time materially reduced vs first run, (d) output artifacts byte-equal to first run for historical periods.</expect>
      <expect>Cache hit rate high. Wall time reduced. Byte-equal historical artifacts.</expect>
    </step>
    <step>
      <run>Cache invalidation test: modify holdings_{date}.parquet mtime (or simulate stale mtime) for one period. Run INF_D_06. Verify: stale period recomputed, cache updated, fresh periods still cached.</run>
      <expect>Selective cache invalidation works correctly.</expect>
    </step>
    <step>
      <run>INFINC_REBUILD=true validation: run with env var. Verify: cache flushed, full rebuild, cache repopulated.</run>
      <expect>Full rebuild path clean.</expect>
    </step>
    <step>
      <run>Repeat second-run wall time comparison for INF_D_05 + INF_D_09.</run>
      <expect>Same pass criteria. Wall time reduced on cached run.</expect>
    </step>
  </phase>

  <phase id="3" when="commit + deploy">
    <step>
      <run>safe-commit.sh --author "0.4.0_DS_ClientPlatform~D &lt;0.4.0_DS_ClientPlatform~D@opal.agent&gt;" -m "feat(INFINC.004): Pattern C per-HH timeseries anchor cache — INF_D_06/D_05/D_09" -- data/orion/scripts/gold/INF_D_06.client_timeseries.py data/orion/scripts/gold/INF_D_05.client_top_holdings.py data/orion/scripts/gold/INF_D_09.account_timeseries.py</run>
      <expect>Commit clean. No contamination.</expect>
    </step>
    <step>
      <run>safe-deploy.sh — push CLOUD + S3 upload + comp-pipescript deployed MATCH for INF_D_06 + INF_D_05 + INF_D_09.</run>
      <expect>SHA-MATCH on all three. Deploy clean.</expect>
    </step>
    <step>
      <run>SSM-direct INF_D_06 two-run validation. Log first-run cache-miss count + wall time. Log second-run cache-hit count + wall time. Report delta.</run>
      <expect>Wall time materially reduced on second run. Cache hit rate ~92%+ (all past quarter-ends except current).</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + AE 0.6.1 with: commit SHA, deploy MATCH, first-run vs second-run wall time comparison, cache-hit evidence, byte-equal attestation for historical HH artifacts.</run>
      <expect>Evidence-bearing RAVC2. Phase 5 (Pattern D dependency-skip) authorized post-RAVC2.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: INF_D_06 uses hh_timeseries_anchors.parquet cache for past quarter-end periods
    AC2: INF_D_05 same Pattern C anchor cache
    AC3: INF_D_09 same Pattern C anchor cache
    AC4: Cache key: (hh_id, period, script_id); invalidation on holdings mtime/etag change
    AC5: Current quarter always recomputed (no cache for in-progress period)
    AC6: INFINC_REBUILD=true → cache flush + full rebuild
    AC7: Schema version guard: if SCHEMA_VERSION bumped → full rebuild + cache flush
    AC8: Second-run wall time materially less than first-run (cache hit rate ~92%+)
    AC9: Historical HH artifacts byte-equal between first and second run (correctness)
    AC10: ds-commit-gate.sh 3-gate PASS on all three scripts
    AC11: from __future__ import annotations preserved as first import (Rule 15)
    AC12: safe-deploy.sh PASS + comp-pipescript deployed MATCH on all three scripts
    AC13: No emoji per CLAUDE.md
    AC14: RAVC2 to COO + CC CTO + AE 0.6.1 with wall-time comparison evidence
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 0 comp-pipescript io x3; Phase 1 ds-commit-gate.sh x3; Phase 3 comp-pipescript deployed x3; safe-deploy.sh.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCY: INFINC.003 RAVC2 (c6493139f) — COMPLETE.
    AE 0.6.1: CC on RAVC2; chain re-fire for INF_D_06/D_05/D_09 after deploy.
    DOWNSTREAM: Phase 5 (Pattern D dependency-skip for INF_D_00/D_00b/D_00c/D_02/D_02b etc.) gates on this RAVC2.
    NO PLATINUM SHAPE CHANGE: HH artifact schema unchanged; downstream consumers unaffected by cache vs full-rebuild.
  </cross_domain_coordination>

  <notes>
    **Serial discipline:** INF_D_06 first (highest-impact). ds-commit-gate.sh PASS before D_05. D_05 PASS before D_09.

    **Cache S3 path:** s3://opal-data-inf/gold/cache/hh_timeseries_anchors_{script_id}.parquet (per-script cache to avoid cross-script contamination).

    **Holdings mtime/etag check:** S3 ListObjectsV2 with Metadata=True gives Last-Modified + ETag. Cache entry is valid if stored ETag matches current S3 ETag for that holdings_{date}.parquet. If ETags match → skip anchor read. If mismatch → recompute + update cache.

    **Current quarter definition:** the period whose end date is in the future or is the most recent quarter-end. Only this period is always recomputed.

    **pd.concat sort=False:** required in cache DataFrame operations to preserve column order.

    **No emoji per CLAUDE.md.**

    **Author identity:** --author="0.4.0_DS_ClientPlatform~D &lt;0.4.0_DS_ClientPlatform~D@opal.agent&gt;".
  </notes>
</task_order>
