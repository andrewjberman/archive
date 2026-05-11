<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.GOLD</id>
    <project>ADVI_INFNNA</project>
    <title>Gold canonical_nna rebuild + INF_D_08 + INF_D_00c re-run with corrected historical attribution</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <priority>high</priority>
    <estimated_effort>~2h gold rebuild + dispatch + verify</estimated_effort>
  </metadata>

  <references>
    <ref type="incident">INFNNA.001 RAVC2 — historical canonical_nna parquets carry stale IWM-aggregated attribution from before Orion's retroactive rep_id reattribution. Joe Brandenburg (rep_id=6) absent from these artifacts because pull_inflection_transactions_v2.py @RepIDs hardcoded "3,11,12".</ref>
    <ref type="silver_inputs">silver/transactions/2026-05-07.parquet (1.15M rows, full historical, rep_id 3+6+11+12 included). silver/api_dims/accounts_v2/snapshot_date=2026-05-07 (848 rows, $203.2M, INFLECTION_REP_IDS filtered).</ref>
    <ref type="gold_scripts">data/orion/scripts/gold/INF_C_01.canonical_nna.py (canonical_nna builder); INF_D_08.nmec_nmnc_nna.py (firm + per-advisor NNA artifact); INF_D_00c.portal_leaderboard.py (per-advisor leaderboard NNA)</ref>
    <ref type="dependency_to">INFNNA.SILVER (per-date silver builds for tax + perf + billing must complete first)</ref>
  </references>

  <context>
    Once silver layer is rebuilt with INFLECTION_REP_IDS {3,6,11,12} attribution AND
    per-date historical coverage, the gold layer must be regenerated to reflect the
    corrected attribution. The critical artifact is canonical_nna_{date}.parquet — which
    carries cumulative cash flow attribution per advisor over time. Without rebuilding,
    the portal's NMNC/NNA inconsistency persists ($19.7M Q2 NMNC vs -$1.36M Q2 firm NNA)
    because canonical_nna's IWM bucket still holds Joe + Patrick + Peter historical flows.

    INF_C_01 reads silver/transactions + silver/api_dims/accounts_v2 + activity dim;
    produces gold/canonical/canonical_nna_{date}.parquet for each date in range.

    INF_D_08 (firm + per-advisor NNA) and INF_D_00c (leaderboard) consume canonical_nna
    and produce platinum-bound JSONs (eventually). Both must re-run after canonical_nna.
  </context>

  <scope>
    <step>
      Read INF_C_01.canonical_nna.py header to understand inputs, outputs, date-range
      args, and idempotency. Confirm it reads:
        - silver/transactions/{date}.parquet (or silver/transactions/*.parquet rolled up)
        - silver/api_dims/accounts_v2/snapshot_date={date}/data.parquet
        - silver/api_dims/activity/* if available
      And produces:
        - gold/canonical/canonical_nna_{date}.parquet
    </step>
    <step>
      Determine canonical date range for rebuild. Recommended: 2020-03-11 → 2026-05-07
      (full historical) so leaderboard MAX window + NNA timeseries chart all reflect
      corrected attribution.

      If runtime is prohibitive (gold script per-date overhead high), narrow to YTD-only
      first (2026-01-01 → today) and surface to COO for full-historical decision.
    </step>
    <step>
      Run INF_C_01.canonical_nna.py for the chosen date range. Use --start/--end args
      if available, or wrap in date-loop with skip-existing logic.

      Local execution preferred (pyarrow joins fit in COO laptop memory) OR dispatch via
      AE 0.7 SSM on inf-gold-layer-runner if remote is required.

      Track failures + skip-400 dates (pre-onboarding expected behavior).
    </step>
    <step>
      Verify canonical_nna parquet for a Q2 2026 date:
        - Sample row should show Joe Brandenburg (rep_id=6) with non-zero NNA values
        - IWM (rep_id=3) should normalize to small NNA (its 13 actual accounts only)
        - Sum of advisor NNAs ≈ firm NNA
    </step>
    <step>
      Re-run INF_D_08.nmec_nmnc_nna.py (no args; uses latest bronze date).
      Verify platinum/firm/nmec_nmnc_nna.json:
        - Joe Brandenburg (rep_id=6) appears with non-zero nmnc_aua + nna_*
        - peter_lee no longer dominates with 89% nmnc share
        - Firm QTD NNA reflects all 4 advisors
    </step>
    <step>
      Re-run INF_D_00c.portal_leaderboard.py.
      Verify platinum/firm/leaderboard.json:
        - 4 entries (one per advisor)
        - Joe Brandenburg's NNA ≠ 0
        - Firm total NNA reflats to a value consistent with Q2 NMNC reconciliation
        (NMNC ≈ NNA-inflows from new accounts)
    </step>
    <step>
      Coordinate with AE 0.7 for PROD dispatch (if local rebuild is staging-only). PROD
      run path:
        - Commit any code changes via DS commit cycle
        - S3 upload via comp-pipescript deployed MATCH
        - SSM dispatch to inf-gold-layer-runner with --chain INF_C_01 + INF_D_08 + INF_D_00c
    </step>
    <step>
      RAVC1 (mid): canonical_nna rebuild complete with sample verification.
      RAVC2 (final): INF_D_08 + INF_D_00c re-run complete with platinum artifact diffs vs prior version. Cite specific Joe/IWM/Peter delta numbers.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-validate INF_C_01 — exit 0 required before gold artifacts ship</tool>
    <tool>comp-pipescript deployed INF_C_01 — MATCH check post any code change</tool>
    <tool>comp-pipescript io INF_C_01 — confirm canonical input/output schema</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">canonical_nna parquets rebuilt for full historical range (or chosen narrower range).</criterion>
    <criterion id="AC2">Sample Q2 2026 canonical_nna shows Joe Brandenburg with non-zero NNA, IWM normalized to small share.</criterion>
    <criterion id="AC3">platinum/firm/nmec_nmnc_nna.json: Joe present, IWM ≤ 5% of firm AUA, sum of advisors == firm.</criterion>
    <criterion id="AC4">platinum/firm/leaderboard.json: 4 entries, Joe non-zero NNA.</criterion>
    <criterion id="AC5">NMNC/NNA reconciliation sanity: Q2 NMNC ≈ Q2 firm NNA from new-client accounts (within 10% — exact match unlikely due to flow timing).</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>INFNNA.SILVER must complete (at minimum tax + transactions + accounts_v2 silvers must be present for historical date range).</upstream>
    <downstream>INFNNA.PORTAL-VERIFY consumes the new platinum artifacts.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~18:00Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Pre-authorized. Begin once INFNNA.SILVER produces sufficient silver coverage. RAVC at canonical_nna rebuild + each gold script re-run.</message>
  </go_signal>
</task_order>
