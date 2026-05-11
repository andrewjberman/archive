<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFTGT.TO-8</id>
    <project>ADVI_INFTGT</project>
    <title>INF_D_05 activity_scan + INF_D_06 cash_drag actually compute (fix zero-rows emit)</title>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>complete</status>
    <priority>P1 (Andrew direct — 1hr deadline)</priority>
    <authorized_by>Andrew direct 2026-05-11 — "no queuing for tomorrow, we address this now" + 1hr deadline (relayed via 2.0.0_SA_COO)</authorized_by>
    <closure_via>commit 147b85326 + S3 MATCH both files</closure_via>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFTGT_PRD.md §4.3 + §6.TO-8</ref>
    <ref type="parent">ADVI_INFTGT parallel sprint (slot 3 of 4: DS~A TO-7 / DS~B TO-2b+4b / DS~D TO-5)</ref>
    <ref type="affected_artifact">s3://opal-data-inf/platinum/firm/activity_scan.json + cash_drag.json</ref>
  </references>

  <context>
    Both `activity_scan.json` and `cash_drag.json` were emitting rows of all-zero values
    (aua=0, txn_count_12m=0, activity_score≈0.5016, segment="buy_and_hold" for activity;
    aua=0, cash_aua=0, cash_pct=0 for cash drag). Frontend renders this as "Awaiting data"
    empty-state per PRD §4.3.

    Investigation surfaced three distinct findings:
    1. INF_D_05 tz-aware vs tz-naive Timestamp comparison silently dropped all 1,510 TRN
       partitions through the executor try/except (script-level bug).
    2. Both scripts read `gold/holdings/{keys[-1]}.parquet` without verifying upstream
       health — vulnerable to INF_B_01 zero-MV regression (empirical 2026-05-06..08).
    3. PRD §4.3 empty-state convention not codified in scripts.

    Per COO architectural-parity directive (received 20:50Z): partner-facing total_aua
    should align with canonical AUA source (per DS~B's parallel investigation,
    `gold/timeseries/client_performance.parquet`).
  </context>

  <scope>
    <step>comp-pipescript io INF_D_05 + INF_D_06 (catalog naming-collision surfaced; manual source reads).</step>
    <step>comp-trace txn_count_12m --direction both (skipped; root cause already empirically diagnosed via local dry-run telemetry).</step>
    <step>Empirical diagnosis: standalone dry-run of both scripts against current silver+gold state.</step>
    <step>Fix tz comparison in INF_D_05.load_txns_12m (cutoff_date = tz_localize(None)).</step>
    <step>Switch INF_D_05 AUA source to canonical client_performance.parquet with walk-back to latest non-zero AUA date.</step>
    <step>Add bounded walk-back (14-key max) in INF_D_06.list_holdings_keys for "current" snapshot.</step>
    <step>Add PRD §4.3 empty-state gate to both scripts.</step>
    <step>Pre-commit gate + safe-commit + push (safe-deploy hook auto-S3-deploys + verifies SHA).</step>
    <step>Manual SHA cross-check both files MATCH.</step>
    <step>Standalone re-run validation: real values emitted for both artifacts.</step>
    <step>RAVC4 to COO with commit SHA + S3 SHAs + standalone validation evidence + upstream regression flag.</step>
  </scope>

  <acceptance_criteria>
    1. Activity Scan top-rows have non-zero AUA and txn counts where Orion data exists.
       MET — top HH 463: $4.44M AUA / 1,147 txn / activity_score 0.7098 / segment=active.
    2. Cash Drag top-rows have non-zero cash_aua + cash_pct where holdings have non-zero MV.
       MET — top HH 1367: $109K AUA / 100% cash_pct / $109K cash_aua / 2 days above threshold.
    3. UI surfaces top-N (not "Awaiting data") on next authorized chain rerun.
       PENDING chain rerun — code-path validated locally on current data.
    4. Pre-commit gate exits 0 for both files.
       MET — py_compile + AST + ruff py39 all PASS.
    5. S3 MATCH verified for both files post-push.
       MET — safe-deploy hook auto-verified; manual cross-check confirmed.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>comp-pipescript io INF_D_05</run><expect>I/O manifest for activity_scan.py.</expect><observed>Catalog naming-collision: returned INF_D_05.client_top_holdings.py manifest, not activity_scan. Fell back to direct source read.</observed></step>
      <step><run>comp-pipescript io INF_D_06</run><expect>I/O manifest for cash_drag.py.</expect><observed>Same catalog naming-collision (returned INF_D_06.client_timeseries.py). Direct source read used.</observed></step>
      <step><run>comp-trace txn_count_12m --direction both</run><expect>Locate missing transaction source.</expect><observed>SKIPPED — local dry-run telemetry showed tz comparison as immediate root cause, no trace needed.</observed></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>.tools/ds-commit-gate.sh INF_D_05.activity_scan.py INF_D_06.cash_drag.py</run><expect>Exit 0 per file.</expect><observed>PASS for both — py_compile + AST + ruff py39.</observed></step>
      <step><run>Standalone python rerun against current silver+gold (boto3 fetch)</run><expect>Non-zero rows in artifact.</expect><observed>INF_D_05: 305 HHs / 263,812 TRN rows / median 752 / active 152 / buy_and_hold 153 / firm AUA $189.7M. INF_D_06: 293 HHs / 92 above 5% cash threshold / firm AUA $189.85M / cash $14.5M.</observed></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>Manual hashlib.sha256 cross-check both files local vs s3://opal-data-inf/code/gold/</run><expect>MATCH both files.</expect><observed>INF_D_05: 79f8b45d3e139459 MATCH. INF_D_06: f1f9eed38339ec95 MATCH.</observed></step>
      <step><run>comp-validate INF_D_05 --artifact /tmp/activity_scan.json</run><expect>Exit 0.</expect><observed>SKIPPED — chain rerun on HOLD per Andrew; no fresh artifact on S3 yet. Local validation is the agreed gate.</observed></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None code-wise. Upstream INF_B_01 zero-MV regression is OUT OF SCOPE for TO-8;
    surfaced separately to COO for routing.
  </dependencies>

  <followups>
    <followup priority="high">INF_B_01 priced daily holdings regression — 3 consecutive days (2026-05-06..08) have price=0 firm-wide. Defensive walk-back in TO-8 fix tolerates it, but root cause needs addressing for partner-facing AUA accuracy on every downstream consumer that reads gold/holdings/{latest}.</followup>
    <followup priority="low">comp-pipescript io catalog naming-collision: INF_D_05 prefix returns client_top_holdings, INF_D_06 returns client_timeseries (instead of the activity_scan + cash_drag pair). Bundle into existing INF_COMP_PIPESCRIPT_DEPLOYED_COVERAGE follow-up from DS~B.</followup>
  </followups>

  <next>Standdown DS~C after RAVC4 close per COO authorization 20:50Z.</next>
</task_order>
