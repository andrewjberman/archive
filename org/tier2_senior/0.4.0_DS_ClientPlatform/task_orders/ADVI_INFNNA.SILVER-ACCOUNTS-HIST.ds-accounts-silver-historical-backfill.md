<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.SILVER-ACCOUNTS-HIST</id>
    <project>ADVI_INFNNA</project>
    <title>silver/accounts_v2 per-date historical backfill + assets_v2/accounts_v2 disambiguation in SILVER TO AC4</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>staged</status>
    <priority>low</priority>
    <estimated_effort>~30-60 min</estimated_effort>
    <authorized_by>Andrew direct 2026-05-11 (approved COO recommended routing)</authorized_by>
  </metadata>

  <references>
    <ref type="parent_finding">DS~A Proposal-2 sweep 2026-05-11 — `decaaf523` SILVER AC4 FAIL: only 7 snapshot dates of accounts_v2. ALSO: SILVER TO AC4 calls dim "assets_v2" but `assets_v2/` has just 1 snapshot — `accounts_v2/` is the relevant dim.</ref>
    <ref type="affected_path">silver/accounts_v2/ — 7 snapshot dates currently; target ~6 years of daily/weekly snapshots</ref>
    <ref type="naming_issue">SILVER TO AC4 text disambiguation needed: assets_v2 (1 snapshot) vs accounts_v2 (7 snapshots, the relevant dim)</ref>
  </references>

  <context>
    INFNNA.SILVER TO AC4 currently failing — silver/accounts_v2 has only 7 snapshot dates. AC4 text in the original SILVER TO refers to "assets_v2" but `assets_v2/` is a different (1-snapshot) dim — DS~A flagged the naming disambiguation needed.

    Two-part scope:
    1. **Update SILVER TO AC4** — text correction: assets_v2 → accounts_v2 (clarify which dim AC4 measures completeness on)
    2. **Build historical accounts_v2 backfill** — per-date pattern, mirror PERFDIM-CREATOR ThreadPoolExecutor approach

    Independent of ACCOUNT-ID-COERCE — silver/accounts_v2 is read by INF_A_00, INF_D_08, and others, but these scripts use whatever accounts_v2 state exists; expanding to historical is additive.

    Bandwidth-gated: priority `low`. Pickup when DS~A bandwidth is free; no Andrew gate.
  </context>

  <scope>
    <step>
      **Update SILVER TO AC4 text** — disambiguate. Find the SILVER TO file (`ADVI_INFNNA.SILVER.ds-historical-silver-builds.md`). Update AC4 to say:
      &gt; AC4: silver/accounts_v2/ has ≥{N} snapshot dates spanning 2020-03-11 → present. (NOT silver/assets_v2/ which is a 1-snapshot reference dim.)

      Commit as DS-lane edit.
    </step>

    <step>
      Survey existing silver/accounts_v2 code. Identify the per-date backfill entry point.
    </step>

    <step>
      Build the dispatcher script (local Python ThreadPoolExecutor pattern, 64 workers). Path: `data/orion/scripts/silver/build_accounts_v2_historical.py` or equivalent.

      Pre-commit gate: `.tools/ds-commit-gate.sh data/orion/scripts/silver/*.py`.
    </step>

    <step>
      Dry-run on 1 week of dates first to validate. Capture timing + soft-fail rate.
    </step>

    <step>
      Full backfill 2020-03-11 → 2026-05-11. Expected wall-clock ~30-60 min for ~2,250 daily snapshots.
    </step>

    <step>
      Verify output: partition count, spot-check 3 dates, soft-fail rate &lt;5%. Verify downstream INF_A_00 still ingests new partitions correctly (regression check).
    </step>

    <step>
      Update SILVER TO: mark AC4 PASS with row counts + soft-fail list. Commit. RAVC2 to COO.
    </step>
  </scope>

  <acceptance_criteria>
    1. SILVER TO AC4 text disambiguated (assets_v2 → accounts_v2 clarification).
    2. Dispatcher script shipped + gate-PASS.
    3. Full backfill completes within ~60 min wall-clock.
    4. Partition count matches expected (2,250+ daily snapshots).
    5. Soft-fail rate &lt;5%; failed dates documented.
    6. Downstream INF_A_00 regression check PASS (no new errors on next cascade).
    7. SILVER TO AC4 marked PASS.
    8. RAVC2 to COO with backfill summary.
  </acceptance_criteria>

  <blocking>
    No upstream blockers. Bandwidth-gated only.

    Adjacent: do NOT execute while ACCOUNT-ID-COERCE or LEADERBOARD-JOE-ABSENT are in flight — DS~A must finish those first. SILVER-PERFORMANCE-HIST can run before or after this TO; they are independent of each other.
  </blocking>

  <notes>
    If accounts_v2 backfill exposes a new dtype-drift on any column (similar to ACCOUNT-ID-COERCE's account_id mixed-state issue), surface immediately and pause backfill before propagating drift to 2,250 partitions. Apply the `coerce_account_id` helper pattern preemptively if the same risk applies to other columns.
  </notes>
</task_order>
