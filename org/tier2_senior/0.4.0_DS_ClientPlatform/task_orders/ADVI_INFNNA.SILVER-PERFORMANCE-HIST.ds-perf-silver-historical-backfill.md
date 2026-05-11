<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.SILVER-PERFORMANCE-HIST</id>
    <project>ADVI_INFNNA</project>
    <title>silver/performance per-date historical backfill 2020-03-11 → 2026-05-11 — mirror tax_realized per-date pattern</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>staged</status>
    <priority>low</priority>
    <estimated_effort>~30-60 min</estimated_effort>
    <authorized_by>Andrew direct 2026-05-11 (approved COO recommended routing)</authorized_by>
  </metadata>

  <references>
    <ref type="parent_finding">DS~A Proposal-2 sweep 2026-05-11 — `decaaf523` SILVER AC2 FAIL: only 4 snapshot dates exist (04-28, 05-09, 05-10, 05-11). Historical not built.</ref>
    <ref type="reference_pattern">tax_realized silver per-date historical backfill — uses local Python ThreadPoolExecutor pattern from PERFDIM-CREATOR. Mirror that approach.</ref>
    <ref type="reference_commit">PERFDIM-CREATOR commit `94c624901` for the canonical per-date pattern</ref>
    <ref type="affected_path">silver/performance/ — 4 snapshot dates currently; target ~6 years of daily/weekly snapshots</ref>
  </references>

  <context>
    INFNNA.SILVER TO AC2 currently failing — silver/performance has only 4 snapshot dates (04-28, 05-09, 05-10, 05-11). Historical per-date snapshots from 2020-03-11 (Inflection bronze frontier) to 2026-05-11 (today) not built.

    Performance silver is needed for any future historical analytics, multi-year regression analyses, or back-test scenarios. Not blocking current portal correctness, but a structural gap.

    Mirror the tax_realized per-date pattern (PERFDIM-CREATOR `94c624901`):
    - Per-date executor using local Python ThreadPoolExecutor (64 workers worked well for the bronze backfill at 10x speedup)
    - One partition per snapshot date
    - Soft-fail tolerance for dates with no underlying bronze coverage

    Independent of ACCOUNT-ID-COERCE — silver/performance is read by INF_C_00 (performance gold), not by the 6 ACCOUNT-ID-COERCE-affected scripts.

    Bandwidth-gated: priority is `low`. Pickup when DS~A bandwidth is free; no Andrew gate.
  </context>

  <scope>
    <step>
      Survey existing silver/performance code. Identify the per-date backfill entry point or build script that needs to be invoked per-date.
    </step>

    <step>
      Build the dispatcher script (local Python ThreadPoolExecutor pattern, 64 workers). Path: `data/orion/scripts/silver/build_performance_historical.py` or equivalent location consistent with existing conventions.

      Pre-commit gate: `.tools/ds-commit-gate.sh data/orion/scripts/silver/*.py`.
    </step>

    <step>
      Dry-run on 1 week of dates first to validate the pattern works. Capture timing + soft-fail rate.
    </step>

    <step>
      Full backfill 2020-03-11 → 2026-05-11. Expected wall-clock ~30-60 min for ~2,250 daily snapshots at 64-worker parallelism (extrapolating from performance bronze backfill 50min / 2,123 partitions).
    </step>

    <step>
      Verify output: partition count = expected per-date count; spot-check 3 dates (early-2020, mid-2023, recent-2026) for non-empty content. Soft-fail rate should be &lt;5% (similar to performance bronze's 2.5% soft-fail).
    </step>

    <step>
      Update SILVER TO: mark AC2 PASS with row counts + soft-fail list. Commit. RAVC2 to COO.
    </step>
  </scope>

  <acceptance_criteria>
    1. Dispatcher script shipped + gate-PASS.
    2. Full backfill completes within ~60 min wall-clock.
    3. Partition count matches expected (2,250+ daily snapshots).
    4. Soft-fail rate &lt;5%; failed dates documented.
    5. SILVER TO AC2 marked PASS.
    6. RAVC2 to COO with backfill summary.
  </acceptance_criteria>

  <blocking>
    No upstream blockers. Bandwidth-gated only.

    Adjacent: do NOT execute while ACCOUNT-ID-COERCE or LEADERBOARD-JOE-ABSENT are in flight — DS~A must finish those first.
  </blocking>

  <notes>
    The performance gold layer (INF_C_00) currently uses whatever silver/performance state exists. After this backfill, INF_C_00 will have richer historical input. Verify INF_C_00 output regression — wall-clock should rise proportional to input size; correctness should be unchanged on overlapping dates.
  </notes>
</task_order>
