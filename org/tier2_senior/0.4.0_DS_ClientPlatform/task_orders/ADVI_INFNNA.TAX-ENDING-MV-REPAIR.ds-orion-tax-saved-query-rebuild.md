<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.TAX-ENDING-MV-REPAIR</id>
    <project>ADVI_INFNNA</project>
    <title>Orion tax saved-query rebuild — restore Ending MV column dropped from bronze 2026-05-07+ (mirror PERFDIM-CREATOR pattern)</title>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status>
    <priority>medium</priority>
    <estimated_effort>~45-75 min</estimated_effort>
  </metadata>

  <references>
    <ref type="parent_ravc">DS~A RAVC3 INFNNA.SILVER 4-issue triage 2026-05-08T~14:00Z — Issue 3 root cause</ref>
    <ref type="defensive_fix_already_in_place">DS~A `a0bccb306` 2026-05-08 — defensive `_safe_sum` in build_tax_dim.py main(); silver builds succeed with ending_mv=0 when bronze column missing</ref>
    <ref type="anchor_pattern">PERFDIM-CREATOR `94c624901` 2026-05-08 (DS~A) — clone Tax Dim verbose template + restore Activity Option (additionalOptions=13)</ref>
    <ref type="empirical_evidence">2026-05-06 tax_unrealized.csv: 33 cols including Ending MV at position 11. 2026-05-07 + 2026-05-08: 32 cols, Ending MV ABSENT. Saved-query regression somewhere between 05-06 and 05-07.</ref>
  </references>

  <context>
    Tax `Ending MV` column dropped from Orion saved-query output between 2026-05-06 and 2026-05-07. Defensive `_safe_sum` fix shipped (`a0bccb306`) means silver builds succeed but `ending_mv = 0` for all dates from 2026-05-07+ in silver/api_dims/tax_unrealized/.

    **Non-blocking for INFNNA.GOLD** (canonical NNA derives from transactions + billing, not tax ending_mv directly). But silver tax_unrealized loses a meaningful field for downstream use (tax-related dashboards, ending market value reporting).

    **Pattern: PERFDIM-CREATOR** — DS~A's earlier fix today for the performance dim saved query. Same class of bug:
    - Saved query in Orion has additionalOptions = N
    - N is missing the Activity Option that produces the field we need
    - Fix: clone the verbose template, set additionalOptions correctly, recreate the saved query
    - PERFDIM-CREATOR used `additionalOptions=13` cloned from Billing Dim verbose `6a6a0354-ac63-47f9-bfc6-c769266abe04`

    For tax: identify which additionalOptions value includes "Ending MV"; recreate the saved query with that value; verify a recent date returns Ending MV in the bronze CSV; remove `_safe_sum` defensive fallback from build_tax_dim.py once verified (or leave defensive — non-urgent cleanup).

    **Reprocess scope:** silver tax_unrealized for 2026-05-07+ dates can be rebuilt from new bronze if desired (small wall-clock). Or accept ending_mv=0 for those ~2 dates and only flow forward correctly. Decision per DS~D after seeing the fix work on a fresh date.
  </context>

  <scope>
    <step>
      Identify the current tax saved query: read `data/orion/manual_api/create_tax_dim_queries.py` (line 45 INFLECTION_REP_IDS — note this is OLD `[3, 11, 12]` per SEED-INF drift; not your TO scope but flag in RAVC). Look for the saved-query creation function and current additionalOptions value.
    </step>

    <step>
      Clone PERFDIM-CREATOR pattern: examine `pull_inflection_performance_dim.py` (or wherever the saved-query was rebuilt today) to see the additionalOptions=13 pattern. The Billing Dim verbose template `6a6a0354-ac63-47f9-bfc6-c769266abe04` is the working source.
    </step>

    <step>
      Determine which Activity Option includes "Ending MV" for tax dim. Likely candidates:
      - Look at the Orion API documentation OR
      - Empirically test additionalOptions values (1, 3, 7, 13, 15, 31) by calling the tax saved query with each value and inspecting which one returns the Ending MV column
      - Or: clone the verbose Tax Dim template (similar to Billing Dim verbose) and find its additionalOptions value

      Pre-commit gate: any code change to `data/orion/manual_api/*.py` requires `.tools/ds-commit-gate.sh`.
    </step>

    <step>
      Recreate the tax saved query in Orion with corrected additionalOptions:
      - Use Orion REST API to delete existing tax saved query (or version it)
      - Create new saved query with verified additionalOptions including Ending MV
      - Capture saved-query GUID + name for documentation

      Test: pull bronze for 2026-05-07 OR 2026-05-08 with new saved query. Verify `Ending MV` column present in CSV.
    </step>

    <step>
      Optional: rebuild silver tax_unrealized for 2026-05-07 + 2026-05-08 from new bronze. Re-run `build_tax_dim.py` for those dates. Verify `ending_mv` non-zero in silver Parquet.

      OR document the known $0-ending_mv state for those 2 dates in TO close-out and leave defensive fix in place (lighter touch).
    </step>

    <step>
      Commit `data/orion/manual_api/create_tax_dim_queries.py` (or whichever script changed). Push. Update saved-query GUID in any reference docs.

      RAVC2 to COO with: new saved-query GUID + bronze 2026-05-08 verification + (if rebuilt) silver verification.
    </step>
  </scope>

  <acceptance_criteria>
    1. Tax saved-query recreated with corrected additionalOptions; new GUID captured.
    2. Empirical: bronze pull for 2026-05-07 OR 2026-05-08 returns CSV with `Ending MV` column present.
    3. Pre-commit gate (`.tools/ds-commit-gate.sh`) PASS on any modified script.
    4. (Optional) Silver tax_unrealized for 2026-05-07/08 rebuilt with ending_mv non-zero — OR documented known state per DS~D judgment.
    5. Session log Compiler Tools section reproduces each `<run>` with observed output + pass/fail.
    6. RAVC2 to COO with: saved-query GUID, bronze CSV column-list before/after, silver rebuild status (yes/no/deferred).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>aws s3 cp s3://opal-data-inf/bronze/orion-api/2026-05-08/tax_unrealized.csv /tmp/tax_post.csv 2>&amp;1 &amp;&amp; head -1 /tmp/tax_post.csv | tr ',' '\n' | wc -l</run>
        <expect>Returns 32 (no Ending MV). Confirms current bronze state shows the missing column.</expect>
        <if_mismatch>If returns 33 (Ending MV present): saved-query may have already been fixed; verify with column name grep before authoring code.</if_mismatch>
      </step>
      <step>
        <run>aws s3 cp s3://opal-data-inf/bronze/orion-api/2026-05-06/tax_unrealized.csv /tmp/tax_pre.csv 2>&amp;1 &amp;&amp; head -1 /tmp/tax_pre.csv | grep -c "Ending MV"</run>
        <expect>Returns 1 (Ending MV present in pre-regression date). Confirms pre-2026-05-07 baseline.</expect>
        <if_mismatch>If returns 0: column rename happened earlier than thought; investigate further back.</if_mismatch>
      </step>
      <step>
        <run>git log --oneline --all data/orion/manual_api/pull_inflection_performance_dim.py | head -3</run>
        <expect>Returns commits including PERFDIM-CREATOR fix `94c624901`. Read for additionalOptions=13 pattern.</expect>
        <if_mismatch>If no PERFDIM-CREATOR commit: check git log on `create_*_dim_queries.py` instead.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>aws s3 ls s3://opal-data-inf/bronze/orion-api/2026-05-08/tax_unrealized.csv 2>&amp;1 &amp;&amp; aws s3 cp s3://opal-data-inf/bronze/orion-api/2026-05-08/tax_unrealized.csv /tmp/tax_after.csv &amp;&amp; head -1 /tmp/tax_after.csv | grep -c "Ending MV"</run>
        <expect>Returns 1 (Ending MV present in post-fix bronze).</expect>
        <if_mismatch>If 0 still: saved-query change didn't propagate; debug.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <reprocess_required>
      Bronze: trigger fresh pull on 2026-05-08 (or accept tomorrow's natural cron run). Silver: optional re-run for 2026-05-07/08 dates per DS~D judgment.
    </reprocess_required>
  </data_reprocess_scope>

  <dependencies>
    None. Parallel-dispatchable with FOLLOWUP-1 (DS~B) + FOLLOWUP-2 (DS~C) + perf backfill (DS~A).
  </dependencies>
</task_order>
